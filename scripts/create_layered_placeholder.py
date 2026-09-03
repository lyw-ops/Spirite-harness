"""Write a three-layer geometric demo beside a copied Animation Plan.

Usage: python scripts/create_layered_placeholder.py /tmp/sprite-m3/demo
No existing files are replaced; choose a new directory for a new demo.
"""
from pathlib import Path
import shutil
import sys

from PIL import Image, ImageDraw


def main(output: Path) -> None:
    output = output.expanduser().resolve()
    if output.exists():
        raise SystemExit(f'Refusing to replace existing demo directory: {output}')
    output.mkdir(parents=True)
    assets = output / 'assets'
    assets.mkdir()
    shapes = [
        ('body', (28, 32), (40, 160, 170, 255)),
        ('head', (22, 20), (245, 175, 50, 255)),
        ('hand', (12, 12), (220, 85, 95, 200)),
    ]
    for name, size, color in shapes:
        image = Image.new('RGBA', size)
        draw = ImageDraw.Draw(image)
        if name == 'head':
            draw.polygon([(size[0] // 2, 1), (size[0] - 2, size[1] - 2), (1, size[1] - 2)], fill=color)
        elif name == 'hand':
            draw.ellipse((1, 1, size[0] - 2, size[1] - 2), fill=color)
        else:
            draw.rectangle((1, 1, size[0] - 2, size[1] - 2), fill=color)
        image.save(assets / f'{name}.png')
    template = Path(__file__).resolve().parents[1] / 'examples/layered-placeholder/animation.json'
    shutil.copyfile(template, output / 'animation.json')
    print(f'Wrote geometric placeholder layers and animation.json to {output}')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('Usage: create_layered_placeholder.py OUTPUT_DIRECTORY')
    main(Path(sys.argv[1]))
