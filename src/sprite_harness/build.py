"""Build-directory creation, loading, and validation.

A build directory is the artifact contract produced by ``sprite-harness plan``:

```text
build/
  plan.json         # normalized Animation Plan
  frame-plan.json   # deterministic per-frame transform table
  qa/plan.qa.json   # QA report for the plan stage
  frames/           # renderer output (later milestones); frame_000.png ...
  preview.gif       # optional preview artifacts
  contact-sheet.png
```

Validation of a build directory checks the plan, the binding between plan and
frame plan, and — when ``frames/`` exists — the rendered frames themselves.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

from PIL import Image, UnidentifiedImageError

from . import __version__
from .expand import FRAME_PLAN_VERSION, expand_plan, normalize_plan, plan_digest
from .geometry import sample_poses
from .layers import LayerScene, render_source_pose
from .jsonio import dumps_strict
from .plan import AnimationPlan, Layer, load_plan, resolved_anchor
from .plan_validator import validate_plan
from .processing import ProcessingError, ensure_safe_build_output
from .qa import build_qa_report, qa_report_path, write_json_artifact
from .spec import AnimationSpec, FrameSpec, SpecLoadError
from .validator import ValidationIssue, ValidationResult


PLAN_FILENAME = "plan.json"
FRAME_PLAN_FILENAME = "frame-plan.json"
FRAMES_DIRNAME = "frames"
BBOX_TOLERANCE_PX = 2.0

# Render manifest (docs/renderer.md): written by `sprite-harness render` after
# a complete frame set, binding the frames to a plan revision and a motion mode.
RENDER_MANIFEST_FILENAME = "render.json"
RENDER_MANIFEST_VERSION = 1
RENDER_TRANSACTION_DIRNAME = ".render-transaction"
RENDER_MODES = ("full", "hold_first_frame")
RENDER_MANIFEST_KEYS = frozenset(
    {"render_version", "animation_id", "generated_by", "plan_digest", "mode"}
)

# Every authoritative top-level frame-plan field; anything else is unknown.
FRAME_PLAN_KEYS = frozenset(
    {
        "frame_plan_version",
        "animation_id",
        "generated_by",
        "plan_digest",
        "source",
        "playback",
        "canvas",
        "anchor",
        "reduced_motion",
        "frames",
    }
)
GENERATED_BY_PATTERN = re.compile(r"^sprite-harness \S+$")

# Frame-plan sections recomputed from the trusted plan and compared verbatim.
RECOMPUTED_SECTIONS = ("playback", "canvas", "anchor", "reduced_motion", "frames")


def _issue(code: str, message: str, **context: Any) -> ValidationIssue:
    return ValidationIssue(code=code, message=message, context=context)


def is_build_dir(path: Path) -> bool:
    return path.is_dir() and (path / FRAME_PLAN_FILENAME).is_file()


@dataclass(frozen=True)
class BuildArtifacts:
    build_dir: Path
    plan: AnimationPlan
    normalized_plan: dict[str, Any]
    frame_plan: dict[str, Any]

    @property
    def frames_dir(self) -> Path:
        return self.build_dir / FRAMES_DIRNAME

    @property
    def protected_paths(self) -> tuple[Path, ...]:
        from .generation import generation_paths
        return (*self.plan.protected_paths(), self.build_dir / FRAME_PLAN_FILENAME,
                *generation_paths(self))

    @property
    def animation_id(self) -> str:
        return str(self.frame_plan.get("animation_id", self.plan.animation_id))


# ---------------------------------------------------------------------------
# Source inspection


def inspect_source(
    source_path: Path, *, background: str, require_png: bool = False
) -> tuple[dict[str, Any] | None, list[ValidationIssue]]:
    """Read-only inspection of the source sprite; never modifies the file."""

    issues: list[ValidationIssue] = []
    if not source_path.is_file():
        issues.append(
            _issue("SOURCE_NOT_FOUND", "Source image does not exist.", path=str(source_path))
        )
        return None, issues
    try:
        with Image.open(source_path) as image:
            image.load()
            width, height = image.size
            image_format = image.format
            has_alpha = image.mode in {"RGBA", "LA"} or (
                image.mode == "P" and "transparency" in image.info
            )
    except (UnidentifiedImageError, OSError, ValueError) as exc:
        issues.append(
            _issue(
                "SOURCE_INVALID_IMAGE",
                "Source file is not a readable image.",
                path=str(source_path),
                detail=str(exc),
            )
        )
        return None, issues
    if require_png and image_format != "PNG":
        issues.append(_issue("SOURCE_PNG_REQUIRED", "Layer sources must be PNG images.", path=str(source_path)))
    if (require_png or background.casefold() == "transparent") and not has_alpha:
        issues.append(
            _issue(
                "SOURCE_ALPHA_REQUIRED",
                "A transparent canvas requires a source image with an alpha channel.",
                path=str(source_path),
            )
        )
    digest = hashlib.sha256(source_path.read_bytes()).hexdigest()
    return {"sha256": f"sha256:{digest}", "width": width, "height": height}, issues


def _compare_source_identity(
    plan: AnimationPlan | Layer, source_stats: dict[str, Any], source_path: Path
) -> list[ValidationIssue]:
    """Compare a plan's declared source identity against the inspected file."""

    issues: list[ValidationIssue] = []
    if plan.source_sha256 is not None and plan.source_sha256 != source_stats["sha256"]:
        issues.append(
            _issue(
                "SOURCE_DIGEST_MISMATCH",
                "Source file content does not match the declared SHA-256.",
                path=str(source_path),
                expected=plan.source_sha256,
                actual=source_stats["sha256"],
            )
        )
    declared = (plan.source_width, plan.source_height)
    actual = (source_stats["width"], source_stats["height"])
    if any(
        expected is not None and expected != measured
        for expected, measured in zip(declared, actual)
    ):
        issues.append(
            _issue(
                "SOURCE_DIMENSION_MISMATCH",
                "Source image dimensions do not match the declared width/height.",
                path=str(source_path),
                expected=list(declared),
                actual=list(actual),
            )
        )
    return issues


def _inspect_layers(plan: AnimationPlan, *, require_identity: bool = False) -> tuple[list[dict], list[ValidationIssue]]:
    stats_list = []
    errors = []
    for layer in plan.layers or ():
        path = (plan.spec_dir / layer.source_image).resolve()
        stats, issues = inspect_source(path, background=plan.background, require_png=True)
        if require_identity and any(value is None for value in
                (layer.source_sha256, layer.source_width, layer.source_height)):
            issues.append(_issue("INVALID_SOURCE_IDENTITY", "Normalized layers require SHA-256 and dimensions."))
        if stats is not None:
            issues.extend(_compare_source_identity(layer, stats, path))
        errors.extend(replace(issue, context={**issue.context, "target": layer.target}) for issue in issues)
        stats_list.append(stats)
    return stats_list, errors


# ---------------------------------------------------------------------------
# Build creation (the `plan` command)


def create_build(
    plan: AnimationPlan,
    output_dir: Path,
    *,
    source_override: Path | None = None,
) -> dict[str, Any]:
    """Normalize, validate, and expand a plan into a build directory.

    Returns a JSON-ready payload. Nothing is written when validation fails.
    """

    if plan.layered and source_override is not None:
        raise SpecLoadError("SOURCE_MODE_CONFLICT", "--source cannot be combined with source.layers.", path=plan.spec_path)
    result = validate_plan(plan)
    errors = list(result.errors)
    warnings = list(result.warnings)

    source_path = plan.resolved_source_path(source_override)
    source_stats: dict[str, Any] | None = None
    if source_path is not None:
        source_stats, source_issues = inspect_source(source_path, background=plan.background)
        errors.extend(source_issues)
        if source_stats is not None:
            errors.extend(_compare_source_identity(plan, source_stats, source_path))

    layer_sources, layer_errors = _inspect_layers(plan)
    errors.extend(layer_errors)
    canvas: tuple[int, int] | None = None
    if plan.canvas_width is not None and plan.canvas_height is not None:
        canvas = (plan.canvas_width, plan.canvas_height)
        if source_stats is not None and (source_stats["width"], source_stats["height"]) != canvas:
            warnings.append(
                _issue(
                    "CANVAS_SOURCE_MISMATCH",
                    "Source image dimensions differ from the declared canvas; "
                    "rendering will require anchor-based placement.",
                    canvas=list(canvas),
                    source=[source_stats["width"], source_stats["height"]],
                )
            )
    elif plan.layered:
        canvas = (plan.reference_width, plan.reference_height)
    elif source_stats is not None:
        canvas = (source_stats["width"], source_stats["height"])
    else:
        errors.append(
            _issue(
                "CANVAS_UNRESOLVED",
                "Plan declares no canvas and no source image; the canvas cannot be resolved.",
            )
        )

    combined = ValidationResult(errors=tuple(errors), warnings=tuple(warnings))
    if not combined.valid:
        return {"success": False, "animation_id": plan.animation_id, **combined.as_dict()}

    if output_dir.expanduser().is_symlink():
        raise ProcessingError("OUTPUT_OVERLAPS_SOURCE", "Build output must not be a symbolic link.")
    output = output_dir.expanduser().resolve()
    if output.is_file():
        raise ProcessingError(
            "OUTPUT_NOT_A_DIRECTORY", "Build output must be a directory.", output=str(output)
        )
    protected = {plan.spec_dir.resolve()}
    if source_path is not None:
        protected.add(source_path.parent)
    protected.update((plan.spec_dir / layer.source_image).resolve().parent for layer in plan.layers or ())
    if output in protected:
        raise ProcessingError(
            "OUTPUT_OVERLAPS_SOURCE",
            "Build output cannot be the directory holding the plan spec or source image.",
            output=str(output),
        )

    # The written plan.json records the source with a path that resolves from
    # its new location inside the build directory, plus the inspected identity
    # (sha256, dimensions) so the plan digest binds the source.
    plan_source: dict[str, Any] | None = None
    if source_path is not None and source_stats is not None:
        plan_source = {
            "image": os.path.relpath(source_path, output),
            "sha256": source_stats["sha256"],
            "width": source_stats["width"],
            "height": source_stats["height"],
        }

    if plan.layered:
        plan_source = normalize_plan(plan)["source"]
        for layer, stats, declared in zip(plan_source["layers"], layer_sources, plan.layers):
            layer.update(stats)
            layer["image"] = os.path.relpath((plan.spec_dir / declared.source_image).resolve(), output)
        # Check effective geometry with actual dimensions before writing artifacts.
        bound = replace(plan, canvas_width=canvas[0], canvas_height=canvas[1], layers=tuple(
            replace(layer, source_width=stats["width"], source_height=stats["height"])
            for layer, stats in zip(plan.layers, layer_sources)))
        bound_result = validate_plan(bound)
        if not bound_result.valid:
            return {"success": False, "animation_id": plan.animation_id, **bound_result.as_dict()}
    normalized = normalize_plan(plan, canvas=canvas, source=plan_source)
    frame_plan = expand_plan(plan, normalized)

    checks = [
        {"id": "plan_semantics", "status": "pass"},
        {"id": "source_inspected", "status": "pass" if plan_source else "skipped"},
        {"id": "canvas_resolved", "status": "pass"},
        {
            "id": "displacement_constraints",
            "status": "pass"
            if plan.max_displacement_px is not None or plan.max_frame_delta_px is not None
            else "skipped",
        },
        {"id": "expansion", "status": "pass"},
    ]
    qa_document = build_qa_report(
        stage="plan", animation_id=plan.animation_id, result=combined, checks=checks
    )

    plan_path = output / PLAN_FILENAME
    frame_plan_path = output / FRAME_PLAN_FILENAME
    qa_path = qa_report_path(output, "plan")
    inputs = (*plan.protected_paths(), *((source_path,) if source_path else ()))
    for target in (plan_path, frame_plan_path, qa_path):
        ensure_safe_build_output(inputs, target, output)
    write_json_artifact(plan_path, normalized)
    write_json_artifact(frame_plan_path, frame_plan)
    write_json_artifact(qa_path, qa_document)

    return {
        "success": True,
        "animation_id": plan.animation_id,
        "output_dir": str(output),
        "frame_count": plan.frame_count,
        "track_count": len(plan.tracks),
        "event_count": len(plan.events),
        "artifacts": {
            "plan": str(plan_path),
            "frame_plan": str(frame_plan_path),
            "qa_report": str(qa_path),
        },
        **combined.as_dict(),
    }


# ---------------------------------------------------------------------------
# Build loading and validation


def load_build(directory: str | Path) -> BuildArtifacts:
    build_dir = Path(directory).expanduser().resolve()
    frame_plan_path = build_dir / FRAME_PLAN_FILENAME
    plan_path = build_dir / PLAN_FILENAME
    if not frame_plan_path.is_file():
        raise SpecLoadError(
            "INPUT_NOT_FOUND", "Build directory has no frame-plan.json.", path=build_dir
        )
    if not plan_path.is_file():
        raise SpecLoadError(
            "INPUT_NOT_FOUND", "Build directory has no plan.json.", path=build_dir
        )
    try:
        frame_plan = json.loads(frame_plan_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SpecLoadError(
            "MALFORMED_SPEC", f"Frame plan is not valid JSON: {exc}", path=frame_plan_path
        ) from exc
    if not isinstance(frame_plan, dict):
        raise SpecLoadError(
            "MALFORMED_SPEC", "Frame plan root must be an object.", path=frame_plan_path
        )
    plan = load_plan(plan_path)
    # Canvas fallback comes from the trusted plan's declared source dimensions,
    # never from the untrusted frame plan under validation.
    canvas = None
    if (
        plan.canvas_width is None
        and plan.source_width is not None
        and plan.source_height is not None
    ):
        canvas = (plan.source_width, plan.source_height)
    normalized = normalize_plan(plan, canvas=canvas)
    return BuildArtifacts(
        build_dir=build_dir, plan=plan, normalized_plan=normalized, frame_plan=frame_plan
    )


def validate_build_inputs(
    build: BuildArtifacts, *, include_generation: bool = True,
) -> tuple[ValidationResult, list[dict[str, Any]]]:
    """Validate everything rendering depends on: plan, source, frame plan.

    Deliberately excludes checks on previously rendered frames so broken or
    stale derived output never blocks a safe re-render, while a tampered plan,
    source, or frame plan always does.
    """

    errors: list[ValidationIssue] = []
    warnings: list[ValidationIssue] = []
    checks: list[dict[str, Any]] = []

    plan_result = validate_plan(build.plan)
    errors.extend(plan_result.errors)
    warnings.extend(plan_result.warnings)
    checks.append({"id": "plan_semantics", "status": "pass" if plan_result.valid else "fail"})

    try:
        current = load_build(build.build_dir)
        if (_canonical(current.normalized_plan) != _canonical(build.normalized_plan)
                or _canonical(current.frame_plan) != _canonical(build.frame_plan)):
            errors.append(_issue('INPUT_CHANGED', 'Loaded build descriptions differ from the current files.'))
    except SpecLoadError as exc:
        errors.append(_issue(exc.code, exc.message))
    source_status = _validate_source(build, errors)
    checks.append({"id": "source_identity", "status": source_status})

    consistent = _validate_frame_plan(build, errors, warnings)
    checks.append({"id": "frame_plan_consistency", "status": "pass" if consistent else "fail"})

    if include_generation and not errors:
        from .generation import load_generation
        from .contracts import ContractViolation
        marker = build.build_dir / '.generation-transaction'
        if marker.exists() or marker.is_symlink():
            errors.append(_issue('GENERATION_TRANSACTION_INCOMPLETE', 'Generation transaction requires recovery.'))
        elif (build.build_dir / 'generation').exists() or (build.build_dir / 'generation').is_symlink():
            try:
                load_generation(build)
                checks.append({'id': 'generation_inputs', 'status': 'pass'})
            except (SpecLoadError, ProcessingError) as exc:
                errors.append(_issue(exc.code, exc.message))
                checks.append({'id': 'generation_inputs', 'status': 'fail'})
    return ValidationResult(errors=tuple(errors), warnings=tuple(warnings)), checks


def _validate_build(build: BuildArtifacts) -> tuple[ValidationResult, list[dict[str, Any]]]:
    transaction = build.build_dir / RENDER_TRANSACTION_DIRNAME
    if transaction.exists() or transaction.is_symlink():
        return ValidationResult(errors=(
            _issue(
                "RENDER_TRANSACTION_INCOMPLETE",
                "A render transaction is active or interrupted; recover it before validation.",
                transaction=str(transaction),
            ),
        )), [{"id": "render_transaction", "status": "fail"}]
    result, checks = validate_build_inputs(build)
    errors = list(result.errors)
    warnings = list(result.warnings)

    if not result.valid:
        checks.append({"id": "frame_files", "status": "skipped"})
        return result, checks
    manifest_path = build.build_dir / RENDER_MANIFEST_FILENAME
    if (build.frames_dir.exists() or build.frames_dir.is_symlink()
            or manifest_path.exists() or manifest_path.is_symlink()):
        mode, manifest_status = _validate_render_manifest(build, manifest_path, errors, warnings)
        checks.append({"id": "render_manifest", "status": manifest_status})
        frame_errors, frame_warnings = _validate_frames(
            build, mode=mode, verify_pixels=manifest_status == "pass"
        )
        errors.extend(frame_errors)
        warnings.extend(frame_warnings)
        checks.append({"id": "frame_files", "status": "pass" if not frame_errors else "fail"})
    else:
        checks.append({"id": "frame_files", "status": "skipped"})

    if transaction.exists() or transaction.is_symlink():
        errors.append(_issue(
            "RENDER_TRANSACTION_INCOMPLETE", "Output changed during validation; retry after recovery.",
            transaction=str(transaction),
        ))

    return ValidationResult(errors=tuple(errors), warnings=tuple(warnings)), checks


def _canonical(value: Any) -> str:
    """Canonical strict-JSON form; distinguishes 1 from 1.0 and True from 1."""

    return dumps_strict(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _validate_source(build: BuildArtifacts, errors: list[ValidationIssue]) -> str:
    """Re-inspect the source image and compare it with the digest-bound identity."""

    plan = build.plan
    if plan.layered:
        _, issues = _inspect_layers(plan, require_identity=True)
        errors.extend(issues)
        return "fail" if issues else "pass"
    if plan.source_image is None:
        return "skipped"
    before = len(errors)
    source_path = plan.resolved_source_path()
    source_stats, issues = inspect_source(source_path, background=plan.background)
    errors.extend(issues)
    if source_stats is not None:
        errors.extend(_compare_source_identity(plan, source_stats, source_path))
    return "pass" if len(errors) == before else "fail"


def _validate_frame_plan(
    build: BuildArtifacts,
    errors: list[ValidationIssue],
    warnings: list[ValidationIssue],
) -> bool:
    """Verify the entire frame-plan document against a trusted recomputation.

    Nothing in the frame plan under test feeds the recomputation: the expected
    document is derived from ``plan.json`` alone (loaded, validated, and
    re-expanded), then compared section by section in canonical JSON form so
    changed values, changed types, and added/removed fields all fail.
    """

    frame_plan = build.frame_plan
    before = len(errors)

    unknown = sorted(str(key) for key in set(frame_plan) - FRAME_PLAN_KEYS)
    if unknown:
        errors.append(
            _issue(
                "MALFORMED_FRAME_PLAN",
                "Frame plan contains unknown top-level fields.",
                fields=unknown,
            )
        )
    missing = sorted(FRAME_PLAN_KEYS - set(frame_plan))
    if missing:
        errors.append(
            _issue(
                "MALFORMED_FRAME_PLAN",
                "Frame plan is missing required top-level fields.",
                fields=missing,
            )
        )

    version = frame_plan.get("frame_plan_version")
    expected_version = 2 if build.plan.layered else FRAME_PLAN_VERSION
    if "frame_plan_version" in frame_plan and (type(version) is not int or version != expected_version):
        errors.append(
            _issue(
                "UNSUPPORTED_FRAME_PLAN_VERSION",
                "Frame plan version is not supported.",
                actual=version,
                supported=[expected_version],
            )
        )
        return False

    generated_by = frame_plan.get("generated_by")
    if "generated_by" in frame_plan:
        if not isinstance(generated_by, str) or not GENERATED_BY_PATTERN.match(generated_by):
            errors.append(
                _issue(
                    "MALFORMED_FRAME_PLAN",
                    "Frame plan 'generated_by' must be a 'sprite-harness <version>' string.",
                    actual=generated_by,
                )
            )
        elif generated_by != f"sprite-harness {__version__}":
            # Provenance is informational, not digest-bound: builds stay
            # validatable across harness releases.
            warnings.append(
                _issue(
                    "GENERATED_BY_MISMATCH",
                    "Frame plan was generated by a different harness release.",
                    actual=generated_by,
                    current=f"sprite-harness {__version__}",
                )
            )

    if frame_plan.get("animation_id") != build.plan.animation_id:
        errors.append(
            _issue(
                "ANIMATION_ID_MISMATCH",
                "Frame plan and plan disagree on the animation id.",
                plan=build.plan.animation_id,
                frame_plan=frame_plan.get("animation_id"),
            )
        )

    expected_digest = plan_digest(build.normalized_plan)
    if frame_plan.get("plan_digest") != expected_digest:
        errors.append(
            _issue(
                "PLAN_DIGEST_MISMATCH",
                "Frame plan was generated from a different plan revision.",
                expected=expected_digest,
                actual=frame_plan.get("plan_digest"),
            )
        )

    frames = frame_plan.get("frames")
    if not isinstance(frames, list):
        errors.append(_issue("MALFORMED_FRAME_PLAN", "Frame plan 'frames' must be an array."))
        return False
    if len(frames) != build.plan.frame_count:
        errors.append(
            _issue(
                "FRAME_PLAN_COUNT_MISMATCH",
                "Frame plan frame count does not match the plan.",
                expected=build.plan.frame_count,
                actual=len(frames),
            )
        )
    indices = [frame.get("index") for frame in frames if isinstance(frame, dict)]
    if indices != list(range(len(frames))):
        errors.append(
            _issue(
                "FRAME_PLAN_INDEX_GAP",
                "Frame plan indices must be contiguous starting at zero.",
                actual=indices,
            )
        )

    # A full deterministic recomputation of the document from the trusted plan
    # catches every hand-edited value: playback, canvas, anchor, reduced
    # motion, source binding, transforms, offsets, events, files, and types.
    if validate_plan(build.plan).valid:
        expected = expand_plan(build.plan, build.normalized_plan)
        if _canonical(expected["source"]) != _canonical(frame_plan.get("source")):
            errors.append(
                _issue(
                    "FRAME_PLAN_SOURCE_MISMATCH",
                    "Frame plan source binding does not match the plan's source identity.",
                    expected=expected["source"],
                    actual=frame_plan.get("source"),
                )
            )
        for section in RECOMPUTED_SECTIONS:
            if _canonical(expected[section]) == _canonical(frame_plan.get(section)):
                continue
            context: dict[str, Any] = {"section": section}
            if section == "frames":
                context["first_mismatch_index"] = next(
                    (
                        index
                        for index, frame in enumerate(expected[section])
                        if index >= len(frames)
                        or _canonical(frame) != _canonical(frames[index])
                    ),
                    min(len(frames), len(expected[section])),
                )
            else:
                context["expected"] = expected[section]
                context["actual"] = frame_plan.get(section)
            errors.append(
                _issue(
                    "FRAME_PLAN_STALE",
                    "Frame plan content does not match a deterministic "
                    "re-expansion of the plan.",
                    **context,
                )
            )
    return len(errors) == before


def _validate_render_manifest(
    build: BuildArtifacts,
    manifest_path: Path,
    errors: list[ValidationIssue],
    warnings: list[ValidationIssue],
) -> tuple[str, str]:
    """Validate ``render.json`` and return (effective mode, check status).

    An absent manifest means an externally rendered frame set and is judged as
    full motion (backward compatible with pre-renderer builds).
    """

    if manifest_path.is_symlink() or (
        manifest_path.exists() and not manifest_path.is_file()
    ):
        errors.append(_issue(
            "MALFORMED_RENDER_MANIFEST", "Render manifest must be a regular, non-symlink file.",
            path=str(manifest_path),
        ))
        return "full", "fail"
    if not manifest_path.is_file():
        if (build.build_dir / 'generation').exists():
            errors.append(_issue('GENERATED_RENDER_MANIFEST_REQUIRED', 'Generated builds with frames require an explicit render manifest.'))
            return 'full', 'fail'
        return "full", "skipped"
    before = len(errors)
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(
            _issue(
                "MALFORMED_RENDER_MANIFEST",
                "Render manifest is not valid JSON.",
                path=str(manifest_path),
                detail=str(exc),
            )
        )
        return "full", "fail"
    if not isinstance(manifest, dict):
        errors.append(
            _issue(
                "MALFORMED_RENDER_MANIFEST",
                "Render manifest root must be an object.",
                path=str(manifest_path),
            )
        )
        return "full", "fail"

    generated = type(manifest.get('render_version')) is int and manifest.get('render_version') == 2 and manifest.get('backend') == 'generated-input'
    manifest_keys = RENDER_MANIFEST_KEYS | {'backend', 'generation'} if generated else RENDER_MANIFEST_KEYS
    if generated:
        from .generation import load_generation
        from .contracts import require_equal
        try:
            _, binding = load_generation(build)
            require_equal(manifest.get('generation'), binding, 'RENDER_GENERATION_STALE')
        except (SpecLoadError, ProcessingError) as exc:
            errors.append(_issue(exc.code, exc.message))
    unknown = sorted(str(key) for key in set(manifest) - manifest_keys)
    if unknown:
        errors.append(
            _issue(
                "MALFORMED_RENDER_MANIFEST",
                "Render manifest contains unknown fields.",
                fields=unknown,
            )
        )
    missing = sorted(manifest_keys - set(manifest))
    if missing:
        errors.append(
            _issue(
                "MALFORMED_RENDER_MANIFEST",
                "Render manifest is missing required fields.",
                fields=missing,
            )
        )

    version = manifest.get("render_version")
    if "render_version" in manifest and type(version) is not int:
        errors.append(_issue(
            "MALFORMED_RENDER_MANIFEST", "render_version must be an integer, not a boolean or string.",
            actual=version,
        ))
    elif "render_version" in manifest and version != RENDER_MANIFEST_VERSION and not generated:
        errors.append(
            _issue(
                "UNSUPPORTED_RENDER_MANIFEST_VERSION",
                "Render manifest version is not supported.",
                actual=version,
                supported=[RENDER_MANIFEST_VERSION],
            )
        )

    generated_by = manifest.get("generated_by")
    if "generated_by" in manifest:
        if not isinstance(generated_by, str) or not GENERATED_BY_PATTERN.match(generated_by):
            errors.append(
                _issue(
                    "MALFORMED_RENDER_MANIFEST",
                    "Render manifest 'generated_by' must be a "
                    "'sprite-harness <version>' string.",
                    actual=generated_by,
                )
            )
        elif generated_by != f"sprite-harness {__version__}":
            warnings.append(
                _issue(
                    "GENERATED_BY_MISMATCH",
                    "Render manifest was generated by a different harness release.",
                    artifact=RENDER_MANIFEST_FILENAME,
                    actual=generated_by,
                    current=f"sprite-harness {__version__}",
                )
            )

    if "animation_id" in manifest and manifest.get("animation_id") != build.plan.animation_id:
        errors.append(
            _issue(
                "ANIMATION_ID_MISMATCH",
                "Render manifest and plan disagree on the animation id.",
                plan=build.plan.animation_id,
                render_manifest=manifest.get("animation_id"),
            )
        )

    expected_digest = plan_digest(build.normalized_plan)
    if "plan_digest" in manifest and manifest.get("plan_digest") != expected_digest:
        errors.append(
            _issue(
                "RENDER_MANIFEST_STALE",
                "Frames were rendered from a different plan revision.",
                expected=expected_digest,
                actual=manifest.get("plan_digest"),
            )
        )

    mode = manifest.get("mode")
    if "mode" in manifest and mode not in RENDER_MODES:
        errors.append(
            _issue(
                "MALFORMED_RENDER_MANIFEST",
                "Render manifest mode is not supported.",
                actual=mode,
                supported=list(RENDER_MODES),
            )
        )
        mode = "full"
    elif mode == "hold_first_frame" and build.plan.reduced_motion != "hold_first_frame":
        # The plan declares no reduced variant distinct from full motion, so a
        # hold render cannot be a faithful output of this plan.
        errors.append(
            _issue(
                "RENDER_MODE_MISMATCH",
                "Render manifest claims a reduced-motion mode the plan does not declare.",
                manifest_mode=mode,
                plan_reduced_motion=build.plan.reduced_motion,
            )
        )
    if not isinstance(mode, str) or mode not in RENDER_MODES:
        mode = "full"
    return mode, "pass" if len(errors) == before else "fail"


def _load_source_rgba(plan: AnimationPlan) -> Image.Image | LayerScene | None:
    """The trusted source sprite as RGBA, or None when it cannot be read.

    Read-only; identity errors are reported by the source_identity stage, so
    callers only need the pixels (for modeling expected geometry).
    """

    if plan.layered:
        try:
            return LayerScene.load(plan)
        except (UnidentifiedImageError, OSError, ValueError):
            return None
    source_path = plan.resolved_source_path()
    if source_path is None or not source_path.is_file():
        return None
    try:
        with Image.open(source_path) as image:
            image.load()
            return image.convert("RGBA")
    except (UnidentifiedImageError, OSError, ValueError):
        return None


def _validate_frames(
    build: BuildArtifacts,
    *,
    mode: str = "full",
    verify_pixels: bool = False,
) -> tuple[list[ValidationIssue], list[ValidationIssue]]:
    errors: list[ValidationIssue] = []
    warnings: list[ValidationIssue] = []
    if build.frames_dir.is_symlink() or (
        build.frames_dir.exists() and not build.frames_dir.is_dir()
    ):
        return [_issue(
            "FRAMES_DIR_CONFLICT", "frames must be a real directory inside the build.",
            path=str(build.frames_dir),
        )], warnings
    plan = build.plan
    frame_plan = expand_plan(plan, build.normalized_plan)
    canvas = frame_plan.get("canvas", {})
    expected_size = (
        (canvas.get("width"), canvas.get("height")) if isinstance(canvas, dict) else (None, None)
    )
    transparent = plan.background.casefold() == "transparent"
    pixel_source = None
    pixel_poses = []
    if verify_pixels and validate_plan(plan).valid:
        pixel_source = _load_source_rgba(plan)
        if pixel_source is None:
            errors.append(_issue(
                "FRAME_CONTENT_UNVERIFIED",
                "A built-in render manifest requires a readable bound source for pixel verification.",
            ))
        else:
            manifest = json.loads((build.build_dir / RENDER_MANIFEST_FILENAME).read_text())
            if manifest.get('backend') == 'generated-input':
                from .generation import load_generation
                from .layers import ReplacementScene
                images, _ = load_generation(build)
                pixel_source = ReplacementScene(pixel_source, images)
            pixel_poses = sample_poses(plan)
            if mode == "hold_first_frame" and pixel_poses:
                pixel_poses = [pixel_poses[0]] * len(pixel_poses)

    expected_files = [
        frame.get("file")
        for frame in frame_plan.get("frames", [])
        if isinstance(frame, dict) and isinstance(frame.get("file"), str)
    ]
    expected_set = {build.build_dir / file for file in expected_files}
    actual_files = sorted(build.frames_dir.glob("*.png"))
    for extra in actual_files:
        if extra not in expected_set:
            errors.append(
                _issue(
                    "UNEXPECTED_FRAME_FILE",
                    "Frame directory contains a file the frame plan does not declare.",
                    path=str(extra),
                )
            )

    bboxes: list[tuple[float, float, int] | None] = []  # (center_x, bottom, index)
    digests: list[str | None] = []
    for index, file in enumerate(expected_files):
        frame_path = build.build_dir / file
        if frame_path.is_symlink() or not frame_path.resolve().is_relative_to(build.build_dir):
            errors.append(_issue(
                "FRAME_PATH_OUTSIDE_BUILD",
                "Frame paths must stay inside the build and must not be symbolic links.",
                frame=file, index=index,
            ))
            bboxes.append(None)
            digests.append(None)
            continue
        if not frame_path.is_file():
            errors.append(
                _issue("FRAME_MISSING", "Frame file does not exist.", frame=file, index=index)
            )
            bboxes.append(None)
            digests.append(None)
            continue
        try:
            with Image.open(frame_path) as image:
                image.load()
                size = image.size
                has_alpha = image.mode in {"RGBA", "LA"} or (
                    image.mode == "P" and "transparency" in image.info
                )
                rgba = image.convert("RGBA")
                bbox = rgba.split()[-1].getbbox()
        except (UnidentifiedImageError, OSError, ValueError) as exc:
            errors.append(
                _issue(
                    "FRAME_INVALID_IMAGE",
                    "Frame file is not a readable image.",
                    frame=file,
                    index=index,
                    detail=str(exc),
                )
            )
            bboxes.append(None)
            digests.append(None)
            continue
        digests.append(hashlib.sha256(frame_path.read_bytes()).hexdigest())

        # Built-in renders promise deterministic RGBA content, not just a
        # matching silhouette. Recompute from trusted inputs, never from a
        # digest supplied by the output under test. External frame sets retain
        # their geometric contract and need not imitate this renderer.
        if pixel_source is not None and index < len(pixel_poses):
            trusted_canvas = build.normalized_plan.get("canvas", {})
            trusted_size = (trusted_canvas.get("width"), trusted_canvas.get("height"))
            if all(type(dimension) is int and dimension > 0 for dimension in trusted_size):
                expected_pixels = render_source_pose(
                    pixel_source, pixel_poses[index], trusted_size, resolved_anchor(plan)
                )
                if rgba.size != expected_pixels.size or rgba.tobytes() != expected_pixels.tobytes():
                    errors.append(_issue(
                        "FRAME_CONTENT_MISMATCH",
                        "Decoded RGBA pixels do not match the deterministic source transform.",
                        frame=file, index=index,
                    ))

        if expected_size != (None, None) and size != expected_size:
            errors.append(
                _issue(
                    "FRAME_DIMENSION_MISMATCH",
                    "Frame dimensions do not match the canvas.",
                    frame=file,
                    index=index,
                    expected=list(expected_size),
                    actual=list(size),
                )
            )
        if transparent and not has_alpha:
            errors.append(
                _issue(
                    "FRAME_ALPHA_REQUIRED",
                    "A transparent canvas requires frames with an alpha channel.",
                    frame=file,
                    index=index,
                )
            )
        if bbox is None:
            errors.append(
                _issue(
                    "FRAME_EMPTY",
                    "Frame contains no visible pixels.",
                    frame=file,
                    index=index,
                )
            )
            bboxes.append(None)
            continue
        left, top, right, bottom = bbox
        if left == 0 or top == 0 or right == size[0] or bottom == size[1]:
            warnings.append(
                _issue(
                    "CONTENT_TOUCHES_EDGE",
                    "Visible content touches the canvas edge; the sprite may be cropped.",
                    frame=file,
                    index=index,
                    bbox=[left, top, right, bottom],
                )
            )
        bboxes.append(((left + right) / 2.0, float(bottom), index))

    if mode == "hold_first_frame":
        # A hold_first_frame render keeps the declared frame count and file
        # names, so every frame must be byte-identical to the first one.
        reference = next((digest for digest in digests if digest is not None), None)
        for index, digest in enumerate(digests):
            if digest is not None and reference is not None and digest != reference:
                errors.append(
                    _issue(
                        "HOLD_FRAME_MISMATCH",
                        "hold_first_frame output frames must be byte-identical.",
                        frame=expected_files[index],
                        index=index,
                    )
                )

    _validate_geometry(build, mode, bboxes, errors, warnings, source_override=pixel_source)
    return errors, warnings


def _validate_geometry(
    build: BuildArtifacts,
    mode: str,
    bboxes: list[tuple[float, float, int] | None],
    errors: list[ValidationIssue],
    warnings: list[ValidationIssue],
    *, source_override=None,
) -> None:
    """Compare measured frame geometry against trusted expectations.

    Expectations come from the validated plan (recomputed poses) and, when
    rotation/scale/opacity are involved, from the trusted source image
    transformed through the documented pose geometry — never from the frames
    under test (docs/renderer.md).
    """

    plan = build.plan
    if not validate_plan(plan).valid:
        return  # No trusted geometry; plan errors are already reported.
    poses = sample_poses(plan)
    if mode == "hold_first_frame" and poses:
        poses = [poses[0]] * len(poses)
    if len(poses) != len(bboxes):
        return  # Count mismatch is reported by frame-plan consistency.

    source = source_override if source_override is not None else (_load_source_rgba(plan) if plan.source_image is not None or plan.layered else None)
    if source is None:
        # No trusted pixels to model against. Pure translations keep the
        # relative offset check; rotate/scale/opacity cannot be verified
        # honestly, so say so instead of guessing.
        if all(pose.is_translation_only for pose in poses):
            offsets = [(pose.dx, pose.dy) for pose in poses]
            _validate_drift(build, offsets, bboxes, errors)
        else:
            warnings.append(
                _issue(
                    "GEOMETRY_UNVERIFIED",
                    "Build uses rotate/scale/opacity but binds no readable source "
                    "image; bbox and ground checks were skipped instead of guessed.",
                    skipped_checks=["BBOX_DRIFT_EXCEEDED", "GROUND_DRIFT_EXCEEDED"],
                )
            )
        return

    canvas = build.normalized_plan.get("canvas", {})
    width = canvas.get("width") if isinstance(canvas, dict) else None
    height = canvas.get("height") if isinstance(canvas, dict) else None
    if not isinstance(width, int) or not isinstance(height, int):
        return
    anchor = resolved_anchor(plan)
    for box, pose in zip(bboxes, poses):
        if box is None:
            continue
        center, bottom, index = box
        expected = render_source_pose(source, pose, (width, height), anchor).getchannel("A").getbbox()
        if expected is None:
            errors.append(
                _issue(
                    "BBOX_DRIFT_EXCEEDED",
                    "Frame shows content where the modeled transform produces none.",
                    index=index,
                    expected_bbox=None,
                    actual_center_x=center,
                    tolerance=BBOX_TOLERANCE_PX,
                )
            )
            continue
        left, _top, right, expected_bottom = expected
        expected_center = (left + right) / 2.0
        if abs(center - expected_center) > BBOX_TOLERANCE_PX:
            errors.append(
                _issue(
                    "BBOX_DRIFT_EXCEEDED",
                    "Frame content drifts horizontally from the modeled transform.",
                    index=index,
                    expected_center_x=expected_center,
                    actual_center_x=center,
                    tolerance=BBOX_TOLERANCE_PX,
                )
            )
        if abs(bottom - float(expected_bottom)) > BBOX_TOLERANCE_PX:
            errors.append(
                _issue(
                    "GROUND_DRIFT_EXCEEDED",
                    "Frame ground line drifts from the modeled transform.",
                    index=index,
                    expected_bottom=float(expected_bottom),
                    actual_bottom=bottom,
                    tolerance=BBOX_TOLERANCE_PX,
                )
            )


def _validate_drift(
    build: BuildArtifacts,
    offsets: list[tuple[float, float]],
    bboxes: list[tuple[float, float, int] | None],
    errors: list[ValidationIssue],
) -> None:
    """Compare measured bounding boxes against the offsets the plan declares."""

    reference = next((box for box in bboxes if box is not None), None)
    if reference is None or len(offsets) != len(bboxes):
        return
    ref_center, ref_bottom, ref_index = reference
    ref_dx, ref_dy = offsets[ref_index]

    previous: tuple[float, float] | None = None
    plan = build.plan
    for box in bboxes:
        if box is None:
            previous = None
            continue
        center, bottom, index = box
        dx, dy = offsets[index]
        expected_center = ref_center + (dx - ref_dx)
        expected_bottom = ref_bottom + (dy - ref_dy)
        if abs(center - expected_center) > BBOX_TOLERANCE_PX:
            errors.append(
                _issue(
                    "BBOX_DRIFT_EXCEEDED",
                    "Frame content drifts horizontally beyond the planned offset.",
                    index=index,
                    expected_center_x=expected_center,
                    actual_center_x=center,
                    tolerance=BBOX_TOLERANCE_PX,
                )
            )
        if abs(bottom - expected_bottom) > BBOX_TOLERANCE_PX:
            errors.append(
                _issue(
                    "GROUND_DRIFT_EXCEEDED",
                    "Frame ground line drifts beyond the planned offset.",
                    index=index,
                    expected_bottom=expected_bottom,
                    actual_bottom=bottom,
                    tolerance=BBOX_TOLERANCE_PX,
                )
            )
        if previous is not None and plan.max_frame_delta_px is not None:
            delta = max(abs(center - previous[0]), abs(bottom - previous[1]))
            if delta > plan.max_frame_delta_px + BBOX_TOLERANCE_PX:
                errors.append(
                    _issue(
                        "FRAME_DELTA_EXCEEDED",
                        "Measured frame-to-frame movement exceeds the allowed delta.",
                        index=index,
                        delta=delta,
                        limit=plan.max_frame_delta_px,
                        tolerance=BBOX_TOLERANCE_PX,
                    )
                )
        previous = (center, bottom)


# ---------------------------------------------------------------------------
# Adapter for preview/contact-sheet reuse


def build_to_animation_spec(build: BuildArtifacts) -> AnimationSpec:
    """Present a rendered build directory as a frame-manifest animation."""

    if not build.frames_dir.is_dir():
        raise ProcessingError(
            "FRAMES_NOT_RENDERED",
            "Build directory has no frames/ yet; render frames before previewing.",
            build=str(build.build_dir),
        )
    frame_plan = build.frame_plan
    canvas = frame_plan.get("canvas", {})
    anchor = frame_plan.get("anchor", {})
    frames = tuple(
        FrameSpec(file=frame["file"], duration=1.0)
        for frame in frame_plan.get("frames", [])
        if isinstance(frame, dict) and isinstance(frame.get("file"), str)
    )
    return AnimationSpec(
        version=1,
        id=build.animation_id,
        character_id="-",
        state_id="-",
        canvas_width=int(canvas.get("width", 0)),
        canvas_height=int(canvas.get("height", 0)),
        background=str(canvas.get("background", "transparent")),
        anchor_x=float(anchor.get("x", 0.5)),
        anchor_y=float(anchor.get("y", 1.0)),
        fps=float(build.plan.fps),
        loop=build.plan.loop,
        frames=frames,
        spec_path=build.build_dir / FRAME_PLAN_FILENAME,
        animation_dir=build.build_dir,
    )


def validate_build(build: BuildArtifacts) -> tuple[ValidationResult, list[dict[str, Any]]]:
    from .transactions import snapshot, recheck
    from .contracts import ContractViolation
    paths = [*build.protected_paths, build.build_dir / 'render.json',
             *(build.build_dir / f'frames/frame_{i:03d}.png' for i in range(build.plan.frame_count))]
    try:
        before = snapshot(paths)
        result, checks = _validate_build(build)
        recheck(before)
        return result, checks
    except ContractViolation as exc:
        return ValidationResult(errors=(_issue(exc.code, exc.message),)), [{'id': 'input_stability', 'status': 'fail'}]
