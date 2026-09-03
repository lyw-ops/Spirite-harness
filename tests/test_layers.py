"""Layered contract and independent pixel oracles; no renderer-generated expectations."""
import copy
import hashlib
import json
import os
import shutil
from pathlib import Path

import jsonschema
import pytest
from PIL import Image, PngImagePlugin

from sprite_harness.build import create_build, load_build, validate_build
from sprite_harness.cli import main
from sprite_harness.expand import normalize_plan
from sprite_harness.plan import load_plan
from test_render import REPO_ROOT, parsed, track, render, nonzero_pixels, frame_hashes

RED = (255, 0, 0, 255)
BLUE = (0, 0, 255, 255)


def layer(target, image, position=(4, 4), anchor=None):
    return {"target": target, "image": str(image),
            "anchor": anchor or {"type": "center"},
            "position": {"x": position[0], "y": position[1]}}


def write_spec(tmp_path, layers=None, **updates):
    directory = tmp_path / 'spec'
    directory.mkdir(exist_ok=True)
    if layers is None:
        for name, size, color in [('back', (4, 4), RED), ('front', (2, 2), BLUE)]:
            Image.new('RGBA', size, color).save(directory / f'{name}.png')
        layers = [layer('back', 'back.png'), layer('front', 'front.png')]
    doc = {"plan_version": 2, "animation_id": "layers", "playback": {"fps": 8, "frame_count": 4, "loop": True},
           "source": {"reference_canvas": {"width": 8, "height": 8}, "layers": layers},
           "anchor": {"type": "center"}, "tracks": []}
    doc.update(updates)
    path = directory / 'animation.json'
    path.write_text(json.dumps(doc))
    return path, doc


def build_layers(tmp_path, capsys, layers=None, **updates):
    path, _ = write_spec(tmp_path, layers, **updates)
    build = tmp_path / 'build'
    assert main(['plan', '--spec', str(path), '--output', str(build), '--json']) == 0
    parsed(capsys)
    return build


def read_pixels(build, index=0):
    return nonzero_pixels(build / 'frames' / f'frame_{index:03d}.png')


def assert_valid(build, capsys):
    assert main(['validate', str(build), '--json']) == 0
    return parsed(capsys)


def run_bad_spec(tmp_path, capsys, change, expected_code, exit_code=1):
    path, doc = write_spec(tmp_path)
    change(doc)
    path.write_text(json.dumps(doc))
    code = main(['plan', '--spec', str(path), '--output', str(tmp_path / 'build'), '--json'])
    payload = parsed(capsys)
    assert code == exit_code, payload
    assert expected_code in {e['code'] for e in payload['errors']}
    assert not (tmp_path / 'build').exists()


@pytest.mark.parametrize('change,code', [
    (lambda d: d['source'].__setitem__('layers', []), 'EMPTY_LAYERS'),
    (lambda d: d['source']['layers'][1].__setitem__('target', 'back'), 'DUPLICATE_LAYER_TARGET'),
    (lambda d: d['source']['layers'][1].__setitem__('target', 'sprite'), 'RESERVED_LAYER_TARGET'),
    (lambda d: d.__setitem__('tracks', [track('rotate', 1, target='missing')]), 'UNKNOWN_LAYER_TARGET'),
    (lambda d: d.__setitem__('events', [{'event_id':'e','type':'blink','target':'missing','frames':[0]}]), 'UNKNOWN_LAYER_TARGET'),
    (lambda d: d.__setitem__('plan_version', 1), 'PLAN_SOURCE_VERSION_MISMATCH'),
    (lambda d: d.__setitem__('source', {'image':'back.png'}), 'PLAN_SOURCE_VERSION_MISMATCH'),
    (lambda d: d['source']['reference_canvas'].__setitem__('width', 0), 'INVALID_REFERENCE_CANVAS'),
    (lambda d: d['source']['layers'][0].__setitem__('anchor', {'type':'custom','x':2,'y':0}), 'INVALID_LAYER_ANCHOR'),
    (lambda d: d['source']['layers'][0].__setitem__('anchor', {'type':'center','x':0}), 'INVALID_LAYER_ANCHOR'),
    (lambda d: d['source']['layers'][0].__setitem__('anchor', {'type':'custom','x':0}), 'INVALID_LAYER_ANCHOR'),
    (lambda d: d['source']['layers'][0]['position'].__setitem__('x', float('inf')), 'INVALID_LAYER_POSITION'),
    (lambda d: d['source']['layers'][0].__setitem__('sha256', 'bad'), 'INVALID_SOURCE_IDENTITY'),
    (lambda d: d['source']['layers'][0].__setitem__('width', 0), 'INVALID_SOURCE_IDENTITY'),
])
def test_semantic_rejections(tmp_path, capsys, change, code):
    run_bad_spec(tmp_path, capsys, change, code)


@pytest.mark.parametrize('change,code', [
    (lambda d: d['source'].__setitem__('image','back.png'), 'SOURCE_MODE_CONFLICT'),
    (lambda d: d.__setitem__('plan_version', True), 'MALFORMED_SPEC'),
    (lambda d: d['source'].__setitem__('layers', {}), 'MALFORMED_SPEC'),
    (lambda d: d['source'].__delitem__('reference_canvas'), 'MALFORMED_SPEC'),
    (lambda d: d['source']['reference_canvas'].__setitem__('width', True), 'MALFORMED_SPEC'),
    (lambda d: d['source']['layers'][0].__setitem__('width', True), 'MALFORMED_SPEC'),
    (lambda d: d['source']['layers'][0].__setitem__('target', 9), 'MALFORMED_SPEC'),
    (lambda d: d['source']['layers'][0].__setitem__('image', None), 'MALFORMED_SPEC'),
    (lambda d: d['source']['layers'][0].__setitem__('z_index', 2), 'MALFORMED_SPEC'),
    (lambda d: d['source']['layers'][0].__delitem__('anchor'), 'MALFORMED_SPEC'),
    (lambda d: d['source']['layers'][0].__delitem__('position'), 'MALFORMED_SPEC'),
    (lambda d: d['source']['layers'][0]['position'].__setitem__('x', '4'), 'MALFORMED_SPEC'),
    (lambda d: d['source']['layers'][0]['position'].__setitem__('z', 0), 'MALFORMED_SPEC'),
    (lambda d: d['source'].__setitem__('directory', '.'), 'MALFORMED_SPEC'),
])
def test_shape_rejections_and_schema_parity(tmp_path, capsys, change, code):
    run_bad_spec(tmp_path, capsys, change, code, 2)
    document = json.loads((tmp_path / 'spec' / 'animation.json').read_text())
    schema = json.loads((REPO_ROOT / 'schemas' / 'animation-plan.schema.json').read_text())
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(document, schema)


def test_cli_source_override_conflicts(tmp_path, capsys):
    path, _ = write_spec(tmp_path)
    assert main(['plan','--spec',str(path),'--source',str(path.parent/'back.png'),'--json']) == 2
    assert parsed(capsys)['errors'][0]['code'] == 'SOURCE_MODE_CONFLICT'


@pytest.mark.parametrize('index', [0, 1])
@pytest.mark.parametrize('damage,code', [
    ('missing', 'SOURCE_NOT_FOUND'), ('bad', 'SOURCE_INVALID_IMAGE'),
    ('alpha', 'SOURCE_ALPHA_REQUIRED'), ('format', 'SOURCE_PNG_REQUIRED'),
    ('replace', 'SOURCE_DIGEST_MISMATCH'), ('resize', 'SOURCE_DIMENSION_MISMATCH'),
])
def test_every_source_is_rechecked(tmp_path, capsys, index, damage, code):
    build = build_layers(tmp_path, capsys)
    source = tmp_path / 'spec' / ('back.png' if index == 0 else 'front.png')
    size = (4, 4) if index == 0 else (2, 2)
    if damage == 'missing': source.unlink()
    elif damage == 'bad': source.write_bytes(b'broken')
    elif damage == 'alpha': Image.new('RGB', size).save(source)
    elif damage == 'format': Image.new('RGBA', size).save(source, format='TIFF')
    else: Image.new('RGBA', (5, 5) if damage == 'resize' else size, (4, 5, 6, 7)).save(source)
    for command in ['validate', 'render']:
        assert main([command, str(build), '--json']) == 1
        assert code in {e['code'] for e in parsed(capsys)['errors']}
    assert not (build / 'frames').exists()


@pytest.mark.parametrize('field,value', [('sha256','sha256:'+'0'*64), ('width',17), ('height',19)])
def test_pinned_layer_identity_at_plan_time(tmp_path, capsys, field, value):
    code = 'SOURCE_DIGEST_MISMATCH' if field == 'sha256' else 'SOURCE_DIMENSION_MISMATCH'
    run_bad_spec(tmp_path, capsys, lambda d: d['source']['layers'][1].__setitem__(field,value), code)


def test_roundtrip_relocation_schemas_and_entire_pipeline(tmp_path, capsys):
    build = build_layers(tmp_path, capsys, tracks=[track('rotate', 8, target='front')])
    plan = load_plan(build / 'plan.json')
    assert normalize_plan(plan) == json.loads((build / 'plan.json').read_text())
    for l in plan.layers:
        assert (plan.spec_dir / l.source_image).resolve().is_file()
        assert l.source_sha256 and l.source_width and l.source_height
    relocated = tmp_path / 'relocated'
    relocated.mkdir()
    shutil.move(tmp_path / 'spec', relocated / 'spec')
    shutil.move(build, relocated / 'build')
    build = relocated / 'build'
    for args in [['render'], ['validate','--write-qa'], ['preview'], ['contact-sheet'], ['report']]:
        assert main([args[0], str(build), *args[1:], '--json']) == 0
        result = parsed(capsys)
    assert result['layer_targets'] == ['back', 'front']
    assert result['source_mode'] == 'layered'
    for file, schema in [('plan.json','animation-plan'),('frame-plan.json','frame-plan'),('render.json','render'),('qa/frames.qa.json','qa')]:
        jsonschema.validate(json.loads((build/file).read_text()), json.loads((REPO_ROOT/'schemas'/f'{schema}.schema.json').read_text()))
    assert (build / 'preview.gif').is_file()
    assert (build / 'contact-sheet.png').is_file()


@pytest.mark.parametrize('change', [
    lambda d: d['source']['layers'].reverse(),
    lambda d: d['source']['layers'][0].__setitem__('anchor', {'type':'bottom_center'}),
    lambda d: d['source']['layers'][0]['position'].__setitem__('x', 5),
    lambda d: d['source']['layers'][0].__setitem__('target', 'renamed'),
    lambda d: d['source']['reference_canvas'].__setitem__('width', 12),
])
def test_changed_layer_semantics_invalidates_old_artifacts(tmp_path, capsys, change):
    build = build_layers(tmp_path, capsys)
    assert render(build) == 0
    parsed(capsys)
    p = build / 'plan.json'
    document = json.loads(p.read_text())
    change(document)
    p.write_text(json.dumps(document))
    assert main(['validate',str(build),'--json']) == 1
    assert 'PLAN_DIGEST_MISMATCH' in {e['code'] for e in parsed(capsys)['errors']}


@pytest.mark.parametrize('change', [
    lambda d: d['source']['layers'].reverse(),
    lambda d: d['source']['layers'][0]['position'].__setitem__('y', 9),
    lambda d: d['frames'][0]['layers'].reverse(),
    lambda d: d['frames'][0]['layers'][0].__setitem__('target','other'),
    lambda d: d['frames'][0]['layers'][0]['translation'].__setitem__('x', True),
    lambda d: d['frames'][0]['global_pose'].__setitem__('opacity',0.1),
    lambda d: d['frames'][0].__delitem__('layers'),
    lambda d: d['frames'][0]['layers'][0].__setitem__('extra',0),
    lambda d: d.__setitem__('frame_plan_version',True),
])
def test_frame_plan_cannot_supply_its_own_expectations(tmp_path, capsys, change):
    build = build_layers(tmp_path, capsys)
    p = build / 'frame-plan.json'
    document = json.loads(p.read_text())
    change(document)
    p.write_text(json.dumps(document))
    assert render(build) == 1
    assert {e['code'] for e in parsed(capsys)['errors']} & {'FRAME_PLAN_STALE','FRAME_PLAN_SOURCE_MISMATCH','UNSUPPORTED_FRAME_PLAN_VERSION'}
    assert not (build / 'frames').exists()


@pytest.mark.parametrize('anchor,position,expected', [
    ({'type':'center'}, (4,4), (3,3)),
    ({'type':'bottom_center'}, (4,4), (3,2)),
    ({'type':'custom','x':0,'y':0}, (4,4), (4,4)),
])
def test_static_positions_different_sizes_and_anchors(tmp_path,capsys,anchor,position,expected):
    path, doc = write_spec(tmp_path)
    layers = doc['source']['layers']
    layers[1]['anchor'], layers[1]['position'] = anchor, {'x':position[0],'y':position[1]}
    build = build_layers(tmp_path,capsys,layers)
    assert render(build) == 0
    parsed(capsys)
    pixels = read_pixels(build)
    blue = {p for p,c in pixels.items() if c == BLUE}
    x,y=expected
    assert blue == {(x,y),(x+1,y),(x,y+1),(x+1,y+1)}
    assert pixels[(2,2)] == (BLUE if (2,2) in blue else RED)
    assert_valid(build,capsys)


def test_local_translation_global_translation_and_static_layer(tmp_path,capsys):
    build = build_layers(tmp_path,capsys, tracks=[
        track('translate_x',1,target='front',curve='triangle',track_id='local'),
        track('translate_y',1,curve='triangle',track_id='global')])
    assert render(build) == 0
    parsed(capsys)
    pixels = read_pixels(build,1)
    # Front starts at (3,3): local +1 x, then global +1 y. Back only moves +1 y.
    assert {p for p,c in pixels.items() if c == BLUE} == {(4,4),(5,4),(4,5),(5,5)}
    assert pixels[(2,3)] == RED
    fp=json.loads((build/'frame-plan.json').read_text())
    assert fp['frames'][1]['offset'] == {'x':0.0,'y':1.0}
    assert fp['frames'][1]['layers'][1]['translation'] == {'x':1.0,'y':0.0}
    assert_valid(build,capsys)


def test_local_and_global_90_degree_rotation_hand_computed(tmp_path,capsys):
    # Source pixel center (1.5,2.5), anchor (2,2), position (4,4).
    # Local CW -> (3.5,3.5); local x+1 -> (4.5,3.5).
    # Global CW around (4,4) -> (4.5,4.5); global y+1 -> (4.5,5.5).
    source=tmp_path/'pixel.png';im=Image.new('RGBA',(4,4));im.putpixel((1,2),RED);im.save(source)
    build=build_layers(tmp_path,capsys,[layer('mark',source)], tracks=[
        track('rotate',60,target='mark',phase=.25,track_id='r1'),
        track('rotate',30,target='mark',phase=.25,track_id='r2'),
        track('translate_x',1,target='mark',phase=.25,track_id='local'),
        track('rotate',90,phase=.25,track_id='global_r'),
        track('translate_y',1,phase=.25,track_id='global_t')])
    assert render(build)==0;parsed(capsys)
    pixels=read_pixels(build)
    assert set(pixels)=={(4,5)}
    assert pixels[(4,5)][3]>=253
    assert_valid(build,capsys)


def test_local_scale_product_bilinear_reference(tmp_path,capsys):
    source=tmp_path/'block.png';im=Image.new('RGBA',(8,8))
    for x in (3,4):
        for y in (3,4):im.putpixel((x,y),RED)
    im.save(source)
    build=build_layers(tmp_path,capsys,[layer('mark',source)],tracks=[
        track('scale',.25,target='mark',curve='linear',phase=.5,track_id='a'),
        track('scale',.6,target='mark',curve='linear',phase=.5,track_id='b')])
    assert render(build)==0;parsed(capsys)
    # Scale 2: inverse sample at output (1.5,1.5) is (2.75,2.75),
    # bilinear support weight .25*.25 -> floor(255/16)=15.
    pixels=read_pixels(build)
    assert pixels[(1,1)] == (255,0,0,15)
    assert pixels[(3,3)] == RED
    assert (0,0) not in pixels
    assert_valid(build,capsys)


@pytest.mark.parametrize('reverse,global_opacity,expected', [
    (False,False,(85,0,170,192)), (True,False,(170,0,85,192)),
    (False,True,(85,0,170,96)),
])
def test_alpha_over_order_and_global_opacity_once(tmp_path,capsys,reverse,global_opacity,expected):
    # a=128/255 over 128/255 -> a_out=192; front RGB weight 2/3.
    # Applying 0.5 globally yields alpha 96; per-layer fading would yield 112.
    sources=[]
    for name,color in [('red',(255,0,0,128)),('blue',(0,0,255,128))]:
        path=tmp_path/f'{name}.png';Image.new('RGBA',(2,2),color).save(path);sources.append(layer(name,path))
    if reverse:sources.reverse()
    build=build_layers(tmp_path,capsys,sources,tracks=[track('opacity',-.5,phase=.25)] if global_opacity else [])
    assert render(build)==0;parsed(capsys)
    assert read_pixels(build)[(3,3)] == expected
    assert_valid(build,capsys)


def test_local_opacity_product(tmp_path,capsys):
    # Front opacity .5*.5=.25 -> alpha64 over opaque red -> (191,0,64,255).
    build=build_layers(tmp_path,capsys,tracks=[track('opacity',-.5,target='front',phase=.25,track_id=str(i)) for i in range(2)])
    assert render(build)==0;parsed(capsys)
    assert read_pixels(build)[(3,3)]==(191,0,64,255)
    assert_valid(build,capsys)


@pytest.mark.parametrize('invisibility', ['opacity','clipping','occlusion','source'])
def test_invisible_layer_is_legal(tmp_path,capsys,invisibility):
    path,doc=write_spec(tmp_path)
    layers=doc['source']['layers'];tracks=[]
    if invisibility=='opacity':tracks=[track('opacity',-1,target='front',phase=.25)]
    elif invisibility=='clipping':layers[1]['position']['x']=100
    elif invisibility=='occlusion':layers.reverse()
    else:Image.new('RGBA',(2,2)).save(path.parent/'front.png')
    build=build_layers(tmp_path,capsys,layers,tracks=tracks)
    assert render(build)==0;parsed(capsys)
    assert set(read_pixels(build).values()) == {RED}
    assert_valid(build,capsys)


def test_intermediate_clipping_precedes_global_transform(tmp_path,capsys):
    path,doc=write_spec(tmp_path)
    layers=doc['source']['layers'];layers[1]['position']['x']=10
    build=build_layers(tmp_path,capsys,layers, tracks=[track('translate_x',-3,phase=.25)])
    assert render(build)==0;parsed(capsys)
    # Fully clipped blue cannot reappear at x=6 after the global shift.
    assert set(read_pixels(build).values()) == {RED}


def test_output_canvas_anchor_alignment(tmp_path,capsys):
    build=build_layers(tmp_path,capsys,canvas={'width':12,'height':16})
    assert render(build)==0;parsed(capsys)
    # Reference center(4,4) aligns to output center(6,8), with no scale.
    assert {p for p,c in read_pixels(build).items() if c==BLUE} == {(5,7),(6,7),(5,8),(6,8)}


def test_all_local_layers_empty_refuses_publication(tmp_path,capsys):
    build=build_layers(tmp_path,capsys,tracks=[track('opacity',-1,target=t,phase=.25,track_id=t) for t in ['front','back']])
    assert render(build)==4
    assert parsed(capsys)['errors'][0]['code']=='RENDERED_FRAME_EMPTY'
    assert not (build/'frames').exists()
    assert not (build/'.render-transaction').exists()


@pytest.mark.parametrize('target', ['front','sprite'])
@pytest.mark.parametrize('motion,amplitudes,code', [
    ('scale',[-1],'INVALID_EFFECTIVE_SCALE'), ('opacity',[-2],'INVALID_EFFECTIVE_OPACITY'),
    ('scale',[1e200,1e200],'NONFINITE_EFFECTIVE_TRANSFORM'),
    ('opacity',[1e200,1e200],'NONFINITE_EFFECTIVE_TRANSFORM'),
    ('rotate',[1e308,1e308],'NONFINITE_EFFECTIVE_TRANSFORM'),
    ('translate_x',[1e308,1e308],'NONFINITE_EFFECTIVE_TRANSFORM'),
    ('scale',[-.999999]*60,'INVALID_EFFECTIVE_SCALE'),
])
def test_composed_numeric_errors(tmp_path,capsys,target,motion,amplitudes,code):
    tracks=[track(motion,a,target=target,curve='linear',phase=.5,track_id=str(i)) for i,a in enumerate(amplitudes)]
    run_bad_spec(tmp_path,capsys,lambda d:d.__setitem__('tracks',tracks),code)


def test_position_plus_local_translation_overflow(tmp_path,capsys):
    def change(d):
        d['source']['layers'][1]['position']['x']=1e308
        d['tracks']=[track('translate_x',1e308,target='front',phase=.25)]
    run_bad_spec(tmp_path,capsys,change,'NONFINITE_EFFECTIVE_TRANSFORM')


def test_local_budget_and_events_remain_explicit(tmp_path,capsys):
    build=build_layers(tmp_path,capsys,tracks=[track('translate_x',100,target='front')],
        constraints={'max_displacement_px':1,'max_frame_delta_px':1},
        events=[{'event_id':'e','type':'blink','target':'back','frames':[0]}])
    assert render(build)==0;parsed(capsys)
    assert_valid(build,capsys)
    assert read_pixels(build)[(2,2)]==RED


@pytest.mark.parametrize('corruption', ['rgb','alpha','order'])
def test_same_silhouette_pixel_corruption(tmp_path,capsys,corruption):
    build=build_layers(tmp_path,capsys)
    assert render(build)==0;parsed(capsys)
    path=build/'frames/frame_000.png'
    with Image.open(path) as im:changed=im.convert('RGBA')
    bbox=changed.getchannel('A').getbbox()
    if corruption=='order':
        # Wrong order: opaque back over front, same outer silhouette.
        for x in range(3,5):
            for y in range(3,5):changed.putpixel((x,y),RED)
    elif corruption=='rgb':changed.putpixel((3,3),(0,255,0,255))
    else:changed.putpixel((3,3),(0,0,255,100))
    assert changed.getchannel('A').getbbox()==bbox
    changed.save(path)
    assert main(['validate',str(build),'--json'])==1
    assert 'FRAME_CONTENT_MISMATCH' in {e['code'] for e in parsed(capsys)['errors']}


def test_modes_repeatability_and_all_source_hashes(tmp_path,capsys):
    build=build_layers(tmp_path,capsys,tracks=[track('rotate',7,target='front',track_id='local'),track('translate_y',1,track_id='global')], reduced_motion={'mode':'hold_first_frame'})
    source_paths=load_build(build).plan.protected_paths()
    before={p:p.read_bytes() for p in source_paths}
    assert render(build)==0;parsed(capsys)
    full=frame_hashes(build)
    assert len(set(full))>1
    assert render(build,'--overwrite')==0;parsed(capsys)
    assert frame_hashes(build)==full
    assert render(build,'--overwrite','--reduced-motion')==0;parsed(capsys)
    assert frame_hashes(build)==[full[0]]*4
    assert_valid(build,capsys)
    assert {p:p.read_bytes() for p in source_paths}==before
    # Full frames cannot be relabeled as held output, or vice versa.
    manifest=build/'render.json';doc=json.loads(manifest.read_text());doc['mode']='full';manifest.write_text(json.dumps(doc))
    assert main(['validate',str(build),'--json'])==1;parsed(capsys)


def test_external_layer_frames_have_geometry_only_contract(tmp_path,capsys):
    build=build_layers(tmp_path,capsys)
    (build/'frames').mkdir()
    # Independent flattened green image with expected outer geometry.
    for i in range(4):
        im=Image.new('RGBA',(8,8))
        for x in range(2,6):
            for y in range(2,6):im.putpixel((x,y),(0,255,0,255))
        im.save(build/'frames'/f'frame_{i:03d}.png')
    assert_valid(build,capsys)
    (build/'.render-transaction').mkdir()
    assert main(['validate',str(build),'--json'])==1
    assert parsed(capsys)['errors'][0]['code']=='RENDER_TRANSACTION_INCOMPLETE'


@pytest.mark.parametrize('source_index',[0,1])
@pytest.mark.parametrize('alias',['symlink','hardlink'])
@pytest.mark.parametrize('slot',['frames/frame_000.png','render.json'])
def test_every_source_alias_protected(tmp_path,capsys,source_index,alias,slot):
    build=build_layers(tmp_path,capsys)
    source=(tmp_path/'spec'/('back.png' if source_index==0 else 'front.png'))
    before=source.read_bytes();target=build/slot;target.parent.mkdir(exist_ok=True)
    if alias=='symlink':target.symlink_to(source)
    else:os.link(source,target)
    assert render(build,'--overwrite')==4
    assert parsed(capsys)['errors'][0]['code']=='FRAMES_DIR_CONFLICT'
    assert source.read_bytes()==before


@pytest.mark.parametrize('source_name',['back.png','front.png','animation.json'])
@pytest.mark.parametrize('slot',['plan.json','frame-plan.json','qa/plan.qa.json'])
def test_plan_publication_protects_images_and_description(tmp_path,capsys,source_name,slot):
    spec,_=write_spec(tmp_path);source=spec.parent/source_name;before=source.read_bytes()
    output=tmp_path/'build';target=output/slot;target.parent.mkdir(parents=True)
    os.link(source,target)
    assert main(['plan','--spec',str(spec),'--output',str(output),'--json'])==4
    assert parsed(capsys)['errors'][0]['code']=='OUTPUT_OVERLAPS_SOURCE'
    assert source.read_bytes()==before


@pytest.mark.parametrize('command',['preview','contact-sheet'])
@pytest.mark.parametrize('source_index',[0,1])
def test_preview_cannot_overwrite_layers(tmp_path,capsys,command,source_index):
    build=build_layers(tmp_path,capsys)
    assert render(build)==0;parsed(capsys)
    source=load_build(build).plan.protected_paths()[source_index+1];before=source.read_bytes()
    assert main([command,str(build),'--output',str(source),'--json'])==4
    assert parsed(capsys)['errors'][0]['code']=='OUTPUT_OVERLAPS_SOURCE'
    assert source.read_bytes()==before


def test_very_large_but_finite_local_translation_is_clipped(tmp_path,capsys):
    build=build_layers(tmp_path,capsys,tracks=[track('translate_x',1e100,target='front',curve='linear',phase=.5)])
    assert render(build)==0;parsed(capsys)
    assert set(read_pixels(build).values())=={RED}
    assert_valid(build,capsys)


@pytest.mark.parametrize('alias',['symlink','hardlink'])
def test_runtime_description_cannot_alias_render_manifest(tmp_path,capsys,alias):
    build=build_layers(tmp_path,capsys)
    source=build/'plan.json';before=source.read_bytes()
    if alias=='symlink':(build/'render.json').symlink_to(source)
    else:os.link(source,build/'render.json')
    assert render(build,'--overwrite')==4
    assert parsed(capsys)['errors'][0]['code']=='FRAMES_DIR_CONFLICT'
    assert source.read_bytes()==before


def test_qa_write_cannot_overwrite_layer(tmp_path,capsys):
    build=build_layers(tmp_path,capsys)
    assert render(build)==0;parsed(capsys)
    source=tmp_path/'spec/front.png';before=source.read_bytes()
    os.link(source,build/'qa/frames.qa.json')
    assert main(['validate',str(build),'--write-qa','--json'])==4
    assert parsed(capsys)['errors'][0]['code']=='OUTPUT_OVERLAPS_SOURCE'
    assert source.read_bytes()==before


def test_example_plan_schema():
    jsonschema.validate(json.loads((REPO_ROOT/'examples/layered-placeholder/animation.json').read_text()),
        json.loads((REPO_ROOT/'schemas/animation-plan.schema.json').read_text()))
