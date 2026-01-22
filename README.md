# IPPS - Insanely Productive Programming System

A development system for AI-assisted coding workflows, optimized for a single programmer working with AI agents.

**Philosophy:** One programmer, structured workflows, AI handling the cognitive overhead. Inspired by Douglas Engelbart's intelligence augmentation and Frederick Brooks' "surgical team" concept - but replacing the support team entirely with AI. No sync meetings, no communication costs, minimum coordination necessary.

**Why all this structure?** AI agents are powerful but inconsistent. Without constraints, they:
- Interpret instructions differently each time
- Skip important steps or over-engineer simple tasks
- Lose context across sessions
- Make the same mistakes repeatedly

IPPS solves this through **deterministic agent behavior**:
- **AGEN** (AGENtic English) eliminates ambiguity - same verb always means same action (users can extend)
- **EDIRD** (Explore, Design, Implement, Refine, Deliver) prevents skipped steps - gates enforce quality before progress
- **STRUT** (STRUctured Thinking) tracks state - agent always knows where it is in the plan
- **TRACTFUL** (Traceable Requirements Artifacts and Coded Templates For Unified Lifecycle) preserves knowledge - every detail is covered by documents that survive session boundaries

The goal: Run [`/go`](.windsurf/workflows/go.md) and watch the agent execute a multi-session project autonomously, picking up exactly where it left off, never repeating past failures.

## Core Concepts

IPPS is built on four integrated specifications that enable autonomous agent operation:

- **[AGEN - Agentic English](SPEC_AGEN_AGENTIC_ENGLISH.md)** - Controlled vocabulary with verbs `[VERB]`, placeholders `[PLACEHOLDER]`, and states `STATE`. Eliminates ambiguity in agent instructions.

- **[EDIRD - Phase Model](SPEC_EDIRD_PHASE_MODEL.md)** - Five-phase workflow (Explore, Design, Implement, Refine, Deliver) with gates and deterministic next-action logic. Supports BUILD (code) and SOLVE (knowledge) workflows.

- **[STRUT - Structured Thinking](SPEC_STRUT_STRUCTURED_THINKING.md)** - Tree notation for planning and tracking agent work. Uses unique IDs (`P1`, `P1-S1`, `P1-D1`), checkbox states (`[ ]`, `[x]`, `[N]`), and transitions for flow control.

- **[TRACTFUL - Document Framework](SPEC_TRACTFUL_DOCUMENT_FRAMEWORK.md)** - Document types (INFO, SPEC, IMPL, TEST, TASKS) with unique IDs and traceability. Defines how documents reference each other and track progress.

**How they work together:**
```
AGEN provides the language    → Verbs, placeholders, outcomes (-OK, -FAIL, -SKIP)
EDIRD provides the phases     → EXPLORE → DESIGN → IMPLEMENT → REFINE → DELIVER
STRUT provides the notation   → Tree structure for plans with progress tracking
TRACTFUL provides the docs    → INFO, SPEC, IMPL, TEST, TASKS with unique IDs
```

**Design principle:** Each spec has a single responsibility. AGEN defines vocabulary. EDIRD defines phases and gates. STRUT defines notation. TRACTFUL defines documents. Workflows orchestrate them without hardcoding phase knowledge.

**Mini-example** - A hotfix plan in STRUT notation:
```
[ ] P1 [IMPLEMENT]: Fix null pointer bug
├─ Objectives:
│   └─ [ ] Bug no longer reproduces
├─ Strategy: Locate root cause, apply minimal fix, test
├─ [ ] P1-S1 [ANALYZE](stack trace)
├─ [ ] P1-S2 [IMPLEMENT](null check)
├─ [ ] P1-S3 [TEST]
├─ [ ] P1-S4 [COMMIT]("fix: null check in getUserById")
├─ Deliverables:
│   ├─ [ ] P1-D1: Root cause identified
│   ├─ [ ] P1-D2: Fix implemented
│   └─ [ ] P1-D3: Tests pass
└─> Transitions:
    - P1-D1 - P1-D3 checked → [END]
    - Tests fail after 3 attempts → [CONSULT]
```

## Table of Contents

- [Core Concepts](#core-concepts)
- [Overview](#overview)
- [How to Add to Your Project](#how-to-add-to-your-project)
- [DevSystem Versions](#devsystem-versions)
- [Agentic English](#agentic-english)
- [EDIRD Phase Model](#edird-phase-model---explore-design-implement-refine-deliver)
- [STRUT - Structured Thinking](#strut---structured-thinking)
- [TRACTFUL - Document Framework](#tractful---document-framework)
- [Agentic Concepts and Strategies](#agentic-concepts-and-strategies)
- [Key Conventions](#key-conventions)
- [Agent Tools](#agent-tools-installed-automatically-by-skill)
- [Project Structure](#project-structure)
- [Skills](#skills)
- [File Naming Conventions](#file-naming-conventions)
- [Workspaces and Sessions](#workspaces-and-sessions)
- [Usage Examples](#usage-examples)
- [Agent Compatibility](#agent-compatibility)

## Overview

IPPS provides structured rules, workflows, and skills for AI agents to follow consistent conventions during pair programming sessions. The current version (V3.2) introduces the EDIRD phase model, Agentic English vocabulary, and STRUT notation for deterministic agent behavior.

## How to Add to Your Project

Copy the `.windsurf/` folder to your VS Code or Windsurf workspace root:
```
your-project/
└── .windsurf/
    ├── rules/
    ├── workflows/
    └── skills/
```

## DevSystem Versions

- **[DevSystemV1](DevSystemV1/)** - Legacy system using rules and workflows
- **[DevSystemV2](DevSystemV2/)** - Previous version with modular skills and workflows
- **[DevSystemV2.1](DevSystemV2.1/)** - Previous version with refined workflows
- **[DevSystemV3](DevSystemV3/)** - Previous version with EDIRD phase model and Agentic English
- **[DevSystemV3.1](DevSystemV3.1/)** - Previous version with STRUT notation
- **[DevSystemV3.2](DevSystemV3.2/)** - Current system with Concurrent blocks, effort allocation, planning guidance

## Agentic English

A controlled vocabulary for agent-human communication. Provides consistent terminology across all workflows.

**Full specification**: [SPEC_AGEN_AGENTIC_ENGLISH.md](SPEC_AGEN_AGENTIC_ENGLISH.md)

**Goal**: Eliminate ambiguity in agent instructions by using bracketed verbs, placeholders, and labels.

**Rationale**: Agents interpret natural language inconsistently. Agentic English provides deterministic instructions that agents can reliably parse and execute.

**Syntax**:
- `[VERB]` - Action to execute (e.g., `[RESEARCH]`, `[VERIFY]`, `[IMPLEMENT]`)
- `[PLACEHOLDER]` - Value to substitute (e.g., `[ACTOR]`, `[WORKSPACE_FOLDER]`)
- `[LABEL]` - Classification to apply (e.g., `[UNVERIFIED]`, `[CRITICAL]`)
- `STATE` - Condition with NO brackets (e.g., `COMPLEXITY-HIGH`, `HOTFIX`, `SINGLE-PROJECT`)

**Extensibility**: Verbs are abstract concepts. Complex verbs CAN be concretized as dedicated workflows (e.g., `[COMMIT]` → [`/commit`](.windsurf/workflows/commit.md)), but this is optional. Simple verbs work inline within phase workflows.

**Example workflow instruction**:
```
1. [RESEARCH] affected code in [SRC_FOLDER]
2. [CONSULT] with [ACTOR] if unclear
3. [IMPLEMENT] changes
4. [VERIFY] against spec
5. [COMMIT] with conventional message
```

## EDIRD Phase Model - Explore, Design, Implement, Refine, Deliver

A 5-phase workflow model for both BUILD (code) and SOLVE (knowledge/decisions) work.

**Full specification**: [SPEC_EDIRD_PHASE_MODEL.md](SPEC_EDIRD_PHASE_MODEL.md)

**Goal**: Consistent phase structure for all development work with deterministic next-action logic. We want the agent to always do the right thing when the [`/go`](.windsurf/workflows/go.md) workflow is executed until the initial goal is reached.

**Rationale**: Without phases, agents skip important steps or apply heavyweight processes to simple tasks. EDIRD provides the right amount of process for each complexity level.

**Phases**:
- **EXPLORE** - Understand before acting: `[RESEARCH]`, `[ANALYZE]`, `[ASSESS]`, `[SCOPE]`
- **DESIGN** - Plan before executing: `[PLAN]`, `[WRITE-SPEC]`, `[PROVE]`, `[PARTITION]`
- **IMPLEMENT** - Execute the plan: `[IMPLEMENT]`, `[TEST]`, `[FIX]`, `[COMMIT]`
- **REFINE** - Improve quality: `[REVIEW]`, `[VERIFY]`, `[CRITIQUE]`, `[RECONCILE]`
- **DELIVER** - Complete and hand off: `[VALIDATE]`, `[MERGE]`, `[DEPLOY]`, `[CLOSE]`

**Complexity mapping**:
- `COMPLEXITY-LOW` → patch version (single file, clear scope)
- `COMPLEXITY-MEDIUM` → minor version (multiple files, backward compatible)
- `COMPLEXITY-HIGH` → major version (breaking changes, architecture)

**Operation Modes**:
- `IMPL-CODEBASE` (default) → Output to project source folders
- `IMPL-ISOLATED` → Output to `[SESSION_FOLDER]/` only (for POCs, prototypes)

**Example BUILD flow**:
```
[EXPLORE] → [ASSESS] complexity → Gate check
[DESIGN] → [WRITE-SPEC] → [PROVE] risky parts → Gate check
[IMPLEMENT] → [IMPLEMENT]→[TEST]→[FIX]→green→next → Gate check
[REFINE] → [VERIFY] against spec → [CRITIQUE] if HIGH → Gate check
[DELIVER] → [COMMIT] → [MERGE]
```

## STRUT - Structured Thinking

Tree notation for planning and tracking complex autonomous work.

**Full specification**: [SPEC_STRUT_STRUCTURED_THINKING.md](SPEC_STRUT_STRUCTURED_THINKING.md)

**Goal**: Provide a notation for agent plans that supports progress tracking, hierarchical decomposition, and flow control.

**Rationale**: Agents need structured plans they can parse, update, and resume across sessions. STRUT provides unique IDs for every item, checkbox states for progress, and transitions for conditional flow.

**Core elements**:
- **Plan ID** - Unique identifier (e.g., `P1`, `P2`)
- **Step ID** - Plan + sequence (e.g., `P1-S1`, `P1-S2`)
- **Deliverable ID** - Plan + deliverable (e.g., `P1-D1`, `P1-D2`)
- **Checkbox states** - `[ ]` pending, `[x]` done, `[N]` done N times (retry count)
- **Concurrent blocks** - Group parallel steps under `Concurrent: <strategy>`
- **Dependencies** - `← Px-Sy` suffix for explicit wait conditions

**Structure**:
```
[ ] P1 [EXPLORE]: Evaluate database options
├─ Objectives:
│   └─ [ ] Recommendation ready ← P1-D1, P1-D2
├─ Strategy: Research 3 options in parallel, then compare (10min AWT)
├─ [ ] P1-S1 [DEFINE](evaluation criteria)
├─ Concurrent: Independent research, no shared state
│   ├─ [ ] P1-S2 [RESEARCH](PostgreSQL)
│   ├─ [ ] P1-S3 [RESEARCH](MongoDB)
│   └─ [ ] P1-S4 [RESEARCH](DynamoDB)
├─ [ ] P1-S5 [EVALUATE](compare against criteria)
├─ [ ] P1-S6 [RECOMMEND](winner with rationale)
├─ Deliverables:
│   ├─ [ ] P1-D1: Comparison matrix complete
│   └─ [ ] P1-D2: Recommendation documented
└─> Transitions:
    - P1-D1, P1-D2 checked → [END]
    - No clear winner → [CONSULT]
```

## TRACTFUL - Document Framework

Document types and templates that cover the entire development cycle from exploration of ideas to fixing issues.

**Full specification**: [SPEC_TRACTFUL_DOCUMENT_FRAMEWORK.md](SPEC_TRACTFUL_DOCUMENT_FRAMEWORK.md)

**Goal**: Ensure all development artifacts are uniquely identified, properly structured, and traceable from ideation to maintenance.

**Rationale**: Agents need consistent document templates to create, reference, and update. TRACTFUL provides document types for each stage and a unified ID system (TDID) for cross-referencing.

**Document types**:
- **INFO** (IN) - Research findings, analysis results
- **SPEC** (SP) - Specifications with requirements and design decisions
- **IMPL** (IP) - Implementation plans with steps and edge cases
- **TEST** (TP) - Test plans with test cases and verification
- **TASKS** (TK) - Partitioned work items for execution

**ID system (TDID)**:
- **Document ID** - `[TOPIC]-[TYPE][NN]` (e.g., `AUTH-SP01`, `CRWL-IP02`)
- **Item ID** - `[TOPIC]-[ITEM]-[NN]` (e.g., `AUTH-FR-01`, `CRWL-DD-03`)
- **Cross-reference** - `filename.md [DOC-ID]`

## Agentic Concepts and Strategies

Acronyms and techniques used throughout IPPS for consistent agent behavior:

- **PREN** - Proper English. Precise natural language avoiding confusion, ambiguities, and term conflicts
- **AGEN** - Agentic English. PREN enriched with semantics: `@mentions`, `/workflow`, `[VERB]`, `[PLACEHOLDER]`
- **HWT** - Human Work Time. Partition target: max 0.5h per task for predictable progress
- **AWT** - Agentic Work Time. Agent time estimate for planning and capacity
- **MEPI** - Most Executable Point of Information. Used for research when action is needed
- **MCPI** - Most Complete Point of Information. Used for research when thoroughness is needed
- **SOCAS** - Signs Of Confusion And Sloppiness. 10 criteria for detecting agent degradation
- **MNF** - Must Not Forget. Technique for critical item tracking during task execution
- **ASANAPAP** - As Short As Necessary, As Precise As Possible. Conciseness principle for workflows and documents

**Full registry**: [ID-REGISTRY.md](ID-REGISTRY.md) - All acronyms, TOPICs, states, and named concepts

## Key Conventions

- [Core Conventions](DevSystemV3.2/rules/core-conventions.md) - Text formatting, document structure, header blocks
- [DevSystem Core](DevSystemV3.2/rules/devsystem-core.md) - Workspace scenarios, folder structure, workflow reference
- [DevSystem IDs](DevSystemV3.2/rules/devsystem-ids.md) - Document IDs, topic registry, tracking IDs
- [Agentic English](DevSystemV3.2/rules/agentic-english.md) - Controlled vocabulary for agent instructions
- [EDIRD Phase Planning](DevSystemV3.2/rules/edird-phase-planning.md) - Phase model core rules
- [Git Conventions](DevSystemV3.2/skills/git-conventions/SKILL.md) - Commit message format, .gitignore rules
- [Coding Conventions](DevSystemV3.2/skills/coding-conventions/SKILL.md) - Python, PowerShell, workflow style rules
- [Workflow Rules](DevSystemV3.2/skills/coding-conventions/WORKFLOW-RULES.md) - ASANAPAP principle, workflow formatting

## Agent Tools (installed automatically by skill)

Local tool installations in `.tools/` (gitignored). Run `SETUP.md` in each skill folder to install.

**pdf-tools** ([SETUP](DevSystemV2.1/skills/pdf-tools/SETUP.md)) - Enables agent to read entire PDFs by converting pages to JPG images for vision analysis:
- **7-Zip** (`.tools/7z/`) - Archive extraction, NSIS installer unpacking
- **Poppler** (`.tools/poppler/`) - PDF to image, text extraction, split/merge
- **QPDF** (`.tools/qpdf/`) - PDF manipulation, optimization, repair
- **Ghostscript** (`.tools/gs/`) - PDF compression, image downsampling

**github** ([SETUP](DevSystemV2.1/skills/github/SETUP.md)):
- **GitHub CLI** (`.tools/gh/`) - Repos, issues, PRs, releases

**llm-evaluation** ([SKILL](DevSystemV3.2/skills/llm-evaluation/SKILL.md)) - Evaluate LLM output quality by generating questions, collecting answers, and scoring with a judge model:
- **Python venv** (`.tools/llm-eval-venv/`) - OpenAI, Anthropic SDKs
- **API keys** (`.env` in current working directory, or use `--keys-file`) - OPENAI_API_KEY, ANTHROPIC_API_KEY

Run `SETUP.md` in each skill folder to install required tools locally to `.tools/`.

## Project Structure

```
IPPS/
├── .tools/                       # Local tool installations (gitignored)
├── .windsurf/                    # Active agent configuration (copied from DevSystemV3.2)
│   ├── rules/
│   ├── workflows/
│   └── skills/
├── DevSystemV1/                  # Legacy (deprecated)
├── DevSystemV2/                  # Legacy (deprecated)
├── DevSystemV2.1/                # Legacy (deprecated)
├── DevSystemV3/                  # Previous version
├── DevSystemV3.1/                # Previous version
├── DevSystemV3.2/                # Current system
│   ├── rules/
│   │   ├── core-conventions.md   # Text formatting, document structure
│   │   ├── devsystem-core.md     # Workspace scenarios, folder structure, operation modes
│   │   ├── devsystem-ids.md      # Document and item ID conventions
│   │   ├── agentic-english.md    # Controlled vocabulary for agent instructions
│   │   └── edird-phase-planning.md # EDIRD phase model core rules
│   ├── skills/
│   │   ├── coding-conventions/   # Python, PowerShell, workflow style rules
│   │   ├── edird-phase-planning/ # Phase gates, flows, planning
│   │   ├── git/                  # Commit history navigation, file recovery
│   │   ├── git-conventions/      # Commit message format
│   │   ├── github/               # GitHub CLI operations
│   │   ├── llm-evaluation/       # LLM evaluation pipeline scripts
│   │   ├── pdf-tools/            # PDF scripts and tools
│   │   ├── session-management/   # Session templates
│   │   └── write-documents/      # Spec, impl, test templates
│   └── workflows/
│       ├── build.md              # BUILD workflow entry point
│       ├── commit.md             # Git conventional commits
│       ├── continue.md           # Execute next items on plan
│       ├── critique.md           # Devil's Advocate review
│       ├── fail.md               # Record failures
│       ├── go.md                 # Autonomous loop (recap + continue)
│       ├── implement.md          # IMPLEMENT phase
│       ├── learn.md              # Extract learnings from failures
│       ├── partition.md          # Split plans into testable chunks
│       ├── prime.md              # Load workspace context
│       ├── recap.md              # Analyze context, identify status
│       ├── reconcile.md          # Pragmatic reconciliation
│       ├── rename.md             # Global/local refactoring
│       ├── research.md           # Structured research
│       ├── session-archive.md    # Archive session folder
│       ├── session-close.md      # Close and sync session
│       ├── session-new.md        # Initialize session
│       ├── session-resume.md     # Resume session
│       ├── session-save.md       # Save session progress
│       ├── solve.md              # SOLVE workflow entry point
│       ├── sync.md               # Document synchronization
│       ├── test.md               # Run tests based on scope
│       ├── transcribe.md         # PDF/web transcription
│       ├── verify.md             # Verification against specs and rules
│       ├── write-impl-plan.md    # Create implementation plan
│       ├── write-spec.md         # Create specification
│       ├── write-strut.md        # Create STRUT plans
│       ├── write-tasks-plan.md   # Create tasks plan
│       └── write-test-plan.md    # Create test plan
├── ID-REGISTRY.md                # Prevents term/ID collisions (DevSystem constants + project topics)
└── README.md
```

## Skills

- **edird-phase-planning** - High-level phase planning with effort allocation, planning guidance, gates
- **git** - Commit history navigation, file recovery from previous commits
- **github** - GitHub CLI operations (repos, issues, PRs)
- **llm-evaluation** - Generic LLM evaluation pipeline (process, questions, answers, scoring)
- **pdf-tools** - PDF conversion, compression, analysis using Ghostscript, Poppler, QPDF
- **session-management** - Session init, save, resume, close workflows
- **write-documents** - Spec, impl, test, info, tasks document templates

## File Naming Conventions

IPPS uses special prefixes to control how files are processed:

- **`!` prefix** - Priority files (e.g., `!NOTES.md`). Read first during [`/prime`](.windsurf/workflows/prime.md). Contains critical project information.
- **`_` prefix** - Ignored by automatic workflows (e.g., `_SPEC_*.md`, `_PrivateSessions/`). Used for session-specific, WIP, or archived content.
- **`.` prefix** - Hidden files following Unix convention (e.g., `.windsurf/`, `.gitignore`).

## Workspaces and Sessions

IPPS uses a two-level tracking system: **workspace-level** files for project-wide information and **session-level** files for focused work periods. In MONOREPO workspaces, there's an additional **project-level** layer between workspace and sessions.

### Workspace Files

Located in workspace root (or project root in monorepos):

| File | Required | Purpose |
|------|----------|---------|
| `!NOTES.md` | ✅ Yes | Critical project info, agent instructions, key patterns |
| `!PROBLEMS.md` | Optional | Known issues across the project |
| `!PROGRESS.md` | Optional | Overall project progress |
| `FAILS.md` | Auto-created | Lessons learned from past mistakes (via [`/fail`](.windsurf/workflows/fail.md) workflow, synced from sessions) |
| `LEARNINGS.md` | Auto-created | Reusable patterns (via [`/learn`](.windsurf/workflows/learn.md) workflow analyzing fails) |
| `ID-REGISTRY.md` | ✅ Yes | Authoritative source for TOPICs, acronyms, and IDs |

### Session Files

Located in session folder (e.g., `_2026-01-15_FixAuthBug/`):

| File | Required | Purpose |
|------|----------|---------|
| `NOTES.md` | ✅ Yes | Session goal, key decisions, findings, resume instructions |
| `PROBLEMS.md` | ✅ Yes | Problems discovered during session (Open/Resolved/Deferred) |
| `PROGRESS.md` | ✅ Yes | To-do list, in-progress, done, tried-but-not-used |
| `FAILS.md` | Auto-created | Session-specific failures (run [`/fail`](.windsurf/workflows/fail.md) to record) |
| `LEARNINGS.md` | Auto-created | Lessons from failures (run [`/learn`](.windsurf/workflows/learn.md) to analyze fails) |

### Session Lifecycle

```
/prime           → Load constants and documents from workspace and devsystem
                   (README, NOTES, PROBLEMS, FAILS, LEARNINGS, ID-REGISTRY, ...)
/session-new     → Create session folder with NOTES, PROBLEMS, PROGRESS
    ↓
  [work]         → Create specs, implement, track progress
    ↓              (/fail to record failures, /learn to extract lessons)
    ↓
/session-save    → Document findings, commit changes
    ↓
/session-resume  → Re-read session docs, continue work
    ↓
/session-close   → Sync FAILS and LEARNINGS to workspace, prepare for archive
    ↓
/session-archive → Move session folder to _Archive/
```

### Sync on Session Close

When [`/session-close`](.windsurf/workflows/session-close.md) runs:
- **FAILS.md** - [MEDIUM] and [HIGH] severity entries sync to workspace `FAILS.md`
- **LEARNINGS.md** - Patterns from [MEDIUM]/[HIGH] fails sync to workspace `LEARNINGS.md` or `!NOTES.md`
- **PROBLEMS.md** - Open/deferred problems sync to workspace `!PROBLEMS.md`

This ensures lessons learned survive session boundaries and prevent repeated mistakes.

## Usage Examples

### Prime Context

**Workflows:** [`/prime`](.windsurf/workflows/prime.md)

Load workspace context before starting work:
```
/prime
```

The prime workflow:
1. Reads all `.md` files in `[AGENT_FOLDER]/rules/` (core conventions, system behavior)
2. Reads all `!*.md` files (priority documentation with critical project info)
3. Reads standard `.md` files in workspace root (excluding `_` and `!` prefixed)
4. Detects workspace scenario (project structure, version strategy, work mode)
5. Reports summary: files read, scenario detected

Typically loads: `README.md`, `!NOTES.md`, `!PROBLEMS.md`, `FAILS.md`, `LEARNINGS.md`, `ID-REGISTRY.md`, agent rules

### Workflow Entry Points

Both workflows **automatically create a session**, follow EDIRD phases, and close when done.

**Workflows:** [`/build`](.windsurf/workflows/build.md), [`/solve`](.windsurf/workflows/solve.md)

Start a BUILD workflow (create software, new features):
```
/build "Add user authentication API"
```

Start a SOLVE workflow (research, analysis, decisions):
```
/solve "Evaluate database migration options"
```

### Session Workflows

**Workflows:** [`/session-new`](.windsurf/workflows/session-new.md), [`/session-save`](.windsurf/workflows/session-save.md), [`/session-resume`](.windsurf/workflows/session-resume.md), [`/session-close`](.windsurf/workflows/session-close.md)

Start a new work session:
```
/session-new
```
Creates a session folder with NOTES.md, PROBLEMS.md, PROGRESS.md.

Save progress during work:
```
/session-save
```

Resume an existing session:
```
/session-resume
```

Close session and sync findings:
```
/session-close
```

### Autonomous Execution

**Workflows:** [`/go`](.windsurf/workflows/go.md), [`/recap`](.windsurf/workflows/recap.md), [`/continue`](.windsurf/workflows/continue.md)

Run autonomous loop until goal reached:
```
/go
```

The [`/go`](.windsurf/workflows/go.md) workflow cycles through:
1. [`/recap`](.windsurf/workflows/recap.md) - Analyze context, identify current status
2. [`/continue`](.windsurf/workflows/continue.md) - Execute next items on plan
3. Repeat until goal reached or blocker hit

### Document Cycle (INFO -> SPEC -> IMPL -> TEST -> TASKS)

**Workflows:** [`/research`](.windsurf/workflows/research.md), [`/write-spec`](.windsurf/workflows/write-spec.md), [`/write-impl-plan`](.windsurf/workflows/write-impl-plan.md), [`/write-test-plan`](.windsurf/workflows/write-test-plan.md), [`/write-tasks-plan`](.windsurf/workflows/write-tasks-plan.md), [`/implement`](.windsurf/workflows/implement.md), [`/verify`](.windsurf/workflows/verify.md), [`/sync`](.windsurf/workflows/sync.md), [`/rename`](.windsurf/workflows/rename.md), [`/commit`](.windsurf/workflows/commit.md)

This follows the Specification-Driven Development (SDD) methodology used by [GitHub spec-kit](https://github.com/github/spec-kit) and [Zencoder](https://docs.zencoder.ai/user-guides/tutorials/spec-driven-development-guide).

1. **Research** - Gather information:
```
/research
```
Creates `_INFO_*.md` with findings.

2. **Specify** - Create specification:
```
/write-spec
```
Creates `_SPEC_*.md` from requirements.

3. **Plan** - Create implementation plan:
```
/write-impl-plan
```
Creates `_IMPL_*.md` from spec.

4. **Test Plan** - Create test plan:
```
/write-test-plan
```
Creates `_TEST_*.md` from spec.

5. **Tasks** - Partition into discrete work items:
```
/write-tasks-plan
```
Creates `_TASKS_*.md` from IMPL/TEST. **Mandatory before implementation.**

6. **Implement** - Execute the tasks:
```
/implement
```

7. **Verify** - Check work against specs:
```
/verify
```

8. **Sync** - Update dependent documents:
```
/sync
```

9. **Rename** - Global/local pattern replacement:
```
/rename
```

10. **Commit** - Create conventional commits:
```
/commit
```

## Agent Compatibility

| Feature | Windsurf | Claude Code | Codex CLI | GitHub Copilot |
|---------|----------|-------------|-----------|----------------|
| **Type** | IDE | Terminal | Terminal | IDE Extension |
| **Platform** | Windows, macOS, Linux | Windows, macOS, Linux | macOS, Linux, Windows (WSL) | VS Code, Visual Studio, JetBrains |
| **Instructions** | `.windsurf/rules/*.md` | `CLAUDE.md` | `AGENTS.md` | `.github/copilot-instructions.md` |
| **Commands/Workflows** | `.windsurf/workflows/*.md` | `.claude/commands/*.md` | Custom prompts only | Prompt files only |
| **Skills** | ✅ Yes | ✅ Yes | ❌ No | ❌ No |
| **Subagents** | ❌ No | ✅ Yes | ❌ No | ✅ Yes (custom agents) |
| **Hooks** | ✅ Yes | ✅ Yes | ❌ No | ❌ No |
| **MCP Support** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Sandbox** | ❌ No | ❌ No | ✅ Yes (OS-level) | ❌ No |
| **Config Format** | JSON + Protobuf | JSON | TOML | JSON |

### Deploying to Other Agents

**Claude Code:**
- `.windsurf/rules/*.md` → `CLAUDE.md` (merge into single file)
- `.windsurf/workflows/*.md` → `.claude/commands/*.md`
- `.windsurf/skills/*/SKILL.md` → `.claude/skills/*/SKILL.md`

**Codex CLI:**
- `.windsurf/rules/*.md` → `AGENTS.md` (merge into single file)

**GitHub Copilot:**
- `.windsurf/rules/*.md` → `.github/copilot-instructions.md` (merge into single file)

### Detailed Documentation

- [Agent Comparison](_INFO_AGENT_COMPARISON.md) - Full feature comparison with detailed tables
- [How Windsurf Works](INFO_HOW_WINDSURF_WORKS.md) - Windsurf IDE and Cascade assistant
- [How Claude Code Works](_INFO_HOW_CLAUDE_CODE_WORKS.md) - Anthropic's terminal agent
- [How Codex CLI Works](_INFO_HOW_CODEX_WORKS.md) - OpenAI's terminal agent
- [How GitHub Copilot Works](_INFO_HOW_COPILOT_WORKS.md) - GitHub's IDE extension

### Technical Reference

- [ASCII Art Width Test](_INFO_ASCII_ART_WIDTH_TEST.md) - Unicode character width testing for monospace fonts
- [ASCII Art Transcription Cost/Quality Eval](_Sessions/_Archive/_2026-01-23_JpgToAsciiArtTranscriptionCostQualityEval/INFO_ASCII_ART_TRANSCRIPTION_COST_QUALITY_EVAL.md) - LLM model comparison for image-to-ASCII transcription
