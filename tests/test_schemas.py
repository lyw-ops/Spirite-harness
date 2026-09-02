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
