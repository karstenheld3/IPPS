# Playwriter MCP Setup

Run once to configure Playwriter for real browser automation with existing logins.

## 1. Verify Node.js

```powershell
node --version
npm --version
```

Expected: Node.js 18+. If missing: https://nodejs.org

## 2. Install Chrome Extension

https://chromewebstore.google.com/detail/playwriter-mcp/jfeammnjpkecdekppnclgkkffahnhfhe

- Click extension icon on tab to control it
- Green = connected, Gray = not attached

## 3. Install CLI

```powershell
npm i -g playwriter
playwriter --help
```

## 4. Test Connection

```powershell
playwriter session new
# Multiple browsers? Specify: playwriter session new --browser "browser:Chrome"
playwriter -s 1 -e 'await page.goto("https://example.com")'
```

## 5. Install Skill for Agents (Recommended)

```powershell
npx -y skills add remorses/playwriter
```

## 6. Add to Windsurf MCP Config (Optional)

Target config entry:
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

Config path: `$env:USERPROFILE\.codeium\windsurf\mcp_config.json`

Essential steps:
1. Read existing config or create `{ "mcpServers": {} }`
2. Convert PSCustomObject to Hashtable if needed
3. Add `playwriter` server entry
4. Backup before writing, save as UTF8

After adding, restart Windsurf. Check: Command Palette > "MCP: Show Servers"

## Troubleshooting

### Extension Icon Not Turning Green
- Click directly on icon (not right-click)
- Must be normal webpage (not chrome://, about:, extension pages)

### Connection Errors
```powershell
playwriter session reset 1
```

### View Logs
```powershell
playwriter logfile
```

### All Pages Return about:blank
Restart Chrome completely (known Chrome bug).

## 8. Configuration Options

### Environment Variables

```powershell
$env:PLAYWRITER_HOST = "192.168.1.10"       # Remote host (LAN or tunnel URL)
$env:PLAYWRITER_TOKEN = "your-secret-token"  # Required for remote access
```

### MCP Config with Environment Variables

```json
{
  "mcpServers": {
    "playwriter": {
      "command": "npx",
      "args": ["playwriter@latest"],
      "env": {
        "PLAYWRITER_HOST": "192.168.1.10",
        "PLAYWRITER_TOKEN": "your-secret-token"
      }
    }
  }
}
```

### Server Mode (remote access)

```powershell
npx -y playwriter serve --token <secret>
# With tunnel:
npx -y traforo -p 19988 -t my-machine -- npx -y playwriter serve --token <secret>
```

## Quick Reference

- **Extension**: Click icon on tab (green = active)
- **CLI**: `playwriter -s <id> -e '<code>'`
- **Session**: `playwriter session new` / `list` / `reset`
- **Logs**: `playwriter logfile`
- **WebSocket**: `localhost:19988`
- **Remote**: Set `PLAYWRITER_HOST` and `PLAYWRITER_TOKEN`