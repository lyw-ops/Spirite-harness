"""Whole-sprite pose sampling and affine geometry shared by renderer and validator.

The pose contract is documented in ``docs/renderer.md`` and fixed there before
this implementation: pixel ``(i, j)`` has center ``(i + 0.5, j + 0.5)``, x
points right, y points down, positive rotation is clockwise on screen, and the
forward map of a source point ``p`` is::

    P = A_dst + (dx, dy) + R(theta) . s . (p - A_src)

with ``A_src``/``A_dst`` the anchor point in source and canvas coordinates.
Rotation values add across tracks, scale and opacity factors ``1 + value``
multiply, opacity is clamped into ``[0, 1]``, and translation comes from the
aggregate frame offset exactly once.

The validator deliberately shares this module with the renderer so a legal
transform never registers as drift; independence is provided by reference
tests with hand-computed expected pixel positions.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from PIL import Image

from .curves import sample_track_value
from .expand import _round as round_value
from .expand import sample_offsets
from .plan import SPRITE_TARGET, AnimationPlan, Track
from .validator import ValidationIssue


TRANSPARENT = (0, 0, 0, 0)

# Placement offsets this close to an integer render through the exact
# pixel-copy path instead of resampling.
INTEGRAL_EPSILON = 1e-9


@dataclass(frozen=True)
class FramePose:
    """The composed whole-sprite transform of one frame."""

    index: int
    dx: float
    dy: float
    rotate_deg: float
    scale: float
    opacity: float

    @property
    def is_translation_only(self) -> bool:
        return self.rotate_deg == 0.0 and self.scale == 1.0 and self.opacity == 1.0


def _target_tracks(plan: AnimationPlan, motion: str, target: str = SPRITE_TARGET) -> list[Track]:
    return [
        track
        for track in plan.tracks
        if track.target == target and track.motion == motion
    ]


def _sample(track: Track, index: int, plan: AnimationPlan) -> float:
    """One track sample, rounded exactly like the frame-plan values."""

    return round_value(
        sample_track_value(
            track.curve,
            track.amplitude,
            index,
            plan.frame_count,
            loop=plan.loop,
            cycles=track.cycles,
            phase=track.phase,
        )
    )


def sample_poses(plan: AnimationPlan, target: str = SPRITE_TARGET, *, clamp_opacity: bool = True) -> list[FramePose]:
    """Compose per-frame poses for one target (the global sprite by default).

    Translation is the aggregate frame offset (translate tracks targeting
    ``sprite``, applied exactly once). Rotate samples add; scale and opacity
    factors ``1 + value`` multiply; opacity is clamped into ``[0, 1]``.
    A target's tracks never contribute to another target's pose.
    """

    offsets = sample_offsets(plan, target)
    rotate_tracks = _target_tracks(plan, "rotate", target)
    scale_tracks = _target_tracks(plan, "scale", target)
    opacity_tracks = _target_tracks(plan, "opacity", target)

    poses: list[FramePose] = []
    for index in range(plan.frame_count):
        rotate_deg = 0.0
        for track in rotate_tracks:
            rotate_deg += _sample(track, index, plan)
        scale = 1.0
        for track in scale_tracks:
            scale *= 1.0 + _sample(track, index, plan)
        opacity = 1.0
        for track in opacity_tracks:
            opacity *= 1.0 + _sample(track, index, plan)
        poses.append(
            FramePose(
                index=index,
                dx=offsets[index][0],
                dy=offsets[index][1],
                rotate_deg=round_value(rotate_deg),
                scale=scale,
                opacity=min(max(opacity, 0.0), 1.0) if clamp_opacity else opacity,
            )
        )
    return poses


def pose_document(pose: FramePose) -> dict:
    return {"translation": {"x": pose.dx, "y": pose.dy},
            "rotate_deg": pose.rotate_deg, "scale": pose.scale, "opacity": pose.opacity}


def effective_value_issues(plan: AnimationPlan) -> list[ValidationIssue]:
    """Validate factors, composed values and affine coefficients before rendering.

    Local zero opacity is legal. Global opacity zero and any scale product
    underflow are not. Check the raw opacity product before clamping infinity.
    """
    from .plan import resolved_anchor

    issues: list[ValidationIssue] = []
    targets = [SPRITE_TARGET, *(layer.target for layer in plan.layers or ())]
    for target in targets:
        before = len(issues)
        for track in (t for t in plan.tracks if t.target == target):
            for index in range(plan.frame_count):
                value = _sample(track, index, plan)
                code = None
                if not math.isfinite(value):
                    code = "NONFINITE_EFFECTIVE_TRANSFORM"
                elif track.motion == "scale" and 1.0 + value <= 0:
                    code = "INVALID_EFFECTIVE_SCALE"
                elif track.motion == "opacity" and 1.0 + value < 0:
                    code = "INVALID_EFFECTIVE_OPACITY"
                if code:
                    issues.append(ValidationIssue(code=code,
                        message="Track has an invalid effective transform value.",
                        context={"target": target, "track_id": track.track_id, "frame": index,
                                 "factor": 1.0 + value}))
                    break
        if len(issues) != before:
            continue
        layer = next((layer for layer in plan.layers or () if layer.target == target), None)
        for pose in sample_poses(plan, target, clamp_opacity=False):
            values = [pose.dx, pose.dy, pose.rotate_deg, pose.scale, pose.opacity]
            code = None
            if not all(math.isfinite(value) for value in values):
                code = "NONFINITE_EFFECTIVE_TRANSFORM"
            elif pose.scale <= 0:
                code = "INVALID_EFFECTIVE_SCALE"
            elif target == SPRITE_TARGET and pose.opacity == 0:
                code = "FULLY_TRANSPARENT_FRAME"
            else:
                # Also reject finite components whose placement/inverse arithmetic
                # overflows. Actual source sizes are bound during build creation.
                if layer:
                    ax, ay = resolved_anchor(layer)
                    a_src = ((layer.source_width or 1) * ax, (layer.source_height or 1) * ay)
                    a_dst = (layer.position_x, layer.position_y)
                else:
                    ax, ay = resolved_anchor(plan)
                    sw = plan.reference_width if plan.layered else plan.source_width
                    sh = plan.reference_height if plan.layered else plan.source_height
                    a_src = ((sw or 1) * ax, (sh or 1) * ay)
                    a_dst = ((plan.canvas_width or sw or 1) * ax,
                             (plan.canvas_height or sh or 1) * ay)
                coeffs = inverse_affine_coeffs(pose, a_src, a_dst)
                if not all(math.isfinite(value) for value in (*coeffs,
                        a_dst[0] + pose.dx, a_dst[1] + pose.dy)):
                    code = "NONFINITE_EFFECTIVE_TRANSFORM"
            if code:
                issues.append(ValidationIssue(code=code,
                    message="Composed transform must be finite, with positive scale and visible global opacity.",
                    context={"target": target, "frame": pose.index}))
                break
    return issues


def anchor_points(
    anchor: tuple[float, float],
    source_size: tuple[int, int],
    canvas_size: tuple[int, int],
) -> tuple[tuple[float, float], tuple[float, float]]:
    """Concrete anchor coordinates in source and canvas pixel space."""

    ax, ay = anchor
    a_src = (source_size[0] * ax, source_size[1] * ay)
    a_dst = (canvas_size[0] * ax, canvas_size[1] * ay)
    return a_src, a_dst


def integral_translation(
    pose: FramePose,
    a_src: tuple[float, float],
    a_dst: tuple[float, float],
) -> tuple[int, int] | None:
    """Exact integer paste position for a pure integral translation, else None."""

    if pose.rotate_deg != 0.0 or pose.scale != 1.0:
        return None
    dx = a_dst[0] + pose.dx - a_src[0]
    dy = a_dst[1] + pose.dy - a_src[1]
    rx, ry = round(dx), round(dy)
    if abs(dx - rx) <= INTEGRAL_EPSILON and abs(dy - ry) <= INTEGRAL_EPSILON:
        return int(rx), int(ry)
    return None


def inverse_affine_coeffs(
    pose: FramePose,
    a_src: tuple[float, float],
    a_dst: tuple[float, float],
) -> tuple[float, float, float, float, float, float]:
    """Output-to-input affine coefficients for ``Image.transform``.

    Inverse of the documented forward map: ``p = A_src + (1/s) . R(-theta) .
    (P - A_dst - (dx, dy))``, expressed as the six coefficients Pillow expects.
    """

    theta = math.radians(pose.rotate_deg)
    cos_t = math.cos(theta)
    sin_t = math.sin(theta)
    scale = pose.scale
    tx = a_dst[0] + pose.dx
    ty = a_dst[1] + pose.dy
    a = cos_t / scale
    b = sin_t / scale
    c = a_src[0] - (a * tx + b * ty)
    d = -sin_t / scale
    e = cos_t / scale
    f = a_src[1] - (d * tx + e * ty)
    return a, b, c, d, e, f


def opacity_lut(opacity: float) -> list[int]:
    """Alpha lookup table: ``alpha_out = floor(alpha_in * opacity + 0.5)``."""

    return [min(255, int(alpha * opacity + 0.5)) for alpha in range(256)]


def render_pose(
    source: Image.Image,
    pose: FramePose,
    canvas_size: tuple[int, int],
    anchor: tuple[float, float],
) -> Image.Image:
    """Render one frame of the whole-sprite transform onto a transparent canvas.

    ``source`` must already be RGBA. Integral pure translations are exact pixel
    copies; every other pose resamples with explicit bilinear interpolation.
    Opacity is applied to the alpha channel after the geometric transform.
    """

    a_src, a_dst = anchor_points(anchor, source.size, canvas_size)
    shift = integral_translation(pose, a_src, a_dst)
    if shift is not None:
        frame = Image.new("RGBA", canvas_size, TRANSPARENT)
        frame.paste(source, shift)
    else:
        frame = source.transform(
            canvas_size,
            Image.Transform.AFFINE,
            inverse_affine_coeffs(pose, a_src, a_dst),
            resample=Image.Resampling.BILINEAR,
            fillcolor=TRANSPARENT,
        )
    if pose.opacity != 1.0:
        frame.putalpha(frame.getchannel("A").point(opacity_lut(pose.opacity)))
    return frame


def expected_alpha_bbox(
    source: Image.Image,
    pose: FramePose,
    canvas_size: tuple[int, int],
    anchor: tuple[float, float],
) -> tuple[int, int, int, int] | None:
    """Model the alpha bounding box a correct render of ``pose`` must produce.

    Derived from the trusted source image and the verified transform only —
    never from the frames under validation. The result is clipped to the
    canvas exactly like real output.
    """

    return render_pose(source, pose, canvas_size, anchor).getchannel("A").getbbox()
