"""Deterministic expansion of an Animation Plan into a frame plan.

The frame plan is pure math over the declared motion tracks: per frame, each
track is sampled into a concrete transform value, and translate tracks that
target the reserved ``"sprite"`` label are aggregated into a whole-sprite pixel
offset. Tracks targeting semantic parts (``head``, ``hand_right``, …) are
expanded per frame but never move the aggregate offset. No pixels are
synthesized here; renderers (milestone 2+) consume the frame plan.
"""

from __future__ import annotations

import hashlib
from typing import Any

from . import __version__
from .curves import sample_track_value
from .jsonio import dumps_strict
from .plan import SPRITE_TARGET, AnimationPlan, resolved_anchor


FRAME_PLAN_VERSION = 1
FRAME_FILE_TEMPLATE = "frames/frame_{index:03d}.png"
VALUE_DECIMALS = 6


def _round(value: float) -> float:
    rounded = round(value, VALUE_DECIMALS)
    return 0.0 if rounded == 0 else rounded


def sample_offsets(plan: AnimationPlan) -> list[tuple[float, float]]:
    """Aggregate whole-sprite pixel offset (x right, y down) per frame.

    Only translate tracks targeting :data:`~sprite_harness.plan.SPRITE_TARGET`
    contribute; target-local motion (a hand, a head) never shifts the
    whole-sprite bounding-box expectation.
    """

    offsets: list[tuple[float, float]] = []
    for index in range(plan.frame_count):
        dx = 0.0
        dy = 0.0
        for track in plan.tracks:
            if track.target != SPRITE_TARGET or track.motion not in (
                "translate_x",
                "translate_y",
            ):
                continue
            value = sample_track_value(
                track.curve,
                track.amplitude,
                index,
                plan.frame_count,
                loop=plan.loop,
                cycles=track.cycles,
                phase=track.phase,
            )
            if track.motion == "translate_x":
                dx += value
            else:
                dy += value
        offsets.append((_round(dx), _round(dy)))
    return offsets


def normalize_plan(
    plan: AnimationPlan,
    *,
    canvas: tuple[int, int] | None = None,
    source: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Canonical fully-defaulted plan document, suitable for ``plan.json``.

    ``canvas`` supplies dimensions inherited from the source image when the
    plan itself declares none. ``source`` replaces the plan's own source block
    (build creation passes the build-relative path plus the inspected identity
    so the written ``plan.json`` resolves and digest-binds the source).
    """

    width, height = (
        (plan.canvas_width, plan.canvas_height)
        if plan.canvas_width is not None
        else (canvas if canvas is not None else (None, None))
    )
    document: dict[str, Any] = {
        "plan_version": plan.version,
        "animation_id": plan.animation_id,
        "playback": {
            "fps": plan.fps,
            "frame_count": plan.frame_count,
            "loop": plan.loop,
        },
        "canvas": {
            "width": width,
            "height": height,
            "background": plan.background,
        },
        "anchor": (
            {"type": plan.anchor_type, "x": plan.anchor_x, "y": plan.anchor_y}
            if plan.anchor_type == "custom"
            else {"type": plan.anchor_type}
        ),
        "reduced_motion": {"mode": plan.reduced_motion},
        "tracks": [
            {
                "track_id": track.track_id,
                "target": track.target,
                "motion": track.motion,
                "amplitude": track.amplitude,
                "unit": track.unit,
                "curve": track.curve,
                "cycles": track.cycles,
                "phase": track.phase,
            }
            for track in plan.tracks
        ],
        "events": [
            {
                "event_id": event.event_id,
                "type": event.type,
                **({"target": event.target} if event.target is not None else {}),
                "frames": list(event.frames),
            }
            for event in plan.events
        ],
    }
    if source is not None:
        document["source"] = dict(source)
    elif plan.source_image is not None:
        source_block: dict[str, Any] = {"image": plan.source_image}
        if plan.source_sha256 is not None:
            source_block["sha256"] = plan.source_sha256
        if plan.source_width is not None:
            source_block["width"] = plan.source_width
        if plan.source_height is not None:
            source_block["height"] = plan.source_height
        document["source"] = source_block
    if plan.seed is not None:
        document["seed"] = plan.seed
    constraints: dict[str, Any] = {}
    if plan.max_displacement_px is not None:
        constraints["max_displacement_px"] = plan.max_displacement_px
    if plan.max_frame_delta_px is not None:
        constraints["max_frame_delta_px"] = plan.max_frame_delta_px
    if constraints:
        document["constraints"] = constraints
    if plan.metadata:
        document["metadata"] = plan.metadata
    return document


def plan_digest(normalized_plan: dict[str, Any]) -> str:
    """Stable content digest binding a frame plan to its normalized plan.

    Canonicalization is strict JSON; non-finite numbers (only reachable in
    invalid, hand-edited plans) map to deterministic strings so the digest is
    always defined and validation can still report the semantic error.
    """

    canonical = dumps_strict(
        normalized_plan, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    )
    return "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def frame_plan_source(normalized_plan: dict[str, Any]) -> dict[str, Any] | None:
    """The frame plan's source block, derived only from the normalized plan."""

    source = normalized_plan.get("source")
    if not isinstance(source, dict):
        return None
    if not all(field in source for field in ("image", "sha256", "width", "height")):
        return None
    return {
        "path": source["image"],
        "sha256": source["sha256"],
        "width": source["width"],
        "height": source["height"],
    }


def expand_plan(plan: AnimationPlan, normalized_plan: dict[str, Any]) -> dict[str, Any]:
    """Sample every track at every frame into a frame plan document.

    Every authoritative frame-plan field is derived from ``plan`` and
    ``normalized_plan`` alone, so validation can recompute the expected
    document without trusting the frame plan under test.
    """

    events_by_frame: dict[int, list[str]] = {}
    for event in plan.events:
        for frame in event.frames:
            events_by_frame.setdefault(frame, []).append(event.event_id)

    offsets = sample_offsets(plan)
    frames: list[dict[str, Any]] = []
    for index in range(plan.frame_count):
        transforms = [
            {
                "track_id": track.track_id,
                "target": track.target,
                "motion": track.motion,
                "unit": track.unit,
                "value": _round(
                    sample_track_value(
                        track.curve,
                        track.amplitude,
                        index,
                        plan.frame_count,
                        loop=plan.loop,
                        cycles=track.cycles,
                        phase=track.phase,
                    )
                ),
            }
            for track in plan.tracks
        ]
        frames.append(
            {
                "index": index,
                "file": FRAME_FILE_TEMPLATE.format(index=index),
                "time_s": _round(index / plan.fps),
                "transforms": transforms,
                "offset": {"x": offsets[index][0], "y": offsets[index][1]},
                "events": sorted(events_by_frame.get(index, [])),
            }
        )

    anchor_x, anchor_y = resolved_anchor(plan)
    return {
        "frame_plan_version": FRAME_PLAN_VERSION,
        "animation_id": plan.animation_id,
        "generated_by": f"sprite-harness {__version__}",
        "plan_digest": plan_digest(normalized_plan),
        "source": frame_plan_source(normalized_plan),
        "playback": normalized_plan["playback"],
        "canvas": normalized_plan["canvas"],
        "anchor": {"type": plan.anchor_type, "x": anchor_x, "y": anchor_y},
        "reduced_motion": normalized_plan["reduced_motion"],
        "frames": frames,
    }
