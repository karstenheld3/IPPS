---
description: Fix bugs - record, investigate, create [BUG_FOLDER], test, commit, update docs (renamed from fix.md)
---

# Bugfix Workflow

## Required Skills

- @write-documents for INFO, STRUT, and FIXES templates
- @coding-conventions for code changes
- @session-management for session setup (PROJECT-MODE only)

## MUST-NOT-FORGET

- Determine context FIRST: SESSION-MODE or PROJECT-MODE
- Always create `[BUG_FOLDER]` (both contexts)
- Impact assessment BEFORE implementing fix
- Test impacted functionality BEFORE committing
- Run `/learn` after fix is verified (optional but recommended)

## Trigger

- `/bugfix [problem-description]` - Known problem
- `/bugfix` - Discovery mode

## Quick Reference

SESSION-MODE (bug during active session):
- Bug ID: `[TOPIC]-BG-NNNN`, Folder: `[SESSION_FOLDER]/[TOPIC]-BG-NNNN_Desc/`
- Docs: SPEC, IMPL, TEST. Commit: `fix([TOPIC]-BG-NNNN): description`

PROJECT-MODE (bug after session closed):
- Bug ID: `GLOB-BG-NNNN`, Folder: `[BUGFIXES_FOLDER]/GLOB-BG-NNNN_Desc/`
- Docs: SPEC, IMPL, TEST + `*_FIXES.md`. Commit: `fix(GLOB-BG-NNNN): description`
- `[BUGFIXES_FOLDER]` = `[DEFAULT_SESSIONS_FOLDER]/_BugFixes/`

## Step 1: Determine Context

SESSION-MODE: `[SESSION_FOLDER]` exists, bug found while working. Fix in session folder, `[TOPIC]-BG-NNNN` ID. No `*_FIXES.md`.

PROJECT-MODE: No active session. Fix in persistent `_BugFixes` session (never archived), `GLOB-BG-NNNN` ID. Also create/update `*_FIXES.md` next to component IMPL or SPEC doc.

[BUG_FOLDER] structure (both modes):
```
[BUG_FOLDER]/
├── PROBLEMS.md
├── _INFO_*.md, _STRUT_*.md
├── backup/, poc/, test/
```

## Step 2: Ensure _BugFixes Session Exists (PROJECT-MODE only)

1. Read `!NOTES.md` for `[BUGFIXES_FOLDER]` path
2. If not exists, create with NOTES.md, PROBLEMS.md, PROGRESS.md, FAILS.md
3. This session is PERMANENT - never archived

SESSION-MODE: Skip, use current `[SESSION_FOLDER]`

## Step 3: Record Problem

Discovery mode (no description): analyze conversation for errors, check test output, look for failure phrases. Nothing found → exit "No issues detected".

Record in PROBLEMS.md:
- SESSION-MODE: `[SESSION_FOLDER]/PROBLEMS.md`, `[SESSION_TOPIC]-PR-NNNN`
- PROJECT-MODE: `[BUGFIXES_FOLDER]/PROBLEMS.md`, `GLOB-PR-NNNN`

Entry: ID, Status: Open, Reported timestamp, verbatim prompt, initial assessment.

## Step 4: Analyze and Create [BUG_FOLDER]

1. Make assumptions about causes, search code, verify each
2. Confirm as **bug** when deviation from desired behavior prevents goal

Bug = flaw in code, IMPL design, library behavior assessment, or SPEC assumption.

Create [BUG_FOLDER] only when confirmed:
- SESSION-MODE: next BG number from `[SESSION_FOLDER]/NOTES.md` "Bug List"
- PROJECT-MODE: next BG number from `[BUGFIXES_FOLDER]/NOTES.md`

Create `PROBLEMS.md` inside. Update parent PR entry: "→ Now tracked as [BG-ID]"

## Step 5: Reproduce Bug

- Use `.tmp` scripts or Playwright MCP, artifacts ONLY in `[BUG_FOLDER]`
- Verify bug exists before changes
- 3 failed attempts → [CONSULT] with user

## Step 6: Deep Analysis

Run `/write-info` → `_INFO_*.md` in `[BUG_FOLDER]`: evidence, observations, root cause hypothesis.

## Step 7: Develop Plan

Run `/write-strut` → fix plan with verifiable phases, testing actions, backup to `[BUG_FOLDER]/backup/`. NEVER commit untested code. Verify assumptions first, test in POCs for medium complexity, add logging before conclusions.

## Step 8: Impact Assessment

MANDATORY before implementing:
1. List all code paths interacting with fix location
2. Identify dependent functionality (callers, UI, endpoints, tests)
3. Document in `[BUG_FOLDER]/PROBLEMS.md`
4. Create test cases for each impacted area BEFORE fix

## Step 9: Execute Plan

Run `/implement`: small cycles (implement → test → fix → green → next). For complex plans: `/write-tasks-plan` and `/write-test-plan`. Update tracking docs frequently.

## Step 10: Final Verification and Documentation

### 10.1 Verify Fix
- BEFORE/AFTER comparison using backup. All tests must pass.

### 10.2 Update Documentation
ALWAYS: Update SPEC, IMPL, TEST for newly discovered scenario.
PROJECT-MODE only: Create/update `*_FIXES.md` next to `*_IMPL_*.md` (or `*_SPEC_*.md` if no IMPL).

### 10.3 Commit
Run `/commit`: `fix([BG-ID]): description`

### 10.4 Mark Resolved
Update PROBLEMS.md: Status: Resolved, timestamp, solution description.

## Step 11: Completion Checklist

- [ ] Context determined (SESSION-MODE or PROJECT-MODE)
- [ ] `[BUG_FOLDER]` created with all artifacts
- [ ] Impact assessment documented
- [ ] All impacted functionality tested and passing
- [ ] SPEC/IMPL/TEST docs updated with new scenario
- [ ] `*_FIXES.md` created/updated (PROJECT-MODE only)
- [ ] PROBLEMS.md entry marked Resolved
- [ ] Clean commit with proper message format

## Post-Fix

Run `/learn` to extract lessons from this fix.

## _FIXES.md Format (PROJECT-MODE only)

```markdown
### GLOB-BG-NNNN IssueDescription

**Problem**: Single sentence
**Solution**: Single sentence

**Changed or added files**:
- `path/to/file.py` - What was changed
```