# INFO: EDIRD Phase Model - Variation Comparison

**Doc ID**: EDIRD-IN01
**Goal**: Compare Variation A (Unified) and Variation B (Dual) to support decision on which model to adopt

## Summary

**Variation A (Unified)** - `_SPEC_EDIRD_VARIATION_A_UNIFIED.md [EDIRD-SP02]`
- One model with consistent phase names: EXPLORE, DESIGN, IMPLEMENT, REFINE, DELIVER
- Adapts to BUILD vs SOLVE through verb selection
- Simpler to learn, consistent vocabulary

**Variation B (Dual)** - `_SPEC_EDIRD_VARIATION_B_DUAL.md [EDIRD-SP03]`
- Two models with domain-optimized phase names
- BUILD: SCOPE, ARCHITECT, CODE, HARDEN, SHIP
- SOLVE: UNDERSTAND, FRAME, WORK, POLISH, DELIVER
- More intuitive per domain, but more to learn

## Side-by-Side Comparison

### Phase Names

```
Variation A (Unified)     Variation B: BUILD       Variation B: SOLVE
─────────────────────     ──────────────────       ──────────────────
[EXPLORE]                 [SCOPE]                  [UNDERSTAND]
[DESIGN]                  [ARCHITECT]              [FRAME]
[IMPLEMENT]               [CODE]                   [WORK]
[REFINE]                  [HARDEN]                 [POLISH]
[DELIVER]                 [SHIP]                   [DELIVER]
```

### Conceptual Focus

**Variation A:**
- Universal phases that apply to any work
- Workflow type (BUILD/SOLVE) determines verb emphasis
- "One language, many dialects"

**Variation B:**
- Domain-specific phases optimized for clarity
- Explicit model switching based on output type
- "Right tool for the job"

### Learning Curve

**Variation A:**
- Learn 5 phase names once
- Learn verb sets per workflow type
- Total: 5 phases + verb mapping

**Variation B:**
- Learn 10 phase names (5 per model)
- Verbs naturally grouped by model
- Total: 10 phases + model selection

### Mental Model

**Variation A:**
```
Work → Assess BUILD or SOLVE → Same phases, different verbs
```

**Variation B:**
```
Work → Assess BUILD or SOLVE → Different phases, natural verbs
```

## Evaluation Criteria

### Criterion 1: Ease of Learning

- **A wins**: One set of phase names to memorize
- B requires learning two vocabularies

### Criterion 2: Intuitive Feel

- **B wins**: "SCOPE → ARCHITECT → CODE" feels more natural for coding
- A's "EXPLORE → DESIGN → IMPLEMENT" is generic

### Criterion 3: Consistency Across Domains

- **A wins**: Same terminology whether coding or writing
- B requires mental switching

### Criterion 4: Domain Optimization

- **B wins**: Each model can evolve independently
- A must compromise between domains

### Criterion 5: Communication Clarity

- **Tie**: Both are clear once learned
- A: "I'm in DESIGN phase" (context determines meaning)
- B: "I'm in ARCHITECT phase" (meaning is explicit)

### Criterion 6: Hybrid Work

- **A wins**: Easy to blend code and thinking
- B requires explicit model switching

### Criterion 7: Extensibility

- **B wins**: Can add new models (e.g., TEACH, OPERATE)
- A would need to add more workflow types to single model

## Use Case Analysis

### Use Case: Software Development Team

**Variation A advantages:**
- Consistent vocabulary in standups and documentation
- Everyone speaks same language regardless of task

**Variation B advantages:**
- Code-focused phases match developer mental models
- SOLVE model for architecture decisions, retrospectives

**Winner**: Slight edge to A for team consistency

### Use Case: Individual Knowledge Worker

**Variation A advantages:**
- Simpler to remember
- Smooth transitions between coding and writing

**Variation B advantages:**
- Clear mental switch between "building" and "thinking"
- SOLVE model feels natural for research, writing

**Winner**: Slight edge to B for domain clarity

### Use Case: AI Agent Implementation

**Variation A advantages:**
- Simpler prompt engineering (one model)
- Less branching logic

**Variation B advantages:**
- Clearer tool selection per model
- Easier to optimize each model separately

**Winner**: A for simplicity, B for optimization

## Recommendation Framework

### Choose Variation A (Unified) if:

- Team needs consistent vocabulary
- Work frequently blends code and non-code
- Simplicity is valued over specialization
- Agent implementation needs to be simple

### Choose Variation B (Dual) if:

- Domain clarity is more important than consistency
- Work is clearly either BUILD or SOLVE, rarely mixed
- Team prefers intuitive terminology per domain
- Future extensibility to other models is desired

## Hybrid Option

Could combine approaches:

- Use Variation A phase names (EDIRD) as the standard
- Allow Variation B aliases for domain-specific contexts

```
Standard: EXPLORE, DESIGN, IMPLEMENT, REFINE, DELIVER
BUILD alias: SCOPE, ARCHITECT, CODE, HARDEN, SHIP
SOLVE alias: UNDERSTAND, FRAME, WORK, POLISH, DELIVER
```

This gives:
- One canonical vocabulary for documentation
- Domain-intuitive aliases for daily use
- Best of both worlds, but more complexity

## Decision Factors

**Questions to answer:**

1. How often does your work blend BUILD and SOLVE?
   - Often → A
   - Rarely → B

2. How important is team vocabulary consistency?
   - Very → A
   - Less → B

3. Do you anticipate adding more workflow models?
   - Yes → B
   - No → A

4. Which feels more natural to you?
   - Abstract phases → A
   - Domain phases → B

## Document History

**[2026-01-15 19:20]**
- Initial comparison document created
- Added side-by-side phase comparison
- Added 7 evaluation criteria with analysis
- Added use case analysis (team, individual, AI agent)
- Added recommendation framework
- Added hybrid option consideration
