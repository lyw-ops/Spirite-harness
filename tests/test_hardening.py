"""Regression tests for build hardening: full frame-plan integrity, source
identity revalidation, strict JSON, loop-cycle continuity, and whole-sprite
offset semantics."""

import json
from pathlib import Path

import pytest
from PIL import Image

from sprite_harness.cli import main
from sprite_harness.curves import SUPPORTED_CURVES, sample_track_value
from sprite_harness.exit_codes import (
    MALFORMED_SPECIFICATION,
    SUCCESS,
    VALIDATION_FAILURE,
)
from sprite_harness.expand import expand_plan, normalize_plan, sample_offsets
from sprite_harness.plan import load_plan
from sprite_harness.plan_validator import validate_plan
from sprite_harness.spec import SpecLoadError


def strict_loads(text: str):
    """Parse with a JSON parser that rejects NaN/Infinity tokens."""

    def reject(token: str):
        raise AssertionError(f"non-standard JSON token emitted: {token}")

    return json.loads(text, parse_constant=reject)


def parsed_stdout(capsys):
    return strict_loads(capsys.readouterr().out)


def sprite_track(**overrides) -> dict:
    track = {
        "track_id": "bob",
        "target": "sprite",
        "motion": "translate_y",
        "amplitude": 2,
        "unit": "px",
        "curve": "sine",
    }
    track.update(overrides)
    return track


def write_spec(tmp_path: Path, **overrides) -> Path:
    data = {
        "plan_version": 1,
        "animation_id": "hardening_loop",
        "canvas": {"width": 32, "height": 32, "background": "transparent"},
        "playback": {"fps": 8, "frame_count": 4, "loop": True},
        "anchor": {"type": "bottom_center"},
        "constraints": {"max_displacement_px": 4, "max_frame_delta_px": 3},
        "tracks": [sprite_track()],
        "events": [{"event_id": "blink", "type": "blink", "frames": [1]}],
    }
    data.update(overrides)
    spec_dir = tmp_path / "spec"
    spec_dir.mkdir(exist_ok=True)
    path = spec_dir / "animation.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def make_build(tmp_path: Path, capsys, *, source: Path | None = None, **overrides) -> Path:
    spec = write_spec(tmp_path, **overrides)
    build = tmp_path / "build"
    argv = ["plan", "--spec", str(spec), "--output", str(build), "--json"]
    if source is not None:
        argv += ["--source", str(source)]
    assert main(argv) == SUCCESS
    capsys.readouterr()
    return build


def make_source(tmp_path: Path, size=(32, 32), color=(10, 20, 30, 255)) -> Path:
    source = tmp_path / "base.png"
    Image.new("RGBA", size, color).save(source)
    return source


def validate_codes(build: Path, capsys) -> tuple[int, set[str], dict]:
    code = main(["validate", str(build), "--json"])
    payload = parsed_stdout(capsys)
    return code, {error["code"] for error in payload["errors"]}, payload


def tamper_frame_plan(build: Path, mutate) -> None:
    path = build / "frame-plan.json"
    frame_plan = json.loads(path.read_text(encoding="utf-8"))
    mutate(frame_plan)
    path.write_text(json.dumps(frame_plan), encoding="utf-8")


# ---------------------------------------------------------------------------
# Issue 1 — full frame-plan integrity


@pytest.mark.parametrize(
    ("mutate", "expected_code"),
    [
        (lambda fp: fp["canvas"].__setitem__("width", 999), "FRAME_PLAN_STALE"),
        (lambda fp: fp["canvas"].__setitem__("width", 32.0), "FRAME_PLAN_STALE"),
        (lambda fp: fp["playback"].__setitem__("fps", 12), "FRAME_PLAN_STALE"),
        (lambda fp: fp["playback"].__setitem__("loop", False), "FRAME_PLAN_STALE"),
        (lambda fp: fp["anchor"].__setitem__("x", 0.25), "FRAME_PLAN_STALE"),
        (lambda fp: fp["anchor"].__setitem__("extra", 1), "FRAME_PLAN_STALE"),
        (
            lambda fp: fp["reduced_motion"].__setitem__("mode", "hold_first_frame"),
            "FRAME_PLAN_STALE",
        ),
        (lambda fp: fp.__setitem__("sneaky", True), "MALFORMED_FRAME_PLAN"),
        (lambda fp: fp.pop("canvas"), "MALFORMED_FRAME_PLAN"),
        (
            lambda fp: fp["frames"][1]["transforms"][0].__setitem__("value", 9.5),
            "FRAME_PLAN_STALE",
        ),
        (lambda fp: fp["frames"][2]["offset"].__setitem__("y", 9.0), "FRAME_PLAN_STALE"),
        (lambda fp: fp["frames"][1].__setitem__("events", []), "FRAME_PLAN_STALE"),
        (
            lambda fp: fp["frames"][0].__setitem__("file", "frames/frame_777.png"),
            "FRAME_PLAN_STALE",
        ),
        (
            lambda fp: fp["frames"][0].__setitem__("annotation", "hi"),
            "FRAME_PLAN_STALE",
        ),
        (
            lambda fp: fp.__setitem__("generated_by", "someone else"),
            "MALFORMED_FRAME_PLAN",
        ),
        (lambda fp: fp.__setitem__("animation_id", "other"), "ANIMATION_ID_MISMATCH"),
        (
            lambda fp: fp.__setitem__("frame_plan_version", 2),
            "UNSUPPORTED_FRAME_PLAN_VERSION",
        ),
    ],
    ids=[
        "canvas-width",
        "canvas-width-type",
        "playback-fps",
        "playback-loop",
        "anchor-x",
        "anchor-unknown-field",
        "reduced-motion-mode",
        "unknown-root-field",
        "missing-root-field",
        "nested-transform-value",
        "nested-offset",
        "nested-events",
        "frame-filename",
        "nested-unknown-field",
        "generated-by",
        "animation-id",
        "frame-plan-version",
    ],
)
def test_tampered_frame_plan_fails(tmp_path, capsys, mutate, expected_code):
    build = make_build(tmp_path, capsys)
    tamper_frame_plan(build, mutate)
    code, codes, _ = validate_codes(build, capsys)
    assert code == VALIDATION_FAILURE
    assert expected_code in codes


def test_frame_plan_stale_reports_first_mismatching_frame(tmp_path, capsys):
    build = make_build(tmp_path, capsys)
    tamper_frame_plan(build, lambda fp: fp["frames"][2]["offset"].__setitem__("y", 9.0))
    code, _, payload = validate_codes(build, capsys)
    assert code == VALIDATION_FAILURE
    stale = [error for error in payload["errors"] if error["code"] == "FRAME_PLAN_STALE"]
    assert stale and stale[0]["section"] == "frames"
    assert stale[0]["first_mismatch_index"] == 2


def test_generated_by_from_other_release_is_warning_only(tmp_path, capsys):
    build = make_build(tmp_path, capsys)
    tamper_frame_plan(build, lambda fp: fp.__setitem__("generated_by", "sprite-harness 0.0.1"))
    code, _, payload = validate_codes(build, capsys)
    assert code == SUCCESS
    assert "GENERATED_BY_MISMATCH" in {warning["code"] for warning in payload["warnings"]}


def test_untouched_build_still_validates(tmp_path, capsys):
    build = make_build(tmp_path, capsys)
    code, codes, payload = validate_codes(build, capsys)
    assert code == SUCCESS
    assert codes == set()
    checks = {check["id"]: check["status"] for check in payload["checks"]}
    assert checks["frame_plan_consistency"] == "pass"
    assert checks["source_identity"] == "skipped"


# ---------------------------------------------------------------------------
# Issue 2 — source identity and digest revalidation


def test_plan_json_source_is_rebased_and_round_trips(tmp_path, capsys):
    source = make_source(tmp_path)
    build = make_build(tmp_path, capsys, source=source)

    plan_document = strict_loads((build / "plan.json").read_text(encoding="utf-8"))
    assert plan_document["source"]["image"] == "../base.png"
    assert plan_document["source"]["sha256"].startswith("sha256:")
    assert plan_document["source"]["width"] == 32
    assert plan_document["source"]["height"] == 32

    # The recorded path resolves from plan.json's location inside the build.
    reloaded = load_plan(build / "plan.json")
    assert reloaded.resolved_source_path() == source.resolve()
    assert validate_plan(reloaded).valid

    frame_plan = strict_loads((build / "frame-plan.json").read_text(encoding="utf-8"))
    assert frame_plan["source"]["path"] == plan_document["source"]["image"]
    assert frame_plan["source"]["sha256"] == plan_document["source"]["sha256"]

    code, _, payload = validate_codes(build, capsys)
    assert code == SUCCESS
    checks = {check["id"]: check["status"] for check in payload["checks"]}
    assert checks["source_identity"] == "pass"


def test_modified_source_bytes_fail_validation(tmp_path, capsys):
    source = make_source(tmp_path)
    build = make_build(tmp_path, capsys, source=source)
    before = source.read_bytes()
    Image.new("RGBA", (32, 32), (99, 99, 99, 255)).save(source)
    code, codes, _ = validate_codes(build, capsys)
    assert code == VALIDATION_FAILURE
    assert "SOURCE_DIGEST_MISMATCH" in codes
    assert "SOURCE_DIMENSION_MISMATCH" not in codes
    assert source.read_bytes() != before  # validation never restores/modifies


def test_resized_source_fails_validation(tmp_path, capsys):
    source = make_source(tmp_path)
    build = make_build(tmp_path, capsys, source=source)
    Image.new("RGBA", (48, 48), (10, 20, 30, 255)).save(source)
    code, codes, _ = validate_codes(build, capsys)
    assert code == VALIDATION_FAILURE
    assert {"SOURCE_DIGEST_MISMATCH", "SOURCE_DIMENSION_MISMATCH"} <= codes


def test_missing_source_fails_validation(tmp_path, capsys):
    source = make_source(tmp_path)
    build = make_build(tmp_path, capsys, source=source)
    source.unlink()
    code, codes, _ = validate_codes(build, capsys)
    assert code == VALIDATION_FAILURE
    assert "SOURCE_NOT_FOUND" in codes


def test_invalid_source_image_fails_validation(tmp_path, capsys):
    source = make_source(tmp_path)
    build = make_build(tmp_path, capsys, source=source)
    source.write_bytes(b"not a png at all")
    code, codes, _ = validate_codes(build, capsys)
    assert code == VALIDATION_FAILURE
    assert "SOURCE_INVALID_IMAGE" in codes


def test_newly_opaque_source_fails_validation(tmp_path, capsys):
    source = make_source(tmp_path)
    build = make_build(tmp_path, capsys, source=source)
    Image.new("RGB", (32, 32), (10, 20, 30)).save(source)
    code, codes, _ = validate_codes(build, capsys)
    assert code == VALIDATION_FAILURE
    assert "SOURCE_ALPHA_REQUIRED" in codes


def test_tampered_frame_plan_source_binding_fails(tmp_path, capsys):
    source = make_source(tmp_path)
    build = make_build(tmp_path, capsys, source=source)
    tamper_frame_plan(
        build, lambda fp: fp["source"].__setitem__("sha256", "sha256:" + "0" * 64)
    )
    code, codes, _ = validate_codes(build, capsys)
    assert code == VALIDATION_FAILURE
    assert "FRAME_PLAN_SOURCE_MISMATCH" in codes


def test_declared_source_identity_is_checked_at_plan_time(tmp_path, capsys):
    source = make_source(tmp_path)
    spec = write_spec(
        tmp_path,
        source={"image": "../base.png", "sha256": "sha256:" + "0" * 64},
    )
    code = main(["plan", "--spec", str(spec), "--output", str(tmp_path / "b"), "--json"])
    payload = parsed_stdout(capsys)
    assert code == VALIDATION_FAILURE
    assert "SOURCE_DIGEST_MISMATCH" in {error["code"] for error in payload["errors"]}
    assert not (tmp_path / "b").exists()
    assert source.is_file()


def test_builds_without_source_still_work(tmp_path, capsys):
    build = make_build(tmp_path, capsys)
    plan_document = strict_loads((build / "plan.json").read_text(encoding="utf-8"))
    assert "source" not in plan_document
    code, _, _ = validate_codes(build, capsys)
    assert code == SUCCESS


def test_artifacts_with_source_are_deterministic(tmp_path, capsys):
    source = make_source(tmp_path)
    spec = write_spec(tmp_path)
    first = tmp_path / "build-a"
    second = tmp_path / "build-b"
    for output in (first, second):
        code = main(
            ["plan", "--spec", str(spec), "--output", str(output),
             "--source", str(source), "--json"]
        )
        assert code == SUCCESS
        capsys.readouterr()
    for name in ("plan.json", "frame-plan.json", "qa/plan.qa.json"):
        assert (first / name).read_bytes() == (second / name).read_bytes()


# ---------------------------------------------------------------------------
# Issue 3 — strict JSON


def test_nan_fps_yields_invalid_fps_and_strict_json(tmp_path, capsys):
    spec = tmp_path / "plan.yaml"
    spec.write_text(
        "plan_version: 1\n"
        "animation_id: nan_fps\n"
        "canvas: {width: 16, height: 16}\n"
        "playback:\n"
        "  fps: .nan\n"
        "  frame_count: 2\n"
        "  loop: true\n",
        encoding="utf-8",
    )
    code = main(["plan", "--spec", str(spec), "--output", str(tmp_path / "b"), "--json"])
    payload = parsed_stdout(capsys)  # strict parser: NaN token would fail here
    assert code == VALIDATION_FAILURE
    errors = {error["code"]: error for error in payload["errors"]}
    assert "INVALID_FPS" in errors
    assert errors["INVALID_FPS"]["actual"] == "NaN"


def test_infinite_amplitude_diagnostics_are_strict_json(tmp_path, capsys):
    spec = tmp_path / "plan.yaml"
    spec.write_text(
        "plan_version: 1\n"
        "animation_id: inf_amp\n"
        "canvas: {width: 16, height: 16}\n"
        "playback: {fps: 8, frame_count: 2, loop: true}\n"
        "tracks:\n"
        "  - {track_id: t, target: sprite, motion: translate_y, amplitude: .inf, unit: px}\n",
        encoding="utf-8",
    )
    code = main(["plan", "--spec", str(spec), "--output", str(tmp_path / "b"), "--json"])
    payload = parsed_stdout(capsys)
    assert code == VALIDATION_FAILURE
    errors = {error["code"]: error for error in payload["errors"]}
    assert errors["INVALID_AMPLITUDE"]["actual"] == "Infinity"


@pytest.mark.parametrize(
    "metadata_yaml",
    [
        "metadata: {created: 2026-09-02}",
        "metadata: {weight: .nan}",
        "metadata: {tags: !!set {a: null, b: null}}",
        "metadata: {1: one}",
    ],
    ids=["date", "nan", "set", "int-key"],
)
def test_non_json_metadata_is_malformed_spec(tmp_path, capsys, metadata_yaml):
    spec = tmp_path / "plan.yaml"
    spec.write_text(
        "plan_version: 1\n"
        "animation_id: meta\n"
        "canvas: {width: 16, height: 16}\n"
        "playback: {fps: 8, frame_count: 2, loop: true}\n"
        f"{metadata_yaml}\n",
        encoding="utf-8",
    )
    code = main(["plan", "--spec", str(spec), "--output", str(tmp_path / "b"), "--json"])
    payload = parsed_stdout(capsys)
    assert code == MALFORMED_SPECIFICATION
    assert payload["errors"][0]["code"] == "METADATA_NOT_JSON_COMPATIBLE"
    assert not (tmp_path / "b").exists()


def test_json_compatible_metadata_round_trips(tmp_path, capsys):
    build = make_build(
        tmp_path,
        capsys,
        metadata={"notes": "ok", "level": 3, "ratio": 0.5, "flags": [True, None]},
    )
    plan_document = strict_loads((build / "plan.json").read_text(encoding="utf-8"))
    assert plan_document["metadata"]["flags"] == [True, None]
    code, _, _ = validate_codes(build, capsys)
    assert code == SUCCESS


def test_persisted_artifacts_and_qa_are_strict_json(tmp_path, capsys):
    source = make_source(tmp_path)
    build = make_build(tmp_path, capsys, source=source)
    assert main(["validate", str(build), "--write-qa", "--json"]) == SUCCESS
    capsys.readouterr()
    for artifact in [
        build / "plan.json",
        build / "frame-plan.json",
        *sorted((build / "qa").glob("*.qa.json")),
    ]:
        strict_loads(artifact.read_text(encoding="utf-8"))


def test_validate_json_output_is_strict_for_invalid_build(tmp_path, capsys):
    build = make_build(tmp_path, capsys)
    plan_path = build / "plan.json"
    document = json.loads(plan_path.read_text(encoding="utf-8"))
    document["playback"]["fps"] = float("nan")
    plan_path.write_text(json.dumps(document), encoding="utf-8")  # json module still emits NaN
    code, codes, _ = validate_codes(build, capsys)  # strict parse inside
    assert code == VALIDATION_FAILURE
    assert "INVALID_FPS" in codes


# ---------------------------------------------------------------------------
# Issue 4 — loop cycle continuity


def test_fractional_cycles_rejected_for_looping_plan(tmp_path, capsys):
    spec = write_spec(tmp_path, tracks=[sprite_track(cycles=2.5)])
    code = main(["plan", "--spec", str(spec), "--output", str(tmp_path / "b"), "--json"])
    payload = parsed_stdout(capsys)
    assert code == VALIDATION_FAILURE
    assert "NON_INTEGRAL_LOOP_CYCLES" in {error["code"] for error in payload["errors"]}


def test_integral_float_cycles_allowed_for_looping_plan(tmp_path, capsys):
    build = make_build(tmp_path, capsys, tracks=[sprite_track(cycles=2.0, amplitude=1)])
    code, _, _ = validate_codes(build, capsys)
    assert code == SUCCESS


def test_fractional_cycles_allowed_for_non_looping_plan(tmp_path, capsys):
    build = make_build(
        tmp_path,
        capsys,
        playback={"fps": 8, "frame_count": 5, "loop": False},
        tracks=[sprite_track(cycles=0.5, amplitude=1)],
        events=[],
    )
    code, _, _ = validate_codes(build, capsys)
    assert code == SUCCESS


@pytest.mark.parametrize("curve", SUPPORTED_CURVES)
@pytest.mark.parametrize("phase", [0.0, 0.3])
@pytest.mark.parametrize("cycles", [1, 2])
def test_looping_curves_are_continuous_at_the_seam(curve, phase, cycles):
    frame_count = 8
    kwargs = dict(loop=True, cycles=cycles, phase=phase)
    wrapped = sample_track_value(curve, 1.0, frame_count, frame_count, **kwargs)
    first = sample_track_value(curve, 1.0, 0, frame_count, **kwargs)
    assert wrapped == pytest.approx(first, abs=1e-9)


def test_fractional_cycles_would_jump_at_the_seam():
    # Demonstrates why the contract exists: without integral cycles the frame
    # after the last differs from frame 0.
    kwargs = dict(loop=True, cycles=1.25, phase=0.0)
    wrapped = sample_track_value("sine", 1.0, 8, 8, **kwargs)
    first = sample_track_value("sine", 1.0, 0, 8, **kwargs)
    assert abs(wrapped - first) > 0.5


# ---------------------------------------------------------------------------
# Issue 5 — whole-sprite vs target-local offsets


def hand_track(**overrides) -> dict:
    track = {
        "track_id": "reach",
        "target": "hand_right",
        "motion": "translate_y",
        "amplitude": 10,
        "unit": "px",
        "curve": "sine",
    }
    track.update(overrides)
    return track


def test_hand_only_translation_does_not_move_global_offset(tmp_path):
    spec = write_spec(tmp_path, tracks=[hand_track()], events=[])
    plan = load_plan(spec)
    result = validate_plan(plan)
    assert result.valid, [error.as_dict() for error in result.errors]  # 10 px hand > 4 px budget: exempt
    assert sample_offsets(plan) == [(0.0, 0.0)] * plan.frame_count
    frame_plan = expand_plan(plan, normalize_plan(plan))
    for frame in frame_plan["frames"]:
        assert frame["offset"] == {"x": 0.0, "y": 0.0}
        assert frame["transforms"][0]["target"] == "hand_right"
    values = [frame["transforms"][0]["value"] for frame in frame_plan["frames"]]
    assert any(value != 0.0 for value in values)  # still expanded per target


def test_sprite_translation_is_the_only_offset_contributor(tmp_path):
    mixed = write_spec(tmp_path, tracks=[sprite_track(), hand_track()], events=[])
    solo_dir = tmp_path / "solo"
    solo_dir.mkdir()
    sprite_only = write_spec(solo_dir, tracks=[sprite_track()], events=[])
    assert sample_offsets(load_plan(mixed)) == sample_offsets(load_plan(sprite_only))


def test_sprite_translation_exceeding_budget_still_fails(tmp_path):
    spec = write_spec(tmp_path, tracks=[sprite_track(amplitude=10)], events=[])
    codes = {error.code for error in validate_plan(load_plan(spec)).errors}
    assert "DISPLACEMENT_EXCEEDED" in codes


def test_rendered_frames_ignore_target_local_motion(tmp_path, capsys):
    build = make_build(tmp_path, capsys, tracks=[sprite_track(), hand_track()], events=[])
    frame_plan = json.loads((build / "frame-plan.json").read_text(encoding="utf-8"))
    frames_dir = build / "frames"
    frames_dir.mkdir()
    for frame in frame_plan["frames"]:
        dx, dy = round(frame["offset"]["x"]), round(frame["offset"]["y"])
        image = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
        for x in range(12 + dx, 20 + dx):
            for y in range(12 + dy, 20 + dy):
                image.putpixel((x, y), (200, 40, 40, 255))
        image.save(build / frame["file"])
    assert main(["validate", str(build), "--json"]) == SUCCESS
    capsys.readouterr()


def test_example_plan_uses_sprite_target_for_whole_sprite_motion():
    example = Path(__file__).resolve().parents[1] / "examples" / "reimu-eating" / "eating-loop.json"
    plan = load_plan(example)
    targets = {track.track_id: track.target for track in plan.tracks}
    assert targets["breathing"] == "sprite"
    assert targets["sway"] == "sprite"
    assert targets["head_bob"] == "head"
    assert targets["eating_hand"] == "hand_right"
    offsets = sample_offsets(plan)
    assert any(offset != (0.0, 0.0) for offset in offsets)


# ---------------------------------------------------------------------------
# Loader hardening


def test_metadata_rejection_via_loader(tmp_path):
    spec = tmp_path / "plan.yaml"
    spec.write_text(
        "plan_version: 1\n"
        "animation_id: meta\n"
        "canvas: {width: 16, height: 16}\n"
        "playback: {fps: 8, frame_count: 2, loop: true}\n"
        "metadata: {when: 2026-01-01}\n",
        encoding="utf-8",
    )
    with pytest.raises(SpecLoadError) as info:
        load_plan(spec)
    assert info.value.code == "METADATA_NOT_JSON_COMPATIBLE"
    assert info.value.details["problems"][0]["path"] == "metadata.when"


def test_invalid_declared_source_identity_is_validation_error(tmp_path):
    spec = write_spec(tmp_path, source={"image": "base.png", "sha256": "bogus", "width": 0})
    codes = {error.code for error in validate_plan(load_plan(spec)).errors}
    assert "INVALID_SOURCE_IDENTITY" in codes
