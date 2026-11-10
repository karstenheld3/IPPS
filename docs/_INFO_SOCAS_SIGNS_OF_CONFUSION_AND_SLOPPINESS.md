# INFO: SOCAS - Signs of Confusion and Sloppiness

**Doc ID**: SOCAS-IN01
**Goal**: List the selected SOCAS rules ranked by priority (cost/benefit) per target file, with overlap handling for APAPALAN (As Precise As Possible, As Little As Necessary) and MECT (Minimal Explicit Consistent Terminology), as input for splitting SOCAS into 4 context-aware rule files
**Timeline**: Created 2026-03-06, Updated 6 times (2026-03-06 - 2026-11-10)

**Depends on:**
- `_INFO_SOCAS_DISCARDED_RULE_CANDIDATES.md [SOCAS-IN02]` for all discarded, merged and deferred candidates with reasoning

## Summary

**Origin:** Developed by Karsten Held 2026

- SOCAS is a quick screen of simple yes/no rules for signs of confusion and sloppiness in any content. It flags signs; it never proves a claim true or false. Deep analysis, source evaluation and fact-check stay separate commands [VERIFIED]
- SOCAS splits into 4 target files; every rule lives in exactly one file [VERIFIED: decision SOCASCONTEXT-DD-01]:
  - `SOCAS_RULES.md` (general): 18 rules + 12 application rules + 2 reporting rules. Logic, statistics, fallacies, manipulation, superficial signs
  - `SOCAS_WRITING_RULES.md`: 11 rules. Publications, reports, websites, marketing, non-code normative documents
  - `SOCAS_COMMUNICATION_RULES.md`: 8 rules. Chat, email, orders, requests, written traces of calls
  - `SOCAS_CODING_RULES.md`: 9 rules. Code, repositories, dependencies, code specifications
- Priority = cost/benefit per rule: P1 = cheap and valuable (run always), P2 = run when time allows or content type demands, P3 = run only on request. 46 selected sign rules: 34 P1, 12 P2, 0 P3; 14 application and reporting rules: 13 P1, 1 P2. Ranked lists per field: section 2.3 [ASSUMED: agent judgment from research evidence grades, section 2.1]
- Audit against the deep research: all 76 numbered research candidates (RC-N, RC-W, RC-M, RC-D, RC-G, QS, SM) and design rules R1 to R14 are accounted for as selected, merged, deferred or discarded. 10 drafted rules (all 4 P3 drafts included), 18 research candidates and 8 forms of old criteria are discarded (21), merged (9) or deferred (6) with reasoning in `_INFO_SOCAS_DISCARDED_RULE_CANDIDATES.md [SOCAS-IN02]`; the draft numbered GN-17 in version 2026-11-10 14:30 re-entered as SOCAS-GN-08 after a sign-level check against the old `SOCAS_RULES.md` (section 8) [VERIFIED: ID cross-check of both documents]
- A quick pass runs about 19-22 P1 rules (13 general + 6-9 field), close to the 17 criteria of the standalone prompt v6.2 and the [19-item surgical safety checklist](https://www.nejm.org/doi/full/10.1056/NEJMsa0810119) [VERIFIED: research IN03 F3, web check 2026-11-10]
- Overlap handling: APAPALAN and MECT prescribe how to write; SOCAS detects signs in any content, including content written by others. Where a MECT or APAPALAN rule covers a sign, SOCAS keeps only its test question and cites the rule ID as the fix. No BAD/GOOD example is copied [ASSUMED: interpretation of zero-overlap requirement, open decision OD-1 option 1]
- Statistics rules sit in the general file, web source checks in the writing file; content of the other fields that cites external sources also runs SOCAS-WR-01 [ASSUMED: open decision OD-2 option 1]
- Context awareness: every selected sign rule states an **Applies to** condition; content outside it gets `SKIP` (SOCAS-AP-04). SOCAS-AP-03 picks the field file from the content types listed at the start of sections 5-7, including IPPS document types; the condition picks the rules inside it. On code, the text rules of the general file return `SKIP` (section 4) [ASSUMED: design from research recommendation IN01 5.2]
- "Incomplete specification" (old SOCAS-CR-06) no longer runs on articles: its requirement tests move to `SOCAS-CD-08`/`CD-09` (code specifications) and `SOCAS-WR-11` (non-code normative documents); "conclusions without evidence" moves to `SOCAS-GN-04` [VERIFIED: research IN07]
- All 17 old criteria `SOCAS-CR-01` to `CR-17` are retired; section 8 maps each to its new rule or to its entry in SOCAS-IN02 [VERIFIED]

```
SOCAS run (one holistic pass, fixed rank order, SOCAS-AP-11)
├─> 1) Context first (SOCAS-AP-03): type, audience, purpose, stage
├─> 2) SOCAS_RULES.md           18 GN rules (always; 13 P1)
├─> 3) One field file by type:
│      ├─> SOCAS_WRITING_RULES.md        11 WR rules (9 P1)
│      ├─> SOCAS_COMMUNICATION_RULES.md   8 CM rules (6 P1)
│      └─> SOCAS_CODING_RULES.md          9 CD rules (6 P1)
├─> 4) Web checks (max 5 sources, SOCAS-AP-09) or "web checks: not run"
└─> 5) Score and report (SOCAS-AP-02, SOCAS-RP-01, RP-02)
```

## Table of Contents

1. [Purpose and Scope](#1-purpose-and-scope)
2. [Priority Model and Rule Format](#2-priority-model-and-rule-format)
3. [Overlap Handling with APAPALAN and MECT](#3-overlap-handling-with-apapalan-and-mect)
4. [SOCAS_RULES.md - General Rules](#4-socas_rulesmd---general-rules)
5. [SOCAS_WRITING_RULES.md - Writing and Publications](#5-socas_writing_rulesmd---writing-and-publications)
6. [SOCAS_COMMUNICATION_RULES.md - Communication](#6-socas_communication_rulesmd---communication)
7. [SOCAS_CODING_RULES.md - Code and Code Specifications](#7-socas_coding_rulesmd---code-and-code-specifications)
8. [Migration Map from SOCAS-CR-01 to SOCAS-CR-17](#8-migration-map-from-socas-cr-01-to-socas-cr-17)
9. [Next Steps](#9-next-steps)
10. [Sources](#10-sources)
11. [Document History](#11-document-history)

## 1. Purpose and Scope

SOCAS answers one question fast: does this content show signs that its author was confused or sloppy? It runs on documents, messages and code, written by people or agents. It judges the text, never the author.

In scope:
- Quick, rule-based checks an agent can run in one pass, mostly from the text alone
- Small, bounded web lookups (open a cited source, look up a package name or sponsor)

Out of scope (separate commands):
- Truth verdicts and independent evidence search: `/fact-check`
- Logic and risk review in depth: `/critique`
- Writing the fix: APAPALAN and MECT rules, applied by `/improve`
- AI-authorship detection: no rule; detectors are unreliable ([OpenAI classifier](https://openai.com/index/new-ai-classifier-for-indicating-ai-written-text/) withdrawn 2023-07-20; [61.3% false positives on non-native essays](https://pmc.ncbi.nlm.nih.gov/articles/PMC10382961/)) [VERIFIED] (SOCAS-IN01-SC-OPENAI-CLSF, SOCAS-IN01-SC-PMC-GPTDET)

Research basis: session research SOCASCONTEXT-SOCASRSRCH (2026-11-10, documents IN01 to IN10, 152 registered sources). Evidence grades in this document: A = several independent studies or large audits, B = one strong study or official analysis, C = standards body or expert consensus, D = opinion only, `[ASSUMED]` = no source found.

## 2. Priority Model and Rule Format

### 2.1 Priority = Cost / Benefit

Cost (effort for the agent per run):
- **low**: yes/no test on a quoted passage, text only
- **medium**: needs context judgment, approximate counting, or 1 web lookup
- **high**: needs a tool (scanner, metric), several web lookups, or visual inspection

Value (benefit when the sign is found):
- **high**: evidence A-B and the sign puts decisions at risk
- **medium**: evidence B-C, or high evidence with narrow scope
- **low**: evidence D or `[ASSUMED]`

Priority from cost and value:
- **P1**: low cost + high or medium value, or medium cost + high value. Runs in every SOCAS pass on matching content
- **P2**: medium cost + medium value, low cost + low value, or high cost + high value. Runs when the content type demands it or time allows
- **P3**: high cost + medium or low value, or medium cost + low value. Runs only on explicit request

Priorities are agent judgment from evidence grades, not measured [ASSUMED]. No study validates any SOCAS-style score against outcomes (rework, decision errors) [VERIFIED: gap in research IN03].

### 2.2 Rule Format

Every sign rule in sections 4.1 to 4.3 and 5 to 7 has (application and reporting rules in 4.4 use a short form: rule, priority, origin):
- Signs: what to look for
- **Applies to**: content condition; content outside it gets `SKIP` (SOCAS-AP-04). Replaces the per-type SKIP list of the standalone prompt, which let SOCAS-CR-06 run on articles
- **Test**: one yes/no question answered for a quoted passage (research rule R1)
- **Priority**: `P[N] | Cost: [level], [why] | Value: [level], [evidence]`
- **Web**: `no`, or the lookup it needs
- **Overlap**: `none`, or the APAPALAN or MECT rule IDs that prescribe the fix
- **Replaces**: old SOCAS IDs and research candidate IDs (`RC-*`, `QS*`, `SM-*`) it absorbs

ID scheme: `SOCAS-[CAT]-[NN]`. Categories: `GN` general, `WR` writing, `CM` communication, `CD` coding, `AP` application, `RP` reporting. Note: `SOCAS-CM-*` (communication signs) is a different rule set from `APAPL-CM-*` (APAPALAN communication production rules). Numbers run continuously per category: the selected rules first (this document), then the entries of `_INFO_SOCAS_DISCARDED_RULE_CANDIDATES.md [SOCAS-IN02]`. An ID is stable from this renumbering on (SOCASCONTEXT-DD-10): a re-entered candidate keeps its number and a number is never reused for another rule.

### 2.3 Selected Rules Ranked by Priority

Ranking key: priority, then value (high first), then cost (low first), then evidence grade, then ID. A time-limited run executes the P1 block of the general file and of one field file (SOCAS-AP-11). Rules whose **Applies to** condition the content does not meet return `SKIP` (for example the statistics rules SOCAS-GN-09 to GN-13 on content without figures).

Application and reporting rules (every field, always active):
- P1: SOCAS-AP-01, AP-02, AP-03, AP-04 to AP-09, AP-11, AP-12, RP-01, RP-02
- P2: SOCAS-AP-10 (decisions only)

General - `SOCAS_RULES.md` (18 rules: 13 P1, 5 P2):
1. SOCAS-GN-01 Contradictions and Impossible Numbers - P1
2. SOCAS-GN-07 Manipulation Technique - P1
3. SOCAS-GN-09 Numbers Without Base - P1
4. SOCAS-GN-11 Causal Claim Beyond Design - P1
5. SOCAS-GN-14 Noise and Filler - P1
6. SOCAS-GN-08 Overlapping Concerns and Duplicate Mechanisms - P1
7. SOCAS-GN-16 Unnecessary Complexity - P1
8. SOCAS-GN-17 Lack of Structure - P1
9. SOCAS-GN-03 Undefined or Ambiguous Key Terms - P1
10. SOCAS-GN-02 Inconsistent Naming and Format - P1
11. SOCAS-GN-04 Unsupported Conclusion - P1
12. SOCAS-GN-05 Assumption as Fact, Unqualified Claim, No Alternatives - P1
13. SOCAS-GN-10 Biased Counting - P1
14. SOCAS-GN-13 Misleading Chart - P2
15. SOCAS-GN-12 Significance and Testing Misread - P2
16. SOCAS-GN-15 Impressive Form Without Substance - P2
17. SOCAS-GN-06 Fallacy with Quote - P2
18. SOCAS-GN-18 Presentation Sloppiness - P2

Writing - `SOCAS_WRITING_RULES.md` (11 rules: 9 P1, 2 P2):
1. SOCAS-WR-06 Pressure Tactics in Commercial Text - P1
2. SOCAS-WR-01 Cited Source Missing or Changed - P1
3. SOCAS-WR-05 Undisclosed Commercial Interest - P1
4. SOCAS-WR-07 Unsubstantiated Commercial Claim - P1
5. SOCAS-WR-09 Empty Structure - P1
6. SOCAS-WR-10 Vague Word Where a Measure Belongs - P1
7. SOCAS-WR-11 Requirement Quality in Normative Documents - P1
8. SOCAS-WR-02 Specific Claim Without Source - P1
9. SOCAS-WR-03 Missing Date, Author, Version or Scope - P1
10. SOCAS-WR-04 Responsible Party and Interest Unclear - P2
11. SOCAS-WR-08 Outdated Content - P2

Communication - `SOCAS_COMMUNICATION_RULES.md` (8 rules: 6 P1, 2 P2):
1. SOCAS-CM-01 Who Does What by When Unclear - P1
2. SOCAS-CM-04 Underspecified or Conflicting Order - P1
3. SOCAS-CM-05 Tone Depends on Unstated Intent - P1
4. SOCAS-CM-06 Rude or Hostile Language - P1
5. SOCAS-CM-07 Pressure Without Reason or Inverted Priorities - P1
6. SOCAS-CM-02 Lookups Needed to Act - P1
7. SOCAS-CM-03 Unbacked Basis for Action - P2
8. SOCAS-CM-08 Omitted or Replaced Information - P2

Coding - `SOCAS_CODING_RULES.md` (9 rules: 6 P1, 3 P2):
1. SOCAS-CD-02 Insecure Construction - P1
2. SOCAS-CD-08 Behavior, Edge Cases or Acceptance Undefined - P1
3. SOCAS-CD-01 Invented Dependency - P1
4. SOCAS-CD-09 Unverifiable Requirement Wording - P1
5. SOCAS-CD-04 Change Too Large to Review - P1
6. SOCAS-CD-07 Missing Tests, History or Setup - P1
7. SOCAS-CD-05 Excess Complexity - P2
8. SOCAS-CD-06 Stale or Unhealthy Dependency - P2
9. SOCAS-CD-03 Unresolved Debt Markers - P2

### 2.4 Selection and Discard Criteria

A drafted rule or research candidate is not selected when one criterion applies (details and per-candidate reasoning in SOCAS-IN02):
- **WEAK-P3**: priority P3 (high cost with medium or low value, or medium cost with low value) - contradicts the quick-screen purpose
- **WEAK-UNSOURCED**: low value, no evidence found, research advises to leave it out until sourced
- **MERGED**: another selected SOCAS rule tests the same sign; the sign moves into that rule
- **DEFER-PRODUCTION**: an APAPALAN or MECT rule covers the sign completely and the SOCAS draft has low value
- **DEFER-COMMAND**: the check needs deep work that belongs to `/fact-check`, `/critique` or `/research`
- **NOT-A-SIGN**: production rule (how to write) or method that assesses people, not content
- **CONTRADICTED**: evidence speaks against the rule
- **OPEN-DECISION**: design alternative kept for a pending user decision

Kept despite low value: SOCAS-GN-18 (typos are the literal sign of sloppiness, no other rule covers them, cost is low) and SOCAS-CD-03 (agent-written code leaves unfinished stubs; no other rule covers them, cost is low). Both stay P2.

## 3. Overlap Handling with APAPALAN and MECT

### 3.1 Principle: Production Rules vs Detection Signs

- APAPALAN (`APAPALAN_RULES.md`) and MECT (`MECT_WRITING_RULES.md`, `MECT_CODING_RULES.md`) are production rules: how to write text and code
- SOCAS rules are detection signs: how to judge content, including content you did not write
- One sign, one owner. When a production rule already defines the fix, SOCAS does not restate it

### 3.2 Three Handling Types

- **NONE**: no APAPALAN or MECT rule covers the sign. SOCAS owns sign, test and examples. Most logic, statistics, fallacy, manipulation, sourcing, security and dependency rules
- **REF**: an APAPALAN or MECT rule prescribes the fix. SOCAS keeps the test question and only the signs the production rule does not list; the rule entry cites the production rule ID as the fix. SOCAS copies no BAD/GOOD example from it. `/improve` applies the cited rule
- **DEFER**: a production rule covers the sign completely. SOCAS has no own rule; a SOCAS run reports violations under the production rule ID. List in 3.3

The old SOCAS criteria copied BAD/GOOD examples from APAPALAN (for example "garage / service / workshop" from APAPL-NM-01, "Use OBO for SPO" from APAPL-PR-06, "Retry 3 times" from APAPL-PR-07). The split removes these copies.

### 3.3 DEFER List (Signs SOCAS Does Not Own)

- Questions and requests not labeled or not in own paragraph: APAPL-CM-02
- Dates without weekday, ISO format or timezone: APAPL-CM-03, APAPL-PR-01
- Abbreviations not spelled out at first use: APAPL-PR-06
- Passive voice outside requirements: MECT-VO-01 (a requirement without actor stays a sign of SOCAS-WR-11)
- Identifier naming, word pairs, casing, prefixes in code: MECT-PR-01 to PR-03, MECT-ND-01 to ND-09, MECT-CO-01 to CO-05
- Comment wording, error messages, log messages: MECT-PR-04 to PR-07, MECT-BR-02, MECT-BR-05
- User-facing messages and documentation wording in code: MECT-DC-01 to DC-03
- Text that repeats the same information, items of mixed granularity in one list: APAPL-BR-03, MECT-LT-02 (text part of SOCAS-GN-08; duplicate mechanisms in a design stay in SOCAS-GN-08)
- Items in no discernible order: APAPL-ST-05, MECT-LT-02 (draft SOCAS-GN-21; steps that cannot run in the stated order stay in SOCAS-WR-11)
- Metaphors, idioms and slang that obscure the claim: MECT-WC-10 (draft SOCAS-GN-22; humor without information stays in SOCAS-GN-14)

### 3.4 Overlap Count

- REF rules: 16 of 46 selected sign rules (GN 7, WR 4, CM 4, CD 1)
- NONE rules: 30 of 46
- DEFER: signs of 3 drafts moved to production rules (text part of SOCAS-GN-08, presentation-order part of GN-21, metaphor and idiom part of GN-22)
- No SOCAS rule restates an APAPALAN or MECT rule body [ASSUMED: holds once the 4 files are written from this document]

## 4. SOCAS_RULES.md - General Rules

Runs on every content type. Holds the abstract form of signs; field files hold concrete forms. A rule whose **Applies to** condition the content does not meet returns `SKIP`; a rule whose condition is met but that has too little to test returns `NO INFORMATION` (SOCAS-AP-04). Neither is a score.

On code (source code, scripts, configuration, diffs), SOCAS-GN-02, GN-03, GN-14, GN-16, GN-17 and GN-18 return `SKIP`: naming, comments, error and log messages in code belong to `MECT_CODING_RULES.md` (DEFER list in 3.3), complexity to SOCAS-CD-05. Technical READMEs and code specifications are text and run all general rules.

Selected: 18 rules. Drafts not selected (GN-19, GN-20, GN-21, GN-22): `_INFO_SOCAS_DISCARDED_RULE_CANDIDATES.md [SOCAS-IN02]`.

### 4.1 Consistency and Reasoning

#### SOCAS-GN-01: Contradictions and Impossible Numbers

- Two statements, figures, dates, owners or scopes contradict each other
- Message forms: two deadlines, two owners or two scopes in one message; "urgent" and "no rush" together
- Numbers that cannot be true: parts do not sum to the total, percentages that should sum to 100 do not, a mean impossible for the stated sample size, a date before the event it describes
- **Applies to**: all content
- **Test**: Do two passages contradict each other, or is a number arithmetically impossible?
- **Priority**: P1 | Cost: low, text only (arithmetic by tool when available) | Value: high, evidence A ([statcheck](https://link.springer.com/article/10.3758/s13428-015-0664-2): half of psychology papers had an inconsistent p-value)
- **Web**: no
- **Overlap**: none
- **Replaces**: SOCAS-CR-01 (contradiction part), RC-N01, RC-M10, SOCAS-CM-09 draft (merged)

#### SOCAS-GN-02: Inconsistent Naming and Format

- One concept with several names, one name for several concepts, format changes without reason
- **Applies to**: all text; not code (section 4)
- **Test**: Is one thing named, numbered or formatted in two ways?
- **Priority**: P1 | Cost: low, text only | Value: medium, evidence C (requirement consistency, [ISO 29148 summary](https://claimdig.com/guides/good-requirements/))
- **Web**: no
- **Overlap**: REF - fix by APAPL-NM-01, APAPL-PR-09, MECT-WC-05
- **Replaces**: SOCAS-CR-01 (naming part), SOCAS-CR-12 (inconsistent formatting)

#### SOCAS-GN-03: Undefined or Ambiguous Key Terms

- Key term undefined for the intended reader; a word with several readings; a dangerous meta-word without qualifier; a creative name or hidden reference (easter egg) the reader must decode
- **Applies to**: all text; not code (section 4)
- **Test**: Would the intended reader understand every key term the first time it appears?
- **Priority**: P1 | Cost: low, text only | Value: medium, evidence B-C ([IBM](https://www.ibm.com/docs/en/erqa?topic=assistant-guidelines-good-requirements) and [NASA](https://www.nasa.gov/reference/appendix-c-how-to-write-a-good-requirement/) requirement guidelines; [European Union (EU) claims study](https://op.europa.eu/en/publication-detail/-/publication/f7c4cb8b-f877-11ee-a251-01aa75ed71a1/language-en): 54 of 150 claims unclear)
- **Web**: no
- **Overlap**: REF - fix by APAPL-PR-12, APAPL-NM-02, APAPL-NM-03, MECT-WC-01, MECT-WC-09. Abbreviations: DEFER to APAPL-PR-06. Metaphors, idioms: DEFER to MECT-WC-10
- **Replaces**: SOCAS-CR-02, SOCAS-CR-07 (creative names part), SOCAS-GN-22 draft (merged)

#### SOCAS-GN-04: Unsupported Conclusion

- A conclusion does not follow from evidence stated in the content; missing steps; claim without grounds or without a link (warrant) between grounds and claim
- **Applies to**: content that draws conclusions or makes recommendations
- **Test**: Does each conclusion follow from evidence stated in the content, with the steps in between?
- **Priority**: P1 | Cost: low, text only | Value: medium, evidence C ([Toulmin method](https://writing.colostate.edu/guides/guide.cfm?guideid=58): claim, grounds, warrant)
- **Web**: no
- **Overlap**: none
- **Replaces**: SOCAS-CR-10 (core), SOCAS-CR-06 (part "conclusions without evidence"), RC-G01

#### SOCAS-GN-05: Assumption as Fact, Unqualified Claim, No Alternatives

- Assumption presented as fact; universal or causal claim ("proves", "always", "guarantees") without stated limits or conditions; one explanation only for a surprising result; no alternatives or trade-offs; unjustified selection ("three reasons" - why these three?)
- Appeal to an expert that fails one of the six critical questions (expertise, field, exact assertion, trustworthiness, agreement with other experts, backing evidence)
- **Applies to**: content that makes claims, choices or recommendations
- **Test**: Is an assumption or strong claim stated without limits, or is a choice, explanation or expert opinion given without the alternatives or evidence considered?
- **Priority**: P1 | Cost: low, text only | Value: medium, evidence C ([Calling Bullshit course](https://www.callingbullshit.org/videos.html): generate several hypotheses; [Walton critical questions](https://cgi.csc.liv.ac.uk/~floriana/CMNA/WaltonReed.pdf))
- **Web**: no (expert credentials: optional 1 lookup)
- **Overlap**: none
- **Replaces**: SOCAS-CR-10 (alternatives part), SOCAS-GN-19 draft (merged), RC-N07, RC-G02, RC-G03, QS10, SM-19

#### SOCAS-GN-06: Fallacy with Quote

- A passage matches one of 7 fallacy families: strawman, begging the question, equivocation, cherry-picking, appeal to popularity, suppressed evidence, post hoc. Personal attack, false dichotomy and appeal to emotion belong to SOCAS-GN-07
- Finding needs quote, family name, one sentence of reasoning, and a check that context does not make the argument sound. No label without a quote
- **Applies to**: content that argues for a position
- **Test**: Does a quoted passage match a fallacy family, and does the context fail to make the argument sound?
- **Priority**: P2 | Cost: medium, context check against false positives | Value: medium, evidence C ([Internet Encyclopedia of Philosophy](https://iep.utm.edu/fallacy/): a fallacy label cannot replace examination of the context)
- **Web**: no
- **Overlap**: none
- **Replaces**: RC-G04

#### SOCAS-GN-07: Manipulation Technique

- Emotionally manipulative language, incoherent arguments, false dichotomy, scapegoating, ad hominem, fake experts, false balance
- Abstract form; concrete commercial forms in SOCAS-WR-06, message forms in SOCAS-CM-07
- **Applies to**: content that tries to persuade or to change the reader's view
- **Test**: Does the text use a named manipulation technique instead of evidence?
- **Priority**: P1 | Cost: low, text only | Value: high, evidence A ([7 preregistered studies](https://www.science.org/doi/10.1126/sciadv.abo6254), n = 6464 + 22,632: technique recognition is teachable)
- **Web**: no
- **Overlap**: none
- **Replaces**: SOCAS-CR-17 (abstract part), RC-N08, RC-G05

#### SOCAS-GN-08: Overlapping Concerns and Duplicate Mechanisms

- Two parts of a design, process, rule set or codebase do the same job in different ways; a new mechanism for a problem the content already solves elsewhere; concepts that overlap without a stated boundary; responsibilities split inconsistently between parts; a duplicated mechanism or code block with slight variations
- **Applies to**: content that describes a design, system, process, rule set or code (specifications, architecture and process documents, rule files, workflows, source code); not narrative or persuasive text
- **Test**: Do two parts do the same job differently, or does the content add a mechanism for a problem it already solves elsewhere?
- **Priority**: P1 | Cost: low, cross-passage comparison as in SOCAS-GN-01 | Value: medium, evidence B with narrow scope ([inconsistent changes to code clones](https://wwwbroy.in.tum.de/~juergens/publications/ICSE2009_RP_0110_juergens.pdf): 52% of 1,427 clone groups were changed inconsistently, every second unintentional inconsistency was a fault, 107 confirmed faults in 5 systems); transfer to non-code designs [ASSUMED]
- **Web**: no
- **Overlap**: none (APAPL-BR-03 and MECT-LT-02 cover repeated text and list grouping, not duplicate mechanisms; that text part stays DEFER, section 3.3)
- **Replaces**: SOCAS-CR-03 (design part), `/verify` and `/improve` sign "new solutions for already solved problems", the draft numbered GN-17 in version 2026-11-10 14:30 (re-entered 2026-11-10)

### 4.2 Numbers and Statistics

Each rule applies only to content with figures, rates, studies or charts (see **Applies to**); otherwise `SKIP`. Training does not protect: researchers endorsed on average more than 3 of 6 false statements about confidence intervals ([Hoekstra et al. 2014](https://www.ejwagenmakers.com/inpress/HoekstraEtAlPBR.pdf)) [VERIFIED] (SOCAS-IN01-SC-HOEKSTRA-CI). Do not raise a score for statistical vocabulary or credentials.

#### SOCAS-GN-09: Numbers Without Base

- Percentage, ratio or "x times" without raw numbers or base; relative risk without absolute risk; test accuracy without prevalence; sample size missing or small for a strong claim; "average" without mean or median
- **Applies to**: content with percentages, ratios, averages or study results
- **Test**: Does each percentage, ratio or average come with its raw numbers, base and sample size?
- **Priority**: P1 | Cost: low, text only | Value: high, evidence A-B ([natural frequencies](https://pmc.ncbi.nlm.nih.gov/articles/PMC200816/): most of 48 doctors answered correctly vs about 8% with conditional probabilities)
- **Web**: no
- **Overlap**: none
- **Replaces**: QS1, QS2, QS4, SM-01 to SM-04, SM-13

#### SOCAS-GN-10: Biased Counting

- Self-selected or opt-in sample; response rate missing; only survivors or winners counted; groups that differed before the treatment compared as if randomized
- **Applies to**: content that reports surveys, samples, case collections or success stories
- **Test**: Does the content state who was counted and who is missing?
- **Priority**: P1 | Cost: low, text only | Value: medium, evidence C (course material, [Huff summary](https://thinkr.org/newsletter/how-to-lie-with-statistics))
- **Web**: no
- **Overlap**: none
- **Replaces**: QS3, SM-06 to SM-08

#### SOCAS-GN-11: Causal Claim Beyond Design

- Causal verbs (causes, drives, leads to) on observational data; before-and-after read as effect; improvement of an extreme group read as treatment effect (regression to the mean); pooled totals hiding opposite subgroup trends (Simpson's paradox); the conclusion concerns a different quantity than the one measured (survival rate read as life gained)
- **Applies to**: content that states causes or effects from data or experience
- **Test**: Does the causal wording match the design, and does the conclusion concern the measured quantity?
- **Priority**: P1 | Cost: low, text only | Value: high, evidence B ([BMJ on regression to the mean](https://pmc.ncbi.nlm.nih.gov/articles/PMC1125994/); [Gigerenzer on survival rates](https://journals.sagepub.com/doi/full/10.1111/j.1539-6053.2008.00033.x))
- **Web**: no
- **Overlap**: none
- **Replaces**: QS5, QS6, SM-09 to SM-12, SM-14

#### SOCAS-GN-12: Significance and Testing Misread

- "Significant" used as "important"; no effect size or interval; "no significant difference, so no effect"; confidence interval read as probability; many outcomes measured, one reported; hypothesis formed after seeing the data
- **Applies to**: content that reports statistical tests, significance or confidence intervals
- **Test**: Is effect size or interval given, and is it stated how many things were tested?
- **Priority**: P2 | Cost: medium, needs statistics judgment | Value: medium, evidence B ([American Statistical Association (ASA) statement on p-values](https://www.tandfonline.com/doi/full/10.1080/00031305.2016.1154108)) with narrow scope (research content only)
- **Web**: no
- **Overlap**: none
- **Replaces**: QS7, QS8, SM-15 to SM-17, SM-20

#### SOCAS-GN-13: Misleading Chart

- Bar axis not starting at zero; dual axes; bubbles sized by diameter; inverted axis; no axis label or unit
- **Applies to**: content with charts or graphs
- **Test**: Are axes, scales and sizes honest and labeled?
- **Priority**: P2 | Cost: high, needs visual inspection | Value: high, evidence B ([ACM CHI 2015 conference study](https://dl.acm.org/doi/10.1145/2702123.2702608); [n = 329 study](https://doi.org/10.1145/3380851.3416762): misreading regardless of visualization training)
- **Web**: no
- **Overlap**: none
- **Replaces**: QS9, SM-18

### 4.3 Signal, Noise and Form

#### SOCAS-GN-14: Noise and Filler

- Filler and hedging; obvious things explained at length while complex things stay unexplained; the same point restated in different words; jokes or humor that carry no information
- **Applies to**: all text; not code (section 4)
- **Test**: Can you delete the passage without the reader losing information?
- **Priority**: P1 | Cost: low, text only | Value: medium, evidence B ([concise web text](https://www.nngroup.com/articles/concise-scannable-and-objective-how-to-write-for-the-web/): +58% measured usability, 51 users)
- **Web**: no
- **Overlap**: REF - fix by APAPL-PR-07, APAPL-BR-02, APAPL-BR-03, MECT-LT-04 (humor: none)
- **Replaces**: SOCAS-CR-08, SOCAS-CR-07 (humor part)

#### SOCAS-GN-15: Impressive Form Without Substance

- Abstract statement that cannot be false (buzzword profundity); impressive detail (jargon, figures, technical terms) irrelevant to the logic of the claim; claim supported only by repeating it; boasting without facts; interesting but irrelevant material
- **Applies to**: content that argues or explains; not reference lists, data tables or code
- **Test**: Could the statement be false, and does the impressive detail support the argument?
- **Priority**: P2 | Cost: medium, relevance judgment | Value: medium, evidence B ([pseudo-profound sentences](https://journal.sjdm.org/15/15923a/jdm15923a.pdf) rated 2.6 of 5; [irrelevant neuroscience](https://pmc.ncbi.nlm.nih.gov/articles/PMC2778755/) made bad explanations more satisfying to novices)
- **Web**: no
- **Overlap**: REF - fix by APAPL-PR-07
- **Replaces**: SOCAS-CR-07 (irrelevant material part), RC-G06 to RC-G09

#### SOCAS-GN-16: Unnecessary Complexity

- Jargon where plain language works; complicated constructions for simple matters; long words to sound expert; a design, process or solution more complex than the problem needs (over-engineering, indirection without benefit)
- **Applies to**: all text, including designs and processes described in text; not code (section 4; code uses SOCAS-CD-05)
- **Test**: Is there a simpler word, sentence or solution that says or does the same?
- **Priority**: P1 | Cost: low, text only | Value: medium, evidence B ([longer words lowered judged author intelligence](https://onlinelibrary.wiley.com/doi/10.1002/acp.1178); [accessible abstracts](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2021.714321/full) raised understanding 47.9% to 57.9%); design part [ASSUMED], by analogy to SOCAS-CD-05
- **Web**: no
- **Overlap**: REF - fix by MECT-WC-02, MECT-VO-03 (design part: none)
- **Replaces**: SOCAS-CR-11 (text and design part)

#### SOCAS-GN-17: Lack of Structure

- Long text without breaks; nothing the reader can cite (no headings, numbers, IDs); long document without table of contents
- **Applies to**: text over about 300 words [ASSUMED threshold]; not code (section 4)
- **Test**: Can the reader find and cite a specific point?
- **Priority**: P1 | Cost: low, text only | Value: medium, evidence B ([guideline-optimized application programming interface (API) documentation](https://doi.org/10.1145/3380851.3416759): task accuracy 86.35% vs 74.24%)
- **Web**: no
- **Overlap**: REF - fix by APAPL-PR-05, APAPL-ST-06, APAPL-ST-07
- **Replaces**: SOCAS-CR-09

#### SOCAS-GN-18: Presentation Sloppiness

- Typos and grammatical errors; broken internal references ("see above", missing section); wrong dates. External sources: SOCAS-WR-01; outdated content: SOCAS-WR-08; stale code: SOCAS-CD-06
- **Applies to**: all text; not code (section 4)
- **Test**: Are there typos, grammatical errors, broken internal references or wrong dates?
- **Priority**: P2 | Cost: low, text only | Value: low, `[ASSUMED]` (no study shows sloppiness predicts unreliable content)
- **Web**: no
- **Overlap**: REF - fix by APAPL-PR-04
- **Replaces**: SOCAS-CR-12 (typos, grammatical errors and internal references)

### 4.4 Application and Reporting Rules

These rules govern every SOCAS run, in all 4 files. Format: rule, priority with reason, origin.

#### SOCAS-AP-01: Quote and Rule ID per Finding

- Every finding names the rule (`[written-out name] ([ID])`), quotes the passage (max 25 words) and gives its location. No quote, no deduction
- **Priority**: P1 | Cost: low | Value: high, evidence B ([CheckEval](https://aclanthology.org/2025.emnlp-main.796/): decomposed yes/no questions raised agreement across 12 judge models by 0.45)
- **Replaces**: SOCAS-AP-01 (same ID, extended by location)

#### SOCAS-AP-02: Scoring and Rework Threshold

- Per rule one of 6 values, anchored by the passages that pass the test (standalone prompt v6.2 Consistency Rule 3): 0 passages = 10; 1 minor passage = 8; 2+ minor or 1 noticeable = 6; reader must ask back or may misunderstand = 4; decisions at risk or repeated across the content = 2; content unusable for its purpose = 0. 6 or lower = flagged; 4 or lower = violated
- The verdict comes from the count of violated rules (SOCAS-RP-02); 3+ violated rules = rework recommendation. A mean score over applicable rules is informational only, with equal weights. The selected rules carry no dimension, so the 40/30/20/10 dimension weights of the standalone prompt apply only after every rule is assigned to a dimension
- **Priority**: P1 | Cost: low | Value: high, evidence A-B ([Dawes 1979](https://doi.org/10.1037/0003-066x.34.7.571): equal-weight models predict as well as fitted weights; no source found for 40/30/20/10)
- **Replaces**: SOCAS-AP-02 (same ID), research rules R4 (equal weights), R5 (verdict band, decimals informational); weights decision open [ASSUMED]

#### SOCAS-AP-03: Context First and File Selection

- Before any rule runs: state content type, audience, purpose and stage (draft, working version, final version). Then load `SOCAS_RULES.md` plus one field file: writing, communication or coding. The content types of each field, including IPPS document types, are listed at the start of sections 5, 6 and 7
- Mixed content: score each part with its own field file; violated rules of all parts add up to one verdict, and a rule violated in two parts counts once. Direct commercial messages (sales email, offer sent by chat) load the communication file plus SOCAS-WR-05 to WR-07. Content of any field that cites external sources also runs SOCAS-WR-01. Documents that recommend actions or decisions (reports, proposals, INFO documents) also run SOCAS-CM-01
- **Priority**: P1 | Cost: low | Value: medium, evidence C (research rules R3 and R6; by analogy the Stop step of the [SIFT method](https://www.aft.org/ae/spring2025/caulfield_wineburg) (Stop, Investigate the source, Find other coverage, Trace the claim): 30 seconds of context improved weak critical thinkers' decisions)
- **Replaces**: SOCAS-AP-03 (same ID, redefined from "context-appropriate subset" to file selection), research rules R3 (short core plus field modules), R6 (context first), standalone prompt Principle 6 and "Applicability by Content Type"

#### SOCAS-AP-04: SKIP vs NO INFORMATION

- `SKIP` = the content does not meet the rule's **Applies to** condition; the finding names the unmet condition in one line. `NO INFORMATION` = the condition is met but the content gives too little to test. Neither creates a deduction. When it is unclear whether the condition is met, run the rule
- **Priority**: P1 | Cost: low | Value: medium, evidence B ([Cochrane Risk of Bias 2 (RoB 2) tool](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-08) uses a separate "No information" answer)
- **Replaces**: research rule R7

#### SOCAS-AP-05: One Passage, One Finding

- A passage counts for the one rule whose test fits best. The concrete field rule takes precedence over its abstract general rule (SOCAS-WR-06 before SOCAS-GN-07)
- **Priority**: P1 | Cost: low | Value: medium, `[ASSUMED]` (prevents double deduction)
- **Replaces**: standalone prompt Consistency Rule 6

#### SOCAS-AP-06: Scoring Guard

- No credit for polish, visual design, long words, credentials, statistical vocabulary or repeated assertion. No rule judges authorship (human or AI)
- **Priority**: P1 | Cost: low | Value: high, evidence A-B ([design look appeared in 46.1% of 2,684 credibility comments](https://credibility.stanford.edu/pdf/How_Do_People_Evaluate_a_Web_Site%27s_Credibility_v37.pdf); AI detectors unreliable, see section 1)
- **Replaces**: RC-G10, research rule R13, standalone prompt Principle 3

#### SOCAS-AP-07: Tolerant Thresholds

- No exact-count thresholds unless a counting tool ran on the final text. Use "several" or "most", or label a count `approx`
- **Priority**: P1 | Cost: low | Value: medium, evidence B ([large language models (LLMs) fail at counting repeated tokens](https://dl.acm.org/doi/10.1145/3818606))
- **Replaces**: research rule R9; standalone prompt Consistency Rule 7 ("3+ per 1,000 words: count, do not estimate")

#### SOCAS-AP-08: Self-Evaluation Flag

- When the scoring agent wrote the content, the output states `self-evaluation`. When available, a model other than the author model scores the content [ASSUMED: common mitigation, not measured for SOCAS]
- **Priority**: P1 | Cost: low | Value: medium, evidence B ([LLM judges score their own output higher](https://arxiv.org/abs/2404.13076), NeurIPS 2024)
- **Replaces**: research rule R11

#### SOCAS-AP-09: Web Budget

- Open max 5 sources per run, decision-relevant first, one claim per source. Status per source: `OK: confirmed`, `WARNING: changed`, `ERROR: not found`, `SKIP: inaccessible`. A dead link is `SKIP`, not fabrication. A run without web access prints `web checks: not run`
- Registry and dependency lookups (SOCAS-CD-01, CD-06) run by tool when available; without a tool, unknown or unusual names come first and each lookup counts against the budget
- **Priority**: P1 | Cost: medium, web access | Value: high, evidence B ([fact-check accuracy fell about 42% as tool calls grew from 2 to 150](https://arxiv.org/html/2605.06635v1), preprint)
- **Replaces**: research rule R12, standalone prompt Sourcing Check step 1

#### SOCAS-AP-10: Run-to-Run Noise

- Score each content separately; never rank several contents by score alone. For decisions, run twice and compare verdict bands
- **Priority**: P2 | Cost: medium, second run | Value: medium, evidence C ([13.6% pairwise verdict flips on identical reruns](https://arxiv.org/html/2606.13685), preprint)
- **Replaces**: research rules R10, R14

#### SOCAS-AP-11: Run Order

- One holistic pass over all applicable rules in the fixed rank order of section 2.3: general file first, then the field file; within each file P1 before P2. Quote before score: collect the quotes of all rules first, apply SOCAS-AP-05 (field rule before general rule), then score. A time-limited run stops after the P1 rules and states `P2 rules: not run`
- **Priority**: P1 | Cost: low | Value: medium, evidence C ([scoring all criteria in one prompt preserved consistency](https://arxiv.org/html/2610.12083v1); [criteria order shifts scores](https://arxiv.org/html/2602.02219v2), so the order must be fixed; preprints)
- **Replaces**: research rule R8 (fixed ID order replaced by fixed rank order)

#### SOCAS-AP-12: Presence Tests Do Not Violate Alone

- A rule that only tests whether a feature is present (SOCAS-WR-03 date and author, SOCAS-WR-04 responsible party, SOCAS-CD-07 tests and setup) scores 6 at worst (flagged, not violated), unless the absence blocks the purpose of the content. A finding of SOCAS-WR-01 (opened source missing or changed) can violate alone, because it rests on the source itself
- **Priority**: P1 | Cost: low | Value: medium, evidence B by inference (easy-to-fake surface features misled historians and students, so surface features discriminate poorly; [fact-checkers who left the page](https://journals.sagepub.com/doi/10.1177/016146811912101102) judged better and faster; 45 participants)
- **Replaces**: research rule R2

#### SOCAS-RP-01: Finding Format

- Each finding: severity label, written-out rule name with ID, quote, location, one-line reason. Severity follows the rule score: `LOW` = 6, `MEDIUM` = 4, `HIGH` = 2, `CRITICAL` = 0 (standalone prompt v6.2 Severity Labels)
- **Priority**: P1 | Cost: low | Value: high (output is checkable)
- **Replaces**: SOCAS-RP-01 (same ID; severity scale aligned with standalone prompt: LOW, MEDIUM, HIGH, CRITICAL)

#### SOCAS-RP-02: Summary Format

- After findings: violated rules as `N of T` applicable rules, count of `SKIP` rules, verdict, `web checks: not run` or source count, `self-evaluation` when applicable, `P2 rules: not run` for time-limited runs. Verdicts: `OK` (0 violated), `PARTIAL FAIL` (1-2), `FAIL` (3+)
- **Priority**: P1 | Cost: low | Value: high (one-line decision)
- **Replaces**: SOCAS-RP-02 (same ID; the verdict words `PASS`, `ACCEPTABLE`, `REWORK` are replaced by the standalone prompt status words)

## 5. SOCAS_WRITING_RULES.md - Writing and Publications

Content types: articles, reports, ebooks, whitepapers, INFO documents, news, blog posts, slide decks, websites, offers, proposals, newsletters, marketing and sales text, user documentation, review outputs (`_CRITIQUE`, `_FACT-CHECK`), tracking files (NOTES, PROBLEMS, PROGRESS, FAILS), and non-code normative documents (policies, standard operating procedures (SOPs), process descriptions, standards, rule files, guides, templates, workflows, `SKILL.md` files). Code specifications and technical READMEs use section 7; prompts and other one-time orders for agents use section 6.

Selected: 11 rules. Discarded, merged or deferred: draft WR-12, original-source and other-coverage checks (RC-W05, RC-W06, deferred to `/fact-check`), readability formulas, proposal warning signs, requirement templates and others: `_INFO_SOCAS_DISCARDED_RULE_CANDIDATES.md [SOCAS-IN02]`.

### 5.1 Sources and Provenance

#### SOCAS-WR-01: Cited Source Missing or Changed

- A cited source does not exist, or exists but says something different (other figure, date, scope or wording)
- A reference without enough data to find it (no author, year or venue) is searched by title; not found = `ERROR: not found`. A present digital object identifier (DOI) proves nothing: 64% of fabricated references with a DOI had a valid DOI pointing to an unrelated article
- **Applies to**: content that cites sources (links, named studies, "according to")
- **Test**: Does the opened source exist and say what the content claims at the cited location?
- **Priority**: P1 | Cost: medium, web within SOCAS-AP-09 budget | Value: high, evidence A ([LLM references: 18% to 55% fabricated](https://pmc.ncbi.nlm.nih.gov/articles/PMC10484980/); [64% of fabricated DOIs pointed to unrelated articles](https://pmc.ncbi.nlm.nih.gov/articles/PMC12658395/))
- **Web**: yes, max 5 sources
- **Overlap**: none
- **Replaces**: SOCAS-CR-12 (broken and stale external references), standalone prompt Sourcing Check, RC-W01, RC-N10, SOCAS-WR-12 draft (merged)

#### SOCAS-WR-02: Specific Claim Without Source

- A sentence with a number, named party, date or money value gives no source for it
- **Applies to**: content that states facts with numbers, named parties, dates or money values
- **Test**: Does each specific factual claim name where it comes from?
- **Priority**: P1 | Cost: low, text only | Value: medium, evidence C ([check-worthy sentences](https://ceur-ws.org/Vol-3677/paper4.pdf) contain more numbers and named entities)
- **Web**: no
- **Overlap**: none
- **Replaces**: RC-N03

#### SOCAS-WR-03: Missing Date, Author, Version or Scope

- No date, no named author or owner, no version, no stated scope or coverage limits
- **Applies to**: documents shared beyond the author (stage working version or final version); not drafts. In a repository, version control records date and author; only version and scope are tested
- **Test**: Can the reader tell when, by whom and for what scope the content was written?
- **Priority**: P1 | Cost: low, text only | Value: medium, evidence C ([AACODS checklist](https://fac.flinders.edu.au/dspace/api/core/bitstreams/e94a96eb-0334-4300-8880-c836d4d9a676/content) (Authority, Accuracy, Coverage, Objectivity, Date, Significance): no discernible date is "a strong concern")
- **Web**: no
- **Overlap**: none (APAPL-PR-01 governs date format, not presence)
- **Replaces**: RC-N06

#### SOCAS-WR-04: Responsible Party and Interest Unclear

- Organizational or customer-facing content with no named responsible person or organization, only generic contacts (info@), or no way to tell the publisher's interest
- **Applies to**: organizational or customer-facing content (websites, offers, newsletters, customer policies); not articles by a named author, memos or internal specifications
- **Test**: Can the reader find who is responsible for this content and what their interest is?
- **Priority**: P2 | Cost: medium, 1 web lookup of the publisher | Value: medium, evidence B ([checking the source in other tabs beats close reading](https://journals.sagepub.com/doi/10.1177/016146811912101102)); the [Stanford credibility comments](https://credibility.stanford.edu/pdf/How_Do_People_Evaluate_a_Web_Site%27s_Credibility_v37.pdf) show only that readers look at sponsor identity and company motive, not that the sign is valid
- **Web**: optional, 1 lookup
- **Overlap**: REF - contact format fixed by APAPL-PR-03
- **Replaces**: SOCAS-CR-04 (reworded from "named contact" to "responsible party and interest"), RC-W02

### 5.2 Commercial Intent and Persuasion

#### SOCAS-WR-05: Undisclosed Commercial Interest

- Selling while presenting as information, education or opinion; sponsor or funder not named; independence claim contradicted by a commercial relationship; call to action only after long emotional build-up; hidden or recurring costs revealed late; guilt-inducing decline options; author condemns competitors for tactics it uses itself; advertising formatted as editorial content; comparisons or rankings ordered by paid placement
- **Applies to**: content with a call to action, a vendor or sponsor as author, or product recommendations
- **Test**: Does content that presents itself as information, education or opinion lose its purpose when the final call to action is removed, or does it hide a commercial interest of the author? Openly commercial content (offer, product page, sales email) passes the first part
- **Priority**: P1 | Cost: medium, 1 web lookup when no sponsor is named | Value: high, evidence A ([Cochrane review](https://www.cochrane.org/evidence/MR000033_industry-sponsorship-and-research-outcome): sponsored studies reached favorable conclusions more often, relative risk (RR) 1.34)
- **Web**: optional, 1 lookup of author or publisher
- **Overlap**: none
- **Replaces**: SOCAS-CR-16, RC-W03

#### SOCAS-WR-06: Pressure Tactics in Commercial Text

- Artificial scarcity or deadline on non-scarce goods; countdown timers; unverifiable social proof ("thousands of customers"); testimonials without disclosed payment or connection; unsolicited "free" gift creating obligation; small ask (quiz, trial) escalating to a large ask; cancel harder than sign-up; fear appeal only the product solves; in-group vs out-group framing; purchase framed as moral duty or identity act ("join the movement")
- Concrete commercial form of SOCAS-GN-07 (SOCAS-AP-05: this rule takes precedence)
- **Applies to**: commercial or persuasive content (offers, sales text, marketing, fundraising)
- **Test**: Does the text push the reader with pressure, fear, invented scarcity or unverifiable social proof instead of evidence?
- **Priority**: P1 | Cost: low, text only | Value: high, evidence A-B ([US Federal Trade Commission (FTC) dark-pattern report](https://search.ftc.gov/system/files/ftc_gov/pdf/P214800%20Dark%20Patterns%20Report%209.14.2022%20-%20FINAL.pdf): dark patterns doubled sign-ups for a dubious service)
- **Web**: optional (whether the scarcity is real)
- **Overlap**: none
- **Replaces**: SOCAS-CR-17 (commercial part), SOCAS-CR-16 (moral and identity framing part)

#### SOCAS-WR-07: Unsubstantiated Commercial Claim

- Quality, environmental or performance claim without a named certificate, test report or standard the reader can open
- **Applies to**: content with quality, environmental or performance claims about a product or service
- **Test**: Does each marketing claim name evidence the reader can check?
- **Priority**: P1 | Cost: medium, 1 web lookup of the named scheme | Value: high, evidence B ([European Commission](https://environment.ec.europa.eu/topics/circular-economy-topics/green-claims_en): 53% of green claims vague, misleading or unfounded; 40% without supporting evidence)
- **Web**: optional, 1 lookup
- **Overlap**: none
- **Replaces**: RC-W07

### 5.3 Currency, Structure and Precision

#### SOCAS-WR-08: Outdated Content

- Outdated facts next to current ones; latest cited source much older than the content date; named product versions behind the current version; references to abandoned tools or sources
- **Applies to**: content that names products, versions, prices, laws or sources with a date
- **Test**: Is any fact, version or source outdated relative to the content date?
- **Priority**: P2 | Cost: medium, 1 date or version lookup | Value: medium, evidence C ([reference rot](https://www.pewresearch.org/data-labs/2024/05/17/when-online-content-disappears/): 38% of 2013 webpages gone by 2023)
- **Web**: optional, 1 lookup
- **Overlap**: none
- **Replaces**: SOCAS-CR-12 (outdated information part), RC-W04

#### SOCAS-WR-09: Empty Structure

- Headings label topics instead of stating findings; main point buried at the end or missing; summaries describe what a section covers, not what it found; no stated purpose
- **Applies to**: documents that report or argue (articles, reports, INFO documents, slide decks, proposals); not reference-type documents (API reference, rule index, glossary), where topic headings are the correct form
- **Test**: Can the reader get the main point from the headings and the first paragraph alone?
- **Priority**: P1 | Cost: low, text only | Value: medium, evidence B ([assertion-evidence slides](https://www.ijee.ie/articles/Vol29-6/23_ijee2791ns.pdf): better comprehension and delayed recall, 110 students)
- **Web**: no
- **Overlap**: REF - fix by MECT-HS-01, APAPL-ST-01
- **Replaces**: SOCAS-CR-13

#### SOCAS-WR-10: Vague Word Where a Measure Belongs

- Unverifiable adjectives where the claim needs a number, unit, scope or condition: flexible, easy, sufficient, robust, fast, user-friendly, appropriate, "-ly" adverbs; vague claim terms: natural, sustainable, eco
- **Applies to**: claims about quality, performance, effort or requirements
- **Test**: Does a claim that needs a measure carry only a vague qualifier?
- **Priority**: P1 | Cost: low, text only | Value: medium, evidence B-C ([NASA](https://www.nasa.gov/reference/appendix-c-how-to-write-a-good-requirement/) and [IBM](https://www.ibm.com/docs/en/erqa?topic=assistant-guidelines-good-requirements) requirement lists; [EU study](https://op.europa.eu/en/publication-detail/-/publication/f7c4cb8b-f877-11ee-a251-01aa75ed71a1/language-en): 54 of 150 environmental claims unclear)
- **Web**: no
- **Overlap**: REF - fix by APAPL-PR-07; SOCAS adds the term list
- **Replaces**: SOCAS-CR-08 (generic phrasing part), RC-N02

#### SOCAS-WR-11: Requirement Quality in Normative Documents

- Required and optional not distinguishable; escape clauses ("where possible", "as appropriate", "etc.", "and/or", "but not limited to"); one statement holding several obligations; no actor; edge case undefined; no escalation or exception path in a process description; steps in an order that cannot run (a step needs the result of a later step)
- **Applies to**: normative documents: policies, SOPs, process descriptions, standards, rule files, guides, templates, workflows, `SKILL.md` files
- **Test**: Can the reader tell what is required, what is optional, who must act and what happens in the edge case, and can the steps run in the stated order?
- **Priority**: P1 | Cost: low, text only | Value: medium, evidence B-C (Internet Engineering Task Force key words [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119.html) and [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174.html), IBM, NASA, [Easy Approach to Requirements Syntax (EARS) case study](https://doi.org/10.1109/re.2009.9))
- **Web**: no
- **Overlap**: REF - obligation words fixed by MECT-VO-04, missing actor fixed by MECT-VO-01
- **Replaces**: SOCAS-CR-06 (non-code normative part), SOCAS-CR-04 (escalation path part), SOCAS-CR-14 (step order part), RC-N04, RC-N05

## 6. SOCAS_COMMUNICATION_RULES.md - Communication

Content types: chat, email, short memos, status messages, requests, orders, meeting notes, conversation entries, the written trace of calls (summary, confirmation, call notes), and prompts (`_PROMPTS_*`) and other one-time orders written for agents. Reusable procedures for agents (workflows, SOPs) use section 5. Spoken tone and read-back cannot be checked from text [ASSUMED].

APAPALAN CM rules prescribe the form of a message (APAPL-CM-02 and CM-03 in the DEFER list in 3.3; APAPL-CM-01 is the fix cited by SOCAS-CM-01). SOCAS-CM rules detect what those rules do not: the content is wrong, empty of substance or hostile even when the form is right. Evidence comes mostly from healthcare handoffs and lab experiments; no study of business email quality scoring was found [VERIFIED: research IN08].

Selected: 8 rules. Discarded or merged drafts CM-09 (into SOCAS-GN-01), CM-10, CM-11 (into SOCAS-CM-07), plus read-back and handoff formats: `_INFO_SOCAS_DISCARDED_RULE_CANDIDATES.md [SOCAS-IN02]`.

User focus questions (decision SOCASCONTEXT-DD-01) and the rules that answer them:
- Is it actionable? SOCAS-CM-01, SOCAS-CM-04
- Is it self-contained? SOCAS-CM-02
- Does it require much lookup or verification effort? SOCAS-CM-02 (lookups), SOCAS-CM-03 (verification)
- Does it contradict itself? SOCAS-GN-01 (message forms)
- Does it contain underspecified requests or actions? SOCAS-CM-04, SOCAS-CM-01
- Does it contain misleading or vague interpretations? SOCAS-GN-03 (ambiguous terms), SOCAS-GN-05 (assumption as fact), SOCAS-CM-05 (meaning depends on unstated tone)
- Does it contain manipulative or aggressive language? SOCAS-GN-07, SOCAS-CM-06, SOCAS-CM-07
- Is the tone appropriate? SOCAS-CM-05, SOCAS-CM-06; appropriateness that depends on relationship and culture has no rule (draft SOCAS-CM-10 discarded, SOCAS-IN02)
- Does it omit or replace relevant information? SOCAS-CM-08
- Does it invert priorities? SOCAS-CM-07

### 6.1 Actionability

#### SOCAS-CM-01: Who Does What by When Unclear

- The reader must guess the actor, the outcome or the time of a request or decision
- **Applies to**: messages with a request, decision or commitment, and documents that recommend actions or decisions (SOCAS-AP-03); not purely informational content
- **Test**: Can the reader say who must do what by when?
- **Priority**: P1 | Cost: low, text only | Value: high, evidence A-B ([plans stating when, where and how](https://kops.uni-konstanz.de/entities/publication/2e749bfb-8533-437c-8203-7e788c910c5f): d = 0.65 over 94 tests)
- **Web**: no
- **Overlap**: REF - fix by APAPL-CM-01, APAPL-CM-02, APAPL-ST-02
- **Replaces**: SOCAS-CR-05 (no owner or decision maker, in messages and in documents that recommend actions), RC-M01

#### SOCAS-CM-02: Lookups Needed to Act

- "See attachment", "as discussed", "per the thread", a bare link, or a reference to a previous message carries the information the reader needs
- **Applies to**: messages with a request or decision
- **Test**: Must the reader open another source to understand or act? Count the lookups
- **Priority**: P1 | Cost: low, text only | Value: medium, evidence B ([integrated vs separated sources](https://doi.org/10.1016/j.learninstruc.2006.10.001): d = 0.85 over 50 studies; transfer from instruction to messages by analogy)
- **Web**: no
- **Overlap**: REF - fix by APAPL-ST-03, APAPL-ST-04
- **Replaces**: SOCAS-CR-05 (scattered information), RC-M02

#### SOCAS-CM-03: Unbacked Basis for Action

- The reader must trust a claim before acting: figures, names, claimed approvals ("legal approved this"), claimed earlier decisions
- **Applies to**: messages that ask the reader to act
- **Test**: Does acting on the message require trusting a claim the message does not back?
- **Priority**: P2 | Cost: medium, judgment of what needs backing | Value: medium, evidence C
- **Web**: no (verification itself: `/fact-check`)
- **Overlap**: none
- **Replaces**: research focus question Q2 (verification effort)

#### SOCAS-CM-04: Underspecified or Conflicting Order

- The request leaves open a choice between valid but inconsistent results (which file, which version, which format, when done); two requirements in one order conflict. Core case: orders written for agents
- **Applies to**: one-time orders and work requests, especially prompts written for agents; reusable procedures (workflows, SOPs) use SOCAS-WR-11
- **Test**: Does the order leave valid but inconsistent results open, or do two of its requirements conflict?
- **Priority**: P1 | Cost: low, text only | Value: high, evidence B ([unstated requirements dropped agent accuracy 22.6% on average, up to 93.1%](https://aclanthology.org/2026.findings-acl.441/); Association for Computational Linguistics (ACL) Findings 2026)
- **Web**: no
- **Overlap**: REF - fix by APAPL-ST-04
- **Replaces**: RC-M03, RC-D09

### 6.2 Tone and Pressure

#### SOCAS-CM-05: Tone Depends on Unstated Intent

- Irony, sarcasm, humor or understatement in a text-only channel, with the intended tone not stated in words
- **Applies to**: all messages in text-only channels
- **Test**: Does the meaning depend on a tone the words do not state?
- **Priority**: P1 | Cost: low, text only | Value: high, evidence B ([email senders predicted 78% tone accuracy, readers reached 56%](https://doi.org/10.1037/0022-3514.89.6.925); 5 experiments)
- **Web**: no
- **Overlap**: none (MECT-WC-10 covers idioms, not irony)
- **Replaces**: RC-M04

#### SOCAS-CM-06: Rude or Hostile Language

- Insult, threat, contempt, profanity, identity attack. Judge the sentence, not the person. Expect false positives on quoted speech and negations
- **Applies to**: all messages
- **Test**: Does a quoted phrase insult, threaten or show contempt?
- **Priority**: P1 | Cost: low, text only | Value: high, evidence B ([mild rudeness lowered performance of 24 randomized medical teams](https://pubmed.ncbi.nlm.nih.gov/26260718/) via less information sharing)
- **Web**: no
- **Overlap**: none
- **Replaces**: RC-M05

#### SOCAS-CM-07: Pressure Without Reason or Inverted Priorities

- Deadline, escalation threat or urgency with no stated reason; deadline or small item emphasized while the larger consequence is absent or last; the main ask comes after background or secondary items. Concrete message form of SOCAS-GN-07
- **Applies to**: messages with a deadline, escalation or urgency word, or with a request
- **Test**: Is pressure applied without a stated reason, or does the order of the message hide the main ask or the larger consequence?
- **Priority**: P1 | Cost: low, text only | Value: high, evidence B ([spurious urgency: 31.3% vs 13.3% chose the worse task](https://academic.oup.com/jcr/article-abstract/45/3/673/4847790), 5 experiments; [reminding people of the payoffs at the moment of choice reduced the effect](https://hub.jhu.edu/2018/05/31/meeting-deadlines-time-management-behaviors/))
- **Web**: no (truth of the deadline: owner or web)
- **Overlap**: REF - ask-first order fixed by APAPL-ST-01
- **Replaces**: RC-M06, RC-M08, RC-M09, SOCAS-CM-11 draft (merged)

### 6.3 Completeness

#### SOCAS-CM-08: Omitted or Replaced Information

- What the reader needs to decide or act is missing (what, who, by when, impact, risks, what is unknown); a question answered with a different, easier answer
- **Applies to**: messages that ask for a decision, answer a question or hand over work
- **Test**: Is anything the reader needs to decide missing, or is the question answered with a different one?
- **Priority**: P2 | Cost: medium, element list per message type | Value: medium, evidence C ([I-PASS handoff elements](https://www.nejm.org/doi/full/10.1056/NEJMsa1405556) (Illness severity, Patient summary, Action list, Situation awareness, Synthesis by receiver); [US Centers for Disease Control and Prevention (CDC) Clear Communication Index](https://www.cdc.gov/ccindex/tool/description-examples-parta.html) item on what is not known)
- **Web**: no
- **Overlap**: none
- **Replaces**: RC-M07

## 7. SOCAS_CODING_RULES.md - Code and Code Specifications

Content types: source code, configuration, scripts, diffs and pull requests, repositories, dependencies, technical READMEs, code specifications (software SPEC, IMPL, TEST, API specifications; in IPPS all `_SPEC_*`, `_IMPL_*`, `_TEST_*` and `_TASKS_*` documents, including specifications of workflows and skills, because they specify executable agent behavior). User interfaces: no selected rule (draft SOCAS-CD-11 discarded until researched).

`MECT_CODING_RULES.md` owns naming, comments, error messages, logs and documentation wording (DEFER list in 3.3). SOCAS-CD rules cover other areas. Tool checks (scanner, complexity metric, registry lookup) beat an LLM pass; a SOCAS run calls or recommends them and flags only obvious cases without them [ASSUMED]. Not encoded: "defects cost 100 times more later" ([no delayed-issue effect in 171 projects](https://doi.org/10.1007/s10664-016-9469-x)) [VERIFIED] (SOCAS-IN01-SC-EMSE-MENZIES-DIE).

Selected: 9 rules. Discarded drafts CD-10 (net-negative adoption) and CD-11 (user interface signs), plus function length and comment ratio limits: `_INFO_SOCAS_DISCARDED_RULE_CANDIDATES.md [SOCAS-IN02]`.

### 7.1 Code and Repository

#### SOCAS-CD-01: Invented Dependency

- A package or import name does not exist in its registry, or exists without history
- **Applies to**: code, dependency manifests and documentation that name packages
- **Test**: Does every package or import exist in its registry with a history?
- **Priority**: P1 | Cost: medium, 1 registry lookup per name | Value: high, evidence B ([19.7% of 2.23 million packages suggested by 16 code models did not exist](https://www.usenix.org/system/files/usenixsecurity25-spracklen.pdf); USENIX Security 2025)
- **Web**: yes, registry lookup by tool; without a tool, unknown or unusual names first within the SOCAS-AP-09 budget
- **Overlap**: none
- **Replaces**: RC-D01

#### SOCAS-CD-02: Insecure Construction

- String-built SQL or shell commands, hard-coded secrets, unsafe deserialization, disabled certificate checks
- **Applies to**: source code, scripts, configuration
- **Test**: Does the code contain a construction known as insecure?
- **Priority**: P1 | Cost: low for obvious cases (scanner for full check) | Value: high, evidence B ([about 40% of 1,689 GitHub Copilot programs vulnerable](https://arxiv.org/html/2108.09293v3))
- **Web**: no
- **Overlap**: none
- **Replaces**: RC-D02

#### SOCAS-CD-03: Unresolved Debt Markers

- TODO, FIXME or hack markers without owner, date or ticket; a marker on the core function. One marker is not a defect
- **Applies to**: source code
- **Test**: Are there debt markers without owner or date, or on the core function?
- **Priority**: P2 | Cost: low, text search | Value: low, [markers are common](https://doi.org/10.1109/icsme.2014.31) (2.4% to 31% of files in 4 systems)
- **Web**: no
- **Overlap**: none (MECT-PR-04 covers comment wording only)
- **Replaces**: RC-D03

#### SOCAS-CD-04: Change Too Large to Review

- Diff over about 400 lines without split, or without stated purpose [ASSUMED threshold for other teams]
- **Applies to**: diffs and pull requests
- **Test**: Is the change too large to review in one pass, or without stated purpose?
- **Priority**: P1 | Cost: low, line count from diff | Value: medium, evidence C ([2,500 reviews: defect density dropped above 200 lines](https://static1.smartbear.co/support/media/resources/cc/book/code-review-cisco-case-study.pdf); vendor-run case study)
- **Web**: no
- **Overlap**: none
- **Replaces**: RC-D04

#### SOCAS-CD-05: Excess Complexity

- Deep nesting, long branching chains, indirection without benefit, over-engineered solution for a simple problem. Use a complexity tool for the metric
- **Applies to**: source code
- **Test**: Is there a simpler construction that does the same?
- **Priority**: P2 | Cost: medium, tool or judgment | Value: medium, evidence B ([Cognitive Complexity correlated 0.654 with comprehension time](https://dl.acm.org/doi/10.1145/3382494.3410636), 14 studies)
- **Web**: no
- **Overlap**: none
- **Replaces**: SOCAS-CR-11 (code part), RC-D05

#### SOCAS-CD-06: Stale or Unhealthy Dependency

- Archived or abandoned repository referenced as active; no maintenance activity; known vulnerabilities; declared end-of-life without successor; many open issues without maintainer response
- **Applies to**: code, READMEs or proposals that name dependencies a decision rests on
- **Test**: Is a decision-relevant dependency active, maintained and free of known vulnerabilities?
- **Priority**: P2 | Cost: medium, 1 lookup per decision-relevant dependency | Value: medium, evidence C ([Open Source Security Foundation (OpenSSF) Scorecard](https://github.com/ossf/scorecard/blob/main/README.md) checks; the tool states a low score is not a definitive risk)
- **Web**: yes
- **Overlap**: none
- **Replaces**: SOCAS-CR-12 (stale code and tools part), RC-D06

#### SOCAS-CD-07: Missing Tests, History or Setup

- No tests or tests disabled; no version history or a single commit; boilerplate README without setup instructions; dead code
- **Applies to**: repositories and code deliveries (bids, handovers); not code snippets
- **Test**: Are tests, history and setup instructions present?
- **Priority**: P1 | Cost: low, file listing | Value: medium, evidence C ([US government 18F guide for evaluating bids](https://guides.18f.gov/derisking-government-tech/resources/evaluate-bids/))
- **Web**: no
- **Overlap**: none
- **Replaces**: RC-D07

### 7.2 Code Specifications

#### SOCAS-CD-08: Behavior, Edge Cases or Acceptance Undefined

- Behavior, edge cases (empty input, timeout, concurrent access), error handling or acceptance check not stated; two requirements conflict; unstated assumptions
- **Applies to**: code specifications (section 7 content types)
- **Test**: Can the implementer tell the required behavior, the edge cases, the error handling and how acceptance is checked?
- **Priority**: P1 | Cost: low, text only | Value: high, evidence B ([unstated requirements dropped agent accuracy 22.6% on average](https://aclanthology.org/2026.findings-acl.441/); [NASA](https://www.nasa.gov/reference/appendix-c-how-to-write-a-good-requirement/) and [IBM](https://www.ibm.com/docs/en/erqa?topic=assistant-guidelines-good-requirements) requirement rules)
- **Web**: no
- **Overlap**: none
- **Replaces**: SOCAS-CR-06 (code specification part), RC-D08

#### SOCAS-CD-09: Unverifiable Requirement Wording

- Escape clauses; one requirement holding several obligations; adjectives without measure; goals without tolerance range; missing units; to be determined (TBD) values without owner and date; requirement without unique ID; requirement without rationale or parent ("why is it here?")
- **Applies to**: code specifications
- **Test**: Is each requirement one verifiable obligation with measure, unit and an owner for open values?
- **Priority**: P1 | Cost: low, text only | Value: medium, evidence B-C ([RFC 8174](https://www.rfc-editor.org/rfc/rfc8174.html), IBM, NASA, [EARS](https://doi.org/10.1109/re.2009.9))
- **Web**: no
- **Overlap**: REF - obligation words fixed by MECT-VO-04; IDs fixed by APAPL-PR-05
- **Replaces**: SOCAS-CR-06 (requirement wording part), RC-N04, RC-N05 (code specification part), research IN07 Field 1 (traceability, units, tolerances, TBD tracking)

## 8. Migration Map from SOCAS-CR-01 to SOCAS-CR-17

Old ID → new rule IDs. Old IDs are retired and not reused; the legacy SOCAS-AP-04 below is not the current SOCAS-AP-04. Sign-level check against the old `SOCAS_RULES.md` (2026-11-10): every old sign maps to a selected rule, a DEFER entry (section 3.3) or a SOCAS-IN02 entry.

Criteria:
- **SOCAS-CR-01** Inconsistencies → SOCAS-GN-01 (contradictions), SOCAS-GN-02 (naming and format)
- **SOCAS-CR-02** Ambiguous naming and wording → SOCAS-GN-03; missing glossary merged into SOCAS-GN-03 (SOCAS-IN02)
- **SOCAS-CR-03** Overlapping concerns → SOCAS-GN-08 (duplicate mechanisms, overlapping concepts, inconsistent split of responsibilities); repeated text and mixed list granularity deferred to APAPL-BR-03, MECT-LT-02
- **SOCAS-CR-04** Undisclosed contact information → SOCAS-WR-04 (reworded to responsible party and interest); no escalation path: SOCAS-WR-11
- **SOCAS-CR-05** Ineffective communication → SOCAS-CM-01 (also for documents that recommend actions, SOCAS-AP-03), SOCAS-CM-02; buried details in documents: SOCAS-WR-09; information scattered across documents: SOCAS-IN02
- **SOCAS-CR-06** Incomplete specification → SOCAS-CD-08, SOCAS-CD-09 (code specifications), SOCAS-WR-11 (non-code normative documents), SOCAS-GN-04 (conclusions without evidence)
- **SOCAS-CR-07** Confusing elements → SOCAS-GN-03 (creative names, hidden references), SOCAS-GN-14 (humor without information), SOCAS-GN-15 (irrelevant material); metaphors DEFER to MECT-WC-10 (draft SOCAS-GN-22 merged); excessive analogies: SOCAS-IN02
- **SOCAS-CR-08** Information vs noise imbalance → SOCAS-GN-14, SOCAS-WR-10 (generic phrasing)
- **SOCAS-CR-09** Lack of structure → SOCAS-GN-17
- **SOCAS-CR-10** Gaps in reasoning → SOCAS-GN-04, SOCAS-GN-05; new statistics rules SOCAS-GN-09 to GN-13
- **SOCAS-CR-11** Unnecessary complexity → SOCAS-GN-16 (text, designs and processes), SOCAS-CD-05 (code)
- **SOCAS-CR-12** Presentation sloppiness → SOCAS-GN-18 (typos, grammatical errors, internal references), SOCAS-GN-02 (formatting), SOCAS-WR-01 (external sources), SOCAS-WR-08 (outdated content), SOCAS-CD-06 (stale code and tools)
- **SOCAS-CR-13** Empty structure → SOCAS-WR-09
- **SOCAS-CR-14** Arbitrary sequencing → deferred (draft SOCAS-GN-21) to APAPL-ST-05, MECT-LT-02; steps that cannot run in the stated order: SOCAS-WR-11
- **SOCAS-CR-15** Net-negative adoption → discarded (draft SOCAS-CD-10); dependency health signs stay in SOCAS-CD-06
- **SOCAS-CR-16** Disguised commercial intent → SOCAS-WR-05; purchase framed as moral duty or identity: SOCAS-WR-06
- **SOCAS-CR-17** Weaponized persuasion → SOCAS-GN-07 (abstract), SOCAS-WR-06 (commercial), SOCAS-CM-07 (messages)

Application and reporting:
- **SOCAS-AP-01**, **AP-02**, **RP-01**, **RP-02** → same IDs, extended (section 4.4)
- **SOCAS-AP-03** Context-appropriate subset → SOCAS-AP-03 redefined as file selection; the old subsets Agent Output Review, Document Review, Source Evaluation and Organizational Assessment are replaced by the field files; the repository health signs of Source Evaluation moved to SOCAS-CD-06; ranking sources by SOCAS count: SOCAS-IN02
- **SOCAS-AP-04 (legacy)** UX-specific criteria → discarded (draft SOCAS-CD-11) until researched; legacy ID AP-04 retired (the current SOCAS-AP-04 is another rule)

New selected rules without old predecessor: SOCAS-GN-06, GN-09 to GN-13, WR-02, WR-03, WR-07, CM-03, CM-04, CM-05, CM-06, CM-08, CD-01 to CD-04, CD-07, AP-04 to AP-12.

Old rules without own successor (criterion SOCAS-CR-14 deferred; criterion SOCAS-CR-15 and legacy application rule SOCAS-AP-04 discarded) carry their reasoning in SOCAS-IN02 section 2.

## 9. Next Steps

1. DONE 2026-11-10 (user decisions OD-1 option 1, OD-2 option 1, verdict by violated count, ID scheme and discards confirmed, content-type mapping confirmed): open points were OD-1 overlap handling (this document assumes REF/DEFER as in section 3), OD-2 home of statistics and web source checks (this document assumes option 1, see Summary), verdict by violated count with an informational equal-weight mean vs 40/30/20/10 dimension weights (needs a dimension per rule, SOCAS-AP-02), new ID scheme `GN`/`WR`/`CM`/`CD`, content-type mapping (SOCAS-AP-03 and the start of sections 5-7), and confirm or reverse each discard in `_INFO_SOCAS_DISCARDED_RULE_CANDIDATES.md [SOCAS-IN02]`
2. DONE 2026-11-10 for the PromptSystem folder (consumers listed below updated, 0 grep hits; `docs/` and `specs/` references remain): write `SOCAS_RULES.md`, `SOCAS_WRITING_RULES.md`, `SOCAS_COMMUNICATION_RULES.md` (in `@skills:write-documents`) and `SOCAS_CODING_RULES.md` (in `@skills:coding-conventions`) from sections 4-7. Replace old IDs (`SOCAS-CR-*`, legacy `SOCAS-AP-04`) and subset names in all consumers, then confirm 0 grep hits:
   - Workflows: `/verify` (Agent Output Review subset), `/critique`, `/improve` and `/research` (Source Evaluation subset), `/fact-check` (triage signals SOCAS-CR-06, CR-08, CR-10, CR-12, CR-13)
   - Skill files: `INFO_RULES.md`, `SKILL.md` and `TEMPLATE_GUIDES.md`, `TEMPLATE_RULES.md`, `MINTO_GUIDES.md` (write-documents), `ID-REGISTRY_TEMPLATE.md` ("17 criteria")
   - `/research` and `/improve` rank sources by SOCAS count; SOCAS-AP-10 forbids ranking by score alone, so source ranking needs a new basis
3. Build the context-aware standalone SOCAS prompt (v6.2: 17 criteria in 4 weighted dimensions, 20 `/detect` signals) from this document (architecture decision pending). Constraints: v6.2 picks its verdict line by SOCAS score band, its firewall rule needs the Integrity dimension, its criteria carry BAD/GOOD examples, and it carries only 13 APAPALAN and MECT rules (for `/improve`); the other DEFER signs of section 3.3 and the REF fixes must be inlined as plain test questions
4. Research the re-entry conditions of discarded candidates with missing evidence (SOCAS-IN02 section 4): user interface signs, net-negative adoption, tone appropriateness
5. Calibrate priorities: run each field file twice on 5-10 real contents per field; demote rules with frequent false positives, promote rules that found decision-relevant problems

## 10. Sources

Claims were checked against search-result excerpts (abstract or page text) on 2026-11-10, not full texts. `[COMMUNITY]` = preprint or secondary summary.

**Application rules (AP):**
- `SOCAS-IN01-SC-ACL-CHKEVAL`: https://aclanthology.org/2025.emnlp-main.796/ - Binary checklist questions raised agreement across 12 judge models by 0.45 (AP-01) [VERIFIED]
- `SOCAS-IN01-SC-APA-DAWES`: https://doi.org/10.1037/0003-066x.34.7.571 - Equal-weight linear models are robust (AP-02) [VERIFIED]
- `SOCAS-IN01-SC-AFT-SIFT`: https://www.aft.org/ae/spring2025/caulfield_wineburg - SIFT; 30 seconds of context improved decisions (AP-03) [VERIFIED]
- `SOCAS-IN01-SC-COCH-ROB2`: https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-08 - RoB 2 signalling questions with "No information" answer (AP-04) [VERIFIED]
- `SOCAS-IN01-SC-STNFD-FOGGCRED`: https://credibility.stanford.edu/pdf/How_Do_People_Evaluate_a_Web_Site%27s_Credibility_v37.pdf - Design look in 46.1% of 2,684 credibility comments (AP-06, WR-04) [VERIFIED]
- `SOCAS-IN01-SC-OPENAI-CLSF`: https://openai.com/index/new-ai-classifier-for-indicating-ai-written-text/ - Classifier found 26% of AI text, withdrawn 2023-07-20 (AP-06) [VERIFIED]
- `SOCAS-IN01-SC-PMC-GPTDET`: https://pmc.ncbi.nlm.nih.gov/articles/PMC10382961/ - Detectors misclassified 61.3% of non-native essays (AP-06) [VERIFIED]
- `SOCAS-IN01-SC-ACM-LTRCOUNT`: https://dl.acm.org/doi/10.1145/3818606 - LLMs fail to count repeated tokens (AP-07) [VERIFIED]
- `SOCAS-IN01-SC-ARXIV-SELFPREF`: https://arxiv.org/abs/2404.13076 - LLM evaluators favor their own generations (AP-08) [VERIFIED]
- `SOCAS-IN01-SC-ARXIV-CITEDNV`: https://arxiv.org/html/2605.06635v1 - Citation accuracy 39-77%; accuracy falls with search depth (AP-09) [COMMUNITY]
- `SOCAS-IN01-SC-ARXIV-COINFLIP`: https://arxiv.org/html/2606.13685 - 13.6% verdict flips on identical reruns (AP-10) [COMMUNITY]
- `SOCAS-IN01-SC-ARXIV-VERDICT`: https://arxiv.org/html/2610.12083v1 - Scoring all criteria in one prompt preserved consistency (AP-11) [COMMUNITY]
- `SOCAS-IN01-SC-ARXIV-RUBPOS`: https://arxiv.org/html/2602.02219v2 - Order of criteria shifts rubric scores (AP-11) [COMMUNITY]

**General rules (GN):**
- `SOCAS-IN01-SC-SPRINGER-STATCHK`: https://link.springer.com/article/10.3758/s13428-015-0664-2 - Half of papers with at least one inconsistent p-value (GN-01) [VERIFIED]
- `SOCAS-IN01-SC-CLAIMDIG-GOODREQ`: https://claimdig.com/guides/good-requirements/ - Quality criteria for requirements, synthesis of ISO 29148 (GN-02) [COMMUNITY]
- `SOCAS-IN01-SC-IBM-RQA`: https://www.ibm.com/docs/en/erqa?topic=assistant-guidelines-good-requirements - Vague words, escape clauses, compound requirements (GN-03, WR-10, WR-11, CD-09) [VERIFIED]
- `SOCAS-IN01-SC-NASA-APPC`: https://www.nasa.gov/reference/appendix-c-how-to-write-a-good-requirement/ - Unverifiable terms list, TBD tracking (GN-03, WR-10, CD-08, CD-09) [VERIFIED]
- `SOCAS-IN01-SC-CSU-TOULMIN`: https://writing.colostate.edu/guides/guide.cfm?guideid=58 - Claim, grounds, warrant, qualifier, rebuttal (GN-04, GN-05) [VERIFIED]
- `SOCAS-IN01-SC-CALLBS-VID`: https://www.callingbullshit.org/videos.html - Too good to be true; multiple hypotheses (GN-05) [VERIFIED]
- `SOCAS-IN01-SC-WALTON-SCHEMES`: https://cgi.csc.liv.ac.uk/~floriana/CMNA/WaltonReed.pdf - Argument from expert opinion, six critical questions (GN-05) [VERIFIED]
- `SOCAS-IN01-SC-IEP-FALLACIES`: https://iep.utm.edu/fallacy/ - Fallacy label cannot replace examination of context (GN-06) [VERIFIED]
- `SOCAS-IN01-SC-SCIADV-INOCUL`: https://www.science.org/doi/10.1126/sciadv.abo6254 - Technique-based inoculation, 7 preregistered studies (GN-07, WR-06) [VERIFIED]
- `SOCAS-IN01-SC-ICSE-CLONES`: https://wwwbroy.in.tum.de/~juergens/publications/ICSE2009_RP_0110_juergens.pdf - Inconsistent changes in 52% of 1,427 clone groups, 107 confirmed faults (GN-08) [VERIFIED]
- `SOCAS-IN01-SC-PMC-GIGER02`: https://pmc.ncbi.nlm.nih.gov/articles/PMC200816/ - Natural frequencies vs conditional probabilities, 48 doctors (GN-09) [VERIFIED]
- `SOCAS-IN01-SC-THINKR-HUFF`: https://thinkr.org/newsletter/how-to-lie-with-statistics - Huff's five questions; self-selected samples (GN-10) [COMMUNITY]
- `SOCAS-IN01-SC-PMC-RTM`: https://pmc.ncbi.nlm.nih.gov/articles/PMC1125994/ - Regression to the mean read as treatment effect (GN-11) [VERIFIED]
- `SOCAS-IN01-SC-SAGE-GIGER07`: https://journals.sagepub.com/doi/full/10.1111/j.1539-6053.2008.00033.x - Higher survival rates do not imply longer life (GN-11) [VERIFIED]
- `SOCAS-IN01-SC-TANDF-ASAPVAL`: https://www.tandfonline.com/doi/full/10.1080/00031305.2016.1154108 - ASA principles on p-values (GN-12) [VERIFIED]
- `SOCAS-IN01-SC-HOEKSTRA-CI`: https://www.ejwagenmakers.com/inpress/HoekstraEtAlPBR.pdf - Researchers endorsed more than 3 of 6 false CI statements (GN-12) [VERIFIED]
- `SOCAS-IN01-SC-ACM-DECVIS`: https://dl.acm.org/doi/10.1145/2702123.2702608 - Deceptive chart techniques mislead readers (GN-13) [VERIFIED]
- `SOCAS-IN01-SC-ACM-DECTAC`: https://doi.org/10.1145/3380851.3416762 - Truncated axes and 3-D effects misled 329 participants regardless of training (GN-13) [VERIFIED]
- `SOCAS-IN01-SC-NNG-CONCISE`: https://www.nngroup.com/articles/concise-scannable-and-objective-how-to-write-for-the-web/ - Concise +58%, objective +27% measured usability (GN-14, GN-15) [VERIFIED]
- `SOCAS-IN01-SC-JDM-BSRECEPT`: https://journal.sjdm.org/15/15923a/jdm15923a.pdf - Pseudo-profound sentences rated 2.6 of 5 (GN-15) [VERIFIED]
- `SOCAS-IN01-SC-PMC-WEISBERG`: https://pmc.ncbi.nlm.nih.gov/articles/PMC2778755/ - Irrelevant neuroscience made bad explanations more satisfying (GN-15) [VERIFIED]
- `SOCAS-IN01-SC-WILEY-ERUDITE`: https://onlinelibrary.wiley.com/doi/10.1002/acp.1178 - Needlessly long words lowered judged author intelligence (GN-16) [VERIFIED]
- `SOCAS-IN01-SC-FRONT-WRITING`: https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2021.714321/full - Accessible abstracts raised understanding 47.9% to 57.9% (GN-16) [VERIFIED]
- `SOCAS-IN01-SC-ACM-APIDOC`: https://doi.org/10.1145/3380851.3416759 - Guideline-optimized API docs: accuracy 86.35% vs 74.24% (GN-17) [VERIFIED]

**Writing rules (WR):**
- `SOCAS-IN01-SC-PMC-FABCHAT`: https://pmc.ncbi.nlm.nih.gov/articles/PMC10484980/ - ChatGPT-3.5 fabricated 55%, GPT-4 18% of citations (WR-01) [VERIFIED]
- `SOCAS-IN01-SC-PMC-MHCITE`: https://pmc.ncbi.nlm.nih.gov/articles/PMC12658395/ - 64% of fabricated citations with DOI had a valid DOI to an unrelated article (WR-01) [VERIFIED]
- `SOCAS-IN01-SC-CEUR-CHECKWORTHY`: https://ceur-ws.org/Vol-3677/paper4.pdf - Check-worthy sentences contain more numbers and named entities (WR-02) [VERIFIED]
- `SOCAS-IN01-SC-FLINDERS-AACODS`: https://fac.flinders.edu.au/dspace/api/core/bitstreams/e94a96eb-0334-4300-8880-c836d4d9a676/content - AACODS: missing date is a strong concern (WR-03) [VERIFIED]
- `SOCAS-IN01-SC-SAGE-LATREAD`: https://journals.sagepub.com/doi/10.1177/016146811912101102 - Fact-checkers read laterally and judged sources better (WR-04, AP-12) [VERIFIED]
- `SOCAS-IN01-SC-COCH-SPONSOR`: https://www.cochrane.org/evidence/MR000033_industry-sponsorship-and-research-outcome - Sponsored studies: favorable conclusions RR 1.34 (WR-05) [VERIFIED]
- `SOCAS-IN01-SC-FTC-DARKPAT`: https://search.ftc.gov/system/files/ftc_gov/pdf/P214800%20Dark%20Patterns%20Report%209.14.2022%20-%20FINAL.pdf - Dark-pattern taxonomy: social proof, scarcity, urgency, obstruction (WR-06) [VERIFIED]
- `SOCAS-IN01-SC-EC-GREEN`: https://environment.ec.europa.eu/topics/circular-economy-topics/green-claims_en - 53% of green claims vague, misleading or unfounded (WR-07) [VERIFIED]
- `SOCAS-IN01-SC-EUOP-ENVCLAIMS`: https://op.europa.eu/en/publication-detail/-/publication/f7c4cb8b-f877-11ee-a251-01aa75ed71a1/language-en - 54 of 150 claims unclear (WR-07, WR-10) [VERIFIED]
- `SOCAS-IN01-SC-PEW-LINKROT`: https://www.pewresearch.org/data-labs/2024/05/17/when-online-content-disappears/ - 38% of 2013 webpages gone by 2023 (WR-08) [VERIFIED]
- `SOCAS-IN01-SC-IJEE-ASSERTEV`: https://www.ijee.ie/articles/Vol29-6/23_ijee2791ns.pdf - Assertion-evidence slides: better comprehension, 110 students (WR-09) [VERIFIED]
- `SOCAS-IN01-SC-RFC-2119`: https://www.rfc-editor.org/rfc/rfc2119.html - Key words MUST, SHOULD, MAY (WR-11) [VERIFIED]
- `SOCAS-IN01-SC-RFC-8174`: https://www.rfc-editor.org/rfc/rfc8174.html - Only UPPERCASE key words carry defined meaning (WR-11, CD-09) [VERIFIED]
- `SOCAS-IN01-SC-IEEE-EARS`: https://doi.org/10.1109/re.2009.9 - EARS templates address 8 common requirement problems (WR-11, CD-09) [VERIFIED]

**Communication rules (CM):**
- `SOCAS-IN01-SC-KOPS-IMPLINT`: https://kops.uni-konstanz.de/entities/publication/2e749bfb-8533-437c-8203-7e788c910c5f - Implementation intentions d = 0.65 over 94 tests (CM-01) [VERIFIED]
- `SOCAS-IN01-SC-LI-GINNS`: https://doi.org/10.1016/j.learninstruc.2006.10.001 - Integrated sources d = 0.85 over 50 studies (CM-02) [VERIFIED]
- `SOCAS-IN01-SC-ACL-UNDERSPEC`: https://aclanthology.org/2026.findings-acl.441/ - Unstated requirements dropped accuracy 22.6% on average (CM-04, CD-08) [VERIFIED]
- `SOCAS-IN01-SC-QHC-HUMANFACTOR`: https://doi.org/10.1136/qhc.13.suppl_1.i85 - Communication failure root cause in over 70% of 2,455 sentinel events (GN-01 message forms) [VERIFIED]
- `SOCAS-IN01-SC-JPSP-KRUGER`: https://doi.org/10.1037/0022-3514.89.6.925 - Email tone: 78% predicted vs 56% actual accuracy (CM-05) [VERIFIED]
- `SOCAS-IN01-SC-PUBMED-RUDENESS`: https://pubmed.ncbi.nlm.nih.gov/26260718/ - Rudeness lowered performance of 24 randomized teams (CM-06) [VERIFIED]
- `SOCAS-IN01-SC-OUP-MEREURG`: https://academic.oup.com/jcr/article-abstract/45/3/673/4847790 - Mere urgency effect, 5 experiments (CM-07) [VERIFIED]
- `SOCAS-IN01-SC-JHU-MEREURG`: https://hub.jhu.edu/2018/05/31/meeting-deadlines-time-management-behaviors/ - Reminding people of payoffs at the moment of choice reduced the effect (CM-07) [VERIFIED]
- `SOCAS-IN01-SC-NEJM-IPASS`: https://www.nejm.org/doi/full/10.1056/NEJMsa1405556 - I-PASS handoff bundle: preventable adverse events -30% (CM-08) [VERIFIED]
- `SOCAS-IN01-SC-CDC-CCI`: https://www.cdc.gov/ccindex/tool/description-examples-parta.html - What is known and not known (CM-08) [VERIFIED]

**Coding rules (CD):**
- `SOCAS-IN01-SC-USENIX-SPRACKLEN`: https://www.usenix.org/system/files/usenixsecurity25-spracklen.pdf - 19.7% of 2.23 million suggested packages hallucinated (CD-01) [VERIFIED]
- `SOCAS-IN01-SC-ARXIV-COPILOTSEC`: https://arxiv.org/html/2108.09293v3 - About 40% of 1,689 Copilot programs vulnerable (CD-02) [VERIFIED]
- `SOCAS-IN01-SC-ICSME-SATD`: https://doi.org/10.1109/icsme.2014.31 - Self-admitted technical debt in 2.4% to 31% of files (CD-03) [VERIFIED]
- `SOCAS-IN01-SC-SMARTBEAR-CISCO`: https://static1.smartbear.co/support/media/resources/cc/book/code-review-cisco-case-study.pdf - 2,500 reviews: defect density drops above 200 lines (CD-04) [VERIFIED]
- `SOCAS-IN01-SC-ESEM-COGCOMPLEX`: https://dl.acm.org/doi/10.1145/3382494.3410636 - Cognitive Complexity correlates 0.654 with comprehension time (CD-05) [VERIFIED]
- `SOCAS-IN01-SC-OSSF-SCORECARD`: https://github.com/ossf/scorecard/blob/main/README.md - Automated repository health checks (CD-06) [VERIFIED]
- `SOCAS-IN01-SC-18F-BIDS`: https://guides.18f.gov/derisking-government-tech/resources/evaluate-bids/ - Warning signs: no tests, no history, boilerplate README (CD-07) [VERIFIED]
- `SOCAS-IN01-SC-EMSE-MENZIES-DIE`: https://doi.org/10.1007/s10664-016-9469-x - No delayed-issue effect in 171 projects (section 7 exclusion) [VERIFIED]

## 11. Document History

**[2026-11-10 18:23]**
- Changed: IDs renumbered per category in heading order (selected rules here first, discarded entries continue in SOCAS-IN02); entries below use the previous numbering, for example the rule now numbered SOCAS-GN-08 appears below as SOCAS-GN-17
- Changed: ID policy (SOCASCONTEXT-DD-10): numbers are stable from this renumbering on; the old SOCAS-AP-04 (user interface criteria) is a legacy ID

**[2026-11-10 15:27]**
- Added: SOCAS-GN-17 re-entered (design part of old SOCAS-CR-03: duplicate mechanisms, new solution for a solved problem); source ICSE-CLONES
- Changed: Signs restored from the old `SOCAS_RULES.md` after a sign-level check: over-engineered designs (SOCAS-GN-19), grammatical errors (SOCAS-GN-22), moral or identity framing of a purchase (SOCAS-WR-07), escalation path and executable step order (SOCAS-WR-12), owner and decision maker in documents that recommend actions (SOCAS-CM-01 via SOCAS-AP-03); counts 46 sign rules (34 P1), REF 16, NONE 30
- Fixed: Next Steps 3 (v6.2 inlines 13 APAPALAN and MECT rules; verdict by score band and Integrity firewall are constraints); section 8 maps every old sign

**[2026-11-10 15:15]**
- Added: IPPS document types in the content types of sections 5-7; mixed-content verdict, WR-01 for cited sources in all fields (SOCAS-AP-03); focus-question trace in section 6; SKIP guardrail (SOCAS-AP-05) and `N of T` summary (SOCAS-RP-02); passage-count anchors (SOCAS-AP-02) and severity mapping (SOCAS-RP-01) from standalone prompt v6.2; full consumer list in Next Steps 2
- Changed: General text rules GN-02, GN-03, GN-15, GN-21, GN-22 return `SKIP` on code (section 4); SOCAS-CM-08 takes the ask-first sign as REF to APAPL-ST-01 (REF 16, NONE 29); SOCAS-WR-06 test passes openly commercial content; verdict from violated count, mean informational; value of GN-03, WR-12, CD-10 set to medium per section 2.1 and ranking 2.3 reordered; evidence grades of AP-03, AP-13, WR-05 corrected
- Fixed: DEFER list 3.3 (APAPL-CM-01 owned by SOCAS-CM-01, humor not covered by MECT-WC-10, actor in requirements); section 8 subset names and status words (deferred vs discarded); SOCAS-AP-05 vs section 4 intro; web budget for registry lookups (SOCAS-AP-10, CD-01)

**[2026-11-10 15:05]**
- Added: **Applies to** condition on all 45 selected sign rules; rule format 2.2, SOCAS-AP-05 and 2.3 use `SKIP` for content outside the condition
- Added: SOCAS-AP-03 sends direct commercial messages (sales email, offer by chat) also through SOCAS-WR-06 to WR-08
- Added: Inline source links at first mention in sections 4-7 (INFO-SC-05); sources CLAIMDIG-GOODREQ, ACM-DECTAC, RFC-2119, JHU-MEREURG
- Changed: Acronyms written out at first use (APAPALAN, MECT, LLM, SIFT, RoB 2, FTC, RFC, EARS, DOI, SOP, TBD, CDC, OpenSSF and others); idioms replaced by explicit wording; SOCAS-GN-16 renamed to "Impressive Form Without Substance"
- Fixed: Rule format scope (2.2), DEFER count wording (3.4), summary reference to SOCAS-IN02, AP-13 wording

**[2026-11-10 14:45]**
- Added: Section 2.3 ranked selection per field, section 2.4 selection and discard criteria, SOCAS-AP-12 (run order, R8), SOCAS-AP-13 (presence tests, R2)
- Changed: Merged drafts GN-05 into GN-06, GN-20 into GN-03, CM-05 into GN-01, WR-03 into WR-01, CM-11 into CM-08; extended WR-06 and CD-10 with research IN07 signs; source count corrected from 196 to 152
- Moved: Discarded drafts GN-05, GN-14, GN-17, GN-18, GN-20, WR-03, CM-05, CM-09, CM-11, CD-07, CD-11 to `_INFO_SOCAS_DISCARDED_RULE_CANDIDATES.md [SOCAS-IN02]`

**[2026-11-10 14:30]**
- Changed: Rewritten for the 4-file split; all rules listed with priority, target file and overlap handling
- Added: General rules for statistics, fallacies, manipulation and superficial signs; communication and coding rules; application rules AP-05 to AP-11
- Removed: SOCAS-CR-01 to CR-17 (retired, see section 8); SOCAS-AP-04 (moved to SOCAS-CD-11)

**[2026-03-06 00:00]**
- Initial document created with 15 criteria
