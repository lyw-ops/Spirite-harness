"""Bounded input snapshots and reversible whole-directory publication."""
from contextlib import contextmanager
import os
from pathlib import Path
import shutil
import stat

from .contracts import ContractViolation, byte_digest
from .processing import ProcessingError


def reject_links(path):
    for part in (path, *path.parents):
        if part.is_symlink():
            raise ProcessingError('OUTPUT_CONFLICT', 'Symbolic link paths are not allowed.', path=str(part))


def snapshot(paths):
    result = {}
    for path in set(Path(p) for p in paths):
        if not path.exists() and not path.is_symlink():
            result[path] = None
            continue
        info = path.stat()
        if not stat.S_ISREG(info.st_mode):
            raise ContractViolation('INPUT_NOT_REGULAR', 'Snapshot input must be a regular file.', path=str(path))
        result[path] = (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns,
                        byte_digest(path.read_bytes()))
    return result


def recheck(before):
    if snapshot(before) != before:
        raise ContractViolation('INPUT_CHANGED', 'Input identity changed during the operation; publication cancelled.')


def guard_directory(output, inputs, allowed, overwrite):
    reject_links(output)
    target = output.resolve()
    for source in inputs:
        if source.resolve().is_relative_to(target):
            raise ProcessingError('OUTPUT_OVERLAPS_SOURCE', 'Output contains an immutable input.', path=str(source))
    if output.exists():
        if not output.is_dir():
            raise ProcessingError('OUTPUT_CONFLICT', 'Output must be a directory.')
        entries = list(output.rglob('*'))
        for entry in entries:
            relative = entry.relative_to(output).as_posix()
            if entry.is_symlink() or not (entry.is_dir() or entry.is_file()):
                raise ProcessingError('OUTPUT_CONFLICT', 'Nonregular output entry.', path=str(entry))
            if entry.is_dir():
                if not any(name.startswith(relative + '/') for name in allowed):
                    raise ProcessingError('OUTPUT_CONFLICT', 'Unknown output directory; nothing removed.', path=str(entry))
            elif relative not in allowed:
                raise ProcessingError('OUTPUT_CONFLICT', 'Unknown output file; nothing removed.', path=str(entry))
            elif any(p.is_file() and entry.samefile(p) for p in inputs):
                raise ProcessingError('OUTPUT_OVERLAPS_SOURCE', 'Output aliases immutable input.', path=str(entry))
        if entries and not overwrite:
            raise ProcessingError('OUTPUT_EXISTS', 'Output exists; use --overwrite for declared artifacts.')


@contextmanager
def transaction(marker, kind):
    reject_links(marker)
    try:
        marker.mkdir()
    except FileExistsError as exc:
        raise ProcessingError(kind + '_TRANSACTION_INCOMPLETE', 'A writer is active or recovery is required.') from exc
    preserve = False
    try:
        yield marker
    except ProcessingError as exc:
        preserve = exc.code.endswith('_RECOVERY_REQUIRED')
        raise
    finally:
        if not preserve:
            try:
                shutil.rmtree(marker)
            except OSError as exc:
                raise ProcessingError(kind + '_RECOVERY_REQUIRED', 'Cleanup failed; preserve the recovery directory.') from exc


def publish_directory(staged, output, marker, kind):
    moves = []
    try:
        if output.exists():
            os.replace(output, marker / 'previous')
            moves.append((output, marker / 'previous'))
        os.replace(staged, output)
        moves.append((staged, output))
    except BaseException:
        try:
            for original, destination in reversed(moves):
                os.replace(destination, original)
        except BaseException as exc:
            raise ProcessingError(kind + '_RECOVERY_REQUIRED', 'Publication and rollback failed; recovery materials retained.') from exc
        raise
