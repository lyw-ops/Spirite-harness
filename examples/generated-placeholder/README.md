# Explicit generated-input example

All artwork is original programmatic geometry. The supplied adapter is an
**offline test substitute**, not a real model result. Requests replace only
explicit head/hand frame indices and explicitly reuse one candidate per item.

```bash
.venv/bin/python scripts/acceptance_m4_m5.py --output build/m4-m5-demo
```

Inspect `build/m4-m5-demo/generated/build-full/generation/` for normalized
request, response, accepted inputs and generation QA. `build-full` and
`build-hold` contain separate renders, previews and frame QA. `atlas-full`
and `atlas-hold` contain exports with current pixel round-trip checks.

The installed CLI commands and all expected/actual exits are recorded in the
output's commands.json. For real generation, see [adapters.md](../../docs/adapters.md).
