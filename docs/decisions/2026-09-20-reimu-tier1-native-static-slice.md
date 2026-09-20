# Reimu Tier1 native static vertical slice

Date: 2026-09-20

## Scope and source boundary

The existing Eating Set v1 `task_1` drawing is connected to the native
Consumer as the explicit `work_eating_task_1` identity. It is selected only
when the observed state is `working` and the single
`PetBehavior.foodTier(activeTaskCount:)` policy maps the current count to
exactly Tier1. No second count-to-tier policy was introduced.

The source, runtime base, and only runtime frame are byte-identical 596×596
RGBA PNGs with SHA-256
`8dd9ff95bcfc2a891c997564496097328ec800d83b887ed08b54a608fe410e0e`.
No source pixel was regenerated, repainted, segmented, resized, or moved. The
package declares one 125 ms frame and remains an honest static hold. It is not
a completed eating animation, and the flattened character, onigiri, table,
tatami, tear marks, and expression are never moved as a whole to imitate
motion.

## Runtime behavior

- A change from animated Tier2 to Tier1 waits for the current 1.6-second Tier2
  loop boundary.
- Tiers 1, 3, 4, and 5 are static safe frames, so leaving them adds no
  artificial wait.
- Failure, needs-input, click, drag, pause, and every path that leaves
  `working` preserve immediate priority. Recovery re-evaluates the newest
  observed count rather than restoring a stale Tier1 presentation.
- Reduced motion selects the same Tier1 frame 0.
- Missing base/frame data, manifest identity changes, and manifest or frame
  digest mismatches degrade only Tier1 to the existing standing clip. Tiers
  2–5, standing, manual feeding, reaction art, and slouch remain available.
- `desktop/macos/build.py --work-tier-1` requires `--preview`; production
  identity remains blocked until the user approves the native review.

## Native build and technical evidence

The independent preview is
`build/reimu-tier1-runtime-v1/灵梦桌宠预览.app`, version 1.13/build15,
bundle identifier `local.reimu.onigiri.preview`. It was freshly compiled from
the dirty, uncommitted Consumer worktree based on
`d2b6bef76d9b5330f5e56a7ee61fbe86c6cdf9ac`, using
`SDKROOT=/Library/Developer/CommandLineTools/SDKs/MacOSX26.5.sdk` and isolated
module caches under `/private/tmp`. No system toolchain setting was changed.
The executable SHA-256 is
`df4f5c0b7261977e009c9c4537f3b854641d362997cedc63da0e02ac03b93f03`.

The stable local preview archive is
`build/reimu-tier1-runtime-v1/灵梦桌宠预览.zip`, SHA-256
`3dc88e0da1eaeb7019e7624dfe7a503c79239b2f571d47f28360a8ed5a5287ef`.
A fresh `/private/tmp` extraction retained the executable digest and passed
strict deep signature verification. It reported Tiers 1/3/4/5 as one 125 ms
frame each, Tier2 as 16 frames, standing and slouch as 140 frames each, manual
eating as 40 frames, and reaction art as verified.

The current source snapshot passed:

- 198 Swift behavior checks;
- 37 native AppKit checks;
- 125 Consumer tool tests with the Harness CLI available and no skips;
- 14 observer/installer bridge tests and the browser runtime check;
- 31 synthetic status-contract cases;
- four isolated package/loading/fallback checks for each of Tiers 1–5;
- three reaction and five standing checks;
- the Consumer repository gate and `git diff --check`;
- the Tier1 production-without-preview negative gate.

The isolated runtime capture uses only
`runtime-preview/isolated-snapshot.json`, never the real provider state. It
covers animated Tier2 into Tier1 at its safe boundary, every Tier1–5 identity,
count nine capped to Tier5, immediate `needs_input` preemption, and recovery to
the latest count-four Tier4. Five Tier1 window captures are byte-identical.

## Native geometry and visual boundary

Tier1 uses the same full 596×596 canvas placement strategy as the approved
Tier3–5 stills. Native AppKit captures at 160 pt and 596 pt show no alpha
clipping. At 160 pt (measured from the 2× Retina capture, alpha greater than
1), Tier1's visible box is about 118×137.5 pt with 2.5 pt bottom support margin.
Its smaller height is the existing hunched-over source pose, not an added
rescale. Tier2 is about 150×156 pt, Tier3 about 120.5×147 pt, Tier4 about
117.5×148.5 pt, and Tier5 about 119.5×154.5 pt. The cross-tier footprint
changes are shown rather than hidden.

Review artifacts:

- `build/reimu-tier1-runtime-v1/runtime-preview/review-sheet.png`
- `build/reimu-tier1-runtime-v1/runtime-preview/runtime-review.gif`
- `build/reimu-tier1-runtime-v1/qa/native-size-review.png`
- `build/reimu-tier1-runtime-v1/qa/native-size-geometry.json`

Implementation, resource isolation, native integration, and technical gates
pass. The user's visual approval of Tier1 size, support, crop, static pose, and
cross-tier change remains pending. No application was installed, no real state
source was written, and no Tier1 commit, push, tag, or publication occurred.
