# Reimu standing → Tier2 endpoint seam feasibility experiment

Date: 2026-09-20

This record covers only a bounded AI-only endpoint-seam feasibility experiment.
It does not create pose 1–5, a complete transition, a production package, a
Consumer route, a native runtime preview, visual approval, installation,
commit, or publication.

## Baseline and immutable endpoints

Both repositories were fetched before generation. Harness HEAD and
`origin/main` remain
`37d9384cc91ef3b3f0c349405d15f174f7c66c2f`; Consumer HEAD and
`origin/main` remain
`c2684cc3fecbdfbe0ae238a13f8e22fef333295d`. Existing uncommitted
specification, ledger, handoff, and failure records were preserved.

The four immutable bindings were re-read and match the frozen values:

- standing open pose:
  `4b390982469cedbc3b1a0b3792c49a686e2b87b7dda6e5ab12d7bc73cd3e75e7`;
- standing manifest:
  `85ef36b41e6c57305984525998a16887013aa5e5be6231453df60e4b46677496`;
- Tier2 frame 0:
  `0251947e0ca94f0ba0fa4b724d37fac242c86ba4de9591bb558c226ad4904cfe`;
- Tier2 source manifest:
  `81aa07c5503150f634a0b6e267f9621147f6f6a275e25b79b6c41e7ef1d447de`.

The 596×596 standing receipt was regenerated from the immutable 1254×1254
source using uniform `596/1254`, Pillow LANCZOS, placement `(0,0)`, and PNG
`compress_level=9`. Its SHA-256 remains
`02a087e34141aed4f65cb07a006f7275fadaf4aacb034f69c7aea598202a25b0`;
the declared standing support line remains `y=584.5933014354067`. The receipt
does not replace the standing source.

The endpoint-only review confirmed that the declared Tier2 support edge at
`y=585` is geometrically close to the standing line, but the endpoints do not
by themselves prove compatibility. Visually, Tier2 has a larger/livelier eye
read, a more compact seated head/body ratio, and a broad table/tatami footprint.

## Five bounded generation calls

The built-in image generator was used through the `imagegen` and `hatch-pet`
skills. No CLI/API fallback, model switch, segmentation, `rembg`, guessed mask,
historical failed pixel reuse, or endpoint pixel extraction was used. Five of
the six authorized calls were consumed; the last call was deliberately left
unused once one repair could no longer make all three layers pass.

| Call | Intended layer | Result |
| ---: | --- | --- |
| 1 | seated character | Best visual study: recognizable face/hair/bow and close target pose, true alpha and safe inset, but 77 detached components at alpha ≥ 8. Rejected. |
| 2 | character alpha repair | Same root issue remained and increased to 116 detached components at alpha ≥ 8. Rejected; no similar repair repeated. |
| 3 | clean character regeneration | Changed strategy still produced 103 detached components at alpha ≥ 8 and moved the lower body farther from Tier2 with visible forward shoes. Rejected. |
| 4 | fixed tatami back | True alpha and related perspective, but the main component touches the bottom edge, 121 border alpha pixels are nonzero, the front/right corner is clipped, and low-alpha components remain. Rejected. |
| 5 | fixed table/meal front | Correct content inventory and an inset main component, but low-alpha components remain; the table is deeper/taller with longer and differently placed legs than Tier2. Rejected. |

Every original is a new 1254×1254 RGBA generation stored only as diagnostic
evidence. The alpha reports, full prompts, SHA-256 values, and 596px plus
320px light/dark review sheets are under
`build/reimu-standing-tier2-seam-feasibility-v1/`.

## Composition and seam result

No layer passed the complete material gate. In particular, the strongest
character candidate passed identity review but failed the strict no-speck,
no-near-transparent-contamination rule. The tatami also failed crop safety,
and the table failed endpoint-near geometry.

Therefore no 596×596 composition parameters were chosen and no
`candidate.png`, `review-sheet.png`, `seam-review.gif`, endpoint overlay, or
endpoint diff was created. A placeholder or rejected-layer composite would
misrepresent the experiment. `composition.json` records the material-gate
stop instead.

The experiment result is **failed before composition**. It does not establish
whether a valid three-layer candidate can join Tier2 naturally. The current
diagnostics do show that, at 320px, the table depth/leg geometry and the third
character candidate's shoes remain visible differences; they are not hidden
by native display scale.

## Recommendation and gates

Do not author intermediate action frames yet. First obtain three independently
clean source layers with exact-zero background outside connected silhouettes,
safe inset, and endpoint-near feet, table, and tatami geometry. Then repeat the
same endpoint-only seam experiment. This is narrower and cheaper than making
pose 1–5 before the landing composition is proven.

`REIMU-WORK-TRANSITIONS-001` remains unchanged:

| Gate | Status |
| --- | --- |
| specification | `ready` |
| implementation | `pending` |
| technical | `pending` |
| visual | `pending` |
| consumer | `pending` |
| publication | `unpublished` |

The seam experiment itself is `failed`, not “in review” or approved. No
production behavior, `PetBehavior.foodTier`, provider state, installation,
commit, or push was touched.
