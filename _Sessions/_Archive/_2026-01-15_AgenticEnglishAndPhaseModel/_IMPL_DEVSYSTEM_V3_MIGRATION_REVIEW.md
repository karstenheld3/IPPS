# REVIEW: DevSystem V3 Migration Plan

**Doc ID**: DSVS-RV02
**Goal**: Review DSVS-IP01 against source specs (AGEN-SP01, EDIRD-SP04) before implementation
**Reviewed**: 2026-01-15 20:39

**Reviews:**
- `_IMPL_DEVSYSTEM_V3_MIGRATION.md [DSVS-IP01]` - Migration plan

**Against:**
- `_SPEC_AGEN_AGENTIC_ENGLISH.md [AGEN-SP01]` - Vocabulary spec
- `_SPEC_EDIRD_PHASE_MODEL_2.md [EDIRD-SP04]` - Phase model spec

## Summary

**Status**: Ready for implementation with minor clarifications

The IMPL plan is well-structured and comprehensive. Most spec requirements are addressed. A few gaps and clarifications identified below.

## Findings

### Compliance Check: Implementation Guarantees

| ID | Requirement | IMPL Coverage | Status |
|----|-------------|---------------|--------|
| IG-01 | Phase names stable (EDIRD) | edird-core.md template | OK |
| IG-02 | Complexity→semver mapping | edird-core.md Core Principles | OK |
| IG-03 | All workflows start with [ASSESS] | Entry Rule section in edird-core.md | OK |
| IG-04 | Gate failures loop within phase | Gate Summaries + skill | OK |
| IG-05 | Workflow type persists | Core Principles section | OK |
| IG-06 | Every verb outcome has handler | NEXT_ACTION.md in skill | OK |
| IG-07 | Small verifiable cycles | edird-core.md + implement.md template | OK |
| IG-08 | PROGRESS.md has full phase plan | Phase Tracking section in devsystem-core.md update | CLARIFY |
| IG-09 | Gate summaries always-on, full in skill | edird-core.md + GATES.md | OK |

### Compliance Check: Functional Requirements

| ID | Requirement | IMPL Coverage | Status |
|----|-------------|---------------|--------|
| FR-01 | 5-phase structure | edird-core.md Phases section | OK |
| FR-02 | Workflow type selection | Core Principles + Entry Rule | OK |
| FR-03 | Complexity/problem assessment | Entry Rule references [ASSESS] | OK |
| FR-04 | Phase gates | Gate Summaries + GATES.md skill | OK |
| FR-05 | Verb-phase mapping | edird-core.md lists verbs per phase | OK |
| FR-06 | Deterministic next action | NEXT_ACTION.md in skill | OK |
| FR-07 | Workflow branching syntax | BRANCHING.md in skill | OK |
| FR-08 | Hybrid workflow support | FLOWS.md includes Section 11 | OK |

## Issues

### RV02-01: IG-08 - Phase Plan Template Missing

**Severity**: Minor
**Location**: IS-04 (devsystem-core.md update)

The Phase Tracking section shows NOTES.md format but does not show PROGRESS.md format. Per IG-08, agent must maintain all 5 phases with status in PROGRESS.md.

**Fix**: Add PROGRESS.md template to IS-04:

```markdown
## PROGRESS.md Phase Plan Template

```markdown
## Phase Plan

- [ ] **EXPLORE** - pending
- [x] **DESIGN** - done
- [ ] **IMPLEMENT** - in_progress
- [ ] **REFINE** - pending
- [ ] **DELIVER** - pending
```

### RV02-02: Session Templates Need Phase Tracking

**Severity**: Minor
**Location**: IS-08 (Skills Migration) - session-management skill

The session-management skill creates NOTES.md, PROGRESS.md, PROBLEMS.md templates. These need to include phase tracking sections per EDIRD-SP04.

**Fix**: IS-08 already mentions "Add phase tracking templates" for session-management skill. Ensure templates include:
- NOTES.md: "Current Phase" section
- PROGRESS.md: "Phase Plan" section with 5 phases

### RV02-03: Workflow Template Missing workflow_type Guidance

**Severity**: Minor
**Location**: IS-07 (New Workflow Template)

The template frontmatter includes `workflow_type: [BUILD|SOLVE]` but not all workflows need this. Phase workflows (explore.md, design.md, etc.) operate within both types.

**Fix**: Make workflow_type optional in template:

```markdown
---
description: [Brief description]
phase: [EXPLORE|DESIGN|IMPLEMENT|REFINE|DELIVER]
workflow_type: [BUILD|SOLVE|BOTH]  # Optional, omit if phase applies to both
---
```

### RV02-04: Missing Verb: [DRAFT] in AGEN-SP01

**Severity**: Info
**Location**: AGEN-SP01 vs EDIRD-SP04

EDIRD-SP04 uses `[DRAFT]` in SOLVE WRITING flow (line 556), but AGEN-SP01 defines it in Documentation category. Consistency is fine - just noting for reference.

**Status**: No action needed

### RV02-05: Test Case Gap - SOLVE DECISION Flow

**Severity**: Minor
**Location**: Section 9 (Test Cases)

Test scenarios cover BUILD (LOW, HIGH) and SOLVE (RESEARCH). Missing explicit test for SOLVE DECISION flow from EDIRD-SP04 Section 10.

**Fix**: Add test case:

```markdown
- **DSVS-IP01-TC-13**: Run SOLVE DECISION workflow -> ok=true, [CONCLUDE] and [RECOMMEND] executed, decision documented
```

### RV02-06: Edge Case - Workflow Type Switch Mid-Session

**Severity**: Minor
**Location**: Section 10 (Edge Cases)

EDIRD-SP04 Section 11 describes workflow switching with [ACTOR] confirmation. This is not covered in edge cases.

**Fix**: Add edge case:

```markdown
### DSVS-IP01-EC-04: Workflow Type Switch

If assessment changes during EXPLORE:
- [CONSULT] with [ACTOR]: "This looks more like a [BUILD|SOLVE] workflow. Confirm?"
- If confirmed, switch workflow_type and restart with appropriate verbs
- Document switch in NOTES.md
```

## Recommendations

### R-01: Start with Phase 1-2 Before Pilot

The plan correctly identifies `implement.md` as pilot. Recommend completing Phase 1 (Setup) and Phase 2 (Rules: agentic-english.md, edird-core.md) before pilot, since pilot workflow references these rules.

### R-02: Create Skill Before Workflow

IS-03c (edird-phase-model skill) should complete before IS-05 (implement.md pilot), since implement.md may reference @edird-phase-model for stuck detection.

### R-03: Verification Before Each Batch

Add explicit verification step after each workflow batch (Batches 1-7) before proceeding to next. This catches regressions early.

## Implementation Order (Adjusted)

Based on dependencies:

1. **IS-01, IS-02**: Create V3 folder, copy base files
2. **IS-03**: Create agentic-english.md rule
3. **IS-03b**: Create edird-core.md rule
4. **IS-03c**: Create edird-phase-model skill (4 files)
5. **IS-04**: Update devsystem-core.md
6. **IS-05**: Restructure implement.md (pilot)
7. **IS-06**: Test pilot workflow
8. **Batches 1-7**: Workflow migration (with verification after each)
9. **IS-08**: Skills migration
10. **IS-09, IS-10**: Testing
11. **IS-11 through IS-14**: Deployment

## Decision Required

**Q1**: Should we implement all issues (RV02-01 through RV02-06) before starting, or address during implementation?

**Recommendation**: Fix RV02-01 and RV02-02 now (template completeness). Others can be addressed as we encounter them.

## Document History

**[2026-01-15 20:39]**
- Initial review completed
- 6 issues identified (1 info, 5 minor)
- 3 recommendations made
- Implementation order adjusted for dependencies
