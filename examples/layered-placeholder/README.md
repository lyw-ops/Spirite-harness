# Three-layer geometric placeholder

The example uses a static rectangle (`body`), a rotating triangle (`head`),
a translating/fading circle (`hand`), and global sprite sway. Labels are only
example bindings; the core contains no body-part or character rules. The event
is an annotation. All artwork is generated from simple geometry.

From the repository root, with the current package installed:

```bash
.venv/bin/python scripts/create_layered_placeholder.py /tmp/sprite-m3-demo
.venv/bin/sprite-harness plan --spec /tmp/sprite-m3-demo/animation.json --output /tmp/sprite-m3-demo/build
.venv/bin/sprite-harness render /tmp/sprite-m3-demo/build
.venv/bin/sprite-harness validate /tmp/sprite-m3-demo/build --write-qa
.venv/bin/sprite-harness preview /tmp/sprite-m3-demo/build
.venv/bin/sprite-harness contact-sheet /tmp/sprite-m3-demo/build
.venv/bin/sprite-harness report /tmp/sprite-m3-demo/build

# Reduced variant: freezes every local and global transform at frame 0.
.venv/bin/sprite-harness render /tmp/sprite-m3-demo/build --reduced-motion --overwrite
.venv/bin/sprite-harness validate /tmp/sprite-m3-demo/build --write-qa
.venv/bin/sprite-harness preview /tmp/sprite-m3-demo/build
.venv/bin/sprite-harness contact-sheet /tmp/sprite-m3-demo/build
```

Choose a fresh demo directory; the asset generator refuses replacement.
See [the layered contract](../../docs/layered-sprites.md) for paths, anchors,
composition and verification. No automatic decomposition, skeleton, AI action
synthesis or atlas exporter is included.
