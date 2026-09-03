"""Optional paid/live smoke; requires explicit consent flag and environment key."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

from PIL import Image, ImageDraw


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--authorize-paid-call',action='store_true',help='Authorize a paid model request and upload of the generated geometric reference.')
    args=parser.parse_args()
    if not args.authorize_paid_call:raise SystemExit('Live invocation requires --authorize-paid-call.')
    if not os.environ.get('OPENAI_API_KEY'):raise SystemExit('OPENAI_API_KEY is required; no request was made.')
    output=args.output.expanduser().resolve()
    if output.exists():raise SystemExit('Choose a fresh output directory.')
    output.mkdir(parents=True)
    im=Image.new('RGBA',(1024,1024));ImageDraw.Draw(im).rectangle((320,320,704,704),fill=(40,160,170,255));im.save(output/'source.png')
    plan={'plan_version':1,'animation_id':'live_geometry','seed':2026,'source':{'image':'source.png'},
          'canvas':{'width':1024,'height':1024,'background':'transparent'},'anchor':{'type':'center'},
          'playback':{'fps':2,'frame_count':2,'loop':True},'tracks':[]}
    spec={'generation_version':1,'request_id':'live-geometry','adapter':{'id':'openai-images','version':'0.1.0','model':'gpt-image-1',
           'parameters':{'quality':'medium','input_fidelity':'high','rate_limit_retries':0,'timeout_seconds':90},'seed_policy':'allow_unsupported'},
          'requests':[{'id':'square','target':'sprite','frames':[0,1],
                       'instruction':'Keep the simple centered geometric square and transparent canvas. Change the square color to bright blue. No letters, no additional objects.'}]}
    for name,doc in [('animation.json',plan),('generation.json',spec),('export.json',{'export_version':1,'clips':[{'id':'live','build':'build'}],
              'grid':{'cell_width':1040,'cell_height':1040,'columns':2,'padding':8}})]:
        (output/name).write_text(json.dumps(doc,indent=2)+'\n')
    bin_dir=Path(sys.executable).parent;cli=bin_dir/'sprite-harness';adapter=bin_dir/'sprite-openai-adapter';build=output/'build'
    records=[]
    commands=[['plan','--spec',output/'animation.json','--output',build],
              ['generate',build,'--spec',output/'generation.json','--adapter-argv',json.dumps([str(adapter)])],
              ['render',build,'--generated-input'],['validate',build,'--write-qa'],['preview',build],['contact-sheet',build],
              ['export','--spec',output/'export.json','--output',output/'atlas'],['validate-export',output/'atlas'],['report',output/'atlas']]
    environment=dict(os.environ);environment.pop('PYTHONPATH',None)
    for args in commands:
        proc=subprocess.run([str(cli),*[str(a) for a in args],'--json'],env=environment,cwd=output,capture_output=True,text=True,timeout=150)
        # Core deliberately discards all adapter raw stdout/stderr and secrets.
        records.append({'command':[str(a) for a in args],'exit':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr})
        (output/'commands.json').write_text(json.dumps(records,indent=2,allow_nan=False)+'\n')
        if proc.returncode:raise SystemExit(f'Live smoke stopped at {args[0]}; inspect the redacted command log.')
    print(f'Live provider smoke completed: {output}')


if __name__=='__main__':main()
