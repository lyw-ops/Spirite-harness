"""Generate a clearly labeled placeholder source sprite for renderer demos.

The drawing is deliberately schematic and marked as placeholder artwork; no
third-party or franchise artwork is produced. Pair it with an Animation Plan:

    python scripts/create_placeholder_sprite.py demo/sprite.png
    sprite-harness plan --spec examples/reimu-eating/eating-loop.json \
        --source demo/sprite.png --output demo/build
    sprite-harness render demo/build
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw


DEFAULT_OUTPUT = (
    Path(__file__).resolve().parents[1]
    / "examples"
    / "reimu-eating"
    / "placeholder-sprite.png"
)
SIZE = (160, 190)


def main(output: Path) -> None:
    image = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Schematic shrine-maiden-ish placeholder: head, bow, robe, ground shadow.
    draw.ellipse((46, 34, 114, 102), fill=(255, 224, 200, 255), outline=(70, 45, 55, 255), width=3)
    draw.polygon(((38, 44), (80, 12), (122, 44), (106, 56), (80, 40), (54, 56)), fill=(205, 42, 58, 255))
    draw.ellipse((60, 60, 72, 72), fill=(60, 40, 50, 255))
    draw.ellipse((88, 60, 100, 72), fill=(60, 40, 50, 255))
    draw.ellipse((72, 84, 88, 92), fill=(150, 55, 65, 255))
    draw.polygon(((50, 102), (110, 102), (128, 180), (32, 180)), fill=(205, 42, 58, 255))
    draw.polygon(((72, 102), (88, 102), (98, 176), (62, 176)), fill=(245, 240, 220, 255))
    draw.rectangle((30, 180, 130, 186), fill=(90, 60, 60, 120))

    draw.rectangle((8, 2, 152, 24), fill=(25, 25, 32, 210))
    draw.text((14, 4), "PLACEHOLDER", fill="white")
    draw.text((14, 13), "NOT FINAL ARTWORK", fill=(255, 175, 185, 255))

    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output, optimize=True)
    print(f"wrote {output} ({SIZE[0]}x{SIZE[1]} RGBA)")


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_OUTPUT)
