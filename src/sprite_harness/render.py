"""Deterministic single-image and explicit layered renderer (milestones 2/3).

Renders ``build/frames/`` from a build directory's digest-verified inputs
(``plan.json``, ``frame-plan.json``, the bound source sprite) by applying the
per-frame whole-sprite pose — translate, rotate, uniform scale, opacity — as
specified in ``docs/renderer.md``. Writes are transactional: frames are staged
inside the build directory and committed only when every frame succeeded, and
the render manifest (``render.json``) is published last. A transaction marker
blocks consumers until commit or rollback finishes. The source image is never modified, and the
deterministic pipeline never consumes ``plan.seed``.
"""

from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Any

from PIL import Image, UnidentifiedImageError

from . import __version__
from .build import (
    RENDER_MANIFEST_FILENAME,
    RENDER_MANIFEST_VERSION,
    RENDER_TRANSACTION_DIRNAME,
    BuildArtifacts,
    validate_build_inputs,
)
from .expand import expand_plan, plan_digest
from .geometry import FramePose, sample_poses
from .layers import LayerScene, render_source_pose
from .plan import SPRITE_TARGET, resolved_anchor
from .processing import ProcessingError
from .qa import write_json_artifact
from .validator import ValidationIssue


def _declared_frame_names(build: BuildArtifacts) -> list[str]:
    """Frame file basenames recomputed from the trusted plan.

    Pre-render validation has already proven the frame plan on disk equals
    this recomputation, so the rendered files match its declared ``file``
    entries exactly.
    """

    expected = expand_plan(build.plan, build.normalized_plan)
    return [Path(frame["file"]).name for frame in expected["frames"]]


def _check_output_slot(
    build: BuildArtifacts, declared: list[str], *, overwrite: bool
) -> None:
    """Enforce the overwrite policy before any pixel work.

    Only the declared derived products (the frame plan's frame files plus
    ``render.json``) are ever replaced; unknown files in ``frames/`` are never
    deleted and abort the render instead.
    """

    frames_dir = build.frames_dir
    manifest_path = build.build_dir / RENDER_MANIFEST_FILENAME
    for path in (frames_dir, manifest_path):
        if path.is_symlink():
            raise ProcessingError(
                "FRAMES_DIR_CONFLICT",
                "Render output must not be a symbolic link.",
                paths=[str(path)],
            )
    if manifest_path.exists() and not manifest_path.is_file():
        raise ProcessingError(
            "FRAMES_DIR_CONFLICT", "render.json must be a regular file.",
            paths=[str(manifest_path)],
        )
    sources = build.protected_paths
    for source_path in sources:
        if (source_path.is_relative_to(frames_dir.resolve())
            or source_path == manifest_path.resolve()
            or (manifest_path.is_file() and manifest_path.samefile(source_path))):
            raise ProcessingError(
                "FRAMES_DIR_CONFLICT", "Render output overlaps or aliases an immutable input.",
                paths=[str(source_path)],
            )
    declared_set = set(declared)
    existing: list[str] = []
    if frames_dir.is_dir():
        extras = sorted(
            str(entry.relative_to(build.build_dir))
            for entry in frames_dir.iterdir()
            if entry.is_symlink() or not entry.is_file() or entry.name not in declared_set
        )
        if extras:
            raise ProcessingError(
                "FRAMES_DIR_CONFLICT",
                "frames/ contains files the frame plan does not declare; "
                "move them away — render never deletes unknown files.",
                paths=extras,
            )
        if sources:
            aliases = [str(entry) for entry in frames_dir.iterdir()
                       if any(entry.samefile(source_path) for source_path in sources)]
            if aliases:
                raise ProcessingError(
                    "FRAMES_DIR_CONFLICT", "Render output aliases the immutable source.",
                    paths=aliases,
                )
        existing = sorted(
            entry.name for entry in frames_dir.iterdir() if entry.name in declared_set
        )
    elif frames_dir.exists():
        raise ProcessingError(
            "FRAMES_DIR_CONFLICT",
            "frames is not a directory.",
            paths=[str(frames_dir)],
        )
    if (existing or manifest_path.is_file()) and not overwrite:
        raise ProcessingError(
            "FRAMES_ALREADY_RENDERED",
            "Build already has rendered output; pass --overwrite to replace "
            "the declared frame files and render manifest.",
            frames=len(existing),
            manifest=manifest_path.is_file(),
        )


def _publish_generation(build: BuildArtifacts, transaction: Path) -> None:
    """Publish directory + manifest with reversible renames under a fail-closed marker.

    If rollback itself fails, keep all recovery material and the marker; no
    consumer may treat the remaining files as an external full-motion build.
    """

    moves: list[tuple[Path, Path]] = []

    def move(source: Path, destination: Path) -> None:
        os.replace(source, destination)
        moves.append((source, destination))

    try:
        if build.frames_dir.exists():
            move(build.frames_dir, transaction / "previous-frames")
        manifest = build.build_dir / RENDER_MANIFEST_FILENAME
        if manifest.exists():
            move(manifest, transaction / "previous-render.json")
        move(transaction / "new-frames", build.frames_dir)
        move(transaction / "new-render.json", manifest)
    except BaseException as failure:
        try:
            for original, destination in reversed(moves):
                os.replace(destination, original)
        except BaseException as rollback_failure:
            raise ProcessingError(
                "RENDER_RECOVERY_REQUIRED",
                "Render publication and rollback failed; recovery files were preserved. "
                "Do not remove the transaction directory before restoring the previous output.",
                transaction=str(transaction),
                detail=str(failure),
                rollback_detail=str(rollback_failure),
            ) from rollback_failure
        raise


def _load_source(build: BuildArtifacts) -> Image.Image | LayerScene:
    if build.plan.layered:
        try:
            return LayerScene.load(build.plan)
        except (UnidentifiedImageError, OSError, ValueError) as exc:
            raise ProcessingError("RENDER_SOURCE_UNREADABLE", "A source layer became unreadable.", detail=str(exc)) from exc
    source_path = build.plan.resolved_source_path()
    if source_path is None:
        raise ProcessingError(
            "RENDER_SOURCE_REQUIRED",
            "Build binds no source image; there is nothing to transform.",
            build=str(build.build_dir),
        )
    try:
        with Image.open(source_path) as image:
            image.load()
            return image.convert("RGBA")
    except (UnidentifiedImageError, OSError, ValueError) as exc:
        # Unreachable after input validation, but never render from a
        # half-read source.
        raise ProcessingError(
            "RENDER_SOURCE_UNREADABLE",
            "Source image could not be read.",
            path=str(source_path),
            detail=str(exc),
        ) from exc


def _skipped_tracks(build: BuildArtifacts) -> list[dict[str, str]]:
    if build.plan.layered:
        return []
    return [
        {"track_id": track.track_id, "target": track.target, "motion": track.motion}
        for track in build.plan.tracks
        if track.target != SPRITE_TARGET
    ]


def render_build(
    build: BuildArtifacts,
    *,
    reduced_motion: bool = False,
    overwrite: bool = False,
    generated_input: bool = False,
) -> dict[str, Any]:
    """Render the build's frame set; returns a JSON-ready result payload.

    Raises :class:`ProcessingError` for renderer preconditions and output
    failures; returns ``success: False`` with the validation issues when the
    build's inputs do not validate.
    """

    from .transactions import snapshot, recheck
    from .generation import load_generation
    from .layers import ReplacementScene
    generation_marker = build.build_dir / '.generation-transaction'
    if generation_marker.exists() or generation_marker.is_symlink():
        raise ProcessingError('GENERATION_TRANSACTION_INCOMPLETE', 'Generation is active or needs recovery.')
    before = snapshot(build.protected_paths)
    result, checks = validate_build_inputs(build)
    if not result.valid:
        return {
            "success": False,
            "build": str(build.build_dir),
            "animation_id": build.animation_id,
            "checks": checks,
            **result.as_dict(),
        }

    plan = build.plan
    transaction = build.build_dir / RENDER_TRANSACTION_DIRNAME
    if transaction.exists() or transaction.is_symlink():
        raise ProcessingError(
            "RENDER_TRANSACTION_INCOMPLETE",
            "A render transaction is active or needs recovery; output was not changed.",
            transaction=str(transaction),
        )
    if plan.background.casefold() != "transparent":
        raise ProcessingError(
            "UNSUPPORTED_BACKGROUND",
            "The built-in renderer only renders transparent backgrounds.",
            actual=plan.background,
        )

    declared = _declared_frame_names(build)
    _check_output_slot(build, declared, overwrite=overwrite)
    source = _load_source(build)
    binding = None
    if generated_input:
        images, binding = load_generation(build)
        source = ReplacementScene(source, images)

    mode = plan.reduced_motion if reduced_motion else "full"
    canvas = build.normalized_plan["canvas"]
    canvas_size = (canvas["width"], canvas["height"])
    anchor = resolved_anchor(plan)
    poses = sample_poses(plan)

    frames_dir = build.frames_dir
    manifest_path = build.build_dir / RENDER_MANIFEST_FILENAME
    try:
        transaction.mkdir()
    except FileExistsError as exc:
        raise ProcessingError(
            "RENDER_TRANSACTION_INCOMPLETE", "Another render owns the output slot.",
            transaction=str(transaction),
        ) from exc
    staging = transaction / "new-frames"
    preserve_recovery = False
    try:
        staging.mkdir()
        if mode == "hold_first_frame":
            first = staging / declared[0]
            _render_frame(source, poses[0], canvas_size, anchor, first)
            for name in declared[1:]:
                shutil.copyfile(first, staging / name)
        else:
            for pose, name in zip(poses, declared):
                _render_frame(source, pose, canvas_size, anchor, staging / name)

        write_json_artifact(
            transaction / "new-render.json",
            {
                "render_version": 2 if generated_input else RENDER_MANIFEST_VERSION,
                **({"backend": "generated-input", "generation": binding} if generated_input else {}),
                "animation_id": plan.animation_id,
                "generated_by": f"sprite-harness {__version__}",
                "plan_digest": plan_digest(build.normalized_plan),
                "mode": mode,
            },
        )
        recheck(before)
        # Recheck after rendering in case the output slot changed while staging.
        _check_output_slot(build, declared, overwrite=overwrite)
        try:
            _publish_generation(build, transaction)
        except ProcessingError as exc:
            preserve_recovery = exc.code == "RENDER_RECOVERY_REQUIRED"
            raise
    finally:
        if not preserve_recovery:
            # Removing the marker is the final commit step. If cleanup fails,
            # validation stays fail-closed until the transaction is recovered.
            try:
                shutil.rmtree(transaction)
            except OSError as exc:
                raise ProcessingError(
                    "RENDER_RECOVERY_REQUIRED",
                    "Transaction cleanup failed; inspect the retained output and recovery directory.",
                    transaction=str(transaction), detail=str(exc),
                ) from exc

    warnings = [warning.as_dict() for warning in result.warnings]
    skipped = _skipped_tracks(build)
    if skipped:
        warnings.append(
            ValidationIssue(
                code="TARGET_TRACKS_SKIPPED",
                message=(
                    "Tracks targeting sprite parts were not rendered; the "
                    "milestone-2 renderer applies whole-sprite transforms only."
                ),
                context={"tracks": skipped},
            ).as_dict()
        )
    return {
        "success": True,
        "build": str(build.build_dir),
        "animation_id": build.animation_id,
        "mode": mode,
        "backend": "generated-input" if generated_input else "deterministic",
        "frame_count": len(declared),
        "frames_dir": str(frames_dir),
        "render_manifest": str(manifest_path),
        "skipped_tracks": skipped,
        "checks": checks,
        "errors": [],
        "warnings": warnings,
    }


def _render_frame(
    source: Image.Image | LayerScene,
    pose: FramePose,
    canvas_size: tuple[int, int],
    anchor: tuple[float, float],
    path: Path,
) -> None:
    frame = render_source_pose(source, pose, canvas_size, anchor)
    if frame.getchannel("A").getbbox() is None:
        raise ProcessingError(
            "RENDERED_FRAME_EMPTY",
            "The composed frame has no visible pixels (extreme scaling or "
            "clipping); refusing to write output that cannot validate.",
            frame=path.name,
            index=pose.index,
        )
    frame.save(path, format="PNG")
