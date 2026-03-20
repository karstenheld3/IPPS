---
trigger: always_on
---

# DevSystem Core

## Definitions

### Core Concepts

- **[WORKSPACE]**: Windsurf/VSCode workspace root folder
- **[PROJECT]**: Monorepo: project subfolder. No Monorepo: Workspace = Project
- **[SESSION]**: All context for a work session - folder, files, conversations, commits, tracking files

### Agent Folder

**[AGENT_FOLDER]**: Windsurf: `.windsurf/` | Claude Code: `.claude/`

### Configuration

- **[RULES]**: `[AGENT_FOLDER]/rules/`
- **[WORKFLOWS]**: `[AGENT_FOLDER]/workflows/`
- **[SKILLS]**: `[AGENT_FOLDER]/skills/`

### Document Types

- **[INFO]** (IN): Research, analysis. Example: `AUTH-IN01`
- **[SPEC]** (SP): Specification, reverse-updated from verified code. Example: `CRWL-SP01`
- **[IMPL]** (IP): Implementation plan, reverse-updated from verified code. Example: `CRWL-IP01`
- **[TEST]** (TP): Test plans for SPEC/IMPL. Example: `CRWL-TP01`
- **[TASKS]** (TK): Partitioned task lists from IMPL/TEST. Example: `CRWL-TK01`. Created via `/write-tasks-plan` or `/partition`

### Tracking Documents

One of each type per scope (workspace, project, or session).

- **[NOTES]**: Agent MUST read to avoid unintentional behavior
- **[PROGRESS]**: Agent MUST read to avoid unintentional behavior
- **[PROBLEMS]**: Per-session tracking. On `/session-finalize`, sync to project
- **[FAILS]**: Lessons learned. Agent MUST read during `/prime` (except `_` prefix files). Never delete entries unconfirmed, only append or mark resolved.

### Placeholders

- **[ACTOR]**: Decision-making entity (default: user, in /go-autonomous: agent)

### MNF (MUST-NOT-FORGET) Technique

**Planning**: Create `MUST-NOT-FORGET` list (5-15 items, name unchanged for grep). Collect from FAILS.md, learnings, rules, specs, user instructions. Include in plan or document top.

**Completion**: Review each MNF item before marking done. Verify compliance or document why N/A. Update FAILS.md if violated.

### Complexity Levels

- **COMPLEXITY-LOW**: Single file, clear scope, no dependencies → patch
- **COMPLEXITY-MEDIUM**: Multiple files, some dependencies, backward compatible → minor
- **COMPLEXITY-HIGH**: Breaking changes, new patterns, external APIs, architecture → major

### Operation Modes

- **IMPL-CODEBASE** (default): Output to project source folders. For SPEC, IMPL, TEST, [IMPLEMENT], HOTFIX, BUGFIX.
- **IMPL-ISOLATED**: Output to `[SESSION_FOLDER]/` or `[SESSION_FOLDER]/poc/`. For [PROVE], POCs, prototypes. Existing code/config/runtime MUST NOT be affected. NEVER create folders in workspace root. **REQUIRES SESSION**: run `/session-new` first if none exists.

## Workspace Scenarios

- **Project Structure**: SINGLE-PROJECT | MONOREPO
- **Version Strategy**: SINGLE-VERSION | MULTI-VERSION
- **Work Mode**: SESSION-MODE | PROJECT-MODE

## Folder Structure

### Single Project

```
[WORKSPACE_FOLDER]/
├── [AGENT_FOLDER]/
│   ├── rules/
│   ├── workflows/
│   └── skills/
├── _Archive/
├── _[SESSION_FOLDER]/
│   ├── _IMPL_*.md, _INFO_*.md, _SPEC_*.md, _TEST_*.md
│   ├── NOTES.md, PROBLEMS.md, PROGRESS.md, FAILS.md
├── src/
├── !NOTES.md
├── !PROBLEMS.md
├── !PROGRESS.md
└── FAILS.md
```

### Monorepo

```
[WORKSPACE_FOLDER]/
├── [AGENT_FOLDER]/
├── _Archive/
├── [PROJECT_A]/
│   ├── _Archive/
│   ├── _[SESSION_FOLDER]/
│   ├── src/
│   ├── NOTES.md, PROBLEMS.md, PROGRESS.md, FAILS.md
├── [PROJECT_B]/
│   └── ...
├── !NOTES.md, !PROBLEMS.md, !PROGRESS.md, FAILS.md
```

## File Naming Conventions

- **! prefix**: High relevance, extra attention during `/prime`
- **_ prefix**: Skipped by auto-priming. Session-specific, WIP, archived content.
- **. prefix**: Hidden (Unix convention)
- **.tmp prefix**: Temporary scripts, delete after use

## Placeholders

- **[WORKSPACE_FOLDER]**: Absolute path of workspace root
- **[PROJECT_FOLDER]**: Project root (same as workspace if no monorepo)
- **[SRC_FOLDER]**: Source folder absolute path
- **[DEFAULT_SESSIONS_FOLDER]**: Session base folder (default: `[WORKSPACE_FOLDER]`, override in `!NOTES.md`)
- **[SESSION_ARCHIVE_FOLDER]**: Default: `[SESSION_FOLDER]/../_Archive`
- **[SESSION_FOLDER]**: Active session folder absolute path

## Workflow Reference

`/build` BUILD entry (code) | `/bugfix` Record/fix bugs | `/commit` Conventional commits | `/continue` Execute next plan items | `/critique` Devil's Advocate | `/fail` Record failures | `/go` Autonomous loop | `/implement` Execute from plan | `/learn` Extract learnings | `/partition` Split into tasks | `/prime` Load context | `/recap` Identify status | `/reconcile` Pragmatic review | `/rename` Refactoring with verification | `/research` Structured research | `/session-archive` Archive session | `/session-finalize` Finalize, sync, prepare archive | `/session-new` Init session | `/session-load` Resume session | `/session-save` Save progress | `/solve` SOLVE entry (knowledge) | `/sync` Doc synchronization | `/test` Run tests | `/transcribe` PDF/web to markdown | `/verify` Verify against specs/rules | `/write-impl-plan` IMPL from spec | `/write-spec` SPEC from requirements | `/write-strut` Create STRUT plans | `/write-tasks-plan` TASKS from IMPL/TEST | `/write-test-plan` TEST from spec

## STRUT Execution

Create via `/write-strut` or `@skills:write-documents` with `STRUT_TEMPLATE.md`.

### Execution Algorithm

1. Find first unchecked step `[ ] Px-Sy`
2. Execute verb action with parameters
3. Mark `[x]` on success, increment `[N]` on retry
4. Check if any `Px-Dy` deliverables can be checked
5. At phase boundary: run `/verify` for transition conditions
6. Follow transition to next phase, `[CONSULT]`, or `[END]`

### Verification Gates

- Run `/verify` after creating STRUT plans (structure validation)
- Run `/verify` before phase transitions
- Only `/verify` has authority to approve autonomous phase transitions

### Resuming Interrupted Plans

1. Read PROGRESS.md or document with STRUT plan
2. Find first unchecked deliverable `[ ] Px-Dy`
3. Identify feeding steps, continue from first unchecked

### Checkbox States

`[ ]` Pending | `[x]` Done | `[N]` Done N times (retried)

### Transition Targets

`[PHASE-NAME]` Next phase | `[CONSULT]` Escalate to [ACTOR] | `[END]` Plan complete