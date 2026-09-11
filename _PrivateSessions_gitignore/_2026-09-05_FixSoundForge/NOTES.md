# Session Notes

**Doc ID**: SNDFRGFX-NOTES

## Initial Request

````text
lets fix soundforge 

"c:\Program Files (x86)\Sonic Foundry\Sound Forge 6.0" 

Problems:
1. It stalls building peaks files
2. I can't drag + drop files into it

Something has changed with windows 11 that sandboxes or blocks these older apps

I want full functionality
````

## Session Info

- **Started**: 2026-09-05
- **Goal**: Fix Sound Forge 6.0 compatibility issues on Windows 11 (peaks file stalling, drag-and-drop broken)
- **Operation Mode**: IMPL-ISOLATED
- **Output Location**: Session folder (research + fixes)

## Agent Instructions

- Research before acting - understand root causes first
- Sound Forge 6.0 install path: `C:\Program Files (x86)\Sonic Foundry\Sound Forge 6.0`
- Two distinct problems: peaks file building stalls, drag-and-drop broken
- User suspects Windows 11 sandboxing/blocking of legacy 32-bit apps

## Key Decisions

- **SNDFRGFX-DD-01**: Remove WINXPSP3 compat mode, keep RunAsInvoker only. Rationale: XP SP3 shim interferes with OLE drag-and-drop on Windows 11. Forum research shows same-era audio editors (Goldwave 5.55) fixed drag-drop by switching from XP to Win7 compat or removing it entirely.
- **SNDFRGFX-DD-02**: Change temp folder from `E:` (root) to `E:\SoundForgeTemp` (subfolder). Rationale: Writing temp files to drive root may cause path issues on Windows 11. Subfolder is cleaner and avoids potential permission issues.
- **SNDFRGFX-DD-03**: Set user TEMP/TMP environment variables to `E:\SoundForgeTemp`. Rationale: C: drive has only 2 GB free. If Sound Forge falls back to env TEMP, low disk space could cause stalling.

## Revert (2026-09-11)

- **SNDFRGFX-DD-04**: Revert user TEMP/TMP env vars to Windows default (`C:\Users\User\AppData\Local\Temp`). Rationale: Changing system-wide env vars was overreach — Sound Forge uses S10312 registry value directly, not env vars. C: has only 0.8 GB free but Sound Forge won't fall back to env TEMP if S10312 is set.
- **SNDFRGFX-DD-05**: Keep S10312 at `E:\SoundForgeTemp` (app-specific, no system impact). E: has 115 GB free.
- **Alternative peaks fix**: If peaks still stall, root cause is likely source file location (Dropbox-synced folders), not temp folder. `.sfk` peak files are written to same directory as source audio. Copy source files to local non-synced folder before editing.

## Important Findings

- Sound Forge 6.0 is 32-bit (x86), no manifest, pre-Vista legacy app [VERIFIED]
- Compat flags were `~ WINXPSP3` (RunAsInvoker + XP SP3 version lie) [VERIFIED]
- Temp folder was set to `E:` (drive root, no subfolder) [VERIFIED]
- C: drive had 2.1 GB free (2026-09-05), now 0.8 GB free (2026-09-11) [VERIFIED]
- User TEMP/TMP env vars were changed to E:\SoundForgeTemp (2026-09-05), reverted to C:\Users\User\AppData\Local\Temp (2026-09-11) [VERIFIED]
- No VirtualStore redirection for Sound Forge [VERIFIED]
- No .sfk peak files found on system [VERIFIED]
- UIPI blocks drag-and-drop between different integrity levels [VERIFIED]
- Forum user with Goldwave 5.55 fixed identical drag-drop issue by removing XP compat mode [VERIFIED]

## Topic Registry

**Global topics** (registered in ID-REGISTRY.md):
- `SNDFRGFX` - Sound Forge 6.0 Windows 11 compatibility fix

**Subtopics** (session-local):
(none)

## Topic Folders

(none)

## Step Folders

(none)

## Bug List

(none yet)

## Significant Prompts Log

(none yet)
