---
description: Fix any problem by reading relevant DevSystem knowledge and applying it
---

# Fix Workflow

## Required Reading (Always)

- `rules/devsystem-core.md` - Core definitions, document types, workflow reference
- `rules/agent-behavior.md` - Attitude, communication, work patterns

## MUST-NOT-FORGET

- Read context-specific files BEFORE acting
- Apply knowledge from read files, don't just route to other workflows
- Document findings before implementing
- Verify fix against the principles read

## Step 1: Classify Problem

- CODE - Implementation defect
- DOCUMENT - Incorrect/incomplete documentation
- DESIGN - Architecture or approach flaw
- UNDERSTANDING - Knowledge gap
- PROCESS - Workflow or procedure issue
- CONFIGURATION - Settings or environment

## Step 2: Read Context-Specific Knowledge

READ from `[AGENT_FOLDER]` based on classification:

CODE: `workflows/bugfix.md`, `workflows/implement.md`, `skills/coding-conventions/SKILL.md`

DOCUMENT: `workflows/improve.md`, `workflows/verify.md`, `skills/write-documents/SKILL.md`

DESIGN: `workflows/critique.md`, `workflows/reconcile.md`, `rules/edird-phase-planning.md`

UNDERSTANDING: `workflows/research.md`, `workflows/deep-research.md`, `skills/deep-research/SKILL.md`

PROCESS: `workflows/write-spec.md`, `workflows/write-impl-plan.md`

## Step 3: Apply Knowledge

1. Understand the problem (root cause)
2. Assess impact (what's affected)
3. Plan the fix (minimal change)
4. Execute the fix
5. Verify against read principles