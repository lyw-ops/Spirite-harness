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
with concrete sampled transform values. No pixels are synthesized in
milestone 1.

```bash
sprite-harness plan --spec animation.json --source base.png --output build/
sprite-harness validate build/ --write-qa
```

## Fields

| Field | Required | Meaning |
| --- | --- | --- |
| `plan_version` | yes | Const `1`. |
| `animation_id` | yes | Filesystem-safe slug. |
| `source.image` | no | Source sprite path, relative to the plan file; `--source` overrides it. The source is immutable input. |
| `canvas` | no | Output `width`/`height` and `background` (default `transparent`). Omitted canvas inherits the source dimensions; a plan with neither cannot expand (`CANVAS_UNRESOLVED`). |
| `playback` | yes | `fps` (> 0), `frame_count` (≥ 1), `loop`. |
| `anchor` | no | `bottom_center` (default), `center`, or `custom` with normalized `x`/`y`. The anchor is the stable reference point (e.g. ground contact). |
| `seed` | no | Deterministic seed reserved for stochastic stages (milestone 4). Deterministic stages never consume it. |
| `constraints` | no | `max_displacement_px` (per-axis offset budget from the base pose) and `max_frame_delta_px` (per-axis change between consecutive frames, including the loop seam). |
| `reduced_motion.mode` | no | `full` (default) or `hold_first_frame`; a directive for runtimes honoring OS reduced-motion preferences. |
| `tracks` | no | Deterministic motion tracks (below). |
| `events` | no | Discrete per-frame annotations, e.g. blink (below). |
| `metadata` | no | Free-form consumer data; the harness never interprets it. |

## Tracks

A track applies one motion to one semantic target:

```json
{
  "track_id": "breathing",
  "target": "body",
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
- `target` is an advisory semantic label (`body`, `head`, `hand_right`, …).
  The harness does not claim an arbitrary flattened sprite can be decomposed
  into these parts; renderers decide what they can honor.
- The sampled value of a track at frame `i` of `n` is
  `amplitude × curve(u)` with `u = frac((i / period) × cycles + phase)`, where
  `period = n` for loops and `n − 1` otherwise.
- Curves: `sine` and `triangle` are periodic in `[-1, 1]` and start at 0.
  `linear`, `ease_in`, `ease_out`, `ease_in_out` are mirrored (ping-pong)
  inside each cycle in `[0, 1]`, so every named curve is loop-continuous.
  `hold` is constant 0.
- All translate tracks are aggregated per frame into a whole-sprite pixel
  `offset` (x right, y down) that the validator checks against `constraints`
  and, once frames exist, against measured bounding boxes.

## Events

Events mark discrete moments (blink timing, chew beats) without pretending to
be continuous motion:

```json
{ "event_id": "blink_mid", "type": "blink", "target": "eyes", "frames": [5, 6] }
```

`type` is a free string; frame indices must be in range and event ids unique.
The expansion lists active event ids per frame.

## Determinism

Expansion is pure math: the same plan always yields a byte-identical
`plan.json`, `frame-plan.json`, and `qa/plan.qa.json` (values rounded to six
decimals, no timestamps). `frame-plan.json` embeds `plan_digest`, the SHA-256
of the canonical normalized plan, so a stale or hand-edited pairing fails
validation (`PLAN_DIGEST_MISMATCH`, `FRAME_PLAN_STALE`).

## Validation error codes

Plan-stage codes: `UNSUPPORTED_PLAN_VERSION`, `INVALID_ANIMATION_ID`,
`INVALID_FPS`, `INVALID_FRAME_COUNT`, `INVALID_CANVAS_SIZE`, `INVALID_ANCHOR`,
`INVALID_SEED`, `INVALID_CONSTRAINT`, `UNSUPPORTED_REDUCED_MOTION`,
`DUPLICATE_TRACK_ID`, `UNSUPPORTED_MOTION`, `UNIT_MISMATCH`,
`UNSUPPORTED_CURVE`, `INVALID_AMPLITUDE`, `INVALID_CYCLES`, `INVALID_PHASE`,
`DUPLICATE_EVENT_ID`, `EVENT_FRAME_OUT_OF_RANGE`, `DISPLACEMENT_EXCEEDED`,
`FRAME_DELTA_EXCEEDED`, `SOURCE_NOT_FOUND`, `SOURCE_INVALID_IMAGE`,
`SOURCE_ALPHA_REQUIRED`, `CANVAS_UNRESOLVED`. Warnings: `ZERO_MOTION`,
`CANVAS_SOURCE_MISMATCH`.

Build/frame-stage codes: `UNSUPPORTED_FRAME_PLAN_VERSION`,
`ANIMATION_ID_MISMATCH`, `PLAN_DIGEST_MISMATCH`, `MALFORMED_FRAME_PLAN`,
`FRAME_PLAN_COUNT_MISMATCH`, `FRAME_PLAN_INDEX_GAP`, `FRAME_PLAN_STALE`,
`FRAME_MISSING`, `UNEXPECTED_FRAME_FILE`, `FRAME_INVALID_IMAGE`,
`FRAME_DIMENSION_MISMATCH`, `FRAME_ALPHA_REQUIRED`, `FRAME_EMPTY`,
`BBOX_DRIFT_EXCEEDED`, `GROUND_DRIFT_EXCEEDED`, `FRAME_DELTA_EXCEEDED`.
Warning: `CONTENT_TOUCHES_EDGE` (possible cropping). Measured-pixel checks use
a fixed 2 px tolerance for subpixel rendering.

Exit codes follow the shared contract in
[`docs/animation-spec.md`](animation-spec.md#exit-code-contract).
