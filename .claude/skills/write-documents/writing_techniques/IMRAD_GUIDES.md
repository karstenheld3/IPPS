# IMRAD Guide

Read BEFORE writing an empirical report, benchmark study, systematic review, or evaluation with `using IMRAD`. IMRaD = Introduction, Methods, Results, and Discussion, extended here with an abstract and recommendations.

## 1. Decide Whether IMRaD Fits

Use IMRaD when the reader must judge and reuse the evidence: the report documents the whole finding set within a declared scope, including null results and findings that contradict each other. Typical outputs: empirical research reports, A/B test and pilot evaluations, benchmark studies, systematic reviews, audit findings.

Tell the user that a different technique fits better, and keep `IMRAD` until the user decides (`DRSYNART-DD-08`), when:
- The reader needs one recommendation and the evidence only supports it: use `MINTO` (and link the full report)
- The reader stops early and needs the headline result only: use `IMINTO` as a summary note
- The text is meant for a broad audience and must hold attention: use `ABTSTORY` or `KABOB` and cite the report

The organizing principle is completeness over the declared scope, not a single governing thought. Applying the pyramid principle to a report turns it into an argument and hides findings.

## 2. Plan Before Writing

1. Write the scope: question(s), population or system, period, and what is explicitly out of scope
2. Write the research questions as numbered questions (RQ1, RQ2, ...); results will follow this numbering
3. Document the method so another analyst could repeat it: data sources, sample, period, tools, analysis steps, exclusions
4. List every finding per research question, including null and contradictory results, with a confidence level
5. List every hypothesis that still survives the evidence; the discussion must name all of them

## 3. Execute Each Section

1. Introduction: from general context to the specific gap, ending with the numbered research questions and the scope
2. Methods: data, sample, period, procedure, analysis, exclusions. Impersonal passive voice is acceptable here where the actor is irrelevant
3. Results: one subsection per research question; facts only, with numbers, uncertainty ranges, and confidence labels; no interpretation
4. Discussion: interpretation per research question, surviving alternative explanations, comparison with prior work, and limitations
5. Recommendations: actionable next steps that follow from the results, each tied to a research question
6. Abstract: write last, about 100 words, neutral summary of question, method, main results, and main limitation

## 4. When the User Also Passes a Persona

- This section applies only when the user passes `as <persona>`. Without it, apply no persona and do not pick one from the list below (`DRSYNART-DD-08`)
- Fitting personas, offered only when the user asks for persona help: `ANALYST` (quantitative studies), `JURIST` (compliance analyses), `INTELLECTUAL` (public research summaries), `HISTORIAN` (archival studies)
- High-Formality personas (7-8) fit Methods and Results; a lower Warmth is appropriate because the reader judges evidence, not tone
- Persona traits fit the Discussion: Pre-Emptive Reader Objection for confounders, The Catch for boundary conditions, Inline Sanity Math for translating effect sizes. No traits in the Abstract or Methods
- Persona style must not upgrade confidence levels, round away uncertainty, or omit null results

## 5. Use the Template and the Example

- Skeleton: [TEMPLATES/IMRAD_TEMPLATE.md](TEMPLATES/IMRAD_TEMPLATE.md)
- Complete GOOD example with `ANALYST`: [EXAMPLES/IMRAD_EXAMPLE_01-EmpiricalResultsReport.md](EXAMPLES/IMRAD_EXAMPLE_01-EmpiricalResultsReport.md)

## 6. Strategic Review Questions

Used by `/critique` after writing:
- Did the reader need the complete finding set, or would a decision memo with a linked report have served them better?
- Were the research questions fixed before the analysis, or adjusted to match the results?
- Would another analyst reach the same results by following the Methods section?
