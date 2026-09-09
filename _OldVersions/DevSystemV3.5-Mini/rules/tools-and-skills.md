---
trigger: always_on
---

# Tools and Skills

## Browser Automation (Playwright vs Playwriter)

- Playwright MCP (default) - Microsoft's MCP server. Fresh browser instance. `npx @playwright/mcp@latest`
- Playwriter (exception) - Chrome extension + CLI. Uses real browser with existing logins/cookies. From `playwriter.dev`

When to use:
- Playwright MCP: Default. Clean sessions, no existing auth needed.
- Playwriter: Only when user explicitly says "Playwriter".