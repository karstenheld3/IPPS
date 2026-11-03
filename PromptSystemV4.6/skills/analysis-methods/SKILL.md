---
name: analysis-methods
description: Apply when conducting pattern detection, hypothesis generation, validation and ranking, full synthesis with /analyze, or structured step-by-step problem investigation with /investigate.
---

# Analysis and Synthesis Methods Skill

Layer 2 of the research-to-deliverable pipeline. Systematic qualitative coding, pattern detection, abductive hypothesis generation, and evidence validation with calibrated confidence. Origin: `_INFO_TARGET_ARCHITECTURE.md [DRSYNART-IN02]` and `_INFO_RSRCHMTHD-01_Summary.md [DRSYNART-RSRCHMTHD-IN01]`.

## When to Use

**Use this skill** when the user's intent requires:
- Qualitative coding and extracting empirical findings from research or raw text
- Detecting themes, mapping contradictions, and identifying evidence gaps
- Formulating falsifiable working hypotheses with competing alternatives and test plans
- Weighting evidence, compiling an ACH audit trail, and ranking statements from proven to refuted
- Synthesizing validated findings into C2 Validated Knowledge for deliverable authoring
- Conducting multi-session step-by-step problem investigations with an append-only log

## Do NOT Apply When

- Initial data gathering or web search without analytical synthesis is needed -> use `@skills:research-methods` (`/research`, `/deep-research`)
- Authoring final deliverables (articles, reports, ebooks) -> use `@skills:write-documents` (`/propose-*`, `/draft-*`, `/write-*`)
- Fixing known-cause code or environment defects directly -> use `/fix` or `/bugfix`

## MUST-NOT-FORGET

- Single home for analysis methods (`DRSYNART-DD-01`): routes `/analyze`, `/pattern-detect`, `/hypothesize`, `/validate`, and `/investigate`
- Generic input capability (`DRSYNART-DD-04`): operates on C1, bundles, notes, or raw text; non-C1 input triggers S1 coding pass to establish provenance (`DRSYNART-FR-12`)
- Strict stage progression (`DRSYNART-FR-13`): Pattern Detection (S2) -> Hypotheses (S3) -> Validation (S4); never abduct hypotheses before mapping patterns or contradictions
- Calibrated prose vocabulary (`DRSYNART-DD-06`): likelihood and confidence must be distinct prose phrases (ICD-203); never use bracket labels or numeric percentages
- Loop-back discipline (`DRSYNART-8.6`): record open research questions for Layer 1 in the deliverable; never invoke Layer 1 workflows autonomously
- CHECKS isolation (`DRSYNART-FR-32`, `GRUC-IG-03`): CHECKS files are never loaded during working workflow execution

## Intent Lookup

- **Detect patterns, themes, contradictions, or gaps** -> `PATTERN-DETECTION_GUIDES.md` (workflow `/pattern-detect`)
- **Formulate competing hypotheses and crucial test plans** -> `HYPOTHESIS_GUIDES.md` (workflow `/hypothesize`)
- **Weight evidence, test disconfirmation, and rank claims** -> `VALIDATION_GUIDES.md` (workflow `/validate`)
- **Execute end-to-end multi-stage analysis into one Analysis INFO** -> `ANALYSIS_GUIDES.md` (workflow `/analyze`)
- **Step-by-step defect investigation with append-only log** -> `INVESTIGATION_GUIDES.md` (workflow `/investigate`)

## C1 -> C2 Hand-over Contract

- **Input (C1 Knowledge Library or raw material)**:
  - C1: `_INFO_[TOPIC]-IN01_Summary.md`, `_INFO_[TOPIC]-IN02_Sources.md`, topic files, `_SOURCES/`
  - Any raw input: single INFO, bundle, notes, PDF transcriptions, websites, or conversation text (`DRSYNART-DD-04`). Non-C1 input triggers S1 coding pass to establish provenance (`DRSYNART-FR-12`).
- **Output (C2 Validated Knowledge)**:
  - From `/analyze`: always one `_INFO_[TOPIC]-IN[NN]_Analysis.md` (from `ANALYSIS_TEMPLATE.md`) containing Pattern Map, Hypothesis Register, Validation Report, and Research Questions for Layer 1.
  - From stage workflows: one specialized artifact (`_PatternMap.md`, `_HypothesisRegister.md`, or `_ValidationReport.md`).
  - Every validated item carries:
    1. A position on the 9-point ranking scale: `refuted` < 7 ICD-203 terms < `proven` (`DRSYNART-8.6`).
    2. A Kent likelihood phrase and a separate confidence phrase in prose (`DRSYNART-DD-06`).
    3. An entry in the disconfirmation log documenting attempted refutations.

## Rule-ID Prefixes

- `ANA-`: Analysis orchestration, tier resolution, and `/analyze` rules (`ANALYSIS_GUIDES.md`)
- `PTD-`: Pattern detection, codebook, theme, and contradiction rules (`PATTERN-DETECTION_RULES.md`)
- `HYP-`: Hypothesis generation, competing alternatives, and test plan rules (`HYPOTHESIS_RULES.md`)
- `VAL-`: Evidence weighting, ACH audit trail, disconfirmation, and ranking rules (`VALIDATION_RULES.md`)
- `IL-`: Investigation log and state transition rules (`INVESTIGATION_LOG_RULES.md`)

## Folder Layout

```
analysis-methods/
├── SKILL.md
├── ANALYSIS_GUIDES.md
├── ANALYSIS_CHECKS.md
├── ANALYSIS_TEMPLATE.md
├── PATTERN-DETECTION_GUIDES.md
├── PATTERN-DETECTION_RULES.md
├── PATTERN-DETECTION_TEMPLATE.md
├── HYPOTHESIS_GUIDES.md
├── HYPOTHESIS_RULES.md
├── HYPOTHESIS_TEMPLATE.md
├── VALIDATION_GUIDES.md
├── VALIDATION_RULES.md
├── VALIDATION_TEMPLATE.md
├── INVESTIGATION_GUIDES.md
├── INVESTIGATION_LOG_RULES.md
└── INVESTIGATION_LOG_TEMPLATE.md
```
