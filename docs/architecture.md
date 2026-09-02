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
                 v  (renderer, milestone 2+)
             build/frames/*.png
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
| `build.py` | Build-directory creation, loading, validation (full frame-plan recomputation, source identity re-inspection, rendered-frame drift checks), manifest adapter |
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
Normalization writes under `generated/`. The generated frame plan and
manifests make derived frame sets explicit instead of relying on directory
conventions at runtime.

## Error boundary

Syntax and required-shape failures are specification errors (exit 2; missing
inputs exit 3). Parsed but invalid values, constraint violations, and frame
problems are validation failures (exit 1). Rendering, output, and other
operational failures are processing failures (exit 4). CLI exit codes and
structured JSON preserve that distinction for shell scripts and CI.
