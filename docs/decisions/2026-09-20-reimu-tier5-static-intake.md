# Tier5 static intake — 2026-09-20

Tier5 represents five or more active tasks: a happy meal with ramen, rice
balls, side dishes, tea, sparkles, and heart marks. The existing Eating Set v1
task_5 source is preserved byte-for-byte in
`build/reimu-tier5-intake-20260920/source-base.png`. SHA-256:
`ffd3752c4cdf333a88dc70e766dc4fbdf584662bb242365b3a3ff8a2860f8342`.
It is a 596×596 RGBA sprite; alpha bbox is (76,11,520,586), with a 10 px
bottom margin.

The public Harness plan/render/validate/preview/contact-sheet pipeline passed
in both full and reduced-motion modes. Each mode has one 125 ms frame and loops
as a static hold. Decoded RGBA is identical to the source in both modes, and
the original Consumer source digest is unchanged. The expected `ZERO_MOTION`
warning is retained; this is not an authored eating animation.

Artifacts are under `build/reimu-tier5-intake-20260920/`, including the pinned
input specification, intake receipt, full/reduced builds, previews, and saved
QA reports. The agent inspected the source and the 160 px contact sheet: the
meal and expression remain readable and there is no clipping. Native
integration is tracked separately. Human visual approval remains pending. No
application was installed and no Tier5 commit or publication occurred.
