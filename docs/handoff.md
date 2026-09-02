# Project handoff

Last updated: 2026-09-03

## Status

Milestone 1 (contract + validation) is implemented and hardened. The hardening
pass closed five contract gaps: full frame-plan integrity validation, source
identity revalidation, strict JSON at every boundary, loop-cycle continuity,
and whole-sprite vs target-local offset semantics. No renderer exists yet by
design; see `docs/roadmap.md`. Example art is placeholder-only or
specification-only; no finished animation artwork is claimed.

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
- Build-directory validation (`build.py`): full frame-plan recomputation,
  source identity re-inspection, and rendered-frame checks
- Strict JSON boundary (`jsonio.py`) shared by the CLI, artifacts, QA reports,
  and digest canonicalization
- Frame-manifest layer unchanged in behavior

## Hardening decisions (2026-09-03)

### Full frame-plan integrity

`validate` recomputes the **entire** expected frame plan from `plan.json`
alone (loaded, semantically validated, re-expanded) and compares every
authoritative section in canonical strict-JSON form, so changed values,
changed JSON types (`32` vs `32.0`, `true` vs `1`), added fields, and removed
fields all fail. Nothing from the frame plan under test feeds the
recomputation. Codes: `MALFORMED_FRAME_PLAN` (unknown/missing top-level fields
or an invalid document envelope), `FRAME_PLAN_STALE` with a `section` context
(recomputed content mismatch, including nested added/removed fields; `frames`
mismatches also report `first_mismatch_index`),
`FRAME_PLAN_SOURCE_MISMATCH` (source binding differs from the plan's
digest-bound identity). `generated_by` is deliberately provenance-only: it
must match `sprite-harness <version>` in shape (error otherwise), and a
different release yields only the `GENERATED_BY_MISMATCH` warning so builds
stay validatable across releases.

### Source identity and revalidation

`create_build` writes the source into the generated `plan.json` as
`source: {image, sha256, width, height}` with `image` rewritten (via
`os.path.relpath`) to resolve from inside the build directory — this covers
`--source` overrides and makes the identity part of `plan_digest`. The
Animation Plan schema/loader gained optional `source.sha256/width/height`, so
`plan.json` still round-trips through the loader, and an input spec may pin
its source. `validate` re-opens the source read-only and compares digest,
dimensions, and the alpha requirement (`SOURCE_NOT_FOUND`,
`SOURCE_INVALID_IMAGE`, `SOURCE_DIGEST_MISMATCH`,
`SOURCE_DIMENSION_MISMATCH`, `SOURCE_ALPHA_REQUIRED`; new check id
`source_identity`). The canvas fallback in `load_build` now comes from the
plan's declared source dimensions, never from the untrusted frame plan.
Builds without a source keep working when the plan declares a canvas.

### Strict JSON

All serialization goes through `jsonio.dumps_strict` (`allow_nan=False`);
non-finite numbers in diagnostic contexts become the deterministic strings
`"NaN"`/`"Infinity"`/`"-Infinity"` first, so a `.nan` FPS still reports
`INVALID_FPS` at exit 1 instead of crashing. Free-form YAML `metadata` is
recursively validated as JSON-compatible (null, booleans, integers, finite
floats, strings, arrays, string-keyed objects); dates, sets, non-string keys,
and non-finite numbers are rejected at load time with
`METADATA_NOT_JSON_COMPATIBLE` (exit 2). `plan_digest` canonicalization uses
the same strict serialization (unchanged digests for all valid plans).

### Loop cycle continuity

For `playback.loop: true`, every track's `cycles` must be a positive integer
value (`2` or `2.0`; otherwise `NON_INTEGRAL_LOOP_CYCLES`). Whole cycles make
the sampled sequence exactly periodic, so every supported curve — periodic or
mirrored easing, at any phase — returns to its frame-0 value without a position
jump at the loop seam. Non-looping animations may keep positive fractional cycles. The
schema expresses the rule with a root-level `if playback.loop then
tracks[].cycles multipleOf 1`; the semantic validator enforces it
authoritatively.

### Whole-sprite vs target-local offsets

The track target `sprite` is reserved for whole-sprite transforms; **only**
translate tracks targeting `sprite` aggregate into the per-frame `offset`.
Displacement constraints, the frame-plan `offset`, and rendered-frame
bbox/ground checks all use these same semantics (they share
`sample_offsets`). Target-local tracks (`head`, `hand_right`, …) remain in
`transforms`, deterministic and per-frame, but never move the whole-sprite
expectation — milestone 1 cannot verify target-local pixels until the
milestone-3 renderer/layer contract exists. The Reimu example's breathing and
sway tracks now target `sprite`. Compatibility note: frame plans generated
before this change with translate tracks on part labels re-validate as stale;
re-run `plan`.

## Error-code changes

New: `FRAME_PLAN_SOURCE_MISMATCH`, `SOURCE_DIGEST_MISMATCH`,
`SOURCE_DIMENSION_MISMATCH`, `NON_INTEGRAL_LOOP_CYCLES`,
`INVALID_SOURCE_IDENTITY`, `METADATA_NOT_JSON_COMPATIBLE`; new warning
`GENERATED_BY_MISMATCH`. Broadened: `MALFORMED_FRAME_PLAN` (top-level envelope
problems), `FRAME_PLAN_STALE` (recomputed content mismatches, including nested
structural differences; now carries `section` /
`first_mismatch_index` context), and the `SOURCE_*` codes now also fire during
build validation. Exit codes 0–4 are unchanged.

## Schema changes

- `animation-plan.schema.json`: optional `source.sha256/width/height`;
  loop→integer-cycles conditional (`allOf`/`if`/`then`, `multipleOf: 1`);
  reserved-`sprite` target description; JSON-compatible metadata description.
- `frame-plan.schema.json`: `generated_by` pattern
  `^sprite-harness \S+$`; clarified `source.path` (build-relative, equals
  `plan.json` `source.image`) and whole-sprite `offset` descriptions. No
  structural changes; existing untampered artifacts still conform.

## Verification

Verified on macOS with Python 3.14.5, Pillow 12.3.0, PyYAML 6.0.3,
jsonschema 4.x, pytest 9.1.1. The package requires Python 3.11+.

```text
$ .venv/bin/pytest
151 passed            # was 73; +78 hardening regression tests
$ python -m compileall src/sprite_harness tests   # clean
$ pip check                                       # no broken requirements

# plan + validate, human and JSON modes, exit codes verified
$ sprite-harness plan --spec examples/reimu-eating/eating-loop.json --output <tmp>          # exit 0
$ sprite-harness validate <tmp> --write-qa [--json]                                         # exit 0
$ <edit frame-plan.json canvas.width to 999>; sprite-harness validate <tmp> --json          # exit 1, FRAME_PLAN_STALE(section=canvas)
$ sprite-harness plan --source base.png …; <replace base.png>; validate                     # exit 1, SOURCE_DIGEST_MISMATCH
$ plan with playback.fps: .nan (YAML)                                                       # exit 1, INVALID_FPS, "actual": "NaN"
$ sprite-harness validate examples/reimu-eating-task2 [--json]                              # exit 0 (manifest layer intact)
```

Every demonstrated `--json` output and persisted artifact was parsed with a
strict JSON parser (`json.loads(..., parse_constant=<reject>)`); no
NaN/Infinity tokens. Two builds from identical inputs and layout are
byte-identical (`plan.json`, `frame-plan.json`, `qa/plan.qa.json`), including
builds with a `--source`.

Local quirk: Python 3.14 on macOS skips `.pth` files carrying the hidden file
flag, which a sandboxed `pip install -e` can set. If `sprite_harness` cannot be
imported after an editable install, run
`chflags nohidden .venv/lib/python3.14/site-packages/*.pth`, or use a regular
`pip install '.[dev]'` (pytest uses `pythonpath=src` regardless).

## Known limitations and non-goals

- No renderer: `build/frames/` must currently be produced externally; preview
  on a build without frames fails with `FRAMES_NOT_RENDERED`.
- Target-local (non-`sprite`) transforms are expanded and digest-bound but
  cannot be pixel-verified until the milestone-3 layer contract exists.
- `generated_by` is provenance, not digest-bound (deliberate: builds must stay
  validatable across harness releases); tampering with it alone is detected
  only when the string shape breaks or the release differs (warning).
- `rotate`/`scale`/`opacity` tracks are expanded and schema-checked but not
  yet exercised by any renderer or measured validation.
- Background values other than `transparent` are metadata only.
- Source revalidation proves identity at validate time; it cannot prevent a
  swap after validation (no filesystem locking, by design).
- No provider APIs, diffusion/image-generation dependencies, ComfyUI, Live2D,
  interpolation, optical flow, video output, or ffmpeg.

## Suggested next work (milestone 2)

Deterministic whole-sprite transform renderer with Pillow: render
`build/frames/` from the frame plan (translate + anchor placement first),
golden-file tests that rendered output passes `validate`, and a
reduced-motion render mode. Any new plan fields require schema, docs, loader,
validator, JSON, and compatibility tests in the same change.
