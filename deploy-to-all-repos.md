---
description: Deploy DevSystem files to all linked repositories
---

# Deploy to All Repos

Copies DevSystem files from this repo's `.windsurf` folder to all linked repositories according to their specific rules.

## MUST-NOT-FORGET

1. **Check DevSystem version FIRST** - Read `!NOTES.md` to get `[DEVSYSTEM]` (e.g., `DevSystemV3.1`) before ANY other action
2. **Read target repo NOTES.md** - For each repo in `[LINKED_REPOS]`, read its `!NOTES.md` or `NOTES.md` to check for special deployment rules (e.g., OpenClaw has no `.windsurf/` folder)
3. **Sync before deploy** - Copy from `[DEVSYSTEM]\*` to `.windsurf\` BEFORE running preview
4. **Clean deprecated files** - Remove deprecated files from `.windsurf/` after sync (edird-core.md, go-autonomous.md, next.md, edird-phase-model/)
5. **Output format** - ALWAYS use the exact text format in "Output Format" section (NO tables, NO markdown tables)
6. **List filenames** - ALWAYS list explicit filenames after each category (Add, Overwrite, Delete), not just counts
7. **PowerShell execution** - Run PowerShell code directly (pwsh IS PowerShell Core). Do NOT wrap in `powershell -Command "..."` - that causes `$` escaping conflicts
8. **Skill categories** - Each repo has a `Skills:` assignment (All, Development, Personal). Only deploy skills matching that category

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

Read `[SKILL_CATEGORIES]` and `[LINKED_REPOS]` sections from `!NOTES.md` to get:
- Skill category definitions (Development, Personal, All)
- List of target repositories with their assigned skill category
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

#### 2.2 Compare Source and Target Files (JSON Output)

Run this PowerShell script. It outputs JSON for consistent parsing:

```powershell
# Compare DevSystem files - outputs JSON
$source = "[WORKSPACE_FOLDER]\.windsurf"

# Skill categories (from [SKILL_CATEGORIES] in !NOTES.md)
$skillCategories = @{
    "Development" = @("coding-conventions", "deep-research", "edird-phase-planning", "git-conventions", "github", "llm-computer-use", "llm-evaluation", "llm-transcription", "ms-playwright-mcp", "pdf-tools", "session-management", "windows-desktop-control", "windsurf-auto-model-switcher", "write-documents", "youtube-downloader")
    "Personal" = @("google-account", "travel-info")
}
$skillCategories["All"] = $skillCategories["Development"] + $skillCategories["Personal"]

# Target repos (from [LINKED_REPOS] in !NOTES.md)
$targets = @(
    @{ Path = "e:\Dev\KarstensWorkspace\.windsurf"; Skills = "All" }
    @{ Path = "e:\Dev\OpenAI-BackendTools\.windsurf"; Skills = "Development" }
    @{ Path = "e:\Dev\PRXL\src\.windsurf"; Skills = "Development" }
    @{ Path = "e:\Dev\SharePoint-GPT-Middleware\.windsurf"; Skills = "Development" }
    @{ Path = "e:\Dev\USTVA\.windsurf"; Skills = "Development" }
    @{ Path = "e:\Dev\openclaw\workspace"; Skills = "All" }
    @{ Path = "e:\Dev\LLM-Research\.windsurf"; Skills = "Development" }
)

# Deprecated files allowlist
$deprecatedFiles = @{
    "rules" = @("commit-rules.md", "devsystem-rules.md", "document-rules.md", "git-rules.md", "proper-english-rules.md", "python-rules.md", "tools-rules.md", "edird-core.md")
    "workflows" = @("review-devilsadvocate.md", "review-pragmaticprogrammer.md", "session-init.md", "go-autonomous.md", "next.md", "new-feature.md", "new-task.md", "setup-pdftools.md", "deliver.md", "design.md", "explore.md", "go-research.md", "refine.md", "session-resume.md")
}
$deprecatedSkillFolders = @("edird-phase-model", "ipps-deep-research")

function Test-SkillIncluded {
    param([string]$RelPath, [string]$Category)
    if (-not $RelPath.StartsWith("skills\")) { return $true }
    $skillName = ($RelPath.Split('\'))[1]
    return $skillCategories[$Category] -contains $skillName
}

$sourceFiles = Get-ChildItem -Path $source -Recurse -File | ForEach-Object { $_.FullName.Substring($source.Length + 1) } | Where-Object { $_ }

# Collect results as objects
$results = @()
foreach ($t in $targets) {
    $target = $t.Path; $cat = $t.Skills
    $filtered = $sourceFiles | Where-Object { Test-SkillIncluded $_ $cat }
    $excluded = $sourceFiles | Where-Object { -not (Test-SkillIncluded $_ $cat) } | ForEach-Object { ($_ -split '\\')[1] } | Select-Object -Unique
    
    $r = @{ Path = $target; Skills = $cat; IsNew = $false; Add = @(); Overwrite = @(); Unchanged = 0; Delete = @(); ExcludedSkills = @($excluded) }
    
    if (-not (Test-Path $target)) {
        $r.IsNew = $true; $r.Add = @($filtered)
    } else {
        foreach ($rel in $filtered) {
            $src = Join-Path $source $rel; $tgt = Join-Path $target $rel
            if (-not (Test-Path $tgt)) { $r.Add += $rel }
            elseif ((Get-FileHash $src -Algorithm MD5).Hash -ne (Get-FileHash $tgt -Algorithm MD5).Hash) { $r.Overwrite += $rel }
            else { $r.Unchanged++ }
        }
        foreach ($folder in $deprecatedFiles.Keys) {
            Get-ChildItem -Path "$target\$folder" -File -EA SilentlyContinue | Where-Object { $deprecatedFiles[$folder] -contains $_.Name } | ForEach-Object { $r.Delete += "$folder\$($_.Name)" }
        }
        foreach ($sf in $deprecatedSkillFolders) { if (Test-Path "$target\skills\$sf") { $r.Delete += "skills\$sf" } }
    }
    $results += [PSCustomObject]$r
}

# Output JSON
$results | ConvertTo-Json -Depth 3
```

#### 2.3 Format JSON Output

Parse the JSON and format as text. **CRITICAL:** Use this exact format:

```
[Path]
  [UP TO DATE] N files unchanged

[Path]
  - Add: N files
      file1, file2, file3
  - Overwrite: N files
      file1, file2
  - Delete: N deprecated files
      file1, file2
  - Excluded skills: skill1, skill2

[Path]
  [NEW REPO] .windsurf folder does not exist - will create with N files
  - Excluded skills: skill1, skill2

Summary: X repos to process, Y files to deploy, Z files to delete.
```

#### 2.4 Apply Copy Rules

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

### 3. Verify MNF Compliance

Review each MNF item above and confirm compliance.

### 4. Summary

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
      workflows\session-finalize.md, session-new.md, solve.md, test.md
      workflows\write-impl-plan.md, write-spec.md, write-test-plan.md
      ...
  - Delete: 1 deprecated file
      rules/old-file.md

C:\Dev\Repo3
  [NEW REPO] .windsurf folder does not exist - will create with 41 files

C:\Dev\Repo4
  - Add: 27 new files
      workflows\build.md, commit.md, critique.md, reconcile.md
      workflows\session-finalize.md, session-new.md, solve.md, test.md
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

### V3.2 Migration (Deprecated Skills Files)

- `skills/llm-transcription/transcribe-image-to-markdown-advanced.py` → removed (consolidated into transcribe-image-to-markdown.py)

### V3.2 → V3.3 Migration (Renamed Skills)

- `skills/ipps-deep-research/` → renamed to `skills/deep-research/`

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

## OpenClaw-Specific Files

For the OpenClaw workspace (`e:\Dev\openclaw\workspace`) only:

**Additional files to sync from workspace root:**
- `_OPENCLAW-AGENTS.md` → copy to `AGENTS.md` (one-time setup, or when updated)
- `_OPENCLAW_WORKFLOWS.md` → copy to `WORKFLOWS.md` (sync every time workflows added/removed)

**These files are NOT synced to other repos** - they are OpenClaw-specific.
