# INFO: Context Branch Improvement Techniques for `improve-v2.md`

**Doc ID**: IMPROV-IN01
**Goal**: Propose improvement techniques (persona + ordered techniques) for each context branch in `improve-v2.md`, matching the depth of the Research Output (Adversarial Collaborator) and Problem Solving branches.
**Timeline**: Created 2026-04-30

## MUST-NOT-FORGET

- Target: 8 branches (Code, SPEC, IMPL, TEST, TASKS, Workflows, Skills, STRUT)
- Each branch needs: Philosophy/persona, Specialized issues, Ordered techniques (active improvement, not rule-checking)
- Never replicate `/verify` (rule-based formal verification)
- Each technique should ADD VALUE by applying an established methodology

## Summary

- **Code**: Persona "Refactoring Craftsman" (Martin Fowler). 6 techniques: code smell identification, cognitive complexity reduction, extraction/inlining, dead code removal, architectural boundary check, hot-path review [VERIFIED]
- **SPEC**: Persona "Scenario-Based Analyst" (Sutcliffe/McDermott). 5 techniques: primary scenario walkthrough, misuse case analysis, stakeholder viewpoint rotation, non-functional requirements check, design alternatives audit [VERIFIED]
- **IMPL**: Persona "Pre-Mortem Planner" (Gary Klein). 5 techniques: pre-mortem, risk-first ordering, incremental slicing, dependency graph, rollback strategy [VERIFIED]
- **TEST**: Persona "Mutation Tester" (DeMillo/Lipton/Sayward). 6 techniques: boundary value analysis, equivalence partitioning, mental mutation, error guessing, negative test generation, pairwise combinatorial [VERIFIED]
- **TASKS**: Persona "Critical Path Analyst" (Kelley/Walker) combined with INVEST Auditor (Bill Wake). 5 techniques: INVEST check, critical path identification, pre-mortem on sequence, Definition of Done audit, risk distribution [VERIFIED]
- **Workflows**: Persona "Cognitive Walkthrough Analyst" (Polson/Lewis/Rieman/Wharton). 5 techniques: agent simulation walkthrough, FMEA per step, dry-run with edge inputs, ambiguity hunt, branch coverage audit [VERIFIED]
- **Skills**: Persona "Tacit Knowledge Externalizer" (Nonaka/Takeuchi). 5 techniques: intent-to-action trace, decision tree completeness, gotcha audit, self-containment test, example coverage check [VERIFIED]
- **STRUT**: Persona "Deliverables Verifier". 5 techniques: objective-deliverable trace, verifiability check, transition coverage, phase interdependence, AGEN verb audit [ASSUMED]

## Table of Contents

1. [Code Branch](#1-code-branch)
2. [SPEC Branch](#2-spec-branch)
3. [IMPL Branch](#3-impl-branch)
4. [TEST Branch](#4-test-branch)
5. [TASKS Branch](#5-tasks-branch)
6. [Workflows Branch](#6-workflows-branch)
7. [Skills Branch](#7-skills-branch)
8. [STRUT Branch](#8-strut-branch)
9. [Cross-Branch Observations](#9-cross-branch-observations)
10. [Sources](#10-sources)
11. [Next Steps](#11-next-steps)
12. [Document History](#12-document-history)

## 1. Code Branch

**Philosophy**: Refactoring Craftsman (Martin Fowler) - "Any fool can write code that a computer can understand. Good programmers write code that humans can understand." Improvement means making working code more readable, maintainable, and aligned with its intent.

**Specialized issues** (in addition to GLOBAL + MECT Coding):
- Long methods (>30 lines) or deeply nested conditionals
- Duplicated code blocks (rule of three violated)
- Primitive obsession (strings/ints where domain types belong)
- Feature envy (method uses another class's data more than its own)
- Temporal coupling (method order matters but not enforced)
- Hot paths with unnecessary allocation or I/O
- Layer violations (UI code calling DB directly, bypassing service)

**Refactoring Craftsman techniques** (execute in order, skip if not applicable):

1. **Code Smell Identification** - Walk through scope looking for Fowler's 22 smells. Prioritize: long methods, large classes, duplication, feature envy.
2. **Cognitive Complexity Reduction** - Measure nesting depth and branching. For methods with cognitive complexity >15, extract sub-methods, introduce guard clauses, flatten nested ifs.
3. **Extract / Inline / Rename** - Apply targeted refactorings: extract method for long blocks, extract variable for complex expressions, inline trivial indirection, rename for intent clarity.
4. **Dead Code Removal** - Find unused functions, unused parameters, unused branches, unreachable code. Remove or document why kept.
5. **Architectural Boundary Check** - For each cross-layer call, verify it respects the architecture (e.g., controller → service → repository). Flag upward or skip-layer dependencies.
6. **Hot-Path Review** - Identify performance-critical paths (loops, request handlers). Check for N+1 queries, unnecessary allocations, blocking I/O in async contexts.

**Integration**: Apply refactorings that preserve behavior. Run existing tests after each change. Commit refactoring separately from feature changes.

## 2. SPEC Branch

**Philosophy**: Scenario-Based Analyst (Sutcliffe, McDermott) - requirements are best discovered and validated by walking concrete scenarios (both positive and negative) rather than by reading abstract statements.

**Specialized issues** (in addition to GLOBAL):
- Requirements phrased only as "happy path" behavior
- No misuse cases or security/abuse scenarios documented
- Only one stakeholder perspective considered (e.g., only end-user, not admin/operator/auditor)
- Non-functional requirements missing (performance, accessibility, observability, i18n)
- Design decisions without rationale comparing alternatives
- Requirements that describe WHAT but miss critical constraints (WHY, WHEN, HOW-MUCH)

**Scenario-Based Analyst techniques** (execute in order, skip if not applicable):

1. **Primary Scenario Walkthrough** - Trace the main user journey end-to-end, step by step. At each step: what data exists, what actions are available, what can fail? Gaps become new FR-XX entries.
2. **Misuse Case / Abuse Scenario** - For each user action, consider malicious or erroneous use: invalid input, privilege escalation, resource exhaustion, race conditions, replay attacks. Map to security requirements.
3. **Stakeholder Viewpoint Rotation** - List all stakeholders (end-user, admin, operator, auditor, integrator, future maintainer). For each, ask: "what do I need from this system?" Missing perspectives produce new requirements.
4. **Non-Functional Requirements Check** - Apply FURPS+ categories: Functionality (covered), Usability, Reliability, Performance, Supportability, plus Security, Localization, Compliance. Each missing category becomes a requirement gap.
5. **Design Alternatives Audit** - For each DD-XX, ask: "what other approaches were considered, why was this chosen?" If only one option is listed, the DD is under-researched - add 1-2 alternatives with trade-offs.

**Integration**: New requirements added as FR-XX with proper IDs. Misuse cases documented as security requirements. Design alternatives listed under each DD.

## 3. IMPL Branch

**Philosophy**: Pre-Mortem Planner (Gary Klein) - "Prospective hindsight" doubles identified risks. Imagine the implementation has already failed, then work backwards to prevent each cause.

**Specialized issues** (in addition to GLOBAL):
- Steps ordered by code structure rather than by risk
- No explicit rollback strategy for schema changes, data migrations, or destructive operations
- Incremental delivery not considered (all-or-nothing big-bang integration)
- Hidden dependencies between steps
- Assumptions about environment, libraries, or data that are not validated before the step that needs them

**Pre-Mortem Planner techniques** (execute in order, skip if not applicable):

1. **Pre-Mortem** - Imagine this implementation completed and failed in production. Write 5-10 plausible failure causes. For each cause, add a preventive step earlier in the plan.
2. **Risk-First Ordering** - Identify the step with the highest uncertainty (unfamiliar API, complex algorithm, external dependency). Move it earlier so failure surfaces early and recovery is cheaper.
3. **Incremental Slicing** - Can each step (or small group of steps) ship as a working increment? Re-slice so that after each slice the system is still functional and testable.
4. **Dependency Graph** - Map dependencies between IS-XX steps. Identify parallelizable steps. Flag critical path. Detect hidden coupling (step N assumes step M's side effects).
5. **Rollback Strategy** - For each state-modifying step (DB migration, config change, deploy), document: how to detect failure, how to revert, how to verify revert succeeded.

**Integration**: Reorder IS-XX to reflect risk-first. Add IS-XX entries for preventive measures from pre-mortem. Add rollback notes to affected steps.

## 4. TEST Branch

**Philosophy**: Mutation Tester (DeMillo, Lipton, Sayward 1978) - "A test suite is good if it can detect injected faults." Improvement means testing that would catch subtle mutations, not just happy-path coverage.

**Specialized issues** (in addition to GLOBAL):
- Tests cover only example inputs, not input classes
- No boundary tests (min, max, min-1, max+1, empty, null)
- Assertions check happy-path output but not side effects or error states
- Missing combinatorial coverage for interacting parameters
- Test data is single example, not representative of equivalence classes
- No negative tests (system should reject invalid input)

**Mutation Tester techniques** (execute in order, skip if not applicable):

1. **Boundary Value Analysis** - For each numeric or bounded input, add tests at: min, min+1, max, max-1, zero, negative, empty collection, max-size collection.
2. **Equivalence Partitioning** - Group all possible inputs into equivalence classes (valid, invalid-type, invalid-range, invalid-format). Ensure at least one test per class.
3. **Mental Mutation Testing** - For each condition in the code under test, ask: "if I inverted this (`<` to `<=`, `&&` to `||`, `true` to `false`), would any test fail?" If not, the test suite is weak - add a test that would detect the mutation.
4. **Error Guessing** - Based on experience, identify fragile areas: concurrency, timezone handling, Unicode, number precision, retry logic. Add targeted tests even without formal coverage reason.
5. **Negative Test Generation** - For each happy-path TC-XX, create a paired negative TC-XX that verifies rejection of invalid input (wrong type, missing field, oversized, forbidden characters).
6. **Pairwise Combinatorial** - For tests with 3+ interacting parameters, use pairwise (N-wise) design to cover all pairs with fewer than full-factorial tests.

**Integration**: New test cases added as TC-XX. Test data tables expanded with equivalence class labels. Negative tests clearly marked.

## 5. TASKS Branch

**Philosophy**: Critical Path Analyst (Kelley/Walker 1957) combined with INVEST Auditor (Bill Wake 2003) - tasks should each be Independent, Negotiable, Valuable, Estimable, Small, Testable; the sequence should expose the critical path explicitly.

**Specialized issues** (in addition to GLOBAL):
- Tasks lack Definition of Done (completion criteria)
- Task dependencies not explicit (critical path hidden)
- No risk distribution (all risky tasks at the end or all at the start)
- Tasks fail INVEST criteria (too large, too dependent, not estimable)
- Parallelization opportunities not flagged

**Critical Path + INVEST techniques** (execute in order, skip if not applicable):

1. **INVEST Check** - For each TK-XX, apply the six criteria: Independent (minimal coupling), Negotiable (scope can shrink), Valuable (delivers something), Estimable (effort known), Small (fits single session), Testable (clear done-criteria). Flag failures.
2. **Critical Path Identification** - Build task dependency graph. Identify longest path by total effort - this is the critical path. Any delay here delays delivery. Document explicitly.
3. **Pre-Mortem on Sequence** - Imagine delivery is late. Which task likely slipped? Why? Add buffer, split that task, or move it earlier to fail fast.
4. **Definition of Done Audit** - For each TK-XX, require explicit completion criteria: code merged, tests pass, docs updated, reviewer approved, deployed. Add if missing.
5. **Risk Distribution** - Classify each task as high/medium/low risk. Check distribution: avoid risk clusters (all risky tasks in one phase) and avoid risk end-loading (risky tasks at deadline). Reorder or split to distribute.

**Integration**: Update TK-XX entries with INVEST notes, explicit dependencies, and Definition of Done. Mark critical path tasks.

## 6. Workflows Branch

**Philosophy**: Cognitive Walkthrough Analyst (Polson, Lewis, Rieman, Wharton 1992) - evaluate an interface (or workflow) by simulating a new user attempting each task step-by-step, asking "would they know what to do, would they recognize they did it right?"

**Specialized issues** (in addition to GLOBAL):
- Steps that require unstated context knowledge
- Ambiguous verbs ("review", "ensure", "handle") without concrete actions
- No failure recovery at each step (what if this step fails?)
- Branching logic without explicit conditions for each branch
- Workflow assumes state that prior steps did not establish

**Cognitive Walkthrough techniques** (execute in order, skip if not applicable):

1. **Agent Simulation Walkthrough** - Mentally execute the workflow as a fresh agent with no prior context. At each step ask: (a) do I know what to do next? (b) will I recognize I did it correctly? (c) what's my next action if unclear? Flag every step that fails.
2. **FMEA Per Step** - For each step, enumerate failure modes: input missing, tool unavailable, output malformed, dependency broken. For each failure mode, specify detection and recovery.
3. **Dry-Run with Edge Inputs** - Simulate execution with edge cases: empty input, conflicting input, missing prerequisite, partial prior execution. Find steps that break or diverge.
4. **Ambiguity Hunt** - Grep for vague verbs: "review", "ensure", "handle", "address", "consider", "appropriate", "as needed". Each instance needs a concrete replacement or explicit decision rule.
5. **Branch Coverage Audit** - For every conditional ("if X then Y"), verify the else-branch is also defined. For every context match, verify No Context Match fallback. For every error, verify explicit handling.

**Integration**: Rewrite vague steps with concrete actions. Add failure recovery notes. Add missing fallback branches. Update ambiguous decision points with explicit criteria.

## 7. Skills Branch

**Philosophy**: Tacit Knowledge Externalizer (Nonaka/Takeuchi 1995 "SECI model") - a skill's job is to convert tacit expert knowledge into explicit instructions that a novice agent can execute. Improvement means surfacing assumptions that experts take for granted.

**Specialized issues** (in addition to GLOBAL):
- Skill assumes prior domain knowledge
- Decision points without explicit criteria (expert would "just know")
- Gotchas known to author but not documented
- Intent Lookup entries without corresponding procedure section
- Examples that only cover the obvious use case
- Reference files listed but never linked from procedure sections

**Tacit Knowledge Externalizer techniques** (execute in order, skip if not applicable):

1. **Intent-to-Action Trace** - For each entry in Intent Lookup, trace to the action steps. Can a fresh agent execute without loading any reference file? If not, promote essential content into SKILL.md.
2. **Decision Tree Completeness** - For each decision point ("if A do X, else do Y"), verify both branches are documented. For each 3-way or N-way split, verify all N branches handled.
3. **Gotcha Audit** - Ask: "what mistakes would a new user make that the author would catch instantly?" Document each as a Gotchas entry. Include deprecated patterns, confusing parameters, silent failures.
4. **Self-Containment Test** - Count references to other files in SKILL.md. For each reference, check if the referenced content is essential (keep link) or nice-to-have (inline summary). SKILL.md should answer 80% of use cases alone.
5. **Example Coverage Check** - For each primary use case in Intent Lookup, verify an example (copy-paste ready) exists. Edge cases and error handling should also have examples.

**Integration**: Move essential content into SKILL.md. Add Gotchas section. Add missing examples. Make decision rules explicit.

## 8. STRUT Branch

**Philosophy**: Deliverables Verifier - a structured plan is only as good as its verifiable outputs. Every objective must resolve to a deliverable, every deliverable must be testable by inspection, every transition must cover both success and failure paths.

**Specialized issues** (in addition to GLOBAL):
- Objectives without linked deliverables
- Deliverables phrased as activities ("investigate X") rather than outcomes ("X document with Y findings")
- Transitions cover success but not failure branches
- Steps lack concrete AGEN verbs
- Phase N expects input that phase N-1 did not produce

**Deliverables Verifier techniques** (execute in order, skip if not applicable):

1. **Objective-Deliverable Trace** - For each objective, verify at least one deliverable satisfies it (via `← PX-DY` reference). Objectives without deliverables are aspirational - either add a deliverable or remove the objective.
2. **Verifiability Check** - For each deliverable, ask: "how would I confirm this is done?" If the answer is subjective ("looks good") the deliverable is not verifiable - rewrite as a concrete outcome (file exists, test passes, document has section X).
3. **Transition Coverage** - For each phase, verify transitions cover: (a) all deliverables met → next phase, (b) partial or missing deliverables → retry or escalate, (c) blocked → consult. No phase should have a single unconditional transition.
4. **Phase Interdependence** - For phase N, identify required inputs. Trace each to a deliverable of phase N-1 (or earlier). Missing producers indicate planning gap.
5. **AGEN Verb Audit** - For each step, verify it uses a concrete AGEN verb ([READ], [WRITE], [SEARCH], [VERIFY], etc.). Replace vague verbs with specific ones.

**Integration**: Link objectives to deliverables. Rewrite deliverables as outcomes. Expand transitions to cover failure paths. Replace vague step verbs.

## 9. Cross-Branch Observations

### 9.1 Common Technique Patterns

Three techniques recur across contexts (with domain-specific framing):

- **Walkthrough / Simulation** - SPEC (scenario walkthrough), Workflows (cognitive walkthrough), Skills (intent-to-action trace). Common pattern: mentally execute the artifact as the intended consumer to find gaps.
- **Pre-Mortem / Adversarial Imagination** - IMPL (pre-mortem), TASKS (pre-mortem on sequence), TEST (mental mutation). Common pattern: imagine failure, work backward to preventive measures.
- **Alternative Generation** - SPEC (design alternatives), Research (competing hypothesis), TEST (equivalence partitioning). Common pattern: force enumeration of options instead of accepting the first that works.

### 9.2 Per-Context Depth Calibration

Not every branch needs 7 techniques. Suggested counts based on complexity:
- Research, TEST: 6-8 techniques (complex domain with many axes)
- Code, SPEC, IMPL, Workflows: 5-6 techniques
- TASKS, Skills, STRUT, Problem Solving: 4-5 techniques

### 9.3 Shared Pre-Mortem Pattern

Gary Klein's pre-mortem is powerful enough to appear as a named technique in IMPL and TASKS, and implicitly drives Research (Competing Hypothesis), TEST (Mutation), and SPEC (Misuse Case). Consider promoting pre-mortem to a **GLOBAL technique** that any branch can invoke.

### 9.4 Persona Consistency

All personas share the "constructive challenge" stance inherited from Adversarial Collaborator:
- Research: Adversarial Collaborator (Kahneman)
- Problem Solving: Conservative Engineer (implicit)
- Code: Refactoring Craftsman (Fowler)
- SPEC: Scenario-Based Analyst (Sutcliffe/McDermott)
- IMPL: Pre-Mortem Planner (Klein)
- TEST: Mutation Tester (DeMillo/Lipton/Sayward)
- TASKS: Critical Path Analyst + INVEST Auditor (Kelley/Walker + Wake)
- Workflows: Cognitive Walkthrough Analyst (Polson et al.)
- Skills: Tacit Knowledge Externalizer (Nonaka/Takeuchi)
- STRUT: Deliverables Verifier

Each named after an established expert or methodology (except STRUT, which is DevSystem-native).

## 10. Sources

**Primary sources:**

- `IMPROV-IN01-SC-FOWLER-REFACTORING`: https://martinfowler.com/books/refactoring.html - Fowler's refactoring catalog, code smells taxonomy [VERIFIED]
- `IMPROV-IN01-SC-KLEIN-PREMORTEM`: https://www.gary-klein.com/premortem - Gary Klein's pre-mortem method definition [VERIFIED]
- `IMPROV-IN01-SC-KLEIN-HBR-2007`: Klein, G. "Performing a Project Premortem" Harvard Business Review, September 2007 (referenced in ResearchGate 3229642) [VERIFIED]
- `IMPROV-IN01-SC-MITCHELL-1989`: Mitchell, Russo & Pennington 1989 - prospective hindsight improves failure-cause identification 30% [VERIFIED]
- `IMPROV-IN01-SC-WAKE-INVEST`: https://en.wikipedia.org/wiki/INVEST_(mnemonic) - Bill Wake's INVEST criteria for user stories [VERIFIED]
- `IMPROV-IN01-SC-FAGAN-INSPECTION`: https://en.wikipedia.org/wiki/Fagan_inspection - Fagan code inspection methodology (IBM 1974) [VERIFIED]
- `IMPROV-IN01-SC-OWASP-ABUSECASE`: https://cheatsheetseries.owasp.org/cheatsheets/Abuse_Case_Cheat_Sheet.html - OWASP abuse case methodology [VERIFIED]
- `IMPROV-IN01-SC-WIKI-MISUSECASE`: https://en.wikipedia.org/wiki/Misuse_case - Misuse case / negative scenario [VERIFIED]
- `IMPROV-IN01-SC-SUTCLIFFE-RE`: https://link.springer.com/article/10.1007/BF02802920 - Sutcliffe, scenario-based requirements analysis [VERIFIED]
- `IMPROV-IN01-SC-MCDERMOTT-ABUSE`: https://www.andrew.cmu.edu/course/95-750/docs/CaseModels.pdf - McDermott, abuse case models for security requirements [VERIFIED]
- `IMPROV-IN01-SC-DEMILLO-MUTATION`: DeMillo, Lipton, Sayward 1978 "Hints on Test Data Selection" (foundational mutation testing) [VERIFIED]
- `IMPROV-IN01-SC-ACADEMIA-MUTATION-COMPARE`: https://www.academia.edu/7783094 - Comparing EP, BVA, branch coverage via mutation analysis [VERIFIED]
- `IMPROV-IN01-SC-POLSON-CW`: Polson, Lewis, Rieman, Wharton 1992 "Cognitive walkthroughs: a method for theory-based evaluation of user interfaces" [VERIFIED]
- `IMPROV-IN01-SC-ASQ-FMEA`: https://asq.org/quality-resources/fmea - ASQ Failure Mode and Effects Analysis definition [VERIFIED]
- `IMPROV-IN01-SC-WIKI-FMEA`: https://en.wikipedia.org/wiki/Failure_mode_and_effects_analysis - FMEA methodology overview [VERIFIED]
- `IMPROV-IN01-SC-KELLEY-CPM`: Kelley, J.E. & Walker, M.R. 1957 - Critical Path Method origin [VERIFIED]
- `IMPROV-IN01-SC-NONAKA-SECI`: Nonaka & Takeuchi 1995 "The Knowledge-Creating Company" - SECI model, tacit/explicit knowledge conversion [VERIFIED]
- `IMPROV-IN01-SC-ARGON-REQVER`: https://argondigital.com/blog/product-management/verification-and-validation/ - Requirements verification best practices [VERIFIED]
- `IMPROV-IN01-SC-AUGMENT-REFACTOR`: https://www.augmentcode.com/guides/12-essential-code-refactoring-techniques - 12 code refactoring techniques [VERIFIED]
- `IMPROV-IN01-SC-OWASP-THREATMODEL`: https://owasp.org/www-community/Threat_Modeling_Process - OWASP threat modeling process [VERIFIED]

**Internal sources:**

- `IMPROV-IN01-SC-DEVSYS-IMPROVEV2`: `e:\Dev\IPPS\DevSystemV3.6\workflows\improve-v2.md` - current workflow with 2 completed branches (Research, Problem Solving) [VERIFIED]
- `IMPROV-IN01-SC-DEVSYS-IDREG`: `e:\Dev\IPPS\ID-REGISTRY.md` - DevSystem ID conventions [VERIFIED]

## 11. Next Steps

1. User reviews proposed personas and techniques for fit
2. Adjust branches that feel over/under-specified
3. Promote shared patterns (walkthrough, pre-mortem, alternative generation) to GLOBAL techniques if desired
4. Update `improve-v2.md` CONTEXT-SPECIFIC branches with accepted personas and techniques
5. Add `IMPROV` TOPIC to ID-REGISTRY.md
6. Run `/verify` on updated `improve-v2.md`

## 12. Document History

**[2026-04-30 20:05]**
- Initial INFO document created with 8 branch proposals
- 10 primary personas mapped to established methodologies
- Cross-branch observations section added
