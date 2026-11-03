# Validation Rules

Verification rules for validation artifacts produced with `/validate` or during stage S4 of `/analyze`.

Writing quality: Apply `APAPALAN_RULES.md` and `MECT_WRITING_RULES.md`. Key rules: AP-PR-07 (be specific), AP-PR-05 (referenceable IDs), MW-VO-01 (active voice), MW-WC-02 (plain language).

## Rule Index

Input & Search (IN / SR)
- VAL-IN-01: Input flexibility and statement ingestion
- VAL-SR-01: Multi-tier evidence search

Weighting & Audit Trail (WT / AC)
- VAL-WT-01: Two-layer evidence weighting (GRADE certainty and Toulmin warrants)
- VAL-AC-01: ACH matrix audit trail standards

Disconfirmation & Evidence Thresholds (DC / PR)
- VAL-DC-01: Exhaustive disconfirmation logging and search exhaustion
- VAL-PR-01: Evidence thresholds for proven and refuted ranks

Ranking & Phrasing (RK / LK)
- VAL-RK-01: Strict 0-8 ranking scale and deterministic tie-breaking
- VAL-LK-01: Calibrated ICD-203 prose likelihood and independent confidence phrasing

Layer Loop-Back (LP)
- VAL-LP-01: Layer 1 loop-back research question recording

## VAL-IN-01: Input Flexibility and Statement Ingestion

The validation artifact must accept candidate hypotheses from a structured register (`H-NN`) or bare empirical statements, assigning referenceable IDs to each ingested statement before validation.

Artifact check: Verify every entry under `## Items` carries an identifier (`H-NN` or continuous index) and a clear claim statement.

**BAD:**
```markdown
## Items

We received some claims from the team about database caching and network issues.
```

**GOOD:**
```markdown
## Items

- H-01: Configuration reload scripts trigger thread lock contention on shared memory caches, blocking requests for over 3 seconds.
- H-02: External network packet loss during reload causes client retry storms, saturating network interfaces.
```

## VAL-SR-01: Multi-Tier Evidence Search

Evidence collection must search local workspace documents and transcriptions first before executing targeted external web searches or empirical code tests.

Artifact check: Verify search records and test citations indicate local source checks prior to external web queries.

**BAD:**
```markdown
### Search Log: H-01

- Search: Ran 15 general web queries on search engine to see how databases handle locks.
```

**GOOD:**
```markdown
### Search Log: H-01

- Local search: Inspected `_SOURCES/CORP-SC-OPS-01_traces.json` (found 4 diagnostic trace events).
- External fallback: None required; local evidence settles lock contention mechanism.
```

## VAL-WT-01: Two-Layer Evidence Weighting (GRADE Certainty and Toulmin Warrants)

Validation must evaluate evidence at two distinct layers: an overall GRADE certainty rating (high, moderate, low, very low) with downgrade factors per hypothesis, and a Toulmin warrant explaining the specific diagnostic link for each evidence finding.

Artifact check: Verify `## Evidence Weights` contains both Toulmin warrants for diagnostic links and GRADE certainty assessments with downgrade rationale for each hypothesis.

**BAD:**
```markdown
### Evidence Weight: H-01

- Supporting finding: F-04 proves H-01 because it was found in the logs.
- Overall weight: Strong.
```

**GOOD:**
```markdown
### Evidence Weight: H-01 x F-04

- Hypothesis: H-01
- Grounds: F-04 (Kernel traces measure 3.8s thread stalls during distributed lock renegotiation)
- Toulmin Warrant: Thread stalls occurring specifically during lock renegotiation demonstrate that shared memory contention is the direct mechanism producing transaction delays.
- Polarity: Consistent
- Diagnosticity: High

### Hypothesis Certainty: H-01

- Inconsistencies: 0 of 6 diagnostic findings
- GRADE Certainty: Moderate (downgraded once for imprecision: fewer than 5 independent cluster traces)
```

## VAL-AC-01: ACH Matrix Audit Trail Standards

The Analysis of Competing Hypotheses matrix must record consistency ratings (Consistent, Inconsistent, Not Applicable) as an audit trail and search director, never as an automated arithmetic verdict.

Artifact check: Verify the ACH matrix lists hypotheses as columns/items and findings as rows with C/I/NA ratings, accompanied by analytical commentary rather than mechanical minus-summing verdicts.

**BAD:**
```markdown
### ACH Matrix Results

H-01 had 1 minus and H-02 had 3 minuses, so H-01 is mathematically declared the winner.
```

**GOOD:**
```markdown
### ACH Matrix (Audit Trail)

- Finding F-04 (Lock contention traces):
  - H-01: Consistent (directly supports shared memory lock contention)
  - H-02: Inconsistent (shows delay occurs in kernel mutex, not network interface)
- Audit Note: Inconsistency with H-02 directs disconfirmation search DL-03; matrix serves as audit trail, not automated scoring verdict.
```

## VAL-DC-01: Exhaustive Disconfirmation Logging and Search Exhaustion

Every hypothesis ranked above `refuted` must undergo at least one explicit disconfirmation attempt recorded in the disconfirmation log, specifying the predicted observation searched and an explicit `exhausted: yes` or `exhausted: no` flag.

Artifact check: Verify every hypothesis with rank > 0 has at least one corresponding entry in `## Disconfirmation Log` containing an explicit `Exhausted: Yes` or `Exhausted: No` field.

**BAD:**
```markdown
### Disconfirmation Log

We checked our assumptions and found no reason to doubt H-01.
```

**GOOD:**
```markdown
### Disconfirmation Log: DL-01

- Hypothesis: H-01
- Predicted observation: Thread queue wait times should remain below 50 ms during reload if H-01 is false.
- Search query: "thread_wait_ms < 50" in local trace logs.
- Result: Zero events matched; all measured stalls exceeded 1,200 ms.
- Matrix cell update: Consistent
- Exhausted: Yes
```

## VAL-PR-01: Evidence Thresholds for Proven and Refuted Ranks

A rank of 8 (`proven`) strictly requires `[PROVEN]` or `[TESTED]` evidence. A rank of 0 (`refuted`) strictly requires citing the specific refuting evidence ID from the disconfirmation log or findings list.

Artifact check: Verify any hypothesis ranked as `proven` cites `[PROVEN]` or `[TESTED]` test artifacts, and any hypothesis ranked as `refuted` cites a specific refuting finding or `DL-NN` identifier.

**BAD:**
```markdown
1. H-01 (Rank 8 - Proven)
   - Evidence: Supported by several articles and industry blog posts.
2. H-02 (Rank 0 - Refuted)
   - Evidence: Disproved by the team during review.
```

**GOOD:**
```markdown
1. H-01 (Rank 8 - Proven)
   - Evidence: Verified by benchmark run CORP-SC-BENCH-01 [TESTED] and trace analysis F-04 [PROVEN].
2. H-02 (Rank 0 - Refuted)
   - Evidence: Decisively refuted by packet trace analysis in DL-03 (zero dropped packets during stall).
```

## VAL-RK-01: Strict 0-8 Ranking Scale and Deterministic Tie-Breaking

All hypotheses must be ranked on the standard 0-8 scale (`refuted` < Kent ICD-203 terms < `proven`). No two hypotheses may share the same rank position; ties must be broken deterministically (higher confidence first, then higher evidence weight) with the tie-break explicitly recorded.

Artifact check: Verify every ranked item occupies a unique position in `## Ranking` (1, 2, 3...) with an assigned 0-8 scale score, and verify any identical scores carry an explicit `Tie-break:` rationale.

**BAD:**
```markdown
## Ranking

- H-01: Rank 6 (Highly likely)
- H-03: Rank 6 (Highly likely)
- H-02: Rank 0 (Refuted)
```

**GOOD:**
```markdown
## Ranking

1. H-01 (Scale Position: 6 - Highly likely; Analytic Confidence: Moderate confidence)
   - Tie-break: Outranks H-03 due to higher GRADE certainty (moderate vs low).
2. H-03 (Scale Position: 6 - Highly likely; Analytic Confidence: Low confidence)
   - Tie-break: Placed second due to lower evidence diversity.
3. H-02 (Scale Position: 0 - Refuted)
   - Refuting evidence ID: DL-03
```

## VAL-LK-01: Calibrated ICD-203 Prose Likelihood and Independent Confidence Phrasing

Likelihood (remote, highly unlikely, unlikely, roughly even chance, likely, highly likely, almost certain) and analytic confidence (low, moderate, high) must be expressed as separate, standard prose phrases. Bracketed labels and pseudo-precise numeric percentages are strictly prohibited.

Artifact check: Verify `## Ranking` contains separate prose phrases for likelihood and confidence, and contains zero bracket labels (such as `[LIKELY]`) and zero percentage values.

**BAD:**
```markdown
- H-01: [LIKELY] [CONFIDENCE: HIGH] (85% certainty)
```

**GOOD:**
```markdown
- H-01: It is highly likely that shared memory contention causes gateway reload stalls, assessed with moderate confidence based on trace telemetry.
```

## VAL-LP-01: Layer 1 Loop-Back Research Question Recording

Any hypothesis evaluated with low confidence and `exhausted: yes` in its disconfirmation log must be recorded as a targeted research question in `## Research Questions for Layer 1`. Validation workflows must never execute Layer 1 research calls autonomously.

Artifact check: Verify `## Research Questions for Layer 1` lists targeted research questions for unsettled hypotheses, and verify no autonomous research execution is triggered.

**BAD:**
```markdown
## Research Questions for Layer 1

None. The agent ran web searches automatically to fill in all missing answers.
```

**GOOD:**
```markdown
## Research Questions for Layer 1

- RQ-05: What is the maximum throughput threshold where edge gateway queue contention transitions from linear delay to catastrophic thread exhaustion?
  - Prompted by: H-03 (low confidence, disconfirmation exhausted)
  - Recommended Layer 1 action: Targeted deep research query over synthetic load benchmarks.
```
