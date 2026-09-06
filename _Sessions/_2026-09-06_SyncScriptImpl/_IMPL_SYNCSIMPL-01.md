# IMPL: sync.ps1 — Single Generic DevSystem Sync Script

**Doc ID**: SYNCSIMPL-IP01
**Goal**: Implement `sync.ps1` with `-diff` and `-execute` modes, reading all config from target's `devsystem-sync.json`
**Target file**: `DevSystemV4.3/skills/workspace-management/sync.ps1`

**Depends on:**
- `_SPEC_SKILL_WORKFLOW-MANAGEMENT.md [WSKMGMT-SP01]` for FR-44 through FR-54 (sync architecture)
- `devsystem-sync.json` data structure defined in WSKMGMT-SP01 section 10

**Does not depend on:**
- Any project-specific deployment script
- `deploy-to-all-repos.md` (legacy, deleted)

## MUST-NOT-FORGET

- Script must be generic — no hardcoded paths, no project-specific data
- All config read from target's `devsystem-sync.json` — nothing read from source
- Source is purely a content provider (read-only during sync)
- All parameters accept JSON arrays OR single strings
- `-diff` must never modify anything — preview only
- `never_overwrite` files are protected from both overwrite AND deletion
- `deprecated` files are deleted only in `-execute` mode
- Command-line parameter paths (`-sources`, `-targets`, `-configs`) resolved against current working directory
- `source` field inside `devsystem-sync.json` resolved relative to config file's directory (target root)
- Script must handle Unicode filenames and paths with spaces
- Privacy gate: no real identifiers in script or embedded examples
- `last_sync` timestamp written only in `-execute` mode, only on success
- Exit codes must be deterministic for CI/automation use

## 1. Script Interface

### 1.1 Parameters

- **`-diff`** — switch, one of `-diff`/`-execute` required. Preview mode: show changes, modify nothing
- **`-execute`** — switch, one of `-diff`/`-execute` required. Apply mode: copy, delete, update timestamp
- **`-sources`** — string (JSON array or single), required. Source repo paths to filter on (relative or absolute). Filters which source entries in config to sync
- **`-targets`** — string (JSON array or single), required. Target repo paths (relative or absolute)
- **`-configs`** — string (JSON array or single), required. Paths to `devsystem-sync.json` files, paired 1:1 with targets
- **`-output-file`** — string, optional, default: console. File path for full diff report
- **`-verbose`** — switch, optional, default: false. Show excluded files and skip reasons in output

### 1.2 Parameter Parsing

**SYNCSIMPL-IP01-IS-01: Array-or-string coercion**

All array parameters (`-sources`, `-targets`, `-configs`) accept:
- Single string: `-sources "../IPPS/DevSystemV4.3"` → treated as `["../IPPS/DevSystemV4.3"]`
- JSON array string: `-sources '["../IPPS/DevSystemV4.3", "../Company/knowledge"]'` → parsed as array
- Absolute paths: accepted, used as-is
- Relative paths: resolved against the current working directory

```powershell
function Resolve-PathParam {
    param([string]$Value, [string]$ParamName)
    if ([string]::IsNullOrWhiteSpace($Value)) {
        Write-Error "Parameter -$ParamName is required"
        exit 2
    }
    $trimmed = $Value.Trim()
    if ($trimmed.StartsWith('[') -and $trimmed.EndsWith(']')) {
        try {
            $array = $trimmed | ConvertFrom-Json
            return @($array | ForEach-Object { [System.IO.Path]::GetFullPath($_) })
        } catch {
            Write-Error "Parameter -$ParamName contains invalid JSON: $trimmed"
            exit 2
        }
    }
    return @([System.IO.Path]::GetFullPath($trimmed))
}
```

**SYNCSIMPL-IP01-IS-02: Mode validation**

- Exactly one of `-diff` or `-execute` must be specified
- Both specified → error, exit 2
- Neither specified → error, exit 2

### 1.3 Exit Codes

- **0** — Success: diff completed (may have 0 changes), or execute completed successfully
- **1** — Success with changes: diff found changes, or execute applied changes
- **2** — Error: invalid parameters, missing config, invalid JSON
- **3** — Error: source path not found or inaccessible
- **4** — Error: target path not found or inaccessible
- **5** — Error: file system error during execute (copy/delete failed)

### 1.4 Output Streams

- **stdout**: Diff report (add/modify/delete/skip) or execute summary (X added, Y modified, Z deleted)
- **stderr**: Errors, warnings, verbose diagnostic messages
- `-output-file` present: full report to file, stdout shows summary only
- `-output-file` absent: full report to stdout

## 2. Config Reading

**SYNCSIMPL-IP01-IS-03: Read devsystem-sync.json**

For each config file in `-configs`:
1. Read file from the resolved path
2. Parse JSON
3. Validate structure (see IS-04)
4. For each source entry in `sources` array:
   - Resolve `source` path relative to config file's directory
   - Load bundle definitions from `bundles` object
   - Load `selected_bundles` array
   - Load `include`, `exclude`, `deprecated`, `never_overwrite` arrays

**SYNCSIMPL-IP01-IS-04: Config validation**

```powershell
function Test-SyncConfig {
    param([object]$Config, [string]$ConfigPath)
    $errors = @()
    if (-not $Config.sources) {
        $errors += "Missing 'sources' array in $ConfigPath"
    }
    foreach ($src in $Config.sources) {
        if (-not $src.source) { $errors += "Source entry missing 'source' field in $ConfigPath" }
        if (-not $src.selected_bundles) { $errors += "Source '$($src.source)' missing 'selected_bundles' array" }
        if (-not $src.bundles) { $errors += "Source '$($src.source)' missing 'bundles' definitions" }
        if (-not $src.include) { $errors += "Source '$($src.source)' missing 'include' array" }
        if (-not $src.exclude) { $errors += "Source '$($src.source)' missing 'exclude' array" }
        if (-not $src.deprecated) { $errors += "Source '$($src.source)' missing 'deprecated' array" }
        if (-not $src.never_overwrite) { $errors += "Source '$($src.source)' missing 'never_overwrite' array" }
        foreach ($bundleName in $src.selected_bundles) {
            if (-not $src.bundles.$bundleName) {
                $errors += "Source '$($src.source)' selects bundle '$bundleName' but bundle not defined in 'bundles'"
            }
        }
    }
    if ($errors.Count -gt 0) {
        foreach ($e in $errors) { Write-Error $e }
        exit 2
    }
}
```

## 3. File Discovery and Filtering

**SYNCSIMPL-IP01-IS-05: Source file discovery**

1. Enumerate all files in source path recursively (excluding directories)
2. Compute relative path from source root for each file (using forward slashes for glob matching)
3. Apply filters in evaluation order:

```
Step 1: source include
  → Keep files matching any pattern in source entry's `include` array
  → If include is ["*"], keep everything

Step 2: source exclude
  → Remove files matching any pattern in source entry's `exclude` array

Step 3: bundle include (union of all selected bundles)
  → For each bundle in selected_bundles, keep files matching that bundle's `include` patterns
  → Union: file passes if it matches ANY selected bundle's include

Step 4: bundle exclude (union of all selected bundles)
  → For each bundle in selected_bundles, remove files matching that bundle's `exclude` patterns
  → Union: file is removed if it matches ANY selected bundle's exclude

Step 5: target never_overwrite
  → Mark files matching never_overwrite patterns as "skip" (not overwrite, not delete)
  → These files are excluded from both add and modify operations

Step 6: deprecated
  → Mark files matching deprecated patterns for deletion at target
  → Only checked against target (not source)
```

**SYNCSIMPL-IP01-IS-06: Glob pattern matching**

Use PowerShell wildcard matching with `WildcardPattern` class:
- `*` matches any sequence (including path separators)
- `?` matches single character
- Patterns match against forward-slash relative paths (e.g., `skills/coding-conventions/SKILL.md`)
- Case-insensitive on Windows, case-sensitive on Linux (platform-detected at runtime)

```powershell
function Test-GlobMatch {
    param([string]$Path, [string[]]$Patterns)
    $options = if ($IsLinux -or $IsMacOS) {
        [System.Management.Automation.WildcardOptions]::None
    } else {
        [System.Management.Automation.WildcardOptions]::IgnoreCase
    }
    foreach ($pattern in $Patterns) {
        $wildcard = [System.Management.Automation.WildcardPattern]::new(
            $pattern,
            $options
        )
        if ($wildcard.IsMatch($path)) { return $true }
    }
    return $false
}
```

**SYNCSIMPL-IP01-IS-07: File content comparison**

Use SHA-256 hash comparison for file equality:
- Source file hash computed from file content
- Target file hash computed from file content (if target file exists)
- If hashes differ → file is "modified"
- If target file doesn't exist → file is "new"
- If source file doesn't exist but target does and file is in deprecated → "delete"
- If source file doesn't exist but target does and file is NOT in deprecated → "unchanged" (not managed by sync)

```powershell
function Get-FileHash256 {
    param([string]$Path)
    if (-not (Test-Path $Path -PathType Leaf)) { return $null }
    return (Get-FileHash -Path $Path -Algorithm SHA256).Hash
}
```

## 4. Diff Mode

**SYNCSIMPL-IP01-IS-08: Diff report generation**

For each source-target-config triplet:
1. Discover and filter source files (IS-05)
2. For each filtered source file:
   - Compute relative path
   - Check if target file exists
   - If not exists -> classify as ADD
   - If exists, compare hashes -> MODIFY if different, UNCHANGED if same
   - Check never_overwrite -> reclassify as SKIP with reason 'never_overwrite'
3. For each deprecated pattern:
   - Check if matching file exists at target
   - If yes -> classify as DELETE
   - Check never_overwrite -> reclassify as SKIP with reason 'never_overwrite protects deletion'
4. Collect all results into report (format in IS-20)

**SYNCSIMPL-IP01-IS-10: Output file handling**

- `-output-file` present:
  - Full report in IS-20 format (with 100-char headers, timestamps, progress indicators) -> file
  - stdout: `Summary: 3 add, 2 modify, 1 delete, 1 skip, 45 unchanged.`
  - Exit code: 0 if no changes, 1 if changes found
- `-output-file` absent:
  - Full report in IS-20 format -> stdout
  - Exit code: 0 if no changes, 1 if changes found

## 5. Execute Mode

**SYNCSIMPL-IP01-IS-11: Execute operations**

For each ADD:
1. Create target directory structure if needed
2. Copy source file to target
3. Log: `  [ x / n ] Copying 'skills/new-skill/SKILL.md'...` then `    OK.`

For each MODIFY:
1. Create backup: `<target>.bak` (only if file differs)
2. Copy source file to target (overwrite)
3. Log: `  [ x / n ] Updating 'skills/coding-conventions/SKILL.md'...` then `    OK.`
4. Delete backup file after successful copy
5. If copy fails, restore from backup before reporting error

For each DELETE (deprecated):
1. Check never_overwrite — if matches, skip
2. Delete target file
3. Log: `  [ x / n ] Deleting 'specs/commit-rules.md'...` then `    OK.`

For each SKIP:
- Log: `  SKIP: 'specs/sops/project-release.md' -> never_overwrite.`
- No action

Full execute output format in IS-21.

**SYNCSIMPL-IP01-IS-12: last_sync timestamp update**

After all operations complete successfully:
1. Read `devsystem-sync.json`
2. Update `last_sync` field with current UTC timestamp in ISO 8601 format: `2026-09-06T13:35:00Z`
3. Write back to file
4. Log: `  Updating 'last_sync' timestamp...` then `    OK. last_sync='2026-09-06T13:35:00Z'.`

If any operation fails:
- Do NOT update `last_sync`
- Report partial success
- Exit with code 5

**SYNCSIMPL-IP01-IS-13: Execute summary**

Superseded by IS-21 (execute summary format with full LOG-UF compliance). Execute output uses the IS-21 format with 100-char headers, timestamps, progress indicators, and RESULT keyword.

## 6. Multi-Source/Target/Config Handling

**SYNCSIMPL-IP01-IS-14: Target-config pairing and source filtering**

Targets and configs are paired 1:1 by index: `targets[0]` uses `configs[0]`.
If only one config provided, it applies to all targets.

The `-sources` parameter acts as a **filter** on which source entries in the config to sync.
If `-sources` is provided, only source entries in the config whose `source` path matches one of the `-sources` values are processed.
If `-sources` is `*` or not filtering, all source entries in the config are processed.

Flow:
```
For each target[i]:
  ├─> Read config[i] (or config[0] if single config)
  ├─> For each source entry in config.sources:
  │   ├─> Resolve source path relative to config file's directory
  │   ├─> If -sources provided and source path not in -sources list → skip
  │   ├─> Discover and filter source files
  │   ├─> Compare against target
  │   └─> Diff or execute
  └─> Update last_sync in config[i] (execute mode only)
```

Example:
```powershell
sync.ps1 -diff -sources '../IPPS/DevSystemV4.3' -targets '.' -configs 'devsystem-sync.json'
```
→ Read devsystem-sync.json from current dir, find source entry matching `../IPPS/DevSystemV4.3`, sync that source to current dir.

Example multi-target:
```powershell
sync.ps1 -diff -targets '["../Lana-V2-Dev", "../USTVA"]' -configs '["devsystem-sync.json", "devsystem-sync.json"]'
```
→ Read each target's devsystem-sync.json, sync all sources in each config to that target.

**SYNCSIMPL-IP01-IS-15: Config-to-target relationship**

- Config file path from `-configs` parameter is resolved against current working directory (IS-01)
- `source` field inside config is resolved relative to config file's directory (IS-03)
- Each target has its own `devsystem-sync.json` at its root with its own sources and bundles
- Script reads config for each target, filters sources by `-sources` parameter, syncs matching sources

## 7. Error Handling

**SYNCSIMPL-IP01-IS-16: Error scenarios**

- **Missing required parameter** — exit 2: `Parameter -sources is required`. Abort before any file operations
- **Invalid JSON in parameter** — exit 2: `Parameter -sources contains invalid JSON`. Abort
- **Both -diff and -execute** — exit 2: `Cannot specify both -diff and -execute`. Abort
- **Neither -diff nor -execute** — exit 2: `Must specify either -diff or -execute`. Abort
- **Config file not found** — exit 2: `Config file not found: <path>`. Abort
- **Invalid config JSON** — exit 2: `Invalid JSON in config: <path>`. Abort
- **Config validation failed** — exit 2: `Source entry missing 'source' field`. Abort
- **Source path not found** — exit 3: `Source path not found: <path>`. Abort
- **Target path not found** — exit 4: `Target path not found: <path>`. Abort
- **Copy failed (disk full, permissions)** — exit 5: `Failed to copy <file>: <error>`. Continue with remaining, report partial
- **Delete failed (permissions, locked)** — exit 5: `Failed to delete <file>: <error>`. Continue with remaining, report partial
- **Config write failed (last_sync)** — exit 5: `Failed to update last_sync: <error>`. Report, exit 5

**SYNCSIMPL-IP01-IS-17: Continue-on-error policy**

- Parameter/config errors: abort immediately, no operations performed
- File operation errors: log error, continue with remaining files, report partial success at end
- `last_sync` only updated if all file operations succeeded (or no operations were needed)

## 8. Edge Cases

**SYNCSIMPL-IP01-EC-01: Empty source directory**
- Source path exists but contains no files matching include patterns
- Diff: report 0 ADD, 0 MODIFY, check deprecated at target
- Execute: no copies, only deprecated deletions and timestamp update

**SYNCSIMPL-IP01-EC-02: Empty target directory**
- Target path exists but is empty (fresh repo)
- All source files classified as ADD
- No MODIFY, no DELETE

**SYNCSIMPL-IP01-EC-03: Source and target are the same path**
- Allowed but produces 0 changes (all files UNCHANGED)
- Deprecated files would be deleted from source — warn user before execute
- Log: `[WARNING] Source and target are the same path: <path>`

**SYNCSIMPL-IP01-EC-04: Config file at target root but source path in config is absolute**
- Accept absolute paths in config `source` field
- Log: `[WARNING] Source path in config is absolute: <path>. Consider using relative paths for portability.`
- Continue with sync

**SYNCSIMPL-IP01-EC-05: Bundle selected but not defined in bundles object**
- Config validation (IS-04) catches this and exits with code 2

**SYNCSIMPL-IP01-EC-06: File exists at target but not in source and not in deprecated**
- File is unmanaged (not part of sync)
- Diff: not reported (not in source, not deprecated)
- Execute: not deleted (only deprecated files are deleted)
- This preserves downstream customizations

**SYNCSIMPL-IP01-EC-07: never_overwrite file exists at target with different content than source**
- Diff: classified as SKIP with reason "never_overwrite"
- Execute: not overwritten, logged as SKIP
- Source content is NOT copied

**SYNCSIMPL-IP01-EC-08: Deprecated file also matches never_overwrite**
- never_overwrite takes precedence over deprecated
- File is NOT deleted
- Diff: classified as SKIP with reason "never_overwrite protects deletion"
- Execute: logged as SKIP

**SYNCSIMPL-IP01-EC-09: Unicode filenames**
- Use `[System.IO.Directory]::EnumerateFiles()` with `System.IO.SearchOption::AllDirectories` for Unicode-safe enumeration
- Do not use `Get-ChildItem` with `-Recurse` (has known Unicode issues on older PowerShell)

**SYNCSIMPL-IP01-EC-10: Paths with spaces**
- All file operations use quoted paths or `[System.IO.Path]` methods
- No shell expansion or string splitting on spaces

## 9. Logging

sync.ps1 has two logging types per SPEC section 13: User-Facing (UF) and Script-Level (SC). Output must comply with `LOGGING-RULES.md`, `LOGGING-RULES-USER-FACING.md`, and `LOGGING-RULES-SCRIPT-LEVEL.md`.

**SYNCSIMPL-IP01-IS-18: User-Facing output (stdout)**

Applies to: diff preview, execute summary, progress during long operations.

- **100-char START/END headers/footers** required (LOG-UF-06):
  `=============================== START: WORKSPACE SYNC ===============================`
  `================================ END: WORKSPACE SYNC =================================`
- **Timestamps** in `[YYYY-MM-DD HH:MM:SS]` format at header and footer (LOG-UF-01)
- **Duration** in footer: `(2.0 secs)` or `(1 min 30 secs)` (LOG-GN-04)
- **Progress indicators** `[ x / n ]` at line start for file iteration (LOG-UF-02)
- **Announce > Track > Report** pattern (LOG-GN philosophy):
  - Announce: `Comparing files...`
  - Track: `  [ 1 / 3 ] Adding 'skills/new-skill/SKILL.md'...`
  - Report: `  3 new files found.`
- **Status keywords** (LOG-UF-03, LOG-GN philosophy):
  - `OK.` or `OK: <details>` for success
  - `SKIP: <why>` for skipped items
  - `ERROR: <what> -> <system error>` for item-level errors
  - `FAIL: <summary>` for activity-level failure
  - `PARTIAL FAIL: <summary>` for partial success
  - `WARNING: <non-breaking problem>`
- **MUST NOT use `INFO`, `DEBUG`, `WARN` prefixes** (LOG-UF rules)
- **Quote paths and names** with single quotes (LOG-GN-02)
- **Ellipsis** on ongoing actions, period on results (LOG-GN-10, LOG-GN-11)
- **Numbers first** in result messages (LOG-GN-03)
- **RESULT:** keyword on final line before footer (LOG-SC-07)

**SYNCSIMPL-IP01-IS-19: Script-Level output (stderr, for debugging)**

Applies to: diagnostic messages, hash comparisons, glob match details, config parsing traces.

- **No timestamps** (LOG-SC-01) — deterministic output for diff comparison
- **Comparison markers** (LOG-SC-04): `[equal]`, `[different]`
- **Status markers** (LOG-SC-04): `[ok]`, `[fail]`
- **Self-contained detail** (LOG-SC-06): include file paths, expected/actual values, line numbers
- **Summary with counts** (LOG-SC-07): `OK: X, SKIP: Y, FAIL: Z`
- **`-verbose` flag** enables Script-Level output on stderr; without it, only User-Facing output on stdout

**SYNCSIMPL-IP01-IS-20: Diff report format (User-Facing, stdout or -output-file)**

```
=============================== START: WORKSPACE SYNC PREVIEW ===============================
[2026-09-06 13:35:00]

Syncing from '../IPPS/DevSystemV4.3' to '.'...
  Reading 'devsystem-sync.json'...
    OK. 1 source, 1 bundle selected.
  Comparing files...
    [ 1 / 3 ] Adding 'skills/new-skill/SKILL.md'...
    [ 2 / 3 ] Adding 'workflows/new-workflow.md'...
    [ 3 / 3 ] Adding 'specs/new-spec.md'...
    3 new files found.
  Comparing modified files...
    [ 1 / 2 ] 'skills/coding-conventions/SKILL.md' differs...
    [ 2 / 2 ] 'workflows/sync.md' differs...
    2 modified files found.
  Checking deprecated files...
    [ 1 / 1 ] 'specs/commit-rules.md' marked for deletion...
    1 deprecated file found.
  Checking never-overwrite files...
    1 file protected: 'specs/sops/project-release.md'.

Summary: 3 add, 2 modify, 1 delete, 1 skip, 45 unchanged.
RESULT: CHANGES FOUND
================================ END: WORKSPACE SYNC PREVIEW =================================
[2026-09-06 13:35:02] (2.0 secs)
```

With `-verbose`, Script-Level output on stderr:
```
EXCLUDED (12):
  [ 1 / 12 ] 'skills/google-account/SKILL.md' excluded -> bundle exclude: Development
  [ 2 / 12 ] 'skills/travel-info/SKILL.md' excluded -> bundle exclude: Development
  [ 3 / 12 ] '__pycache__/cache.py' excluded -> source exclude
  ...
  12 files excluded.
```

**SYNCSIMPL-IP01-IS-21: Execute summary format (User-Facing, stdout)**

```
=============================== START: WORKSPACE SYNC EXECUTE ===============================
[2026-09-06 13:35:00]

Syncing from '../IPPS/DevSystemV4.3' to '.'...
  Adding files...
    [ 1 / 3 ] Copying 'skills/new-skill/SKILL.md'...
      OK.
    [ 2 / 3 ] Copying 'workflows/new-workflow.md'...
      OK.
    [ 3 / 3 ] Copying 'specs/new-spec.md'...
      OK.
    3 files added.
  Modifying files...
    [ 1 / 2 ] Updating 'skills/coding-conventions/SKILL.md'...
      OK.
    [ 2 / 2 ] Updating 'workflows/sync.md'...
      OK.
    2 files modified.
  Deleting deprecated files...
    [ 1 / 1 ] Deleting 'specs/commit-rules.md'...
      OK.
    1 file deleted.
  Skipping protected files...
    SKIP: 'specs/sops/project-release.md' -> never_overwrite.
  Updating 'last_sync' timestamp...
    OK. last_sync='2026-09-06T13:35:02Z'.

Summary: 3 added, 2 modified, 1 deleted, 1 skipped.
RESULT: OK
================================ END: WORKSPACE SYNC EXECUTE =================================
[2026-09-06 13:35:02] (2.0 secs)
```

## 10. Script Structure

```
sync.ps1
├─> Parameter block (param declaration with validation)
├─> Resolve-PathParam function (IS-01)
├─> Test-SyncConfig function (IS-04)
├─> Test-GlobMatch function (IS-06)
├─> Get-FileHash256 function (IS-07)
├─> Get-SourceFiles function (IS-05)
├─> Invoke-FileFilter function (IS-05 evaluation order)
├─> Compare-Files function (IS-07, IS-08)
├─> New-DiffReport function (IS-20)
├─> Invoke-Execute function (IS-11, IS-21)
├─> Update-LastSync function (IS-12)
├─> Main execution block:
│   ├─> Parse and validate parameters (IS-01, IS-02)
│   ├─> For each target-config pair (IS-14):
│   │   ├─> Read and validate config (IS-03, IS-04)
│   │   ├─> For each source entry matching -sources filter:
│   │   │   ├─> Discover and filter source files (IS-05)
│   │   │   ├─> Compare against target (IS-07, IS-08)
│   │   │   ├─> If -diff: generate report (IS-20, IS-10)
│   │   │   └─> If -execute: apply changes (IS-11, IS-21), update timestamp (IS-12)
│   └─> Output summary and exit with appropriate code
```

## 11. Verification Checklist

- [ ] VC-01: Script runs with single-string parameters
- [ ] VC-02: Script runs with JSON array parameters
- [ ] VC-03: `-diff` mode produces no file changes
- [ ] VC-04: `-diff` mode output matches actual file differences
- [ ] VC-05: `-execute` mode copies new files correctly
- [ ] VC-06: `-execute` mode overwrites modified files correctly
- [ ] VC-07: `-execute` mode deletes deprecated files correctly
- [ ] VC-08: `never_overwrite` files are not overwritten
- [ ] VC-09: `never_overwrite` files are not deleted even if deprecated
- [ ] VC-10: `last_sync` timestamp updated after successful execute
- [ ] VC-11: `last_sync` timestamp NOT updated after failed execute
- [ ] VC-12: Exit code 0 when no changes
- [ ] VC-13: Exit code 1 when changes found in diff
- [ ] VC-14: Exit code 2 on parameter/config errors
- [ ] VC-15: Exit code 3 on missing source
- [ ] VC-16: Exit code 4 on missing target
- [ ] VC-17: Exit code 5 on file operation errors
- [ ] VC-18: Unicode filenames handled correctly
- [ ] VC-19: Paths with spaces handled correctly
- [ ] VC-20: `-output-file` writes full report to file, summary to console
- [ ] VC-21: `-verbose` shows excluded files with reasons
- [ ] VC-22: Targets and configs paired 1:1 correctly, source filtering works (IS-14)
- [ ] VC-23: Empty source directory handled gracefully
- [ ] VC-24: Empty target directory handled gracefully
- [ ] VC-25: Unmanaged files at target are not deleted
- [ ] VC-26: User-Facing output uses 100-char START/END headers (LOG-UF-06)
- [ ] VC-27: User-Facing output uses `[YYYY-MM-DD HH:MM:SS]` timestamps (LOG-UF-01)
- [ ] VC-28: Progress indicators use `[ x / n ]` format (LOG-UF-02)
- [ ] VC-29: Status keywords match LOG-UF-03 patterns (OK, SKIP, ERROR, FAIL, PARTIAL FAIL)
- [ ] VC-30: No `INFO`/`DEBUG`/`WARN` prefixes in User-Facing output (LOG-UF rules)
- [ ] VC-31: Paths and names quoted with single quotes (LOG-GN-02)
- [ ] VC-32: Announce > Track > Report pattern visible in output (LOG-GN philosophy)
- [ ] VC-33: Two-level error format `<what failed> -> <system error>` (LOG-GN-08)
- [ ] VC-34: Script-Level output (stderr) has no timestamps (LOG-SC-01)
- [ ] VC-35: RESULT: keyword on final line before footer (LOG-SC-07)

## Document History

**[2026-09-06 13:50]**
- Fixed: IS-18/IS-19 — replaced `INFO`/`WARN`/`ERROR`/`DEBUG` log levels with LOG-UF/LOG-SC compliant status keywords [VERIFIED]
- Fixed: IS-19 log format `[ADD]`/`[MODIFY]` replaced with Announce>Track>Report pattern, 100-char headers, timestamps, progress indicators [VERIFIED]
- Added: IS-20 — diff report format with full LOG-UF compliance [VERIFIED]
- Added: IS-21 — execute summary format with full LOG-UF compliance [VERIFIED]
- Added: IS-19 — Script-Level output spec with LOG-SC compliance [VERIFIED]
- Removed: old IS-09 (superseded by IS-20) [VERIFIED]
- Fixed: SPEC section 13 — stale `rules/` and `[RULES_SOURCE_FOLDER]`/`[RULES_FOLDER]` references, rewritten logging examples to comply with LOG-UF/LOG-SC rules [VERIFIED]
- Fixed: Script structure tree indentation and IS references [VERIFIED]
- Added: VC-26 through VC-35 — logging compliance verification items [VERIFIED]

**[2026-09-06 13:45]**
- Fixed: IS-14 — replaced incorrect source-config cross-product with target-config 1:1 pairing and source filtering [VERIFIED]
- Fixed: IS-06 — platform-aware glob matching (case-sensitive on Linux, case-insensitive on Windows) [VERIFIED]
- Fixed: IS-11 — backup cleanup now definitive (delete on success, restore on failure) [VERIFIED]
- Fixed: MNF — clarified path resolution (command-line vs config-internal) [VERIFIED]
- Fixed: Sections 1.1, 1.3, 7 — converted markdown tables to lists per core-conventions [VERIFIED]
- Updated: IS-15 — clarified config path resolution vs source field resolution [VERIFIED]

**[2026-09-06 13:40]**
- Initial implementation plan created
- Covers: parameters, config reading, file discovery, glob matching, diff mode, execute mode, multi-source handling, error handling, edge cases, logging, script structure, verification checklist
