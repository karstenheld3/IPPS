# Playwriter MCP Uninstall

## 1. Remove from Windsurf MCP Config

```powershell
$configPath = "$env:USERPROFILE\.codeium\windsurf\mcp_config.json"

if (-not (Test-Path $configPath)) {
    Write-Host "MCP config not found at: $configPath" -ForegroundColor Yellow
    return
}

try {
    $configContent = Get-Content $configPath -Raw
    $config = $configContent | ConvertFrom-Json -AsHashtable
} catch {
    Write-Host "Error reading config: $_" -ForegroundColor Red
    return
}

if ($config -isnot [System.Collections.Hashtable]) {
    $configHash = @{}
    $config.PSObject.Properties | ForEach-Object { $configHash[$_.Name] = $_.Value }
    $config = $configHash
}

if (-not $config.mcpServers -or -not $config.mcpServers.ContainsKey("playwriter")) {
    Write-Host "Playwriter not found in MCP config" -ForegroundColor Yellow
    return
}

$backupPath = "$configPath._beforeRemovingPlaywriter_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
Copy-Item $configPath $backupPath
Write-Host "Backup: $backupPath" -ForegroundColor Cyan

$config.mcpServers.Remove("playwriter")
$config | ConvertTo-Json -Depth 10 | Set-Content $configPath -Encoding UTF8
Write-Host "Removed Playwriter from Windsurf MCP config" -ForegroundColor Green
Write-Host "Restart Windsurf to complete" -ForegroundColor Yellow
```

## 2. Uninstall CLI

```powershell
npm uninstall -g playwriter
Get-Command playwriter -ErrorAction SilentlyContinue  # Should return nothing
```

## 3. Remove Chrome Extension

Go to `chrome://extensions/`, find "Playwriter MCP", click "Remove".

## 4. Clean Up Data (Optional)

```powershell
$playwriterDir = "$env:USERPROFILE\.playwriter"
if (Test-Path $playwriterDir) {
    Remove-Item $playwriterDir -Recurse -Force
    Write-Host "Removed: $playwriterDir" -ForegroundColor Green
} else {
    Write-Host "No Playwriter data directory found" -ForegroundColor Yellow
}
```

## 5. Remove Skill (if installed)

```powershell
npx -y skills remove remorses/playwriter
```

## Uninstall Checklist

- [ ] Removed from MCP config
- [ ] CLI uninstalled (`npm uninstall -g playwriter`)
- [ ] Chrome extension removed
- [ ] (Optional) Data directory cleaned up
- [ ] (Optional) Skill removed
- [ ] Windsurf restarted