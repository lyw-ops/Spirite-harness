# Reimu Tier1 Consumer source publication

Date: 2026-09-20

The approved Tier1 native static vertical slice is published in Consumer
commit `c2684cc3fecbdfbe0ae238a13f8e22fef333295d`. The commit was pushed to
`origin/main`, and `git ls-remote` independently reported the same SHA for
`refs/heads/main`.

The published scope contains the explicit `work_eating_task_1` identity,
exact-count-one selection through the existing single capped `ReimuFoodTier`
policy, safe-boundary behavior, immediate higher-priority preemption,
latest-count recovery, the independent byte-pinned one-frame package,
isolated fallback, approved build pin, tests, and handoff documentation.

The published source and runtime frame retain SHA-256
`8dd9ff95bcfc2a891c997564496097328ec800d83b887ed08b54a608fe410e0e`.
The approved source manifest has SHA-256
`ad9e4b9887359df3d2567d434ab169993b33e5026578e50351a0722c0624b84f`.

Publication closes only the Consumer Git source gate. No application was
installed, no tag or package release was created, and the one-frame Tier1 hold
is still not a completed eating animation.
