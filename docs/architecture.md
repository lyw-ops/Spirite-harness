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
source sprite + Animation Plan spec
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
| `geometry.py` | Whole-sprite pose sampling (rotate sums, scale/opacity factor products) and the documented anchor-affine transform shared by renderer and validator |
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

Source sprites and source frames are never modified. `plan` writes only into
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
