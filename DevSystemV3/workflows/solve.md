---
description: SOLVE workflow - explore problems, evaluate ideas, make decisions
phase: EXPLORE
---

# Solve Workflow

Main entry point for SOLVE workflow - research, analysis, evaluation, decisions.

## Required Skills

- @session-management for session setup
- @edird-phase-model for phase details
- @write-documents for document templates

## Usage

```
/solve "Research authentication best practices"
/solve "Analyze why API returns 500 errors"
/solve "Evaluate database migration options"
```

## Step 1: Initialize Session

Run `/session-init` with task name as topic.

Creates session folder with:
- NOTES.md (with Current Phase tracking)
- PROGRESS.md (with Phase Plan)
- PROBLEMS.md

## Step 1b: Determine Operation Mode

**CRITICAL**: Before any implementation, determine operation mode:

- **IMPL-CODEBASE** (default): Implement in existing codebase
  - For: SPEC, IMPL, TEST, [IMPLEMENT], HOTFIX, BUGFIX
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
**Operation Mode**: IMPL-ISOLATED
**Output Location**: [SESSION_FOLDER]/poc/
```

## Step 2: EXPLORE Phase

1. [ASSESS] problem type:
   - RESEARCH - Gather information on a topic
   - ANALYSIS - Deep dive into code/data/behavior
   - EVALUATION - Compare options and make recommendations
   - WRITING - Create documentation or content
   - DECISION - Make a choice between alternatives
   - HOTFIX - Urgent production fix
   - BUGFIX - Non-urgent defect resolution

2. [RESEARCH] existing information (MANDATORY if research triggers detected - cite sources)
3. [ANALYZE] the problem space
4. [SCOPE] define boundaries

### Gate Check: EXPLORE→DESIGN

- [ ] Problem clearly understood
- [ ] Workflow type: SOLVE confirmed
- [ ] Problem type assessed
- [ ] Scope boundaries defined
- [ ] No blocking unknowns

**Pass**: Proceed to DESIGN | **Fail**: Continue EXPLORE

## Step 3: DESIGN Phase

1. [PLAN] approach to solving
2. [OUTLINE] structure for output
3. [WRITE-INFO] → `_INFO_[TOPIC].md` (if research needed)
4. [VALIDATE] approach with user (if needed)

### For RESEARCH / ANALYSIS

- Focus on information gathering
- Output: INFO document with findings

### For EVALUATION / DECISION

- Focus on options comparison
- Output: INFO document with recommendations

### For HOTFIX / BUGFIX

- Focus on root cause identification
- Output: Fix plan, then switch to BUILD mode

### Gate Check: DESIGN→IMPLEMENT

- [ ] Approach documented
- [ ] Structure/criteria validated
- [ ] No open questions

**Pass**: Proceed to IMPLEMENT | **Fail**: Continue DESIGN

## Step 4: IMPLEMENT Phase

1. [EXECUTE] the plan:
   - For RESEARCH: [GATHER] → [SYNTHESIZE]
   - For ANALYSIS: [INVESTIGATE] → [ANALYZE]
   - For EVALUATION: [EVALUATE] → [COMPARE]
   - For WRITING: [DRAFT] → [EDIT]
   - For DECISION: [WEIGH] → [DECIDE]
   - For HOTFIX/BUGFIX: [FIX] → [TEST]

2. [DOCUMENT] findings in session docs
3. Update PROGRESS.md

### Gate Check: IMPLEMENT→REFINE

- [ ] Core work complete
- [ ] All sections drafted
- [ ] Progress documented

**Pass**: Proceed to REFINE | **Fail**: Continue IMPLEMENT

## Step 5: REFINE Phase

1. [REVIEW] self-review of work
2. [VERIFY] claims and findings
3. [CRITIQUE] arguments (find weak points)
4. [RECONCILE] ideal vs practical
5. [IMPROVE] clarity and quality

### Gate Check: REFINE→DELIVER

- [ ] Self-review complete
- [ ] Claims verified
- [ ] Arguments strengthened
- [ ] Quality improved

**Pass**: Proceed to DELIVER | **Fail**: Continue REFINE

## Step 6: DELIVER Phase

1. [CONCLUDE] draw final conclusions
2. [RECOMMEND] with rationale (or [PROPOSE] if multiple options)
3. [PRESENT] findings to user
4. [VALIDATE] with user
5. [CLOSE] mark as done
6. Run `/session-close`

## Phase Tracking

Update NOTES.md after each phase:

```markdown
## Current Phase

**Phase**: IMPLEMENT
**Problem Type**: RESEARCH
**Last verb**: [SYNTHESIZE]-OK
**Gate status**: 2/3 items checked
```

## Problem Type Quick Reference

| Type | Focus | Primary Output |
|------|-------|----------------|
| RESEARCH | Information gathering | INFO document |
| ANALYSIS | Understanding behavior | Findings + root cause |
| EVALUATION | Options comparison | Recommendations |
| WRITING | Content creation | Document/content |
| DECISION | Choice making | Decision + rationale |
| HOTFIX | Urgent fix | Working fix + deploy |
| BUGFIX | Defect resolution | Fix + regression tests |
