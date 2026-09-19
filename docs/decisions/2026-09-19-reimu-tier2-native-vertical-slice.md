# Reimu task_2 native vertical slice receipt

Date: 2026-09-19

This receipt records the local, uncommitted consumer integration that connects the
observer's real active-task count to the approved Reimu `task_2` exact-frame loop.
It is not an artwork approval, installation receipt, commit, push, tag, or release.

## Scope and invariant

- Consumer baseline: `d7394914fe2bffc5cec03d49c54d2d7285d56cd5`.
- Harness baseline: `7679b98ea34958115ed7456aac8a0589a01bdd21`, local
  `main` one commit ahead of `origin/main` before this task.
- Runtime selection: observed base `working` plus exact `activeTaskCount == 2`
  selects the explicit `work_eating_task_2` identity.
- Tier policy remains `min(activeTaskCount, 5)`. The animation never mutates work
  truth. Tiers 1, 3, 4, and 5 use named standing fallbacks; 5+ caps at tier 5.
- The packaged source remains `task_2-chew-v9`: 16 exact 596 px RGBA frames,
  10 fps, 1.6 seconds, looping, with frame 0 as the reduced-motion still.
  Source manifest SHA-256 is
  `81aa07c5503150f634a0b6e267f9621147f6f6a275e25b79b6c41e7ef1d447de`;
  base/frame endpoint SHA-256 is
  `0251947e0ca94f0ba0fa4b724d37fac242c86ba4de9591bb558c226ad4904cfe`.
- Ordinary tier changes commit at the current visual loop boundary. Leaving
  `working` and the existing failure, needs-input, click, drag, and pause paths
  preempt immediately. Return resolves the latest observed count.
- Missing or digest-mismatched tier-2 assets degrade that tier to standing
  without disabling the existing standing, manual eating, or reaction clips.
- No character art or approved source frame was created, redrawn, resampled, or
  modified. `idle_onigiri`, `drag_float`, `drag_land`, and tiers 1/3/4/5 remain open.

## Changed consumer source

- `desktop/macos/PetBehavior.swift`
- `desktop/macos/main.swift`
- `desktop/macos/build.py`
- `desktop/macos/test_behavior.swift`
- `desktop/macos/test_status.py`
- `desktop/macos/test_work_tier2.py`
- `desktop/README.md`
- `docs/reimu-action-system.md`
- `pets/reimu/metadata/actions.json`
- `scripts/check-repository.sh`
- `HANDOFF.md`

## Technical evidence

- Harness CLI: repository venv reports `0.8.0` and imports from that venv's
  `site-packages`.
- Consumer tool suite: 125 tests passed in 35.448 seconds. All nine Harness
  integration tests executed and none skipped: five animation-pipeline cases plus
  the idle, waiting, running, and review row end-to-end cases.
- Swift behavior model: 169 checks passed.
- Observer-to-native snapshot contract: 31 cases passed, including two concurrent
  active sessions producing count 2.
- Native asset checks: standing 5/5, reaction 3/3, task_2 package/fallback 4/4.
- Native AppKit self-test: 33/33 passed, including explicit task_2 identity,
  exact frame selection, reduced motion, safe fallback, timer/menu/window behavior.
- Consumer repository check passed with the bundled workspace Python placed first
  on `PATH`; its five v7 and five v9 importer checks passed. The first attempt with
  macOS `/usr/bin/python3` stopped before repository assertions because that
  interpreter has no Pillow module.
- App runtime checks passed; JSON parsing and `git diff --check` passed.
- Harness aggregate verification passed all nine gates; its pytest phase reports
  674 passed in 15.45 seconds. The receipt is
  `build/verification/20260919T124638.851303Z/report.json`. A sandboxed first run
  passed 673 tests and failed only because the sandbox denied the offline test's
  temporary `127.0.0.1` bind; the unchanged command passed with local-loopback
  permission and did not contact a real provider.

The independently built preview executable SHA-256 is
`5b6756ab798ee721f8afce060ef816a87a6e8b19287ca3cd19dc64dda04446ff`.
Its native loader reports 16 task_2 frames and no fallback. The isolated review
run's launch report selects artwork `workEatingTier2` and behavior
`work_eating_task_2`. Its behavior log records `working -> needs_input -> working`
with tier 2 reselected on the fresh entry.
The final review ZIP was created after removing only launch-added Finder extended
attributes and applying an ad-hoc signature. A fresh `/private/tmp` extraction passed
strict deep code-signature verification. The expanded Documents/FileProvider copy can
reacquire FinderInfo even without a new launch, so it is not the stable signature
artifact. The ZIP SHA-256 is
`24fef70880caaaf36fc3ca6252bf2000672fbf9f874ab3d1c747d40f09a09ec8`.

## Visual-review artifact

The local review-only outputs are under
`build/reimu-tier2-runtime-v1/runtime-preview/`:

- `runtime-review.gif` (320 x 348), SHA-256
  `31f94c64d9678b2b75a75608a2fb5613f7dcc341014ae764807b43707acb3577`;
- `review-sheet.png` (640 x 696), SHA-256
  `4b3ca545e9c414576d18ec6ae0eef26ab738e7c1a610aeb968441de26d5abdef`.

The preview uses an isolated local work snapshot and does not invoke a provider.
It demonstrates entry, continued looping, immediate needs-input preemption, and
fresh count-2 recovery. The user subsequently said the result was OK, approving the
current native tier-2 loop, scale, and demonstrated direct-switch behavior. This does
not approve transition artwork that does not yet exist.

The user also requested that transition animation remain explicit future work. A
separate backlog task covers entry from standing/fallback, exit from task_2, future
cross-tier changes, and recovery into the latest working tier. High-priority states
must continue to preempt immediately; a transition may never delay them or restore a
stale count. The approved direct-switch slice remains the baseline until that separate
task passes its own gates.

## Six gates

| Gate | Status | Boundary |
| --- | --- | --- |
| specification | ready | Tier policy, truth ownership, fallbacks, switching, preemption, and reduced motion are explicit. |
| implementation | ready | The tier-2-only native source path and tests are present in the uncommitted consumer tree. |
| technical | passed | The exact local commands above passed after selecting the documented Python runtime. |
| visual | approved | The user approved the current native tier-2 loop preview; future transition animation is a separate gated task. |
| consumer | verified | The consumer compiles, loads the exact package, and passes repository/runtime suites. |
| publication | unpublished | Nothing was committed, pushed, tagged, installed, or released in this task. |
