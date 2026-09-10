---
intended_model: claude-sonnet-4-5
context_window_size: 200k
reasoning_settings: high
prompt_system: IPPS
---

## Prompt 1 - Rewrite sync.ps1 for new targets-based schema

<!-- Rewrite sync.ps1 to accept -config (single JSON path), read targets array, output markdown preview per template. No bundles, no -sources/-targets/-configs params. -->

````
Rewrite `PromptSystemV4.4/skills/workspace-management/sync.ps1` to implement the new `promptsystem-sync.json` schema defined in `specs/_SPEC_WORKFLOW-MANAGEMENT_SKILL.md` FR-44 and FR-46.

The new schema uses a top-level `targets` array (not `sources`). Each target entry has: `path` (relative agent folder, e.g., `.devin`), `source` (relative path to source agent folder), `include` (glob whitelist), `exclude` (glob blacklist), `never_overwrite` (glob patterns). Top-level `deprecated` array is shared across all targets. No `bundles` or `selected_bundles` — include/exclude is the single filter layer.

New CLI parameters:
- `-config`: path to promptsystem-sync.json (required)
- `-preview_file`: path for markdown preview output (optional)
- `-output_file`: path for full text report (optional)
- `-diff` or `-execute`: mode flag (required)

Remove old parameters: `-sources`, `-targets`, `-configs`, `-deprecated`.

The script must:
- Read all config from the single JSON file at `-config` path
- Resolve `source` and `path` relative to the config file's directory
- Filter files: target include -> target exclude -> target never_overwrite -> deprecated (single layer, no bundle resolution)
- In `-diff` mode: write markdown preview to `-preview_file` formatted per `PROMPTSYSTEM_SYNC_PREVIEW_TEMPLATE.md` in the workspace-management skill folder. Structure:
  - Header: source path and target count
  - Deprecated files section (from top-level `deprecated` array)
  - Per-target blocks: Add count + file list, Overwrite count + file list, Delete count + file list, Skipped with reason, Locally modified, Excluded skills
  - Summary: aggregate counts across all targets
- Paths in preview use Windows backslashes, relative to target agent folder root
- In `-execute` mode: copy new/changed files, delete deprecated files, write `last_sync` timestamp to JSON
- Preserve existing logic for: hash-based file comparison, locally-modified detection (compare target file LastWriteTime against `last_sync`), never_overwrite enforcement

Constraints:
- Do not change the script's location or filename
- Do not add external PowerShell module dependencies
- Do not remove the text report output capability (console or `-output_file`)
- Keep the existing `Compare-Files` hash comparison approach
- The `deprecated` array paths are relative to the target agent folder, same as file paths in include/exclude

Verify: Run `sync.ps1 -diff -config "E:\Dev\USTVA\promptsystem-sync.json"` (after Prompt 2 updates the JSON). Script exits 0, produces markdown preview file with per-target blocks matching PROMPTSYSTEM_SYNC_PREVIEW_TEMPLATE.md. No errors about missing `bundles` or `selected_bundles`.
````

---

## Prompt 2 - Update all 9 downstream promptsystem-sync.json files to new schema

<!-- All 9 JSON files converted: sources array -> targets array, bundles removed, deprecated top-level, source paths point to agent folder. -->

````
Convert all 9 downstream `promptsystem-sync.json` files from the old schema to the new schema. The old schema has `sources` array with `selected_bundles`, `bundles`, per-source `deprecated`. The new schema has top-level `deprecated` and `targets` array.

New schema structure:
```json
{
  "last_sync": "existing-value-or-null",
  "deprecated": ["file1.md", "file2.md"],
  "targets": [
    {
      "path": ".devin",
      "source": "../IPPS/.devin",
      "include": ["*"],
      "exclude": [],
      "never_overwrite": []
    }
  ]
}
```

The 9 files to update (all at workspace root unless noted):
1. `E:\Dev\KarstensWorkspace\promptsystem-sync.json` — single target, include `["*"]`, exclude `[]`
2. `E:\Dev\OpenAI-BackendTools\promptsystem-sync.json` — single target, exclude development-only skills (same patterns as current top-level exclude)
3. `E:\Dev\PRXL\src\promptsystem-sync.json` — single target, same exclude patterns as current
4. `E:\Dev\SharePoint-GPT-Middleware\promptsystem-sync.json` — single target, preserve `never_overwrite: ["workflows/project-release.md"]`
5. `E:\Dev\USTVA\promptsystem-sync.json` — single target, include `["*"]`, exclude `[]`
6. `E:\Dev\openclaw\workspace\promptsystem-sync.json` — single target, preserve `never_overwrite: ["AGENTS.md", "HEARTBEAT.md", "memory/*", "MEMORY.md"]`
7. `E:\Dev\LLM-Research\promptsystem-sync.json` — single target, same exclude patterns as current
8. `E:\Dev\Lana-V1\promptsystem-sync.json` — TWO targets: `.devin` and `.lana`. Both from same source. `.devin` has `never_overwrite: ["skills/selftest/*"]`, `.lana` has `exclude: ["__pycache__/*", "*.pyc"]`
9. `E:\Dev\Lana-V1-Dev\promptsystem-sync.json` — single target. This is the ONLY config that actively used bundle include patterns. Move the `bundles.development.include` patterns into the target's `include` array. The current bundle include has specific skill/workflow/spec paths — those become the target `include` array.

For each file:
- Read the current JSON
- Extract `deprecated` from the source entry (if present) and move to top-level
- Extract `never_overwrite` from the source entry and keep in target entry
- Extract `include` and `exclude` from the source entry (or from bundle definitions for Lana-V1-Dev) and use as target `include`/`exclude`
- Set `source` to the current source path but pointing to the agent folder (e.g., if current source is `../IPPS/DevSystemV4.3`, change to `../IPPS/.devin` — the source agent folder, not the PromptSystem version folder)

Wait — check the actual current source paths in each file. The source should point to wherever the specs/, skills/, workflows/ folders live. If the current source is `../IPPS/DevSystemV4.3` and that folder contains specs/skills/workflows, then the new source should be `../IPPS/.devin` (the agent folder that contains the same structure). Verify by checking which folder in IPPS actually contains the synced content.

Constraints:
- Preserve `last_sync` timestamp if present
- Preserve all `never_overwrite` patterns exactly
- Preserve all `exclude` patterns exactly (including `__pycache__/*`, `*.pyc` for Lana-V1)
- Do not create backup files — overwrite the JSON files directly
- Do not add fields not in the new schema (no `bundles`, no `selected_bundles`, no `sources`)

Verify: Each JSON file parses as valid JSON. Each has `targets` array (not `sources`). No file contains `bundles` or `selected_bundles` keys. `deprecated` is top-level (not inside a target entry). Lana-V1 has 2 target entries, all others have 1.
````

---

## Prompt 3 - Update NOTES.md, sync.md, and PREVIEW_TEMPLATE for new schema

<!-- NOTES.md [LINKED_REPOS] lists repo roots only. sync.md uses new CLI. Preview template matches JSON output. -->

````
Update 3 files to reflect the new `promptsystem-sync.json` schema:

1. `E:\Dev\IPPS\NOTES.md` — Update the `[LINKED_REPOS]` section:
   - Replace absolute agent folder paths (e.g., `e:\Dev\KarstensWorkspace\.devin`) with relative repo root paths only (e.g., `../KarstensWorkspace`)
   - Remove all sub-bullets (Skills, Overwrite, Never overwrite, Delete, Special) — that information now lives in each repo's `promptsystem-sync.json`
   - Keep the section header as `**[LINKED_REPOS]**:`
   - List 9 repos (Lana-V1 appears once, not twice — the `.lana` target is discovered from its promptsystem-sync.json)
   - Use relative paths from IPPS workspace root: `../KarstensWorkspace`, `../OpenAI-BackendTools`, `../PRXL/src`, `../SharePoint-GPT-Middleware`, `../USTVA`, `../openclaw/workspace`, `../LLM-Research`, `../Lana-V1`, `../Lana-V1-Dev`

2. `E:\Dev\IPPS\PromptSystemV4.4\workflows\sync.md` — Update the Workspace Sync section (lines ~213-274):
   - Replace `sync.ps1 -diff -sources <source> -targets <target> -configs promptsystem-sync.json -deprecated '<JSON array>' -preview_file <path>` with `sync.ps1 -diff -config <path> -preview_file <path>`
   - Replace `sync.ps1 -execute -sources <source> -targets <target> -configs promptsystem-sync.json -deprecated '<JSON array>'` with `sync.ps1 -execute -config <path>`
   - Remove step 2 about reading `[DEPRECATED_FILES]` from NOTES.md — deprecated is now in promptsystem-sync.json top-level
   - Update step 3: "For each target entry in config" (not "for each source entry")
   - Remove references to `selected_bundles`, `bundles`, bundle definitions
   - Update step 4: preview file is now JSON (read JSON, format using PROMPTSYSTEM_SYNC_PREVIEW_TEMPLATE.md)
   - Keep the MUST-NOT-FORGET block (diff ALL targets before execute, present in chat, etc.)
   - Keep the use cases section but update parameter references

3. `E:\Dev\IPPS\PromptSystemV4.4\skills\workspace-management\PROMPTSYSTEM_SYNC_PREVIEW_TEMPLATE.md`:
   - Update header: source path comes from JSON preview `source` field, N = number of targets in JSON
   - Change "Deprecated Files (source-level, from NOTES.md [DEPRECATED_FILES])" to "Deprecated Files (from promptsystem-sync.json top-level)"
   - Update per-target preview block: use `path` field from JSON (relative, e.g., `.devin`) instead of absolute paths
   - Add `locally_modified` field to the template block
   - Update the Full Example to use relative paths and new field names
   - Remove references to "bundle include/exclude rules" — use "target include/exclude patterns"

Constraints:
- Do not modify the `[DEPRECATED_FILES]` section in NOTES.md (only update `[LINKED_REPOS]`)
- Do not change other sections of sync.md (Code→Docs, SPEC→Downstream, etc.)
- Do not change the MUST-NOT-FORGET block in sync.md
- Preserve the template's conditional comments (include block only when count > 0, etc.)

Verify: NOTES.md `[LINKED_REPOS]` contains 9 relative paths, no absolute paths, no sub-bullets. sync.md has no references to `-sources`, `-targets`, `-configs`, `-deprecated`, `selected_bundles`, or `bundles`. PREVIEW_TEMPLATE has `locally_modified` field and uses relative paths in example.
````

---

## Prompt 4 - Test: Run diff preview on one target

<!-- Run sync.ps1 -diff on USTVA (simplest config) to verify script works with new schema. -->

````
Test the rewritten `sync.ps1` by running a diff preview on the simplest downstream repo (USTVA — single target, include all, no exclusions).

Run:
```
powershell -File "E:\Dev\IPPS\PromptSystemV4.4\skills\workspace-management\sync.ps1" -diff -config "E:\Dev\USTVA\promptsystem-sync.json" -preview_file "E:\Dev\IPPS\.tmp_sync_preview.md"
```

Then read the generated `.tmp_sync_preview.md` file.

Verify:
- Script exits with code 0 (no errors)
- Preview file exists and contains markdown formatted per `PROMPTSYSTEM_SYNC_PREVIEW_TEMPLATE.md`
- Markdown contains header with source path and target count
- Markdown contains per-target block with Add/Overwrite/Delete/Skipped sections
- No references to `bundles` or `selected_bundles` in the output
- File paths in the markdown use Windows backslashes
- If script fails, report the error message and fix the issue in sync.ps1

Constraints:
- Do not run `-execute` mode
- Do not modify any downstream repo files
- If the script fails, fix sync.ps1 and re-run (max 3 attempts)

Verify: `.tmp_sync_preview.md` exists, contains markdown with per-target preview blocks matching the template structure.
````

---

## Prompt 5 - Test: Full sync preview to all targets and execute

<!-- Run diff for all 9 repos, present preview in chat, execute on confirmation. -->

````
Run the full sync preview across all 9 downstream repos using the new `sync.ps1` and updated `promptsystem-sync.json` files.

Read `NOTES.md` `[LINKED_REPOS]` section for the list of repo roots. For each repo root, run:
```
powershell -File "E:\Dev\IPPS\PromptSystemV4.4\skills\workspace-management\sync.ps1" -diff -config "<repo_root>\promptsystem-sync.json" -preview_file "E:\Dev\IPPS\.tmp_sync_preview_<reponame>.md"
```

After all diffs complete, read all preview markdown files and present a summary in chat using the format from `PROMPTSYSTEM_SYNC_PREVIEW_TEMPLATE.md`:
- One section per target (never aggregate)
- Files to add, modify, delete, skip
- Locally modified files (if any)
- Excluded skills (if any)
- Deprecated files
- Summary line: N repos, N files to deploy, N files to delete

Prompt for confirmation. On confirmation keyword, run `-execute` for each repo:
```
powershell -File "E:\Dev\IPPS\PromptSystemV4.4\skills\workspace-management\sync.ps1" -execute -config "<repo_root>\promptsystem-sync.json"
```

After execution, verify each repo's `promptsystem-sync.json` has updated `last_sync` timestamp.

Constraints:
- Run `-diff` for ALL repos before any `-execute`
- Present preview in chat text (not buried in command output)
- Do not execute without explicit confirmation keyword
- If any diff fails, report error and stop — do not execute on failed repos
- Clean up `.tmp_sync_preview_*.md` files after completion

/verify against `specs/_SPEC_WORKFLOW-MANAGEMENT_SKILL.md` FR-44, FR-46, FR-49

Verify: All 9 repos synced. Each `promptsystem-sync.json` has updated `last_sync`. No errors in any sync execution. Preview was presented in chat before execution.
````
