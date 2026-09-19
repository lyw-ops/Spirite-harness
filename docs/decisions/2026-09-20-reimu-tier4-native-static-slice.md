# Reimu Tier 4 native static vertical slice

Date: 2026-09-20

## Scope and source boundary

The existing Eating Set v1 `task_4` drawing is now connected to the native
consumer as the explicit `work_eating_task_4` identity. It is selected only
when the observed state is `working` and `activeTaskCount == 4`. The single
`PetBehavior.foodTier(activeTaskCount:)` policy remains the only count-to-tier
mapping and still caps five or more tasks at Tier 5, so a count of five or more
cannot select Tier 4.

The source, runtime base, and only runtime frame are byte-identical 596×596
RGBA PNGs with SHA-256
`9f0b18946eca4c7c0d27a8dbbd5f966da615867913d8e91c8454dd629de0b238`.
No source pixel was regenerated, repainted, segmented, resized, or moved. The
package declares one 125 ms frame and remains an honest static hold. It is not
a completed ramen-eating animation, and the flattened character, table, food,
tatami, steam, and heart marks are never moved as a whole to imitate motion.

## Runtime behavior

- A change from animated Tier 2 to Tier 4 waits for the current 1.6-second
  Tier 2 loop boundary.
- Tier 3 and Tier 4 are static safe frames, so leaving either still adds no
  artificial wait.
- Leaving `working`, failure, needs-input, click, drag, and pause paths keep
  their existing immediate priority. Recovery re-evaluates the newest observed
  count rather than restoring a stale Tier 4 presentation.
- Reduced motion selects the same Tier 4 frame 0.
- Missing base/frame data, manifest identity changes, and manifest or frame
  digest mismatches degrade only Tier 4 to the existing standing clip. Tier 2,
  Tier 3, standing, manual feeding, reaction art, and slouch remain available.
- `desktop/macos/build.py --work-tier-4` requires `--preview`; production
  identity remains blocked until the user approves the native review.

## Native build and technical evidence

The independent preview is
`build/reimu-tier4-runtime-v1/灵梦桌宠预览.app`, version 1.11/build 13,
bundle identifier `local.reimu.onigiri.preview`. It was freshly compiled from
the dirty, uncommitted Consumer worktree based on
`6a1318257d9bedc2b9a937304ea4b434ca874409`, using
`SDKROOT=/Library/Developer/CommandLineTools/SDKs/MacOSX26.5.sdk` and isolated
module caches under `/private/tmp`. No system toolchain setting was changed.
The executable SHA-256 is
`fa81b7d6dda788a9ce0ee5deb265f10fff8c1ad918953f087e8036b9fbae4bb9`.

The stable local preview archive is
`build/reimu-tier4-runtime-v1/灵梦桌宠预览.zip`, SHA-256
`50ec909dd58aa4801db388d646a4b3c767631ccc96283a2375dfeb7b87570ad4`.
A fresh `/private/tmp` extraction retained the executable digest, passed strict
deep signature verification, and reported Tier 2 (16 frames), Tier 3 (one
125 ms frame), Tier 4 (one 125 ms frame), standing (140 frames), slouch (140
frames), manual eating (40 frames), and reaction art as verified.

The current source snapshot passed:

- 181 Swift behavior checks;
- 35 native AppKit checks;
- 125 Consumer tool tests with the Harness CLI available and no skips;
- 14 observer/installer bridge tests and the browser runtime check;
- 31 synthetic status-contract cases;
- four isolated package/loading/fallback checks for each of Tier 2, Tier 3,
  and Tier 4;
- three reaction and five standing checks;
- the Consumer repository gate and `git diff --check`;
- the Tier 4 production-without-preview negative gate.

The isolated runtime capture uses only
`runtime-preview/isolated-snapshot.json`, never the real provider state. It
covers Tier 2, Tier 3, Tier 4, immediate `needs_input` preemption, and recovery
to the latest count-two Tier 2. Five Tier 4 window captures are byte-identical.

## Native geometry and visual boundary

Tier 4 uses the same full 596×596 canvas placement strategy as the approved
Tier 3 still. Native AppKit captures at 160 pt and 596 pt show no alpha clipping.
At 160 pt (measured from the 2× Retina capture, alpha greater than 1), Tier 4's
visible box is about 117.5×148.5 pt with 2.5 pt bottom support margin. Tier 3 is
about 120.5×147 pt with the same 2.5 pt margin. Tier 2 is visibly wider at about
150×156 pt with a 2 pt margin; this existing cross-tier footprint change is
shown rather than hidden by rescaling the artwork.

Review artifacts:

- `build/reimu-tier4-runtime-v1/runtime-preview/review-sheet.png`
- `build/reimu-tier4-runtime-v1/runtime-preview/runtime-review.gif`
- `build/reimu-tier4-runtime-v1/qa/native-size-review.png`
- `build/reimu-tier4-runtime-v1/qa/native-size-geometry.json`

Implementation, resource isolation, native integration, and technical gates
pass. The user's visual approval of Tier 4 size, support, crop, static pose, and
cross-tier change remains pending. No application was installed, no real state
source was written, and no commit, push, tag, or publication occurred.
