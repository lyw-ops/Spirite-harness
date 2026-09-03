"""Small strict schema boundary for the shipped M4/M5 JSON contracts.

Only the keywords used by our packaged schemas are implemented. Development
checks compare against jsonschema; it remains a development-only dependency.
"""
from functools import lru_cache
from importlib.resources import files
import hashlib
import json
import math
import re
from pathlib import Path

from .spec import SpecLoadError
from .processing import ProcessingError

MAX_JSON_BYTES = 4 * 1024 * 1024
MAX_IMAGE_BYTES = 32 * 1024 * 1024
MAX_PIXELS = 64_000_000


class ContractViolation(ProcessingError):
    """Well-formed inputs that fail an integrity or semantic gate (exit 1)."""


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False)


def digest(value):
    return byte_digest(canonical(value).encode('utf-8'))


def byte_digest(data):
    return 'sha256:' + hashlib.sha256(data).hexdigest()


def rgba_digest(image):
    return byte_digest(image.convert('RGBA').tobytes())


def regular_bytes(path, limit=MAX_JSON_BYTES):
    import stat
    path = Path(path)
    try:
        info = path.lstat()
    except FileNotFoundError as exc:
        raise SpecLoadError('INPUT_NOT_FOUND', 'Required input is missing.', path=path) from exc
    if not stat.S_ISREG(info.st_mode):
        raise ContractViolation('INPUT_NOT_REGULAR', 'Input must be a regular non-symlink file.', path=str(path))
    if info.st_size > limit:
        raise ContractViolation('INPUT_TOO_LARGE', 'Input exceeds the byte limit.', limit=limit)
    with path.open('rb') as stream:
        content = stream.read(limit + 1)
    if len(content) > limit:
        raise ContractViolation('INPUT_TOO_LARGE', 'Input exceeds the byte limit.', limit=limit)
    return content


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate JSON property')
        result[key] = value
    return result


def parse_json(data):
    def reject(_):
        raise ValueError('Non-finite JSON number')
    return json.loads(data, object_pairs_hook=_pairs, parse_constant=reject)


def read_json(path, schema=None):
    try:
        value = parse_json(regular_bytes(path))
        _finite(value)
    except (ValueError, UnicodeError, RecursionError) as exc:
        raise SpecLoadError('MALFORMED_SPEC', 'Expected bounded, finite, unique-key JSON.', path=Path(path)) from exc
    if schema:
        check_schema(value, schema)
    return value


def _finite(value):
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError('Nonfinite')
    if isinstance(value, dict):
        for child in value.values():
            _finite(child)
    if isinstance(value, list):
        for child in value:
            _finite(child)


@lru_cache
def schema_document(name):
    return json.loads(files('sprite_harness').joinpath('contracts', f'{name}.schema.json').read_text())


def check_schema(value, name):
    def check(v, s):
        if 'oneOf' in s:
            count = 0
            for variant in s['oneOf']:
                try:
                    check(v, variant)
                    count += 1
                except ValueError:
                    pass
            if count != 1:
                raise ValueError('oneOf')
        types = s.get('type', [])
        if isinstance(types, str):
            types = [types]
        actual = ('null' if v is None else 'boolean' if type(v) is bool else 'integer' if type(v) is int
                  else 'number' if type(v) is float else 'string' if type(v) is str
                  else 'object' if type(v) is dict else 'array' if type(v) is list else '')
        if types and actual not in types and not (actual == 'integer' and 'number' in types):
            raise ValueError('type')
        if 'const' in s and canonical(v) != canonical(s['const']):
            raise ValueError('const')
        if 'enum' in s and canonical(v) not in [canonical(x) for x in s['enum']]:
            raise ValueError('enum')
        if actual in ('integer', 'number'):
            if ('minimum' in s and v < s['minimum'] or 'maximum' in s and v > s['maximum']
                    or 'exclusiveMinimum' in s and v <= s['exclusiveMinimum']):
                raise ValueError('range')
        if actual == 'string':
            if len(v) < s.get('minLength', 0) or len(v) > s.get('maxLength', MAX_JSON_BYTES):
                raise ValueError('length')
            if 'pattern' in s and not re.search(s['pattern'], v):
                raise ValueError('pattern')
        if actual == 'object':
            props = s.get('properties', {})
            if not set(s.get('required', [])).issubset(v):
                raise ValueError('required')
            if s.get('additionalProperties') is False and set(v) - set(props):
                raise ValueError('unknown field')
            for key in v.keys() & props.keys():
                check(v[key], props[key])
        if actual == 'array':
            if len(v) < s.get('minItems', 0) or len(v) > s.get('maxItems', 65536):
                raise ValueError('array length')
            if s.get('uniqueItems') and len({canonical(x) for x in v}) != len(v):
                raise ValueError('duplicate array item')
            for child in v:
                check(child, s.get('items', {}))
    try:
        _finite(value)
        check(value, schema_document(name))
    except (ValueError, TypeError, OverflowError, RecursionError) as exc:
        raise SpecLoadError('MALFORMED_SPEC', f'Invalid {name} contract ({exc}).') from exc


def require_equal(actual, expected, code):
    if canonical(actual) != canonical(expected):
        raise ContractViolation(code, 'Artifact does not match its trusted inputs.')
