---
description: Find and fix contradictions, inconsistencies, and improvement opportunities
auto_execution_mode: 1
---

# Improve Workflow

Autonomous self-improvement in three phases: enrich content, filter through pragmatic assessment, then polish expression.

**Goal**: Improved output with enriched content and consistent quality

**Why**: First-pass output has coverage gaps, methodology weaknesses, and APAPALAN (As Precise As Possible, As Little As Necessary) / MECT (Minimal Explicit Consistent Terminology) violations. Phase 1 strengthens substance; Phase 2 filters out over-engineering; Phase 3 strengthens expression.

## Required Skills

- @skills:write-documents for APAPALAN_RULES, MECT_WRITING_RULES, templates, rules
- @skills:coding-conventions for MECT_CODING_RULES
- @skills:deep-research for research enrichment techniques

## MUST-NOT-FORGET

- Apply fixes immediately - this workflow has authority to correct issues
- Phase 1 (enrich) → Phase 2 (pragmatic filter) → Phase 3 (polish) - strict order
- Every Phase 1 proposal must pass Phase 2 before applying
- Re-read context-specific templates and rules before assessing (see Phase 1 reads per context)
- CRITICAL severity first, then HIGH, group related fixes
- Preserve existing IDs (FR-XX, NFR-XX, DD-XX, IS-XX, TC-XX, TK-XX, etc.)
- Never replicate `/verify` (rule-based formal verification) or `/critique` (logic flaw detection)
- Research enrichment adds value through new evidence, not fault-finding

## Mandatory Re-read

**SESSION-MODE**: NOTES.md, PROBLEMS.md, PROGRESS.md, FAILS.md

**PROJECT-MODE**: README.md, !NOTES.md or NOTES.md, FAILS.md, ID-REGISTRY.md

## GLOBAL-RULES

Apply to ALL contexts before any context-specific steps.

### Issue Categories (all contexts)

1. Contradictions
2. Inconsistencies
3. Ambiguities
4. Underspecified behavior
5. Broken dependencies
6. Incorrect/unverified assumptions
7. Flawed logic/thinking
8. Unnecessary complexity
9. New solutions for already solved problems
10. Concept overlap
11. Broken rules

### Phase 2: Pragmatic Filter (all contexts)

Every Phase 1 enrichment proposal must pass this filter before applying. For each proposed improvement, answer:

1. **Already addressed?** - Check existing content, code, conversation for coverage
2. **Real risk or theoretical?** - Has this happened in practice, or is it speculative?
3. **Proportionate?** - Does the fix cost more than the risk it mitigates?
4. **Concept count justified?** - If this adds concepts, does the added clarity or coverage outweigh the added complexity?
5. **Simpler alternative?** - Can a comment, constraint, or one-liner replace a structural change?

**Decision per proposal**:
- **APPLY** - passes all 5 questions → apply immediately
- **DEFER** - fails any question → log to `_DEFERRED_IMPROVEMENTS.md` with assessment rationale

Deferred proposals use reconcile's findings format. Run `/reconcile` on `_DEFERRED_IMPROVEMENTS.md` for pragmatic review.

### Phase 3: Quality Polish (all contexts)

**APAPALAN** - apply to all written documents and communications:
- **AP-PR-07**: Be specific - replace vague statements with concrete, verifiable ones
- **AP-PR-09**: Consistent patterns - same concept = same format everywhere
- **AP-BR-02**: Cut filler - drop articles, verbose constructions, redundant phrases
- **AP-NM-01**: One name per concept - find and fix synonyms and polysemy
- **AP-NM-05**: Use standard terms - replace invented jargon with established terminology
- **AP-ST-01**: Goal first - reader knows WHY before HOW

**MECT Writing** - apply to written documents:
- **MW-VO-01**: Active voice - actor before action
- **MW-VO-03**: Simplest verb - "review" not "carry out a review"
- **MW-VO-04**: Obligation words - must/must not/should/may, never "shall"
- **MW-WC-01**: Word-level precision - accuracy != precision, simple != simplistic
- **MW-TD-01**: Naming structure - explicit name -> specifiers -> states -> mnemonics
- **MW-HS-01**: Informative headings - state content, not topic
- **MW-DT-01**: Four description lenses - intentional/functional/technical/contextual

**MECT Coding** - apply to code:
- **MC-PR-01**: One name per concept across codebase - no synonyms across layers
- **MC-PR-03**: No meta-words without qualifier - qualify Manager, Service, Handler
- **MC-PR-05**: Error messages state what failed, why, and recovery action
- **MC-PR-06**: Log messages self-contained - each line understandable alone
- **MC-BR-04**: Boolean functions use predicate prefix (is_/has_/can_), not "check_"
- **MC-CO-01**: Corresponding pairs use same word stem (open/close, encode/decode)
- **MC-CO-03**: Convergent naming - same term in URL, payload, variable, log, docs
- **MC-ND-06**: Disambiguate by qualifying, not renaming

### Fix Rules (all contexts)

- Preserve IDs (FR-XX, NFR-XX, DD-XX, IS-XX, TC-XX, TK-XX)
- Pick simplest fix when multiple valid options
- Remove broken refs or add missing targets
- Apply APAPALAN + MECT to all text changes (precision first, then brevity)
- Apply MECT_CODING_RULES to all code changes (naming, logs, errors)

## Cross-Context Techniques

Three generative techniques any branch may invoke. Referenced from context-specific sections rather than duplicated.

1. **Pre-Mortem** (Gary Klein) - Imagine this artifact completed and failed in production/use. Write 5-10 plausible failure causes. For each, add a preventive measure to the artifact.
2. **Walkthrough** (Polson et al.) - Mentally execute the artifact as its intended consumer (user, agent, developer). At each step ask: (a) do I know what to do? (b) will I recognize I did it right? Flag every point that stalls.
3. **Alternative Generation** - For each key decision in the artifact, enumerate 2-3 alternatives not yet considered. Compare trade-offs. Either adopt a better alternative or document why the current choice wins.

# CONTEXT-SPECIFIC

**Persona**: Adversarial Collaborator (Kahneman) - improve through constructive challenge backed by new evidence. Each context applies a domain-specific methodological lens.

Detection: determine context from file naming and content, then apply matching section. Multiple contexts may apply. When scope is a folder, classify each file independently.

## Code

**Lens**: Refactoring Craftsman (Fowler) - make working code more readable, maintainable, and aligned with intent.

**Phase 1**: Skip - code enrichment is implementation, not improvement.

**Phase 3 reads**: `MECT_CODING_RULES.md` (@skills:coding-conventions)

**Specialized issues** (in addition to GLOBAL):
- Duplicated code blocks (rule of three violated)
- Feature envy (method uses another class's data more than its own)

**Adversarial Collaborator techniques** (execute in order, skip if not applicable):

1. **Code Smell Identification** - Walk through scope for Fowler's smells. Prioritize: long methods, large classes, duplication, feature envy, primitive obsession.
2. **Cognitive Complexity Reduction** - For methods with deep nesting or high branching, extract sub-methods, introduce guard clauses, flatten nested ifs.
3. **Extract / Inline / Rename** - Extract method for long blocks, extract variable for complex expressions, inline trivial indirection, rename for intent clarity.
4. **Architectural Boundary Restoration** - For each cross-layer call, verify it respects architecture. Flag upward or skip-layer dependencies. Propose restructuring.
5. **Testability Refactoring** - Find code hard to test (static dependencies, hidden state, tight coupling). Propose refactorings that make it testable.

## SPEC Documents

**Lens**: Scenario-Based Analyst (Sutcliffe/McDermott) - requirements are best discovered by walking concrete scenarios, both positive and negative.

**Phase 1 reads**: `SPEC_RULES.md`, `SPEC_TEMPLATE.md` (@skills:write-documents), source INFO documents

**Specialized issues** (in addition to GLOBAL):
- Requirements phrased only as happy-path behavior
- No misuse cases or security/abuse scenarios
- Only one stakeholder perspective considered
- Non-functional requirements missing (performance, accessibility, observability)
- Design decisions without rationale or alternatives
- Multiplicative design decisions (too many testing configurations)

**Adversarial Collaborator techniques** (execute in order, skip if not applicable):

1. **Primary Scenario Walkthrough** - Trace main user journey end-to-end. At each step: what data exists, what actions available, what can fail? Gaps become new FR-XX.
2. **Misuse Case Generation** - For each user action, consider malicious or erroneous use: invalid input, privilege escalation, resource exhaustion, race conditions. Map to security requirements.
3. **Stakeholder Viewpoint Rotation** - List all stakeholders (end-user, admin, operator, auditor, integrator, maintainer). For each: "what do I need from this system?" Missing perspectives produce new requirements.
4. **Non-Functional Requirements Generation** - For the system under spec, imagine it at 100x scale, operated by a hostile user, audited by compliance, translated into 5 languages. Each scenario revealing a missing requirement produces a new NFR-XX.
5. **Design Alternatives Generation** - For each DD-XX, add 1-2 alternatives with trade-offs if only one option is listed.

## IMPL Plans

**Lens**: Pre-Mortem Planner (Gary Klein) - prospective hindsight doubles identified risks. Imagine the implementation has already failed, then work backwards.

**Phase 1 reads**: `IMPL_TEMPLATE.md` (@skills:write-documents), source SPEC

**Specialized issues** (in addition to GLOBAL):
- Steps ordered by code structure rather than by risk
- No rollback strategy for destructive operations
- Incremental delivery not considered (big-bang integration)
- Hidden dependencies between steps
- Environment/library assumptions not validated before the step that needs them

**Adversarial Collaborator techniques** (execute in order, skip if not applicable):

1. **Pre-Mortem** - Imagine implementation completed and failed. Write 5-10 plausible failure causes. Add preventive steps earlier in the plan.
2. **Risk-First Ordering** - Identify step with highest uncertainty (unfamiliar API, complex algorithm, external dependency). Move it earlier so failure surfaces cheaply.
3. **Incremental Slicing** - Re-slice so that after each step (or small group) the system is still functional and testable.
4. **Parallelization Discovery** - Map dependencies between IS-XX steps. Identify which could execute concurrently. Propose reorganization into parallel tracks.
5. **Rollback Strategy** - For each state-modifying step (DB migration, config change, deploy): how to detect failure, how to revert, how to verify revert succeeded.

## TEST Plans

**Lens**: Mutation Tester (DeMillo/Lipton/Sayward) - a test suite is good if it can detect injected faults, not just confirm the happy path.

**Phase 1 reads**: `TEST_TEMPLATE.md` (@skills:write-documents), source SPEC + IMPL

**Specialized issues** (in addition to GLOBAL):
- Tests cover only example inputs, not input classes
- No boundary tests (min, max, min-1, max+1, empty, null)
- Assertions check happy-path output but not side effects or error states
- Missing combinatorial coverage for interacting parameters
- No negative tests (system should reject invalid input)

**Adversarial Collaborator techniques** (execute in order, skip if not applicable):

1. **Boundary Value Analysis** - For each numeric or bounded input, add tests at: min, min+1, max, max-1, zero, negative, empty collection, max-size collection.
2. **Equivalence Partitioning** - Group all possible inputs into equivalence classes (valid, invalid-type, invalid-range, invalid-format). Ensure at least one test per class.
3. **Mental Mutation Testing** - For each condition in code under test, ask: "if I inverted this (`<` to `<=`, `&&` to `||`, `true` to `false`), would any test fail?" If not, add a test that detects the mutation.
4. **Error Guessing** - Based on experience, identify fragile areas: concurrency, timezone handling, Unicode, number precision, retry logic. Add targeted tests.
5. **Negative Test Generation** - For each happy-path TC-XX, create a paired TC-XX that verifies rejection of invalid input.
6. **Pairwise Combinatorial** - For tests with 3+ interacting parameters, use pairwise design to cover all pairs with fewer than full-factorial tests.

## TASKS Plans

**Lens**: Critical Path Analyst (Kelley/Walker) - expose the critical path explicitly, distribute risk, ensure each task delivers standalone value.

**Phase 1 reads**: `TASKS_TEMPLATE.md` (@skills:write-documents), source IMPL + TEST

**Specialized issues** (in addition to GLOBAL):
- Tasks too large for single-session completion
- Dependencies between tasks not explicit (critical path hidden)
- Risk concentrated in one phase (all risky tasks at start or end)
- Tasks mixing implementation and testing concerns
- Parallelization opportunities not flagged

**Adversarial Collaborator techniques** (execute in order, skip if not applicable):

1. **Task Shrinking** - For each task larger than one session, propose decomposition into 2-3 sub-tasks that each deliver a testable increment.
2. **Critical Path Identification** - Build dependency graph. Identify longest path by effort - this drives delivery. Document explicitly.
3. **Pre-Mortem on Sequence** - Imagine delivery is late. Which task likely slipped? Why? Add buffer, split that task, or move it earlier.
4. **Done-Criteria Strengthening** - For each TK-XX, propose 2-3 measurable completion criteria the current plan does not state (e.g., "API responds within 500ms under 100 RPS" vs "performance acceptable").
5. **Risk Distribution** - Classify each task as high/medium/low risk. Avoid risk clusters and risk end-loading. Reorder or split to distribute.

## Workflows

**Lens**: Cognitive Walkthrough Analyst (Polson/Lewis/Rieman/Wharton) - evaluate a workflow by simulating a new agent attempting each step.

**Phase 1 reads**: `WORKFLOW_RULES.md`, `WORKFLOW_TEMPLATE.md` (@skills:write-documents)

**Specialized issues** (in addition to GLOBAL):
- Steps requiring unstated context knowledge
- No failure recovery at each step
- Branching logic without explicit conditions for each branch
- Workflow assumes state that prior steps did not establish

**Adversarial Collaborator techniques** (execute in order, skip if not applicable):

1. **Agent Simulation Walkthrough** - Execute workflow as a fresh agent with no prior context. At each step: (a) do I know what to do? (b) will I recognize success? (c) what if unclear? Flag failures.
2. **FMEA Per Step** - For each step, enumerate failure modes: input missing, tool unavailable, output malformed, dependency broken. Specify detection and recovery for each.
3. **Dry-Run with Edge Inputs** - Simulate with: empty input, conflicting input, missing prerequisite, partial prior execution. Find steps that break.
4. **Vague Verb Concretion** - For each vague verb ("review", "ensure", "handle", "address", "consider"), generate a concrete replacement with verb + object + success criterion.

## Skills

**Lens**: Tacit Knowledge Externalizer (Nonaka/Takeuchi) - convert tacit expert knowledge into explicit instructions a novice agent can execute.

**Phase 1 reads**: `SKILL_RULES.md`, `SKILL_TEMPLATE.md` (@skills:write-documents)

**Specialized issues** (in addition to GLOBAL):
- Skill assumes prior domain knowledge not documented
- Decision points without explicit criteria (expert would "just know")
- Gotchas known to author but not documented
- Intent Lookup entries without corresponding procedure
- Examples covering only the obvious use case

**Adversarial Collaborator techniques** (execute in order, skip if not applicable):

1. **Intent-to-Action Trace** - For each Intent Lookup entry, trace to action steps. Can a fresh agent execute without loading reference files? If not, promote essential content into SKILL.md.
2. **Gotcha Externalization** - Ask: "what mistakes would a new user make that the author catches instantly?" Document each as a Gotchas entry.
3. **Reference Collapse** - For each "See X.md" in SKILL.md, ask: "would a new agent succeed without reading X.md?" If not, inline the essential 3-5 sentences.
4. **Example Generation from Novice Perspective** - For each primary use case, write the example a new agent would most need. Include edge cases and error handling examples.

## Research Output (INFO Documents)

**Lens**: Evidence-Finding Collaborator (Kahneman) - improve through constructive challenge backed by new evidence. Not fault-finding; evidence-finding.

**Phase 1 reads**: `INFO_TEMPLATE.md` (@skills:write-documents), `RESEARCH_STRATEGY_MEPI.md` or `RESEARCH_STRATEGY_MCPI.md` (@skills:deep-research)

**Specialized issues** (in addition to GLOBAL):
- Sources concentrated on single search engine or database
- All sources in one language when topic has international coverage
- Missing primary sources (only secondary/community tier)
- Stale sources (>12 months for fast-moving topics)
- Claims without verification labels
- Findings marked [ASSUMED] but testable
- Alternative interpretations not considered
- Search queries too narrow (premature narrowing)

**Adversarial Collaborator techniques** (execute in order, skip if not applicable):

1. **Key Assumptions Check** - Extract 3-5 implicit assumptions from findings. For each: is there evidence, or is it assumed?
2. **Query Generalization** - Extract original search queries from source URLs/context. Broaden with synonyms, alternative terminology, related concepts. Compare expanded results against existing source list.
3. **Method Challenge** - Evaluate the research method itself: Was the question decomposed correctly? Were the right source types consulted (web search vs academic databases vs official docs vs code repos)? Was the strategy appropriate (MEPI (Most Effective, Practical, Informative) vs MCPI (Most Complete, Precise, Informative))? If a different method would yield different results, execute it and compare.
4. **Competing Hypothesis Search** - Formulate the strongest alternative explanation not yet considered. Design 2-3 queries that would confirm or deny it.
5. **Alternative Language Search** - Re-search key topics in relevant alternative languages (determine from topic domain).
6. **Citation Chain** - Follow references from existing tier 1-2 sources. Check "cited by" for newer work.
7. **Temporal Freshness** - For sources >6 months old in fast-moving fields, search for superseding content.
8. **Source Validation** - Verify top 5 primary sources still accessible (use Playwright MCP with classic Google search if available).

**Integration**: New findings marked `[IMPROVED]`, challenged claims marked `[CHALLENGED]`. Update Sources section and Document History.

## Problem Solving Approaches

**Phase 1 reads**: PROBLEMS.md, FAILS.md, LEARNINGS.md

**Applies to**: Solution approaches in PROBLEMS.md, PROGRESS.md, session NOTES.md, or conversation context where an approach to solving a problem is described or attempted.

**Specialized issues** (in addition to GLOBAL):
- Steps too large (single failure blocks entire approach)
- Assumptions treated as facts without verification
- No fallback if primary approach fails
- Missing intermediate verification points
- Jumping to implementation before confirming diagnosis
- Optimistic assumptions about environment or dependencies

**Improvement techniques** (apply to solution approaches):

1. **Decompose further** - Break steps that could fail into smaller, independently verifiable sub-steps
2. **Add assumption gates** - Before each step that depends on an assumption, add explicit verification of that assumption
3. **Conservative ordering** - Reorder to execute cheapest/fastest validations first (fail fast, fail cheap)
4. **Add rollback points** - Identify where to revert if a step fails, before executing it
5. **Verify-before-act** - For each action that modifies state, verify the precondition holds first

## No Context Match

1. Apply GLOBAL Issue Categories only
2. Execute Phase 3 (Quality Polish) only
3. Skip Phase 1 (Content Enrichment) and Phase 2 (Pragmatic Filter)

# EXECUTION

## Steps

1. **Scope**: file path → that file; folder → all .md/code; none → conversation context
2. **Detect context** per file:
   - `_INFO_*` or Sources section with source IDs → Research Output
   - `_SPEC_*` or FR-XX/DD-XX IDs → SPEC Document
   - `_IMPL_*` or IS-XX IDs → IMPL Plan
   - `_TEST_*` or TC-XX IDs → TEST Plan
   - `_TASKS_*` or TK-XX IDs → TASKS Plan
   - `.py`, `.ps1`, `.js`, `.ts` etc. → Code
   - Workflow folder `.md` files → Workflow
   - Skill folder files → Skill
   - Solution approaches in tracking docs → Problem Solving
   - No match → No Context Match
3. **Re-read dependencies**:
   - Rules: `[AGENT_FOLDER]/rules/*.md`
   - Context-specific templates and rules (see Phase 1 reads per context)
   - Writing quality: `APAPALAN_RULES.md` + `MECT_WRITING_RULES.md` (@skills:write-documents)
   - Code quality: `MECT_CODING_RULES.md` (@skills:coding-conventions)
   - Workspace: README, NOTES, ID-REGISTRY, FAILS, LEARNINGS
   - Session: NOTES, PROBLEMS, PROGRESS (if SESSION-MODE)
4. **Phase 1: Content Enrichment** - Execute context-specific enrichment steps. Skip for Code and No Context Match.
5. **Phase 2: Pragmatic Filter** - For each Phase 1 proposal, run the 5 pragmatic questions. APPLY or DEFER.
6. **Phase 3: Quality Polish** - Build issue list from GLOBAL + context-specific categories. Apply APAPALAN, MECT Writing, MECT Coding checks.
7. **Fix plan** - CRITICAL first, then HIGH, group related fixes
8. **Execute fixes** - Update Document History with improvement summary
9. **Verify** - Re-read improved output, check for regressions

## Gate Check: Phase 1 → Phase 2

- [ ] Content enrichment complete (or skipped for Code/No Context Match)
- [ ] New findings integrated with proper labels (research context)
- [ ] No unresolved competing hypotheses left unaddressed (research context)
- [ ] Assumption gates added where needed (problem solving context)

Pass: Proceed to Phase 2 | Fail: Continue Phase 1

## Gate Check: Phase 2 → Phase 3

- [ ] Every Phase 1 proposal has a pragmatic assessment
- [ ] APPLY proposals applied to artifact
- [ ] DEFER proposals logged to `_DEFERRED_IMPROVEMENTS.md` with rationale

Pass: Proceed to Phase 3 | Fail: Continue Phase 2

## Stuck Detection

If 3 consecutive fix attempts cause regressions:
1. Document in PROBLEMS.md
2. Revert to last stable state
3. Ask user for guidance

# FINALIZATION

## Quality Gate

- [ ] All fixes maintain valid document structure
- [ ] IDs preserved (no broken FR-XX, NFR-XX, DD-XX, IS-XX, TC-XX references)
- [ ] No regressions in dependent documents
- [ ] APAPALAN/MECT compliance in all modified text

## Output

- Modified files in place
- Document History updated with improvement summary
- PROBLEMS.md updated if stuck or regression occurred
