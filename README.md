# Sprite Harness

A model-independent pipeline for turning a **static transparent sprite or explicit PNG layers** plus a
**declarative animation specification** into validated animation frame
sequences — suitable for desktop pets and sprite atlases.

```text
sprite / PNG layers → Animation Plan → frame plan → frames → validation → preview → QA report
```

Claude Code, OpenAI Codex, future coding agents, humans, and CI are all clients
of the same shell/JSON API. The canonical workflow lives in
[`HARNESS.md`](HARNESS.md); `AGENTS.md` and `CLAUDE.md` are thin pointers to
it, so every agent executes the same steps and produces the same artifacts.

> **Naming** — the GitHub repository is `Spirite-harness` for historical
> reasons; the project itself is **Sprite Harness**.

## Quick start

```bash
python3 -m venv .venv
.venv/bin/pip install '.[dev]'

# A clearly labeled programmatic placeholder sprite for the demo
.venv/bin/python scripts/create_placeholder_sprite.py /tmp/demo/sprite.png

# Expand the example Animation Plan into a build directory
.venv/bin/sprite-harness plan \
  --spec examples/reimu-eating/eating-loop.json \
  --source /tmp/demo/sprite.png \
  --output /tmp/demo/build/

# Render the frame set deterministically from the frame plan
.venv/bin/sprite-harness render /tmp/demo/build/

# Validate the build (plan + frame plan + rendered frames)
.venv/bin/sprite-harness validate /tmp/demo/build/ --write-qa

# Preview artifacts
.venv/bin/sprite-harness preview /tmp/demo/build/
.venv/bin/sprite-harness contact-sheet /tmp/demo/build/

# Frame-manifest animations (existing frame sets) work too
.venv/bin/sprite-harness validate examples/reimu-eating-task2 --json
.venv/bin/sprite-harness preview examples/reimu-eating-task2

.venv/bin/pytest
```

Milestone 1 is **contract + validation**: `plan` normalizes an Animation Plan
and deterministically expands it into a per-frame transform table
(`frame-plan.json`). Milestone 2 is the **deterministic transform renderer**:
`render` applies the frame plan's whole-sprite transforms (translate, rotate,
uniform scale, opacity) to the bound source sprite — semantics in
[`docs/renderer.md`](docs/renderer.md). Milestone 3 adds explicit PNG layers, local transforms,
ordered composition and exact composite pixel validation. Package **0.7.0**.
See [the layered contract](docs/layered-sprites.md). M4 adds optional explicit source-space generation; M5 adds deterministic grid
atlases with offline pixel round-trip validation. See
[`docs/roadmap.md`](docs/roadmap.md).

## Layered demo

```bash
.venv/bin/python scripts/create_layered_placeholder.py /tmp/sprite-m3-demo
.venv/bin/sprite-harness plan --spec /tmp/sprite-m3-demo/animation.json --output /tmp/sprite-m3-demo/build
.venv/bin/sprite-harness render /tmp/sprite-m3-demo/build
.venv/bin/sprite-harness validate /tmp/sprite-m3-demo/build --write-qa
.venv/bin/sprite-harness preview /tmp/sprite-m3-demo/build
.venv/bin/sprite-harness contact-sheet /tmp/sprite-m3-demo/build
.venv/bin/sprite-harness report /tmp/sprite-m3-demo/build
```

V2 plans declare `source.reference_canvas` and ordered `source.layers` inline.
Every layer supplies `target`, PNG `image`, `anchor` and `position`. Use a fresh
demo directory; the generator refuses to overwrite existing artwork. V1
`source.image` / `--source` remain supported; combining `--source` with layers
is an error. See [the example](examples/layered-placeholder/README.md).

## Commands

```text
sprite-harness plan --spec FILE [--source PNG] [--output DIR] [--json]
sprite-harness generate <build-dir> --spec FILE --adapter-argv JSON [--timeout SECONDS] [--overwrite] [--json]
sprite-harness render <build-dir> [--generated-input] [--reduced-motion] [--overwrite] [--json]
sprite-harness validate <animation|build-dir> [--write-qa] [--json]
sprite-harness normalize <animation> [--scale none|fit] [--output DIR] [--json]
sprite-harness preview <animation|build-dir> [--output FILE] [--json]
sprite-harness contact-sheet <animation|build-dir> [--output FILE] [--thumb-size PX] [--json]
sprite-harness export --spec FILE --output DIR [--overwrite] [--json]
sprite-harness validate-export <export-dir> [--json]
sprite-harness report <animation|build-dir|export-dir> [--json]
```

An animation argument may be a directory containing `animation.yaml`,
`animation.yml`, or `animation.json`, a direct path to one of those manifests,
or a build directory produced by `plan`.

## Two specification layers

| Layer | Schema | Purpose |
| --- | --- | --- |
| **Animation Plan** (动画计划) | [`schemas/animation-plan.schema.json`](schemas/animation-plan.schema.json) | Declarative intent: source, canvas, FPS, loop, anchor, motion tracks, easing curves, displacement budgets, blink events, reduced motion, seed. See [`docs/animation-plan.md`](docs/animation-plan.md). |
| **Frame plan** | [`schemas/frame-plan.schema.json`](schemas/frame-plan.schema.json) | Deterministic expansion: one entry per frame with sampled transform values, digest-bound to the plan. |
| **Render manifest** | [`schemas/render.schema.json`](schemas/render.schema.json) | Record of a completed render: plan digest + motion mode of `build/frames/`. See [`docs/renderer.md`](docs/renderer.md). |
| **Generation** | [`generation-spec`](schemas/generation-spec.schema.json), [`request`](schemas/generation-request.schema.json), [`response`](schemas/generation-response.schema.json), [`accepted inputs`](schemas/generated-inputs.schema.json) | Optional explicit source-space replacements and frozen identities. |
| **Atlas** | [`export-spec`](schemas/export-spec.schema.json), [`export-config`](schemas/export-config.schema.json), [`atlas`](schemas/atlas.schema.json) | Explicit grid export, playback/pivot metadata and pixel round trip. |
| **Frame manifest** | [`schemas/animation.schema.json`](schemas/animation.schema.json) | Playable frame sets that already exist on disk. See [`docs/animation-spec.md`](docs/animation-spec.md). |
| **QA report** | [`schemas/qa.schema.json`](schemas/qa.schema.json) | Deterministic validation record per stage. |

## Examples

- [`examples/layered-placeholder/`](examples/layered-placeholder/) — three explicit
  geometric PNG layers with local motion and global sprite sway.

- [`examples/reimu-eating/`](examples/reimu-eating/) — an Animation Plan for a
  Reimu eating loop (breathing, head motion, eating hand, blink), written for
  the [gensokyo-codex-pets](https://github.com/lyw-ops/gensokyo-codex-pets)
  consumer. Specification-only: no artwork is included, and nothing
  Reimu-specific exists in the harness itself.
- [`examples/reimu-eating-task2/`](examples/reimu-eating-task2/) — a
  frame-manifest example with clearly marked programmatic placeholder frames.

## Documentation

- [`HARNESS.md`](HARNESS.md) — canonical protocol: workflow, artifact
  conventions, stable contracts, artwork safety
- [`docs/animation-plan.md`](docs/animation-plan.md) — Animation Plans v1/v2
- [`docs/renderer.md`](docs/renderer.md) — deterministic renderer: transform
  semantics, anchors, reduced motion, overwrite policy, error codes
- [`docs/layered-sprites.md`](docs/layered-sprites.md) — layered input, coordinates,
  composition, identity, validation boundaries and compatibility
- [`docs/animation-spec.md`](docs/animation-spec.md) — frame manifest v1 and
  exit codes
- [`docs/architecture.md`](docs/architecture.md) — module layout
- [`docs/roadmap.md`](docs/roadmap.md) — milestones 1–5
- [`docs/handoff.md`](docs/handoff.md) — cross-session project handoff

## M4/M5 demonstration and acceptance

```bash
.venv/bin/pip install --no-deps --no-build-isolation .
.venv/bin/pip install --no-deps --no-build-isolation ./adapters/openai
.venv/bin/python scripts/acceptance_m4_m5.py --output build/m4-m5-demo
```

The script uses only original geometric assets and an explicitly labeled
**offline test adapter**. It runs installed CLI commands outside the repository,
records every exit/stdout/stderr, exercises old single/layered paths, generated
inputs, full/hold, and a multi-clip fixed grid. Real provider transport tests
exercise the separate adapter. **Live provider acceptance is not completed**
without separately authorized credentials and paid calls.

Contracts: [generation](docs/generation.md), [adapters](docs/adapters.md),
[atlas](docs/atlas.md), [transactions/recovery](docs/transactions.md).
No implicit network calls, automatic decomposition, scaling, trimming or runtime
compatibility claims. The fixed 8x11 / 192x208 grid is a generic example.
