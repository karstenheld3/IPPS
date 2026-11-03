# Hypothesis Rules

Verification rules for hypothesis register artifacts produced with `/hypothesize` or during stage S3 of `/analyze`.

Writing quality: Apply `APAPALAN_RULES.md` and `MECT_WRITING_RULES.md`. Key rules: AP-PR-07 (be specific), AP-PR-05 (referenceable IDs), MW-VO-01 (active voice), MW-WC-02 (plain language).

## Rule Index

Form & Statement (FM / ST)
- HYP-FM-01: Standard hypothesis form classification
- HYP-ST-01: Explanatory statement requirements and theme differentiation

Diversity & Competition (DV / RV)
- HYP-DV-01: Candidate count (3-7 range) and set diversity standards
- HYP-RV-01: Mandatory rival or null hypothesis pairing

Falsification & Testing (FL / TP)
- HYP-FL-01: Explicit falsifier and refutation criteria
- HYP-TP-01: Actionable crucial test plan specification

Likelihood & Calibration (LK)
- HYP-LK-01: Calibrated ICD-203 prose likelihood phrasing

## HYP-FM-01: Standard Hypothesis Form Classification

Every hypothesis entry must specify its logical form as one of the four standard types: Causal, Correlational, Categorical, or Predictive.

Artifact check: Verify every entry under `## Hypothesis Register` specifies `Form:` containing one of: `Causal`, `Correlational`, `Categorical`, or `Predictive`.

**BAD:**
```markdown
### Hypothesis Entry: H-01

- Statement: Gateway latency spikes during configuration updates.
- Form: General observation
```

**GOOD:**
```markdown
### Hypothesis Entry: H-01

- Statement: Configuration reload scripts trigger thread lock contention on shared memory caches, blocking requests for over 3 seconds.
- Form: Causal (lock contention mechanism produces thread blockage)
```

## HYP-ST-01: Explanatory Statement Requirements and Theme Differentiation

Every hypothesis statement must assert a causal mechanism, associative relationship, categorical property, or predictive outcome. A hypothesis must not simply restate an empirical theme from stage S2.

Artifact check: Verify the hypothesis statement proposes an explanation or prediction beyond repeating the title or synthesis text of its prompt theme.

**BAD:**
```markdown
### Hypothesis Entry: H-01

- Prompted by: Theme 1 (Edge Invalidation Fragility)
- Statement: Distributed edge caches experience cascading invalidation stalls during updates.
```

**GOOD:**
```markdown
### Hypothesis Entry: H-01

- Prompted by: Theme 1 (Edge Invalidation Fragility)
- Statement: Schema updates force synchronous cryptographic key re-negotiation across edge nodes, exhausting thread pools and causing cascading invalidation stalls.
```

## HYP-DV-01: Candidate Count (3-7 Range) and Set Diversity Standards

The hypothesis register must contain between 3 and 7 mutually exclusive candidate hypotheses per research question. At least one candidate in each set must contradict the dominant theme or reject a core assumption from the Key Assumptions Check.

Artifact check: Verify the number of hypotheses per research question is between 3 and 7 inclusive, and verify that at least one candidate asserts an alternative mechanism opposing the primary theme.

**BAD:**
```markdown
## Research Question: RQ-02

- H-01: Lock contention causes gateway stalls.
- H-02: Mutex locking delays gateway requests.
```

**GOOD:**
```markdown
## Research Question: RQ-02

- H-01: Lock contention in shared memory causes thread blockage during reload.
- H-02: Network packet loss during reload causes client retry storms, saturating network interfaces.
- H-03: Downstream database query queuing creates artificial backpressure, independent of gateway reload operations.
```

## HYP-RV-01: Mandatory Rival or Null Hypothesis Pairing

Every candidate hypothesis must explicitly name at least one mutually exclusive rival hypothesis (`H-NN`) within the same set or designate the null hypothesis (`H-00`). Competing hypotheses must not be capable of both being true simultaneously.

Artifact check: Verify every hypothesis entry contains a `Rival hypothesis:` field citing a valid `H-NN` identifier or explicit null hypothesis.

**BAD:**
```markdown
### Hypothesis Entry: H-01

- Statement: Edge cache lock contention delays client request processing.
- Rival hypothesis: None
```

**GOOD:**
```markdown
### Hypothesis Entry: H-01

- Statement: Edge cache lock contention delays client request processing.
- Rival hypothesis: H-02 (External network latency, not internal cache locking, causes client delays)
```

## HYP-FL-01: Explicit Falsifier and Refutation Criteria

Every hypothesis must specify a concrete, observable empirical finding or measurable threshold that would decisively refute it if detected.

Artifact check: Verify every hypothesis entry contains a `Falsifier:` field specifying an observable condition capable of refuting the claim.

**BAD:**
```markdown
### Hypothesis Entry: H-01

- Falsifier: The hypothesis is false if performance does not improve.
```

**GOOD:**
```markdown
### Hypothesis Entry: H-01

- Falsifier: Kernel telemetry demonstrates thread queue wait times remain below 50 ms during peak configuration reload cycles.
```

## HYP-TP-01: Actionable Crucial Test Plan Specification

Every hypothesis must define crucial test plan rows detailing target evidence, search venue (local files, transcripts, or targeted queries), and decisive exclusion conditions that eliminate at least one competitor.

Artifact check: Verify test plan rows exist for each hypothesis and specify target evidence, search venue, and decisive exclusion criteria.

**BAD:**
```markdown
### Crucial Test: H-01

- Test: Look into log files to see what happened.
```

**GOOD:**
```markdown
### Crucial Test: H-01 vs H-02

- Target evidence: Kernel lock trace logs during synthetic configuration reload.
- Search venue: Local telemetry logs in `_SOURCES/CORP-SC-OPS-01_traces.json`.
- Decisive exclusion condition: If thread wait states occur in `net_rx` rather than `mutex_lock`, H-01 is refuted and H-02 is supported.
- Cruciality: High (decisively discriminates between internal lock contention and external network partition).
```

## HYP-LK-01: Calibrated ICD-203 Prose Likelihood Phrasing

Prior likelihood must be expressed strictly as an ICD-203 prose phrase (almost certain, highly likely, likely, roughly even chance, unlikely, highly unlikely, remote). Bracketed labels and pseudo-precise numeric percentages are prohibited.

Artifact check: Verify `Prior likelihood:` contains a valid ICD-203 prose phrase and contains zero bracket labels (such as `[LIKELY]`) and zero percentage numbers.

**BAD:**
```markdown
### Hypothesis Entry: H-01

- Prior likelihood: [LIKELY] 75%
```

**GOOD:**
```markdown
### Hypothesis Entry: H-01

- Prior likelihood: Roughly even chance (prose phrase per ICD-203)
```
