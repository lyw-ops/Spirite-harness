# Reimu standing-to-Tier2 entry generation attempt

Date: 2026-09-20

This record covers only the attempted artwork intake for the first
`standing_to_tier_2` vertical slice. It does not supersede the frozen transition
specification and does not create a transition package, runtime node, preview,
visual approval, consumer integration, installation, commit, or publication.

## Endpoint audit

Both repositories were fetched before work. Harness remained at
`37d9384cc91ef3b3f0c349405d15f174f7c66c2f` and Consumer remained at
`c2684cc3fecbdfbe0ae238a13f8e22fef333295d`, each equal to `origin/main`.
The pre-existing uncommitted specification and handoff edits were preserved.

The immutable endpoint files passed the same SHA-256 audit before and after the
attempt:

- standing open pose: `4b390982469cedbc3b1a0b3792c49a686e2b87b7dda6e5ab12d7bc73cd3e75e7`;
- standing manifest: `85ef36b41e6c57305984525998a16887013aa5e5be6231453df60e4b46677496`;
- Tier2 frame 0: `0251947e0ca94f0ba0fa4b724d37fac242c86ba4de9591bb558c226ad4904cfe`;
- Tier2 source manifest: `81aa07c5503150f634a0b6e267f9621147f6f6a275e25b79b6c41e7ef1d447de`.

A review-only 596x596 standing receipt was deterministically derived with one
uniform `596 / 1254` Pillow LANCZOS resample at `(0, 0)`. Its SHA-256 is
`02a087e34141aed4f65cb07a006f7275fadaf4aacb034f69c7aea598202a25b0`;
the approved shoe line maps from `1230 / 1254` to `y = 584.5933014354067`.
The receipt does not replace or modify the standing source.

## Artwork attempts and stop condition

The built-in image generator was given both immutable endpoints as references
and a 3x2 layout-only guide. Two complete-scene attempts produced six real
character poses, but both kept a non-key gradient background and redrew the
table, tatami, plate, food, and cup differently from cell to cell. They failed
the fixed-scene requirement.

The strategy was then changed to explicit layers. A transparent table/meal
foreground was produced, but the six-pose character-only sheet again contained
a visible gradient. A final background-extraction edit still did not produce a
usable transparent alpha layer. At that point the repeated root failure met the
mandatory stop condition.

The rejected attempts and their digests are recorded in
`build/reimu-work-transition-standing-to-tier2-v1/failure-report.json`. They
are diagnostic evidence only and are not transition originals, approved art,
or runtime inputs.

No local segmentation, whole-scene transform, cross-dissolve, optical flow,
automatic morph, historical cut pixels, or static placeholder preview was used
to conceal the failure. Because no valid character layer exists, deterministic
assembly, the eight-frame package, Harness full/reduced validation, native
preview, interruption tests, and Consumer import were not run.

## Gate result

| Gate | Status | Boundary |
| --- | --- | --- |
| specification | `ready` | The existing freeze remains authoritative. |
| implementation | `pending` | No usable authored character source, eight-frame package, or manifest exists. |
| technical | `pending` | No final material snapshot exists to validate. |
| visual | `pending` | No valid native preview was created; nothing is in review or approved. |
| consumer | `pending` | Production behavior and the Consumer tree were not integrated. |
| publication | `unpublished` | Nothing was committed, pushed, tagged, installed, or released. |

The next attempt requires a genuine transparent six-pose character sheet or
explicit character layers with stable identity, plus fixed scene layers. Only
then may deterministic assembly and the isolated native-review contract resume.
