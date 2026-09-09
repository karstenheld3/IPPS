# Microsoft Playwright MCP Uninstall

Remove Microsoft Playwright MCP server from your system.

## MUST-NOT-FORGET

- Close Chrome before removing profile (lock conflict)
- Backup config before modifying
- Restart Windsurf after removal

## Quick Uninstall

Run script, answer with single character (1-4 or Q):

```powershell
$configPath = "$env:USERPROFILE\.codeium\windsurf\mcp_config.json"
$profileDir = "$env:USERPROFILE\.ms-playwright-mcp-profile"
$browsersDir = "$env:LOCALAPPDATA\ms-playwright"
$authFiles = @("$env:USERPROFILE\auth.json","$env:USERPROFILE\.auth.json",".\auth.json")
$npxCacheDir = "$env:LOCALAPPDATA\npm-cache\_npx"

$hasConfig = $false
$hasProfile = Test-Path $profileDir
$hasBrowsers = Test-Path $browsersDir
$hasAuth = ($authFiles | Where-Object { Test-Path $_ }).Count -gt 0
$hasNpmCache = $false
if (Test-Path $npxCacheDir) {
    $hasNpmCache = (Get-ChildItem $npxCacheDir -Directory -ErrorAction SilentlyContinue | Where-Object {
        Test-Path "$($_.FullName)\node_modules\@playwright" -ErrorAction SilentlyContinue
    }).Count -gt 0
}
if (Test-Path $configPath) {
    try {
        $config = Get-Content $configPath -Raw | ConvertFrom-Json -AsHashtable
        $hasConfig = $config.mcpServers -and $config.mcpServers.ContainsKey("playwright")
    } catch { }
}

Write-Host "`n=== Microsoft Playwright MCP Uninstall ===`n"
Write-Host "  [C] Config:   $(if ($hasConfig) {'Found'} else {'Not found'})"
Write-Host "  [P] Profile:  $(if ($hasProfile) {'Found'} else {'Not found'})"
Write-Host "  [A] Auth:     $(if ($hasAuth) {'Found'} else {'Not found'})"
Write-Host "  [B] Browsers: $(if ($hasBrowsers) {'Found'} else {'Not found'})"
Write-Host "  [N] NPM:      $(if ($hasNpmCache) {'Found'} else {'Not found'})"
Write-Host "`n  1=Config only  2=Config+Profile+Auth  3=+Browsers  4=+NPM  Q=Quit`n"

$choice = Read-Host "What to remove? [1/2/3/4/Q]"
if ($choice -notin @('1','2','3','4','Q','q')) { Write-Host "Invalid choice" -ForegroundColor Red; return }
if ($choice -in @('Q','q')) { Write-Host "Cancelled." -ForegroundColor Yellow; return }

$removeConfig = $choice -in @('1','2','3','4')
$removeProfile = $choice -in @('2','3','4')
$removeAuth = $choice -in @('2','3','4')
$removeBrowsers = $choice -in @('3','4')
$removeNpmCache = $choice -eq '4'

if ($removeConfig -and $hasConfig) {
    try {
        $configContent = Get-Content $configPath -Raw
        $config = $configContent | ConvertFrom-Json -AsHashtable
        if ($config.mcpServers -isnot [System.Collections.Hashtable]) {
            $serversHash = @{}; $config.mcpServers.PSObject.Properties | ForEach-Object { $serversHash[$_.Name] = $_.Value }; $config.mcpServers = $serversHash
        }
        if ($config.mcpServers.ContainsKey("playwright")) {
            $backupPath = "$configPath._beforeRemovingMsPlaywrightMcp_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
            Copy-Item $configPath $backupPath -ErrorAction Stop
            $config.mcpServers.Remove("playwright")
            $config | ConvertTo-Json -Depth 10 | Set-Content $configPath -Encoding UTF8 -ErrorAction Stop
            Write-Host "[C] Removed config (backup: $backupPath)" -ForegroundColor Green
        } else { Write-Host "[C] Config already removed" -ForegroundColor Gray }
    } catch { Write-Host "[C] Failed: $_" -ForegroundColor Red }
} elseif ($removeConfig) { Write-Host "[C] Config already removed" -ForegroundColor Gray }

if ($removeProfile -and $hasProfile) {
    try {
        if (Get-Process chrome -ErrorAction SilentlyContinue) { Write-Host "[P] Warning: Chrome running, profile may be locked" -ForegroundColor Yellow }
        Remove-Item $profileDir -Recurse -Force -ErrorAction Stop; Write-Host "[P] Removed profile" -ForegroundColor Green
    } catch { Write-Host "[P] Failed: Close Chrome, delete manually: $profileDir" -ForegroundColor Red }
} elseif ($removeProfile) { Write-Host "[P] Already removed" -ForegroundColor Gray }

if ($removeAuth) {
    $foundAuth = $authFiles | Where-Object { Test-Path $_ }
    if ($foundAuth) { $foundAuth | ForEach-Object { try { Remove-Item $_ -Force; Write-Host "[A] Removed: $_" -ForegroundColor Green } catch { Write-Host "[A] Failed: $_" -ForegroundColor Red } } }
    else { Write-Host "[A] No auth files found" -ForegroundColor Gray }
}

if ($removeBrowsers -and $hasBrowsers) {
    try {
        $size = [math]::Round((Get-ChildItem $browsersDir -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1MB, 0)
        Remove-Item $browsersDir -Recurse -Force -ErrorAction Stop; Write-Host "[B] Removed browsers ($size MB)" -ForegroundColor Green
    } catch { Write-Host "[B] Failed: Delete manually: $browsersDir" -ForegroundColor Red }
} elseif ($removeBrowsers) { Write-Host "[B] Already removed" -ForegroundColor Gray }

if ($removeNpmCache -and $hasNpmCache) {
    try {
        Get-ChildItem $npxCacheDir -Directory -ErrorAction SilentlyContinue | Where-Object { Test-Path "$($_.FullName)\node_modules\@playwright" } | Remove-Item -Recurse -Force -ErrorAction Stop
        Write-Host "[N] Removed Playwright from npx cache" -ForegroundColor Green
    } catch { Write-Host "[N] Failed: Delete manually from $npxCacheDir" -ForegroundColor Red }
} elseif ($removeNpmCache) { Write-Host "[N] Already clean" -ForegroundColor Gray }

Write-Host "`n=== Done === Restart Windsurf to apply changes" -ForegroundColor Cyan
```

## What Gets Removed

- Option 1 - Config entry in `mcp_config.json`
- Option 2 - Config + Profile (`[USER_PROFILE_PATH]\.ms-playwright-mcp-profile`) + Auth files (`auth.json`, `.auth.json`)
- Option 3 - Option 2 + Browsers at `[LOCALAPPDATA]\ms-playwright` (~500MB-2GB)
- Option 4 - Option 3 + NPM cache at `[LOCALAPPDATA]\npm-cache\_npx`

## Manual Removal

### Config Entry
Edit `[USER_PROFILE_PATH]\.codeium\windsurf\mcp_config.json`, delete `"playwright": { ... }` from `mcpServers`.

### Other Components
```powershell
Remove-Item "$env:USERPROFILE\.ms-playwright-mcp-profile" -Recurse -Force
Remove-Item "$env:USERPROFILE\auth.json" -Force -ErrorAction SilentlyContinue
Remove-Item "$env:USERPROFILE\.auth.json" -Force -ErrorAction SilentlyContinue
Remove-Item ".\auth.json" -Force -ErrorAction SilentlyContinue
Remove-Item "$env:LOCALAPPDATA\ms-playwright" -Recurse -Force
```

## Troubleshooting

### "Access Denied" on profile
Close all Chrome windows, end `chrome.exe` in Task Manager, retry.

### Restore config from backup
Backups saved as `mcp_config.json._beforeRemovingMsPlaywrightMcp_YYYYMMDD_HHMMSS`.
```powershell
Copy-Item "[BACKUP_PATH]" "$env:USERPROFILE\.codeium\windsurf\mcp_config.json" -Force
```