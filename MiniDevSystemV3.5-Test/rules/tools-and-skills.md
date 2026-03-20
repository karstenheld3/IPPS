---
trigger: always_on
---

# Tools and Skills

## Browser Automation (Playwright vs Playwriter)

Different tools with similar names:

- **Playwright MCP** (default) - Microsoft's MCP server. Fresh browser instance. `npx @playwright/mcp@latest`
- **Playwriter** (exception) - Chrome extension + CLI. Uses your **real browser** with existing logins/cookies. Install from `playwriter.dev`

**When to use:**
- **Playwright MCP**: Default. Clean sessions, standard automation, no existing auth needed
- **Playwriter**: Only when user explicitly asks for `Playwriter`