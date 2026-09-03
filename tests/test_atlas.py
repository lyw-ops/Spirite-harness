"""Hand-computed atlas layout, identity and full RGBA round-trip checks."""
import copy
import json
from pathlib import Path
import shutil

import jsonschema
import pytest
from PIL import Image, PngImagePlugin

from sprite_harness.atlas import export_atlas, validate_export
from sprite_harness.build import load_build
from sprite_harness.cli import main
from sprite_harness.contracts import ContractViolation, read_json
from sprite_harness.render import render_build
from test_generation import fixture_build, generated, ROOT
from test_render import parsed


def export_spec(tmp_path, builds, grid=None):
    path = tmp_path / 'export.json'
    doc = {'export_version': 1, 'clips': [{'id': f'clip{i}', 'build': str(p.relative_to(tmp_path))} for i, p in enumerate(builds)],
           'grid': grid or {'cell_width': 12, 'cell_height': 12, 'columns': 3, 'padding': 2}}
    path.write_text(json.dumps(doc))
    return path, doc


def exported(tmp_path, generated_input=False):
    if generated_input:
        build, _ = generated(tmp_path)
    else:
        build = fixture_build(tmp_path)
    render_build(load_build(build), generated_input=generated_input)
    spec, _ = export_spec(tmp_path, [build])
    output = tmp_path / 'atlas'
    export_atlas(spec, output)
    return build, spec, output


def test_hand_computed_multiclip_grid_pivots_and_unused_rgba(tmp_path):
    a = fixture_build(tmp_path, frame_count=2, name='first')
    b = fixture_build(tmp_path, frame_count=3, name='second', size=(10, 6))
    for build in (a, b): render_build(load_build(build))
    spec, doc = export_spec(tmp_path, [b, a], {'cell_width': 14, 'cell_height': 12, 'columns': 3, 'rows': 3, 'padding': 2})
    output = tmp_path / 'atlas'
    export_atlas(spec, output)
    metadata = read_json(output/'atlas.json')
    assert [c['build'] for c in metadata['clips']] == ['../second', '../first']
    frames = [f for c in metadata['clips'] for f in c['frames']]
    assert [(f['rect']['x'], f['rect']['y']) for f in frames] == [(2, 2), (16, 2), (30, 2), (2, 14), (16, 14)]
    assert frames[0]['pivot'] == {'x': 5.0, 'y': 3.0}
    assert frames[0]['atlas_pivot'] == {'x': 7.0, 'y': 5.0}
    assert frames[3]['pivot'] == {'x': 4.0, 'y': 4.0}
    assert frames[3]['atlas_pivot'] == {'x': 6.0, 'y': 18.0}
    assert all(f['duration_ms'] == 125 for f in frames)
    with Image.open(output/'atlas.png') as image:
        assert image.size == (42, 36)
        # Independently locate each complete canvas, checking every unused byte.
        expected = Image.new('RGBA', (42, 36))
        for build, count, positions in [(b, 3, [(2,2),(16,2),(30,2)]), (a, 2, [(2,14),(16,14)])]:
            for i, xy in enumerate(positions):
                with Image.open(build/f'frames/frame_{i:03d}.png') as source:
                    expected.paste(source, xy)
        assert image.tobytes() == expected.tobytes()
    assert validate_export(output)['frame_count'] == 5


@pytest.mark.parametrize('mutation', ['color', 'alpha', 'hidden_rgb', 'padding', 'empty_cell', 'size', 'missing'])
def test_atlas_pixel_corruption(tmp_path, mutation):
    _, _, output = exported(tmp_path)
    path = output/'atlas.png'
    with Image.open(path) as im: image = im.convert('RGBA')
    if mutation == 'color': image.putpixel((4,4), (0,255,0,255))
    elif mutation == 'alpha': image.putpixel((4,4), (255,0,0,128))
    elif mutation == 'hidden_rgb': image.putpixel((5,5), (99,0,0,0))
    elif mutation == 'padding': image.putpixel((0,0), (0,0,0,1))
    elif mutation == 'empty_cell': image.putpixel((30,20), (1,2,3,4))
    elif mutation == 'size': image = Image.new('RGBA', (1,1))
    if mutation == 'missing': path.unlink()
    else: image.save(path)
    with pytest.raises(Exception): validate_export(output)


@pytest.mark.parametrize('field,value', [('index', 1), ('duration', 2.0), ('duration_ms', 100),
                                        ('pivot', {'x': 0, 'y': 0}), ('atlas_pivot', {'x': 0, 'y': 0}),
                                        ('rect', {'x': 3, 'y': 2, 'width': 8, 'height': 8}), ('placement', {'x': 1, 'y': 2})])
def test_metadata_not_trusted_as_layout_oracle(tmp_path, field, value):
    _, _, output = exported(tmp_path)
    path = output/'atlas.json'; doc = read_json(path)
    doc['clips'][0]['frames'][0][field] = value
    path.write_text(json.dumps(doc))
    with pytest.raises(ContractViolation, match='Artifact'): validate_export(output)


def test_swap_cells_rejected(tmp_path):
    _, _, output = exported(tmp_path, generated_input=True)
    path = output/'atlas.png'
    with Image.open(path) as im: image = im.convert('RGBA')
    a = image.crop((2,2,10,10)); b = image.crop((14,2,22,10))
    image.paste(b,(2,2));image.paste(a,(14,2));image.save(path)
    with pytest.raises(ContractViolation) as exc: validate_export(output)
    assert exc.value.code == 'ATLAS_FRAME_MISMATCH'


@pytest.mark.parametrize('change,exit_code', [
    (lambda d: d.__setitem__('export_version', True), 2),
    (lambda d: d.__setitem__('extra', 2), 2),
    (lambda d: d['grid'].__setitem__('columns', True), 2),
    (lambda d: d['grid'].__setitem__('cell_width', 1.0), 2),
    (lambda d: d['grid'].__setitem__('cell_width', -1), 2),
    (lambda d: d['grid'].__setitem__('padding', -1), 2),
    (lambda d: d['grid'].__setitem__('padding', 7), 1),
    (lambda d: d['grid'].__setitem__('rows', 1), 1),
    (lambda d: d['grid'].__setitem__('cell_width', 5), 1),
    (lambda d: d['grid'].update({'cell_width': 16384, 'columns': 16384}), 1),
    (lambda d: d['clips'].append(copy.deepcopy(d['clips'][0])), 1),
])
def test_export_spec_rejections(tmp_path, capsys, change, exit_code):
    build = fixture_build(tmp_path); render_build(load_build(build))
    spec, doc = export_spec(tmp_path, [build]); change(doc); spec.write_text(json.dumps(doc))
    assert main(['export', '--spec', str(spec), '--output', str(tmp_path/'out'), '--json']) == exit_code
    assert parsed(capsys)['errors']
    assert not (tmp_path/'out').exists()


@pytest.mark.parametrize('what', ['source', 'frame', 'render', 'generation', 'spec', 'qa'])
def test_input_and_qa_changes_invalidate_export(tmp_path, what):
    build, spec, output = exported(tmp_path, generated_input=True)
    if what == 'source': p = load_build(build).plan.resolved_source_path(); p.write_bytes(b'bad')
    elif what == 'frame': (build/'frames/frame_000.png').write_bytes(b'bad')
    elif what == 'render': render_build(load_build(build), generated_input=True, reduced_motion=True, overwrite=True)
    elif what == 'generation': (build/'generation/inputs/shape.png').write_bytes(b'bad')
    elif what == 'spec': spec.write_text(spec.read_text() + '\n')
    else:
        p = output/'export.qa.json'; d = read_json(p); d['subjects']['atlas_digest'] = 'sha256:'+'0'*64;p.write_text(json.dumps(d))
    with pytest.raises(Exception): validate_export(output)


def test_rgba_equivalent_reencoding_is_separate_from_byte_identity(tmp_path):
    build, _, output = exported(tmp_path)
    path = build/'frames/frame_001.png'
    with Image.open(path) as im: image = im.convert('RGBA')
    old = path.read_bytes(); info = PngImagePlugin.PngInfo(); info.add_text('encoding', 'changed')
    image.save(path, pnginfo=info)
    assert path.read_bytes() != old
    result = validate_export(output)
    assert result['reencoded_frames'] == [{'clip': 'clip0', 'index': 1}]
    path = output/'atlas.png'
    with Image.open(path) as im: image = im.convert('RGBA')
    image.save(path, pnginfo=info)
    assert validate_export(output)['valid']


def test_hold_bytes_rule_is_not_relaxed_for_atlas(tmp_path):
    build, spec, output = exported(tmp_path)
    render_build(load_build(build), reduced_motion=True, overwrite=True)
    export_atlas(spec, output, overwrite=True)
    path = build/'frames/frame_001.png'
    with Image.open(path) as im: image = im.convert('RGBA')
    info = PngImagePlugin.PngInfo(); info.add_text('encoding', 'changed');image.save(path,pnginfo=info)
    with pytest.raises(ContractViolation) as exc: validate_export(output)
    assert exc.value.code == 'EXPORT_INPUT_INVALID'


def test_repeat_export_and_repair_damaged_old_products(tmp_path):
    _, spec, output = exported(tmp_path)
    before = {p.name: p.read_bytes() for p in output.iterdir()}
    export_atlas(spec, output, overwrite=True)
    assert before == {p.name: p.read_bytes() for p in output.iterdir()}
    (output/'atlas.json').write_bytes(b'broken')
    (output/'atlas.png').write_bytes(b'broken')
    export_atlas(spec, output, overwrite=True)
    assert before == {p.name: p.read_bytes() for p in output.iterdir()}
    assert validate_export(output)['valid']


def test_atlas_schema_and_relocation(tmp_path):
    parent = tmp_path/'parent';parent.mkdir()
    _, _, output = exported(parent, generated_input=True)
    for file, name in [('atlas.json','atlas'),('export-config.json','export-config'),('export-spec.json','export-spec'),('export.qa.json','qa')]:
        jsonschema.validate(read_json(output/file), read_json(ROOT/'schemas'/f'{name}.schema.json'))
    moved = tmp_path/'moved';shutil.move(parent,moved)
    assert validate_export(moved/'atlas')['valid']


@pytest.mark.parametrize('file,field',[('atlas.json','atlas_version'),('export-config.json','config_version')])
@pytest.mark.parametrize('bad',[True,1.0,'1',2,None])
def test_atlas_versions_strict_runtime(tmp_path,file,field,bad):
    from sprite_harness.spec import SpecLoadError
    _,_,out=exported(tmp_path);doc=read_json(out/file);doc[field]=bad;(out/file).write_text(json.dumps(doc))
    with pytest.raises(SpecLoadError):validate_export(out)


def test_export_clip_order_and_timing_tamper(tmp_path):
    a=fixture_build(tmp_path,name='a');b=fixture_build(tmp_path,name='b')
    for build in (a,b):render_build(load_build(build))
    spec,_=export_spec(tmp_path,[b,a]);out=tmp_path/'atlas';export_atlas(spec,out)
    path=out/'atlas.json';doc=read_json(path);doc['clips'].reverse();path.write_text(json.dumps(doc))
    with pytest.raises(ContractViolation):validate_export(out)


def test_old_external_build_frames_are_valid_export_inputs(tmp_path):
    build=fixture_build(tmp_path);render_build(load_build(build));(build/'render.json').unlink()
    # Existing external contract deliberately permits new colors at modeled geometry.
    for p in (build/'frames').iterdir():
        with Image.open(p) as im:image=im.convert('RGBA')
        image.putpixel((2,2),(0,255,0,255));image.save(p)
    spec,_=export_spec(tmp_path,[build]);out=tmp_path/'atlas';export_atlas(spec,out)
    assert validate_export(out)['clips'][0]['backend']=='external'
    assert read_json(out/'atlas.json')['clips'][0]['identities']['render'] is None
