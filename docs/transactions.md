# Generation/export publication and recovery

M2/M3's `.render-transaction` protocol is retained. Generation uses
`BUILD/.generation-transaction`; atlas uses sibling
`.OUTPUT_NAME.export-transaction` so interruption remains detectable even
while the output directory is absent. Markers are created exclusively before
staging. A build generation writer also owns the render lock: generation and
render never publish concurrently. Consumers reject any active marker.

Generation and export stage a **complete directory**. Publication renames the
old directory to `previous`, then `new` to the output. Every successful move
is reversed on failure. Rollback or cleanup failure preserves recovery
materials and blocks consumers. Hard process exits retain the marker. Unknown
files, symlinks (including parents/dangling links), nonregular files, source
overlap and hard-link aliases abort; nothing unknown is deleted.

After stopping the writer, preserve the complete directory and transaction.
Restore `previous` as one complete output (move any displaced output aside),
or inspect the fully published new directory if cleanup alone failed. Move
the marker aside only after restoring a complete set, then run validate or
validate-export. Never erase a marker merely to bypass validation. Generation
also leaves a render marker after forced exit; both must be recovered.

Generation inputs and export specifications are captured before validation
and normalization using file bytes and stat identity. Export validation also
captures its output artifacts before reading the configuration; discovered
build inputs are added without replacing earlier identities. Inputs are
checked after normalization/validation and immediately before publication.
Generation also verifies that the adapter did not change its request or
reference copies. It checks the complete staging tree before copying accepted
inputs, rejects pre-existing harness-owned destinations and creates input
files exclusively. Undeclared directories and symlinks also fail offline
bundle validation. Validation/export are not atomic snapshots across build
directories. Concurrent mutations detected at these boundaries cancel the
operation. Hostile filesystem races between individual syscalls, arbitrary
adapter code running with the user's filesystem permissions, and power-loss
durability are outside this guarantee. Run only explicitly trusted executables;
the process protocol is not an OS security sandbox.
