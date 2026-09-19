# Reimu task_4 native visual approval and packaging-gate release

Date: 2026-09-20

The user reviewed the delivered Tier 4 native review artifacts and replied
“可以”. This closes the visual gate for the exact one-frame vertical slice
shown by those artifacts. It closes only the visual boundary left open by
`2026-09-20-reimu-tier4-native-static-slice.md`; that earlier technical record
remains unchanged historical evidence.

## Approved subject

- `runtime-preview/review-sheet.png` SHA-256:
  `3f1c926b43a37ca22d3f335cd728d2800b0bdf55725989c97542ec915aea4a4f`.
- `runtime-preview/runtime-review.gif` SHA-256:
  `e509bdae43a6561cc1ae17045103e5e72a227d79663c275ec5b0d6b73c430f0f`.
- `qa/native-size-review.png` SHA-256:
  `3c6fffc41a160ea28a04db25d9e28cfe94e63fc3eb3f64151465cfb8fba2600a`.
- Tier 4 source PNG SHA-256:
  `9f0b18946eca4c7c0d27a8dbbd5f966da615867913d8e91c8454dd629de0b238`.
- The reviewed preview's Tier 4 source-manifest SHA-256:
  `311dc81875bbaac2953d2284a374bb709cf8ad7c8887dd438d91deac2db891ef`.
- Approval covers the displayed native size, placement, support and crop, the
  one-frame static hold, Tier 2/3/4 switching, immediate `needs_input`
  preemption, and recovery using the latest count-two snapshot.

This approval does not claim or approve a multi-frame ramen-eating animation,
new entry/exit or cross-tier transition artwork, installation, commit, push,
tag, or release.

## Source and build boundary after approval

The source manifest's approval sentence was updated without changing an image,
frame binding, playback field, or provenance field. Its new SHA-256 is
`c187f8d4390d4f082001c599dab6d2dbd8e699662c9a42cbe84bed9cd3300221`;
the base and frame remain byte-identical to the approved PNG digest above.

The consumer's `desktop/macos/build.py --work-tier-4` no longer requires
`--preview`. It still fails closed on the exact manifest digest, identity,
canvas, playback declaration, frame path, and image SHA-256. The existing
1.11/build 13 preview remains the exact visual evidence that the user approved.
No formal-identity Tier 4 application or archive was generated in this step,
and nothing was installed or published.

## Post-approval verification

Using the existing MacOSX26.5.sdk compatibility path and isolated module caches
under `/private/tmp`, a fresh 1.11/build 13 preview compiled successfully from
the updated dirty Consumer source. Its executable SHA-256 is
`d752555fd4f347784a33371e5f29947302f6768118bf7d1ab81c5657bd3be45f`.
The packaged Tier 4 manifest has the new digest above, and its base PNG retains
the approved image digest.

The rebuilt preview passed strict deep signature verification and all four
Tier 4 loader/isolation cases: accepted package, damaged frame, malformed
manifest, and missing base. Each broken-package case continued to degrade only
Tier 4. The Consumer repository gate and diff whitespace check also passed.
The Harness aggregate verifier passed 674 pytest cases plus workflow generation,
byte compilation, diff, and layered smoke gates; the timestamped receipt lives
under the ignored `build/verification/` evidence directory.
This verification used an isolated preview build; it did not connect to the
real task provider or create a production-identity deliverable.
