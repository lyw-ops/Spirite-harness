# Tier4 static intake — 2026-09-20

Tier4 represents exactly four active tasks: happy ramen eating with dumplings.
The existing Eating Set v1 task_4 source is preserved byte-for-byte in
`build/reimu-tier4-intake-20260920/source-base.png`.
SHA-256: `9f0b18946eca4c7c0d27a8dbbd5f966da615867913d8e91c8454dd629de0b238`.
It is a 596×596 RGBA sprite; alpha bbox is (78,35,517,586), with a 10 px bottom margin.

The public Harness plan/render/validate/preview/contact-sheet pipeline passed
in both full and reduced-motion modes. Each mode has one 125 ms frame, looping
as a static hold. Decoded RGBA is identical to the source in both modes, and the
original consumer source digest is unchanged. The expected ZERO_MOTION warning
is retained; this is not an authored eating animation.

Artifacts are under `build/reimu-tier4-intake-20260920/`, including the pinned
input specification, intake receipt, full/reduced builds and saved QA reports.
The agent inspected the source and the 160 px contact sheet: meal and expression
remain readable and there is no clipping. Human review of this candidate and
choice of next scope are pending. No consumer/runtime code, app installation,
commit or publication changed. Existing Tier3 working-tree changes are preserved.

Next scope was offered to the maintainer: static native integration like Tier3,
static artwork revision, or authored eating motion. Native integration, if chosen,
must select exact count four, preserve safe loop-boundary changes and immediate
high-priority interruption, and provide isolated missing/corrupt asset fallback.
