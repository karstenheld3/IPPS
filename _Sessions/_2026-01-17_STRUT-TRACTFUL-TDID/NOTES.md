# Session Notes

## Session Info

- **Started**: 2026-01-17
- **Goal**: Formalize STRUT, TRACTFUL, TDID concepts; improve AGEN/EDIRD; create DevSystemV3.1

## Current Phase

**Phase**: EXPLORE
**Workflow**: SOLVE (WRITING + ANALYSIS)
**Assessment**: COMPLEXITY-HIGH (architecture, new patterns, multiple specs)

## IMPORTANT: Cascade Agent Instructions

1. No Markdown tables - use unnumbered lists with indented properties
2. No emojis in documentation
3. Use ASCII quotes ("double" or 'single'), never Unicode quotes
4. Use Unicode box-drawing for trees/flows: `├─>` `└─>` `│`
5. Keep ASCII `+` `-` `|` for UI diagrams
6. Most recent changes at top in changelog sections
7. Reference docs by filename AND Doc ID: `SPEC_STRUT_STRUCTURED_THINKING.md [STRUT-SP01]`
8. Gate checks require evidence - cannot mark phase complete without deliverables
9. Never auto-deploy to linked repos
10. COMPLEXITY-HIGH requires comprehensive docs with detailed analysis

## Topic Registry

- **AGEN** - Agentic English - controlled vocabulary
- **EDIRD** - Phase model (Explore, Design, Implement, Refine, Deliver)
- **STRUT** - Structured Thinking - method and notation
- **TRACT** - Traceable Requirements Artifacts and Coded Templates
- **TRACTFUL** - Traceable Requirements Artifacts and Coded Templates For Unified Lifecycle
- **TDID** - Tractful Document ID system
- **GLOB** - Global/workspace-wide concerns

## Key Concepts to Formalize

### STRUT (Structured Thinking)

Method and notation for:
- Planning complex tasks
- Tracking progress through phases
- Verifying completion
- Supporting autonomous long runs

### TRACTFUL (Document Framework)

Document types and templates:
- INFO, SPEC, IMPL, TEST, FIX, FAILS, REVIEW, TASKS
- Universal ID system (TDID)
- Verb-driven actions
- Cross-document traceability

### TDID (Document ID System)

- Global uniqueness guarantee
- Topic registry requirement
- Document and item IDs
- Cross-reference format

### AGEN Extensions

New syntax distinction:
- `STATE` (uppercase, no brackets) - TOPICs, concepts, conditions, context state
- `[INSTRUCTION]` (brackets) - verbs, placeholders, labels

New verbs:
- `[RECAP]` - analyze context, revisit plan, identify status
- `[CONTINUE]` - forward-looking assessment, execute next items
- `[GO]` - sequence of RECAP + CONTINUE until goal reached
- `[LEARN]` - analyze for fails, document in FAILS.md
- `[RESEARCH]` - iterative research with MEPI strategy
- `[PARTITION]` - split IMPL/TEST/TASK plans into testable chunks

### SOCAS (Signs Of Confusion And Sloppiness)

Quality evaluation heuristic for [RESEARCH] and [REVIEW]:
- Inconsistent terminology: Same concept named multiple ways
- Undefined or hand-wavy concepts: Key nouns without clear definition
- Unnecessary complexity: Abstractions that don't earn their cost
- Overlapping responsibilities: Two components doing the same job
- Gaps in reasoning: Conclusions not supported by evidence
- Implicit assumptions: Critical constraints left unstated
- Local optimization: Ignoring system-level effects
- Ambiguity left unresolved: Known conflicts without decision
- Presentation sloppiness: Typos, stale references, unclear structure
- No explicit tradeoffs: Choices without discussion of alternatives

### MEPI (Most Executable Point of Information)

Research strategy for [RESEARCH] verb:
- Strive for MEPI, not MCPI (Most Complete Point of Information)
- Evaluate sources against each other
- Drop noise, redundancy, speculative content, unverified sources
- Rank sources by SOCAS criteria

## Session Acceptance Criteria

1. All specs are harmonized: Minimum overlap, clear responsibilities, all phases covered
2. Agent can use STRUT method for autonomous long runs of development/problem solving
3. Separation of concerns:
   - STRUT: method and formal framework
   - EDIRD: thinking logic and approach, dependency tree, acceptance criteria
   - TRACTFUL: implementation framework (documents, templates)
   - AGEN: language for cross-layer communication
   - TDID: global document/item cross-referencing
4. After a run, all work is fully documented and packaged
5. Working solution for workspace-wide CONSTANT uniqueness
6. TASKS template and writing skill integrated

## Session Outputs

- `DevSystemV3.1/` - New DevSystem version folder
- `SPEC_STRUT_STRUCTURED_THINKING.md [STRUT-SP01]` - Structured Thinking spec
- `SPEC_TRACTFUL.md [TRACTFUL-SP01]` - Document framework spec
- `SPEC_TDID.md [TDID-SP01]` - Document ID system spec
- `SPEC_AGEN_AGENTIC_ENGLISH.md [AGEN-SP02]` - Updated AGEN spec
- `SPEC_EDIRD_PHASE_MODEL.md [EDIRD-SP05]` - Updated EDIRD spec

## Key Decisions

**KD-01: STRUT format is verb-centric, not task-centric**
- Uses AGEN verbs as plan nodes
- Enables verb outcome tracking (-OK, -FAIL, -SKIP, -PARTIAL)
- Consistent with workflow definitions

**KD-02: STRUT is phase-model agnostic**
- Works with EDIRD or alternative phase models
- Phase names come from model, not hardcoded in STRUT
- Allows experimentation with different models

**KD-03: STRUT does NOT include time/priority**
- Sequence determined by order in plan
- Time estimates belong in TASKS documents
- Priority determined by dependency order

**KD-04: STRUT does NOT invent new keywords**
- Use only existing AGEN verbs and outcomes (-OK, -FAIL, -SKIP)
- No EXHAUST, TRY, or other invented keywords
- Loop exhaustion handled via fall-through to next sibling or labeled blocks

## Important Findings

**Research completed**: `INFO_STRUT_FEATURES.md [STRUT-IN01]`

**3 Use Cases identified:**
1. Session Planning - generate plan at start
2. Autonomous Execution - determine next action from state
3. Resume/Handoff - new agent understands exact state

**STRUT Format (proposed):**
```
[FROM] → [TO]: <phase description>
├─ [VERB](params): <activity description>
├─ [VERB]-OK: <completed activity>
│   └─ -FAIL → [RECOVERY]: failure handler
└─> Gate: [PHASE]→[PHASE]
    ├─ [ ] Condition (ref: FR-XX)
    └─ [x] Completed condition
```

**8 Core Features (STRUT-FR-01 to FR-08):**
- Phase structure, Verb tree, Outcome tracking, Failure handlers
- Gate conditions, Conditional branching, Plan generation, Plan persistence

**5 Design Decisions (STRUT-DD-01 to DD-05):**
- Verb-centric, Phase-model agnostic, No time estimates
- Single agent assumption, Gate items are checkboxes

## Workflows to Run on Resume

1. `/prime` - reload context
2. Read all session documents
3. Check PROGRESS.md for current status
4. Continue with next pending item

