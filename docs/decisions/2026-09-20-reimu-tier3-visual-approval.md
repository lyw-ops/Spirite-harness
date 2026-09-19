# Reimu task_3 native visual approval and production-gate release

Date: 2026-09-20

The user reviewed the native Tier 3 review sheet and GIF delivered from
`build/reimu-tier3-runtime-v1/runtime-preview/` and replied “可以”. This closes
the visual gate for the exact static vertical slice reviewed there.

## Approved subject

- `review-sheet.png` SHA-256:
  `c1855b8766046178b81bef62cb490a38fe4022a6b438a2c81667d6e79c159c7a`.
- `runtime-review.gif` SHA-256:
  `557d7c6f083aec19b7a57c6d70408e17c17861f22ecfabebc74300b3b95fa180`.
- Tier 3 source PNG SHA-256:
  `45c212c88bd39053bb351d5f7bdf8da5d1a95ca743c532232290288927a2a9ff`.
- Reviewed preview's Tier 3 source-manifest SHA-256:
  `eb8a226ae8936205e69044bd146aa4a7a89fb6702d1fe7daf5c16e7c322528d2`.
- Approval covers the displayed native size and pose, the one-frame static
  hold, immediate `needs_input` preemption, and recovery to the latest Tier 2
  count shown by the reviewed artifact.

The approval does not claim or approve a multi-frame Tier 3 animation, authored
entry/exit or cross-tier transitions, installation, commit, push, tag, or release.

## Production gate and local package

The consumer's `desktop/macos/build.py --work-tier-3` no longer requires
`--preview`. It still fails closed on the exact manifest identity, canvas,
playback declaration, frame path, image SHA-256, and source-manifest SHA-256.
After approval, the manifest's approval sentence was updated without changing
any image or playback field. The production source-manifest SHA-256 is
`17909602578f8c961480f9d7aaf0fce19b732c859bb107dfdc05a28a197540bc`.

A source build in non-preview mode passed all resource checks and reached Swift
compilation. Compilation could not run on this host because the installed Command
Line Tools compiler and SDK have different Swift patch versions; the compiler also
could not write its normal user module cache inside the sandbox. This is a local
toolchain condition, not a Tier 3 validation failure.

Because no Swift source changed after the reviewed preview was compiled, the local
formal-identity delivery was assembled from that exact reviewed app. The Tier 3
manifest's approval sentence was refreshed, `CFBundleIdentifier`, `CFBundleName`,
`CFBundleDisplayName`, `PetPreviewBuild`, and the corresponding manifest pin were
changed to the production values, then the copied bundle was stripped of extended
attributes and ad-hoc signed again. The executable and every packaged art resource
otherwise come from the reviewed bundle.

- Package: `build/reimu-tier3-runtime-v1/release/灵梦桌宠-1.10-build12.zip`.
- ZIP SHA-256:
  `6cfab44b193e2d16259d523dddcfc53b20104a6c7dafd8d95e9e3d1d958823e8`.
- Extracted executable SHA-256:
  `c6a136c10f248293967abca2e3b5cb2679080a8d760a66ba45ab2b81d40b6bc0`.
- Extracted identity: `local.reimu.onigiri.desktop`, version 1.10/build 12,
  `PetPreviewBuild = false`.
- A fresh `/private/tmp` extraction passed strict deep code-signature validation.
- Native `--validate-assets` reported Tier 2 as 16 frames with no fallback,
  Tier 3 as one 125 ms frame with no fallback, standing as 140 frames, slouch
  as 140 frames, and the annoyed reaction as verified.

The package is a local delivery artifact. It has not been installed and does not
satisfy the publication gate.
