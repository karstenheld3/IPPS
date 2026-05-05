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
    "Development" = @("coding-conventions", "deep-research", "edird-phase-planning", "git", "git-conventions", "github", "llm-computer-use", "llm-evaluation", "llm-transcription", "ms-playwright-mcp", "ms-playwright-mcp-v2", "pdf-tools", "playwriter-mcp", "session-management", "windows-desktop-control", "windsurf-auto-model-switcher", "write-documents", "youtube-downloader")
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
    "rules" = @("commit-rules.md", "devsystem-rules.md", "document-rules.md", "git-rules.md", "proper-english-rules.md", "python-rules.md", "tools-rules.md", "edird-core.md", "cascade-model-switching.md", "research-and-report-writing-rules.md", "implementation-specification-rules.md")
    "workflows" = @("review-devilsadvocate.md", "review-pragmaticprogrammer.md", "session-init.md", "go-autonomous.md", "next.md", "new-feature.md", "new-task.md", "setup-pdftools.md", "deliver.md", "design.md", "explore.md", "go-research.md", "refine.md", "session-resume.md", "start-conversation.md", "update-conversation.md")
}
$deprecatedSkillFolders = @("edird-phase-model", "ipps-deep-research")

# Personal workflows (from [PERSONAL_WORKFLOWS] in !NOTES.md) - excluded from Development-only repos
$personalWorkflows = @("conversation-start.md", "conversation-update.md")

function Test-FileIncluded {
    param([string]$RelPath, [string]$Category)
    if ($RelPath.StartsWith("skills\")) {
        $skillName = ($RelPath.Split('\'))[1]
        return $skillCategories[$Category] -contains $skillName
    }
    if ($Category -ne "All" -and $RelPath.StartsWith("workflows\")) {
        $fileName = Split-Path $RelPath -Leaf
        if ($personalWorkflows -contains $fileName) { return $false }
    }
    return $true
}

$sourceFiles = Get-ChildItem -Path $source -Recurse -File | Where-Object { $_.DirectoryName -notmatch '__pycache__' -and $_.Extension -ne '.pyc' } | ForEach-Object { $_.FullName.Substring($source.Length + 1) } | Where-Object { $_ }

# Collect results as objects
$results = @()
foreach ($t in $targets) {
    $target = $t.Path; $cat = $t.Skills
    $filtered = $sourceFiles | Where-Object { Test-FileIncluded $_ $cat }
    $excluded = $sourceFiles | Where-Object { -not (Test-FileIncluded $_ $cat) } | ForEach-Object { ($_ -split '\\')[1] } | Select-Object -Unique
    
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

# Format deterministically — do NOT hand-write preview output
function Format-DeployPreview {
    param($Results)
    $lines = @()
    foreach ($r in $Results) {
        $lines += ""
        $lines += $r.Path
        if ($r.IsNew) {
            $lines += "  [NEW REPO] .windsurf folder does not exist - will create with $($r.Add.Count) files"
        } elseif ($r.Add.Count -eq 0 -and $r.Overwrite.Count -eq 0 -and $r.Delete.Count -eq 0) {
            $lines += "  [UP TO DATE] $($r.Unchanged) files unchanged"
        } else {
            if ($r.Add.Count -gt 0) {
                $lines += "  - Add: $($r.Add.Count) new files"
                $lines += ($r.Add | ForEach-Object { "      $_" })
            }
            if ($r.Overwrite.Count -gt 0) {
                $lines += "  - Overwrite: $($r.Overwrite.Count) older files"
                $lines += ($r.Overwrite | ForEach-Object { "      $_" })
            }
            if ($r.Delete.Count -gt 0) {
                $lines += "  - Delete: $($r.Delete.Count) deprecated files"
                $lines += ($r.Delete | ForEach-Object { "      $_" })
            }
            if ($r.Skipped) { $lines += "  - Skipped: $($r.Skipped)" }
        }
        if ($r.ExcludedSkills -and $r.ExcludedSkills.Count -gt 0) {
            $lines += "  - Excluded skills: " + ($r.ExcludedSkills -join ', ')
        }
    }
    $lines += ""
    $add = ($Results | ForEach-Object { $_.Add.Count } | Measure-Object -Sum).Sum
    $ow  = ($Results | ForEach-Object { $_.Overwrite.Count } | Measure-Object -Sum).Sum
    $del = ($Results | ForEach-Object { $_.Delete.Count } | Measure-Object -Sum).Sum
    $lines += "Summary: $($Results.Count) repos to process, $($add + $ow) files to deploy, $del files to delete."
    return ($lines -join "`n")
}

# Emit JSON (for inspection) AND formatted text
$json = $results | ConvertTo-Json -Depth 3
$preview = Format-DeployPreview $results
Write-Output $preview
```

#### 2.3 Emit Preview to Chat

**CRITICAL:** Preview goes in chat, NOT to a `.tmp` file. Use the `Format-DeployPreview` function from step 2.2 — do NOT hand-format.

**Required format** (emitted by `Format-DeployPreview`):

```
<RepoPath>
  [UP TO DATE] N files unchanged

<RepoPath>
  - Add: N new files
      skills\<skill>\<file>.md
      workflows\<file>.md
  - Overwrite: N older files
      rules\<file>.md
      skills\<skill>\<file>.md
  - Delete: N deprecated files
      rules\<old-file>.md
  - Skipped: <reason>
  - Excluded skills: skill1, skill2

<RepoPath>
  [NEW REPO] .windsurf folder does not exist - will create with N files

Summary: X repos to process, Y files to deploy, Z files to delete.
```

**GOOD example**:

```
e:\Dev\KarstensWorkspace\.windsurf
  - Add: 10 new files
      skills\deep-research\RESEARCH_CREATE_SUMMARY.md
      skills\deep-research\RESEARCH_SUMMARY_TEMPLATE.md
      skills\ms-playwright-mcp-v2\SKILL.md
  - Overwrite: 18 older files
      rules\agentic-english.md
      rules\core-conventions.md
      workflows\verify.md

Summary: 7 repos to process, 202 files to deploy, 0 files to delete.
```

**BAD examples** (reject ALL of these):

Aligned-column / 2D grid (also counts as a table even without pipes):

```
e:\Dev\KarstensWorkspace\.windsurf            Add=10  Overwrite=18  Delete=0
e:\Dev\OpenAI-BackendTools\.windsurf          Add=10  Overwrite=19  Delete=0
```

Bullet summary without filenames:

```
- **KarstensWorkspace** (All): 10 add, 18 overwrite
- **OpenAI-BackendTools** (Dev): 10 add, 19 overwrite
```

Reworded Summary line:

```
Summary: 7 repos, 70 add, 132 overwrite, 0 delete
```

Missing filenames, "..." truncation, abbreviated paths (`sk\` instead of `skills\`), or any manual rewriting of what `Format-DeployPreview` returns.

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

Format is defined in step 2.3 and enforced by the `Format-DeployPreview` function in step 2.2. Do NOT hand-write preview output — run the function and emit its return value verbatim.

See GLOB-FL-023 and GLOB-FL-024 in FAILS.md for the failure history that motivated this enforcement.

## Files to Exclude

Always exclude from deployment:
- `__pycache__/` directories and `*.pyc` files (never deploy compiled Python bytecode)
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

### V3.3 → V3.4 Migration (Deprecated Rules)

- `rules/cascade-model-switching.md` → removed (moved to `skills/windsurf-auto-model-switcher/`)
- `rules/research-and-report-writing-rules.md` → removed (consolidated into `skills/write-documents/`)
- `rules/implementation-specification-rules.md` → removed (consolidated into `skills/write-documents/`)

### V3.6 Migration (Renamed Workflows)

- `workflows/start-conversation.md` → renamed to `workflows/conversation-start.md`
- `workflows/update-conversation.md` → renamed to `workflows/conversation-update.md`

### V3.4 Migration (Renamed/New Workflows)

- `workflows/fix.md` - NEW generic problem-fixing workflow (reads DevSystem knowledge)
- `workflows/bugfix.md` - Code bug fixing (was fix.md, now separate)

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
