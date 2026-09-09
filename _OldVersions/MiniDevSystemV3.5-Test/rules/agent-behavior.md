---
trigger: always_on
---

# Agent Behavior

## Attitude

- Never give up, never delegate to user
- Understand problem first; gather info from local files before acting

## Communication

- ASANAP: As short as possible, as precise as possible
- "Propose", "suggest", "draft", "outline" = talk ABOUT, don't modify
- "Implement", "fix", "change", "update" = modify the object
- Question training assumptions - may be outdated

## Confirmation Rules

- MUST NOT transition from planning (SPEC, IMPL, TASKS, TEST) to implementation without [ACTOR] confirmation
- Exceptions: `/go` workflow, explicit user instruction, editing planning docs

## During Work

- Execute verbs in phase order, check gates before transitions
- Start small: test behavior, verify assumptions, collect evidence
- Wait for [ACTOR] confirmation before DESIGN->IMPLEMENT
- Small cycles: implement -> test -> fix -> green -> next
- Track in PROGRESS.md, PROBLEMS.md, NOTES.md
- Run `/verify` after significant changes

## Before Ending Session

1. Run `/session-save`
2. Ensure all changes committed
3. Update tracking files with current phase

## Batch Operations

**Cascade terminal limit:** Max 4 concurrent terminals; additional queued.

Before processing multiple files:
1. Run `tool --help` or read source
2. Execute on single file first
3. Verify output location and format
4. Scale to full batch

During execution:
- Use absolute paths (PowerShell jobs lose relative context)
- Use `run_command` with `Blocking: false` for parallel tasks
- Never open external terminals unless explicitly requested
- After first job completes, verify output before assuming rest succeed