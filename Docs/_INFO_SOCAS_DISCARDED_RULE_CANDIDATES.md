# INFO: SOCAS Discarded Rule Candidates

**Doc ID**: SOCAS-IN02
**Goal**: Record every SOCAS rule candidate that was not selected for the 4 SOCAS rule files, with status and reasoning, so each one can be confirmed, reversed or re-entered later
**Timeline**: Created 2026-11-10, Updated 3 times (2026-11-10 - 2026-11-10)

**Depends on:**
- `_INFO_SOCAS_SIGNS_OF_CONFUSION_AND_SLOPPINESS.md [SOCAS-IN01]` for the selected rules, priority model (section 2.1), ranking (section 2.3) and selection criteria (section 2.4)

## Summary

- 36 candidates are not selected: 10 drafted SOCAS rules, 18 research candidates and 8 forms of old SOCAS criteria [VERIFIED: counted in sections 2-3]
- Status per candidate:
  - `[DISCARDED]` 21: the sign leaves SOCAS
  - `[MERGED]` 9: the sign survives inside a selected rule (target ID given)
  - `[DEFERRED]` 6: the sign belongs to a production rule (APAPALAN: As Precise As Possible, As Little As Necessary; MECT: Minimal Explicit Consistent Terminology), another command (`/fact-check`) or an open user decision
- All statuses are proposals. The user confirms or reverses each one; a reversed candidate returns to SOCAS-IN01 under its original ID [ASSUMED: workflow proposal]
- 3 old SOCAS rules lose their own rule: SOCAS-CR-14 arbitrary sequencing, CR-15 net-negative adoption, AP-04 user interface checks. CR-14 stays checkable through APAPALAN and MECT production rules and, for steps that cannot run in order, SOCAS-WR-12. CR-03 returned as SOCAS-GN-17 after a sign-level check against the old `SOCAS_RULES.md` [VERIFIED: SOCAS-IN01 section 8]
- All 4 drafts with priority P3 are discarded: a quick screen has no room for high-cost or low-value checks [VERIFIED: SOCAS-IN01 section 2.4]

## Table of Contents

1. [Discard Criteria and Status Words](#1-discard-criteria-and-status-words)
2. [Drafted SOCAS Rules Not Selected](#2-drafted-socas-rules-not-selected)
3. [Research Candidates Not Selected](#3-research-candidates-not-selected)
4. [Re-Entry Conditions](#4-re-entry-conditions)
5. [Next Steps](#5-next-steps)
6. [Sources](#6-sources)
7. [Document History](#7-document-history)

## 1. Discard Criteria and Status Words

Status words:
- **`[DISCARDED]`**: the candidate leaves SOCAS; no selected rule tests its sign
- **`[MERGED]`**: the sign moves into a selected SOCAS rule; the candidate has no own ID
- **`[DEFERRED]`**: the sign is handled outside SOCAS: by an APAPALAN or MECT production rule (SOCAS-IN01 section 3.3), by another command, or after an open user decision

Reason codes (one or more per candidate):
- **WEAK-P3**: priority P3 (high cost with medium or low value, or medium cost with low value); contradicts the quick-screen purpose
- **WEAK-UNSOURCED**: low value, no evidence found, research advises to leave it out until sourced
- **MERGED**: another selected SOCAS rule tests the same passage; two rules would double-count (SOCAS-AP-06)
- **DEFER-PRODUCTION**: an APAPALAN or MECT rule covers the sign completely and the SOCAS draft has low value (zero-overlap decision SOCASCONTEXT-DD-01)
- **DEFER-COMMAND**: the check needs deep work that belongs to `/fact-check`, `/critique` or `/research`
- **NOT-A-SIGN**: production rule (how to write) or method that assesses people, not content
- **CONTRADICTED**: evidence speaks against the rule
- **OPEN-DECISION**: design alternative kept for a pending user decision

Entry format: status and reason codes | priority it had (or would have) with cost and value | reasoning | origin | target (merged or deferred only).

## 2. Drafted SOCAS Rules Not Selected

Drafts from SOCAS-IN01 version 2026-11-10 14:30. Their IDs are retired and not reused. Exception: SOCAS-GN-17 (overlapping concerns) re-entered SOCAS-IN01 on 2026-11-10 under its original ID (section 4): the sign-level check against the old `SOCAS_RULES.md` showed that APAPL-BR-03 and MECT-LT-02 cover repeated text and list grouping, not duplicate mechanisms in a design. Its text part stays deferred (SOCAS-IN01 section 3.3).

### 2.1 General Drafts

#### SOCAS-GN-05: Unqualified Strong Claim

- **Status**: `[MERGED]` | MERGED
- **Had**: P2 | Cost: low | Value: low, evidence C-D
- **Reasoning**: The research rates this a cheap but weak presence test that does not stand alone (research IN05, cost and value ranking). A universal claim without limits is an assumption stated as fact; the test of SOCAS-GN-06 hits the same passage, so two rules would double-count
- **Origin**: RC-N07, RC-G02
- **Target**: SOCAS-GN-06 (sign "universal or causal claim without stated limits")

#### SOCAS-GN-14: Spurious Precision

- **Status**: `[DISCARDED]` | WEAK-P3
- **Had**: P3 | Cost: medium, needs domain knowledge to judge possible precision | Value: low, evidence D
- **Reasoning**: Only [secondary summaries of Huff (1954)](https://thinkr.org/newsletter/how-to-lie-with-statistics) support it; the book was not accessed. Judging how precise a number can be needs domain knowledge the agent may lack. The "forecast stated as fact" part is caught by SOCAS-GN-06 (assumption as fact)
- **Origin**: RC-N09, SM-05

#### SOCAS-GN-18: Arbitrary Sequencing

- **Status**: `[DEFERRED]` | DEFER-PRODUCTION, WEAK-UNSOURCED
- **Had**: P2 | Cost: low | Value: low, `[ASSUMED]`
- **Reasoning**: No direct study; the only indirect support is "main message first" ([US Centers for Disease Control and Prevention (CDC) Clear Communication Index](https://www.cdc.gov/ccindex/tool/description-examples-parta.html)), which SOCAS-WR-10 and APAPL-ST-01 already cover. Ordering is prescribed by APAPL-ST-05 (general to specific) and MECT-LT-02. Steps that cannot run in the stated order (a step needs the result of a later step) are a requirement defect, not presentation order; they stay a sign of SOCAS-WR-12
- **Origin**: SOCAS-CR-14
- **Target**: APAPL-ST-05, MECT-LT-02 (presentation order); SOCAS-WR-12 (step order in procedures)

#### SOCAS-GN-20: Confusing Elements

- **Status**: `[MERGED]` | MERGED, DEFER-PRODUCTION
- **Had**: P2 | Cost: low | Value: low, `[ASSUMED]`
- **Reasoning**: Metaphors and idioms are covered by MECT-WC-10 (explicit over figurative). MECT-WC-10 does not cover jokes, so humor that carries no information moves to SOCAS-GN-15 (can the passage be deleted without losing information?). A creative name or hidden reference the reader must decode fails the test of SOCAS-GN-03 (would the reader understand every key term?). Seductive-detail evidence is real but inconsistent ([15 of 39 studies without effect](https://pmc.ncbi.nlm.nih.gov/articles/PMC8442593/)) and already used by SOCAS-GN-16
- **Origin**: SOCAS-CR-07 (humor and metaphor part)
- **Target**: SOCAS-GN-03 (creative names, hidden references); SOCAS-GN-15 (humor without information); MECT-WC-10 (metaphors, idioms)

### 2.2 Writing Drafts

#### SOCAS-WR-03: Unverifiable Reference List

- **Status**: `[MERGED]` | MERGED
- **Had**: P2 | Cost: low | Value: low, presence test only
- **Reasoning**: A complete-looking reference proves nothing: [64% of fabricated references with a digital object identifier (DOI)](https://pmc.ncbi.nlm.nih.gov/articles/PMC12658395/) had a valid DOI pointing to an unrelated article. Only opening the source decides; SOCAS-WR-01 does that and searches incomplete references by title. Presence tests alone are weak signals (research rule R2, SOCAS-AP-13)
- **Origin**: RC-N10
- **Target**: SOCAS-WR-01

### 2.3 Communication Drafts

#### SOCAS-CM-05: Self-Contradicting Message

- **Status**: `[MERGED]` | MERGED
- **Had**: P1 | Cost: low | Value: medium, evidence C
- **Reasoning**: The research places contradiction in the general file and gives message forms only as examples (research IN08, RC-M10: "lives in general file, field example only"). A separate rule would count the same passage twice
- **Origin**: RC-M10
- **Target**: SOCAS-GN-01 (sign "two deadlines, two owners or two scopes in one message")

#### SOCAS-CM-09: Inappropriate Tone

- **Status**: `[DISCARDED]` | WEAK-P3
- **Had**: P3 | Cost: medium, needs knowledge of the relationship | Value: low, `[ASSUMED]`
- **Reasoning**: No study defines appropriate tone for business messages (research IN08 Q7). The judgment depends on relationship, history and culture the agent does not see, so findings would be low-confidence guesses. The measurable parts of the focus question "is the tone appropriate" stay covered: SOCAS-CM-06 (tone depends on unstated intent) and SOCAS-CM-07 (rude or hostile language); trace of all 10 focus questions in SOCAS-IN01 section 6
- **Origin**: research focus question Q7

#### SOCAS-CM-11: Inverted Priorities

- **Status**: `[MERGED]` | MERGED
- **Had**: P1 | Cost: low | Value: medium, evidence B-C
- **Reasoning**: Both parts test priority inversion in the same passage as SOCAS-CM-08. "Deadline emphasized above the larger consequence" rests on the same mere-urgency evidence. "Main ask not in the first lines" has medium value, so DEFER-PRODUCTION (low value only) does not apply; SOCAS-CM-08 keeps it as REF to APAPL-ST-01 (goal first), as SOCAS-WR-10 does for documents. The focus question "does it invert priorities" is answered by SOCAS-CM-08
- **Origin**: RC-M08, RC-M09
- **Target**: SOCAS-CM-08 (both parts; ask-first fix by APAPL-ST-01)

### 2.4 Coding Drafts

#### SOCAS-CD-07: Net-Negative Adoption

- **Status**: `[DISCARDED]` | WEAK-P3, DEFER-COMMAND
- **Had**: P3 | Cost: high, several lookups in issue trackers and community forums | Value: low, `[ASSUMED]`
- **Reasoning**: The research found only tool documentation ([Open Source Security Foundation (OpenSSF) Scorecard](https://github.com/ossf/scorecard/blob/main/README.md)), no evidence that workaround counts or migration discussions predict adoption failure (research IN01 limitations). Weighing a tool's problems against its value is a full assessment for `/research` or `/critique`. The cheap health signs (archived, unmaintained, known vulnerabilities) stay in SOCAS-CD-06
- **Origin**: SOCAS-CR-15

#### SOCAS-CD-11: User Interface Review Signs

- **Status**: `[DISCARDED]` | WEAK-P3
- **Had**: P3 | Cost: high, needs the running interface or screenshots | Value: low, `[ASSUMED]`: not researched
- **Reasoning**: User interface criteria were not researched in either round (research IN09 D8). A text-only run cannot test tab order, dialogs or visual hierarchy. The command-name sign duplicates APAPL-NM-05 (standard terms). Kept here as re-entry material: established pattern broken without gain; related elements far apart; no tab order or keyboard support; no copy function for relevant text; unclear visual hierarchy; non-standard command names; data deleted or lost without confirmation; dialog with entered data closes on outside click
- **Origin**: SOCAS-AP-04

### 2.5 Old Criterion Forms Replaced

#### SOCAS-CR-04 Original Test: Named Contact Person

- **Status**: `[DISCARDED]` | WEAK-UNSOURCED
- **Had**: test "Can the reader find a named person to contact for this topic?"
- **Reasoning**: No study shows that generic contact addresses predict sloppy content (research IN07). Readers mention who is behind a site and why it exists ([sponsor identity 8.8%, company motive 15.5% of credibility comments](https://credibility.stanford.edu/pdf/How_Do_People_Evaluate_a_Web_Site%27s_Credibility_v37.pdf)), not contact addresses; mention counts show what readers look at, not which signs are valid. The concept survives reworded in SOCAS-WR-05 (responsible party and interest), supported by lateral reading evidence. The sign "no escalation path documented" moved to SOCAS-WR-12 (process descriptions)
- **Origin**: SOCAS-CR-04, standalone prompt v6.2

#### SOCAS-CR-06 Scope: Requirement Tests on All Content Types

- **Status**: `[DISCARDED]` | CONTRADICTED
- **Had**: one criterion "Incomplete specification" applied to articles, reports and emails as well as specifications
- **Reasoning**: The session problem itself: requirement tests (must vs may, edge cases) fit specifications only (research IN07 Field 1 and 2); "conclusions without evidence" duplicated Gaps in reasoning (SOCAS-CR-10). The parts live on in SOCAS-CD-09, SOCAS-CD-10, SOCAS-WR-12 (scoped) and SOCAS-GN-04
- **Origin**: SOCAS-CR-06

#### Dimension Weights 40/30/20/10

- **Status**: `[DEFERRED]` | OPEN-DECISION
- **Had**: Soundness 40, Usefulness 30, Clarity 20, Integrity 10 (standalone prompt v6.2)
- **Reasoning**: No source was found for these weights; equal-weight models predict as well as fitted weights ([Dawes 1979](https://doi.org/10.1037/0003-066x.34.7.571)). The selected rules carry no dimension, so the weights first need a dimension per rule. SOCAS-AP-02 proposes the verdict from the violated count and an informational equal-weight mean; the user decides (SOCAS-IN01 Next Steps 1)
- **Origin**: standalone prompt v6.2 Scoring Rules

#### Exact-Count Thresholds

- **Status**: `[DISCARDED]` | CONTRADICTED
- **Had**: standalone prompt v6.2 Consistency Rule 7 ("3+ per 1,000 words: count, do not estimate")
- **Reasoning**: [Large language models (LLMs) fail at counting repeated tokens](https://dl.acm.org/doi/10.1145/3818606); error grows with the count. SOCAS-AP-08 replaces exact counts by tolerant thresholds or a counting tool
- **Origin**: standalone prompt v6.2 Consistency Rule 7

#### SOCAS-CR-02 Sign: Missing Glossary

- **Status**: `[MERGED]` | MERGED
- **Had**: sign "Missing glossary for domain terms" (old `SOCAS_RULES.md`)
- **Reasoning**: A glossary is one fix among several (definition at first use, link, plain word). SOCAS-GN-03 tests the outcome directly: would the intended reader understand every key term the first time it appears? Requiring a glossary would be a presence test (SOCAS-AP-13) and would flag short documents that define terms inline
- **Origin**: SOCAS-CR-02
- **Target**: SOCAS-GN-03

#### SOCAS-CR-05 Sign: Information Scattered Across Documents

- **Status**: `[MERGED]` | MERGED, NOT-A-SIGN
- **Had**: sign "Information scattered across multiple documents" for all content types (old `SOCAS_RULES.md`)
- **Reasoning**: In messages and orders the sign survives in SOCAS-CM-02 (lookups needed to act): the reader must act without seeking more sources (APAPL-ST-04). In documents, a reference to another document is the prescribed fix against repetition (APAPL-BR-03, APAPL-PR-04), so a reference alone is not a sign; an undefined term or a broken reference is tested by SOCAS-GN-03 and SOCAS-GN-22
- **Origin**: SOCAS-CR-05
- **Target**: SOCAS-CM-02 (messages and orders)

#### SOCAS-CR-07 Sign: Excessive Metaphors or Analogies

- **Status**: `[DISCARDED]` | WEAK-UNSOURCED
- **Had**: sign "Excessive metaphors or analogies" (old `SOCAS_RULES.md`)
- **Reasoning**: Metaphors are deferred to MECT-WC-10 (explicit over figurative, draft SOCAS-GN-20). An analogy used as proof is the fallacy "false analogy", which is not among the 7 fallacy families the research selected for SOCAS-GN-07 (research IN10); no evidence was found that analogies used as explanation signal confusion. Re-entry condition in section 4
- **Origin**: SOCAS-CR-07

#### Source Evaluation Subset: Rank Sources by SOCAS Count

- **Status**: `[DISCARDED]` | CONTRADICTED
- **Had**: old `SOCAS_RULES.md` subset "Source Evaluation (`/research`)": "High SOCAS count = unreliable source. Prefer sources with low SOCAS indicators"
- **Reasoning**: Identical reruns flip [13.6% of pairwise verdicts](https://arxiv.org/html/2606.13685) (preprint), so a ranking by count alone is noise between close sources; SOCAS-AP-11 forbids ranking by score alone. Signs still flag a source; the ranking basis for `/research` and `/improve` is open (SOCAS-IN01 Next Steps 2). The repository health signals of the subset moved to SOCAS-CD-06
- **Origin**: old `SOCAS_RULES.md` Source Evaluation subset; `/research`, `/improve` Phase 1

## 3. Research Candidates Not Selected

Candidates from the session research SOCASCONTEXT-SOCASRSRCH (IN03 to IN10) that never became an own drafted rule. Numbered candidates not listed here are selected or merged in SOCAS-IN01 (see the **Replaces** line of each rule). Keys `RX-NN` are local to this document.

### 3.1 Writing and Publications

#### RX-01: Original Source Behind a Secondary One (RC-W05)

- **Status**: `[DEFERRED]` | DEFER-COMMAND
- **Would be**: P3 | Cost: high, search for the first version of a figure or quote | Value: medium, evidence B
- **Reasoning**: The research itself assigns it to `/fact-check` (research IN01 index, IN05). Multi-source search is where agents degrade: [fact-check accuracy fell about 42% as tool calls grew from 2 to 150](https://arxiv.org/html/2605.06635v1) (preprint)
- **Target**: `/fact-check`

#### RX-02: Other Coverage of a Claim (RC-W06)

- **Status**: `[DEFERRED]` | DEFER-COMMAND
- **Would be**: P3 | Cost: high, several searches plus an independence judgment | Value: low to medium, evidence B-D
- **Reasoning**: Sources that all read the same original add no evidence, so counting coverage needs synthesis, not a quick lookup. Includes the [First Draft](https://firstdraftnews.org/articles/verifying-online-information-the-absolute-essentials/) check "did the event happen at all", which is a truth verdict
- **Target**: `/fact-check`

#### RX-03: Readability Formulas as Quality Score (research IN07 Field 2)

- **Status**: `[DISCARDED]` | CONTRADICTED
- **Would be**: P2 | Cost: low with a tool | Value: low
- **Reasoning**: [Critics](https://doi.org/10.1109/tpc.1981.6447826) show the formulas ignore reader skill, subject knowledge, motivation, genre and context (excerpt-level evidence). Plain-language benefits are captured by SOCAS-GN-19 without a formula

#### RX-04: Proposal Warning Signs (research IN07 Field 3)

- **Status**: `[DISCARDED]` | WEAK-UNSOURCED, MERGED
- **Would be**: P2 | Cost: low, except price comparison (market data) | Value: low, [practitioner guidance](https://nmsconsulting.com/consulting-rfp-scorecard/) only, no study
- **Reasoning**: Most signs are already tested: scope with "etc." and no exclusions (SOCAS-WR-12 escape clauses), value claims without baseline (SOCAS-GN-09), no acceptance terms (SOCAS-WR-12), vague staffing and timelines that depend on unowned client inputs (SOCAS-CM-01, SOCAS-WR-11), generic case studies without measurable outcomes (SOCAS-GN-16). "Price far below peers" needs market data and belongs to `/research`

#### RX-05: Bid Cites Projects the Vendor Did Not Build (research IN07 Field 3)

- **Status**: `[DEFERRED]` | DEFER-COMMAND
- **Would be**: P3 | Cost: high, ownership research per cited project | Value: medium, evidence C ([US government 18F bid guide](https://guides.18f.gov/derisking-government-tech/resources/evaluate-bids/))
- **Reasoning**: A cited project that does not say what the bid claims is caught by SOCAS-WR-01; proving who built a project needs repository and contract research
- **Target**: `/fact-check`

#### RX-06: Documentation Types and Freshness (research IN07 Field 4)

- **Status**: `[DISCARDED]` | NOT-A-SIGN, MERGED
- **Would be**: P3 | Cost: medium | Value: low, evidence C ([Google documentation guide](https://google.github.io/styleguide/docguide/best_practices.html))
- **Reasoning**: Separating tutorial, how-to, reference and concept is a writing technique (DIATAXIS in `@skills:write-documents`), not a detection sign. The detectable parts are tested: outdated documentation (SOCAS-WR-09), boilerplate README without setup (SOCAS-CD-08)

#### RX-07: Easy Approach to Requirements Syntax (EARS) Templates (research IN07 Field 1)

- **Status**: `[DISCARDED]` | NOT-A-SIGN
- **Would be**: P2 | Cost: medium | Value: medium, evidence B ([aero-engine case study](https://doi.org/10.1109/re.2009.9))
- **Reasoning**: EARS prescribes how to write requirements (5 sentence templates). Requiring the templates would fail correct requirements written in plain form. The problems EARS addresses (ambiguity, vagueness, complexity) are detected by SOCAS-CD-10 and SOCAS-WR-12. Candidate for the SPEC writing rules instead

#### RX-08: Three-Question Requirement Review (research IN07 Field 1)

- **Status**: `[MERGED]` | MERGED
- **Would be**: P1 | Cost: low | Value: medium, evidence C ([practitioner synthesis of ISO 29148](https://claimdig.com/guides/good-requirements/))
- **Reasoning**: The three questions are already tests of selected rules: "could two readers interpret this differently?" (SOCAS-GN-03), "how would it be verified?" (SOCAS-CD-10, SOCAS-WR-12), "why is it here?" (SOCAS-CD-10 sign "requirement without rationale or parent")
- **Target**: SOCAS-GN-03, SOCAS-CD-10, SOCAS-WR-12

#### RX-09: String-Feature Classifier for Fabricated References (research IN05 RC-N10)

- **Status**: `[DISCARDED]` | WEAK-P3
- **Would be**: P3 | Cost: high, needs a trained model | Value: medium, evidence C ([area under the curve (AUC) 0.876](https://arxiv.org/pdf/2603.03299), preprint)
- **Reasoning**: Not a rule an agent applies by reading; it needs code and training data. SOCAS-WR-01 opens the source instead, which decides directly

### 3.2 Communication

#### RX-10: Read-Back or Receiver Summary Missing (research IN08)

- **Status**: `[DISCARDED]` | WEAK-UNSOURCED, NOT-A-SIGN
- **Would be**: P2 | Cost: low | Value: low, evidence very low certainty
- **Reasoning**: [Read-back of medication orders](https://pmc.ncbi.nlm.nih.gov/articles/PMC5659252/): rounds with an error 21% vs 76%, but single site and not randomized; a [review of closed-loop training](https://hdl.handle.net/10037/33922) found 4 randomized trials with very low certainty. Read-back is a practice for spoken orders; a written message rarely shows whether it happened. Missing information for the receiver is tested by SOCAS-CM-10

#### RX-11: Handoff Format Required (SBAR: Situation, Background, Assessment, Recommendation; I-PASS; research IN08)

- **Status**: `[DISCARDED]` | NOT-A-SIGN
- **Would be**: P1 | Cost: low | Value: medium, evidence B
- **Reasoning**: [I-PASS](https://www.nejm.org/doi/full/10.1056/NEJMsa1405556) (Illness severity, Patient summary, Action list, Situation awareness, Synthesis by receiver) cut preventable adverse events 30%, but only as a bundle with training, observation and a culture campaign; the format alone is not shown to work. [SBAR improved patient outcomes only within multifaceted interventions](https://bmjopen.bmj.com/content/11/12/e055247). Prescribing a format is a production rule. The I-PASS element list (what, who, by when, risks, what is unknown) feeds the test of SOCAS-CM-10

### 3.3 Coding

#### RX-12: Function Length Limits and Comment Ratios (research IN09 D8)

- **Status**: `[DISCARDED]` | WEAK-UNSOURCED
- **Would be**: P2 | Cost: low with a tool | Value: low, no evidence gathered
- **Reasoning**: The research advises to leave them out until sourced. Complexity that hurts comprehension is tested by SOCAS-CD-05 with a validated metric (Cognitive Complexity)

#### RX-13: "Defects Cost 100 Times More Later" as Rule Justification (research IN09 D8)

- **Status**: `[DISCARDED]` | CONTRADICTED
- **Would be**: not a rule; a justification some rule files use
- **Reasoning**: [No delayed-issue effect in 171 projects](https://doi.org/10.1007/s10664-016-9469-x) (2006-2014); the authors call it possibly a historical relic. No SOCAS rule may use it as justification

### 3.4 General and Method

#### RX-14: AI-Authorship Signals (research IN04 F6)

- **Status**: `[DISCARDED]` | CONTRADICTED
- **Would be**: P2 | Cost: low | Value: none
- **Reasoning**: [OpenAI's classifier](https://openai.com/index/new-ai-classifier-for-indicating-ai-written-text/) found 26% of AI text, mislabeled 9% of human text and was withdrawn on 2023-07-20; [7 detectors misclassified 61.3% of non-native essays](https://pmc.ncbi.nlm.nih.gov/articles/PMC10382961/). SOCAS-AP-07 forbids any authorship judgment

#### RX-15: Tests That Assess People (Watson-Glaser, Cognitive Reflection Test, Argument Mapping; research IN10 part A)

- **Status**: `[DISCARDED]` | NOT-A-SIGN
- **Would be**: not applicable to content
- **Reasoning**: These instruments measure a person's critical thinking ([instruction effect g = 0.30 over 341 effects](https://journals.sagepub.com/doi/10.3102/0034654314551063)), not the quality of a text; [Cognitive Reflection Test scores are inflated by prior exposure](https://pmc.ncbi.nlm.nih.gov/articles/PMC5225989/). They justify the method (ask a test question, check by calculation) but give no document rule. Toulmin parts and expert-appeal questions, which do apply to text, are selected in SOCAS-GN-04 and SOCAS-GN-06

#### RX-16: Natural Frequencies and Absolute Risks as Required Presentation (research IN06 part A)

- **Status**: `[MERGED]` | MERGED, NOT-A-SIGN
- **Would be**: P1 | Cost: low | Value: high, evidence B ([48 doctors](https://pmc.ncbi.nlm.nih.gov/articles/PMC200816/))
- **Reasoning**: Requiring a presentation form is a writing fix. The detection part, a relative risk or conditional probability without base or absolute risk, is a sign of SOCAS-GN-09
- **Target**: SOCAS-GN-09

#### RX-17: Worst-Domain Aggregation (Cochrane Risk of Bias 2 (RoB 2); research IN03 F5)

- **Status**: `[DEFERRED]` | OPEN-DECISION
- **Would be**: P1 | Cost: low | Value: medium, evidence C
- **Reasoning**: Alternative to the verdict by violated count: the worst rule decides the verdict, as in [RoB 2](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-08). With 19-30 rules per run and noisy single runs ([13.6% verdict flips on identical reruns](https://arxiv.org/html/2606.13685), preprint), one false finding would decide the verdict. SOCAS-AP-02 (3+ violated rules = rework) and SOCAS-RP-01 (worst findings first) already expose the worst rule. Kept as option for the scoring decision
- **Target**: user decision on SOCAS-AP-02 scoring

#### RX-18: Balanced Permutations of Criteria Order (research IN04 F3)

- **Status**: `[DISCARDED]` | WEAK-P3
- **Would be**: P3 | Cost: high, several runs per content | Value: medium, evidence C ([rubric order flipped the top candidate on 16% to 39% of prompts](https://arxiv.org/html/2602.02219v2), preprint)
- **Reasoning**: The bias hurts most when several documents are ranked; SOCAS-AP-11 forbids ranking by score and reruns only for decisions. SOCAS-AP-12 fixes the order so that runs stay comparable

## 4. Re-Entry Conditions

A candidate returns to SOCAS-IN01 under its original ID when its condition is met:
- **SOCAS-CD-11** user interface signs: a research round on interface review heuristics with outcome evidence, and a run that can see the interface. First re-entry candidate: "data deleted or lost without confirmation" (high impact, cheap to see in a screenshot) [ASSUMED]
- **SOCAS-CD-07** net-negative adoption: evidence that workarounds, unresolved defects or migration discussions predict adoption failure
- **SOCAS-CM-09** inappropriate tone: a validated rubric or study for tone appropriateness in written business messages
- **SOCAS-GN-14** spurious precision: a study that shows spurious precision misleads readers measurably
- **SOCAS-GN-18** arbitrary sequencing: evidence that presentation order reduces comprehension beyond what APAPL-ST-05 and MECT-LT-02 already catch
- **SOCAS-CR-07 analogies**: research showing false analogy among the frequent fallacies in business or technical content
- **RX-04** proposal warning signs: a study that links the signs to proposal outcomes
- **RX-10** read-back: a controlled study of confirmation requests in written channels
- **RX-12** function length and comment ratios: evidence that they predict defects or comprehension
- **RX-17** worst-domain aggregation and the dimension weights 40/30/20/10: user decision on SOCAS-AP-02

## 5. Next Steps

1. User reviews every status in sections 2-3; reply format per candidate: `GN-18 confirm`, `CD-11 reverse`
2. Move reversed candidates back into SOCAS-IN01 with their original ID; recount the ranking (SOCAS-IN01 section 2.3) and the overlap count (section 3.4)
3. Plan the re-entry research of section 4 as a separate research round

## 6. Sources

Claims were checked against search-result excerpts (abstract or page text) on 2026-11-10, not full texts. `[COMMUNITY]` = preprint or secondary summary.

**Drafted rules (section 2):**
- `SOCAS-IN02-SC-THINKR-HUFF`: https://thinkr.org/newsletter/how-to-lie-with-statistics - Huff summary, spurious precision (GN-14) [COMMUNITY]
- `SOCAS-IN02-SC-CDC-CCI`: https://www.cdc.gov/ccindex/tool/description-examples-parta.html - Main message first (GN-18) [VERIFIED]
- `SOCAS-IN02-SC-PMC-SEDUCDET`: https://pmc.ncbi.nlm.nih.gov/articles/PMC8442593/ - Seductive details: 15 of 39 studies without effect (GN-20) [VERIFIED]
- `SOCAS-IN02-SC-PMC-MHCITE`: https://pmc.ncbi.nlm.nih.gov/articles/PMC12658395/ - 64% of fabricated citations with DOI pointed to unrelated articles (WR-03) [VERIFIED]
- `SOCAS-IN02-SC-OSSF-SCORECARD`: https://github.com/ossf/scorecard/blob/main/README.md - Repository health checks, only tool documentation for CD-07 [VERIFIED]
- `SOCAS-IN02-SC-STNFD-FOGGCRED`: https://credibility.stanford.edu/pdf/How_Do_People_Evaluate_a_Web_Site%27s_Credibility_v37.pdf - Sponsor identity 8.8%, company motive 15.5% of credibility comments (CR-04 test) [VERIFIED]
- `SOCAS-IN02-SC-APA-DAWES`: https://doi.org/10.1037/0003-066x.34.7.571 - Equal weights robust (dimension weights) [VERIFIED]
- `SOCAS-IN02-SC-ACM-LTRCOUNT`: https://dl.acm.org/doi/10.1145/3818606 - LLMs fail to count repeated tokens (exact-count thresholds) [VERIFIED]

**Research candidates (section 3):**
- `SOCAS-IN02-SC-ARXIV-CITEDNV`: https://arxiv.org/html/2605.06635v1 - Fact-check accuracy fell about 42% with search depth (RX-01) [COMMUNITY]
- `SOCAS-IN02-SC-FIRSTDRAFT`: https://firstdraftnews.org/articles/verifying-online-information-the-absolute-essentials/ - First check: did the event happen (RX-02) [VERIFIED]
- `SOCAS-IN02-SC-DOI-RDBLTYFAIL`: https://doi.org/10.1109/tpc.1981.6447826 - Why readability formulas fail (RX-03) [VERIFIED excerpt]
- `SOCAS-IN02-SC-NMS-RFPSCORE`: https://nmsconsulting.com/consulting-rfp-scorecard/ - Proposal warning signs, practitioner guidance (RX-04) [COMMUNITY]
- `SOCAS-IN02-SC-18F-BIDS`: https://guides.18f.gov/derisking-government-tech/resources/evaluate-bids/ - Bid warning signs, including cited projects the vendor did not create (RX-05) [VERIFIED]
- `SOCAS-IN02-SC-GOOGLE-DOCGUIDE`: https://google.github.io/styleguide/docguide/best_practices.html - Minimum viable, fresh documentation (RX-06) [VERIFIED]
- `SOCAS-IN02-SC-IEEE-EARS`: https://doi.org/10.1109/re.2009.9 - EARS templates (RX-07) [VERIFIED]
- `SOCAS-IN02-SC-CLAIMDIG-GOODREQ`: https://claimdig.com/guides/good-requirements/ - Three-question requirement review (RX-08) [COMMUNITY]
- `SOCAS-IN02-SC-ARXIV-CITEAUDIT`: https://arxiv.org/pdf/2603.03299 - String-feature classifier AUC 0.876 (RX-09) [COMMUNITY]
- `SOCAS-IN02-SC-PMC-READBACK`: https://pmc.ncbi.nlm.nih.gov/articles/PMC5659252/ - Read-back: 21% vs 76% rounds with medication error, single site (RX-10) [VERIFIED]
- `SOCAS-IN02-SC-UIT-CLCREVIEW`: https://hdl.handle.net/10037/33922 - Closed-loop training review, 4 randomized controlled trials, very low certainty (RX-10) [VERIFIED]
- `SOCAS-IN02-SC-NEJM-IPASS`: https://www.nejm.org/doi/full/10.1056/NEJMsa1405556 - I-PASS bundle with training: preventable adverse events -30% (RX-11) [VERIFIED]
- `SOCAS-IN02-SC-BMJO-SBAR21`: https://bmjopen.bmj.com/content/11/12/e055247 - SBAR: outcomes improve only with multifaceted interventions (RX-11) [VERIFIED]
- `SOCAS-IN02-SC-EMSE-MENZIES-DIE`: https://doi.org/10.1007/s10664-016-9469-x - No delayed-issue effect in 171 projects (RX-13) [VERIFIED]
- `SOCAS-IN02-SC-OPENAI-CLSF`: https://openai.com/index/new-ai-classifier-for-indicating-ai-written-text/ - Classifier withdrawn 2023-07-20 (RX-14) [VERIFIED]
- `SOCAS-IN02-SC-PMC-GPTDET`: https://pmc.ncbi.nlm.nih.gov/articles/PMC10382961/ - 61.3% false positives on non-native essays (RX-14) [VERIFIED]
- `SOCAS-IN02-SC-SAGE-ABRAMI`: https://journals.sagepub.com/doi/10.3102/0034654314551063 - Critical-thinking instruction g = 0.30 (RX-15) [VERIFIED]
- `SOCAS-IN02-SC-PMC-CRTSUCCESS`: https://pmc.ncbi.nlm.nih.gov/articles/PMC5225989/ - Prior exposure inflates CRT scores (RX-15) [VERIFIED]
- `SOCAS-IN02-SC-PMC-GIGER02`: https://pmc.ncbi.nlm.nih.gov/articles/PMC200816/ - Natural frequencies, 48 doctors (RX-16) [VERIFIED]
- `SOCAS-IN02-SC-COCH-ROB2`: https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-08 - Worst-domain overall judgment (RX-17) [VERIFIED]
- `SOCAS-IN02-SC-ARXIV-COINFLIP`: https://arxiv.org/html/2606.13685 - 13.6% verdict flips on identical reruns (RX-17) [COMMUNITY]
- `SOCAS-IN02-SC-ARXIV-RUBPOS`: https://arxiv.org/html/2602.02219v2 - Rubric order flips top candidate on 16% to 39% of prompts (RX-18) [COMMUNITY]

## 7. Document History

**[2026-11-10 15:27]**
- Added: 4 old `SOCAS_RULES.md` forms found by a sign-level check: missing glossary, information scattered across documents, excessive analogies, source ranking by SOCAS count; counts now 36 candidates (21 discarded, 9 merged, 6 deferred)
- Changed: SOCAS-GN-18 target (step order in procedures to SOCAS-WR-12); SOCAS-CR-04 entry (escalation path to SOCAS-WR-12)
- Removed: SOCAS-GN-17 entry (re-entered SOCAS-IN01 as selected rule; text part stays deferred)
- Fixed: RX-17 rule count per run (19-30: 18 general rules, field file, SOCAS-AP-03 cross-loads); Next Steps reply example

**[2026-11-10 15:15]**
- Changed: SOCAS-CM-11 reason codes (DEFER-PRODUCTION removed; ask-first part merged into SOCAS-CM-08 as REF to APAPL-ST-01); SOCAS-GN-20 target (humor to SOCAS-GN-15, MECT-WC-10 covers metaphors and idioms only); dimension weights reasoning (no dimension per rule)
- Fixed: SOCAS-CR-04 reasoning (mention counts are not validity evidence); RX-17 rule count per run

**[2026-11-10 15:05]**
- Added: Inline source links at first mention in sections 2-3 (INFO-SC-05)
- Changed: Acronyms written out at first use (APAPALAN, MECT, CDC, DOI, OpenSSF, LLM, EARS, AUC, SBAR, I-PASS, RoB 2); "red flags" replaced by "warning signs"
- Fixed: SOCAS-CR-06 scope entry reason code MERGED replaced by CONTRADICTED (research shows requirement tests do not fit articles)

**[2026-11-10 14:45]**
- Initial document created: 11 drafted rules, 18 research candidates and 4 old criterion forms with status and reasoning
