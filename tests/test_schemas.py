"""The JSON Schemas and the implementation must not drift apart."""

import json
from pathlib import Path

import jsonschema
import pytest
import yaml

from sprite_harness.cli import main
from sprite_harness.exit_codes import SUCCESS


REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = REPO_ROOT / "schemas"


def load_schema(name: str) -> dict:
    return json.loads((SCHEMAS / name).read_text(encoding="utf-8"))


def test_schemas_are_valid_draft_2020_12():
    for schema_file in sorted(SCHEMAS.glob("*.schema.json")):
        schema = json.loads(schema_file.read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator.check_schema(schema)


def test_example_plan_conforms_to_animation_plan_schema():
    document = json.loads(
        (REPO_ROOT / "examples" / "reimu-eating" / "eating-loop.json").read_text(encoding="utf-8")
    )
    jsonschema.validate(document, load_schema("animation-plan.schema.json"))


def test_animation_plan_schema_accepts_pulse_duty_cycle():
    document = json.loads(
        (REPO_ROOT / "examples" / "reimu-eating" / "eating-loop.json").read_text(
            encoding="utf-8"
        )
    )
    document["tracks"][0]["curve"] = "pulse"
    document["tracks"][0]["duty_cycle"] = 0.25
    jsonschema.validate(document, load_schema("animation-plan.schema.json"))


@pytest.mark.parametrize(
    ("curve", "duty_cycle"),
    [("sine", 0.25), ("pulse", 0)],
)
def test_animation_plan_schema_rejects_invalid_duty_cycle_use(curve, duty_cycle):
    document = json.loads(
        (REPO_ROOT / "examples" / "reimu-eating" / "eating-loop.json").read_text(
            encoding="utf-8"
        )
    )
    document["tracks"][0]["curve"] = curve
    document["tracks"][0]["duty_cycle"] = duty_cycle
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(document, load_schema("animation-plan.schema.json"))


def example_plan_document():
    return json.loads(
        (REPO_ROOT / "examples" / "reimu-eating" / "eating-loop.json").read_text(
            encoding="utf-8"
        )
    )


def keyframe_track_document():
    return {
        "track_id": "food_approach",
        "target": "held_food",
        "motion": "translate_y",
        "unit": "px",
        "keyframes": [
            {"at": 0, "value": -5, "interpolation": "ease_in_out"},
            {"at": 0.28, "value": -14, "interpolation": "ease_in"},
            {"at": 0.52, "value": -7, "interpolation": "hold"},
        ],
    }


def test_animation_plan_schema_accepts_keyframe_track():
    document = example_plan_document()
    document["tracks"][0] = keyframe_track_document()
    jsonschema.validate(document, load_schema("animation-plan.schema.json"))


def test_animation_plan_schema_accepts_non_loop_final_keyframe_at_one():
    document = example_plan_document()
    document["playback"]["loop"] = False
    track = keyframe_track_document()
    track["keyframes"][-1]["at"] = 1
    document["tracks"][0] = track
    jsonschema.validate(document, load_schema("animation-plan.schema.json"))


@pytest.mark.parametrize("mutate", [
    lambda track, document: track.__setitem__("amplitude", 1),
    lambda track, document: track.__setitem__("curve", "sine"),
    lambda track, document: track.__setitem__("keyframes", []),
    lambda track, document: track.__delitem__("keyframes"),
    lambda track, document: track["keyframes"][0].__setitem__("at", 0.1),
    lambda track, document: track["keyframes"][-1].__setitem__("at", 1.5),
    lambda track, document: track["keyframes"][-1].__setitem__("at", 1),
    lambda track, document: track["keyframes"][0].__setitem__("interpolation", "cubic"),
    lambda track, document: track["keyframes"][0].__setitem__("ease", "x"),
    lambda track, document: track["keyframes"][0].__delitem__("value"),
])
def test_animation_plan_schema_rejects_invalid_keyframe_tracks(mutate):
    document = example_plan_document()
    track = keyframe_track_document()
    mutate(track, document)
    document["tracks"][0] = track
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(document, load_schema("animation-plan.schema.json"))


def test_example_manifest_conforms_to_animation_schema():
    document = yaml.safe_load(
        (REPO_ROOT / "examples" / "reimu-eating-task2" / "animation.yaml").read_text(
            encoding="utf-8"
        )
    )
    jsonschema.validate(document, load_schema("animation.schema.json"))


@pytest.fixture
def example_build(tmp_path, capsys):
    build = tmp_path / "build"
    code = main(
        [
            "plan",
            "--spec",
            str(REPO_ROOT / "examples" / "reimu-eating" / "eating-loop.json"),
            "--output",
            str(build),
            "--json",
        ]
    )
    assert code == SUCCESS
    assert main(["validate", str(build), "--write-qa", "--json"]) == SUCCESS
    capsys.readouterr()
    return build


def test_generated_artifacts_conform_to_schemas(example_build):
    plan = json.loads((example_build / "plan.json").read_text(encoding="utf-8"))
    jsonschema.validate(plan, load_schema("animation-plan.schema.json"))

    frame_plan = json.loads((example_build / "frame-plan.json").read_text(encoding="utf-8"))
    jsonschema.validate(frame_plan, load_schema("frame-plan.schema.json"))

    qa_schema = load_schema("qa.schema.json")
    for qa_file in sorted((example_build / "qa").glob("*.qa.json")):
        jsonschema.validate(json.loads(qa_file.read_text(encoding="utf-8")), qa_schema)
