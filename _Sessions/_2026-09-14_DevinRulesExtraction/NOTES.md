# Session: Devin/Cascade Rules Extraction

**Doc ID**: DEVINRLES-NOTES
**Goal**: Extract Devin/Cascade/Windsurf-specific rules into rules/devin.md, configure sync exclusions for Lana-V1 and Hera-V1

## Current Phase

**Phase**: IMPLEMENT
**Workflow**: Direct implementation (clear scope, COMPLEXITY-MEDIUM)
**Assessment**: Rules analysis complete, ready to implement

## User Prompts

Move all devin or cascade specific rules into rules/devin.md so we can exclude it when syncing promptsystem to lana-v1 and hera-v1. Also modify or initialize lana-v1 and hera-v1 promptsystem-sync.json to exclude irrelevant stuff like travel-info and model switcher.

## Analysis: Devin/Cascade-Specific Content in Rules

### agent-behavior.md
- Line 12, 19: `ask_user_question` tool references (Cascade-specific tool)
- Line 171: `Cascade terminal limit` (Cascade-specific implementation detail)
- Lines 183-184: `run_command with Blocking: false` (Cascade-specific tool API)

### promptsystem-core.md
- Line 14: `Windsurf/VSCode workspace root folder` (Windsurf-specific)
- Lines 30-32: `Devin: .devin/` / `Claude Code: .claude/` agent folder mapping (agent-specific)
- Line 329: `/switch-model - Switch Cascade AI model tier` (Cascade-specific workflow)

### tools-and-skills.md
- Line 55: `@devin-auto-model-switcher` skill entry (Cascade-specific)

### agentic-english.md
- Line 62: `[AGENT_FOLDER]` mentions `.devin/` or `.claude/` (agent-specific folder names)

## Plan

1. Create `rules/devin.md` with extracted Devin/Cascade/Windsurf-specific rules
2. Remove/neutralize those references from original rule files
3. Update Lana-V1 `promptsystem-sync.json` - add exclusions
4. Create Hera-V1 `promptsystem-sync.json` - with same exclusions

## IMPORTANT: Cascade Agent Instructions

- `ask_user_question` tool is FORBIDDEN - resolve ambiguity through analysis
- Cascade terminal limit: max 4 concurrent terminals
- Use `run_command` with `Blocking: false` for parallel tasks
