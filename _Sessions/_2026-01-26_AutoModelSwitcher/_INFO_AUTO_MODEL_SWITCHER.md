# INFO: Auto Model Switcher Research

**Doc ID**: AMSW-IN01
**Goal**: Document how to programmatically switch Cascade models in Windsurf

## Summary

**Key Finding**: Model switching in Windsurf is **UI-driven only**. The model configuration is stored in a protobuf binary file that cannot be safely edited. However, keyboard simulation can trigger model cycling.

**Feasibility**: Partial - keyboard simulation works but has limitations.

## Storage Locations

### Conversation State
- **Path**: `~/.codeium/windsurf/cascade/*.pb`
- **Format**: Protocol Buffers (binary)
- **Contents**: Each conversation stored as UUID-named `.pb` file
- **Editable**: No (binary format, no schema)

### User Settings + Model Config
- **Path**: `~/.codeium/windsurf/user_settings.pb`
- **Format**: Protocol Buffers (binary)
- **Contents**: Cascade UI settings, model configurations, conversation IDs
- **Editable**: No (UI only)

### Editor Settings
- **Path**: `%APPDATA%/Windsurf/User/settings.json`
- **Format**: JSON
- **Contents**: VS Code-style editor settings
- **Editable**: Yes
- **Relevant key**: `windsurf.rememberLastModelSelection` (boolean)

### State Database
- **Path**: `%APPDATA%/Windsurf/User/globalStorage/state.vscdb`
- **Format**: SQLite
- **Contents**: Window state, recent files, extension state

## Available Models (from user_settings.pb)

```
MODEL_CLAUDE_4_5_OPUS              - Claude Opus 4.5
MODEL_CLAUDE_4_5_OPUS_THINKING     - Claude Opus 4.5 (Thinking)
MODEL_CLAUDE_4_SONNET              - Claude Sonnet 4
MODEL_CLAUDE_4_SONNET_THINKING     - Claude Sonnet 4 (Thinking)
MODEL_PRIVATE_2                    - Claude Sonnet 4.5
MODEL_PRIVATE_3                    - Claude Sonnet 4.5 (Thinking)
MODEL_PRIVATE_11                   - Claude Haiku 4.5
MODEL_GPT_5_2_LOW                  - GPT-5.2 (Low)
MODEL_GPT_5_2_MEDIUM               - GPT-5.2 (Medium)
MODEL_CHAT_O3                      - O3
MODEL_GOOGLE_GEMINI_2_5_PRO        - Gemini 2.5 Pro
MODEL_SWE_1_5                      - SWE-1.5
MODEL_DEEPSEEK_R1                  - DeepSeek R1
MODEL_XAI_GROK_3                   - Grok 3
```

## VS Code Commands for Model Switching

| Command | Keybinding | Description |
|---------|------------|-------------|
| `windsurf.cascade.toggleModelSelector` | Ctrl+/ | Opens model selector UI |
| `windsurf.cascade.switchToNextModel` | Ctrl+Shift+/ | Cycles to next model |
| `windsurf.cascade.openAgentPicker` | Ctrl+Shift+. | Opens agent picker |

## Programmatic Approaches

### 1. Keyboard Simulation (Working)

PowerShell script that focuses Windsurf and sends keystrokes:

```powershell
# Focus Windsurf window and send Ctrl+Shift+/ to cycle model
Add-Type -AssemblyName System.Windows.Forms
$proc = Get-Process -Name "Windsurf" | Where-Object { $_.MainWindowTitle -ne "" } | Select-Object -First 1
[Win32]::SetForegroundWindow($proc.MainWindowHandle)
[System.Windows.Forms.SendKeys]::SendWait("^+/")
```

**Limitations**:
- Requires window focus (briefly steals focus from user)
- Cycles models sequentially (cannot select specific model)
- May not work if Cascade panel not focused

### 2. Hooks (Limited)

Cascade hooks can trigger scripts at specific events but cannot:
- Change the model selection
- Access internal Cascade state
- Modify the UI

**Possible use**: Trigger model switch script after specific events.

### 3. VS Code Extension (Theoretical)

A custom VS Code extension could use:
```javascript
vscode.commands.executeCommand('windsurf.cascade.switchToNextModel');
```

**Limitations**:
- Requires extension development
- Commands may not be exposed to external extensions
- Model selection is still sequential

### 4. Direct Protobuf Modification (Not Recommended)

The `user_settings.pb` file uses Protocol Buffers format without a published schema.
- Risk of corrupting settings
- Windsurf may validate/regenerate on startup
- No documentation available

## UI Update Mechanism

Windsurf's Cascade panel updates automatically when:
- Model is changed via UI
- Conversation is switched
- Settings are modified through UI

**No external refresh command found** - the UI is tightly coupled to internal state.

## Conclusions

1. **Cannot directly set a specific model** - only cycle through available models
2. **Protobuf files are not user-editable** - binary format without schema
3. **Keyboard simulation is the only working approach** for external model switching
4. **Hooks cannot modify Cascade state** - only trigger external actions
5. **UI updates automatically** - no manual refresh needed after model change

## Recommended Approach

For workflow/skill integration:

1. Create PowerShell script for keyboard simulation
2. Call from workflow using `run_command`
3. Accept limitations (focus stealing, sequential cycling)

Alternative: Request Codeium add CLI support for model selection (e.g., `windsurf chat --model claude-sonnet-4.5`)

## Document History

**[2026-01-26 09:30]**
- Initial research completed
- Documented storage locations, commands, and approaches
