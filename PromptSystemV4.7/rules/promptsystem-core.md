---
trigger: always_on
---

# PromptSystem Core

Core definitions and structure for the development system.

Section markers `<!-- START: Skill: X, File: Y -->` name where to read more: file `Y` of @skills:X. `Core` = defined here only.

## Definitions

### Core Concepts

<!-- START: Core -->
- **[WORKSPACE]**: The workspace root folder
- **[PROJECT]**: If Monorepo (workspace contains multiple projects), the project subfolder. No Monorepo: Workspace = Project
- **[SESSION]**: All context belonging to a work session - folder, files, conversations, commits, and tracking files (notes, problems, progress)
<!-- END: Core -->

<!-- START: Skill: workspace-management, File: WORKSPACE-GUIDES.md -->
- **[PRODUCT_VERSION]**: Current product version string (e.g., `4.3`, `1.2.0`, `2026-03-15`). Composes `[PROMPTSYSTEM_FOLDER]` as `[WORKSPACE_FOLDER]\PromptSystem[PRODUCT_VERSION]`; used for release version extraction
- **[DEV_SPECS_FOLDER]**: `[WORKSPACE_FOLDER]/specs/` - shared specifications, design guidelines, and SOPs
- **[DEV_KNOWLEDGE_FOLDER]**: `[WORKSPACE_FOLDER]/knowledge/` - reference documents organized as knowledge bundles (topic folders with `.md` files)
- **[PROMPTSYSTEM_SYNC_CONFIG]**: `promptsystem-sync.json` at `[WORKSPACE_FOLDER]` root, only in SYNCED repos. Single source of truth for sync configuration; managed by `sync.ps1` and `/sync workspace`
- Specs and knowledge: synced from upstream in SYNCED repos, authored locally in SELF-CONTAINED repos
<!-- END: Skill: workspace-management -->

<!-- START: Core -->

### Agent Folder

**[AGENT_FOLDER]** location depends on agent (e.g., `.devin/`, `.claude/`, `.agent/`); defined in the agent-specific rule file.

### Configuration

- **[RULES]**: The current set of agent rules in `[AGENT_FOLDER]/rules/`
- **[WORKFLOWS]**: The current set of agent workflows in `[AGENT_FOLDER]/workflows/`. List by purpose and quality pipelines (VCRIV, FACRIV): `tools-and-skills.md`
- **[SKILLS]**: Agent Skills in `[AGENT_FOLDER]/skills/`
- **[GRUC]**: Guides, Rules, Checks - pre-calculated compliance criteria. GUIDE + RULES in each skill folder; CHECKS in each skill folder (for skills) or `drift-control/` (for workflows). Exception: `write-documents` and `analysis-methods` maintain consolidated checks.

<!-- END: Core -->

<!-- START: Skill: promptsystem, File: PROMPTSYSTEM_IDS.md -->

### Document Types

- **[INFO]** (IN): Information gathering from web research, option and code analysis, reading documents
- **[SPEC]** (SP): A specification conforming to defined rules
- **[IMPL]** (IP): An implementation plan
- SPEC and IMPL: when implemented, must be reverse-updated (synced) from verified code changes
- **[TEST]** (TP): Test plans suffixed to corresponding SPEC or IMPL
- **[TASKS]** (TK): Partitioned task lists from IMPL/TEST plans, created via `/write-tasks-plan`
- Doc IDs (`CRAWLENG-SP01`): `promptsystem-ids.md`
<!-- END: Skill: promptsystem -->

<!-- START: Core -->

### Tracking Documents

One of each type per scope (workspace, project, session).

- **[NOTES]**, **[PROGRESS]**: Important information and progress tracking. Agent MUST read both to avoid unintentional behavior
- **[PROBLEMS]**: Problem tracking. Each session tracks issues in its own `PROBLEMS.md`. On `/session-finalize`, sync to project [PROBLEMS]
- **[FAILS]**: Failure log - lessons learned from past mistakes. Agent MUST read during `/prime` to avoid repeating errors (except when using the `_` prefix). Never delete entries unconfirmed, only append or mark as resolved.

### Placeholders

- **[ACTOR]**: Decision-making entity (default: user, in `/go` autonomous mode: agent)

### MNF (MUST-NOT-FORGET) Technique

Prevents critical oversights during task execution.

- **Planning phase**: create a `MUST-NOT-FORGET` list (5-15 items max; name must not be changed, to be greppable). Collect items from FAILS.md, learnings, rules, specs, user instructions. Include it in the plan or at the top of the working document
- **Completion phase**: review each MNF item before marking the task done. Verify compliance or document why the item doesn't apply. Update FAILS.md if any MNF item was violated

### Complexity Levels

Maps to semantic versioning:

- **COMPLEXITY-LOW**: Single file, clear scope, no dependencies → patch version
- **COMPLEXITY-MEDIUM**: Multiple files, some dependencies, backward compatible → minor version
- **COMPLEXITY-HIGH**: Breaking changes, new patterns, external APIs, architecture → major version

### Operation Modes

- **IMPL-CODEBASE** (default): Implement in existing codebase. For SPEC, IMPL, TEST, [IMPLEMENT], HOTFIX, BUGFIX. Output: project source folders (`src/`, etc.). Affects existing code, configuration, runtime
- **IMPL-ISOLATED**: Implement separately from existing codebase. For [PROVE], Proofs of Concept (POCs), prototypes, self-contained test scripts. Output: `[SESSION_FOLDER]/`, `[SESSION_FOLDER]/_poc/`, `T##_` (Topic) folders, or `S##_` (Step) folders. Existing code/config/runtime MUST NOT be affected. NEVER create folders in workspace root. **REQUIRES SESSION**: if no session exists, run `/session-new` first
<!-- END: Core -->

<!-- START: Skill: workspace-management, File: WORKSPACE-GUIDES.md -->

## Workspace Scenarios

- **Dimension 1 - Project Structure**: SINGLE-PROJECT (workspace contains one project), MONOREPO (multiple independent projects), WORKSPACE (workspace root with multiple independent repos, not monorepo; detected by presence of a `*.code-workspace` file)
- **Dimension 2 - Version Strategy**: SINGLE-VERSION (one active version, no migration), MULTI-VERSION (side-by-side versions, e.g., V1 and V2 coexisting)
<!-- END: Skill: workspace-management -->

<!-- START: Skill: session-management, File: SKILL.md -->
- **Dimension 3 - Work Mode**: SESSION-MODE (time-limited session with specific goals), PROJECT-MODE (work spans entire project without session boundaries)
<!-- END: Skill: session-management -->

<!-- START: Skill: workspace-management, File: WORKSPACE-GUIDES.md -->
- **Dimension 4 - Sync Relationship**: SYNCED (repo participates in sync dependency tree, has upstream/downstream), SELF-CONTAINED (repo manages all content locally, no sync relationships)
- **Dimension 5 - Workspace Type**: SOFTWARE-DEV (has product repo, build/test rules, runtime environment, release configuration; Dimension 1 applies), GENERAL (research, documentation, finance; no product repo, no build infrastructure, no release configuration; code allowed only in session folders (POCs, analysis scripts); defaults to IMPL-ISOLATED; Dimension 1 = N/A)

## Folder Structure

- **Single project, workspace root**: `[AGENT_FOLDER]/` (`rules/`, `workflows/`, `skills/`), `specs/` (workspace-level specs), `docs/` (INFO, research, how-tos), `src/`, `_archive_gitignore/` (archived sessions, not versioned), tracking files `!NOTES.md`, `PROBLEMS.md`, `!PROGRESS.md`, `FAILS.md`
- **Session folder** `_[SESSION_FOLDER]/` (starts with underscore): `_agentwork/`, `_INFO_*.md`, `_SPEC_*.md`, `_IMPL_*.md`, `_TEST_*.md`, `NOTES.md`, `PROBLEMS.md`, `PROGRESS.md`, `FAILS.md`
- **Monorepo**: same root, but each `[PROJECT]/` folder holds its own sessions, `src/`, and tracking files
- **Multi-Repo Workspace**: same root plus `[folder-name].code-workspace`, without `src/`; product code lives in `[PRODUCT_REPO_FOLDER]/` (`src/`, `docs/`, `README.md`), which may be outside `[WORKSPACE_FOLDER]`

<!-- END: Skill: workspace-management -->

<!-- START: Skill: workspace-management, File: WORKSPACE-RULES.md -->

## Document Placement

Two folders for workspace-level documents. Enforceable rules: WS-DP-01 through WS-DP-06.

- **specs/** - Verifiable agent instructions: _SPEC_*, _IMPL_*, _TEST_* files, and unprefixed rules files with enforceable IDs. _TASKS_* files are session-scoped and stay in session folders
- **docs/** - Explanatory knowledge: _INFO_* files and unprefixed research articles. Read for understanding, not for execution verification
- Decision rule: "Can the agent verify compliance against this document?" If yes, specs/. Does it explain why/how something works? docs/. Exception: an _INFO_* file may reside in specs/ if a _SPEC_* file in the same workspace lists it under "Depends on"
- Both folders are optional (WS-DP-06); `/prime` does not create them. Folders exist: documents MUST be placed per the rules above. No folders and no active session: workspace folder root. Active session: session-scoped documents (_IMPL_*, _TEST_*, _TASKS_*) go in the session folder
- **OPTIONS and DRAFT Placement (DRSYNART-DD-36)**: `[ID]-OPTIONS-NN_` and `[ID]-DRAFT-NN_` files are deliverables in the active working folder, never in `_agentwork/`; `/cleanup` must not delete them

<!-- END: Skill: workspace-management -->

<!-- START: Skill: promptsystem, File: PROMPTSYSTEM_AGENT_FOLDERS.md -->

## File Naming Conventions

- **Priority files (`!` prefix)**: high relevance. Must be treated with extra attention during `/prime`
- **Ignored files (`_` prefix)**: skipped by automatic priming workflows. Use for session-specific, WIP, or archived content. Single `_` prefix files are deliverables (INFO, SPEC, IMPL, TEST, TASKS); never auto-deleted
- **Scaffolding files (`__` prefix)**: process artifacts that workflows and skills auto-create during execution (STRUTs, TASKS, templates for self-tracking). Persist during active work, deleted by `/cleanup` after the goal is reached. Documents the user explicitly creates via `/write-tasks-plan`, `/write-strut`, `/write-spec`, etc. are deliverables (no `__`)
- **Temp files (`.tmp_` prefix)**: single-run temp (scripts, rebuildable folders). Deleted within the same workflow or by `/cleanup`
- **Hidden files (`.` prefix)**: Unix convention - hidden from directory listings
- **Git exclusion suffix (`_gitignore`)**: append before the extension to exclude any file or folder from git without editing `.gitignore`: `data_gitignore.json`, `_download_gitignore/`. Patterns in `.gitignore`: `*_gitignore.*`, `*_gitignore/`, `.tmp_*`, `_agentwork/`
<!-- END: Skill: promptsystem -->

<!-- START: Skill: workspace-management, File: WORKSPACE-GUIDES.md -->

## Placeholders

- **[WORKSPACE_FOLDER]**: Absolute path of root folder where agent operates
- **[PROJECT_FOLDER]**: Absolute path of project folder (same as workspace if no monorepo)
- **[SRC_FOLDER]**: Absolute path of source folder
<!-- END: Skill: workspace-management -->

<!-- START: Skill: session-management, File: SKILL.md -->

- **[SESSIONS_FOLDER]**: Base folder for sessions (default: `[WORKSPACE_FOLDER]`, override in `!NOTES.md`)
- **[SESSION_ARCHIVE_FOLDER]**: Archive folder for closed sessions (default: `[WORKSPACE_FOLDER]/_archive_gitignore`)
- **[SESSION_FOLDER]**: Absolute path of currently active session folder
<!-- END: Skill: session-management -->

<!-- START: Skill: write-documents, File: STRUT_TEMPLATE.md -->

## STRUT Execution

STRUT plans use structured notation for progress tracking: steps `[ ] Px-Sy`, deliverables `[ ] Px-Dy`, checkbox `[x]` done or `[N]` done N times, transitions to `[PHASE-NAME]`, `[CONSULT]` (escalate to [ACTOR]), or `[END]`. Create them with `/write-strut`.

- **Execute**: perform the first unchecked step, update its checkbox, check deliverables, follow the transition at the phase boundary
- **Verification gates**: run `/verify` after creating a STRUT plan and before every phase transition. Only `/verify` has authority to approve autonomous phase transitions
- **Resume**: continue at the first unchecked step that feeds the first unchecked deliverable
<!-- END: Skill: write-documents -->

