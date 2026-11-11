---
description: Delete temporary files and artifacts left by workflows and skills, strip PromptSystem artifacts from documents for publishing, or slim tracking files for fast session load and prime
auto_execution_mode: 3
---

# Cleanup Workflow

Delete temporary files, build artifacts, and workflow leftovers from workspace and tools folders.

**Goal**: Clean workspace with all temporary and intermediate files removed

**Why**: Workflows and skills leave behind temp scripts, Python cache, versioned backups, and MCP config backups that accumulate over time

Scope: File deletion (normal modes), in-place text transformation (file modes), or archive-and-slim of tracking files (prime modes). Does NOT uninstall tools, remove sessions, or modify source code.

## MUST-NOT-FORGET

- **When in doubt, infer narrowest scope** - never block on scope questions
- Scan BEFORE deleting - always show preview of what will be removed
- NEVER delete `../.tools/` output folders (see Protected Locations)
- NEVER delete `/go` backups/zips. Utility folders are deleted by affix only: `_agentwork/` and `.tmp_*` (see `agent-behavior.md` section Agent-Created Folders). Never descend into `_archive*` folders
- **All categories auto-delete after preview** - no confirmation needed
- User can run `/commit` before `/cleanup` if backups are needed
- Prompt system mode: always preview artifacts before transforming, never remove document content (only PromptSystem artifacts)
- `to [newfile]` mode: NEVER modify the original file. Copy first, clean the copy
- In-place mode on non-git-tracked files: create `_vN` backup before transforming (prevents unrecoverable data loss)
- **NEVER collapse code fences**: triple backtick (```) delimiters must be preserved. Regex that removes empty backtick pairs (`` `\` ``) must NOT run on lines containing ``` - it collapses fences to single backticks. Always verify fence count before and after transformation
- Prime modes: snapshot copy BEFORE any edit, verified by hash. Archive entries, never destroy them. Never alter workspace constants, `[LITERAL]` values, config blocks, open items, or confirmed user decisions (see Prime Mode)

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
- `/cleanup workspace prime` - snapshot workspace tracking files to `[SESSION_ARCHIVE_FOLDER]/!workspace/[YYYY-MM-DD_HH-MM]/`, then slim `NOTES.md`, `PROBLEMS.md`, `FAILS.md`, `ID-REGISTRY.md`, `PROGRESS.md`
- `/cleanup session prime` - same for the active session; snapshot and archived entries go to `[SESSION_FOLDER]/_archive/[YYYY-MM-DD_HH-MM]/`
- `/cleanup prime` - context-dependent: session when the work context is inside a session folder, else workspace (see Prime Scope Resolution)

**Path-scoped mode** (`/cleanup [path]`): When an explicit path is provided, scan is STRICTLY limited to that path. No other workspace locations are scanned. All categories still apply but only within the given path.

**Category-scoped mode** (`/cleanup review`): When a category keyword is provided, ONLY that category is deleted. All other categories are skipped entirely.

**File mode** (`/cleanup [file]`): Text transformation on a single file. Two sub-modes:
- General (no keyword): strip INFO verification markers (`[VERIFIED]`, `VERIFIED, `), delete `_vN` backups
- Prompt system (`prompt system`, `make article`, `as article`, or `for publishing` keyword): strip all PromptSystem artifacts (headers, markers, references, annotations). See File Transformation section.

**Prime mode** (`/cleanup [workspace|session] prime`): Archive-and-slim of tracking files so `/prime` and `/session-load` read less. No temp-file deletion, no scan of cleanup categories. See Prime Mode section.

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

- Category 1: Agent temp files and folders (`.tmp_*`, `*.tmp`) - single-run scripts and rebuildable folders (`.tmp_jpgs/`, `.tmp_extracted/`), always disposable
- Category 2: Python build artifacts (`__pycache__/`, `*.pyc`) - regenerated automatically
- Category 3: Improve workflow backups (`_vN.*`) - safety copies after improvement accepted
- Category 4: MCP config backups - superseded config snapshots
- Category 5: Review output files (`*_CRITIQUE.md`, `*_FACT-CHECK.md`) - findings should be addressed before cleanup
- Category 6: Workflow scaffolding (`__*.md`, legacy `STRUT_*`) - consumed process artifacts
- Category 7: Agent work folders (`_agentwork/`) - all operational artifacts (cards, prompts, STRUTs, scripts, temp output) per `agent-behavior.md` File Placement
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

- **Pattern**: `.tmp_*` files, `.tmp_*` folders (deleted recursively), `*.tmp` files
- **Locations**: `[WORKSPACE_FOLDER]` recursive, `[SESSIONS_FOLDER]` recursive, excluding `_archive*` folders (script files are expected inside `_agentwork/`; matches outside it are misplaced leftovers)
- **Source**: Agent scripts and their `_out.txt` / `_err.txt` files, `/test`, `/implement`, `/go`, rebuildable folders `.tmp_jpgs/` and `.tmp_extracted/` (consuming steps re-create them when missing)
- **Note**: `.tmp_*` files and folders are dotfiles - invisible to `fd`/`find_by_name` by default. Always use PowerShell `Get-ChildItem -Force` or `fd --hidden` to scan for them.

### 2. Python Build Artifacts [AUTO-DELETE]

- **Pattern**: `__pycache__/` directories, `*.pyc` files, `.pytest_cache/`, `.mypy_cache/`
- **Locations**: `[WORKSPACE_FOLDER]` recursive, `[PROMPTSYSTEM_FOLDER]` recursive, `[AGENT_FOLDER]` recursive, `[LINKED_REPOS]` recursive (workspace scope only)
- **Source**: Python script execution
- **Linked repos**: read `[LINKED_REPOS]` list from `NOTES.md`. Each entry is a relative path from `[WORKSPACE_FOLDER]`. Scan each repo's `[AGENT_FOLDER]` and source folders. Skip `_archive*`, `.git`, `node_modules`, `venv`, `.venv`

### 3. Improve Workflow Artifacts [AUTO-DELETE]

- **Pattern**: `*_vN.*` versioned backups (filename ending in `_v` followed by digits before extension), `*_DEFERRED_IMPROVEMENTS.md`
- **Locations**: `[WORKSPACE_FOLDER]` recursive, excluding `_archive*` folders and `_OldDevSystemVersions/`
- **Source**: `/improve` workflow versioned backups and deferred improvement logs

### 4. MCP Config Backups [AUTO-DELETE]

- **Pattern**: `mcp_config.json._beforeRemoving*`, `mcp_config.json._backup_*`
- **Location**: MCP config directory (resolve from agent-specific MCP config path - see @skills:coding-conventions AGENT-SKILL-RULES.md section 3.2.1)
- **Source**: MCP server install/uninstall scripts (ms-playwright-mcp)

### 5. Review Output Files [AUTO-DELETE]

- **Pattern**: `*_CRITIQUE.md`, `*_FACT-CHECK.md`, legacy `*_REVIEW.md`
- **Locations**: `[WORKSPACE_FOLDER]` recursive, `[SESSION_FOLDER]` recursive, excluding `_archive*` folders and `_OldDevSystemVersions/`
- **Source**: `/critique` and `/fact-check` workflows create these per review run. Intended to be discarded after findings are addressed.
- **Transition note**: `*_REVIEW.md` is the pre-rename convention. Match both old and new conventions.

### 6. Workflow Scaffolding [AUTO-DELETE]

- **Pattern**: `__*.md` files (double underscore prefix). Also legacy patterns: `STRUT_*.md` (not `STRUT_TEMPLATE.md`), `_TASKS_*.md` (files auto-created by `/go` before convention change)
- **Locations**: `[WORKSPACE_FOLDER]` recursive, `[SESSION_FOLDER]` recursive, excluding `_archive*` folders, `_OldDevSystemVersions/`, and skill folders
- **Source**: `/deep-research` (STRUTs, TASKS, templates), `/go` (TASKS), `/bugfix` (STRUTs). These are process-tracking files auto-created by workflows. User-invoked outputs (`TASKS_[TOPIC].md` from `/write-tasks-plan`, `STRUT_[TOPIC].md` from `/write-strut`) are deliverables and MUST NOT be matched.
- **Transition note**: Legacy patterns (`STRUT_*.md` without `__`, `_TASKS_*.md`) exist in older sessions. Match both old and new conventions. Exclude `STRUT_TEMPLATE.md` and `TASKS_TEMPLATE.md` (skill resources).

### 7. Agent Work Folders [AUTO-DELETE]

- **Pattern**: `_agentwork/` directories, deleted recursively
- **Locations**: `[WORKSPACE_FOLDER]` recursive, `[SESSION_FOLDER]` recursive, excluding `_archive*` folders and `_OldDevSystemVersions/`
- **Source**: All workflows and agent work per `agent-behavior.md` `_agentwork/` Folder (cards, `_PROMPTS_*`, `__STRUT_*`, `__TASKS_*`, `__DRIFT_*`, `.tmp_*` scripts and output files)

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
6. Annotation labels: `[VERIFIED]`, `[TESTED]`, `[LITERAL]`, `[ASSUMED]`, `[PROVEN]`, `[CRITICAL]`, `[HIGH]`, `[MEDIUM]`, `[LOW]`, `[RESOLVED]`, `[WONT-FIX]`, `[NEEDS-DISCUSSION]`, `[CONTRADICTS]`, `[OUTDATED]`, `[INCOMPLETE]`, `[UNVERIFIED]` - including any content inside the brackets when the label is a prefix (e.g., `[UNVERIFIED - Einzelfallprüfung]` → remove entire bracket construct)
7. Skill references: `@skills:...`, `@rules:...`
8. Rule IDs: `APAPL-PR-*`, `APAPL-NM-*`, `APAPL-BR-*`, `APAPL-ST-*`, `CV-DT-*`, `CV-TR-*`, `CV-LN-*`, `SPEC-CT-*`, `IL-*`
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
- Rule citation or compliance reference (e.g., "per APAPL-PR-07", "follows APAPALAN") → Remove
- Document topic or content (e.g., a document titled "APAPALAN Rules" discussing the principle) → Keep
- When unclear, keep the content and note it in the report

## Prime Mode

**Applies**: `/cleanup workspace prime`, `/cleanup session prime`, `/cleanup prime`

**Goal**: Tracking files hold only what the next session needs. Everything else is archived, not deleted.

### Prime Scope Resolution

No questions. Resolve in this order, first match wins:

1. Keyword `workspace` or `session` given: use it
2. Active document or last edited file is inside `[SESSIONS_FOLDER]/_*` (or its `T##_*` subfolder): session = that folder (parent session for `T##_*`)
3. `/session-load` or `/session-new` ran in this conversation: session = that folder
4. Otherwise: workspace

State the resolved scope in one line before starting.

### Targets

- **Workspace** (files at `[WORKSPACE_FOLDER]` root, with or without `!` prefix): `NOTES.md`, `PROBLEMS.md`, `FAILS.md`, `ID-REGISTRY.md`, `PROGRESS.md`. Snapshot also copies `LEARNINGS.md` (not slimmed)
- **Session** (files at `[SESSION_FOLDER]` root): `NOTES.md`, `PROBLEMS.md`, `PROGRESS.md`, `FAILS.md`
- Missing files are skipped. Files already below 60 lines are snapshotted but not slimmed
- Archive folder: workspace = `[SESSION_ARCHIVE_FOLDER]/!workspace/` (default `[WORKSPACE_FOLDER]/_archive_gitignore/!workspace/`, create if missing); session = `[SESSION_FOLDER]/_archive/`. Writing into `_archive*` is allowed; the rule "never descend into `_archive*`" covers scanning only

### Entry Classification

Split each file into entries (heading block, list item with its sub-lines, or paragraph). Classify each:

- **KEEP**: open or deferred problems, unresolved fails, current phase, to-do and in-progress items, valid MUST-NOT-FORGET items, confirmed user decisions, rules still enforced and not stated elsewhere, workspace constants, `[LITERAL]` values, config blocks (`[RELEASE_CONFIG]`, `[LINKED_REPOS]`, and similar parsed by workflows), headings other workflows read (`Current Phase`, `Significant Prompts Log`, `Topic Registry`)
- **ARCHIVE**: resolved, wont-fix and completed items, done progress items, change logs, dated result reports and test run records of finished work, session status blocks whose work is committed, tombstones ("renamed to X"), verbatim prompts that no open item depends on
- **COMPACT**: kept entries rewritten shorter (see Compaction)

When unsure whether an entry is still needed, KEEP it and list it under "Unsure" in the report.

### Per-File Rules

- **NOTES.md**: archive finished-work blocks and dated result sections. Keep structure: MUST-NOT-FORGET, TOC, project info, constants, active rules, reference
- **PROBLEMS.md**: keep `Open` and `Deferred`. Archive `Resolved` entries and `Problems Changes` log. Keep the section headings
- **FAILS.md**: unresolved entries stay in full. Resolved entries: archive the full entry, keep one line in a `Prevention Rules` list at the top: `[ID] rule`. Rules stating the same prevention merge into one line listing all IDs. This keeps lessons loaded and entries retrievable by ID (archiving is not deletion; satisfies the never-delete-unconfirmed rule)
- **ID-REGISTRY.md**: keep framework, identifier, label and state definitions that are not duplicated in `[AGENT_FOLDER]/rules/` (verify by grep before removing a duplicate; replace with a one-line pointer). Topics: keep ID, description cut to one line, date, for topics referenced by an open item, a non-archived session or a workspace document. All other topic IDs collapse into one `Retired topics (do not reuse)` line listing IDs only. Never drop an ID entirely: uniqueness check needs it. Tombstones join the retired line
- **PROGRESS.md**: archive done items, keep to-do and in-progress

### Compaction

- One instruction, one statement. Merge duplicates inside the file; across files keep the most authoritative location and point to it
- Remove content already stated in `[AGENT_FOLDER]/rules/` or skills (grep distinctive phrases first); do not leave a pointer unless the reader needs to know where it moved
- Shorten prose per APAPALAN: drop filler, keep every condition, name, path, number and command exactly
- Reorganize for discoverability: MUST-NOT-FORGET, TOC, project info, constants, active rules grouped by topic (most frequently needed first), reference last. Max 7 ungrouped items per list. Informative headings that state content, not topic
- Do not rewrite quoted text, verbatim prompts or code fences
- Add one pointer line per slimmed file below its title: `Older entries: [archive folder path]` (parent folder, never a dated subfolder, so it never goes stale)

### Prime Steps

**P1: Resolve**: scope, target files, archive folder, timestamp `[YYYY-MM-DD_HH-MM]` (local time). Read NOTES.md for `[SESSIONS_FOLDER]`, `[SESSION_ARCHIVE_FOLDER]`.

**P2: Snapshot**: create `[archive folder]/[YYYY-MM-DD_HH-MM]/` and copy every existing target file (and `LEARNINGS.md` for workspace) with its original name. Compare SHA256 of each copy to its source. Any mismatch: stop, report, change nothing. Run file operations through the supervised script pattern of Step 2 when more than a few files are involved.

**P3: Classify**: read each target, split into entries, classify per Entry Classification. Record before/after counts of: lines, characters, IDs (all `[TOPIC]-[TYPE]-[NNNN]` and `[TOPIC]-[TYPE]-[NN]` patterns), workspace constants (`[NAME]:` definitions), code fences.

**P4: Preview** in chat, per file:

```
Prime Preview (workspace|session)
=================================
Snapshot: [archive folder]/[YYYY-MM-DD_HH-MM]/

[file] ([before] -> [after] lines)
  Archive: [N entries] [IDs or headings]
  Compact: [N edits] [one-line summary each]
  Reorganize: [yes/no, new section order]
  Unsure (kept): [entries]
```

No confirmation gate (all cleanup categories auto-execute). The snapshot is the safety copy.

**P5: Execute**: write the slimmed files UTF-8 without BOM. Write archived entries to `[archive folder]/[YYYY-MM-DD_HH-MM]/ARCHIVED_ENTRIES.md` under one heading per source file. The snapshot already holds the originals; this file lets a reader find removed entries without diffing.

**P6: Verify** (any failure: restore the file from snapshot, report):

- Every ID from the snapshot appears in the slimmed file, or in `ARCHIVED_ENTRIES.md`, or on the retired-topics line
- Workspace constant definitions identical before and after (names and values)
- Code fence count equal per file
- TOC entries match headings of each slimmed file
- Every open problem and unresolved fail still present
- No dangling references: grep remaining targets for each archived ID, repoint or drop the reference

**P7: Report**

```
Prime Complete (workspace|session)
==================================
Snapshot: [path]
[file]: [before] -> [after] lines, [before] -> [after] chars (~[N] tokens saved)
Archived: [N entries]  Compacted: [N]  Kept unsure: [N]
Verification: [pass|fail per P6 check]
```

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
6. **Workspace** - everything in `[WORKSPACE_FOLDER]`, `[PROMPTSYSTEM_FOLDER]`, `[AGENT_FOLDER]`, and `[LINKED_REPOS]` (read from NOTES.md)

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
- **Workspace** → scan `[WORKSPACE_FOLDER]`, `[PROMPTSYSTEM_FOLDER]`, `[AGENT_FOLDER]`, and `[LINKED_REPOS]` (read from NOTES.md)

Detect applicable contexts:
- File Cleanup: always active (normal modes)
- File Transformation - General: active when `/cleanup [file]` without a publishing keyword
- File Transformation - Prompt System: active when `prompt system`, `make article`, `as article`, or `for publishing` keyword detected (skips normal scan/delete flow)

**Prime mode branch**: If keyword `prime` detected, skip Steps 2-5 and execute Prime Steps instead.

**File mode branch**: If `[file]` argument detected, skip Steps 2-5 and execute File Transformation Steps instead. Within file mode, publishing keywords (`prompt system`, `make article`, `as article`, `for publishing`) select prompt system sub-mode; otherwise general sub-mode applies.

## Step 2: Scan

Scan per active context. Collect full paths.

**File Cleanup scan:** run the commands below through the supervised runner (`agent-behavior.md` Terminal Hang Prevention): write them into `[WORKSPACE_FOLDER]/_agentwork/.tmp_cleanup_scan_[HHmmss].ps1`, emit full paths with `Write-Output`, run it with `-Expected 20 -Topic cleanup`, then `read_file` the `_log.txt` and `_out.txt` files. Never run these pipelines inline. Exclude the scan script and its output files from the preview; delete them last.

```powershell
# 1. Agent temp files and .tmp_* folders (dotfiles: -Force required; skip archive folders and items inside a .tmp_ folder)
Get-ChildItem -Path "[SCOPE]" -Recurse -Force | Where-Object { ($_.Name -like '.tmp_*' -or $_.Name -like '*.tmp') -and $_.FullName -notmatch '_archive' -and $_.FullName -notmatch '[\\/]\.tmp_[^\\/]*[\\/]' }

# 2. Python artifacts
Get-ChildItem -Path "[SCOPE]" -Recurse -Directory | Where-Object { $_.Name -in @('__pycache__', '.pytest_cache', '.mypy_cache') }
Get-ChildItem -Path "[SCOPE]" -Recurse -File -Filter "*.pyc"
# 2b. Python artifacts in linked repos (workspace scope only; read [LINKED_REPOS] from NOTES.md)
# foreach ($repo in $linkedRepos) { Get-ChildItem -Path $repo -Recurse -Directory | Where-Object { $_.Name -in @('__pycache__', '.pytest_cache', '.mypy_cache') -and $_.FullName -notmatch '\\.git|node_modules|venv|\.venv' } }

# 3. Improve artifacts (_vN backups: filename_vN.ext where N is one or more digits)
Get-ChildItem -Path "[SCOPE]" -Recurse -File | Where-Object { $_.BaseName -match '_v\d+$' -and $_.DirectoryName -notmatch '_archive|_OldDevSystemVersions' }
Get-ChildItem -Path "[SCOPE]" -Recurse -File -Filter "*_DEFERRED_IMPROVEMENTS.md" | Where-Object { $_.DirectoryName -notmatch '_archive|_OldDevSystemVersions' }

# 4. MCP config backups (resolve MCP config directory first)
Get-ChildItem -Path "[MCP_CONFIG_DIR]" -File | Where-Object { $_.Name -match '^mcp_config\.json\._' }

# 5. Review output files (critique + fact-check, legacy _REVIEW)
Get-ChildItem -Path "[SCOPE]" -Recurse -File | Where-Object { ($_.Name -like '*_CRITIQUE.md' -or $_.Name -like '*_FACT-CHECK.md' -or $_.Name -like '*_REVIEW.md') -and $_.DirectoryName -notmatch '_archive|_OldDevSystemVersions' }

# 6. Workflow scaffolding (__ prefix + legacy patterns)
Get-ChildItem -Path "[SCOPE]" -Recurse -File -Filter "__*.md" | Where-Object { $_.DirectoryName -notmatch '_archive|_OldDevSystemVersions|skills' }
# Legacy: standalone STRUT files (not STRUT_TEMPLATE.md, not in skill folders)
Get-ChildItem -Path "[SCOPE]" -Recurse -File | Where-Object { $_.Name -match '^STRUT_' -and $_.Name -ne 'STRUT_TEMPLATE.md' -and $_.DirectoryName -notmatch '_archive|_OldDevSystemVersions|skills' }

# 7. Agent work folders
Get-ChildItem -Path "[SCOPE]" -Recurse -Directory -Force -Filter "_agentwork" | Where-Object { $_.FullName -notmatch '_archive|_OldDevSystemVersions' }
```

**INFO marker scan (normal modes only):**

```powershell
# 8. INFO verification markers (count files and occurrences)
Get-ChildItem -Path "[SCOPE]" -Recurse -File -Filter "_INFO_*.md" | Where-Object {
    $_.DirectoryName -notmatch '_archive|_OldDevSystemVersions' -and
    (Select-String -Path $_.FullName -Pattern '\[VERIFIED\]|VERIFIED, ' -Quiet)
}
```

Filter out protected locations from results.

**Fails card carry-out** (before Agent Work Folders are deleted): for every `_agentwork/__CARD_*-Fails.md` found, select the "Never again" lines that recur or apply beyond the project and generalize them (no paths, names, values). Target: in IPPS the agent `ROBUSTNESS_CARD_TEMPLATE.md` banned list (@skills:terminal-robustness); in any other workspace the workspace `FAILS.md`. Rules: Fails card rules in `ROBUSTNESS_CARD_SKELETON.md`. Lines that apply only to the project are deleted with the folder.

## Step 3: Preview

Display grouped results in chat:

```
Cleanup Preview
===============

Agent Temp Files and Folders (N items):
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

Agent Work Folders (N folders):
  [full path 1]
  [full path 2]

Fails Card Carry-Out (N lines, written before deletion):
  [generalized line] -> [target file]

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
- Directories (`__pycache__/`, `.pytest_cache/`, `.mypy_cache/`, `.tmp_*/`, `_agentwork/`): `Remove-Item -Recurse -Force -Confirm:$false`
- Run deletions through the same temp-script pattern as the scan when more than a few items are affected
- INFO markers: strip `[VERIFIED]` and `VERIFIED, ` via text replacement

```powershell
# Strip verification markers from INFO documents (UTF-8 without BOM; Set-Content -Encoding UTF8 adds a BOM in PowerShell 5.1)
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
$fullPath = (Resolve-Path -LiteralPath $file).ProviderPath
$content = [System.IO.File]::ReadAllText($fullPath, $utf8NoBom)
$content = $content -replace ' \[VERIFIED\]', ''
$content = $content -replace 'VERIFIED, ', ''
[System.IO.File]::WriteAllText($fullPath, $content, $utf8NoBom)
```

## Step 5: Report

```
Cleanup Complete
================

Deleted:
  Agent Temp Files and Folders: N items
  Python Build Artifacts: N items
  Improve Workflow Artifacts: N files
  MCP Config Backups: N files
  Review Output Files: N files
  Workflow Scaffolding: N files
  Agent Work Folders: N folders
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
8. Remove rule IDs (`APAPL-PR-*`, `CV-DT-*`, etc.) when used as citations
9. Remove PromptSystem concept references when used as citations
10. Remove session tracking references when used as workflow instructions
11. Remove `[CONFIRMATION_KEYWORDS]` and system placeholders
12. Remove session metadata lines (`**Phase**:`, `**Operation Mode**:`, etc.)
13. Clean up: remove empty headings, double blank lines, orphaned list markers, empty parenthetical constructs (`()` or `[]` left after annotation stripping), dangling separators (` -` at end of line, `, ;` sequences)
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
- [ ] Scans ran as `_agentwork/.tmp_` script, not inline pipelines
- [ ] `_archive*` folders skipped; `.tmp_*` folders and `_agentwork/` folders listed and deleted by affix only
- [ ] Protected locations excluded from results
- [ ] Preview shown in chat with full paths
- [ ] If explicit path provided: scan STRICTLY limited to that path, no other locations scanned
- [ ] If category keyword provided: only that category deleted, all others skipped
- [ ] If file mode: appropriate sub-mode selected (general or prompt system), file transformed in-place
- [ ] If prime mode: scope resolved without questions, snapshot hash-verified before any edit, P6 checks all pass, pointer line added to each slimmed file
- [ ] Code fence integrity: ``` count before == after (no collapsed fences)
- [ ] All categories deleted without asking (user runs `/commit` before if backups needed)
- [ ] Deletion results reported with counts

## Output

- Clean workspace with temporary files removed (normal modes)
- Deletion report in chat with per-category counts (normal modes)
- File with INFO markers stripped and `_vN` backups deleted (general file mode)
- Publishable clean markdown file with PromptSystem artifacts stripped (prompt system mode)
- Transformation report with artifact counts and kept items (file modes)
- Snapshot folder, `ARCHIVED_ENTRIES.md`, slimmed tracking files and size report (prime modes)
