import json
import math
from pathlib import Path

import pytest

from sprite_harness.curves import cycle_position, sample_curve
from sprite_harness.expand import expand_plan, normalize_plan, plan_digest, sample_offsets
from sprite_harness.plan import load_plan
from sprite_harness.plan_validator import validate_plan
from sprite_harness.spec import SpecLoadError


REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_PLAN = REPO_ROOT / "examples" / "reimu-eating" / "eating-loop.json"


def make_plan(tmp_path: Path, **overrides) -> Path:
    data = {
        "plan_version": 1,
        "animation_id": "test_loop",
        "canvas": {"width": 32, "height": 32, "background": "transparent"},
        "playback": {"fps": 8, "frame_count": 8, "loop": True},
        "anchor": {"type": "bottom_center"},
        "constraints": {"max_displacement_px": 4, "max_frame_delta_px": 2},
        "tracks": [
            {
                "track_id": "bob",
                "target": "body",
                "motion": "translate_y",
                "amplitude": 2,
                "unit": "px",
                "curve": "sine",
            }
        ],
        "events": [{"event_id": "blink", "type": "blink", "frames": [3]}],
    }
    data.update(overrides)
    path = tmp_path / "plan.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# Curves


def test_periodic_curves_start_at_zero_and_are_bounded():
    for curve in ("sine", "triangle"):
        assert sample_curve(curve, 0.0) == pytest.approx(0.0)
        values = [sample_curve(curve, i / 100) for i in range(100)]
        assert max(values) <= 1.0 + 1e-9
        assert min(values) >= -1.0 - 1e-9


def test_easing_curves_are_mirrored_and_loop_continuous():
    for curve in ("linear", "ease_in", "ease_out", "ease_in_out"):
        assert sample_curve(curve, 0.0) == pytest.approx(0.0)
        assert sample_curve(curve, 0.5) == pytest.approx(1.0)
        assert sample_curve(curve, 0.25) == pytest.approx(sample_curve(curve, 0.75))


def test_loop_cycle_position_wraps_exactly():
    positions = [cycle_position(i, 8, loop=True, cycles=1, phase=0) for i in range(8)]
    assert positions[0] == 0.0
    assert positions[-1] == pytest.approx(7 / 8)
    # The frame after the last is the first again: u wraps to 0.
    assert math.isclose(cycle_position(8, 8, loop=True, cycles=1, phase=0) % 1.0, 0.0)


def test_non_loop_reaches_cycle_end_on_final_frame():
    # The final frame lands exactly on the cycle boundary, which wraps to 0;
    # every supported curve evaluates identically at u=0 and u=1.
    assert cycle_position(7, 8, loop=False, cycles=1, phase=0) == pytest.approx(0.0, abs=1e-9)
    assert cycle_position(4, 9, loop=False, cycles=1, phase=0) == pytest.approx(0.5)


# ---------------------------------------------------------------------------
# Loading


def test_example_plan_loads_and_validates():
    plan = load_plan(EXAMPLE_PLAN)
    result = validate_plan(plan)
    assert result.valid, [error.as_dict() for error in result.errors]
    assert plan.animation_id == "eating_loop"
    assert plan.frame_count == 12
    assert len(plan.tracks) == 4


def test_missing_plan_file(tmp_path):
    with pytest.raises(SpecLoadError) as info:
        load_plan(tmp_path / "missing.json")
    assert info.value.code == "INPUT_NOT_FOUND"


def test_unknown_root_field_rejected(tmp_path):
    path = make_plan(tmp_path)
    data = json.loads(path.read_text())
    data["reimu_special"] = True
    path.write_text(json.dumps(data))
    with pytest.raises(SpecLoadError) as info:
        load_plan(path)
    assert info.value.code == "MALFORMED_SPEC"


def test_wrong_type_rejected(tmp_path):
    path = make_plan(tmp_path, playback={"fps": "fast", "frame_count": 8, "loop": True})
    with pytest.raises(SpecLoadError):
        load_plan(path)


# ---------------------------------------------------------------------------
# Semantic validation


def error_codes(path):
    return {error.code for error in validate_plan(load_plan(path)).errors}


def test_unsupported_plan_version(tmp_path):
    assert "UNSUPPORTED_PLAN_VERSION" in error_codes(make_plan(tmp_path, plan_version=99))


def test_invalid_animation_id(tmp_path):
    assert "INVALID_ANIMATION_ID" in error_codes(make_plan(tmp_path, animation_id="../evil"))


def test_custom_anchor_requires_coordinates(tmp_path):
    assert "INVALID_ANCHOR" in error_codes(make_plan(tmp_path, anchor={"type": "custom"}))


def test_named_anchor_forbids_coordinates(tmp_path):
    assert "INVALID_ANCHOR" in error_codes(
        make_plan(tmp_path, anchor={"type": "center", "x": 0.5, "y": 0.5})
    )


def test_track_unit_must_match_motion(tmp_path):
    path = make_plan(
        tmp_path,
        tracks=[
            {
                "track_id": "spin",
                "target": "body",
                "motion": "rotate",
                "amplitude": 3,
                "unit": "px",
            }
        ],
    )
    assert "UNIT_MISMATCH" in error_codes(path)


def test_unsupported_curve_and_motion(tmp_path):
    path = make_plan(
        tmp_path,
        tracks=[
            {
                "track_id": "warp",
                "target": "body",
                "motion": "teleport",
                "amplitude": 3,
                "unit": "px",
                "curve": "chaotic",
            }
        ],
    )
    codes = error_codes(path)
    assert {"UNSUPPORTED_MOTION", "UNSUPPORTED_CURVE"} <= codes


def test_duplicate_track_and_event_ids(tmp_path):
    track = {
        "track_id": "bob",
        "target": "body",
        "motion": "translate_y",
        "amplitude": 1,
        "unit": "px",
    }
    path = make_plan(
        tmp_path,
        tracks=[track, dict(track)],
        events=[
            {"event_id": "blink", "type": "blink", "frames": [0]},
            {"event_id": "blink", "type": "blink", "frames": [1]},
        ],
    )
    codes = error_codes(path)
    assert {"DUPLICATE_TRACK_ID", "DUPLICATE_EVENT_ID"} <= codes


def test_event_frames_must_be_in_range(tmp_path):
    path = make_plan(tmp_path, events=[{"event_id": "late", "type": "blink", "frames": [8]}])
    assert "EVENT_FRAME_OUT_OF_RANGE" in error_codes(path)


def test_phase_range(tmp_path):
    path = make_plan(
        tmp_path,
        tracks=[
            {
                "track_id": "bob",
                "target": "body",
                "motion": "translate_y",
                "amplitude": 1,
                "unit": "px",
                "phase": 1.0,
            }
        ],
    )
    assert "INVALID_PHASE" in error_codes(path)


def test_displacement_constraint_enforced(tmp_path):
    path = make_plan(
        tmp_path,
        tracks=[
            {
                "track_id": "jump",
                "target": "body",
                "motion": "translate_y",
                "amplitude": 10,
                "unit": "px",
            }
        ],
    )
    codes = error_codes(path)
    assert "DISPLACEMENT_EXCEEDED" in codes
    assert "FRAME_DELTA_EXCEEDED" in codes


def test_static_plan_gets_zero_motion_warning(tmp_path):
    plan = load_plan(make_plan(tmp_path, tracks=[], events=[]))
    result = validate_plan(plan)
    assert result.valid
    assert {warning.code for warning in result.warnings} == {"ZERO_MOTION"}


# ---------------------------------------------------------------------------
# Expansion


def test_expansion_is_deterministic_and_loop_bounded(tmp_path):
    plan = load_plan(make_plan(tmp_path))
    normalized = normalize_plan(plan)
    first = expand_plan(plan, normalized)
    second = expand_plan(plan, normalized)
    assert first == second
    offsets = sample_offsets(plan)
    assert len(offsets) == 8
    assert offsets[0] == (0.0, 0.0)
    # Loop seam: the wraparound step stays within the same bound as any step.
    deltas = [
        max(abs(b[0] - a[0]), abs(b[1] - a[1]))
        for a, b in zip(offsets, offsets[1:] + offsets[:1])
    ]
    assert max(deltas) <= 2.0


def test_normalize_plan_round_trips_through_loader(tmp_path):
    plan = load_plan(EXAMPLE_PLAN)
    normalized = normalize_plan(plan)
    rewritten = tmp_path / "normalized.json"
    rewritten.write_text(json.dumps(normalized), encoding="utf-8")
    reloaded = load_plan(rewritten)
    assert validate_plan(reloaded).valid
    assert normalize_plan(reloaded) == normalized
    assert plan_digest(normalize_plan(reloaded)) == plan_digest(normalized)


def test_frame_plan_shape(tmp_path):
    plan = load_plan(make_plan(tmp_path))
    normalized = normalize_plan(plan)
    frame_plan = expand_plan(plan, normalized)
    assert frame_plan["frame_plan_version"] == 1
    assert frame_plan["plan_digest"].startswith("sha256:")
    assert frame_plan["anchor"] == {"type": "bottom_center", "x": 0.5, "y": 1.0}
    frames = frame_plan["frames"]
    assert [frame["index"] for frame in frames] == list(range(8))
    assert frames[0]["file"] == "frames/frame_000.png"
    assert frames[3]["events"] == ["blink"]
    assert frames[0]["transforms"][0]["motion"] == "translate_y"
    assert frames[0]["time_s"] == 0.0
    assert frames[1]["time_s"] == pytest.approx(1 / 8)
