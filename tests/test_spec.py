from pathlib import Path

import pytest

from sprite_harness.spec import SpecLoadError, load_spec, numeric_sort_key
from sprite_harness.validator import validate_animation


def test_spec_parsing(animation_factory):
    path = animation_factory()
    spec = load_spec(path)
    assert spec.id == "test_animation"
    assert spec.canvas_size == (16, 16)
    assert [frame.duration for frame in spec.frames] == [1.0, 2.0]


def test_unsupported_spec_version_is_structured_validation_error(animation_factory):
    spec = load_spec(animation_factory(version=2))
    result = validate_animation(spec)
    assert not result.valid
    assert result.errors[0].code == "UNSUPPORTED_SPEC_VERSION"
    assert result.errors[0].as_dict()["supported"] == [1]


def test_numeric_frame_ordering():
    paths = [Path("frame_10.png"), Path("frame_2.png"), Path("frame_001.png")]
    assert sorted(paths, key=numeric_sort_key) == [
        Path("frame_001.png"),
        Path("frame_2.png"),
        Path("frame_10.png"),
    ]


def test_malformed_spec_is_rejected(tmp_path):
    spec_path = tmp_path / "animation.yaml"
    spec_path.write_text("frames: [\n", encoding="utf-8")
    with pytest.raises(SpecLoadError) as caught:
        load_spec(spec_path)
    assert caught.value.code == "MALFORMED_SPEC"


def test_unknown_properties_are_rejected(animation_factory):
    path = animation_factory()
    spec_path = path / "animation.yaml"
    spec_path.write_text(spec_path.read_text() + "provider: codex\n", encoding="utf-8")
    with pytest.raises(SpecLoadError) as caught:
        load_spec(path)
    assert caught.value.code == "MALFORMED_SPEC"
    assert caught.value.details["properties"] == ["provider"]
