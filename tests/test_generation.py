"""M4 contracts and independently drawn source-space pixel oracles."""
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys

import jsonschema
import pytest
from PIL import Image, PngImagePlugin

from sprite_harness.build import create_build, load_build, validate_build
from sprite_harness.cli import main
from sprite_harness.contracts import ContractViolation, byte_digest, digest, read_json
from sprite_harness.generation import derive_seed, generate_build, load_generation, normalize_request
from sprite_harness.plan import load_plan
from sprite_harness.render import render_build
from test_render import parsed, track, nonzero_pixels

ROOT = Path(__file__).resolve().parents[1]
ADAPTER = [sys.executable, str(ROOT / 'scripts/offline_test_adapter.py')]


def fixture_build(tmp_path, *, layered=False, tracks=None, frame_count=4, name='build', seed=17, size=(8, 8)):
    spec_dir = tmp_path / (name + '-sources')
    spec_dir.mkdir(parents=True)
    image = Image.new('RGBA', (4, 4))
    image.putpixel((0, 0), (255, 0, 0, 255))
    image.save(spec_dir / 'source.png')
    doc = {'plan_version': 2 if layered else 1, 'animation_id': 'geometry', 'seed': seed,
           'canvas': {'width': size[0], 'height': size[1], 'background': 'transparent'},
           'anchor': {'type': 'center'}, 'playback': {'fps': 8, 'loop': True, 'frame_count': frame_count},
           'tracks': tracks or [], 'reduced_motion': {'mode': 'hold_first_frame'}}
    if layered:
        Image.new('RGBA', (2, 2), (255, 0, 0, 128)).save(spec_dir / 'back.png')
        doc['source'] = {'reference_canvas': {'width': size[0], 'height': size[1]}, 'layers': [
            {'target': 'back', 'image': 'back.png', 'anchor': {'type': 'center'}, 'position': {'x': 4, 'y': 4}},
            {'target': 'mark', 'image': 'source.png', 'anchor': {'type': 'center'}, 'position': {'x': 4, 'y': 4}}]}
    else:
        doc['source'] = {'image': 'source.png'}
    path = spec_dir / 'animation.json'
    path.write_text(json.dumps(doc))
    result = create_build(load_plan(path), tmp_path / name)
    assert result['success'], result
    return tmp_path / name


def generation_spec(tmp_path, target='sprite', frames=None, name='generation.json'):
    doc = {'generation_version': 1, 'request_id': 'demo',
           'adapter': {'id': 'offline-test', 'version': '1', 'model': 'geometry-test-substitute', 'parameters': {}, 'seed_policy': 'required'},
           'requests': [{'id': 'shape', 'target': target, 'frames': frames if frames is not None else [1, 2], 'instruction': 'Draw a geometric square for testing.'}]}
    path = tmp_path / name
    path.write_text(json.dumps(doc))
    return path, doc


def generated(tmp_path, *, layered=False, frames=None, tracks=None):
    path = fixture_build(tmp_path, layered=layered, tracks=tracks)
    spec, _ = generation_spec(tmp_path, 'mark' if layered else 'sprite', frames)
    assert generate_build(load_build(path), spec, ADAPTER)['success']
    return path, spec


@pytest.mark.parametrize('layered', [False, True])
def test_source_replacement_oracle_and_offline_replay(tmp_path, monkeypatch, layered):
    path, spec = generated(tmp_path, layered=layered,
                           tracks=[track('translate_x', 1, curve='triangle')])
    build = load_build(path)
    before = {p: p.read_bytes() for p in build.protected_paths}
    import sprite_harness.generation as gen
    monkeypatch.setattr(gen, 'run_adapter', lambda *a, **k: pytest.fail('offline render/validation called adapter'))
    assert render_build(build, generated_input=True)['success']
    pixels = nonzero_pixels(path / 'frames/frame_001.png')
    # Replacement square in 4x4 source is (1,1)..(2,2), centered at (4,4),
    # then global +1 x -> (4,3)..(5,4). Back alpha128 -> composed alpha224.
    # Green = round(180*192 / (192 + 128*63/255)) = 155.
    alpha = 224 if layered else 192
    expected = (70, 155, 206, alpha) if layered else (40, 180, 240, alpha)
    assert set(pixels) == {(4, 3), (5, 3), (4, 4), (5, 4)}
    assert set(pixels.values()) == {expected}
    assert nonzero_pixels(path / 'frames/frame_000.png')[(2, 2)] == (255, 0, 0, 255)
    assert validate_build(build)[0].valid
    frames_before = [p.read_bytes() for p in sorted((path / 'frames').iterdir())]
    assert render_build(build, generated_input=True, overwrite=True)['success']
    assert frames_before == [p.read_bytes() for p in sorted((path / 'frames').iterdir())]
    assert before == {p: p.read_bytes() for p in before}


def test_replacement_then_local_global_translation_opacity_once(tmp_path):
    tracks = [track('translate_x', 1, target='mark', curve='triangle', track_id='local'),
              track('translate_y', 1, curve='triangle', track_id='global'),
              track('opacity', -.5, curve='triangle', track_id='fade')]
    path, _ = generated(tmp_path, layered=True, tracks=tracks)
    assert render_build(load_build(path), generated_input=True)['success']
    pixels = nonzero_pixels(path / 'frames/frame_001.png')
    # Candidate x=4,5; global y=4,5; local square overlaps only back column x4.
    assert pixels[(5, 4)] == (40, 180, 240, 96)
    assert pixels[(4, 4)] == (70, 155, 206, 112)
    assert pixels[(3, 4)] == (255, 0, 0, 64)
    assert validate_build(load_build(path))[0].valid


@pytest.mark.parametrize('frames', [[1, 2], [0, 3]])
def test_hold_freezes_actual_frame_zero_mapping(tmp_path, frames):
    path, _ = generated(tmp_path, frames=frames)
    build = load_build(path)
    render_build(build, generated_input=True)
    first = (path / 'frames/frame_000.png').read_bytes()
    render_build(build, generated_input=True, overwrite=True, reduced_motion=True)
    assert all(p.read_bytes() == first for p in (path / 'frames').iterdir())
    assert validate_build(build)[0].valid


@pytest.mark.parametrize('change,code', [
    (lambda d: d.__setitem__('generation_version', True), 'MALFORMED_SPEC'),
    (lambda d: d.__setitem__('generation_version', 1.0), 'MALFORMED_SPEC'),
    (lambda d: d.__setitem__('generation_version', 2), 'MALFORMED_SPEC'),
    (lambda d: d.__setitem__('extra', 1), 'MALFORMED_SPEC'),
    (lambda d: d['adapter']['parameters'].__setitem__('value', float('inf')), 'MALFORMED_SPEC'),
    (lambda d: d['requests'][0].__setitem__('frames', [True]), 'MALFORMED_SPEC'),
    (lambda d: d['requests'][0].__setitem__('frames', [1, 1]), 'MALFORMED_SPEC'),
    (lambda d: d['requests'][0].__setitem__('frames', [9]), 'GENERATION_FRAME_OUT_OF_RANGE'),
    (lambda d: d['requests'][0].__setitem__('target', 'new'), 'UNKNOWN_GENERATION_TARGET'),
    (lambda d: d['requests'].append(copy.deepcopy(d['requests'][0])), 'DUPLICATE_GENERATION_REQUEST'),
    (lambda d: d['requests'].append({**d['requests'][0], 'id': 'other'}), 'GENERATION_MAPPING_OVERLAP'),
])
def test_spec_rejections(tmp_path, capsys, change, code):
    build = fixture_build(tmp_path)
    path, doc = generation_spec(tmp_path)
    change(doc); path.write_text(json.dumps(doc))
    actual = main(['generate', str(build), '--spec', str(path), '--adapter-argv', json.dumps(ADAPTER), '--json'])
    assert actual == (2 if code == 'MALFORMED_SPEC' else 1)
    assert parsed(capsys)['errors'][0]['code'] == code
    assert not (build / 'generation').exists()


def test_layered_sprite_is_not_a_replaceable_layer(tmp_path):
    build = fixture_build(tmp_path, layered=True)
    path, _ = generation_spec(tmp_path, 'sprite')
    with pytest.raises(ContractViolation, match='Replacement target'):
        generate_build(load_build(build), path, ADAPTER)


def test_seed_derivation_and_binding(tmp_path):
    build = load_build(fixture_build(tmp_path))
    path, _ = generation_spec(tmp_path)
    request = normalize_request(build, path, build.build_dir / 'generation')
    expected = int.from_bytes(hashlib.sha256(b'["sprite-harness-generation-v1",17,"demo","shape","sprite",[1,2]]').digest()[:8], 'big')
    assert request['items'][0]['seed'] == expected == derive_seed(17, 'demo', 'shape', 'sprite', [2, 1])
    assert derive_seed(18, 'demo', 'shape', 'sprite', [1, 2]) != expected
    changed = copy.deepcopy(request); changed['seed'] += 1
    assert digest(request) != digest(changed)


@pytest.mark.parametrize('file', ['spec.json', 'request.json', 'response.json', 'accepted.json', 'inputs/shape.png', 'references/shape.png', 'generation.qa.json'])
def test_frozen_input_tampering_fails_offline(tmp_path, file):
    path, _ = generated(tmp_path)
    render_build(load_build(path), generated_input=True)
    target = path / 'generation' / file
    if file.endswith('.png'):
        with Image.open(target) as im:
            changed = im.convert('RGBA')
        changed.putpixel((1, 1), (1, 2, 3, 4)); changed.save(target)
    else:
        data = json.loads(target.read_text()); data['extra'] = True; target.write_text(json.dumps(data))
    assert not validate_build(load_build(path))[0].valid


@pytest.mark.parametrize('what', ['spec', 'source', 'plan_seed', 'mapping'])
def test_original_input_changes_invalidate_generated_render(tmp_path, what):
    path, spec = generated(tmp_path)
    build = load_build(path)
    render_build(build, generated_input=True)
    if what in ('spec', 'mapping'):
        doc = json.loads(spec.read_text())
        if what == 'spec': doc['requests'][0]['instruction'] += ' changed'
        else: doc['requests'][0]['frames'] = [0]
        spec.write_text(json.dumps(doc))
    elif what == 'source':
        Image.new('RGBA', (4, 4), (1, 2, 3, 4)).save(build.plan.resolved_source_path())
    else:
        p = path / 'plan.json'; doc = json.loads(p.read_text()); doc['seed'] += 1; p.write_text(json.dumps(doc))
    assert not validate_build(load_build(path))[0].valid


@pytest.mark.parametrize('pixel', [(0, 255, 0, 192), (40, 180, 240, 16)])
def test_generated_same_bbox_pixel_tamper_fails(tmp_path, pixel):
    path, _ = generated(tmp_path)
    render_build(load_build(path), generated_input=True)
    p = path / 'frames/frame_001.png'
    with Image.open(p) as im: changed = im.convert('RGBA')
    before = changed.getchannel('A').getbbox()
    changed.putpixel((3, 3), pixel); changed.save(p)
    assert changed.getchannel('A').getbbox() == before
    assert 'FRAME_CONTENT_MISMATCH' in {e.code for e in validate_build(load_build(path))[0].errors}


def test_generation_bundle_relocation(tmp_path):
    parent = tmp_path / 'parent'; parent.mkdir()
    path, _ = generated(parent)
    render_build(load_build(path), generated_input=True)
    moved = tmp_path / 'moved'; shutil.move(parent, moved)
    assert validate_build(load_build(moved / 'build'))[0].valid


def test_all_m4_artifacts_match_schemas(tmp_path):
    path, _ = generated(tmp_path)
    render_build(load_build(path), generated_input=True)
    for file, schema in [('spec.json', 'generation-spec'), ('request.json', 'generation-request'),
                         ('response.json', 'generation-response'), ('accepted.json', 'generated-inputs'),
                         ('generation.qa.json', 'qa')]:
        jsonschema.validate(json.loads((path/'generation'/file).read_text()), json.loads((ROOT/'schemas'/f'{schema}.schema.json').read_text()))
    jsonschema.validate(json.loads((path/'render.json').read_text()), json.loads((ROOT/'schemas/render.schema.json').read_text()))


@pytest.mark.parametrize('mutation', ['missing', 'duplicate', 'identity', 'path', 'dimension', 'alpha', 'invalid_png', 'seed', 'version', 'unknown'])
def test_untrusted_adapter_response_rejected(tmp_path, monkeypatch, mutation):
    import sprite_harness.generation as gen
    path = fixture_build(tmp_path)
    spec, _ = generation_spec(tmp_path)
    real = gen.run_adapter
    def corrupt(argv, req, response, output, timeout):
        real(argv, req, response, output, timeout)
        doc = json.loads(response.read_text())
        if mutation == 'missing': doc['results'] = []
        elif mutation == 'duplicate': doc['results'] *= 2
        elif mutation == 'identity': doc['request_digest'] = 'sha256:' + '0'*64
        elif mutation == 'path': doc['results'][0]['file'] = '../source.png'
        elif mutation == 'dimension': doc['results'][0]['width'] += 1
        elif mutation == 'seed': doc['seed_supported'] = False
        elif mutation == 'version': doc['response_version'] = True
        elif mutation == 'unknown': doc['surprise'] = 1
        else:
            image_path = output / doc['results'][0]['file']
            if mutation == 'alpha': Image.new('RGB', (4, 4)).save(image_path)
            else: image_path.write_bytes(b'not png')
            doc['results'][0]['sha256'] = byte_digest(image_path.read_bytes())
        response.write_text(json.dumps(doc))
    monkeypatch.setattr(gen, 'run_adapter', corrupt)
    with pytest.raises(Exception): generate_build(load_build(path), spec, ADAPTER)
    assert not (path / 'generation').exists()
    assert not (path / '.generation-transaction').exists()


def test_adapter_timeout_redacts_output_and_cleans_transaction(tmp_path, capsys):
    path = fixture_build(tmp_path)
    spec, _ = generation_spec(tmp_path)
    command = [sys.executable, '-c', 'import time; print("secret-canary"); time.sleep(30)']
    assert main(['generate', str(path), '--spec', str(spec), '--adapter-argv', json.dumps(command), '--timeout', '.05', '--json']) == 4
    payload = parsed(capsys)
    assert payload['errors'][0]['code'] == 'ADAPTER_TIMEOUT'
    assert 'secret-canary' not in json.dumps(payload)
    assert not (path / '.generation-transaction').exists()


def test_candidate_order_does_not_define_mapping(tmp_path):
    path = fixture_build(tmp_path)
    spec, doc = generation_spec(tmp_path, frames=[2])
    doc['requests'].append({**doc['requests'][0], 'id': 'second', 'frames': [0]})
    spec.write_text(json.dumps(doc))
    generate_build(load_build(path), spec, ADAPTER)
    request = read_json(path/'generation/request.json')
    response = read_json(path/'generation/response.json')
    assert [r['id'] for r in response['results']] == ['second', 'shape']
    assert [r['id'] for r in request['items']] == ['shape', 'second']
    images, _ = load_generation(load_build(path))
    assert set(images) == {('sprite', 2), ('sprite', 0)}


@pytest.mark.parametrize('schema,file,version', [('generation-request','request.json','request_version'),
                                               ('generation-response','response.json','response_version'),
                                               ('generated-inputs','accepted.json','accepted_version')])
@pytest.mark.parametrize('bad',[True,False,1.0,'1',2,None])
def test_all_protocol_versions_are_strict(tmp_path,schema,file,version,bad):
    from sprite_harness.contracts import check_schema
    from sprite_harness.spec import SpecLoadError
    path,_=generated(tmp_path)
    document=read_json(path/'generation'/file);document[version]=bad
    with pytest.raises(SpecLoadError):check_schema(document,schema)


@pytest.mark.parametrize('file',['back.png','source.png'])
def test_all_original_layers_remain_required_for_generated_build(tmp_path,file):
    path,_=generated(tmp_path,layered=True);render_build(load_build(path),generated_input=True)
    (tmp_path/'build-sources'/file).write_bytes(b'changed')
    assert not validate_build(load_build(path))[0].valid


def test_replacement_rotation_oracle(tmp_path):
    path,_=generated(tmp_path,frames=[0],tracks=[track('rotate',90,phase=.25)])
    render_build(load_build(path),generated_input=True)
    # Centered 2x2 candidate remains centered after a 90 degree turn.
    assert set(nonzero_pixels(path/'frames/frame_000.png'))=={(3,3),(3,4),(4,3),(4,4)}
    assert validate_build(load_build(path))[0].valid


def test_missing_seed_and_explicit_generation_required(tmp_path,capsys):
    path=fixture_build(tmp_path)
    plan=path/'plan.json';doc=read_json(plan);doc.pop('seed');plan.write_text(json.dumps(doc))
    from sprite_harness.expand import normalize_plan,expand_plan
    loaded=load_plan(plan);(path/'frame-plan.json').write_text(json.dumps(expand_plan(loaded,normalize_plan(loaded))))
    spec,_=generation_spec(tmp_path)
    assert main(['generate',str(path),'--spec',str(spec),'--adapter-argv',json.dumps(ADAPTER),'--json'])==1
    assert parsed(capsys)['errors'][0]['code']=='GENERATION_SEED_REQUIRED'
    assert main(['render',str(path),'--json'])==0;parsed(capsys)
    assert main(['render',str(path),'--generated-input','--overwrite','--json'])==3;parsed(capsys)


@pytest.mark.parametrize('attack',['directory','symlink','hardlink','oversized','request_change','collision'])
def test_adapter_filesystem_boundary(tmp_path,monkeypatch,attack):
    import sprite_harness.generation as gen
    path=fixture_build(tmp_path);spec,_=generation_spec(tmp_path)
    real=gen.run_adapter
    def corrupt(argv,req,response,output,timeout):
        real(argv,req,response,output,timeout)
        doc=read_json(response);candidate=output/doc['results'][0]['file']
        if attack=='request_change':req.write_text(req.read_text()+'\n')
        elif attack=='collision':(output/'unrequested.png').write_bytes(candidate.read_bytes())
        else:
            candidate.unlink()
            source=path.parent/'build-sources/source.png'
            if attack=='directory':candidate.mkdir()
            elif attack=='symlink':candidate.symlink_to(source)
            elif attack=='hardlink':os.link(source,candidate)
            else:
                with candidate.open('wb') as stream:stream.truncate(gen.MAX_IMAGE_BYTES+1)
    monkeypatch.setattr(gen,'run_adapter',corrupt)
    with pytest.raises(Exception):generate_build(load_build(path),spec,ADAPTER)
    assert not (path/'generation').exists()


def test_generated_manifest_binding_and_missing_manifest(tmp_path):
    path,_=generated(tmp_path);render_build(load_build(path),generated_input=True)
    manifest=path/'render.json';doc=read_json(manifest);doc['generation']['accepted_digest']='sha256:'+'0'*64;manifest.write_text(json.dumps(doc))
    assert 'RENDER_GENERATION_STALE' in {e.code for e in validate_build(load_build(path))[0].errors}
    manifest.unlink()
    assert 'GENERATED_RENDER_MANIFEST_REQUIRED' in {e.code for e in validate_build(load_build(path))[0].errors}


@pytest.mark.parametrize('layered',[False,True])
def test_empty_generated_local_layer_legal_but_final_empty_frame_fails(tmp_path,monkeypatch,layered):
    import sprite_harness.generation as gen
    from sprite_harness.processing import ProcessingError
    path=fixture_build(tmp_path,layered=layered)
    spec,_=generation_spec(tmp_path,'mark' if layered else 'sprite',[0])
    real=gen.run_adapter
    def blank(argv,req,response,output,timeout):
        real(argv,req,response,output,timeout)
        doc=read_json(response);p=output/doc['results'][0]['file'];Image.new('RGBA',(4,4)).save(p)
        doc['results'][0]['sha256']=byte_digest(p.read_bytes());response.write_text(json.dumps(doc))
    monkeypatch.setattr(gen,'run_adapter',blank)
    generate_build(load_build(path),spec,ADAPTER)
    if layered:
        render_build(load_build(path),generated_input=True)
        assert validate_build(load_build(path))[0].valid
        assert set(nonzero_pixels(path/'frames/frame_000.png').values())=={(255,0,0,128)}
    else:
        with pytest.raises(ProcessingError) as exc:render_build(load_build(path),generated_input=True)
        assert exc.value.code=='RENDERED_FRAME_EMPTY'
        assert not (path/'frames').exists()


def test_fast_oversized_adapter_response_has_stable_error(tmp_path,capsys):
    path=fixture_build(tmp_path);spec,_=generation_spec(tmp_path)
    code='import sys; from pathlib import Path; p=Path(sys.argv[sys.argv.index("--response")+1]); p.write_bytes(b"x"*(4*1024*1024+1))'
    argv=[sys.executable,'-c',code]
    assert main(['generate',str(path),'--spec',str(spec),'--adapter-argv',json.dumps(argv),'--json'])==4
    assert parsed(capsys)['errors'][0]['code']=='ADAPTER_RESPONSE_TOO_LARGE'
