# Session Notes

**Doc ID**: AMSW-NOTES
**Started**: 2026-01-26
**Goal**: Research Windsurf Cascade internals to enable automatic model switching from workflows/skills

## Current Phase

**Phase**: DESIGN (in progress)
**Workflow**: /solve (research-focused)
**Assessment**: Redesigning model switching - explicit models in STRUT/TASKS, safety checks via screenshot before switching.

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

### Best Fast + Cheap Options [VERIFIED]
- **Gemini 3 Flash Medium**: 372 TPS, 78% SWE-Bench (Fastest + Best coding)
- **Grok Code Fast 1**: 236 TPS, 70.8% SWE-Bench (Free in Windsurf)
- **Claude Haiku 4.5**: ~150 TPS, 73.3% SWE-Bench (1x Windsurf cost)
- **DeepSeek V3**: ~80 TPS, 38.8% SWE-Bench (Free, general purpose)

### Tested Approaches

1. **Keyboard simulation (cycling)** - [WORKS] `switch-model-v3.ps1` cycles models reliably
2. **Keyboard simulation (selection)** - [WORKS] `select-windsurf-model-in-ide.ps1` with Ctrl+Shift+F9
3. **Dry-run mode** - [WORKS] `-DryRun` parameter previews selection without keyboard events
4. **Fuzzy matching + cost priority** - [WORKS] Correctly selects cheapest matching model
5. **Default fallback** - [WORKS] Defaults to Claude Sonnet 4 when no match found
6. **Refocus method** - [PROVEN] `Ctrl+Shift+A` is the bulletproof method to refocus Cascade chat

## Document History

**[2026-01-26 16:30]**
- PRODUCTION READY: `select-windsurf-model-in-ide.ps1` finalized
- ADDED: Dry-run mode, mandatory validation, cost-based prioritization
- FIXED: Default model set to Claude Sonnet 4 (2x)
- UPDATED: MODEL-LOW to Gemini 3 Flash Medium (78% SWE-Bench, 372 TPS)
- RESEARCHED: Fast and cheap models (Grok, Gemini Flash, DeepSeek)

- TESTED: Screenshot-based safety check workflow [SUCCESS]
- Agent successfully: took screenshot, verified 4 safety conditions, switched Opus→Sonnet
- Added switch-back pattern to cascade-model-switching.md rule
- Model switch takes effect on next user message (verified with before/after screenshots)

**[2026-01-26 13:49]**
- REDESIGNING: Model switching approach
- New direction: Explicit models in STRUT Strategy + step overrides (not tiers)
- Safety checks via screenshot before switching (verify Windsurf foreground, Cascade open, user idle)
- Configuration priority: Session NOTES.md > Workspace !NOTES.md

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
