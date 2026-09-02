"""Human- and machine-readable animation report data."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .spec import AnimationSpec
from .validator import ValidationResult


def build_report(spec: AnimationSpec, validation: ValidationResult) -> dict[str, Any]:
    generated_dir = spec.animation_dir / "generated"
    candidates = {
        "preview": generated_dir / "preview.gif",
        "contact_sheet": generated_dir / "contact-sheet.png",
        "normalized_spec": generated_dir / "animation.yaml",
        "normalized_frames": generated_dir / "normalized",
    }
    artifacts = {
        name: {"path": str(path.resolve()), "exists": path.exists()}
        for name, path in candidates.items()
    }
    return {
        "animation_id": spec.id,
        "spec_version": spec.version,
        "spec_path": str(spec.spec_path),
        "character": spec.character_id,
        "state": spec.state_id,
        "frame_count": len(spec.frames),
        "canvas": {
            "width": spec.canvas_width,
            "height": spec.canvas_height,
            "background": spec.background,
        },
        "anchor": {"x": spec.anchor_x, "y": spec.anchor_y},
        "playback": {"fps": spec.fps, "loop": spec.loop},
        "validation": validation.as_dict(),
        "artifacts": artifacts,
    }


def human_report(report: dict[str, Any]) -> str:
    canvas = report["canvas"]
    anchor = report["anchor"]
    playback = report["playback"]
    validation = report["validation"]
    lines = [
        f"Animation: {report['animation_id']}",
        f"Character: {report['character']}",
        f"State: {report['state']}",
        f"Frames: {report['frame_count']}",
        f"Canvas: {canvas['width']}x{canvas['height']} ({canvas['background']})",
        f"Anchor: ({anchor['x']}, {anchor['y']})",
        f"Playback: {playback['fps']} fps, loop={str(playback['loop']).lower()}",
        f"Validation: {'valid' if validation['valid'] else 'invalid'}",
        "Artifacts:",
    ]
    for name, artifact in report["artifacts"].items():
        state = "present" if artifact["exists"] else "not generated"
        lines.append(f"  {name}: {artifact['path']} ({state})")
    if validation["errors"]:
        lines.append("Errors:")
        for error in validation["errors"]:
            lines.append(f"  [{error['code']}] {error['message']}")
    return "\n".join(lines)

