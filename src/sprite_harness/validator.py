"""Semantic and frame-level validation with stable machine error codes."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from PIL import Image, UnidentifiedImageError

from .spec import AnimationSpec, is_finite_number


SUPPORTED_SPEC_VERSIONS = {1}


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    message: str
    context: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {"code": self.code, "message": self.message, **self.context}


@dataclass(frozen=True)
class ValidationResult:
    errors: tuple[ValidationIssue, ...]
    warnings: tuple[ValidationIssue, ...] = ()

    @property
    def valid(self) -> bool:
        return not self.errors

    def as_dict(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "errors": [error.as_dict() for error in self.errors],
            "warnings": [warning.as_dict() for warning in self.warnings],
        }


def _issue(code: str, message: str, **context: Any) -> ValidationIssue:
    return ValidationIssue(code=code, message=message, context=context)


def _path_is_within(path: Path, directory: Path) -> bool:
    try:
        path.relative_to(directory)
        return True
    except ValueError:
        return False


def validate_animation(spec: AnimationSpec) -> ValidationResult:
    errors: list[ValidationIssue] = []

    if spec.version not in SUPPORTED_SPEC_VERSIONS:
        errors.append(
            _issue(
                "UNSUPPORTED_SPEC_VERSION",
                "Specification version is not supported.",
                version=spec.version,
                supported=sorted(SUPPORTED_SPEC_VERSIONS),
            )
        )
    if spec.canvas_width <= 0 or spec.canvas_height <= 0:
        errors.append(
            _issue(
                "INVALID_CANVAS_SIZE",
                "Canvas width and height must be positive integers.",
                actual=[spec.canvas_width, spec.canvas_height],
            )
        )
    if not is_finite_number(spec.fps) or spec.fps <= 0:
        errors.append(
            _issue(
                "INVALID_FPS", "Playback FPS must be a finite number above zero.", actual=spec.fps
            )
        )
    if (
        not is_finite_number(spec.anchor_x)
        or not is_finite_number(spec.anchor_y)
        or not 0 <= spec.anchor_x <= 1
        or not 0 <= spec.anchor_y <= 1
    ):
        errors.append(
            _issue(
                "INVALID_ANCHOR",
                "Anchor coordinates must be finite values from 0 through 1.",
                actual=[spec.anchor_x, spec.anchor_y],
            )
        )
    if not spec.frames:
        errors.append(_issue("ZERO_FRAMES", "Animation must contain at least one frame."))

    seen: dict[str, int] = {}
    expected_ratio = (
        spec.canvas_width / spec.canvas_height
        if spec.canvas_width > 0 and spec.canvas_height > 0
        else None
    )
    for index, frame in enumerate(spec.frames):
        normalized_file = str(spec.frame_path(frame))
        if normalized_file in seen:
            errors.append(
                _issue(
                    "DUPLICATE_FRAME",
                    "Frame file appears more than once in the specification.",
                    frame=frame.file,
                    first_index=seen[normalized_file],
                    duplicate_index=index,
                )
            )
        else:
            seen[normalized_file] = index

        if not is_finite_number(frame.duration) or frame.duration <= 0:
            errors.append(
                _issue(
                    "INVALID_DURATION",
                    "Frame duration must be a finite number above zero.",
                    frame=frame.file,
                    index=index,
                    actual=frame.duration,
                )
            )

        frame_path = spec.frame_path(frame)
        if not _path_is_within(frame_path, spec.animation_dir.resolve()):
            errors.append(
                _issue(
                    "FRAME_OUTSIDE_ANIMATION",
                    "Frame path must stay inside the animation directory.",
                    frame=frame.file,
                    index=index,
                )
            )
            continue
        if not frame_path.is_file():
            errors.append(
                _issue(
                    "FRAME_MISSING",
                    "Frame file does not exist.",
                    frame=frame.file,
                    index=index,
                    path=str(frame_path),
                )
            )
            continue

        try:
            with Image.open(frame_path) as image:
                image.load()
                actual_size = image.size
                has_alpha = image.mode in {"RGBA", "LA"} or (
                    image.mode == "P" and "transparency" in image.info
                )
        except (UnidentifiedImageError, OSError, ValueError) as exc:
            errors.append(
                _issue(
                    "FRAME_INVALID_IMAGE",
                    "Frame file is not a readable image.",
                    frame=frame.file,
                    index=index,
                    path=str(frame_path),
                    detail=str(exc),
                )
            )
            continue

        if actual_size != spec.canvas_size:
            errors.append(
                _issue(
                    "FRAME_DIMENSION_MISMATCH",
                    "Frame dimensions do not match the declared canvas.",
                    frame=frame.file,
                    index=index,
                    expected=list(spec.canvas_size),
                    actual=list(actual_size),
                )
            )
        if expected_ratio is not None and actual_size[1] > 0:
            actual_ratio = actual_size[0] / actual_size[1]
            if abs(actual_ratio - expected_ratio) > 1e-9:
                errors.append(
                    _issue(
                        "FRAME_ASPECT_RATIO_MISMATCH",
                        "Frame aspect ratio does not match the declared canvas.",
                        frame=frame.file,
                        index=index,
                        expected=expected_ratio,
                        actual=actual_ratio,
                    )
                )
        if spec.background.casefold() == "transparent" and not has_alpha:
            errors.append(
                _issue(
                    "FRAME_ALPHA_REQUIRED",
                    "A transparent canvas requires frames with an alpha channel.",
                    frame=frame.file,
                    index=index,
                )
            )

    return ValidationResult(errors=tuple(errors))
