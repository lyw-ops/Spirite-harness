from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

from PIL import Image
import pytest
import yaml


@pytest.fixture
def animation_factory(tmp_path: Path) -> Callable[..., Path]:
    counter = 0

    def create(
        *,
        version: int = 1,
        fps: float = 6,
        anchor: tuple[float, float] = (0.5, 0.94),
        canvas: tuple[int, int] = (16, 16),
        frames: list[dict[str, Any]] | None = None,
        create_images: bool = True,
        image_size: tuple[int, int] | None = None,
        image_mode: str = "RGBA",
    ) -> Path:
        nonlocal counter
        animation_dir = tmp_path / f"animation-{counter}"
        counter += 1
        animation_dir.mkdir()
        frames_dir = animation_dir / "frames"
        frames_dir.mkdir()
        if frames is None:
            frames = [
                {"file": "frames/frame_000.png", "duration": 1, "action": "hold"},
                {"file": "frames/frame_001.png", "duration": 2, "action": "move"},
            ]
        data = {
            "version": version,
            "id": "test_animation",
            "character": {"id": "tester"},
            "state": {"id": "testing"},
            "canvas": {
                "width": canvas[0],
                "height": canvas[1],
                "background": "transparent",
            },
            "anchor": {"x": anchor[0], "y": anchor[1]},
            "playback": {"fps": fps, "loop": True},
            "frames": frames,
        }
        (animation_dir / "animation.yaml").write_text(
            yaml.safe_dump(data, sort_keys=False), encoding="utf-8"
        )
        if create_images:
            for index, frame in enumerate(frames):
                path = animation_dir / frame["file"]
                path.parent.mkdir(parents=True, exist_ok=True)
                if not path.exists():
                    mode = image_mode
                    color = (
                        (255, index * 40 % 256, 0, 80 + index * 80 % 176)
                        if mode == "RGBA"
                        else (255, index * 40 % 256, 0)
                    )
                    Image.new(mode, image_size or canvas, color).save(path)
        return animation_dir

    return create
