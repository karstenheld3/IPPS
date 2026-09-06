# Devil's Advocate Review: WSKMGMT-SP01

**Reviewed**: 2026-09-06 14:00
**Context**: SPEC `_SPEC_SKILL_WORKFLOW-MANAGEMENT.md` (WSKMGMT-SP01) and current implementation (`sync.ps1`, skill docs, workflow updates)
**Reviewer**: /critique workflow

## MUST-NOT-FORGET (from SPEC)

1. Skill files must be generic - no project-specific data
2. Sync config is JSON-based: devsystem-sync.json at target root is single source of truth
3. Downstream modifications allowed during verify
4. Detection must be deterministic - no ambiguity between SYNCED and SELF-CONTAINED
5. SELF-CONTAINED repos must pass /verify
6. Include/exclude refiners evaluated in order: source include -> source exclude -> bundle include -> bundle exclude -> never_overwrite -> deprecated
7. `rules` folder renamed to `specs` - all references updated

## MUST-RESEARCH

1. **File sync conflict detection** - How do rsync/syncthing detect locally-modified files? Relevance: NFR-02 requires this but implementation lacks it
2. **JSON config file preservation** - How to update a single field in JSON without reformatting? Relevance: Update-LastSync reformats entire config
3. **PowerShell backup file safety** - Best practices for temp backup files in PowerShell? Relevance: .bak files could be committed accidentally
4. **Upstream sync patterns** - How do package managers handle bidirectional sync? Relevance: FR-14 specifies upstream but not implemented
5. **Glob pattern edge cases** - Common failure modes in glob matching? Relevance: Test-GlobMatch handles basic patterns but edge cases untested

## Industry Research Findings

### 1. File sync conflict detection
rsync uses `--update` flag (skip files that are newer on receiver) and `--checksum` for content comparison. Syncthing uses modification time + content hash. Both detect "locally modified" by comparing target modification time against last sync timestamp. The implementation in sync.ps1 compares content hashes only (SHA-256) but does NOT check modification time against last_sync. This means a file modified locally and at source with different content will be silently overwritten without warning, violating NFR-02.

### 2. JSON config preservation
PowerShell `ConvertFrom-Json` / `ConvertTo-Json` round-trip reorders keys and changes formatting. `Json.NET` (via `Newtonsoft.Json`) preserves formatting with `JsonLoadSettings`. For PowerShell-native solutions, raw string replacement of the `last_sync` field is safer than full deserialization/reserialization. The current `Update-LastSync` function causes unnecessary git diff noise.

### 3. PowerShell backup file safety
Best practice: use `.tmp_` prefix (gitignored by convention) and place in same directory for atomic rename. The implementation uses `.bak` suffix which is not gitignored. If process is killed between copy and cleanup, `.bak` files persist and may be accidentally committed.

### 4. Upstream sync patterns
Package managers (npm, pip) are strictly downstream. Bidirectional sync tools (syncthing, unison) treat both sides as equal peers. The SPEC's upstream concept (target -> source push) is unusual - it's more like a git push than a sync. The implementation correctly omits upstream from sync.ps1 (it's a workflow concern: swap source/target parameters), but the SPEC still lists it as a script feature in FR-14.

### 5. Glob pattern edge cases
Common failures: `**` not matching zero directories, trailing slashes, empty pattern matching everything, case sensitivity on Linux. The implementation's `Test-GlobMatch` converts to regex but doesn't handle `**` (double-star) - it treats `*` as `[^\\]*` which only matches within one path segment. This is correct for the SPEC's usage but should be documented.

---

## Critical Issues

### CRIT-01: FR-14 is stale - specifies `.sync-timestamp` file and locally-modified warning, contradicts FR-44/FR-46

**Severity**: CRITICAL
**Type**: SPEC contradiction + implementation gap
**Location**: SPEC FR-14 (line 350-351), SPEC NFR-02 (line 670), `sync.ps1`

FR-14 states:
- "Before overwriting a file not in the preserve list, check if target file was modified after last sync timestamp. If so, warn user and offer to add to preserve list or proceed with overwrite"
- "Store last sync timestamp in target folder root (`.sync-timestamp`, gitignored). Missing timestamp triggers full comparison"

FR-44/FR-46 superseded this with `last_sync` field in `devsystem-sync.json`. But FR-14 was never updated. The implementation follows FR-44/46 (writes `last_sync` to JSON), but does NOT implement the locally-modified warning from FR-14/NFR-02.

NFR-02 states: "Diff preview must mark files modified locally since last sync as 'locally modified - will be overwritten'"

**Impact**: A user edits a file locally (e.g., customizes a spec), then runs sync. The sync overwrites the local modification without warning because the script only compares content hashes, not modification times. Data loss is silent.

**Recommendation**:
1. Update FR-14: remove `.sync-timestamp` reference, keep locally-modified warning as a requirement on the diff mode (check target file modification time against `last_sync` in devsystem-sync.json)
2. Implement locally-modified detection in `Compare-Files`: if target file LastWriteTime > config last_sync AND content differs, mark as `LOCALLY_MODIFIED` instead of `MODIFY`
3. Update NFR-02: change "will be overwritten" to "will be overwritten (locally modified since last sync)"

### CRIT-02: Upstream sync direction specified in FR-14 but not implemented in sync.ps1

**Severity**: HIGH
**Type**: Implementation gap
**Location**: SPEC FR-14 (line 346), SPEC Section 9 Action Flow (lines 897-914), `sync.ps1`

FR-14 states: "Supports downstream (source to target) and upstream (target to source) directions"

Section 9 shows upstream sync flows: "Diff [AGENT_FOLDER] against [DEVSYSTEM_FOLDER]", "Diff [KNOWLEDGE_FOLDER] against [KNOWLEDGE_SOURCE_FOLDER]", "Diff [SPECS_FOLDER] against [SPECS_SOURCE_FOLDER]"

`sync.ps1` has no `-direction` parameter and always syncs source -> target. Upstream sync would require swapping source and target parameters.

**Impact**: `/sync workspace upstream` cannot be executed with sync.ps1 as-is. The workflow would need to manually swap parameters, but the script's config reading logic assumes config is at target, not source.

**Recommendation**: Either:
1. Remove upstream from FR-14 and Section 9 (upstream is a workflow-level concern: swap -sources and -targets parameters), OR
2. Add `-direction` parameter to sync.ps1 that swaps source/target internally and reads config from the appropriate side

Option 1 is simpler and aligns with DD-18 (target owns config). Upstream sync = run sync.ps1 with swapped parameters from the other repo's perspective.

---

## High Priority

### CRIT-03: SPEC MNF line 38 says "Register in [SKILL_CATEGORIES]" but FR-48 says [SKILL_CATEGORIES] is obsolete

**Severity**: HIGH
**Type**: SPEC internal contradiction
**Location**: SPEC MNF line 38, SPEC FR-48 line 613

MNF: "Register `workspace-management` in `NOTES.md` `[SKILL_CATEGORIES]`"
FR-48: "Existing [SKILL_CATEGORIES] and [LINKED_REPOS] in NOTES.md become obsolete and are removed"

WORKSPACE-RULES.md still has WS-ST-02 and WS-ST-03 enforcing [SKILL_CATEGORIES] registration. If [SKILL_CATEGORIES] is obsolete, these rules are dead code.

**Impact**: Agents following the MNF will try to register skills in an obsolete section. Agents following FR-48 will remove [SKILL_CATEGORIES], then fail WS-ST-02/03 verification.

**Recommendation**: Decide: either keep [SKILL_CATEGORIES] (remove FR-48's "obsolete" clause) or remove it (delete WS-ST-02/03, update MNF, update SKILL.md). Given that the skill registration concept is still useful for integrity checks, recommend keeping [SKILL_CATEGORIES] but removing [LINKED_REPOS] only.

### CRIT-04: Section 9 Action Flow doesn't match Section 8 Key Mechanisms

**Severity**: HIGH
**Type**: SPEC internal contradiction
**Location**: SPEC Section 8 (lines 803-820), SPEC Section 9 (lines 872-895)

Section 8 (Key Mechanisms) shows: "For each source in config: Run sync.ps1 -diff -sources <source> -targets <target> -configs devsystem-sync.json"

Section 9 (Action Flow) shows three separate operations: "For Prompt System: Diff [DEVSYSTEM_FOLDER] against [AGENT_FOLDER]", "For Knowledge: Diff [KNOWLEDGE_SOURCE_FOLDER] against [KNOWLEDGE_FOLDER]", "For Specs: Diff [SPECS_SOURCE_FOLDER] against [SPECS_FOLDER]"

Section 9 implies 3 separate diff operations with different source/target pairs. Section 8 implies a single sync.ps1 call that iterates sources from config. The implementation follows Section 8.

**Impact**: An implementer reading Section 9 would build 3 separate sync calls. An implementer reading Section 8 would build a single call with multi-source config. The resulting architectures are different.

**Recommendation**: Update Section 9 to match Section 8: "For each source in devsystem-sync.json: Run sync.ps1 -diff with source path and target path from config"

---

## Medium Priority

### CRIT-05: Test-SyncConfig doesn't validate array types for include/exclude/deprecated/never_overwrite

**Severity**: MEDIUM
**Type**: Logic flaw / input validation gap
**Location**: `sync.ps1` `Test-SyncConfig` (lines 63-87)

`Test-SyncConfig` checks for existence of fields but doesn't validate that `include`, `exclude`, `deprecated`, `never_overwrite` are arrays. If a user provides a string instead of an array (e.g., `"include": "*.md"` instead of `"include": ["*.md"]`), `Test-GlobMatch` would iterate over characters of the string instead of patterns, causing silent misbehavior.

**Impact**: Invalid config causes silent file filtering failures. Files that should be included are excluded and vice versa.

**Recommendation**: Add type validation in `Test-SyncConfig`:
```powershell
foreach ($field in @('include', 'exclude', 'deprecated', 'never_overwrite')) {
    $val = $source.$field
    if ($val -isnot [array]) {
        Write-Error "Source entry '$($source.source)' field '$field' must be an array, got $($val.GetType().Name)"
        return $false
    }
}
```

### CRIT-06: Update-LastSync reformats JSON config file

**Severity**: MEDIUM
**Type**: Logic flaw / data integrity
**Location**: `sync.ps1` `Update-LastSync` (lines 575-581)

`Update-LastSync` does `ConvertFrom-Json` -> modify -> `ConvertTo-Json`. PowerShell's `ConvertTo-Json` reorders keys alphabetically and changes formatting (indentation, spacing). This causes unnecessary git diff noise every time sync is executed, even if only `last_sync` changed.

**Impact**: Every sync execution creates a large git diff in `devsystem-sync.json` even though only the timestamp changed. This makes git history noisy and hard to review.

**Recommendation**: Use raw string replacement instead of full deserialization:
```powershell
function Update-LastSync {
    param([string]$ConfigPath, [string]$Timestamp)
    $content = Get-Content -Path $ConfigPath -Raw -Encoding UTF8
    $pattern = '"last_sync"\s*:\s*"[^"]*"'
    $replacement = "`"last_sync`": `"$Timestamp`""
    $newContent = [regex]::Replace($content, $pattern, $replacement)
    if ($newContent -eq $content) {
        # last_sync field doesn't exist yet, add it before closing brace
        $newContent = $content.TrimEnd().TrimEnd('}') + ",`n  `"last_sync`": `"$Timestamp`"`n}`n"
    }
    Set-Content -Path $ConfigPath -Value $newContent -Encoding UTF8 -NoNewline
}
```

### CRIT-07: SKILL.md MNF item 2 says "Sync before deploy" but deploy is obsolete

**Severity**: MEDIUM
**Type**: Implementation drift
**Location**: `SKILL.md` line 23

MNF item 2: "Sync before deploy - always run diff and review changes before executing sync"

"Deploy" is obsolete terminology - `deploy-to-all-repos.md` was deleted and replaced by sync. The MNF should say "Always run -diff before -execute" or similar.

**Impact**: Agents reading "sync before deploy" may search for a deploy workflow that doesn't exist.

**Recommendation**: Update to "Always run sync.ps1 -diff before -execute - review changes before applying"

### CRIT-08: SKILL.md MNF item 3 says "preserve list" but implementation uses "never_overwrite"

**Severity**: MEDIUM
**Type**: Terminology inconsistency
**Location**: `SKILL.md` line 24

MNF item 3: "Check preserve list before overwriting - files in preserve list are never overwritten during sync"

The implementation and SPEC use `never_overwrite`, not "preserve list". This is stale terminology from the old FR-14 which mentioned "preserve list".

**Impact**: Agents searching for "preserve list" in code/config won't find anything. Terminology mismatch causes confusion.

**Recommendation**: Update to "Check never_overwrite patterns before overwriting - files matching never_overwrite are never overwritten or deleted during sync"

---

## Low Priority

### CRIT-09: DD-12 still says "rules" instead of "specs"

**Severity**: LOW
**Type**: SPEC drift
**Location**: SPEC DD-12 (line 731)

DD-12: "If a repo syncs knowledge but not rules, it still has sync markers and is SYNCED."

Should say "specs" not "rules" per FR-50.

### CRIT-10: SPEC line 58 says "pending /rename execution" but rename is done

**Severity**: LOW
**Type**: SPEC drift
**Location**: SPEC MNF line 58

"`rules` folder renamed to `specs` with subfolders `sops/` and `guides/` - pending /rename execution"

The rename has been executed. "pending /rename execution" should be removed.

### CRIT-11: SPEC target files still list deleted files

**Severity**: LOW
**Type**: SPEC drift
**Location**: SPEC lines 16-17

Lines 16-17 list `workspace_diff_template.ps1` and `workspace_sync_template.ps1` as "(replaced by sync.ps1)". These files have been deleted. The SPEC should remove them from the target files list or mark as "deleted, replaced by sync.ps1".

### CRIT-12: .bak backup files not gitignored

**Severity**: LOW
**Type**: Risk
**Location**: `sync.ps1` line 493

Backup files use `.bak` extension (e.g., `file.md.bak`). If the process is killed between copy and cleanup, `.bak` files persist. The `*_gitignore` convention or `.tmp_` prefix would be safer.

**Recommendation**: Either use `.tmp_` prefix for backups (already gitignored by convention) or add `*.bak` to `.gitignore`.

### CRIT-13: Source path filtering uses -ieq always (case-insensitive on all platforms)

**Severity**: LOW
**Type**: Platform compatibility
**Location**: `sync.ps1` line 659

`$sourcePath -ieq $filterFull` uses case-insensitive comparison. On Linux, `/path/Source` and `/path/source` are different paths. Should use `-eq` (case-sensitive) on Linux, `-ieq` on Windows.

**Recommendation**: Use `$PSVersionTable.Platform` to determine case sensitivity, or use `[System.IO.Path]::Equals()` which is platform-aware.

### CRIT-14: SPEC example in Section 13 shows "OK. 1 source, 1 bundle selected." but implementation only outputs "OK."

**Severity**: LOW
**Type**: SPEC vs implementation mismatch
**Location**: SPEC line 1135, `sync.ps1` line 366

SPEC logging example: "OK. 1 source, 1 bundle selected."
Implementation: "OK."

The implementation doesn't have access to source/bundle counts at this point in the code (it's inside a per-source-entry function). The SPEC example is aspirational but the implementation can't easily provide this info without restructuring.

**Recommendation**: Either update the SPEC example to match implementation ("OK.") or restructure the code to pass source/bundle counts into the report function.

### CRIT-15: Target file enumeration for deprecated check is O(n*m) per source entry

**Severity**: LOW
**Type**: Performance
**Location**: `sync.ps1` `Compare-Files` lines 271-304

For each source entry, `Compare-Files` enumerates ALL target files and checks each against deprecated patterns. With 3 source entries, 500 target files, and 5 deprecated patterns, this is 7500 comparisons. Not a problem for small workspaces but could exceed NFR-01's 10-second limit for large workspaces.

**Recommendation**: Cache the target file list across source entries, or pre-compute deprecated matches once.

---

## Questions That Need Answers

1. **Is upstream sync actually needed?** The SPEC specifies it (FR-14, Section 9) but the implementation doesn't support it. If upstream sync is handled by the workflow (swapping parameters), should FR-14 be updated to remove the direction requirement?

2. **Should [SKILL_CATEGORIES] be kept or removed?** FR-48 says obsolete, but WS-ST-02/03 rules still enforce it. What is the intended end state?

3. **Is the locally-modified warning (NFR-02) a must-have or nice-to-have?** Implementing it requires checking file modification times against `last_sync`, which adds complexity. If it's a must-have, it's a critical implementation gap.

4. **Should sync.ps1 enforce diff-before-execute?** Currently, running `-execute` without first running `-diff` will apply changes without preview. Should the script refuse to execute without a prior diff, or is this the workflow's responsibility?

5. **What happens if devsystem-sync.json has zero sources?** The script would produce an empty report and exit 0. Is this correct behavior for a misconfigured repo, or should it be an error (exit 2)?

---

## Summary

| Severity | Count | Categories |
|---|---|---|
| CRITICAL | 1 | SPEC contradiction + implementation gap (FR-14/NFR-02) |
| HIGH | 3 | Upstream gap, SPEC contradiction (MNF vs FR-48), Section 8 vs 9 |
| MEDIUM | 4 | Config validation, JSON reformatting, SKILL.md terminology |
| LOW | 7 | SPEC drift, backup safety, platform compat, performance |
| Questions | 5 | Need user decisions |

**Top 3 actions recommended:**
1. Fix FR-14: remove `.sync-timestamp`, keep locally-modified warning, implement in sync.ps1
2. Resolve [SKILL_CATEGORIES] contradiction: keep or remove, update all references
3. Align Section 9 Action Flow with Section 8 Key Mechanisms (single sync.ps1 call, not 3 separate)
