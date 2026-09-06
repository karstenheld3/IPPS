# SPEC: Unified Project Release Workflow

**Doc ID**: RLSPROJ-SP01
**Feature**: unified-project-release
**Goal**: Define a single config-driven project-release workflow that supports single-repo and multi-repo workspaces with date-based or semver tagging
**Timeline**: Created 2026-09-05

**Target file(s)**:
- `DevSystemV4.3/workflows/project-release.md` (replaces existing)
- Workspace `NOTES.md` / `!NOTES.md` (new `[RELEASE_CONFIG]` section)

**Depends on:**
- `SOPS.md` for post-release Standard Operating Procedure (SOP) steps (existing per-workspace)
- `@skills:write-documents` for document structure conventions
- `@skills:workspace-management` for workspace mode detection and workspace constants
- `@skills:session-management` for `[SESSIONS_FOLDER]` constant and session folder conventions
- `DEV_REPO_NOTES_TEMPLATE.md` from workspace-management skill for NOTES.md structure integration

**Does not depend on:**
- `_SPEC_IPPS_PROMPT_FILE_FORMAT.md [IPPSPRMTFMT-SP01]` (unrelated format spec)

## MUST-NOT-FORGET

- ONE workflow file serves ALL workspace types - no per-repo customization of the workflow itself
- All release configuration lives in workspace NOTES.md under `[RELEASE_CONFIG]` section
- Workflow MUST detect workspace context first (single-repo vs multi-repo) like `/prime` Step 4, then branch correctly
- Product repo is always released first, dev repo second (if configured)
- Agent MUST NOT run build tools (build.bat, build.ps1, cargo, etc.) - binary build is user-managed
- Release notes always go to product repo's configured release notes directory
- Post-release version bump is mandatory and is the LAST step of the release process
- Workflow must read SOPS.md (or `_SOPS.md`) for post-release procedures - SOPS file name varies per workspace
- Existing per-workspace project-release.md files must be replaceable by this single workflow

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
10. [Configuration Schema](#10-configuration-schema)
11. [Technical Constraints](#11-technical-constraints)
12. [Logging Requirements](#12-logging-requirements)
13. [Failure Recovery](#13-failure-recovery)
14. [Document History](#14-document-history)

## 1. Scenario

**Problem:** Three variants of `project-release.md` exist with hardcoded paths, repo-specific logic, and duplicated step definitions. Adding a new workspace requires copying and modifying the workflow. Configuration is scattered across workflow files, SOPS files, and NOTES files with no single source of truth for release parameters.

**Solution:**
- A single generic `project-release.md` workflow reads all release parameters from a `[RELEASE_CONFIG]` section in the workspace's NOTES.md
- The workflow supports 1 to N repos, each with independent tag format, version source, and post-release bump strategy
- Product repo is released first (version bump, build, tag, release notes, GitHub release), then dev repo(s) are tagged with the same or derived version
- Optional steps (binary build, version consistency gate) are activated by config flags, not hardcoded

**What we don't want:**
- Per-workspace copies of project-release.md with slightly different hardcoded paths
- Workflow files containing repo paths, version files, or tag formats - those belong in NOTES.md config
- Agent executing build tools autonomously (binary build is always user-managed)
- Release notes location hardcoded in workflow - must be configurable
- Separate workflows for "single repo" vs "multi-repo" - one workflow handles both
- SOPS file name hardcoded - some workspaces use `SOPS.md`, others `_SOPS.md`

## 2. Context

### Current State (BEFORE)

Three variants of project-release.md exist:

```
Workspace A (single-repo, date-based)
├── Tag format: YYYY-MM-DD (date-based)
├── Repos: 1 (single)
├── Version source: DevSystem folder name (DevSystemVX.Y)
├── Binary: none
├── Release notes: Docs/ReleaseNotes/
├── Post-release bump: rename DevSystem folder
└── SOPS file: SOPS.md

Workspace B (multi-repo, semver)
├── Tag format: vX.Y.Z (semver)
├── Repos: 2 (product + dev)
├── Version source: pyproject.toml (product), none (dev)
├── Binary: user-built exe (product)
├── Release notes: docs/ReleaseNotes/ (product repo, lowercase)
├── Post-release bump: patch bump in pyproject.toml (product)
├── Version gate: 4-way consistency check (product)
└── SOPS file: _SOPS.md
```

### Proposed State (AFTER)

```
ONE workflow: project-release.md (generic, config-driven)
├── Reads [RELEASE_CONFIG] from workspace NOTES.md
├── Supports 1 to N repo entries
├── Each repo: independent tag_format, version_source, post_release_bump
├── Optional: binary_build, version_gate
├── Release notes: always to product repo's configured directory
└── SOPS file: configured name (SOPS.md or _SOPS.md)
```

### Workspace Dimension Coverage

The workflow supports all 4 combinations of workspace dimensions:

- **SINGLE-PROJECT + SINGLE-VERSION**: One repo entry in config, date-based or semver tags
- **SINGLE-PROJECT + MULTI-VERSION**: One repo entry, version source tracks active version
- **WORKSPACE (multi-repo) + SINGLE-VERSION**: Two+ repo entries, same version tag across repos
- **WORKSPACE (multi-repo) + MULTI-VERSION**: Two+ repo entries, each with independent or derived version

## 3. Domain Objects

### ReleaseConfig

A configuration block in workspace NOTES.md that defines all release parameters for that workspace.

**Storage**: Workspace `NOTES.md` or `!NOTES.md` under `[RELEASE_CONFIG]` section
**Definition**: This spec, section 10 (Configuration Schema)

**Key properties:**
- `sops_file` - Name of SOPS file in workspace (e.g., `SOPS.md`, `_SOPS.md`). Stored as `[SOPS_FILE]` constant
- `repos` - Ordered list of RepoConfig entries (product first, then dev)
- `release_notes_dir` - Path to release notes directory, composed from `[PRODUCT_DOCS_FOLDER]`. Stored as `[RELEASE_NOTES_FOLDER]` constant
- `release_notes_naming` - Filename pattern for release notes files
- `sessions_folder` - Session folder path, typically `[SESSIONS_FOLDER]`
- `tag_annotation_template` - Optional template for git tag annotation message

### RepoConfig

Configuration for a single repo participating in the release process.

**Key properties:**
- `name` - Human-readable identifier (e.g., `product`, `dev`)
- `path` - Repo root path using workspace constants (e.g., `[WORKSPACE_FOLDER]`, `[PRODUCT_REPO_FOLDER]`, `[WORKSPACE_FOLDER]`)
- `role` - `product` or `dev` (determines release order and notes placement)
- `tag_format` - Tag naming pattern: `date` (YYYY-MM-DD) or `semver` (vX.Y.Z)
- `version_source` - How version is determined: `devsystem_folder`, `pyproject_toml`, `package_json`, `none`
- `version_file` - Path to version source file using workspace constants (e.g., `[PRODUCT_REPO_FOLDER]\pyproject.toml`). Required when version_source is file-based
- `post_release_bump` - Bump strategy: `devsystem_rename`, `patch_bump`, `minor_bump`, `none`
- `binary_build` - Boolean: whether user must build a binary before release
- `binary_path_pattern` - Pattern for binary path (e.g., `dist/myapp-{version}-win-x64.exe`)
- `version_gate` - Boolean: whether version consistency gate is required before tagging
- `test_command` - Optional shell command to run tests for this repo
- `github_release` - Boolean: whether to create GitHub release for this repo
- `github_release_assets` - List of file paths to attach as release assets
- `github_release_notes` - `file` or `reference` (dev repo notes reference product release)

### VersionSource

Mechanism for determining the current version string of a repo.

**Types:**
- `devsystem_folder` - Version derived from DevSystem folder name (e.g., `DevSystemV4.3` -> `4.3`)
- `pyproject_toml` - Version from `pyproject.toml` `[project] version` field
- `package_json` - Version from `package.json` `version` field
- `none` - No version source (tag-only repo, version derived from tag or product repo)

### TagFormat

Pattern for git tag names.

**Types:**
- `date` - `YYYY-MM-DD` format (e.g., `2026-09-05`)
- `semver` - `vX.Y.Z` format (e.g., `v1.0.1`)

### VersionGate

Optional pre-tagging consistency check that verifies version alignment across multiple sources before creating tags.

**Checks (when enabled):**
- Version source file version matches planned tag version
- Binary filename version matches (when binary_build is true)
- Binary `--version` output matches (when binary_build is true)
- Planned git tag matches version source

### ReleaseNotes

Markdown document summarizing sessions, artifacts, and changes since last release.

**Storage**: Product repo's configured `release_notes_dir`
**Naming**: Configured pattern (default: `RELEASE_NOTES_v{VERSION}_{DATE}.md`)

## 4. Functional Requirements

**RLSPROJ-FR-01: Read Release Configuration**
- Workflow MUST read `[RELEASE_CONFIG]` section from workspace NOTES.md (or `!NOTES.md`)
- If no `[RELEASE_CONFIG]` section exists, workflow MUST report error and halt
- Workflow MUST read SOPS file (name from config) for post-release procedures

**RLSPROJ-FR-02: Support Single-Repo Mode**
- When `repos` list contains one entry, workflow executes single-repo release flow
- No cross-repo tagging or version synchronization needed

**RLSPROJ-FR-03: Support Multi-Repo Mode**
- When `repos` list contains 2+ entries, workflow executes multi-repo release flow
- Product repo (role=product) is always released first
- Dev repo(s) (role=dev) are tagged after product repo is tagged. In multi-repo mode, all tags are created locally first (two-phase per FR-10), then pushed product-first
- All repos receive the same tag string when tag_format matches
- When tag formats differ between repos, dev repo independently derives its tag from its own version_source (e.g., product tags `2026-09-05`, dev reads its own version_source and tags `v4.3`)

**RLSPROJ-FR-04: Support Date-Based Tag Format**
- When `tag_format` is `date`, tag string is `YYYY-MM-DD` using current date
- User may override date with explicit value

**RLSPROJ-FR-05: Support Semver Tag Format**
- When `tag_format` is `semver`, tag string is `vX.Y.Z` derived from version source
- Pre-tagging: version source file must already contain the target release version (user bumps via SOPS procedure or manual edit before invoking workflow)
- Post-release bump (FR-15) increments to the NEXT development version after release is complete

**RLSPROJ-FR-06: Determine Release Scope**
- Workflow MUST find last release tag (most recent by creation date)
- If no previous tags exist (first release): scope is all commits from `HEAD` to initial commit
- Workflow MUST list commits since last tag
- Workflow MUST list changed files since last tag
- In multi-repo mode, scope is determined for each repo independently

**RLSPROJ-FR-07: Inventory Sessions**
- Workflow MUST find session folders in configured `sessions_folder`
- Workflow MUST exclude archive folders (names containing `Archive`)
- For each session, collect: name, date, goal (from NOTES.md), status (from PROGRESS.md), artifacts (SPEC, IMPL, TEST, INFO documents and scripts created in session), key findings
- Session inventory runs against the repo containing the sessions folder (typically dev repo in multi-repo mode)

**RLSPROJ-FR-08: Generate Release Notes**
- Release notes MUST be created in product repo's configured `release_notes_dir`
- Workflow MUST check existing files in that directory for naming convention
- Default naming pattern: `RELEASE_NOTES_v{VERSION}_{DATE}.md`
- Release notes MUST include: summary, sessions overview, new skills/workflows, workspace file changes, statistics
- Release notes are committed to product repo before tagging

**RLSPROJ-FR-09: Commit Release Notes**
- Workflow MUST commit release notes to product repo before creating tags
- Commit message format: `docs: add release notes for [TAG]`

**RLSPROJ-FR-10: Create Git Tags**
- Before creating any tag, workflow MUST check if tag already exists locally and on remote. If tag exists at same commit: skip tagging for that repo, log "tag already exists". If tag exists at different commit: halt and report conflict
- In multi-repo mode, workflow MUST use two-phase tagging: (1) create all tags locally first, (2) verify all local tags created successfully, (3) push all tags to remote. If any local tag creation fails: delete all locally created tags and halt
- Tags MUST be pushed atomically (tag and commit together) to ensure consistency within each repo
- Tag annotation: use configured `tag_annotation_template` (default: `Release {TAG}: {SUMMARY}`)
- Tags MUST be pushed to remote before proceeding to GitHub release

**RLSPROJ-FR-11: Version Consistency Gate**
- When `version_gate` is true for a repo, workflow MUST verify version alignment before tagging
- Checks: version source file, binary filename (if binary_build), binary version output (if binary_build), planned tag
- If binary cannot execute (non-zero exit, file not found, permission denied): report as "binary not runnable" (distinct from version mismatch), halt, and instruct user to verify binary platform compatibility
- If version mismatch: workflow MUST halt and instruct user to rebuild
- Gate runs per-repo (each repo with version_gate=true gets its own check)

**RLSPROJ-FR-12: User Confirmation Before GitHub Release**
- Workflow MUST present summary to user: version, sessions count, key artifacts, tag name, binary path (if applicable)
- Workflow MUST ask explicit yes/no before creating GitHub release(s)
- No GitHub release created without explicit user confirmation
- If user declines: workflow skips GitHub release, proceeds to post-release version bump (FR-15)

**RLSPROJ-FR-13: Create GitHub Releases**
- Before creating, workflow MUST check if release already exists for tag (`gh release view [TAG]`). If exists: skip, log "release already exists"
- Product repo: GitHub release with release notes file and optional binary assets
- Dev repo(s): GitHub release per `github_release_notes` config (`file` = use release notes file, `reference` = link to product release)
- Workflow MUST report all release URLs to user
- If `gh` Command Line Interface (CLI) not installed, workflow MUST provide manual release URL

**RLSPROJ-FR-14: Binary Build Step**
- When `binary_build` is true, workflow MUST ask user to build the binary manually
- Workflow MUST NOT execute build tools (build.bat, build.ps1, cargo, etc.)
- Workflow MUST wait for user confirmation that binary is built before proceeding
- Workflow MUST verify binary exists at configured path pattern before proceeding

**RLSPROJ-FR-15: Post-Release Version Bump**
- After all tags pushed and GitHub releases created (or skipped per FR-12), workflow MUST execute post-release bump
- Bump strategy per repo: `devsystem_rename`, `patch_bump`, `minor_bump`, `none`
- `devsystem_rename`: rename `DevSystem[OLD]` folder to `DevSystem[NEW]`, update NOTES.md, sync to `.devin/`
- `patch_bump`: increment patch version in version source file
- `minor_bump`: increment minor version in version source file
- `none`: no bump (tag-only repo)
- Post-release bump is the LAST step of the release process
- Workflow MUST execute post-release bump automatically without asking for user confirmation. This is not a discretionary step
- Bumped changes MUST be committed and pushed

**RLSPROJ-FR-16: Report Results**
- Workflow MUST report: all release URLs, tag names, binary paths (if applicable), session count, artifact count
- In multi-repo mode, report covers all repos

**RLSPROJ-FR-17: Pre-Release Clean Worktree Check**
- Before any release steps, workflow MUST verify all configured repos have clean git worktree (no uncommitted changes)
- If any repo is dirty: workflow MUST halt and report which files are uncommitted in which repo
- User MUST commit or stash changes before re-invoking workflow

**RLSPROJ-FR-18: Config Validation**
- After parsing `[RELEASE_CONFIG]`, workflow MUST validate config before proceeding
- Required global keys MUST be present: `sops_file`, `sessions_folder`, `release_notes_dir`
- Each `[RELEASE_REPO]` block MUST have all required keys: `path`, `role`, `tag_format`, `version_source`, `post_release_bump`
- Enum values MUST be valid: `tag_format` in [`date`, `semver`], `role` in [`product`, `dev`], `version_source` in [`devsystem_folder`, `pyproject_toml`, `package_json`, `none`], `post_release_bump` in [`devsystem_rename`, `patch_bump`, `minor_bump`, `none`]
- Conditional keys MUST be present when parent key requires: `version_file` when `version_source` is file-based, `binary_path_pattern` when `binary_build` is true
- If validation fails: workflow MUST report specific missing or invalid key and halt

**RLSPROJ-FR-19: Run Tests Before Release**
- Before generating release notes, workflow MUST run project tests for each repo where `test_command` is configured
- `test_command` lookup order: (1) `[RELEASE_REPO]` config in `[RELEASE_CONFIG]`, (2) `## Build/Test Rules` section in NOTES.md, (3) skip
- If no test command found for a repo: skip tests for that repo, log "no test command configured"
- If tests fail: workflow MUST halt and report failures. User fixes issues, re-invokes workflow
- In multi-repo mode, product repo tests run before dev repo steps begin

## 5. Non-Functional Requirements

**RLSPROJ-NFR-01: Configurability**
- All workspace-specific parameters MUST be configurable via `[RELEASE_CONFIG]` in NOTES.md
- Zero hardcoded paths, repo names, or version formats in the workflow file itself
- Adding a new workspace requires only adding a `[RELEASE_CONFIG]` section to its NOTES.md

**RLSPROJ-NFR-02: Backward Compatibility**
- Workspaces with existing `[RELEASE_CONFIG]`-less NOTES.md MUST receive clear error message guiding config setup
- Existing SOPS.md post-release procedures remain unchanged - workflow references them by configured file name

**RLSPROJ-NFR-03: Idempotency**
- Re-running workflow after partial failure MUST detect existing tags and skip re-tagging
- Re-running after GitHub release created MUST detect existing release and skip

**RLSPROJ-NFR-04: Safety**
- No destructive git operations without user confirmation
- No build tool execution by agent
- Version gate halts on any mismatch

## 6. Design Decisions

**RLSPROJ-DD-01: Configuration in NOTES.md, not workflow file**
Rationale: NOTES.md is already the workspace configuration file (sessions folder, agent folder, DevSystem version). Release config is workspace-specific, not workflow-generic. Keeping it in NOTES.md means the workflow file never needs editing per-workspace.

**RLSPROJ-DD-02: Product-first ordering**
Rationale: Product repo contains shippable artifacts (binary, release notes). Dev repo contains knowledge artifacts. Product must be tagged and released first so dev repo release can reference the product release URL. In single-repo mode, the one repo is the product.

**RLSPROJ-DD-03: Tag format is per-repo, not per-workspace**
Rationale: In multi-repo workspaces, product may use semver (`v1.0.1`) while dev repo uses date-based tags (`2026-09-05`), or both may use the same format. In single-repo workspaces, date-based tags are common. Per-repo config allows mixed or uniform formats without workflow modification.

**RLSPROJ-DD-04: Version source is per-repo**
Rationale: Product repo may track version in `pyproject.toml` while dev repo has no version file (derives version from product repo's tag). DevSystem workspaces track version via folder name. Each repo needs its own version source declaration.

**RLSPROJ-DD-05: Binary build is always user-managed**
Rationale: Build tools (build.bat, cargo, PyApp) require interactive environments, toolchain checks, and may fail in ways the agent cannot diagnose. User builds manually, agent verifies binary exists. Consistent with workspace `!NOTES.md` Build Rules.

**RLSPROJ-DD-06: Version gate is optional and per-repo**
Rationale: Not all repos have binaries or multiple version sources. The gate is only meaningful when version appears in multiple places (file, binary filename, binary output, tag). Config flag `version_gate: true` activates it per-repo.

**RLSPROJ-DD-07: Release notes always in product repo**
Rationale: Release notes are user-facing documentation. Product repo is the user-facing repo. Dev repo release notes (if any) are minimal and reference the product release. This simplifies the notes generation to one output location.

**RLSPROJ-DD-08: SOPS file name is configurable**
Rationale: Some workspaces use `SOPS.md`, others use `_SOPS.md`. Hardcoding either name breaks workspaces using the other. Config field `sops_file` lets each workspace specify its own.

**RLSPROJ-DD-09: Post-release bump strategy is per-repo**
Rationale: DevSystem workspaces rename a version folder (`DevSystemV4.3` -> `DevSystemV4.4`). Product repos bump a version field in a file (`pyproject.toml`). Dev repos may not need any bump. Per-repo `post_release_bump` config handles all three cases.

**RLSPROJ-DD-10: Sessions folder is configurable**
Rationale: Workspaces use different session folder names (e.g., `_PrivateSessions`, `_Sessions`). The workflow must not assume a fixed folder name.

**RLSPROJ-DD-11: No new TOPIC for SOPS integration**
Rationale: SOPS files are workspace-specific and already maintained. The workflow references them by configured name. No need to create a unified SOPS spec - each workspace has its own operational procedures.

## 7. Implementation Guarantees

**RLSPROJ-IG-01:** The same `project-release.md` file deployed to any workspace with a valid `[RELEASE_CONFIG]` section will execute correctly without modification.

**RLSPROJ-IG-02:** No git tag is created before release notes are committed to the product repo.

**RLSPROJ-IG-03:** No GitHub release is created without explicit user confirmation.

**RLSPROJ-IG-04:** Post-release version bump executes only after all tags are pushed and GitHub releases are created.

**RLSPROJ-IG-05:** Agent never executes build tools (build.bat, build.ps1, cargo, etc.) regardless of config.

## 8. Key Mechanisms

### Config Parsing

The workflow reads the `[RELEASE_CONFIG]` section from NOTES.md. The section uses a simple key-value format with nested repo entries:

```
## Release Configuration

[RELEASE_CONFIG]
sops_file: [SOPS_FILE]
sessions_folder: [SESSIONS_FOLDER]
release_notes_dir: [RELEASE_NOTES_FOLDER]
release_notes_naming: RELEASE_NOTES_v{VERSION}_{DATE}.md

[RELEASE_REPO: product]
path: [WORKSPACE_FOLDER]
role: product
tag_format: date
version_source: devsystem_folder
post_release_bump: devsystem_rename
binary_build: false
github_release: true

[RELEASE_REPO: dev]
path: [WORKSPACE_FOLDER]
role: dev
tag_format: semver
version_source: pyproject_toml
version_file: [PRODUCT_REPO_FOLDER]\pyproject.toml
post_release_bump: patch_bump
binary_build: true
binary_path_pattern: dist/[appname]-{version}-win-x64.exe
version_gate: true
github_release: true
github_release_assets:
  - dist/[appname]-{version}-win-x64.exe
  - dist/SHA256SUMS.txt
```

### Version Extraction

- `devsystem_folder`: Parse `[PRODUCT_VERSION]: X.Y` from NOTES.md, extract `X.Y`
- `pyproject_toml`: Parse `version = "X.Y.Z"` from configured version_file
- `package_json`: Parse `"version": "X.Y.Z"` from configured version_file
- `none`: No version extraction; tag is the version identifier

### Tag Derivation

- `date` format: `YYYY-MM-DD` from current date (or user-specified date)
- `semver` format: `vX.Y.Z` from version source after bump

### Release Notes Template

The workflow uses a standard release notes template (defined by the workflow, not per-workspace) with placeholders for: date, version, session count, session details, skills, workflows, statistics.

### Post-Release Bump Execution

- `devsystem_rename`: Read current version from NOTES.md, increment minor, rename folder, update NOTES.md, sync to `.devin/`, commit, push
- `patch_bump`: Read version from version_file, increment patch, write back, commit, push
- `minor_bump`: Read version from version_file, increment minor, reset patch to 0, write back, commit, push
- `none`: Skip

## 9. Action Flow

### Context Detection

Before any release steps, workflow MUST detect workspace context using the same logic as `/prime` Step 4 and `@skills:workspace-management` WORKSPACE-GUIDES.md:

1. Detect workspace mode: `main.code-workspace` exists → WORKSPACE mode (multi-repo), else → SINGLE-PROJECT or MONOREPO
2. Read `[RELEASE_CONFIG]` from workspace NOTES.md (or `!NOTES.md`)
3. If no `[RELEASE_CONFIG]` section: error and halt
4. Count `[RELEASE_REPO]` blocks: 1 → single-repo flow, 2+ → multi-repo flow
5. Validate config (FR-18)
6. Verify all configured repos have clean worktree (FR-17)
7. Read SOPS file (name from config) for workspace-specific procedures and deviations
8. Resolve repo paths using workspace constants (`[WORKSPACE_FOLDER]`, `[PRODUCT_REPO_FOLDER]`, `[WORKSPACE_FOLDER]`) when config uses them

### Single-Repo Release Flow

```
User invokes /project-release
├─> Detect workspace context (see Context Detection above)
├─> Read SOPS file for workspace-specific procedures
├─> Run tests (FR-19)
│   └─> If tests fail: halt, report failures
├─> Determine release scope (git log since last tag) (FR-06)
├─> Inventory sessions from configured sessions_folder (FR-07)
├─> Generate release notes (FR-08)
│   └─> Write to product repo's release_notes_dir
├─> Commit release notes to product repo (FR-09)
├─> [If binary_build: true]
│   ├─> Ask user to build binary (FR-14)
│   └─> Verify binary exists at configured path
├─> [If version_gate: true]
│   └─> Run version consistency check (FR-11)
│       └─> If mismatch or binary not runnable: halt
├─> Check if tag exists (FR-10 pre-check)
├─> Create git tag in product repo (FR-10)
├─> Push tag and commits to remote
├─> Present summary to user (FR-12)
│   └─> Ask: "Create GitHub release? (y/n)"
├─> [If confirmed]
│   └─> Create GitHub release with notes and assets (FR-13)
├─> Execute post-release version bump without asking (FR-15)
│   └─> Commit and push bump
└─> Report results (FR-16)
```

### Multi-Repo Release Flow

```
User invokes /project-release
├─> Detect workspace context (see Context Detection above)
├─> Read SOPS file for workspace-specific procedures
├─> Determine release scope for each repo (FR-06)
├─> Inventory sessions (from configured sessions_folder in dev repo) (FR-07)
│
├─> [PRODUCT REPO]
│   ├─> Run tests (FR-19)
│   │   └─> If tests fail: halt
│   ├─> Generate release notes (FR-08)
│   │   └─> Write to PRODUCT repo's release_notes_dir
│   ├─> Commit release notes to product repo (FR-09)
│   ├─> [If binary_build: true]
│   │   ├─> Ask user to build binary (FR-14)
│   │   └─> Verify binary exists
│   ├─> [If version_gate: true]
│   │   └─> Run version consistency check for product repo (FR-11)
│   │       └─> If mismatch or binary not runnable: halt
│   └─> (Tagging deferred to two-phase step below)
│
├─> [DEV REPO]
│   ├─> Run tests (FR-19)
│   │   └─> If tests fail: halt
│   ├─> Research last evaluation results (from session artifacts, llm-evaluation skill outputs)
│   ├─> Generate dev release notes referencing product release
│   ├─> Commit dev release notes
│   └─> (Tagging deferred to two-phase step below)
│
├─> [TWO-PHASE TAGGING] (FR-10)
│   ├─> Phase 1: Create all tags locally (product + dev)
│   │   └─> If any tag creation fails: delete all local tags, halt
│   ├─> Phase 2: Push all tags to remote (product first, then dev)
│   │   └─> Use git push --atomic for tag + commit per repo
│   └─> Present summary to user (FR-12)
│       └─> Ask: "Create GitHub releases? (y/n)"
│
├─> [If confirmed]
│   ├─> Check for existing GitHub releases (FR-13 idempotency)
│   ├─> Create product GitHub release with notes and binary assets
│   └─> Create dev GitHub release (notes reference product release)
│
├─> Execute post-release version bump per repo without asking (FR-15)
│   ├─> Product repo bump (if configured)
│   └─> Dev repo bump (if configured)
│
└─> Report all results (FR-16): all release URLs, tags, binary paths
```

## 10. Configuration Schema

### [RELEASE_CONFIG] Section Format

The `[RELEASE_CONFIG]` section uses a simple text-based key-value format readable by both humans and agents. It is placed in the workspace's NOTES.md (or `!NOTES.md`) under a `## Release Configuration` heading.

### Global Config Keys

- `sops_file` - (required) Name of SOPS file in workspace root (e.g., `SOPS.md`, `_SOPS.md`)
- `sessions_folder` - (required) Session folder name or path relative to `[WORKSPACE_FOLDER]`. May use `[SESSIONS_FOLDER]` constant
- `release_notes_dir` - (required) Path relative to product repo root where release notes are stored. May use `[PRODUCT_DOCS_FOLDER]` constant
- `release_notes_naming` - (optional) Filename pattern. Default: `RELEASE_NOTES_v{VERSION}_{DATE}.md`. Placeholders: `{VERSION}`, `{DATE}`
- `tag_annotation_template` - (optional) Template for git tag annotation. Default: `Release {TAG}: {SUMMARY}`

### Per-Repo Config Keys

Each repo is defined in a `[RELEASE_REPO: <name>]` block:

- `path` - (required) Repo root path. Must use workspace constants (e.g., `[WORKSPACE_FOLDER]`, `[PRODUCT_REPO_FOLDER]`, `[WORKSPACE_FOLDER]`)
- `role` - (required) `product` or `dev`
- `tag_format` - (required) `date` or `semver`
- `version_source` - (required) `devsystem_folder`, `pyproject_toml`, `package_json`, or `none`
- `version_file` - (conditional) Path to version file. Must use workspace constants (e.g., `[PRODUCT_REPO_FOLDER]\pyproject.toml`). Required when version_source is file-based
- `post_release_bump` - (required) `devsystem_rename`, `patch_bump`, `minor_bump`, or `none`
- `binary_build` - (optional) `true` or `false`. Default: `false`
- `binary_path_pattern` - (conditional) Pattern for binary path relative to repo root. Required when binary_build is true. Placeholder: `{version}`
- `version_gate` - (optional) `true` or `false`. Default: `false`
- `test_command` - (optional) Shell command to run tests for this repo. If absent: tests skipped for that repo
- `github_release` - (optional) `true` or `false`. Default: `true`
- `github_release_assets` - (optional) List of file paths to attach as release assets. One per line, prefixed with `- `
- `github_release_notes` - (optional) `file` (use release notes file) or `reference` (reference product release). Default: `file` for product, `reference` for dev

### Example: Single-Repo, Date-Based

```
## Release Configuration

[RELEASE_CONFIG]
sops_file: [SOPS_FILE]
sessions_folder: [SESSIONS_FOLDER]
release_notes_dir: [RELEASE_NOTES_FOLDER]
release_notes_naming: RELEASE_NOTES_v{VERSION}_{DATE}.md

[RELEASE_REPO: product]
path: [WORKSPACE_FOLDER]
role: product
tag_format: date
version_source: devsystem_folder
post_release_bump: devsystem_rename
github_release: true
```

### Example: Multi-Repo, Semver

```
## Release Configuration

[RELEASE_CONFIG]
sops_file: [SOPS_FILE]
sessions_folder: [SESSIONS_FOLDER]
release_notes_dir: [RELEASE_NOTES_FOLDER]
release_notes_naming: RELEASE_NOTES_v{VERSION}_{DATE}.md

[RELEASE_REPO: product]
path: [PRODUCT_REPO_FOLDER]
role: product
tag_format: semver
version_source: pyproject_toml
version_file: [PRODUCT_REPO_FOLDER]\pyproject.toml
post_release_bump: patch_bump
binary_build: true
binary_path_pattern: dist/[appname]-{version}-win-x64.exe
version_gate: true
github_release: true
github_release_assets:
  - dist/[appname]-{version}-win-x64.exe
  - dist/SHA256SUMS.txt

[RELEASE_REPO: dev]
path: [WORKSPACE_FOLDER]
role: dev
tag_format: semver
version_source: none
post_release_bump: none
github_release: true
github_release_notes: reference
```

### Example: Single-Repo, Date-Based (Alternative Sessions Folder)

```
## Release Configuration

[RELEASE_CONFIG]
sops_file: [SOPS_FILE]
sessions_folder: [SESSIONS_FOLDER]
release_notes_dir: [RELEASE_NOTES_FOLDER]
release_notes_naming: RELEASE_NOTES_v{VERSION}_{DATE}.md

[RELEASE_REPO: product]
path: [WORKSPACE_FOLDER]
role: product
tag_format: date
version_source: devsystem_folder
post_release_bump: devsystem_rename
github_release: true
```

### NOTES.md Template

This section integrates with `DEV_REPO_NOTES_TEMPLATE.md` from `@skills:workspace-management` and `NOTES_TEMPLATE.md` from `@skills:session-management`. Add the following to NOTES.md after existing sections (e.g., after `## Build/Test Rules`):

**Step 1: Add release constants to `## Workspace Constants` section**

These constants compose from existing workspace constants defined in `DEV_REPO_NOTES_TEMPLATE.md`:

```
# Release-specific constants (compose from workspace constants above)
[SOPS_FILE]: SOPS.md
[RELEASE_NOTES_FOLDER]: [PRODUCT_DOCS_FOLDER]\ReleaseNotes
```

Instructions: Adjust values as needed. `[SOPS_FILE]` is the SOPS filename (`SOPS.md` or `_SOPS.md`). `[RELEASE_NOTES_FOLDER]` composes from `[PRODUCT_DOCS_FOLDER]` and a `ReleaseNotes` subfolder. `sessions_folder` uses `[SESSIONS_FOLDER]` from session-management skill directly.

**Step 2: Add `## Release Configuration` section**

```
## Release Configuration

[RELEASE_CONFIG]
sops_file: [SOPS_FILE]
sessions_folder: [SESSIONS_FOLDER]
release_notes_dir: [RELEASE_NOTES_FOLDER]
release_notes_naming: RELEASE_NOTES_v{VERSION}_{DATE}.md
tag_annotation_template: Release {TAG}: {SUMMARY}

# Single-repo: one [RELEASE_REPO] block
# Multi-repo: product block first, then dev block(s)
# All paths use workspace constants from ## Workspace Constants section

[RELEASE_REPO: product]
path: [WORKSPACE_FOLDER]
role: product
tag_format: [date or semver]
version_source: [devsystem_folder or pyproject_toml or package_json or none]
# version_file: [PRODUCT_REPO_FOLDER]\pyproject.toml  # Required when version_source is pyproject_toml or package_json
post_release_bump: [devsystem_rename or patch_bump or minor_bump or none]
# binary_build: true     # Uncomment if product has a binary
# binary_path_pattern: dist/[appname]-{version}-win-x64.exe  # Required when binary_build is true
# version_gate: true     # Uncomment if version consistency check needed
# test_command: [command]  # Uncomment if tests not already defined in ## Build/Test Rules
github_release: true
# github_release_assets:  # Uncomment if binary assets to attach
#   - dist/[appname]-{version}-win-x64.exe

# [RELEASE_REPO: dev]    # Uncomment for multi-repo
# path: [WORKSPACE_FOLDER]
# role: dev
# tag_format: [date or semver]
# version_source: [devsystem_folder or pyproject_toml or package_json or none]
# post_release_bump: [devsystem_rename or patch_bump or minor_bump or none]
# test_command: [command]
# github_release: true
# github_release_notes: reference  # Dev repo references product release
```

**Integration with existing NOTES.md sections:**
- `## Workspace Constants`: All path values in `[RELEASE_CONFIG]` reference constants defined here. Release-specific constants compose from existing ones (e.g., `[RELEASE_NOTES_FOLDER]` from `[PRODUCT_DOCS_FOLDER]`)
- `## Build/Test Rules`: If `test_command` is already defined there, omit it from `[RELEASE_REPO]` config. Workflow reads `test_command` from `[RELEASE_CONFIG]` first, falls back to `## Build/Test Rules` section
- `## Project Info`: Workspace mode (WORKSPACE, SINGLE-PROJECT, MONOREPO) is already declared here. Context Detection step 1 reads this to determine branching
- `[SESSIONS_FOLDER]`: Defined by `@skills:session-management`, defaults to `[WORKSPACE_FOLDER]`. Used directly as `sessions_folder` in `[RELEASE_CONFIG]`

### Config Decision Guide

**When to use `date` vs `semver` tag format:**
- `date`: Single-repo DevSystem workspaces, knowledge repos, no binary releases. Tags like `2026-09-05` convey "what changed since last date" without version management overhead
- `semver`: Product repos with binaries, public APIs, or semantic versioning expectations. Tags like `v1.0.1` convey breaking/minor/patch intent

**When to use each `version_source`:**
- `devsystem_folder`: Workspace tracks version via DevSystem folder name (e.g., `DevSystemV4.3` -> version `4.3`). Use for DevSystem-only workspaces
- `pyproject_toml`: Python project with version in `pyproject.toml`. Requires `version_file` path
- `package_json`: Node.js project with version in `package.json`. Requires `version_file` path
- `none`: Repo has no version file. Version is derived from tag or product repo. Use for dev repos that mirror product version

**When to use each `post_release_bump`:**
- `devsystem_rename`: DevSystem workspaces. Renames `DevSystemVX.Y` folder to next minor, updates NOTES.md, syncs to `.devin/`. Follows SOPS SOP 7 or equivalent
- `patch_bump`: Product repos after patch release. Increments `X.Y.Z` to `X.Y.Z+1` in version file
- `minor_bump`: Product repos after minor release. Increments `X.Y.Z` to `X.Y+1.0` in version file
- `none`: Tag-only repos, dev repos with no version file, or repos where bump is handled externally

**When to enable `binary_build`:**
- Enable when product repo ships a binary (exe, app, binary distribution). Workflow asks user to build, verifies binary exists at `binary_path_pattern`
- Disable for knowledge repos, DevSystem-only workspaces, or repos without binary artifacts

**When to enable `version_gate`:**
- Enable when version appears in multiple places (version file, binary filename, binary `--version` output, tag). Gate catches mismatches before tagging
- Disable for repos with single version source or no binary

**When to use `github_release_notes: reference` vs `file`:**
- `file` (default for product): GitHub release body contains full release notes content
- `reference` (default for dev): GitHub release body links to product repo's release URL. Use for dev repos that don't need separate notes

## 11. Technical Constraints

- Workflow file contains zero hardcoded repo paths, version formats, or SOPS file names
- All paths in config use workspace constants (e.g., `[WORKSPACE_FOLDER]`, `[PRODUCT_REPO_FOLDER]`, `[WORKSPACE_FOLDER]`, `[RELEASE_NOTES_FOLDER]`). No absolute paths in config values
- Git operations use `git -C <path>` syntax for multi-repo support (no `cd` commands)
- Release notes template is defined by the workflow (not per-workspace) because it is generic across all workspaces
- The `[RELEASE_CONFIG]` section format is intentionally non-YAML to match the existing NOTES.md key-value style (e.g., `[SESSIONS_FOLDER]`, `[AGENT_FOLDER]`)
- Config parsing is line-based: keys before `[RELEASE_REPO:` blocks are global, keys inside blocks are per-repo
- The workflow must handle the case where NOTES.md uses `!NOTES.md` naming (priority file) vs `NOTES.md`
- Post-release bump for `devsystem_rename` must follow SOPS.md SOP 7 or equivalent procedure in the workspace's SOPS file

## 12. Logging Requirements

This workflow produces user-facing output (progress messages, summaries, error reports). No server or script-level logging is applicable.

**User-Facing Output (UF):**
- Workflow MUST announce each phase before executing (context detection, tests, release notes, build, version gate, tagging, GitHub release, bump)
- Workflow MUST report success or failure of each step with specific details (tag name, release URL, binary path)
- Error messages MUST state what failed, why, and recovery action (per Failure Recovery section)
- Final report (FR-16) MUST be emitted in chat, not to a file

## 13. Failure Recovery

### Principles

- Never delete remote tags. Tags on `origin` are immutable - treat as published
- Never force-push tags. A moved tag breaks downstream consumers and FR-06 last-tag detection
- When in doubt: halt and report. Agent MUST NOT attempt destructive recovery without user guidance

### Per-Failure-Point Recovery

**Release notes commit failed:**
- Detection: `git commit` returns non-zero
- Recovery: Abort release. Release notes file may be staged but uncommitted. User fixes issue (e.g., pre-commit hook failure) and re-invokes workflow. Re-run detects no tag exists, re-commits notes

**Tag creation failed (local):**
- Detection: `git tag` returns non-zero
- Recovery (single-repo): Abort. No tag exists locally or remotely. User fixes issue and re-invokes
- Recovery (multi-repo): Delete all locally created tags from this run (`git tag -d [TAG]` per repo). Abort. User fixes issue and re-invokes

**Tag push failed:**
- Detection: `git push` returns non-zero
- Recovery: Local tag exists but remote does not. Check if remote tag exists at same commit (`git ls-remote --tags origin [TAG]`). If yes: log "tag already on remote", continue. If no: retry push once. If retry fails: abort, report push error, leave local tag in place. User resolves remote issue (auth, permissions, branch protection) and re-invokes

**GitHub release creation failed:**
- Detection: `gh release create` returns non-zero or `gh` not installed
- Recovery: Tags are already pushed (immutable). Report failure reason. If `gh` not installed: provide manual release URL (`https://github.com/[OWNER]/[REPO]/releases/new?tag=[TAG]`). User creates release manually. Post-release bump (FR-15) proceeds regardless - GitHub release is not a gate for version bump

**Post-release bump failed:**
- Detection: Version file write fails, folder rename fails, or commit/push fails
- Recovery: Tags and GitHub releases (if created) are immutable. Report failure. If folder rename partially completed: user manually finishes rename and updates NOTES.md. If version file write failed: no state changed, user fixes and re-invokes. If commit failed: user resolves and commits manually. Re-run detects existing tag, skips tagging, retries bump

## 14. Document History

**[2026-09-06 23:35]**
- Added: `@skills:session-management` dependency for `[SESSIONS_FOLDER]` constant
- Added: Release Constants subsection in NOTES.md template (`SOPS.md`, `[RELEASE_NOTES_FOLDER]`) composing from existing workspace constants. `sessions_folder` uses `[SESSIONS_FOLDER]` directly
- Changed: All config examples (Section 8, Section 10) use release constants instead of literal values
- Changed: Config schema requires workspace constants for all path values (no absolute paths)
- Changed: Domain objects ReleaseConfig and RepoConfig updated to reference workspace constants
- Changed: Technical Constraint updated: all paths use workspace constants, no absolute paths
- Changed: NOTES.md template now 2-step: (1) add release constants to Workspace Constants, (2) add Release Configuration section

**[2026-09-06 23:20]**
- Added: `@skills:workspace-management` dependency for workspace mode detection and constants
- Changed: Context Detection step 1 now uses workspace mode detection logic (main.code-workspace) per WORKSPACE-GUIDES.md
- Changed: All config examples use workspace constants (`[WORKSPACE_FOLDER]`, `[PRODUCT_REPO_FOLDER]`, `[WORKSPACE_FOLDER]`) instead of absolute paths (WS-CT-02)
- Changed: NOTES.md template integrates with DEV_REPO_NOTES_TEMPLATE.md, references existing ## Workspace Constants and ## Build/Test Rules sections
- Changed: FR-19 test_command lookup order: [RELEASE_CONFIG] first, falls back to ## Build/Test Rules section in NOTES.md
- Changed: RepoConfig.path and Per-Repo Config path now accept workspace constants, not just absolute paths
- Changed: Technical Constraint on paths updated to allow workspace constants
- Added: Context Detection step 8 resolves workspace constants in repo paths

**[2026-09-06 23:10]**
- Added: Section 10 NOTES.md Template with copy-paste `[RELEASE_CONFIG]` placeholders and inline comments
- Added: Section 10 Config Decision Guide explaining when to use each tag format, version source, bump strategy, binary build, version gate, and GitHub release notes mode

**[2026-09-06 23:00]**
- Added: Section 12 Logging Requirements (SPEC-LG-01)
- Fixed: SPEC-CT-02 - abstracted git commands in FR-06, FR-10, FR-17 to requirement-level statements
- Fixed: SOCAS-01 - domain objects RepoConfig and ReleaseConfig missing properties (test_command, github_release_notes, tag_annotation_template)
- Fixed: SOCAS-02 - "build or ship" undefined term in action flows replaced with "build"
- Fixed: SOCAS-06 - dev repo tests missing in multi-repo action flow (FR-19 says "for each repo")
- Fixed: SOCAS-06 - FR-19 SOPS reference removed, test_command only from config
- Fixed: SOCAS-10 - DD-03 rationale now shows mixed-format case (product semver, dev date-based)

**[2026-09-06 22:15]**
- Added: FR-19 Run Tests Before Release with `test_command` config key
- Added: Section 9 Context Detection step (like `/prime` Step 4) before branching into single-repo or multi-repo flow
- Added: FR-13 idempotency check for existing GitHub releases
- Changed: FR-03 fixed contradiction with FR-10 two-phase tagging - dev repos tagged after product, all tags created locally first
- Changed: FR-10 tag annotation now references configured `tag_annotation_template` instead of hardcoded format
- Changed: Section 9 completely rewritten - both action flows restructured with correct step order (context detection → tests → release notes → build → version gate → tag → release → bump)
- Changed: Multi-repo flow adds DEV REPO section with research last evaluation results step
- Changed: Multi-repo flow removes contradictory sequential tagging from PRODUCT REPO section
- Fixed: DD-03, DD-05, DD-08, DD-10 real project names replaced with generic descriptions (privacy gate)
- Fixed: Domain object `binary_path_pattern` example replaced generic app name (privacy gate)
- Added: `test_command` to Per-Repo Config Keys in Section 10

**[2026-09-06 00:15]**
- Added: FR-17 Pre-release clean worktree check (RV-004)
- Added: FR-18 Config validation (RV-006)
- Added: Section 12 Failure Recovery with per-failure-point procedures (RV-001)
- Changed: FR-10 rewritten with two-phase tagging, tag-exists pre-check, `git push --atomic` (RV-002, RV-005)
- Changed: FR-11 distinguishes "binary not runnable" from version mismatch (RV-007)
- Changed: FR-15 adds "without asking for user confirmation" (RV-003)
- Changed: Section 8 release notes template wording from "embedded in workflow file" to "defined by the workflow" (RV-008)
- Changed: All config examples and diagrams use generic placeholders instead of real paths (RV-009)
- Changed: Multi-repo action flow updated with two-phase tagging

**[2026-09-05 23:15]**
- Fixed: FR-08 placeholder format aligned with domain object and config schema (`{VERSION}_{DATE}`)
- Fixed: FR-03 tag derivation reworded - dev repo independently derives from own version_source, not from product tag
- Fixed: FR-13 references `github_release_notes` config field instead of ambiguous "or"
- Fixed: FR-15 accounts for user declining GitHub release (FR-12)
- Fixed: AP-PR-06 acronyms expanded on first use (SOP, CLI)
- Fixed: FR-07 artifacts defined as SPEC, IMPL, TEST, INFO documents and scripts

**[2026-09-05 22:45]**
- Fixed: FR-06 first-release handling (no previous tags)
- Fixed: FR-12 consequence when user declines GitHub release
- Fixed: FR-05 vs FR-15 pre-tagging vs post-release bump ambiguity
- Fixed: ReleaseNotes naming placeholder consistency (`{VERSION}` everywhere)
- Fixed: FR-03 tag derivation for differing tag formats

**[2026-09-05 22:30]**
- Initial specification created
