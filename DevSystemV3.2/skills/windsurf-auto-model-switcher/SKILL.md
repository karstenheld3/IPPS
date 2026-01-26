---
name: windsurf-auto-model-switcher
description: Switch Windsurf Cascade AI models programmatically via keyboard simulation. Apply when needing to change models from workflows or scripts.
---

# Windsurf Auto Model Switcher

Switch Windsurf Cascade AI models programmatically using keyboard simulation.

## Verb Mapping

This skill implements:
- [SWITCH-MODEL] - Change the active Cascade model

**Phases**: Any (utility skill)

## MUST-NOT-FORGET

- Requires custom keybindings (see SETUP.md)
- German keyboards: Ctrl+Alt produces special chars (AltGr), use F-keys instead
- Model selector requires Windsurf window focus
- Cannot directly select model via API - only UI automation works

## Prerequisites

1. Run SETUP.md to install required keybindings
2. Windsurf must be running with Cascade panel visible

## Available Scripts

- `select-model.ps1` - Select a specific model by search query
- `switch-model.ps1` - Cycle to the next model in the list

## Usage

### Select Specific Model

```powershell
# Select Claude Sonnet 4.5
.\select-model.ps1 -Query "sonnet 4.5"

# Select Claude Opus 4.5 (Thinking)
.\select-model.ps1 -Query "opus 4.5 thinking"

# Select GPT-5.2 Low Reasoning
.\select-model.ps1 -Query "gpt-5.2 low"
```

### Cycle Models

```powershell
# Cycle to next model
.\switch-model.ps1

# Cycle multiple times
.\switch-model.ps1 -CycleCount 3
```

## Custom Keybindings

File: `%APPDATA%/Windsurf/User/keybindings.json`

| Shortcut | Command | Description |
|----------|---------|-------------|
| Ctrl+Shift+F9 | `windsurf.cascade.toggleModelSelector` | Open model selector |
| Ctrl+Shift+F10 | `windsurf.cascade.switchToNextModel` | Cycle to next model |

## Known Model Names (from UI)

Use these exact names or partial matches as `-Query` parameter:

**Claude**
- Claude Opus 4.5 (Thinking)
- Claude Opus 4.5
- Claude Opus 4.1 (Thinking)
- Claude Opus 4.1
- Claude Sonnet 4.5 Thinking
- Claude Sonnet 4.5 (1M)
- Claude Sonnet 4.5
- Claude Sonnet 4 (Thinking)
- Claude Sonnet 4
- Claude Haiku 4.5
- Claude 3.7 Sonnet (Thinking)
- Claude 3.7 Sonnet
- Claude 3.5 Sonnet

**GPT-5.2**
- GPT-5.2 X-High Reasoning Fast
- GPT-5.2 X-High Reasoning
- GPT-5.2 High Reasoning Fast
- GPT-5.2 High Reasoning
- GPT-5.2 Medium Reasoning Fast
- GPT-5.2 Medium Reasoning
- GPT-5.2 Low Reasoning Fast
- GPT-5.2 Low Reasoning
- GPT-5.2 No Reasoning Fast
- GPT-5.2 No Reasoning

**GPT-5.1 / GPT-5**
- GPT-5.1 (high reasoning)
- GPT-5.1 (medium reasoning)
- GPT-5.1 (low reasoning)
- GPT-5.1 (no reasoning)
- GPT-5 (high reasoning)
- GPT-5 (medium reasoning)
- GPT-5 (low reasoning)

**Gemini**
- Gemini 2.5 Pro
- Gemini 3 Pro High
- Gemini 3 Pro Medium
- Gemini 3 Pro Low
- Gemini 3 Flash High
- Gemini 3 Flash Medium
- Gemini 3 Flash Low

**Other**
- o3 (high reasoning)
- o3
- SWE-1.5
- SWE-1
- xAI Grok-3
- xAI Grok-3 mini (Thinking)
- Grok Code Fast 1
- DeepSeek R1 (0528)
- DeepSeek V3 (0324)
- Kimi K2
- Minimax M2
- Qwen3-Coder
- GPT-4o
- GPT-4.1

## Limitations

1. **No direct API** - Windsurf stores model config in protobuf binary (no schema)
2. **Requires window focus** - Script briefly steals focus to send keystrokes
3. **Sequential selection only** - Cannot jump directly to a model by index
4. **Hooks don't work** - `post_cascade_response` hook never triggers

## Troubleshooting

### Script types into editor instead of model selector

- Ensure keybindings are installed (run SETUP.md)
- Restart Windsurf after installing keybindings

### Model doesn't change

- Ensure Cascade panel is visible (not collapsed)
- Try running script again with Windsurf in foreground

### Special characters appear (German keyboard)

- Use Ctrl+Shift+F9/F10, NOT Ctrl+Alt combinations
- Ctrl+Alt = AltGr on German keyboards, produces special chars
