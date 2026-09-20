# Reimu task_1 native visual approval and packaging-gate release

Date: 2026-09-20

The user reviewed the delivered Tier1 native review artifacts and replied
“收口”. This closes the visual gate for the exact one-frame vertical slice
shown by those artifacts. It closes only the visual boundary left open by
`2026-09-20-reimu-tier1-native-static-slice.md`; that earlier technical record
remains unchanged historical evidence.

## Approved subject

- `runtime-preview/review-sheet.png` SHA-256:
  `6051e752d620237af54c76acf877820058a81f9f8efc542819c8c7c344248281`.
- `runtime-preview/runtime-review.gif` SHA-256:
  `74e9dd2f77c27ccc1ff21ec255deef3d1300c2ec39a9bd2f13e25753301a338c`.
- `qa/native-size-review.png` SHA-256:
  `6fea4ee19f9f057b995969e6f146f4bcc3f5ab5f4f7c51116ce8443ca09abf87`.
- Tier1 source PNG SHA-256:
  `8dd9ff95bcfc2a891c997564496097328ec800d83b887ed08b54a608fe410e0e`.
- The reviewed preview's Tier1 source-manifest SHA-256:
  `10cfbb9daa8247421782c9b4e64aaef449567e5a6e06e310c7788afc0308b5eb`.
- Approval covers the displayed native size, placement, support and crop, the
  one-frame static hold, Tier1–5 switching, count-nine capping to Tier5,
  immediate `needs_input` preemption, and recovery using the latest count-four
  snapshot.

This approval does not claim or approve a multi-frame eating animation, new
entry/exit or cross-tier transition artwork, installation, tag, or package
release.

## Source and build boundary after approval

The source manifest's approval sentence was updated without changing an image,
frame binding, playback field, or provenance field. Its new SHA-256 is
`ad9e4b9887359df3d2567d434ab169993b33e5026578e50351a0722c0624b84f`;
the base and frame remain byte-identical to the approved PNG digest above.

The Consumer's `desktop/macos/build.py --work-tier-1` no longer requires
`--preview`. It still fails closed on the exact manifest digest, identity,
canvas, playback declaration, frame path, and image SHA-256. The existing
1.13/build15 preview remains the exact visual evidence that the user approved.
No application was installed or package release created.

## Post-approval verification

Using MacOSX26.5.sdk and isolated module caches under `/private/tmp`, a fresh
1.13/build15 preview compiled successfully from the approved source. Its
executable SHA-256 is
`de4c3d47c464e2a8e269b9d496977392ca10b05fe4ded78416dbca97eb4c380c`.
A separate temporary non-preview build also passed the released production
gate; its executable SHA-256 is
`61dfb650a8f4c2016efe7f6bb05cac0bf13e9e576c8a202206a49cc79fef691b`.
Both `/private/tmp` bundles passed strict deep signature verification. The
non-preview bundle was only a gate check and was not installed or published.

The approved source passed 198 Swift behavior checks, 37 native AppKit checks,
125 Consumer tool tests with the Harness CLI available and no skips, 14 bridge
tests, the browser runtime check, 31 status contract cases, four isolated
loading/fallback cases for each of Tiers 1–5, three reaction checks, five
standing checks, the Consumer repository gate, and diff whitespace checks.
The Harness aggregate passed 674 tests; the evidence report is
`build/verification/20260920T051509.747320Z/report.json`. A preceding sandboxed
attempt is retained separately and records that its only failure was denial of
the test suite's temporary `127.0.0.1` bind.
