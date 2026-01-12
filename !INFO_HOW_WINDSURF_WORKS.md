# How Windsurf Works

## Table of Contents

1. [Overview](#overview)
2. [Directory Structure](#directory-structure)
3. [Settings Storage](#settings-storage)
4. [Cascade AI Assistant](#cascade-ai-assistant)
5. [Workflows and Rules](#workflows-and-rules)
6. [Key Files Reference](#key-files-reference)

## Overview

Windsurf is an AI-powered IDE based on VS Code, developed by Codeium. It includes Cascade, an agentic AI coding assistant that can read, write, and execute code.

## Directory Structure

```
C:\Users\<User>\
├── .codeium\
│   └── windsurf\
│       ├── user_settings.pb      # Cascade UI settings (protobuf binary)
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

### Capabilities

- **Read files** - View source code in workspace
- **Write/Edit files** - Create and modify code
- **Run terminal commands** - Execute shell commands
- **Web search** - Search documentation and web
- **MCP integration** - Connect to external tools via Model Context Protocol
- **Tool calling** - Up to 20-25 tool calls per prompt

### Auto Execution Policies

- **Disabled** - All terminal commands require manual approval
- **Allowlist** - Only allowlisted commands are auto-executed
- **Auto** - Model decides if command is safe (premium models only)
- **Turbo** - All commands auto-executed (except denylist)

### Auto-Continue

When enabled, Cascade automatically continues its response when hitting the per-response invocation limit. Each continue consumes additional credits.

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

Project-specific instructions for Cascade stored in:
- `.windsurf/rules/` - Workspace rules
- Global rules via Windsurf Settings panel

### Memories

Persistent context Cascade remembers across conversations:
- Auto-generated (if enabled)
- User-created via "remember this" commands

## Key Files Reference

- `settings.json` - Editor preferences (JSON, editable)
- `keybindings.json` - Keyboard shortcuts
- `user_settings.pb` - Cascade UI settings (protobuf, UI-only)
- `state.vscdb` - Window/extension state (SQLite)
- `mcp_config.json` - MCP server configurations
- `.codeiumignore` - Files Cascade should ignore
- `.windsurf/workflows/*.md` - Custom workflows
- `.windsurf/rules/*.md` - Project rules for Cascade

## Sources

- Windsurf Documentation: https://docs.windsurf.com/
- Windsurf Changelog: https://windsurf.com/changelog
- Local file system investigation (2026-01-11)
