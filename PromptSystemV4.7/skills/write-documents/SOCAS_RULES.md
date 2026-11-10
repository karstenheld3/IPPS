# SOCAS General Rules

Signs of Confusion and Sloppiness (SOCAS) is a quick screen of simple yes/no rules for signs that content was produced by someone confused or sloppy. It flags signs; it never proves a claim true or false and never judges the author. Origin: `_INFO_SOCAS_SIGNS_OF_CONFUSION_AND_SLOPPINESS.md [SOCAS-IN01]` (Karsten Held, 2026). Discarded, merged and deferred candidates with reasoning: `_INFO_SOCAS_DISCARDED_RULE_CANDIDATES.md [SOCAS-IN02]`.

Use during `/verify`, `/critique`, `/improve`, `/research` and `/fact-check`.

**Out of scope (separate commands)**:
- Truth verdicts and independent evidence search: `/fact-check`
- Logic and risk review in depth: `/critique`
- Writing the fix: APAPALAN and MECT rules, applied by `/improve`
- AI-authorship detection: no rule exists; detectors are unreliable ([OpenAI classifier](https://openai.com/index/new-ai-classifier-for-indicating-ai-written-text/) withdrawn 2023-07-20; [61.3% false positives on non-native essays](https://pmc.ncbi.nlm.nih.gov/articles/PMC10382961/))

## SOCAS Files

Every rule lives in exactly one file. A run loads this file plus one field file chosen by content type (SOCAS-AP-03):
- `SOCAS_RULES.md` (this file, `write-documents`): general rules for logic, statistics, fallacies, manipulation and superficial signs; application and reporting rules for every run
- `SOCAS_WRITING_RULES.md` (`write-documents`): publications, reports, websites, marketing, non-code normative documents
- `SOCAS_COMMUNICATION_RULES.md` (`write-documents`): chat, email, orders, requests, written traces of calls, prompts
- `SOCAS_CODING_RULES.md` (`coding-conventions`): code, repositories, dependencies, code specifications

SOCAS detects signs in any content, including content written by others. APAPALAN (`APAPALAN_RULES.md`) and MECT (`MECT_WRITING_RULES.md`, `MECT_CODING_RULES.md`) prescribe how to write. Where such a rule covers a sign, the SOCAS rule keeps only its test question and cites the rule ID as the fix (`Overlap: REF`). SOCAS copies no BAD/GOOD example from them.

```
SOCAS run (one holistic pass, fixed rank order, SOCAS-AP-11)
├─> 1) Context first (SOCAS-AP-03): type, audience, purpose, stage
├─> 2) SOCAS_RULES.md           general rules (always)
├─> 3) One field file by content type:
│      ├─> SOCAS_WRITING_RULES.md
│      ├─> SOCAS_COMMUNICATION_RULES.md
│      └─> SOCAS_CODING_RULES.md
├─> 4) Web checks (max 5 sources, SOCAS-AP-09) or "web checks: not run"
└─> 5) Score and report (SOCAS-AP-02, SOCAS-RP-01, RP-02)
```

## Rule Index

General (GN) - this file
- SOCAS-GN-01: Contradictions and Impossible Numbers
- SOCAS-GN-02: Inconsistent Naming and Format
- SOCAS-GN-03: Undefined or Ambiguous Key Terms
- SOCAS-GN-04: Unsupported Conclusion
- SOCAS-GN-05: Assumption as Fact, Unqualified Claim, No Alternatives
- SOCAS-GN-06: Fallacy with Quote
- SOCAS-GN-07: Manipulation Technique
- SOCAS-GN-08: Overlapping Concerns and Duplicate Mechanisms
- SOCAS-GN-09: Numbers Without Base
- SOCAS-GN-10: Biased Counting
- SOCAS-GN-11: Causal Claim Beyond Design
- SOCAS-GN-12: Significance and Testing Misread
- SOCAS-GN-13: Misleading Chart
- SOCAS-GN-14: Noise and Filler
- SOCAS-GN-15: Impressive Form Without Substance
- SOCAS-GN-16: Unnecessary Complexity
- SOCAS-GN-17: Lack of Structure
- SOCAS-GN-18: Presentation Sloppiness

Application (AP) - every run
- SOCAS-AP-01: Quote and Rule ID per Finding
- SOCAS-AP-02: Scoring and Rework Threshold
- SOCAS-AP-03: Context First and File Selection
- SOCAS-AP-04: SKIP vs NO INFORMATION
- SOCAS-AP-05: One Passage, One Finding
- SOCAS-AP-06: Scoring Guard
- SOCAS-AP-07: Tolerant Thresholds
- SOCAS-AP-08: Self-Evaluation Flag
- SOCAS-AP-09: Web Budget
- SOCAS-AP-10: Run-to-Run Noise
- SOCAS-AP-11: Run Order
- SOCAS-AP-12: Presence Tests Do Not Violate Alone

Reporting (RP) - every run
- SOCAS-RP-01: Finding Format
- SOCAS-RP-02: Summary Format

Rule IDs are continuous per category at release. Discarded and deferred candidates continue the numbering in their own list (see the header of this file). Once released, a rule ID is stable: it is never renumbered or reused for another sign.

## Table of Contents

- [Priority and Rule Format](#priority-and-rule-format)
- [Rank Order](#rank-order)
- [General Rules](#general-rules)
- [Application Rules](#application-rules)
- [Reporting Rules](#reporting-rules)

## Priority and Rule Format

Priority = cost / benefit of one rule. Cost (effort for the agent per run):
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
- **P3**: high cost + medium or low value, or medium cost + low value. Runs only on explicit request (no selected rule has this priority)

Evidence grades: A = several independent studies or large audits, B = one strong study or official analysis, C = standards body or expert consensus, D = opinion only, `[ASSUMED]` = no source found. Priorities are agent judgment from evidence grades, not measured. No study validates any SOCAS-style score against outcomes.

Every sign rule has:
- Signs: what to look for
- **Applies to**: content condition; content outside it gets `SKIP` (SOCAS-AP-04)
- **Test**: one yes/no question answered for a quoted passage
- **Priority**: `P[N] | Cost: [level], [why] | Value: [level], [evidence]`
- **Web**: `no`, or the lookup it needs
- **Overlap**: `none`, or the APAPALAN or MECT rule IDs that prescribe the fix (`REF`)

ID scheme: `SOCAS-[CAT]-[NN]`. Categories: `GN` general, `WR` writing, `CM` communication, `CD` coding, `AP` application, `RP` reporting. `SOCAS-CM-*` (communication signs) is a different rule set from `APAPL-CM-*` (APAPALAN communication production rules).

## Rank Order

A run executes rules in this fixed order: general file first, then the field file; within each file P1 before P2, then by value (high first), cost (low first), evidence grade, ID. A time-limited run executes the P1 rules of this file and of one field file (SOCAS-AP-11). Rules whose **Applies to** condition the content does not meet return `SKIP`.

General rules:
- P1: SOCAS-GN-01, GN-07, GN-09, GN-11, GN-14, GN-08, GN-16, GN-17, GN-03, GN-02, GN-04, GN-05, GN-10
- P2: SOCAS-GN-13, GN-12, GN-15, GN-06, GN-18

Application and reporting rules (every run, always active):
- P1: SOCAS-AP-01, AP-02, AP-03, AP-04 to AP-09, AP-11, AP-12, RP-01, RP-02
- P2: SOCAS-AP-10 (decisions only)

## General Rules

Run on every content type. These rules hold the abstract form of signs; field files hold the concrete forms. A rule whose **Applies to** condition the content does not meet returns `SKIP`; a rule whose condition is met but that has too little to test returns `NO INFORMATION` (SOCAS-AP-04). Neither is a score.

On code (source code, scripts, configuration, diffs), SOCAS-GN-02, GN-03, GN-14, GN-16, GN-17 and GN-18 return `SKIP`: naming, comments, error and log messages in code belong to `MECT_CODING_RULES.md`, complexity to SOCAS-CD-05. Technical READMEs and code specifications are text and run all general rules.

### Consistency and Reasoning

#### SOCAS-GN-01: Contradictions and Impossible Numbers

- Two statements, figures, dates, owners or scopes contradict each other
- Message forms: two deadlines, two owners or two scopes in one message; "urgent" and "no rush" together
- Numbers that cannot be true: parts do not sum to the total, percentages that should sum to 100 do not, a mean impossible for the stated sample size, a date before the event it describes
- **Applies to**: all content
- **Test**: Do two passages contradict each other, or is a number arithmetically impossible?
- **Priority**: P1 | Cost: low, text only (arithmetic by tool when available) | Value: high, evidence A ([statcheck](https://link.springer.com/article/10.3758/s13428-015-0664-2): half of psychology papers had an inconsistent p-value)
- **Web**: no
- **Overlap**: none

#### SOCAS-GN-02: Inconsistent Naming and Format

- One concept with several names, one name for several concepts, format changes without reason
- **Applies to**: all text; not code (see above)
- **Test**: Is one thing named, numbered or formatted in two ways?
- **Priority**: P1 | Cost: low, text only | Value: medium, evidence C (requirement consistency, [ISO 29148 summary](https://claimdig.com/guides/good-requirements/))
- **Web**: no
- **Overlap**: REF - fix by APAPL-NM-01, APAPL-PR-09, MECT-WC-05

#### SOCAS-GN-03: Undefined or Ambiguous Key Terms

- Key term undefined for the intended reader; a word with several readings; a dangerous meta-word without qualifier; a creative name or hidden reference (easter egg) the reader must decode
- **Applies to**: all text; not code (see above)
- **Test**: Would the intended reader understand every key term the first time it appears?
- **Priority**: P1 | Cost: low, text only | Value: medium, evidence B-C ([IBM](https://www.ibm.com/docs/en/erqa?topic=assistant-guidelines-good-requirements) and [NASA](https://www.nasa.gov/reference/appendix-c-how-to-write-a-good-requirement/) requirement guidelines; [European Union (EU) claims study](https://op.europa.eu/en/publication-detail/-/publication/f7c4cb8b-f877-11ee-a251-01aa75ed71a1/language-en): 54 of 150 claims unclear)
- **Web**: no
- **Overlap**: REF - fix by APAPL-PR-12, APAPL-NM-02, APAPL-NM-03, MECT-WC-01, MECT-WC-09. Abbreviations: DEFER to APAPL-PR-06. Metaphors, idioms: DEFER to MECT-WC-10

#### SOCAS-GN-04: Unsupported Conclusion

- A conclusion does not follow from evidence stated in the content; missing steps; claim without grounds or without a link (warrant) between grounds and claim
- **Applies to**: content that draws conclusions or makes recommendations
- **Test**: Does each conclusion follow from evidence stated in the content, with the steps in between?
- **Priority**: P1 | Cost: low, text only | Value: medium, evidence C ([Toulmin method](https://writing.colostate.edu/guides/guide.cfm?guideid=58): claim, grounds, warrant)
- **Web**: no
- **Overlap**: none

#### SOCAS-GN-05: Assumption as Fact, Unqualified Claim, No Alternatives

- Assumption presented as fact; universal or causal claim ("proves", "always", "guarantees") without stated limits or conditions; one explanation only for a surprising result; no alternatives or trade-offs; unjustified selection ("three reasons" - why these three?)
- Appeal to an expert that fails one of the six critical questions (expertise, field, exact assertion, trustworthiness, agreement with other experts, backing evidence)
- **Applies to**: content that makes claims, choices or recommendations
- **Test**: Is an assumption or strong claim stated without limits, or is a choice, explanation or expert opinion given without the alternatives or evidence considered?
- **Priority**: P1 | Cost: low, text only | Value: medium, evidence C ([Calling Bullshit course](https://www.callingbullshit.org/videos.html): generate several hypotheses; [Walton critical questions](https://cgi.csc.liv.ac.uk/~floriana/CMNA/WaltonReed.pdf))
- **Web**: no (expert credentials: optional 1 lookup)
- **Overlap**: none

#### SOCAS-GN-06: Fallacy with Quote

- A passage matches one of 7 fallacy families: strawman, begging the question, equivocation, cherry-picking, appeal to popularity, suppressed evidence, post hoc. Personal attack, false dichotomy and appeal to emotion belong to SOCAS-GN-07
- Finding needs quote, family name, one sentence of reasoning, and a check that context does not make the argument sound. No label without a quote
- **Applies to**: content that argues for a position
- **Test**: Does a quoted passage match a fallacy family, and does the context fail to make the argument sound?
- **Priority**: P2 | Cost: medium, context check against false positives | Value: medium, evidence C ([Internet Encyclopedia of Philosophy](https://iep.utm.edu/fallacy/): a fallacy label cannot replace examination of the context)
- **Web**: no
- **Overlap**: none

#### SOCAS-GN-07: Manipulation Technique

- Emotionally manipulative language, incoherent arguments, false dichotomy, scapegoating, ad hominem, fake experts, false balance
- Abstract form; concrete commercial forms in SOCAS-WR-06, message forms in SOCAS-CM-07
- **Applies to**: content that tries to persuade or to change the reader's view
- **Test**: Does the text use a named manipulation technique instead of evidence?
- **Priority**: P1 | Cost: low, text only | Value: high, evidence A ([7 preregistered studies](https://www.science.org/doi/10.1126/sciadv.abo6254), n = 6464 + 22,632: technique recognition is teachable)
- **Web**: no
- **Overlap**: none

#### SOCAS-GN-08: Overlapping Concerns and Duplicate Mechanisms

- Two parts of a design, process, rule set or codebase do the same job in different ways; a new mechanism for a problem the content already solves elsewhere; concepts that overlap without a stated boundary; responsibilities split inconsistently between parts; a duplicated mechanism or code block with slight variations
- **Applies to**: content that describes a design, system, process, rule set or code (specifications, architecture and process documents, rule files, workflows, source code); not narrative or persuasive text
- **Test**: Do two parts do the same job differently, or does the content add a mechanism for a problem it already solves elsewhere?
- **Priority**: P1 | Cost: low, cross-passage comparison as in SOCAS-GN-01 | Value: medium, evidence B with narrow scope ([inconsistent changes to code clones](https://wwwbroy.in.tum.de/~juergens/publications/ICSE2009_RP_0110_juergens.pdf): 52% of 1,427 clone groups were changed inconsistently, every second unintentional inconsistency was a fault, 107 confirmed faults in 5 systems); transfer to non-code designs [ASSUMED]
- **Web**: no
- **Overlap**: none (APAPL-BR-03 and MECT-LT-02 cover repeated text and list grouping, not duplicate mechanisms; the text part stays with those rules)

### Numbers and Statistics

Each rule applies only to content with figures, rates, studies or charts (see **Applies to**); otherwise `SKIP`. Training does not protect: researchers endorsed on average more than 3 of 6 false statements about confidence intervals ([Hoekstra et al. 2014](https://www.ejwagenmakers.com/inpress/HoekstraEtAlPBR.pdf)). Do not raise a score for statistical vocabulary or credentials.

#### SOCAS-GN-09: Numbers Without Base

- Percentage, ratio or "x times" without raw numbers or base; relative risk without absolute risk; test accuracy without prevalence; sample size missing or small for a strong claim; "average" without mean or median
- **Applies to**: content with percentages, ratios, averages or study results
- **Test**: Does each percentage, ratio or average come with its raw numbers, base and sample size?
- **Priority**: P1 | Cost: low, text only | Value: high, evidence A-B ([natural frequencies](https://pmc.ncbi.nlm.nih.gov/articles/PMC200816/): most of 48 doctors answered correctly vs about 8% with conditional probabilities)
- **Web**: no
- **Overlap**: none

#### SOCAS-GN-10: Biased Counting

- Self-selected or opt-in sample; response rate missing; only survivors or winners counted; groups that differed before the treatment compared as if randomized
- **Applies to**: content that reports surveys, samples, case collections or success stories
- **Test**: Does the content state who was counted and who is missing?
- **Priority**: P1 | Cost: low, text only | Value: medium, evidence C (course material, [Huff summary](https://thinkr.org/newsletter/how-to-lie-with-statistics))
- **Web**: no
- **Overlap**: none

#### SOCAS-GN-11: Causal Claim Beyond Design

- Causal verbs (causes, drives, leads to) on observational data; before-and-after read as effect; improvement of an extreme group read as treatment effect (regression to the mean); pooled totals hiding opposite subgroup trends (Simpson's paradox); the conclusion concerns a different quantity than the one measured (survival rate read as life gained)
- **Applies to**: content that states causes or effects from data or experience
- **Test**: Does the causal wording match the design, and does the conclusion concern the measured quantity?
- **Priority**: P1 | Cost: low, text only | Value: high, evidence B ([BMJ on regression to the mean](https://pmc.ncbi.nlm.nih.gov/articles/PMC1125994/); [Gigerenzer on survival rates](https://journals.sagepub.com/doi/full/10.1111/j.1539-6053.2008.00033.x))
- **Web**: no
- **Overlap**: none

#### SOCAS-GN-12: Significance and Testing Misread

- "Significant" used as "important"; no effect size or interval; "no significant difference, so no effect"; confidence interval read as probability; many outcomes measured, one reported; hypothesis formed after seeing the data
- **Applies to**: content that reports statistical tests, significance or confidence intervals
- **Test**: Is effect size or interval given, and is it stated how many things were tested?
- **Priority**: P2 | Cost: medium, needs statistics judgment | Value: medium, evidence B ([American Statistical Association (ASA) statement on p-values](https://www.tandfonline.com/doi/full/10.1080/00031305.2016.1154108)) with narrow scope (research content only)
- **Web**: no
- **Overlap**: none

#### SOCAS-GN-13: Misleading Chart

- Bar axis not starting at zero; dual axes; bubbles sized by diameter; inverted axis; no axis label or unit
- **Applies to**: content with charts or graphs
- **Test**: Are axes, scales and sizes honest and labeled?
- **Priority**: P2 | Cost: high, needs visual inspection | Value: high, evidence B ([ACM CHI 2015 conference study](https://dl.acm.org/doi/10.1145/2702123.2702608); [n = 329 study](https://doi.org/10.1145/3380851.3416762): misreading regardless of visualization training)
- **Web**: no
- **Overlap**: none

### Signal, Noise and Form

#### SOCAS-GN-14: Noise and Filler

- Filler and hedging; obvious things explained at length while complex things stay unexplained; the same point restated in different words; jokes or humor that carry no information
- **Applies to**: all text; not code (see above)
- **Test**: Can you delete the passage without the reader losing information?
- **Priority**: P1 | Cost: low, text only | Value: medium, evidence B ([concise web text](https://www.nngroup.com/articles/concise-scannable-and-objective-how-to-write-for-the-web/): +58% measured usability, 51 users)
- **Web**: no
- **Overlap**: REF - fix by APAPL-PR-07, APAPL-BR-02, APAPL-BR-03, MECT-LT-04 (humor: none)

#### SOCAS-GN-15: Impressive Form Without Substance

- Abstract statement that cannot be false (buzzword profundity); impressive detail (jargon, figures, technical terms) irrelevant to the logic of the claim; claim supported only by repeating it; boasting without facts; interesting but irrelevant material
- **Applies to**: content that argues or explains; not reference lists, data tables or code
- **Test**: Could the statement be false, and does the impressive detail support the argument?
- **Priority**: P2 | Cost: medium, relevance judgment | Value: medium, evidence B ([pseudo-profound sentences](https://journal.sjdm.org/15/15923a/jdm15923a.pdf) rated 2.6 of 5; [irrelevant neuroscience](https://pmc.ncbi.nlm.nih.gov/articles/PMC2778755/) made bad explanations more satisfying to novices)
- **Web**: no
- **Overlap**: REF - fix by APAPL-PR-07

#### SOCAS-GN-16: Unnecessary Complexity

- Jargon where plain language works; complicated constructions for simple matters; long words to sound expert; a design, process or solution more complex than the problem needs (over-engineering, indirection without benefit)
- **Applies to**: all text, including designs and processes described in text; not code (code uses SOCAS-CD-05)
- **Test**: Is there a simpler word, sentence or solution that says or does the same?
- **Priority**: P1 | Cost: low, text only | Value: medium, evidence B ([longer words lowered judged author intelligence](https://onlinelibrary.wiley.com/doi/10.1002/acp.1178); [accessible abstracts](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2021.714321/full) raised understanding 47.9% to 57.9%); design part [ASSUMED], by analogy to SOCAS-CD-05
- **Web**: no
- **Overlap**: REF - fix by MECT-WC-02, MECT-VO-03 (design part: none)

#### SOCAS-GN-17: Lack of Structure

- Long text without breaks; nothing the reader can cite (no headings, numbers, IDs); long document without table of contents
- **Applies to**: text over about 300 words [ASSUMED threshold]; not code (see above)
- **Test**: Can the reader find and cite a specific point?
- **Priority**: P1 | Cost: low, text only | Value: medium, evidence B ([guideline-optimized application programming interface (API) documentation](https://doi.org/10.1145/3380851.3416759): task accuracy 86.35% vs 74.24%)
- **Web**: no
- **Overlap**: REF - fix by APAPL-PR-05, APAPL-ST-06, APAPL-ST-07

#### SOCAS-GN-18: Presentation Sloppiness

- Typos and grammatical errors; broken internal references ("see above", missing section); wrong dates. External sources: SOCAS-WR-01; outdated content: SOCAS-WR-08; stale code: SOCAS-CD-06
- **Applies to**: all text; not code (see above)
- **Test**: Are there typos, grammatical errors, broken internal references or wrong dates?
- **Priority**: P2 | Cost: low, text only | Value: low, `[ASSUMED]` (no study shows sloppiness predicts unreliable content). Kept because typos are the literal sign of sloppiness, no other rule covers them and the cost is low
- **Web**: no
- **Overlap**: REF - fix by APAPL-PR-04

## Application Rules

These rules govern every SOCAS run, in all 4 files. Format: rule, priority with reason.

### SOCAS-AP-01: Quote and Rule ID per Finding

- Every finding names the rule (`[written-out name] ([ID])`), quotes the passage (max 25 words) and gives its location. No quote, no deduction
- **Priority**: P1 | Cost: low | Value: high, evidence B ([CheckEval](https://aclanthology.org/2025.emnlp-main.796/): decomposed yes/no questions raised agreement across 12 judge models by 0.45)

### SOCAS-AP-02: Scoring and Rework Threshold

- Per rule one of 6 values, anchored by the passages that pass the test: 0 passages = 10; 1 minor passage = 8; 2+ minor or 1 noticeable = 6; reader must ask back or may misunderstand = 4; decisions at risk or repeated across the content = 2; content unusable for its purpose = 0. 6 or lower = flagged; 4 or lower = violated
- The verdict comes from the count of violated rules (SOCAS-RP-02); 3+ violated rules = rework recommendation. A mean score over applicable rules is informational only, with equal weights. Rules carry no dimension weights
- **Priority**: P1 | Cost: low | Value: high, evidence A-B ([Dawes 1979](https://doi.org/10.1037/0003-066x.34.7.571): equal-weight models predict as well as fitted weights; no source found for unequal dimension weights)

### SOCAS-AP-03: Context First and File Selection

- Before any rule runs: state content type, audience, purpose and stage (draft, working version, final version). Then load `SOCAS_RULES.md` plus one field file: writing, communication or coding. The content types of each field, including IPPS document types, are listed at the start of each field file
- Mixed content: score each part with its own field file; violated rules of all parts add up to one verdict, and a rule violated in two parts counts once. Direct commercial messages (sales email, offer sent by chat) load the communication file plus SOCAS-WR-05 to WR-07. Content of any field that cites external sources also runs SOCAS-WR-01. Documents that recommend actions or decisions (reports, proposals, INFO documents) also run SOCAS-CM-01
- **Priority**: P1 | Cost: low | Value: medium, evidence C (by analogy the Stop step of the [SIFT method](https://www.aft.org/ae/spring2025/caulfield_wineburg) (Stop, Investigate the source, Find other coverage, Trace the claim): 30 seconds of context improved weak critical thinkers' decisions)

### SOCAS-AP-04: SKIP vs NO INFORMATION

- `SKIP` = the content does not meet the rule's **Applies to** condition; the finding names the unmet condition in one line. `NO INFORMATION` = the condition is met but the content gives too little to test. Neither creates a deduction. When it is unclear whether the condition is met, run the rule
- **Priority**: P1 | Cost: low | Value: medium, evidence B ([Cochrane Risk of Bias 2 (RoB 2) tool](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-08) uses a separate "No information" answer)

### SOCAS-AP-05: One Passage, One Finding

- A passage counts for the one rule whose test fits best. The concrete field rule takes precedence over its abstract general rule (SOCAS-WR-06 before SOCAS-GN-07)
- **Priority**: P1 | Cost: low | Value: medium, `[ASSUMED]` (prevents double deduction)

### SOCAS-AP-06: Scoring Guard

- No credit for polish, visual design, long words, credentials, statistical vocabulary or repeated assertion. No rule judges authorship (human or AI)
- **Priority**: P1 | Cost: low | Value: high, evidence A-B ([design look appeared in 46.1% of 2,684 credibility comments](https://credibility.stanford.edu/pdf/How_Do_People_Evaluate_a_Web_Site%27s_Credibility_v37.pdf); AI detectors are unreliable, see the out-of-scope list above)

### SOCAS-AP-07: Tolerant Thresholds

- No exact-count thresholds unless a counting tool ran on the final text. Use "several" or "most", or label a count `approx`
- **Priority**: P1 | Cost: low | Value: medium, evidence B ([large language models (LLMs) fail at counting repeated tokens](https://dl.acm.org/doi/10.1145/3818606))

### SOCAS-AP-08: Self-Evaluation Flag

- When the scoring agent wrote the content, the output states `self-evaluation`. When available, a model other than the author model scores the content [ASSUMED: common mitigation, not measured for SOCAS]
- **Priority**: P1 | Cost: low | Value: medium, evidence B ([LLM judges score their own output higher](https://arxiv.org/abs/2404.13076), NeurIPS 2024)

### SOCAS-AP-09: Web Budget

- Open max 5 sources per run, decision-relevant first, one claim per source. Status per source: `OK: confirmed`, `WARNING: changed`, `ERROR: not found`, `SKIP: inaccessible`. A dead link is `SKIP`, not fabrication. A run without web access prints `web checks: not run`
- Registry and dependency lookups (SOCAS-CD-01, CD-06) run by tool when available; without a tool, unknown or unusual names come first and each lookup counts against the budget
- **Priority**: P1 | Cost: medium, web access | Value: high, evidence B ([fact-check accuracy fell about 42% as tool calls grew from 2 to 150](https://arxiv.org/html/2605.06635v1), preprint)

### SOCAS-AP-10: Run-to-Run Noise

- Score each content separately; never rank several contents by score alone. For decisions, run twice and compare verdict bands. A SOCAS result may demote or exclude a content (for example a source), but never ranks contents against each other
- **Priority**: P2 | Cost: medium, second run | Value: medium, evidence C ([13.6% pairwise verdict flips on identical reruns](https://arxiv.org/html/2606.13685), preprint)

### SOCAS-AP-11: Run Order

- One holistic pass over all applicable rules in the fixed rank order of the Rank Order sections: general file first, then the field file; within each file P1 before P2. Quote before score: collect the quotes of all rules first, apply SOCAS-AP-05 (field rule before general rule), then score. A time-limited run stops after the P1 rules and states `P2 rules: not run`
- **Priority**: P1 | Cost: low | Value: medium, evidence C ([scoring all criteria in one prompt preserved consistency](https://arxiv.org/html/2610.12083v1); [criteria order shifts scores](https://arxiv.org/html/2602.02219v2), so the order must be fixed; preprints)

### SOCAS-AP-12: Presence Tests Do Not Violate Alone

- A rule that only tests whether a feature is present (SOCAS-WR-03 date and author, SOCAS-WR-04 responsible party, SOCAS-CD-07 tests and setup) scores 6 at worst (flagged, not violated), unless the absence blocks the purpose of the content. A finding of SOCAS-WR-01 (opened source missing or changed) can violate alone, because it rests on the source itself
- **Priority**: P1 | Cost: low | Value: medium, evidence B by inference (easy-to-fake surface features misled historians and students, so surface features discriminate poorly; [fact-checkers who left the page](https://journals.sagepub.com/doi/10.1177/016146811912101102) judged better and faster; 45 participants)

## Reporting Rules

### SOCAS-RP-01: Finding Format

- Each finding: severity label, written-out rule name with ID, quote, location, one-line reason. Severity follows the rule score: `LOW` = 6, `MEDIUM` = 4, `HIGH` = 2, `CRITICAL` = 0
- **Priority**: P1 | Cost: low | Value: high (output is checkable)

### SOCAS-RP-02: Summary Format

- After findings: violated rules as `N of T` applicable rules, count of `SKIP` rules, verdict, `web checks: not run` or source count, `self-evaluation` when applicable, `P2 rules: not run` for time-limited runs. Verdicts: `OK` (0 violated), `PARTIAL FAIL` (1-2), `FAIL` (3+)
- **Priority**: P1 | Cost: low | Value: high (one-line decision)

