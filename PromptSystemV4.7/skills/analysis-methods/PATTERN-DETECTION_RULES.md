# Pattern Detection Rules

Verification rules for pattern detection artifacts produced with `/pattern-detect` or during stage S2 of `/analyze`.

Writing quality: Apply `APAPALAN_RULES.md` and `MECT_WRITING_RULES.md`. Key rules: APAPL-PR-07 (be specific), APAPL-PR-05 (referenceable IDs), MECT-VO-01 (active voice), MECT-WC-02 (plain language).

## Rule Index

Codebook & Findings (CD)
- PTD-CD-01: Codebook entry six-field completeness and boundary rules
- PTD-CD-02: Findings list attribution, coding, and verification labelling

Themes (TH)
- PTD-TH-01: Dual-source qualification for primary themes
- PTD-TH-02: Mandatory counter-finding and negative case search

Contradictions (CR)
- PTD-CR-01: Symmetrical contradiction register pairs and typing

Assumptions (AC)
- PTD-AC-01: Key assumptions check and fragility assessment

Gaps (GP)
- PTD-GP-01: Traceable evidence gap cataloging and research question mapping

## PTD-CD-01: Codebook Entry Six-Field Completeness and Boundary Rules

Every codebook entry must define exactly six fields: code ID, brief definition, full definition, when to use, when not to use, and example quote. The "when not to use" field must state an explicit negative exclusion boundary.

Artifact check: Verify every entry under `## Codebook` contains all six labeled fields and an explicit "When not to use" exclusion condition.

**BAD:**
```markdown
### Code Entry: CODE-CACHE-MISS

- Definition: When the cache does not return the requested object.
- Usage: Use when cache misses are logged.
```

**GOOD:**
```markdown
### Code Entry: CODE-CACHE-MISS

- Brief definition: Cache lookup failure requiring downstream database retrieval.
- Full definition: Any logged telemetry event where an L2 cache request fails to locate an active key, forcing synchronous query execution on the backing datastore.
- When to use: Apply to service trace logs, latency metrics, and audit findings recording cache lookup misses.
- When not to use: Do not apply to planned cache invalidation runs, cold cluster boots, or client-side connection drops.
- Example quote: "Edge cache lookups missed for 42% of customer profile queries following configuration reload."
```

## PTD-CD-02: Findings List Attribution, Coding, and Verification Labelling

Every finding in the findings list must carry a finding ID, verbatim claim or close paraphrase, assigned code IDs, source ID, and verification label. If input is C1, finding IDs and source IDs must match C1 references.

Artifact check: Verify every entry under `## Findings List` contains finding ID, code tags, source ID, and verification label (`[VERIFIED]`, `[ASSUMED]`, `[TESTED]`, or `[PROVEN]`).

**BAD:**
```markdown
- Cache latency increased significantly across edge gateways during cutover.
```

**GOOD:**
```markdown
- F-03: Edge gateway cache lookups missed for 42% of customer profile queries following configuration reload.
  - Codes: CODE-CACHE-MISS, CODE-LATENCY-SPIKE
  - Source: CORP-SC-OPS-01 (Tier 1, audit timestamp 2026-03-15)
  - Verification Label: [VERIFIED]
```

## PTD-TH-01: Dual-Source Qualification for Primary Themes

Every primary theme must name at least two finding IDs originating from at least two distinct source authorities. Prevalence across citations from a single source does not qualify a theme.

Artifact check: Verify every entry under `## Theme Map` lists at least two distinct finding IDs and that those findings trace to at least two different source IDs in the findings list.

**BAD:**
```markdown
### Theme 1: Edge Invalidation Fragility

- Member findings: F-03, F-04
- Findings trace to: CORP-SC-OPS-01, CORP-SC-OPS-01
- Synthesis: Edge caches fail during reload events due to single-source operational reports.
```

**GOOD:**
```markdown
### Theme 1: Edge Invalidation Fragility

- Member findings: F-03, F-09
- Findings trace to: CORP-SC-OPS-01 (operations telemetry), CORP-SC-AUDIT-02 (independent compliance audit)
- Synthesis: Distributed edge caches experience cascading invalidation stalls when cluster configuration schemas update without rolling key pre-population.
```

## PTD-TH-02: Mandatory Counter-Finding and Negative Case Search

Every theme in the theme map must record an explicit check for counter-findings or negative cases. If an active search yielded no counter-evidence, the entry must document the search scope and record zero findings.

Artifact check: Verify every theme block contains a "Counter-findings" section detailing refuting evidence or explicitly logging that a search was conducted with zero refuting hits.

**BAD:**
```markdown
### Theme 2: Automated Failover Efficiency

- Member findings: F-11, F-14
- Synthesis: Automated routing engines reroute traffic within 500 ms without user impact.
```

**GOOD:**
```markdown
### Theme 2: Automated Failover Efficiency

- Member findings: F-11, F-14
- Synthesis: Automated routing engines reroute traffic within 500 ms during primary link termination.
- Counter-findings: Checked cross-zone failover benchmarks in CORP-SC-BENCH-01; no conflicting observations found across 12 synthetic partition runs.
```

## PTD-CR-01: Symmetrical Contradiction Register Pairs and Typing

Every contradiction entry must be assigned a unique ID (`CR-NN`), a category, Side A with finding ID and source tier, Side B with finding ID and source tier, a specific contradiction type (factual, scope, temporal, or definitional), and status `OPEN`.

Artifact check: Verify every entry under `## Contradiction Register` contains both Side A and Side B with finding IDs and source tiers, a valid contradiction type, and status `OPEN`.

**BAD:**
```markdown
- CR-01: Operations says queue pooling is fast, but field engineering disagrees due to high cloud costs.
```

**GOOD:**
```markdown
### Contradiction Entry: CR-01

- Category: QUEUE-ROUTING
- Side A: F-12 (CORP-SC-AUDIT-01, Tier 1) "Consolidating regional queues into a shared routing engine reduces triage delays by 84%."
- Side B: F-27 (CORP-SC-FIELD-02, Tier 2) "Regional queue isolation is essential to prevent cross-zone network egress costs from doubling."
- Contradiction type: Scope (operational latency reduction versus cloud infrastructure egress expense)
- Status: OPEN
```

## PTD-AC-01: Key Assumptions Check and Fragility Assessment

The pattern detection artifact must contain a Key Assumptions Check evaluating the structural premises underpinning the themes, including an assessment of fragility and analytical impact if the premise fails.

Artifact check: Verify the `## Key Assumptions` section exists and lists explicit structural assumptions with fragility ratings and impact descriptions.

**BAD:**
```markdown
## Key Assumptions

We assume network connectivity and cloud infrastructure remain available during our benchmark tests.
```

**GOOD:**
```markdown
## Key Assumptions

- KAC-01: Regional gateway latency assumes cross-zone network round-trip times remain below 5 ms under non-partitioned conditions.
  - Fragility: Moderate. Egress congestion during batch export cycles increases latency up to 18 ms.
  - Impact if invalid: Failover triggers prematurely, causing false-positive queue migrations.
```

## PTD-GP-01: Traceable Evidence Gap Cataloging and Research Question Mapping

The pattern detection artifact must contain an evidence gap catalog listing every research question or analytical dimension lacking empirical findings, with its analytical consequence.

Artifact check: Verify the `## Gaps` section exists and lists missing observations mapped to specific research questions or matrix dimensions.

**BAD:**
```markdown
## Gaps

More data is needed on overall system performance under different user conditions.
```

**GOOD:**
```markdown
## Gaps

- GAP-01: Research question RQ-04 lacks empirical findings regarding sustained write throughput during prolonged multi-region network partitions exceeding 15 minutes.
  - Affected dimension: Resiliency and partition tolerance.
  - Consequence for S3: Requires an exploratory hypothesis regarding partition durability limits.
```
