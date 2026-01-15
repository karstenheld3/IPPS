# SPEC: EDIRD Phase Model - Variation A (Unified)

**Doc ID**: EDIRD-SP02
**Goal**: Single adaptive phase model that works for both BUILD (code creation) and SOLVE (general problem-solving)

**Depends on:**
- `_SPEC_AGEN_AGENTIC_ENGLISH.md [AGEN-SP01]` for verb definitions and syntax

## MUST-NOT-FORGET

- One model, two workflow types: BUILD and SOLVE
- Workflow type determines verb emphasis, not phase structure
- Phases remain constant: EXPLORE, DESIGN, IMPLEMENT, REFINE, DELIVER
- BUILD = creating new software/features (code-centric)
- SOLVE = universal problem-solving (writing, research, decisions, analysis)

## Table of Contents

- [1. Concept](#1-concept)
- [2. Workflow Types](#2-workflow-types)
- [3. Phase Definitions](#3-phase-definitions)
- [4. Verb Mapping by Workflow Type](#4-verb-mapping-by-workflow-type)
- [5. Assessment Logic](#5-assessment-logic)
- [6. Example Flows](#6-example-flows)
- [7. Advantages and Disadvantages](#7-advantages-and-disadvantages)
- [8. Document History](#8-document-history)

## 1. Concept

A single EDIRD phase model adapts to different work contexts through **workflow type selection**. The five phases remain constant, but the verbs and outputs change based on whether you're building software or solving a general problem.

```
┌─────────────────────────────────────────────────────────────┐
│                    EDIRD Phase Model                        │
├─────────────────────────────────────────────────────────────┤
│  [EXPLORE] → [DESIGN] → [IMPLEMENT] → [REFINE] → [DELIVER]  │
├─────────────────────────────────────────────────────────────┤
│  Workflow Type: BUILD          │  Workflow Type: SOLVE      │
│  └─> Code-centric creation     │  └─> Universal thinking    │
└─────────────────────────────────────────────────────────────┘
```

## 2. Workflow Types

### BUILD (Feature-Based)

**Purpose**: Create new software, features, systems

**Domain**: Code-centric - the primary output is working software

**Triggers**:
- "Add a new feature..."
- "Build a system that..."
- "Create an API for..."
- "Implement authentication..."

**Assessment**: Uses COMPLEXITY-LOW/MEDIUM/HIGH → maps to semantic versioning

**Outputs**: Code, tests, documentation, deployed software

### SOLVE (Problem-Based)

**Purpose**: Explore problems, evaluate ideas, create knowledge, make decisions

**Domain**: Universal - applies to any intellectual work

**Triggers**:
- "Research the options for..."
- "Evaluate whether we should..."
- "Write a document about..."
- "Figure out why..."
- "Decide between..."
- "Analyze the impact of..."

**Assessment**: Uses PROBLEM-TYPE to determine approach depth

**Problem Types**:
- HOTFIX - Production down, immediate action
- BUGFIX - Defect in existing functionality
- CHORE - Maintenance, cleanup, updates
- MIGRATION - Data or system migration
- RESEARCH - Explore a topic, gather information
- ANALYSIS - Deep dive into data or situation
- EVALUATION - Compare options, make recommendations
- WRITING - Create documents, books, reports
- DECISION - Choose between alternatives

**Outputs**: Documents, decisions, insights, recommendations, knowledge artifacts (and sometimes code)

## 3. Phase Definitions

Phases have universal meanings that apply to both BUILD and SOLVE:

### [EXPLORE]

**Universal meaning**: Understand the situation before acting

- BUILD: What feature? What constraints? What architecture patterns?
- SOLVE: What's the real problem? What do I need to learn? What are the boundaries?

### [DESIGN]

**Universal meaning**: Plan your approach before executing

- BUILD: Specs, architecture, POCs, test strategy
- SOLVE: Structure, methodology, outline, evaluation criteria

### [IMPLEMENT]

**Universal meaning**: Execute the planned work

- BUILD: Write code, configure systems, integrate components
- SOLVE: Write the document, conduct the analysis, perform the research

### [REFINE]

**Universal meaning**: Improve quality through review and iteration

- BUILD: Test, review, fix bugs, optimize performance
- SOLVE: Edit, critique, verify claims, strengthen arguments

### [DELIVER]

**Universal meaning**: Complete and hand off

- BUILD: Deploy, document, merge, close
- SOLVE: Publish, present, decide, archive

## 4. Verb Mapping by Workflow Type

### BUILD Workflow Verbs

```
[EXPLORE]
├─> [RESEARCH] existing solutions and patterns
├─> [ANALYZE] affected code and dependencies
├─> [ASSESS] → COMPLEXITY-LOW/MEDIUM/HIGH
├─> [CONSULT] with [ACTOR] on requirements
└─> [DECIDE] approach

[DESIGN]
├─> [PLAN] structured approach
├─> [OUTLINE] high-level structure (all)
├─> [WRITE-SPEC] specification (MEDIUM+)
├─> [PROVE] risky parts with POC (HIGH)
├─> [PROPOSE] options to [ACTOR] (HIGH)
├─> [VALIDATE] design
├─> [WRITE-IMPL] implementation plan (MEDIUM+)
└─> [WRITE-TEST] test plan (HIGH)

[IMPLEMENT]
├─> [IMPLEMENT] code changes
├─> [CONFIGURE] environment/settings
├─> [INTEGRATE] components (MEDIUM+)
├─> [TEST] during implementation
├─> [REFACTOR] as needed
└─> [COMMIT] small, frequent

[REFINE]
├─> [REVIEW] self-review
├─> [VERIFY] against spec/rules
├─> [TEST] regression testing
├─> [CRITIQUE] devil's advocate (HIGH)
├─> [RECONCILE] pragmatic adjustments (HIGH)
├─> [FIX] found issues
└─> [OPTIMIZE] if needed

[DELIVER]
├─> [TEST] final pass
├─> [VALIDATE] with [ACTOR]
├─> [MERGE] branches
├─> [DEPLOY] to environment
├─> [FINALIZE] documentation
├─> [HANDOFF] communicate
├─> [CLOSE] mark done
└─> [ARCHIVE] if session-based
```

### SOLVE Workflow Verbs

```
[EXPLORE]
├─> [RESEARCH] the topic, domain, or problem space
├─> [ANALYZE] existing information, data, context
├─> [ASSESS] → PROBLEM-TYPE (RESEARCH/ANALYSIS/EVALUATION/WRITING/DECISION/etc.)
├─> [CONSULT] with [ACTOR] to clarify scope
├─> [ENUMERATE] all aspects to consider
└─> [DECIDE] what question to answer

[DESIGN]
├─> [PLAN] approach and methodology
├─> [OUTLINE] structure (document, analysis, evaluation)
├─> [PROVE] assumptions if needed
├─> [PROPOSE] structure to [ACTOR]
└─> [VALIDATE] approach covers the problem

[IMPLEMENT]
├─> [RESEARCH] deep dive (for RESEARCH type)
├─> [ANALYZE] data/situation (for ANALYSIS type)
├─> [WRITE] content (for WRITING type)
├─> [EVALUATE] options (for EVALUATION type)
├─> [IMPLEMENT] code if solution requires it
└─> [COMMIT] progress checkpoints

[REFINE]
├─> [REVIEW] own work
├─> [VERIFY] claims and accuracy
├─> [CRITIQUE] find weaknesses
├─> [RECONCILE] balance ideal vs practical
├─> [FIX] errors and gaps
└─> [IMPROVE] clarity and quality

[DELIVER]
├─> [VALIDATE] with [ACTOR]
├─> [FINALIZE] polish and complete
├─> [PROPOSE] recommendations (for EVALUATION/DECISION)
├─> [DECIDE] final choice (for DECISION type)
├─> [HANDOFF] communicate findings
├─> [CLOSE] mark complete
└─> [ARCHIVE] for future reference
```

## 5. Assessment Logic

First action in EXPLORE phase determines workflow path:

```
[EXPLORE]
├─> [ASSESS] work type:
│   │
│   ├─> Is primary output CODE?
│   │   └─> Yes → BUILD workflow
│   │       └─> [ASSESS] complexity → COMPLEXITY-LOW/MEDIUM/HIGH
│   │
│   └─> Is primary output KNOWLEDGE/DECISION/DOCUMENT?
│       └─> Yes → SOLVE workflow
│           └─> [ASSESS] problem type → RESEARCH/ANALYSIS/EVALUATION/WRITING/DECISION
│                                       or HOTFIX/BUGFIX/CHORE/MIGRATION
```

## 6. Example Flows

### BUILD Example: Add User Authentication

```
[EXPLORE]
├─> [RESEARCH] auth patterns (OAuth, JWT, sessions)
├─> [ANALYZE] existing user model
├─> [ASSESS] → COMPLEXITY-HIGH (new pattern, external API)
└─> [DECIDE] OAuth2 with JWT tokens

[DESIGN]
├─> [WRITE-SPEC] authentication specification
├─> [PROVE] OAuth flow with test provider
├─> [WRITE-IMPL] implementation plan
└─> [WRITE-TEST] test plan

[IMPLEMENT]
├─> [IMPLEMENT] auth endpoints
├─> [CONFIGURE] OAuth provider
├─> [INTEGRATE] with user service
└─> [COMMIT] incremental commits

[REFINE]
├─> [VERIFY] against spec
├─> [TEST] all auth flows
├─> [CRITIQUE] security review
└─> [FIX] found issues

[DELIVER]
├─> [DEPLOY] to staging, then production
├─> [FINALIZE] documentation
└─> [CLOSE] mark feature complete
```

### SOLVE Example: Evaluate Database Options

```
[EXPLORE]
├─> [RESEARCH] current database limitations
├─> [ANALYZE] usage patterns and growth projections
├─> [ASSESS] → EVALUATION problem type
└─> [DECIDE] evaluate PostgreSQL vs MongoDB vs DynamoDB

[DESIGN]
├─> [OUTLINE] evaluation criteria (cost, performance, scalability, team expertise)
├─> [PLAN] how to gather data for each criterion
└─> [VALIDATE] criteria with [ACTOR]

[IMPLEMENT]
├─> [RESEARCH] each database option
├─> [ANALYZE] against each criterion
├─> [WRITE] findings for each option
└─> [EVALUATE] score each option

[REFINE]
├─> [VERIFY] accuracy of claims
├─> [CRITIQUE] are we missing considerations?
├─> [RECONCILE] ideal vs practical constraints
└─> [IMPROVE] clarity of recommendation

[DELIVER]
├─> [PROPOSE] recommendation with rationale
├─> [VALIDATE] with [ACTOR]
├─> [DECIDE] final choice
└─> [ARCHIVE] evaluation document
```

### SOLVE Example: Write Book Chapter

```
[EXPLORE]
├─> [RESEARCH] topic deeply
├─> [ANALYZE] what readers need to understand
├─> [ASSESS] → WRITING problem type
└─> [DECIDE] chapter scope and angle

[DESIGN]
├─> [OUTLINE] chapter structure
├─> [PLAN] examples and illustrations needed
└─> [VALIDATE] outline with editor

[IMPLEMENT]
├─> [WRITE] first draft
├─> [RESEARCH] additional details as needed
└─> [COMMIT] save progress

[REFINE]
├─> [REVIEW] read through
├─> [CRITIQUE] find weak arguments
├─> [VERIFY] accuracy of facts
├─> [IMPROVE] prose quality
└─> [FIX] errors

[DELIVER]
├─> [VALIDATE] with editor
├─> [FINALIZE] final polish
└─> [HANDOFF] submit chapter
```

## 7. Advantages and Disadvantages

### Advantages

- **Conceptual simplicity** - One model to learn and remember
- **Consistent vocabulary** - Same phase names regardless of work type
- **Flexible** - Adapts to context through verb selection
- **Transferable skills** - Process thinking applies across domains
- **Easy switching** - Can shift from BUILD to SOLVE mid-work if needed

### Disadvantages

- **Verb overload** - Many verbs to track across both workflow types
- **Assessment complexity** - Must determine BUILD vs SOLVE before starting
- **Potential confusion** - Same phase names, different activities
- **Less specialized** - May not optimize perfectly for either domain

## 8. Document History

**[2026-01-15 18:50]**
- Initial variation created
- Defined unified model with BUILD and SOLVE workflow types
- Added verb mappings for both workflow types
- Added three example flows (feature, evaluation, writing)
