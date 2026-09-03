"""Reproducible full engineering gates with exact command/output records.

Run with the repository venv. Local loopback HTTP test permission is required;
there are no live provider requests, package downloads, commits or pushes.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys


def main(output, acceptance):
    repo=Path(__file__).resolve().parents[1]
    output=output.resolve();output.mkdir(parents=True,exist_ok=True)
    if (output/'gates.json').exists():raise SystemExit('Use a fresh verification directory.')
    records=[]
    commands=[('pytest',[sys.executable,'-m','pytest']),
              ('compileall',[sys.executable,'-m','compileall','-q','src','adapters/openai/src','scripts','tests']),
              ('install-core',[sys.executable,'-m','pip','install','--no-deps','--no-build-isolation','.']),
              ('install-provider',[sys.executable,'-m','pip','install','--no-deps','--no-build-isolation','./adapters/openai']),
              ('pip-check',[sys.executable,'-m','pip','check']),
              ('diff-check',['git','diff','--check']),
              ('acceptance',[sys.executable,'scripts/acceptance_m4_m5.py','--output',str(acceptance.resolve())])]
    for label,argv in commands:
        process=subprocess.run(argv,cwd=repo,capture_output=True,text=True,timeout=180)
        record={'gate':label,'argv':argv,'expected_exit':0,'actual_exit':process.returncode,
                'stdout':process.stdout,'stderr':process.stderr}
        records.append(record)
        (output/(label+'.log')).write_text(process.stdout+process.stderr)
        (output/'gates.json').write_text(json.dumps(records,indent=2,allow_nan=False)+'\n')
        print(f'{label}: exit {process.returncode}',flush=True)
        if process.returncode:raise SystemExit('Gate failed; inspect '+str(output/(label+'.log')))
    for name in ['commands.json','summary.json']:
        (output/('cli-'+name)).write_bytes((acceptance/name).read_bytes())
    print(f'All gates passed. Logs: {output}',flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True);parser.add_argument('--acceptance',type=Path,required=True)
    args=parser.parse_args();main(args.output,args.acceptance)
