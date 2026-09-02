# Reimu eating-loop Animation Plan example

[`eating-loop.json`](eating-loop.json) is an example **Animation Plan** for the
`work_eating` state of the [gensokyo-codex-pets](https://github.com/lyw-ops/gensokyo-codex-pets)
Reimu desktop pet. It demonstrates the declarative intermediate representation
without any character logic in the harness itself: everything Reimu-specific
lives in this plan and in its free-form `metadata`.

No artwork is included. The plan declares its own 192×208 canvas (one cell of
that project's sprite-atlas contract), so it expands without a source image; a
real run would pass the base sprite explicitly:

```bash
sprite-harness plan --spec examples/reimu-eating/eating-loop.json \
  --source path/to/reimu-base.png \
  --output examples/reimu-eating/build/
sprite-harness validate examples/reimu-eating/build/
```

Without `--source`, `plan` still normalizes, validates, and expands the plan
into a deterministic frame plan — useful for reviewing motion before any
rendering exists.

## What the plan encodes

- **Breathing** — a 1.5 px sine on the whole sprite, one cycle per loop.
- **Head motion** — a 1 px mirrored ease on the head, two cycles, slightly
  out of phase with the hand.
- **Eating hand** — the right hand rises 1.5 px twice per loop (two bites).
- **Secondary sway** — a 0.5 px horizontal whole-sprite sine; deliberately
  restrained.
- **Blink** — a discrete `blink` event on frames 5–6.
- **Chewing** — `mouth_chew` events aligned with the hand cycle.
- **Constraints** — total offset ≤ 4 px, frame-to-frame change ≤ 2 px.
- **Reduced motion** — runtimes should hold the first frame.

Breathing and sway target the reserved `sprite` label because they move the
whole sprite: only such tracks contribute to the aggregate per-frame `offset`
that the displacement constraints and bbox/ground checks verify. The remaining
`target` values (`head`, `hand_right`, `eyes`, `mouth`) are semantic part
labels for a future layered renderer; they are expanded per frame but never
move the whole-sprite offset, and the harness does not claim a flattened
sprite can be perfectly decomposed into these parts.
