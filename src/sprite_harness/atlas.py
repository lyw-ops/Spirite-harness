"""Deterministic grid atlas publication and independent per-frame round trip."""
from copy import deepcopy
from pathlib import Path
import os
import shutil

from PIL import Image

from .build import load_build, validate_build
from .contracts import (ContractViolation, MAX_PIXELS, byte_digest, digest, read_json,
                        regular_bytes, require_equal, rgba_digest)
from .expand import expand_plan, plan_digest
from .generation import inspect_png, load_generation
from .plan import resolved_anchor
from .qa import subject_qa, write_json_artifact
from .spec import SpecLoadError
from .transactions import guard_directory, publish_directory, recheck, reject_links, snapshot, transaction

EXPORT_FILES = {'atlas.png', 'atlas.json', 'export-spec.json', 'export-config.json', 'export.qa.json'}


def export_marker(root):
    return root.parent / f'.{root.name}.export-transaction'


def ensure_complete(root):
    marker = export_marker(root)
    if marker.exists() or marker.is_symlink():
        raise ContractViolation('EXPORT_TRANSACTION_INCOMPLETE', 'Export is active or needs recovery.')


def build_paths(build):
    return (*build.protected_paths, build.build_dir / 'render.json',
            *(build.build_dir / f'frames/frame_{i:03d}.png' for i in range(build.plan.frame_count)))


def normalize_config(spec_path, root):
    spec = read_json(spec_path, 'export-spec')
    if len(spec['clips']) > 4096:
        raise ContractViolation('EXPORT_LIMIT_EXCEEDED', 'At most 4096 clips are supported.')
    if len({clip['id'] for clip in spec['clips']}) != len(spec['clips']):
        raise ContractViolation('DUPLICATE_CLIP_ID', 'Clip ids must be unique.')
    builds, clips, total = [], [], 0
    for clip in spec['clips']:
        path = (spec_path.parent / clip['build']).resolve()
        build = load_build(path)
        builds.append(build)
        total += build.plan.frame_count
        clips.append({'id': clip['id'], 'build': os.path.relpath(path, root)})
    grid = dict(spec['grid'])
    grid.setdefault('rows', (total + grid['columns'] - 1) // grid['columns'])
    if total < 1 or total > 65536 or total > grid['rows'] * grid['columns']:
        raise ContractViolation('EXPORT_CAPACITY_EXCEEDED', 'Grid cannot contain the complete frame set.')
    width, height = grid['columns'] * grid['cell_width'], grid['rows'] * grid['cell_height']
    if width > 16384 or height > 16384 or width * height > MAX_PIXELS:
        raise ContractViolation('EXPORT_LIMIT_EXCEEDED', 'Atlas exceeds dimension/pixel limits.')
    if 2 * grid['padding'] >= min(grid['cell_width'], grid['cell_height']):
        raise ContractViolation('EXPORT_INVALID_PADDING', 'Padding leaves no frame area.')
    for build in builds:
        canvas = build.normalized_plan['canvas']
        if (canvas['width'] > grid['cell_width'] - 2 * grid['padding'] or
                canvas['height'] > grid['cell_height'] - 2 * grid['padding']):
            raise ContractViolation('EXPORT_FRAME_TOO_LARGE', 'Complete source canvas does not fit the cell.')
    return {'config_version': 1, 'spec': {'path': os.path.relpath(spec_path.resolve(), root),
                                        'sha256': byte_digest(regular_bytes(spec_path))},
            'clips': clips, 'grid': grid}, builds


def assemble(config, builds):
    """Recompute every rect/timing/pivot from inputs, never atlas metadata."""
    grid = config['grid']
    atlas = Image.new('RGBA', (grid['columns'] * grid['cell_width'], grid['rows'] * grid['cell_height']), (0, 0, 0, 0))
    clips, index = [], 0
    for declared, build in zip(config['clips'], builds):
        result, _ = validate_build(build)
        if not result.valid:
            raise ContractViolation('EXPORT_INPUT_INVALID', 'An input build failed current validation.', errors=result.as_dict()['errors'])
        render_path = build.build_dir / 'render.json'
        if render_path.exists():
            render = read_json(render_path)
            mode = render['mode']
            backend = render.get('backend', 'deterministic')
        else:
            mode, backend = 'full', 'external'
        generation = load_generation(build)[1] if backend == 'generated-input' else None
        ax, ay = resolved_anchor(build.plan)
        frames = []
        frame_plan = expand_plan(build.plan, build.normalized_plan)
        for source_frame in frame_plan['frames']:
            path = build.build_dir / source_frame['file']
            image, info = inspect_png(path)
            x = (index % grid['columns']) * grid['cell_width'] + grid['padding']
            y = (index // grid['columns']) * grid['cell_height'] + grid['padding']
            atlas.paste(image, (x, y))  # copy all RGBA bytes, including hidden RGB
            frames.append({'index': source_frame['index'], 'file': source_frame['file'],
                           'byte_digest': info['sha256'], 'rgba_digest': info['rgba_digest'],
                           'width': image.width, 'height': image.height,
                           'duration': 1.0, 'duration_ms': 1000.0 / build.plan.fps,
                           'rect': {'x': x, 'y': y, 'width': image.width, 'height': image.height},
                           'placement': {'x': grid['padding'], 'y': grid['padding']},
                           'pivot': {'x': ax * image.width, 'y': ay * image.height},
                           'atlas_pivot': {'x': x + ax * image.width, 'y': y + ay * image.height}})
            index += 1
        clips.append({'id': declared['id'], 'build': declared['build'],
                      'plan_digest': plan_digest(build.normalized_plan),
                      'identities': {'plan': byte_digest(regular_bytes(build.build_dir / 'plan.json')),
                                     'frame_plan': byte_digest(regular_bytes(build.build_dir / 'frame-plan.json')),
                                     'render': byte_digest(regular_bytes(render_path)) if render_path.exists() else None,
                                     'generation': generation},
                      'backend': backend, 'mode': mode, 'fps': build.plan.fps, 'loop': build.plan.loop,
                      'anchor': {'x': ax, 'y': ay}, 'frame_count': len(frames), 'frames': frames})
    document = {'atlas_version': 1, 'config_digest': digest(config),
                'image': {'file': 'atlas.png', 'width': atlas.width, 'height': atlas.height,
                          'rgba_digest': rgba_digest(atlas)}, 'grid': grid, 'clips': clips}
    return atlas, document


def export_qa(metadata):
    return subject_qa('export', {'config_digest': metadata['config_digest'],
                                'atlas_digest': digest(metadata)},
                      ['input_validation', 'layout_recomputed', 'frame_rgba_round_trip', 'transparent_unused_pixels'])


def export_atlas(spec_path, output, *, overwrite=False):
    output = output.expanduser().absolute()
    reject_links(output)
    ensure_complete(output)
    spec_path = spec_path.expanduser().absolute()
    before = snapshot([spec_path])
    config, builds = normalize_config(spec_path, output)
    inputs = (spec_path, *(p for build in builds for p in build_paths(build)))
    # Add discovered inputs without replacing the spec's first-read identity.
    before.update(snapshot(p for p in inputs if p not in before))
    recheck(before)
    guard_directory(output, inputs, EXPORT_FILES, overwrite)
    output.parent.mkdir(parents=True, exist_ok=True)
    marker = export_marker(output)
    with transaction(marker, 'EXPORT'):
        atlas, metadata = assemble(config, builds)
        recheck(before)
        staged = marker / 'new'
        staged.mkdir()
        atlas.save(staged / 'atlas.png', format='PNG')
        shutil.copyfile(spec_path, staged / 'export-spec.json')
        write_json_artifact(staged / 'export-config.json', config)
        write_json_artifact(staged / 'atlas.json', metadata)
        # Decode the written PNG and compare every trusted source region before publication.
        round_trip(staged / 'atlas.png', atlas, metadata, builds)
        write_json_artifact(staged / 'export.qa.json', export_qa(metadata))
        recheck(before)
        guard_directory(output, inputs, EXPORT_FILES, overwrite)
        publish_directory(staged, output, marker, 'EXPORT')
    return {'success': True, 'output': str(output), 'clip_count': len(builds),
            'frame_count': sum(c['frame_count'] for c in metadata['clips']),
            'atlas': str(output / 'atlas.png'), 'config_digest': digest(config)}


def round_trip(path, expected, metadata, builds):
    actual, _ = inspect_png(path)
    if actual.size != expected.size:
        raise ContractViolation('ATLAS_DIMENSION_MISMATCH', 'Atlas dimensions differ from the trusted layout.')
    for clip, build in zip(metadata['clips'], builds):
        for frame in clip['frames']:
            rect = frame['rect']
            image, _ = inspect_png(build.build_dir / frame['file'])
            cropped = actual.crop((rect['x'], rect['y'], rect['x'] + rect['width'], rect['y'] + rect['height']))
            if image.size != cropped.size or image.tobytes() != cropped.tobytes():
                raise ContractViolation('ATLAS_FRAME_MISMATCH', 'Atlas crop differs from the complete source RGBA.', clip=clip['id'], index=frame['index'])
    if actual.tobytes() != expected.tobytes():
        raise ContractViolation('ATLAS_PADDING_MISMATCH', 'Padding or unused cells must be transparent RGBA zero.')


def validate_export(output):
    output = output.expanduser().absolute()
    ensure_complete(output)
    reject_links(output)
    before = snapshot(output / file for file in EXPORT_FILES)
    config = read_json(output / 'export-config.json', 'export-config')
    spec_path = (output / config['spec']['path']).resolve()
    if spec_path not in before:
        before.update(snapshot([spec_path]))
    expected_config, builds = normalize_config(spec_path, output)
    inputs = (spec_path, *(p for build in builds for p in build_paths(build)),
              *(output / file for file in EXPORT_FILES))
    before.update(snapshot(p for p in inputs if p not in before))
    recheck(before)
    require_equal(config, expected_config, 'EXPORT_CONFIG_STALE')
    if regular_bytes(output / 'export-spec.json') != regular_bytes(spec_path):
        raise ContractViolation('EXPORT_SPEC_STALE', 'Original export specification changed.')
    actual_metadata = read_json(output / 'atlas.json', 'atlas')
    atlas, expected_metadata = assemble(config, builds)
    comparable = deepcopy(actual_metadata)
    reencoded = []
    # Byte observations are separate from RGBA requirements. Only these
    # observational hashes may differ after a pixel-equivalent re-encoding.
    for old_clip, new_clip in zip(comparable['clips'], expected_metadata['clips']):
        for old, new in zip(old_clip['frames'], new_clip['frames']):
            if old['byte_digest'] != new['byte_digest']:
                reencoded.append({'clip': new_clip['id'], 'index': new['index']})
            old['byte_digest'] = new['byte_digest']
    require_equal(comparable, expected_metadata, 'ATLAS_METADATA_STALE')
    round_trip(output / 'atlas.png', atlas, expected_metadata, builds)
    require_equal(read_json(output / 'export.qa.json'), export_qa(actual_metadata), 'EXPORT_QA_STALE')
    if {p.name for p in output.iterdir()} != EXPORT_FILES:
        raise ContractViolation('EXPORT_CONTENTS_MISMATCH', 'Export contains undeclared or missing files.')
    recheck(before)
    ensure_complete(output)
    return {'valid': True, 'success': True, 'output': str(output),
            'clip_count': len(builds), 'frame_count': sum(c['frame_count'] for c in expected_metadata['clips']),
            'clips': [{'id': c['id'], 'backend': c['backend'], 'mode': c['mode']} for c in expected_metadata['clips']],
            'reencoded_frames': reencoded, 'checks': export_qa(actual_metadata)['checks'], 'errors': [], 'warnings': []}
