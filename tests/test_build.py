import json
from pathlib import Path

import pytest
from PIL import Image

from sprite_harness.cli import main
from sprite_harness.exit_codes import (
    MISSING_INPUT,
    PROCESSING_FAILURE,
    SUCCESS,
    VALIDATION_FAILURE,
)


def parsed_stdout(capsys):
    return json.loads(capsys.readouterr().out)


@pytest.fixture
def plan_spec(tmp_path: Path):
    def create(**overrides) -> Path:
        data = {
            "plan_version": 1,
            "animation_id": "test_loop",
            "canvas": {"width": 32, "height": 32, "background": "transparent"},
            "playback": {"fps": 8, "frame_count": 4, "loop": True},
            "anchor": {"type": "bottom_center"},
            "constraints": {"max_displacement_px": 4, "max_frame_delta_px": 3},
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
        }
        data.update(overrides)
        spec_dir = tmp_path / "spec"
        spec_dir.mkdir(exist_ok=True)
        path = spec_dir / "animation.json"
        path.write_text(json.dumps(data), encoding="utf-8")
        return path

    return create


def run_plan(spec: Path, output: Path, *extra: str) -> int:
    return main(["plan", "--spec", str(spec), "--output", str(output), "--json", *extra])


def render_frames(build_dir: Path, *, box_offset: dict[int, tuple[int, int]] | None = None) -> None:
    """Draw a small opaque square per frame at the planned offset."""

    frame_plan = json.loads((build_dir / "frame-plan.json").read_text())
    canvas = frame_plan["canvas"]
    frames_dir = build_dir / "frames"
    frames_dir.mkdir(exist_ok=True)
    for frame in frame_plan["frames"]:
        dx = round(frame["offset"]["x"])
        dy = round(frame["offset"]["y"])
        if box_offset and frame["index"] in box_offset:
            extra = box_offset[frame["index"]]
            dx += extra[0]
            dy += extra[1]
        image = Image.new("RGBA", (canvas["width"], canvas["height"]), (0, 0, 0, 0))
        for x in range(12 + dx, 20 + dx):
            for y in range(12 + dy, 20 + dy):
                image.putpixel((x, y), (200, 40, 40, 255))
        image.save(build_dir / frame["file"])


def test_plan_writes_deterministic_artifacts(plan_spec, tmp_path, capsys):
    spec = plan_spec()
    first = tmp_path / "build-a"
    second = tmp_path / "build-b"
    assert run_plan(spec, first) == SUCCESS
    payload = parsed_stdout(capsys)
    assert payload["success"] is True
    assert payload["frame_count"] == 4
    assert run_plan(spec, second) == SUCCESS
    capsys.readouterr()
    for name in ("plan.json", "frame-plan.json", "qa/plan.qa.json"):
        assert (first / name).read_bytes() == (second / name).read_bytes()
    qa = json.loads((first / "qa" / "plan.qa.json").read_text())
    assert qa["stage"] == "plan"
    assert qa["valid"] is True
    assert {check["id"] for check in qa["checks"]} >= {"plan_semantics", "expansion"}


def test_plan_source_is_recorded_and_untouched(plan_spec, tmp_path, capsys):
    spec = plan_spec()
    source = tmp_path / "base.png"
    Image.new("RGBA", (32, 32), (10, 20, 30, 255)).save(source)
    before = source.read_bytes()
    build = tmp_path / "build"
    assert run_plan(spec, build, "--source", str(source)) == SUCCESS
    capsys.readouterr()
    assert source.read_bytes() == before
    frame_plan = json.loads((build / "frame-plan.json").read_text())
    assert frame_plan["source"]["width"] == 32
    assert frame_plan["source"]["sha256"].startswith("sha256:")
    assert frame_plan["source"]["path"] == "../base.png"


def test_plan_canvas_inherited_from_source(plan_spec, tmp_path, capsys):
    spec = plan_spec()
    data = json.loads(spec.read_text())
    del data["canvas"]
    spec.write_text(json.dumps(data))
    source = tmp_path / "base.png"
    Image.new("RGBA", (48, 64), (0, 0, 0, 255)).save(source)
    build = tmp_path / "build"
    assert run_plan(spec, build, "--source", str(source)) == SUCCESS
    capsys.readouterr()
    plan = json.loads((build / "plan.json").read_text())
    assert plan["canvas"] == {"width": 48, "height": 64, "background": "transparent"}


def test_plan_without_canvas_or_source_fails(plan_spec, tmp_path, capsys):
    spec = plan_spec()
    data = json.loads(spec.read_text())
    del data["canvas"]
    spec.write_text(json.dumps(data))
    assert run_plan(spec, tmp_path / "build") == VALIDATION_FAILURE
    payload = parsed_stdout(capsys)
    assert payload["errors"][0]["code"] == "CANVAS_UNRESOLVED"
    assert not (tmp_path / "build").exists()


def test_plan_missing_source_fails(plan_spec, tmp_path, capsys):
    spec = plan_spec()
    code = run_plan(spec, tmp_path / "build", "--source", str(tmp_path / "missing.png"))
    assert code == VALIDATION_FAILURE
    assert parsed_stdout(capsys)["errors"][0]["code"] == "SOURCE_NOT_FOUND"


def test_plan_opaque_source_with_transparent_canvas_fails(plan_spec, tmp_path, capsys):
    spec = plan_spec()
    source = tmp_path / "base.png"
    Image.new("RGB", (32, 32), (10, 20, 30)).save(source)
    code = run_plan(spec, tmp_path / "build", "--source", str(source))
    assert code == VALIDATION_FAILURE
    assert parsed_stdout(capsys)["errors"][0]["code"] == "SOURCE_ALPHA_REQUIRED"


def test_plan_output_cannot_be_spec_directory(plan_spec, capsys):
    spec = plan_spec()
    assert run_plan(spec, spec.parent) == PROCESSING_FAILURE
    assert parsed_stdout(capsys)["errors"][0]["code"] == "OUTPUT_OVERLAPS_SOURCE"


def test_validate_build_passes_and_writes_qa(plan_spec, tmp_path, capsys):
    spec = plan_spec()
    build = tmp_path / "build"
    assert run_plan(spec, build) == SUCCESS
    capsys.readouterr()
    assert main(["validate", str(build), "--write-qa", "--json"]) == SUCCESS
    payload = parsed_stdout(capsys)
    assert payload["valid"] is True
    assert {check["id"]: check["status"] for check in payload["checks"]}["frame_files"] == "skipped"
    qa = json.loads(Path(payload["qa_report"]).read_text())
    assert qa["stage"] == "build"


def test_validate_detects_tampered_plan(plan_spec, tmp_path, capsys):
    spec = plan_spec()
    build = tmp_path / "build"
    assert run_plan(spec, build) == SUCCESS
    capsys.readouterr()
    plan = json.loads((build / "plan.json").read_text())
    plan["playback"]["fps"] = 12
    (build / "plan.json").write_text(json.dumps(plan))
    assert main(["validate", str(build), "--json"]) == VALIDATION_FAILURE
    codes = {error["code"] for error in parsed_stdout(capsys)["errors"]}
    assert "PLAN_DIGEST_MISMATCH" in codes


def test_validate_detects_hand_edited_frame_plan(plan_spec, tmp_path, capsys):
    spec = plan_spec()
    build = tmp_path / "build"
    assert run_plan(spec, build) == SUCCESS
    capsys.readouterr()
    frame_plan = json.loads((build / "frame-plan.json").read_text())
    frame_plan["frames"][1]["offset"]["y"] = 9.0
    (build / "frame-plan.json").write_text(json.dumps(frame_plan))
    assert main(["validate", str(build), "--json"]) == VALIDATION_FAILURE
    codes = {error["code"] for error in parsed_stdout(capsys)["errors"]}
    assert "FRAME_PLAN_STALE" in codes


def test_validate_build_missing_plan_is_missing_input(plan_spec, tmp_path, capsys):
    spec = plan_spec()
    build = tmp_path / "build"
    assert run_plan(spec, build) == SUCCESS
    capsys.readouterr()
    (build / "plan.json").unlink()
    assert main(["validate", str(build), "--json"]) == MISSING_INPUT
    assert parsed_stdout(capsys)["errors"][0]["code"] == "INPUT_NOT_FOUND"


def test_validate_rendered_frames_pass(plan_spec, tmp_path, capsys):
    spec = plan_spec()
    build = tmp_path / "build"
    assert run_plan(spec, build) == SUCCESS
    capsys.readouterr()
    render_frames(build)
    assert main(["validate", str(build), "--write-qa", "--json"]) == SUCCESS
    payload = parsed_stdout(capsys)
    assert {check["id"]: check["status"] for check in payload["checks"]}["frame_files"] == "pass"
    qa = json.loads(Path(payload["qa_report"]).read_text())
    assert qa["stage"] == "frames"


def test_validate_detects_bbox_drift(plan_spec, tmp_path, capsys):
    spec = plan_spec()
    build = tmp_path / "build"
    assert run_plan(spec, build) == SUCCESS
    capsys.readouterr()
    render_frames(build, box_offset={2: (6, 0)})
    assert main(["validate", str(build), "--json"]) == VALIDATION_FAILURE
    codes = {error["code"] for error in parsed_stdout(capsys)["errors"]}
    assert "BBOX_DRIFT_EXCEEDED" in codes


def test_validate_detects_ground_drift(plan_spec, tmp_path, capsys):
    spec = plan_spec()
    build = tmp_path / "build"
    assert run_plan(spec, build) == SUCCESS
    capsys.readouterr()
    render_frames(build, box_offset={1: (0, 7)})
    assert main(["validate", str(build), "--json"]) == VALIDATION_FAILURE
    codes = {error["code"] for error in parsed_stdout(capsys)["errors"]}
    assert "GROUND_DRIFT_EXCEEDED" in codes


def test_validate_detects_missing_and_unexpected_frames(plan_spec, tmp_path, capsys):
    spec = plan_spec()
    build = tmp_path / "build"
    assert run_plan(spec, build) == SUCCESS
    capsys.readouterr()
    render_frames(build)
    (build / "frames" / "frame_003.png").rename(build / "frames" / "frame_099.png")
    assert main(["validate", str(build), "--json"]) == VALIDATION_FAILURE
    codes = {error["code"] for error in parsed_stdout(capsys)["errors"]}
    assert {"FRAME_MISSING", "UNEXPECTED_FRAME_FILE"} <= codes


def test_validate_detects_wrong_dimensions(plan_spec, tmp_path, capsys):
    spec = plan_spec()
    build = tmp_path / "build"
    assert run_plan(spec, build) == SUCCESS
    capsys.readouterr()
    render_frames(build)
    Image.new("RGBA", (16, 16), (0, 0, 0, 0)).save(build / "frames" / "frame_001.png")
    assert main(["validate", str(build), "--json"]) == VALIDATION_FAILURE
    codes = {error["code"] for error in parsed_stdout(capsys)["errors"]}
    assert {"FRAME_DIMENSION_MISMATCH", "FRAME_EMPTY"} <= codes


def test_preview_and_contact_sheet_on_build(plan_spec, tmp_path, capsys):
    spec = plan_spec()
    build = tmp_path / "build"
    assert run_plan(spec, build) == SUCCESS
    capsys.readouterr()

    # Before rendering, preview is a processing failure with a clear code.
    assert main(["preview", str(build), "--json"]) == PROCESSING_FAILURE
    assert parsed_stdout(capsys)["errors"][0]["code"] == "FRAMES_NOT_RENDERED"

    render_frames(build)
    assert main(["preview", str(build), "--json"]) == SUCCESS
    preview = parsed_stdout(capsys)
    assert preview["output"] == str(build / "preview.gif")
    with Image.open(preview["output"]) as image:
        assert image.n_frames == 4

    assert main(["contact-sheet", str(build), "--thumb-size", "32", "--json"]) == SUCCESS
    sheet = parsed_stdout(capsys)
    assert Path(sheet["output"]) == build / "contact-sheet.png"


def test_report_on_build(plan_spec, tmp_path, capsys):
    spec = plan_spec()
    build = tmp_path / "build"
    assert run_plan(spec, build) == SUCCESS
    capsys.readouterr()
    assert main(["report", str(build), "--json"]) == SUCCESS
    report = parsed_stdout(capsys)
    assert report["animation_id"] == "test_loop"
    assert report["frame_count"] == 4
    assert report["artifacts"]["frames"]["exists"] is False
