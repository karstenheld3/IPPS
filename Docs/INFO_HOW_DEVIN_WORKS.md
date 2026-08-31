# INFO: How Devin Desktop Works

**Doc ID**: DVDT-IN01
**Goal**: Comprehensive reference for Devin Desktop (formerly Windsurf) - agent harnesses, AI models, customization, developer tools, enterprise controls, and architecture internals
**Version scope**: Devin Desktop 3.8.20+ / Devin Local 2026.5.26+
**Timeline**: Created 2026-08-27, Updated 2 times (2026-08-27 - 2026-08-30)

## Summary

**Agent Architecture:**
- Devin Local (Rust-based) replaces Cascade as primary agent with subagents, OS-level sandboxing, and 5 permission modes [VERIFIED]
- Conversation sharing now supported in Devin Local (previously Cascade-only) [VERIFIED]
- ACP open protocol enables 12+ agents (Codex, Claude, OpenCode, Junie, Gemini, Amp, Cline, etc.) plus custom agent registration via local registry [VERIFIED]

**AI Models:**
- SWE-1.7 replaces SWE-1.6 with 4.5x improvement on FrontierCode (9.4% → 42.3%) [VERIFIED]
- Claude Fable 5 restored globally 2026-07-01 after first-ever US export control on commercial AI model [VERIFIED]
- Claude Opus 5 and GPT-5.6 (Sol/Terra/Luna tiers) added since last version [VERIFIED]

**Permissions and Security:**
- Agent profiles and permission modes now independent controls [VERIFIED]
- Smart mode: fast model auto-judges routine actions with hardcoded never-auto-approved list [VERIFIED]
- Security Swarm: 72% recall on 50 real-world GitHub Security Advisory (GHSA) vulns, 30% lower cost per finding [VERIFIED]

**Extensibility:**
- Plugins (closed beta) bundle skills, rules, subagents, hooks, MCP servers under namespace [VERIFIED]
- Skills detection ceiling ~32-36 model-triggered; user-only skills bypass limit [VERIFIED]
- `devin migrate workflows` converts Cascade workflows to native Skills [VERIFIED]

**Enterprise:**
- Sandbox enforcement org-wide, permission rule composition (deny-wins across levels) [VERIFIED]
- FedRAMP, SSO/SCIM, GPO/MDM, Analytics API available [VERIFIED]

**Architecture:**
- VS Code OSS 1.126 base. Go language server handles all AI communication [TESTED 2026-05]
- Three independent network stacks with separate proxy handling [TESTED 2026-05]

## Table of Contents

1. [Overview](#1-overview)
2. [Product History](#2-product-history)
3. [Agent Architecture](#3-agent-architecture)
4. [Agent Command Center and Spaces](#4-agent-command-center-and-spaces)
5. [AI Models and Routing](#5-ai-models-and-routing)
6. [Permissions and Security](#6-permissions-and-security)
7. [Code Editing and Completion](#7-code-editing-and-completion)
8. [Code Review](#8-code-review)
9. [Extensibility: Rules and AGENTS.md](#9-extensibility-rules-and-agentsmd)
10. [Extensibility: Skills and Workflows](#10-extensibility-skills-and-workflows)
11. [Extensibility: Plugins, MCP, and Hooks](#11-extensibility-plugins-mcp-and-hooks)
12. [Cascade (Legacy Agent)](#12-cascade-legacy-agent)
13. [Devin CLI Reference](#13-devin-cli-reference)
14. [Pricing and Plans](#14-pricing-and-plans)
15. [Enterprise Features](#15-enterprise-features)
16. [Settings and Configuration](#16-settings-and-configuration)
17. [Architecture Internals](#17-architecture-internals)
18. [Sources](#18-sources)
19. [Document History](#19-document-history)

## 1. Overview

Devin Desktop (formerly Windsurf) is an AI-powered IDE built on [VS Code Open Source Software](https://github.com/microsoft/vscode) (OSS) 1.126, developed by [Cognition](https://cognition.com/) (formerly Codeium). Renamed on 2026-06-02 via standard over-the-air update. Settings, keybindings, and most VS Code extensions remain compatible. The product frames itself as "an agent manager with a full IDE built in, not the other way around." [VERIFIED]

**Platform support:**
- **Windows** 10+ (64-bit)
- **macOS** Yosemite+
- **Linux** Ubuntu 20.04+ (glibc >= 2.31); other distributions glibc >= 2.28 [VERIFIED]

**Remote development:**
- **SSH** - Built-in implementation (not Microsoft's). Linux remote hosts only
- **Dev Containers** - macOS, Windows, Linux. Local and remote (via SSH). Requires Docker
- **Windows Subsystem for Linux (WSL)** - Beta support. Requires pre-configured WSL on Windows [VERIFIED]

**IDE plugins:** Cascade agent also available as plugin for JetBrains (2023.3+), Visual Studio (17.5.5+), Neovim, Vim, Emacs, Xcode, Sublime Text, Eclipse. Devin Local only supported in Devin Desktop and Devin CLI. [VERIFIED]

**Devin Next:** Pre-release channel with early access. Download at [devin.ai/download](https://devin.ai/download). [VERIFIED]

**Key concepts:**
- **Agent Command Center (ACC)** - Default surface. Kanban view managing all agents
- **Agent Client Protocol (ACP)** - Open protocol for running any compatible agent (Codex, Claude, OpenCode, Junie, Gemini CLI)
- **Devin Local** - Primary local agent (replaces Cascade for new sessions)
- **Devin Cloud** - Autonomous cloud agent with own VM
- **Devin CLI** - Terminal agent, same harness as Devin Local
- **Cascade** - Legacy local agent, still maintained and shipped. Modes: Code, Plan, Ask
- **Spaces** - Task grouping with shared context
- **Adaptive Model Router** - Automatic model selection based on task complexity
- **Windsurf Tab** - AI-powered code completion (Autocomplete and Supercomplete)
- **Fast Context** - SWE-grep models for rapid codebase search (20x faster)
- **DeepWiki** - Auto-generated codebase documentation and architecture diagrams
- **Devin Review** - Deep PR review with smart diff organization
- **Security Swarm** - Agentic security vulnerability scanning
- **Quota system** - Daily/weekly token budgets replacing credit system [VERIFIED]

## 2. Product History

On 2026-06-02, [Cognition](https://cognition.com/) (which acquired Codeium) renamed Windsurf to Devin Desktop via standard over-the-air update. The primary agent changed from Cascade to Devin Local. Cascade remains available as a legacy agent (see Section 12). [VERIFIED]

**Key renames:**
- Windsurf.exe / Windsurf.app → Devin.exe / Devin.app
- windsurf.com/editor → [devin.ai/download](https://devin.ai/download)
- docs.devin.com → [docs.devin.ai/desktop](https://docs.devin.ai/desktop)

**File path changes:** Per-user IDE data moved from `Windsurf/` to `Devin/` on all OSes. Extensions moved from `~/.windsurf/extensions/` to `~/.devin/extensions/`. `.codeium/` directory unchanged. [VERIFIED]

**Workspace path fallbacks:** `.devin/` preferred, `.windsurf/` fallback for rules, skills, plans, and workflows. Rules precedence: 1) `.devin/rules/`, 2) `.windsurf/rules/`, 3) `.devinrules` (legacy single-file). AGENTS.md, agents.md, and `.cursor/rules/*.mdc` also read. [VERIFIED]

**CLI aliases:** `devin-desktop`, `surf`, `windsurf` all continue to work. [VERIFIED]

**Backward compatibility (unchanged):**
- Plans and pricing stay the same
- VS Code and Windsurf extensions remain compatible
- Keybindings preserved
- Language Server Protocols (LSPs) functional
- Workflows and Skills continue working (with path fallbacks)
- Settings and configuration carry over automatically
- No manual migration needed (OTA update)
- Migration wizard available for remote SSH workspaces [VERIFIED]

**What changed in development tools:**
- Status bar hidden by default; restore with `"workbench.statusBar.visible": true`
- Settings and Keyboard Shortcuts open as regular editor tabs by default
- "Plugins" (IDE extension marketplaces) renamed to "Extensions"
- Base IDE updated to VS Code 1.126 [VERIFIED]

**Update channels:** Stable (default) and Next (pre-release). Auto-update enabled by default. Enterprise can disable auto-update via GPO/MDM policy. "Restart to Update" asks confirmation when local agents are still working. Download Next at [devin.ai/download](https://devin.ai/download). [VERIFIED]

**Network allowlist:** Add `*.devin.com`, `*.devin.ai`, `*.devinenterprise.com`, `*.codeiumdata.com`, `*.codeium.com`, `*.googleapis.com`. Update downloads: `windsurf-stable.codeiumdata.com`. [VERIFIED]

**MDM/Device Management:** Application name changed. Policies allowing "Windsurf" may block "Devin" - update MDM allowlists after the June 2 update. [VERIFIED]

## 3. Agent Architecture

Devin Desktop provides multiple agent harnesses that coexist in the IDE. An agent selector in the bottom-right corner when starting new conversations offers: Devin Local (primary), Cascade (legacy), and ACP agents (if enabled). Enterprise admins can disable Cascade entirely. [VERIFIED]

### 3.1 Devin Local

Devin Local is the primary local agent, successor to Cascade. Completely rewritten in Rust. Shares the same harness as Devin CLI. [VERIFIED]

**Key improvements over Cascade:**
- **Token efficiency** - 30% fewer tokens for same tasks, greater prompt caching [VERIFIED]
- **Subagents** - Spawn independent subagents (foreground or background). Nesting supported (`max-nesting` default 3). Default subagent model: SWE-1.7. Custom subagents defined in `AGENT.md` files at `.devin/agents/<name>/AGENT.md` or global `~/.config/devin/agents/`. `.claude/agents/*.md` auto-discovered [VERIFIED]
- **OS-level sandboxing** - Filesystem isolation (writable/readable paths) and network filtering (domain allowlists/denylists). Enterprise-enforceable. Plan mode works in sandbox [VERIFIED]
- **Quick Review** - Dedicated subagent for rapid feedback on changes [VERIFIED]
- **Plan mode** - Agent researches with read-only commands, maintains persistent Markdown plan at `~/.devin/plans/plan-<session>.md`, asks for approval before implementing [VERIFIED]

**Permissions model:** Deny/Ask/Allow rules scoped to: file reads, file writes, command execution, HTTP fetches, MCP tools. "Always Allow" grants persist across sessions (since 2026.5.26). Session permission grants apply to root agent and all sibling subagents. See Section 6 for full permission mode details. [VERIFIED]

**MCP configuration (Devin Local):**
- **Project**: `.devin/config.json` (version-controlled)
- **Local override**: `.devin/config.local.json` (gitignored)
- **User**: `~/.config/devin/config.json` [VERIFIED]

**Supports:** Rules, AGENTS.md, Skills, Plugins, Codemaps, Fast Context, Megaplan, Conversation sharing [VERIFIED]

**Does NOT support:**
- **Memories** - Does not persist. Migrate to Skills
- **Workflows** - `.devin/workflows/` not read. Migrate to native Skills
- **Code Lenses** - Do not trigger Devin Local
- **App Deploys** - Not supported [VERIFIED]

**Additional capabilities (since 2026.5.26):**
- Skill `permissions:` frontmatter applies to auto-approvals
- Editable command approvals (click to edit before approving)
- Edits in autonomous mode produce reviewable diffs
- MCP servers support client-defined OAuth scopes
- Windows: detects GPO-blocked PowerShell, falls back to Git Bash
- Keyboard shortcuts for permission requests (always-allow and reject) [VERIFIED]

**Enterprise controls:** Sandbox enforcement, granular permissions, network enforcement, disable Cascade option. See Section 15. [VERIFIED]

### 3.2 Devin Cloud

Autonomous software engineering agent on its own VM with desktop, browser, and computer use. Works asynchronously. Delivers Pull Requests. [VERIFIED]

**Agent tiers:**
- **Standard** - Default Devin Cloud agent
- **Ultra** - Most capable. Excels at long-horizon tasks and debugging. Toggle via `!ultra` in Slack
- **Fast** - Quicker, lower-cost tier. Toggle via `!fast` in Slack
- **Fusion** - Shown as mode badge on session-create cards in Desktop [ASSUMED from changelog] [VERIFIED]

**Delegation workflow:**
1. Plan locally with Devin Local or Cascade
2. One-click delegation to Devin Cloud
3. Devin spins up VM, works independently (debugging, deployment, testing)
4. Review changes and test results in-editor
5. Returns a reviewable Pull Request [VERIFIED]

**Managed Devins (parallel cloud sessions):**
- Coordinator session breaks large tasks into parallel workstreams
- Each child session runs on its own isolated VM
- Coordinator scopes work, monitors Agent Compute Units (ACUs), resolves conflicts, compiles results
- Spawn, message, sleep/terminate, and wait-for-all-complete from parent session
- Available through Devin MCP server (sessions, playbooks, schedules, knowledge) [VERIFIED]

**Pricing:** Consumes shared quota and extra usage balance. Same token-based system. [VERIFIED]

**Desktop integration:**
- Server-side send queue synced with web app; `Cmd/Ctrl+Enter` queues next message on server
- Multi-user (Slack) sessions show each participant's name above messages
- "Copy link" action in cloud session menus
- "Remote ACP is disconnected" banner with Reconnect action when connection drops
- Configure session network policy and grant/deny network access inline from chat [VERIFIED]

**Availability:** Included with Pro, Max, Teams. Enterprise: disabled by default, admin must enable. First-time users get up to $50 in extra usage. [VERIFIED]

### 3.3 Devin CLI

Rust-based CLI agent available for all Devin Desktop users. Same harness as Devin Local. Sessions accessible from both IDE and CLI. [VERIFIED]

**Capabilities:**
- Full codebase and tools access on user's machine
- Hand off to Devin Cloud for async work
- Multi-model support: all models available in Devin Local
- Subagents, Skills, Plugins, MCP, Hooks - same as desktop
- Windows: `Install Devin CLI` command writes a shim that auto-updates with Desktop [VERIFIED]

**Install:**
- macOS/Linux: `curl -fsSL https://cli.devin.ai/install.sh | bash`
- Windows: See [docs.devin.ai/desktop](https://docs.devin.ai/desktop) [VERIFIED]

Detailed commands and slash commands in Section 13.

### 3.4 Agent Client Protocol (ACP)

Devin Desktop ships with [ACP](https://agentclientprotocol.com/), an open-source protocol that standardizes communication between code editors and coding agents. Analogous to Language Server Protocol (LSP) for language intelligence. Third-party agents get the same interface as Devin: Kanban view, Spaces, shared context. [VERIFIED]

**Compatible agents (built-in registry):**
- **Codex CLI** (OpenAI)
- **Claude Agent** (Anthropic)
- **OpenCode** - Open source coding agent
- **Junie** (JetBrains)
- **Gemini CLI** (Google)
- **Amp** - Frontier coding agent
- **Google Antigravity** - Google's AI coding agent
- **Auggie CLI** (Augment Code)
- **Autohand Code** (Autohand AI)
- **Cline** - Autonomous coding agent CLI
- **Codebuddy Code** (Tencent Cloud)
- **Agoragentic** - Agent marketplace with 174+ AI capabilities
- **Custom agents** - Any ACP-compatible binary registered via local or team registry [VERIFIED 2026-08-30]

**Enabling:**
1. Command Palette (`Ctrl+Shift+P`) > "Devin User Settings"
2. Click "Agents" tab
3. Toggle on desired ACP agents
4. Restart Devin Desktop (or run `Reload ACP Connections` from Command Palette to iterate without restart) [VERIFIED 2026-08-30]

**Registry configuration:**
- **macOS/Linux**: `~/.windsurf/acp/registry.json` (Devin Desktop) or `~/.windsurf-next/acp/registry.json` (Next) [VERIFIED]
- **Windows**: Documented paths above do NOT work. The extension source (`getWindsurfConfigDirectory` in `windsurf/dist/extension.js`) hardcodes `path.join(os.homedir(), "AppData", "Roaming", "Code", "User")` on Windows, ignoring the `.windsurf-next` channel variable. Actual path: `%APPDATA%\Code\User\acp\registry.json` [TESTED 2026-08-31]
- **Team**: configured via Devin Settings at [windsurf.com/team/settings](https://windsurf.com/team/settings)
- Command Palette: "Open Local ACP Registry Config" creates/opens the file at the correct path for the current OS and channel [VERIFIED 2026-08-31]

**ACP registry format:**
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
          "darwin-aarch64": { "archive": "", "cmd": "devin", "args": ["acp"] },
          "windows-x86_64": { "archive": "", "cmd": "devin", "args": ["acp"] }
        }
      }
    }
  ],
  "extensions": []
}
```
[VERIFIED 2026-08-30]

**Custom agent registration:**
1. Add agent entry to local registry JSON (`cmd` = absolute path to binary, `args` = ACP flag)
2. Binary must already be installed locally -- Devin Desktop does not download from `archive` URLs
3. Restart Devin Desktop or run `Reload ACP Connections` from Command Palette
4. Enable the agent in Devin User Settings > Agents tab
5. Agent environment variables: configure via `...` button next to each agent in the Agents tab, or via `devin.acp.agentEnv.<agentId>` in `settings.json` [VERIFIED 2026-08-30]

**Availability:** Pro, Max, and Teams users. Enterprise admins contact account team for third-party agent access. [VERIFIED]

**Limitations (Devin Desktop as ACP client):**
- Session modes not exposed in UI -- use session config option with `"mode"` category instead
- Terminal capabilities not advertised -- agents run commands in own subprocess and stream output via `tool_call` updates
- Distribution downloads not supported -- binary must be pre-installed
- **Windows registry path bug**: `getWindsurfConfigDirectory()` returns `%APPDATA%\Code\User` on Windows regardless of product channel (stable/next/insiders/airgap). The `.windsurf-next` variable is set but never used in the Windows branch. macOS and Linux use the correct channel-specific `~/.windsurf-*` path. [TESTED 2026-08-31]

### 3.5 Cascade

Legacy local agent. Open via `Cmd/Ctrl+L` or click agent icon (top right). Maintained and shipped as part of Devin Desktop. [VERIFIED]

Three modes (Code, Plan, Ask) and four execution levels (Disabled, Allowlist, Auto, Turbo). See Section 12 for detailed coverage of modes, Memories, and Cascade-only features.

Enterprise can disable Cascade via "Enable Cascade" control. [VERIFIED]

## 4. Agent Command Center and Spaces

### 4.1 Agent Command Center

The default surface in Devin Desktop. Manages every agent (local and cloud) from one Kanban board grouped by status: In Progress, Blocked, Ready for Review. [VERIFIED]

**Agent types shown:** Local agents (Devin Local, Cascade, ACP agents) and Cloud agents (Devin sessions on VMs). Display as Kanban board (default) or list/inbox view. [VERIFIED]

**Key capability:** Parallel agents. Multiple agents working simultaneously on different parts of the same project. One engineer fans out work, reviews results as they land. [VERIFIED]

**Multi-window:** Configure agent window location via `devin.agentWindow.location` setting. [VERIFIED]

**Session controls:**
- Rename: double-click session tab or `/rename` slash command
- Fork: "Duplicate session" action to branch off a conversation
- Share: "Copy link" action in session context menu
- Select text in transcript and add to chat input with "Add to chat" / `Cmd/Ctrl+L`
- New tabs default to Devin Local when no preferred agent chosen
- Agents unavailable in Restricted Mode (untrusted workspaces); hooks do not load [VERIFIED]

**UI features:**
- Restyled command palette, Inter font, rounded pill session tabs with state/PR icons
- Timeline navigator for Devin Local sessions
- Agent sidebar: right-click context menus, per-workspace filters/sort/grouping, greyed-out locked sessions, sticky grouped spaces
- Session-create cards show Devin mode badge (Fast, Ultra, Fusion)
- PR editor tabs show state-specific icon (open, draft, merged, closed)
- Unified notifications for OS notifications when any session finishes or needs input
- "Open customizations" from new-tab menu and Devin Local session context menu
- Plugins section in customizations listing loaded and available plugins
- `@`-mention menu includes Rules for manual-trigger activation
- Performance: faster syntax highlighting for streaming diffs, no typing lag during background streaming [VERIFIED]

### 4.2 Spaces

Spaces group everything related to a task or project: agent sessions (local and cloud), pull requests, files, and project-level context. [VERIFIED]

**Context sharing:** New sessions in a Space inherit everything the Space already knows. Agents start with useful context instead of blank slate. Switching Spaces = switching tasks with view restored exactly as left. [VERIFIED]

**Creating a Space:**
- Drag session onto session in sidebar
- Split pane `Cmd/Ctrl+\` then "New Session" in empty pane
- Keyboard shortcut `Cmd/Ctrl+T` opens new session in current Space
- Every session is its own Space by default [VERIFIED]

## 5. AI Models and Routing

### 5.1 Cognition Models

No direct API access - available exclusively through Devin platform (Web, Desktop, CLI). [VERIFIED]

**[SWE-1.7](https://cognition.com/blog/swe-1-7)** (released 2026-07-08):
- Replaces SWE-1.6 as primary in-house model. Trained from Kimi K2.7 base using Cognition's RL pipeline
- Cerebras inference at ~1000 tokens/second. SWE-1.7 Lightning: same intelligence, lower latency (`/fast` selects it)
- FrontierCode 1.1 Main: 42.3% (4.5x improvement over SWE-1.6's 9.4%), Terminal-Bench 2.1: 81.5%, SWE-Bench Multilingual: 77.8%
- Cost per FrontierCode task: $1.97
- Behavioral change: spends more time investigating before editing, better at root causes and edge cases
- Free on paid plans [VERIFIED]

**SWE-1.6** - Previous-generation. Parallel tool calls, less looping. Free on paid plans [VERIFIED]

**SWE-1.5** - Previous frontier. ~950 tokens/sec. Free model [VERIFIED]

**Utility models:**
- **SWE-1-mini** - Powers Windsurf Tab passive suggestions, optimized for real-time latency
- **swe-grep / swe-grep-mini** - Powers Fast Context. Up to 2,800 tokens/sec. RL-trained for parallel tool calling
- **SWE-check** - Quick Review model for bug detection. Free. Up to 10x faster than deep review [VERIFIED]

### 5.2 Anthropic Models

**[Claude Opus 5](https://www.anthropic.com/research/claude-opus-5)** (released 2026-07-24):
- $5/$25 per MTok (same as Opus 4.8); Fast mode at $10/$50 (2.5x speed)
- 1M token context, 128K max output (300K on Batch API with beta header)
- Knowledge cutoff: May 2026; adaptive thinking (default effort `high`)
- Available: Claude API, Amazon Bedrock, Google Cloud, Microsoft Foundry
- Frontier-Bench v0.1 SOTA (2x Opus 4.8), CursorBench 3.2 within 0.5% of Fable 5
- Default on Claude Max, strongest on Claude Pro [VERIFIED]

**[Claude Sonnet 5](https://www.anthropic.com/news/claude-sonnet-5)** (released 2026-06-30):
- $2/$10 per MTok ([introductory pricing made permanent](https://platform.claude.com/docs/en/about-claude/pricing) 2026-08-10)
- 1M token context, 128K max output
- Knowledge cutoff: January 2026
- Newer tokenizer: ~30% more tokens for same text vs Sonnet 4.6
- Outperforms Opus 4.8 on FrontierCode. Default for Free and Pro plans [VERIFIED]

**[Claude Fable 5](https://devin.ai/blog/claude-fable-5-available-in-devin/)** (released 2026-06-09):
- $10/$50 per MTok, 1M context, 128K max output, "Mythos-class" flagship
- Knowledge cutoff: January 2026; adaptive thinking (always on), default effort `high`
- **Suspension and restoration:** Suspended 2026-06-12 by US Commerce Department export control directive (first-ever applied to commercial AI model). Commerce Department lifted controls 2026-06-30. Anthropic [restored access](https://www.anthropic.com/news/fable-mythos-access) globally 2026-07-01. Status: **restored** [VERIFIED]

**Also available:** Claude Opus 4.8, Opus 4.7 (with Fast modes), Sonnet 4.6, Opus 4.6, Sonnet 4.5 [VERIFIED]

### 5.3 OpenAI Models

**[GPT-5.6](https://devin.ai/blog/gpt-5-6)** (released 2026-07-09):
- Three tiers sharing 1.05M context, 128K max output, knowledge cutoff February 16, 2026
- Reasoning effort: none, low, medium (default), high, xhigh, max. `gpt-5.6` alias routes to Sol
- **Sol** (flagship): $5/$30 per MTok. Fast mode: $10/$60 (2.5x speed). Long-context surcharge: 2x input / 1.5x output above 272K tokens
- **Terra** (balanced): $2/$12 per MTok (was $2.50/$15 at launch)
- **Luna** (fast/cheap): $0.20/$1.20 per MTok (was $1/$6 at launch, [80% cut](https://openai.com/index/advancing-the-price-performance-frontier-with-gpt-5-6/)). Cached input: $0.02/MTok
- Sol Terminal-Bench 2.1: 88.8%; Sol SWE-Bench Pro: 64.6%; Luna Terminal-Bench: 82.5%
- Luna WARNING: 41.3% on Nerova long-context recall - unsuitable for document/codebase analysis
- GPT-5.6 variants are Devin Local only; disabled in Cascade model picker
- Caveats: METR found Sol reward-hacks at highest rate of any tested model [VERIFIED]

**Also available:** GPT-5.5, GPT-5.4 / 5.4 Mini, GPT-5.2-Codex / 5.1-Codex / 5.1-Codex Max, o4-mini [VERIFIED]

### 5.4 Other Models

**[Gemini 3.7 Flash](https://devin.ai/blog/gemini-37-flash)** (released 2026-08-13, Google DeepMind):
- $0.75/$3.75 per MTok (introductory through 2026-12-31, then $1.50/$7.50)
- 1M token context, 64K max output. Knowledge cutoff: March 2026
- Three thinking levels (low, medium [default], high). Multimodal: text, image, audio, video
- Sonnet 5-level performance at less than half the cost
- Live in Desktop and CLI [VERIFIED]

**[Kimi K3](https://devin.ai/blog/kimi-k3/)** (released 2026-07-16, Moonshot AI):
- $3/$15 per MTok, $0.30 cache hit (flat, no long-context surcharge)
- 1M token context, 128K max output (configurable up to 1M)
- 2.8T total parameters (Mixture of Experts (MoE): 896 experts, 16 active/token = ~280B active)
- Always-on thinking; reasoning effort: none, low, medium, high, xhigh, max
- GPQA Diamond 93.5% (highest open-weight), FrontierCode 59.6
- [Open weights](https://codersera.com/blog/kimi-k3-complete-guide-2026/) released 2026-07-27
- Live in Desktop and CLI [VERIFIED]

**Also available:** Gemini 3.1 Pro, Gemini 3 Pro/Flash, Kimi K2.5, Grok Code Fast, DeepSeek-R1/V3 [VERIFIED]

### 5.5 FrontierCode Ranking

Based on [Kimi K3 announcement](https://devin.ai/blog/kimi-k3/) benchmark chart:

```
64.9  Claude Fable 5 (restored)
63.6  GPT-5.6 Sol
60.6  Claude Opus 4.8 / Opus 5
59.6  Kimi K3
58.2  GPT-5.5
56.7  Claude Sonnet 5
56.2  GPT-5.6 Terra
55.8  SWE-1.7
55.1  GPT-5.6 Luna
54.6  Claude Sonnet 4.6
```
[VERIFIED]

### 5.6 Model Routing and Selection

**Adaptive Model Router:** Automatically selects best model for each task. Pro, Max, Teams. Introductory pricing: $0.50/$2.00/$0.10 per MTok (input/output/cache read). Fixed rate regardless of underlying model. [VERIFIED]

**Arena Mode:** Two models respond simultaneously, anonymously. User votes, identities revealed. Battle groups, personal/global leaderboards, sync-or-branch followup. [VERIFIED]

**Model Picker:** Groups models by family with hovercards. Per-model token rates visible. Prompt cache timer. Pin favorites for quick access. [VERIFIED]

**Bring Your Own Key (BYOK):** Available to free and paid individual users (not Teams/Enterprise). Supported: Claude 4 Sonnet / Opus (regular and Thinking). Configure at [devin.ai/subscription/provider-api-keys](https://devin.ai/subscription/provider-api-keys). [ASSUMED URL]

## 6. Permissions and Security

Agent profiles and permission modes are two independent controls. Agent profiles control what the agent does (Normal, Plan, Ask). Permission modes control what runs automatically. Previously coupled; now a user can be in Plan mode with Accept Edits permissions, or Ask mode with Bypass. [VERIFIED]

### 6.1 Permission Modes

Five permission modes, switchable via `Shift+Tab`, `/mode` (interactive selector), or `--permission-mode`:

- **Normal** (default): reads auto-approve, writes/commands prompt for approval
- **Accept Edits**: workspace edits auto-approve, commands still prompt
- **Smart**: edits auto-approve + fast model judges whether other actions are safe. Falls back to normal prompt when uncertain
- **Bypass** (aliases: `/yolo`, `/dangerous`): all actions auto-approve, no sandbox
- **Autonomous**: sandbox-enforced, requires `--sandbox` [VERIFIED]

**Permission matrix (key differences):**
- **Read-only tools** (file reads, grep, glob): Auto in all modes
- **File edits** (`edit`/`write`): Prompt in Normal, Auto in Accept Edits/Smart/Bypass, Prompt in Autonomous
- **Shell commands and fetches**: Prompt in Normal/Accept Edits, Auto when judged safe in Smart, Auto in Bypass/Autonomous
- **High-risk actions**: Always Prompt in Normal/Accept Edits/Smart, Auto in Bypass/Autonomous [VERIFIED]

### 6.2 Smart Permission Mode

Fast model judges action safety, auto-approves routine dev work. See [permissions reference](https://docs.devin.ai/cli/reference/permissions) for full details. Rolling out gradually via server-side flag. [VERIFIED]

**Never auto-approved** regardless of model judgment: package installs, downloads that execute code, mutating `git`, `rm`, `sudo`, `kubectl delete`, destructive cloud CLI operations (`aws`, `gcloud`, `az`, `terraform`), and reads/writes to dotenv files, key material, Git config, or agent config. [VERIFIED]

### 6.3 Permission Rule Composition

Explicit `deny:` always wins across levels. Precedence: enterprise > mode > user > project > subagent. "Always allow" only appears when effective; denials identify responsible layer. [VERIFIED]

**Session grants:** "Always Allow" grants persist across sessions (since 2026.5.26). Session permission grants apply to root agent and all sibling subagents (no re-prompting). Global option: "always allow `<cmd>` in all projects" saved to user-level `config.json`. [VERIFIED]

### 6.4 Security Hardening

- **Symlink write protection**: `edit`, `write`, `apply_patch`, `notebook_edit` refuse writes through symlinks (3.7.16 + CLI)
- **Restricted Mode**: agents unavailable in untrusted workspaces, hooks don't load
- **Sudo handling**: password prompts fail fast with explanation instead of hanging
- **Windows TLS**: root + intermediate certificates loaded from Windows cert store (fixes corporate CA/proxy, 3.7.16)
- **Separate MCP logs**: each server gets its own `MCP: <server>` output channel [VERIFIED]

### 6.5 Sandbox

Autonomous mode enforces filesystem isolation (writable/readable paths from permission scopes) and network filtering (domain allowlists/denylists). Enterprise-enforceable org-wide. Plan mode works inside sandbox. [VERIFIED]

## 7. Code Editing and Completion

### 7.1 Tab Completion

Windsurf Tab is a contextually aware diff-suggestion engine powered by SWE-1-mini. Name retained from Windsurf branding. [VERIFIED]

- **Supercomplete** (recommended, default) - Small windows around cursor suggesting deletions and additions
- **Autocomplete** - Traditional inline completion at cursor position
- **Tab to Jump** - Anticipates next cursor position. Press Tab to navigate
- **Tab to Import** - After defining new dependency, press Tab to auto-import at file top [VERIFIED]

**Context sources:** Current file and open files, recent terminal activity, recent code changes, clipboard contents (opt-in), agent chat history. [VERIFIED]

**Shortcuts:** Accept: `Tab`. Cancel: `Esc`. Accept word-by-word: `Cmd+Right` (VS Code) / `Alt+Shift+\` (JetBrains). [VERIFIED]

### 7.2 Fast Context

Specialized subagent retrieving relevant code 20x faster than traditional agentic search. Uses SWE-grep and SWE-grep-mini models. Triggers automatically, executes up to 8 parallel tool calls per turn (max 4 turns). Restricted cross-platform tools (grep, read, glob). Supported in Devin Local since 3.6.21. [VERIFIED]

### 7.3 DeepWiki

AI-powered codebase documentation. Auto-indexes repositories and generates architecture diagrams, codebase summaries, links to source code. New agents in a Space read the DeepWiki index for immediate context. [VERIFIED]

Usage: Hover over symbol > `Cmd+Shift+Click` for explanation. Send explanations to agent via context menu. [VERIFIED]

### 7.4 Knowledge Base

Teams and Enterprise only. Google Docs as shared context for entire team. Admin connects Google Drive via OAuth, adds up to 50 docs. Agents automatically reference relevant knowledge base documents when answering questions. Updates to Google Docs reflected automatically. [VERIFIED]

### 7.5 Remote Indexing

Teams and Enterprise only. Index remote repositories without local clone. Pre-indexes at team level, speeds up codebase-wide searches.
Admin configures via team settings portal. [VERIFIED]

### 7.6 Web and Docs Search

- `@web` - General web search
- `@docs` - Curated documentation search
- Paste URLs directly into chat [VERIFIED]

### 7.7 Ignore Files

`.codeiumignore`, `.devinignore`, `.windsurfignore` all honored. Global: `~/.codeium/windsurf/.codeiumignore`. Setting: `devin.allowCascadeAccessGitignoreFiles`. [VERIFIED]

## 8. Code Review

### 8.1 Devin Review

Deep PR review with smart diff organization. Enterprise requires Cognition platform agreement. [VERIFIED]

**Capabilities:** Organizes diffs around logic of change (not alphabetical), groups related edits, displays copied/moved code cleanly, identifies bugs with explanations, in-editor review. [VERIFIED]

**Autofix:** Devin generates fixes for review comments and applies back to PR branch. Closes the loop: agent writes code, Devin Review checks, Devin fixes. [VERIFIED]

**Workflow:** 1) Agent creates PR → 2) Devin Review analyzes diff → 3) Findings surfaced in-editor → 4) Codebase-aware chat for context → 5) Autofix applies corrections → 6) GitHub auto-merge when checks pass. [VERIFIED]

**Security in Devin Review:** Every PR gets automatic security review alongside code review. Enabled by default (toggle in Settings > Review > Security scan). [VERIFIED]

**Vulnerability categories:**
- Injection (SQL, Cross-Site Scripting (XSS), command, template)
- Auth flaws (missing/broken access control, privilege escalation, auth bypass)
- Secrets exposure (hardcoded keys, tokens in logs, credentials in source)
- Server-Side Request Forgery (SSRF) and path traversal
- Insecure deserialization, prototype pollution
- Missing input validation on untrusted data
- Weak cryptography (algorithms, key management)
- Transport/cookie security (missing HTTPS enforcement, permissive Cross-Origin Resource Sharing (CORS), insecure cookie flags) [VERIFIED]

**Findings:** Classified by severity: Critical (fix before merge) and Warning (investigate). Tagged with Common Weakness Enumeration (CWE) identifier. Includes description, recommendation, and fix. Respects `REVIEW.md` and `SECURITY.md` for custom security policies. [VERIFIED]

**Remediation:** Devin writes the fix and opens a merge-ready PR. One click posts the finding as inline GitHub PR comment. [VERIFIED]

### 8.2 Quick Review

Fast local review before opening a PR. Devin Local only. [VERIFIED]

**Models:**
- **SWE-check** - Fast, free for all tiers (10x faster than deep review)
- **GPT 5.5** - Deep agentic review, token-based pricing
- **Opus 4.7** - Deep agentic review, token-based pricing [VERIFIED]

Enterprise: admin controls available review models. Two Review Loops pattern: Quick Review before PR (fast feedback on working tree), Devin Review after PR (deep review with Autofix). [VERIFIED]

### 8.3 Security Swarm

Full-codebase vulnerability scanner powered by Agentic MapReduce. Parallel Devin agents analyze the codebase like a team of security researchers. [VERIFIED]

**Five stages:**
1. **Plan** (agentic) - Agent studies repo, builds threat model, writes selectors (routes, auth boundaries, deserialization sinks). Editable before swarm fans out
2. **Shard** (deterministic) - Selectors run over entire repo. Matches bucketed into bounded batches
3. **Map** (agentic) - One child Devin session per batch, in parallel. Traces issues across files
4. **Reduce** (agentic) - Deduplicates, attaches owners, assigns priority (P0/P1/P2)
5. **Verify** (optional, agentic) - Sandboxed session reproduces exploit. Confirmed/False Positive/Inconclusive [VERIFIED]

**Results:** 72% recall on 50 real-world GitHub Security Advisory (GHSA) vulnerabilities across 14 languages. 30% lower cost per finding than nearest alternative. [VERIFIED]

**Scheduling:** Daily, weekly, or custom. First scan is full baseline. Subsequent scans process only changed files (cost tracks diff, not repo size). [VERIFIED]

**Devin Security Program:** Six-week engagement. Cognition engineers embed with customer team to burn down CVE backlog and set up ongoing Security Swarm scanning. [VERIFIED]

## 9. Extensibility: Rules and AGENTS.md

Six mechanisms customize agent behavior: Memories (Cascade only), Rules, Workflows (Cascade only), Skills (universal), Plugins (Devin Local/CLI), AGENTS.md. This section covers Rules and AGENTS.md. [VERIFIED]

### 9.1 Rules

Persistent instructions that agents follow. Both Cascade and Devin Local support rules. [VERIFIED]

**Storage locations (discovery order):**
1. **Global rules**: `~/.codeium/windsurf/memories/global_rules.md` (always on, 6,000 char limit)
2. **Workspace rules**: `.devin/rules/*.md` (preferred) or `.windsurf/rules/*.md` (fallback). One file per rule, 12,000 chars per file
3. **AGENTS.md**: Directory-scoped. Root-level = always-on, subdirectory = auto-glob
4. **System-level** (Enterprise): `/etc/devin/rules/` or `C:\ProgramData\Devin\rules\`
- `.devinrules` legacy single-file still read [VERIFIED]

**Activation modes** (frontmatter `trigger` field):
- **Always On** (`always_on`) - Full rule in system prompt on every message
- **Model Decision** (`model_decision`) - Only `description` shown; agent reads full rule when relevant
- **Glob** (`glob`) - Applied when files matching `globs` pattern are touched
- **Manual** (`manual`) - Activated by `@rule-name` in chat [VERIFIED]

**Example:**
```markdown
---
trigger: glob
globs: **/*.test.ts
---

All test files must use describe/it blocks and mock external API calls.
```
[VERIFIED]

### 9.2 AGENTS.md

Directory-scoped instruction files. Placed in any directory. Agent auto-discovers and scopes instructions to files within that directory. Root-level = always-on, subdirectory = auto-glob. Both Cascade and Devin Local support AGENTS.md. Also reads `agents.md`. [VERIFIED]

## 10. Extensibility: Skills and Workflows

### 10.1 Skills

Bundles for complex tasks. Include `SKILL.md` plus supporting files. Works with both Cascade and Devin Local. Follows open [Agent Skills](https://agentskills.io/) standard. [VERIFIED]

**SKILL.md frontmatter:**
```yaml
---
name: my-skill
description: What this skill does (shown in completions)
argument-hint: "[file] [options]"
model: sonnet
subagent: true
agent: reviewer
allowed-tools:
  - read
  - grep
permissions:
  allow:
    - Read(src/**)
    - Exec(npm run test)
  deny:
    - Write(/etc/**)
triggers:
  - user
  - model
---
```
[VERIFIED]

**Skill permissions:** Additive to session base. Cannot grant what is denied at higher level. `allow` = auto-approved during execution, `deny` = blocked, `ask` = always prompt. [VERIFIED]

**Progressive disclosure (context cost):**

At session start, agent sees only the skill catalog (name + description per skill). Full SKILL.md body loaded ONLY when the skill is invoked. Near-zero tokens until needed. [VERIFIED]

- **Cascade**: "Only name and description shown to model by default. Full SKILL.md content and supporting files loaded only when Cascade decides to invoke the skill"
- **Devin Local/CLI**: "At the start of every session, Devin sees a list of all available skills (name + description). When a skill is invoked, Devin reads the full SKILL.md file and injects its body into current context"
- `$ARGUMENTS`/`$1-$9` interpolation for parameterized skills. Skills survive context compaction [VERIFIED]

**Invocation control:**
- `triggers: ["user", "model"]` (default) - Agent can auto-invoke, user can type `/name`
- `triggers: ["user"]` - User-only. Agent cannot auto-invoke. Equivalent to workflow behavior
- Devin Local: one skill active at a time. Invoking a new skill replaces the previous one
- Cascade: supports concurrent skills (no one-at-a-time limitation) [VERIFIED]

**Cross-platform comparison (Claude Code `disable-model-invocation`):**

Claude Code provides stronger invocation control than Devin's `triggers`:
- Default: user can invoke, agent can invoke, description in context
- `disable-model-invocation: true`: user can invoke, agent cannot invoke, description **removed from context** (zero tokens)
- `user-invocable: false`: user cannot invoke, agent can invoke, description in context

Key difference: Claude Code's `disable-model-invocation: true` removes the description from agent context entirely. Devin's `triggers: ["user"]` prevents auto-invocation but descriptions may still be loaded. Both fields can coexist in the same SKILL.md; each platform reads only its own. [VERIFIED]

**Detection ceiling:** Agent skill-selection accuracy degrades beyond ~32-36 model-triggered skills. This ceiling applies ONLY to skills the agent can auto-invoke. User-only skills (`triggers: ["user"]` / `disable-model-invocation: true`) bypass this limit entirely since the agent never needs to select them. [VERIFIED]

**Discovery paths (6 locations):**
1. `.agents/skills/<name>/SKILL.md` (recommended, cross-platform)
2. `.devin/skills/<name>/SKILL.md`
3. `.windsurf/skills/<name>/SKILL.md` (legacy fallback)
4. `.claude/skills/<name>/SKILL.md` (if Claude Code config reading enabled)
5. Global: `~/.config/devin/skills/<name>/SKILL.md`
6. System (Enterprise): OS-specific paths [VERIFIED]

Duplicate names across locations: each copy surfaces with location prefix (`/agents:foo`, `/claude:foo`). [VERIFIED]

**`devin skills` CLI commands:** `list` (filter by `--trigger`), `show <name>`, `paths`, `search`. [VERIFIED]

### 10.2 Workflows (Cascade Only)

Step-by-step procedures as markdown. Invoked via `/workflow-name`. NOT supported with Devin Local. [VERIFIED]

**Storage:** `.devin/workflows/*.md` or `.windsurf/workflows/*.md`

**Format:**
```yaml
---
description: [short title]
---
[specific steps]
```

**Migration to Devin Local/CLI:**
- **Devin Desktop**: Convert to native Skills at `.devin/skills/<name>/SKILL.md` (only method for `/slash-command` autocomplete)
- **Devin CLI**: Place in `.claude/commands/` (imported as slash commands, does NOT work in Desktop)
- `.devin/workflows/` explicitly excluded from import by either

**Migration command:** `devin migrate workflows` converts legacy workflows to native skills (since 2026.5.26). [VERIFIED]

## 11. Extensibility: Plugins, MCP, and Hooks

### 11.1 Plugins

Bundles of skills, rules, subagents, hooks, and MCP servers in a single installable package. Closed beta (contact support@cognition.ai for access). [VERIFIED]

**Plugin structure:**
```
my-plugin/
  .devin-plugin/plugin.json   # Manifest (required)
  AGENTS.md                   # Always-on rules (optional)
  rules/                      # Triggered rules (optional)
  agents/<name>.md             # Custom subagent profiles (optional)
  hooks.json                  # Lifecycle hooks (optional)
  .mcp.json                   # MCP servers (optional, no client secrets)
  skills/<name>/SKILL.md       # Skills, invoked as /my-plugin:<skill> (optional)
```
[VERIFIED]

**Manifest precedence:** `.devin-plugin/plugin.json` > `.claude-plugin/plugin.json` > root `plugin.json`. [VERIFIED]

**Governance:** `requiredPlugins` (auto-installed), `optionalPlugins` (endorsed), `forbiddenPlugins` (blocked, supports glob). Higher authority wins. [VERIFIED]

**CLI commands:** `install <source>`, `list`, `info <name>`, `update [name]`, `remove <name>`. New: `git-subdir` source installs from shared repo subdirectory. Personal plugins sync to Cloud by default; `Install locally` for device-only. [VERIFIED]

### 11.2 MCP Integration

Devin Desktop supports [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) for external tools and services. MCP prompts surface as `/mcp__<server>__<prompt>` slash commands. [VERIFIED]

**Devin MCP Server (Cloud API):** Official Cognition MCP server at `https://mcp.devin.ai/mcp`. API key auth (prefix `cog_` or `apk_user_`). Tools: repository docs, session management, playbook/knowledge/schedule management. [VERIFIED]

**Cascade MCP config:** `~/.codeium/windsurf/mcp_config.json`. Transport: stdio, Server-Sent Events (SSE), Remote HTTP. [VERIFIED]

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

**Devin Local MCP config:**
- **Project**: `.devin/config.json` (version-controlled)
- **Local override**: `.devin/config.local.json` (gitignored)
- **User**: `~/.config/devin/config.json`
- Server-level "approve all" (session or permanent) for MCP tool permissions
- MCP servers moved to dedicated `mcp_config.json` (migrated automatically) [VERIFIED]

**OAuth:** MCP OAuth flow forwards RFC 8707 resource parameter. "Authenticate" button clears stored credentials and reruns browser flow. [VERIFIED]

**Admin controls (Teams/Enterprise):** MCP Registry (pre-configured approved servers), MCP Whitelist (regex-based control). [VERIFIED]

### 11.3 Lifecycle Hooks

Shell scripts running before/after agent actions. `.devin/hooks.json` or `~/.codeium/windsurf/hooks.json`. Plugin-contributed hooks labeled with plugin name. [VERIFIED]

**Configuration:**
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

**Hook events:**
- `pre_read_code` / `post_read_code`
- `pre_write_code` / `post_write_code`
- `pre_run_command` / `post_run_command`
- `pre_mcp_tool_use` / `post_mcp_tool_use`
- `pre_user_prompt` (can block)
- `post_cascade_response` / `post_cascade_response_with_transcript`
- `post_setup_worktree`
- `SessionEnd` hooks with reason; `Stop` hooks receive `last_assistant_message` [VERIFIED]

**Devin Local:** Hooks repaired for blocking user prompts (since 2026.5.26). Hooks tab lists configured hooks with source and trigger events. Hooks do not load in Restricted Mode. [VERIFIED]

## 12. Cascade (Legacy Agent)

Legacy local agent. Maintained and shipped as part of Devin Desktop. Open via `Cmd/Ctrl+L` or agent icon. Enterprise can disable via "Enable Cascade" control. Cascade-specific config hidden when disabled for team. [VERIFIED]

### 12.1 Modes

Three modes, switchable via toggle below input box or `Ctrl+.`:

- **Code Mode** - Full tool access. Default mode
- **Plan Mode** - Full tool access. Type `megaplan` for advanced form. Auto-switches to Code Mode when implementing
- **Ask Mode** - Search tools only. Cannot modify files or run commands [VERIFIED]

### 12.2 Execution Levels

Four auto-execution levels (separate from Devin Local's permission modes):

- **Disabled** - All commands require approval
- **Allowlist** - Only allowlisted commands auto-execute
- **Auto** - Model decides if safe (premium models only)
- **Turbo** - All commands auto-execute except denylist [VERIFIED]

### 12.3 Memories

Auto-generated during conversation. Workspace-scoped. Stored in `~/.codeium/windsurf/memories/`. Creating/using memories does NOT consume quota. Not supported in Devin Local. Recommendation: prefer Rules or Skills for durable, shared knowledge. [VERIFIED]

### 12.4 Cascade-Only Features

Features present in Cascade but absent from Devin Local:

- **Memories** - Auto-remembered context (see 12.3)
- **Workflows** - Step-by-step procedures as markdown (see Section 10.2)
- **Code Lenses** - Inline actions (Explain, Refactor, Add Docstring). Do not trigger Devin Local
- **App Deploys** - Deploy to Netlify directly from IDE (Next.js, React, Vue, Svelte). Beta
- **Concurrent skills** - Cascade supports multiple active skills; Devin Local limits to one at a time [VERIFIED]

**Capabilities shared with Devin Local:** Rules, AGENTS.md, Skills, MCP, Fast Context, Megaplan, Codemaps. Shared extensibility features (Rules, Skills, Plugins, MCP, Hooks) documented in Sections 9-11. [VERIFIED]

### 12.5 Architecture (Cascade-Specific)

Based on reverse-engineering and system prompt analysis. Cascade uses a distinct architecture from Devin Local. [ASSUMED]

**Multi-model pipeline:** Cascade orchestrates multiple AI models in a pipeline, each with a specialized role:
- **Primary reasoning model** - Handles main chat responses and tool calls
- **Thinking/planning generator** - Produces extended thinking chains for complex tasks
- **Memory/context model** - Manages context compression and retrieval
- **Summarization model** - Compresses long conversation histories for context window management [ASSUMED]

**System prompt structure:**
- ~50 KB fixed overhead (12 XML sections including identity, behavioral instructions, user rules, tool definitions, IDE metadata)
- Total fixed context overhead ~91 KB when including injected behaviors, tool descriptions, and MCP recommendations
- User rules section explicitly states rules "take precedence over any following instructions" [ASSUMED]

**Tool inventory:** 27 native tools across categories: file operations (read, edit, write, notebook edit), search (grep, find by name, code search), terminal (run command, command status), browser (browser preview), deployment (deploy web app), memory (create memory), and project management (todo list). Additional MCP tools loaded conditionally per workspace configuration. [ASSUMED]

**Feature flags:** ~40 feature flags controlling model selection, tool availability, A/B testing, and behavioral modes. Flags injected into system prompt at session start. Control which models are used for different pipeline roles. [ASSUMED]

**Behavioral control mechanisms (7 layers):**
1. **System prompt sections** - 12 XML sections defining identity and capabilities
2. **User rules override** - Injected with explicit precedence statement
3. **Tool description constraints** - Behavioral guidance embedded in tool definitions
4. **Feature flag injection** - Runtime configuration of models and behaviors
5. **Checkpoint anchors** - Periodic re-injection of critical instructions
6. **Injected behaviors** - Dynamic instructions based on conversation state
7. **MCP recommendations** - Server-provided guidance for tool usage [ASSUMED]

**Protocol:** gRPC-based communication between IDE and Codeium language server. Primary method `GetChatMessage` sends entire accumulated context window per turn (no delta encoding). Context grows from ~37 KB on first call to 500+ KB in long sessions. [ASSUMED]

## 13. Devin CLI Reference

Same harness as Devin Local. Sessions accessible from both IDE and CLI. All commands are ACP slash commands, invocable from any ACP client. [VERIFIED]

### 13.1 Top-Level Commands

- `devin` - Start interactive session (accepts prompt as argument)
- `devin rm <session-id-or-name>` - Delete session with confirmation (`--force` for non-interactive)
- `devin desktop` - Open Devin Desktop; `devin .` opens Desktop on current path
- `devin doctor` - Check subagent profiles for incorrect frontmatter
- `devin plugins install|list|info|update|remove` - Plugin management (see Section 11.1)
- `devin skills list|show|paths|search` - Skill management (see Section 10.1)
- `devin migrate workflows` - Convert legacy Cascade workflows to native skills [VERIFIED]

**Global flags:**
- `--model <name>` - Override model selection for session
- `--permission-mode <mode>` - Set permission mode (normal, accept-edits, smart, bypass, autonomous)
- `--sandbox` - Enable filesystem/network sandbox (required for autonomous mode)
- `--resume <session>` - Resume an existing session by ID or name
- `--print` - Print last assistant message and exit (non-interactive)
- `--output-format <json|text|stream-json>` - Output format for CI/scripting
- `--verbose` - Increase logging verbosity [VERIFIED]

### 13.2 Slash Commands

- `/recap` - Agent-generated summary of work, decisions, progress
- `/rename <title>` - Rename current session
- `/btw <question>` - Parallel side-chat without entering main conversation
- `/fast` - Select SWE-1.7 Lightning (or fallback fast model)
- `/usage` - Quota panel with daily/weekly bars, reset times, extra usage balance
- `/mode` - Interactive permission mode selector (arrow keys + Enter)
- `/smart`, `/mode smart` - Switch to Smart permission mode
- `/plan`, `/ask`, `/normal` - Switch agent profile. `/plan <prompt>` switches and sends in one step
- `/share` - Display server-returned share URL
- `/loop` - Continue agent execution
- `/mcp` - MCP server management
- `/context`, `/add-dir`, `/undo-add-dir`, `/workspace` - Context management
- `/shortcuts` - List all keybindings
- `/status`, `/help` - Instant commands (run while agent is working) [VERIFIED]

**Megaplan keywords:** `megaplan`, `ultraplan`, `masterplan` trigger extensive planning. [VERIFIED]

### 13.3 Configuration

CLI-specific keys in `.devin/config.json` or `~/.config/devin/config.json`. General config paths in Section 16. [VERIFIED]

- **`keymap`** - Configurable keybindings section
- **`notify`** - `"never"`, `"smart"` (default, notify when terminal unfocused), or `"always"`. Uses BEL, OSC 9 (iTerm2), OSC 777 (rxvt-unicode)
- **`subagents_enabled`** - Toggle subagent tools (on by default)
- **`read_config_from`** - Import config from other tools (Cursor, Claude Code, Windsurf, OpenCode, VS Code, Zed). Disable per-tool: `{ "read_config_from": { "cursor": false } }`
- **`attribution`** - Set to `false` to suppress Devin mentions in commit messages
- **Background shells** - `Ctrl+B` lists running commands [VERIFIED]

### 13.4 Developer Tools

**Terminal integration:**
- Command execution with permissions model (Devin Local) or auto-execution policies (Cascade)
- Send terminal selection to agent via context menu
- @-mention terminal output in chat
- Dedicated Terminal (beta) - separate terminal profile for agent execution [VERIFIED]

**Windsurf Previews:** Preview web apps in IDE or browser with element selection, error capture, and agent integration. Remote ACP agent sessions proxy local dev server; captured elements and console output land in message box as pending context. [VERIFIED]

**Other IDE tools:**
- **Vibe and Replace** - AI-powered find-and-replace. Search codebase, apply AI prompt to each match. Modes: Smart (careful), Fast
- **Codemaps** - Visual architecture diagrams. Referenced via `@codemap-name`. Devin Local supports since 3.6.22
- **AI Commit Messages** - Auto-generated commit messages from staged changes
- **Worktrees** - Git worktree support. Merge button to bring changes back. Pick existing worktree from agent location selector. `post_setup_worktree` hook event
- **Diff Zones** - Visual indicators for agent-edited code regions
- **Smart Paste** - Context-aware paste with AI-assisted transformation
- **Send Problems to Agent** - Problems panel integration, highlight error for agent resolution [VERIFIED]

## 14. Pricing and Plans

Quota-based usage system (replaced credits March 2026). Daily and weekly allowance that refreshes automatically. Cost per token varies by model. Free models (SWE-1.5) don't count. Most users never hit limits. [VERIFIED]

**Plan tiers:**
- **Free** - Limited quota, limited model availability, unlimited Tab completions
- **Pro** ($15/month) - Expanded quota, all models, extra usage available
- **Max** ($60/month) - Highest individual quota, significantly higher limits
- **Teams** ($40/user/month) - Team management, Knowledge Base, Remote Indexing, analytics, Role-Based Access Control (RBAC)
- **Enterprise** (custom, ACU-based) - Single Sign-On (SSO)/System for Cross-domain Identity Management (SCIM), FedRAMP, system-level controls

Note: Check [devin.ai/pricing](https://devin.ai/pricing) for current rates. [ASSUMED prices]

**Extra usage pricing (introductory):** $0.50/$2.00/$0.10 per MTok (input/output/cache read). When quota exhausted: Free waits for reset, Pro/Max/Teams purchase extra usage. [VERIFIED]

**Enterprise billing:** Agent Compute Units (ACUs) - tokens converted at per-token rates. Per-user or per-group caps via admin portal. Seat rotation: new member inherits remaining quota mid-cycle. [VERIFIED]

**When quota exhausted:**
- **Free**: Wait for daily/weekly reset
- **Pro/Max/Teams**: Purchase extra usage [VERIFIED]

**Making quota last:**
- Be precise, remove unnecessary context
- Switch to free models (SWE-1.5) for routine tasks
- Use smaller models (Haiku, GPT 5.2 Mini, Kimi K2.5) for simple tasks
- Avoid unnecessarily long sessions
- Use single model per task for caching benefits
- Stay on Adaptive Model Router for automatic optimization [VERIFIED]

## 15. Enterprise Features

### 15.1 Admin Portal

Admin portal at devin.ai/team/settings. User management with role assignment, user groups for bulk operations, quota allocation and per-user/per-group caps. [VERIFIED]

### 15.2 Role-Based Access Control (RBAC)

**Roles:** Built-in (Admin, Member) and custom roles with granular permissions.

**Permissions:** Model access, feature access, auto-execution levels, "Disable Access" to restrict users entirely. Review model controls for team-wide enforcement. [VERIFIED]

### 15.3 Single Sign-On (SSO) and SCIM

**Providers:** Azure AD/Entra ID, Google Workspace, Okta, OneLogin, Generic OpenID Connect (OIDC)/Security Assertion Markup Language (SAML).

**SCIM:** System for Cross-domain Identity Management for automated user lifecycle (provisioning, deprovisioning, group sync). [VERIFIED]

### 15.4 Group Policy Object (GPO) / Mobile Device Management (MDM)

- **Windows**: ADMX/ADML templates for Group Policy
- **macOS**: `.mobileconfig` profiles for MDM
- **Linux**: JSON policy files
- **Extension management**: AllowedExtensions whitelist, server-driven deny lists [VERIFIED]

### 15.5 Federal Risk and Authorization Management Program (FedRAMP)

FedRAMP Security Admin Guide available with administrative roles, permissions, multi-factor authentication (MFA), and security settings reference. [VERIFIED]

### 15.6 Analytics API

- Get Cascade Analytics (lines written, commands run, tool usage)
- Custom Analytics Query (selections, filters, aggregations)
- Get Team Credit Balance
- Get/Set Usage Configuration
- Per-user analytics
- Service keys with rate limits [VERIFIED]

### 15.7 Devin Local Enterprise Controls

Additional controls only available with Devin Local:
- **Sandbox enforcement** - Org-wide sandbox mode, domain filtering, `sandbox.excluded` allow/ask/deny config to run specific commands outside sandbox
- **Granular permissions** - Fine-grained action control beyond Cascade's execution levels
- **Network enforcement** - Allowed/denied domain lists
- **Terminal allow/deny lists** - Enforced through CLI permission scopes
- **Enterprise login** - Login policies enforced in CLI
- **Disable Cascade** - Force Devin Local exclusively for team [VERIFIED]

## 16. Settings and Configuration

### 16.1 File Paths and Fallbacks

**Directory structure (Windows, post-rename):**
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
├── .devin\extensions\             # Devin extensions (was .windsurf/)
├── .config\devin\config.json      # Devin Local user-level config
├── AppData\Local\Programs\Devin\  # Main installation (was Windsurf)
│   └── resources\app\extensions\
├── AppData\Local\Programs\Devin Next\  # Preview channel
└── AppData\Roaming\Devin\User\    # User data
    ├── settings.json
    ├── keybindings.json
    └── globalStorage\state.vscdb
```
[VERIFIED]

**macOS paths:**
- Installation: `/Applications/Devin.app`
- User data: `~/Library/Application Support/Devin/User/`
- Agent settings: `~/.codeium/windsurf/` (unchanged)
- Devin Local config: `~/.config/devin/config.json` [VERIFIED]

**Linux paths:**
- User data: `~/.config/Devin/User/`
- Agent settings: `~/.codeium/windsurf/` (unchanged)
- Devin Local config: `~/.config/devin/config.json` [VERIFIED]

**Executable names:** `Devin.exe` (Windows), `Devin.app` (macOS), `devin` (Linux). CLI aliases: `devin-desktop`, `surf`, `windsurf` (all still work). [VERIFIED]

**Workspace path fallbacks:** `.devin/` preferred, `.windsurf/` fallback for rules, skills, plans, workflows. `.devinrules` still read. See Section 2 for full precedence. [VERIFIED]

### 16.2 Settings

**Two settings systems:**
- **Editor settings** - JSON at `%APPDATA%\Devin\User\settings.json`. Editable via text editor. Includes `windsurf.*` keys for agent settings
- **Agent settings** (UI-only subset) - Protobuf at `%USERPROFILE%\.codeium\windsurf\user_settings.pb`. Many settings also writable via `windsurf.*` keys [VERIFIED]

**Key agent settings:** Both `windsurf.*` and `devin.*` prefixes work.

```json
{
  "windsurf.autoExecutionPolicy": "turbo",
  "windsurf.autoWebRequestPolicy": "turbo",
  "windsurf.autoContinue": true,
  "windsurf.completionMode": "autocomplete",
  "windsurf.rememberLastModelSelection": true,
  "windsurf.allowCascadeAccessGitignoreFiles": true,
  "windsurf.acp.enabledAgents": { "devin-cli": true },
  "devin.agentWindow.location": "separate"
}
```
[VERIFIED]

**Attribution:** Set `attribution` to `false` in `.devin/config.json` to suppress Devin mentions in commit messages. [VERIFIED]

**Key files reference:**

**User config:**
- `settings.json` - Editor preferences (JSON)
- `keybindings.json` - Keyboard shortcuts
- `user_settings.pb` - Agent UI settings (protobuf)
- `state.vscdb` - Window/extension state (SQLite)
- `mcp_config.json` - MCP servers (Cascade)
- `hooks.json` - User-level hooks [VERIFIED]

**Workspace config:**
- `.devin/rules/*.md` - Project rules (preferred)
- `.windsurf/rules/*.md` - Project rules (fallback)
- `.devin/workflows/*.md` - Custom workflows (Cascade only)
- `.devin/skills/*/SKILL.md` - Skills
- `.devin/config.json` - Devin Local MCP and permissions
- `.devin/config.local.json` - Local override (gitignored)
- `.devin/hooks.json` - Workspace hooks
- `AGENTS.md` - Directory-scoped instructions
- `.codeiumignore` / `.devinignore` / `.windsurfignore` - Ignore files

**ACP config:** `~/.devin/acp/registry.json` - Local ACP agent registry [VERIFIED]

### 16.3 Proxy, Network, and Telemetry

**Telemetry:** Non-essential telemetry collected by default. Opt out at devin.ai/account > Privacy > toggle "Disable Telemetry". Since 3.6.22, product analytics not started before account status resolves, so telemetry never collected for opt-out accounts. [VERIFIED]

**What telemetry controls:**
- Non-essential data collection used to improve the product
- Does NOT affect prompt caching, autocomplete, or agent functionality
- Stored server-side (account setting), not in local config files [VERIFIED]

**Proxy configuration:** Three independent network stacks with different proxy behavior (see Section 17 for details). Go binary (language server) honors proxy only when `detect_proxy=true` in `user_settings.pb`. Windows TLS: root + intermediate certificates loaded from Windows cert store, fixing corporate Certificate Authority (CA) and proxy issues (since 3.7.16). [VERIFIED]

**Working with private/gitignored folders:**

Agents can read/write gitignored files when explicitly referenced, but gitignored folders are hidden from the workspace snapshot shown at conversation start.

To make a gitignored folder visible to agents while keeping contents private, use a `.gitkeep` file:

```gitignore
# In .gitignore - folder contents ignored, folder tracked
_PrivateSessions/*
!_PrivateSessions/.gitkeep
```

Result: folder appears in workspace snapshot, contents stay private. [VERIFIED]

## 17. Architecture Internals

Based on reverse-engineering from Windsurf 2.x era. Core architecture assumed unchanged in Devin Desktop rename. [ASSUMED - verify before enterprise security/monitoring use]

**Process model:**
```
Devin.exe (Electron main process)
├── Devin.exe (GPU process)
├── Devin.exe (renderer - editor UI)
├── Devin.exe (extension host - Node.js)
├── Devin.exe (shared process, file watcher)
└── language_server_windows_x64.exe (Codeium language server - Go binary, ~166 MB)
```
~14 Electron processes + 1 language server handling ALL AI communication. [TESTED 2026-05 on Windsurf]

**Bundled dependencies:**
- **ripgrep 15.0.0** (`rg.exe`) at `resources/app/node_modules/@vscode/ripgrep-universal/bin/win32-x64/rg.exe` (~5.4 MB). Inherited from VS Code OSS. Features: PCRE2 with JIT, SIMD (SSE2/SSSE3/AVX2 at runtime). Used by:
  - Workspace text search (`Ctrl+Shift+F`)
  - Extension host grep (extensions calling VS Code search API)
  - Cascade/Devin Local context gathering (`Ptn.quickGrepContext`)
  - Deepwiki summary indexing (`NMn._loadDeepwikiSummary`)
  - Node summary extraction (`DN.getSummary`)
- Missing `rg.exe` causes cascading `ENOENT` errors across extension host, search, and context features. Source: [BurntSushi/ripgrep](https://github.com/BurntSushi/ripgrep) [TESTED 2026-08-31]

**API endpoints:**
- `https://server.self-serve.devin.com` - Primary API (auth, settings, telemetry)
- `https://inference.codeium.com` - AI inference (chat, completions, tool calls) [TESTED 2026-05]

**Three independent network stacks:**
1. **Chromium** (renderer): System proxy. Handles: marketplace, updates, previews
2. **Node.js** (extension host): Honors HTTP_PROXY/HTTPS_PROXY. Handles: extensions, MCP
3. **Go binary** (language server): Honors proxy only when `--detect_proxy=true`. Handles: ALL AI communication [TESTED 2026-05]

**MCP transport:** JSON-RPC 2.0 over Newline-Delimited JSON (NDJSON) via stdio. Protocol version `2025-11-25`. MCP tools receive ONLY tool_call arguments - no system prompt leakage. [TESTED 2026-05]

**Proxy detection:** `user_settings.pb` field 34 (`detect_proxy`, bool), default `false`. UI: Settings > "Detect Proxy" checkbox. [TESTED 2026-05]

**gRPC protocol (Cascade):** 7 service methods on the primary API endpoint. Key method `GetChatMessage` sends the entire accumulated context window per turn - no delta encoding. Context payload grows from ~37 KB on first call to 506 KB in long sessions. Each turn includes: system prompt (~50 KB fixed), conversation history, tool results, and injected behaviors. [ASSUMED]

**Multi-model pipeline (Cascade):** Four distinct model roles orchestrated per turn: primary reasoning, thinking/planning generation, memory/context management, and summarization. Model assignments controlled by ~40 feature flags. See Section 12.5 for Cascade-specific architecture details. [ASSUMED]

**Feature flag system:** ~40 flags controlling model selection, tool availability, A/B testing, and behavioral modes. Injected into the system prompt at session start. Enterprise admins can override flags via admin portal. [ASSUMED]

**Telemetry:** Opt-out via Settings > Telemetry. Categories: usage analytics, crash reports, extension telemetry. No code content transmitted in telemetry payloads. [VERIFIED]

**Update mechanism:** Two channels: Stable (default) and Next (pre-release). Auto-update enabled by default. Enterprise can disable auto-update via GPO/MDM policy. [VERIFIED]

## 18. Sources

**Primary Sources:**
- `DVDT-IN01-SC-DVNAI-RNAME`: https://devin.ai/blog/windsurf-is-now-devin-desktop - Official rename announcement [VERIFIED]
- `DVDT-IN01-SC-DVNDC-CHLG`: https://docs.devin.ai/desktop/changelog - Desktop changelog [VERIFIED]
- `DVDT-IN01-SC-DVNDC-FAQ`: https://docs.devin.ai/desktop/devin-desktop-faq - Transition FAQ [VERIFIED]
- `DVDT-IN01-SC-DVNDC-DVNL`: https://docs.devin.ai/desktop/devin-local - Devin Local docs [VERIFIED]
- `DVDT-IN01-SC-DVNDC-ACP`: https://docs.devin.ai/desktop/acp - ACP docs [VERIFIED]
- `DVDT-IN01-SC-DVNDC-PERM`: https://docs.devin.ai/cli/reference/permissions - Permissions reference [VERIFIED]
- `DVDT-IN01-SC-DVNDC-SKLL`: https://docs.devin.ai/cli/extensibility/skills/creating-skills - Skills reference [VERIFIED]
- `DVDT-IN01-SC-DVNDC-PLGN`: https://docs.devin.ai/cli/extensibility/plugins/overview - Plugins overview [VERIFIED]
- `DVDT-IN01-SC-DVNDC-CLST`: https://docs.devin.ai/cli/changelog/stable - CLI changelog [VERIFIED]
- `DVDT-IN01-SC-DVNAI-SECR`: https://devin.ai/blog/security-in-devin-review - Security in Review [VERIFIED]
- `DVDT-IN01-SC-DVNAI-AMPR`: https://devin.ai/blog/agentic-map-reduce - Agentic MapReduce [VERIFIED]
- `DVDT-IN01-SC-DVNAI-SWEV`: https://devin.ai/blog/security-swarm-eval - Security Swarm eval [VERIFIED]
- `DVDT-IN01-SC-CGNTN-SWRM`: https://cognition.com/blog/introducing-devin-security-swarm - Security Swarm launch [VERIFIED]
- `DVDT-IN01-SC-CGNTN-SW17`: https://cognition.com/blog/swe-1-7 - SWE-1.7 announcement [VERIFIED]
- `DVDT-IN01-SC-DVNAI-GP56`: https://devin.ai/blog/gpt-5-6 - GPT-5.6 in Devin [VERIFIED]
- `DVDT-IN01-SC-DVNAI-FB5`: https://devin.ai/blog/claude-fable-5-available-in-devin/ - Fable 5 in Devin [VERIFIED]
- `DVDT-IN01-SC-DVNAI-GM37`: https://devin.ai/blog/gemini-37-flash - Gemini 3.7 Flash in Devin [VERIFIED]
- `DVDT-IN01-SC-DVNAI-KM3`: https://devin.ai/blog/kimi-k3/ - Kimi K3 in Devin [VERIFIED]
- `DVDT-IN01-SC-ANTHR-OP5`: https://www.anthropic.com/research/claude-opus-5 - Claude Opus 5 [VERIFIED]
- `DVDT-IN01-SC-ANTHR-SN5`: https://www.anthropic.com/news/claude-sonnet-5 - Claude Sonnet 5 [VERIFIED]
- `DVDT-IN01-SC-ANTHR-REST`: https://www.anthropic.com/news/fable-mythos-access - Fable/Mythos restored [VERIFIED]
- `DVDT-IN01-SC-OPENAI-PC`: https://openai.com/index/advancing-the-price-performance-frontier-with-gpt-5-6/ - GPT-5.6 price cuts [VERIFIED]
- `DVDT-IN01-SC-ACPSP-HOME`: https://agentclientprotocol.com/ - ACP specification [VERIFIED]
- `DVDT-IN01-SC-DVNDC-ACP`: https://docs.devin.ai/desktop/acp - ACP agent setup and registry [VERIFIED]
- `DVDT-IN01-SC-DVNDC-ACPC`: https://docs.devin.ai/desktop/acp-custom - Building custom ACP agents [VERIFIED]
- `DVDT-IN01-SC-DVNDC-MCP`: https://docs.devin.ai/work-with-devin/devin-mcp - Devin MCP Server [VERIFIED]

**Secondary Sources:**
- `DVDT-IN01-SC-APIDG-WHAT`: https://apidog.com/blog/whats-new-in-devin-2026/ - Feature comparison [VERIFIED]
- `DVDT-IN01-SC-RLSBT-UPDT`: https://releasebot.io/updates/windsurf - Release aggregation [VERIFIED]
- `DVDT-IN01-SC-CLDCD-SKLL`: https://code.claude.com/docs/en/skills - Claude Code skills reference [VERIFIED]

## 19. Document History

**[2026-08-31 00:35]**
- Added: Section 17 bundled dependencies -- ripgrep 15.0.0 binary, location, features, IDE uses, failure mode

**[2026-08-31 00:10]**
- Fixed: Section 3.4 Windows ACP registry path -- documented `~/.windsurf-next/acp/` does not work on Windows
- Added: Root cause analysis of `getWindsurfConfigDirectory()` Windows branch bug
- Added: `Open Local ACP Registry Config` as recommended discovery method
- Changed: Verification labels updated to `[TESTED 2026-08-31]` for path findings

**[2026-08-30 23:50]**
- Changed: Section 3.4 ACP registry paths corrected (`~/.windsurf/acp/` not `~/.devin/acp/`)
- Changed: Command Palette label "Windsurf User Settings" → "Devin User Settings"
- Added: 7 agents to compatible agents list (Amp, Google Antigravity, Auggie CLI, Autohand Code, Cline, Codebuddy Code, Agoragentic)
- Added: Custom agent registration workflow (5 steps)
- Added: ACP client limitations (session modes, terminal, distribution downloads)
- Added: `Reload ACP Connections` command, env var configuration via `...` button
- Added: `archive` and `extensions` fields to registry format example
- Added: Sources DVDT-IN01-SC-DVNDC-ACP, DVDT-IN01-SC-DVNDC-ACPC

**[2026-08-27 20:12]**
- Fixed: AP-PR-06 acronym expansions on first use (GHSA, MoE, SSE, CORS, XSS, OIDC, SAML, FedRAMP)
- Fixed: FrontierCode 1.1 → FrontierCode 1.1 Main (per source benchmark name)

**[2026-08-27 20:12]**
- Initial document recreated from template (Option B: Capability-Layer organization)
- Recreated from scratch. Previous version archived
- Applied corrections: SWE-1.7 replaces SWE-1.6, Fable 5 restored, conversation sharing now in Devin Local
- Added: Claude Opus 5, Claude Sonnet 5, GPT-5.6 (Sol/Terra/Luna), Gemini 3.7 Flash, Kimi K3
- Added: Smart permission mode, permission/agent mode independence, permission rule composition
- Added: Plugin expanded structure (rules, hooks, MCP, subagents), Devin MCP Server
- 19 sections, 27 source entries, 6 summary categories
