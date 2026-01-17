<DevSystem EmojisAllowed=true />

# Devil's Advocate Review 2: STRUT Example Case Simulations

**Reviewed**: 2026-01-17 17:05
**Document**: `INFO_STRUT_EXAMPLE_CASE_SIMULATION.md [STRUT-IN03]`
**Focus**: LLM interpretability, cognitive load, notation ambiguity

## Key Constraint

**STRUT is LLM-evaluated, not machine-parsed.** Formal parsing concerns (BPMN gateways, process algebra deadlock detection, DSL anti-patterns) from Review 1 are irrelevant. We only need notation that is **unambiguous for LLM and human readers**.

## MUST-NOT-FORGET

1. STRUT is read by LLMs - clarity over formal syntax
2. Gate checks require evidence - artifacts must exist
3. STRUT should be phase-model agnostic (not hardcode EDIRD)
4. Single developer assumption is intentional
5. Decomposition trigger is complexity-based
6. Cognitive load: humans hold ~4 chunks in working memory

## MUST-RESEARCH

1. **LLM instruction clarity** - What makes prompts unambiguous for LLMs?
2. **Cognitive load in notation** - How much complexity before readers lose track?
3. **Pseudocode conventions** - How do established standards handle branching?
4. **Checklist design** - How to structure pass/fail states clearly?
5. **Progressive disclosure** - How to layer complexity without overwhelming?

## Industry Research Findings

**LLM Prompt Engineering Best Practices** (Palantir):
- Be clear and specific - straightforward language, no overloading
- Provide context to anchor interpretation
- Break complex tasks into simpler parts
- Use examples to establish patterns

**Cognitive Load Theory** (Zakirullin):
- Humans hold ~4 chunks in working memory
- Extraneous cognitive load (presentation complexity) can be reduced
- Nested conditions increase load exponentially
- Early returns and named intermediates reduce load
- Descriptive names let readers skip over details

**Implications for STRUT**:
- Each case should be scannable in <4 chunks at any nesting level
- Named patterns (like "step 1:", "endpoint A:") reduce load
- Deeply nested structures (Case 6 NEST) push cognitive limits

## Critical Issues

### ❌ C-01: Inconsistent nesting depth creates cognitive overload

**What**: Case 6 (NEST pattern) has 4+ levels of indentation inside the `[SOLVE]` block. Case 7 failure handling has 5 levels.

**Where**: Case 6 lines 394-416, Case 7 lines 484-493

**Why it's problematic**: LLMs and humans both struggle with deeply nested structures. Research shows >3 levels significantly increases misinterpretation risk.

**Example**:
```
├─ ┌─ [SOLVE](EVALUATION): "Which email provider?"
│  │  [EXPLORE]:
│  │  ├─ [RESEARCH](sendgrid)
│  │  │   └─ -FAIL -> [CONSULT]
```
This is 4 levels before reaching the actual verb.

**Suggested fix**: Flatten NEST by referencing external sub-workflow:
```
├─ [SOLVE](EVALUATION): "Which email provider?" -> see: EMAIL_PROVIDER_EVAL
│   └─ -FAIL -> [CONSULT](product owner)
```

### ❌ C-02: Gate checkbox semantics unclear for partial completion

**What**: Case 9 shows `[x] C DEFERRED` and `[x] D DEFERRED` as checked items. Does `[x]` mean "addressed" or "completed successfully"?

**Where**: Case 9 lines 656-661

**Why it's problematic**: An LLM reading this might interpret `[x]` as "done" when it actually means "acknowledged but not done". This ambiguity could cause incorrect workflow progression.

**Suggested fix**: Use different markers:
- `[x]` - completed successfully
- `[~]` - deferred/partial
- `[ ]` - not addressed

Or use explicit labels: `[DEFERRED] C - architectural decision needed`

### ❌ C-03: Arrow (->) overloaded but LLM-interpretable in context

**What**: Review 1 flagged `->` having multiple meanings. However, for LLM interpretation this is NOT a problem because:
- Context disambiguates: `-FAIL ->` is clearly a failure handler
- `Gate: ... -> SKIP` is clearly a conditional skip
- Phase headers like `EXPLORE -> IMPLEMENT` are clearly transitions

**Resolution**: This is NOT a critical issue for LLM evaluation. The context provides sufficient disambiguation. **Dismiss C-01 from Review 1.**

## High Priority Issues

### ⚠️ H-01: Phase names hardcoded (violates phase-model agnosticism)

**What**: All cases use `[EXPLORE]`, `[DESIGN]`, `[IMPLEMENT]`, `[REFINE]`, `[DELIVER]` explicitly.

**Where**: Throughout all 10 cases

**Why it matters**: STRUT claims to be phase-model agnostic, but these examples tightly couple to EDIRD. If someone uses a different phase model (e.g., Kanban with just "TODO/DOING/DONE"), these examples don't translate.

**Suggested fix**: Either:
1. Accept that STRUT examples are EDIRD-specific (update claims)
2. Add alternative examples with different phase models
3. Use generic phase labels `[PHASE-1]`, `[PHASE-2]` with EDIRD as one binding

### ⚠️ H-02: Verb parameters lack type hints

**What**: Parameters like `[ASSESS](COMPLEXITY-MEDIUM)` vs `[ASSESS](EVALUATION)` use same verb with different parameter types (complexity level vs problem type).

**Where**: Case 2 line 109 vs Case 4 line 242

**Why it matters**: LLM might conflate these. Is `EVALUATION` a complexity level or problem type?

**Suggested fix**: Use explicit type prefixes when ambiguous:
- `[ASSESS](complexity: MEDIUM)`
- `[ASSESS](type: EVALUATION)`

### ⚠️ H-03: Repetition notation not consistently applied

**What**: Some cases use `|: [VERB] :| xN` for bounded retry, others use prose like "attempt monolithic" followed by numbered failures.

**Where**: Case 2 line 107 uses `|: :| x3`, Case 8 lines 557-561 uses prose

**Why it matters**: Inconsistent notation increases cognitive load. LLM must parse two different patterns for the same concept.

**Suggested fix**: Standardize on one notation. If prose is clearer, use it everywhere. If `|: :| xN` is the standard, apply it consistently.

## Medium Priority Issues

### ⚡ M-01: No explicit success path after -FAIL handlers

**What**: Failure handlers show what to do on failure, but don't explicitly show return to normal flow.

**Where**: Throughout, e.g., Case 7 lines 485-493

**Example**:
```
├─ |: [TEST](sandbox) :| x3
│   ├─ -FAIL: undocumented api behavior
│   │   └─ [FIX](adjust to actual response)
```

**Question**: After `[FIX]`, does control return to `[TEST]` for retry, or continue to next step? The implicit assumption is retry, but it's not stated.

**Suggested fix**: Add explicit continuation:
```
│   ├─ -FAIL: undocumented_api_behavior
│   │   └─ [FIX](adjust to actual response) -> retry
```

### ⚡ M-02: DONE semantics vary

**What**: Some cases end with `└─> DONE`, others with `└─> DONE: Decision = PostgreSQL`, others with `└─> EXIT: ABORTED`.

**Where**: Case 4 line 293, Case 7 line 529

**Why it matters**: These represent different workflow outcomes but use similar syntax. An LLM tracking workflow state needs to distinguish between successful completion, partial completion, and abort.

**Suggested fix**: Standardize terminal states:
- `DONE` - successful completion
- `DONE(partial: 3/5)` - partial completion with count
- `DONE(output: Decision = X)` - completion with output
- `ABORTED(reason)` - workflow terminated

### ⚡ M-03: Step numbering vs step naming inconsistent

**What**: Case 3 uses "step 1:", "step 2:", etc. Case 9 uses "endpoint A:", "endpoint B:", etc.

**Where**: Case 3 lines 180-204, Case 9 lines 627-653

**Why it matters**: Both are valid approaches, but mixing them in the same document creates pattern inconsistency.

**Suggested fix**: Document when to use each:
- Numbered steps: sequential, order matters
- Named items: parallel or independent, order flexible

## Questions That Need Answers

1. **Should STRUT support non-EDIRD phase models?** If yes, examples needed. If no, update claims.

2. **What's the maximum nesting depth for LLM reliability?** Testing needed to find where LLMs start misinterpreting.

3. **Should gate items have required vs optional distinction?** Some gates seem mandatory, others informational.

4. **How should parallel execution be notated?** Current notation is purely sequential.

## Devil's Advocate Summary

**Reviewed**: INFO_STRUT_EXAMPLE_CASE_SIMULATION.md [STRUT-IN03]
**Time spent**: ~15 minutes

**Research Topics Investigated**:
1. LLM instruction clarity - Clear, specific, contextual prompts work best
2. Cognitive load - 4-chunk limit, nesting increases load exponentially
3. Pseudocode conventions - Consistent structure aids parsing
4. Checklist design - Clear pass/fail semantics essential
5. Progressive disclosure - Layer complexity, don't dump it

**Findings**:
- ❌ CRITICAL: 2
- ⚠️ HIGH: 3
- ⚡ MEDIUM: 3
- LOW: 0

**Top 3 Risks**:
1. Deep nesting in NEST pattern exceeds cognitive/LLM limits
2. Gate checkbox semantics ambiguous for deferred items
3. Phase-model coupling contradicts agnosticism claim

**Dismissed from Review 1**:
- C-01 (arrow overloading) - LLM handles context-based disambiguation fine
- BPMN/Process Algebra concerns - irrelevant for LLM-evaluated notation

**Industry Alternatives Identified**:
- Flatten nested workflows via references (like function calls)
- Use explicit type hints for ambiguous parameters

**Files Created/Updated**:
- `INFO_STRUT_EXAMPLE_CASE_SIMULATION_REVIEW_2.md` - This review

**Recommendation**: PROCEED WITH CAUTION - Address C-01 (nesting depth) and C-02 (checkbox semantics) before formalizing STRUT spec.
