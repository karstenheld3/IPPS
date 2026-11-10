---
name: pattern-detect
description: Code findings, detect themes, catalog contradictions, evaluate assumptions, and identify research gaps into a Pattern Map deliverable
disable-model-invocation: true
---

# Pattern Detect Workflow

Synthesize empirical findings into a structured Pattern Map deliverable through qualitative coding, thematic clustering, contradiction mapping, assumption audits, and gap identification.

**Goal**: `_INFO_[TOPIC]-IN[NN]_PatternMap.md` conforming to `PATTERN-DETECTION_TEMPLATE.md`

**Why**: Transforms raw or research inputs into rigorous, attributed findings, coherent themes, and explicit fault lines that serve as empirical ground for hypothesis abduction.

## Required Skills

- @skills:analysis-methods `PATTERN-DETECTION_GUIDES.md` (coding pass, theme building, contradiction register, key assumptions, gaps)
- @skills:analysis-methods `PATTERN-DETECTION_RULES.md` (output verification, source thresholds, contradiction pairing)
- @skills:analysis-methods `PATTERN-DETECTION_TEMPLATE.md` (deliverable structure)
- @skills:analysis-methods `ANALYSIS_GUIDES.md` (input provenance, stage sequence, tier resolution)
- Never load CHECKS files during execution (`DRSYNART-FR-32`, `GRUC-IG-03`)

## MUST-NOT-FORGET

- First response line (`DRSYNART-8.1`): output `Tier N - [reason]` before any other text
- Tier resolution (`DRSYNART-FR-02`): Tier 1 default for single file, bundle, or raw text; Tier 2 when input is a `T##_` research folder or keyword `tier 2`
- Generic input (`DRSYNART-DD-04`, `DRSYNART-FR-03`): accept C1, single INFO, bundle, PDF transcriptions, websites, notes, or chat text
- S1 coding pass (`DRSYNART-FR-12`): execute qualitative coding pass on non-C1 input before theme building; record input provenance in header block
- Two-source theme rule (`PTD-TH-01`): every theme must cite >=2 finding IDs from >=2 independent sources
- Counter-finding search (`PTD-TH-02`): document search scope and negative findings for every theme
- Two-sided contradiction rule (`PTD-CR-01`): every contradiction must cite both Side A and Side B with source IDs and remain OPEN
- Planning anchor (`DRSYNART-IG-05`): at Tier 2, `/write-strut` first, then `/write-prompts`; execute unless `plan` or `plan only`
- CHECKS files are invisible during execution; never load them in this workflow
- Invariant 6: analysis workflows modify session tracking files (`NOTES.md`, `PROBLEMS.md`, `PROGRESS.md`, `FAILS.md`) only through `/session-save`

## Command Grammar

```text
/pattern-detect [<input>] [tier N] [plan | plan only]
```

## Context-Specific Branches

- **Branch 1 (Tier 1 - Single-Turn Synthesis, Default)**: Input is a single file, bundle, or raw material. Run S1 coding pass (if non-C1), thematic clustering, contradiction cataloging, assumption checks, and gap identification in one turn.
- **Branch 2 (Tier 2 - Planned Folder Processing)**: Input is a `T##_` research folder or called with `tier 2`. Invoke `/write-strut` then `/write-prompts` (1 PROMPTS file, 3-5 prompts). Stop if `plan` or `plan only`. Execute headlessly.

## Steps

1. **Tier Resolution and Input Ingestion**:
   - Evaluate input and keywords: `T##_` folder or `tier 2` -> Tier 2; else Tier 1 default.
   - Emit `Tier N - [reason]` on first response line.
   - Inspect `<input>`: if C1 Knowledge Library, inherit finding claims and `-02` source IDs; if non-C1, execute S1 qualitative coding pass to construct codebook and attributed findings list (`DRSYNART-FR-12`).
2. **Planning (Tier 2 only)**:
   - Run `/write-strut` for `_agentwork/__STRUT_[TOPIC].md`.
   - Run `/write-prompts` for 1 PROMPTS file with separate `/verify` + `/fix` checkpoint prompts (`DRSYNART-NFR-05`).
   - If `plan` or `plan only`: report PROMPTS file path and stop.
3. **Thematic Synthesis and Register Compilation**:
   - Execute theme building via selected method per `PATTERN-DETECTION_GUIDES.md`. Record counter-findings search for every theme.
   - Catalog all empirical incompatibilities in the Contradiction Register with status `OPEN`.
   - Audit structural premises via Key Assumptions Check and list missing observations in Gaps.
4. **Output Compilation and Verification**:
   - Compile `_INFO_[TOPIC]-IN[NN]_PatternMap.md` using `PATTERN-DETECTION_TEMPLATE.md`.
   - Run verification against `PATTERN-DETECTION_RULES.md`. At Tier 2, sync tracking via `/session-save`.

## Output

- Deliverable: `_INFO_[TOPIC]-IN[NN]_PatternMap.md` (or nested `_INFO_[TOPIC]-[SUBTOPIC]-IN01_PatternMap.md`) beside input or in session root (Tier 1), or in `S##_[SUBTOPIC]_Analysis_YYYY-MM-DD\` (Tier 2).
- Scaffolding (Tier 2 only): `__STRUT_[TOPIC].md` and `_PROMPTS_*.md` in `_agentwork/` (removed on `/cleanup`).
- Contains: header block with input provenance, Codebook, Findings List, Theme Map, Contradiction Register, Key Assumptions, Gaps.

## Quality Gate

- [ ] First response line declares `Tier N - [reason]`
- [ ] Non-C1 input includes S1 qualitative coding pass and input provenance in header block
- [ ] Every theme supported by >=2 finding IDs from >=2 independent sources with counter-findings search logged
- [ ] Contradictions record both Side A and Side B with finding and source IDs and remain OPEN
- [ ] Output conforms to `PATTERN-DETECTION_TEMPLATE.md` with zero Markdown tables
- [ ] Zero craft or method knowledge in workflow body; zero CHECKS files loaded; session files modified only through `/session-save`
