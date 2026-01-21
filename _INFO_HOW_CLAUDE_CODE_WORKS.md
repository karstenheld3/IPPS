# INFO: How Claude Code Works

**Doc ID**: CLCD-IN01
**Goal**: Document Claude Code features, configuration, and integration for cross-agent compatibility reference

## Summary

Key findings for cross-agent compatibility:
- Claude Code uses `CLAUDE.md` for instructions (equivalent to Windsurf rules) [VERIFIED]
- Commands stored in `.claude/commands/*.md`, invoked as `/command-name` [VERIFIED]
- Skills in `.claude/skills/<name>/SKILL.md` with same SKILL.md format as Windsurf [VERIFIED]
- Subagents (`.claude/agents/`) are unique to Claude Code - no Windsurf equivalent [VERIFIED]
- MCP config in `.mcp.json` (project) or `~/.claude.json` (user) [VERIFIED]
- Hooks configured in `settings.json`, similar events to Windsurf hooks [VERIFIED]

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Directory Structure](#directory-structure)
4. [Settings and Configuration](#settings-and-configuration)
5. [AI Assistant Features](#ai-assistant-features)
6. [Memory and Instructions](#memory-and-instructions)
7. [Commands and Workflows](#commands-and-workflows)
8. [Skills](#skills)
9. [Subagents](#subagents)
10. [Hooks](#hooks)
11. [MCP Integration](#mcp-integration)
12. [Plugins](#plugins)
13. [Terminal and CLI](#terminal-and-cli)
14. [Key Files Reference](#key-files-reference)
15. [Sources](#sources)

## Overview

Claude Code is Anthropic's agentic coding tool that lives in your terminal. It helps developers build features from descriptions, debug issues, navigate codebases, and automate tasks.

**Key characteristics:**
- Terminal-based (not an IDE or chat window)
- Can read/write files, run commands, create commits
- Supports Model Context Protocol (MCP) for external tool integration
- Enterprise-ready with API, AWS, or GCP hosting options

## Installation

**Native Install (Recommended):**
```bash
# macOS/Linux
curl -fsSL https://claude.ai/install.sh | bash

# Windows PowerShell
irm https://claude.ai/install.ps1 | iex

# Windows CMD
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

**Package Managers:**
```bash
# Homebrew (macOS)
brew install --cask claude-code

# WinGet (Windows)
winget install Anthropic.ClaudeCode
```

**Requirements:** Claude subscription (Pro, Max, Teams, or Enterprise) or Claude Console account.

## Directory Structure

```
~/.claude/                        # User config directory
├── CLAUDE.md                     # Global instructions (all projects)
├── settings.json                 # User settings
├── agents/                       # User subagents
│   └── my-agent.md
├── commands/                     # User slash commands
│   └── my-command.md
├── rules/                        # User-level rules
│   └── preferences.md
└── skills/                       # User skills
    └── my-skill/
        └── SKILL.md

~/.claude.json                    # Preferences, OAuth, MCP servers, caches

your-project/
├── CLAUDE.md                     # Project instructions (checked in)
├── CLAUDE.local.md               # Local instructions (gitignored)
├── .claude/
│   ├── CLAUDE.md                 # Alternative project instructions location
│   ├── settings.json             # Project settings (checked in)
│   ├── settings.local.json       # Local settings (gitignored)
│   ├── agents/                   # Project subagents
│   ├── commands/                 # Project slash commands
│   └── rules/                    # Project rules
│       ├── code-style.md
│       └── testing.md
└── .mcp.json                     # Project MCP servers (checked in)
```

**Managed Settings (IT/Admin deployed):**
- macOS: `/Library/Application Support/ClaudeCode/`
- Linux/WSL: `/etc/claude-code/`
- Windows: `C:\Program Files\ClaudeCode\`

## Settings and Configuration

### Configuration Scopes

Scopes listed from highest to lowest precedence:

1. **Managed** - Organization-wide, cannot be overridden
2. **Command line** - Temporary session overrides
3. **Local** - `.claude/settings.local.json` (personal, not committed)
4. **Project** - `.claude/settings.json` (team-shared)
5. **User** - `~/.claude/settings.json` (personal defaults)

### Settings File (settings.json)

```json
{
  "permissions": {
    "allow": ["Bash(npm run lint)", "Bash(npm run test:*)"],
    "deny": ["Bash(curl:*)", "Read(./.env)", "Read(./secrets/**)"]
  },
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1"
  },
  "hooks": {
    "PreToolUse": {"Bash": "echo 'Running command...'"}
  },
  "model": "claude-sonnet-4-5-20250929"
}
```

**Key settings:**
- **permissions** - Allow/deny rules for tools
- **env** - Environment variables
- **hooks** - Lifecycle hooks configuration
- **model** - Default model to use
- **attribution** - Commit/PR attribution text
- **includeCoAuthoredBy** - Add co-authored-by to commits
- **respectGitignore** - Honor .gitignore for @ suggestions

### Environment Variables

- `ANTHROPIC_API_KEY` - API key for authentication
- `CLAUDE_CODE_USE_BEDROCK` - Use Amazon Bedrock
- `CLAUDE_CODE_USE_VERTEX` - Use Google Vertex AI
- `BASH_DEFAULT_TIMEOUT_MS` - Default bash timeout
- `DISABLE_TELEMETRY` - Disable telemetry
- `DISABLE_AUTOUPDATER` - Disable auto-updates
- `HTTP_PROXY` / `HTTPS_PROXY` - Proxy configuration

## AI Assistant Features

### Capabilities

- **Read/Write files** - View and modify source code
- **Run terminal commands** - Execute shell commands with permission controls
- **Web search** - Fetch information from the web
- **MCP integration** - Connect to external tools (GitHub, databases, APIs)
- **Extended thinking** - Deep reasoning for complex problems
- **Background tasks** - Run operations in background

### Input Modes

- **Normal** - Standard text input
- **Multiline** - Use `\` at end of line, or `Shift+Enter`
- **Vim mode** - Enable with `/vim` command
- **Bash mode** - Prefix with `!` to run shell commands directly

### Prompt Syntax (Agentic Language Enrichments)

Claude Code supports several input enrichments for precise control:

**@mentions** - Reference context:
- `@file` or `@path/to/file` - Reference specific files
- `@folder/` - Reference entire directories
- Files in prompts via `@README` syntax in CLAUDE.md

**/commands** - Invoke automation:
- `/command-name` - Run command from `.claude/commands/`
- Built-in: `/memory`, `/init`, `/clear`, `/compact`, `/resume`, etc.
- Custom commands support `$ARGUMENTS`, `$1`, `$2` placeholders

**!bang** - Direct shell execution:
- `!command` - Execute bash command directly without AI interpretation

**#hashtag** - Memory shortcut:
- `#` key - Add instruction to CLAUDE.md during conversation

**Other enrichments:**
- **Pipe input** - `cat file.txt | claude -p "explain"` includes file content
- **Multiline** - Use `\` at end of line or `Shift+Enter`
- **Image attachments** - Supported via CLI flags

### Keyboard Shortcuts

- `Ctrl+C` - Cancel current operation
- `Ctrl+D` - Exit Claude Code
- `Ctrl+L` - Clear screen
- `Ctrl+R` - Reverse search history
- `Esc` - Cancel current input / interrupt
- `/` - Open slash commands menu
- `@` - Reference files
- `!` - Execute bash command directly

### Permission Modes

- **default** - Ask for permission on sensitive operations
- **acceptEdits** - Auto-accept file edits, ask for other operations
- **dontAsk** - Auto-accept most operations
- **bypassPermissions** - Skip all permission checks (dangerous)
- **plan** - Read-only planning mode

## Memory and Instructions

### CLAUDE.md Files

Claude automatically loads CLAUDE.md files at conversation start. Use for:
- Frequently used commands (build, test, lint)
- Code style preferences and naming conventions
- Architectural patterns
- Developer environment setup

**Locations (in priority order):**
1. Managed: `/Library/Application Support/ClaudeCode/CLAUDE.md` (system-wide)
2. Project: `./CLAUDE.md` or `./.claude/CLAUDE.md`
3. User: `~/.claude/CLAUDE.md`
4. Local: `./CLAUDE.local.md` (gitignored)

**Imports in CLAUDE.md:**
```markdown
See @README for project overview and @package.json for npm commands.

# Additional Instructions
- git workflow @docs/git-instructions.md
```

### Modular Rules (.claude/rules/)

Organize instructions into focused files:

```
.claude/rules/
├── code-style.md      # Code style guidelines
├── testing.md         # Testing conventions
├── security.md        # Security requirements
└── frontend/
    └── react.md       # React-specific rules
```

**Path-specific rules with frontmatter:**
```yaml
---
paths:
  - "src/api/**/*.ts"
---

# API Development Rules
- All API endpoints must include input validation
- Use the standard error response format
```

### Memory Commands

- `/memory` - Open memory editor
- `/init` - Generate initial CLAUDE.md for project
- `#` key - Add instruction to CLAUDE.md during conversation

## Commands and Workflows

### Built-in Slash Commands

- `/add-dir` - Add directory to context
- `/agents` - Manage subagents
- `/clear` - Clear conversation context
- `/compact [instructions]` - Compact context with optional focus
- `/config` - Open configuration
- `/context` - Show current context
- `/cost` - Show session cost
- `/doctor` - Diagnose issues
- `/exit` - Exit Claude Code
- `/export [filename]` - Export conversation
- `/help` - Show available commands
- `/hooks` - Manage hooks
- `/init` - Initialize CLAUDE.md
- `/login` / `/logout` - Authentication
- `/mcp` - Manage MCP servers
- `/memory` - Edit memory files
- `/model` - Change model
- `/permissions` - View/edit permissions
- `/plan` - Enter planning mode
- `/resume [session]` - Resume previous session
- `/review` - Code review
- `/rewind` - Rewind to checkpoint

### Custom Slash Commands

Store prompt templates in `.claude/commands/` (project) or `~/.claude/commands/` (user).

**Example:** `.claude/commands/fix-issue.md`
```markdown
---
allowed-tools: Bash(git:*), Read, Edit
description: Fix a GitHub issue
---

Fix issue #$ARGUMENTS following our coding standards:
1. Understand the problem
2. Search for relevant files
3. Implement the fix
4. Write tests
5. Create a commit
```

**Invocation:** `/fix-issue 123`

**Features:**
- `$ARGUMENTS` - All arguments as string
- `$1`, `$2`, etc. - Individual arguments
- `!`backtick`` - Execute bash and include output
- `@file` - Reference files

## Skills

Skills bundle complex multi-step tasks with supporting resources.

**Based on:** Agent Skills open format (https://agentskills.io/)

### Skill Locations

- **User:** `~/.claude/skills/<skill-name>/SKILL.md`
- **Project:** `.claude/skills/<skill-name>/SKILL.md`

### SKILL.md Format

```yaml
---
name: deploy-to-production
description: Guides deployment with safety checks
---

## Pre-deployment Checklist
1. Run all tests
2. Check for uncommitted changes
...
```

### Skills vs Slash Commands

- **Skills** - Complex tasks with supporting files, auto-invoked based on description
- **Slash commands** - Simple prompt templates, explicitly invoked with `/command`

## Subagents

Subagents are specialized AI assistants that run in isolated contexts.

### Built-in Subagents

- **Explore** - Fast file discovery (Haiku model, read-only)
- **Plan** - Codebase research for planning (inherited model, read-only)
- **General-purpose** - Complex research and modifications (inherited model, all tools)

### Subagent Configuration

**Locations:**
- User: `~/.claude/agents/`
- Project: `.claude/agents/`

**Example:** `.claude/agents/code-reviewer.md`
```yaml
---
name: code-reviewer
description: Reviews code for quality and best practices
tools: Read, Glob, Grep
model: sonnet
permissionMode: default
---

You are a code reviewer. Analyze code and provide specific, actionable feedback on quality, security, and best practices.
```

**Frontmatter fields:**
- `name` - Subagent name
- `description` - When to invoke (used for auto-delegation)
- `tools` - Allowed tools (comma-separated)
- `disallowedTools` - Denied tools
- `model` - `sonnet`, `opus`, `haiku`, or `inherit`
- `permissionMode` - `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan`
- `skills` - Skills to include
- `hooks` - Lifecycle hooks

### Subagent Commands

- `/agents` - View, create, edit, delete subagents
- CLI: `claude --agents '{...}'` - Define inline subagents

## Hooks

Hooks execute custom code at key points in Claude's workflow.

### Hook Events

- **PreToolUse** - Before a tool runs (can block)
- **PostToolUse** - After a tool runs
- **PermissionRequest** - When permission is requested
- **Notification** - On notifications
- **UserPromptSubmit** - When user submits prompt
- **Stop** - When conversation stops
- **SubagentStop** - When subagent stops
- **PreCompact** - Before context compaction
- **SessionStart** - When session starts
- **SessionEnd** - When session ends

### Hook Configuration

In `settings.json`:
```json
{
  "hooks": {
    "PreToolUse": {
      "Bash": "echo 'Running: $TOOL_INPUT'"
    },
    "PostToolUse": {
      "Edit": "/path/to/formatter.sh"
    }
  }
}
```

### Hook Output

- **Exit code 0** - Success, continue
- **Exit code 2** - Block the action
- **JSON output** - Advanced control (modify inputs, add messages)

## MCP Integration

Model Context Protocol enables Claude to access custom tools and services.

### MCP Scopes

- **Local** - `~/.claude.json` (personal, one project)
- **User** - `~/.claude.json` mcpServers field (personal, all projects)
- **Project** - `.mcp.json` (team-shared)
- **Managed** - `managed-mcp.json` (IT-deployed)

### Adding MCP Servers

```bash
# HTTP server
claude mcp add --transport http stripe https://mcp.stripe.com

# Project-scoped
claude mcp add --transport http github --scope project https://mcp.github.com

# User-scoped
claude mcp add --transport http slack --scope user https://mcp.slack.com
```

### .mcp.json Format

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

**Environment variable expansion:**
- `${VAR}` - Expands to VAR value
- `${VAR:-default}` - Uses default if VAR not set

### MCP Commands

- `/mcp` - Manage MCP servers
- `claude mcp add` - Add server
- `claude mcp remove` - Remove server
- `claude mcp reset-project-choices` - Reset project MCP choices

## Plugins

Plugins extend Claude Code with additional functionality.

### Plugin Locations

- User: `~/.claude/plugins/`
- Project: `.claude/plugins/`

### Plugin Features

- Custom tools
- Slash commands
- MCP servers
- Subagents

### Plugin Commands

- `/plugin` - Manage plugins
- Marketplace discovery via settings

## Terminal and CLI

### CLI Commands

```bash
# Start interactive session
claude

# Start with initial prompt
claude "explain this project"

# Print mode (non-interactive)
claude -p "explain this function"

# Pipe input
cat logs.txt | claude -p "explain errors"

# Continue last session
claude -c

# Resume named session
claude -r "auth-refactor" "Continue this work"

# Update Claude Code
claude update
```

### CLI Flags

- `-p, --print` - Print mode (non-interactive)
- `-c, --continue` - Continue last session
- `-r, --resume <session>` - Resume named session
- `--model <model>` - Use specific model (`sonnet`, `opus`)
- `--agent <name>` - Use specific subagent
- `--dangerously-skip-permissions` - Skip all permission checks
- `--add-dir <paths>` - Add directories to context
- `--mcp-config <file>` - Use specific MCP config
- `--output-format <format>` - Output format (`text`, `json`, `stream-json`)

### Print Mode Features

Print mode (`-p`) enables scripting and automation:
```bash
# Analyze logs
tail -f app.log | claude -p "Alert if errors appear"

# CI integration
claude -p "Translate new strings to French and create PR"

# Structured output
claude -p --output-format json "List all TODO comments"
```

## Key Files Reference

**User Config:**
- `~/.claude/CLAUDE.md` - Global instructions
- `~/.claude/settings.json` - User settings
- `~/.claude/agents/` - User subagents
- `~/.claude/commands/` - User slash commands
- `~/.claude/rules/` - User rules
- `~/.claude.json` - Preferences, OAuth, MCP servers

**Project Config:**
- `CLAUDE.md` - Project instructions (checked in)
- `CLAUDE.local.md` - Local instructions (gitignored)
- `.claude/settings.json` - Project settings (checked in)
- `.claude/settings.local.json` - Local settings (gitignored)
- `.claude/agents/` - Project subagents
- `.claude/commands/` - Project slash commands
- `.claude/rules/` - Project rules with optional path patterns
- `.mcp.json` - Project MCP servers

**Managed (IT-deployed):**
- `managed-settings.json` - Enforced settings
- `managed-mcp.json` - Enforced MCP servers
- `CLAUDE.md` - Organization-wide instructions

## Sources

**Official Documentation:** [VERIFIED 2026-01-15]
- https://code.claude.com/docs/en/overview - Overview and quickstart
- https://code.claude.com/docs/en/settings - Settings and configuration
- https://code.claude.com/docs/en/memory - Memory and CLAUDE.md
- https://code.claude.com/docs/en/slash-commands - Slash commands
- https://code.claude.com/docs/en/skills - Agent Skills
- https://code.claude.com/docs/en/sub-agents - Subagents
- https://code.claude.com/docs/en/hooks - Hooks reference
- https://code.claude.com/docs/en/mcp - MCP integration
- https://code.claude.com/docs/en/cli-reference - CLI reference
- https://code.claude.com/docs/en/interactive-mode - Interactive mode

**Best Practices:**
- https://www.anthropic.com/engineering/claude-code-best-practices

## Document History

**[2026-01-15 08:35]**
- Initial document created from official Claude Code documentation
- Researched: overview, settings, memory, commands, skills, subagents, hooks, MCP, CLI
- Sources verified against code.claude.com/docs
