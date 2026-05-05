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
14. [Sources](#sources)

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

## Document History

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
