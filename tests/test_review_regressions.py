"""Regression probes from the strict M4/M5 delivery review."""
import json
import os

import pytest

from sprite_harness.atlas import validate_export
from sprite_harness.build import load_build, validate_build
from sprite_harness.contracts import ContractViolation
from sprite_harness.processing import ProcessingError
from sprite_harness.generation import generate_build
from test_atlas import exported
from test_generation import ADAPTER, generated
from test_generation_export_safety import bytes_tree, setup_case


@pytest.mark.parametrize('kind', ['GENERATION', 'EXPORT'])
def test_spec_change_during_normalization_cancels_publication(tmp_path, monkeypatch, kind):
    _, output, marker, action, _, _ = setup_case(tmp_path, kind)
    before = bytes_tree(output)
    name = 'generation' if kind == 'GENERATION' else 'atlas'
    module = __import__('sprite_harness.' + name, fromlist=['x'])
    function = 'normalize_request' if kind == 'GENERATION' else 'normalize_config'
    original = getattr(module, function)

    def change(*args, **kwargs):
        result = original(*args, **kwargs)
        spec = args[1] if kind == 'GENERATION' else args[0]
        spec.write_bytes(spec.read_bytes() + b'\n')
        return result

    monkeypatch.setattr(module, function, change)
    with pytest.raises(ContractViolation) as error:
        action()
    assert error.value.code == 'INPUT_CHANGED'
    assert bytes_tree(output) == before
    assert not marker.exists()


def test_export_config_change_after_first_read_cannot_validate(tmp_path, monkeypatch):
    _, _, output = exported(tmp_path)
    import sprite_harness.atlas as atlas
    original = atlas.read_json
    path = output / 'export-config.json'

    def change(file, *args, **kwargs):
        result = original(file, *args, **kwargs)
        if file == path:
            changed = dict(result)
            changed['grid'] = {**result['grid'], 'columns': 1}
            path.write_text(json.dumps(changed))
        return result

    monkeypatch.setattr(atlas, 'read_json', change)
    with pytest.raises(ContractViolation) as error:
        validate_export(output)
    assert error.value.code == 'INPUT_CHANGED'


@pytest.mark.parametrize('entry', ['extra_file', 'extra_directory', 'input_symlink', 'input_hardlink'])
def test_adapter_cannot_publish_undeclared_entries_or_alias_copy_destination(tmp_path, monkeypatch, entry):
    build, spec = generated(tmp_path)
    import sprite_harness.generation as gen
    original = gen.run_adapter
    before = bytes_tree(build / 'generation')
    source = build.parent / 'build-sources/source.png'
    source_bytes = source.read_bytes()

    def change(argv, request, response, candidates, timeout):
        original(argv, request, response, candidates, timeout)
        staged = request.parent
        if entry == 'extra_file':
            (staged / 'unexpected.txt').write_text('adapter debug output')
        elif entry == 'extra_directory':
            (staged / 'unexpected').mkdir()
        elif entry == 'input_symlink':
            (staged / 'inputs/shape.png').symlink_to(source)
        else:
            os.link(source, staged / 'inputs/shape.png')

    monkeypatch.setattr(gen, 'run_adapter', change)
    try:
        with pytest.raises(ProcessingError):
            generate_build(load_build(build), spec, ADAPTER, overwrite=True)
    finally:
        assert source.read_bytes() == source_bytes
        assert bytes_tree(build / 'generation') == before
        assert not (build / '.generation-transaction').exists()


@pytest.mark.parametrize('entry', ['empty_directory', 'directory_symlink'])
def test_frozen_bundle_rejects_undeclared_directories(tmp_path, entry):
    build, _ = generated(tmp_path)
    path = build / 'generation/unexpected'
    if entry == 'empty_directory':
        path.mkdir()
    else:
        path.symlink_to(tmp_path, target_is_directory=True)
    assert not validate_build(load_build(build))[0].valid
