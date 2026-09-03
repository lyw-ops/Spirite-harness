"""Real installed-CLI acceptance, run from an isolated cwd with PYTHONPATH removed.

Usage: .venv/bin/python scripts/acceptance_m3.py --output build/m3-acceptance
Creates only a fresh output tree. Saves every subprocess result and a summary.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from PIL import Image


def strict(text):
    def reject(value):
        raise ValueError(f'Non-JSON constant: {value}')
    return json.loads(text, parse_constant=reject)


def hashes(build):
    return [hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((build/'frames').glob('*.png'))]


def main(output):
    repo=Path(__file__).resolve().parents[1]
    output=output.resolve()
    if output.exists():
        raise SystemExit(f'Refusing existing acceptance directory: {output}')
    output.mkdir(parents=True)
    cli=Path(sys.executable).parent/'sprite-harness'
    environment=dict(os.environ)
    environment.pop('PYTHONPATH',None)
    records=[]
    with tempfile.TemporaryDirectory(prefix='sprite-m3-cli-') as work:
        def run(argv, expected=0, as_json=False):
            process=subprocess.run([str(a) for a in argv],cwd=work,env=environment,
                capture_output=True,text=True,timeout=60)
            record={'argv':[str(a) for a in argv], 'cwd':work, 'exit':process.returncode,
                    'expected_exit':expected,'stdout':process.stdout,'stderr':process.stderr}
            records.append(record)
            (output/'commands.json').write_text(json.dumps(records,indent=2,allow_nan=False)+'\n')
            assert process.returncode==expected,record
            return strict(process.stdout) if as_json else process.stdout.strip()

        def command(*args, expected=0):
            return run([cli,*args,'--json'],expected,True)

        identity=run([sys.executable,'-c',
            'import sprite_harness, importlib.metadata, json; print(json.dumps({"version":sprite_harness.__version__, "distribution":importlib.metadata.version("sprite-animation-harness"), "path":sprite_harness.__file__}))'],as_json=True)
        assert identity['version']==identity['distribution']=='0.5.0',identity
        assert 'site-packages' in identity['path'],identity
        assert run([cli,'--version'])=='0.5.0'

        layered=output/'layered'
        single=output/'single'
        run([sys.executable,repo/'scripts/create_layered_placeholder.py',layered])
        run([sys.executable,repo/'scripts/create_placeholder_sprite.py',single/'sprite.png'])
        sources=list((layered/'assets').glob('*.png'))+[layered/'animation.json',single/'sprite.png']
        before={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
        results={}
        for kind,spec,root,override in [
            ('layered',layered/'animation.json',layered,[]),
            ('single',repo/'examples/reimu-eating/eating-loop.json',single,['--source',single/'sprite.png'])]:
            build=root/'build'
            command('plan','--spec',spec,*override,'--output',build)
            render=command('render',build)
            assert render['mode']=='full' and render['frame_count']==12
            if kind=='layered':assert render['skipped_tracks']==[]
            else:assert any(w['code']=='TARGET_TRACKS_SKIPPED' for w in render['warnings'])
            full=hashes(build)
            assert len(full)==12 and len(set(full))>1
            command('validate',build,'--write-qa')
            command('preview',build)
            command('contact-sheet',build)
            report=command('report',build)
            assert report['validation']['valid']
            for cmd in ('validate','preview','contact-sheet','report'):
                assert run([cli,cmd,build])
            command('render',build,expected=4)
            repeat=root/'build-repeat'
            command('plan','--spec',spec,*override,'--output',repeat)
            assert run([cli,'render',repeat])
            assert hashes(repeat)==full
            for file in ('plan.json','frame-plan.json','render.json'):
                assert (repeat/file).read_bytes()==(build/file).read_bytes()
            held=root/'build-hold'
            assert run([cli,'plan','--spec',spec,*override,'--output',held])
            command('render',held,'--reduced-motion')
            assert hashes(held)==[full[0]]*12
            command('validate',held,'--write-qa')
            command('preview',held)
            command('contact-sheet',held)
            command('report',held)
            # Same bounding box, wrong interior RGB, detected by installed validator.
            frame=build/'frames/frame_000.png'
            with Image.open(frame) as image:wrong=image.convert('RGBA')
            bbox=wrong.getchannel('A').getbbox()
            for y in range(wrong.height):
                for x in range(wrong.width):
                    r,g,b,a=wrong.getpixel((x,y))
                    if a:wrong.putpixel((x,y),(255-r,255-g,255-b,a))
            assert wrong.getchannel('A').getbbox()==bbox
            wrong.save(frame)
            invalid=command('validate',build,expected=1)
            assert 'FRAME_CONTENT_MISMATCH' in {e['code'] for e in invalid['errors']}
            command('render',build,'--overwrite')
            assert hashes(build)==full
            command('validate',build,'--write-qa')
            # Malformed frame plan is exit 2; restored exactly after the probe.
            fp=build/'frame-plan.json';original=fp.read_bytes();fp.write_text('{')
            command('render',build,expected=2)
            fp.write_bytes(original)
            command('render',root/'absent',expected=3)
            results[kind]={'full_frames':12,'distinct_full_frames':len(set(full)),
                'held_frames':12,'distinct_held_frames':1,'build':str(build)}

        command('plan','--spec',layered/'animation.json','--source',single/'sprite.png',
                '--output',output/'mixed',expected=2)
        # Validate all sources, not only the first: corrupt the last source.
        last=layered/'assets/hand.png';original=last.read_bytes()
        Image.new('RGBA',(14,14),(1,2,3,4)).save(last)
        invalid=command('validate',layered/'build',expected=1)
        assert {'SOURCE_DIGEST_MISMATCH','SOURCE_DIMENSION_MISMATCH'} <= {e['code'] for e in invalid['errors']}
        last.write_bytes(original)
        for p in sources:assert hashlib.sha256(p.read_bytes()).hexdigest()==before[str(p)]
        for p in output.rglob('*.json'):strict(p.read_text())
        summary={'identity':identity,'commands':len(records),'cwd_outside_repository':True,
                 'pythonpath_removed':True,'strict_json':True,'exit_codes_checked':[0,1,2,3,4],
                 'source_hashes_unchanged':before,'pipelines':results}
        (output/'summary.json').write_text(json.dumps(summary,indent=2,allow_nan=False)+'\n')
        print(json.dumps(summary,indent=2,allow_nan=False))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    main(parser.parse_args().output)
