# Minto Document Rules

Verification priority:
1. Structural completeness - MINTO tree integrity
2. Logic soundness - MECE, no orphans, closing discipline
3. Evidence traceability - every claim backed by source

## Rule Index

Draft Structure (DS)
- MINTO-DS-01: Exactly 3 candidate arguments present
- MINTO-DS-02: One candidate marked `[RECOMMENDED]` (highest composite score)
- MINTO-DS-03: Selection criteria documented with weights and rationale
- MINTO-DS-04: Findings inventory present with source references and verification labels
- MINTO-DS-05: Source material list present and non-empty

Argument Quality (AQ)
- MINTO-AQ-01: Each A connects to a listener motivator (Magnet Rule)
- MINTO-AQ-02: Questions ordered Why → How → What (no What precedes Why)
- MINTO-AQ-03: One-Argument Test documented per candidate
- MINTO-AQ-04: Each answer is a single declarative sentence

Tree Integrity (TI)
- MINTO-TI-01: Every QnAn has at least one sub-question (S-node)
- MINTO-TI-02: Every sub-question has at least one evidence item (E-node)
- MINTO-TI-03: No orphan nodes (every Q has A, every A has S, every S has E)
- MINTO-TI-04: Every E-node references a source finding from the inventory
- MINTO-TI-05: Maximum 3 questions, 3 answers per question, 3 evidence per sub-question

MECE (ME)
- MINTO-ME-01: Questions under same A do not overlap
- MINTO-ME-02: Answers under same Q do not overlap
- MINTO-ME-03: Evidence items under same S do not overlap

Article Structure (AS)
- MINTO-AS-01: Doc ID assigned in format `[TOPIC]-MINTO-[NN]`
- MINTO-AS-02: Executive Summary restates A (2-3 sentences max)
- MINTO-AS-03: One section per Q with heading derived from question text
- MINTO-AS-04: MINTO tree appendix present and matches prose structure
- MINTO-AS-05: Prose follows top-down order (conclusion, arguments, evidence)

Closing (CL)
- MINTO-CL-01: Closing section present with summary lines grouped by parent Q
- MINTO-CL-02: One summary line per answer
- MINTO-CL-03: Final line restates A as conclusion
- MINTO-CL-04: Closing introduces no claims absent from the tree

## MINTO-DS-01: Exactly 3 Candidates

Draft must contain exactly 3 candidate arguments, each with a complete MINTO Root Section.

**BAD:**
```markdown
## Candidate 1 [RECOMMENDED]
### A: Our tool is better.

## Candidate 2
### A: Speed matters.
```

**GOOD:**
```markdown
## Candidate 1 [RECOMMENDED]
Score: goal_alignment=5, supportability=5, impact=5, specificity=5 (composite: 5.00)
One-Argument Test: passed
### A: The AI research tools everyone uses are built for speed - ours is built for proof.
[Full MINTO Root Section with Q1-Q3 and answers]

## Candidate 2
[Same structure]

## Candidate 3
[Same structure]
```

## MINTO-AQ-01: Magnet Rule

Every root argument must connect to a listener motivator. State the magnet explicitly.

**BAD:**
```markdown
### A: Our platform has good features.
```

**GOOD:**
```markdown
### A: Our platform cuts your audit preparation from 3 weeks to 2 days.
**Magnet**: Saving a resource currently wasted (time on manual audit prep)
```

## MINTO-AQ-02: Question Ordering

Questions must follow Why → How → What. No What-type question may precede a Why-type.

**BAD:**
```markdown
Q1 (What): What features does it have?
Q2 (Why): Why does this matter?
Q3 (How): How does it work?
```

**GOOD:**
```markdown
Q1 (Why): Why does proof matter more than speed?
Q2 (How): How do you actually prove output is correct?
Q3 (What): What does "built for proof" look like in practice?
```

## MINTO-TI-03: No Orphan Nodes

Every branch must terminate at evidence level. No intermediate nodes left without children.

**BAD:**
```markdown
Q1A1: They are beautiful.
  (no sub-question or evidence)
```

**GOOD:**
```markdown
Q1A1: They are beautiful.
  └ Q1A1-S1: "In what way?"
    ├ Q1A1-S1E1: Lovely curves.
    └ Q1A1-S1E2: Modesty in the possessor.
```

## MINTO-TI-04: Evidence References Source

Every E-node must reference a finding from the inventory by ID.

**BAD:**
```markdown
Q1A1-S1E1: AI is unreliable in finance.
```

**GOOD:**
```markdown
Q1A1-S1E1: AI hallucinations generate plausible but factually wrong financial data (F08)
```

## MINTO-ME-01: Questions MECE

Questions under the same argument must not overlap in scope.

**BAD:**
```markdown
Q1: Why is speed important?
Q2: Why does latency matter?
```
(Speed and latency overlap - same concern phrased differently)

**GOOD:**
```markdown
Q1: Why does proof matter more than speed?
Q2: How do you prove output is correct?
Q3: What does this look like vs. generic tools?
```

## MINTO-CL-04: No New Claims in Closing

Closing summarizes proved branches only. Every statement in closing must trace back to a tree node.

**BAD:**
```markdown
## Conclusion
The market is also growing at 46% CAGR, making this an excellent investment.
```
(Market growth claim not present in the MINTO tree)

**GOOD:**
```markdown
## Conclusion
Wrong answers delivered fast destroy value. Speed is commoditized. Fiduciary duty demands demonstrable basis.
The AI research tools everyone uses are built for speed. Ours is built for proof.
```
(Every claim present in tree branches)

## MINTO-AS-04: Appendix Matches Prose

The MINTO tree appendix must structurally match the prose article. Every section heading corresponds to a Q-node. Every paragraph's key claim corresponds to a QnAn-node.

**Verification procedure:**
1. Count prose sections (excluding Executive Summary and Conclusion) = number of Q-nodes
2. Count bold claims per section = number of answers per Q
3. Verify appendix tree has the same Q/A/S/E structure as prose implies
