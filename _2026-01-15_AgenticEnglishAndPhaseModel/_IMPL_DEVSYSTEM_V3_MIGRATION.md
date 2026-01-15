<DevSystem MarkdownTablesAllowed=true />

# IMPL: DevSystem V3 Migration Plan

**Doc ID**: DSVS-IP01
**Goal**: Step-by-step migration from DevSystemV2.1 to V3 with EDIRD phase model and Agentic English
**Timeline**: Created 2026-01-15

**Target files**:
- `DevSystemV3/rules/*.md` (NEW folder)
- `DevSystemV3/workflows/*.md` (NEW folder)
- `DevSystemV3/skills/*/SKILL.md` (UPDATE)
- `.windsurf/` (DEPLOY target)

**Depends on:**
- `_INFO_DEVSYSTEM_V3_MIGRATION.md [DSVS-IN01]` for challenges analysis
- `_SPEC_AGEN_AGENTIC_ENGLISH.md [AGEN-SP01]` for vocabulary
- `_SPEC_EDIRD_PHASE_MODEL_2.md [EDIRD-SP04]` for phase model

## MUST-NOT-FORGET

- Hybrid migration: Create V3 folder, test, then deploy
- Rules first (low risk), then workflows (high risk), then skills
- Pilot with `implement.md` before batch migration
- Keep DevSystemV2.1 intact until all linked repos migrated
- Add `agentic-english.md` as always-on rule (AGEN-SP01 content)
- Phase tracking: NOTES.md has current phase, PROGRESS.md has full phase plan

## Table of Contents

- [1. Migration Overview](#1-migration-overview)
- [2. Phase 1: Setup](#2-phase-1-setup)
- [3. Phase 2: Rules Migration](#3-phase-2-rules-migration)
- [4. Phase 3: Pilot Workflow](#4-phase-3-pilot-workflow)
- [5. Phase 4: Workflow Migration](#5-phase-4-workflow-migration)
- [6. Phase 5: Skills Migration](#6-phase-5-skills-migration)
- [7. Phase 6: Testing](#7-phase-6-testing)
- [8. Phase 7: Deployment](#8-phase-7-deployment)
- [9. Test Cases](#9-test-cases)
- [10. Verification Checklist](#10-verification-checklist)

## 1. Migration Overview

### File Mapping

**V2.1 → V3 transformation types:**
- **KEEP**: Copy unchanged
- **UPDATE**: Update terminology/syntax
- **RESTRUCTURE**: Major rewrite with EDIRD phases
- **NEW**: Create from scratch
- **MERGE**: Combine multiple files
- **DEPRECATE**: Remove (document reason)

## 2. Phase 1: Setup

### DSVS-IP01-IS-01: Create DevSystemV3 Folder Structure

```
[WORKSPACE_FOLDER]/DevSystemV3/
├── rules/
│   ├── agentic-english.md      [NEW] - Verb syntax + list (~150 lines)
│   ├── edird-core.md           [NEW] - Phase summary + gates principle (~80 lines)
│   ├── core-conventions.md     [KEEP]
│   ├── devsystem-core.md       [UPDATE]
│   ├── devsystem-ids.md        [KEEP]
│   └── workspace-rules.md      [KEEP]
├── skills/
│   ├── edird-phase-model/      [NEW] - Progressive disclosure
│   │   ├── SKILL.md            - When to invoke, quick reference
│   │   ├── GATES.md            - Full gate checklists per phase
│   │   ├── FLOWS.md            - BUILD/SOLVE workflow sequences
│   │   └── NEXT_ACTION.md      - Deterministic logic for autonomous mode
│   └── (copy all from V2.1)    [UPDATE]
└── workflows/
    └── (restructure per Phase 4)
```

**Progressive Disclosure Strategy:**
- **Tier 1 (always-on rules)**: ~230 lines total - agentic-english.md + edird-core.md
- **Tier 2 (on-demand skill)**: ~600 lines - Full EDIRD model, invoked for [PLAN], [DECOMPOSE], or debugging

### DSVS-IP01-IS-02: Copy Base Files

```powershell
# Create V3 folder
New-Item -Path "DevSystemV3" -ItemType Directory -Force
New-Item -Path "DevSystemV3/rules" -ItemType Directory -Force
New-Item -Path "DevSystemV3/skills" -ItemType Directory -Force
New-Item -Path "DevSystemV3/workflows" -ItemType Directory -Force

# Copy rules (will update later)
Copy-Item -Path "DevSystemV2.1/rules/*" -Destination "DevSystemV3/rules/" -Recurse

# Copy skills (will update later)
Copy-Item -Path "DevSystemV2.1/skills/*" -Destination "DevSystemV3/skills/" -Recurse

# Copy workflows (will restructure later)
Copy-Item -Path "DevSystemV2.1/workflows/*" -Destination "DevSystemV3/workflows/" -Recurse
```

## 3. Phase 2: Rules Migration

### DSVS-IP01-IS-03: Create agentic-english.md Rule

Create `DevSystemV3/rules/agentic-english.md` from AGEN-SP01 (~150 lines):

**Content:**
- Extract core syntax rules from AGEN-SP01
- Include verb reference (one-line each)
- Include placeholder reference
- Include context states reference
- Mark as `trigger: always_on`

**Sections to include:**
- Syntax (instruction tokens vs context states)
- Verb categories (one-line each)
- Placeholders
- Labels
- Context states

**Omit from rule:**
- Document history
- Long examples
- Cross-references to other specs

### DSVS-IP01-IS-03b: Create edird-core.md Rule

Create `DevSystemV3/rules/edird-core.md` (~80 lines):

**Content:**
- 5 phases with one-line purpose each
- Gate principle (checklist before phase transition)
- Retry limits: LOW=infinite, MEDIUM/HIGH=max 5 per phase then [CONSULT]
- Small cycles principle ([IMPLEMENT]→[TEST]→[FIX]→green→next)
- Reference to @edird-phase-model skill for full model
- Mark as `trigger: always_on`

**Template:**
```markdown
---
trigger: always_on
---

# EDIRD Phase Model (Core)

For full model with gates, flows, and next-action logic: invoke @edird-phase-model

## Phases

- **EXPLORE** - Understand before acting. [RESEARCH], [ANALYZE], [ASSESS], [SCOPE]
- **DESIGN** - Plan before executing. [PLAN], [DECOMPOSE], [WRITE-SPEC], [PROVE]
- **IMPLEMENT** - Execute the plan. [IMPLEMENT], [TEST], [FIX], [COMMIT]
- **REFINE** - Improve quality. [REVIEW], [VERIFY], [CRITIQUE], [RECONCILE]
- **DELIVER** - Complete and hand off. [VALIDATE], [MERGE], [DEPLOY], [CLOSE]

## Core Principles

- **Gates**: Checklist must pass before phase transition. Gate failures loop within phase.
- **Small cycles**: [IMPLEMENT]→[TEST]→[FIX]→green→next. Never large untestable steps
- **Retry limits**: COMPLEXITY-LOW: infinite retries (until user stops). COMPLEXITY-MEDIUM/HIGH: max 5 attempts per phase, then [CONSULT]
- **Verb outcomes**: -OK (proceed), -FAIL (handle per verb), -SKIP (intentional)
- **Workflow type**: BUILD (code) or SOLVE (knowledge). Determined in EXPLORE, persists unless switched with [ACTOR] confirmation
- **Complexity**: LOW=patch, MEDIUM=minor, HIGH=major (maps to semantic versioning)

## Entry Rule

All workflows start in EXPLORE with [ASSESS] to determine workflow type and complexity/problem-type.

## Gate Summaries

- **EXPLORE→DESIGN**: Problem understood, scope defined, workflow type determined
- **DESIGN→IMPLEMENT**: SPEC, IMPL, TEST docs exist, plan decomposed, risks proven
- **IMPLEMENT→REFINE**: All steps implemented, tests pass, no TODO/FIXME
- **REFINE→DELIVER**: Reviews complete, issues reconciled, ready to merge
- **DELIVER→DONE**: Validated, merged, deployed (if applicable), session closed

## Phase Tracking

- Agent updates NOTES.md with current phase on transition. User adds notes manually.
- Agent maintains full phase plan in PROGRESS.md (phases with status: pending/in_progress/done)
```

### DSVS-IP01-IS-03c: Create edird-phase-model Skill

Create `DevSystemV3/skills/edird-phase-model/` folder with 4 files:

**SKILL.md** (~50 lines):
```markdown
---
name: edird-phase-model
description: Apply when doing [PLAN], [DECOMPOSE], or debugging workflow issues
---

# EDIRD Phase Model (Full)

## When to Invoke

- [PLAN] - Read FLOWS.md for workflow type (BUILD/SOLVE)
- [DECOMPOSE] - Read GATES.md for gate requirements
- Stuck or debugging - Read NEXT_ACTION.md for deterministic logic

## Quick Reference

Workflow types: BUILD (code output) | SOLVE (knowledge/decision output)
Assessment: COMPLEXITY-LOW/MEDIUM/HIGH | PROBLEM-TYPE (RESEARCH/ANALYSIS/etc.)

## Files

- GATES.md - Full gate checklists for each phase transition
- FLOWS.md - Verb sequences for BUILD and SOLVE workflows, hybrid situations
- NEXT_ACTION.md - Deterministic next-action logic for autonomous mode
- BRANCHING.md - Context state branching syntax
```

**GATES.md** (~150 lines): Extract Section 7 from EDIRD-SP04

**FLOWS.md** (~200 lines): Extract Section 10 + Section 11 (Hybrid Situations) from EDIRD-SP04

**NEXT_ACTION.md** (~150 lines): Extract Section 9 from EDIRD-SP04

**BRANCHING.md** (~50 lines): Extract branching syntax from AGEN-SP01
- Context states (no brackets) in condition headers
- Format: `## For CONTEXT-STATE` followed by `[VERB]` instructions

### DSVS-IP01-IS-04: Update devsystem-core.md

**Changes:**
- Add EDIRD phase model reference
- Update Workflow Reference section with phase categories
- Add "Phase Tracking" section for sessions
- Update Agent Instructions with EDIRD flow

**Add to Workflow Reference:**
```markdown
### Phase Workflows

- **EXPLORE**: `/explore` - [RESEARCH], [ANALYZE], [ASSESS], [SCOPE]
- **DESIGN**: `/design` - [PLAN], [WRITE-SPEC], [WRITE-IMPL], [WRITE-TEST], [PROVE]
- **IMPLEMENT**: `/implement` - [IMPLEMENT], [TEST], [FIX], [COMMIT]
- **REFINE**: `/refine` - [REVIEW], [VERIFY], [CRITIQUE], [RECONCILE]
- **DELIVER**: `/deliver` - [VALIDATE], [MERGE], [DEPLOY], [CLOSE], [ARCHIVE]
```

**Add Phase Tracking section:**
```markdown
## Phase Tracking

Sessions track current phase in NOTES.md:

```markdown
## Current Phase

**Phase**: DESIGN
**Last verb**: [WRITE-SPEC]-OK
**Gate status**: 3/5 items checked
```

Sessions track full phase plan in PROGRESS.md:

```markdown
## Phase Plan

- [ ] **EXPLORE** - pending
- [x] **DESIGN** - done
- [ ] **IMPLEMENT** - in_progress
- [ ] **REFINE** - pending
- [ ] **DELIVER** - pending
```

## 4. Phase 3: Pilot Workflow

### DSVS-IP01-IS-05: Restructure implement.md (Pilot)

**Current structure:**
- Informal instructions
- Skills reference
- Rules list

**V3 structure:**
```markdown
---
description: Execute implementation from IMPL plan
phase: IMPLEMENT
---

# Implement Workflow

## Required Skills

- @coding-conventions for coding style
- @write-documents for tracking

## Phase: IMPLEMENT

**Entry gate:** DESIGN→IMPLEMENT passed (IMPL plan exists)

### Verb Sequence

1. For each step in IMPL plan:
   - [IMPLEMENT] code changes
   - [TEST] verify step works
   - [FIX] if tests fail (per retry limits)
   - [COMMIT] when green
2. [VERIFY] against IMPL plan

### Gate Check: IMPLEMENT→REFINE

- [ ] All steps from IMPL plan implemented
- [ ] Tests pass
- [ ] No TODO/FIXME left unaddressed
- [ ] Progress committed

**Pass**: Run `/refine` | **Fail**: Continue [IMPLEMENT]

## Stuck Detection

If 3 consecutive [FIX] attempts fail:
1. [CONSULT] with [ACTOR]
2. Document in PROBLEMS.md
3. Either get guidance or [DEFER] and continue
```

### DSVS-IP01-IS-06: Test Pilot Workflow

**Test scenarios:**
1. Run `/implement` on simple task (COMPLEXITY-LOW)
2. Run `/implement` on multi-file task (COMPLEXITY-MEDIUM)
3. Verify gate checks work
4. Verify stuck detection triggers after 3 failures
5. Verify [COMMIT] creates proper commits

**Success criteria:**
- Agent follows verb sequence
- Gate checks prevent premature phase transition
- Stuck detection works
- Output matches EDIRD-SP04 expectations

## 5. Phase 4: Workflow Migration

### Batch 1: Entry Workflows

| File | Action | Notes |
|------|--------|-------|
| `next.md` | UPDATE | Add [ASSESS] for workflow type |
| `prime.md` | KEEP | No phase structure needed |

### Batch 2: Phase Workflows (NEW)

| File | Action | Content |
|------|--------|---------|
| `explore.md` | NEW | EXPLORE phase verbs, gate |
| `design.md` | NEW | DESIGN phase verbs, gate |
| `refine.md` | NEW | REFINE phase verbs, gate |
| `deliver.md` | NEW | DELIVER phase verbs, gate |

### Batch 3: Existing Workflows (RESTRUCTURE)

| File | Action | Phase Mapping |
|------|--------|---------------|
| `implement.md` | RESTRUCTURE | IMPLEMENT phase (pilot) |
| `go-autonomous.md` | RESTRUCTURE | Full EDIRD cycle wrapper |
| `go-research.md` | RESTRUCTURE | SOLVE workflow (RESEARCH type) |
| `verify.md` | RESTRUCTURE | [VERIFY] verb implementation |
| `commit.md` | UPDATE | [COMMIT] verb implementation |

### Batch 4: Session Workflows (UPDATE)

| File | Action | Changes |
|------|--------|---------|
| `session-init.md` | UPDATE | Add phase tracking template |
| `session-save.md` | UPDATE | Save current phase state |
| `session-resume.md` | UPDATE | Restore phase state |
| `session-close.md` | UPDATE | Ensure DELIVER phase complete |
| `session-archive.md` | KEEP | No phase logic needed |

### Batch 5: Document Workflows (UPDATE)

| File | Action | Phase |
|------|--------|-------|
| `write-spec.md` | UPDATE | DESIGN phase, [WRITE-SPEC] verb |
| `write-impl-plan.md` | UPDATE | DESIGN phase, [WRITE-IMPL] verb |
| `write-test-plan.md` | UPDATE | DESIGN phase, [WRITE-TEST] verb |

### Batch 6: Review Workflows (RESTRUCTURE)

| File | Action | Verb Mapping |
|------|--------|--------------|
| `review-devilsadvocate.md` | RESTRUCTURE | [CRITIQUE] implementation |
| `review-pragmaticprogrammer.md` | RESTRUCTURE | [RECONCILE] implementation |

### Batch 7: Utility Workflows (UPDATE)

| File | Action | Notes |
|------|--------|-------|
| `rename.md` | UPDATE | Add [VERIFY] step |
| `sync.md` | UPDATE | Add [VERIFY] step |
| `setup-pdftools.md` | KEEP | No phase structure needed |

### DSVS-IP01-IS-07: New Workflow Template

Use this template for all restructured workflows:

```markdown
---
description: [Brief description]
phase: [EXPLORE|DESIGN|IMPLEMENT|REFINE|DELIVER]
workflow_type: [BUILD|SOLVE]
---

# [Workflow Name]

## Required Skills

- @[skill-name] for [purpose]

## Phase: [PHASE]

**Entry gate:** [Previous phase]→[This phase] passed

### Verb Sequence

1. [VERB] - Description
2. [VERB] - Description
   - On [VERB]-FAIL: [Handler]

### Gate Check: [This phase]→[Next phase]

- [ ] Gate item 1
- [ ] Gate item 2

**Pass**: [Next action] | **Fail**: Continue in [This phase]

## Stuck Detection

If no progress after 3 verb cycles: [CONSULT] with [ACTOR]
```

## 6. Phase 5: Skills Migration

### DSVS-IP01-IS-08: Update All Skills

**Changes for each skill:**

1. **Add verb-skill mapping** to SKILL.md:
```markdown
## Verb Mapping

This skill implements:
- [WRITE-SPEC] - Use SPEC_TEMPLATE.md
- [WRITE-IMPL] - Use IMPL_TEMPLATE.md
```

2. **Update placeholders** - Replace informal paths with `[PLACEHOLDER]` syntax

3. **Add phase context** - Note which phases typically invoke this skill

### Skill-Specific Changes

| Skill | Changes |
|-------|---------|
| `coding-conventions` | Add verb mapping for [IMPLEMENT], [REFACTOR] |
| `git-conventions` | Add verb mapping for [COMMIT], [MERGE] |
| `github` | KEEP (external tool integration) |
| `ms-playwright-mcp` | KEEP (external tool integration) |
| `pdf-tools` | KEEP (external tool integration) |
| `session-management` | Add phase tracking templates: NOTES.md gets "Current Phase" section, PROGRESS.md gets "Phase Plan" section with 5 phases |
| `write-documents` | Add verb mapping for all [WRITE-*] verbs |

## 7. Phase 6: Testing

### DSVS-IP01-IS-09: End-to-End Test Scenarios

**Scenario 1: BUILD COMPLEXITY-LOW**
```
Task: "Add a logging statement to function X"
Expected flow: EXPLORE(brief) → DESIGN(skip) → IMPLEMENT → REFINE(brief) → DELIVER
Verifications:
- [ASSESS] returns COMPLEXITY-LOW
- DESIGN phase skipped or minimal
- [COMMIT] creates single commit
```

**Scenario 2: BUILD COMPLEXITY-HIGH**
```
Task: "Add new authentication system"
Expected flow: Full EDIRD cycle with all gates
Verifications:
- [ASSESS] returns COMPLEXITY-HIGH
- [PROVE] executed for risky parts
- [CRITIQUE] and [RECONCILE] in REFINE phase
- Multiple commits
```

**Scenario 3: SOLVE RESEARCH**
```
Task: "Research best practices for X"
Expected flow: EDIRD with SOLVE verbs
Verifications:
- [ASSESS] returns RESEARCH type
- Output is INFO document, not code
- [CONCLUDE] and [RECOMMEND] in DELIVER
```

**Scenario 4: Session Lifecycle**
```
Task: Start session, do partial work, save, resume, complete
Verifications:
- Phase state saved in NOTES.md
- Resume restores correct phase
- [CLOSE] verifies DELIVER complete
```

### DSVS-IP01-IS-10: Regression Tests

Verify existing functionality still works:
- [ ] `/prime` loads context correctly
- [ ] `/session-init` creates all required files
- [ ] `/verify` runs all checks
- [ ] `/commit` creates proper commit messages
- [ ] Document templates produce valid documents

## 8. Phase 7: Deployment

### DSVS-IP01-IS-11: Deploy to IPPS

```powershell
# Backup current .windsurf
Copy-Item -Path ".windsurf" -Destination ".windsurf.v2.1.backup" -Recurse

# Deploy V3
Remove-Item -Path ".windsurf/*" -Recurse -Force
Copy-Item -Path "DevSystemV3/*" -Destination ".windsurf/" -Recurse
```

### DSVS-IP01-IS-12: Update !NOTES.md

```markdown
Current [DEVSYSTEM]: DevSystemV3
Current [DEVSYSTEM_FOLDER]: [WORKSPACE_FOLDER]\DevSystemV3
```

### DSVS-IP01-IS-13: Deploy to Linked Repos

For each repo in [LINKED_REPOS]:
1. Read repo's !NOTES.md for special instructions
2. Backup existing .windsurf (or .claude)
3. Copy DevSystemV3 content
4. Verify with `/prime`
5. Test with simple task

**Linked repos:**
- e:\Dev\KarstensWorkspace
- e:\Dev\OpenAI-BackendTools
- e:\Dev\PRXL\src
- e:\Dev\SharePoint-GPT-Middleware

### DSVS-IP01-IS-14: Archive DevSystemV2.1

After all repos migrated:
```powershell
Move-Item -Path "DevSystemV2.1" -Destination "_Archive/DevSystemV2.1"
```

## 9. Test Cases

### Category 1: Workflow Execution (4 tests)

- **DSVS-IP01-TC-01**: Run `/implement` on COMPLEXITY-LOW task -> ok=true, single commit created
- **DSVS-IP01-TC-02**: Run `/implement` on COMPLEXITY-MEDIUM task -> ok=true, multiple commits, all tests pass
- **DSVS-IP01-TC-03**: Run `/go-research` -> ok=true, INFO document created with SOLVE flow
- **DSVS-IP01-TC-04**: Run `/verify` on new document -> ok=true, all checks pass

### Category 2: Session Lifecycle (3 tests)

- **DSVS-IP01-TC-05**: `/session-init` creates phase tracking in NOTES.md -> ok=true, "Current Phase" section exists
- **DSVS-IP01-TC-06**: `/session-save` then `/session-resume` -> ok=true, phase state restored
- **DSVS-IP01-TC-07**: `/session-close` with incomplete DELIVER -> ok=false, warning about incomplete phase

### Category 3: Gate and Retry Limits (5 tests)

- **DSVS-IP01-TC-08**: Attempt phase transition with unchecked gate item -> ok=false, remains in current phase
- **DSVS-IP01-TC-09**: COMPLEXITY-MEDIUM with 5 [FIX] failures -> ok=true, [CONSULT] triggered
- **DSVS-IP01-TC-10**: `/implement` without IMPL plan -> ok=false, error message, stays in DESIGN
- **DSVS-IP01-TC-11**: COMPLEXITY-LOW with 10+ retries -> ok=true, continues until user stops
- **DSVS-IP01-TC-12**: [CONSULT] timeout -> graceful degradation, log and wait

## 10. Verification Checklist

### Pre-Migration

- [ ] **DSVS-IP01-VC-01**: AGEN-SP01 and EDIRD-SP04 finalized

### Post-Migration

- [ ] **DSVS-IP01-VC-02**: `/prime` works
- [ ] **DSVS-IP01-VC-03**: `/session-init` creates files with phase tracking
- [ ] **DSVS-IP01-VC-04**: `/implement` follows EDIRD verb sequence
- [ ] **DSVS-IP01-VC-05**: `/verify` passes all checks
- [ ] **DSVS-IP01-VC-06**: Gate checks prevent premature transitions
- [ ] **DSVS-IP01-VC-07**: Retry limits trigger correctly

## Edge Cases

### DSVS-IP01-EC-01: Mixed Version Repos

If a repo has documents using V2.1 syntax:
- V3 workflows should still work
- Log warning but don't fail
- Suggest updating documents

### DSVS-IP01-EC-02: Partial Session State

If session NOTES.md lacks "Current Phase":
- Infer from existing documents (SPEC exists → at least DESIGN)
- Ask [ACTOR] to confirm

### DSVS-IP01-EC-03: Custom Workflows

If repo has custom workflows in .windsurf/workflows/:
- Don't overwrite
- Log warning about potential incompatibility
- User must migrate manually

## Document History

**[2026-01-15 20:41]**
- Fixed: RV02-01 - Added PROGRESS.md phase plan template to IS-04
- Fixed: RV02-02 - Clarified session-management skill phase tracking templates

**[2026-01-15 20:29]**
- Fixed: RV-01 - Added gate summaries to edird-core.md template
- Fixed: RV-04 - Removed [DECOMPOSE] from implement.md template (belongs in DESIGN)
- Fixed: RV-05 - Added phase tracking rule (agent updates, user adds notes)
- Fixed: RV-06 - Updated retry limits (LOW=infinite, MEDIUM/HIGH=5 per phase)
- Removed: Timeline estimate (migration done with agent)

**[2026-01-15 20:17]**
- Fixed: Verified against EDIRD-SP04 spec requirements
- Added: edird-core.md now includes IG-02 (complexity→semver), IG-04 (gate failures), IG-05 (workflow persistence)
- Added: Entry Rule section (IG-03: all workflows start with [ASSESS])
- Added: BRANCHING.md to skill (FR-07: context state branching)
- Changed: FLOWS.md now includes Section 11 (FR-08: hybrid situations)

**[2026-01-15 20:16]**
- Changed: Hybrid EDIRD approach for progressive disclosure
- Added: IS-03b (edird-core.md rule) and IS-03c (edird-phase-model skill)
- Added: Folder structure shows edird-phase-model/ skill with 5 files
- Added: Progressive Disclosure Strategy (Tier 1: ~230 lines, Tier 2: ~600 lines)

**[2026-01-15 20:25]**
- Added: DevSystem tag for Markdown tables
- Added: Timeline field, Target files field
- Added: Test Cases section (TC-01 through TC-09)
- Added: Verification Checklist IDs (VC-01 through VC-12)
- Fixed: TOC updated with new sections

**[2026-01-15 20:20]**
- Initial implementation plan created
- 14 implementation steps defined (IS-01 through IS-14)
- 3 edge cases identified (EC-01 through EC-03)
- Batch migration strategy for workflows
- Test scenarios for all workflow types
