---
description: Global and local refactoring with exhaustive search and verification
auto_execution_mode: 1
---

# Rename / Refactor Workflow

### Phase 1: Analysis

1. Clarify scope - Global (workspace) or Local (folder/files)?
2. Search all occurrences - `grep_search: Query="<old_pattern>", SearchPath="<scope>", CaseSensitive=false`
3. Build occurrence list - file path, line number(s), context
4. Identify special cases - protected files (`.windsurf/`, `node_modules/`), binaries (skip), case sensitivity risks

### Phase 2: Planning

5. Create replacement plan - group by: Direct edits, Manual sync (protected folders), Skip (binary/generated)
6. Present plan to user - show total occurrences; confirm only if Step 4 yielded critical cases

### Phase 3: Execution

7. Execute replacements - `replace_all=true` for accessible files; PowerShell copy for protected folders

### Phase 4: Verification

8. Re-search for old pattern - should return zero results except user-confirmed exceptions
9. Report results - files updated, remaining occurrences, manual actions needed