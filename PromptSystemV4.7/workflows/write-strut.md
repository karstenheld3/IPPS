---
description: Create STRUT plans with proper format
---

# Write STRUT Workflow

Create or insert a STRUT plan (Structured Thinking notation) into any document.

## Required Skills

- @skills:write-documents for STRUT template and formatting rules
- @skills:promptsystem for the AGEN verb vocabulary (`PROMPTSYSTEM_AGENTIC_ENGLISH.md`)

## MUST-NOT-FORGET

- Final message starts with `Deliverables`: clickable workspace-relative paths (backticked, forward slashes) of main output files + short purpose (`agent-behavior.md` Deliverables first)
- Run `/verify` to validate STRUT structure
- **NEVER modify tracking documents** (PROGRESS.md, PROBLEMS.md, NOTES.md, FAILS.md). Write-* workflows create NEW files only. Tracking docs are session state, not agent operation artifacts.
- Pre-Write Privacy Gate (`agent-behavior.md`): General-purpose documents → all content generic. ILLUSTRATIVE content in any file → examples generic. Assess context BEFORE writing.

## Step 1: Read Template

Read `STRUT_TEMPLATE.md` from the @skills:write-documents skill folder.

Read `PROMPTSYSTEM_AGENTIC_ENGLISH.md` from the @skills:promptsystem skill folder: every step uses a verb from this vocabulary.

## Step 2: Determine Location

STRUT plans go to:
- `_agentwork/__STRUT_[TOPIC].md` - Standalone scaffolding file in the working folder (default, deleted by `/cleanup`)
- `_IMPL_*.md` - Embedded in implementation plans
- `_TASKS_*.md` - Embedded in task plans

## Step 3: Create STRUT

**Goal**: Write a plan that is clear, actionable, and trackable.

Follow `STRUT_TEMPLATE.md` structure exactly.

## Step 4: Verify

Run `/verify` to validate STRUT structure (Planning context).
