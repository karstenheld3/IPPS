---
name: ms-playwright-mcp
description: Apply when automating browser interactions, web scraping, or UI testing with AI agents
---

# Playwright MCP Guide

Reference files:
- [PLAYWRIGHT_ADVANCED_WORKFLOWS.md](PLAYWRIGHT_ADVANCED_WORKFLOWS.md) - Cookie popups, scrolling, expanding items
- [PLAYWRIGHT_AUTHENTICATION.md](PLAYWRIGHT_AUTHENTICATION.md) - Persistent profiles, storage state
- [PLAYWRIGHT_FULL_PAGE_SCREENSHOT.md](PLAYWRIGHT_FULL_PAGE_SCREENSHOT.md) - Complete page capture
- [PLAYWRIGHT_TROUBLESHOOTING.md](PLAYWRIGHT_TROUBLESHOOTING.md) - Common issues, debugging
- [SETUP.md](SETUP.md) - Installation

## Intent Lookup

- Research/read articles → Navigate, dismiss cookie popup, scroll lazy content, screenshot
- Find product/compare → Navigate, search, `browser_evaluate` to extract data
- Fill form/submit → `browser_fill` for fields, `browser_click` for submit
- Download file → Find links via [Advanced Workflows Section 5](PLAYWRIGHT_ADVANCED_WORKFLOWS.md#5-find-and-extract-links), click to download
- Log into site → Fill credentials, submit; use [PLAYWRIGHT_AUTHENTICATION.md](PLAYWRIGHT_AUTHENTICATION.md) to persist
- Bank transfer/pay bills → Requires persistent profile; `browser_snapshot` before each action
- Check email/attachments → Navigate webmail, expand messages, click attachment links
- Archive webpage → [Full page screenshot workflow](PLAYWRIGHT_ADVANCED_WORKFLOWS.md)
- Dynamic content → Scroll to load lazy content, expand collapsed sections, proceed
- Handle cookie popup → [Advanced Workflows #1](PLAYWRIGHT_ADVANCED_WORKFLOWS.md#1-close-cookie-popups)
- Run custom JavaScript → `browser_evaluate(expression: "...")`
- Debug failures → [PLAYWRIGHT_TROUBLESHOOTING.md](PLAYWRIGHT_TROUBLESHOOTING.md)
- UI testing: navigate+snapshot to verify load, submit invalid data for validation, click menus for nav flow, resize+screenshot for responsive, hover+click for button states, trigger/interact/close modals, force errors for error handling, snapshot for accessibility, before/after screenshots for comparison, full auth flow for login/logout

## MUST-NOT-FORGET

- Use accessibility tree (not screenshots) for element selection
- Reference elements via `ref=e5` format from `browser_snapshot`
- Always call `browser_snapshot` before clicking to get current refs
- NEVER auto-close browser: Only user may close browser - sessions preserve authentication state (banking, email, etc.)
- For logged-in sessions: Use persistent user profile or storage state
- Always use `type: "jpeg"` for screenshots (default is png, which produces unnecessarily large files)
- Downloads go to temp folder: `$env:TEMP\playwright-mcp-output\[session]\` - NOT user Downloads folder. Copy files to destination after download completes.

## Configuration

Repository: https://github.com/microsoft/playwright-mcp
Package: `@playwright/mcp`

Basic (isolated session):
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

Persistent profile (remembers logins):
```json
{
  "args": ["@playwright/mcp@latest", "--user-data-dir", "[USER_PROFILE_PATH]/.ms-playwright-mcp-profile"]
}
```

Headless: Add `"--headless"` to args.

Timeouts: Add `"--timeout-action", "10000", "--timeout-navigation", "120000"` for slow pages.

## Available Tools

### Navigation
- browser_navigate - `browser_navigate(url: "https://example.com")`

### Element Interaction
- browser_snapshot - Get accessibility tree with element refs
- browser_click - `browser_click(element: "Button", ref: "e12")`
- browser_type - `browser_type(element: "Input", ref: "e8", text: "query")`
- browser_fill - `browser_fill(element: "Email", ref: "e3", value: "user@example.com")`
- browser_select - `browser_select(element: "Country", ref: "e15", values: ["USA"])`
- browser_hover - `browser_hover(element: "Menu", ref: "e5")`
- browser_drag - Drag and drop between elements
- browser_press_key - `browser_press_key(key: "Enter")` or `browser_press_key(key: "Control+A")`

### Inspection
- browser_screenshot - `browser_screenshot(type: "jpeg")` or `browser_screenshot(fullPage: true, type: "jpeg")`
- browser_console_messages - Get console logs
- browser_evaluate - `browser_evaluate(expression: "document.title")`

### Timing
- browser_wait_for - `browser_wait_for(time: 2)` wait seconds, or `browser_wait_for(text: "Loading")` wait for text

### Session
- browser_close - Close browser and free resources

## Common Workflows

### Navigate and Click
```
1. browser_navigate(url: "https://example.com")
2. browser_snapshot()
3. browser_click(element: "Login button", ref: "e12")
```

### Fill Form
```
1. browser_snapshot()
2. browser_fill(element: "Username", ref: "e3", value: "user@example.com")
3. browser_fill(element: "Password", ref: "e5", value: "password123")
4. browser_click(element: "Submit", ref: "e8")
```

After navigation or click, call `browser_snapshot()` to verify page loaded and get updated refs.

For cookie popups, lazy-load scrolling, expanding collapsed items: see [PLAYWRIGHT_ADVANCED_WORKFLOWS.md](PLAYWRIGHT_ADVANCED_WORKFLOWS.md).

## Element Selection

1. Call `browser_snapshot()` to get current page structure
2. Find element in returned accessibility tree
3. Use the `ref` value in subsequent commands

Selector priority (when refs unavailable):
1. `[data-testid="submit"]` - Best
2. `getByRole('button', { name: 'Save' })` - Semantic
3. `getByText('Sign in')` - User-facing
4. `input[name="email"]` - HTML attributes
5. Avoid: `.btn-primary`, `#submit` - Classes/IDs change

## Requirements

- Node.js 18+ with npx in PATH
- Chrome/Chromium for headed mode