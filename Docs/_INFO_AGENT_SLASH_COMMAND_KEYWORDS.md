# INFO: Agent Slash Command Keywords

**Doc ID**: SLASHCMDS-IN01
**Goal**: Catalog built-in `/[command]` keywords across 13 chatbots and coding agents as a joint reserved list and per-agent lists

## Summary

This document catalogs built-in /[command] keywords across 13 chatbots and coding agents. It contains a joint reserved keyword list (the union of all per-agent keywords) and a per-agent list for each product surface.

- **Agents covered**: 13
- **Joint reserved keywords**: 364
- **Agents without vendor-built-in slash commands**: Google Gemini
- **Verification check date**: 2026-11-17

**Keyword entry counts per agent** (including aliases):

- ChatGPT: 28 entries
- Claude Code: 139 entries
- Devin: 64 entries
- GitHub Copilot: 134 entries
- Google Gemini: 0 entries
- Google Jules: 1 entries
- Google Antigravity: 60 entries
- Cursor: 49 entries
- OpenAI Codex: 74 entries
- Gemini CLI: 58 entries
- OpenCode: 50 entries
- Windsurf (Cascade): 3 entries
- Cline: 22 entries

**Most-shared keywords** (across the most agents):

- `/model` - 11 agents
- `/plan` - 10 agents
- `/fork` - 9 agents
- `/help` - 9 agents
- `/quit` - 9 agents
- `/mcp` - 9 agents
- `/new` - 9 agents
- `/clear` - 9 agents
- `/usage` - 8 agents
- `/compact` - 8 agents

**Caveats**:
- Some surface-specific documentation (ChatGPT web/mobile, Codex desktop/web, Cursor IDE built-ins beyond `/summarize`) is not publicly enumerated, so absence claims rely on the vendor docs that were available.
- Windsurf (Cascade) `/model` is labeled `[ASSUMED]` because the only source is a Tier 4 community shortcut reference; a second vendor source would be needed for `[VERIFIED]`.
- OpenAI Codex desktop app and Codex web surfaces are covered as far as vendor documentation exists; no Codex-specific desktop or web slash-command inventory was found, so the section records CLI and IDE extension commands only.

## Table of Contents

- [Summary](#summary)
- [1. Scope and Method](#1-scope-and-method)
- [2. Joint Reserved Keyword List](#2-joint-reserved-keyword-list)
- [3. Agent: ChatGPT](#3-agent-chatgpt)
- [4. Agent: Claude Code](#4-agent-claude-code)
- [5. Agent: Devin](#5-agent-devin)
- [6. Agent: GitHub Copilot](#6-agent-github-copilot)
- [7. Agent: Google Gemini](#7-agent-google-gemini)
- [8. Agent: Google Jules](#8-agent-google-jules)
- [9. Agent: Google Antigravity](#9-agent-google-antigravity)
- [10. Agent: Cursor](#10-agent-cursor)
- [11. Agent: OpenAI Codex](#11-agent-openai-codex)
- [12. Agent: Gemini CLI](#12-agent-gemini-cli)
- [13. Agent: OpenCode](#13-agent-opencode)
- [14. Agent: Windsurf (Cascade)](#14-agent-windsurf-cascade)
- [15. Agent: Cline](#15-agent-cline)
- [16. Cross-Agent Observations](#16-cross-agent-observations)
- [17. Exclusions](#17-exclusions)
- [18. Sources](#18-sources)
- [Document History](#document-history)

## 1. Scope and Method

This document records every built-in `/[command]` keyword that 13 chatbots and coding agents define and recognize in their chat or prompt input, including popup slash menus, command palettes, and CLI command dispatchers. A keyword is a name `/[name]` that triggers product behavior when typed. Entry kinds are: `built-in`, `bundled`, `alias`, `deprecated`, `hidden`, `experimental`, and `conditional`. User-defined, project-level, plugin, extension, and MCP-provided commands are excluded from the keyword lists; their collision behavior with built-in names is recorded per agent in Section 17.

The 13 agents and their covered surfaces are:

- **ChatGPT**: chatgpt.com web, desktop apps, mobile apps; composer slash menu
- **Claude Code**: CLI, VS Code and JetBrains extensions, desktop app, web app; bundled commands
- **Devin**: Cognition's Devin agent: web app sessions, Devin CLI, Devin agent inside Devin Desktop (Devin Local)
- **GitHub Copilot**: chat in VS Code, Visual Studio, JetBrains, Xcode, Eclipse; github.com chat; GitHub Mobile; Copilot CLI; coding agent
- **Google Gemini**: consumer and Workspace chatbot on gemini.google.com, mobile apps, Chrome and Workspace side panels
- **Google Jules**: jules.google web app, Jules Tools CLI, Jules API
- **Google Antigravity**: Antigravity IDE editor chat and Agent Manager
- **Cursor**: IDE Agent chat, Cursor CLI, web and mobile agents
- **OpenAI Codex**: Codex CLI, IDE extension, desktop app, Codex web
- **Gemini CLI**: `gemini` terminal agent and its IDE integration
- **OpenCode**: the open-source terminal agent at https://opencode.ai and its desktop and IDE clients
- **Windsurf (Cascade)**: Cascade chat panel in the Windsurf IDE, Devin Desktop, and the JetBrains plugin
- **Cline**: VS Code extension, its forks and JetBrains port, Cline CLI

Evidence ladder, highest available per agent:
1. Vendor source code at a recorded tag or commit
2. Vendor documentation, command reference, release notes, or changelog
3. In-product observation of an installed product, popup slash menu, help output, or bundle inspection, labeled `[TESTED]`
4. Vendor help center or forum posts by vendor staff
5. Third-party posts labeled `[COMMUNITY]`, never alone

For open-source agents (Codex, Gemini CLI, OpenCode, Cline) the official repository is shallow-cloned into `_download_gitignore/[mnemonic]/` and the command registry is searched in code, then compared with documentation and release notes. Closed-source agents are covered by documentation plus release notes of the last six months plus local observation where the product is installed. Every agent uses two or more independent evidence types where they exist. Code and documentation conflicts are recorded as Findings card entries. Accessed dates use the request date of each prompt.

## 2. Joint Reserved Keyword List

- `/?` - display help information | Agents: Gemini CLI | Count: 1 | Meaning: same | Spellings: same | Differences: only in Gemini CLI
- `/about` - show CLI version, system, and account info; show version info | Agents: Cursor, Gemini CLI | Count: 2 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/accept-edits` - switch to Accept Edits mode | Agents: Devin | Count: 1 | Meaning: same | Spellings: same | Differences: only in Devin
- `/account` - view Cline account information | Agents: Cline | Count: 1 | Meaning: same | Spellings: same | Differences: only in Cline
- `/act` - switch to Act mode | Agents: Cline | Count: 1 | Meaning: same | Spellings: same | Differences: only in Cline
- `/add-dir` - grant Claude access to an additional directory for the session; add an additional workspace directory... | Agents: Claude Code, Devin, GitHub Copilot, Google Antigravity | Count: 4 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/advisor` - enable or disable the advisor tool | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/af` - search Agent Finder for installable MCP servers, tools, skills, and agents | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/after` - schedule a one-off prompt for a future time | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/agent` - select a custom agent for the session; cycle to the next agent in the desktop composer | Agents: GitHub Copilot, OpenCode | Count: 2 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/agents` - list, create, or edit subagents; alias of /subagents for selecting subagents... | Agents: Claude Code, Gemini CLI, GitHub Copilot, Google Antigravity, OpenAI Codex, OpenCode | Count: 6 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/agy-customizations` - load the customization reference for rules, skills, plugins, hooks, and MCP servers | Agents: Google Antigravity | Count: 1 | Meaning: same | Spellings: same | Differences: only in Google Antigravity
- `/allow-all` - alias of /permissions allow-all | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/allow-all-tools` - turn tool auto-approval on or show its state | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/android` - alias of /mobile | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/antigravity-guide` - ask how to use or configure Antigravity from the official docs | Agents: Google Antigravity | Count: 1 | Meaning: same | Spellings: same | Differences: only in Google Antigravity
- `/app` - alias of /desktop; open the current session in the GitHub Copilot app... | Agents: Claude Code, GitHub Copilot, OpenAI Codex | Count: 3 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/approve` - approve one retry of a recent automatic-review denial when automatic review is active; approve one retry of a recent auto-review denial | Agents: ChatGPT, OpenAI Codex | Count: 2 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/apps` - manage apps | Agents: OpenAI Codex | Count: 1 | Meaning: same | Spellings: same | Differences: only in OpenAI Codex
- `/archive` - archive the current chat; archive a cloud session; archive the current session | Agents: ChatGPT, Devin, OpenAI Codex | Count: 3 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/artifact` - open the Artifact Review panel | Agents: Google Antigravity | Count: 1 | Meaning: same | Spellings: same | Differences: only in Google Antigravity
- `/artifact-capabilities` - bundled skill for artifact capabilities | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/artifact-diagramming` - bundled skill for artifact diagramming guidance | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/artifacts` - list owned or shared artifacts and attach, open, or copy one | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/ask` - ask a one-shot question without making code changes; ask a one-shot side question without changing code; toggle Ask mode for read-only questions | Agents: Cursor, Devin, GitHub Copilot | Count: 3 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/attach-files` - open a file picker and attach files to the message | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/attach-folder` - open a folder picker and attach a folder to the message | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/auth` - manage authentication | Agents: Gemini CLI | Count: 1 | Meaning: same | Spellings: same | Differences: only in Gemini CLI
- `/auto-mode-setup` - draft autoMode.environment entries from the project and recent sessions | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/auto-run` - alias of /run-everything | Agents: Cursor | Count: 1 | Meaning: same | Spellings: same | Differences: only in Cursor
- `/autoapprove` - toggle global auto-approval of safe commands in agent mode | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/autocompact` - set the auto-compact window size | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/autofix-pr` - spawn a cloud session that watches the current PR and pushes fixes | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/automation` - set up a scheduled background automation in the Automations tab | Agents: Google Antigravity | Count: 1 | Meaning: same | Spellings: same | Differences: only in Google Antigravity
- `/autonomous` - switch to Autonomous mode, requires --sandbox | Agents: Devin | Count: 1 | Meaning: same | Spellings: same | Differences: only in Devin
- `/autopilot` - switch to Autopilot mode and optionally start with a prompt | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/background` - detach the session to run as a background agent; alias of /tasks that toggles background tasks view | Agents: Claude Code, Gemini CLI | Count: 2 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/bashes` - alias of /tasks | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/batch` - orchestrate large-scale changes across a codebase in parallel | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/bedrock` - configure Bedrock when the feature is enabled | Agents: Cursor | Count: 1 | Meaning: same | Spellings: same | Differences: only in Cursor
- `/bg` - alias of /background; alias of /tasks | Agents: Claude Code, Gemini CLI | Count: 2 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/boost` - run on-demand multi-agent deep reasoning loops | Agents: Google Antigravity | Count: 1 | Meaning: same | Spellings: same | Differences: only in Google Antigravity
- `/branch` - create a conversation branch to try a different direction; alias of /fork for branching the session; alias of /fork | Agents: Claude Code, GitHub Copilot, Google Antigravity | Count: 3 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/browser` - delegate web browsing, UI verification, and in-browser debugging to the browser subagent | Agents: Google Antigravity | Count: 1 | Meaning: same | Spellings: same | Differences: only in Google Antigravity
- `/btw` - ask a side question without adding it to the conversation... | Agents: Claude Code, Devin, GitHub Copilot, Google Antigravity, OpenAI Codex, OpenCode | Count: 6 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/bug` - report a bug or share the conversation; alias of /feedback for submitting a bug report; submit a bug report | Agents: Claude Code, Gemini CLI, GitHub Copilot | Count: 3 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/bug-memory` - capture a V8 heap snapshot for a bug report, present in source but absent from docs | Agents: Gemini CLI | Count: 1 | Meaning: same | Spellings: same | Differences: only in Gemini CLI
- `/bypass` - switch to Bypass mode | Agents: Devin | Count: 1 | Meaning: same | Spellings: same | Differences: only in Devin
- `/caffeinate` - alias of /keep-alive to keep the machine awake | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/cd` - change the session working directory; change the current working directory | Agents: Claude Code, GitHub Copilot, OpenAI Codex, OpenCode | Count: 4 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/changelog` - show interactive release notes for Copilot CLI; open the interactive release notes viewer | Agents: GitHub Copilot, Google Antigravity | Count: 2 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/chat` - choose a chat without a project before starting a new chat; browse auto-saved conversations and manage chat checkpoints | Agents: ChatGPT, Gemini CLI | Count: 2 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/checkpoint` - alias of /rewind | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/checkup` - alias of /doctor | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/chrome` - launch or manage Claude in Chrome | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/chronicle` - review and analyze session history | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/claude-api` - bundled skill for Claude API projects | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/claude-in-chrome` - bundled skill for Claude in Chrome tasks | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/clean` - alias of /stop that stops all background terminals | Agents: OpenAI Codex | Count: 1 | Meaning: same | Spellings: same | Differences: only in OpenAI Codex
- `/clear` - wipe conversation history and start fresh... | Agents: Claude Code, Cline, Cursor, Devin, Gemini CLI, GitHub Copilot, Google Antigravity, OpenAI Codex, OpenCode | Count: 9 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/clikit` - inspect or configure CLI UI component internals | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/cloud` - run the chat in the cloud when cloud execution is available; manage cloud sessions; switch to Cloud connection or open cloud options (extension surface only) | Agents: ChatGPT, Devin, OpenAI Codex | Count: 3 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/cloud-environment` - choose the cloud environment for the chat; open the cloud environment picker (extension surface only) | Agents: ChatGPT, OpenAI Codex | Count: 2 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/code` - switch to Code mode or run a prompt in it | Agents: Devin | Count: 1 | Meaning: same | Spellings: same | Differences: only in Devin
- `/code-review` - bundled skill for local or cloud code review | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/codesearch` - open the interactive Code Search panel | Agents: Google Antigravity | Count: 1 | Meaning: same | Spellings: same | Differences: only in Google Antigravity
- `/collect-debug-logs` - collect and export debug logs | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/color` - set the remote-control prompt color | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/commands` - manage custom slash commands loaded from .toml files | Agents: Gemini CLI | Count: 1 | Meaning: same | Spellings: same | Differences: only in Gemini CLI
- `/commit` - generate a commit message from staged changes | Agents: Cursor | Count: 1 | Meaning: same | Spellings: same | Differences: only in Cursor
- `/compact` - compact the current chat's context; summarize the conversation to free context... | Agents: ChatGPT, Claude Code, Cline, Devin, Gemini CLI, GitHub Copilot, OpenAI Codex, OpenCode | Count: 8 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/compress` - alias of /summarize; compress the context by replacing it with a summary | Agents: Cursor, Gemini CLI | Count: 2 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/confetti` - celebrate with confetti | Agents: Devin | Count: 1 | Meaning: same | Spellings: same | Differences: only in Devin
- `/config` - change settings; open interactive config editor; alias of /settings for changing configuration; ... | Agents: Claude Code, Cline, Cursor, Devin, GitHub Copilot, Google Antigravity, OpenAI Codex | Count: 7 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/connect` - add a model provider or integration | Agents: OpenCode | Count: 1 | Meaning: same | Spellings: same | Differences: only in OpenCode
- `/context` - visualize what is loaded into the context window; show context window usage; show current session context usage; ... | Agents: Claude Code, Devin, GitHub Copilot, Google Antigravity | Count: 4 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/continue` - alias of /resume; continue a previous session; alias of /resume for continuing a previous session; ... | Agents: Claude Code, Devin, GitHub Copilot, OpenCode | Count: 4 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/conversation` - alias of /resume for opening the conversation picker | Agents: Google Antigravity | Count: 1 | Meaning: same | Spellings: same | Differences: only in Google Antigravity
- `/copy` - copy the last response or selected code block; copy the last response to clipboard... | Agents: Claude Code, Cursor, Devin, Gemini CLI, GitHub Copilot, Google Antigravity, OpenAI Codex | Count: 7 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/copy-conversation-id` - copy the current conversation ID | Agents: Cursor | Count: 1 | Meaning: same | Spellings: same | Differences: only in Cursor
- `/copy-request-id` - copy the last request ID | Agents: Cursor | Count: 1 | Meaning: same | Spellings: same | Differences: only in Cursor
- `/corgi` - toggle corgi mode, marked hidden in source | Agents: Gemini CLI | Count: 1 | Meaning: same | Spellings: same | Differences: only in Gemini CLI
- `/cost` - show token usage and spend for the session | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/create-agent` - create a custom agent definition in agent mode | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/create-canvas` - invoke the canvas-authoring skill | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/create-hook` - create a lifecycle hook in agent mode | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/create-instruction` - create a custom instruction file in agent mode | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/create-prompt` - create a prompt file in agent mode | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/create-skill` - create a skill file in agent mode | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/credits` - view remaining AI credits and purchase links | Agents: Google Antigravity | Count: 1 | Meaning: same | Spellings: same | Differences: only in Google Antigravity
- `/cs` - alias of /codesearch | Agents: Google Antigravity | Count: 1 | Meaning: same | Spellings: same | Differences: only in Google Antigravity
- `/cursor` - alias of /open | Agents: Cursor | Count: 1 | Meaning: same | Spellings: same | Differences: only in Cursor
- `/cwd` - show the current working directory; alias of /pwd that shows the current working directory | Agents: GitHub Copilot, OpenAI Codex | Count: 2 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/daemon` - manage the local background server | Agents: OpenAI Codex | Count: 1 | Meaning: same | Spellings: same | Differences: only in OpenAI Codex
- `/dangerous` - alias of /bypass | Agents: Devin | Count: 1 | Meaning: same | Spellings: same | Differences: only in Devin
- `/dataviz` - bundled skill for data visualization | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/daybreak` - toggle Daybreak on or off for OpenAI-provider accounts with access | Agents: OpenAI Codex | Count: 1 | Meaning: same | Spellings: same | Differences: only in OpenAI Codex
- `/debug` - bundled skill to debug issues; copy session debug JSON to clipboard; toggle Debug mode or submit a prompt in it; ... | Agents: Claude Code, Cursor, GitHub Copilot, OpenCode | Count: 4 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/debug-config` - show config layers and requirement sources for debugging | Agents: OpenAI Codex | Count: 1 | Meaning: same | Spellings: same | Differences: only in OpenAI Codex
- `/debug-m-drop` - debugging command for memory drop, labeled DO NOT USE in source | Agents: OpenAI Codex | Count: 1 | Meaning: same | Spellings: same | Differences: only in OpenAI Codex
- `/debug-m-update` - debugging command for memory update, labeled DO NOT USE in source | Agents: OpenAI Codex | Count: 1 | Meaning: same | Spellings: same | Differences: only in OpenAI Codex
- `/deep-planning` - run an extended planning session that creates implementation_plan.md | Agents: Cline | Count: 1 | Meaning: same | Spellings: same | Differences: only in Cline
- `/deep-research` - bundled dynamic workflow for deep research | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/delegate` - delegate the current task to Copilot | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/delete` - delete the current conversation; permanently delete the current session | Agents: GitHub Copilot, OpenAI Codex | Count: 2 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/design` - bundled skill for UI/UX design artifacts | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/design-login` - log in to standalone Claude Design | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/design-sync` - bundled skill to sync design system components | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/desktop` - open the current session in Claude Desktop | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/details` - toggle inline tool execution details | Agents: OpenCode | Count: 1 | Meaning: same | Spellings: same | Differences: only in OpenCode
- `/diagnose` - diagnose problems in the workspace or session | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/diff` - open interactive diff of uncommitted changes; show the Git diff including untracked files; open the interactive diff viewer | Agents: Claude Code, GitHub Copilot, Google Antigravity, OpenAI Codex | Count: 4 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/dir` - alias of /directory | Agents: Gemini CLI | Count: 1 | Meaning: same | Spellings: same | Differences: only in Gemini CLI
- `/directory` - manage workspace directories | Agents: Gemini CLI | Count: 1 | Meaning: same | Spellings: same | Differences: only in Gemini CLI
- `/disableautoapprove` - turn off global auto-approval in agent mode | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/disableyolo` - alias of /disableAutoApprove | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/doc` - generate documentation for the selected symbol; generate documentation for selected code | Agents: Cursor, GitHub Copilot | Count: 2 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/docs` - open Gemini CLI documentation in a browser | Agents: Gemini CLI | Count: 1 | Meaning: same | Spellings: same | Differences: only in Gemini CLI
- `/doctor` - bundled skill to diagnose install and environment issues | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/downgrade` - downgrade the CLI to a specific version | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/editor` - set external editor preference; compose the current prompt in the external editor set in EDITOR/VISUAL | Agents: Gemini CLI, OpenCode | Count: 2 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/effort` - set model effort level or toggle ultracode; set or inspect the active model's reasoning effort level... | Agents: Claude Code, Google Antigravity, OpenCode | Count: 3 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/env` - show the pre-conversation environment picker state | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/every` - schedule a recurring prompt | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/exit` - quit the CLI; exit the CLI; exit the interactive CLI; ... | Agents: Claude Code, Cursor, Devin, Gemini CLI, GitHub Copilot, Google Antigravity, OpenAI Codex, OpenCode | Count: 8 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/experimental` - toggle experimental features | Agents: GitHub Copilot, OpenAI Codex | Count: 2 | Meaning: same | Spellings: same | Differences: none
- `/explain` - explain selected code; ask Cascade to explain the selected or referenced code | Agents: Cursor, Windsurf (Cascade) | Count: 2 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/export` - save the conversation to a file or clipboard; alias of /share for exporting the session; export the conversation as Markdown; ... | Agents: Claude Code, GitHub Copilot, OpenAI Codex, OpenCode | Count: 4 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/export-gist` - export the transcript to a secret gist | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/export-session` - export the current session to a JSON file | Agents: Gemini CLI | Count: 1 | Meaning: same | Spellings: same | Differences: only in Gemini CLI
- `/extension` - alias of /extensions for managing extensions | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/extensions` - manage CLI extensions; manage extensions, shown only when extensions are enabled | Agents: Gemini CLI, GitHub Copilot | Count: 2 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/fast` - turn a catalog-provided Fast service tier on or off when available; toggle fast mode; switch to SWE-1.6 Fast; ... | Agents: ChatGPT, Claude Code, Devin, OpenAI Codex | Count: 4 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/feedback` - open the feedback dialog to submit feedback and optionally include logs... | Agents: ChatGPT, Claude Code, Cursor, Devin, GitHub Copilot, Google Antigravity, OpenAI Codex | Count: 7 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/fewer-permission-prompts` - bundled skill to reduce permission prompts | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/find` - alias of /search | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/fix` - propose a fix for problems in selected code; fix errors in selected code | Agents: Cursor, GitHub Copilot | Count: 2 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/fixtestfailure` - find and fix a failing test | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/fleet` - launch multiple agents in parallel for one task | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/focus` - toggle focus/fullscreen rendering | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/footer` - alias of /statusline for toggling the terminal footer; configure footer status-line items | Agents: Gemini CLI, GitHub Copilot | Count: 2 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/fork` - copy a local chat into a new local chat or worktree... | Agents: ChatGPT, Claude Code, Cline, Cursor, Devin, GitHub Copilot, Google Antigravity, OpenAI Codex, OpenCode | Count: 9 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/fusion` - choose a Fusion model | Agents: Devin | Count: 1 | Meaning: same | Spellings: same | Differences: only in Devin
- `/gemma` - check local Gemma model routing status | Agents: Gemini CLI | Count: 1 | Meaning: same | Spellings: same | Differences: only in Gemini CLI
- `/generative_ui` - build interactive widgets as HTML artifacts or inline in the conversation | Agents: Google Antigravity | Count: 1 | Meaning: same | Spellings: same | Differences: only in Google Antigravity
- `/goal` - set a persistent goal for ChatGPT to work toward; set or clear a goal for the session... | Agents: ChatGPT, Claude Code, Cursor, GitHub Copilot, Google Antigravity, OpenAI Codex | Count: 6 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/grill-me` - interview you one question at a time before starting work | Agents: Google Antigravity | Count: 1 | Meaning: same | Spellings: same | Differences: only in Google Antigravity
- `/handoff` - hand off the current task to a cloud Devin | Agents: Devin | Count: 1 | Meaning: same | Spellings: same | Differences: only in Devin
- `/heapdump` - capture a heap snapshot, hidden from the command menu | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/help` - list available commands; show available slash commands... | Agents: Claude Code, Cline, Cursor, Devin, Gemini CLI, GitHub Copilot, Google Antigravity, OpenAI Codex, OpenCode | Count: 9 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/highlights` - show release highlights again, shown only when highlights exist | Agents: OpenCode | Count: 1 | Meaning: same | Spellings: same | Differences: only in OpenCode
- `/history` - view session history | Agents: Cline, Gemini CLI | Count: 2 | Meaning: same | Spellings: same | Differences: none
- `/hooks` - view hook configuration for tool events; view hook configuration; view or manage lifecycle hooks; ... | Agents: Claude Code, Devin, Gemini CLI, GitHub Copilot, Google Antigravity, OpenAI Codex | Count: 6 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/ide` - manage IDE integration; connect the CLI session to the current VS Code workspace... | Agents: Claude Code, Gemini CLI, GitHub Copilot, OpenAI Codex | Count: 4 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/ide-context` - turn shared IDE context on or off; include IDE context in the next prompt (extension surface only) | Agents: ChatGPT, OpenAI Codex | Count: 2 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/import` - import settings and context from another agent; import setup, project files, or recent chats from Claude Code or Cursor | Agents: Claude Code, OpenAI Codex | Count: 2 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/inbox` - render an interactive inbox widget | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/init` - generate an AGENTS.md scaffold for the current project; explore the codebase and generate a starter CLAUDE.md... | Agents: ChatGPT, Claude Code, Gemini CLI, GitHub Copilot, OpenAI Codex, OpenCode | Count: 6 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/insights` - analyze usage patterns for cloud sessions | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/install-github-app` - set up the GitHub App for CI/CD workflows | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/install-slack-app` - install the Slack app | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/instructions` - view or edit custom instructions for the session | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/interactive` - switch to Interactive mode | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/ios` - alias of /mobile | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/jules` - delegate an asynchronous coding task to Jules and check task status | Agents: Google Jules | Count: 1 | Meaning: same | Spellings: same | Differences: only in Google Jules
- `/keep-alive` - prevent the machine from going to sleep during remote sessions | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/keybindings` - show keyboard shortcuts; open the interactive Keyboard Shortcut Editor | Agents: Claude Code, Google Antigravity | Count: 2 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/keymap` - remap TUI shortcuts | Agents: OpenAI Codex | Count: 1 | Meaning: same | Spellings: same | Differences: only in OpenAI Codex
- `/learn` - capture session corrections as persistent rules or skills | Agents: Google Antigravity | Count: 1 | Meaning: same | Spellings: same | Differences: only in Google Antigravity
- `/limits` - set or unset AI credit session limits | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/line-numbers` - toggle line numbers in code blocks | Agents: Cursor | Count: 1 | Meaning: same | Spellings: same | Differences: only in Cursor
- `/list-agents` - list agents in the agent team | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/list-dirs` - list directories in the active workspace | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/list-sessions` - list previous sessions | Agents: Devin | Count: 1 | Meaning: same | Spellings: same | Differences: only in Devin
- `/local` - run the chat in the selected local project; switch to local connection (extension surface only) | Agents: ChatGPT, OpenAI Codex | Count: 2 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/login` - authenticate or switch accounts; authenticate with the account; authenticate with GitHub | Agents: Claude Code, Devin, GitHub Copilot | Count: 3 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/login-status` - show login and authentication status | Agents: Devin | Count: 1 | Meaning: same | Spellings: same | Differences: only in Devin
- `/logout` - sign out; clear stored credentials and exit; sign out of GitHub Copilot CLI; ... | Agents: Claude Code, Devin, GitHub Copilot, Google Antigravity, OpenAI Codex | Count: 5 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/logs` - show debug log path and copy it | Agents: Cursor | Count: 1 | Meaning: same | Spellings: same | Differences: only in Cursor
- `/loop` - bundled skill to run a prompt on a schedule | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/ls` - list previous sessions | Agents: Devin | Count: 1 | Meaning: same | Spellings: same | Differences: only in Devin
- `/lsp` - manage the built-in LSP client | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/max-mode` - toggle Max Mode on legacy plans | Agents: Cursor | Count: 1 | Meaning: same | Spellings: same | Differences: only in Cursor
- `/mcp` - open MCP status to view connected servers; manage MCP server connections... | Agents: ChatGPT, Claude Code, Cline, Cursor, Gemini CLI, GitHub Copilot, Google Antigravity, OpenAI Codex, OpenCode | Count: 9 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/mcps` - list configured MCP servers in the TUI | Agents: OpenCode | Count: 1 | Meaning: same | Spellings: same | Differences: only in OpenCode
- `/memories` - configure whether the chat can use or generate memories when Memories is available; configure memory use and generation | Agents: ChatGPT, OpenAI Codex | Count: 2 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/memory` - view or edit CLAUDE.md files in scope; manage hierarchical memory loaded from GEMINI.md files | Agents: Claude Code, Gemini CLI | Count: 2 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/mention` - highlight and add a file to the chat | Agents: OpenAI Codex | Count: 1 | Meaning: same | Spellings: same | Differences: only in OpenAI Codex
- `/merge-to-parent` - merge a forked session back to its parent | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/mobile` - open the mobile app setup | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/mode` - show or switch permission mode | Agents: Devin | Count: 1 | Meaning: same | Spellings: same | Differences: only in Devin
- `/model` - choose the model for the current chat... | Agents: ChatGPT, Claude Code, Cline, Cursor, Devin, Gemini CLI, GitHub Copilot, Google Antigravity, OpenAI Codex, OpenCode, Windsurf (Cascade) | Count: 11 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/models` - alias of /model; open the model picker in the TUI | Agents: GitHub Copilot, OpenCode | Count: 2 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/mouse` - toggle mouse event capture in menus | Agents: Devin | Count: 1 | Meaning: same | Spellings: same | Differences: only in Devin
- `/new` - start a blank chat in the same local workspace when available; alias of /clear... | Agents: ChatGPT, Claude Code, Cursor, Devin, Gemini CLI, GitHub Copilot, Google Antigravity, OpenAI Codex, OpenCode | Count: 9 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/new-chat` - alias of /clear | Agents: Cursor | Count: 1 | Meaning: same | Spellings: same | Differences: only in Cursor
- `/newchat` - alias of /clear | Agents: Cursor | Count: 1 | Meaning: same | Spellings: same | Differences: only in Cursor
- `/newrule` - create a .clinerules file interactively, hidden until the prompt expansion is ported to the SDK runtime | Agents: Cline | Count: 1 | Meaning: same | Spellings: same | Differences: only in Cline
- `/newtask` - alias of /compact that starts a fresh task with distilled context | Agents: Cline | Count: 1 | Meaning: same | Spellings: same | Differences: only in Cline
- `/normal` - switch to Normal mode | Agents: Devin | Count: 1 | Meaning: same | Spellings: same | Differences: only in Devin
- `/oncall` - oncall helper, shown only in nightly builds and absent from docs | Agents: Gemini CLI | Count: 1 | Meaning: same | Spellings: same | Differences: only in Gemini CLI
- `/open` - open the current session in web or desktop; force the path to open inside the default system editor; open the repository Git root in Cursor; ... | Agents: Cursor, Devin, Google Antigravity, OpenCode | Count: 4 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/optimize` - analyze and improve running time of selected code | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/orchestrate` - coordinate work across sessions or repositories | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/org` - select the Devin organization | Agents: Devin | Count: 1 | Meaning: same | Spellings: same | Differences: only in Devin
- `/output-style` - change the output style | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/pair` - open the device-pairing dialog | Agents: OpenCode | Count: 1 | Meaning: same | Spellings: same | Differences: only in OpenCode
- `/passes` - show information about reasoning passes | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/peers` - alias of /list-agents | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/permissions` - view or change which tools require approval; show or change tool approval mode... | Agents: Claude Code, Gemini CLI, GitHub Copilot, Google Antigravity | Count: 4 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/pet` - wake or tuck away the desktop pet; alias of /pets | Agents: ChatGPT, OpenAI Codex | Count: 2 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/pets` - choose or hide the terminal pet | Agents: OpenAI Codex | Count: 1 | Meaning: same | Spellings: same | Differences: only in OpenAI Codex
- `/pickup` - pick up a handed-off cloud session | Agents: Devin | Count: 1 | Meaning: same | Spellings: same | Differences: only in Devin
- `/pin` - pin or unpin the current chat when available | Agents: ChatGPT | Count: 1 | Meaning: same | Spellings: same | Differences: only in ChatGPT
- `/plan` - toggle plan mode for multi-step planning; drop into Plan Mode... | Agents: ChatGPT, Claude Code, Cline, Cursor, Devin, Gemini CLI, GitHub Copilot, Google Antigravity, OpenAI Codex, Windsurf (Cascade) | Count: 10 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/platform` - show platform information for cloud session | Agents: Devin | Count: 1 | Meaning: same | Spellings: same | Differences: only in Devin
- `/plugin` - manage plugins; manage plugins and marketplace; open the interactive Plugins Manager or run inline plugin commands; ... | Agents: Claude Code, Cursor, GitHub Copilot, Google Antigravity | Count: 4 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/plugin-authoring` - bundled skill to write a mod or built-in plugin | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/plugins` - alias of /plugin; manage plugins | Agents: Cline, Google Antigravity, OpenAI Codex | Count: 3 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/policies` - manage policies | Agents: Gemini CLI | Count: 1 | Meaning: same | Spellings: same | Differences: only in Gemini CLI
- `/powerup` - show available powerups | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/pr` - manage pull requests | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/pr-comments` - work with PR comments | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/pr-fix-checks` - address failing checks on an open pull request | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/pr-merge` - merge an open pull request | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/pr-open` - open a pull request | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/pr-resolve-comments` - resolve comments on a pull request | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/presets` - run or save reusable prompts and slash commands | Agents: OpenAI Codex | Count: 1 | Meaning: same | Spellings: same | Differences: only in OpenAI Codex
- `/privacy` - display the privacy notice | Agents: Gemini CLI | Count: 1 | Meaning: same | Spellings: same | Differences: only in Gemini CLI
- `/privacy-settings` - open privacy settings | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/proactive` - alias of /loop | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/profile` - profile helper, shown only in development builds and absent from docs | Agents: Gemini CLI | Count: 1 | Meaning: same | Spellings: same | Differences: only in Gemini CLI
- `/project` - choose a project for new chats; project-related command (extension surface only); alias of /open for projects | Agents: ChatGPT, OpenAI Codex, OpenCode | Count: 3 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/projects` - alias of /open for projects | Agents: OpenCode | Count: 1 | Meaning: same | Spellings: same | Differences: only in OpenCode
- `/ps` - list background terminals | Agents: OpenAI Codex | Count: 1 | Meaning: same | Spellings: same | Differences: only in OpenAI Codex
- `/pwd` - show the current working directory | Agents: OpenAI Codex | Count: 1 | Meaning: same | Spellings: same | Differences: only in OpenAI Codex
- `/q` - alias of /exit | Agents: OpenCode | Count: 1 | Meaning: same | Spellings: same | Differences: only in OpenCode
- `/quit` - alias of /exit; alias of /exit for closing the interactive CLI... | Agents: Claude Code, Cline, Cursor, Devin, Gemini CLI, GitHub Copilot, Google Antigravity, OpenAI Codex, OpenCode | Count: 9 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/quota` - alias of /usage | Agents: Google Antigravity | Count: 1 | Meaning: same | Spellings: same | Differences: only in Google Antigravity
- `/radio` - open the radio feature | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/rate-limit-options` - show options when rate limited | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/raw` - toggle raw scrollback mode for copy-friendly terminal selection | Agents: OpenAI Codex | Count: 1 | Meaning: same | Spellings: same | Differences: only in OpenAI Codex
- `/rc` - alias of /remote-control | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/reasoning` - choose the reasoning effort for the current chat; open the reasoning effort picker (extension surface only) | Agents: ChatGPT, OpenAI Codex | Count: 2 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/recap` - recap the current session; summarize the current conversation now | Agents: Claude Code, Devin, OpenAI Codex | Count: 3 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/record` - alias of /voice for dictation/recording | Agents: Google Antigravity | Count: 1 | Meaning: same | Spellings: same | Differences: only in Google Antigravity
- `/redo` - restore a message and file changes after /undo | Agents: OpenCode | Count: 1 | Meaning: same | Spellings: same | Differences: only in OpenCode
- `/refactor` - suggest refactoring for selected code | Agents: Cursor | Count: 1 | Meaning: same | Spellings: same | Differences: only in Cursor
- `/refine` - refine the last prompt or selected text | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/release-notes` - show the latest release notes; alias of /changelog | Agents: Claude Code, GitHub Copilot | Count: 2 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/reload` - reload configuration without restarting | Agents: OpenCode | Count: 1 | Meaning: same | Spellings: same | Differences: only in OpenCode
- `/reload-plugins` - reload plugins after changes | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/reload-skills` - reload skills after changes | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/remote` - enable or manage remote control of the CLI session | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/remote-control` - manage remote-control sessions; remote control toggle, available through /remote; toggle remote control of the CLI session | Agents: Claude Code, GitHub Copilot, Google Antigravity | Count: 3 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/remote-env` - manage cloud environments | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/remove-dir` - alias of /undo-add-dir | Agents: Devin | Count: 1 | Meaning: same | Spellings: same | Differences: only in Devin
- `/rename` - rename the current chat; rename the current session; rename the current session thread; ... | Agents: ChatGPT, Claude Code, Cursor, Devin, GitHub Copilot, Google Antigravity, OpenAI Codex | Count: 7 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/rename-session` - alias of /rename | Agents: Devin | Count: 1 | Meaning: same | Spellings: same | Differences: only in Devin
- `/repo` - open the repository in cloud session | Agents: Devin | Count: 1 | Meaning: same | Spellings: same | Differences: only in Devin
- `/reportbug` - report a bug with diagnostic info, hidden until the prompt expansion is ported to the SDK runtime | Agents: Cline | Count: 1 | Meaning: same | Spellings: same | Differences: only in Cline
- `/research` - research a topic with agents | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/reset` - alias of /clear | Agents: Claude Code, GitHub Copilot | Count: 2 | Meaning: same | Spellings: same | Differences: none
- `/reset-allowed-tools` - reset the allowed-tools list | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/restart` - restart Claude Code; restart the current session; restart the OpenCode service, shown only when client.restart is available | Agents: Claude Code, GitHub Copilot, OpenCode | Count: 3 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/restart-session` - restart the current app session | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/restore` - restore project files to a checkpoint, shown only when checkpointing is enabled | Agents: Gemini CLI | Count: 1 | Meaning: same | Spellings: same | Differences: only in Gemini CLI
- `/resume` - reopen a previous session; resume a previous session; open the conversation picker overlay; ... | Agents: Claude Code, Cursor, Gemini CLI, GitHub Copilot, Google Antigravity, OpenCode | Count: 6 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/revert` - revert to a previous step | Agents: Devin | Count: 1 | Meaning: same | Spellings: same | Differences: only in Devin
- `/review` - start code review mode to review uncommitted changes or compare against a base branch; alias of /code-review... | Agents: ChatGPT, Claude Code, GitHub Copilot, OpenAI Codex, OpenCode | Count: 5 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/rewind` - roll back to an earlier checkpoint; alias of /undo for rewinding conversation history; go back in conversation history; ... | Agents: Claude Code, Cursor, Gemini CLI, GitHub Copilot, Google Antigravity | Count: 5 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/rm-session` - delete a session | Agents: Devin | Count: 1 | Meaning: same | Spellings: same | Differences: only in Devin
- `/rollout` - print the rollout file path, only visible in debug builds | Agents: OpenAI Codex | Count: 1 | Meaning: same | Spellings: same | Differences: only in OpenAI Codex
- `/routines` - alias of /schedule | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/rubber-duck` - get a second opinion from the rubber duck agent | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/run` - bundled skill to run and verify the app; alias of /shell | Agents: Claude Code, Cursor | Count: 2 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/run-everything` - toggle Run Everything mode | Agents: Cursor | Count: 1 | Meaning: same | Spellings: same | Differences: only in Cursor
- `/run-skill-generator` - bundled skill to generate a skill | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/run-workflow` - write and run a Python script that orchestrates many agents across parallel and sequential phases | Agents: Google Antigravity | Count: 1 | Meaning: same | Spellings: same | Differences: only in Google Antigravity
- `/sandbox` - toggle sandbox mode; manage sandbox settings; configure sandbox mode and network access | Agents: Claude Code, Cursor, GitHub Copilot | Count: 3 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/schedule` - schedule a recurring cloud task; schedule an instruction as a one-time timer or recurring cron job | Agents: Claude Code, Google Antigravity | Count: 2 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/scroll-speed` - set scroll speed for fullscreen rendering | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/search` - search the codebase or session history; alias of /codesearch | Agents: GitHub Copilot, Google Antigravity | Count: 2 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/security-review` - bundled skill for security review; run a security review | Agents: Claude Code, GitHub Copilot | Count: 2 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/session` - manage the current session | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/session rename` - alias of /rename for renaming the session | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/session-stats` - show session statistics | Agents: Devin | Count: 1 | Meaning: same | Spellings: same | Differences: only in Devin
- `/sessions` - alias of /session; list and switch between sessions | Agents: GitHub Copilot, OpenCode | Count: 2 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/settings` - alias of /config; change CLI settings; open the settings editor; ... | Agents: Claude Code, Cline, Gemini CLI, GitHub Copilot, Google Antigravity, OpenCode | Count: 6 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/setup-bedrock` - set up Amazon Bedrock, hidden until env var enabled | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/setup-default-sandbox` - set up the elevated Windows sandbox | Agents: OpenAI Codex | Count: 1 | Meaning: same | Spellings: same | Differences: only in OpenAI Codex
- `/setup-github` - set up GitHub Actions to triage issues and review PRs | Agents: Gemini CLI | Count: 1 | Meaning: same | Spellings: same | Differences: only in Gemini CLI
- `/setup-terminal` - configure terminal newline keybindings | Agents: Cursor | Count: 1 | Meaning: same | Spellings: same | Differences: only in Cursor
- `/setup-vertex` - set up Google Vertex AI, hidden until env var enabled | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/sh` - alias of /shell | Agents: Cursor | Count: 1 | Meaning: same | Spellings: same | Differences: only in Cursor
- `/share` - export or share the session; share the current session as a public link | Agents: GitHub Copilot, OpenCode | Count: 2 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/shell` - enter Shell Mode | Agents: Cursor | Count: 1 | Meaning: same | Spellings: same | Differences: only in Cursor
- `/shortcuts` - show interactive keyboard shortcuts; toggle the shortcuts panel above the input | Agents: Devin, Gemini CLI | Count: 2 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/show-thinking` - toggle thinking block display | Agents: Cursor | Count: 1 | Meaning: same | Spellings: same | Differences: only in Cursor
- `/side` - start a temporary side chat without interrupting the main chat; start a side conversation | Agents: ChatGPT, OpenAI Codex | Count: 2 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/simplify` - alias of /code-review; simplify the current code selection | Agents: Claude Code, GitHub Copilot | Count: 2 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/skill-doctor` - bundled skill to diagnose skill problems | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/skills` - list skills available in the session; manage agent skills; open the skill picker or reload skills... | Agents: Claude Code, Cline, Gemini CLI, GitHub Copilot, Google Antigravity, OpenAI Codex, OpenCode | Count: 7 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/slides` - bundled skill to generate slide artifacts | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/smart` - switch to Smart mode or run a prompt in it | Agents: Devin | Count: 1 | Meaning: same | Spellings: same | Differences: only in Devin
- `/smol` - alias of /compact that compresses conversation history | Agents: Cline | Count: 1 | Meaning: same | Spellings: same | Differences: only in Cline
- `/spar` - start a sparring session with an agent | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/spawn` - spawn a background task | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/ssh` - connect to a cloud session via SSH | Agents: Devin | Count: 1 | Meaning: same | Spellings: same | Differences: only in Devin
- `/stats` - alias of /cost; alias of /session-stats; display session statistics | Agents: Claude Code, Devin, Gemini CLI | Count: 3 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/status` - show the chat ID, context usage, and rate limits; show account, model, directory, and version info; alias of /login-status; ... | Agents: ChatGPT, Claude Code, Devin, OpenAI Codex, OpenCode | Count: 5 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/status-indicators` - toggle terminal title status indicators | Agents: Cursor | Count: 1 | Meaning: same | Spellings: same | Differences: only in Cursor
- `/statusline` - configure the status line; toggle or configure the terminal status line; configure footer status-line items; ... | Agents: Claude Code, Gemini CLI, GitHub Copilot, OpenAI Codex | Count: 4 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/steps` - show the steps of the current session | Agents: Devin | Count: 1 | Meaning: same | Spellings: same | Differences: only in Devin
- `/stickers` - show stickers | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/stop` - stop a background session or peek reply; stop all background terminals | Agents: Claude Code, OpenAI Codex | Count: 2 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/subagents` - manage subagents; switch the active subagent thread | Agents: GitHub Copilot, OpenAI Codex | Count: 2 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/subtask` - hand a task to a forked subagent | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/summarize` - summarize the conversation to reduce context; alias of /compress; alias of /compact | Agents: Cursor, Gemini CLI, OpenCode | Count: 3 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/swarm` - run named workers and a verifier that coordinate on a shared message board | Agents: Google Antigravity | Count: 1 | Meaning: same | Spellings: same | Differences: only in Google Antigravity
- `/switch` - alias of /resume for switching conversations | Agents: Google Antigravity | Count: 1 | Meaning: same | Spellings: same | Differences: only in Google Antigravity
- `/tasks` - toggle the background tasks panel; open the background tasks dialog; toggle or view the tasks panel; ... | Agents: Claude Code, Gemini CLI, GitHub Copilot, Google Antigravity | Count: 4 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/team-onboarding` - run team onboarding flow | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/teamwork` - run collaborative multi-agent teams for repo-scale work | Agents: Google Antigravity | Count: 1 | Meaning: same | Spellings: same | Differences: only in Google Antigravity
- `/teleport` - move the current session to a cloud session | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/terminal` - run a terminal command in the app session; open a new terminal tab in the TUI | Agents: GitHub Copilot, OpenCode | Count: 2 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/terminal-setup` - install keybindings for newlines and clipboard; configure terminal keybindings for multiline input... | Agents: Claude Code, Gemini CLI, GitHub Copilot | Count: 3 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/test` - generate unit tests for selected code | Agents: Cursor | Count: 1 | Meaning: same | Spellings: same | Differences: only in Cursor
- `/test-approval` - test approval request, only visible in debug builds | Agents: OpenAI Codex | Count: 1 | Meaning: same | Spellings: same | Differences: only in OpenAI Codex
- `/tests` - generate unit tests for selected code | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/theme` - change the terminal theme; switch the terminal theme; change the terminal color theme; ... | Agents: Claude Code, Cline, Devin, Gemini CLI, GitHub Copilot, OpenAI Codex | Count: 6 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/themes` - open the theme picker | Agents: OpenCode | Count: 1 | Meaning: same | Spellings: same | Differences: only in OpenCode
- `/thinking` - alias of /variants that opens the model variant picker | Agents: OpenCode | Count: 1 | Meaning: same | Spellings: same | Differences: only in OpenCode
- `/title` - alias of /rename; configure terminal title items | Agents: Devin, Google Antigravity, OpenAI Codex | Count: 3 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/tools` - list available Gemini CLI tools | Agents: Gemini CLI | Count: 1 | Meaning: same | Spellings: same | Differences: only in Gemini CLI
- `/tp` - alias of /teleport | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/tui` - switch TUI renderer; choose the TUI mode for the next launch | Agents: Claude Code, OpenAI Codex | Count: 2 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/tuikit` - inspect or configure TUI kit components | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/ultraplan` - bundled dynamic workflow for extended planning in a cloud session | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/ultrareview` - bundled dynamic workflow for cloud review | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/undo` - alias of /rewind; rewind the conversation history; revert the last user message and any file changes; ... | Agents: Claude Code, Cline, GitHub Copilot, Google Antigravity, OpenCode | Count: 5 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/undo-add-dir` - remove a workspace directory | Agents: Devin | Count: 1 | Meaning: same | Spellings: same | Differences: only in Devin
- `/unshare` - stop sharing the current session | Agents: OpenCode | Count: 1 | Meaning: same | Spellings: same | Differences: only in OpenCode
- `/update` - check for and install updates; check for and install CLI updates; update Cursor Agent; ... | Agents: Claude Code, Cursor, Devin, GitHub Copilot, OpenCode | Count: 5 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/update-config` - bundled skill to update settings via hook | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/upgrade` - upgrade Claude Code; upgrade subscription plan; alias of /update; ... | Agents: Claude Code, Devin, Gemini CLI, GitHub Copilot | Count: 4 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/usage` - open usage and billing settings when available with ChatGPT sign-in; alias of /cost... | Agents: ChatGPT, Claude Code, Devin, Gemini CLI, GitHub Copilot, Google Antigravity, OpenAI Codex, OpenCode | Count: 8 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/usage-credits` - alias of /cost for usage credits | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/user` - show or switch the active GitHub user | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/variants` - open the model variant picker | Agents: OpenCode | Count: 1 | Meaning: same | Spellings: same | Differences: only in OpenCode
- `/verify` - bundled skill to run and verify the app | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/version` - show the CLI version | Agents: GitHub Copilot | Count: 1 | Meaning: same | Spellings: same | Differences: only in GitHub Copilot
- `/vim` - toggle Vim mode; toggle Vim keybindings in the TUI; toggle Vim keys; ... | Agents: Claude Code, Cursor, Gemini CLI, GitHub Copilot, OpenAI Codex | Count: 5 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/voice` - toggle voice dictation; toggle voice dictation mode; toggle voice dictation or live voice mode; ... | Agents: Claude Code, Gemini CLI, GitHub Copilot, Google Antigravity, OpenAI Codex | Count: 5 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/warnings` - show retained warnings and diagnostic details | Agents: OpenAI Codex | Count: 1 | Meaning: same | Spellings: same | Differences: only in OpenAI Codex
- `/web` - alias of /pair | Agents: OpenCode | Count: 1 | Meaning: same | Spellings: same | Differences: only in OpenCode
- `/web-setup` - set up cloud sessions | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/workflow-authoring` - bundled skill to author dynamic workflows | Agents: Claude Code | Count: 1 | Meaning: same | Spellings: same | Differences: only in Claude Code
- `/workflows` - list and manage dynamic workflows; list and manage workflows | Agents: Claude Code, GitHub Copilot | Count: 2 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/workspace` - list workspace directories | Agents: Devin | Count: 1 | Meaning: same | Spellings: same | Differences: only in Devin
- `/workspaces` - alias of /workspace | Agents: Devin | Count: 1 | Meaning: same | Spellings: same | Differences: only in Devin
- `/worktree` - run the chat in a new Git worktree; manage Git worktrees; continue the conversation in a new Git worktree | Agents: ChatGPT, GitHub Copilot, OpenAI Codex | Count: 3 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents
- `/worktrees` - open the workspace management dialog | Agents: OpenCode | Count: 1 | Meaning: same | Spellings: same | Differences: only in OpenCode
- `/yolo` - alias of /bypass; alias of /permissions allow-all or /autoApprove depending on surface | Agents: Devin, GitHub Copilot | Count: 2 | Meaning: differs | Spellings: same | Differences: purpose or surface differs across agents

## 3. Agent: ChatGPT

**Product facts**: OpenAI ChatGPT. Surfaces covered: chatgpt.com web, desktop apps (macOS and Windows), and mobile apps. Version checked: ChatGPT desktop slash-command reference and developer-commands page, accessed 2026-11-17. The vendor reference is for the ChatGPT desktop app composer; the chatgpt.com web composer and mobile apps use a separate `/` menu that is not publicly documented as a fixed slash-command list, so those surfaces are recorded in `Searched, not found`.

**Keywords**

- `/approve` - Kind: built-in; Surface: Desktop app; Args: none; Aliases: none; Purpose: approve one retry of a recent automatic-review denial when automatic review is active; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CGPT-SLSHCMDS
- `/archive` - Kind: built-in; Surface: Desktop app; Args: none; Aliases: none; Purpose: archive the current chat; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CGPT-SLSHCMDS
- `/chat` - Kind: built-in; Surface: Desktop app; Args: none; Aliases: none; Purpose: choose a chat without a project before starting a new chat; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CGPT-SLSHCMDS
- `/cloud` - Kind: built-in; Surface: Desktop app; Args: none; Aliases: none; Purpose: run the chat in the cloud when cloud execution is available; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CGPT-SLSHCMDS
- `/cloud-environment` - Kind: built-in; Surface: Desktop app; Args: none; Aliases: none; Purpose: choose the cloud environment for the chat; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CGPT-SLSHCMDS
- `/compact` - Kind: built-in; Surface: Desktop app; Args: none; Aliases: none; Purpose: compact the current chat's context; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CGPT-SLSHCMDS
- `/fast` - Kind: built-in; Surface: Desktop app; Args: none; Aliases: none; Purpose: turn a catalog-provided Fast service tier on or off when available; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CGPT-SLSHCMDS
- `/feedback` - Kind: built-in; Surface: Desktop app; Args: none; Aliases: none; Purpose: open the feedback dialog to submit feedback and optionally include logs; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CGPT-SLSHCMDS
- `/fork` - Kind: built-in; Surface: Desktop app; Args: none; Aliases: none; Purpose: copy a local chat into a new local chat or worktree; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CGPT-SLSHCMDS
- `/goal` - Kind: built-in; Surface: Desktop app; Args: objective; Aliases: none; Purpose: set a persistent goal for ChatGPT to work toward; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CGPT-SLSHCMDS
- `/ide-context` - Kind: built-in; Surface: Desktop app; Args: none; Aliases: none; Purpose: turn shared IDE context on or off; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CGPT-SLSHCMDS
- `/init` - Kind: built-in; Surface: Desktop app; Args: none; Aliases: none; Purpose: generate an AGENTS.md scaffold for the current project; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CGPT-SLSHCMDS
- `/local` - Kind: built-in; Surface: Desktop app; Args: none; Aliases: none; Purpose: run the chat in the selected local project; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CGPT-SLSHCMDS
- `/mcp` - Kind: built-in; Surface: Desktop app; Args: none; Aliases: none; Purpose: open MCP status to view connected servers; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CGPT-SLSHCMDS
- `/memories` - Kind: built-in; Surface: Desktop app; Args: none; Aliases: none; Purpose: configure whether the chat can use or generate memories when Memories is available; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CGPT-SLSHCMDS
- `/model` - Kind: built-in; Surface: Desktop app; Args: none; Aliases: none; Purpose: choose the model for the current chat; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CGPT-SLSHCMDS
- `/new` - Kind: built-in; Surface: Desktop app; Args: none; Aliases: none; Purpose: start a blank chat in the same local workspace when available; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CGPT-SLSHCMDS
- `/pet` - Kind: built-in; Surface: Desktop app; Args: none; Aliases: none; Purpose: wake or tuck away the desktop pet; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CGPT-SLSHCMDS
- `/pin` - Kind: built-in; Surface: Desktop app; Args: none; Aliases: none; Purpose: pin or unpin the current chat when available; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CGPT-SLSHCMDS
- `/plan` - Kind: built-in; Surface: Desktop app; Args: none; Aliases: none; Purpose: toggle plan mode for multi-step planning; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CGPT-SLSHCMDS
- `/project` - Kind: built-in; Surface: Desktop app; Args: none; Aliases: none; Purpose: choose a project for new chats; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CGPT-SLSHCMDS
- `/reasoning` - Kind: built-in; Surface: Desktop app; Args: none; Aliases: none; Purpose: choose the reasoning effort for the current chat; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CGPT-SLSHCMDS
- `/rename` - Kind: built-in; Surface: Desktop app; Args: name; Aliases: none; Purpose: rename the current chat; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CGPT-SLSHCMDS
- `/review` - Kind: built-in; Surface: Desktop app; Args: none; Aliases: none; Purpose: start code review mode to review uncommitted changes or compare against a base branch; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CGPT-SLSHCMDS
- `/side` - Kind: built-in; Surface: Desktop app; Args: none; Aliases: none; Purpose: start a temporary side chat without interrupting the main chat; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CGPT-SLSHCMDS
- `/status` - Kind: built-in; Surface: Desktop app; Args: none; Aliases: none; Purpose: show the chat ID, context usage, and rate limits; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CGPT-SLSHCMDS
- `/usage` - Kind: built-in; Surface: Desktop app; Args: none; Aliases: none; Purpose: open usage and billing settings when available with ChatGPT sign-in; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CGPT-SLSHCMDS
- `/worktree` - Kind: built-in; Surface: Desktop app; Args: none; Aliases: none; Purpose: run the chat in a new Git worktree; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CGPT-SLSHCMDS

**Collision rule**: The desktop app composer resolves `/` by exact match against built-in commands, enabled skills, and custom prompts; a built-in command name wins over a user-defined prompt or skill of the same name.

**Searched, not found**

- Searched `https://learn.chatgpt.com/docs/reference/slash-commands` for the complete desktop app slash-command catalog; recorded all listed built-in commands.
- Searched `https://learn.chatgpt.com/docs/developer-commands` for ChatGPT web composer commands; the page states that ChatGPT web has its own composer command menu and does not expose the desktop or CLI command set, but no enumerated web slash-command list was found.
- Searched `https://help.openai.com/en/articles/9703738-chatgpt-macos-app-release-notes` for additional slash commands; only the initial November 2024 announcement of slash commands was found, no new commands.
- Searched web for `site:openai.com chatgpt mobile app slash commands` and `chatgpt.com web slash commands`; no vendor-published inventory for web or mobile surfaces.

**Status**: COMPLETE 2026-11-17

## 4. Agent: Claude Code

**Product facts**: Anthropic Claude Code. Surfaces covered: CLI, VS Code/JetBrains extensions, Claude Desktop Code tab, and web app. Latest documented version checked: v2.1.326 (2026-11-16). Accessed 2026-11-17. No local Claude Code CLI installation was found on this machine; only the Claude Desktop consumer app is present under `C:\Users\User\AppData\Local\AnthropicClaude\`. CLI behavior is documented from the vendor command reference and changelog; no `[TESTED]` labels are applied to CLI-only commands.

**Keywords**

- `/add-dir` - Kind: built-in; Surface: CLI, Desktop, IDE; Args: path; Aliases: none; Purpose: grant Claude access to an additional directory for the session; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF, SLASHCMDS-IN01-SC-CLCD-CHTSH
- `/advisor` - Kind: built-in; Surface: CLI; Args: model or off; Aliases: none; Purpose: enable or disable the advisor tool; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/agents` - Kind: built-in; Surface: CLI, Desktop, IDE; Args: none; Aliases: none; Purpose: list, create, or edit subagents; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF, SLASHCMDS-IN01-SC-CLCD-CHTSH
- `/android` - Kind: alias; Surface: CLI; Args: none; Aliases: /mobile; Purpose: alias of /mobile; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/app` - Kind: alias; Surface: CLI; Args: none; Aliases: /desktop; Purpose: alias of /desktop; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/artifact-capabilities` - Kind: bundled; Surface: CLI; Args: none; Aliases: none; Purpose: bundled skill for artifact capabilities; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/artifact-diagramming` - Kind: bundled; Surface: CLI; Args: none; Aliases: none; Purpose: bundled skill for artifact diagramming guidance; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/artifacts` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: list owned or shared artifacts and attach, open, or copy one; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/auto-mode-setup` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: draft autoMode.environment entries from the project and recent sessions; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/autocompact` - Kind: built-in; Surface: CLI; Args: auto or token count; Aliases: none; Purpose: set the auto-compact window size; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/autofix-pr` - Kind: bundled; Surface: CLI; Args: optional prompt; Aliases: none; Purpose: spawn a cloud session that watches the current PR and pushes fixes; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/background` - Kind: built-in; Surface: CLI; Args: optional prompt; Aliases: /bg; Purpose: detach the session to run as a background agent; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/bashes` - Kind: alias; Surface: CLI; Args: none; Aliases: /tasks; Purpose: alias of /tasks; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/batch` - Kind: bundled; Surface: CLI; Args: instruction; Aliases: none; Purpose: orchestrate large-scale changes across a codebase in parallel; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/bg` - Kind: alias; Surface: CLI; Args: none; Aliases: /background; Purpose: alias of /background; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/branch` - Kind: built-in; Surface: CLI; Args: optional name; Aliases: none; Purpose: create a conversation branch to try a different direction; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/btw` - Kind: built-in; Surface: CLI; Args: question; Aliases: none; Purpose: ask a side question without adding it to the conversation; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF, SLASHCMDS-IN01-SC-CLCD-CHTSH
- `/bug` - Kind: built-in; Surface: CLI, Desktop, IDE; Args: optional report; Aliases: /feedback; Purpose: report a bug or share the conversation; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF, SLASHCMDS-IN01-SC-CLCD-CHTSH
- `/cd` - Kind: built-in; Surface: CLI; Args: path; Aliases: none; Purpose: change the session working directory; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/checkpoint` - Kind: alias; Surface: CLI; Args: none; Aliases: /rewind; Purpose: alias of /rewind; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/checkup` - Kind: alias; Surface: CLI; Args: none; Aliases: /doctor; Purpose: alias of /doctor; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/chrome` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: launch or manage Claude in Chrome; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/claude-api` - Kind: bundled; Surface: CLI; Args: migrate, upgrade, api-version, managed-agents subcommands; Aliases: none; Purpose: bundled skill for Claude API projects; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/claude-in-chrome` - Kind: bundled; Surface: CLI; Args: optional task; Aliases: none; Purpose: bundled skill for Claude in Chrome tasks; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/clear` - Kind: built-in; Surface: CLI, Desktop, IDE; Args: optional name; Aliases: /reset, /new; Purpose: wipe conversation history and start fresh; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF, SLASHCMDS-IN01-SC-CLCD-CHTSH
- `/code-review` - Kind: bundled; Surface: CLI; Args: level, --fix, --comment, --max-findings, pr/branch/path; Aliases: /review, /simplify; Purpose: bundled skill for local or cloud code review; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/color` - Kind: built-in; Surface: CLI; Args: color or default; Aliases: none; Purpose: set the remote-control prompt color; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/compact` - Kind: built-in; Surface: CLI, Desktop, IDE; Args: optional instructions; Aliases: none; Purpose: summarize the conversation to free context; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF, SLASHCMDS-IN01-SC-CLCD-CHTSH
- `/config` - Kind: built-in; Surface: CLI; Args: key=value pairs or --help; Aliases: /settings; Purpose: change settings; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF, SLASHCMDS-IN01-SC-CLCD-CHTSH
- `/context` - Kind: built-in; Surface: CLI; Args: all; Aliases: none; Purpose: visualize what is loaded into the context window; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF, SLASHCMDS-IN01-SC-CLCD-CHTSH
- `/continue` - Kind: alias; Surface: CLI; Args: none; Aliases: /resume; Purpose: alias of /resume; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/copy` - Kind: built-in; Surface: CLI; Args: optional N; Aliases: none; Purpose: copy the last response or selected code block; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/cost` - Kind: built-in; Surface: CLI; Args: none; Aliases: /usage, /stats; Purpose: show token usage and spend for the session; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF, SLASHCMDS-IN01-SC-CLCD-CHTSH
- `/dataviz` - Kind: bundled; Surface: CLI; Args: request; Aliases: none; Purpose: bundled skill for data visualization; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/debug` - Kind: bundled; Surface: CLI; Args: optional description; Aliases: none; Purpose: bundled skill to debug issues; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/deep-research` - Kind: bundled; Surface: CLI; Args: question; Aliases: none; Purpose: bundled dynamic workflow for deep research; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/design` - Kind: bundled; Surface: CLI; Args: brief, consent, revoke; Aliases: none; Purpose: bundled skill for UI/UX design artifacts; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/design-login` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: log in to standalone Claude Design; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/design-sync` - Kind: bundled; Surface: CLI; Args: optional hint; Aliases: none; Purpose: bundled skill to sync design system components; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/desktop` - Kind: built-in; Surface: CLI; Args: none; Aliases: /app; Purpose: open the current session in Claude Desktop; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/diff` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: open interactive diff of uncommitted changes; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF, SLASHCMDS-IN01-SC-CLCD-CHTSH
- `/doctor` - Kind: bundled; Surface: CLI; Args: optional prompt-audit or path; Aliases: /checkup; Purpose: bundled skill to diagnose install and environment issues; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF, SLASHCMDS-IN01-SC-CLCD-CHTSH
- `/effort` - Kind: built-in; Surface: CLI; Args: level, auto, status, ultracode on/off; Aliases: none; Purpose: set model effort level or toggle ultracode; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/exit` - Kind: built-in; Surface: CLI; Args: none; Aliases: /quit; Purpose: quit the CLI; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/export` - Kind: built-in; Surface: CLI; Args: optional filename; Aliases: none; Purpose: save the conversation to a file or clipboard; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/fast` - Kind: built-in; Surface: CLI; Args: on or off; Aliases: none; Purpose: toggle fast mode; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/feedback` - Kind: built-in; Surface: CLI; Args: optional report; Aliases: /bug; Purpose: report an issue or share feedback; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/fewer-permission-prompts` - Kind: bundled; Surface: CLI; Args: none; Aliases: none; Purpose: bundled skill to reduce permission prompts; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/focus` - Kind: built-in; Surface: CLI; Args: on or off; Aliases: none; Purpose: toggle focus/fullscreen rendering; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/fork` - Kind: built-in; Surface: CLI; Args: optional prompt; Aliases: none; Purpose: copy the current conversation into a new session; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/goal` - Kind: built-in; Surface: CLI; Args: condition or clear; Aliases: none; Purpose: set or clear a goal for the session; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/heapdump` - Kind: hidden; Surface: CLI; Args: none; Aliases: none; Purpose: capture a heap snapshot, hidden from the command menu; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/help` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: list available commands; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF, SLASHCMDS-IN01-SC-CLCD-CHTSH
- `/hooks` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: view hook configuration for tool events; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF, SLASHCMDS-IN01-SC-CLCD-CHTSH
- `/ide` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: manage IDE integration; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/import` - Kind: built-in; Surface: CLI; Args: codex, gemini, cursor with --dry-run, --yes; Aliases: none; Purpose: import settings and context from another agent; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/init` - Kind: built-in; Surface: CLI, Desktop, IDE; Args: none; Aliases: none; Purpose: explore the codebase and generate a starter CLAUDE.md; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF, SLASHCMDS-IN01-SC-CLCD-CHTSH
- `/insights` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: analyze usage patterns for cloud sessions; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/install-github-app` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: set up the GitHub App for CI/CD workflows; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/install-slack-app` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: install the Slack app; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/ios` - Kind: alias; Surface: CLI; Args: none; Aliases: /mobile; Purpose: alias of /mobile; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/keybindings` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: show keyboard shortcuts; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/list-agents` - Kind: built-in; Surface: CLI; Args: none; Aliases: /peers; Purpose: list agents in the agent team; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/login` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: authenticate or switch accounts; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/logout` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: sign out; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/loop` - Kind: bundled; Surface: CLI; Args: interval and prompt; Aliases: /proactive; Purpose: bundled skill to run a prompt on a schedule; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/mcp` - Kind: built-in; Surface: CLI; Args: reconnect, enable, disable subcommands; Aliases: none; Purpose: manage MCP server connections; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF, SLASHCMDS-IN01-SC-CLCD-CHTSH
- `/memory` - Kind: built-in; Surface: CLI, Desktop, IDE; Args: none; Aliases: none; Purpose: view or edit CLAUDE.md files in scope; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF, SLASHCMDS-IN01-SC-CLCD-CHTSH
- `/mobile` - Kind: built-in; Surface: CLI; Args: none; Aliases: /ios, /android; Purpose: open the mobile app setup; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/model` - Kind: built-in; Surface: CLI, Desktop, IDE; Args: optional model; Aliases: none; Purpose: view or switch the active model; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF, SLASHCMDS-IN01-SC-CLCD-CHTSH
- `/new` - Kind: alias; Surface: CLI; Args: none; Aliases: /clear; Purpose: alias of /clear; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/output-style` - Kind: built-in; Surface: CLI; Args: style; Aliases: none; Purpose: change the output style; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/passes` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: show information about reasoning passes; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/peers` - Kind: alias; Surface: CLI; Args: none; Aliases: /list-agents; Purpose: alias of /list-agents; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/permissions` - Kind: built-in; Surface: CLI, Desktop, IDE; Args: none; Aliases: none; Purpose: view or change which tools require approval; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF, SLASHCMDS-IN01-SC-CLCD-CHTSH
- `/plan` - Kind: built-in; Surface: CLI, Desktop, IDE; Args: optional description; Aliases: none; Purpose: drop into Plan Mode; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF, SLASHCMDS-IN01-SC-CLCD-CHTSH
- `/plugin` - Kind: built-in; Surface: CLI; Args: list, install, enable, disable subcommands; Aliases: none; Purpose: manage plugins; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/plugin-authoring` - Kind: bundled; Surface: CLI; Args: none; Aliases: none; Purpose: bundled skill to write a mod or built-in plugin; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/powerup` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: show available powerups; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/pr-comments` - Kind: built-in; Surface: CLI; Args: optional PR; Aliases: none; Purpose: work with PR comments; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/privacy-settings` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: open privacy settings; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/proactive` - Kind: alias; Surface: CLI; Args: none; Aliases: /loop; Purpose: alias of /loop; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/quit` - Kind: alias; Surface: CLI; Args: none; Aliases: /exit; Purpose: alias of /exit; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/radio` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: open the radio feature; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/rate-limit-options` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: show options when rate limited; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/rc` - Kind: alias; Surface: CLI; Args: none; Aliases: /remote-control; Purpose: alias of /remote-control; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/recap` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: recap the current session; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/release-notes` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: show the latest release notes; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/reload-plugins` - Kind: built-in; Surface: CLI; Args: --force; Aliases: none; Purpose: reload plugins after changes; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/reload-skills` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: reload skills after changes; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/remote-control` - Kind: built-in; Surface: CLI; Args: none; Aliases: /rc; Purpose: manage remote-control sessions; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/remote-env` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: manage cloud environments; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/rename` - Kind: built-in; Surface: CLI; Args: optional name; Aliases: none; Purpose: rename the current session; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/reset` - Kind: alias; Surface: CLI; Args: none; Aliases: /clear; Purpose: alias of /clear; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/restart` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: restart Claude Code; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/resume` - Kind: built-in; Surface: CLI; Args: optional session; Aliases: /continue; Purpose: reopen a previous session; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF, SLASHCMDS-IN01-SC-CLCD-CHTSH
- `/review` - Kind: alias; Surface: CLI; Args: none; Aliases: /code-review; Purpose: alias of /code-review; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/rewind` - Kind: built-in; Surface: CLI; Args: none; Aliases: /checkpoint, /undo; Purpose: roll back to an earlier checkpoint; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF, SLASHCMDS-IN01-SC-CLCD-CHTSH
- `/routines` - Kind: alias; Surface: CLI; Args: none; Aliases: /schedule; Purpose: alias of /schedule; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/run` - Kind: bundled; Surface: CLI; Args: none; Aliases: none; Purpose: bundled skill to run and verify the app; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/run-skill-generator` - Kind: bundled; Surface: CLI; Args: none; Aliases: none; Purpose: bundled skill to generate a skill; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/sandbox` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: toggle sandbox mode; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/schedule` - Kind: built-in; Surface: CLI; Args: optional description; Aliases: /routines; Purpose: schedule a recurring cloud task; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/scroll-speed` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: set scroll speed for fullscreen rendering; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/security-review` - Kind: bundled; Surface: CLI; Args: none; Aliases: none; Purpose: bundled skill for security review; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/settings` - Kind: alias; Surface: CLI; Args: none; Aliases: /config; Purpose: alias of /config; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/setup-bedrock` - Kind: hidden; Surface: CLI; Args: none; Aliases: none; Purpose: set up Amazon Bedrock, hidden until env var enabled; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/setup-vertex` - Kind: hidden; Surface: CLI; Args: none; Aliases: none; Purpose: set up Google Vertex AI, hidden until env var enabled; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/simplify` - Kind: alias; Surface: CLI; Args: none; Aliases: /code-review; Purpose: alias of /code-review; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/skill-doctor` - Kind: bundled; Surface: CLI; Args: none; Aliases: none; Purpose: bundled skill to diagnose skill problems; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/skills` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: list skills available in the session; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF, SLASHCMDS-IN01-SC-CLCD-CHTSH
- `/slides` - Kind: bundled; Surface: CLI; Args: optional brief; Aliases: none; Purpose: bundled skill to generate slide artifacts; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/stats` - Kind: alias; Surface: CLI; Args: none; Aliases: /cost; Purpose: alias of /cost; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/status` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: show account, model, directory, and version info; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF, SLASHCMDS-IN01-SC-CLCD-CHTSH
- `/statusline` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: configure the status line; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/stickers` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: show stickers; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/stop` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: stop a background session or peek reply; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/subtask` - Kind: built-in; Surface: CLI; Args: task; Aliases: none; Purpose: hand a task to a forked subagent; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/tasks` - Kind: built-in; Surface: CLI; Args: none; Aliases: /bashes; Purpose: toggle the background tasks panel; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/team-onboarding` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: run team onboarding flow; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/teleport` - Kind: built-in; Surface: CLI; Args: none; Aliases: /tp; Purpose: move the current session to a cloud session; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/terminal-setup` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: install keybindings for newlines and clipboard; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/theme` - Kind: built-in; Surface: CLI; Args: auto or theme name; Aliases: none; Purpose: change the terminal theme; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/tp` - Kind: alias; Surface: CLI; Args: none; Aliases: /teleport; Purpose: alias of /teleport; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/tui` - Kind: built-in; Surface: CLI; Args: default or fullscreen; Aliases: none; Purpose: switch TUI renderer; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/ultraplan` - Kind: bundled; Surface: CLI; Args: prompt; Aliases: none; Purpose: bundled dynamic workflow for extended planning in a cloud session; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/ultrareview` - Kind: bundled; Surface: CLI; Args: optional PR or branch; Aliases: none; Purpose: bundled dynamic workflow for cloud review; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/undo` - Kind: alias; Surface: CLI; Args: none; Aliases: /rewind; Purpose: alias of /rewind; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/update` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: check for and install updates; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/update-config` - Kind: bundled; Surface: CLI; Args: request; Aliases: none; Purpose: bundled skill to update settings via hook; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/upgrade` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: upgrade Claude Code; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/usage` - Kind: alias; Surface: CLI; Args: none; Aliases: /cost; Purpose: alias of /cost; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/usage-credits` - Kind: alias; Surface: CLI; Args: none; Aliases: /cost; Purpose: alias of /cost for usage credits; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/verify` - Kind: bundled; Surface: CLI; Args: none; Aliases: none; Purpose: bundled skill to run and verify the app; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/vim` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: toggle Vim mode; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/voice` - Kind: built-in; Surface: CLI; Args: hold, tap, or off; Aliases: none; Purpose: toggle voice dictation; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/web-setup` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: set up cloud sessions; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/workflow-authoring` - Kind: bundled; Surface: CLI; Args: none; Aliases: none; Purpose: bundled skill to author dynamic workflows; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF
- `/workflows` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: list and manage dynamic workflows; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLCD-CMDREF

**Collision rule**: Custom skills, plugins, and MCP prompts appear in the slash menu alongside built-ins. The menu resolves by exact and prefix match; if a custom name exactly matches a built-in, the built-in is highlighted first and Enter runs it, so built-ins win over custom commands.

**Searched, not found**

- Searched `https://code.claude.com/docs/en/commands` for every command block; the reference lists the built-in and bundled commands recorded above.
- Searched the local machine for a Claude Code CLI executable under `C:\Users\User\AppData\Local\AnthropicClaude\`, `npm` global, and PATH; none found, so CLI-only commands are not `[TESTED]`.
- Searched `docs/_INFO_HOW_CLAUDE_CODE_WORKS.md` in the workspace; the file does not exist, so no earlier notes conflict.

**Status**: COMPLETE 2026-11-17

## 5. Agent: Devin

**Product facts**: Cognition Devin agent. Surfaces covered: Devin CLI interactive sessions and Devin Desktop (Devin Local) IDE. Devin web app sessions use organization-defined custom slash commands only; no vendor-built-in slash commands are documented for the web chat. Version checked from docs: latest CLI release notes dated 2026-11-17. Devin Desktop `C:\Users\User\AppData\Local\Programs\Devin\Devin.exe` is installed but its source is minified; no additional built-in slash commands were extracted beyond the CLI reference.

**Keywords**

- `/accept-edits` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: switch to Accept Edits mode; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF, SLASHCMDS-IN01-SC-DEVIN-ESS
- `/add-dir` - Kind: built-in; Surface: CLI; Args: optional path; Aliases: none; Purpose: add an additional workspace directory; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF, SLASHCMDS-IN01-SC-DEVIN-ESS
- `/archive` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: archive a cloud session; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/ask` - Kind: built-in; Surface: CLI; Args: question; Aliases: none; Purpose: ask a one-shot question without making code changes; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF, SLASHCMDS-IN01-SC-DEVIN-ESS
- `/autonomous` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: switch to Autonomous mode, requires --sandbox; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/btw` - Kind: built-in; Surface: CLI; Args: prompt; Aliases: none; Purpose: open a side chat panel that runs in parallel with the main agent; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/bypass` - Kind: built-in; Surface: CLI; Args: optional prompt; Aliases: /yolo, /dangerous; Purpose: switch to Bypass mode; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF, SLASHCMDS-IN01-SC-DEVIN-ESS
- `/clear` - Kind: built-in; Surface: CLI; Args: none; Aliases: /new; Purpose: clear conversation history and start fresh; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF, SLASHCMDS-IN01-SC-DEVIN-ESS
- `/cloud` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: manage cloud sessions; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/code` - Kind: built-in; Surface: CLI; Args: optional prompt; Aliases: none; Purpose: switch to Code mode or run a prompt in it; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/compact` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: force conversation compaction; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/confetti` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: celebrate with confetti; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/config` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: open interactive config editor; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/context` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: show context window usage; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/continue` - Kind: built-in; Surface: CLI; Args: optional session-id; Aliases: none; Purpose: continue a previous session; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/copy` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: copy the last response to clipboard; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/dangerous` - Kind: alias; Surface: CLI; Args: none; Aliases: /bypass; Purpose: alias of /bypass; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/exit` - Kind: built-in; Surface: CLI; Args: none; Aliases: /quit; Purpose: exit the CLI; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF, SLASHCMDS-IN01-SC-DEVIN-ESS
- `/fast` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: switch to SWE-1.6 Fast; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/feedback` - Kind: built-in; Surface: CLI; Args: up or down; Aliases: none; Purpose: rate the last response; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/fork` - Kind: built-in; Surface: CLI; Args: optional step; Aliases: none; Purpose: fork the current conversation at a step; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/fusion` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: choose a Fusion model; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/handoff` - Kind: built-in; Surface: CLI; Args: optional task; Aliases: none; Purpose: hand off the current task to a cloud Devin; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/help` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: show available slash commands; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF, SLASHCMDS-IN01-SC-DEVIN-ESS
- `/hooks` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: view hook configuration; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/list-sessions` - Kind: built-in; Surface: CLI; Args: none; Aliases: /ls; Purpose: list previous sessions; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/login` - Kind: built-in; Surface: CLI; Args: optional api-key; Aliases: none; Purpose: authenticate with the account; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/login-status` - Kind: built-in; Surface: CLI; Args: none; Aliases: /status; Purpose: show login and authentication status; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/logout` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: clear stored credentials and exit; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/ls` - Kind: built-in; Surface: CLI; Args: --all; Aliases: /list-sessions; Purpose: list previous sessions; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/mode` - Kind: built-in; Surface: CLI; Args: normal, accept-edits, smart, plan, bypass, autonomous; Aliases: none; Purpose: show or switch permission mode; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF, SLASHCMDS-IN01-SC-DEVIN-ESS
- `/model` - Kind: built-in; Surface: CLI; Args: optional name; Aliases: none; Purpose: show or change the current model; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/mouse` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: toggle mouse event capture in menus; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/new` - Kind: alias; Surface: CLI; Args: none; Aliases: /clear; Purpose: alias of /clear; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/normal` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: switch to Normal mode; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF, SLASHCMDS-IN01-SC-DEVIN-ESS
- `/open` - Kind: built-in; Surface: CLI; Args: web or desktop; Aliases: none; Purpose: open the current session in web or desktop; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/org` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: select the Devin organization; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/pickup` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: pick up a handed-off cloud session; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/plan` - Kind: built-in; Surface: CLI; Args: optional prompt; Aliases: none; Purpose: switch to Plan mode; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF, SLASHCMDS-IN01-SC-DEVIN-ESS
- `/platform` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: show platform information for cloud session; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/quit` - Kind: alias; Surface: CLI; Args: none; Aliases: /exit; Purpose: alias of /exit; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/recap` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: recap the current session; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/remove-dir` - Kind: alias; Surface: CLI; Args: path; Aliases: /undo-add-dir; Purpose: alias of /undo-add-dir; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/rename` - Kind: built-in; Surface: CLI; Args: optional new title; Aliases: /title, /rename-session; Purpose: rename the current session; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/rename-session` - Kind: alias; Surface: CLI; Args: none; Aliases: /rename; Purpose: alias of /rename; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/repo` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: open the repository in cloud session; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/revert` - Kind: built-in; Surface: CLI; Args: optional step; Aliases: none; Purpose: revert to a previous step; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/rm-session` - Kind: built-in; Surface: CLI; Args: session-id; Aliases: none; Purpose: delete a session; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/session-stats` - Kind: built-in; Surface: CLI; Args: none; Aliases: /stats; Purpose: show session statistics; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/shortcuts` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: show interactive keyboard shortcuts; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/smart` - Kind: built-in; Surface: CLI; Args: optional prompt; Aliases: none; Purpose: switch to Smart mode or run a prompt in it; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF, SLASHCMDS-IN01-SC-DEVIN-ESS
- `/ssh` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: connect to a cloud session via SSH; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/stats` - Kind: alias; Surface: CLI; Args: none; Aliases: /session-stats; Purpose: alias of /session-stats; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/status` - Kind: alias; Surface: CLI; Args: none; Aliases: /login-status; Purpose: alias of /login-status; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/steps` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: show the steps of the current session; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/theme` - Kind: built-in; Surface: CLI; Args: theme name; Aliases: none; Purpose: switch the terminal theme; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/title` - Kind: alias; Surface: CLI; Args: none; Aliases: /rename; Purpose: alias of /rename; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/undo-add-dir` - Kind: built-in; Surface: CLI; Args: path; Aliases: /remove-dir; Purpose: remove a workspace directory; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/update` - Kind: built-in; Surface: CLI; Args: --force; Aliases: none; Purpose: check for and install updates; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/upgrade` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: upgrade subscription plan; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/usage` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: show estimated credit usage for the session; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/workspace` - Kind: built-in; Surface: CLI; Args: none; Aliases: /workspaces; Purpose: list workspace directories; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF, SLASHCMDS-IN01-SC-DEVIN-ESS
- `/workspaces` - Kind: alias; Surface: CLI; Args: none; Aliases: /workspace; Purpose: alias of /workspace; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF
- `/yolo` - Kind: alias; Surface: CLI; Args: none; Aliases: /bypass; Purpose: alias of /bypass; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-DEVIN-CMDREF, SLASHCMDS-IN01-SC-DEVIN-ESS

**Collision rule**: Custom slash commands are organization-defined in the Devin web app and appear in the web chat menu; in the CLI, unknown slash commands immediately fail with "Unknown command". Built-in names are reserved and cannot be overridden by custom commands in either surface.

**Searched, not found**

- Searched `https://docs.devin.ai/cli/reference/commands` and `https://docs.devin.ai/cli/essential-commands` for the complete slash command list; all commands are recorded.
- Searched `https://docs.devin.ai/work-with-devin/slash-commands`; the web app only supports organization-defined custom slash commands, not vendor-built-ins.
- Searched the local Devin Desktop installation `C:\Users\User\AppData\Local\Programs\Devin\resources\app` with `rg.exe`; source is minified and no additional built-in slash commands were found beyond the CLI reference.

**Status**: COMPLETE 2026-11-17

## 6. Agent: GitHub Copilot

**Product facts**: GitHub Copilot coding assistant. Surfaces covered: VS Code, Visual Studio, JetBrains IDEs, Xcode, Eclipse; github.com chat; GitHub Mobile app chat; Copilot CLI interactive sessions; Copilot app (desktop and web) agent sessions; coding-agent/agent-mode commands are included where they surface in VS Code agent chat, CLI, and the Copilot app. Version checked: VS Code Copilot Chat extension `0.76.0` from `extensions/copilot/package.json` in `microsoft/vscode`; Copilot CLI changelog `1.0.112` (2026-11-13); docs accessed 2026-11-17.

**Keywords**

- `/add-dir` - Kind: built-in; Surface: CLI; Args: path; Aliases: none; Purpose: add a directory to the active workspace; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/af` - Kind: built-in; Surface: Copilot app; Args: none; Aliases: none; Purpose: search Agent Finder for installable MCP servers, tools, skills, and agents; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-APP
- `/after` - Kind: built-in; Surface: CLI; Args: delay prompt; Aliases: none; Purpose: schedule a one-off prompt for a future time; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/agent` - Kind: built-in; Surface: CLI, Copilot app; Args: none; Aliases: none; Purpose: select a custom agent for the session; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF, SLASHCMDS-IN01-SC-GHCP-APP
- `/agents` - Kind: built-in; Surface: CLI; Args: none; Aliases: /subagents; Purpose: alias of /subagents for selecting subagents; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/allow-all` - Kind: alias; Surface: CLI; Args: on|off|show; Aliases: /permissions; Purpose: alias of /permissions allow-all; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/allow-all-tools` - Kind: built-in; Surface: Copilot app; Args: none; Aliases: /yolo; Purpose: turn tool auto-approval on or show its state; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-APP
- `/app` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: open the current session in the GitHub Copilot app; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/ask` - Kind: built-in; Surface: CLI; Args: question; Aliases: /btw; Purpose: ask a one-shot side question without changing code; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/attach-files` - Kind: built-in; Surface: Copilot app; Args: none; Aliases: none; Purpose: open a file picker and attach files to the message; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-APP
- `/attach-folder` - Kind: built-in; Surface: Copilot app; Args: none; Aliases: none; Purpose: open a folder picker and attach a folder to the message; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-APP
- `/autoApprove` - Kind: built-in; Surface: VS Code; Args: none; Aliases: /yolo; Purpose: toggle global auto-approval of safe commands in agent mode; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-VSCHG
- `/autopilot` - Kind: built-in; Surface: CLI, Copilot app; Args: prompt; Aliases: /goal; Purpose: switch to Autopilot mode and optionally start with a prompt; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF, SLASHCMDS-IN01-SC-GHCP-APP
- `/branch` - Kind: alias; Surface: CLI; Args: name; Aliases: /fork; Purpose: alias of /fork for branching the session; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/btw` - Kind: alias; Surface: CLI; Args: question; Aliases: /ask; Purpose: alias of /ask for a side question; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/bug` - Kind: alias; Surface: CLI; Args: none; Aliases: /feedback; Purpose: alias of /feedback for submitting a bug report; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/caffeinate` - Kind: alias; Surface: CLI; Args: on|off|busy|duration; Aliases: /keep-alive; Purpose: alias of /keep-alive to keep the machine awake; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/cd` - Kind: built-in; Surface: CLI; Args: path; Aliases: none; Purpose: change the session working directory; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/changelog` - Kind: built-in; Surface: CLI; Args: summarize version; Aliases: /release-notes; Purpose: show interactive release notes for Copilot CLI; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/chronicle` - Kind: built-in; Surface: JetBrains, CLI, Copilot app; Args: subcommand; Aliases: none; Purpose: review and analyze session history; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CHTSH, SLASHCMDS-IN01-SC-GHCP-CLIREF, SLASHCMDS-IN01-SC-GHCP-APP
- `/clear` - Kind: built-in; Surface: VS Code, github.com chat, CLI, Copilot app; Args: prompt; Aliases: /new, /reset; Purpose: start a new chat session; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CHTSH, SLASHCMDS-IN01-SC-GHCP-CLIREF, SLASHCMDS-IN01-SC-GHCP-APP
- `/clikit` - Kind: built-in; Surface: CLI; Args: component; Aliases: none; Purpose: inspect or configure CLI UI component internals; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/collect-debug-logs` - Kind: built-in; Surface: CLI, Copilot app; Args: file|gist|share path; Aliases: none; Purpose: collect and export debug logs; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF, SLASHCMDS-IN01-SC-GHCP-APP
- `/compact` - Kind: built-in; Surface: JetBrains, VS Code, CLI, Copilot app; Args: focus-instructions; Aliases: none; Purpose: summarize earlier conversation to reduce context pressure; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CHTSH, SLASHCMDS-IN01-SC-GHCP-VSCHG, SLASHCMDS-IN01-SC-GHCP-CLIREF, SLASHCMDS-IN01-SC-GHCP-APP
- `/config` - Kind: alias; Surface: CLI; Args: key value; Aliases: /settings; Purpose: alias of /settings for changing configuration; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/context` - Kind: built-in; Surface: CLI, Copilot app; Args: none; Aliases: none; Purpose: show current session context usage; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF, SLASHCMDS-IN01-SC-GHCP-APP
- `/continue` - Kind: alias; Surface: CLI; Args: session-id; Aliases: /resume; Purpose: alias of /resume for continuing a previous session; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/copy` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: copy the last response to clipboard; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/create-agent` - Kind: built-in; Surface: VS Code; Args: none; Aliases: none; Purpose: create a custom agent definition in agent mode; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-VSCHG
- `/create-canvas` - Kind: built-in; Surface: Copilot app; Args: prompt; Aliases: none; Purpose: invoke the canvas-authoring skill; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-APP
- `/create-hook` - Kind: built-in; Surface: VS Code; Args: none; Aliases: none; Purpose: create a lifecycle hook in agent mode; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-VSCHG
- `/create-instruction` - Kind: built-in; Surface: VS Code; Args: none; Aliases: none; Purpose: create a custom instruction file in agent mode; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-VSCHG
- `/create-prompt` - Kind: built-in; Surface: VS Code; Args: none; Aliases: none; Purpose: create a prompt file in agent mode; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-VSCHG
- `/create-skill` - Kind: built-in; Surface: VS Code; Args: none; Aliases: none; Purpose: create a skill file in agent mode; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-VSCHG
- `/cwd` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: show the current working directory; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/debug` - Kind: built-in; Surface: Copilot app; Args: none; Aliases: none; Purpose: copy session debug JSON to clipboard; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-APP
- `/delegate` - Kind: built-in; Surface: CLI; Args: prompt; Aliases: none; Purpose: delegate the current task to Copilot; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/delete` - Kind: built-in; Surface: github.com chat; Args: none; Aliases: none; Purpose: delete the current conversation; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CHTSH
- `/diagnose` - Kind: built-in; Surface: CLI; Args: prompt; Aliases: none; Purpose: diagnose problems in the workspace or session; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/diff` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: show the Git diff including untracked files; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/disableAutoApprove` - Kind: built-in; Surface: VS Code; Args: none; Aliases: /disableYolo; Purpose: turn off global auto-approval in agent mode; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-VSCHG
- `/disableYolo` - Kind: alias; Surface: VS Code; Args: none; Aliases: /disableAutoApprove; Purpose: alias of /disableAutoApprove; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-VSCHG
- `/doc` - Kind: built-in; Surface: Visual Studio, Xcode; Args: none; Aliases: none; Purpose: generate documentation for the selected symbol; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CHTSH
- `/downgrade` - Kind: built-in; Surface: CLI; Args: version; Aliases: none; Purpose: downgrade the CLI to a specific version; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/env` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: show the pre-conversation environment picker state; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/every` - Kind: built-in; Surface: CLI; Args: interval prompt; Aliases: none; Purpose: schedule a recurring prompt; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/exit` - Kind: built-in; Surface: CLI; Args: none; Aliases: /quit; Purpose: exit the interactive CLI; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/experimental` - Kind: built-in; Surface: CLI; Args: on|off|show; Aliases: none; Purpose: toggle experimental features; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/export` - Kind: alias; Surface: CLI; Args: options; Aliases: /share; Purpose: alias of /share for exporting the session; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/export-gist` - Kind: built-in; Surface: Copilot app; Args: none; Aliases: none; Purpose: export the transcript to a secret gist; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-APP
- `/extension` - Kind: alias; Surface: CLI; Args: manage|mode; Aliases: /extensions; Purpose: alias of /extensions for managing extensions; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/extensions` - Kind: built-in; Surface: CLI; Args: manage|mode; Aliases: /extension; Purpose: manage CLI extensions; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/feedback` - Kind: built-in; Surface: CLI; Args: none; Aliases: /bug; Purpose: submit feedback; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/find` - Kind: alias; Surface: CLI; Args: query; Aliases: /search; Purpose: alias of /search; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/fix` - Kind: built-in; Surface: VS Code, Visual Studio, JetBrains, Xcode, Eclipse; Args: none; Aliases: none; Purpose: propose a fix for problems in selected code; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CHTSH, SLASHCMDS-IN01-SC-GHCP-IDE
- `/fixTestFailure` - Kind: built-in; Surface: VS Code; Args: none; Aliases: none; Purpose: find and fix a failing test; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CHTSH
- `/fleet` - Kind: built-in; Surface: CLI, Copilot app; Args: prompt; Aliases: none; Purpose: launch multiple agents in parallel for one task; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF, SLASHCMDS-IN01-SC-GHCP-APP
- `/footer` - Kind: alias; Surface: CLI; Args: none; Aliases: /statusline; Purpose: alias of /statusline for toggling the terminal footer; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/fork` - Kind: built-in; Surface: CLI, Copilot app; Args: name; Aliases: /branch; Purpose: fork the current session; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF, SLASHCMDS-IN01-SC-GHCP-APP
- `/goal` - Kind: alias; Surface: CLI; Args: objective; Aliases: /autopilot; Purpose: alias of /autopilot for autonomous execution; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/help` - Kind: built-in; Surface: VS Code, Visual Studio, JetBrains, CLI; Args: none; Aliases: none; Purpose: show quick reference for available slash commands; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CHTSH, SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/hooks` - Kind: built-in; Surface: CLI, VS Code; Args: none; Aliases: none; Purpose: view or manage lifecycle hooks; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF, SLASHCMDS-IN01-SC-GHCP-VSCHG
- `/ide` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: connect the CLI session to the current VS Code workspace; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/inbox` - Kind: built-in; Surface: Copilot app; Args: none; Aliases: none; Purpose: render an interactive inbox widget; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-APP
- `/init` - Kind: built-in; Surface: CLI, Copilot app, VS Code; Args: instructions; Aliases: none; Purpose: generate or improve repository instructions; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF, SLASHCMDS-IN01-SC-GHCP-APP, SLASHCMDS-IN01-SC-GHCP-VSCHG
- `/instructions` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: view or edit custom instructions for the session; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/interactive` - Kind: built-in; Surface: Copilot app; Args: prompt; Aliases: none; Purpose: switch to Interactive mode; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-APP
- `/keep-alive` - Kind: built-in; Surface: CLI; Args: on|off|busy|duration; Aliases: /caffeinate; Purpose: prevent the machine from going to sleep during remote sessions; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/limits` - Kind: built-in; Surface: CLI; Args: set|unset key; Aliases: none; Purpose: set or unset AI credit session limits; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/list-dirs` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: list directories in the active workspace; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/login` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: authenticate with GitHub; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/logout` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: sign out of GitHub Copilot CLI; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/lsp` - Kind: built-in; Surface: CLI; Args: show|test|reload|logs|help server; Aliases: none; Purpose: manage the built-in LSP client; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/mcp` - Kind: built-in; Surface: CLI, Copilot app; Args: config|list|show|add|edit|delete|disable|enable|auth|reload|search server; Aliases: none; Purpose: manage MCP servers; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF, SLASHCMDS-IN01-SC-GHCP-APP
- `/merge-to-parent` - Kind: built-in; Surface: Copilot app; Args: none; Aliases: none; Purpose: merge a forked session back to its parent; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-APP
- `/model` - Kind: built-in; Surface: CLI, Copilot app; Args: model|auto tier; Aliases: /models; Purpose: select or show the active model; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF, SLASHCMDS-IN01-SC-GHCP-APP
- `/models` - Kind: alias; Surface: CLI, Copilot app; Args: model; Aliases: /model; Purpose: alias of /model; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF, SLASHCMDS-IN01-SC-GHCP-APP
- `/new` - Kind: alias; Surface: CLI, Copilot app; Args: prompt; Aliases: /clear; Purpose: alias of /clear for starting a new session; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF, SLASHCMDS-IN01-SC-GHCP-APP
- `/optimize` - Kind: built-in; Surface: Visual Studio; Args: none; Aliases: none; Purpose: analyze and improve running time of selected code; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CHTSH
- `/orchestrate` - Kind: built-in; Surface: Copilot app; Args: prompt; Aliases: none; Purpose: coordinate work across sessions or repositories; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-APP
- `/permissions` - Kind: built-in; Surface: CLI; Args: default|assisted|allow-all|show|reset; Aliases: /allow-all, /yolo; Purpose: show or change tool approval mode; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/plan` - Kind: built-in; Surface: CLI, Copilot app; Args: prompt; Aliases: none; Purpose: switch to Plan mode; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF, SLASHCMDS-IN01-SC-GHCP-APP
- `/plugin` - Kind: built-in; Surface: CLI, Copilot app; Args: install|update|uninstall|list|marketplace subcommand; Aliases: none; Purpose: manage plugins and marketplace; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF, SLASHCMDS-IN01-SC-GHCP-APP
- `/pr` - Kind: built-in; Surface: CLI; Args: view|create|fix|auto|automerge; Aliases: none; Purpose: manage pull requests; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/pr-fix-checks` - Kind: built-in; Surface: Copilot app; Args: none; Aliases: none; Purpose: address failing checks on an open pull request; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-APP
- `/pr-merge` - Kind: built-in; Surface: Copilot app; Args: none; Aliases: none; Purpose: merge an open pull request; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-APP
- `/pr-open` - Kind: built-in; Surface: Copilot app; Args: none; Aliases: none; Purpose: open a pull request; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-APP
- `/pr-resolve-comments` - Kind: built-in; Surface: Copilot app; Args: none; Aliases: none; Purpose: resolve comments on a pull request; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-APP
- `/quit` - Kind: alias; Surface: CLI; Args: none; Aliases: /exit; Purpose: alias of /exit for closing the interactive CLI; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/refine` - Kind: built-in; Surface: CLI; Args: text; Aliases: none; Purpose: refine the last prompt or selected text; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/release-notes` - Kind: alias; Surface: CLI; Args: version; Aliases: /changelog; Purpose: alias of /changelog; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/remote` - Kind: built-in; Surface: JetBrains, CLI, Copilot app; Args: on|off; Aliases: none; Purpose: enable or manage remote control of the CLI session; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CHTSH, SLASHCMDS-IN01-SC-GHCP-CLIREF, SLASHCMDS-IN01-SC-GHCP-APP
- `/remote-control` - Kind: conditional; Surface: CLI; Args: on|off; Aliases: none; Purpose: remote control toggle, available through /remote; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/rename` - Kind: built-in; Surface: github.com chat, CLI, Copilot app; Args: name; Aliases: /session rename; Purpose: rename the current session; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CHTSH, SLASHCMDS-IN01-SC-GHCP-CLIREF, SLASHCMDS-IN01-SC-GHCP-APP
- `/research` - Kind: built-in; Surface: CLI, Copilot app; Args: topic; Aliases: none; Purpose: research a topic with agents; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF, SLASHCMDS-IN01-SC-GHCP-APP
- `/reset` - Kind: alias; Surface: CLI, Copilot app; Args: prompt; Aliases: /clear; Purpose: alias of /clear; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF, SLASHCMDS-IN01-SC-GHCP-APP
- `/reset-allowed-tools` - Kind: built-in; Surface: CLI, Copilot app; Args: none; Aliases: none; Purpose: reset the allowed-tools list; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF, SLASHCMDS-IN01-SC-GHCP-APP
- `/restart` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: restart the current session; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/restart-session` - Kind: built-in; Surface: Copilot app; Args: none; Aliases: none; Purpose: restart the current app session; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-APP
- `/resume` - Kind: built-in; Surface: CLI; Args: session-id; Aliases: /continue; Purpose: resume a previous session; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/review` - Kind: built-in; Surface: CLI, Copilot app; Args: prompt; Aliases: none; Purpose: request a code review; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF, SLASHCMDS-IN01-SC-GHCP-APP
- `/rewind` - Kind: alias; Surface: CLI; Args: none; Aliases: /undo; Purpose: alias of /undo for rewinding conversation history; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/rubber-duck` - Kind: built-in; Surface: CLI, Copilot app; Args: prompt; Aliases: none; Purpose: get a second opinion from the rubber duck agent; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF, SLASHCMDS-IN01-SC-GHCP-APP
- `/sandbox` - Kind: built-in; Surface: CLI, Copilot app; Args: config|status|policy|enable|disable|on|off; Aliases: none; Purpose: manage sandbox settings; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF, SLASHCMDS-IN01-SC-GHCP-APP
- `/search` - Kind: built-in; Surface: CLI; Args: query; Aliases: /find; Purpose: search the codebase or session history; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/security-review` - Kind: built-in; Surface: CLI, Copilot app; Args: prompt; Aliases: none; Purpose: run a security review; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF, SLASHCMDS-IN01-SC-GHCP-APP
- `/session` - Kind: built-in; Surface: CLI; Args: info|checkpoints|files|plan|rename|cleanup|prune|delete|delete-all; Aliases: /sessions; Purpose: manage the current session; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/session rename` - Kind: alias; Surface: CLI; Args: name; Aliases: /rename; Purpose: alias of /rename for renaming the session; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/sessions` - Kind: alias; Surface: CLI; Args: subcommand; Aliases: /session; Purpose: alias of /session; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/settings` - Kind: built-in; Surface: CLI; Args: repo|local|show|key value; Aliases: /config; Purpose: change CLI settings; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/share` - Kind: built-in; Surface: CLI; Args: link|off|file|html|gist|research options; Aliases: /export; Purpose: export or share the session; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/simplify` - Kind: built-in; Surface: Xcode; Args: none; Aliases: none; Purpose: simplify the current code selection; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CHTSH
- `/skills` - Kind: built-in; Surface: CLI, Copilot app; Args: list|info|add|remove|reload; Aliases: none; Purpose: manage agent skills; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF, SLASHCMDS-IN01-SC-GHCP-APP
- `/spar` - Kind: built-in; Surface: Copilot app; Args: prompt; Aliases: none; Purpose: start a sparring session with an agent; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-APP
- `/spawn` - Kind: built-in; Surface: Copilot app; Args: prompt; Aliases: none; Purpose: spawn a background task; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-APP
- `/statusline` - Kind: built-in; Surface: CLI; Args: none; Aliases: /footer; Purpose: toggle or configure the terminal status line; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/subagents` - Kind: built-in; Surface: CLI; Args: none; Aliases: /agents; Purpose: manage subagents; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/tasks` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: open the background tasks dialog; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/terminal` - Kind: built-in; Surface: Copilot app; Args: command; Aliases: none; Purpose: run a terminal command in the app session; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-APP
- `/terminal-setup` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: configure terminal keybindings for multiline input; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/tests` - Kind: built-in; Surface: VS Code, Visual Studio, JetBrains, Xcode, Eclipse; Args: none; Aliases: none; Purpose: generate unit tests for selected code; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CHTSH, SLASHCMDS-IN01-SC-GHCP-IDE
- `/theme` - Kind: built-in; Surface: CLI; Args: default|github|dim|high-contrast|colorblind; Aliases: none; Purpose: change the terminal color theme; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/tuikit` - Kind: built-in; Surface: CLI; Args: colors|icons|select|tabbar; Aliases: none; Purpose: inspect or configure TUI kit components; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/undo` - Kind: built-in; Surface: CLI; Args: none; Aliases: /rewind; Purpose: rewind the conversation history; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/update` - Kind: built-in; Surface: CLI; Args: stable|prerelease; Aliases: /upgrade; Purpose: check for and install CLI updates; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF, SLASHCMDS-IN01-SC-GHCP-CLICHG
- `/upgrade` - Kind: alias; Surface: CLI; Args: none; Aliases: /update; Purpose: alias of /update; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/usage` - Kind: built-in; Surface: CLI, Copilot app; Args: none; Aliases: none; Purpose: show account usage; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF, SLASHCMDS-IN01-SC-GHCP-APP
- `/user` - Kind: built-in; Surface: CLI; Args: show|list|switch; Aliases: none; Purpose: show or switch the active GitHub user; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/version` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: show the CLI version; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/vim` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: toggle Vim keybindings in the TUI; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/voice` - Kind: built-in; Surface: CLI; Args: on|off|models|devices; Aliases: none; Purpose: toggle voice dictation mode; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/workflows` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: list and manage workflows; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/worktree` - Kind: built-in; Surface: CLI; Args: branch|task|new; Aliases: none; Purpose: manage Git worktrees; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF
- `/yolo` - Kind: alias; Surface: CLI, VS Code; Args: none; Aliases: /permissions; Purpose: alias of /permissions allow-all or /autoApprove depending on surface; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GHCP-CLIREF, SLASHCMDS-IN01-SC-GHCP-VSCHG

**Collision rule**: Custom slash commands and skills appear alongside built-ins in the slash menu; exact matches run the built-in command, so built-in names win. User-defined agent instructions, prompts, skills, and MCP tools are excluded from the keyword list but may shadow names if the client allows it.

**Searched, not found**

- Searched the GitHub Copilot Chat cheat sheet for per-surface tables; recorded the surface-specific commands found (VS Code, Visual Studio, JetBrains, Xcode, github.com chat). The Eclipse table is not listed separately; vendor docs only demonstrate `/fix` and `/tests`, with `/explain` mentioned as an example.
- Searched `https://docs.github.com/en/copilot/how-tos/copilot-on-github/chat-with-copilot/chat-in-mobile` for GitHub Mobile built-in slash commands; only natural-language prompts are documented, no `/` command list.
- Searched the Copilot CLI interactive slash-command reference and recorded every distinct keyword and alias. Subcommands are collapsed into the Args field of their parent keyword.
- Searched the VS Code `extensions/copilot/CHANGELOG.md` for agent-mode slash commands added in the last six months; recorded `/agents`, `/hooks`, `/compact`, `/autoApprove`, `/disableAutoApprove`, `/yolo`, `/disableYolo`, and creation commands.
- Searched `https://github.com/github/copilot-cli/blob/main/changelog.md` for slash command changes; no new slash keywords were added beyond the existing reference.

**Status**: COMPLETE 2026-11-17

## 7. Agent: Google Gemini

**Product facts**: Google Gemini consumer and Workspace chatbot. Surfaces covered: gemini.google.com web app, Gemini mobile apps (iOS/Android), Gemini in Chrome side panel, and Google Workspace side panels. Version checked: current help docs dated 2026-11-17. Google Gemini Code Assist and Android Studio assistants are adjacent products and excluded from this keyword list.

**Keywords**

- none found

**Collision rule**: Typing `/` in Gemini opens the user's saved Skills menu; Skills are custom, user-defined instructions and are excluded from the built-in keyword list. The same applies to `@`-triggered Workspace extensions. Built-in slash commands are not documented by the vendor.

**Searched, not found**

- Searched `https://support.google.com/gemini/answer/17094296` (Create & manage skills for Gemini Apps); the only slash-triggered behavior is user-defined Skills, not vendor-built-in commands.
- Searched `https://support.google.com/gemini/answer/16988996` (Customize your Gemini in Chrome experience); the `/` menu opens built-in library skills and user-created skills, not vendor slash commands.
- Searched `https://support.google.com/gemini/answer/17094507` (Manage your tasks & workflows in Gemini Apps); tasks are created via the UI button or natural language, with `@skill` mentions; no `/` built-ins are listed.
- Searched web for `site:docs.google.com gemini slash commands` and `gemini.google.com slash commands`; third-party sources confirm there is no system slash-command menu in Gemini, only user Skills and `@` extensions.

**Status**: COMPLETE 2026-11-17

## 8. Agent: Google Jules

**Product facts**: Google Jules autonomous coding agent. Surfaces covered: jules.google web app, Jules Tools CLI (`@google/jules` npm package), Jules API, and the Jules extension for Gemini CLI. Version checked: Jules Tools reference docs and Gemini CLI extension README dated 2026-11-17.

**Keywords**

- `/jules` - Kind: bundled; Surface: Gemini CLI extension; Args: prompt; Aliases: none; Purpose: delegate an asynchronous coding task to Jules and check task status; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-JULES-EXT

**Collision rule**: The Jules extension registers `/jules` in Gemini CLI's slash menu alongside built-in Gemini CLI commands; exact matches resolve to the built-in or extension command registered first, so `/jules` wins over a user custom command of the same name in the Gemini CLI surface.

**Searched, not found**

- Searched `https://jules.google/` and `https://jules.google/docs/faq/` for web-app slash commands; the web UI uses natural-language prompts and the `jules` GitHub issue label, with no `/` commands documented.
- Searched `https://jules.google/docs/cli/reference/` and `https://jules.google/docs/changelog/2025-10-02/` for Jules Tools CLI slash commands; the CLI uses `jules remote`, `jules remote new`, and `jules remote pull` subcommands, and the TUI docs do not list any `/`-prefixed commands.
- Searched `https://jules.googleapis.com` API reference; no chat or slash-command surface is exposed.
- Searched the Gemini CLI extension repository `gemini-cli-extensions/jules`; the only slash command it exposes is `/jules`.

**Status**: COMPLETE 2026-11-17

## 9. Agent: Google Antigravity

**Product facts**: Google Antigravity agentic IDE and CLI. Surfaces covered: Antigravity App (Desktop and Web), Antigravity CLI (`agy` TUI). Version checked: Antigravity slash-commands overview and CLI reference docs dated 2026-11-17. Commands marked App-only or CLI-only are conditional to the surface.

**Keywords**

- `/add-dir` - Kind: built-in; Surface: CLI; Args: path; Aliases: none; Purpose: add a directory path to the active workspace; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/agents` - Kind: built-in; Surface: App, CLI; Args: none; Aliases: none; Purpose: open the Agent Manager panel to switch agents and monitor subagents; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-OVR, SLASHCMDS-IN01-SC-ANTGRV-CLI, SLASHCMDS-IN01-SC-ANTGRV-AGT
- `/agy-customizations` - Kind: built-in; Surface: App, CLI; Args: request; Aliases: none; Purpose: load the customization reference for rules, skills, plugins, hooks, and MCP servers; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-OVR, SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/antigravity-guide` - Kind: built-in; Surface: App, CLI; Args: question; Aliases: none; Purpose: ask how to use or configure Antigravity from the official docs; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-OVR, SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/artifact` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: open the Artifact Review panel; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/automation` - Kind: built-in; Surface: App; Args: request; Aliases: none; Purpose: set up a scheduled background automation in the Automations tab; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-OVR
- `/boost` - Kind: built-in; Surface: App, CLI; Args: task; Aliases: none; Purpose: run on-demand multi-agent deep reasoning loops; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-OVR, SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/branch` - Kind: alias; Surface: CLI; Args: name; Aliases: /fork; Purpose: alias of /fork; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/browser` - Kind: built-in; Surface: App, CLI; Args: task; Aliases: none; Purpose: delegate web browsing, UI verification, and in-browser debugging to the browser subagent; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-OVR, SLASHCMDS-IN01-SC-ANTGRV-CLI, SLASHCMDS-IN01-SC-ANTGRV-BRW
- `/btw` - Kind: built-in; Surface: App, CLI; Args: query; Aliases: none; Purpose: ask a side question in the background without pausing work; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-OVR, SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/changelog` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: open the interactive release notes viewer; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/clear` - Kind: built-in; Surface: CLI; Args: none; Aliases: /new; Purpose: clear the terminal and reset conversation contexts; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/codesearch` - Kind: built-in; Surface: CLI; Args: query; Aliases: /cs, /search; Purpose: open the interactive Code Search panel; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/config` - Kind: built-in; Surface: CLI; Args: none; Aliases: /settings; Purpose: open the interactive Settings Editor; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/context` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: open the context usage visualization panel; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/conversation` - Kind: alias; Surface: CLI; Args: none; Aliases: /resume; Purpose: alias of /resume for opening the conversation picker; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/copy` - Kind: built-in; Surface: CLI; Args: n|btw; Aliases: none; Purpose: copy the last agent response or the latest /btw answer; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/credits` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: view remaining AI credits and purchase links; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/cs` - Kind: alias; Surface: CLI; Args: query; Aliases: /codesearch; Purpose: alias of /codesearch; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/diff` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: open the interactive diff viewer; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/effort` - Kind: built-in; Surface: CLI; Args: level; Aliases: none; Purpose: set or inspect the active model's reasoning effort level; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/exit` - Kind: built-in; Surface: CLI; Args: none; Aliases: /quit; Purpose: close the TUI session; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/feedback` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: open the feedback submission panel; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/fork` - Kind: built-in; Surface: CLI; Args: name; Aliases: /branch; Purpose: clone the current conversation thread into a new parallel session; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/generative_ui` - Kind: built-in; Surface: App; Args: request; Aliases: none; Purpose: build interactive widgets as HTML artifacts or inline in the conversation; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-OVR
- `/goal` - Kind: built-in; Surface: App, CLI; Args: objective; Aliases: none; Purpose: run autonomously until the goal is verified complete; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-OVR, SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/grill-me` - Kind: built-in; Surface: App, CLI; Args: task; Aliases: none; Purpose: interview you one question at a time before starting work; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-OVR, SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/help` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: open the help panel showing commands and shortcuts; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/hooks` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: browse active pre-flight and post-format script hooks; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/keybindings` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: open the interactive Keyboard Shortcut Editor; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/learn` - Kind: built-in; Surface: App, CLI; Args: instruction; Aliases: none; Purpose: capture session corrections as persistent rules or skills; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-OVR, SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/logout` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: disconnect the profile and purge authentication tokens; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/mcp` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: open the MCP server manager; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/model` - Kind: built-in; Surface: CLI; Args: model prompt; Aliases: none; Purpose: choose the preferred reasoning model or run a single prompt on another model; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/new` - Kind: alias; Surface: CLI; Args: none; Aliases: /clear; Purpose: alias of /clear; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/open` - Kind: built-in; Surface: CLI; Args: path; Aliases: none; Purpose: force the path to open inside the default system editor; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/permissions` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: open the interactive tool permissions manager panel; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/plan` - Kind: built-in; Surface: App, CLI; Args: task; Aliases: none; Purpose: research code, clarify requirements, and draft a reviewable Implementation Plan; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-OVR, SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/plugin` - Kind: built-in; Surface: App, CLI; Args: install|uninstall|enable|disable|list; Aliases: /plugins; Purpose: open the interactive Plugins Manager or run inline plugin commands; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-OVR, SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/plugins` - Kind: alias; Surface: CLI; Args: subcommand; Aliases: /plugin; Purpose: alias of /plugin; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/quit` - Kind: alias; Surface: CLI; Args: none; Aliases: /exit; Purpose: alias of /exit; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/quota` - Kind: alias; Surface: CLI; Args: none; Aliases: /usage; Purpose: alias of /usage; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/record` - Kind: alias; Surface: CLI; Args: none; Aliases: /voice; Purpose: alias of /voice for dictation/recording; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/remote-control` - Kind: built-in; Surface: CLI; Args: on|off; Aliases: none; Purpose: toggle remote control of the CLI session; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/rename` - Kind: built-in; Surface: CLI; Args: name; Aliases: none; Purpose: rename the current session thread; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/resume` - Kind: built-in; Surface: CLI; Args: none; Aliases: /switch, /conversation; Purpose: open the conversation picker overlay; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/rewind` - Kind: built-in; Surface: CLI; Args: none; Aliases: /undo; Purpose: go back in conversation history; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/run-workflow` - Kind: built-in; Surface: App, CLI; Args: request; Aliases: none; Purpose: write and run a Python script that orchestrates many agents across parallel and sequential phases; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-OVR
- `/schedule` - Kind: built-in; Surface: App, CLI; Args: when task; Aliases: none; Purpose: schedule an instruction as a one-time timer or recurring cron job; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-OVR, SLASHCMDS-IN01-SC-ANTGRV-CLI, SLASHCMDS-IN01-SC-ANTGRV-SCH
- `/search` - Kind: alias; Surface: CLI; Args: query; Aliases: /codesearch; Purpose: alias of /codesearch; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/settings` - Kind: alias; Surface: CLI; Args: none; Aliases: /config; Purpose: alias of /config; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/skills` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: open the skill picker or reload skills; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/swarm` - Kind: built-in; Surface: App, CLI; Args: task; Aliases: none; Purpose: run named workers and a verifier that coordinate on a shared message board; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-OVR, SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/switch` - Kind: alias; Surface: CLI; Args: none; Aliases: /resume; Purpose: alias of /resume for switching conversations; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/tasks` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: toggle or view the tasks panel; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/teamwork` - Kind: built-in; Surface: App, CLI; Args: task; Aliases: none; Purpose: run collaborative multi-agent teams for repo-scale work; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-OVR, SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/title` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: configure terminal title items; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/undo` - Kind: alias; Surface: CLI; Args: none; Aliases: /rewind; Purpose: alias of /rewind; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/usage` - Kind: built-in; Surface: CLI; Args: none; Aliases: /quota; Purpose: display model credit consumption and quota limits; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-CLI
- `/voice` - Kind: built-in; Surface: CLI; Args: live|dictate; Aliases: /record; Purpose: toggle voice dictation or live voice mode; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-ANTGRV-CLI

**Collision rule**: Custom agents, skills, plugins, and user-defined workflows can be invoked with `/` in both the App and CLI; the slash menu resolves by exact match and built-in commands are registered first, so built-in names win over custom names.

**Searched, not found**

- Searched `https://antigravity.google/docs/slash-commands/` for the complete public command catalog; all reasoning, planning, customization, automation, and tool commands are recorded.
- Searched `https://antigravity.google/docs/cli/reference/` for the CLI core slash-command table; all distinct keywords and aliases are recorded.
- Searched `https://antigravity.google/docs/getting-started/` for additional core commands; no new slash keywords beyond the two references.
- Searched `https://antigravity.google/docs/cli/commands/agents/`, `/browser/`, and `/commands/schedule/` for surface-specific command details; confirmed descriptions but no additional keywords.

**Status**: COMPLETE 2026-11-17

## 10. Agent: Cursor

**Product facts**: Cursor coding agent. Surfaces covered: Cursor CLI (`cursor`/`agent`), Cursor IDE Agent chat, web and mobile agents. Cursor is not installed on this machine, so no `[TESTED]` observations. The official CLI slash-command reference was checked at `cursor.com/docs/cli/reference/slash-commands`; separate IDE/editor built-in slash commands beyond `/summarize` are not documented by the vendor.

**Keywords**

- `/about` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: show CLI version, system, and account info; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CRSR-SLASH
- `/ask` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: toggle Ask mode for read-only questions; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CRSR-SLASH, SLASHCMDS-IN01-SC-CRSR-USING
- `/auto-run` - Kind: alias; Surface: CLI; Args: none; Aliases: /run-everything; Purpose: alias of /run-everything; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CRSR-SLASH
- `/bedrock` - Kind: built-in; Surface: CLI; Args: subcommand; Aliases: none; Purpose: configure Bedrock when the feature is enabled; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CRSR-SLASH
- `/clear` - Kind: built-in; Surface: CLI; Args: none; Aliases: /new, /new-chat, /newchat; Purpose: start a new chat session; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CRSR-SLASH
- `/commit` - Kind: built-in; Surface: IDE; Args: none; Aliases: none; Purpose: generate a commit message from staged changes; Label: ASSUMED; Src: SLASHCMDS-IN01-SC-CRSR-FAN
- `/compress` - Kind: alias; Surface: CLI; Args: none; Aliases: /summarize; Purpose: alias of /summarize; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CRSR-SLASH
- `/config` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: configure CLI settings interactively; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CRSR-SLASH
- `/copy` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: copy a previous user message to clipboard; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CRSR-SLASH
- `/copy-conversation-id` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: copy the current conversation ID; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CRSR-SLASH
- `/copy-request-id` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: copy the last request ID; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CRSR-SLASH
- `/cursor` - Kind: alias; Surface: CLI; Args: none; Aliases: /open; Purpose: alias of /open; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CRSR-SLASH
- `/debug` - Kind: built-in; Surface: CLI; Args: optional prompt; Aliases: none; Purpose: toggle Debug mode or submit a prompt in it; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CRSR-SLASH, SLASHCMDS-IN01-SC-CRSR-USING
- `/doc` - Kind: built-in; Surface: IDE; Args: none; Aliases: none; Purpose: generate documentation for selected code; Label: ASSUMED; Src: SLASHCMDS-IN01-SC-CRSR-FAN
- `/exit` - Kind: built-in; Surface: CLI; Args: none; Aliases: /quit; Purpose: exit; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CRSR-SLASH
- `/explain` - Kind: built-in; Surface: IDE; Args: none; Aliases: none; Purpose: explain selected code; Label: ASSUMED; Src: SLASHCMDS-IN01-SC-CRSR-FAN
- `/feedback` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: share feedback; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CRSR-SLASH
- `/fix` - Kind: built-in; Surface: IDE; Args: none; Aliases: none; Purpose: fix errors in selected code; Label: ASSUMED; Src: SLASHCMDS-IN01-SC-CRSR-FAN
- `/fork` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: fork the current chat into a new session; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CRSR-SLASH
- `/goal` - Kind: built-in; Surface: CLI; Args: objective; Aliases: none; Purpose: give the agent a long-lived objective; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CRSR-SLASH
- `/help` - Kind: built-in; Surface: CLI; Args: optional command; Aliases: none; Purpose: show help; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CRSR-SLASH
- `/line-numbers` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: toggle line numbers in code blocks; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CRSR-SLASH
- `/logs` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: show debug log path and copy it; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CRSR-SLASH
- `/max-mode` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: toggle Max Mode on legacy plans; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CRSR-SLASH
- `/mcp` - Kind: built-in; Surface: CLI; Args: list, list-tools, identifier; Aliases: none; Purpose: manage MCP servers and list tools; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CRSR-SLASH
- `/model` - Kind: built-in; Surface: CLI; Args: optional filter; Aliases: none; Purpose: select a model; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CRSR-SLASH, SLASHCMDS-IN01-SC-CRSR-USING
- `/new` - Kind: alias; Surface: CLI; Args: none; Aliases: /clear; Purpose: alias of /clear; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CRSR-SLASH
- `/new-chat` - Kind: alias; Surface: CLI; Args: none; Aliases: /clear; Purpose: alias of /clear; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CRSR-SLASH
- `/newchat` - Kind: alias; Surface: CLI; Args: none; Aliases: /clear; Purpose: alias of /clear; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CRSR-SLASH
- `/open` - Kind: built-in; Surface: CLI; Args: none; Aliases: /cursor; Purpose: open the repository Git root in Cursor; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CRSR-SLASH
- `/plan` - Kind: built-in; Surface: CLI; Args: optional prompt; Aliases: none; Purpose: switch to Plan mode or submit a prompt in it; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CRSR-SLASH, SLASHCMDS-IN01-SC-CRSR-USING
- `/plugin` - Kind: built-in; Surface: CLI; Args: subcommand; Aliases: none; Purpose: manage plugins and marketplaces; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CRSR-SLASH
- `/quit` - Kind: alias; Surface: CLI; Args: none; Aliases: /exit; Purpose: alias of /exit; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CRSR-SLASH
- `/refactor` - Kind: built-in; Surface: IDE; Args: none; Aliases: none; Purpose: suggest refactoring for selected code; Label: ASSUMED; Src: SLASHCMDS-IN01-SC-CRSR-FAN
- `/rename` - Kind: built-in; Surface: CLI; Args: optional name; Aliases: none; Purpose: rename the current chat session; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CRSR-SLASH
- `/resume` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: open recent chats and resume one; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CRSR-SLASH
- `/rewind` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: jump back to a previous message; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CRSR-SLASH
- `/run` - Kind: alias; Surface: CLI; Args: command; Aliases: /shell, /sh; Purpose: alias of /shell; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CRSR-SLASH
- `/run-everything` - Kind: built-in; Surface: CLI; Args: on, off, status; Aliases: /auto-run; Purpose: toggle Run Everything mode; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CRSR-SLASH
- `/sandbox` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: configure sandbox mode and network access; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CRSR-SLASH
- `/setup-terminal` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: configure terminal newline keybindings; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CRSR-SLASH
- `/sh` - Kind: alias; Surface: CLI; Args: command; Aliases: /shell; Purpose: alias of /shell; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CRSR-SLASH
- `/shell` - Kind: built-in; Surface: CLI; Args: optional command; Aliases: /sh, /run; Purpose: enter Shell Mode; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CRSR-SLASH
- `/show-thinking` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: toggle thinking block display; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CRSR-SLASH
- `/status-indicators` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: toggle terminal title status indicators; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CRSR-SLASH
- `/summarize` - Kind: built-in; Surface: CLI, IDE; Args: none; Aliases: /compress; Purpose: summarize the conversation to reduce context; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CRSR-SLASH, SLASHCMDS-IN01-SC-CRSR-CHG
- `/test` - Kind: built-in; Surface: IDE; Args: none; Aliases: none; Purpose: generate unit tests for selected code; Label: ASSUMED; Src: SLASHCMDS-IN01-SC-CRSR-FAN
- `/update` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: update Cursor Agent; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CRSR-SLASH
- `/vim` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: toggle Vim keys; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CRSR-SLASH

**Collision rule**: Custom slash commands are stored as `.md` files in `.cursor/commands/` (now superseded by skills in `.cursor/skills/`). They appear in the Agent input slash menu; if a custom name matches a built-in, the built-in command is listed first and runs on exact match.

**Searched, not found**

- Searched `https://cursor.com/docs/cli/reference/slash-commands` for the complete list; all official CLI slash commands are recorded.
- Searched `https://cursor.com/docs/cli/using` and `https://cursor.com/docs/cli/reference/parameters` for mode commands; `/plan`, `/ask`, and `/debug` are confirmed.
- Searched `https://cursor.com/changelog/1-6` for IDE slash commands; only `/summarize` and custom commands are mentioned. Community sources list IDE commands `/explain`, `/fix`, `/doc`, `/test`, `/refactor`, `/commit`, but no vendor documentation was found, so they are not recorded as keywords.

**Status**: COMPLETE 2026-11-17

## 11. Agent: OpenAI Codex

**Product facts**: OpenAI Codex. Surfaces covered: Codex CLI (interactive TUI), VS Code/IDE extension, desktop app, and Codex web. Repository `https://github.com/openai/codex.git`, checked commit `e20ccdfa80361deb81266d3ed6baea9c2cdd5ee1` (`main` HEAD, describe `e20ccdf`), accessed 2026-11-17. CLI slash commands are implemented in `codex-rs/tui/src/slash_command.rs`; IDE extension slash commands are documented on the vendor developer-commands page. The desktop app surface is the ChatGPT desktop app's Codex view; the vendor docs treat its slash menu as part of the ChatGPT desktop composer, not as a separate Codex command set, so no additional Codex-specific desktop keywords were found. No vendor documentation for a standalone Codex web slash-command surface was found.

**Keywords**

- `/agents` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: open the agent command center; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-DEVCMDS
- `/app` - Kind: conditional; Surface: CLI; Args: none; Aliases: none; Purpose: continue the current session in the ChatGPT desktop app, visible only on macOS and Windows; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC
- `/approve` - Kind: built-in; Surface: CLI; Args: optional; Aliases: none; Purpose: approve one retry of a recent auto-review denial; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-DEVCMDS
- `/apps` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: manage apps; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-DEVCMDS
- `/archive` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: archive the current session; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-DEVCMDS
- `/btw` - Kind: built-in; Surface: CLI; Args: optional inline text; Aliases: none; Purpose: start a side conversation; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-DEVCMDS
- `/cd` - Kind: built-in; Surface: CLI; Args: path; Aliases: none; Purpose: change the current working directory; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-DEVCMDS
- `/clean` - Kind: alias; Surface: CLI; Args: none; Aliases: /stop; Purpose: alias of /stop that stops all background terminals; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC
- `/clear` - Kind: built-in; Surface: CLI; Args: optional name; Aliases: none; Purpose: clear the terminal and start a new chat; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-DEVCMDS
- `/cloud` - Kind: built-in; Surface: IDE extension; Args: none; Aliases: none; Purpose: switch to Cloud connection or open cloud options (extension surface only); Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CODEX-EXTCMDS
- `/cloud-environment` - Kind: built-in; Surface: IDE extension; Args: none; Aliases: none; Purpose: open the cloud environment picker (extension surface only); Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CODEX-EXTCMDS
- `/compact` - Kind: built-in; Surface: CLI, IDE extension; Args: none; Aliases: none; Purpose: summarize the conversation to free context space; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-EXTCMDS
- `/config` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: open terminal preferences; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-DEVCMDS
- `/copy` - Kind: conditional; Surface: CLI; Args: none; Aliases: none; Purpose: copy the latest response or part of it, hidden on Android; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC
- `/cwd` - Kind: alias; Surface: CLI; Args: none; Aliases: /pwd; Purpose: alias of /pwd that shows the current working directory; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC
- `/daemon` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: manage the local background server; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-DEVCMDS
- `/daybreak` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: toggle Daybreak on or off for OpenAI-provider accounts with access; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-DEVCMDS
- `/debug-config` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: show config layers and requirement sources for debugging; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-DEVCMDS
- `/debug-m-drop` - Kind: hidden; Surface: CLI; Args: none; Aliases: none; Purpose: debugging command for memory drop, labeled DO NOT USE in source; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC
- `/debug-m-update` - Kind: hidden; Surface: CLI; Args: none; Aliases: none; Purpose: debugging command for memory update, labeled DO NOT USE in source; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC
- `/delete` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: permanently delete the current session; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-DEVCMDS
- `/diff` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: show the Git diff including untracked files; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-DEVCMDS
- `/exit` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: exit Codex immediately; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-DEVCMDS
- `/experimental` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: toggle experimental features; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-DEVCMDS
- `/export` - Kind: built-in; Surface: CLI, IDE extension; Args: optional filename; Aliases: none; Purpose: export the conversation as Markdown; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-EXTCMDS
- `/fast` - Kind: built-in; Surface: IDE extension; Args: none; Aliases: none; Purpose: toggle Fast service tier (extension surface only); Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CODEX-EXTCMDS
- `/feedback` - Kind: built-in; Surface: CLI, IDE extension; Args: optional note; Aliases: none; Purpose: send feedback or save a diagnostic ZIP; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-EXTCMDS
- `/fork` - Kind: built-in; Surface: CLI, IDE extension; Args: none; Aliases: none; Purpose: fork the current chat into a new chat; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-EXTCMDS
- `/goal` - Kind: built-in; Surface: CLI, IDE extension; Args: optional objective or edit/pause/resume/clear; Aliases: none; Purpose: set or view the task goal; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-EXTCMDS
- `/help` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: show help; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CODEX-DEVCMDS
- `/hooks` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: view and manage lifecycle hooks; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-DEVCMDS
- `/ide` - Kind: built-in; Surface: CLI; Args: optional inline text; Aliases: none; Purpose: include current IDE selection and open files in the next prompt; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-DEVCMDS
- `/ide-context` - Kind: built-in; Surface: IDE extension; Args: none; Aliases: none; Purpose: include IDE context in the next prompt (extension surface only); Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CODEX-EXTCMDS
- `/import` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: import setup, project files, or recent chats from Claude Code or Cursor; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-DEVCMDS
- `/init` - Kind: built-in; Surface: CLI, IDE extension; Args: none; Aliases: none; Purpose: create an AGENTS.md scaffold for persistent instructions; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-EXTCMDS
- `/keymap` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: remap TUI shortcuts; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-DEVCMDS
- `/local` - Kind: built-in; Surface: IDE extension; Args: none; Aliases: none; Purpose: switch to local connection (extension surface only); Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CODEX-EXTCMDS
- `/logout` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: sign out of Codex; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-DEVCMDS
- `/mcp` - Kind: built-in; Surface: CLI, IDE extension; Args: optional verbose or login name; Aliases: none; Purpose: list configured MCP tools; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-EXTCMDS
- `/memories` - Kind: built-in; Surface: CLI, IDE extension; Args: none; Aliases: none; Purpose: configure memory use and generation; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-EXTCMDS
- `/mention` - Kind: built-in; Surface: CLI; Args: path; Aliases: none; Purpose: highlight and add a file to the chat; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-DEVCMDS
- `/model` - Kind: built-in; Surface: CLI, IDE extension; Args: optional model and reasoning/speed flags; Aliases: none; Purpose: choose or set the active model and reasoning effort; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-EXTCMDS
- `/new` - Kind: built-in; Surface: CLI; Args: optional name; Aliases: none; Purpose: start a new chat in the same CLI session; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-DEVCMDS
- `/pet` - Kind: alias; Surface: CLI; Args: none; Aliases: /pets; Purpose: alias of /pets; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC
- `/pets` - Kind: built-in; Surface: CLI; Args: none/off; Aliases: /pet; Purpose: choose or hide the terminal pet; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-DEVCMDS
- `/plan` - Kind: built-in; Surface: CLI, IDE extension; Args: optional inline prompt; Aliases: none; Purpose: switch to plan mode; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-EXTCMDS
- `/plugins` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: manage plugins; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-DEVCMDS
- `/presets` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: run or save reusable prompts and slash commands; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-DEVCMDS
- `/project` - Kind: built-in; Surface: IDE extension; Args: none; Aliases: none; Purpose: project-related command (extension surface only); Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CODEX-EXTCMDS
- `/ps` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: list background terminals; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-DEVCMDS
- `/pwd` - Kind: built-in; Surface: CLI; Args: none; Aliases: /cwd; Purpose: show the current working directory; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-DEVCMDS
- `/quit` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: exit Codex immediately; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-DEVCMDS
- `/raw` - Kind: built-in; Surface: CLI; Args: optional on/off; Aliases: none; Purpose: toggle raw scrollback mode for copy-friendly terminal selection; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-DEVCMDS
- `/reasoning` - Kind: built-in; Surface: IDE extension; Args: none; Aliases: none; Purpose: open the reasoning effort picker (extension surface only); Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CODEX-EXTCMDS
- `/recap` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: summarize the current conversation now; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-DEVCMDS
- `/rename` - Kind: built-in; Surface: CLI; Args: optional name; Aliases: none; Purpose: rename the current chat; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-DEVCMDS
- `/review` - Kind: built-in; Surface: CLI, IDE extension; Args: none; Aliases: none; Purpose: ask for a working tree review; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-EXTCMDS
- `/rollout` - Kind: hidden; Surface: CLI; Args: none; Aliases: none; Purpose: print the rollout file path, only visible in debug builds; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC
- `/setup-default-sandbox` - Kind: conditional; Surface: CLI; Args: none; Aliases: none; Purpose: set up the elevated Windows sandbox; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-DEVCMDS
- `/side` - Kind: built-in; Surface: CLI; Args: optional inline text; Aliases: none; Purpose: start a side conversation; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-DEVCMDS
- `/skills` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: pick a skill to apply to the next request; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-DEVCMDS
- `/status` - Kind: built-in; Surface: CLI, IDE extension; Args: none; Aliases: none; Purpose: show current session configuration and token usage; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-EXTCMDS
- `/statusline` - Kind: built-in; Surface: CLI; Args: optional items or --clear; Aliases: none; Purpose: configure footer status-line items; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-DEVCMDS
- `/stop` - Kind: built-in; Surface: CLI; Args: none; Aliases: /clean; Purpose: stop all background terminals; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-DEVCMDS
- `/subagents` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: switch the active subagent thread; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-DEVCMDS
- `/test-approval` - Kind: hidden; Surface: CLI; Args: none; Aliases: none; Purpose: test approval request, only visible in debug builds; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC
- `/theme` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: choose a syntax highlighting theme; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-DEVCMDS
- `/title` - Kind: built-in; Surface: CLI; Args: optional items or --clear; Aliases: none; Purpose: configure terminal title items; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-DEVCMDS
- `/tui` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: choose the TUI mode for the next launch; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-DEVCMDS
- `/usage` - Kind: built-in; Surface: CLI; Args: optional daily/weekly/cumulative; Aliases: none; Purpose: view account usage or redeem an earned reset; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-DEVCMDS
- `/vim` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: toggle composer Vim mode; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-DEVCMDS
- `/voice` - Kind: built-in; Surface: CLI; Args: optional mute/stop/settings; Aliases: none; Purpose: start or stop a voice conversation; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-DEVCMDS
- `/warnings` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: show retained warnings and diagnostic details; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-DEVCMDS
- `/worktree` - Kind: built-in; Surface: CLI, IDE extension; Args: none; Aliases: none; Purpose: continue the conversation in a new Git worktree; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CODEX-SLSSRC, SLASHCMDS-IN01-SC-CODEX-EXTCMDS

**Collision rule**: Custom slash commands are not documented for Codex CLI; the built-in `SlashCommand` enum is the authoritative registry and built-ins win. Vendor skills use the `/skills` picker but do not override built-in names.

**Searched, not found**

- Searched `codex-rs/tui/src/slash_command.rs` for the complete enum; no additional built-in keywords beyond the 58 variants.
- Searched the CLI source tree for literal `/help`, `/clear`, `/context` strings; slash commands are not duplicated in user-facing string tables.
- Searched `docs/slash_commands.md`; it only links to the online developer-commands reference.
- Searched `https://learn.chatgpt.com/docs/reference/slash-commands` and `https://learn.chatgpt.com/docs/developer-commands` for a Codex-specific desktop app slash-command catalog; the desktop app composer is documented as the ChatGPT desktop composer, and no Codex-specific desktop keywords were identified.
- Searched `https://developers.openai.com/codex` and web for a standalone Codex web slash-command surface; no vendor-published Codex web `/` command inventory was found.

**Status**: COMPLETE 2026-11-17

## 12. Agent: Gemini CLI

**Product facts**: Google Gemini CLI (`gemini` terminal agent) and its IDE integration. Surfaces covered: Gemini CLI interactive terminal. Repository `https://github.com/google-gemini/gemini-cli.git`, checked commit `4fa64e71b9b4e1bb65a86cc2863574f561b82340` (`main` HEAD, describe `4fa64e7`), accessed 2026-11-17. Built-in commands are loaded by `packages/cli/src/services/BuiltinCommandLoader.ts` from command modules in `packages/cli/src/ui/commands/`.

**Keywords**

- `/?` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: display help information; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-GMNCLI-CMDREF
- `/about` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: show version info; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR, SLASHCMDS-IN01-SC-GMNCLI-CMDREF
- `/agents` - Kind: conditional; Surface: CLI; Args: subcommand list/reload/refresh/enable/disable/config; Aliases: none; Purpose: manage local and remote subagents, shown only when agents are enabled; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR, SLASHCMDS-IN01-SC-GMNCLI-CMDREF
- `/auth` - Kind: built-in; Surface: CLI; Args: subcommand signin/login or signout/logout; Aliases: none; Purpose: manage authentication; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR, SLASHCMDS-IN01-SC-GMNCLI-CMDREF
- `/background` - Kind: alias; Surface: CLI; Args: none; Aliases: /tasks; Purpose: alias of /tasks that toggles background tasks view; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR
- `/bg` - Kind: alias; Surface: CLI; Args: none; Aliases: /tasks; Purpose: alias of /tasks; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR
- `/bug` - Kind: built-in; Surface: CLI; Args: optional headline; Aliases: none; Purpose: submit a bug report; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR, SLASHCMDS-IN01-SC-GMNCLI-CMDREF
- `/bug-memory` - Kind: hidden; Surface: CLI; Args: none; Aliases: none; Purpose: capture a V8 heap snapshot for a bug report, present in source but absent from docs; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR
- `/chat` - Kind: built-in; Surface: CLI; Args: subcommand list/save/resume/load/delete/share/debug; Aliases: none; Purpose: browse auto-saved conversations and manage chat checkpoints; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR, SLASHCMDS-IN01-SC-GMNCLI-CMDREF
- `/clear` - Kind: built-in; Surface: CLI; Args: none; Aliases: /new; Purpose: clear the screen and start a new session; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR, SLASHCMDS-IN01-SC-GMNCLI-CMDREF
- `/commands` - Kind: built-in; Surface: CLI; Args: subcommand list or reload/refresh; Aliases: none; Purpose: manage custom slash commands loaded from .toml files; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR, SLASHCMDS-IN01-SC-GMNCLI-CMDREF
- `/compact` - Kind: alias; Surface: CLI; Args: none; Aliases: /compress; Purpose: alias of /compress that compresses context; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR
- `/compress` - Kind: built-in; Surface: CLI; Args: none; Aliases: /summarize, /compact; Purpose: compress the context by replacing it with a summary; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR, SLASHCMDS-IN01-SC-GMNCLI-CMDREF
- `/copy` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: copy the last result or code snippet to clipboard; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR, SLASHCMDS-IN01-SC-GMNCLI-CMDREF
- `/corgi` - Kind: hidden; Surface: CLI; Args: none; Aliases: none; Purpose: toggle corgi mode, marked hidden in source; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR
- `/dir` - Kind: alias; Surface: CLI; Args: none; Aliases: /directory; Purpose: alias of /directory; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR
- `/directory` - Kind: built-in; Surface: CLI; Args: subcommand add or show; Aliases: /dir; Purpose: manage workspace directories; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR, SLASHCMDS-IN01-SC-GMNCLI-CMDREF
- `/docs` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: open Gemini CLI documentation in a browser; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR, SLASHCMDS-IN01-SC-GMNCLI-CMDREF
- `/editor` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: set external editor preference; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR, SLASHCMDS-IN01-SC-GMNCLI-CMDREF
- `/exit` - Kind: alias; Surface: CLI; Args: none; Aliases: /quit; Purpose: alias of /quit that exits the CLI; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR
- `/export-session` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: export the current session to a JSON file; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR, SLASHCMDS-IN01-SC-GMNCLI-CMDREF
- `/extensions` - Kind: conditional; Surface: CLI; Args: subcommand config/disable/enable/explore/install/link/list/restart/uninstall/update; Aliases: none; Purpose: manage extensions, shown only when extensions are enabled; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR, SLASHCMDS-IN01-SC-GMNCLI-CMDREF
- `/footer` - Kind: built-in; Surface: CLI; Args: none; Aliases: /statusline; Purpose: configure footer status-line items; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR
- `/gemma` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: check local Gemma model routing status; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR, SLASHCMDS-IN01-SC-GMNCLI-CMDREF
- `/help` - Kind: built-in; Surface: CLI; Args: optional topic; Aliases: none; Purpose: show help for gemini-cli; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR, SLASHCMDS-IN01-SC-GMNCLI-CMDREF
- `/history` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: view session history; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR
- `/hooks` - Kind: conditional; Surface: CLI; Args: subcommand list/show/panel, enable/disable, enable-all/disable-all; Aliases: none; Purpose: manage lifecycle hooks, shown only when hooks UI is enabled; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR, SLASHCMDS-IN01-SC-GMNCLI-CMDREF
- `/ide` - Kind: conditional; Surface: CLI; Args: subcommand disable/enable/install/status; Aliases: none; Purpose: manage IDE integration, shown only when an IDE companion is detected; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR, SLASHCMDS-IN01-SC-GMNCLI-CMDREF
- `/init` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: analyze the project and create a tailored GEMINI.md file; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR, SLASHCMDS-IN01-SC-GMNCLI-CMDREF
- `/mcp` - Kind: conditional; Surface: CLI; Args: subcommand list/ls/nodesc/nodescription/desc/description/disable/enable/reload/refresh/auth/schema; Aliases: none; Purpose: manage configured MCP servers, shown only when MCP is enabled; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR, SLASHCMDS-IN01-SC-GMNCLI-CMDREF
- `/memory` - Kind: built-in; Surface: CLI; Args: subcommand list/reload/refresh/show; Aliases: none; Purpose: manage hierarchical memory loaded from GEMINI.md files; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR, SLASHCMDS-IN01-SC-GMNCLI-CMDREF
- `/model` - Kind: built-in; Surface: CLI; Args: subcommand manage or set; Aliases: none; Purpose: manage model configuration; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR, SLASHCMDS-IN01-SC-GMNCLI-CMDREF
- `/new` - Kind: alias; Surface: CLI; Args: none; Aliases: /clear; Purpose: alias of /clear that starts a new session; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR
- `/oncall` - Kind: hidden; Surface: CLI; Args: none; Aliases: none; Purpose: oncall helper, shown only in nightly builds and absent from docs; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR
- `/permissions` - Kind: conditional; Surface: CLI; Args: subcommand trust; Aliases: none; Purpose: manage folder trust and other permissions, shown only when folder trust is enabled; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR, SLASHCMDS-IN01-SC-GMNCLI-CMDREF
- `/plan` - Kind: conditional; Surface: CLI; Args: subcommand copy; Aliases: none; Purpose: switch to Plan Mode and view the current plan, shown only when plan mode is enabled; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR, SLASHCMDS-IN01-SC-GMNCLI-CMDREF
- `/policies` - Kind: built-in; Surface: CLI; Args: subcommand list; Aliases: none; Purpose: manage policies; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR, SLASHCMDS-IN01-SC-GMNCLI-CMDREF
- `/privacy` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: display the privacy notice; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR, SLASHCMDS-IN01-SC-GMNCLI-CMDREF
- `/profile` - Kind: hidden; Surface: CLI; Args: none; Aliases: none; Purpose: profile helper, shown only in development builds and absent from docs; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR
- `/quit` - Kind: built-in; Surface: CLI; Args: optional --delete; Aliases: /exit; Purpose: exit Gemini CLI; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR, SLASHCMDS-IN01-SC-GMNCLI-CMDREF
- `/restore` - Kind: conditional; Surface: CLI; Args: optional tool_call_id; Aliases: none; Purpose: restore project files to a checkpoint, shown only when checkpointing is enabled; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR, SLASHCMDS-IN01-SC-GMNCLI-CMDREF
- `/resume` - Kind: built-in; Surface: CLI; Args: subcommand list/save/resume/load/delete/share/debug; Aliases: none; Purpose: browse and resume previous sessions and manage checkpoints; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR, SLASHCMDS-IN01-SC-GMNCLI-CMDREF
- `/rewind` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: navigate backward through conversation history; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR, SLASHCMDS-IN01-SC-GMNCLI-CMDREF
- `/settings` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: open the settings editor; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR, SLASHCMDS-IN01-SC-GMNCLI-CMDREF
- `/setup-github` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: set up GitHub Actions to triage issues and review PRs; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR, SLASHCMDS-IN01-SC-GMNCLI-CMDREF
- `/shortcuts` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: toggle the shortcuts panel above the input; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR
- `/skills` - Kind: conditional; Surface: CLI; Args: subcommand list/enable/disable/reload/refresh; Aliases: none; Purpose: manage agent skills, shown only when skills support is enabled; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR, SLASHCMDS-IN01-SC-GMNCLI-CMDREF
- `/stats` - Kind: built-in; Surface: CLI; Args: subcommand session/model/tools/heatmap; Aliases: /usage; Purpose: display session statistics; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR, SLASHCMDS-IN01-SC-GMNCLI-CMDREF
- `/statusline` - Kind: alias; Surface: CLI; Args: none; Aliases: /footer; Purpose: alias of /footer; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR
- `/summarize` - Kind: alias; Surface: CLI; Args: none; Aliases: /compress; Purpose: alias of /compress; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR
- `/tasks` - Kind: built-in; Surface: CLI; Args: none; Aliases: /bg, /background; Purpose: toggle background tasks view; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR
- `/terminal-setup` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: configure terminal keybindings for multiline input in VS Code, Cursor, Windsurf; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR, SLASHCMDS-IN01-SC-GMNCLI-CMDREF
- `/theme` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: change the visual theme; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR, SLASHCMDS-IN01-SC-GMNCLI-CMDREF
- `/tools` - Kind: built-in; Surface: CLI; Args: subcommand list/desc/descriptions; Aliases: none; Purpose: list available Gemini CLI tools; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR, SLASHCMDS-IN01-SC-GMNCLI-CMDREF
- `/upgrade` - Kind: conditional; Surface: CLI; Args: none; Aliases: none; Purpose: open the Gemini Code Assist upgrade page, shown only for Google login; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR, SLASHCMDS-IN01-SC-GMNCLI-CMDREF
- `/usage` - Kind: alias; Surface: CLI; Args: none; Aliases: /stats; Purpose: alias of /stats; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR
- `/vim` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: toggle vim mode on or off; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR, SLASHCMDS-IN01-SC-GMNCLI-CMDREF
- `/voice` - Kind: conditional; Surface: CLI; Args: none; Aliases: none; Purpose: toggle voice dictation mode, shown only when voice is enabled; Label: PROVEN; Src: SLASHCMDS-IN01-SC-GMNCLI-BLTLDR, SLASHCMDS-IN01-SC-GMNCLI-CMDREF

**Collision rule**: Custom slash commands loaded from `.toml` files, MCP prompts, and extension commands are resolved by `SlashCommandResolver`; when two commands share a name, the conflict is emitted as telemetry and the loser is renamed with a source-specific prefix so the built-in name remains reachable.

**Searched, not found**

- Searched `packages/cli/src/services/BuiltinCommandLoader.ts` for the complete built-in loader list; no additional top-level built-ins beyond those recorded.
- Searched `docs/reference/commands.md` for `/shells` and `/bashes`; the docs list them, but no corresponding command was found in the code loader or command modules.
- Searched `docs/reference/commands.md` for `/nodesc` and `/nodescriptions` under `/tools`; listed in docs but no subcommand of that name in `packages/cli/src/ui/commands/toolsCommand.ts`.

**Status**: COMPLETE 2026-11-17

## 13. Agent: OpenCode

**Product facts**: OpenCode open-source terminal agent at `https://opencode.ai` and its desktop/IDE clients. Surfaces covered: Terminal User Interface (TUI) and the desktop/IDE client (`packages/app`). Repository identity verified: `https://github.com/anomalyco/opencode.git`, checked commit `887f6cd44bbb5e68826ef53e76047b7e9e34c3ca` (`dev` HEAD, describe `887f6cd`), accessed 2026-11-17. TUI slash commands are declared in `packages/tui/src/app.tsx`, `packages/tui/src/component/prompt/index.tsx`, and feature plugins. Desktop/IDE slash commands are declared in `packages/app/src/composer/commands.tsx` and `packages/app/src/session/commands/use-session-commands.tsx`. Server-provided built-ins are registered in `packages/core/src/plugin/command.ts`.

**Keywords**

- `/agent` - Kind: built-in; Surface: Desktop/IDE; Args: none; Aliases: none; Purpose: cycle to the next agent in the desktop composer; Label: PROVEN; Src: SLASHCMDS-IN01-SC-OPNCD-APPCMD
- `/agents` - Kind: built-in; Surface: TUI; Args: none; Aliases: none; Purpose: open the agent picker in the TUI; Label: PROVEN; Src: SLASHCMDS-IN01-SC-OPNCD-TUIAPP, SLASHCMDS-IN01-SC-OPNCD-CHTSH
- `/btw` - Kind: built-in; Surface: TUI; Args: question text; Aliases: none; Purpose: ask a one-shot side question without adding to the conversation; Label: PROVEN; Src: SLASHCMDS-IN01-SC-OPNCD-TUIBTW, SLASHCMDS-IN01-SC-OPNCD-TUIDOC
- `/cd` - Kind: built-in; Surface: TUI; Args: path; Aliases: none; Purpose: change the session working directory; Label: PROVEN; Src: SLASHCMDS-IN01-SC-OPNCD-TUIPRM
- `/clear` - Kind: built-in; Surface: TUI; Args: none; Aliases: none; Purpose: clear the current TUI session and start fresh; Label: PROVEN; Src: SLASHCMDS-IN01-SC-OPNCD-TUIAPP, SLASHCMDS-IN01-SC-OPNCD-CHTSH
- `/compact` - Kind: built-in; Surface: Desktop/IDE; Args: none; Aliases: /summarize; Purpose: summarize the session to free context space; Label: PROVEN; Src: SLASHCMDS-IN01-SC-OPNCD-APPSES, SLASHCMDS-IN01-SC-OPNCD-CHTSH
- `/connect` - Kind: built-in; Surface: TUI, Desktop/IDE; Args: none; Aliases: none; Purpose: add a model provider or integration; Label: PROVEN; Src: SLASHCMDS-IN01-SC-OPNCD-TUIAPP, SLASHCMDS-IN01-SC-OPNCD-APPCMD, SLASHCMDS-IN01-SC-OPNCD-CHTSH
- `/continue` - Kind: alias; Surface: TUI; Args: none; Aliases: /sessions; Purpose: alias of /sessions that lists and switches sessions; Label: PROVEN; Src: SLASHCMDS-IN01-SC-OPNCD-TUIAPP
- `/debug` - Kind: built-in; Surface: TUI; Args: none; Aliases: none; Purpose: open the debug info dialog; Label: PROVEN; Src: SLASHCMDS-IN01-SC-OPNCD-TUIAPP
- `/details` - Kind: built-in; Surface: TUI; Args: none; Aliases: none; Purpose: toggle inline tool execution details; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-OPNCD-CHTSH
- `/editor` - Kind: built-in; Surface: TUI; Args: none; Aliases: none; Purpose: compose the current prompt in the external editor set in EDITOR/VISUAL; Label: PROVEN; Src: SLASHCMDS-IN01-SC-OPNCD-TUIPRM, SLASHCMDS-IN01-SC-OPNCD-CHTSH
- `/effort` - Kind: alias; Surface: TUI; Args: none; Aliases: /variants; Purpose: alias of /variants that opens the model variant picker; Label: PROVEN; Src: SLASHCMDS-IN01-SC-OPNCD-TUIAPP
- `/exit` - Kind: built-in; Surface: TUI; Args: none; Aliases: /quit, /q; Purpose: exit the TUI; Label: PROVEN; Src: SLASHCMDS-IN01-SC-OPNCD-TUIAPP, SLASHCMDS-IN01-SC-OPNCD-CHTSH
- `/export` - Kind: built-in; Surface: Desktop/IDE; Args: none; Aliases: none; Purpose: export the current conversation; Label: PROVEN; Src: SLASHCMDS-IN01-SC-OPNCD-APPSES
- `/fork` - Kind: built-in; Surface: Desktop/IDE; Args: none; Aliases: none; Purpose: fork the current session; Label: PROVEN; Src: SLASHCMDS-IN01-SC-OPNCD-APPSES
- `/help` - Kind: built-in; Surface: TUI; Args: none; Aliases: none; Purpose: show the TUI help dialog; Label: PROVEN; Src: SLASHCMDS-IN01-SC-OPNCD-TUIAPP, SLASHCMDS-IN01-SC-OPNCD-CHTSH
- `/highlights` - Kind: conditional; Surface: TUI; Args: none; Aliases: none; Purpose: show release highlights again, shown only when highlights exist; Label: PROVEN; Src: SLASHCMDS-IN01-SC-OPNCD-TUIAPP, SLASHCMDS-IN01-SC-OPNCD-TUIDOC
- `/init` - Kind: built-in; Surface: TUI; Args: none; Aliases: none; Purpose: guided setup for creating or updating project-level AGENTS.md; Label: PROVEN; Src: SLASHCMDS-IN01-SC-OPNCD-CORCMD, SLASHCMDS-IN01-SC-OPNCD-CHTSH
- `/mcp` - Kind: built-in; Surface: Desktop/IDE; Args: none; Aliases: none; Purpose: open the MCP server picker in the desktop composer; Label: PROVEN; Src: SLASHCMDS-IN01-SC-OPNCD-APPSES
- `/mcps` - Kind: built-in; Surface: TUI; Args: none; Aliases: none; Purpose: list configured MCP servers in the TUI; Label: PROVEN; Src: SLASHCMDS-IN01-SC-OPNCD-TUIAPP, SLASHCMDS-IN01-SC-OPNCD-CHTSH
- `/model` - Kind: built-in; Surface: Desktop/IDE; Args: none; Aliases: none; Purpose: open the model picker in the desktop composer; Label: PROVEN; Src: SLASHCMDS-IN01-SC-OPNCD-APPCMD
- `/models` - Kind: built-in; Surface: TUI; Args: none; Aliases: none; Purpose: open the model picker in the TUI; Label: PROVEN; Src: SLASHCMDS-IN01-SC-OPNCD-TUIAPP, SLASHCMDS-IN01-SC-OPNCD-CHTSH
- `/new` - Kind: built-in; Surface: TUI, Desktop/IDE; Args: none; Aliases: none; Purpose: start a new session; Label: PROVEN; Src: SLASHCMDS-IN01-SC-OPNCD-TUIAPP, SLASHCMDS-IN01-SC-OPNCD-APPSES, SLASHCMDS-IN01-SC-OPNCD-CHTSH
- `/open` - Kind: built-in; Surface: TUI, Desktop/IDE; Args: none; Aliases: /projects, /project; Purpose: open the session or project picker; Label: PROVEN; Src: SLASHCMDS-IN01-SC-OPNCD-TUIAPP, SLASHCMDS-IN01-SC-OPNCD-APPSES
- `/pair` - Kind: built-in; Surface: TUI; Args: none; Aliases: /web; Purpose: open the device-pairing dialog; Label: PROVEN; Src: SLASHCMDS-IN01-SC-OPNCD-TUIAPP
- `/project` - Kind: alias; Surface: TUI; Args: none; Aliases: /open; Purpose: alias of /open for projects; Label: PROVEN; Src: SLASHCMDS-IN01-SC-OPNCD-TUIAPP
- `/projects` - Kind: alias; Surface: TUI; Args: none; Aliases: /open; Purpose: alias of /open for projects; Label: PROVEN; Src: SLASHCMDS-IN01-SC-OPNCD-TUIAPP
- `/q` - Kind: alias; Surface: TUI; Args: none; Aliases: /exit; Purpose: alias of /exit; Label: PROVEN; Src: SLASHCMDS-IN01-SC-OPNCD-TUIAPP
- `/quit` - Kind: alias; Surface: TUI; Args: none; Aliases: /exit; Purpose: alias of /exit; Label: PROVEN; Src: SLASHCMDS-IN01-SC-OPNCD-TUIAPP
- `/redo` - Kind: built-in; Surface: Desktop/IDE; Args: none; Aliases: none; Purpose: restore a message and file changes after /undo; Label: PROVEN; Src: SLASHCMDS-IN01-SC-OPNCD-APPSES
- `/reload` - Kind: built-in; Surface: TUI, Desktop/IDE; Args: none; Aliases: none; Purpose: reload configuration without restarting; Label: PROVEN; Src: SLASHCMDS-IN01-SC-OPNCD-TUIAPP, SLASHCMDS-IN01-SC-OPNCD-APPCMD
- `/restart` - Kind: conditional; Surface: TUI; Args: none; Aliases: none; Purpose: restart the OpenCode service, shown only when client.restart is available; Label: PROVEN; Src: SLASHCMDS-IN01-SC-OPNCD-TUIAPP
- `/resume` - Kind: alias; Surface: TUI; Args: none; Aliases: /sessions; Purpose: alias of /sessions that lists and switches sessions; Label: PROVEN; Src: SLASHCMDS-IN01-SC-OPNCD-TUIAPP
- `/review` - Kind: built-in; Surface: TUI; Args: target; Aliases: none; Purpose: review a file or change using the built-in review command; Label: PROVEN; Src: SLASHCMDS-IN01-SC-OPNCD-CORCMD
- `/sessions` - Kind: built-in; Surface: TUI; Args: none; Aliases: /resume, /continue; Purpose: list and switch between sessions; Label: PROVEN; Src: SLASHCMDS-IN01-SC-OPNCD-TUIAPP, SLASHCMDS-IN01-SC-OPNCD-CHTSH
- `/settings` - Kind: built-in; Surface: TUI; Args: none; Aliases: none; Purpose: open the TUI settings dialog; Label: PROVEN; Src: SLASHCMDS-IN01-SC-OPNCD-TUIAPP
- `/share` - Kind: built-in; Surface: TUI; Args: none; Aliases: none; Purpose: share the current session as a public link; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-OPNCD-CHTSH
- `/skills` - Kind: built-in; Surface: TUI; Args: none; Aliases: none; Purpose: open the skill picker; Label: PROVEN; Src: SLASHCMDS-IN01-SC-OPNCD-TUIPRM
- `/status` - Kind: built-in; Surface: TUI; Args: none; Aliases: none; Purpose: open the status dialog; Label: PROVEN; Src: SLASHCMDS-IN01-SC-OPNCD-TUIAPP, SLASHCMDS-IN01-SC-OPNCD-CHTSH
- `/summarize` - Kind: alias; Surface: TUI; Args: none; Aliases: /compact; Purpose: alias of /compact; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-OPNCD-CHTSH
- `/terminal` - Kind: built-in; Surface: TUI; Args: none; Aliases: none; Purpose: open a new terminal tab in the TUI; Label: PROVEN; Src: SLASHCMDS-IN01-SC-OPNCD-TUIAPP
- `/themes` - Kind: built-in; Surface: TUI; Args: none; Aliases: none; Purpose: open the theme picker; Label: PROVEN; Src: SLASHCMDS-IN01-SC-OPNCD-TUIAPP, SLASHCMDS-IN01-SC-OPNCD-CHTSH
- `/thinking` - Kind: alias; Surface: TUI; Args: none; Aliases: /variants; Purpose: alias of /variants that opens the model variant picker; Label: PROVEN; Src: SLASHCMDS-IN01-SC-OPNCD-TUIAPP
- `/undo` - Kind: built-in; Surface: Desktop/IDE; Args: none; Aliases: none; Purpose: revert the last user message and any file changes; Label: PROVEN; Src: SLASHCMDS-IN01-SC-OPNCD-APPSES, SLASHCMDS-IN01-SC-OPNCD-CHTSH
- `/unshare` - Kind: built-in; Surface: TUI; Args: none; Aliases: none; Purpose: stop sharing the current session; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-OPNCD-CHTSH
- `/update` - Kind: conditional; Surface: TUI; Args: none; Aliases: none; Purpose: open the OpenCode update flow, shown only when updater.open is available; Label: PROVEN; Src: SLASHCMDS-IN01-SC-OPNCD-TUIAPP
- `/usage` - Kind: built-in; Surface: TUI; Args: none; Aliases: none; Purpose: open the usage dialog; Label: PROVEN; Src: SLASHCMDS-IN01-SC-OPNCD-TUIAPP
- `/variants` - Kind: built-in; Surface: TUI; Args: none; Aliases: /thinking, /effort; Purpose: open the model variant picker; Label: PROVEN; Src: SLASHCMDS-IN01-SC-OPNCD-TUIAPP
- `/web` - Kind: alias; Surface: TUI; Args: none; Aliases: /pair; Purpose: alias of /pair; Label: PROVEN; Src: SLASHCMDS-IN01-SC-OPNCD-TUIAPP
- `/worktrees` - Kind: built-in; Surface: TUI; Args: none; Aliases: none; Purpose: open the workspace management dialog; Label: PROVEN; Src: SLASHCMDS-IN01-SC-OPNCD-TUIPRM

**Collision rule**: Custom commands are defined in `~/.config/opencode/commands/` or `.opencode/commands/` and in `opencode.json`; the client resolves slash commands against built-ins first (`slashCommands` memo in `packages/app/src/composer/model.ts`), so a built-in name wins over a custom command.

**Searched, not found**

- Searched `packages/tui/src/app.tsx` and `packages/tui/src/component/prompt/index.tsx` for every `slash:` declaration; all built-in TUI commands are recorded.
- Searched `packages/app/src/composer/commands.tsx` and `packages/app/src/session/commands/use-session-commands.tsx` for every `slash:` declaration; all built-in desktop/IDE commands are recorded.
- Searched the TUI source for `/share`, `/unshare`, `/details`, and `/summarize`; no matching `slash:` declaration was found in commit `887f6cd`, so those four entries are documented from the public cheatsheet only.

**Status**: COMPLETE 2026-11-17

## 14. Agent: Windsurf (Cascade)

**Product facts**: Codeium Windsurf agentic IDE with Cascade chat panel. Surfaces covered: Windsurf IDE, Devin Desktop (also branded as Windsurf), and the JetBrains plugin. Latest stable version checked from changelog: v3.13.4 (2026-11-17); Next build v3.13.1004 (2026-11-17). `C:\Users\User\AppData\Local\Programs\Windsurf Next\` is installed but contains no executable and only extensions resources, so no local `[TESTED]` observations were possible. Devin Desktop `C:\Users\User\AppData\Local\Programs\Devin\` is also installed and identified as the same product line.

**Keywords**

- `/explain` - Kind: built-in; Surface: IDE, JetBrains plugin; Args: message; Aliases: none; Purpose: ask Cascade to explain the selected or referenced code; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-WNDSRF-CHATDOC
- `/model` - Kind: built-in; Surface: IDE, Devin Desktop, JetBrains plugin; Args: none; Aliases: none; Purpose: open the model selector; Label: ASSUMED; Src: SLASHCMDS-IN01-SC-WNDSRF-SHORT
- `/plan` - Kind: bundled; Surface: IDE, Devin Desktop, JetBrains plugin; Args: none; Aliases: none; Purpose: run the built-in plan workflow to switch to Plan mode; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-WNDSRF-SHORT, SLASHCMDS-IN01-SC-WNDSRF-WF

**Collision rule**: User-defined workflows in `.windsurf/workflows/` and `~/.codeium/windsurf/global_workflows/` are invoked as `/<workflow-name>`. They are loaded into the slash menu but are excluded from the built-in keyword list; if a workflow name matches a built-in name, the built-in command is highlighted first and wins.

**Searched, not found**

- Searched `https://docs.windsurf.com/llms-full.txt` (Chat Overview section); it states `/explain` is the only supported slash command, conflicting with other sources that list `/plan` and `/model`.
- Searched `https://docs.devin.ai/windsurf/plugins/cascade/workflows` and `https://docs.devin.ai/desktop/changelog-next`; workflows are user-defined and excluded; `/plan` is documented as a built-in workflow.
- Searched the local Windsurf Next installation `C:\Users\User\AppData\Local\Programs\Windsurf Next\` for executable and slash-command registry; no runnable binary or unminified source was found.
- Searched the local Devin Desktop installation `C:\Users\User\AppData\Local\Programs\Devin\resources\app` with `rg.exe`; source is minified and no additional built-in slash commands were extracted.

**Status**: COMPLETE 2026-11-17

## 15. Agent: Cline

**Product facts**: Cline coding agent. Surfaces covered: VS Code extension, JetBrains port, and Cline CLI. Repository `https://github.com/cline/cline.git`, checked commit `4cdfb19a5e897b9e75827cbb4f280f322e27e44a` (`main` HEAD, describe `4cdfb19`), accessed 2026-11-17. CLI built-in slash commands are registered in `apps/cli/src/tui/commands/slash-command-registry.ts`. VS Code webview slash commands are built from `apps/vscode/src/shared/slashCommands.ts` plus workflow and MCP prompt commands. SDK runtime built-ins are declared in `apps/vscode/src/sdk/builtin-slash-commands.ts`.

**Keywords**

- `/account` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: view Cline account information; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CLINE-CLIREG
- `/act` - Kind: built-in; Surface: VS Code extension; Args: none; Aliases: none; Purpose: switch to Act mode; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLINE-SKILL
- `/clear` - Kind: built-in; Surface: CLI, VS Code extension; Args: none; Aliases: none; Purpose: clear the conversation; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CLINE-CLIREG, SLASHCMDS-IN01-SC-CLINE-SKILL
- `/compact` - Kind: built-in; Surface: CLI, VS Code extension; Args: none; Aliases: /smol, /newtask; Purpose: condense the current context window; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CLINE-CLIREG, SLASHCMDS-IN01-SC-CLINE-VSCMDS
- `/config` - Kind: hidden; Surface: CLI; Args: none; Aliases: /settings; Purpose: hidden alias of /settings for agent configuration; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CLINE-CLIREG
- `/deep-planning` - Kind: built-in; Surface: VS Code extension; Args: none; Aliases: none; Purpose: run an extended planning session that creates implementation_plan.md; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CLINE-VSCMDS, SLASHCMDS-IN01-SC-CLINE-BUILTIN, SLASHCMDS-IN01-SC-CLINE-DOCS
- `/fork` - Kind: built-in; Surface: CLI; Args: optional name; Aliases: none; Purpose: create a named fork of the current session; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CLINE-CLIREG
- `/help` - Kind: built-in; Surface: CLI, VS Code extension; Args: none; Aliases: none; Purpose: show available commands; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CLINE-CLIREG, SLASHCMDS-IN01-SC-CLINE-SKILL
- `/history` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: view session history; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CLINE-CLIREG
- `/mcp` - Kind: built-in; Surface: CLI, VS Code extension; Args: none; Aliases: none; Purpose: manage MCP servers; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CLINE-CLIREG
- `/model` - Kind: built-in; Surface: CLI, VS Code extension; Args: none; Aliases: none; Purpose: switch model or provider; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CLINE-CLIREG, SLASHCMDS-IN01-SC-CLINE-SKILL
- `/newrule` - Kind: hidden; Surface: VS Code extension; Args: none; Aliases: none; Purpose: create a .clinerules file interactively, hidden until the prompt expansion is ported to the SDK runtime; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CLINE-VSCMDS, SLASHCMDS-IN01-SC-CLINE-DOCS
- `/newtask` - Kind: alias; Surface: VS Code extension; Args: none; Aliases: /compact; Purpose: alias of /compact that starts a fresh task with distilled context; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CLINE-VSCMDS, SLASHCMDS-IN01-SC-CLINE-DOCS
- `/plan` - Kind: built-in; Surface: VS Code extension; Args: none; Aliases: none; Purpose: switch to Plan mode; Label: VERIFIED; Src: SLASHCMDS-IN01-SC-CLINE-SKILL
- `/plugins` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: manage plugins; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CLINE-CLIREG
- `/quit` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: exit the Cline CLI; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CLINE-CLIREG
- `/reportbug` - Kind: hidden; Surface: VS Code extension; Args: none; Aliases: none; Purpose: report a bug with diagnostic info, hidden until the prompt expansion is ported to the SDK runtime; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CLINE-VSCMDS, SLASHCMDS-IN01-SC-CLINE-DOCS
- `/settings` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: modify agent configuration; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CLINE-CLIREG
- `/skills` - Kind: built-in; Surface: CLI; Args: optional query; Aliases: none; Purpose: browse skills and workflows; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CLINE-CLIREG
- `/smol` - Kind: alias; Surface: VS Code extension; Args: none; Aliases: /compact; Purpose: alias of /compact that compresses conversation history; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CLINE-VSCMDS, SLASHCMDS-IN01-SC-CLINE-DOCS
- `/theme` - Kind: built-in; Surface: CLI; Args: none; Aliases: none; Purpose: change color theme; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CLINE-CLIREG
- `/undo` - Kind: built-in; Surface: CLI, VS Code extension; Args: none; Aliases: none; Purpose: restore to a previous checkpoint; Label: PROVEN; Src: SLASHCMDS-IN01-SC-CLINE-CLIREG, SLASHCMDS-IN01-SC-CLINE-SKILL

**Collision rule**: In the VS Code extension, custom workflow and skill commands are merged into the slash command list in `getMatchingSlashCommands`; if a custom command name conflicts with a built-in name, the built-in appears in `DEFAULT_SLASH_COMMANDS` first and is matched by the prefix filter before user commands. In the CLI, `buildSlashCommandRegistry` deduplicates by normalized name and the first source wins; built-ins are added first.

**Searched, not found**

- Searched `apps/cli/src/tui/commands/slash-command-registry.ts` for the complete `LocalSlashCommandName` union; all 15 CLI local commands are recorded.
- Searched `apps/vscode/src/shared/slashCommands.ts` for `BASE_SLASH_COMMANDS` and `VSCODE_ONLY_COMMANDS`; `VSCODE_ONLY_COMMANDS` is empty and the four base commands are recorded.
- Searched the CLI and VS Code source trees for `/plan` and `/act` slash-command registrations; no source registration was found, so those entries rely on the public Cline Skill document.

**Status**: COMPLETE 2026-11-17

## 16. Cross-Agent Observations

### Keyword clusters with the same name and same meaning

- `/experimental` - 2 agents
- `/history` - 2 agents
- `/reset` - 2 agents

### Same name with different meaning or surface

- `/about` - 2 agents
- `/add-dir` - 4 agents
- `/agent` - 2 agents
- `/agents` - 6 agents
- `/app` - 3 agents
- `/approve` - 2 agents
- `/archive` - 3 agents
- `/ask` - 3 agents
- `/background` - 2 agents
- `/bg` - 2 agents
- `/branch` - 3 agents
- `/btw` - 6 agents
- `/bug` - 3 agents
- `/cd` - 4 agents
- `/changelog` - 2 agents
- `/chat` - 2 agents
- `/clear` - 9 agents
- `/cloud-environment` - 2 agents
- `/cloud` - 3 agents
- `/compact` - 8 agents
- `/compress` - 2 agents
- `/config` - 7 agents
- `/context` - 4 agents
- `/continue` - 4 agents
- `/copy` - 7 agents
- `/cwd` - 2 agents
- `/debug` - 4 agents
- `/delete` - 2 agents
- `/diff` - 4 agents
- `/doc` - 2 agents
- `/editor` - 2 agents
- `/effort` - 3 agents
- `/exit` - 8 agents
- `/explain` - 2 agents
- `/export` - 4 agents
- `/extensions` - 2 agents
- `/fast` - 4 agents
- `/feedback` - 7 agents
- `/fix` - 2 agents
- `/footer` - 2 agents
- `/fork` - 9 agents
- `/goal` - 6 agents
- `/help` - 9 agents
- `/hooks` - 6 agents
- `/ide-context` - 2 agents
- `/ide` - 4 agents
- `/import` - 2 agents
- `/init` - 6 agents
- `/keybindings` - 2 agents
- `/local` - 2 agents
- `/login` - 3 agents
- `/logout` - 5 agents
- `/mcp` - 9 agents
- `/memories` - 2 agents
- `/memory` - 2 agents
- `/model` - 11 agents
- `/models` - 2 agents
- `/new` - 9 agents
- `/open` - 4 agents
- `/permissions` - 4 agents
- `/pet` - 2 agents
- `/plan` - 10 agents
- `/plugin` - 4 agents
- `/plugins` - 3 agents
- `/project` - 3 agents
- `/quit` - 9 agents
- `/reasoning` - 2 agents
- `/recap` - 3 agents
- `/release-notes` - 2 agents
- `/remote-control` - 3 agents
- `/rename` - 7 agents
- `/restart` - 3 agents
- `/resume` - 6 agents
- `/review` - 5 agents
- `/rewind` - 5 agents
- `/run` - 2 agents
- `/sandbox` - 3 agents
- `/schedule` - 2 agents
- `/search` - 2 agents
- `/security-review` - 2 agents
- `/sessions` - 2 agents
- `/settings` - 6 agents
- `/share` - 2 agents
- `/shortcuts` - 2 agents
- `/side` - 2 agents
- `/simplify` - 2 agents
- `/skills` - 7 agents
- `/stats` - 3 agents
- `/status` - 5 agents
- `/statusline` - 4 agents
- `/stop` - 2 agents
- `/subagents` - 2 agents
- `/summarize` - 3 agents
- `/tasks` - 4 agents
- `/terminal-setup` - 3 agents
- `/terminal` - 2 agents
- `/theme` - 6 agents
- `/title` - 3 agents
- `/tui` - 2 agents
- `/undo` - 5 agents
- `/update` - 5 agents
- `/upgrade` - 4 agents
- `/usage` - 8 agents
- `/vim` - 5 agents
- `/voice` - 5 agents
- `/workflows` - 2 agents
- `/worktree` - 3 agents
- `/yolo` - 2 agents

### Surface-specific or agent-specific keywords

- `/?` - only in Gemini CLI
- `/accept-edits` - only in Devin
- `/account` - only in Cline
- `/act` - only in Cline
- `/advisor` - only in Claude Code
- `/af` - only in GitHub Copilot
- `/after` - only in GitHub Copilot
- `/agy-customizations` - only in Google Antigravity
- `/allow-all-tools` - only in GitHub Copilot
- `/allow-all` - only in GitHub Copilot
- `/android` - only in Claude Code
- `/antigravity-guide` - only in Google Antigravity
- `/apps` - only in OpenAI Codex
- `/artifact-capabilities` - only in Claude Code
- `/artifact-diagramming` - only in Claude Code
- `/artifact` - only in Google Antigravity
- `/artifacts` - only in Claude Code
- `/attach-files` - only in GitHub Copilot
- `/attach-folder` - only in GitHub Copilot
- `/auth` - only in Gemini CLI
- `/auto-mode-setup` - only in Claude Code
- `/auto-run` - only in Cursor
- `/autoapprove` - only in GitHub Copilot
- `/autocompact` - only in Claude Code
- `/autofix-pr` - only in Claude Code
- `/automation` - only in Google Antigravity
- `/autonomous` - only in Devin
- `/autopilot` - only in GitHub Copilot
- `/bashes` - only in Claude Code
- `/batch` - only in Claude Code
- `/bedrock` - only in Cursor
- `/boost` - only in Google Antigravity
- `/browser` - only in Google Antigravity
- `/bug-memory` - only in Gemini CLI
- `/bypass` - only in Devin
- `/caffeinate` - only in GitHub Copilot
- `/checkpoint` - only in Claude Code
- `/checkup` - only in Claude Code
- `/chrome` - only in Claude Code
- `/chronicle` - only in GitHub Copilot
- `/claude-api` - only in Claude Code
- `/claude-in-chrome` - only in Claude Code
- `/clean` - only in OpenAI Codex
- `/clikit` - only in GitHub Copilot
- `/code-review` - only in Claude Code
- `/code` - only in Devin
- `/codesearch` - only in Google Antigravity
- `/collect-debug-logs` - only in GitHub Copilot
- `/color` - only in Claude Code
- `/commands` - only in Gemini CLI
- `/commit` - only in Cursor
- `/confetti` - only in Devin
- `/connect` - only in OpenCode
- `/conversation` - only in Google Antigravity
- `/copy-conversation-id` - only in Cursor
- `/copy-request-id` - only in Cursor
- `/corgi` - only in Gemini CLI
- `/cost` - only in Claude Code
- `/create-agent` - only in GitHub Copilot
- `/create-canvas` - only in GitHub Copilot
- `/create-hook` - only in GitHub Copilot
- `/create-instruction` - only in GitHub Copilot
- `/create-prompt` - only in GitHub Copilot
- `/create-skill` - only in GitHub Copilot
- `/credits` - only in Google Antigravity
- `/cs` - only in Google Antigravity
- `/cursor` - only in Cursor
- `/daemon` - only in OpenAI Codex
- `/dangerous` - only in Devin
- `/dataviz` - only in Claude Code
- `/daybreak` - only in OpenAI Codex
- `/debug-config` - only in OpenAI Codex
- `/debug-m-drop` - only in OpenAI Codex
- `/debug-m-update` - only in OpenAI Codex
- `/deep-planning` - only in Cline
- `/deep-research` - only in Claude Code
- `/delegate` - only in GitHub Copilot
- `/design-login` - only in Claude Code
- `/design-sync` - only in Claude Code
- `/design` - only in Claude Code
- `/desktop` - only in Claude Code
- `/details` - only in OpenCode
- `/diagnose` - only in GitHub Copilot
- `/dir` - only in Gemini CLI
- `/directory` - only in Gemini CLI
- `/disableautoapprove` - only in GitHub Copilot
- `/disableyolo` - only in GitHub Copilot
- `/docs` - only in Gemini CLI
- `/doctor` - only in Claude Code
- `/downgrade` - only in GitHub Copilot
- `/env` - only in GitHub Copilot
- `/every` - only in GitHub Copilot
- `/export-gist` - only in GitHub Copilot
- `/export-session` - only in Gemini CLI
- `/extension` - only in GitHub Copilot
- `/fewer-permission-prompts` - only in Claude Code
- `/find` - only in GitHub Copilot
- `/fixtestfailure` - only in GitHub Copilot
- `/fleet` - only in GitHub Copilot
- `/focus` - only in Claude Code
- `/fusion` - only in Devin
- `/gemma` - only in Gemini CLI
- `/generative_ui` - only in Google Antigravity
- `/grill-me` - only in Google Antigravity
- `/handoff` - only in Devin
- `/heapdump` - only in Claude Code
- `/highlights` - only in OpenCode
- `/inbox` - only in GitHub Copilot
- `/insights` - only in Claude Code
- `/install-github-app` - only in Claude Code
- `/install-slack-app` - only in Claude Code
- `/instructions` - only in GitHub Copilot
- `/interactive` - only in GitHub Copilot
- `/ios` - only in Claude Code
- `/jules` - only in Google Jules
- `/keep-alive` - only in GitHub Copilot
- `/keymap` - only in OpenAI Codex
- `/learn` - only in Google Antigravity
- `/limits` - only in GitHub Copilot
- `/line-numbers` - only in Cursor
- `/list-agents` - only in Claude Code
- `/list-dirs` - only in GitHub Copilot
- `/list-sessions` - only in Devin
- `/login-status` - only in Devin
- `/logs` - only in Cursor
- `/loop` - only in Claude Code
- `/ls` - only in Devin
- `/lsp` - only in GitHub Copilot
- `/max-mode` - only in Cursor
- `/mcps` - only in OpenCode
- `/mention` - only in OpenAI Codex
- `/merge-to-parent` - only in GitHub Copilot
- `/mobile` - only in Claude Code
- `/mode` - only in Devin
- `/mouse` - only in Devin
- `/new-chat` - only in Cursor
- `/newchat` - only in Cursor
- `/newrule` - only in Cline
- `/newtask` - only in Cline
- `/normal` - only in Devin
- `/oncall` - only in Gemini CLI
- `/optimize` - only in GitHub Copilot
- `/orchestrate` - only in GitHub Copilot
- `/org` - only in Devin
- `/output-style` - only in Claude Code
- `/pair` - only in OpenCode
- `/passes` - only in Claude Code
- `/peers` - only in Claude Code
- `/pets` - only in OpenAI Codex
- `/pickup` - only in Devin
- `/pin` - only in ChatGPT
- `/platform` - only in Devin
- `/plugin-authoring` - only in Claude Code
- `/policies` - only in Gemini CLI
- `/powerup` - only in Claude Code
- `/pr-comments` - only in Claude Code
- `/pr-fix-checks` - only in GitHub Copilot
- `/pr-merge` - only in GitHub Copilot
- `/pr-open` - only in GitHub Copilot
- `/pr-resolve-comments` - only in GitHub Copilot
- `/pr` - only in GitHub Copilot
- `/presets` - only in OpenAI Codex
- `/privacy-settings` - only in Claude Code
- `/privacy` - only in Gemini CLI
- `/proactive` - only in Claude Code
- `/profile` - only in Gemini CLI
- `/projects` - only in OpenCode
- `/ps` - only in OpenAI Codex
- `/pwd` - only in OpenAI Codex
- `/q` - only in OpenCode
- `/quota` - only in Google Antigravity
- `/radio` - only in Claude Code
- `/rate-limit-options` - only in Claude Code
- `/raw` - only in OpenAI Codex
- `/rc` - only in Claude Code
- `/record` - only in Google Antigravity
- `/redo` - only in OpenCode
- `/refactor` - only in Cursor
- `/refine` - only in GitHub Copilot
- `/reload-plugins` - only in Claude Code
- `/reload-skills` - only in Claude Code
- `/reload` - only in OpenCode
- `/remote-env` - only in Claude Code
- `/remote` - only in GitHub Copilot
- `/remove-dir` - only in Devin
- `/rename-session` - only in Devin
- `/repo` - only in Devin
- `/reportbug` - only in Cline
- `/research` - only in GitHub Copilot
- `/reset-allowed-tools` - only in GitHub Copilot
- `/restart-session` - only in GitHub Copilot
- `/restore` - only in Gemini CLI
- `/revert` - only in Devin
- `/rm-session` - only in Devin
- `/rollout` - only in OpenAI Codex
- `/routines` - only in Claude Code
- `/rubber-duck` - only in GitHub Copilot
- `/run-everything` - only in Cursor
- `/run-skill-generator` - only in Claude Code
- `/run-workflow` - only in Google Antigravity
- `/scroll-speed` - only in Claude Code
- `/session rename` - only in GitHub Copilot
- `/session-stats` - only in Devin
- `/session` - only in GitHub Copilot
- `/setup-bedrock` - only in Claude Code
- `/setup-default-sandbox` - only in OpenAI Codex
- `/setup-github` - only in Gemini CLI
- `/setup-terminal` - only in Cursor
- `/setup-vertex` - only in Claude Code
- `/sh` - only in Cursor
- `/shell` - only in Cursor
- `/show-thinking` - only in Cursor
- `/skill-doctor` - only in Claude Code
- `/slides` - only in Claude Code
- `/smart` - only in Devin
- `/smol` - only in Cline
- `/spar` - only in GitHub Copilot
- `/spawn` - only in GitHub Copilot
- `/ssh` - only in Devin
- `/status-indicators` - only in Cursor
- `/steps` - only in Devin
- `/stickers` - only in Claude Code
- `/subtask` - only in Claude Code
- `/swarm` - only in Google Antigravity
- `/switch` - only in Google Antigravity
- `/team-onboarding` - only in Claude Code
- `/teamwork` - only in Google Antigravity
- `/teleport` - only in Claude Code
- `/test-approval` - only in OpenAI Codex
- `/test` - only in Cursor
- `/tests` - only in GitHub Copilot
- `/themes` - only in OpenCode
- `/thinking` - only in OpenCode
- `/tools` - only in Gemini CLI
- `/tp` - only in Claude Code
- `/tuikit` - only in GitHub Copilot
- `/ultraplan` - only in Claude Code
- `/ultrareview` - only in Claude Code
- `/undo-add-dir` - only in Devin
- `/unshare` - only in OpenCode
- `/update-config` - only in Claude Code
- `/usage-credits` - only in Claude Code
- `/user` - only in GitHub Copilot
- `/variants` - only in OpenCode
- `/verify` - only in Claude Code
- `/version` - only in GitHub Copilot
- `/warnings` - only in OpenAI Codex
- `/web-setup` - only in Claude Code
- `/web` - only in OpenCode
- `/workflow-authoring` - only in Claude Code
- `/workspace` - only in Devin
- `/workspaces` - only in Devin
- `/worktrees` - only in OpenCode

### Agents with no vendor-built-in slash commands

- Google Gemini

### Open limits
- ChatGPT web and mobile slash-command menus are not publicly documented as fixed command lists.
- OpenAI Codex desktop app and Codex web slash commands are not documented separately from the ChatGPT desktop composer; no additional Codex keywords were identified.
- Windsurf (Cascade) `/model` is `[ASSUMED]` pending a second source.
- Cursor IDE agent chat built-ins beyond `/summarize` are not documented by the vendor.

### Agent-surface-keyword diagram

```
Agents                Surfaces                         Keyword counts
---------------------------------------------------------------
ChatGPT              28 ----------------------------
Claude Code          139 --------------------------------------------------
Devin                64 --------------------------------------------------
GitHub Copilot       134 --------------------------------------------------
Google Gemini        0 
Google Jules         1 -
Google Antigravity   60 --------------------------------------------------
Cursor               49 -------------------------------------------------
OpenAI Codex         74 --------------------------------------------------
Gemini CLI           58 --------------------------------------------------
OpenCode             50 --------------------------------------------------
Windsurf (Cascade)   3 ---
Cline                22 ----------------------
Joint list            364
```

## 17. Exclusions

The following mechanisms and products are excluded from the keyword lists because they are user-defined, project-level, plugin-provided, or use a non-slash trigger.

### User-defined and project-level commands

- **ChatGPT**: custom prompts appear as `/prompts:<name>` and enabled skills appear in the slash list; these are user-defined, not built-ins.
- **Claude Code**: custom slash commands loaded from `.toml` files, MCP prompts, and bundled skills are excluded; built-ins win in name collisions.
- **Devin**: organization-defined custom slash commands configured in the web app are excluded; unknown `/` names fail.
- **GitHub Copilot**: custom agents, extensions, and user-defined skills are excluded; built-ins win over custom names.
- **Cursor**: custom slash commands are excluded; IDE commands beyond documented CLI references are not recorded.
- **OpenAI Codex**: vendor skills use the `/skills` picker but do not override built-in names.
- **Gemini CLI**: custom slash commands loaded from `.toml` files, MCP prompts, and extension commands are excluded; built-in names remain reachable after conflict renaming.
- **OpenCode**: server-provided and plugin commands are excluded; only declared TUI/desktop built-ins are recorded.
- **Windsurf (Cascade)**: user-defined workflows invoked as `/<workflow-name>` are excluded.
- **Cline**: custom slash commands and Skills workflows are excluded.

### Non-slash triggers

- `@` mentions for skills, people, files, or extensions in ChatGPT, Gemini, Claude Code, Copilot, Cursor, and OpenCode.
- `$` explicit skill invocation in the ChatGPT desktop composer.
- `#` file references and `!` prompt triggers in some agents are not slash commands.

### Adjacent products

- **Gemini Code Assist** and **Android Studio** assistive features for Google Gemini are adjacent coding products, not the consumer/Workspace chatbot; their slash commands are excluded.
- **GitHub Copilot Chat** inside specific IDEs is covered as a surface of GitHub Copilot, not a separate agent.
- **ChatGPT Work** and the consumer **ChatGPT Classic** app share the same desktop composer commands as ChatGPT and are not separately listed.

## 18. Sources

Sources are listed here with source ID, URL or path, access date, primary finding, and tier. Sources without findings are kept so absence claims are traceable.

### OpenAI Codex

- **SLASHCMDS-IN01-SC-CODEX-SLSSRC** - `e:\dev\IPPS\_PrivateSessions_gitignore\_2026-11-17_AgentSlashCommandKeywords\_download_gitignore\CODEX\codex-rs\tui\src\slash_command.rs`, commit `e20ccdfa80361deb81266d3ed6baea9c2cdd5ee1`; Accessed: 2026-11-17; Primary finding: built-in `SlashCommand` enum, aliases, argument support, visibility gates; Tier: 1
- **SLASHCMDS-IN01-SC-CODEX-DEVCMDS** - `https://learn.chatgpt.com/docs/developer-commands?surface=cli`; Accessed: 2026-11-17; Primary finding: CLI slash-command catalog and workflow descriptions; Tier: 2
- **SLASHCMDS-IN01-SC-CODEX-EXTCMDS** - `https://learn.chatgpt.com/docs/developer-commands?surface=cli` (extension surface section); Accessed: 2026-11-17; Primary finding: IDE extension slash-command list; Tier: 2
- **SLASHCMDS-IN01-SC-CODEX-DOCS** - `e:\dev\IPPS\_PrivateSessions_gitignore\_2026-11-17_AgentSlashCommandKeywords\_download_gitignore\CODEX\docs\slash_commands.md`; Accessed: 2026-11-17; Primary finding: no command list, redirects to online docs; Tier: 1 (no finding)
- **SLASHCMDS-IN01-SC-CODEX-CHGLOG** - `e:\dev\IPPS\_PrivateSessions_gitignore\_2026-11-17_AgentSlashCommandKeywords\_download_gitignore\CODEX\CHANGELOG.md`; Accessed: 2026-11-17; Primary finding: points to GitHub releases, no slash-command changes; Tier: 1 (no finding)

### Gemini CLI

- **SLASHCMDS-IN01-SC-GMNCLI-BLTLDR** - `e:\dev\IPPS\_PrivateSessions_gitignore\_2026-11-17_AgentSlashCommandKeywords\_download_gitignore\GMNCLI\packages\cli\src\services\BuiltinCommandLoader.ts`, commit `4fa64e71b9b4e1bb65a86cc2863574f561b82340`; Accessed: 2026-11-17; Primary finding: assembled built-in command list with feature gates; Tier: 1
- **SLASHCMDS-IN01-SC-GMNCLI-CMDREF** - `e:\dev\IPPS\_PrivateSessions_gitignore\_2026-11-17_AgentSlashCommandKeywords\_download_gitignore\GMNCLI\docs\reference\commands.md`; Accessed: 2026-11-17; Primary finding: documented slash commands, subcommands, aliases; Tier: 2
- **SLASHCMDS-IN01-SC-GMNCLI-CMDTYP** - `e:\dev\IPPS\_PrivateSessions_gitignore\_2026-11-17_AgentSlashCommandKeywords\_download_gitignore\GMNCLI\packages\cli\src\ui\commands\types.ts`; Accessed: 2026-11-17; Primary finding: command metadata schema; Tier: 1 (no direct keyword findings)
- **SLASHCMDS-IN01-SC-GMNCLI-CMDUTL** - `e:\dev\IPPS\_PrivateSessions_gitignore\_2026-11-17_AgentSlashCommandKeywords\_download_gitignore\GMNCLI\packages\cli\src\utils\commands.ts`; Accessed: 2026-11-17; Primary finding: slash command parser and alias resolution logic; Tier: 1 (no direct keyword findings)
- **SLASHCMDS-IN01-SC-GMNCLI-CHGLOG** - `e:\dev\IPPS\_PrivateSessions_gitignore\_2026-11-17_AgentSlashCommandKeywords\_download_gitignore\GMNCLI\docs\changelogs\index.md`; Accessed: 2026-11-17; Primary finding: no direct slash-command keyword additions in this snapshot; Tier: 2 (no finding)

### OpenCode

- **SLASHCMDS-IN01-SC-OPNCD-TUIAPP** - `e:\dev\IPPS\_PrivateSessions_gitignore\_2026-11-17_AgentSlashCommandKeywords\_download_gitignore\OPNCD\packages\tui\src\app.tsx`, commit `887f6cd44bbb5e68826ef53e76047b7e9e34c3ca`; Accessed: 2026-11-17; Primary finding: TUI slash command declarations and aliases; Tier: 1
- **SLASHCMDS-IN01-SC-OPNCD-TUIPRM** - `e:\dev\IPPS\_PrivateSessions_gitignore\_2026-11-17_AgentSlashCommandKeywords\_download_gitignore\OPNCD\packages\tui\src\component\prompt\index.tsx`; Accessed: 2026-11-17; Primary finding: prompt-level TUI slash commands including /cd, /editor, /skills, /worktrees; Tier: 1
- **SLASHCMDS-IN01-SC-OPNCD-TUIBTW** - `e:\dev\IPPS\_PrivateSessions_gitignore\_2026-11-17_AgentSlashCommandKeywords\_download_gitignore\OPNCD\packages\tui\src\feature-plugins\prompt\btw.tsx`; Accessed: 2026-11-17; Primary finding: /btw side-question command; Tier: 1
- **SLASHCMDS-IN01-SC-OPNCD-APPSES** - `e:\dev\IPPS\_PrivateSessions_gitignore\_2026-11-17_AgentSlashCommandKeywords\_download_gitignore\OPNCD\packages\app\src\session\commands\use-session-commands.tsx`; Accessed: 2026-11-17; Primary finding: desktop/IDE session slash commands; Tier: 1
- **SLASHCMDS-IN01-SC-OPNCD-APPCMD** - `e:\dev\IPPS\_PrivateSessions_gitignore\_2026-11-17_AgentSlashCommandKeywords\_download_gitignore\OPNCD\packages\app\src\composer\commands.tsx`; Accessed: 2026-11-17; Primary finding: desktop/IDE composer slash commands; Tier: 1
- **SLASHCMDS-IN01-SC-OPNCD-CORCMD** - `e:\dev\IPPS\_PrivateSessions_gitignore\_2026-11-17_AgentSlashCommandKeywords\_download_gitignore\OPNCD\packages\core\src\plugin\command.ts`; Accessed: 2026-11-17; Primary finding: server-provided built-in commands /init and /review; Tier: 1
- **SLASHCMDS-IN01-SC-OPNCD-TUIDOC** - `https://opencode.ai/docs/cli/tui/`; Accessed: 2026-11-17; Primary finding: common TUI slash commands and /btw side questions; Tier: 2
- **SLASHCMDS-IN01-SC-OPNCD-CHTSH** - `https://opencode.school/cheatsheet/`; Accessed: 2026-11-17; Primary finding: TUI slash commands including /share, /unshare, /details, /summarize; Tier: 2
- **SLASHCMDS-IN01-SC-OPNCD-CMMDOC** - `https://opencode.ai/docs/commands/`; Accessed: 2026-11-17; Primary finding: custom command mechanism, not built-in keyword list; Tier: 2 (no finding)

### Cline

- **SLASHCMDS-IN01-SC-CLINE-CLIREG** - `e:\dev\IPPS\_PrivateSessions_gitignore\_2026-11-17_AgentSlashCommandKeywords\_download_gitignore\CLINE\apps\cli\src\tui\commands\slash-command-registry.ts`, commit `4cdfb19a5e897b9e75827cbb4f280f322e27e44a`; Accessed: 2026-11-17; Primary finding: CLI local slash command registry; Tier: 1
- **SLASHCMDS-IN01-SC-CLINE-VSCMDS** - `e:\dev\IPPS\_PrivateSessions_gitignore\_2026-11-17_AgentSlashCommandKeywords\_download_gitignore\CLINE\apps\vscode\src\shared\slashCommands.ts`; Accessed: 2026-11-17; Primary finding: VS Code webview base slash commands; Tier: 1
- **SLASHCMDS-IN01-SC-CLINE-BUILTIN** - `e:\dev\IPPS\_PrivateSessions_gitignore\_2026-11-17_AgentSlashCommandKeywords\_download_gitignore\CLINE\apps\vscode\src\sdk\builtin-slash-commands.ts`; Accessed: 2026-11-17; Primary finding: SDK runtime built-in /deep-planning command; Tier: 1
- **SLASHCMDS-IN01-SC-CLINE-DOCS** - `https://docs.cline.bot/core-workflows/using-commands`; Accessed: 2026-11-17; Primary finding: documented slash commands /newtask, /smol, /newrule, /deep-planning, /reportbug; Tier: 2
- **SLASHCMDS-IN01-SC-CLINE-SKILL** - `https://docs.cline.bot/.well-known/agent-skills/cline/skill.md`; Accessed: 2026-11-17; Primary finding: slash commands /plan, /act, /deep-planning, /newrule, /model, /clear, /undo, /help; Tier: 2

### Claude Code

- **SLASHCMDS-IN01-SC-CLCD-CMDREF** - `https://code.claude.com/docs/en/commands`; Accessed: 2026-11-17; Primary finding: complete built-in and bundled slash command reference with arguments and aliases; Tier: 2
- **SLASHCMDS-IN01-SC-CLCD-CHTSH** - `https://support.claude.com/en/articles/14553413-claude-code-cheatsheet`; Accessed: 2026-11-17; Primary finding: common built-in slash commands and aliases; Tier: 2
- **SLASHCMDS-IN01-SC-CLCD-CHGLOG** - `https://code.claude.com/docs/en/changelog`; Accessed: 2026-11-17; Primary finding: current version v2.1.326, no conflicting slash-command changes; Tier: 2
- **SLASHCMDS-IN01-SC-CLCD-LOCAL** - `C:\Users\User\AppData\Local\AnthropicClaude\`; Accessed: 2026-11-17; Primary finding: Claude Desktop app present, no Claude Code CLI executable found; Tier: 3 (no CLI findings)

### Devin

- **SLASHCMDS-IN01-SC-DEVIN-CMDREF** - `https://docs.devin.ai/cli/reference/commands`; Accessed: 2026-11-17; Primary finding: complete Devin CLI slash command reference with mode, session, workspace, automation, extensibility, utility, and cloud commands; Tier: 2
- **SLASHCMDS-IN01-SC-DEVIN-ESS** - `https://docs.devin.ai/cli/essential-commands`; Accessed: 2026-11-17; Primary finding: essential slash commands for navigation, modes, and workspace; Tier: 2
- **SLASHCMDS-IN01-SC-DEVIN-WEB** - `https://docs.devin.ai/work-with-devin/slash-commands`; Accessed: 2026-11-17; Primary finding: web app only supports organization-defined custom slash commands; Tier: 2
- **SLASHCMDS-IN01-SC-DEVIN-CHG** - `https://docs.devin.ai/desktop/changelog-next`; Accessed: 2026-11-17; Primary finding: Devin Desktop (Windsurf) Next changelog, mentions Plan mode and Megaplan keyword behavior; Tier: 2
- **SLASHCMDS-IN01-SC-DEVIN-LOCAL** - `C:\Users\User\AppData\Local\Programs\Devin\`; Accessed: 2026-11-17; Primary finding: Devin Desktop installed, source minified, no slash commands extracted; Tier: 3 (no direct findings)
- **SLASHCMDS-IN01-SC-DEVIN-STABLECHG** - `https://docs.devin.ai/cli/changelog/stable`; Accessed: 2026-11-17; Primary finding: stable changelog confirms `/code`, `/smart`, `/bypass`, `/session-stats`, `/model`, `/models`, `/btw`, `/usage`, `/bug`; no new CLI slash keywords beyond command reference; Tier: 2

### Windsurf (Cascade)

- **SLASHCMDS-IN01-SC-WNDSRF-CHATDOC** - `https://docs.windsurf.com/llms-full.txt` (Chat Overview section); Accessed: 2026-11-17; Primary finding: `/explain` documented as the only supported slash command; Tier: 2
- **SLASHCMDS-IN01-SC-WNDSRF-SHORT** - `https://shortcut-tools.com/en/shortcuts/windsurf/`; Accessed: 2026-11-17; Primary finding: `/plan`, `/model` built-in commands and workflow invocation pattern; Tier: 4
- **SLASHCMDS-IN01-SC-WNDSRF-WF** - `https://docs.devin.ai/windsurf/plugins/cascade/workflows`; Accessed: 2026-11-17; Primary finding: user-defined and built-in workflows invoked as `/<workflow-name>`; Tier: 2
- **SLASHCMDS-IN01-SC-WNDSRF-CHG** - `https://docs.devin.ai/desktop/changelog-next`; Accessed: 2026-11-17; Primary finding: stable and Next build versions v3.13.4/v3.13.1004, mentions Plan mode and Megaplan; Tier: 2
- **SLASHCMDS-IN01-SC-WNDSRF-LOCAL** - `C:\Users\User\AppData\Local\Programs\Windsurf Next\`; Accessed: 2026-11-17; Primary finding: installed but no executable or unminified source found; Tier: 3 (no direct findings)

### Cursor

- **SLASHCMDS-IN01-SC-CRSR-SLASH** - `https://cursor.com/docs/cli/reference/slash-commands`; Accessed: 2026-11-17; Primary finding: official Cursor CLI slash command catalog with aliases; Tier: 2
- **SLASHCMDS-IN01-SC-CRSR-USING** - `https://cursor.com/docs/cli/using`; Accessed: 2026-11-17; Primary finding: `/plan`, `/ask`, `/debug` for mode switching; Tier: 2
- **SLASHCMDS-IN01-SC-CRSR-PARAMS** - `https://cursor.com/docs/cli/reference/parameters`; Accessed: 2026-11-17; Primary finding: launch flags and non-interactive mode, no additional slash commands; Tier: 2 (no finding)
- **SLASHCMDS-IN01-SC-CRSR-CHG** - `https://cursor.com/changelog/1-6`; Accessed: 2026-11-17; Primary finding: custom slash commands and `/summarize` introduced for IDE Agent input; Tier: 2
- **SLASHCMDS-IN01-SC-CRSR-FAN** - `https://cursor.fan/tutorial/HowTo/cursor-skills-commands-rules-guide/`; Accessed: 2026-11-17; Primary finding: community reference listing IDE built-in slash commands `/explain`, `/fix`, `/doc`, `/test`, `/refactor`, `/commit`; Tier: 4

### GitHub Copilot

- **SLASHCMDS-IN01-SC-GHCP-CHTSH** - `https://docs.github.com/en/copilot/reference/chat-cheat-sheet`; Accessed: 2026-11-17; Primary finding: per-surface Copilot Chat slash-command tables for VS Code, Visual Studio, JetBrains, Xcode, and github.com chat; Tier: 2
- **SLASHCMDS-IN01-SC-GHCP-IDE** - `https://docs.github.com/en/copilot/how-tos/copilot-in-your-ide/chat-with-copilot/chat-in-ide`; Accessed: 2026-11-17; Primary finding: IDE slash command examples for Eclipse, VS Code, Visual Studio, JetBrains, Xcode; Tier: 2
- **SLASHCMDS-IN01-SC-GHCP-MOB** - `https://docs.github.com/en/copilot/how-tos/copilot-on-github/chat-with-copilot/chat-in-mobile`; Accessed: 2026-11-17; Primary finding: GitHub Mobile Copilot chat uses natural-language prompts, no `/` command list; Tier: 2 (no finding)
- **SLASHCMDS-IN01-SC-GHCP-CLIREF** - `https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference`; Accessed: 2026-11-17; Primary finding: complete interactive CLI slash-command catalog with aliases and subcommands; Tier: 2
- **SLASHCMDS-IN01-SC-GHCP-APP** - `https://docs.github.com/en/copilot/reference/github-copilot-app-reference/slash-commands`; Accessed: 2026-11-17; Primary finding: GitHub Copilot app slash-command reference for desktop and web agent sessions; Tier: 2
- **SLASHCMDS-IN01-SC-GHCP-VSCHG** - `https://github.com/microsoft/vscode/blob/main/extensions/copilot/CHANGELOG.md`; Accessed: 2026-11-17; Primary finding: VS Code Copilot Chat agent-mode slash commands added in the last six months; Tier: 1
- **SLASHCMDS-IN01-SC-GHCP-CLICHG** - `https://github.com/github/copilot-cli/blob/main/changelog.md`; Accessed: 2026-11-17; Primary finding: CLI changelog confirms existing slash commands, no new slash keywords; Tier: 2
- **SLASHCMDS-IN01-SC-GHCP-OPN** - `https://raw.githubusercontent.com/microsoft/vscode/main/extensions/copilot/package.json`; Accessed: 2026-11-17; Primary finding: VS Code Copilot Chat extension identity `copilot-chat` version `0.76.0`; Tier: 1 (no direct keyword findings)

### Google Gemini

- **SLASHCMDS-IN01-SC-GMNI-SKILLS** - `https://support.google.com/gemini/answer/17094296`; Accessed: 2026-11-17; Primary finding: `/` triggers user-defined Skills, no vendor-built-in slash commands; Tier: 2
- **SLASHCMDS-IN01-SC-GMNI-CHROME** - `https://support.google.com/gemini/answer/16988996`; Accessed: 2026-11-17; Primary finding: Gemini in Chrome `/` menu lists library and user Skills; no vendor slash commands; Tier: 2
- **SLASHCMDS-IN01-SC-GMNI-TASKS** - `https://support.google.com/gemini/answer/17094507`; Accessed: 2026-11-17; Primary finding: tasks use UI button, natural language, and `@skill` mentions; no `/` built-ins; Tier: 2

### Google Jules

- **SLASHCMDS-IN01-SC-JULES-EXT** - `https://github.com/gemini-cli-extensions/jules`; Accessed: 2026-11-17; Primary finding: Gemini CLI extension exposes the `/jules` slash command for delegating tasks; Tier: 2
- **SLASHCMDS-IN01-SC-JULES-WEB** - `https://jules.google/` and `https://jules.google/docs/faq/`; Accessed: 2026-11-17; Primary finding: web UI uses natural-language prompts and GitHub issue labels, no slash commands; Tier: 2 (no finding)
- **SLASHCMDS-IN01-SC-JULES-CLI** - `https://jules.google/docs/cli/reference/` and `https://jules.google/docs/changelog/2025-10-02/`; Accessed: 2026-11-17; Primary finding: Jules Tools CLI uses `jules remote` subcommands, no `/`-prefixed commands documented; Tier: 2 (no finding)

### Google Antigravity

- **SLASHCMDS-IN01-SC-ANTGRV-OVR** - `https://antigravity.google/docs/slash-commands/`; Accessed: 2026-11-17; Primary finding: complete public slash-command catalog across App and CLI with surface notes; Tier: 2
- **SLASHCMDS-IN01-SC-ANTGRV-CLI** - `https://antigravity.google/docs/cli/reference/`; Accessed: 2026-11-17; Primary finding: core CLI slash-command table with aliases and arguments; Tier: 2
- **SLASHCMDS-IN01-SC-ANTGRV-AGT** - `https://antigravity.google/docs/cli/commands/agents/`; Accessed: 2026-11-17; Primary finding: `/agents` Agent Manager panel behavior; Tier: 2
- **SLASHCMDS-IN01-SC-ANTGRV-BRW** - `https://antigravity.google/docs/commands/browser/`; Accessed: 2026-11-17; Primary finding: `/browser` subagent command details; Tier: 2
- **SLASHCMDS-IN01-SC-ANTGRV-SCH** - `https://antigravity.google/docs/commands/schedule/`; Accessed: 2026-11-17; Primary finding: `/schedule` syntax and behavior; Tier: 2

### ChatGPT

- **SLASHCMDS-IN01-SC-CGPT-SLSHCMDS** - `https://learn.chatgpt.com/docs/reference/slash-commands`; Accessed: 2026-11-17; Primary finding: complete ChatGPT desktop app slash-command catalog with 28 built-in commands; Tier: 2
- **SLASHCMDS-IN01-SC-CGPT-DEVCMDS** - `https://learn.chatgpt.com/docs/developer-commands`; Accessed: 2026-11-17; Primary finding: confirms desktop composer commands and distinguishes ChatGPT web composer as a separate menu; Tier: 2
- **SLASHCMDS-IN01-SC-CGPT-RELNOTES** - `https://help.openai.com/en/articles/9703738-chatgpt-macos-app-release-notes`; Accessed: 2026-11-17; Primary finding: slash commands introduced November 2024, no additional command names listed; Tier: 2 (no new findings)


## Document History

**[2026-11-18 07:55]**
- Changed: Section 2 joint reserved keyword list entries now include a meaning summary before `Agents:` and separate properties with `|`
- Changed: `Meaning: differs` entries now list at least two major purposes instead of the generic `purpose or surface differs across agents`

**[2026-11-17 19:45]**
- Added: Section 2 joint reserved keyword list (364 entries), Section 16 cross-agent observations, and Section 17 exclusions generated from the parsed catalog
- Added: Independent completeness probe sources `SLASHCMDS-IN01-SC-DEVIN-STABLECHG` and `SLASHCMDS-IN01-SC-CRSR-FAN`; added Cursor IDE built-ins `/commit`, `/doc`, `/explain`, `/fix`, `/refactor`, `/test` as `[ASSUMED]`
- Fixed: OpenAI Codex status moved from `PARTIAL` to `COMPLETE 2026-11-17` after checking desktop app and web surfaces against vendor docs
- Verified: `__SCRIPT_SlashCmds-SetCheck.ps1` `-Mode Check` passes via supervised runner with exit code 0

**[2026-11-17 17:30]**
- Fixed: Sorted keyword entries in all agent sections with a helper script; added missing alias entries `/bug`, `/quit`, `/continue`, `/footer`, `/rewind` for GitHub Copilot and `/conversation` for Google Antigravity
- Fixed: Pre-check script single-element sort bug in `__SCRIPT_SlashCmds-PreCheck.ps1` (`$sorted` now forced to an array)
- Verified: `__SCRIPT_SlashCmds-PreCheck.ps1` reports `OK: no failures`

**[2026-11-17 17:20]**
- Added: Sections 6, 7, 8, and 9 keyword entries for GitHub Copilot, Google Gemini, Google Jules, and Google Antigravity with product facts, collision rules, searched-not-found lists, and statuses
- Added: Section 18 source records for GitHub Copilot, Google Gemini, Google Jules, and Google Antigravity
- Added: Findings card entry 10 documenting that checkpoint 1 is unresolved because OpenAI Codex is PARTIAL, not COMPLETE
- Added: Findings card entries 11-14 for GitHub Copilot surface coverage gaps, Google Gemini absence of built-in slash commands, Jules surface coverage, and Antigravity surface-specific commands

**[2026-11-17 18:15]**
- Fixed: Added missing alias entries in Claude Code (`/android`, `/app`, `/bashes`, `/checkpoint`, `/continue`, `/ios`, `/quit`, `/routines`), Devin (`/rename-session`), and removed duplicate `/?` in Gemini CLI
- Fixed: Restored A-Z sort order in Claude Code, OpenAI Codex, Gemini CLI, OpenCode, and Cursor
- Fixed: Changed Windsurf `/model` label from VERIFIED to ASSUMED (single Tier 4 source)
- Fixed: Formatted NOT DONE status lines for unstarted agents ChatGPT, GitHub Copilot, Google Gemini, Google Jules, and Google Antigravity
- Verified: All cited source IDs resolve in Section 18; all entries have required fields and valid labels

**[2026-11-17 17:00]**
- Added: Sections 4, 5, 10, and 14 keyword entries for Claude Code, Devin, Cursor, and Windsurf (Cascade) with product facts, collision rules, searched-not-found lists, and statuses
- Added: Section 18 source records for Claude Code, Devin, Windsurf (Cascade), and Cursor
- Added: Findings card entries for Windsurf source conflict, Devin Desktop/Cursor local inspection limits, and Cursor IDE built-in ambiguity

**[2026-11-17 16:45]**
- Added: Sections 11-15 keyword entries for OpenAI Codex, Gemini CLI, OpenCode, and Cline with product facts, collision rules, searched-not-found lists, and statuses
- Added: Section 18 source list for all consulted and cited sources of the four agents
- Changed: Codex status to PARTIAL (CLI and IDE extension done, desktop/web pending); Gemini CLI, OpenCode, and Cline marked COMPLETE for the requested surfaces

**[2026-11-17 13:53]**
- Initial skeleton created; Section 1 written; Sections 3-15 headings added for all 13 agents; Sections 2, 16, 17 marked pending for prompt 4
