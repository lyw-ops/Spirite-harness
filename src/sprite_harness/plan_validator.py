"""Semantic validation of Animation Plans with stable machine error codes."""

from __future__ import annotations

import re

from .curves import SUPPORTED_CURVES
from .expand import sample_offsets
from .geometry import effective_value_issues
from .plan import ANCHOR_TYPES, REDUCED_MOTION_MODES, SUPPORTED_MOTIONS, AnimationPlan
from .spec import is_finite_number
from .validator import ValidationIssue, ValidationResult


SUPPORTED_PLAN_VERSIONS = {1}
ANIMATION_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")
SOURCE_DIGEST_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")


def _issue(code: str, message: str, **context: object) -> ValidationIssue:
    return ValidationIssue(code=code, message=message, context=dict(context))


def validate_plan(plan: AnimationPlan) -> ValidationResult:
    errors: list[ValidationIssue] = []
    warnings: list[ValidationIssue] = []

    if plan.version not in SUPPORTED_PLAN_VERSIONS:
        errors.append(
            _issue(
                "UNSUPPORTED_PLAN_VERSION",
                "Animation plan version is not supported.",
                version=plan.version,
                supported=sorted(SUPPORTED_PLAN_VERSIONS),
            )
        )
    if not ANIMATION_ID_PATTERN.match(plan.animation_id):
        errors.append(
            _issue(
                "INVALID_ANIMATION_ID",
                "Animation id must be a filesystem-safe slug "
                "(letters, digits, '_', '-', '.'; starting with a letter or digit).",
                actual=plan.animation_id,
            )
        )
    if not is_finite_number(plan.fps) or plan.fps <= 0:
        errors.append(
            _issue("INVALID_FPS", "Playback FPS must be a finite number above zero.", actual=plan.fps)
        )
    if plan.frame_count < 1:
        errors.append(
            _issue(
                "INVALID_FRAME_COUNT",
                "Frame count must be at least one.",
                actual=plan.frame_count,
            )
        )
    if (plan.canvas_width is None) != (plan.canvas_height is None) or (
        plan.canvas_width is not None
        and (plan.canvas_width <= 0 or plan.canvas_height <= 0)
    ):
        errors.append(
            _issue(
                "INVALID_CANVAS_SIZE",
                "Canvas width and height must both be positive integers.",
                actual=[plan.canvas_width, plan.canvas_height],
            )
        )

    if plan.anchor_type not in ANCHOR_TYPES:
        errors.append(
            _issue(
                "INVALID_ANCHOR",
                "Anchor type is not supported.",
                actual=plan.anchor_type,
                supported=list(ANCHOR_TYPES),
            )
        )
    elif plan.anchor_type == "custom":
        if (
            plan.anchor_x is None
            or plan.anchor_y is None
            or not is_finite_number(plan.anchor_x)
            or not is_finite_number(plan.anchor_y)
            or not 0 <= plan.anchor_x <= 1
            or not 0 <= plan.anchor_y <= 1
        ):
            errors.append(
                _issue(
                    "INVALID_ANCHOR",
                    "A custom anchor requires x and y as finite values from 0 through 1.",
                    actual=[plan.anchor_x, plan.anchor_y],
                )
            )
    elif plan.anchor_x is not None or plan.anchor_y is not None:
        errors.append(
            _issue(
                "INVALID_ANCHOR",
                "Anchor coordinates are only allowed with the 'custom' anchor type.",
                type=plan.anchor_type,
            )
        )

    _validate_source_identity(plan, errors)

    if plan.seed is not None and plan.seed < 0:
        errors.append(_issue("INVALID_SEED", "Seed must be a non-negative integer.", actual=plan.seed))

    for name, value in (
        ("max_displacement_px", plan.max_displacement_px),
        ("max_frame_delta_px", plan.max_frame_delta_px),
    ):
        if value is not None and (not is_finite_number(value) or value <= 0):
            errors.append(
                _issue(
                    "INVALID_CONSTRAINT",
                    "Constraint values must be finite numbers above zero.",
                    constraint=name,
                    actual=value,
                )
            )

    if plan.reduced_motion not in REDUCED_MOTION_MODES:
        errors.append(
            _issue(
                "UNSUPPORTED_REDUCED_MOTION",
                "Reduced-motion mode is not supported.",
                actual=plan.reduced_motion,
                supported=list(REDUCED_MOTION_MODES),
            )
        )

    track_errors = _validate_tracks(plan, errors)
    _validate_events(plan, errors)

    if not plan.tracks and not plan.events:
        warnings.append(
            _issue(
                "ZERO_MOTION",
                "Plan declares no tracks and no events; the expansion is a static hold.",
            )
        )

    # Constraint enforcement requires structurally sound tracks and playback.
    if not track_errors and plan.frame_count >= 1:
        # Effective scale/opacity chains no renderer could honor are plan
        # errors, so both `plan` and `render` reject them (docs/renderer.md).
        errors.extend(effective_value_issues(plan))
        if plan.max_displacement_px is not None or plan.max_frame_delta_px is not None:
            _validate_displacement(plan, errors)

    return ValidationResult(errors=tuple(errors), warnings=tuple(warnings))


def _validate_source_identity(plan: AnimationPlan, errors: list[ValidationIssue]) -> None:
    if plan.source_image is None:
        return
    if plan.source_sha256 is not None and not SOURCE_DIGEST_PATTERN.match(plan.source_sha256):
        errors.append(
            _issue(
                "INVALID_SOURCE_IDENTITY",
                "Source sha256 must have the form 'sha256:<64 hex digits>'.",
                actual=plan.source_sha256,
            )
        )
    for name, value in (("width", plan.source_width), ("height", plan.source_height)):
        if value is not None and value < 1:
            errors.append(
                _issue(
                    "INVALID_SOURCE_IDENTITY",
                    "Source dimensions must be positive integers.",
                    dimension=name,
                    actual=value,
                )
            )


def _validate_tracks(plan: AnimationPlan, errors: list[ValidationIssue]) -> bool:
    found_error = False
    seen: dict[str, int] = {}
    for index, track in enumerate(plan.tracks):
        if track.track_id in seen:
            errors.append(
                _issue(
                    "DUPLICATE_TRACK_ID",
                    "Track ids must be unique inside a plan.",
                    track_id=track.track_id,
                    first_index=seen[track.track_id],
                    duplicate_index=index,
                )
            )
            found_error = True
        else:
            seen[track.track_id] = index

        if track.motion not in SUPPORTED_MOTIONS:
            errors.append(
                _issue(
                    "UNSUPPORTED_MOTION",
                    "Track motion is not supported.",
                    track_id=track.track_id,
                    actual=track.motion,
                    supported=sorted(SUPPORTED_MOTIONS),
                )
            )
            found_error = True
        elif track.unit != SUPPORTED_MOTIONS[track.motion]:
            errors.append(
                _issue(
                    "UNIT_MISMATCH",
                    "Track unit does not match its motion type.",
                    track_id=track.track_id,
                    motion=track.motion,
                    expected=SUPPORTED_MOTIONS[track.motion],
                    actual=track.unit,
                )
            )
            found_error = True
        if track.curve not in SUPPORTED_CURVES:
            errors.append(
                _issue(
                    "UNSUPPORTED_CURVE",
                    "Track curve is not supported.",
                    track_id=track.track_id,
                    actual=track.curve,
                    supported=list(SUPPORTED_CURVES),
                )
            )
            found_error = True
        if not is_finite_number(track.amplitude):
            errors.append(
                _issue(
                    "INVALID_AMPLITUDE",
                    "Track amplitude must be a finite number.",
                    track_id=track.track_id,
                    actual=track.amplitude,
                )
            )
            found_error = True
        if not is_finite_number(track.cycles) or track.cycles <= 0:
            errors.append(
                _issue(
                    "INVALID_CYCLES",
                    "Track cycles must be a finite number above zero.",
                    track_id=track.track_id,
                    actual=track.cycles,
                )
            )
            found_error = True
        elif plan.loop and track.cycles != int(track.cycles):
            # Loop-cycle continuity contract: a looping animation returns to
            # frame 0, so every track must complete whole cycles or the curve
            # value jumps at the loop seam.
            errors.append(
                _issue(
                    "NON_INTEGRAL_LOOP_CYCLES",
                    "Looping playback requires a positive integer cycle count "
                    "so the curve is continuous across the loop seam.",
                    track_id=track.track_id,
                    actual=track.cycles,
                )
            )
            found_error = True
        if not is_finite_number(track.phase) or not 0 <= track.phase < 1:
            errors.append(
                _issue(
                    "INVALID_PHASE",
                    "Track phase must be at least 0 and below 1.",
                    track_id=track.track_id,
                    actual=track.phase,
                )
            )
            found_error = True
    return found_error


def _validate_events(plan: AnimationPlan, errors: list[ValidationIssue]) -> None:
    seen: dict[str, int] = {}
    for index, event in enumerate(plan.events):
        if event.event_id in seen:
            errors.append(
                _issue(
                    "DUPLICATE_EVENT_ID",
                    "Event ids must be unique inside a plan.",
                    event_id=event.event_id,
                    first_index=seen[event.event_id],
                    duplicate_index=index,
                )
            )
        else:
            seen[event.event_id] = index
        out_of_range = [frame for frame in event.frames if not 0 <= frame < plan.frame_count]
        if out_of_range:
            errors.append(
                _issue(
                    "EVENT_FRAME_OUT_OF_RANGE",
                    "Event frame indices must lie inside the frame range.",
                    event_id=event.event_id,
                    frames=out_of_range,
                    frame_count=plan.frame_count,
                )
            )


def _validate_displacement(plan: AnimationPlan, errors: list[ValidationIssue]) -> None:
    offsets = sample_offsets(plan)
    if plan.max_displacement_px is not None:
        for index, (dx, dy) in enumerate(offsets):
            magnitude = max(abs(dx), abs(dy))
            if magnitude > plan.max_displacement_px + 1e-9:
                errors.append(
                    _issue(
                        "DISPLACEMENT_EXCEEDED",
                        "Frame offset exceeds the allowed displacement.",
                        frame=index,
                        offset=[dx, dy],
                        limit=plan.max_displacement_px,
                    )
                )
    if plan.max_frame_delta_px is not None and len(offsets) > 1:
        pairs = list(zip(offsets, offsets[1:]))
        if plan.loop:
            pairs.append((offsets[-1], offsets[0]))
        for index, (current, following) in enumerate(pairs):
            delta = max(abs(following[0] - current[0]), abs(following[1] - current[1]))
            if delta > plan.max_frame_delta_px + 1e-9:
                errors.append(
                    _issue(
                        "FRAME_DELTA_EXCEEDED",
                        "Offset change between consecutive frames exceeds the allowed delta.",
                        from_frame=index,
                        to_frame=(index + 1) % len(offsets),
                        delta=delta,
                        limit=plan.max_frame_delta_px,
                    )
                )
