import json
from pathlib import Path

from PIL import Image

from sprite_harness.cli import main
from sprite_harness.exit_codes import (
    MALFORMED_SPECIFICATION,
    MISSING_INPUT,
    PROCESSING_FAILURE,
    SUCCESS,
    VALIDATION_FAILURE,
)
from sprite_harness.spec import load_spec
from sprite_harness.validator import validate_animation


def parsed_stdout(capsys):
    return json.loads(capsys.readouterr().out)


def test_validate_json_and_success_status(animation_factory, capsys):
    path = animation_factory()
    assert main(["validate", str(path), "--json"]) == SUCCESS
    payload = parsed_stdout(capsys)
    assert payload["command"] == "validate"
    assert payload["valid"] is True
    assert payload["errors"] == []


def test_missing_input_status(tmp_path, capsys):
    assert main(["validate", str(tmp_path / "missing"), "--json"]) == MISSING_INPUT
    assert parsed_stdout(capsys)["errors"][0]["code"] == "INPUT_NOT_FOUND"


def test_malformed_spec_status(tmp_path, capsys):
    spec = tmp_path / "animation.yaml"
    spec.write_text("version: [", encoding="utf-8")
    assert main(["validate", str(spec), "--json"]) == MALFORMED_SPECIFICATION
    assert parsed_stdout(capsys)["errors"][0]["code"] == "MALFORMED_SPEC"


def test_validation_failure_status(animation_factory, capsys):
    path = animation_factory(fps=0)
    assert main(["validate", str(path), "--json"]) == VALIDATION_FAILURE
    assert parsed_stdout(capsys)["valid"] is False


def test_json_report_structure(animation_factory, capsys):
    path = animation_factory()
    assert main(["report", str(path), "--json"]) == SUCCESS
    report = parsed_stdout(capsys)
    assert report["animation_id"] == "test_animation"
    assert report["frame_count"] == 2
    assert report["canvas"]["width"] == 16
    assert report["validation"] == {"valid": True, "errors": [], "warnings": []}
    assert set(report["artifacts"]) == {
        "preview",
        "contact_sheet",
        "normalized_spec",
        "normalized_frames",
    }


def test_preview_and_contact_sheet(animation_factory, capsys):
    path = animation_factory()
    assert main(["preview", str(path), "--json"]) == SUCCESS
    preview = parsed_stdout(capsys)
    assert preview["durations_ms"] == [167, 333]
    with Image.open(preview["output"]) as image:
        assert image.n_frames == 2
        encoded_durations = []
        for index in range(image.n_frames):
            image.seek(index)
            encoded_durations.append(image.info["duration"])
        assert encoded_durations == [160, 330]

    assert main(["contact-sheet", str(path), "--thumb-size", "64", "--json"]) == SUCCESS
    sheet = parsed_stdout(capsys)
    assert sheet["frame_count"] == 2
    assert Path(sheet["output"]).is_file()


def test_invalid_thumbnail_size_is_processing_failure(animation_factory, capsys):
    path = animation_factory()
    assert (
        main(["contact-sheet", str(path), "--thumb-size", "12", "--json"])
        == PROCESSING_FAILURE
    )
    assert parsed_stdout(capsys)["errors"][0]["code"] == "INVALID_THUMB_SIZE"


def test_artifact_cannot_overwrite_source_frame(animation_factory, capsys):
    path = animation_factory()
    source = path / "frames" / "frame_000.png"
    before = source.read_bytes()
    assert (
        main(["preview", str(path), "--output", str(source), "--json"])
        == PROCESSING_FAILURE
    )
    assert parsed_stdout(capsys)["errors"][0]["code"] == "OUTPUT_OVERLAPS_SOURCE"
    assert source.read_bytes() == before


def test_unexpected_failure_maps_to_processing_exit(
    animation_factory, capsys, monkeypatch
):
    path = animation_factory()

    def fail(*args, **kwargs):
        raise RuntimeError("boom")

    monkeypatch.setattr("sprite_harness.cli.create_preview", fail)
    assert main(["preview", str(path), "--json"]) == PROCESSING_FAILURE
    payload = parsed_stdout(capsys)
    assert payload["errors"][0]["code"] == "PROCESSING_ERROR"
    assert payload["errors"][0]["type"] == "RuntimeError"


def test_normalization_is_non_destructive(animation_factory, capsys):
    path = animation_factory(canvas=(20, 20), image_size=(10, 12), image_mode="RGB")
    source = path / "frames" / "frame_000.png"
    before = source.read_bytes()
    assert main(["normalize", str(path), "--json"]) == SUCCESS
    result = parsed_stdout(capsys)
    assert source.read_bytes() == before
    generated_spec = Path(result["spec"])
    assert generated_spec.is_file()
    generated_validation = validate_animation(load_spec(generated_spec))
    assert generated_validation.valid
    assert result["frames"][0]["position"] == [5, 8]


def test_normalization_custom_output_manifest_paths(animation_factory, tmp_path, capsys):
    path = animation_factory(canvas=(20, 20), image_size=(10, 10))
    output = tmp_path / "custom-derived"
    assert (
        main(["normalize", str(path), "--output", str(output), "--json"])
        == SUCCESS
    )
    result = parsed_stdout(capsys)
    assert validate_animation(load_spec(result["spec"])).valid
    assert load_spec(result["spec"]).frames[0].file == "custom-derived/frame_000.png"


def test_normalization_output_cannot_mix_with_sources(animation_factory, capsys):
    path = animation_factory()
    output = path / "frames" / "derived"
    assert (
        main(["normalize", str(path), "--output", str(output), "--json"])
        == PROCESSING_FAILURE
    )
    assert parsed_stdout(capsys)["errors"][0]["code"] == "OUTPUT_OVERLAPS_SOURCE"
    assert not output.exists()


def test_oversized_normalization_requires_explicit_scale(animation_factory, capsys):
    path = animation_factory(canvas=(10, 10), image_size=(20, 10))
    assert main(["normalize", str(path), "--json"]) == PROCESSING_FAILURE
    assert parsed_stdout(capsys)["errors"][0]["code"] == "FRAME_TOO_LARGE"
    assert main(["normalize", str(path), "--scale", "fit", "--json"]) == SUCCESS
    result = parsed_stdout(capsys)
    assert result["frames"][0]["size"] == [10, 10]
    assert result["frames"][0]["scale"] == 0.5
