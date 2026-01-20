# Session Critique: STRUT-TRACTFUL-TDID

**Doc ID**: STRUT-RV01
**Reviewed**: 2026-01-20 19:20, Reconciled 2026-01-20 19:30
**Context**: Devil's Advocate review + Pragmatic reconciliation of session outcomes

## MUST-NOT-FORGET (from INITIAL_PROMPT)

- Separation of concerns: STRUT = method/notation, EDIRD = thinking logic, TRACTFUL = document framework, AGEN = language, TDID = cross-referencing
- STRUT and EDIRD are completely independent
- Writing skills implement TRACT and belong to TRACTFUL framework
- `/sync` workflow exists at `DevSystemV3.1/workflows/sync.md`
- STRUT IDs are ephemeral (session-scoped), TDID is permanent (cross-document)

## Specs Under Review

1. **AGEN-SP01** - Agentic English (controlled vocabulary)
2. **STRUT-SP01** - Structured Thinking (tree notation for planning)
3. **TRACT-SP01** - TRACTFUL Document Framework (traceability via documents)
4. **EDIRD-SP05** - Phase Model (BUILD/SOLVE workflow phases)

## Scope Analysis

### AGEN (Agentic English)

**Claimed scope:** Controlled vocabulary for agent-human communication

**Actual content:**
- Verbs (actions)
- Placeholders (substitution tokens)
- Labels (classifications)
- States (conditions for branching)

**Verdict:** Clear scope. AGEN is the language layer.

### STRUT (Structured Thinking)

**Claimed scope:** Tree notation for planning and tracking autonomous agent work

**Actual content:**
- Phase/Step/Deliverable IDs (P1, P1-S1, P1-D1)
- Tree structure with box-drawing
- Checkbox states
- Transitions

**Verdict:** Clear scope. STRUT is the planning notation.

### TRACTFUL (Document Framework)

**Claimed scope:** Document framework for lifecycle traceability

**Actual content:**
- Document types (INFO, SPEC, IMPL, TEST, TASKS, FIXES, FAILS, LEARNINGS, REVIEW)
- TDID system (document and item IDs)
- Traceability rules
- Writing rules (from write-documents skill)
- File naming conventions

**Verdict:** Clear scope. TRACTFUL is the document layer.

### EDIRD (Phase Model)

**Claimed scope:** Unified phase model for BUILD and SOLVE workflows

**Actual content:**
- 5 phases (EXPLORE, DESIGN, IMPLEMENT, REFINE, DELIVER)
- Workflow types (BUILD, SOLVE)
- Verb mapping per phase
- Gates and transitions
- States (complexity, problem types)
- Next-action logic

**Verdict:** Clear scope. EDIRD is the workflow orchestration layer.

## Critical Issues

### CRIT-01: ID System Overlap (STRUT vs TRACTFUL)

**Problem:** Two ID systems exist:
- STRUT uses: `P1`, `P1-S1`, `P1-D1` (phase/step/deliverable)
- TRACTFUL uses: `TOPIC-TYPE-NN` (document/item IDs via TDID)

**Status:** ✅ DISMISSED - Not a problem

**Reconciliation:** User confirmed these are intentionally separate:
- STRUT IDs are **ephemeral** and **session-scoped** (temporary execution tracking)
- TDID is **permanent** for cross-document referencing
- They do not overlap - different purposes, different scopes

**Action:** None needed. This is correct design.

### CRIT-02: States Definition Overlap (AGEN vs EDIRD)

**Problem:** States defined in both AGEN and EDIRD.

**Status:** ✅ DISMISSED - Correct layering

**Reconciliation:** User confirmed:
- AGEN defines **what states exist** (vocabulary)
- EDIRD **uses states** to define conditional behavior

**Action:** None needed. AGEN owns definitions, EDIRD uses them.

### CRIT-03: Verb Ownership (AGEN vs EDIRD)

**Problem:** Both specs discuss verbs.

**Status:** ✅ DISMISSED - Correct layering

**Reconciliation:** User confirmed:
- AGEN defines verbs (vocabulary)
- EDIRD uses AGEN verbs (orchestration)

**Action:** None needed. Correct separation of concerns.

## High Priority Issues

### HIGH-01: STRUT Phases vs EDIRD Phases

**Problem:** STRUT examples use EDIRD phase names (EXPLORE, DESIGN, IMPLEMENT).

**Status:** ✅ DISMISSED - Correct independence

**Reconciliation:** User confirmed:
- STRUT is a way to keep track of long running session phases
- STRUT does NOT depend on EDIRD - they are completely independent
- Examples happen to use EDIRD phases but STRUT works with any phase model

**Action:** Clarify in STRUT-SP01 that examples use EDIRD phases for illustration only. STRUT is phase-model agnostic.

### HIGH-02: TRACTFUL Writing Rules Duplication

**Problem:** TRACTFUL section 8 duplicates write-documents skill content.

**Status:** ⚠️ CONFIRMED - Needs refactoring

**Reconciliation:** User confirmed:
- Writing skills implement TRACT and belong to TRACTFUL framework
- Skills are independent of STRUT and EDIRD
- TRACTFUL owns write-documents skill

**Action:** 
- TRACTFUL spec defines requirements (FR/IG/AC)
- write-documents skill provides implementation (templates, rules)
- Remove duplication: TRACTFUL references skill, skill implements TRACTFUL

### HIGH-03: Missing STRUT-TRACTFUL Integration

**Problem:** No clear statement on how STRUT plans relate to TRACTFUL documents.

**Status:** ✅ DISMISSED - Correct separation

**Reconciliation:** User confirmed:
- STRUT is notation (how to write plans)
- TRACTFUL is the container (where plans live)
- STRUT is used in sessions, defined in DevSystem rules, not in EDIRD

**Action:** Add one-line clarification to both specs:
- STRUT-SP01: "STRUT plans are embedded in TRACTFUL documents (NOTES.md, PROGRESS.md)"
- TRACT-SP01: "STRUT notation may be used within planning sections"

## Medium Priority Issues

### MED-01: TDID in TRACTFUL vs ID-REGISTRY

**Problem:** TDID is defined in TRACTFUL spec section 4, but ID-REGISTRY.md also describes IDs.

**Status:** ✅ DISMISSED - Correct layering

**Reconciliation:** 
- TRACTFUL defines TDID **system** (rules, formats)
- ID-REGISTRY lists **registered values** (actual TOPICs, IDs in use)

**Action:** None needed. This is correct separation.

### MED-02: Acceptance Criteria Not Testable

**Problem:** TRACT-AC-03 requires `/sync` workflow which doesn't exist.

**Status:** ✅ DISMISSED - Already exists

**Reconciliation:** User confirmed `/sync` workflow exists at `DevSystemV3.1/workflows/sync.md`

**Action:** None needed.

### MED-03: EDIRD States Section Name

**Problem:** EDIRD section 12 is called "States" but includes workflow types, complexity levels, and problem types.

**Status:** ⚠️ CONFIRMED - Minor improvement

**Action:** Consider renaming to "Context Values" for clarity. Low priority.

## Questions Resolved

1. **Should STRUT depend on EDIRD?** → No. Completely independent.
2. **Should Writing Rules move to skill?** → Yes. Skills implement TRACT, belong to TRACTFUL.
3. **Where is `/sync` workflow?** → `DevSystemV3.1/workflows/sync.md`
4. **Are STRUT IDs related to TDID?** → No. STRUT IDs are ephemeral/session-scoped.

## Summary

**Overall assessment:** The specs are well-designed with clear scope boundaries. Most findings were dismissed as correct design after user reconciliation.

**Confirmed Layering (independent, not stacked):**
```
AGEN        - Language layer (vocabulary: verbs, states, placeholders)
TRACTFUL    - Document layer (templates, TDID, traceability, owns write-documents skill)
STRUT       - Planning layer (session notation, ephemeral IDs)
EDIRD       - Orchestration layer (phases, gates, flow - uses AGEN verbs)
```

**Key Clarifications:**
- STRUT and EDIRD are completely independent
- STRUT IDs are ephemeral (session-scoped), TDID is permanent
- Writing skills belong to TRACTFUL, not EDIRD
- AGEN defines vocabulary, EDIRD uses it

## Pragmatic Review Summary

**Findings Reviewed**: 9
**Confirmed**: 2 (HIGH-02, MED-03)
**Dismissed**: 7 (CRIT-01, CRIT-02, CRIT-03, HIGH-01, HIGH-03, MED-01, MED-02)
**Needs Discussion**: 0

**Recommended Actions** (in priority order):

1. **Refactor TRACTFUL section 8** - Move implementation details to write-documents skill, keep only FR/IG/AC in spec
   - Effort: Medium
   - Impact: High (removes duplication, clarifies ownership)

2. **Add STRUT-TRACTFUL clarification** - One line in each spec about how they relate
   - Effort: Low
   - Impact: Medium (prevents future confusion)

3. **Rename EDIRD section 12** - "States" → "Context Values" (optional)
   - Effort: Low
   - Impact: Low (minor clarity improvement)

**Next Step**: Implement actions 1-2 or defer to next session.

## Document History

**[2026-01-20 19:30]**
- Reconciled: Applied user clarifications to all findings
- Dismissed: 7 findings as correct design
- Confirmed: 2 findings need action (HIGH-02, MED-03)
- Added: Pragmatic Review Summary

**[2026-01-20 19:20]**
- Initial critique created
