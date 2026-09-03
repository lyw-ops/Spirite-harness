# Architecture

```text
Claude Code ----\
Codex -----------+-- shell / CLI / JSON --> Sprite Harness Core --> artifacts
Human / CI -----/
```

All callers share one interface. Nothing in `src/sprite_harness` imports or
requires an agent or image-generation provider, and deterministic validation
never requires an LLM.

## Pipeline

```text
single sprite / explicit PNG layers + Animation Plan spec
        |
        `--> plan ----> build/plan.json + build/frame-plan.json + build/qa/plan.qa.json
                 |
                 v
             render [--reduced-motion] --> build/frames/*.png + build/render.json
                 |
                 +--> validate [--write-qa] --> build/qa/frames.qa.json
                 +--> preview / contact-sheet --> build/preview.gif, build/contact-sheet.png

source frames + animation.yaml (frame-manifest layer)
        |
        +--> validate / report (read only)
        +--> normalize --> generated/normalized/*.png + generated/animation.yaml
        +--> preview / contact-sheet --> generated artifacts
```

## Modules

| Module | Responsibility |
| --- | --- |
| `plan.py` | Locate and parse Animation Plans (JSON/YAML) into typed immutable data |
| `plan_validator.py` | Value-level plan checks: versions, anchors, tracks, events, displacement budgets |
| `curves.py` | Deterministic curve sampling (periodic and mirrored easing curves) |
| `expand.py` | Plan normalization, content digest, and expansion into the frame plan |
| `build.py` | Build-directory creation, loading, validation (full frame-plan recomputation, source identity re-inspection, transaction/manifest gates, mode-aware geometry and built-in RGBA verification), manifest adapter |
| `geometry.py` | Global and target-local pose sampling, finite effective-value checks, (rotate sums, scale/opacity factor products) and the documented anchor-affine transform shared by renderer and validator |
| `layers.py` | Loads all explicit PNG layers, samples local poses, clips and alpha-over composites on the reference canvas, then dispatches through unchanged M2 `render_pose` |
| `render.py` | Deterministic renderer: input/output safety checks, exclusive transaction marker, whole-directory publication, rollback/recovery, render manifest (docs/renderer.md) |
| `qa.py` | Deterministic QA report assembly and JSON artifact writing |
| `jsonio.py` | Strict JSON boundary: `allow_nan=False` serialization, deterministic non-finite diagnostics, JSON-compatibility checks for free-form metadata |
| `spec.py` | Locate and parse frame manifests into typed immutable data |
| `validator.py` | Manifest frame checks: filesystem, image, dimensions, aspect, alpha |
| `normalize.py` | Explicit uniform scaling, transparent padding, anchor placement, derived manifest |
| `preview.py` | Frame-duration-aware animated GIF generation with Pillow |
| `contact_sheet.py` | Deterministic labeled development overview |
| `report.py` | Shared report model plus human rendering |
| `processing.py` | Shared processing errors and source-artwork output guards |
| `cli.py` | Argument parsing, build-dir dispatch, JSON envelopes, error mapping, exit codes |

## Artwork lifecycle

Source sprites, all layer PNGs, and layer descriptions are never modified. `plan` writes only into
its build directory and refuses an output directory that coincides with the
spec's or source's directory. The generated `plan.json` records the source
with a build-relative path plus its SHA-256 and dimensions, and `validate`
re-inspects the file read-only against that digest-bound identity.
Normalization writes under `generated/`. `render` reads the source read-only,
re-validates every input, rejects output symlinks and source collisions, and
stages frames under an exclusive `.render-transaction/` marker. Whole-directory
publication replaces only declared derived products (`frames/frame_NNN.png`
and `render.json`) with backups and rollback — unknown files are never deleted.
Unfinished transactions block consumers until recovery. The generated frame plan
and manifests make derived frame sets explicit instead of relying on directory
conventions at runtime.

## Error boundary

Syntax and required-shape failures are specification errors (exit 2; missing
inputs exit 3). Parsed but invalid values, constraint violations, and frame
problems are validation failures (exit 1). Rendering, output, and other
operational failures are processing failures (exit 4). CLI exit codes and
structured JSON preserve that distinction for shell scripts and CI.

## Layered contract

V2 Animation Plans use an inline `source.layers` array and explicit
`source.reference_canvas`; the normalized plan is the runtime layer description.
There is no external manifest loader or metadata fallback. `plan.py` enforces
shape; `plan_validator.py` enforces targets, anchors, finite positions and
composed transforms. `build.py` inspects all PNGs and binds paths/hash/dimensions;
`expand.py` emits a v2 frame plan with ordered local poses and a global pose.
V1 normalization/expansion stays compatible. `render.json` and QA stay v1.

The renderer and validator both use `LayerScene` to reconstruct the composite
from verified inputs. Independent hand-computed RGBA/coordinate tests guard
against shared implementation errors. Input errors stop frame consumption;
output artifacts never supply missing expected values. `processing.py` also
protects all inputs from plan/QA/preview output aliases. The full contract and
external-frame verification boundary are in [layered-sprites.md](layered-sprites.md).

## Generation and export (0.7.0)

`contracts.py` provides strict bounded JSON and packaged schema checking without
adding a runtime jsonschema dependency. The root schemas and packaged copies
must match. `generation.py` normalizes requests, runs an explicit subprocess,
accepts PNGs and verifies frozen bundles offline. `ReplacementScene` selects
source pixels before existing LayerScene/global rendering. `transactions.py`
provides input identity snapshots and reversible directory publication for
new stages; the existing render transaction implementation remains in place.
`atlas.py` validates builds, computes one grid layout, publishes artifacts and
checks every crop against trusted input pixels. `adapters/openai` is a separate
Python distribution; it is never imported by the core. Credentials stay only
in the adapter process environment. See the new contracts for precise versions,
trust limits, quotas and recovery.
