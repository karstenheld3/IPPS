---
description: Execute implementation from context, INFO, SPEC or IMPL documents
auto_execution_mode: 1
---

# Implement Workflow

## Required Skills

- @coding-conventions for coding style
- @write-documents for tracking

## MUST-NOT-FORGET

Flow: Prerequisites → GLOBAL-RULES → Impact Assessment → Execution

- Prerequisites ensure required documents (SPEC, IMPL, TEST) exist
- GLOBAL-RULES apply BEFORE any code change
- Impact Assessment MANDATORY before implementation
- Run `/verify` after implementation complete

Prerequisites quick ref:
- INFO only → `/write-spec`
- SPEC only → `/write-impl-plan`
- IMPL only → `/write-test-plan`

## GLOBAL-RULES

Apply to ALL contexts. Goal: Understand full impact before changes.

1. Trace scope - all artifacts affected (direct and indirect)
2. Assess impact - what functionality depends on affected artifacts
3. Define verification - checkpoints to catch regressions early

Document rules:
- IMPL exists → Add "Impact Analysis" section to IMPL
- No IMPL + multi-file change → Create IMPL with analysis
- TEST exists → Add new test cases to TEST
- No TEST + multi-file change → Create TEST

# CONTEXT-SPECIFIC

## No Documents

Implement whatever was proposed or specified in conversation.

## Prerequisites Missing

- INFO only → Run `/write-spec` first
- SPEC only → Run `/write-impl-plan` first
- IMPL only → Run `/write-test-plan` first

## Ready to Implement

Entry conditions:
- IMPL plan exists
- TEST exists (no test code) → Implement function skeletons, then failing tests
- TEST + test code exists → Proceed to implementation

### Operation Mode Check

Verify from NOTES.md before any code changes:
- IMPL-CODEBASE → output to project source folders
- IMPL-ISOLATED → output to `[SESSION_FOLDER]/` only, NEVER workspace root

### Impact Assessment

MANDATORY. Apply GLOBAL-RULES with code-specific focus:

1. List all code paths interacting with target locations
2. Identify dependent functionality:
   - Callers and consumers
   - UI components
   - Other endpoints
   - Test files
3. Create test cases for each impacted area BEFORE implementing

### Execution Sequence

1. For each IMPL plan step:
   - Implement code changes
   - Run tests to verify
   - Fix if tests fail (per retry limits)
   - Commit when green
2. Run `/verify` against IMPL plan

### Gate Check: IMPLEMENT→REFINE

- [ ] All steps from IMPL plan implemented
- [ ] Tests pass
- [ ] No TODO/FIXME left unaddressed
- [ ] Progress committed

Pass: Run `/refine` | Fail: Continue implementing

## Stuck Detection

If 3 consecutive fix attempts fail:
1. Ask user for guidance
2. Document in PROBLEMS.md
3. Either get guidance or defer and continue

## Attitude

- Senior engineer, anticipating complexity, reducing risks
- Completer/Finisher, never leaves clutter undocumented
- Small cycles: implement → test → fix → green → next

## Rules

- Small, verifiable steps - never large untestable chunks
- Track progress in PROGRESS.md after each commit
- Document problems in PROBLEMS.md immediately
- Remove `.tmp_*` files after implementation complete