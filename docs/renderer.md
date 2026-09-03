# Deterministic transform renderer (milestones 2 and 3)

`sprite-harness render` turns a validated build directory (one source sprite +
`plan.json` + `frame-plan.json`) into the frame set the frame plan declares.
The single-image M2 path renders **whole-sprite transforms**: translate, rotate,
uniform scale, and opacity applied to the entire source image. It uses Pillow
and pure math — no model APIs, no image generation, no interpolation between
frames. M3 adds explicit layered PNG inputs: local transforms on a reference
canvas, ordered alpha-over composition, then this same global transform once.
See [layered-sprites.md](layered-sprites.md) for the authoritative layered
contract, clipping, identity and version rules.

```bash
sprite-harness render build/ [--reduced-motion] [--overwrite] [--json]
```

- JSON Schema for the render manifest:
  [`schemas/render.schema.json`](../schemas/render.schema.json)
- Renderer module: `sprite_harness.render`; shared geometry:
  `sprite_harness.geometry`

## Inputs and pre-render validation

Rendering consumes only artifacts of an existing build: `plan.json`,
`frame-plan.json`, and all digest-bound source images (one PNG per layer in v2). Before any pixel work,
`render` re-runs the full **input** validation — plan semantics, source
identity (path, SHA-256, dimensions, alpha requirement), and the complete
frame-plan recomputation against `plan_digest` — and refuses to render (exit 1)
if anything fails. A tampered `frame-plan.json`, any replaced or resized source,
or an invalid plan can never be rendered.

Input validation is deliberately separate from rendered-frame validation:
existing broken or stale files under `frames/` never block a re-render (they
are derived output, handled by the overwrite policy below), and rendering never
skips the plan/source/frame-plan integrity checks to get around them.

Renderable builds additionally require:

- a bound source image (`RENDER_SOURCE_REQUIRED` otherwise, exit 4) — a plan
  without a source has nothing to transform;
- `canvas.background: transparent` (`UNSUPPORTED_BACKGROUND` otherwise,
  exit 4) — other background values are metadata the milestone-2 renderer
  cannot honor, and silently rendering them transparent would misrepresent the
  output.

## Coordinate system and per-frame pose

Pixel `(i, j)` covers the unit square `[i, i+1) × [j, j+1)` with center
`(i + 0.5, j + 0.5)`. The x axis points right, the y axis points **down**.
Positive rotation is **clockwise on screen**. All geometry below is expressed
in these continuous pixel coordinates.

For each frame, the sampled `transforms` of the verified frame plan are
composed into one whole-sprite pose. Only tracks with the reserved target
`sprite` participate; every other target is skipped (see below).

| Component | Composition over tracks | Source of values |
| --- | --- | --- |
| translation `(dx, dy)` | sum of translate samples | the frame's `offset` — translate transforms are **not** applied again, so translation is applied exactly once |
| rotation `θ` (degrees) | **sum** of `rotate` samples | `transforms` |
| scale `s` | **product** of the factors `1 + value` per `scale` track | `transforms` |
| opacity `o` | **product** of the factors `1 + value` per `opacity` track, then clamped into `[0, 1]` | `transforms` |

Scale is always uniform — one factor for both axes; there is no per-axis
scaling anywhere in the harness.

Validity of effective values is enforced at plan validation time (so both
`plan` and `render` reject them, exit 1):

- any per-track scale factor `1 + value ≤ 0` → `INVALID_EFFECTIVE_SCALE`;
- any per-track opacity factor `1 + value < 0` → `INVALID_EFFECTIVE_OPACITY`;
- effective opacity exactly `0` on any frame → `FULLY_TRANSPARENT_FRAME`
  (a fully transparent frame would always fail frame validation as
  `FRAME_EMPTY`, so it is rejected up front).

Opacity above `1` is **clamped to 1 silently**; the clamp is part of the
defined transfer function (like CSS opacity), not an anomaly. In v1 these rules apply to `sprite` tracks; local labels remain advisory.
In v2 every rendered target is checked, with zero local opacity allowed. Raw
products, sums and affine coefficients must stay finite before opacity clamping
(`NONFINITE_EFFECTIVE_TRANSFORM`); scale underflow to zero is invalid.

## Anchor and placement

The plan's anchor (`bottom_center` = `(0.5, 1.0)`, `center` = `(0.5, 0.5)`, or
`custom` `(x, y)`) resolves to two concrete points:

- source anchor `A_src = (source_width · x, source_height · y)`
- canvas anchor `A_dst = (canvas_width · x, canvas_height · y)`

The forward map of a source point `p` for a frame with pose
`(dx, dy, θ, s, o)` is:

```text
P = A_dst + (dx, dy) + R(θ) · s · (p − A_src)
R(θ) = [[cos θ, −sin θ], [sin θ, cos θ]]   (clockwise for θ > 0 with y down)
```

The source anchor therefore lands on the canvas anchor plus the frame offset
on every frame, and rotation and scale both pivot around that same stable
anchor point. This holds for any source/canvas size combination — a source
smaller or larger than the canvas is placed purely by anchor alignment, never
stretched to fit.

The canvas is fixed at the frame plan's `canvas.width × canvas.height` for
every frame and never grows to fit a transformed sprite. Content that a
transform pushes past the canvas edge is clipped; the validator reports
`CONTENT_TOUCHES_EDGE` as a warning when visible pixels touch the border.

## Resampling, rounding, determinism

- **Exact path** — when a frame's pose is a pure translation (`θ = 0`,
  `s = 1`) and the total placement `A_dst + (dx, dy) − A_src` is integral,
  the source is copied pixel-for-pixel at that integer position (clipped by
  the canvas). Static frames and integer translations are exact copies of the
  source.
- **Resampling path** — every other pose uses one inverse affine transform
  (Pillow `Image.transform` with explicit `Resampling.BILINEAR` and a fully
  transparent `fillcolor`), evaluated at output pixel centers as defined
  above. Bilinear interpolation is the explicit, documented interpolation
  choice; no Pillow default is relied on. Pillow's fixed-point arithmetic may
  differ from ideal real-valued sampling by ±1/255 per channel; the
  validator's 2 px measurement tolerance absorbs this.
- **Opacity** — applied after the geometric transform to the alpha channel
  only, through the lookup table `alpha_out = floor(alpha_in · o + 0.5)`.
- Pillow's RGBA bilinear affine path resamples premultiplied color, then
  converts back to straight RGBA. Transparent fill is black with alpha zero;
  opacity is subsequently applied to alpha only.
- Rendering is deterministic: the same build, mode, and environment (Python
  and Pillow versions) produce byte-identical PNGs. Frames carry no
  timestamps, no random metadata, and no absolute paths, and the renderer
  never consumes `plan.seed` (used by explicit generation request derivation, milestone 4).

## Single-image target-local tracks are skipped, loudly

Tracks whose `target` is not `sprite` (e.g. `head`, `hand_right`) cannot be
rendered from a flattened sprite. The renderer:

- skips them and reports the stable warning `TARGET_TRACKS_SKIPPED` with the
  affected track ids and targets, in both human and JSON output;
- never folds them into the whole-sprite pose or the global offset;
- never claims the motion was rendered.

V2 layered plans instead bind each local target to an explicit PNG and render
its local transforms. Unknown targets are errors; no layer is inferred.

## Reduced motion

The plan's `reduced_motion.mode` (`full` or `hold_first_frame`) declares what
a reduced-motion variant of the animation is. `render` renders the **full**
variant by default; `--reduced-motion` renders the variant the plan declares:

- mode `full`: the reduced variant is identical to the full render;
- mode `hold_first_frame`: the complete frame-0 pose/composite is rendered once and written to
  **every** declared frame file — the frame count and `frames/frame_NNN.png`
  naming are preserved, and all frames are byte-identical.

The effective mode of the rendered frame set is recorded in the render
manifest (below) so validation, preview, and QA always judge the output by the
mode it was actually rendered in. Full and reduced outputs live in the same
`frames/` slot of a build, so they never mix: re-rendering in the other mode
replaces the whole frame set and its manifest under the transaction guard
(with `--overwrite`). Regenerate preview/contact-sheet/QA after a successful
re-render; existing derived previews and reports are snapshots, not live views.

## The render manifest (`build/render.json`)

A successful render writes `render.json`
([schema](../schemas/render.schema.json)):

```json
{
  "render_version": 1,
  "animation_id": "eating_loop",
  "generated_by": "sprite-harness 0.5.0",
  "plan_digest": "sha256:…",
  "mode": "full"
}
```

`plan_digest` binds the manifest to the plan revision that produced the
frames; `mode` is the effective render mode. `generated_by` is informational
provenance with the same rules as the frame plan's. The manifest is written
**last**, after the complete staged frame directory is in place. A render is
complete only after `.render-transaction/` is removed. An interrupted
transaction is an error even if `render.json` is absent (never an implicit
external full-motion build).

Validation of a build with rendered frames reads the manifest:

- active/interrupted `.render-transaction/` → `RENDER_TRANSACTION_INCOMPLETE`,
  with no frame validation or preview allowed until recovery;
- absent manifest and no transaction → the frame set is judged as `full` motion (backward
  compatible with externally rendered milestone-1 builds);
- malformed shape, unknown/missing fields, or a bad mode value →
  `MALFORMED_RENDER_MANIFEST`; an unsupported `render_version` →
  `UNSUPPORTED_RENDER_MANIFEST_VERSION`; a wrong `animation_id` →
  `ANIMATION_ID_MISMATCH`;
- `render_version` must be a canonical integer (not a boolean, float, string,
  null, array, or object); type violations are `MALFORMED_RENDER_MANIFEST`;
- `plan_digest` differing from the current plan → `RENDER_MANIFEST_STALE`;
- `mode: hold_first_frame` on a plan whose `reduced_motion.mode` is `full` →
  `RENDER_MODE_MISMATCH`;
- in `hold_first_frame` mode every frame must be byte-identical to frame 0
  (`HOLD_FRAME_MISMATCH` otherwise), and geometry is judged against the
  frame-0 pose — never against the full-motion offsets.

## How rendered frames are verified

Frame validation never derives expectations from the frames under test.
Expectations come from the trusted, digest-verified inputs:

- **Built-in renders with a valid `render.json`** also undergo exact decoded
  RGBA comparison against the bound source rendered at each verified pose
  (`FRAME_CONTENT_MISMATCH`). This catches wrong colors, opacity, shape, and
  swapped pixels even when the bounding box is unchanged. Missing trusted
  pixels are an error (`FRAME_CONTENT_UNVERIFIED`). PNG encoding/metadata may
  differ if decoded pixels agree (hold mode still requires byte identity).
  Pixel expectations are recomputed, not copied from hashes supplied by the
  frame set. Exact comparison requires the same rendering environment;
  legitimate resampling differences across Pillow versions require re-rendering.
- **Builds with a bound source** are judged model-based for every pose kind:
  the validator transforms the trusted source image's alpha channel through
  the same documented pose geometry and compares the expected bounding-box
  center and bottom (clipped to the canvas exactly like real output) against
  the measured frame, within a fixed 2 px tolerance. Legal
  translation/rotation/scale/opacity — including translation that clips at
  the canvas edge — does not register as drift. Geometric mismatches fail
  (`BBOX_DRIFT_EXCEEDED`, `GROUND_DRIFT_EXCEEDED`, and the existing
  dimension/alpha/naming checks). Geometry alone does not establish pixel
  identity: external frames without a render manifest retain this contract
  and may intentionally contain different artwork at the planned geometry.
- **Builds without a bound source** (externally rendered milestone-1
  workflows) keep the milestone-1 relative check when every pose is a pure
  translation (`θ = 0`, `s = 1`, `o = 1`, including `hold_first_frame`
  output): measured alpha bounding-box centers and bottoms must track the
  recomputed per-frame offsets relative to a reference frame, within the same
  2 px tolerance. If such a build has rotation/scale/opacity tracks, the
  geometry cannot be modeled from trusted inputs; the validator emits the
  stable warning `GEOMETRY_UNVERIFIED` and skips only the bbox/ground checks
  instead of guessing. It never fabricates expectations from the output
  itself.
- The measured frame-to-frame delta check (`FRAME_DELTA_EXCEEDED`) applies on
  the no-source relative path; on the model-based path every frame is already
  bounded absolutely by its own modeled expectation, and the plan-stage
  offset-delta constraint remains enforced.
- A frame with no visible pixels is always `FRAME_EMPTY`; a transform chain
  that would produce one fails earlier (`FULLY_TRANSPARENT_FRAME` at plan
  validation, `RENDERED_FRAME_EMPTY` at render time if clipping or extreme
  scaling empties a frame).

The renderer and the validator share the geometry module by design; the test
suite therefore contains independent small-image reference tests whose
expected pixel positions are hand-computed (e.g. a single-pixel sprite rotated
90° about a known anchor), so a bug shared by renderer and validator still
fails the suite.

## Output safety and overwrite policy

- All source images and the runtime layer description are read-only; rendering never modifies, renames, or deletes
  it (tests verify the source hash is unchanged by a render).
- `.render-transaction/` is created exclusively as the writer lock, staging
  area, recovery directory, and fail-closed marker. A second writer is refused;
  validators and preview commands refuse active/interrupted transactions.
- All frames and the new manifest are staged before publication. Old frames
  and manifest are renamed to `previous-frames/` and `previous-render.json`
  inside the transaction; the complete `new-frames/` directory is published
  in one rename, followed by `new-render.json`. Publication exceptions reverse
  all successful renames. Staging failures leave old output untouched.
- Successful commit/rollback removes the transaction. If rollback or cleanup
  fails, `RENDER_RECOVERY_REQUIRED` preserves the remaining recovery material.
  Abrupt process termination also leaves the marker, so no mixed or incomplete
  set is accepted as external frames. This is exception recovery and detection
  of interrupted processes, not a power-loss durability guarantee or a
  filesystem snapshot for concurrent readers. Retry validation after rendering.
- Output directories, manifest paths, and frame entries must not be symlinks
  (including dangling links); non-regular frame entries are refused. Source
  paths inside the output slot or hard-link aliases of the source are refused
  as `FRAMES_DIR_CONFLICT`. The slot is checked before rendering and again
  before publication. This does not defend against a hostile process racing
  arbitrary filesystem replacements between individual system calls.
- If `frames/` already contains any declared frame file, or `render.json`
  exists, `render` refuses by default (`FRAMES_ALREADY_RENDERED`, exit 4).
  `--overwrite` allows the re-render; its scope is exactly the declared
  derived products — the frame files named by the frame plan plus
  `render.json`. Files in `frames/` that the frame plan does not declare are
  never deleted: they abort the render (`FRAMES_DIR_CONFLICT`, exit 4) until
  the user moves them away.

### Recovery after an interrupted process

Do not delete `.render-transaction/` just to silence the error. First ensure no
writer is running and preserve the whole build, including the transaction.
Inspect the contents: `previous-frames/` and `previous-render.json` are the
old generation (if they existed); `new-frames/` and `new-render.json` are the
staged generation, and missing staged paths may already be published at the
build root. Restore **one complete matching generation**, moving any displaced
files aside rather than deleting them. Only then move the transaction directory
out of the build and run `validate --write-qa`; regenerate previews. Automatic
recovery is deliberately not guessed from a partially recovered directory.

## Result reporting

Success (exit 0) reports, in human and `--json` form: the frame count, the
frames directory and manifest path, the effective render mode, and any
capability warnings (`TARGET_TRACKS_SKIPPED`). The renderer never describes
skipped target-local motion as rendered.

## Error codes and exits

Exit codes keep the shared contract (0 success, 1 validation failure, 2
malformed specification, 3 missing input, 4 processing failure).

| Code | Exit | Meaning |
| --- | --- | --- |
| `RENDER_SOURCE_REQUIRED` | 4 | Build has no bound source image to transform. |
| `UNSUPPORTED_BACKGROUND` | 4 | Canvas background is not `transparent`. |
| `FRAMES_ALREADY_RENDERED` | 4 | Declared output exists and `--overwrite` was not given. |
| `FRAMES_DIR_CONFLICT` | 4 | `frames/` holds files the frame plan does not declare; nothing is deleted. |
| `RENDER_TRANSACTION_INCOMPLETE` | 1 validate / 4 render | Active or interrupted transaction; rendering and consumers are blocked. |
| `RENDER_RECOVERY_REQUIRED` | 4 | Publication rollback or transaction cleanup failed; recovery material is retained. |
| `FRAME_PATH_OUTSIDE_BUILD` | 1 | Frame path leaves the build or is a symbolic link. |
| `FRAME_CONTENT_MISMATCH` | 1 | Built-in output RGBA differs from the recomputed source transform. |
| `FRAME_CONTENT_UNVERIFIED` | 1 | Built-in render manifest has no readable source for pixel verification. |
| `RENDERED_FRAME_EMPTY` | 4 | A composed frame has no visible pixels (extreme scale/clipping). |
| `RENDER_SOURCE_UNREADABLE` | 4 | The source became unreadable between validation and rendering (defensive; input validation normally reports `SOURCE_INVALID_IMAGE` first). |
| `INVALID_EFFECTIVE_SCALE` | 1 | A sprite scale track reaches a factor ≤ 0 (plan stage). |
| `INVALID_EFFECTIVE_OPACITY` | 1 | A sprite opacity track reaches a factor < 0 (plan stage). |
| `FULLY_TRANSPARENT_FRAME` | 1 | Effective opacity is 0 on some frame (plan stage). |
| `MALFORMED_RENDER_MANIFEST` | 1 | `render.json` shape/fields/mode invalid (validate stage). |
| `UNSUPPORTED_RENDER_MANIFEST_VERSION` | 1 | Unknown `render_version` (validate stage). |
| `RENDER_MANIFEST_STALE` | 1 | Manifest digest does not match the current plan (validate stage). |
| `RENDER_MODE_MISMATCH` | 1 | Manifest mode conflicts with the plan's reduced-motion declaration. |
| `HOLD_FRAME_MISMATCH` | 1 | `hold_first_frame` output frames are not byte-identical. |
| Warnings | — | `TARGET_TRACKS_SKIPPED` (render), `GEOMETRY_UNVERIFIED` (validate, no source to model against). |

Pre-render input validation failures reuse the existing plan/build codes
(`FRAME_PLAN_STALE`, `PLAN_DIGEST_MISMATCH`, `SOURCE_DIGEST_MISMATCH`, …;
layer-specific errors in [layered-sprites.md](layered-sprites.md)) at
exit 1; a missing `plan.json`/`frame-plan.json` is exit 3; unreadable JSON is
exit 2.

## Limitations (deliberate)

- Layered motion requires explicitly provided PNGs. No automatic decomposition,
  skeletons, parent-child joints, IK, meshes or complex masks. Single-image
  target-local tracks still produce the skipped warning.
- Optional source-space generation is explicit and outside the core; no provider
  SDKs in the core, interpolation, optical flow or video output.
- Only `transparent` backgrounds render.
- Exact built-in pixel verification assumes the same rendering environment;
  geometry-only external validation does not prove artwork identity.

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
