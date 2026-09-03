# Roadmap

Milestones are strictly separated so the contract stabilizes before any pixel
synthesis exists. Each milestone builds on the artifacts of the previous one;
none may weaken the provider-neutral boundary in [`HARNESS.md`](../HARNESS.md).

## Milestone 1 — Contract + validation (implemented)

- Animation Plan IR, JSON Schemas (plan, frame plan, QA report, frame manifest)
- `sprite-harness plan`: normalization and deterministic expansion into a
  digest-bound frame plan; no pixel synthesis
- Plan validation, build-directory validation, frame-set validation
  (dimensions, alpha, numbering, bounding-box/ground drift, displacement)
- GIF preview and contact sheet from rendered frame directories
- Deterministic QA reports

## Milestone 2 — Deterministic transform renderer (implemented)

- `sprite-harness render`: `build/frames/` from a single source sprite by
  applying the frame plan's whole-sprite transforms (translate, rotate,
  uniform scale, opacity) with Pillow, honoring anchor placement and
  transparent padding — semantics fixed in `docs/renderer.md`
- Render manifest (`render.json`, `schemas/render.schema.json`) binding the
  frame set to its plan revision and motion mode; transactional writes;
  model-based frame validation from the trusted source image
- Hand-computed reference tests; rendered frames pass milestone-1 validation
- Reduced-motion variants (`--reduced-motion`, `hold_first_frame`) rendered
  from the same plan
- Target-local tracks are skipped with a stable warning, never approximated

## Milestone 3 — Layered-sprite animation (implemented, 0.5.0)

- Animation Plan/frame-plan v2: inline ordered PNG layers, explicit reference
  canvas, build-relative paths and every layer identity bound to the plan digest
- Independent local translation/rotation/uniform scale/opacity, alpha-over
  composition then one M2 global transform; anchors and clipping fixed in
  [layered-sprites.md](layered-sprites.md)
- Layer-aware source/transform/final RGBA validation, reduced-motion hold,
  existing transaction safety and complete CLI/QA pipeline
- V1 single-image plans and their pixel algorithm remain supported
- Still no claim that flattened sprites can be decomposed automatically

## Milestone 4 — Optional source-space generation (implemented, 0.7.0)

- Strict spec/request/response/accepted-input contracts and explicit subprocess
  argv; copied references and accepted PNGs; stable seed derivation.
- Frozen source replacement before unchanged local/global rendering; offline
  original/generated identity and final RGBA validation, full/hold modes.
- External separately installable OpenAI image edit adapter and offline geometric
  test substitute. Real adapter transport tests pass; live provider acceptance
  remains uncompleted pending explicit authorization and credentials.
- Bounded subprocesses/responses/images, transactional publication and recovery.

## Milestone 5 — Deterministic grid atlases (implemented, 0.7.0)

- One exporter for a single build or explicit ordered clips, fixed cell/padding,
  computed or fixed capacity, full canvases and transparent unused pixels.
- Versioned layout/provenance/timing/pivot metadata and subject-bound QA.
- Offline input revalidation and complete per-frame RGBA round trip; metadata,
  mode changes, padding and stale QA are checked from recomputed expectations.
- PNG byte identity observations stay distinct from pixel equivalence.

Later work: runtime-specific adapters, optional standalone atlas trust modes,
trimming/rotation and other packing algorithms require separate contracts.
No interpolation, optical flow, video, automatic decomposition or GUI is included.
