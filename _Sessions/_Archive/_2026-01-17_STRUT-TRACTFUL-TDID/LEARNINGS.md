# Session Learnings

## Active Learnings

### `EDIRD-LN-003` IDE Buffer Sync After Major Rewrites

- **When**: 2026-01-20
- **Source**: EDIRD-FL-001
- **Problem Type**: BUILD / COMPLEXITY-LOW (file editing)

#### Context

Agent rewrote go.md completely (removed all EDIRD references). Edit succeeded on disk but user's IDE showed stale content.

#### Root Cause

Agent tooling writes to disk, but IDE buffers are independent. Major file rewrites can leave IDE showing old content.

#### Prevention Rules

1. After major file rewrites (>50% changed), warn: "File rewritten - reload in IDE if showing old content"
2. When user reports "file shows X" but agent wrote Y, verify with `Get-Content` before re-editing
3. Distinguish between "edit failed" vs "IDE buffer stale"

---

### `EDIRD-LN-002` Plain English in Workflows

- **When**: 2026-01-20
- **Source**: EDIRD-FL-002
- **Problem Type**: BUILD / COMPLEXITY-MEDIUM (documentation style)

#### Context

Agent updated test.md using AGEN verbs ([GATHER], [TEST], [VERIFY]) following pattern from verify.md. User wanted plain English.

#### Root Cause

No explicit style guide distinguishing where AGEN verbs belong vs plain English.

#### Prevention Rules

1. **Rules**: AGEN verbs OK (always-on, formal definitions)
2. **Skills**: AGEN verbs OK (invoked when needed, specialized knowledge)
3. **Workflows**: Plain English (entry points, user-facing instructions)
4. When updating workflows, convert AGEN verbs to plain English equivalents

---

### `EDIRD-LN-001` Workflow-Skill Separation Principle

- **When**: 2026-01-20
- **Source**: EDIRD-FL-001, EDIRD-FL-002, EDIRD-FL-003
- **Problem Type**: BUILD / COMPLEXITY-MEDIUM (architecture refactoring)

#### Context at Decision Time

- Task: Implement DevSystemV3.1 with renamed/simplified EDIRD components
- Available: Session specs (AGEN, STRUT, TRACTFUL, EDIRD), existing DevSystemV3 structure
- Constraint: User wanted workflows decoupled from EDIRD, skills to hold phase logic

#### Assumptions Made

- `[UNVERIFIED]` Existing workflow patterns (AGEN verbs, detailed phase steps) should be preserved
- `[CONTRADICTS]` Workflows and skills can both contain detailed phase instructions
- `[VERIFIED]` Skills are invoked by workflows and provide specialized knowledge

#### Rationale

- Original design: Workflows were self-contained with full phase details
- New design: Skills hold reusable knowledge, workflows are thin entry points
- Trade-off: Less duplication vs more indirection

#### Actual Outcome

- Workflows initially retained detailed content duplicating skill
- Used AGEN verbs in workflows when plain English was expected
- Required user correction to simplify and normalize language

#### Problem Dependency Tree

```
[Root: No clear workflow-skill contract]
├─> [Duplicated content in build.md/solve.md]
│   └─> [Symptom: Verbose workflows, DRY violation]
├─> [AGEN verbs in workflow instructions]
│   └─> [Symptom: Inconsistent style, harder to read]
└─> [No style guide for workflow language]
    └─> [Symptom: Mixed AGEN/English in same file]
```

#### Root Cause Analysis

1. **Root cause**: No explicit contract defining what belongs in workflows vs skills
2. **Counterfactual**: If we had a "workflow = entry point + skill ref + workflow-specific rules only" guideline, duplication would have been caught immediately
3. **Prevention**: Define and document the workflow-skill boundary before implementation

#### Prevention Rules

1. **Workflows are thin**: Entry point, skill references, workflow-specific rules only
2. **Skills hold knowledge**: Phase logic, gates, detailed procedures go in skills
3. **Plain English in workflows**: AGEN verbs for rules/skills, plain English for workflow instructions
4. **DRY check after adding skills**: Review all referencing workflows for content that should move to skill

## Resolved Learnings

(none yet)
