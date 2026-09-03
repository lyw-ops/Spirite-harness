"""Explicit layered raster input and two-stage composition (docs/layered-sprites.md)."""

from dataclasses import dataclass

from PIL import Image

from .geometry import (
    FramePose, TRANSPARENT, integral_translation, inverse_affine_coeffs,
    opacity_lut, render_pose, sample_poses,
)
from .plan import AnimationPlan, resolved_anchor


@dataclass
class LayerScene:
    plan: AnimationPlan
    images: list[Image.Image]
    poses: list[list[FramePose]]

    @classmethod
    def load(cls, plan: AnimationPlan) -> "LayerScene":
        images = []
        for layer in plan.layers:
            with Image.open(plan.spec_dir / layer.source_image) as image:
                image.load()
                images.append(image.convert("RGBA"))
        return cls(plan, images, [sample_poses(plan, layer.target) for layer in plan.layers])

    def composite(self, index: int) -> Image.Image:
        size = (self.plan.reference_width, self.plan.reference_height)
        result = Image.new("RGBA", size, TRANSPARENT)
        for layer, image, poses in zip(self.plan.layers, self.images, self.poses):
            pose = poses[index]
            ax, ay = resolved_anchor(layer)
            a_src = (image.width * ax, image.height * ay)
            a_dst = (layer.position_x, layer.position_y)
            shift = integral_translation(pose, a_src, a_dst)
            if shift is not None:
                local = Image.new("RGBA", size, TRANSPARENT)
                # A finite translation can exceed Pillow's C integer range.
                # Fully clipped layers contribute nothing, even at huge offsets.
                if (shift[0] < size[0] and shift[1] < size[1]
                        and shift[0] + image.width > 0 and shift[1] + image.height > 0):
                    local.paste(image, shift)
            else:
                local = image.transform(
                    size, Image.Transform.AFFINE,
                    inverse_affine_coeffs(pose, a_src, a_dst),
                    resample=Image.Resampling.BILINEAR, fillcolor=TRANSPARENT,
                )
            if pose.opacity != 1.0:
                local.putalpha(local.getchannel("A").point(opacity_lut(pose.opacity)))
            # Invisible layers are legal. Only the final frame must be nonempty.
            result.alpha_composite(local)
        return result


def render_source_pose(
    source: Image.Image | LayerScene, pose: FramePose,
    canvas_size: tuple[int, int], anchor: tuple[float, float],
) -> Image.Image:
    composite = source.composite(pose.index) if isinstance(source, (LayerScene, ReplacementScene)) else source
    return render_pose(composite, pose, canvas_size, anchor)


@dataclass
class ReplacementScene:
    """Select frozen source-space pixels before either transform stage."""
    original: Image.Image | LayerScene
    replacements: dict[tuple[str, int], Image.Image]

    def composite(self, index: int) -> Image.Image:
        if isinstance(self.original, LayerScene):
            scene = self.original
            images = [self.replacements.get((layer.target, index), image)
                      for layer, image in zip(scene.plan.layers, scene.images)]
            return LayerScene(scene.plan, images, scene.poses).composite(index)
        return self.replacements.get(('sprite', index), self.original)
