"""Deterministic, labeled development contact sheets."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont

from .processing import ensure_safe_artifact_output
from .spec import AnimationSpec


def create_contact_sheet(
    spec: AnimationSpec,
    output: Path | None = None,
    *,
    thumb_size: int = 192,
) -> dict[str, Any]:
    output_path = (
        output.resolve()
        if output is not None
        else (spec.animation_dir / "generated" / "contact-sheet.png").resolve()
    )
    ensure_safe_artifact_output(spec, output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    columns = max(1, math.ceil(math.sqrt(len(spec.frames))))
    rows = math.ceil(len(spec.frames) / columns)
    margin = 12
    label_height = 38
    cell_width = thumb_size + margin * 2
    cell_height = thumb_size + label_height + margin * 2
    sheet = Image.new(
        "RGBA", (columns * cell_width, rows * cell_height), (30, 32, 38, 255)
    )
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()

    for index, frame in enumerate(spec.frames):
        column = index % columns
        row = index // columns
        origin_x = column * cell_width
        origin_y = row * cell_height
        image_box = (origin_x + margin, origin_y + margin)
        with Image.open(spec.frame_path(frame)) as source:
            thumbnail = source.convert("RGBA")
            thumbnail.thumbnail((thumb_size, thumb_size), Image.Resampling.LANCZOS)
        image_x = image_box[0] + (thumb_size - thumbnail.width) // 2
        image_y = image_box[1] + (thumb_size - thumbnail.height) // 2
        sheet.alpha_composite(thumbnail, (image_x, image_y))
        thumbnail.close()

        label = f"{index}: {Path(frame.file).name}"
        action = frame.action or ""
        draw.text(
            (origin_x + margin, origin_y + margin + thumb_size + 4),
            label,
            fill=(245, 245, 248, 255),
            font=font,
        )
        draw.text(
            (origin_x + margin, origin_y + margin + thumb_size + 19),
            action[:30],
            fill=(170, 190, 220, 255),
            font=font,
        )

    sheet.save(output_path, format="PNG")
    sheet.close()
    return {
        "success": True,
        "animation_id": spec.id,
        "output": str(output_path),
        "format": "PNG",
        "frame_count": len(spec.frames),
        "columns": columns,
        "rows": rows,
        "thumb_size": thumb_size,
    }
