# INFO: How Windsurf Works

**Doc ID**: WSRF-IN01
**Goal**: Document Windsurf IDE features, configuration, and Cascade AI assistant for cross-agent compatibility reference

## Summary

Key findings for cross-agent compatibility:
- Windsurf uses `.windsurf/rules/*.md` for instructions (always-on or trigger-based) [VERIFIED]
- Workflows stored in `.windsurf/workflows/*.md`, invoked as `/workflow-name` [VERIFIED]
- Skills in `.windsurf/skills/<name>/SKILL.md` or `.agents/skills/` using Agent Skills format [VERIFIED]
- Cascade settings: many now in `settings.json` as `windsurf.*` keys (portable); some remain UI-only in `user_settings.pb` [UPDATED 2026-05-05]
- MCP config in `~/.codeium/windsurf/mcp_config.json` [VERIFIED]
- Hooks in `.windsurf/hooks.json` or `~/.codeium/windsurf/hooks.json` [VERIFIED]
- Memories auto-generated during conversation, workspace-scoped [VERIFIED]
- Model switching preserves full context; model fixed per response, change takes effect on next turn [TESTED]
- Smaller context window: earlier messages dropped/summarized automatically without warning [VERIFIED] 
- Different providers (Claude/GPT/SWE): Cascade abstracts differences, transparent switching [VERIFIED]
- Arena Mode: side-by-side model comparison with battle groups and leaderboards [VERIFIED 2026-03]
- Plan Mode: dedicated mode for implementation planning before coding [VERIFIED 2026-03]
- New model picker with family grouping, variant toggles, and pin feature [VERIFIED 2026-03]
- Language server is a 166MB Go binary making direct HTTPS calls to Codeium APIs [TESTED 2026-05]
- Proxy detection disabled by default (`--detect_proxy=false`), controllable via `user_settings.pb` field 34 [TESTED 2026-05]
- MCP transport: NDJSON over stdio (JSON-RPC 2.0), protocol version `2025-11-25` [TESTED 2026-05]
- MCP tools receive ONLY tool_call arguments, zero system prompt leakage [TESTED 2026-05]
- HTTP_PROXY env vars break Cascade when detect_proxy=false (language server ignores proxy, connection fails) [TESTED 2026-05]

## Table of Contents

1. [Overview](#overview)
2. [Directory Structure](#directory-structure)
3. [Settings and Configuration](#settings-storage)
4. [AI Assistant Features](#cascade-ai-assistant)
5. [Memory and Instructions](#workflows-and-rules)
6. [Commands and Workflows](#workflows-and-rules)
7. [Skills](#skills)
8. [Hooks](#cascade-hooks)
9. [MCP Integration](#mcp-integration)
10. [Terminal and CLI](#terminal-features)
11. [Other Features](#other-features)
12. [Key Files Reference](#key-files-reference)
13. [Available Models](#available-models-updated-2026-03)
14. [Architecture Internals](#architecture-internals-tested-2026-05)
15. [Sources](#sources)

## Overview

Windsurf is an AI-powered IDE based on VS Code, developed by Codeium. It includes Cascade, an agentic AI coding assistant that can read, write, and execute code.

## Directory Structure

```
C:\Users\<User>\
├── .codeium\
│   └── windsurf\
│       ├── user_settings.pb      # Cascade UI settings (protobuf binary)
│       ├── mcp_config.json       # MCP server configurations
│       ├── hooks.json            # User-level Cascade hooks
│       ├── global_rules.md       # Global rules for all workspaces
│       ├── skills\               # Global skills (all workspaces)
│       └── metrics\              # Usage metrics
│
├── AppData\
│   ├── Local\Programs\
│   │   ├── Windsurf\             # Main installation
│   │   │   └── resources\app\extensions\  # Built-in extensions
│   │   └── Windsurf Next\        # Preview/beta version
│   │
│   └── Roaming\
│       ├── Windsurf\
│       │   └── User\
│       │       ├── settings.json      # Editor settings (JSON)
│       │       ├── keybindings.json   # Keyboard shortcuts
│       │       └── globalStorage\
│       │           └── state.vscdb    # SQLite state database
│       │
│       └── Windsurf - Next\
│           └── User\             # Same structure as Windsurf
```

## Settings Storage

### Two Separate Settings Systems

Windsurf uses **two different systems** for storing settings:

- **Editor settings**
  - Format: JSON
  - Location: `%APPDATA%\Windsurf\User\settings.json`
  - Editable: Yes, text editor
- **Cascade settings** (UI-only subset)
  - Format: Protobuf binary
  - Location: `%USERPROFILE%\.codeium\windsurf\user_settings.pb`
  - Editable: No, UI only
  - Note: Many Cascade settings now also writable via `windsurf.*` keys in `settings.json`

### Editor Settings (settings.json)

Standard VS Code settings in JSON format, plus many `windsurf.*` Cascade settings.

**Location:** `C:\Users\<User>\AppData\Roaming\Windsurf\User\settings.json`

**Standard editor keys:** theme, font, tab size, extension settings, git, terminal preferences.

**Windsurf/Cascade keys confirmed in settings.json** (updated 2026-05-05):
```json
{
  "windsurf.autoExecutionPolicy": "turbo",
  "windsurf.autoWebRequestPolicy": "turbo",
  "windsurf.autoContinue": true,
  "windsurf.completionMode": "autocomplete",
  "windsurf.chatFontSize": "default",
  "windsurf.rememberLastModelSelection": true,
  "windsurf.openRecentConversation": true,
  "windsurf.explainAndFixInCurrentConversation": false,
  "windsurf.allowCascadeAccessGitignoreFiles": true,
  "windsurf.acp.enabledAgents": { "devin-cli": true }
}
```

**Deprecated keys** (superseded by `windsurf.completionMode`):
- `windsurf.autocompleteEnabled`
- `windsurf.enableSupercomplete`
- `windsurf.autocompleteSpeed`

### Cascade Settings (user_settings.pb)

**UPDATE (2026-05-05):** Many settings previously believed to be protobuf-only are now also available as `windsurf.*` keys in `settings.json` (see above). The protobuf file still exists and stores additional state.

**Location:** `C:\Users\<User>\.codeium\windsurf\user_settings.pb`

**Settings confirmed as UI-only** (no `settings.json` key found):
- **Allow Cascade in Background** - Whether Cascade runs when switching conversations
- **Auto-Generate Memories** - Autonomously create memories
- **Auto-Open Edited Files** - Open files in background when Cascade edits them
- **Cascade Auto-Fix Lints** - Auto-fix lint errors from Cascade edits
- **Disable Fast Context Agent** - Disable parallel search subagent
- **Enable Cascade Web Tools** - Web search capability
- **Read Claude Code Config** - Read .claude/skills/ directories
- **Windsurf Preview** - Browser previews for dev servers
- **Cascade Completion Notifications** - Background completion notifications
- **Search Max Workspace File Count** - Embedding file count limit (default 5000)
- **Detect Proxy** - Automatic proxy detection

**Also stored:** model configurations, conversation IDs, allow/deny lists for auto-execution.

**Implications:**
- UI-only settings must be configured through Windsurf Settings panel
- The `windsurf.*` keys in `settings.json` ARE portable via file copy
- The `.pb` file contains both redundant copies and exclusive settings

### State Database (state.vscdb)

SQLite database storing:
- Window state and layout
- Recent files and workspaces
- Extension state
- Command history

**Location:** `C:\Users\<User>\AppData\Roaming\Windsurf\User\globalStorage\state.vscdb`

## Cascade AI Assistant

Open Cascade: `Cmd/Ctrl+L` or click Cascade icon (top right). Selected text in editor/terminal auto-included.

### Modes

- **Code Mode**: Create and modify codebase files
- **Chat Mode**: Questions about codebase or coding principles (proposes code you can accept/insert)
- **Plan Mode**: Create detailed implementation plans before coding. Type `megaplan` for advanced form with clarifying questions [NEW 2026-01-30]
- **Arena Mode**: Side-by-side model comparison with hidden identities. Select via Arena tab in model picker [NEW 2026-01-30]

### Capabilities

- **Read/Write files** - View and modify source code
- **Run terminal commands** - Execute shell commands with permission controls
- **Web search** - `@web` for general search, `@docs` for curated docs, paste URLs
- **MCP integration** - Connect to external tools (GitHub, databases, APIs)
- **Tool calling** - Up to 20 tools per prompt; use "continue" button if stopped
- **Voice input** - Transcribe speech to text
- **Plans and Todo Lists** - Built-in planning agent for complex tasks
- **Queued Messages** - Queue new messages while Cascade works
- **Linter integration** - Auto-fix linting errors (free, no credit charge)
- **Git Worktree Support** - Spawn multiple sessions in same repo without conflicts [NEW Wave 13]
- **Multi-Cascade Panes & Tabs** - View sessions side-by-side or as dashboard [NEW Wave 13]
- **Cascade Dedicated Terminal** - Reliable zsh shell for agent commands (Beta, opt-in) [NEW Wave 13]

### Checkpoints and Reverts

- Hover over prompt > click revert arrow to restore codebase state
- Create named snapshots from within conversation
- **Warning**: Reverts are currently irreversible

### Real-time Awareness

Cascade is aware of your real-time actions - no need to re-prompt context. Just say "Continue".

### Simultaneous Cascades

Multiple Cascades can run simultaneously. Navigate via dropdown (top left of panel).
**Warning**: If two Cascades edit same file simultaneously, edits can race and fail.

### Prompt Syntax (Agentic Language Enrichments)

Cascade supports several input enrichments for precise control:

**@mentions** - Reference context:
- `@file` - Reference specific files
- `@skill-name` - Invoke a skill
- `@web` / `@docs` - Web/docs search
- `@terminal` - Reference terminal output
- `@conversation` - Reference previous conversations (retrieves relevant parts)
- `@codemap-name` - Reference a codemap

**/workflows** - Invoke automation:
- `/workflow-name` - Run workflow from `.windsurf/workflows/`
- Workflows are Markdown files with YAML frontmatter

**Other enrichments:**
- **URL pasting** - Paste URLs directly, Cascade fetches content
- **Selected text** - Highlight in editor/terminal, then `Ctrl+L` to include
- **Image attachments** - Drag/drop or paste images into chat

### Sharing Conversations

Teams/Enterprise only: Click `...` > "Share Conversation" to share trajectories with team.

### Auto Execution Policies

- **Disabled** - All commands require manual approval
- **Allowlist** - Only allowlisted commands auto-execute (`windsurf.cascadeCommandsAllowList`)
- **Auto** - Model decides if safe (premium models only)
- **Turbo** - All commands auto-execute except denylist (`windsurf.cascadeCommandsDenyList`)

### Auto-Continue

When enabled, Cascade automatically continues when hitting per-response limit. Each continue consumes credits.

### Arena Mode [NEW 2026-01-30]

Side-by-side model comparison with hidden identities:

- **Battle Groups** - Choose specific models or let Windsurf select from curated groups ("fast models" vs "smart models")
- **Personal & Global Leaderboards** - Votes contribute to both personal preferences and global rankings
- **Sync or Branch** - Send followups to both agents simultaneously, or branch to explore different paths
- **Free Trial** - Battle groups free for first week for paid users

Access via Arena tab in model picker.

### Plan Mode [NEW 2026-01-30]

Dedicated mode for implementation planning:

- Create detailed plans before diving into code
- Type `megaplan` in input box for advanced form with clarifying questions
- Auto-switches back to Code Mode when you start implementing

### New Model Picker [NEW 2026-03]

- Groups models by family with hovercards
- Toggles for variants (reasoning effort, speed)
- Pin favorite models for quick access

### Model Switching and Context Window [TESTED 2026-01-26]

**Key behavior when switching models mid-conversation:**

- **Context preserved** - Full conversation history stays intact when switching models [VERIFIED]
- **Model fixed per response** - Model selection happens BEFORE response generation; cannot switch mid-turn [TESTED]
- **New model sees full context** - The switched-to model receives complete conversation (messages, tool calls, file reads) [VERIFIED]
- **No context reset** - Switching does NOT start fresh; continues with existing context [TESTED]
- **Token limits differ** - Models have different context windows (e.g., Claude ~200K, some GPT variants smaller) [VERIFIED]
- **Automatic truncation** - When context grows too long, Cascade summarizes messages and clears history [VERIFIED]
- **Context window indicator** - UI shows current context usage to help decide when to start new session [VERIFIED]

**Smaller context window behavior:** [VERIFIED from changelog]
- When switching to model with smaller context, earlier context may be **dropped without warning**
- Cascade mitigates this by **summarizing messages** before truncation
- No explicit user control over what gets truncated
- Recommendation: Start new session when approaching limits or switching to smaller model

**Different provider behavior (Claude vs GPT vs SWE):** [VERIFIED]
- **Tool schemas differ** - Each provider has different tool calling conventions
- **System prompt handling** - Providers interpret system prompts differently
- **Cascade abstracts this** - Windsurf handles provider differences internally
- **No user action needed** - Switching providers mid-conversation works transparently
- **Potential issues**: Complex tool sequences may behave differently across providers [ASSUMED]

**Execution model:**
```
[User sends message]
       |
[Model is selected] <-- FIXED for entire response
       |
[Agent generates response with full context]
       |
[Response complete]
       |
[Next user message] <-- Only here can model change take effect
```

**Implications for cost optimization:**

- Agent cannot switch its own model mid-response
- Tier-based switching must happen at conversation turn boundaries
- Each model processes the FULL context (cost compounds on long conversations)
- Cross-conversation references (`@conversation`) retrieve relevant parts only to avoid overwhelming context window [VERIFIED]

**Source**: Session research `_2026-01-26_AutoModelSwitcher`, docs.windsurf.com/windsurf/cascade/cascade

## Cascade Hooks

Execute custom shell commands at key points in Cascade's workflow for logging, security, validation.

### Hook Locations (merged in order: system > user > workspace)

- **System**: `C:\ProgramData\Windsurf\hooks.json` (Windows), `/etc/windsurf/hooks.json` (Linux)
- **User**: `~/.codeium/windsurf/hooks.json`
- **Workspace**: `.windsurf/hooks.json`

### Hook Events

- `pre_read_code` / `post_read_code` - Before/after file read
- `pre_write_code` / `post_write_code` - Before/after file write
- `pre_run_command` / `post_run_command` - Before/after terminal command
- `pre_mcp_tool_use` / `post_mcp_tool_use` - Before/after MCP tool
- `pre_user_prompt` / `post_cascade_response` - Before/after user interaction
- `post_cascade_response_with_transcript` - Response with full transcript [NEW 2026-03]
- `post_setup_worktree` - After worktree initialization [NEW 2026-02]

**Pre-hooks can block actions** by exiting with code 2.

**New fields in `post_cascade_response`:**
- `rules_applied` - Tracks which rules were triggered [NEW 2026-02]

### Configuration Example

```json
{
  "hooks": {
    "pre_write_code": [
      {
        "command": "python3 /path/to/validator.py",
        "show_output": true,
        "working_directory": "/path/to/dir"
      }
    ]
  }
}
```

### Use Cases

- Logging all Cascade actions for compliance
- Blocking access to sensitive files
- Running formatters/linters after edits
- Blocking dangerous commands

### Enterprise Hook Features [NEW 2026-02]

- **Cloud configuration** - Configure hooks via cloud dashboard for enterprise teams
- **Organization-wide allow/deny lists** - Admins set command auto-execution policies
- **Windows Group Policy** - Manage Windsurf restrictions via GPO
- **System-level Rules & Workflows** - Deploy via MDM policies

## MCP Integration

Model Context Protocol enables Cascade to access custom tools and services.

### Configuration

**Location**: `~/.codeium/windsurf/mcp_config.json`

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "<TOKEN>"
      }
    }
  }
}
```

### Transport Types

- `stdio` - Standard input/output
- `Streamable HTTP` - HTTP endpoint
- `SSE` - Server-sent events

### Tool Limit

Cascade has limit of 100 total MCP tools. Toggle individual tools in MCP settings.

### Adding MCPs

Cascade panel > MCPs icon (top right) > MCP Marketplace, or edit `mcp_config.json` manually.

### MCP Improvements [NEW 2026-03]

- **Refresh button** - Manually refresh MCP server connections
- **Auto OAuth** - Automatic OAuth login when adding HTTP/SSE MCP servers
- **Improved context management** - Better handling of MCP server context

## Workflows and Rules

### Workflows

Custom automation scripts stored in `.windsurf/workflows/` as Markdown files.

**Format:**
```markdown
---
description: Short description of workflow
---
Step-by-step instructions...
```

**Invocation:** `/workflow-name` in Cascade chat

### Rules

Project-specific instructions for Cascade. Max 12000 characters per rule file.

**Locations:**
- `.windsurf/rules/` - Workspace rules (also discovered in subdirs and up to git root)
- Global rules via Windsurf Settings panel

**Activation Modes:**
- **Manual** - Via `@mention` in Cascade input
- **Always On** - Always applied
- **Model Decision** - Model decides based on description
- **Glob** - Applied to files matching pattern (e.g., `*.js`, `src/**/*.ts`)

### Memories

Persistent context Cascade remembers across conversations:
- Auto-generated during conversation (workspace-scoped)
- User-created via "remember this" commands
- Creating/using memories does NOT consume credits

### AGENTS.md

Directory-scoped instructions that auto-apply based on file location.

- **Root directory**: Instructions apply globally (like "always on" rule)
- **Subdirectories**: Instructions apply only when working with files in that dir

**Format**: Plain markdown, no frontmatter required. File: `AGENTS.md` or `agents.md`

**vs Rules**: AGENTS.md = simple location-based; Rules = complex activation logic

## Skills

Skills bundle complex multi-step tasks with supporting resources into folders that Cascade can invoke.

**Based on**: Agent Skills open format (https://agentskills.io/)

### Skill Locations

- **Workspace**: `.windsurf/skills/<skill-name>/SKILL.md`
- **Workspace (alt)**: `.agents/skills/<skill-name>/SKILL.md` [NEW 2026-02]
- **Global**: `~/.codeium/windsurf/skills/<skill-name>/SKILL.md`
- **System (Enterprise)**: MDM-managed configs for organization-wide skills [NEW 2026-03]

### SKILL.md Format

```yaml
---
name: deploy-to-production
description: Guides the deployment process to production with safety checks
---

## Pre-deployment Checklist
1. Run all tests
2. Check for uncommitted changes
...
```

### Creating Skills

**Via UI**: Cascade panel > three dots > Customizations > Skills > "+ Workspace" or "+ Global"

**Manual**: Create folder `.windsurf/skills/<skill-name>/` with `SKILL.md`

### Invocation

- **Automatic**: Cascade uses progressive disclosure to invoke when task matches description
- **Manual**: Type `@skill-name` in Cascade input

### Skills vs Rules vs Workflows

- **Skills**: Complex tasks with supporting files (folder). Invoked via progressive disclosure or @-mention.
- **Rules**: Behavioral guidelines (single file). Trigger-based.
- **Workflows**: Automation scripts (single file). Invoked via `/command`.

See `_INFO_AGENT_SKILLS.md` for full specification details.

## Terminal Features

### Command Mode

`Cmd/Ctrl+I` in terminal - Generate CLI syntax from natural language prompts.

### Cascade Integration

- Highlight terminal text + `Cmd/Ctrl+L` to send to Cascade
- `@terminal` to reference terminal in chat

### Allow/Deny Lists

- `windsurf.cascadeCommandsAllowList` - Commands that always auto-execute
- `windsurf.cascadeCommandsDenyList` - Commands that never auto-execute

## Other Features

### Codemaps (Beta)

Shareable hierarchical maps of codebase showing code execution flow and component relationships.

- Access: Activity Bar (left) or Command Palette > "Focus on Codemaps View"
- Create from recent navigation or custom prompt
- Reference in Cascade via `@codemap-name`

### AI Commit Messages

Generate git commit messages with one click (sparkle icon next to commit field).
Available to all paid users, no limits.

### Explain and Fix

Highlight error in editor > click "Explain and Fix" for Cascade to resolve.

### Send Problems to Cascade

Problems panel > "Send to Cascade" button to include as @-mention.

### Working with Private/Gitignored Folders

Cascade can read/write gitignored files when explicitly referenced, but gitignored folders are hidden from the workspace snapshot shown at conversation start.

**To make a gitignored folder visible to Cascade while keeping contents private:**

1. Use a `.gitkeep` file to track the folder structure
2. Configure `.gitignore` to ignore contents but not the `.gitkeep`

**.gitignore pattern:**
```gitignore
# Private sessions folder (contents ignored, folder tracked)
# Pattern: ignore all contents (*) but negate (!) the .gitkeep file
# Result: folder visible in git/Cascade, but session files stay private
_PrivateSessions/*
!_PrivateSessions/.gitkeep
```

**.gitkeep file:**
```bash
echo "# This file makes the folder visible to Cascade" > _PrivateSessions/.gitkeep
```

**How it works:**
- `_PrivateSessions/*` - Ignores all files/folders inside
- `!_PrivateSessions/.gitkeep` - Negation pattern, tracks this specific file
- Result: Folder appears in workspace, contents stay private

### Telemetry and Privacy

Windsurf collects non-essential telemetry data by default. Opt out via Codeium account settings.

**Disable Telemetry:**
1. Open https://windsurf.com/account (or Codeium account page)
2. Scroll to **Privacy** section
3. Toggle **Disable Telemetry** to on

**What it controls:**
- Non-essential data collection used to improve the product
- Does NOT affect prompt caching, autocomplete, or Cascade functionality
- Stored server-side (account setting), not in local config files

## Key Files Reference

**User Config:**
- `settings.json` - Editor preferences (JSON, editable)
- `keybindings.json` - Keyboard shortcuts
- `user_settings.pb` - Cascade UI settings (protobuf, UI-only)
- `state.vscdb` - Window/extension state (SQLite)
- `mcp_config.json` - MCP server configurations
- `~/.codeium/windsurf/hooks.json` - User-level Cascade hooks

**Workspace Config:**
- `.codeiumignore` - Files Cascade should ignore
- `.windsurf/workflows/*.md` - Custom workflows
- `.windsurf/rules/*.md` - Project rules for Cascade
- `.windsurf/skills/*/SKILL.md` - Skills with supporting resources
- `.windsurf/hooks.json` - Workspace-level Cascade hooks
- `AGENTS.md` - Directory-scoped instructions

## Available Models [Updated 2026-03]

Models available in Cascade, grouped by provider:

**OpenAI:**
- GPT-5.4, GPT-5.4 Mini (latest)
- GPT-5.3-Codex-Spark
- GPT-5.2-Codex (with reasoning efforts: low, medium, high, xhigh)
- GPT-5.1, GPT-5.1-Codex

**Anthropic:**
- Claude Opus 4.6 (with/without thinking, fast mode available)
- Claude Sonnet 4.6 (with/without thinking)
- Claude Sonnet 4.5

**Google:**
- Gemini 3.1 Pro (low/high thinking)
- Gemini 3 Pro, Gemini 3 Flash

**Codeium:**
- SWE-1.5 (free for all users, default model)
- SWE-1, SWE-1-lite, SWE-1-mini

**Other:**
- GLM-5 (Zhipu AI)
- Minimax M2.5

**Reasoning Effort:** Many models support configurable reasoning effort (none, low, medium, high, xhigh) affecting speed and cost.

## Architecture Internals [TESTED 2026-05]

Reverse-engineered from binary analysis, process inspection, and interception testing during session `_2026-05-27_CascadeMetapromptExtraction`.

### Process Model

Windsurf runs as multiple processes:

```
Windsurf.exe (Electron main process)
├─ Windsurf.exe (GPU process)
├─ Windsurf.exe (renderer - editor UI)
├─ Windsurf.exe (extension host - Node.js)
├─ Windsurf.exe (shared process)
├─ Windsurf.exe (file watcher)
└─ language_server_windows_x64.exe (Codeium language server - Go binary)
```

- **Electron processes** (~14 total): Standard VS Code/Electron architecture. Renderer, GPU, extension host, file watcher, shared process, utility processes.
- **Language server** (1 process): The critical binary that handles ALL Cascade AI communication.

### Language Server Binary [TESTED]

**Path**: `C:\Users\<User>\AppData\Local\Programs\Windsurf\resources\app\extensions\windsurf\bin\language_server_windows_x64.exe`

**Characteristics:**
- Size: ~166 MB
- Language: Go (compiled binary, contains Go runtime strings)
- Launched by: `extension.js` in the Windsurf extension via `child_process.spawn()`
- Modified: Matches Windsurf release date (updated with each Windsurf version)

**Command line** (observed via `Win32_Process.CommandLine`):
```
language_server_windows_x64.exe
  --api_server_url https://server.self-serve.windsurf.com
  --run_child
  --enable_lsp
  --extension_server_port <port>
  --ide_name windsurf
  --random_port
  --inference_api_server_url https://inference.codeium.com
  --database_dir <user_home>\.codeium\windsurf\database\<hash>
  --enable_index_service
  --enable_local_search
  --search_max_workspace_file_count 5000
  --indexed_files_retention_period_days 30
  --workspace_id <workspace_id>
  --sentry_telemetry
  --sentry_environment stable
  --codeium_dir .codeium/windsurf
  --extensions_dir <user_home>\.windsurf\extensions
  --parent_pipe_path \\.\pipe\server_<uuid>
  --windsurf_version <version>
  --stdin_initial_metadata
  --detect_proxy=false
```

**Key parameters:**
- `--api_server_url`: Primary Codeium API endpoint (account, settings, telemetry)
- `--inference_api_server_url`: AI inference endpoint (Cascade chat completions)
- `--parent_pipe_path`: Named pipe for IPC between extension host and language server
- `--detect_proxy`: Controls whether the binary honors HTTP_PROXY/HTTPS_PROXY env vars
- `--stdin_initial_metadata`: Binary receives API key via stdin (protobuf) at startup, then stdin closes

### API Endpoints [TESTED]

- `https://server.self-serve.windsurf.com` - Primary API (auth, settings, telemetry, user data)
- `https://inference.codeium.com` - AI inference (Cascade chat, completions, tool calls)

Both are HTTPS. The language server makes direct outbound connections (not via Electron/Node.js network stack).

### Startup Sequence [TESTED]

Reconstructed from `extension.js` (minified, 9.4MB) analysis:

1. **Electron main process** starts, loads workspace
2. **Extension host** (Node.js) loads `windsurf` extension
3. Extension reads `UserSettings` from `user_settings.pb` via `SettingsWatcher`
4. Extension builds environment: `{ ...process.env, ...languageServerEnv, CODEIUM_EDITOR_APP_ROOT, WINDSURF_CSRF_TOKEN }`
5. Extension reads `detectProxy` from `UserSettingBroadcaster.getInstance().userSettings.detectProxy` (default: `false`)
6. Extension creates named pipe: `\\.\pipe\server_<uuid>`
7. Extension spawns `language_server_windows_x64.exe` with full argument list including `--detect_proxy=<value>`
8. Extension writes API key metadata (protobuf binary) to language server stdin, then closes stdin
9. Language server connects to Codeium APIs and signals ready via named pipe
10. Cascade UI becomes interactive

**Key code** (from `extension.js`, deobfuscated):
```javascript
// Environment construction
const env = {
  ...process.env,
  ...languageServerEnv,
  ...getExtraEnv(),
  CODEIUM_EDITOR_APP_ROOT: appRoot,
  WINDSURF_CSRF_TOKEN: csrfToken,
  ...(isWindsurfInsiders() ? { GORACE: "halt_on_error=1" } : {})
};

// Proxy detection from user settings
const detectProxy = await (async function(env) {
  let enabled = false;
  try {
    const settings = UserSettingBroadcaster.getInstance();
    await settings.isReady;
    enabled = settings.userSettings.detectProxy;
  } catch {}
  return processProxySettings(enabled, env);
})(env);

args.push(`--detect_proxy=${detectProxy}`);

// Spawn language server
const child = spawn(binaryPath, args, { cwd: undefined, env: env });
const metadata = MetadataProvider.getInstance().getMetadata();
if (metadata.apiKey) {
  child.stdin.write(metadata.toBinary());
}
child.stdin.end();
```

### Proxy Detection [TESTED]

**Setting location**: `user_settings.pb` field 34 (`detect_proxy`, bool, protobuf wire type 0)

**Default**: `false` (proxy detection disabled)

**Effect when false**: Language server binary ignores `HTTP_PROXY`, `HTTPS_PROXY`, `NO_PROXY` env vars entirely. All connections go direct.

**Effect when true**: Language server binary reads and honors standard proxy env vars. The Go binary contains full proxy support (proxy.Proxy, proxyURL, proxyAuth, proxyForURL, proxyManager, proxyAddress, proxyNetwork - 418 proxy-related strings found in binary).

**Go binary proxy env var support** (confirmed via string analysis):
- `HTTP_PROXY` / `http_proxy`
- `HTTPS_PROXY` / `https_proxy`
- `NO_PROXY` / `no_proxy`
- Standard Go `net/http` proxy resolution via `golang.org/s/cgihttpproxy`

**UI location**: Windsurf Settings panel > "Detect Proxy" checkbox (UI-only setting, not in `settings.json`)

**Test result**: With `detect_proxy=false` and `HTTP_PROXY`/`HTTPS_PROXY` set, Cascade is completely non-functional. UI loads but messages cannot be submitted (Enter key does nothing). The language server fails to connect to Codeium APIs because it ignores the proxy but the proxy env vars may affect other components.

### Network Architecture [TESTED]

Three independent network stacks in Windsurf:

1. **Chromium** (Electron renderer): Uses `--proxy-server` flag or system proxy. `HTTP_PROXY` env vars NOT directly honored. Handles: marketplace, update checks, web previews.
2. **Node.js** (extension host): Honors `HTTP_PROXY`/`HTTPS_PROXY` env vars and `NODE_TLS_REJECT_UNAUTHORIZED`. Handles: extension operations, MCP communication.
3. **Go binary** (language server): Independent TLS stack. Honors proxy env vars ONLY when `--detect_proxy=true`. Handles: ALL Cascade AI communication, completions, telemetry.

**Consequence**: Setting proxy env vars without enabling `detect_proxy` creates a split-brain: Node.js extension host may route through proxy while the language server goes direct (or fails if env vars affect DNS/routing).

### Extension-Language Server Communication [TESTED]

**Transport**: Named pipe (`\\.\pipe\server_<uuid>`)

**Protocol**: Protobuf-based RPC (language server is a gRPC/protobuf service)

**Key files involved:**
- `extension.js` (9.4MB, minified): Orchestrates spawn, IPC, settings
- `user_settings.pb`: Protobuf binary with `UserSettings` message
- Named pipe: bidirectional communication after startup

**Settings sync**: Extension writes settings changes to language server via `setUserSettings` RPC call. Settings are also persisted to `user_settings.pb` file and watched for external changes.

### MCP Transport [TESTED]

- **Protocol**: JSON-RPC 2.0
- **Transport**: NDJSON (newline-delimited JSON) over stdio
- **NOT**: LSP-style Content-Length headers (initial assumption was wrong)
- **Protocol version**: Windsurf requests `2025-11-25`
- **Tool visibility**: MCP tools receive ONLY `tool_call` arguments. System prompt, conversation context, user rules, memories, workspace info are NOT visible to MCP servers.
- **Registration**: Tools visible to Cascade within seconds of Windsurf restart
- **Config**: `~/.codeium/windsurf/mcp_config.json`

### Inspected Files Reference

- `C:\Users\<User>\AppData\Local\Programs\Windsurf\resources\app\extensions\windsurf\dist\extension.js` (9.4MB, minified JS) - Main extension logic, language server spawn, settings management
- `C:\Users\<User>\AppData\Local\Programs\Windsurf\resources\app\extensions\windsurf\bin\language_server_windows_x64.exe` (166MB, Go binary) - Codeium language server, AI communication
- `C:\Users\<User>\AppData\Local\Programs\Windsurf\resources\app\extensions\windsurf\package.json` - Extension manifest, declared settings
- `C:\Users\<User>\.codeium\windsurf\user_settings.pb` (69KB, protobuf) - User settings including `detectProxy` (field 34)
- `C:\Users\<User>\.codeium\windsurf\mcp_config.json` - MCP server configurations
- `C:\Users\<User>\AppData\Roaming\Windsurf\User\settings.json` - VS Code/Windsurf JSON settings

### Protobuf Schema (UserSettings, partial) [TESTED]

Extracted from `extension.js` protobuf definitions:

```
UserSettings {
  field 33: disable_cascade_browser_previews (bool)
  field 34: detect_proxy (bool)
  field 35: disable_tab_to_import (bool)
  field 36: use_clipboard_for_completions (bool)
  // ... additional fields
}
```

Default values are protobuf defaults (false for bool, 0 for int, "" for string). Unset fields are omitted from the .pb file.

### Interception Test Results Summary [TESTED]

| Method | Can capture exact API payload? | Issue |
|--------|-------------------------------|-------|
| DevTools Network Tab | No | Extension host traffic in separate process [ASSUMED] |
| MCP Server Observer | No | Only sees tool_call arguments, not prompt |
| HTTP Proxy (env vars) | No | `detect_proxy=false` causes Cascade to break |
| HTTP Proxy (detect_proxy=true) | TBD | Not yet tested with setting enabled |
| SSLKEYLOGFILE | TBD | Go binary unlikely to honor (requires explicit `tls.Config.KeyLogWriter`) |
| mitmproxy local mode (WinDivert) | TBD | Network-level capture, still needs MITM cert trust |

### Next Steps for Exact Prompt Capture

1. **Enable `detect_proxy=true`** via Windsurf Settings UI, install mitmproxy CA cert in Windows trust store, retry proxy interception
2. **Named pipe interception**: Monitor `\\.\pipe\server_*` for protobuf messages between extension and language server
3. **Process memory dump**: Search language server process memory for prompt content after Cascade interaction

## Sources

**Cascade Documentation:** [TESTED 2026-01-13]
- https://docs.windsurf.com/windsurf/cascade/cascade - Cascade overview, modes, features
- https://docs.windsurf.com/windsurf/cascade/hooks - Cascade Hooks configuration and events
- https://docs.windsurf.com/windsurf/cascade/mcp - MCP integration and configuration
- https://docs.windsurf.com/windsurf/cascade/memories - Memories, Rules, and activation modes
- https://docs.windsurf.com/windsurf/cascade/agents-md - AGENTS.md directory-scoped instructions
- https://docs.windsurf.com/windsurf/cascade/web-search - Web and docs search
- https://docs.windsurf.com/windsurf/terminal - Terminal features and auto-execution
- https://docs.windsurf.com/windsurf/codemaps - Codemaps (Beta)
- https://docs.windsurf.com/windsurf/cascade/skills - Skills

**Other:**
- Windsurf Changelog: https://windsurf.com/changelog
- Agent Skills Specification: https://agentskills.io/
- Local file system investigation (2026-01-11)
- Session `_2026-01-26_AutoModelSwitcher` - Model switching and context window research [TESTED]
- https://docs.windsurf.com/windsurf/cascade/worktrees - Git worktree support [NEW 2026-02]
- https://docs.windsurf.com/windsurf/cascade/skills - Skills (system-level support) [UPDATED 2026-03]
- Session `_2026-05-27_CascadeMetapromptExtraction/S03_CSMP-ExtractionTesting_2026-05-27` - Binary analysis, process inspection, interception testing [TESTED 2026-05]
- `Win32_Process.CommandLine` inspection of `language_server_windows_x64.exe` [TESTED 2026-05]
- String analysis of Go binary (166MB) for proxy, TLS, and protocol strings [TESTED 2026-05]
- `extension.js` (9.4MB) regex-based deobfuscation of spawn logic, settings watcher, proxy detection [TESTED 2026-05]
- MCP observer tool (custom NDJSON JSON-RPC 2.0 server) confirming transport protocol [TESTED 2026-05]
- mitmproxy 12.2.3 interception testing (proxy mode) confirming language server proxy behavior [TESTED 2026-05]

## Document History

**[2026-05-28 12:29]**
- Added: Architecture Internals section with process model, language server binary analysis, API endpoints, startup sequence, proxy detection, network architecture, MCP transport, and inspected files reference [TESTED]
- Added: Summary entries for language server, proxy detection, MCP transport findings
- Added: Sources for session S03 testing, binary analysis, extension.js deobfuscation, MCP observer, mitmproxy testing
- Updated: TOC with Architecture Internals entry

**[2026-03-30 19:48]**
- Added: Telemetry and Privacy subsection under Other Features [VERIFIED]

**[2026-03-19 10:33]**
- Added: Arena Mode section with battle groups, leaderboards, sync/branch
- Added: Plan Mode section with megaplan command
- Added: New Model Picker section (family grouping, variant toggles, pin)
- Added: Git Worktree Support, Multi-Cascade Panes & Tabs, Dedicated Terminal to Capabilities
- Added: New hooks (post_cascade_response_with_transcript, post_setup_worktree, rules_applied field)
- Added: .agents/skills/ as alternate skill location
- Added: MCP Improvements section (refresh button, auto OAuth)
- Added: Enterprise Hook Features (cloud config, org-wide policies, GPO, MDM)
- Added: System-level Skills for Enterprise
- Updated: Summary with Arena Mode, Plan Mode, New Model Picker findings
- Source: windsurf.com/changelog (Wave 13-14, Feb-Mar 2026 updates)

**[2026-01-26 13:22]**
- Added: Smaller context window behavior (truncation, summarization)
- Added: Different provider behavior (Claude/GPT/SWE abstraction)
- Source: windsurf.com/changelog (Wave 13 Context Window Indicator)

**[2026-01-26 13:20]**
- Added: Model Switching and Context Window section with [TESTED] findings
- Added: Summary entry for model switching behavior

**[2026-01-13]**
- Initial document created from Cascade documentation research
