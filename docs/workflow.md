# Sprite Harness project workflow

This workflow adapts the useful parts of the KLS project process to animation
engineering: one canonical task ledger, generated progress views, a single
local verification entry point, and evidence that is bound to the exact source
snapshot it evaluated. It does **not** import theorem-specific concepts or
pretend that automated checks can make an artistic judgment.

## Sources of truth

| Concern | Canonical source | Derived or ephemeral evidence |
| --- | --- | --- |
| Product and core protocol | `HARNESS.md` | README summaries |
| Work items and gate states | `workflow/tasks.json` | `workflow/README.md`, `STATUS.md`, `TREE.mmd` |
| Important decisions and corrections | dated files under `docs/decisions/` | handoff summaries |
| Local engineering acceptance | source tree at one snapshot | `build/verification/<run>/report.json` and `latest.json` |
| Artwork approval | explicit human decision tied to preview/source digests | screenshots, contact sheets, or QA files named by that decision |
| Consumer integration | consumer source plus its own test receipt | copied packages or local app installs are not sufficient evidence |
| Publication | exact commit and remote ref | a local commit or local receipt is not a remote publication result |

Generated progress files never become an independent source of status. Build
outputs and `build/verification/` receipts are local evidence unless a
maintainer deliberately promotes a reviewed receipt into a release record.

## The six gates

Every task has all six gate records, but only the gates listed in
`required_gates` determine completion.

1. **Specification** — intent, semantics, source provenance, constraints, and
   reduced-motion behavior are explicit.
2. **Implementation** — the requested source, schemas, code, tests, or authored
   assets exist. “In progress” may include useful partial artifacts; it is not
   completion.
3. **Technical** — deterministic validation passes on the final source
   snapshot. A pass covers only the commands and trust boundary named by the
   receipt.
4. **Visual** — a human approves the actual preview at the intended scale and
   timing. Schema validity, pixel checks, and a contact sheet cannot grant this
   status.
5. **Consumer** — the exact artifact is integrated into the target runtime and
   its selection, interruption, reduced-motion, and fallback behavior are
   verified there. A Harness preview alone cannot grant this status.
6. **Publication** — the intended commit/tag/package has been published and
   its remote identity checked. Commit, push, installation, and release are
   separate actions.

Gate success must name evidence. `not_required` is allowed only where the task
truly has no such boundary; it is not a shortcut around a missing check. The
derived task stage is the first unsatisfied required gate, unless a required
gate is failed, rejected, or blocked.

## Normal work cycle

1. Inspect the repository, current branch, dirty tree, relevant decisions, and
   consumer boundary before editing.
2. Add or update the task in `workflow/tasks.json`. Record dependencies and
   required gates before marking implementation complete.
3. Implement the smallest coherent source change. Source artwork remains
   immutable; generated artifacts stay under `build/` or another declared
   output directory.
4. Run `python workflow/update.py` and inspect the generated table and graph.
5. Run the aggregate local gate with the repository environment:

   ```bash
   .venv/bin/python scripts/verify.py
   ```

   The verifier records commands, logs, Git identity, dirty state, and a digest
   of tracked plus non-ignored untracked source files. It fails if that source
   set changes during the run.
6. If artwork changed, review the full-motion and reduced-motion previews at
   useful desktop scales. Record approval or rejection against exact source or
   artifact digests; do not translate a technical pass into visual approval.
7. Integrate into the consumer only when that task requires it. Record the
   consumer repository, commit/worktree boundary, exact imported artifact, and
   consumer-side tests separately.
8. Before a commit, stage only the intended canonical inputs and regenerate
   progress from the Git index:

   ```bash
   git add <intended source and workflow records>
   .venv/bin/python workflow/update.py --index
   git add workflow/README.md workflow/STATUS.md workflow/TREE.mmd
   .venv/bin/python workflow/update.py --index --check
   ```

   Then rerun the affected validation on the final staged/source snapshot.
9. Commit only under the maintainer's requested scope. Push only after explicit
   push authorization, then compare the remote ref with the local commit.

## Aggregate verification receipt

`scripts/verify.py` runs these local gates without network access or package
installation:

- workflow ledger validation and generated-view consistency;
- whitespace/conflict checks against `HEAD`;
- Python byte-compilation;
- the full pytest suite;
- a source-tree CLI smoke path for layered `plan → render → validate → report`;
- before/after source snapshot equality.

The receipt deliberately does not claim live-provider acceptance, manual
visual approval, consumer-native behavior, installation, code signing, remote
CI, or publication. Those remain their own gates. If a long run observes
source drift, discard the stale result and rerun on a coherent snapshot.

## WIP, release evidence, and corrections

- `build/` is WIP/local evidence and is ignored by Git. Do not cite an old
  `latest.json` after source changes.
- A reviewed release receipt may be copied to a named directory under
  `verification/` together with its trust scope. Promotion is explicit; the
  verifier never publishes evidence automatically.
- Record significant route changes, rejected visual directions, incorrect
  status claims, and compatibility decisions as dated append-only notes under
  `docs/decisions/`. A later correction supersedes an earlier conclusion
  without rewriting what was known at the time.
- `docs/handoff.md` remains a chronological narrative, but the task ledger and
  exact receipts decide current machine-readable status.
