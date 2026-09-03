"""Explicit provider-neutral generation, frozen input binding and offline replay."""
from pathlib import Path
import hashlib
import io
import os
import re
import shutil
import signal
import subprocess
import time

from PIL import Image, UnidentifiedImageError

from .contracts import (ContractViolation, MAX_IMAGE_BYTES, MAX_JSON_BYTES, MAX_PIXELS,
                        byte_digest, canonical, check_schema, digest, read_json,
                        regular_bytes, require_equal, rgba_digest)
from .expand import plan_digest
from .plan import resolved_anchor
from .processing import ProcessingError
from .qa import subject_qa, write_json_artifact
from .spec import SpecLoadError
from .transactions import guard_directory, publish_directory, recheck, snapshot, transaction

GENERATION_DIR = 'generation'
GENERATION_MARKER = '.generation-transaction'


def derive_seed(seed, request_id, item_id, target, frames):
    data = ['sprite-harness-generation-v1', seed, request_id, item_id, target, sorted(frames)]
    return int.from_bytes(hashlib.sha256(canonical(data).encode()).digest()[:8], 'big')


def normalize_request(build, spec_path, root):
    spec = read_json(spec_path, 'generation-spec')
    if build.plan.seed is None:
        raise ContractViolation('GENERATION_SEED_REQUIRED', 'Generation requires an explicit plan.seed.')
    sources = ({layer.target: (build.plan.spec_dir / layer.source_image, layer)
                for layer in build.plan.layers} if build.plan.layered else
               {'sprite': (build.plan.resolved_source_path(), build.plan)})
    seen_ids, seen_pairs = set(), set()
    items = []
    for item in spec['requests']:
        target, ident = item['target'], item['id']
        if ident in seen_ids:
            raise ContractViolation('DUPLICATE_GENERATION_REQUEST', 'Request ids must be unique.')
        seen_ids.add(ident)
        if target not in sources or sources[target][0] is None:
            raise ContractViolation('UNKNOWN_GENERATION_TARGET', 'Replacement target must bind an existing source PNG.')
        frames = sorted(item['frames'])
        for index in frames:
            if index >= build.plan.frame_count:
                raise ContractViolation('GENERATION_FRAME_OUT_OF_RANGE', 'Requested frame is outside the plan.')
            if (target, index) in seen_pairs:
                raise ContractViolation('GENERATION_MAPPING_OVERLAP', 'Target/frame mappings must not overlap.')
            seen_pairs.add((target, index))
        source_path, source = sources[target]
        image, stats = inspect_png(source_path)
        ax, ay = resolved_anchor(source)
        normalized = {**item, 'frames': frames,
                      'seed': derive_seed(build.plan.seed, spec['request_id'], ident, target, frames),
                      'source': {'path': f'references/{ident}.png',
                                 'sha256': stats['sha256'], 'width': image.width, 'height': image.height,
                                 'anchor': {'x': ax, 'y': ay}},
                      'output': {'width': image.width, 'height': image.height,
                                 'format': 'PNG', 'alpha': 'required'}}
        normalized['item_digest'] = digest(normalized)
        items.append(normalized)
    if len(items) > 256 or sum(i['output']['width'] * i['output']['height'] for i in items) > MAX_PIXELS:
        raise ContractViolation('GENERATION_LIMIT_EXCEEDED', 'At most 256 candidates / 64 million total pixels are supported.')
    request = {'request_version': 1, 'request_id': spec['request_id'],
               'plan_digest': plan_digest(build.normalized_plan),
               'spec': {'path': 'spec.json',
                        'sha256': byte_digest(regular_bytes(spec_path))},
               'seed': build.plan.seed, 'adapter': spec['adapter'], 'items': items}
    check_schema(request, 'generation-request')
    return request


def inspect_png(path):
    data = regular_bytes(path, MAX_IMAGE_BYTES)
    try:
        with Image.open(io.BytesIO(data)) as image:
            if image.format != 'PNG':
                raise ContractViolation('GENERATION_PNG_REQUIRED', 'Candidate/reference must be PNG.')
            if image.width > 16384 or image.height > 16384 or image.width * image.height > MAX_PIXELS:
                raise ContractViolation('IMAGE_LIMIT_EXCEEDED', 'Image dimensions exceed the supported limit.')
            if image.mode not in ('RGBA', 'LA') and not (image.mode == 'P' and 'transparency' in image.info):
                raise ContractViolation('GENERATION_ALPHA_REQUIRED', 'PNG must already contain an alpha channel.')
            image.load()
            rgba = image.convert('RGBA')
    except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError) as exc:
        raise ContractViolation('GENERATION_INVALID_PNG', 'PNG could not be decoded.') from exc
    return rgba, {'sha256': byte_digest(data), 'rgba_digest': rgba_digest(rgba),
                  'width': rgba.width, 'height': rgba.height}


def inside(root, relative):
    path = root / relative
    if Path(relative).is_absolute() or '..' in Path(relative).parts or not path.resolve().is_relative_to(root.resolve()):
        raise ContractViolation('GENERATION_PATH_ESCAPE', 'Candidate path escapes its declared output area.')
    for part in (path, *path.parents):
        if part == root.parent:
            break
        if part.is_symlink():
            raise ContractViolation('GENERATION_PATH_ESCAPE', 'Candidate paths must not use symlinks.')
    return path


def response_bindings(request, response):
    check_schema(response, 'generation-response')
    require_equal(response['request_id'], request['request_id'], 'GENERATION_RESPONSE_MISMATCH')
    require_equal(response['request_digest'], digest(request), 'GENERATION_RESPONSE_MISMATCH')
    require_equal(response['adapter'], {k: request['adapter'][k] for k in ('id', 'version', 'model')}, 'GENERATION_ADAPTER_MISMATCH')
    if not response['seed_supported'] and request['adapter']['seed_policy'] == 'required':
        raise ContractViolation('GENERATION_SEED_UNSUPPORTED', 'Adapter does not support the required seed.')
    by_id, files, candidates = {}, set(), set()
    for result in response['results']:
        if result['id'] in by_id or result['file'] in files or result['candidate_id'] in candidates:
            raise ContractViolation('GENERATION_RESULT_DUPLICATE', 'Duplicate result, file or candidate identity.')
        by_id[result['id']] = result
        files.add(result['file'])
        candidates.add(result['candidate_id'])
    if set(by_id) != {item['id'] for item in request['items']}:
        raise ContractViolation('GENERATION_RESULT_COVERAGE', 'Every request requires exactly one result.')
    for item in request['items']:
        result = by_id[item['id']]
        require_equal(result['item_digest'], item['item_digest'], 'GENERATION_ITEM_MISMATCH')
        require_equal([result['width'], result['height']], [item['output']['width'], item['output']['height']], 'GENERATION_SIZE_MISMATCH')
        inside(Path('/candidate-output'), result['file'])
        if Path(result['file']).name != result['file']:
            raise ContractViolation('GENERATION_PATH_ESCAPE', 'Candidate files must be direct children of the output directory.')
    return by_id


def accepted_document(request, response, stats, spec_source):
    bindings = response_bindings(request, response)
    inputs = []
    for item in request['items']:
        result = bindings[item['id']]
        info = stats[item['id']]
        require_equal([info['sha256'], info['width'], info['height']],
                      [result['sha256'], result['width'], result['height']], 'GENERATION_CANDIDATE_MISMATCH')
        inputs.append({'id': item['id'], 'candidate_id': result['candidate_id'],
                       'target': item['target'], 'frames': item['frames'],
                       'file': f"inputs/{item['id']}.png", **info})
    return {'accepted_version': 1, 'spec_source': spec_source, 'plan_digest': request['plan_digest'],
            'request_digest': digest(request), 'response_digest': digest(response),
            'spec_digest': request['spec']['sha256'], 'seed_supported': response['seed_supported'],
            'inputs': inputs}


def generation_qa(accepted):
    return subject_qa('generation', {'request_digest': accepted['request_digest'],
                                   'accepted_digest': digest(accepted)},
                      ['request_binding', 'candidate_integrity', 'mapping_coverage'],
                      skipped=['visual_semantics', 'aesthetic_quality', 'provider_authenticity'])


def owned_files(request):
    return {'spec.json', 'request.json', 'response.json', 'accepted.json', 'generation.qa.json',
            *(f'{directory}/{item["id"]}.png' for directory in ('references', 'inputs') for item in request['items'])}


def generation_paths(build):
    """Protect all current bundle files even when a manifest is damaged."""
    root = build.build_dir / GENERATION_DIR
    paths = list(root.rglob('*')) if root.is_dir() and not root.is_symlink() else []
    protected = [path for path in paths if path.is_file()]
    try:
        accepted = read_json(root / 'accepted.json', 'generated-inputs')
        protected.append((root / accepted['spec_source']['path']).resolve())
    except (SpecLoadError, ProcessingError):
        pass
    return tuple(protected)


def load_generation(build):
    root = build.build_dir / GENERATION_DIR
    if root.is_symlink():
        raise ContractViolation('GENERATION_PATH_ESCAPE', 'Generation directory must not be a symlink.')
    request = read_json(root / 'request.json', 'generation-request')
    guard_directory(root, (), owned_files(request), overwrite=True)
    accepted = read_json(root / 'accepted.json', 'generated-inputs')
    origin = (root / accepted['spec_source']['path']).resolve()
    require_equal(accepted['spec_source']['sha256'], request['spec']['sha256'], 'GENERATION_SPEC_STALE')
    expected = normalize_request(build, origin, root)
    require_equal(request, expected, 'GENERATION_REQUEST_STALE')
    if regular_bytes(root / 'spec.json') != regular_bytes(origin):
        raise ContractViolation('GENERATION_SPEC_STALE', 'Original generation spec changed.')
    response = read_json(root / 'response.json', 'generation-response')
    response_bindings(request, response)
    stats, images = {}, {}
    for item in request['items']:
        reference_path = inside(root, item['source']['path'])
        _, info = inspect_png(reference_path)
        require_equal(info['sha256'], item['source']['sha256'], 'GENERATION_REFERENCE_CHANGED')
        path = inside(root, f"inputs/{item['id']}.png")
        image, stats[item['id']] = inspect_png(path)
        for index in item['frames']:
            images[item['target'], index] = image
    require_equal(accepted, accepted_document(request, response, stats, accepted['spec_source']), 'GENERATION_INPUTS_STALE')
    require_equal(read_json(root / 'generation.qa.json'), generation_qa(accepted), 'GENERATION_QA_STALE')
    actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if not p.is_dir()}
    if actual != owned_files(request):
        raise ContractViolation('GENERATION_BUNDLE_CONTENTS', 'Generation bundle has missing or undeclared files.')
    return images, {'request_digest': digest(request), 'accepted_digest': digest(accepted)}


def run_adapter(argv, request_path, response_path, output, timeout):
    if (not isinstance(argv, list) or not argv or any(type(arg) is not str or not arg or '\x00' in arg for arg in argv)
            or not isinstance(timeout, (float, int)) or not 0 < timeout <= 3600):
        raise SpecLoadError('MALFORMED_SPEC', 'Explicit adapter argv and a finite timeout in (0,3600] are required.')
    args = [*argv, '--request', str(request_path), '--response', str(response_path), '--output', str(output)]
    # Never retain or echo adapter stdout/stderr, argv or inherited credentials.
    try:
        process = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                   start_new_session=True, shell=False)
    except OSError as exc:
        raise ProcessingError('ADAPTER_START_FAILED', 'Adapter executable could not be started.') from exc
    deadline = time.monotonic() + timeout

    def check_limits():
        if response_path.is_file() and response_path.stat().st_size > MAX_JSON_BYTES:
            raise ProcessingError('ADAPTER_RESPONSE_TOO_LARGE', 'Adapter response exceeds the byte limit.')
        total = 0
        for path in output.iterdir():
            if path.is_symlink() or not path.is_file():
                raise ProcessingError('ADAPTER_OUTPUT_INVALID', 'Adapter outputs must be regular files.')
            length = path.stat().st_size
            total += length
            if length > MAX_IMAGE_BYTES or total > 256 * 1024 * 1024:
                raise ProcessingError('ADAPTER_OUTPUT_TOO_LARGE', 'Adapter output exceeds its quota.')

    try:
        while process.poll() is None:
            if time.monotonic() > deadline:
                raise ProcessingError('ADAPTER_TIMEOUT', 'Adapter exceeded its deadline; result is unknown, no automatic retry.')
            check_limits()
            time.sleep(0.02)
        check_limits()  # Fast exits obey exactly the same limits and error codes.
        if process.returncode != 0:
            code = 'ADAPTER_FAILED'
            try:
                failure = read_json(response_path)
                allowed = {'ADAPTER_AUTH_REQUIRED', 'PROVIDER_AUTH_FAILED', 'PROVIDER_RATE_LIMITED',
                           'PROVIDER_TIMEOUT', 'PROVIDER_UNAVAILABLE', 'PROVIDER_REJECTED',
                           'PROVIDER_INVALID_RESPONSE', 'PROVIDER_OUTPUT_INVALID',
                           'PROVIDER_UNSUPPORTED_SIZE', 'PROVIDER_SEED_UNSUPPORTED', 'ADAPTER_INVALID_REQUEST'}
                if isinstance(failure, dict) and failure.get('error_code') in allowed:
                    code = failure['error_code']
            except (SpecLoadError, ProcessingError):
                pass
            raise ProcessingError(code, 'Adapter failed; credentials and raw diagnostics are not logged. No automatic core retry.')
    finally:
        # Reap/terminate the complete process group, including lingering children.
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait()


def generate_build(build, spec_path, argv, *, timeout=120, overwrite=False):
    from .build import validate_build_inputs
    from .transactions import reject_links
    root = build.build_dir / GENERATION_DIR
    marker = build.build_dir / GENERATION_MARKER
    spec_path = spec_path.expanduser().absolute()
    inputs = (*build.plan.protected_paths(), build.build_dir / 'frame-plan.json',
              build.build_dir / 'render.json', spec_path)
    # Bind the first reads, including normalization, to the publication check.
    before = snapshot(inputs)
    # Core build inputs only: old generated inputs may be rebuilt explicitly.
    result, _ = validate_build_inputs(build, include_generation=False)
    if not result.valid:
        raise ContractViolation('GENERATION_BUILD_INVALID', 'Plan/source/frame-plan failed validation.', errors=result.as_dict()['errors'])
    request = normalize_request(build, spec_path, root)
    recheck(before)
    allowed = owned_files(request)
    if root.is_dir() and not root.is_symlink():
        # The old spec establishes which files are owned; arbitrary filenames
        # are never inferred from a directory scan.
        old = read_json(root / 'request.json', 'generation-request')
        allowed |= owned_files(old)
    guard_directory(root, inputs, allowed, overwrite)
    # The existing render marker provides mutual exclusion with M2/M3 render.
    with transaction(build.build_dir / '.render-transaction', 'RENDER'):
        with transaction(marker, 'GENERATION'):
            staged = marker / 'new'
            staged.mkdir()
            (staged / 'references').mkdir()
            (staged / 'inputs').mkdir()
            shutil.copyfile(spec_path, staged / 'spec.json')
            write_json_artifact(staged / 'request.json', request)
            for item in request['items']:
                original = (next(build.plan.spec_dir / layer.source_image for layer in build.plan.layers if layer.target == item['target'])
                            if build.plan.layered else build.plan.resolved_source_path())
                shutil.copyfile(original, staged / item['source']['path'])
            adapter_inputs = snapshot([staged / 'request.json', staged / 'spec.json', *(staged / item['source']['path'] for item in request['items'])])
            candidates = marker / 'candidates'
            candidates.mkdir()
            response_path = staged / 'response.json'
            run_adapter(argv, staged / 'request.json', response_path, candidates, timeout)
            recheck(adapter_inputs)
            # The adapter owns only its response and candidates. Check the
            # whole staging tree before any core write could follow an alias.
            guard_directory(staged, inputs, owned_files(request), overwrite=True)
            destinations = {'accepted.json', 'generation.qa.json',
                            *(f'inputs/{item["id"]}.png' for item in request['items'])}
            if any((staged / name).exists() or (staged / name).is_symlink() for name in destinations):
                raise ContractViolation('GENERATION_OUTPUT_COLLISION', 'Adapter populated a harness-owned destination.')
            response = read_json(response_path, 'generation-response')
            bindings = response_bindings(request, response)
            stats = {}
            for item in request['items']:
                candidate = inside(candidates, bindings[item['id']]['file'])
                _, stats[item['id']] = inspect_png(candidate)
                if candidate.stat().st_nlink != 1 or any(p.is_file() and candidate.samefile(p) for p in inputs):
                    raise ContractViolation('GENERATION_CANDIDATE_ALIAS', 'Candidate must be an independent file.')
                with candidate.open('rb') as source, (staged / f"inputs/{item['id']}.png").open('xb') as destination:
                    shutil.copyfileobj(source, destination)
                _, copied = inspect_png(staged / f"inputs/{item['id']}.png")
                require_equal(copied, stats[item['id']], 'INPUT_CHANGED')
            if {p.name for p in candidates.iterdir()} != {r['file'] for r in bindings.values()}:
                raise ContractViolation('GENERATION_OUTPUT_COLLISION', 'Candidate directory contains undeclared output.')
            accepted = accepted_document(request, response, stats, {'path': os.path.relpath(spec_path.resolve(), root), 'sha256': request['spec']['sha256']})
            write_json_artifact(staged / 'accepted.json', accepted)
            write_json_artifact(staged / 'generation.qa.json', generation_qa(accepted))
            recheck(before)
            guard_directory(staged, inputs, owned_files(request), overwrite=True)
            guard_directory(root, inputs, allowed, overwrite)
            publish_directory(staged, root, marker, 'GENERATION')
    return {'success': True, 'output': str(root), 'backend': 'generated-input',
            'request_digest': digest(request), 'accepted_digest': digest(accepted),
            'seed_supported': response['seed_supported'], 'accepted_count': len(accepted['inputs'])}
