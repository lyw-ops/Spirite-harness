# Animation Plans v1 and v2

The Animation Plan (动画计划) is the declarative intermediate representation
between a static source sprite and rendered animation frames. It is
character-neutral and renderer-neutral: it says *what should move, how much,
and when*, without prescribing how pixels are produced.

- JSON Schema: [`schemas/animation-plan.schema.json`](../schemas/animation-plan.schema.json)
- Typed representation: `sprite_harness.plan.AnimationPlan`
- Example: [`examples/reimu-eating/eating-loop.json`](../examples/reimu-eating/eating-loop.json)

A plan file may be JSON or YAML. `sprite-harness plan` normalizes it into a
canonical `plan.json` and deterministically expands it into a
[`frame-plan.json`](../schemas/frame-plan.schema.json) — one entry per frame
with concrete sampled transform values. V2 binds explicitly supplied PNG layers;
[the layered contract](layered-sprites.md) defines its source and pose fields. `sprite-harness render` (milestones 2/3,
see [`docs/renderer.md`](renderer.md)) turns those values into
`build/frames/`.

```bash
sprite-harness plan --spec animation.json --source base.png --output build/
sprite-harness render build/
sprite-harness validate build/ --write-qa
```

## Fields

| Field | Required | Meaning |
| --- | --- | --- |
| `plan_version` | yes | `1` for single-image / external plans; `2` for explicit layered plans. |
| `animation_id` | yes | Filesystem-safe slug. |
| `source.image` | no | Source sprite path, relative to the plan file; `--source` overrides it. The source is immutable input. |
| `source.sha256`, `source.width`, `source.height` | no | Expected source identity. Generated `plan.json` always records them (with `image` rewritten to resolve from inside the build directory), binding the source into `plan_digest`; declaring them in an input spec pins the source. Build validation re-inspects the file against them. |
| `source.layers`, `source.reference_canvas` | v2 | Nonempty ordered PNG layers and explicit reference dimensions. Each layer requires target/image/anchor/position, may pin SHA-256/dimensions. Exclusive with source.image and --source; see [layered-sprites.md](layered-sprites.md). |
| `canvas` | no | Output `width`/`height` and `background` (default `transparent`). Omitted canvas inherits source dimensions (v1) or reference dimensions (v2); a plan with neither cannot expand (`CANVAS_UNRESOLVED`). |
| `playback` | yes | `fps` (> 0), `frame_count` (≥ 1), `loop`. |
| `anchor` | no | `bottom_center` (default), `center`, or `custom` with normalized `x`/`y`. The anchor is the stable reference point (e.g. ground contact). |
| `seed` | no | Explicit generation seed (M4); required only for generation requests. Deterministic transforms never consume it. |
| `constraints` | no | `max_displacement_px` (per-axis offset budget from the base pose) and `max_frame_delta_px` (per-axis change between consecutive frames, including the loop seam). |
| `reduced_motion.mode` | no | `full` (default) or `hold_first_frame`; a directive for runtimes honoring OS reduced-motion preferences. |
| `tracks` | no | Deterministic motion tracks (below). |
| `events` | no | Discrete per-frame annotations, e.g. blink (below). |
| `metadata` | no | Free-form consumer data; the harness never interprets it. Values must be JSON-compatible (null, booleans, integers, finite floats, strings, arrays, objects with string keys); YAML-only values such as dates, sets, and non-finite numbers are rejected (`METADATA_NOT_JSON_COMPATIBLE`, exit 2). |

## Tracks

A track applies one motion to one semantic target. It comes in exactly one of
two kinds: a **curve track** (an `amplitude` scaled by a whole-cycle curve) or
a **keyframe track** (an explicit piecewise timeline). The field sets are
mutually exclusive: `keyframes` never appears together with `amplitude`,
`curve`, `cycles`, `phase`, or `duty_cycle` (`TRACK_MODE_CONFLICT`, exit 2).

Both kinds share the target and composition rules:

- `motion` / `unit` pairs: `translate_x`/`translate_y` → `px`, `rotate` →
  `deg`, `scale`/`opacity` → `ratio` (effective value is `1 + sampled value`).
  Across multiple tracks for the same rendered target of one motion, rotate samples add and
  scale/opacity factors multiply; effective opacity is clamped into `[0, 1]`.
  A sprite scale factor reaching zero or below, a negative opacity factor, or
  a frame with effective opacity exactly zero is rejected at plan validation
  (`INVALID_EFFECTIVE_SCALE`, `INVALID_EFFECTIVE_OPACITY`,
  `FULLY_TRANSPARENT_FRAME`) — see [`docs/renderer.md`](renderer.md).
- The reserved target `sprite` addresses the whole sprite. In single-image v1, every other
  `target` is an advisory semantic part label (`head`, `hand_right`, …); the
  harness does not claim an arbitrary flattened sprite can be decomposed into
  these parts, and renderers decide what they can honor. Labels stay
  provider- and character-neutral. In v2 every local target must bind a declared
  PNG layer; unknown track/event targets fail `UNKNOWN_LAYER_TARGET`. Array
  order is back to front. All local transforms are rendered and digest-bound.

### Curve tracks

```json
{
  "track_id": "breathing",
  "target": "sprite",
  "motion": "translate_y",
  "amplitude": 1.5,
  "unit": "px",
  "curve": "sine",
  "cycles": 1,
  "phase": 0.75
}
```

- The sampled value of a track at frame `i` of `n` is
  `amplitude × curve(u)` with `u = frac((i / period) × cycles + phase)`, where
  `period = n` for loops and `n − 1` otherwise.
- Curves: `sine` and `triangle` are periodic in `[-1, 1]` and start at 0.
  `linear`, `ease_in`, `ease_out`, `ease_in_out` are mirrored (ping-pong)
  inside each cycle in `[0, 1]`. `pulse` is a discrete periodic curve: it is
  `+1` while `u < duty_cycle` and `-1` for the rest of the cycle;
  `duty_cycle` defaults to `0.5`, must be in `(0, 1]`, and is invalid on other
  curves. `hold` is constant 0.
- A pulse gives complementary binary opacity without cross-fading: bind two
  layers to the same pulse and use amplitude `-1` on the normally visible
  layer and `+1` on the pulse-visible layer. Their effective opacity factors
  are exactly `0`/`2` before the documented `[0,1]` clamp, so exactly one
  layer is visible at every sampled frame.
- Loop continuity: when `playback.loop` is true, every track's `cycles` must
  be a positive integer (`NON_INTEGRAL_LOOP_CYCLES` otherwise). Whole cycles
  make the sampled sequence exactly periodic, so every curve returns to its
  frame-0 value at the next cycle boundary. `pulse` deliberately contains a
  discrete edge; place it away from the loop seam unless that edge is the
  intended transition. Non-looping animations may use positive fractional
  cycles.

### Keyframe tracks

Multi-phase motion with per-phase durations and shapes (approach, hold, snap
back, settle) replaces the curve fields with an explicit piecewise timeline:

```json
{
  "track_id": "food_approach",
  "target": "held_food",
  "motion": "translate_y",
  "unit": "px",
  "keyframes": [
    {"at": 0.0,  "value": -5,  "interpolation": "ease_in_out"},
    {"at": 0.28, "value": -14, "interpolation": "ease_in"},
    {"at": 0.4,  "value": -16, "interpolation": "ease_out"},
    {"at": 0.52, "value": -7,  "interpolation": "hold"},
    {"at": 0.82, "value": -7,  "interpolation": "ease_in_out"}
  ]
}
```

- `at` is normalized loop time, independent of FPS and frame count. Frame `i`
  of `n` samples time `u = i / n` for loops (positions stay in `[0, 1)`; time
  1 is the seam and belongs to the next repetition's frame 0) and
  `u = i / (n − 1)` otherwise (the final frame samples exactly 1).
- A track needs at least one keyframe (`INSUFFICIENT_KEYFRAMES`; a single
  keyframe is a constant). Times must be finite, the first must be exactly 0,
  and they must increase strictly; looping playback requires every `at` below
  1, non-looping playback allows the final keyframe exactly at 1
  (`INVALID_KEYFRAME_TIME`). Values must be finite
  (`INVALID_KEYFRAME_VALUE`).
- `value` is the direct sampled track value at that time — no amplitude is
  involved. It uses the same composition semantics as curve-track samples: a
  pixel offset for `translate_*`, degrees for `rotate`, and for
  `scale`/`opacity` the ratio whose effective factor is `1 + value`, with all
  existing effective-value rules (`INVALID_EFFECTIVE_SCALE`,
  `INVALID_EFFECTIVE_OPACITY`, `FULLY_TRANSPARENT_FRAME`) unchanged.
- Each keyframe's `interpolation` shapes the segment to the *next* keyframe:
  `linear`, `ease_in` (`t²`), `ease_out` (`1 − (1 − t)²`), `ease_in_out`
  (smoothstep `t²(3 − 2t)`), or `hold`. `hold` keeps the keyframe's value for
  the whole segment and steps exactly on the next keyframe's `at` — discrete
  switches never produce partially interpolated frames. The default is
  `linear`; anything else is `UNSUPPORTED_INTERPOLATION`.
- Sampling exactly at a keyframe's `at` returns its `value` exactly; between
  keyframes the segment interpolates `value₀ + (value₁ − value₀) ×
  ease(t)` with `t = (u − at₀) / (at₁ − at₀)`. Every sampled value is then
  rounded to six decimals exactly like curve-track samples.
- **Loop closure:** when `playback.loop` is true the timeline's final segment
  runs from the last keyframe back to the *first keyframe's value*, reaching
  it exactly at time 1 — which is the same instant as time 0 of the next
  repetition — shaped by the last keyframe's `interpolation`. Continuous
  shapes therefore close the seam without a jump; a `hold` last segment keeps
  the last value through the seam and steps to the first value exactly on
  frame 0. Keyframe tracks declare no `cycles`, and the integer-cycles loop
  rule does not apply to them; the wrap segment is their loop-continuity
  contract.
- **Non-looping tail:** when the last keyframe sits before time 1 the value
  holds from that keyframe to the final frame; the last keyframe's
  `interpolation` only takes effect in looping playback.
- Keyframed `opacity` with `hold` segments and values `-1`/`0` gives exact
  `0`/`1` factors — mutually exclusive layered variants (mouth shapes, eye
  states) switch discretely with no cross-fade frame, with arbitrary
  per-phase timing.

### Offsets and constraints

- Only translate tracks targeting `sprite` are aggregated per frame into the
  whole-sprite pixel `offset` (x right, y down) that the validator checks
  against `constraints` and, once frames exist, against measured bounding
  boxes and the ground line. Target-local tracks are expanded per frame in
  `transforms` but never move the aggregate offset — v1 skips them; v2 renders them in reference-canvas coordinates before
  applying the global sprite pose once. Constraints remain global-only.

## Events

Events mark discrete moments (blink timing, chew beats) without pretending to
be continuous motion:

```json
{ "event_id": "blink_mid", "type": "blink", "target": "eyes", "frames": [5, 6] }
```

`type` is a free string; frame indices must be in range and event ids unique.
The expansion lists active event ids per frame. Event names do not trigger
pixel actions in either mode.

## Determinism and integrity

Expansion is pure math: the same plan always yields a byte-identical
`plan.json`, `frame-plan.json`, and `qa/plan.qa.json` (values rounded to six
decimals, no timestamps). All JSON boundaries are strict: artifacts and
`--json` output never contain `NaN`/`Infinity` tokens; non-finite numbers in
diagnostics are rendered as the strings `"NaN"`, `"Infinity"`, `"-Infinity"`.

`frame-plan.json` embeds `plan_digest`, the SHA-256 of the canonical
normalized plan, and build validation recomputes the entire expected frame
plan from `plan.json` alone — never from the frame plan under test — and
compares every authoritative section in canonical JSON form. A stale pairing
fails with `PLAN_DIGEST_MISMATCH`; hand-edited playback/canvas/anchor/
reduced-motion/frame content (values or types) fails with `FRAME_PLAN_STALE`
naming the section; unknown or missing fields fail with
`MALFORMED_FRAME_PLAN`; an edited source binding fails with
`FRAME_PLAN_SOURCE_MISMATCH`. `generated_by` is informational provenance: it
must look like `sprite-harness <version>`, and a different release produces
only the `GENERATED_BY_MISMATCH` warning.

When the build was created with a source image, `plan.json` records the
source path (resolving from inside the build directory) plus its SHA-256 and
dimensions, all covered by `plan_digest`. `validate` re-opens the source and
fails on `SOURCE_NOT_FOUND`, `SOURCE_INVALID_IMAGE`, `SOURCE_DIGEST_MISMATCH`,
`SOURCE_DIMENSION_MISMATCH`, or `SOURCE_ALPHA_REQUIRED`. The source is only
ever read, never modified.

## Validation error codes

Plan-stage codes: `UNSUPPORTED_PLAN_VERSION`, `INVALID_ANIMATION_ID`,
`INVALID_FPS`, `INVALID_FRAME_COUNT`, `INVALID_CANVAS_SIZE`, `INVALID_ANCHOR`,
`INVALID_SEED`, `INVALID_CONSTRAINT`, `UNSUPPORTED_REDUCED_MOTION`,
`INVALID_SOURCE_IDENTITY`, `DUPLICATE_TRACK_ID`, `UNSUPPORTED_MOTION`,
`UNIT_MISMATCH`, `UNSUPPORTED_CURVE`, `INVALID_AMPLITUDE`, `INVALID_CYCLES`,
`NON_INTEGRAL_LOOP_CYCLES`, `INVALID_PHASE`, `INVALID_DUTY_CYCLE`,
`DUTY_CYCLE_REQUIRES_PULSE`, `INSUFFICIENT_KEYFRAMES`,
`INVALID_KEYFRAME_TIME`, `INVALID_KEYFRAME_VALUE`,
`UNSUPPORTED_INTERPOLATION`, `DUPLICATE_EVENT_ID`,
`EVENT_FRAME_OUT_OF_RANGE`, `DISPLACEMENT_EXCEEDED`, `FRAME_DELTA_EXCEEDED`,
`SOURCE_NOT_FOUND`, `SOURCE_INVALID_IMAGE`, `SOURCE_ALPHA_REQUIRED`,
`SOURCE_DIGEST_MISMATCH`, `SOURCE_DIMENSION_MISMATCH`, `CANVAS_UNRESOLVED`,
`INVALID_EFFECTIVE_SCALE`, `INVALID_EFFECTIVE_OPACITY`,
`FULLY_TRANSPARENT_FRAME`.
Warnings: `ZERO_MOTION`, `CANVAS_SOURCE_MISMATCH`.

Build/frame-stage codes: `UNSUPPORTED_FRAME_PLAN_VERSION`,
`ANIMATION_ID_MISMATCH`, `PLAN_DIGEST_MISMATCH`, `MALFORMED_FRAME_PLAN`,
`FRAME_PLAN_COUNT_MISMATCH`, `FRAME_PLAN_INDEX_GAP`, `FRAME_PLAN_STALE`,
`FRAME_PLAN_SOURCE_MISMATCH`, `SOURCE_NOT_FOUND`, `SOURCE_INVALID_IMAGE`,
`SOURCE_ALPHA_REQUIRED`, `SOURCE_DIGEST_MISMATCH`,
`SOURCE_DIMENSION_MISMATCH`, `FRAME_MISSING`, `UNEXPECTED_FRAME_FILE`,
`FRAME_INVALID_IMAGE`, `FRAME_DIMENSION_MISMATCH`, `FRAME_ALPHA_REQUIRED`,
`FRAME_EMPTY`, `BBOX_DRIFT_EXCEEDED`, `GROUND_DRIFT_EXCEEDED`,
`FRAME_DELTA_EXCEEDED`, `MALFORMED_RENDER_MANIFEST`,
`UNSUPPORTED_RENDER_MANIFEST_VERSION`, `RENDER_MANIFEST_STALE`,
`RENDER_MODE_MISMATCH`, `HOLD_FRAME_MISMATCH`, `RENDER_TRANSACTION_INCOMPLETE`,
`FRAMES_DIR_CONFLICT`, `FRAME_PATH_OUTSIDE_BUILD`, `FRAME_CONTENT_MISMATCH`,
`FRAME_CONTENT_UNVERIFIED`. Warnings:
`CONTENT_TOUCHES_EDGE` (possible cropping), `GENERATED_BY_MISMATCH` (build
produced by a different harness release), `GEOMETRY_UNVERIFIED`
(rotate/scale/opacity with no bound source to model against).
Geometric checks use a fixed 2 px tolerance for subpixel rendering;
builds with a bound source are verified against the source image transformed
through the documented pose geometry. Built-in outputs with `render.json`
additionally require exact decoded RGBA agreement with that recomputation;
external frame sets keep the geometric contract (see [`docs/renderer.md`](renderer.md)).

Render-stage codes (exit 4, `sprite-harness render`):
`RENDER_SOURCE_REQUIRED`, `UNSUPPORTED_BACKGROUND`, `FRAMES_ALREADY_RENDERED`,
`FRAMES_DIR_CONFLICT`, `RENDERED_FRAME_EMPTY`, `RENDER_SOURCE_UNREADABLE`,
`RENDER_TRANSACTION_INCOMPLETE`, `RENDER_RECOVERY_REQUIRED`.
Warning: `TARGET_TRACKS_SKIPPED`.

Loading errors (exit 2) additionally include `METADATA_NOT_JSON_COMPATIBLE`
for YAML metadata that cannot be represented as standard JSON, and
`TRACK_MODE_CONFLICT` for a track mixing `keyframes` with curve-track fields.

Exit codes follow the shared contract in
[`docs/animation-spec.md`](animation-spec.md#exit-code-contract).

## V2 additions and compatibility

See [layered-sprites.md](layered-sprites.md) for the complete v2 source/pose
schema, errors and coordinate contract. Local zero opacity and invisible layers
are legal; negative opacity, nonpositive scale and non-finite effective chains
are errors. V2 frame plans include every layer binding and ordered per-frame
local poses plus the global pose. All sources are re-inspected and all sections
are recomputed from the normalized plan. Built-in final RGBA is compared exactly.

Single-image v1 artifacts keep their original structure and digest semantics;
only invalid non-finite effective transform chains gain an explicit rejection.
V1/frame-plan versions must be canonical integers. Render/QA/frame-manifest
versions remain 1; only the layered plan/frame-plan use version 2.

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
