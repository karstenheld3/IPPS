---
description: Document synchronization
auto_execution_mode: 1
---

# Sync Workflow

## Required Skills

- @write-documents for document formatting rules
- @coding-conventions for code-related sync

## Workflow

1. Determine sync context (Code→Docs, SPEC→Downstream, IMPL→TEST, Session→Project, etc.)
2. Read GLOBAL-RULES
3. Read relevant Context-Specific section
4. Create sync task list
5. Execute sync task list
6. Run Final Steps

## GLOBAL-RULES

- Read source document/code BEFORE updating dependents
- Preserve existing IDs (FR-XX, DD-XX) - never renumber
- Add new items at end of section with next available number
- Mark synced items with timestamp in Document History
- Update verification labels on status change: `[TESTED]`/`[PROVEN]`/`[VERIFIED]`
- Keep formatting consistent with target document style
- Never delete content without explicit user confirmation

## Sync Direction Reference

```
Code Changes
├─> IMPL (implementation details)
├─> SPEC (if behavior changed)
└─> TEST (expected results)

SPEC Changes
├─> IMPL (add/update steps)
└─> TEST (add/update cases)

IMPL Changes
├─> SPEC (if reveals spec gaps)
└─> TEST (edge case updates)

Session Documents
├─> Project NOTES.md (reusable decisions, patterns)
├─> Project PROBLEMS.md (resolved issues with project impact)
└─> Project PROGRESS.md (completed milestones)

Major Project Changes
├─> README.md (features, structure, usage)
├─> NOTES.md (conventions, topic registry)
└─> PROGRESS.md (milestones, versions)
```

## Final Steps

1. Re-read all modified documents
2. [VERIFY] cross-references valid (IDs exist in source)
3. Update Document History in each modified file
4. Check for orphaned references

# CONTEXT-SPECIFIC

## Code→Docs

Detect: Compare behavior vs SPEC, approach vs IMPL. Note deviations.

- **IMPL**: Update changed steps, add EC-XX discovered, mark completed in checklist
- **SPEC**: Update FR-XX if interpretation changed, add DD-XX for new decisions, update IG-XX
- **TEST**: Update TC-XX results if behavior changed, add TC-XX for new edge cases

## SPEC→Downstream

- **IMPL**: Add steps for new FR-XX, update affected steps, add edge case handling
- **TEST**: Add TC-XX per new FR-XX, update for changed requirements, remove/mark obsolete TC-XX

## IMPL→TEST

- Add TC-XX for new EC-XX edge cases
- Update test phases if order changed
- Add setup/teardown for new dependencies

## Session→Project

**NOTES.md**: Key Decisions → Project NOTES.md; Agent Instructions → rules/NOTES.md; Findings → relevant SPEC/INFO

**PROBLEMS.md**: Resolved with impact → Project PROBLEMS.md; Unrelated bugs → PROBLEMS.md or issues; Deferred → PROBLEMS.md with priority

**PROGRESS.md**: Completed milestones → Project PROGRESS.md; Tried But Not Used → Project NOTES.md; Coverage changes → TEST documents

## Verification Label Updates

Promote: `[ASSUMED]`→`[VERIFIED]` (confirmed) → `[TESTED]` (POC works) → `[PROVEN]` (in production)

Where: INFO (source claims), SPEC (decisions/assumptions), IMPL (edge case choices), TEST (expected behaviors)

## Cross-Document Reference Sync

Check: IMPL refs to SPEC (FR-XX, DD-XX, IG-XX), TEST refs to SPEC+IMPL (FR-XX, EC-XX), "Depends on" headers

Fix: Update renumbered IDs, remove deleted refs, note moved targets