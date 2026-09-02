from PIL import Image

from sprite_harness.spec import load_spec
from sprite_harness.validator import validate_animation


def error_codes(path):
    return {error.code for error in validate_animation(load_spec(path)).errors}


def test_missing_frame(animation_factory):
    path = animation_factory(create_images=False)
    assert "FRAME_MISSING" in error_codes(path)


def test_duplicate_frame_detection(animation_factory):
    frames = [
        {"file": "frames/frame_000.png", "duration": 1},
        {"file": "frames/frame_000.png", "duration": 1},
    ]
    assert "DUPLICATE_FRAME" in error_codes(animation_factory(frames=frames))


def test_duplicate_frame_alias_detection(animation_factory):
    frames = [
        {"file": "frames/frame_000.png", "duration": 1},
        {"file": "frames/../frames/frame_000.png", "duration": 1},
    ]
    assert "DUPLICATE_FRAME" in error_codes(animation_factory(frames=frames))


def test_wrong_image_dimensions(animation_factory):
    path = animation_factory(canvas=(16, 16), image_size=(16, 12))
    codes = error_codes(path)
    assert "FRAME_DIMENSION_MISMATCH" in codes
    assert "FRAME_ASPECT_RATIO_MISMATCH" in codes


def test_invalid_fps(animation_factory):
    assert "INVALID_FPS" in error_codes(animation_factory(fps=0))


def test_invalid_duration(animation_factory):
    frames = [{"file": "frames/frame_000.png", "duration": 0}]
    assert "INVALID_DURATION" in error_codes(animation_factory(frames=frames))


def test_invalid_anchor(animation_factory):
    assert "INVALID_ANCHOR" in error_codes(animation_factory(anchor=(1.1, -0.1)))


def test_empty_animation(animation_factory):
    assert "ZERO_FRAMES" in error_codes(animation_factory(frames=[]))


def test_alpha_is_required_for_transparent_canvas(animation_factory):
    assert "FRAME_ALPHA_REQUIRED" in error_codes(animation_factory(image_mode="RGB"))


def test_invalid_image_file(animation_factory):
    path = animation_factory(create_images=False)
    frame_path = path / "frames" / "frame_000.png"
    frame_path.write_text("not a png", encoding="utf-8")
    assert "FRAME_INVALID_IMAGE" in error_codes(path)


def test_frame_path_cannot_escape_animation(animation_factory, tmp_path):
    outside = tmp_path / "outside.png"
    Image.new("RGBA", (16, 16), (0, 0, 0, 0)).save(outside)
    frames = [{"file": "../outside.png", "duration": 1}]
    assert "FRAME_OUTSIDE_ANIMATION" in error_codes(
        animation_factory(frames=frames, create_images=False)
    )
