"""Shared transaction failure gates; original render safety tests remain intact."""
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

from sprite_harness.atlas import export_atlas, export_marker, validate_export
from sprite_harness.build import load_build, validate_build
from sprite_harness.cli import main
from sprite_harness.contracts import ContractViolation
from sprite_harness.generation import generate_build
from sprite_harness.processing import ProcessingError
from sprite_harness.render import render_build
from test_generation import ADAPTER, ROOT, fixture_build, generated, generation_spec
from test_atlas import exported, export_spec
from test_render import parsed


def setup_case(tmp_path, kind):
    if kind == 'GENERATION':
        build, spec = generated(tmp_path)
        output = build/'generation';marker=build/'.generation-transaction'
        action=lambda: generate_build(load_build(build),spec,ADAPTER,overwrite=True)
        validate=lambda: validate_build(load_build(build))[0].valid
        inputs=[*load_build(build).plan.protected_paths(),spec,build/'frame-plan.json']
    else:
        build,spec,output=exported(tmp_path)
        marker=export_marker(output)
        action=lambda: export_atlas(spec,output,overwrite=True)
        validate=lambda: validate_export(output)['valid']
        inputs=[*load_build(build).protected_paths,spec,build/'render.json',build/'frames/frame_000.png']
    return build,output,marker,action,validate,inputs


def bytes_tree(root):
    return {p.relative_to(root).as_posix():p.read_bytes() for p in root.rglob('*') if p.is_file()}


@pytest.mark.parametrize('kind',['GENERATION','EXPORT'])
@pytest.mark.parametrize('step',[1,2])
def test_each_directory_publication_failure_rolls_back(tmp_path,monkeypatch,kind,step):
    import sprite_harness.transactions as tx
    build,out,marker,action,validate,_=setup_case(tmp_path,kind)
    before=bytes_tree(out);real=tx.os.replace;calls=[]
    def replace(src,dst):
        calls.append(1)
        if len(calls)==step:raise OSError('injected publish error')
        return real(src,dst)
    with monkeypatch.context() as patch:
        patch.setattr(tx.os,'replace',replace)
        with pytest.raises(OSError):action()
    assert bytes_tree(out)==before
    assert not marker.exists()
    assert validate()


@pytest.mark.parametrize('kind',['GENERATION','EXPORT'])
def test_rollback_failure_preserves_backup_and_marker(tmp_path,monkeypatch,kind):
    import sprite_harness.transactions as tx
    build,out,marker,action,validate,_=setup_case(tmp_path,kind)
    before=bytes_tree(out);real=tx.os.replace;calls=[]
    def replace(src,dst):
        calls.append(1)
        if len(calls)>=2:raise OSError('disk unavailable')
        return real(src,dst)
    with monkeypatch.context() as patch:
        patch.setattr(tx.os,'replace',replace)
        with pytest.raises(ProcessingError) as exc:action()
    assert exc.value.code==kind+'_RECOVERY_REQUIRED'
    assert marker.exists() and bytes_tree(marker/'previous')==before
    if kind=='GENERATION':assert not validate()
    else:
        with pytest.raises(ContractViolation):validate()
    with pytest.raises(Exception):action()


@pytest.mark.parametrize('kind',['GENERATION','EXPORT'])
def test_cleanup_failure_blocks_consumers(tmp_path,monkeypatch,kind):
    import sprite_harness.transactions as tx
    build,out,marker,action,validate,_=setup_case(tmp_path,kind)
    def fail(*a,**k):raise OSError('cleanup unavailable')
    with monkeypatch.context() as patch:
        patch.setattr(tx.shutil,'rmtree',fail)
        with pytest.raises(ProcessingError):action()
    assert marker.exists()
    if kind=='GENERATION':assert not validate()
    else:
        with pytest.raises(ContractViolation):validate()


@pytest.mark.parametrize('kind',['GENERATION','EXPORT'])
def test_unknown_files_and_directories_are_preserved(tmp_path,kind):
    _,out,_,action,_,_=setup_case(tmp_path,kind)
    (out/'notes').mkdir();(out/'notes/precious.txt').write_text('keep')
    before=bytes_tree(out)
    with pytest.raises(ProcessingError):action()
    assert bytes_tree(out)==before


@pytest.mark.parametrize('kind',['GENERATION','EXPORT'])
@pytest.mark.parametrize('alias',['symlink','dangling','hardlink'])
def test_output_aliases_preserve_every_input(tmp_path,kind,alias):
    _,out,_,action,_,inputs=setup_case(tmp_path,kind)
    source=inputs[-1];before=source.read_bytes()
    target=out/('inputs/shape.png' if kind=='GENERATION' else 'atlas.png')
    target.unlink()
    if alias=='hardlink':os.link(source,target)
    else:target.symlink_to(source if alias=='symlink' else tmp_path/'missing')
    with pytest.raises(Exception):action()
    assert source.read_bytes()==before


@pytest.mark.parametrize('kind',['GENERATION','EXPORT'])
def test_input_change_during_staging_cancels_publication(tmp_path,monkeypatch,kind):
    build,out,_,action,_,inputs=setup_case(tmp_path,kind)
    before=bytes_tree(out);source=inputs[-1]
    if kind=='GENERATION':
        import sprite_harness.generation as module
        real=module.run_adapter
        def change(*a,**k):
            result=real(*a,**k);source.write_bytes(source.read_bytes()+b'\n');return result
        monkeypatch.setattr(module,'run_adapter',change)
    else:
        import sprite_harness.atlas as module
        real=module.round_trip
        def change(*a,**k):
            result=real(*a,**k);source.write_bytes(source.read_bytes()+b'\n');return result
        monkeypatch.setattr(module,'round_trip',change)
    with pytest.raises(ContractViolation) as exc:action()
    assert exc.value.code=='INPUT_CHANGED'
    assert bytes_tree(out)==before


@pytest.mark.parametrize('kind',['GENERATION','EXPORT'])
def test_concurrent_reader_writer_observe_lock(tmp_path,monkeypatch,kind):
    build,out,marker,action,validate,_=setup_case(tmp_path,kind)
    import sprite_harness.transactions as tx
    real=tx.publish_directory;observed=[]
    def publish(*a,**k):
        observed.append(marker.exists())
        with pytest.raises(Exception):action()
        if kind=='GENERATION':
            assert not validate()
            with pytest.raises(ProcessingError):render_build(load_build(build),overwrite=True)
        else:
            with pytest.raises(ContractViolation):validate()
        return real(*a,**k)
    module=__import__('sprite_harness.generation' if kind=='GENERATION' else 'sprite_harness.atlas',fromlist=['x'])
    monkeypatch.setattr(module,'publish_directory',publish)
    action()
    assert observed==[True] and validate()


@pytest.mark.parametrize('kind',['GENERATION','EXPORT'])
@pytest.mark.parametrize('step',[1,2])
def test_forced_process_exit_retains_recovery(tmp_path,capsys,kind,step):
    build,out,marker,_,_,_=setup_case(tmp_path,kind)
    spec=tmp_path/('generation.json' if kind=='GENERATION' else 'export.json')
    program='''
import os,sys,json
from pathlib import Path
import sprite_harness.transactions as tx
from sprite_harness.build import load_build
from sprite_harness.generation import generate_build
from sprite_harness.atlas import export_atlas
real=tx.os.replace
calls=0
def replace(src,dst):
 global calls
 real(src,dst)
 calls+=1
 if calls==int(sys.argv[5]):os._exit(77)
tx.os.replace=replace
if sys.argv[1]=='GENERATION':generate_build(load_build(sys.argv[2]),Path(sys.argv[3]),json.loads(sys.argv[6]),overwrite=True)
else:export_atlas(Path(sys.argv[3]),Path(sys.argv[4]),overwrite=True)
'''
    proc=subprocess.run([sys.executable,'-c',program,kind,str(build),str(spec),str(out),str(step),json.dumps(ADAPTER)],
                        env={**os.environ,'PYTHONPATH':str(ROOT/'src')},capture_output=True,timeout=15)
    assert proc.returncode==77,proc.stderr
    assert marker.exists()
    for command in (['validate','preview','contact-sheet','report'] if kind=='GENERATION' else ['validate-export','report']):
        assert main([command,str(build if kind=='GENERATION' else out),'--json'])==1
        parsed(capsys)


@pytest.mark.parametrize('command',['preview','contact-sheet'])
@pytest.mark.parametrize('file',['generation/spec.json','generation/request.json','generation/inputs/shape.png','render.json','frames/frame_001.png'])
def test_preview_protects_all_frozen_inputs_and_manifests(tmp_path,capsys,command,file):
    build,_=generated(tmp_path);render_build(load_build(build),generated_input=True)
    source=build/file;before=source.read_bytes()
    alias=tmp_path/'alias';os.link(source,alias)
    assert main([command,str(build),'--output',str(alias),'--json'])==4
    parsed(capsys)
    assert source.read_bytes()==before


@pytest.mark.parametrize('kind',['GENERATION','EXPORT'])
def test_initial_publication_failure_has_no_partial_product(tmp_path,monkeypatch,kind):
    import sprite_harness.transactions as tx
    build=fixture_build(tmp_path)
    if kind=='GENERATION':
        spec,_=generation_spec(tmp_path);out=build/'generation'
        action=lambda:generate_build(load_build(build),spec,ADAPTER)
    else:
        render_build(load_build(build));spec,_=export_spec(tmp_path,[build]);out=tmp_path/'atlas'
        action=lambda:export_atlas(spec,out)
    def fail(*a,**k):raise OSError('publish failed')
    monkeypatch.setattr(tx.os,'replace',fail)
    with pytest.raises(OSError):action()
    assert not out.exists()


@pytest.mark.parametrize('kind',['GENERATION','EXPORT'])
def test_staging_failure_keeps_previous_complete_output(tmp_path,monkeypatch,kind):
    _,out,marker,action,validate,_=setup_case(tmp_path,kind)
    before=bytes_tree(out)
    module=__import__('sprite_harness.generation' if kind=='GENERATION' else 'sprite_harness.atlas',fromlist=['x'])
    def fail(*a,**k):raise OSError('write failed')
    with monkeypatch.context() as patch:
        patch.setattr(module,'write_json_artifact',fail)
        with pytest.raises(OSError):action()
    assert bytes_tree(out)==before and not marker.exists() and validate()


def test_export_output_cannot_contain_input_build(tmp_path):
    build=fixture_build(tmp_path);render_build(load_build(build));spec,_=export_spec(tmp_path,[build])
    with pytest.raises(ProcessingError) as exc:export_atlas(spec,tmp_path,overwrite=True)
    assert exc.value.code=='OUTPUT_OVERLAPS_SOURCE'


def test_generation_output_cannot_contain_original_spec(tmp_path):
    build=fixture_build(tmp_path);(build/'generation').mkdir()
    spec,_=generation_spec(build/'generation')
    with pytest.raises(Exception):generate_build(load_build(build),spec,ADAPTER,overwrite=True)
    assert spec.is_file()
