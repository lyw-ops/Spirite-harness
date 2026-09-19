# Reimu task_3 native static vertical slice receipt

Date: 2026-09-19

This receipt records the local, uncommitted consumer integration that connects the
observer's real active-task count three to the existing Reimu `task_3` Eating Set
drawing. It is not a multi-frame animation claim, visual approval, installation,
commit, push, tag, or release.

## Scope and invariant

- Consumer baseline: `d7394914fe2bffc5cec03d49c54d2d7285d56cd5`, with the
  previously verified tier-2 work still uncommitted.
- Harness baseline: `7679b98ea34958115ed7456aac8a0589a01bdd21`, with the
  tier-2 ledger receipt already present as uncommitted work.
- Runtime selection: observed base `working` plus exact `activeTaskCount == 3`
  selects the explicit `work_eating_task_3` identity.
- The source is the pre-existing Eating Set v1 `task_3` 596 px RGBA image,
  SHA-256 `45c212c88bd39053bb351d5f7bdf8da5d1a95ca743c532232290288927a2a9ff`.
  `base.png` and `frames/frame_000.png` are byte-identical to that source.
- Source manifest SHA-256 is
  `eb8a226ae8936205e69044bd146aa4a7a89fb6702d1fe7daf5c16e7c322528d2`.
  It declares one 125 ms frame at 8 fps, looping only as a static hold.
- No character pixels were generated, repainted, segmented, resampled, or moved.
  In particular, the flattened table and tatami are not translated to manufacture
  motion. A real tier-3 loop still requires reviewed exact frames or explicit layers.
- Tier 2 to tier 3 waits for the current 1.6 second chew-loop boundary. Tier 3 is
  itself a safe still, so leaving it does not impose a made-up seven-second boundary.
- Failure, needs-input, click, drag, pause, and system gates continue to preempt
  immediately. Recovery uses the latest observed count.
- Missing or digest-mismatched tier-3 assets degrade only tier 3 to standing. Tier 2,
  standing, manual eating, and slouch remain available.
- Native production packaging is fail-closed: `build.py --work-tier-3` requires
  `--preview` until visual approval is recorded.

## Changed consumer source

- `desktop/macos/PetBehavior.swift`
- `desktop/macos/main.swift`
- `desktop/macos/build.py`
- `desktop/macos/test_behavior.swift`
- `desktop/macos/test_work_tier3.py`
- `desktop/README.md`
- `docs/reimu-action-system.md`
- `pets/reimu/metadata/actions.json`
- `pets/reimu/animations/eating/sources/task_3-static-v1/`
- `scripts/check-repository.sh`
- `HANDOFF.md`

## Technical evidence

- 172 Swift behavior checks passed, including tier-3 selection, static semantics,
  isolated fallback, tier-2 boundary entry, immediate exit from the tier-3 still,
  and latest-count recovery.
- The full 125-test consumer tool suite passed with Harness 0.8.0 and Node 20.20.2.
- Four task-2 and four task-3 native package/fallback checks passed.
- Fourteen observer/installer bridge tests, 31 status cases, three reaction checks,
  five standing checks, the repository gate, JSON parsing, and `git diff --check`
  passed on the synchronized consumer tree.
- Native AppKit self-test passed 34 checks, including both workload identities,
  resource loading, static/reduced-motion behavior, exact frame selection, timer,
  menu, window, placement, hit testing, logging, and existing slouch/meal paths.
- The isolated launch report selected artwork `workEatingTier3` and behavior
  `work_eating_task_3`. Eight native tier-3 window captures were byte-identical.
  The behavior log then recorded immediate `needs_input` preemption and a fresh
  count-two recovery to tier 2.
- Harness aggregate verification passed all nine local gates with 674 pytest cases;
  the current coherent-snapshot receipt is indexed by
  `build/verification/latest.json`. A sandboxed first run
  passed 673 cases and failed only because the sandbox denied the offline test's
  temporary `127.0.0.1` bind; the unchanged command passed with local-loopback
  permission and contacted no real provider.

The preview is 1.10/build 12. Executable SHA-256 is
`079cf2f5036cd23f7cee0412a0ce8c65f70beca0c5633de32b513df388ad0abb`.
The stable review ZIP SHA-256 is
`89b10b66227efa9a069180cf672333cdba362bf13f3ab3862850a46928a63dbf`;
a fresh `/private/tmp` extraction passed strict deep code-signature verification.

## Visual-review artifact

Review-only outputs are under `build/reimu-tier3-runtime-v1/runtime-preview/`:

- `runtime-review.gif`, SHA-256
  `557d7c6f083aec19b7a57c6d70408e17c17861f22ecfabebc74300b3b95fa180`;
- `review-sheet.png`, SHA-256
  `c1855b8766046178b81bef62cb490a38fe4022a6b438a2c81667d6e79c159c7a`.

The sheet shows count-three entry, an unchanged static hold, immediate
`needs_input` preemption, and recovery to the latest count-two tier. The artifact uses
an isolated local snapshot and never contacts a real provider. Technical inspection
found no clipping, scale jump, source drift, or unintended animation. Human approval
of the native tier-3 size and pose remains pending.

## Six gates

| Gate | Status | Boundary |
| --- | --- | --- |
| specification | ready | Count-three identity, immutable source, static semantics, switching, preemption, reduced motion, and fallback are explicit. |
| implementation | ready | The consumer contains the exact package, loader, selector, preview-only build gate, and regression tests. |
| technical | passed | Consumer, AppKit, package, repository, and isolated runtime checks passed. |
| visual | in review | The native review sheet and GIF exist; user approval has not yet been recorded. |
| consumer | verified | The synchronized consumer tree selects tier 3 only for working plus count three and degrades it independently. |
| publication | unpublished | Nothing was installed, committed, pushed, tagged, or released. |
