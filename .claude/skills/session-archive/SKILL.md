---
name: session-archive
description: Archive a completed session folder
disable-model-invocation: true
---

# Archive Session Workflow

**Goal**: Completed session folder moved to the archive folder and committed.

**Why**: Archiving removes finished work from active context and keeps it recoverable.

## Required Skills

- @skills:session-management for archive conventions

Use this workflow to move a completed session folder to the archive folder `[WORKSPACE_FOLDER]/_archive_gitignore/` (`[SESSION_ARCHIVE_FOLDER]`). The archive folder is not versioned; git history keeps the session content.

## MUST-NOT-FORGET

- Run `/cleanup [SESSION_FOLDER]` first when `_agentwork` or `.tmp_*` folders exist
- Never overwrite an existing archived folder of the same name
- Run `git add` and `git commit` as two separate commands

## Steps

0. **Check for deletable leftovers**
   - Search `[SESSION_FOLDER]` with `find_by_name` for directories named `_agentwork` and directories starting with `.tmp_` (Type `directory`)
   - If any found: run `/cleanup [SESSION_FOLDER]` first. Archive expects no `_agentwork/` and no `.tmp_*` folder to remain

1. **Move session folder to the archive folder**
// turbo
   ```powershell
   New-Item -ItemType Directory -Path "[SESSION_ARCHIVE_FOLDER]" -Force | Out-Null
   Move-Item -Path "[SESSION_FOLDER]" -Destination "[SESSION_ARCHIVE_FOLDER]"
   ```
   Replace `[SESSION_FOLDER]` with actual folder name (e.g., `_2026-01-10_DontOverwriteWithEmptyValues`). Never overwrite an existing archived folder of the same name; use a `_v2`, `_v3` suffix for the new name

2. **Commit archive**
// turbo
   ```powershell
   git add -A
   git commit -m "[type](scope): [description] - archive session"
   ```
   Run as two separate commands (inline whitelist: no chained statements)

## Example

```powershell
Move-Item -Path "_2026-01-10_DontOverwriteWithEmptyValues" -Destination "[WORKSPACE_FOLDER]\_archive_gitignore\"
git add -A
git commit -m "fix(sap-import): preserve user data during SAP import - archive session"
```

## Agent-Created Folders

- `_archive_gitignore/` - role: archive; parent: workspace root; creator: Step 1; content: archived session folders
