# Minto Article Guide

Read BEFORE writing. Verify output against `MINTO_RULES.md`.

## 1. AMINTON Notation

MINTO comes from Barbara Minto, "The Pyramid Principle" (3rd ed., 2009) - top-down structure, SCQA introduction, vertical Q&A dialogue, MECE grouping. AMINTON = Agentic MINTO Notation. It extends the Minto Pyramid with two additions: the question is an explicit node type, and the full path is the node ID, so every ID encodes its parentage.

Five node types, four levels:

```
A                 Root argument (the governing thought)
Qn                Question the audience raises against A          (Q1, Q2, Q3)
QnAn              Answer to that question - a declarative claim   (Q1A1, Q1A2)
QnAn-Sn           Sub-question: what must be proved for the answer (Q1A1-S1)
QnAn-SnEn         Evidence answering the sub-question              (Q1A1-S1E2)
```

The hyphen marks the drill-down boundary: `Q1A2` is in the Root Section, `Q1A2-S1E1` is in its drill-down section. `Q2A1-S1E3` reads: second question, first answer, first sub-question, third evidence. Full specification with delivery sections: `[MINTO-IN01]` ("Agentic Minto Articles", IPPS `docs/`, not distributed with the PromptSystem).

## 2. Working Files

Three sequential working file kinds exist under DD-16 and DD-36:

1. **Options** (`MINTO-OPTIONS-NN_[Title].md`) - Working-folder deliverable (not deleted by `/cleanup`). Contains Brief, findings inventory, selection criteria, and 3 scored candidate arguments with AMINTON Root Sections. **Template**: `TEMPLATES/MINTO_OPTIONS_TEMPLATE.md`
   - **AMINTON Options Exemption (DD-43)**: MINTO is exempt from the document-type five-field outline (`Goal`, `Content`, `Evidence`, `Reason`, `Handoff`). The candidate outline takes the form of an AMINTON Q/A tree with declarative answer claims. Quality gates applying to MINTO OPTIONS evaluate the tree structure and candidate scores, not the five-field format.
2. **Draft** (`MINTO-DRAFT-NN_[Title].md`) - Working-folder deliverable (not deleted by `/cleanup`). Expands the chosen candidate into full AMINTON drill-down branches and section scaffolding before drafting prose.
3. **Output** (`YYYY-MM-DD_[Title].md`) - Final publication deliverable in the working folder. Complete top-down prose article with AMINTON tree appendix. **Template**: `TEMPLATES/MINTO_TEMPLATE.md`

## 3. Planning Decisions

### 3.1 Before Generating Candidates

Answer these before building the findings inventory:

1. **What is the article's purpose?** (persuade, explain, propose, investigate)
2. **Who is the audience?** (role, expertise, decision power, existing beliefs)
3. **What action should the audience take?** (approve, buy, change, investigate)
4. **What does the audience already want or fear?** (the magnet)

Record the answers in the `## Brief` section of the OPTIONS file (Purpose, Audience, Reader outcome `do`, Audience `needs`) together with the user's request as Mandate. Goal Alignment and Impact scores are measured against these Brief fields.

### 3.2 Magnet Rule

The root argument (A) must connect to at least one audience motivator:
- Gaining an advantage others lack
- Reducing a risk currently carried
- Saving a resource currently wasted
- Gaining access otherwise unavailable

If A does not hit a magnet, the tree will not move the audience to action - regardless of evidence quality. Test every candidate against the magnet before scoring. This is a candidate-viability filter, not a framing device. The SCQA introduction (Section 5.1) handles reader engagement at presentation time.

### 3.3 Argument Selection Strategy

When scoring candidates, weight dimensions by article purpose:
- **Sales pitch**: Goal Alignment (30%), Supportability (30%), Impact (25%), Specificity (15%)
- **Investment proposal**: Supportability (35%), Specificity (30%), Impact (20%), Goal Alignment (15%)
- **Investigative**: Supportability (40%), Specificity (30%), Impact (20%), Goal Alignment (10%)

Override defaults when user provides explicit criteria.

## 4. Building the AMINTON Tree

**The tree is the primary working artifact.** Never write prose without a complete AMINTON tree. The tree prevents drift: every paragraph must serve a node, every heading must map to a Q, every claim must trace to a QnAn. If you cannot map output back to the tree, the output does not belong.

Sequence (no exceptions):
1. Think bottom-up: extract findings, group, synthesize upward into candidate arguments
2. Build the tree: A → Qs → QnAns → QnAn-Sn → QnAn-SnEn
3. Verify the tree: MECE, no orphans, logical ordering, same kind same level
4. THEN write prose top-down from the verified tree

Do not start prose (Section 5) before the tree passes verification. Do not modify prose without checking the tree first.

### 4.1 Question Ordering

Questions under A arise from what the governing thought naturally raises in the audience's mind. The ordering follows one of Minto's four logical methods (comparative, chronological, structural, deductive) - never arbitrary.

**Common question patterns** (from Minto, Exhibit 12):

- **Something went wrong** → What do we do?
- **Something could go wrong** → How can we prevent it?
- **Something has changed** → What should we do?
- **Someone disagrees** → Who is right?

**Sinek heuristic (Why-How-What)** - useful default for persuasive/sales arguments:
- **Q1 (Why)**: Motivation, pain, urgency - lead with this when the audience does not yet feel the problem
- **Q2 (How)**: Mechanism, proof, capability - follow when the audience needs to believe it works
- **Q3 (What)**: Scope, features, description - last, because What without Why has no pull

A audience who understands WHY will tolerate HOW and WHAT. But this is a starting heuristic, not a law.

**Other valid orderings** (examples from Minto):
- **Chronological**: "What happened? What caused it? What should we do next?" (investigation)
- **Structural**: "What are the three divisions' problems?" (one Q per organizational unit)
- **Comparative**: "Which option is best? What are the trade-offs? What is the risk?" (evaluation)
- **Single-question**: "Why should we replace the current system?" with multiple independent answers below (the simplest and often strongest structure)

**Decision rule**: Choose the ordering that matches how the grouping was formed. If you reasoned by weighing impact, use comparative (most important first). If you traced a causal chain, use chronological. If you divided a system into parts, use structural.

### 4.2 The One-Argument Test

Before finalizing a multi-question tree, ask: "Can I collapse this into ONE question with three answers?" If yes, consider whether a single powerful question with deeper evidence might be more focused. This is a diagnostic, not a directive - multi-question structures are Minto's expected norm (3-5 Key Line points at level 2).

### 4.3 Evidence Selection

For each sub-question (S-node), select evidence that:
1. **Is traceable** - references a specific finding from the inventory with source
2. **Is concrete** - numbers, dates, names, quoted text (not vague claims)
3. **Is independent** - does not restate the parent answer in different words

### 4.4 Structure Constraints

- 3 questions preferred, up to 5 when the argument requires independent dimensions (Q1...Q5)
- Maximum 3 answers per question (QnA1, QnA2, QnA3) - fewer is acceptable
- Maximum 3 evidence items per sub-question (QnAn-S1E1...E3) - fewer is acceptable
- These are cognitive load limits, not minimum requirements

### 4.5 Structure Visualization

When the AMINTON tree has 3+ Q-branches, add a tree diagram before the Executive Summary. The diagram uses Unicode box-drawing characters per `ASCII_ART_GUIDES.md`. Purpose: reader sees the argument structure at a glance before reading prose. The tree diagram supplements the AMINTON tree appendix (machine-readable) with a visual rendering for human readers.

**Format rules:**
- Label the root argument `Argument:` (not `A`) - readable without AMINTON knowledge
- Continue multi-line argument text with `│` prefix, not blank-space indentation
- Separate argument from questions with a bare `│` line
- Use `├─ Qn  ` (2 spaces after Qn) for question branches
- Wrap long evidence lines with `│   │       ` continuation
- Precede the diagram with one sentence explaining what A and Q1-Q4 mean and how the parts map to the article structure
- Keep all lines up to 100 chars to avoid wrapping on narrow viewports
- Example:

```
The article argues one governing thesis (A) and answers four questions (Q1-Q4)
a reader would raise against it. Part I provides the evidence base, Part II makes
the argument, Part III turns it into a playbook.

PART I   Situation: [one-line summary]
            │
            v
Argument:  [Root argument A - first line]
│          [continuation lines with │ prefix]
│
├─ Q1  [Question 1]
│   ├─ [evidence - keep up to 100 chars, wrap with │   │       ]
│   ├─ [evidence]
│   └─ [evidence]
├─ Q2  [Question 2]
│   ├─ [evidence]
│   └─ [evidence]
└─ Q3  [Question 3]
    ├─ [evidence]
    └─ [evidence]
            │
            v
PART III [one-line summary]
```

## 5. Writing the Prose Article

Prose is DERIVED FROM the completed tree, not written independently. Every paragraph must map to an AMINTON node. If prose drifts from the tree, the fix is always: update the tree first, then regenerate prose from it.

### 5.1 Top-Down Order

Prose follows conclusion-first structure:
1. **Executive Summary (SCQA)** - Situation (what reader already knows, 1-2 sentences) → Complication (what changed or threatens, 1-2 sentences) → Answer (restate A). Total: 2-3 paragraphs max. The reader must feel the need before receiving the answer.
2. **Section per Q** - Each question becomes a heading; answers become paragraphs
3. **Evidence woven in** - S/E level content supports paragraphs without explicit node IDs
4. **Conclusion** - Summarize proved branches, restate A

### 5.2 Summarize Don't Label (Minto's Rule 1)

Every summary statement - headings, opening sentences, answer nodes - must capture the *significance* of what follows, not merely label its category. This is the single most common writing failure Minto identifies.

**The test**: Does the summary communicate something meaningful even if the reader never reads the details below?

- **BAD** (labels): "The company has three problems." / "Background" / "Findings" / "Analysis"
- **GOOD** (summaries): "Three structural problems prevent effective delegation." / "Phase 1 delivers 80% of the cost reduction."

Apply to:
- **Section headings** - State the idea, not the topic. Reading headings alone should tell the article's story.
- **Answer nodes** - Each QnAn must be a complete declarative claim, not a topic pointer.
- **Opening sentences** - Each paragraph's first sentence summarizes the paragraph's point.

Minto: "If you formulate your headings properly, they will stand in the table of contents as a precis of your report."

### 5.3 Prose Style

- Write as if the reader has NOT seen the tree - prose must stand alone
- Bold the key claim in each paragraph (the answer being proved)
- Evidence appears as supporting detail within the paragraph, not as a separate list
- Do NOT include AMINTON node IDs in prose sections - the appendix provides the machine-readable structure
- Default to **inductive** presentation (state the point, then support) - reserve deductive chains for paragraph level where premises stay close together

### 5.4 Closing Generation

The closing section:
- One summary line per answer, grouped by parent question
- Restate A as final line
- Contains NO claims absent from the tree (nothing new in closing)
- Serves as the "if you remember nothing else" takeaway

### 5.5 Revision: Two Diagnostic Tests

Apply at every level during revision:
- **"So what?"** - If you cannot answer clearly, the statement does not belong. Removes filler, strengthens cause-effect.
- **"Why is that true?"** - Validates claims or exposes hidden assumptions. Surfaces weakness before the reader does.

## 6. Process Checklist (Before Completion)

- [ ] Planning decisions documented (purpose, audience, action, magnet)
- [ ] AMINTON tree complete and verified BEFORE prose was written
- [ ] One-Argument Test considered and result documented
- [ ] Same Kind, Same Level: all items in each grouping describable by one plural noun
- [ ] Scoring criteria selected for article purpose (Section 3.3)
- [ ] Evidence evaluated for concreteness and independence (Section 4.3)
- [ ] Every prose paragraph maps to an AMINTON node (no unmapped content)
- [ ] Headings state ideas not categories - reading headings alone tells the story (Section 5.2)
- [ ] "So what?" and "Why is that true?" applied at every level (Section 5.5)
- [ ] Prose tested for standalone readability (no tree knowledge required)
- [ ] Run `/verify` against `MINTO_RULES.md` for structural compliance

## 7. Named Failure Modes

When reviewing or critiquing MINTO articles, verify against these nine technique-specific failure modes (reference AMINTON node IDs in findings):

1. **Magnet failure** - Root argument A does not connect to an audience motivator (advantage, risk reduction, resource saving, access; `MINTO-AQ-01`).
2. **Circular evidence** - Evidence node (E-node) restates the parent answer instead of providing independent proof.
3. **False MECE** - Questions or answers appear distinct but testing reveals logical overlap or gaps (`MINTO-ME-01`).
4. **Unsupported claim** - Answer claim in prose has no corresponding E-node in the appendix tree.
5. **Closing creep** - Closing section adds nuance, qualification, or claims absent from the tree (`MINTO-CL-04`).
6. **Single-source dependency** - Entire argument branch rests on a single finding that could be erroneous.
7. **Misapplied statistic** - Evidence cited does not actually support the quantitative claim made (`SOCAS-GN-04`).
8. **Absolute claim vulnerability** - Unqualified generalizations ("all", "none", "always", "never") invite immediate counter-examples.
9. **Hidden trade-off** - Positioning argument obscures an obvious buyer objection, known downside, or operational cost.
