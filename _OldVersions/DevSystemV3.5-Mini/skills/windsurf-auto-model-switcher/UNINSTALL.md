# Uninstall: Windsurf Auto Model Switcher

## Automatic Uninstall (PowerShell)

```powershell
$keybindingsPath = "$env:APPDATA\Windsurf\User\keybindings.json"
$keybindings = Get-Content $keybindingsPath -Raw | ConvertFrom-Json
$commandsToRemove = @("windsurf.cascade.toggleModelSelector", "windsurf.cascade.switchToNextModel")
$keybindings = $keybindings | Where-Object { $_.command -notin $commandsToRemove }
$keybindings | ConvertTo-Json -Depth 10 | Set-Content $keybindingsPath -Encoding UTF8
```

Restart Windsurf after running.

## Manual Uninstall

1. `Ctrl+Shift+P` -> "Preferences: Open Keyboard Shortcuts (JSON)"
2. Remove entries with commands `windsurf.cascade.toggleModelSelector` and `windsurf.cascade.switchToNextModel`
3. Save and restart Windsurf

## What Gets Removed

- `Ctrl+Shift+F9` -> `windsurf.cascade.toggleModelSelector`
- `Ctrl+Shift+F10` -> `windsurf.cascade.switchToNextModel`

Default Windsurf keybindings (`Ctrl+/` and `Ctrl+Shift+/`) remain unaffected.

## Verify

Press `Ctrl+Shift+F9` - nothing should happen.