"""TEST SUBSTITUTE ONLY: draw geometric PNG candidates; never contacts a model."""
import argparse
import hashlib
import json
from PIL import Image, ImageDraw


def digest(data):
    return 'sha256:' + hashlib.sha256(data).hexdigest()


def main():
    from pathlib import Path
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('request', 'response', 'output'):
        parser.add_argument('--' + name, type=Path, required=True)
    args = parser.parse_args()
    request = json.loads(args.request.read_text())
    results = []
    for item in request['items']:
        size = (item['output']['width'], item['output']['height'])
        im = Image.new('RGBA', size)
        # Explicitly a geometric test substitute, independent of the renderer.
        color = (40, 180, 240, 192)
        ImageDraw.Draw(im).rectangle((size[0]//4, size[1]//4, max(size[0]//4, size[0]*3//4-1), max(size[1]//4, size[1]*3//4-1)), fill=color)
        path = args.output / (item['id'] + '.png')
        with path.open('xb') as stream:
            im.save(stream, format='PNG')
        results.append({'id': item['id'], 'item_digest': item['item_digest'], 'candidate_id': item['id'],
                        'file': path.name, 'sha256': digest(path.read_bytes()),
                        'width': size[0], 'height': size[1], 'provider_request_id': None})
    result = {'response_version': 1, 'request_id': request['request_id'],
              'request_digest': digest(json.dumps(request, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False).encode()),
              'adapter': {k: request['adapter'][k] for k in ('id', 'version', 'model')},
              'seed_supported': True, 'results': list(reversed(results))}
    with args.response.open('x') as stream:
        json.dump(result, stream, sort_keys=True, allow_nan=False)
        stream.write('\n')


if __name__ == '__main__':
    main()
