---
description: Save session progress
auto_execution_mode: 3
---

# Save Session Workflow

**Goal**: Session progress persisted in tracking files and committed.

**Why**: Unsaved progress is lost when the conversation ends.

## Required Skills

- @skills:session-management for session file structure
- @skills:git-conventions for commit format

## MUST-NOT-FORGET

- Document only verified facts; mark with `[TESTED]` or `[ASSUMED]`
- Update all session files, then sync topic folder progress to the parent PROGRESS.md
- Run `/commit` last

Re-read the entire conversation and find:
- New problems found -> to be documented in session PROBLEMS.md
- Important findings -> to be documented in session NOTES.md
- Things that did work and things that didn't -> to be documented in session PROGRESS.md
- Be very careful to NOT document assumptions that are not verified.
- Wait until tests and pocs prove what is working and what not.
- Use [TESTED] and [ASSUMED] markers

Compare all changes since the last commit and summarize.
 -> to be documented in session PROGRESS.md

Update all session files.

## Topic Folder Sync

Run @skills:session-management **Topic Folder Save Sync** procedure. If working in `T##_*` folder, sync progress summary to parent PROGRESS.md.

## Commit

Run `/commit` workflow.