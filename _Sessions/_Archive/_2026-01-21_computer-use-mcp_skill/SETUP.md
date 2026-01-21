# Claude Computer Use MCP Setup

Run once to configure computer-use-mcp for full desktop automation via screenshot analysis and mouse/keyboard control.

**WARNING**: This gives AI complete control of your computer. Use with caution.

**Compatibility Note**: This MCP server is verified with Claude Desktop and Cursor. Windsurf support uses the same MCP protocol and is expected to work, but is not officially verified by the package author.

## Pre-Installation Verification

Complete ALL verification steps before modifying your system. If any step fails, fix it before proceeding to installation.

## 1. Verify Node.js Installation

```powershell
node --version
npm --version
npx --version
```

Expected: Node.js 18+ installed and in PATH.
If not installed: Download from https://nodejs.org (LTS version recommended).

## 2. Verify npx Path

**Find npx location:**
```powershell
(Get-Command npx).Source
```

**If npx not found in MCP config**, use full path:
```powershell
# Common locations:
# Windows (nvm): [USER_PROFILE_PATH]\.nvm\versions\node\v20.19.0\bin\npx.cmd
# Windows (default): [PROGRAM_FILES]\nodejs\npx.cmd
# Windows (Chocolatey): [PROGRAM_DATA]\chocolatey\bin\npx.exe
```

## 3. Test computer-use-mcp Package

**Download and test (does NOT modify Windsurf config):**
```powershell
npx -y computer-use-mcp --help
```

**Expected output:**
```
Usage: computer-use-mcp [options]

Options:
  -h, --help     display help for command
```

If you see help output, the package works. If errors occur, check:
- Node.js version (must be 18+)
- Network connectivity (package needs to download)
- Antivirus blocking npx

## 4. Test nut.js Input Control

nut.js is the library that controls mouse/keyboard. Test it works on your system:

```powershell
# Test nut.js can load (does NOT move mouse/keyboard yet)
node -e "const { mouse } = require('@nut-tree/nut-js'); console.log('nut.js loaded successfully');"
```

**If error "Cannot find module":**
```powershell
# Install nut.js temporarily to test
npm install --no-save @nut-tree/nut-js
node -e "const { mouse } = require('@nut-tree/nut-js'); console.log('nut.js loaded successfully');"
```

**If error about native modules or Visual C++:**
- Install Visual C++ Redistributable: https://aka.ms/vs/17/release/vc_redist.x64.exe
- Restart terminal and try again

## 5. Test Screenshot Capture

```powershell
# Test screenshot capability (saves test image)
node -e "
const { screen } = require('@nut-tree/nut-js');
(async () => {
  const img = await screen.grab();
  console.log('Screenshot captured: ' + img.width + 'x' + img.height);
})();
"
```

**Expected output:** `Screenshot captured: [width]x[height]`

**If black screen or error:**
- Check GPU driver is up to date
- Try running terminal as Administrator
- On multi-monitor: primary monitor is captured

## 6. Verify Windsurf MCP Support

Check Windsurf can load MCP servers:

```powershell
# Check if MCP config exists
$configPath = "$env:USERPROFILE\.codeium\windsurf\mcp_config.json"
if (Test-Path $configPath) {
    Write-Host "[OK] MCP config exists: $configPath" -ForegroundColor Green
    Get-Content $configPath | ConvertFrom-Json | ConvertTo-Json -Depth 3
} else {
    Write-Host "[INFO] No MCP config yet - will be created during installation" -ForegroundColor Yellow
}
```

## Pre-Installation Checklist

Before proceeding, confirm:
- [ ] Node.js 18+ installed and in PATH
- [ ] npx works and path is known
- [ ] computer-use-mcp package downloads and shows help
- [ ] nut.js loads without errors
- [ ] Screenshot capture works
- [ ] Windsurf MCP config location verified

**If all checks pass, proceed to installation.**

---

## Installation

## 7. Add to Windsurf Global Config

Run this PowerShell script to add computer-use-mcp without modifying existing servers:

```powershell
# === Add Claude Computer Use MCP to Windsurf ===

# Pre-checks
Write-Host "=== Pre-flight Checks ===" -ForegroundColor Cyan

# Check npx availability
$npxPath = Get-Command npx -ErrorAction SilentlyContinue
if (-not $npxPath) {
    Write-Host "[FAIL] npx not found in PATH" -ForegroundColor Red
    Write-Host "Install Node.js 18+ from https://nodejs.org" -ForegroundColor Yellow
    return
}
Write-Host "[OK] npx found: $($npxPath.Source)" -ForegroundColor Green

# Check Node.js version
$nodeVersion = node --version 2>$null
if ($nodeVersion -match 'v(\d+)') {
    $majorVersion = [int]$matches[1]
    if ($majorVersion -lt 18) {
        Write-Host "[WARN] Node.js $nodeVersion detected, v18+ recommended" -ForegroundColor Yellow
    } else {
        Write-Host "[OK] Node.js $nodeVersion" -ForegroundColor Green
    }
}

Write-Host ""

$configPath = "$env:USERPROFILE\.codeium\windsurf\mcp_config.json"

# Expected target config
$targetServer = @{
    command = "npx"
    args = @("-y", "computer-use-mcp")
}

# Read existing config or create empty structure
$needsUpdate = $false
if (Test-Path $configPath) {
    try {
        $configContent = Get-Content $configPath -Raw
        if ([string]::IsNullOrWhiteSpace($configContent)) {
            $config = @{ mcpServers = @{} }
            $needsUpdate = $true
        } else {
            $config = $configContent | ConvertFrom-Json -AsHashtable
        }
    } catch {
        Write-Host "Error reading config: $_" -ForegroundColor Red
        Write-Host "Creating new config" -ForegroundColor Yellow
        $config = @{ mcpServers = @{} }
        $needsUpdate = $true
    }
} else {
    # Create directory if needed
    $configDir = Split-Path $configPath
    if (-not (Test-Path $configDir)) {
        New-Item -ItemType Directory -Path $configDir -Force | Out-Null
    }
    $config = @{ mcpServers = @{} }
    $needsUpdate = $true
}

# Ensure mcpServers key exists (handle both Hashtable and PSCustomObject)
if ($config -is [System.Collections.Hashtable]) {
    if (-not $config.ContainsKey("mcpServers") -or $null -eq $config.mcpServers) {
        $config.mcpServers = @{}
        $needsUpdate = $true
    }
} else {
    # PSCustomObject from JSON - convert to hashtable for easier manipulation
    $configHash = @{}
    $config.PSObject.Properties | ForEach-Object { $configHash[$_.Name] = $_.Value }
    $config = $configHash
    if (-not $config.mcpServers) {
        $config.mcpServers = @{}
        $needsUpdate = $true
    }
}

# Convert mcpServers to hashtable if needed
if ($config.mcpServers -and $config.mcpServers -isnot [System.Collections.Hashtable]) {
    $serversHash = @{}
    $config.mcpServers.PSObject.Properties | ForEach-Object { $serversHash[$_.Name] = $_.Value }
    $config.mcpServers = $serversHash
}

# Check current state vs target state
if ($config.mcpServers.ContainsKey("computer-use")) {
    $current = $config.mcpServers["computer-use"]
    $currentJson = $current | ConvertTo-Json -Depth 5 -Compress
    $targetJson = $targetServer | ConvertTo-Json -Depth 5 -Compress
    
    if ($currentJson -eq $targetJson) {
        Write-Host "computer-use MCP already configured with correct settings" -ForegroundColor Green
        Write-Host "No changes needed" -ForegroundColor Gray
    } else {
        Write-Host "computer-use MCP exists but with different settings:" -ForegroundColor Yellow
        Write-Host "Current: $currentJson" -ForegroundColor Gray
        Write-Host "Target:  $targetJson" -ForegroundColor Gray
        $response = Read-Host "Update to target settings? (y/n)"
        if ($response -eq 'y') {
            $needsUpdate = $true
            $config.mcpServers["computer-use"] = $targetServer
        }
    }
} else {
    $needsUpdate = $true
    $config.mcpServers["computer-use"] = $targetServer
}

# Only write if changes are needed
if ($needsUpdate) {
    # Backup before modifying
    if (Test-Path $configPath) {
        $backupPath = "$configPath._beforeAddingComputerUseMcp_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
        try {
            Copy-Item $configPath $backupPath -ErrorAction Stop
            Write-Host "Backup: $backupPath" -ForegroundColor Cyan
        } catch {
            Write-Host "[FAIL] Could not create backup: $_" -ForegroundColor Red
            Write-Host "Aborting to prevent data loss" -ForegroundColor Yellow
            return
        }
    }
    
    try {
        $config | ConvertTo-Json -Depth 10 | Set-Content $configPath -Encoding UTF8 -ErrorAction Stop
        Write-Host "Added computer-use MCP to Windsurf" -ForegroundColor Green
    } catch {
        Write-Host "[FAIL] Could not write config: $_" -ForegroundColor Red
        if ($backupPath -and (Test-Path $backupPath)) {
            Write-Host "Restoring from backup..." -ForegroundColor Yellow
            Copy-Item $backupPath $configPath -Force
        }
        return
    }
}

# === Installation Summary ===
Write-Host ""
Write-Host "=== Installation Summary ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Installed components:" -ForegroundColor White

# MCP Config
Write-Host "  [C] MCP Config entry" -ForegroundColor Green
Write-Host "      Path: $configPath" -ForegroundColor Gray

# NPM package (downloaded on first use)
$npxCacheDir = "$env:LOCALAPPDATA\npm-cache\_npx"
$hasNpmCache = $false
if (Test-Path $npxCacheDir) {
    $computerUseCache = Get-ChildItem $npxCacheDir -Directory -ErrorAction SilentlyContinue | Where-Object {
        Test-Path "$($_.FullName)\node_modules\computer-use-mcp" -ErrorAction SilentlyContinue
    } | Select-Object -First 1
    if ($computerUseCache) {
        $hasNpmCache = $true
        Write-Host "  [N] NPM package (cached)" -ForegroundColor Green
        Write-Host "      Path: $($computerUseCache.FullName)" -ForegroundColor Gray
    }
}
if (-not $hasNpmCache) {
    Write-Host "  [N] NPM package (will download on first use)" -ForegroundColor Yellow
    Write-Host "      Path: $npxCacheDir\<hash>\node_modules\computer-use-mcp" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Next steps:" -ForegroundColor White
Write-Host "  1. Restart Windsurf" -ForegroundColor White
Write-Host "  2. Check MCP status: Command Palette > 'MCP: Show Servers'" -ForegroundColor White
Write-Host "  3. Test: Ask AI to 'Take a screenshot of my desktop'" -ForegroundColor White
Write-Host ""
Write-Host "IMPORTANT: This gives AI full control of mouse/keyboard!" -ForegroundColor Red
Write-Host "Consider using a sandboxed user account (see Section 9)" -ForegroundColor Yellow
Write-Host ""
```

## 8. Verify Installation

After configuring, restart Windsurf.

**Check MCP server status:**
1. View > Command Palette > "MCP: Show Servers"
2. computer-use should show green status
3. If red/orange: check Troubleshooting section

**Test basic operation:**

Ask Cascade: "Use the computer-use tools to take a screenshot and describe what you see"

**Expected behavior:**
1. Cascade should invoke the `computer` tool with action `screenshot`
2. You should see a brief pause while screenshot is captured
3. Cascade describes what it sees on your screen

**If Cascade doesn't use the tool:**
- Check MCP server is green in status
- Try: "Use the computer tool to capture my screen"
- Check which model Cascade is using (Claude Sonnet 4+ works best)

**If screenshot is black or wrong:**
- Multi-monitor: only primary monitor is captured
- GPU issue: update graphics drivers
- Permission issue: run Windsurf as Administrator (test only)

## 9. Recommended Setup for Best Results

### 9.1 Screen Resolution

Use 720p (1280x720) for better model accuracy.

**Windows - Change resolution:**
```powershell
# Check current resolution
Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.Screen]::PrimaryScreen.Bounds

# To change: Right-click desktop > Display settings > Resolution > 1280 x 720
```

**Windows - Virtual display (keep native resolution):**
Consider using tools like:
- displayoverride-mac (macOS only)
- Custom Resolution Utility (Windows)
- Or run in a VM at 720p

### 9.2 Rango Browser Extension

Install for keyboard-based browser navigation (more reliable than coordinate clicks):

**Chrome:**
https://chromewebstore.google.com/detail/rango/lnemjdnjjofijemhdogofbpcedhgcpmb

**After installation:**
1. Open Rango extension options
2. Increase font size for better visibility
3. Enable keyboard hints

**Why Rango helps:**
- Claude can type keyboard shortcuts instead of clicking coordinates
- Keyboard navigation is deterministic (coordinates are not)
- Works even if window position changes

### 9.3 Sandboxed User Account (Recommended)

For safety, create a separate Windows user account:

**Create sandboxed user:**
```powershell
# Run as Administrator
$username = "AIAutomation"
$password = ConvertTo-SecureString "YourSecurePassword123!" -AsPlainText -Force
New-LocalUser -Name $username -Password $password -Description "Sandboxed account for AI automation"
Add-LocalGroupMember -Group "Users" -Member $username

Write-Host "Created user: $username" -ForegroundColor Green
Write-Host "Log into this account for computer-use sessions" -ForegroundColor Yellow
```

**Switch to sandboxed user:**
1. Windows key > Click your profile icon > Switch user
2. Log into AIAutomation account
3. Run Windsurf and computer-use from there

**Benefits:**
- AI cannot access your personal files
- Mistakes are isolated to sandbox account
- Easy to reset/delete if something goes wrong

### 9.4 Clean Desktop

For better accuracy:
- Remove unnecessary desktop icons
- Close irrelevant windows
- Use a simple wallpaper (solid color or low contrast)
- Zoom in on the active window when possible

## 10. Security Considerations

### 10.1 Risk Assessment

**CRITICAL**: This MCP server gives AI:
- Full screenshot access to your entire screen
- Complete mouse control (click, drag, move)
- Complete keyboard control (type, shortcuts)
- Ability to interact with ANY application

**Risks:**
- Prompt injections can cause unintended actions
- Models make frequent mistakes (clicking wrong elements)
- Sensitive data visible on screen can be captured
- AI could accidentally delete files, send emails, etc.

### 10.2 Mitigation Strategies

**Minimal exposure:**
- Close sensitive applications before use
- Use sandboxed user account (Section 9.3)
- Don't leave password managers visible
- Log out of sensitive accounts in browser

**Supervision:**
- Always watch the screen during operation
- Be ready to move mouse to abort (nut.js releases on user input)
- Keep tasks simple and well-defined

**Network isolation (advanced):**
```powershell
# Disable network for sandboxed user (optional, run as Admin)
# This prevents AI from making external requests
netsh advfirewall firewall add rule name="Block AIAutomation" dir=out action=block `
    program="C:\Program Files\Windsurf\Windsurf.exe" `
    localuser="AIAutomation"
```

### 10.3 What NOT to do

- Never use on accounts with admin privileges
- Never leave banking/financial apps open
- Never give access to email with password resets
- Never run unattended for long periods
- Never use for tasks involving sensitive credentials

## 11. Troubleshooting

### MCP Server Not Loading

**Check 1: Node.js and npx**
```powershell
node --version   # Should be v18+
npx --version    # Should work
```

**Check 2: Config file location**
```powershell
$configPath = "$env:USERPROFILE\.codeium\windsurf\mcp_config.json"
if (Test-Path $configPath) {
    Get-Content $configPath | ConvertFrom-Json | ConvertTo-Json -Depth 5
} else {
    Write-Host "Config not found at: $configPath" -ForegroundColor Red
}
```

**Check 3: Test MCP manually**
```powershell
npx -y computer-use-mcp --help
```

### nut.js Permission Errors (Windows)

nut.js requires accessibility permissions to control mouse/keyboard.

**Error:** "Failed to get screen dimensions" or similar

**Fix 1: Run Windsurf as Administrator** (not recommended for security)

**Fix 2: Grant accessibility permissions**
- Windows Settings > Privacy & Security > Accessibility
- Ensure Windsurf has permission

**Fix 3: Check antivirus**
Some antivirus software blocks automation tools:
- Add Windsurf to exclusions
- Add npx cache folder to exclusions

### nut.js Permission Errors (macOS)

**Grant permissions:**
1. System Preferences > Security & Privacy > Privacy
2. Add Terminal/Windsurf to:
   - Accessibility
   - Screen Recording

### Model Accuracy Issues

**Symptoms:** AI clicks wrong elements, misinterprets screen content

**Solutions:**
1. **Reduce resolution** - 720p works best
2. **Zoom in** - Focus on active window
3. **Clean desktop** - Remove visual clutter
4. **Use Rango** - Keyboard navigation is more reliable
5. **Better model** - Use Claude Sonnet 4+ or Opus 4+
6. **Clear instructions** - Be specific about what to click

### Screenshot Capture Issues

**Error:** Black screen or partial capture

**Possible causes:**
- GPU acceleration issues
- Multi-monitor confusion
- Permission denied

**Fix:**
```powershell
# Check display info
Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.Screen]::AllScreens | ForEach-Object {
    Write-Host "Display: $($_.DeviceName) - $($_.Bounds.Width)x$($_.Bounds.Height)" -ForegroundColor Cyan
}
```

### Mouse/Keyboard Not Working

**Error:** AI reports actions but nothing happens

**Check nut.js directly:**
```powershell
# Test if nut.js can control input
npx -y @nut-tree/nut-js --version
```

**Common fixes:**
- Restart Windsurf
- Check no other automation tool is running
- Verify accessibility permissions
- Try running as different user

## 12. Alternative: Playwriter (Browser-Only)

If you only need browser automation with logged-in sessions, Playwriter is safer and more reliable:

```json
{
  "mcpServers": {
    "playwriter": {
      "command": "npx",
      "args": ["playwriter@latest"]
    }
  }
}
```

**Plus install Chrome extension:**
https://chromewebstore.google.com/detail/playwriter

**Benefits over computer-use-mcp:**
- You keep mouse/keyboard control
- AI interacts via DOM (more reliable than coordinates)
- Works alongside you in same browser
- Uses existing logged-in sessions
- Cannot access desktop applications (safer)

**Use computer-use-mcp only when:**
- You need desktop app automation (not just browser)
- Target app uses canvas/WebGL that Playwright cannot handle
- You need cross-application workflows

## 13. Completion Checklist

- [ ] Node.js 18+ installed
- [ ] npx accessible (full path if needed)
- [ ] Ran setup script (Section 7)
- [ ] Restarted Windsurf
- [ ] MCP server shows green status
- [ ] Test screenshot works
- [ ] (Recommended) Screen resolution set to 720p
- [ ] (Recommended) Rango extension installed
- [ ] (Recommended) Sandboxed user account created
- [ ] (Important) Understood security risks

## Quick Reference

- **Default config** - Basic desktop automation
- **+ Rango extension** - Browser interactions via keyboard
- **+ 720p resolution** - Better model accuracy
- **+ Sandboxed user** - Safer operation
- **Playwriter instead** - Browser-only, keep mouse control

## References

- **Repository**: https://github.com/domdomegg/computer-use-mcp
- **nut.js (input control)**: https://github.com/nut-tree/nut.js
- **Anthropic Computer Use docs**: https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool
- **Rango extension**: https://chromewebstore.google.com/detail/rango/lnemjdnjjofijemhdogofbpcedhgcpmb
