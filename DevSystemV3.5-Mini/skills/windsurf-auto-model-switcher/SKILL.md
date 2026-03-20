---
name: windsurf-auto-model-switcher
description: Switch Windsurf Cascade AI models programmatically. Apply when needing to change models from workflows or scripts.
---

# Windsurf Auto Model Switcher

Switch models via keyboard simulation.

## MUST-NOT-FORGET

- Requires custom keybindings (see SETUP.md)
- German keyboards: Use F-keys, not Ctrl+Alt (AltGr conflict)
- Model selector requires Windsurf window focus
- Auto-switching requires safety check (screenshot verification)

## Model Hints in STRUT

STRUT Strategy sections may include model hints (recommendations only - agent decides):
```
├─ Strategy: Analyze requirements, design solution
│   - Opus for analysis, Sonnet for implementation
```

## Prerequisites

1. Run SETUP.md to install keybindings
2. Restart Windsurf after setup

## Files

- `select-windsurf-model-in-ide.ps1` - Select model by search query
- `windsurf-model-registry.json` - Available models and costs
- `update-model-registry/UPDATE_WINDSURF_MODEL_REGISTRY.md` - Registry update workflow

## Usage

```powershell
.\select-windsurf-model-in-ide.ps1 -Query "sonnet 4.5"
.\select-windsurf-model-in-ide.ps1 -Query "opus 4.5 thinking"
.\select-windsurf-model-in-ide.ps1 -Query "gpt-5.2 low"
```

## Keybindings

- `Ctrl+Shift+F9` - Open model selector
- `Ctrl+Shift+F10` - Cycle to next model

## Troubleshooting

**Script types into editor**: Run SETUP.md and restart Windsurf.
**Model doesn't change**: Ensure Cascade panel is visible.