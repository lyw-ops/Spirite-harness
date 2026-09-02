"""Animation specification loading and typed in-memory representation."""

from __future__ import annotations

from dataclasses import dataclass
import json
import math
from pathlib import Path
import re
from typing import Any

import yaml


SPEC_FILENAMES = ("animation.yaml", "animation.yml", "animation.json")


@dataclass(frozen=True)
class FrameSpec:
    file: str
    duration: float
    action: str | None = None


@dataclass(frozen=True)
class AnimationSpec:
    version: int
    id: str
    character_id: str
    state_id: str
    canvas_width: int
    canvas_height: int
    background: str
    anchor_x: float
    anchor_y: float
    fps: float
    loop: bool
    frames: tuple[FrameSpec, ...]
    spec_path: Path
    animation_dir: Path

    @property
    def canvas_size(self) -> tuple[int, int]:
        return (self.canvas_width, self.canvas_height)

    def frame_path(self, frame: FrameSpec) -> Path:
        return (self.animation_dir / frame.file).resolve()


class SpecLoadError(Exception):
    """An input cannot be represented as an animation specification."""

    def __init__(
        self,
        code: str,
        message: str,
        *,
        path: Path | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.path = path
        self.details = details or {}

    def as_error(self) -> dict[str, Any]:
        error: dict[str, Any] = {"code": self.code, "message": self.message}
        if self.path is not None:
            error["path"] = str(self.path)
        error.update(self.details)
        return error


def resolve_spec_path(animation: str | Path) -> Path:
    candidate = Path(animation).expanduser()
    if not candidate.exists():
        raise SpecLoadError(
            "INPUT_NOT_FOUND", "Animation input does not exist.", path=candidate
        )
    if candidate.is_file():
        return candidate.resolve()
    if not candidate.is_dir():
        raise SpecLoadError(
            "INPUT_NOT_FOUND", "Animation input is not a file or directory.", path=candidate
        )

    matches = [candidate / name for name in SPEC_FILENAMES if (candidate / name).is_file()]
    if not matches:
        raise SpecLoadError(
            "SPEC_NOT_FOUND",
            f"No animation specification found; expected one of: {', '.join(SPEC_FILENAMES)}.",
            path=candidate.resolve(),
        )
    if len(matches) > 1:
        raise SpecLoadError(
            "AMBIGUOUS_SPEC",
            "Animation directory contains more than one supported specification file.",
            path=candidate.resolve(),
            details={"candidates": [str(path.resolve()) for path in matches]},
        )
    return matches[0].resolve()


def _read_mapping(path: Path) -> dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise SpecLoadError(
            "SPEC_READ_ERROR", f"Could not read specification: {exc}", path=path
        ) from exc

    try:
        if path.suffix.lower() == ".json":
            data = json.loads(text)
        else:
            data = yaml.safe_load(text)
    except (json.JSONDecodeError, yaml.YAMLError) as exc:
        raise SpecLoadError(
            "MALFORMED_SPEC", f"Specification syntax is invalid: {exc}", path=path
        ) from exc

    if not isinstance(data, dict):
        raise SpecLoadError(
            "MALFORMED_SPEC", "Specification root must be an object.", path=path
        )
    return data


def _mapping(value: Any, field: str, path: Path) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise SpecLoadError(
            "MALFORMED_SPEC", f"Field '{field}' must be an object.", path=path
        )
    return value


def _required(mapping: dict[str, Any], field: str, path: Path) -> Any:
    if field not in mapping:
        raise SpecLoadError(
            "MALFORMED_SPEC", f"Required field '{field}' is missing.", path=path
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
        raise SpecLoadError(
            "MALFORMED_SPEC", f"Field '{field}' must be a number.", path=path
        )
    return float(value)


def _integer(value: Any, field: str, path: Path) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise SpecLoadError(
            "MALFORMED_SPEC", f"Field '{field}' must be an integer.", path=path
        )
    return value


def _string(value: Any, field: str, path: Path) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SpecLoadError(
            "MALFORMED_SPEC", f"Field '{field}' must be a non-empty string.", path=path
        )
    return value


def load_spec(animation: str | Path) -> AnimationSpec:
    """Load YAML or JSON into a typed spec; semantic checks happen separately."""

    path = resolve_spec_path(animation)
    data = _read_mapping(path)
    _reject_unknown(
        data,
        {"version", "id", "character", "state", "canvas", "anchor", "playback", "frames"},
        "root",
        path,
    )
    character = _mapping(_required(data, "character", path), "character", path)
    state = _mapping(_required(data, "state", path), "state", path)
    canvas = _mapping(_required(data, "canvas", path), "canvas", path)
    anchor = _mapping(_required(data, "anchor", path), "anchor", path)
    playback = _mapping(_required(data, "playback", path), "playback", path)
    _reject_unknown(character, {"id"}, "character", path)
    _reject_unknown(state, {"id"}, "state", path)
    _reject_unknown(canvas, {"width", "height", "background"}, "canvas", path)
    _reject_unknown(anchor, {"x", "y"}, "anchor", path)
    _reject_unknown(playback, {"fps", "loop"}, "playback", path)

    raw_frames = _required(data, "frames", path)
    if not isinstance(raw_frames, list):
        raise SpecLoadError(
            "MALFORMED_SPEC", "Field 'frames' must be an array.", path=path
        )

    frames: list[FrameSpec] = []
    for index, raw_frame in enumerate(raw_frames):
        frame = _mapping(raw_frame, f"frames[{index}]", path)
        _reject_unknown(frame, {"file", "duration", "action"}, f"frames[{index}]", path)
        action = frame.get("action")
        if action is not None and not isinstance(action, str):
            raise SpecLoadError(
                "MALFORMED_SPEC",
                f"Field 'frames[{index}].action' must be a string when present.",
                path=path,
            )
        frames.append(
            FrameSpec(
                file=_string(
                    _required(frame, "file", path), f"frames[{index}].file", path
                ),
                duration=_number(
                    _required(frame, "duration", path),
                    f"frames[{index}].duration",
                    path,
                ),
                action=action,
            )
        )

    loop = _required(playback, "loop", path)
    if not isinstance(loop, bool):
        raise SpecLoadError(
            "MALFORMED_SPEC", "Field 'playback.loop' must be a boolean.", path=path
        )

    return AnimationSpec(
        version=_integer(_required(data, "version", path), "version", path),
        id=_string(_required(data, "id", path), "id", path),
        character_id=_string(
            _required(character, "id", path), "character.id", path
        ),
        state_id=_string(_required(state, "id", path), "state.id", path),
        canvas_width=_integer(
            _required(canvas, "width", path), "canvas.width", path
        ),
        canvas_height=_integer(
            _required(canvas, "height", path), "canvas.height", path
        ),
        background=_string(
            _required(canvas, "background", path), "canvas.background", path
        ),
        anchor_x=_number(_required(anchor, "x", path), "anchor.x", path),
        anchor_y=_number(_required(anchor, "y", path), "anchor.y", path),
        fps=_number(_required(playback, "fps", path), "playback.fps", path),
        loop=loop,
        frames=tuple(frames),
        spec_path=path,
        animation_dir=path.parent,
    )


def numeric_sort_key(value: str | Path) -> tuple[tuple[int, int | str], ...]:
    """Natural, deterministic key: frame_2 precedes frame_10."""

    chunks = re.split(r"(\d+)", str(value).casefold())
    return tuple(
        (0, int(chunk)) if chunk.isdigit() else (1, chunk)
        for chunk in chunks
        if chunk
    )


def is_finite_number(value: float) -> bool:
    return math.isfinite(value)
