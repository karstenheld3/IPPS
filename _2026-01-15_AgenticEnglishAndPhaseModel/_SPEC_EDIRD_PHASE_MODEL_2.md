# SPEC: EDIRD Phase Model v2

**Doc ID**: EDIRD-SP04
**Goal**: Unified phase model for BUILD and SOLVE workflows with deterministic next-action logic for autonomous agent operation

**Depends on:**
- `_SPEC_AGEN_AGENTIC_ENGLISH.md [AGEN-SP01]` for verb definitions and syntax

## MUST-NOT-FORGET

- Phases: EXPLORE, DESIGN, IMPLEMENT, REFINE, DELIVER (EDIRD)
- Workflow types: BUILD (code output) and SOLVE (knowledge/decision output)
- Gates determine phase transitions - agent checks gate before proceeding
- Agent can always determine next action from: current phase + workflow type + last verb outcome
- [ACTOR] = Agent in autonomous mode, User in interactive mode
- Execute verbs in listed order; re-check gate after each verb completion
- Stuck detection: If no gate progress after 3 verb cycles, or 3 consecutive [FIX] attempts fail, [CONSULT] [ACTOR]

## Table of Contents

- [1. Scenario](#1-scenario)
- [2. Context](#2-context)
- [3. Domain Objects](#3-domain-objects)
- [4. Concept](#4-concept)
- [5. Workflow Types](#5-workflow-types)
- [6. Phase Definitions](#6-phase-definitions)
- [7. Phase Gates](#7-phase-gates)
- [8. Verb Mapping](#8-verb-mapping)
- [9. Next Action Logic](#9-next-action-logic)
- [10. Workflow Flows](#10-workflow-flows)
- [11. Hybrid Situations](#11-hybrid-situations)
- [12. Context States](#12-context-states)
- [13. Functional Requirements](#13-functional-requirements)
- [14. Design Decisions](#14-design-decisions)
- [15. Implementation Guarantees](#15-implementation-guarantees)
- [16. Document History](#16-document-history)

## 1. Scenario

**Problem:** Development workflows lack consistent phase structure. Agents and humans use different terminology, skip important steps, or apply heavyweight processes to simple tasks. Additionally, non-code work (research, writing, decisions) lacks a structured approach.

**Solution:**
- Define 5 standard phases: EXPLORE, DESIGN, IMPLEMENT, REFINE, DELIVER (EDIRD)
- Support two workflow types: BUILD (code) and SOLVE (knowledge/decisions)
- Map verbs to phases based on complexity level or problem type
- Use gates to ensure prerequisites before phase transitions
- Enable deterministic next-action logic for autonomous agent operation

**What we don't want:**
- Rigid waterfall - phases can overlap and iterate
- One-size-fits-all - complexity determines which verbs apply
- Bureaucracy for simple changes - COMPLEXITY-LOW skips heavy documentation
- Code-only focus - SOLVE workflow handles research, writing, decisions

## 2. Context

This specification consolidates:
- `_SPEC_EDIRD_PHASE_MODEL.md [EDIRD-SP01]` - Original phase model
- `_SPEC_EDIRD_VARIATION_A_UNIFIED.md [EDIRD-SP02]` - Unified BUILD/SOLVE model
- `_SPEC_EDIRD_VARIATION_B_DUAL.md [EDIRD-SP03]` - Gate checklists and hybrid situations

The model synthesizes terminology from Agile, ITIL, PRINCE2, Shape Up, Double Diamond, Scrum, and SDLC into a unified 5-phase structure that applies to both code creation and general problem-solving.

## 3. Domain Objects

### Phase

A **Phase** is a high-level stage in the workflow.

**Properties:**
- `name` - Phase identifier (EXPLORE, DESIGN, IMPLEMENT, REFINE, DELIVER)
- `verbs` - List of applicable verbs for this phase
- `gate` - Checklist of prerequisites for exiting this phase

### Workflow Type

A **Workflow Type** determines the primary output and verb emphasis.

**Values:**
- BUILD - Primary output is working code
- SOLVE - Primary output is knowledge, decisions, or documents

### Complexity Level (BUILD)

A **Complexity Level** determines which verbs apply within each phase for BUILD workflows.

**Values:**
- COMPLEXITY-LOW - Single file, clear scope, no dependencies (patch version)
- COMPLEXITY-MEDIUM - Multiple files, some dependencies, backward compatible (minor version)
- COMPLEXITY-HIGH - Breaking changes, new patterns, external APIs (major version)

### Problem Type (SOLVE)

A **Problem Type** classifies SOLVE work for appropriate verb emphasis.

**Values:**
- RESEARCH - Explore topic, gather information
- ANALYSIS - Deep dive into data or situation
- EVALUATION - Compare options, make recommendations
- WRITING - Create documents, books, reports
- DECISION - Choose between alternatives
- HOTFIX - Production down (code-related)
- BUGFIX - Defect investigation
- CHORE - Maintenance analysis
- MIGRATION - Data or system migration

### Gate

A **Gate** is a checklist of prerequisites that must be satisfied before transitioning to the next phase.

**Properties:**
- `from_phase` - Source phase
- `to_phase` - Target phase
- `checklist` - List of verification items
- `workflow_conditions` - Additional items based on workflow type/complexity

## 4. Concept

A single phase model that adapts to work type through workflow selection. The agent determines the next action at any point using:

```
next_action = f(workflow_type, current_phase, last_verb_outcome, gate_status)
```

This enables fully autonomous operation when [ACTOR] = Agent.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        EDIRD Phase Model v2                             │
├─────────────────────────────────────────────────────────────────────────┤
│  [EXPLORE] → [DESIGN] → [IMPLEMENT] → [REFINE] → [DELIVER]              │
├─────────────────────────────────────────────────────────────────────────┤
│  Workflow: BUILD                  │  Workflow: SOLVE                    │
│  Output: Working code             │  Output: Knowledge/decisions        │
│  Assess: COMPLEXITY               │  Assess: PROBLEM-TYPE               │
└─────────────────────────────────────────────────────────────────────────┘
```

## 5. Workflow Types

### BUILD

**Purpose**: Create new software, features, systems

**Primary output**: Working code

**Triggers**:
- "Add a feature..."
- "Build a system..."
- "Implement..."
- "Create an API..."

**Assessment**: COMPLEXITY-LOW / COMPLEXITY-MEDIUM / COMPLEXITY-HIGH

### SOLVE

**Purpose**: Explore problems, evaluate ideas, create knowledge, make decisions

**Primary output**: Documents, decisions, insights, recommendations

**Triggers**:
- "Research..."
- "Evaluate..."
- "Write..."
- "Decide..."
- "Analyze..."
- "Figure out..."

**Assessment**: RESEARCH / ANALYSIS / EVALUATION / WRITING / DECISION

**Problem types** (code-related SOLVE):
- HOTFIX - Production down
- BUGFIX - Defect in existing code
- CHORE - Maintenance, cleanup
- MIGRATION - Data or system migration

**Note**: HOTFIX/BUGFIX are SOLVE because primary focus is understanding the problem; code fix is secondary output.

## 6. Phase Definitions

### [EXPLORE]

- **Purpose**: Understand the situation before acting
- **BUILD**: What feature? What constraints? What patterns?
- **SOLVE**: What's the real problem? What do I need to learn?
- **Entry**: Start of workflow
- **Exit**: Gate EXPLORE→DESIGN passes
- **Verbs**: [RESEARCH], [ANALYZE], [ASSESS], [SCOPE], [GATHER], [CONSULT], [DECIDE]

### [DESIGN]

- **Purpose**: Plan the approach before executing
- **BUILD**: Specs, architecture, POCs, test strategy
- **SOLVE**: Structure, methodology, outline, criteria
- **Entry**: Gate EXPLORE→DESIGN passed
- **Exit**: Gate DESIGN→IMPLEMENT passes
- **Verbs**: [PLAN], [OUTLINE], [FRAME], [PROVE], [WRITE-SPEC], [WRITE-IMPL], [PROPOSE], [VALIDATE]

### [IMPLEMENT]

- **Purpose**: Execute the planned work
- **BUILD**: Write code, configure, integrate
- **SOLVE**: Write document, conduct analysis, perform research
- **Entry**: Gate DESIGN→IMPLEMENT passed
- **Exit**: Gate IMPLEMENT→REFINE passes
- **Verbs**: [IMPLEMENT], [WRITE], [RESEARCH], [ANALYZE], [EVALUATE], [SYNTHESIZE], [CONFIGURE], [INTEGRATE], [COMMIT]

### [REFINE]

- **Purpose**: Improve quality through review and iteration
- **BUILD**: Test, review, fix bugs, optimize
- **SOLVE**: Edit, critique, verify claims, strengthen arguments
- **Entry**: Gate IMPLEMENT→REFINE passed
- **Exit**: Gate REFINE→DELIVER passes
- **Verbs**: [REVIEW], [VERIFY], [TEST], [CRITIQUE], [RECONCILE], [FIX], [IMPROVE], [OPTIMIZE]

### [DELIVER]

- **Purpose**: Complete and hand off
- **BUILD**: Deploy, document, merge, close
- **SOLVE**: Present, conclude, recommend, decide, archive
- **Entry**: Gate REFINE→DELIVER passed
- **Exit**: Workflow complete
- **Verbs**: [CONCLUDE], [RECOMMEND], [PROPOSE], [VALIDATE], [DEPLOY], [MERGE], [FINALIZE], [HANDOFF], [CLOSE], [ARCHIVE]

## 7. Phase Gates

Gates are checklists that must pass before transitioning. Agent evaluates gates automatically.

### EXPLORE → DESIGN

```
┌─ Gate: EXPLORE → DESIGN ─────────────────────────────────────────────┐
│                                                                       │
│  [ ] Problem or goal clearly understood                               │
│  [ ] Workflow type determined (BUILD or SOLVE)                        │
│  [ ] Assessment complete:                                             │
│      - BUILD: COMPLEXITY-LOW/MEDIUM/HIGH                              │
│      - SOLVE: PROBLEM-TYPE identified                                 │
│  [ ] Scope boundaries defined                                         │
│  [ ] No blocking unknowns requiring [ACTOR] input                     │
│                                                                       │
│  If any unchecked → remain in [EXPLORE], execute next verb            │
│  If all checked → proceed to [DESIGN]                                 │
└───────────────────────────────────────────────────────────────────────┘
```

### DESIGN → IMPLEMENT

```
┌─ Gate: DESIGN → IMPLEMENT ───────────────────────────────────────────┐
│                                                                       │
│  [ ] Approach documented (outline, spec, or plan)                     │
│  [ ] Risky parts proven via POC (if COMPLEXITY-HIGH)                  │
│  [ ] No open questions requiring [ACTOR] decision                     │
│  [ ] For BUILD MEDIUM+: Test strategy defined                         │
│  [ ] For SOLVE: Structure/criteria validated                          │
│                                                                       │
│  If any unchecked → remain in [DESIGN], execute next verb             │
│  If all checked → proceed to [IMPLEMENT]                              │
└───────────────────────────────────────────────────────────────────────┘
```

### IMPLEMENT → REFINE

```
┌─ Gate: IMPLEMENT → REFINE ───────────────────────────────────────────┐
│                                                                       │
│  [ ] Core work complete (code written / document drafted)             │
│  [ ] For BUILD: Tests pass                                            │
│  [ ] For BUILD: No TODO/FIXME left unaddressed                        │
│  [ ] For SOLVE: All sections drafted                                  │
│  [ ] Progress committed/saved                                         │
│                                                                       │
│  If any unchecked → remain in [IMPLEMENT], execute next verb          │
│  If all checked → proceed to [REFINE]                                 │
└───────────────────────────────────────────────────────────────────────┘
```

### REFINE → DELIVER

```
┌─ Gate: REFINE → DELIVER ─────────────────────────────────────────────┐
│                                                                       │
│  [ ] Self-review complete                                             │
│  [ ] Verification against spec/rules passed                           │
│  [ ] For BUILD COMPLEXITY-HIGH: Critique and reconcile complete       │
│  [ ] For SOLVE: Claims verified, arguments strengthened               │
│  [ ] All found issues fixed                                           │
│                                                                       │
│  If any unchecked → remain in [REFINE], execute next verb             │
│  If all checked → proceed to [DELIVER]                                │
└───────────────────────────────────────────────────────────────────────┘
```

## 8. Verb Mapping

### BUILD Workflow Verbs by Phase

```
[EXPLORE]
├─> [RESEARCH] existing solutions and patterns
├─> [ANALYZE] affected code and dependencies
├─> [GATHER] requirements and context
├─> [ASSESS] → COMPLEXITY-LOW/MEDIUM/HIGH
├─> [SCOPE] define boundaries
├─> [CONSULT] with [ACTOR] on requirements (if needed)
└─> [DECIDE] approach

[DESIGN]
├─> [PLAN] structured approach
├─> [OUTLINE] high-level structure (all)
├─> [WRITE-SPEC] specification (MEDIUM+)
├─> [PROVE] risky parts with POC (HIGH)
├─> [PROPOSE] options to [ACTOR] (HIGH)
├─> [VALIDATE] design with [ACTOR]
├─> [WRITE-IMPL] implementation plan (MEDIUM+)
└─> [WRITE-TEST] test plan (HIGH)

[IMPLEMENT]
├─> [IMPLEMENT] code changes
├─> [CONFIGURE] environment/settings
├─> [INTEGRATE] components (MEDIUM+)
├─> [TEST] during implementation
├─> [REFACTOR] as needed
└─> [COMMIT] small, frequent

[REFINE]
├─> [REVIEW] self-review
├─> [VERIFY] against spec/rules
├─> [TEST] regression testing
├─> [CRITIQUE] devil's advocate (HIGH)
├─> [RECONCILE] pragmatic adjustments (HIGH)
├─> [FIX] found issues
└─> [OPTIMIZE] if needed

[DELIVER]
├─> [TEST] final pass
├─> [VALIDATE] with [ACTOR]
├─> [MERGE] branches
├─> [DEPLOY] to environment
├─> [FINALIZE] documentation
├─> [HANDOFF] communicate
├─> [CLOSE] mark done
└─> [ARCHIVE] if session-based
```

### SOLVE Workflow Verbs by Phase

```
[EXPLORE]
├─> [RESEARCH] the topic, domain, or problem space
├─> [ANALYZE] existing information, data, context
├─> [GATHER] logs, context, requirements
├─> [ASSESS] → problem type (RESEARCH/ANALYSIS/EVALUATION/WRITING/DECISION)
├─> [SCOPE] define what question to answer
├─> [ENUMERATE] all aspects to consider
├─> [CONSULT] with [ACTOR] to clarify scope (if needed)
└─> [DECIDE] framing of the problem

[DESIGN]
├─> [FRAME] the problem structure
├─> [PLAN] approach and methodology
├─> [OUTLINE] structure (document, analysis, evaluation)
├─> [DEFINE] criteria or evaluation framework
├─> [PROVE] assumptions if needed
├─> [PROPOSE] structure to [ACTOR]
└─> [VALIDATE] approach covers the problem

[IMPLEMENT]
├─> [RESEARCH] deep dive (RESEARCH type)
├─> [ANALYZE] data/situation (ANALYSIS type)
├─> [WRITE] content (WRITING type)
├─> [EVALUATE] options against criteria (EVALUATION type)
├─> [SYNTHESIZE] findings into understanding
├─> [DRAFT] initial versions
├─> [IMPLEMENT] code if solution requires it
└─> [COMMIT] progress checkpoints

[REFINE]
├─> [REVIEW] own work
├─> [VERIFY] claims and accuracy
├─> [CRITIQUE] find weaknesses
├─> [RECONCILE] balance ideal vs practical
├─> [FIX] errors and gaps
└─> [IMPROVE] clarity and quality

[DELIVER]
├─> [CONCLUDE] draw final conclusions
├─> [SUMMARIZE] key findings
├─> [RECOMMEND] if single option (with rationale)
├─> [PROPOSE] if multiple options
├─> [PRESENT] findings to [ACTOR]
├─> [VALIDATE] with [ACTOR]
├─> [DECIDE] final choice (DECISION type)
├─> [FINALIZE] polish and complete
├─> [HANDOFF] communicate findings
├─> [CLOSE] mark complete
└─> [ARCHIVE] for future reference
```

## 9. Next Action Logic

The agent determines the next action using this decision tree:

```
┌─ NEXT ACTION DECISION TREE ──────────────────────────────────────────┐
│                                                                       │
│  1. What is current phase?                                            │
│     └─> Check phase gate                                              │
│                                                                       │
│  2. Does gate pass?                                                   │
│     ├─> YES: Transition to next phase, start first verb               │
│     └─> NO: What gate item is unchecked?                              │
│         └─> Execute verb that addresses unchecked item                │
│                                                                       │
│  3. What was last verb outcome?                                       │
│     ├─> -OK: Proceed to next verb in phase                            │
│     ├─> -FAIL: Handle based on verb (see transitions below)           │
│     └─> -SKIP: Proceed to next verb (complexity didn't require it)    │
│                                                                       │
│  4. No more verbs in phase?                                           │
│     └─> Re-evaluate gate                                              │
│                                                                       │
│  5. In [DELIVER] and all done?                                        │
│     └─> [CLOSE] and [ARCHIVE] if session-based                        │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

### Verb Outcome Transitions

```
[RESEARCH]-OK   → next verb in sequence
[RESEARCH]-FAIL → [CONSULT] (need help finding info)

[ASSESS]-OK     → [SCOPE] or [DECIDE]
[ASSESS]-FAIL   → [RESEARCH] (need more context)

[PROVE]-OK      → [WRITE-SPEC] or proceed to gate check
[PROVE]-FAIL    → [RESEARCH] (back to explore fundamentals)

[VERIFY]-OK     → next verb or gate check
[VERIFY]-FAIL   → [FIX] → [VERIFY] (loop until OK)

[CRITIQUE]-OK   → [RECONCILE]
[CRITIQUE]-FAIL → [FIX] (immediate issues found)

[TEST]-OK       → next verb or gate check
[TEST]-FAIL     → [FIX] → [TEST] (loop until OK)

[VALIDATE]-OK   → proceed
[VALIDATE]-FAIL → [CONSULT] (clarify requirements)

[CONSULT]-OK    → resume previous activity
[CONSULT]-FAIL  → [QUESTION] more specifically, or escalate
```

### Autonomous Mode Decision

When [ACTOR] = Agent, the agent uses this logic:

```
IF gate_passes(current_phase):
    current_phase = next_phase
    current_verb = first_verb_for(current_phase, workflow_type, complexity)
ELSE:
    unchecked = find_unchecked_gate_items()
    current_verb = verb_that_addresses(unchecked[0])
    
EXECUTE current_verb

IF verb_outcome == OK:
    current_verb = next_verb_in_sequence()
ELIF verb_outcome == FAIL:
    current_verb = failure_handler(current_verb)
ELIF verb_outcome == SKIP:
    current_verb = next_verb_in_sequence()
```

## 10. Workflow Flows

### BUILD COMPLEXITY-HIGH Flow

```
[EXPLORE]
├─> [RESEARCH] → [ANALYZE] → [GATHER] → [ASSESS] → [SCOPE] → [DECIDE]
└─> Gate check

[DESIGN]
├─> [PLAN] → [OUTLINE] → [WRITE-SPEC] → [PROVE] → [PROPOSE] → [VALIDATE]
├─> [WRITE-IMPL] → [WRITE-TEST]
└─> Gate check

[IMPLEMENT]
├─> [IMPLEMENT] → [CONFIGURE] → [INTEGRATE] → [TEST] → [COMMIT]
└─> Gate check

[REFINE]
├─> [REVIEW] → [VERIFY] → [TEST] → [CRITIQUE] → [RECONCILE] → [FIX]
└─> Gate check

[DELIVER]
├─> [VALIDATE] → [MERGE] → [DEPLOY] → [FINALIZE] → [HANDOFF] → [CLOSE]
└─> [ARCHIVE] if session-based
```

### BUILD COMPLEXITY-LOW Flow

```
[EXPLORE]
├─> [ANALYZE] → [ASSESS] → [DECIDE]
└─> Gate check

[DESIGN]
├─> [OUTLINE]
└─> Gate check

[IMPLEMENT]
├─> [IMPLEMENT] → [TEST] → [COMMIT]
└─> Gate check

[REFINE]
├─> [REVIEW] → [FIX]
└─> Gate check

[DELIVER]
├─> [MERGE] → [CLOSE]
└─> Done
```

### SOLVE EVALUATION Flow

```
[EXPLORE]
├─> [RESEARCH] → [ANALYZE] → [ASSESS] → EVALUATION → [SCOPE] → [ENUMERATE]
└─> Gate check

[DESIGN]
├─> [FRAME] → [OUTLINE] criteria → [DEFINE] evaluation framework → [VALIDATE]
└─> Gate check

[IMPLEMENT]
├─> [RESEARCH] each option → [ANALYZE] against criteria → [EVALUATE] → [SYNTHESIZE]
└─> Gate check

[REFINE]
├─> [REVIEW] → [VERIFY] claims → [CRITIQUE] → [RECONCILE] → [IMPROVE]
└─> Gate check

[DELIVER]
├─> [CONCLUDE] → [RECOMMEND] with rationale → [PRESENT] → [VALIDATE] → [ARCHIVE]
└─> Done
```

### SOLVE WRITING Flow

```
[EXPLORE]
├─> [RESEARCH] topic → [ANALYZE] audience needs → [ASSESS] → WRITING → [SCOPE]
└─> Gate check

[DESIGN]
├─> [FRAME] → [OUTLINE] structure → [PLAN] examples → [VALIDATE] with [ACTOR]
└─> Gate check

[IMPLEMENT]
├─> [DRAFT] → [WRITE] sections → [RESEARCH] additional details → [COMMIT]
└─> Gate check

[REFINE]
├─> [REVIEW] → [CRITIQUE] → [VERIFY] facts → [IMPROVE] prose → [FIX]
└─> Gate check

[DELIVER]
├─> [FINALIZE] → [VALIDATE] with [ACTOR] → [HANDOFF] → [ARCHIVE]
└─> Done
```

### SOLVE HOTFIX Flow

```
[EXPLORE]
├─> [ANALYZE] identify root cause
├─> [GATHER] logs and context
├─> [ASSESS] → HOTFIX
└─> [DECIDE] fix approach
    └─> Gate: Root cause identified

[DESIGN]
├─> [PROVE] fix works
└─> [VALIDATE] with [ACTOR] (if time permits)
    └─> Gate: Fix proven

[IMPLEMENT]
├─> [FIX] apply fix
├─> [TEST] verify fix
└─> [COMMIT] with hotfix message
    └─> Gate: Fix applied, tests pass

[REFINE]
├─> [VERIFY] no regressions
├─> [TEST] regression testing
└─> [REVIEW] quick review
    └─> Gate: No regressions

[DELIVER]
├─> [DEPLOY] immediately
├─> [STATUS] notify stakeholders
└─> [CLOSE] mark resolved
```

### SOLVE DECISION Flow

```
[EXPLORE]
├─> [RESEARCH] options and constraints
├─> [ANALYZE] stakeholder needs
├─> [ASSESS] → DECISION
├─> [ENUMERATE] all factors
└─> [SCOPE] decision boundaries
    └─> Gate check

[DESIGN]
├─> [FRAME] decision structure
├─> [DEFINE] evaluation criteria
├─> [OUTLINE] options to evaluate
└─> [VALIDATE] criteria with [ACTOR]
    └─> Gate check

[IMPLEMENT]
├─> [RESEARCH] each option
├─> [ANALYZE] against criteria
├─> [EVALUATE] score options
└─> [SYNTHESIZE] findings
    └─> Gate check

[REFINE]
├─> [CRITIQUE] blind spots?
├─> [VERIFY] assumptions
├─> [RECONCILE] trade-offs
└─> [IMPROVE] clarity
    └─> Gate check

[DELIVER]
├─> [CONCLUDE] final assessment
├─> [RECOMMEND] with rationale
├─> [VALIDATE] with [ACTOR]
├─> [DECIDE] final choice
└─> [ARCHIVE] decision rationale
```

## 11. Hybrid Situations

Some work involves both BUILD and SOLVE workflows.

### SOLVE then BUILD

Research best approach, then build it:

```
┌─ SOLVE Workflow ──────────────────────────────────────────────────────┐
│                                                                       │
│  [EXPLORE] → [DESIGN] → [IMPLEMENT] → [REFINE] → [DELIVER]            │
│                                                    │                  │
│  Output: Decision or recommendation ───────────────┘                  │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─ BUILD Workflow ──────────────────────────────────────────────────────┐
│                                                                       │
│  [EXPLORE] → [DESIGN] → [IMPLEMENT] → [REFINE] → [DELIVER]            │
│  (use decision from SOLVE as input)                                   │
│                                                                       │
│  Output: Working code                                                 │
└───────────────────────────────────────────────────────────────────────┘
```

**Example**: "Should we use PostgreSQL or MongoDB?" (SOLVE: EVALUATION) → decision made → "Implement PostgreSQL integration" (BUILD)

### BUILD with Embedded SOLVE

Building requires investigation mid-workflow:

```
┌─ BUILD Workflow ──────────────────────────────────────────────────────┐
│                                                                       │
│  [EXPLORE] → [DESIGN]                                                 │
│                  │                                                    │
│                  ▼ Encounter unknown                                  │
│           ┌─ Mini SOLVE ──────────┐                                   │
│           │ [EXPLORE] → [DESIGN]  │                                   │
│           │ → [IMPLEMENT] → ...   │                                   │
│           │ → [DELIVER](insight)  │                                   │
│           └───────────────────────┘                                   │
│                  │                                                    │
│                  ▼ Resume with knowledge                              │
│            [DESIGN] continued → [IMPLEMENT] → [REFINE] → [DELIVER]    │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

**Example**: While designing auth system, need to research OAuth providers → mini SOLVE (RESEARCH) → return to BUILD with findings

### Switching Workflows

Agent can switch workflows if assessment changes:

```
IF during [EXPLORE]:
    initial_assessment = BUILD
    BUT primary_output_changes_to_document
THEN:
    [CONSULT] with [ACTOR]: "This looks more like a SOLVE workflow. Confirm?"
    IF confirmed:
        workflow_type = SOLVE
        restart_with_appropriate_verbs
```

## 12. Context States

Context states (no brackets) used for branching:

### Workflow Type

- **BUILD** - Primary output is working code
- **SOLVE** - Primary output is knowledge, decisions, or documents

### Complexity (BUILD)

- **COMPLEXITY-LOW** - Single file, clear scope → patch version
- **COMPLEXITY-MEDIUM** - Multiple files, some dependencies → minor version
- **COMPLEXITY-HIGH** - Breaking changes, new patterns → major version

### Problem Type (SOLVE)

- **RESEARCH** - Explore topic, gather information
- **ANALYSIS** - Deep dive into data or situation
- **EVALUATION** - Compare options, make recommendations
- **WRITING** - Create documents, books, reports
- **DECISION** - Choose between alternatives
- **HOTFIX** - Production down (code-related)
- **BUGFIX** - Defect investigation
- **CHORE** - Maintenance analysis
- **MIGRATION** - Data or system migration

## 13. Functional Requirements

**EDIRD-FR-01: Phase Structure**
- Workflow consists of 5 sequential phases: EXPLORE, DESIGN, IMPLEMENT, REFINE, DELIVER
- Phases use bracket syntax `[PHASE]` as instruction tokens
- Each phase maps to specific verbs from Agentic English vocabulary

**EDIRD-FR-02: Workflow Type Selection**
- First action determines workflow type: BUILD or SOLVE
- BUILD: Primary output is working code
- SOLVE: Primary output is knowledge, decisions, or documents
- Workflow type determines verb emphasis and assessment criteria

**EDIRD-FR-03: Complexity/Problem Assessment**
- For BUILD: `[ASSESS]` determines COMPLEXITY-LOW/MEDIUM/HIGH
- For SOLVE: `[ASSESS]` determines problem type (RESEARCH/ANALYSIS/EVALUATION/WRITING/DECISION/HOTFIX/BUGFIX/CHORE/MIGRATION)
- Assessment happens in EXPLORE phase
- Assessment determines which verbs apply in subsequent phases

**EDIRD-FR-04: Phase Gates**
- Each phase transition requires gate check
- Gate is a checklist of prerequisites
- Cannot proceed to next phase until gate passes
- Gates are context-dependent (workflow type, complexity, problem type)

**EDIRD-FR-05: Verb-Phase Mapping**
- Each verb belongs to one primary phase
- Verbs can be skipped based on complexity level or problem type
- Verb outcomes (-OK, -FAIL, -SKIP) determine next action

**EDIRD-FR-06: Deterministic Next Action**
- Agent can always determine next action from current state
- State = (workflow_type, current_phase, last_verb_outcome, gate_status)
- Enables fully autonomous operation when [ACTOR] = Agent

**EDIRD-FR-07: Workflow Branching**
- Context states (no brackets) appear in condition headers
- Instruction tokens (brackets) appear in action steps
- Format: `## For CONTEXT-STATE` followed by `[VERB]` instructions

**EDIRD-FR-08: Hybrid Workflow Support**
- SOLVE can transition to BUILD (research then implement)
- BUILD can embed mini-SOLVE (investigate during implementation)
- Agent can switch workflows with [ACTOR] confirmation

## 14. Design Decisions

**EDIRD-DD-01:** Unified model for BUILD and SOLVE. Rationale: Same phases apply to any intellectual work; verb selection adapts to context.

**EDIRD-DD-02:** Gates enable autonomous operation. Rationale: Agent can always determine if phase is complete by evaluating gate checklist.

**EDIRD-DD-03:** Next action is deterministic. Rationale: Given current state (phase, workflow, last outcome, gate status), exactly one action is correct.

**EDIRD-DD-04:** Verb failures have defined handlers. Rationale: Agent knows how to recover from any failure without [ACTOR] intervention (unless [CONSULT] required).

**EDIRD-DD-05:** Complexity/problem-type assessed in EXPLORE. Rationale: Early assessment determines verb depth for entire workflow.

**EDIRD-DD-06:** SOLVE includes code-related problem types. Rationale: HOTFIX/BUGFIX start with problem investigation (SOLVE) before any code changes.

**EDIRD-DD-07:** Five-phase model (E-D-I-R-D). Rationale: Balances granularity with simplicity. Covers exploration, planning, execution, refinement, and delivery.

**EDIRD-DD-08:** Complexity determines verb application, not phase skipping. Rationale: All phases execute, but with different depth. COMPLEXITY-LOW still has DESIGN phase, just with `[OUTLINE]` instead of `[SPEC]`.

## 15. Implementation Guarantees

**EDIRD-IG-01:** Phase names are stable vocabulary - EXPLORE, DESIGN, IMPLEMENT, REFINE, DELIVER will not change.

**EDIRD-IG-02:** Complexity levels map to semantic versioning - LOW=patch, MEDIUM=minor, HIGH=major.

**EDIRD-IG-03:** All workflows start with EXPLORE phase containing `[ASSESS]` verb.

**EDIRD-IG-04:** Gate failures loop back within current phase, not to previous phases. Verb failures (e.g., `[PROVE]-FAIL`) may trigger iteration to earlier phases.

**EDIRD-IG-05:** Workflow type (BUILD/SOLVE) is determined in EXPLORE and persists for entire workflow unless explicitly switched with [ACTOR] confirmation.

**EDIRD-IG-06:** Every verb outcome (-OK, -FAIL, -SKIP) has a defined handler - agent never gets stuck without knowing next action.

## 16. Document History

**[2026-01-15 19:35]**
- Added: Stuck detection rule to MUST-NOT-FORGET (3 verb cycles or 3 [FIX] attempts)
- Added: Verb execution order clarification to MUST-NOT-FORGET
- Added: HOTFIX/BUGFIX rationale note in Workflow Types section
- Addressed: EDIRD-RV-01, RV-02, RV-03, RV-04 from Devil's Advocate review

**[2026-01-15 19:30]**
- Added: Scenario section (Problem/Solution/What we don't want)
- Added: Context section (consolidation references)
- Added: Domain Objects section (Phase, Workflow Type, Complexity Level, Problem Type, Gate)
- Added: Functional Requirements FR-01 through FR-08
- Added: Implementation Guarantees IG-01 through IG-06
- Added: Design Decisions DD-07 and DD-08
- Added: SOLVE HOTFIX Flow
- Added: SOLVE DECISION Flow
- Added: Hybrid Situations section (SOLVE→BUILD, embedded SOLVE, workflow switching)
- Updated: Table of Contents with all 16 sections

**[2026-01-15 19:25]**
- Initial v2 specification created
- Consolidated BUILD/SOLVE unified model from EDIRD-SP02
- Added comprehensive gate checklists from EDIRD-SP03
- Added Next Action Logic for autonomous agent operation
- Added verb outcome transition handlers
- Added workflow flows for BUILD (HIGH/LOW) and SOLVE (EVALUATION/WRITING)
- Moved workflow types and problem types from AGEN-SP01
