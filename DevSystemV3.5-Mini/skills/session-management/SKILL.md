---
name: session-management
description: Apply when initializing, saving, resuming, or closing a work session
---

# Session Management Guide

Sessions track EDIRD phases: NOTES.md has "Current Phase" (phase, last verb, gate status), PROGRESS.md has "Phase Plan" (5 phases with status).

## MUST-NOT-FORGET

- Session folder location: `[DEFAULT_SESSIONS_FOLDER]/_YYYY-MM-DD_[SessionTopicCamelCase]/`
- Default: `[DEFAULT_SESSIONS_FOLDER]` = `[WORKSPACE_FOLDER]` (override in `!NOTES.md`)
- Required files: NOTES.md, PROBLEMS.md, PROGRESS.md
- Lifecycle: Init → Work → Save → Resume → Finalize → Archive
- Sync session PROBLEMS.md to project on /session-finalize
- Phase tracking: NOTES.md has current phase, PROGRESS.md has full phase plan
- **Acronyms/principles in NOTES.md**: Always spell out acronyms and principles fully so agents can understand them without external context. Example: "APAPALAN: As Precise As Possible, As Little As Necessary" not just "APAPALAN principle"
- **STOP after session init**: After creating session files, STOP and wait for user review. Do NOT implement session goal until explicitly requested. User must review and refine goals before work begins.

## Session Lifecycle

1. **Init** (`/session-new`): Create session folder with tracking files
2. **Work**: Create specs, plans, implement, track progress
3. **Save** (`/session-save`): Document findings, commit changes
4. **Resume** (`/session-load`): Re-read session documents, continue work
5. **Finalize** (`/session-finalize`): Sync findings to project files, prepare for archive

## Session Folder Location

Base: `[DEFAULT_SESSIONS_FOLDER]` (default: `[WORKSPACE_FOLDER]`, overridable in `!NOTES.md`)
Format: `[DEFAULT_SESSIONS_FOLDER]/_YYYY-MM-DD_[SessionTopicCamelCase]/`

## Required Session Files

Templates from this skill folder:

- **NOTES.md** (`NOTES_TEMPLATE.md`): Context, agent instructions, working patterns, large initial prompts (>120 tokens). Static knowledge.
- **PROBLEMS.md** (`PROBLEMS_TEMPLATE.md`): All problems - prompts, questions, features, bugs, investigations. Each gets unique ID, tracks status (Open/Resolved/Deferred). Dynamic problem list.
- **PROGRESS.md** (`PROGRESS_TEMPLATE.md`): To-do, done, tried-but-not-used. Task execution status.

## Assumed Workflow

```
1. INIT: /session-new → folder + NOTES, PROBLEMS, PROGRESS created
2. PREPARE: User prepares manually OR explains problem, agent assists
3. WORK: Implement, decide, test, verify. Track continuously.
4. SAVE: /session-save → update + commit
5. RESUME: /session-load → prime from files, continue
6. FINALIZE: /session-finalize → sync to project/workspace
7. ARCHIVE: Move folder to _Archive/
```

## ID System

See `[AGENT_FOLDER]/rules/devsystem-ids.md` for complete system.

- Document: `[TOPIC]-[DOC][NN]` (IN, SP, IP, TP) - e.g., `CRWL-SP01`
- Tracking: `[TOPIC]-[TYPE]-[NNNN]` (BG, FT, PR, FX, TK) - e.g., `SAP-BG-0001`
- Topic Registry: Maintained in project NOTES.md

## Session Init Template

### NOTES.md
```markdown
# Session Notes
## Session Info
- **Started**: [DATE]
- **Goal**: [Brief description]
## Key Decisions
## Important Findings
## Workflows to Run on Resume
```

### PROBLEMS.md
```markdown
# Session Problems
## Open
## Resolved
## Deferred
```

### PROGRESS.md
```markdown
# Session Progress
## To Do
## In Progress
## Done
## Tried But Not Used
```