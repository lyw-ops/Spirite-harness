import json
import math
from pathlib import Path

import pytest

from sprite_harness.curves import (
    cycle_position,
    keyframe_position,
    sample_curve,
    sample_keyframes,
)
from sprite_harness.expand import expand_plan, normalize_plan, plan_digest, sample_offsets
from sprite_harness.plan import Keyframe, Track, load_plan
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
                "target": "sprite",
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


def test_pulse_curve_uses_declared_duty_cycle():
    assert sample_curve("pulse", 0.0, duty_cycle=0.25) == 1.0
    assert sample_curve("pulse", 0.249999, duty_cycle=0.25) == 1.0
    assert sample_curve("pulse", 0.25, duty_cycle=0.25) == -1.0
    assert sample_curve("pulse", 0.999999, duty_cycle=0.25) == -1.0


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
# Keyframe sampling


def keyframes(*points):
    return tuple(Keyframe(at=at, value=value, interpolation=interpolation)
                 for at, value, interpolation in points)


def test_keyframe_position_mappings():
    assert [keyframe_position(i, 8, loop=True) for i in range(8)] == [i / 8 for i in range(8)]
    # The frame after the last is the seam: time 1 wraps to exactly 0.
    assert keyframe_position(8, 8, loop=True) == 0.0
    assert keyframe_position(4, 5, loop=False) == 1.0
    assert keyframe_position(0, 1, loop=False) == 0.0


def test_keyframes_are_hit_exactly():
    timeline = keyframes((0.0, -5.0, "ease_in_out"), (0.25, -14.0, "ease_in"),
                         (0.5, -16.0, "ease_out"), (0.75, -7.0, "linear"))
    for loop in (True, False):
        for keyframe in timeline:
            assert sample_keyframes(timeline, keyframe.at, loop=loop) == keyframe.value


@pytest.mark.parametrize(("interpolation", "expected"), [
    ("linear", 5.0),
    ("ease_in", 2.5),
    ("ease_out", 7.5),
    ("ease_in_out", 5.0),
    ("hold", 0.0),
])
def test_each_interpolation_shape_mid_segment(interpolation, expected):
    timeline = keyframes((0.0, 0.0, interpolation), (0.5, 10.0, "hold"))
    assert sample_keyframes(timeline, 0.25, loop=False) == pytest.approx(expected)


def test_ease_in_and_out_quarter_points():
    timeline = keyframes((0.0, 0.0, "ease_in"), (1.0, 1.0, "hold"))
    assert sample_keyframes(timeline, 0.25, loop=False) == pytest.approx(0.0625)
    timeline = keyframes((0.0, 0.0, "ease_out"), (1.0, 1.0, "hold"))
    assert sample_keyframes(timeline, 0.25, loop=False) == pytest.approx(0.4375)


def test_hold_keeps_value_and_steps_exactly_on_the_next_keyframe():
    timeline = keyframes((0.0, 3.0, "hold"), (0.5, -2.0, "linear"))
    assert sample_keyframes(timeline, 0.0, loop=False) == 3.0
    assert sample_keyframes(timeline, 0.499999, loop=False) == 3.0
    assert sample_keyframes(timeline, 0.5, loop=False) == -2.0


def test_loop_wrap_segment_returns_to_the_first_value_at_the_seam():
    timeline = keyframes((0.0, 0.0, "linear"), (0.5, 10.0, "linear"))
    # Wrap segment interpolates from the last keyframe back to the first value.
    assert sample_keyframes(timeline, 0.75, loop=True) == pytest.approx(5.0)
    assert sample_keyframes(timeline, 0.999999, loop=True) == pytest.approx(0.0, abs=1e-4)
    # Frame 0 of the next repetition (time 1 wraps to 0) is the first value.
    assert sample_keyframes(timeline, keyframe_position(8, 8, loop=True), loop=True) == 0.0


def test_loop_hold_last_segment_steps_exactly_at_the_seam():
    timeline = keyframes((0.0, 1.0, "hold"), (0.5, -1.0, "hold"))
    assert sample_keyframes(timeline, 0.999999, loop=True) == -1.0
    assert sample_keyframes(timeline, 0.0, loop=True) == 1.0


def test_non_loop_tail_holds_the_last_value():
    timeline = keyframes((0.0, 0.0, "linear"), (0.5, 10.0, "ease_in_out"))
    assert sample_keyframes(timeline, 0.75, loop=False) == 10.0
    assert sample_keyframes(timeline, 1.0, loop=False) == 10.0


def test_single_keyframe_is_a_constant_track():
    timeline = keyframes((0.0, -0.5, "linear"))
    for loop in (True, False):
        for u in (0.0, 0.3, 0.999999, 1.0 if not loop else 0.5):
            assert sample_keyframes(timeline, u, loop=loop) == -0.5


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


@pytest.mark.parametrize("duty_cycle", [0, -0.1, 1.1, float("inf")])
def test_pulse_duty_cycle_range(tmp_path, duty_cycle):
    path = make_plan(
        tmp_path,
        tracks=[{
            "track_id": "blink",
            "target": "body",
            "motion": "opacity",
            "amplitude": 1,
            "unit": "ratio",
            "curve": "pulse",
            "duty_cycle": duty_cycle,
        }],
    )
    assert "INVALID_DUTY_CYCLE" in error_codes(path)


def test_duty_cycle_requires_pulse_curve(tmp_path):
    path = make_plan(
        tmp_path,
        tracks=[{
            "track_id": "bad_duty",
            "target": "body",
            "motion": "opacity",
            "amplitude": -0.5,
            "unit": "ratio",
            "curve": "sine",
            "duty_cycle": 0.25,
        }],
    )
    assert "DUTY_CYCLE_REQUIRES_PULSE" in error_codes(path)


def test_pulse_default_is_normalized_and_roundtrips(tmp_path):
    path = make_plan(
        tmp_path,
        tracks=[{
            "track_id": "blink",
            "target": "body",
            "motion": "opacity",
            "amplitude": 1,
            "unit": "ratio",
            "curve": "pulse",
        }],
    )
    normalized = normalize_plan(load_plan(path))
    assert normalized["tracks"][0]["duty_cycle"] == 0.5
    normalized_path = tmp_path / "normalized.json"
    normalized_path.write_text(json.dumps(normalized))
    reloaded = load_plan(normalized_path)
    assert normalize_plan(reloaded) == normalized


def test_track_positional_field_order_is_stable():
    # Regression: the historical positional order (track_id, target, motion,
    # amplitude, unit) is API for existing constructors and must not shift
    # when keyframe fields are added behind it.
    track = Track("bob", "sprite", "translate_y", 2.0, "px")
    assert track.amplitude == 2.0
    assert track.unit == "px"
    assert track.curve == "sine"
    assert track.cycles == 1.0
    assert track.phase == 0.0
    assert track.duty_cycle is None
    assert track.keyframes is None


def keyframe_track(track_keyframes, **overrides):
    data = {
        "track_id": "kf",
        "target": "sprite",
        "motion": "translate_y",
        "unit": "px",
        "keyframes": track_keyframes,
    }
    data.update(overrides)
    return data


@pytest.mark.parametrize("legacy_field", [
    {"amplitude": 1},
    {"curve": "sine"},
    {"cycles": 2},
    {"phase": 0.5},
    {"duty_cycle": 0.5},
])
def test_keyframes_reject_curve_track_fields(tmp_path, legacy_field):
    path = make_plan(tmp_path, tracks=[keyframe_track([{"at": 0, "value": 0}], **legacy_field)])
    with pytest.raises(SpecLoadError) as info:
        load_plan(path)
    assert info.value.code == "TRACK_MODE_CONFLICT"


@pytest.mark.parametrize("track_keyframes", [
    "not-an-array",
    [{"at": 0, "value": 0, "easing": "linear"}],
    [{"at": 0}],
    [{"value": 0}],
    [{"at": "0", "value": 0}],
    [{"at": 0, "value": 0, "interpolation": 3}],
])
def test_malformed_keyframes_rejected_at_load(tmp_path, track_keyframes):
    path = make_plan(tmp_path, tracks=[keyframe_track(track_keyframes)])
    with pytest.raises(SpecLoadError) as info:
        load_plan(path)
    assert info.value.code == "MALFORMED_SPEC"


def test_empty_keyframes_rejected(tmp_path):
    path = make_plan(tmp_path, tracks=[keyframe_track([])])
    assert "INSUFFICIENT_KEYFRAMES" in error_codes(path)


@pytest.mark.parametrize("track_keyframes", [
    [{"at": 0.1, "value": 0}],
    [{"at": 0, "value": 0}, {"at": 0.5, "value": 1}, {"at": 0.5, "value": 2}],
    [{"at": 0, "value": 0}, {"at": 0.5, "value": 1}, {"at": 0.25, "value": 2}],
    [{"at": 0, "value": 0}, {"at": -0.5, "value": 1}],
    [{"at": 0, "value": 0}, {"at": 1.0, "value": 1}],
    [{"at": 0, "value": 0}, {"at": 1.5, "value": 1}],
    [{"at": 0, "value": 0}, {"at": float("inf"), "value": 1}],
])
def test_invalid_keyframe_times(tmp_path, track_keyframes):
    path = make_plan(tmp_path, tracks=[keyframe_track(track_keyframes)])
    assert "INVALID_KEYFRAME_TIME" in error_codes(path)


def test_non_loop_allows_final_keyframe_at_time_one(tmp_path):
    path = make_plan(
        tmp_path,
        playback={"fps": 8, "frame_count": 8, "loop": False},
        tracks=[keyframe_track([
            {"at": 0, "value": 0},
            {"at": 1, "value": -3, "interpolation": "ease_out"},
        ])],
    )
    assert error_codes(path) == set()


def test_invalid_keyframe_value(tmp_path):
    path = make_plan(tmp_path, tracks=[keyframe_track([{"at": 0, "value": float("nan")}])])
    assert "INVALID_KEYFRAME_VALUE" in error_codes(path)


def test_unsupported_interpolation(tmp_path):
    path = make_plan(
        tmp_path,
        tracks=[keyframe_track([{"at": 0, "value": 0, "interpolation": "cubic"}])],
    )
    assert "UNSUPPORTED_INTERPOLATION" in error_codes(path)


def test_keyframe_track_unit_mismatch(tmp_path):
    path = make_plan(tmp_path, tracks=[keyframe_track([{"at": 0, "value": 0}], unit="deg")])
    assert "UNIT_MISMATCH" in error_codes(path)


def test_keyframed_sprite_translation_enforces_displacement(tmp_path):
    path = make_plan(
        tmp_path,
        tracks=[keyframe_track([{"at": 0, "value": 0}, {"at": 0.5, "value": -16}])],
    )
    assert "DISPLACEMENT_EXCEEDED" in error_codes(path)


@pytest.mark.parametrize(("motion", "value", "code"), [
    ("opacity", -1.5, "INVALID_EFFECTIVE_OPACITY"),
    ("opacity", -1, "FULLY_TRANSPARENT_FRAME"),
    ("scale", -1, "INVALID_EFFECTIVE_SCALE"),
])
def test_keyframed_effective_value_rules(tmp_path, motion, value, code):
    path = make_plan(
        tmp_path,
        tracks=[keyframe_track(
            [
                {"at": 0, "value": 0, "interpolation": "hold"},
                {"at": 0.5, "value": value, "interpolation": "hold"},
            ],
            motion=motion,
            unit="ratio",
        )],
    )
    assert code in error_codes(path)


def test_keyframe_track_expansion_hits_and_interpolates_exactly(tmp_path):
    path = make_plan(
        tmp_path,
        tracks=[keyframe_track([
            {"at": 0, "value": 0, "interpolation": "linear"},
            {"at": 0.5, "value": -4, "interpolation": "linear"},
        ])],
    )
    plan = load_plan(path)
    result = validate_plan(plan)
    assert result.valid, [error.as_dict() for error in result.errors]
    frame_plan = expand_plan(plan, normalize_plan(plan))
    values = [frame["transforms"][0]["value"] for frame in frame_plan["frames"]]
    # Linear ramp to the keyframe at mid-loop, wrap segment back to frame 0.
    assert values == [0.0, -1.0, -2.0, -3.0, -4.0, -3.0, -2.0, -1.0]
    assert [frame["offset"]["y"] for frame in frame_plan["frames"]] == values


def test_keyframe_track_normalization_roundtrips_and_is_deterministic(tmp_path):
    path = make_plan(
        tmp_path,
        constraints={},
        tracks=[keyframe_track([
            {"at": 0, "value": -5},
            {"at": 0.25, "value": -14, "interpolation": "ease_in"},
            {"at": 0.5, "value": -7, "interpolation": "hold"},
        ])],
    )
    plan = load_plan(path)
    normalized = normalize_plan(plan)
    track_document = normalized["tracks"][0]
    assert set(track_document) == {"track_id", "target", "motion", "unit", "keyframes"}
    assert track_document["keyframes"][0]["interpolation"] == "linear"
    normalized_path = tmp_path / "normalized.json"
    normalized_path.write_text(json.dumps(normalized))
    reloaded = load_plan(normalized_path)
    assert normalize_plan(reloaded) == normalized
    assert plan_digest(normalize_plan(reloaded)) == plan_digest(normalized)


def test_displacement_constraint_enforced(tmp_path):
    path = make_plan(
        tmp_path,
        tracks=[
            {
                "track_id": "jump",
                "target": "sprite",
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
