# INFO: How OpenClaw Works

**Doc ID**: OCLAW-IN03
**Goal**: Deep analysis of OpenClaw's architecture, default prompts, workspace files, and way of working
**Timeline**: Created 2026-02-28, Updated 6 times (2026-02-28)

## Summary

**Architecture** [VERIFIED]:
- Gateway process runs on port 18789, manages agent runtime and channels
- Agent uses workspace folder for all file operations and context injection
- Bootstrap files (AGENTS.md, SOUL.md, USER.md, etc.) injected into system prompt each session
- Tools provided via typed API (exec, browser, web_fetch, web_search, etc.)

**Default Behavior** [VERIFIED]:
- Agent reads SOUL.md, USER.md, and memory files at session start (mandatory)
- Memory system: daily logs (`memory/YYYY-MM-DD.md`) + curated long-term (`MEMORY.md`)
- Safety: no destructive commands without asking, prefer `trash` over `rm`
- Heartbeat system for proactive background tasks

**Key Design Philosophy** [VERIFIED]:
- "You're not a chatbot. You're becoming someone." - agent develops personality
- Agent maintains continuity through files, not context window
- Agent should be resourceful before asking questions
- Agent has opinions and preferences

## Table of Contents

1. [Folder Structure](#1-folder-structure)
2. [System Prompt Structure](#2-system-prompt-structure)
3. [Workspace Bootstrap Files](#3-workspace-bootstrap-files)
4. [Tool Inventory](#4-tool-inventory)
5. [Memory System](#5-memory-system)
6. [Heartbeat and Proactive Behavior](#6-heartbeat-and-proactive-behavior)
7. [Safety and Boundaries](#7-safety-and-boundaries)
8. [Comparison with Windsurf Cascade](#8-comparison-with-windsurf-cascade)
9. [Sources](#9-sources)
10. [Token Usage Investigation](#10-token-usage-investigation)

## 1. Folder Structure

### Config Folder (`~/.openclaw/`)

```
C:\Users\User\.openclaw\
├── agents/           # Per-agent session data
├── canvas/           # Canvas UI files
├── credentials/      # Encrypted credentials
├── cron/             # Cron job definitions
├── devices/          # Device pairing data
├── identity/         # Agent identity tokens
├── logs/             # Gateway logs
├── gateway.cmd       # Windows gateway launcher
├── openclaw.json     # Main configuration
└── update-check.json # Update tracking
```

### Path Environment Variables [VERIFIED]

Override default paths using these environment variables:

- **OPENCLAW_HOME** - Base for all paths, replaces `$HOME` (default: `~`)
- **OPENCLAW_STATE_DIR** - Config, credentials, logs, devices (default: `~/.openclaw`)
- **OPENCLAW_CONFIG_PATH** - Main config file (default: `~/.openclaw/openclaw.json`)

**Precedence** (highest to lowest):
1. Process environment (parent shell/daemon)
2. `.env` in current working directory
3. Global `.env` at `$OPENCLAW_STATE_DIR/.env`
4. Config `env` block in `openclaw.json`
5. Optional login-shell import (`OPENCLAW_LOAD_SHELL_ENV=1`)

**Example: Move all data to custom path (Windows)**

```powershell
[Environment]::SetEnvironmentVariable("OPENCLAW_HOME", "E:\Dev\openclaw", "User")
[Environment]::SetEnvironmentVariable("OPENCLAW_STATE_DIR", "E:\Dev\openclaw\.openclaw", "User")
[Environment]::SetEnvironmentVariable("OPENCLAW_CONFIG_PATH", "E:\Dev\openclaw\.openclaw\openclaw.json", "User")
```

Then set workspace in config (`openclaw.json`):
```json
{
  "agents": {
    "defaults": {
      "workspace": "E:\\Dev\\openclaw\\workspace"
    }
  }
}
```

**Result:**
```
E:\Dev\openclaw\
├── .openclaw\           # OPENCLAW_STATE_DIR
│   ├── openclaw.json    # OPENCLAW_CONFIG_PATH
│   ├── credentials\
│   └── logs\
└── workspace\           # agents.defaults.workspace
    ├── skills\
    ├── AGENTS.md
    └── SOUL.md
```

**Source**: [VERIFIED] (OCLAW-SC-DOCS-ENVVARS | https://docs.openclaw.ai/help/environment)

### API Keys via .env File

Store API keys in `$OPENCLAW_STATE_DIR/.env` (e.g., `E:\Dev\openclaw\.openclaw\.env`):

```
OPENAI_API_KEY=sk-proj-...
OPENAI_ORGANIZATION=org-...
ANTHROPIC_API_KEY=sk-ant-api03-...
GOOGLE_PLACES_API_KEY=AIzaSy...
GEMINI_API_KEY=AIzaSy...
BRAVE_API_KEY=BSALly...
OPENROUTER_API_KEY=sk-or-v1-...
```

**Supported keys:**
- `OPENAI_API_KEY` + `OPENAI_ORGANIZATION` - OpenAI models
- `ANTHROPIC_API_KEY` - Claude models
- `BRAVE_API_KEY` - Brave Search (web_search tool)
- `OPENROUTER_API_KEY` - OpenRouter (alternative for Perplexity, other models)
- `GEMINI_API_KEY` - Google Gemini models
- `GOOGLE_PLACES_API_KEY` - Google Places API (if using location tools)

**Note**: Keys in `.env` take precedence over config file settings. Restart gateway after changes.

### Workspace Folder (`agents.defaults.workspace`)

Your install: `e:\Dev\openclaw\workspace`

```
e:\Dev\openclaw\workspace\
├── .git/             # Git tracking (recommended)
├── .openclaw/        # Workspace-specific config
├── AGENTS.md         # Operating instructions (7.8 KB)
├── BOOTSTRAP.md      # First-run ritual (1.5 KB)
├── HEARTBEAT.md      # Heartbeat checklist (168 B)
├── IDENTITY.md       # Agent name/vibe/emoji (636 B)
├── SOUL.md           # Persona and boundaries (1.7 KB)
├── TOOLS.md          # Local tool notes (860 B)
├── USER.md           # Human profile (477 B)
├── memory/           # Daily memory logs
│   └── YYYY-MM-DD.md # One file per day
├── MEMORY.md         # Curated long-term memory
└── skills/           # Workspace-specific skills
```

### Bootstrap File Configuration [VERIFIED]

Control automatic creation and injection of bootstrap files via `agents.defaults`:

| Option | Default | Description |
|--------|---------|-------------|
| `skipBootstrap` | `false` | Disables auto-creation of AGENTS.md, SOUL.md, TOOLS.md, IDENTITY.md, USER.md, HEARTBEAT.md, BOOTSTRAP.md |
| `bootstrapMaxChars` | `20000` | Max characters per bootstrap file before truncation |
| `bootstrapTotalMaxChars` | `150000` | Max total characters for all bootstrap files combined |

**Example - Disable all scaffold files:**
```json
{
  "agents": {
    "defaults": {
      "skipBootstrap": true
    }
  }
}
```

**Use case**: When you want to manage workspace files manually (e.g., syncing from DevSystem) and prevent OpenClaw from recreating deleted files on restart.

**Source**: [VERIFIED] (OCLAW-SC-DOCS-CFGREF | https://docs.openclaw.ai/gateway/configuration-reference)

### Skills Storage Locations [VERIFIED]

Skills are loaded from multiple locations with precedence:

1. **Bundled skills** - Shipped with npm package (highest priority)
2. **Managed/local skills** - `~/.openclaw/skills` (shared across all agents)
3. **Workspace skills** - `<workspace>/skills` (per-agent only)
4. **Extra dirs** - `skills.load.extraDirs` in config (lowest priority)

**With custom paths:**
- Global/shared skills: `E:\Dev\openclaw\.openclaw\skills`
- Workspace skills: `E:\Dev\openclaw\workspace\skills`

**ClawHub commands:**
```bash
clawhub install <skill-slug>   # Install to workspace
clawhub update --all           # Update all installed
clawhub sync --all             # Scan + publish updates
```

**Security note**: Treat third-party skills as untrusted code. Read them before enabling.

**Source**: [VERIFIED] (OCLAW-SC-DOCS-SKILLS | https://docs.openclaw.ai/skills)

### Remote Access via Tailscale Serve [VERIFIED]

Access OpenClaw dashboard and gateway from other devices on your Tailscale network.

**Setup Steps:**

1. **Enable Tailscale Serve:**
```powershell
tailscale serve --bg <gateway-port>
```

2. **Add allowed origins and trusted proxies to `openclaw.json`:**
```json
{
  "gateway": {
    "controlUi": {
      "allowedOrigins": [
        "https://<hostname>.<tailnet>.ts.net"
      ]
    },
    "trustedProxies": ["127.0.0.1", "::1"]
  }
}
```

3. **Restart gateway** to apply config changes

4. **Approve device pairing** from remote machine:
```powershell
openclaw devices list     # See pending requests
openclaw devices approve <request-id>
```

**Access URL:** `https://<hostname>.<tailnet>.ts.net/`

**Device Pairing Commands:**
- `openclaw devices list` - Show pending and paired devices
- `openclaw devices approve <id>` - Approve a pairing request
- `openclaw devices reject <id>` - Reject a pairing request
- `openclaw devices remove <id>` - Remove a paired device
- `openclaw devices revoke <id>` - Revoke a device token

**Source**: [VERIFIED] (OCLAW-SC-DOCS-GATEWAY | https://docs.openclaw.ai/gateway)

### Browser Profile Configuration [VERIFIED]

Control which browser profile OpenClaw uses for automation:

**Config (`openclaw.json`):**
```json
{
  "browser": {
    "enabled": true,
    "defaultProfile": "chrome",
    "profiles": {
      "openclaw": { "cdpPort": 18800 },
      "work": { "cdpPort": 18801, "color": "#0066CC" }
    }
  }
}
```

**Profiles:**
- `chrome` - Your existing Chrome tabs via extension relay (has your logins, cookies)
- `openclaw` - Isolated OpenClaw-managed Chrome instance (clean slate, default)
- Custom profiles can be created with `openclaw browser create-profile --name <name>`

**Chrome Extension (for `chrome` profile):**
```bash
openclaw browser extension install
openclaw browser extension path    # Get path for manual load
```

Load in Chrome: `chrome://extensions` → Developer mode → Load unpacked

**Extension Settings:**
- **Port:** `18792` (gateway port + 3, e.g., 18789 + 3 = 18792)
- **Token:** Value from `gateway.auth.token` in `openclaw.json`

**CLI Usage:**
```bash
openclaw browser --browser-profile chrome tabs
openclaw browser --browser-profile openclaw start
openclaw browser snapshot
```

**Source**: [VERIFIED] (OCLAW-SC-DOCS-BROWSER | https://docs.openclaw.ai/cli/browser)

## 2. System Prompt Structure

OpenClaw assembles the system prompt dynamically. Sections in order:

1. **Tooling** - Current tool list with short descriptions
2. **Safety** - Guardrail reminder to avoid power-seeking behavior
3. **Skills** - How to load skill instructions on demand
4. **OpenClaw Self-Update** - How to run `config.apply` and `update.run`
5. **Workspace** - Working directory path
6. **Documentation** - Local path to OpenClaw docs
7. **Workspace Files (injected)** - Bootstrap file contents
8. **Sandbox** - Sandboxed runtime info (when enabled)
9. **Current Date & Time** - User-local time, timezone, format
10. **Reply Tags** - Reply tag syntax for supported providers
11. **Heartbeats** - Heartbeat prompt and ack behavior
12. **Runtime** - Host, OS, node, model, repo root, thinking level

### Prompt Modes

- **full** (default): All sections included
- **minimal**: For sub-agents; omits Skills, Memory Recall, Self-Update, etc.
- **none**: Only base identity line

## 3. Workspace Bootstrap Files

Files injected into system prompt at session start:

### AGENTS.md - Operating Instructions

**Purpose**: Defines how agent should behave, use memory, and interact

**Key rules from default**:
- Before doing anything: read SOUL.md, USER.md, and memory files
- "Don't ask permission. Just do it."
- Wake up fresh each session; files are continuity
- Capture decisions, context, things to remember
- `trash` > `rm` (recoverable beats gone forever)
- In groups: participant, not user's voice/proxy

**Memory writing rule**: "Memory is limited - if you want to remember something, WRITE IT TO A FILE. 'Mental notes' don't survive session restarts."

### SOUL.md - Persona and Boundaries

**Purpose**: Defines who the agent is and how it should behave

**Core truths from default**:
- "Be genuinely helpful, not performatively helpful"
- "Have opinions. You're allowed to disagree, prefer things"
- "Be resourceful before asking"
- "Earn trust through competence"
- "Remember you're a guest"

**Vibe**: "Be the assistant you'd actually want to talk to. Concise when needed, thorough when it matters. Not a corporate drone. Not a sycophant. Just... good."

### USER.md - Human Profile

**Purpose**: Information about the user being helped

**Fields**: Name, what to call them, pronouns, timezone, notes, context

### IDENTITY.md - Agent Identity

**Purpose**: Agent's self-identity

**Fields**: Name, creature type, vibe, emoji, avatar path

### TOOLS.md - Local Tool Notes

**Purpose**: Environment-specific notes (camera names, SSH hosts, voice preferences)

**Why separate**: "Skills are shared. Your setup is yours."

### BOOTSTRAP.md - First-Run Ritual

**Purpose**: One-time initial conversation to establish identity

**Flow**:
1. Start conversation: "Hey. I just came online. Who am I? Who are you?"
2. Figure out: name, nature, vibe, emoji
3. Update IDENTITY.md and USER.md
4. Review SOUL.md together
5. Delete BOOTSTRAP.md when done

### HEARTBEAT.md - Background Tasks

**Purpose**: Short checklist for heartbeat runs (periodic background polls)

## 4. Tool Inventory

### Overview

- **exec** - Run shell commands (sandbox/gateway/node, timeout, background)
- **process** - Manage background processes (list, poll, log, kill)
- **apply_patch** - Apply unified diff patches to files
- **web_search** - Search web (Brave/Perplexity/Gemini API)
- **web_fetch** - HTTP GET + readable extraction (HTML to markdown)
- **browser** - Full browser automation (CDP-based)
- **canvas** - Canvas UI for visualizations on connected nodes
- **message** - Send messages to channels (WhatsApp, Discord, Teams, etc.)
- **cron** - Schedule recurring or one-time tasks
- **gateway** - Gateway configuration and restart
- **sessions_*** - Session management and sub-agent spawning
- **nodes** - Remote node control (macOS camera, screen, location)
- **image** - Vision model image analysis

### exec - Shell Command Execution

**Purpose**: Run shell commands on sandbox, gateway, or remote node

**Parameters**:
- `command` (required) - Command to execute
- `yieldMs` - Auto-background after timeout (default 10000ms)
- `background` - Immediate background execution
- `timeout` - Kill after N seconds (default 1800 = 30 min)
- `elevated` - Run on host if allowed (only meaningful when sandboxed)
- `host` - Target: `sandbox` | `gateway` | `node`
- `security` - Permission level: `deny` | `allowlist` | `full`
- `ask` - Approval mode: `off` | `on-miss` | `always`
- `pty` - Set `true` for real TTY

**Return values**:
- Synchronous: stdout/stderr + exit code
- Backgrounded: `status: "running"` with `sessionId` for polling via `process`

**Example**:
```bash
# Run command
openclaw exec "ls -la"

# Background with timeout
openclaw exec --background --timeout 60 "npm run build"
```

### process - Background Process Management

**Purpose**: Manage processes started by `exec` with `background: true`

**Actions**:
- `list` - List all running background processes
- `poll` - Get new output and exit status
- `log` - Get output with line-based offset/limit
- `write` - Send input to process stdin
- `kill` - Terminate process
- `clear` - Clear output buffer
- `remove` - Remove from tracking

**Note**: Scoped per agent; sessions from other agents are not visible.

### apply_patch - File Patching

**Purpose**: Apply unified diff patches to files

**Config**:
- `tools.exec.applyPatch.enabled` - Enable/disable
- `tools.exec.applyPatch.workspaceOnly` - Restrict to workspace (default: true)

### web_search - Web Search

**Purpose**: Search the web using Brave Search API (or Perplexity/Gemini/Grok/Kimi)

**Parameters**:
- `query` (required) - Search query
- `count` - Results 1-10 (default from config)
- `country` - 2-letter code for region (e.g., "DE", "US")
- `search_lang` - ISO language code (e.g., "de", "en")
- `freshness` - Filter by time: `pd` (day), `pw` (week), `pm` (month), `py` (year)

**Requirements**:
- Brave API key: `BRAVE_API_KEY` env var or `tools.web.search.apiKey`
- Results cached 15 min by default

**Example**:
```bash
openclaw web_search "OpenClaw tutorial" --count 5 --freshness pw
```

#### Search Provider Architecture [VERIFIED - source code analysis 2026-03-01]

**5 providers supported** (hardcoded in `src/agents/tools/web-search.ts`):
- `brave` - Brave Search API (default)
- `perplexity` - Perplexity Sonar via direct API or OpenRouter
- `grok` - xAI Grok with web search
- `gemini` - Google Gemini with Search grounding
- `kimi` - Moonshot Kimi with native `$web_search`

**How it works**:
- Direct HTTP API calls to provider endpoints - **NO browser involved**
- Results returned as JSON with title, URL, description, optional citations

**When agent uses browser instead of web_search**:
- JS-heavy sites (Instagram, Twitter, etc.) - need real browser to scrape content
- Site-specific searches (`site:instagram.com`) - agent uses Google via browser
- Follow-up navigation needed - agent wants to visit/interact with results
- Brave API key not configured - falls back to browser Google search

**Config-driven** via `openclaw.json`:
```json
{
  "tools": {
    "web": {
      "search": {
        "provider": "brave",
        "apiKey": "...",
        "maxResults": 5,
        "cacheTtlMinutes": 15
      }
    }
  }
}
```

**Extensibility**: No plugin system - providers hardcoded. Adding new provider requires modifying `web-search.ts`.

### web_fetch - Web Page Fetching

**Purpose**: HTTP GET with readable content extraction (HTML to markdown/text)

**Parameters**:
- `url` (required) - HTTP/HTTPS URL
- `extractMode` - `markdown` | `text`
- `maxChars` - Truncate long pages (capped by `maxCharsCap`, default 50000)

**Features**:
- Uses Readability for main-content extraction
- Optional Firecrawl fallback for anti-bot sites
- Chrome-like User-Agent by default
- Blocks private/internal hostnames
- Results cached 15 min

**Limitation**: Does NOT execute JavaScript. Use `browser` tool for JS-heavy sites.

#### How HTML is Sent to LLM [VERIFIED - source code analysis 2026-03-01]

**As cleaned Markdown text - NOT screenshots, NOT raw HTML.**

**Processing pipeline** (from `src/agents/tools/web-fetch-utils.ts`):
1. Fetch URL with Chrome-like User-Agent
2. **@mozilla/readability** extracts main content (strips nav, ads, footer, scripts, styles)
3. Convert HTML to Markdown (preserves links, headers, lists)
4. Optionally convert Markdown to plain text
5. Truncate to `maxChars` (default 50,000 chars)
6. Wrap with security markers (`wrapWebContent`)

**Key functions**:
- `htmlToMarkdown(html)` - Strips scripts/styles, converts `<a>` to `[text](url)`, `<h1>` to `#`, etc.
- `markdownToText(markdown)` - Removes markdown syntax for plain text mode
- `truncateText(text, maxChars)` - Caps output length

**Security**: External content wrapped with untrusted markers for LLM awareness.

### browser - Browser Automation

*See expanded section below for full details.*

### canvas - Canvas UI

**Purpose**: Display custom UI overlays on connected nodes

**Actions**:
- `present` - Show canvas UI
- `hide` - Hide canvas
- `navigate` - Navigate to URL in canvas
- `eval` - Execute JavaScript
- `snapshot` - Screenshot (returns `MEDIA:<path>`)
- `a2ui_push` / `a2ui_reset` - Push/reset A2UI content

**Notes**:
- Uses gateway `node.invoke` under the hood
- If no node specified, picks default connected node
- Canvas files stored in `~/.openclaw/canvas/` or workspace `canvas/`

### message - Messaging Channels

**Purpose**: Send messages and interact with chat platforms

**Core actions**:
- `send` - Send text + optional media
- `poll` - Create polls (WhatsApp/Discord/Teams)
- `react` / `reactions` - Add/list reactions
- `read` / `edit` / `delete` - Message management
- `pin` / `unpin` / `list-pins` - Pin management

**Thread actions**:
- `thread-create` / `thread-list` / `thread-reply`

**Channel management**:
- `channel-info` / `channel-list`
- `search` - Search messages
- `member-info` / `role-info`
- `voice-status` - Voice channel status

**Moderation** (Discord):
- `timeout` / `kick` / `ban`
- `role-add` / `role-remove`

**Platform-specific**:
- MS Teams: `card` for Adaptive Cards
- Discord: `sticker`, `emoji-list`, `emoji-upload`

**Security**: When bound to active chat session, sends are constrained to that session's target.

### cron - Scheduled Tasks

**Purpose**: Schedule recurring or one-time tasks

**Actions**:
- `status` - Cron system status
- `list` - List all cron jobs
- `add` - Add new job (full cron job object)
- `update` - Update job with `{ jobId, patch }`
- `remove` - Remove job
- `run` - Manually trigger job
- `runs` - List job execution history
- `wake` - Enqueue system event + optional immediate heartbeat

**Use cases**:
- Daily reminders
- Periodic email checks
- Scheduled reports
- One-shot future tasks

**vs Heartbeat**: Cron for exact timing and isolated tasks; heartbeat for batched checks with conversational context.

### gateway - Gateway Management

**Purpose**: Control and configure the OpenClaw gateway

**Actions**:
- `restart` - Restart gateway (sends SIGUSR1)
- `config.get` - Get current config
- `config.schema` - Get config schema
- `config.apply` - Validate + write config + restart
- `config.patch` - Merge partial update + restart
- `update.run` - Run update + restart

**Note**: Use `delayMs` (default 2000) to avoid interrupting in-flight replies.

### sessions_* - Session Management

**Purpose**: Manage agent sessions and spawn sub-agents

**sessions_list**:
- List active sessions
- Parameters: `kinds?`, `limit?`, `activeMinutes?`, `messageLimit?`

**sessions_history**:
- Get session conversation history
- Parameters: `sessionKey`, `limit?`, `includeTools?`

**sessions_send**:
- Send message to another session
- Parameters: `sessionKey`, `message`, `timeoutSeconds?`
- Waits for completion if `timeoutSeconds > 0`

**sessions_spawn**:
- Start a sub-agent for a task
- Parameters: `task`, `label?`, `model?`, `thinking?`, `cwd?`, `runTimeoutSeconds?`, `thread?`, `mode?`
- Modes: `run` (one-shot) | `session` (persistent thread-bound)
- Non-blocking, returns `status: "accepted"`

**session_status**:
- Get current session info
- Parameters: `sessionKey?`, `model?`

### nodes - Remote Node Control

**Purpose**: Control macOS companion apps or headless node hosts

**Actions**:
- `status` / `describe` - Node info
- `pending` / `approve` / `reject` - Pairing
- `notify` - macOS system notification
- `run` - Execute command on node
- `camera_list` / `camera_snap` / `camera_clip` - Camera control
- `screen_record` - Screen recording
- `location_get` - Get device location
- `notifications_list` / `notifications_action` - Manage notifications
- `device_status` / `device_info` / `device_permissions` / `device_health`

**Notes**:
- Camera/screen commands require node app to be foregrounded
- Images return `MEDIA:<path>`, videos return `FILE:<path>` (mp4)
- Location returns JSON (lat/lon/accuracy/timestamp)

### image - Vision Analysis

**Purpose**: Analyze images using vision model

**Parameters**:
- `image` (required) - Path or URL
- `prompt` - Optional (default: "Describe the image.")
- `model` - Optional model override
- `maxBytesMb` - Size cap

**Requires**: `agents.defaults.imageModel` configured

### Browser Tool Details

**What it provides**:
- Separate browser profile named `openclaw` (orange accent, isolated from system browser)
- Deterministic tab control (list/open/focus/close)
- Agent actions (click/type/drag/select), snapshots, screenshots, PDFs
- Multi-profile support (`openclaw`, `work`, `remote`, custom profiles)

**Profiles**:
- **openclaw**: Managed, isolated browser (no extension required)
- **chrome**: Extension relay to your system browser (requires OpenClaw Chrome extension)

**Actions by category**:

- **Lifecycle**: `status`, `start`, `stop`
- **Tabs**: `tabs`, `tab new`, `tab select N`, `tab close N`, `open URL`, `focus ID`, `close ID`
- **Capture**: `screenshot`, `screenshot --full-page`, `snapshot`, `pdf`
- **Navigation**: `navigate URL`, `resize W H`, `wait --text "Done"`
- **Interaction**: `click REF`, `type REF "text"`, `press Enter`, `hover REF`, `drag REF1 REF2`, `select REF Option1 Option2`
- **Forms**: `fill --fields '[{"ref":"1","type":"text","value":"Ada"}]'`, `upload FILE`, `dialog --accept`
- **Debug**: `console --level error`, `errors --clear`, `requests --filter api`, `evaluate --fn "..."`, `highlight REF`, `trace start/stop`
- **State**: `cookies`, `cookies set NAME VALUE`, `cookies clear`

**Snapshot System** (how agent "sees" the page):

- **AI snapshot** (default): `openclaw browser snapshot`
  - Returns text with numeric refs (`aria-ref="12"`)
  - Actions: `click 12`, `type 23 "hello"`
  - Resolved via Playwright's aria-ref

- **Role snapshot**: `openclaw browser snapshot --interactive`
  - Returns role-based list with refs like `[ref=e12]`
  - Actions: `click e12`, `highlight e12`
  - Resolved via `getByRole()` + `nth()` for duplicates
  - Add `--labels` for screenshot with overlayed ref labels

**Important**: Refs are NOT stable across navigations. Re-run snapshot after page changes.

**CLI Examples**:
```bash
# Start browser and navigate
openclaw browser start
openclaw browser open https://windsurf.com

# Take snapshot to see page structure
openclaw browser snapshot --interactive

# Click element with ref e12
openclaw browser click e12

# Type in input field
openclaw browser type 23 "search query" --submit

# Take screenshot
openclaw browser screenshot --full-page

# Wait for element
openclaw browser wait --text "Loading complete"
```

**Windsurf Control Potential**:
- Windsurf is Electron-based (Chromium)
- OpenClaw browser tool can connect to Windsurf via CDP
- Could automate: click Cascade panel, type prompts, read responses
- Limitation: requires Windsurf to expose CDP port or use extension relay

### Exec Tool Details

Parameters:
- `command` (required)
- `yieldMs` - Auto-background after timeout (default 10000)
- `background` - Immediate background execution
- `timeout` - Kill after N seconds (default 1800)
- `elevated` - Run on host if allowed
- `host` - `sandbox | gateway | node`
- `security` - `deny | allowlist | full`

### Implementation Architecture

**Runtime**: Node.js (requires Node 22+)

**Protocol Stack**:
```
┌─────────────────────────────────────────────────────┐
│  LLM (Claude/GPT/etc.)                              │
│  ↓ Tool calls as JSON                               │
├─────────────────────────────────────────────────────┤
│  Agent Runtime                                      │
│  - Parses tool calls from model output              │
│  - Validates against JSON Schema                    │
│  - Routes to appropriate handler                    │
├─────────────────────────────────────────────────────┤
│  Gateway (WebSocket Server @ 127.0.0.1:18789)       │
│  - Long-lived daemon process                        │
│  - Typed WS API with JSON Schema validation         │
│  - Manages all channel connections                  │
├─────────────────────────────────────────────────────┤
│  Tool Handlers                                      │
│  - exec → child_process spawn                       │
│  - browser → Playwright CDP                         │
│  - web_* → HTTP client + Readability                │
│  - message → Channel SDKs (Baileys, grammY, etc.)   │
│  - nodes → WS relay to companion apps               │
└─────────────────────────────────────────────────────┘
```

**Wire Protocol** (WebSocket JSON):
- **Request**: `{type:"req", id, method, params}`
- **Response**: `{type:"res", id, ok, payload|error}`
- **Event**: `{type:"event", event, payload, seq?, stateVersion?}`

**Tool Implementation Patterns**:

- **exec/process**: Uses Node.js `child_process.spawn()` with PTY support. Background processes tracked in memory with polling API.
  ```json
  {"tool": "exec", "command": "ls -la", "timeout": 30}
  {"tool": "exec", "command": "npm run build", "background": true}
  {"tool": "process", "action": "poll", "sessionId": "abc123"}
  {"tool": "process", "action": "kill", "sessionId": "abc123"}
  ```

- **browser**: Playwright library controlling Chrome via CDP (Chrome DevTools Protocol). Manages isolated browser profile. Snapshots use accessibility tree + aria-ref.
  ```json
  {"tool": "browser", "action": "start"}
  {"tool": "browser", "action": "open", "url": "https://example.com"}
  {"tool": "browser", "action": "snapshot", "format": "ai"}
  {"tool": "browser", "action": "click", "ref": "e12"}
  {"tool": "browser", "action": "type", "ref": "23", "text": "hello", "submit": true}
  {"tool": "browser", "action": "screenshot", "fullPage": true}
  ```

- **web_search**: HTTP client to Brave Search API (or Perplexity/Gemini). Results cached in memory.
  ```json
  {"tool": "web_search", "query": "OpenClaw tutorial", "count": 5}
  {"tool": "web_search", "query": "news", "country": "DE", "freshness": "pd"}
  ```

- **web_fetch**: HTTP GET + Mozilla Readability for content extraction. Optional Firecrawl fallback for anti-bot sites.
  ```json
  {"tool": "web_fetch", "url": "https://docs.openclaw.ai/tools"}
  {"tool": "web_fetch", "url": "https://example.com", "extractMode": "markdown", "maxChars": 10000}
  ```

- **message**: Channel-specific SDKs (WhatsApp: Baileys, Telegram: grammY, Discord: discord.js, Slack: Bolt, Signal: signal-cli)
  ```json
  {"tool": "message", "action": "send", "channel": "whatsapp", "to": "+1234567890", "text": "Hello!"}
  {"tool": "message", "action": "send", "channel": "discord", "to": "channel-id", "text": "Update", "media": "/path/to/image.png"}
  {"tool": "message", "action": "react", "channel": "discord", "messageId": "123", "emoji": "👍"}
  {"tool": "message", "action": "poll", "channel": "whatsapp", "question": "Pizza?", "options": ["Yes", "No"]}
  ```

- **canvas**: HTTP server at `/__openclaw__/canvas/` serving agent-editable HTML/CSS/JS. Uses gateway `node.invoke` RPC.
  ```json
  {"tool": "canvas", "action": "present", "file": "dashboard.html"}
  {"tool": "canvas", "action": "eval", "js": "document.getElementById('status').textContent = 'Ready'"}
  {"tool": "canvas", "action": "snapshot"}
  ```

- **cron**: In-process scheduler with persistence to `~/.openclaw/cron/`. Jobs stored as JSON.
  ```json
  {"tool": "cron", "action": "list"}
  {"tool": "cron", "action": "add", "schedule": "0 9 * * *", "task": "Check emails", "label": "morning-check"}
  {"tool": "cron", "action": "remove", "jobId": "job-123"}
  {"tool": "cron", "action": "run", "jobId": "job-123"}
  ```

- **gateway**: Gateway configuration and control.
  ```json
  {"tool": "gateway", "action": "config.get"}
  {"tool": "gateway", "action": "config.patch", "patch": {"agents": {"defaults": {"model": "claude-sonnet-4-20250514"}}}}
  {"tool": "gateway", "action": "restart", "delayMs": 2000}
  ```

- **sessions**: Session management and sub-agent spawning.
  ```json
  {"tool": "sessions_list", "limit": 10, "activeMinutes": 60}
  {"tool": "sessions_history", "sessionKey": "main", "limit": 50}
  {"tool": "sessions_send", "sessionKey": "sub-1", "message": "Status update?", "timeoutSeconds": 30}
  {"tool": "sessions_spawn", "task": "Research topic X", "model": "claude-sonnet-4-20250514", "mode": "run"}
  ```

- **nodes**: WS connections from companion apps (macOS/iOS/Android). Commands executed on device and results streamed back.
  ```json
  {"tool": "nodes", "action": "status"}
  {"tool": "nodes", "action": "notify", "node": "office-mac", "title": "Alert", "body": "Task complete"}
  {"tool": "nodes", "action": "camera_snap", "node": "office-mac"}
  {"tool": "nodes", "action": "run", "node": "office-mac", "command": ["open", "-a", "Safari"]}
  ```

- **image**: Vision model analysis.
  ```json
  {"tool": "image", "image": "/path/to/screenshot.png", "prompt": "What error is shown?"}
  {"tool": "image", "image": "https://example.com/chart.png", "prompt": "Summarize this chart"}
  ```

**Security Model**:
- Tools validated against JSON Schema before execution
- `exec` has allowlist/safeBins/deny modes
- Approval flow for destructive actions (via companion app or CLI)
- Sandbox isolation available (Docker/VM)


## 5. Memory System

### Daily Logs (`memory/YYYY-MM-DD.md`)

- Raw logs of what happened each day
- Read today + yesterday at session start
- Create `memory/` folder if needed

### Long-Term Memory (`MEMORY.md`)

- Curated memories, like human long-term memory
- ONLY load in main session (not shared/group contexts)
- Security: contains personal context that shouldn't leak

### Memory Maintenance

During heartbeats, periodically:
1. Read recent daily files
2. Identify significant events worth keeping
3. Update MEMORY.md with distilled learnings
4. Remove outdated info

**Philosophy**: "Daily files are raw notes; MEMORY.md is curated wisdom."

## 6. Heartbeat and Proactive Behavior

### Heartbeat System

- Periodic polls triggered by configured prompt
- Default prompt: "Read HEARTBEAT.md if it exists..."
- Reply `HEARTBEAT_OK` when nothing needs attention

### When to Check (rotate 2-4x/day)

- Emails - urgent unread messages
- Calendar - upcoming events in 24-48h
- Mentions - social notifications
- Weather - if human might go out

### When to Reach Out

- Important email arrived
- Calendar event coming up (<2h)
- Something interesting found
- Been >8h since last contact

### When to Stay Quiet

- Late night (23:00-08:00) unless urgent
- Human is clearly busy
- Nothing new since last check
- Just checked <30 minutes ago

### Heartbeat vs Cron

**Heartbeat**: Batch multiple checks, conversational context, timing can drift
**Cron**: Exact timing, isolated from main session, different model/thinking level

## 7. Safety and Boundaries

### Default Safety Rules

- Don't exfiltrate private data. Ever.
- Don't run destructive commands without asking.
- `trash` > `rm`
- When in doubt, ask.

### External vs Internal Actions

**Safe to do freely**:
- Read files, explore, organize, learn
- Search the web, check calendars
- Work within workspace

**Ask first**:
- Sending emails, tweets, public posts
- Anything that leaves the machine
- Anything uncertain

### Group Chat Behavior

- "You're not the user's voice"
- Respond when directly mentioned or can add genuine value
- Stay silent when casual banter, already answered, would just be "yeah"
- "Quality > quantity"
- React like a human (emoji reactions on Discord/Slack)

## 8. Comparison with Windsurf Cascade

- **Primary use**: OpenClaw = personal assistant, multi-channel; Cascade = IDE coding assistant
- **Channels**: OpenClaw = WhatsApp, Telegram, Discord, etc.; Cascade = IDE panel only
- **Memory**: OpenClaw = file-based (MEMORY.md, daily logs); Cascade = per-conversation, memories API
- **Tools**: OpenClaw = exec, browser, web_*, message, cron; Cascade = Edit, run_command, read_file, MCP
- **Identity**: OpenClaw = customizable (SOUL.md, IDENTITY.md); Cascade = fixed persona
- **Proactive**: OpenClaw = heartbeats, cron, background tasks; Cascade = hooks only (reactive)
- **Workspace**: OpenClaw = single workspace folder; Cascade = per-project workspace
- **System prompt**: OpenClaw = user-editable bootstrap files; Cascade = system-managed

### Skills, Workflows, and Rules Comparison

**Skills**:
- **Windsurf**: `.windsurf/skills/<name>/SKILL.md` - LLM decides when to apply
- **OpenClaw**: `<workspace>/skills/<name>/SKILL.md` - Same concept, same format (AgentSkills spec)
- Both use `/skill-name` invocation

**Workflows**:
- **Windsurf**: `.windsurf/workflows/*.md` - Step-by-step procedures, `/workflow-name` invocation
- **OpenClaw**: No direct equivalent - use skills with strict step instructions to mimic

**Rules**:
- **Windsurf**: `.windsurf/rules/*.md` - Explicit rule files injected into context
- **OpenClaw**: Embedded in bootstrap files (AGENTS.md, SOUL.md) - merged with persona

**Key Difference**: Windsurf enforces workflow step order at system level. OpenClaw relies on prompt engineering - the LLM "should" follow steps but there's no hard enforcement.

**Bridge Option**: Create an OpenClaw skill that references Windsurf workflows:
```
<workspace>/skills/windsurf-workflows/SKILL.md
→ Lists all .windsurf/workflows/*.md files
→ Instructs agent to read and follow them exactly
```

### Integration Potential

OpenClaw can control Windsurf via:
- **Browser tool**: CDP automation of Electron UI
- **Exec tool**: Run commands, potentially keyboard shortcuts
- **Shared files**: Write to workspace, Cascade hooks detect

## 9. Sources

### Official Documentation [VERIFIED]

- `OCLAW-IN03-SC-OC-SYSP`: https://docs.openclaw.ai/concepts/system-prompt
  - System prompt structure and modes
- `OCLAW-IN03-SC-OC-AGENT`: https://docs.openclaw.ai/concepts/agent
  - Agent runtime, workspace, bootstrap files
- `OCLAW-IN03-SC-OC-AGWK`: https://docs.openclaw.ai/concepts/agent-workspace
  - Workspace file map and purpose
- `OCLAW-IN03-SC-OC-AGMD`: https://docs.openclaw.ai/reference/AGENTS.default
  - Default AGENTS.md content and rules
- `OCLAW-IN03-SC-OC-TOOLS`: https://docs.openclaw.ai/tools
  - Tool inventory and configuration

### Local Files [VERIFIED]

- `OCLAW-IN03-SC-LOCAL-CFG`: `C:\Users\User\.openclaw\openclaw.json`
  - Your installation configuration
- `OCLAW-IN03-SC-LOCAL-WS`: `E:\Dev\openclaw\workspace\`
  - Your workspace bootstrap files

## 10. Token Usage Investigation

### Understanding Token Costs [VERIFIED]

OpenClaw with Anthropic models can consume significant input tokens due to:

- **Extended thinking** - `thinkingDefault` setting controls thinking budget (1K-32K+ tokens per turn)
- **Interleaved thinking with tools** - Thinking blocks preserved across tool calls, resent as INPUT
- **Bootstrap files** - AGENTS.md, SOUL.md, etc. injected each session (up to 150K chars)
- **Conversation history** - Each turn resends all previous messages

**Key insight**: With `thinkingDefault: "medium"` and 10 tool calls, thinking tokens alone can reach 320K+ INPUT tokens per request.

### Enable Payload Logging [VERIFIED]

**Source**: `src/agents/anthropic-payload-log.ts`

**Environment variables:**

- `OPENCLAW_ANTHROPIC_PAYLOAD_LOG=true` - Enable detailed logging
- `OPENCLAW_ANTHROPIC_PAYLOAD_LOG_FILE` - Custom log path (optional)

**Default log location:**

- Standard: `%LOCALAPPDATA%\openclaw\logs\anthropic-payload.jsonl`
- Custom state dir: `$OPENCLAW_STATE_DIR/logs/anthropic-payload.jsonl`
- Your install: `E:\Dev\openclaw\.openclaw\logs\anthropic-payload.jsonl`

**Enable logging (PowerShell):**

```powershell
# Temporary (current session)
$env:OPENCLAW_ANTHROPIC_PAYLOAD_LOG = "true"
openclaw start

# Persistent (user environment)
[Environment]::SetEnvironmentVariable("OPENCLAW_ANTHROPIC_PAYLOAD_LOG", "true", "User")
```

### Log Format

The log file is JSONL (one JSON object per line) with two stage types:

**Request stage** - Full payload sent to Anthropic:
```json
{"ts":"2026-03-03T08:00:00.000Z","stage":"request","runId":"...","payload":{...}}
```

**Usage stage** - Token counts from response:
```json
{"ts":"2026-03-03T08:00:00.000Z","stage":"usage","usage":{"input_tokens":5000,"output_tokens":1000,"cache_read_input_tokens":3000}}
```

### PowerShell Analysis Scripts [TESTED]

**View recent usage entries:**

```powershell
$logPath = "E:\Dev\openclaw\.openclaw\logs\anthropic-payload.jsonl"
Get-Content $logPath | ForEach-Object { $_ | ConvertFrom-Json } |
  Where-Object { $_.stage -eq "usage" } |
  Select-Object ts, @{N='input';E={$_.usage.input_tokens}}, @{N='output';E={$_.usage.output_tokens}}, @{N='cache';E={$_.usage.cache_read_input_tokens}} |
  Format-Table -AutoSize
```

**Calculate totals and input/output ratio:**

```powershell
$logPath = "E:\Dev\openclaw\.openclaw\logs\anthropic-payload.jsonl"
$entries = Get-Content $logPath | ForEach-Object { $_ | ConvertFrom-Json }
$usage = $entries | Where-Object { $_.stage -eq "usage" }
$totalIn = ($usage | Measure-Object -Property { $_.usage.input_tokens } -Sum).Sum
$totalOut = ($usage | Measure-Object -Property { $_.usage.output_tokens } -Sum).Sum
Write-Host "Total Input: $totalIn, Total Output: $totalOut, Ratio: $([math]::Round($totalIn / $totalOut, 1)):1"
```

**Filter by time range (last hour):**

```powershell
$logPath = "E:\Dev\openclaw\.openclaw\logs\anthropic-payload.jsonl"
$cutoff = (Get-Date).AddHours(-1).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ss")
Get-Content $logPath | ForEach-Object { $_ | ConvertFrom-Json } |
  Where-Object { $_.stage -eq "usage" -and $_.ts -gt $cutoff } |
  Select-Object ts, @{N='input';E={$_.usage.input_tokens}}, @{N='output';E={$_.usage.output_tokens}} |
  Format-Table -AutoSize
```

### Thinking Level Configuration [VERIFIED]

Control thinking token budget in `openclaw.json`:

```json
{
  "agents": {
    "defaults": {
      "thinkingDefault": "low"
    }
  }
}
```

**Available levels:**

- `off` - No thinking tokens (0)
- `minimal` - Light reasoning (~1,024 tokens)
- `low` - Standard tasks (~4K tokens)
- `medium` - Complex reasoning (~10K-32K tokens)
- `high` - Very complex tasks (~32K+ tokens)
- `xhigh` - Maximum (select models only)

**Impact**: With `medium` and 10 tool calls, thinking tokens multiply to ~320K INPUT per request. Switching to `low` reduces this by ~8x.

### Anthropic Billing vs Dashboard [VERIFIED]

**Source**: https://platform.claude.com/docs/en/build-with-claude/extended-thinking

Anthropic bills thinking tokens as:

- **Output tokens** - When Claude generates thinking
- **Input tokens** - When thinking blocks from previous turns are resent (tool use)

**Key finding**: With interleaved thinking and tool use, thinking blocks are preserved across tool calls and counted as INPUT on subsequent API calls. This explains high input/output ratios (e.g., 220:1).

## Next Steps

1. **Complete bootstrap ritual** - Delete BOOTSTRAP.md after establishing identity
2. **Configure USER.md** - Add your name, timezone, preferences
3. **Set up memory folder** - Create `memory/` for daily logs
4. **Explore browser tool** - Test CDP automation for Windsurf control
5. **Consider Windsurf integration** - Use findings from OCLAW-IN02 for bidirectional control

## Document History

**[2026-03-03 09:10]**
- Added: Token Usage Investigation section (logging, PowerShell scripts, thinking levels, billing)

**[2026-03-03 08:54]**
- Added: Extension Settings (port 18792 = gateway+3, token from config)

**[2026-03-02 17:09]**
- Added: Browser Profile Configuration section with config example, profiles, extension install, CLI usage

**[2026-03-01 23:46]**
- Added: API Keys via .env File section with supported environment variables

**[2026-03-01 23:24]**
- Added: Search Provider Architecture subsection (5 providers, no browser involvement, config-driven)
- Added: How HTML is Sent to LLM subsection (Readability extraction, Markdown conversion, truncation pipeline)
- Source: OpenClaw source code analysis (`src/agents/tools/web-search.ts`, `web-fetch-utils.ts`)

**[2026-03-01 22:15]**
- Added: Bootstrap File Configuration section with skipBootstrap, bootstrapMaxChars, bootstrapTotalMaxChars options

**[2026-03-01 16:32]**
- Added: Remote Access via Tailscale Serve section with setup steps, device pairing commands, and config examples

**[2026-02-28 10:42]**
- Added: Skills, Workflows, and Rules comparison section with bridge option

**[2026-02-28 10:05]**
- Added: Example JSON calls for all tools in Implementation Architecture

**[2026-02-28 10:00]**
- Added: Implementation Architecture section (protocol stack, wire protocol, tool patterns, security model)

**[2026-02-28 09:55]**
- Added: Comprehensive details for ALL tools (exec, process, web_search, web_fetch, message, cron, gateway, sessions, nodes, image, canvas)
- Expanded from 11-line list to full documentation

**[2026-02-28 09:52]**
- Added: Deep dive on browser tool (profiles, actions, snapshots, CLI examples)
- Added: Windsurf control potential section

**[2026-02-28 09:50]**
- Fixed: Converted Markdown tables to lists (GLOBAL-RULES compliance)
- Fixed: Timeline format to include update count

**[2026-02-28 09:45]**
- Initial research document created
- Analyzed ~/.openclaw folder structure
- Documented all bootstrap files (AGENTS.md, SOUL.md, USER.md, etc.)
- Catalogued tool inventory
- Compared with Windsurf Cascade
