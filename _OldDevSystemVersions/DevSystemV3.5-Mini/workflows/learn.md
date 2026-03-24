---
description: Extract lessons from resolved problems through structured retrospective analysis
auto_execution_mode: 1
---

# Learn Workflow

Run after a problem is marked resolved in PROBLEMS.md to extract transferable lessons.

## Required Skills

- @write-documents for LEARNINGS_TEMPLATE.md structure

## MUST-NOT-FORGET

- Run `/fail` first in discovery mode (no args)
- Session entries sync to workspace on `/session-finalize`

## Trigger

- Problem marked as resolved in PROBLEMS.md
- `/learn [TOPIC]-PR-NNN` or `/learn` (discovery mode)

## Step 0: Discovery Mode (no context provided)

1. Run `/fail` to detect current issues
2. If `/fail` creates entry, use as learning target
3. If no issues found, report "No failures detected" and exit

## Step 1: Identify Problem

Read resolved problem entry: ID, description, solution, linked FAILS.md entries.

## Step 2: Classify Problem Type

BUILD: COMPLEXITY-LOW / COMPLEXITY-MEDIUM / COMPLEXITY-HIGH

SOLVE: RESEARCH / ANALYSIS / EVALUATION / WRITING / DECISION / HOTFIX / BUGFIX / CHORE / MIGRATION

## Step 3: Reconstruct Context

From conversation history, commits, documents:
1. What information was available at decision time?
2. What was NOT available but should have been?
3. What constraints existed?

## Step 4: Reconstruct Assumptions

List all assumptions. Mark: `[VERIFIED]`, `[UNVERIFIED]`, `[CONTRADICTS]`

## Step 5: Reconstruct Rationale

1. Requirements specified? (FR, DD, IG references)
2. Design decisions and why?
3. Trade-offs accepted?

## Step 6: Compare to Actual Outcome

1. What actually happened?
2. Where did plan diverge from reality?
3. What signals were missed?

## Step 7: Collect Evidence

Gather: conversation excerpts, code diffs, error logs, document references (SPEC, IMPL, TEST)

## Step 8: Build Problem Dependency Tree

```
[Root Cause]
├─> [Contributing Factor 1]
│   └─> [Symptom A]
└─> [Contributing Factor 2]
    ├─> [Symptom B]
    └─> [Symptom C]
```

Work backwards from symptoms to root cause.

## Step 9: Identify Root Cause and Prevention

1. Root cause: Single sentence identifying fundamental issue
2. Counterfactual: "If we had [X], then [Y]"
3. Prevention: "Next time, we should [actionable guidance]"

## Step 10: Create Learning Entry

1. Location (SESSION-FIRST rule):
   - SESSION-MODE → `[SESSION_FOLDER]/LEARNINGS.md` (create if needed, syncs on `/session-finalize`)
   - PROJECT-MODE → `[WORKSPACE_FOLDER]/LEARNINGS.md`
2. Assign ID: `[TOPIC]-LN-[NNN]`
3. Fill all sections from steps 2-9
4. Place at top of file

## Step 11: Update Linked FAILS Entries

1. Find FAILS.md entries with matching TOPIC or problem reference
2. Update "Why it went wrong" with root cause insight
3. Update "Suggested fix" with prevention guidance
4. Add code examples if applicable

## Quality Gate

- [ ] Problem type correctly classified
- [ ] All assumptions identified and labeled
- [ ] Root cause is actionable (not just "we made a mistake")
- [ ] Prevention guidance is specific (not just "be more careful")
- [ ] Linked FAILS entries updated