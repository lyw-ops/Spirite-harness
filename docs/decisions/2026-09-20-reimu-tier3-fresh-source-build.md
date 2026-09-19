# Reimu Tier 3 fresh-source production build receipt

Date: 2026-09-20

This receipt closes the local Swift toolchain caveat recorded by the Tier 3
visual-approval and consumer-publication decisions. It does not change the
approved artwork, runtime behavior, consumer commit, or visual scope.

## Toolchain resolution

The selected Command Line Tools installation contains Swift compiler
`swiftlang-6.4.0.34.1`, while its default macOS 27.0 SDK Swift interfaces were
created by `swiftlang-6.4.0.31.4`. That patch mismatch still makes the default
SDK unusable for this build. The same installation also contains macOS 26.5
SDK interfaces created by Swift 6.3.2; the current Swift 6.4 compiler
successfully imported that compatible interface and compiled an AppKit probe.

The production build therefore used:

- the published Consumer source at commit
  `6a1318257d9bedc2b9a937304ea4b434ca874409`;
- `SDKROOT=/Library/Developer/CommandLineTools/SDKs/MacOSX26.5.sdk`;
- isolated Clang and Swift module caches under `/private/tmp`;
- the approved Tier 2 and Tier 3 exact packages, standing, slouch, reaction,
  icon, and 40-frame base package already bound by `desktop/macos/build.py`;
- production mode, without `--preview` and without installing the application.

No system component was installed, updated, or reconfigured.

## Result and verification

The fresh build produced an arm64, macOS 13+ application with identity
`local.reimu.onigiri.desktop`, version 1.10/build 12, and
`PetPreviewBuild = false`. Its executable SHA-256 is
`c4e59cc9311fd25e836f3d7c4bf55c3d2eefc66ad44d6cb09476c75a6f7d0ae0`.

The stable local package is
`build/reimu-tier3-runtime-v1/release/灵梦桌宠-1.10-build12.zip`, SHA-256
`97c4708052e3aff9fe2a93e314446aeed0e16cbe9ee589f10c34450cac00a6d8`.
A new `/private/tmp` extraction passed strict deep signature verification,
retained the production identity, contained the same executable SHA-256, and
reported all bundled assets valid. The previous locally assembled package is
preserved at
`build/reimu-tier3-runtime-v1/release/legacy/灵梦桌宠-1.10-build12-reviewed-binary.zip`,
SHA-256
`6cfab44b193e2d16259d523dddcfc53b20104a6c7dafd8d95e9e3d1d958823e8`.

Verification on the fresh executable passed:

- 172 Swift behavior checks;
- 31 cross-language status-contract cases;
- 3 reaction-loader checks and 5 standing-loader checks;
- 4 Tier 2 package/fallback checks and 4 Tier 3 package/fallback checks;
- built-in asset validation: 40 base frames, 140 standing frames, 140 slouch
  frames, 16 Tier 2 frames, one 125 ms Tier 3 frame, and verified reaction art;
- strict deep signature verification before packaging and after fresh ZIP
  extraction.

This is a local build receipt, not an app installation, tag, GitHub release, or
completion of the still-unbuilt Tier 3 multi-frame animation and authored
work-eating transitions.
