---
name: workspace-management
description: Manages multi-repo workspace setup, DevSystem synchronization, and knowledge distribution. Use when configuring workspace constants, syncing between source and target repos, verifying workspace integrity, or committing across multiple repos.
compatibility: PowerShell 7+ for diff/sync scripts
---

# Workspace Management

Manages workspace setup, DevSystem sync, and knowledge distribution across product/dev/company repo architectures.

References (loaded on demand):
- WORKSPACE-GUIDES.md - High-level guidance on workspace setup, product/dev separation, sync sources
- WORKSPACE-RULES.md - Verifiable rules for workspace integrity, required files and constants
- WORKSPACE_CREATION_QUESTIONNAIRE.md - Interactive questionnaire for creating new workspaces with defaults
- DEV_REPO_NOTES_TEMPLATE.md - Template for DevRepo NOTES.md with all workspace constants
- PRODUCT_REPO_README_TEMPLATE.md - Template for ProductRepo README.md
- COMPANY_REPO_NOTES_TEMPLATE.md - Template for CompanyRepo NOTES.md with sync policy tracking
- sync.ps1 - Generic sync script with -diff and -execute modes (replaces workspace_diff_template.ps1 and workspace_sync_template.ps1)

## MUST-NOT-FORGET

1. All paths must come from workspace constants in DevRepo NOTES.md - never hardcode project-specific paths
2. Always run sync.ps1 -diff before -execute - review changes before applying
3. Check never_overwrite patterns - files matching never_overwrite are never overwritten or deleted during sync
4. Rollback on shared branches (main, master, remote-tracked) requires explicit confirmation - advise revert commit instead
5. Privacy gate - no real identifiers, project names, or paths in any skill file
6. Sync config is JSON-based: devsystem-sync.json at target [WORKSPACE_FOLDER] root is single source of truth - no NOTES.md prose lookup

## Intent Lookup

User wants to...
- Create a new workspace → WORKSPACE_CREATION_QUESTIONNAIRE.md questionnaire
- Compare workspace settings → Procedure 1, FR-15
- Update workspace from source → Procedure 2, FR-16
- Roll back workspace settings → Procedure 3, FR-17
- Check if repo is synced or self-contained → Procedure 4, FR-18
- Check workspace integrity → Procedure 4, FR-18
- Compare DevSystem files → Procedure 1, FR-19
- Update DevSystem from source → Procedure 2, FR-20
- Roll back DevSystem → Procedure 3, FR-21
- Check DevSystem integrity → Procedure 4, FR-22
- Compare knowledge bundles → Procedure 1, FR-23
- Update knowledge from source → Procedure 2, FR-24
- Roll back knowledge → Procedure 3, FR-25
- Check knowledge integrity → Procedure 4, FR-26
- Commit across multiple repos → Procedure 5, FR-30

## Core Procedures

### 1. Compare

```
1. Read devsystem-sync.json from target [WORKSPACE_FOLDER] root
2. Determine sync area (WORKSPACE, DEVSYSTEM, KNOWLEDGE)
3. Determine sync source and target from config source entries
4. Run sync.ps1 -diff -sources <source> -targets <target> -configs <config>
5. Review structured diff report: new files, modified files, deleted files, skipped files
6. Note excluded files (filtered by bundle include/exclude rules) with -verbose
```

Use before any sync operation to preview changes. Use before deploy to verify DevSystem is current.

### 2. Update

```
1. Run Compare procedure first
2. Review diff preview - check for breaking changes, locally-modified files
3. Read all sync config from target's devsystem-sync.json (bundles, filters, never_overwrite, deprecated)
4. Confirm sync: prompt user (yes/go/confirmed/execute/apply to proceed, no/cancel/abort/stop to abort)
5. Run sync.ps1 -execute -sources <source> -targets <target> -configs <config>
6. Verify last_sync timestamp updated in devsystem-sync.json
7. Report results per file: added, modified, deleted, skipped
```

Use to sync DevSystem from source, knowledge from Company, or specs from Company. Downstream = sync from source to all targets. Upstream = sync from here back to source.

### 3. Rollback

```
1. Determine area to rollback (WORKSPACE, DEVSYSTEM, KNOWLEDGE)
2. Check current branch: if shared (main, master, remote-tracked), display warning
3. Advise manual revert commit for shared branches. Proceed only with explicit confirmation
4. For non-shared branches: use git history to identify previous version
5. Roll back using git checkout of previous committed version
6. Report what changed between current and rolled-back version
```

Use when sync introduced errors or unwanted changes. IG-07: rollback on shared branches is dangerous - always warn first.

### 4. Integrity Check

```
1. Determine area to check (WORKSPACE, DEVSYSTEM, KNOWLEDGE)
2. For WORKSPACE: verify required constants in DevRepo NOTES.md, required files exist, workspace structure matches declared mode
3. For DEVSYSTEM: verify agent folder has specs/, workflows/, skills/ subfolders, all skills registered in [SKILL_CATEGORIES], no deprecated files
4. For KNOWLEDGE: verify knowledge folder exists if [KNOWLEDGE_FOLDER] set, all bundles in devsystem-sync.json exist, no empty bundles
5. Report sync relationship state (SYNCED or SELF-CONTAINED)
6. Report gaps and incompatibilities
7. Fix actions: missing constant -> add with template default. Missing file -> create from template. Broken reference -> report only. Structural violation -> report only
```

Use via /verify workspace context. Downstream customizations are allowed and do not fail verification.

### 5. Multi-Repo Commit

```
1. Detect WORKSPACE mode (main.code-workspace exists)
2. Detect changes across all git repos in workspace
3. Commit order: 1) product repo, 2) dev repo, 3) all other workspace repos
4. For each repo with changes:
   a. Detect uncommitted changes
   b. Analyze by type (feat, fix, docs, test, chore)
   c. Use git -C [repo_path] for all git operations
   d. Detect and use per-repo git config (user.name, user.email)
   e. Create conventional commits
5. If a repo commit fails: report error, continue with remaining repos, summarize partial success
6. Skip repos with no changes silently
7. Report committed changes per repo at end
```

Use via /commit in WORKSPACE mode. SINGLE-PROJECT and MONOREPO modes use existing single-repo commit behavior.

## Gotchas

- Sync config is JSON-based - All sync configuration lives in devsystem-sync.json at target [WORKSPACE_FOLDER] root. No NOTES.md prose lookup or hardcoded arrays
- never_overwrite overrides deprecated - Files matching never_overwrite patterns are protected from both overwrite and deletion, even if also matching deprecated patterns
- Rollback on shared branches - Using git checkout on shared branches (main, master) can cause issues for other contributors. Always use revert commit instead. IG-07 requires explicit confirmation

## Quick Config

Always required workspace constants in DevRepo NOTES.md:

```
## Workspace Constants
- [DEV_REPO_FOLDER]: [WORKSPACE_FOLDER]
- [PRODUCT_REPO_FOLDER]: [WORKSPACE_FOLDER]\..\[product-repo-name]
- [KNOWLEDGE_FOLDER]: [DEV_REPO_FOLDER]\knowledge
- [SPECS_FOLDER]: [DEV_REPO_FOLDER]\specs
- [PRODUCT_DOCS_FOLDER]: [PRODUCT_REPO_FOLDER]\docs
```

Required for SYNCED only (remove if SELF-CONTAINED):

```
- [COMPANY_REPO_FOLDER]: [WORKSPACE_FOLDER]\..\Company
- [KNOWLEDGE_SOURCE_FOLDER]: [COMPANY_REPO_FOLDER]\knowledge
- [SPECS_SOURCE_FOLDER]: [COMPANY_REPO_FOLDER]\specs
```

See DEV_REPO_NOTES_TEMPLATE.md for full template with defaults and instructions.
