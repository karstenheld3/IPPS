# Report Checks

Audits process discipline and quality improvement for reports written with `/write-report` or planned with `/propose-report` and `/draft-report`.

Evidence sources: final output document, options proposal (`[ID]-OPTIONS-NN_`), working draft (`[ID]-DRAFT-NN_`), planning notes, conversation history.

## Process Discipline (PD)

### RPT-PD-01: Governing Thought Formulated First

- Action: Agent formulated a single-sentence governing answer before structuring key-line sections or exhibits
- Evidence: Planning artifact or draft opens with an explicit governing thought that answers the core client mandate
- Failure indicator: Report opens with a topic description ("Analysis of Support Operations") rather than a declarative answer
- References: RPT-CT-01, RPT-CT-02

### RPT-PD-02: Options Proposal Scored with Bake-Off Integration

- Action: Agent drafted candidate options scored against standard weights and executed a sample bake-off when `compare techniques` was invoked
- Evidence: `[ID]-OPTIONS-NN_` records Goal Alignment (30%), Supportability (30%), Impact (25%), Specificity (15%) with one recommended candidate; every outline section carries `Goal`, `Content`, `Evidence`, `Reason`, `Handoff` as plain (not bold) labels; the `Why` line names the Brief field behind Goal Alignment and Impact; bake-off samples scored without loading CHECKS
- Failure indicator: Options proposal missing, unscored, outline written as one arrow chain, bold field labels below section lines, scores that cite no Brief field, or CHECKS files loaded during sample evaluation
- References: RPT-CT-04

### RPT-PD-03: Action Titles Enforced Across Sections and Exhibits

- Action: Agent formulated every section heading and exhibit title as an active declarative message stating the takeaway
- Evidence: Skimming section headings and exhibit titles in sequence outlines a complete coherent storyline
- Failure indicator: Section headings or exhibit labels use static noun phrases ("Cost Overview", "Ticket Latency Chart")
- References: RPT-ST-03, RPT-EV-01

### RPT-PD-04: Stand-Alone Executive Summary Structure

- Action: Agent structured the executive summary to deliver governing thought, top key-line findings, and full recommendation
- Evidence: Executive summary contains the governing answer, numbered key findings, and an actionable decision block with owner and deadline
- Failure indicator: Executive summary serves as a table-of-contents preview listing what the report will discuss
- References: RPT-ST-02, RPT-CT-01

### RPT-PD-05: Progressive Disclosure and Appendix Separation

- Action: Agent partitioned exhaustive survey datasets, raw calculation scripts, and questionnaires into the appendix
- Evidence: Main narrative flows continuously for decision-makers; supplementary technical methodology resides in appendix
- Failure indicator: Narrative body is blocked by multi-page raw data tables or extended methodology descriptions
- References: RPT-ST-04

### RPT-PD-06: Actionable Recommendation Accountability

- Action: Agent worded every recommendation with a named organizational owner, concrete action verb, deadline, and linked findings
- Evidence: Recommendations specify role or department, operational mandate, target completion date, and audit finding IDs
- Failure indicator: Recommendations phrased as passive advice without an accountable owner or enforceable deadline
- References: RPT-CT-03

### RPT-PD-07: Data Isolation and Number Discipline

- Action: Agent placed exact multi-variable numerical data in tables and restricted prose to operational takeaways
- Evidence: Sentences explain comparisons and consequences rather than repeating raw digits listed in adjacent exhibits
- Failure indicator: Body text lists more than two exact numerical values that already appear in an adjacent table
- References: RPT-EV-02, RPT-EV-01

### RPT-PD-08: Independent Fact-Checking Execution

- Action: Agent verified every empirical metric and financial figure against source findings using a separate verification step
- Evidence: Every factual claim traces to a verified finding ID or is tagged `[ASSUMED]`; verification recorded in audit logs
- Failure indicator: Metrics stated without source references, or unverified assumptions presented as factual certainties
- References: RPT-EV-03

### RPT-PD-09: Style Sheet Consistency and Lard Reduction

- Action: Agent established a style sheet before copyediting and applied the Paramedic Method to eliminate nominalizations
- Evidence: Standardized terms and currency formats maintained across all sections; lard factor remains below one-third
- Failure indicator: Lard factor exceeds 33%, passive voice dominates, or currency/units change format across sections
- References: RPT-ED-01, RPT-ED-02

### RPT-PD-10: Release Check Documented

- Action: Agent verified the report against all seven release check criteria and recorded the release record
- Evidence: Release check block exists in DRAFT or verification log with complete header, AI detection status, and word count
- Failure indicator: Report published without an explicit release check verification record
- References: RPT-RC-01, RPT-ST-01

### RPT-PD-11: Brief Recorded Before Options

- Action: Agent wrote the Brief before generating options, carried it into the DRAFT, and kept it out of the output document
- Evidence: OPTIONS and DRAFT files contain `## Brief` with all nine fields; Mandate quotes the user request; derived values carry `[ASSUMED]`; DRAFT records `Brief changes`
- Failure indicator: No Brief, Brief written after scoring, Mandate paraphrased, derived values unmarked, or Brief copied into the published report
- References: RPT-CT-05, RPT-CT-04

## Quality Improvement (QI)

### RPT-QI-01: Executive Summary Decision Efficacy

- Question: Can an executive authorize the proposed capital allocation or policy change by reading ONLY the executive summary?
- Improvement tip: Ensure the executive summary states the exact investment amount, payback timeline, primary risk mitigation, and executive sponsor.

### RPT-QI-02: Key-Line MECE Sharpness

- Question: Do the supporting claims beneath the governing thought have zero conceptual overlap while completely covering the mandate?
- Improvement tip: Group claims by a single transparent logic (comparative, chronological, structural, or deductive) and ensure no finding belongs to two categories.

### RPT-QI-03: Exhibit Message Speed

- Question: Can a reader glance at an exhibit for five seconds and instantly state its conclusion without reading surrounding prose?
- Improvement tip: Align the chart or table format with the comparison type (bar for item ranking, line for time series) and highlight the key outlier visually or in the action title.

### RPT-QI-04: Recommendation Operational Pragmatism

- Question: Does the recommendation account for organizational inertia, operational change freezes, and resource constraints?
- Improvement tip: Pair the recommendation with a four-week transition boundary or contingency protocol, specifying who resolves operational bottlenecks.

### RPT-QI-05: Analytical Balance and Caveat Transparency

- Question: Does the report acknowledge trade-offs, alternative interpretations, and data limitations fairly?
- Improvement tip: Add a short counterpoint paragraph addressing why competing alternatives were rejected, citing specific cost or risk boundaries.
