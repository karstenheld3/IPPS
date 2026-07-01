# Minto Article Guide

Read BEFORE writing. Verify output against `MINTO_RULES.md`. For notation details, see `_INFO_AGENTIC_MINTO_ARTICLES.md [MINTO-IN01]`.

## 1. Document Types

Two Minto document types exist:

1. **Draft** (`__DRAFT-MINTO_*.md`) - Scaffolding. Contains findings inventory, selection criteria, and 3 scored candidate arguments with MINTO Root Sections. Deleted by `/cleanup` after article exists.
2. **Article** (`_MINTO_*.md`) - Deliverable. Complete top-down prose article with MINTO tree appendix.

## 2. Planning Decisions

### 2.1 Before Generating Candidates

Answer these before building the findings inventory:

1. **What is the article's purpose?** (persuade, explain, propose, investigate)
2. **Who is the listener?** (role, expertise, decision power, existing beliefs)
3. **What action should the listener take?** (approve, buy, change, investigate)
4. **What does the listener already want or fear?** (the magnet)

### 2.2 Magnet Rule

The root argument (A) must connect to at least one listener motivator:
- Gaining an advantage others lack
- Reducing a risk currently carried
- Saving a resource currently wasted
- Gaining access otherwise unavailable

If A does not hit a magnet, the tree will not move the listener to action - regardless of evidence quality. Test every candidate against the magnet before scoring.

### 2.3 Argument Selection Strategy

When scoring candidates, weight dimensions by article purpose:
- **Sales pitch**: Goal Alignment (30%), Supportability (30%), Impact (25%), Specificity (15%)
- **Investment proposal**: Supportability (35%), Specificity (30%), Impact (20%), Goal Alignment (15%)
- **Investigative**: Supportability (40%), Specificity (30%), Impact (20%), Goal Alignment (10%)

Override defaults when user provides explicit criteria.

## 3. Building the MINTO Tree

### 3.1 Question Ordering

Questions under A arise from what the governing thought naturally raises in the listener's mind. The ordering follows one of Minto's four logical methods (comparative, chronological, structural, deductive) - never arbitrary.

**Common question patterns** (from Minto, Exhibit 12):

- **Something went wrong** → What do we do?
- **Something could go wrong** → How can we prevent it?
- **Something has changed** → What should we do?
- **Someone disagrees** → Who is right?

**Sinek heuristic (Why-How-What)** - useful default for persuasive/sales arguments:
- **Q1 (Why)**: Motivation, pain, urgency - lead with this when the listener does not yet feel the problem
- **Q2 (How)**: Mechanism, proof, capability - follow when the listener needs to believe it works
- **Q3 (What)**: Scope, features, description - last, because What without Why has no pull

A listener who understands WHY will tolerate HOW and WHAT. But this is a starting heuristic, not a law.

**Other valid orderings** (examples from Minto):
- **Chronological**: "What happened? What caused it? What should we do next?" (investigation)
- **Structural**: "What are the three divisions' problems?" (one Q per organizational unit)
- **Comparative**: "Which option is best? What are the trade-offs? What is the risk?" (evaluation)
- **Single-question**: "Why should we replace the current system?" with multiple independent answers below (the simplest and often strongest structure)

**Decision rule**: Choose the ordering that matches how the grouping was formed. If you reasoned by weighing impact, use comparative (most important first). If you traced a causal chain, use chronological. If you divided a system into parts, use structural.

### 3.2 The One-Argument Test

Before finalizing a multi-question tree, ask: "Can I collapse this into ONE question with three answers?" If yes, the tree is likely stronger with one powerful question and deeper evidence. Multiple top-level questions dilute each other when time is limited.

### 3.3 Evidence Selection

For each sub-question (S-node), select evidence that:
1. **Is traceable** - references a specific finding from the inventory with source
2. **Is concrete** - numbers, dates, names, quoted text (not vague claims)
3. **Is independent** - does not restate the parent answer in different words

### 3.4 Structure Constraints

- Maximum 3 questions per argument (Q1, Q2, Q3) - fewer is acceptable
- Maximum 3 answers per question (QnA1, QnA2, QnA3) - fewer is acceptable
- Maximum 3 evidence items per sub-question (QnAn-S1E1...E3) - fewer is acceptable
- These are cognitive load limits for delivery, not minimum requirements

## 4. Writing the Prose Article

### 4.1 Top-Down Order

Prose follows conclusion-first structure:
1. **Executive Summary** - Restate A as opening (2-3 sentences)
2. **Section per Q** - Each question becomes a heading; answers become paragraphs
3. **Evidence woven in** - S/E level content supports paragraphs without explicit node IDs
4. **Conclusion** - Summarize proved branches, restate A

### 4.2 Summarize Don't Label (Minto's Rule 1)

Every summary statement - headings, opening sentences, answer nodes - must capture the *significance* of what follows, not merely label its category. This is the single most common writing failure Minto identifies.

**The test**: Does the summary communicate something meaningful even if the reader never reads the details below?

- **BAD** (labels): "The company has three problems." / "Background" / "Findings" / "Analysis"
- **GOOD** (summaries): "Three structural problems prevent effective delegation." / "Phase 1 delivers 80% of the cost reduction."

Apply to:
- **Section headings** - State the idea, not the topic. Reading headings alone should tell the article's story.
- **Answer nodes** - Each QnAn must be a complete declarative claim, not a topic pointer.
- **Opening sentences** - Each paragraph's first sentence summarizes the paragraph's point.

Minto: "If you formulate your headings properly, they will stand in the table of contents as a precis of your report."

### 4.3 Prose Style

- Write as if the reader has NOT seen the tree - prose must stand alone
- Bold the key claim in each paragraph (the answer being proved)
- Evidence appears as supporting detail within the paragraph, not as a separate list
- Do NOT include MINTO node IDs in prose sections - the appendix provides the machine-readable structure
- Default to **inductive** presentation (state the point, then support) - reserve deductive chains for paragraph level where premises stay close together

### 4.4 Closing Generation

The closing section:
- One summary line per answer, grouped by parent question
- Restate A as final line
- Contains NO claims absent from the tree (nothing new in closing)
- Serves as the "if you remember nothing else" takeaway

### 4.5 Revision: Two Diagnostic Tests

Apply at every level during revision:
- **"So what?"** - If you cannot answer clearly, the statement does not belong. Removes filler, strengthens cause-effect.
- **"Why is that true?"** - Validates claims or exposes hidden assumptions. Surfaces weakness before the reader does.

## 5. Process Checklist (Before Completion)

- [ ] Planning decisions documented (purpose, listener, action, magnet)
- [ ] One-Argument Test considered and result documented
- [ ] Scoring criteria selected for article purpose (Section 2.3)
- [ ] Evidence evaluated for concreteness and independence (Section 3.3)
- [ ] Headings state ideas not categories - reading headings alone tells the story (Section 4.2)
- [ ] "So what?" and "Why is that true?" applied at every level (Section 4.5)
- [ ] Prose tested for standalone readability (no tree knowledge required)
- [ ] Run `/verify` against `MINTO_RULES.md` for structural compliance
