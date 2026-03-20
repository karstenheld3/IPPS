---
description: Resume a development session
auto_execution_mode: 1
---

## Required Skills

- @session-management for session file structure

## MUST-NOT-FORGET

- Run `/prime` BEFORE reading session documents
- `/prime` loads FAILS.md, ID-REGISTRY.md, !NOTES.md - critical workspace context

## Step 1: Identify Session

- Path provided with NOTES.md, PROGRESS.md, PROBLEMS.md → use that session
- No path → find most recent:

```powershell
Get-ChildItem -Path "[DEFAULT_SESSIONS_FOLDER]" -Directory -Filter "_*" | Where-Object { Test-Path "$($_.FullName)\NOTES.md" } | Sort-Object { (Get-ChildItem $_.FullName -File | Sort-Object LastWriteTime -Descending | Select-Object -First 1).LastWriteTime } -Descending | Select-Object -First 1 -ExpandProperty FullName
```

## Step 2: Load Context

Run `/prime` now.

## Step 3: Read Session Documents

Read all session documents (NOTES.md, PROGRESS.md, PROBLEMS.md, INFO/SPEC/IMPL/TASK files). Restore phase state from NOTES.md "Current Phase" section. Ensure all state progress documented in NOTES.md, PROGRESS.md, PROBLEMS.md.

## Step 4: Summarize and Propose

Single row: "Read [a] .md files ([b] priority), [c] code files ([d] .py, [e] ...). Mode: [scenario]"

Then summarize findings and propose next steps (max 20 short lines).

## Step 5: Verify MUST-NOT-FORGET

Review each MNF item above and confirm compliance.