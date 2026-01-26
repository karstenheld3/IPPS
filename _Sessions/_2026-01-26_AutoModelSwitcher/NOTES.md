# Session Notes

**Doc ID**: AMSW-NOTES
**Started**: 2026-01-26
**Goal**: Research Windsurf Cascade internals to enable automatic model switching from workflows/skills

## Current Phase

**Phase**: IMPLEMENT (in progress)
**Workflow**: /solve (research-focused)
**Assessment**: Model cycling works, model selection needs keybinding fix

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

- `Ctrl+Alt+M` -> `windsurf.cascade.toggleModelSelector` (when: !terminalFocus)
- `Ctrl+Alt+N` -> `windsurf.cascade.switchToNextModel` (when: !terminalFocus)

### Tested Approaches

1. **Keyboard simulation (cycling)** - [WORKS] `switch-model-v3.ps1` cycles models reliably
2. **Keyboard simulation (selection)** - [PARTIAL] `select-model.ps1` needs keybinding fix, typed into editor
3. **Hooks** - [FAILED] `post_cascade_response` hook never triggered
4. **Ctrl+L focus** - [FAILED] Toggles panel closed instead of focusing
5. **Ctrl+Shift+I focus** - [FAILED] Spawns new Cascade windows

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

## Document History

**[2026-01-26 10:01]**
- Updated with tested findings and custom keybindings
- Model cycling confirmed working
- Model selection needs restart to test keybinding fix

**[2026-01-26 09:28]**
- Initial session created for AutoModelSwitcher research
