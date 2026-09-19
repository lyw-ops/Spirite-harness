"""Deterministic sampling for Animation Plan motion tracks.

Curve tracks: every curve maps a normalized cycle position ``u`` in ``[0, 1)``
to a weight. Periodic curves return values in ``[-1, 1]`` and are
loop-continuous by construction. Easing curves return values in ``[0, 1]`` and
are mirrored (ping-pong) inside each cycle so that a looping animation never
jumps at the cycle boundary. ``pulse`` is a deliberately discrete periodic
curve: it is ``+1`` for the declared duty fraction and ``-1`` otherwise.
``hold`` always returns 0.

Keyframe tracks: an explicit piecewise timeline over normalized loop time in
``[0, 1]``. Each keyframe carries a direct value and the interpolation shape
of the segment to the next keyframe; a looping track's final segment returns
to the first keyframe's value exactly at time 1 (the loop seam).
"""

from __future__ import annotations

import math


PERIODIC_CURVES = ("sine", "triangle")
EASING_CURVES = ("linear", "ease_in", "ease_out", "ease_in_out")
DISCRETE_CURVES = ("pulse",)
SUPPORTED_CURVES = PERIODIC_CURVES + EASING_CURVES + DISCRETE_CURVES + ("hold",)

# Per-segment shapes a keyframe may declare for the span to the next keyframe.
KEYFRAME_INTERPOLATIONS = EASING_CURVES + ("hold",)


def cycle_position(
    frame_index: int,
    frame_count: int,
    *,
    loop: bool,
    cycles: float,
    phase: float,
) -> float:
    """Normalized position of a frame inside the track's cycle.

    Looping animations divide the cycle over ``frame_count`` steps so the frame
    after the last one (the first frame again) lands exactly on the next cycle
    boundary. Non-looping animations reach the end of the cycle on the final
    frame.
    """

    period = frame_count if loop else max(frame_count - 1, 1)
    return math.fmod((frame_index / period) * cycles + phase, 1.0)


def sample_curve(curve: str, u: float, *, duty_cycle: float = 0.5) -> float:
    if curve == "hold":
        return 0.0
    if curve == "sine":
        return math.sin(math.tau * u)
    if curve == "triangle":
        if u < 0.25:
            return 4.0 * u
        if u < 0.75:
            return 2.0 - 4.0 * u
        return 4.0 * u - 4.0
    if curve == "pulse":
        return 1.0 if u < duty_cycle else -1.0
    if curve not in EASING_CURVES:
        raise ValueError(f"Unsupported curve: {curve}")

    # Easing curves are mirrored within the cycle: 0 -> 1 across the first
    # half, back 1 -> 0 across the second half, shaped by the easing function.
    v = 2.0 * u if u <= 0.5 else 2.0 - 2.0 * u
    return _ease(curve, v)


def _ease(shape: str, t: float) -> float:
    """Easing weight for a normalized progress ``t`` in ``[0, 1]``."""

    if shape == "linear":
        return t
    if shape == "ease_in":
        return t * t
    if shape == "ease_out":
        return 1.0 - (1.0 - t) * (1.0 - t)
    if shape == "ease_in_out":
        return t * t * (3.0 - 2.0 * t)
    raise ValueError(f"Unsupported easing shape: {shape}")


def sample_track_value(
    curve: str,
    amplitude: float,
    frame_index: int,
    frame_count: int,
    *,
    loop: bool,
    cycles: float,
    phase: float,
    duty_cycle: float = 0.5,
) -> float:
    u = cycle_position(frame_index, frame_count, loop=loop, cycles=cycles, phase=phase)
    return amplitude * sample_curve(curve, u, duty_cycle=duty_cycle)


def keyframe_position(frame_index: int, frame_count: int, *, loop: bool) -> float:
    """Normalized time of a frame on a keyframe track's timeline.

    Looping playback spreads the timeline over ``frame_count`` steps so the
    frame after the last one (the first frame again) lands exactly on time 1,
    which wraps to 0; sampled positions stay in ``[0, 1)``. Non-looping
    playback reaches time 1 exactly on the final frame.
    """

    if loop:
        return math.fmod(frame_index / frame_count, 1.0)
    return frame_index / max(frame_count - 1, 1)


def sample_keyframes(keyframes, u: float, *, loop: bool) -> float:
    """Sample a validated keyframe sequence at normalized time ``u``.

    ``keyframes`` are records with ``at``, ``value``, and ``interpolation``
    attributes (:class:`sprite_harness.plan.Keyframe`), already validated:
    non-empty, finite, strictly increasing ``at`` starting at exactly 0.

    Each keyframe's ``interpolation`` shapes the segment to the next keyframe;
    ``hold`` keeps the keyframe's value and steps exactly on the next
    keyframe's ``at``. Sampling exactly at a keyframe's ``at`` returns its
    ``value`` exactly. After the last keyframe, a looping track interpolates
    back to the first keyframe's value, reaching it exactly at time 1 (the
    loop seam) using the last keyframe's interpolation; a non-looping track
    holds the last value through the end.
    """

    last = keyframes[-1]
    if u >= last.at:
        if not loop:
            return last.value
        return _segment_value(last.at, last.value, 1.0, keyframes[0].value, last.interpolation, u)
    for index in range(len(keyframes) - 1):
        following = keyframes[index + 1]
        if u < following.at:
            current = keyframes[index]
            return _segment_value(
                current.at, current.value, following.at, following.value, current.interpolation, u
            )
    raise ValueError("Keyframe segments do not cover the sampled time.")


def _segment_value(
    start_at: float,
    start_value: float,
    end_at: float,
    end_value: float,
    interpolation: str,
    u: float,
) -> float:
    if interpolation == "hold":
        return start_value
    weight = _ease(interpolation, (u - start_at) / (end_at - start_at))
    return start_value + (end_value - start_value) * weight


def sample_track(track, frame_index: int, frame_count: int, *, loop: bool) -> float:
    """Raw sampled value of one plan track (curve or keyframe kind) at a frame.

    ``track`` is the plan's typed track record. A track with ``keyframes``
    samples its piecewise timeline; every other track samples its cycle curve
    scaled by ``amplitude``. Both kinds produce the value in the motion's
    shared composition semantics (px, deg, or the ratio whose effective
    factor is ``1 + value``).
    """

    if track.keyframes is not None:
        return sample_keyframes(
            track.keyframes,
            keyframe_position(frame_index, frame_count, loop=loop),
            loop=loop,
        )
    return sample_track_value(
        track.curve,
        track.amplitude,
        frame_index,
        frame_count,
        loop=loop,
        cycles=track.cycles,
        phase=track.phase,
        duty_cycle=track.duty_cycle if track.duty_cycle is not None else 0.5,
    )
