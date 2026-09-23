# INFO: How Claude Code Works

**Doc ID**: CLCD-IN01
**Goal**: Document Claude Code features, configuration, and integration for cross-agent compatibility reference
**Timeline**: Created 2026-01-15, Updated 8 times (2026-01-15 - 2026-09-21)

## Summary

Key findings for cross-agent compatibility:
- Current version: **2.1.278** (2.1.277 shipped 2026-09-18). Default models: Claude Sonnet 5 / Opus 5 / Fable 5.1, all with 1M-token context [VERIFIED 2026-09-21]
- Commands merged into Skills (v2.1.3, Jan 2026). `.claude/commands/` still works (same frontmatter except `name` and `paths`), but skills are the recommended format [VERIFIED]
- Skills in `.claude/skills/<name>/SKILL.md` following the [Agent Skills open standard](https://agentskills.io) [VERIFIED]
- Discovery precedence: enterprise > personal (`~/.claude/skills/`) > project (`.claude/skills/`); a skill beats a same-named command file; plugin skills namespaced `/plugin:skill` [VERIFIED 2026-09-21]
- `disable-model-invocation: true` makes a skill user-only AND removes description from agent context (zero tokens) [VERIFIED]
- `user-invocable: false` hides from `/` menu but keeps in agent context (shadow tool risk) [VERIFIED]
- Progressive disclosure: only name+description in context at startup (~100 tokens/skill, truncated at 1,536 chars), full body on invocation, supporting files on demand [VERIFIED 2026-09-21]
- Listing budget tunable: `skillListingBudgetFraction` (default 0.01 = 1% of context window; 0.02 is the documented raise example), `skillListingMaxDescChars` (default 1,536); `/reload-skills` re-scans directories without restart; `claude plugin validate .claude/skills` checks SKILL.md [VERIFIED 2026-09-21]
- Skill-selection degrades with auto-invocable skill count: -8 pass points at 52 skills, -21 at 202 (skill shadowing dominates, context overhead negligible); user-only skills bypass selection entirely [VERIFIED 2026-09-21]
- Skill content persists across turns; auto-compaction re-attaches first 5,000 tokens per skill (25,000 combined) [VERIFIED 2026-09-21]
- Dynamic context injection: `` !`command` `` runs before skill content reaches Claude; `shell: powershell` frontmatter for Windows [VERIFIED 2026-09-21]
- `.claude/rules/*.md` rule files with optional `paths:` frontmatter - loaded alongside CLAUDE.md (equivalent to Windsurf rules) [VERIFIED 2026-09-21]
- AGENTS.md read when no CLAUDE.md exists (v2.1.277); `/config` Project instructions selects mode [VERIFIED 2026-09-21]
- Auto memory in `~/.claude/projects/<project>/memory/` accumulates learnings automatically [VERIFIED 2026-09-21]
- Plugins bundle skills/agents/hooks/MCP/LSP/monitors under namespace (`/plugin:skill`), installable via marketplace or as skills-directory plugin (`<name>@skills-dir`) [VERIFIED]
- `skillOverrides` in settings.json overrides visibility per skill: `on` / `name-only` / `user-invocable-only` / `off` [VERIFIED 2026-09-21]
- Bundled skills (`/doctor`, `/code-review`, `/batch`, `/debug`, `/loop`, `/claude-api`, `/verify`, `/workflow-authoring`) ship with Claude Code; `/skill-doctor` reports skill usage costs [VERIFIED 2026-09-21]
- Subagents (`.claude/agents/`) run in background by default (v2.1.198), can preload skills, unique to Claude Code [VERIFIED]
- Model Context Protocol (MCP) config in `.mcp.json` (project), `~/.claude.json` (user), `managedMcpServers` setting (enterprise, v2.1.259) [VERIFIED]
- Hooks in `settings.json` and in skill/agent frontmatter; similar events to Windsurf hooks [VERIFIED]
- PowerShell tool on Windows (default without Git Bash); `shell` frontmatter selects bash vs powershell [VERIFIED 2026-09-21]
- Cloud/remote: Cowork sessions, cloud environments, Remote Control, Dispatch, `claude --teleport`, routines, self-hosted runners (v2.1.224) [VERIFIED 2026-09-21]

## Table of Contents

1. [Overview](#1-overview)
2. [Installation](#2-installation)
3. [Directory Structure](#3-directory-structure)
4. [Settings and Configuration](#4-settings-and-configuration)
5. [AI Assistant Features](#5-ai-assistant-features)
6. [Memory and Instructions](#6-memory-and-instructions)
7. [Commands and Workflows](#7-commands-and-workflows)
8. [Skills](#8-skills)
9. [Subagents](#9-subagents)
10. [Hooks](#10-hooks)
11. [MCP Integration](#11-mcp-integration)
12. [Plugins](#12-plugins)
13. [Cloud, Remote, and Automation](#13-cloud-remote-and-automation)
14. [Terminal and CLI](#14-terminal-and-cli)
15. [Key Files Reference](#15-key-files-reference)
16. [Sources](#16-sources)
17. [Document History](#17-document-history)

## 1. Overview

Claude Code is Anthropic's agentic coding tool. It runs in the terminal (command-line interface, CLI; primary), in integrated development environments (IDEs) (VS Code, JetBrains), in a Desktop app, on mobile, in the browser, in Slack, and as a Chrome extension. It builds features from descriptions, debugs issues, navigates codebases, and automates tasks.

**Key characteristics:**
- Terminal-based core (not an IDE or chat window)
- Can read/write files, run commands, create commits and pull requests
- Supports Model Context Protocol (MCP) for external tool integration
- Enterprise-ready with API, AWS Bedrock, GCP Vertex, or Microsoft Foundry hosting options
- Current version 2.1.278 (2.1.277 shipped 2026-09-18) [VERIFIED 2026-09-21]

**Default models (v2.1.257+):** Claude Sonnet 5 (default since v2.1.197), Claude Opus 5 (default Opus since v2.1.219), Claude Fable 5.1 (default Fable since v2.1.257). All ship with 1M-token context windows. [VERIFIED 2026-09-21]

**Recent milestones:** [VERIFIED 2026-09-21]

- v2.1.278: auto mode defaults to server-side classifier, no classifier-overhead billing (also Bedrock, Vertex, Foundry, gateways)
- v2.1.277 (2026-09-18): AGENTS.md native support
- v2.1.261: `/skill-doctor` skill usage report
- v2.1.257 (2026-09-01): Fable 5.1 default; `/add-dir` loads nested skills
- v2.1.224: self-hosted runners (Team/Enterprise run sessions on own machines)
- v2.1.218: frontmatter booleans accept `yes/no/on/off/1/0`; `background: false` for forked skills
- v2.1.199: `skillOverrides` "off" hides from Remote Control/Agent SDK listings
- v2.1.198: subagents in background by default; Claude in Chrome reached general availability (GA)
- v2.1.197: Sonnet 5 default, 1M-token context
- v2.1.3 (Jan 2026): commands merged into skills

## 2. Installation

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

**Version check and updates:**
```bash
claude --version    # Print current version
claude update       # Update Claude Code
```

## 3. Directory Structure

```
~/.claude/                        # User config directory
├── CLAUDE.md                     # Global instructions (all projects)
├── settings.json                 # User settings
├── agents/                       # User subagents
│   └── my-agent.md
├── commands/                     # User slash commands (legacy format)
│   └── my-command.md
├── rules/                        # User-level rules
│   └── preferences.md
├── skills/                       # User skills (available in all projects)
│   ├── my-skill/
│   │   └── SKILL.md
│   └── synced/                   # RESERVED: skills synced from claude.ai
├── plugins/                      # Installed plugins
├── output-styles/                # Custom output styles
├── keybindings.json              # Custom keybindings
└── themes/                       # Custom themes

~/.claude.json                    # Preferences, OAuth, MCP servers, caches
~/.claude/projects/<project>/memory/  # Auto memory per project

your-project/
├── CLAUDE.md                     # Project instructions (checked in)
├── AGENTS.md                     # Read when no CLAUDE.md exists (v2.1.277)
├── CLAUDE.local.md               # Local instructions (gitignored)
├── .claude/
│   ├── CLAUDE.md                 # Alternative project instructions location
│   ├── settings.json             # Project settings (checked in)
│   ├── settings.local.json       # Local settings (gitignored)
│   ├── agents/                   # Project subagents
│   ├── commands/                 # Project slash commands (legacy format)
│   ├── skills/                   # Project skills
│   │   └── my-skill/
│   │       └── SKILL.md
│   ├── rules/                    # Project rules
│   │   ├── code-style.md
│   │   └── testing.md
│   ├── workflows/                # Dynamic workflows (*.js)
│   ├── output-styles/            # Output styles (*.md)
│   ├── agent-memory/             # Persistent subagent memory
│   └── plugins/                  # Project plugins
├── .mcp.json                     # Project MCP servers (checked in)
└── .worktreeinclude             # Worktree file inclusion
```

**Reserved name:** A skill folder named `synced` (any capitalization) is skipped in enterprise, personal, and project locations - Claude Code uses it for skills downloaded from claude.ai. [VERIFIED 2026-09-21]

**Managed Settings (IT/Admin deployed):**
- macOS: `/Library/Application Support/ClaudeCode/`
- Linux/WSL: `/etc/claude-code/`
- Windows: `C:\Program Files\ClaudeCode\`

## 4. Settings and Configuration

### 4.1 Configuration Scopes

Scopes listed from highest to lowest precedence:

1. **Managed** - Organization-wide, cannot be overridden (narrow exceptions documented in settings docs)
2. **Command line** - Temporary session overrides (`--permission-mode`, `--settings`)
3. **Local** - `.claude/settings.local.json` (personal, not committed)
4. **Project** - `.claude/settings.json` (team-shared)
5. **User** - `~/.claude/settings.json` (personal defaults)

Some environment variables override their equivalent setting; behavior varies per variable.

### 4.2 Settings File (settings.json)

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
  "model": "claude-sonnet-4-5-20250929",
  "skillOverrides": {
    "legacy-context": "name-only",
    "deploy": "off"
  }
}
```

**Key settings:**
- **permissions** - Allow/deny rules for tools (including `Skill(name)` rules for skills)
- **env** - Environment variables
- **hooks** - Lifecycle hooks configuration
- **model** - Default model to use
- **skillOverrides** - Per-skill visibility: `"on"` (default), `"name-only"` (name without description), `"user-invocable-only"` (hidden from Claude), `"off"` (hidden everywhere); written by the `/skills` menu to `.claude/settings.local.json`; plugin skills unaffected [VERIFIED 2026-09-21]
- **claudeMdExcludes** - Glob list of CLAUDE.md/rules files to exclude from loading [VERIFIED 2026-09-21]
- **disableBundledSkills** - Turn off bundled skills (`/doctor` stays typable; hide via `skillOverrides` or `DISABLE_DOCTOR_COMMAND`) [VERIFIED 2026-09-21]
- **disableSkillShellExecution** - Replace `` !`cmd` `` injections with a policy notice (managed-settings use case) [VERIFIED 2026-09-21]
- **managedMcpServers** - Enterprise-provided HTTP/SSE MCP servers (v2.1.259) [VERIFIED 2026-09-21]
- **availableModels** - Organization model allowlist (restricts `model` overrides) [VERIFIED 2026-09-21]
- **attribution** - Commit/PR attribution text
- **includeCoAuthoredBy** - Add co-authored-by to commits
- **respectGitignore** - Honor .gitignore for @ suggestions

### 4.3 Environment Variables

- `ANTHROPIC_API_KEY` - API key for authentication
- `CLAUDE_CODE_USE_BEDROCK` - Use Amazon Bedrock
- `CLAUDE_CODE_USE_VERTEX` - Use Google Vertex AI
- `CLAUDE_CONFIG_DIR` - Override `~/.claude` location
- `CLAUDE_CODE_USE_POWERSHELL_TOOL` - Force PowerShell tool on/off
- `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` - Turn off all background task features
- `BASH_DEFAULT_TIMEOUT_MS` - Default bash timeout
- `DISABLE_TELEMETRY` - Disable telemetry
- `DISABLE_AUTOUPDATER` - Disable auto-updates
- `HTTP_PROXY` / `HTTPS_PROXY` - Proxy configuration

## 5. AI Assistant Features

### 5.1 Capabilities

- **Read/Write files** - View and modify source code
- **Run terminal commands** - Execute shell commands with permission controls
- **Web search/fetch** - Retrieve information from the web
- **MCP integration** - Connect to external tools (GitHub, databases, APIs)
- **Extended thinking** - Deep reasoning for complex problems (`ultrathink` for one-off deep reasoning)
- **Background tasks** - Run operations and subagents in background (`/tasks` panel)
- **Checkpoints** - `/rewind` restores code and conversation to earlier points (background forked skills excluded)
- **Parallel agents** - Multiple Claude Code agents, agent view, Agent SDK

### 5.2 Input Modes

- **Normal** - Standard text input
- **Multiline** - Use `\` at end of line, or `Shift+Enter`
- **Vim mode** - Enable with `/vim` command
- **Bash mode** - Prefix with `!` to run shell commands directly
- **PowerShell mode** - PowerShell tool runs when enabled (default on Windows without Git Bash)

### 5.3 Prompt Syntax (Agentic Language Enrichments)

Claude Code supports several input enrichments for precise control:

**@mentions** - Reference context:
- `@file` or `@path/to/file` - Reference specific files
- `@folder/` - Reference entire directories
- Files in prompts via `@README` syntax in CLAUDE.md

**/commands** - Invoke automation:
- `/command-name` - Run command from `.claude/skills/` or legacy `.claude/commands/`
- Built-in: `/memory`, `/init`, `/clear`, `/compact`, `/resume`, etc.
- Skills support `$ARGUMENTS`, `$ARGUMENTS[N]`, `$N`, named arguments

**!bang** - Direct shell execution:
- `!command` - Execute shell command directly without AI interpretation

**# key** - Memory shortcut (not a hashtag system):
- Press `#` during conversation to save current instruction to `CLAUDE.md`
- Single-purpose key, not user-defined tags
- Example:
  ```
  You: "Always use pnpm instead of npm"
       [press # key]
  Claude: "I've added this to your project instructions in CLAUDE.md"
  ```

**Other enrichments:**
- **Pipe input** - `cat file.txt | claude -p "explain"` includes file content
- **Multiline** - Use `\` at end of line or `Shift+Enter`
- **Image attachments** - Supported via CLI flags

### 5.4 Keyboard Shortcuts

- `Ctrl+C` - Cancel current operation
- `Ctrl+D` - Exit Claude Code
- `Ctrl+L` - Clear screen
- `Ctrl+R` - Reverse search history
- `Esc` - Cancel current input / interrupt
- `/` - Open slash commands menu
- `@` - Reference files
- `!` - Execute bash command directly

### 5.5 Permission Modes

- **default** - Ask for permission on sensitive operations
- **acceptEdits** - Auto-accept file edits, ask for other operations
- **dontAsk** - Auto-accept most operations
- **auto** - Server-side classifier eliminates prompts (default for API/Enterprise users; since v2.1.278 also on Bedrock, Vertex, Foundry, and gateways; the server-side classifier does not charge classifier overhead) [VERIFIED 2026-09-21]
- **bypassPermissions** - Skip all permission checks (dangerous)
- **plan** - Read-only planning mode (classifier reviews commands before execution)

## 6. Memory and Instructions

### 6.1 CLAUDE.md Files

Claude automatically loads CLAUDE.md files at conversation start. Use for:
- Frequently used commands (build, test, lint)
- Code style preferences and naming conventions
- Architectural patterns
- Developer environment setup

**Locations (in priority order):**
1. Managed: `/Library/Application Support/ClaudeCode/CLAUDE.md` (system-wide; `claudeMd` key in managed-settings.json is an alternative delivery)
2. Project: `./CLAUDE.md` or `./.claude/CLAUDE.md`
3. User: `~/.claude/CLAUDE.md`
4. Local: `./CLAUDE.local.md` (gitignored)

**Loading mechanics:** [VERIFIED 2026-09-21]
- When working in a subdirectory (e.g. `foo/bar/`), Claude loads `foo/bar/CLAUDE.md`, then `foo/CLAUDE.md`, walking up to the root
- `--add-dir` with `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` also loads CLAUDE.md from additional directories
- `--setting-sources` controls which setting sources load (`user`, `project`, `local`)
- Managed CLAUDE.md deploys via configuration management systems

**Imports in CLAUDE.md:**
```markdown
See @README for project overview and @package.json for npm commands.

# Additional Instructions
- git workflow @docs/git-instructions.md
```

### 6.2 Modular Rules (.claude/rules/)

Organize instructions into focused files, loaded alongside project CLAUDE.md: [VERIFIED 2026-09-21]

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

- `paths` accepts globs (`src/**/*`, `*.md`, `src/components/*.tsx`, `{a,b}/{c,d}/*.{ts,tsx}`, `[abc]` character classes); escape literal `[` as `\[`
- A rule without `paths` loads always (project scope)
- User-level rules: `~/.claude/rules/`
- Share rules across projects via symlinks (`ln -s ~/shared-claude-rules .claude/rules/shared`)
- Exclude rules via `claudeMdExcludes` in settings (e.g. `"**/monorepo/CLAUDE.md"`)

**When to use rules vs skills:** A section of CLAUDE.md that has grown into a procedure rather than a fact is better as a skill; facts and standing conventions stay in CLAUDE.md/rules.

### 6.3 AGENTS.md (v2.1.277)

Claude Code reads AGENTS.md when no CLAUDE.md exists: [VERIFIED 2026-09-21]

- Fallback check covers `CLAUDE.md`, `.claude/CLAUDE.md`, `CLAUDE.local.md` in the working directory or above it
- `~/.claude/CLAUDE.md`, managed CLAUDE.md, and `.claude/rules/` keep loading alongside AGENTS.md
- `/config` Project instructions modes:
  - `claude-md-or-agents-md` (default) - CLAUDE.md, or AGENTS.md when none exists
  - `claude-md-and-agents-md` - both, CLAUDE.md first
  - `claude-md` - CLAUDE.md only
  - `managed-only` - managed CLAUDE.md and auto memory only
- Not available on Bedrock/Vertex/Foundry or sessions without feature-flag fetching (first session after upgrade, telemetry disabled, `disableAllHooks`); import AGENTS.md from a CLAUDE.md in those environments

### 6.4 Auto Memory

- Claude accumulates learnings automatically in `~/.claude/projects/<project>/memory/` [VERIFIED 2026-09-21]
- `/memory` views and edits all memory files
- Enable/disable per project under "Auto memory" in `/config`
- Project skills and repo-declared plugins carry over to cloud sessions; personal auto memory does not

### 6.5 Memory Commands

- `/memory` - Open memory editor
- `/init` - Generate initial CLAUDE.md for project (improved template with `CLAUDE_CODE_NEW_INIT=1`)
- `#` key - Add instruction to CLAUDE.md during conversation

## 7. Commands and Workflows

### 7.1 Built-in Slash Commands

- `/add-dir` - Add directory to context (loads nested skills, v2.1.257+)
- `/agents` - Manage subagents
- `/clear` - Clear conversation context
- `/compact [instructions]` - Compact context with optional focus
- `/config` - Open configuration (includes Project instructions: AGENTS.md mode)
- `/context` - Show current context
- `/cost` - Show session cost
- `/desktop` - Continue terminal session in Desktop app (requires claude.ai subscription)
- `/exit` - Exit Claude Code
- `/export [filename]` - Export conversation
- `/help` - Show available commands
- `/hooks` - Manage hooks
- `/init` - Initialize CLAUDE.md
- `/login` / `/logout` - Authentication
- `/mcp` - Manage MCP servers
- `/memory` - Edit memory files
- `/model` - Change model (includes effort level)
- `/permissions` - View/edit permissions
- `/plan` - Enter planning mode
- `/plugin` - Manage plugins (Installed tab, Stats tab)
- `/reload-skills` - Re-scan skill and command directories without restarting the session (v2.1.152+) [VERIFIED 2026-09-21]
- `/resume [session]` - Resume previous session
- `/rewind` - Rewind to checkpoint
- `/skills` - Skill visibility menu (Space cycles states, writes `skillOverrides`)
- `/tasks` - Background task panel
- `/vim` - Toggle Vim mode

### 7.2 Bundled Skills

Claude Code ships prompt-based bundled skills: `/doctor`, `/code-review` (alias `/review`), `/batch`, `/debug`, `/loop`, `/claude-api`, `/verify`, `/workflow-authoring` (dynamic workflows only). Most bundled skills auto-invoke when relevant; some (`/verify`) run only on explicit invocation. Turn off with `disableBundledSkills`. A same-named project skill replaces a bundled command but never its aliases. [VERIFIED 2026-09-21]

**Bundled `/verify` recipe recording:** when `/verify` has to build and drive an app without a recorded recipe, it writes what worked to `.claude/skills/verify/SKILL.md` at the repo root (or the touched directory in a monorepo) - any project skill at that path gets overwritten. Do not place a custom skill at `.claude/skills/verify/`. [VERIFIED 2026-09-21]

### 7.3 Custom Slash Commands

Store prompt templates in `.claude/skills/<name>/SKILL.md` (recommended) or legacy `.claude/commands/*.md` (project) / `~/.claude/commands/` (user). Both create `/name` and work identically; command files support the same frontmatter except `name` and `paths`. [VERIFIED 2026-09-21]

**Example:** `.claude/commands/fix-issue.md`
```markdown
---
allowed-tools: Bash(git:*), Read, Edit
description: Fix a GitHub issue
disable-model-invocation: true
---

Fix issue #$ARGUMENTS following our coding standards:
1. Understand the problem
2. Search for relevant files
3. Implement the fix
4. Write tests
5. Create a commit
```

**Invocation:** `/fix-issue 123`

**Command name derivation:** [VERIFIED 2026-09-21]
- Skill directory under `~/.claude/skills/` or `.claude/skills/` → directory name (`deploy-staging` → `/deploy-staging`)
- File under `.claude/commands/` → filename without extension (`deploy.md` → `/deploy`)
- File in a subdirectory of `.claude/commands/` → `/subdir:filename` (each `/` becomes `:`)
- Nested project skill that clashes with another name → `/relative-subdir:name` (e.g. `/apps/web:deploy`)
- Plugin skill → `/plugin-name:skill-name`

**Arguments:** [VERIFIED 2026-09-21]
- `$ARGUMENTS` - All arguments as string; if no placeholder receives arguments, `ARGUMENTS: <input>` is appended to the content
- `$ARGUMENTS[N]` or `$N` - Positional (an indexed placeholder with no argument stays literal)
- Named arguments - frontmatter `arguments` list; `$name` expands (empty string when missing)
- Stacking - `/a /b args` loads both, each receives `args`; first skill plus up to 5 more expand; stops at the first non-inline-user-invocable skill token

**Dynamic content:**
- `` !`command` `` - Execute shell command and include output (runs before Claude sees the content)
- `@file` - Reference files
- ```` ```! ```` fenced blocks - Multi-line command injection

## 8. Skills

Skills bundle complex multi-step tasks with supporting resources.

**Based on:** [Agent Skills open standard](https://agentskills.io). Claude Code extends the standard with invocation control, subagent execution, and dynamic context injection. [VERIFIED 2026-09-21]

### 8.1 Commands-Skills Merge (v2.1.3, January 2026)

As of v2.1.3, **commands have been merged into skills**. `.claude/commands/deploy.md` and `.claude/skills/deploy/SKILL.md` both create `/deploy` and work identically. Existing `.claude/commands/` files continue to work. [VERIFIED]

**Why Anthropic merged them (from [GitHub issue #13115](https://github.com/anthropics/claude-code/issues/13115) and official sources):**

1. **Implementation parity** - Both were markdown with YAML frontmatter, both injected prompts, both supported the same fields. Two codepaths for identical mechanics.
2. **Skills are a strict superset** - Skills add: directory for supporting files, subagent execution (`context: fork`), progressive disclosure, auto-invocation by model.
3. **Maintenance burden** - One system to maintain, one parser, one discovery path.

**What the merge preserved:**
- `disable-model-invocation: true` → command-like (user-only, never auto-invoked)
- Default (no flag) → skill-like (agent can auto-invoke when relevant)
- If a skill and command share the same name, the skill takes precedence.

**What was lost:**
- Browsability: no longer possible to scan "things I explicitly trigger" vs "knowledge the agent uses" by directory
- Semantic clarity: the distinction between "execute this procedure NOW" and "apply this knowledge when relevant" is collapsed into a frontmatter flag

### 8.2 Skill Locations and Precedence

- **Enterprise** - `[managed-settings-dir]/.claude/skills/<name>/SKILL.md` | Loads: all users on managed machines
- **Personal** - `~/.claude/skills/<name>/SKILL.md` | Loads: all your projects (not Cowork/cloud sessions)
- **Project** - `.claude/skills/<name>/SKILL.md` | Loads: sessions in this repository
- **Nested** - `<subdir>/.claude/skills/<name>/SKILL.md` | Loads: sessions in or below `<subdir>` (lazy)
- **Additional directory** - `.claude/skills/` in `--add-dir` directories | Loads: that session
- **Plugin** - `<plugin>/skills/<name>/SKILL.md` | Loads: wherever the plugin is enabled, as `/plugin-name:skill-name`
- **claude.ai account** - skills enabled for the account | Loads: Cowork, cloud sessions, terminal sessions signed in with that account

[VERIFIED 2026-09-21]

**Precedence when names clash:** [VERIFIED 2026-09-21]
- Enterprise over personal, personal over project
- A skill beats a same-named `.claude/commands/` file
- Project skill replaces a bundled skill's command, but not its aliases
- Plugin skills coexist (namespaced)
- Project-root and nested skills with the same name: both load
- claude.ai synced skill that matches another command: the other skill runs; synced skill stays as `/anthropic-skills:<name>`

**Known precedence bugs (open, 2026-09):** the documented rules above are not always honored - bundled `code-review` shadowed a same-named repo skill on some versions ([issue #71734](https://github.com/anthropics/claude-code/issues/71734)), the Skill tool executed a parent/global skill over the local one ([issue #20309](https://github.com/anthropics/claude-code/issues/20309), open since January), and a bundled/custom name collision corrupted skill loading entirely on v2.1.178/179 ([issue #69175](https://github.com/anthropics/claude-code/issues/69175)). Prefer unique skill names over relying on same-name overrides. [VERIFIED 2026-09-21]

**Monorepo loading:** Project skills load from the working directory up to the repository root. Skills in subdirectories below the working directory do not load at startup - they load on first file read/edit in that subdirectory and stay available. `/add-dir <path>` loads them sooner (v2.1.257+); `/cd` adds the new directory's project skills (v2.1.246+). [VERIFIED 2026-09-21]

**Symlinks:** A skill folder entry can be a symlink; Claude Code reads SKILL.md from the target and deduplicates. (Note: IPPS avoids symlinks on Windows.) [VERIFIED 2026-09-21]

### 8.3 SKILL.md Format

```yaml
---
name: deploy-to-production
description: Guides deployment with safety checks
disable-model-invocation: true    # Optional: makes it command-like (user-only)
context: fork                     # Optional: run as subagent
allowed-tools: Read, Bash(git:*)  # Optional: pre-approve tools
model: sonnet                     # Optional: override model
---

## Pre-deployment Checklist
1. Run all tests
2. Check for uncommitted changes
```

- Directory name = command name; `name` field only sets the display label (except in plugins, where it can set the command's last segment)
- Frontmatter is parsed only when the opening `---` is the file's first line; otherwise the whole file is content
- Booleans accept `yes/no/on/off/1/0` in any case (v2.1.218+)
- Keep SKILL.md under 500 lines; move reference material to supporting files in the skill directory
- `description` + `when_to_use` are truncated at 1,536 characters combined in the skill listing

**Full frontmatter reference:** [VERIFIED 2026-09-21]
- `name` - Display label in listings
- `description` - What + when; drives auto-invocation; first non-empty body line if omitted
- `when_to_use` - Additional trigger context, appended to description
- `argument-hint` - Autocomplete hint (e.g. `[issue-number]`)
- `arguments` - Named positional arguments for `$name` substitution
- `disable-model-invocation` - true = user-only (also blocks preloading into subagents and scheduled task firing, v2.1.196+)
- `user-invocable` - false = Claude-only
- `allowed-tools` - Tools pre-approved during the invoking turn (grant clears on next message)
- `disallowed-tools` - Tools removed while the skill is active (cannot remove `EndConversation`)
- `model` - Model override for the turn; `inherit` keeps session model; ignored if excluded by `availableModels`
- `effort` - Effort level: `low`/`medium`/`high`/`xhigh`/`max`
- `context: fork` - Run in a fresh subagent context
- `agent` - Subagent type for forked skills (`Explore`, `Plan`, `general-purpose`, custom)
- `background` - false = wait for fork result in-turn (default true, v2.1.218+)
- `hooks` - Hooks registered on invocation, kept for the session
- `paths` - Globs limiting auto-activation to matching files (skills only, not command files)
- `shell` - `bash` (default) or `powershell` for `` !`cmd` `` injections
- `metadata` - Free-form YAML map for own tooling
- `license`, `compatibility` - Agent Skills spec fields; accepted, not acted on

**Agent Skills spec subset** (claude.ai uploads, Skills API, `package_skill.py`): only `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools` are allowed; other fields fail packaging. Claude Code itself accepts all fields. [VERIFIED 2026-09-21]

**Unknown/custom frontmatter fields are silently stripped** before the content reaches the model - the skill keeps working, but the model never sees the field values ([issue #13005](https://github.com/anthropics/claude-code/issues/13005)). VS Code additionally flags attributes outside its allowlist; cosmetic only, recently downgraded from warnings to gray-out hints ([VS Code issue #294520](https://github.com/microsoft/vscode/issues/294520)). [VERIFIED 2026-09-21]

### 8.4 Invocation Control

Two frontmatter fields control who can invoke a skill:

- **Default (no field)** - User can invoke: yes | Claude can invoke: yes | Description in context: yes, always loaded
- **`disable-model-invocation: true`** - User can invoke: yes | Claude can invoke: no | Description in context: **no, removed from context**
- **`user-invocable: false`** - User can invoke: no | Claude can invoke: yes | Description in context: yes, always loaded

**`disable-model-invocation: true`** - User-only. The skill appears in the `/` autocomplete menu but its description is NOT loaded into Claude's context. Zero token cost. Claude cannot auto-trigger it. This is the exact equivalent of a workflow/explicit command. Use for: destructive skills (`/deploy`), expensive operations, timing-sensitive procedures. If Claude tries anyway, Claude Code blocks the call and instructs it to suggest running the command yourself. As of v2.1.196 it also prevents preloading into subagents and scheduled-task firing. [VERIFIED]

**`user-invocable: false`** - Claude-only. Hidden from `/` menu but Claude CAN still invoke it via the Skill tool. The description IS loaded into context. Use for: background knowledge that isn't actionable as a command (`/legacy-system-context`). **Caution:** This creates a "shadow tool" - the user doesn't see it in the menu but Claude can still execute it. [VERIFIED]

**Known issue ([bug #26251](https://github.com/anthropics/claude-code/issues/26251)):** In some versions, Claude refuses to execute `disable-model-invocation: true` skills via the Skill tool even when the user explicitly types `/name`. The model misinterprets the flag as "I cannot use the Skill tool for this skill at all." Status: reported, may be fixed in later versions. [VERIFIED]

Source: [Claude Code skills documentation](https://code.claude.com/docs/en/skills#control-who-invokes-a-skill) [VERIFIED]

### 8.5 Skill Content Lifecycle

[VERIFIED 2026-09-21]

- Invoked skill content enters the conversation as a single message and persists across later turns; the file is not re-read
- Re-invocation with identical rendered content: short "already loaded" note; with different content (new arguments or new dynamic output): full content appended again
- Auto-compaction re-attaches the most recent invocation of each skill: first 5,000 tokens per skill, combined 25,000-token budget, newest first - older skills can be dropped entirely after compaction
- `allowed-tools` grants clear when the next message is sent, even though content persists; re-invocation re-applies them
- Write guidance that should apply throughout a task as standing instructions, not one-time steps
- If a skill seems to stop influencing behavior, strengthen its `description`/instructions or use hooks to enforce deterministically

### 8.6 Dynamic Context Injection

[VERIFIED 2026-09-21]

- Inline `` !`command` `` (recognized when `!` starts a line or follows whitespace) and fenced ```` ```! ```` blocks run before the skill content is sent to Claude; output replaces the placeholder
- The harness (Claude Code client) executes the command, not the model: Claude never sees the command text, never decides, and cannot approve or deny it - it receives only the rendered output. Whether default permission mode prompts the user before an injected command runs is not documented [UNVERIFIED]
- Single pass: command output is not re-scanned for further placeholders
- Working directory follows the session shell (moves with `cd`); use `${CLAUDE_SKILL_DIR}` or `${CLAUDE_PROJECT_DIR}` for stable paths
- `shell: powershell` runs injections through the PowerShell tool (on by default on Windows without Git Bash)
- PowerShell version is auto-detected, not selectable: the tool prefers `pwsh.exe` (PowerShell 7+) found on PATH, falling back to `powershell.exe` (5.1); no user-configurable pin exists. Microsoft Store (MSIX) installs of PS7 can be missed by detection because `pwsh.exe` is a WindowsApps execution alias (issue #55041, open; winget/MSI installs resolved since v2.1.126). Check the active version with `$PSVersionTable.PSVersion` [VERIFIED 2026-09-21]
- `disableSkillShellExecution: true` replaces each command with `[shell command execution disabled by policy]`
- claude.ai-synced skills never run shell commands locally (v2.1.228+)
- `ultrathink` anywhere in skill content triggers deeper reasoning for that run

**Example** (bash default; each placeholder is replaced by command output before the content reaches Claude):

````markdown
---
description: Release helper with environment snapshot
---
Release candidate: !`git rev-parse --short HEAD` on !`git branch --show-current`

```!
git status --short
node --version
```
````

With `shell: powershell` in the frontmatter, the injections run through the PowerShell tool:

````markdown
---
description: Windows environment snapshot
shell: powershell
---
Snapshot taken: !`Get-Date -Format "yyyy-MM-dd HH:mm"`

```!
(Get-ChildItem -Recurse -File).Count
$PSVersionTable.PSVersion
```
````

### 8.7 Skill Permissions

[VERIFIED 2026-09-21]

- Permission rules: `Skill(name)` exact match, `Skill(name *)` prefix match; allow or deny
- Deny rule on an unqualified name also blocks nested and alias-listed skills (v2.1.260+)
- Denying the `Skill` tool entirely disables all skill auto-invocation
- `allowed-tools` in a project skill applies even in untrusted `-p` runs - review skills committed to a repository before running Claude Code there
- A few built-in commands are available through the Skill tool (`/init`, `/security-review`); most (`/compact`) are not

**Where rules are configured:** `permissions.allow` / `deny` / `ask` arrays in `settings.json` at four levels (deny wins across all): project `.claude/settings.json` (committed), personal `.claude/settings.local.json` (gitignored), user `~/.claude/settings.json`, and managed settings in an OS-protected path outside the project (highest precedence). Skill visibility (`skillOverrides`) lives in the same files. [VERIFIED 2026-09-21]

**Self-modification (can the agent edit its own config?):** settings are plain files, so this is a real attack surface. Bounds: [VERIFIED mechanics 2026-09-21]

- Default permission mode prompts before file edits - silent self-modification requires pre-existing over-broad rules or `acceptEdits`
- `allowed-tools` grants expire after the invoking turn - a skill cannot permanently widen its own permissions via frontmatter
- `deny` rules win over `allow` at every level, and removing a deny requires editing the file the deny protects (self-protecting for the Edit/Write tools)
- Gap: a `deny Edit(...)` rule does NOT stop shell writes (`Set-Content` via Bash/PowerShell bypasses file-tool rules) - shell permission rules are command-prefix based, not file-path based. Default and `acceptEdits` modes still prompt before running the shell command (the command text is visible), so an unattended jailbreak requires `dontAsk`/`auto`/`bypassPermissions` mode or a broad shell allow rule
- Hard guarantees: `PreToolUse` hooks blocking settings-path edits (fail-open: a broken or unparseable hook lets the action proceed - see section 10.4), and managed settings the project cannot reach
- Consequence: skills act with the invoker's permissions during their turn - review skills committed to a repository before running Claude Code there

### 8.8 Progressive Disclosure (Context Cost)

In a regular session, skill descriptions are loaded into context so Claude knows what's available, but **full skill content only loads when invoked**. This means:

- Skills with `disable-model-invocation: true` = **zero tokens** in context
- Auto-invocable skills = ~100 tokens each (name+description only, truncated at 1,536 chars)
- Full SKILL.md body = loaded **only** when `/skill-name` is typed or Claude auto-invokes
- Supporting files (reference docs, scripts) = loaded only when referenced, on demand

Exception: Subagents with preloaded skills load full skill content at startup (via `skills:` field in agent frontmatter). [VERIFIED]

**`/skill-doctor`** (v2.1.261+) reports per-skill context cost and invocation counts; flags never-invoked skills and where to turn them off. Interactive sessions open the report in the `/plugin` manager's Stats tab; `-p` mode prints it as text. [VERIFIED 2026-09-21]

**Listing budget tuning:** [VERIFIED 2026-09-21]
- `skillListingBudgetFraction` - Context-window fraction reserved for the skill listing (default `0.01` = 1%; the docs' `0.02` is a raise example)
- `skillListingMaxDescChars` - Per-description character cap in the listing (default `1,536`)
- `SLASH_COMMAND_TOOL_CHAR_BUDGET` - Character budget for the skill listing
- `claude plugin validate .claude/skills` - Validates SKILL.md files in a skills directory

**Budget baseline caveat:** the fraction appears computed against a fixed ~200K-token reference even on 1M-context models, so the effective budget stays ~8,000 chars there ([issue #57941](https://github.com/anthropics/claude-code/issues/57941), open). Raise the fraction explicitly on extended-context models if descriptions get dropped. [VERIFIED as reported issue 2026-09-21]

### 8.9 Skill-Selection Degradation at Scale

Skill-selection accuracy degrades as auto-invocable skill libraries grow. The 2026 study [More Skills, Worse Agents?](https://arxiv.org/abs/2605.24050) measured on SkillsBench a monotonic pass-rate drop: 8 points at 52 skills, 14 at 102, 21 at 202. Skill shadowing (a wrong, similar-description skill winning the match) causes up to 68% of the degradation and is the only statistically significant effect; context overhead is indistinguishable from noise. Community reports place the practical ceiling near 30-40 skills: Claude Code historically truncated the skill listing around 30 entries ([issue #13343](https://github.com/anthropics/claude-code/issues/13343)), and skills overlapping Claude's trained behaviors (e.g., git) trigger less reliably than novel-domain skills ([issue #30387](https://github.com/anthropics/claude-code/issues/30387)). [VERIFIED 2026-09-21]

This ceiling applies ONLY to skills Claude can auto-invoke (those without `disable-model-invocation: true`). User-only skills bypass the limit entirely since Claude never needs to select them.

### 8.10 Skills vs Slash Commands (Historical, Pre-Merge)

Before v2.1.3, these were separate concepts:
- **Skills** - Complex tasks with supporting files, auto-invoked based on description
- **Slash commands** - Simple prompt templates, explicitly invoked with `/command`

After v2.1.3, this distinction is preserved only via `disable-model-invocation` frontmatter flag.

## 9. Subagents

Subagents are specialized AI assistants that run in isolated contexts.

### 9.1 Built-in Subagents

- **Explore** - Fast file discovery (read-only, skips CLAUDE.md and git status to keep context small)
- **Plan** - Codebase research for planning (read-only, skips CLAUDE.md and git status)
- **General-purpose** - Complex research and modifications (inherited model, all tools)

**Background execution:** Since v2.1.198, subagents run in the background by default - you keep working while they run, results arrive on completion. Background subagents use a narrower tool set; set `background: false` where the full tool set matters. [VERIFIED 2026-09-21]

### 9.2 Subagent Configuration

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
- `skills` - Skills to preload (full content injected at startup)
- `hooks` - Lifecycle hooks
- `omitClaudeMd` - Run without user, project, and local CLAUDE.md files (v2.1.271+) [VERIFIED 2026-09-21]

**Forking:** A subagent can fork the current conversation (receives full history) - distinct from a skill's `context: fork`, which starts with no history. [VERIFIED 2026-09-21]

### 9.3 Subagent Commands

- `/agents` - View, create, edit, delete subagents
- CLI: `claude --agents '{...}'` - Define inline subagents

## 10. Hooks

Hooks execute custom code at key points in Claude's workflow.

### 10.1 Hook Events

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

### 10.2 Hook Configuration

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

**Hooks in skills and agents:** Both SKILL.md and agent frontmatter accept a `hooks` field. Hooks registered by a skill run from invocation to session end (with a `once` option for one-time registration). Use hooks to enforce skill behavior deterministically instead of relying on prompt adherence. [VERIFIED 2026-09-21]

### 10.3 Hook Output

- **Exit code 0** - Success, continue
- **Exit code 2** - Block the action
- **JSON output** - Advanced control (modify inputs, add messages)

### 10.4 PreToolUse Workings

[VERIFIED 2026-09-21 - hooks reference]

**Matcher:** the config key under `PreToolUse` is a tool-name pattern - `Bash`, `Edit`, `Write`, `Read`, `Glob`, `Grep`, `Agent`, `WebFetch`, `WebSearch`, MCP tool names, or `Bash|PowerShell` to cover both shell tools; omitted matcher = all tools.

**Input:** JSON on stdin - common fields (`session_id`, `prompt_id`, `transcript_path`, `cwd`, `scratchpad_dir`, `permission_mode`, `hook_event_name`) plus `tool_name`, `tool_input` (full tool parameters: Bash/PowerShell = `command`, `description`, `timeout`, `run_in_background`; Edit/Write/Read = `file_path` + payload), and `tool_use_id`. MCP tool calls add `mcp_server` and the tool name.

**Decisions:**

- Exit 0 - proceed; stderr is shown to Claude (non-blocking)
- Exit 2 - block the tool call; stderr is shown to Claude
- JSON stdout - `permissionDecision`: `allow` (skips the permission flow entirely) / `deny` / `ask` / `defer`, with `permissionDecisionReason`; `updatedInput` rewrites the tool call; `additionalContext` injects context for Claude. When the JSON passes schema validation, the exit code is ignored - the JSON alone decides

**Fail-open:** a hook whose output fails JSON parsing or schema validation, or whose script is missing, is a NON-BLOCKING error - the tool call proceeds. A blocking guarantee requires a working hook script.

**Windows specifics:**

- `tool_input` paths arrive with backslash separators even when the hook runs under Git Bash - normalize before comparing (`file_path.replace("\\", "/")`, or `FILE_PATH="${FILE_PATH//\\//}"` in Bash), or the comparison never matches and the block never fires
- `~` and relative paths are expanded before hooks run - no bypass via path spelling
- Where the PowerShell tool is enabled it is the primary shell, and without Git Bash the Bash tool is not registered at all - a hook matching only `Bash` never fires there; match `Bash|PowerShell` to cover both

## 11. MCP Integration

Model Context Protocol (MCP) enables Claude to access custom tools and services.

### 11.1 MCP Scopes

- **Local** - `~/.claude.json` (personal, one project)
- **User** - `~/.claude.json` mcpServers field (personal, all projects)
- **Project** - `.mcp.json` (team-shared)
- **Managed** - `managedMcpServers` setting (IT-deployed HTTP/SSE servers, v2.1.259; command entries are skipped) [VERIFIED 2026-09-21]

### 11.2 Adding MCP Servers

```bash
# HTTP server
claude mcp add --transport http stripe https://mcp.stripe.com

# Project-scoped
claude mcp add --transport http github --scope project https://mcp.github.com

# User-scoped
claude mcp add --transport http slack --scope user https://mcp.slack.com
```

### 11.3 .mcp.json Format

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

### 11.4 MCP Commands

- `/mcp` - Manage MCP servers
- `claude mcp add` - Add server
- `claude mcp remove` - Remove server
- `claude mcp reset-project-choices` - Reset project MCP choices

## 12. Plugins

Plugins bundle skills, agents, hooks, MCP servers, Language Server Protocol (LSP) configs, and settings into a single installable package with namespace isolation. [VERIFIED]

### 12.1 Plugin Structure

```
my-plugin/
  .claude-plugin/
    plugin.json             # Manifest (ONLY file inside .claude-plugin/)
  skills/                   # Skills (folder per skill, each with SKILL.md)
    code-review/
      SKILL.md
  agents/                   # Custom subagents (.md files)
    reviewer.md
  commands/                 # Legacy slash commands (flat .md files)
  hooks/
    hooks.json              # Lifecycle hooks (same schema as settings.json hooks)
  .mcp.json                 # MCP server config
  .lsp.json                 # LSP server config (symbol-level search)
  monitors/
    monitors.json           # Background monitors
  bin/                      # Binaries added to PATH
  settings.json             # Default settings applied when plugin is enabled
```

**Critical:** Only `plugin.json` goes inside `.claude-plugin/`. All other directories at plugin root. Placing `skills/` or `hooks/` inside `.claude-plugin/` causes silent discovery failure. [VERIFIED]

### 12.2 Skills-Directory Plugins

A skill folder with an added `.claude-plugin/plugin.json` loads as a plugin named `<name>@skills-dir`, able to bundle agents, hooks, and MCP servers. In a project's `.claude/skills/`, this requires accepting the workspace trust dialog first. Scaffold with `claude plugin init`; test with `claude --plugin-dir <path>`. [VERIFIED 2026-09-21]

### 12.3 Manifest (`plugin.json`)

```json
{
  "name": "quality-review",
  "version": "1.0.0",
  "description": "Code quality automation tools",
  "author": { "name": "Team Name" },
  "homepage": "https://github.com/team/quality-review",
  "repository": "https://github.com/team/quality-review"
}
```

The `name` field becomes the namespace prefix. A `code-review` skill inside plugin `quality-review` is invoked as `/quality-review:code-review`. In plugin skills, frontmatter `name` can override the command's last segment. [VERIFIED]

### 12.4 Namespace Rules

- Plugin skills are always namespaced: `/plugin-name:skill-name`
- Standalone skills (in `.claude/skills/`) use short form: `/skill-name`
- Namespacing prevents collisions when multiple plugins ship skills with the same name (e.g., three plugins each with `/deploy`)
- Cross-references in CLAUDE.md and subagent definitions must use the namespaced form
- Plugin skills are not affected by `skillOverrides`; manage them through `/plugin` [VERIFIED 2026-09-21]

### 12.5 Installation and Management

```bash
# Install from GitHub
claude plugins install owner/repo

# Install from local folder (for authoring/testing)
claude plugins install ./my-plugin

# Scaffold a new plugin
claude plugin init my-plugin

# List installed plugins
claude plugins list

# Update a specific plugin (or all)
claude plugins update quality-review
claude plugins update

# Remove a plugin
claude plugins remove quality-review

# Reload after edits (during development)
/reload-plugins
```

[VERIFIED]

**Repo-declared plugins:** Plugins declared in the repository's `.claude/settings.json` install at session start - this carries over to cloud sessions. Plugins enabled only in user settings do not transfer. [VERIFIED 2026-09-21]

### 12.6 Testing During Development

Use `claude --plugin-dir ./my-plugin` or `claude plugins install ./my-plugin` for local testing. After every edit, run `/reload-plugins` to pick up changes. Verify skills appear under the plugin namespace (`/my-plugin:skill-name`), agents show in `/agents`, and hooks fire as expected. [VERIFIED]

### 12.7 Marketplace

Enterprise admins can run an in-org marketplace via `marketplace.json`. A `relevance` block in marketplace entries enables Claude Code to suggest installing a plugin when it fits the user's work context (v2.1.152+). [VERIFIED]

```bash
# Install from marketplace
claude plugins install quality-review@my-marketplace
```

The `@my-marketplace` suffix disambiguates when multiple marketplaces ship a plugin with the same name. [VERIFIED]

### 12.8 Plugin Locations

- User: `~/.claude/plugins/`
- Project: `.claude/plugins/`
- Installed from remote: cached in user plugin directory [VERIFIED]

### 12.9 When to Use Plugins vs Standalone Skills

- **Standalone (`.claude/skills/`)** - Personal workflows, project-specific, quick experiments
- **Plugin (`.claude-plugin/`)** - Team sharing, community distribution, version management, reuse across projects [VERIFIED]

## 13. Cloud, Remote, and Automation

[VERIFIED 2026-09-21]

### 13.1 Cowork and Cloud Sessions

- Cowork sessions and cloud environments do not read `~/.claude/skills/` or personal rules from the local machine
- Both load the skills enabled for your claude.ai account, synced at session start (manage via Desktop app sidebar or claude.ai skills settings)
- Cloud sessions additionally load project skills committed to the cloned repository's `.claude/skills/` and repo-declared plugins
- A personal skill that exists only locally is reported "not found" when a routine invokes it (each routine run starts as a fresh cloud session)

### 13.2 Remote Access

- **Remote Control** - Continue a session from phone or browser
- **Dispatch** - Message a task from the phone; opens a Desktop session
- **`claude --teleport`** - Pull a web/mobile-started task into the terminal (requires claude.ai subscription)
- **`/desktop`** - Continue the current terminal session in the Desktop app (requires claude.ai subscription; macOS and x64 Windows)
- **Slack** - `@Claude` in Slack with a bug report returns a pull request

### 13.3 Scheduled and Recurring Work

- **Routines** - Cloud scheduled tasks; keep running when the computer is off; trigger on API calls or GitHub events; created from web, Desktop app, or `/schedule` in the CLI
- **Desktop scheduled tasks** - Run locally on your machine with direct file access; DO load `~/.claude/skills/`
- **`/loop`** - Repeats a prompt within a CLI session for quick polling
- Scheduled tasks firing a `disable-model-invocation: true` skill do not run it (v2.1.196+)

### 13.4 Self-Hosted Runners

Team and Enterprise plans can run Claude Code sessions on their own machines instead of Anthropic's hosted infrastructure (v2.1.224).

### 13.5 CI/CD

GitHub Actions and GitLab continuous integration/continuous delivery (CI/CD) integrations run Claude Code in pipelines (commit messages, PR review, translations).

## 14. Terminal and CLI

### 14.1 CLI Commands

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

# Background session
claude --bg

# Update Claude Code
claude update
```

### 14.2 CLI Flags

- `-p, --print` - Print mode (non-interactive)
- `-c, --continue` - Continue last session
- `-r, --resume <session>` - Resume named session
- `--model <model>` - Use specific model (`sonnet`, `opus`)
- `--agent <name>` - Use specific subagent
- `--dangerously-skip-permissions` - Skip all permission checks
- `--add-dir <paths>` - Add directories to context (also loads their skills)
- `--plugin-dir <path>` - Load a plugin for testing
- `--setting-sources` - Control which setting sources load (`user`, `project`, `local`)
- `--mcp-config <file>` - Use specific MCP config
- `--output-format <format>` - Output format (`text`, `json`, `stream-json`)
- `--teleport` - Pull a cloud-started task into the terminal

### 14.3 Print Mode Features

Print mode (`-p`) enables scripting and automation:
```bash
# Analyze logs
tail -f app.log | claude -p "Alert if errors appear"

# CI integration
claude -p "Translate new strings to French and create PR"

# Structured output
claude -p --output-format json "List all TODO comments"
```

**Windows note:** The PowerShell tool runs shell commands when enabled (on by default on Windows without Git Bash, on with Git Bash for claude.ai/Console accounts; needs `CLAUDE_CODE_USE_POWERSHELL_TOOL=1` on Bedrock/Vertex/Foundry and macOS/Linux/WSL). Skills can force it with `shell: powershell`. [VERIFIED 2026-09-21]

## 15. Key Files Reference

**User Config (`~/.claude/`):**
- `~/.claude/CLAUDE.md` - Global instructions
- `~/.claude/rules/` - User rules
- `~/.claude/settings.json` - User settings (includes `skillOverrides`)
- `~/.claude/agents/` - User subagents
- `~/.claude/commands/` - User slash commands (legacy)
- `~/.claude/skills/` - User skills (`synced/` reserved for claude.ai downloads)
- `~/.claude/plugins/` - User plugins
- `~/.claude/output-styles/` - Custom output styles
- `~/.claude/keybindings.json` - Custom keybindings
- `~/.claude/themes/` - Custom themes
- `~/.claude.json` - Preferences, OAuth, MCP servers
- `~/.claude/projects/<project>/memory/` - Auto memory

**Project Config:**
- `CLAUDE.md` - Project instructions (checked in)
- `AGENTS.md` - Fallback instructions when no CLAUDE.md (v2.1.277)
- `CLAUDE.local.md` - Local instructions (gitignored)
- `.claude/settings.json` - Project settings (checked in, includes `skillOverrides`)
- `.claude/settings.local.json` - Local settings (gitignored)
- `.claude/agents/` - Project subagents
- `.claude/commands/` - Project slash commands (legacy)
- `.claude/skills/` - Project skills
- `.claude/rules/` - Project rules with optional `paths` frontmatter
- `.claude/workflows/` - Dynamic workflows (`*.js`)
- `.claude/output-styles/` - Output styles (`*.md`)
- `.claude/agent-memory/` - Persistent subagent memory
- `.claude/plugins/` - Project plugins
- `.mcp.json` - Project MCP servers
- `.worktreeinclude` - Worktree file inclusion
- `.claude-plugin/plugin.json` - Plugin manifest (if project IS a plugin)

**Managed (IT-deployed):**
- `managed-settings.json` - Enforced settings
- `managedMcpServers` setting - Enforced MCP servers (v2.1.259)
- `CLAUDE.md` - Organization-wide instructions

## 16. Sources

**Official Documentation:** [VERIFIED 2026-09-21]
- `CLCD-IN01-SC-CCDOCS-SKILLS`: https://code.claude.com/docs/en/skills - Skills and commands merged; discovery, frontmatter, invocation, lifecycle, permissions
- `CLCD-IN01-SC-CCDOCS-MEMORY`: https://code.claude.com/docs/en/memory - CLAUDE.md hierarchy, `.claude/rules/`, AGENTS.md, auto memory
- `CLCD-IN01-SC-CCDOCS-CLAUDEDIR`: https://code.claude.com/docs/en/claude-directory - `.claude` directory file reference
- `CLCD-IN01-SC-CCDOCS-OVERVIEW`: https://code.claude.com/docs/en/overview - Feature overview, platforms
- `CLCD-IN01-SC-CCDOCS-PLUGINS`: https://code.claude.com/docs/en/plugins - Plugin structure and distribution
- `CLCD-IN01-SC-CCDOCS-CHNGLG`: https://code.claude.com/docs/en/changelog - Release notes
- `CLCD-IN01-SC-GITHUB-CHNGLG`: https://github.com/anthropics/claude-code/blob/HEAD/CHANGELOG.md - Version history
- `CLCD-IN01-SC-GITHUB-CMDDEV`: https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/command-development/SKILL.md - Official command-development skill

**Official Documentation (previous verifications):** [VERIFIED 2026-01-15, 2026-08-04]
- `CLCD-IN01-SC-CCDOCS-OVRW2`: https://code.claude.com/docs/en/overview - Overview and quickstart
- `CLCD-IN01-SC-CCDOCS-SETTNG`: https://code.claude.com/docs/en/settings - Settings and configuration
- `CLCD-IN01-SC-CCDOCS-SUBAGT`: https://code.claude.com/docs/en/sub-agents - Subagents
- `CLCD-IN01-SC-CCDOCS-HOOKSR`: https://code.claude.com/docs/en/hooks - Hooks reference
- `CLCD-IN01-SC-CCDOCS-MCPDOC`: https://code.claude.com/docs/en/mcp - MCP integration
- `CLCD-IN01-SC-CCDOCS-CLIRF`: https://code.claude.com/docs/en/cli-reference - CLI reference
- `CLCD-IN01-SC-CCDOCS-TLSREF`: https://code.claude.com/docs/en/tools-reference - PowerShell tool version auto-detection (pwsh.exe preferred, powershell.exe fallback)
- `CLCD-IN01-SC-CCDOCS-INTMOD`: https://code.claude.com/docs/en/interactive-mode - Interactive mode

**Best Practices:**
- `CLCD-IN01-SC-ANTHR-BSTPRC`: https://www.anthropic.com/engineering/claude-code-best-practices - Claude Code usage best practices

**Community Sources:** [VERIFIED 2026-08-04, 2026-09-21]
- `CLCD-IN01-SC-GITHUB-13115`: https://github.com/anthropics/claude-code/issues/13115 - Commands-skills merge rationale
- `CLCD-IN01-SC-GITHUB-26251`: https://github.com/anthropics/claude-code/issues/26251 - Bug: disable-model-invocation blocks user invocation via Skill tool
- `CLCD-IN01-SC-GITHUB-19141`: https://github.com/anthropics/claude-code/issues/19141 - Clarification: user-invocable vs disable-model-invocation distinction
- `CLCD-IN01-SC-GITHUB-13005`: https://github.com/anthropics/claude-code/issues/13005 - Custom frontmatter fields stripped before model context; skills do not break
- `CLCD-IN01-SC-GITHUB-71734`: https://github.com/anthropics/claude-code/issues/71734 - Bundled code-review shadows repo skill (open)
- `CLCD-IN01-SC-GITHUB-20309`: https://github.com/anthropics/claude-code/issues/20309 - Skill tool executes parent/global over local same-name skill (open since January)
- `CLCD-IN01-SC-GITHUB-69175`: https://github.com/anthropics/claude-code/issues/69175 - Bundled/custom name collision corrupted skill loading (v2.1.178/179)
- `CLCD-IN01-SC-GITHUB-57941`: https://github.com/anthropics/claude-code/issues/57941 - Listing budget computed against fixed ~200K baseline on 1M-context models (open)
- `CLCD-IN01-SC-VSCODE-294520`: https://github.com/microsoft/vscode/issues/294520 - VS Code warns on unknown SKILL.md frontmatter attributes (cosmetic, downgraded to hints)
- `CLCD-IN01-SC-GITHUB-55041`: https://github.com/anthropics/claude-code/issues/55041 - PowerShell tool launches 5.1 instead of pwsh.exe 7 on MSIX/Store installs (open); interpreter not user-configurable
- `CLCD-IN01-SC-GITHUB-83928`: https://github.com/anthropics/claude-code/issues/83928 - PowerShell tool targets 5.1 on stock Windows; pwsh preferred once installed (reporter confirms 7.6.4 after winget install)
- `CLCD-IN01-SC-DEVTO-DIGEST`: https://dev.to/aicoding-guide/this-week-in-claude-code-codex-and-gemini-cli-week-of-september-20-2026-2fg1 - v2.1.270-2.1.277 digest, AGENTS.md modes
- `CLCD-IN01-SC-CRYPT-AGENTSMD`: https://cryptobriefing.com/anthropic-claude-code-agents-md-support/ - AGENTS.md support news (2026-09-18)
- `CLCD-IN01-SC-AGSKL-STD`: https://agentskills.io - Agent Skills open standard
- `CLCD-IN01-SC-PLATF-SKLBP`: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview.md - Progressive disclosure mechanics
- `CLCD-IN01-SC-DEVDT-DMINV`: https://www.developersdigest.tech/guides/disable-model-invocation - disable-model-invocation usage guide
- `CLCD-IN01-SC-CLDFS-PLGDST`: https://claudefa.st/blog/tools/mcp-extensions/plugins-distribution - Plugin distribution patterns, marketplace setup
- `CLCD-IN01-SC-ARXIV-SKLSDW`: https://arxiv.org/abs/2605.24050 - Skill shadowing study: monotonic pass-rate drop up to 21 points at 202 skills; shadowing = 68% of degradation, context overhead insignificant
- `CLCD-IN01-SC-GITHUB-13343`: https://github.com/anthropics/claude-code/issues/13343 - 30-skill listing truncation made remaining skills undiscoverable (v2.0.60 era, later removed)
- `CLCD-IN01-SC-GITHUB-30387`: https://github.com/anthropics/claude-code/issues/30387 - Skills overlapping Claude's trained behaviors trigger ~50% less reliably than novel-domain skills

## 17. Document History

**[2026-09-21 12:05]**
- Added: Section 10.4 PreToolUse Workings (matcher patterns, stdin input schema, decision control via exit codes and permissionDecision JSON, fail-open behavior, Windows path and shell-matcher pitfalls); section 8.7 hard-guarantees line now references the fail-open caveat

**[2026-09-21 11:55]**
- Added: Permission rule config locations (4 settings levels, deny-wins) and self-modification analysis to section 8.7 (Edit-vs-shell write gap with permission-mode nuance, hooks and managed settings as hard guarantees)

**[2026-09-21 11:50]**
- Added: PowerShell version auto-detection details to section 8.6 (pwsh.exe preferred over powershell.exe, no user pin, MSIX detection bug #55041); 3 sources

**[2026-09-21 11:45]**
- Added: Dynamic context injection examples to section 8.6 (inline placeholders, fenced block, bash and powershell variants)

**[2026-09-21 11:35]**
- Fixed: `skillListingBudgetFraction` default 0.02 → 0.01 (0.02 is the documented raise example); added fixed ~200K baseline caveat (issue #57941)
- Added: Bundled `/verify` recipe recording overwrites `.claude/skills/verify/SKILL.md` (section 7.2)
- Added: Known precedence bugs - issues #71734, #20309, #69175 (section 8.2)
- Added: Unknown frontmatter fields silently stripped (issue #13005); VS Code cosmetic warnings (VS Code issue #294520) (section 8.3)
- Added: 6 community sources; synced from CLAUDEIPPS-IN02 research

**[2026-09-21 11:16]**
- Changed: Section 8.9 rewritten from unsourced "~32-36" claim to evidenced skill-selection degradation (arXiv 2605.24050: -8/-14/-21 pass points at 52/102/202 skills, shadowing 68%; GitHub issues #13343, #30387); heading renamed from "Detection Ceiling" to "Skill-Selection Degradation at Scale"
- Added: 3 sources to Community Sources section; Summary bullet for selection degradation

**[2026-09-21 11:14]**
- Fixed: Broken inline-code fencing for the fenced-bang notation (sections 7.3 and 8.6) - delimiters now use more backticks than the enclosed content
- Added: `/reload-skills` (v2.1.152+) to built-in commands; listing budget tuning block to section 8.8 (skillListingBudgetFraction 0.02, skillListingMaxDescChars 1,536, SLASH_COMMAND_TOOL_CHAR_BUDGET, claude plugin validate) - supports IPPS workflow-to-skill migration
- Added: Summary bullet for listing budget and validation tooling

**[2026-09-21 11:13]**
- Changed: Current version updated 2.1.277 → 2.1.278; auto mode scope extended (Bedrock, Vertex, Foundry, gateways per v2.1.278)
- Fixed: `/skill-doctor` version attribution 2.1.252 → 2.1.261 (changelog 2.1.252 has no such entry; release notes and community sources date it 2026-09-04)
- Fixed: `omitClaudeMd` version attribution 2.1.270 → 2.1.271
- Changed: Fact-check pass - version attributions verified against official changelog and release pages; confirmed Fable 5.1 default (v2.1.257), `/add-dir` nested skills (v2.1.257), `/cd` project skills (v2.1.246), frontmatter booleans (v2.1.218), scheduled-task block (v2.1.196), compaction budgets 5,000/25,000, 1,536-char description cap

**[2026-09-21 11:07]**
- Fixed: Future-dated history timestamps corrected (11:30 → 10:30, 11:55 → 10:52; last write verified via file LastWriteTime 2026-09-21 10:52:41 - previous timestamps were future-dated, actual edit times were earlier)
- Fixed: MCP expanded at first use in Summary (AP-PR-06)
- Fixed: Summary bundled skills list completed to match section 7.2 (`/verify`, `/workflow-authoring` added)
- Fixed: Inline bare URLs converted to markdown links (Agent Skills standard, skills docs, GitHub issues #13115 and #26251)
- Added: CLCD topic registered in ID-REGISTRY.md

**[2026-09-21 10:52]**
- Changed: All section headings numbered and subsections decimal-numbered per INFO rules; TOC anchors updated
- Changed: Skill Locations and Invocation Control tables converted to lists per core conventions
- Fixed: Timeline format; acronyms expanded at first use (CLI, IDE, LSP, GA, CI/CD)
- Added: Source IDs to Sources section

**[2026-09-21 10:30]**
- Added: AGENTS.md section (v2.1.277 fallback, /config modes, availability limits)
- Added: Auto Memory section
- Added: Skill Locations and Precedence table (enterprise/personal/project/nested/add-dir/plugin/claude.ai)
- Added: Command name derivation rules (subdirectory `:` syntax, nested clash form)
- Added: Skill Content Lifecycle (persistence, re-invoke dedup, compaction 5k/25k budgets)
- Added: Dynamic Context Injection section (!`cmd`, shell frontmatter, PowerShell tool, disableSkillShellExecution)
- Added: Skill Permissions section (Skill(name) rules, allow/deny)
- Added: Bundled Skills section; /skill-doctor; /skills menu
- Added: Full frontmatter reference (20 fields incl. when_to_use, arguments, effort, background, hooks, paths, shell, metadata)
- Added: Cloud, Remote, and Automation section (Cowork, cloud sessions, Remote Control, Dispatch, teleport, routines, scheduled tasks, /loop, self-hosted runners, CI/CD)
- Added: Skills-directory plugins, repo-declared plugins, claude plugin init, --plugin-dir
- Added: Monorepo/subdirectory skill loading, reserved `synced` folder name, symlink handling
- Changed: Version updated to 2.1.277; models updated (Sonnet 5 / Opus 5 / Fable 5.1, 1M context)
- Changed: skillOverrides updated to string-state format (on/name-only/user-invocable-only/off)
- Changed: Directory structure expanded (workflows/, output-styles/, agent-memory/, keybindings.json, themes/, synced/, .worktreeinclude)
- Changed: Settings expanded (claudeMdExcludes, disableBundledSkills, disableSkillShellExecution, managedMcpServers, availableModels)
- Changed: Subagents updated (background default v2.1.198, skills preloading, omitClaudeMd, conversation fork)
- Changed: Hooks updated (hooks in skill/agent frontmatter, once option)
- Changed: Key Files Reference and CLI flags updated; Windows PowerShell notes added
- Changed: Sources updated with 2026-09-21 verification (old slash-commands URL removed - merged into skills page)

**[2026-08-04 17:50]**
- Added: Invocation Control subsection with full behavior table (disable-model-invocation removes from context, user-invocable creates shadow tool)
- Added: Override Skill Visibility subsection (skillOverrides in settings.json)
- Added: Progressive Disclosure subsection (context cost mechanics, zero tokens for user-only skills)
- Added: Detection Ceiling subsection (32-36 model-triggered skills)
- Added: Known bug #26251 (disable-model-invocation blocking user invocation)
- Changed: Plugins section expanded from stub to full documentation (structure, manifest, namespace, CLI, marketplace, testing)
- Changed: Key Files Reference updated with skills, plugins, skillOverrides, plugin manifest
- Changed: Summary updated with invocation control findings, progressive disclosure, plugins, skillOverrides
- Added: 9 new sources (official docs, community, plugin guides)

**[2026-07-23 17:30]**
- Added: Commands-Skills Merge section (v2.1.3, Jan 2026) with full rationale from GitHub issue #13115
- Added: `disable-model-invocation`, `context: fork`, progressive disclosure to SKILL.md format
- Changed: Summary updated to reflect merge (commands = legacy format)
- Changed: Skills section restructured to document pre/post-merge state
- Sources: github.com/anthropics/claude-code/issues/13115, code.claude.com/docs/en/skills, blog.devgenius.io

**[2026-01-15 08:35]**
- Initial document created from official Claude Code documentation
- Researched: overview, settings, memory, commands, skills, subagents, hooks, MCP, CLI
- Sources verified against code.claude.com/docs
