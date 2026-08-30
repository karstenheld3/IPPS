# INFO: Devin Desktop Recent Changes (Since 2026-08-04)

**Doc ID**: DVDT-IN02
**Goal**: Capture all Devin Desktop, Devin CLI, and AI model changes since DVDT-IN01 was last updated (2026-08-04) to prepare a targeted update pass
**Timeline**: Created 2026-08-27, Updated 1 time

## Summary

**New AI models (7 additions):**
- SWE-1.7 (released 2026-07-08): trained from Kimi K2.7 via RL, served on Cerebras at ~1000 tok/s, FrontierCode 1.1 Main 42.3% (4.5x over SWE-1.6). Lightning variant for lower latency [VERIFIED]
- Claude Opus 5: $5/$25 per MTok, 1M context, knowledge cutoff May 2026 (released 2026-07-24) [VERIFIED]
- Claude Sonnet 5 (released 2026-06-30): $2/$10 per MTok (introductory pricing made permanent 2026-08-10), 1M context, outperforms Opus 4.8 on FrontierCode [VERIFIED]
- Claude Fable 5: released 2026-06-09, suspended 2026-06-12 by US Commerce Dept BIS export control directive (first-ever for a commercial AI model). Remains suspended [VERIFIED]
- GPT-5.6 family: Sol ($4/$20), Terra ($2/$12), Luna ($0.20/$1.20), all 1.05M context (released 2026-07-09) [VERIFIED]
- Gemini 3.7 Flash (released 2026-08-13): $0.75/$3.75 per MTok (introductory), 1M context, Sonnet 5-level at half the cost [VERIFIED]
- Kimi K3 (released 2026-07-16, Moonshot AI): $3/$15 per MTok, 2.8T params (280B active MoE), open weights, FrontierCode 59.6 [VERIFIED]

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

[SWE-1.7](https://cognition.com/blog/swe-1-7) (released 2026-07-08) is Cognition's latest software engineering model, replacing SWE-1.6 as the primary in-house model. Trained from a [Kimi K2.7](https://docs.devin.ai/desktop/models) base model using Cognition's own reinforcement learning pipeline across 4 datacenters on 3 continents. Key training innovations: top-p entropy preservation, multi-cluster distributed training with compressed weight deltas, higher-quality data curation, and self-compaction for long agent trajectories.

**Serving**: Cerebras inference at ~1000 tokens/second. SWE-1.7 Lightning is a faster variant on Cerebras with the same intelligence at lower latency. The `/fast` CLI command selects SWE-1.7 Lightning when available.

**Benchmarks** (self-reported by Cognition):
- FrontierCode 1.1 Main: 42.3% (GPT-5.5: 43.0%, Opus 4.8: 46.5%)
- Terminal-Bench 2.1: 81.5% (GPT-5.5: 84.2%, Opus 4.8: 86.9%)
- SWE-Bench Multilingual: 77.8% (GPT-5.5: 76.8%, Opus 4.8: 84.4%)
- Cost per FrontierCode task: $1.97 (Opus 4.8: ~$1.80 per Artificial Analysis)
- Jump from SWE-1.6 (9.4% on FrontierCode 1.1 Main) to SWE-1.7 (42.3%) = 4.5x improvement

**Behavioral change**: SWE-1.7 spends more time investigating before editing, reads more of the codebase, and is better at finding root causes, hidden requirements, and edge cases.

No direct API access - available exclusively through Devin platform (Web, Desktop, CLI). Previous model naming in DVDT-IN01 referenced SWE-1.6 as latest. SWE-1.6 is now listed as "previous-generation" in official docs.

### 1.2 Claude Models

Three new Claude models since last update:

**[Claude Opus 5](https://platform.claude.com/docs/en/models/opus-5/overview)** (released 2026-07-24):
- $5/$25 per MTok (input/output), fast mode at $10/$50
- 1M token context, 128K max output
- Knowledge cutoff: May 2026
- SWE-bench Verified: 96.0%, SWE-bench Pro: 79.2%
- Positioned as "complex agentic coding and enterprise work"

**[Claude Sonnet 5](https://www.anthropic.com/news/claude-sonnet-5)** (released 2026-06-30):
- $2/$10 per MTok (input/output) - originally introductory through 2026-08-31, [made permanent on 2026-08-10](https://platform.claude.com/docs/en/about-claude/pricing) (scheduled increase to $3/$15 canceled)
- 1M token context, 128K max output
- Knowledge cutoff: January 2026
- Uses newer tokenizer producing ~30% more tokens for the same text vs Sonnet 4.6 (improved performance but higher token consumption per request)
- Outperforms Opus 4.8 on [FrontierCode](https://cognition.com/blog) benchmark
- Default model for Free and Pro plans; available to Max, Team, Enterprise
- Positioned as "most agentic Sonnet yet" - matches Opus 4.8 capability at Sonnet speed and price

**[Claude Fable 5](https://devin.ai/blog/claude-fable-5-available-in-devin/)** (released 2026-06-09, suspended 2026-06-12):
- $10/$50 per MTok, 1M context, 128K max output, "Mythos-class" flagship
- Knowledge cutoff: January 2026; adaptive thinking (always on), default effort `high`
- Made available in Devin Cloud, Desktop, and CLI on 2026-06-09
- **Suspension timeline**:
  - 2026-06-09: Anthropic launches Fable 5 publicly (first Mythos-class model for general availability)
  - 2026-06-12 17:21 ET: US Commerce Department Bureau of Industry and Security (BIS) issues export control directive requiring suspension of Fable 5 and Mythos 5 access by all foreign nationals worldwide, including Anthropic's own foreign-national employees. Anthropic given ~90 minutes to comply
  - 2026-06-12: Anthropic disables both models globally (cannot filter by nationality in real time)
  - 2026-06-26/27: Mythos 5 partially restored for 100+ US critical-infrastructure institutions
  - Fable 5 remains fully suspended for general use (no announced restart date)
- **Trigger**: Amazon report describing a method to bypass Fable 5's cybersecurity safeguards (ask model to "fix this code" after direct security-review prompt refused). Anthropic called the technique "narrow and non-universal" and argued the same capabilities exist in competing models
- First-ever US export control applied to a commercial AI model deployment under the Export Administration Regulations (EAR) framework
- Ultra mode in Devin now uses other available models instead

### 1.3 GPT-5.6 Family

[GPT-5.6](https://devin.ai/blog/gpt-5-6) released 2026-07-09 with three tiers sharing 1.05M context and 128K max output:

- **Sol** (flagship): $4/$20 per MTok (standard), $10/$45 (>272K tokens). Frontier reasoning for hardest tasks
- **Terra** (balanced): $2/$12 per MTok. Competitive with GPT-5.5 at half the price
- **Luna** (fast/cheap): $0.20/$1.20 per MTok

GPT-5.6 variants are Devin Local only; disabled in Cascade model picker (already noted in DVDT-IN01 3.6.22 update).

### 1.4 Other Models

**[Gemini 3.7 Flash](https://devin.ai/blog/gemini-37-flash)** (released 2026-08-13, by Google DeepMind):
- Live in Desktop and CLI
- $0.75/$3.75 per MTok (introductory through 2026-12-31), then $1.50/$7.50. 50% Devin-specific discount through 2026-08-27
- 1M token context, 64K max output
- Knowledge cutoff: March 2026
- Built on Gemini 3.6 Flash with algorithmic improvements to core reasoning; three thinking levels (low, medium [default], high)
- Multimodal input: text, image, audio, video
- [Model card](https://deepmind.google/models/model-cards/gemini-3-7-flash/): benchmarks show Sonnet 5-level performance at less than half the cost

**[Kimi K3](https://devin.ai/blog/kimi-k3/)** (released 2026-07-16, by Moonshot AI):
- Live in Desktop and CLI
- $3/$15 per MTok, $0.30 cache hit (flat across full 1M context, no long-context surcharge)
- 1,048,576 token context (1M), 128K max output (configurable up to 1M)
- 2.8 trillion total parameters (Mixture of Experts: 896 experts, 16 active per token = ~280B active)
- Kimi Delta Attention: hybrid linear attention + attention residuals for stable long-context recall
- Always-on thinking mode (reasoning by default); reasoning effort levels: none, low, medium, high, xhigh, max
- Native vision input (MMMU-Pro 81.6%); no audio/video input
- [Open weights](https://codersera.com/blog/kimi-k3-complete-guide-2026/) released 2026-07-27 under Modified MIT "Kimi K3 License"
- Benchmarks: GPQA Diamond 93.5% (highest open-weight), DeepSWE 67.5%, Terminal-Bench 2.1 88.3%, FrontierCode score 59.6
- FrontierCode 59.6, positioned between Opus 4.8 (60.6) and GPT-5.5 (58.2)

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

**Permission matrix** (key differences between modes):
- **Read-only tools** (file reads, grep, glob): Auto in all modes
- **File edits via `edit`/`write`**: Prompt in Normal, Auto (in workspace) in Accept Edits/Smart, Auto anywhere in Bypass, Prompt in Autonomous
- **Shell commands and fetches**: Prompt in Normal/Accept Edits, Auto when judged safe in Smart, Auto in Bypass/Autonomous
- **High-risk** (installs, `rm`, `sudo`, mutating `git`, `kubectl delete`, cloud CLIs, sensitive paths): Always Prompt in Normal/Accept Edits/Smart, Auto in Bypass/Autonomous

Never auto-approved in smart mode regardless of model judgment: package installs, downloads that execute code, mutating `git`, `rm`, `sudo`, `kubectl delete`, destructive cloud CLI operations (`aws`, `gcloud`, `az`, `terraform`), and reads/writes to dotenv files, key material, Git config, or agent config.

Switch via `/smart`, `/mode smart`, `Shift+Tab`, or `--permission-mode smart`. See [permissions reference](https://docs.devin.ai/cli/reference/permissions) for full details. Rolling out gradually via server-side flag - may not be available on all accounts yet.

### 3.2 Agent Mode and Permission Mode Separation

Agent profiles (normal, plan, ask) and permission modes (normal, accept edits, smart, bypass, autonomous) are now independent controls. `/plan <prompt>` switches mode and sends prompt in one step. Permission modes cycled with `Shift+Tab` or `/mode`.

### 3.3 Plugins Expanded

Plugins can now contribute rules, hooks, MCP servers, and custom subagents (not just skills). Still in closed beta (contact support@cognition.ai for access).

**Plugin directory structure**:
```
my-plugin/
  .devin-plugin/plugin.json   # Manifest (required)
  AGENTS.md                   # Always-on rules (optional)
  rules/                      # Triggered rules (optional)
  agents/<name>.md             # Custom subagent profiles (optional)
  hooks.json                  # Lifecycle hooks (optional)
  .mcp.json                   # MCP servers (optional, no client secrets)
  skills/<name>/SKILL.md       # Skills (optional)
```

**Manifest precedence**: `.devin-plugin/plugin.json` > `.claude-plugin/plugin.json` > root `plugin.json`

New sources and options:
- `git-subdir` source installs plugin from shared repo subdirectory (`devin plugins install acme/vendor-plugins#plugins/stripe`)
- Claude-compatible `.claude-plugin/plugin.json` manifest with `CLAUDE_PROJECT_DIR` and `CLAUDE_PLUGIN_ROOT` env vars
- [Agent Plugins 1.0.0](https://github.com/agentplugins/agent-plugins-spec) format compatibility (root `mcp.json`, `${PLUGIN_ROOT}` expansion)
- `devin plugins info` and install trust prompt list all contributed items before confirmation
- `devin plugins` commands require login; personal plugins sync to Cloud by default

### 3.4 New Commands and Slash Commands

- `devin rm <session-id-or-name>` - delete session with confirmation (`--force` for non-interactive); refuses if another Devin instance has the session open
- `devin desktop` - open Devin Desktop; `devin .` opens Desktop on current path
- `devin doctor` - check subagent profiles for incorrect frontmatter
- `/recap` - agent-generated short summary of work done, key decisions, and current progress
- `/rename <new title>` - rename current session
- `/btw <question>` - opens a side-chat panel running in parallel with the main agent. Questions answered using current conversation context; responses appear in a box below agent output without entering the main conversation. Agent continues working uninterrupted
- `/fast` - selects SWE-1.7 Lightning (or fallback fast model)
- `/usage` - richer panel with daily/weekly quota bars, reset times, extra usage balance
- These commands (plus `/loop`, `/mcp`, `/context`, `/add-dir`, `/undo-add-dir`, `/workspace`) are now ACP slash commands, invocable from any ACP client (Desktop, JetBrains, Zed)

### 3.5 Other CLI Features

- Editable command approvals: "Edit command" tweaks proposed command inline before approving; "Describe change to command" has fast model rewrite it in plain language (out-of-band, nothing enters conversation). ACP clients get the same affordances
- Global permission options: "always allow `<cmd>` in all projects" saved to user-level `config.json`; web-fetch prompts gained equivalent "always allow all web fetches" option
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
- `notify` config option: `"never"`, `"smart"` (default, notify only when terminal unfocused), or `"always"`. Uses BEL character, OSC 9 (iTerm2), and OSC 777 (rxvt-unicode) escape sequences
- MCP servers moved to dedicated config files (`mcp_config.json`) instead of `mcpServers` key in `config.json`. Existing entries migrated automatically on startup
- `/mode` now opens interactive selector (arrow keys + Enter) instead of printing static list

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
2. Claude Fable 5 remains suspended with no announced restart date (verified 2026-08-27)
3. Claude Sonnet 5 introductory pricing ($2/$10) made permanent on 2026-08-10 - no longer time-limited
4. Monitor Claude Opus 5 availability in Devin Desktop (confirmed in CLI, verify Desktop model picker)
5. Verify Gemini 3.7 Flash introductory pricing beyond Devin-specific discount expiry (2026-08-27)
6. Monitor Kimi K3 open weights availability (committed release 2026-07-27 under Modified MIT)

## 7. Sources

**Primary Sources:**
- `DVDT-IN02-SC-DVAI-DTCL`: https://docs.devin.ai/desktop/changelog - Desktop releases 3.6.22 through 3.8.20 [VERIFIED]
- `DVDT-IN02-SC-DVAI-CLCL`: https://docs.devin.ai/cli/changelog/stable - CLI stable changelog (smart mode, plugins, commands) [VERIFIED]
- `DVDT-IN02-SC-DVAI-MDLS`: https://docs.devin.ai/desktop/models - Current model list (SWE-1.7, SWE-1.7 Lightning) [VERIFIED]
- `DVDT-IN02-SC-DVAI-GPT56`: https://devin.ai/blog/gpt-5-6 - GPT-5.6 Sol/Terra/Luna announcement and pricing [VERIFIED]
- `DVDT-IN02-SC-DVAI-SNT5`: https://devin.ai/blog/claude-sonnet-5 - Claude Sonnet 5 in Devin announcement [VERIFIED]
- `DVDT-IN02-SC-DVAI-FBL5`: https://devin.ai/blog/claude-fable-5-available-in-devin/ - Claude Fable 5 release and suspension [VERIFIED]
- `DVDT-IN02-SC-DVAI-GMN37`: https://devin.ai/blog/gemini-37-flash - Gemini 3.7 Flash announcement [VERIFIED]
- `DVDT-IN02-SC-DVAI-KMK3`: https://devin.ai/blog/kimi-k3/ - Kimi K3 announcement and FrontierCode chart [VERIFIED]
- `DVDT-IN02-SC-DVAI-PRMS`: https://docs.devin.ai/cli/reference/permissions - Smart mode and permission system reference [VERIFIED]
- `DVDT-IN02-SC-DVAI-PLGN`: https://docs.devin.ai/cli/extensibility/plugins/overview - Plugin format, directory structure, manifest precedence [VERIFIED]
- `DVDT-IN02-SC-CLAI-MDLS`: https://platform.claude.com/docs/en/about-claude/models/overview - Claude model family overview (Opus 5, Sonnet 5, Fable 5 specs) [VERIFIED]
- `DVDT-IN02-SC-CLAI-PRCE`: https://platform.claude.com/docs/en/about-claude/pricing - Claude pricing (Sonnet 5 introductory made permanent, tokenizer note) [VERIFIED]
- `DVDT-IN02-SC-ANTH-SNT5`: https://www.anthropic.com/news/claude-sonnet-5 - Anthropic Sonnet 5 launch announcement (release date 2026-06-30, pricing permanence edit 2026-08-10) [VERIFIED]
- `DVDT-IN02-SC-COGN-SW17`: https://cognition.com/blog/swe-1-7 - SWE-1.7 training pipeline, benchmarks, Kimi K2.7 base, Cerebras serving [VERIFIED]
- `DVDT-IN02-SC-GDMN-G37F`: https://deepmind.google/models/model-cards/gemini-3-7-flash/ - Gemini 3.7 Flash model card (specs, benchmarks, pricing) [VERIFIED]
- `DVDT-IN02-SC-CLGC-G37P`: https://cloud.google.com/gemini-enterprise-agent-platform/generative-ai/pricing - Gemini 3.7 Flash pricing (introductory/standard rates, context caching) [VERIFIED]
- `DVDT-IN02-SC-MNST-KK3P`: https://kie.ai/blog/kimi-k3-pricing - Kimi K3 API pricing ($3/$15, $0.30 cache hit, flat 1M context) [VERIFIED]
- `DVDT-IN02-SC-HKAI-KK3R`: https://hokai.io/hub/models/kimi-k3 - Kimi K3 specs (2.8T params, 280B active, Delta Attention, benchmarks) [VERIFIED]
- `DVDT-IN02-SC-CDSR-KK3G`: https://codersera.com/blog/kimi-k3-complete-guide-2026/ - Kimi K3 open weights (Modified MIT, released 2026-07-27) [VERIFIED]
- `DVDT-IN02-SC-TCIN-CMP`: https://tech-insider.org/claude-fable-5-vs-opus-5-vs-gpt-5-6-sol-2026/ - Model comparison with pricing and benchmark tables [VERIFIED]

**Secondary Sources (Fable 5 suspension context):**
- `DVDT-IN02-SC-FRBS-FBL5`: https://councils.forbes.com/blog/the-first-time-washington-controlled-the-model-instead-of-the-chips - Forbes analysis of Commerce Dept export control precedent [VERIFIED]
- `DVDT-IN02-SC-GTLW-FBL5`: https://www.gtlaw.com/-/media/files/insights/alerts/2026/06/ - Greenberg Traurig legal alert on Fable 5 export control directive [VERIFIED]
- `DVDT-IN02-SC-TCFL-FBL5`: https://techfyle.com/claude-fable-5-government-suspension-anthropic-export-control-2026/ - TechFyle timeline of BIS directive (5:21pm ET, ~90min to comply) [VERIFIED]
- `DVDT-IN02-SC-BTHN-FBL5`: https://www.buildthisnow.com/blog/models/fable-5-ban-explained - Fable 5 ban timeline (Amazon trigger, Pentagon supply-chain-risk label) [VERIFIED]

## 8. Document History

**[2026-08-27 20:10]**
- Changed: Enriched all model entries with release dates, pricing, context/output specs, architecture details, and benchmark data from official sources
- Added: SWE-1.7 training pipeline (Kimi K2.7 base, RL across 4 datacenters), benchmark table, behavioral changes, Cerebras serving speed
- Added: Claude Sonnet 5 release date (2026-06-30), exact pricing ($2/$10 permanent), tokenizer change (+30% tokens)
- Added: Claude Fable 5 detailed suspension timeline (BIS directive, Amazon trigger, Mythos 5 partial restoration, EAR framework first)
- Added: Gemini 3.7 Flash release date (2026-08-13), pricing ($0.75/$3.75 introductory), specs (1M/64K), thinking levels, knowledge cutoff
- Added: Kimi K3 full specs (2.8T MoE, Delta Attention, open weights 2026-07-27, GPQA 93.5%)
- Added: Smart permission mode permission matrix comparing all 5 modes
- Added: Plugin directory structure and manifest precedence
- Added: /btw and /recap behavioral details, ACP slash command support, devin rm --force
- Added: notify config, MCP config file migration, /mode interactive selector
- Added: 14 new sources (Cognition, Anthropic, Google, Moonshot, Forbes, Greenberg Traurig, TechFyle, BuildThisNow)
- Changed: Summary updated with release dates, pricing, and key specs per model
- Changed: Next Steps updated with resolved items (Fable 5 status, Sonnet 5 pricing permanence)

**[2026-08-27 19:43]**
- Initial research document created
- Cataloged: 7 new AI models, 4 Desktop releases (3.6.27 through 3.8.20), major CLI update
- Identified 7 areas requiring updates in DVDT-IN01
