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
- Impact Assessment is MANDATORY before implementation
- Run `/verify` after implementation complete
- INFO only → `/write-spec` | SPEC only → `/write-impl-plan` | IMPL only → `/write-test-plan`

## GLOBAL-RULES

Apply to ALL implementation contexts. Goal: Understand full impact before making changes.

1. Trace scope - Identify all artifacts affected by the change (direct and indirect)
2. Assess impact - Determine what functionality depends on affected artifacts
3. Define verification - Create checkpoints to catch regressions early

Document rules:
- IMPL exists → Add "Impact Analysis" section to IMPL
- No IMPL + multi-file change → Create IMPL with analysis
- TEST exists → Add new test cases to TEST
- No TEST + multi-file change → Create TEST

# CONTEXT-SPECIFIC

## No Documents

Implement whatever was proposed or specified in conversation.

## Prerequisites Missing

- INFO only → `/write-spec` first
- SPEC only → `/write-impl-plan` first
- IMPL only → `/write-test-plan` first

## Ready to Implement

Entry: IMPL plan exists. TEST exists (no code) → implement skeletons then failing tests. TEST + code → proceed.

### Operation Mode Check

From NOTES.md: IMPL-CODEBASE → project source folders | IMPL-ISOLATED → `[SESSION_FOLDER]/` only, NEVER workspace root

### Impact Assessment

MANDATORY. Apply GLOBAL-RULES with code focus:

1. List all code paths interacting with target locations
2. Identify dependent functionality: callers, consumers, UI components, endpoints, test files
3. Create test cases for each impacted area BEFORE implementing

### Execution Sequence

1. For each IMPL step: implement → run tests → fix if fail → commit when green
2. Run `/verify` against IMPL plan

### Gate Check: IMPLEMENT→REFINE

- [ ] All steps from IMPL plan implemented
- [ ] Tests pass
- [ ] No TODO/FIXME left unaddressed
- [ ] Progress committed

Pass: `/refine` | Fail: Continue implementing

## Stuck Detection

3 consecutive fix attempts fail:
1. Ask user for guidance
2. Document in PROBLEMS.md
3. Get guidance or defer and continue

## Rules

- Profile: Senior engineer, completer/finisher. Small cycles: implement → test → fix → green → next
- Never implement large untestable chunks
- Track progress in PROGRESS.md after each commit
- Document problems in PROBLEMS.md immediately
- Remove `.tmp_*` files after implementation complete