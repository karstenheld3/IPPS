<DevSystem MarkdownTablesAllowed=true EmojisAllowed=true />

# INFO: AI Coding Agent Comparison

**Doc ID**: AGNT-IN01
**Goal**: Compare Windsurf, Claude Code, OpenAI Codex CLI, GitHub Copilot, OpenClaw, and Meta Muse Code features for cross-agent compatibility

**Based on:**
- [`INFO_HOW_WINDSURF_WORKS.md [WSRF-IN01]`](../INFO_HOW_WINDSURF_WORKS.md)
- [`_INFO_HOW_CLAUDE_CODE_WORKS.md [CLCD-IN01]`](_INFO_HOW_CLAUDE_CODE_WORKS.md)
- [`_INFO_HOW_CODEX_WORKS.md [CODX-IN01]`](_INFO_HOW_CODEX_WORKS.md)
- [`_INFO_HOW_COPILOT_WORKS.md [CPLT-IN01]`](_INFO_HOW_COPILOT_WORKS.md)
- [`_INFO_HOW_OPENCLAW_WORKS.md [OCLAW-IN03]`](_INFO_HOW_OPENCLAW_WORKS.md)
- [`_INFO_OPENCLAW.md [OCLAW-IN01]`](_INFO_OPENCLAW.md)
- [Introducing Muse Code and Muse Spark 1.2](https://research.meta.ai/blog/introducing-muse-code-and-muse-spark-1-2) (Meta, 2026-08-05)
- [Muse Code Docs](https://dev.meta.ai/docs/muse-code) (Meta Developer)

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

### Muse Code

- **Goal**: Terminal coding agent with persistent background agents. Co-trained model + harness for repository-scale execution.
- **Best for**: Long-horizon tasks, kernel optimization, multi-file refactors, CI pipelines
- **Not ideal for**: Windows users, IDE-integrated workflows (no VS Code extension)
- **Fields**: Large codebase engineering, GPU kernel optimization, multi-step debugging, CI/CD
- **Use cases**: Fan-out subagents across worktrees, plan-then-execute with approval gates, stress-test plans with `/grill`, long-running autonomous goals

## Agent Comparison Summary

| Feature | Windsurf | Claude Code | Codex CLI | GitHub Copilot | OpenClaw | Muse Code |
|---------|----------|-------------|-----------|----------------|----------|----------|
| **Type** | IDE | Terminal | Terminal | IDE Extension | Gateway + Multi-channel | Terminal |
| **Platform** | Windows, macOS, Linux | Windows, macOS, Linux | macOS, Linux, Windows (WSL) | VS Code, Visual Studio, JetBrains | Windows, macOS, Linux | macOS, Linux |
| **Instructions** / **Rules** | `.devin/rules/*.md` | `CLAUDE.md` | `AGENTS.md` | `.github/copilot-instructions.md` | `AGENTS.md`, `SOUL.md` | `AGENTS.md` (falls back to `CLAUDE.md`) |
| **Commands/Workflows** | `.devin/workflows/*.md` | `.claude/commands/*.md` (legacy) | ❌ Removed (v0.117.0) | Prompt files only | Skills only (no workflows) | Skills only (no workflows) |
| **Skills** | ✅ Yes | ✅ Yes (absorbed commands) | ✅ Yes (`.agents/skills/`) | ❌ No | ✅ Yes | ✅ Yes (`.agents/skills/`) |
| **Subagents** | ❌ No | ✅ Yes | ✅ Yes (`/agent`) | ✅ Yes (custom agents) | ✅ Yes (`sessions_spawn`) | ✅ Yes (worktree-isolated) |
| **Hooks** | ✅ Yes | ✅ Yes | ❌ No | ❌ No | ✅ Yes (webhooks) | ✅ Yes |
| **MCP Support** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ❌ No (native tools) | ✅ Yes |
| **Sandbox** | ❌ No | ❌ No | ✅ Yes (OS-level) | ❌ No | ✅ Yes (Docker/VM) | ✅ Yes (OS-level, on by default) |
| **Config Format** | JSON + Protobuf | JSON | TOML | JSON | JSON | JSON |

## Detailed Agent Comparison

### Instructions and Memory

| Aspect | Windsurf | Claude Code | Codex CLI | GitHub Copilot | OpenClaw | Muse Code |
|--------|----------|-------------|-----------|----------------|----------|----------|
| **Global instructions file** | `~/.codeium/windsurf/global_rules.md` | `~/.claude/CLAUDE.md` | `~/.codex/AGENTS.md` | User settings only | `~/.openclaw/workspace/AGENTS.md` | `~/.config/muse/settings.json` (also loads `~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`) |
| **Project instructions file** | `.devin/rules/*.md` | `CLAUDE.md` or `.claude/CLAUDE.md` | `AGENTS.md` | `.github/copilot-instructions.md` | `<workspace>/AGENTS.md`, `SOUL.md` | `AGENTS.md` (falls back to `CLAUDE.md`) |
| **Local (gitignored) instructions** | Not supported | `CLAUDE.local.md` | Not supported | Not supported | Not supported | Not supported |
| **Override mechanism** | Trigger-based rules | Precedence scopes | `AGENTS.override.md` | Path-specific `.instructions.md` | Bootstrap file injection | Deeper file wins over shallower |
| **Path-specific instructions** | Trigger in frontmatter | `.claude/rules/*.md` with globs | Directory-scoped `AGENTS.md` | `.github/instructions/*.instructions.md` | Not supported | Directory-scoped `AGENTS.md` (walks up to `.git` boundary) |
| **Auto-generated memories** | ✅ Yes (workspace-scoped) | ❌ No | ❌ No | ❌ No | ✅ Yes (`memory/YYYY-MM-DD.md`) | ✅ Yes (observer agents: memory recall, skill recall) |
| **Instruction size limit** | None documented | None documented | 32 KiB combined | None documented | None documented | None documented |

### Commands and Workflows

| Aspect | Windsurf | Claude Code | Codex CLI | GitHub Copilot | OpenClaw | Muse Code |
|--------|----------|-------------|-----------|----------------|----------|----------|
| **Custom commands** | `/workflow-name` | `/command-name` (legacy) | ❌ Removed (use skills) | Not supported | `/skill-name` | `/skill <name>` |
| **Command location (project)** | `.devin/workflows/*.md` | `.claude/commands/*.md` (legacy) | `.agents/skills/*/SKILL.md` | `.github/prompts/*.prompt.md` | `<workspace>/skills/*/SKILL.md` | `.agents/skills/*/SKILL.md` |
| **Command location (user)** | Not supported | `~/.claude/commands/*.md` (legacy) | `~/.agents/skills/*/SKILL.md` | Not supported | `~/.openclaw/skills/*/SKILL.md` | `~/.config/muse/skills/` and `~/.agents/skills/` |
| **Command format** | Markdown with YAML frontmatter | Markdown with arguments | ❌ Removed → SKILL.md | Markdown with YAML frontmatter | AgentSkills YAML frontmatter | SKILL.md (AgentSkills format) |
| **Built-in commands** | `/prime`, `/verify`, `/commit` | `/init`, `/memory`, `/agents` | `/review`, `/compact`, `/skills` | None | None (use skills) | `/goal`, `/compact`, `/fork`, `/side`, `/effort` |

### Prompt Syntax (Agentic Language Enrichments)

| Enrichment | Windsurf | Claude Code | Codex CLI | GitHub Copilot | OpenClaw | Muse Code |
|------------|----------|-------------|-----------|----------------|----------|----------|
| **File reference** | `@file` | `@file` | `@` (fuzzy picker) | `#file:name` | File tools | `@` (path autocomplete) |
| **Folder reference** | `@folder/` | `@folder/` | ❌ No | ❌ No | File tools | ❌ No |
| **Skill invocation** | `@skill-name` | `@skill-name` | `$skill-name` or `/skills` | N/A | `/skill-name` | `/skill <name>` |
| **Web/docs search** | `@web`, `@docs` | ❌ No | `--search` flag | ❌ No | `web_search` tool | ❌ No |
| **Terminal reference** | `@terminal` | ❌ No | ❌ No | `@terminal` | ❌ No | ❌ No |
| **Conversation reference** | `@conversation` | ❌ No | ❌ No | ❌ No | Session history | ❌ No |
| **Workspace context** | (automatic) | (automatic) | (automatic) | `@workspace` | Bootstrap files | (automatic, after trust) |
| **Selection reference** | (automatic) | (automatic) | (automatic) | `#selection` | N/A | N/A |
| **Codemap reference** | `@codemap-name` | ❌ No | ❌ No | ❌ No | ❌ No | ❌ No |
| **Slash commands** | `/workflow-name` | `/command-name` | `/skills` + `$name` | ❌ No (use prompts) | `/skill-name` | `/goal`, `/compact`, `/fork`, `/side` |
| **Custom prompts** | N/A | N/A | ❌ Removed (v0.117.0) | Prompt files | Skills | Skills |
| **Shell execution** | ❌ No | `!command` | `!command` | ❌ No | `exec` tool | `!command` |
| **Memory shortcut** | ❌ No | `#` key (saves to CLAUDE.md) | ❌ No | ❌ No | Write to `memory/` | ❌ No |
| **MCP tool reference** | (automatic) | (automatic) | (automatic) | `#tool:name` | Native tools | (automatic) |
| **URL pasting** | ✅ Yes (fetches content) | ❌ No | ❌ No | ❌ No | `web_fetch` tool | ❌ No |
| **Image attachments** | ✅ Yes (drag/drop) | ✅ Yes (CLI flag) | ✅ Yes (`-i` flag) | ✅ Yes (Agent mode) | `image` tool | ✅ Yes (`-i` flag) |
| **Pipe input** | N/A | `cat file \| claude -p` | `cat file \| codex exec` | N/A | N/A | `--prompt-file` |

**Key differences:**
- **Windsurf/Claude use `@`** for context references, **Copilot uses `#`** (same concept, different syntax)
- **Terminal agents** (Claude Code, Codex, Muse Code) support `!bang` for direct shell execution
- **Only Windsurf** supports URL pasting with automatic content fetching
- **Only Windsurf** has `@conversation` to reference previous chat sessions

### Skills

| Aspect | Windsurf | Claude Code | Codex CLI | GitHub Copilot | OpenClaw | Muse Code |
|--------|----------|-------------|-----------|----------------|----------|----------|
| **Skills supported** | ✅ Yes | ✅ Yes (absorbed commands) | ✅ Yes (absorbed prompts) | ❌ No | ✅ Yes | ✅ Yes |
| **Skill location (project)** | `.devin/skills/<name>/SKILL.md` | `.claude/skills/<name>/SKILL.md` | `.agents/skills/<name>/SKILL.md` | N/A | `<workspace>/skills/<name>/SKILL.md` | `.agents/skills/<name>/SKILL.md` (also scans `.codex/skills`, `.claude/skills`) |
| **Skill location (user)** | `~/.codeium/windsurf/skills/` | `~/.claude/skills/` | `~/.agents/skills/` | N/A | `~/.openclaw/skills/` | `~/.config/muse/skills/` and `~/.agents/skills/` |
| **Skill format** | YAML frontmatter + Markdown | YAML frontmatter + Markdown | YAML frontmatter + Markdown | N/A | AgentSkills YAML + Markdown | YAML frontmatter + Markdown (AgentSkills) |
| **Skill invocation** | `@skill-name` or auto-trigger | `@skill-name` or auto-trigger | `$skill-name` or auto-trigger | N/A | `/skill-name` | `/skill <name>` or observer auto-trigger |
| **Disable auto-invocation** | `triggers: [user]` | `disable-model-invocation: true` | `allow_implicit_invocation: false` | N/A | N/A (always explicit) | Not documented |
| **Progressive disclosure** | ❌ No (full load) | ✅ Yes (3-level) | ✅ Yes (3-level) | N/A | ❌ No (full load) | Not documented |
| **Skill import** | N/A | N/A | N/A | N/A | N/A | `muse skills import --from claude\|codex` |

### Subagents and Custom Agents

| Aspect | Windsurf | Claude Code | Codex CLI | GitHub Copilot | OpenClaw | Muse Code |
|--------|----------|-------------|-----------|----------------|----------|----------|
| **Subagents supported** | ❌ No | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Agent location (project)** | N/A | `.claude/agents/*.md` | N/A (runtime) | `.github/agents/*.agent.md` | N/A (runtime spawn) | N/A (runtime spawn) |
| **Agent location (user)** | N/A | `~/.claude/agents/*.md` | N/A (runtime) | VS Code profile folder | N/A (runtime spawn) | N/A (runtime spawn) |
| **Agent format** | N/A | Markdown with config | `/agent` command | YAML frontmatter + Markdown | `sessions_spawn` tool call | `subagent_spawn` tool call |
| **Built-in agents** | N/A | Explore, Plan, General | `/agent` threads | Ask, Edit, Agent | Main + spawned sessions | 4 observer agents (memory, skill, goal, verification) |
| **Agent handoffs** | N/A | Not supported | N/A | ✅ Yes (sequential workflows) | `sessions_send` messaging | `subagent_send_message` |
| **Worktree isolation** | N/A | ✅ Yes (`isolation: worktree`) | ❌ No | ❌ No | ❌ No | ✅ Yes (`--subagent-worktree-isolation`) |
| **Nesting depth** | N/A | Multi-level | Multi-level | Sequential | Multi-level | One level only |

### Hooks

| Aspect | Windsurf | Claude Code | Codex CLI | GitHub Copilot | OpenClaw | Muse Code |
|--------|----------|-------------|-----------|----------------|----------|----------|
| **Hooks supported** | ✅ Yes | ✅ Yes | ❌ No | ❌ No | ✅ Yes (webhooks) | ✅ Yes |
| **Hook location (project)** | `.devin/hooks.json` | `.claude/settings.json` | N/A | N/A | N/A | `.muse/hooks.json` |
| **Hook location (user)** | `~/.codeium/windsurf/hooks.json` | `~/.claude/settings.json` | N/A | N/A | `~/.openclaw/openclaw.json` | `~/.config/muse/settings.json` |
| **Managed hooks** | Not supported | Not supported | N/A | N/A | N/A | ✅ Yes (`managed_hooks_path`, pre-approved) |
| **PreToolUse hook** | ✅ Yes | ✅ Yes | N/A | N/A | ❌ No | ✅ Yes |
| **PostToolUse hook** | ✅ Yes | ✅ Yes | N/A | N/A | ❌ No | ✅ Yes |
| **Notification hook** | ✅ Yes | ✅ Yes | N/A | N/A | ✅ Yes (multi-channel) | ✅ Yes (Stop event) |
| **Session hooks** | SessionStart, SessionEnd | SessionStart, SessionEnd | N/A | N/A | Webhooks (Gmail, cron) | SessionStart, SubagentStart/Stop, Stop |
| **LLM lifecycle hooks** | ❌ No | ❌ No | N/A | N/A | ❌ No | ✅ Yes (PreLLMCall, PostLLMCall, PreCompact, PostCompact) |

### MCP Integration

| Aspect | Windsurf | Claude Code | Codex CLI | GitHub Copilot | OpenClaw | Muse Code |
|--------|----------|-------------|-----------|----------------|----------|----------|
| **MCP supported** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ❌ No | ✅ Yes |
| **Config location (project)** | Not supported | `.mcp.json` | Not supported | `.vscode/mcp.json` | N/A | Not documented |
| **Config location (user)** | `~/.codeium/windsurf/mcp_config.json` | `~/.claude.json` | `~/.codex/config.toml` | User settings | N/A | `~/.config/muse/settings.json` |
| **Config format** | JSON | JSON | TOML | JSON | N/A | JSON |
| **STDIO servers** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | N/A | ✅ Yes |
| **HTTP servers** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | N/A | ✅ Yes (streamable HTTP) |
| **OAuth support** | Not documented | ✅ Yes | ✅ Yes | ✅ Yes | N/A | Not documented |
| **Tool allow/deny lists** | Not documented | Not documented | ✅ Yes (`enabled_tools`, `disabled_tools`) | Not documented | N/A (native tools) | Not documented |

### Configuration

| Aspect | Windsurf | Claude Code | Codex CLI | GitHub Copilot | OpenClaw | Muse Code |
|--------|----------|-------------|-----------|----------------|----------|----------|
| **Main config file** | `settings.json` + `user_settings.pb` | `~/.claude/settings.json` | `~/.codex/config.toml` | VS Code `settings.json` | `~/.openclaw/openclaw.json` | `~/.config/muse/settings.json` |
| **Config format** | JSON + Protobuf binary | JSON | TOML | JSON | JSON | JSON (`schema_version: 1` required) |
| **Project config** | Not supported | `.claude/settings.json` | Not supported | `.vscode/settings.json` | `<workspace>/.openclaw/` | `.muse/` |
| **Local (gitignored) config** | Not supported | `.claude/settings.local.json` | Not supported | Not supported | Not supported | Not supported |
| **Managed/Admin config** | Not supported | `/etc/claude-code/` | `/etc/codex/*.toml` | Enterprise policies | Not supported | ✅ Yes (`managed_hooks_path`) |
| **Configuration profiles** | Not supported | Not supported | ✅ Yes (`--profile`) | Not supported | Multi-agent via `agents.list` | Not supported |
| **Environment variables** | Limited | Extensive | Limited | Limited | `OPENCLAW_*` vars | `META_API_KEY` |

### Security and Permissions

| Aspect | Windsurf | Claude Code | Codex CLI | GitHub Copilot | OpenClaw | Muse Code |
|--------|----------|-------------|-----------|----------------|----------|----------|
| **OS-level sandbox** | ❌ No | ❌ No | ✅ Yes | ❌ No | ✅ Yes (Docker/VM) | ✅ Yes (on by default, fails closed) |
| **Sandbox technology** | N/A | N/A | Seatbelt (macOS), Landlock+seccomp (Linux) | N/A | Docker containers | Seatbelt (macOS), bubblewrap (Linux) |
| **Approval modes** | Auto-execution policies | Permission modes | Approval policies + sandbox modes | Agent mode permissions | `ask`, `allowlist`, `deny` | `on-request` (default), `untrusted`, `never` |
| **Read-only mode** | Not supported | `plan` mode | `read-only` sandbox | Ask mode | `security: deny` | `--disable-write --disable-shell` |
| **Full auto mode** | Turbo mode | `bypassPermissions` | `--full-auto` | Agent mode | `security: full` | `--yolo` (disables approval + sandbox) |
| **Network control** | Not documented | Not documented | ✅ Yes (off by default) | Not documented | Sandbox network isolation | ✅ Yes (`proxy-only` default, `restricted`, `enabled`) |
| **Allow/deny rules** | Allowlist/Denylist for commands | Permission rules in settings | `requirements.toml` | Not supported | `safeBins`, `allowedArgs` | Staged shell review (per-command argv-prefix rules) |

### Terminal and CLI

| Aspect | Windsurf | Claude Code | Codex CLI | GitHub Copilot | OpenClaw | Muse Code |
|--------|----------|-------------|-----------|----------------|----------|----------|
| **Interface type** | IDE with integrated terminal | Pure terminal (TUI) | Pure terminal (TUI) | IDE extension | Gateway + WebChat/WhatsApp/CLI | Pure terminal (TUI) |
| **CLI tool** | N/A | `claude` | `codex` | `gh copilot` (extension) | `openclaw` | `muse` |
| **Non-interactive mode** | N/A | `claude -p "prompt"` | `codex exec "prompt"` | N/A | `openclaw agent "prompt"` | `muse exec "prompt"` |
| **Resume sessions** | Conversation dropdown | `claude -c` | `codex resume` | Not supported | Session keys | `muse resume` (`--last` or UUID) |
| **Session storage** | Internal database | Local transcripts | `~/.codex/sessions/` | Not supported | `~/.openclaw/agents/sessions/` | Append-only event log (date-stamped, replay-exact) |
| **Shell completions** | N/A | ✅ Yes | ✅ Yes | N/A | ✅ Yes | Not documented |
| **Session branching** | ❌ No | ❌ No | ❌ No | ❌ No | ❌ No | ✅ Yes (`/fork`, `/side`) |

### Key File Locations

| File Type | Windsurf | Claude Code | Codex CLI | GitHub Copilot | OpenClaw | Muse Code |
|-----------|----------|-------------|-----------|----------------|----------|----------|
| **Instructions** | `.devin/rules/*.md` | `CLAUDE.md` | `AGENTS.md` | `.github/copilot-instructions.md` | `AGENTS.md`, `SOUL.md` | `AGENTS.md` |
| **Commands/Workflows** | `.devin/workflows/*.md` | `.claude/commands/*.md` (legacy) | ❌ Removed → Skills | `.github/prompts/*.prompt.md` | `skills/*/SKILL.md` | Skills only |
| **Skills** | `.devin/skills/*/SKILL.md` | `.claude/skills/*/SKILL.md` | `.agents/skills/*/SKILL.md` | N/A | `skills/*/SKILL.md` | `.agents/skills/*/SKILL.md` |
| **Agents** | N/A | `.claude/agents/*.md` | `/agent` (runtime) | `.github/agents/*.agent.md` | `sessions_spawn` (runtime) | `subagent_spawn` (runtime) |
| **Hooks** | `.devin/hooks.json` | `.claude/settings.json` | N/A | N/A | `openclaw.json` webhooks | `.muse/hooks.json` |
| **MCP servers** | `~/.codeium/windsurf/mcp_config.json` | `.mcp.json` | `~/.codex/config.toml` | `.vscode/mcp.json` | N/A (native tools) | `~/.config/muse/settings.json` |
| **Main config** | `%APPDATA%\Windsurf\User\settings.json` | `~/.claude/settings.json` | `~/.codex/config.toml` | VS Code settings | `~/.openclaw/openclaw.json` | `~/.config/muse/settings.json` |

## Design Convergence: Commands Merged into Skills

The industry is converging on a unified "skills" concept that absorbs what was previously "commands" or "workflows":

| Tool | Original Model | Current Model (2026) | Separation Mechanism |
|------|---------------|---------------------|---------------------|
| Windsurf Cascade | Workflows + Skills + Rules (3 types) | Legacy, being sunset | Directory separation |
| Claude Code | Commands + Skills + Rules (3 types) | Skills absorbed Commands (v2.1.3, Jan 2026) | `disable-model-invocation: true` flag |
| Codex CLI | Prompts + AGENTS.md (2 types) | Skills absorbed Prompts (v0.117.0, Mar 2026) | `allow_implicit_invocation: false` in openai.yaml |
| Devin CLI/Local | Skills + Rules (2 types, from start) | Skills only (never had commands) | `triggers: [user]` frontmatter |
| Muse Code | Skills only (from start, Aug 2026) | Skills only (never had commands) | Observer agents auto-trigger skills |

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
- **Muse Code** - Uses `AGENTS.md` natively, falls back to `CLAUDE.md`; `muse skills import --from claude|codex` migrates skills

### AGENTS.md Compatibility

**Codex CLI**, **GitHub Copilot**, and **Muse Code** support `AGENTS.md` files:
- Enable in Copilot: `"chat.useAgentsMdFile": true`
- Codex reads `AGENTS.md` automatically
- Muse Code reads `AGENTS.md` automatically, falls back to `CLAUDE.md` if no `AGENTS.md` found
- Use `AGENTS.override.md` for Codex-specific overrides

### Skills Portability

Windsurf, Claude Code, Codex CLI, OpenClaw, and Muse Code share compatible `SKILL.md` formats:
- Same YAML frontmatter structure (AgentSkills open standard: https://agentskills.io/)
- Invocation: `@skill-name` (Windsurf/Claude), `$skill-name` (Codex), `/skill-name` (OpenClaw), `/skill <name>` (Muse Code)
- Vendor-neutral path: `.agents/skills/` (Codex chose this explicitly for cross-tool sharing)
- Skills can be copied between `.devin/skills/`, `.claude/skills/`, `.agents/skills/`, and `<workspace>/skills/`
- Codex confirms: symlink `~/.claude/skills/` to `~/.agents/skills/` and both products see the same skills
- Muse Code scans `.agents/skills/`, `.codex/skills/`, and `.claude/skills/` automatically; `muse skills import --from claude|codex` handles migration

### OpenClaw Unique Features

- **Multi-channel**: WhatsApp, Telegram, Discord, Slack, Signal, iMessage
- **Proactive behavior**: Heartbeats, cron jobs, background tasks
- **Memory system**: Daily logs (`memory/YYYY-MM-DD.md`) + curated `MEMORY.md`
- **Browser automation**: CDP-based browser tool with accessibility snapshots
- **Remote nodes**: Control macOS/iOS/Android companion apps
- **Subagents**: Runtime `sessions_spawn` for parallel task execution
- **No MCP**: Uses native tools instead (exec, browser, web_search, etc.)

### Muse Code Unique Features

- **Persistent observer agents**: 4 background agents (memory recall, skill recall, goal tracking, verification) run throughout each session, making their own model calls. Toggled via `runtime_capabilities` in settings [VERIFIED]
- **Worktree-isolated subagents**: Fan-out spawns a git worktree per child under `.muse/worktrees/` in detached HEAD. Children cannot collide on files. Requires git repo; silently ignored without one [VERIFIED]
- **Append-only event log**: Every model call, tool run, approval, and edit is appended to a local log. Replay-exact and restart-safe: after a crash, the agent resumes where it stopped [VERIFIED]
- **Staged shell review**: Compound commands reviewed stage by stage, not as one line. Reject one stage and nothing runs, not even safe stages before it [VERIFIED]
- **Co-trained model**: Muse Spark 1.2 co-trained with Muse Code harness for optimal coding usability. Includes rejection-sampled trajectories, goal conditioning, and context compaction training [VERIFIED]
- **Session branching**: `/fork` branches a new session from current state; `/side` opens a parallel conversation that leaves the main thread untouched [VERIFIED]
- **Skill import**: `muse skills import --from claude|codex` migrates existing skills from other agents. Also scans `.claude/skills/` and `.codex/skills/` automatically [VERIFIED]
- **Managed hooks**: Central administration via `managed_hooks_path` - hooks that run without per-user trust step [VERIFIED]
- **Network sandboxing**: `proxy-only` default stops for review on first connection to new host/port; `restricted` blocks all network; `enabled` allows full egress [VERIFIED]
- **No Windows support**: macOS and Linux only (beta, Aug 2026) [VERIFIED]
- **Pricing**: $1.25/$4.25 per million tokens (input/output); $0.10/$0.20 if training data sharing enabled. No subscription tier [VERIFIED]

## Document History

**[2026-08-13 16:25]**
- Added: Muse Code (Meta) as 6th agent across all comparison tables
- Added: Muse Code design goals, unique features section
- Added: Muse Code row to Design Convergence table
- Updated: Cross-Agent Compatibility Notes and Skills Portability for Muse Code
- Updated: Key differences to include Muse Code terminal agent `!bang` support
- Added: New rows to Subagents table (Worktree isolation, Nesting depth)
- Added: New rows to Hooks table (Managed hooks, LLM lifecycle hooks)
- Added: New row to Terminal/CLI table (Session branching)
- Added: New row to Skills table (Skill import)
- Sources: https://research.meta.ai/blog/introducing-muse-code-and-muse-spark-1-2, https://dev.meta.ai/docs/muse-code, https://codersera.com/blog/muse-code-complete-guide-2026/

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
