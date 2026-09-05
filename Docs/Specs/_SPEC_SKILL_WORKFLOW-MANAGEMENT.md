# SPEC: Workspace Management Skill

**Doc ID**: WSKMGMT-SP01
**Feature**: workspace-management-skill
**Goal**: Specify a skill that manages agentic workspace setup, DevSystem synchronization, and knowledge distribution across product/dev/company repo architectures
**Timeline**: Created 2026-09-03, Updated 0 times (2026-09-03 - 2026-09-03)
**Target file(s)**:
- `DevSystemV4.3/rules/devsystem-core.md` (Operation Modes, Workspace Scenarios)
- `DevSystemV4.3/skills/workspace-management/SKILL.md`
- `DevSystemV4.3/skills/workspace-management/WORKSPACE-GUIDES.md`
- `DevSystemV4.3/skills/workspace-management/WORKSPACE-RULES.md`
- `DevSystemV4.3/skills/workspace-management/DEV_REPO_NOTES_TEMPLATE.md`
- `DevSystemV4.3/skills/workspace-management/PRODUCT_REPO_README_TEMPLATE.md`
- `DevSystemV4.3/skills/workspace-management/COMPANY_REPO_NOTES_TEMPLATE.md`
- `DevSystemV4.3/skills/workspace-management/workspace_diff_template.ps1`
- `DevSystemV4.3/skills/workspace-management/workspace_sync_template.ps1`
- `DevSystemV4.3/workflows/verify.md` (new context section)
- `DevSystemV4.3/workflows/sync.md` (new context section)
- `DevSystemV4.3/workflows/commit.md` (multi-repo commit support)
- `ID-REGISTRY.md` (Workspace Context states)

**Depends on:**
- `DevSystemV4.3/rules/devsystem-core.md` for existing operation modes and workspace scenarios
- `DevSystemV4.3/skills/session-management/SKILL.md` for session folder structure (T##/S##)
- `deploy-to-all-repos.md` for diff/sync preview/confirm pattern

**Does not depend on:**
- Any project-specific SPEC (this skill is generic, reusable across all DevSystem workspaces)

## MUST-NOT-FORGET

- Skill files must be generic - no project-specific data, no real identifiers, addresses, or names
- All new rules/workflows/skills created in `[DEVSYSTEM_FOLDER]` first, then sync to `.devin/`
- Register `workspace-management` in `NOTES.md` `[SKILL_CATEGORIES]` and `deploy-to-all-repos.md` `$skillCategories`
- Follow SOP 1 (SOPS.md) for new skill creation including verification
- `deploy-to-all-repos.md` is inspiration for diff/sync scripts, not a copy target - scripts must be generic, not hardcoded to any specific project
- Workspace constants are defined in DevRepo NOTES.md, not in the skill itself - skill reads them from there
- Sync policy lookup order: 1) downstream repo NOTES.md, 2) CompanyRepo NOTES.md - never skip to defaults without checking both
- Downstream repo modifications are allowed during verify - only gaps and incompatibilities must be fixed
- IMPL-ISOLATED extension is a core rule change affecting all DevSystem users - must be backwards compatible
- WORKSPACE mode is additive to Dimension 1 - existing SINGLE-PROJECT and MONOREPO detection must not break
- Dimension 4 (Sync Relationship) is additive - existing 3 dimensions must not break
- Detection must be deterministic - no ambiguity between SYNCED and SELF-CONTAINED
- SELF-CONTAINED repos must still pass /verify - missing sync constants are valid, not gaps
- Existing repos with [LINKED_REPOS] or [*_SOURCE_FOLDER] are SYNCED by default - no migration needed

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

**Problem:** DevSystem workspaces come in multiple architectures (single project, monorepo, multi-repo workspace with product/dev separation). The current system has no unified way to compare workspace state against central sources, update from sources, roll back changes, or verify integrity. Existing mechanisms (SOPS.md, deploy-to-all-repos.md, /prime, /sync) are scattered, project-specific, and do not cover the full product/dev/company repo pattern.

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

Real-world pattern: A DevRepo (private, git) contains specs, sessions, evals, knowledge, and an agent folder (`.devin/`). It has `main.code-workspace` referencing a separate ProductRepo (public, git) with shipped code. A `Company` folder serves as central source for knowledge and rules. The DevSystem source is a separate folder with versioned DevSystem releases.

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
  (docs only, no rules/knowledge/DevSystem artifacts)

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
- `deploy-to-all-repos.md`: Deploys `.devin/` to linked repos with preview/confirm flow
- `/prime`: Detects workspace scenario, reads rules and docs
- `/sync`: Document-level sync (code to docs, session to project)
- `/verify`: Multi-context verification (SPEC, IMPL, Code, TEST, etc.)
- Session management skill: Init/save/resume/finalize/archive lifecycle

None of these provide unified workspace compare/update/rollback/integrity operations. The workspace-management skill fills this gap.

Note: The DevSystem source repository is the upstream source for all DevSystem workspaces. It contains the canonical version of rules, skills, and workflows.

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
- `rules_folder` - `[DEV_REPO_FOLDER]\rules`
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

A **CompanyRepo** is a central source folder (not necessarily a git repo) containing knowledge bundles and rules shared across multiple workspaces. Tracks downstream repositories and sync policies.

**Storage:** `[COMPANY_REPO_FOLDER]` (default: `[WORKSPACE_FOLDER]\..\Company`)
**Key properties:**
- `notes_path` - `[COMPANY_REPO_FOLDER]\NOTES.md`
- `knowledge_source_folder` - `[COMPANY_REPO_FOLDER]\knowledge`
- `rules_source_folder` - `[COMPANY_REPO_FOLDER]\rules`
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

A **PromptSystem** is a folder containing `rules`, `skills`, and `workflows` subfolders. The DevSystem source is a PromptSystem. Agent folders (e.g., `.devin`, `.[product-agent-folder]`) are PromptSystem mirrors.

**Storage:** `[DEVSYSTEM_FOLDER]` (source), `[AGENT_FOLDER]` (mirror)
**Key properties:**
- `rules_folder` - contains rule `.md` files
- `workflows_folder` - contains workflow `.md` files
- `skills_folder` - contains skill subfolders with `SKILL.md`

### KnowledgeBundle

A **KnowledgeBundle** is a folder of reference documents for a specific topic (e.g., `Windsurf/`, `AI-Standards/`, `OpenAI/`).

**Storage:** `[KNOWLEDGE_FOLDER]` (local) or `[KNOWLEDGE_SOURCE_FOLDER]` (central)
**Key properties:**
- `bundle_name` - folder name (e.g., `Windsurf`)
- `documents` - list of contained `.md` files
- `sub_bundles` - nested folders (e.g., `Windsurf/HowCascadeWorks/`)

### RulesBundle

A **RulesBundle** is a folder of rules, workflows, design guidelines, and SOPs shared from Company to downstream repos.

**Storage:** `[RULES_FOLDER]` (local) or `[RULES_SOURCE_FOLDER]` (central)
**Key properties:**
- `bundle_name` - folder name
- `documents` - list of contained `.md` files

### SyncRelationship

A **SyncRelationship** is the 4th workspace scenario dimension, indicating whether a repo participates in a sync dependency tree.

**Storage:** Detected from DevRepo NOTES.md content (not stored as a field)
**Key properties:**
- `state` - SYNCED or SELF-CONTAINED
- `has_upstream` - boolean, true if [*_SOURCE_FOLDER] constants defined
- `has_downstream` - boolean, true if [LINKED_REPOS] section defined

### Detection Markers

Sync-related markers in NOTES.md that indicate SYNCED state:
- `[LINKED_REPOS]` section present → has downstream targets
- `[KNOWLEDGE_SOURCE_FOLDER]` constant defined → has knowledge upstream
- `[RULES_SOURCE_FOLDER]` constant defined → has rules upstream
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
- Required constants: `[DEV_REPO_FOLDER]`, `[PRODUCT_REPO_FOLDER]`, `[COMPANY_REPO_FOLDER]`, `[KNOWLEDGE_FOLDER]`, `[KNOWLEDGE_SOURCE_FOLDER]`, `[RULES_FOLDER]`, `[RULES_SOURCE_FOLDER]`, `[PRODUCT_DOCS_FOLDER]`
- Constants are workspace-specific - skill reads them from NOTES.md, does not hardcode values
- `DEV_REPO_NOTES_TEMPLATE.md` provides the template with all constants and defaults

**WSKMGMT-FR-07: Three sync sources**
- Prompt System: default source is DevSystem source `[WORKSPACE_FOLDER]\..\[DevSystemSourceName]\DevSystemV*`, syncs to `[DEV_REPO_FOLDER]\.devin` and/or other agent folders
- Knowledge: default source is `[KNOWLEDGE_SOURCE_FOLDER]` (Company), syncs to `[KNOWLEDGE_FOLDER]`
- Rules: default source is `[RULES_SOURCE_FOLDER]` (Company), syncs to `[RULES_FOLDER]`
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
- Per downstream repo: repo path, skill categories, knowledge bundles, rules, workflows, DevSystem rules to sync
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
- Supports downstream (source to target) and upstream (target to source) directions
- Handles file copy, delete, and content migration for breaking changes
- Preview mode (dry-run) and execute mode
- Must be generic - no hardcoded project paths
- Before overwriting a file not in the preserve list, check if target file was modified after last sync timestamp. If so, warn user and offer to add to preserve list or proceed with overwrite
- Store last sync timestamp in target folder root (`.sync-timestamp`, gitignored). Missing timestamp triggers full comparison

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
- Verify agent folder exists and contains rules, workflows, skills subfolders
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
- Verify agent folder contains required subfolders (rules, workflows, skills)
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
- MUST-NOT-FORGET section (5-8 items): generic paths only, sync before deploy, preserve list check, rollback warning for shared branches, privacy gate, register in NOTES.md and deploy-to-all-repos.md
- Intent Lookup: maps 3 areas (WORKSPACE, DEVSYSTEM, KNOWLEDGE) x 4 operations (compare, update, rollback, integrity) to procedures and FR references
- Core Procedures: compare workspace, update from source, rollback, integrity check, multi-repo commit
- References: links to WORKSPACE-GUIDES.md, WORKSPACE-RULES.md, DEV_REPO_NOTES_TEMPLATE.md, PRODUCT_REPO_README_TEMPLATE.md, COMPANY_REPO_NOTES_TEMPLATE.md
- Gotchas: sync timestamp missing triggers full diff, preserve list overrides overwrite rules, rollback on shared branches requires revert commit
- Follows SKILL_RULES.md (all SK-* rules) and SKILL_TEMPLATE.md structure

**WSKMGMT-FR-30: commit.md multi-repo support**
- In WORKSPACE mode, detect changes across all git repos in the workspace
- Commit order: 1) product repo first, 2) dev repo second, 3) all other workspace repos
- For each repo: detect uncommitted changes, analyze by type (feat, fix, docs, test, chore), create conventional commits
- If no changes in a repo, skip silently
- Report committed changes per repo at end
- In SINGLE-PROJECT and MONOREPO modes, behavior is unchanged (single repo commit)
- Must detect and use per-repo git config (user.name, user.email) - do not assume workspace-wide git identity
- All git operations must be explicitly scoped to the target repo using `git -C [repo_path]` or equivalent. Do not rely on current working directory for repo resolution
- If a repo commit fails, report the failure with error message, continue with remaining repos, and summarize partial success at end. Do not roll back already-committed repos

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
- Check NOTES.md for sync markers: [LINKED_REPOS], [*_SOURCE_FOLDER], [DEVSYSTEM]
- Report all 4 dimensions in final output
- Example: "Mode: WORKSPACE + SINGLE-VERSION + SESSION-MODE + SYNCED"

**WSKMGMT-FR-35: Make sync source constants conditional**
- WS-CT-01 in WORKSPACE-RULES.md must split constants into:
  - Always required (5): [DEV_REPO_FOLDER], [PRODUCT_REPO_FOLDER], [KNOWLEDGE_FOLDER], [RULES_FOLDER], [PRODUCT_DOCS_FOLDER]
  - Required for SYNCED only (3): [COMPANY_REPO_FOLDER], [KNOWLEDGE_SOURCE_FOLDER], [RULES_SOURCE_FOLDER]
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

## 5. Non-Functional Requirements

**WSKMGMT-NFR-01: Performance - Diff execution time**
- Diff scripts must complete within 10 seconds for workspaces with up to 500 files
- Verification method: timed execution against a WORKSPACE-mode workspace with 500+ files

**WSKMGMT-NFR-02: Reliability - Sync safety**
- Sync scripts must never delete files without showing them in preview first
- Sync scripts must create backup of overwritten files before writing
- Diff preview must mark files modified locally since last sync as 'locally modified - will be overwritten'
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

**WSKMGMT-DD-04:** Workspace constants tracked in DevRepo NOTES.md. New constants: `[DEV_REPO_FOLDER]`, `[PRODUCT_REPO_FOLDER]`, `[COMPANY_REPO_FOLDER]`, `[KNOWLEDGE_FOLDER]`, `[KNOWLEDGE_SOURCE_FOLDER]`, `[RULES_FOLDER]`, `[RULES_SOURCE_FOLDER]`, `[PRODUCT_DOCS_FOLDER]`. Rationale: Centralizes workspace configuration for the skill's compare/update/rollback/integrity operations.

**WSKMGMT-DD-05:** Three sync sources for WORKSPACE mode: (1) Prompt System from DevSystem source, (2) Knowledge from Company folder, (3) Rules from Company folder. Each supports downstream and upstream sync. Rationale: Different content types have different sources and sync directions.

**WSKMGMT-DD-06:** Workspace Management Skill contains GRUC files plus templates plus diff/sync scripts. Checks are embedded in the `/verify` workflow (FR-27 "Workspace Setup" context) rather than a separate WORKSPACE-CHECKS.md file. Rationale: GRUC pattern (Guides + Rules + Checks) extended with templates and scripts. Checks live in verify.md because workspace verification is workflow-triggered (`/verify workspace`), not skill-internal. Templates provide structure, scripts provide automation, guides provide understanding, rules provide verification.

**WSKMGMT-DD-07:** `/verify` workflow gets a new context: "Workspace Setup". Rationale: `/verify` already has context-specific sections (Cross-Document, INFO, SPEC, IMPL, Code, TEST, Session, Workflow, Skill, Template, etc.) - adding workspace setup as a new context is the natural integration point. Downstream modifications are allowed because workspaces legitimately customize their setup.

**WSKMGMT-DD-08:** `/sync` workflow gets a new context: "Workspace Sync" with policy lookup and preview/confirm flow. Rationale: `/sync` already has context-specific sections and a preview/execute pattern - adding workspace sync as a new context reuses the existing workflow structure. Policy lookup order (downstream first, CompanyRepo second) ensures local customizations take precedence over central defaults.

**WSKMGMT-DD-09:** `/commit` workflow extended for WORKSPACE mode. In multi-repo workspace mode, commits changes across multiple git repos in order: 1) product repo first, 2) dev repo second, 3) all other workspace repos. Rationale: Product repo changes (code, tests) are the primary deliverable and should be committed first. Dev repo changes (specs, sessions, knowledge) are secondary. Other repos (Company, linked repos) are tertiary. Dev repo is committed second because it contains documentation of the product changes. Temporary inconsistency (product committed, dev not) is acceptable because dev repo content is not a runtime dependency. This ordering ensures product changes are not left uncommitted if dev repo commit fails.

**WSKMGMT-DD-10:** Diff and sync scripts (FR-13, FR-14) generalize `deploy-to-all-repos.md` patterns, not duplicate them. `deploy-to-all-repos.md` deploys from `.devin/` staging to linked repos with hardcoded repo lists and skill categories. The new scripts generalize this to: (1) read source and target from workspace constants, not hardcoded paths, (2) read sync policy from NOTES.md, not inline configuration, (3) support 3 sync sources (Prompt System, Knowledge, Rules), not only DevSystem, (4) support upstream and downstream, not only downstream. `deploy-to-all-repos.md` remains unchanged for existing deployment workflows. The new scripts are the foundation for `/sync workspace` context. Rationale: `deploy-to-all-repos.md` solves 80% of the problem but is project-specific. Generalizing its proven patterns (hash comparison, skill filtering, preview/confirm) into generic scripts avoids duplication while preserving the working deployment workflow.

**WSKMGMT-DD-11:** Two states only (SYNCED, SELF-CONTAINED), not three. A repo is either part of a dependency tree or it isn't. No "partial sync" state. Rationale: Simplicity. If a repo syncs knowledge but not rules, it still has sync markers and is SYNCED. The sync policy handles which sources to sync.

**WSKMGMT-DD-12:** Auto-detection, not declaration. Sync relationship is inferred from NOTES.md content, not from an explicit field. Rationale: Zero migration cost. Existing repos are automatically classified correctly. Adding an explicit `[SYNC_RELATIONSHIP]: SYNCED` field would require all existing repos to update.

**WSKMGMT-DD-13:** Sync source constants are conditional, not base constants. [COMPANY_REPO_FOLDER], [KNOWLEDGE_SOURCE_FOLDER] and [RULES_SOURCE_FOLDER] are only required for SYNCED repos. Rationale: Self-contained repos don't have upstream sources. Requiring these constants would force self-contained repos to define meaningless paths.

**WSKMGMT-DD-14:** Dimension 4 is orthogonal to Dimension 1. A SINGLE-PROJECT repo can be SYNCED (syncs from DevSystem) or SELF-CONTAINED (standalone). A WORKSPACE repo can be SYNCED (full dependency tree) or SELF-CONTAINED (multi-repo but no external sync). Rationale: Sync relationship and project structure are independent concerns.

**WSKMGMT-DD-15:** [DEVSYSTEM] reference in NOTES.md counts as a sync marker. Even if a repo doesn't have [LINKED_REPOS] or [*_SOURCE_FOLDER], referencing [DEVSYSTEM] means it syncs from a DevSystem source. Rationale: [DEVSYSTEM] is the primary sync marker - it identifies the upstream DevSystem version.

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

**WSKMGMT-IG-11:** deploy-to-all-repos.md must continue to work unchanged - it already reads [LINKED_REPOS] which only exists in SYNCED repos.

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

### Sync Policy Lookup Chain

```
Resolve sync policy:
├─> Check downstream repo NOTES.md for [SYNC_POLICY] section?
│   ├─ Found -> Use downstream policy (local customizations take precedence)
│   └─ Not found
│       ├─> Check CompanyRepo NOTES.md for downstream repo entry?
│       │   ├─ Found -> Use CompanyRepo policy (central default for this repo)
│       │   └─ Not found
│       │       └─> Use workspace constants defaults (fallback)
```

### Diff and Sync Flow

```
User runs /sync workspace
├─> Read workspace constants from DevRepo NOTES.md
├─> Resolve sync policy (lookup chain above)
├─> For each sync source (Prompt System, Knowledge, Rules):
│   ├─> Run diff script: compare source vs target
│   └─> Collect diff results
├─> Show preview: files to add, modify, delete, skip
├─> Prompt for confirmation
│   ├─> Confirmed -> Run sync script for each source
│   │   ├─> Create backups of files to overwrite
│   │   ├─> Execute copy/delete operations
│   │   └─> Report results
│   └─> Not confirmed -> Abort, no changes
```

### Sync Relationship Detection

```
Detect sync relationship:
├─> Check NOTES.md for sync markers:
│   ├─> [LINKED_REPOS] section present? → has downstream
│   ├─> [KNOWLEDGE_SOURCE_FOLDER] defined? → has knowledge upstream
│   ├─> [RULES_SOURCE_FOLDER] defined? → has rules upstream
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
│   │   ├─> Check sync policy if [SYNC_POLICY] section exists
│   │   └─> Check [LINKED_REPOS] targets exist
│   └─> SELF-CONTAINED
│       ├─> Check 5 base constants only
│       ├─> Skip sync source constant checks
│       └─> Skip sync policy validation
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
├─> Read DevRepo NOTES.md
│   ├─> Extract workspace constants
│   └─> Extract sync policy (if present)
├─> Resolve sync policy via lookup chain
├─> For Prompt System:
│   ├─> Diff [DEVSYSTEM_FOLDER] against [AGENT_FOLDER]
│   │   └─> Returns: new files, modified files, deleted files
│   ├─> Show preview
│   └─> If confirmed: sync downstream
├─> For Knowledge:
│   ├─> Diff [KNOWLEDGE_SOURCE_FOLDER] against [KNOWLEDGE_FOLDER]
│   ├─> Show preview
│   └─> If confirmed: sync downstream
└─> For Rules:
    ├─> Diff [RULES_SOURCE_FOLDER] against [RULES_FOLDER]
    ├─> Show preview
    └─> If confirmed: sync downstream
```

### Workspace Sync (upstream)

```
/sync workspace upstream
├─> Read DevRepo NOTES.md
├─> For Prompt System:
│   ├─> Diff [AGENT_FOLDER] against [DEVSYSTEM_FOLDER]
│   ├─> Show preview (changes to push back to central source)
│   └─> If confirmed: sync upstream
├─> For Knowledge:
│   ├─> Diff [KNOWLEDGE_FOLDER] against [KNOWLEDGE_SOURCE_FOLDER]
│   ├─> Show preview
│   └─> If confirmed: sync upstream
└─> For Rules:
    ├─> Diff [RULES_FOLDER] against [RULES_SOURCE_FOLDER]
    ├─> Show preview
    └─> If confirmed: sync upstream
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
│   └─> rules/, workflows/, skills/ subfolders exist?
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
[RULES_FOLDER]: [DEV_REPO_FOLDER]\rules
[PRODUCT_DOCS_FOLDER]: [PRODUCT_REPO_FOLDER]\docs

# Required for SYNCED only (3):
[COMPANY_REPO_FOLDER]: [WORKSPACE_FOLDER]\..\Company
[KNOWLEDGE_SOURCE_FOLDER]: [COMPANY_REPO_FOLDER]\knowledge
[RULES_SOURCE_FOLDER]: [COMPANY_REPO_FOLDER]\rules
```

### Sync Policy (in downstream NOTES.md or CompanyRepo NOTES.md)

```
[SYNC_POLICY]
- Source: [DEVSYSTEM_FOLDER]
  Target: [AGENT_FOLDER]
  Direction: downstream
  Filter: skill_categories=Development
  Overwrite: rules/*, workflows/*, skills/*
  Preserve: skills/selftest/ (local-only skill)
- Source: [KNOWLEDGE_SOURCE_FOLDER]
  Target: [KNOWLEDGE_FOLDER]
  Direction: downstream
  Filter: include=Windsurf/,AI-Standards/
  Overwrite: all
  Preserve: (none)
- Source: [RULES_SOURCE_FOLDER]
  Target: [RULES_FOLDER]
  Direction: downstream
  Filter: (all)
  Overwrite: all
  Preserve: (none)
```

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
Workspace Sync Preview
├─> Prompt System: [DEVSYSTEM_FOLDER] -> [AGENT_FOLDER]
│   ├─> 3 new files:
│   │   ├─> skills/workspace-management/SKILL.md
│   │   ├─> skills/workspace-management/WORKSPACE-GUIDES.md
│   │   └─> skills/workspace-management/WORKSPACE-RULES.md
│   ├─> 2 modified files:
│   │   ├─> rules/devsystem-core.md
│   │   └─> workflows/verify.md
│   └─> 0 deleted files
├─> Knowledge: [KNOWLEDGE_SOURCE_FOLDER] -> [KNOWLEDGE_FOLDER]
│   └─> No changes
└─> Rules: [RULES_SOURCE_FOLDER] -> [RULES_FOLDER]
    └─> No changes

Confirm sync? (yes/go/confirmed to execute, no/cancel to abort)
```

**Expected output for verify:**
```
Workspace Verify: [DevRepo Name] (WORKSPACE mode)
├─> Required files:
│   ├─> NOTES.md: OK
│   ├─> PROBLEMS.md: OK
│   ├─> PROGRESS.md: OK
│   ├─> ID-REGISTRY.md: OK
│   └─> SOPS.md: OK
├─> Workspace constants:
│   ├─> [DEV_REPO_FOLDER]: OK
│   ├─> [PRODUCT_REPO_FOLDER]: OK
│   ├─> [COMPANY_REPO_FOLDER]: OK
│   ├─> [KNOWLEDGE_FOLDER]: OK
│   ├─> [KNOWLEDGE_SOURCE_FOLDER]: MISSING - not defined in NOTES.md
│   ├─> [RULES_FOLDER]: OK
│   ├─> [RULES_SOURCE_FOLDER]: MISSING - not defined in NOTES.md
│   └─> [PRODUCT_DOCS_FOLDER]: OK
├─> Agent folder:
│   ├─> rules/: OK (7 files)
│   ├─> workflows/: OK (24 files)
│   └─> skills/: OK (18 skills)
└─> 2 issues found:
    ├─> MISSING: [KNOWLEDGE_SOURCE_FOLDER] constant in NOTES.md
    └─> MISSING: [RULES_SOURCE_FOLDER] constant in NOTES.md

Fixing issues...
├─> Added [KNOWLEDGE_SOURCE_FOLDER]: [COMPANY_REPO_FOLDER]\knowledge
└─> Added [RULES_SOURCE_FOLDER]: [COMPANY_REPO_FOLDER]\rules

Verify complete. 2 issues fixed.
```

## 14. Technical Constraints

- Diff and sync scripts are PowerShell (`.ps1`) - consistent with existing DevSystem scripts in SOPS.md and deploy-to-all-repos.md
- Scripts must use `Compare-Object` or equivalent for file content comparison. Hash-based comparison (SHA-256) is preferred for file content equality due to performance
- Scripts must handle Unicode filenames and paths with spaces
- Skill files must follow SKILL_RULES.md (all SK-* rules) and WORKFLOW_RULES.md (applicable WF-* rules)
- Templates must follow TEMPLATE_RULES.md (all TMPL-* rules)
- verify.md integration adds a new context section, does not modify existing contexts
- sync.md integration adds a new context section, does not modify existing contexts
- devsystem-core.md edits are limited to Operation Modes and Workspace Scenarios sections
- ID-REGISTRY.md edit adds one line to Workspace Context states
- Skill must be registered in NOTES.md `[SKILL_CATEGORIES]` under Development category
- Skill must be registered in deploy-to-all-repos.md `$skillCategories` under Development category
- All skill files must pass privacy gate (no real identifiers, addresses, names, project-specific data)

## 15. Document History

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
