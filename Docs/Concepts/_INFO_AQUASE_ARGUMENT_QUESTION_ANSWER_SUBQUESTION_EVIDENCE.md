# INFO: AQUASE - Argument-Question-Answer-Subquestion-Evidence

**Doc ID**: AQUASE-IN01
**Goal**: Define the AQUASE notation system for structured argumentation using section-based delivery with path-based node IDs

## Summary

- AQUASE (Argument-Question-Answer-Subquestion-Evidence) structures arguments into 4 sections + closing for verbal delivery [VERIFIED]
- Root section: A (thesis) → Q1...Qn (questions) → QnA1...QnAn (answers per question) [VERIFIED]
- Drill-down sections (A, B, C): Each expands one Q-branch with sub-questions and evidence [VERIFIED]
- Closing section: Summarizes proved branches and restates A as conclusion [VERIFIED]
- IDs concatenate within a section (QnAn), hyphens mark section boundaries (QnAn-SnEn) [VERIFIED]
- Applicable to any field requiring structured argumentation: sales, investment, journalism, policy, legal [VERIFIED]

## Table of Contents

1. [The Problem AQUASE Solves](#1-the-problem-aquase-solves)
2. [ID System](#2-id-system)
3. [Section Structure](#3-section-structure)
4. [Delivery Mechanics](#4-delivery-mechanics)
5. [Full Example](#5-full-example)
6. [Applied Examples](#6-applied-examples)
7. [Sources](#7-sources)
8. [Document History](#8-document-history)

## 1. The Problem AQUASE Solves

Minto's Pyramid Principle defines the argumentative logic (top-down, SCQA (Situation-Complication-Question-Answer), vertical Q&A dialogue, MECE (Mutually Exclusive, Collectively Exhaustive) grouping) and discusses decimal numbering (1, 1.1, 1.1.1) as one of several presentation options to make pyramid structure visible in documents (Ch. 6, "How to Highlight the Structure"). However, Minto's decimal numbering encodes position within a flat outline, not the Q&A relationship between levels. The question that connects a parent claim to its supporting evidence remains invisible in the numbering - you see hierarchy but not WHY the next level exists.

AQUASE makes two additions: 1) Q becomes an explicit node type (not just an implied relationship), and 2) the full path IS the ID, encoding parentage directly. Reading `Q1A2-S1E3` tells you exactly where in the argument structure you are and who the parent is at every level.

## 2. ID System

### 2.1 Core Rules

- **A** = Root argument (thesis / hook) - one per tree
- **Q** = Question (raised by the preceding argument)
- **QnAn** = Answer to question n, answer number n (concatenated within a section)
- **S** = Sub-question (drill-down question within a section)
- **E** = Evidence (answers a sub-question)
- **Hyphen** = Section boundary (separates root-level from drill-down level)
- Numbers are LOCAL within their parent (restart at 1 per parent)

### 2.2 Level Structure

```
Level 0: A                          (root argument / thesis)
Level 1: Q1, Q2, Q3                 (questions raised by A)
Level 2: Q1A1, Q1A2, Q2A1, ...     (answers per question)
Level 3: Q1A1-S1, Q1A2-S1, ...     (sub-questions per answer - hyphen marks section boundary)
Level 4: Q1A1-S1E1, Q1A1-S1E2, ... (evidence answering sub-questions)
```

### 2.3 Reading an ID

`Q2A1-S1E3` reads as: "Second question's first answer (Q2A1), drilled into its first sub-question (S1), third piece of evidence (E3)."

### 2.4 Hyphen Rule

Hyphens appear ONLY at section boundaries - the transition from Root Section into drill-down Sections A/B/C:
- `Q1A2` = no hyphen (within Root Section)
- `Q1A2-S1` = hyphen (entering Section A's drill-down)
- `Q1A2-S1E1` = one hyphen total (evidence in Section A)

This keeps IDs short and visually distinguishes overview (Root) from depth (Sections).

## 3. Section Structure

```
A: Pigs should be kept as pets.
├ Q1: "Why?"
│ ├ Q1A1: They are beautiful.
│ └ Q1A2: They are marvellously fat.
│
└ Q2: "How?"
  └ Q2A1: They could be bred to fascinating variations.


A: Pigs should be kept as pets.
└ Q1: "Why?"
  ├ Q1A1: They are beautiful.
  │ └ Q1A1-S1: "In what way?"
  │   ├ Q1A1-S1E1: Presence proves lovely curves to the onlooker.
  │   └ Q1A1-S1E2: Greater modesty in the possessor.
  │
  └ Q1A2: They are marvellously fat.
    └ Q1A2-S1: "Why does that matter?"
      └ Q1A2-S1E1: Symbols linked to the land - so English they deserve the national symbol.

A: Pigs should be kept as pets.
└ Q2: "How?"
  └ Q2A1: They could be bred to fascinating variations.
    └ Q2A1-S1: "What variations?"
      ├ Q2A1-S1E1: In types.
      ├ Q2A1-S1E2: In size.
      ├ Q2A1-S1E3: In personalities.
      └ Q2A1-S1E4: In functions.

Q1 "Why?": They are beautiful - in curves and modesty.
Q1 "Why?": They are fat - symbolically English.
Q2 "How?": They can be bred to fascinating variations in type, size, personality, and function.
└─> A: Pigs should be kept as pets.
```

An AQUASE tree is delivered in 4 sections + closing:

### 3.1 Root Section

Contains the thesis, all questions, and all top-level answers. Gives the listener the complete overview.

```
A: [Root argument]
├ Q1: "[Question 1]"
│ ├ Q1A1: [Answer]
│ ├ Q1A2: [Answer]
│ └ Q1A3: [Answer]
├ Q2: "[Question 2]"
│ ├ Q2A1: [Answer]
│ └ Q2A2: [Answer]
└ Q3: "[Question 3]"
  ├ Q3A1: [Answer]
  ├ Q3A2: [Answer]
  └ Q3A3: [Answer]
```

### 3.2 Sections A, B, C (Drill-Down)

Each section expands one Q-branch. Starts from A, narrows to the relevant Q, then drills each answer into sub-questions and evidence.

```
A: [Root argument]
└ Qn: "[Question n]"
  ├ QnA1: [Answer]
  │ └ QnA1-S1: "[Sub-question]"
  │   ├ QnA1-S1E1: [Evidence]
  │   ├ QnA1-S1E2: [Evidence]
  │   └ QnA1-S1E3: [Evidence]
  ├ QnA2: [Answer]
  │ └ QnA2-S1: "[Sub-question]"
  │   └ QnA2-S1E1: [Evidence]
  └ QnA3: [Answer]
    └ QnA3-S1: "[Sub-question]"
      ├ QnA3-S1E1: [Evidence]
      └ QnA3-S1E2: [Evidence]
```

### 3.3 Closing Section

Summarizes each Q-branch as proved, then restates A as conclusion:

```
Q1 "[Question 1]": [Summary of Q1A1]
Q1 "[Question 1]": [Summary of Q1A2]
Q1 "[Question 1]": [Summary of Q1A3]
Q2 "[Question 2]": [Summary of Q2A1]
Q2 "[Question 2]": [Summary of Q2A2]
Q3 "[Question 3]": [Summary of Q3A1]
Q3 "[Question 3]": [Summary of Q3A2]
Q3 "[Question 3]": [Summary of Q3A3]
└─> A: [Root argument restated as conclusion]
```

One summary line per answer. Lines are grouped by their parent Q, with the question text repeated.

### 3.4 Constraints

- **Maximum 3 questions** per level (Q1, Q2, Q3) - fewer is fine
- **Maximum 3 answers** per question (QnA1, QnA2, QnA3) - fewer is fine
- **Maximum 3 evidence** per sub-question (QnAn-S1E1...E3) - fewer is fine
- These are cognitive load limits for verbal delivery, not structural requirements

The Pigs example demonstrates variable structure: Q1 has 2 answers, Q2 has 1. Section A has 2 evidence items under Q1A1 and 1 under Q1A2. Section B has 4 evidence items under Q2A1 (exceeding 3 where the content demands it).

A maxed-out 3x3 tree would contain:
- Root Section: 1 + 3 + 9 = 13 nodes
- Sections A + B + C: 9 answers x (1 sub-question + 3 evidence) = 36 nodes
- Closing: up to 9 summary lines + 1 conclusion
- But most real arguments are asymmetric - some branches are deeper, others are thin

## 4. Delivery Mechanics

### 4.1 Delivery Order

1. **Root Section** - always delivered in full (overview)
2. **Sections A/B/C** - selectively, based on listener interest or time
3. **Closing** - always delivered (locks in the conclusion)

### 4.2 Filler Sentences for Section Transitions

- **A → Q1** (opening): "That raises three questions. The first..."
- **Q1 answers → Q2** (next question): "That was the first question. The second..."
- **Q3 answers → Section A** (drill-down): "Let me go deeper on the first point..."
- **Section A → Section B** (next drill-down): "Now for the second question in more detail..."
- **Last section → Closing**: "So, putting it all together..."
- **Closing → A**: "And that is why [root argument]."

### 4.3 Selective Depth

In live delivery, not every section needs to be presented:
- Always deliver: Root Section + Closing
- Optionally deliver: 1-3 drill-down sections based on listener interest
- Use the tree as a navigation map, not a script

### 4.4 Naming Convention

When referencing AQUASE trees in documents:
- Name by root: "the A tree" or by narrative name: "Value-First AQUASE"
- Reference nodes by full ID: "see Q1A2-S1E3 for the cost argument"
- Reference sections: "Section B covers the how"

### 4.5 Selecting and Ordering Questions

When building a tree from candidate arguments, evaluate each on two dimensions:

**Dimension 1: Impact** - How strongly does this move the listener toward action?

- **High**: Creates urgency, reveals unrecognized risk, or promises concrete measurable gain
- **Medium**: Builds credibility, provides proof, demonstrates capability
- **Low**: Descriptive, informational, scopes or defines without motivating

**Dimension 2: Why / How / What** (Sinek principle: start with Why)

- **Why**: Addresses motivation, pain, or purpose - always position first
- **How**: Mechanism, proof, capability - position second
- **What**: Scope, description, features - position last

**Ordering rule**: Highest-Impact + Why-type question goes first. A listener who understands WHY will tolerate HOW and WHAT. A listener who hears WHAT first may never reach WHY.

**Selection rules** (when candidates exceed 3 slots):

1. Score each candidate on Impact (1-3) and type (Why/How/What)
2. Keep the top 3 as questions. Others become drill-down material in Sections A/B/C
3. If two candidates compete for the same slot: the one addressing WHY wins
4. If one candidate is dramatically stronger than all others: promote it to the ONLY top-level question, demote the rest to answers beneath it

**The One-Argument Test**:

Before finalizing a multi-question tree, ask: "Can I collapse this into ONE question with three answers?" If yes, the tree is likely stronger with one powerful question and deeper evidence. Multiple top-level questions dilute each other when time is limited. One argument that lands beats three that compete for attention.

**The Magnet Rule**:

The root argument (A) must connect to at least one listener motivator - something the audience already wants or fears. Examples: gaining an advantage others lack, reducing a risk they currently carry, saving a resource they are wasting, or gaining access they cannot get elsewhere.

If A doesn't hit a magnet, the tree won't move the listener to action - regardless of how well-structured the evidence is.

## 5. Full Example

Source: Barbara Minto, "The Pyramid Principle" (adapted)

### Root Section

```
A: Pigs should be kept as pets.
├ Q1: "Why?"
│ ├ Q1A1: They are beautiful.
│ └ Q1A2: They are marvellously fat.
│
└ Q2: "How?"
  └ Q2A1: They could be bred to fascinating variations.
```

### Section A (Q1: "Why?")

```
A: Pigs should be kept as pets.
└ Q1: "Why?"
  ├ Q1A1: They are beautiful.
  │ └ Q1A1-S1: "In what way?"
  │   ├ Q1A1-S1E1: Presence proves lovely curves to the onlooker.
  │   └ Q1A1-S1E2: Greater modesty in the possessor.
  │
  └ Q1A2: They are marvellously fat.
    └ Q1A2-S1: "Why does that matter?"
      └ Q1A2-S1E1: Symbols linked to the land - so English they deserve the national symbol.
```

### Section B (Q2: "How?")

```
A: Pigs should be kept as pets.
└ Q2: "How?"
  └ Q2A1: They could be bred to fascinating variations.
    └ Q2A1-S1: "What variations?"
      ├ Q2A1-S1E1: In types.
      ├ Q2A1-S1E2: In size.
      ├ Q2A1-S1E3: In personalities.
      └ Q2A1-S1E4: In functions.
```

### Closing

```
Q1 "Why?": They are beautiful - in curves and modesty.
Q1 "Why?": They are fat - symbolically English.
Q2 "How?": They can be bred to fascinating variations in type, size, personality, and function.
└─> A: Pigs should be kept as pets.
```

## 6. Applied Examples

### 6.1 Sales Argument: Enterprise Software

```
A: Our system reduces your order errors by 40% - provably within 90 days.
├ Q1: "How does it work?"
│ ├ Q1A1: Automatic validation against your framework agreements.
│ ├ Q1A2: Pattern detection flags duplicates and unusual quantities.
│ └ Q1A3: Real-time sync with your ERP.
│
├ Q2: "Who else has done this?"
│ ├ Q2A1: Three comparable manufacturing clients achieved 35-48% error reduction.
│ └ Q2A2: Industry benchmark (Gartner 2024): error rates drop from 4.2% to 1.8%.
│
└ Q3: "What's the risk for us?"
  ├ Q3A1: 90-day pilot with clear before-and-after metrics.
  ├ Q3A2: You only pay if error rate drops below your agreed target.
  └ Q3A3: No lock-in - we integrate with your existing stack.


A: Our system reduces your order errors by 40% - provably within 90 days.
└ Q1: "How does it work?"
  ├ Q1A1: Automatic validation against your framework agreements.
  │ └ Q1A1-S1: "What exactly is validated?"
  │   ├ Q1A1-S1E1: Prices and volume discounts against the active framework agreement.
  │   ├ Q1A1-S1E2: Delivery terms and lead times vs. contractual commitments.
  │   └ Q1A1-S1E3: Supplier-specific constraints (MOQ, packaging units, order windows).
  │
  ├ Q1A2: Pattern detection flags duplicates and unusual quantities.
  │ └ Q1A2-S1: "What patterns?"
  │   ├ Q1A2-S1E1: Duplicate orders across departments (caught before submission).
  │   ├ Q1A2-S1E2: Quantities deviating >30% from 12-month rolling average.
  │   └ Q1A2-S1E3: Price spikes vs. commodity index for raw materials.
  │
  └ Q1A3: Real-time sync with your ERP.
    └ Q1A3-S1: "Which ERPs and how fast?"
      ├ Q1A3-S1E1: SAP S/4HANA, Oracle, Microsoft Dynamics - certified connectors.
      ├ Q1A3-S1E2: Bidirectional sync - changes in ERP reflect within 60 seconds.
      └ Q1A3-S1E3: Setup: API connector, 2-day integration sprint, no downtime.


A: Our system reduces your order errors by 40% - provably within 90 days.
└ Q2: "Who else has done this?"
  ├ Q2A1: Three comparable manufacturing clients achieved 35-48% error reduction.
  │ └ Q2A1-S1: "Which clients and what errors?"
  │   ├ Q2A1-S1E1: Automotive tier-1 supplier - wrong part numbers from manual entry dropped from 18% to 3%.
  │   ├ Q2A1-S1E2: Chemical distributor - outdated pricing errors eliminated entirely (were 15% of orders).
  │   └ Q2A1-S1E3: Packaging manufacturer - duplicate orders across 4 plants reduced by 91%.
  │
  └ Q2A2: Industry benchmark (Gartner 2024): error rates drop from 4.2% to 1.8%.
    └ Q2A2-S1: "What does Gartner measure?"
      ├ Q2A2-S1E1: Study covers 847 manufacturing firms using automated procurement validation.
      └ Q2A2-S1E2: Median time to ROI: 67 days (our 90-day guarantee is conservative).


A: Our system reduces your order errors by 40% - provably within 90 days.
└ Q3: "What's the risk for us?"
  ├ Q3A1: 90-day pilot with clear before-and-after metrics.
  │ └ Q3A1-S1: "What do you measure?"
  │   ├ Q3A1-S1E1: Error rate by type: wrong price, wrong quantity, wrong item, duplicate.
  │   ├ Q3A1-S1E2: Baseline from your last 6 months vs. pilot period - same categories.
  │   └ Q3A1-S1E3: Weekly dashboard - you see progress in real time, not just at the end.
  │
  ├ Q3A2: You only pay if error rate drops below your agreed target.
  │ └ Q3A2-S1: "What if it doesn't?"
  │   ├ Q3A2-S1E1: No fee. We absorb integration costs. You keep the data and dashboards.
  │   └ Q3A2-S1E2: Exit clause: 30-day written notice, no penalties, full data export.
  │
  └ Q3A3: No lock-in - we integrate with your existing stack.
    └ Q3A3-S1: "What happens after the pilot?"
      ├ Q3A3-S1E1: Annual subscription based on order volume - scales with you.
      ├ Q3A3-S1E2: All rules and configurations are yours - exportable in open format.
      └ Q3A3-S1E3: Switch to competitor anytime - we provide migration support.


Q1 "How does it work?": Validates prices, flags duplicates, syncs with your ERP in real time.
Q1 "How does it work?": Catches deviations from framework agreements before orders go out.
Q1 "How does it work?": No manual data entry - eliminates stale data as an error source.
Q2 "Who else has done this?": Three manufacturers achieved 35-48% reduction - documented.
Q2 "Who else has done this?": Gartner benchmark confirms: 4.2% to 1.8% industry-wide.
Q3 "What's the risk for us?": 90-day pilot, you define success, no fee if we miss the target.
Q3 "What's the risk for us?": No lock-in, you keep everything, exit anytime.
Q3 "What's the risk for us?": Your data, your rules, your choice.
└─> A: Our system reduces your order errors by 40% - provably within 90 days.
```

### 6.2 Investment Proposal: Renewable Energy Fund

```
A: The fund delivers 8-10% net IRR at lower volatility than listed infrastructure ETFs (GRESB benchmark: 6-7% with 2x drawdown).
├ Q1: "How do you get 8-10% net?"
│ ├ Q1A1: Long-term PPAs secure 70% of gross revenue.
│ ├ Q1A2: Operating costs fixed via full-service OEM contracts.
│ └ Q1A3: Conservative leverage (45% LTV) at fixed rates.
│
├ Q2: "What about technology risk?"
│ ├ Q2A1: Exclusively proven onshore wind and solar.
│ ├ Q2A2: Average asset age 4.2 years with 20+ years remaining life.
│ └ Q2A3: Technical availability 97.3% vs. 95% industry average.
│
└ Q3: "What about concentration risk?"
  ├ Q3A1: 14 sites across 4 countries.
  ├ Q3A2: No single site exceeds 12% of portfolio.
  └ Q3A3: 85% EUR-denominated; SEK naturally hedged.


A: The fund delivers 8-10% net IRR at lower volatility than listed infrastructure ETFs.
└ Q1: "How do you get 8-10% net?"
  ├ Q1A1: Long-term PPAs secure 70% of gross revenue for 15-20 years.
  │ └ Q1A1-S1: "Who are the offtakers?"
  │   ├ Q1A1-S1E1: Seven investment-grade corporates (A- or better) across utilities and industrials.
  │   ├ Q1A1-S1E2: Contracts are inflation-indexed - real returns remain stable regardless of CPI.
  │   └ Q1A1-S1E3: Average remaining PPA duration: 12.4 years - no cliff in revenue.
  │
  ├ Q1A2: Operating costs fixed via full-service OEM contracts.
  │ └ Q1A2-S1: "What's included?"
  │   ├ Q1A2-S1E1: Full turbine/panel maintenance, spare parts, and performance guarantee.
  │   ├ Q1A2-S1E2: Indexed at 1.5% p.a. - well below revenue escalation of 2.5%.
  │   └ Q1A2-S1E3: Penalty clause: OEM pays for availability below 96%.
  │
  └ Q1A3: Conservative leverage (45% LTV) at fixed rates.
    └ Q1A3-S1: "What's the debt structure?"
      ├ Q1A3-S1E1: 12-year amortizing project finance - fully matched to PPA tenor.
      ├ Q1A3-S1E2: Fixed rate locked at 3.8% (2024 closing) - no floating exposure.
      └ Q1A3-S1E3: DSCR covenant at 1.3x - current coverage: 1.7x (comfortable headroom).


A: The fund delivers 8-10% net IRR at lower volatility than listed infrastructure ETFs.
└ Q2: "What about technology risk?"
  ├ Q2A1: Exclusively proven onshore wind and solar - no prototypes.
  │ └ Q2A1-S1: "How proven?"
  │   ├ Q2A1-S1E1: Turbine models: Vestas V110, Siemens Gamesa SG 3.4 - 10,000+ units deployed globally.
  │   ├ Q2A1-S1E2: Solar: LONGi Hi-MO 5 modules - bankability confirmed by all major technical advisors.
  │   └ Q2A1-S1E3: No single-axis trackers, no bifacial in northern sites - conservative tech selection.
  │
  ├ Q2A2: Average asset age 4.2 years - past infant mortality.
  │ └ Q2A2-S1: "What's the maintenance outlook?"
  │   ├ Q2A2-S1E1: Major component exchange (gearbox, blades) not expected before year 12-15.
  │   └ Q2A2-S1E2: Reserve fund: EUR 2.1M earmarked for unplanned capex - covers 2 major events.
  │
  └ Q2A3: Technical availability 97.3% vs. 95% industry average.
    └ Q2A3-S1: "How is that measured?"
      ├ Q2A3-S1E1: Time-based availability (IEC 61400-26) - independently verified quarterly.
      └ Q2A3-S1E2: Three-year track record - no single quarter below 96.1%.


A: The fund delivers 8-10% net IRR at lower volatility than listed infrastructure ETFs.
└ Q3: "What about concentration risk?"
  ├ Q3A1: 14 sites across 4 countries.
  │ └ Q3A1-S1: "Which countries and why?"
  │   ├ Q3A1-S1E1: Germany (6 sites) - mature regulatory framework, priority dispatch.
  │   ├ Q3A1-S1E2: Spain (4) - high irradiation, competitive auction prices locked.
  │   └ Q3A1-S1E3: Sweden (2), Portugal (2) - different wind regimes, uncorrelated generation profiles.
  │
  ├ Q3A2: No single site exceeds 12%; no single offtaker exceeds 25%.
  │ └ Q3A2-S1: "What if an offtaker defaults?"
  │   ├ Q3A2-S1E1: PPA replacement clause: 6-month window to re-contract at market rates.
  │   └ Q3A2-S1E2: Merchant floor price modeled at EUR 45/MWh - fund remains cash-positive even without PPA.
  │
  └ Q3A3: 85% EUR-denominated; SEK hedged via operating costs.
    └ Q3A3-S1: "How does the natural hedge work?"
      ├ Q3A3-S1E1: Swedish sites generate revenue in SEK; Swedish OEM contracts and land lease paid in SEK.
      └ Q3A3-S1E2: Net SEK exposure after operating costs: <3% of fund NAV.


Q1 "How do you get 8-10% net?": Secured revenue (PPAs), locked costs (OEM), conservative leverage - the math is transparent.
Q1 "How do you get 8-10% net?": 72% EBITDA margin with 45% LTV delivers 5.5% cash yield + NAV growth.
Q1 "How do you get 8-10% net?": No revenue speculation - 70% contracted for 12+ years with investment-grade counterparties.
Q2 "What about technology risk?": Proven turbines and panels only - 10,000+ units deployed, independently verified availability.
Q2 "What about technology risk?": Past infant mortality, reserves funded, OEM warranty active for 10 years.
Q2 "What about technology risk?": 97.3% availability sustained over 3 years - no quarter below 96.1%.
Q3 "What about concentration risk?": 14 sites, 4 countries, uncorrelated wind/solar profiles.
Q3 "What about concentration risk?": No single point of failure - site, offtaker, or currency.
Q3 "What about concentration risk?": Natural hedge limits net FX exposure to <3% of NAV.
└─> A: The fund delivers 8-10% net IRR at lower volatility than listed infrastructure ETFs.
```

### 6.3 Journalistic Article: Investigative Reporting

```
A: The city paid 12 million euros for an IT system that never went live.
├ Q1: "How did the vendor get in?"
│ ├ Q1A1: Tender criteria copied from the winner's datasheet.
│ ├ Q1A2: Competitor complaints dismissed without investigation.
│ └ Q1A3: Pre-tender emails between city official and vendor CEO.
│
├ Q2: "How did it get so expensive?"
│ ├ Q2A1: Five contract amendments - EUR 3.2M grew to EUR 12.1M.
│ └ Q2A2: Three amendments structured just below council approval threshold.
│
└ Q3: "Why is it shut down?"
  ├ Q3A1: Internal assessment: "fundamental architectural deficiencies."
  ├ Q3A2: Three departments independently procured their own solutions.
  └ Q3A3: No recovery claim - contract contained no performance guarantee.


A: The city paid 12 million euros for an IT system that never went live.
└ Q1: "How did the vendor get in?"
  ├ Q1A1: Three of five mandatory criteria use verbatim phrasing from the winner's datasheet.
  │ └ Q1A1-S1: "How do you know it's verbatim?"
  │   ├ Q1A1-S1E1: Side-by-side comparison: criteria text matches product spec document (exhibit A in our archive).
  │   ├ Q1A1-S1E2: Technical terms used appear in no other vendor's documentation - unique to this product.
  │   └ Q1A1-S1E3: The criteria were added in the final revision, 8 days before publication - not in the first two drafts.
  │
  ├ Q1A2: Two losing bidders filed formal complaints - both dismissed.
  │ └ Q1A2-S1: "What happened to the complaints?"
  │   ├ Q1A2-S1E1: Review panel consisted of three city employees - no external member, no conflict-of-interest disclosure.
  │   └ Q1A2-S1E2: Decision rationale: 14 words total. "Criteria reflect operational requirements. Complaint rejected."
  │
  └ Q1A3: Emails between city official and vendor CEO three months before tender.
    └ Q1A3-S1: "What do the emails say?"
      ├ Q1A3-S1E1: City official requests "technical input for specification drafting" - sent to vendor only.
      ├ Q1A3-S1E2: Vendor responds with 6-page document - three sections match final tender criteria word-for-word.
      └ Q1A3-S1E3: Obtained via freedom-of-information request after initial denial (overturned on appeal).


A: The city paid 12 million euros for an IT system that never went live.
└ Q2: "How did it get so expensive?"
  ├ Q2A1: Five contract amendments - original EUR 3.2M grew to EUR 12.1M (+278%).
  │ └ Q2A1-S1: "What was added?"
  │   ├ Q2A1-S1E1: Amendment 1: "Extended scope" - EUR 1.4M for modules not in original RFP.
  │   ├ Q2A1-S1E2: Amendments 2-4: "Technical adjustments" - EUR 4.8M total, no competitive re-tender.
  │   └ Q2A1-S1E3: Amendment 5: "Project stabilization" - EUR 2.7M, approved 3 weeks before system was shelved.
  │
  └ Q2A2: Three amendments fell just below the threshold requiring council approval.
    └ Q2A2-S1: "What's the threshold?"
      ├ Q2A2-S1E1: Council approval required for amendments exceeding EUR 2.0M individually.
      ├ Q2A2-S1E2: Amendments 2, 3, 4 valued at EUR 1.92M, EUR 1.87M, EUR 1.95M respectively.
      └ Q2A2-S1E3: Statistical probability of three consecutive amendments landing within 5% below threshold: <0.3%.


A: The city paid 12 million euros for an IT system that never went live.
└ Q3: "Why is it shut down?"
  ├ Q3A1: Internal assessment: "fundamental architectural deficiencies."
  │ └ Q3A1-S1: "What deficiencies?"
  │   ├ Q3A1-S1E1: System could not handle concurrent users above 200 - city has 4,600 employees.
  │   ├ Q3A1-S1E2: Data migration from legacy systems failed on 3 of 7 datasets - no recovery path documented.
  │   └ Q3A1-S1E3: Assessment author: external auditor (commissioned after newspaper inquiry - not proactively initiated).
  │
  ├ Q3A2: Three departments independently procured their own solutions.
  │ └ Q3A2-S1: "When and why?"
  │   ├ Q3A2-S1E1: Finance department switched to alternative 14 months into the project - cited "unacceptable delays."
  │   ├ Q3A2-S1E2: HR and Building Services followed within 4 months - both cited same vendor's "lack of responsiveness."
  │   └ Q3A2-S1E3: Combined cost of three departmental solutions: EUR 890K - functional and live within 6 months.
  │
  └ Q3A3: No recovery claim filed - contract contained no performance guarantee.
    └ Q3A3-S1: "Why no guarantee?"
      ├ Q3A3-S1E1: Original contract template (city standard) includes performance clause - it was removed in final negotiation.
      ├ Q3A3-S1E2: Negotiation protocol shows removal requested by vendor, approved by same city official from Q1A3.
      └ Q3A3-S1E3: Legal department was not consulted on the removal - confirmed via internal memo.


Q1 "How did the vendor get in?": Tailored criteria, suppressed complaints, pre-tender coordination.
Q1 "How did the vendor get in?": Verbatim spec language, 14-word rejection, emails obtained via FOI.
Q1 "How did the vendor get in?": The vendor wrote the requirements it was then selected against.
Q2 "How did it get so expensive?": Five amendments, +278%, each conveniently below council threshold.
Q2 "How did it get so expensive?": Statistical near-impossibility of three consecutive sub-threshold amendments.
Q3 "Why is it shut down?": System couldn't handle 200 users (city has 4,600), three departments gave up and built their own.
Q3 "Why is it shut down?": No recovery possible - performance guarantee deliberately removed from contract.
Q3 "Why is it shut down?": EUR 12M spent, EUR 890K solved the problem three times over.
└─> A: The city paid 12 million euros for an IT system that never went live.
```

## 7. Sources

- `AQUASE-IN01-SC-MINTO-PYR`: Barbara Minto, "The Pyramid Principle" (3rd ed., 2009) - Ch. 6 "How to Highlight the Structure", decimal numbering (p. 81); Ch. 2 vertical Q&A dialogue [VERIFIED]

## 8. Document History

**[2026-07-01 16:38]**
- Changed: Complete restructure to section-based notation (Root + A/B/C + Closing)
- Renamed: AQUAT → AQUASE (Argument-Question-Answer-Subquestion-Evidence)
- Changed: ID system from path-hyphenated (A1-Q1-A2-Q1-A3) to concatenated (Q1A2-S1E3)
- Changed: Root marker from numbered A1 to singular A
- Added: Pigs example (Minto) as full worked example with all sections
- Changed: Applied examples show Root Section only (compact format)

**[2026-07-01 15:56]**
- Created public version from internal concept document
- Removed session-specific references and non-public sources
- Added 3 applied examples: Sales Argument (Enterprise Software), Investment Proposal (Renewable Energy Fund), Journalistic Article (Investigative Reporting)
- Translated all content to English
