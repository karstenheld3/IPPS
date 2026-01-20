# Session Critique: STRUT-TRACTFUL-TDID

**Doc ID**: STRUT-RV01
**Reviewed**: 2026-01-20 19:20
**Context**: Devil's Advocate review of session outcomes for modularity and scope clarity

## MUST-NOT-FORGET

- Each spec must have clear scope and not interfere with other specs
- Specs can build on each other but must not diffuse clarity
- No ambiguities between specs
- Clear modularity required

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

**Impact:** Confusion about which ID system to use when.

**Question:** Are these complementary or overlapping?

**Analysis:**
- STRUT IDs are for **plan execution** (ephemeral, per-session)
- TRACTFUL IDs are for **documents and requirements** (persistent, cross-session)
- They operate at different levels and do not conflict

**Recommendation:** Clarify in both specs that:
- STRUT IDs = execution tracking (temporary)
- TDID = document traceability (permanent)

### CRIT-02: States Definition Overlap (AGEN vs EDIRD)

**Problem:** States are defined in both:
- AGEN defines: Syntax for states (no brackets, uppercase)
- EDIRD defines: Actual state values (BUILD, SOLVE, COMPLEXITY-HIGH, etc.)

**Impact:** Unclear where to look for state definitions.

**Question:** Should AGEN define syntax only, or also define states?

**Analysis:**
- AGEN defines the **syntax** for states
- EDIRD defines **workflow-specific** states
- ID-REGISTRY.md lists all states

**Recommendation:** 
- AGEN should define syntax only, reference ID-REGISTRY for values
- EDIRD should define workflow states
- ID-REGISTRY is the authoritative list

### CRIT-03: Verb Ownership (AGEN vs EDIRD)

**Problem:** Both specs discuss verbs:
- AGEN defines all verbs (vocabulary)
- EDIRD maps verbs to phases

**Impact:** Confusion about where to add new verbs.

**Analysis:**
- AGEN owns verb **definitions** (what the verb means)
- EDIRD owns verb **mapping** (when to use the verb)

**Verdict:** This is correct layering. AGEN = definitions, EDIRD = orchestration.

**Recommendation:** Make this explicit in both specs.

## High Priority Issues

### HIGH-01: STRUT Phases vs EDIRD Phases

**Problem:** STRUT examples use EDIRD phase names (EXPLORE, DESIGN, IMPLEMENT).

**Impact:** Coupling between STRUT and EDIRD when STRUT claims to be phase-model agnostic.

**Question:** Is STRUT coupled to EDIRD or not?

**Analysis:** STRUT depends on AGEN for verbs. STRUT examples use EDIRD phases, but STRUT notation could work with any phase model.

**Recommendation:** 
- STRUT-SP01 should clarify: "Examples use EDIRD phases but STRUT works with any phase model"
- Or: STRUT explicitly depends on EDIRD

### HIGH-02: TRACTFUL Writing Rules Duplication

**Problem:** TRACTFUL section 8 duplicates write-documents skill content.

**Impact:** Two sources of truth for writing rules.

**Analysis:** TRACTFUL is the spec, write-documents skill is the implementation. The spec should define requirements, not copy implementation details.

**Recommendation:** 
- TRACTFUL should reference write-documents skill, not duplicate it
- Keep FR/IG/AC in TRACTFUL, move implementation details to skill

### HIGH-03: Missing STRUT-TRACTFUL Integration

**Problem:** No clear statement on how STRUT plans relate to TRACTFUL documents.

**Impact:** Unclear how planning (STRUT) connects to documentation (TRACTFUL).

**Question:** Does a STRUT plan live in a TRACTFUL document?

**Recommendation:** Add clarification:
- STRUT plans can be embedded in NOTES.md or PROGRESS.md
- STRUT is notation, TRACTFUL is the container

## Medium Priority Issues

### MED-01: TDID in TRACTFUL vs ID-REGISTRY

**Problem:** TDID is defined in TRACTFUL spec section 4, but ID-REGISTRY.md also describes IDs.

**Impact:** Unclear which is authoritative.

**Recommendation:**
- TRACTFUL defines TDID **system** (rules, formats)
- ID-REGISTRY lists **registered values** (actual TOPICs, IDs in use)

### MED-02: Acceptance Criteria Not Testable

**Problem:** TRACT-AC-03 requires `/sync` workflow which doesn't exist.

**Impact:** Cannot verify acceptance criteria.

**Recommendation:** Either create `/sync` workflow or defer AC-03.

### MED-03: EDIRD States Section Name

**Problem:** EDIRD section 12 is called "States" but includes workflow types, complexity levels, and problem types - not just states.

**Recommendation:** Rename to "Context Values" or keep as "States" with subsections.

## Questions That Need Answers

1. Should STRUT explicitly depend on EDIRD, or remain phase-model agnostic?
2. Should TRACTFUL Writing Rules section be moved entirely to write-documents skill?
3. Where should `/sync` workflow be defined?
4. Is the STRUT ID system (P1-S1) related to TDID or completely separate?

## Summary

**Overall assessment:** The specs are reasonably modular with clear scope boundaries. The main issues are:

1. **ID systems** - Two systems exist (STRUT and TDID) but they serve different purposes
2. **State definitions** - Split between AGEN (syntax) and EDIRD (values) is correct but needs clarification
3. **Writing rules duplication** - TRACTFUL duplicates skill content

**Layering (bottom to top):**
```
AGEN        - Language layer (vocabulary)
TRACTFUL    - Document layer (templates, IDs, traceability)
STRUT       - Planning layer (execution notation)
EDIRD       - Orchestration layer (phases, gates, flow)
```

Each layer builds on lower layers without circular dependencies.

## Recommendations

1. Add explicit clarification about STRUT IDs vs TDID to both specs
2. Move Writing Rules details from TRACTFUL to write-documents skill, keep only FR/IG/AC
3. Clarify STRUT's relationship to EDIRD (uses examples but works with any phase model)
4. Add "Relationship to Other Specs" section to each spec

## Document History

**[2026-01-20 19:20]**
- Initial critique created
