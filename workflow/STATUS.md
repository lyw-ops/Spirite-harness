# Sprite Harness task status

> Generated from `workflow/tasks.json`; do not edit by hand.

Ledger date: **2026-11-10**.

A gate records one claim only. In particular, `technical: passed` never supplies visual, consumer, installation, or publication evidence.

| Task | Kind | Derived stage | Required gates | Dependencies |
| --- | --- | --- | --- | --- |
| `HARNESS-KEYFRAMES-001` · Release keyframe tracks and the discrete pulse curve | core-capability | **complete** | specification, implementation, technical, consumer, publication | — |
| `HARNESS-WORKFLOW-001` · Adopt the evidence-bound Sprite Harness workflow | infrastructure | **complete** | specification, implementation, technical, publication | — |
| `REIMU-ACTIONS-001` · Produce the six-tier work-eating, idle onigiri, and grabbed-drag action set | animation-delivery | **implementation** | specification, implementation, technical, visual, consumer, publication | `HARNESS-KEYFRAMES-001` |
| `REIMU-SCENE-REACTIONS-001` · Scene-aware click reactions, Reimu-voiced lines, and plain standing idle | consumer-vertical-slice | **visual review** | specification, implementation, technical, visual, consumer, publication | `REIMU-TIER-EMOTE-LOOPS-RUNTIME-001` |
| `REIMU-TIER-EMOTE-LOOPS-INTAKE-001` · Prepare emote-layer life loops for the static Tier1/3/4/5 stills | animation-delivery | **complete** | specification, implementation, technical, visual | `REIMU-TIER1-INTAKE-001`, `REIMU-TIER4-INTAKE-001`, `REIMU-TIER5-INTAKE-001`, `REIMU-TIER3-RUNTIME-001` |
| `REIMU-TIER-EMOTE-LOOPS-RUNTIME-001` · Play the Tier1/3/4/5 emote loops in the native pet | consumer-vertical-slice | **complete** | specification, implementation, technical, visual, consumer, publication | `REIMU-TIER-EMOTE-LOOPS-INTAKE-001`, `REIMU-TIER1-RUNTIME-001` |
| `REIMU-TIER-FACE-LOOPS-INTAKE-001` · Prepare face-motion candidates for the Tier3/4/5 loops | animation-delivery | **complete** | specification, implementation, technical, visual | `REIMU-TIER-EMOTE-LOOPS-INTAKE-001` |
| `REIMU-TIER-FACE-LOOPS-RUNTIME-001` · Play the Tier3/4/5 face loops in the native pet | consumer-vertical-slice | **complete** | specification, implementation, technical, visual, consumer, publication | `REIMU-TIER-FACE-LOOPS-INTAKE-001`, `REIMU-TIER-EMOTE-LOOPS-RUNTIME-001` |
| `REIMU-TIER1-INTAKE-001` · Prepare and review the existing Tier1 onigiri still | animation-delivery | **complete** | specification, implementation, technical, visual | — |
| `REIMU-TIER1-RUNTIME-001` · Connect observed count one to the existing native Tier1 still | consumer-vertical-slice | **complete** | specification, implementation, technical, visual, consumer, publication | `REIMU-TIER5-RUNTIME-001`, `REIMU-TIER1-INTAKE-001` |
| `REIMU-TIER2-RUNTIME-001` · Connect observed count two to the approved native task_2 loop | consumer-vertical-slice | **complete** | specification, implementation, technical, visual, consumer, publication | `REIMU-ACTIONS-001` |
| `REIMU-TIER3-RUNTIME-001` · Connect observed count three to the existing native task_3 still | consumer-vertical-slice | **complete** | specification, implementation, technical, visual, consumer, publication | `REIMU-TIER2-RUNTIME-001` |
| `REIMU-TIER4-INTAKE-001` · Prepare and review the existing Tier4 ramen still | animation-delivery | **complete** | specification, implementation, technical, visual | — |
| `REIMU-TIER4-RUNTIME-001` · Connect observed count four to the existing native Tier4 still | consumer-vertical-slice | **complete** | specification, implementation, technical, visual, consumer, publication | `REIMU-TIER3-RUNTIME-001`, `REIMU-TIER4-INTAKE-001` |
| `REIMU-TIER5-INTAKE-001` · Prepare and review the existing Tier5 meal still | animation-delivery | **complete** | specification, implementation, technical, visual | — |
| `REIMU-TIER5-RUNTIME-001` · Connect five or more observed tasks to the existing native Tier5 still | consumer-vertical-slice | **complete** | specification, implementation, technical, visual, consumer, publication | `REIMU-TIER4-RUNTIME-001`, `REIMU-TIER5-INTAKE-001` |
| `REIMU-WORK-TRANSITIONS-001` · Author transitions around native workload eating | animation-delivery | **implementation** | specification, implementation, technical, visual, consumer, publication | `REIMU-TIER2-RUNTIME-001`, `REIMU-TIER3-RUNTIME-001`, `REIMU-TIER4-RUNTIME-001`, `REIMU-TIER5-RUNTIME-001`, `REIMU-TIER1-RUNTIME-001` |

<a id="harness-keyframes-001"></a>
## `HARNESS-KEYFRAMES-001` · Release keyframe tracks and the discrete pulse curve

Derived stage: **complete**.

| Gate | Required | Status | Evidence | Boundary note |
| --- | --- | --- | --- | --- |
| specification | yes | `ready` | [animation-plan.md](../docs/animation-plan.md), [animation-plan.schema.json](../schemas/animation-plan.schema.json) | Keyframe and pulse semantics are described in the current working tree. |
| implementation | yes | `ready` | [curves.py](../src/sprite_harness/curves.py), [expand.py](../src/sprite_harness/expand.py), [test_plan.py](../tests/test_plan.py) | The keyframe and pulse implementation is published in the exact Harness commit named by the publication gate. |
| technical | yes | `passed` | [2026-09-19-0.8.0-workflow-closure.md](../docs/decisions/2026-09-19-0.8.0-workflow-closure.md) | Current-version M3 and M4/M5 acceptance plus the aggregate Harness verification passed. |
| visual | no | `not_required` | — | The generic core feature has no character-art approval gate. |
| consumer | yes | `verified` | [2026-09-19-0.8.0-workflow-closure.md](../docs/decisions/2026-09-19-0.8.0-workflow-closure.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/tree/d7394914fe2bffc5cec03d49c54d2d7285d56cd5) | All 125 consumer tests passed with the 0.8.0 CLI explicitly pinned; no Harness integration test was skipped. |
| publication | yes | `published` | [remote](https://github.com/lyw-ops/Spirite-harness/commit/7679b98ea34958115ed7456aac8a0589a01bdd21) | The maintainer-authorized push was verified at origin/main; no tag or package release is implied. |

<a id="harness-workflow-001"></a>
## `HARNESS-WORKFLOW-001` · Adopt the evidence-bound Sprite Harness workflow

Derived stage: **complete**.

| Gate | Required | Status | Evidence | Boundary note |
| --- | --- | --- | --- | --- |
| specification | yes | `ready` | [workflow.md](../docs/workflow.md), [HARNESS.md](../HARNESS.md) | The canonical lifecycle, evidence boundaries, and publication protocol are documented. |
| implementation | yes | `ready` | [update.py](../workflow/update.py), [verify.py](../scripts/verify.py), [test_workflow.py](../tests/test_workflow.py) | The task ledger, generated views, aggregate verifier, and regression tests exist. |
| technical | yes | `passed` | [2026-09-19-0.8.0-workflow-closure.md](../docs/decisions/2026-09-19-0.8.0-workflow-closure.md) | The aggregate workflow, pytest, compile, diff, and layered CLI smoke gates passed on the closure source. |
| visual | no | `not_required` | — | Workflow infrastructure has no artwork approval gate. |
| consumer | no | `not_required` | — | This infrastructure does not itself change a consumer runtime. |
| publication | yes | `published` | [remote](https://github.com/lyw-ops/Spirite-harness/commit/7679b98ea34958115ed7456aac8a0589a01bdd21) | The maintainer authorized publication; origin/main was independently verified at the exact workflow commit. |

<a id="reimu-actions-001"></a>
## `REIMU-ACTIONS-001` · Produce the six-tier work-eating, idle onigiri, and grabbed-drag action set

Derived stage: **implementation**.

| Gate | Required | Status | Evidence | Boundary note |
| --- | --- | --- | --- | --- |
| specification | yes | `ready` | [remote](https://github.com/lyw-ops/gensokyo-codex-pets/blob/d7394914fe2bffc5cec03d49c54d2d7285d56cd5/docs/reimu-action-system.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/blob/d7394914fe2bffc5cec03d49c54d2d7285d56cd5/pets/reimu/metadata/actions.json) | The behavior contract is pinned to the published consumer commit instead of an ambiguous moving branch. |
| implementation | yes | `in_progress` | — | Existing task_2 work is partial coverage; the six tiers and independent grabbed pose are not a finished set. |
| technical | yes | `pending` | — | Each authored set needs deterministic plan/render/validate and reduced-motion evidence. |
| visual | yes | `pending` | — | Technical QA cannot approve expression, silhouette, scale, timing, or transition quality. |
| consumer | yes | `pending` | — | Native runtime state selection, interruption, landing, and tier switching remain separately verifiable. |
| publication | yes | `unpublished` | — | The design commit is published; the complete action delivery is not. |

<a id="reimu-scene-reactions-001"></a>
## `REIMU-SCENE-REACTIONS-001` · Scene-aware click reactions, Reimu-voiced lines, and plain standing idle

Derived stage: **visual review**.

| Gate | Required | Status | Evidence | Boundary note |
| --- | --- | --- | --- | --- |
| specification | yes | `ready` | [2026-11-10-reimu-scene-reactions-and-idle.md](../docs/decisions/2026-11-10-reimu-scene-reactions-and-idle.md) | Reaction words follow the scene on screen; light clicks never cut away from a work meal; idle only stands unless the user opts back in. |
| implementation | yes | `ready` | [2026-11-10-reimu-scene-reactions-and-idle.md](../docs/decisions/2026-11-10-reimu-scene-reactions-and-idle.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/2c62a77067d53746824946eeeb4c6c8ff2522175) | PetScene, PetLines, held work artwork during light reactions, idleAutonomy and its menu toggle exist in the published Consumer commit. |
| technical | yes | `passed` | [2026-11-10-reimu-scene-reactions-and-idle.md](../docs/decisions/2026-11-10-reimu-scene-reactions-and-idle.md) | 217 behavior, 37 native AppKit, 31 status, per-tier loader and fallback checks and strict signatures passed on the 1.16/build 18 bundle. |
| visual | yes | `in_review` | [2026-11-10-reimu-scene-reactions-and-idle.md](../docs/decisions/2026-11-10-reimu-scene-reactions-and-idle.md) | The lines and the idle change were installed on the user's request without a line-by-line review. |
| consumer | yes | `verified` | [2026-11-10-reimu-scene-reactions-and-idle.md](../docs/decisions/2026-11-10-reimu-scene-reactions-and-idle.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/2c62a77067d53746824946eeeb4c6c8ff2522175) | Installed 1.16 runs with the new reactions; idle autonomy is off by default in the production identity. |
| publication | yes | `published` | [2026-11-10-reimu-scene-reactions-and-idle.md](../docs/decisions/2026-11-10-reimu-scene-reactions-and-idle.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/2c62a77067d53746824946eeeb4c6c8ff2522175) | The maintainer asked to commit and push on 2026-11-10; the exact Consumer commit was verified on origin/main. No tag or package release is implied. |

<a id="reimu-tier-emote-loops-intake-001"></a>
## `REIMU-TIER-EMOTE-LOOPS-INTAKE-001` · Prepare emote-layer life loops for the static Tier1/3/4/5 stills

Derived stage: **complete**.

| Gate | Required | Status | Evidence | Boundary note |
| --- | --- | --- | --- | --- |
| specification | yes | `ready` | [2026-11-10-reimu-tier-emote-loops-intake.md](../docs/decisions/2026-11-10-reimu-tier-emote-loops-intake.md) | Lossless split of each approved still into detached alpha components; only emote symbols move; frame 0 and reduced motion must equal the approved still. |
| implementation | yes | `ready` | [2026-11-10-reimu-tier-emote-loops-intake.md](../docs/decisions/2026-11-10-reimu-tier-emote-loops-intake.md) | Layer sources, plans, full and reduced builds, pixel gates, and review exports exist under build/reimu-tier-emote-loops-v1. |
| technical | yes | `passed` | [2026-11-10-reimu-tier-emote-loops-intake.md](../docs/decisions/2026-11-10-reimu-tier-emote-loops-intake.md) | All eight public CLI builds validate; frame 0 and every reduced frame equal the approved still; no changed pixel lies outside the emote regions. Tier1 motion is weak at 160 px. |
| visual | yes | `approved` | [2026-11-10-reimu-tier-emote-loops-intake.md](../docs/decisions/2026-11-10-reimu-tier-emote-loops-intake.md), [2026-11-10-reimu-tier-emote-loops-runtime.md](../docs/decisions/2026-11-10-reimu-tier-emote-loops-runtime.md) | The user reviewed the v1 GIFs and replied "可以，接入" on 2026-11-10. Approval covers the symbol motion shown; it is not an eating animation. |
| consumer | no | `not_required` | [2026-11-10-reimu-tier-emote-loops-intake.md](../docs/decisions/2026-11-10-reimu-tier-emote-loops-intake.md) | Intake only; native integration needs a separate runtime task after visual approval. |
| publication | no | `not_required` | [2026-11-10-reimu-tier-emote-loops-intake.md](../docs/decisions/2026-11-10-reimu-tier-emote-loops-intake.md) | Local review candidate; no publication requested. |

<a id="reimu-tier-emote-loops-runtime-001"></a>
## `REIMU-TIER-EMOTE-LOOPS-RUNTIME-001` · Play the Tier1/3/4/5 emote loops in the native pet

Derived stage: **complete**.

| Gate | Required | Status | Evidence | Boundary note |
| --- | --- | --- | --- | --- |
| specification | yes | `ready` | [2026-11-10-reimu-tier-emote-loops-runtime.md](../docs/decisions/2026-11-10-reimu-tier-emote-loops-runtime.md) | 24-frame 10 fps loops whose first and last frames are the approved still; tier switching, preemption, reduced motion and isolated fallback are unchanged. |
| implementation | yes | `ready` | [2026-11-10-reimu-tier-emote-loops-runtime.md](../docs/decisions/2026-11-10-reimu-tier-emote-loops-runtime.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/0c814aa95ec464bbadef6a2c3344b9724b73b302) | The published Consumer commit contains the four exact-frame packages, builder pins, clip specs, frame selection, tests, and repository gate. |
| technical | yes | `passed` | [2026-11-10-reimu-tier-emote-loops-runtime.md](../docs/decisions/2026-11-10-reimu-tier-emote-loops-runtime.md) | Fresh 1.14/build 16 compilation, 198 behavior, 37 native AppKit, 31 status, per-tier loader and fallback checks, repository gate and strict signatures passed. |
| visual | yes | `approved` | [2026-11-10-reimu-tier-emote-loops-runtime.md](../docs/decisions/2026-11-10-reimu-tier-emote-loops-runtime.md), [2026-11-10-reimu-scene-reactions-and-idle.md](../docs/decisions/2026-11-10-reimu-scene-reactions-and-idle.md) | The user replied "v2可以" on 2026-11-10 after the re-timed v2 loops were installed as 1.14/build 16 and the v2 review GIF was shown. Approval covers symbol motion only. |
| consumer | yes | `verified` | [2026-11-10-reimu-tier-emote-loops-runtime.md](../docs/decisions/2026-11-10-reimu-tier-emote-loops-runtime.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/0c814aa95ec464bbadef6a2c3344b9724b73b302) | The installed 1.14 loads all four loops, selects loop frames while working, holds frame 0 under reduced motion, and degrades a damaged package to standing on its own. |
| publication | yes | `published` | [2026-11-10-reimu-tier-emote-loops-runtime.md](../docs/decisions/2026-11-10-reimu-tier-emote-loops-runtime.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/0c814aa95ec464bbadef6a2c3344b9724b73b302) | The maintainer asked to commit and push on 2026-11-10; the exact Consumer commit was verified on origin/main. No tag or package release is implied. |

<a id="reimu-tier-face-loops-intake-001"></a>
## `REIMU-TIER-FACE-LOOPS-INTAKE-001` · Prepare face-motion candidates for the Tier3/4/5 loops

Derived stage: **complete**.

| Gate | Required | Status | Evidence | Boundary note |
| --- | --- | --- | --- | --- |
| specification | yes | `ready` | [2026-11-10-reimu-tier-face-loops-intake.md](../docs/decisions/2026-11-10-reimu-tier-face-loops-intake.md) | Local continuous warps of approved pixels inside measured boxes; rest frames and reduced motion equal the approved still. |
| implementation | yes | `ready` | [2026-11-10-reimu-tier-face-loops-intake.md](../docs/decisions/2026-11-10-reimu-tier-face-loops-intake.md) | Candidates exist for Tier3 chew, Tier4 noodle sway and Tier5 laugh under build/reimu-tier-face-loops-v1; the Tier1 blink was rejected and removed. |
| technical | yes | `passed` | [2026-11-10-reimu-tier-face-loops-intake.md](../docs/decisions/2026-11-10-reimu-tier-face-loops-intake.md) | All eight public CLI builds validate and every change stays inside the emote and face regions. The motion is faint at 160 px and Tier5 has residual edge artifacts. |
| visual | yes | `approved` | [2026-11-10-reimu-tier-face-loops-intake.md](../docs/decisions/2026-11-10-reimu-tier-face-loops-intake.md), [2026-11-10-reimu-tier-face-loops-runtime.md](../docs/decisions/2026-11-10-reimu-tier-face-loops-runtime.md) | The user reviewed the GIFs and zoomed pose sheet and replied "接入这三个" on 2026-11-10 for Tier3, Tier4 and Tier5. The rejected Tier1 blink is not part of the approval. |
| consumer | no | `not_required` | [2026-11-10-reimu-tier-face-loops-intake.md](../docs/decisions/2026-11-10-reimu-tier-face-loops-intake.md) | Intake only. |
| publication | no | `not_required` | [2026-11-10-reimu-tier-face-loops-intake.md](../docs/decisions/2026-11-10-reimu-tier-face-loops-intake.md) | Local review candidate. |

<a id="reimu-tier-face-loops-runtime-001"></a>
## `REIMU-TIER-FACE-LOOPS-RUNTIME-001` · Play the Tier3/4/5 face loops in the native pet

Derived stage: **complete**.

| Gate | Required | Status | Evidence | Boundary note |
| --- | --- | --- | --- | --- |
| specification | yes | `ready` | [2026-11-10-reimu-tier-face-loops-runtime.md](../docs/decisions/2026-11-10-reimu-tier-face-loops-runtime.md) | Same 24-frame 10 fps contract as the emote loops; first and last frames are the approved still; Tier1 keeps its emote loop. |
| implementation | yes | `ready` | [2026-11-10-reimu-tier-face-loops-runtime.md](../docs/decisions/2026-11-10-reimu-tier-face-loops-runtime.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/2c62a77067d53746824946eeeb4c6c8ff2522175) | Three exact-frame packages, builder pins and the repository gate exist in the published Consumer commit. |
| technical | yes | `passed` | [2026-11-10-reimu-tier-face-loops-runtime.md](../docs/decisions/2026-11-10-reimu-tier-face-loops-runtime.md) | Fresh 1.17/build 19 compilation, 217 behavior, 37 native AppKit, 31 status, per-tier loader and fallback checks, repository gate and strict signatures passed. |
| visual | yes | `approved` | [2026-11-10-reimu-tier-face-loops-intake.md](../docs/decisions/2026-11-10-reimu-tier-face-loops-intake.md), [2026-11-10-reimu-tier-face-loops-runtime.md](../docs/decisions/2026-11-10-reimu-tier-face-loops-runtime.md) | The integrated frames are exactly the reviewed candidates; native placement of these tiers was approved on 2026-09-20. The user had reduced motion switched on at install time, so on-screen playback was not observed. |
| consumer | yes | `verified` | [2026-11-10-reimu-tier-face-loops-runtime.md](../docs/decisions/2026-11-10-reimu-tier-face-loops-runtime.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/2c62a77067d53746824946eeeb4c6c8ff2522175) | The installed 1.17 loads all three face loops and keeps the per-tier isolated fallback. |
| publication | yes | `published` | [2026-11-10-reimu-tier-face-loops-runtime.md](../docs/decisions/2026-11-10-reimu-tier-face-loops-runtime.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/2c62a77067d53746824946eeeb4c6c8ff2522175) | The maintainer asked to commit and push on 2026-11-10; the exact Consumer commit was verified on origin/main. No tag or package release is implied. |

<a id="reimu-tier1-intake-001"></a>
## `REIMU-TIER1-INTAKE-001` · Prepare and review the existing Tier1 onigiri still

Derived stage: **complete**.

| Gate | Required | Status | Evidence | Boundary note |
| --- | --- | --- | --- | --- |
| specification | yes | `ready` | [2026-09-20-reimu-tier1-static-intake.md](../docs/decisions/2026-09-20-reimu-tier1-static-intake.md) | Exact count one; immutable existing onigiri source; one-frame static hold. |
| implementation | yes | `ready` | [2026-09-20-reimu-tier1-static-intake.md](../docs/decisions/2026-09-20-reimu-tier1-static-intake.md) | Pinned source, plan, normal and reduced builds, previews, and intake report exist under build/reimu-tier1-intake-20260920. |
| technical | yes | `passed` | [2026-09-20-reimu-tier1-static-intake.md](../docs/decisions/2026-09-20-reimu-tier1-static-intake.md) | Both public CLI pipelines pass with expected ZERO_MOTION; decoded pixels equal the source in normal and reduced motion; the original digest is unchanged. |
| visual | yes | `approved` | [2026-09-20-reimu-tier1-static-intake.md](../docs/decisions/2026-09-20-reimu-tier1-static-intake.md), [2026-09-20-reimu-tier1-native-static-slice.md](../docs/decisions/2026-09-20-reimu-tier1-native-static-slice.md), [2026-09-20-reimu-tier1-visual-approval.md](../docs/decisions/2026-09-20-reimu-tier1-visual-approval.md) | The user approved the reviewed Tier1 source and native presentation on 2026-09-20; the one-frame source remains a static hold, not a completed animation. |
| consumer | no | `not_required` | [2026-09-20-reimu-tier1-static-intake.md](../docs/decisions/2026-09-20-reimu-tier1-static-intake.md) | This task covers artwork intake only; native integration is tracked separately by REIMU-TIER1-RUNTIME-001. |
| publication | no | `not_required` | [2026-09-20-reimu-tier1-static-intake.md](../docs/decisions/2026-09-20-reimu-tier1-static-intake.md) | Local review candidate; no publication requested. |

<a id="reimu-tier1-runtime-001"></a>
## `REIMU-TIER1-RUNTIME-001` · Connect observed count one to the existing native Tier1 still

Derived stage: **complete**.

| Gate | Required | Status | Evidence | Boundary note |
| --- | --- | --- | --- | --- |
| specification | yes | `ready` | [2026-09-20-reimu-tier1-native-static-slice.md](../docs/decisions/2026-09-20-reimu-tier1-native-static-slice.md), [2026-09-20-reimu-tier1-visual-approval.md](../docs/decisions/2026-09-20-reimu-tier1-visual-approval.md) | Exact count one through the single tier policy, immutable one-frame source, safe-boundary switching, immediate preemption, latest-count recovery, reduced motion, isolated fallback, and visual approval boundary are explicit. |
| implementation | yes | `ready` | [2026-09-20-reimu-tier1-native-static-slice.md](../docs/decisions/2026-09-20-reimu-tier1-native-static-slice.md), [2026-09-20-reimu-tier1-visual-approval.md](../docs/decisions/2026-09-20-reimu-tier1-visual-approval.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/c2684cc3fecbdfbe0ae238a13f8e22fef333295d) | The published Consumer commit contains the independent resource package, native identity, loader, selector, targeted tests, and the visually approved production-eligible build gate. |
| technical | yes | `passed` | [2026-09-20-reimu-tier1-native-static-slice.md](../docs/decisions/2026-09-20-reimu-tier1-native-static-slice.md), [2026-09-20-reimu-tier1-visual-approval.md](../docs/decisions/2026-09-20-reimu-tier1-visual-approval.md) | Fresh Swift compilation, behavior, AppKit, resource isolation, fallback, observer, tool, repository, signature, archive, and isolated runtime capture checks passed. |
| visual | yes | `approved` | [2026-09-20-reimu-tier1-native-static-slice.md](../docs/decisions/2026-09-20-reimu-tier1-native-static-slice.md), [2026-09-20-reimu-tier1-visual-approval.md](../docs/decisions/2026-09-20-reimu-tier1-visual-approval.md) | The user approved the reviewed native size, placement, support and crop, static hold, Tier1–5 switching, immediate preemption, and latest-count recovery on 2026-09-20. |
| consumer | yes | `verified` | [2026-09-20-reimu-tier1-native-static-slice.md](../docs/decisions/2026-09-20-reimu-tier1-native-static-slice.md), [2026-09-20-reimu-tier1-visual-approval.md](../docs/decisions/2026-09-20-reimu-tier1-visual-approval.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/c2684cc3fecbdfbe0ae238a13f8e22fef333295d) | The published Consumer source selects Tier1 only through the single mapping while working with exact count one, independently degrades a broken package, and accepts the approved manifest in preview or production identity. |
| publication | yes | `published` | [2026-09-20-reimu-tier1-publication.md](../docs/decisions/2026-09-20-reimu-tier1-publication.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/c2684cc3fecbdfbe0ae238a13f8e22fef333295d) | The exact Consumer commit is verified on origin/main; no application installation, tag, or package release is implied. |

<a id="reimu-tier2-runtime-001"></a>
## `REIMU-TIER2-RUNTIME-001` · Connect observed count two to the approved native task_2 loop

Derived stage: **complete**.

| Gate | Required | Status | Evidence | Boundary note |
| --- | --- | --- | --- | --- |
| specification | yes | `ready` | [2026-09-19-reimu-tier2-native-vertical-slice.md](../docs/decisions/2026-09-19-reimu-tier2-native-vertical-slice.md) | The count-truth boundary, tier-2-only identity, honest fallbacks, loop-boundary switching, preemption, and reduced-motion rules are explicit. |
| implementation | yes | `ready` | [2026-09-19-reimu-tier2-native-vertical-slice.md](../docs/decisions/2026-09-19-reimu-tier2-native-vertical-slice.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/6a1318257d9bedc2b9a937304ea4b434ca874409) | The published consumer commit contains the observer-to-behavior data path, exact package loader, selector, and regression tests. |
| technical | yes | `passed` | [2026-09-19-reimu-tier2-native-vertical-slice.md](../docs/decisions/2026-09-19-reimu-tier2-native-vertical-slice.md) | Harness 0.8.0 integration, Swift behavior, native loader, AppKit self-test, repository, JSON, runtime, and diff gates passed. |
| visual | yes | `approved` | [2026-09-19-reimu-tier2-native-vertical-slice.md](../docs/decisions/2026-09-19-reimu-tier2-native-vertical-slice.md) | The user approved the current native tier-2 loop preview; unbuilt transition animations are tracked as a separate future task. |
| consumer | yes | `verified` | [2026-09-19-reimu-tier2-native-vertical-slice.md](../docs/decisions/2026-09-19-reimu-tier2-native-vertical-slice.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/6a1318257d9bedc2b9a937304ea4b434ca874409) | The consumer preserves the observed count and selects exact task_2 only for working plus count two; unavailable tiers remain honest fallbacks. |
| publication | yes | `published` | [2026-09-20-reimu-tier2-tier3-publication.md](../docs/decisions/2026-09-20-reimu-tier2-tier3-publication.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/6a1318257d9bedc2b9a937304ea4b434ca874409) | The exact consumer commit is verified on origin/main; preview packages remain local and no app installation, tag, or package release is implied. |

<a id="reimu-tier3-runtime-001"></a>
## `REIMU-TIER3-RUNTIME-001` · Connect observed count three to the existing native task_3 still

Derived stage: **complete**.

| Gate | Required | Status | Evidence | Boundary note |
| --- | --- | --- | --- | --- |
| specification | yes | `ready` | [2026-09-19-reimu-tier3-native-static-slice.md](../docs/decisions/2026-09-19-reimu-tier3-native-static-slice.md) | Count-three identity, immutable one-frame source, honest static semantics, switching, preemption, reduced motion, and isolated fallback are explicit. |
| implementation | yes | `ready` | [2026-09-19-reimu-tier3-native-static-slice.md](../docs/decisions/2026-09-19-reimu-tier3-native-static-slice.md), [2026-09-20-reimu-tier3-visual-approval.md](../docs/decisions/2026-09-20-reimu-tier3-visual-approval.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/6a1318257d9bedc2b9a937304ea4b434ca874409) | The published consumer commit contains the exact static package, selector, loader, regression tests, and a production-eligible build path after visual approval. |
| technical | yes | `passed` | [2026-09-19-reimu-tier3-native-static-slice.md](../docs/decisions/2026-09-19-reimu-tier3-native-static-slice.md), [2026-09-20-reimu-tier3-visual-approval.md](../docs/decisions/2026-09-20-reimu-tier3-visual-approval.md), [2026-09-20-reimu-tier3-fresh-source-build.md](../docs/decisions/2026-09-20-reimu-tier3-fresh-source-build.md) | Consumer tools, fresh Swift source compilation, Swift behavior, native AppKit, package fallback, observer bridge, repository, JSON, runtime capture, formal-identity package validation, signature, and diff gates passed. |
| visual | yes | `approved` | [2026-09-20-reimu-tier3-visual-approval.md](../docs/decisions/2026-09-20-reimu-tier3-visual-approval.md) | The user approved the reviewed native tier-3 size, pose, static hold, and demonstrated switching on 2026-09-20; this still is not a completed multi-frame animation. |
| consumer | yes | `verified` | [2026-09-19-reimu-tier3-native-static-slice.md](../docs/decisions/2026-09-19-reimu-tier3-native-static-slice.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/6a1318257d9bedc2b9a937304ea4b434ca874409) | The consumer selects exact task_3 only for working plus count three, preserves tier-2 behavior, and degrades a broken tier-3 package independently. |
| publication | yes | `published` | [2026-09-20-reimu-tier2-tier3-publication.md](../docs/decisions/2026-09-20-reimu-tier2-tier3-publication.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/6a1318257d9bedc2b9a937304ea4b434ca874409) | The exact consumer commit is verified on origin/main; the formal-identity ZIP remains local and no app installation, tag, or package release is implied. |

<a id="reimu-tier4-intake-001"></a>
## `REIMU-TIER4-INTAKE-001` · Prepare and review the existing Tier4 ramen still

Derived stage: **complete**.

| Gate | Required | Status | Evidence | Boundary note |
| --- | --- | --- | --- | --- |
| specification | yes | `ready` | [2026-09-20-reimu-tier4-static-intake.md](../docs/decisions/2026-09-20-reimu-tier4-static-intake.md) | Exact count four; immutable existing ramen/dumpling source; one-frame static hold. |
| implementation | yes | `ready` | [2026-09-20-reimu-tier4-static-intake.md](../docs/decisions/2026-09-20-reimu-tier4-static-intake.md) | Pinned source, plan, normal and reduced builds, previews and intake report exist under build/reimu-tier4-intake-20260920. |
| technical | yes | `passed` | [2026-09-20-reimu-tier4-static-intake.md](../docs/decisions/2026-09-20-reimu-tier4-static-intake.md) | Both public CLI pipelines pass with expected ZERO_MOTION; decoded pixels equal the source; original digest unchanged. |
| visual | yes | `approved` | [2026-09-20-reimu-tier4-static-intake.md](../docs/decisions/2026-09-20-reimu-tier4-static-intake.md), [2026-09-20-reimu-tier4-visual-approval.md](../docs/decisions/2026-09-20-reimu-tier4-visual-approval.md) | The user approved the reviewed Tier 4 source and native presentation on 2026-09-20; the one-frame source remains a static hold, not a completed animation. |
| consumer | no | `not_required` | [2026-09-20-reimu-tier4-static-intake.md](../docs/decisions/2026-09-20-reimu-tier4-static-intake.md) | This task covers artwork intake only; native integration is tracked separately by REIMU-TIER4-RUNTIME-001. |
| publication | no | `not_required` | [2026-09-20-reimu-tier4-static-intake.md](../docs/decisions/2026-09-20-reimu-tier4-static-intake.md) | Local review candidate; no publication requested. |

<a id="reimu-tier4-runtime-001"></a>
## `REIMU-TIER4-RUNTIME-001` · Connect observed count four to the existing native Tier4 still

Derived stage: **complete**.

| Gate | Required | Status | Evidence | Boundary note |
| --- | --- | --- | --- | --- |
| specification | yes | `ready` | [2026-09-20-reimu-tier4-native-static-slice.md](../docs/decisions/2026-09-20-reimu-tier4-native-static-slice.md), [2026-09-20-reimu-tier4-visual-approval.md](../docs/decisions/2026-09-20-reimu-tier4-visual-approval.md) | Exact count four, immutable one-frame source, safe-boundary switching, immediate preemption, latest-count recovery, reduced motion, isolated fallback, and the post-approval packaging boundary are explicit. |
| implementation | yes | `ready` | [2026-09-20-reimu-tier4-native-static-slice.md](../docs/decisions/2026-09-20-reimu-tier4-native-static-slice.md), [2026-09-20-reimu-tier4-visual-approval.md](../docs/decisions/2026-09-20-reimu-tier4-visual-approval.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/aa820f07a1352f5e9291548f08187e408aada5bd) | The published Consumer commit contains the independent resource package, native identity, loader, selector, targeted tests, and the visually approved production-eligible build gate. |
| technical | yes | `passed` | [2026-09-20-reimu-tier4-native-static-slice.md](../docs/decisions/2026-09-20-reimu-tier4-native-static-slice.md), [2026-09-20-reimu-tier4-visual-approval.md](../docs/decisions/2026-09-20-reimu-tier4-visual-approval.md) | Fresh Swift compilation, behavior, AppKit, resource isolation, fallback, observer, tool, repository, signature, archive, isolated runtime capture, and the updated manifest pin checks passed. |
| visual | yes | `approved` | [2026-09-20-reimu-tier4-native-static-slice.md](../docs/decisions/2026-09-20-reimu-tier4-native-static-slice.md), [2026-09-20-reimu-tier4-visual-approval.md](../docs/decisions/2026-09-20-reimu-tier4-visual-approval.md) | The user approved the reviewed native size, placement, support and crop, static hold, Tier 2/3/4 switching, immediate preemption, and latest-count recovery on 2026-09-20. |
| consumer | yes | `verified` | [2026-09-20-reimu-tier4-native-static-slice.md](../docs/decisions/2026-09-20-reimu-tier4-native-static-slice.md), [2026-09-20-reimu-tier4-visual-approval.md](../docs/decisions/2026-09-20-reimu-tier4-visual-approval.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/aa820f07a1352f5e9291548f08187e408aada5bd) | The published Consumer source selects Tier4 only for working plus exact count four, independently degrades a broken package, and accepts the approved manifest in preview or production identity. |
| publication | yes | `published` | [2026-09-20-reimu-tier4-publication.md](../docs/decisions/2026-09-20-reimu-tier4-publication.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/aa820f07a1352f5e9291548f08187e408aada5bd) | The exact Consumer commit is verified on origin/main; no application installation, tag, or package release is implied. |

<a id="reimu-tier5-intake-001"></a>
## `REIMU-TIER5-INTAKE-001` · Prepare and review the existing Tier5 meal still

Derived stage: **complete**.

| Gate | Required | Status | Evidence | Boundary note |
| --- | --- | --- | --- | --- |
| specification | yes | `ready` | [2026-09-20-reimu-tier5-static-intake.md](../docs/decisions/2026-09-20-reimu-tier5-static-intake.md) | Five or more active tasks; immutable existing meal source; one-frame static hold. |
| implementation | yes | `ready` | [2026-09-20-reimu-tier5-static-intake.md](../docs/decisions/2026-09-20-reimu-tier5-static-intake.md) | Pinned source, plan, normal and reduced builds, previews, and intake report exist under build/reimu-tier5-intake-20260920. |
| technical | yes | `passed` | [2026-09-20-reimu-tier5-static-intake.md](../docs/decisions/2026-09-20-reimu-tier5-static-intake.md) | Both public CLI pipelines pass with expected ZERO_MOTION; decoded pixels equal the source in normal and reduced motion; the original digest is unchanged. |
| visual | yes | `approved` | [2026-09-20-reimu-tier5-static-intake.md](../docs/decisions/2026-09-20-reimu-tier5-static-intake.md), [2026-09-20-reimu-tier5-native-static-slice.md](../docs/decisions/2026-09-20-reimu-tier5-native-static-slice.md), [2026-09-20-reimu-tier5-visual-approval.md](../docs/decisions/2026-09-20-reimu-tier5-visual-approval.md) | The user approved the reviewed Tier5 source and native presentation on 2026-09-20; the one-frame source remains a static hold, not a completed animation. |
| consumer | no | `not_required` | [2026-09-20-reimu-tier5-static-intake.md](../docs/decisions/2026-09-20-reimu-tier5-static-intake.md) | This task covers artwork intake only; native integration is tracked separately by REIMU-TIER5-RUNTIME-001. |
| publication | no | `not_required` | [2026-09-20-reimu-tier5-static-intake.md](../docs/decisions/2026-09-20-reimu-tier5-static-intake.md) | Local review candidate; no publication requested. |

<a id="reimu-tier5-runtime-001"></a>
## `REIMU-TIER5-RUNTIME-001` · Connect five or more observed tasks to the existing native Tier5 still

Derived stage: **complete**.

| Gate | Required | Status | Evidence | Boundary note |
| --- | --- | --- | --- | --- |
| specification | yes | `ready` | [2026-09-20-reimu-tier5-native-static-slice.md](../docs/decisions/2026-09-20-reimu-tier5-native-static-slice.md), [2026-09-20-reimu-tier5-visual-approval.md](../docs/decisions/2026-09-20-reimu-tier5-visual-approval.md) | The single capped tier policy, immutable one-frame source, safe-boundary switching, immediate preemption, latest-count recovery, reduced motion, isolated fallback, and visual approval boundary are explicit. |
| implementation | yes | `ready` | [2026-09-20-reimu-tier5-native-static-slice.md](../docs/decisions/2026-09-20-reimu-tier5-native-static-slice.md), [2026-09-20-reimu-tier5-visual-approval.md](../docs/decisions/2026-09-20-reimu-tier5-visual-approval.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/d2b6bef76d9b5330f5e56a7ee61fbe86c6cdf9ac) | The published Consumer commit contains the independent resource package, native identity, loader, selector, targeted tests, and the visually approved production-eligible build gate. |
| technical | yes | `passed` | [2026-09-20-reimu-tier5-native-static-slice.md](../docs/decisions/2026-09-20-reimu-tier5-native-static-slice.md), [2026-09-20-reimu-tier5-visual-approval.md](../docs/decisions/2026-09-20-reimu-tier5-visual-approval.md) | Fresh Swift compilation, behavior, AppKit, resource isolation, fallback, observer, tool, repository, signature, archive, and isolated runtime capture checks passed. |
| visual | yes | `approved` | [2026-09-20-reimu-tier5-native-static-slice.md](../docs/decisions/2026-09-20-reimu-tier5-native-static-slice.md), [2026-09-20-reimu-tier5-visual-approval.md](../docs/decisions/2026-09-20-reimu-tier5-visual-approval.md) | The user approved the reviewed native size, placement, support and crop, static hold, Tier2/3/4/5 switching, capped selection, immediate preemption, and latest-count recovery on 2026-09-20. |
| consumer | yes | `verified` | [2026-09-20-reimu-tier5-native-static-slice.md](../docs/decisions/2026-09-20-reimu-tier5-native-static-slice.md), [2026-09-20-reimu-tier5-visual-approval.md](../docs/decisions/2026-09-20-reimu-tier5-visual-approval.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/d2b6bef76d9b5330f5e56a7ee61fbe86c6cdf9ac) | The published Consumer source selects Tier5 only through the single capped mapping while working, independently degrades a broken package, and accepts the approved manifest in preview or production identity. |
| publication | yes | `published` | [2026-09-20-reimu-tier5-publication.md](../docs/decisions/2026-09-20-reimu-tier5-publication.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/d2b6bef76d9b5330f5e56a7ee61fbe86c6cdf9ac) | The exact Consumer commit is verified on origin/main; no application installation, tag, or package release is implied. |

<a id="reimu-work-transitions-001"></a>
## `REIMU-WORK-TRANSITIONS-001` · Author transitions around native workload eating

Derived stage: **implementation**.

| Gate | Required | Status | Evidence | Boundary note |
| --- | --- | --- | --- | --- |
| specification | yes | `ready` | [2026-09-20-reimu-work-transitions-spec.md](../docs/decisions/2026-09-20-reimu-work-transitions-spec.md) | The directed entry, exit, and cross-tier identity matrix, sharing rule, safe-boundary and preemption semantics, immutable endpoint and manifest contract, reduced-motion and isolated-fallback behavior, first vertical slice, future tests, and native preview evidence are frozen without claiming any artwork or runtime implementation. |
| implementation | yes | `pending` | [2026-09-20-reimu-standing-tier2-entry-generation-blocked.md](../docs/decisions/2026-09-20-reimu-standing-tier2-entry-generation-blocked.md), [2026-09-20-reimu-standing-tier2-serial-generation-blocked.md](../docs/decisions/2026-09-20-reimu-standing-tier2-serial-generation-blocked.md), [2026-09-20-reimu-standing-tier2-seam-feasibility-failed.md](../docs/decisions/2026-09-20-reimu-standing-tier2-seam-feasibility-failed.md) | The first standing-to-Tier2 generation attempt was stopped after complete-scene and explicit-layer strategies both failed the transparent-background and fixed-scene gates. The subsequent AI-only single-frame serial attempt also stopped before import. A bounded endpoint-seam experiment then used five of six allowed image calls: no character layer passed the strict detached-low-alpha gate, the tatami was clipped, and the table geometry drifted, so no composite candidate or transition package exists. |
| technical | yes | `pending` | [2026-09-20-reimu-standing-tier2-entry-generation-blocked.md](../docs/decisions/2026-09-20-reimu-standing-tier2-entry-generation-blocked.md), [2026-09-20-reimu-standing-tier2-serial-generation-blocked.md](../docs/decisions/2026-09-20-reimu-standing-tier2-serial-generation-blocked.md), [2026-09-20-reimu-standing-tier2-seam-feasibility-failed.md](../docs/decisions/2026-09-20-reimu-standing-tier2-seam-feasibility-failed.md) | The four immutable endpoint digests and deterministic 596px standing receipt were reverified, but the endpoint-seam experiment failed its layer material gates before composition. No candidate, endpoint overlay/diff, full/reduced validation, interruption, route-isolation, or fallback test exists. |
| visual | yes | `pending` | [2026-09-20-reimu-standing-tier2-entry-generation-blocked.md](../docs/decisions/2026-09-20-reimu-standing-tier2-entry-generation-blocked.md), [2026-09-20-reimu-standing-tier2-serial-generation-blocked.md](../docs/decisions/2026-09-20-reimu-standing-tier2-serial-generation-blocked.md), [2026-09-20-reimu-standing-tier2-seam-feasibility-failed.md](../docs/decisions/2026-09-20-reimu-standing-tier2-seam-feasibility-failed.md) | Rejected generation attempts and the endpoint-seam experiment are diagnostic evidence only. The closest character study remains unaccepted, no three-layer candidate or seam preview exists, and the route is neither in review nor approved. |
| consumer | yes | `pending` | — | The Consumer still uses the approved direct switch; a future integration must preserve the single tier policy, immediate high-priority preemption, isolated route fallback, and latest-observation recovery. |
| publication | yes | `unpublished` | — | The specification and blocked-attempt records were committed with the 2026-11-10 Harness records commit; no transition has been authored, installed, tagged, or released. |
