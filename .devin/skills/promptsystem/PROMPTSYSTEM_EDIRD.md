# EDIRD Phase Planning

Full EDIRD phase model. Short form (rule): `edird-phase-planning.md`.

## When to Invoke

- `/go` workflow (BUILD or SOLVE mode)
- [PLAN] - creating high-level plans to achieve goals
- Planning for long agentic runs for features, fixes, or research
- Looking up an AGEN verb, label, or state for a STRUT plan or phase plan: `PROMPTSYSTEM_AGENTIC_ENGLISH.md`

**NOT for document writing** - Use dedicated workflows instead:
- `/write-spec` for SPEC documents
- `/write-impl-plan` for IMPL documents
- `/write-test-plan` for TEST documents
- `/write-tasks-plan` for TASKS documents

## MUST-NOT-FORGET

- `/go` is the entry workflow (BUILD or SOLVE mode)
- Use `/write-spec`, `/write-impl-plan`, `/write-test-plan`, `/write-tasks-plan` for documents
- Check gates before phase transitions

## Quick Reference

**Phases:** EXPLORE → DESIGN → IMPLEMENT → REFINE → DELIVER

**Workflow types:** BUILD (code output) | SOLVE (knowledge/decision output)

**Assessment:** COMPLEXITY-LOW/MEDIUM/HIGH | PROBLEM-TYPE (RESEARCH/ANALYSIS/EVALUATION/WRITING/DECISION)

## Phases

- **EXPLORE** - Understand before acting. [RESEARCH], [ANALYZE], [ASSESS], [SCOPE]
- **DESIGN** - Plan before executing. [PLAN], [DECOMPOSE], [WRITE-SPEC], [PROVE]
- **IMPLEMENT** - Execute the plan. [IMPLEMENT], [TEST], [FIX], [COMMIT]
- **REFINE** - Improve quality. [REVIEW], [VERIFY], [CRITIQUE], [RECONCILE]
- **DELIVER** - Complete and hand off. [VALIDATE], [MERGE], [DEPLOY], [CLOSE]

Verb vocabulary (all AGEN verbs, labels, states): `PROMPTSYSTEM_AGENTIC_ENGLISH.md` in this skill folder.

## Core Principles

- **Gates**: Checklist must pass before phase transition. Gate failures loop within phase.
- **Small cycles**: [IMPLEMENT]→[TEST]→[FIX]→green→next. Never large untestable steps.
- **Verb outcomes**: -OK (proceed), -FAIL (handle per verb), -SKIP (intentional).
- **Workflow type**: BUILD (code) or SOLVE (knowledge). Determined in EXPLORE, persists unless switched with [ACTOR] confirmation.
- **Complexity**: LOW=patch, MEDIUM=minor, HIGH=major (maps to semantic versioning).
- **Visual verification**: UI/game/graphics work MUST include visual [PROVE] before full implementation.

## Entry Rule

All workflows start in EXPLORE with [ASSESS] to determine workflow type and complexity/problem-type.

**Gate output is mandatory.** Before each phase transition, agent MUST output explicit gate evaluation (see Mandatory Gate Output). No self-approval without evidence.

**Artifact verification.** Agent MUST list created artifacts (files) as gate evidence. Claiming "plan complete" without artifact files is gate bypass.

**Research before implementation.** If task requires accuracy to an external system, [RESEARCH] with cited sources is mandatory. Training data assumptions are not research.

**Visual reference for replicas.** Replica/clone work MUST include visual reference (screenshot/video) during EXPLORE, not just text research.

## Workflow Types

### BUILD (via `/go`)

Primary output is working code. Triggers: "Add a feature...", "Build...", "Implement..."

Assessment: COMPLEXITY-LOW / COMPLEXITY-MEDIUM / COMPLEXITY-HIGH

Required documents by complexity:
- **LOW**: Inline plan sufficient, documents optional
- **MEDIUM**: `_SPEC_*.md` + `_IMPL_*.md` required (NO EXCEPTIONS - create files before proceeding)
- **HIGH**: All documents required (`_INFO_*.md`, `_SPEC_*.md`, `_IMPL_*.md`, `_TEST_*.md`)

**Gate enforcement**: DESIGN→IMPLEMENT gate MUST list actual file paths created. If files don't exist, gate fails.

### SOLVE (via `/go`)

Primary output is knowledge, decisions, or documents. Triggers: "Research...", "Evaluate...", "Write...", "Decide..."

Assessment: RESEARCH / ANALYSIS / EVALUATION / WRITING / DECISION / HOTFIX / BUGFIX

Note: HOTFIX/BUGFIX are SOLVE because primary focus is understanding the problem; code fix is secondary.

## Phase Gates

### EXPLORE → DESIGN

- [ ] Problem or goal clearly understood
- [ ] Workflow type determined (BUILD or SOLVE)
- [ ] Assessment complete (BUILD: COMPLEXITY | SOLVE: PROBLEM-TYPE)
- [ ] Scope boundaries defined
- [ ] No blocking unknowns requiring [ACTOR] input

### DESIGN → IMPLEMENT

- [ ] Approach documented (outline, spec, or plan)
- [ ] Risky parts proven via POC (if COMPLEXITY-MEDIUM or higher)
- [ ] No open questions requiring [ACTOR] decision
- [ ] For BUILD: SPEC, IMPL, TEST documents created
- [ ] For BUILD: TASKS document created via [PARTITION]
- [ ] For SOLVE: Structure/criteria validated

### IMPLEMENT → REFINE

- [ ] Core work complete (code written / document drafted)
- [ ] For BUILD: Tests pass
- [ ] For BUILD: No TODO/FIXME left unaddressed
- [ ] For SOLVE: All sections drafted
- [ ] Progress committed/saved

### REFINE → DELIVER

- [ ] Self-review complete
- [ ] Verification against spec/rules passed
- [ ] For BUILD COMPLEXITY-MEDIUM+: Critique and reconcile complete
- [ ] For SOLVE: Claims verified, arguments strengthened
- [ ] All found issues fixed

### DELIVER → DONE

- [ ] Validated, merged, deployed (if applicable), session closed

## Workflow Examples

### BUILD (COMPLEXITY-HIGH)

```
[EXPLORE] → [RESEARCH] → [ANALYZE] → [ASSESS] → [SCOPE] → Gate
[DESIGN]  → [PLAN] → [WRITE-SPEC] → [WRITE-IMPL-PLAN] → [PROVE] → [PARTITION] → Gate
[IMPLEMENT] → [IMPLEMENT] → [TEST] → [FIX] → [COMMIT] → Gate (loop until green)
[REFINE] → [REVIEW] → [VERIFY] → [CRITIQUE] → [RECONCILE] → Gate
[DELIVER] → [VALIDATE] → [MERGE] → [CLOSE] → [ARCHIVE]
```

### SOLVE (EVALUATION)

```
[EXPLORE] → [RESEARCH] → [ANALYZE] → [ASSESS] → EVALUATION → Gate
[DESIGN]  → [FRAME] → [OUTLINE] criteria → [DEFINE] framework → Gate
[IMPLEMENT] → [RESEARCH] options → [EVALUATE] → [SYNTHESIZE] → Gate
[REFINE] → [CRITIQUE] → [VERIFY] claims → [IMPROVE] → Gate
[DELIVER] → [CONCLUDE] → [RECOMMEND] → [VALIDATE] → [ARCHIVE]
```

**Note:** COMPLEXITY-LOW skips [PROVE], [CRITIQUE], [RECONCILE].

## Phase Plan Requirements

Plans created via [PLAN] must define:
- **Objectives** - What success looks like
- **Strategy** - How to achieve objectives
- **Deliverables** - Concrete outputs with checkboxes
- **Transitions** - When to move to next phase

**Planning Horizon:**
```
[EXPLORE]   ← Plan now
[DESIGN]    ← Plan now
[IMPLEMENT] ← TBD (after DESIGN gate)
[REFINE]    ← TBD (after IMPLEMENT gate)
[DELIVER]   ← Plan now (shipping tasks from NOTES)
```

## How to Plan Well

### Goal Decomposition

1. **Start with outcome** - What does "done" look like?
2. **Identify dependencies** - What must complete before what?
3. **Find parallel opportunities** - What can run concurrently?
4. **Size steps for testability** - Each step should be verifiable

### Scope Calibration

- **Too big**: Step takes >30min AWH or touches >3 files → decompose further
- **Too small**: Step takes <2min AWH → combine with adjacent step
- **Right size**: Verifiable outcome, clear done criteria, single responsibility
- **Prompt-executed steps**: size per @skills:write-documents `TASKS_GUIDES.md` Section 3 instead of the minute-based limits above

### Dependency Mapping

Ask for each step:
- What inputs do I need? (determines predecessors)
- What outputs do I produce? (determines successors)
- Can this run while something else runs? (candidate for Concurrent block)

### Common Planning Mistakes

- **Vague objectives**: "Make it work" → Define specific success criteria
- **Missing dependencies**: Steps that assume prior work → Explicit `← Px-Sy`
- **Over-sequencing**: All steps linear when some could parallelize
- **Under-estimating**: No AWH in Strategy → Add time budget
- **Skipping verification**: No test step after implement → Add [TEST] or [VERIFY]

## Next Action Logic

1. **Check phase gate** → Pass? → Next phase, first verb
2. **Gate fails?** → Execute verb that addresses unchecked item
3. **Verb outcome:** -OK → next verb | -FAIL → handle | -SKIP → next verb
4. **No more verbs?** → Re-evaluate gate
5. **[DELIVER] done?** → [CLOSE] and [ARCHIVE] if session-based

**Common failure handlers:**
- -FAIL on [RESEARCH], [ASSESS], [PLAN] → [CONSULT] or more [RESEARCH]
- -FAIL on [TEST], [VERIFY] → [FIX] → retry

## Effort Allocation

### Time Units

- **AWH** (Agent Work Hours) - Agent processing time, excludes user wait
- **HWH** (Human Work Hours) - Human equivalent effort for task sizing. TASKS items carry HWH estimates (@skills:write-documents `TASKS_GUIDES.md` Section 2); `PROMPTS_GUIDES.md` Section 1g converts HWH into prompt count and cost per model

### Phase Budgets by Complexity

| Phase | LOW | MEDIUM | HIGH |
|-------|-----|--------|------|
| EXPLORE | 5min | 15min | 30min |
| DESIGN | 5min | 30min | 60min |
| IMPLEMENT | varies | varies | varies |
| REFINE | 5min | 15min | 30min |
| DELIVER | 2min | 5min | 10min |

Values are AWH guidelines, not hard limits.

### Diminishing Returns

- Phase takes 2x budget without gate progress → [CONSULT]
- Same step retried 3x without improvement → [CONSULT]
- Research yields no new information after 3 sources → move on

### Retry Limits

- **COMPLEXITY-LOW**: Infinite retries (until user stops)
- **COMPLEXITY-MEDIUM/HIGH**: Max 5 attempts per phase, then [CONSULT] with [ACTOR]
  - When `[ACTOR] = agent`: self-resolve, log decision, proceed

## Stuck Detection

If no progress after retry limit:
1. Document in PROBLEMS.md
2. [CONSULT] with [ACTOR]:
   - `[ACTOR] = user`: present problem, wait for guidance
   - `[ACTOR] = agent`: evaluate alternatives against rules, log decision, proceed or [DEFER]
3. Either get guidance or [DEFER] and continue

## Phase Tracking

- Agent updates NOTES.md with current phase on transition. User adds notes manually.
- Agent maintains full phase plan in PROGRESS.md (phases with status: pending/in_progress/done).

## Planning Notation

Use appropriate notation based on scope:

- **STRUT** - High-level orchestration for complex multi-phase processes
  - When: Multi-phase work, autonomous runs (/go), session-spanning tasks, deep research
  - Contains: Phases, Objectives, Strategy, Steps, Deliverables, Transitions, **Time Log**
  - Tracks: Phase state, active intervals, net working time
  - Invoke: @skills:write-documents for STRUT_TEMPLATE.md or `/write-strut`
  - Verify: /verify workflow (STRUT Planning + STRUT Transition contexts)

- **TASKS** - Low-level execution for granular task coordination
  - When: Single-phase execution, partitioned IMPL steps, research file-by-file work
  - Contains: Task items with files, done-when criteria, verification commands, **task estimates in HWH (Human Work Hours)** (per @skills:write-documents `TASKS_GUIDES.md`)
  - Tracks: Individual task progress, timing `[HH:MM-HH:MM]`, parallel execution
  - Created via: [PARTITION] verb from IMPL plan or Phase 4 of research strategies

## Mandatory Gate Output

Before proceeding to next phase, output:

```markdown
## Gate: [CURRENT_PHASE] → [NEXT_PHASE]

**Complexity**: [LOW/MEDIUM/HIGH] | **Artifacts**: [list created docs]

- [x] Item - Evidence: [specific evidence]
- [ ] Item - BLOCKED: [what's missing]

**Gate status**: PASS | FAIL
```
