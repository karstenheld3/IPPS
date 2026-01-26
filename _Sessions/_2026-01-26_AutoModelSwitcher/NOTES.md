# Session Notes

**Doc ID**: AMSW-NOTES
**Started**: 2026-01-26
**Goal**: Research Windsurf Cascade internals to enable automatic model switching from workflows/skills

## Current Phase

**Phase**: IMPLEMENT (paused)
**Workflow**: /solve (research-focused)
**Assessment**: Hooks approach dropped - too fragile. Manual model switching works. Need different solution for automation.

## Session Info

**Objective**: Find where Windsurf stores:
1. Conversation state
2. Currently used model setting
3. Method to change model programmatically
4. Way to force UI updates

## Key Decisions

1. **Keyboard simulation is viable** - PowerShell script can cycle models via Ctrl+Shift+/ [TESTED]
2. **No direct API available** - Cannot select specific model programmatically [TESTED]
3. **Protobuf not editable** - Binary format without schema, unsafe to modify [TESTED]
4. **UI updates automatically** - No manual refresh needed after keyboard-triggered change [TESTED]
5. **German keyboard requires custom keybindings** - Ctrl+/ doesn't work, use Ctrl+Alt+M [TESTED]
6. **Ctrl+L toggles Cascade** - Do NOT use to focus, it closes the panel [TESTED]
7. **Ctrl+Shift+I spawns new windows** - Do NOT use, it creates new Cascade conversations [TESTED]

## Important Findings

### Storage Locations

- **Conversation state**: `~/.codeium/windsurf/cascade/*.pb` (UUID-named protobuf files)
- **User settings + model config**: `~/.codeium/windsurf/user_settings.pb` (protobuf binary)
- **Editor settings**: `%APPDATA%/Windsurf/User/settings.json` (JSON, editable)
- **State database**: `%APPDATA%/Windsurf/User/globalStorage/state.vscdb` (SQLite)

### Model Configuration

- Models stored in `user_settings.pb` as protobuf
- Model identifiers: `MODEL_CLAUDE_4_5_OPUS`, `MODEL_GPT_5_2_LOW`, `MODEL_PRIVATE_2` (Sonnet 4.5), etc.
- Settings setting: `windsurf.rememberLastModelSelection` in settings.json
- **Cannot edit protobuf by hand** - binary format, no schema available

### VS Code Commands for Model Switching

- `windsurf.cascade.toggleModelSelector` - Opens model selector UI (Ctrl+/ or custom Ctrl+Alt+M)
- `windsurf.cascade.switchToNextModel` - Cycles to next model (Ctrl+Shift+/ or custom Ctrl+Alt+N)
- `windsurf.cascade.openAgentPicker` - Open agent picker (Ctrl+Shift+.)

### Custom Keybindings Added (German keyboard compatible)

File: `%APPDATA%/Windsurf/User/keybindings.json`

- `Ctrl+Shift+F9` -> `windsurf.cascade.toggleModelSelector` (when: !terminalFocus) [TESTED]
- `Ctrl+Shift+F10` -> `windsurf.cascade.switchToNextModel` (when: !terminalFocus) [TESTED]

**Note**: `Ctrl+Alt+*` does NOT work on German keyboards (AltGr produces special chars like µ)

### Tested Approaches

1. **Keyboard simulation (cycling)** - [WORKS] `switch-model-v3.ps1` cycles models reliably
2. **Keyboard simulation (selection)** - [WORKS] `select-windsurf-model-in-ide.ps1` with Ctrl+Shift+F9
3. **Hooks + auto-model-switch.ps1** - [DROPPED] Too fragile - requires Cascade restart to reload config, timing issues, popup interference
4. **Ctrl+L focus** - [FAILED] Toggles panel closed instead of focusing
5. **Ctrl+Shift+I focus** - [FAILED] Spawns new Cascade windows
6. **Ctrl+Alt+M** - [FAILED] Produces µ on German keyboard (AltGr conflict)

## IMPORTANT: Cascade Agent Instructions

- Use `/prime` to load context when resuming
- Track all findings in this NOTES.md
- Problems go in PROBLEMS.md with IDs
- Progress tracked in PROGRESS.md
- Follow EDIRD phases: EXPLORE -> DESIGN -> IMPLEMENT -> REFINE -> DELIVER

## Workflows to Run on Resume

1. `/prime` - Load workspace context
2. `/recap` - Review session state
3. `/continue` - Execute next items

## Model Discovery Findings [TESTED]

**Approach**: Fullscreen screenshot capture for all sections

**DPI Scaling Fix** [CRITICAL]:
- Windows DPI scaling causes `.NET Screen.Bounds` to return logical pixels, not physical
- Physical: 2560x1600, Logical: 2048x1280 (125% scaling)
- Must use Win32 `GetDeviceCaps(DESKTOPHORZRES/DESKTOPVERTRES)` for actual resolution
- Fixed in `simple-screenshot.ps1`

**Two screenshot scripts**:
- `simple-screenshot.ps1` - Passive, no UI interaction, for testing/verification
- `capture-with-crop.ps1` - Opens model selector, sends keystrokes, for registry updates

**Screenshots saved to**: `[WORKSPACE]/.tools/_screenshots/`

## Document History

**[2026-01-26 13:25]**
- DROPPED hooks approach - too fragile (requires restart, timing issues)
- Fixed DPI scaling in screenshot script (was capturing 2048x1280 instead of 2560x1600)
- Created `simple-screenshot.ps1` for passive captures (no UI interaction)
- Manual model switching works, need different automation approach

**[2026-01-26 12:33]**
- Auto-model-switcher TESTED and WORKING
- Fixed popup close issue: Use Ctrl+Shift+F9 toggle instead of Escape
- Agent can switch models mid-conversation (takes effect on next user message)
- Verified with screenshots: Opus → Sonnet → Opus transitions work cleanly

**[2026-01-26 11:43]**
- Model discovery workflow simplified to fullscreen capture
- 55% JPEG compression blocked by antivirus (script modification triggers scan)
- WORKFLOW.md updated with simplified approach
- Note: Truncation issues at the time were actually DPI scaling, not LLM image scaling (see FL-011)

**[2026-01-26 10:09]**
- Model selection WORKING with `select-model.ps1` + `Ctrl+Shift+F9`
- Toggle between Opus Thinking and Sonnet 4.5 confirmed

**[2026-01-26 10:01]**
- Updated with tested findings and custom keybindings
- Model cycling confirmed working
- Model selection needs restart to test keybinding fix

**[2026-01-26 09:28]**
- Initial session created for AutoModelSwitcher research
