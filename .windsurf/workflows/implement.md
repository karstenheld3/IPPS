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

### Existing TEST (no test code)

Implement function skeletons from IMPL, then full failing tests from TEST.

### Existing TEST + test code

Implement everything from IMPL in small verifiable steps.

## Operation Mode Check

Before implementing, verify operation mode from NOTES.md:
- **IMPL-CODEBASE** → output to project source folders
- **IMPL-ISOLATED** → output to `[SESSION_FOLDER]/` only, NEVER workspace root

## Execution Loop

For each step in IMPL plan:
1. Make code changes
2. Verify step works
3. Fix if tests fail (max 3 retries)
4. Commit when green
5. Check against IMPL plan

## Quality Gate

- [ ] All steps from IMPL plan implemented
- [ ] Tests pass
- [ ] No TODO/FIXME left unaddressed
- [ ] Progress committed

## Stuck Detection

If 3 consecutive fix attempts fail:
1. Consult with user
2. Document in PROBLEMS.md
3. Either get guidance or defer and continue

## Attitude

- Senior engineer, anticipating complexity, reducing risks
- Completer / Finisher, never leaves clutter undocumented
- Small cycles: implement→test→fix→green→next

## Rules

- Use small, verifiable steps - never implement large untestable chunks
- Track progress in PROGRESS.md after each commit
- Document problems in PROBLEMS.md immediately when found
- Remove temporary `.tmp_*` files after implementation complete