# INFO: STRUT Features and Use Cases

**Doc ID (TDID)**: STRUT-IN01
**Goal**: Research features and use cases for STRUT (Structured Thinking) notation based on real-world project analysis

## Summary

**Key Findings:**

STRUT must support three distinct use cases:
1. **Session Planning** - Agent creates STRUT plan at session start, updates on phase transitions
2. **Autonomous Execution** - Agent determines next action from plan state without user input
3. **Resume/Handoff** - New agent or human can read plan and understand exact state

**STRUT Plan Format (proposed):**
```
[FROM] → [TO]: <phase description, mention outcome>
├─ [VERB](params): <activity description, mention outcome>
├─ [VERB]: <activity description>
└─> [ ] Gate item (links to AC or FR if applicable)
```

**What STRUT does NOT deal with:**
- Priority of activities (determined by dependency and phase order)
- Time estimates (use HHW in TASKS documents)
- Resource allocation (single agent assumption)

## Table of Contents

- Summary
- Research Sources
- Use Case 1: Session Planning
- Use Case 2: Autonomous Execution
- Use Case 3: Resume and Handoff
- Pattern Analysis: Real-World SPECs
- Pattern Analysis: Current Workflows
- STRUT Format Requirements
- Feature List
- Document History

## Research Sources

### DevSystem Files (Current)

- `.windsurf/workflows/build.md` - BUILD workflow with EDIRD phases
- `.windsurf/workflows/solve.md` - SOLVE workflow with problem types
- `.windsurf/workflows/go-autonomous.md` - Autonomous execution pattern
- `.windsurf/workflows/implement.md` - Implementation phase details
- `SPEC_EDIRD_PHASE_MODEL.md [EDIRD-SP05]` - Phase definitions and gates

### SharePoint-GPT-Middleware (Real-World Project)

- `_V2_SPEC_CRAWLER.md` - Complex spec with FR, DD, domain objects
- `_V2_SPEC_ROUTERS.md` - Router architecture, endpoint patterns
- `_V2_SPEC_DOMAINS_UI.md` - UI specification with user actions
- `_V2_IMPL_CRAWLER.md` - Implementation plan with step functions
- `_V2_IMPL_DOMAINS_CRAWL.md` - Dialog implementation with edge cases

### Archived Research

- `_INFO_PROJECT_PHASES_OPTIONS.md [PHSE-IN01]` - Industry framework analysis (ITIL, PRINCE2, Shape Up, Scrum, Double Diamond)

## Use Case 1: Session Planning

**Scenario:** User starts `/build "Add user authentication"` or `/solve "Research OAuth providers"`

**Agent must:**
1. Assess workflow type (BUILD/SOLVE) and complexity
2. Generate STRUT plan with phases and expected verbs
3. Record plan in session PROGRESS.md
4. Track current position in plan

**Current approach (from build.md):**
- Phase tracking in NOTES.md (current phase, last verb, gate status)
- Phase plan in PROGRESS.md (5 phases with pending/in_progress/done)
- No verb-level plan - agent decides verbs ad-hoc

**Problem:** Agent can choose arbitrary verbs within phase. No upfront planning of verb sequence.

**STRUT solution:** Generate verb tree at session start based on:
- Workflow type (BUILD/SOLVE)
- Complexity (LOW/MEDIUM/HIGH)
- Problem type (for SOLVE)

## Use Case 2: Autonomous Execution

**Scenario:** Agent runs `/go-autonomous` and must complete work without user input

**Agent must:**
1. Know exactly what to do next at any point
2. Handle verb failures with defined recovery
3. Detect when gate passes and transition phases
4. Know when to stop (all gates passed, DELIVER complete)

**Current approach (from go-autonomous.md):**
```
EXPLORE → DESIGN → IMPLEMENT → REFINE → DELIVER
```
Each phase has verb list but no dependency or sequence info.

**Current decision logic (from EDIRD-SP05):**
```
next_action = f(workflow_type, current_phase, last_verb_outcome, gate_status)
```

**Problem:** Verb sequence within phase is implicit. Agent must know EDIRD spec to determine order.

**STRUT solution:** Explicit verb tree with:
- Ordered verb sequence per phase
- Conditional branches (e.g., "if COMPLEXITY-HIGH: [PROVE]")
- Failure handlers inline (e.g., "[VERIFY]-FAIL → [FIX]")

## Use Case 3: Resume and Handoff

**Scenario:** User runs `/session-resume` or new agent takes over mid-session

**Agent must:**
1. Understand current state from plan
2. Know what was completed, what failed, what's next
3. Continue without repeating completed work
4. Maintain consistency with original approach

**Current approach:**
- NOTES.md: Current Phase, Last verb, Gate status
- PROGRESS.md: Phase plan with checkboxes
- No verb-level completion tracking

**Problem:** If agent was mid-[RESEARCH] when session saved, new agent doesn't know:
- Which research was completed
- What sources were checked
- What's left to do

**STRUT solution:** Verb-level completion markers:
```
[EXPLORE] → [DESIGN]: Understand authentication requirements
├─ [ASSESS]-OK: COMPLEXITY-MEDIUM (multiple files, some dependencies)
├─ [RESEARCH]-PARTIAL: Found OAuth providers (3/5 checked)
├─ [SCOPE]-PENDING
└─> [ ] Gate: Problem understood, complexity assessed, scope defined
```

## Pattern Analysis: Real-World SPECs

### From _V2_SPEC_CRAWLER.md

**Structure observed:**
- Scenario (Problem/Solution/What we don't want)
- Domain Objects with properties and relationships
- Functional Requirements (V2CR-FR-01 through FR-XX)
- Design Decisions (V2CR-DD-01 through DD-XX)
- Implementation Guarantees (V2CR-IG-01 through IG-XX)
- Detailed sections (Local Storage, Map Files, Edge Cases)

**Key pattern:** FR/DD/IG provide acceptance criteria. STRUT gates can reference these:
```
└─> [ ] Gate: V2CR-FR-01 satisfied (change detection by immutable ID)
```

### From _V2_IMPL_CRAWLER.md

**Structure observed:**
- File structure with responsibilities
- Dataclasses with fields
- Function signatures with docstrings
- Edge case list (V2CR-IP01-EC-XX)
- Implementation steps (IS-XX)
- Verification checklist

**Key pattern:** Implementation is decomposed into:
1. Module-level (which files)
2. Class/function-level (what to create)
3. Step-level (order of implementation)

**STRUT parallel:** Phase → Verb → Sub-verb with specific params

### From _V2_IMPL_DOMAINS_CRAWL.md

**Structure observed:**
- Edge cases (V2DM-IP03-EC-01 through EC-10)
- Known limitations (KL-01, KL-02)
- Verification issues from /verify-spec (VI-01 through VI-07)
- Implementation steps (IS-01 through IS-XX)

**Key pattern:** Verification issues are discovered during planning and explicitly documented. This is a form of pre-implementation [VERIFY].

## Pattern Analysis: Current Workflows

### build.md Verb Sequence

```
EXPLORE:
├─ [ASSESS] complexity
├─ [ANALYZE] existing code
├─ [GATHER] requirements
├─ [RESEARCH] if needed
└─ [SCOPE] boundaries

DESIGN:
├─ [PLAN] approach
├─ [WRITE-SPEC]
├─ [PROVE] if MEDIUM+
├─ [WRITE-IMPL-PLAN]
├─ [WRITE-TEST-PLAN]
└─ [DECOMPOSE]

IMPLEMENT:
├─ [IMPLEMENT] → [TEST] → [FIX] loop
└─ [COMMIT]

REFINE:
├─ [REVIEW]
├─ [VERIFY]
├─ [TEST]
├─ [CRITIQUE] if MEDIUM+
├─ [RECONCILE] if MEDIUM+
└─ [FIX]

DELIVER:
├─ [VALIDATE]
├─ [MERGE]
├─ [FINALIZE]
└─ [CLOSE]
```

### solve.md Verb Variations

Problem-type specific verb emphasis:
- RESEARCH: [GATHER] → [SYNTHESIZE]
- ANALYSIS: [INVESTIGATE] → [ANALYZE]
- EVALUATION: [EVALUATE] → [COMPARE]
- WRITING: [DRAFT] → [EDIT]
- DECISION: [WEIGH] → [DECIDE]
- HOTFIX/BUGFIX: [FIX] → [TEST]

**Key insight:** SOLVE has verb variations based on problem type. STRUT must support conditional verb selection.

## STRUT Format Requirements

### Must Support

1. **Phase transitions** with gate conditions
2. **Verb sequences** within phases (ordered)
3. **Conditional verbs** based on context (complexity, problem type)
4. **Verb parameters** for specificity (e.g., `[WRITE-SPEC](FEATURE)`)
5. **Verb outcomes** tracking (-OK, -FAIL, -SKIP, -PARTIAL)
6. **Failure handlers** inline (what to do on -FAIL)
7. **Gate references** to FR/IG/AC from SPECs
8. **Nesting** for sub-activities (verb contains sub-verbs)

### Must NOT Include

1. **Priority** - determined by sequence order
2. **Time estimates** - use TASKS document HHW
3. **Resource allocation** - single agent assumption
4. **Detailed instructions** - those belong in workflows/skills

### Format Proposal

```
[EXPLORE] → [DESIGN]: Understand problem, assess complexity
├─ [ASSESS](workflow, complexity): Determine BUILD/SOLVE, LOW/MEDIUM/HIGH
│   └─ → COMPLEXITY-HIGH: Enable POC requirement
├─ [ANALYZE](existing code): Study patterns and dependencies
├─ [GATHER](requirements): Collect from user/docs
├─ [RESEARCH](if accuracy needed): External sources, cite findings
│   └─ -FAIL → [CONSULT]: Need user help finding info
├─ [SCOPE](boundaries): Define in/out of scope
└─> Gate: EXPLORE→DESIGN
    ├─ [ ] Problem/goal clearly understood
    ├─ [ ] Workflow type determined (BUILD)
    ├─ [ ] Complexity assessed (MEDIUM)
    └─ [ ] Scope boundaries defined
```

## Feature List

### Core Features (STRUT-FR)

**STRUT-FR-01: Phase Structure**
- Plan organized by phases (from EDIRD or alternative model)
- Phase has: name, description, outcome expectation
- Phase transitions are explicit with gates

**STRUT-FR-02: Verb Tree**
- Verbs listed in execution order within phase
- Verbs can have parameters: `[VERB](param1, param2)`
- Verbs can have conditional triggers: `if CONTEXT: [VERB]`
- Verbs can nest sub-verbs for complex activities

**STRUT-FR-03: Outcome Tracking**
- Each verb tracks outcome: -OK, -FAIL, -SKIP, -PARTIAL
- -PARTIAL includes progress indicator (e.g., "3/5 checked")
- Outcomes persist across session saves

**STRUT-FR-04: Failure Handlers**
- Each verb can define failure handler: `-FAIL → [RECOVERY-VERB]`
- Default failure handler: [CONSULT] after retry limit
- Retry limits configurable per complexity

**STRUT-FR-05: Gate Conditions**
- Gates are checklists at phase end
- Gate items can reference FR/IG/AC IDs
- Gate items track checked/unchecked state
- Gate must pass before phase transition

**STRUT-FR-06: Conditional Branching**
- Context states (COMPLEXITY, PROBLEM-TYPE) affect verb selection
- Conditional verbs: `if COMPLEXITY-HIGH: [PROVE]`
- Conditional skips: `if COMPLEXITY-LOW: [SKIP] POC`

**STRUT-FR-07: Plan Generation**
- Agent generates STRUT plan from workflow type + complexity
- Plan template comes from EDIRD or alternative model
- Plan customized based on session context

**STRUT-FR-08: Plan Persistence**
- Plan stored in PROGRESS.md or separate STRUT file
- Plan survives session save/resume
- Plan readable by human or different agent

### Design Decisions (STRUT-DD)

**STRUT-DD-01: Verb-centric, not task-centric**
- Plan uses AGEN verbs, not arbitrary task descriptions
- Ensures consistency with workflow definitions
- Allows verb outcome tracking

**STRUT-DD-02: Phase model agnostic**
- STRUT notation works with EDIRD or alternatives
- Phase names come from model, not hardcoded
- Allows swapping phase models

**STRUT-DD-03: No time estimates**
- STRUT tracks sequence and state, not duration
- Time estimates belong in TASKS documents
- Keeps STRUT focused on "what" not "how long"

**STRUT-DD-04: Single agent assumption**
- No parallel execution or resource allocation
- Agent executes verbs sequentially
- Simplifies state tracking

**STRUT-DD-05: Gate items are checkboxes**
- Boolean checked/unchecked state
- No partial completion for gates (use -PARTIAL for verbs)
- Gate passes when all items checked

## Repetition Notation Research

Research into how other domains handle repetition, loops, and conditional flow.

### Musical Notation

**Source:** Wikipedia - Repeat sign, bellandcomusic.com

Musical notation has evolved compact symbols for repetition:

**Simple Repeat** `|: ... :|`
- Bars enclosed by repeat signs play twice
- If no start sign, repeat from beginning

**Numbered Endings (Volta brackets)**
- `1.` First time through, play this ending
- `2.` Second time through, play this ending
- Supports N endings for N repetitions

**Jump Instructions**
- **D.C. (Da Capo)** - "from the head" - go back to beginning
- **D.S. (Dal Segno)** - "from the sign" - go back to marked point (𝄋)
- **al Fine** - play until "Fine" (end) marker
- **al Coda** - play until coda sign, then jump to coda section

**STRUT Application:**
```
[IMPLEMENT] → [REFINE]: Build and polish
├─ [IMPLEMENT] code changes
├─ [TEST]
├─ |: [FIX] if -FAIL :| (repeat until -OK)
├─ [COMMIT]
└─> Gate: tests pass
```

Or using D.S. style for non-adjacent jumps:
```
├─ [VERIFY] 𝄋              ← mark this point
├─ [FIX] if -FAIL
└─ D.S. [VERIFY]           ← jump back to marked point
```

### EBNF/BNF Notation

**Source:** cs.man.ac.uk, ISO EBNF standard

Grammar specification languages use concise repetition operators:

**Kleene Operators**
- `*` (star) - zero or more: `[VERB]*`
- `+` (plus) - one or more: `[VERB]+`
- `?` (optional) - zero or one: `[VERB]?`

**Bounded Repetition (ABNF style)**
- `2*5 item` - between 2 and 5 times
- `1* item` - 1 or more times
- `*3 item` - at most 3 times

**Grouping and Alternation**
- `( )` - grouping
- `|` - alternation (choice)
- `[ ]` - optional (Wirth style)
- `{ }` - repeat 0+ (Wirth style)

**STRUT Application:**
```
[EXPLORE] → [DESIGN]
├─ [ASSESS]
├─ [ANALYZE]+                    ← one or more times
├─ ([RESEARCH] | [GATHER])*      ← zero or more of either
├─ [PROVE]?                      ← optional (if COMPLEXITY-HIGH)
└─> Gate
```

### Process Algebra (CSP, CCS, ACP)

**Source:** Wikipedia - Process calculus

Process algebras model concurrent/sequential behavior:

**Recursion**
- Named processes can reference themselves: `P = a.P` (do action a, then become P again)
- Enables infinite behavior from finite description

**Replication**
- `!P` - unlimited parallel copies of P (bang operator)
- Models server processes that can handle unlimited requests

**Sequential Composition**
- `P ; Q` - do P, then do Q
- `a.P` - do action a, then continue as P

**Choice**
- `P + Q` - choose between P or Q (non-deterministic)
- `P [] Q` - external choice (environment decides)

**STRUT Application:**
```
[IMPLEMENT] phase:
├─ step = [IMPLEMENT] → [TEST] → ([FIX] → step | [COMMIT])
│         ↑_______________________________↵  (recursion on failure)
```

### Proposed STRUT Repetition Notation

Combining insights from all three domains:

**Simple Repetition**
```
├─ [VERB]* (description)           ← zero or more
├─ [VERB]+ (description)           ← one or more
├─ [VERB]? (description)           ← optional
├─ [VERB]{2,5} (description)       ← 2 to 5 times
```

**Conditional Loop (Musical repeat style)**
```
├─ |: [TEST] → [FIX] if -FAIL :|      ← repeat block until condition
├─ |: [TEST] → [FIX] if -FAIL :| ×3   ← repeat max 3 times, then escalate
```

**Multi-Verb Sequence Loop (Block style)**

When multiple verbs must repeat together as a unit:

```
├─ |: LOOP ×3 (until [TEST]-OK)
│   ├─ [FIX](identified issue)
│   └─ [TEST](verify fix)
│  :|
```

Or using indentation with gate (matches phase syntax):

```
├─ LOOP ×3:
│   ├─ [FIX](identified issue)
│   ├─ [TEST](verify fix)
│   └─> Gate:
│       └─ [ ] Test passes
│   -FAIL ×3 -> [CONSULT]
```

**Semantics:**
- `×N` = max iterations (required for bounded loops)
- Gate defines exit condition (same as phase gates)
- Loop exits on: gate passes OR max iterations reached
- If max reached without gate pass: execute `-FAIL ×N` handler

**Example with multiple tests:**
```
├─ LOOP ×3:
│   ├─ [TEST](unit tests)
│   ├─ [TEST](integration tests)
│   ├─ [FIX](if any fail)
│   └─> Gate:
│       ├─ [ ] Unit tests pass
│       └─ [ ] Integration tests pass
│   -FAIL ×3 -> [CONSULT]
```

**Example in context:**
```
[IMPLEMENT]: Fix what we can
├─ [IMPLEMENT](add database index)
├─ LOOP ×3:
│   ├─ [TEST](verify improvement)
│   ├─ [FIX](if regression)
│   └─> Gate:
│       └─ [ ] Performance improved
│   -FAIL ×3 -> [CONSULT](why tests keep failing)
├─ [COMMIT](fix A)
```

**Control flow:**
- Loop succeeds (gate passes within 3 attempts) → continue to `[COMMIT]`
- Loop fails (3 attempts exhausted) → execute `-FAIL ×3` handler, skip `[COMMIT]`

**Named Marker with Jump (Dal Segno style)**
```
├─ 𝄋 [VERIFY]                      ← named checkpoint
├─ ... other verbs ...
├─ D.S. [VERIFY] if -FAIL          ← jump back to checkpoint
```

**Recursive Step Definition** (with named labels)
```
├─ [IMPLEMENT]
├─ |: test_fix_cycle :| ×3:
│   ├─ [TEST]
│   │   └─ -FAIL → [FIX] → test_fix_cycle
│   │   └─ -OK → commit_fix
│   └─ -FAIL ×3 → [CONSULT]
├─ commit_fix:
│   └─ [COMMIT]
```

**Choice (Alternation)**
```
├─ ([PROVE] | [PROTOTYPE])         ← choose one
├─ [VALIDATE] | [CONSULT]          ← alternative paths
```

### Summary: Notation Comparison

**Concept** → **Music** → **EBNF** → **Process Algebra** → **STRUT Proposal**

- Repeat N times → Volta `1.` `2.` → `{N}` → recursion → `[VERB]{N}`
- Repeat 0+ → (none) → `*` → `!P` → `[VERB]*`
- Repeat 1+ → (none) → `+` → recursive → `[VERB]+`
- Optional → (none) → `?` or `[ ]` → `P + 0` → `[VERB]?`
- Loop until condition → `|: :|` → (none) → `rec X.P` → `|: label :| ×N` (verb or block)
- Jump to point → D.S./D.C. → (none) → (none) → `D.S. [marker]`
- Choice → (none) → `|` → `+` → `([A] | [B])`

## Advanced Control Flow Patterns

Three named patterns for complex STRUT plans.

### Pattern 1: NEST (Nested Workflow Invocation)

**Problem:** A workflow encounters an unknown that requires a full sub-workflow to resolve before continuing.

**Inspiration:** EDIRD "BUILD with Embedded SOLVE" pattern - mid-workflow investigation.

**Notation:**
```
[PHASE] → [PHASE]: Description
├─ [VERB]
├─ [VERB]
├─ ┌─ NEST([WORKFLOW-TYPE]): "sub-goal description"
│  │  [EXPLORE] → [DESIGN] → [IMPLEMENT] → [REFINE] → [DELIVER]
│  │  Output: insight, decision, or artifact
│  └─ END NEST
├─ [VERB] (continues with NEST output)
└─> Gate
```

**Semantics:**
- NEST creates a complete sub-workflow with its own phases and gates
- Parent workflow pauses until NEST completes
- NEST output becomes input to next verb in parent
- NEST can be BUILD, SOLVE, or any workflow type
- Nesting depth is unlimited but discouraged beyond 2 levels

**Example: BUILD with embedded SOLVE**
```
[DESIGN] → [IMPLEMENT]: Design auth system
├─ [PLAN] architecture
├─ ┌─ NEST(SOLVE:EVALUATION): "Which OAuth provider?"
│  │  [EXPLORE] → [RESEARCH] providers
│  │  [DESIGN] → [DEFINE] criteria
│  │  [IMPLEMENT] → [EVALUATE] options
│  │  [DELIVER] → [RECOMMEND] Auth0
│  └─ END NEST → provider_choice
├─ [WRITE-SPEC](provider_choice): Spec using Auth0
└─> Gate: design complete
```

**Transition Rules:**
- NEST-OK: Continue to next verb with output
- NEST-FAIL: Escalate to parent, may trigger parent [CONSULT]
- NEST gates are independent of parent gates

### Pattern 2: RETRY (Bounded Retry with Escalation)

**Problem:** An activity may fail transiently. Need bounded retries before escalating.

**Inspiration:** EDIRD retry limits (COMPLEXITY-LOW: infinite, MEDIUM/HIGH: max 5).

**Notation:**
```
├─ [VERB]{max_N, on_exhaust}: description
│   └─ -FAIL{1..N} → [RECOVERY-VERB]
- Counter resets on -OK or phase restart

**Example: Bounded test-fix cycle**
```
[IMPLEMENT] → [REFINE]: Implement feature
├─ [IMPLEMENT] code
├─ [TEST]{5, [CONSULT]}: run tests
│   └─ -FAIL{1..5} → [FIX]
│   └─ -FAIL{6} → [CONSULT] "Tests failing after 5 fix attempts"
├─ [COMMIT]
└─> Gate
```

**Shorthand variants:**
- `[VERB]{3}` - retry 3 times, then [CONSULT] (default escalation)
- `[VERB]{∞}` - infinite retries (for COMPLEXITY-LOW)
- `[VERB]{1, [PARTITION]}` - try once, then re-partition (see Pattern 3)

### Pattern 3: DECOMPOSE-ON-FAIL (Adaptive Re-partitioning)

**Problem:** A task is too large or complex. Instead of retrying the same approach, break it down and retry with smaller pieces.

**Inspiration:** Shape Up "scope hammering", Agile story splitting.

**Notation:**
```
├─ [VERB]{1, DECOMPOSE-ON-FAIL}: description
│   └─ -FAIL → [PARTITION](current_task) → TASKS_[TOPIC].md
│            → foreach subtask: [VERB](subtask)
│            → [AGGREGATE] results
```

**Semantics:**
- On first failure, invoke [PARTITION] on the failing task
- [PARTITION] creates new TASKS plan with smaller chunks
- Execute each subtask independently
- Aggregate results back to parent context
- If any subtask fails, it can recursively DECOMPOSE-ON-FAIL

**Example: Complex implementation with auto-decomposition**
```
[IMPLEMENT] → [REFINE]: Build crawler module
├─ [IMPLEMENT]{1, DECOMPOSE-ON-FAIL}: implement_step_01
│   └─ -FAIL → [PARTITION](step_01)
│            → TASKS_CRAWLER_STEP01.md
│            ┌─ [IMPLEMENT] substep_01a -OK
│            ├─ [IMPLEMENT] substep_01b -OK
│            └─ [IMPLEMENT] substep_01c -OK
│            → [AGGREGATE] → step_01 -OK
├─ [TEST]
└─> Gate
```

**Combined with RETRY:**
```
├─ [IMPLEMENT]{3, DECOMPOSE-ON-FAIL}: complex_task
│   └─ -FAIL{1..3} → [FIX] (try to fix as-is)
│   └─ -FAIL{4} → [PARTITION] → subtasks → retry each
```

**Key insight:** This pattern acknowledges that failure often means "task too big" rather than "task impossible". Decomposition is a first-class recovery strategy.

### Transition State Machine

Complete state machine for verb execution:

```
                    ┌────────────────────────────────────┐
                    │                                    │
                    ▼                                    │
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌────────┴───┐
│ PENDING │────>│ RUNNING │────>│   OK    │────>│ NEXT-VERB  │
└─────────┘     └────┬────┘     └─────────┘     └────────────┘
                     │
                     │ -FAIL
                     ▼
                ┌─────────┐     retry_count < max?
                │  FAIL   │─────────────────────┐
                └────┬────┘                     │ yes
                     │ no                       ▼
                     │                   ┌─────────────┐
                     ▼                   │  RECOVERY   │
              ┌────────────┐             │ ([FIX] etc) │
              │ ON-EXHAUST │             └──────┬──────┘
              └─────┬──────┘                    │
                    │                           │
     ┌──────────────┼──────────────┐            │
     ▼              ▼              ▼            │
┌─────────┐  ┌───────────┐  ┌──────────┐        │
│[CONSULT]│  │[PARTITION]│  │[DEFER]   │        │ 
└─────────┘  └───────────┘  └──────────┘        │
                    │                           │
                    ▼                           │
             ┌───────────┐                      │
             │ SUBTASKS  │──────────────────────┘
             └───────────┘   (retry with smaller tasks)
```

### Phase-Level Transitions

Phases also have OK/FAIL states:

```
[PHASE]-OK:   All verbs completed, gate passed → transition to next phase
[PHASE]-FAIL: Gate failed after verb exhaustion → options:
              ├─ [CONSULT] with [ACTOR]
              ├─ [ITERATE] phase (reset and retry)
              └─ [ABORT] workflow
```

**Phase retry notation:**
```
[EXPLORE]{2} → [DESIGN]: Explore with max 2 phase iterations
├─ ... verbs ...
└─> Gate
    └─ -FAIL{1} → [ITERATE] [EXPLORE]
    └─ -FAIL{2} → [CONSULT] "Cannot pass EXPLORE gate"
```

## Escalation Patterns

Three patterns for handling -FAIL when retries are exhausted.

### Escalation 1: CONSULT (Human in the Loop)

**When:** Agent lacks knowledge, authority, or capability to proceed.

**Notation:**
```
├─ [VERB]{N, [CONSULT]}: description
│   └─ -FAIL{N+1} → [CONSULT] "reason for escalation"
```

**Behavior:**
- Pause execution
- Present situation to [ACTOR] (user)
- Wait for guidance or decision
- Resume with provided direction

**Example:**
```
├─ [IMPLEMENT]{3, [CONSULT]}: integrate payment API
│   └─ -FAIL{4} → [CONSULT] "API key rejected after 3 attempts. Need credentials check."
│                 ↓ user provides new key
│                 → [IMPLEMENT] resumes
```

**Best for:** External dependencies, permission issues, ambiguous requirements.

### Escalation 2: DEFER (Postpone and Continue)

**When:** Failure blocks one path but alternatives exist.

**Notation:**
```
├─ [VERB]{N, [DEFER]}: description
│   └─ -FAIL{N+1} → [DEFER](reason) → continue next verb
│                 → [BACKLOG] deferred item
```

**Behavior:**
- Mark verb as DEFERRED (not FAIL)
- Log reason and context to PROBLEMS.md
- Add to session backlog for later
- Continue with next verb in sequence
- Revisit deferred items before DELIVER gate

**Example:**
```
[IMPLEMENT] → [REFINE]
├─ [IMPLEMENT] core auth -OK
├─ [IMPLEMENT]{2, [DEFER]}: SSO integration
│   └─ -FAIL{3} → [DEFER] "IdP not responding, continue without SSO"
├─ [IMPLEMENT] session management -OK
├─ [TEST]
└─> Gate
    └─ [ ] All deferred items resolved or explicitly excluded
```

**Best for:** Non-blocking features, external service outages, time-boxed work.

### Escalation 3: ABORT (Fail Fast)

**When:** Failure is fundamental and continuing is wasteful.

**Notation:**
```
├─ [VERB]{N, [ABORT]}: description
│   └─ -FAIL{N+1} → [ABORT] "critical failure reason"
│                 → workflow terminates
```

**Behavior:**
- Stop all execution immediately
- Record failure state to PROBLEMS.md
- Do NOT proceed to next verb or phase
- Require explicit restart or new session

**Example:**
```
[EXPLORE] → [DESIGN]
├─ [ASSESS]{1, [ABORT]}: verify database access
│   └─ -FAIL{2} → [ABORT] "Cannot connect to production DB. Fix infrastructure first."
```

**Best for:** Infrastructure failures, invalid assumptions, corrupted state.

### Escalation Decision Matrix

```
┌─────────────────────────────────────────────────────────────────────┐
│                     Can continue without this verb?                 │
│                         YES                 NO                      │
├───────────────────────────────────────────────────────────────────┤
│ Human can help?  YES  → [DEFER] + [BACKLOG]   [CONSULT]            │
│                  NO   → [DEFER] + [BACKLOG]   [ABORT]              │
└─────────────────────────────────────────────────────────────────────┘
```

### Combined Example

```
[IMPLEMENT] → [REFINE]: Build notification system
├─ [IMPLEMENT]{3, [CONSULT]}: email service
│   └─ -FAIL{1..3} → [FIX]
│   └─ -FAIL{4} → [CONSULT] "SMTP config issue"
├─ [IMPLEMENT]{2, [DEFER]}: SMS notifications
│   └─ -FAIL{3} → [DEFER] "Twilio quota exceeded, proceed without SMS"
├─ [IMPLEMENT]{1, [ABORT]}: core message queue
│   └─ -FAIL{2} → [ABORT] "Message broker down, cannot continue"
├─ [TEST]
└─> Gate
```

## STRUT Examples

Progressive examples from minimal to comprehensive.

### Example 1: Simple (COMPLEXITY-LOW, single phase focus)

Hotfix workflow - fix a bug, test, commit.

```
[IMPLEMENT] → [DELIVER]: Fix null pointer in getUserById()
├─ [FIX]: Add null check before accessing user.email
├─ [TEST]: Run unit tests for UserService
├─ [COMMIT]: "fix(user): add null check in getUserById"
└─> Gate
    └─ [x] Bug no longer reproduces
    └─ [x] Tests pass
```

**Characteristics:**
- Single phase shown (others implicit)
- No retry logic needed
- No conditional branches
- Linear verb sequence

### Example 2: Medium (COMPLEXITY-MEDIUM, full BUILD workflow)

Add a new feature with spec and tests.

```
[EXPLORE] → [DESIGN]: Understand password reset requirements
├─ [ASSESS]-OK: COMPLEXITY-MEDIUM (3 files, email dependency)
├─ [ANALYZE]-OK: Existing auth module in src/auth/
├─ [GATHER]-OK: Requirements from ticket AUTH-123
└─> Gate
    └─ [x] Complexity assessed
    └─ [x] Existing code understood
    └─ [x] Requirements clear

[DESIGN] → [IMPLEMENT]: Plan password reset feature
├─ [PLAN]-OK: Token-based reset with 24h expiry
├─ [WRITE-SPEC]-OK: _SPEC_PASSWORD_RESET.md
├─ [WRITE-IMPL-PLAN]-OK: _IMPL_PASSWORD_RESET.md
└─> Gate
    └─ [x] SPEC created with FR/DD
    └─ [x] IMPL plan has steps

[IMPLEMENT] → [REFINE]: Build password reset
├─ [IMPLEMENT]-OK: ResetToken model
├─ [IMPLEMENT]-OK: /forgot-password endpoint
├─ [IMPLEMENT]-OK: /reset-password endpoint
├─ |: [TEST] → [FIX] if -FAIL :| ×3
├─ [COMMIT]-OK: "feat(auth): add password reset flow"
└─> Gate
    └─ [x] All endpoints working
    └─ [x] Tests pass

[REFINE] → [DELIVER]: Review and verify
├─ [VERIFY]-OK: Code matches SPEC
├─ [TEST]-OK: Integration tests pass
└─> Gate
    └─ [x] SPEC satisfied
    └─ [x] No regressions

[DELIVER]: Complete feature
├─ [VALIDATE]-OK: Manual test successful
├─ [CLOSE]-OK: Ticket AUTH-123 resolved
└─> Gate
    └─ [x] Feature delivered
```

### Example 3: Complex (with retries and escalation)

Build with bounded retries and escalation paths.

```
[IMPLEMENT] → [REFINE]: Build OAuth integration
├─ [IMPLEMENT]-OK: OAuth client wrapper
├─ [IMPLEMENT]{3, [CONSULT]}: OAuth callback handler
│   └─ -FAIL{1} → [FIX](typo_redirect_uri)
│   └─ -FAIL{2} → [FIX](missing_scope)
│   └─ -OK
├─ [IMPLEMENT]{2, [DEFER]}: Social login buttons
│   └─ -FAIL{1} → [FIX](css_issue)
│   └─ -FAIL{2} → [FIX](icon_loading)
│   └─ -FAIL{3} → [DEFER] "UI polish, defer to next sprint"
├─ |: [TEST] → [FIX] if -FAIL :| ×5
│   └─ -FAIL{6} → [CONSULT] "Tests still failing after 5 attempts"
├─ [COMMIT]-OK
└─> Gate
    └─ [x] Core OAuth working
    └─ [ ] Deferred: Social buttons (logged in PROBLEMS.md)
```

### Example 4: Nested (embedded SOLVE within BUILD)

Research decision needed mid-implementation.

```
[DESIGN] → [IMPLEMENT]: Design caching layer
├─ [PLAN]-OK: Need distributed cache
├─ ┌─ NEST(SOLVE:EVALUATION): "Redis vs Memcached?"
│  │  
│  │  [EXPLORE] → [DESIGN]: Evaluate cache options
│  │  ├─ [RESEARCH]-OK: Redis features (persistence, pub/sub)
│  │  ├─ [RESEARCH]-OK: Memcached features (simple, fast)
│  │  └─> Gate: [x] Options understood
│  │  
│  │  [DESIGN] → [IMPLEMENT]: Define criteria
│  │  ├─ [DEFINE]-OK: Need pub/sub for invalidation
│  │  ├─ [DEFINE]-OK: Need persistence for session data
│  │  └─> Gate: [x] Criteria defined
│  │  
│  │  [IMPLEMENT] → [DELIVER]: Evaluate and decide
│  │  ├─ [EVALUATE]-OK: Redis meets all criteria
│  │  ├─ [EVALUATE]-OK: Memcached fails persistence requirement
│  │  ├─ [RECOMMEND]-OK: Use Redis
│  │  └─> Gate: [x] Decision made
│  │  
│  └─ END NEST → cache_choice = "Redis"
│
├─ [WRITE-SPEC](cache_choice)-OK: Redis caching spec
├─ [WRITE-IMPL-PLAN]-OK: Redis integration steps
└─> Gate
    └─ [x] Cache technology selected
    └─ [x] Design complete
```

### Example 5: Comprehensive (all features)

Full workflow with nesting, retries, escalation, repetition, and decomposition.

```
[EXPLORE] → [DESIGN]: Build payment processing system
├─ [ASSESS]-OK: COMPLEXITY-HIGH (external API, PCI compliance)
├─ [ANALYZE]+: Existing billing code (3 iterations)
├─ [RESEARCH]?: PCI-DSS requirements (optional, skipped - team has docs)
├─ [GATHER]-OK: Requirements from JIRA PAY-001
└─> Gate
    └─ [x] COMPLEXITY-HIGH confirmed
    └─ [x] PCI requirements understood

[DESIGN] → [IMPLEMENT]: Design payment architecture
├─ [PLAN]-OK: Stripe integration with tokenization
├─ ┌─ NEST(SOLVE:EVALUATION): "Stripe vs Braintree vs Adyen?"
│  │  ├─ [RESEARCH]* providers
│  │  ├─ [EVALUATE] against criteria
│  │  ├─ [RECOMMEND]-OK: Stripe (best docs, PCI Level 1)
│  │  └─ END NEST → provider = "Stripe"
│  └─
├─ [WRITE-SPEC]-OK: _SPEC_PAYMENTS.md [PAY-SP01]
├─ [PROVE]{1, [CONSULT]}: POC Stripe integration
│   └─ -OK (POC successful)
├─ [WRITE-IMPL-PLAN]-OK: _IMPL_PAYMENTS.md [PAY-IP01]
├─ [WRITE-TEST-PLAN]-OK: _TEST_PAYMENTS.md [PAY-TP01]
└─> Gate
    └─ [x] SPEC with PAY-FR-01..FR-12
    └─ [x] POC validates approach
    └─ [x] IMPL plan ready

[IMPLEMENT]{2} → [REFINE]: Build payment system
├─ [IMPLEMENT]{1, DECOMPOSE-ON-FAIL}: Stripe client
│   └─ -FAIL → [PARTITION] → 3 subtasks
│            ├─ [IMPLEMENT] StripeConfig -OK
│            ├─ [IMPLEMENT] StripeClient -OK
│            └─ [IMPLEMENT] StripeWebhooks -OK
│            → [AGGREGATE] -OK
├─ [IMPLEMENT]{3, [CONSULT]}: Payment processing
│   └─ -FAIL{1..3} → [FIX]
│   └─ -OK
├─ [IMPLEMENT]{2, [DEFER]}: Subscription billing
│   └─ -FAIL{3} → [DEFER] "Phase 2 feature"
├─ |: [TEST] → [FIX] if -FAIL :| ×5
│   └─ -FAIL{6} → [CONSULT]
├─ 𝄋 checkpoint_tests_pass
├─ [IMPLEMENT]{1, [ABORT]}: PCI audit logging
│   └─ -FAIL{2} → [ABORT] "Cannot proceed without audit trail"
├─ [TEST]-OK: Verify audit logs
├─ D.S. checkpoint_tests_pass if audit -FAIL
├─ [COMMIT]-OK: "feat(payments): add Stripe integration"
└─> Gate
    └─ [x] PAY-FR-01..FR-10 satisfied
    └─ [ ] PAY-FR-11 (subscriptions) → DEFERRED
    └─ [x] PAY-FR-12 (audit) satisfied
    └─ -FAIL{1} → [ITERATE] [IMPLEMENT]
    └─ -FAIL{2} → [CONSULT] "Cannot pass IMPLEMENT gate"

[REFINE] → [DELIVER]: Review and harden
├─ [REVIEW]-OK: Code review passed
├─ [VERIFY]-OK: All FR satisfied (except deferred)
├─ [TEST]-OK: Load testing passed
├─ ([CRITIQUE] | [SECURITY-AUDIT]): Choose verification method
│   └─ [SECURITY-AUDIT]-OK: No vulnerabilities found
├─ [RECONCILE]-OK: Addressed review findings
└─> Gate
    └─ [x] Security audit passed
    └─ [x] Performance acceptable
    └─ [x] DEFERRED items logged

[DELIVER]: Release payment system
├─ [VALIDATE]-OK: Staging environment test
├─ [MERGE]-OK: PR #456 merged
├─ [DEPLOY]?: Production deploy (if authorized)
│   └─ [CONSULT] "Ready for production?"
│   └─ user: "Yes, deploy"
│   └─ [DEPLOY]-OK
├─ [CLOSE]-OK: JIRA PAY-001 resolved
└─> Gate
    └─ [x] Production deployed
    └─ [x] Documentation updated
    └─ [x] Handoff complete
```

### Example Legend

| Symbol | Meaning |
|--------|---------|
| `-OK` | Completed successfully |
| `-FAIL` | Failed, needs recovery |
| `-PARTIAL` | Partially complete |
| `-SKIP` | Intentionally skipped |
| `{N}` | Max N retries |
| `{N, [ESC]}` | Retry N times, then escalate |
| `×N` | Repeat block N times |
| `+` | One or more |
| `*` | Zero or more |
| `?` | Optional |
| `\|: :\|` | Repeat until condition |
| `𝄋` | Named checkpoint |
| `D.S.` | Jump to checkpoint |
| `NEST()` | Embedded sub-workflow |
| `( \| )` | Choice between options |

## Document History

**[2026-01-17 16:00]**
- Added: STRUT Examples section
- Example 1: Simple (hotfix)
- Example 2: Medium (full BUILD)
- Example 3: Complex (retries/escalation)
- Example 4: Nested (embedded SOLVE)
- Example 5: Comprehensive (all features)
- Added: Example legend

**[2026-01-17 15:50]**
- Added: Escalation Patterns section
- Escalation 1: CONSULT - human in the loop
- Escalation 2: DEFER - postpone and continue
- Escalation 3: ABORT - fail fast
- Added: Escalation decision matrix
- Added: Combined example showing all three patterns

**[2026-01-17 15:45]**
- Added: Advanced Control Flow Patterns section
- Pattern 1: NEST - nested workflow invocation
- Pattern 2: RETRY - bounded retry with escalation
- Pattern 3: DECOMPOSE-ON-FAIL - adaptive re-partitioning
- Added: Verb transition state machine diagram
- Added: Phase-level OK/FAIL transitions

**[2026-01-17 15:30]**
- Added: Repetition Notation Research section
- Sources: Musical notation (Wikipedia), EBNF (cs.man.ac.uk), Process algebra (Wikipedia)
- Proposed STRUT notation for repetition, loops, jumps, and choice

**[2026-01-17 15:20]**
- Initial research document created
- Analyzed DevSystem workflows and SharePoint-GPT-Middleware specs
- Defined 3 use cases: planning, execution, resume
- Proposed STRUT format with 8 features and 5 design decisions
