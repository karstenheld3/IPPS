# Analysis Checks

Audits process discipline and quality improvement for multi-stage qualitative synthesis and evidence validation executed with `/analyze` or Layer 2 stage workflows (`/pattern-detect`, `/hypothesize`, `/validate`).

Evidence sources: final analysis deliverable (`_INFO_[TOPIC]-IN[NN]_Analysis.md` or stage INFO files), planning STRUT (`__STRUT_[TOPIC].md`), stage PROMPTS files, disconfirmation logs, conversation history.

## Section 1: /analyze Orchestration Checks

### Process Discipline (PD)

#### ANA-PD-01: STRUT and PROMPTS Drafted Before Content Edits

- Action: Agent drafted `__STRUT_[TOPIC].md` and prompt files before modifying analysis deliverables
- Evidence: STRUT and PROMPTS files exist in `_agentwork/` with timestamps preceding content edits
- Failure indicator: Analysis text authored directly in deliverable without prior STRUT and prompt file planning
- References: ANA-OR-01

#### ANA-PD-02: Tier 3 Human Review Points Recorded

- Action: Agent halted execution between stage prompt files for user inspection during Tier 3 runs
- Evidence: Execution logs record user inspection and sign-off after Pattern Map and Hypothesis Register before next prompt file launches
- Failure indicator: Tier 3 execution ran continuously through all stages without human pause
- References: ANA-OR-04

#### ANA-PD-03: Tier 3 Devil's Advocate Prompt Executed

- Action: Agent executed a dedicated adversarial devil's advocate prompt attacking top candidate hypotheses before final ranking
- Evidence: Stage PROMPTS files include an adversarial prompt attacking top 3 candidates; Validation Report logs challenged assumptions
- Failure indicator: Tier 3 finalized rankings without an explicit devil's advocate challenge
- References: ANA-OR-05

### Quality Improvement (QI)

#### ANA-QI-01: Stage Boundary Fidelity

- Quality question: Did each stage complete its analytical deliverable before subsequent stage reasoning commenced?
- Improvement tip: Prevent premature hypothesizing by verifying that theme maps and contradiction registers are fully drafted before abducting candidate hypotheses.

#### ANA-QI-02: Tier Calibration and Scope Escalation

- Quality question: Does the execution tier match the empirical breadth and multi-approach complexity of the input material?
- Improvement tip: Escalate single-topic sets with deep structural conflicts to Tier 3 to allow dedicated devil's advocate scrutiny and intermediate user reviews.

## Section 2: Pattern Detection Checks (PATTERN-DETECTION)

### Process Discipline (PD)

#### PTD-PD-01: S1 Coding Pass Executed Before Thematic Synthesis

- Action: Agent extracted observations into a six-field codebook and attributed findings list before synthesizing themes
- Evidence: `## Codebook` and `## Findings List` contain populated entries with exclusion rules and source tiers preceding `## Theme Map`
- Failure indicator: Themes generated directly from raw input text without intermediate coding pass
- References: PTD-CD-01, PTD-CD-02

#### PTD-PD-02: Counter-Finding Negative Case Search Conducted

- Action: Agent conducted an explicit search for counter-findings and negative cases for every synthesized theme
- Evidence: Every theme entry in `## Theme Map` contains a `Counter-findings:` section detailing search scope and findings or zero-hit log
- Failure indicator: Themes lack counter-finding search documentation
- References: PTD-TH-02

#### PTD-PD-03: Two-Sided Contradiction Register Sourcing

- Action: Agent logged both sides of empirical conflicts with specific finding IDs, source tiers, and contradiction types
- Evidence: Every entry in `## Contradiction Register` cites Side A and Side B with finding IDs, source IDs, and contradiction types
- Failure indicator: Contradictions cite only one side or summarize disputes without finding IDs
- References: PTD-CR-01

### Quality Improvement (QI)

#### PTD-QI-01: Codebook Exclusion Sharpness

- Quality question: Do when-not-to-use exclusion boundaries actively prevent semantic drift and overlapping category assignments?
- Improvement tip: Sharpen negative exclusion rules whenever two codes frequently co-occur without distinct analytical roles.

#### PTD-QI-02: Contradiction Typing for Hypothesis Abduction

- Quality question: Are empirical contradictions classified with sufficient precision to serve as direct seeds for competing hypotheses in S3?
- Improvement tip: Distinguish scope boundaries from direct empirical conflicts to clarify alternative causal mechanisms.

## Section 3: Hypothesis Generation Checks (HYPOTHESIS)

### Process Discipline (PD)

#### HYP-PD-01: Rival Hypothesis Written Before Validation

- Action: Agent formulated an explicit mutually exclusive rival or null hypothesis for every candidate before entering stage S4
- Evidence: Every entry in `## Hypothesis Register` populates `Rival hypothesis:` with a valid `H-NN` or `H-00` identifier
- Failure indicator: Candidate hypotheses stand as isolated uncontested assertions without rivals
- References: HYP-RV-01

#### HYP-PD-02: Observable Falsifier Defined Prior to Testing

- Action: Agent specified a concrete, measurable refutation condition for every hypothesis before testing
- Evidence: Each hypothesis entry contains an empirical threshold or observable finding in `Falsifier:`
- Failure indicator: Falsifiers rely on broad generalities or absence of positive outcomes
- References: HYP-FL-01

#### HYP-PD-03: Candidate Set Contrarian Diversity

- Action: Agent included at least one candidate that contradicts the dominant theme or rejects a shared structural assumption
- Evidence: Hypothesis set contains an alternative explanation challenging dominant source narratives
- Failure indicator: All candidate hypotheses share identical structural premises from the Key Assumptions Check
- References: HYP-DV-01

### Quality Improvement (QI)

#### HYP-QI-01: Explanatory Form Precision

- Quality question: Does the hypothesis assert an explanatory mechanism or relationship rather than merely restating an empirical theme?
- Improvement tip: Convert descriptive observations into testable "X produces Y via M" causal or predictive formulations.

#### HYP-QI-02: Crucial Test Discrimination Power

- Quality question: Does the test plan specify an experiment or query that decisively excludes at least one competitor?
- Improvement tip: Construct crucial test plan rows that yield mutually exclusive predictions for rival candidates.

## Section 4: Validation and Evidence Weighting Checks (VALIDATION)

### Process Discipline (PD)

#### VAL-PD-01: Local-First Search with External Fallback Logged

- Action: Agent searched local workspace files and transcriptions first before executing targeted external queries or tests
- Evidence: Search logs and test citations demonstrate local inspection preceded external searches
- Failure indicator: Validation executed broad external web searches without auditing existing local transcriptions
- References: VAL-SR-01

#### VAL-PD-02: Active Disconfirmation Search Recorded

- Action: Agent executed explicit refutation queries for every candidate above `refuted` and recorded search exhaustion
- Evidence: `## Disconfirmation Log` records queries, observed results, and an explicit `Exhausted: Yes/No` flag for each item
- Failure indicator: Validation collected only confirming evidence for favored hypotheses
- References: VAL-DC-01

#### VAL-PD-03: Evidence Verification for Proven and Refuted Ranks

- Action: Agent verified `[PROVEN]` or `[TESTED]` evidence before assigning Rank 8, and cited refuting IDs for Rank 0
- Evidence: Citations for Rank 8 items point to verified test runs; Rank 0 items cite refuting finding or `DL-NN` IDs
- Failure indicator: Rank 8 granted based on observational articles or assumptions
- References: VAL-PR-01

#### VAL-PD-04: Layer 1 Loop-Back Confinement

- Action: Agent recorded unsettled items with exhausted searches as Layer 1 research questions without triggering autonomous calls
- Evidence: `## Research Questions for Layer 1` populated; no external Layer 1 workflows invoked autonomously
- Failure indicator: Validation workflow called `/research` or `/deep-research` automatically
- References: VAL-LP-01

### Quality Improvement (QI)

#### VAL-QI-01: Toulmin Warrant Explanatory Strength

- Quality question: Does each warrant explain the exact logical bridge connecting empirical grounds to the hypothesis claim?
- Improvement tip: Test the warrant by removing it; if the connection feels like an ungrounded leap, strengthen the logical warrant.

#### VAL-QI-02: Kent Likelihood and Analytic Confidence Calibration

- Quality question: Are probabilistic likelihood and evidence confidence evaluated and phrased as separate, independent prose statements?
- Improvement tip: Ensure hypotheses supported by high-tier but sparse sources carry high likelihood with low or moderate confidence.
