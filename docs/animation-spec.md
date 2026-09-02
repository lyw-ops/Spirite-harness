# Animation specification v1

An animation is a directory containing exactly one of `animation.yaml`,
`animation.yml`, or `animation.json`. A caller may also pass the manifest path
directly. Relative frame paths are resolved from the manifest's directory and
must stay inside that directory.

```yaml
version: 1
id: reimu_eating_task_2
character:
  id: reimu
state:
  id: eating.task_2
canvas:
  width: 1024
  height: 1024
  background: transparent
anchor:
  x: 0.5
  y: 0.94
playback:
  fps: 6
  loop: true
frames:
  - file: frames/frame_000.png
    duration: 1
    action: hold_onigiri
```

The JSON Schema is at `schemas/animation.schema.json`. Runtime frame order is the
array order in `frames`; filenames are not used to infer playback order.

`duration` is measured in frame units. The display time in milliseconds is
`duration / fps * 1000` (subject to GIF's timing granularity). `action` is opaque
metadata for humans and agents and has no runtime meaning.

Canvas anchors use normalized coordinates from `(0, 0)` at the top-left through
`(1, 1)` at the bottom-right. During normalization, the same normalized point on
the source image is aligned to the declared canvas anchor. This yields position
`(anchor_x * (canvas_width - frame_width), anchor_y * (canvas_height - frame_height))`.

For a transparent canvas, each source frame must have an alpha channel.
Normalization converts inputs to RGBA, adds transparent padding, and can repair
that representation. It does not assert that any particular pixel is transparent.

## Validation error codes

The validator currently emits:

- `UNSUPPORTED_SPEC_VERSION`
- `INVALID_CANVAS_SIZE`
- `INVALID_FPS`
- `INVALID_ANCHOR`
- `ZERO_FRAMES`
- `DUPLICATE_FRAME`
- `INVALID_DURATION`
- `FRAME_OUTSIDE_ANIMATION`
- `FRAME_MISSING`
- `FRAME_INVALID_IMAGE`
- `FRAME_DIMENSION_MISMATCH`
- `FRAME_ASPECT_RATIO_MISMATCH`
- `FRAME_ALPHA_REQUIRED`

Specification loading errors use `INPUT_NOT_FOUND`, `SPEC_NOT_FOUND`,
`AMBIGUOUS_SPEC`, `SPEC_READ_ERROR`, or `MALFORMED_SPEC`.

Validation JSON carries both `errors` (fail the run) and `warnings`
(informational). Animation Plan and build-directory codes are listed in
[`animation-plan.md`](animation-plan.md#validation-error-codes).

## Exit-code contract

| Code | Meaning |
| ---: | --- |
| 0 | Success |
| 1 | Validation failure |
| 2 | Malformed or ambiguous specification |
| 3 | Missing animation input or manifest |
| 4 | Processing/internal failure |

These codes are API and must remain deterministic. New meanings require a
versioned compatibility decision.

