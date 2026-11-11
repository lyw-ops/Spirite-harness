# Sprite Harness task status

> Generated from `workflow/tasks.json`; do not edit by hand.

Ledger date: **2026-11-11**.

A gate records one claim only. In particular, `technical: passed` never supplies visual, consumer, installation, or publication evidence.

| Task | Kind | Derived stage | Required gates | Dependencies |
| --- | --- | --- | --- | --- |
| `HARNESS-KEYFRAMES-001` · Release keyframe tracks and the discrete pulse curve | core-capability | **complete** | specification, implementation, technical, consumer, publication | — |
| `HARNESS-WORKFLOW-001` · Adopt the evidence-bound Sprite Harness workflow | infrastructure | **complete** | specification, implementation, technical, publication | — |
| `REIMU-ACTIONS-001` · Produce the six-tier work-eating, idle onigiri, and grabbed-drag action set | animation-delivery | **implementation** | specification, implementation, technical, visual, consumer, publication | `HARNESS-KEYFRAMES-001` |
| `REIMU-CUTER-STANDING-INTAKE-001` · Prepare a cuter, more chibi standing figure | animation-delivery | **blocked** | specification, implementation, technical, visual | — |
| `REIMU-DIALOGUE-ACTIONS-001` · Event remarks, a deeper click ladder and eyelid beats from Reimu's persona | consumer-vertical-slice | **complete** | specification, implementation, technical, visual, consumer, publication | `REIMU-SCENE-REACTIONS-001` |
| `REIMU-EATING-KEYFRAMES-INTAKE-001` · Author hand and mouth eating keyframes for the work tiers | animation-delivery | **complete** | specification, implementation, technical, visual | `REIMU-TIER-FACE-LOOPS-RUNTIME-001` |
| `REIMU-EATING-KEYFRAMES-RUNTIME-001` · Play the eating keyframe loops in the native pet (all five work tiers) | consumer-vertical-slice | **complete** | specification, implementation, technical, visual, consumer, publication | `REIMU-EATING-KEYFRAMES-INTAKE-001`, `REIMU-TIER-FACE-LOOPS-RUNTIME-001` |
| `REIMU-FAILURE-DROOP-001` · Hanging her head and sighing once when the observed work fails | consumer-vertical-slice | **complete** | specification, implementation, technical, visual, consumer, publication | `REIMU-STANDING-YAWN-001` |
| `REIMU-GOHEI-FLOAT-SWEEP-001` · Gohei on the fourth standing click, floating while dragged, sweeping; and the Codex review of every line | consumer-vertical-slice | **complete** | specification, implementation, technical, visual, consumer, publication | `REIMU-FAILURE-DROOP-001`, `REIMU-NIGHT-SLEEP-001` |
| `REIMU-MANGA-BALLOONS-001` · Draw Reimu's lines as manga speech balloons | consumer-vertical-slice | **complete** | specification, implementation, technical, visual, consumer, publication | `REIMU-DIALOGUE-ACTIONS-001` |
| `REIMU-NIGHT-SLEEP-001` · Sleeping at the low table late at night, with rules for falling asleep and waking | consumer-vertical-slice | **complete** | specification, implementation, technical, visual, consumer, publication | `REIMU-POOF-BRIDGE-001`, `REIMU-STANDING-YAWN-001` |
| `REIMU-POOF-BRIDGE-001` · Smoke display bridge between pose families | consumer-vertical-slice | **complete** | specification, implementation, technical, visual, consumer, publication | `REIMU-TEA-BREAK-001` |
| `REIMU-PROPS-OFFERING-BOX-INTAKE-001` · Prepare the offering box and coin props for standing scenes | animation-delivery | **blocked** | specification, implementation, technical, visual | `REIMU-SCENE-REACTIONS-001` |
| `REIMU-SCENE-REACTIONS-001` · Scene-aware click reactions, Reimu-voiced lines, and plain standing idle | consumer-vertical-slice | **complete** | specification, implementation, technical, visual, consumer, publication | `REIMU-TIER-EMOTE-LOOPS-RUNTIME-001` |
| `REIMU-STANDING-YAWN-001` · Standing yawn for sleepy clicks and late greetings | consumer-vertical-slice | **complete** | specification, implementation, technical, visual, consumer, publication | `REIMU-DIALOGUE-ACTIONS-001` |
| `REIMU-TEA-BREAK-001` · Tea break at the low table after a round of work | consumer-vertical-slice | **complete** | specification, implementation, technical, visual, consumer, publication | `REIMU-DIALOGUE-ACTIONS-001`, `REIMU-EATING-KEYFRAMES-RUNTIME-001` |
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
| `REIMU-WAITING-SLOUCH-001` · Slouch at the low table while the observed work waits for input | consumer-vertical-slice | **visual review** | specification, implementation, technical, visual, consumer, publication | `REIMU-DIALOGUE-ACTIONS-001`, `REIMU-POOF-BRIDGE-001` |
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

<a id="reimu-cuter-standing-intake-001"></a>
## `REIMU-CUTER-STANDING-INTAKE-001` · Prepare a cuter, more chibi standing figure

Derived stage: **blocked**.

| Gate | Required | Status | Evidence | Boundary note |
| --- | --- | --- | --- | --- |
| specification | yes | `ready` | [2026-11-10-reimu-cuter-standing-study.md](../docs/decisions/2026-11-10-reimu-cuter-standing-study.md) | Smooth, locally uniform rescale of the approved standing drawing: larger head, smaller body, fixed shoe line. The reading of the request as "the standing pose" is unconfirmed. |
| implementation | yes | `blocked` | [2026-11-10-reimu-cuter-standing-study.md](../docs/decisions/2026-11-10-reimu-cuter-standing-study.md) | Stopped at the 596 px study after the visual rejection; no production poses were made. |
| technical | yes | `pending` | [2026-11-10-reimu-cuter-standing-study.md](../docs/decisions/2026-11-10-reimu-cuter-standing-study.md) | Study only: bounds and shoe line were checked, and variant B matches the seated character scale. No package, digest or loader check exists. |
| visual | yes | `rejected` | [2026-11-10-reimu-cuter-standing-study.md](../docs/decisions/2026-11-10-reimu-cuter-standing-study.md) | The user replied "不太行，保持原样吧" on 2026-11-10. The approved standing figure stays as it is; none of the study variants is to be integrated. |
| consumer | no | `not_required` | [2026-11-10-reimu-cuter-standing-study.md](../docs/decisions/2026-11-10-reimu-cuter-standing-study.md) | Intake only. |
| publication | no | `not_required` | [2026-11-10-reimu-cuter-standing-study.md](../docs/decisions/2026-11-10-reimu-cuter-standing-study.md) | Local review candidate. |

<a id="reimu-dialogue-actions-001"></a>
## `REIMU-DIALOGUE-ACTIONS-001` · Event remarks, a deeper click ladder and eyelid beats from Reimu's persona

Derived stage: **complete**.

| Gate | Required | Status | Evidence | Boundary note |
| --- | --- | --- | --- | --- |
| specification | yes | `ready` | [2026-11-11-reimu-dialogue-and-action-design.md](../docs/decisions/2026-11-11-reimu-dialogue-and-action-design.md) | Persona rules, the event table with its pacing limits, per-scene line tables, the four-step click ladder, three eyelid beats and the ordered list of actions that still need new artwork are written down. |
| implementation | yes | `ready` | [2026-11-11-reimu-dialogue-and-action-design.md](../docs/decisions/2026-11-11-reimu-dialogue-and-action-design.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/36834509b3780dc0a3ca13342928ef03b8ddd9bb) | PetClock, PetEvent, the extended PetLines, react_stare, event remarks, the launch greeting and the menu toggle are in the published Consumer commit. No image asset was added or changed. |
| technical | yes | `passed` | [2026-11-11-reimu-dialogue-and-action-design.md](../docs/decisions/2026-11-11-reimu-dialogue-and-action-design.md) | 254 behavior, 38 native AppKit, reaction, standing, per-tier loader, status contract and repository gate checks and strict signatures passed on the 1.20/build 22 bundle. |
| visual | yes | `approved` | [2026-11-11-reimu-dialogue-and-action-design.md](../docs/decisions/2026-11-11-reimu-dialogue-and-action-design.md), [2026-11-11-reimu-gohei-float-sweep-and-line-review.md](../docs/decisions/2026-11-11-reimu-gohei-float-sweep-and-line-review.md) | The maintainer did not review the lines one by one and on 2026-11-11 delegated that review to Codex; it kept 119 of 135 lines and revised 16, all adopted and installed with 1.27/build 29. The maintainer then approved the installation with the three kinds of change summarised. The eyelid beats were never singled out for review. |
| consumer | yes | `verified` | [2026-11-11-reimu-dialogue-and-action-design.md](../docs/decisions/2026-11-11-reimu-dialogue-and-action-design.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/36834509b3780dc0a3ca13342928ef03b8ddd9bb) | Installed as 1.20/build 22 (since superseded by 1.21 and 1.22, which keep it); remarks are on by default and the launch greeting and a real work-eased remark were recorded in the behavior log. Idle still only stands. |
| publication | yes | `published` | [2026-11-11-reimu-dialogue-and-action-design.md](../docs/decisions/2026-11-11-reimu-dialogue-and-action-design.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/36834509b3780dc0a3ca13342928ef03b8ddd9bb) | The maintainer delegated all further steps including commit and push on 2026-11-11; the exact Consumer commit is on origin/main. No tag or release. |

<a id="reimu-eating-keyframes-intake-001"></a>
## `REIMU-EATING-KEYFRAMES-INTAKE-001` · Author hand and mouth eating keyframes for the work tiers

Derived stage: **complete**.

| Gate | Required | Status | Evidence | Boundary note |
| --- | --- | --- | --- | --- |
| specification | yes | `ready` | [2026-11-10-reimu-eating-keyframes-work-order.md](../docs/decisions/2026-11-10-reimu-eating-keyframes-work-order.md) | Two newly drawn keyframes per tier inside a measured edit box that lies inside the opaque silhouette; everything outside is locked to the approved still. Tier3 is the pilot. |
| implementation | yes | `ready` | [2026-11-10-reimu-eating-keyframes-work-order.md](../docs/decisions/2026-11-10-reimu-eating-keyframes-work-order.md), [2026-11-10-reimu-eating-keyframes-tier3-pilot.md](../docs/decisions/2026-11-10-reimu-eating-keyframes-tier3-pilot.md), [2026-11-10-reimu-eating-keyframes-tiers-1-2-4-5-candidates.md](../docs/decisions/2026-11-10-reimu-eating-keyframes-tiers-1-2-4-5-candidates.md) | Keyframes for all five tiers were drawn by the local Codex image tool and taken in; Tier2 and Tier5 needed one redraw each. Intake gained an opt-in changed-blob mask for the tiers whose arms move. |
| technical | yes | `passed` | [2026-11-10-reimu-eating-keyframes-tier3-pilot.md](../docs/decisions/2026-11-10-reimu-eating-keyframes-tier3-pilot.md), [2026-11-10-reimu-eating-keyframes-tiers-1-2-4-5-candidates.md](../docs/decisions/2026-11-10-reimu-eating-keyframes-tiers-1-2-4-5-candidates.md) | All five tiers: zero registration shift, rest and reduced frames equal the approved still, no change outside the measured rectangles and emote regions, Harness plan/render/validate pass. 160 px legibility 460-1440 px against the still. Tier1 K1-K2 differ by only 145 px, below the 250 floor; the guessed ring threshold of 10 was dropped in favour of zero shift plus a zoomed seam check. |
| visual | yes | `approved` | [2026-11-10-reimu-eating-keyframes-tier3-pilot.md](../docs/decisions/2026-11-10-reimu-eating-keyframes-tier3-pilot.md), [2026-11-10-reimu-eating-keyframes-tiers-1-2-4-5-candidates.md](../docs/decisions/2026-11-10-reimu-eating-keyframes-tiers-1-2-4-5-candidates.md), [2026-11-11-reimu-eating-keyframes-all-tiers-runtime.md](../docs/decisions/2026-11-11-reimu-eating-keyframes-all-tiers-runtime.md) | Tier3: "可以，继续" on 2026-11-10. Tier1, Tier2, Tier4 and Tier5: the user reviewed the comparison GIFs with the listed weak spots and replied "都可以，接入" on 2026-11-11. |
| consumer | no | `not_required` | [2026-11-10-reimu-eating-keyframes-work-order.md](../docs/decisions/2026-11-10-reimu-eating-keyframes-work-order.md) | Intake only. |
| publication | no | `not_required` | [2026-11-10-reimu-eating-keyframes-work-order.md](../docs/decisions/2026-11-10-reimu-eating-keyframes-work-order.md) | Local work order. |

<a id="reimu-eating-keyframes-runtime-001"></a>
## `REIMU-EATING-KEYFRAMES-RUNTIME-001` · Play the eating keyframe loops in the native pet (all five work tiers)

Derived stage: **complete**.

| Gate | Required | Status | Evidence | Boundary note |
| --- | --- | --- | --- | --- |
| specification | yes | `ready` | [2026-11-10-reimu-eating-keyframes-tier3-runtime.md](../docs/decisions/2026-11-10-reimu-eating-keyframes-tier3-runtime.md), [2026-11-11-reimu-eating-keyframes-all-tiers-runtime.md](../docs/decisions/2026-11-11-reimu-eating-keyframes-all-tiers-runtime.md) | Same exact-frame contract as the loops they replace: 24 frames at 10 fps, Tier2 16 frames; first and last frames are the approved still. |
| implementation | yes | `ready` | [2026-11-10-reimu-eating-keyframes-tier3-runtime.md](../docs/decisions/2026-11-10-reimu-eating-keyframes-tier3-runtime.md), [2026-11-11-reimu-eating-keyframes-all-tiers-runtime.md](../docs/decisions/2026-11-11-reimu-eating-keyframes-all-tiers-runtime.md) | Five task_N-eating-keyframes-v1 packages, all five builder pins and the repository gate are in Consumer commit 3b46b9c; no Swift change. |
| technical | yes | `passed` | [2026-11-10-reimu-eating-keyframes-tier3-runtime.md](../docs/decisions/2026-11-10-reimu-eating-keyframes-tier3-runtime.md), [2026-11-11-reimu-eating-keyframes-all-tiers-runtime.md](../docs/decisions/2026-11-11-reimu-eating-keyframes-all-tiers-runtime.md) | Fresh 1.19/build 21 compilation, 217 behavior, 37 native AppKit, status, per-tier loader and fallback checks, repository gate and strict signatures passed. |
| visual | yes | `approved` | [2026-11-10-reimu-eating-keyframes-tier3-pilot.md](../docs/decisions/2026-11-10-reimu-eating-keyframes-tier3-pilot.md), [2026-11-10-reimu-eating-keyframes-tiers-1-2-4-5-candidates.md](../docs/decisions/2026-11-10-reimu-eating-keyframes-tiers-1-2-4-5-candidates.md), [2026-11-11-reimu-eating-keyframes-all-tiers-runtime.md](../docs/decisions/2026-11-11-reimu-eating-keyframes-all-tiers-runtime.md) | The integrated frames are exactly the reviewed candidates (Tier3 approved 2026-11-10, the other four 2026-11-11). Reduced motion was on at install time, so on-screen playback was not observed. |
| consumer | yes | `verified` | [2026-11-11-reimu-eating-keyframes-all-tiers-runtime.md](../docs/decisions/2026-11-11-reimu-eating-keyframes-all-tiers-runtime.md) | The installed 1.19 loads all five keyframe loops (24/16/24/24/24 frames, reason none) and keeps the isolated per-tier fallback. |
| publication | yes | `published` | [2026-11-11-reimu-eating-keyframes-all-tiers-runtime.md](../docs/decisions/2026-11-11-reimu-eating-keyframes-all-tiers-runtime.md) | Consumer 3b46b9c85ff0c5dc3c6c94c40bac9fc578f2035d pushed to origin/main on 2026-11-11 at the user's request ("提交并推送"); installed locally as 1.19 / build 21 with a verified rollback. No tag or release. |

<a id="reimu-failure-droop-001"></a>
## `REIMU-FAILURE-DROOP-001` · Hanging her head and sighing once when the observed work fails

Derived stage: **complete**.

| Gate | Required | Status | Evidence | Boundary note |
| --- | --- | --- | --- | --- |
| specification | yes | `ready` | [2026-11-11-reimu-dialogue-and-action-design.md](../docs/decisions/2026-11-11-reimu-dialogue-and-action-design.md), [2026-11-11-reimu-failure-droop.md](../docs/decisions/2026-11-11-reimu-failure-droop.md) | Row 4 of the action roadmap; the pose pair, the once-per-failure trigger, reduced motion and the fallback to the eyelid wince are written down. The maintainer answered "画" on 2026-11-11. |
| implementation | yes | `ready` | [2026-11-11-reimu-failure-droop.md](../docs/decisions/2026-11-11-reimu-failure-droop.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/46e5799c161334dc116111b55b22dfb858cdd44c) | The droop-v1 pose table (with the approval record), presentation(droopAllowed:), the optional --droop build input, its package test and the gate rule are in the published Consumer commit. |
| technical | yes | `passed` | [2026-11-11-reimu-failure-droop.md](../docs/decisions/2026-11-11-reimu-failure-droop.md) | Harness 0.8.0 validation, pixel gates (zero changed pixels outside the take rectangle, unchanged shoe line, 3248-3648 px changed at 160 px), 311 behavior, 44 native and 4 package checks and strict signatures passed on the installed 1.25/build 27 bundle. |
| visual | yes | `approved` | [2026-11-11-reimu-failure-droop.md](../docs/decisions/2026-11-11-reimu-failure-droop.md) | With the side-by-side review GIF delivered and the three weak spots listed, the maintainer replied "可以，安装" on 2026-11-11. Approval was given from an offline composite before installation; reduced motion was on at install, so the droop may not have been seen on screen. |
| consumer | yes | `verified` | [2026-11-11-reimu-failure-droop.md](../docs/decisions/2026-11-11-reimu-failure-droop.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/46e5799c161334dc116111b55b22dfb858cdd44c) | Installed as 1.25/build 27, built from the sources later published unchanged; the installed loader reports droop_reason none and droop_frames 4. |
| publication | yes | `published` | [2026-11-11-reimu-failure-droop.md](../docs/decisions/2026-11-11-reimu-failure-droop.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/46e5799c161334dc116111b55b22dfb858cdd44c) | The exact Consumer commit is on origin/main; the maintainer answered "提交并推送" on 2026-11-11. No tag or release. |

<a id="reimu-gohei-float-sweep-001"></a>
## `REIMU-GOHEI-FLOAT-SWEEP-001` · Gohei on the fourth standing click, floating while dragged, sweeping; and the Codex review of every line

Derived stage: **complete**.

| Gate | Required | Status | Evidence | Boundary note |
| --- | --- | --- | --- | --- |
| specification | yes | `ready` | [2026-11-11-reimu-dialogue-and-action-design.md](../docs/decisions/2026-11-11-reimu-dialogue-and-action-design.md), [2026-11-11-reimu-gohei-float-sweep-and-line-review.md](../docs/decisions/2026-11-11-reimu-gohei-float-sweep-and-line-review.md) | Rows 3, 5 and 6 of the action roadmap, with each trigger, reduced motion and fallback written down, and the brief given to Codex for the line review. The maintainer answered "做完，台词你可以让codex去根据博丽灵梦的人物性格和习惯去review" on 2026-11-11. |
| implementation | yes | `ready` | [2026-11-11-reimu-gohei-float-sweep-and-line-review.md](../docs/decisions/2026-11-11-reimu-gohei-float-sweep-and-line-review.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/a81b57b21d7bfd29fcb22a1d371c2ffe784136f6) | The gohei-v1, float-v1 and sweep-v1 pose tables (with the approval record), their actions and triggers, three optional build inputs, three package tests, the gate rules and the sixteen revised lines are in the published Consumer commit. |
| technical | yes | `passed` | [2026-11-11-reimu-gohei-float-sweep-and-line-review.md](../docs/decisions/2026-11-11-reimu-gohei-float-sweep-and-line-review.md) | Harness 0.8.0 validation and pixel gates for all three (zero changed pixels outside the take rectangles for gohei and sweep; float is taken whole), 353 behavior checks, 49 native checks, 4 checks per new package and every other package test and strict signatures passed on the installed 1.27/build 29 bundle. |
| visual | yes | `approved` | [2026-11-11-reimu-gohei-float-sweep-and-line-review.md](../docs/decisions/2026-11-11-reimu-gohei-float-sweep-and-line-review.md) | With three review GIFs delivered and the triggers, the line changes and the weak spots listed, the maintainer replied "可以，安装" on 2026-11-11. The GIFs were offline composites; reduced motion was on at install; the sixteen revised lines were reviewed by Codex at the maintainer's request and not read one by one by the maintainer. |
| consumer | yes | `verified` | [2026-11-11-reimu-gohei-float-sweep-and-line-review.md](../docs/decisions/2026-11-11-reimu-gohei-float-sweep-and-line-review.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/a81b57b21d7bfd29fcb22a1d371c2ffe784136f6) | Installed as 1.27/build 29, built from the sources later published unchanged; the installed loader reports every reason none and 4 frames for each new package. |
| publication | yes | `published` | [2026-11-11-reimu-gohei-float-sweep-and-line-review.md](../docs/decisions/2026-11-11-reimu-gohei-float-sweep-and-line-review.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/a81b57b21d7bfd29fcb22a1d371c2ffe784136f6) | The exact Consumer commit is on origin/main; the maintainer answered "提交并推送" on 2026-11-11. No tag or release. |

<a id="reimu-manga-balloons-001"></a>
## `REIMU-MANGA-BALLOONS-001` · Draw Reimu's lines as manga speech balloons

Derived stage: **complete**.

| Gate | Required | Status | Evidence | Boundary note |
| --- | --- | --- | --- | --- |
| specification | yes | `ready` | [2026-11-11-reimu-manga-balloons.md](../docs/decisions/2026-11-11-reimu-manga-balloons.md) | Four balloon shapes from the maintainer's reference image, the rule that picks one from how a line is said, punctuation-only wrapping, and placement above the head that avoids the status card are written down. |
| implementation | yes | `ready` | [2026-11-11-reimu-manga-balloons.md](../docs/decisions/2026-11-11-reimu-manga-balloons.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/36834509b3780dc0a3ca13342928ef03b8ddd9bb) | SpeechBalloon.swift (click-through window, four shapes, layout), BalloonStyle in PetBehavior.swift and the --render-balloons review sheet are in the published Consumer commit. |
| technical | yes | `passed` | [2026-11-11-reimu-manga-balloons.md](../docs/decisions/2026-11-11-reimu-manga-balloons.md) | 262 behavior and 40 native checks, including every line fitting inside all four outlines at the smallest and largest pet size and the placement cases, passed on the 1.21/build 23 bundle with strict signatures. |
| visual | yes | `approved` | [2026-11-11-reimu-manga-balloons.md](../docs/decisions/2026-11-11-reimu-manga-balloons.md) | With 1.21 and then 1.22 installed and the app-rendered review sheet delivered, the maintainer was asked whether the balloons and the tea break look right and replied "都可以" on 2026-11-11. Approval covers the four shapes and their placement as shipped. |
| consumer | yes | `verified` | [2026-11-11-reimu-manga-balloons.md](../docs/decisions/2026-11-11-reimu-manga-balloons.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/36834509b3780dc0a3ca13342928ef03b8ddd9bb) | Installed as 1.21/build 23; the window list showed the balloon window appear with the launch greeting and disappear about three seconds later. |
| publication | yes | `published` | [2026-11-11-reimu-manga-balloons.md](../docs/decisions/2026-11-11-reimu-manga-balloons.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/36834509b3780dc0a3ca13342928ef03b8ddd9bb) | Published with the dialogue work in the same Consumer commit on origin/main. No tag or release. |

<a id="reimu-night-sleep-001"></a>
## `REIMU-NIGHT-SLEEP-001` · Sleeping at the low table late at night, with rules for falling asleep and waking

Derived stage: **complete**.

| Gate | Required | Status | Evidence | Boundary note |
| --- | --- | --- | --- | --- |
| specification | yes | `ready` | [2026-11-11-reimu-dialogue-and-action-design.md](../docs/decisions/2026-11-11-reimu-dialogue-and-action-design.md), [2026-11-11-reimu-night-sleep.md](../docs/decisions/2026-11-11-reimu-night-sleep.md) | Row 7 of the action roadmap. When she falls asleep, every way she wakes, pause, reduced motion, mute and the menu switch are written down, including two choices that differ from earlier notes (on by default; sleeps under reduced motion). The maintainer answered "做" on 2026-11-11. |
| implementation | yes | `ready` | [2026-11-11-reimu-night-sleep.md](../docs/decisions/2026-11-11-reimu-night-sleep.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/eb978dc6685371b4a3894e5326c0b2fca8c57125) | The night_sleep-v1 package (the September drawings, byte-identical, with the approval record), PetAction.nightSleep and nightWake, the menu switch, the --night-sleep build input, its package test and the gate rule are in the published Consumer commit. |
| technical | yes | `passed` | [2026-11-11-reimu-night-sleep.md](../docs/decisions/2026-11-11-reimu-night-sleep.md) | 334 behavior checks (23 new), 46 native checks (2 new), 4 package checks, every other package test, the repository gate and strict signatures passed on the installed 1.26/build 28 bundle. |
| visual | yes | `approved` | [2026-11-11-reimu-night-sleep.md](../docs/decisions/2026-11-11-reimu-night-sleep.md) | With the review GIF delivered and the rules, the two designer choices and the weak spots listed, the maintainer replied "可以，安装" on 2026-11-11. The GIF was an offline composite; the feature first shows after 23:00 and twenty quiet minutes, and reduced motion was on at install, so it has not been seen on screen. |
| consumer | yes | `verified` | [2026-11-11-reimu-night-sleep.md](../docs/decisions/2026-11-11-reimu-night-sleep.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/eb978dc6685371b4a3894e5326c0b2fca8c57125) | Installed as 1.26/build 28, built from the sources later published unchanged; the installed loader reports sleep_reason none and sleep_frames 5. |
| publication | yes | `published` | [2026-11-11-reimu-night-sleep.md](../docs/decisions/2026-11-11-reimu-night-sleep.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/eb978dc6685371b4a3894e5326c0b2fca8c57125) | The exact Consumer commit is on origin/main; the maintainer answered "提交并推送" on 2026-11-11. No tag or release. |

<a id="reimu-poof-bridge-001"></a>
## `REIMU-POOF-BRIDGE-001` · Smoke display bridge between pose families

Derived stage: **complete**.

| Gate | Required | Status | Evidence | Boundary note |
| --- | --- | --- | --- | --- |
| specification | yes | `ready` | [2026-11-11-reimu-poof-display-bridge.md](../docs/decisions/2026-11-11-reimu-poof-display-bridge.md) | A display bridge under the frozen transition specification's own definition: when it appears, when it never does, its five 80 ms steps and that the behavior model is not delayed. It closes no gate of REIMU-WORK-TRANSITIONS-001. |
| implementation | yes | `ready` | [2026-11-11-reimu-poof-display-bridge.md](../docs/decisions/2026-11-11-reimu-poof-display-bridge.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/cb160884b5d8d43a9511f66938018345552aef9c) | The poof-v1 effect package (re-exported with the approval record), DisplayBridge and PoseFamily, the overlay drawing, the menu toggle, the optional --poof build input, its package test and the gate rule are in the published Consumer commit. |
| technical | yes | `passed` | [2026-11-11-reimu-poof-display-bridge.md](../docs/decisions/2026-11-11-reimu-poof-display-bridge.md) | 292 behavior checks including the five bridge rules, 42 native and 4 package checks and strict signatures passed on the installed 1.23/build 25 bundle; the full cloud hides 89.6-97.7% of each family's silhouette. |
| visual | yes | `approved` | [2026-11-11-reimu-poof-display-bridge.md](../docs/decisions/2026-11-11-reimu-poof-display-bridge.md) | The maintainer replied "都可以，安装" on 2026-11-11 after the review GIF, which is a Python composite on the runtime timing and not a recording of the app. Reduced motion was on at install, so the bridge may not have been seen on screen. It closes no gate of REIMU-WORK-TRANSITIONS-001. |
| consumer | yes | `verified` | [2026-11-11-reimu-poof-display-bridge.md](../docs/decisions/2026-11-11-reimu-poof-display-bridge.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/cb160884b5d8d43a9511f66938018345552aef9c) | Installed as 1.23/build 25; the installed loader reports poof_reason none and poof_frames 4. |
| publication | yes | `published` | [2026-11-11-reimu-poof-display-bridge.md](../docs/decisions/2026-11-11-reimu-poof-display-bridge.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/cb160884b5d8d43a9511f66938018345552aef9c) | The exact Consumer commit is on origin/main; the maintainer agreed to install, commit and push in the same reply. No tag or release. |

<a id="reimu-props-offering-box-intake-001"></a>
## `REIMU-PROPS-OFFERING-BOX-INTAKE-001` · Prepare the offering box and coin props for standing scenes

Derived stage: **blocked**.

| Gate | Required | Status | Evidence | Boundary note |
| --- | --- | --- | --- | --- |
| specification | yes | `ready` | [2026-11-10-reimu-props-offering-box-intake.md](../docs/decisions/2026-11-10-reimu-props-offering-box-intake.md) | A script-drawn offering box beside the standing pose on the shoe line, plus a movable coin; shown only in standing scenes. |
| implementation | yes | `ready` | [2026-11-10-reimu-props-offering-box-intake.md](../docs/decisions/2026-11-10-reimu-props-offering-box-intake.md) | Prop images and a composited mock-up exist under build/reimu-props-v1; no runtime code exists. |
| technical | yes | `passed` | [2026-11-10-reimu-props-offering-box-intake.md](../docs/decisions/2026-11-10-reimu-props-offering-box-intake.md) | The box is on the 596 canvas, rests on the shoe line and overlaps no opaque pixel of the standing figure. No runtime or interaction test exists yet. |
| visual | yes | `rejected` | [2026-11-10-reimu-props-offering-box-intake.md](../docs/decisions/2026-11-10-reimu-props-offering-box-intake.md), [2026-11-10-reimu-cuter-standing-study.md](../docs/decisions/2026-11-10-reimu-cuter-standing-study.md) | The user replied "有点怪异" on 2026-11-10. The script-drawn flat style does not sit with the character art; props should come from the same image source as the character. |
| consumer | no | `not_required` | [2026-11-10-reimu-props-offering-box-intake.md](../docs/decisions/2026-11-10-reimu-props-offering-box-intake.md) | Intake only; the click-to-donate interaction needs a separate runtime task. |
| publication | no | `not_required` | [2026-11-10-reimu-props-offering-box-intake.md](../docs/decisions/2026-11-10-reimu-props-offering-box-intake.md) | Local review candidate. |

<a id="reimu-scene-reactions-001"></a>
## `REIMU-SCENE-REACTIONS-001` · Scene-aware click reactions, Reimu-voiced lines, and plain standing idle

Derived stage: **complete**.

| Gate | Required | Status | Evidence | Boundary note |
| --- | --- | --- | --- | --- |
| specification | yes | `ready` | [2026-11-10-reimu-scene-reactions-and-idle.md](../docs/decisions/2026-11-10-reimu-scene-reactions-and-idle.md) | Reaction words follow the scene on screen; light clicks never cut away from a work meal; idle only stands unless the user opts back in. |
| implementation | yes | `ready` | [2026-11-10-reimu-scene-reactions-and-idle.md](../docs/decisions/2026-11-10-reimu-scene-reactions-and-idle.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/2c62a77067d53746824946eeeb4c6c8ff2522175) | PetScene, PetLines, held work artwork during light reactions, idleAutonomy and its menu toggle exist in the published Consumer commit. |
| technical | yes | `passed` | [2026-11-10-reimu-scene-reactions-and-idle.md](../docs/decisions/2026-11-10-reimu-scene-reactions-and-idle.md) | 217 behavior, 37 native AppKit, 31 status, per-tier loader and fallback checks and strict signatures passed on the 1.16/build 18 bundle. |
| visual | yes | `approved` | [2026-11-10-reimu-scene-reactions-and-idle.md](../docs/decisions/2026-11-10-reimu-scene-reactions-and-idle.md), [2026-11-10-reimu-props-offering-box-intake.md](../docs/decisions/2026-11-10-reimu-props-offering-box-intake.md) | The user replied "差不多" on 2026-11-10 after using the installed lines; individual lines may still be revised on request. |
| consumer | yes | `verified` | [2026-11-10-reimu-scene-reactions-and-idle.md](../docs/decisions/2026-11-10-reimu-scene-reactions-and-idle.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/2c62a77067d53746824946eeeb4c6c8ff2522175) | Installed 1.16 runs with the new reactions; idle autonomy is off by default in the production identity. |
| publication | yes | `published` | [2026-11-10-reimu-scene-reactions-and-idle.md](../docs/decisions/2026-11-10-reimu-scene-reactions-and-idle.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/2c62a77067d53746824946eeeb4c6c8ff2522175) | The maintainer asked to commit and push on 2026-11-10; the exact Consumer commit was verified on origin/main. No tag or package release is implied. |

<a id="reimu-standing-yawn-001"></a>
## `REIMU-STANDING-YAWN-001` · Standing yawn for sleepy clicks and late greetings

Derived stage: **complete**.

| Gate | Required | Status | Evidence | Boundary note |
| --- | --- | --- | --- | --- |
| specification | yes | `ready` | [2026-11-11-reimu-standing-yawn.md](../docs/decisions/2026-11-11-reimu-standing-yawn.md) | The pose pair, the three event-tied triggers, interruption by any click, reduced motion and isolated fallback are written down; the maintainer asked for it with "画打哈欠". |
| implementation | yes | `ready` | [2026-11-11-reimu-standing-yawn.md](../docs/decisions/2026-11-11-reimu-standing-yawn.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/cb160884b5d8d43a9511f66938018345552aef9c) | The yawn-v1 pose table (re-exported with the approval record), PetAction.yawn, greet(yawn:), the optional --yawn build input, its package test and the gate rule are in the published Consumer commit. |
| technical | yes | `passed` | [2026-11-11-reimu-standing-yawn.md](../docs/decisions/2026-11-11-reimu-standing-yawn.md) | Harness 0.8.0 validation, pixel gates (zero changed pixels outside the two take rectangles, unchanged opaque bounds and shoe line, 913-1477 px changed at 160 px), 292 behavior, 42 native and 4 package checks and strict signatures passed on the installed 1.23/build 25 bundle. |
| visual | yes | `approved` | [2026-11-11-reimu-standing-yawn.md](../docs/decisions/2026-11-11-reimu-standing-yawn.md) | With the side-by-side review GIF delivered, the maintainer replied "都可以，安装" on 2026-11-11. Approval was given from the GIF before installation; reduced motion was on at install, so on-screen playback may not have been seen. |
| consumer | yes | `verified` | [2026-11-11-reimu-standing-yawn.md](../docs/decisions/2026-11-11-reimu-standing-yawn.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/cb160884b5d8d43a9511f66938018345552aef9c) | Installed as 1.23/build 25; the installed loader reports yawn_reason none and yawn_frames 4. |
| publication | yes | `published` | [2026-11-11-reimu-standing-yawn.md](../docs/decisions/2026-11-11-reimu-standing-yawn.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/cb160884b5d8d43a9511f66938018345552aef9c) | The exact Consumer commit is on origin/main; the maintainer agreed to install, commit and push in the same reply. No tag or release. |

<a id="reimu-tea-break-001"></a>
## `REIMU-TEA-BREAK-001` · Tea break at the low table after a round of work

Derived stage: **complete**.

| Gate | Required | Status | Evidence | Boundary note |
| --- | --- | --- | --- | --- |
| specification | yes | `ready` | [2026-11-11-reimu-dialogue-and-action-design.md](../docs/decisions/2026-11-11-reimu-dialogue-and-action-design.md), [2026-11-11-reimu-tea-break.md](../docs/decisions/2026-11-11-reimu-tea-break.md) | The action, its trigger (working to round-ended only), its end, click behaviour, reduced motion and isolated fallback are written down; the maintainer asked for it with "画收工茶". |
| implementation | yes | `ready` | [2026-11-11-reimu-tea-break.md](../docs/decisions/2026-11-11-reimu-tea-break.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/4dc36a9950a8a9a50f009e30a498cf4d046f7c16) | The tea_break-v1 package (48 frames), PetScene.tea, PetArtwork.teaBreak, the optional --tea-break build input, its package test and the repository gate are in the published Consumer commit. |
| technical | yes | `passed` | [2026-11-11-reimu-tea-break.md](../docs/decisions/2026-11-11-reimu-tea-break.md) | Harness 0.8.0 validation of the full and reduced builds, the pixel gates (zero changed pixels outside the take rectangle against the approved task_3 still, unchanged opaque bounds, 1179-1458 px changed at 160 px), 274 behavior, 41 native and 5 package checks and strict signatures passed on the 1.22/build 24 bundle. |
| visual | yes | `approved` | [2026-11-11-reimu-tea-break.md](../docs/decisions/2026-11-11-reimu-tea-break.md) | With 1.22 installed and the side-by-side review GIF delivered, the maintainer replied "都可以" on 2026-11-11. Approval covers the three poses and the loop as shipped, with the weak spots listed in the record; reduced motion was on at the time, so on-screen playback may not have been seen. |
| consumer | yes | `verified` | [2026-11-11-reimu-tea-break.md](../docs/decisions/2026-11-11-reimu-tea-break.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/4dc36a9950a8a9a50f009e30a498cf4d046f7c16) | Installed as 1.22/build 24; the installed loader reports tea_break_reason none and all five tiers none. |
| publication | yes | `published` | [2026-11-11-reimu-tea-break.md](../docs/decisions/2026-11-11-reimu-tea-break.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/4dc36a9950a8a9a50f009e30a498cf4d046f7c16) | The exact Consumer commit is on origin/main under the maintainer's delegation. No tag or release. |

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

<a id="reimu-waiting-slouch-001"></a>
## `REIMU-WAITING-SLOUCH-001` · Slouch at the low table while the observed work waits for input

Derived stage: **visual review**.

| Gate | Required | Status | Evidence | Boundary note |
| --- | --- | --- | --- | --- |
| specification | yes | `ready` | [2026-11-11-reimu-dialogue-and-action-design.md](../docs/decisions/2026-11-11-reimu-dialogue-and-action-design.md), [2026-11-11-reimu-waiting-slouch.md](../docs/decisions/2026-11-11-reimu-waiting-slouch.md) | Listed in the action design as the one change that needs no new art; when it shows, clicks, reduced motion, the fallback without the clip and the bridge rule are written down. The maintainer answered "做" on 2026-11-11. |
| implementation | yes | `ready` | [2026-11-11-reimu-waiting-slouch.md](../docs/decisions/2026-11-11-reimu-waiting-slouch.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/05cde7d29f6dca97b7e1c600546227c66e09f5d6) | presentation(waitSlouchAllowed:), the host flag and the tests are in the published Consumer commit; no asset was added or changed. |
| technical | yes | `passed` | [2026-11-11-reimu-waiting-slouch.md](../docs/decisions/2026-11-11-reimu-waiting-slouch.md) | 301 behavior checks (9 new), 43 native checks (1 new), every package test, the repository gate and strict signatures passed on the installed 1.24/build 26 bundle. |
| visual | yes | `in_review` | [2026-11-11-reimu-waiting-slouch.md](../docs/decisions/2026-11-11-reimu-waiting-slouch.md) | The slouch loop itself is approved art; its use for the waiting state has not been seen by the maintainer, and no screen capture was possible. |
| consumer | yes | `verified` | [2026-11-11-reimu-waiting-slouch.md](../docs/decisions/2026-11-11-reimu-waiting-slouch.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/05cde7d29f6dca97b7e1c600546227c66e09f5d6) | Installed as 1.24/build 26, built from the sources later published unchanged; the installed loader reports slouch_reason none. |
| publication | yes | `published` | [2026-11-11-reimu-waiting-slouch.md](../docs/decisions/2026-11-11-reimu-waiting-slouch.md), [remote](https://github.com/lyw-ops/gensokyo-codex-pets/commit/05cde7d29f6dca97b7e1c600546227c66e09f5d6) | The exact Consumer commit is on origin/main; the maintainer answered "提交并推送" on 2026-11-11. No tag or release. |

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
