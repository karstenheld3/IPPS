---
description: Execute implementation from IMPL plan
---

# Implement Workflow

Implements execution phase - build from plan in small verified steps.

## Required Skills

- @coding-conventions for coding style
- @write-documents for tracking

## Context Branching

Check what documents exist and proceed accordingly:

### No SPEC, IMPL, TEST documents

Implement whatever was proposed or specified in conversation.

### Existing INFO only

Run `/write-spec` first.

### Existing SPEC only

Run `/write-impl-plan` first.

### Existing IMPL only

Run `/write-test-plan` first.

### Existing TEST only (no TASKS)

Run `/write-tasks-plan` first. TASKS document is mandatory before implementation.

### Existing TASKS (no code yet)

Implement function skeletons from IMPL, then full failing tests from TEST.

### Existing TASKS + test code

Implement everything from TASKS in small verifiable steps.

## Operation Mode Check

Before implementing, verify operation mode from NOTES.md:
- **IMPL-CODEBASE** → output to project source folders
- **IMPL-ISOLATED** → output to `[SESSION_FOLDER]/` only, NEVER workspace root

## Execution Loop

For each task in TASKS plan:
1. Make code changes
2. Verify task works
3. Fix if tests fail
4. Commit when green
5. Mark task complete in TASKS

## Quality Gate

- [ ] All tasks from TASKS plan completed
- [ ] Tests pass
- [ ] No TODO/FIXME left unaddressed
- [ ] Progress committed

## Stuck Detection

If 3 consecutive fix attempts fail on a task:
1. Document failure in PROBLEMS.md
2. **Re-partition**: Run `/write-tasks-plan` to create new TASKS version with smaller chunks
3. If re-partition doesn't help: Consult with user

## Attitude

- Senior engineer, anticipating complexity, reducing risks
- Completer / Finisher, never leaves clutter undocumented
- Small cycles: implement→test→fix→green→next

## Rules

- Use small, verifiable steps - never implement large untestable chunks
- Track progress in PROGRESS.md after each commit
- Document problems in PROBLEMS.md immediately when found
- Remove temporary `.tmp_*` files after implementation complete