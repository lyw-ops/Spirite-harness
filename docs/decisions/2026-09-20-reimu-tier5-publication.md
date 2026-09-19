# Reimu Tier5 Consumer source publication

Date: 2026-09-20

The approved Tier5 native static vertical slice is published in Consumer
commit `d2b6bef76d9b5330f5e56a7ee61fbe86c6cdf9ac`. The commit was pushed to
`origin/main`, and `git ls-remote` independently reported the same SHA for
`refs/heads/main`.

The published scope contains the explicit `work_eating_task_5` identity,
five-or-more selection through the existing single capped `ReimuFoodTier`
policy, safe-boundary behavior, immediate higher-priority preemption,
latest-count recovery, the independent byte-pinned one-frame package,
isolated fallback, approved build pin, tests, and handoff documentation.

The published source and runtime frame retain SHA-256
`ffd3752c4cdf333a88dc70e766dc4fbdf584662bb242365b3a3ff8a2860f8342`.
The approved source manifest has SHA-256
`0b48b3730b2b26e6043af5a229bd0033fc6b97615e1d67dc14a4897cc4fd9a3f`.

Publication closes only the Consumer Git source gate. No application was
installed, no tag or package release was created, and the one-frame Tier5 hold
is still not a completed eating animation.
