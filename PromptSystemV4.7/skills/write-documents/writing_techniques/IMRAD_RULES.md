# IMRAD Rules

Output standards for documents written `using IMRAD` (Abstract, Introduction, Methods, Results, Discussion, Recommendations).

**Writing quality:** Apply `APAPALAN_RULES.md` and `MECT_WRITING_RULES.md`. Key rules: APAPL-PR-07 (be specific), APAPL-PR-05 (referenceable IDs), APAPL-PR-01 (datetime format).

## Rule Index

Structure (ST)
- IMRAD-ST-01: Sections appear in order: Abstract, Introduction, Methods, Results, Discussion, Recommendations
- IMRAD-ST-02: Abstract has about 100 words and is a neutral summary
- IMRAD-ST-03: Results are organized by numbered research question
- IMRAD-ST-04: Discussion contains a Limitations subsection

Content (CT)
- IMRAD-CT-01: All findings within the declared scope are reported, including null results
- IMRAD-CT-02: Results contain no interpretation; interpretation belongs in the Discussion
- IMRAD-CT-03: Recommendations reference the research question they follow from

Evidence (EV)
- IMRAD-EV-01: Every finding carries a number, an uncertainty range where applicable, and a confidence label
- IMRAD-EV-02: All hypotheses that survive the evidence are named
- IMRAD-EV-03: Methods are reproducible (data source, sample, period, tools, exclusions)

## IMRAD-ST-01: Section Order

**BAD:** Recommendations first, then a "Findings" section mixing method and interpretation.

**GOOD:** Abstract, 1. Introduction, 2. Methods, 3. Results, 4. Discussion, 5. Recommendations.

## IMRAD-ST-02: Neutral 100-Word Abstract

**BAD:** "This groundbreaking study proves that the four-day week transforms productivity."

**GOOD:** "We compared ticket resolution in 4 teams on a four-day week with 4 teams on a five-day week over 6 months (n = 18,400 tickets). Median resolution time did not differ (difference 0.2 hours, 95% interval -0.6 to 1.0)..."

## IMRAD-ST-03: Results by Research Question

**BAD:** Results ordered by the date the analyst ran each query.

**GOOD:** `### 3.1 RQ1: Resolution time`, `### 3.2 RQ2: Customer satisfaction`, `### 3.3 RQ3: Sick days`

## IMRAD-ST-04: Limitations Subsection

**BAD:** Limitations mentioned in one clause in the conclusion.

**GOOD:** `### 4.4 Limitations` listing team selection, period length, and measurement changes.

## IMRAD-CT-01: Complete Findings Including Null Results

**BAD:** The report omits RQ2 because satisfaction did not change.

**GOOD:** "RQ2: Customer satisfaction did not change measurably (4.31 vs. 4.29 of 5; difference within measurement noise)."

## IMRAD-CT-02: No Interpretation in Results

**BAD:** "Resolution time stayed flat, which proves that employees worked more focused."

**GOOD:** Results: "Resolution time stayed flat (difference 0.2 hours)." Discussion: "One explanation is higher focus; a second is that ticket volume per agent fell by 6%."

## IMRAD-CT-03: Recommendations Tied to Research Questions

**BAD:** "Introduce the four-day week company-wide."

**GOOD:** "Extend the pilot to two more departments for 6 months (RQ1, RQ3), with ticket volume per agent held constant."

## IMRAD-EV-01: Numbers, Ranges, Confidence

**BAD:** "Sick days dropped significantly."

**GOOD:** "Sick days fell from 4.8 to 3.1 per person over 6 months (difference -1.7, 95% interval -2.9 to -0.5). Confidence: medium (small sample, one season)."

## IMRAD-EV-02: Surviving Hypotheses Named

**BAD:** Discussion presents higher motivation as the only cause.

**GOOD:** "Three explanations remain consistent with the data: higher focus, lower ticket volume per agent, and seasonal variation. The pilot cannot separate them."

## IMRAD-EV-03: Reproducible Methods

**BAD:** "We analyzed the ticket data."

**GOOD:** "Source: help-desk export of all tickets closed 2026-01-01 to 2026-06-30 (n = 18,400). Excluded: tickets reopened more than twice (n = 212). Analysis: median comparison with bootstrap intervals (10,000 resamples)."
