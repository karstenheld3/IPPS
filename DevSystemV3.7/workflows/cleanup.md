---
description: Delete temporary files and artifacts left by workflows and skills
auto_execution_mode: 1
---

# Cleanup Workflow

Delete temporary files, build artifacts, and workflow leftovers from workspace and tools folders.

**Goal**: Clean workspace with all temporary and intermediate files removed

**Why**: Workflows and skills leave behind temp scripts, Python cache, versioned backups, and MCP config backups that accumulate over time

Scope: File deletion only. Does NOT uninstall tools, remove sessions, or modify source code.

## MUST-NOT-FORGET

- Scan BEFORE deleting - always preview first, never delete without showing what will be removed
- NEVER delete `../.tools/` output folders (see Protected Locations)
- NEVER delete `/bugfix` `backup/` folders or `/go` backups/zips
- Confirmation required before any deletion (destructive workflow)

## Trigger

- `/cleanup` - scan entire workspace and known locations
- `/cleanup [path]` - scan only specified path

## GLOBAL-RULES

Apply to all cleanup runs regardless of scope.

1. Scan all target locations and collect file list BEFORE deleting anything
2. Group findings by category in preview
3. Show full paths in preview - never abbreviate or truncate
4. Require explicit user confirmation after preview
5. Report deletion results with counts per category

# CONTEXT-SPECIFIC

Detection: determine applicable contexts from scope. Multiple contexts may apply in a single run.

## File Cleanup

**Applies**: Always (every `/cleanup` run)

Delete files and directories matching these patterns:

### 1. Agent Temp Files

- **Pattern**: `.tmp_*` files, `*.tmp` files
- **Locations**: `[WORKSPACE_FOLDER]` recursive, `[DEFAULT_SESSIONS_FOLDER]` recursive
- **Source**: Agent scripts, `/test`, `/implement`, `/go`, `/improve` STRUT plans, youtube-downloader metadata

### 2. Python Build Artifacts

- **Pattern**: `__pycache__/` directories, `*.pyc` files, `.pytest_cache/`, `.mypy_cache/`
- **Locations**: `[WORKSPACE_FOLDER]` recursive, `[DEVSYSTEM_FOLDER]` recursive, `[AGENT_FOLDER]` recursive
- **Source**: Python script execution

### 3. Improve Workflow Artifacts

- **Pattern**: `*_vN.*` versioned backups (filename ending in `_v` followed by digits before extension), `*_DEFERRED_IMPROVEMENTS.md`
- **Locations**: `[WORKSPACE_FOLDER]` recursive, excluding `_Archive/` and `_OldDevSystemVersions/`
- **Source**: `/improve` workflow versioned backups and deferred improvement logs

### 4. MCP Config Backups

- **Pattern**: `mcp_config.json._beforeRemoving*`, `mcp_config.json._backup_*`
- **Location**: MCP config directory (resolve from Windsurf/Codeium config path)
- **Source**: MCP server install/uninstall scripts (ms-playwright-mcp, playwriter-mcp)

## INFO Document Cleanup

**Applies**: When `_INFO_*.md` files exist in scope (excluding `_Archive/` and `_OldDevSystemVersions/`)

Strip verification markers in-place (text modification, not file deletion):

- **Pattern**: `[VERIFIED]` labels, `VERIFIED, ` prefixes
- **Source**: `/research`, `/write-info`, `/verify` workflows add these during authoring. After content is finalized, markers are noise.

## No Context Match

If scope contains no matching patterns and no INFO documents:
- Report "Workspace is clean - nothing to delete" and exit

## Protected Locations (NEVER Delete)

These folders and their contents are EXCLUDED from all cleanup operations:

- `[WORKSPACE_FOLDER]/../.tools/_pdf_to_jpg_converted/` - PDF conversion output
- `[WORKSPACE_FOLDER]/../.tools/_pdf_output/` - Compressed PDF output
- `[WORKSPACE_FOLDER]/../.tools/_screenshots/` - Desktop screenshots
- `[WORKSPACE_FOLDER]/../.tools/_web_screenshots/` - Web page screenshots
- `[WORKSPACE_FOLDER]/../.tools/_image_to_markdown/` - Transcription intermediates
- `[WORKSPACE_FOLDER]/../.tools/_installer/` - Downloaded tool installers
- `*/backup/` inside `_BugFixes/` session folders - `/bugfix` recovery data
- Any `.zip` or backup created by `/go` workflow

# EXECUTION

## Step 1: Determine Scope and Context

- No args → scan `[WORKSPACE_FOLDER]` and all known locations
- Path arg → scan only that path

Read NOTES.md to resolve `[DEFAULT_SESSIONS_FOLDER]` and `[DEVSYSTEM_FOLDER]`.

Detect applicable contexts:
- File Cleanup: always active
- INFO Document Cleanup: active if `_INFO_*.md` files exist in scope

## Step 2: Scan

Scan per active context. Collect full paths.

**File Cleanup scan:**

```powershell
# 1. Agent temp files
Get-ChildItem -Path "[SCOPE]" -Recurse -File | Where-Object { $_.Name -like '.tmp_*' -or $_.Name -like '*.tmp' }

# 2. Python artifacts
Get-ChildItem -Path "[SCOPE]" -Recurse -Directory | Where-Object { $_.Name -in @('__pycache__', '.pytest_cache', '.mypy_cache') }
Get-ChildItem -Path "[SCOPE]" -Recurse -File -Filter "*.pyc"

# 3. Improve artifacts (_vN backups: filename_vN.ext where N is one or more digits)
Get-ChildItem -Path "[SCOPE]" -Recurse -File | Where-Object { $_.BaseName -match '_v\d+$' -and $_.DirectoryName -notmatch '_Archive|_OldDevSystemVersions' }
Get-ChildItem -Path "[SCOPE]" -Recurse -File -Filter "*_DEFERRED_IMPROVEMENTS.md" | Where-Object { $_.DirectoryName -notmatch '_Archive|_OldDevSystemVersions' }

# 4. MCP config backups (resolve MCP config directory first)
Get-ChildItem -Path "[MCP_CONFIG_DIR]" -File | Where-Object { $_.Name -match '^mcp_config\.json\._' }
```

**INFO Document Cleanup scan:**

```powershell
# 5. INFO verification markers (count files and occurrences)
Get-ChildItem -Path "[SCOPE]" -Recurse -File -Filter "_INFO_*.md" | Where-Object {
    $_.DirectoryName -notmatch '_Archive|_OldDevSystemVersions' -and
    (Select-String -Path $_.FullName -Pattern '\[VERIFIED\]|VERIFIED, ' -Quiet)
}
```

Filter out protected locations from results.

## Step 3: Preview

Display grouped results in chat:

```
Cleanup Preview
===============

Agent Temp Files (N files):
  [full path 1]
  [full path 2]

Python Build Artifacts (N items):
  [full path 1]
  [full path 2]

Improve Workflow Artifacts (N files):
  [full path 1] (backup _v0)
  [full path 2] (deferred)

MCP Config Backups (N files):
  [full path 1]

INFO Verification Markers (N files to modify):
  [full path 1] (M occurrences)
  [full path 2] (M occurrences)

Total: N items to delete, N files to modify
```

If no items found: report "Workspace is clean - nothing to delete" and exit.

## Step 4: Confirm

Ask user for explicit confirmation. User may:
- **Confirm all** - delete everything shown
- **Exclude categories** - skip specific categories (e.g., "skip improve artifacts")
- **Cancel** - abort without deleting

## Step 5: Delete

Delete confirmed items:
- Files: `Remove-Item -Force`
- Directories (`__pycache__/`, `.pytest_cache/`, `.mypy_cache/`): `Remove-Item -Recurse -Force`
- INFO markers: strip `[VERIFIED]` and `VERIFIED, ` via text replacement

```powershell
# Strip verification markers from INFO documents
$content = Get-Content -Path $file -Raw -Encoding UTF8
$content = $content -replace ' \[VERIFIED\]', ''
$content = $content -replace 'VERIFIED, ', ''
Set-Content -Path $file -Value $content -Encoding UTF8 -NoNewline
```

## Step 6: Report

```
Cleanup Complete
================

Deleted:
  Agent Temp Files: N files
  Python Build Artifacts: N items
  Improve Workflow Artifacts: N files
  MCP Config Backups: N files
  INFO Markers Stripped: N files

Total: N items deleted, N files modified
Errors: [count and paths if any]
```

# FINALIZATION

## Quality Gate

- [ ] All target locations scanned before any deletion
- [ ] Protected locations excluded from results
- [ ] Preview shown in chat with full paths
- [ ] User confirmed before deletion
- [ ] Deletion results reported with counts

## Output

- Clean workspace with temporary files removed
- Deletion report in chat with per-category counts
