# Reimu Tier 4 consumer source publication

Date: 2026-09-20

The approved Tier 4 native static vertical slice is published in Consumer
commit `aa820f07a1352f5e9291548f08187e408aada5bd`. The commit was pushed to
`origin/main`, and `git ls-remote` independently reported the same SHA for
`refs/heads/main`.

The published scope contains the explicit `work_eating_task_4` identity, exact
count-four selection through the existing single `ReimuFoodTier` policy,
safe-boundary behavior, immediate higher-priority preemption, latest-count
recovery, the independent byte-pinned one-frame package, isolated fallback,
build pin, tests, and handoff documentation.

The published source and runtime frame retain SHA-256
`9f0b18946eca4c7c0d27a8dbbd5f966da615867913d8e91c8454dd629de0b238`.
The approved source manifest has SHA-256
`c187f8d4390d4f082001c599dab6d2dbd8e699662c9a42cbe84bed9cd3300221`.

Publication closes only the Consumer Git source gate. No application was
installed, no tag or package release was created, and the one-frame Tier 4
hold is still not a completed ramen-eating animation.
