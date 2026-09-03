# Sprite Harness protocol

This is the canonical, provider-neutral specification for Sprite Harness. Every
coding agent (Claude Code, OpenAI Codex, future agents), human maintainer, and
CI job follows this one document. Agent entry files (`AGENTS.md`, `CLAUDE.md`)
link here and must not duplicate or extend it with provider-specific behavior.

## 1. Product boundary

Sprite Harness turns a **static transparent sprite or explicit PNG layers** plus a **declarative
animation specification** into validated animation frame sequences:

```text
sprite / explicit PNG layers           Animation Plan spec (JSON/YAML)
        \                                  /
         `--> sprite-harness plan --------'
                    |
                    v
        build/  plan.json  frame-plan.json  qa/plan.qa.json
                    |
                    v
        sprite-harness render build/  [--reduced-motion]
                    |
                    v
        build/frames/frame_000.png ...   build/render.json
                    |
                    v
        sprite-harness validate build/   -->  qa/frames.qa.json
                    |
                    v
        sprite-harness preview / contact-sheet
```

Agents, humans, CI systems, and image generators are all **clients**. The
harness core is a provider-neutral Python package whose primary interfaces are
the `sprite-harness` command line and its JSON output. The core must never
require Claude Code, OpenAI Codex, or any other model provider, and
deterministic validation must never require an LLM.

Do not add provider SDKs, provider-specific prompts, hidden editor state, or
agent-only control paths to the core. Do not hard-code any character or
franchise into schemas or code; character specifics belong in example plans and
free-form `metadata`. Generation/rendering stays separate from validation, and
sprite semantics (plans, tracks, anchors) stay separate from any rendering
backend.

## 2. Canonical workflow

Every animation task follows the same steps, whichever agent executes them:

1. **Inspect input assets** — read-only: source sprite dimensions, alpha,
   provenance. Never modify, rename, resize in place, or delete source assets.
2. **Read the animation specification** — an Animation Plan
   (`schemas/animation-plan.schema.json`, see `docs/animation-plan.md`) or a
   frame manifest (`schemas/animation.schema.json`, see
   `docs/animation-spec.md`).
3. **Produce/normalize the Animation Plan** — `sprite-harness plan --spec …
   [--source …] --output build/` writes the canonical `plan.json`.
4. **Validate the plan** — `plan` refuses to write artifacts for an invalid
   plan; `sprite-harness validate build/` re-checks any existing build.
5. **Render frames** — `sprite-harness render build/ [--reduced-motion]
   [--overwrite]` applies local layer transforms/composition (v2 inputs), then
   global sprite transforms (translate, rotate, uniform scale, opacity) with Pillow and
   writes `build/frames/` plus the `render.json` manifest (see
   `docs/renderer.md`). In single-image mode, tracks targeting sprite parts are skipped with the
   stable `TARGET_TRACKS_SKIPPED` warning. Layered mode requires explicit target
   bindings; see [the layered contract](docs/layered-sprites.md).
   Externally rendered frames that follow the frame plan's file names remain
   valid input for validation.
6. **Validate generated frames** — `sprite-harness validate build/` checks
   dimensions, alpha, numbering, drift, and displacement against the frame plan.
7. **Generate a preview** — `sprite-harness preview build/` and
   `sprite-harness contact-sheet build/`.
8. **Write the QA report** — `plan` writes `qa/plan.qa.json`; `validate
   --write-qa` writes `qa/frames.qa.json` (`qa/build.qa.json` before frames
   exist). Reports conform to `schemas/qa.schema.json`.
9. **Never silently modify source assets** — all products are written under the
   build directory (or `generated/` for frame-manifest animations); scaling is
   explicit and uniform, never per-axis.

Optional M4 runs after plan validation: explicitly `generate`, then
`render --generated-input`. Optional M5 runs after frame validation:
`export --spec FILE --output DIR`, then `validate-export DIR`. These stages
never run implicitly. Their contracts and transactions are specified below.

## 3. Artifact conventions

A build directory produced by `plan` is laid out as:

```text
build/
  plan.json          # normalized Animation Plan (round-trips through the loader)
  frame-plan.json    # deterministic per-frame transform table, digest-bound to plan.json
  qa/
    plan.qa.json     # QA report for the plan stage
    frames.qa.json   # QA report from `validate --write-qa` once frames exist
  frames/            # renderer output: frame_000.png, frame_001.png, ...
  render.json        # render manifest: plan digest + motion mode of the frame set
  preview.gif        # optional preview artifacts
  contact-sheet.png
```

- Frame files are zero-padded, contiguous from `frame_000.png`, and exactly
  match the `file` entries in `frame-plan.json`.
- `frame-plan.json` carries a `plan_digest` (SHA-256 of the canonical
  normalized plan) and every authoritative field of the document — playback,
  canvas, anchor, reduced motion, source binding, and frames — is verified
  against a deterministic recomputation from `plan.json`. Editing `plan.json`
  or hand-editing any part of `frame-plan.json` (values, types, or added
  fields) fails validation. Only `generated_by` is informational provenance,
  validated for shape so builds stay checkable across harness releases.
- In layered mode every layer has a build-relative path, SHA-256, dimensions,
  anchor and static position; layer order and explicit reference canvas are
  digest-bound. Validation re-inspects all layers and recomputes the complete
  frame-plan and final RGBA from the trusted plan. No runtime data is hidden
  in metadata and no original authoring file is needed after normalization.
- When a build has a source image, the generated `plan.json` records it with a
  path that resolves from inside the build directory plus its SHA-256 and
  dimensions; `validate` re-inspects the source file and fails on missing,
  replaced, resized, unreadable, or newly opaque sources.
- A successful render writes `render.json`
  (`schemas/render.schema.json`) **after** all frame files, binding the frame
  set to its plan revision (`plan_digest`) and recording the effective motion
  mode (`full` or `hold_first_frame`); validation judges the frames by that
  mode and recomputes their decoded RGBA pixels from the bound source. An
  absent manifest means an externally rendered frame set, judged geometrically
  as full motion, **only when no `.render-transaction/` marker exists**.
- Rendering stages complete frame directories and uses reversible renames.
  Publication failures roll back the previous output; an interrupted process
  or failed recovery retains `.render-transaction/` and blocks validation and
  further rendering until recovery. Source/output aliases and symlink output
  paths are rejected before writing. See `docs/renderer.md` for recovery.
- Generated artifacts are deterministic: same inputs, same mode, and the same
  runtime environment yield byte-identical outputs (no timestamps, no random
  metadata, no absolute temporary paths) — for rendered PNGs as well as JSON.
- Frame-manifest animations (the pre-plan format) keep their existing layout:
  the manifest plus source frames, with derived products under `generated/`.

## 4. Stable contracts

- Keep specifications versioned (`plan_version`, `version`,
  `frame_plan_version`, `render_version`, `qa_version`) and validate versions
  explicitly.
- Keep `--json` output strictly standards-compliant JSON with stable error
  codes: serialize with `allow_nan=False`, map non-finite numbers in
  diagnostics to the strings `"NaN"`/`"Infinity"`/`"-Infinity"`, and reject
  non-JSON-compatible specification values (YAML dates, sets, non-finite
  metadata numbers). Do not mix progress text into standard output in JSON
  mode.
- Preserve the documented process exit codes (0 success, 1 validation failure,
  2 malformed specification, 3 missing input, 4 processing failure).
- Treat frame order in manifests and frame plans as authoritative; natural
  sorting is discovery tooling only.
- Treat `action` (manifests), single-image non-`sprite` target labels, and
  `metadata` as human/agent-facing labels. Playback uses only file order,
  durations, FPS, and loop settings, and the harness never claims a flattened
  sprite can be perfectly decomposed into named body parts.
- The track target `sprite` is reserved for whole-sprite transforms: only
  translate tracks targeting `sprite` contribute to the aggregate per-frame
  `offset` that displacement constraints and rendered-frame bbox/ground checks
  verify. In layered mode local translation never contributes to this offset.
  Both modes use the same global transform rules (rotate values add; scale/opacity factors `1 + value` multiply,
  opacity clamped into `[0, 1]`; semantics fixed in `docs/renderer.md`).
  Single-image local tracks remain skipped with a stable warning. Layered
  v2 plans bind every target to an explicit PNG and render local transforms
  on a fixed reference canvas, alpha-over in array order, followed by one
  global transform. Invisible local layers are legal; final empty frames fail.
  Input modes are exclusive; `--source` with layers is rejected. Plan/frame-plan
  v1 remain supported; v2 is required for layers. Render/QA/frame-manifest v1
  stay unchanged. No automatic decomposition is claimed.
- Looping playback (`playback.loop: true`) requires every track to declare a
  positive integer `cycles` so all curves are continuous across the loop seam;
  non-looping playback may use positive fractional cycles.
- Resolve frame paths inside their animation/build directory; reject traversal
  outside it.
- The explicit `seed` is used only by generation request derivation (milestone 4);
  deterministic stages must not consume it.

## 5. Artwork safety

Source artwork is immutable input. Never overwrite, rename, resize in place,
or delete source sprites or frames. Write all products into the build
directory or `generated/`. Runtime consumers use an explicitly chosen manifest
or frame plan; they must not guess which files are current.

Scaling must be explicit and uniform. Transparent padding and anchor-based
placement are allowed. Never stretch one axis independently. Do not commit
third-party or copyrighted artwork; examples use programmatically drawn
placeholders or ship as specification-only.

## 6. Change workflow

1. Inspect the repository and working tree before editing.
2. When a data or CLI contract changes, update the JSON Schema, the docs, the
   parser, the validator, and the tests in the same change.
3. Add tests using tiny images generated at test time; avoid binary fixtures.
4. Run the full test suite and exercise affected CLI commands in both human
   and JSON modes.
5. Regenerate example artifacts when rendering behavior changes.
6. Record important decisions, verification, limitations, and next work in
   `docs/handoff.md`.

Keep dependencies small: Python 3.11+, Pillow, PyYAML for the core; pytest and
jsonschema for development. No ffmpeg, no GUI frameworks.

## 7. Optional generation and atlas export

Package 0.7.0 implements M4's explicit external generation and M5's grid
export. Read [generation.md](docs/generation.md), [adapters.md](docs/adapters.md),
[atlas.md](docs/atlas.md), and [transactions.md](docs/transactions.md).

`generate BUILD --spec FILE --adapter-argv JSON` checks and freezes source-space
PNG replacements in `BUILD/generation/`. `render --generated-input` explicitly
uses them before the unchanged M2/M3 transformations. Default render remains
deterministic and offline. No event or target name triggers generation.
Offline validate rechecks original and accepted inputs and final decoded RGBA.
Render v1 remains deterministic; render v2 binds backend/request/accepted input
digests. Hold freezes the complete frame-0 selection, local composition and
whole-sprite transform. Generation success alone says nothing about final QA.

`export --spec FILE --output DIR` validates explicit ordered input builds and
publishes one grid atlas; `validate-export DIR` recomputes metadata/layout and
compares every source-frame crop and every unused pixel. Single-clip sheets use
the same path. Report validates current inputs; saved QA remains a snapshot.
Generation/export QA v2 binds its subjects; plan/frame/frame-manifest versions
remain compatible. Generation and export have fail-closed directory transactions.
Sources, generation requests, frozen inputs and export inputs remain read-only
through all consuming operations. No automatic commit, publishing or deployment.

## 8. Milestone boundaries

The roadmap lives in `docs/roadmap.md`. Milestone 1 (contract + validation)
milestone 2 (whole-sprite transforms), and milestone 3 (explicit layered PNG
rendering, `docs/layered-sprites.md`) are implemented. Milestones 4 and 5
are implemented as the explicit optional
generation and deterministic grid export contracts above. The optional real
provider adapter is implemented and tested locally; live provider acceptance
requires separately authorized credentials/calls. Layered parts must be
provided explicitly and are never approximated from flattened sprites.
Keep all model APIs and provider integrations outside the core. Do not add
diffusion/image-generation dependencies to the core, ComfyUI,
Live2D, interpolation, optical flow, or video generation ahead of their
milestone, and do not generate new copyrighted character artwork at any
milestone.
