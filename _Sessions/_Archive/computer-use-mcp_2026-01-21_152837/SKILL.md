---
name: computer-use-mcp
description: Desktop automation via Claude Computer Use MCP. Apply when automating desktop applications, canvas-based UIs, or full-screen interactions.
---

# Claude Computer Use

This skill provides guidance for using the `computer-use-mcp` server to give Cascade control of your desktop via screenshot analysis and mouse/keyboard control.

**Package**: `computer-use-mcp` (npm)
**Author**: domdomegg
**Underlying library**: nut.js (Node.js desktop automation)

## When to Use

- Desktop application automation (not just browser)
- Canvas/WebGL applications that DOM-based tools cannot handle
- Full-screen interactions requiring visual recognition
- Cross-application workflows
- Citrix/VDI environments where DOM access is unavailable

## When NOT to Use

- **Windsurf/Cascade** - MCP protocol incompatibility causes Cascade failures (see `MCPS-FL-008`)
- Browser-only automation with logged-in sessions (use Playwriter instead)
- Tasks requiring you to work alongside the AI (mouse/keyboard are hijacked)
- High-security environments (full desktop access is risky)
- Tasks requiring high precision (models make frequent coordinate errors)

## Compatibility

**Verified compatible:**
- Claude Desktop
- Cursor
- Cline

**NOT compatible:**
- Windsurf/Cascade - MCP protocol/tool schema issue, breaks all Cascade operations

**Platform support** (when using compatible clients):
- macOS - Full support via Core Graphics
- Linux - Full support via X11/libxdo
- Windows - Package runs, but untested with compatible clients

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│ Windsurf/Cascade                                                │
│   └─> MCP Protocol (stdio)                                      │
│         └─> computer-use-mcp (Node.js)                          │
│               └─> nut.js library                                │
│                     ├─> Screen: grab(), width(), height()       │
│                     ├─> Mouse: move(), click(), drag()          │
│                     └─> Keyboard: type(), pressKey(), hotkey()  │
│                           └─> Native OS APIs                    │
│                                 ├─> Windows: Win32 API          │
│                                 ├─> macOS: Core Graphics        │
│                                 └─> Linux: X11/libxdo           │
└─────────────────────────────────────────────────────────────────┘
```

## Tool Actions

The MCP server exposes a single `computer` tool with the following actions:

### Screenshot Actions

- **`screenshot`** - Capture full screen, returns base64 PNG image

### Mouse Actions

- **`mouse_move`** - Move cursor to (x, y) coordinates
- **`left_click`** - Single left click at current position
- **`right_click`** - Single right click at current position
- **`double_click`** - Double left click at current position
- **`left_click_drag`** - Click and drag from current to (x, y)
- **`middle_click`** - Middle mouse button click
- **`scroll`** - Scroll up/down by specified amount

### Keyboard Actions

- **`key`** - Press single key or key combination (e.g., `ctrl+c`, `enter`, `tab`)
- **`type`** - Type text string character by character

### Action Parameters

```json
{
  "action": "mouse_move",
  "coordinate": [x, y]
}

{
  "action": "key",
  "text": "ctrl+s"
}

{
  "action": "type",
  "text": "Hello world"
}
```

## nut.js Technical Details

nut.js is a cross-platform Node.js library for desktop automation:

- **Platforms**: Windows, macOS, Linux
- **Native bindings**: Uses N-API for native OS interaction
- **Dependencies**: Visual C++ Redistributable (Windows), Accessibility permissions (macOS)
- **Features**: Mouse/keyboard control, screen capture, image recognition, OCR

### nut.js API Used by computer-use-mcp

```javascript
// Screen capture
const { screen } = require('@nut-tree/nut-js');
const image = await screen.grab();  // Returns Image object

// Mouse control
const { mouse, Point } = require('@nut-tree/nut-js');
await mouse.move([new Point(x, y)]);
await mouse.leftClick();
await mouse.rightClick();
await mouse.drag([new Point(endX, endY)]);

// Keyboard control
const { keyboard, Key } = require('@nut-tree/nut-js');
await keyboard.type("text");
await keyboard.pressKey(Key.Enter);
await keyboard.pressKey(Key.LeftControl, Key.C);  // Ctrl+C
```

## Model Requirements

Computer Use works best with specific Claude models:

- **Recommended**: Claude Sonnet 4, Claude Opus 4
- **API header**: `anthropic-beta: computer-use-2025-01-24`
- **Tool name**: `computer_20251124` (Anthropic's official tool version)

Note: Cascade uses its own model selection. Computer use accuracy depends on which model Cascade invokes.

## Execution Cycle

1. **Screenshot** - AI requests screenshot via `screenshot` action
2. **Analysis** - Model analyzes image to identify UI elements
3. **Action** - Model decides action (click, type, etc.) with coordinates
4. **Execute** - nut.js performs the action on OS
5. **Verify** - AI takes another screenshot to verify result
6. **Repeat** - Continue until task complete or error

## Limitations

- **Coordinate accuracy** - Models frequently click wrong elements
- **Resolution sensitivity** - Higher resolutions = more errors
- **Speed** - Each action requires screenshot + analysis (slow)
- **No DOM access** - Cannot read element properties or text reliably
- **Security risk** - Full desktop control, vulnerable to prompt injection
- **Exclusive control** - User cannot use mouse/keyboard during operation

## Best Practices

1. **Use 720p resolution** - Smaller screens = better accuracy
2. **Install Rango extension** - Keyboard navigation for browsers (more reliable than clicks)
3. **Use latest Claude models** - Sonnet 4+ or Opus 4+ for best results
4. **Supervise closely** - Treat like giving a toddler computer access
5. **Sandboxed account** - Create separate user account for automation
6. **Clean desktop** - Remove visual clutter for better recognition
7. **Zoom in** - Focus on active window when possible

## Comparison with Alternatives

- **Playwriter** - Browser-only, DOM-based, user keeps control, more reliable
- **Microsoft Playwright MCP** - Browser automation via Playwright, no vision
- **Anthropic Reference Implementation** - Official Docker-based, requires VM

## Supporting Files

- `SETUP.md` - Installation and configuration instructions (with pre-verification)

## Sources

- **computer-use-mcp repository**: https://github.com/domdomegg/computer-use-mcp
- **nut.js documentation**: https://nutjs.dev/
- **nut.js GitHub**: https://github.com/nut-tree/nut.js
- **nut.js API reference**: https://nut-tree.github.io/apidoc/
- **Anthropic Computer Use docs**: https://docs.anthropic.com/en/docs/build-with-claude/computer-use
- **Anthropic Computer Use tool**: https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool
- **Rango browser extension**: https://chromewebstore.google.com/detail/rango/lnemjdnjjofijemhdogofbpcedhgcpmb
