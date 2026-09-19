# Sprite Harness progress

This directory is the generated project view. The canonical task source is
[`tasks.json`](tasks.json); lifecycle and evidence rules live in
[`docs/workflow.md`](../docs/workflow.md). Do not hand-edit generated blocks,
[`STATUS.md`](STATUS.md), or [`TREE.mmd`](TREE.mmd).

Use `python workflow/update.py` while editing. Before publication, stage the
intended canonical inputs, run `python workflow/update.py --index`, stage the
generated views, and finish with `python workflow/update.py --index --check`.
That keeps unrelated unstaged work out of the published status view.

Symbols and text are both present: `✓` complete, `◐` active, `!` blocked. Color
is supplementary and never the only status signal.

## Current summary

<!-- BEGIN GENERATED SUMMARY -->
**8 complete** · **1 implementation** · **1 specification**
<!-- END GENERATED SUMMARY -->

## Task register

<!-- BEGIN GENERATED TASKS -->
| Task | Derived stage | Next unsatisfied required gate |
| --- | --- | --- |
| [`HARNESS-KEYFRAMES-001`](STATUS.md#harness-keyframes-001) | **complete** | — |
| [`HARNESS-WORKFLOW-001`](STATUS.md#harness-workflow-001) | **complete** | — |
| [`REIMU-ACTIONS-001`](STATUS.md#reimu-actions-001) | **implementation** | implementation |
| [`REIMU-TIER2-RUNTIME-001`](STATUS.md#reimu-tier2-runtime-001) | **complete** | — |
| [`REIMU-TIER3-RUNTIME-001`](STATUS.md#reimu-tier3-runtime-001) | **complete** | — |
| [`REIMU-TIER4-INTAKE-001`](STATUS.md#reimu-tier4-intake-001) | **complete** | — |
| [`REIMU-TIER4-RUNTIME-001`](STATUS.md#reimu-tier4-runtime-001) | **complete** | — |
| [`REIMU-TIER5-INTAKE-001`](STATUS.md#reimu-tier5-intake-001) | **complete** | — |
| [`REIMU-TIER5-RUNTIME-001`](STATUS.md#reimu-tier5-runtime-001) | **complete** | — |
| [`REIMU-WORK-TRANSITIONS-001`](STATUS.md#reimu-work-transitions-001) | **specification** | specification |
<!-- END GENERATED TASKS -->

## Dependency view

Arrows point from a prerequisite to the task that depends on it. A dependency
edge does not claim that either endpoint passed its technical or visual gates.

<!-- BEGIN GENERATED TREE -->
```mermaid
flowchart LR
    N_HARNESS_KEYFRAMES_001["✓ HARNESS-KEYFRAMES-001<br/>Release keyframe tracks and the discrete pulse curve<br/>stage: complete"]
    N_HARNESS_WORKFLOW_001["✓ HARNESS-WORKFLOW-001<br/>Adopt the evidence-bound Sprite Harness workflow<br/>stage: complete"]
    N_REIMU_ACTIONS_001["◐ REIMU-ACTIONS-001<br/>Produce the six-tier work-eating, idle onigiri, and grabbed-drag action set<br/>stage: implementation"]
    N_REIMU_TIER2_RUNTIME_001["✓ REIMU-TIER2-RUNTIME-001<br/>Connect observed count two to the approved native task_2 loop<br/>stage: complete"]
    N_REIMU_TIER3_RUNTIME_001["✓ REIMU-TIER3-RUNTIME-001<br/>Connect observed count three to the existing native task_3 still<br/>stage: complete"]
    N_REIMU_TIER4_INTAKE_001["✓ REIMU-TIER4-INTAKE-001<br/>Prepare and review the existing Tier4 ramen still<br/>stage: complete"]
    N_REIMU_TIER4_RUNTIME_001["✓ REIMU-TIER4-RUNTIME-001<br/>Connect observed count four to the existing native Tier4 still<br/>stage: complete"]
    N_REIMU_TIER5_INTAKE_001["✓ REIMU-TIER5-INTAKE-001<br/>Prepare and review the existing Tier5 meal still<br/>stage: complete"]
    N_REIMU_TIER5_RUNTIME_001["✓ REIMU-TIER5-RUNTIME-001<br/>Connect five or more observed tasks to the existing native Tier5 still<br/>stage: complete"]
    N_REIMU_WORK_TRANSITIONS_001["◐ REIMU-WORK-TRANSITIONS-001<br/>Author transitions around native workload eating<br/>stage: specification"]
    N_HARNESS_KEYFRAMES_001 --> N_REIMU_ACTIONS_001
    N_REIMU_ACTIONS_001 --> N_REIMU_TIER2_RUNTIME_001
    N_REIMU_TIER2_RUNTIME_001 --> N_REIMU_TIER3_RUNTIME_001
    N_REIMU_TIER3_RUNTIME_001 --> N_REIMU_TIER4_RUNTIME_001
    N_REIMU_TIER4_INTAKE_001 --> N_REIMU_TIER4_RUNTIME_001
    N_REIMU_TIER4_RUNTIME_001 --> N_REIMU_TIER5_RUNTIME_001
    N_REIMU_TIER5_INTAKE_001 --> N_REIMU_TIER5_RUNTIME_001
    N_REIMU_TIER2_RUNTIME_001 --> N_REIMU_WORK_TRANSITIONS_001
    N_REIMU_TIER3_RUNTIME_001 --> N_REIMU_WORK_TRANSITIONS_001
    N_REIMU_TIER4_RUNTIME_001 --> N_REIMU_WORK_TRANSITIONS_001
    N_REIMU_TIER5_RUNTIME_001 --> N_REIMU_WORK_TRANSITIONS_001
    classDef complete fill:#dbeafe,stroke:#1d4ed8,color:#172554;
    classDef active fill:#ffedd5,stroke:#c2410c,color:#431407;
    classDef blocked fill:#fee2e2,stroke:#b91c1c,color:#450a0a;
    class N_HARNESS_KEYFRAMES_001,N_HARNESS_WORKFLOW_001,N_REIMU_TIER2_RUNTIME_001,N_REIMU_TIER3_RUNTIME_001,N_REIMU_TIER4_INTAKE_001,N_REIMU_TIER4_RUNTIME_001,N_REIMU_TIER5_INTAKE_001,N_REIMU_TIER5_RUNTIME_001 complete;
    class N_REIMU_ACTIONS_001,N_REIMU_WORK_TRANSITIONS_001 active;
```
<!-- END GENERATED TREE -->
