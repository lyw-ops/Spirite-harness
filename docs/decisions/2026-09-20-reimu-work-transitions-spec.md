# Reimu workload-transition specification freeze

Date: 2026-09-20

This decision closes only the specification gate of
`REIMU-WORK-TRANSITIONS-001`. It does not provide transition artwork, a
transition manifest, a runtime node, a native preview, visual approval,
consumer integration, installation, commit, or publication. The approved
direct switch remains the complete production fallback until each later gate
has its own evidence.

## Verified baseline

The specification was checked against Harness
`37d9384cc91ef3b3f0c349405d15f174f7c66c2f` and Consumer
`c2684cc3fecbdfbe0ae238a13f8e22fef333295d`; both local `main` refs matched
`origin/main` after fetch and both worktrees were clean before this draft.

| Endpoint | Approved package | Frames / playback | Endpoint SHA-256 | Source-manifest SHA-256 |
| --- | --- | --- | --- | --- |
| `standing_v1` | `neutral_standing_v1/idle_blink` | 140 at 20 fps, 7 s loop | frame 0/base `4b390982469cedbc3b1a0b3792c49a686e2b87b7dda6e5ab12d7bc73cd3e75e7` | `85ef36b41e6c57305984525998a16887013aa5e5be6231453df60e4b46677496` |
| `tier_1_v1` | `task_1-static-v1` | one 125 ms frame, static hold | `8dd9ff95bcfc2a891c997564496097328ec800d83b887ed08b54a608fe410e0e` | `ad9e4b9887359df3d2567d434ab169993b33e5026578e50351a0722c0624b84f` |
| `tier_2_v1` | `task_2-chew-v9` | 16 frames at 10 fps, 1.6 s loop | frame 0/base `0251947e0ca94f0ba0fa4b724d37fac242c86ba4de9591bb558c226ad4904cfe` | `81aa07c5503150f634a0b6e267f9621147f6f6a275e25b79b6c41e7ef1d447de` |
| `tier_3_v1` | `task_3-static-v1` | one 125 ms frame, static hold | `45c212c88bd39053bb351d5f7bdf8da5d1a95ca743c532232290288927a2a9ff` | `17909602578f8c961480f9d7aaf0fce19b732c859bb107dfdc05a28a197540bc` |
| `tier_4_v1` | `task_4-static-v1` | one 125 ms frame, static hold | `9f0b18946eca4c7c0d27a8dbbd5f966da615867913d8e91c8454dd629de0b238` | `c187f8d4390d4f082001c599dab6d2dbd8e699662c9a42cbe84bed9cd3300221` |
| `tier_5_v1` | `task_5-static-v1` | one 125 ms frame, static hold | `ffd3752c4cdf333a88dc70e766dc4fbdf584662bb242365b3a3ff8a2860f8342` | `0b48b3730b2b26e6043af5a229bd0033fc6b97615e1d67dc14a4897cc4fd9a3f` |

The five runtime manifests and files were re-read rather than inferred from
earlier receipts. Tier 2 remains the only substantive multi-frame workload
animation. Tiers 1, 3, 4, and 5 are digest-pinned stills and must not be called
completed eating animations.

`ReimuFoodTier = min(max(activeTaskCount, 0), 5)` remains the sole count policy
boundary. The uncapped observed count remains provider truth. Transition
selection consumes an already resolved tier and must not contain count tests,
named workload bands, or a second `>= 5` rule.

## Logical transition matrix

Endpoint tokens are `standing`, `tier_1`, `tier_2`, `tier_3`, `tier_4`, and
`tier_5`. `standing` also names the existing safe fallback presentation; it
does not claim that a missing tier resource exists.

The following are independent logical route identities:

- entry: `standing_to_tier_1` through `standing_to_tier_5`;
- exit: `tier_1_to_standing` through `tier_5_to_standing`;
- cross-tier: every ordered pair `tier_i_to_tier_j` where `i != j`, for 20
  directed identities.

Direction is semantic. An entry clip is not automatically an exit clip played
backward, and `tier_i_to_tier_j` is not interchangeable with
`tier_j_to_tier_i`. Reversal is allowed only when a future manifest names the
source resource in `reverse_of`, both endpoint bindings still match exactly,
and the reversed timing and body mechanics receive their own visual approval.

These 30 route identities do not create 30 implemented states. A route becomes
available only when a digest-pinned package exists and passes later gates. The
runtime must keep an absent route absent and use the current direct switch.

### Resource sharing

Two route identities may refer to one visual resource only when all of the
following are evidenced:

1. their authored start poses bind to the same endpoint ID, decoded RGBA,
   placement, scale, and support line;
2. their authored end poses bind to the same endpoint ID, decoded RGBA,
   placement, scale, and support line;
3. their direction, duration, cancel points, and reduced-motion destination
   are the same;
4. native-size review explicitly covers every logical route that names the
   shared resource.

Sharing because two branches are convenient in code is forbidden. The current
Tier endpoints are visually and digest-distinct, so this freeze pre-authorizes
no cross-tier visual sharing. The five entry routes may share controller code,
and the five exit routes may share controller code, but not art. A future
common authored bridge is possible only after its identical bridge endpoint is
itself frozen and approved. A recovery path may reuse an entry resource only
when the action's actual last rendered pose is the entry resource's exact
`from_endpoint`; otherwise recovery switches directly or uses a separately
authored recovery route.

## Timing, cancellation, and arbitration

The state observer remains authoritative throughout a transition. There is no
transition queue and no restoration of a captured old target.

### Normal path rules

- **Enter work:** from the exact standing/fallback representative pose, start
  a valid `standing_to_tier_i` resource immediately. If it is unavailable or
  invalid, switch directly to the latest tier exactly as today.
- **Leave work:** a static Tier 1/3/4/5 may start its valid exit immediately;
  no artificial loop wait is added. A valid normal Tier 2 exit starts only at
  the next 1.6-second safe loop boundary. When no valid exit resource exists,
  the approved current direct-switch behavior is preserved.
- **Cross-tier:** leaving Tier 2 for an ordinary count change waits for the
  current 1.6-second boundary. Leaving a static Tier adds no wait. At that
  decision point the runtime reads the newest observed tier and uses only the
  matching valid directed route; otherwise it switches directly.
- **Recover after interaction:** when an interaction ends, read the latest
  state and uncapped count, resolve the current tier once through the existing
  policy, and use a transition only if the action's actual terminal pose
  exactly matches that resource's declared start endpoint. Never resume a
  pre-interaction tier or transition.

An implementation may determine that a package is unavailable before a Tier 2
boundary; it must not add a wait merely to discover that it will fall back.

### Cancellation

- Failure, `needs_input`, click, drag, pause, system suspension, and any other
  higher-priority state take the body immediately. They do not wait for a Tier
  loop boundary, transition cancel marker, or transition end.
- Every authored frame boundary is a normal cancellation point. A task-count
  or ordinary work-state change during a transition is applied at the next
  frame boundary or at the transition end, whichever comes first.
- At a normal cancellation point, discard the old target, re-read the newest
  observed state, and resolve it afresh. Do not enqueue the old route, play a
  reverse route from an unbound intermediate pose, or replay the interrupted
  route later.
- If the new target has no transition whose `from_endpoint` is the exact
  current pose, use the current direct switch. Correct state and bounded
  latency take precedence over inventing continuity.
- A completed transition hands off to the declared target representative
  frame, then starts that target's normal playback clock. Tier 2 therefore
  continues from frame 0 into its approved 10 fps loop rather than restarting
  an already elapsed hidden loop.

### Reduced motion and failure isolation

Reduced motion never plays a dynamic transition. It directly selects the
target tier's declared representative frame: frame 0 for Tiers 1–5 and the
approved standing open pose for standing/fallback. It does not freeze an
intermediate transition frame.

Missing files, unreadable PNGs, manifest identity changes, endpoint-summary
mismatches, frame-summary mismatches, invalid ordering, or load failures
disable only that directed route. The fallback is the existing direct switch.
No transition failure may disable a workload tier, standing, manual feeding,
slouch, click reactions, drag handling, failure, waiting, or another valid
transition.

## Artwork and package contract

### Immutable endpoints and prohibited substitutes

All approved standing, Tier 1–5, and Tier 2 loop files are immutable inputs.
They may not be overwritten, repainted, split, stretched, re-encoded, or moved
in place. Derived endpoint receipts live in a new transition package and never
replace the source.

Whole-character, table, food, or tatami translation, rotation, scaling,
shaking, cross-dissolve, or opacity pulsing is not an authored character
transition. A plain cut or fade may be used later as an honestly labelled
`display_bridge`, but it never closes the authored-character visual gate. The
historical `build/reimu-idle-meal-transition-20260907-v1/cut/` is useful only
as evidence about placement and direct display switching. Its pixels are not
approved workload-transition source and must not be copied into a new package.

An `authored_character_transition` must come from separately supplied and
approved original poses or explicit layers. Character motion must be expressed
through pose and local body-part changes. Fixed scene elements remain fixed
unless an authored scene change is itself visible and approved.

### Names and directories

For a future route `<transition_id>`:

```text
pets/reimu/animations/work_transitions/sources/<transition_id>-v1/
  source.json
  originals/                 # original pose or layer inputs; never derived endpoint copies
  frames/frame_000.png ...   # approved exact 596 x 596 RGBA sequence

assets/reimu/work_transitions/<transition_id>/
  animation.json
  base.png
  frames/frame_000.png ...
```

`transition_id` is one of the frozen logical IDs above. Version suffixes belong
to the source-package directory, not to the identity. A package for a cut or
fade uses a different `resource_kind` and cannot occupy an
`authored_character_transition` path while claiming authored motion.

### Required manifest fields

`source.json` must contain:

- `exact_frame_source_version`, `character: "reimu"`,
  `state_set: "work_transitions"`, `transition_id`, `resource_id`, and
  `resource_kind` (`authored_character_transition` or `display_bridge`);
- `canvas: {width: 596, height: 596, mode: "RGBA"}`;
- `playback` with fixed `fps`, `frame_count`, `duration_ms`, and `loop: false`;
- ordered `frames`, each with zero-padded contiguous file name,
  `duration_ms`, and SHA-256;
- `from_endpoint` and `to_endpoint`, each with endpoint ID, source-manifest
  path and SHA-256, representative-frame path and SHA-256, canonical placement,
  uniform scale, and support-line binding;
- `cancel_points`, containing every frame boundary;
- `reduced_motion: {mode: "target_representative_frame", endpoint: ...}`;
- `constraints` declaring no hidden resampling, no non-uniform scale, and no
  whole-scene transform used as character motion;
- `provenance` naming the original pose/layer sources, authoring method,
  creator or provider, permission, and approval state;
- `approval`, initially pending, with no invented approver or date.

The generated `animation.json` repeats the runtime-authoritative playback,
endpoint, reduced-motion, frame, digest, and provenance bindings and records
the exact source-manifest SHA-256. Frame order is manifest order, never file
system discovery order.

All transition frames are 596×596 RGBA. Scale is uniform and explicit. Native
placement is measured against the approved standing shoe line
`1230 / 1254`; on the 596 reference canvas this is approximately y=584.59.
Tier endpoint support edges remain their approved values (Tier 2: 585/596;
Tier 3: 585/596; Tiers 1/4/5: 586/596). Existing footprint differences remain visible; no
per-tier hidden resampling may disguise them. The manifest binds both endpoint
placements and a per-frame support policy, and native review must expose any
intended lift or contact change rather than normalize it away.

### Endpoint equality

The default requirement is decoded-RGBA equality at both ends:

- the first transition frame equals the canonical 596×596 render receipt of
  `from_endpoint` pixel for pixel;
- the last transition frame equals the canonical 596×596 render receipt of
  `to_endpoint` pixel for pixel.

The 596×596 Tier endpoints already have byte-exact representatives. Standing
requires a deterministic 596×596 endpoint render receipt from the immutable
1254×1254 approved open pose using the declared uniform placement; producing
that receipt does not modify the standing source.

If an authored bridge genuinely needs a non-identical first or last frame, it
must bind that frame as a transition-only bridge pose and obtain separate
visual approval. Evidence must include endpoint and bridge digests, full-size
and 160 pt side-by-side views, alpha/onion-skin or diff views, support-line and
bounding-box measurements, and a native-timing preview showing no pop. That
approval does not replace or rewrite the approved endpoint.

## First implementation slice: standing/fallback to Tier 2

The first recommended vertical slice is `standing_to_tier_2`, not the full
cross-tier matrix and not both directions at once.

It has the highest value-to-scope ratio because Tier 2 is the only real dynamic
workload loop, its frame 0 is an exact safe seam, and entry is the first visible
moment when observed work changes the character. This slice exercises the new
package, endpoint binding, handoff into a loop, reduced-motion bypass, isolated
fallback, cancellation, and native review without also introducing Tier 2 exit
boundary scheduling or 20 directed cross-tier art problems. `tier_2_to_standing`
is the next slice after entry passes, because it is the best test of the 1.6 s
departure boundary and normal-exit cancellation semantics.

No required source for this slice currently exists. The next round needs:

1. the immutable approved standing open pose and a new deterministic 596×596
   endpoint render receipt;
2. immutable Tier 2 frame 0 and its existing package/manifest digests;
3. newly authored original standing-to-seated Reimu poses or explicit layers,
   including body, head/hair/bow, sleeves/arms/hands, and the contact change;
4. separately controllable table, tatami, and Tier 2 meal layers or authored
   complete frames that keep those scene elements stable;
5. a 6–9 frame sequence at 12 fps (500–750 ms total), `loop: false`, with
   every frame boundary cancellable;
6. `source.json`, exact frame digests, provenance/permission, full/reduced
   Harness validation, and an isolated native review package.

The recommended timing is a constraint for this first slice, not evidence that
frames exist. Its non-goals are exit, Tier 1/3/4/5 entry, any cross-tier route,
runtime count-policy changes, new provider behavior, app installation, and
reuse of historical cut/fade pixels.

### Next-round material checklist

- [ ] Copy neither endpoint nor historical-transition pixels into an
  `originals/` claim; record the immutable endpoint paths and digests as
  references only.
- [ ] Produce and verify the deterministic 596×596 standing endpoint receipt,
  including uniform scale, placement, alpha bbox, and support-line report.
- [ ] Supply newly authored original standing-to-seated poses or explicit
  layers with provenance and permission.
- [ ] Author 6–9 ordered 596×596 RGBA frames at 12 fps without whole-scene
  transform substitutes.
- [ ] Make frame 0 equal the standing endpoint receipt and the last frame equal
  approved Tier 2 frame 0, or collect the separate endpoint-exception evidence
  required above.
- [ ] Write `source.json` with both endpoint bindings, every frame digest,
  `loop: false`, all frame-boundary cancel points, provenance, and reduced
  motion targeting Tier 2 frame 0.
- [ ] Run full and reduced Harness validation without modifying either source
  endpoint.
- [ ] Build only an isolated native preview using simulated snapshots, then
  create the required native-size review media and measurements.

### First-slice acceptance table

| Scenario | Required result |
| --- | --- |
| Valid idle/standing → working count 2 | One authored entry plays once, lands exactly on Tier 2 frame 0, then the approved 10 fps loop continues. |
| Count changes to 4 during entry | At the next frame boundary, discard the Tier 2 target and resolve the latest Tier 4 state; do not resume or queue Tier 2 entry. |
| Count changes above 5 during entry | Resolve Tier 5 through the single capped policy; no route-local threshold is allowed. |
| Failure / `needs_input` / click / drag / pause | Preempt immediately, without waiting for a transition frame or end. |
| Reduced motion | Skip every entry frame and display Tier 2 frame 0 directly. |
| Missing package | Use the current direct standing → Tier 2 switch; Tier 2 itself remains available. |
| Bad manifest or one bad frame digest | Disable only `standing_to_tier_2` and use the same direct switch. |
| Tier 1/3/4/5, manual feed, slouch | Existing behavior and resource availability remain unchanged. |
| Preview state source | Read only the isolated fixture; prove that no real provider path was read or written. |
| Native visual review | Show real-time timing plus 596 and 160 pt light/dark evidence with endpoint, bbox, scale, and support checks; automated QA alone cannot approve it. |

## Required future tests

Implementation and consumer gates remain pending until tests cover all of the
following:

- Tier 2 ordinary departure waits for its 1.6 s safe loop boundary when a
  valid authored route is used;
- static Tier 1/3/4/5 departure adds no artificial wait;
- all Tier 1–5 target selections, with a single count policy and counts at or
  above five still capped to Tier 5;
- failure, `needs_input`, click, drag, pause, suspension, and other
  high-priority events preempt immediately;
- a count or work-state change during a transition resolves the latest state
  at the next cancellation point and never resumes an obsolete target;
- reduced motion directly selects the target representative frame;
- one missing transition file, bad manifest digest, or bad frame digest
  disables only that route and preserves the current direct switch;
- all other tiers, standing, manual feeding, slouch, click reactions, drag,
  waiting, and failure remain usable;
- isolated simulated snapshots and real provider state are never read or
  written by the same preview run.

## Future native preview contract

No preview is produced by this specification-only round. When real art exists,
an independent preview must show, at minimum:

1. standing hold → authored entry → at least two complete Tier 2 loops;
2. interruption near the start, middle, and end by failure, `needs_input`,
   click, drag, and pause;
3. target-count changes during entry, including a latest Tier 4 recovery and a
   count above five resolving to Tier 5;
4. reduced-motion direct entry;
5. missing package, bad manifest digest, and bad frame digest direct fallbacks;
6. an unaffected Tier 1/3/4/5, manual-feed, and slouch sampling;
7. only isolated snapshot fixtures, with an explicit assertion that no real
   provider path was opened or written.

Review media must include real-time native playback, a frame/contact sheet,
596 pt or pixel output, 160 pt Retina output on light and dark backgrounds, and
endpoint/support overlays. It must report alpha bounding boxes, support-line
measurements, scale/placement, endpoint pixel equality, frame timing, package
and preview digests, and any deliberate transition-only endpoint exception.
Automated validity cannot approve motion, and a fabricated hold or no-art
preview cannot satisfy this contract.

## Gate result

| Gate | Status after this decision | Boundary |
| --- | --- | --- |
| specification | ready | Matrix, identity, arbitration, source contract, first slice, tests, and preview evidence are frozen here. |
| implementation | pending | No authored transition source, frames, manifest, or runtime node exists. |
| technical | pending | No transition package or implementation has been validated. |
| visual | pending | No transition has been previewed or approved. |
| consumer | pending | The Consumer still uses the approved direct-switch implementation. |
| publication | unpublished | This is an uncommitted local specification draft. |
