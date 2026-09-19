# Reimu native Tier 2 and Tier 3 consumer publication

Date: 2026-09-20

The maintainer authorized a reviewed cleanup, commit, and push after approving the
Tier 3 native preview. The coupled Tier 2 dynamic and Tier 3 static vertical slices
were published to the Consumer repository as one atomic commit:

- repository: `https://github.com/lyw-ops/gensokyo-codex-pets`;
- branch: `main`;
- commit: `6a1318257d9bedc2b9a937304ea4b434ca874409`;
- title: `feat: connect Reimu work eating tiers 2 and 3`.

`git ls-remote origin refs/heads/main` returned that exact SHA after the push, and
the Consumer worktree was clean. Before commit, the final source passed 125 tool
tests with the Harness CLI explicitly present, 14 observer/installer bridge tests,
31 state-contract cases, the app runtime and repository gates, `git diff --check`,
and the Tier 2/Tier 3 native package and isolated-fallback checks. The previously
recorded 172 Swift behavior and 34 AppKit checks remain tied to the same Swift
source. A fresh Swift compile could not be repeated after the host Command Line
Tools compiler and SDK moved to different patch versions; that environment boundary
is recorded in the Tier 3 visual-approval decision.

The publication includes the source, tests, exact Tier 3 static package, handoff,
and design/runtime documentation. It does not install the app, publish the local
formal-identity ZIP, create a tag or release, complete Tier 3 multi-frame animation,
or approve the separately tracked work-eating transitions.
