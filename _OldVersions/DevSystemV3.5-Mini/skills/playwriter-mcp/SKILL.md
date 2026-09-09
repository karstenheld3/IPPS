---
name: playwriter-mcp
description: ONLY apply when user EXPLICITLY mentions "Playwriter". Default browser automation is ms-playwright-mcp.
---

# Playwriter MCP Guide

ACTIVATION: Only use when user explicitly says "Playwriter". Default browser MCP is `ms-playwright-mcp`.

## When to Use Playwriter (vs Playwright MCP)

Use Playwriter when: existing logged-in sessions (bank, email, social media), ad blockers/password managers/extensions needed, avoiding bot detection, real-time AI collaboration

Use Playwright MCP when: clean isolated sessions, testing without user state, standard automation

## Intent Lookup

- Bank/bills/email/social/gov forms/authenticated scraping -> Existing session, cookies, extensions
- Debug web app -> `getCDPSession`, `createDebugger`, breakpoints
- Record demo -> `startRecording` / `stopRecording`
- Get element refs -> `snapshot({ page })` or `screenshotWithAccessibilityLabels({ page })`
- Click by ref -> `page.locator('aria-ref=e5').click()`
- Persist data -> `state.varName = ...`
- Intercept API -> `page.on('response', ...)`

## MUST-NOT-FORGET

- Install Chrome extension FIRST (from Chrome Web Store)
- Click extension icon on tab to enable control (icon turns green)
- Use single quotes for `-e` to prevent bash interpretation
- Never call `browser.close()` - it closes YOUR Chrome
- Use `state.varName` to persist data between calls
- Green icon = connected, gray = not controlled
- TIMEOUTS: ALWAYS pass timeout (default 20000ms is too long!). Use `1500` for simple ops, `3000` for screenshots.
- NO waitForTimeout inside code - causes stalls. Use proper waits like `waitForSelector` instead.
- goto() stalls on SPAs - default `waitUntil: 'load'` never fires on SharePoint/dynamic sites. Use `{ waitUntil: 'domcontentloaded' }`.
- click() can stall - if element triggers animation/loading that blocks. Don't click multiple elements in one call.
- After any cancellation - always check connection before proceeding with more operations.
- If stalled, reset won't work - user must restart Chrome or click extension icon again.

## CLI Commands

```bash
playwriter session new          # Create sandbox, get ID
playwriter session list         # Show sessions + state keys
playwriter session reset <id>   # Fix connection issues
playwriter -s <id> -e '<code>' # Run Playwright code in session
```

Variables in scope: `page`, `context`, `state`, `require`

## Key Operations

```bash
# Navigate + screenshot
playwriter -s 1 -e 'await page.goto("https://example.com")'
playwriter -s 1 -e 'await page.screenshot({ path: "shot.jpg", type: "jpeg", quality: 80, fullPage: true })'

# Visual labels (Vimium-style) + click
playwriter -s 1 -e 'await screenshotWithAccessibilityLabels({ page })'
playwriter -s 1 -e 'await page.locator("aria-ref=e5").click()'

# Accessibility snapshot (no screenshot)
playwriter -s 1 -e 'console.log(await snapshot({ page }))'

# Persist data between calls
playwriter -s 1 -e "state.users = await page.$$eval('.user', els => els.map(e => e.textContent))"

# Intercept network
playwriter -s 1 -e "state.requests = []; page.on('response', r => { if (r.url().includes('/api/')) state.requests.push(r.url()) })"

# Screen recording [ASSUMED]
playwriter -s 1 -e 'await startRecording({ page, outputPath: "./recording.mp4", frameRate: 30 })'
playwriter -s 1 -e 'await stopRecording({ page })'
```

Visual label colors: Yellow=links, Orange=buttons, Coral=inputs, Pink=checkboxes, Peach=sliders, Salmon=menus, Amber=tabs

## MCP Configuration

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

## Troubleshooting

- All pages return about:blank -> Restart Chrome (known `chrome.debugger` bug)
- Extension not turning green -> Click directly on icon (not right-click), try `playwriter session reset <id>`
- View logs -> `playwriter logfile` (path to `~/.playwriter/relay-server.log`)

## Security

- WebSocket binds to `localhost:19988` only (use `--token` for auth)
- Only tabs where you clicked extension icon are controlled
- Chrome shows automation banner on controlled tabs

## Requirements

- Chrome/Chromium, Node.js 18+ with npm, Playwriter Chrome extension
- See [SETUP.md](SETUP.md) for installation