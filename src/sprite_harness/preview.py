"""Animated GIF preview generation without ffmpeg."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from PIL import Image

from .processing import ensure_safe_artifact_output
from .spec import AnimationSpec


def create_preview(spec: AnimationSpec, output: Path | None = None) -> dict[str, Any]:
    output_path = (
        output.resolve()
        if output is not None
        else (spec.animation_dir / "generated" / "preview.gif").resolve()
    )
    ensure_safe_artifact_output(spec, output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    images: list[Image.Image] = []
    durations: list[int] = []
    try:
        for frame in spec.frames:
            with Image.open(spec.frame_path(frame)) as source:
                images.append(source.convert("RGBA"))
            durations.append(max(10, round((frame.duration / spec.fps) * 1000)))

        save_options: dict[str, Any] = {
            "save_all": True,
            "append_images": images[1:],
            "duration": durations,
            "disposal": 2,
            "optimize": False,
        }
        if spec.loop:
            save_options["loop"] = 0
        images[0].save(output_path, format="GIF", **save_options)
    finally:
        for image in images:
            image.close()

    return {
        "success": True,
        "animation_id": spec.id,
        "output": str(output_path),
        "format": "GIF",
        "frame_count": len(spec.frames),
        "durations_ms": durations,
        "loop": spec.loop,
    }
