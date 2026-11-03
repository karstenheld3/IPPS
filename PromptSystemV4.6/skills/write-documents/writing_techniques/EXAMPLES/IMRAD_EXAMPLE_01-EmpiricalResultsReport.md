# IMRAD Example 01: EmpiricalResultsReport

Pilot evaluation report written `using IMRAD as ANALYST`. The company, teams, and all data are fictional.

## Context

A software company ran a six-month four-day-week pilot in customer support. Leadership, the works council, and team leads must judge the evidence before deciding on next steps. The report must document all results, including the ones that do not change, so that each group can check the claims they care about.

## Document

```markdown
# Four-Day Week Pilot in Customer Support: Resolution Time, Satisfaction, and Sick Days, 2026-01 to 2026-06

## Abstract

We compared 4 support teams on a four-day week (32 hours) with 4 teams on a five-day week (40 hours) from 2026-01-01 to 2026-06-30, using 18,400 closed tickets and HR absence records. Median resolution time did not differ measurably (difference +0.2 hours, 95% interval -0.6 to +1.0). Customer satisfaction did not change (4.31 vs. 4.29 of 5). Sick days fell by 1.7 per person (95% interval -2.9 to -0.5). Ticket volume per agent was 6% lower in pilot teams, which limits causal conclusions. One season and 8 teams restrict generalization.

## 1. Introduction

Support leadership expected that fewer working hours would slow ticket handling. The works council expected lower absence. Neither expectation had been tested in this company.

Research questions:
- RQ1: Did median ticket resolution time differ between pilot and comparison teams?
- RQ2: Did customer satisfaction differ?
- RQ3: Did sick days per person differ?

Scope: first-level customer support, 8 teams, 2026-01-01 to 2026-06-30. Out of scope: second-level engineering support, salary effects.

## 2. Methods

- Data source: help-desk export of all tickets closed in the period (exported 2026-07-03); HR absence records
- Sample: n = 18,400 tickets; 64 agents in 8 teams of similar size and product area, 4 assigned to the pilot by lottery
- Period: 2026-01-01 to 2026-06-30
- Procedure: pilot teams worked Monday to Thursday, 32 hours; comparison teams worked 40 hours over five days
- Analysis: median comparison with bootstrap 95% intervals (10,000 resamples); survey means compared with t-test
- Exclusions: tickets reopened more than twice (n = 212), because reopen handling changed in March

## 3. Results

### 3.1 RQ1: Resolution time

Median resolution time was 6.4 hours in pilot teams and 6.2 hours in comparison teams (difference +0.2 hours, 95% interval -0.6 to +1.0). Confidence: high.

### 3.2 RQ2: Customer satisfaction

Mean satisfaction was 4.31 of 5 in pilot teams and 4.29 in comparison teams (n = 5,120 survey responses; difference within measurement noise, p = 0.61). Confidence: high.

### 3.3 RQ3: Sick days

Sick days averaged 3.1 per person in pilot teams and 4.8 in comparison teams over six months (difference -1.7, 95% interval -2.9 to -0.5). Confidence: medium (one winter season, 64 people).

### 3.4 Ticket volume per agent

Pilot agents closed 6% fewer tickets per person than comparison agents, because routing assigned tickets by available hours.

## 4. Discussion

### 4.1 Interpretation

Even though pilot agents worked 20% fewer hours, resolution time and satisfaction stayed within measurement noise. Sick days fell by about a third. Over six months and 32 pilot agents, that equals roughly 54 fewer sick days.

### 4.2 Alternative explanations

Three explanations remain consistent with the data: higher focus during shorter weeks; lower ticket volume per agent (section 3.4); and seasonal variation in illness that affected teams differently. The pilot cannot separate these explanations.

### 4.3 Limitations

- One season: winter illness patterns may exaggerate the sick-day difference
- Routing by available hours reduced pilot workload by 6%, so resolution time was not tested under equal load
- 8 teams in one product area; other support areas may differ

## 5. Recommendations

- Extend the pilot to two more product areas for six months, with tickets routed by team instead of by hours, to test resolution time under equal load (RQ1)
- Keep tracking sick days through a summer season before estimating annual savings (RQ3)
- Continue the satisfaction survey unchanged so results remain comparable (RQ2)
```

## Key Decisions

- Results for all three research questions, including two "no measurable difference" results (IMRAD-CT-01)
- The unexpected workload difference reported as its own result (3.4) instead of being hidden, because it limits every causal claim (IMRAD-EV-02)
- Results contain numbers, intervals, and confidence labels only; interpretation appears in the Discussion (IMRAD-CT-02, IMRAD-EV-01)
- Methods name source, export date, sample, lottery assignment, analysis, and exclusions with counts, so another analyst can repeat the analysis (IMRAD-EV-03)
- Abstract written last at about 100 words, neutral, and states the main limitation (IMRAD-ST-02)
- Recommendations extend the pilot instead of deciding company-wide, each tied to a research question (IMRAD-CT-03)
- Persona `ANALYST` (Formality 7, Density 7): two traits in different Discussion paragraphs, Pre-Emptive Reader Objection ("Even though pilot agents worked 20% fewer hours...") and Inline Sanity Math (54 fewer sick days); no traits in Abstract, Methods, or Results
