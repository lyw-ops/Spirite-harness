"""Generate small-on-disk, visibly labeled 1024px placeholder source frames."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
FRAME_DIR = ROOT / "examples" / "reimu-eating-task2" / "frames"
ACTIONS = (
    "HOLD ONIGIRI",
    "RAISE ONIGIRI",
    "BITE",
    "PUFF CHEEKS",
    "CHEW",
    "RETURN",
)
HAND_POSITIONS = ((650, 690), (625, 590), (580, 500), (570, 525), (590, 555), (640, 650))


def main() -> None:
    FRAME_DIR.mkdir(parents=True, exist_ok=True)
    font = ImageFont.load_default(size=26)
    small_font = ImageFont.load_default(size=18)
    for index, (action, hand) in enumerate(zip(ACTIONS, HAND_POSITIONS, strict=True)):
        image = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        # A deliberately schematic shrine-maiden placeholder silhouette.
        draw.ellipse((318, 250, 706, 638), fill=(255, 224, 200, 255), outline=(70, 45, 55, 255), width=9)
        draw.polygon(((270, 300), (512, 115), (754, 300), (670, 356), (512, 274), (354, 356)), fill=(205, 42, 58, 255))
        draw.rectangle((466, 80, 558, 315), fill=(245, 240, 220, 255))
        draw.polygon(((512, 80), (384, 185), (512, 225), (640, 185)), fill=(245, 240, 220, 255))
        draw.arc((380, 330, 500, 480), 180, 350, fill=(60, 40, 50, 255), width=8)
        draw.arc((524, 330, 644, 480), 190, 360, fill=(60, 40, 50, 255), width=8)
        mouth_width = 42 if index in (2, 4) else 24
        draw.ellipse((512 - mouth_width, 500, 512 + mouth_width, 520), fill=(150, 55, 65, 255))
        if index in (3, 4):
            draw.ellipse((352, 465, 430, 525), fill=(246, 150, 155, 180))
            draw.ellipse((594, 465, 672, 525), fill=(246, 150, 155, 180))
        draw.polygon(((330, 640), (694, 640), (790, 960), (234, 960)), fill=(205, 42, 58, 255))
        draw.polygon(((470, 640), (554, 640), (610, 930), (414, 930)), fill=(245, 240, 220, 255))

        hx, hy = hand
        draw.line((610, 700, hx, hy), fill=(255, 224, 200, 255), width=42)
        draw.ellipse((hx - 32, hy - 32, hx + 32, hy + 32), fill=(255, 224, 200, 255))
        draw.polygon(((hx - 60, hy + 35), (hx + 58, hy + 35), (hx, hy - 80)), fill=(248, 248, 238, 255), outline=(45, 50, 48, 255))
        draw.rectangle((hx - 52, hy + 18, hx + 50, hy + 43), fill=(45, 65, 48, 255))

        draw.rounded_rectangle((28, 28, 996, 112), radius=18, fill=(25, 25, 32, 210))
        draw.text((52, 47), f"PLACEHOLDER {index}/5 - {action}", fill="white", font=font)
        draw.text((52, 78), "NOT FINAL ARTWORK", fill=(255, 175, 185, 255), font=small_font)
        image.save(FRAME_DIR / f"frame_{index:03d}.png", optimize=True)


if __name__ == "__main__":
    main()
