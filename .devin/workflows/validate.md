---
description: Weight evidence, compile ACH audit trail, log disconfirmation, and rank hypotheses or statements into a Validation Report deliverable
default_tier: 1 (default)
---

# Validate Workflow

Test working hypotheses or empirical statements against diagnostic evidence, log disconfirmation attempts, and rank items on the 0-8 scale into a Validation Report deliverable.

**Goal**: `_INFO_[TOPIC]-IN[NN]_ValidationReport.md` conforming to `VALIDATION_TEMPLATE.md`

**Why**: Establishes empirical credibility through two-layer evidence weighting, exhaustive disconfirmation, and deterministic ranking with calibrated likelihood and confidence prose assessments.

## Required Skills

- @skills:analysis-methods `VALIDATION_GUIDES.md` (evidence search, GRADE and Toulmin weighting, ACH audit trail, disconfirmation, 0-8 ranking, loop-back, writing implications)
- @skills:analysis-methods `VALIDATION_RULES.md` (output verification, evidence thresholds, tie-breaking, ICD-203 prose likelihood and confidence)
- @skills:analysis-methods `VALIDATION_TEMPLATE.md` (deliverable structure)
- @skills:analysis-methods `ANALYSIS_GUIDES.md` (orchestration, likelihood and confidence phrasing, loop-back, tier resolution)
- Never load CHECKS files during execution (`DRSYNART-FR-32`, `GRUC-IG-03`)

## MUST-NOT-FORGET

- First response line (`DRSYNART-8.1`): output `Tier N - [reason]` before any other text
- Tier resolution (`DRSYNART-FR-02`): Tier 1 default for single file, register, or statements; Tier 2 when input is a `T##_` research folder or keyword `tier 2`
- Input flexibility (`DRSYNART-DD-04`, `DRSYNART-FR-03`, `VAL-IN-01`): accept hypothesis register or bare empirical statements
- Multi-tier evidence search (`VAL-SR-01`): search local material first; execute targeted web search or run tests whenever local material does not settle an item, at every tier
- ACH matrix discipline (`VAL-AC-01`): use ACH matrix strictly as an audit trail and search director, never as a mechanical verdict calculator
- Mandatory disconfirmation (`VAL-DC-01`): log refutation queries and explicit `exhausted: yes/no` flag for every candidate above refuted
- Strict 0-8 ranking (`VAL-RK-01`): refuted (0) < Kent ICD-203 terms (1-7) < proven (8); zero tied ranks permitted; break ties deterministically and record rationale
- Evidence thresholds (`VAL-PR-01`): proven requires `[PROVEN]` or `[TESTED]` evidence; refuted requires refuting finding ID
- Calibrated prose phrasing (`VAL-LK-01`, `DRSYNART-DD-06`): express likelihood and confidence as distinct prose sentences; never use bracket labels or percentages
- Layer 1 loop-back confinement (`VAL-LP-01`, `DRSYNART-8.6`): record unsettled items as Layer 1 research questions; never call Layer 1 workflows autonomously
- Planning anchor (`DRSYNART-IG-05`): at Tier 2, `/write-strut` first, then `/write-prompts`; execute unless `plan` or `plan only`
- CHECKS files are invisible during execution; never load them in this workflow
- Invariant 6: analysis workflows modify session tracking files (`NOTES.md`, `PROBLEMS.md`, `PROGRESS.md`, `FAILS.md`) only through `/session-save`

## Command Grammar

```text
/validate [<input>] [tier N] [plan | plan only]
```

## Context-Specific Branches

- **Branch 1 (Tier 1 - Single-Turn Validation, Default)**: Input is a hypothesis register, document, or bare list of statements. Run multi-tier evidence search, two-layer weighting, ACH audit trail, disconfirmation logging, and 0-8 ranking in one turn.
- **Branch 2 (Tier 2 - Planned Folder Processing)**: Input is a `T##_` research folder or called with `tier 2`. Invoke `/write-strut` then `/write-prompts` (1 PROMPTS file, 3-5 prompts). Stop if `plan` or `plan only`. Execute headlessly.

## Steps

1. **Tier Resolution and Input Ingestion**:
   - Evaluate input and keywords: `T##_` folder or `tier 2` -> Tier 2; else Tier 1 default.
   - Emit `Tier N - [reason]` on first response line.
   - Ingest `<input>`: if hypothesis register, inherit IDs and falsifiers; if bare statements, assign continuous IDs (`H-01`, `H-02`), extract claims, and infer null hypotheses (`VAL-IN-01`).
2. **Planning (Tier 2 only)**:
   - Run `/write-strut` for `_agentwork/__STRUT_[TOPIC].md`.
   - Run `/write-prompts` for 1 PROMPTS file with separate `/verify` + `/fix` checkpoint prompts (`DRSYNART-NFR-05`).
   - If `plan` or `plan only`: report PROMPTS file path and stop.
3. **Evidence Search, Weighting, and Disconfirmation**:
   - Execute multi-tier evidence search (`VAL-SR-01`): search local files first; escalate to targeted web search or empirical tests whenever local material does not settle an item, at every tier.
   - Apply two-layer weighting (`VAL-WT-01`): GRADE certainty per hypothesis and Toulmin warrant per diagnostic finding link.
   - Audit diagnostic findings via ACH Matrix (`VAL-AC-01`). Log refutation attempts and search exhaustion in Disconfirmation Log (`VAL-DC-01`).
4. **Ranking Compilation and Handoff**:
   - Score items on 0-8 scale (`VAL-RK-01`); break ties deterministically by confidence, then evidence weight, recording tie-breaks. Verify thresholds for proven and refuted (`VAL-PR-01`).
   - Formulate likelihood and confidence as distinct prose sentences (`VAL-LK-01`).
   - Record open items (`exhausted: yes`, low confidence) in Research Questions for Layer 1 (`VAL-LP-01`). Document Writing Implications for Layer 3.
   - Compile `_INFO_[TOPIC]-IN[NN]_ValidationReport.md` using `VALIDATION_TEMPLATE.md`.
   - Run verification against `VALIDATION_RULES.md`. At Tier 2, sync tracking via `/session-save`.

## Output

- Deliverable: `_INFO_[TOPIC]-IN[NN]_ValidationReport.md` (or nested `_INFO_[TOPIC]-[SUBTOPIC]-IN01_ValidationReport.md`) beside input or in session root (Tier 1), or in `S##_[SUBTOPIC]_Analysis_YYYY-MM-DD\` (Tier 2).
- Scaffolding (Tier 2 only): `__STRUT_[TOPIC].md` and `_PROMPTS_*.md` in `_agentwork/` (removed on `/cleanup`).
- Contains: header block with input provenance, Items, Evidence Weights, ACH Matrix, Disconfirmation Log, Ranking (0-8 with prose likelihood and confidence), Research Questions for Layer 1, Writing Implications.

## Quality Gate

- [ ] First response line declares `Tier N - [reason]`
- [ ] Evidence search executed local-first with targeted web or test fallback when local material did not settle an item
- [ ] Disconfirmation logged for every item above refuted with explicit exhausted flag
- [ ] All items ranked on strict 0-8 scale with zero tied ranks and recorded tie-breaks
- [ ] Proven rank supported by `[PROVEN]` or `[TESTED]` evidence; refuted rank cites refuting finding ID
- [ ] Likelihood and confidence phrased as distinct prose sentences without bracket labels or percentages
- [ ] Unsettled items recorded in Research Questions for Layer 1 without autonomous Layer 1 workflow calls
- [ ] Output conforms to `VALIDATION_TEMPLATE.md` with zero Markdown tables
- [ ] Zero craft or method knowledge in workflow body; zero CHECKS files loaded; session files modified only through `/session-save`
