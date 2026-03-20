---
description: Initialize a new development session
auto_execution_mode: 1
---

## Required Skills

- @session-management for session folder structure and tracking files

## Step 1: Check for Existing Session

If [SESSION_FOLDER] already contains NOTES.md, PROGRESS.md, PROBLEMS.md: run `/session-load` instead.

## Step 2: Create Session Folder

If no [SESSION_FOLDER] provided, create in default sessions folder:
`_YYYY-MM-DD_[PROBLEM_DESCRIPTION]/` (alphanumeric only, no spaces)

## Step 3: Create Session Documents

Create from @session-management templates in [SESSION_FOLDER]:

- `NOTES.md` - Include "Current Phase" section. Record large user prompts (>120 tokens) verbatim in "User Prompts" section
- `PROGRESS.md` - Include "Phase Plan" with 5 phases
- `PROBLEMS.md` - Derive all problems from user's request. Each gets ID `[TOPIC]-PR-[NNN]` in "Open" section

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

Read rules in windsurf rules folder, write key instructions into NOTES.md under "IMPORTANT: Cascade Agent Instructions".

See `devsystem-core.md` sections "Document Types" and "Tracking Documents" for full list.

**Acronym expansion rule**: Always spell out acronyms fully in NOTES.md. Example: "APAPALAN: As Precise As Possible, As Little As Necessary" not just "APAPALAN principle".