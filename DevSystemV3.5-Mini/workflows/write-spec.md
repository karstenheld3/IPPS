---
description: Create specification from requirements
auto_execution_mode: 1
---

# Write Specification Workflow

## Required Skills

- @write-documents for document structure and formatting rules

## MUST-NOT-FORGET

- Run `/verify` after spec complete

## Prerequisites

- User has described problem or feature
- Clarify scope and naming before starting
- Read @write-documents skill

## Steps

1. **Gather Requirements**
   - Clarify scope if unclear
   - Identify domain objects, actions, constraints
   - Document anti-patterns ("What we don't want")

2. **Propose Alternatives** (complex tasks only)
   - Present 2-3 approaches with pros/cons
   - Let user choose before proceeding

3. **Create `_SPEC_[COMPONENT].md`** in session folder per @write-documents:
   - Header block (Goal, Target file, Dependencies)
   - Scenario (Problem, Solution, What we don't want)
   - Domain Objects
   - Functional Requirements (XXXX-FR-01)
   - Design Decisions (XXXX-DD-01)
   - Key Mechanisms

4. **For UI Specs** (`_SPEC_[COMPONENT]_UI.md`)
   - Add User Actions + UX Design with ASCII diagrams
   - Show ALL buttons and interactive elements

5. **Verify** - Run `/verify`, check exhaustiveness: all domain objects, buttons, functions listed?