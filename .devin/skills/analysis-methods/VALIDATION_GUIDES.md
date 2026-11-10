# Validation and Evidence Weighting Guide

Read BEFORE validating hypotheses, weighting evidence, constructing ACH matrices, executing disconfirmation searches, or ranking analytical claims with `/validate` or during stage S4 of `/analyze`.

## 1. Purpose and Reader Outcome

After reading this GUIDE, you can validate any set of hypotheses or empirical statements and rank them on a single comparable 0-8 scale from refuted to proven. You can execute local-first evidence searches with web and test fallbacks, apply a two-layer weighting scheme (GRADE certainty and Toulmin warrants), use the Analysis of Competing Hypotheses (ACH) matrix strictly as an audit trail, log exhaustive disconfirmation attempts, eliminate tied ranks deterministically, state likelihood and confidence in distinct ICD-203 prose phrases, and record open items as Layer 1 research questions without breaking layer boundaries.

## 2. Validation Decisions in Working Order

Executing validation follows eight core analytical decisions in the sequence below.

### Decision 1: Input Material Ingestion

- **Question**: What input material is accepted for validation?
- **Options**:
  - Structured hypothesis register: ingesting candidate entries (`H-01`, `H-02`) directly from stage S3.
  - Bare empirical statements: ingesting arbitrary candidate assertions from notes, user prompts, conversation context, or external reports (`DRSYNART-DD-04`).
- **Criterion**: Accept both input types. When input is a structured register, inherit existing IDs, prompt links, and falsifiers. When input is a bare list of statements, assign continuous IDs (`H-01`, `H-02`), extract their underlying claims, and infer the null hypothesis for each before testing (`VAL-IN-01`).
- **Source**: `_SPEC_IPPS_RESEARCH_AND_WRITING_TOOLS.md` Section 4.3 and DD-04.
- **Rule Reference**: `VAL-IN-01`.

### Decision 2: Multi-Tier Evidence Search

- **Question**: Where and how is diagnostic evidence collected?
- **Options**:
  - Local-first sequential search: search local workspace files, session notes, and transcriptions first; execute targeted web search queries whenever local material fails to settle an item; run automated scripts or code tests where the item is empirically testable.
  - Local-only passive search: relying solely on whatever findings happen to be in the immediate prompt.
  - Unbounded web search: executing broad external queries before checking existing local assets.
- **Criterion**: Always search locally first. If local evidence is non-diagnostic or incomplete, escalate to targeted web search or run empirical tests at every tier (`DRSYNART-FR-16`). Web queries must be targeted specifically to confirm or refute predicted observations.
- **Source**: `T01_RSRCHMTHD_ResearchToArticleMethods_2026-10-19/_INFO_RSRCHMTHD-08_CompetingHypothesesAndDisconfirmation.md` Section RQ-17.
- **Rule Reference**: `VAL-SR-01`.

### Decision 3: Two-Layer Evidence Weighting

- **Question**: How is evidence strength and certainty evaluated across findings?
- **Options**:
  - Two-layer hybrid weighting: GRADE-style certainty rating (high, moderate, low, very low) evaluating the whole body of evidence behind each hypothesis, combined with a Toulmin warrant explaining the specific diagnostic relevance of each individual finding link.
  - Bayesian likelihood ratios: computing subjective probability products across cells.
  - Source-tier weighting alone: judging claims purely by domain authority of the source URL.
- **Criterion**: Apply both layers (`DRSYNART-FR-16`). Plain source tiers rate the container, not the claim. Bayesian ratios require hundreds of uncalibrated guesses. Toulmin warrants explain *why* evidence bears on a claim, while GRADE evaluates overall body consistency and risk of bias (`VAL-WT-01`).
- **Source**: `T01_RSRCHMTHD_ResearchToArticleMethods_2026-10-19/_INFO_RSRCHMTHD-09_EvidenceWeightingAndConfidence.md` Section RQ-16; Schuenemann et al. (2013); Toulmin (1958).
- **Rule Reference**: `VAL-WT-01`.

### Decision 4: ACH Matrix as Audit Trail

- **Question**: What role does the Analysis of Competing Hypotheses matrix play in validation?
- **Options**:
  - Audit trail and search director: mapping findings across hypotheses to identify non-diagnostic rows, track inconsistencies, and direct searches toward discriminating items.
  - Automated verdict calculator: mechanically summing minuses and letting the lowest minus score dictate the winner.
- **Criterion**: Treat the ACH matrix strictly as an audit trail and search director (`DRSYNART-FR-16`). Controlled trials prove that mechanical ACH does not reduce confirmation bias (Dhami 2019). The matrix reveals what remains un-tested; the analyst and evidence weights decide the conclusion (`VAL-AC-01`).
- **Source**: `T01_RSRCHMTHD_ResearchToArticleMethods_2026-10-19/_INFO_RSRCHMTHD-08_CompetingHypothesesAndDisconfirmation.md` Section RQ-15; Heuer (1999); Dhami et al. (2019).
- **Rule Reference**: `VAL-AC-01`.

### Decision 5: Disconfirmation Logging and Search Exhaustion

- **Question**: How are refutation attempts documented?
- **Options**:
  - Typed disconfirmation log with exhaustion flag: recording every query, search venue, observed result, and explicit `exhausted: yes/no` flag.
  - Passive absence logging: assuming that lack of finding implies disproof without recording query scope.
- **Criterion**: Every candidate hypothesis above `refuted` must undergo at least one explicit disconfirmation search documented in the disconfirmation log (`DRSYNART-FR-16`). Mark `exhausted: yes` only when both local files and targeted external queries return zero additional diagnostic findings (`VAL-DC-01`).
- **Source**: `T01_RSRCHMTHD_ResearchToArticleMethods_2026-10-19/_INFO_RSRCHMTHD-08_CompetingHypothesesAndDisconfirmation.md` Sections RQ-17 and RQ-20; Platt (1964).
- **Rule Reference**: `VAL-DC-01`.

### Decision 6: Ranking on the 0-8 Scale and Tie-Breaking

- **Question**: How are validated items scored, ordered, and expressed?
- **Options**:
  - Standard 0-8 ranking scale: mapping claims to 0 (`refuted`), 1-7 (Kent ICD-203 likelihood terms in ascending order), or 8 (`proven`); breaking ties deterministically by confidence level, then evidence weight; expressing likelihood and confidence as distinct prose phrases.
  - Floating percentage score: assigning arbitrary percentages (e.g. 78.4%) or bracketed tags (`[CONFIDENT]`).
- **Criterion**: Enforce the Section 8.6 scale strictly (`DRSYNART-8.6`, `DRSYNART-DD-06`):
  - Scale positions: 0 (`refuted`), 1 (`remote`), 2 (`highly unlikely`), 3 (`unlikely`), 4 (`roughly even chance`), 5 (`likely`), 6 (`highly likely`), 7 (`almost certain`), 8 (`proven`).
  - No two items may share a rank. Ties are broken first by higher confidence level (high > moderate > low), then by higher evidence weight; every tie-break must be explicitly recorded (`VAL-RK-01`).
  - `proven` strictly requires `[PROVEN]` or `[TESTED]` evidence. `refuted` strictly requires citing the refuting evidence ID (`VAL-PR-01`).
  - Likelihood and confidence must be distinct prose phrases, never bracket labels (`VAL-LK-01`).
- **Source**: `_SPEC_IPPS_RESEARCH_AND_WRITING_TOOLS.md` Section 8.6; ICD 203 Analytic Standards; Kent (1964).
- **Rule Reference**: `VAL-RK-01`, `VAL-LK-01`, `VAL-PR-01`.

### Decision 7: Open Items and Layer 1 Loop-Back

- **Question**: How are un-settled hypotheses handled?
- **Options**:
  - Loop-back recording: when an item carries low confidence and `exhausted: yes` in the disconfirmation log, formulate one targeted research question and record it in `Research Questions for Layer 1`.
  - Autonomous research execution: `/validate` calling `/research` or `/deep-research` automatically.
- **Criterion**: Always record open questions in the deliverable section; never call Layer 1 workflows autonomously (`DRSYNART-8.6`). The user or `/go` orchestrator determines whether to launch targeted Layer 1 research (`VAL-LP-01`).
- **Source**: `_SPEC_IPPS_RESEARCH_AND_WRITING_TOOLS.md` Section 8.6.
- **Rule Reference**: `VAL-LP-01`.

### Decision 8: Writing Implications for Layer 3

- **Question**: How does validated knowledge hand over to deliverable authoring?
- **Options**:
  - Actionable writing implications: documenting surviving hypotheses, their rank order, core Toulmin warrants, and recommended structural placement for Layer 3 workflows (`/propose-*`, `/write-*`).
  - Raw matrix handover: passing raw table minuses without narrative translation.
- **Criterion**: Author an explicit "Writing Implications" section. Identify the primary thesis (highest-ranking survivor), alternative perspectives to acknowledge, and key counter-arguments to address in deliverable drafting.
- **Source**: `_SPEC_IPPS_RESEARCH_AND_WRITING_TOOLS.md` Section 4.3 and Section 8.6.
- **Rule Reference**: `VAL-RK-01`, `VAL-WT-01`.

## 3. Annotated Excerpts

### Annotated Excerpt 1: Weighted Evidence Link with Toulmin Warrant and GRADE Certainty

```markdown
### Evidence Weight: H-01 x F-04

- Hypothesis: H-01 (Shared memory lock contention causes gateway reload stalls)
- Grounds: F-04 (Kernel traces measure 3.8s thread stalls during distributed lock renegotiation)
- Source: CORP-SC-OPS-01 (Tier 1, audit timestamp 2026-03-15) [VERIFIED]
- Toulmin Warrant: Thread stalls occurring specifically during lock renegotiation demonstrate that shared memory contention is the direct mechanism producing transaction delays.
- Polarity: Consistent
- Diagnosticity: High (discriminates H-01 from network partition hypothesis H-02)

### Hypothesis Certainty: H-01

- Inconsistencies: 0 of 6 diagnostic findings
- GRADE Certainty: Moderate (downgraded once for imprecision: fewer than 5 independent cluster traces)
- Overall Likelihood: Highly likely (prose phrase per ICD-203)
- Analytic Confidence: Moderate confidence (prose phrase per ICD-203)
```

*What makes this work*: Grounds link to verified empirical findings, the Toulmin warrant explains the logical bridge, and GRADE certainty tracks downgrade rationale transparently.

### Annotated Excerpt 2: Disconfirmation Log and Ranked Output with Tie-Break

```markdown
### Disconfirmation Log: DL-03

- Hypothesis: H-02 (External network partition causes gateway reload stalls)
- Predicted observation: Network interface packet drop counters should spike during reload stalls.
- Search query: "drop_rx" OR "retransmit" across telemetry logs in `_sources/CORP-SC-OPS-01_traces.json`.
- Result: Retransmit counters remained flat (<0.01%) during stall window.
- Matrix cell update: Inconsistent (refuting observation)
- Search scope: Local traces + 1 targeted gateway benchmark
- Exhausted: Yes

### Ranked Findings

1. H-01 (Rank 6 - Highly likely, with moderate confidence)
   - Tie-break: Outranks H-03 due to higher GRADE certainty (moderate vs low).
2. H-03 (Rank 6 - Highly likely, with low confidence)
   - Tie-break: Placed below H-01 due to lower evidence diversity.
3. H-02 (Rank 0 - Refuted)
   - Refuting evidence ID: DL-03 (Packet drop retransmits flat during stall).
```

*What makes this work*: Disconfirmation actively searches for refutation and logs exhaustion. Ranks use the 0-8 scale, break ties deterministically, and express likelihood and confidence in distinct prose phrases.

## 4. Named Failure Modes

- **Confirmation-Only Search** (`VAL-SR-01`): Searching only for evidence that confirms the leading hypothesis while ignoring predictions that would disprove it.
  - *Prevention*: Enforce the disconfirmation log; require every candidate above `refuted` to execute at least one refutation search.
- **ACH Score Used as Verdict** (`VAL-AC-01`): Treating the ACH minus count as an automatic calculation that decides the winner without evaluating warrant quality.
  - *Prevention*: Use ACH strictly as an audit trail; require explicit Toulmin warrants and GRADE certainty evaluations for ranking.
- **Tied Ranks in Final Order** (`VAL-RK-01`): Leaving two hypotheses at the same rank position without breaking the tie.
  - *Prevention*: Break ties deterministically: higher confidence wins first, then higher evidence weight; document the tie-break explicitly.
- **Merged or Bracketed Likelihood and Confidence** (`VAL-LK-01`): Writing `[LIKELY]` or mixing confidence into probability (e.g. "we are 80% confident it is true").
  - *Prevention*: State likelihood and confidence as separate prose phrases: "It is likely that..." paired with "with moderate confidence".
- **Proven Claim Without Tested Evidence** (`VAL-PR-01`): Assigning Rank 8 (`proven`) to a hypothesis supported only by observational citations or assumptions.
  - *Prevention*: Require `[PROVEN]` or `[TESTED]` evidence to grant Rank 8; otherwise cap ranking at Rank 7 (`almost certain`).
- **Autonomous Layer Re-entry** (`VAL-LP-01`): Triggering `/research` or `/deep-research` automatically during validation instead of recording questions in the deliverable.
  - *Prevention*: Record open items in the "Research Questions for Layer 1" section; halt execution after VCRIV.

## 5. Quality Heuristics

1. **Active Disconfirmation**: Every surviving hypothesis has at least one recorded search attempting to refute it.
2. **Dual-Layer Justification**: Every diagnostic link has a Toulmin warrant, and every hypothesis has a GRADE certainty rating with clear downgrade factors.
3. **Strict Monotonic Ordering**: Every item occupies a unique rank from 0 to 8; zero tied ranks exist in final output.
4. **Prose Precision**: Likelihood and confidence are expressed in standard ICD-203 prose phrases with zero bracket labels or percentages.
5. **Auditable Lineage**: Every refuted item cites its refuting evidence ID, and every proven item cites tested or proven evidence.

## 6. Self-Review Questions

1. Did the validation search local assets first before escalating to web search or tests? (`VAL-SR-01`)
2. Does every diagnostic evidence link carry an explicit Toulmin warrant explaining its relevance? (`VAL-WT-01`)
3. Is overall body certainty evaluated using GRADE criteria with transparent downgrade reasons? (`VAL-WT-01`)
4. Is the ACH matrix used strictly as an audit trail rather than an automated scoring verdict? (`VAL-AC-01`)
5. Does every hypothesis above `refuted` have an active refutation attempt logged with an `exhausted` flag? (`VAL-DC-01`)
6. Does every item occupy a unique rank on the 0-8 scale with all ties broken and documented? (`VAL-RK-01`)
7. Are likelihood and confidence expressed as separate prose phrases rather than bracket labels or percentages? (`VAL-LK-01`)
8. Does Rank 8 (`proven`) cite only `[PROVEN]` or `[TESTED]` evidence, and does Rank 0 (`refuted`) cite its refuting ID? (`VAL-PR-01`)
9. Are open items recorded as Layer 1 research questions rather than triggering autonomous research calls? (`VAL-LP-01`)

## 7. RULES References

Verification standards for validation artifacts are enforced by `VALIDATION_RULES.md` across the following rule groups:
- `VAL-IN-01`: Input flexibility and statement ingestion standards.
- `VAL-SR-01`: Multi-tier evidence search requirements.
- `VAL-WT-01`: Two-layer evidence weighting (GRADE certainty and Toulmin warrants).
- `VAL-AC-01`: ACH matrix audit trail standards.
- `VAL-DC-01`: Disconfirmation logging and search exhaustion standards.
- `VAL-RK-01`: Strict 0-8 ranking scale and deterministic tie-breaking.
- `VAL-LK-01`: Calibrated ICD-203 prose likelihood and independent confidence phrasing.
- `VAL-PR-01`: Evidence thresholds for proven and refuted ranks.
- `VAL-LP-01`: Layer 1 loop-back research question recording.
