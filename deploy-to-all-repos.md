---
description: Deploy DevSystem files to all linked repositories
---

# Deploy to All Repos

Copies DevSystem files from this repo's `.windsurf` folder to all linked repositories according to their specific rules.

## MUST-NOT-FORGET

1. **Check DevSystem version FIRST** - Read `!NOTES.md` to get `[DEVSYSTEM]` (e.g., `DevSystemV3.1`) before ANY other action
2. **Sync before deploy** - Copy from `[DEVSYSTEM]\*` to `.windsurf\` BEFORE running preview
3. **Clean deprecated files** - Remove deprecated files from `.windsurf/` after sync (edird-core.md, go-autonomous.md, next.md, edird-phase-model/)
4. **Output format** - ALWAYS use the exact text format in "Output Format" section (NO tables, NO markdown tables)
5. **List filenames** - ALWAYS list explicit filenames after each category (Add, Overwrite, Delete), not just counts

**WHY:** `.windsurf/` may contain stale files from older DevSystem versions. Deploying without syncing first will propagate deprecated files to all linked repos.

## Execution Modes

**Default (Preview/Dry-Run):** Show what WOULD be done, then ask for confirmation before making any changes.

**Auto-Execute:** ONLY if user message contains an EXPLICIT confirmation keyword:
- `yes`, `confirm`, `ok`, `do it`, `execute`, `proceed`

Example: `deploy-to-all-repos confirm` - executes without preview prompt

**CRITICAL - NOT Confirmation Keywords:**
These phrases invoke the workflow but are NOT confirmation:
- "deploy to all repos"
- "deploy-to-all-repos"
- "deploy-all"
- "deploy all"
- "deploy to all"

ALWAYS show preview and ask for explicit confirmation first.

## Prerequisites

Read `[LINKED_REPOS]` section from `*NOTES.md` to get:
- List of target repositories
- Copy/overwrite rules for each repo
- Files to preserve (if any)

## Workflow Steps

### 0. Check Execution Mode

- If user message contains confirmation keyword: set `AUTO_EXECUTE = true`
- Otherwise: set `AUTO_EXECUTE = false` (preview mode)

### 1. Read Configuration

Read `*NOTES.md` and extract `[LINKED_REPOS]` section.

### 2. For Each Linked Repository

Execute the following for each repo in `[LINKED_REPOS]`:

#### 2.1 Verify Target Exists

Check that the target repo path exists. Skip if not found (warn user).

#### 2.2 Compare Source and Target Files (Parallel)

Use this PowerShell snippet to analyze all target repos **in parallel**:

```powershell
# Compare DevSystem files between source and multiple target repos (PARALLEL)
$source = "[WORKSPACE_FOLDER]\.windsurf"  # This repo's .windsurf folder
$targets = @(
    # Populate from [LINKED_REPOS] in !NOTES.md
)

# NOTE: Run comparisons in parallel for faster analysis
# $targets | ForEach-Object -Parallel { ... } -ThrottleLimit 4

# Deprecated files from V1, V2, V3 migrations (only these can be deleted)
$deprecatedFiles = @{
    "rules" = @("commit-rules.md", "devsystem-rules.md", "document-rules.md", "git-rules.md", "proper-english-rules.md", "python-rules.md", "tools-rules.md", "edird-core.md")
    "workflows" = @("review-devilsadvocate.md", "review-pragmaticprogrammer.md", "session-init.md", "go-autonomous.md", "next.md", "new-feature.md", "new-task.md", "setup-pdftools.md", "deliver.md", "design.md", "explore.md", "go-research.md", "refine.md", "session-resume.md")
}
# Deprecated skill folders (entire folder can be deleted if renamed)
$deprecatedSkillFolders = @("edird-phase-model")

# Get all source files (relative paths)
$sourceFiles = Get-ChildItem -Path $source -Recurse -File | ForEach-Object {
    $_.FullName.Substring($source.Length + 1)
} | Where-Object { $_ }

foreach ($target in $targets) {
    $repoName = (Split-Path (Split-Path $target -Parent) -Leaf)
    Write-Host "`n=== $repoName ===" -ForegroundColor Cyan
    
    if (-not (Test-Path $target)) {
        Write-Host "  [NEW REPO] .windsurf folder does not exist - will create with $($sourceFiles.Count) files" -ForegroundColor Green
        continue
    }
    
    $new = @(); $modified = @(); $unchanged = @()
    foreach ($rel in $sourceFiles) {
        $srcFile = Join-Path $source $rel
        $tgtFile = Join-Path $target $rel
        if (-not (Test-Path $tgtFile)) { $new += $rel }
        else {
            $srcHash = (Get-FileHash $srcFile -Algorithm MD5).Hash
            $tgtHash = (Get-FileHash $tgtFile -Algorithm MD5).Hash
            if ($srcHash -ne $tgtHash) { $modified += $rel } else { $unchanged += $rel }
        }
    }
    
    # Find deprecated files in rules and workflows
    $deprecated = @()
    foreach ($folder in $deprecatedFiles.Keys) {
        $deprecated += Get-ChildItem -Path "$target\$folder" -File -ErrorAction SilentlyContinue | 
            Where-Object { $deprecatedFiles[$folder] -contains $_.Name } | 
            ForEach-Object { "$folder\$($_.Name)" }
    }
    
    # Output summary
    if ($new.Count -eq 0 -and $modified.Count -eq 0 -and $deprecated.Count -eq 0) {
        Write-Host "  [UP TO DATE] $($unchanged.Count) files unchanged" -ForegroundColor Gray
    } else {
        if ($new.Count -gt 0) { Write-Host "  NEW: $($new.Count)" -ForegroundColor Green; $new | ForEach-Object { Write-Host "    $_" -ForegroundColor Green } }
        if ($modified.Count -gt 0) { Write-Host "  MODIFIED: $($modified.Count)" -ForegroundColor Yellow; $modified | ForEach-Object { Write-Host "    $_" -ForegroundColor Yellow } }
        if ($deprecated.Count -gt 0) { Write-Host "  DELETE: $($deprecated.Count)" -ForegroundColor Red; $deprecated | ForEach-Object { Write-Host "    $_" -ForegroundColor Red } }
        if ($unchanged.Count -gt 0) { Write-Host "  UNCHANGED: $($unchanged.Count)" -ForegroundColor Gray }
    }
    
}
```

#### 2.3 Apply Copy Rules

For each source file, apply the repo-specific rules:

**Standard Rules (unless overridden):**
- Overwrite existing files
- Delete deprecated/renamed files from older DevSystem versions
- Don't delete unrelated existing files

**Special Rules (check per-repo):**
- Some repos may have "Never overwrite" rules for specific file patterns (e.g., `session*.md`)
- **CRITICAL:** "Never overwrite" patterns also protect files from DELETION
- Files matching these patterns are FULLY PROTECTED - no overwrite, no delete
- Check `[LINKED_REPOS]` for file-specific exceptions

#### 2.4 Copy Files

Copy files to target repo's `.windsurf` folder, respecting rules.

Note: This workflow lives in workspace root, so it won't be deployed.

#### 2.5 Report Changes

For each repo, report:
- Files copied/updated
- Files skipped (due to rules)
- Files deleted (deprecated)
- Errors encountered

### 3. Summary

Provide final summary:
- Total repos processed
- Total files deployed
- Any errors or skipped repos

## Output Format

**CRITICAL:** Use the exact format below. Do NOT use tables or other formats.

```
C:\Dev\Repo1
  [UP TO DATE] 41 files unchanged

C:\Dev\Repo2
  - Add: 41 files
      workflows\build.md, commit.md, critique.md, reconcile.md
      workflows\session-close.md, session-new.md, solve.md, test.md
      workflows\write-impl-plan.md, write-spec.md, write-test-plan.md
      ...
  - Delete: 1 deprecated file
      rules/old-file.md

C:\Dev\Repo3
  [NEW REPO] .windsurf folder does not exist - will create with 41 files

C:\Dev\Repo4
  - Add: 27 new files
      workflows\build.md, commit.md, critique.md, reconcile.md
      workflows\session-close.md, session-new.md, solve.md, test.md
      workflows\write-impl-plan.md, write-spec.md, write-test-plan.md
      ...
  - Overwrite: 13 older files
      skills/file28.md, file29.md
      ...
  - Delete: 7 deprecated files
      full/path/to/file/old1.md, old2.md
  - Skipped: session*.md files (per repo rules)

Summary: X repos to process, Y files to deploy, Z files to delete.
```

## Files to Exclude

Always exclude from deployment:
- Any files matching repo-specific "Never overwrite" patterns

Note: This workflow (`deploy-to-all-repos.md`) lives in workspace root, not in `.windsurf/`, so it is automatically excluded from deployment.

## Deprecated Files (Allowlist)

**CRITICAL:** Only delete files that are KNOWN deprecated DevSystem files. If a file is not on this list, it is considered an unrelated custom file and MUST be left untouched.

### V1 → V2 Migration (Deprecated Rules)

- `rules/commit-rules.md`
- `rules/devsystem-rules.md`
- `rules/document-rules.md`
- `rules/git-rules.md`
- `rules/proper-english-rules.md`
- `rules/python-rules.md`
- `rules/tools-rules.md`

### V2 → V3 Migration (Deprecated Workflows)

- `workflows/review-devilsadvocate.md` → replaced by `workflows/critique.md`
- `workflows/review-pragmaticprogrammer.md` → replaced by `workflows/reconcile.md`
- `workflows/new-feature.md` → replaced by `workflows/build.md`
- `workflows/new-task.md` → replaced by `workflows/solve.md`
- `workflows/setup-pdftools.md` → moved to `skills/pdf-tools/SETUP.md`

### V3 → V3.1 Migration (Deprecated/Renamed)

- `rules/edird-core.md` → renamed to `rules/edird-phase-planning.md`
- `workflows/go-autonomous.md` → renamed to `workflows/go.md`
- `workflows/next.md` → removed (use `/go` instead)
- `skills/edird-phase-model/` → renamed to `skills/edird-phase-planning/`
  - `SKILL.md` consolidated (BRANCHING.md, FLOWS.md, GATES.md, NEXT_ACTION.md removed)

### V3.1 → V3.2 Migration (Deprecated Workflows)

- `workflows/deliver.md` → removed (phase-specific, use `/implement` instead)
- `workflows/design.md` → removed (phase-specific, use `/write-spec` instead)
- `workflows/explore.md` → removed (phase-specific, use `/research` instead)
- `workflows/go-research.md` → removed (use `/research` instead)
- `workflows/refine.md` → removed (phase-specific, use `/verify` instead)

### V3.1 New Files

**Renamed Rules:**
- `rules/edird-phase-planning.md` - EDIRD phase model core (was edird-core.md)

**Renamed/Consolidated Skill:**
- `skills/edird-phase-planning/SKILL.md` - Single consolidated file (was edird-phase-model/)

**New Workflows:**
- `workflows/go.md` - Autonomous loop using recap + continue (was go-autonomous.md)
- `workflows/recap.md` - Analyze context, identify current status
- `workflows/continue.md` - Execute next items on plan
- `workflows/fail.md` - Record failures to FAILS.md
- `workflows/learn.md` - Extract learnings from failures

**If a file is NOT on the deprecated list:** Do NOT delete it. It is a custom repo-specific file.
