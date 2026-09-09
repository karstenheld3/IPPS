# INFO: How Windsurf Works

**Doc ID**: WSRF-IN01
**Goal**: Comprehensive reference for Windsurf Integrated Development Environment (IDE) - agent harnesses, AI models, customization, developer tools, enterprise controls, and architecture internals
**Version scope**: Windsurf 2.0+ (June 2026) / Devin Local 2026.5.26

## Summary

**Agent harnesses:**
- Two local agents: Cascade (legacy) and Devin Local (next-gen, 30% more token-efficient, subagents, OS-level sandboxing) [VERIFIED]
- Devin Cloud: autonomous cloud agent on dedicated Virtual Machines (VMs), in-editor Pull Request (PR) review [VERIFIED]
- Devin for Terminal: Rust-based Command Line Interface (CLI) agent, cross-platform [VERIFIED]
- Agent Command Center: Kanban-style management of all local and cloud agents [VERIFIED]
- Spaces: task grouping with shared context across agent sessions [VERIFIED]

**Cascade specifics:**
- Three modes: Code, Plan, Ask (formerly Chat). `megaplan` for advanced planning [VERIFIED]
- `.devin/rules/*.md` for instructions, 4 trigger modes: `always_on`, `model_decision`, `glob`, `manual` [VERIFIED]
- Workflows in `.devin/workflows/*.md`, invoked as `/workflow-name` [VERIFIED]
- Skills in `.devin/skills/<name>/SKILL.md` or `.agents/skills/` - ONLY mechanism working across both Cascade and Devin Local [VERIFIED]
- Memories auto-generated during conversation, workspace-scoped [VERIFIED]
- Model switching preserves full context; model fixed per response, change takes effect on next turn [TESTED]
- Smaller context window: earlier messages dropped/summarized automatically without warning [VERIFIED]
- Different providers (Claude/GPT/SWE): Cascade abstracts differences, transparent switching [VERIFIED]

**Devin Local limitations:**
- Does NOT support: Workflows, Memories, Codemaps, Code Lenses, App Deploys, Conversation Sharing [VERIFIED]
- Permissions model (Deny/Ask/Allow) differs fundamentally from Cascade's auto-execution levels [VERIFIED]
- Config: `.devin/config.json` for Model Context Protocol (MCP) and permissions [VERIFIED]

**AI models:**
- SWE-1.6 (in-house, optimized for software engineering), Claude Opus 4.8, GPT-5.5 [VERIFIED]
- Adaptive router: intelligent model selection balancing speed and capability [VERIFIED]
- Arena Mode: side-by-side model comparison with battle groups and leaderboards [VERIFIED]
- Bring Your Own Key (BYOK) for Anthropic models [VERIFIED]

**Code completion and context:**
- Windsurf Tab: Autocomplete (fast) and Supercomplete (multi-line diff suggestions) [VERIFIED]
- Fast Context: SWE-grep models, 20x faster retrieval than traditional search [VERIFIED]
- Knowledge Base: shared Google Docs as team knowledge (Teams/Enterprise) [VERIFIED]
- Remote Indexing: index remote repositories without local clone [VERIFIED]

**Pricing (as of June 2026):**
- Quota-based usage (replaced credits March 2026): daily and weekly token budgets [VERIFIED]
- Plans: Free, Pro ($15/mo), Max ($60/mo), Teams ($40/user/mo), Enterprise [ASSUMED prices]

**Enterprise:**
- Role Based Access Control (RBAC), Single Sign-On (SSO)/System for Cross-domain Identity Management (SCIM), FedRAMP, Analytics API [VERIFIED]
- Enterprise policies via Group Policy Object (GPO)/Mobile Device Management (MDM) [VERIFIED]

**Settings and configuration:**
- Cascade settings: many now in `settings.json` as `windsurf.*` keys (portable); some remain UI-only in `user_settings.pb` [VERIFIED]
- MCP config in `~/.codeium/windsurf/mcp_config.json` [VERIFIED]
- Hooks in `.devin/hooks.json` or `~/.codeium/windsurf/hooks.json`, 12 events [VERIFIED]

**Architecture internals:**
- Language server is a 166MB Go binary making direct HTTPS calls to Codeium APIs [TESTED 2026-05]
- Proxy detection disabled by default (`--detect_proxy=false`), controllable via `user_settings.pb` field 34 [TESTED 2026-05]
- MCP transport: NDJSON over stdio (JSON-RPC 2.0), protocol version `2025-11-25` [TESTED 2026-05]
- MCP tools receive ONLY tool_call arguments, zero system prompt leakage [TESTED 2026-05]
- HTTP_PROXY env vars break Cascade when detect_proxy=false (language server ignores proxy, connection fails) [TESTED 2026-05]

## Table of Contents

1. [Overview](#overview)
2. [Agent Harnesses](#agent-harnesses)
3. [Agent Command Center and Spaces](#agent-command-center-and-spaces)
4. [AI Models and Routing](#ai-models-and-routing)
5. [Windsurf Tab (Code Completion)](#windsurf-tab-code-completion)
6. [Context Awareness and Search](#context-awareness-and-search)
7. [Customization](#customization)
8. [Cascade Hooks](#cascade-hooks)
9. [MCP Integration](#mcp-integration)
10. [Developer Tools](#developer-tools)
11. [Pricing and Plans](#pricing-and-plans)
12. [Enterprise Features](#enterprise-features)
13. [Settings and Configuration](#settings-and-configuration)
14. [Architecture Internals](#architecture-internals-tested)
15. [Sources](#sources)
16. [Document History](#document-history)

## Overview

Windsurf is an AI-powered IDE built on VS Code Open Source Software (OSS), developed by Codeium. Settings, keybindings, and most VS Code extensions are compatible. VS Code and Cursor configurations can be imported during onboarding. [VERIFIED]

**Platform support:**
- **Windows** 10+
- **macOS** Yosemite+
- **Linux** Ubuntu 20.04+ (or glibc >= 2.31); other distributions glibc >= 2.28 [VERIFIED]

**Remote development:**
- **SSH** - Built-in implementation (not Microsoft's). Linux remote hosts only. [VERIFIED]
- **Dev Containers** - macOS, Windows, Linux. Local and remote (via SSH). Requires Docker. [VERIFIED]
- **Windows Subsystem for Linux (WSL)** - Beta support since v1.1.0. Requires pre-configured WSL on Windows. [VERIFIED]

**Windsurf Plugins:** Cascade agent also available as plugin for JetBrains (2023.3+), Visual Studio (17.5.5+), Neovim, Vim, Emacs, Xcode, Sublime Text, Eclipse. Devin Local only supported in Windsurf IDE and Devin CLI. [VERIFIED]

**Windsurf Next:** Pre-release channel with early access to new features. Opt-in download at windsurf.com/editor/download-next. [VERIFIED]

Windsurf provides two local agent harnesses (Cascade and Devin Local), an autonomous cloud agent (Devin Cloud), and a CLI agent (Devin for Terminal). Agents read/write files, run terminal commands, search the web, call MCP tools, and deploy apps. The Agent Command Center provides a unified Kanban view of all agent sessions.

**Key concepts:**
- **Agent harnesses** - Cascade (legacy, full feature set) and Devin Local (next-gen, 30% more efficient, subagents)
- **Adaptive Model Router** - Automatic model selection optimizing speed and capability
- **Windsurf Tab** - AI-powered code completion (Autocomplete and Supercomplete)
- **Fast Context** - SWE-grep models for rapid codebase search (20x faster than traditional)
- **Customization** - Rules, Workflows, Skills, AGENTS.md, and Memories
- **Quota system** - Daily/weekly token budgets replacing the old credit system (March 2026)

## Agent Harnesses

Windsurf provides two local agent harnesses that coexist in the IDE. Cascade is the legacy agent with the full feature set. Devin Local is the next-generation agent intended to eventually replace Cascade. Both share the same editor integration but differ in architecture, permissions, and supported features.

### Cascade (Legacy Local Agent)

Open Cascade: `Cmd/Ctrl+L` or click Cascade icon (top right). Selected text in editor/terminal auto-included.

**Modes**

Cascade offers three modes, switchable via toggle below input box or `Ctrl+.`:

- **Code Mode** - Full tool access. For complex features, refactoring, code generation. All tools enabled including file read/write, terminal, MCP, web search. Default mode. [VERIFIED]
- **Plan Mode** - Full tool access. For complex features requiring planning before coding. Type `megaplan` for advanced form with clarifying questions. Auto-switches to Code Mode when implementing. [VERIFIED]
- **Ask Mode** - Search tools only. For learning, planning, questions. Cannot modify files or run commands. [VERIFIED]

**Note**: "Chat Mode" from earlier documentation has been renamed to "Ask Mode". [VERIFIED]

**Capabilities**

- **Read/Write files** - View and modify source code
- **Run terminal commands** - Execute shell commands with permission controls
- **Web search** - `@web` for general search, `@docs` for curated docs, paste URLs
- **MCP integration** - Connect to external tools (GitHub, databases, APIs)
- **Tool calling** - Up to 20 tools per prompt; use "continue" button if stopped
- **Voice input** - Transcribe speech to text
- **Plans and Todo Lists** - Built-in planning agent for complex tasks
- **Queued Messages** - Queue new messages while Cascade works
- **Linter integration** - Auto-fix linting errors (free, no quota charge)
- **Image attachments** - Drag/drop or paste images into chat [VERIFIED]
- **Mermaid diagram support** - Renders Mermaid diagrams in chat [VERIFIED]
- **Git Worktree Support** - Spawn multiple sessions in same repo without conflicts [VERIFIED]
- **Multi-Cascade Panes and Tabs** - View sessions side-by-side or as dashboard [VERIFIED]

**Prompt Syntax (@-mentions and enrichments)**

**@-mentions** for referencing context:
- `@file` - Reference specific files
- `@skill-name` - Invoke a skill
- `@web` / `@docs` - Web/docs search
- `@terminal` - Reference terminal output
- `@conversation` - Reference previous conversations (retrieves relevant parts)
- `@codemap-name` - Reference a codemap

**Workflows:** `/workflow-name` runs workflow from `.devin/workflows/`

**Other enrichments:**
- **URL pasting** - Paste URLs directly, Cascade fetches content
- **Selected text** - Highlight in editor/terminal, then `Ctrl+L` to include
- **Image attachments** - Drag/drop or paste images into chat

**Checkpoints and Reverts**

- Hover over prompt > click revert arrow to restore codebase state
- Create named snapshots from within conversation
- **Warning**: Reverts are currently irreversible [VERIFIED]

**Real-time Awareness**

Cascade is aware of real-time user actions - no need to re-prompt context. Just say "Continue". [VERIFIED]

**Simultaneous Cascades**

Multiple Cascades can run simultaneously. Navigate via dropdown (top left of panel).
**Warning**: If two Cascades edit same file simultaneously, edits can race and fail. [VERIFIED]

**Auto-Execution Policies**

Four levels for command auto-execution:

- **Disabled** - All commands require manual approval
- **Allowlist** - Only allowlisted commands auto-execute (`windsurf.cascadeCommandsAllowList`)
- **Auto** - Model decides if safe (premium models only)
- **Turbo** - All commands auto-execute except denylist (`windsurf.cascadeCommandsDenyList`)

Enterprise admins can set a maximum auto-execution level for the organization. [VERIFIED]

**Auto-Continue**

When enabled, Cascade automatically continues when hitting per-response limit. Each continue consumes quota. [VERIFIED]

**Sharing Conversations**

Teams/Enterprise only: Click `...` > "Share Conversation" to share trajectories with team. Not yet available for Devin Local. [VERIFIED]

### Devin Local Agent (Next-Gen, Preview)

Devin Local is the next-generation local agent harness, shared with Devin CLI. Runs on user's machine with access to local files, tools, and environment. Currently in preview. **Intended to eventually replace Cascade as primary local agent.** [VERIFIED]

**Key Improvements Over Cascade**

- **Token efficiency** - 30% fewer tokens than Cascade for the same tasks, with greater focus on prompt caching [VERIFIED]
- **Subagents** - Can spawn independent subagents for subtasks, foreground or background. Share tools and codebase context with parent. [VERIFIED]
- **OS-level sandboxing** - Filesystem isolation (writable/readable paths from permission scopes) and network filtering (domain allowlists/denylists). Enterprise-enforceable. [VERIFIED]
- **Quick Review** - Dedicated subagent for rapid feedback on changes (see Section 10.4 Developer Tools) [VERIFIED]

**Permissions Model**

Replaces Cascade's auto-execution levels with fine-grained permissions:

- **Deny** rules - Block actions entirely (highest priority)
- **Ask** rules - Always prompt for approval
- **Allow** rules - Auto-approve without prompting

Scoped to: file reads, file writes, command execution, HTTP fetches, MCP tools. Configurable at project, user, or organization level. "Always Allow" grants now persist across sessions (since 2026.5.26). [VERIFIED]

**MCP Configuration (Devin Local)**

Different from Cascade's `mcp_config.json`:

- **Project**: `.devin/config.json` (checked into version control, shared with team)
- **Local override**: `.devin/config.local.json` (gitignored)
- **User**: `~/.config/devin/config.json` [VERIFIED]

**Limitations vs Cascade**

Not yet supported in Devin Local:

- **Memories** - Does not persist memories between sessions. Migrate to Skills.
- **Workflows** - Not available. Migrate to Skills.
- **Codemaps** - Does not read codemaps yet.
- **Code Lenses** - Do not trigger Devin Local.
- **Fast Context** - Uses subagents instead, no same UI as Cascade.
- **App Deploys** - Not supported.
- **Conversation Sharing** - Not yet available.
- **JetBrains** - Not supported in JetBrains plugin. [VERIFIED]

Devin Local DOES support: Rules, AGENTS.md files, Skills. [VERIFIED]

**Recent Updates (2026.5.26)**

- Aware of files open in editor as context
- MCP tool permission: server-level "approve all" options (session or permanent)
- Repaired hooks for blocking user prompts
- Plan mode works in OS sandbox
- "Always Allow" persists across sessions
- Image attachment warnings for unsupported models [VERIFIED]

**Enterprise Controls (Devin Local)**

- **Sandbox enforcement** - Require sandbox mode for all users, configure org-wide domain filtering
- **Granular permissions** - Fine-grained action control
- **Network enforcement** - Allowed/denied domain lists
- **Disable Cascade** - Force team to use Devin Local exclusively [VERIFIED]

### Devin Cloud (Autonomous Cloud Agent)

Devin Cloud is an autonomous software engineering agent running on its own Virtual Machine (VM) with desktop, browser, and computer use. Works asynchronously - continues after user closes laptop. Delivers Pull Requests. [VERIFIED]

**Availability**

- Included with every self-serve Windsurf plan (Pro, Max, Teams) [VERIFIED]
- Enterprise: disabled by default, admin must enable from organization settings [VERIFIED]
- Rolling out gradually; requires GitHub connection [VERIFIED]
- First-time users get up to $50 in extra usage for trying Devin [VERIFIED]

**Delegation Workflow**

1. Plan locally with Cascade or Devin Local
2. One-click delegation to Devin Cloud
3. Devin spins up its own VM and works independently
4. Review Devin changes and test results in-editor via Agent Command Center
5. Devin sessions appear alongside local sessions in Kanban view [VERIFIED]

**In-Editor PR Review**

Devin Cloud Pull Requests can be reviewed directly in the Windsurf editor. Open the PR, review changes, and request modifications without leaving the IDE. [VERIFIED]

**Pricing**

- Self-serve: Devin Cloud directly consumes shared Windsurf quota and extra usage balance [VERIFIED]
- No separate billing; same token-based system as Cascade [VERIFIED]

### Devin for Terminal (CLI Agent)

Devin CLI agent available for all Windsurf users with existing subscription:

- Runs on user's machine with full codebase/tools access
- Can hand off to Devin Cloud seamlessly
- Multi-model: Opus 4.7, GPT-5.5, SWE-1.6
- Written in Rust, high performance
- Sessions accessible from both Windsurf IDE and CLI
- Available at https://devin.ai/terminal [VERIFIED]

### Agent Selector

Agent selector in bottom-right corner of Windsurf when starting new conversations. Enterprise admins can disable legacy Cascade entirely via "Enable Cascade" control. [VERIFIED]

## Agent Command Center and Spaces

### Agent Command Center (Kanban View)

A unified surface introduced in Windsurf 2.0 for managing every agent - local and cloud - from one place. Organized as a Kanban board grouped by status, showing what each agent is working on, what is blocked, and what is ready for review. [VERIFIED]

Agent columns:
- **Local agents** - Cascade sessions running in the editor
- **Cloud agents** - Devin sessions running on their own VMs

Also supports list display option (added post-2.0). [VERIFIED]

The Agent Command Center does not replace the editor. Integrated with existing Windsurf editor features for jumping back into a session and making last-mile edits manually. [VERIFIED]

Recent improvements:
- List display option for agent inbox [VERIFIED]
- Improved sessions sidebar sorting and filtering [VERIFIED]
- Performance improvements for loading and switching sessions [VERIFIED]

### Spaces (Task Grouping)

Spaces group everything related to a specific task or project into a single view:

- **Agent sessions** - Local Cascade sessions and cloud Devin sessions
- **Pull requests** - PRs opened by user or agents
- **Files** - Files relevant to the task
- **Context** - Project-level context inherited by new sessions [VERIFIED]

**Context sharing**: New sessions in a Space inherit everything the Space already knows. New agents can start working immediately without re-explanation. [VERIFIED]

**Switching**: View is restored exactly as left it. Switching Spaces = switching tasks. [VERIFIED]

**Creating a Space** (three methods):
- **Drag session onto session** - In sidebar, drag to group as Space
- **Split pane** - `Cmd/Ctrl+\` to split, then "New Session" in empty pane
- **Keyboard shortcut** - `Cmd/Ctrl+T` opens new session in current Space [VERIFIED]

**Default behavior**: Every session is its own Space by default, even if not shown as one. No need to create a Space to start working - group sessions whenever useful. [VERIFIED]

## AI Models and Routing

### SWE Model Family (In-house)

Cognition's in-house models built specifically for software engineering:

- **SWE-1.6** - Latest model, optimized for intelligence and model UX. Uses parallel tool calls more often, loops less, relies more on its own tools than terminal. [VERIFIED]
- **SWE-1.6 Fast** - Same intelligence, unmatched speed and cost. Paying users only. [VERIFIED]
- **SWE-1.5** - Previous frontier agentic coding model. Near Claude 4.5-level performance at 13x the speed. **Free model.** [VERIFIED]
- **SWE-1** - First agentic coding model. Claude 3.5-level performance at fraction of cost. [VERIFIED]
- **SWE-1-mini** - Powers Windsurf Tab passive suggestions, optimized for real-time latency. [VERIFIED]
- **swe-grep / swe-grep-mini** - Powers context retrieval and Fast Context. Up to 2,800 tokens/sec. RL-trained for parallel tool calling. [VERIFIED]
- **SWE-check** - Quick Review model for code review. Free for all tiers. [VERIFIED]

### Third-Party Models (as of June 2026)

**Anthropic:**
- Claude Opus 4.8 / Claude Opus 4.8 Fast Mode [VERIFIED]
- Claude Opus 4.7 / 4.7 Fast Mode (~2.5x higher output speed) [VERIFIED]
- Claude Sonnet 4.6, Opus 4.6 / 4.6 Fast Mode, Sonnet 4.5

**OpenAI:**
- GPT-5.5, GPT-5.4 / GPT-5.4 Mini [VERIFIED]
- GPT-5.2-Codex / GPT-5.1-Codex / GPT-5.1-Codex Max
- o4-mini

**Google:**
- Gemini 3.1 Pro / Gemini 3 Pro / Gemini 3 Flash

**Other:**
- Grok Code Fast, GLM-5, Minimax M2.5
- DeepSeek-R1 / DeepSeek-V3
- Falcon Alpha [VERIFIED]

**Note**: For the most up-to-date pricing, refer to the model selector in Windsurf IDE. [VERIFIED]

### Adaptive Model Router

Intelligent model router that automatically selects the best AI model for each task. Evaluates each request and dynamically routes: simple tasks to fast/efficient models, complex tasks to more capable ones. [VERIFIED]

**Pricing (self-serve, introductory through 2026-06-07):**
Fixed per-token rate regardless of underlying model:
- Input: $0.50/M tokens
- Output: $2.00/M tokens
- Cache read: $0.10/M tokens

Typically consumes fewer tokens overall than manual frontier model selection. [VERIFIED]

**Enterprise pricing:**
- **Cognition Platform**: Agent Compute Unit (ACU) consumption scales with tokens and model selected
- **Legacy Credits**: Variable-token credit pricing, cheaper models cost fewer credits [VERIFIED]

**Tips:**
- Be specific with prompts for better routing
- Stay on same model across turns for caching
- Use as default; switch manually only when needed [VERIFIED]

### Arena Mode

Two models respond to same prompt simultaneously, anonymously. User chooses the better response. Model identities revealed after voting. [VERIFIED]

- **Battle Groups** - Models paired in groups. Each prompt picks a pair from the group. [VERIFIED]
- **Quota cost** - User is charged for the more expensive of the two models. [VERIFIED]
- **Limitations** - Cannot be used for Plan Mode. Some models may not support Arena pairing. [VERIFIED]

Access via Arena tab in model picker.

### Model Picker

- Groups models by family with hovercards
- Toggles for variants (reasoning effort, speed)
- Pin favorite models for quick access [VERIFIED]

### Bring Your Own Key (BYOK)

- Available only to free and paid individual users (not Teams/Enterprise)
- Currently supported models: Claude 4 Sonnet / Claude 4 Sonnet (Thinking), Claude 4 Opus / Claude 4 Opus (Thinking)
- API key configured at: https://windsurf.com/subscription/provider-api-keys [VERIFIED]

### Model Switching and Context Window [TESTED 2026-01-26]

**Note**: Behavior below was tested with Cascade. Devin Local model switching behavior may differ. [ASSUMED]

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
[Model CAN be changed for NEXT turn]
```

## Windsurf Tab (Code Completion)

Windsurf Tab is a contextually aware diff-suggestion and navigation engine powered by SWE-1-mini (custom in-house model optimized for real-time latency). [VERIFIED]

### Autocomplete vs Supercomplete

- **Supercomplete** (recommended, default) - Appears in small windows around cursor to suggest both deletions and additions. Most powerful mode. [VERIFIED]
- **Autocomplete** - Traditional inline completion at cursor position. Simpler, familiar interface. [VERIFIED]

### Tab to Jump

Anticipates next cursor position and prompts with a "Tab to Jump" label at a certain line. Press Tab to navigate there. Avoids manual scrolling/clicking to next edit location. [VERIFIED]

### Tab to Import

After defining a new dependency in a file, press Tab to auto-import it at file top. Cursor stays in same position. [VERIFIED]

### Context Sources

Windsurf Tab is broadly context-aware:
- Current file and open files
- Recent terminal activity
- Recent code changes
- Clipboard contents (opt-in via Settings)
- Cascade chat history [VERIFIED]

### Keyboard Shortcuts

- **Accept suggestion**: `Tab`
- **Cancel suggestion**: `Esc`
- **Accept word-by-word**: `Cmd+Right` (VS Code) / `Alt+Shift+\` (JetBrains) [VERIFIED]

### Settings

All features individually configurable:
- Autocomplete vs Supercomplete mode toggle
- Clipboard as context opt-in
- Tab to Import on/off
- Tab to Jump on/off [VERIFIED]

## Context Awareness and Search

### Default Context

Out-of-the-box context sources:
- **Current file and open files** - Most relevant code
- **Entire local codebase** - Indexed (including files not open), relevant snippets sourced by retrieval engine
- **Pro users** - Expanded context lengths, increased indexing limits, higher limits on custom/pinned context
- **Teams/Enterprise** - Remote repository indexing [VERIFIED]

### Fast Context

Specialized subagent that retrieves relevant code from codebase up to 20x faster than traditional agentic search. Powers Cascade's ability to quickly understand large codebases. [VERIFIED]

How it works:
1. Triggers automatically when Cascade receives a query requiring code search
2. Uses SWE-grep and SWE-grep-mini models
3. Identifies relevant files and code sections using parallel tool calls
4. Executes multiple searches simultaneously
5. Returns targeted results in seconds rather than minutes

Prevents context pollution. Conserves context budget for actual task. [VERIFIED]

**SWE-grep models:**
- **SWE-grep** - High-intelligence variant for complex retrieval
- **SWE-grep-mini** - Ultra-fast, 2,800+ tokens/sec

Both RL-trained. Execute up to 8 parallel tool calls per turn over max 4 turns. Use restricted cross-platform tools (grep, read, glob). [VERIFIED]

**Devin Local note:** Devin Local uses subagents instead of Fast Context and lacks the same Fast Context UI. [VERIFIED]

### Knowledge Base (Beta)

- Teams and Enterprise only
- Pull in Google Docs as shared context for entire team
- Only Google Docs supported (not images, but charts/tables/formatted text supported)
- Admin connects Google Drive via OAuth, adds up to 50 docs
- All team members have access regardless of individual Google Drive ACLs
- Cascade accesses docs specified in Windsurf dashboard [VERIFIED]

### Remote Indexing

- Teams and Enterprise only
- Index remote repositories that developers work across
- Security guarantees maintained [VERIFIED]

### Web and Docs Search

- `@web` - General web search
- `@docs` - Curated documentation search
- Paste URLs directly into chat - Cascade fetches and parses content

Cascade browses the internet as a human would. Web tools designed to get only necessary information for efficient quota usage. Can parse and chunk web pages and documentation for real-time context. [VERIFIED]

### Windsurf Ignore

- `.codeiumignore` file using gitignore-style syntax
- Prevents Cascade from reading/indexing specific files
- Global file: `~/.codeium/windsurf/.codeiumignore`
- `windsurf.allowCascadeAccessGitignoreFiles` setting controls access to gitignored files [VERIFIED]

## Customization

Windsurf provides five mechanisms for customizing agent behavior. Skills are the only mechanism working across both Cascade and Devin Local.

### Decision Guide

- **Memories** - Automatically remembered context, quick manual notes
- **Rules** - Persistent coding style, project conventions, behavioral constraints
- **Workflows** - Step-by-step procedures, repeatable processes
- **Skills** - Complex multi-step tasks requiring templates, scripts, supporting files
- **AGENTS.md** - Directory-scoped instructions [VERIFIED]

### Rules

Persistent instructions that Cascade follows every time. Set coding style, project conventions, behavioral constraints. [VERIFIED]

**Storage locations (rules discovery):**
1. **Global rules**: `~/.codeium/windsurf/memories/global_rules.md` (single file, always on, 6,000 char limit) [VERIFIED]
2. **Workspace rules**: `.devin/rules/*.md` (one file per rule, 12,000 chars per file) [VERIFIED]
3. **AGENTS.md**: Directory-scoped rules (see below). Root-level = always-on, subdirectory = auto-glob for that directory [VERIFIED]
4. **System-level** (Enterprise): OS-specific paths (e.g. `/etc/windsurf/rules/`), read-only for end users [VERIFIED]

Windsurf searches `.devin/rules/` in the current workspace, sub-directories, and parent directories up to git root. Multiple workspaces: rules deduplicated, shown with shortest relative path. [VERIFIED]

**Activation modes (frontmatter `trigger` field):**

Each workspace rule declares an activation mode via YAML frontmatter. Controls when the rule reaches Cascade and how much context window it consumes:

- **Always On** (`trigger: always_on`) - Full rule content in system prompt on every message. Highest context cost. [VERIFIED]
- **Model Decision** (`trigger: model_decision`) - Only `description` field shown in system prompt. Cascade reads full rule when it decides description is relevant. [VERIFIED]
- **Glob** (`trigger: glob`) - Applied when Cascade reads or edits files matching the `globs` pattern (e.g. `*.js`, `src/**/*.ts`). Context cost only when matching files touched. [VERIFIED]
- **Manual** (`trigger: manual`) - Not in system prompt. Activated by typing `@rule-name` in Cascade input. Zero context cost until invoked. [VERIFIED]

Global rules and root-level AGENTS.md don't use frontmatter - always on. [VERIFIED]

**Example workspace rule file:**

```markdown
---
trigger: glob
globs: **/*.test.ts
---

All test files must use describe/it blocks and mock external API calls.
```

**Best practices:**
- Keep rules simple, concise, specific. Too long or vague rules confuse Cascade.
- Use bullet points and markdown formatting (easier than long paragraphs)
- No need for generic rules ("write good code") - already in Cascade's training
- Example templates: windsurf.com/editor/directory [VERIFIED]

**System-level rules (Enterprise):** Enterprise admins push rules to all team members via cloud dashboard. System rules cannot be overridden by workspace rules. [VERIFIED]

### Workflows

Step-by-step procedures defined as markdown files. Cascade follows them when invoked via `/workflow-name` slash command. [VERIFIED]

**Storage locations:**
1. **Workspace**: `.devin/workflows/*.md`
2. **System-level** (Enterprise): Cloud dashboard [VERIFIED]

**Format:**
```yaml
---
description: [short title]
---
[specific steps]
```

**Precedence (Enterprise):** System-level workflows override workspace workflows with same name. [VERIFIED]

**Generate with Cascade:** Ask Cascade to create a workflow and it will generate the `.md` file automatically. [VERIFIED]

**Devin Local compatibility:** Workflows are NOT supported with Devin Local. Migrate workflows to Skills for compatibility. [VERIFIED]

### Skills

Bundles for complex, multi-step tasks. Include `SKILL.md` description plus supporting files (templates, scripts, checklists, reference data). [VERIFIED]

**Creation:**
- **UI method**: Windsurf Settings > Skills (easiest)
- **Manual**: Create `SKILL.md` in `.devin/skills/<skill-name>/` or `.agents/skills/<skill-name>/` [VERIFIED]

**SKILL.md format:**
```yaml
---
description: [description for automatic invocation matching]
---
[instructions and steps]
```

Required frontmatter field: `description`. [VERIFIED]

**Supporting resources:** Additional files in skill folder are referenced by SKILL.md. Templates, scripts, checklists, data files. [VERIFIED]

**Invocation:**
- **Automatic** - Cascade matches task to skill description
- **Manual** - `@skill-name` in chat [VERIFIED]

**Skill scopes:**
1. **Project**: `.devin/skills/<name>/` or `.agents/skills/<name>/`
2. **System-level** (Enterprise): Cloud dashboard [VERIFIED]

**Skills vs Rules vs Workflows:**
- **Rules**: Simple behavioral constraints. Always active or conditional. No files.
- **Workflows**: Step-by-step procedures. Single file. Invoked via slash command.
- **Skills**: Complex tasks. Multiple files. Auto-matched or manually invoked. [VERIFIED]

**Devin Local compatibility:** Skills ARE supported with Devin Local. Skills are the universal customization mechanism across both agent harnesses. Devin Local also supports Devin CLI skill format. [VERIFIED]

### AGENTS.md

Directory-scoped instruction files. Similar to Cursor's `.cursorrules` but with directory scoping. [VERIFIED]

**Discovery and scoping:**
- Placed in any directory
- Cascade automatically discovers and applies them
- Instructions scoped to files within that directory (and subdirectories)
- Multiple AGENTS.md files can coexist at different directory levels [VERIFIED]

**Format:**
```markdown
# Purpose
Description of the directory's purpose

# Guidelines
- Coding conventions
- Architecture patterns
```

**Comparison with Rules:**
- **Rules**: Global or workspace-wide. Settings-based. For project-level conventions.
- **AGENTS.md**: Directory-scoped. File-based. For directory-specific patterns. [VERIFIED]

**Devin Local compatibility:** AGENTS.md IS supported with Devin Local. [VERIFIED]

### Memories

Cascade auto-generates memories during conversation when it encounters context it believes is useful to remember. User can also prompt "create a memory of ..." at any time. [VERIFIED]

**Storage and scoping:**
- Stored locally in `~/.codeium/windsurf/memories/`
- Workspace-scoped: memories from one workspace not available in another
- Not committed to repository
- Retrieved automatically when Cascade believes they are relevant
- Creating and using memories does NOT consume quota [VERIFIED]

**Management:** Windsurf Settings > Memories (via Customizations icon in Cascade top right). Review, edit, delete auto-generated memories. [VERIFIED]

**Recommendation:** For durable, shared knowledge, prefer Rules (`.devin/rules/`) or AGENTS.md over auto-generated memories. Rules are version-controlled, shareable, and give explicit activation control. [VERIFIED]

**Devin Local compatibility:** Memories are NOT supported with Devin Local. Migrate critical memories to Skills. [VERIFIED]

## Cascade Hooks

Shell scripts that run before/after Cascade actions. Enable logging, access control, formatting, automation. [VERIFIED]

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

- **pre_read_code** / **post_read_code** - Before/after reading code
- **pre_write_code** / **post_write_code** - Before/after writing code
- **pre_run_command** / **post_run_command** - Before/after terminal commands
- **pre_mcp_tool_use** / **post_mcp_tool_use** - Before/after MCP tool calls
- **pre_user_prompt** - Before user prompt (can block)
- **post_cascade_response** - After Cascade response
- **post_cascade_response_with_transcript** - After response with full transcript
- **post_setup_worktree** - After worktree setup [VERIFIED]

### Input and Exit Codes

All hooks receive JSON via stdin with event type, file paths, command details. [VERIFIED]

Exit codes:
- **0** - Allow action
- **Non-zero** - Block action (for pre-* hooks) [VERIFIED]

### Example Use Cases

- Logging all Cascade actions
- Restricting file access
- Blocking dangerous commands
- Blocking policy-violating prompts
- Running code formatters after edits
- Setting up worktrees
- Tracking triggered rules (`rules_applied` field) [VERIFIED]

### Enterprise Distribution

- **Cloud Dashboard** - Push hooks to all team members
- **System-level file deployment** - Deploy via filesystem
- **Workspace hooks** - Include in project repo [VERIFIED]

### Devin Local Hooks

Hooks repaired for Devin Local to allow blocking user prompts (2026.5.26). [VERIFIED]

## MCP Integration

Windsurf supports Model Context Protocol (MCP) for connecting agents to external tools and services. [VERIFIED]

### Adding MCP Servers

**One-click install:** Install MCP plugins via deeplink URLs. Click install link and server is added to config automatically. [VERIFIED]

**Manual configuration:** Edit `mcp_config.json`:
- Windows: `%USERPROFILE%\.codeium\windsurf\mcp_config.json`
- macOS/Linux: `~/.codeium/windsurf/mcp_config.json`

Individual tools from MCP servers can be enabled/disabled. [VERIFIED]

### Config Format

```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-name"],
      "env": {
        "API_KEY": "${env:API_KEY}"
      }
    }
  }
}
```

### Transport Types

- **stdio** - Local process, communicates via stdin/stdout (default)
- **SSE** - Server-Sent Events over HTTP
- **Remote HTTP** - HTTP endpoint with optional auth headers [VERIFIED]

### Config Interpolation

Environment variables supported with `${env:VARIABLE_NAME}` syntax. [VERIFIED]

### Admin Controls (Teams and Enterprise)

**MCP Registry:** Admins can pre-configure a registry of approved MCP servers that appear in the IDE for easy installation. [VERIFIED]

**MCP Whitelist:** Regex-based whitelist to control which MCP servers can be used. Server names and commands matched against regex patterns. Configuration options: allow all, deny all, or selective patterns. [VERIFIED]

### Devin Local MCP Configuration

Different from Cascade's `mcp_config.json`:

- **Project**: `.devin/config.json` (version-controlled)
- **Local override**: `.devin/config.local.json` (gitignored)
- **User**: `~/.config/devin/config.json`

MCP tool permissions in Devin Local offer server-level "approve all" (session or permanent). [VERIFIED]

### OAuth Support

MCP servers supporting OAuth can authenticate automatically. [VERIFIED]

## Developer Tools

### Terminal

- **Command execution** - Cascade runs terminal commands with auto-execution policies
- **Send terminal selection to Cascade** - Select text in terminal, send to chat
- **@-mention terminal** - Reference terminal output in Cascade prompts
- **Command in Terminal** - Type Windsurf command in terminal with inline suggestions
- **Dedicated Terminal** - Beta. Separate terminal profile for agent execution, preventing interference with user's terminal sessions. [VERIFIED]

Enterprise controls: Admin-controlled maximum auto-execution level. Team-wide allowlist and denylist configuration. [VERIFIED]

### Windsurf Previews

Preview web apps locally in IDE or browser with element selection, error capture, and Cascade integration. Optimized for Chrome, Arc, and Chromium-based browsers. [VERIFIED]

- **In-IDE Preview** - Web app view as editor tab
- **Send Elements to Cascade** - Select UI elements and send as @-mention
- **Error capture** - Console errors can be sent to Cascade
- **Tool call activation** - Ask Cascade to preview, or click Web icon in toolbar [VERIFIED]

### Vibe and Replace

AI-powered evolution of find-and-replace. Search codebase for exact text matches, apply AI prompt to each replacement. For context-aware transformations and refactors. [VERIFIED]

Modes:
- **Smart** - Slower model, applies changes more carefully
- **Fast** - Faster model, applies changes quickly

Mode selected via dropdown next to prompt box. [VERIFIED]

### Quick Review (Devin Local)

Agentic code review on local changes. Only available with Devin Local agent (not legacy Cascade). Independent second opinion by separate review agent. [VERIFIED]

Available models:
- **SWE-check** - Fast, lightweight, free for all tiers
- **GPT 5.5** - Deep agentic review, token-based pricing
- **Opus 4.7** - Deep agentic review, token-based pricing [VERIFIED]

Enterprise: Admin must enable Quick Review from team settings. Can control which review models are available. [VERIFIED]

**Devin Review** (separate from Quick Review): Available for all self-serve users with 2-week free trial. Enterprise requires Cognition platform agreement. [VERIFIED]

### Codemaps

Visual architecture diagrams of code structure. Created and shared in Windsurf. Referenced by Cascade via `@codemap-name`. Devin Local does not yet read Codemaps. [VERIFIED]

### App Deploys

Deploy web apps directly from Windsurf to Netlify. Cascade tool call. Creates public URLs, automatic builds, project claiming. Beta. Supports Next.js, React, Vue, Svelte, and more. Not supported with Devin Local. [VERIFIED]

### DeepWiki

AI-powered explanations of code symbols, implemented from Devin's DeepWiki feature. Located in Primary Side Bar / Activity Bar. [VERIFIED]

Usage:
- Hover over symbol > `Cmd+Shift+Click` for detailed explanation
- Explains functions, variables, classes beyond basic type info
- Send explanations to Cascade via `...` menu > "Add to Cascade" [VERIFIED]

### AI Commit Messages

Auto-generated commit messages based on staged changes. [VERIFIED]

### Worktrees

Git worktree support for working on multiple branches simultaneously. Each worktree has its own directory and working tree. Worktrees visible in Source Control panel. `post_setup_worktree` hook event for configuring worktree environment (install deps, setup env files). [VERIFIED]

### Other Developer Tools

- **Diff Zones** - Agent-controlled code regions where Cascade makes edits. Visual indicators show which code sections are being modified. [VERIFIED]
- **Explain and Fix** - Highlight error in Problems panel or editor > "Explain and Fix" to have Cascade resolve. [VERIFIED]
- **Code Lenses** - Inline actions above functions: Explain, Refactor, Add Docstring. Click to trigger Cascade. Not yet supported with Devin Local. [VERIFIED]
- **Smart Paste** - Context-aware paste that adapts content to target location. [VERIFIED]
- **Send Problems to Cascade** - Problems panel > "Send to Cascade" button to include as @-mention. [VERIFIED]

## Pricing and Plans

Windsurf replaced credits with a quota-based usage system in March 2026. [VERIFIED]

### Quota-Based Usage

- Plan includes daily and weekly usage allowance
- Budget based on tokens consumed per request
- Cost per token varies by model
- Free models (SWE-1.5) don't count against quota
- Daily quota > 1/7 of weekly quota (allows weekend heavy use) [VERIFIED]

**When quota exhausted:**
- **Free**: Wait for daily or weekly reset
- **Pro/Max/Teams**: Purchase extra usage to continue [VERIFIED]

**Checking quota:**
- Usage meter in Windsurf IDE (status bar > "Windsurf Settings" > "Plan Info")
- Web: windsurf.com/subscription/manage-plan [VERIFIED]

### Plan Tiers

- **Free** - Limited daily/weekly quota, free models only (SWE-1.5), wait for reset when exhausted
- **Pro** - $15/month, expanded quota, access to all models, extra usage available
- **Max** - $60/month, highest individual quota, all models, extra usage
- **Teams** - $40/user/month, team management, Knowledge Base, Remote Indexing, shared analytics, RBAC
- **Enterprise** - Custom pricing (Agent Compute Unit/ACU or legacy credit based), SSO/SCIM, FedRAMP, system-level controls

**Note**: Prices from training data. Check windsurf.com/pricing for current rates. [ASSUMED prices]

### Making Quota Last

- Be precise, remove unnecessary context
- Switch to free models (SWE-1.5) for routine tasks
- Avoid unnecessarily long sessions
- Use single frontier model per task for caching benefits [VERIFIED]

### Enterprise Billing

- **Cognition Platform (ACUs)** - Agent Compute Units, model usage converted to ACUs
- **Legacy Credits** - Credit-based system, being phased out
- **Credit cap configuration** - Admins can set per-user or per-group caps via admin portal or Analytics API [VERIFIED]

### Seat Rotation

If a team member leaves mid-cycle and a new member takes the seat, the new member inherits remaining credits. Full reset at next billing cycle start. [VERIFIED]

## Enterprise Features

### Admin Portal and Team Setup

- Admin portal at windsurf.com/team/settings
- User management with role assignment
- User groups for bulk operations
- Quota allocation and caps per user/group [VERIFIED]

### Role Based Access Control (RBAC)

**Roles:**
- Built-in roles (Admin, Member, etc.)
- Custom roles with granular permissions
- Administrative hierarchy [VERIFIED]

**Permissions (modifiable per role):**
- Model access
- Feature access (Cascade, Tab, MCP, etc.)
- Auto-execution levels
- **Disable Windsurf Access** feature for restricting users entirely [VERIFIED]

**User Groups:** Organize users into groups for bulk permission management. [VERIFIED]

### SSO and SCIM

Multiple SSO providers supported:
- Azure AD / Entra ID
- Google Workspace
- Okta
- OneLogin
- Generic OIDC / SAML

SCIM provisioning for automated user lifecycle management. [VERIFIED]

### Enterprise Policies (GPO/MDM)

- **Windows Group Policies (GPO)** - ADMX/ADML files for managing Windsurf via Group Policy. Controls extension management. [VERIFIED]
- **macOS Configuration Profiles** - Sample .mobileconfig for MDM deployment. [VERIFIED]
- **Linux JSON Policies** - JSON-based policy files for Linux deployment. [VERIFIED]
- **Extension Management** - AllowedExtensions whitelist. Server-driven extension deny lists supported. [VERIFIED]

### FedRAMP

FedRAMP Security Admin Guide available. Includes administrative role definitions, permission reference, admin account lifecycle procedures, authentication and MFA requirements, security settings reference. [VERIFIED]

### Analytics API

**Built-in analytics:** Dashboard for individuals and teams showing usage, productivity metrics. [VERIFIED]

**API endpoints:**
- **Get Cascade Analytics** - cascade_lines, cascade_runs, cascade_tool_usage
- **Custom Analytics Query** - Flexible query with selections, filters, aggregations
- **Get Team Credit Balance** - Current credit balance
- **Get/Set Usage Configuration** - Per-user caps, per-group caps
- **Get User Page Analytics** - Per-user analytics [VERIFIED]

**Authentication:** Service Keys with required permissions. Rate limits enforced. [VERIFIED]

### Domain Verification

- Verify domain in Windsurf admin
- With SSO: users auto-join team on signup
- Without SSO: users auto-join on login [VERIFIED]

## Settings and Configuration

### Directory Structure (Windows)

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

### Two Settings Systems

Windsurf uses **two different systems** for storing settings:

- **Editor settings** - Format: JSON. Location: `%APPDATA%\Windsurf\User\settings.json`. Editable via text editor.
- **Cascade settings** (UI-only subset) - Format: Protobuf binary. Location: `%USERPROFILE%\.codeium\windsurf\user_settings.pb`. Editable via Windsurf Settings UI only. Many settings now also writable via `windsurf.*` keys in `settings.json`.

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

### Working with Private/Gitignored Folders

Cascade can read/write gitignored files when explicitly referenced, but gitignored folders are hidden from the workspace snapshot shown at conversation start.

**To make a gitignored folder visible to Cascade while keeping contents private:**

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
echo "# This file makes the folder visible to Cascade" > _PrivateSessions/.gitkeep
```

**How it works:**
- `_PrivateSessions/*` - Ignores all files/folders inside
- `!_PrivateSessions/.gitkeep` - Negation pattern, tracks this specific file
- Result: Folder appears in workspace, contents stay private

### Key Files Reference

**User Config:**
- `settings.json` - Editor preferences (JSON, editable)
- `keybindings.json` - Keyboard shortcuts
- `user_settings.pb` - Cascade UI settings (protobuf, UI-only)
- `state.vscdb` - Window/extension state (SQLite)
- `mcp_config.json` - MCP server configurations
- `~/.codeium/windsurf/hooks.json` - User-level Cascade hooks

**Workspace Config:**
- `.codeiumignore` - Files Cascade should ignore
- `.devin/workflows/*.md` - Custom workflows
- `.devin/rules/*.md` - Project rules for Cascade
- `.devin/skills/*/SKILL.md` - Skills with supporting resources
- `.devin/hooks.json` - Workspace-level Cascade hooks
- `AGENTS.md` - Directory-scoped instructions

**Devin Local Config:**
- `.devin/config.json` - Project MCP and permissions (version-controlled)
- `.devin/config.local.json` - Local override (gitignored)
- `~/.config/devin/config.json` - User-level config

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
  --api_server_url https://server.self-serve.devin.com
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
  --extensions_dir <user_home>\.devin\extensions
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

- `https://server.self-serve.devin.com` - Primary API (auth, settings, telemetry, user data)
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

- **DevTools Network Tab** - Cannot capture. Extension host traffic in separate process. [ASSUMED]
- **MCP Server Observer** - Cannot capture. Only sees tool_call arguments, not prompt. [TESTED]
- **HTTP Proxy (env vars)** - Cannot capture. `detect_proxy=false` causes Cascade to break. [TESTED]
- **HTTP Proxy (detect_proxy=true)** - [Not yet tested as of 2026-05]
- **SSLKEYLOGFILE** - [Not yet tested as of 2026-05]. Go binary unlikely to honor (requires explicit `tls.Config.KeyLogWriter`).
- **mitmproxy local mode (WinDivert)** - [Not yet tested as of 2026-05]. Network-level capture, still needs MITM cert trust.

### Next Steps for Exact Prompt Capture

1. **Enable `detect_proxy=true`** via Windsurf Settings UI, install mitmproxy CA cert in Windows trust store, retry proxy interception
2. **Named pipe interception**: Monitor `\\.\pipe\server_*` for protobuf messages between extension and language server
3. **Process memory dump**: Search language server process memory for prompt content after Cascade interaction

## Sources

### Deep Research (Comprehensive Review, 2026-06-01)

Source IDs reference `_INFO_WSFT-02_Sources.md [WSFT-IN02]` in session `_2026-06-01_WindsurfFeatureResearch`.

**Primary source**: https://docs.devin.com/llms-full.txt (full documentation export, accessed 2026-06-01)

**Official documentation (34 sources)**: Cascade overview, modes, models, Adaptive router, Tab completion, Fast Context, context awareness, MCP, rules, workflows, skills, hooks, Devin Cloud, Devin Local, Agent Command Center, Spaces, Quick Review, Vibe and Replace, Previews, Terminal, Codemaps, Worktrees, Arena Mode, AGENTS.md, App Deploys, web search, quota, RBAC, DeepWiki, FedRAMP, Analytics API, Enterprise Policies. All from docs.devin.com.

**Changelog**: https://windsurf.com/changelog (Windsurf Editor and Windsurf Next, accessed 2026-06-01)

### Previous Research and Testing

- https://docs.devin.com/windsurf/cascade/cascade - Cascade documentation [TESTED 2026-01-13]
- Session `_2026-01-26_AutoModelSwitcher` - Model switching and context window research [TESTED]
- Session `_2026-05-27_CascadeMetapromptExtraction/S03_CSMP-ExtractionTesting_2026-05-27` - Binary analysis, process inspection, interception testing [TESTED 2026-05]
- `Win32_Process.CommandLine` inspection of `language_server_windows_x64.exe` [TESTED 2026-05]
- String analysis of Go binary (166MB) for proxy, TLS, and protocol strings [TESTED 2026-05]
- `extension.js` (9.4MB) regex-based deobfuscation of spawn logic, settings watcher, proxy detection [TESTED 2026-05]
- MCP observer tool (custom NDJSON JSON-RPC 2.0 server) confirming transport protocol [TESTED 2026-05]
- mitmproxy 12.2.3 interception testing (proxy mode) confirming language server proxy behavior [TESTED 2026-05]
- Local file system investigation (2026-01-11)
- Agent Skills Specification: https://agentskills.io/

## Document History

**[2026-06-02]**
- Added: Overview section enriched with VS Code OSS base, platform support (Win/Mac/Linux with min versions), remote development (SSH/Dev Containers/WSL), Windsurf Plugins availability, Windsurf Next channel (from docs.devin.com)
- Added: Rules section enriched with 4 activation modes (was 2), frontmatter trigger format, character limits, glob example, discovery details, best practices (from docs.devin.com)
- Added: Memories section enriched with storage location, workspace scoping, no-quota-cost, explicit creation prompt, recommendation to prefer Rules
- Fixed: Acronyms expanded on first use (MCP, CLI, VM, PR, SCIM, IDE, ACU)
- Fixed: 17 H4 headings converted to bold paragraph headers (MW-HS-02 max 3 levels)
- Fixed: Non-standard [UPDATED] label replaced with [VERIFIED]
- Fixed: Locale-dependent date "June 7, 2026" changed to "2026-06-07"
- Changed: Complete document restructure from deep research session `_2026-06-01_WindsurfFeatureResearch`
- Added: Sections 1-13 rewritten with comprehensive content from 14 research topic files
- Added: Agent Harnesses section (Cascade, Devin Local, Devin Cloud, Devin Terminal, Agent Selector)
- Added: Agent Command Center and Spaces section
- Added: AI Models (SWE family, third-party, Adaptive router, Arena Mode, BYOK)
- Added: Windsurf Tab section (Autocomplete, Supercomplete, Tab to Jump/Import)
- Added: Context Awareness (Fast Context, Knowledge Base, Remote Indexing, Windsurf Ignore)
- Added: Customization section (Rules, Workflows, Skills, AGENTS.md, Memories with decision guide)
- Added: Developer Tools section (Terminal, Previews, Vibe and Replace, Quick Review, Codemaps, App Deploys, DeepWiki, Worktrees, Diff Zones, Code Lenses, Smart Paste)
- Added: Pricing and Plans (quota system, plan tiers, enterprise billing)
- Added: Enterprise Features (RBAC, SSO/SCIM, GPO/MDM, FedRAMP, Analytics API)
- Added: Settings and Configuration (consolidated directory structure, settings systems, telemetry, private folders, key files)
- Changed: "Chat Mode" renamed to "Ask Mode" throughout
- Changed: "credits" replaced with "quota" terminology
- Changed: Interception test results table converted to list format
- Changed: TBD entries annotated with "[Not yet tested as of 2026-05]"
- Removed: Duplicate old sections (content relocated to new structure)
- Fixed: All acronyms expanded on first use (RBAC, SSO, SCIM, GPO, MDM, ACU)

**[2026-05-28 12:29]**
- Added: Architecture Internals section with process model, language server binary analysis, API endpoints, startup sequence, proxy detection, network architecture, MCP transport, and inspected files reference [TESTED]

**[2026-03-30 19:48]**
- Added: Telemetry and Privacy subsection [VERIFIED]

**[2026-03-19 10:33]**
- Added: Arena Mode, Plan Mode, Model Picker, worktrees, enterprise hooks, system-level skills
- Source: windsurf.com/changelog (Wave 13-14, Feb-Mar 2026)

**[2026-01-26 13:20]**
- Added: Model Switching and Context Window section with [TESTED] findings

**[2026-01-13]**
- Initial document created from Cascade documentation research
