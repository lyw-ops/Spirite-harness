"""Regression gates for immutable sources, publication, and pixel integrity."""

import hashlib
import json
import os
import subprocess
import sys

import pytest
from PIL import Image, PngImagePlugin

from sprite_harness.build import RENDER_TRANSACTION_DIRNAME, load_build
from sprite_harness.cli import main
from sprite_harness.render import render_build
from test_render import REPO_ROOT, block_sprite, frame_hashes, make_build, parsed, render, track


def snapshot(build):
    return frame_hashes(build), (build / "render.json").read_bytes()


@pytest.mark.parametrize("failure_step", [1, 2, 3, 4])
def test_each_publication_failure_restores_previous_generation(
    tmp_path, capsys, monkeypatch, failure_step
):
    import sprite_harness.render as renderer

    source = block_sprite(tmp_path / "source.png")
    build = make_build(
        tmp_path, capsys, source=source,
        tracks=[track("translate_x", 1, curve="triangle")],
        reduced_motion="hold_first_frame",
    )
    assert render(build) == 0
    capsys.readouterr()
    before = snapshot(build)
    real_replace = renderer.os.replace
    calls = 0

    def flaky_replace(src, dst):
        nonlocal calls
        calls += 1
        if calls == failure_step:
            raise OSError("injected publication failure")
        return real_replace(src, dst)

    monkeypatch.setattr(renderer.os, "replace", flaky_replace)
    assert render(build, "--overwrite", "--reduced-motion") == 4
    assert parsed(capsys)["errors"][0]["code"] == "PROCESSING_ERROR"
    assert snapshot(build) == before
    assert not (build / RENDER_TRANSACTION_DIRNAME).exists()
    assert main(["validate", str(build), "--json"]) == 0


@pytest.mark.parametrize("failure_step", [1, 2])
def test_initial_publication_failure_leaves_no_output(
    tmp_path, capsys, monkeypatch, failure_step
):
    import sprite_harness.render as renderer

    source = block_sprite(tmp_path / "source.png")
    build = make_build(tmp_path, capsys, source=source)
    real_replace = renderer.os.replace
    calls = 0

    def flaky_replace(src, dst):
        nonlocal calls
        calls += 1
        if calls == failure_step:
            raise OSError("injected publication failure")
        return real_replace(src, dst)

    monkeypatch.setattr(renderer.os, "replace", flaky_replace)
    assert render(build) == 4
    capsys.readouterr()
    assert not (build / "frames").exists()
    assert not (build / "render.json").exists()
    assert not (build / RENDER_TRANSACTION_DIRNAME).exists()


def test_failed_rollback_keeps_backups_and_blocks_consumers(tmp_path, capsys, monkeypatch):
    import sprite_harness.render as renderer

    source = block_sprite(tmp_path / "source.png")
    build = make_build(tmp_path, capsys, source=source)
    assert render(build) == 0
    capsys.readouterr()
    before = snapshot(build)
    real_replace = renderer.os.replace
    calls = 0

    def failed_disk(src, dst):
        nonlocal calls
        calls += 1
        if calls >= 3:
            raise OSError("publication and rollback unavailable")
        return real_replace(src, dst)

    monkeypatch.setattr(renderer.os, "replace", failed_disk)
    assert render(build, "--overwrite") == 4
    assert parsed(capsys)["errors"][0]["code"] == "RENDER_RECOVERY_REQUIRED"
    transaction = build / RENDER_TRANSACTION_DIRNAME
    assert (transaction / "previous-render.json").read_bytes() == before[1]
    assert [hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted((transaction / "previous-frames").glob("*.png"))] == before[0]
    assert main(["validate", str(build), "--json"]) == 1
    assert parsed(capsys)["errors"][0]["code"] == "RENDER_TRANSACTION_INCOMPLETE"
    assert render(build, "--overwrite") == 4
    assert parsed(capsys)["errors"][0]["code"] == "RENDER_TRANSACTION_INCOMPLETE"


def test_staged_manifest_failure_does_not_touch_existing_output(tmp_path, capsys, monkeypatch):
    import sprite_harness.render as renderer

    source = block_sprite(tmp_path / "source.png")
    build = make_build(tmp_path, capsys, source=source)
    assert render(build) == 0
    capsys.readouterr()
    before = snapshot(build)

    def fail_manifest(*args, **kwargs):
        raise OSError("manifest write unavailable")

    monkeypatch.setattr(renderer, "write_json_artifact", fail_manifest)
    assert render(build, "--overwrite") == 4
    capsys.readouterr()
    assert snapshot(build) == before
    assert not (build / RENDER_TRANSACTION_DIRNAME).exists()


def test_cleanup_failure_is_fail_closed(tmp_path, capsys, monkeypatch):
    import sprite_harness.render as renderer

    source = block_sprite(tmp_path / "source.png")
    build = make_build(tmp_path, capsys, source=source)

    def fail_cleanup(*args, **kwargs):
        raise OSError("cleanup unavailable")

    with monkeypatch.context() as patch:
        patch.setattr(renderer.shutil, "rmtree", fail_cleanup)
        assert render(build) == 4
        assert parsed(capsys)["errors"][0]["code"] == "RENDER_RECOVERY_REQUIRED"
    assert (build / RENDER_TRANSACTION_DIRNAME).is_dir()
    assert main(["validate", str(build), "--json"]) == 1
    assert parsed(capsys)["errors"][0]["code"] == "RENDER_TRANSACTION_INCOMPLETE"


def test_concurrent_writer_and_reader_refuse_active_transaction(tmp_path, capsys, monkeypatch):
    import sprite_harness.render as renderer

    source = block_sprite(tmp_path / "source.png")
    build = make_build(tmp_path, capsys, source=source)
    original = renderer._render_frame
    visited = False

    def observe(*args, **kwargs):
        nonlocal visited
        if not visited:
            visited = True
            assert render(build, "--overwrite") == 4
            assert parsed(capsys)["errors"][0]["code"] == "RENDER_TRANSACTION_INCOMPLETE"
            assert main(["validate", str(build), "--json"]) == 1
            assert parsed(capsys)["errors"][0]["code"] == "RENDER_TRANSACTION_INCOMPLETE"
        return original(*args, **kwargs)

    monkeypatch.setattr(renderer, "_render_frame", observe)
    assert render(build) == 0
    capsys.readouterr()
    assert visited
    assert main(["validate", str(build), "--json"]) == 0


def test_process_exit_during_publication_cannot_look_like_external_frames(tmp_path, capsys):
    source = block_sprite(tmp_path / "source.png")
    build = make_build(
        tmp_path, capsys, source=source,
        tracks=[track("translate_x", 1, curve="triangle")],
        reduced_motion="hold_first_frame",
    )
    assert render(build) == 0
    capsys.readouterr()
    program = """
import os, sys
from sprite_harness.build import load_build
import sprite_harness.render as renderer
real_replace = renderer.os.replace
calls = 0
def terminate_after_publish(src, dst):
    global calls
    real_replace(src, dst)
    calls += 1
    if calls == 3:
        os._exit(77)
renderer.os.replace = terminate_after_publish
renderer.render_build(load_build(sys.argv[1]), overwrite=True, reduced_motion=True)
"""
    environment = dict(os.environ, PYTHONPATH=str(REPO_ROOT / "src"))
    process = subprocess.run([sys.executable, "-c", program, str(build)], env=environment,
                             capture_output=True, text=True, timeout=15)
    assert process.returncode == 77, process.stderr
    assert (build / RENDER_TRANSACTION_DIRNAME).is_dir()
    assert not (build / "render.json").exists()
    for command in ("validate", "preview", "contact-sheet", "report"):
        assert main([command, str(build), "--json"]) == 1
        payload = parsed(capsys)
        result = payload.get("validation", payload)
        assert result["errors"][0]["code"] == "RENDER_TRANSACTION_INCOMPLETE"
    assert render(build, "--overwrite") == 4
    capsys.readouterr()


@pytest.mark.parametrize("slot", ["frames", "frame", "manifest", "dangling"])
def test_symbolic_link_outputs_are_refused_without_following_them(tmp_path, capsys, slot):
    outside = tmp_path / "outside"
    outside.mkdir()
    source = block_sprite(outside / "frame_000.png")
    before = source.read_bytes()
    build = make_build(tmp_path, capsys, source=source)
    if slot == "frames":
        (build / "frames").symlink_to(outside, target_is_directory=True)
    elif slot == "frame":
        (build / "frames").mkdir()
        (build / "frames" / "frame_000.png").symlink_to(source)
    elif slot == "manifest":
        (build / "render.json").symlink_to(source)
    else:
        (build / "frames").symlink_to(outside / "missing", target_is_directory=True)
    assert render(build, "--overwrite") == 4
    assert parsed(capsys)["errors"][0]["code"] == "FRAMES_DIR_CONFLICT"
    assert source.read_bytes() == before
    assert set(p.name for p in outside.iterdir()) == {"frame_000.png"}
    assert main(["validate", str(build), "--json"]) == 1
    capsys.readouterr()


def test_source_inside_declared_output_slot_is_preserved(tmp_path, capsys):
    (tmp_path / "build" / "frames").mkdir(parents=True)
    source = block_sprite(tmp_path / "build" / "frames" / "frame_000.png")
    before = source.read_bytes()
    build = make_build(tmp_path, capsys, source=source)
    assert render(build, "--overwrite") == 4
    assert parsed(capsys)["errors"][0]["code"] == "FRAMES_DIR_CONFLICT"
    assert source.read_bytes() == before


def test_source_hard_link_in_output_is_refused(tmp_path, capsys):
    source = block_sprite(tmp_path / "source.png")
    before = source.read_bytes()
    build = make_build(tmp_path, capsys, source=source)
    (build / "frames").mkdir()
    os.link(source, build / "frames" / "frame_000.png")
    assert render(build, "--overwrite") == 4
    assert parsed(capsys)["errors"][0]["code"] == "FRAMES_DIR_CONFLICT"
    assert source.read_bytes() == before


@pytest.mark.parametrize("corruption", ["rgb", "alpha", "shape"])
def test_same_bbox_pixel_corruption_is_rejected(tmp_path, capsys, corruption):
    source = block_sprite(tmp_path / "source.png", box=(1, 1, 6, 6))
    build = make_build(tmp_path, capsys, source=source)
    assert render(build) == 0
    capsys.readouterr()
    path = build / "frames" / "frame_001.png"
    with Image.open(path) as original:
        changed = original.convert("RGBA")
    before = changed.getchannel("A").getbbox()
    for y in range(changed.height):
        for x in range(changed.width):
            r, g, b, alpha = changed.getpixel((x, y))
            if alpha and corruption != "shape":
                changed.putpixel((x, y), (0, 255, 0, alpha) if corruption == "rgb"
                                 else (r, g, b, 17))
    if corruption == "shape":
        changed.putpixel((before[0] + 1, before[1] + 1), (0, 0, 0, 0))
    assert changed.getchannel("A").getbbox() == before
    changed.save(path)
    assert main(["validate", str(build), "--json"]) == 1
    assert "FRAME_CONTENT_MISMATCH" in {e["code"] for e in parsed(capsys)["errors"]}


def test_reencoded_png_with_identical_rgba_still_validates(tmp_path, capsys):
    source = block_sprite(tmp_path / "source.png")
    build = make_build(tmp_path, capsys, source=source)
    assert render(build) == 0
    capsys.readouterr()
    path = build / "frames" / "frame_001.png"
    before = path.read_bytes()
    with Image.open(path) as original:
        rgba = original.convert("RGBA")
    metadata = PngImagePlugin.PngInfo()
    metadata.add_text("test", "encoding is not pixel content")
    rgba.save(path, pnginfo=metadata)
    assert path.read_bytes() != before
    assert main(["validate", str(build), "--json"]) == 0
    capsys.readouterr()


def test_external_frames_are_not_forced_to_match_builtin_pixels(tmp_path, capsys):
    source = block_sprite(tmp_path / "source.png")
    build = make_build(tmp_path, capsys, source=source)
    (build / "frames").mkdir()
    # Independently drawn blue content at the source's expected anchor placement.
    for index in range(4):
        block_sprite(build / "frames" / f"frame_{index:03d}.png", size=(16, 16),
                     box=(7, 11, 8, 12), color=(0, 0, 255, 255))
    assert not (build / "render.json").exists()
    assert main(["validate", str(build), "--json"]) == 0
    capsys.readouterr()


@pytest.mark.parametrize("version", [True, False, "1", None, [], {}, 1.5])
def test_render_version_has_strict_type(tmp_path, capsys, version):
    source = block_sprite(tmp_path / "source.png")
    build = make_build(tmp_path, capsys, source=source)
    assert render(build) == 0
    capsys.readouterr()
    path = build / "render.json"
    document = json.loads(path.read_text())
    document["render_version"] = version
    path.write_text(json.dumps(document))
    assert main(["validate", str(build), "--json"]) == 1
    assert "MALFORMED_RENDER_MANIFEST" in {e["code"] for e in parsed(capsys)["errors"]}
    import jsonschema
    schema = json.loads((REPO_ROOT / "schemas" / "render.schema.json").read_text())
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(document, schema)
