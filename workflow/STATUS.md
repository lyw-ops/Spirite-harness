# Sprite Harness task status

> Generated from `workflow/tasks.json`; do not edit by hand.

Ledger date: **2026-11-11**.

A gate records one claim only. In particular, `technical: passed` never supplies visual, consumer, installation, or publication evidence.

| Task | Kind | Derived stage | Required gates | Dependencies |
| --- | --- | --- | --- | --- |
| `HARNESS-KEYFRAMES-001` · Release keyframe tracks and the discrete pulse curve | core-capability | **complete** | specification, implementation, technical, consumer, publication | — |
| `HARNESS-WORKFLOW-001` · Adopt the evidence-bound Sprite Harness workflow | infrastructure | **complete** | specification, implementation, technical, publication | — |

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
