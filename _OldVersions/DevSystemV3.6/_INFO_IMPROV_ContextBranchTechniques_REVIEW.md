# _INFO_IMPROV_ContextBranchTechniques_REVIEW.md

**Doc ID**: IMPROV-IN01-RV01
**Goal**: Critique the proposals in `IMPROV-IN01` for overlap with `/verify` (rule-based formal verification) vs. true conceptual content improvement (Adversarial Collaborator stance)
**Reviewed**: 2026-04-30 20:10
**Context**: User challenged whether proposed techniques really improve content quality at a conceptual level, or drift into rule-compliance checking that belongs in `verify.md`

## Review Method

**Discriminator applied to each technique**:

- **IMPROVE** (Adversarial Collaborator stance): *Generates new content, alternatives, or evidence.* Output expands the artifact. Answer to "what new thing did this produce?"
- **VERIFY** (rule-based check): *Evaluates existing content against a rule.* Output is a pass/fail or a list of rule violations. Answer to "did this comply?"
- **BORDERLINE**: Mixes both. Needs reframing.

A technique is pure-IMPROVE when its output could include *new requirements, new tests, new sources, new alternatives, new scenarios, new rollback steps* - things that did not exist before the technique ran.

## Table of Contents

1. [Critical Issues](#critical-issues)
2. [High Priority](#high-priority)
3. [Medium Priority](#medium-priority)
4. [Low Priority](#low-priority)
5. [Branch-by-Branch Classification](#branch-by-branch-classification)
6. [Recommendations](#recommendations)
7. [Document History](#document-history)

## Critical Issues

### `IMPROV-IN01-RV01-RF-01` STRUT branch is ~80% verify territory

- **Location**: `IMPROV-IN01` section 8 STRUT Branch
- **What**: 4 of 5 proposed techniques are rule-compliance checks that already belong in `verify.md`:
  - Objective-Deliverable Trace: "verify at least one deliverable satisfies it" - pure checklist
  - Transition Coverage: "verify transitions cover success/failure" - pure checklist
  - Phase Interdependence: "trace each to a deliverable of phase N-1" - pure checklist
  - AGEN Verb Audit: "verify uses a concrete AGEN verb" - pure rule check
- **Risk**: Implementing this branch would duplicate verify.md's STRUT validation. The persona name "Deliverables Verifier" literally names the verify function.
- **Evidence**: Verbs used are "verify", "trace", "audit" - all verify-family. Only "Verifiability Check" (rewriting vague deliverables as concrete outcomes) generates new content.
- **Suggested action**: Either (a) drop STRUT from improve-v2 entirely - let verify.md handle it, or (b) rethink improve for STRUT as decomposition re-evaluation: "Is this the right decomposition? Could phases be flatter? More parallel? Fewer phases?" That is Adversarial Collaborator thinking about structure.

### `IMPROV-IN01-RV01-RF-02` TASKS INVEST Check is pure verify

- **Location**: `IMPROV-IN01` section 5 TASKS Branch, technique 1
- **What**: "For each TK-XX, apply the six criteria: Independent, Negotiable, Valuable, Estimable, Small, Testable. Flag failures." - this is a compliance checklist against a named standard.
- **Risk**: Belongs in verify.md. Named INVEST as a methodology makes this indistinguishable from "apply WF-ST-02 to each step".
- **Suggested action**: Replace with a generative TASKS technique. Options:
  - **Task Shrinking**: For each task failing "Small", propose a decomposition into 2-3 sub-tasks that each satisfy INVEST (generates new tasks).
  - **Value Slicing**: Re-arrange tasks so each delivers standalone value even if later tasks slip (generates new ordering + task merges/splits).
  - Move "INVEST Check" itself to verify.md.

## High Priority

### `IMPROV-IN01-RV01-RF-03` "Audit" verbs signal verify-thinking

- **Location**: Multiple sections. Instances: SPEC "Design Alternatives Audit", TASKS "Definition of Done Audit", Workflows "Branch Coverage Audit", Skills "Gotcha Audit", STRUT "AGEN Verb Audit".
- **What**: "Audit" semantically means "check for compliance against a standard" - this is verify's job. Some of these are genuinely generative (Design Alternatives Audit *adds* alternatives, Gotcha Audit *adds* documentation) but the naming obscures this.
- **Risk**: Readers of improve-v2 will perform these techniques as checklists rather than generators.
- **Suggested action**: Rename audits that are generative:
  - "Design Alternatives Audit" → "Design Alternatives Generation"
  - "Gotcha Audit" → "Gotcha Externalization" (match the Nonaka/Takeuchi persona)
  - "Definition of Done Audit" → drop (verify job)
  - "Branch Coverage Audit" → drop (verify job) or reframe as "Missing Branch Enumeration"
  - "AGEN Verb Audit" → drop (verify job)

### `IMPROV-IN01-RV01-RF-04` Workflows "Branch Coverage Audit" is verify

- **Location**: `IMPROV-IN01` section 6 Workflows Branch, technique 5
- **What**: "For every conditional ('if X then Y'), verify the else-branch is also defined" - pure compliance check against WF-BR-02.
- **Risk**: Duplicates verify.md workflow branch coverage rule.
- **Suggested action**: Drop. The other Workflows techniques (Cognitive Walkthrough, FMEA, Dry-Run, Ambiguity Hunt) are all genuinely generative and sufficient.

### `IMPROV-IN01-RV01-RF-05` SPEC "Non-Functional Requirements Check" is a FURPS+ checklist

- **Location**: `IMPROV-IN01` section 2 SPEC Branch, technique 4
- **What**: "Apply FURPS+ categories: Functionality, Usability, Reliability, Performance, Supportability, plus Security, Localization, Compliance. Each missing category becomes a requirement gap."
- **Risk**: Named taxonomy check = verify territory. The *output* (new FR-XX per category) is generative, but the *technique* is checklist-driven.
- **Suggested action**: Keep the technique but reframe from "check" to "imagine": "**Non-Functional Dimension Stress Test**: For the system under spec, imagine it at 100x scale, 0.1x scale, run by a hostile user, operated at 3am by a sleep-deprived admin, audited by compliance, translated into 5 languages. Each scenario that reveals a missing requirement produces a new FR-XX." This is Adversarial Collaborator framing.

### `IMPROV-IN01-RV01-RF-06` Code "Dead Code Removal" is verify territory

- **Location**: `IMPROV-IN01` section 1 Code Branch, technique 4
- **What**: "Find unused functions, unused parameters, unused branches, unreachable code."
- **Risk**: This is static analysis. Linters (ESLint, pyflakes, Ruff) handle dead code detection. Belongs with verify/tooling, not conceptual improvement.
- **Suggested action**: Drop or replace with a generative Code technique. Options:
  - **Abstraction Opportunity Mining**: Identify 2-3 places where similar logic appears in different forms. Propose a shared abstraction (new function, new type, new pattern).
  - **Testability Refactoring**: Find code that is hard to test (static dependencies, hidden state). Propose refactorings that make it testable.

### `IMPROV-IN01-RV01-RF-07` Skills "Example Coverage Check" is a checklist

- **Location**: `IMPROV-IN01` section 7 Skills Branch, technique 5
- **What**: "For each primary use case in Intent Lookup, verify an example exists."
- **Risk**: Pure compliance check. Belongs in verify.md as SK-CT-04 rule check.
- **Suggested action**: Replace with "**Example Generation from Novice Perspective**: For each primary use case, imagine a new agent attempting it with zero context. Write the example that would most help them succeed. Generates new examples; does not just flag missing ones."

### `IMPROV-IN01-RV01-RF-08` Skills "Self-Containment Test" is mechanical counting

- **Location**: `IMPROV-IN01` section 7 Skills Branch, technique 4
- **What**: "Count references to other files in SKILL.md. Should answer 80% of use cases alone."
- **Risk**: Quantitative threshold = verify territory. The *decision* (promote content into SKILL.md) is generative, but the framing is compliance.
- **Suggested action**: Rename and reframe: "**Reference Collapse**: For each `See X.md` pointer in SKILL.md, ask 'would a new agent succeed 80% of the time without reading X.md?' If not, inline the essential 3-5 sentences." The action is generative (new inlined content), the measurement is qualitative.

## Medium Priority

### `IMPROV-IN01-RV01-RF-09` IMPL "Dependency Graph" is structural

- **Location**: `IMPROV-IN01` section 3 IMPL Branch, technique 4
- **What**: "Map dependencies between IS-XX steps. Identify parallelizable steps. Flag hidden coupling."
- **Risk**: Borderline. Building a graph is analytical. *Parallelization discovery* is generative. *Hidden coupling detection* is closer to verify.
- **Suggested action**: Split the technique. Keep the generative part ("**Parallelization Discovery**: identify which IS-XX could execute concurrently; propose reorganization into parallel tracks where beneficial"). Drop the structural part (let verify handle "steps must list explicit dependencies").

### `IMPROV-IN01-RV01-RF-10` TASKS "Definition of Done Audit" is pure verify

- **Location**: `IMPROV-IN01` section 5 TASKS Branch, technique 4
- **What**: "For each TK-XX, require explicit completion criteria."
- **Risk**: Checklist against a standard ("has DoD or not").
- **Suggested action**: Drop. Move to verify.md. Replace with generative technique such as "**Done-Criteria Strengthening**: For each TK-XX, propose 2-3 *measurable* DoD criteria the current plan doesn't state (e.g., 'API responds within 500ms under 100 RPS' vs 'performance acceptable')." The output adds concrete criteria.

### `IMPROV-IN01-RV01-RF-11` Workflows "Ambiguity Hunt" is grep-based

- **Location**: `IMPROV-IN01` section 6 Workflows Branch, technique 4
- **What**: "Grep for vague verbs: 'review', 'ensure', 'handle'..."
- **Risk**: Pattern-matching = verify territory. But the *replacement* is generative.
- **Suggested action**: Keep but reframe: "**Vague Verb Concretion**: Find vague verbs; for each, generate a concrete replacement (verb + object + success criterion). Example: 'ensure data is valid' → 'check that every record has non-null id field; reject the batch with error E01 if any row fails'." The focus is on what replaces the vagueness, not on finding it.

### `IMPROV-IN01-RV01-RF-12` STRUT "Verifiability Check" name contradicts purpose

- **Location**: `IMPROV-IN01` section 8 STRUT Branch, technique 2
- **What**: "For each deliverable ask 'how would I confirm this is done?' If subjective, rewrite as concrete outcome."
- **Risk**: Only genuinely generative STRUT technique, but named "Check" - reinforces verify-thinking.
- **Suggested action**: Rename to "**Deliverable Sharpening**" or "**Outcome Rewriting**". This is the single strong improve technique for STRUT; elevate it, drop the four verify-like siblings.

## Low Priority

### `IMPROV-IN01-RV01-RF-13` "Pre-Mortem" is listed per-context but could be GLOBAL

- **Location**: `IMPROV-IN01` sections 3 (IMPL), 5 (TASKS), 9.3 (cross-branch observation already notes this)
- **What**: Cross-branch observation correctly identifies pre-mortem as shared pattern. Section 9.3 suggests promoting to GLOBAL. Worth elevating in recommendations.
- **Suggested action**: Document in final recommendations as "**GLOBAL techniques**: Pre-Mortem, Walkthrough, Alternative Generation apply to all contexts and should be invokable from any branch." This avoids 8x duplication.

### `IMPROV-IN01-RV01-RF-14` TEST branch is the gold standard for improve-thinking

- **Location**: `IMPROV-IN01` section 4 TEST Branch
- **What**: All 6 techniques genuinely generate new tests (BVA, EP, Mutation, Error Guessing, Negative Tests, Pairwise). None are compliance checks.
- **Suggested action**: Use TEST branch as the reference pattern when reworking the other branches. Each technique should answer "what new TC-XX will this produce?"

## Branch-by-Branch Classification

Honest assessment of each proposed technique:

### Code (6 techniques)
- Code Smell Identification: IMPROVE
- Cognitive Complexity Reduction: IMPROVE (threshold is the *trigger*, extraction is the *action*)
- Extract/Inline/Rename: IMPROVE (gold)
- Dead Code Removal: **VERIFY** - drop
- Architectural Boundary Check: BORDERLINE - rename "Architectural Boundary Restoration" (find violations → propose restructuring)
- Hot-Path Review: IMPROVE

**Verdict**: 4 strong, 1 borderline, 1 drop. Add "Abstraction Opportunity Mining" or "Testability Refactoring" to replace dropped one.

### SPEC (5 techniques)
- Primary Scenario Walkthrough: IMPROVE (gold)
- Misuse Case / Abuse Scenario: IMPROVE (gold)
- Stakeholder Viewpoint Rotation: IMPROVE (gold)
- Non-Functional Requirements Check: BORDERLINE - reframe as "Non-Functional Dimension Stress Test"
- Design Alternatives Audit: IMPROVE if renamed to "Generation"

**Verdict**: Strong overall. Minor reframing of 2 techniques.

### IMPL (5 techniques)
- Pre-Mortem: IMPROVE (gold)
- Risk-First Ordering: IMPROVE
- Incremental Slicing: IMPROVE (gold)
- Dependency Graph: BORDERLINE - split into generative + verify parts
- Rollback Strategy: BORDERLINE - "propose rollback for each step" is improve; "check rollback documented" is verify

**Verdict**: 3 strong, 2 need split.

### TEST (6 techniques)
- All 6: IMPROVE (gold)

**Verdict**: Reference standard. No changes needed.

### TASKS (5 techniques)
- INVEST Check: **VERIFY** - drop
- Critical Path Identification: IMPROVE
- Pre-Mortem on Sequence: IMPROVE
- Definition of Done Audit: **VERIFY** - drop
- Risk Distribution: IMPROVE

**Verdict**: 3 strong, 2 drop. Replace with generative techniques (Task Shrinking, Done-Criteria Strengthening).

### Workflows (5 techniques)
- Agent Simulation Walkthrough: IMPROVE (gold)
- FMEA Per Step: IMPROVE (generates recovery steps)
- Dry-Run with Edge Inputs: IMPROVE
- Ambiguity Hunt: BORDERLINE - reframe to "Vague Verb Concretion"
- Branch Coverage Audit: **VERIFY** - drop

**Verdict**: 3 strong, 1 reframe, 1 drop.

### Skills (5 techniques)
- Intent-to-Action Trace: IMPROVE
- Decision Tree Completeness: **VERIFY** - drop
- Gotcha Audit: IMPROVE if renamed to "Externalization"
- Self-Containment Test: BORDERLINE - reframe to "Reference Collapse"
- Example Coverage Check: **VERIFY** - drop, replace with "Example Generation from Novice Perspective"

**Verdict**: 2 strong, 1 rename, 1 reframe, 2 drop.

### STRUT (5 techniques)
- Objective-Deliverable Trace: **VERIFY** - drop
- Verifiability Check: IMPROVE (rename to "Deliverable Sharpening")
- Transition Coverage: **VERIFY** - drop
- Phase Interdependence: **VERIFY** - drop
- AGEN Verb Audit: **VERIFY** - drop

**Verdict**: Only 1 of 5 is improve. Either drop STRUT branch entirely or rebuild with genuinely generative techniques (Decomposition Re-Evaluation, Phase Flattening, Parallelization Discovery).

## Recommendations

### Must Do (before updating improve-v2.md)

- [ ] Drop STRUT branch as currently proposed. Either remove it or rebuild with 3 genuinely generative techniques focused on re-decomposition and structural alternatives.
- [ ] Drop TASKS "INVEST Check" and "Definition of Done Audit". Replace with "Task Shrinking" and "Done-Criteria Strengthening".
- [ ] Drop Workflows "Branch Coverage Audit". Existing 4 techniques are sufficient.
- [ ] Drop Skills "Decision Tree Completeness" and "Example Coverage Check". Replace the latter with "Example Generation from Novice Perspective".
- [ ] Drop Code "Dead Code Removal". Replace with "Abstraction Opportunity Mining" or "Testability Refactoring".

### Should Do (terminology alignment)

- [ ] Rename all "Audit" techniques that are generative to "Generation", "Externalization", or similar active verbs.
- [ ] Rename SPEC "Design Alternatives Audit" → "Design Alternatives Generation".
- [ ] Rename Skills "Gotcha Audit" → "Gotcha Externalization".
- [ ] Rename STRUT "Verifiability Check" → "Deliverable Sharpening".
- [ ] Rename Workflows "Ambiguity Hunt" → "Vague Verb Concretion" (emphasize the replacement, not the detection).
- [ ] Reframe SPEC "Non-Functional Requirements Check" as "Non-Functional Dimension Stress Test" using scenario framing.

### Could Do (structural improvements)

- [ ] Promote Pre-Mortem, Walkthrough, Alternative Generation to GLOBAL techniques invokable from any branch. This reduces duplication and signals their cross-context power.
- [ ] Add a "Discriminator" note at the top of CONTEXT-SPECIFIC explaining the IMPROVE vs VERIFY distinction, so future additions maintain the philosophy.
- [ ] Consider adopting Adversarial Collaborator as the unifying persona for all branches, with domain-specific "aspects" (the Fowler aspect, the Klein aspect, etc.) rather than a different persona per branch.

## Meta-Observation

The INFO document's section 9.4 listed distinct personas per branch as a strength. On reflection, this may be a weakness: eight different personas dilute the unifying philosophy. The user's own framing ("matching the persona of the Adversarial Collaborator") suggests a **single** persona with **eight lenses**, not eight personas.

Alternative framing: The Adversarial Collaborator improves research through new evidence; the same Collaborator improves SPEC through new scenarios, improves IMPL through pre-mortems, improves TEST through mutations, etc. The persona is constant; the evidence type varies by context.

## Document History

**[2026-04-30 20:10]**
- Initial review created
- Applied IMPROVE/VERIFY discriminator to all 45 proposed techniques
- Flagged ~11 techniques as verify-territory requiring drop or reframe
- STRUT branch identified as most problematic (4 of 5 techniques are verify)
- Meta-observation: single persona with 8 lenses may be stronger than 8 personas
