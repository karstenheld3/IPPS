# INFO: Playwright Integration for AI Agents

**Doc ID**: PWRT-IN01
**Goal**: Comprehensive research on MCP servers, agent skills, and approaches for integrating Playwright browser automation with AI agents
**Timeline**: Created 2026-01-15, Updated 4 times (2026-01-15)

## Summary

- **Two primary approaches exist**: Accessibility Tree (DOM-based) vs Vision-based (screenshot recognition) [VERIFIED]
- **MCP** = Model Context Protocol, standard for connecting AI models to external tools
- **Microsoft Playwright MCP** (`@playwright/mcp`) is the official, most mature MCP server for browser automation [VERIFIED]
- **Playwriter** (remorses/playwriter) offers browser extension approach for existing browser sessions with logged-in state [VERIFIED]
- **Browser-Use** provides Python-based agent framework with MCP server support and cloud infrastructure [VERIFIED]
- **Authentication handling** via: persistent user profiles, storage state files, or browser extension connection to existing sessions [VERIFIED]
- **Claude Computer Use** is the primary vision-based approach, using screenshot analysis + mouse/keyboard control [VERIFIED]
- **OmniParser** (Microsoft) enhances vision-based approaches with Set-of-Mark UI element detection [VERIFIED]
- **Common MCP issues**: npx path not found, profile lock errors, inotify exhaustion on Linux [VERIFIED]
- **Flaky test causes**: Race conditions, unstable selectors, network unpredictability, state contamination [VERIFIED]
- **CAPTCHA workarounds**: Stealth browsers, real browser fingerprints, human-in-the-loop, profile persistence [VERIFIED]

## Table of Contents

1. [Automation Approaches](#1-automation-approaches)
2. [MCP Servers for Browser Automation](#2-mcp-servers-for-browser-automation)
3. [Agent Frameworks](#3-agent-frameworks)
4. [Authentication Strategies](#4-authentication-strategies)
5. [Vision-Based Approaches](#5-vision-based-approaches)
6. [Comparison Matrix](#6-comparison-matrix)
7. [Community Experiences, Tips, and Known Problems](#7-community-experiences-tips-and-known-problems)
8. [Sources](#8-sources)
9. [Next Steps](#9-next-steps)
10. [Document History](#10-document-history)

## 1. Automation Approaches

### 1.1 Accessibility Tree (DOM-Based)

Uses Playwright's accessibility tree to identify and interact with elements. DOM (Document Object Model) is the structured representation of a webpage. No vision model required.

**Advantages:**
- Fast and lightweight - operates on structured data
- Deterministic element selection via refs (element references, e.g., `aria-ref=e5`)
- LLM-friendly - no vision model needed
- Lower token usage compared to screenshots
- Reliable, repeatable interactions

**Disadvantages:**
- Cannot interact with canvas-based or non-standard UI
- May miss visually obvious elements not in accessibility tree
- Requires DOM access (problematic for some sites)

### 1.2 Vision-Based (Screenshot Recognition)

Uses screenshots analyzed by vision models (GPT-4V, Claude) to identify UI elements.

**Advantages:**
- Works with any visual interface (canvas, images, non-standard UI elements)
- Can handle complex visual layouts (grids, dashboards, maps)
- Platform-agnostic (works on desktop, web, mobile)

**Disadvantages:**
- Higher latency due to image processing
- More expensive (vision model tokens)
- Less deterministic - coordinates may vary
- Requires vision-capable LLM (Large Language Model)

### 1.3 Hybrid Approaches

Modern tools combine both:
- **Playwriter**: `screenshotWithAccessibilityLabels()` overlays Vimium-style labels on interactive elements
- **Stagehand**: Choose code vs natural language per action
- **Browser-Use**: DOM analysis with optional vision fallback

## 2. MCP Servers for Browser Automation

### 2.1 Microsoft Playwright MCP (Official)

**Repository**: https://github.com/microsoft/playwright-mcp
**Package**: `@playwright/mcp`
**Stars**: High activity, 57 contributors, 47 releases

**Key Features:**
- Uses Playwright's accessibility tree (no vision model needed)
- Cross-browser support: Chrome, Firefox, Safari
- Compatible with: VS Code, Cursor, Windsurf, Claude Desktop, Copilot, Codex, Goose

**Installation:**
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

**Tools Provided:**
- `browser_navigate` - Navigate to URL
- `browser_click` - Click elements (single/double, modifiers)
- `browser_type` - Type text into inputs
- `browser_screenshot` - Capture page screenshots
- `browser_snapshot` - Get accessibility tree
- `browser_evaluate` - Execute JavaScript
- `browser_drag` - Drag and drop operations
- `browser_console_messages` - Get console logs
- `browser_close` - Close browser

**Authentication Options:**
- Persistent user profile (default): `--user-data-dir`
- Isolated mode: `--isolated` with `--storage-state`
- Browser extension: Connect to existing logged-in browser

### 2.2 Playwriter (remorses)

**Repository**: https://github.com/remorses/playwriter
**Package**: `playwriter`

**Key Differentiator**: Chrome extension-based, connects to existing browser tabs.

**Advantages over Playwright MCP:**
- Uses your existing browser with logged-in sessions
- Work alongside the AI in same browser
- Reuse ad blockers, password managers, other extensions
- Bypass automation detection (can disconnect extension temporarily)
- Less resource usage - no separate Chrome instance
- Full Playwright API via single `execute` tool

**Installation:**
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

**Visual Labels Feature:**
```javascript
// Take screenshot with Vimium-style labels on interactive elements
await screenshotWithAccessibilityLabels({ page });
// Use refs to interact
await page.locator('aria-ref=e5').click();
```

### 2.3 ExecuteAutomation MCP-Playwright

**Repository**: https://github.com/executeautomation/mcp-playwright
**Package**: `@executeautomation/playwright-mcp-server`

**Features:**
- Device emulation with 143 real device presets
- Test code generation
- Web scraping capabilities
- HTTP mode for standalone server deployment

**Installation:**
```bash
npm install -g @executeautomation/playwright-mcp-server
# or via Claude Code
claude mcp add --transport stdio playwright npx @executeautomation/playwright-mcp-server
```

### 2.4 Browser MCP

**Website**: https://browsermcp.io
**Repository**: https://github.com/browsermcp/mcp

**Key Features:**
- Chrome extension + MCP server combination
- Uses existing browser profile (logged-in sessions)
- Local execution (no remote servers)
- Stealth mode using real browser fingerprint

**Tools:**
- Navigate, Go Back, Go Forward
- Click, Drag & Drop, Hover, Type Text
- Press Key, Wait
- Snapshot (accessibility), Screenshot
- Get Console Logs

### 2.5 Browser-Use MCP Server

**Documentation**: https://docs.browser-use.com/customize/mcp-server
**Repository**: https://github.com/browser-use/browser-use

**Cloud vs Self-Hosted:**

Cloud (recommended for production):
- Stealth browsers to avoid detection/CAPTCHA
- Scalable infrastructure
- Memory management, proxy rotation

Self-hosted:
- Local browser control
- Custom model support (OpenAI, Anthropic, local Ollama)

**Tools:**
- `browser_task` - Execute multi-step browser tasks
- `list_browser_profiles` - List available auth profiles
- `monitor_task` - Real-time task monitoring

### 2.6 Other Notable MCP Servers

**Puppeteer-based:**
- `@modelcontextprotocol/server-puppeteer` - Official Anthropic Puppeteer server (uses CDP - Chrome DevTools Protocol)
- `mcp-puppeteer-advanced` - Enhanced Puppeteer with stealth plugin
- `puppeteer-real-browser-mcp-server` - Detection-resistant automation

**Selenium-based:**
- `selenium-mcp-server` - Selenium WebDriver for LLM control

**Specialized:**
- `anchor-browser` - Remote-hosted controllable browser
- `airtop-mcp-server` - Airtop cloud browser integration
- `nova-act-mcp-server` - Amazon Nova Act SDK integration

## 3. Agent Frameworks

### 3.1 Browser-Use

**Repository**: https://github.com/browser-use/browser-use
**Language**: Python
**Stars**: 70k+, 283 contributors

**Architecture:**
- Agent-based with task decomposition
- DOM analysis + optional vision
- Custom tool support
- MCP server included

**Quick Start:**
```python
from browser_use import Agent, Browser, ChatBrowserUse
import asyncio

async def example():
    browser = Browser()
    llm = ChatBrowserUse()
    agent = Agent(
        task="Find the number of stars of the browser-use repo",
        llm=llm,
        browser=browser,
    )
    history = await agent.run()
    return history

asyncio.run(example())
```

**Authentication:**
- Real browser profiles: Reuse existing Chrome profile with saved logins
- Cloud profile sync: `curl -fsSL https://browser-use.com/profile.sh | BROWSER_USE_API_KEY=XXXX sh`

### 3.2 Stagehand

**Repository**: https://github.com/browserbase/stagehand
**Website**: https://www.stagehand.dev
**Languages**: TypeScript, Python

**Key Concept**: Hybrid code + natural language automation.

**Features:**
- `act()` - Single action via natural language
- `agent()` - Multi-step task execution
- `extract()` - Structured data extraction with Zod schemas (TypeScript validation library)
- Auto-caching and self-healing for production reliability

**Example:**
```typescript
const page = stagehand.context.pages()[0];
await page.goto("https://github.com/browserbase");

// Natural language action
await stagehand.act("click on the stagehand repo");

// Multi-step agent task
const agent = stagehand.agent();
await agent.execute("Get to the latest PR");

// Structured extraction
const { author, title } = await stagehand.extract(
  "extract the author and title of the PR",
  z.object({
    author: z.string(),
    title: z.string(),
  }),
);
```

### 3.3 Agent-Browser (Vercel)

**Repository**: https://github.com/vercel-labs/agent-browser
**Website**: https://agent-browser.dev

**Architecture:**
- Rust CLI for fast command parsing
- Node.js daemon for Playwright management
- Cross-platform native binaries

**Features:**
- 50+ commands for comprehensive automation
- Session management for isolated browser instances
- Ref-based element selection from accessibility snapshots

**Example:**
```bash
agent-browser open example.com
agent-browser snapshot -i
# Output: - heading "Example Domain" [ref=e1]
#         - link "More information..." [ref=e2]
agent-browser click @e2
agent-browser screenshot page.png
```

## 4. Authentication Strategies

### 4.1 Persistent User Profile

Store browser data between sessions. Default for most MCP servers.

**Playwright MCP:**
```
# Windows: %USERPROFILE%\AppData\Local\ms-playwright\mcp-{channel}-profile
# macOS: ~/Library/Caches/ms-playwright/mcp-{channel}-profile
# Linux: ~/.cache/ms-playwright/mcp-{channel}-profile
```

Override with: `--user-data-dir=/path/to/profile`

### 4.2 Storage State Files

Export/import cookies, localStorage, IndexedDB.

**Save state after login:**
```typescript
await page.context().storageState({ path: 'playwright/.auth/user.json' });
```

**Load state in new session:**
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": [
        "@playwright/mcp@latest",
        "--isolated",
        "--storage-state=path/to/storage.json"
      ]
    }
  }
}
```

### 4.3 Session Storage (Special Case)

Session storage is not persisted by default. Manual handling required:

```javascript
// Save
const sessionStorage = await page.evaluate(() => JSON.stringify(sessionStorage));
fs.writeFileSync('session.json', sessionStorage);

// Restore
const sessionStorage = JSON.parse(fs.readFileSync('session.json'));
await context.addInitScript(storage => {
  if (window.location.hostname === 'example.com') {
    for (const [key, value] of Object.entries(storage))
      window.sessionStorage.setItem(key, value);
  }
}, sessionStorage);
```

### 4.4 Browser Extension Connection

Connect to existing browser with logged-in sessions.

**Playwriter approach:**
1. Install Chrome extension
2. Click extension icon on tab to control
3. AI agent inherits all logged-in sessions

**Playwright MCP Chrome Extension:**
- `--extension` flag to connect to running browser
- Requires "Playwright MCP Bridge" extension

### 4.5 Authentication Setup Project (Playwright Test)

For test automation, authenticate once and reuse:

```typescript
// tests/auth.setup.ts
import { test as setup } from '@playwright/test';

setup('authenticate', async ({ page }) => {
  await page.goto('https://example.com/login');
  await page.fill('[name="username"]', 'user');
  await page.fill('[name="password"]', 'pass');
  await page.click('button[type="submit"]');
  await page.waitForURL('https://example.com/dashboard');
  await page.context().storageState({ path: 'playwright/.auth/user.json' });
});
```

## 5. Vision-Based Approaches

### 5.1 Claude Computer Use

**Documentation**: https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool

**Capabilities:**
- Screenshot capture
- Mouse control (click, drag, move)
- Keyboard input
- Desktop automation (any application)

**Requirements:**
- Virtual display (Xvfb)
- Desktop environment (Linux recommended)
- Docker container for isolation

**Limitations:**
- Higher latency than DOM-based approaches
- Vision accuracy may hallucinate coordinates
- Limited on social media (no account creation/impersonation)
- Scrolling and spreadsheet interaction less reliable

**Model Compatibility:**
- Claude 4 models: `computer_20251124`
- Claude Sonnet 3.7: `computer_20250124`

**Security Considerations:**
- Use dedicated VM (Virtual Machine)/container
- Avoid sensitive data access
- Limit internet to allowlist
- Human confirmation for critical actions

### 5.2 OmniParser (Microsoft)

**Repository**: https://github.com/microsoft/OmniParser
**Hugging Face**: https://huggingface.co/microsoft/OmniParser-v2.0

**Purpose**: Parse UI screenshots into structured elements for vision-based GUI (Graphical User Interface) agents.

**How it works:**
1. Fine-tuned object detection model identifies UI elements
2. Set-of-Mark (SoM) approach labels each element
3. Icon captioning model describes element functions
4. Structured output enables grounded actions

**Components:**
- `icon_detect` - YOLO (You Only Look Once)-based element detection (AGPL - Affero General Public License)
- `icon_caption_florence` - Element description model (MIT license)

**Integration with agents:**
- OmniParser + Claude Computer Use
- OmniParser + GPT-4V
- OmniParser + Qwen 2.5VL
- OmniParser + DeepSeek R1

**OmniTool**: Windows 11 VM control with OmniParser + vision model of choice.

### 5.3 Set-of-Mark (SoM) Prompting

Visual grounding technique where interactive elements are labeled directly on screenshots.

**Implementations:**
- OmniParser: Automatic UI element detection and labeling
- Playwriter: `screenshotWithAccessibilityLabels()` with Vimium-style labels
- WebVoyager: End-to-end web agent using SoM

**Benefits:**
- GPT-4V can provide precise coordinates for actions
- Reduces hallucination of element positions
- Works with complex visual layouts

## 6. Comparison Matrix

### 6.1 MCP Servers

**Microsoft Playwright MCP:**
- Approach: Accessibility Tree
- Auth: Persistent profile, storage state, extension
- Best for: General browser automation, testing
- Maturity: High (official, well-maintained)

**Playwriter:**
- Approach: Accessibility Tree + Visual Labels
- Auth: Existing browser sessions via extension
- Best for: Working with logged-in sites, collaboration
- Maturity: Medium (active development)

**Browser-Use MCP:**
- Approach: DOM + optional vision
- Auth: Cloud profiles, real browser profiles
- Best for: Production automation, stealth requirements
- Maturity: High (large community)

**Browser MCP:**
- Approach: Accessibility Tree
- Auth: Existing browser profile via extension
- Best for: Local automation with existing logins
- Maturity: Medium

### 6.2 Accessibility Tree vs Vision

**Use Accessibility Tree when:**
- Speed is critical
- Elements are in standard DOM
- Token budget is limited
- Deterministic selection needed

**Use Vision when:**
- Canvas/image-based UI
- Non-standard elements
- Spatial layout matters
- Cross-platform (desktop, mobile)

**Use Hybrid when:**
- Complex pages with mixed content
- Need visual verification
- Production reliability required

## 7. Community Experiences, Tips, and Known Problems

### 7.1 Known Problems and Limitations

**MCP Server Connection Issues:**
- **npx not found**: Cursor/Windsurf may fail to find `npx` command. Fix: Use full path to npx in config (e.g., `C:\\Users\\user\\.nvm\\versions\\node\\v20.19.0\\bin\\npx.cmd`)
- **Profile lock errors**: Browser profile SingletonLock files can cause startup failures. Reset script:
  ```bash
  pkill -f mcp-chrome-profile || true
  rm -f ~/Library/Caches/ms-playwright/mcp-chrome-profile/SingletonLock
  ```
- **Extension mode not connecting**: `--extension` flag may launch new Chrome instead of connecting to existing instance (GitHub issue #921)
- **Linux inotify exhaustion**: "no space left on device" error is NOT disk space - it's inotify watches. Fix: `echo "fs.inotify.max_user_watches = 2097152" | sudo tee /etc/sysctl.d/99-idea.conf`

**Browser-Use Reliability Issues:**
- Infinite loops on basic URL navigation reported by users
- Library described as "not production-ready" for complex workflows
- Memory consumption issues when running multiple agents in parallel
- Recommendation: Use Browser-Use Cloud API for production (handles scaling, stealth, proxies)

**Stagehand Evolution:**
- V3 removed Playwright dependency, now uses CDP (Chrome DevTools Protocol) directly
- Reason: Playwright's testing-first approach adds overhead for automation scenarios
- V3 is 44% faster than V2, especially for iframes and shadow DOMs
- Auto-caching reduces LLM inference costs for repeated actions

### 7.2 Microsoft Playwright MCP Specific Issues

**"Browser already in use" Error (GitHub #942, #1245):**
- Occurs on first attempt even with no prior browser sessions
- Common in LXC containers, WSL, and SSH remote connections
- **Workarounds:**
  - Use `--isolated` flag to run separate browser instances
  - Delete SingletonLock file before starting: `rm -f ~/.cache/ms-playwright/mcp-chrome-*/SingletonLock`
  - In containers: Use `--no-sandbox` with appropriate security measures

**Session Not Found in HTTP/Container Mode (GitHub #1140):**
- Multi-step operations fail after first request in Kubernetes/Docker
- Root cause: Session deleted immediately on transport close
- **Workaround:** Use stdio transport instead of HTTP when possible
- **Pending fix:** Delayed session cleanup (5-second delay proposed)

**Extension Mode Launches New Browser (GitHub #921):**
- `--extension` flag starts new Chrome instead of connecting to existing instance
- Prevents using authenticated sessions in existing browser
- **Workaround:** Use Playwriter instead for existing browser connection
- **Alternative:** Use `--storage-state` to export/import authentication

**Variable Success Rate in Claude Code (GitHub #1383):**
- Playwright MCP works intermittently - sometimes succeeds, sometimes fails with undefined errors
- Tools return "Error calling tool: undefined" without clear cause
- **Workarounds:**
  - Restart MCP server between sessions
  - Use `--headless` consistently or `--headed` consistently, don't mix
  - Add explicit browser installation: run `npx playwright install chromium` first

**5-Second Ping Timeout (GitHub #1293):**
- HTTP transport breaks for operations taking >5 seconds
- Affects page loads, complex form submissions, file uploads
- **Workaround:** Use stdio transport for long operations
- **Config fix:** Increase `--timeout-navigation` (default 60000ms)

**Flatpak/Sandbox Incompatibility (GitHub #1296):**
- MCP server fails expecting `node_modules/lib` in sandbox
- **Workaround:** Install globally or use Docker image instead

**Agent Opens 1000+ Tabs (GitHub #1299):**
- Agent fails on first attempt, then loops creating new tabs
- **Fix:** Add explicit `browser_close` between task attempts
- **Prevention:** Use `--snapshot-mode=none` to reduce token usage

**Timeout Configuration:**
```bash
npx @playwright/mcp@latest \
  --timeout-action 10000 \
  --timeout-navigation 120000 \
  --headless
```

### 7.3 Tips and Best Practices

**Context Engineering for AI Agents:**
- Create structured test folders with separate prompt files and data
- Include authentication steps, browser versions, environment variables
- Provide clear data sources (credentials, sample data, expected outputs)
- Be explicit: Instead of "Test the login," specify step-by-step actions

**Avoiding Flaky Tests:**
- **Race conditions**: Tests proceed before app ready - use proper waits
- **Unstable selectors**: Avoid selectors that change between renders
- **Network unpredictability**: Handle API response time variations
- **State contamination**: Isolate tests, don't share state

**Playwright Auto-Waiting Limitations:**
Auto-waiting does NOT help with:
- Elements waiting for background data to load
- Custom JavaScript UI controls without standard disabled attributes
- Page transitions where URL doesn't change
- Dynamically loaded content after page appears ready
- Virtual scrolling content

**Timeout Configuration:**
```typescript
// playwright.config.ts
export default defineConfig({
  timeout: 2 * 60 * 1000,      // Test timeout: 2 minutes
  expect: { timeout: 10000 }   // Expect timeout: 10 seconds
});
```
- Never set timeout to 0 (infinite)
- Use `test.slow()` for tests that need 3x normal timeout
- Different values for dev vs CI environments

**Wait Strategies:**
```javascript
// Wait for element states
await page.waitForSelector('#loading-spinner', { state: 'hidden' });
await page.waitForSelector('#data-loaded', { timeout: 10000 });

// Wait for page states
await page.waitForLoadState('networkidle');
await page.waitForURL('**/dashboard');
```

### 7.4 CAPTCHA and Bot Detection

**Problem**: AI browser agents trigger CAPTCHA and bot detection systems.

**Solutions:**
- **Stealth browsers**: Browser-Use Cloud, Browserbase provide detection-resistant browsers
- **Real browser fingerprints**: Playwriter and Browser MCP use your actual browser profile
- **Proxy rotation**: Required for repeated automation on same sites
- **Human-in-the-loop**: Design workflows where human can intervene for CAPTCHA
- **AWS Web Bot Auth**: Amazon Bedrock AgentCore Browser offers bot authentication (preview)

**Workarounds:**
- Disconnect Playwriter extension temporarily to bypass Google login detection
- Use persistent user profiles to maintain session cookies
- Avoid headless mode when possible - use headed browser with extension

### 7.5 Production Deployment Considerations

**Challenges reported by practitioners:**
- Keeping sessions stable for long-running/scheduled tasks
- Expired cookies and session state across multiple runs
- JavaScript-heavy pages and slow-loading components
- Random UI changes breaking selectors

**Recommendations:**
- Abstract interactions behind custom actions rather than full DOM exposure
- Use managed browser environments (Browserbase, Browser-Use Cloud, Hyperbrowser)
- Implement retry logic with exponential backoff
- Monitor browser memory consumption
- Test MCPs individually before blaming the IDE

## 8. Sources

**Primary Sources:**
- `PWRT-IN01-SC-MSGH-PWMCP`: https://github.com/microsoft/playwright-mcp - Official Playwright MCP server documentation [VERIFIED]
- `PWRT-IN01-SC-RMRS-PLWR`: https://github.com/remorses/playwriter - Playwriter browser extension MCP [VERIFIED]
- `PWRT-IN01-SC-BRUS-GH`: https://github.com/browser-use/browser-use - Browser-Use agent framework [VERIFIED]
- `PWRT-IN01-SC-BRBS-STGH`: https://github.com/browserbase/stagehand - Stagehand AI browser framework [VERIFIED]
- `PWRT-IN01-SC-PWRT-AUTH`: https://playwright.dev/docs/auth - Playwright authentication documentation [VERIFIED]
- `PWRT-IN01-SC-ANTH-CMPU`: https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool - Claude Computer Use documentation [VERIFIED]
- `PWRT-IN01-SC-MSGH-OMNI`: https://github.com/microsoft/OmniParser - OmniParser vision-based GUI agent [VERIFIED]
- `PWRT-IN01-SC-EXAU-MCPP`: https://github.com/executeautomation/mcp-playwright - ExecuteAutomation Playwright MCP [VERIFIED]
- `PWRT-IN01-SC-BRMCP-IO`: https://browsermcp.io - Browser MCP extension and server [VERIFIED]
- `PWRT-IN01-SC-VRCEL-AGBR`: https://agent-browser.dev - Vercel Agent-Browser CLI [VERIFIED]
- `PWRT-IN01-SC-MCPSO-BRAU`: https://mcp.so/servers?category=browser-automation - MCP server directory [VERIFIED]
- `PWRT-IN01-SC-BRUS-MCP`: https://docs.browser-use.com/customize/mcp-server - Browser-Use MCP documentation [VERIFIED]

**Community Sources:**
- `PWRT-IN01-SC-CRSR-MCPBG`: https://forum.cursor.com/t/playwright-mcp-does-not-work/103933 - Cursor forum: MCP troubleshooting, npx path issues [VERIFIED]
- `PWRT-IN01-SC-RDAI-BRWS`: https://www.reddit.com/r/AI_Agents/comments/1pb6l6w/ - Reddit: Real-world browser agent challenges [VERIFIED]
- `PWRT-IN01-SC-RDWF-MCPS`: https://www.reddit.com/r/windsurf/comments/1oq6z10/ - Reddit: Windsurf MCP inotify fix [VERIFIED]
- `PWRT-IN01-SC-MSGH-ISS921`: https://github.com/microsoft/playwright-mcp/issues/921 - GitHub: Extension mode connection issue [VERIFIED]
- `PWRT-IN01-SC-MSGH-ISS942`: https://github.com/microsoft/playwright-mcp/issues/942 - GitHub: Browser already in use error [VERIFIED]
- `PWRT-IN01-SC-MSGH-ISS1140`: https://github.com/microsoft/playwright-mcp/issues/1140 - GitHub: Session management in containers [VERIFIED]
- `PWRT-IN01-SC-MSGH-ISS1293`: https://github.com/microsoft/playwright-mcp/issues/1293 - GitHub: 5-second ping timeout issue [VERIFIED]
- `PWRT-IN01-SC-MSGH-ISS1299`: https://github.com/microsoft/playwright-mcp/issues/1299 - GitHub: Agent opens 1000 tabs [VERIFIED]
- `PWRT-IN01-SC-ANTH-ISS1383`: https://github.com/anthropics/claude-code/issues/1383 - GitHub: Playwright MCP variable success rate [VERIFIED]
- `PWRT-IN01-SC-BRBS-V3BL`: https://www.browserbase.com/blog/stagehand-v3 - Stagehand V3 announcement, Playwright graduation [VERIFIED]
- `PWRT-IN01-SC-BTST-FLKY`: https://betterstack.com/community/guides/testing/avoid-flaky-playwright-tests/ - Flaky test prevention guide [VERIFIED]
- `PWRT-IN01-SC-SPTST-TIPS`: https://supatest.ai/blog/playwright-mcp-setup-guide - Playwright MCP best practices [VERIFIED]

## 9. Next Steps

1. **For immediate integration**: Start with Microsoft Playwright MCP for well-supported, accessibility tree-based automation
2. **For logged-in sites**: Use Playwriter with browser extension to leverage existing sessions
3. **For production**: Consider Browser-Use cloud for stealth and scalability
4. **For complex visual UIs**: Combine accessibility snapshot with `screenshotWithAccessibilityLabels` for hybrid approach
5. **For desktop automation**: Evaluate Claude Computer Use with OmniParser for vision-based control

## 10. Document History

**[2026-01-15 11:05]**
- Added: Section 7.2 - Microsoft Playwright MCP Specific Issues
- Added: "Browser already in use" error workarounds (GitHub #942, #1245)
- Added: Session not found in HTTP/container mode (GitHub #1140)
- Added: Extension mode connection issues (GitHub #921)
- Added: Variable success rate in Claude Code (GitHub #1383)
- Added: 5-second ping timeout issue (GitHub #1293)
- Added: Agent opens 1000+ tabs issue (GitHub #1299)
- Added: Flatpak/sandbox incompatibility workarounds
- Added: Timeout configuration example
- Added: 6 new GitHub issue sources

**[2026-01-15 10:37]**
- Added: Section 7 - Community Experiences, Tips, and Known Problems
- Added: Known MCP server connection issues and fixes
- Added: Browser-Use reliability concerns from community
- Added: Stagehand V3 evolution (removed Playwright dependency)
- Added: Tips for avoiding flaky tests
- Added: CAPTCHA and bot detection workarounds
- Added: Production deployment considerations
- Added: 7 community sources (forums, Reddit, GitHub issues)

**[2026-01-15 10:36]**
- Fixed: Acronyms expanded on first use (MCP, DOM, LLM, CDP, refs)
- Fixed: "HuggingFace" corrected to "Hugging Face"
- Added: Zod explanation in Stagehand section

**[2026-01-15 10:31]**
- Initial research document created
- Added: MCP servers comparison (Microsoft Playwright MCP, Playwriter, Browser-Use, Browser MCP, ExecuteAutomation)
- Added: Agent frameworks section (Browser-Use, Stagehand, Agent-Browser)
- Added: Authentication strategies (persistent profile, storage state, session storage, extension)
- Added: Vision-based approaches (Claude Computer Use, OmniParser, Set-of-Mark)
- Added: Comparison matrix for approach selection
