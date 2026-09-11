# Session Problems

**Doc ID**: SNDFRGFX-PROBLEMS

## Open

**SNDFRGFX-PR-0001: Sound Forge 6.0 stalls building peaks files**
- **History**: Added 2026-09-05 18:06
- **Description**: When opening audio files, Sound Forge 6.0 stalls during "Building peaks" phase (visible in status bar). The waveform display appears but the process never completes.
- **Impact**: Cannot work with audio files - application becomes unresponsive during peaks generation
- **Next Steps**: Research Windows 11 compatibility issues with legacy 32-bit apps writing temp/cache files

**SNDFRGFX-PR-0002: Drag and drop files into Sound Forge 6.0 broken**
- **History**: Added 2026-09-05 18:06
- **Description**: Cannot drag files from Explorer into the Sound Forge 6.0 window. Previously worked on older Windows versions.
- **Impact**: Must use File > Open instead of drag-and-drop workflow
- **Next Steps**: Research UIPI (User Interface Privilege Isolation) and UAC interaction with legacy apps on Windows 11

## Resolved

**SNDFRGFX-PR-0001: Sound Forge 6.0 stalls building peaks files**
- **History**: Added 2026-09-05 18:06 | Resolved 2026-09-05 18:30
- **Solution**: Changed temp folder from `E:` (root) to `E:\SoundForgeTemp` (proper subfolder) via S10312 registry value. Initially also set user TEMP/TMP env vars to same location, but reverted those on 2026-09-11 (SNDFRGFX-DD-04) — system env vars were overreach. S10312 is app-specific and sufficient. Alternative if peaks still stall: copy source audio to local non-synced folder (Dropbox sync may block .sfk writes).
- **Verification**: Pending user test

**SNDFRGFX-PR-0002: Drag and drop files into Sound Forge 6.0 broken**
- **History**: Added 2026-09-05 18:06 | Resolved 2026-09-05 18:30
- **Solution**: Removed WINXPSP3 compatibility mode shim (kept RunAsInvoker `~` only). XP SP3 version lie shim interferes with OLE drag-and-drop on Windows 11. Forum research confirms same-era audio editors had identical issue fixed by removing XP compat.
- **Verification**: Pending user test

## Deferred

(none)

## Problems Changes

**[2026-09-05 18:06]**
- Added: SNDFRGFX-PR-0001 (peaks file stalling)
- Added: SNDFRGFX-PR-0002 (drag-and-drop broken)
