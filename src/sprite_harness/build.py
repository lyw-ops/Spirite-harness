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
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from PIL import Image, UnidentifiedImageError

from .expand import FRAME_PLAN_VERSION, expand_plan, normalize_plan, plan_digest, sample_offsets
from .plan import AnimationPlan, load_plan
from .plan_validator import validate_plan
from .processing import ProcessingError
from .qa import build_qa_report, qa_report_path, write_json_artifact
from .spec import AnimationSpec, FrameSpec, SpecLoadError
from .validator import ValidationIssue, ValidationResult


PLAN_FILENAME = "plan.json"
FRAME_PLAN_FILENAME = "frame-plan.json"
FRAMES_DIRNAME = "frames"
BBOX_TOLERANCE_PX = 2.0


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
    def animation_id(self) -> str:
        return str(self.frame_plan.get("animation_id", self.plan.animation_id))


# ---------------------------------------------------------------------------
# Source inspection


def inspect_source(
    source_path: Path, *, background: str
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
    if background.casefold() == "transparent" and not has_alpha:
        issues.append(
            _issue(
                "SOURCE_ALPHA_REQUIRED",
                "A transparent canvas requires a source image with an alpha channel.",
                path=str(source_path),
            )
        )
    digest = hashlib.sha256(source_path.read_bytes()).hexdigest()
    return {"sha256": f"sha256:{digest}", "width": width, "height": height}, issues


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

    result = validate_plan(plan)
    errors = list(result.errors)
    warnings = list(result.warnings)

    source_path = plan.resolved_source_path(source_override)
    source_stats: dict[str, Any] | None = None
    if source_path is not None:
        source_stats, source_issues = inspect_source(source_path, background=plan.background)
        errors.extend(source_issues)

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

    output = output_dir.expanduser().resolve()
    if output.is_file():
        raise ProcessingError(
            "OUTPUT_NOT_A_DIRECTORY", "Build output must be a directory.", output=str(output)
        )
    protected = {plan.spec_dir.resolve()}
    if source_path is not None:
        protected.add(source_path.parent)
    if output in protected:
        raise ProcessingError(
            "OUTPUT_OVERLAPS_SOURCE",
            "Build output cannot be the directory holding the plan spec or source image.",
            output=str(output),
        )

    source_info: dict[str, Any] | None = None
    if source_path is not None and source_stats is not None:
        source_info = {
            "path": os.path.relpath(source_path, output),
            **source_stats,
        }

    normalized = normalize_plan(plan, canvas=canvas)
    frame_plan = expand_plan(plan, normalized, source_info=source_info)

    checks = [
        {"id": "plan_semantics", "status": "pass"},
        {"id": "source_inspected", "status": "pass" if source_info else "skipped"},
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
    canvas = None
    raw_canvas = frame_plan.get("canvas")
    if (
        plan.canvas_width is None
        and isinstance(raw_canvas, dict)
        and isinstance(raw_canvas.get("width"), int)
        and isinstance(raw_canvas.get("height"), int)
    ):
        canvas = (raw_canvas["width"], raw_canvas["height"])
    normalized = normalize_plan(plan, canvas=canvas)
    return BuildArtifacts(
        build_dir=build_dir, plan=plan, normalized_plan=normalized, frame_plan=frame_plan
    )


def validate_build(build: BuildArtifacts) -> tuple[ValidationResult, list[dict[str, Any]]]:
    errors: list[ValidationIssue] = []
    warnings: list[ValidationIssue] = []
    checks: list[dict[str, Any]] = []

    plan_result = validate_plan(build.plan)
    errors.extend(plan_result.errors)
    warnings.extend(plan_result.warnings)
    checks.append({"id": "plan_semantics", "status": "pass" if plan_result.valid else "fail"})

    consistent = _validate_frame_plan(build, errors)
    checks.append({"id": "frame_plan_consistency", "status": "pass" if consistent else "fail"})

    if build.frames_dir.is_dir():
        frame_errors, frame_warnings = _validate_frames(build)
        errors.extend(frame_errors)
        warnings.extend(frame_warnings)
        checks.append({"id": "frame_files", "status": "pass" if not frame_errors else "fail"})
    else:
        checks.append({"id": "frame_files", "status": "skipped"})

    return ValidationResult(errors=tuple(errors), warnings=tuple(warnings)), checks


def _validate_frame_plan(build: BuildArtifacts, errors: list[ValidationIssue]) -> bool:
    frame_plan = build.frame_plan
    before = len(errors)

    version = frame_plan.get("frame_plan_version")
    if version != FRAME_PLAN_VERSION:
        errors.append(
            _issue(
                "UNSUPPORTED_FRAME_PLAN_VERSION",
                "Frame plan version is not supported.",
                actual=version,
                supported=[FRAME_PLAN_VERSION],
            )
        )
        return False

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

    # A deep re-expansion catches any hand-edited transform, offset, or event.
    if len(errors) == before and validate_plan(build.plan).valid:
        recomputed = expand_plan(
            build.plan, build.normalized_plan, source_info=frame_plan.get("source")
        )
        if recomputed["frames"] != frames:
            errors.append(
                _issue(
                    "FRAME_PLAN_STALE",
                    "Frame plan content does not match a deterministic re-expansion of the plan.",
                )
            )
    return len(errors) == before


def _expected_offsets(build: BuildArtifacts) -> list[tuple[float, float]]:
    offsets: list[tuple[float, float]] = []
    for frame in build.frame_plan.get("frames", []):
        offset = frame.get("offset", {}) if isinstance(frame, dict) else {}
        offsets.append((float(offset.get("x", 0.0)), float(offset.get("y", 0.0))))
    return offsets


def _validate_frames(
    build: BuildArtifacts,
) -> tuple[list[ValidationIssue], list[ValidationIssue]]:
    errors: list[ValidationIssue] = []
    warnings: list[ValidationIssue] = []
    plan = build.plan
    frame_plan = build.frame_plan
    canvas = frame_plan.get("canvas", {})
    expected_size = (
        (canvas.get("width"), canvas.get("height")) if isinstance(canvas, dict) else (None, None)
    )
    transparent = plan.background.casefold() == "transparent"

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

    offsets = _expected_offsets(build)
    bboxes: list[tuple[float, float, int] | None] = []  # (center_x, bottom, index)
    for index, file in enumerate(expected_files):
        frame_path = build.build_dir / file
        if not frame_path.is_file():
            errors.append(
                _issue("FRAME_MISSING", "Frame file does not exist.", frame=file, index=index)
            )
            bboxes.append(None)
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
            continue

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

    _validate_drift(build, offsets, bboxes, errors)
    return errors, warnings


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
