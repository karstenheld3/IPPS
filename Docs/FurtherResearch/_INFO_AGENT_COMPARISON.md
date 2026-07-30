<DevSystem MarkdownTablesAllowed=true EmojisAllowed=true />

# INFO: AI Coding Agent Comparison

**Doc ID**: AGNT-IN01
**Goal**: Compare Windsurf, Claude Code, OpenAI Codex CLI, GitHub Copilot, and OpenClaw features for cross-agent compatibility

**Based on:**
- [`INFO_HOW_WINDSURF_WORKS.md [WSRF-IN01]`](../INFO_HOW_WINDSURF_WORKS.md)
- [`_INFO_HOW_CLAUDE_CODE_WORKS.md [CLCD-IN01]`](_INFO_HOW_CLAUDE_CODE_WORKS.md)
- [`_INFO_HOW_CODEX_WORKS.md [CODX-IN01]`](_INFO_HOW_CODEX_WORKS.md)
- [`_INFO_HOW_COPILOT_WORKS.md [CPLT-IN01]`](_INFO_HOW_COPILOT_WORKS.md)
- [`_INFO_HOW_OPENCLAW_WORKS.md [OCLAW-IN03]`](_INFO_HOW_OPENCLAW_WORKS.md)
- [`_INFO_OPENCLAW.md [OCLAW-IN01]`](_INFO_OPENCLAW.md)

## Agent Design Goals, Scenario, Field of Application, Example Use Cases

### Windsurf

- **Goal**: AI-powered IDE for pair programming. Agentic coding assistant with deep codebase understanding.
- **Best for**: Full-stack development, refactoring, debugging
- **Not ideal for**: Mobile access, non-coding tasks
- **Fields**: Software development, code review, documentation, test writing
- **Use cases**: Build full features from descriptions, refactor legacy codebases, debug complex issues, generate tests

### Claude Code

- **Goal**: Terminal-based coding agent. "Lives in your terminal" - read, write, execute code.
- **Best for**: CLI workflows, server work, automation scripts
- **Not ideal for**: Visual debugging, GUI-dependent work
- **Fields**: DevOps, scripting, CLI automation, server management
- **Use cases**: Automate git workflows, write shell scripts, navigate codebases, create commits

### Codex CLI

- **Goal**: Secure local coding agent. Open source, sandboxed execution, minimal footprint.
- **Best for**: Security-sensitive environments, auditable AI
- **Not ideal for**: Complex IDE integrations
- **Fields**: Enterprise environments, security-conscious development, code review
- **Use cases**: Review code with security focus, sandboxed execution, offline work, audit via transcripts

### GitHub Copilot

- **Goal**: IDE-integrated code completion. Inline suggestions + chat + autonomous agent mode.
- **Best for**: Quick code completion, existing VS Code users
- **Not ideal for**: Terminal-only workflows
- **Fields**: General coding, learning, prototyping, code completion
- **Use cases**: Inline suggestions while typing, ask questions in chat, generate boilerplate, explain code

### OpenClaw

- **Goal**: Autonomous personal AI assistant. "You're becoming someone" - persistent identity across sessions.
- **Best for**: Remote access, multi-channel communication, automation
- **Not ideal for**: IDE-integrated coding (use with Windsurf)
- **Fields**: Personal automation, remote task execution, multi-platform messaging, browser automation
- **Use cases**: Remote task execution via WhatsApp, browser automation, scheduled tasks, autonomous negotiations

## Agent Comparison Summary

| Feature | Windsurf | Claude Code | Codex CLI | GitHub Copilot | OpenClaw |
|---------|----------|-------------|-----------|----------------|----------|
| **Type** | IDE | Terminal | Terminal | IDE Extension | Gateway + Multi-channel |
| **Platform** | Windows, macOS, Linux | Windows, macOS, Linux | macOS, Linux, Windows (WSL) | VS Code, Visual Studio, JetBrains | Windows, macOS, Linux |
| **Instructions** / **Rules** | `.devin/rules/*.md` | `CLAUDE.md` | `AGENTS.md` | `.github/copilot-instructions.md` | `AGENTS.md`, `SOUL.md` |
| **Commands/Workflows** | `.devin/workflows/*.md` | `.claude/commands/*.md` (legacy) | ❌ Removed (v0.117.0) | Prompt files only | Skills only (no workflows) |
| **Skills** | ✅ Yes | ✅ Yes (absorbed commands) | ✅ Yes (`.agents/skills/`) | ❌ No | ✅ Yes |
| **Subagents** | ❌ No | ✅ Yes | ✅ Yes (`/agent`) | ✅ Yes (custom agents) | ✅ Yes (`sessions_spawn`) |
| **Hooks** | ✅ Yes | ✅ Yes | ❌ No | ❌ No | ✅ Yes (webhooks) |
| **MCP Support** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ❌ No (native tools) |
| **Sandbox** | ❌ No | ❌ No | ✅ Yes (OS-level) | ❌ No | ✅ Yes (Docker/VM) |
| **Config Format** | JSON + Protobuf | JSON | TOML | JSON | JSON |

## Detailed Agent Comparison

### Instructions and Memory

| Aspect | Windsurf | Claude Code | Codex CLI | GitHub Copilot | OpenClaw |
|--------|----------|-------------|-----------|----------------|----------|
| **Global instructions file** | `~/.codeium/windsurf/global_rules.md` | `~/.claude/CLAUDE.md` | `~/.codex/AGENTS.md` | User settings only | `~/.openclaw/workspace/AGENTS.md` |
| **Project instructions file** | `.devin/rules/*.md` | `CLAUDE.md` or `.claude/CLAUDE.md` | `AGENTS.md` | `.github/copilot-instructions.md` | `<workspace>/AGENTS.md`, `SOUL.md` |
| **Local (gitignored) instructions** | Not supported | `CLAUDE.local.md` | Not supported | Not supported | Not supported |
| **Override mechanism** | Trigger-based rules | Precedence scopes | `AGENTS.override.md` | Path-specific `.instructions.md` | Bootstrap file injection |
| **Path-specific instructions** | Trigger in frontmatter | `.claude/rules/*.md` with globs | Directory-scoped `AGENTS.md` | `.github/instructions/*.instructions.md` | Not supported |
| **Auto-generated memories** | ✅ Yes (workspace-scoped) | ❌ No | ❌ No | ❌ No | ✅ Yes (`memory/YYYY-MM-DD.md`) |
| **Instruction size limit** | None documented | None documented | 32 KiB combined | None documented | None documented |

### Commands and Workflows

| Aspect | Windsurf | Claude Code | Codex CLI | GitHub Copilot | OpenClaw |
|--------|----------|-------------|-----------|----------------|----------|
| **Custom commands** | `/workflow-name` | `/command-name` (legacy) | ❌ Removed (use skills) | Not supported | `/skill-name` |
| **Command location (project)** | `.devin/workflows/*.md` | `.claude/commands/*.md` (legacy) | `.agents/skills/*/SKILL.md` | `.github/prompts/*.prompt.md` | `<workspace>/skills/*/SKILL.md` |
| **Command location (user)** | Not supported | `~/.claude/commands/*.md` (legacy) | `~/.agents/skills/*/SKILL.md` | Not supported | `~/.openclaw/skills/*/SKILL.md` |
| **Command format** | Markdown with YAML frontmatter | Markdown with arguments | ❌ Removed → SKILL.md | Markdown with YAML frontmatter | AgentSkills YAML frontmatter |
| **Built-in commands** | `/prime`, `/verify`, `/commit` | `/init`, `/memory`, `/agents` | `/review`, `/compact`, `/skills` | None | None (use skills) |

### Prompt Syntax (Agentic Language Enrichments)

| Enrichment | Windsurf | Claude Code | Codex CLI | GitHub Copilot | OpenClaw |
|------------|----------|-------------|-----------|----------------|----------|
| **File reference** | `@file` | `@file` | `@` (fuzzy picker) | `#file:name` | File tools |
| **Folder reference** | `@folder/` | `@folder/` | ❌ No | ❌ No | File tools |
| **Skill invocation** | `@skill-name` | `@skill-name` | `$skill-name` or `/skills` | N/A | `/skill-name` |
| **Web/docs search** | `@web`, `@docs` | ❌ No | `--search` flag | ❌ No | `web_search` tool |
| **Terminal reference** | `@terminal` | ❌ No | ❌ No | `@terminal` | ❌ No |
| **Conversation reference** | `@conversation` | ❌ No | ❌ No | ❌ No | Session history |
| **Workspace context** | (automatic) | (automatic) | (automatic) | `@workspace` | Bootstrap files |
| **Selection reference** | (automatic) | (automatic) | (automatic) | `#selection` | N/A |
| **Codemap reference** | `@codemap-name` | ❌ No | ❌ No | ❌ No | ❌ No |
| **Slash commands** | `/workflow-name` | `/command-name` | `/skills` + `$name` | ❌ No (use prompts) | `/skill-name` |
| **Custom prompts** | N/A | N/A | ❌ Removed (v0.117.0) | Prompt files | Skills |
| **Shell execution** | ❌ No | `!command` | `!command` | ❌ No | `exec` tool |
| **Memory shortcut** | ❌ No | `#` key (saves to CLAUDE.md) | ❌ No | ❌ No | Write to `memory/` |
| **MCP tool reference** | (automatic) | (automatic) | (automatic) | `#tool:name` | Native tools |
| **URL pasting** | ✅ Yes (fetches content) | ❌ No | ❌ No | ❌ No | `web_fetch` tool |
| **Image attachments** | ✅ Yes (drag/drop) | ✅ Yes (CLI flag) | ✅ Yes (`-i` flag) | ✅ Yes (Agent mode) | `image` tool |
| **Pipe input** | N/A | `cat file \| claude -p` | `cat file \| codex exec` | N/A | N/A |

**Key differences:**
- **Windsurf/Claude use `@`** for context references, **Copilot uses `#`** (same concept, different syntax)
- **Only terminal agents** (Claude Code, Codex) support `!bang` for direct shell execution
- **Only Windsurf** supports URL pasting with automatic content fetching
- **Only Windsurf** has `@conversation` to reference previous chat sessions

### Skills

| Aspect | Windsurf | Claude Code | Codex CLI | GitHub Copilot | OpenClaw |
|--------|----------|-------------|-----------|----------------|----------|
| **Skills supported** | ✅ Yes | ✅ Yes (absorbed commands) | ✅ Yes (absorbed prompts) | ❌ No | ✅ Yes |
| **Skill location (project)** | `.devin/skills/<name>/SKILL.md` | `.claude/skills/<name>/SKILL.md` | `.agents/skills/<name>/SKILL.md` | N/A | `<workspace>/skills/<name>/SKILL.md` |
| **Skill location (user)** | `~/.codeium/windsurf/skills/` | `~/.claude/skills/` | `~/.agents/skills/` | N/A | `~/.openclaw/skills/` |
| **Skill format** | YAML frontmatter + Markdown | YAML frontmatter + Markdown | YAML frontmatter + Markdown | N/A | AgentSkills YAML + Markdown |
| **Skill invocation** | `@skill-name` or auto-trigger | `@skill-name` or auto-trigger | `$skill-name` or auto-trigger | N/A | `/skill-name` |
| **Disable auto-invocation** | `triggers: [user]` | `disable-model-invocation: true` | `allow_implicit_invocation: false` | N/A | N/A (always explicit) |
| **Progressive disclosure** | ❌ No (full load) | ✅ Yes (3-level) | ✅ Yes (3-level) | N/A | ❌ No (full load) |

### Subagents and Custom Agents

| Aspect | Windsurf | Claude Code | Codex CLI | GitHub Copilot | OpenClaw |
|--------|----------|-------------|-----------|----------------|----------|
| **Subagents supported** | ❌ No | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Agent location (project)** | N/A | `.claude/agents/*.md` | N/A (runtime) | `.github/agents/*.agent.md` | N/A (runtime spawn) |
| **Agent location (user)** | N/A | `~/.claude/agents/*.md` | N/A (runtime) | VS Code profile folder | N/A (runtime spawn) |
| **Agent format** | N/A | Markdown with config | `/agent` command | YAML frontmatter + Markdown | `sessions_spawn` tool call |
| **Built-in agents** | N/A | Explore, Plan, General | `/agent` threads | Ask, Edit, Agent | Main + spawned sessions |
| **Agent handoffs** | N/A | Not supported | N/A | ✅ Yes (sequential workflows) | `sessions_send` messaging |

### Hooks

| Aspect | Windsurf | Claude Code | Codex CLI | GitHub Copilot | OpenClaw |
|--------|----------|-------------|-----------|----------------|----------|
| **Hooks supported** | ✅ Yes | ✅ Yes | ❌ No | ❌ No | ✅ Yes (webhooks) |
| **Hook location (project)** | `.devin/hooks.json` | `.claude/settings.json` | N/A | N/A | N/A |
| **Hook location (user)** | `~/.codeium/windsurf/hooks.json` | `~/.claude/settings.json` | N/A | N/A | `~/.openclaw/openclaw.json` |
| **PreToolUse hook** | ✅ Yes | ✅ Yes | N/A | N/A | ❌ No |
| **PostToolUse hook** | ✅ Yes | ✅ Yes | N/A | N/A | ❌ No |
| **Notification hook** | ✅ Yes | ✅ Yes | N/A | N/A | ✅ Yes (multi-channel) |
| **Session hooks** | SessionStart, SessionEnd | SessionStart, SessionEnd | N/A | N/A | Webhooks (Gmail, cron) |

### MCP Integration

| Aspect | Windsurf | Claude Code | Codex CLI | GitHub Copilot | OpenClaw |
|--------|----------|-------------|-----------|----------------|----------|
| **MCP supported** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ❌ No |
| **Config location (project)** | Not supported | `.mcp.json` | Not supported | `.vscode/mcp.json` | N/A |
| **Config location (user)** | `~/.codeium/windsurf/mcp_config.json` | `~/.claude.json` | `~/.codex/config.toml` | User settings | N/A |
| **Config format** | JSON | JSON | TOML | JSON | N/A |
| **STDIO servers** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | N/A |
| **HTTP servers** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | N/A |
| **OAuth support** | Not documented | ✅ Yes | ✅ Yes | ✅ Yes | N/A |
| **Tool allow/deny lists** | Not documented | Not documented | ✅ Yes (`enabled_tools`, `disabled_tools`) | Not documented | N/A (native tools) |

### Configuration

| Aspect | Windsurf | Claude Code | Codex CLI | GitHub Copilot | OpenClaw |
|--------|----------|-------------|-----------|----------------|----------|
| **Main config file** | `settings.json` + `user_settings.pb` | `~/.claude/settings.json` | `~/.codex/config.toml` | VS Code `settings.json` | `~/.openclaw/openclaw.json` |
| **Config format** | JSON + Protobuf binary | JSON | TOML | JSON | JSON |
| **Project config** | Not supported | `.claude/settings.json` | Not supported | `.vscode/settings.json` | `<workspace>/.openclaw/` |
| **Local (gitignored) config** | Not supported | `.claude/settings.local.json` | Not supported | Not supported | Not supported |
| **Managed/Admin config** | Not supported | `/etc/claude-code/` | `/etc/codex/*.toml` | Enterprise policies | Not supported |
| **Configuration profiles** | Not supported | Not supported | ✅ Yes (`--profile`) | Not supported | Multi-agent via `agents.list` |
| **Environment variables** | Limited | Extensive | Limited | Limited | `OPENCLAW_*` vars |

### Security and Permissions

| Aspect | Windsurf | Claude Code | Codex CLI | GitHub Copilot | OpenClaw |
|--------|----------|-------------|-----------|----------------|----------|
| **OS-level sandbox** | ❌ No | ❌ No | ✅ Yes | ❌ No | ✅ Yes (Docker/VM) |
| **Sandbox technology** | N/A | N/A | Seatbelt (macOS), Landlock+seccomp (Linux) | N/A | Docker containers |
| **Approval modes** | Auto-execution policies | Permission modes | Approval policies + sandbox modes | Agent mode permissions | `ask`, `allowlist`, `deny` |
| **Read-only mode** | Not supported | `plan` mode | `read-only` sandbox | Ask mode | `security: deny` |
| **Full auto mode** | Turbo mode | `bypassPermissions` | `--full-auto` | Agent mode | `security: full` |
| **Network control** | Not documented | Not documented | ✅ Yes (off by default) | Not documented | Sandbox network isolation |
| **Allow/deny rules** | Allowlist/Denylist for commands | Permission rules in settings | `requirements.toml` | Not supported | `safeBins`, `allowedArgs` |

### Terminal and CLI

| Aspect | Windsurf | Claude Code | Codex CLI | GitHub Copilot | OpenClaw |
|--------|----------|-------------|-----------|----------------|----------|
| **Interface type** | IDE with integrated terminal | Pure terminal (TUI) | Pure terminal (TUI) | IDE extension | Gateway + WebChat/WhatsApp/CLI |
| **CLI tool** | N/A | `claude` | `codex` | `gh copilot` (extension) | `openclaw` |
| **Non-interactive mode** | N/A | `claude -p "prompt"` | `codex exec "prompt"` | N/A | `openclaw agent "prompt"` |
| **Resume sessions** | Conversation dropdown | `claude -c` | `codex resume` | Not supported | Session keys |
| **Session storage** | Internal database | Local transcripts | `~/.codex/sessions/` | Not supported | `~/.openclaw/agents/sessions/` |
| **Shell completions** | N/A | ✅ Yes | ✅ Yes | N/A | ✅ Yes |

### Key File Locations

| File Type | Windsurf | Claude Code | Codex CLI | GitHub Copilot | OpenClaw |
|-----------|----------|-------------|-----------|----------------|----------|
| **Instructions** | `.devin/rules/*.md` | `CLAUDE.md` | `AGENTS.md` | `.github/copilot-instructions.md` | `AGENTS.md`, `SOUL.md` |
| **Commands/Workflows** | `.devin/workflows/*.md` | `.claude/commands/*.md` (legacy) | ❌ Removed → Skills | `.github/prompts/*.prompt.md` | `skills/*/SKILL.md` |
| **Skills** | `.devin/skills/*/SKILL.md` | `.claude/skills/*/SKILL.md` | `.agents/skills/*/SKILL.md` | N/A | `skills/*/SKILL.md` |
| **Agents** | N/A | `.claude/agents/*.md` | `/agent` (runtime) | `.github/agents/*.agent.md` | `sessions_spawn` (runtime) |
| **Hooks** | `.devin/hooks.json` | `.claude/settings.json` | N/A | N/A | `openclaw.json` webhooks |
| **MCP servers** | `~/.codeium/windsurf/mcp_config.json` | `.mcp.json` | `~/.codex/config.toml` | `.vscode/mcp.json` | N/A (native tools) |
| **Main config** | `%APPDATA%\Windsurf\User\settings.json` | `~/.claude/settings.json` | `~/.codex/config.toml` | VS Code settings | `~/.openclaw/openclaw.json` |

## Design Convergence: Commands Merged into Skills

The industry is converging on a unified "skills" concept that absorbs what was previously "commands" or "workflows":

| Tool | Original Model | Current Model (2026) | Separation Mechanism |
|------|---------------|---------------------|---------------------|
| Windsurf Cascade | Workflows + Skills + Rules (3 types) | Legacy, being sunset | Directory separation |
| Claude Code | Commands + Skills + Rules (3 types) | Skills absorbed Commands (v2.1.3, Jan 2026) | `disable-model-invocation: true` flag |
| Codex CLI | Prompts + AGENTS.md (2 types) | Skills absorbed Prompts (v0.117.0, Mar 2026) | `allow_implicit_invocation: false` in openai.yaml |
| Devin CLI/Local | Skills + Rules (2 types, from start) | Skills only (never had commands) | `triggers: [user]` frontmatter |

**The two conflated interaction patterns:**
1. **Command** (imperative): "Execute `/verify` NOW" - user-initiated, deterministic
2. **Skill** (declarative): "Apply this knowledge when relevant" - agent-initiated, contextual

**Why tools merged them (engineering rationale):**
- Implementation parity: both are markdown + YAML frontmatter injected as prompts
- Skills are a strict superset: add subagent execution, progressive disclosure, supporting files
- One system to maintain vs two with identical mechanics
- OpenAI (Codex): "It doesn't make sense to provide two overlapping features and mechanisms that do the same thing. The industry has rallied behind skills as a standard."

**What was lost:**
- Browsability: can't scan "my explicit commands" separately from "agent knowledge"
- Semantic clarity: "do this now" vs "know this for later" collapsed into a flag
- User mental model: directory separation (`commands/` vs `skills/`) was more intuitive than frontmatter flags

**Note:** Windsurf/Devin Desktop Cascade still maintains the original separation (workflows = user-invoked, skills = auto-invoked). This is the only remaining tool that preserves the directory-level distinction, but it is being sunset.

## Cross-Agent Compatibility Notes

### Using IPPS with Multiple Agents

- **Windsurf** - Native support for `.devin/` structure
- **Claude Code** - Copy rules to `CLAUDE.md`, workflows to `.claude/commands/`
- **Codex CLI** - Copy essential rules to `AGENTS.md`
- **GitHub Copilot** - Copy rules to `.github/copilot-instructions.md`
- **OpenClaw** - Copy rules to `AGENTS.md` + `SOUL.md`, workflows as skills

### AGENTS.md Compatibility

Both **Codex CLI** and **GitHub Copilot** support `AGENTS.md` files:
- Enable in Copilot: `"chat.useAgentsMdFile": true`
- Codex reads `AGENTS.md` automatically
- Use `AGENTS.override.md` for Codex-specific overrides

### Skills Portability

Windsurf, Claude Code, Codex CLI, and OpenClaw share compatible `SKILL.md` formats:
- Same YAML frontmatter structure (AgentSkills open standard: https://agentskills.io/)
- Invocation: `@skill-name` (Windsurf/Claude), `$skill-name` (Codex), `/skill-name` (OpenClaw)
- Vendor-neutral path: `.agents/skills/` (Codex chose this explicitly for cross-tool sharing)
- Skills can be copied between `.devin/skills/`, `.claude/skills/`, `.agents/skills/`, and `<workspace>/skills/`
- Codex confirms: symlink `~/.claude/skills/` to `~/.agents/skills/` and both products see the same skills

### OpenClaw Unique Features

- **Multi-channel**: WhatsApp, Telegram, Discord, Slack, Signal, iMessage
- **Proactive behavior**: Heartbeats, cron jobs, background tasks
- **Memory system**: Daily logs (`memory/YYYY-MM-DD.md`) + curated `MEMORY.md`
- **Browser automation**: CDP-based browser tool with accessibility snapshots
- **Remote nodes**: Control macOS/iOS/Android companion apps
- **Subagents**: Runtime `sessions_spawn` for parallel task execution
- **No MCP**: Uses native tools instead (exec, browser, web_search, etc.)

## Document History

**[2026-07-23 18:00]**
- Changed: All Codex CLI columns updated - skills now ✅, subagents now ✅, custom prompts marked removed
- Added: Codex row to Design Convergence table (v0.117.0, March 2026)
- Added: OpenAI quote to "Why tools merged" rationale
- Added: `disable auto-invocation` and `progressive disclosure` rows to Skills table
- Changed: Skills Portability updated with Codex, vendor-neutral `.agents/skills/` path, symlink tip
- Changed: Key File Locations updated for Codex

**[2026-07-23 17:30]**
- Added: "Design Convergence: Commands Merged into Skills" section documenting industry trend
- Covers: original vs current models, conflated interaction patterns, engineering rationale, what was lost
- Sources: github.com/anthropics/claude-code/issues/13115, Devin CLI docs, Windsurf docs

**[2026-02-28 10:55]**
- Added: Design Goals, Target Scenarios, Fields of Application, Example Use Cases section

**[2026-02-28 10:50]**
- Added: OpenClaw to all comparison tables (5th column)
- Added: OpenClaw Unique Features section
- Updated: Skills Portability to include OpenClaw
- Updated: Cross-Agent Compatibility Notes

**[2026-01-21 11:02]**
- Added: Prompt Syntax (Agentic Language Enrichments) comparison table
- Covers: @mentions, /commands, !bang, #references, URL pasting, images, pipe input

**[2026-01-15 09:20]**
- Added DevSystem exception tags for tables and emojis
- Replaced Yes/No with ✅/❌ emojis in all comparison tables

**[2026-01-15 08:50]**
- Initial comparison document created
- Compiled findings from all four INFO_HOW* documents
- Added Agent Comparison Summary table
- Added Detailed Agent Comparison tables by category
