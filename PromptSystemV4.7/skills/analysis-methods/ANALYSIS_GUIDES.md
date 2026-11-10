# Analysis Orchestration Guide

Read BEFORE executing multi-stage qualitative synthesis or deep analytical investigation with `/analyze` or Layer 2 stage workflows.

## 1. Purpose and Reader Outcome

After reading this GUIDE, you can orchestrate qualitative coding, pattern detection, abductive hypothesis generation, and evidence validation into C2 Validated Knowledge. You can resolve execution tiers, establish input provenance for non-C1 research, enforce sequential analytical discipline, execute devil's advocate reviews, formulate calibrated likelihood and confidence assessments without faux-precise labels, and record open research questions for Layer 1 loop-back without breaking workflow boundaries.

## 2. Orchestration Decisions in Working Order

Executing `/analyze` follows seven core orchestration decisions in the sequence below.

### Decision 1: Execution Tier Selection (`/analyze` Tier 2 vs Tier 3)

- **Question**: Which execution depth and prompt envelope governs the `/analyze` run?
- **Options**:
  - Tier 2 (reduced pipeline): single PROMPTS file (3-10 prompts) executing pattern detection, hypothesis generation, and validation without human pause; produces one `_Analysis.md` deliverable; ends with full VCRIV gate.
  - Tier 3 (full pipeline): three separate PROMPTS files (one per stage) writing into the same `_Analysis.md` deliverable; includes an adversarial devil's advocate prompt attacking top candidate hypotheses; pauses between prompt files for human review.
- **Criterion**: Default to Tier 2 for single research topic sets or standard C1 inputs. Escalate to Tier 3 when input encompasses a multi-approach research program (2+ `T##_` topic folders) or when the user explicitly passes `tier 3` (`DRSYNART-FR-02`). Single-turn analysis without a STRUT is not permitted; single-turn needs run as individual stage workflows (`/pattern-detect`, `/hypothesize`, `/validate`).
- **Source**: `_SPEC_IPPS_RESEARCH_AND_WRITING_TOOLS.md` Section 2.3 and FR-02.
- **Rule Reference**: `ANA-OR-01`.

### Decision 2: Input Provenance and Coding Pass

- **Question**: How is source provenance established when input material is not a C1 Knowledge Library?
- **Options**:
  - Inherited provenance: inherit finding claim IDs and `-02` source IDs directly from C1 Knowledge Library (`_INFO_[TOPIC]-IN01_Summary.md` and `_INFO_[TOPIC]-IN02_Sources.md`).
  - Generated provenance: run Decision 1 coding pass from `PATTERN-DETECTION_GUIDES.md` on raw notes, bundles, transcriptions, or chat text; extract findings into a six-field codebook; assign continuous finding IDs (`F-01`, `F-02`) and local source IDs.
- **Criterion**: If input is C1, inherit IDs to maintain cross-layer traceability. If input is non-C1 or raw material, always execute the S1 coding pass before thematic analysis (`DRSYNART-FR-12`, `DRSYNART-DD-04`). Record input provenance explicitly in the output header block (`DRSYNART-FR-03`).
- **Source**: `T01_RSRCHMTHD_ResearchToArticleMethods_2026-10-19/_INFO_RSRCHMTHD-01_Summary.md` Section S1; Saldana, *The Coding Manual for Qualitative Researchers*.
- **Rule Reference**: `ANA-OR-02`.

### Decision 3: Stage Progression Sequence

- **Question**: In what order do analytical operations execute?
- **Options**:
  - Strict pipeline: Pattern Detection (S2) -> Hypothesis Generation (S3) -> Validation and Ranking (S4).
  - Premature hypothesizing: leaping directly to hypothesis formulation or validation before coding findings or cataloging contradictions.
- **Criterion**: Always execute stages in strict order: map empirical findings into themes, contradictions, and gaps first; abduct competing hypotheses from observed tensions; then weight evidence and test disconfirmations. Never skip pattern detection; ungrounded hypothesis generation introduces confirmation bias (`DRSYNART-FR-13`).
- **Source**: `_SPEC_IPPS_RESEARCH_AND_WRITING_TOOLS.md` Section 4.3; MacQueen et al.; Braun and Clarke (2019).
- **Rule Reference**: `ANA-OR-03`.

### Decision 4: Human Review Points across Tiers

- **Question**: Where does human sign-off occur during execution?
- **Options**:
  - Tier 2 review point: zero human pauses inside the file; the run proceeds headlessly through all prompts to VCRIV completion; user reviews the finished `_Analysis.md` deliverable.
  - Tier 3 review points: execution halts between each stage's PROMPTS file (after Pattern Map completion, and after Hypothesis Register completion); user inspects stage findings and confirms or adjusts scope before the next prompt file launches.
- **Criterion**: Tier 2 runs without pause to minimize latency for focused analysis. Tier 3 pauses between stage files because long-running research synthesis requires user alignment on candidate hypotheses before committing validation compute (`DRSYNART-FR-13`, `DRSYNART-2.3`).
- **Source**: `_SPEC_IPPS_RESEARCH_AND_WRITING_TOOLS.md` Section 2.3 and FR-13.
- **Rule Reference**: `ANA-OR-04`.

### Decision 5: Devil's Advocate Execution (Tier 3 Only)

- **Question**: When and how is adversarial challenge injected into analysis?
- **Options**:
  - Standalone devil's advocate prompt at Tier 3: authors an explicit challenge targeting the top three ranking candidate hypotheses before final ranking; tests alternative explanations, searches refuting evidence, and stress-tests boundary conditions.
  - Omitted or passive review: relying solely on initial hypothesis generation.
- **Criterion**: Mandatory at Tier 3 (`DRSYNART-FR-13`, `DRSYNART-DD-04`). Attack the top three items before locking final ranks. Record all surviving and refuted arguments directly in the Validation Report.
- **Source**: U.S. Intelligence Community Tradecraft; Heuer, *Psychology of Intelligence Analysis*.
- **Rule Reference**: `ANA-OR-05`.

### Decision 6: Calibrated Likelihood and Confidence Prose Phrasing (DD-06)

- **Question**: How are probabilistic assertions and analytical certainty expressed?
- **Options**:
  - Prose phrases: Kent likelihood term (almost certain, highly likely, likely, roughly even chance, unlikely, highly unlikely, remote) paired with an independent prose confidence level (low, moderate, high).
  - Bracket labels or numeric percentages: `[LIKELY]`, `[CONFIDENT]`, `85%`.
- **Criterion**: Strictly use ICD-203 prose phrases (`DRSYNART-DD-06`). Never use bracket labels or faux-precise percentages for qualitative estimates. Likelihood (estimated probability of the statement being true) must always be stated separately from confidence (robustness, diversity, and disconfirmation rigor of the evidence base).
- **Source**: Office of the Director of National Intelligence, *ICD 203 Analytic Standards*; Sherman Kent, *Words of Estimative Probability*.
- **Rule Reference**: `ANA-OR-06`.

### Decision 7: Loop-Back to Layer 1 (Section 8.6)

- **Question**: How does analysis handle open items requiring further research?
- **Options**:
  - Loop-back recording: when an item carries low confidence and `exhausted: yes` in its disconfirmation log, formulate one targeted research question and record it in `ANALYSIS_TEMPLATE.md` section "Research Questions for Layer 1".
  - Autonomous research call: `/analyze` invoking `/research` or `/deep-research` automatically.
- **Criterion**: Always record open questions in the deliverable; never invoke Layer 1 workflows autonomously. The user or `/go` orchestrator decides whether to trigger targeted Layer 1 research based on recorded questions (`DRSYNART-8.6`).
- **Source**: `_SPEC_IPPS_RESEARCH_AND_WRITING_TOOLS.md` Section 8.6.
- **Rule Reference**: `ANA-OR-07`.

## 3. Named Failure Modes

- **Silent Tier Escalation** (`ANA-OR-01`): Workflow escalates to Tier 3 without declaring `Tier 3 - [reason]` on the first response line or plans more than 10 prompts in a Tier 2 PROMPTS file.
  - *Prevention*: Always evaluate input shape and emit tier declaration immediately; enforce NFR-01 prompt caps.
- **Missing Input Provenance** (`ANA-OR-02`): Analysis on raw or non-C1 input uses ad-hoc claim references without establishing a codebook or recording provenance in the header block.
  - *Prevention*: Check input type; if non-C1, execute the Decision 1 coding pass from `PATTERN-DETECTION_GUIDES.md` first.
- **Premature Hypothesizing** (`ANA-OR-03`): Leaping directly to hypothesis formulation without charting findings or identifying contradictions.
  - *Prevention*: Enforce strict pipeline order; every hypothesis must trace to at least one recorded theme, contradiction, or gap.
- **Unmanaged Pause or Skipped Sign-off** (`ANA-OR-04`): Pausing for human input inside a Tier 2 run, or failing to halt between PROMPTS files for user sign-off at Tier 3.
  - *Prevention*: Treat Tier 2 prompt files as autonomous sequences; enforce review checkpoints between files at Tier 3.
- **Omitted Devil's Advocate** (`ANA-OR-05`): Tier 3 analysis finalizes rankings without executing an adversarial challenge against the top three items.
  - *Prevention*: Verify the devil's advocate prompt exists and attacks the top three items before ranking compilation.
- **Bracketed or Numeric Likelihood Labels** (`ANA-OR-06`): Output uses labels like `[LIKELY]` or pseudo-precise numbers like `85%` instead of ICD-203 prose phrases.
  - *Prevention*: Write prose phrases: "It is likely that..." paired with "with moderate confidence".
- **Autonomous Layer Re-entry** (`ANA-OR-07`): `/analyze` invokes `/research` or `/deep-research` on open questions rather than recording them for user decision.
  - *Prevention*: Document questions in the "Research Questions for Layer 1" section; stop after VCRIV.

## 4. Quality Heuristics

1. **Traceable Lineage**: Every claim in the Analysis deliverable traces to a finding ID, and every finding traces to a source ID.
2. **Competing Rigor**: Every working hypothesis has at least one mutually exclusive rival or the null hypothesis and an explicit falsifier.
3. **Calibrated Distinction**: Likelihood (probability) and confidence (evidence strength) are distinct prose phrases; no two items share a rank without an explicit tie-break record.
4. **Audit Trail Independence**: The ACH matrix records consistency ratings as an audit trail and search director, never as an automated decision formula.
5. **Clean Boundaries**: Open empirical gaps are recorded as Layer 1 research questions without triggering external research calls.

## 5. Self-Review Questions

1. Does the first response line declare `Tier N - [reason]` matching input scope? (`ANA-OR-01`)
2. Does the header block record input provenance and trace all findings to source IDs? (`ANA-OR-02`)
3. Did the analysis execute in strict order: Pattern Detection -> Hypotheses -> Validation? (`ANA-OR-03`)
4. Did Tier 2 run without human pause, or did Tier 3 provide review points between prompt files? (`ANA-OR-04`)
5. If running at Tier 3, did a devil's advocate prompt attack the top three candidate hypotheses? (`ANA-OR-05`)
6. Are likelihood and confidence expressed as ICD-203 prose phrases rather than bracket labels or percentages? (`ANA-OR-06`)
7. Are open items with exhausted searches recorded under "Research Questions for Layer 1" rather than triggering automatic research calls? (`ANA-OR-07`)

## 6. Annotated Exemplar Links

- `T01_RSRCHMTHD_ResearchToArticleMethods_2026-10-19/_INFO_RSRCHMTHD-01_Summary.md [DRSYNART-RSRCHMTHD-IN01]`: Demonstrates cross-document qualitative synthesis, method chaining, and ICD-203 vocabulary calibration.
- `T01_RSRCHMTHD_ResearchToArticleMethods_2026-10-19/_INFO_RSRCHMTHD-03_Terminology.md [DRSYNART-RSRCHMTHD-IN03]`: Definitive glossary establishing single names for all 74 pipeline concepts.

## 7. Binding Vocabulary and Glossary Pointer

All analysis stages adhere to the 74 binding terms established in `_INFO_RSRCHMTHD-03_Terminology.md [DRSYNART-RSRCHMTHD-IN03]`. Core terms utilized across stages include:

- **Finding**: Discrete empirical observation extracted from source material with source ID and verification label.
- **Code**: Descriptive tag assigned to a finding in the six-field codebook.
- **Theme**: Unified pattern of meaning connecting findings from two or more independent sources.
- **Contradiction**: Direct empirical or logical conflict between two findings, recorded with both source IDs.
- **Evidence Gap**: Missing observation or empty findings matrix column required to answer the research question.
- **Hypothesis**: Testable declarative explanation abducted from observed patterns or contradictions.
- **Rival Hypothesis**: Mutually exclusive alternative explanation competing for the same phenomenon.
- **Falsifier**: Observable condition that refutes the hypothesis if detected.
- **Crucial Test**: Empirical search or test capable of decisively ruling out one or more competing hypotheses.
- **Toulmin Warrant**: Explicit logical bridge explaining why an item of evidence supports or refutes a hypothesis.
- **GRADE Certainty**: Four-level rating (high, moderate, low, very low) evaluating consistency and risk of bias across the body of evidence.
- **ACH Matrix**: Analysis of Competing Hypotheses matrix tracking diagnostic consistency; acts as audit trail and search director, never as the decision rule.
- **Disconfirmation Log**: Ledger recording what refuting evidence was searched, where, and whether attempts were exhausted.
- **Kent Likelihood**: Standard ICD-203 seven-tier prose probability term: almost certain (>95%), highly likely (80-95%), likely (55-80%), roughly even chance (45-55%), unlikely (20-45%), highly unlikely (5-20%), remote (<5%).
- **Confidence Level**: Independent three-tier prose assessment (high, moderate, low) reflecting evidence diversity, quality, and disconfirmation rigor.
