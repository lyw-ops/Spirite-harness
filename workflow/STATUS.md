# Sprite Harness task status

> Generated from `workflow/tasks.json`; do not edit by hand.

Ledger date: **2026-09-19**.

A gate records one claim only. In particular, `technical: passed` never supplies visual, consumer, installation, or publication evidence.

| Task | Kind | Derived stage | Required gates | Dependencies |
| --- | --- | --- | --- | --- |
| `HARNESS-KEYFRAMES-001` · Release keyframe tracks and the discrete pulse curve | core-capability | **publication** | specification, implementation, technical, consumer, publication | — |
| `HARNESS-WORKFLOW-001` · Adopt the evidence-bound Sprite Harness workflow | infrastructure | **publication** | specification, implementation, technical, publication | — |
| `REIMU-ACTIONS-001` · Produce the six-tier work-eating, idle onigiri, and grabbed-drag action set | animation-delivery | **implementation** | specification, implementation, technical, visual, consumer, publication | `HARNESS-KEYFRAMES-001` |

<a id="harness-keyframes-001"></a>
## `HARNESS-KEYFRAMES-001` · Release keyframe tracks and the discrete pulse curve

Derived stage: **publication**.

| Gate | Required | Status | Evidence | Boundary note |
| --- | --- | --- | --- | --- |
| specification | yes | `ready` | [animation-plan.md](../docs/animation-plan.md), [animation-plan.schema.json](../schemas/animation-plan.schema.json) | Keyframe and pulse semantics are described in the current working tree. |
| implementation | yes | `ready` | [curves.py](../src/sprite_harness/curves.py), [expand.py](../src/sprite_harness/expand.py), [test_plan.py](../tests/test_plan.py) | The implementation is present, but this ledger does not turn uncommitted source into a release. |
| technical | yes | `passed` | [2026-09-19-0.8.0-workflow-closure.md](../docs/decisions/2026-09-19-0.8.0-workflow-closure.md) | Current-version M3 and M4/M5 acceptance plus the aggregate Harness verification passed. |
| visual | no | `not_required` | — | The generic core feature has no character-art approval gate. |
| consumer | yes | `verified` | [2026-09-19-0.8.0-workflow-closure.md](../docs/decisions/2026-09-19-0.8.0-workflow-closure.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/tree/d7394914fe2bffc5cec03d49c54d2d7285d56cd5) | All 125 consumer tests passed with the 0.8.0 CLI explicitly pinned; no Harness integration test was skipped. |
| publication | yes | `unpublished` | — | No commit, push, tag, or package release is inferred from local implementation. |

<a id="harness-workflow-001"></a>
## `HARNESS-WORKFLOW-001` · Adopt the evidence-bound Sprite Harness workflow

Derived stage: **publication**.

| Gate | Required | Status | Evidence | Boundary note |
| --- | --- | --- | --- | --- |
| specification | yes | `ready` | [workflow.md](../docs/workflow.md), [HARNESS.md](../HARNESS.md) | The canonical lifecycle, evidence boundaries, and publication protocol are documented. |
| implementation | yes | `ready` | [update.py](../workflow/update.py), [verify.py](../scripts/verify.py), [test_workflow.py](../tests/test_workflow.py) | The task ledger, generated views, aggregate verifier, and regression tests exist. |
| technical | yes | `passed` | [2026-09-19-0.8.0-workflow-closure.md](../docs/decisions/2026-09-19-0.8.0-workflow-closure.md) | The aggregate workflow, pytest, compile, diff, and layered CLI smoke gates passed on the closure source. |
| visual | no | `not_required` | — | Workflow infrastructure has no artwork approval gate. |
| consumer | no | `not_required` | — | This infrastructure does not itself change a consumer runtime. |
| publication | yes | `unpublished` | — | Commit and push remain separate, explicit maintainer actions. |

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
