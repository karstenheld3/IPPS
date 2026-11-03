# Pattern Detection Guide

Read BEFORE coding findings, detecting themes, mapping contradictions, or identifying research gaps with `/pattern-detect` or during stage S2 of `/analyze`.

## 1. Purpose and Reader Outcome

After reading this GUIDE, you can transform unstructured empirical research or C1 Knowledge Libraries into a structured codebook, an attributed findings list, an evidence-grounded theme map, a two-sided contradiction register, a key assumptions check, and an actionable gap list. You can choose the optimal theme-building method based on data size and tension visibility, and provide verified inputs to abductive hypothesis generation without confirmation bias.

## 2. Pattern Detection Decisions in Working Order

Executing pattern detection follows five core analytical decisions in the sequence below.

### Decision 1: S1 Qualitative Coding Pass

- **Question**: How are raw observations converted into coded, searchable evidence units?
- **Options**:
  - Two-cycle coding with MacQueen codebook: first-cycle open coding close to the source's own terms (emic), second-cycle grouping into categories; maintain a six-field codebook per code (code ID, brief definition, full definition, when to use, when not to use, example quote); produce an attributed findings list.
  - Ad-hoc highlighting: tagging keywords directly without explicit inclusion and exclusion definitions.
- **Criterion**: Always construct or update a six-field codebook and attributed findings list. If input is C1, reuse existing finding claim references and `-02` source IDs. If input is raw material, assign continuous finding IDs (`F-01`, `F-02`) and source IDs (`DRSYNART-FR-12`). Code definitions must specify explicit "when not to use" exclusion boundaries to prevent semantic drift.
- **Source**: `T01_RSRCHMTHD_ResearchToArticleMethods_2026-10-19/_INFO_RSRCHMTHD-04_CodingAndFrameworkAnalysis.md` Section RQ-02; MacQueen et al. (1998); Saldana, *The Coding Manual for Qualitative Researchers*.
- **Rule Reference**: `PTD-CD-01`, `PTD-CD-02`.

### Decision 2: Theme Building Method

- **Question**: Which synthesis method moves coded findings into overarching themes?
- **Options**:
  - Method A (Affinity clustering): grouping related codes into candidate themes by shared mechanisms, reviewing internal coherence (Patton's internal homogeneity), and confirming distinctness (Patton's external heterogeneity).
  - Method B (Frequency and co-occurrence): tallying code frequency and charting co-occurrence across sources in the findings matrix to reveal high-density clusters; counting used strictly to prioritize review, never to qualify themes.
  - Method C (Contradiction-first): starting synthesis directly from open tensions and diverging empirical claims; clustering supporting and opposing evidence around identified fault lines.
- **Criterion**: Base method choice strictly on data volume and conflict visibility:
  - If data set is moderate (<40 codes) with mixed findings: use Method A (Affinity clustering).
  - If data set is large (>40 codes or 15+ sources) with dense findings: use Method B (Frequency and co-occurrence) to surface primary groupings.
  - If data set contains sharp, observable disagreements or opposing factions: use Method C (Contradiction-first) to structure themes around empirical tensions.
  - Every theme must be supported by findings from at least two independent sources (`PTD-TH-01`); prevalence alone does not qualify a theme.
- **Source**: `T01_RSRCHMTHD_ResearchToArticleMethods_2026-10-19/_INFO_RSRCHMTHD-05_ThematicAnalysisAndSynthesis.md` Sections RQ-06 and RQ-07; Braun and Clarke (2006, 2019 codebook variant); Patton (1999).
- **Rule Reference**: `PTD-TH-01`, `PTD-TH-02`.

### Decision 3: Contradiction Register Compilation

- **Question**: How are incompatibilities and conflicting empirical findings handled?
- **Options**:
  - Structured contradiction register: cataloging every incompatible finding pair as a distinct entry (`CR-NN`) recording side A (finding ID, source ID, tier), side B (finding ID, source ID, tier), contradiction type, and status `OPEN`.
  - Consensus averaging: smoothing over conflicting metrics or discarding minority reports to present a uniform narrative.
- **Criterion**: Always preserve contradictions in a typed register; never smooth over conflicting accounts (`DRSYNART-FR-14`). Classify each contradiction by type:
  - Factual: sources disagree on an observable datum or measured metric.
  - Scope: findings use identical terms but describe different operational conditions, scales, or workloads.
  - Temporal: older observation supersedes or is superseded by a newer observation.
  - Definitional: sources use the same terminology for different underlying concepts.
  - Contradictions remain `OPEN` through stage S2 to serve as direct inputs for competing hypotheses in stage S3.
- **Source**: `T01_RSRCHMTHD_ResearchToArticleMethods_2026-10-19/_INFO_RSRCHMTHD-05_ThematicAnalysisAndSynthesis.md` Section RQ-08; Braun and Clarke (2006).
- **Rule Reference**: `PTD-CR-01`.

### Decision 4: Key Assumptions Check (KAC)

- **Question**: What unstated premises and structural assumptions underpin the observed themes?
- **Options**:
  - Systematic Key Assumptions Check: listing the core premises taken for granted across source findings, evaluating their fragility, and noting what would break if they proved invalid.
  - Implicit acceptance: assuming that reported source baselines hold across all operating environments.
- **Criterion**: Every theme map must document an explicit Key Assumptions Check (`DRSYNART-FR-14`). Identify dependencies on environmental stability, vendor guarantees, or baseline configurations. Flag fragile assumptions as vulnerability candidates for hypothesis testing.
- **Source**: U.S. Intelligence Community Tradecraft Primer (2009); Richards J. Heuer Jr.
- **Rule Reference**: `PTD-AC-01`.

### Decision 5: Evidence Gap Identification

- **Question**: What critical dimensions of the research mandate remain unanswered?
- **Options**:
  - Traceable gap catalog: auditing research questions and findings matrix columns for missing observations, documenting each gap with its affected dimension and analytical consequence.
  - Extrapolation: filling missing observations with plausible assumptions without tagging them as gaps.
- **Criterion**: Record all missing observations in the gap list (`DRSYNART-FR-14`). A gap exists whenever a research question lacks findings or when an empirical matrix column contains zero entries. Gaps provide direct seeds for exploratory hypotheses in stage S3.
- **Source**: `T01_RSRCHMTHD_ResearchToArticleMethods_2026-10-19/_INFO_RSRCHMTHD-04_CodingAndFrameworkAnalysis.md` Section RQ-04; Gale et al. (2013).
- **Rule Reference**: `PTD-GP-01`.

## 3. Annotated Excerpts

### Annotated Excerpt 1: Six-Field Codebook Entry and Coded Finding

```markdown
### Code Entry: CODE-LOCK-CONTENTION

- Brief definition: Database locking stalls delaying transaction commit cycles.
- Full definition: Any incident where concurrent transaction writers block execution threads, increasing commit latency above 250 ms across cluster nodes.
- When to use: Apply to incident logs, telemetry traces, or audit findings measuring lock wait times or thread starvation.
- When not to use: Do not apply to network partition drops, cold cache startups, or scheduled maintenance halts.
- Example quote: "Commit threads stalled for 3.8 seconds during distributed lock renegotiation under peak load."

### Coded Finding

- F-04: Commit renegotiation scripts account for 68% of warehouse transaction stalls during peak shift cutover.
  - Codes: CODE-LOCK-CONTENTION, CODE-RETRY-STORM
  - Source: CORP-SC-OPS-01 (Tier 1, audit timestamp 2026-03-15)
  - Verification Label: [VERIFIED]
```

*What makes this work*: The codebook entry establishes unambiguous inclusion and exclusion rules. The coded finding links verbatim claims to source metadata and verification labels, enabling bi-directional traceability across analysis stages.

### Annotated Excerpt 2: Symmetrical Contradiction Register Entry

```markdown
### Contradiction Entry: CR-02

- Category: QUEUE-ROUTING
- Side A: F-12 (CORP-SC-AUDIT-01, Tier 1) "Consolidating regional queues into a shared routing engine reduces triage delays by 84%."
- Side B: F-27 (CORP-SC-FIELD-02, Tier 2) "Regional queue isolation is essential to prevent cross-zone network egress costs from doubling."
- Contradiction type: Scope (operational latency reduction versus cloud infrastructure egress expense)
- Status: OPEN (input to competing hypothesis H-02)
- Triangulation note: Benchmarks in F-33 confirm egress surge under synthetic queue pooling.
```

*What makes this work*: Both conflicting sides are fully attributed with finding IDs, source IDs, and source tiers. The contradiction type isolates why the conflict occurs (scope trade-off) and marks the entry `OPEN` as a structured seed for stage S3 hypothesis abduction.

## 4. Named Failure Modes

- **Single-Source Theme** (`PTD-TH-01`): Defining a theme based on findings from only one source or author, mistaking an isolated viewpoint for a systemic pattern.
  - *Prevention*: Require at least two independent source IDs per theme; record single-source claims as candidate observations, not themes.
- **Asymmetrical Contradiction** (`PTD-CR-01`): Logging a conflict that cites only one side or summarizes disagreement without specific finding and source IDs.
  - *Prevention*: Require both Side A and Side B with finding ID, source ID, and tier for every `CR-NN` entry.
- **Unchallenged Confirmation** (`PTD-TH-02`): Finalizing themes without conducting an explicit negative case search for counter-findings that contradict the theme.
  - *Prevention*: Document an explicit counter-findings check under every theme; if no counter-finding exists, record that a search was conducted and yielded zero hits.
- **Undefined Code Boundaries** (`PTD-CD-01`): Writing codebook definitions without explicit "when not to use" exclusion criteria, causing codes to overlap and expand indefinitely.
  - *Prevention*: Enforce all six fields in every codebook entry; verify exclusion boundaries before second-cycle coding.
- **Untraced Findings** (`PTD-CD-02`): Extracting observations without source IDs or verification labels, breaking cross-layer provenance.
  - *Prevention*: Verify every finding row carries source ID, tier, and verification label before proceeding to thematic synthesis.

## 5. Quality Heuristics

1. **Dual-Source Minimum**: Every primary theme contains at least two finding IDs originating from two distinct source authorities.
2. **Exclusion Precision**: Every code in the codebook defines both positive inclusion criteria and negative exclusion boundaries.
3. **Symmetrical Disagreement**: Every contradiction record presents both sides with equal structural fidelity (finding ID, source ID, tier, verbatim claim).
4. **Exhaustive Negative Search**: Every theme explicitly documents an active search for counter-findings or refuting observations.
5. **Clear Tension Typing**: Every contradiction is classified as factual, scope, temporal, or definitional, avoiding vague conflict labels.

## 6. Self-Review Questions

1. Does every codebook entry contain all six required fields, including explicit when-not-to-use rules? (`PTD-CD-01`)
2. Does every extracted finding carry a finding ID, code tags, source ID, and verification label? (`PTD-CD-02`)
3. Does every theme link to at least two finding IDs from two independent sources? (`PTD-TH-01`)
4. Did every theme record an active search for counter-findings and negative cases? (`PTD-TH-02`)
5. Does every contradiction entry cite both Side A and Side B with finding IDs and source tiers? (`PTD-CR-01`)
6. Does the theme map document an explicit Key Assumptions Check with fragility ratings? (`PTD-AC-01`)
7. Does the gap list record all unanswered research questions and missing empirical dimensions? (`PTD-GP-01`)

## 7. RULES References

Verification standards for pattern detection artifacts are enforced by `PATTERN-DETECTION_RULES.md` across the following rule groups:
- `PTD-CD-01` through `PTD-CD-02`: Codebook and findings list requirements.
- `PTD-TH-01` through `PTD-TH-02`: Thematic qualification and counter-finding search requirements.
- `PTD-CR-01`: Symmetrical contradiction register requirements.
- `PTD-AC-01`: Key assumptions check completeness.
- `PTD-GP-01`: Traceable evidence gap cataloging.
