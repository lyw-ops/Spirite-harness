# Roadmap

Milestones are strictly separated so the contract stabilizes before any pixel
synthesis exists. Each milestone builds on the artifacts of the previous one;
none may weaken the provider-neutral boundary in [`HARNESS.md`](../HARNESS.md).

## Milestone 1 — Contract + validation (current)

- Animation Plan IR, JSON Schemas (plan, frame plan, QA report, frame manifest)
- `sprite-harness plan`: normalization and deterministic expansion into a
  digest-bound frame plan; no pixel synthesis
- Plan validation, build-directory validation, frame-set validation
  (dimensions, alpha, numbering, bounding-box/ground drift, displacement)
- GIF preview and contact sheet from rendered frame directories
- Deterministic QA reports

## Milestone 2 — Deterministic transform renderer

- Render `build/frames/` from a single source sprite by applying the frame
  plan's whole-sprite transforms (translate; then rotate/scale/opacity) with
  Pillow, honoring anchor placement and transparent padding
- Golden-file tests: rendered frames must pass milestone-1 validation
- Reduced-motion variants rendered from the same plan

## Milestone 3 — Layered-sprite animation

- Optional layered input (one PNG per declared `target`) so tracks address
  real parts instead of the whole sprite
- Layer composition order, per-layer anchors, and layer-aware validation
- Still no claim that flattened sprites can be decomposed automatically

## Milestone 4 — Optional AI-assisted frame generation

- A renderer adapter interface where an image model proposes frames for
  targets the deterministic renderer cannot honor (mouth shapes, blinks)
- The plan's `seed` becomes meaningful; generated frames must still pass the
  same deterministic validation and QA gates
- Adapters live outside the core; the core never depends on a provider SDK

## Milestone 5 — Sprite-sheet / atlas exporters

- Pack validated frame sets into sprite sheets and atlas layouts (e.g. fixed
  cell grids such as the 8×11 / 192×208 desktop-pet contract) with metadata
- Export manifests for common runtimes; round-trip validation of packed atlases
