---
description: Deploy DevSystem files to all linked repositories
---

# Deploy to All Repos

Copies DevSystem files from this repo's `.windsurf` folder to all linked repositories according to their specific rules.

## Execution Modes

**Default (Preview/Dry-Run):** Show what WOULD be done, then ask for confirmation before making any changes.

**Auto-Execute:** If user starts workflow with confirmation keyword, perform changes immediately:
- `all`, `yes`, `confirm`, `ok`, `do it`, `execute`

Example: `/deploy-to-all-repos confirm` - executes without preview prompt

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

#### 2.2 Compare Source and Target Files

Use this PowerShell snippet to analyze all target repos at once:

```powershell
# Compare DevSystem files between source and multiple target repos
$source = "[WORKSPACE_FOLDER]\.windsurf"  # This repo's .windsurf folder
$targets = @(
    # Populate from [LINKED_REPOS] in !NOTES.md
)

# Deprecated V1 files (only these can be deleted)
$deprecatedRules = @("commit-rules.md", "devsystem-rules.md", "document-rules.md", "git-rules.md", "proper-english-rules.md", "python-rules.md", "tools-rules.md")

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
    
    # Find deprecated files
    $deprecated = Get-ChildItem -Path "$target\rules" -File -ErrorAction SilentlyContinue | 
        Where-Object { $deprecatedRules -contains $_.Name } | ForEach-Object { $_.Name }
    
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

## Example Execution

```
Processing: C:\Dev\Repo1
  - Copied: rules/core-conventions.md
  - Copied: rules/devsystem-core.md
  - Copied: workflows/prime.md
  - Deleted: workflows/old-deprecated.md (deprecated)

Processing: C:\Dev\Repo2
  - Copied: rules/core-conventions.md
  - Skipped: session*.md files (per repo rules)
  ...

Summary: 5 repos processed, 45 files deployed, 0 errors
```

## Files to Exclude

Always exclude from deployment:
- Any files matching repo-specific "Never overwrite" patterns

Note: This workflow (`deploy-to-all-repos.md`) lives in workspace root, not in `.windsurf/`, so it is automatically excluded from deployment.

## Deprecated Files (Allowlist)

**CRITICAL:** Only delete files that are KNOWN deprecated DevSystem files. If a file is not on this list, it is considered an unrelated custom file and MUST be left untouched.

**Known Deprecated DevSystem V1 Rules:**
- `commit-rules.md`
- `devsystem-rules.md`
- `document-rules.md`
- `git-rules.md`
- `proper-english-rules.md`
- `python-rules.md`
- `tools-rules.md`

**Known Deprecated DevSystem V1 Workflows:**
- (none currently identified)

**If a file is NOT on this list:** Do NOT delete it. It is a custom repo-specific file.
