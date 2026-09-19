# Reimu Tier5 native static vertical slice

Date: 2026-09-20

## Scope and source boundary

The existing Eating Set v1 `task_5` drawing is connected to the native
Consumer as the explicit `work_eating_task_5` identity. It is selected only
when the observed state is `working` and the single
`PetBehavior.foodTier(activeTaskCount:)` policy maps the current count to Tier5.
That policy remains `min(max(count, 0), 5)`: exact count four still selects
Tier4, while five and higher counts select Tier5 without a second distributed
`>= 5` branch.

The source, runtime base, and only runtime frame are byte-identical 596×596
RGBA PNGs with SHA-256
`ffd3752c4cdf333a88dc70e766dc4fbdf584662bb242365b3a3ff8a2860f8342`.
No source pixel was regenerated, repainted, segmented, resized, or moved. The
package declares one 125 ms frame and remains an honest static hold. It is not
a completed eating animation, and the flattened character, table, food,
tatami, steam, sparkles, droplets, and hearts are never moved as a whole to
imitate motion.

## Runtime behavior

- A change from animated Tier2 to Tier5 waits for the current 1.6-second Tier2
  loop boundary.
- Tiers 3, 4, and 5 are static safe frames, so leaving them adds no artificial
  wait.
- Failure, needs-input, click, drag, pause, and every path that leaves
  `working` preserve immediate priority. Recovery re-evaluates the newest
  observed count rather than restoring a stale Tier5 presentation.
- Reduced motion selects the same Tier5 frame 0.
- Missing base/frame data, manifest identity changes, and manifest or frame
  digest mismatches degrade only Tier5 to the existing standing clip. Tiers 2,
  3, and 4, standing, manual feeding, reaction art, and slouch remain
  available.
- `desktop/macos/build.py --work-tier-5` requires `--preview`; production
  identity remains blocked until the user approves the native review.

## Native build and technical evidence

The independent preview is
`build/reimu-tier5-runtime-v1/灵梦桌宠预览.app`, version 1.12/build14,
bundle identifier `local.reimu.onigiri.preview`. It was freshly compiled from
the dirty, uncommitted Consumer worktree based on
`aa820f07a1352f5e9291548f08187e408aada5bd`, using
`SDKROOT=/Library/Developer/CommandLineTools/SDKs/MacOSX26.5.sdk` and isolated
module caches under `/private/tmp`. No system toolchain setting was changed.
The executable SHA-256 is
`31002218cb33c888586fa3bf9ddcf4f0511f87c4acfe4cdb0b3f6a61a6ac08b3`.

The stable local preview archive is
`build/reimu-tier5-runtime-v1/灵梦桌宠预览.zip`, SHA-256
`a7f9e9075506986850bb1ee13f28b477ef6b0275335731f2e39abd3f7167a1e7`.
A fresh `/private/tmp` extraction retained the executable digest, passed strict
deep signature verification, and reported Tier2 (16 frames), Tiers 3/4/5 (one
125 ms frame each), standing (140 frames), slouch (140 frames), manual eating
(40 frames), and reaction art as verified. The expanded workspace app may be
rewritten with Finder metadata after signing, so the ZIP extraction—not that
mutable copy—is the signature-verified review package.

The current source snapshot passed:

- 190 Swift behavior checks;
- 36 native AppKit checks;
- 125 Consumer tool tests with the Harness CLI available and no skips;
- 14 observer/installer bridge tests and the browser runtime check;
- 31 synthetic status-contract cases;
- four isolated package/loading/fallback checks for each of Tiers 2, 3, 4,
  and 5;
- three reaction and five standing checks;
- the Consumer repository gate and `git diff --check`;
- the Tier5 production-without-preview negative gate.

The isolated runtime capture uses only
`runtime-preview/isolated-snapshot.json`, never the real provider state. It
covers Tiers 2, 3, and 4, exact count five, count nine capped to Tier5,
immediate `needs_input` preemption, and recovery to the latest count-four Tier4.
Five Tier5 window captures are byte-identical.

## Native geometry and visual boundary

Tier5 uses the same full 596×596 canvas placement strategy as the approved
Tier3 and Tier4 stills. Native AppKit captures at 160 pt and 596 pt show no
alpha clipping. At 160 pt (measured from the 2× Retina capture, alpha greater
than 1), Tier5's visible box is about 119.5×154.5 pt with 2.5 pt bottom support
margin. Tier4 is about 117.5×148.5 pt, Tier3 about 120.5×147 pt, both with the
same 2.5 pt margin. Tier2 remains wider at about 150×156 pt with a 2 pt margin;
the existing cross-tier footprint change is shown rather than hidden by
rescaling the artwork.

Review artifacts:

- `build/reimu-tier5-runtime-v1/runtime-preview/review-sheet.png`
- `build/reimu-tier5-runtime-v1/runtime-preview/runtime-review.gif`
- `build/reimu-tier5-runtime-v1/qa/native-size-review.png`
- `build/reimu-tier5-runtime-v1/qa/native-size-geometry.json`

Implementation, resource isolation, native integration, and technical gates
pass. The user's visual approval of Tier5 size, support, crop, static pose, and
cross-tier change remains pending. No application was installed, no real state
source was written, and no Tier5 commit, push, tag, or publication occurred.
