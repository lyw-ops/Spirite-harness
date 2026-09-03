"""Installed 0.7.0 CLI acceptance outside the repository; full logs, no live API."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from PIL import Image, PngImagePlugin


def strict(text):
    def reject(token):raise ValueError('Nonfinite JSON token: '+token)
    def pairs(entries):
        result={}
        for key,value in entries:
            if key in result:raise ValueError('Duplicate key')
            result[key]=value
        return result
    return json.loads(text,parse_constant=reject,object_pairs_hook=pairs)


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def tree(path):return {p.relative_to(path).as_posix():sha(p) for p in path.rglob('*') if p.is_file()}


def main(output):
    repo=Path(__file__).resolve().parents[1];output=output.resolve()
    if output.exists():raise SystemExit('Choose a fresh output directory.')
    cli=Path(sys.executable).parent/'sprite-harness'
    provider=Path(sys.executable).parent/'sprite-openai-adapter'
    env=dict(os.environ);env.pop('PYTHONPATH',None);env.pop('OPENAI_API_KEY',None)
    records=[]
    with tempfile.TemporaryDirectory(prefix='sprite-m4-m5-cli-') as work:
        def run(argv,expected=0,as_json=False):
            proc=subprocess.run([str(a) for a in argv],cwd=work,env=env,capture_output=True,text=True,timeout=60)
            record={'argv':[str(a) for a in argv],'cwd':work,'expected_exit':expected,'actual_exit':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr}
            records.append(record)
            if output.exists():(output/'commands.json').write_text(json.dumps(records,indent=2,allow_nan=False)+'\n')
            assert proc.returncode==expected,record
            return strict(proc.stdout) if as_json else proc.stdout.strip()
        def command(*argv,expected=0):return run([cli,*argv,'--json'],expected,True)
        identity=run([sys.executable,'-c','import sprite_harness,importlib.metadata,json;print(json.dumps({"runtime":sprite_harness.__version__,"distribution":importlib.metadata.version("sprite-animation-harness"),"module":sprite_harness.__file__,"provider_distribution":importlib.metadata.version("sprite-openai-adapter")}))'],as_json=True)
        assert identity['runtime']==identity['distribution']=='0.7.0' and 'site-packages' in identity['module'],identity
        assert run([cli,'--version'])=='0.7.0'
        run([sys.executable,repo/'scripts/create_m4_m5_example.py',output])
        sources=[p for kind in ['single','layered','generated'] for p in (output/kind).rglob('*') if p.is_file()]
        originals={str(p):sha(p) for p in sources}
        adapter=json.dumps([sys.executable,str(repo/'scripts/offline_test_adapter.py')])
        pipelines={};all_exports={};built={}
        for kind in ('single','layered','generated'):
            root=output/kind;generated_args=['--generated-input'] if kind=='generated' else []
            for mode in ('full','hold'):
                build=root/f'build-{mode}'
                command('plan','--spec',root/'animation.json','--output',build)
                if kind=='generated':command('generate',build,'--spec',root/'generation.json','--adapter-argv',adapter)
                rendered=command('render',build,*generated_args,*(['--reduced-motion'] if mode=='hold' else []))
                assert rendered['backend']==('generated-input' if kind=='generated' else 'deterministic')
                assert rendered['mode']==('full' if mode=='full' else 'hold_first_frame')
                frame_bytes=[p.read_bytes() for p in sorted((build/'frames').iterdir())]
                assert len(set(frame_bytes))==(1 if mode=='hold' else 12)
                if mode=='hold':assert frame_bytes==[(root/'build-full/frames/frame_000.png').read_bytes()]*12
                command('validate',build,'--write-qa');command('preview',build);command('contact-sheet',build)
                assert command('report',build)['validation']['valid']
                spec=root/f'export-{mode}.json'
                spec.write_text(json.dumps({'export_version':1,'clips':[{'id':kind,'build':build.name}],
                                           'grid':{'cell_width':192,'cell_height':208,'columns':8,'padding':8}},indent=2)+'\n')
                atlas=root/f'atlas-{mode}'
                command('export','--spec',spec,'--output',atlas)
                assert command('validate-export',atlas)['frame_count']==12
                command('report',atlas)
                before=tree(atlas);command('export','--spec',spec,'--output',atlas,'--overwrite');assert tree(atlas)==before
                if kind=='generated':
                    frozen=tree(build/'generation')
                    command('render',build,*generated_args,*(['--reduced-motion'] if mode=='hold' else []),'--overwrite')
                    assert frame_bytes==[p.read_bytes() for p in sorted((build/'frames').iterdir())]
                    assert tree(build/'generation')==frozen
                built[kind,mode]=build;all_exports[kind,mode]=atlas
                pipelines[f'{kind}-{mode}']={'build':str(build),'atlas':str(atlas),'frames':12,'mode':rendered['mode'],'backend':rendered['backend']}
        # Fixed multi-clip grid: explicit non-alphabetical order, 36 used / 88 cells.
        for mode in ('full','hold'):
            spec=output/f'multi-{mode}.json'
            spec.write_text(json.dumps({'export_version':1,'clips':[{'id':k,'build':str(built[k,mode].relative_to(output))} for k in ('generated','single','layered')],
                'grid':{'cell_width':192,'cell_height':208,'columns':8,'rows':11,'padding':8}},indent=2)+'\n')
            atlas=output/f'multi-atlas-{mode}'
            command('export','--spec',spec,'--output',atlas)
            check=command('validate-export',atlas);assert [c['id'] for c in check['clips']]==['generated','single','layered']
            command('report',atlas)
            with Image.open(atlas/'atlas.png') as im:
                assert im.size==(1536,2288)
                assert not any(im.crop((0,5*208,1536,2288)).tobytes())
            before=tree(atlas);command('export','--spec',spec,'--output',atlas,'--overwrite');assert tree(atlas)==before
        # Human mode for every new/affected command.
        build=built['generated','full']
        for cmd in ('validate','preview','contact-sheet','report'):assert run([cli,cmd,build])
        assert run([cli,'render',build,'--generated-input','--overwrite'])
        assert run([cli,'generate',build,'--spec',output/'generated/generation.json','--adapter-argv',adapter,'--overwrite'])
        assert run([cli,'plan','--spec',output/'single/animation.json','--output',output/'human-plan'])
        assert run([cli,'export','--spec',output/'multi-full.json','--output',output/'human-atlas'])
        assert run([cli,'validate-export',output/'human-atlas'])
        # All documented failure exits, parsed as strict JSON.
        command('export','--spec',output/'multi-full.json','--output',output/'human-atlas',expected=4)
        command('render',output/'missing',expected=3)
        bad=output/'bad.json';bad.write_text('{')
        command('export','--spec',bad,'--output',output/'bad-export',expected=2)
        bad.write_text(json.dumps({'export_version':1,'clips':[{'id':'single','build':'single/build-full'}],
                                  'grid':{'cell_width':192,'cell_height':208,'columns':1,'rows':1,'padding':8}}))
        command('export','--spec',bad,'--output',output/'bad-export',expected=1)
        frame=build/'frames/frame_002.png';original=frame.read_bytes()
        with Image.open(frame) as im:changed=im.convert('RGBA')
        for y in range(changed.height):
            for x in range(changed.width):
                r,g,b,a=changed.getpixel((x,y))
                if a:changed.putpixel((x,y),(255-r,255-g,255-b,a))
        changed.save(frame)
        assert 'FRAME_CONTENT_MISMATCH' in {e['code'] for e in command('validate',build,expected=1)['errors']}
        command('validate-export',all_exports['generated','full'],expected=1)
        frame.write_bytes(original)
        # Pixel-equivalent full-mode re-encoding remains acceptable to both validators.
        with Image.open(frame) as im:changed=im.convert('RGBA')
        info=PngImagePlugin.PngInfo();info.add_text('encoding','acceptance');changed.save(frame,pnginfo=info)
        command('validate',build)
        assert command('validate-export',all_exports['generated','full'])['reencoded_frames']
        frame.write_bytes(original)
        # Execute installed real adapter's auth boundary, with credentials explicitly absent.
        provider_spec=output/'provider-probe.json'
        d=strict((output/'generated/generation.json').read_text());d['adapter']={'id':'openai-images','version':'0.1.0','model':'gpt-image-1','parameters':{},'seed_policy':'allow_unsupported'}
        provider_spec.write_text(json.dumps(d))
        probe=command('generate',build,'--spec',provider_spec,'--adapter-argv',json.dumps([str(provider)]),'--overwrite',expected=4)
        assert probe['errors'][0]['code']=='ADAPTER_AUTH_REQUIRED'
        for p in sources:assert sha(p)==originals[str(p)]
        for p in output.rglob('*.json'):strict(p.read_text())
        for kind in ('single','layered','generated'):
            for mode in ('full','hold'):command('validate-export',all_exports[kind,mode])
        legacy=[]
        for kind in ('single','layered'):
            for name in ('build','build-hold'):
                old=repo/'build/m3-acceptance-final'/kind/name
                if old.is_dir():
                    command('validate',old);legacy.append(str(old))
        summary={'legacy_builds_verified':legacy,'identity':identity,'subprocess_calls':len(records),'harness_calls':sum(Path(r['argv'][0]).name=='sprite-harness' for r in records),
                 'all_expected_exits_matched':True,'exit_codes':[0,1,2,3,4],'strict_json':True,'pythonpath_removed':True,'cwd_outside_repository':True,
                 'source_hashes_unchanged':originals,'pipelines':pipelines,'multi_clip_order':['generated','single','layered'],
                 'fixed_grid':{'columns':8,'rows':11,'cell_width':192,'cell_height':208,'used_cells':36,'empty_cells':52},
                 'provider_transport':'tested separately with real adapter and local HTTP service',
                 'provider_live':'NOT COMPLETED: no credential or authorization; no live call made'}
        (output/'summary.json').write_text(json.dumps(summary,indent=2,allow_nan=False)+'\n')
        print(json.dumps(summary,indent=2,allow_nan=False))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True)
    main(parser.parse_args().output)
