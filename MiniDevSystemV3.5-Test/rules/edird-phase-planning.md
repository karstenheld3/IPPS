# EDIRD Phase Model (Core)

Full model with gates, flows, planning: invoke @edird-phase-planning skill. Execution rules in `devsystem-core.md`.

## Phases

- **EXPLORE** - Understand before acting. [RESEARCH], [ANALYZE], [ASSESS], [SCOPE]
- **DESIGN** - Plan before executing. [PLAN], [DECOMPOSE], [WRITE-SPEC], [PROVE]
- **IMPLEMENT** - Execute the plan. [IMPLEMENT], [TEST], [FIX], [COMMIT]
- **REFINE** - Improve quality. [REVIEW], [VERIFY], [CRITIQUE], [RECONCILE]
- **DELIVER** - Complete and hand off. [VALIDATE], [MERGE], [DEPLOY], [CLOSE]

## Core Principles

- **Gates**: Checklist must pass before phase transition. Failures loop within phase.
- **Small cycles**: [IMPLEMENT]→[TEST]→[FIX]→green→next. Never large untestable steps.
- **Retry limits**: LOW: infinite. MEDIUM/HIGH: max 5 per phase, then [CONSULT].
- **Verb outcomes**: -OK (proceed), -FAIL (handle per verb), -SKIP (intentional).
- **Workflow type**: BUILD (code) or SOLVE (knowledge). Set in EXPLORE, persists unless [ACTOR] confirms switch.
- **Complexity**: LOW=patch, MEDIUM=minor, HIGH=major (semantic versioning).
- **Visual verification**: UI/game/graphics MUST include visual [PROVE] before full implementation.

## Entry Rule

All workflows start in EXPLORE with [ASSESS] for workflow type and complexity.

- **Gate output mandatory.** Agent MUST output explicit gate evaluation before each transition. No self-approval without evidence.
- **Artifact verification.** Agent MUST list created artifact file paths as gate evidence.
- **Research before implementation.** External system accuracy requires [RESEARCH] with cited sources. Training data assumptions are not research.
- **Visual reference for replicas.** Replica/clone work MUST include screenshot/video during EXPLORE.

## Gate Summaries

- **EXPLORE→DESIGN**: Problem understood, scope defined, workflow type determined
- **DESIGN→IMPLEMENT**: SPEC, IMPL, TEST docs exist, plan decomposed, risks proven
- **IMPLEMENT→REFINE**: All steps implemented, tests pass, no TODO/FIXME
- **REFINE→DELIVER**: Reviews complete, issues reconciled, ready to merge
- **DELIVER→DONE**: Validated, merged, deployed (if applicable), session closed

## Phase Tracking

- Agent updates NOTES.md with current phase on transition.
- Agent maintains phase plan in PROGRESS.md (status: pending/in_progress/done).

## Planning Notation

- **STRUT** - High-level orchestration for complex multi-phase processes
  - When: Multi-phase work, `/go` runs, session-spanning tasks, deep research
  - Contains: Phases, Objectives, Strategy, Steps, Deliverables, Transitions, Time Log
  - Invoke: @write-documents `STRUT_TEMPLATE.md` or `/write-strut`
  - Verify: `/verify` (STRUT Planning + STRUT Transition contexts)
- **TASKS** - Low-level execution for granular task coordination
  - When: Single-phase execution, partitioned IMPL steps, file-by-file research
  - Contains: Task items with files, done-when criteria, verification commands, task durations
  - Created via: [PARTITION] from IMPL plan or Phase 4 of research strategies

## Workflow Types

### BUILD (`/build`)

Primary output: working code. Triggers: "Add a feature...", "Build...", "Implement..."

Required documents by complexity:
- **LOW**: Inline plan sufficient, documents optional
- **MEDIUM**: `_SPEC_*.md` + `_IMPL_*.md` required (NO EXCEPTIONS)
- **HIGH**: All documents required (`_INFO_*.md`, `_SPEC_*.md`, `_IMPL_*.md`, `_TEST_*.md`)

DESIGN→IMPLEMENT gate MUST list actual file paths. Missing files = gate fail.

### SOLVE (`/solve`)

Primary output: knowledge, decisions, documents. Triggers: "Research...", "Evaluate...", "Write...", "Decide..."

Assessment: RESEARCH / ANALYSIS / EVALUATION / WRITING / DECISION / HOTFIX / BUGFIX

HOTFIX/BUGFIX are SOLVE because primary focus is understanding the problem; code fix is secondary.

## Stuck Detection

If no progress after retry limit:
1. [CONSULT] with [ACTOR]
2. Document in PROBLEMS.md
3. Get guidance or [DEFER] and continue