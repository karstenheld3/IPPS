# Microsoft Playwright MCP Setup

Run once to configure Playwright MCP server for browser automation.

## 1. Verify Node.js

```powershell
node --version
npx --version
```

Expected: Node.js 18+. If missing: https://nodejs.org

Find npx path if needed: `(Get-Command npx).Source`

Common locations: `[USER_PROFILE_PATH]\.nvm\versions\node\v20.19.0\bin\npx.cmd`, `[PROGRAM_FILES]\nodejs\npx.cmd`, `[PROGRAM_DATA]\chocolatey\bin\npx.exe`

## 2. Test Playwright MCP

```powershell
npx @playwright/mcp@latest --help
```

## 3. Add to Windsurf Global Config

Config path: `$env:USERPROFILE\.codeium\windsurf\mcp_config.json`

Target entry:
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

Setup script handles: pre-flight checks (npx, Node version), read/create config, PSCustomObject-to-Hashtable conversion, idempotent add/update, backup before write, rollback on failure, installation summary.

```powershell
$configPath = "$env:USERPROFILE\.codeium\windsurf\mcp_config.json"
$targetServer = @{ command = "npx"; args = @("@playwright/mcp@latest") }

# Read or create config
if (Test-Path $configPath) {
    $config = Get-Content $configPath -Raw | ConvertFrom-Json -AsHashtable
} else {
    $configDir = Split-Path $configPath
    if (-not (Test-Path $configDir)) { New-Item -ItemType Directory -Path $configDir -Force | Out-Null }
    $config = @{ mcpServers = @{} }
}

# Ensure mcpServers is Hashtable
if ($config.mcpServers -isnot [System.Collections.Hashtable]) {
    $serversHash = @{}
    $config.mcpServers.PSObject.Properties | ForEach-Object { $serversHash[$_.Name] = $_.Value }
    $config.mcpServers = $serversHash
}

# Backup and write
if (Test-Path $configPath) {
    Copy-Item $configPath "$configPath._backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
}
$config.mcpServers["playwright"] = $targetServer
$config | ConvertTo-Json -Depth 10 | Set-Content $configPath -Encoding UTF8
```

After running: restart Windsurf, check Command Palette > "MCP: Show Servers".

## 4. Configuration Options

### Persistent User Profile (remembers logins)

```json
"args": ["@playwright/mcp@latest", "--user-data-dir", "[USER_PROFILE_PATH]/.ms-playwright-mcp-profile"]
```

```powershell
$profileDir = "$env:USERPROFILE\.ms-playwright-mcp-profile"
if (-not (Test-Path $profileDir)) { New-Item -ItemType Directory -Path $profileDir }
```

### Headless Mode

```json
"args": ["@playwright/mcp@latest", "--headless"]
```

### Specific Browser

```json
"args": ["@playwright/mcp@latest", "--browser", "firefox"]
```

Options: `chromium` (default), `firefox`, `webkit`

### Storage State (pre-authenticated)

```json
"args": ["@playwright/mcp@latest", "--isolated", "--storage-state", "[AUTH_STATE_PATH]"]
```

### Browser Extension Mode

```json
"args": ["@playwright/mcp@latest", "--extension"]
```

Start Chrome first: `& "[PROGRAM_FILES]\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222`

## 5. Troubleshooting

### npx not found

Use full path in config: `"command": "[NPX_FULL_PATH]"`

### Profile lock error

```powershell
Get-Process chrome -ErrorAction SilentlyContinue | Stop-Process -Force
Remove-Item "$env:USERPROFILE\.ms-playwright-mcp-profile\SingletonLock" -Force -ErrorAction SilentlyContinue
```

### Extension mode not connecting

Known issue (GitHub #921). Workaround: start Chrome with `--remote-debugging-port=9222` before enabling extension mode.

### Browsers not installed

```powershell
npx playwright install chromium
```

### Linux inotify exhaustion

```bash
echo "fs.inotify.max_user_watches = 2097152" | sudo tee /etc/sysctl.d/99-playwright.conf
sudo sysctl -p /etc/sysctl.d/99-playwright.conf
```

## 6. Security

- Use `--user-data-dir` for persistent sessions, `--storage-state` for pre-saved auth
- NEVER commit auth.json or profile directories to git

```gitignore
.ms-playwright-mcp-profile/
auth.json
*.auth.json
```

## Quick Reference

- Default - Clean isolated sessions
- `--user-data-dir` - Persistent logins
- `--headless` - Background automation
- `--isolated --storage-state` - Pre-authenticated
- `--extension` - Connect to existing browser