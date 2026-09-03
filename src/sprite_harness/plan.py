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

from .jsonio import json_compat_problems
from .spec import SpecLoadError


ANCHOR_TYPES = ("bottom_center", "center", "custom")
REDUCED_MOTION_MODES = ("full", "hold_first_frame")

# The one reserved track target: transforms that move the whole sprite.
# Only translate tracks targeting it contribute to the aggregate frame offset;
# every other target is a semantic part label a layered renderer may honor.
SPRITE_TARGET = "sprite"

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
class Layer:
    target: str
    source_image: str
    anchor_type: str
    anchor_x: float | None
    anchor_y: float | None
    position_x: float
    position_y: float
    source_sha256: str | None = None
    source_width: int | None = None
    source_height: int | None = None


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
    source_sha256: str | None
    source_width: int | None
    source_height: int | None
    seed: int | None
    max_displacement_px: float | None
    max_frame_delta_px: float | None
    reduced_motion: str
    tracks: tuple[Track, ...]
    events: tuple[PlanEvent, ...]
    metadata: dict[str, Any]
    spec_path: Path
    layers: tuple[Layer, ...] | None = None
    reference_width: int | None = None
    reference_height: int | None = None

    @property
    def layered(self) -> bool:
        return self.layers is not None

    def protected_paths(self) -> tuple[Path, ...]:
        """All immutable runtime inputs, including the layer description."""
        images = ((self.spec_dir / layer.source_image).resolve() for layer in self.layers or ())
        single = self.resolved_source_path()
        return (self.spec_path, *images, *((single,) if single else ()))

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
    unknown = sorted(str(key) for key in set(mapping) - allowed)
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
    try:
        return float(value)
    except OverflowError:
        # Semantic finite-value validation reports this with strict JSON diagnostics.
        return float("-inf") if value < 0 else float("inf")


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


def _load_layer(raw: Any, index: int, path: Path) -> Layer:
    field = f"source.layers[{index}]"
    layer = _mapping(raw, field, path)
    _reject_unknown(layer, {"target", "image", "anchor", "position", "sha256", "width", "height"}, field, path)
    anchor = _mapping(_required(layer, "anchor", path), f"{field}.anchor", path)
    _reject_unknown(anchor, {"type", "x", "y"}, f"{field}.anchor", path)
    position = _mapping(_required(layer, "position", path), f"{field}.position", path)
    _reject_unknown(position, {"x", "y"}, f"{field}.position", path)
    return Layer(
        target=_string(_required(layer, "target", path), f"{field}.target", path),
        source_image=_string(_required(layer, "image", path), f"{field}.image", path),
        anchor_type=_string(_required(anchor, "type", path), f"{field}.anchor.type", path),
        anchor_x=_number(anchor["x"], f"{field}.anchor.x", path) if "x" in anchor else None,
        anchor_y=_number(anchor["y"], f"{field}.anchor.y", path) if "y" in anchor else None,
        position_x=_number(_required(position, "x", path), f"{field}.position.x", path),
        position_y=_number(_required(position, "y", path), f"{field}.position.y", path),
        source_sha256=_string(layer["sha256"], f"{field}.sha256", path) if "sha256" in layer else None,
        source_width=_integer(layer["width"], f"{field}.width", path) if "width" in layer else None,
        source_height=_integer(layer["height"], f"{field}.height", path) if "height" in layer else None,
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
    source_sha256: str | None = None
    source_width: int | None = None
    source_height: int | None = None
    layers = None
    reference_width = reference_height = None
    if "source" in data and isinstance(data["source"], dict) and "layers" in data["source"]:
        source = data["source"]
        if "image" in source:
            raise SpecLoadError("SOURCE_MODE_CONFLICT", "source.image and source.layers are mutually exclusive.", path=path)
        _reject_unknown(source, {"layers", "reference_canvas"}, "source", path)
        reference = _mapping(_required(source, "reference_canvas", path), "source.reference_canvas", path)
        _reject_unknown(reference, {"width", "height"}, "source.reference_canvas", path)
        reference_width = _integer(_required(reference, "width", path), "source.reference_canvas.width", path)
        reference_height = _integer(_required(reference, "height", path), "source.reference_canvas.height", path)
        if not isinstance(source["layers"], list):
            raise SpecLoadError("MALFORMED_SPEC", "source.layers must be an array.", path=path)
        layers = tuple(_load_layer(raw, index, path) for index, raw in enumerate(source["layers"]))
    elif "source" in data:
        source = _mapping(data["source"], "source", path)
        _reject_unknown(source, {"image", "sha256", "width", "height"}, "source", path)
        source_image = _string(_required(source, "image", path, parent="source"), "source.image", path)
        if "sha256" in source:
            source_sha256 = _string(source["sha256"], "source.sha256", path)
        if "width" in source:
            source_width = _integer(source["width"], "source.width", path)
        if "height" in source:
            source_height = _integer(source["height"], "source.height", path)

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
    metadata_problems = json_compat_problems(metadata, "metadata")
    if metadata_problems:
        raise SpecLoadError(
            "METADATA_NOT_JSON_COMPATIBLE",
            "Field 'metadata' must contain only JSON-compatible values "
            "(null, booleans, integers, finite floats, strings, arrays, "
            "objects with string keys).",
            path=path,
            details={"problems": metadata_problems},
        )

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
        source_sha256=source_sha256,
        source_width=source_width,
        source_height=source_height,
        seed=seed,
        max_displacement_px=max_displacement_px,
        max_frame_delta_px=max_frame_delta_px,
        reduced_motion=reduced_motion,
        tracks=tuple(_load_track(raw, index, path) for index, raw in enumerate(raw_tracks)),
        events=tuple(_load_event(raw, index, path) for index, raw in enumerate(raw_events)),
        metadata=metadata,
        spec_path=path,
        layers=layers,
        reference_width=reference_width,
        reference_height=reference_height,
    )


def resolved_anchor(plan: AnimationPlan | Layer) -> tuple[float, float]:
    """Normalized anchor coordinates implied by the anchor type."""

    if plan.anchor_type == "bottom_center":
        return (0.5, 1.0)
    if plan.anchor_type == "center":
        return (0.5, 0.5)
    return (plan.anchor_x if plan.anchor_x is not None else 0.5,
            plan.anchor_y if plan.anchor_y is not None else 1.0)
