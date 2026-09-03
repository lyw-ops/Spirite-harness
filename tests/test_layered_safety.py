"""Run every original M2 safety gate unchanged against a two-layer build.

Reusing the scenarios preserves their failure injection and assertions; this
module changes only the input factory. The original module still runs in full.
"""
import json
from pathlib import Path

import pytest
from PIL import Image

import test_render_safety as gates
from sprite_harness.cli import main


def layered_factory(tmp_path, capsys, *, source, name='build', frame_count=4,
                    canvas=(16,16), background='transparent', anchor=None,
                    tracks=None, reduced_motion=None, loop=True):
    spec_dir=tmp_path/f'{name}-spec'
    spec_dir.mkdir(exist_ok=True)
    with Image.open(source) as im: source_size=im.size
    width,height=canvas or source_size
    anchor=anchor or {'type':'bottom_center'}
    ax,ay=({'center':(.5,.5),'bottom_center':(.5,1)}.get(anchor['type'])
           or (anchor['x'],anchor['y']))
    empty=spec_dir/'empty.png';Image.new('RGBA',(2,2)).save(empty)
    document={'plan_version':2,'animation_id':'render_test',
        'playback':{'fps':8,'frame_count':frame_count,'loop':loop},
        'canvas':{'width':width,'height':height,'background':background},
        'anchor':anchor,'tracks':tracks or [],
        'source':{'reference_canvas':{'width':width,'height':height},'layers':[
            {'target':'visible','image':str(source),'anchor':anchor,
             'position':{'x':width*ax,'y':height*ay}},
            {'target':'invisible','image':'empty.png','anchor':{'type':'center'},
             'position':{'x':0,'y':0}}]}}
    if reduced_motion:document['reduced_motion']={'mode':reduced_motion}
    spec=spec_dir/'animation.json';spec.write_text(json.dumps(document))
    build=tmp_path/name
    assert main(['plan','--spec',str(spec),'--output',str(build),'--json'])==0
    capsys.readouterr()
    return build


@pytest.fixture(autouse=True)
def layered_inputs(monkeypatch):
    monkeypatch.setattr(gates,'make_build',layered_factory)


# Pytest retains the original parametrization and fixtures of each callable.
for _name in dir(gates):
    if _name.startswith('test_'):
        globals()[_name] = getattr(gates,_name)
