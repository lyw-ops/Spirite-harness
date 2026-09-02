"""Deterministic curve sampling for Animation Plan motion tracks.

Every curve maps a normalized cycle position ``u`` in ``[0, 1)`` to a weight.
Periodic curves return values in ``[-1, 1]`` and are loop-continuous by
construction. Easing curves return values in ``[0, 1]`` and are mirrored
(ping-pong) inside each cycle so that a looping animation never jumps at the
cycle boundary. ``hold`` always returns 0.
"""

from __future__ import annotations

import math


PERIODIC_CURVES = ("sine", "triangle")
EASING_CURVES = ("linear", "ease_in", "ease_out", "ease_in_out")
SUPPORTED_CURVES = PERIODIC_CURVES + EASING_CURVES + ("hold",)


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


def sample_curve(curve: str, u: float) -> float:
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

    # Easing curves are mirrored within the cycle: 0 -> 1 across the first
    # half, back 1 -> 0 across the second half, shaped by the easing function.
    v = 2.0 * u if u <= 0.5 else 2.0 - 2.0 * u
    if curve == "linear":
        return v
    if curve == "ease_in":
        return v * v
    if curve == "ease_out":
        return 1.0 - (1.0 - v) * (1.0 - v)
    if curve == "ease_in_out":
        return v * v * (3.0 - 2.0 * v)
    raise ValueError(f"Unsupported curve: {curve}")


def sample_track_value(
    curve: str,
    amplitude: float,
    frame_index: int,
    frame_count: int,
    *,
    loop: bool,
    cycles: float,
    phase: float,
) -> float:
    u = cycle_position(frame_index, frame_count, loop=loop, cycles=cycles, phase=phase)
    return amplitude * sample_curve(curve, u)
