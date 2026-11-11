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
**2 complete**
<!-- END GENERATED SUMMARY -->

## Task register

<!-- BEGIN GENERATED TASKS -->
| Task | Derived stage | Next unsatisfied required gate |
| --- | --- | --- |
| [`HARNESS-KEYFRAMES-001`](STATUS.md#harness-keyframes-001) | **complete** | — |
| [`HARNESS-WORKFLOW-001`](STATUS.md#harness-workflow-001) | **complete** | — |
<!-- END GENERATED TASKS -->

## Dependency view

Arrows point from a prerequisite to the task that depends on it. A dependency
edge does not claim that either endpoint passed its technical or visual gates.

<!-- BEGIN GENERATED TREE -->
```mermaid
flowchart LR
    N_HARNESS_KEYFRAMES_001["✓ HARNESS-KEYFRAMES-001<br/>Release keyframe tracks and the discrete pulse curve<br/>stage: complete"]
    N_HARNESS_WORKFLOW_001["✓ HARNESS-WORKFLOW-001<br/>Adopt the evidence-bound Sprite Harness workflow<br/>stage: complete"]
    classDef complete fill:#dbeafe,stroke:#1d4ed8,color:#172554;
    classDef active fill:#ffedd5,stroke:#c2410c,color:#431407;
    classDef blocked fill:#fee2e2,stroke:#b91c1c,color:#450a0a;
    class N_HARNESS_KEYFRAMES_001,N_HARNESS_WORKFLOW_001 complete;
```
<!-- END GENERATED TREE -->
