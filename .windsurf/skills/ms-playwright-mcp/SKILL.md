---
name: ms-playwright-mcp
description: Apply when automating browser interactions, web scraping, or UI testing with AI agents
---

# Playwright MCP Guide

Rules and usage for Microsoft Playwright MCP server.

## MUST-NOT-FORGET

- Use accessibility tree (not screenshots) for element selection
- Reference elements via `aria-ref=e5` format from browser_snapshot
- Always call `browser_snapshot` before clicking to get current element refs
- Use `browser_close` when done to free resources
- For logged-in sessions: Use Playwriter extension or persistent user profile

## MCP Server Options

### Option 1: Microsoft Playwright MCP (Official)

Best for: Clean browser sessions, automated testing, headless operation.

**Repository**: https://github.com/microsoft/playwright-mcp
**Package**: `@playwright/mcp`

### Option 2: Playwriter (Chrome Extension)

Best for: Existing logged-in sessions, working alongside user, bypassing detection.

**Repository**: https://github.com/remorses/playwriter
**Package**: `playwriter`

## Configuration

### Microsoft Playwright MCP

**Basic configuration (isolated session):**
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

**Persistent user profile (remembers logins):**
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": [
        "@playwright/mcp@latest",
        "--user-data-dir", "[USER_PROFILE_PATH]/.ms-playwright-mcp-profile"
      ]
    }
  }
}
```

**Headless mode:**
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest", "--headless"]
    }
  }
}
```

### Playwriter (Chrome Extension)

1. Install Chrome extension from Chrome Web Store
2. Configure MCP:
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

## Available Tools

### Navigation

**browser_navigate** - Go to URL
```
browser_navigate(url: "https://example.com")
```

### Element Interaction

**browser_snapshot** - Get accessibility tree with element refs
```
browser_snapshot()
// Returns tree with refs like: link "Home" [ref=e5]
```

**browser_click** - Click element by ref
```
browser_click(element: "Submit button", ref: "e12")
// Options: modifiers (Control, Shift, Alt), doubleClick
```

**browser_type** - Type text (clears existing, use for inputs)
```
browser_type(element: "Search input", ref: "e8", text: "search query")
```

**browser_fill** - Fill form field
```
browser_fill(element: "Email", ref: "e3", value: "user@example.com")
```

**browser_select** - Select dropdown option
```
browser_select(element: "Country", ref: "e15", values: ["USA"])
```

### Advanced Interactions

**browser_drag** - Drag and drop
```
browser_drag(
  startElement: "Draggable item", startRef: "e10",
  endElement: "Drop zone", endRef: "e20"
)
```

**browser_hover** - Hover over element
```
browser_hover(element: "Menu", ref: "e5")
```

**browser_press_key** - Press keyboard key
```
browser_press_key(key: "Enter")
browser_press_key(key: "Control+A")
```

### Inspection

**browser_screenshot** - Capture page screenshot
```
browser_screenshot()
// Options: raw (base64 instead of file)
```

**browser_console_messages** - Get console logs
```
browser_console_messages()
// Options: level (error, warning, info)
```

**browser_evaluate** - Execute JavaScript
```
browser_evaluate(expression: "document.title")
```

### Session Management

**browser_close** - Close browser and free resources
```
browser_close()
```

## Common Workflows

### 1. Navigate and Click

```
1. browser_navigate(url: "https://example.com")
2. browser_snapshot()  // Get current element refs
3. browser_click(element: "Login button", ref: "e12")
```

### 2. Fill Form and Submit

```
1. browser_snapshot()
2. browser_fill(element: "Username", ref: "e3", value: "user@example.com")
3. browser_fill(element: "Password", ref: "e5", value: "password123")
4. browser_click(element: "Submit", ref: "e8")
```

### 3. Wait for Content

After navigation or click, call `browser_snapshot()` again to:
- Verify page loaded correctly
- Get updated element refs
- Check for expected content

### 4. Extract Data

```
1. browser_snapshot()  // Get page content
2. browser_evaluate(expression: "document.querySelector('.price').textContent")
```

## Element Selection Best Practices

### Using Refs from Snapshot

1. Call `browser_snapshot()` to get current page structure
2. Find element in returned accessibility tree
3. Use the `ref` value (e.g., `e5`) in subsequent commands

**Example snapshot output:**
```
- banner [ref=e3]:
    - link "Home" [ref=e5] [cursor=pointer]:
        - /url: /
    - navigation [ref=e12]:
        - link "Docs" [ref=e13] [cursor=pointer]
```

### Selector Priority

When refs are not available, use stable selectors:
1. `[data-testid="submit"]` - Best, explicit test attribute
2. `getByRole('button', { name: 'Save' })` - Semantic, accessible
3. `getByText('Sign in')` - User-facing text
4. `input[name="email"]` - HTML attributes
5. Avoid: `.btn-primary`, `#submit` - Classes/IDs change frequently

## Authentication Strategies

### Strategy 1: Persistent User Profile

Configure `--user-data-dir` to persist cookies and login state:
```json
{
  "args": [
    "@playwright/mcp@latest",
    "--user-data-dir", "[USER_PROFILE_PATH]/.ms-playwright-mcp-profile"
  ]
}
```

### Strategy 2: Storage State File

Save authentication state to file:
```javascript
// After login, save state
await context.storageState({ path: 'auth.json' });
```

Use with `--storage-state`:
```json
{
  "args": ["@playwright/mcp@latest", "--storage-state", "auth.json"]
}
```

### Strategy 3: Playwriter Extension

Use existing browser with logged-in sessions:
1. Log in manually in Chrome
2. Connect Playwriter extension
3. MCP uses your authenticated session

## Troubleshooting

### npx not found

Use full path to npx:
```json
{
  "command": "[NPX_FULL_PATH]"
}
```

### Profile lock errors

Reset profile lock:
```powershell
Remove-Item "[USER_PROFILE_PATH]\.ms-playwright-mcp-profile\SingletonLock" -Force -ErrorAction SilentlyContinue
```

### Extension mode not connecting

Known issue (GitHub #921): `--extension` flag may launch new Chrome.
Workaround: Use Playwriter extension instead.

### Element not found

1. Call `browser_snapshot()` to refresh refs
2. Wait for page to fully load
3. Check if element is in iframe (use `browser_evaluate` to access)

### Automation detection

If site blocks automation:
1. Use Playwriter with existing browser profile
2. Disconnect extension temporarily for sensitive sites
3. Use headed mode instead of headless

## Flaky Test Prevention

**Common causes:**
- Race conditions: Tests proceed before app ready
- Unstable selectors: IDs change between renders
- Network unpredictability: API response time varies
- State contamination: Tests share state

**Solutions:**
- Always call `browser_snapshot()` before interacting
- Use stable selectors (data-testid, roles, labels)
- Wait for specific elements, not arbitrary timeouts
- Isolate tests with fresh browser contexts

## Setup

For initial installation, see `SETUP.md` in this skill folder.

**Requirements:**
- Node.js 18+ with npx in PATH
- Chrome/Chromium for headed mode
- For Playwriter: Chrome extension installed
