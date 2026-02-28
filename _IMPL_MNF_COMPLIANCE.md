# IMPL: MNF Compliance for Workflows and Skills

**Doc ID**: MNF-IP01
**Feature**: mnf-global-compliance
**Goal**: Add MUST-NOT-FORGET sections to all workflows and skills that call other workflows
**Timeline**: Created 2026-02-28, Updated 0 times

**Target files**:
- 14 workflow files (MODIFY)
- 4 skill files (MODIFY)

**Depends on:**
- `_INFO_MNF_TECHNIQUE.md [MNF-IN01]` for MNF technique definition

## MUST-NOT-FORGET

- MNF section goes after Required Skills, before Step 1
- MNF items must list all called workflows
- Add verification step at end: "Review each MNF item above and confirm compliance"
- Sync all changes to `.windsurf/` after editing `DevSystemV3.3/`
- **PRESERVE existing MNF items** - merge new items with existing, never replace entire section

## Table of Contents

1. [File Structure](#1-file-structure)
2. [MNF Pattern](#2-mnf-pattern)
3. [Implementation Steps - HIGH Priority](#3-implementation-steps---high-priority)
4. [Implementation Steps - MEDIUM Priority](#4-implementation-steps---medium-priority)
5. [Implementation Steps - LOW Priority](#5-implementation-steps---low-priority)
6. [Implementation Steps - Skills](#6-implementation-steps---skills)
7. [Verification Checklist](#7-verification-checklist)
8. [Document History](#8-document-history)

## 1. File Structure

```
DevSystemV3.3/
├── workflows/
│   ├── build.md              [MODIFY] - HIGH
│   ├── solve.md              [MODIFY] - HIGH
│   ├── implement.md          [MODIFY] - HIGH
│   ├── continue.md           [MODIFY] - HIGH
│   ├── learn.md              [MODIFY] - MEDIUM
│   ├── fail.md               [MODIFY] - MEDIUM
│   ├── transcribe.md         [MODIFY] - MEDIUM
│   ├── session-finalize.md   [MODIFY] - MEDIUM
│   ├── write-spec.md         [MODIFY] - LOW
│   ├── write-impl-plan.md    [MODIFY] - LOW
│   ├── write-test-plan.md    [MODIFY] - LOW
│   ├── write-info.md         [MODIFY] - LOW
│   ├── write-strut.md        [MODIFY] - LOW
│   └── write-tasks-plan.md   [MODIFY] - LOW
└── skills/
    ├── edird-phase-planning/
    │   └── SKILL.md          [MODIFY] - HIGH
    └── deep-research/
        ├── RESEARCH_STRATEGY_MEPI.md  [MODIFY] - MEDIUM
        ├── RESEARCH_STRATEGY_MCPI.md  [MODIFY] - MEDIUM
        └── DOMAIN_DEFAULT.md          [MODIFY] - MEDIUM
```

## 2. MNF Pattern

Standard pattern for workflows calling other workflows:

```markdown
## MUST-NOT-FORGET

- Run `/workflow-name` [when/why]
- Run `/other-workflow` [when/why]

... steps ...

## Step N: Verify MUST-NOT-FORGET

Review each MNF item above and confirm compliance.
```

### Merge Rules

When file already has MNF section:
1. Read existing MNF items
2. Add new workflow-related items
3. Keep all existing items intact
4. Do NOT replace the entire section

## 3. Implementation Steps - HIGH Priority

### MNF-IP01-IS-01: build.md

**Location**: `DevSystemV3.3/workflows/build.md` after Required Skills

**Action**: Add MNF section

**Content**:
```markdown
## MUST-NOT-FORGET

- Run `/session-new` at workflow start
- Run `/session-finalize` when done
- Follow @edird-phase-planning gates between phases
```

**Add at end**: Step for MNF verification

### MNF-IP01-IS-02: solve.md

**Location**: `DevSystemV3.3/workflows/solve.md` after Required Skills

**Action**: Add MNF section

**Content**:
```markdown
## MUST-NOT-FORGET

- Run `/session-new` at workflow start
- Run `/session-finalize` when done
- Follow @edird-phase-planning gates between phases
```

**Add at end**: Step for MNF verification

### MNF-IP01-IS-03: implement.md

**Location**: `DevSystemV3.3/workflows/implement.md` after Required Skills

**Action**: Add MNF section

**Content**:
```markdown
## MUST-NOT-FORGET

- Run `/write-spec` if only INFO exists
- Run `/write-impl-plan` if only SPEC exists
- Run `/write-test-plan` if only IMPL exists
- Run `/verify` after implementation complete
- Run `/refine` after IMPLEMENT gate passes
```

**Add at end**: Step for MNF verification

### MNF-IP01-IS-04: continue.md

**Location**: `DevSystemV3.3/workflows/continue.md` after Required Skills

**Action**: Add MNF section

**Content**:
```markdown
## MUST-NOT-FORGET

- Execute queued workflows in sequence
- Session lifecycle workflows (`/session-finalize`, `/session-archive`) require user confirmation
- Remove workflows from sequence after completion
```

**Add at end**: Step for MNF verification

## 4. Implementation Steps - MEDIUM Priority

### MNF-IP01-IS-05: learn.md

**Location**: `DevSystemV3.3/workflows/learn.md` after Required Skills

**Action**: Add MNF section

**Content**:
```markdown
## MUST-NOT-FORGET

- Run `/fail` first in discovery mode (no args)
- Session entries sync to workspace on `/session-finalize`
```

### MNF-IP01-IS-06: fail.md

**Location**: `DevSystemV3.3/workflows/fail.md` after Trigger section

**Action**: Add MNF section

**Content**:
```markdown
## MUST-NOT-FORGET

- Suggest `/learn` after problem is resolved
- Session entries sync to workspace on `/session-finalize`
```

### MNF-IP01-IS-07: transcribe.md

**Location**: `DevSystemV3.3/workflows/transcribe.md` after Required Skills

**Action**: Add MNF section

**Content**:
```markdown
## MUST-NOT-FORGET

- Run `/verify` after transcription complete
- Keep source images for verification
```

### MNF-IP01-IS-08: session-finalize.md

**Location**: `DevSystemV3.3/workflows/session-finalize.md` after Required Skills

**Action**: Add MNF section

**Content**:
```markdown
## MUST-NOT-FORGET

- Sync session PROBLEMS.md to project
- Suggest `/session-archive` when ready (do NOT auto-run)
```

## 5. Implementation Steps - LOW Priority

### MNF-IP01-IS-09: write-spec.md

**Location**: `DevSystemV3.3/workflows/write-spec.md` after Required Skills

**Action**: Add MNF section

**Content**:
```markdown
## MUST-NOT-FORGET

- Run `/verify` after spec complete
```

### MNF-IP01-IS-10: write-impl-plan.md

**Location**: `DevSystemV3.3/workflows/write-impl-plan.md` after Required Skills

**Action**: Add MNF section

**Content**:
```markdown
## MUST-NOT-FORGET

- Run `/verify` after plan complete
```

### MNF-IP01-IS-11: write-test-plan.md

**Location**: `DevSystemV3.3/workflows/write-test-plan.md` after Required Skills

**Action**: Add MNF section

**Content**:
```markdown
## MUST-NOT-FORGET

- Run `/verify` after plan complete
```

### MNF-IP01-IS-12: write-info.md

**Location**: `DevSystemV3.3/workflows/write-info.md` after Required Skills

**Action**: Add MNF section

**Content**:
```markdown
## MUST-NOT-FORGET

- Run `/verify` after document complete
```

### MNF-IP01-IS-13: write-strut.md

**Location**: `DevSystemV3.3/workflows/write-strut.md` after Required Skills

**Action**: Add MNF section

**Content**:
```markdown
## MUST-NOT-FORGET

- Run `/verify` to validate STRUT structure
```

### MNF-IP01-IS-14: write-tasks-plan.md

**Location**: `DevSystemV3.3/workflows/write-tasks-plan.md` after Required Skills

**Action**: Add MNF section

**Content**:
```markdown
## MUST-NOT-FORGET

- Run `/partition` to split IMPL into tasks
```

## 6. Implementation Steps - Skills

### MNF-IP01-IS-15: edird-phase-planning/SKILL.md

**Location**: `DevSystemV3.3/skills/edird-phase-planning/SKILL.md` after When to Invoke

**Action**: Add MNF section

**Content**:
```markdown
## MUST-NOT-FORGET

- `/build` and `/solve` are the entry workflows
- Use `/write-spec`, `/write-impl-plan`, `/write-test-plan`, `/write-tasks-plan` for documents
- Check gates before phase transitions
```

### MNF-IP01-IS-16: deep-research/RESEARCH_STRATEGY_MEPI.md

**Location**: After header section

**Action**: Add MNF section

**Content**:
```markdown
## MUST-NOT-FORGET

- Run `/verify` on STRUT plan before proceeding
```

### MNF-IP01-IS-17: deep-research/RESEARCH_STRATEGY_MCPI.md

**Location**: After header section

**Action**: Add MNF section

**Content**:
```markdown
## MUST-NOT-FORGET

- Run `/verify` on STRUT plan before proceeding
```

### MNF-IP01-IS-18: deep-research/DOMAIN_DEFAULT.md

**Location**: After VCRIV Pipeline section

**Action**: Add MNF section

**Content**:
```markdown
## MUST-NOT-FORGET

- Run full VCRIV pipeline: `/verify` -> `/critique` -> `/reconcile` -> implement -> `/verify`
```

## 7. Verification Checklist

### Prerequisites
- [x] **MNF-IP01-VC-01**: `_INFO_MNF_TECHNIQUE.md` exists and is complete
- [x] **MNF-IP01-VC-02**: All 18 target files identified and accessible

### Implementation - HIGH Priority (4 files)
- [x] **MNF-IP01-VC-03**: IS-01 `build.md` completed
- [x] **MNF-IP01-VC-04**: IS-02 `solve.md` completed
- [x] **MNF-IP01-VC-05**: IS-03 `implement.md` completed
- [x] **MNF-IP01-VC-06**: IS-04 `continue.md` completed

### Implementation - MEDIUM Priority (4 files)
- [x] **MNF-IP01-VC-07**: IS-05 `learn.md` completed
- [x] **MNF-IP01-VC-08**: IS-06 `fail.md` completed
- [x] **MNF-IP01-VC-09**: IS-07 `transcribe.md` completed
- [x] **MNF-IP01-VC-10**: IS-08 `session-finalize.md` completed

### Implementation - LOW Priority (6 files)
- [x] **MNF-IP01-VC-11**: IS-09 `write-spec.md` completed
- [x] **MNF-IP01-VC-12**: IS-10 `write-impl-plan.md` completed
- [x] **MNF-IP01-VC-13**: IS-11 `write-test-plan.md` completed
- [x] **MNF-IP01-VC-14**: IS-12 `write-info.md` completed
- [x] **MNF-IP01-VC-15**: IS-13 `write-strut.md` completed
- [x] **MNF-IP01-VC-16**: IS-14 `write-tasks-plan.md` completed

### Implementation - Skills (4 files)
- [x] **MNF-IP01-VC-17**: IS-15 `edird-phase-planning/SKILL.md` completed
- [x] **MNF-IP01-VC-18**: IS-16 `RESEARCH_STRATEGY_MEPI.md` completed
- [x] **MNF-IP01-VC-19**: IS-17 `RESEARCH_STRATEGY_MCPI.md` completed
- [x] **MNF-IP01-VC-20**: IS-18 `DOMAIN_DEFAULT.md` completed

### Validation
- [x] **MNF-IP01-VC-21**: All 18 files synced to `.windsurf/`
- [x] **MNF-IP01-VC-22**: Grep confirms all files have `MUST-NOT-FORGET` section
- [x] **MNF-IP01-VC-23**: No duplicate MNF sections in any file

## 8. Document History

**[2026-02-28 13:17]**
- Completed: All 23 verification checklist items marked done
- Verified: No duplicate MNF sections in any file

**[2026-02-28 13:14]**
- Added: Merge Rules section to preserve existing MNF items
- Added: PRESERVE rule to MUST-NOT-FORGET section

**[2026-02-28 13:10]**
- Initial implementation plan created
