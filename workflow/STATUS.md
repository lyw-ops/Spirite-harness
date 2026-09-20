# Sprite Harness task status

> Generated from `workflow/tasks.json`; do not edit by hand.

Ledger date: **2026-09-20**.

A gate records one claim only. In particular, `technical: passed` never supplies visual, consumer, installation, or publication evidence.

| Task | Kind | Derived stage | Required gates | Dependencies |
| --- | --- | --- | --- | --- |
| `HARNESS-KEYFRAMES-001` · Release keyframe tracks and the discrete pulse curve | core-capability | **complete** | specification, implementation, technical, consumer, publication | — |
| `HARNESS-WORKFLOW-001` · Adopt the evidence-bound Sprite Harness workflow | infrastructure | **complete** | specification, implementation, technical, publication | — |
| `REIMU-ACTIONS-001` · Produce the six-tier work-eating, idle onigiri, and grabbed-drag action set | animation-delivery | **implementation** | specification, implementation, technical, visual, consumer, publication | `HARNESS-KEYFRAMES-001` |
| `REIMU-TIER1-INTAKE-001` · Prepare and review the existing Tier1 onigiri still | animation-delivery | **complete** | specification, implementation, technical, visual | — |
| `REIMU-TIER1-RUNTIME-001` · Connect observed count one to the existing native Tier1 still | consumer-vertical-slice | **complete** | specification, implementation, technical, visual, consumer, publication | `REIMU-TIER5-RUNTIME-001`, `REIMU-TIER1-INTAKE-001` |
| `REIMU-TIER2-RUNTIME-001` · Connect observed count two to the approved native task_2 loop | consumer-vertical-slice | **complete** | specification, implementation, technical, visual, consumer, publication | `REIMU-ACTIONS-001` |
| `REIMU-TIER3-RUNTIME-001` · Connect observed count three to the existing native task_3 still | consumer-vertical-slice | **complete** | specification, implementation, technical, visual, consumer, publication | `REIMU-TIER2-RUNTIME-001` |
| `REIMU-TIER4-INTAKE-001` · Prepare and review the existing Tier4 ramen still | animation-delivery | **complete** | specification, implementation, technical, visual | — |
| `REIMU-TIER4-RUNTIME-001` · Connect observed count four to the existing native Tier4 still | consumer-vertical-slice | **complete** | specification, implementation, technical, visual, consumer, publication | `REIMU-TIER3-RUNTIME-001`, `REIMU-TIER4-INTAKE-001` |
| `REIMU-TIER5-INTAKE-001` · Prepare and review the existing Tier5 meal still | animation-delivery | **complete** | specification, implementation, technical, visual | — |
| `REIMU-TIER5-RUNTIME-001` · Connect five or more observed tasks to the existing native Tier5 still | consumer-vertical-slice | **complete** | specification, implementation, technical, visual, consumer, publication | `REIMU-TIER4-RUNTIME-001`, `REIMU-TIER5-INTAKE-001` |
| `REIMU-WORK-TRANSITIONS-001` · Author transitions around native workload eating | animation-delivery | **specification** | specification, implementation, technical, visual, consumer, publication | `REIMU-TIER2-RUNTIME-001`, `REIMU-TIER3-RUNTIME-001`, `REIMU-TIER4-RUNTIME-001`, `REIMU-TIER5-RUNTIME-001`, `REIMU-TIER1-RUNTIME-001` |

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

Derived stage: **specification**.

| Gate | Required | Status | Evidence | Boundary note |
| --- | --- | --- | --- | --- |
| specification | yes | `pending` | [2026-09-19-reimu-tier2-native-vertical-slice.md](../docs/decisions/2026-09-19-reimu-tier2-native-vertical-slice.md), [2026-09-19-reimu-tier3-native-static-slice.md](../docs/decisions/2026-09-19-reimu-tier3-native-static-slice.md) | Candidate scope is entry, exit, future cross-tier changes, and post-transient recovery; exact clips, timing, and art direction are not yet frozen. |
| implementation | yes | `pending` | — | No transition artwork, manifest, or runtime transition node has been implemented. |
| technical | yes | `pending` | — | Transition continuity, interruption, reduced-motion, source-integrity, and fallback tests remain future work. |
| visual | yes | `pending` | — | Future transition timing and pose continuity require a separate native visual review. |
| consumer | yes | `pending` | — | Future transitions must preserve immediate high-priority preemption and restore only the latest observed tier. |
| publication | yes | `unpublished` | — | The transition task is only a recorded backlog item; nothing has been authored, installed, committed, or published for it. |
