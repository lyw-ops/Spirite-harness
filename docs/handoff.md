# Project handoff

Last updated: 2026-09-02

## Status

Milestone 1 (contract + validation) is implemented: the frame-manifest layer
from the first work session plus the Animation Plan layer (plan → deterministic
frame plan → build validation → QA reports). No renderer exists yet by design;
see `docs/roadmap.md`. Example art is placeholder-only or specification-only;
no finished animation artwork is claimed.

## Delivered scope

- Canonical provider-neutral protocol in `HARNESS.md`; `AGENTS.md` and
  `CLAUDE.md` are thin pointers to it
- Animation Plan IR (`docs/animation-plan.md`) with JSON Schema, typed loader
  (`plan.py`), value-level validator (`plan_validator.py`), deterministic curve
  sampling (`curves.py`), and expansion into a digest-bound frame plan
  (`expand.py`)
- `sprite-harness plan --spec … [--source …] --output build/` writing
  `plan.json`, `frame-plan.json`, and `qa/plan.qa.json`; nothing is written
  when validation fails
- Build-directory validation (`build.py`): plan/frame-plan digest binding,
  deep re-expansion staleness check, and rendered-frame checks (numbering,
  dimensions, alpha, empty frames, bounding-box and ground drift against the
  planned offsets, frame-to-frame displacement, edge-cropping warning)
- `validate`, `preview`, `contact-sheet`, and `report` accept build
  directories; `validate --write-qa` writes `qa/frames.qa.json` /
  `qa/build.qa.json`
- Deterministic QA reports (`qa.py`, `schemas/qa.schema.json`) with no
  timestamps; identical inputs yield byte-identical artifacts
- Frame-manifest layer unchanged in behavior; `ValidationResult` gained a
  `warnings` channel (additive JSON key)
- Schema-conformance tests (`tests/test_schemas.py`) keep schemas and
  implementation in lockstep; 73 tests total
- Reimu eating-loop Animation Plan example (`examples/reimu-eating/`),
  specification-only, informed by the gensokyo-codex-pets action system

## Key decisions

- Two specification layers coexist: Animation Plans (intent) and frame
  manifests (playable frame sets). `schemas/animation.schema.json` keeps its
  name for the manifest; the plan schema is
  `schemas/animation-plan.schema.json`.
- Easing curves are mirrored (ping-pong) per cycle so every named curve is
  loop-continuous; periodic curves span [-1, 1], easings [0, 1], `hold` is 0.
- `plan.json` stays round-trippable through the loader (anchor coordinates are
  written only for `custom`); resolved anchor/canvas live in the frame plan.
- `frame-plan.json` embeds `plan_digest` (SHA-256 of the canonical normalized
  plan); `validate` also deterministically re-expands and deep-compares frames
  (`FRAME_PLAN_STALE`).
- Sampled values are rounded to six decimals; measured-pixel drift checks use a
  fixed 2 px tolerance.
- `seed` is reserved for stochastic stages (milestone 4); deterministic stages
  must not consume it.
- Build dispatch: any directory containing `frame-plan.json` is treated as a
  build directory by `validate`/`preview`/`contact-sheet`/`report`.

## Verification

Verified on macOS with Python 3.14.5, Pillow 12.3.0, PyYAML 6.0.3,
jsonschema 4.x, pytest 9.1.1. The package requires Python 3.11+.

```text
$ .venv/bin/pytest
73 passed

$ sprite-harness plan --spec examples/reimu-eating/eating-loop.json --output <tmp> --json
{"success": true, "frame_count": 12, "track_count": 4, ...}   # byte-identical on re-run

$ sprite-harness validate <tmp> --write-qa --json
{"valid": true, "checks": [... "frame_files": "skipped"], ...}
```

Local quirk: Python 3.14 on macOS skips `.pth` files carrying the hidden file
flag, which a sandboxed `pip install -e` can set. If `sprite_harness` cannot be
imported after an editable install, run
`chflags nohidden .venv/lib/python3.14/site-packages/*.pth`.

## Known limitations and non-goals

- No renderer: `build/frames/` must currently be produced externally; preview
  on a build without frames fails with `FRAMES_NOT_RENDERED`.
- `rotate`/`scale`/`opacity` tracks are expanded and schema-checked but not yet
  exercised by any renderer or measured validation.
- Background values other than `transparent` are metadata only.
- GIF preview timing remains subject to GIF timer granularity.
- No provider APIs, diffusion/image-generation dependencies, ComfyUI, Live2D,
  interpolation, optical flow, video output, or ffmpeg.

## Suggested next work (milestone 2)

Deterministic whole-sprite transform renderer with Pillow: render
`build/frames/` from the frame plan (translate + anchor placement first),
golden-file tests that rendered output passes `validate`, and a
reduced-motion render mode. Any new plan fields require schema, docs, loader,
validator, JSON, and compatibility tests in the same change.
