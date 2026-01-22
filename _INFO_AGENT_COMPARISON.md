<DevSystem MarkdownTablesAllowed=true EmojisAllowed=true />

# INFO: AI Coding Agent Comparison

**Doc ID**: AGNT-IN01
**Goal**: Compare Windsurf, Claude Code, OpenAI Codex CLI, and GitHub Copilot features for cross-agent compatibility

**Based on:**
- `INFO_HOW_WINDSURF_WORKS.md [WSRF-IN01]`
- `INFO_HOW_CLAUDE_CODE_WORKS.md [CLCD-IN01]`
- `INFO_HOW_CODEX_WORKS.md [CODX-IN01]`
- `INFO_HOW_COPILOT_WORKS.md [CPLT-IN01]`

## Agent Comparison Summary

| Feature | Windsurf | Claude Code | Codex CLI | GitHub Copilot |
|---------|----------|-------------|-----------|----------------|
| **Type** | IDE | Terminal | Terminal | IDE Extension |
| **Platform** | Windows, macOS, Linux | Windows, macOS, Linux | macOS, Linux, Windows (WSL) | VS Code, Visual Studio, JetBrains |
| **Instructions** / **Rules** | `.windsurf/rules/*.md` | `CLAUDE.md` | `AGENTS.md` | `.github/copilot-instructions.md` |
| **Commands/Workflows** | `.windsurf/workflows/*.md` | `.claude/commands/*.md` | Custom prompts only | Prompt files only |
| **Skills** | ✅ Yes | ✅ Yes | ❌ No | ❌ No |
| **Subagents** | ❌ No | ✅ Yes | ❌ No | ✅ Yes (custom agents) |
| **Hooks** | ✅ Yes | ✅ Yes | ❌ No | ❌ No |
| **MCP Support** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Sandbox** | ❌ No | ❌ No | ✅ Yes (OS-level) | ❌ No |
| **Config Format** | JSON + Protobuf | JSON | TOML | JSON |

## Detailed Agent Comparison

### Instructions and Memory

| Aspect | Windsurf | Claude Code | Codex CLI | GitHub Copilot |
|--------|----------|-------------|-----------|----------------|
| **Global instructions file** | `~/.codeium/windsurf/global_rules.md` | `~/.claude/CLAUDE.md` | `~/.codex/AGENTS.md` | User settings only |
| **Project instructions file** | `.windsurf/rules/*.md` | `CLAUDE.md` or `.claude/CLAUDE.md` | `AGENTS.md` | `.github/copilot-instructions.md` |
| **Local (gitignored) instructions** | Not supported | `CLAUDE.local.md` | Not supported | Not supported |
| **Override mechanism** | Trigger-based rules | Precedence scopes | `AGENTS.override.md` | Path-specific `.instructions.md` |
| **Path-specific instructions** | Trigger in frontmatter | `.claude/rules/*.md` with globs | Directory-scoped `AGENTS.md` | `.github/instructions/*.instructions.md` |
| **Auto-generated memories** | ✅ Yes (workspace-scoped) | ❌ No | ❌ No | ❌ No |
| **Instruction size limit** | None documented | None documented | 32 KiB combined | None documented |

### Commands and Workflows

| Aspect | Windsurf | Claude Code | Codex CLI | GitHub Copilot |
|--------|----------|-------------|-----------|----------------|
| **Custom commands** | `/workflow-name` | `/command-name` | `/prompts: name` | Not supported |
| **Command location (project)** | `.windsurf/workflows/*.md` | `.claude/commands/*.md` | Not supported | `.github/prompts/*.prompt.md` |
| **Command location (user)** | Not supported | `~/.claude/commands/*.md` | Not supported | Not supported |
| **Command format** | Markdown with YAML frontmatter | Markdown with arguments | Not supported | Markdown with YAML frontmatter |
| **Built-in commands** | `/prime`, `/verify`, `/commit` | `/init`, `/memory`, `/agents` | `/review`, `/compact`, `/diff` | None |

### Prompt Syntax (Agentic Language Enrichments)

| Enrichment | Windsurf | Claude Code | Codex CLI | GitHub Copilot |
|------------|----------|-------------|-----------|----------------|
| **File reference** | `@file` | `@file` | `@` (fuzzy picker) | `#file:name` |
| **Folder reference** | `@folder/` | `@folder/` | ❌ No | ❌ No |
| **Skill invocation** | `@skill-name` | `@skill-name` | N/A | N/A |
| **Web/docs search** | `@web`, `@docs` | ❌ No | `--search` flag | ❌ No |
| **Terminal reference** | `@terminal` | ❌ No | ❌ No | `@terminal` |
| **Conversation reference** | `@conversation` | ❌ No | ❌ No | ❌ No |
| **Workspace context** | (automatic) | (automatic) | (automatic) | `@workspace` |
| **Selection reference** | (automatic) | (automatic) | (automatic) | `#selection` |
| **Codemap reference** | `@codemap-name` | ❌ No | ❌ No | ❌ No |
| **Slash commands** | `/workflow-name` | `/command-name` | `/command` | ❌ No (use prompts) |
| **Custom prompts** | N/A | N/A | `/prompts: name` | Prompt files |
| **Shell execution** | ❌ No | `!command` | `!command` | ❌ No |
| **Memory shortcut** | ❌ No | `#` key (saves to CLAUDE.md) | ❌ No | ❌ No |
| **MCP tool reference** | (automatic) | (automatic) | (automatic) | `#tool:name` |
| **URL pasting** | ✅ Yes (fetches content) | ❌ No | ❌ No | ❌ No |
| **Image attachments** | ✅ Yes (drag/drop) | ✅ Yes (CLI flag) | ✅ Yes (`-i` flag) | ✅ Yes (Agent mode) |
| **Pipe input** | N/A | `cat file \| claude -p` | `cat file \| codex exec` | N/A |

**Key differences:**
- **Windsurf/Claude use `@`** for context references, **Copilot uses `#`** (same concept, different syntax)
- **Only terminal agents** (Claude Code, Codex) support `!bang` for direct shell execution
- **Only Windsurf** supports URL pasting with automatic content fetching
- **Only Windsurf** has `@conversation` to reference previous chat sessions

### Skills

| Aspect | Windsurf | Claude Code | Codex CLI | GitHub Copilot |
|--------|----------|-------------|-----------|----------------|
| **Skills supported** | ✅ Yes | ✅ Yes | ❌ No | ❌ No |
| **Skill location (project)** | `.windsurf/skills/<name>/SKILL.md` | `.claude/skills/<name>/SKILL.md` | N/A | N/A |
| **Skill location (user)** | `~/.codeium/windsurf/skills/` | `~/.claude/skills/` | N/A | N/A |
| **Skill format** | YAML frontmatter + Markdown | YAML frontmatter + Markdown | N/A | N/A |
| **Skill invocation** | `@skill-name` or auto-trigger | `@skill-name` or auto-trigger | N/A | N/A |

### Subagents and Custom Agents

| Aspect | Windsurf | Claude Code | Codex CLI | GitHub Copilot |
|--------|----------|-------------|-----------|----------------|
| **Subagents supported** | ❌ No | ✅ Yes | ❌ No | ✅ Yes |
| **Agent location (project)** | N/A | `.claude/agents/*.md` | N/A | `.github/agents/*.agent.md` |
| **Agent location (user)** | N/A | `~/.claude/agents/*.md` | N/A | VS Code profile folder |
| **Agent format** | N/A | Markdown with config | N/A | YAML frontmatter + Markdown |
| **Built-in agents** | N/A | Explore, Plan, General | N/A | Ask, Edit, Agent |
| **Agent handoffs** | N/A | Not supported | N/A | ✅ Yes (sequential workflows) |

### Hooks

| Aspect | Windsurf | Claude Code | Codex CLI | GitHub Copilot |
|--------|----------|-------------|-----------|----------------|
| **Hooks supported** | ✅ Yes | ✅ Yes | ❌ No | ❌ No |
| **Hook location (project)** | `.windsurf/hooks.json` | `.claude/settings.json` | N/A | N/A |
| **Hook location (user)** | `~/.codeium/windsurf/hooks.json` | `~/.claude/settings.json` | N/A | N/A |
| **PreToolUse hook** | ✅ Yes | ✅ Yes | N/A | N/A |
| **PostToolUse hook** | ✅ Yes | ✅ Yes | N/A | N/A |
| **Notification hook** | ✅ Yes | ✅ Yes | N/A | N/A |
| **Session hooks** | SessionStart, SessionEnd | SessionStart, SessionEnd | N/A | N/A |

### MCP Integration

| Aspect | Windsurf | Claude Code | Codex CLI | GitHub Copilot |
|--------|----------|-------------|-----------|----------------|
| **MCP supported** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Config location (project)** | Not supported | `.mcp.json` | Not supported | `.vscode/mcp.json` |
| **Config location (user)** | `~/.codeium/windsurf/mcp_config.json` | `~/.claude.json` | `~/.codex/config.toml` | User settings |
| **Config format** | JSON | JSON | TOML | JSON |
| **STDIO servers** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **HTTP servers** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **OAuth support** | Not documented | ✅ Yes | ✅ Yes | ✅ Yes |
| **Tool allow/deny lists** | Not documented | Not documented | ✅ Yes (`enabled_tools`, `disabled_tools`) | Not documented |

### Configuration

| Aspect | Windsurf | Claude Code | Codex CLI | GitHub Copilot |
|--------|----------|-------------|-----------|----------------|
| **Main config file** | `settings.json` + `user_settings.pb` | `~/.claude/settings.json` | `~/.codex/config.toml` | VS Code `settings.json` |
| **Config format** | JSON + Protobuf binary | JSON | TOML | JSON |
| **Project config** | Not supported | `.claude/settings.json` | Not supported | `.vscode/settings.json` |
| **Local (gitignored) config** | Not supported | `.claude/settings.local.json` | Not supported | Not supported |
| **Managed/Admin config** | Not supported | `/etc/claude-code/` | `/etc/codex/*.toml` | Enterprise policies |
| **Configuration profiles** | Not supported | Not supported | ✅ Yes (`--profile`) | Not supported |
| **Environment variables** | Limited | Extensive | Limited | Limited |

### Security and Permissions

| Aspect | Windsurf | Claude Code | Codex CLI | GitHub Copilot |
|--------|----------|-------------|-----------|----------------|
| **OS-level sandbox** | ❌ No | ❌ No | ✅ Yes | ❌ No |
| **Sandbox technology** | N/A | N/A | Seatbelt (macOS), Landlock+seccomp (Linux) | N/A |
| **Approval modes** | Auto-execution policies | Permission modes | Approval policies + sandbox modes | Agent mode permissions |
| **Read-only mode** | Not supported | `plan` mode | `read-only` sandbox | Ask mode |
| **Full auto mode** | Turbo mode | `bypassPermissions` | `--full-auto` | Agent mode |
| **Network control** | Not documented | Not documented | ✅ Yes (off by default) | Not documented |
| **Allow/deny rules** | Allowlist/Denylist for commands | Permission rules in settings | `requirements.toml` | Not supported |

### Terminal and CLI

| Aspect | Windsurf | Claude Code | Codex CLI | GitHub Copilot |
|--------|----------|-------------|-----------|----------------|
| **Interface type** | IDE with integrated terminal | Pure terminal (TUI) | Pure terminal (TUI) | IDE extension |
| **CLI tool** | N/A | `claude` | `codex` | `gh copilot` (extension) |
| **Non-interactive mode** | N/A | `claude -p "prompt"` | `codex exec "prompt"` | N/A |
| **Resume sessions** | Conversation dropdown | `claude -c` | `codex resume` | Not supported |
| **Session storage** | Internal database | Local transcripts | `~/.codex/sessions/` | Not supported |
| **Shell completions** | N/A | ✅ Yes | ✅ Yes | N/A |

### Key File Locations

| File Type | Windsurf | Claude Code | Codex CLI | GitHub Copilot |
|-----------|----------|-------------|-----------|----------------|
| **Instructions** | `.windsurf/rules/*.md` | `CLAUDE.md` | `AGENTS.md` | `.github/copilot-instructions.md` |
| **Commands/Workflows** | `.windsurf/workflows/*.md` | `.claude/commands/*.md` | N/A | `.github/prompts/*.prompt.md` |
| **Skills** | `.windsurf/skills/*/SKILL.md` | `.claude/skills/*/SKILL.md` | N/A | N/A |
| **Agents** | N/A | `.claude/agents/*.md` | N/A | `.github/agents/*.agent.md` |
| **Hooks** | `.windsurf/hooks.json` | `.claude/settings.json` | N/A | N/A |
| **MCP servers** | `~/.codeium/windsurf/mcp_config.json` | `.mcp.json` | `~/.codex/config.toml` | `.vscode/mcp.json` |
| **Main config** | `%APPDATA%\Windsurf\User\settings.json` | `~/.claude/settings.json` | `~/.codex/config.toml` | VS Code settings |

## Cross-Agent Compatibility Notes

### Using IPPS with Multiple Agents

- **Windsurf** - Native support for `.windsurf/` structure
- **Claude Code** - Copy rules to `CLAUDE.md`, workflows to `.claude/commands/`
- **Codex CLI** - Copy essential rules to `AGENTS.md`
- **GitHub Copilot** - Copy rules to `.github/copilot-instructions.md`

### AGENTS.md Compatibility

Both **Codex CLI** and **GitHub Copilot** support `AGENTS.md` files:
- Enable in Copilot: `"chat.useAgentsMdFile": true`
- Codex reads `AGENTS.md` automatically
- Use `AGENTS.override.md` for Codex-specific overrides

### Skills Portability

Windsurf and Claude Code share the same `SKILL.md` format:
- Same YAML frontmatter structure
- Same invocation pattern (`@skill-name`)
- Skills can be copied between `.windsurf/skills/` and `.claude/skills/`

## Document History

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
