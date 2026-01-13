# How Windsurf Works

## Table of Contents

1. [Overview](#overview)
2. [Directory Structure](#directory-structure)
3. [Settings Storage](#settings-storage)
4. [Cascade AI Assistant](#cascade-ai-assistant)
5. [Cascade Hooks](#cascade-hooks)
6. [MCP Integration](#mcp-integration)
7. [Workflows and Rules](#workflows-and-rules)
8. [Skills](#skills)
9. [Terminal Features](#terminal-features)
10. [Other Features](#other-features)
11. [Key Files Reference](#key-files-reference)
12. [Sources](#sources)

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
- **Cascade settings**
  - Format: Protobuf binary
  - Location: `%USERPROFILE%\.codeium\windsurf\user_settings.pb`
  - Editable: No, UI only

### Editor Settings (settings.json)

Standard VS Code settings in JSON format:
- Theme, font, tab size
- Extension settings
- Git integration
- Terminal preferences

**Location:** `C:\Users\<User>\AppData\Roaming\Windsurf\User\settings.json`

Example keys:
```json
{
  "workbench.colorTheme": "KarstenIse",
  "editor.fontFamily": "'JetBrains Mono', Consolas",
  "editor.tabSize": 2,
  "windsurf.enableSupercomplete": false,
  "windsurf.autocompleteSpeed": "fast",
  "windsurf.autoExecutionPolicy": "off"
}
```

### Cascade Settings (user_settings.pb)

**IMPORTANT DISCOVERY (2026-01-11):**

The Cascade-specific settings visible in the Windsurf Settings panel are stored in a **Protocol Buffers binary file**, not in `settings.json`.

**Location:** `C:\Users\<User>\.codeium\windsurf\user_settings.pb`

Settings stored here include:
- **Allow Cascade in Background** - Whether Cascade runs when switching conversations
- **Auto Execution** - Terminal command auto-execution policy (Disabled/Allowlist/Auto/Turbo)
- **Auto Web Requests** - Web request auto-fetch policy
- **Auto-Continue** - Automatically continue when hitting per-response limit
- **Auto-Generate Memories** - Autonomously create memories
- **Auto-Open Edited Files** - Open files in background when Cascade edits them

**Implications:**
- These settings cannot be edited by hand
- Not portable via batch scripts copying settings.json
- Must be configured through Windsurf UI (Settings panel)
- The `.pb` file also contains model configurations and conversation IDs

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

### Checkpoints and Reverts

- Hover over prompt > click revert arrow to restore codebase state
- Create named snapshots from within conversation
- **Warning**: Reverts are currently irreversible

### Real-time Awareness

Cascade is aware of your real-time actions - no need to re-prompt context. Just say "Continue".

### Simultaneous Cascades

Multiple Cascades can run simultaneously. Navigate via dropdown (top left of panel).
**Warning**: If two Cascades edit same file simultaneously, edits can race and fail.

### @-Mentions

- `@file` - Reference specific files
- `@skill-name` - Invoke a skill
- `@web` / `@docs` - Web/docs search
- `@terminal` - Reference terminal output
- `@conversation` - Reference previous conversations (retrieves relevant parts)

### Sharing Conversations

Teams/Enterprise only: Click `...` > "Share Conversation" to share trajectories with team.

### Auto Execution Policies

- **Disabled** - All commands require manual approval
- **Allowlist** - Only allowlisted commands auto-execute (`windsurf.cascadeCommandsAllowList`)
- **Auto** - Model decides if safe (premium models only)
- **Turbo** - All commands auto-execute except denylist (`windsurf.cascadeCommandsDenyList`)

### Auto-Continue

When enabled, Cascade automatically continues when hitting per-response limit. Each continue consumes credits.

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

**Pre-hooks can block actions** by exiting with code 2.

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
- **Global**: `~/.codeium/windsurf/skills/<skill-name>/SKILL.md`

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
