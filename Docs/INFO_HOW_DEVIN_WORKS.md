# INFO: How Devin Desktop Works

**Doc ID**: DVDT-IN01
**Goal**: Comprehensive reference for Devin Desktop (formerly Windsurf) - agent harnesses, AI models, customization, developer tools, enterprise controls, and architecture internals
**Version scope**: Devin Desktop (June 2026+) / Devin Local 2026.5.26+
**Timeline**: Created 2026-06-03, Updated 5 times (2026-06-03)

## Summary

**Rebrand (2026-06-02):**
- Windsurf renamed to Devin Desktop via standard over-the-air update [VERIFIED]
- Plans, pricing, extensions, keybindings, workflows, LSPs all backward-compatible [VERIFIED]
- Cognition (makers of Devin Cloud) acquired Codeium/Windsurf, unified under "Devin" brand [VERIFIED]
- Agent Command Center now the default surface (was secondary in Windsurf 2.0) [VERIFIED]

**Agent harnesses:**
- Devin Local: primary local agent (successor to Cascade), rewritten in Rust, 30% more token-efficient, subagents, OS-level sandboxing [VERIFIED]
- Cascade: legacy local agent, maintained through at least July 1, 2026. Full feature set (Memories, Workflows, Codemaps) [VERIFIED]
- Devin Cloud: autonomous cloud agent on dedicated VMs, in-editor PR review [VERIFIED]
- Devin CLI: Rust-based terminal agent, cross-platform, same harness as Devin Local [VERIFIED]
- Agent Client Protocol (ACP): open-source protocol, supports Codex, Claude Agent, OpenCode, Junie, Gemini CLI, custom agents [VERIFIED]
- Agent Command Center: Kanban-style management of all local and cloud agents [VERIFIED]
- Spaces: task grouping with shared context across agent sessions [VERIFIED]

**Devin Local specifics:**
- Permissions model: Deny/Ask/Allow (replaces Cascade auto-execution levels) [VERIFIED]
- Config: `.devin/config.json` for MCP and permissions [VERIFIED]
- Does NOT support: Workflows, Memories, Codemaps, Code Lenses, App Deploys, Conversation Sharing [VERIFIED]
- DOES support: Rules, AGENTS.md, Skills [VERIFIED]

**Cascade (legacy) specifics:**
- Three modes: Code, Plan, Ask. `megaplan` for advanced planning [VERIFIED]
- `.devin/rules/*.md` (or `.devin/rules/*.md`), 4 trigger modes: `always_on`, `model_decision`, `glob`, `manual` [VERIFIED]
- Workflows in `.devin/workflows/*.md` (or `.devin/workflows/`), invoked as `/workflow-name` [VERIFIED]
- Skills in `.devin/skills/<name>/SKILL.md` or `.devin/skills/` - ONLY mechanism working across both Cascade and Devin Local [VERIFIED]
- Memories auto-generated during conversation, workspace-scoped [VERIFIED]

**AI models:**
- SWE-1.6 (latest in-house model, optimized intelligence + UX), SWE-1.5 (free) [VERIFIED]
- Claude Opus 4.8 / 4.8 Fast Mode, Claude Opus 4.7 / 4.7 Fast Mode [VERIFIED]
- GPT-5.5, GPT-5.4 / 5.4 Mini [VERIFIED]
- Adaptive router: intelligent model selection balancing speed and capability [VERIFIED]
- Arena Mode: side-by-side model comparison with battle groups and leaderboards [VERIFIED]
- BYOK for Anthropic models [VERIFIED]

**Code completion and context:**
- Windsurf Tab: Autocomplete (fast) and Supercomplete (multi-line diff suggestions) [VERIFIED]
- Fast Context: SWE-grep models, 20x faster retrieval than traditional search [VERIFIED]
- DeepWiki: auto-indexes repos, generates architecture wikis [VERIFIED]
- Knowledge Base: shared Google Docs as team knowledge (Teams/Enterprise) [VERIFIED]
- Remote Indexing: index remote repositories without local clone [VERIFIED]

**Code review:**
- Devin Review: deep PR review with smart diff organization, bug detection, Autofix [VERIFIED]
- Quick Review: fast local review using SWE-check model (free) [VERIFIED]

**Pricing (as of June 2026):**
- Quota-based usage: daily and weekly token budgets [VERIFIED]
- Plans: Free, Pro ($15/mo), Max ($60/mo), Teams ($40/user/mo), Enterprise [ASSUMED prices]
- Enterprise: Agent Compute Units (ACUs) [VERIFIED]

**Enterprise:**
- RBAC, SSO/SCIM, FedRAMP, Analytics API [VERIFIED]
- Enterprise policies via GPO/MDM [VERIFIED]
- Sandbox enforcement, network enforcement, granular permissions (Devin Local) [VERIFIED]

**Configuration and paths:**
- `.devin/rules/` preferred (`.devin/rules/` fallback) [VERIFIED]
- `.devinrules` still read (no `.devinrules` equivalent) [VERIFIED]
- AGENTS.md / agents.md supported [VERIFIED]
- App data: `%APPDATA%\Devin\` (or `%APPDATA%\Windsurf\` legacy) [VERIFIED]
- Extensions: `~/.devin/extensions/` (or `~/.devin/extensions/`) [VERIFIED]
- Executable: `Devin.exe` / `Devin.app` / `devin` (Linux) [VERIFIED]
- CLI binaries: `devin-desktop`, `surf`, `windsurf` (all still work) [VERIFIED]

## Table of Contents

1. [Overview](#overview)
2. [What Changed (Windsurf to Devin Desktop)](#what-changed-windsurf-to-devin-desktop)
3. [Agent Harnesses](#agent-harnesses)
4. [Agent Client Protocol (ACP)](#agent-client-protocol-acp)
5. [Agent Command Center and Spaces](#agent-command-center-and-spaces)
6. [AI Models and Routing](#ai-models-and-routing)
7. [Windsurf Tab (Code Completion)](#windsurf-tab-code-completion)
8. [Context Awareness and Search](#context-awareness-and-search)
9. [Code Review (Devin Review and Quick Review)](#code-review-devin-review-and-quick-review)
10. [Customization](#customization)
11. [Cascade Hooks](#cascade-hooks)
12. [MCP Integration](#mcp-integration)
13. [Developer Tools](#developer-tools)
14. [Pricing and Plans](#pricing-and-plans)
15. [Enterprise Features](#enterprise-features)
16. [Settings and Configuration](#settings-and-configuration)
17. [Architecture Internals](#architecture-internals)
18. [Sources](#sources)
19. [Document History](#document-history)

## Overview

Devin Desktop (formerly Windsurf) is an AI-powered IDE built on VS Code Open Source Software (OSS), developed by Cognition (formerly Codeium). Renamed on 2026-06-02 via standard over-the-air update. Settings, keybindings, and most VS Code extensions remain compatible. The product frames itself as "an agent manager with a full IDE built in, not the other way around." [VERIFIED]

**Platform support:**
- **Windows** 10+ (64-bit)
- **macOS** Yosemite+
- **Linux** Ubuntu 20.04+ (glibc >= 2.31); other distributions glibc >= 2.28 [VERIFIED]

**Remote development:**
- **SSH** - Built-in implementation (not Microsoft's). Linux remote hosts only.
- **Dev Containers** - macOS, Windows, Linux. Local and remote (via SSH). Requires Docker.
- **Windows Subsystem for Linux (WSL)** - Beta support. Requires pre-configured WSL on Windows. [VERIFIED]

**Plugins:** Cascade agent also available as plugin for JetBrains (2023.3+), Visual Studio (17.5.5+), Neovim, Vim, Emacs, Xcode, Sublime Text, Eclipse. Devin Local only supported in Devin Desktop and Devin CLI. [VERIFIED]

**Devin Next:** Pre-release channel with early access. Download at devin.ai/download. [VERIFIED]

**Key concepts:**
- **Agent Command Center** - Default surface. Kanban view managing all agents.
- **Agent Client Protocol (ACP)** - Open protocol for running any compatible agent (Codex, Claude, OpenCode, Junie, Gemini CLI)
- **Devin Local** - Primary local agent (replaces Cascade)
- **Devin Cloud** - Autonomous cloud agent with own VM
- **Devin CLI** - Terminal agent, same harness as Devin Local
- **Spaces** - Task grouping with shared context
- **Adaptive Model Router** - Automatic model selection
- **Windsurf Tab** - AI-powered code completion (Autocomplete and Supercomplete)
- **Fast Context** - SWE-grep models for rapid codebase search (20x faster)
- **DeepWiki** - Auto-generated codebase documentation and architecture diagrams
- **Devin Review** - Deep PR review with smart diff organization
- **Quota system** - Daily/weekly token budgets [VERIFIED]

## What Changed (Windsurf to Devin Desktop)

### Naming and Branding

- Windsurf → Devin Desktop
- Windsurf.exe / Windsurf.app → Devin.exe / Devin.app
- windsurf.com/editor → devin.ai/download
- docs.devin.com → docs.devin.ai/desktop
- Cascade (primary agent) → Devin Local (primary), Cascade (legacy)

[VERIFIED]

### File Path Changes

**Per-user IDE data:**
- macOS: `~/Library/Application Support/Windsurf/` → `~/Library/Application Support/Devin/`
- Windows: `%APPDATA%\Windsurf\` → `%APPDATA%\Devin\`
- Linux: `~/.config/Windsurf/` → `~/.config/Devin/`

**Extensions:**
- `~/.devin/extensions/` → `~/.devin/extensions/`

**CLI binaries:** `devin-desktop`, `surf`, `windsurf` (all continue to work)
- Devin CLI: `devin` (`~/.local/bin/devin` or `%LOCALAPPDATA%\devin\bin\devin.exe`)

**Per-user config:** `~/.codeium/` unchanged (still used for settings, MCP config, hooks)

**System-level config (Enterprise):**
- macOS: `/Library/Application Support/Devin/` (was `Windsurf`)
- Windows: `C:\ProgramData\Devin\` (was `Windsurf`)
- Linux: `/etc/devin/` (was `/etc/windsurf/`)

[VERIFIED]

### Workspace-Level Changes

**Rules precedence:**
1. `.devin/rules/` (preferred, takes precedence)
2. `.devin/rules/` (backward-compatibility fallback)
3. `.devinrules` (legacy single-file, still read)
4. No `.devinrules` single-file equivalent exists

**Workflows:**
- `.devin/workflows/` or `.devin/workflows/` (both read)

**Skills:**
- `.devin/skills/` or `.devin/skills/` (both read)

**Plans:**
- `.devin/plans/` or `.devin/plans/`

**Ignore files:**
- `.codeiumignore` and `.devinignore` (both still honored)

**Also reads:** `AGENTS.md`, `agents.md`, `.cursor/rules/*.mdc` [VERIFIED]

### What Stayed the Same

- Plans and pricing unchanged
- Extensions compatible
- Keybindings preserved
- LSPs and workflows functional
- No migration needed (over-the-air (OTA) update)
- Settings and configuration carry over
- `.codeium/` directory structure unchanged [VERIFIED]

### Network Allowlist Updates

Hostnames to allow:
- `*.codeiumdata.com`
- `update.devin.com` (update check API)
- `*.devin.com`
- `*.codeium.com`
- `*.googleapis.com` (authentication)
- `apis.google.com` (authentication)
- `decagon.ai` (support)
- `docs.devin.ai` or `docs.devinenterprise.com` (documentation)
- `*.devin.ai`
- `*.devinenterprise.com`

**Update downloads:** `windsurf-stable.codeiumdata.com` (stable and next channels) [VERIFIED]

### MDM/Device Management Impact

Application name changed: policies allowing "Windsurf" may flag or block "Devin". Action required: update MDM allowlists before or after the June 2 update. [VERIFIED]

## Agent Harnesses

Devin Desktop provides multiple agent harnesses that coexist in the IDE.

### Devin Local (Primary Local Agent)

Devin Local is the primary local agent, successor to Cascade. Completely rewritten in Rust. Shares the same harness as Devin CLI. [VERIFIED]

**Key Improvements Over Cascade**

- **Token efficiency** - 30% fewer tokens for same tasks, greater focus on prompt caching [VERIFIED]
- **Subagents** - Spawn independent subagents for subtasks (foreground or background). Share tools and codebase context with parent. [VERIFIED]
- **OS-level sandboxing** - Filesystem isolation (writable/readable paths from permission scopes) and network filtering (domain allowlists/denylists). Enterprise-enforceable. [VERIFIED]
- **Quick Review** - Dedicated subagent for rapid feedback on changes [VERIFIED]

**Permissions Model**

Replaces Cascade's auto-execution levels:

- **Deny** rules - Block actions entirely (highest priority)
- **Ask** rules - Always prompt for approval
- **Allow** rules - Auto-approve without prompting

Scoped to: file reads, file writes, command execution, HTTP fetches, Model Context Protocol (MCP) tools. Configurable at project, user, or organization level. "Always Allow" grants persist across sessions (since 2026.5.26). [VERIFIED]

**MCP Configuration (Devin Local)**

- **Project**: `.devin/config.json` (version-controlled, shared with team)
- **Local override**: `.devin/config.local.json` (gitignored)
- **User**: `~/.config/devin/config.json` [VERIFIED]

**Limitations vs Cascade**

Not yet supported in Devin Local:
- **Memories** - Does not persist memories. Migrate to Skills.
- **Workflows** - Not available. Migrate to Skills.
- **Codemaps** - Does not read codemaps yet.
- **Code Lenses** - Do not trigger Devin Local.
- **Fast Context** - Uses subagents instead, no same UI.
- **App Deploys** - Not supported.
- **Conversation Sharing** - Not yet available. [VERIFIED]

Devin Local DOES support: Rules, AGENTS.md, Skills. [VERIFIED]

**Enterprise Controls (Devin Local)**

- **Sandbox enforcement** - Require sandbox mode for all users, org-wide domain filtering
- **Granular permissions** - Fine-grained action control beyond Cascade's level
- **Network enforcement** - Allowed/denied domain lists
- **Disable Cascade** - Force team to use Devin Local exclusively [VERIFIED]

### Cascade (Legacy Local Agent)

Open: `Cmd/Ctrl+L` or click agent icon (top right). Selected text in editor/terminal auto-included. **Legacy status: maintained through at least July 1, 2026.** [VERIFIED]

**Modes**

Three modes, switchable via toggle below input box or `Ctrl+.`:

- **Code Mode** - Full tool access. Default mode. [VERIFIED]
- **Plan Mode** - Full tool access. Type `megaplan` for advanced form. Auto-switches to Code Mode when implementing. [VERIFIED]
- **Ask Mode** - Search tools only. Cannot modify files or run commands. [VERIFIED]

**Capabilities**

- Read/Write files, run terminal commands, web search (`@web`, `@docs`)
- MCP integration, up to 20 tool calls per prompt
- Voice input, Plans and Todo Lists, Queued Messages
- Linter integration (auto-fix, free), Image attachments, Mermaid diagrams
- Git Worktree Support, Multi-Cascade Panes and Tabs [VERIFIED]

**Auto-Execution Policies**

Four levels:
- **Disabled** - All commands require approval
- **Allowlist** - Only allowlisted commands auto-execute
- **Auto** - Model decides if safe (premium models only)
- **Turbo** - All commands auto-execute except denylist [VERIFIED]

### Devin Cloud (Autonomous Cloud Agent)

Autonomous software engineering agent on its own VM with desktop, browser, and computer use. Works asynchronously. Delivers Pull Requests. [VERIFIED]

**Availability:**
- Included with every self-serve plan (Pro, Max, Teams) [VERIFIED]
- Enterprise: disabled by default, admin must enable [VERIFIED]
- First-time users get up to $50 in extra usage [VERIFIED]

**Delegation Workflow:**
1. Plan locally with Devin Local or Cascade
2. One-click delegation to Devin Cloud
3. Devin spins up VM, works independently (debugging, deployment, testing)
4. Review changes and test results in-editor
5. Returns a reviewable Pull Request [VERIFIED]

**Pricing:** Consumes shared quota and extra usage balance. Same token-based system. [VERIFIED]

### Devin for Terminal (CLI Agent)

Rust-based CLI agent available for all Devin Desktop users. Same harness as Devin Local. [VERIFIED]

**Capabilities:**
- Full codebase and tools access on user's machine
- Hand off to Devin Cloud for async work
- Multi-model: Opus 4.7, GPT-5.5, SWE-1.6
- Sessions accessible from both IDE and CLI [VERIFIED]

**Install:**
- macOS/Linux: `curl -fsSL https://cli.devin.ai/install.sh | bash`
- Windows: See official docs at docs.devin.ai/desktop [VERIFIED]

### Agent Selector

Agent selector in bottom-right corner when starting new conversations. Options:
- Devin Local (primary)
- Cascade (legacy)
- ACP agents (if enabled)

Enterprise admins can disable Cascade entirely via "Enable Cascade" control. [VERIFIED]

## Agent Client Protocol (ACP)

Devin Desktop ships with ACP, an open-source protocol that standardizes communication between code editors and coding agents. Analogous to Language Server Protocol (LSP) for language intelligence. [VERIFIED]

**Purpose:** Lets any compatible agent run inside any ACP-compatible editor. Third-party agents get the same interface as Devin: Kanban view, Spaces, shared context. [VERIFIED]

**Example agents (per official docs):**
- **Codex CLI** (OpenAI) - OpenAI's coding agent
- **Claude Agent** (Anthropic) - Anthropic's coding agent
- **OpenCode** - Open source coding agent
- **Junie** (JetBrains) - JetBrains' coding agent
- **Gemini CLI** (Google) - Google's coding agent
- **Custom agents** - In-house agents built by teams [VERIFIED]

**Enabling ACP agents:**
1. Command Palette > "Windsurf User Settings"
2. Click "Agents" tab
3. Toggle on desired ACP agents
4. Restart Devin Desktop [VERIFIED]

**Registry configuration:**
- Local: `~/.devin/acp/registry.json` (or `~/.devin-next/acp/registry.json`)
- Team: configured via team settings
- Command Palette: "Open Local ACP Registry Config" [VERIFIED]

**ACP registry format example (Devin Local):**
```json
{
  "version": "1.0.0",
  "agents": [
    {
      "id": "devin-cli",
      "name": "Devin Local",
      "version": "1.0.0",
      "description": "Devin AI coding agent via Devin CLI",
      "authors": ["Cognition AI"],
      "license": "proprietary",
      "distribution": {
        "binary": {
          "darwin-aarch64": { "cmd": "devin", "args": ["acp"] },
          "windows-x86_64": { "cmd": "devin", "args": ["acp"] }
        }
      }
    }
  ]
}
```
[VERIFIED]

**Availability:** Pro, Max, and Teams users. Enterprise admins contact account team for third-party agent access. [VERIFIED]

**Specification:** https://agentclientprotocol.com/ [VERIFIED]

## Agent Command Center and Spaces

### Agent Command Center (Kanban View)

The default surface in Devin Desktop. Manages every agent (local and cloud) from one place. Kanban board grouped by status. [VERIFIED]

**Status columns:**
- In Progress
- Blocked
- Ready for Review [VERIFIED]

**Agent types shown:**
- Local agents (Devin Local, Cascade, ACP agents)
- Cloud agents (Devin sessions on VMs) [VERIFIED]

**Display options:**
- Kanban board (default)
- List display (inbox view) [VERIFIED]

**Key capability:** Parallel agents. Multiple agents working simultaneously on different parts of same project. One engineer fans out work, reviews results as they land. [VERIFIED]

**Recent improvements:**
- List display option for agent inbox
- Improved sessions sidebar sorting and filtering
- Performance improvements for loading and switching sessions [VERIFIED]

### Spaces (Task Grouping)

Spaces group everything related to a task or project:

- **Agent sessions** - Local and cloud sessions
- **Pull requests** - PRs opened by user or agents
- **Files** - Relevant files
- **Context** - Project-level context inherited by new sessions [VERIFIED]

**Context sharing:** New sessions in a Space inherit everything the Space already knows. Agents start with useful context instead of blank slate. [VERIFIED]

**Switching:** Switching Spaces = switching tasks. View restored exactly as left. [VERIFIED]

**Creating a Space:**
- **Drag session onto session** - In sidebar, drag to group
- **Split pane** - `Cmd/Ctrl+\` then "New Session" in empty pane
- **Keyboard shortcut** - `Cmd/Ctrl+T` opens new session in current Space [VERIFIED]

**Default behavior:** Every session is its own Space by default. No need to create one explicitly. [VERIFIED]

## AI Models and Routing

### SWE Model Family (In-house, Cognition)

- **SWE-1.6** - Latest. Optimized intelligence and model UX. Parallel tool calls, less looping. Free on paid plans. [VERIFIED]
- **SWE-1.6 Fast** - Same intelligence, unmatched speed and cost. Paying users only. [VERIFIED]
- **SWE-1.5** - Previous frontier. ~950 tokens/sec. **Free model.** [VERIFIED]
- **SWE-1** - First agentic model. Claude 3.5-level at fraction of cost. [VERIFIED]
- **SWE-1-mini** - Powers Tab passive suggestions, optimized for real-time latency. [VERIFIED]
- **swe-grep / swe-grep-mini** - Powers Fast Context. Up to 2,800 tokens/sec. RL-trained for parallel tool calling. [VERIFIED]
- **SWE-check** - Quick Review model for bug detection. Free for all tiers. Up to 10x faster than deep review agent. [VERIFIED]

### Third-Party Models (as of June 2026)

**Anthropic:**
- Claude Opus 4.8 ($5.00/M input, $25.00/M output) [VERIFIED]
- Claude Opus 4.8 Fast Mode ($10.00/M input, $50.00/M output) [VERIFIED]
- Claude Opus 4.7 / 4.7 Fast Mode (~2.5x higher output speed) [VERIFIED]
- Claude Sonnet 4.6, Opus 4.6 / 4.6 Fast Mode, Sonnet 4.5

**OpenAI:**
- GPT-5.5, GPT-5.4 / GPT-5.4 Mini
- GPT-5.2-Codex / GPT-5.1-Codex / GPT-5.1-Codex Max
- o4-mini

**Google:**
- Gemini 3.1 Pro / Gemini 3 Pro / Gemini 3 Flash

**Other:**
- Kimi K2.5, Grok Code Fast, GLM-5, Minimax M2.5
- DeepSeek-R1 / DeepSeek-V3
- Falcon Alpha [VERIFIED]

### Adaptive Model Router

Automatically selects best model for each task. Available to Pro, Max, and Teams users. [VERIFIED]

**Pricing (introductory):**
- Input: $0.50/M tokens
- Output: $2.00/M tokens
- Cache read: $0.10/M tokens

Fixed rate regardless of underlying model selected. Typically fewer tokens overall than manual selection. [VERIFIED]

**Tips:**
- Be specific with prompts for better routing
- Stay on same model across turns for caching
- Use as default; switch manually only when needed [VERIFIED]

### Arena Mode

Two models respond simultaneously, anonymously. User votes. Model identities revealed after voting. [VERIFIED]

- **Battle Groups** - Choose specific models or let system select
- **Personal and Global Leaderboards** - Votes contribute to both
- **Sync or Branch** - Followup to both simultaneously, or branch paths [VERIFIED]

### Model Picker

- Groups models by family with hovercards
- Per-model input, output, and cache read token rates visible
- Prompt cache timer in context window indicator
- Token counts in response cards
- Pin favorite models for quick access [VERIFIED]

### Bring Your Own Key (BYOK)

- Available to free and paid individual users (not Teams/Enterprise)
- Currently supported: Claude 4 Sonnet / Opus (regular and Thinking)
- Configure at: devin.ai/subscription/provider-api-keys [ASSUMED URL updated with rename]

## Windsurf Tab (Code Completion)

Contextually aware diff-suggestion engine powered by SWE-1-mini. Name retained from Windsurf branding. [VERIFIED]

### Autocomplete vs Supercomplete

- **Supercomplete** (recommended, default) - Small windows around cursor suggesting deletions and additions
- **Autocomplete** - Traditional inline completion at cursor position [VERIFIED]

### Tab to Jump

Anticipates next cursor position. Press Tab to navigate. Avoids manual scrolling. [VERIFIED]

### Tab to Import

After defining new dependency, press Tab to auto-import at file top. Cursor stays in place. [VERIFIED]

### Context Sources

- Current file and open files
- Recent terminal activity
- Recent code changes
- Clipboard contents (opt-in)
- Agent chat history [VERIFIED]

### Keyboard Shortcuts

- Accept: `Tab`
- Cancel: `Esc`
- Accept word-by-word: `Cmd+Right` (VS Code) / `Alt+Shift+\` (JetBrains) [VERIFIED]

## Context Awareness and Search

### Fast Context

Specialized subagent retrieving relevant code 20x faster than traditional agentic search. Uses SWE-grep and SWE-grep-mini models. [VERIFIED]

- Triggers automatically on code search queries
- Executes multiple searches simultaneously (up to 8 parallel tool calls per turn, max 4 turns)
- Uses restricted cross-platform tools (grep, read, glob)
- Prevents context pollution [VERIFIED]

**Devin Local note:** Devin Local uses subagents instead of Fast Context and lacks the same UI. [VERIFIED]

### DeepWiki

AI-powered codebase documentation. Auto-indexes repositories and generates:
- Architecture diagrams
- Codebase summaries
- Links back to source code [VERIFIED]

New agents in a Space read the DeepWiki index for immediate context instead of crawling the repo cold. Available in Primary Side Bar / Activity Bar. [VERIFIED]

**Usage:**
- Hover over symbol > `Cmd+Shift+Click` for detailed explanation
- Send explanations to agent via context menu [VERIFIED]

### Knowledge Base (Beta)

- Teams and Enterprise only
- Google Docs as shared context for entire team
- Admin connects Google Drive via OAuth, adds up to 50 docs [VERIFIED]

### Remote Indexing

- Teams and Enterprise only
- Index remote repositories without local clone [VERIFIED]

### Web and Docs Search

- `@web` - General web search
- `@docs` - Curated documentation search
- Paste URLs directly into chat [VERIFIED]

### Ignore Files

- `.codeiumignore` - Prevents agent from reading/indexing specific files
- `.devinignore` - Also honored
- Global: `~/.codeium/windsurf/.codeiumignore`
- Setting: `windsurf.allowCascadeAccessGitignoreFiles` [VERIFIED]

## Code Review (Devin Review and Quick Review)

### Devin Review

Deep PR review with smart diff organization. Available for all self-serve users (2-week free trial [ASSUMED]). Enterprise requires Cognition platform agreement. [VERIFIED]

**Capabilities:**
- Organizes diffs around logic of change (not alphabetical files)
- Groups related edits together
- Displays copied/moved code cleanly
- Identifies bugs and flags with explanations
- In-editor review without leaving IDE [VERIFIED]

**Autofix:** When enabled, Devin generates fixes for review comments and applies back to PR branch. Closes the loop: agent writes code, Devin Review checks, Devin fixes issues. [VERIFIED]

**Workflow:**
1. Agent creates PR
2. Devin Review analyzes the diff
3. Findings surfaced in-editor with explanations
4. Ask questions, use codebase-aware chat for context
5. Autofix applies corrections
6. GitHub auto-merge when checks pass [VERIFIED]

### Quick Review

Fast local review before opening a PR. Only available with Devin Local agent. [VERIFIED]

**Models:**
- **SWE-check** - Fast, free for all tiers (10x faster than deep review)
- **GPT 5.5** - Deep agentic review, token-based pricing
- **Opus 4.7** - Deep agentic review, token-based pricing [VERIFIED]

Enterprise: Admin must enable from team settings. Can control available review models. [VERIFIED]

### Two Review Loops

- **Quick Review** - Before opening PR. Fast feedback on working tree changes.
- **Devin Review** - After PR opened. Deep review with smart organization and Autofix. [VERIFIED]

## Customization

Five mechanisms for customizing agent behavior. Skills are the only mechanism working across both Cascade and Devin Local.

### Decision Guide

- **Memories** - Auto-remembered context, quick manual notes (Cascade only)
- **Rules** - Persistent coding style, project conventions, behavioral constraints
- **Workflows** - Step-by-step procedures (Cascade only)
- **Skills** - Complex multi-step tasks with templates/scripts (universal)
- **AGENTS.md** - Directory-scoped instructions [VERIFIED]

### Rules

Persistent instructions that agents follow. [VERIFIED]

**Storage locations (discovery order):**
1. **Global rules**: `~/.codeium/windsurf/memories/global_rules.md` (always on, 6,000 char limit)
2. **Workspace rules**: `.devin/rules/*.md` (preferred) or `.devin/rules/*.md` (fallback). One file per rule, 12,000 chars per file.
3. **AGENTS.md**: Directory-scoped. Root-level = always-on, subdirectory = auto-glob.
4. **System-level** (Enterprise): `/etc/devin/rules/` or `C:\ProgramData\Devin\rules\` [VERIFIED]

**Activation modes (frontmatter `trigger` field):**

- **Always On** (`trigger: always_on`) - Full rule in system prompt on every message
- **Model Decision** (`trigger: model_decision`) - Only `description` shown; agent reads full rule when relevant
- **Glob** (`trigger: glob`) - Applied when files matching `globs` pattern are touched
- **Manual** (`trigger: manual`) - Activated by `@rule-name` in chat [VERIFIED]

**Example:**
```markdown
---
trigger: glob
globs: **/*.test.ts
---

All test files must use describe/it blocks and mock external API calls.
```

### Workflows (Cascade Only)

Step-by-step procedures as markdown. Invoked via `/workflow-name`. **NOT supported with Devin Local.** [VERIFIED]

**Storage:** `.devin/workflows/*.md` or `.devin/workflows/*.md`

**Format:**
```yaml
---
description: [short title]
---
[specific steps]
```

**Migration:** Convert workflows to Skills for Devin Local compatibility. [VERIFIED]

### Skills (Universal)

Bundles for complex tasks. Include `SKILL.md` plus supporting files. **Works with BOTH Cascade and Devin Local.** [VERIFIED]

**Creation:**
- UI: Windsurf Settings > Skills
- Manual: `.devin/skills/<name>/SKILL.md` or `.devin/skills/<name>/SKILL.md` or `.agents/skills/<name>/`

**Invocation:**
- Automatic (agent matches task to skill description)
- Manual (`@skill-name` in chat) [VERIFIED]

### AGENTS.md

Directory-scoped instruction files. Placed in any directory. Agent auto-discovers and scopes instructions to files within that directory. [VERIFIED]

Devin Local and Cascade both support AGENTS.md. [VERIFIED]

### Memories (Cascade Only)

Auto-generated during conversation. Workspace-scoped. Stored in `~/.codeium/windsurf/memories/`. Creating/using memories does NOT consume quota. **NOT supported with Devin Local.** [VERIFIED]

**Recommendation:** Prefer Rules or Skills for durable, shared knowledge. [VERIFIED]

## Cascade Hooks

Shell scripts running before/after agent actions. Enable logging, access control, formatting. [VERIFIED]

### Configuration

`.devin/hooks.json` or `~/.codeium/windsurf/hooks.json`:

```json
{
  "hooks": [
    {
      "event": "post_write_code",
      "command": "python format_code.py",
      "timeout": 30
    }
  ]
}
```

### Hook Events

- `pre_read_code` / `post_read_code`
- `pre_write_code` / `post_write_code`
- `pre_run_command` / `post_run_command`
- `pre_mcp_tool_use` / `post_mcp_tool_use`
- `pre_user_prompt` (can block)
- `post_cascade_response`
- `post_cascade_response_with_transcript`
- `post_setup_worktree` [VERIFIED]

### Devin Local Hooks

Hooks repaired for Devin Local to allow blocking user prompts (2026.5.26). Plan mode works in OS sandbox. [VERIFIED]

## MCP Integration

Devin Desktop supports Model Context Protocol (MCP) for external tools and services. [VERIFIED]

### Cascade MCP Configuration

**Config file:** `~/.codeium/windsurf/mcp_config.json`

```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-name"],
      "env": { "API_KEY": "${env:API_KEY}" }
    }
  }
}
```

**Transport types:** stdio, Server-Sent Events (SSE), Remote HTTP [VERIFIED]

### Devin Local MCP Configuration

Different from Cascade:
- **Project**: `.devin/config.json` (version-controlled)
- **Local override**: `.devin/config.local.json` (gitignored)
- **User**: `~/.config/devin/config.json`

Server-level "approve all" (session or permanent) for MCP tool permissions. [VERIFIED]

### OAuth Support

MCP OAuth flow forwards RFC 8707 resource parameter (fixes auth for servers like Snowflake requiring resource indicators). [VERIFIED]

### Admin Controls (Teams/Enterprise)

- **MCP Registry** - Pre-configured approved servers
- **MCP Whitelist** - Regex-based control of allowed servers [VERIFIED]

## Developer Tools

### Terminal

- Command execution with auto-execution policies (Cascade) or permissions model (Devin Local)
- Send terminal selection to agent
- @-mention terminal output
- Dedicated Terminal (Beta) - Separate terminal profile for agent execution [VERIFIED]

### Windsurf Previews

Preview web apps in IDE or browser with element selection, error capture, and agent integration. [VERIFIED]

### Vibe and Replace

AI-powered find-and-replace. Search codebase, apply AI prompt to each replacement. Modes: Smart (careful) and Fast. [VERIFIED]

### Codemaps

Visual architecture diagrams. Referenced via `@codemap-name`. Devin Local does not yet read Codemaps. [VERIFIED]

### App Deploys

Deploy to Netlify directly from IDE. Supports Next.js, React, Vue, Svelte. Beta. Not supported with Devin Local. [VERIFIED]

### AI Commit Messages

Auto-generated commit messages based on staged changes. [VERIFIED]

### Worktrees

Git worktree support. Each worktree has own directory. `post_setup_worktree` hook event. [VERIFIED]

### Other Tools

- **Diff Zones** - Visual indicators for agent-edited code regions
- **Explain and Fix** - Highlight error, have agent resolve
- **Code Lenses** - Inline actions (Explain, Refactor, Add Docstring). Not yet for Devin Local.
- **Smart Paste** - Context-aware paste
- **Send Problems to Agent** - Problems panel integration [VERIFIED]

## Pricing and Plans

Quota-based usage system (replaced credits in March 2026). [VERIFIED]

### Quota-Based Usage

- Daily and weekly allowance that refreshes automatically
- Cost per token varies by model
- Free models (SWE-1.5) don't count against quota
- Most users never hit limits [VERIFIED]

**When quota exhausted:**
- **Free**: Wait for daily/weekly reset
- **Pro/Max/Teams**: Purchase extra usage [VERIFIED]

**Extra usage pricing (introductory):**
- Input: $0.50/M tokens
- Output: $2.00/M tokens
- Cache read: $0.10/M tokens [VERIFIED]

### Plan Tiers

- **Free** - Limited quota, limited model availability, unlimited Tab completions
- **Pro** - $15/month, expanded quota, all models, extra usage available
- **Max** - $60/month, highest individual quota, significantly higher limits
- **Teams** - $40/user/month, team management, Knowledge Base, Remote Indexing, analytics, RBAC
- **Enterprise** - Custom pricing (ACU-based), SSO/SCIM, FedRAMP, system-level controls

**Note**: Prices from research. Check devin.ai/pricing for current rates. [ASSUMED prices]

### Making Quota Last

- Be precise, remove unnecessary context
- Switch to free models (SWE-1.5) for routine tasks
- Use smaller models (Haiku, GPT 5.2 Mini, Kimi K2.5)
- Avoid unnecessarily long sessions
- Use single model per task for caching benefits [VERIFIED]

### Enterprise Billing

- **Agent Compute Units (ACUs)** - Tokens converted to ACUs at per-token rates listed on models page
- **Legacy Credits** - Being phased out
- **Cap configuration** - Per-user or per-group caps via admin portal [VERIFIED]

### Seat Rotation

If a team member leaves mid-cycle and a new member takes the seat, the new member inherits remaining quota. Full reset at next billing cycle start. [VERIFIED]

## Enterprise Features

### Admin Portal

- Admin portal at devin.ai/team/settings [ASSUMED URL updated with rename]
- User management with role assignment
- User groups for bulk operations
- Quota allocation and caps [VERIFIED]

### Role-Based Access Control (RBAC)

**Roles:** Built-in (Admin, Member) and custom roles with granular permissions.

**Permissions:** Model access, feature access, auto-execution levels, "Disable Access" to restrict users entirely. [ASSUMED label updated with rename]

### Single Sign-On (SSO) and SCIM

Providers: Azure AD/Entra ID, Google Workspace, Okta, OneLogin, Generic OIDC/SAML. System for Cross-domain Identity Management (SCIM) for automated user lifecycle. [VERIFIED]

### Enterprise Policies (Group Policy Object (GPO) / Mobile Device Management (MDM))

- Windows: ADMX/ADML for Group Policy
- macOS: .mobileconfig for MDM
- Linux: JSON policy files
- Extension Management: AllowedExtensions whitelist, server-driven deny lists [VERIFIED]

### FedRAMP

FedRAMP Security Admin Guide available with administrative roles, permissions, multi-factor authentication (MFA), and security settings reference. [VERIFIED]

### Analytics API

- Get Cascade Analytics (lines, runs, tool usage)
- Custom Analytics Query (selections, filters, aggregations)
- Get Team Credit Balance
- Get/Set Usage Configuration
- Per-user analytics
- Service Keys with rate limits [VERIFIED]

### Devin Local Enterprise Controls

Additional controls only available with Devin Local:
- **Sandbox enforcement** - Org-wide sandbox mode and domain filtering
- **Granular permissions** - Fine-grained action control
- **Network enforcement** - Allowed/denied domain lists
- **Disable Cascade** - Force Devin Local exclusively [VERIFIED]

## Settings and Configuration

### Directory Structure (Windows, Post-Rename)

```
C:\Users\<User>\
├── .codeium\
│   └── windsurf\                  # Unchanged (still .codeium/windsurf)
│       ├── user_settings.pb       # Agent UI settings (protobuf binary)
│       ├── mcp_config.json        # MCP server configurations (Cascade)
│       ├── hooks.json             # User-level hooks
│       ├── global_rules.md        # Global rules
│       ├── skills\                # Global skills
│       └── metrics\               # Usage metrics
│
├── .devin\                        # NEW: Devin extensions
│   └── extensions\
│
├── .config\
│   └── devin\
│       └── config.json            # Devin Local user-level config
│
├── AppData\
│   ├── Local\Programs\
│   │   ├── Devin\                 # Main installation (was Windsurf)
│   │   │   └── resources\app\extensions\
│   │   └── Devin Next\            # Preview channel
│   │
│   └── Roaming\
│       └── Devin\                 # User data (was Windsurf)
│           └── User\
│               ├── settings.json
│               ├── keybindings.json
│               └── globalStorage\state.vscdb
```
[VERIFIED]

### Two Settings Systems

- **Editor settings** - JSON at `%APPDATA%\Devin\User\settings.json`. Editable via text editor. Includes `windsurf.*` keys for agent settings.
- **Agent settings** (UI-only subset) - Protobuf at `%USERPROFILE%\.codeium\windsurf\user_settings.pb`. Many settings also writable via `windsurf.*` keys. [VERIFIED]

### Key Agent Settings (`windsurf.*` prefix retained)

```json
{
  "windsurf.autoExecutionPolicy": "turbo",
  "windsurf.autoWebRequestPolicy": "turbo",
  "windsurf.autoContinue": true,
  "windsurf.completionMode": "autocomplete",
  "windsurf.rememberLastModelSelection": true,
  "windsurf.allowCascadeAccessGitignoreFiles": true,
  "windsurf.acp.enabledAgents": { "devin-cli": true }
}
```
[VERIFIED]

### Key Files Reference

**User Config:**
- `settings.json` - Editor preferences (JSON)
- `keybindings.json` - Keyboard shortcuts
- `user_settings.pb` - Agent UI settings (protobuf)
- `state.vscdb` - Window/extension state (SQLite)
- `mcp_config.json` - MCP servers (Cascade)
- `~/.codeium/windsurf/hooks.json` - User-level hooks

**Workspace Config:**
- `.devin/rules/*.md` - Project rules (preferred)
- `.devin/rules/*.md` - Project rules (fallback)
- `.devin/workflows/*.md` - Custom workflows
- `.devin/skills/*/SKILL.md` - Skills
- `.devin/config.json` - Devin Local MCP and permissions
- `.devin/config.local.json` - Local override (gitignored)
- `.devin/hooks.json` - Workspace hooks
- `AGENTS.md` - Directory-scoped instructions
- `.codeiumignore` / `.devinignore` - Ignore files

**ACP Config:**
- `~/.devin/acp/registry.json` - Local ACP agent registry [VERIFIED]

### Telemetry and Privacy

Devin Desktop collects non-essential telemetry data by default. Opt out via account settings.

**Disable Telemetry:**
1. Open devin.ai/account (or Codeium account page) [ASSUMED URL updated with rename]
2. Scroll to **Privacy** section
3. Toggle **Disable Telemetry** to on

**What it controls:**
- Non-essential data collection used to improve the product
- Does NOT affect prompt caching, autocomplete, or agent functionality
- Stored server-side (account setting), not in local config files [VERIFIED]

### Working with Private/Gitignored Folders

Agents can read/write gitignored files when explicitly referenced, but gitignored folders are hidden from the workspace snapshot shown at conversation start.

**To make a gitignored folder visible to agents while keeping contents private:**

1. Use a `.gitkeep` file to track the folder structure
2. Configure `.gitignore` to ignore contents but not the `.gitkeep`

**.gitignore pattern:**
```gitignore
# Private sessions folder (contents ignored, folder tracked)
_PrivateSessions/*
!_PrivateSessions/.gitkeep
```

**.gitkeep file:**
```bash
echo "# This file makes the folder visible to agents" > _PrivateSessions/.gitkeep
```

**How it works:**
- `_PrivateSessions/*` - Ignores all files/folders inside
- `!_PrivateSessions/.gitkeep` - Negation pattern, tracks this specific file
- Result: Folder appears in workspace, contents stay private [VERIFIED]

## Architecture Internals

Based on reverse-engineering from Windsurf 2.x era. Core architecture assumed unchanged in Devin Desktop rename. [ASSUMED based on FAQ - process model untested on Devin Desktop. Verify before enterprise security/monitoring use]

### Process Model

```
Devin.exe (Electron main process)
├─ Devin.exe (GPU process)
├─ Devin.exe (renderer - editor UI)
├─ Devin.exe (extension host - Node.js)
├─ Devin.exe (shared process)
├─ Devin.exe (file watcher)
└─ language_server_windows_x64.exe (Codeium language server - Go binary)
```

- **Electron processes** (~14): Standard VS Code/Electron architecture
- **Language server** (1): Handles ALL AI communication [TESTED 2026-05 on Windsurf]

### Language Server Binary

**Path (estimated)**: `C:\Users\<User>\AppData\Local\Programs\Devin\resources\app\extensions\windsurf\bin\language_server_windows_x64.exe`

**Characteristics:**
- Size: ~166 MB
- Language: Go (compiled binary)
- Makes direct HTTPS calls to Codeium APIs [TESTED 2026-05 on Windsurf]

### API Endpoints

- `https://server.self-serve.devin.com` - Primary API (auth, settings, telemetry)
- `https://inference.codeium.com` - AI inference (chat, completions, tool calls) [TESTED 2026-05]

### Network Architecture

Three independent network stacks:

1. **Chromium** (Electron renderer): System proxy. Handles: marketplace, updates, previews.
2. **Node.js** (extension host): Honors HTTP_PROXY/HTTPS_PROXY. Handles: extensions, MCP.
3. **Go binary** (language server): Honors proxy ONLY when `--detect_proxy=true`. Handles: ALL AI communication. [TESTED 2026-05]

### MCP Transport

- Protocol: JSON-RPC 2.0
- Transport: Newline-Delimited JSON (NDJSON) over stdio
- Protocol version: `2025-11-25`
- Tool visibility: MCP tools receive ONLY tool_call arguments; no system prompt leakage [TESTED 2026-05]

### Proxy Detection

- Setting: `user_settings.pb` field 34 (`detect_proxy`, bool)
- Default: `false` (proxy detection disabled)
- UI: Settings panel > "Detect Proxy" checkbox [TESTED 2026-05]

## Sources

### Official Sources (2026-06-03)

- https://devin.ai/blog/windsurf-is-now-devin-desktop - Official announcement (2026-06-02)
- https://docs.devin.ai/desktop/devin-desktop-faq - Transition FAQ
- https://docs.devin.ai/desktop/devin-local - Devin Local documentation
- https://docs.devin.ai/desktop/acp - Agent Client Protocol documentation
- https://docs.devin.ai/desktop/changelog - Official changelog
- https://docs.devin.ai/desktop/accounts/usage - Plans and usage
- https://devin.ai/pricing - Current pricing page
- https://devin.ai/blog/devin-review-windsurf - Devin Review announcement
- https://agentclientprotocol.com/ - ACP specification
- https://github.com/agentclientprotocol/agent-client-protocol - ACP GitHub

### Third-Party Analysis

- https://apidog.com/blog/whats-new-in-devin-2026/ - Comprehensive feature comparison
- https://releasebot.io/updates/windsurf - Release notes aggregation

### Previous Research (from WSRF-IN01)

- Session `_2026-06-01_WindsurfFeatureResearch` - Deep research on Windsurf 2.x features
- Session `_2026-05-27_CascadeMetapromptExtraction` - Architecture internals testing
- https://docs.devin.com/llms-full.txt - Full documentation export (accessed 2026-06-01)

## Document History

**[2026-06-03 18:30]**
- Fixed: AP-PR-07 violation - removed vague "extremely performant" from CLI section
- Fixed: AP-BR-02 - removed filler "seamlessly" from CLI section
- Fixed: AP-BR-03 - removed redundant "Written in Rust" (already in header)
- Fixed: AP-ST-06 - CLI section restructured: capabilities separated from installation
- Verified: /improve APAPALAN polish pass. No remaining filler words.

**[2026-06-03 17:45]**
- Fixed: Path ordering in Summary - `.devin/` before `.devin/` to match body (lines 33-35)
- Fixed: Stale URLs `windsurf.com/subscription/...` and `windsurf.com/team/settings` updated to `devin.ai` [ASSUMED]
- Fixed: Stale permission label "Disable Windsurf Access" generalized to "Disable Access" [ASSUMED]
- Fixed: DeepWiki "Add to Cascade" menu label generalized to "context menu"
- Added: Telemetry and Privacy subsection (from WSRF-IN01)
- Added: Working with Private/Gitignored Folders subsection (from WSRF-IN01)
- Added: Seat Rotation subsection (from WSRF-IN01)
- Verified: /improve comparison pass against WSRF-IN01 template

**[2026-06-03 17:40]**
- Fixed: Acronyms expanded on first use: WSL, SSE, NDJSON, MFA (AP-PR-06)
- Verified: Final /verify pass after /critique + /reconcile + /implement cycle. All checks pass.

**[2026-06-03 17:35]**
- Fixed: Version scope removed invented "3.x" numbering (RV-001)
- Fixed: ACP heading changed from "Supported agents" to "Example agents" per official docs (RV-002)
- Fixed: Cascade deadline clarified as "at least July 1" (RV-006)
- Fixed: CLI install command noted as macOS/Linux, added Windows reference (RV-008)
- Fixed: Architecture caveat strengthened for enterprise use (RV-005)
- Fixed: Devin Review trial terms marked [ASSUMED] (RV-012)
- Verified: /critique + /reconcile pass completed, 6 confirmed fixes applied

**[2026-06-03 17:30]**
- Fixed: Markdown table in "Naming and Branding" converted to list (GLOBAL-RULES)
- Fixed: Acronyms expanded on first use: MCP, RBAC, SSO, SCIM, GPO, MDM, LSP, OTA (AP-PR-06)
- Fixed: Arrow `->` replaced with `→` in File Path Changes (core-conventions)
- Added: Timeline field in header block (INFO_TEMPLATE)
- Verified: /verify pass completed

**[2026-06-03 17:12]**
- Initial document created from deep research on Devin Desktop (formerly Windsurf)
- Based on: WSRF-IN01 (INFO_HOW_WINDSURF_WORKS.md) as structural template
- Added: "What Changed" section documenting Windsurf-to-Devin transition
- Added: Agent Client Protocol (ACP) section (new in Devin Desktop)
- Added: Code Review section (Devin Review + Quick Review, new prominence)
- Changed: Devin Local promoted to primary agent (was preview in WSRF-IN01)
- Changed: Cascade marked as legacy (through July 1, 2026)
- Changed: Agent Command Center described as default surface (was secondary)
- Changed: File paths updated for Devin naming (.devin/ precedence)
- Changed: Documentation URLs updated (docs.devin.ai)
- Retained: Architecture internals section (core unchanged per FAQ)
- Sources: 10 official, 2 third-party, plus WSRF-IN01 research
