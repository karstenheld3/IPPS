# EDIRD Phase Model (Core)

Full model (gate checklists, gate output format, workflow types, required documents, planning notation, phase plans, effort budgets, stuck detection): invoke @skills:promptsystem `PROMPTSYSTEM_EDIRD.md` for `/go` and for planning long-running work.

**Execution logic**: Execution rules are defined in `promptsystem-core.md`.

## Phases

- **EXPLORE** - Understand before acting. [RESEARCH], [ANALYZE], [ASSESS], [SCOPE]
- **DESIGN** - Plan before executing. [PLAN], [DECOMPOSE], [WRITE-SPEC], [PROVE]
- **IMPLEMENT** - Execute the plan. [IMPLEMENT], [TEST], [FIX], [COMMIT]
- **REFINE** - Improve quality. [REVIEW], [VERIFY], [CRITIQUE], [RECONCILE]
- **DELIVER** - Complete and hand off. [VALIDATE], [MERGE], [DEPLOY], [CLOSE]

## Core Principles

- **Entry**: All workflows start in EXPLORE with [ASSESS] to determine workflow type (BUILD = code, SOLVE = knowledge, decisions, documents) and complexity or problem type
- **Gates**: Checklist must pass before phase transition. Gate failures loop within phase. Before each transition output the explicit gate evaluation with the created artifact files as evidence. No self-approval without evidence
- **Required documents (BUILD)**: COMPLEXITY-LOW inline plan; MEDIUM `_SPEC_*.md` + `_IMPL_*.md`; HIGH also `_INFO_*.md` and `_TEST_*.md`. The DESIGN→IMPLEMENT gate lists the actual file paths; missing files fail the gate
- **Small cycles**: [IMPLEMENT]→[TEST]→[FIX]→green→next. Never large untestable steps
- **Research before implementation**: accuracy to an external system requires [RESEARCH] with cited sources; training data assumptions are not research. UI/game/graphics work includes a visual [PROVE]; replica work a visual reference during EXPLORE
- **Retry limits**: COMPLEXITY-LOW: infinite retries (until user stops). COMPLEXITY-MEDIUM/HIGH: max 5 attempts per phase, then document in PROBLEMS.md and [CONSULT] with [ACTOR] (`[ACTOR] = agent`: self-resolve, log decision, proceed or [DEFER])
- **Phase tracking**: current phase in NOTES.md on transition, full phase plan with status in PROGRESS.md
- **Planning notation**: STRUT for multi-phase orchestration, TASKS for granular single-phase execution

## Gate Summaries

- **EXPLORE→DESIGN**: Problem understood, scope defined, workflow type determined
- **DESIGN→IMPLEMENT**: SPEC, IMPL, TEST docs exist, plan decomposed, risks proven
- **IMPLEMENT→REFINE**: All steps implemented, tests pass, no TODO/FIXME
- **REFINE→DELIVER**: Reviews complete, issues reconciled, ready to merge
- **DELIVER→DONE**: Validated, merged, deployed (if applicable), session closed
