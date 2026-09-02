# Animation Plan v1

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
with concrete sampled transform values. `sprite-harness render` (milestone 2,
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
| `plan_version` | yes | Const `1`. |
| `animation_id` | yes | Filesystem-safe slug. |
| `source.image` | no | Source sprite path, relative to the plan file; `--source` overrides it. The source is immutable input. |
| `source.sha256`, `source.width`, `source.height` | no | Expected source identity. Generated `plan.json` always records them (with `image` rewritten to resolve from inside the build directory), binding the source into `plan_digest`; declaring them in an input spec pins the source. Build validation re-inspects the file against them. |
| `canvas` | no | Output `width`/`height` and `background` (default `transparent`). Omitted canvas inherits the source dimensions; a plan with neither cannot expand (`CANVAS_UNRESOLVED`). |
| `playback` | yes | `fps` (> 0), `frame_count` (≥ 1), `loop`. |
| `anchor` | no | `bottom_center` (default), `center`, or `custom` with normalized `x`/`y`. The anchor is the stable reference point (e.g. ground contact). |
| `seed` | no | Deterministic seed reserved for stochastic stages (milestone 4). Deterministic stages never consume it. |
| `constraints` | no | `max_displacement_px` (per-axis offset budget from the base pose) and `max_frame_delta_px` (per-axis change between consecutive frames, including the loop seam). |
| `reduced_motion.mode` | no | `full` (default) or `hold_first_frame`; a directive for runtimes honoring OS reduced-motion preferences. |
| `tracks` | no | Deterministic motion tracks (below). |
| `events` | no | Discrete per-frame annotations, e.g. blink (below). |
| `metadata` | no | Free-form consumer data; the harness never interprets it. Values must be JSON-compatible (null, booleans, integers, finite floats, strings, arrays, objects with string keys); YAML-only values such as dates, sets, and non-finite numbers are rejected (`METADATA_NOT_JSON_COMPATIBLE`, exit 2). |

## Tracks

A track applies one motion to one semantic target:

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

- `motion` / `unit` pairs: `translate_x`/`translate_y` → `px`, `rotate` →
  `deg`, `scale`/`opacity` → `ratio` (effective value is `1 + sampled value`).
  Across multiple `sprite` tracks of one motion, rotate samples add and
  scale/opacity factors multiply; effective opacity is clamped into `[0, 1]`.
  A sprite scale factor reaching zero or below, a negative opacity factor, or
  a frame with effective opacity exactly zero is rejected at plan validation
  (`INVALID_EFFECTIVE_SCALE`, `INVALID_EFFECTIVE_OPACITY`,
  `FULLY_TRANSPARENT_FRAME`) — see [`docs/renderer.md`](renderer.md).
- The reserved target `sprite` addresses the whole sprite. Every other
  `target` is an advisory semantic part label (`head`, `hand_right`, …); the
  harness does not claim an arbitrary flattened sprite can be decomposed into
  these parts, and renderers decide what they can honor. Labels stay
  provider- and character-neutral.
- The sampled value of a track at frame `i` of `n` is
  `amplitude × curve(u)` with `u = frac((i / period) × cycles + phase)`, where
  `period = n` for loops and `n − 1` otherwise.
- Curves: `sine` and `triangle` are periodic in `[-1, 1]` and start at 0.
  `linear`, `ease_in`, `ease_out`, `ease_in_out` are mirrored (ping-pong)
  inside each cycle in `[0, 1]`. `hold` is constant 0.
- Loop continuity: when `playback.loop` is true, every track's `cycles` must
  be a positive integer (`NON_INTEGRAL_LOOP_CYCLES` otherwise). Whole cycles
  make the sampled sequence exactly periodic, so every curve — periodic or
  mirrored easing, at any phase — returns to its frame-0 value without a
  position jump at the loop seam. Non-looping animations may use positive
  fractional cycles.
- Only translate tracks targeting `sprite` are aggregated per frame into the
  whole-sprite pixel `offset` (x right, y down) that the validator checks
  against `constraints` and, once frames exist, against measured bounding
  boxes and the ground line. Target-local tracks are expanded per frame in
  `transforms` but never move the aggregate offset — milestone 1 cannot verify
  target-local pixels until a renderer/layer contract exists (milestone 3).

## Events

Events mark discrete moments (blink timing, chew beats) without pretending to
be continuous motion:

```json
{ "event_id": "blink_mid", "type": "blink", "target": "eyes", "frames": [5, 6] }
```

`type` is a free string; frame indices must be in range and event ids unique.
The expansion lists active event ids per frame.

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
`NON_INTEGRAL_LOOP_CYCLES`, `INVALID_PHASE`, `DUPLICATE_EVENT_ID`,
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
for YAML metadata that cannot be represented as standard JSON.

Exit codes follow the shared contract in
[`docs/animation-spec.md`](animation-spec.md#exit-code-contract).
