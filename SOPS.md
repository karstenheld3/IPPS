# Standard Operating Procedures (SOPs)

**Goal**: Prevent drift between `[PROMPTSYSTEM_FOLDER]`, `[AGENT_FOLDER]`, and linked repos when changing skills, workflows, or versions.

**Why**: Skills and categories are duplicated across `NOTES.md` and every synced repo. Missing a step silently propagates stale or unregistered content.

**Acronyms**: SOP = Standard Operating Procedure. MNF = MUST-NOT-FORGET.

## Placeholders

- `[PROMPTSYSTEM_FOLDER]` — current PromptSystem source (e.g., `E:\Dev\IPPS\DevSystemV3.6`)
- `[WORKSPACE]` — `E:\Dev\IPPS`
- `[AGENT_FOLDER]` — active agent config (e.g., `[WORKSPACE]\.devin`)
- `<skill>` — skill folder name (e.g., `playwriter-mcp`)
- `<workflow>` — workflow filename without extension (e.g., `adp`)

## MUST-NOT-FORGET

- `[PROMPTSYSTEM_FOLDER]` is the source of truth. Never edit `.devin/` directly
- Skills are discovered by scanning `skills/` folder at startup. No manual registration list needed
- Sync `[PROMPTSYSTEM_FOLDER]` → `.devin/` BEFORE running `/sync workspace`
- `Copy-Item -Recurse -Force` does NOT delete files that no longer exist at source — deletions require explicit `Remove-Item`
- Every SOP ends with a verification step before you can consider the change complete
- All prior PromptSystem releases MUST be backed up in `[WORKSPACE]\_OldDevSystemVersions\` before deletion (SOP 4 step 6)
- **NEVER mention private sessions folder in public artifacts**: release notes, git commit messages, GitHub releases, README, or any publicly visible file. Use generic "internal session" or omit entirely. Session inventories in release notes must only include sessions from `_Sessions/` (tracked sessions), never from the private sessions folder.
- **Release naming convention**: All releases use `vX.Y` format everywhere — git tags, GitHub release titles, release notes headers. Format: `release vX.Y` for GitHub release title, `# Release Notes: vX.Y (YYYY-MM-DD)` for release notes header. No date-based tags, no descriptive suffixes in titles.

## Table of Contents

- [Quick Reference: Sync Command](#quick-reference-sync-command)
- [SOP 1: New Skill Created](#sop-1-new-skill-created)
- [SOP 2: Skill File Added or Removed](#sop-2-skill-file-added-or-removed)
- [SOP 3: Old Skill Deleted or Deprecated](#sop-3-old-skill-deleted-or-deprecated)
- [SOP 4: PromptSystem Version Changed](#sop-4-promptsystem-version-changed)
- [SOP 5: Model Registry JSON Files Updated](#sop-5-model-registry-json-files-updated)
- [SOP 6: Workflow Added, Edited, or Removed](#sop-6-workflow-added-edited-or-removed)
- [SOP 7: Post-Release Version Bump](#sop-7-post-release-version-bump)
- [Common Verification Commands](#common-verification-commands)

## Quick Reference: Sync Command

Sync `[PROMPTSYSTEM_FOLDER]` → `.devin/` after any edit to source. Referenced by NOTES.md "sync" keyword.

```powershell
Copy-Item -Path "[PROMPTSYSTEM_FOLDER]\*" -Destination "[WORKSPACE]\.devin\" -Recurse -Force
```

**Note**: `Copy-Item` does NOT remove files deleted at source. For removal, see SOP 2 (file) or SOP 3 (skill). Use `/sync workspace` with `sync.ps1 -execute` for full sync including deletions via `deprecated` patterns in `promptsystem-sync.json`.

## SOP 1: New Skill Created

**Scenario**: Adding a new skill folder (e.g., `playwriter-mcp`) to PromptSystem.

### Files to modify

1. **Create skill folder**: `[PROMPTSYSTEM_FOLDER]/skills/<skill>/`
   - Required: `SKILL.md` (name, purpose, usage)
   - Optional: `SETUP.md`, `UNINSTALL.md`, `references/`, `assets/`, scripts

2. **Register skill** in `promptsystem-sync.json` at target `[WORKSPACE_FOLDER]` root:
   - Add skill to appropriate bundle include patterns in source entry
   - Sync will distribute to all targets that select that bundle

3. **If skill introduces a workflow**: also create `[PROMPTSYSTEM_FOLDER]/workflows/<name>.md`

4. **If skill introduces a new TOPIC**: register in `[WORKSPACE]/ID-REGISTRY.md`

5. **Sync to `.devin/`**:
   ```powershell
   Copy-Item -Path "[PROMPTSYSTEM_FOLDER]\*" -Destination "[WORKSPACE]\.devin\" -Recurse -Force
   ```

### Verification

```powershell
# 1. Skill folder present in both source and synced copy
Test-Path "[PROMPTSYSTEM_FOLDER]\skills\<skill>\SKILL.md"
Test-Path "[WORKSPACE]\.devin\skills\<skill>\SKILL.md"

# 2. Skill registered in NOTES.md
Select-String -Path "[WORKSPACE]\NOTES.md" -Pattern "<skill>"

# 3. Sync preview includes skill in Add for synced repos
# Run /sync workspace in diff mode and check new skill appears in Add list
```

## SOP 2: Skill File Added or Removed

**Scenario**: Adding new helper script / removing obsolete doc within an existing skill.

### Files to modify

**Adding a file**:
1. Create in `[PROMPTSYSTEM_FOLDER]/skills/<skill>/<new-file>`
2. Sync: `Copy-Item [PROMPTSYSTEM_FOLDER]\* .devin\ -Recurse -Force`
3. **Sync preview shows file in `Add` for all repos** → confirm and run `/sync workspace -execute`

**Removing a file**:
1. Delete from `[PROMPTSYSTEM_FOLDER]/skills/<skill>/<old-file>`
2. Delete from `[WORKSPACE]/.devin/skills/<skill>/<old-file>` (sync does NOT remove)
3. **Known gap**: `Copy-Item` sync does not remove orphaned files from target repos. Use `deprecated` patterns in `promptsystem-sync.json` for full cleanup via `sync.ps1 -execute`. Two options:
   - **Acceptable**: leave stale file in synced repos (no harm if unreferenced)
   - **Full cleanup**: add file pattern to `deprecated` array in `promptsystem-sync.json`, run `/sync workspace -execute`

### Verification

**After adding a file**:

```powershell
# Presence in both locations
Test-Path "[PROMPTSYSTEM_FOLDER]\skills\<skill>\<file>"
Test-Path "[WORKSPACE]\.devin\skills\<skill>\<file>"

# Hash match
(Get-FileHash "[PROMPTSYSTEM_FOLDER]\skills\<skill>\<file>").Hash -eq `
(Get-FileHash "[WORKSPACE]\.devin\skills\<skill>\<file>").Hash
```

**After removing a file**:

```powershell
# Absence in both locations (both should return False)
Test-Path "[PROMPTSYSTEM_FOLDER]\skills\<skill>\<old-file>"
Test-Path "[WORKSPACE]\.devin\skills\<skill>\<old-file>"
```

## SOP 3: Old Skill Deleted or Deprecated

**Scenario**: Retiring a skill (e.g., `edird-phase-model` → replaced by `edird-phase-planning`).

### Files to modify

1. **Delete skill folder from source**:
   ```powershell
   Remove-Item "[PROMPTSYSTEM_FOLDER]\skills\<skill>" -Recurse -Force
   Remove-Item "[WORKSPACE]\.devin\skills\<skill>" -Recurse -Force
   ```

2. **Add to deprecated patterns** in `promptsystem-sync.json`:
   - Add `skills/<skill>/*` to `deprecated` array in relevant source entry
   - This triggers deletion in synced repos on next `/sync workspace -execute`

3. **Document migration** in NOTES.md or session NOTES.md:
   ```markdown
   ### V3.x Migration (Deprecated Skills)
   - `skills/<skill>/` → removed (migrated to `<replacement>` or obsolete)
   ```

4. **If skill had a TOPIC**: mark deprecated in `ID-REGISTRY.md` (do NOT delete, keep history)

### Verification

```powershell
# 1. Folder gone from both source and synced copy
-not (Test-Path "[PROMPTSYSTEM_FOLDER]\skills\<skill>")
-not (Test-Path "[WORKSPACE]\.devin\skills\<skill>")

# 2. Skill NOT in active registries
Select-String -Path "[WORKSPACE]\NOTES.md" -Pattern "\b<skill>\b"  # should return nothing
# promptsystem-sync.json should list it ONLY in deprecated, not in bundle includes

# 3. Sync preview shows "Delete: skills\<skill>" for each synced repo that still has it
# After /sync workspace -execute: verify folder gone from every synced repo
```

## SOP 4: PromptSystem Version Changed

**Scenario**: Moving from `DevSystemV3.6` to `DevSystemV3.7`.

### Files to modify

1. **Create new version folder**:
   ```powershell
   Copy-Item -Path "[WORKSPACE]\DevSystemV3.6" -Destination "[WORKSPACE]\DevSystemV3.7" -Recurse
   ```

2. **Update `NOTES.md`**:
   - Change `[PRODUCT_VERSION]: 3.6` → `[PRODUCT_VERSION]: 3.7` (search for `\[PRODUCT_VERSION\]:`)
   - `[PROMPTSYSTEM_FOLDER]` line usually needs no change (uses `[PRODUCT_VERSION]` placeholder)

3. **Sync new version to `.devin/`**:
   ```powershell
   Copy-Item -Path "[WORKSPACE]\DevSystemV3.7\*" -Destination "[WORKSPACE]\.devin\" -Recurse -Force
   ```

4. **Document migration** in NOTES.md or session NOTES.md:
   - Add section `### V3.6 → V3.7 Migration` under deprecated notes
   - List renamed/removed files and their replacements
   - If files were deleted: add patterns to `deprecated` array in `promptsystem-sync.json`
   - If skills were removed: add `skills/<skill>/*` to `deprecated`

5. **Update SOPs and docs with new version**:
   - `SOPS.md` example paths reference `DevSystemV3.6` in comments — update to new version
   - Any other docs with hardcoded version strings — search and update

6. **Archive old version** (MANDATORY before deletion):
   ```powershell
   Move-Item "[WORKSPACE]\DevSystemV3.6" "[WORKSPACE]\_OldDevSystemVersions\DevSystemV3.6"
   ```
   All prior releases MUST be preserved in `[WORKSPACE]\_OldDevSystemVersions\`. Never delete a version folder without moving it there first.

7. **Run workflow reference check** (MANDATORY):
   ```powershell
   .\check_workflow_refs.ps1
   ```
   Fix any broken references before proceeding. Zero broken references required.

8. **Commit before syncing**: new version is a major change, isolate in git history

9. **Sync to linked repos** via `/sync workspace` (always preview with `-diff` first)

### Verification

```powershell
# 1. NOTES.md points to new version
Select-String -Path "[WORKSPACE]\NOTES.md" -Pattern "\[PRODUCT_VERSION\]:"
# Expected: "[PRODUCT_VERSION]: 3.7"

# 2. .devin matches new version (spot-check a file hash)
(Get-FileHash "[WORKSPACE]\DevSystemV3.7\skills\write-documents\WORKFLOW_RULES.md").Hash -eq `
(Get-FileHash "[WORKSPACE]\.devin\skills\write-documents\WORKFLOW_RULES.md").Hash

# 3. Full byte-count parity (counts should match)
(Get-ChildItem "[WORKSPACE]\DevSystemV3.7" -Recurse -File).Count
(Get-ChildItem "[WORKSPACE]\.devin"      -Recurse -File).Count

# 4. Sync preview shows migration diffs only (no unexpected drift)
# Run /sync workspace -diff, expect:
# - Old-version-specific deprecated files in Delete list
# - Renamed/new files in Add list
# - No Overwrites for files that should be unchanged
```

## SOP 5: Model Registry JSON Files Updated

**Scenario**: Adding a new model, updating pricing, or changing parameter mappings in the LLM evaluation JSON files.

### Source of truth

`[PROMPTSYSTEM_FOLDER]/skills/llm-evaluation/` contains the canonical copies:
- `model-registry.json` — model IDs, context windows, prefix routing, effort levels
- `model-pricing.json` — per-model token pricing
- `model-parameter-mapping.json` — CLI effort-to-API parameter mapping

### All known targets

These locations contain replicas that must be kept in sync:

- **Sync target**: `[WORKSPACE]/.devin/skills/llm-evaluation/` (via standard PromptSystem sync)
- **Same-repo replica**: `[PROMPTSYSTEM_FOLDER]/skills/llm-transcription/` (3 JSON files)
- **External repo**: `E:/Dev/LLM-Research/_Sessions/_2026-03-05_TabularDataFormatsForLLMs/01_CSVScaleLimits/_Scripts/` (3 JSON files)
- **External repo**: `E:/Dev/LLM-Research/_Sessions/_2026-03-05_TabularDataFormatsForLLMs/02_FormatComparison/_Scripts/` (3 JSON files)

**Not a replica**: `[PROMPTSYSTEM_FOLDER]/skills/devin-auto-model-switcher/windsurf-model-registry.json` — different format (Windsurf UI credit multipliers), not API model data.

### Steps

1. **Edit source** in `[PROMPTSYSTEM_FOLDER]/skills/llm-evaluation/`

2. **Copy to all replicas**:
   ```powershell
   $src = "[PROMPTSYSTEM_FOLDER]\skills\llm-evaluation"
   $files = @("model-registry.json","model-pricing.json","model-parameter-mapping.json")
   $targets = @(
     "[PROMPTSYSTEM_FOLDER]\skills\llm-transcription",
     "E:\Dev\LLM-Research\_Sessions\_2026-03-05_TabularDataFormatsForLLMs\01_CSVScaleLimits\_Scripts",
     "E:\Dev\LLM-Research\_Sessions\_2026-03-05_TabularDataFormatsForLLMs\02_FormatComparison\_Scripts"
   )
   foreach ($t in $targets) {
     foreach ($f in $files) { Copy-Item "$src\$f" "$t\$f" -Force }
   }
   ```

3. **Sync PromptSystem to `.devin/`**:
   ```powershell
   Copy-Item -Path "[PROMPTSYSTEM_FOLDER]\*" -Destination "[WORKSPACE]\.devin\" -Recurse -Force
   ```

4. **If effort levels changed**: also update `EFFORT_LEVELS` in `call-llm.py` and `call-llm-batch.py` (both in `[PROMPTSYSTEM_FOLDER]/skills/llm-evaluation/`), then re-sync

5. **If a new model was added**: add test entries to `test-call-llm.py`, run tests, update `LLM_EVALUATION_CLAUDE_MODELS.md`

6. **Create source documentation** in `[WORKSPACE]/_Sessions/!ModelRegistryUpdate/model-sources/` with `[DATE]_` prefix

### Verification

```powershell
$src = "[PROMPTSYSTEM_FOLDER]\skills\llm-evaluation"
$files = @("model-registry.json","model-pricing.json","model-parameter-mapping.json")
$targets = @(
  "[WORKSPACE]\.devin\skills\llm-evaluation",
  "[PROMPTSYSTEM_FOLDER]\skills\llm-transcription",
  "[WORKSPACE]\.devin\skills\llm-transcription",
  "E:\Dev\LLM-Research\_Sessions\_2026-03-05_TabularDataFormatsForLLMs\01_CSVScaleLimits\_Scripts",
  "E:\Dev\LLM-Research\_Sessions\_2026-03-05_TabularDataFormatsForLLMs\02_FormatComparison\_Scripts"
)
$ok = 0; $fail = 0
foreach ($t in $targets) {
  foreach ($f in $files) {
    if ((Get-FileHash "$src\$f").Hash -eq (Get-FileHash "$t\$f").Hash) { $ok++ }
    else { $fail++; Write-Host "MISMATCH: $t\$f" }
  }
}
Write-Host "$ok OK, $fail FAIL"
```

Expected: 15 OK, 0 FAIL (5 targets x 3 files).

## SOP 6: Workflow Added, Edited, or Removed

**Scenario**: Adding a new workflow, editing an existing one, or removing an obsolete workflow.

### Adding or Editing a Workflow

1. **Edit in source**: `[PROMPTSYSTEM_FOLDER]/workflows/<workflow>.md`
   - New workflow: create file following `WORKFLOW_RULES.md` (WF-HD-01 through WF-EX-01)
   - Existing workflow: edit in place

2. **Sync to `[AGENT_FOLDER]`**:
   ```powershell
   Copy-Item -Path "[PROMPTSYSTEM_FOLDER]\*" -Destination "[AGENT_FOLDER]\" -Recurse -Force
   ```

3. **If new workflow**: register in `promptsystem-core.md` Workflow Reference section (alphabetical)

4. **If new workflow**: update `README.md` workflow list and count

5. **Run `/sync`** to propagate changes to `promptsystem-core.md` and `README.md`

6. **If new TOPIC introduced**: register in `ID-REGISTRY.md`

### Removing a Workflow

1. **Delete from source and agent folder**:
   ```powershell
   Remove-Item "[PROMPTSYSTEM_FOLDER]\workflows\<workflow>.md" -Force
   Remove-Item "[AGENT_FOLDER]\workflows\<workflow>.md" -Force
   ```

2. **Remove from `promptsystem-core.md`** Workflow Reference section

3. **Remove from `README.md`** workflow list, update count

4. **If workflow exists in synced repos**: add to `deprecated` patterns in `promptsystem-sync.json`:
   - Add `workflows/<workflow>.md` to `deprecated` array in relevant source entry
   - Next `/sync workspace -execute` will delete it from synced repos

5. **If workflow had a TOPIC**: mark deprecated in `ID-REGISTRY.md` (keep history)

6. **Run `/sync`** to propagate removals to `promptsystem-core.md` and `README.md`

### Verification

**After adding or editing**:

```powershell
# 1. File present in both locations with matching content
Test-Path "[PROMPTSYSTEM_FOLDER]\workflows\<workflow>.md"
Test-Path "[AGENT_FOLDER]\workflows\<workflow>.md"
(Get-FileHash "[PROMPTSYSTEM_FOLDER]\workflows\<workflow>.md").Hash -eq `
(Get-FileHash "[AGENT_FOLDER]\workflows\<workflow>.md").Hash

# 2. Registered in promptsystem-core.md and README.md (new workflows only)
Select-String -Path "[PROMPTSYSTEM_FOLDER]\specs\promptsystem-core.md" -Pattern "<workflow>"
Select-String -Path "[WORKSPACE]\README.md" -Pattern "<workflow>"
```

**After removing**:

```powershell
# 1. File absent from both locations (both should return False)
Test-Path "[PROMPTSYSTEM_FOLDER]\workflows\<workflow>.md"
Test-Path "[AGENT_FOLDER]\workflows\<workflow>.md"

# 2. Not referenced in promptsystem-core.md or README.md
Select-String -Path "[PROMPTSYSTEM_FOLDER]\specs\promptsystem-core.md" -Pattern "<workflow>"  # should return nothing
Select-String -Path "[WORKSPACE]\README.md" -Pattern "<workflow>"  # should return nothing

# 3. Listed in deprecated (if synced to downstream repos)
Select-String -Path "[WORKSPACE]\promptsystem-sync.json" -Pattern "<workflow>"
```

## SOP 7: Post-Release Version Bump

**Scenario**: A release was tagged (e.g., `v4.0`). The working version must be incremented immediately so ongoing development is distinguishable from the released state.

**Why**: Without a bump, the folder name matches the tagged release. Anyone (human or agent) inspecting the workspace cannot tell whether the current state IS the release or has diverged. Git tags are invisible in the filesystem.

### When to apply

Immediately after `git tag` and `git push --tags` for a release. This is the LAST step of the release process.

### Steps

1. **Determine next version**: Increment minor version (e.g., `4.0` → `4.1`). Use major bump only if explicitly planned.

2. **Backup released version** (MANDATORY before rename):
   ```powershell
   # Restore the released version from git at the tag commit
   git archive [TAG] -- "PromptSystem[OLD_VERSION]/" | tar -x -C .
   # Move to archive
   Move-Item "[WORKSPACE]\PromptSystem[OLD_VERSION]" "[WORKSPACE]\_OldDevSystemVersions\PromptSystem[OLD_VERSION]"
   ```
   All prior releases MUST be preserved in `[WORKSPACE]\_OldDevSystemVersions\`. Never rename a version folder without backing it up first.

3. **Rename working folder**:
   ```powershell
   Rename-Item "[WORKSPACE]\PromptSystem[OLD_VERSION]" "PromptSystem[NEW_VERSION]"
   ```

4. **Update `NOTES.md`**:
   - `[PRODUCT_VERSION]: [NEW_VERSION]`

5. **Sync to `.devin/`**:
   ```powershell
   Copy-Item -Path "[WORKSPACE]\PromptSystem[NEW_VERSION]\*" -Destination "[WORKSPACE]\.devin\" -Recurse -Force
   ```

6. **Commit**:
   ```powershell
   git add -A
   git commit -m "chore: bump working version to [NEW_VERSION]"
   ```

### Verification

```powershell
# 1. Old folder gone, new folder exists
-not (Test-Path "[WORKSPACE]\PromptSystem[OLD_VERSION]")
Test-Path "[WORKSPACE]\PromptSystem[NEW_VERSION]"

# 2. Released version backed up
Test-Path "[WORKSPACE]\_OldDevSystemVersions\PromptSystem[OLD_VERSION]"

# 3. NOTES.md references new version
Select-String -Path "[WORKSPACE]\NOTES.md" -Pattern "Current \[PROMPTSYSTEM\]: PromptSystem[NEW_VERSION]"

# 4. .devin/ is synced (spot-check)
(Get-ChildItem "[WORKSPACE]\PromptSystem[NEW_VERSION]" -Recurse -File).Count -eq `
(Get-ChildItem "[WORKSPACE]\.devin" -Recurse -File).Count
```

## Common Verification Commands

### Check for `__pycache__` pollution

```powershell
Get-ChildItem -Path "[WORKSPACE]\DevSystemV3.6","[WORKSPACE]\.devin" -Recurse -Directory -Filter "__pycache__"
# Expected: no output
# Cleanup: pipe to Remove-Item -Recurse -Force
```

### Check skill registration consistency

```powershell
# Extract skills from NOTES.md
$notes = (Select-String -Path "[WORKSPACE]\NOTES.md" -Pattern "^\- \*\*Development\*\*:").Line
# Verify all skills in skills/ folder are registered
Get-ChildItem "[PROMPTSYSTEM_FOLDER]\skills" -Directory | ForEach-Object { $_.Name } | Sort-Object
# Visually compare — they must list identical skills
```

### Compare source vs sync (after any change)

```powershell
# Files in PromptSystem but not in .devin (missing sync)
$src = Get-ChildItem "[PROMPTSYSTEM_FOLDER]" -Recurse -File | ForEach-Object { $_.FullName.Substring("[PROMPTSYSTEM_FOLDER]".Length) }
$dst = Get-ChildItem "[WORKSPACE]\.devin" -Recurse -File | ForEach-Object { $_.FullName.Substring("[WORKSPACE]\.devin".Length) }
Compare-Object $src $dst | Where-Object SideIndicator -eq "<="
```

### Workflow reference integrity check

Mandatory before any release (SOP 4 step 7). Detects references to non-existing workflows in specs, skills, README, and ID-REGISTRY.

```powershell
# Auto-detects [PROMPTSYSTEM_FOLDER] from NOTES.md
.\check_workflow_refs.ps1

# Or specify explicitly
.\check_workflow_refs.ps1 -PromptSystemFolder "[PROMPTSYSTEM_FOLDER]"
```

Expected: `None found!` (zero broken references). Any match must be fixed before release.

### Synced repo drift check

Run `/sync workspace -diff` in preview mode. Any unexpected items in `Add` / `Modify` / `Delete` indicate a missed sync or unregistered skill.

## Document History

**[2026-09-06 14:50]**
- Removed: [SKILL_CATEGORIES] section from NOTES.md and template — skills discovered by scanning skills/ folder, sync controlled by devsystem-sync.json bundles
- Fixed: SOP 2 step 3 — "Deploy preview" to "Sync preview" [VERIFIED from /verify]
- Fixed: SOP 4 step 8 — "Commit before deploying" to "Commit before syncing" [VERIFIED from /verify]
- Fixed: SOP 6 verification — "if deployed to synced repos" to "if synced to downstream repos" [VERIFIED from /verify]
- Fixed: SOP 6 verification commands — `rules\devsystem-core.md` to `specs\devsystem-core.md` (3 occurrences) [VERIFIED from /verify]
- Fixed: Workflow reference check description — "rules, skills, README" to "specs, skills, README" [VERIFIED from /verify]

**[2026-08-31 18:24]**
- Added: Mandatory workflow reference check (SOP 4 step 7) using `check_workflow_refs.ps1`
- Added: Workflow reference integrity check in Common Verification Commands
- Changed: SOP 4 steps renumbered (commit → step 8, deploy → step 9)

**[2026-07-13 13:54]**
- Added: SOP 7 for post-release version bump (increment working version after tagging)

**[2026-06-13 13:47]**
- Added: SOP 6 for workflow add/edit/remove with sync to `[AGENT_FOLDER]`
- Changed: Goal and placeholders updated to include workflows and `[AGENT_FOLDER]`

**[2026-05-30 17:03]**
- Added: SOP 5 for model registry JSON deployment with all known targets

**[2026-04-20 13:15]**
- Added: Quick Reference Sync Command section (fixes NOTES.md "deploy" pointer precision)
- Added: SOP acronym definition (WF-CT-02)
- Added: SOP 2 verification for removal case (check absence, not just presence)
- Added: SOP 4 step 5 for updating SOPs/docs on version change
- Changed: Approximate line numbers (“~line 78”) replaced with pattern-based search hints
- Changed: SOP 4 steps re-numbered (was 5-7, now 5-8 after insertion)

**[2026-04-20 13:06]**
- Initial creation: SOPs for 4 scenarios (new skill, file add/remove, skill delete, version change)
