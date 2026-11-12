# INFO: How OpenAI Codex CLI Works

**Doc ID**: CODX-IN01
**Goal**: Document OpenAI Codex CLI features, configuration, and sandbox security for cross-agent compatibility reference

## Summary

Key findings for cross-agent compatibility:
- Codex uses `AGENTS.md` for instructions (hierarchical, directory-scoped) [VERIFIED]
- `AGENTS.override.md` takes precedence over `AGENTS.md` in same directory [VERIFIED]
- **Skills fully supported** - `.agents/skills/<name>/SKILL.md` format (vendor-neutral path) [VERIFIED 2026-07]
- Custom prompts (`~/.codex/prompts/`) deprecated and **removed in v0.117.0** (March 2026) [VERIFIED 2026-07]
- Invocation: `$skill-name` (explicit), `/skills` (picker), or implicit (model decides based on description) [VERIFIED 2026-07]
- Progressive disclosure: name+description at startup, full SKILL.md on invocation, references on demand [VERIFIED 2026-07]
- No hooks system - use `requirements.toml` for managed policy enforcement [VERIFIED]
- Configuration in `~/.codex/config.toml` (TOML format, not JSON) [VERIFIED]
- MCP servers configured in `config.toml` under `[mcp_servers.<id>]` [VERIFIED]
- OS-level sandbox: Seatbelt (macOS), Landlock+seccomp (Linux) [VERIFIED]
- Subagents supported via `/agent` and `/subagents` commands [VERIFIED 2026-07]

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
12. [Terminal and CLI](#terminal-and-cli)
13. [Key Files Reference](#key-files-reference)
14. [Sources](#sources)

## Overview

Codex CLI is OpenAI's coding agent that runs locally from your terminal. It can read, change, and run code on your machine in the selected directory.

**Key characteristics:**
- Open source, built in Rust for speed and efficiency
- Terminal-based with full-screen TUI (Terminal UI)
- Can read files, make edits, and run commands
- Supports MCP for external tool integration
- OS-level sandboxing for security

**Requirements:** ChatGPT Plus, Pro, Business, Edu, or Enterprise plan, or API key.

## Installation

**npm (Recommended):**
```bash
npm i -g @openai/codex
```

**Upgrade:**
```bash
npm i -g @openai/codex@latest
```

**Platform Support:**
- macOS: Full support
- Linux: Full support
- Windows: Experimental (WSL recommended)

## Directory Structure

```
~/.codex/                         # Codex home directory (or CODEX_HOME)
├── config.toml                   # Main configuration file
├── AGENTS.md                     # Global instructions
├── AGENTS.override.md            # Global override (takes precedence)
├── sessions/                     # Session transcripts
├── log/
│   └── codex-tui.log            # TUI logs
└── prompts/                      # Custom prompts (if configured)

your-project/
├── AGENTS.md                     # Project instructions
├── AGENTS.override.md            # Project override (takes precedence)
└── services/
    └── payments/
        └── AGENTS.override.md    # Directory-specific override
```

**Managed Configuration (IT/Admin):**
- Linux/macOS: `/etc/codex/requirements.toml`, `/etc/codex/managed_config.toml`
- Windows: `~/.codex/managed_config.toml`
- macOS MDM: Preference domain `com.openai.codex`

## Settings and Configuration

### Configuration File

Codex stores configuration in `~/.codex/config.toml`.

### Configuration Precedence

1. CLI flags (highest)
2. Profile values (`--profile <name>`)
3. Root-level values in `config.toml`
4. Built-in defaults (lowest)

### Common Configuration Options

```toml
# Default model
model = "gpt-5-codex"

# Approval policy: untrusted | on-failure | on-request | never
approval_policy = "on-request"

# Sandbox mode: read-only | workspace-write | danger-full-access
sandbox_mode = "workspace-write"

# Reasoning effort: minimal | low | medium | high | xhigh
model_reasoning_effort = "high"

# Environment policy
[shell_environment_policy]
include_only = ["PATH", "HOME"]

# Feature flags
[features]
web_search_request = true
shell_snapshot = true
```

### Feature Flags

Enable in `config.toml` under `[features]` or via CLI:
```bash
codex --enable web_search_request
```

**Available features:**
- `web_search_request` - Allow web searches
- `shell_snapshot` - Speed up repeated commands
- `unified_exec` - PTY-backed exec tool
- `apply_patch_freeform` - Freeform patch tool

### Profiles

Save presets as profiles for quick switching:
```toml
[profiles.full_auto]
approval_policy = "on-request"
sandbox_mode = "workspace-write"

[profiles.readonly_quiet]
approval_policy = "never"
sandbox_mode = "read-only"
```

Use with: `codex --profile full_auto`

## AI Assistant Features

### Capabilities

- **Read/Write files** - View and modify source code
- **Run terminal commands** - Execute shell commands in sandbox
- **Image inputs** - Attach screenshots or design specs
- **Web search** - Search the web (opt-in)
- **Code review** - Review diffs before commit
- **Codex Cloud** - Run tasks in OpenAI-managed containers

### Approval Modes

Control when Codex asks before acting:

- **Auto** (default) - Read, edit, run in workspace; ask for outside access
- **Read-only** - Browse files only, ask before changes
- **Full Access** - Work across machine including network (use sparingly)

Change mid-session with `/approvals` command.

### Sandbox Modes

Control what Codex can technically do:

- **read-only** - No writes, no command execution
- **workspace-write** - Write within workspace only
- **danger-full-access** - Full machine access (dangerous)

```bash
codex --sandbox workspace-write --ask-for-approval on-request
```

### Network Access

Network is off by default in workspace-write mode. Enable in config:
```toml
[sandbox_workspace_write]
network_access = true
```

Or enable web search only:
```toml
[features]
web_search_request = true
```

### OS-Level Sandbox

- **macOS** - Seatbelt policies via `sandbox-exec`
- **Linux** - Landlock + seccomp
- **Windows** - WSL recommended; native sandbox is experimental

## Memory and Instructions

### AGENTS.md Files

Codex reads `AGENTS.md` files to get project-specific instructions.

**Discovery order:**
1. **Global:** `~/.codex/AGENTS.override.md` or `~/.codex/AGENTS.md`
2. **Project:** Walk from git root to current directory, reading `AGENTS.override.md` or `AGENTS.md` in each directory
3. **Merge:** Concatenate all files; later files override earlier ones

**Size limit:** 32 KiB combined (configurable via `project_doc_max_bytes`)

### Creating Global Instructions

```bash
mkdir -p ~/.codex
cat > ~/.codex/AGENTS.md << 'EOF'
## Working agreements
- Always run `npm test` after modifying JavaScript files.
- Prefer `pnpm` when installing dependencies.
- Ask for confirmation before adding new production dependencies.
EOF
```

### Project Instructions

Create `AGENTS.md` in repository root:
```markdown
# AGENTS.md

## Repository expectations
- Run `npm run lint` before opening a pull request.
- Document public utilities in `docs/` when you change behavior.
```

### Directory-Specific Overrides

Create `AGENTS.override.md` in subdirectory to override parent instructions:
```markdown
# services/payments/AGENTS.override.md

## Payments service rules
- Use `make test-payments` instead of `npm test`.
- Never rotate API keys without notifying the security channel.
```

### Fallback Filenames

Configure alternative instruction filenames:
```toml
project_doc_fallback_filenames = ["TEAM_GUIDE.md", "CODEX_INSTRUCTIONS.md"]
```

### Generate with /init

Run `/init` in a directory to have Codex generate an `AGENTS.md` scaffold.

## Commands and Workflows

### Built-in Slash Commands

- `/approvals` - Update approval rules
- `/compact` - Summarize and compress conversation
- `/diff` - Show git diff
- `/exit` / `/quit` - Exit CLI
- `/feedback` - Send feedback
- `/fork` - Branch a saved conversation
- `/init` - Generate AGENTS.md
- `/logout` - Sign out
- `/mcp` - List MCP tools
- `/mention` - Highlight files
- `/model` - Switch model
- `/new` - Start new conversation
- `/resume` - Resume saved conversation
- `/review` - Ask for code review
- `/status` - Show session status

### Custom Prompts (REMOVED in v0.117.0)

Custom prompts (`~/.codex/prompts/`) were **deprecated and removed** in Codex CLI v0.117.0 (March 2026). OpenAI's stated rationale:

> "It doesn't make sense to provide two overlapping features and mechanisms that do the same thing. The industry has rallied behind skills as a standard."

All feature requests to restore commands were rejected (GitHub issues #15941, #18857, #22674). Users are directed to convert prompts to skills. Codex can perform the conversion automatically.

**Migration:** `~/.codex/prompts/commit.md` → `~/.agents/skills/commit/SKILL.md` [VERIFIED 2026-07]

## Skills

Skills are fully supported as of late 2025 (experimental) and stable since mid-2026. Codex follows the open Agent Skills standard (https://agentskills.io/). [VERIFIED 2026-07]

### Skills-Commands Merge (v0.117.0, March 2026)

Codex previously had "custom prompts" in `~/.codex/prompts/` (their equivalent of commands). These were **deprecated and removed** in v0.117.0. OpenAI explicitly rejected all requests to restore them:

> "We previously supported custom slash commands but removed the support in favor of skills, which provide a superset of the functionality." (GitHub issue #22674)

**Why OpenAI merged them:**
1. **Implementation parity** - Both were markdown files injected as context. Two systems for identical mechanics.
2. **Skills are a strict superset** - Add: progressive disclosure (3-level context loading), supporting files (scripts, references, templates), implicit invocation by model, plugins distribution.
3. **Industry standard** - "The industry has rallied behind skills as a standard." OpenAI adopted the vendor-neutral `.agents/skills/` path so skills can be shared across tools.

**What was lost:**
- Custom prompts had zero context cost when not invoked. Skills always inject name+description at startup (budget: 2% of context window or 8,000 chars).
- Custom prompts were never auto-invoked. Skills can be (unless `allow_implicit_invocation: false`).
- Deterministic local execution (no model invocation) is gone. Feature request #18857 explicitly rejected.

### Skill Locations

| Scope | Path | Use |
|-------|------|-----|
| Repo (nearest) | `$CWD/.agents/skills/` | Module-specific workflows |
| Repo (parent) | `../.agents/skills/` | Nested project layouts |
| Repo (root) | `$REPO_ROOT/.agents/skills/` | Team-shared skills |
| User | `~/.agents/skills/` | Personal skills across all projects |
| Admin | `/etc/codex/skills/` | System-wide managed skills |
| Plugins | Plugin directories | Distributed via plugin system |

**Legacy paths (still scanned):** `~/.codex/skills/`, `.codex/skills/`

**Vendor-neutral design:** OpenAI chose `~/.agents/skills/` (not `~/.codex/skills/`) so one folder on disk serves multiple tools. Symlink from `~/.claude/skills/` and both products read the same skills. [VERIFIED 2026-07]

### SKILL.md Format

```yaml
---
name: deploy-staging
description: Deploy current branch to staging. Use when user says "deploy to staging" or "push to stage".
---

## Steps
1. Run tests: `npm run test`
2. Build: `npm run build`
3. Deploy: `./scripts/deploy-staging.sh`
4. Verify health check
```

**Required frontmatter:** `name`, `description` (both mandatory)

**Optional metadata (`agents/openai.yaml`):**
```yaml
interface:
  display_name: "Deploy to Staging"
  short_description: "Deploy current branch"

policy:
  allow_implicit_invocation: false    # Equivalent to disable-model-invocation

dependencies:
  tools:
    - type: "mcp"
      value: "github"
      transport: "streamable_http"
      url: "https://mcp.github.com"
```

### Skill Invocation

Two modes:

1. **Explicit** - `$skill-name` in prompt, or `/skills` picker in TUI
2. **Implicit** - Model matches task to skill `description` and loads it automatically

Control implicit invocation:
- `agents/openai.yaml` → `policy.allow_implicit_invocation: false` (per-skill)
- `[[skills.config]]` in `config.toml` → `enabled = false` (disable entirely)

### Progressive Disclosure (3-Level Context Loading)

- **Level 1 (startup):** Name + description + file path injected into system prompt. Budget: max 2% of context window or 8,000 chars.
- **Level 2 (invocation):** Full `SKILL.md` body loaded when skill is selected.
- **Level 3 (on-demand):** Supporting files (`scripts/`, `references/`, `templates/`) read by model only when needed.

### Skill Directory Structure

```
skill-name/
├── SKILL.md              (required - instructions)
├── agents/
│   └── openai.yaml       (optional - UI metadata, invocation policy)
├── scripts/              (optional - CLI scripts Codex can invoke)
├── references/           (optional - reference docs loaded on demand)
└── templates/            (optional - file templates)
```

### Feature Flag (Legacy)

Skills were behind a feature flag in early versions:
```toml
[features]
skills = true
```
No longer required as of mid-2026 (skills enabled by default). [VERIFIED 2026-07]

### Sources

- https://developers.openai.com/codex/skills
- https://github.com/openai/codex/issues/15941 (custom prompts removal)
- https://github.com/openai/codex/issues/18857 (slash commands rejected)
- https://github.com/openai/codex/issues/22674 (commands rejected again)
- https://deepwiki.com/openai/codex/5.9-skills-system

## Subagents

Codex now supports subagents (multi-agent mode). [VERIFIED 2026-07]

- `/agent` and `/subagents` commands to switch between agent threads
- Built-in code review runs as a separate agent via `/review` command
- Feature flag: `multi_agent = true` in `config.toml`
- Subagent threads run in isolated contexts with their own tool permissions

**Note:** Full subagent documentation pending. Current evidence from GitHub issues and slash commands reference.

## Hooks

**Not supported natively.** Codex does not have a hooks system like Windsurf or Claude Code.

For managed deployments, use `requirements.toml` and `managed_config.toml` to enforce policies.

## MCP Integration

Codex supports Model Context Protocol for external tools.

### Supported Features

- **STDIO servers** - Local processes started by command
- **Streamable HTTP servers** - Remote servers accessed by URL
- **Authentication** - Bearer token, OAuth

### Adding MCP Servers

**Via CLI:**
```bash
codex mcp add context7 -- npx -y @upstash/context7-mcp
codex mcp add figma --url https://mcp.figma.com/mcp
```

**Via config.toml:**
```toml
[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp"]

[mcp_servers.figma]
url = "https://mcp.figma.com/mcp"
bearer_token_env_var = "FIGMA_OAUTH_TOKEN"
```

### MCP Configuration Options

- `command` - Launcher command (STDIO)
- `args` - Command arguments
- `env` - Environment variables
- `url` - Server address (HTTP)
- `bearer_token_env_var` - Auth token env var
- `enabled_tools` - Tool allow list
- `disabled_tools` - Tool deny list
- `startup_timeout_sec` - Startup timeout (default: 10)
- `tool_timeout_sec` - Tool timeout (default: 60)

### MCP Commands

- `/mcp` - List active MCP servers in TUI
- `codex mcp add` - Add server
- `codex mcp login <server>` - OAuth login
- `codex mcp --help` - Show all MCP commands

## Terminal and CLI

### Interactive Mode

```bash
# Start interactive TUI
codex

# Start with initial prompt
codex "Explain this codebase to me"
```

### Non-Interactive Mode (exec)

```bash
# Run single task
codex exec "fix the CI failure"

# With JSON output
codex exec --json "analyze this code"
```

### Session Management

```bash
# Resume picker
codex resume

# Resume last session
codex resume --last

# Resume specific session
codex resume <SESSION_ID>

# Resume all (across directories)
codex resume --all
```

### CLI Flags

- `--model <model>` - Specify model
- `--sandbox <mode>` - Set sandbox mode
- `--ask-for-approval <policy>` - Set approval policy
- `--full-auto` - Workspace write + on-request approvals
- `-a never` - Disable approval prompts
- `--search` - Enable web search
- `--cd <path>` - Set working directory
- `--add-dir <paths>` - Add writable directories
- `-i, --image <files>` - Attach images
- `--profile <name>` - Use config profile
- `--enable <feature>` - Enable feature flag
- `--yolo` / `--dangerously-bypass-approvals-and-sandbox` - Full access (dangerous)

### Prompt Syntax (Agentic Language Enrichments)

Codex CLI supports several input enrichments for precise control:

**@mentions** - Reference context:
- `@` - Opens fuzzy file search picker
- Type after `@` to filter files in workspace

**/commands** - Invoke automation:
- `/command` - Built-in slash commands (`/init`, `/compact`, `/diff`, `/review`, etc.)
- `/prompts: <name>` - Run custom prompt from prompts directory
- No custom slash command system like Claude Code

**!bang** - Direct shell execution:
- `!command` - Execute shell command directly in TUI

**Other enrichments:**
- **Image attachments** - `-i, --image <files>` CLI flag to attach images
- **Pipe input** - Pipe content to `codex exec` for processing
- **Web search** - Enable with `--search` flag or `web_search_request` feature

**Not supported:**
- No `#hashtag` syntax
- No URL pasting (use web search feature instead)
- No @skill invocation (no skills system)

### Shortcuts in TUI

- `@` - Fuzzy file search
- `!` - Run local shell command
- `Esc Esc` - Edit previous message
- `Ctrl+G` - Open external editor for prompt
- `Ctrl+C` - Cancel current operation

### Shell Completions

```bash
# Install completions
codex completion bash
codex completion zsh
codex completion fish

# Add to ~/.zshrc
eval "$(codex completion zsh)"
```

## Key Files Reference

**User Config:**
- `~/.codex/config.toml` - Main configuration
- `~/.codex/AGENTS.md` - Global instructions
- `~/.codex/AGENTS.override.md` - Global override
- `~/.agents/skills/` - User skills (vendor-neutral, shared across tools)
- `~/.codex/sessions/` - Session transcripts
- `~/.codex/log/` - Logs

**Project Config:**
- `AGENTS.md` - Project instructions (checked in)
- `AGENTS.override.md` - Project override
- `.agents/skills/` - Project skills (checked in)

**Managed (IT-deployed):**
- `/etc/codex/requirements.toml` - Enforced requirements
- `/etc/codex/managed_config.toml` - Managed defaults
- macOS MDM: `com.openai.codex` preference domain

## Sources

**Official Documentation:** [VERIFIED 2026-01-15]
- https://developers.openai.com/codex/cli - CLI overview
- https://developers.openai.com/codex/cli/features/ - Features reference
- https://developers.openai.com/codex/cli/reference/ - Command line options
- https://developers.openai.com/codex/config-basic/ - Basic configuration
- https://developers.openai.com/codex/config-reference/ - Configuration reference
- https://developers.openai.com/codex/security - Security and sandbox
- https://developers.openai.com/codex/mcp - MCP integration
- https://developers.openai.com/codex/guides/agents-md/ - AGENTS.md instructions
- https://developers.openai.com/codex/guides/slash-commands - Slash commands

**Skills and Commands (2026-07):**
- https://developers.openai.com/codex/skills - Skills documentation
- https://github.com/openai/codex/issues/15941 - Custom prompts removed (v0.117.0)
- https://github.com/openai/codex/issues/18857 - Slash commands rejected
- https://github.com/openai/codex/issues/22674 - Commands from .agents/commands/ rejected
- https://deepwiki.com/openai/codex/5.9-skills-system - Skills system internals

**Other:**
- https://github.com/openai/codex - Open source repository
- https://agents.md/ - AGENTS.md specification

## Document History

**[2026-07-23 18:00]**
- Added: Full Skills section - locations, SKILL.md format, invocation modes, progressive disclosure, directory structure
- Added: Skills-Commands Merge subsection documenting v0.117.0 removal of custom prompts with OpenAI's explicit rationale
- Changed: Summary updated - skills now verified, custom prompts marked removed
- Changed: Custom Prompts section updated to "REMOVED in v0.117.0" with migration guidance
- Changed: Subagents section updated - now supported via /agent and /subagents commands
- Added: Key Files Reference updated with `.agents/skills/` paths
- Added: Sources section with skills-related GitHub issues
- Sources: developers.openai.com/codex/skills, GitHub issues #15941 #18857 #22674, deepwiki.com

**[2026-01-15 08:35]**
- Initial document created from official Codex CLI documentation
- Researched: overview, configuration, sandbox, AGENTS.md, MCP, CLI
- Sources verified against developers.openai.com/codex

