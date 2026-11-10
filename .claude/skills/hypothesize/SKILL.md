---
name: hypothesize
description: Formulate falsifiable, competing working hypotheses with rivals, falsifiers, and crucial test plans into a Hypothesis Register deliverable
disable-model-invocation: true
---

# Hypothesize Workflow

Abduct competing, testable working hypotheses from empirical themes, open contradictions, and evidence gaps, compiling into a structured Hypothesis Register deliverable.

**Goal**: `_INFO_[TOPIC]-IN[NN]_HypothesisRegister.md` conforming to `HYPOTHESIS_TEMPLATE.md`

**Why**: Generates mutually exclusive explanatory models with explicit refutation conditions and crucial test plans to prevent confirmation bias and enable rigorous validation.

## Required Skills

- @skills:analysis-methods `HYPOTHESIS_GUIDES.md` (form selection, generation methods, 3-7 candidates, rival pairing, falsifier, test plan)
- @skills:analysis-methods `HYPOTHESIS_RULES.md` (output standards, rival and falsifier enforcement, ICD-203 likelihood phrasing)
- @skills:analysis-methods `HYPOTHESIS_TEMPLATE.md` (deliverable structure)
- @skills:analysis-methods `ANALYSIS_GUIDES.md` (orchestration, likelihood and confidence phrasing, stage sequence, tier resolution)
- Never load CHECKS files during execution (`DRSYNART-FR-32`, `GRUC-IG-03`)

## MUST-NOT-FORGET

- First response line (`DRSYNART-8.1`): output `Tier N - [reason]` before any other text
- Tier resolution (`DRSYNART-FR-02`): Tier 1 default for single file, pattern map, or raw text; Tier 2 when input is a `T##_` research folder or keyword `tier 2`
- Input flexibility (`DRSYNART-DD-04`, `DRSYNART-FR-03`): accept pattern map, C1 Knowledge Library, or raw input; when input is not a pattern map, extract empirical themes and contradictions before abducting hypotheses
- Candidate set range (`HYP-DV-01`): generate 3-7 candidate hypotheses per research question; include at least one contrarian candidate challenging dominant narratives
- Mandatory rival or null (`HYP-RV-01`): every hypothesis must name an explicit rival (`H-NN`) or null (`H-00`) ensuring mutual exclusivity
- Observable falsifier (`HYP-FL-01`): define concrete, observable refutation threshold for every hypothesis
- Crucial test plan (`HYP-TP-01`): specify evidence type, search location, and decisive exclusion condition
- Calibrated ICD-203 likelihood and confidence (`HYP-LK-01`, `DRSYNART-DD-06`): use prose terms only; never use bracket labels or numeric percentages
- Planning anchor (`DRSYNART-IG-05`): at Tier 2, `/write-strut` first, then `/write-prompts`; execute unless `plan` or `plan only`
- CHECKS files are invisible during execution; never load them in this workflow
- Invariant 6: analysis workflows modify session tracking files (`NOTES.md`, `PROBLEMS.md`, `PROGRESS.md`, `FAILS.md`) only through `/session-save`

## Command Grammar

```text
/hypothesize [<input>] [tier N] [plan | plan only]
```

## Context-Specific Branches

- **Branch 1 (Tier 1 - Single-Turn Abduction, Default)**: Input is a pattern map or raw text. Abduct candidate hypotheses, bind rivals and falsifiers, define test plans, and compile register in one turn.
- **Branch 2 (Tier 2 - Planned Folder Processing)**: Input is a `T##_` research folder or called with `tier 2`. Invoke `/write-strut` then `/write-prompts` (1 PROMPTS file, 3-5 prompts). Stop if `plan` or `plan only`. Execute headlessly.

## Steps

1. **Tier Resolution and Input Ingestion**:
   - Evaluate input and keywords: `T##_` folder or `tier 2` -> Tier 2; else Tier 1 default.
   - Emit `Tier N - [reason]` on first response line.
   - Inspect `<input>`: if pattern map, ingest themes, contradictions (`CR-NN`), and gaps (`GAP-NN`); if raw material, extract primary themes and contradictions first per `ANALYSIS_GUIDES.md`.
2. **Planning (Tier 2 only)**:
   - Run `/write-strut` for `_agentwork/__STRUT_[TOPIC].md`.
   - Run `/write-prompts` for 1 PROMPTS file with separate `/verify` + `/fix` checkpoint prompts (`DRSYNART-NFR-05`).
   - If `plan` or `plan only`: report PROMPTS file path and stop.
3. **Hypothesis Abduction and Rival Binding**:
   - Abduct 3-7 candidate hypotheses per research question from themes, contradictions, and gaps per `HYPOTHESIS_GUIDES.md`.
   - Classify form (Causal, Correlational, Categorical, Predictive) and ensure explanatory claim.
   - Bind each candidate to an explicit competing rival (`H-NN`) or null (`H-00`).
   - Formulate observable falsifier condition and crucial test plan.
   - Assign prior likelihood and confidence using ICD-203 prose vocabulary.
4. **Output Compilation and Verification**:
   - Compile `_INFO_[TOPIC]-IN[NN]_HypothesisRegister.md` using `HYPOTHESIS_TEMPLATE.md` field order (SPEC Section 10.4).
   - Run verification against `HYPOTHESIS_RULES.md`. At Tier 2, sync tracking via `/session-save`.

## Output

- Deliverable: `_INFO_[TOPIC]-IN[NN]_HypothesisRegister.md` (or nested `_INFO_[TOPIC]-[SUBTOPIC]-IN01_HypothesisRegister.md`) beside input or in session root (Tier 1), or in `S##_[SUBTOPIC]_Analysis_YYYY-MM-DD\` (Tier 2).
- Scaffolding (Tier 2 only): `__STRUT_[TOPIC].md` and `_PROMPTS_*.md` in `_agentwork/` (removed on `/cleanup`).
- Contains: header block with input provenance, Hypothesis Register entries with ID, Statement, Form, Source themes, Rival, Falsifier, Prior likelihood, Confidence, Test plan.

## Quality Gate

- [ ] First response line declares `Tier N - [reason]`
- [ ] Candidate set contains 3-7 competing hypotheses per research question including contrarian alternative
- [ ] Every hypothesis asserts an explanatory mechanism or prediction and names an explicit rival (`H-NN` or `H-00`)
- [ ] Concrete observable falsifier and crucial test plan defined for every candidate
- [ ] Likelihood and confidence phrased in ICD-203 prose without bracket labels or percentages
- [ ] Output conforms to `HYPOTHESIS_TEMPLATE.md` with zero Markdown tables
- [ ] Zero craft or method knowledge in workflow body; zero CHECKS files loaded; session files modified only through `/session-save`
