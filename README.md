# Alyn SA-MP AutoConnect

A separate Alyn SA-MP Mobile build configured for one server.

- Nickname prompt: first launcher screen after Alyn's required startup/file check.
- Server: 142.132.203.47:16234 (fixed in the launcher).
- SA-MP protocol: 0.3.7.
- The original National-Street-RP-Launcher repository is not modified.

## Build

Use the Actions tab and run **Build Alyn AutoConnect APK**, or push a commit to main. The workflow checks out the pinned Alyn source snapshot, applies the AutoConnect changes, and builds a debug APK. Download **alyn-autoconnect-debug** from the workflow run's Artifacts section.

## Important

The Alyn client hooks GTA: San Andreas Android 2.10 only. You must have the legitimate compatible GTA SA game data installed/available on the device. This repository does not bundle Rockstar game data. The first Alyn startup may also perform its normal game-file/update checks.

Source snapshot: [Fiki-io/alyn-remake](https://github.com/Fiki-io/alyn-remake), pinned to commit 2cbb0757572a3e17aa6b4da82d6c7fcd4327eeb1.
