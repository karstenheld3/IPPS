# Minto Article Guide

Read BEFORE writing. Provides strategic decisions for building AQUASE (Argument-Question-Answer-Subquestion-Evidence) trees and rendering Minto articles.

## 1. Document Types

Two Minto document types exist:

1. **Draft** (`__DRAFT-MINTO_*.md`) - Scaffolding. Contains findings inventory, selection criteria, and 3 scored candidate arguments with AQUASE Root Sections. Deleted by `/cleanup` after article exists.
2. **Article** (`_MINTO_*.md`) - Deliverable. Complete top-down prose article with AQUASE appendix.

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

## 3. Building the AQUASE Tree

### 3.1 Question Ordering

Questions under A follow the Why-How-What principle (Sinek):
- **Q1 (Why)**: Motivation, pain, urgency - always first
- **Q2 (How)**: Mechanism, proof, capability - second
- **Q3 (What)**: Scope, features, description - last

A listener who understands WHY will tolerate HOW and WHAT. A listener who hears WHAT first may never reach WHY.

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

### 4.2 Prose Style

- Write as if the reader has NOT seen the tree - prose must stand alone
- Bold the key claim in each paragraph (the answer being proved)
- Evidence appears as supporting detail within the paragraph, not as a separate list
- Do NOT include AQUASE node IDs in prose sections - the appendix provides the machine-readable structure

### 4.3 Closing Generation

The closing section:
- One summary line per answer, grouped by parent question
- Restate A as final line
- Contains NO claims absent from the tree (nothing new in closing)
- Serves as the "if you remember nothing else" takeaway

## 5. Review Checklist (Self-Check Before Completion)

- [ ] A connects to a listener motivator (magnet)
- [ ] Questions follow Why → How → What order
- [ ] No What-type question precedes a Why-type question
- [ ] Answers within one Q are MECE (Mutually Exclusive, Collectively Exhaustive)
- [ ] Each answer is a single declarative sentence (not compound)
- [ ] Each evidence item is traceable to a source
- [ ] Closing restates only proved branches - no new claims
- [ ] Prose reads naturally without knowledge of the AQUASE structure
- [ ] One-Argument Test considered and documented
