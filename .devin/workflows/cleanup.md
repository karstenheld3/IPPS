---
description: Delete temporary files and artifacts left by workflows and skills, or strip PromptSystem artifacts from documents for publishing
auto_execution_mode: 3
---

# Cleanup Workflow

Delete temporary files, build artifacts, and workflow leftovers from workspace and tools folders.

**Goal**: Clean workspace with all temporary and intermediate files removed

**Why**: Workflows and skills leave behind temp scripts, Python cache, versioned backups, and MCP config backups that accumulate over time

Scope: File deletion (normal modes) or in-place text transformation (file modes). Does NOT uninstall tools, remove sessions, or modify source code.

## MUST-NOT-FORGET

- **When in doubt, infer narrowest scope** - never block on scope questions
- Scan BEFORE deleting - always show preview of what will be removed
- NEVER delete `../.tools/` output folders (see Protected Locations)
- NEVER delete `/bugfix` `backup/` folders or `/go` backups/zips
- **All categories auto-delete after preview** - no confirmation needed
- User can run `/commit` before `/cleanup` if backups are needed
- Prompt system mode: always preview artifacts before transforming, never remove document content (only PromptSystem artifacts)
- `to [newfile]` mode: NEVER modify the original file. Copy first, clean the copy
- In-place mode on non-git-tracked files: create `_vN` backup before transforming (prevents unrecoverable data loss)
- **NEVER collapse code fences**: triple backtick (```) delimiters must be preserved. Regex that removes empty backtick pairs (`` `\` ``) must NOT run on lines containing ``` - it collapses fences to single backticks. Always verify fence count before and after transformation

## Trigger

- `/cleanup` - infer scope from conversation context (narrowest scope wins), then scan
- `/cleanup [path]` - scope to specified path directly (recursive scan limited to that path only)
- `/cleanup review` - delete ONLY `*_CRITIQUE.md` and `*_FACT-CHECK.md` files (Category 5 only), leave all other categories intact
- `/cleanup review [path]` - delete ONLY `*_CRITIQUE.md` and `*_FACT-CHECK.md` files within the specified path
- `/cleanup [file]` - general file mode: strip INFO verification markers from [file], delete its `_vN` backups
- `/cleanup [file] prompt system` - prompt system mode: strip ALL PromptSystem artifacts from [file] in-place, producing publishable clean markdown
- `/cleanup [file] make article` - alias for prompt system mode
- `/cleanup [file] as article` - alias for prompt system mode
- `/cleanup [file] for publishing` - alias for prompt system mode
- `/cleanup [file] to [newfile]` - general file mode, write cleaned output to [newfile], leave [file] untouched
- `/cleanup [file] to [newfile] prompt system` - prompt system mode, write cleaned output to [newfile], leave [file] untouched
- `/cleanup [file] to [newfile] make article` - alias for prompt system mode with output file
- `/cleanup [file] to [newfile] as article` - alias for prompt system mode with output file
- `/cleanup [file] to [newfile] for publishing` - alias for prompt system mode with output file

**Path-scoped mode** (`/cleanup [path]`): When an explicit path is provided, scan is STRICTLY limited to that path. No other workspace locations are scanned. All categories still apply but only within the given path.

**Category-scoped mode** (`/cleanup review`): When a category keyword is provided, ONLY that category is deleted. All other categories are skipped entirely.

**File mode** (`/cleanup [file]`): Text transformation on a single file. Two sub-modes:
- General (no keyword): strip INFO verification markers (`[VERIFIED]`, `VERIFIED, `), delete `_vN` backups
- Prompt system (`prompt system`, `make article`, `as article`, or `for publishing` keyword): strip all PromptSystem artifacts (headers, markers, references, annotations). See File Transformation section.

**Output target** (`to [newfile]`): When `to [newfile]` is specified, copy [file] to [newfile] first, then apply cleanup to [newfile]. Original [file] is NEVER modified. When `to [newfile]` is absent, apply cleanup in-place to [file].

**Git-tracking safety check**: Before in-place transformation (no `to [newfile]`), check if [file] is git-tracked. If NOT git-tracked (e.g., in gitignored folders like `_PrivateSessions/`), create a `_vN` backup copy first. This prevents unrecoverable data loss (see GLOB-FL-0003).

## GLOBAL-RULES

Apply to all cleanup runs regardless of scope.

1. Scan all target locations and collect file list BEFORE deleting anything
2. Group findings by category in preview
3. Show full paths in preview - never abbreviate or truncate
4. Auto-delete all categories after preview (see Auto-Delete Categories)
5. Report deletion results with counts per category

## Auto-Delete Categories

All categories auto-delete after preview. No confirmation needed. User can run `/commit` before `/cleanup` if backups are needed.

- Category 1: Agent temp files (`.tmp_*`, `*.tmp`) - single-run scripts, always disposable
- Category 2: Python build artifacts (`__pycache__/`, `*.pyc`) - regenerated automatically
- Category 3: Improve workflow backups (`_vN.*`) - safety copies after improvement accepted
- Category 4: MCP config backups - superseded config snapshots
- Category 5: Review output files (`*_CRITIQUE.md`, `*_FACT-CHECK.md`) - findings should be addressed before cleanup
- Category 6: Workflow scaffolding (`__*.md`, legacy `STRUT_*`) - consumed process artifacts
- INFO marker stripping (`[VERIFIED]` labels) - in-place text modification

**Execution flow:**
1. Scan all categories and show preview
2. Delete all categories immediately (no confirmation needed)
3. Report results

## Post-Workflow Cleanup Trigger

Workflows that create disposable artifacts SHOULD self-clean on successful completion. When a workflow completes successfully, it should delete its own artifacts from the working directory:

- `/improve` → delete `_vN.*` backups of the improved file
- `/drift-detect` → (keep `__DRIFT_*` until `/drift-correct` runs)
- `/drift-correct` → delete `__DRIFT_*` file after all gaps closed
- `/deep-research` → delete `__STRUT_*`, `__TASKS_*`, `__TEMPLATE_*` after research complete
- `/go` → delete `__TASKS_*` after goal reached

If the parent workflow forgets, `/cleanup` catches them. But the goal is: **artifacts should not survive beyond their parent workflow's completion**.

# CONTEXT-SPECIFIC

Detection: determine applicable contexts from scope. Multiple contexts may apply in a single run.

## File Cleanup

**Applies**: Normal modes only (not active in file mode)

Delete files and directories matching these patterns:

### 1. Agent Temp Files [AUTO-DELETE]

- **Pattern**: `.tmp_*` files, `*.tmp` files
- **Locations**: `[WORKSPACE_FOLDER]` recursive, `[SESSIONS_FOLDER]` recursive
- **Source**: Agent scripts, `/test`, `/implement`, `/go`, `/improve` STRUT plans, youtube-downloader metadata
- **Note**: `.tmp_*` files are dotfiles - invisible to `fd`/`find_by_name` by default. Always use PowerShell `Get-ChildItem -Force` or `fd --hidden` to scan for them.

### 2. Python Build Artifacts [AUTO-DELETE]

- **Pattern**: `__pycache__/` directories, `*.pyc` files, `.pytest_cache/`, `.mypy_cache/`
- **Locations**: `[WORKSPACE_FOLDER]` recursive, `[PROMPTSYSTEM_FOLDER]` recursive, `[AGENT_FOLDER]` recursive
- **Source**: Python script execution

### 3. Improve Workflow Artifacts [AUTO-DELETE]

- **Pattern**: `*_vN.*` versioned backups (filename ending in `_v` followed by digits before extension), `*_DEFERRED_IMPROVEMENTS.md`
- **Locations**: `[WORKSPACE_FOLDER]` recursive, excluding `_Archive/` and `_OldDevSystemVersions/`
- **Source**: `/improve` workflow versioned backups and deferred improvement logs

### 4. MCP Config Backups [AUTO-DELETE]

- **Pattern**: `mcp_config.json._beforeRemoving*`, `mcp_config.json._backup_*`
- **Location**: MCP config directory (resolve from agent-specific MCP config path - see @skills:coding-conventions AGENT-SKILL-RULES.md section 3.2.1)
- **Source**: MCP server install/uninstall scripts (ms-playwright-mcp, playwriter-mcp)

### 5. Review Output Files [AUTO-DELETE]

- **Pattern**: `*_CRITIQUE.md`, `*_FACT-CHECK.md`, legacy `*_REVIEW.md`
- **Locations**: `[WORKSPACE_FOLDER]` recursive, `[SESSION_FOLDER]` recursive, excluding `_Archive/` and `_OldDevSystemVersions/`
- **Source**: `/critique` and `/fact-check` workflows create these per review run. Intended to be discarded after findings are addressed.
- **Transition note**: `*_REVIEW.md` is the pre-rename convention. Match both old and new conventions.

### 6. Workflow Scaffolding [AUTO-DELETE]

- **Pattern**: `__*.md` files (double underscore prefix). Also legacy patterns: `STRUT_*.md` (not `STRUT_TEMPLATE.md`), `_TASKS_*.md` (files auto-created by `/go` before convention change)
- **Locations**: `[WORKSPACE_FOLDER]` recursive, `[SESSION_FOLDER]` recursive, excluding `_Archive/`, `_OldDevSystemVersions/`, and skill folders
- **Source**: `/deep-research` (STRUTs, TASKS, templates), `/go` (TASKS), `/bugfix` (STRUTs). These are process-tracking files auto-created by workflows. User-invoked outputs (`TASKS_[TOPIC].md` from `/write-tasks-plan`, `STRUT_[TOPIC].md` from `/write-strut`) are deliverables and MUST NOT be matched.
- **Transition note**: Legacy patterns (`STRUT_*.md` without `__`, `_TASKS_*.md`) exist in older sessions. Match both old and new conventions. Exclude `STRUT_TEMPLATE.md` and `TASKS_TEMPLATE.md` (skill resources).

## File Transformation

Two file transformation modes. Both clean a single file, no deletion of other files.

**Output target**: `to [newfile]` parameter controls where cleaned content is written:
- With `to [newfile]`: copy source to [newfile], clean the copy, original untouched
- Without `to [newfile]`: clean in-place. If file is NOT git-tracked, create `_vN` backup first

### General File Mode

**Applies**: `/cleanup [file]` without a publishing keyword

Strip INFO verification markers in-place:
- Pattern: `[VERIFIED]` labels, `VERIFIED, ` prefixes
- Source: `/research`, `/write-info`, `/verify` workflows add these during authoring. After content is finalized, markers are noise
- Also deletes `_vN` backups of the target file

### Prompt System Mode

**Applies**: `/cleanup [file]` with `prompt system`, `make article`, `as article`, or `for publishing` keyword

Strip all PromptSystem artifacts from a markdown file to produce publishable clean markdown.

### Remove

1. `<PromptSystem .../>` tags (entire line)
2. Document header block: `**Doc ID**:`, `**Goal**:`, `**Target file**:`, `**Depends on:**`, `**Does not depend on:**` and their value lines
3. `## MUST-NOT-FORGET` section: heading and all content until next `## ` heading
4. `## Document History` section: heading and all content until next `## ` heading or EOF
5. Workspace constants: `[WORKSPACE_FOLDER]`, `[SESSION_FOLDER]`, `[PROMPTSYSTEM_FOLDER]`, `[AGENT_FOLDER]`, `[SESSIONS_FOLDER]`, `[SKILL_TOOLS_FOLDER]`, `[DEV_KNOWLEDGE_FOLDER]`, `[DEV_SPECS_FOLDER]`, `[PRODUCT_VERSION]`, `[PRODUCT_REPO_FOLDER]`, `[PRODUCT_SOURCE_FOLDER]`, `[PRODUCT_DOCS_FOLDER]`, `[SESSION_ARCHIVE_FOLDER]`, `[API_KEYS_FILE]`, `[SOPS_FILE]`, `[RELEASE_NOTES_FOLDER]`
6. Annotation labels: `[VERIFIED]`, `[TESTED]`, `[LITERAL]`, `[ASSUMED]`, `[PROVEN]`, `[CRITICAL]`, `[HIGH]`, `[MEDIUM]`, `[LOW]`, `[RESOLVED]`, `[WONT-FIX]`, `[NEEDS-DISCUSSION]`, `[CONTRADICTS]`, `[OUTDATED]`, `[INCOMPLETE]`, `[UNVERIFIED]`
7. Skill references: `@skills:...`, `@rules:...`
8. Rule IDs: `AP-PR-*`, `AP-NM-*`, `AP-BR-*`, `AP-ST-*`, `CV-DT-*`, `CV-TR-*`, `CV-LN-*`, `SPEC-CT-*`, `IL-*`
9. PromptSystem concept references used as rule citations: `APAPALAN`, `MECT`, `SOCAS`, `MNF`, `MEPI`, `MCPI`, `VCRIV`, `FACRIV`, `GRUC`, `EDIRD`, `STRUT`, `TRACT`
10. Session tracking references: `NOTES.md`, `PROGRESS.md`, `PROBLEMS.md`, `FAILS.md`, `LEARNINGS.md` when referenced as workflow instructions
11. `[CONFIRMATION_KEYWORDS]` and other system placeholder references
12. Session metadata lines: `**Phase**:`, `**Operation Mode**:`, `**Workflow**:`, `**Assessment**:`, `**Started**:`, `**Topic Registry**` when they contain PromptSystem-internal state

### Keep

- Document title (`# Title`) and body content (prose, tables, lists, code blocks, images, links)
- Code fences (``` blocks) and their content - never strip, collapse, or modify triple backtick delimiters
- `## Table of Contents` (useful for published docs) - but remove entries pointing to deleted sections
- PromptSystem concept mentions when the document topic IS about them (e.g., a document explaining APAPALAN keeps all APAPALAN content)
- Rule IDs when the document analyzes or discusses specific rules (not when citing them as compliance references)

### Judgment Rule

For each PromptSystem artifact found:
- Rule citation or compliance reference (e.g., "per AP-PR-07", "follows APAPALAN") → Remove
- Document topic or content (e.g., a document titled "APAPALAN Rules" discussing the principle) → Keep
- When unclear, keep the content and note it in the report

## No Context Match

If scope contains no matching patterns and no INFO documents:
- Report "Workspace is clean - nothing to delete" and exit

If prompt system sub-mode and file has no PromptSystem artifacts:
- Report "File is already clean - no PromptSystem artifacts found" and exit

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
- `T##_*/` topic folders inside sessions - these are session subfolders, not temp artifacts

# EXECUTION

## Step 1: Determine Scope and Context

Read NOTES.md to resolve `[SESSIONS_FOLDER]` and `[PROMPTSYSTEM_FOLDER]`.

**Scope resolution** (MANDATORY - resolve scope before scanning):

Six cleanup scopes exist, from narrowest to widest:

1. **Markers** - strip labels within document content (e.g., `[VERIFIED]`, `[IMPROVED]` from INFO docs)
2. **Document** - artifacts of a single document (its `_vN` backups, related temp files)
3. **Workflow/Skill** - artifacts from a specific workflow or skill execution (e.g., all `/improve` backups from one run)
4. **Folder** - everything in a specific directory matching cleanup patterns (e.g., a working subfolder in a session)
5. **Session** - everything in `[SESSION_FOLDER]` matching cleanup patterns
6. **Workspace** - everything in `[WORKSPACE_FOLDER]` and all known locations

**Resolution rules (narrowest scope wins):**
- **Explicit path overrides everything**: If user provides a path argument, scope is STRICTLY that path. No other locations scanned. Do not broaden.
- **Category keyword**: If user says "review", scope to Category 5 only (`*_CRITIQUE.md` and `*_FACT-CHECK.md` files). All other categories skipped.
- **Narrowest scope principle**: Always infer the NARROWEST scope that covers the user's working context. Never broaden beyond what the conversation context requires.
- If all recent work is within a session subfolder (e.g., `Faro-Autokauf/`): scope = **Folder** (that subfolder), NOT Session
- If path arg provided: infer scope type from path type (file → Document, directory → Folder)
- If conversation just finished a `/critique` or `/improve` run: suggest workflow scope
- If conversation spans multiple session subfolders or session root: scope = **Session**
- If ambiguous: infer narrowest scope from conversation context. Default to **Folder** (current working directory) if no context available
- Do NOT ask questions about scope, files, or folders - infer and scan

**After scope is resolved, scan immediately:**
- **Markers** → all INFO docs in scope
- **Document** → infer from conversation or current file, scan its directory
- **Workflow/Skill** → infer from conversation context, scan for its artifacts
- **Folder** → use provided path or infer from conversation context
- **Session** → scan `[SESSION_FOLDER]`
- **Workspace** → scan `[WORKSPACE_FOLDER]` and all known locations

Detect applicable contexts:
- File Cleanup: always active (normal modes)
- File Transformation - General: active when `/cleanup [file]` without a publishing keyword
- File Transformation - Prompt System: active when `prompt system`, `make article`, `as article`, or `for publishing` keyword detected (skips normal scan/delete flow)

**File mode branch**: If `[file]` argument detected, skip Steps 2-5 and execute File Transformation Steps instead. Within file mode, publishing keywords (`prompt system`, `make article`, `as article`, `for publishing`) select prompt system sub-mode; otherwise general sub-mode applies.

## Step 2: Scan

Scan per active context. Collect full paths.

**File Cleanup scan:**

```powershell
# 1. Agent temp files (dotfiles: -Force required)
Get-ChildItem -Path "[SCOPE]" -Recurse -File -Force | Where-Object { $_.Name -like '.tmp_*' -or $_.Name -like '*.tmp' }

# 2. Python artifacts
Get-ChildItem -Path "[SCOPE]" -Recurse -Directory | Where-Object { $_.Name -in @('__pycache__', '.pytest_cache', '.mypy_cache') }
Get-ChildItem -Path "[SCOPE]" -Recurse -File -Filter "*.pyc"

# 3. Improve artifacts (_vN backups: filename_vN.ext where N is one or more digits)
Get-ChildItem -Path "[SCOPE]" -Recurse -File | Where-Object { $_.BaseName -match '_v\d+$' -and $_.DirectoryName -notmatch '_Archive|_OldDevSystemVersions' }
Get-ChildItem -Path "[SCOPE]" -Recurse -File -Filter "*_DEFERRED_IMPROVEMENTS.md" | Where-Object { $_.DirectoryName -notmatch '_Archive|_OldDevSystemVersions' }

# 4. MCP config backups (resolve MCP config directory first)
Get-ChildItem -Path "[MCP_CONFIG_DIR]" -File | Where-Object { $_.Name -match '^mcp_config\.json\._' }

# 5. Review output files (critique + fact-check, legacy _REVIEW)
Get-ChildItem -Path "[SCOPE]" -Recurse -File | Where-Object { ($_.Name -like '*_CRITIQUE.md' -or $_.Name -like '*_FACT-CHECK.md' -or $_.Name -like '*_REVIEW.md') -and $_.DirectoryName -notmatch '_Archive|_OldDevSystemVersions' }

# 6. Workflow scaffolding (__ prefix + legacy patterns)
Get-ChildItem -Path "[SCOPE]" -Recurse -File -Filter "__*.md" | Where-Object { $_.DirectoryName -notmatch '_Archive|_OldDevSystemVersions|skills' }
# Legacy: standalone STRUT files (not STRUT_TEMPLATE.md, not in skill folders)
Get-ChildItem -Path "[SCOPE]" -Recurse -File | Where-Object { $_.Name -match '^STRUT_' -and $_.Name -ne 'STRUT_TEMPLATE.md' -and $_.DirectoryName -notmatch '_Archive|_OldDevSystemVersions|skills' }
```

**INFO marker scan (normal modes only):**

```powershell
# 7. INFO verification markers (count files and occurrences)
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

Review Output Files (N files):
  [full path 1]
  [full path 2]

Workflow Scaffolding (N files):
  [full path 1] (__STRUT_*)
  [full path 2] (__TASKS_*)

INFO Verification Markers (N files to modify):
  [full path 1] (M occurrences)
  [full path 2] (M occurrences)

Total: N items to delete, N files to modify
```

If no items found: report "Workspace is clean - nothing to delete" and exit.

## Step 4: Execute

**Category-scoped mode**: If user said "review", only delete Category 5 items (`*_CRITIQUE.md` and `*_FACT-CHECK.md`). Skip all other categories.

Delete all found items immediately after preview (normal mode only):
- Files: `Remove-Item -Force -Confirm:$false`
- Directories (`__pycache__/`, `.pytest_cache/`, `.mypy_cache/`): `Remove-Item -Recurse -Force -Confirm:$false`
- INFO markers: strip `[VERIFIED]` and `VERIFIED, ` via text replacement

```powershell
# Strip verification markers from INFO documents
$content = Get-Content -Path $file -Raw -Encoding UTF8
$content = $content -replace ' \[VERIFIED\]', ''
$content = $content -replace 'VERIFIED, ', ''
Set-Content -Path $file -Value $content -Encoding UTF8 -NoNewline
```

## Step 5: Report

```
Cleanup Complete
================

Deleted:
  Agent Temp Files: N files
  Python Build Artifacts: N items
  Improve Workflow Artifacts: N files
  MCP Config Backups: N files
  Review Output Files: N files
  Workflow Scaffolding: N files
  INFO Markers Stripped: N files

Total: N items deleted, N files modified
Errors: [count and paths if any]
```

## File Transformation Steps

Execute when file mode is active (skips normal scan/delete flow). Sub-mode determined by publishing keyword (`prompt system`, `make article`, `as article`, `for publishing`).

**F0: Output target resolution**:
1. Check for `to [newfile]` syntax in the command
2. If `to [newfile]` present: copy [file] to [newfile], set target = [newfile], original = [file] (read-only)
3. If `to [newfile]` absent: set target = [file]. Check if git-tracked: `git ls-files --error-unmatch [file]`. If NOT tracked and not in a gitignored folder, create backup: `Copy-Item [file] [file]_v0.md`. If tracked, no backup needed (git history preserves original)

### F1: Read and Analyze

**General sub-mode**:
1. Read the target file (target = [newfile] if `to [newfile]`, else [file])
2. Count `[VERIFIED]` labels and `VERIFIED, ` prefixes
3. Check for `_vN` backup files in the same directory

**Prompt system sub-mode**:
1. Read the target file (target = [newfile] if `to [newfile]`, else [file])
2. Identify all PromptSystem artifacts per the Remove list in File Transformation > Prompt System Mode
3. For each artifact, apply the Judgment Rule: is it a citation/reference or document content?
4. Count artifacts by category

### F2: Preview

**General sub-mode**:
```
File Cleanup Preview
===================
Source: [file path]
Output: [newfile path] or [file path] (in-place)

Markers to strip:
  [VERIFIED] labels: N occurrences
  VERIFIED, prefixes: N occurrences

_vN backups to delete:
  [file_v0.md]
  [file_v1.md]

Total: N markers to strip, N backups to delete
```

**Prompt system sub-mode**:
```
Prompt System Cleanup Preview
=============================
Source: [file path]
Output: [newfile path] or [file path] (in-place)

Artifacts to remove:
  XML tags: N
  Document header: N lines
  MUST-NOT-FORGET section: N lines
  Document History section: N lines
  Workspace constants: N occurrences
  Annotation labels: N occurrences
  Skill/rule references: N occurrences
  Concept references: N occurrences
  Session tracking: N occurrences
  Other: N occurrences

Kept (topic-relevant):
  [list of artifacts kept with reason]

Total: N artifacts to remove
```

### F3: Execute

**General sub-mode**:
1. Strip `[VERIFIED]` and `VERIFIED, ` from the target file via text replacement
2. Delete `_vN` backup files (only when target = [file], not when `to [newfile]`)
3. Write modified content back to target file

**Prompt system sub-mode**:
Transform the target file:
1. Remove `<PromptSystem .../>` lines
2. Remove document header block lines (`**Doc ID**:`, `**Goal**:`, `**Target file**:`, `**Depends on:**`, `**Does not depend on:**` and their values)
3. Remove `## MUST-NOT-FORGET` section (heading through next `## `)
4. Remove `## Document History` section (heading through next `## ` or EOF)
5. Strip workspace constants (remove or replace with descriptive text if removal breaks sentence flow)
6. Strip annotation labels (`[VERIFIED]`, `[TESTED]`, etc.)
7. Remove `@skills:...` and `@rules:...` references
8. Remove rule IDs (`AP-PR-*`, `CV-DT-*`, etc.) when used as citations
9. Remove PromptSystem concept references when used as citations
10. Remove session tracking references when used as workflow instructions
11. Remove `[CONFIRMATION_KEYWORDS]` and system placeholders
12. Remove session metadata lines (`**Phase**:`, `**Operation Mode**:`, etc.)
13. Clean up: remove empty headings, double blank lines, orphaned list markers
14. Update `## Table of Contents` to remove entries pointing to deleted sections
15. **Code fence integrity check**: count ``` occurrences before and after transformation; counts must be equal. If mismatched, a regex collapsed a fence - revert and fix the regex
16. Write cleaned content back to the target file (not the original when `to [newfile]`)

### F4: Report

**General sub-mode**:
```
File Cleanup Complete
=====================
Source: [file path]
Output: [newfile path] or [file path] (in-place)

Stripped:
  [VERIFIED] labels: N
  VERIFIED, prefixes: N

Deleted:
  _vN backups: N files

Total: N markers stripped, N files deleted
```

**Prompt system sub-mode**:
```
Prompt System Cleanup Complete
==============================
Source: [file path]
Output: [newfile path] or [file path] (in-place)

Removed:
  XML tags: N
  Document header: N lines
  MUST-NOT-FORGET section: N lines
  Document History section: N lines
  Workspace constants: N occurrences
  Annotation labels: N occurrences
  Skill/rule references: N occurrences
  Concept references: N occurrences
  Session tracking: N occurrences
  Other: N occurrences

Kept (topic-relevant): N items
  [list with reasons]

Total: N artifacts removed
File size: [before] -> [after]
```

# FINALIZATION

## Quality Gate

- [ ] Scope inferred as narrowest that covers working context
- [ ] All target locations scanned before any deletion
- [ ] Protected locations excluded from results
- [ ] Preview shown in chat with full paths
- [ ] If explicit path provided: scan STRICTLY limited to that path, no other locations scanned
- [ ] If category keyword provided: only that category deleted, all others skipped
- [ ] If file mode: appropriate sub-mode selected (general or prompt system), file transformed in-place
- [ ] Code fence integrity: ``` count before == after (no collapsed fences)
- [ ] All categories deleted without asking (user runs `/commit` before if backups needed)
- [ ] Deletion results reported with counts

## Output

- Clean workspace with temporary files removed (normal modes)
- Deletion report in chat with per-category counts (normal modes)
- File with INFO markers stripped and `_vN` backups deleted (general file mode)
- Publishable clean markdown file with PromptSystem artifacts stripped (prompt system mode)
- Transformation report with artifact counts and kept items (file modes)
