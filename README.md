# Sprite Harness

A model-independent pipeline for turning a **static transparent sprite** plus a
**declarative animation specification** into validated animation frame
sequences — suitable for desktop pets and sprite atlases.

```text
static sprite → Animation Plan → frame plan → frames → validation → preview → QA report
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

# Expand the example Animation Plan into a build directory
.venv/bin/sprite-harness plan \
  --spec examples/reimu-eating/eating-loop.json \
  --output /tmp/eating-build/

# Validate the build (plan + frame plan + rendered frames when present)
.venv/bin/sprite-harness validate /tmp/eating-build/ --write-qa

# Frame-manifest animations (existing frame sets) work too
.venv/bin/sprite-harness validate examples/reimu-eating-task2 --json
.venv/bin/sprite-harness preview examples/reimu-eating-task2

.venv/bin/pytest
```

Milestone 1 is **contract + validation**: `plan` normalizes an Animation Plan
and deterministically expands it into a per-frame transform table
(`frame-plan.json`) without synthesizing pixels. Renderers arrive in later
milestones — see [`docs/roadmap.md`](docs/roadmap.md).

## Commands

```text
sprite-harness plan --spec FILE [--source PNG] [--output DIR] [--json]
sprite-harness validate <animation|build-dir> [--write-qa] [--json]
sprite-harness normalize <animation> [--scale none|fit] [--output DIR] [--json]
sprite-harness preview <animation|build-dir> [--output FILE] [--json]
sprite-harness contact-sheet <animation|build-dir> [--output FILE] [--thumb-size PX] [--json]
sprite-harness report <animation|build-dir> [--json]
```

An animation argument may be a directory containing `animation.yaml`,
`animation.yml`, or `animation.json`, a direct path to one of those manifests,
or a build directory produced by `plan`.

## Two specification layers

| Layer | Schema | Purpose |
| --- | --- | --- |
| **Animation Plan** (动画计划) | [`schemas/animation-plan.schema.json`](schemas/animation-plan.schema.json) | Declarative intent: source, canvas, FPS, loop, anchor, motion tracks, easing curves, displacement budgets, blink events, reduced motion, seed. See [`docs/animation-plan.md`](docs/animation-plan.md). |
| **Frame plan** | [`schemas/frame-plan.schema.json`](schemas/frame-plan.schema.json) | Deterministic expansion: one entry per frame with sampled transform values, digest-bound to the plan. |
| **Frame manifest** | [`schemas/animation.schema.json`](schemas/animation.schema.json) | Playable frame sets that already exist on disk. See [`docs/animation-spec.md`](docs/animation-spec.md). |
| **QA report** | [`schemas/qa.schema.json`](schemas/qa.schema.json) | Deterministic validation record per stage. |

## Examples

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
- [`docs/animation-plan.md`](docs/animation-plan.md) — Animation Plan v1
- [`docs/animation-spec.md`](docs/animation-spec.md) — frame manifest v1 and
  exit codes
- [`docs/architecture.md`](docs/architecture.md) — module layout
- [`docs/roadmap.md`](docs/roadmap.md) — milestones 1–5
- [`docs/handoff.md`](docs/handoff.md) — cross-session project handoff
