---
description: Initialize a new development session
auto_execution_mode: 1
---

## Required Skills

- @session-management for session folder structure and tracking files

## Step 1: Check for Existing Session

Check if user provided a [SESSION_FOLDER].
If path already contains NOTES.md, PROGRESS.md, PROBLEMS.md: Execute `/session-load` instead.

## Step 2: Create Session Folder

If no [SESSION_FOLDER] provided, create in default sessions folder:
`_YYYY-MM-DD_[PROBLEM_DESCRIPTION]/`
[PROBLEM_DESCRIPTION]: alphanumerical only, no spaces.

## Step 3: Create Session Documents

Create tracking files from @session-management templates in [SESSION_FOLDER]:

- `NOTES.md` - Include "Current Phase" section. If user prompt >120 tokens, record verbatim in "User Prompts" section
- `PROGRESS.md` - Include "Phase Plan" section with 5 phases
- `PROBLEMS.md` - Derive all problems from user's initial request. Each gets unique ID `[TOPIC]-PR-[NNN]` in "Open" section

## Step 4: Initialize Phase Tracking

Add to NOTES.md:
```markdown
## Current Phase

**Phase**: EXPLORE
**Workflow**: (pending assessment)
**Assessment**: (pending)
```

Add to PROGRESS.md:
```markdown
## Phase Plan

- [ ] **EXPLORE** - in_progress
- [ ] **DESIGN** - pending
```

## Step 5: Document Agent Instructions

**Session documents**: See `devsystem-core.md` sections "Document Types" and "Tracking Documents" for full list.

Read rules in windsurf rules folder, write key instructions into NOTES.md under "IMPORTANT: Cascade Agent Instructions".

**Acronym expansion rule**: Always spell out acronyms fully in NOTES.md so agent understands without external context. Example: "APAPALAN: As Precise As Possible, As Little As Necessary" not "APAPALAN principle".