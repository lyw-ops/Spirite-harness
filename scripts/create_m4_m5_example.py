"""Create fresh original geometric assets/specs for the three M4/M5 pipelines."""
import json
from pathlib import Path
import shutil
import sys

from PIL import Image, ImageDraw
from create_layered_placeholder import main as draw_layers


def main(output):
    output=output.expanduser().resolve()
    if output.exists():raise SystemExit('Choose a fresh example directory.')
    output.mkdir(parents=True)
    repo=Path(__file__).resolve().parents[1]
    for name in ('layered','generated'):
        draw_layers(output/name)
    generated=output/'generated/animation.json'
    doc=json.loads(generated.read_text());doc['seed']=2026;doc['animation_id']='generated_geometry'
    generated.write_text(json.dumps(doc,indent=2)+'\n')
    shutil.copyfile(repo/'examples/generated-placeholder/generation.json',output/'generated/generation.json')
    single=output/'single';single.mkdir()
    image=Image.new('RGBA',(64,64));draw=ImageDraw.Draw(image)
    draw.rectangle((18,22,46,54),fill=(40,160,170,255))
    draw.polygon([(32,5),(48,23),(16,23)],fill=(245,175,50,255))
    image.save(single/'sprite.png')
    doc={'plan_version':1,'animation_id':'single_geometry','source':{'image':'sprite.png'},
         'canvas':{'width':96,'height':112,'background':'transparent'},'anchor':{'type':'bottom_center'},
         'playback':{'fps':12,'frame_count':12,'loop':True},'reduced_motion':{'mode':'hold_first_frame'},
         'constraints':{'max_displacement_px':3,'max_frame_delta_px':2},
         'tracks':[{'track_id':'sway','target':'sprite','motion':'translate_x','amplitude':2,'unit':'px'},
                   {'track_id':'tilt','target':'sprite','motion':'rotate','amplitude':5,'unit':'deg','phase':0.25}]}
    (single/'animation.json').write_text(json.dumps(doc,indent=2)+'\n')
    print(f'Original geometric examples created: {output}')


if __name__=='__main__':main(Path(sys.argv[1]))
