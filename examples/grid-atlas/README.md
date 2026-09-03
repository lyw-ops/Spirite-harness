# Generic fixed grid

After running the example acceptance script into `build/m4-m5-demo`:

```bash
.venv/bin/sprite-harness export --spec examples/grid-atlas/export.json --output build/fixed-atlas
.venv/bin/sprite-harness validate-export build/fixed-atlas
.venv/bin/sprite-harness report build/fixed-atlas
```

Clips appear in the explicit order generated → single → layered. There are
36 frames in 88 cells, leaving 52 transparent cells. The generic grid is
8x11 with 192x208 cells, including 8-pixel inset padding. There is no scaling
or trimming and no claim of compatibility with an untested runtime.
