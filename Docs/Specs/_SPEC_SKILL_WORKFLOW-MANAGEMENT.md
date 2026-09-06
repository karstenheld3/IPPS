# SPEC: Workspace Management Skill

**Doc ID**: WSKMGMT-SP01
**Feature**: workspace-management-skill
**Goal**: Specify a skill that manages agentic workspace setup, DevSystem synchronization, and knowledge distribution across product/dev/company repo architectures
**Timeline**: Created 2026-09-03, Updated 8 times (2026-09-03 - 2026-09-06)
**Target file(s)**:
- `DevSystemV4.3/specs/devsystem-core.md` (Operation Modes, Workspace Scenarios)
- `DevSystemV4.3/skills/workspace-management/SKILL.md`
- `DevSystemV4.3/skills/workspace-management/WORKSPACE-GUIDES.md`
- `DevSystemV4.3/skills/workspace-management/WORKSPACE-RULES.md`
- `DevSystemV4.3/skills/workspace-management/WORKSPACE_CREATION_QUESTIONNAIRE.md`
- `DevSystemV4.3/skills/workspace-management/DEV_REPO_NOTES_TEMPLATE.md`
- `DevSystemV4.3/skills/workspace-management/PRODUCT_REPO_README_TEMPLATE.md`
- `DevSystemV4.3/skills/workspace-management/COMPANY_REPO_NOTES_TEMPLATE.md`
- `DevSystemV4.3/skills/workspace-management/workspace_diff_template.ps1` (deleted, replaced by sync.ps1)
- `DevSystemV4.3/skills/workspace-management/workspace_sync_template.ps1` (deleted, replaced by sync.ps1)
- `DevSystemV4.3/skills/workspace-management/sync.ps1` (single generic sync script with -diff and -execute modes)
- `[WORKSPACE_FOLDER]\devsystem-sync.json` (target-side sync config, single source of truth)
- `DevSystemV4.3/workflows/workspace-create.md` (new workflow)
- `DevSystemV4.3/workflows/verify.md` (new context section)
- `DevSystemV4.3/workflows/sync.md` (new context section)
- `DevSystemV4.3/workflows/commit.md` (multi-repo commit support)
- `ID-REGISTRY.md` (Workspace Context states)

**Depends on:**
- `DevSystemV4.3/specs/devsystem-core.md` for existing operation modes and workspace scenarios
- `DevSystemV4.3/skills/session-management/SKILL.md` for session folder structure (T##/S##)

**Does not depend on:**
- Any project-specific SPEC (this skill is generic, reusable across all DevSystem workspaces)
- `deploy-to-all-repos.md` is replaced by this spec (FR-49), not a dependency

## MUST-NOT-FORGET

- Skill files must be generic - no project-specific data, no real identifiers, addresses, or names
- All new rules/workflows/skills created in `[DEVSYSTEM_FOLDER]` first, then sync to `.devin/`
- Register `workspace-management` in `NOTES.md` `[SKILL_CATEGORIES]`
- Follow SOP 1 (SOPS.md) for new skill creation including verification
- `deploy-to-all-repos.md` is replaced by `sync.md` workspace sync context using single `sync.ps1` with -diff and -execute modes - no standalone deploy workflow
- Workspace constants are defined in DevRepo NOTES.md, not in the skill itself - skill reads them from there
- Sync config read from `devsystem-sync.json` at target `[WORKSPACE_FOLDER]` root - no NOTES.md prose lookup
- Downstream repo modifications are allowed during verify - only gaps and incompatibilities must be fixed
- IMPL-ISOLATED extension is a core rule change affecting all DevSystem users - must be backwards compatible
- WORKSPACE mode is additive to Dimension 1 - existing SINGLE-PROJECT and MONOREPO detection must not break
- Dimension 4 (Sync Relationship) is additive - existing 3 dimensions must not break
- Detection must be deterministic - no ambiguity between SYNCED and SELF-CONTAINED
- SELF-CONTAINED repos must still pass /verify - missing sync constants are valid, not gaps
- Existing repos with [LINKED_REPOS] or [*_SOURCE_FOLDER] are SYNCED by default - migration to devsystem-sync.json required but sync relationship detection unchanged
- Workspace creation questionnaire must show impact per question so user understands consequences of each choice
- Workspace creation is non-destructive (creating new files/folders) - no confirmation gate per WF-EX-01
- `workspace-create.md` workflow is thin: references WORKSPACE_CREATION_QUESTIONNAIRE.md for questionnaire content, does not replicate questions
- Sync configuration is JSON-based: devsystem-sync.json at target [WORKSPACE_FOLDER] root is single source of truth - no hardcoded arrays in scripts or NOTES.md prose
- Single sync.ps1 script with -diff and -execute modes; params are -sources, -targets, -configs, -output-file (all accept JSON arrays or single strings)
- Source repo only references RELATIVE downstream repo paths (e.g., ../Lana-V2-Dev), never absolute paths
- Bundle definitions live in target's devsystem-sync.json, NOT at source - each source entry carries its own complete sync configuration
- Include/exclude refiners are glob patterns evaluated in order: source include → source exclude → bundle include → bundle exclude → target never_overwrite → deprecated
- `rules` folder renamed to `specs` with subfolders `sops/` and `guides/`

## Table of Contents

1. [Scenario](#1-scenario)
2. [Context](#2-context)
3. [Domain Objects](#3-domain-objects)
4. [Functional Requirements](#4-functional-requirements)
5. [Non-Functional Requirements](#5-non-functional-requirements)
6. [Design Decisions](#6-design-decisions)
7. [Implementation Guarantees](#7-implementation-guarantees)
8. [Key Mechanisms](#8-key-mechanisms)
9. [Action Flow](#9-action-flow)
10. [Data Structures](#10-data-structures)
11. [User Actions](#11-user-actions)
12. [UX Design](#12-ux-design)
13. [Logging Requirements](#13-logging-requirements)
14. [Technical Constraints](#14-technical-constraints)
15. [Document History](#15-document-history)

## 1. Scenario

**Problem:** DevSystem workspaces come in multiple architectures (single project, monorepo, multi-repo workspace with product/dev separation). The current system has no unified way to compare workspace state against central sources, update from sources, roll back changes, or verify integrity. Existing mechanisms (SOPS.md, /prime, /sync) are scattered and do not cover the full product/dev/company repo pattern. The legacy `deploy-to-all-repos.md` script hardcodes target paths and skill categories in PowerShell, is not machine-readable, and is project-specific to IPPS.

**Solution:**
- Extend core rules with WORKSPACE mode and IMPL-ISOLATED T##/S## folders
- Create a workspace-management skill with Guides, Rules, and Checks (GRUC) files, templates, and diff/sync scripts
- Integrate with `/verify` (new "Workspace Setup" context) and `/sync` (new "Workspace Sync" context)
- Cover 3 areas (WORKSPACE, DEVSYSTEM, KNOWLEDGE) x 4 operations (compare, update, rollback, integrity)

**What we don't want:**
- Hardcoded project paths in skill scripts - must work for any DevSystem workspace
- Skill that only works for one workspace pattern - must be generic
- Separate commands for each area/operation - one skill with context-driven behavior
- Templates that bake in project-specific content - templates define structure, not content
- Sync that overwrites downstream modifications without preview - always preview before execute
- Verify that fails on intentional downstream customizations - allow modifications, fix only gaps and incompatibilities

## 2. Context

The DevSystem currently supports two operation modes (IMPL-CODEBASE, IMPL-ISOLATED) and three workspace scenario dimensions (Project Structure, Version Strategy, Work Mode). The existing `/prime` workflow detects these scenarios but cannot classify multi-repo workspaces where a DevRepo contains `main.code-workspace` referencing a separate ProductRepo.

Real-world pattern: A DevRepo (private, git) contains specs, sessions, evals, knowledge, and an agent folder (`.devin/`). It has `main.code-workspace` referencing a separate ProductRepo (public, git) with shipped code. A `Company` folder serves as central source for knowledge and specs. The DevSystem source is a separate folder with versioned DevSystem releases.

### Dependency Tree

```
DevSystem source          CompanyRepo
(upstream origin)         (upstream origin)
    │                         │
    │  downstream             │  downstream
    │  (sync to all           │  (sync to all
    │   targets)              │   targets)
    ▼                         ▼
  DevRepo (current workspace)
    │  owns 1:1
    ▼
  ProductRepo
  (docs only, no specs/knowledge/DevSystem artifacts)

  Dev-to-Dev sync chain (DevRepo as source for other DevRepos):

  [Product 1 DevRepo]
      │  downstream
      │  (sync to all targets)
      ▼
  [Product 2 DevRepo]    ← downstream from Product 1's perspective
      │  owns 1:1         ← Product 1 is upstream from Product 2's perspective
      ▼
  [Product 2 ProductRepo]
```

Direction definitions:
- Downstream = sync from source to all targets (distribute content to dependent repos)
- Upstream = sync from here back to source (push local changes back to origin)
- A repo can be both upstream and downstream simultaneously in a dependency chain

Existing infrastructure:
- `SOPS.md`: 7 Standard Operating Procedures (SOPs) for DevSystem file/skill/version changes
- `/prime`: Detects workspace scenario, reads rules and docs
- `/sync`: Document-level sync (code to docs, session to project) - will gain Workspace Sync context
- `/verify`: Multi-context verification (SPEC, IMPL, Code, TEST, etc.)
- `deploy-to-all-repos.md`: Legacy IPPS-only deployment script - replaced by generic sync.md workspace context (FR-49)
- Session management skill: Init/save/resume/finalize/archive lifecycle

None of these provide unified workspace compare/update/rollback/integrity operations. The workspace-management skill fills this gap.

Note: The DevSystem source repository is the upstream source for all DevSystem workspaces. It contains the canonical version of specs, skills, and workflows.

## 3. Domain Objects

### Workspace

A **Workspace** is the root context for agentic development. Contains one or more repos and a `main.code-workspace` file in WORKSPACE mode.

**Storage:** Filesystem root (e.g., `[WORKSPACE_FOLDER]`)
**Key properties:**
- `workspace_mode` - SINGLE-PROJECT, MONOREPO, or WORKSPACE
- `main_code_workspace` - path to `.code-workspace` file (WORKSPACE mode only)
- `repos` - list of repos contained in the workspace

### DevRepo

A **DevRepo** is the development repository containing specs, sessions, evals, knowledge, SOPs, and agent configuration. Usually private. Contains `main.code-workspace` in WORKSPACE mode.

**Storage:** `[DEV_REPO_FOLDER]`
**Key properties:**
- `notes_path` - `[DEV_REPO_FOLDER]\NOTES.md` (or `!NOTES.md`)
- `agent_folder` - `[DEV_REPO_FOLDER]\.devin` (or project-specific agent folder)
- `knowledge_folder` - `[DEV_REPO_FOLDER]\knowledge`
- `sessions_folder` - `[DEV_REPO_FOLDER]\_Sessions` or `_PrivateSessions`
- `specs_folder` - `[DEV_REPO_FOLDER]\specs`
- `evals_folder` - `[DEV_REPO_FOLDER]\evals`

### ProductRepo

A **ProductRepo** is the product repository containing shipped code, tests, config, and product docs. Usually public. Referenced in `main.code-workspace`.

**Storage:** `[PRODUCT_REPO_FOLDER]`
**Key properties:**
- `readme_path` - `[PRODUCT_REPO_FOLDER]\README.md`
- `docs_folder` - `[PRODUCT_REPO_FOLDER]\docs`
- `src_folder` - `[PRODUCT_REPO_FOLDER]\src`
- `agent_folder` - optional, product-specific agent folder (e.g., `.[product-agent-folder]`)

### CompanyRepo

A **CompanyRepo** is a central source folder (not necessarily a git repo) containing knowledge bundles and specs shared across multiple workspaces. Tracks downstream repositories and sync policies.

**Storage:** `[COMPANY_REPO_FOLDER]` (default: `[WORKSPACE_FOLDER]\..\Company`)
**Key properties:**
- `notes_path` - `[COMPANY_REPO_FOLDER]\NOTES.md`
- `knowledge_source_folder` - `[COMPANY_REPO_FOLDER]\knowledge`
- `specs_source_folder` - `[COMPANY_REPO_FOLDER]\specs`
- `downstream_repos` - list of registered downstream repos with sync policies

### SyncPolicy

A **SyncPolicy** defines what content syncs from which source to which target, in which direction, with which filters.

**Storage:** Downstream repo NOTES.md (priority 1) or CompanyRepo NOTES.md (priority 2)
**Key properties:**
- `source_folder` - central source path
- `target_folder` - local target path
- `direction` - downstream (source to target) or upstream (target to source)
- `content_filter` - include/exclude patterns (e.g., skill categories, knowledge bundles)
- `overwrite_rules` - which files to overwrite vs preserve

### PromptSystem

A **PromptSystem** is a folder containing `specs`, `skills`, and `workflows` subfolders. The DevSystem source is a PromptSystem. Agent folders (e.g., `.devin`, `.[product-agent-folder]`) are PromptSystem mirrors.

**Storage:** `[DEVSYSTEM_FOLDER]` (source), `[AGENT_FOLDER]` (mirror)
**Key properties:**
- `specs_folder` - contains spec `.md` files
- `workflows_folder` - contains workflow `.md` files
- `skills_folder` - contains skill subfolders with `SKILL.md`

### KnowledgeBundle

A **KnowledgeBundle** is a folder of reference documents for a specific topic (e.g., `Windsurf/`, `AI-Standards/`, `OpenAI/`).

**Storage:** `[KNOWLEDGE_FOLDER]` (local) or `[KNOWLEDGE_SOURCE_FOLDER]` (central)
**Key properties:**
- `bundle_name` - folder name (e.g., `Windsurf`)
- `documents` - list of contained `.md` files
- `sub_bundles` - nested folders (e.g., `Windsurf/HowCascadeWorks/`)

### SpecsBundle

A **SpecsBundle** is a folder of specs, workflows, design guidelines, and SOPs shared from Company to downstream repos.

**Storage:** `[SPECS_FOLDER]` (local) or `[SPECS_SOURCE_FOLDER]` (central)
**Key properties:**
- `bundle_name` - folder name
- `documents` - list of contained `.md` files

### SyncRelationship

A **SyncRelationship** is the 4th workspace scenario dimension, indicating whether a repo participates in a sync dependency tree.

**Storage:** Detected from DevRepo NOTES.md content (not stored as a field)
**Key properties:**
- `state` - SYNCED or SELF-CONTAINED
- `has_upstream` - boolean, true if [*_SOURCE_FOLDER] constants defined
- `has_downstream` - boolean, true if [SYNCED_REPOS] section defined in source NOTES.md

### Detection Markers

Sync-related markers that indicate SYNCED state:
- `devsystem-sync.json` exists at [WORKSPACE_FOLDER] root → has sync configuration
- `[SYNCED_REPOS]` section in source NOTES.md → has downstream targets
- `[KNOWLEDGE_SOURCE_FOLDER]` constant defined → has knowledge upstream
- `[SPECS_SOURCE_FOLDER]` constant defined → has specs upstream
- `[DEVSYSTEM_FOLDER]` or `[DEVSYSTEM]` reference → has DevSystem upstream

If none of these markers are found, the repo is SELF-CONTAINED.

Direction definitions:
- Downstream = sync from source to all targets (distribute content to dependent repos)
- Upstream = sync from here back to source (push local changes back to origin)
- SYNCED = repo participates in sync dependency tree (has upstream sources and/or downstream targets)
- SELF-CONTAINED = repo manages all content locally, no sync relationships

## 4. Functional Requirements

### Core Rule Updates

**WSKMGMT-FR-01: Extend IMPL-ISOLATED with Topic and Step folders**
- Add `T##_` (Topic) and `S##_` (Step) folders as valid IMPL-ISOLATED output locations
- Existing `[SESSION_FOLDER]/` and `[SESSION_FOLDER]/poc/` remain valid
- Must be backwards compatible - no existing behavior changes

**WSKMGMT-FR-02: Add WORKSPACE mode to Dimension 1**
- Add `WORKSPACE` as third option in Project Structure dimension
- `WORKSPACE` = workspace root with multiple independent repos (not monorepo)
- Detection: presence of `main.code-workspace` file in workspace root
- Existing `SINGLE-PROJECT` and `MONOREPO` detection must not break

**WSKMGMT-FR-03: Per-repo version detection in WORKSPACE mode**
- In WORKSPACE mode, detect SINGLE-VERSION or MULTI-VERSION for each repo independently
- Report version strategy per repo, not as single workspace-wide value

**WSKMGMT-FR-04: Register WORKSPACE state in ID-REGISTRY.md**
- Add `WORKSPACE` to Workspace Context states in ID-REGISTRY.md
- Keep existing `SINGLE-PROJECT`, `MONOREPO`, `SINGLE-VERSION`, `MULTI-VERSION`, `SESSION-MODE`, `PROJECT-MODE`

### Workspace Architecture

**WSKMGMT-FR-05: Product/Dev repo separation pattern**
- DevRepo contains `main.code-workspace`, specs, sessions, evals, knowledge, SOPs, agent folder
- ProductRepo contains shipped code, tests, config, product docs, optional agent folder
- DevRepo can be private, ProductRepo can be public
- Skill must support this pattern but not require it (SINGLE-PROJECT workspaces still work)

**WSKMGMT-FR-06: Workspace constants in DevRepo NOTES.md**
- Define and track workspace constants in DevRepo NOTES.md
- Required constants: `[DEV_REPO_FOLDER]`, `[PRODUCT_REPO_FOLDER]`, `[COMPANY_REPO_FOLDER]`, `[KNOWLEDGE_FOLDER]`, `[KNOWLEDGE_SOURCE_FOLDER]`, `[SPECS_FOLDER]`, `[SPECS_SOURCE_FOLDER]`, `[PRODUCT_DOCS_FOLDER]`
- Constants are workspace-specific - skill reads them from NOTES.md, does not hardcode values
- `DEV_REPO_NOTES_TEMPLATE.md` provides the template with all constants and defaults

**WSKMGMT-FR-07: Three sync sources**
- Prompt System: default source is DevSystem source `[WORKSPACE_FOLDER]\..\[DevSystemSourceName]\DevSystemV*`, syncs to `[DEV_REPO_FOLDER]\.devin` and/or other agent folders
- Knowledge: default source is `[KNOWLEDGE_SOURCE_FOLDER]` (Company), syncs to `[KNOWLEDGE_FOLDER]`
- Specs: default source is `[SPECS_SOURCE_FOLDER]` (Company), syncs to `[SPECS_FOLDER]`
- Each source supports downstream (source to target) and upstream (target to source) sync

### Skill Files

**WSKMGMT-FR-08: WORKSPACE-GUIDES.md**
- High-level guidance on how to set up agentic projects
- Covers: when to use product/dev separation, how to structure a workspace, how to configure sync sources, how to manage knowledge bundles
- Written for agent consumption (SKILL.md format, no visual-only formatting)

**WSKMGMT-FR-09: WORKSPACE-RULES.md**
- Verifiable rules for workspace setup and integrity
- Each rule has BAD/GOOD examples where non-trivial
- Rule Index at top
- Covers: required files per workspace type, required constants, sync policy requirements, template compliance rules

**WSKMGMT-FR-10: DEV_REPO_NOTES_TEMPLATE.md**
- Template for DevRepo NOTES.md with all workspace constants
- Includes: workspace constants section, sync sources section, project info section, build/test rules section
- Constants have default values and inline instructions for customization
- Follows TEMPLATE_RULES.md (all TMPL-* rules)

**WSKMGMT-FR-11: PRODUCT_REPO_README_TEMPLATE.md**
- Template for ProductRepo README.md with required and optional sections
- Required: project name, goal, setup instructions, build/run commands, test commands
- Optional: architecture overview, configuration, deployment, contributing, license
- Follows TEMPLATE_RULES.md

**WSKMGMT-FR-12: COMPANY_REPO_NOTES_TEMPLATE.md**
- Template for CompanyRepo NOTES.md
- Tracks downstream repositories and sync policy
- Per downstream repo: repo path, skill categories, knowledge bundles, specs, workflows, DevSystem specs to sync
- Defines overwrite rules and content filters per repo
- Follows TEMPLATE_RULES.md

**WSKMGMT-FR-13: Diff scripts**
- PowerShell script that compares source and target folders
- Reports: new files in source (to add), modified files (content differs), deleted files (in target but not source)
- Supports include/exclude filters for content filtering
- Output: structured diff report (not a file-by-file console dump)
- Must be generic - no hardcoded project paths, reads paths from workspace constants

**WSKMGMT-FR-14: Sync scripts**
- PowerShell script that executes sync operations based on diff output
- Handles file copy, delete, and content migration for breaking changes
- Preview mode (dry-run via `-diff`) and execute mode (`-execute`)
- Must be generic - no hardcoded project paths
- Before overwriting a file not in `never_overwrite`, check if target file was modified after `last_sync` timestamp in `devsystem-sync.json`. If so, mark as `LOCALLY_MODIFIED` in diff preview to warn user before overwrite
- Store `last_sync` timestamp in `devsystem-sync.json` at target `[WORKSPACE_FOLDER]` root. Missing timestamp triggers full comparison
- Upstream sync (target to source) is handled at workflow level by swapping `-sources` and `-targets` parameters — sync.ps1 itself is always source-to-target

### WORKSPACE Area Operations

**WSKMGMT-FR-15: Compare workspace settings against central source**
- Compare DevRepo NOTES.md constants against template defaults
- Compare workspace structure against WORKSPACE-RULES.md requirements
- Report: missing constants, mismatched defaults, structural violations

**WSKMGMT-FR-16: Update workspace settings from central source**
- Update DevRepo NOTES.md with new or changed constants from template
- Migrate breaking changes (renamed constants, changed defaults) with content migration
- Preserve workspace-specific customizations (downstream modifications allowed)
- Breaking change = any source change that requires downstream files to be modified beyond simple copy (e.g., renamed constants, changed folder structure). Content migration = transformation applied to downstream files during sync to handle breaking changes

**WSKMGMT-FR-17: Roll back workspace settings to previous version**
- Roll back using git history (last committed version of DevRepo NOTES.md)
- Or roll back to a specific version in central storage (template version history)
- Report what changed between current and rolled-back version

**WSKMGMT-FR-18: Check workspace integrity**
- Verify all required constants present in DevRepo NOTES.md
- Verify all required files exist (NOTES.md, PROBLEMS.md, PROGRESS.md, ID-REGISTRY.md, SOPS.md)
- Verify workspace structure matches declared mode (SINGLE-PROJECT, MONOREPO, WORKSPACE)
- Verify agent folder exists and contains specs, workflows, skills subfolders
- Report gaps and incompatibilities

### DEVSYSTEM Area Operations

**WSKMGMT-FR-19: Compare DevSystem against central source**
- Compare `[AGENT_FOLDER]` content against `[DEVSYSTEM_FOLDER]` (or configured prompt system source)
- Report: new files in source, modified files, deleted files, deprecated files
- Use diff scripts from FR-13

**WSKMGMT-FR-20: Update DevSystem from central source**
- Copy new and modified files from source to target
- Delete deprecated files (with confirmation)
- Migrate breaking changes (renamed skills, changed folder structure) with content migration
- Support skill category filtering (not all repos get all skills)
- Use sync scripts from FR-14

**WSKMGMT-FR-21: Roll back DevSystem to previous version**
- Roll back using git history (last committed version of agent folder)
- Or roll back to archived DevSystem version in `_OldDevSystemVersions/`
- Report what changed between current and rolled-back version

**WSKMGMT-FR-22: Check DevSystem integrity**
- Verify agent folder contains required subfolders (specs, workflows, skills)
- Verify all skills in NOTES.md `[SKILL_CATEGORIES]` exist in skills folder
- Verify all skills in skills folder are registered in `[SKILL_CATEGORIES]`
- Verify workflows reference valid skills
- Verify no deprecated files remain
- Report gaps and incompatibilities

### KNOWLEDGE Area Operations

**WSKMGMT-FR-23: Compare knowledge against central source**
- Compare `[KNOWLEDGE_FOLDER]` content against `[KNOWLEDGE_SOURCE_FOLDER]`
- Report: new bundles in source, modified documents, deleted documents
- Use diff scripts from FR-13

**WSKMGMT-FR-24: Update knowledge from central source**
- Copy new and modified knowledge bundles from source to target
- Delete removed bundles (with confirmation)
- Preserve local additions (bundles in target but not in source are kept unless sync policy says otherwise)
- Use sync scripts from FR-14

**WSKMGMT-FR-25: Roll back knowledge to previous version**
- Roll back using git history (last committed version of knowledge folder)
- Report what changed between current and rolled-back version

**WSKMGMT-FR-26: Check knowledge integrity**
- Verify knowledge folder exists if `[KNOWLEDGE_FOLDER]` constant is set
- Verify all bundles referenced in sync policy exist
- Verify no empty bundles (folders with no documents)
- Report gaps and incompatibilities

### Workflow Integration

**WSKMGMT-FR-27: verify.md "Workspace Setup" context**
- New context in `/verify` workflow: "Workspace Setup"
- Detect by: user runs `/verify workspace` or `/verify setup` or context is workspace configuration
- Verifies current workspace or project setup against WORKSPACE-RULES.md, WORKSPACE-GUIDES.md, and templates
- Downstream repo modifications are allowed (customizations are valid)
- Gaps and incompatibilities must be fixed (missing required files, missing constants, broken references)
- Fix actions per gap type: missing constant -> add with template default. Missing required file -> create from template. Broken reference -> report only (requires user judgment). Structural violation -> report only
- All fixes must be reported with what was changed and why
- Uses WORKSPACE-RULES.md as verification checklist source

**WSKMGMT-FR-28: sync.md "Workspace Sync" context**
- New context in `/sync` workflow: "Workspace Sync"
- Detect by: user runs `/sync workspace` or context is workspace-level sync
- Searches for sync policies in this order: 1) downstream repo NOTES.md, 2) CompanyRepo NOTES.md
- If no policy found, uses defaults from workspace constants
- Runs diff using skill's diff scripts
- Shows preview of sync changes
- Uses diff and sync scripts from workspace-management skill

**WSKMGMT-FR-29: sync.md preview/confirm flow**
- After diff preview, prompt user for confirmation
- Confirmation keywords: "yes", "go", "confirmed", "execute", "apply"
- Non-confirmation keywords: "no", "cancel", "abort", "stop"
- If confirmed: execute sync using skill's sync scripts
- If not confirmed: abort, no changes made
- Preview must show: files to add, files to modify, files to delete, files to skip (with reason)

**WSKMGMT-FR-31: SKILL.md entry point**
- YAML frontmatter: `name: workspace-management`, `description`, `compatibility: PowerShell 7+ for diff/sync scripts`
- MUST-NOT-FORGET section (5-8 items): generic paths only, sync before deploy, preserve list check, rollback warning for shared branches, privacy gate, register in NOTES.md
- Intent Lookup: maps 3 areas (WORKSPACE, DEVSYSTEM, KNOWLEDGE) x 4 operations (compare, update, rollback, integrity) to procedures and FR references
- Core Procedures: compare workspace, update from source, rollback, integrity check, multi-repo commit
- References: links to WORKSPACE-GUIDES.md, WORKSPACE-RULES.md, DEV_REPO_NOTES_TEMPLATE.md, PRODUCT_REPO_README_TEMPLATE.md, COMPANY_REPO_NOTES_TEMPLATE.md
- Gotchas: sync timestamp missing triggers full diff, preserve list overrides overwrite rules, rollback on shared branches requires revert commit
- Follows SKILL_RULES.md (all SK-* rules) and SKILL_TEMPLATE.md structure

**WSKMGMT-FR-30: commit.md multi-repo support**
- In WORKSPACE mode, detect changes across all git repos referenced in [WORKSPACE_FILE] (main.code-workspace)
- Commit order: 1) product repo first, 2) dev repo second, 3) all other workspace repos
- For each repo: detect uncommitted changes, analyze by type (feat, fix, docs, test, chore), create conventional commits
- If no changes in a repo, skip silently
- Report committed changes per repo at end
- In SINGLE-PROJECT and MONOREPO modes, behavior is unchanged (single repo commit)
- Must detect and use per-repo git config (user.name, user.email) - do not assume workspace-wide git identity
- All git operations must be explicitly scoped to the target repo using `git -C [repo_path]` or equivalent. Do not rely on current working directory for repo resolution
- If a repo commit fails, report the failure with error message, continue with remaining repos, and summarize partial success at end. Do not roll back already-committed repos
- **Exclude repos not in [WORKSPACE_FILE]**: Linked repos ([LINKED_REPOS]), deploy targets, and any repo not referenced in main.code-workspace are excluded unless [ACTOR] explicitly requests

**WSKMGMT-FR-40: [WORKSPACE_FOLDER] vs [WORKSPACE_FILE] distinction**
- [WORKSPACE_FOLDER] = filesystem path of workspace root directory. Always present.
- [WORKSPACE_FILE] = main.code-workspace file inside [WORKSPACE_FOLDER]. Only in WORKSPACE mode.
- [WORKSPACE_FILE] defines workspace membership by referencing repo folder paths. Repos may be physically outside [WORKSPACE_FOLDER] (e.g., ../ProductRepo)
- Commit scope in WORKSPACE mode = repos referenced in [WORKSPACE_FILE], not repos inside [WORKSPACE_FOLDER]
- DevRepo NOTES.md should define [WORKSPACE_FILE] constant in WORKSPACE mode, omit in SINGLE-PROJECT/MONOREPO
- WORKSPACE-GUIDES.md must explain the distinction with examples
- WORKSPACE-RULES.md must enforce it via WS-CT-04
- DEV_REPO_NOTES_TEMPLATE.md must include [WORKSPACE_FILE] constant with instructions

### Sync Relationship Dimension

**WSKMGMT-FR-32: Add Dimension 4 to devsystem-core.md**
- Add "Dimension 4: Sync Relationship" to Workspace Scenarios section
- Two states: SYNCED, SELF-CONTAINED
- Detection: based on presence of sync markers in NOTES.md
- Orthogonal to existing 3 dimensions

**WSKMGMT-FR-33: Register states in ID-REGISTRY.md**
- Add SYNCED and SELF-CONTAINED to Workspace Context states
- Keep all existing states unchanged

**WSKMGMT-FR-34: Extend /prime with sync relationship detection**
- After detecting dimensions 1-3, detect dimension 4
- Check for sync markers: devsystem-sync.json at target root, [SYNCED_REPOS] in source NOTES.md, [*_SOURCE_FOLDER], [DEVSYSTEM]
- Report all 4 dimensions in final output
- Example: "Mode: WORKSPACE + SINGLE-VERSION + SESSION-MODE + SYNCED"

**WSKMGMT-FR-35: Make sync source constants conditional**
- WS-CT-01 in WORKSPACE-RULES.md must split constants into:
  - Always required (5): [DEV_REPO_FOLDER], [PRODUCT_REPO_FOLDER], [KNOWLEDGE_FOLDER], [SPECS_FOLDER], [PRODUCT_DOCS_FOLDER]
  - Required for SYNCED only (3): [COMPANY_REPO_FOLDER], [KNOWLEDGE_SOURCE_FOLDER], [SPECS_SOURCE_FOLDER]
- SELF-CONTAINED repos pass verify without sync source constants
- SYNCED repos fail verify if sync source constants are missing

**WSKMGMT-FR-36: Update DEV_REPO_NOTES_TEMPLATE.md**
- Mark sync source constants as conditional: "Required if SYNCED, optional if SELF-CONTAINED"
- Add comment explaining how to opt out of sync (remove source constants)
- Sync Sources section header: "## Sync Sources (SYNCED only - remove if SELF-CONTAINED)"

**WSKMGMT-FR-37: Update verify.md Workspace Setup context**
- Step 1: Detect sync relationship (SYNCED or SELF-CONTAINED)
- Step 2: If SYNCED, check all 8 constants (current behavior)
- Step 3: If SELF-CONTAINED, check 5 base constants only (skip sync source constants)
- Step 4: If SELF-CONTAINED, skip sync policy validation
- Report sync relationship in verify output

**WSKMGMT-FR-38: Update SKILL.md Intent Lookup**
- Add intent: "Check if repo is synced or self-contained → Procedure 4 (integrity check)"
- Core Procedures: integrity check must report sync relationship state

**WSKMGMT-FR-39: Update WORKSPACE-GUIDES.md**
- Add section: "When to use sync vs self-contained"
- Explain: SYNCED repos receive updates from upstream, SELF-CONTAINED repos manage locally
- Explain: Self-contained is valid for standalone projects, prototypes, or repos with custom rules
- Explain: Switching from SELF-CONTAINED to SYNCED = add source constants and run sync

### Workspace Creation

**WSKMGMT-FR-41: WORKSPACE_CREATION_QUESTIONNAIRE.md**
- Interactive questionnaire for creating new single-repo and multi-repo workspaces
- 7 sections: Workspace Mode, Product Repo, Dev Repo, Version Strategy, Sync Sources, Release Configuration, Skill Categories
- Each question shows default value in brackets and impact description explaining consequences
- Conditional sections: SINGLE-PROJECT skips Product Repo, Sync Sources, Skill Categories sections
- Output section lists exact files to generate per workspace mode
- References DEV_REPO_NOTES_TEMPLATE.md and PRODUCT_REPO_README_TEMPLATE.md for file generation
- Guide is a skill resource file (not a template) - contains questionnaire logic, not document skeleton
- Privacy gate compliant: all placeholders generic (e.g., [myapp], [appname])

**WSKMGMT-FR-42: workspace-create.md workflow**
- Thin workflow entry point: references WORKSPACE_CREATION_QUESTIONNAIRE.md for questionnaire content
- Does not replicate questions in workflow body (Workflow-Skill Separation rule)
- Frontmatter: description, auto_execution_mode
- Goal and Why per WF-HD-02
- MUST-NOT-FORGET section per WF-ST-03
- Prerequisites: target folder must not already be a workspace (no existing NOTES.md or !NOTES.md)
- Context branching: SINGLE-PROJECT vs WORKSPACE (determined by Section 1 answer)
- Steps: load guide, present questions section by section, collect answers, generate files from templates, run integrity check
- No confirmation gates - workspace creation is non-destructive per WF-EX-01
- Verification section per WF-ST-04: run `/verify workspace` after creation
- Follows WORKFLOW_RULES.md (all WF-* rules) and WORKFLOW_TEMPLATE.md structure

**WSKMGMT-FR-43: Workspace creation procedure in SKILL.md**
- Add intent to Intent Lookup: "Create a new workspace -> WORKSPACE_CREATION_QUESTIONNAIRE.md questionnaire"
- Add WORKSPACE_CREATION_QUESTIONNAIRE.md to References list
- No new Core Procedure needed - creation flow lives in workflow, guide provides questionnaire content

### JSON-Based Sync Configuration

**WSKMGMT-FR-44: devsystem-sync.json (target-side, single source of truth)**
- Machine-readable JSON file at target `[WORKSPACE_FOLDER]` root (not inside `.devin/`)
- Single source of truth for all sync configuration — no separate bundle file at source
- Each source entry carries its own complete sync configuration:
  - `source`: relative path to source repo (e.g., `../IPPS/DevSystemV4.3`)
  - `selected_bundles`: array of bundle names this target wants from this source
  - `bundles`: bundle definitions with include/exclude glob patterns (what was previously in sync-bundles.json at source)
  - `include`: source-level whitelist of syncable paths
  - `exclude`: source-level global removal patterns
  - `deprecated`: files/folders marked for deletion at target
  - `never_overwrite`: glob patterns for files protected from overwrite and deletion
- `last_sync` timestamp written by sync script after execution
- Replaces [SKILL_CATEGORIES] prose in NOTES.md, [LINKED_REPOS] in NOTES.md, hardcoded arrays in deploy-to-all-repos.md, and the previously proposed sync-bundles.json at source
- New repos added by creating devsystem-sync.json with desired sources and bundles - no source-side changes needed
- Privacy gate compliant: no real paths or identifiers in bundle definitions (use generic examples)

**WSKMGMT-FR-45: Source repo synced repos reference**
- Source repo maintains a list of all repos it syncs to, using RELATIVE paths only
- Referenced in NOTES.md or a simple JSON file at source root
- Example: `../Lana-V2-Dev`, not `e:\Dev\Lana-V2-Dev`
- Source does NOT contain bundle definitions or sync configuration — that lives entirely in target's devsystem-sync.json
- Source list is informational only (for `/sync to targets` workflows to know which repos to push to)
- Enables portability across machines and drive layouts

**WSKMGMT-FR-46: Single sync.ps1 script**
- ONE PowerShell script in workspace-management skill (not two separate scripts)
- Two modes: `-diff` (preview, no changes) and `-execute` (apply changes)
- Parameters: `-sources` (JSON array or single string), `-targets` (JSON array or single string), `-configs` (JSON array or single string of config file paths), `-output-file` (optional filepath)
- Reads devsystem-sync.json from each target for ALL sync configuration: bundle definitions, selected bundles, include/exclude refiners, never_overwrite, deprecated
- Does NOT read any config from source — source is purely a content provider
- Evaluation order (per source entry in target config): source include → source exclude → bundle include (union of all selected bundles) → bundle exclude (union) → target never_overwrite → deprecated
- `-diff` mode: produces list of additions, changes, deletions to output file or console
- `-execute` mode: copies new and changed files, deletes deprecated files, writes last_sync timestamp
- If `-output-file` present: full report goes to file, console just summarizes numbers (X added, Y changed, Z deleted)
- If `-output-file` absent: full report outputs to console
- All parameters accept JSON arrays OR single strings (e.g., `-sources "path1"` or `-sources '["path1","path2"]'`)
- Replaces workspace_sync_template.ps1, workspace_diff_template.ps1, and hardcoded sync logic in deploy-to-all-repos.md

**WSKMGMT-FR-47: Removed (merged into FR-46)**
- diff.ps1 is not a separate script - diff mode is `sync.ps1 -diff`
- This FR is intentionally removed; FR-46 covers both diff and execute in a single script

**WSKMGMT-FR-48: deploy-to-all-repos.md replacement**
- `deploy-to-all-repos.md` is deleted, not refactored
- Its functionality is absorbed by `sync.md` workflow Workspace Sync context (FR-49)
- No standalone deployment workflow exists - all deployment is sync-driven
- Existing [LINKED_REPOS] in NOTES.md becomes obsolete and is removed. [SKILL_CATEGORIES] is retained for workspace integrity checks (WS-ST-02, WS-ST-03)
- SOPS.md SOP 4 (deploy procedure) updated to reference `/sync workspace` instead of `deploy-to-all-repos.md`

**WSKMGMT-FR-49: sync.md Workspace Sync context update**
- Existing `sync.md` Workspace Sync section updated to use `sync.ps1` from workspace-management skill
- Replaces references to `workspace_diff_template.ps1` and `workspace_sync_template.ps1`
- Sync config read from `devsystem-sync.json` at target `[WORKSPACE_FOLDER]` root
- For each source in config: run `sync.ps1 -diff -sources <paths> -targets <paths> -configs <config>` for preview, then `sync.ps1 -execute` for apply
- Multi-source, multi-target, multi-config support in a single script call
- No hardcoded paths, skill categories, or target lists in the workflow itself
- Preview/confirm flow preserved: diff first, show results, confirm, then sync
- Auto-execute on confirmation keywords: yes, go, do, execute, confirmed

**WSKMGMT-FR-50: rules → specs folder rename**
- `[WORKSPACE_FOLDER]\rules` renamed to `[WORKSPACE_FOLDER]\specs`
- `\specs` contains all SPEC, IMPL, TEST files
- `\specs\sops` contains advanced SOPs referenced in SOPS.md
- `\specs\guides` contains guides and how-tos (e.g., UX design guidelines)
- All references to `rules/` in DevSystem files, NOTES.md, sync configs, and workflows updated to `specs/`
- [RULES_FOLDER] constant renamed to [SPECS_FOLDER] in workspace templates
- [RULES_SOURCE_FOLDER] constant renamed to [SPECS_SOURCE_FOLDER]

**WSKMGMT-FR-51: Settings sync use cases**
- `/sync workspace settings from repo xyz` — compares NOTES.md and devsystem-sync.json from repo xyz, merges or replicates them into current repo
- `/sync workspace settings to repo xyz` — compares NOTES.md and devsystem-sync.json from current repo, merges or replicates them into target repo xyz
- `/sync sync settings from repo xyz` — compares and replicates ONLY devsystem-sync.json (not NOTES.md) into current repo
- `/sync sync settings to repo xyz` — compares and replicates ONLY devsystem-sync.json into target repo xyz
- Settings sync uses sync.ps1 with config files as both source and target content
- Merge strategy: target files win for fields that exist in both; source-only fields are added

**WSKMGMT-FR-52: Knowledge sync use cases**
- `/sync knowledge from source` — reads knowledge source from devsystem-sync.json, runs `sync.ps1 -diff`, previews, auto-executes on confirm
- `/sync knowledge to targets` — reads target repos from source NOTES.md synced repos list, runs `sync.ps1 -diff` for each target, previews, auto-executes on confirm
- Knowledge folder structure preserved: subfolders like `AI-Standards/`, `Anthropic/` synced as-is
- Knowledge content is filtered by bundle include/exclude rules in target's devsystem-sync.json

**WSKMGMT-FR-53: Specs sync use cases**
- `/sync specs from source` — reads specs source from devsystem-sync.json, runs `sync.ps1 -diff`, previews, auto-executes on confirm
- `/sync specs to targets` — reads target repos from source NOTES.md synced repos list, runs `sync.ps1 -diff` for each target, previews, auto-executes on confirm
- Specs folder structure preserved: subfolders like `sops/`, `guides/` synced as-is
- Specs content is filtered by bundle include/exclude rules in target's devsystem-sync.json

**WSKMGMT-FR-54: Source repo relative path references**
- Source repo NOTES.md only references downstream repos by RELATIVE paths
- Example: `../Lana-V2-Dev` not `e:\Dev\Lana-V2-Dev`
- Enables portability across different machines and drive layouts
- sync.ps1 resolves relative paths against source repo root

## 5. Non-Functional Requirements

**WSKMGMT-NFR-01: Performance - Diff execution time**
- Diff scripts must complete within 10 seconds for workspaces with up to 500 files
- Verification method: timed execution against a WORKSPACE-mode workspace with 500+ files

**WSKMGMT-NFR-02: Reliability - Sync safety**
- Sync scripts must never delete files without showing them in preview first
- Sync scripts must create backup of overwritten files before writing
- Diff preview must mark files modified locally since last sync (target LastWriteTime > `last_sync` in `devsystem-sync.json`) as 'LOCALLY_MODIFIED - will be overwritten'
- Verification method: dry-run preview must list all deletions and locally modified files before any execute mode runs

**WSKMGMT-NFR-03: Usability - Error messages**
- Diff and sync scripts must report clear, actionable error messages
- Missing constants: name the constant and where it should be defined
- Missing folders: name the folder and expected path
- Verification method: manual review of error output for each failure scenario

**WSKMGMT-NFR-04: Portability - Cross-workspace compatibility**
- Skill must work for SINGLE-PROJECT, MONOREPO, and WORKSPACE modes
- Scripts must not assume presence of ProductRepo or CompanyRepo (optional in SINGLE-PROJECT)
- Templates must indicate which sections are required vs optional per workspace mode
- Verification method: test against a WORKSPACE-mode workspace and a SINGLE-PROJECT workspace

**WSKMGMT-NFR-05: Maintainability - Generic design**
- No hardcoded paths in scripts or rules
- All paths derived from workspace constants in DevRepo NOTES.md
- Skill files contain no project-specific data (privacy gate compliance)
- Verification method: grep for hardcoded paths in skill folder

**WSKMGMT-NFR-06: Reliability - Sync policy validation**
- Sync scripts must validate SyncPolicy fields before execution: verify source and target folders exist, direction is valid enum (downstream or upstream), filter patterns are valid glob or regex
- Report validation errors before starting sync
- Verification method: test with invalid SyncPolicy entries (missing folder, invalid direction, malformed filter)

**WSKMGMT-NFR-07: Backward compatibility (sync relationship)**
- Existing repos with sync markers are automatically SYNCED - no migration needed
- Existing repos without sync markers are automatically SELF-CONTAINED - no action needed
- No repo needs to explicitly declare its sync relationship
- Verification method: run /prime on existing repos, confirm correct detection

**WSKMGMT-NFR-08: Detection determinism (sync relationship)**
- Detection must be deterministic - same NOTES.md content always yields same result
- No heuristic or fuzzy matching - presence of markers is binary
- Verification method: test with NOTES.md containing markers and without

## 6. Design Decisions

**WSKMGMT-DD-01:** New workspace mode `WORKSPACE` added to Dimension 1. Rationale: The DevSystem source repository itself is a workspace with multiple independent repos, not a monorepo. The existing `SINGLE-PROJECT` and `MONOREPO` modes do not cover this pattern.

**WSKMGMT-DD-02:** IMPL-ISOLATED extended to include `T##_` and `S##_` folders as valid output locations. Rationale: Topic and Step folders already exist as session subfolders and are used for isolated work - they should be explicitly recognized as valid IMPL-ISOLATED targets.

**WSKMGMT-DD-03:** Product/Dev repo separation is a first-class WORKSPACE pattern. The workspace root is the DevRepo, which contains `main.code-workspace` referencing the ProductRepo. Rationale: Real-world workspaces demonstrate this pattern - dev repo has specs/sessions/evals/knowledge, product repo has shipped code. Keeps product small, protects proprietary IP.

**WSKMGMT-DD-04:** Workspace constants tracked in DevRepo NOTES.md. New constants: `[DEV_REPO_FOLDER]`, `[PRODUCT_REPO_FOLDER]`, `[COMPANY_REPO_FOLDER]`, `[KNOWLEDGE_FOLDER]`, `[KNOWLEDGE_SOURCE_FOLDER]`, `[SPECS_FOLDER]`, `[SPECS_SOURCE_FOLDER]`, `[PRODUCT_DOCS_FOLDER]`. Rationale: Centralizes workspace configuration for the skill's compare/update/rollback/integrity operations.

**WSKMGMT-DD-05:** Three sync sources for WORKSPACE mode: (1) Prompt System from DevSystem source, (2) Knowledge from Company folder, (3) Specs from Company folder. Each supports downstream and upstream sync. Rationale: Different content types have different sources and sync directions.

**WSKMGMT-DD-06:** Workspace Management Skill contains GRUC files plus templates plus diff/sync scripts. Checks are embedded in the `/verify` workflow (FR-27 "Workspace Setup" context) rather than a separate WORKSPACE-CHECKS.md file. Rationale: GRUC pattern (Guides + Rules + Checks) extended with templates and scripts. Checks live in verify.md because workspace verification is workflow-triggered (`/verify workspace`), not skill-internal. Templates provide structure, scripts provide automation, guides provide understanding, rules provide verification.

**WSKMGMT-DD-07:** `/verify` workflow gets a new context: "Workspace Setup". Rationale: `/verify` already has context-specific sections (Cross-Document, INFO, SPEC, IMPL, Code, TEST, Session, Workflow, Skill, Template, etc.) - adding workspace setup as a new context is the natural integration point. Downstream modifications are allowed because workspaces legitimately customize their setup.

**WSKMGMT-DD-08:** `/sync` workflow gets a new context: "Workspace Sync" with policy lookup and preview/confirm flow. Rationale: `/sync` already has context-specific sections and a preview/execute pattern - adding workspace sync as a new context reuses the existing workflow structure. Policy lookup order (downstream first, CompanyRepo second) ensures local customizations take precedence over central defaults.

**WSKMGMT-DD-09:** `/commit` workflow extended for WORKSPACE mode. In multi-repo workspace mode, commits changes across multiple git repos in order: 1) product repo first, 2) dev repo second, 3) all other workspace repos. Rationale: Product repo changes (code, tests) are the primary deliverable and should be committed first. Dev repo changes (specs, sessions, knowledge) are secondary. Other repos (Company, linked repos) are tertiary. Dev repo is committed second because it contains documentation of the product changes. Temporary inconsistency (product committed, dev not) is acceptable because dev repo content is not a runtime dependency. This ordering ensures product changes are not left uncommitted if dev repo commit fails.

**WSKMGMT-DD-10:** Diff and sync scripts (FR-13, FR-14) are generic, independent of any project-specific deployment script. Scripts read source and target from workspace constants, read sync policy from NOTES.md, support 3 sync sources (Prompt System, Knowledge, Specs), and support upstream and downstream directions. The scripts are the foundation for `/sync workspace` context. Rationale: Project-specific deployment scripts solve 80% of the problem but are not reusable. Generic scripts that read all configuration from workspace constants work for any DevSystem workspace without modification.

**WSKMGMT-DD-11:** Workspace creation uses a guide file (WORKSPACE_CREATION_QUESTIONNAIRE.md) for questionnaire content and a thin workflow (workspace-create.md) for execution flow. Rationale: Workflow-Skill Separation rule states workflows are thin entry points, skills hold knowledge. The questionnaire is knowledge (what to ask, what defaults to offer, what impact to explain) - it belongs in the skill. The workflow is the execution wrapper (load guide, present questions, generate files, verify). This mirrors how session-new.md references session-management skill templates.

**WSKMGMT-DD-12:** Two states only (SYNCED, SELF-CONTAINED), not three. A repo is either part of a dependency tree or it isn't. No "partial sync" state. Rationale: Simplicity. If a repo syncs knowledge but not specs, it still has sync markers and is SYNCED. The sync policy handles which sources to sync.

**WSKMGMT-DD-13:** Auto-detection, not declaration. Sync relationship is inferred from NOTES.md content, not from an explicit field. Rationale: Zero migration cost. Existing repos are automatically classified correctly. Adding an explicit `[SYNC_RELATIONSHIP]: SYNCED` field would require all existing repos to update.

**WSKMGMT-DD-14:** Sync source constants are conditional, not base constants. [COMPANY_REPO_FOLDER], [KNOWLEDGE_SOURCE_FOLDER] and [SPECS_SOURCE_FOLDER] are only required for SYNCED repos. Rationale: Self-contained repos don't have upstream sources. Requiring these constants would force self-contained repos to define meaningless paths.

**WSKMGMT-DD-15:** Dimension 4 is orthogonal to Dimension 1. A SINGLE-PROJECT repo can be SYNCED (syncs from DevSystem) or SELF-CONTAINED (standalone). A WORKSPACE repo can be SYNCED (full dependency tree) or SELF-CONTAINED (multi-repo but no external sync). Rationale: Sync relationship and project structure are independent concerns.

**WSKMGMT-DD-16:** [DEVSYSTEM] reference in NOTES.md counts as a sync marker. Even if a repo doesn't have devsystem-sync.json or [*_SOURCE_FOLDER], referencing [DEVSYSTEM] means it syncs from a DevSystem source. Rationale: [DEVSYSTEM] is the primary sync marker - it identifies the upstream DevSystem version.

**WSKMGMT-DD-17:** [WORKSPACE_FOLDER] and [WORKSPACE_FILE] are distinct concepts. [WORKSPACE_FOLDER] is the filesystem path. [WORKSPACE_FILE] is the main.code-workspace file that defines workspace membership. Repos in the workspace file may be outside the workspace folder. Commit scope is determined by [WORKSPACE_FILE], not by physical location inside [WORKSPACE_FOLDER]. Rationale: GLOB-FL-041 showed that conflating these concepts leads to incorrectly excluding ProductRepo/CompanyRepo from commit scope, or incorrectly including linked repos. The distinction must be explicit in guides, rules, and templates.

**WSKMGMT-DD-18:** Sync configuration lives entirely at target in `devsystem-sync.json` at `[WORKSPACE_FOLDER]` root. No bundle definitions or sync config at source. Rationale: Previous architecture had sync-bundles.json at source defining what is available, and sync-config.json at target declaring what it wants. This created a split-brain: source had to know about bundle definitions, target had to know about source. The corrected architecture puts everything in one file at target — each source entry carries its own complete sync configuration (bundle definitions, include/exclude refiners, deprecated, never_overwrite). Source only maintains a list of relative paths to repos it syncs to (for push operations). This is true single source of truth: target owns its sync config, source is purely a content provider. Adding a new repo requires zero source-side changes. Changing bundles requires editing only the target's devsystem-sync.json.

**WSKMGMT-DD-19:** Single sync.ps1 script with -diff and -execute modes instead of separate diff.ps1 and sync.ps1. Rationale: The diff and execute operations share identical config reading, filtering, and evaluation logic. Splitting them into two scripts duplicates this logic and risks divergence. A single script with mode flag is simpler, has fewer files to maintain, and ensures diff preview always matches execute behavior. Array parameters (-sources, -targets, -configs) enable batch operations in a single call, reducing script invocations for multi-target sync.

**WSKMGMT-DD-20:** Source repo only references downstream repos by relative paths in its synced repos list. Rationale: Absolute paths (e.g., `e:\Dev\Lana-V2-Dev`) are machine-specific and break when repos are cloned to different locations. Relative paths (e.g., `../Lana-V2-Dev`) are portable and work across machines, drive layouts, and CI environments. sync.ps1 resolves relative paths against the source repo root at runtime. The source's synced repos list is informational — it tells `/sync to targets` workflows which repos to push to. The actual sync configuration (bundles, filters, never_overwrite) lives in each target's devsystem-sync.json.

**WSKMGMT-DD-21:** `rules` folder renamed to `specs` with subfolders `sops/` and `guides/`. Rationale: The `rules` folder name is misleading — it contains specifications, implementation plans, test plans, SOPs, and guides, not just rules. The `specs` name better reflects the content. Subfolders `sops/` and `guides/` provide structure for advanced SOPs (referenced by SOPS.md) and how-to guides (e.g., UX design guidelines).

## 7. Implementation Guarantees

**WSKMGMT-IG-01:** Existing SINGLE-PROJECT and MONOREPO workspace detection in `/prime` must continue to work unchanged after WORKSPACE mode is added.

**WSKMGMT-IG-02:** Existing IMPL-ISOLATED behavior for `[SESSION_FOLDER]/` and `[SESSION_FOLDER]/poc/` must continue to work unchanged after T##/S## folders are added.

**WSKMGMT-IG-03:** Sync scripts must never modify files in the central source during downstream sync (source is read-only during downstream).

**WSKMGMT-IG-04:** Verify must not fail on intentional downstream customizations (e.g., extra constants in NOTES.md, additional knowledge bundles, custom SOPs).

**WSKMGMT-IG-05:** All skill files must pass the privacy gate - no real identifiers, addresses, names, or project-specific data in any skill file.

**WSKMGMT-IG-06:** Templates must clearly mark required vs optional sections so agents can create valid workspace files without guessing.

**WSKMGMT-IG-07:** Rollback is intended for local or private branches. For shared or public branches, user should create a revert commit manually. Warning must be displayed before rollback: ensure no other contributors have pulled the current version before rolling back.

**WSKMGMT-IG-08:** Existing /prime detection for dimensions 1-3 must continue to work unchanged after dimension 4 is added.

**WSKMGMT-IG-09:** Existing SYNCED repos must not fail /verify after conditional constants are introduced - they already have sync source constants.

**WSKMGMT-IG-10:** SELF-CONTAINED repos that currently fail /verify for missing sync source constants must pass after this change is implemented.

**WSKMGMT-IG-11:** `deploy-to-all-repos.md` is replaced by `sync.md` workspace context. Existing repos with `[LINKED_REPOS]` in NOTES.md must migrate to `devsystem-sync.json` at `[WORKSPACE_FOLDER]` root - a migration script or procedure must be provided. Absolute paths in `[LINKED_REPOS]` must be converted to relative paths per FR-54.

## 8. Key Mechanisms

### Workspace Mode Detection

```
Detect workspace mode:
├─> main.code-workspace file exists in workspace root?
│   ├─ Yes -> WORKSPACE mode
│   │   └─> Parse .code-workspace JSON for folder list
│   │       └─> First folder (".") = DevRepo
│   │       └─> Other folders = ProductRepo(s) or additional repos
│   └─ No
│       ├─> Multiple project subfolders in workspace?
│       │   ├─ Yes -> MONOREPO
│       │   └─ No -> SINGLE-PROJECT
```

### Sync Config Resolution

```
Resolve sync config:
├─> Check target [WORKSPACE_FOLDER] root for devsystem-sync.json?
│   ├─ Found -> Read devsystem-sync.json
│   │   └─> Each source entry defines: source (relative path), selected_bundles, bundles, include, exclude, deprecated, never_overwrite
│   └─ Not found
│       └─> No sync configured for this repo (SELF-CONTAINED)
```

### Diff and Sync Flow

```
User runs /sync workspace (or /sync knowledge, /sync specs)
├─> Read devsystem-sync.json from target [WORKSPACE_FOLDER] root
├─> For each source in config:
│   ├─> All config from devsystem-sync.json source entry (bundles, refiners, deprecated, never_overwrite)
│   ├─> Run sync.ps1 -diff -sources <source> -targets <target> -configs devsystem-sync.json
│   └─> Collect diff results (add/overwrite/delete/excluded)
├─> Show preview: files to add, modify, delete, skip (with reason)
├─> Prompt for confirmation
│   ├─> Confirmed -> Run sync.ps1 -execute with same params
│   │   ├─> Create backups of files to overwrite
│   │   ├─> Execute copy/delete operations
│   │   ├─> Write last_sync timestamp to devsystem-sync.json
│   │   └─> Report results
│   └─> Not confirmed -> Abort, no changes
```

### Sync Relationship Detection

```
Detect sync relationship:
├─> Check for sync markers:
│   ├─> devsystem-sync.json at [WORKSPACE_FOLDER] root? → has sync config
│   ├─> [SYNCED_REPOS] in source NOTES.md? → has downstream targets
│   ├─> [KNOWLEDGE_SOURCE_FOLDER] defined? → has knowledge upstream
│   ├─> [SPECS_SOURCE_FOLDER] defined? → has specs upstream
│   └─> [DEVSYSTEM] or [DEVSYSTEM_FOLDER] referenced? → has DevSystem upstream
├─> Any marker found?
│   ├─ Yes → SYNCED
│   └─ No → SELF-CONTAINED
```

### Verify with Conditional Constants

```
/verify workspace
├─> Detect sync relationship
│   ├─> SYNCED
│   │   ├─> Check all 8 constants (5 base + 3 sync source)
│   │   ├─> Check devsystem-sync.json exists at [WORKSPACE_FOLDER] root
│   │   └─> Check source paths in devsystem-sync.json resolve to valid paths
│   └─> SELF-CONTAINED
│       ├─> Check 5 base constants only
│       ├─> Skip sync source constant checks
│       └─> Skip devsystem-sync.json validation
```

### Verify Workspace Setup Flow

```
User runs /verify workspace (or /verify setup)
├─> Read WORKSPACE-RULES.md from skill folder
├─> Detect workspace mode (SINGLE-PROJECT, MONOREPO, WORKSPACE)
├─> Read DevRepo NOTES.md for workspace constants
├─> For each rule in WORKSPACE-RULES.md:
│   ├─> Check rule against current workspace state
│   ├─> Downstream modification? -> Pass (allowed)
│   ├─> Gap or incompatibility? -> Flag for fix
│   └─> Compliant? -> Pass
├─> Compare workspace files against templates
│   ├─> DevRepo NOTES.md vs DEV_REPO_NOTES_TEMPLATE.md
│   ├─> ProductRepo README.md vs PRODUCT_REPO_README_TEMPLATE.md (if ProductRepo exists)
│   └─> CompanyRepo NOTES.md vs COMPANY_REPO_NOTES_TEMPLATE.md (if CompanyRepo exists)
├─> Report: passes, gaps, incompatibilities
└─> Fix gaps and incompatibilities immediately
```

## 9. Action Flow

### Workspace Sync (downstream)

```
/sync workspace
├─> Read devsystem-sync.json from target [WORKSPACE_FOLDER] root
├─> For each source in config:
│   ├─> Run sync.ps1 -diff -sources <source> -targets <target> -configs devsystem-sync.json
│   └─> Collect diff results (add/overwrite/delete/locally-modified/excluded)
├─> Show preview: files to add, modify, delete, skip (with reason)
├─> Prompt for confirmation
│   ├─> Confirmed -> Run sync.ps1 -execute with same params
│   │   ├─> Execute copy/delete operations
│   │   ├─> Write last_sync timestamp to devsystem-sync.json
│   │   └─> Report results
│   └─> Not confirmed -> Abort, no changes
```

### Workspace Sync (upstream)

```
/sync workspace upstream
├─> Upstream sync = run sync.ps1 with swapped -sources and -targets parameters
├─> The target repo becomes the source, the original source becomes the target
├─> Config is read from the other repo's devsystem-sync.json
├─> Same diff/confirm/execute flow as downstream
```

### Workspace Verify

```
/verify workspace
├─> Detect workspace mode
├─> Read WORKSPACE-RULES.md
├─> Check required files per workspace mode
│   ├─> DevRepo: NOTES.md, PROBLEMS.md, PROGRESS.md, ID-REGISTRY.md
│   ├─> ProductRepo (if exists): README.md
│   └─> CompanyRepo (if exists): NOTES.md
├─> Check workspace constants in DevRepo NOTES.md
│   └─> Each required constant present and resolves to valid path?
├─> Check agent folder structure
│   └─> specs/, workflows/, skills/ subfolders exist?
├─> Compare against templates
│   ├─> Missing required sections?
│   └─> Incompatible structure?
├─> Report and fix
```

### Workspace Rollback

```
/verify workspace rollback [area]
├─> area = WORKSPACE
│   ├─> Show recent committed versions of DevRepo NOTES.md
│   ├─> User selects version
│   └─> Restore selected version
├─> area = DEVSYSTEM
│   ├─> Option A: Show recent committed versions of agent folder
│   ├─> Option B: List _OldDevSystemVersions/ archives
│   └─> User selects -> restore from git or archive
├─> area = KNOWLEDGE
│   ├─> Show recent committed versions of knowledge folder
│   └─> User selects version -> restore selected version
```

### Multi-Repo Commit (WORKSPACE mode)

```
/commit (in WORKSPACE mode)
├─> Detect workspace mode (WORKSPACE -> multi-repo)
├─> Parse main.code-workspace for repo list
├─> For each repo in commit order:
│   ├─> 1) ProductRepo: detect uncommitted changes
│   │   ├─> No changes? -> Skip silently
│   │   ├─> Changes? -> Analyze by type (feat, fix, docs, test, chore)
│   │   └─> Create conventional commits per @skills:git-conventions
│   ├─> 2) DevRepo: detect uncommitted changes
│   │   ├─> No changes? -> Skip silently
│   │   ├─> Changes? -> Analyze by type
│   │   └─> Create conventional commits
│   └─> 3) Other repos (Company, linked repos): detect uncommitted changes
│       ├─> No changes? -> Skip silently
│       ├─> Changes? -> Analyze by type
│       └─> Create conventional commits
└─> Report: committed changes per repo
```

## 10. Data Structures

### Workspace Constants (in DevRepo NOTES.md)

```
# Always required (5):
[DEV_REPO_FOLDER]: [WORKSPACE_FOLDER]
[PRODUCT_REPO_FOLDER]: [WORKSPACE_FOLDER]\..\[ProductRepoName]
[KNOWLEDGE_FOLDER]: [DEV_REPO_FOLDER]\knowledge
[SPECS_FOLDER]: [DEV_REPO_FOLDER]\specs
[PRODUCT_DOCS_FOLDER]: [PRODUCT_REPO_FOLDER]\docs

# Required for SYNCED only (3):
[COMPANY_REPO_FOLDER]: [WORKSPACE_FOLDER]\..\Company
[KNOWLEDGE_SOURCE_FOLDER]: [COMPANY_REPO_FOLDER]\knowledge
[SPECS_SOURCE_FOLDER]: [COMPANY_REPO_FOLDER]\specs
```

### Sync Config (devsystem-sync.json at [WORKSPACE_FOLDER] root)

Replaced by `devsystem-sync.json` — see data structure above. The old `[SYNC_POLICY]` section in NOTES.md is obsolete and removed per FR-44 and FR-48.

### Diff Report Structure

```
Diff Report: [Source] vs [Target]
├─> New in source (to add):
│   ├─> path/to/new-file.md
│   └─> ...
├─> Modified (content differs):
│   ├─> path/to/changed-file.md
│   └─> ...
├─> Deleted (in target, not in source):
│   ├─> path/to/removed-file.md
│   └─> ...
└─> Skipped (filtered out):
    ├─> path/to/skipped-file.md (reason: excluded by filter)
    └─> ...
```

### Skill Categories (in DevRepo NOTES.md)

```
[SKILL_CATEGORIES]
- Development: workspace-management, session-management, write-documents, coding-conventions
- Research: deep-research, youtube-downloader
- Deployment: hosting, deploy
- Utilities: image-tools, pdf-tools, git, github
```

### Source repo synced repos list (in NOTES.md or simple JSON at source root)

```
[SYNCED_REPOS]
- ../Lana-V2-Dev
- ../USTVA
- ../OpenAI-BackendTools
```

### devsystem-sync.json (target-side, at [WORKSPACE_FOLDER] root — single source of truth)

```json
{
  "sources": [
    {
      "source": "../IPPS/DevSystemV4.3",
      "selected_bundles": ["Development"],
      "bundles": {
        "Development": {
          "include": ["skills/coding-conventions", "skills/git", "skills/write-documents", "workflows/*", "specs/*"],
          "exclude": ["skills/google-account", "skills/travel-info", "workflows/conversation-start.md", "workflows/conversation-update.md"]
        },
        "Personal": {
          "include": ["skills/google-account", "skills/travel-info", "workflows/conversation-start.md", "workflows/conversation-update.md"],
          "exclude": []
        }
      },
      "include": ["skills/*", "workflows/*", "specs/*"],
      "exclude": ["__pycache__/*", "*.pyc", "skills/llm-evaluation/model-sources/*"],
      "deprecated": ["specs/commit-rules.md", "workflows/go-autonomous.md", "skills/edird-phase-model"],
      "never_overwrite": ["specs/sops/project-release.md"]
    },
    {
      "source": "../Company/knowledge",
      "selected_bundles": ["all"],
      "bundles": {
        "all": {
          "include": ["*"],
          "exclude": []
        }
      },
      "include": ["*"],
      "exclude": [],
      "deprecated": [],
      "never_overwrite": []
    }
  ],
  "last_sync": "2026-09-06T13:20:00"
}
```

### sync.ps1 usage examples

```powershell
# Diff mode - preview to console
sync.ps1 -diff -sources "../IPPS/DevSystemV4.3" -targets "." -configs "devsystem-sync.json"

# Diff mode - output to file, console summarizes
sync.ps1 -diff -sources "../IPPS/DevSystemV4.3" -targets "." -configs "devsystem-sync.json" -output-file "sync-report.txt"

# Execute mode - apply changes
sync.ps1 -execute -sources "../IPPS/DevSystemV4.3" -targets "." -configs "devsystem-sync.json"

# Multi-target batch
sync.ps1 -diff -sources '["../IPPS/DevSystemV4.3"]' -targets '["../Lana-V2-Dev", "../USTVA"]' -configs '["devsystem-sync.json"]'
```

### main.code-workspace Structure

```json
{
  "folders": [
    { "path": "." },
    { "path": "../ProductRepoName" }
  ]
}
```

## 11. User Actions

N/A: This is a skill specification, not a UI specification. User actions are workflow invocations (`/verify workspace`, `/sync workspace`) defined in the workflow integration FRs.

## 12. UX Design

N/A: No UI components. All interaction is via CLI/workflow commands and console output.

## 13. Logging Requirements

**Applicable logging types:**
- [x] User-Facing (UF) - `LOGGING-RULES-USER-FACING.md`
- [ ] App-Level (AP) - N/A: no server/service
- [x] Script-Level (SC) - `LOGGING-RULES-SCRIPT-LEVEL.md`

**User-Facing (UF) logging:**
- **Audience**: Developer running workspace verify or sync
- **Goal**: Understand what differs, what will change, what was changed
- **Key operations**: diff preview, sync execution, verify results, rollback

**Script-Level (SC) logging:**
- **Audience**: Developer debugging failed sync or verify
- **Goal**: Trace which files were compared, which failed, why
- **Key operations**: diff comparison, file copy/delete, rule checking

**Expected output for diff preview:**
```
=============================== START: WORKSPACE SYNC PREVIEW ===============================
[2026-09-06 13:35:00]

Syncing from '../IPPS/DevSystemV4.3' to '.'...
  Reading 'devsystem-sync.json'...
    OK.
  Comparing files...
    [ 1 / 3 ] Adding 'skills/workspace-management/SKILL.md'...
    [ 2 / 3 ] Adding 'skills/workspace-management/WORKSPACE-GUIDES.md'...
    [ 3 / 3 ] Adding 'skills/workspace-management/WORKSPACE-RULES.md'...
    3 new files found.
  Comparing modified files...
    [ 1 / 2 ] 'specs/devsystem-core.md' differs...
    [ 2 / 2 ] 'workflows/verify.md' differs...
    2 modified files found.
  Checking deprecated files...
    0 deprecated files found.
  Checking never-overwrite files...
    1 file protected: 'specs/sops/project-release.md'

Summary: 3 add, 2 modify, 0 delete, 1 skip, 45 unchanged.
RESULT: CHANGES FOUND
================================ END: WORKSPACE SYNC PREVIEW =================================
[2026-09-06 13:35:02] (2.0 secs)

Confirm sync? (yes/go/confirmed to execute, no/cancel to abort)
```

**Expected output for verify:**
```
================================ START: WORKSPACE VERIFY =================================
[2026-09-06 13:35:00]

Verifying workspace 'DevRepo' (WORKSPACE mode)...
  Checking required files...
    [ 1 / 5 ] 'NOTES.md'...
      OK.
    [ 2 / 5 ] 'PROBLEMS.md'...
      OK.
    [ 3 / 5 ] 'PROGRESS.md'...
      OK.
    [ 4 / 5 ] 'ID-REGISTRY.md'...
      OK.
    [ 5 / 5 ] 'SOPS.md'...
      OK.
    5 files found.
  Checking workspace constants...
    [ 1 / 8 ] [DEV_REPO_FOLDER]...
      OK.
    [ 2 / 8 ] [PRODUCT_REPO_FOLDER]...
      OK.
    [ 3 / 8 ] [COMPANY_REPO_FOLDER]...
      OK.
    [ 4 / 8 ] [KNOWLEDGE_FOLDER]...
      OK.
    [ 5 / 8 ] [KNOWLEDGE_SOURCE_FOLDER]...
      MISSING: not defined in 'NOTES.md'.
    [ 6 / 8 ] [SPECS_FOLDER]...
      OK.
    [ 7 / 8 ] [SPECS_SOURCE_FOLDER]...
      MISSING: not defined in 'NOTES.md'.
    [ 8 / 8 ] [PRODUCT_DOCS_FOLDER]...
      OK.
    6 constants found, 2 missing.
  Checking agent folder...
    'specs/' found. 7 files.
    'workflows/' found. 24 files.
    'skills/' found. 18 skills.
    OK.

2 issues found:
  MISSING: [KNOWLEDGE_SOURCE_FOLDER] constant in 'NOTES.md'.
  MISSING: [SPECS_SOURCE_FOLDER] constant in 'NOTES.md'.

Fixing issues...
  Adding [KNOWLEDGE_SOURCE_FOLDER] to 'NOTES.md'...
    OK.
  Adding [SPECS_SOURCE_FOLDER] to 'NOTES.md'...
    OK.

Verify complete. 2 issues fixed.
RESULT: PASSED WITH FIXES
================================= END: WORKSPACE VERIFY ==================================
[2026-09-06 13:35:03] (3.0 secs)
```

## 14. Technical Constraints

- Diff and sync scripts are PowerShell (`.ps1`) - consistent with existing DevSystem scripts in SOPS.md
- Scripts must use `Compare-Object` or equivalent for file content comparison. Hash-based comparison (SHA-256) is preferred for file content equality due to performance
- Scripts must handle Unicode filenames and paths with spaces
- Skill files must follow SKILL_RULES.md (all SK-* rules) and WORKFLOW_RULES.md (applicable WF-* rules)
- Templates must follow TEMPLATE_RULES.md (all TMPL-* rules)
- verify.md integration adds a new context section, does not modify existing contexts
- sync.md integration adds a new context section, does not modify existing contexts
- devsystem-core.md edits are limited to Operation Modes and Workspace Scenarios sections
- ID-REGISTRY.md edit adds one line to Workspace Context states
- Skill must be registered in `devsystem-sync.json` Development bundle
- All skill files must pass privacy gate (no real identifiers, addresses, names, project-specific data)

## 15. Document History

**[2026-09-06 14:30]**
- Fixed: FR-14 — removed `.sync-timestamp` reference, updated to `last_sync` in `devsystem-sync.json`, removed upstream direction (upstream = swap params at workflow level) [IMPLEMENTED from /critique CRIT-01, CRIT-02]
- Fixed: NFR-02 — updated locally-modified warning to reference `last_sync` in `devsystem-sync.json` and `LastWriteTime` check [IMPLEMENTED from /critique CRIT-01]
- Fixed: FR-48 — retained [SKILL_CATEGORIES], removed only [LINKED_REPOS] as obsolete [IMPLEMENTED from /critique CRIT-03]
- Fixed: Section 9 Action Flow — rewritten to match Section 8 (single sync.ps1 call iterating sources from config, not 3 separate operations) [IMPLEMENTED from /critique CRIT-04]
- Fixed: DD-12 — "rules" to "specs" [IMPLEMENTED from /critique CRIT-09]
- Fixed: MNF line 58 — removed "pending /rename execution" (rename is done) [IMPLEMENTED from /critique CRIT-10]
- Fixed: Target files — annotated deleted files as "deleted, replaced by sync.ps1" [IMPLEMENTED from /critique CRIT-11]
- Fixed: Section 13 logging example — "OK. 1 source, 1 bundle selected." to "OK." to match implementation [IMPLEMENTED from /critique CRIT-14]
- Updated: Timeline to reflect 8 updates

**[2026-09-05 15:00]**
- Added: FR-40 [WORKSPACE_FOLDER] vs [WORKSPACE_FILE] distinction
- Added: DD-16 rationale for the distinction (from GLOB-FL-041)
- Updated: FR-30 commit.md multi-repo support - exclude repos not in [WORKSPACE_FILE]
- Updated: WS-CT-01 changed from "all 8" to "all required" (conditional constants)
- Added: WS-CT-04 rule for [WORKSPACE_FOLDER] vs [WORKSPACE_FILE]
- Updated: DEV_REPO_NOTES_TEMPLATE.md includes [WORKSPACE_FILE] constant
- Updated: WORKSPACE-GUIDES.md includes [WORKSPACE_FOLDER] vs [WORKSPACE_FILE] section

**[2026-09-04 16:10]**
- Merged: Sync Relationship Dimension (SYNCREL-SP01) into this spec as FR-32..39, NFR-07..08, DD-11..15, IG-08..11, and new Key Mechanisms sections
- Added: SyncRelationship and DetectionMarkers domain objects
- Updated: Workspace Constants data structure now shows conditional split (5 base + 3 SYNCED-only)
- Added: MNF items for Dimension 4 (deterministic detection, SELF-CONTAINED verify pass, auto-detection)
- Source: Merged from `_SPEC_SYNCRELATION_01.md [SYNCREL-SP01]` (deleted)

**[2026-09-04 15:26]**
- Added: Dependency Tree ASCII art diagram in Context section showing upstream/downstream relationships and Dev-to-Dev sync chains
- Added: Direction definitions (downstream = source to all targets, upstream = here back to source)

**[2026-09-03 17:35]**
- Fixed: Script filenames in target files updated to use `_template` suffix (SK-FL-07) and underscore naming: `workspace_diff_template.ps1`, `workspace_sync_template.ps1`

**[2026-09-03 17:30]**
- Added: FR-31 SKILL.md entry point (frontmatter, MNF, Intent Lookup, Core Procedures, References, Gotchas)
- Updated: DD-06 clarified - checks embedded in verify.md (FR-27), not separate WORKSPACE-CHECKS.md file

**[2026-09-03 17:15]**
- Fixed: SOCAS-01 - logging example missing `[COMPANY_REPO_FOLDER]` in workspace constants list
- Fixed: SOCAS-01 - logging example used `[WORKSPACE_FOLDER]\..\Company\knowledge` instead of `[COMPANY_REPO_FOLDER]\knowledge`
- Fixed: Privacy gate - removed remaining real project references from FR-13, FR-14, domain objects, and Document History

**[2026-09-03 17:00]**
- Fixed: Privacy gate - removed real project names from DD-01, DD-03, DD-05, FR-07, Context, Scenario, MUST-NOT-FORGET
- Added: DD-10 clarifying relationship between new diff/sync scripts and existing deploy-to-all-repos.md (generalize, not duplicate)
- Replaced: real project names with generic terms ("DevSystem source", "Real-world workspaces") throughout

**[2026-09-03 16:45]**
- Added: FR-14 locally-modified warning and `.sync-timestamp` tracking (from critique RV-001)
- Added: FR-30 failure recovery and `git -C` repo resolution (from critique RV-002, RV-005)
- Added: FR-16 breaking change and content migration definitions (from critique RV-008)
- Added: FR-27 fix actions per gap type (from critique RV-010)
- Added: FR-06 `[COMPANY_REPO_FOLDER]` constant (from critique RV-009)
- Added: NFR-02 locally-modified file marking in diff preview (from critique RV-001)
- Added: NFR-06 SyncPolicy validation (from critique RV-006)
- Added: IG-07 rollback safety guidance for shared branches (from critique RV-004)
- Added: DD-09 dev repo ordering rationale (from critique RV-014)
- Added: DD-04 `[COMPANY_REPO_FOLDER]` to constants list
- Added: Skill Categories data structure example in section 10 (from critique RV-011)
- Updated: Technical Constraints - hash-based comparison preferred (from critique RV-007)
- Updated: CompanyRepo domain object storage to use `[COMPANY_REPO_FOLDER]`
- Updated: Workspace Constants data structure to include `[COMPANY_REPO_FOLDER]`

**[2026-09-06 13:50]**
- Fixed: Section 13 logging examples — stale `rules/` → `specs/`, `[RULES_SOURCE_FOLDER]` → `[SPECS_SOURCE_FOLDER]`, `[RULES_FOLDER]` → `[SPECS_FOLDER]` [VERIFIED]
- Fixed: Section 13 logging examples — rewritten to comply with LOG-UF-01 (timestamps), LOG-UF-02 (progress indicators), LOG-UF-06 (100-char headers), LOG-GN-02 (quoted paths), LOG-GN-08 (two-level errors), LOG-GN-10 (ellipsis), LOG-GN-11 (sentence endings), LOG-SC-07 (RESULT keyword) [VERIFIED]
- Updated: Timeline to reflect 7 updates

**[2026-09-06 13:35]**
- Revised: FR-44 — bundle definitions moved from source (sync-bundles.json) to target (devsystem-sync.json) as single source of truth
- Revised: FR-45 — source repo only maintains relative path list to synced repos, no bundle definitions
- Revised: FR-46 — sync.ps1 reads ALL config from target's devsystem-sync.json, reads nothing from source
- Revised: FR-49 — sync.md reads devsystem-sync.json instead of per-content-type *-sync.json
- Revised: FR-51 — settings sync uses devsystem-sync.json, not *-sync.json
- Revised: FR-52 — knowledge sync reads from devsystem-sync.json, not knowledge-sync.json
- Revised: FR-53 — specs sync reads from devsystem-sync.json, not specs-sync.json
- Revised: FR-54 — source NOTES.md only (no sync-bundles.json reference)
- Revised: DD-18 — target-only config architecture, no split-brain
- Revised: DD-20 — source synced repos list is informational only
- Updated: Target files — removed sync-bundles.json, added devsystem-sync.json at target
- Updated: MNF — bundle definitions at target, not source
- Updated: Data structures — devsystem-sync.json with complete per-source config, source synced repos list
- Updated: sync.ps1 usage examples — all use devsystem-sync.json
- Updated: Timeline to reflect 6 updates

**[2026-09-06 13:30]**
- Fixed: IG-11 - updated stale `sync-config.json` reference to per-content-type `*-sync.json` [VERIFIED]
- Fixed: Sync Policy Lookup Chain (section 8) - replaced NOTES.md [SYNC_POLICY] with *-sync.json resolution [VERIFIED]
- Fixed: Diff and Sync Flow (section 8) - replaced old diff/sync script references with sync.ps1 -diff/-execute [VERIFIED]
- Fixed: Sync Policy data structure (section 10) - replaced old [SYNC_POLICY] format with reference to *-sync.json [VERIFIED]
- Fixed: Workspace Constants data structure (section 10) - [RULES_FOLDER] → [SPECS_FOLDER], [RULES_SOURCE_FOLDER] → [SPECS_SOURCE_FOLDER] [VERIFIED]
- Fixed: Workspace Verify flow (section 8) - rules/ → specs/ in agent folder check [VERIFIED]
- Fixed: Logging example (section 13) - [RULES_FOLDER] → [SPECS_FOLDER], [RULES_SOURCE_FOLDER] → [SPECS_SOURCE_FOLDER], rules/ → specs/ [VERIFIED]
- Fixed: Depends on - rules/devsystem-core.md → specs/devsystem-core.md [VERIFIED]
- Fixed: DD-14 - [RULES_SOURCE_FOLDER] → [SPECS_SOURCE_FOLDER] [VERIFIED]
- Fixed: Upstream Sync flow (section 8) - [RULES_FOLDER]/[RULES_SOURCE_FOLDER] → [SPECS_FOLDER]/[SPECS_SOURCE_FOLDER] [VERIFIED]
- Fixed: Target files - workspace_diff_template.ps1 and workspace_sync_template.ps1 marked as replaced by sync.ps1 [VERIFIED]
- Updated: IG-11 - added absolute-to-relative path conversion requirement for migration [VERIFIED]

**[2026-09-06 13:20]**
- Revised: FR-44 - sync-bundles.json now references specs/ instead of rules/
- Revised: FR-45 - per-content-type *-sync.json at [WORKSPACE_FOLDER] root (not .devin/sync-config.json)
- Revised: FR-46 - single sync.ps1 with -diff/-execute modes, array params (-sources, -targets, -configs, -output-file)
- Removed: FR-47 - diff.ps1 merged into sync.ps1 -diff mode (DD-19)
- Kept: FR-48 - deploy-to-all-repos.md replacement (unchanged)
- Revised: FR-49 - sync.md uses sync.ps1, per-content-type configs, auto-execute on confirm
- Added: FR-50 - rules → specs folder rename with sops/ and guides/ subfolders
- Added: FR-51 - settings sync use cases (workspace settings from/to, sync settings from/to)
- Added: FR-52 - knowledge sync use cases (knowledge from source, knowledge to targets)
- Added: FR-53 - specs sync use cases (specs from source, specs to targets)
- Added: FR-54 - source repo relative path references only
- Revised: DD-18 - per-content-type config files instead of single sync-config.json
- Added: DD-19 - single script rationale (diff and execute share logic)
- Added: DD-20 - relative path rationale (portability)
- Added: DD-21 - rules → specs rename rationale
- Updated: Target files - removed diff.ps1, sync.ps1 moved to workspace-management skill
- Updated: Data structures - specs-sync.json, knowledge-sync.json, sync.ps1 usage examples
- Updated: MNF - single script, relative paths, rules→specs rename
- Updated: Timeline to reflect 5 updates

**[2026-09-06 12:55]**
- Added: FR-44 (sync-bundles.json - source-side JSON bundle definitions with include/exclude refiners)
- Added: FR-45 (sync-config.json - target-side JSON config with multi-bundle, multi-source support)
- Added: FR-46 (generic sync.ps1 - takes -Source and -Target only, reads JSON config)
- Added: FR-47 (generic diff.ps1 - takes -Source and -Target only, reads JSON config)
- Added: FR-48 (deploy-to-all-repos.md replacement - deleted, not refactored)
- Added: FR-49 (sync.md Workspace Sync context - uses diff.ps1/sync.ps1, reads sync-config.json)
- Added: DD-18 (two-file JSON sync config architecture with three-layer glob refiners)
- Added: sync-bundles.json, sync.ps1, diff.ps1 to target files
- Added: sync-bundles.json and sync-config.json data structures to section 10
- Added: 3 MNF items (JSON-based config, -Source/-Target only params, glob refiner evaluation order)
- Updated: MNF - deploy-to-all-repos.md replaced by sync.md, not just independent
- Updated: Scenario - deploy-to-all-repos.md described as legacy
- Updated: Context - deploy-to-all-repos.md marked as replaced by FR-49
- Updated: FR-31 - removed deploy-to-all-repos.md registration requirement
- Updated: IG-11 - deploy-to-all-repos.md replaced, migration required
- Updated: Technical Constraints - removed deploy-to-all-repos.md references
- Updated: Timeline to reflect 4 updates

**[2026-09-06 00:22]**
- Added: FR-41 (WORKSPACE_CREATION_QUESTIONNAIRE.md - interactive questionnaire)
- Added: FR-42 (workspace-create.md workflow - thin entry point)
- Added: FR-43 (workspace creation procedure in SKILL.md)
- Added: DD-11 (guide + thin workflow separation for workspace creation)
- Renumbered: DD-11 through DD-16 to DD-12 through DD-17 (avoid duplicate DD-11)
- Added: WORKSPACE_CREATION_QUESTIONNAIRE.md to target files
- Added: workspace-create.md to target files
- Updated: Timeline to reflect 3 updates
- Added: 3 MNF items (impact per question, non-destructive creation, thin workflow)

**[2026-09-03 16:10]**
- Fixed: Privacy gate - replaced real project paths with generic placeholders in Context, Domain Objects, NFRs, "What we don't want", and logging examples
- Fixed: AP-PR-06 - expanded GRUC, SOPs acronyms on first use
- Fixed: SOCAS-06 - clarified FR-30 git config handling ("detect and use per-repo git config")
- Fixed: SPEC-CT-02 - removed implementation commands (git, script names, parameters) from action flows, replaced with behavioral descriptions

**[2026-09-03 15:24]**
- Added: WSKMGMT-FR-30 (commit.md multi-repo support)
- Added: WSKMGMT-DD-09 (commit order: product, dev, others)
- Added: Multi-Repo Commit action flow
- Added: commit.md to target files

**[2026-09-03 15:20]**
- Initial specification created
