# Hypothesis Generation Guide

Read BEFORE generating candidate hypotheses, identifying rival explanations, defining falsifiers, or constructing test plans with `/hypothesize` or during stage S3 of `/analyze`.

## 1. Purpose and Reader Outcome

After reading this GUIDE, you can abduct 3-7 testable, competing working hypotheses from themes, open contradictions, and evidence gaps. You can classify each hypothesis into its standard logical form, ensure mutual exclusivity, bind each candidate to an explicit rival or null hypothesis, define observable falsification conditions, state calibrated prior likelihoods in ICD-203 prose, and author crucial test plans that enable stage S4 to validate or refute claims rigorously.

## 2. Hypothesis Generation Decisions in Working Order

Executing hypothesis generation follows six core analytical decisions in the sequence below.

### Decision 1: Hypothesis Form Selection

- **Question**: What logical structure governs the explanatory statement?
- **Options**:
  - Causal: asserts that mechanism M produces effect Y from cause X ("X produces Y via M").
  - Correlational: asserts that variable X and variable Y systematically vary together without asserting directionality.
  - Categorical: asserts that entity X belongs to class C possessing distinct properties P.
  - Predictive: asserts that under specific future condition C, observable outcome O will occur.
- **Criterion**: Match form to the underlying research question (`DRSYNART-FR-15`):
  - If the question asks *why* or *how*: use Causal.
  - If the question asks *whether factors associate*: use Correlational.
  - If the question asks *what kind* or *typology*: use Categorical.
  - If the question asks *what will happen*: use Predictive.
  - Never author a hypothesis that lacks an explanatory or predictive claim; descriptive observations remain in the theme map (`HYP-FM-01`, `HYP-ST-01`).
- **Source**: `T01_RSRCHMTHD_ResearchToArticleMethods_2026-10-19/_INFO_RSRCHMTHD-07_HypothesisGeneration.md` Section RQ-13; Excelsior Online Writing Lab (Hypothesis Types).
- **Rule Reference**: `HYP-FM-01`, `HYP-ST-01`.

### Decision 2: Generation Method and Explanandum Source

- **Question**: From which analytical artifact is the candidate hypothesis abducted?
- **Options**:
  - From themes: abducting mechanisms that explain why an empirical pattern coheres across sources.
  - From contradictions: abducting distinct hypotheses that resolve an open tension (`CR-NN`) by demonstrating scope differences or competing mechanisms.
  - From gaps: abducting exploratory hypotheses that address missing observations in the research matrix.
- **Criterion**: For each research question, generate candidates from all available S2 artifacts (`DRSYNART-FR-15`):
  - Every open contradiction in `Contradiction Register` must prompt at least two competing hypotheses representing alternative resolutions.
  - Themes prompt hypotheses explaining systemic causes.
  - Gaps prompt exploratory hypotheses directing S4 crucial tests.
- **Source**: `T01_RSRCHMTHD_ResearchToArticleMethods_2026-10-19/_INFO_RSRCHMTHD-07_HypothesisGeneration.md` Section Method Description; Douven, *Abduction* (SEP).
- **Rule Reference**: `HYP-ST-01`, `HYP-DV-01`.

### Decision 3: Candidate Count and Set Diversity (3-7 Range)

- **Question**: How many candidate hypotheses must be held simultaneously per research question?
- **Options**:
  - Multiple working hypotheses (3-7 candidates): holding a diverse, mutually exclusive set simultaneously to prevent attachment to a single ruling theory.
  - Single ruling theory or binary pair: holding only one favored explanation or a simple yes/no binary.
- **Criterion**: Always generate between 3 and 7 candidate hypotheses per research question (`DRSYNART-FR-15`). Minimum of 3 prevents binary polarization where the dominant narrative wins by default. Maximum of 7 ensures the subsequent S4 ACH matrix remains cognitively manageable (Heuer 1999). At least one candidate must explicitly contradict the dominant theme or reject a shared assumption identified in the Key Assumptions Check (`HYP-DV-01`).
- **Source**: `T01_RSRCHMTHD_ResearchToArticleMethods_2026-10-19/_INFO_RSRCHMTHD-07_HypothesisGeneration.md` Section RQ-14; Chamberlin (1890); Heuer (1999).
- **Rule Reference**: `HYP-DV-01`.

### Decision 4: Competing Hypothesis Requirement (Rival or Null Pairing)

- **Question**: How is mutual exclusivity and competition enforced within the candidate set?
- **Options**:
  - Explicit rival binding: every candidate hypothesis explicitly links to at least one named rival (`H-NN`) or specifies the null hypothesis (`H-00`), ensuring competing claims cannot both be true simultaneously.
  - Independent assertions: listing standalone ideas that can all co-exist without friction.
- **Criterion**: Every hypothesis entry must name its explicit rival or the null hypothesis (`DRSYNART-FR-15`). If two candidates can both be true simultaneously, split or refine them until they represent mutually exclusive alternatives (`HYP-RV-01`).
- **Source**: `T01_RSRCHMTHD_ResearchToArticleMethods_2026-10-19/_INFO_RSRCHMTHD-07_HypothesisGeneration.md` Section RQ-14; Platt (1964); Pherson (2005).
- **Rule Reference**: `HYP-RV-01`.

### Decision 5: Falsification Condition Definition

- **Question**: What observable evidence would decisively refute the candidate hypothesis?
- **Options**:
  - Precise observable falsifier: stating an explicit empirical finding or measurable threshold that, if discovered, proves the hypothesis false.
  - Vague survival clause: stating broad generalizations that accommodate any outcome.
- **Criterion**: Every candidate hypothesis must define a concrete, observable falsification condition (`DRSYNART-FR-15`). A hypothesis that cannot be refuted by any conceivable empirical observation fails the quality gate and must be rejected (`HYP-FL-01`).
- **Source**: `T01_RSRCHMTHD_ResearchToArticleMethods_2026-10-19/_INFO_RSRCHMTHD-07_HypothesisGeneration.md` Section RQ-12; Karl Popper, *The Logic of Scientific Discovery*.
- **Rule Reference**: `HYP-FL-01`.

### Decision 6: Crucial Test Plan Formulation and Prior Likelihood

- **Question**: What empirical investigations will discriminate between competing candidates, and what is the initial likelihood?
- **Options**:
  - Targeted crucial test plan: defining specific evidence targets, search venues (local files or targeted web queries), and decisive refutation criteria; stating prior likelihood as an ICD-203 prose phrase.
  - Generic inquiry: proposing open-ended research without decisive exclusion criteria or using bracketed confidence labels.
- **Criterion**: Every candidate hypothesis must contain actionable test plan rows detailing what evidence to collect, where to search, and what result refutes the claim (`DRSYNART-FR-15`). State initial likelihood strictly using ICD-203 prose phrases (`DRSYNART-DD-06`, `HYP-LK-01`, `HYP-TP-01`).
- **Source**: `T01_RSRCHMTHD_ResearchToArticleMethods_2026-10-19/_INFO_RSRCHMTHD-07_HypothesisGeneration.md` Sections RQ-12 and RQ-13; Platt (1964); ICD 203 Analytic Standards.
- **Rule Reference**: `HYP-TP-01`, `HYP-LK-01`.

## 3. Annotated Excerpts

### Annotated Excerpt 1: Register Entry with Statement, Rival, Falsifier, and Prose Likelihood

```markdown
### Hypothesis Entry: H-01

- Research question: RQ-02 (What causes edge invalidation stalls during cluster updates?)
- Statement: Configuration reload scripts trigger lock contention on shared memory caches, blocking worker threads for over 3 seconds.
- Form: Causal (lock contention mechanism produces thread blockage)
- Prompted by: Theme 1 (Edge Invalidation Fragility), Contradiction CR-01
- Key assumptions: Assumes worker threads share a single global lock during key renegotiation.
- Rival hypothesis: H-02 (Network partition drops packet ACKs, triggering client retries)
- Falsifier: Benchmark telemetry showing thread queue wait times remain below 50 ms during peak reload.
- Prior likelihood: Roughly even chance (prose phrase per ICD-203)
- Status: CANDIDATE
```

*What makes this work*: The entry specifies the causal mechanism, links to prompt artifacts, identifies a mutually exclusive rival (`H-02`), defines an observable falsifier, and expresses prior likelihood as a calibrated ICD-203 prose phrase.

### Annotated Excerpt 2: Crucial Test Plan Row

```markdown
### Crucial Test Plan: H-01 vs H-02

- Target evidence: Kernel lock trace logs during synthetic configuration reload.
- Search venue: Local telemetry logs in `_sources/CORP-SC-OPS-01_traces.json`.
- Decisive exclusion condition: If thread wait states occur in `net_rx` rather than `mutex_lock`, H-01 is refuted and H-02 is supported.
- Cruciality: High (decisively discriminates between internal lock contention and external network partition).
```

*What makes this work*: The test plan defines a decisive discrimination condition where the outcome excludes one candidate and supports the rival, implementing Platt's strong inference.

## 4. Named Failure Modes

- **Theme Restated as Hypothesis** (`HYP-ST-01`): Copying an empirical theme into the hypothesis register without proposing an underlying explanatory mechanism or causal claim.
  - *Prevention*: Ensure every hypothesis asserts a causal, correlational, categorical, or predictive claim that explains *why* the theme occurs.
- **Missing Rival Hypothesis** (`HYP-RV-01`): Listing a hypothesis without an explicit mutually exclusive rival or null hypothesis, enabling single-theory bias.
  - *Prevention*: Require every entry to name its competing rival (`H-NN`) or the null hypothesis (`H-00`).
- **Non-Falsifiable Hypothesis** (`HYP-FL-01`): Formulating a hypothesis that cannot be refuted by any conceivable empirical finding.
  - *Prevention*: Specify an exact observable metric or finding that decisively refutes the hypothesis.
- **Untestable Claim** (`HYP-TP-01`): Writing a hypothesis whose crucial test plan requires inaccessible data or untestable assumptions.
  - *Prevention*: Formulate test plan rows targeting accessible local documents, source transcriptions, or targeted web search queries.
- **Bracketed or Numeric Likelihood Labels** (`HYP-LK-01`): Using labels like `[LIKELY]` or percentages like `75%` instead of calibrated ICD-203 prose phrases.
  - *Prevention*: Write prose phrases: "It is likely that..." or "roughly even chance".
- **Uniform Set Assumptions** (`HYP-DV-01`): Generating 3-7 candidates that all share the exact same underlying premise.
  - *Prevention*: Apply the Key Assumptions Check across the candidate set; ensure at least one candidate rejects the dominant assumption.

## 5. Quality Heuristics

1. **Explanatory Depth**: Every hypothesis proposes a mechanism, relationship, or rule explaining an observed pattern, not just re-stating it.
2. **Mutual Exclusivity**: Competing hypotheses cannot both be true under the same operating conditions.
3. **Decisive Falsifiability**: Every hypothesis defines a clear empirical threshold that would prove it wrong.
4. **Discriminative Testing**: Crucial test plan rows are designed to eliminate at least one candidate, not just accumulate confirming data.
5. **Calibrated Expression**: Probabilistic assessments strictly utilize standard ICD-203 prose phrases.

## 6. Self-Review Questions

1. Is every hypothesis classified into a standard logical form (causal, correlational, categorical, predictive)? (`HYP-FM-01`)
2. Does every hypothesis assert an explanatory claim rather than restating an empirical theme? (`HYP-ST-01`)
3. Does the register contain between 3 and 7 candidate hypotheses per research question, including at least one contrarian candidate? (`HYP-DV-01`)
4. Is every hypothesis bound to an explicit rival or the null hypothesis? (`HYP-RV-01`)
5. Does every hypothesis define an observable condition that would refute it? (`HYP-FL-01`)
6. Does every hypothesis include actionable crucial test plan rows? (`HYP-TP-01`)
7. Is prior likelihood expressed as an ICD-203 prose phrase rather than a bracket label or percentage? (`HYP-LK-01`)

## 7. RULES References

Verification standards for hypothesis register artifacts are enforced by `HYPOTHESIS_RULES.md` across the following rule groups:
- `HYP-FM-01`: Standard hypothesis form classification.
- `HYP-ST-01`: Explanatory statement requirements and theme differentiation.
- `HYP-DV-01`: Candidate count (3-7 range) and set diversity standards.
- `HYP-RV-01`: Mandatory rival or null hypothesis pairing.
- `HYP-FL-01`: Explicit falsifier and refutation criteria.
- `HYP-TP-01`: Actionable crucial test plan specification.
- `HYP-LK-01`: Calibrated ICD-203 prose likelihood phrasing.
