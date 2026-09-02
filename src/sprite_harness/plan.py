"""Animation Plan loading and typed in-memory representation.

An Animation Plan (动画计划) is the declarative intermediate representation
between a static source sprite and a rendered frame set. Loading enforces shape
only (types, required fields, unknown-field rejection); value-level checks live
in :mod:`sprite_harness.plan_validator`.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

import yaml

from .spec import SpecLoadError


ANCHOR_TYPES = ("bottom_center", "center", "custom")
REDUCED_MOTION_MODES = ("full", "hold_first_frame")

# motion -> required unit
SUPPORTED_MOTIONS = {
    "translate_x": "px",
    "translate_y": "px",
    "rotate": "deg",
    "scale": "ratio",
    "opacity": "ratio",
}


@dataclass(frozen=True)
class Track:
    track_id: str
    target: str
    motion: str
    amplitude: float
    unit: str
    curve: str = "sine"
    cycles: float = 1.0
    phase: float = 0.0


@dataclass(frozen=True)
class PlanEvent:
    event_id: str
    type: str
    frames: tuple[int, ...]
    target: str | None = None


@dataclass(frozen=True)
class AnimationPlan:
    version: int
    animation_id: str
    fps: float
    frame_count: int
    loop: bool
    anchor_type: str
    anchor_x: float | None
    anchor_y: float | None
    canvas_width: int | None
    canvas_height: int | None
    background: str
    source_image: str | None
    seed: int | None
    max_displacement_px: float | None
    max_frame_delta_px: float | None
    reduced_motion: str
    tracks: tuple[Track, ...]
    events: tuple[PlanEvent, ...]
    metadata: dict[str, Any]
    spec_path: Path

    @property
    def spec_dir(self) -> Path:
        return self.spec_path.parent

    def resolved_source_path(self, override: Path | None = None) -> Path | None:
        """Source image path, preferring an explicit CLI override."""

        if override is not None:
            return override.expanduser().resolve()
        if self.source_image is None:
            return None
        return (self.spec_dir / self.source_image).resolve()


def _read_mapping(path: Path) -> dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise SpecLoadError(
            "SPEC_READ_ERROR", f"Could not read animation plan: {exc}", path=path
        ) from exc
    try:
        if path.suffix.lower() == ".json":
            data = json.loads(text)
        else:
            data = yaml.safe_load(text)
    except (json.JSONDecodeError, yaml.YAMLError) as exc:
        raise SpecLoadError(
            "MALFORMED_SPEC", f"Animation plan syntax is invalid: {exc}", path=path
        ) from exc
    if not isinstance(data, dict):
        raise SpecLoadError(
            "MALFORMED_SPEC", "Animation plan root must be an object.", path=path
        )
    return data


def _mapping(value: Any, field: str, path: Path) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise SpecLoadError("MALFORMED_SPEC", f"Field '{field}' must be an object.", path=path)
    return value


def _required(mapping: dict[str, Any], field: str, path: Path, *, parent: str = "") -> Any:
    if field not in mapping:
        name = f"{parent}.{field}" if parent else field
        raise SpecLoadError(
            "MALFORMED_SPEC", f"Required field '{name}' is missing.", path=path
        )
    return mapping[field]


def _reject_unknown(
    mapping: dict[str, Any], allowed: set[str], field: str, path: Path
) -> None:
    unknown = sorted(set(mapping) - allowed)
    if unknown:
        raise SpecLoadError(
            "MALFORMED_SPEC",
            f"Field '{field}' contains unsupported properties: {', '.join(unknown)}.",
            path=path,
            details={"field": field, "properties": unknown},
        )


def _number(value: Any, field: str, path: Path) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise SpecLoadError("MALFORMED_SPEC", f"Field '{field}' must be a number.", path=path)
    return float(value)


def _integer(value: Any, field: str, path: Path) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise SpecLoadError("MALFORMED_SPEC", f"Field '{field}' must be an integer.", path=path)
    return value


def _string(value: Any, field: str, path: Path) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SpecLoadError(
            "MALFORMED_SPEC", f"Field '{field}' must be a non-empty string.", path=path
        )
    return value


def _boolean(value: Any, field: str, path: Path) -> bool:
    if not isinstance(value, bool):
        raise SpecLoadError("MALFORMED_SPEC", f"Field '{field}' must be a boolean.", path=path)
    return value


def _load_track(raw: Any, index: int, path: Path) -> Track:
    field = f"tracks[{index}]"
    track = _mapping(raw, field, path)
    _reject_unknown(
        track,
        {"track_id", "target", "motion", "amplitude", "unit", "curve", "cycles", "phase"},
        field,
        path,
    )
    return Track(
        track_id=_string(_required(track, "track_id", path, parent=field), f"{field}.track_id", path),
        target=_string(_required(track, "target", path, parent=field), f"{field}.target", path),
        motion=_string(_required(track, "motion", path, parent=field), f"{field}.motion", path),
        amplitude=_number(
            _required(track, "amplitude", path, parent=field), f"{field}.amplitude", path
        ),
        unit=_string(_required(track, "unit", path, parent=field), f"{field}.unit", path),
        curve=_string(track.get("curve", "sine"), f"{field}.curve", path),
        cycles=_number(track.get("cycles", 1), f"{field}.cycles", path),
        phase=_number(track.get("phase", 0), f"{field}.phase", path),
    )


def _load_event(raw: Any, index: int, path: Path) -> PlanEvent:
    field = f"events[{index}]"
    event = _mapping(raw, field, path)
    _reject_unknown(event, {"event_id", "type", "target", "frames"}, field, path)
    raw_frames = _required(event, "frames", path, parent=field)
    if not isinstance(raw_frames, list) or not raw_frames:
        raise SpecLoadError(
            "MALFORMED_SPEC", f"Field '{field}.frames' must be a non-empty array.", path=path
        )
    frames = tuple(
        _integer(item, f"{field}.frames[{position}]", path)
        for position, item in enumerate(raw_frames)
    )
    target = event.get("target")
    if target is not None:
        target = _string(target, f"{field}.target", path)
    return PlanEvent(
        event_id=_string(_required(event, "event_id", path, parent=field), f"{field}.event_id", path),
        type=_string(_required(event, "type", path, parent=field), f"{field}.type", path),
        frames=frames,
        target=target,
    )


def load_plan(plan_path: str | Path) -> AnimationPlan:
    """Load a JSON or YAML Animation Plan into the typed representation."""

    path = Path(plan_path).expanduser()
    if not path.is_file():
        raise SpecLoadError("INPUT_NOT_FOUND", "Animation plan file does not exist.", path=path)
    path = path.resolve()
    data = _read_mapping(path)
    _reject_unknown(
        data,
        {
            "plan_version",
            "animation_id",
            "source",
            "canvas",
            "playback",
            "anchor",
            "seed",
            "constraints",
            "reduced_motion",
            "tracks",
            "events",
            "metadata",
        },
        "root",
        path,
    )

    playback = _mapping(_required(data, "playback", path), "playback", path)
    _reject_unknown(playback, {"fps", "frame_count", "loop"}, "playback", path)

    source_image: str | None = None
    if "source" in data:
        source = _mapping(data["source"], "source", path)
        _reject_unknown(source, {"image"}, "source", path)
        source_image = _string(_required(source, "image", path, parent="source"), "source.image", path)

    canvas_width: int | None = None
    canvas_height: int | None = None
    background = "transparent"
    if "canvas" in data:
        canvas = _mapping(data["canvas"], "canvas", path)
        _reject_unknown(canvas, {"width", "height", "background"}, "canvas", path)
        canvas_width = _integer(_required(canvas, "width", path, parent="canvas"), "canvas.width", path)
        canvas_height = _integer(
            _required(canvas, "height", path, parent="canvas"), "canvas.height", path
        )
        if "background" in canvas:
            background = _string(canvas["background"], "canvas.background", path)

    anchor_type = "bottom_center"
    anchor_x: float | None = None
    anchor_y: float | None = None
    if "anchor" in data:
        anchor = _mapping(data["anchor"], "anchor", path)
        _reject_unknown(anchor, {"type", "x", "y"}, "anchor", path)
        anchor_type = _string(_required(anchor, "type", path, parent="anchor"), "anchor.type", path)
        if "x" in anchor:
            anchor_x = _number(anchor["x"], "anchor.x", path)
        if "y" in anchor:
            anchor_y = _number(anchor["y"], "anchor.y", path)

    seed: int | None = None
    if "seed" in data:
        seed = _integer(data["seed"], "seed", path)

    max_displacement_px: float | None = None
    max_frame_delta_px: float | None = None
    if "constraints" in data:
        constraints = _mapping(data["constraints"], "constraints", path)
        _reject_unknown(
            constraints, {"max_displacement_px", "max_frame_delta_px"}, "constraints", path
        )
        if "max_displacement_px" in constraints:
            max_displacement_px = _number(
                constraints["max_displacement_px"], "constraints.max_displacement_px", path
            )
        if "max_frame_delta_px" in constraints:
            max_frame_delta_px = _number(
                constraints["max_frame_delta_px"], "constraints.max_frame_delta_px", path
            )

    reduced_motion = "full"
    if "reduced_motion" in data:
        reduced = _mapping(data["reduced_motion"], "reduced_motion", path)
        _reject_unknown(reduced, {"mode"}, "reduced_motion", path)
        reduced_motion = _string(
            _required(reduced, "mode", path, parent="reduced_motion"), "reduced_motion.mode", path
        )

    raw_tracks = data.get("tracks", [])
    if not isinstance(raw_tracks, list):
        raise SpecLoadError("MALFORMED_SPEC", "Field 'tracks' must be an array.", path=path)
    raw_events = data.get("events", [])
    if not isinstance(raw_events, list):
        raise SpecLoadError("MALFORMED_SPEC", "Field 'events' must be an array.", path=path)

    metadata = data.get("metadata", {})
    if not isinstance(metadata, dict):
        raise SpecLoadError("MALFORMED_SPEC", "Field 'metadata' must be an object.", path=path)

    return AnimationPlan(
        version=_integer(_required(data, "plan_version", path), "plan_version", path),
        animation_id=_string(_required(data, "animation_id", path), "animation_id", path),
        fps=_number(_required(playback, "fps", path, parent="playback"), "playback.fps", path),
        frame_count=_integer(
            _required(playback, "frame_count", path, parent="playback"),
            "playback.frame_count",
            path,
        ),
        loop=_boolean(
            _required(playback, "loop", path, parent="playback"), "playback.loop", path
        ),
        anchor_type=anchor_type,
        anchor_x=anchor_x,
        anchor_y=anchor_y,
        canvas_width=canvas_width,
        canvas_height=canvas_height,
        background=background,
        source_image=source_image,
        seed=seed,
        max_displacement_px=max_displacement_px,
        max_frame_delta_px=max_frame_delta_px,
        reduced_motion=reduced_motion,
        tracks=tuple(_load_track(raw, index, path) for index, raw in enumerate(raw_tracks)),
        events=tuple(_load_event(raw, index, path) for index, raw in enumerate(raw_events)),
        metadata=metadata,
        spec_path=path,
    )


def resolved_anchor(plan: AnimationPlan) -> tuple[float, float]:
    """Normalized anchor coordinates implied by the anchor type."""

    if plan.anchor_type == "bottom_center":
        return (0.5, 1.0)
    if plan.anchor_type == "center":
        return (0.5, 0.5)
    return (plan.anchor_x if plan.anchor_x is not None else 0.5,
            plan.anchor_y if plan.anchor_y is not None else 1.0)
