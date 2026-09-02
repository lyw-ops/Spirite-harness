"""Milestone-2 renderer tests: exact geometry, safety, determinism, contracts.

Expected pixel positions in the reference tests are computed by hand from the
documented semantics (docs/renderer.md), not by running the renderer, so a bug
shared by the renderer and the validator still fails here.
"""

from __future__ import annotations

import hashlib
import json
import tomllib
from pathlib import Path

import pytest
from PIL import Image

from sprite_harness import __version__
from sprite_harness.build import load_build
from sprite_harness.cli import main
from sprite_harness.exit_codes import (
    MALFORMED_SPECIFICATION,
    MISSING_INPUT,
    PROCESSING_FAILURE,
    SUCCESS,
    VALIDATION_FAILURE,
)
from sprite_harness.render import render_build


REPO_ROOT = Path(__file__).resolve().parents[1]

UNIT_BY_MOTION = {
    "translate_x": "px",
    "translate_y": "px",
    "rotate": "deg",
    "scale": "ratio",
    "opacity": "ratio",
}


def parsed(capsys) -> dict:
    """Parse stdout as strict JSON (NaN/Infinity tokens are rejected)."""

    def reject(token):  # pragma: no cover - only on contract violation
        raise AssertionError(f"non-standard JSON constant: {token}")

    return json.loads(capsys.readouterr().out, parse_constant=reject)


def track(motion: str, amplitude: float, **overrides) -> dict:
    data = {
        "track_id": overrides.pop("track_id", f"{motion}_track"),
        "target": "sprite",
        "motion": motion,
        "amplitude": amplitude,
        "unit": UNIT_BY_MOTION[motion],
        "curve": "sine",
        "cycles": 1,
        "phase": 0.0,
    }
    data.update(overrides)
    return data


def block_sprite(path: Path, size=(8, 8), box=(3, 3, 4, 4), color=(200, 40, 40, 255)):
    """Transparent sprite with an opaque rectangle (inclusive box)."""

    image = Image.new("RGBA", size, (0, 0, 0, 0))
    for x in range(box[0], box[2] + 1):
        for y in range(box[1], box[3] + 1):
            image.putpixel((x, y), color)
    image.save(path)
    return path


def make_build(
    tmp_path: Path,
    capsys,
    *,
    source: Path | None,
    name: str = "build",
    frame_count: int = 4,
    canvas: tuple[int, int] | None = (16, 16),
    background: str = "transparent",
    anchor: dict | None = None,
    tracks: list[dict] | None = None,
    reduced_motion: str | None = None,
    loop: bool = True,
) -> Path:
    spec: dict = {
        "plan_version": 1,
        "animation_id": "render_test",
        "playback": {"fps": 8, "frame_count": frame_count, "loop": loop},
        "anchor": anchor or {"type": "bottom_center"},
        "tracks": tracks or [],
    }
    if canvas is not None:
        spec["canvas"] = {"width": canvas[0], "height": canvas[1], "background": background}
    if reduced_motion is not None:
        spec["reduced_motion"] = {"mode": reduced_motion}
    spec_dir = tmp_path / f"{name}-spec"
    spec_dir.mkdir(exist_ok=True)
    spec_path = spec_dir / "animation.json"
    spec_path.write_text(json.dumps(spec), encoding="utf-8")
    build = tmp_path / name
    argv = ["plan", "--spec", str(spec_path), "--output", str(build), "--json"]
    if source is not None:
        argv += ["--source", str(source)]
    assert main(argv) == SUCCESS
    capsys.readouterr()
    return build


def render(build: Path, *args: str) -> int:
    return main(["render", str(build), "--json", *args])


def alpha_bbox(path: Path) -> tuple[int, int, int, int] | None:
    with Image.open(path) as image:
        return image.convert("RGBA").getchannel("A").getbbox()


def nonzero_pixels(path: Path) -> dict[tuple[int, int], tuple[int, int, int, int]]:
    with Image.open(path) as image:
        rgba = image.convert("RGBA")
        return {
            (x, y): rgba.getpixel((x, y))
            for x in range(rgba.width)
            for y in range(rgba.height)
            if rgba.getpixel((x, y))[3] != 0
        }


def frame_hashes(build: Path) -> list[str]:
    return [
        hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted((build / "frames").glob("*.png"))
    ]


# ---------------------------------------------------------------------------
# Static and translation geometry


def test_static_render_is_exact_source_copy(tmp_path, capsys):
    source = tmp_path / "sprite.png"
    image = Image.new("RGBA", (8, 8), (0, 0, 0, 0))
    image.putpixel((1, 2), (10, 20, 30, 255))
    image.putpixel((5, 5), (250, 240, 230, 77))
    image.putpixel((7, 0), (1, 2, 3, 4))
    image.save(source)
    build = make_build(tmp_path, capsys, source=source, canvas=(8, 8), frame_count=2)
    assert render(build) == SUCCESS
    payload = parsed(capsys)
    assert payload["success"] is True
    assert payload["mode"] == "full"
    assert payload["frame_count"] == 2
    with Image.open(source) as src:
        expected = src.convert("RGBA").tobytes()
    for frame in sorted((build / "frames").glob("*.png")):
        with Image.open(frame) as rendered:
            assert rendered.mode == "RGBA"
            assert rendered.tobytes() == expected
    assert main(["validate", str(build), "--json"]) == SUCCESS


def test_translation_directions_and_single_application(tmp_path, capsys):
    # Source block bbox (3,3)-(5,5); bottom_center on a 16x16 canvas pastes the
    # 8x8 source at (4, 8), so the base block bbox is (7, 11, 9, 13).
    source = block_sprite(tmp_path / "sprite.png")
    tracks = [
        track("translate_x", 4, curve="triangle", track_id="tx"),
        track("translate_y", 2, curve="triangle", track_id="ty"),
    ]
    build = make_build(tmp_path, capsys, source=source, tracks=tracks)
    assert render(build) == SUCCESS
    capsys.readouterr()
    # triangle offsets over 4 looping frames: x [0, 4, 0, -4], y [0, 2, 0, -2].
    # A double-applied translation would land at +8/+4 instead.
    expected = [
        (7, 11, 9, 13),
        (11, 13, 13, 15),
        (7, 11, 9, 13),
        (3, 9, 5, 11),
    ]
    for index, bbox in enumerate(expected):
        assert alpha_bbox(build / "frames" / f"frame_{index:03d}.png") == bbox
    assert main(["validate", str(build), "--json"]) == SUCCESS


@pytest.mark.parametrize(
    ("anchor", "expected_bbox"),
    [
        ({"type": "bottom_center"}, (4, 16, 12, 24)),
        ({"type": "center"}, (4, 8, 12, 16)),
        ({"type": "custom", "x": 0, "y": 0}, (0, 0, 8, 8)),
        ({"type": "custom", "x": 0.25, "y": 0.5}, (2, 8, 10, 16)),
    ],
)
def test_anchor_placement_with_source_smaller_than_canvas(
    tmp_path, capsys, anchor, expected_bbox
):
    source = tmp_path / "sprite.png"
    Image.new("RGBA", (8, 8), (90, 90, 200, 255)).save(source)
    build = make_build(
        tmp_path, capsys, source=source, canvas=(16, 24), frame_count=2, anchor=anchor
    )
    assert render(build) == SUCCESS
    capsys.readouterr()
    assert alpha_bbox(build / "frames" / "frame_000.png") == expected_bbox
    assert main(["validate", str(build), "--json"]) == SUCCESS


def test_clipped_translation_validates_against_the_model(tmp_path, capsys):
    # A fully opaque source moving past the fixed canvas edge is clipped, not
    # grown; the model-based check accepts the clipping.
    source = tmp_path / "sprite.png"
    Image.new("RGBA", (8, 8), (10, 200, 10, 255)).save(source)
    build = make_build(
        tmp_path,
        capsys,
        source=source,
        canvas=(8, 8),
        tracks=[track("translate_x", 4, curve="triangle")],
    )
    assert render(build) == SUCCESS
    capsys.readouterr()
    assert alpha_bbox(build / "frames" / "frame_001.png") == (4, 0, 8, 8)
    assert alpha_bbox(build / "frames" / "frame_003.png") == (0, 0, 4, 8)
    assert main(["validate", str(build), "--json"]) == SUCCESS
    payload = parsed(capsys)
    assert payload["valid"] is True
    assert any(w["code"] == "CONTENT_TOUCHES_EDGE" for w in payload["warnings"])


# ---------------------------------------------------------------------------
# Rotation, scale, opacity — hand-computed reference expectations


def rotation_build(tmp_path, capsys, amplitudes: list[float]):
    """8x8 canvas, center anchor, single opaque pixel at (2, 3)."""

    source = tmp_path / "sprite.png"
    image = Image.new("RGBA", (8, 8), (0, 0, 0, 0))
    image.putpixel((2, 3), (200, 100, 50, 255))
    image.save(source)
    tracks = [
        track("rotate", amplitude, phase=0.25, track_id=f"rot{i}")
        for i, amplitude in enumerate(amplitudes)
    ]
    return make_build(
        tmp_path,
        capsys,
        source=source,
        canvas=(8, 8),
        anchor={"type": "center"},
        tracks=tracks,
    )


def test_rotation_90_degrees_lands_on_hand_computed_pixels(tmp_path, capsys):
    # sine with phase 0.25 samples to [+1, 0, -1, 0] over 4 looping frames.
    # Pixel (2,3) has center (2.5, 3.5). About the anchor (4,4):
    #   +90 (cw):  (4 - (3.5-4), 4 + (2.5-4)) = (4.5, 2.5) -> pixel (4, 2)
    #   -90 (ccw): (4 + (3.5-4), 4 - (2.5-4)) = (3.5, 5.5) -> pixel (3, 5)
    build = rotation_build(tmp_path, capsys, [90])
    assert render(build) == SUCCESS
    capsys.readouterr()
    frame0 = nonzero_pixels(build / "frames" / "frame_000.png")
    assert set(frame0) == {(4, 2)}
    assert frame0[(4, 2)][3] >= 253
    # Frame 1 rotates by 0 and is an exact copy.
    frame1 = nonzero_pixels(build / "frames" / "frame_001.png")
    assert frame1 == {(2, 3): (200, 100, 50, 255)}
    frame2 = nonzero_pixels(build / "frames" / "frame_002.png")
    assert set(frame2) == {(3, 5)}
    assert main(["validate", str(build), "--json"]) == SUCCESS


def test_multiple_rotate_tracks_sum(tmp_path, capsys):
    build = rotation_build(tmp_path, capsys, [60, 30])
    assert render(build) == SUCCESS
    capsys.readouterr()
    assert set(nonzero_pixels(build / "frames" / "frame_000.png")) == {(4, 2)}


def scale_build(tmp_path, capsys, amplitudes: list[float]):
    # Mirrored linear easing with phase 0.5 samples to [1, 0.5, 0, 0.5] over 4
    # looping frames: peak factor at frame 0, never below 1, factor 1 at frame 2.
    source = block_sprite(tmp_path / "sprite.png")  # opaque block (3,3)-(4,4)
    tracks = [
        track("scale", amplitude, curve="linear", phase=0.5, track_id=f"scale{i}")
        for i, amplitude in enumerate(amplitudes)
    ]
    return make_build(
        tmp_path,
        capsys,
        source=source,
        canvas=(8, 8),
        anchor={"type": "center"},
        tracks=tracks,
    )


def test_uniform_scale_2x_about_center(tmp_path, capsys):
    # Factor 2 about (4,4): the block region [3,5)x[3,5) maps to [2,6)x[2,6);
    # bilinear support widens the alpha bbox by one pixel on each side.
    build = scale_build(tmp_path, capsys, [1.0])
    assert render(build) == SUCCESS
    capsys.readouterr()
    frame0 = build / "frames" / "frame_000.png"
    assert alpha_bbox(frame0) == (1, 1, 7, 7)
    with Image.open(frame0) as image:
        rgba = image.convert("RGBA")
        for pixel in ((3, 3), (3, 4), (4, 3), (4, 4)):
            assert rgba.getpixel(pixel)[3] == 255
    # Frame 2 scales by 1 and is an exact copy.
    assert alpha_bbox(build / "frames" / "frame_002.png") == (3, 3, 5, 5)
    assert main(["validate", str(build), "--json"]) == SUCCESS


def test_multiple_scale_tracks_multiply(tmp_path, capsys):
    # (1 + 0.25) * (1 + 0.6) = 2.0 -> identical to the single 2x track.
    build = scale_build(tmp_path, capsys, [0.25, 0.6])
    assert render(build) == SUCCESS
    capsys.readouterr()
    assert alpha_bbox(build / "frames" / "frame_000.png") == (1, 1, 7, 7)


def opacity_source(tmp_path) -> Path:
    source = tmp_path / "sprite.png"
    image = Image.new("RGBA", (8, 8), (0, 0, 0, 0))
    image.putpixel((1, 1), (10, 10, 10, 255))
    image.putpixel((2, 2), (10, 10, 10, 128))
    image.putpixel((3, 3), (10, 10, 10, 3))
    image.save(source)
    return source


def test_opacity_lookup_table_is_exact(tmp_path, capsys):
    build = make_build(
        tmp_path,
        capsys,
        source=opacity_source(tmp_path),
        canvas=(8, 8),
        tracks=[track("opacity", -0.5, phase=0.25)],
    )
    assert render(build) == SUCCESS
    capsys.readouterr()
    # Frame 0 opacity 0.5: alpha_out = floor(alpha * 0.5 + 0.5).
    pixels = nonzero_pixels(build / "frames" / "frame_000.png")
    assert pixels[(1, 1)][3] == 128
    assert pixels[(2, 2)][3] == 64
    assert pixels[(3, 3)][3] == 2
    # Frame 1 opacity 1: unchanged.
    pixels = nonzero_pixels(build / "frames" / "frame_001.png")
    assert pixels[(1, 1)][3] == 255
    assert main(["validate", str(build), "--json"]) == SUCCESS


def test_opacity_above_one_clamps_silently(tmp_path, capsys):
    build = make_build(
        tmp_path,
        capsys,
        source=opacity_source(tmp_path),
        canvas=(8, 8),
        tracks=[track("opacity", 0.5, phase=0.25)],
    )
    assert render(build) == SUCCESS
    payload = parsed(capsys)
    assert payload["success"] is True
    assert all(w["code"] != "OPACITY_CLAMPED" for w in payload["warnings"])
    pixels = nonzero_pixels(build / "frames" / "frame_000.png")
    assert pixels[(1, 1)][3] == 255
    assert pixels[(2, 2)][3] == 128


# ---------------------------------------------------------------------------
# Invalid effective values (plan stage)


@pytest.mark.parametrize(
    ("bad_track", "code"),
    [
        (track("scale", -1.0, phase=0.25), "INVALID_EFFECTIVE_SCALE"),
        (track("opacity", -1.5, phase=0.25), "INVALID_EFFECTIVE_OPACITY"),
        (track("opacity", -1.0, phase=0.25), "FULLY_TRANSPARENT_FRAME"),
    ],
)
def test_invalid_effective_values_fail_at_plan_time(tmp_path, capsys, bad_track, code):
    spec_dir = tmp_path / "spec"
    spec_dir.mkdir()
    spec_path = spec_dir / "animation.json"
    spec_path.write_text(
        json.dumps(
            {
                "plan_version": 1,
                "animation_id": "bad_values",
                "canvas": {"width": 8, "height": 8, "background": "transparent"},
                "playback": {"fps": 8, "frame_count": 4, "loop": True},
                "tracks": [bad_track],
            }
        ),
        encoding="utf-8",
    )
    assert (
        main(["plan", "--spec", str(spec_path), "--output", str(tmp_path / "b"), "--json"])
        == VALIDATION_FAILURE
    )
    payload = parsed(capsys)
    assert code in {error["code"] for error in payload["errors"]}
    assert not (tmp_path / "b").exists()


def test_target_local_tracks_are_not_value_checked(tmp_path, capsys):
    source = block_sprite(tmp_path / "sprite.png")
    build = make_build(
        tmp_path,
        capsys,
        source=source,
        tracks=[track("scale", -2.0, phase=0.25, target="head", track_id="local")],
    )
    assert render(build) == SUCCESS
    payload = parsed(capsys)
    assert payload["success"] is True
    assert payload["skipped_tracks"] == [
        {"track_id": "local", "target": "head", "motion": "scale"}
    ]


# ---------------------------------------------------------------------------
# Target-local tracks are skipped with a stable warning and no pixel effect


def test_target_local_tracks_warn_and_do_not_move_pixels(tmp_path, capsys):
    source = block_sprite(tmp_path / "sprite.png")
    with_local = make_build(
        tmp_path,
        capsys,
        source=source,
        name="with-local",
        tracks=[
            track("translate_x", 2, track_id="sway"),
            track("translate_y", 3, target="head", track_id="bob"),
            track("rotate", 15, target="hand_right", track_id="wave"),
        ],
    )
    without_local = make_build(
        tmp_path,
        capsys,
        source=source,
        name="without-local",
        tracks=[track("translate_x", 2, track_id="sway")],
    )
    assert render(with_local) == SUCCESS
    payload = parsed(capsys)
    warning = next(
        w for w in payload["warnings"] if w["code"] == "TARGET_TRACKS_SKIPPED"
    )
    assert {t["track_id"] for t in warning["tracks"]} == {"bob", "wave"}
    assert render(without_local) == SUCCESS
    capsys.readouterr()
    for index in range(4):
        name = f"frame_{index:03d}.png"
        with Image.open(with_local / "frames" / name) as a:
            with Image.open(without_local / "frames" / name) as b:
                assert a.convert("RGBA").tobytes() == b.convert("RGBA").tobytes()


# ---------------------------------------------------------------------------
# Reduced motion


def test_hold_first_frame_render_and_validation(tmp_path, capsys):
    source = block_sprite(tmp_path / "sprite.png")
    tracks = [track("translate_x", 4, curve="triangle"), track("rotate", 20, phase=0.25)]
    build = make_build(
        tmp_path, capsys, source=source, tracks=tracks, reduced_motion="hold_first_frame"
    )
    full = make_build(
        tmp_path,
        capsys,
        source=source,
        name="full",
        tracks=tracks,
        reduced_motion="hold_first_frame",
    )
    assert render(full) == SUCCESS
    capsys.readouterr()
    assert render(build, "--reduced-motion") == SUCCESS
    payload = parsed(capsys)
    assert payload["mode"] == "hold_first_frame"
    assert payload["frame_count"] == 4
    hashes = frame_hashes(build)
    assert len(hashes) == 4
    assert len(set(hashes)) == 1
    # The held pose is frame 0 of the full render.
    assert hashes[0] == frame_hashes(full)[0]
    manifest = json.loads((build / "render.json").read_text(encoding="utf-8"))
    assert manifest["mode"] == "hold_first_frame"
    assert main(["validate", str(build), "--write-qa", "--json"]) == SUCCESS
    payload = parsed(capsys)
    assert payload["valid"] is True

    # A frame swapped in from the full-motion render breaks byte identity.
    (build / "frames" / "frame_002.png").write_bytes(
        (full / "frames" / "frame_002.png").read_bytes()
    )
    assert main(["validate", str(build), "--json"]) == VALIDATION_FAILURE
    codes = {error["code"] for error in parsed(capsys)["errors"]}
    assert "HOLD_FRAME_MISMATCH" in codes


def test_reduced_motion_flag_on_full_mode_plan_renders_full(tmp_path, capsys):
    source = block_sprite(tmp_path / "sprite.png")
    build = make_build(
        tmp_path,
        capsys,
        source=source,
        tracks=[track("translate_x", 4, curve="triangle")],
        reduced_motion="full",
    )
    assert render(build, "--reduced-motion") == SUCCESS
    payload = parsed(capsys)
    assert payload["mode"] == "full"
    manifest = json.loads((build / "render.json").read_text(encoding="utf-8"))
    assert manifest["mode"] == "full"
    assert len(set(frame_hashes(build))) > 1
    assert main(["validate", str(build), "--json"]) == SUCCESS


def test_manifest_hold_mode_on_full_only_plan_is_rejected(tmp_path, capsys):
    source = block_sprite(tmp_path / "sprite.png")
    build = make_build(tmp_path, capsys, source=source, reduced_motion="full")
    assert render(build) == SUCCESS
    capsys.readouterr()
    manifest_path = build / "render.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["mode"] = "hold_first_frame"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    assert main(["validate", str(build), "--json"]) == VALIDATION_FAILURE
    codes = {error["code"] for error in parsed(capsys)["errors"]}
    assert "RENDER_MODE_MISMATCH" in codes


# ---------------------------------------------------------------------------
# Render manifest integrity at validate time


@pytest.mark.parametrize(
    ("mutate", "code"),
    [
        (lambda m: m.__setitem__("extra", 1), "MALFORMED_RENDER_MANIFEST"),
        (lambda m: m.__setitem__("render_version", 2), "UNSUPPORTED_RENDER_MANIFEST_VERSION"),
        (lambda m: m.__setitem__("generated_by", "hax"), "MALFORMED_RENDER_MANIFEST"),
        (lambda m: m.__setitem__("animation_id", "other"), "ANIMATION_ID_MISMATCH"),
        (
            lambda m: m.__setitem__("plan_digest", "sha256:" + "0" * 64),
            "RENDER_MANIFEST_STALE",
        ),
        (lambda m: m.__setitem__("mode", "sideways"), "MALFORMED_RENDER_MANIFEST"),
        (lambda m: m.pop("mode"), "MALFORMED_RENDER_MANIFEST"),
    ],
)
def test_tampered_render_manifest_fails_validation(tmp_path, capsys, mutate, code):
    source = block_sprite(tmp_path / "sprite.png")
    build = make_build(tmp_path, capsys, source=source)
    assert render(build) == SUCCESS
    capsys.readouterr()
    manifest_path = build / "render.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    mutate(manifest)
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    assert main(["validate", str(build), "--json"]) == VALIDATION_FAILURE
    assert code in {error["code"] for error in parsed(capsys)["errors"]}


def test_manifest_from_other_release_is_only_a_warning(tmp_path, capsys):
    source = block_sprite(tmp_path / "sprite.png")
    build = make_build(tmp_path, capsys, source=source)
    assert render(build) == SUCCESS
    capsys.readouterr()
    manifest_path = build / "render.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["generated_by"] = "sprite-harness 0.0.1"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    assert main(["validate", str(build), "--json"]) == SUCCESS
    payload = parsed(capsys)
    assert payload["valid"] is True
    assert any(
        w["code"] == "GENERATED_BY_MISMATCH" and w.get("artifact") == "render.json"
        for w in payload["warnings"]
    )


def test_generated_manifest_conforms_to_schema(tmp_path, capsys):
    jsonschema = pytest.importorskip("jsonschema")
    source = block_sprite(tmp_path / "sprite.png")
    build = make_build(tmp_path, capsys, source=source)
    assert render(build) == SUCCESS
    capsys.readouterr()
    manifest = json.loads((build / "render.json").read_text(encoding="utf-8"))
    schema = json.loads(
        (REPO_ROOT / "schemas" / "render.schema.json").read_text(encoding="utf-8")
    )
    jsonschema.validate(manifest, schema)


# ---------------------------------------------------------------------------
# Rendering refuses invalid inputs; input checks are separate from old output


def test_render_refuses_tampered_frame_plan(tmp_path, capsys):
    source = block_sprite(tmp_path / "sprite.png")
    build = make_build(
        tmp_path, capsys, source=source, tracks=[track("translate_x", 2)]
    )
    frame_plan_path = build / "frame-plan.json"
    frame_plan = json.loads(frame_plan_path.read_text(encoding="utf-8"))
    frame_plan["frames"][1]["offset"]["x"] = 9.5
    frame_plan_path.write_text(json.dumps(frame_plan), encoding="utf-8")
    assert render(build) == VALIDATION_FAILURE
    payload = parsed(capsys)
    assert "FRAME_PLAN_STALE" in {error["code"] for error in payload["errors"]}
    assert not (build / "frames").exists()
    assert not (build / "render.json").exists()


@pytest.mark.parametrize(
    ("damage", "code"),
    [
        ("replace", "SOURCE_DIGEST_MISMATCH"),
        ("resize", "SOURCE_DIMENSION_MISMATCH"),
        ("delete", "SOURCE_NOT_FOUND"),
    ],
)
def test_render_refuses_damaged_source(tmp_path, capsys, damage, code):
    source = block_sprite(tmp_path / "sprite.png")
    build = make_build(tmp_path, capsys, source=source)
    if damage == "replace":
        Image.new("RGBA", (8, 8), (1, 2, 3, 200)).save(source)
    elif damage == "resize":
        Image.new("RGBA", (9, 9), (1, 2, 3, 200)).save(source)
    else:
        source.unlink()
    assert render(build) == VALIDATION_FAILURE
    assert code in {error["code"] for error in parsed(capsys)["errors"]}
    assert not (build / "frames").exists()


def test_render_requires_a_bound_source(tmp_path, capsys):
    build = make_build(tmp_path, capsys, source=None, canvas=(16, 16))
    assert render(build) == PROCESSING_FAILURE
    assert parsed(capsys)["errors"][0]["code"] == "RENDER_SOURCE_REQUIRED"


def test_render_refuses_non_transparent_background(tmp_path, capsys):
    source = block_sprite(tmp_path / "sprite.png")
    build = make_build(
        tmp_path, capsys, source=source, canvas=(16, 16), background="white"
    )
    assert render(build) == PROCESSING_FAILURE
    assert parsed(capsys)["errors"][0]["code"] == "UNSUPPORTED_BACKGROUND"


def test_render_exit_codes_for_missing_and_malformed_builds(tmp_path, capsys):
    assert render(tmp_path / "missing") == MISSING_INPUT
    assert parsed(capsys)["errors"][0]["code"] == "INPUT_NOT_FOUND"
    source = block_sprite(tmp_path / "sprite.png")
    build = make_build(tmp_path, capsys, source=source)
    (build / "frame-plan.json").write_text("{ not json", encoding="utf-8")
    assert render(build) == MALFORMED_SPECIFICATION
    assert parsed(capsys)["errors"][0]["code"] == "MALFORMED_SPEC"


# ---------------------------------------------------------------------------
# Existing-output handling and transactional writes


def test_render_refuses_existing_output_without_overwrite(tmp_path, capsys):
    source = block_sprite(tmp_path / "sprite.png")
    build = make_build(tmp_path, capsys, source=source)
    assert render(build) == SUCCESS
    capsys.readouterr()
    before = frame_hashes(build)
    assert render(build) == PROCESSING_FAILURE
    assert parsed(capsys)["errors"][0]["code"] == "FRAMES_ALREADY_RENDERED"
    assert frame_hashes(build) == before
    assert render(build, "--overwrite") == SUCCESS
    capsys.readouterr()
    assert frame_hashes(build) == before


def test_overwrite_never_deletes_unknown_files(tmp_path, capsys):
    source = block_sprite(tmp_path / "sprite.png")
    build = make_build(tmp_path, capsys, source=source)
    assert render(build) == SUCCESS
    capsys.readouterr()
    stray = build / "frames" / "user-notes.txt"
    stray.write_text("precious", encoding="utf-8")
    assert render(build, "--overwrite") == PROCESSING_FAILURE
    payload = parsed(capsys)
    assert payload["errors"][0]["code"] == "FRAMES_DIR_CONFLICT"
    assert stray.read_text(encoding="utf-8") == "precious"


def test_overwrite_recovers_from_corrupted_old_frames(tmp_path, capsys):
    # Broken derived output must never block a re-render, and re-rendering
    # must not skip input integrity checks.
    source = block_sprite(tmp_path / "sprite.png")
    build = make_build(tmp_path, capsys, source=source)
    assert render(build) == SUCCESS
    capsys.readouterr()
    (build / "frames" / "frame_001.png").write_bytes(b"garbage")
    assert main(["validate", str(build), "--json"]) == VALIDATION_FAILURE
    capsys.readouterr()
    assert render(build, "--overwrite") == SUCCESS
    capsys.readouterr()
    assert main(["validate", str(build), "--json"]) == SUCCESS


def test_midway_failure_leaves_no_partial_output(tmp_path, capsys, monkeypatch):
    import sprite_harness.render as render_module

    source = block_sprite(tmp_path / "sprite.png")
    build = make_build(tmp_path, capsys, source=source)
    original = render_module._render_frame
    calls = {"count": 0}

    def flaky(*args, **kwargs):
        calls["count"] += 1
        if calls["count"] == 3:
            raise OSError("disk full")
        return original(*args, **kwargs)

    monkeypatch.setattr(render_module, "_render_frame", flaky)
    with pytest.raises(OSError):
        render_build(load_build(build))
    assert not (build / "frames").exists()
    assert not (build / "render.json").exists()
    assert list(build.glob(".render-staging-*")) == []


def test_failed_overwrite_render_keeps_previous_output_intact(
    tmp_path, capsys, monkeypatch
):
    import sprite_harness.render as render_module

    source = block_sprite(tmp_path / "sprite.png")
    build = make_build(tmp_path, capsys, source=source)
    assert render(build) == SUCCESS
    capsys.readouterr()
    before = frame_hashes(build)
    manifest_before = (build / "render.json").read_bytes()

    def explode(*args, **kwargs):
        raise OSError("disk full")

    monkeypatch.setattr(render_module, "_render_frame", explode)
    with pytest.raises(OSError):
        render_build(load_build(build), overwrite=True)
    assert frame_hashes(build) == before
    assert (build / "render.json").read_bytes() == manifest_before
    assert main(["validate", str(build), "--json"]) == SUCCESS
    capsys.readouterr()


# ---------------------------------------------------------------------------
# Determinism and source safety


def test_repeat_renders_are_byte_identical_and_source_untouched(tmp_path, capsys):
    source = block_sprite(tmp_path / "sprite.png")
    source_before = hashlib.sha256(source.read_bytes()).hexdigest()
    tracks = [
        track("translate_x", 1.5, track_id="sub"),
        track("rotate", 12, phase=0.25, track_id="rot"),
        track("scale", 0.1, phase=0.5, track_id="pulse"),
        track("opacity", -0.25, track_id="fade"),
    ]
    first = make_build(tmp_path, capsys, source=source, name="first", tracks=tracks)
    second = make_build(tmp_path, capsys, source=source, name="second", tracks=tracks)
    assert render(first) == SUCCESS
    assert render(second) == SUCCESS
    capsys.readouterr()
    assert frame_hashes(first) == frame_hashes(second)
    assert render(first, "--overwrite") == SUCCESS
    capsys.readouterr()
    assert frame_hashes(first) == frame_hashes(second)
    assert (first / "render.json").read_bytes() == (second / "render.json").read_bytes()
    assert hashlib.sha256(source.read_bytes()).hexdigest() == source_before


# ---------------------------------------------------------------------------
# Model-based validation catches real defects


def bar_build(tmp_path, capsys):
    """16x16 horizontal bar sprite rotated ±90 on a 24x24 canvas."""

    source = tmp_path / "bar.png"
    image = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for x in range(16):
        for y in (7, 8):
            image.putpixel((x, y), (120, 200, 120, 255))
    image.save(source)
    return make_build(
        tmp_path,
        capsys,
        source=source,
        canvas=(24, 24),
        anchor={"type": "center"},
        tracks=[track("rotate", 90, phase=0.25)],
    )


def test_swapped_frames_fail_the_model_check(tmp_path, capsys):
    build = bar_build(tmp_path, capsys)
    assert render(build) == SUCCESS
    capsys.readouterr()
    assert main(["validate", str(build), "--json"]) == SUCCESS
    capsys.readouterr()
    frames = build / "frames"
    a = (frames / "frame_000.png").read_bytes()
    b = (frames / "frame_001.png").read_bytes()
    (frames / "frame_000.png").write_bytes(b)
    (frames / "frame_001.png").write_bytes(a)
    assert main(["validate", str(build), "--json"]) == VALIDATION_FAILURE
    codes = {error["code"] for error in parsed(capsys)["errors"]}
    assert codes & {"BBOX_DRIFT_EXCEEDED", "GROUND_DRIFT_EXCEEDED"}


def test_wrong_content_fails_the_model_check(tmp_path, capsys):
    build = bar_build(tmp_path, capsys)
    assert render(build) == SUCCESS
    capsys.readouterr()
    wrong = Image.new("RGBA", (24, 24), (0, 0, 0, 0))
    for x in range(2, 6):
        for y in range(2, 6):
            wrong.putpixel((x, y), (250, 0, 0, 255))
    wrong.save(build / "frames" / "frame_001.png")
    assert main(["validate", str(build), "--json"]) == VALIDATION_FAILURE
    codes = {error["code"] for error in parsed(capsys)["errors"]}
    assert codes & {"BBOX_DRIFT_EXCEEDED", "GROUND_DRIFT_EXCEEDED"}


def test_rotation_without_source_warns_geometry_unverified(tmp_path, capsys):
    build = make_build(
        tmp_path,
        capsys,
        source=None,
        canvas=(16, 16),
        tracks=[track("rotate", 10, phase=0.25)],
    )
    frames_dir = build / "frames"
    frames_dir.mkdir()
    frame_plan = json.loads((build / "frame-plan.json").read_text(encoding="utf-8"))
    for frame in frame_plan["frames"]:
        image = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
        for x in range(6, 10):
            for y in range(6, 10):
                image.putpixel((x, y), (0, 0, 250, 255))
        image.save(build / frame["file"])
    assert main(["validate", str(build), "--json"]) == SUCCESS
    payload = parsed(capsys)
    assert payload["valid"] is True
    assert any(w["code"] == "GEOMETRY_UNVERIFIED" for w in payload["warnings"])


# ---------------------------------------------------------------------------
# Full pipeline, JSON contract, versions


def test_full_pipeline_render_validate_preview_contact_sheet(tmp_path, capsys):
    source = tmp_path / "sprite.png"
    image = Image.new("RGBA", (24, 32), (0, 0, 0, 0))
    for x in range(6, 18):
        for y in range(4, 28):
            image.putpixel((x, y), (240, 180, 40, 255))
    image.save(source)
    build = make_build(
        tmp_path,
        capsys,
        source=source,
        canvas=(32, 40),
        frame_count=6,
        tracks=[
            track("translate_x", 2, track_id="sway"),
            track("translate_y", 1, phase=0.5, track_id="bob"),
            track("rotate", 5, phase=0.25, track_id="tilt"),
            track("scale", 0.05, phase=0.25, track_id="pulse"),
            track("opacity", -0.1, track_id="fade"),
            track("translate_y", 2, target="head", track_id="local"),
        ],
    )
    assert render(build) == SUCCESS
    payload = parsed(capsys)
    assert payload["success"] is True
    assert payload["frame_count"] == 6
    assert payload["mode"] == "full"
    assert Path(payload["frames_dir"]) == build / "frames"
    assert main(["validate", str(build), "--write-qa", "--json"]) == SUCCESS
    payload = parsed(capsys)
    statuses = {check["id"]: check["status"] for check in payload["checks"]}
    assert statuses["render_manifest"] == "pass"
    assert statuses["frame_files"] == "pass"
    assert main(["preview", str(build), "--json"]) == SUCCESS
    preview = parsed(capsys)
    with Image.open(preview["output"]) as gif:
        assert gif.n_frames == 6
    assert main(["contact-sheet", str(build), "--thumb-size", "32", "--json"]) == SUCCESS
    sheet = parsed(capsys)
    assert Path(sheet["output"]).is_file()
    assert main(["report", str(build), "--json"]) == SUCCESS
    report = parsed(capsys)
    assert report["artifacts"]["render_manifest"]["exists"] is True


def test_render_human_output_reports_frames_and_skips(tmp_path, capsys):
    source = block_sprite(tmp_path / "sprite.png")
    build = make_build(
        tmp_path,
        capsys,
        source=source,
        tracks=[track("translate_y", 3, target="head", track_id="bob")],
    )
    assert main(["render", str(build)]) == SUCCESS
    out = capsys.readouterr().out
    assert "Rendered 4 frames (mode: full)" in out
    assert "bob (head)" in out


def test_version_is_consistent_everywhere(capsys):
    pyproject = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert pyproject["project"]["version"] == __version__
    with pytest.raises(SystemExit) as excinfo:
        main(["--version"])
    assert excinfo.value.code == 0
    assert capsys.readouterr().out.strip() == __version__
