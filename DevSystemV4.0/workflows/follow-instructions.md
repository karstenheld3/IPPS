---
description: Post-execution drift detection - build DoD, compare output, fix gaps
---

# Follow Instructions Workflow

Post-execution drift detection and correction. Runs AFTER a workflow or agent instruction completes. Builds a Definition-of-Done (DoD) from the original instruction, compares against actual output through three drift lenses, persists gaps, and fills them.

**Goal**: All instruction-following gaps identified, fixable gaps closed, unfixable gaps logged

**Why**: Agents report "done" while skipping process steps and forgetting requirements. This workflow catches and closes those gaps after execution.

Usage:
- `/follow-instructions` - full audit across all three drift categories
- `/follow-instructions [directive]` - audit with specific focus (e.g., `/follow-instructions that all SPEC sections have acceptance criteria`)

**Scope Boundary**: This workflow fixes **instruction-following failures** (drift from what was asked). Use `/verify` for rule/convention compliance. Use `/critique` for logic flaws and hidden risks.

## MUST-NOT-FORGET

1. Post-execution only: runs AFTER a workflow or instruction completes. Never before or during.
2. Resume first: If `__DOD_[TOPIC].md` exists, skip to Step 4 (FILL). Do NOT regenerate.
3. Re-read the original instruction BEFORE auditing - never audit from memory.
4. Two scored lenses (Output Structure, Process Discipline) + one observational lens (Meta-Criteria).
5. MISSED vs FAIL: MISSED = cannot retroactively fix. FAIL = fixable now.
6. DoD is the contract: once persisted, authoritative. Only add items for newly discovered requirements.
7. Atomic gap closure: one gap at a time. Fix, verify, update `__DOD` and planning docs.

## Mandatory Re-read

**SESSION-MODE**: NOTES.md, PROBLEMS.md, PROGRESS.md, FAILS.md

**PROJECT-MODE**: !NOTES.md or NOTES.md, FAILS.md

## GLOBAL-RULES

Apply to ALL contexts (Code Implementation, Deep Research, Generic).

### Drift Lenses

Every DoD item belongs to one of two scored categories. Meta-Criteria is observational only.

**Category 1 - Output Structure** (scored, ~high agent compliance):
- File/folder count, names, locations
- Content structure (sections, headers, fields)
- Cross-references, IDs, dependencies
- No placeholders, no truncation

**Category 2 - Process Discipline** (scored, ~low agent compliance):
- Step sequence followed as specified
- Processing depth (thorough, not superficial)
- Gate conditions respected
- Tracking files updated (NOTES, PROGRESS, PROBLEMS)
- Required verifications/tests actually run

**Meta-Criteria** (observational, not scored):
Cognitive behaviors that predict instruction-following quality. Noted for pattern detection, not included in DoD table:
- Prompt Decomposition - compound instructions broken down before acting
- Current/Target Comparison - existing state checked before modifying
- Constraint Re-reading - rules re-read mid-execution, not just at start
- Self-Correction - errors detected and fixed during work
- Backtracking - failing approaches abandoned
- Strategy Justification - WHY stated before major decisions
- Quantitative Completeness - ALL items verified processed, not just "enough"

Meta-criteria observations are noted in the report for user awareness.

**Boundary**: This workflow does NOT modify FAILS.md or LEARNINGS.md. Only the user triggers `/fail` or `/learn`.

## Workflow

```
Step 1: ANALYZE - Detect context, build DoD
Step 2: COMPARE - Assess output through drift lenses
Step 3: PERSIST - Write __DOD_[TOPIC].md
Step 4: FILL    - Close FAIL gaps in priority order
Step 5: FINALIZE - Update status, report
```

## Step 1: ANALYZE - Build DoD

### Resume Check

1. Determine `[TOPIC]` from context:
   - User specifies topic explicitly: use that
   - Planning files exist (`__STRUT_[TOPIC].md`, `__TASKS_[TOPIC].md`): extract from filename
   - Fallback: derive from session folder name or conversation subject
2. Search for existing `__DOD_[TOPIC].md`
3. If found: read file, spot-check 2-3 PASS items for regression, skip to Step 4
4. If not found: detect context and build new DoD (continue below)

### Context Detection

```
IF SPEC or IMPL or TASKS exist in scope → Code Implementation context
ELIF /deep-research just completed OR _INFO_*_Summary.md exists → Deep Research context
ELSE → Generic context (use default sources below)
```

### Default Sources (all contexts)

Read in order, extract DoD items from each:

1. **Directive** - if user passed `[directive]` after `/follow-instructions`, this is the primary focus. Filter all other sources through this lens.
2. **Original instruction** - the user prompt that triggered the work. Primary authoritative source.
3. **Planning artifacts** - any `__STRUT_[TOPIC].md`, `__TASKS_[TOPIC].md`, IMPL docs the agent created.
4. **Target workflow MNF** - process requirements the workflow specified.
5. **FAILS.md scan** - past violations of this topic or workflow (prevent recurrence).

For each source, extract requirements and assign:
- **Priority**: HIGH (missing files/sections, universal FAILS violations), MEDIUM (format, incomplete content), LOW (polish, optional)
- **Category**: 1 (Output Structure) or 2 (Process Discipline)

# CONTEXT-SPECIFIC

## Code Implementation

**Applies when**: SPEC, IMPL, or TASKS documents exist in session or project scope.

**Additional sources** (read BEFORE default sources):

1. **SPEC** - Functional requirements (FR-XX), design decisions (DD-XX), implementation guarantees (IG-XX)
2. **IMPL** - Implementation steps (IS-XX), edge cases (EC-XX), verification checklist (VC-XX)
3. **TASKS** - Work items (TK-XX) with completion status
4. **TEST** - Test cases (TC-XX) and expected results

**DoD extraction:**

- Each FR-XX → DoD item: "Requirement FR-XX implemented" (Category 1, HIGH)
- Each IG-XX → DoD item: "Guarantee IG-XX upheld in code" (Category 1, HIGH)
- Each IS-XX → DoD item: "Step IS-XX executed" (Category 2, MEDIUM)
- Each EC-XX → DoD item: "Edge case EC-XX handled" (Category 1, MEDIUM)
- Each unchecked TK-XX → DoD item: "Task TK-XX completed" (Category 2, HIGH)
- Each TC-XX → DoD item: "Test TC-XX passes" (Category 2, HIGH)
- IMPL verification checklist items → DoD items (Category 2, MEDIUM)

**Category 2 specifics for code:**
- Were tests actually run (not just written)?
- Were tracking files updated after implementation?
- Was `/verify` run after completion?
- Were commit messages created for completed steps?

## Deep Research

**Applies when**: `/deep-research` just completed, OR `_INFO_*_Summary.md` exists in session scope.

**Additional sources** (read BEFORE default sources):

1. **DEEP_RESEARCH_RULES.md** - from `@skills:deep-research` skill
2. **STRUT plan** - if `__STRUT_[TOPIC].md` exists, extract unchecked deliverables
3. **Research brief/prompt** - the original research question and scope

**DoD extraction:**

- Each STRUT deliverable → DoD item (Category 1, HIGH if unchecked)
- RULES file requirements → DoD items:
  - Source count thresholds met? (Category 1, HIGH)
  - All sources verified with real URLs? (Category 2, HIGH)
  - Synthesis document complete (no placeholder sections)? (Category 1, HIGH)
  - Multiple perspectives represented? (Category 2, MEDIUM)
  - Contradictions explicitly addressed? (Category 2, MEDIUM)

**Category 2 specifics for research:**
- Were sources actually visited (not hallucinated from training data)?
- Was search performed via specified tools (e.g., Playwright for Google)?
- Were findings cross-verified between sources?

# EXECUTION (all contexts)

## Step 2: COMPARE - Assess Output

For each DoD item, verify against actual output:

- **PASS** - criterion met
- **FAIL** - not met, fixable now (generates TODO)
- **MISSED** - needed during execution, cannot retroactively fix (e.g., backup before modify, STRUT self-tracking)
- **N/A** - not applicable to this context

Additionally, note which meta-criteria were present or absent (observational, not scored).

## Step 3: PERSIST - Write __DOD_[TOPIC].md

Create in working directory (session folder or topic subfolder):

```markdown
<DevSystem MarkdownTablesAllowed=true />
# Definition of Done: [TOPIC]

**Target workflow**: /workflow-name
**Context**: [Code Implementation | Deep Research | Generic]
**Directive**: [directive if provided, otherwise "full audit"]
**Status**: IN_PROGRESS | COMPLETE | BLOCKED

## Criteria

| ID | Criterion | Cat | Priority | Status | Source |
|----|-----------|-----|----------|--------|--------|
| 01 | FR-01 implemented | 1 | HIGH | FAIL | SPEC |
| 02 | Backup before modify | 2 | HIGH | MISSED | workflow MNF |

## TODOs

FAIL items in priority order:

- [ ] 01: Implement FR-01 (user authentication endpoint)
- [ ] 05: Add acceptance criteria to SPEC sections 3-7

## MISSED

- 02: No backup before modifying config (Category 2)

## Meta-Criteria Observations

- Prompt Decomposition: absent (jumped to implementation without breakdown)
- Quantitative Completeness: absent (processed 4/7 items without counting)
```

## Step 4: FILL - Close Gaps

Process TODO items: HIGH first, then MEDIUM, then LOW.

For each TODO:

1. Read the referenced DoD item
2. Execute minimum change to close gap
3. Verify: does the item now PASS?
4. Update `__DOD_[TOPIC].md`: FAIL → PASS, check off TODO
5. Next TODO

If a gap cannot be closed: mark BLOCKED with reason, move to next.

Session boundary: if context exhausted, update `__DOD` with current state. File persists for resume.

## Step 5: FINALIZE

When all TODOs are done or BLOCKED:

1. Update Status: all PASS/MISSED/N/A → `COMPLETE`, any BLOCKED → `BLOCKED`
2. Report summary:

```
## Follow Instructions Summary

**Topic**: [TOPIC]
**Context**: [Code Implementation | Deep Research | Generic]
**Directive**: [directive or "full audit"]
**Status**: [COMPLETE | BLOCKED]

**Scored Results**:
- Category 1 (Output Structure): [pass_count]/[total] PASS
- Category 2 (Process Discipline): [pass_count]/[total] PASS, [missed_count] MISSED

**Meta-Criteria Observations**:
- Present: [list]
- Absent: [list]

**Gaps Fixed**: [count]
**Gaps Blocked**: [count] (with reasons)
```

## Quality Gate

- [ ] All FAIL items resolved (PASS) or BLOCKED with reason
- [ ] `__DOD_[TOPIC].md` updated with final status
- [ ] No items left in FAIL status

## Trigger

- `/follow-instructions` - after any `/build`, `/implement`, `/solve` completion
- `/follow-instructions` - after `/deep-research` completion
- `/follow-instructions [directive]` - when specific aspect needs verification
- As spot-check during long autonomous sessions (`/go`)
- After `/verify` passes but user suspects shallow compliance

## No Context Match

If no SPEC/IMPL/TASKS and no research output exist: use Generic context. Build DoD entirely from conversation and planning artifacts (default sources).
