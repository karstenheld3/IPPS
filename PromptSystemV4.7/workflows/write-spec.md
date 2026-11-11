---
description: Create specification from requirements
auto_execution_mode: 3
---

# Write Specification Workflow

**Goal**: Technical specification created from requirements.

**Why**: A specification gives implementation and tests a single source of truth.

Create technical specifications from requirements.

## Required Skills

- @skills:write-documents for document structure and formatting rules

## MUST-NOT-FORGET

- Final message starts with `Deliverables`: clickable workspace-relative paths (backticked, forward slashes) of main output files + short purpose (`agent-behavior.md` Deliverables first)
- Run `/verify` after spec complete
- **NEVER modify tracking documents** (PROGRESS.md, PROBLEMS.md, NOTES.md, FAILS.md). Write-* workflows create NEW files only. Tracking docs are session state, not agent operation artifacts.
- Pre-Write Privacy Gate (`agent-behavior.md`): General-purpose documents → all content generic. ILLUSTRATIVE content in any file → examples generic. Assess context BEFORE writing.
- Architecture and UX specs MUST include diagrams per `ASCII_ART_GUIDES.md`

## Prerequisites

- User has described the problem or feature
- Clarify scope and naming before starting
- Read @skills:write-documents skill

## Steps

1. **Gather Requirements**
   - Ask clarifying questions if scope is unclear
   - Identify domain objects, actions, and constraints
   - Document "What we don't want" (anti-patterns, rejected approaches)

2. **Propose Alternatives** (for complex tasks)
   - Present 2-3 implementation approaches
   - Compare pros/cons
   - Let user choose before proceeding

3. **Create Specification File**
   - Create `_SPEC_[COMPONENT].md` in session folder
   - Follow @skills:write-documents skill structure:
     - Header block (Goal, Target file, Dependencies)
     - Table of Contents
     - Scenario (Problem, Solution, What we don't want)
     - Domain Objects
     - Functional Requirements (numbered: XXXX-FR-01)
     - Design Decisions (numbered: XXXX-DD-01)
     - Key Mechanisms
     - Technical Constraints (facts constraining implementation - NO code, line numbers, or function signatures)
   - If 2+ domain objects or multi-tier architecture, add component or layer diagram per `ASCII_ART_GUIDES.md`. Mandatory for architecture and UX specs.

4. **For UI Specs** (`_SPEC_[COMPONENT]_UI.md`)
   - Add User Actions section
   - Add UX Design with ASCII diagrams per `ASCII_ART_GUIDES.md`
   - Show ALL buttons and interactive elements

5. **Verify**
   - Run /verify workflow
   - Check exhaustiveness: all domain objects, buttons, functions listed?
