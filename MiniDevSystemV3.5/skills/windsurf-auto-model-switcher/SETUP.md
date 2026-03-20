# Setup: Windsurf Auto Model Switcher

## Automatic Setup (PowerShell)

```powershell
$keybindingsPath = "$env:APPDATA\Windsurf\User\keybindings.json"

if (Test-Path $keybindingsPath) {
    $keybindings = Get-Content $keybindingsPath -Raw | ConvertFrom-Json
} else {
    $keybindings = @()
}

$keybindings = [System.Collections.ArrayList]@($keybindings)

$newBindings = @(
    @{ key = "ctrl+shift+f9"; command = "windsurf.cascade.toggleModelSelector"; when = "!terminalFocus" },
    @{ key = "ctrl+shift+f10"; command = "windsurf.cascade.switchToNextModel"; when = "!terminalFocus" }
)

foreach ($binding in $newBindings) {
    $exists = $keybindings | Where-Object { $_.key -eq $binding.key -and $_.command -eq $binding.command }
    if (-not $exists) { $keybindings.Add([PSCustomObject]$binding) | Out-Null }
}

$keybindings | ConvertTo-Json -Depth 10 | Set-Content $keybindingsPath -Encoding UTF8
```

Restart Windsurf after running.

## Manual Setup

1. `Ctrl+Shift+P` -> "Preferences: Open Keyboard Shortcuts (JSON)"
2. Add:

```json
{ "key": "ctrl+shift+f9", "command": "windsurf.cascade.toggleModelSelector", "when": "!terminalFocus" },
{ "key": "ctrl+shift+f10", "command": "windsurf.cascade.switchToNextModel", "when": "!terminalFocus" }
```

3. Save and restart Windsurf

## Verify

Press `Ctrl+Shift+F9` - model selector popup should appear.

If not working: check JSON syntax is valid, verify file path `%APPDATA%\Windsurf\User\keybindings.json`.