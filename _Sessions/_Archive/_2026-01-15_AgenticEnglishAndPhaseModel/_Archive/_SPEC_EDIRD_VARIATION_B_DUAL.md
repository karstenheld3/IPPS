# SPEC: EDIRD Phase Model - Variation B (Dual)

**Doc ID**: EDIRD-SP03
**Goal**: Two separate phase models optimized for BUILD (code creation) and SOLVE (general problem-solving)

**Depends on:**
- `_SPEC_AGEN_AGENTIC_ENGLISH.md [AGEN-SP01]` for verb definitions and syntax

## MUST-NOT-FORGET

- Two distinct models: BUILD and SOLVE
- Each model has phase names optimized for its domain
- BUILD uses code-centric terminology
- SOLVE uses thinking-centric terminology
- First step always determines which model applies

## Table of Contents

- [1. Concept](#1-concept)
- [2. BUILD Model (Code Creation)](#2-build-model-code-creation)
- [3. SOLVE Model (Problem Solving)](#3-solve-model-problem-solving)
- [4. Model Selection](#4-model-selection)
- [5. Example Flows](#5-example-flows)
- [6. Advantages and Disadvantages](#6-advantages-and-disadvantages)
- [7. Document History](#7-document-history)

## 1. Concept

Two separate phase models, each with vocabulary optimized for its domain. The agent selects the appropriate model based on the primary output type.

```
┌────────────────────────────────────────────────────────────────────────┐
│                         Dual Phase Models                              │
├────────────────────────────────────────────────────────────────────────┤
│  BUILD Model (Code-Centric)                                            │
│  [SCOPE] → [ARCHITECT] → [CODE] → [HARDEN] → [SHIP]                    │
│  Output: Working software                                              │
├────────────────────────────────────────────────────────────────────────┤
│  SOLVE Model (Thinking-Centric)                                        │
│  [UNDERSTAND] → [FRAME] → [WORK] → [POLISH] → [DELIVER]                │
│  Output: Knowledge, decisions, documents, insights                     │
└────────────────────────────────────────────────────────────────────────┘
```

## 2. BUILD Model (Code Creation)

### Purpose

Create new software, features, systems. The primary output is working code.

### Phase Definitions

**[SCOPE]** - Define what to build
- Understand requirements and constraints
- Assess complexity (LOW/MEDIUM/HIGH)
- Confirm boundaries with [ACTOR]

**[ARCHITECT]** - Design the solution
- Plan technical approach
- Create specifications (MEDIUM+)
- Prove risky parts with POC (HIGH)
- Define test strategy

**[CODE]** - Write the software
- Implement the solution
- Configure environment
- Integrate components
- Commit frequently

**[HARDEN]** - Make it robust
- Test thoroughly
- Review and critique
- Fix issues
- Optimize performance

**[SHIP]** - Deploy and close
- Final validation
- Deploy to environment
- Document and handoff
- Close and archive

### BUILD Verb Mapping

```
[SCOPE]
├─> [RESEARCH] existing solutions and patterns
├─> [ANALYZE] affected code and dependencies
├─> [ASSESS] → COMPLEXITY-LOW/MEDIUM/HIGH
├─> [CONSULT] with [ACTOR] on requirements
└─> [DECIDE] approach
    └─> Gate: Scope confirmed, complexity assessed

[ARCHITECT]
├─> [PLAN] technical approach
├─> [OUTLINE] high-level structure
├─> [WRITE-SPEC] specification (MEDIUM+)
├─> [PROVE] risky parts with POC (HIGH)
├─> [PROPOSE] options to [ACTOR] (HIGH)
├─> [VALIDATE] design
├─> [WRITE-IMPL] implementation plan (MEDIUM+)
└─> [WRITE-TEST] test plan (HIGH)
    └─> Gate: Design complete, POC successful

[CODE]
├─> [IMPLEMENT] code changes
├─> [CONFIGURE] environment/settings
├─> [INTEGRATE] components (MEDIUM+)
├─> [TEST] during implementation
├─> [REFACTOR] as needed
└─> [COMMIT] small, frequent
    └─> Gate: All code complete, tests pass

[HARDEN]
├─> [REVIEW] self-review
├─> [VERIFY] against spec/rules
├─> [TEST] regression testing
├─> [CRITIQUE] devil's advocate (HIGH)
├─> [RECONCILE] pragmatic adjustments (HIGH)
├─> [FIX] found issues
└─> [OPTIMIZE] if needed
    └─> Gate: All issues resolved, verification passed

[SHIP]
├─> [TEST] final pass
├─> [VALIDATE] with [ACTOR]
├─> [MERGE] branches
├─> [DEPLOY] to environment
├─> [FINALIZE] documentation
├─> [HANDOFF] communicate
├─> [CLOSE] mark done
└─> [ARCHIVE] if session-based
```

### Complexity-Based Flow (BUILD)

```
COMPLEXITY-LOW:    [SCOPE](lite) → [ARCHITECT](outline) → [CODE] → [HARDEN](review) → [SHIP]
COMPLEXITY-MEDIUM: [SCOPE] → [ARCHITECT](spec) → [CODE] → [HARDEN](verify) → [SHIP]
COMPLEXITY-HIGH:   [SCOPE](full) → [ARCHITECT](spec+POC) → [CODE] → [HARDEN](full) → [SHIP]
```

## 3. SOLVE Model (Problem Solving)

### Purpose

Explore problems, evaluate ideas, create knowledge, make decisions. Output can be documents, decisions, insights, recommendations, or occasionally code.

### Phase Definitions

**[UNDERSTAND]** - Grasp the problem
- Research the domain or topic
- Analyze existing information
- Identify what needs to be learned or decided
- Determine problem type

**[FRAME]** - Structure the approach
- Plan methodology
- Outline structure (document, analysis, evaluation)
- Define criteria or scope
- Validate approach with [ACTOR]

**[WORK]** - Execute the thinking
- Research deeply
- Analyze data or situations
- Write content
- Evaluate options
- Generate insights

**[POLISH]** - Refine quality
- Review own work
- Verify accuracy and claims
- Critique and strengthen
- Improve clarity

**[DELIVER]** - Complete and handoff
- Present findings or recommendations
- Make or support decisions
- Finalize deliverable
- Archive for reference

### Problem Types

Assessed in [UNDERSTAND] phase:

- **RESEARCH** - Explore a topic, gather information
- **ANALYSIS** - Deep dive into data or situation
- **EVALUATION** - Compare options, make recommendations
- **WRITING** - Create documents, books, reports
- **DECISION** - Choose between alternatives
- **HOTFIX** - Production down (code-related but uses SOLVE for diagnosis)
- **BUGFIX** - Defect investigation
- **CHORE** - Maintenance analysis

### SOLVE Verb Mapping

```
[UNDERSTAND]
├─> [RESEARCH] the topic, domain, or problem space
├─> [ANALYZE] existing information, data, context
├─> [ASSESS] → problem type (RESEARCH/ANALYSIS/EVALUATION/WRITING/DECISION)
├─> [CONSULT] with [ACTOR] to clarify scope
├─> [ENUMERATE] all aspects to consider
└─> [DECIDE] what question to answer
    └─> Gate: Problem understood, scope defined

[FRAME]
├─> [PLAN] approach and methodology
├─> [OUTLINE] structure (document, analysis, evaluation)
├─> [PROVE] assumptions if needed
├─> [PROPOSE] structure to [ACTOR]
└─> [VALIDATE] approach covers the problem
    └─> Gate: Approach validated, structure clear

[WORK]
├─> [RESEARCH] deep dive (RESEARCH type)
├─> [ANALYZE] data/situation (ANALYSIS type)
├─> [WRITE] content (WRITING type)
├─> [EVALUATE] options against criteria (EVALUATION type)
├─> [SYNTHESIZE] findings into understanding
├─> [IMPLEMENT] code if solution requires it
└─> [COMMIT] progress checkpoints
    └─> Gate: Core work complete

[POLISH]
├─> [REVIEW] own work
├─> [VERIFY] claims and accuracy
├─> [CRITIQUE] find weaknesses
├─> [RECONCILE] balance ideal vs practical
├─> [FIX] errors and gaps
└─> [IMPROVE] clarity and quality
    └─> Gate: Quality verified, issues resolved

[DELIVER]
├─> [CONCLUDE] draw final conclusions
├─> [RECOMMEND] if recommending single option
├─> [PROPOSE] if presenting multiple options
├─> [VALIDATE] with [ACTOR]
├─> [FINALIZE] polish and complete
├─> [DECIDE] final choice (DECISION type)
├─> [HANDOFF] communicate findings
├─> [CLOSE] mark complete
└─> [ARCHIVE] for future reference
```

### Problem-Type Flow (SOLVE)

```
RESEARCH:   [UNDERSTAND] → [FRAME](outline) → [WORK](research) → [POLISH] → [DELIVER](INFO doc)
ANALYSIS:   [UNDERSTAND] → [FRAME](criteria) → [WORK](analyze) → [POLISH] → [DELIVER](findings)
EVALUATION: [UNDERSTAND] → [FRAME](criteria) → [WORK](evaluate) → [POLISH] → [DELIVER](recommendation)
WRITING:    [UNDERSTAND] → [FRAME](outline) → [WORK](write) → [POLISH](edit) → [DELIVER](document)
DECISION:   [UNDERSTAND] → [FRAME](criteria) → [WORK](evaluate) → [POLISH] → [DELIVER](decision)
```

## 4. Model Selection

First action determines which model to use:

```
[ASSESS] primary output type:
│
├─> Is primary output WORKING CODE?
│   └─> Yes → BUILD model
│       └─> Phases: [SCOPE] → [ARCHITECT] → [CODE] → [HARDEN] → [SHIP]
│
└─> Is primary output KNOWLEDGE/DECISION/DOCUMENT?
    └─> Yes → SOLVE model
        └─> Phases: [UNDERSTAND] → [FRAME] → [WORK] → [POLISH] → [DELIVER]
```

### Hybrid Situations

Some work involves both models:

**SOLVE then BUILD**: Research best approach, then build it
```
[UNDERSTAND] → [FRAME] → [WORK](evaluate options) → [DELIVER](decision)
    └─> Then switch to BUILD model for implementation
```

**BUILD with embedded SOLVE**: Building requires investigation
```
[SCOPE] → [ARCHITECT]
    └─> Encounter unknown → mini [UNDERSTAND] → [FRAME] → [WORK]
    └─> Return to [ARCHITECT] with knowledge
```

## 5. Example Flows

### BUILD Example: Add User Authentication

```
[SCOPE]
├─> [RESEARCH] auth patterns (OAuth, JWT, sessions)
├─> [ANALYZE] existing user model
├─> [ASSESS] → COMPLEXITY-HIGH
└─> [DECIDE] OAuth2 with JWT tokens

[ARCHITECT]
├─> [WRITE-SPEC] authentication specification
├─> [PROVE] OAuth flow with test provider
├─> [WRITE-IMPL] implementation plan
└─> [WRITE-TEST] test plan

[CODE]
├─> [IMPLEMENT] auth endpoints
├─> [CONFIGURE] OAuth provider
├─> [INTEGRATE] with user service
└─> [COMMIT] incremental commits

[HARDEN]
├─> [VERIFY] against spec
├─> [TEST] all auth flows
├─> [CRITIQUE] security review
└─> [FIX] found issues

[SHIP]
├─> [DEPLOY] to staging, then production
├─> [FINALIZE] documentation
└─> [CLOSE] mark feature complete
```

### SOLVE Example: Evaluate Database Options

```
[UNDERSTAND]
├─> [RESEARCH] current database limitations
├─> [ANALYZE] usage patterns and growth projections
├─> [ASSESS] → EVALUATION problem type
└─> [DECIDE] evaluate PostgreSQL vs MongoDB vs DynamoDB

[FRAME]
├─> [OUTLINE] evaluation criteria (cost, performance, scalability)
├─> [PLAN] how to gather data for each criterion
└─> [VALIDATE] criteria with [ACTOR]

[WORK]
├─> [RESEARCH] each database option
├─> [ANALYZE] against each criterion
├─> [EVALUATE] score each option
└─> [SYNTHESIZE] overall assessment

[POLISH]
├─> [VERIFY] accuracy of claims
├─> [CRITIQUE] missing considerations?
├─> [RECONCILE] ideal vs practical
└─> [IMPROVE] clarity of recommendation

[DELIVER]
├─> [CONCLUDE] PostgreSQL best fits our needs
├─> [RECOMMEND] with rationale
├─> [VALIDATE] with [ACTOR]
└─> [ARCHIVE] evaluation document
```

### SOLVE Example: Write Book Chapter

```
[UNDERSTAND]
├─> [RESEARCH] topic deeply
├─> [ANALYZE] what readers need to understand
├─> [ASSESS] → WRITING problem type
└─> [DECIDE] chapter scope and angle

[FRAME]
├─> [OUTLINE] chapter structure
├─> [PLAN] examples and illustrations needed
└─> [VALIDATE] outline with editor

[WORK]
├─> [WRITE] first draft
├─> [RESEARCH] additional details as needed
└─> [COMMIT] save progress

[POLISH]
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

### SOLVE Example: Strategic Decision

```
[UNDERSTAND]
├─> [RESEARCH] market conditions
├─> [ANALYZE] competitive landscape
├─> [ASSESS] → DECISION problem type
├─> [ENUMERATE] all factors to consider
└─> [DECIDE] scope: Build vs Buy vs Partner

[FRAME]
├─> [OUTLINE] decision criteria
├─> [PLAN] information needed for each option
└─> [VALIDATE] criteria with stakeholders

[WORK]
├─> [RESEARCH] each option thoroughly
├─> [ANALYZE] cost, time, risk for each
├─> [EVALUATE] against criteria
└─> [SYNTHESIZE] findings

[POLISH]
├─> [CRITIQUE] are we missing anything?
├─> [VERIFY] assumptions
├─> [RECONCILE] short-term vs long-term
└─> [IMPROVE] clarity of reasoning

[DELIVER]
├─> [CONCLUDE] Partner is best option
├─> [RECOMMEND] specific partner approach
├─> [VALIDATE] with [ACTOR]
├─> [DECIDE] proceed with partnership
└─> [ARCHIVE] decision rationale
```

## 6. Advantages and Disadvantages

### Advantages

- **Domain-optimized vocabulary** - Phase names feel natural for each domain
- **Clear mental model** - No confusion about which verbs apply
- **Explicit output focus** - BUILD = code, SOLVE = knowledge/decisions
- **Easier learning** - Learn one model at a time based on work type
- **Specialized optimization** - Each model can evolve independently

### Disadvantages

- **Two models to learn** - More vocabulary to remember
- **Model switching overhead** - Must explicitly switch between models
- **Potential duplication** - Some concepts overlap (gates, outcomes)
- **Hybrid complexity** - Mixed work requires coordination between models
- **Different phase names** - Cannot use consistent terminology across domains

## 7. Document History

**[2026-01-15 19:15]**
- Initial variation created
- Defined BUILD model: SCOPE, ARCHITECT, CODE, HARDEN, SHIP
- Defined SOLVE model: UNDERSTAND, FRAME, WORK, POLISH, DELIVER
- Added model selection logic
- Added four example flows (feature, evaluation, writing, decision)
