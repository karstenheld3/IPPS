# SPEC: EDIRD Phase Model

**Doc ID**: EDIRD-SP01
**Goal**: Specify the phase-based workflow model for agent-driven development

**Depends on:**
- `_SPEC_AGEN_AGENTIC_ENGLISH.md [AGEN-SP01]` for verb definitions and syntax

## MUST-NOT-FORGET

- Phases use brackets `[PHASE]` - they are instruction tokens
- Context states use no brackets (COMPLEXITY-HIGH, HOTFIX) - they are condition tokens
- Phase transitions require gate checks before proceeding
- Complexity assessment happens in EXPLORE phase, not before

## Table of Contents

- [1. Scenario](#1-scenario)
- [2. Context](#2-context)
- [3. Domain Objects](#3-domain-objects)
- [4. Functional Requirements](#4-functional-requirements)
- [5. Design Decisions](#5-design-decisions)
- [6. Implementation Guarantees](#6-implementation-guarantees)
- [7. Key Mechanisms](#7-key-mechanisms)
- [8. Action Flow](#8-action-flow)
- [9. Document History](#9-document-history)

## 1. Scenario

**Problem:** Development workflows lack consistent phase structure. Agents and humans use different terminology, skip important steps, or apply heavyweight processes to simple tasks.

**Solution:**
- Define 5 standard phases: EXPLORE, DESIGN, IMPLEMENT, REFINE, DELIVER
- Map verbs to phases based on complexity level
- Use gates to ensure prerequisites before phase transitions
- Support both FEATURE-BASED and PROBLEM-BASED workflows

**What we don't want:**
- Rigid waterfall - phases can overlap and iterate
- One-size-fits-all - complexity determines which verbs apply
- Bureaucracy for simple changes - COMPLEXITY-LOW skips heavy documentation

## 2. Context

This specification formalizes the phase model researched in `INFO_PROJECT_PHASES_OPTIONS.md [PHSE-IN01]`. The model synthesizes terminology from Agile, ITIL, PRINCE2, Shape Up, Double Diamond, Scrum, and SDLC into a unified 5-phase structure.

## 3. Domain Objects

### Phase

A **Phase** is a high-level stage in the development workflow.

**Properties:**
- `name` - Phase identifier (EXPLORE, DESIGN, IMPLEMENT, REFINE, DELIVER)
- `verbs` - List of applicable verbs for this phase
- `gate` - Checklist of prerequisites for exiting this phase

### Complexity Level

A **Complexity Level** determines which verbs apply within each phase.

**Values:**
- COMPLEXITY-LOW - Single file, clear scope, no dependencies (patch version)
- COMPLEXITY-MEDIUM - Multiple files, some dependencies, backward compatible (minor version)
- COMPLEXITY-HIGH - Breaking changes, new patterns, external APIs (major version)

### Problem Type

A **Problem Type** classifies non-feature work for abbreviated workflows.

**Values:**
- HOTFIX - Production down, immediate action
- BUGFIX - Defect in existing functionality
- CHORE - Maintenance, cleanup, dependency updates
- MIGRATION - Data or system migration

### Gate

A **Gate** is a checklist of prerequisites that must be satisfied before transitioning to the next phase.

**Properties:**
- `from_phase` - Source phase
- `to_phase` - Target phase
- `checklist` - List of verification items

## 4. Functional Requirements

**EDIRD-FR-01: Phase Structure**
- Workflow consists of 5 sequential phases: EXPLORE, DESIGN, IMPLEMENT, REFINE, DELIVER
- Phases use bracket syntax `[PHASE]` as instruction tokens
- Each phase maps to specific verbs from Agentic English vocabulary

**EDIRD-FR-02: Complexity Assessment**
- First action in EXPLORE phase is `[ASSESS]` complexity
- Complexity determines which verbs apply in subsequent phases
- For COMPLEXITY-LOW: skip heavy documentation (specs, plans)
- For COMPLEXITY-HIGH: require POC, specs, and full review cycle

**EDIRD-FR-03: Phase Gates**
- Each phase transition requires gate check
- Gate is a checklist of prerequisites
- Cannot proceed to next phase until gate passes
- Gates are context-dependent (complexity, problem type)

**EDIRD-FR-04: Verb-Phase Mapping**
- Each verb belongs to one primary phase
- Verbs can be skipped based on complexity level
- Verb outcomes (-OK, -FAIL, -SKIP) determine next action

**EDIRD-FR-05: Problem-Based Workflows**
- HOTFIX, BUGFIX, CHORE, MIGRATION use abbreviated phase flows
- Problem type assessed in EXPLORE instead of complexity
- Same phase structure, different verb emphasis

**EDIRD-FR-06: Workflow Branching**
- Context states (no brackets) appear in condition headers
- Instruction tokens (brackets) appear in action steps
- Format: `## For CONTEXT-STATE` followed by `[VERB]` instructions

## 5. Design Decisions

**EDIRD-DD-01:** Five-phase model (E-D-I-R-D). Rationale: Balances granularity with simplicity. Covers exploration, planning, execution, refinement, and delivery.

**EDIRD-DD-02:** Complexity determines verb application, not phase skipping. Rationale: All phases execute, but with different depth. COMPLEXITY-LOW still has DESIGN phase, just with `[OUTLINE]` instead of `[SPEC]`.

**EDIRD-DD-03:** Gates use checklist format. Rationale: Explicit, verifiable conditions prevent premature phase transitions.

**EDIRD-DD-04:** Phases are instruction tokens (brackets). Rationale: Phases are actions the agent executes, not conditions to check.

**EDIRD-DD-05:** REFINE phase includes both self-review and external review. Rationale: Separates implementation from quality assurance, catches issues before delivery.

## 6. Implementation Guarantees

**EDIRD-IG-01:** Phase names are stable vocabulary - EXPLORE, DESIGN, IMPLEMENT, REFINE, DELIVER will not change.

**EDIRD-IG-02:** Complexity levels map to semantic versioning - LOW=patch, MEDIUM=minor, HIGH=major.

**EDIRD-IG-03:** All workflows start with EXPLORE phase containing `[ASSESS]` verb.

**EDIRD-IG-04:** Gate failures loop back within current phase, not to previous phases. Verb failures (e.g., `[PROVE]-FAIL`) may trigger iteration to earlier phases.

## 7. Key Mechanisms

### Complexity-Based Verb Filtering

Each phase has a full verb list. Complexity filters which verbs execute:

```
[DESIGN] phase verbs:
├─> [PLAN] - all complexities
├─> [OUTLINE] - all complexities
├─> [SPEC] - MEDIUM+
├─> [PROVE] - HIGH only
├─> [PROPOSE] - HIGH only
├─> [VALIDATE] - all complexities
├─> [WRITE-IMPL](SPEC) - MEDIUM+
└─> [WRITE-TEST](SPEC) - HIGH only
```

### Gate Checklist Pattern

Gates use checkbox format for clear verification:

```
DESIGN → IMPLEMENT gate:
├─> [ ] Approach documented (outline, spec, or plan)
├─> [ ] Risky parts proven via POC (if HIGH)
├─> [ ] No open questions requiring [ACTOR] decision
└─> [ ] Test strategy defined (if MEDIUM+)
```

### Verb Outcome Transitions

Verb outcomes determine control flow:

```
[PROVE]-OK   → [SPEC] or [IMPLEMENT]
[PROVE]-FAIL → [RESEARCH] (back to explore)
[VERIFY]-OK  → next phase
[VERIFY]-FAIL → [FIX] → [VERIFY] (loop until OK)
```

## 8. Action Flow

### Feature-Based Workflow (COMPLEXITY-HIGH)

```
[EXPLORE]
├─> [RESEARCH] existing solutions
├─> [ANALYZE] affected code
├─> [ASSESS] → COMPLEXITY-HIGH
├─> [CONSULT] with [ACTOR]
└─> [DECIDE] approach
    └─> Gate: Problem understood, scope confirmed

[DESIGN]
├─> [PLAN] structured approach
├─> [PROVE] risky parts with POC
├─> [SPEC] write specification
├─> [PROPOSE] options to [ACTOR]
├─> [VALIDATE] design
├─> [WRITE-IMPL](SPEC)
└─> [WRITE-TEST](SPEC)
    └─> Gate: Spec complete, POC successful, plans ready

[IMPLEMENT]
├─> [IMPLEMENT] code changes
├─> [CONFIGURE] environment
├─> [INTEGRATE] components
├─> [TEST] during implementation
├─> [REFACTOR] as needed
└─> [COMMIT] small, frequent
    └─> Gate: All code complete, tests pass

[REFINE]
├─> [REVIEW] self-review
├─> [VERIFY] against spec/rules
├─> [TEST] regression testing
├─> [CRITIQUE] devil's advocate
├─> [RECONCILE] pragmatic adjustments
├─> [FIX] found issues
└─> [OPTIMIZE] if needed
    └─> Gate: All issues resolved, verification passed

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

### Problem-Based Workflow (HOTFIX)

```
[EXPLORE]
├─> [ANALYZE] identify root cause
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

## 9. Document History

**[2026-01-15 18:23]**
- Changed: Renamed from "IPPS Phase Model" to "EDIRD Phase Model"
- Changed: Phase names DISCOVERY → EXPLORE, IMPROVE → REFINE
- Changed: Doc ID prefix PHSE → EDRD
- Added: `[TEST]` verb to REFINE phase for regression testing

**[2026-01-15 18:08]**
- Fixed: Doc ID reference AGEN-IN01 → AGEN-SP01
- Changed: EDRD-IG-04 clarified - verb failures may trigger phase iteration

**[2026-01-15 17:46]**
- Initial specification created from INFO_PROJECT_PHASES_OPTIONS.md
