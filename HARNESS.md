# Sprite Harness protocol

This is the canonical, provider-neutral specification for Sprite Harness. Every
coding agent (Claude Code, OpenAI Codex, future agents), human maintainer, and
CI job follows this one document. Agent entry files (`AGENTS.md`, `CLAUDE.md`)
link here and must not duplicate or extend it with provider-specific behavior.

## 1. Product boundary

Sprite Harness turns a **static transparent sprite** plus a **declarative
animation specification** into validated animation frame sequences:

```text
static sprite (PNG)                     Animation Plan spec (JSON/YAML)
        \                                  /
         `--> sprite-harness plan --------'
                    |
                    v
        build/  plan.json  frame-plan.json  qa/plan.qa.json
                    |
                    v  (renderer, milestone 2+)
        build/frames/frame_000.png ...
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
5. **Produce frames if a renderer is available** — into `build/frames/`,
   following the frame plan's file names. Milestone 1 ships no renderer; that
   is expected.
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
- When a build has a source image, the generated `plan.json` records it with a
  path that resolves from inside the build directory plus its SHA-256 and
  dimensions; `validate` re-inspects the source file and fails on missing,
  replaced, resized, unreadable, or newly opaque sources.
- Generated JSON artifacts are deterministic: same inputs, byte-identical
  outputs (no timestamps).
- Frame-manifest animations (the pre-plan format) keep their existing layout:
  the manifest plus source frames, with derived products under `generated/`.

## 4. Stable contracts

- Keep specifications versioned (`plan_version`, `version`,
  `frame_plan_version`, `qa_version`) and validate versions explicitly.
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
- Treat `action` (manifests), non-`sprite` `target` labels (tracks), and
  `metadata` as human/agent-facing labels. Playback uses only file order,
  durations, FPS, and loop settings, and the harness never claims a flattened
  sprite can be perfectly decomposed into named body parts.
- The track target `sprite` is reserved for whole-sprite transforms: only
  translate tracks targeting `sprite` contribute to the aggregate per-frame
  `offset` that displacement constraints and rendered-frame bbox/ground checks
  verify. Target-local tracks (`head`, `hand_right`, …) are expanded per frame
  but cannot be pixel-verified until a renderer/layer contract exists.
- Looping playback (`playback.loop: true`) requires every track to declare a
  positive integer `cycles` so all curves are continuous across the loop seam;
  non-looping playback may use positive fractional cycles.
- Resolve frame paths inside their animation/build directory; reject traversal
  outside it.
- The deterministic `seed` is reserved for stochastic stages (milestone 4);
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

## 7. Milestone boundaries

The roadmap lives in `docs/roadmap.md`. Milestone 1 (current) is contract +
validation: `plan` normalizes and expands specifications deterministically but
synthesizes no pixels. Do not implement model APIs, provider integrations,
diffusion/image-generation dependencies, ComfyUI, Live2D, interpolation,
optical flow, or video generation ahead of their milestone, and do not
generate new copyrighted character artwork at any milestone.
