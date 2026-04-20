# Standard Operating Procedures (SOPs)

**Goal**: Prevent drift between `[DEVSYSTEM_FOLDER]`, `.windsurf/`, and linked repos when changing skills or versions.

**Why**: Skills and categories are duplicated across `NOTES.md`, `deploy-to-all-repos.md`, and every linked repo. Missing a step silently propagates stale or unregistered content.

**Acronyms**: SOP = Standard Operating Procedure. MNF = MUST-NOT-FORGET.

## Placeholders

- `[DEVSYSTEM_FOLDER]` — current DevSystem source (e.g., `E:\Dev\IPPS\DevSystemV3.6`)
- `[WORKSPACE]` — `E:\Dev\IPPS`
- `<skill>` — skill folder name (e.g., `playwriter-mcp`)

## MUST-NOT-FORGET

- `[DEVSYSTEM_FOLDER]` is the source of truth. Never edit `.windsurf/` directly
- `NOTES.md [SKILL_CATEGORIES]` and `deploy-to-all-repos.md $skillCategories` must stay in sync (duplicated list — weakness)
- Sync `[DEVSYSTEM_FOLDER]` → `.windsurf/` BEFORE running `/deploy-to-all-repos`
- `Copy-Item -Recurse -Force` does NOT delete files that no longer exist at source — deletions require explicit `Remove-Item`
- Every SOP ends with a verification step before you can consider the change complete

## Table of Contents

- [Quick Reference: Sync Command](#quick-reference-sync-command)
- [SOP 1: New Skill Created](#sop-1-new-skill-created)
- [SOP 2: Skill File Added or Removed](#sop-2-skill-file-added-or-removed)
- [SOP 3: Old Skill Deleted or Deprecated](#sop-3-old-skill-deleted-or-deprecated)
- [SOP 4: DevSystem Version Changed](#sop-4-devsystem-version-changed)
- [Common Verification Commands](#common-verification-commands)

## Quick Reference: Sync Command

Sync `[DEVSYSTEM_FOLDER]` → `.windsurf/` after any edit to source. Referenced by NOTES.md "deploy" keyword.

```powershell
Copy-Item -Path "[DEVSYSTEM_FOLDER]\*" -Destination "[WORKSPACE]\.windsurf\" -Recurse -Force
```

**Note**: `Copy-Item` does NOT remove files deleted at source. For removal, see SOP 2 (file) or SOP 3 (skill).

## SOP 1: New Skill Created

**Scenario**: Adding a new skill folder (e.g., `playwriter-mcp`) to DevSystem.

### Files to modify

1. **Create skill folder**: `[DEVSYSTEM_FOLDER]/skills/<skill>/`
   - Required: `SKILL.md` (name, purpose, usage)
   - Optional: `SETUP.md`, `UNINSTALL.md`, `references/`, `assets/`, scripts

2. **Register skill** in `[WORKSPACE]/NOTES.md` `[SKILL_CATEGORIES]`:
   - Append `<skill>` to `Development` or `Personal` list (alphabetical order)

3. **Mirror registration** in `[WORKSPACE]/deploy-to-all-repos.md`:
   - Append `"<skill>"` to the matching array in `$skillCategories` hashtable (search for `"Development" = @(` or `"Personal" = @(`)

4. **If skill introduces a workflow**: also create `[DEVSYSTEM_FOLDER]/workflows/<name>.md`

5. **If skill introduces a new TOPIC**: register in `[WORKSPACE]/ID-REGISTRY.md`

6. **Sync to `.windsurf/`**:
   ```powershell
   Copy-Item -Path "[DEVSYSTEM_FOLDER]\*" -Destination "[WORKSPACE]\.windsurf\" -Recurse -Force
   ```

### Verification

```powershell
# 1. Skill folder present in both source and synced copy
Test-Path "[DEVSYSTEM_FOLDER]\skills\<skill>\SKILL.md"
Test-Path "[WORKSPACE]\.windsurf\skills\<skill>\SKILL.md"

# 2. Skill registered in both registries (should print 2 matches)
Select-String -Path "[WORKSPACE]\NOTES.md","[WORKSPACE]\deploy-to-all-repos.md" -Pattern "<skill>"

# 3. Deploy preview includes skill in Add for "All" repos and (if Development) Development repos
# Run deploy-to-all-repos in preview mode (no confirm) and check Excluded skills does NOT contain <skill>
```

## SOP 2: Skill File Added or Removed

**Scenario**: Adding new helper script / removing obsolete doc within an existing skill.

### Files to modify

**Adding a file**:
1. Create in `[DEVSYSTEM_FOLDER]/skills/<skill>/<new-file>`
2. Sync: `Copy-Item [DEVSYSTEM_FOLDER]\* .windsurf\ -Recurse -Force`
3. Deploy preview shows file in `Add` for all repos → confirm and deploy

**Removing a file**:
1. Delete from `[DEVSYSTEM_FOLDER]/skills/<skill>/<old-file>`
2. Delete from `[WORKSPACE]/.windsurf/skills/<skill>/<old-file>` (sync does NOT remove)
3. **Known gap**: current `deploy-to-all-repos.md` does not remove orphaned files from target repos unless listed in `$deprecatedFiles`. Two options:
   - **Acceptable**: leave stale file in linked repos (no harm if unreferenced)
   - **Full cleanup**: manually delete from each linked repo, or extend `$deprecatedFiles` (see SOP 3 pattern)

### Verification

**After adding a file**:

```powershell
# Presence in both locations
Test-Path "[DEVSYSTEM_FOLDER]\skills\<skill>\<file>"
Test-Path "[WORKSPACE]\.windsurf\skills\<skill>\<file>"

# Hash match
(Get-FileHash "[DEVSYSTEM_FOLDER]\skills\<skill>\<file>").Hash -eq `
(Get-FileHash "[WORKSPACE]\.windsurf\skills\<skill>\<file>").Hash
```

**After removing a file**:

```powershell
# Absence in both locations (both should return False)
Test-Path "[DEVSYSTEM_FOLDER]\skills\<skill>\<old-file>"
Test-Path "[WORKSPACE]\.windsurf\skills\<skill>\<old-file>"
```

## SOP 3: Old Skill Deleted or Deprecated

**Scenario**: Retiring a skill (e.g., `edird-phase-model` → replaced by `edird-phase-planning`).

### Files to modify

1. **Delete skill folder from source**:
   ```powershell
   Remove-Item "[DEVSYSTEM_FOLDER]\skills\<skill>" -Recurse -Force
   Remove-Item "[WORKSPACE]\.windsurf\skills\<skill>" -Recurse -Force
   ```

2. **Unregister from `NOTES.md`** `[SKILL_CATEGORIES]`: remove `<skill>` from its list

3. **Unregister from `deploy-to-all-repos.md`**: remove `"<skill>"` from `$skillCategories` hashtable

4. **Add to deprecated list** in `deploy-to-all-repos.md`:
   - Append `<skill>` to `$deprecatedSkillFolders` array (search for `$deprecatedSkillFolders = @(`)
   - This triggers deletion in linked repos on next deploy

5. **Document migration** in `deploy-to-all-repos.md` "Deprecated Files" section:
   ```markdown
   ### V3.x Migration (Deprecated Skills)
   - `skills/<skill>/` → removed (migrated to `<replacement>` or obsolete)
   ```

6. **If skill had a TOPIC**: mark deprecated in `ID-REGISTRY.md` (do NOT delete, keep history)

### Verification

```powershell
# 1. Folder gone from both source and synced copy
-not (Test-Path "[DEVSYSTEM_FOLDER]\skills\<skill>")
-not (Test-Path "[WORKSPACE]\.windsurf\skills\<skill>")

# 2. Skill NOT in active registries
Select-String -Path "[WORKSPACE]\NOTES.md" -Pattern "\b<skill>\b"  # should return nothing
# deploy-to-all-repos.md should list it ONLY in $deprecatedSkillFolders, not in $skillCategories

# 3. Deploy preview shows "Delete: skills\<skill>" for each linked repo that still has it
# After deploy: verify folder gone from every linked repo
foreach ($r in $linkedRepos) { Test-Path "$r\skills\<skill>" }  # all should be False
```

## SOP 4: DevSystem Version Changed

**Scenario**: Moving from `DevSystemV3.6` to `DevSystemV3.7`.

### Files to modify

1. **Create new version folder**:
   ```powershell
   Copy-Item -Path "[WORKSPACE]\DevSystemV3.6" -Destination "[WORKSPACE]\DevSystemV3.7" -Recurse
   ```

2. **Update `NOTES.md`**:
   - Change `Current [DEVSYSTEM]: DevSystemV3.6` → `Current [DEVSYSTEM]: DevSystemV3.7` (search for `Current \[DEVSYSTEM\]:`)
   - `Current [DEVSYSTEM_FOLDER]` line usually needs no change (uses `[DEVSYSTEM]` placeholder)

3. **Sync new version to `.windsurf/`**:
   ```powershell
   Copy-Item -Path "[WORKSPACE]\DevSystemV3.7\*" -Destination "[WORKSPACE]\.windsurf\" -Recurse -Force
   ```

4. **Document migration** in `[WORKSPACE]/deploy-to-all-repos.md`:
   - Add section `### V3.6 → V3.7 Migration` under "Deprecated Files (Allowlist)"
   - List renamed/removed files and their replacements
   - If files were deleted: add to `$deprecatedFiles` hashtable (by folder: `rules`, `workflows`)
   - If skills were removed: add to `$deprecatedSkillFolders`

5. **Update SOPs and docs with new version**:
   - `SOPS.md` example paths reference `DevSystemV3.6` in comments — update to new version
   - Any other docs with hardcoded version strings — search and update

6. **Archive old version** (optional):
   ```powershell
   # Keep for historical reference, or:
   Remove-Item "[WORKSPACE]\DevSystemV3.6" -Recurse -Force
   ```

7. **Commit before deploying**: new version is a major change, isolate in git history

8. **Deploy to linked repos** via `/deploy-to-all-repos` (always preview first)

### Verification

```powershell
# 1. NOTES.md points to new version
Select-String -Path "[WORKSPACE]\NOTES.md" -Pattern "Current \[DEVSYSTEM\]:"
# Expected: "Current [DEVSYSTEM]: DevSystemV3.7"

# 2. .windsurf matches new version (spot-check a file hash)
(Get-FileHash "[WORKSPACE]\DevSystemV3.7\skills\write-documents\WORKFLOW_RULES.md").Hash -eq `
(Get-FileHash "[WORKSPACE]\.windsurf\skills\write-documents\WORKFLOW_RULES.md").Hash

# 3. Full byte-count parity (counts should match)
(Get-ChildItem "[WORKSPACE]\DevSystemV3.7" -Recurse -File).Count
(Get-ChildItem "[WORKSPACE]\.windsurf"      -Recurse -File).Count

# 4. Deploy preview shows migration diffs only (no unexpected drift)
# Run /deploy-to-all-repos in preview, expect:
# - Old-version-specific deprecated files in Delete list
# - Renamed/new files in Add list
# - No Overwrites for files that should be unchanged
```

## Common Verification Commands

### Check for `__pycache__` pollution

```powershell
Get-ChildItem -Path "[WORKSPACE]\DevSystemV3.6","[WORKSPACE]\.windsurf" -Recurse -Directory -Filter "__pycache__"
# Expected: no output
# Cleanup: pipe to Remove-Item -Recurse -Force
```

### Check skill registration consistency

```powershell
# Extract skills from NOTES.md
$notes = (Select-String -Path "[WORKSPACE]\NOTES.md" -Pattern "^\- \*\*Development\*\*:").Line
# Extract from deploy-to-all-repos.md
$deploy = (Select-String -Path "[WORKSPACE]\deploy-to-all-repos.md" -Pattern '"Development" = @\(').Line
# Visually compare — they must list identical skills
```

### Compare source vs sync (after any change)

```powershell
# Files in DevSystem but not in .windsurf (missing sync)
$src = Get-ChildItem "[DEVSYSTEM_FOLDER]" -Recurse -File | ForEach-Object { $_.FullName.Substring("[DEVSYSTEM_FOLDER]".Length) }
$dst = Get-ChildItem "[WORKSPACE]\.windsurf" -Recurse -File | ForEach-Object { $_.FullName.Substring("[WORKSPACE]\.windsurf".Length) }
Compare-Object $src $dst | Where-Object SideIndicator -eq "<="
```

### Linked repo drift check

Run `/deploy-to-all-repos` in preview mode. Any unexpected items in `Add` / `Overwrite` / `Delete` indicate a missed sync or unregistered skill.

## Document History

**[2026-04-20 13:15]**
- Added: Quick Reference Sync Command section (fixes NOTES.md "deploy" pointer precision)
- Added: SOP acronym definition (WF-CT-02)
- Added: SOP 2 verification for removal case (check absence, not just presence)
- Added: SOP 4 step 5 for updating SOPs/docs on version change
- Changed: Approximate line numbers (“~line 78”) replaced with pattern-based search hints
- Changed: SOP 4 steps re-numbered (was 5-7, now 5-8 after insertion)

**[2026-04-20 13:06]**
- Initial creation: SOPs for 4 scenarios (new skill, file add/remove, skill delete, version change)
