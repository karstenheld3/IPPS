# Session Progress

**Doc ID**: AMSW-PROGRESS

## Phase Plan

- [x] **EXPLORE** - complete
- [ ] **DESIGN** - skipped (POC-style)
- [x] **IMPLEMENT** - paused (hooks approach dropped)
- [ ] **REFINE** - pending
- [ ] **DELIVER** - pending

## To Do

(none - POC complete)

## In Progress

(none)

## Done

- [x] Session initialized
- [x] Search Windsurf app data folders for state files
- [x] Examine Windsurf configuration files (settings.json, user_settings.pb)
- [x] Check for SQLite databases (state.vscdb)
- [x] Research Windsurf extension API (package.json commands)
- [x] Test model switching approaches (keyboard simulation)
- [x] Create proof-of-concept script (switch-model.ps1)
- [x] Document findings (_INFO_AUTO_MODEL_SWITCHER.md)
- [x] [TESTED] Model cycling with `switch-model-v3.ps1` - confirmed working
- [x] [TESTED] Custom keybindings added to `keybindings.json`
- [x] [TESTED] Extracted model list from `user_settings.pb`
- [x] Fix keybinding focus requirement (removed `cascadePanel.focused`)
- [x] [TESTED] Fix German keyboard - use Ctrl+Shift+F9 instead of Ctrl+Alt+M
- [x] [TESTED] Model selection with `select-windsurf-model-in-ide.ps1` - confirmed working
- [x] [TESTED] Toggle between Claude Opus 4.5 Thinking and Claude Sonnet 4.5
- [x] [TESTED] Model discovery via UI screenshot capture
- [x] [TESTED] Fullscreen capture workflow
- [x] Created `windsurf-model-registry.json` with 68 models and costs
- [x] Updated UPDATE_WINDSURF_MODEL_REGISTRY.md with workflow
- [x] Recorded failures AMSW-FL-001 through AMSW-FL-011 in FAILS.md
- [x] [TESTED] Fixed DPI scaling issue - use Win32 GetDeviceCaps for physical resolution
- [x] Created `simple-screenshot.ps1` for passive screenshots (no UI interaction)
- [x] Separated screenshot scripts: simple (passive) vs capture-with-crop (active)

## Tried But Not Used

- **Ctrl+L to focus Cascade** - [TESTED] Toggles panel closed, not usable
- **Ctrl+Shift+I to focus Cascade** - [TESTED] Spawns new Cascade windows
- **Hooks + auto-model-switch.ps1** - [DROPPED] Too fragile - requires Cascade restart to reload config, timing issues, popup interference
- **switch-model.ps1 (v1)** - Superseded by v3
- **switch-model-v2.ps1** - Superseded by v3
- **Ctrl+Alt+M keybinding** - [TESTED] Produces µ on German keyboard (AltGr conflict)
- **55% JPEG compression** - [TESTED] Antivirus blocks modified scripts with keybd_event
- **Clipboard-based model extraction** - [TESTED] Unreliable, cycles endlessly
- **.NET Screen.Bounds for resolution** - [FAILED] Returns logical pixels, not physical (DPI scaling)
