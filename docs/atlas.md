# Grid atlas export v1 (M5)

```text
sprite-harness export --spec export.json --output DIR [--overwrite] [--json]
sprite-harness validate-export DIR [--json]
sprite-harness report DIR [--json]
```

One implementation packs both single-clip sheets and multi-clip atlases.
The JSON export spec requires `export_version: 1`, `clips` (ordered unique
`id` and `build` path), and `grid` (`cell_width`, `cell_height`, `columns`,
`padding`, optional `rows`). This release takes validated build directories,
including external frames through the existing build contract; it does not
accept directory scans or standalone frame manifests. Paths resolve from
the spec. Inputs must remain available for offline validation.

Cell dimensions include padding. Frame (w,h) is placed at integer (padding,
padding) within its cell; it must fit in
`(cell_width - 2*padding, cell_height - 2*padding)`. No trim, rotation, scale,
extrusion or duplicated frames. Index k occupies column k%columns, row
k//columns. Without explicit rows use ceil(total_frames/columns); explicit
rows must provide enough capacity. Frame and clip order come from the clips
array and trusted frame plan. Empty cells and every unused pixel are RGBA
(0,0,0,0), including hidden RGB. The generic fixed example is 8 columns,
11 rows, 192x208 cells; no runtime compatibility is implied.

The exporter validates every input, records original spec byte identity and
`export-spec.json` snapshot, and writes normalized `export-config.json` with
output-relative build/spec paths and computed rows. `atlas.json` binds the
configuration digest, plan/frame-plan/render byte identities, normalized plan
digest, generated-input request/accepted identities, backend/motion mode,
ordered clips, FPS, loop, per-frame duration, source paths/index/dimensions,
decoded RGBA digest, rect and pivot. Source pivot = normalized anchor*(w,h);
atlas pivot = rect origin + source pivot. Rects cover the entire source canvas.
Output names are fixed: atlas.png, atlas.json, export-spec.json,
export-config.json, export.qa.json. No timestamps or absolute temporary paths.

Source frame PNG file hashes are *observed byte identities*, not pixel
requirements: metadata retains the export-time byte hashes; validation
reports re-encoding separately while comparing current RGBA. Source artwork,
plans, generation inputs and manifests retain strict byte binding. Held frames
still must be byte-identical to one another under the existing build rule.
Atlas PNG re-encoding with identical RGBA is also allowed.

`validate-export` revalidates every build and reconstructs the configuration,
complete metadata and layout independently of atlas.json rects. It crops each
trusted rect and compares all RGBA bytes against each current source frame,
then compares the entire atlas to catch padding/unused-cell defects. It checks
the export QA against a recomputed subject-bound snapshot; QA alone is never
evidence of current validity. Missing inputs, mode changes, stale metadata,
bad pixels or stale QA fail. Report performs current validation.

Limits: at most 4096 clips/65536 total frames, each dimension <=16384,
atlas <=64 million pixels. Integers are strict (booleans/floats rejected).
Unknown fields and invalid capacity/placement fail before publishing.
Repeated export of unchanged inputs in the same runtime is byte-identical.
Input mutation detection and recovery are in [transactions.md](transactions.md).
