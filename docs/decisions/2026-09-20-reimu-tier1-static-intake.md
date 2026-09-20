# Tier1 static intake — 2026-09-20

Tier1 represents exactly one active task: Reimu eating one onigiri with a
slightly teary expression. The existing Eating Set v1 task_1 source is
preserved byte-for-byte in
`build/reimu-tier1-intake-20260920/source-base.png`. SHA-256:
`8dd9ff95bcfc2a891c997564496097328ec800d83b887ed08b54a608fe410e0e`.
It is a 596×596 RGBA sprite; alpha bbox is (78,76,517,586), with a 10 px
bottom margin.

The public Harness plan/render/validate/preview/contact-sheet pipeline passed
in both full and reduced-motion modes. Each mode has one 125 ms frame and loops
as a static hold. Decoded RGBA is identical to the source in both modes, and
the original Consumer source digest is unchanged. The expected `ZERO_MOTION`
warning is retained; this is not an authored eating animation.

Artifacts are under `build/reimu-tier1-intake-20260920/`, including the pinned
input specification, intake receipt, full/reduced builds, previews, and saved
QA reports. The agent inspected the source and 160 px contact sheet: the
onigiri, expression, table, and tatami remain readable and there is no
clipping. Native integration is tracked separately. Human visual approval
remains pending. No application was installed and no Tier1 commit or
publication occurred.
