# Layered sprites (milestone 3)

This contract fixes the input and geometry before the renderer implementation.
Use Animation Plan **v2** for layered input. V1 single-image plans and `--source`
keep their existing behavior. V2 requires this inline `source` object:

```json
{
  "reference_canvas": {"width": 64, "height": 64},
  "layers": [
    {"target": "panel", "image": "assets/panel.png",
     "anchor": {"type": "center"}, "position": {"x": 32, "y": 32}},
    {"target": "marker", "image": "assets/marker.png",
     "anchor": {"type": "custom", "x": 0, "y": 0},
     "position": {"x": 28, "y": 12}}
  ]
}
```

`source.image` and `source.layers` are mutually exclusive. `--source` with
layered input is an error, even if its path names a layer. Invalid layered
input never falls back to single-image mode. No directory discovery, external
layer manifest, or required metadata is involved. The enclosing plan file is
the layer description. Empty arrays, duplicate targets, and the reserved
target `sprite` are errors. Every track and optional event target in a layered
plan must name `sprite` or a declared layer. Events remain annotations: their
names never generate pixel actions. Untracked layers render statically.

Every layer requires a PNG with an alpha channel (RGBA, LA or transparent
palette); an opaque RGBA rectangle is valid. Source images may be completely
transparent. Each layer requires an anchor (`center`, `bottom_center`, or
`custom` normalized x/y in [0,1]) and a finite static position in reference
canvas pixels. Array order is authoritative, back to front; there is no z-index.

## Coordinates and two-stage rendering

Pixel (i,j) has center (i+0.5,j+0.5). X points right, y down, positive rotation
is clockwise, exactly as M2. For source point p in a layer:

```
q = position + local_translation + R(local_rotation) * local_scale * (p - A_layer)
A_layer = (image_width * anchor.x, image_height * anchor.y)
R(t) = [[cos(t), -sin(t)], [sin(t), cos(t)]]
```

The source anchor maps to the declared position plus local translation.
Local translation uses reference-canvas axes and pixels; it is not rotated
by the local rotation. Each transformed layer is clipped to a transparent
reference canvas, its opacity applied, then alpha-over composited in array
order. Invisible, occluded or fully clipped individual layers are permitted.

The full reference-canvas composite is transformed once by the unchanged M2
`render_pose` algorithm using the global plan anchor: its source anchor is
on the reference canvas, its destination anchor on `plan.canvas`. Global
translation comes from `frame.offset` exactly once. Global opacity applies
once to the final transformed composite, never to individual layers. Final
output clips to `plan.canvas`; pixels lost at the intermediate clip cannot
reappear after a global translation. Both canvases are fixed. An omitted
`plan.canvas` defaults to the explicitly declared reference size; a different
output canvas uses anchor alignment, without an implicit fit or scale.

For each target, translate samples sum (rounded once to six decimals), rotate
samples sum (each sample and final sum rounded to six decimals), scale and
opacity factors `1 + sample` multiply in track order. Scale is uniform and
strictly positive. Negative opacity factors are invalid; effective opacity
clamps to [0,1] **after** a finite product is verified. Local opacity zero is
valid; global opacity zero is `FULLY_TRANSPARENT_FRAME`. Non-finite composed
values, placement or inverse coefficients fail as `NONFINITE_EFFECTIVE_TRANSFORM`;
scale product underflow to zero is `INVALID_EFFECTIVE_SCALE`.

Both stages use the M2 exact integer-translation copy path (tolerance 1e-9)
or explicit Pillow premultiplied RGBA bilinear affine sampling. Opacity uses
`floor(alpha * opacity + 0.5)`. Alpha-over uses Pillow's 8-bit rounding:
`a = a_front + a_back*(1-a_front)`, with premultiplied color summed then
converted to straight RGB. Each stage quantizes to 8 bits. Consequently the
two-stage result need not equal a single combined affine resampling.
Global displacement/frame-delta constraints still apply only to global offset;
M3 has no independent local motion budget. Final empty frames are rejected.

## Paths, identity and artifacts

Input image paths resolve relative to their enclosing plan, never the current
working directory. Normalization rewrites all paths relative to the build and
pins each file's SHA-256 and dimensions. Optional `sha256`, `width`, `height`
on input layers pin identity before normalization. Target/image binding,
order, anchors, positions, reference/output canvases, and all tracks participate
in the canonical plan digest. The normalized plan is the runtime description;
the original authoring file is not a runtime dependency or an external manifest.
Moving a complete parent tree preserves relative paths and digest. Moving only
a build requires regenerating it with `plan`; paths are not guessed or repaired.

Frame-plan v2 contains the normalized layered `source` plus the existing frame
fields and, on each frame, `global_pose` and an ordered `layers` pose array.
Pose fields are `translation: {x,y}`, `rotate_deg`, `scale`, `opacity`; local
entries also contain `target`. All values are recomputed from the trusted plan.
The loader/validator never repairs expectations from output artifacts.

Built-in output (`render.json` v1) reopens **all** sources, verifies their
identities, recomputes the complete two-stage image, and compares decoded RGBA
exactly. A same-bbox RGB/alpha/order defect fails `FRAME_CONTENT_MISMATCH`.
External frames (no render manifest and no transaction marker) retain full-mode
dimension/alpha/nonempty/naming and modeled composite geometry validation
(2 px tolerance); a flattened image cannot prove the state of hidden layers
or exact colors. No per-layer visibility requirement is imposed.

Full motion is default. `--reduced-motion` honors the plan's mode;
`hold_first_frame` freezes the **entire** frame-0 composite and global pose,
preserving names/count with byte-identical files. Manifest, pixels and mode
must agree. Re-rendering replaces a complete frame generation under the same
M2 exclusive `.render-transaction` marker, backups, rollback and fail-closed
recovery protocol in [renderer.md](renderer.md). All layer images and the
runtime description are immutable. Output symlinks (including dangling links),
overlaps and hard-link aliases are refused. Unknown files are never deleted.

## Errors and compatibility

Shape/type/unknown fields and boolean versions: `MALFORMED_SPEC` (exit 2).
Mixed source modes: `SOURCE_MODE_CONFLICT` (exit 2).
V1 with layers or v2 without layers: `PLAN_SOURCE_VERSION_MISMATCH` (exit 1).
Layer semantics (exit 1): `EMPTY_LAYERS`, `DUPLICATE_LAYER_TARGET`,
`RESERVED_LAYER_TARGET`, `UNKNOWN_LAYER_TARGET`, `INVALID_REFERENCE_CANVAS`,
`INVALID_LAYER_ANCHOR`, `INVALID_LAYER_POSITION`, `INVALID_SOURCE_IDENTITY`.
Source checks reuse `SOURCE_NOT_FOUND`, `SOURCE_INVALID_IMAGE`,
`SOURCE_ALPHA_REQUIRED`, `SOURCE_DIGEST_MISMATCH`, `SOURCE_DIMENSION_MISMATCH`
and add `SOURCE_PNG_REQUIRED`. Effective transform errors and final empty-frame
errors retain M2 codes, plus the finite-composition check above. Frame-plan
edits reuse `FRAME_PLAN_STALE`, `FRAME_PLAN_SOURCE_MISMATCH`,
`PLAN_DIGEST_MISMATCH`. All exits remain 0/1/2/3/4.

Package: 0.5.0. Plan/frame-plan **v2 only for layers**; single-image v1
normalization and pixel algorithm remain unchanged. Old v1 builds still load
with at most the informational `GENERATED_BY_MISMATCH` warning. Frame-plan
version must match its plan's source mode; a v2 label alone cannot upgrade a
v1 build. Render v1 still means digest + mode and requires no shape change.
QA v1 and frame-manifest v1 are unchanged. No existing test assertions need
version migration. M4 generation and M5 export are documented separately below.

## M4/M5 compatibility (package 0.7.0)

Plan and frame-plan versions remain v1 for single images and v2 for layers.
Ordinary render continues writing render v1 with the same pixel algorithm.
`render --generated-input` explicitly selects a validated frozen generation
bundle and writes render v2, binding its request and accepted input digests.
Replacement PNGs must preserve source dimensions and anchor space; all local
composition, global transforms, clipping, displacement constraints and final
pixel checks still apply. Hold freezes frame 0, including replacement selection.
Generation/export QA use v2; existing plan/build/frame QA v1 remains readable.
No event triggers generation. See [generation.md](generation.md),
[adapters.md](adapters.md), [atlas.md](atlas.md) and
[transactions.md](transactions.md). Export reads validated build frames in
frame-plan order, including old v1/v2 and explicit generated-input builds.
