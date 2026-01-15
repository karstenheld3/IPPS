---
description: BUILD workflow - create software, features, systems
phase: EXPLORE
---

# Build Workflow

Main entry point for BUILD workflow - creating software, features, systems.

## Required Skills

- @session-management for session setup
- @edird-phase-model for phase details
- @write-documents for document templates

## Usage

```
/build "Add user authentication API"
```

## Step 1: Initialize Session

Run `/session-init` with feature name as topic.

Creates session folder with:
- NOTES.md (with Current Phase tracking)
- PROGRESS.md (with Phase Plan)
- PROBLEMS.md

## Step 1b: Determine Operation Mode

**CRITICAL**: Before any implementation, determine operation mode:

- **IMPL-CODEBASE** (default): Implement in existing codebase
  - For: SPEC, IMPL, TEST, [IMPLEMENT]
  - Files created in project source folders
  - Affects existing code/config/runtime

- **IMPL-ISOLATED**: Implement separately from existing codebase
  - For: [PROVE], POCs, prototypes, self-contained test scripts
  - Files created in `[SESSION_FOLDER]/` or `[SESSION_FOLDER]/poc/`
  - Existing code, configuration, or runtime MUST NOT be affected
  - NEVER create folders in workspace root
  - **REQUIRES SESSION**: If no session exists, run `/session-init` first

Record in NOTES.md:
```markdown
**Operation Mode**: IMPL-CODEBASE
**Target**: src/features/[feature]/
```

## Step 2: EXPLORE Phase

1. [ASSESS] complexity: COMPLEXITY-LOW / MEDIUM / HIGH
2. [ANALYZE] existing code and patterns
3. [GATHER] requirements from user
4. [RESEARCH] if task requires accuracy to external system (cite sources, not training data)
5. [SCOPE] define boundaries

**For UI/game/replica work**: Visual reference (screenshot/video of target) is MANDATORY. Text research alone is insufficient.

### Gate Check: EXPLORE→DESIGN

- [ ] Problem or goal clearly understood
- [ ] Workflow type: BUILD confirmed
- [ ] Complexity assessed
- [ ] Scope boundaries defined
- [ ] No blocking unknowns

**Pass**: Proceed to DESIGN | **Fail**: Continue EXPLORE

## Step 3: DESIGN Phase

1. [PLAN] structured approach
2. [WRITE-SPEC] → `_SPEC_[FEATURE].md`
3. [PROVE] risky parts with POC (if COMPLEXITY-MEDIUM or higher)
4. [WRITE-IMPL-PLAN] → `_IMPL_[FEATURE].md`
5. [WRITE-TEST-PLAN] → `_TEST_[FEATURE].md` (optional for LOW)
6. [DECOMPOSE] into small testable steps

### Gate Check: DESIGN→IMPLEMENT

**MANDATORY ARTIFACT CHECK** (list actual file paths):
- [ ] Spec document: `[SESSION_FOLDER]/_SPEC_*.md` exists (MEDIUM+)
- [ ] Impl plan: `[SESSION_FOLDER]/_IMPL_*.md` exists (MEDIUM+)
- [ ] Visual [PROVE] completed (if UI/game work)
- [ ] No open questions

**Gate evidence format**:
```
Artifacts created:
- _SPEC_FEATURE.md (X lines)
- _IMPL_FEATURE.md (Y lines)
- POC verified: [screenshot/description]
```

**Pass**: Proceed to IMPLEMENT | **Fail**: Continue DESIGN

**WARNING**: Claiming gate pass without listing actual artifacts is gate bypass (see GLOB-FL-004).

## Step 4: IMPLEMENT Phase

For each step in IMPL plan:

1. [IMPLEMENT] code changes (max 100 lines before visual check for UI work)
2. [TEST] verify step works (visual verification for UI/game)
3. [FIX] if tests fail (max 3 retries, then [CONSULT])
4. [COMMIT] when green
5. Update PROGRESS.md

**UI/Game rule**: Never implement >100 lines without visual verification. Monolithic implementation is forbidden.

### Gate Check: IMPLEMENT→REFINE

- [ ] All IMPL steps complete
- [ ] Tests pass
- [ ] No TODO/FIXME unaddressed
- [ ] Progress committed

**Pass**: Proceed to REFINE | **Fail**: Continue IMPLEMENT

## Step 5: REFINE Phase

1. [REVIEW] self-review of work
2. [VERIFY] against spec/rules
3. [TEST] regression testing
4. [CRITIQUE] and [RECONCILE] (if MEDIUM+)
5. [FIX] issues found

### Gate Check: REFINE→DELIVER

- [ ] Self-review complete
- [ ] Verification passed
- [ ] Critique/reconcile done (if MEDIUM+)
- [ ] All issues fixed

**Pass**: Proceed to DELIVER | **Fail**: Continue REFINE

## Step 6: DELIVER Phase

1. [VALIDATE] with user (final approval)
2. [MERGE] branches if applicable
3. [FINALIZE] documentation
4. [CLOSE] mark as done
5. Run `/session-close`

## Phase Tracking

Update NOTES.md after each phase:

```markdown
## Current Phase

**Phase**: IMPLEMENT
**Last verb**: [TEST]-OK
**Gate status**: 3/4 items checked
```

## Stuck Detection

If 3 consecutive [FIX] attempts fail:
1. Document in PROBLEMS.md
2. [CONSULT] with user
3. Wait for guidance or [DEFER]
