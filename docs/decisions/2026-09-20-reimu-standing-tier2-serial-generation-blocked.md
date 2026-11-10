# Standing-to-Tier2 single-frame AI-only attempt

Date: 2026-09-20

This is a new attempt after the earlier multi-pose generation failure. It does
not replace that failure record or reuse any of its pixels. The user authorized
only `standing_to_tier_2`, using serial character edits, two independent fixed
scene layers, and deterministic composition after material acceptance.

Both repositories were fetched. Harness HEAD and origin/main remain
`37d9384cc91ef3b3f0c349405d15f174f7c66c2f`; Consumer HEAD and origin/main remain
`c2684cc3fecbdfbe0ae238a13f8e22fef333295d`. Existing uncommitted specification,
ledger, handoff, and failure-record content was preserved. No production Swift
code, task-count policy, real provider state, installation, commit, or push was
performed.

## Immutable inputs and receipt

All four SHA-256 bindings match before and after generation:

| Input | SHA-256 |
| --- | --- |
| Standing open pose | `4b390982469cedbc3b1a0b3792c49a686e2b87b7dda6e5ab12d7bc73cd3e75e7` |
| Standing manifest | `85ef36b41e6c57305984525998a16887013aa5e5be6231453df60e4b46677496` |
| Tier2 frame 0 | `0251947e0ca94f0ba0fa4b724d37fac242c86ba4de9591bb558c226ad4904cfe` |
| Tier2 source manifest | `81aa07c5503150f634a0b6e267f9621147f6f6a275e25b79b6c41e7ef1d447de` |

The standing receipt was regenerated from the original 1254-square image with
Pillow 12.3.0 LANCZOS, uniform `596/1254`, placement `(0,0)`, PNG
`compress_level=9`. Its SHA-256 is
`02a087e34141aed4f65cb07a006f7275fadaf4aacb034f69c7aea598202a25b0`.
The mapped shoe support is `y=584.5933014354067`; the alpha bbox is
`(165,16,445,587)`. The alpha extent is not a redefinition of the shoe line.
Default PNG compression initially produced different file bytes with identical
RGBA pixels; recording compression level 9 resolved the byte mismatch.

Tier1–5 source/runtime manifests and all listed frame digests were recomputed.
Tier2 remains 16 frames at 10 fps, 1600 ms; Tiers1/3/4/5 remain single 125 ms
stills. This audit does not validate a new transition.

## Seven new diagnostic candidates

The built-in imagegen path was used through the imagegen and hatch-pet skills,
with one visual worker per asset. No API/CLI fallback or local raster generation
was used. Every call generated or edited one square image; no six-pose sheet
was requested. Scene jobs were independent; the character chain never advanced
past pose 1. Exact prompts are preserved with digests in the local report.

| Candidate | SHA-256 | Rejection |
| --- | --- | --- |
| table-initial | `8ad2581d9bd63cb2e18749252337459d914393c7b3bf8f1a5b73e12daa6858d9` | Detached low-alpha speckles and table proportion mismatch. |
| tatami-initial | `a4c685e1e4ba6f88a3dc4acc493dafcf0013299253878b7750a9b98e942f548d` | Bottom corner touches boundary; low-alpha background contamination. |
| pose1-initial | `d21541b6ca8ceac11826955c9ef3a3aa61266beb4c8882392828125b13b70a90` | Transparent instead of required green; knee bend unclear; eye-size drift. |
| table-repair | `2a708b0d4c08dc59cd93eab4da77a45e17fe1610b73a7d5bc6145d5daf595c89` | Nonuniform green background; table remains too wide. |
| tatami-repair | `bd7b3adef39fe1181383cc8fc1afc1e85b03a4089e19ec9e4a114f020bb8e19a` | Nonuniform green background; bottom corner still touches boundary. |
| pose1-repair | `5a2a1bb9e4aabe6afbe16f1316dae0988115aef04d4d1cd0b158a6df735e67c3` | Nonuniform green background; knee bend and eyes still fail. |
| pose1-regenerate | `7872481c0abd8eb9cfdebb7164979d6af3962c1ec5db7741ac21fc31a719ac01` | Fresh clean-standing edit still gives nonuniform background and unclear knee bend. |

Each scene candidate received one targeted repair. Pose 1 received one
background repair, then a changed strategy: regenerate the current pose from
the clean standing endpoint instead of editing the contaminated candidate.
Standing and Tier2 were attached as identity and target references. The final
result still failed the uniform-background gate, so generation stopped under
the user's convergence rule.

The read-only background gate uses zero RGB tolerance for the requested exact
`#00FF00`, checks the complete border and 10-percent corner patches, requires
at least 35 percent exact-green canvas coverage, and still requires visual
background/identity/motion inspection. This is a conservative intake test,
not an image segmentation algorithm. No candidate passed the combined gates.
No chroma key, alpha cleanup, rembg, guessed mask, morph, fade, hidden scale,
historical cut pixels, or static substitute was applied.

## Artifacts and gates

Local evidence is under
`build/reimu-work-transition-standing-to-tier2-serial-v1/`:

- `failure-report.json`: candidate/prompt hashes, reasons, endpoints, gates;
- `qa/preflight.json`: fetched refs, original dirty-file hashes, receipt;
- `qa/*-initial.json`, `qa/*-repair.json`, `qa/pose1-regenerate.json`: pixel metrics;
- `qa/existing-tier-manifest-audit.json`: existing Tier1–5 digest checks;
- `prompts/` and `candidates/`: this round's new prompts and unmodified rejected PNGs;
- `standing-596.png`: deterministic endpoint receipt, not new authored art;
- `qa/final-validation.json`: repository-check results after this record.

These PNGs are diagnostic candidates, not formal `originals/` or frames.
No transition source manifest, Consumer import tool, eight-frame sequence,
full/reduced transition build, endpoint seam comparison, stable-scene sequence,
route tests, native app preview, runtime GIF, or contact sheet exists. In
particular, frame6→7 continuity and six-frame scene stability are untested.
No real provider state was read or written.

| Gate | Status |
| --- | --- |
| specification | ready |
| implementation | pending |
| technical | pending |
| visual | pending |
| consumer | pending |
| publication | unpublished |

Repository validation is recorded separately from transition acceptance.
A future attempt must first establish a genuinely uniform character background
and identity-preserving knee motion, then complete the six serial poses and
fixed-layer geometry. No endpoint exception or weakened background rule was
approved by this attempt.
