# INFO: How Playwriter MCP Works

**Doc ID**: PLWR-IN01
**Goal**: Document Playwriter MCP architecture, installation, and usage for agent-controlled browser automation
**Strategy**: MEPI (practical, curated)
**Domain**: SOFTWARE

**Version scope**: playwriter@latest as of 2026-03-15

## Summary

Playwriter is a Chrome extension + CLI (Command Line Interface)/MCP (Model Context Protocol) that lets AI agents control your **real browser** with existing logins, cookies, and extensions. Unlike Playwright MCP (which spawns a fresh browser instance), Playwriter connects to tabs you explicitly enable via the extension icon.

**Key differentiator**: Uses `chrome.debugger` API to connect to your running Chrome, inheriting all logged-in sessions. No separate browser process, no bot detection flags, full Playwright API.

## Architecture

```
+---------------------+    +-------------------+    +-----------------+
|      BROWSER        |    |     LOCALHOST     |    |   MCP CLIENT    |
|                     |    |                   |    |                 |
| +---------------+   |    | WebSocket Server  |    | +-----------+   |
| |  Extension    |<-------> :19988            |    | | AI Agent  |   |
| +-------+-------+   | WS |                   |    | +-----------+   |
|         |           |    |  /extension       |    |       |         |
|  chrome.debugger    |    |                   |    |       v         |
|         v           |    |       v           |    |  /cdp/:id       |
| +-----------+       |    | +---------------+ |    |                 |
| | Tab (green) |<----------->|   execute    |<-----> Playwright API  |
| +-----------+       |    | +---------------+ |    |                 |
| | Tab (gray)  |     |    |                   |    |                 |
+---------------------+    +-------------------+    +-----------------+
     (not controlled)
```

**Flow**:
1. Extension attaches to tab via `chrome.debugger` when you click its icon (turns green)
2. Extension opens WebSocket to local relay server on `localhost:19988`
3. CLI/MCP client connects to same relay
4. CDP (Chrome DevTools Protocol) commands flow through relay to extension to Chrome

## Key Components

**Chrome Extension** (from Chrome Web Store)
- Attaches to tabs via `chrome.debugger` API
- WebSocket connection to local relay (`localhost:19988`)
- Icon indicates state: green = connected, gray = not attached
- Chrome shows automation banner on controlled tabs

**CLI** (`npm i -g playwriter`)
- Session management: `playwriter session new`, `session list`, `session reset`
- Execute Playwright code: `playwriter -s <id> -e '<code>'`
- Variables in scope: `page`, `context`, `state` (persists), `require`

**MCP Server** (optional, skill-based recommended)
- Direct config: `npx playwriter@latest` in mcp_config.json
- Skill-based (recommended): `npx -y skills add remorses/playwriter`

**WebSocket Relay** (`localhost:19988`)
- Multiplexes sessions (multiple agents can share browser)
- Forwards CDP commands between clients and extension
- Log file: `~/.playwriter/relay-server.log`

## Session Model

Each session has **isolated state** but shares browser tabs:

```bash
playwriter session new          # Creates sandbox, outputs ID (e.g., 1)
playwriter -s 1 -e '<code>'     # Execute in session 1
playwriter session list         # Show sessions + state keys
playwriter session reset <id>   # Fix connection issues
```

**State persistence**: Use `state.varName` to persist data between calls:
```javascript
playwriter -s 1 -e "state.users = await page.$$eval('.user', els => els.map(e => e.textContent))"
playwriter -s 1 -e "console.log(state.users)"
```

**Create isolated pages**: Avoid interference from other agents:
```javascript
playwriter -s 1 -e 'state.myPage = await context.newPage(); await state.myPage.goto("https://example.com")'
```

## Screenshots

**Basic screenshot**:
```javascript
await page.screenshot({ path: 'screenshot.png' })
```

**Full page screenshot**:
```javascript
await page.screenshot({ path: 'fullpage.png', fullPage: true })
```

**JPEG (smaller file)**:
```javascript
await page.screenshot({ path: 'screenshot.jpg', type: 'jpeg', quality: 80 })
```

## Visual Labels Feature

Vimium-style labels for AI element identification:

```javascript
await screenshotWithAccessibilityLabels({ page })
// Returns screenshot + accessibility snapshot with aria-ref selectors
await page.locator('aria-ref=e5').click()
```

**Color coding**:
- Yellow = links
- Orange = buttons
- Coral = inputs
- Pink = checkboxes
- Peach = sliders
- Salmon = menus
- Amber = tabs

## Accessibility Snapshot (No Screenshot)

Get accessibility tree without taking a screenshot:
```javascript
await snapshot({ page })
// Returns accessibility tree with aria-ref selectors
```

## MCP Configuration

**Skill-based (recommended)**:
```bash
npx -y skills add remorses/playwriter
```

**Direct MCP config** (mcp_config.json):
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

## Comparison with Playwright MCP

- **Playwriter**: Uses YOUR browser with existing logins, cookies, extensions. No bot detection. Single Chrome process.
- **Playwright MCP**: Spawns fresh browser. Clean slate. Double memory. Often flagged by bot detectors.

**When to use Playwriter**:
- Need existing logged-in sessions
- Want to use ad blockers, password managers
- Avoiding automation detection
- Collaborating with AI (you see what it does in real-time)

**When to use Playwright MCP**:
- Need clean, isolated sessions
- Testing without user state
- Standard automation tasks

## Screen Recording [ASSUMED]

Record browser session as MP4 video:

```javascript
// Start recording
await startRecording({ page, outputPath: './recording.mp4', frameRate: 30 })

// Navigate, interact - recording continues across page navigations
await page.click('a')
await page.waitForLoadState('domcontentloaded')
await page.goBack()

// Stop and save
await stopRecording({ page })
```

**Features**:
- Uses `chrome.tabCapture` - survives page navigation
- 30-60fps recording
- Check status: `await isRecording({ page })`
- Cancel without saving: `await cancelRecording({ page })`

## Debugger and Live Editing [ASSUMED]

**Set breakpoints**:
```javascript
state.cdp = await getCDPSession({ page })
state.dbg = createDebugger({ cdp: state.cdp })
await state.dbg.enable()

// List scripts
state.scripts = await state.dbg.listScripts({ search: 'app' })
console.log(state.scripts.map(s => s.url))

// Set breakpoint
await state.dbg.setBreakpoint({ file: state.scripts[0].url, line: 42 })
```

**Live edit page code**:
```javascript
state.cdp = await getCDPSession({ page })
state.editor = createEditor({ cdp: state.cdp })
await state.editor.enable()

await state.editor.edit({
  url: 'https://example.com/app.js',
  oldString: 'const DEBUG = false',
  newString: 'const DEBUG = true'
})
```

## Security Model

- **Local only**: WebSocket binds to `localhost:19988` (note: any local process can connect; use `--token` for authenticated access)
- **Origin validation**: Only Playwriter extension origin accepted (browsers cannot spoof Origin header)
- **Explicit consent**: Only tabs where you clicked extension icon are controlled
- **Visible automation**: Chrome shows automation banner on controlled tabs
- **No remote by default**: Malicious websites cannot connect

## Remote Access

Control Chrome on remote machine via traforo tunnels:

**On host**:
```bash
npx -y traforo -p 19988 -t my-machine -- npx -y playwriter serve --token <secret>
```

**From remote**:
```bash
export PLAYWRITER_HOST=https://my-machine-tunnel.traforo.dev
export PLAYWRITER_TOKEN=<secret>
playwriter -s 1 -e 'await page.goto("https://example.com")'
```

LAN access: `PLAYWRITER_HOST=192.168.1.10` (no tunnel needed)

## Programmatic API

Connect without CLI:
```javascript
import { chromium } from 'playwright-core'
import { startPlayWriterCDPRelayServer, getCdpUrl } from 'playwriter'

const server = await startPlayWriterCDPRelayServer()
const browser = await chromium.connectOverCDP(getCdpUrl())
const page = browser.contexts()[0].pages()[0]

await page.goto('https://example.com')
await page.screenshot({ path: 'screenshot.png' })

// Don't call browser.close() - it closes user's Chrome!
server.close()
```

## Known Issues

- If all pages return `about:blank`, restart Chrome (Chrome bug in `chrome.debugger` API)
- Browser may switch to light mode on connect (Playwright issue #37627)

## Troubleshooting

View relay server logs:
```bash
playwriter logfile  # prints log file path (~/.playwriter/relay-server.log)
```

CDP traffic analysis:
```bash
jq -r '.direction + "\t" + (.message.method // "response")' ~/.playwriter/cdp.jsonl | uniq -c
```

## Common Use Cases

**User wants to...**
- **Check bank account / pay bills** -> Use existing logged-in session, visual labels for navigation
- **Read email / send messages** -> Existing Gmail/Outlook session, no re-auth needed
- **Post to social media** -> Existing Twitter/LinkedIn session, bypass bot detection
- **Fill government forms** -> Use saved passwords, extensions, existing auth
- **Scrape authenticated content** -> No login flow needed, use existing cookies
- **Debug web app** -> Set breakpoints, live edit code, record session
- **Record demo/tutorial** -> Screen recording with `startRecording`
- **Collaborate with AI** -> You see what AI does in real-time, can intervene

**Technical tasks...**
- **Get element refs** -> `await snapshot({ page })` or `await screenshotWithAccessibilityLabels({ page })`
- **Click by ref** -> `await page.locator('aria-ref=e5').click()`
- **Persist data** -> `state.varName = ...` survives between calls
- **Intercept API calls** -> `page.on('response', ...)` with state persistence
- **Record session** -> `startRecording` / `stopRecording`

## Sources

- `PLWR-IN01-SC-RMRS-GH`: https://github.com/remorses/playwriter [VERIFIED]
- `PLWR-IN01-SC-RMRS-DEV`: https://playwriter.dev [VERIFIED]
- `PLWR-IN01-SC-RMRS-CWS`: Chrome Web Store extension page [VERIFIED]

Accessed: 2026-03-15

## Document History

**[2026-03-15 14:55]**
- Added [ASSUMED] labels to untested features (Screen Recording, Debugger)
- Added localhost security note
- Fixed version scope to include date

**[2026-03-15 14:50]**
- Added Screenshots, Screen Recording, Debugger, Common Use Cases sections
- Added Accessibility Snapshot section

**[2026-03-15 14:48]**
- Initial creation via /deep-research workflow
- Documented architecture, CLI, MCP setup, security model
