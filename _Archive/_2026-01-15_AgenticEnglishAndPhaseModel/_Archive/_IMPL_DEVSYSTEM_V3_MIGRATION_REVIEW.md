<DevSystem EmojisAllowed=true />

# Devil's Advocate Review: DevSystem V3 Migration Plan

**Reviewed**: 2026-01-15 20:21
**Document**: `_IMPL_DEVSYSTEM_V3_MIGRATION.md [DSVS-IP01]`
**Focus**: Flawed assumptions, logic errors, hidden risks

## MUST-NOT-FORGET (Review Constraints)

- Goal: Migrate DevSystemV2.1 to V3 with EDIRD phase model
- Progressive disclosure: ~230 lines always-on, ~600 lines on-demand
- Hybrid migration: Create V3 folder, test, then deploy
- 4 linked repos must also be migrated

## Critical Issues

### ❌ `DSVS-RV-01` Assumption: Agent Will Invoke Skills When Needed

**Where**: IS-03b, IS-03c (edird-core.md + edird-phase-model skill)

**Assumption**: "For full model with gates, flows, and next-action logic: invoke @edird-phase-model"

**Problem**: Agents don't reliably invoke skills unless:
1. A workflow explicitly requires it with `## Required Skills`
2. The user mentions it with `@skill-name`
3. The task description triggers the skill description match

**Risk**: Agent sees edird-core.md (always-on), thinks it has enough context, and proceeds without reading GATES.md or FLOWS.md. Results in:
- Skipping gates because checklist not loaded
- Wrong verb sequence because FLOWS.md not read
- No stuck detection because NEXT_ACTION.md not consulted

**Evidence**: Current Windsurf behavior - skills are only invoked when explicitly referenced or when description strongly matches task.

**Suggested fix**: 
- Add explicit gate checklists to edird-core.md (not just "invoke skill")
- Or add `## Required Skills: @edird-phase-model` to ALL phase workflows

### ❌ `DSVS-RV-02` No Rollback Plan If Migration Breaks Agent

**Where**: IS-11 (Deploy to IPPS), IS-13 (Deploy to Linked Repos)

**Problem**: Plan says "Backup current .windsurf" but no rollback procedure if:
- Agent behavior degrades after V3 deployment
- Linked repo has incompatible custom workflows
- New workflows cause infinite loops or stuck states

**Current plan**:
```powershell
Copy-Item -Path ".windsurf" -Destination ".windsurf.v2.1.backup" -Recurse
Remove-Item -Path ".windsurf/*" -Recurse -Force
Copy-Item -Path "DevSystemV3/*" -Destination ".windsurf/" -Recurse
```

**Risk**: If V3 has issues, user must manually restore backup. No documented procedure.

**Suggested fix**: Add IS-15 "Rollback Procedure":
```powershell
# If V3 causes issues:
Remove-Item -Path ".windsurf/*" -Recurse -Force
Copy-Item -Path ".windsurf.v2.1.backup/*" -Destination ".windsurf/" -Recurse
```

### ❌ `DSVS-RV-03` 25-Hour Estimate is Unrealistic for One Person

**Where**: Section 1 (Migration Overview - Timeline)

**Assumption**: 25 hours total effort

**Problem**: Estimate assumes:
- No unexpected issues during restructuring
- All 20 workflows convert cleanly to EDIRD phases
- Testing reveals no design flaws requiring spec updates
- Linked repos have no custom modifications

**Hidden complexity**:
- Phase 4 "Batch migrate remaining" = 19 workflows in 8 hours = 25 min/workflow
- Each workflow needs: read, restructure, test, fix, commit
- 25 min is optimistic for RESTRUCTURE actions

**Risk**: Underestimate leads to rushed work, incomplete testing, or abandoned migration.

**Suggested fix**: 
- Add 50% buffer (37.5 hours)
- Or split into multiple sessions with checkpoints
- Or reduce scope (migrate critical workflows first, deprecate others)

## High Priority Issues

### ⚠️ `DSVS-RV-04` Workflow Template Has [DECOMPOSE] in Wrong Phase

**Where**: IS-05 (Restructure implement.md - V3 structure)

**Problem**: Template shows:
```markdown
## Phase: IMPLEMENT
1. [DECOMPOSE] - Break IMPL plan into small testable steps
```

**But**: Per EDIRD-SP04, [DECOMPOSE] belongs to DESIGN phase, not IMPLEMENT phase.

**Risk**: Contradicts spec. Agent confusion about when decomposition happens.

**Suggested fix**: Remove [DECOMPOSE] from implement.md. Decomposition should happen in `/design` workflow before `/implement` is called.

### ⚠️ `DSVS-RV-05` Missing: How Agent Knows Current Phase

**Where**: IS-03b (edird-core.md), Phase Tracking section

**Problem**: Plan says "Sessions track current phase in NOTES.md" but:
- Who writes the phase to NOTES.md? Agent? User?
- When is it updated? After each verb? After phase transition?
- What if NOTES.md doesn't have "Current Phase" section?

**Risk**: Without clear ownership, phase tracking won't happen consistently.

**Suggested fix**: Add to edird-core.md:
```markdown
## Phase Tracking (Agent Responsibility)

After each phase transition, agent MUST update session NOTES.md:
1. Add/update "## Current Phase" section
2. Record: Phase name, last verb outcome, gate status
3. If NOTES.md missing section, create it
```

### ⚠️ `DSVS-RV-06` Test Cases Don't Cover Failure Modes

**Where**: Section 9 (Test Cases)

**Problem**: All test cases are happy-path:
- TC-01: "ok=true, single commit created"
- TC-02: "ok=true, multiple commits, all tests pass"

**Missing**:
- What if `/implement` called without IMPL plan?
- What if gate check fails and agent loops forever?
- What if [CONSULT] returns no response?

**Risk**: Migration passes testing but fails in edge cases.

**Suggested fix**: Add failure-mode test cases:
- TC-10: `/implement` without IMPL plan -> ok=false, error message, stays in DESIGN
- TC-11: Gate loop exceeds 3 cycles -> [CONSULT] triggered
- TC-12: [CONSULT] timeout -> graceful degradation

## Medium Priority Issues

### ⚡ `DSVS-RV-07` BRANCHING.md Purpose Unclear

**Where**: IS-03c (edird-phase-model skill)

**Problem**: BRANCHING.md described as "Context state branching syntax" but:
- Is this reference documentation or executable rules?
- When would agent read this file?
- SKILL.md "When to Invoke" doesn't mention BRANCHING.md

**Risk**: File created but never used.

**Suggested fix**: Either add BRANCHING.md to "When to Invoke" section, or merge content into FLOWS.md.

### ⚡ `DSVS-RV-08` Linked Repos May Have Diverged

**Where**: IS-13 (Deploy to Linked Repos)

**Assumption**: All linked repos use standard DevSystemV2.1 structure

**Problem**: !NOTES.md shows linked repos with instructions like:
- "Overwrite everything"
- "Delete deprecated or renamed files"
- "Don't delete unrelated existing files"

But no verification that repos haven't added custom workflows or modified skills.

**Risk**: Overwriting custom content in linked repos.

**Suggested fix**: Add verification step before deployment:
```powershell
# List files in target .windsurf not in DevSystemV3
Compare-Object (Get-ChildItem target/.windsurf -Recurse) (Get-ChildItem DevSystemV3 -Recurse)
```

## Questions That Need Answers

1. **Skill invocation**: How do we ensure agent reads @edird-phase-model when needed?

2. **Phase tracking ownership**: Who updates NOTES.md with current phase - agent or workflow?

3. **Failure recovery**: What's the documented rollback procedure?

4. **Time estimate**: Is 25 hours realistic, or should we plan for 40+?

5. **Linked repo verification**: How do we check for custom content before overwriting?

## Summary

| Priority | Count | Status |
|----------|-------|--------|
| ❌ Critical | 3 | Needs resolution before implementation |
| ⚠️ High | 3 | Should address for robust operation |
| ⚡ Medium | 2 | Worth clarifying |

**Overall Assessment**: The plan has good structure but makes optimistic assumptions about agent behavior and timeline. Critical issues center around skill invocation reliability and missing rollback procedures.

**Recommendation**: Address Critical issues RV-01 and RV-02 before starting migration. Consider RV-03 timeline adjustment.
