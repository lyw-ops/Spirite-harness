# Project handoff

Last updated: 2026-09-03 — first external consumer integration recorded;
package remains **0.7.0** (no core change).

The M4/M5 verification records below describe the pre-publication working
tree. Their "no commit/push" statements are historical; publication was
subsequently authorized after the strict review and complete offline
acceptance passed.

## First consumer integration: gensokyo-codex-pets (2026-09-03)

Sprite Harness 0.7.0 is now consumed in production by
[gensokyo-codex-pets](https://github.com/lyw-ops/gensokyo-codex-pets)
(commit `c9d921b`, `docs/sprite-harness-integration.md` there) for the Reimu
Eating Set: six real 596×596 flattened RGBA sprites, one single-image v1
Animation Plan per state, driven end to end through the public CLI only —
`plan → render → validate --write-qa → preview → contact-sheet → report`, all
in `--json` mode from subprocesses with exit-code checks. **No harness core
change was needed and none was made**; no character-specific logic entered the
harness. This section records what the integration exercised and observed so
future harness work does not re-derive it.

What the consumer run confirmed in practice:

- The identity/static path works as designed: `frame_count: 1` plans with no
  tracks validate with only the expected `ZERO_MOTION` warning, and the
  rendered frame is **byte-identical to the source** through the exact
  integer-copy path — the consumer relies on this for its baseline frames.
- Determinism held at the consumer boundary: repeated full builds (plan through
  publish) produced byte-identical artifacts, letting the consumer treat
  "rebuild is a no-op diff" as a repository check.
- The flattened-vs-layered boundary is confirmed by measurement, not just
  contract: a restrained whole-sprite `translate_y` (±2 px) experiment rendered
  and validated cleanly, and per-frame alpha bounding boxes showed the ground
  line (tatami bottom) moving by the full amplitude with the rest of the scene.
  The consumer therefore shipped an identity baseline instead of fake motion —
  exactly the outcome the `TARGET_TRACKS_SKIPPED` / no-decomposition contract
  is meant to force.
- `--json` outputs were machine-consumed throughout; stable exit codes and the
  `errors`/`warnings` shapes were sufficient to gate publication (validation
  failure or any unexpected warning blocks the consumer's publish step).

Consumer-side observations (working as specified; recorded as API-ergonomics
notes, not bugs):

- Constraint values must be strictly positive (`INVALID_CONSTRAINT` for `0`),
  so a deliberately static plan declares a minimal 1 px budget rather than 0.
- Top-level JSON success flags differ by command: `plan` reports `success`,
  `validate` reports `valid`. Consumers must read the right key per command;
  a future (non-breaking) unification could add a shared field.
- `CONTENT_TOUCHES_EDGE` fires for test fixtures whose opaque pixels reach the
  canvas edge — correct behavior, worth remembering when writing tiny
  generated test images (give them a transparent border).

Next step for this consumer (drives future harness usage, not core changes):

1. Explicit layered Reimu PNGs (body/head/eyes/mouth/hand/food/table/tatami)
   are the consumer's next art milestone; the eating states then move to
   **Animation Plan v2** inline `source.layers` with local tracks (breathing,
   head bob, eating hand, blink, chew) — the M3 contract as shipped, no new
   harness capability required. The consumer's spec/builder already pass
   per-state plan overrides through, so v2 adoption is a data change there.
2. After layered clips exist and Codex standard-row performances are designed,
   the consumer plans to use the **M5 `export`** grid atlas for the Codex v2
   sheet (its 8×11 / 192×208 target matches the generic fixed example). Food
   tiers are not Codex rows; that mapping stays consumer-side.
3. **M4 generation remains unused and unauthorized** in the consumer pipeline;
   its builds are offline and deterministic by policy.

## Current delivery and remaining live step

M1–M5 engineering is implemented. M4 adds optional, explicit source-space PNG
replacement generation through external processes; M5 adds deterministic grid
atlases and complete offline pixel round trips. The real OpenAI adapter is a
separate installable distribution (`sprite-openai-adapter` 0.1.0), with real
request construction/authentication/response handling tested through a local
HTTP service. **Live provider acceptance is NOT completed**: no usable key or
paid-call/source-upload authorization was available. No real model request was
made. The offline geometric adapter is explicitly a test substitute.

## Actual starting state and preservation

Started from `main`, HEAD `b27c6d9de84a6f3a982b9ebd76e742b43f93e68e`,
package 0.5.0, with the complete uncommitted M3 working tree. Baseline execution:
**381 passed in 2.25s**. The render rollback/retained-marker safety, all-source
identity checks, exact RGBA recomputation, strict versions and two-stage M3
geometry were present. No M3 reimplementation, reset, clean, stash, clone,
commit or push was used. Every baseline file is still present; all 12 original
test files, including untracked M3 tests, have unchanged byte hashes. See
[baseline.json](../verification/m4-m5/baseline.json) and
[preservation.json](../verification/m4-m5/strict-review/preservation.json).
The old M3 handoff is preserved below as historical context.

## Contract decisions and versions

| Artifact | Version/compatibility |
| --- | --- |
| Package | 0.5.0 → 0.7.0 directly; no intermediate release |
| Animation Plan / frame plan | v1 single-image and v2 explicit layers unchanged |
| Render | v1 deterministic unchanged; v2 strictly requires generated-input backend and request/accepted digests |
| Generation spec / request / response / accepted inputs | Each starts at strict v1, separate version keys |
| Export spec / normalized config / atlas | Each starts at strict v1 |
| QA | Existing plan/build/frame v1 retained; generation/export v2 binds subjects |
| Frame manifest | v1 unchanged; export accepts existing external frames through validated build inputs |

No mechanical migration of old builds is required. Four actual pre-existing
0.5.0 single/layered full/hold builds were validated by installed 0.7.0.
Canonical integer types are checked at runtime (including rejection of 1.0
and booleans); JSON Schema's mathematical integer convention alone cannot
express the lexical 1 versus 1.0 distinction. All new schemas ship with the
package and parity tests ensure they match schemas/.

One generation spec maps each unique request id to an existing target and an
explicit set of frames; one candidate is explicitly reused across that set.
Request/response identity, coverage, size, alpha and content hashes are checked
before copying accepted PNGs into generation/inputs. Copied source references
and the spec snapshot let adapters resolve all request paths during staging.
The accepted manifest separately binds the original spec path/hash. Request
normalization is recomputed from the original spec and verified plan. Changes
to seed, source, instruction or mapping invalidate old generated artifacts.

`render --generated-input` replaces source pixels before unchanged M2/M3
transforms; ordinary render uses originals. Unmapped frames use originals;
requested-but-missing results fail. Hold always selects actual frame 0 (with
originals for its unmapped targets), then freezes the complete composition and
pose. Offline validation never runs an adapter, but rechecks original and
frozen inputs and recomputes final RGBA/geometry, including hidden RGB.
Global constraints and final nonempty-frame requirements remain active.

The item seed derives from SHA-256 over the documented canonical tuple, never
Python hash/time/temporary paths/arrival order. OpenAI Images does not expose
the requested seed capability: the adapter requires allow_unsupported and
reports false. Frozen input replay is byte deterministic in the same runtime;
new stochastic model invocations are not promised to repeat. Hashes and bbox
checks cannot establish action semantics, aesthetic quality or provider
identity. QA explicitly marks those checks skipped. Local digests are not
cryptographic provider authentication or protection against replacing all
trusted inputs together.

M5 preserves full canvases, uses integer top-left padding and row-major cells,
and never trims/rotates/scales/extrudes/duplicates frames. It reconstructs
layout, timing and pivots from configuration and validated builds, then checks
every source crop and all unused RGBA bytes. Source-frame PNG byte hashes are
observations separate from RGBA requirements, so full-mode re-encoding remains
compatible; held frame sets still require mutual byte identity. Metadata,
input mode/identity and stale export QA are checked offline.

## Safety and failure behavior

Existing render publication remains in place. New generation/export stages
publish complete directories with exclusive markers, previous-output backups
and reversible renames. Generation also holds the existing render lock.
Publication/staging/rollback/cleanup failures, forced exits, concurrent readers
and writers, symlinks/dangling links/hard-link aliases, unknown files and input
changes were exercised. Inputs are checked again before publication; validation
also checks identity stability. These checks do not create an atomic snapshot
across directories, protect against arbitrary hostile filesystem races, provide
power-loss durability, or sandbox a trusted executable's OS permissions.
See [transactions.md](transactions.md) for recovery; never delete a marker to
silence a failed validation. Malformed/invalid/missing/processing exits remain
2/1/3/4, with strict JSON even for CLI argument errors.

Provider process/stdout/stderr, timeout, response/image limits and redacted
error mapping are in [adapters.md](adapters.md). Redirects are disabled.
The core never retries; optional provider retries are limited to one 429.
Unknown-outcome timeouts, interrupted downloads and 5xx are not retried.
No credentials, provider raw errors or credential-bearing headers are logged.

## Final executed verification

Strict review rerun: **594 passed in 14.44s**.
This comprises all 381 baseline tests plus 213 new cases. Original test files
were not edited, removed, skipped or weakened. New independent pixel oracles
check source replacement, local/global ordering, alpha-over rounding, opacity,
frame-0 freezing, full-canvas placement and hand-computed atlas pivots/rects.
The real provider adapter has both a local HTTP service test and injected
transport tests for errors, finite retries, timeouts, bad outputs and redaction.

The subsequent strict review reproduced and fixed input-snapshot gaps in
generation/export normalization and export-config validation. It also fixed
staged copy destinations that could alias and overwrite original sources,
undeclared adapter files being published, and undeclared directories being
ignored by offline bundle validation. Nine regression cases failed before
their respective fixes and now pass. See the detailed
[review report](../verification/m4-m5/strict-review/review.md).

Every final engineering gate exited 0: pytest, compileall, current package
reinstallation, separate adapter installation, pip check, git diff --check,
and installed-CLI acceptance. No dependencies were downloaded for installation.
Package metadata, runtime import and CLI all report 0.7.0. Imports resolve from
`.venv/lib/python3.14/site-packages`, not the repository source tree.

Installed CLI acceptance made **103 subprocess calls**, including **101 harness
CLI calls**, from a temporary cwd outside the repository with PYTHONPATH
removed. Expected and actual exits matched throughout, including 0/1/2/3/4.
Success/failure JSON and all JSON artifacts passed a parser rejecting duplicate
keys and nonfinite tokens. Human modes exercised plan/generate/render/validate/
preview/contact-sheet/export/validate-export/report. All original example input
hashes remained unchanged. Full and held renders and repeated atlas exports
were checked for deterministic bytes; same-bbox corruption failed, full-mode
PNG re-encoding passed, and the installed real adapter refused missing auth
without contacting a provider. Existing 0.5.0 artifacts also validated.

Final logs and artifacts:

- [gates.json](../verification/m4-m5/strict-review/gates.json): exact verification commands, exits and complete stdout/stderr.
- [pytest.log](../verification/m4-m5/strict-review/pytest.log): full-suite output.
- [cli-commands.json](../verification/m4-m5/strict-review/cli-commands.json): every installed CLI invocation and expected/actual exit.
- [cli-summary.json](../verification/m4-m5/strict-review/cli-summary.json): installation identity, pipeline outputs, source hashes and live status.
- [visual-qa.json](../verification/m4-m5/strict-review/visual-qa.json): actual atlas/contact-sheet inspection and file hashes.
- [review.json](../verification/m4-m5/strict-review/review.json): review findings, verification results and final Git state.

`build/m4-m5-strict-review/` contains the latest binary artifacts (ignored
build products, retained locally). The earlier initial/final/release runs
are retained as preceding checkpoints; strict-review/ is the latest gate record.

## Reproduction and pipeline locations

Use fresh output directories. One command performs tests, compile checks,
installation, pip/diff checks and installed outside-repository CLI acceptance:

```bash
.venv/bin/python scripts/verify_m4_m5.py \
  --output verification/m4-m5/review-rerun \
  --acceptance build/m4-m5-review-rerun
```

The fake HTTP service needs permission to bind localhost. No live provider
traffic occurs. To run just the examples after installing both local packages:

```bash
.venv/bin/python scripts/acceptance_m4_m5.py --output build/m4-m5-demo
```

Under the latest `build/m4-m5-strict-review/` directory:

| Pipeline | Outputs |
| --- | --- |
| Old M2 single-image | single/build-full, single/build-hold, single/atlas-full, single/atlas-hold |
| M3 three-layer | layered/build-full, layered/build-hold, layered/atlas-full, layered/atlas-hold |
| M4 offline test adapter | generated/build-full, generated/build-hold, generated/atlas-full, generated/atlas-hold |
| Multi-clip fixed grid | multi-atlas-full, multi-atlas-hold; configs multi-full.json and multi-hold.json |

Every build has frames, preview.gif, contact-sheet.png, render.json and frame
QA. M4 builds additionally contain the complete generation bundle and generation
QA. Every atlas directory has atlas.png, atlas.json, export-config.json,
export-spec.json and export.qa.json. The multi-clip atlas is 1536x2288: 8x11
cells, each 192x208, 8px padding. Explicit order is generated → single → layered,
36 used cells and 52 transparent empty cells. Full and hold exports are separate.
Actual final atlas and generated contact sheet were visually inspected: the
specified candidate-frame changes, clip order, grid gaps and empty rows match
the contract. This is geometric layout QA, not model-semantic acceptance.

For individual commands use the exact installed invocation list in the CLI
log or the command contracts in generation.md / atlas.md. The generic fixed
example also lives at examples/grid-atlas/export.json.

## Changed files for review

New core modules: contracts.py, generation.py, atlas.py, transactions.py and
packaged schemas under src/sprite_harness/contracts/. Integration changes:
build.py, render.py, layers.py, cli.py and qa.py. The new real provider adapter
is entirely under adapters/openai; the core's dependencies remain Pillow and
PyYAML. New tests are test_generation.py, test_atlas.py,
test_generation_export_safety.py, test_provider_adapter.py and
test_new_contracts.py. New scripts create geometric inputs, run the offline
adapter, run optional authorized live smoke, and reproduce all acceptance/gates.
HARNESS, README, roadmap, architecture, animation-plan, renderer, layered-sprites
and handoff are updated. New contract docs are generation.md, adapters.md,
atlas.md and transactions.md. New examples are generated-placeholder/ and
grid-atlas/. pyproject/runtime are 0.7.0; render/QA schemas are versioned unions.
The underlying uncommitted M3 diff remains part of the reviewable worktree.

## Known limits and next step

No known unresolved deterministic pipeline/engineering gate failures remain.
Generation/export have documented memory/file/dimension quotas. Export requires
accessible validated builds; external frames are accepted through the existing
build contract, not raw directory scans or standalone frame manifests. No
trimming, rotation packing, scaling, extrusion, runtime-specific compatibility,
automatic decomposition, interpolation, optical flow, video or GUI is included.
Exact rendering requires the same Pillow/runtime environment.

The only remaining provider acceptance step is an explicitly authorized live
call with a usable OPENAI_API_KEY. It can use the prepared original 1024x1024
geometric smoke workflow:

```bash
.venv/bin/python scripts/live_provider_smoke.py \
  --output build/live-smoke --authorize-paid-call
```

The chosen provider adapter supports only documented native output sizes and
refuses tiny source images. It does not resize, repair alpha or guarantee a
seeded model result. Live success must be recorded from that actual run; package
installation and local transport success do not count as live acceptance.

Final Git HEAD and branch remain `b27c6d9` / `main`. All work is uncommitted and
unpublished for independent review; no commit or push was performed.

---

## Historical M3 handoff (preserved from the starting worktree)

Last updated: 2026-09-03 — milestone 3, package 0.5.0.

## Status and actual baseline

M1, M2 and M3 are implemented. M3 renders explicitly supplied PNG layers;
M4 AI generation and M5 atlas/exporters remain unimplemented. No automatic
sprite decomposition, skeleton, IK, mesh, mask system, video or GUI is claimed.

Work started on `main`, commit `b27c6d9` (`Implement milestone 2 renderer with
safe publication and pixel validation`), package 0.4.0, with a clean working
tree. The existing 229 tests passed before edits. Inspection confirmed all M2
review fixes: source/output aliases, whole-generation publication and rollback,
interrupted-transaction blocking, exact decoded RGBA verification, and strict
render-version types. No M2 fixes had to be recreated from an older baseline.
No commits or pushes were made. The completed implementation remains in the
working tree for independent review; all original test files are unchanged.

## Design and contracts

- One input format: v2 Animation Plan `source.reference_canvas` plus inline
  `source.layers`. No external layer manifest or hidden metadata fields.
  `source.image` and `--source` retain v1 behavior; mixed modes are rejected.
- Every layer supplies a unique target, PNG, named/custom normalized anchor,
  and finite static position. `sprite` is reserved. Array order is the only
  back-to-front order. Unknown layered track/event targets fail; events remain
  annotations. Untracked layers remain visible at their static positions.
- The authoring plan owns relative image paths. Normalization rewrites every
  path relative to the build, pins each PNG's SHA-256/dimensions and includes
  all bindings, order, anchors, positions and canvases in the digest. The
  normalized plan becomes the runtime description; the original authoring
  file is not an additional runtime dependency. Moving a complete parent tree
  retains the same relative paths; moving only the build needs regeneration.
- Local transforms use reference-canvas axes, then clip to the reference
  canvas and alpha-over composite in order. One unchanged M2 `render_pose`
  applies global anchor alignment, transform and opacity to the composite.
  Local translation never enters global offset. Global opacity is applied
  once, after composition. A different output canvas does not imply fitting.
- Rotate sums; scale/opacity factors multiply; opacity clamps only after a
  finite product check. Nonpositive scale, negative opacity and non-finite
  effective geometry fail. Invisible local layers are valid; only the final
  frame must be nonempty. Very large finite local integer translations clip
  without passing overflowing integer coordinates to Pillow. Global budgets
  remain global; there is no independent local displacement budget.
- Both raster stages use the documented integer-copy or bilinear affine path,
  8-bit alpha-over, and `floor(alpha * opacity + 0.5)` opacity rounding. The
  intermediate clip and quantization are intentional.
- `frame-plan.json` v2 includes all layer bindings plus ordered local poses and
  a global pose for every frame. Full frame-plan consistency is recomputed
  from the plan. Failed input verification stops frame consumption. A valid
  built-in manifest requires exact decoded RGBA from **all** trusted sources.
  External frames retain composite geometry validation, which cannot establish
  hidden-layer state or exact artwork identity.
- Full is default; reduced `hold_first_frame` freezes the entire first-frame
  local composition and global pose. All held PNGs are byte-identical.
- M2 publication functions and recovery flow are reused. Source guards now
  include every layer and runtime description, manifest hard-link aliases,
  and plan/QA/preview output aliases. Unknown output files remain protected.

The normative coordinate, path, error and compatibility contract is
[layered-sprites.md](layered-sprites.md); transaction recovery remains in
[renderer.md](renderer.md#recovery-after-an-interrupted-process).

## Schema and version decisions

| Contract | Decision | Compatibility |
| --- | --- | --- |
| Package | 0.4.0 → 0.5.0 | pyproject and runtime version agree; verified installed distribution too |
| Animation Plan | v2 for layers, v1 retained | V1 normalization/source override behavior retained; v2 requires layered source |
| Frame plan | v2 for layered source and ordered local/global poses | V1 structure retained; version must match the plan's input mode and have canonical integer type |
| Render manifest | v1 unchanged | Existing digest + mode fully binds the layered plan; no additional fields needed |
| QA | v1 unchanged | Existing check/issue representation supports layer context |
| Frame manifest | v1 unchanged | Existing external-frame workflow preserved |

Schemas `animation-plan.schema.json` and `frame-plan.schema.json` describe both
versions and reject cross-mode fields. New errors include
`SOURCE_MODE_CONFLICT` (exit 2), `PLAN_SOURCE_VERSION_MISMATCH`, `EMPTY_LAYERS`,
`DUPLICATE_LAYER_TARGET`, `RESERVED_LAYER_TARGET`, `UNKNOWN_LAYER_TARGET`,
`INVALID_REFERENCE_CANVAS`, `INVALID_LAYER_ANCHOR`, `INVALID_LAYER_POSITION`,
`SOURCE_PNG_REQUIRED`, `NONFINITE_EFFECTIVE_TRANSFORM` (exit 1).
Existing source/transform/frame/pixel/transaction errors are reused.

V1 output pixels and normalization were not changed. Invalid non-finite
compositions gain explicit rejection. Historical provenance strings still
produce only `GENERATED_BY_MISMATCH`. No test assertions were migrated,
removed, skipped or weakened to obtain compatibility.

## Verification actually executed

Environment: macOS, Python 3.14.5, Pillow 12.3.0, PyYAML 6.0.3, pytest 9.1.1.

```text
Baseline: .venv/bin/pytest                         229 passed
Final: .venv/bin/pytest -o addopts='' -q            381 passed in 2.61s
.venv/bin/python -m compileall -q src/sprite_harness tests scripts    exit 0
.venv/bin/pip install --no-deps --no-build-isolation .               exit 0, 0.5.0 wheel installed
.venv/bin/pip check                                                exit 0, no broken requirements
git diff --check                                                  exit 0
Installed CLI --version                                           0.5.0
Installed importlib.metadata version                              0.5.0
Installed module location                                         .venv/lib/python3.14/site-packages/sprite_harness
```

381 = 229 unchanged original tests + 123 new layer/contract/pixel/safety tests
+ all 29 original M2 safety scenarios rerun unchanged with two-layer inputs.
Independent oracles hand-compute placement, combined local/global rotation and
translation, bilinear scale support, opacity products, alpha-over order and
post-composite global opacity. Tests cover every-source replacement and resize,
round-trip and relocation, strict shapes/versions, tampering, transparent /
occluded / clipped layers, numeric overflow/underflow, same-bbox corruption,
full/hold modes, source hashes, re-encoding compatibility and external frames.
The shared safety scenarios include every publication rename, staging failure,
rollback/cleanup failure, forced subprocess exit, concurrent readers/writers,
symlinks, hard links and rebuilding damaged outputs.

Final real installed-CLI acceptance: **54 subprocess calls, all expected exits
matched**. Every harness command ran in a temporary cwd outside the repository
with `PYTHONPATH` removed. Both module and distribution identities were checked
before running; no pytest `pythonpath=src` fallback was used. All JSON outputs
and artifacts passed a parser rejecting NaN/Infinity; success and failures
covered process exits 0/1/2/3/4. Plan/render/validate/preview/contact-sheet/report
were exercised in JSON and human modes. Each pipeline produced 12 distinct full
frames, repeated renders matched bytes, and the reduced build held frame 0
across 12 identical PNGs. Same-bbox RGB corruption failed, overwrite repaired
it, the last source layer's resize/replacement failed, and all source hashes
were restored/unchanged after the deliberate probes. The layered contact sheet
was visually inspected; it shows only the intended simple geometric shapes.

Local environment repair: the existing 0.4.0 dist-info directory contained only
orphan duplicate files and no METADATA. It made pip's first success label say
0.4.0 and metadata discovery return None despite loading 0.5.0 code. The directory
was **moved intact**, not deleted, to
`build/m3-install-recovery/sprite_animation_harness-0.4.0.dist-info`. A subsequent
regular reinstall reports 0.5.0 consistently. Pip's cache-permission warning is
benign; installation and `pip check` succeeded without cache or network use.

## Reproduction and artifacts

From the repository root:

```bash
.venv/bin/pip install --no-deps --no-build-isolation .
# Choose a fresh output directory; the acceptance script never replaces one.
.venv/bin/python scripts/acceptance_m3.py --output build/m3-review-acceptance
```

The full recorded final run is under `build/m3-acceptance-final/` (ignored build
output, retained locally):

- `summary.json`: installed identity, 54 calls, checked exits, source hashes and results.
- `commands.json`: full command arguments, outside cwd, expected/actual exits, stdout/stderr.
- `layered/build/`: full three-layer plan, frame plan, render manifest, 12 PNGs,
  `preview.gif`, `contact-sheet.png`, plan/frame QA.
- `layered/build-hold/`: corresponding reduced build and previews/QA.
- `single/build/` and `single/build-hold/`: old M2 example with generated placeholder.
- `layered/build-repeat/` and `single/build-repeat/`: deterministic comparison builds.

A minimal layered demonstration with a fresh directory:

```bash
.venv/bin/python scripts/create_layered_placeholder.py /tmp/sprite-m3-demo
.venv/bin/sprite-harness plan --spec /tmp/sprite-m3-demo/animation.json --output /tmp/sprite-m3-demo/build
.venv/bin/sprite-harness render /tmp/sprite-m3-demo/build
.venv/bin/sprite-harness validate /tmp/sprite-m3-demo/build --write-qa
.venv/bin/sprite-harness preview /tmp/sprite-m3-demo/build
.venv/bin/sprite-harness contact-sheet /tmp/sprite-m3-demo/build
.venv/bin/sprite-harness report /tmp/sprite-m3-demo/build
```

## Changed files for review

- Protocol/docs: `HARNESS.md`, `README.md`, `docs/roadmap.md`,
  `docs/architecture.md`, `docs/animation-plan.md`, `docs/renderer.md`,
  `docs/handoff.md`, new `docs/layered-sprites.md`.
- Version/contracts: `pyproject.toml`, `src/sprite_harness/__init__.py`,
  `schemas/animation-plan.schema.json`, `schemas/frame-plan.schema.json`.
- Core: `src/sprite_harness/plan.py`, `plan_validator.py`, `expand.py`,
  `geometry.py`, new `layers.py`, `build.py`, `render.py`, `processing.py`, `cli.py`.
- Tests: new `tests/test_layers.py`, `tests/test_layered_safety.py`.
- Example/tools: new `examples/layered-placeholder/animation.json`,
  `examples/layered-placeholder/README.md`, `scripts/create_layered_placeholder.py`,
  `scripts/acceptance_m3.py`.

## Limits and next work

No known unresolved M3 functional failures remain after the recorded gates.
Exact pixel validation requires the same Pillow rendering environment;
legitimate cross-version resampling changes require re-rendering. External
flattened frames cannot prove occluded layers. Transactions detect interrupted
processes and recover ordinary publication failures; they do not promise
power-loss durability or protection from hostile filesystem replacement races.
Source files should not be edited concurrently with rendering. Derived preview
and QA files remain snapshots and should be regenerated after changing mode.
There are no independent local motion budgets or resource-size quotas.

The input is explicitly authored layers, not automatically extracted body
parts. Events do not synthesize actions. M4 and M5 remain separate future work.
