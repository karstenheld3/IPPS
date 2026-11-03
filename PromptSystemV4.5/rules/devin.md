---
trigger: always_on
---

# Devin/Cascade-Specific Rules

Agent-specific rules for Windsurf/Devin (Cascade) environments. Excluded from sync to non-Devin agent repos.

## Tool Constraints

- NEVER ask questions. NEVER use the `ask_user_question` tool. Resolve ambiguity through prompt analysis, not clarification requests
- The `ask_user_question` tool is FORBIDDEN. This includes all interactive prompt mechanisms. The only exception: when two interpretations lead to destructive, irreversible, and materially different outcomes
- Cascade: `gesetze-im-internet.de` Playwright only. `search_web` / `read_url_content` on this domain crash the conversation. Repeat this ban in prompts that research German law

## Terminal Limits

**Cascade terminal limit (2026-03-09):** Max 4 concurrent terminals. Additional terminals are queued/delayed.

Command execution follows `agent-behavior.md` Terminal Hang Prevention and Batch Operations. Cascade specifics:

- Non-whitelisted commands: `run_command` runs only the `pwsh -NoProfile -NonInteractive -File _agentwork/.tmp_[purpose].ps1 > ... 2> ...` line; read results with `read_file`
- Use `run_command` with `Blocking: false` for parallel or slow tasks, poll with `command_status`
- Never open external terminals unless explicitly requested

## Agent Folder Mapping

**[AGENT_FOLDER]** location for Devin/Cascade:
- `.devin/`

## Workspace Definition

- **[WORKSPACE]**: The Windsurf/VSCode workspace root folder

## Cascade-Specific Workflows

- `/switch-model` - Switch Cascade AI model tier (HIGH, MID, LOW)

## Cascade-Specific Skills

- `@devin-auto-model-switcher` - Switch Cascade AI model tier programmatically
