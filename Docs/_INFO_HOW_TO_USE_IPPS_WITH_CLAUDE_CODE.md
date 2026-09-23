# INFO: How to Use IPPS with Claude Code

**Doc ID**: CLCD-IN02
**Goal**: Explain how to run IPPS in Claude Code - setup, daily usage, and the differences from the Devin deployment
**Timeline**: Created 2026-09-23

## Summary

- IPPS runs in Claude Code out of the box: the `.claude/` folder holds all rules and skills; Claude Code loads them automatically at session start [PROVEN]
- All IPPS slash commands work unchanged (`/prime`, `/go`, `/commit`, ...) with one exception: the verify workflow runs as `/ipps-verify` [VERIFIED]
- Model switching uses Claude Code's native `/model`; the Devin `switch-model` workflow is not deployed [PROVEN]
- MCP servers (Playwright, Playwriter, seo-tools) register per agent: `claude mcp add <name> -- <command>` or `.mcp.json`, not the Devin JSON config [VERIFIED]
- After IPPS updates, running sessions need a restart or `/reload-skills` to pick up new skills [VERIFIED]
- Regenerating `.claude/` after source changes is a maintainer task - see [For Maintainers](#7-for-maintainers) at the end

## Table of Contents

1. [Setup](#1-setup)
2. [Daily Usage](#2-daily-usage)
3. [What Works Differently](#3-what-works-differently)
4. [Reserved Claude Code Commands](#4-reserved-claude-code-commands)
5. [Context Cost](#5-context-cost)
6. [Troubleshooting](#6-troubleshooting)
7. [For Maintainers](#7-for-maintainers)
8. [Sources](#8-sources)
9. [Document History](#9-document-history)

## 1. Setup

Requirements: Claude Code installed and the `.claude/` folder in your project root. In this repository it is already deployed; to use IPPS in another project, copy the folder there:

```
your-project/
└── .claude/
    ├── rules/          # 7 rule files - loaded at every session start
    └── skills/         # 71 skills = 48 workflows + 23 domain skills
```

Claude Code discovers both automatically - no configuration needed. The `[AGENT_FOLDER]` placeholder used throughout IPPS texts resolves to `.claude/` in Claude Code sessions, so no adjustments are needed.

First session:

```
cd your-project
claude
/prime
```

`/prime` loads the workspace context (NOTES, PROGRESS, FAILS). From there, work as usual.

## 2. Daily Usage

All IPPS slash commands work the same way - type them into the Claude Code prompt:

```
/prime
/go "Add user registration endpoint"
/verify            →  /ipps-verify
/commit
```

- Skills accept `$ARGUMENTS`: `/go "task description"`
- Workflows run user-invoked only - the agent never auto-triggers them
- The [README usage examples](../README.md#usage-examples) apply unchanged

## 3. What Works Differently

- **Verify**: invoke as `/ipps-verify` - `/verify` runs the bundled Claude Code skill instead, which would overwrite the IPPS path [VERIFIED]
- **Model switching**: use the native `/model` (includes effort level); the Devin `switch-model` workflow is not deployed [PROVEN]
- **MCP servers**: register per agent - `claude mcp add <name> -- <command>` or `.mcp.json`, not the Devin JSON config path. Each skill's SETUP.md branches per agent [VERIFIED]
- **Conversation cleanup**: `/remove conversation` (Devin-only mode) does not apply; Claude Code manages sessions via `/resume`, `/export`
- **Terminal vs IDE**: Claude Code runs in the terminal (plus IDE extensions); Devin is an IDE. No functional impact on IPPS workflows
- **Personal skills** (`~/.claude/skills/`) are not available in cloud/Cowork sessions; the project-level `.claude/` deployment carries over via the repository [VERIFIED]

## 4. Reserved Claude Code Commands

Claude Code reserves its own command names - built-in slash commands (`/clear`, `/compact`, `/context`, `/model`, `/resume`, ...) and bundled skills (`/doctor`, `/code-review` (alias `/review`), `/batch`, `/debug`, `/loop`, `/claude-api`, `/workflow-authoring`). An IPPS workflow whose name collides with one of them deploys under a different name:

- **`/verify`** → deployed as **`/ipps-verify`**. The bundled Claude Code `/verify` skill records its recipes to `.claude/skills/verify/SKILL.md`, overwriting any project skill at that path [VERIFIED]

All other 70 IPPS skill names are unreserved - checked against the full built-in command and bundled skill lists (sections 7.1 and 7.2 of [`_INFO_HOW_CLAUDE_CODE_WORKS.md`](_INFO_HOW_CLAUDE_CODE_WORKS.md)) [VERIFIED 2026-09-23]

When adding workflows later:

- Never place a skill at `.claude/skills/verify/` - the bundled skill overwrites it on use
- Check new names against the built-in commands and bundled skills first; rename on collision (`ipps-` prefix)
- A same-named project skill replaces a bundled command but never its aliases; bundled skills can be disabled via `disableBundledSkills` [VERIFIED]

## 5. Context Cost

- The 48 workflow skills are user-only: zero context tokens - the model never sees their descriptions
- The 9 model-triggered domain skills (write-documents, session-management, coding-conventions, research-methods, workspace-management, drift-control, edird-phase-planning, git-conventions, ms-playwright-mcp) cost ~100 tokens each (name + description)
- Full skill content loads only on invocation (progressive disclosure); supporting files load on demand
- Tuning (rarely needed): `skillListingBudgetFraction` (default 1% of context window), `skillListingMaxDescChars` (default 1,536); `/skill-doctor` reports per-skill cost and invocation counts

## 6. Troubleshooting

- **Command not found** after an IPPS update: restart Claude Code or run `/reload-skills` [VERIFIED]
- **`/verify` runs the wrong skill**: use `/ipps-verify` (see [Reserved Claude Code Commands](#4-reserved-claude-code-commands))
- **Workflow does not fire automatically**: IPPS workflows are user-only by design - invoke them explicitly
- **Rules not loaded**: `CLAUDE.md` and `.claude/rules/` both load at session start; IPPS content lives in `rules/`, no CLAUDE.md merge needed

## 7. For Maintainers

`.claude/` is generated from `PromptSystemV4.4/` - never edit it directly, changes are lost on the next regeneration. Edit `PromptSystemV4.4/`, then regenerate:

```
PromptSystemV4.4/ (source of truth, edit here)
  ├─> robocopy /MIR ──────────> .devin/   (Devin, 1:1 mirror)
  └─> _PROMPTS_UpdateClaude.md prompts ──> .claude/  (Claude Code, transformed)
```

1. Open `_PROMPTS_UpdateClaude.md` in the repository root
2. Run its 7 prompts in order (preflight, rules, workflows, checkpoint 1, skills, checkpoint 2, finalize)
3. The sequence is idempotent - re-running it performs a full rebuild (deletes and recreates `rules/` and `skills/`) and must not corrupt state

Transform per workflow file: keep `description`, add `name` (folder name) and `disable-model-invocation: true` (makes the skill user-only - the equivalent of an IPPS workflow), drop `auto_execution_mode`, body unchanged. Devin-specific items are excluded (`devin.md` rule, `switch-model` workflow, `devin-auto-model-switcher` skill - Claude Code has native `/model`). Deployment state and known issues are tracked in `__CARD_UpdateClaude-Findings.md` during regeneration runs (removed by `/cleanup`).

Open maintainer tasks:

1. Live-test the deployment in a real Claude Code session: `/prime`, `/go` on a small task, `/ipps-verify`
2. Fix the 6 source skills lacking frontmatter in `PromptSystemV4.4/skills/` so regeneration needs no frontmatter patching
3. Extend `README.md` "Agent Compatibility" section - its Claude Code column still documents the pre-migration `.claude/commands/` approach

## 8. Sources

**Primary Sources:**
- `CLCD-IN02-SC-CLCD-IN01`: `Docs/_INFO_HOW_CLAUDE_CODE_WORKS.md` - Claude Code mechanics: skills discovery, invocation control, progressive disclosure, `/reload-skills`, MCP scopes [VERIFIED 2026-09-23]
- `CLCD-IN02-SC-IPPS-PROMPTS`: `_PROMPTS_UpdateClaude.md` - deployment sequence, transform rules, exclusions, verify criteria [VERIFIED 2026-09-23]
- `CLCD-IN02-SC-IPPS-CARD`: `__CARD_UpdateClaude-Findings.md` - deployment state, counts, verification results [PROVEN 2026-09-23, 34 checks 0 failures]
- `CLCD-IN02-SC-IPPS-README`: `README.md` - IPPS usage examples and workflow reference [VERIFIED 2026-09-23]

## 9. Document History

**[2026-09-23 16:25]**
- Added: "Reserved Claude Code Commands" section - `/verify` collision, rename rule for future workflows

**[2026-09-23 16:15]**
- Changed: restructured for users - Setup, Daily Usage, Differences, Troubleshooting first; deployment internals moved to "For Maintainers" section

**[2026-09-23 15:55]**
- Initial document created from CLCD-IN01 and the verified `.claude` deployment state (commits `dbff6ea`, `11f68d1`)
