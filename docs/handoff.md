# Project handoff

Last updated: 2026-09-03 (milestone 2 + independent-review fixes)

## Status

Milestone 1 (contract + validation, hardened) and milestone 2 (deterministic
whole-sprite transform renderer) are implemented. `sprite-harness render`
turns a validated build (source sprite + `plan.json` + `frame-plan.json`) into
`build/frames/` plus a `render.json` manifest; rendered output passes the
milestone-1 validation pipeline end to end (validate → preview →
contact-sheet → QA). Package version 0.4.0. Example art remains
placeholder-only or specification-only; no finished animation artwork is
claimed, and the harness still claims no per-part, layered, or AI-assisted
rendering.

## Delivered scope (milestone 2, 2026-09-03)

- `sprite-harness render <build> [--reduced-motion] [--overwrite] [--json]`
- `geometry.py`: per-frame whole-sprite pose sampling and the documented
  anchor-affine transform, shared by renderer and validator
- `render.py`: pre-render input validation, transactional staged writes,
  render manifest written last
- Render manifest contract: `render.json` + `schemas/render.schema.json` +
  loader/validator in `build.py` + docs + tests (the one new artifact)
- Mode-aware, model-based rendered-frame validation in `build.py`
- Effective scale/opacity validation at plan stage (`plan_validator.py` via
  `geometry.effective_value_issues`)
- Renderer semantics fixed in `docs/renderer.md` before implementation;
  README/HARNESS/roadmap/architecture/animation-plan updated
- `scripts/create_placeholder_sprite.py` for a labeled programmatic demo
  sprite
- 78 milestone-2 tests (229 total; all 151 milestone-1 tests unchanged and passing)

## Independent-review fixes

The initial 200-test implementation passed its suite but failed five independent
probes. This revision closes four findings and adds 29 regression cases:

1. Symbolic-link output directories could overwrite source artwork outside the
   build. Render now rejects output symlinks (including dangling links), source
   paths inside the output slot, and source hard-link aliases. Validation also
   rejects linked/out-of-build frame paths.
2. Per-file publication could leave a mixed generation after an OS error, which
   an absent manifest incorrectly let validation treat as external full motion.
   Publication now uses reversible directory/manifest renames under an exclusive
   `.render-transaction/` guard; interrupted processes and failed rollbacks stay
   fail-closed and preserve recovery material.
3. Bounding-box checks missed different RGB, opacity, or interior shape with the
   same silhouette. Built-in manifests now require exact decoded RGBA comparison
   against trusted source/pose recomputation. External frames remain geometric
   inputs, not necessarily pixel copies of the built-in renderer.
4. Python's `True == 1` accepted boolean render versions. The runtime now checks
   canonical integer type; the schema explicitly declares an integer.

Regression coverage includes every publication rename, initial publication,
failed rollback/cleanup, staging-manifest failure, concurrent operations,
abrupt subprocess exit, source collisions, same-bbox corruption, PNG re-encoding,
external-frame compatibility, and malformed version types.

## Key design decisions

### Semantics fixed in docs/renderer.md (the contract)

Pixel centers at `(i + 0.5, j + 0.5)`, x right, y down, positive rotation
clockwise. Forward map `P = A_dst + offset + R(θ)·s·(p − A_src)` where the
anchor resolves to a source point and a canvas point; rotation and scale pivot
on that same anchor, translation comes from the frame's aggregate `offset`
exactly once (translate transforms are never applied a second time).
Composition across tracks: rotate sums; scale and opacity multiply as factors
`1 + value`; opacity clamps into `[0, 1]` silently (documented transfer
function, like CSS). Uniform scale only. Interpolation is explicit bilinear
(`Image.transform` with `Resampling.BILINEAR`, transparent fill); a pure
integral translation takes an exact pixel-copy path (`paste`), so static and
integer-translate frames are byte-exact copies. Opacity applies after geometry
via the LUT `floor(alpha × o + 0.5)`. The canvas is fixed; transforms clip.

### Invalid effective values fail at plan time

A sprite scale factor `1 + value ≤ 0` (`INVALID_EFFECTIVE_SCALE`), a negative
opacity factor (`INVALID_EFFECTIVE_OPACITY`), or a frame with effective
opacity exactly 0 (`FULLY_TRANSPARENT_FRAME`) is rejected by `validate_plan`,
so `plan` refuses to write the build and `render` (which re-runs plan
semantics) refuses too. Compatibility note: plans that previously validated
with such values (they were never renderable) now fail at exit 1.

### Input validation is separate from old-output validation

`validate_build_inputs` (plan semantics + source identity + full frame-plan
recomputation) is what `render` requires to pass with zero errors; broken or
stale files under `frames/` never block a re-render and never bypass input
integrity. `validate_build` = inputs + render-manifest + frame checks.

### Render manifest (`render.json`) — the minimal contract extension

`{render_version, animation_id, generated_by, plan_digest, mode}`. Written
**after** all frames are published, with `.render-transaction/` removed only
after commit succeeds. Its presence is meaningful only without a transaction
marker. Validation: interrupted transaction → error; otherwise
absent → judged as `full` (backward compatible with externally rendered
milestone-1 builds); `MALFORMED_RENDER_MANIFEST`,
`UNSUPPORTED_RENDER_MANIFEST_VERSION`, `RENDER_MANIFEST_STALE` (digest),
`ANIMATION_ID_MISMATCH`, `RENDER_MODE_MISMATCH` (claiming `hold_first_frame`
on a plan declaring `full`); `generated_by` stays provenance-only
(`GENERATED_BY_MISMATCH` warning).

### Reduced motion

`render` renders full motion by default; `--reduced-motion` renders the
variant the plan declares (`full` → identical to full; `hold_first_frame` →
the frame-0 pose written to every declared file, byte-identical, count and
naming preserved). Validation judges a hold set against the frame-0 pose and
enforces byte identity (`HOLD_FRAME_MISMATCH`) — it never judges hold output
against full-motion offsets, and full/reduced outputs occupy the same
`frames/` slot so they cannot mix.

### Model-based frame verification (no self-certification)

With a bound source, expected per-frame geometry is the trusted source's alpha
channel transformed through the verified pose (shared `geometry` module),
clipped to the canvas; measured bbox center/bottom must match within the
existing 2 px tolerance. Built-in renders additionally compare decoded RGBA
exactly, detecting wrong RGB/opacity/shape even with an unchanged bbox. External
frame sets retain geometry-only validation and do not claim content identity.
Expectations never come from the frames under test. Without a bound
source: pure-translation builds keep the milestone-1 relative-offset check
(and the measured `FRAME_DELTA_EXCEEDED` check, which now applies only on
that path); rotate/scale/opacity builds get the stable `GEOMETRY_UNVERIFIED`
warning instead of a fake pass. Renderer and validator share the geometry
module deliberately; independent hand-computed reference tests (single pixel
rotated 90° about a known anchor, 2× scale bbox, exact opacity LUT values,
anchor placement tables) exist so a shared bug still fails the suite.

### Output safety

Source images are read-only (tests assert the source hash is unchanged).
Frames and the manifest are staged under the exclusive `.render-transaction/`
guard. Whole-directory and manifest publication uses reversible renames and
backup paths; staging/publication failures preserve the old generation when
rollback succeeds. Failed rollback, cleanup, or abrupt process termination
retains the guard and remaining recovery material, blocking validation and
further writes. Recovery instructions are in `docs/renderer.md`; never remove
the guard merely to bypass validation. Overwrite scope is the declared products
(frame-plan file names + `render.json`); unknown files in `frames/` abort with
`FRAMES_DIR_CONFLICT` and are never deleted. Without `--overwrite`, existing
declared output is refused (`FRAMES_ALREADY_RENDERED`). Renders are
deterministic (no timestamps/random metadata/absolute paths in artifacts) and
never consume `plan.seed`.

## Error-code changes (all documented in docs/renderer.md and animation-plan.md)

New plan-stage (exit 1): `INVALID_EFFECTIVE_SCALE`,
`INVALID_EFFECTIVE_OPACITY`, `FULLY_TRANSPARENT_FRAME`.
New validate-stage (exit 1): `MALFORMED_RENDER_MANIFEST`,
`UNSUPPORTED_RENDER_MANIFEST_VERSION`, `RENDER_MANIFEST_STALE`,
`RENDER_MODE_MISMATCH`, `HOLD_FRAME_MISMATCH`.
New render-stage (exit 4): `RENDER_SOURCE_REQUIRED`, `UNSUPPORTED_BACKGROUND`,
`FRAMES_ALREADY_RENDERED`, `FRAMES_DIR_CONFLICT`, `RENDERED_FRAME_EMPTY`,
`RENDER_SOURCE_UNREADABLE` (defensive), `RENDER_RECOVERY_REQUIRED`.
New review gates: `RENDER_TRANSACTION_INCOMPLETE` (exit 1 validate / 4 render),
`FRAME_PATH_OUTSIDE_BUILD`, `FRAME_CONTENT_MISMATCH`,
`FRAME_CONTENT_UNVERIFIED` (exit 1).
New warnings: `TARGET_TRACKS_SKIPPED` (render), `GEOMETRY_UNVERIFIED`
(validate). Process exit codes 0–4 unchanged.

## Schema changes

- New `schemas/render.schema.json` (render manifest v1, explicit integer version).
- `animation-plan.schema.json`, `frame-plan.schema.json`, `qa.schema.json`
  unchanged; existing artifacts still conform.

## Compatibility notes

- Builds rendered externally (no `render.json`) validate as before (full
  motion, relative check when no source is bound).
- Builds **with a bound source and frames** are verified model-based against
  source geometry. Built-in renders with a manifest additionally require exact
  RGBA agreement; external frames remain geometry-only. Legal clipped
  translation passes (previously the relative check could flag it).
- Plans with sprite scale/opacity tracks whose effective values are
  unrenderable (factor ≤ 0 / < 0 / opacity 0) now fail plan validation.
- The measured `FRAME_DELTA_EXCEEDED` frame check applies only on the
  no-source relative path; the plan-stage offset-delta constraint is
  unchanged.
- `report` gained a `render_manifest` artifact row; `validate` gained the
  `render_manifest` check id.

## Verification (macOS, Python 3.14.5, Pillow 12.3.0, PyYAML 6.0.3, pytest 9.1.1)

```text
$ .venv/bin/pytest                                   # 229 passed (was 151; +78)
$ .venv/bin/python -m compileall src/sprite_harness tests scripts   # clean
$ .venv/bin/pip install --no-deps --no-build-isolation .            # installed 0.4.0 wheel
$ .venv/bin/pip check                                             # no broken requirements
$ git diff --check                                                   # clean
$ .venv/bin/sprite-harness --version                                 # 0.4.0 (installed CLI, matches pyproject/__init__)

# Installed-CLI end-to-end (placeholder sprite + examples/reimu-eating):
$ python scripts/create_placeholder_sprite.py <demo>/sprite.png
$ sprite-harness plan --spec examples/reimu-eating/eating-loop.json \
    --source <demo>/sprite.png --output <demo>/build                 # exit 0
$ sprite-harness render <demo>/build                                 # exit 0, 12 frames,
                                                                     # TARGET_TRACKS_SKIPPED: head_bob, eating_hand
$ sprite-harness validate <demo>/build --write-qa                    # exit 0
$ sprite-harness preview <demo>/build; sprite-harness contact-sheet <demo>/build  # exit 0
$ sprite-harness render <demo>/build --reduced-motion --overwrite    # exit 0, mode hold_first_frame
$ sprite-harness validate <demo>/build --json                        # valid: true (hold mode)
$ shasum -c source.sha                                               # source unchanged by rendering

# Two independent plan+render runs: frames/*.png, render.json, plan.json,
# frame-plan.json byte-identical across builds.
# Failure paths: tampered frame-plan -> render exit 1 (FRAME_PLAN_STALE);
# existing output w/o --overwrite -> exit 4 (FRAMES_ALREADY_RENDERED);
# missing build -> exit 3; malformed frame-plan JSON -> exit 2.
```

All `--json` outputs and artifacts parse under a strict JSON parser (tests use
`parse_constant` rejection). Post-review installed-CLI acceptance ran 22 checks
outside the repository with `PYTHONPATH` removed and imports confirmed from
site-packages: two independent full renders were byte-identical, full motion
produced 12 distinct frames, reduced motion produced one distinct frame across
12 files, source bytes were unchanged, and same-bbox RGB corruption failed
validation and was repaired by overwrite. All five original independent
failure probes also passed against the installed package.

Local quirk (unchanged): Python 3.14 on macOS can
skip `.pth` files carrying the hidden flag after a sandboxed editable install;
use a regular `pip install '.[dev]'` (pytest uses `pythonpath=src` regardless).

## Known limitations and non-goals

- Whole-sprite transforms only: target-local tracks are expanded and
  digest-bound but skipped at render time (`TARGET_TRACKS_SKIPPED`); no
  automatic decomposition of flattened sprites is claimed. Layered rendering
  is milestone 3.
- Only `canvas.background: transparent` renders (`UNSUPPORTED_BACKGROUND`
  otherwise); other backgrounds remain metadata.
- Pixel-exact output is guaranteed per environment (Python/Pillow versions);
  Pillow's resampling may differ across releases. Built-in RGBA verification
  is exact; re-render under the current environment if resampling differs.
  The 2 px tolerance applies to geometry, not pixel identity.
- Transaction recovery handles exceptions and detects interrupted processes;
  it does not guarantee power-loss durability or defend against a hostile
  process replacing filesystem paths between system calls.
- Re-render replaces frames and the manifest; regenerate existing preview,
  contact-sheet and QA snapshots before distributing that generation.
- Builds with rotate/scale/opacity but no bound source cannot be
  geometry-verified (`GEOMETRY_UNVERIFIED` warning, honest skip).
- No provider APIs, no image generation, no interpolation/optical flow/video,
  no ffmpeg, no GUI. `plan.seed` is still never consumed (milestone 4).

## Suggested next work (milestone 3 boundary)

Layered-sprite input: one PNG per declared `target`, a layer manifest bound
into `plan_digest`, per-layer anchors and composition order, per-layer pose
rendering reusing `geometry.py`, and layer-aware validation that finally
pixel-verifies target-local tracks. Keep the milestone-2 whole-sprite path as
the flattened fallback. Any new artifact/field again requires schema, loader,
validator, docs, and tests in the same change; still no claim that a flattened
sprite can be decomposed automatically.
