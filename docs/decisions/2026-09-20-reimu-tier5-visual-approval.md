# Reimu task_5 native visual approval and packaging-gate release

Date: 2026-09-20

The user reviewed the delivered Tier5 native review artifacts and replied
“可以，收口后接着做”. This closes the visual gate for the exact one-frame
vertical slice shown by those artifacts. It closes only the visual boundary
left open by `2026-09-20-reimu-tier5-native-static-slice.md`; that earlier
technical record remains unchanged historical evidence.

## Approved subject

- `runtime-preview/review-sheet.png` SHA-256:
  `bbf3103a3dd17a4c239a36fc8cbddcfbe73e206c1c941404a7bee8b9d83a6b25`.
- `runtime-preview/runtime-review.gif` SHA-256:
  `4f43ad0f330e042ddcd3d6882b98edd9c64666c6399f4dd535d37592889c094d`.
- `qa/native-size-review.png` SHA-256:
  `85563fbc648587b391d3f42d159464879b5594a64062c6b643fc1190129a2bfb`.
- Tier5 source PNG SHA-256:
  `ffd3752c4cdf333a88dc70e766dc4fbdf584662bb242365b3a3ff8a2860f8342`.
- The reviewed preview's Tier5 source-manifest SHA-256:
  `3bf14a0d2eaada5e584679acd59ed10686980984c6299ab33a7efeca47ca1a16`.
- Approval covers the displayed native size, placement, support and crop, the
  one-frame static hold, Tier2/3/4/5 switching, five-or-more capped selection,
  immediate `needs_input` preemption, and recovery using the latest count-four
  snapshot.

This approval does not claim or approve a multi-frame eating animation, new
entry/exit or cross-tier transition artwork, installation, tag, or package
release.

## Source and build boundary after approval

The source manifest's approval sentence was updated without changing an image,
frame binding, playback field, or provenance field. Its new SHA-256 is
`0b48b3730b2b26e6043af5a229bd0033fc6b97615e1d67dc14a4897cc4fd9a3f`;
the base and frame remain byte-identical to the approved PNG digest above.

The Consumer's `desktop/macos/build.py --work-tier-5` no longer requires
`--preview`. It still fails closed on the exact manifest digest, identity,
canvas, playback declaration, frame path, and image SHA-256. The existing
1.12/build14 preview remains the exact visual evidence that the user approved.
No application was installed or package release created.

## Post-approval verification

Using MacOSX26.5.sdk and isolated module caches under `/private/tmp`, a fresh
1.12/build14 preview compiled successfully from the approved source. Its
executable SHA-256 is
`da690effe51cdfb79d67ea3943fa8694fb926e4aaee25e58da15b4206504096e`.
A separate temporary non-preview build also passed the released production
gate; its executable SHA-256 is
`34682de6c185bc06758a54aaea54775e5b7954d903f16720547549152a131a99`.
Both bundles passed strict deep signature verification. The non-preview bundle
was only a `/private/tmp` gate check and was not installed or published.

The approved source passed 190 Swift behavior checks, 36 native AppKit checks,
125 Consumer tool tests, 14 bridge tests, the browser runtime check, 31 status
contract cases, four isolated loading/fallback cases for each of Tiers 2–5,
three reaction checks, five standing checks, the repository gate, and diff
whitespace checks.
