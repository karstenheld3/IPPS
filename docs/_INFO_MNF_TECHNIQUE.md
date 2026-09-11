# INFO: MNF (MUST-NOT-FORGET) Technique

**Doc ID**: MNF-IN01
**Goal**: Document the MNF technique for preventing critical oversights during task execution

## Summary

MNF is a lightweight checklist technique that ensures critical items are not forgotten during complex tasks. It operates in two phases: planning (create list) and completion (verify list).

**When to use**: Any task where forgetting a constraint would cause rework, errors, or rule violations.

## Technique Definition

### Purpose

Prevents critical oversights by making important constraints explicit and verifiable.

### Planning Phase

1. Create `MUST-NOT-FORGET` list (5-15 items max)
2. Collect items from:
   - FAILS.md (past mistakes)
   - Learnings and rules
   - Specs and user instructions
   - Session-specific constraints
3. Place at top of working document (after header block, before TOC)

### Completion Phase

1. Review each MNF item before marking task done
2. Verify compliance or document why item doesn't apply
3. Update FAILS.md if any MNF item was violated

## Placement Rules

**In documents** (SPEC, IMPL, TEST):
- After header block
- Before Table of Contents
- Section title: `## MUST-NOT-FORGET`

**In workflows**:
- After Required Skills section
- Before Step 1
- Reference in final step: "Review each MNF item above and confirm compliance"

**In skills**:
- After overview/purpose section
- Before detailed instructions

## Examples

### Workflow Example (session-load.md)

```markdown
## Required Skills
- @session-management

## MUST-NOT-FORGET
- Run `/prime` workflow BEFORE reading session documents
- `/prime` loads FAILS.md, ID-REGISTRY.md, !NOTES.md

## Step 1: Identify Session
...

## Step 5: Verify MUST-NOT-FORGET
Review each MNF item above and confirm compliance.
```

### Skill Example (git-conventions)

```markdown
## MUST-NOT-FORGET
- Use Conventional Commits: `<type>(<scope>): <description>`
- Types: feat, fix, docs, refactor, test, chore, style, perf
```

### SPEC Document Example

```markdown
# SPEC: Feature Name

**Doc ID**: FEAT-SP01
**Goal**: ...

## MUST-NOT-FORGET
- All API endpoints require authentication
- Response times must be < 200ms
- No breaking changes to existing clients

## Table of Contents
...
```

## Item Guidelines

**Good MNF items**:
- Specific and verifiable
- Reference concrete constraints
- Drawn from past failures or explicit rules
- Referenced workflows (e.g., `/prime`, `/verify`) - ensures they are actually called
- VCRIV pipeline steps when applicable - all 5 steps must complete in sequence

**Bad MNF items**:
- Vague ("be careful")
- Obvious ("write good code")
- Too many (>15 loses effectiveness)

## Related Concepts

- **FAILS.md**: Source of MNF items from past mistakes
- **VCRIV**: Quality pipeline that uses MNF at verification gates
- **STRUT**: Structured plans that include MNF sections

## Document History

**[2026-02-28 13:06]**
- Added: VCRIV pipeline steps to Item Guidelines

**[2026-02-28 13:05]**
- Added: Referenced workflows rule to Item Guidelines

**[2026-02-28 13:03]**
- Initial document created
