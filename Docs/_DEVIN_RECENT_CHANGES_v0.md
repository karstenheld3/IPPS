# INFO: Devin Desktop Recent Changes (Since 2026-08-04)

**Doc ID**: DVDT-IN02
**Goal**: Capture all Devin Desktop, Devin CLI, and AI model changes since DVDT-IN01 was last updated (2026-08-04) to prepare a targeted update pass
**Timeline**: Created 2026-08-27, Updated 0 times

## Summary

**New AI models (7 additions):**
- SWE-1.7 replaces SWE-1.6 as latest in-house model; SWE-1.7 Lightning variant on Cerebras [VERIFIED]
- Claude Opus 5: $5/$25 per MTok, 1M context, knowledge cutoff May 2026 (released 2026-07-24) [VERIFIED]
- Claude Sonnet 5: outperforms Opus 4.8 on FrontierCode, 30% less quota through 2026-08-31 [VERIFIED]
- Claude Fable 5: released 2026-06-09, suspended 2026-06-12 following US government directive [VERIFIED]
- GPT-5.6 family: Sol ($4/$20), Terra ($2/$12), Luna ($0.20/$1.20), all 1.05M context (released 2026-07-09) [VERIFIED]
- Gemini 3.7 Flash: live in Desktop and CLI, 50% discount through 2026-08-27 [VERIFIED]
- Kimi K3: live in Desktop and CLI, scores between Opus 4.8 and GPT-5.5 on FrontierCode [VERIFIED]

**Desktop releases (4 since 3.6.22):**
- 3.8.20: Agent Command Center (ACC) multi-window, Devin Local conversation sharing, plan mode with Markdown file, customization search, permission rule composition [VERIFIED]
- 3.7.25: faster sidebar for large session counts, MCP auth fix for GitLab/Atlassian [VERIFIED]
- 3.7.16: symlink write protection, Windows TLS cert store fix, "Plugins" renamed to "Extensions" [VERIFIED]
- 3.6.27: telemetry gated on account status [VERIFIED]

**CLI features (major update):**
- Smart permission mode: fast model judges action safety, auto-approves routine dev work [VERIFIED]
- Agent mode and permission mode are now independent controls [VERIFIED]
- Plugins expanded: can contribute rules, hooks, MCP servers, subagents [VERIFIED]
- New commands: `/recap`, `/rename`, `/btw` (parallel side-chat), `devin rm`, `devin doctor` [VERIFIED]
- Editable command approvals, configurable keybindings, MCP prompts as slash commands [VERIFIED]

**Cascade status:**
- Cascade-specific config hidden when disabled for team [VERIFIED]
- Devin Local now default agent for new tabs [VERIFIED]
- Devin Local now supports conversation sharing (previously listed as NOT supported in DVDT-IN01) [VERIFIED]

## Table of Contents

1. [New AI Models](#1-new-ai-models)
2. [Desktop Releases](#2-desktop-releases)
3. [CLI Changes](#3-cli-changes)
4. [Security Updates](#4-security-updates)
5. [Impact on DVDT-IN01](#5-impact-on-dvdt-in01)
6. [Next Steps](#6-next-steps)
7. [Sources](#7-sources)
8. [Document History](#8-document-history)

## 1. New AI Models

### 1.1 SWE-1.7

[SWE-1.7](https://docs.devin.ai/desktop/models) is Cognition's latest software engineering model, replacing SWE-1.6 as the primary in-house model. SWE-1.7 Lightning is a faster variant served on Cerebras with the same intelligence at lower latency. The `/fast` CLI command now selects SWE-1.7 Lightning when available.

Previous model naming in DVDT-IN01 referenced SWE-1.6 as latest. SWE-1.6 is now listed as "previous-generation" in official docs.

### 1.2 Claude Models

Three new Claude models since last update:

**[Claude Opus 5](https://platform.claude.com/docs/en/models/opus-5/overview)** (released 2026-07-24):
- $5/$25 per MTok (input/output), fast mode at $10/$50
- 1M token context, 128K max output
- Knowledge cutoff: May 2026
- SWE-bench Verified: 96.0%, SWE-bench Pro: 79.2%
- Positioned as "complex agentic coding and enterprise work"

**[Claude Sonnet 5](https://devin.ai/blog/claude-sonnet-5)** (released before 2026-08-27):
- Outperforms Opus 4.8 on [FrontierCode](https://cognition.com/blog) benchmark
- 30% less quota than Sonnet 4.6 through 2026-08-31
- Positioned as "best combination of speed and intelligence"

**[Claude Fable 5](https://devin.ai/blog/claude-fable-5-available-in-devin/)** (released 2026-06-09, suspended 2026-06-12):
- $10/$50 per MTok, "Mythos-class" flagship
- Made available in Devin Cloud, Desktop, and CLI on 2026-06-09
- Suspended 2026-06-12 following Anthropic announcement and US government directive
- Ultra mode now uses other available models instead

### 1.3 GPT-5.6 Family

[GPT-5.6](https://devin.ai/blog/gpt-5-6) released 2026-07-09 with three tiers sharing 1.05M context and 128K max output:

- **Sol** (flagship): $4/$20 per MTok (standard), $10/$45 (>272K tokens). Frontier reasoning for hardest tasks
- **Terra** (balanced): $2/$12 per MTok. Competitive with GPT-5.5 at half the price
- **Luna** (fast/cheap): $0.20/$1.20 per MTok

GPT-5.6 variants are Devin Local only; disabled in Cascade model picker (already noted in DVDT-IN01 3.6.22 update).

### 1.4 Other Models

**[Gemini 3.7 Flash](https://devin.ai/blog/gemini-37-flash)**: Live in Desktop and CLI. 50% introductory discount through 2026-08-27.

**[Kimi K3](https://devin.ai/blog/kimi-k3/)**: Live in Desktop and CLI. FrontierCode score 59.6, positioned between Opus 4.8 (60.6) and GPT-5.5 (58.2).

### 1.5 Current FrontierCode Ranking

Based on the [Kimi K3 announcement](https://devin.ai/blog/kimi-k3/) benchmark chart:

```
64.9  Claude Fable 5 (suspended)
63.6  GPT-5.6 Sol
60.6  Claude Opus 4.8
59.6  Kimi K3
58.2  GPT-5.5
56.7  Claude Sonnet 5
56.2  GPT-5.6 Terra
55.8  SWE-1.7
55.1  GPT-5.6 Luna
54.6  Claude Sonnet 4.6
```

Note: Claude Opus 5 not shown in this chart. The [Kimi K3 blog post](https://devin.ai/blog/kimi-k3/) includes a separate chart placing Opus 5 at 60.6, level with Opus 4.8.

## 2. Desktop Releases

Four stable releases since 3.6.22 (last covered in DVDT-IN01): 3.6.27, 3.7.16, 3.7.25, 3.8.20.

### 2.1 Release 3.8.20 (Latest Stable)

Source: [Desktop changelog](https://docs.devin.ai/desktop/changelog)

**ACC:**
- Follows selected space instead of being tied to one folder
- New `devin.agentWindow.location` setting splits ACC into a separate window
- Multiple agent windows can run side-by-side
- Improved Ctrl/Cmd+G mode switching performance

**Devin Local:**
- Multi-root workspace support including virtual filesystem folders
- Conversation sharing: sanitized transcripts (system prompts dropped, secrets redacted, paths normalized), team-visible link via actions menu
- Reliable mid-turn reverting: revert buttons appear immediately, cancel turn before rewinding
- Customizations panel: search across all sections (skills, subagents, rules, hooks, plugins, MCP servers), new Subagents section
- Plugins installed from Customizations default to personal plugins (sync to Cloud and other devices); `Install locally` for device-only
- Permission rule composition: explicit `deny:` always wins, "always allow" only appears when effective, denials identify responsible layer
- Running subagents can be stopped individually without cancelling the turn
- "Explain and Fix Problem" routes to Devin Local when Cascade disabled
- Status indicators on tabs (same as Cascade legacy tabs)
- `post_setup_worktree` hooks run for worktrees created from Devin Local sessions
- Terminal activity and user-edit activity sharing settings for Agent Client Protocol (ACP) agents
- Plan mode: full Markdown plan file with explicit Implement button
- `mcp_config.json` no longer shows "Property is not allowed" warnings
- Up/down arrows navigate chat input history again
- Migration wizard works in remote SSH workspaces

**Devin Cloud:**
- Session sidebar: improved filtering and sorting controls
- Live shell output streaming while commands run
- Session tabs and command palette: Copy Session URL
- Network config changes and access requests manageable inline from chat
- Failed sends restore draft to input

**Desktop general:**
- Windows: `Install Devin CLI` writes a shim, so updating Desktop updates the `devin` command
- Linux: `.deb` upgrade no longer removes shared Microsoft apt keyring
- Workspace trust warnings on sidebar, composer, and welcome page; trust prompt to activate agents
- Session rename from tab dropdown
- Enterprise: link to request more usage at Agent Compute Units (ACU) limits
- VS Code 1.126 base

### 2.2 Release 3.7.25

- Faster sidebar for users with thousands of cached sessions (lazy processing)
- MCP auth fix for self-hosted GitLab servers and older Atlassian MCP instances

### 2.3 Release 3.7.16

- "Restart to Update" asks confirmation when local agents are still working
- Settings and Keyboard Shortcuts open as regular editor tabs by default (`"workbench.editor.useModal": "all"` for modal)
- Bug fix: editor keybindings accidentally triggered from agent chat
- "Plugins" (IDE extension marketplaces) renamed to "Extensions"
- Cascade-specific configuration hidden when Cascade disabled for team
- Devin Local conversation sharing (first appeared here)
- Customizations panel with search, Subagents section, plugin refresh
- Clickable `+X -Y` diff summary opens multi-diff editor
- Duplicate session and send as fork (opens in new tab)
- Editable queued messages
- Separate MCP server logs per server (`MCP: <server>` output channels)
- Large-file ACP reads bounded and paginated

### 2.4 Release 3.6.27

- Telemetry not started before account status resolves (no collection for opted-out accounts)

## 3. CLI Changes

Source: [CLI changelog (stable)](https://docs.devin.ai/cli/changelog/stable)

### 3.1 Smart Permission Mode

New permission mode where workspace edits auto-approve (like Accept Edits) and a fast model judges whether other actions are safe to auto-run. Falls back to normal prompt when uncertain.

Never auto-approved in smart mode: package installs, `rm`, `sudo`, `kubectl delete`, cloud CLIs, sensitive paths (dotenv, key material, Git config, agent config).

Switch via `/smart`, `/mode smart`, `Shift+Tab`, or `--permission-mode smart`. See [permissions reference](https://docs.devin.ai/cli/reference/permissions) for full details.

### 3.2 Agent Mode and Permission Mode Separation

Agent profiles (normal, plan, ask) and permission modes (normal, accept edits, smart, bypass, autonomous) are now independent controls. `/plan <prompt>` switches mode and sends prompt in one step. Permission modes cycled with `Shift+Tab` or `/mode`.

### 3.3 Plugins Expanded

Plugins can now contribute rules, hooks, MCP servers, and custom subagents (not just skills). New sources:
- `git-subdir` source installs plugin from shared repo subdirectory
- Claude-compatible `.claude-plugin/plugin.json` manifest
- [Agent Plugins 1.0.0](https://github.com/agentplugins/agent-plugins-spec) format compatibility
- `devin plugins` commands require login; personal plugins sync to Cloud by default

### 3.4 New Commands and Slash Commands

- `devin rm <session-id-or-name>` - delete session with confirmation
- `devin desktop` - open Devin Desktop; `devin .` opens Desktop on current path
- `devin doctor` - check subagent profiles for incorrect frontmatter
- `/recap` - agent-generated session summary
- `/rename <new title>` - rename current session
- `/btw` - side-chat panel running in parallel with main agent
- `/fast` - selects SWE-1.7 Lightning (or fallback fast model)
- `/usage` - richer panel with daily/weekly quota bars, reset times, extra usage balance

### 3.5 Other CLI Features

- Editable command approvals: edit proposed command inline or describe change in plain language for fast model rewrite
- Global permission options: "always allow `<cmd>` in all projects" saved to user-level `config.json`
- Configurable keybindings via `keymap` section in `config.json`; `/shortcuts` lists all bindings
- MCP prompts as `/mcp__<server>__<prompt>` slash commands
- Copilot skill discovery from `.github/skills/` and `~/.copilot/skills/`
- `subagents_enabled` setting (on by default) to toggle subagent tools
- Megaplan keywords (`megaplan`, `ultraplan`, `masterplan`) trigger extensive planning
- Shell integration removed (was preview); `devin shell remove` to clean up
- Skill improvements: full `SKILL.md` passed to model (not truncated), `$ARGUMENTS`/`$1-$9` interpolation, skills survive context compaction
- `SessionEnd` lifecycle hooks with reason; `Stop` hooks receive `last_assistant_message`
- Plugin-contributed skills, rules, hooks, subagents labeled with plugin name in lists
- Ask and Plan modes can use `webfetch` and `notebook_read` for research
- Broader Claude plugin compatibility: `hooks/hooks.json`, `CLAUDE_PROJECT_DIR`, `CLAUDE_PLUGIN_ROOT` env vars, `tools` as alias for `allowed-tools`
- `/share` displays server-returned share URL
- Instant slash commands (`/status`, `/context`, `/fast`, `/help`) run immediately while agent is working
- Background shells tray (`Ctrl+B`) lists running commands

## 4. Security Updates

- **Symlink write protection**: `edit`, `write`, `apply_patch`, `notebook_edit` tools refuse to write through symlinks (Desktop 3.7.16 + CLI)
- **Restricted Mode**: all agents unavailable in untrusted workspaces, hooks don't load
- **Permission rule composition**: explicit `deny:` always wins across levels (enterprise, mode, user, project, subagent)
- **`sudo` handling**: password prompts fail fast with explanation instead of hanging
- **Windows TLS**: root and intermediate certificates loaded from Windows cert store again (fixes corporate CA/proxy issues)
- **Separate MCP logs**: each server gets its own `MCP: <server>` output channel

## 5. Impact on DVDT-IN01

Changes required in `INFO_HOW_DEVIN_WORKS.md [DVDT-IN01]`:

### 5.1 Header Block

- Update Timeline: "Updated 10 times (latest 2026-08-27)"
- Update Version scope: add latest Desktop version (3.8.20) and CLI version

### 5.2 Summary Section

- Update model list: add SWE-1.7, Claude Opus 5, Claude Sonnet 5, GPT-5.6 Sol/Terra/Luna, Gemini 3.7 Flash, Kimi K3
- Note Claude Fable 5 suspension
- Update "Does NOT support: Conversation Sharing" to "DOES support" for Devin Local
- Add smart permission mode to Devin Local specifics
- Add agent/permission mode separation
- Update extensibility: plugins contribute rules, hooks, MCP servers, subagents

### 5.3 AI Models Section

- Add SWE-1.7 and SWE-1.7 Lightning (replace SWE-1.6 as latest)
- Add Claude Opus 5 with pricing and benchmarks
- Add Claude Sonnet 5 with FrontierCode comparison
- Add Claude Fable 5 with suspension note
- Add GPT-5.6 Sol/Terra/Luna family
- Add Gemini 3.7 Flash
- Add Kimi K3

### 5.4 Customization Section

- Smart permission mode details
- Agent/permission mode separation
- Plugin expansion (rules, hooks, MCP servers, subagents)
- Agent Plugins 1.0.0 format
- Configurable keybindings
- Copilot skill discovery

### 5.5 CLI Section

- New commands: `devin rm`, `devin desktop`, `devin doctor`
- New slash commands: `/recap`, `/rename`, `/btw`, `/fast`, `/usage`
- Shell integration removed
- MCP prompts support

### 5.6 Security Section

- Symlink write protection
- Restricted Mode for untrusted workspaces
- `sudo` handling improvement

### 5.7 Corrections

- Devin Local now supports conversation sharing (was listed as NOT supported)
- "Plugins" (IDE extension marketplaces) renamed to "Extensions" in 3.7.16
- SWE-1.6 is now "previous-generation", not latest

## 6. Next Steps

1. Update `INFO_HOW_DEVIN_WORKS.md [DVDT-IN01]` with changes cataloged in Section 5
2. Verify model pricing against official docs (prices may have changed since blog posts)
3. Check if Claude Fable 5 suspension has been lifted since 2026-06-12
4. Monitor Claude Opus 5 availability in Devin Desktop (confirmed in CLI, verify Desktop model picker)

## 7. Sources

**Primary Sources:**
- `DVDT-IN02-SC-DVAI-DTCL`: https://docs.devin.ai/desktop/changelog - Desktop releases 3.6.22 through 3.8.20 [VERIFIED]
- `DVDT-IN02-SC-DVAI-CLCL`: https://docs.devin.ai/cli/changelog/stable - CLI stable changelog (smart mode, plugins, commands) [VERIFIED]
- `DVDT-IN02-SC-DVAI-MDLS`: https://docs.devin.ai/desktop/models - Current model list (SWE-1.7, SWE-1.7 Lightning) [VERIFIED]
- `DVDT-IN02-SC-DVAI-GPT56`: https://devin.ai/blog/gpt-5-6 - GPT-5.6 Sol/Terra/Luna announcement and pricing [VERIFIED]
- `DVDT-IN02-SC-DVAI-SNT5`: https://devin.ai/blog/claude-sonnet-5 - Claude Sonnet 5 announcement and FrontierCode results [VERIFIED]
- `DVDT-IN02-SC-DVAI-FBL5`: https://devin.ai/blog/claude-fable-5-available-in-devin/ - Claude Fable 5 release and suspension [VERIFIED]
- `DVDT-IN02-SC-DVAI-GMN37`: https://devin.ai/blog/gemini-37-flash - Gemini 3.7 Flash announcement [VERIFIED]
- `DVDT-IN02-SC-DVAI-KMK3`: https://devin.ai/blog/kimi-k3/ - Kimi K3 announcement and FrontierCode chart [VERIFIED]
- `DVDT-IN02-SC-DVAI-PRMS`: https://docs.devin.ai/cli/reference/permissions - Smart mode and permission system reference [VERIFIED]
- `DVDT-IN02-SC-CLAI-MDLS`: https://platform.claude.com/docs/en/about-claude/models/overview - Claude model family overview (Opus 5, Sonnet 5, Fable 5 specs) [VERIFIED]
- `DVDT-IN02-SC-TCIN-CMP`: https://tech-insider.org/claude-fable-5-vs-opus-5-vs-gpt-5-6-sol-2026/ - Model comparison with pricing and benchmark tables [VERIFIED]

## 8. Document History

**[2026-08-27 19:43]**
- Initial research document created
- Cataloged: 7 new AI models, 4 Desktop releases (3.6.27 through 3.8.20), major CLI update
- Identified 7 areas requiring updates in DVDT-IN01
