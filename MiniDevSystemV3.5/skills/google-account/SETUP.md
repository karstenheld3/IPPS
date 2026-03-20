# Google Account Skill Setup (gogcli)

## Agent Invocation (from PowerShell)

**CRITICAL**: WSL PATH is often broken. Always use this pattern:

```powershell
wsl bash -c "export PATH='/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/linuxbrew/.linuxbrew/bin'; gog <command>"
```

Example (with auth):
```powershell
wsl bash -c "export PATH='/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/linuxbrew/.linuxbrew/bin'; export GOG_ACCOUNT='you@gmail.com'; export GOG_KEYRING_PASSWORD='pass'; gog --json gmail search 'is:unread' --max 5"
```

**Current status**:
- [x] gogcli installed: v0.11.0 at `/home/linuxbrew/.linuxbrew/bin/gog`
- [ ] OAuth credentials configured
- [ ] Account authorized

## Quick OAuth Setup (Agent-Assisted via Playwright MCP)

### Step 1: Create Project
`https://console.cloud.google.com/projectcreate` - Name: `gogcli-personal`, note PROJECT_ID

### Step 2: Enable APIs
Navigate to each and click Enable:
- `https://console.cloud.google.com/apis/library/gmail.googleapis.com?project={PROJECT_ID}`
- `https://console.cloud.google.com/apis/library/calendar-json.googleapis.com?project={PROJECT_ID}`
- `https://console.cloud.google.com/apis/library/drive.googleapis.com?project={PROJECT_ID}`
- `https://console.cloud.google.com/apis/library/tasks.googleapis.com?project={PROJECT_ID}`
- `https://console.cloud.google.com/apis/library/people.googleapis.com?project={PROJECT_ID}`

### Step 3: Configure OAuth Consent
`https://console.cloud.google.com/apis/credentials/consent?project={PROJECT_ID}`
- App name: `gogcli`, Audience: **External**, your email for support + developer contact

### Step 4: Add Test User (CRITICAL)
`https://console.cloud.google.com/auth/audience?project={PROJECT_ID}` - Add your email.
**Without this step, OAuth will fail with "Error 403: access_denied"**

### Step 5: Create OAuth Client
`https://console.cloud.google.com/auth/clients/create?project={PROJECT_ID}`
- Type: Desktop app, Name: `gogcli-desktop`, Download JSON

### Step 6: Store Credentials
```powershell
Copy-Item "$env:TEMP\playwright-mcp-output\*\client-secret-*.json" -Destination "$env:USERPROFILE\.gogcli\client-secret.json"
wsl bash -c "export PATH='/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/linuxbrew/.linuxbrew/bin'; gog auth credentials /mnt/c/Users/\$USER/.gogcli/client-secret.json"
```

### Step 7: Authorize Account

**Method A: Automated with Playwright MCP**
1. Start auth (non-blocking): `gog auth add your@gmail.com --services gmail --manual`
2. Agent navigates to auth URL via Playwright MCP, clicks through consent
3. Browser redirects to localhost (ERR_CONNECTION_REFUSED expected)
4. Capture redirect URL from `mcp1_browser_network_requests`
5. Pipe redirect URL: `echo "<REDIRECT_URL>" | gog auth add your@gmail.com --services gmail --manual`

**Method B: Manual in WSL**
```bash
export PATH='/home/linuxbrew/.linuxbrew/bin:$PATH'
export GOG_KEYRING_PASSWORD='gogcli'
gog auth add your@gmail.com --manual
```

### Verify
```powershell
wsl bash -c "export PATH='/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/linuxbrew/.linuxbrew/bin'; export GOG_KEYRING_PASSWORD='gogcli'; gog auth status"
```

## Pre-Installation Verification

### 1. Check WSL
```powershell
wsl --version
```
If not installed: `wsl --install` (Admin PowerShell), restart, run `wsl`

### 2. Check Homebrew in WSL
```bash
brew --version
```
If not installed:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> ~/.bashrc
```

### 3. Check Go (only if building from source)
`go version` - Expected: go1.21+. Install: https://go.dev/dl/

## Installation

### Install gogcli

**Option A: WSL with Homebrew (Recommended)**
```bash
brew install steipete/tap/gogcli
gog --version
```

**Option B: Build from Source (Windows)**
```powershell
git clone https://github.com/steipete/gogcli.git
cd gogcli
go build -o bin/gog.exe ./cmd/gog
```

**Option C: Build from Source (WSL)**
```bash
git clone https://github.com/steipete/gogcli.git
cd gogcli && make
export PATH="$PATH:$PWD/bin"
```

### Google Cloud Setup (Steps 2-5)

Same as Quick OAuth Setup Steps 1-5 above.

### Store Credentials
```bash
gog auth credentials ~/.tools/gogcli-client-secret.json
```

### Authorize Account

**Interactive**: `gog auth add you@gmail.com`

**Headless**: `gog auth add you@gmail.com --services user --manual` - copy URL, approve in browser, paste redirect URL back.

### Configure for Agent Automation
```bash
gog auth keyring file
```

Add to `~/.bashrc`:
```bash
export GOG_ACCOUNT='you@gmail.com'
export GOG_KEYRING_BACKEND='file'
export GOG_KEYRING_PASSWORD='your-secure-password'
export GOG_ENABLE_COMMANDS='gmail,calendar,tasks,drive'
```

### Verify Setup
```bash
gog auth status
gog gmail labels list
gog --json gmail search 'is:unread' --max 5
```

### Create Attachments Directory
```bash
mkdir -p [TOOLS_FOLDER]/_downloaded_attachments
```

## Troubleshooting

**"No credentials found"**: `gog auth credentials ~/path/to/client_secret.json`

**"Token expired"/"Invalid grant"**: `gog auth add you@gmail.com --force-consent`

**"Keyring password required"**: `export GOG_KEYRING_PASSWORD='your-password'`

**WSL "gog: command not found"**: `eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"` or `export PATH="$PATH:~/gogcli/bin"`

**Permission denied**: Ensure APIs enabled in Google Cloud Console.

## Security Notes

- Store `client_secret.json` outside workspace (not in git)
- Use environment variables for `GOG_KEYRING_PASSWORD`
- Never commit credentials or tokens
- Use `GOG_ENABLE_COMMANDS` to restrict available commands