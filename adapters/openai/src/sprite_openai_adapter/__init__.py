"""External OpenAI Images adapter. Never imported by sprite_harness core.

Official API checked 2026-09-03: POST /v1/images/edits, multipart image,
model gpt-image-1, PNG transparent output, explicit native size. No seed API.
"""
import argparse
import base64
import hashlib
import http.client
import io
import json
import os
from pathlib import Path
import re
import socket
import stat
import time
import urllib.error
import urllib.request
import uuid

from PIL import Image

MAX_RESPONSE = 48 * 1024 * 1024
MAX_IMAGE = 32 * 1024 * 1024


class AdapterError(Exception):
    def __init__(self, code):
        self.code = code
        super().__init__(code)


def canonical(data):
    return json.dumps(data, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False)


def sha(data):
    return 'sha256:' + hashlib.sha256(data).hexdigest()


def multipart(fields, image):
    boundary = 'sprite-' + uuid.uuid4().hex
    parts = []
    for name, value in fields.items():
        parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"\r\n\r\n{value}\r\n'.encode())
    parts += [f'--{boundary}\r\nContent-Disposition: form-data; name="image[]"; filename="source.png"\r\nContent-Type: image/png\r\n\r\n'.encode(), image, b'\r\n', f'--{boundary}--\r\n'.encode()]
    return b''.join(parts), 'multipart/form-data; boundary=' + boundary


def _decode_png(data, size):
    if len(data) > MAX_IMAGE:
        raise AdapterError('PROVIDER_OUTPUT_INVALID')
    try:
        with Image.open(io.BytesIO(data)) as im:
            if im.format != 'PNG' or im.size != size or im.mode not in ('RGBA', 'LA') and not (im.mode == 'P' and 'transparency' in im.info):
                raise AdapterError('PROVIDER_OUTPUT_INVALID')
            im.load()
    except (OSError, ValueError, Image.DecompressionBombError) as exc:
        raise AdapterError('PROVIDER_OUTPUT_INVALID') from exc


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def http_transport(request, timeout):
    # Never forward Authorization or source artwork to a redirect destination.
    return urllib.request.build_opener(_NoRedirect()).open(request, timeout=timeout)


def generate(request, request_dir, output, *, api_key, transport=http_transport, sleep=time.sleep):
    if not api_key:
        raise AdapterError('ADAPTER_AUTH_REQUIRED')
    adapter = request.get('adapter', {})
    if (type(request.get('request_version')) is not int or request['request_version'] != 1 or
            adapter.get('id') != 'openai-images' or adapter.get('version') != '0.1.0' or adapter.get('model') != 'gpt-image-1'):
        raise AdapterError('ADAPTER_INVALID_REQUEST')
    if adapter.get('seed_policy') != 'allow_unsupported':
        raise AdapterError('PROVIDER_SEED_UNSUPPORTED')
    params = adapter.get('parameters', {})
    if set(params) - {'quality', 'input_fidelity', 'timeout_seconds', 'rate_limit_retries'}:
        raise AdapterError('ADAPTER_INVALID_REQUEST')
    quality = params.get('quality', 'medium')
    fidelity = params.get('input_fidelity', 'high')
    timeout = params.get('timeout_seconds', 90)
    retries = params.get('rate_limit_retries', 0)
    if (quality not in ('medium', 'high') or fidelity not in ('low', 'high') or
            type(timeout) not in (int, float) or not 0 < timeout <= 300 or
            type(retries) is not int or retries not in (0, 1)):
        raise AdapterError('ADAPTER_INVALID_REQUEST')
    results = []
    # Preflight every item before sending any potentially paid request.
    prepared = []
    seen = set()
    for item in request['items']:
        size = (item['output']['width'], item['output']['height'])
        if size not in ((1024, 1024), (1024, 1536), (1536, 1024)):
            raise AdapterError('PROVIDER_UNSUPPORTED_SIZE')
        source_path = request_dir / item['source']['path']
        if (source_path.is_symlink() or not source_path.resolve().is_relative_to(request_dir.resolve())
                or not stat.S_ISREG(source_path.stat().st_mode) or source_path.stat().st_size > MAX_IMAGE):
            raise AdapterError('ADAPTER_INVALID_REQUEST')
        source = source_path.read_bytes()
        if sha(source) != item['source']['sha256']:
            raise AdapterError('ADAPTER_INVALID_REQUEST')
        _decode_png(source, size)
        ident = item['id']
        if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,79}', ident) or ident in seen or (output / f'{ident}.png').exists():
            raise AdapterError('ADAPTER_INVALID_REQUEST')
        seen.add(ident)
        prepared.append((item, size, source))
    for item, size, source in prepared:
        body, content_type = multipart({'model': 'gpt-image-1', 'prompt': item['instruction'],
                                       'size': f'{size[0]}x{size[1]}', 'n': '1', 'background': 'transparent',
                                       'output_format': 'png', 'quality': quality, 'input_fidelity': fidelity}, source)
        http_request = urllib.request.Request('https://api.openai.com/v1/images/edits', data=body,
                                             headers={'Authorization': 'Bearer ' + api_key, 'Content-Type': content_type}, method='POST')
        for attempt in range(retries + 1):
            try:
                with transport(http_request, timeout=timeout) as response:
                    payload = response.read(MAX_RESPONSE + 1)
                    provider_id = response.headers.get('x-request-id')
                break
            except urllib.error.HTTPError as exc:
                status = exc.code
                exc.close()
                if status == 429 and attempt < retries:
                    sleep(1)  # bounded; no provider-controlled unbounded delay
                    continue
                raise AdapterError('PROVIDER_RATE_LIMITED' if status == 429 else
                                   'PROVIDER_AUTH_FAILED' if status in (401, 403) else
                                   'PROVIDER_UNAVAILABLE' if status >= 500 else 'PROVIDER_REJECTED') from None
            except (TimeoutError, socket.timeout):
                raise AdapterError('PROVIDER_TIMEOUT') from None
            except (urllib.error.URLError, OSError, http.client.HTTPException):
                # Outcome is unknown: never automatically repeat a paid request.
                raise AdapterError('PROVIDER_UNAVAILABLE') from None
        if len(payload) > MAX_RESPONSE:
            raise AdapterError('PROVIDER_INVALID_RESPONSE')
        try:
            data = json.loads(payload)
            if not isinstance(data.get('data'), list) or len(data['data']) != 1:
                raise ValueError()
            raw = base64.b64decode(data['data'][0]['b64_json'], validate=True)
        except (ValueError, TypeError, KeyError, UnicodeError):
            raise AdapterError('PROVIDER_INVALID_RESPONSE') from None
        _decode_png(raw, size)
        if not isinstance(provider_id, str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,200}', provider_id) or api_key in provider_id:
            provider_id = None
        filename = item['id'] + '.png'
        with (output / filename).open('xb') as stream:
            stream.write(raw)
        results.append({'id': item['id'], 'item_digest': item['item_digest'],
                        'candidate_id': item['id'], 'file': filename, 'sha256': sha(raw),
                        'width': size[0], 'height': size[1], 'provider_request_id': provider_id})
    return {'response_version': 1, 'request_id': request['request_id'],
            'request_digest': sha(canonical(request).encode()),
            'adapter': {key: adapter[key] for key in ('id', 'version', 'model')},
            'seed_supported': False, 'results': results}


def main(argv=None):
    parser = argparse.ArgumentParser(description='Explicit external OpenAI image edit adapter (paid network calls).')
    parser.add_argument('--request', type=Path, required=True)
    parser.add_argument('--response', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.request.stat().st_size > 4 * 1024 * 1024:
            raise AdapterError('ADAPTER_INVALID_REQUEST')
        request = json.loads(args.request.read_text())
        result = generate(request, args.request.parent, args.output, api_key=os.environ.get('OPENAI_API_KEY'))
        code = 0
    except AdapterError as exc:
        result, code = {'error_code': exc.code}, 4
    except Exception:
        result, code = {'error_code': 'ADAPTER_INVALID_REQUEST'}, 4
    # A fresh explicit response path only. No raw headers/body/exceptions/secrets.
    with args.response.open('x') as stream:
        json.dump(result, stream, allow_nan=False, sort_keys=True)
        stream.write('\n')
    return code
