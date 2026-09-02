"""Non-destructive frame normalization into a derived-artwork directory."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Any

from PIL import Image
import yaml

from .processing import ProcessingError
from .spec import AnimationSpec, FrameSpec
from .validator import ValidationResult, validate_animation


NORMALIZABLE_CODES = {
    "FRAME_DIMENSION_MISMATCH",
    "FRAME_ASPECT_RATIO_MISMATCH",
    "FRAME_ALPHA_REQUIRED",
}


class NormalizationError(ProcessingError):
    pass


def blocking_validation(result: ValidationResult) -> ValidationResult:
    return ValidationResult(
        errors=tuple(error for error in result.errors if error.code not in NORMALIZABLE_CODES)
    )


def _assert_safe_output(spec: AnimationSpec, output_dir: Path) -> None:
    resolved_output = output_dir.resolve()
    source_paths = [spec.frame_path(frame) for frame in spec.frames]
    if resolved_output == spec.animation_dir.resolve():
        raise NormalizationError(
            "UNSAFE_OUTPUT_PATH",
            "Normalization output cannot be the animation source directory.",
            output=str(resolved_output),
        )
    for source_path in source_paths:
        source_directory = source_path.parent
        if (
            source_path == resolved_output
            or resolved_output in source_path.parents
            or source_directory == resolved_output
            or source_directory in resolved_output.parents
        ):
            raise NormalizationError(
                "OUTPUT_OVERLAPS_SOURCE",
                "Normalization output cannot contain or sit inside source artwork.",
                output=str(resolved_output),
                source=str(source_path),
            )


def _normalized_image(
    source: Image.Image,
    canvas_size: tuple[int, int],
    anchor: tuple[float, float],
    scale_mode: str,
) -> tuple[Image.Image, float, tuple[int, int]]:
    image = source.convert("RGBA")
    original_size = image.size
    canvas_width, canvas_height = canvas_size

    if scale_mode == "fit":
        factor = min(canvas_width / image.width, canvas_height / image.height)
        new_size = (
            max(1, round(image.width * factor)),
            max(1, round(image.height * factor)),
        )
        if new_size != image.size:
            image = image.resize(new_size, Image.Resampling.LANCZOS)
    elif image.width > canvas_width or image.height > canvas_height:
        raise NormalizationError(
            "FRAME_TOO_LARGE",
            "Frame exceeds the canvas; rerun with '--scale fit' to scale uniformly.",
            actual=list(image.size),
            canvas=list(canvas_size),
        )

    x = round(anchor[0] * (canvas_width - image.width))
    y = round(anchor[1] * (canvas_height - image.height))
    canvas = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    canvas.alpha_composite(image, (x, y))
    factor = image.width / original_size[0]
    return canvas, factor, (x, y)


def normalize_animation(
    spec: AnimationSpec,
    *,
    output_dir: Path | None = None,
    scale_mode: str = "none",
) -> dict[str, Any]:
    if scale_mode not in {"none", "fit"}:
        raise NormalizationError(
            "INVALID_SCALE_MODE", "Scale mode must be 'none' or 'fit'.", actual=scale_mode
        )

    validation = validate_animation(spec)
    blocking = blocking_validation(validation)
    if not blocking.valid:
        raise NormalizationError(
            "NORMALIZATION_INPUT_INVALID",
            "Animation has validation errors that normalization cannot repair.",
            errors=[error.as_dict() for error in blocking.errors],
        )

    destination = (
        output_dir.resolve()
        if output_dir is not None
        else (spec.animation_dir / "generated" / "normalized").resolve()
    )
    _assert_safe_output(spec, destination)
    destination.mkdir(parents=True, exist_ok=True)

    frame_results: list[dict[str, Any]] = []
    derived_frames: list[FrameSpec] = []
    for index, frame in enumerate(spec.frames):
        source_path = spec.frame_path(frame)
        output_path = destination / f"frame_{index:03d}.png"
        with Image.open(source_path) as source:
            original_size = source.size
            normalized, scale_factor, position = _normalized_image(
                source,
                spec.canvas_size,
                (spec.anchor_x, spec.anchor_y),
                scale_mode,
            )
            normalized.save(output_path, format="PNG")

        frame_results.append(
            {
                "index": index,
                "source": str(source_path),
                "output": str(output_path),
                "original_size": list(original_size),
                "size": list(spec.canvas_size),
                "scale": scale_factor,
                "position": list(position),
            }
        )
        derived_frames.append(replace(frame, file=output_path.name))

    generated_root = destination.parent
    generated_spec_path = generated_root / "animation.yaml"
    generated_data = {
        "version": spec.version,
        "id": f"{spec.id}.normalized",
        "character": {"id": spec.character_id},
        "state": {"id": spec.state_id},
        "canvas": {
            "width": spec.canvas_width,
            "height": spec.canvas_height,
            "background": spec.background,
        },
        "anchor": {"x": spec.anchor_x, "y": spec.anchor_y},
        "playback": {"fps": spec.fps, "loop": spec.loop},
        "frames": [
            {
                "file": (destination / frame.file).relative_to(generated_root).as_posix(),
                "duration": frame.duration,
                **({"action": frame.action} if frame.action is not None else {}),
            }
            for frame in derived_frames
        ],
    }
    generated_spec_path.write_text(
        yaml.safe_dump(generated_data, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )

    return {
        "success": True,
        "animation_id": spec.id,
        "output_dir": str(destination),
        "spec": str(generated_spec_path),
        "scale_mode": scale_mode,
        "frames": frame_results,
    }
