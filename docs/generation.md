# Generation contract v1 (M4)

Generation is an explicit, optional source-space replacement stage. No event,
track, target name, or ordinary command launches a model. The only entry is:

```text
sprite-harness generate BUILD --spec generation.json --adapter-argv '["executable", "arg"]' [--timeout 120] [--overwrite] [--json]
sprite-harness render BUILD --generated-input [--reduced-motion] [--overwrite] [--json]
```

The generation spec has `generation_version: 1`, `request_id`, `adapter`
(`id`, `version`, `model`, JSON `parameters`, `seed_policy`: `required` or
`allow_unsupported`), and nonempty `requests`. Each request has a unique `id`,
an existing `target`, a nonempty distinct `frames` array and `instruction`.
One request means **one PNG explicitly reused for all its listed frames**.
Overlapping target/frame pairs are errors. Single-image plans allow only
`sprite`; layered plans allow only declared ordinary layers. No new layers,
inferred parts, interpolation, resizing, alpha repair, or automatic masking.

`plan.seed` is required for generation. The item seed is the first eight bytes,
big endian, of SHA-256 over UTF-8 canonical JSON of
`["sprite-harness-generation-v1", plan.seed, request_id, item.id, target, sorted_frames]`.
Canonical JSON uses sorted keys, compact separators, Unicode, no NaN/Infinity.
No Python hash, clock, directory or response order enters this calculation.
An unsupported provider seed requires explicit `allow_unsupported`; the
response records the actual capability. Replayable requests do not imply
repeatable stochastic model pixels.

## Data flow and versions

The original generation spec is read-only and remains an accessible identity
dependency. `generation/spec.json` is its byte-for-byte snapshot.
`generation/request.json` is recomputed from that spec plus the verified plan:
it binds the plan digest, spec snapshot path/hash, adapter settings, seed, each item,
source path/hash/dimensions/anchor, fixed PNG/alpha/output size requirements,
and a build-owned source copy in `references/`. Paths resolve from their
descriptor; copied reference paths are relative to request.json.

The external adapter produces `response.json` and candidates. The unmodified
protocol response binds request and item digests, adapter identity, seed
capability, candidate id/file/hash/size and optional provider request id. Its
file paths are relative to the explicit candidate output directory; they
never refer to frames/. Arrival order is immaterial. The core requires exact
one-to-one item coverage, unique candidate ids/paths, readable bounded PNGs,
alpha channels, matching source dimensions and hashes. Fully transparent
layers are legal; the final renderer still rejects empty frames.

Only accepted candidate bytes are copied into `generation/inputs/`.
`generation/accepted.json` binds request/response/spec digests, all accepted
file byte identities, decoded RGBA identities and explicit frame mappings.
Its `spec_source` records the original spec path (relative to accepted.json)
and byte digest; the adapter request itself references only copied local files.
Its content digest is bound by render v2 (`backend: generated-input`,
`generation: {request_digest, accepted_digest}`). Ordinary renders keep
render v1; plan/frame-plan v1/v2, frame-manifest v1 and existing QA v1 stay
compatible. Generation/export QA use v2 with explicit subject bindings.

`generate` success means accepted inputs, **not** validated animation frames.
`render --generated-input` loads only the accepted bundle, replaces pixels
before the existing local/global transform stages, and never invokes an
adapter. All other target/frame pairs use original sources. Missing requested
results fail, never fall back. Hold mode selects frame **0**, using originals
where frame 0 has no mapping, then freezes the complete composite/pose into
byte-identical held PNGs. An arbitrary first returned candidate is never frame 0.

Offline validate rechecks original sources, spec, copied references, request,
response and accepted inputs, then recomputes geometry and final decoded RGBA.
Old deterministic and external-frame verification rules remain in force.
Generation artifacts with a missing render manifest cannot masquerade as
external rendered frames. Reports distinguish backend and motion mode.

Hashes prove binding/integrity and pixel consistency, not visual semantics,
quality, provider authenticity, or authenticity against coordinated replacement
of every trusted input. QA explicitly skips semantic/aesthetic assessment.
Move the complete parent tree to preserve relative paths; moving just a build
requires re-authoring its bindings. Same frozen inputs and runtime yield the
same rendered PNG bytes. Recalling a stochastic model makes no such promise.

See [adapters.md](adapters.md) for the process and live-provider contract and
[transactions.md](transactions.md) for publication/recovery and race boundaries.
