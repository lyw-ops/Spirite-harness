"""Shared processing errors and output-path safety checks."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .spec import AnimationSpec


class ProcessingError(Exception):
    def __init__(self, code: str, message: str, **details: Any) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = details

    def as_error(self) -> dict[str, Any]:
        return {"code": self.code, "message": self.message, **self.details}


def ensure_safe_build_output(inputs: tuple[Path, ...], output: Path, build_dir: Path) -> None:
    """Guard a derived file against all bound artwork and description files."""
    # Check the output itself and its parents within the build before resolve(),
    # which would erase evidence of dangling or outward-pointing symlinks.
    for path in (output, *output.parents):
        if path == build_dir.parent:
            break
        if path.is_symlink():
            raise ProcessingError("OUTPUT_OVERLAPS_SOURCE", "Artifact output must not use symbolic links.", output=str(path))
    target = output.resolve()
    for source in inputs:
        if target == source.resolve() or (target.is_file() and source.is_file() and target.samefile(source)):
            raise ProcessingError("OUTPUT_OVERLAPS_SOURCE", "Artifact output aliases an immutable input.", output=str(output), source=str(source))


def ensure_safe_artifact_output(spec: AnimationSpec, output: Path) -> None:
    """Reject output locations that could overwrite or mix with source artwork."""

    target = output.resolve()
    if target == spec.spec_path.resolve():
        raise ProcessingError(
            "OUTPUT_OVERLAPS_SOURCE",
            "Generated artifact cannot overwrite the source specification.",
            output=str(target),
        )
    for frame in spec.frames:
        source = spec.frame_path(frame)
        source_directory = source.parent
        if target == source or source_directory == target.parent or source_directory in target.parents:
            raise ProcessingError(
                "OUTPUT_OVERLAPS_SOURCE",
                "Generated artifact cannot be written inside a source-artwork directory.",
                output=str(target),
                source=str(source),
            )
