---
description: Deploy DevSystem files to all linked repositories
---

# Deploy to All Repos

Copies DevSystem files from this repo's `.windsurf` folder to all linked repositories according to their specific rules.

## Prerequisites

Read `[LINKED_REPOS]` section from `*NOTES.md` to get:
- List of target repositories
- Copy/overwrite rules for each repo
- Files to preserve (if any)

## Workflow Steps

### 1. Read Configuration

Read `*NOTES.md` and extract `[LINKED_REPOS]` section.

### 2. For Each Linked Repository

Execute the following for each repo in `[LINKED_REPOS]`:

#### 2.1 Verify Target Exists

Check that the target repo path exists. Skip if not found (warn user).

#### 2.2 List Source Files

List all files in this repo's `.windsurf` folder:
- `.windsurf/rules/*.md`
- `.windsurf/workflows/*.md`
- `.windsurf/skills/**/*`

#### 2.3 Apply Copy Rules

For each source file, apply the repo-specific rules:

**Standard Rules (unless overridden):**
- Overwrite existing files
- Delete deprecated/renamed files from older DevSystem versions
- Don't delete unrelated existing files

**Special Rules (check per-repo):**
- Some repos may have "Never overwrite" rules for specific files
- Check `[LINKED_REPOS]` for file-specific exceptions

#### 2.4 Copy Files

Copy files to target repo's `.windsurf` folder, respecting rules.

**CRITICAL: NEVER copy this workflow file (`deploy-to-all-repos.md`) to linked repos.**

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
Processing: e:\Dev\Repo1
  - Copied: rules/core-conventions.md
  - Copied: rules/devsystem-core.md
  - Copied: workflows/prime.md
  - Skipped: workflows/deploy-to-all-repos.md (self-exclusion)
  - Deleted: workflows/old-deprecated.md (deprecated)

Processing: e:\Dev\Repo2
  - Copied: rules/core-conventions.md
  - Skipped: session*.md files (per repo rules)
  ...

Summary: 5 repos processed, 45 files deployed, 0 errors
```

## Files to Exclude

Always exclude from deployment:
- `workflows/deploy-to-all-repos.md` (this workflow - NEVER deploy to linked repos)
- Any files matching repo-specific "Never overwrite" patterns

## Deprecated Files

When deleting deprecated files, check for files that:
- Were renamed in newer DevSystem versions
- Were removed from DevSystem
- Have old naming conventions

Common deprecated patterns:
- Old workflow names that were renamed
- Files from DevSystemV1 if upgrading to V2
