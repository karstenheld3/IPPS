<DevSystem MarkdownTablesAllowed=true />

# INFO: Project Phases and Workflow Terminology

**Doc ID**: PHSE-IN01
**Goal**: Research proven phase/stage terminology from industry frameworks for DevSystem workflow markers
**Timeline**: Created 2026-01-15, 2 updates

## Summary

**Key Findings (copy/paste ready):**

**Recommended Stage Model (D-S-I-I-D):**
- **DISCOVERY** - Understand the problem (research, investigate, validate assumptions)
- **DESIGN** - Plan the solution (specs, plans, POCs, test plans)
- **IMPLEMENT** - Build the solution (code, integrate)
- **IMPROVE** - Refine and verify (review, critique, fix)
- **DELIVER** - Ship and close (deploy, merge, handoff)

**Industry Terminology Worth Stealing:**
- ITIL: "Service Transition" (moving from design to operation) [VERIFIED]
- PRINCE2: "Initiate" vs "Control" vs "Close" (clear gate terminology) [VERIFIED]
- Shape Up: "Shaping" (pre-implementation design work) [VERIFIED]
- Double Diamond: "Discover/Define/Develop/Deliver" (4D model) [VERIFIED]
- Scrum: "Planning/Review/Retrospective" (inspect-adapt cycle) [VERIFIED]

**Phase Completion Terminology:**
- ITIL: Uses "gates" between stages
- PRINCE2: "Authorization" to proceed
- Scrum: "Done" with Definition of Done
- Shape Up: "Shipped" or "Cut"

## Table of Contents

- Summary
- Framework Comparison
- ITIL Service Lifecycle
- PRINCE2 Project Phases
- Shape Up (Basecamp)
- Scrum Events
- Double Diamond
- Classic SDLC
- Agile SDLC
- Synthesis and Recommendations
- FEATURE-BASED Phase Hierarchy
  - Complexity Assessment
  - Phase-Verb Mapping
  - Complexity-Based Flow
  - Phase Transition Gates
  - Verb Outcome Transitions
- PROBLEM-BASED Phase Hierarchy
- Sources
- Document History

## Framework Comparison

### High-Level Stage Mapping

**ITIL v3 (Information Technology Infrastructure Library)** (5 stages):
- Service Strategy → Service Design → Service Transition → Service Operation → Continual Improvement

**PRINCE2 (Projects IN Controlled Environments)** (7 processes):
- Starting Up → Initiating → Directing → Controlling Stage → Managing Delivery → Managing Boundaries → Closing

**Shape Up** (3 parts):
- Shaping → Betting → Building

**Double Diamond** (4 phases):
- Discover → Define → Develop → Deliver

**Scrum** (sprint cycle):
- Planning → Daily Work → Review → Retrospective

**Classic SDLC** (7 phases):
- Planning → Requirements → Design → Coding → Testing → Deployment → Maintenance

**Agile SDLC** (5 phases):
- Ideation → Development → Testing → Deployment → Operations

## ITIL Service Lifecycle

**Source**: ITIL v3 Framework (Information Technology Infrastructure Library)

### Five Stages

**Stage 1: Service Strategy**
- Purpose: Set long-term service goals, align IT with business objectives
- Activities: Determine which services to offer, evaluate market needs, plan investments
- Key processes: Portfolio management, financial management, demand management

**Stage 2: Service Design**
- Purpose: Translate strategy into practical blueprints
- Activities: Plan new/updated services, consider capacity, performance, security
- Key processes: Catalog management, availability management, capacity management

**Stage 3: Service Transition**
- Purpose: Manage change from development to live operation
- Activities: Test, deploy, integrate with minimal disruption
- Key processes: Change management, release management, configuration management
- **Notable**: This is the "ready for production" gate

**Stage 4: Service Operation**
- Purpose: Day-to-day delivery and support
- Activities: Incident management, problem management, access control
- Focus: Keep services available, resolve issues promptly

**Stage 5: Continual Service Improvement (CSI)**
- Purpose: Continuous feedback loop throughout lifecycle
- Activities: Measure, review, implement improvements
- Philosophy: "You can never be perfect, keep improving"

### ITIL Terminology Worth Adopting

- **Transition** - Moving from design to operation (clear gate concept)
- **Operation** - Running state after deployment
- **Continual Improvement** - Never-ending refinement cycle

## PRINCE2 Project Phases

**Source**: PRINCE2 (Projects IN Controlled Environments)

### Seven Processes

**1. Starting Up a Project (SU)**
- Pre-project phase, triggered by project mandate
- Purpose: Verify project is worthwhile
- Output: Project Brief
- Gate: Project Board decides whether to initiate

**2. Initiating a Project (IP)**
- First official stage
- Purpose: Define quality, timeline, costs, risks, resources
- Output: Project Initiation Documentation (PID)
- Gate: Authorization to start

**3. Directing a Project (DP)**
- Runs throughout project
- Purpose: Project Board oversight and decisions
- Activities: Authorize stages, provide guidance, handle exceptions

**4. Controlling a Stage (CS)**
- Day-to-day management within a stage
- Activities: Assign work, check quality, track progress
- Output: Highlight reports, issue logs, risk registers

**5. Managing Product Delivery (MP)**
- Actual work execution
- Purpose: Deliver products as specified
- Output: Work packages, checkpoint reports

**6. Managing a Stage Boundary (SB)**
- Transition between stages
- Purpose: Review stage, plan next stage
- Output: End Stage Report, next stage plan
- Gate: Authorization to proceed

**7. Closing a Project (CP)**
- Final stage
- Activities: Formal handover, lessons learned, closure
- Output: End Project Report

### PRINCE2 Terminology Worth Adopting

- **Initiate** vs **Start Up** - Clear distinction between pre-work and official start
- **Control** - Active management during execution
- **Stage Boundary** - Explicit transition/gate concept
- **Close** - Formal completion with handover

## Shape Up (Basecamp)

**Source**: Shape Up methodology by Basecamp (Ryan Singer)

### Three Parts

**Part 1: Shaping**
- Pre-implementation design work
- Properties: Rough (not detailed), Solved (addresses core problem), Bounded (fixed appetite)
- Activities: Set boundaries, find elements, identify risks/rabbit holes, write pitch
- Output: Pitch document with Problem, Appetite, Solution, Rabbit Holes, No-Gos

**Part 2: Betting**
- Decision-making about what to build
- Philosophy: "Bets, not backlogs" - no infinite todo lists
- Activities: Six-week cycles, cool-down periods, betting table decisions
- Modes: R&D mode, Production mode, Cleanup mode

**Part 3: Building**
- Execution phase
- Philosophy: "Done means deployed"
- Activities: Hand over responsibility, get one piece done, map scopes, show progress
- Tracking: Hill charts (uphill = figuring out, downhill = executing)

### Shape Up Terminology Worth Adopting

- **Shaping** - Pre-implementation design work (distinct from coding)
- **Appetite** - Fixed time budget (vs variable scope)
- **Pitch** - Proposal document with clear boundaries
- **Cool-down** - Recovery/cleanup period between cycles
- **Hill Chart** - Progress visualization (uncertainty → certainty)
- **Scope Hammering** - Cutting scope to fit time

## Scrum Events

**Source**: Scrum Guide 2020

### Sprint Cycle

**Sprint Planning**
- Purpose: Lay out work for the sprint
- Topics: Why valuable? What can be done? How will it get done?
- Output: Sprint Goal, Sprint Backlog
- Timebox: Max 8 hours for 1-month sprint

**Daily Scrum**
- Purpose: Inspect progress, adapt plan
- Focus: Progress toward Sprint Goal, actionable plan for next day
- Timebox: 15 minutes

**Sprint Review**
- Purpose: Inspect outcome, determine future adaptations
- Activities: Present results, discuss progress, collaborate on next steps
- Focus: Working session, not just presentation
- Timebox: Max 4 hours for 1-month sprint

**Sprint Retrospective**
- Purpose: Plan ways to increase quality and effectiveness
- Activities: Inspect what went well, what problems occurred, identify improvements
- Output: Improvement actions (may add to next Sprint Backlog)
- Timebox: Max 3 hours for 1-month sprint

### Scrum Terminology Worth Adopting

- **Planning** - Explicit planning phase before work
- **Review** - Inspect outcomes with stakeholders
- **Retrospective** - Self-improvement reflection
- **Definition of Done** - Clear completion criteria
- **Increment** - Usable output from each sprint

## Double Diamond

**Source**: British Design Council (2005)

### Four Phases

**Discover (Divergent)**
- Purpose: Understand the issue, not assume
- Activities: Speak to affected people, gather insights
- Mindset: Expand understanding

**Define (Convergent)**
- Purpose: Define challenge based on discovery
- Activities: Synthesize insights, reframe problem
- Output: Clear problem statement

**Develop (Divergent)**
- Purpose: Give different answers to defined problem
- Activities: Seek inspiration, co-design with different people
- Mindset: Multiple solutions for one problem

**Deliver (Convergent)**
- Purpose: Test solutions at small scale, improve
- Activities: Prototype, test, refine, reject non-working solutions
- Output: Validated solution

### Double Diamond Terminology Worth Adopting

- **Discover/Define/Develop/Deliver** - 4D model, clear progression
- **Divergent/Convergent** - Expand then focus pattern
- **Two Diamonds** - First diamond = right problem, second diamond = right solution

## Classic SDLC (Software Development Life Cycle)

**Source**: Traditional Software Development Life Cycle

### Seven Phases

**1. Planning**
- Define purpose and scope
- Feasibility study
- Output: Project Plan, Software Requirement Specification (SRS)

**2. Requirements Analysis**
- Gather user expectations
- Distinguish essential from desirable features
- Output: Requirements Specification Document

**3. Design**
- Build framework, outline structure
- Data flow diagrams, UI mockups, system dependencies
- Output: Software Design Document (SDD)

**4. Coding (Implementation)**
- Convert design to code
- Code reviews, preliminary testing
- Output: Functional software

**5. Testing**
- Quality inspection
- Unit, integration, system, acceptance testing
- Cycle: Test → Find bugs → Fix → Retest

**6. Deployment**
- Roll out to end-users
- Methods: Big Bang, Blue-Green, Canary
- Includes: User manuals, training

**7. Maintenance**
- Ongoing support and improvement
- Respond to feedback, fix issues, upgrade
- Long-term: Renovation or phase-out decisions

## Agile SDLC

**Source**: Mendix/Industry Standard

### Five Stages

**1. Ideation**
- Define purpose and goal
- Document requirements
- Prioritize tasks, allocate resources

**2. Development**
- Build first iteration
- Includes UX/UI design, architecture, coding
- Often longest stage

**3. Testing**
- Verify functionality before release
- Check code cleanliness, address bugs, trial runs
- Quick feedback loops

**4. Deployment**
- Push to production
- Security assessments, documentation updates
- Software is live and accessible

**5. Operations**
- Ongoing maintenance
- Squash bugs, improve features
- Collect feedback for future iterations

## Synthesis and Recommendations

### Mapping to Proposed Model

Proposed: DISCOVERY → DESIGN → IMPLEMENT → IMPROVE → DELIVER

**Framework Support:**

| Stage | ITIL | PRINCE2 | Shape Up | Double Diamond | SDLC |
|------------|------|---------|----------|----------------|------|
| DISCOVERY | Strategy | Starting Up, Initiating | Shaping | Discover, Define | Planning, Requirements |
| DESIGN | Design | Initiating | Shaping | Define, Develop | Design |
| IMPLEMENT | Transition | Controlling, Delivery | Building | Develop | Coding, Testing |
| IMPROVE | CSI | Managing Boundaries | Cool-down | Deliver | Testing |
| DELIVER | Operation | Closing | Ship | Deliver | Deployment |

### Recommended Phase Markers

**Stage Markers (high-level):**
- `[DISCOVERY]` - Research phase
- `[DESIGN]` - Planning phase (includes POCs)
- `[IMPLEMENT]` - Execution phase
- `[IMPROVE]` - Refinement phase
- `[DELIVER]` - Completion phase

**Completion Markers:**
- `-OK` suffix recommended (concise, positive)
- Alternative: `-DONE` or `-COMPLETE`
- PRINCE2 style: `-AUTHORIZED` (gate passed)

### Alternative Stage Names Considered

For IMPROVE stage (to avoid I-I collision):
- **REFINE** (R) - Polish and improve
- **REVIEW** (R) - Inspect and adapt
- **HARDEN** (H) - Make robust
- **POLISH** (P) - Final touches

For unique letter mnemonics:
- D-S-I-R-L: Discovery, deSign, Implement, Refine, deLiver
- D-S-I-H-L: Discovery, deSign, Implement, Harden, deLiver

### Bugfix vs Feature Workflows

**Features** (full cycle):
```
DISCOVERY → DESIGN (spec + plan + test plan) → IMPLEMENT → IMPROVE → DELIVER
```

**Problems/Bugfixes** (abbreviated):
```
DISCOVERY → DESIGN (POC proves fix) → IMPLEMENT → IMPROVE → DELIVER
```

The DESIGN phase scales based on work type - heavy for features, light for fixes.

**See also:** `_INFO_AGENTIC_ENGLISH.md [AGEN-IN01]` for verb definitions, syntax, and placeholders.

## FEATURE-BASED Phase Hierarchy

### Complexity Assessment (First Step)

```
[DISCOVERY]
├─> [ASSESS] complexity level (maps to semver):
│   ├─> COMPLEXITY-LOW: Single file, clear scope, no dependencies → patch version
│   ├─> COMPLEXITY-MEDIUM: Multiple files, some dependencies, backward compatible → minor version
│   └─> COMPLEXITY-HIGH: Breaking changes, new patterns, external APIs, architecture → major version
```

### Phase-Verb Mapping by Complexity

```
[DISCOVERY] ─────────────────────────────────────────────────────────────────
├─> [RESEARCH] - Explore existing solutions, docs, patterns
├─> [ANALYZE] - Study affected code and dependencies
├─> [ASSESS] - Determine complexity level (COMPLEXITY-LOW/MEDIUM/HIGH)
├─> [CONSULT] - Collect requirements, clarify scope with [ACTOR] (if MEDIUM+)
└─> [DECIDE] - Confirm approach before proceeding

[DESIGN] ────────────────────────────────────────────────────────────────────
├─> [PLAN] - Create structured approach
├─> [OUTLINE] - High-level structure (all)
├─> [SPEC] - Write specification (if MEDIUM+)
├─> [PROVE] - POC for risky parts (if HIGH)
├─> [PROPOSE] - Present options to [ACTOR] (if HIGH)
├─> [VALIDATE] - Confirm design with [ACTOR]
├─> [WRITE-IMPL](SPEC) - Create IMPL plan from spec (if MEDIUM+)
└─> [WRITE-TEST](SPEC) - Create TEST plan from spec (if HIGH)

[IMPLEMENT] ─────────────────────────────────────────────────────────────────
├─> [IMPLEMENT] - Write code
├─> [CONFIGURE] - Environment/settings (if needed)
├─> [INTEGRATE] - Connect components (if MEDIUM+)
├─> [TEST] - Run tests during implementation
├─> [REFACTOR] - Clean up as needed
└─> [COMMIT] - Small, frequent commits

[IMPROVE] ───────────────────────────────────────────────────────────────────
├─> [REVIEW] - Self-review implementation
├─> [VERIFY] - Check against spec/rules
├─> [CRITIQUE] - Devil's advocate (if HIGH)
├─> [RECONCILE] - Pragmatic programmer (if HIGH)
├─> [FIX] - Address found issues
├─> [OPTIMIZE] - Performance improvements (if needed)
└─> [IMPROVE] - Quality enhancements

[DELIVER] ───────────────────────────────────────────────────────────────────
├─> [TEST] - Final test pass
├─> [VALIDATE] - [ACTOR] acceptance
├─> [MERGE] - Combine branches
├─> [DEPLOY] - Push to environment
├─> [FINALIZE] - Documentation, cleanup
├─> [HANDOFF] - Transfer/communicate
├─> [CLOSE] - Mark done, sync tracking
└─> [ARCHIVE] - Archive if session-based
```

### Complexity-Based Flow

```
COMPLEXITY-LOW:    DISCOVERY(lite) → DESIGN(outline) → IMPLEMENT → IMPROVE(review) → DELIVER    [patch]
COMPLEXITY-MEDIUM: DISCOVERY → DESIGN(spec) → IMPLEMENT → IMPROVE(verify) → DELIVER             [minor]
COMPLEXITY-HIGH:   DISCOVERY(full) → DESIGN(spec+POC+plans) → IMPLEMENT → IMPROVE(full) → DELIVER [major]
```

### Phase Transition Gates

```
DISCOVERY → DESIGN gate:
├─> [ ] Problem/requirement clearly understood
├─> [ ] Complexity level assessed
└─> [ ] Scope confirmed with [ACTOR] (if MEDIUM+)

DESIGN → IMPLEMENT gate:
├─> [ ] Approach documented (outline, spec, or plan)
├─> [ ] Risky parts proven via POC (if HIGH)
├─> [ ] No open questions requiring [ACTOR] decision
└─> [ ] Test strategy defined (if MEDIUM+)

IMPLEMENT → IMPROVE gate:
├─> [ ] All planned code changes complete
├─> [ ] Tests pass
└─> [ ] No TODO/FIXME left unaddressed

IMPROVE → DELIVER gate:
├─> [ ] Self-review complete
├─> [ ] Verification against spec/rules passed
└─> [ ] All found issues fixed
```

### Verb Outcome Transitions

```
[RESEARCH]-OK   → [ANALYZE]
[RESEARCH]-FAIL → [CONSULT] (need help finding info)

[ASSESS]-OK     → [CONSULT] or [DECIDE]
[ASSESS]-FAIL   → [RESEARCH] (need more context)

[PROVE]-OK      → [SPEC] or [IMPLEMENT]
[PROVE]-FAIL    → [RESEARCH] (back to discovery)

[CRITIQUE]-OK   → [RECONCILE]
[CRITIQUE]-FAIL → [FIX] (immediate issues found)

[VERIFY]-OK     → next phase
[VERIFY]-FAIL   → [FIX] → [VERIFY] (loop until OK)

[VALIDATE]-OK   → proceed
[VALIDATE]-FAIL → [CONSULT] (clarify requirements)
```

## PROBLEM-BASED Phase Hierarchy

Applies to: Bugfixes, chores, migrations, reviews, deployments, hotfixes.

### Problem Type Assessment (First Step)

```
[DISCOVERY]
├─> [ASSESS] problem type:
│   ├─> HOTFIX: Production down, immediate action required
│   ├─> BUGFIX: Defect in existing functionality
│   ├─> CHORE: Maintenance, cleanup, dependency updates
│   ├─> MIGRATION: Data or system migration
│   ├─> REVIEW: Code review, security audit, compliance check
│   └─> ASSESSMENT: Analyze options for meeting requirement (output: INFO)
```

### Phase-Verb Mapping by Problem Type

```
[DISCOVERY] ─────────────────────────────────────────────────────────────────
├─> [ANALYZE] - Identify root cause, reproduce issue
├─> [RESEARCH] - Find similar issues, known solutions
├─> [ASSESS] - Determine problem type and severity
├─> [GATHER] - Collect logs, error messages, context
└─> [DECIDE] - Confirm fix approach

[DESIGN] ────────────────────────────────────────────────────────────────────
├─> [OUTLINE] - Quick fix plan (HOTFIX/BUGFIX)
├─> [PROVE] - POC to verify fix works
├─> [PLAN] - Migration/rollback plan (if MIGRATION)
├─> [CONSULT] - Get approval for risky changes
└─> [VALIDATE] - Confirm approach addresses root cause

[IMPLEMENT] ─────────────────────────────────────────────────────────────────
├─> [FIX] - Apply the fix
├─> [REFACTOR] - Clean up related code (if CHORE)
├─> [CONFIGURE] - Update settings (if needed)
├─> [TEST] - Verify fix works, no regressions
└─> [COMMIT] - Small, focused commits

[IMPROVE] ───────────────────────────────────────────────────────────────────
├─> [REVIEW] - Self-review the fix
├─> [VERIFY] - Confirm root cause addressed
├─> [TEST] - Regression testing
└─> [IMPROVE] - Add safeguards to prevent recurrence

[DELIVER] ───────────────────────────────────────────────────────────────────
├─> [MERGE] - Merge fix
├─> [DEPLOY] - Deploy to affected environment
├─> [VALIDATE] - Confirm fix in production
├─> [STATUS] - Report resolution
├─> [CLOSE] - Mark issue resolved
└─> [ARCHIVE] - Document lessons learned (if significant)
```

### Problem-Type Flow

```
HOTFIX:     DISCOVERY(fast) → DESIGN(POC) → IMPLEMENT(fix) → IMPROVE(verify) → DELIVER(urgent)
BUGFIX:     DISCOVERY → DESIGN(POC) → IMPLEMENT → IMPROVE(review) → DELIVER
CHORE:      DISCOVERY(lite) → DESIGN(outline) → IMPLEMENT → IMPROVE(verify) → DELIVER
MIGRATION:  DISCOVERY → DESIGN(plan+rollback) → IMPLEMENT(staged) → IMPROVE(full) → DELIVER(staged)
REVIEW:     DISCOVERY → DESIGN(checklist) → [CRITIQUE] → [RECONCILE] → DELIVER(report)
ASSESSMENT: DISCOVERY(full) → [RESEARCH] → [ANALYZE] → [PROPOSE] → DELIVER(INFO doc)
```

## Sources

**ITIL Service Lifecycle:**
- `PHSE-IN01-SC-INVGT-ITILSVC` - invgate.com/itsm/itil/itil-service-lifecycle
- Primary findings: 5 stages (Strategy, Design, Transition, Operation, CSI), gate-based progression

**PRINCE2 Processes:**
- `PHSE-IN01-SC-P2WIKI-PROC` - prince2.wiki/processes/
- Primary findings: 7 processes, clear initiation vs control vs close terminology

**Shape Up:**
- `PHSE-IN01-SC-BCAMP-SHPUP` - basecamp.com/shapeup
- Primary findings: Shaping/Betting/Building, fixed time variable scope, cool-down periods

**Scrum Guide:**
- `PHSE-IN01-SC-SCRUM-GUIDE` - scrumguides.org/scrum-guide.html
- Primary findings: Planning/Review/Retrospective cycle, Definition of Done

**Double Diamond:**
- `PHSE-IN01-SC-WIKI-DBLDMD` - en.wikipedia.org/wiki/Double_Diamond_(design_process_model)
- Primary findings: Discover/Define/Develop/Deliver, divergent/convergent thinking

**SDLC Phases:**
- `PHSE-IN01-SC-HARNS-SDLC` - harness.io/blog/software-development-life-cycle-phases
- Primary findings: 7 phases (Planning through Maintenance), various models

**Agile SDLC:**
- `PHSE-IN01-SC-MENDX-AGILE` - mendix.com/blog/agile-software-development-lifecycle-stages/
- Primary findings: 5 stages (Ideation, Development, Testing, Deployment, Operations)

## Document History

**[2026-01-15 16:46]**
- Moved: Atomic Activities section to `_INFO_AGENTIC_ENGLISH.md [AGEN-IN01]`
- Added: Reference to new document

**[2026-01-15 16:40]**
- Added: WRITE verb variants ([WRITE-INFO], [WRITE-SPEC], [WRITE-IMPL], [WRITE-TEST])
- Added: [VERB-VARIANT] and [VERB](input) syntax patterns
- Changed: Updated DESIGN phase to use [WRITE-IMPL](SPEC) and [WRITE-TEST](SPEC)

**[2026-01-15 16:31]**
- Added: Syntax explanation section in Summary

**[2026-01-15 16:29]**
- Changed: Added COMPLEXITY- prefix to all complexity levels

**[2026-01-15 16:28]**
- Changed: Complexity levels from 4 (SIMPLE/MODERATE/COMPLEX/CRITICAL) to 3 (LOW/MEDIUM/HIGH)
- Added: Semver mapping (LOW→patch, MEDIUM→minor, HIGH→major)

**[2026-01-15 16:24]**
- Added: [ACTOR] placeholder (decision-making entity, default: user, in /go-autonomous: agent)
- Added: Verb outcome markers ([VERB]-OK, [VERB]-FAIL, [VERB]-SKIP)
- Added: Phase Transition Gates section
- Added: Verb Outcome Transitions section
- Changed: Replaced all "user" references with [ACTOR]

**[2026-01-15 16:05]**
- Added: ASSESSMENT problem type (output: INFO doc with options)

**[2026-01-15 16:03]**
- Added: PROBLEM-BASED Phase Hierarchy with problem type assessment
- Added: Problem-type flows (HOTFIX, BUGFIX, CHORE, MIGRATION, REVIEW)

**[2026-01-15 16:02]**
- Added: FEATURE-BASED Phase Hierarchy with complexity assessment
- Added: Phase-verb mapping and complexity-based flows

**[2026-01-15 15:37]**
- Fixed: Added DevSystem tag for table allowance
- Fixed: Expanded acronyms (ITIL, PRINCE2, SDLC, POC)
- Fixed: Updated Timeline with update count

**[2026-01-15 15:35]**
- Added: Atomic Activities (Verbs) section with reusable activity markers

**[2026-01-15 14:45]**
- Initial research document created
- Added: ITIL, PRINCE2, Shape Up, Scrum, Double Diamond, SDLC findings
- Added: Synthesis and recommendations section
