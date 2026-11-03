# Report Guide

Read BEFORE writing a consulting report, research report, decision memo, whitepaper, or institutional audit with `/propose-report`, `/draft-report`, or `/write-report`.

## 1. Purpose and Reader Outcome

After reading this GUIDE, you can write a report designed for non-linear readers from governing thought to release. You can formulate a governing answer, structure key-line claims with action titles, design data exhibits that state one clear message, produce an executive summary that stands completely alone, separate narrative findings from methodology appendices, word actionable recommendations with owner and date, execute multi-tier workflows, and run a technique bake-off without quality drift.

## 2. Report Craft Decisions in Working Order

Every report follows ten core craft decisions, executed in the sequence below.

### Decision 1: Governing Thought (Central Answer)

- **Question**: What is the single sentence that answers the core question the reader brings to this report?
- **Options**:
  - Recommendation statement: "Consolidate regional ticketing tools onto one platform within 10 months to cut support response times by 50%."
  - Empirical finding: "Database locking scripts account for 84% of warehouse dispatch halts across peak operating hours."
  - Evaluative conclusion: "The candidate architecture meets throughput targets but introduces unacceptable vendor lock-in risks."
  - Topic description: "Analysis of regional customer support operations."
- **Criterion**: Choose the form matching the report mandate: recommendation for consulting/decision reports, empirical finding for research reports, evaluative conclusion for audit reports. Never use a topic description. The governing thought must stand at the apex of the report pyramid and answer the client's question in one declarative sentence.
- **Source**: Barbara Minto, *The Pyramid Principle*.
- **Rule Reference**: `RPT-CT-01`.

### Decision 2: Key-Line Ordering Logic

- **Question**: What logical sequence connects the main claims directly beneath the governing thought?
- **Options**:
  - Comparative: ranking options or findings by importance, cost, or urgency (strongest first).
  - Chronological: tracing cause before effect or chronological discovery stages.
  - Structural: dividing an organization, architecture, or market into mutually exclusive components.
  - Deductive: establishing an accepted premise, identifying a complication, and deriving the conclusion.
  - Why-How-What: addressing reader motivation, operational execution, and final deliverables.
- **Criterion**: Base ordering strictly on the grouping method. If weighing alternatives, use comparative. If diagnosing a failure cascade, use chronological. If auditing system divisions, use structural. Ordering must be transparent and non-arbitrary.
- **Source**: Barbara Minto, *The Pyramid Principle*.
- **Rule Reference**: `RPT-CT-02`.

### Decision 3: One Message per Section and Exhibit

- **Question**: What single takeaway does each section and each data exhibit convey?
- **Options**: A topic label ("Regional Performance Metrics"); an action title stating the conclusion ("Northern Region Halved First-Response Times During Four-Month Consolidation Pilot").
- **Criterion**: Every section heading and exhibit title must state its conclusion as an active claim. A non-linear reader skimming headings and exhibits alone must understand the complete storyline without reading body paragraphs.
- **Source**: Gene Zelazny, *Say It With Charts*; Government Statistical Service (GSS), *Writing About Statistics*.
- **Rule Reference**: `RPT-ST-03`, `RPT-EV-01`.

#### Annotated Excerpt 1: Action Title and Exhibit Design

```markdown
### Exhibit 3: Ticket Transfer Latency Consumes 31% of Support Working Hours

- Metric: Regional transfer volume vs. direct ticket resolution (FY2025 audit data, n = 42,000 tickets)
- Primary finding: A customer ticket routed across regional boundaries requires an average of 4.2 business hours of manual triage before agent assignment
- Source: Customer Operations Incident Ledger, 2025-Q4

Manual transfers between regional queues account for 118k EUR in annual overhead. Consolidating all three regional queues into a shared routing engine eliminates the re-entry step and reduces average transfer latency to under six minutes.
```

*What makes this work*: Exhibit 3 carries an active declarative title stating the message rather than a generic label like "Transfer Data". The supporting text explains the operational consequence without redundantly repeating the raw data points listed in the exhibit.

### Decision 4: Action Title vs. Topic Title Discipline

- **Question**: Should section headings name the topic or state the takeaway?
- **Options**:
  - Action title: declarative sentence asserting the finding ("Consolidating Platforms Recovers 166k EUR in Annual License Redundancy").
  - Topic title: noun phrase naming the subject ("License Cost Analysis").
  - Research question title: question answered by the section ("Does Cross-Region Routing Delay High-Priority Tickets?").
- **Criterion**: Use action titles for consulting, decision, and institutional reports. Use question titles only in formal research reports following IMRAD where sections directly answer numbered research questions. Never use topic titles; they force readers to parse prose to learn the point.
- **Source**: Barbara Minto, *The Pyramid Principle*; Gene Zelazny, *Say It With Charts*.
- **Rule Reference**: `RPT-ST-03`.

### Decision 5: Data Placement (Text, Table, or Chart)

- **Question**: How should each empirical metric be presented to the reader?
- **Options**:
  - Prose text: single number placed in narrative context.
  - Table: structured rows and columns presenting exact values for multi-variable comparison.
  - Chart: visual display of relationships (bar for item comparison, line for time series, scatter for correlation).
- **Criterion**: Match format to reader comparison needs (Zelazny and Tufte):
  - Use tables for exact numerical lookups or small datasets (<10 values).
  - Use charts only when visual pattern or trend slope conveys more than exact digits.
  - Never use pie charts for precise values.
  - Avoid putting more than two numbers in a single sentence.
  - Never repeat numbers in both prose and table; the table holds the exact data, prose explains the operational implication.
- **Source**: Edward Tufte, *The Visual Display of Quantitative Information*; Gene Zelazny, *Say It With Charts*.
- **Rule Reference**: `RPT-EV-02`.

### Decision 6: Stand-Alone Executive Summary

- **Question**: What does the executive summary contain, and can an executive act without reading the rest of the report?
- **Options**:
  - Condensed report: governing thought, key-line claims, primary empirical evidence, and actionable recommendation.
  - Table of contents summary: prose description listing what each section covers.
  - Abstract: neutral 100-word summary of questions and findings.
  - Highlights list: unconnected bullet points of interesting numbers.
- **Criterion**: Use the condensed report structure for consulting and institutional reports. It must stand completely alone: a reader who reviews only the executive summary must receive the governing thought, key supporting claims, primary evidence, and the recommendation. Never write a table-of-contents summary. Keep to 1-3 pages maximum (or 2-4 pages for complex institutional audits per GAO standards).
- **Source**: U.S. Government Accountability Office (GAO), *Executive Guide*; Barbara Minto, *The Pyramid Principle*.
- **Rule Reference**: `RPT-ST-02`.

#### Annotated Excerpt 2: Stand-Alone Executive Summary and Actionable Recommendation

```markdown
## Executive Summary

Customer support operations currently run across three regional ticketing platforms resulting from the 2024 merger. Since Q1 2026, median first-response time has lengthened from 4.5 to 9.0 hours, and enterprise customer churn reports identify slow support as the primary cancellation driver. We recommend investing 280k EUR to consolidate all three regions onto a unified ticketing platform by Q2 2027; license savings and manual routing reductions repay this capital expenditure within 10 months.

Key findings:
1. Fragmented tools generate 190k EUR in annual duplicate licenses and manual transfer overhead.
2. Northern region pilot proved that shared queueing cuts first-response times by 53%.
3. System migration risk is restricted to a four-week operational change freeze per region.

### Recommended Action
- Owner: Head of Customer Operations
- Action: Execute vendor agreement and authorize 280k EUR capital expenditure for shared platform migration
- Target Date: Contract execution by 2026-11-30; full regional cutover by 2027-06-30
- Linked Findings: Audit Findings F-02 and F-07
```

*What makes this work*: The executive summary opens with Situation, Complication, and Answer. Key findings summarize the key line. The recommendation explicitly names the owner, concrete action, deadline, and source findings, enabling leadership to act immediately.

### Decision 7: Appendix vs. Body Partitioning

- **Question**: What content stays in the primary report body, and what moves to the appendix?
- **Options**:
  - Progressive disclosure: executive findings, core storyline, and high-level exhibits in the body; comprehensive methodology, raw data tables, calculation scripts, and questionnaires in the appendix.
  - Monolithic body: all survey data, statistical proofs, and analysis in the main text.
- **Criterion**: Apply progressive disclosure (GSS/GAO). The body serves decision-makers moving top-down; the appendix serves auditors, technical specialists, and analysts who need to verify or replicate results. Never block the narrative storyline with pages of raw tabular data.
- **Source**: Government Statistical Service (GSS), *Writing About Statistics*; U.S. GAO.
- **Rule Reference**: `RPT-ST-04`.

### Decision 8: Actionable Recommendation Wording

- **Question**: How is a recommendation formulated?
- **Options**:
  - Vague suggestion: "Management should consider reviewing queue routing policies."
  - Passive finding: "Ticket transfer delays represent a substantial operational problem."
  - Actionable mandate: "The Head of Customer Operations should consolidate regional queues onto Platform X by Q2 2027."
- **Criterion**: Every recommendation must specify an accountable owner (role or department), a concrete action verb, an enforceable deadline, and linked body findings. A recommendation without an owner is a wish; without a deadline, it is an indefinite delay.
- **Source**: U.S. Government Accountability Office (GAO), *Standards for Internal Control*.
- **Rule Reference**: `RPT-CT-03`.

### Decision 9: Exhibit Numbering and Cross-Referencing

- **Question**: How are exhibits cataloged and referenced within prose?
- **Options**: Sequential numbering (Exhibit 1, Exhibit 2) with explicit text cross-references; section-based numbering (Exhibit 3.1, 3.2); unnumbered inline graphics.
- **Criterion**: Use sequential numbering throughout the report body (`Exhibit 1`, `Exhibit 2`). Every exhibit must carry a number, an action title, and a source attribution line. Body text must reference every exhibit explicitly before or immediately after its appearance ("as detailed in Exhibit 2").
- **Source**: Office for National Statistics (ONS), *Statistical Article Standards*.
- **Rule Reference**: `RPT-EV-01`.

### Decision 10: Report Convention Selection

- **Question**: Which established structural convention governs the report layout?
- **Options**:
  - Minto pyramid: consulting standard (governing answer first, MECE key-line claims, evidence drill-down).
  - IMRAD: scientific/empirical research standard (Introduction, Methods, Results, Discussion).
  - Institutional audit: GAO/GSS standard (Executive Summary, Background, Findings in Brief, Analysis, Recommendations, Agency Comments).
- **Criterion**: Select convention strictly by reader need:
  - If the reader needs to approve a commercial or operational decision: use Minto pyramid.
  - If the reader needs to inspect data validity and replicate analysis: use IMRAD.
  - If the reader needs compliance, governance, and audit accountability: use GAO institutional audit.
- **Source**: International Committee of Medical Journal Editors (ICMJE); Barbara Minto.
- **Rule Reference**: `RPT-CT-02`.

## 3. Type-Owned Decisions and Workflow Integrations

Reports possess distinct defaults governing execution depth, option scoring, and multi-tier compilation.

### Tier Selection and Escalation Rules (NFR-03)

- **Tier 1 (Default for Small Reports)**: When input material contains at most 6 top-level sections and targets at most 5,000 words, `/write-report` executes at tier 1 in a single turn (2-10 minutes).
- **Tier 2 (Planned Multi-Step Sequence)**: When input exceeds 6 sections or 5,000 words, or when called with `tier 2`, the workflow drafts a STRUT and a single PROMPTS file (3-10 prompts) executing without pause.
- **Tier 3 Escalation**: When a tier-2 plan exceeds 10 prompts, it automatically escalates to tier 3 (2-8 prompt files with review checkpoints).

### Audience Adaptation (`for <audience>`)

The optional parameter `for <audience>` adapts technical density, exhibit focus, and recommendation framing:
- `for executive`: leads with capital allocations, payback periods, risk thresholds, and governance mandates.
- `for practitioners / technical specialists`: leads with architectural specifications, benchmark deviations, and deployment protocols.
- `for public / regulatory oversight`: leads with compliance audit findings, methodology transparency, and plain-language summaries.
- **Rule Reference**: `RPT-CT-03`.

### Option Proposals and Scoring (`/propose-report`)

When invoked via `/propose-report`, the workflow produces `[ID]-OPTIONS-NN_[Title].md`:
- Brief first: before generating options, write the `## Brief` section (Mandate, Purpose, Audience, Reader outcome, Governing question, In scope, Out of scope, Constraints, Success criteria). Quote the user's request verbatim as Mandate; mark every value you derive instead of taking from the user with `[ASSUMED]`. Without a Brief, nobody can check Goal Alignment or Impact.
- Default candidate count: exactly 3 options.
- Outline: every section on its own numbered line with five fields: `Goal` (cites the Reader outcome item it serves), `Content`, `Evidence` (finding IDs or `[ASSUMED]`), `Reason`, `Handoff`. A section whose Goal serves no Reader outcome item is a cut or appendix candidate.
- Standard scoring weights: Goal Alignment (30%), Supportability (30%), Impact (25%), Specificity (15%). Goal Alignment is scored against the Brief `Governing question`, `Purpose`, and `Reader outcome`; Impact against the Brief `Audience` and its stated need; Supportability reads the `Evidence` field of every section.
- Concludes with one recommended option and selection rationale; the `Why` line names the Brief field behind the Goal Alignment and Impact scores.
- `/draft-report` copies the Brief and keeps the chosen outline's sections and field names, adding detail (fill-in instructions in `Content`, diagram placeholders, claim-level Evidence Placement). `/write-report` never copies the Brief into the output.
- **Rule Reference**: `RPT-CT-04`, `RPT-CT-05`.

### Sample Bake-Off (`compare techniques` per DRSYNART-DD-39)

When the user calls `/propose-report` with `compare techniques <ID>, <ID>[, <ID>]` (2-4 technique IDs, e.g., `compare techniques MINTO, IMRAD, DIATAXIS`):
- The workflow writes one candidate option per technique ID.
- It authors one complete sample section per candidate directly into the OPTIONS file.
- Sample length cap: at tier 1, sample sections are capped at 500 words each to protect the single-turn budget; when full-length sample sections are requested, escalate to tier 2.
- It scores each sample section against:
  1. This GUIDE's quality heuristics (action titles, non-linear navigation, exhibit message clarity).
  2. The style-pattern signals (`AI_WRITING_DETECTION_RULES.md`).
  3. CHECKS files are NEVER loaded during bake-off scoring (`DRSYNART-FR-32`).
- Results are recorded under each option's `Sample:` field.

### Default Storytelling Pass for Untechniqued Reports

When invoked without `using <ID>`, the report applies progressive disclosure:
1. Executive summary opens with governing answer.
2. Section headings use action titles to carry the narrative thread.
3. Body sections synthesize findings before presenting supporting tables.
- **Rule Reference**: `RPT-ST-05`.

### Technique Override Rule (`using <ID>`)

When the user passes `using <ID>` (e.g., `using MINTO` or `using IMRAD`):
- The technique implements the document type's Slot Contract (`DRSYNART-DD-44`) with five fusion assignments:
  1. **Header block = type**: `FRAME` slot (`Doc ID`, `Document Type: report`, `Technique`, `Persona`, `Audience`, `Source`) is owned by the report type.
  2. **OPTIONS/DRAFT scaffolding = type**: `FRAME` slot (Brief, scoring criteria, Style Sheet, Open Questions, Release Check) is owned by the report type.
  3. **Body section inventory and order = technique**: `SECTIONS` slot is filled by the technique's exported Section Inventory (ordered list of section roles and action titles).
  4. **Outline wrapping**: In OPTIONS and DRAFT, each technique inventory row is wrapped with the five DD-43 outline fields (`Goal`, `Content`, `Evidence`, `Reason`, `Handoff`).
  5. **Technique exemptions**: Any stage exemptions (such as MINTO's AMINTON Q/A tree in OPTIONS) live in the technique's own GUIDES, not in type files or session notes.
- Without `using <ID>`, the report type's default Section Inventory (Executive Summary, Key Lines, Recommendations, Appendices) applies.
- Report quality rules (`RPT-ST-03`, `RPT-EV-01..02`, `RPT-ED-01..02`, `RPT-RC-01`) remain strictly binding.
- Technique rules never waive house style or privacy rules.

## 4. Editorial Quality and Consistency Standards

### Edit Levels Applied to Reports

Reports require all five standard editing passes:
1. Developmental edit: structure, pyramid logic, and appendix separation.
2. Line edit: clarity, flow, and Paramedic Method lard reduction.
3. Copyedit: numbers, dates, units, and style sheet consistency.
4. Fact-check: independent verification of every metric and source link.
5. Proofread: cross-reference validation, exhibit numbering, and formatting.

### Clarity Principles (Line Edit)

1. **Lanham's Paramedic Method**: Eliminate state-of-being verbs and passive constructions; ensure the lard factor remains under one-third.
2. **Williams's Characters and Actions**: Name institutional actors as grammatical subjects and decisions as verbs. Place familiar baselines first, then new findings.
3. **Pinker's Classic Style**: Treat the report as a transparent lens positioning the reader to see organizational and technical realities clearly.
- **Rule Reference**: `RPT-ED-01`.

### Fact-Checking Standard

Reports carry formal decision liability and require rigorous fact-checking (Borel):
- Every metric, percentage, currency figure, and date must be cross-referenced to a registered finding ID or marked `[ASSUMED]`.
- Fact-checking must be performed independently from authoring prompts.
- **Rule Reference**: `RPT-EV-03`.

### Tier 2-3 Pass Sequence (DRSYNART-SPEC-8.3)

At tier 2-3, report execution follows a compiled prompt sequence:
1. Developmental outline compiled into DRAFT file with section goals and exhibit placeholders.
2. Section prompts execute draft writing and line editing.
3. Checkpoint prompts verify structural and evidence criteria.
4. Copyediting pass regularizes terms and tables against the style sheet.
5. Independent fact-check verifies calculations and citations.
6. Release check verifies final publication integrity.

### Release Check Standards

Before release, every report must satisfy the seven release check criteria (`DRSYNART-SPEC-8.5`):
1. Header fields complete: `Doc ID: [TOPIC]-REPORT-[NN]`, `Document Type: report`, `Technique`, `Persona`, `Audience`, `Source`.
2. Sourcing: every empirical metric cited or marked `[ASSUMED]`.
3. Numbering and cross-references: continuous exhibit numbering; all text references resolve.
4. Presentation hygiene: zero agent prompts, scratchpads, or workflow metadata.
5. AI-writing detection: signals below threshold (at most 1 signal across Sourcing, Style, Structure, Voice; excluding structural signals produced by technique by construction).
6. Persona trait budget respected (when a persona is specified).
7. Word count within target range.
- **Rule Reference**: `RPT-RC-01`.

### Output Naming Conventions

All report artifacts follow `DRSYNART-FR-24`:
- Options file: `[ID]-OPTIONS-NN_[Title].md`
- Draft file: `[ID]-DRAFT-NN_[Title].md`
- Final report: `YYYY-MM-DD_[Title].md`
- Deliverables reside in the active working folder, never in `_agentwork/`.

## 5. Named Failure Modes and Strategic Mitigations

1. **Topic Title Instead of Action Title**: Headings describe subject matter rather than asserting a conclusion ("Cost Review" instead of "Duplicate Tool Licenses Cost 190k EUR Annually").
   - *Strategic mitigation*: Convert every noun heading into a declarative sentence stating the finding. See `RPT-ST-03`.
2. **Exhibit Without a Message**: Charts or tables are labeled with descriptions ("2026 Ticket Volume") rather than conclusions.
   - *Strategic mitigation*: Add an action title above every exhibit stating what the visual data proves. See `RPT-EV-01`.
3. **Executive Summary as Table of Contents**: The summary lists what topics the report will discuss instead of presenting the governing answer, findings, and recommendation.
   - *Strategic mitigation*: Apply the stand-alone test. Rewrite the summary to include the governing thought, top 3-5 findings, and full recommendation. See `RPT-ST-02`.
4. **Number Duplication in Text and Table**: Prose repeats every digit and percentage already displayed in an adjacent data table.
   - *Strategic mitigation*: Let the table hold the exact numbers. Restrict prose to stating the operational takeaway or comparison. See `RPT-EV-02`.
5. **Recommendation Without Owner or Date**: Recommendations are worded as passive advice without accountability ("Routing protocols should be optimized").
   - *Strategic mitigation*: Enforce owner, action verb, target date, and linked finding ID for every recommendation. See `RPT-CT-03`.
6. **Methods Blocking the Main Narrative**: The primary report body is bogged down by pages of survey methodology or raw data logs.
   - *Strategic mitigation*: Partition content per progressive disclosure. Relocate methodology and raw data to the appendix. See `RPT-ST-04`.
7. **Pie Chart for Exact Values**: Pie charts or complex multi-dimensional graphics obscure numerical comparisons.
   - *Strategic mitigation*: Convert pie charts to clean tables for exact numbers or horizontal bar charts for item rankings. See `RPT-EV-01`.
8. **Unfocused Key Line (Lack of MECE)**: Supporting claims under the governing thought overlap or leave major gaps.
   - *Strategic mitigation*: Group claims by one logical principle (comparative, chronological, structural, or deductive) and verify mutually exclusive categories. See `RPT-CT-02`.
9. **Unverified Assumptions Stated as Facts**: Projections and forecasts are presented as empirical certainties without caveats.
   - *Strategic mitigation*: Tag all forward-looking projections with `[ASSUMED]` and state driving variables. See `RPT-EV-03`.
10. **Lardaceous Prose in Executive Reporting**: Sentences are burdened with passive nominalizations and empty filler phrases.
    - *Strategic mitigation*: Execute the Paramedic Method pass; reduce lard factor below one-third. See `RPT-ED-01`.

## 6. Quality Heuristics (Observable Properties)

Test these observable properties on the finished report:
- **Stand-Alone Test**: Can an executive make an informed decision by reading ONLY the executive summary? (Yes / No)
- **Skim Test**: Does reading section headings and exhibit titles alone provide a continuous, coherent argument? (Yes / No)
- **Action Title Test**: Is every section heading and exhibit title phrased as a complete declarative message rather than a noun phrase? (Yes / No)
- **Recommendation Accountability Test**: Does every recommendation specify a named owner, concrete action, and deadline? (Yes / No)
- **Duplication Test**: Are exact numerical values isolated in tables without redundant repetition in prose sentences? (Yes / No)
- **Appendix Separation Test**: Are raw survey instruments, methodology scripts, and extended tables placed in the appendix? (Yes / No)

## 7. Self-Review Questions

Review the report against these numbered questions before release:
1. Does the header block contain all six required fields matching FR-24? (`RPT-ST-01`)
2. Can a reader act on the recommendation from the executive summary alone? (`RPT-ST-02`)
3. Does every section heading state a clear conclusion rather than a topic? (`RPT-ST-03`)
4. Are detailed methodology and supplementary datasets partitioned into the appendix? (`RPT-ST-04`)
5. Does the report structure follow progressive disclosure when written without a technique? (`RPT-ST-05`)
6. Does the entire report support a single governing thought answering the client's question? (`RPT-CT-01`)
7. Do key-line claims follow a stated logical ordering without conceptual overlap? (`RPT-CT-02`)
8. Does every recommendation name an accountable owner, an action verb, and a deadline? (`RPT-CT-03`)
9. Does every exhibit carry an action title, source line, and appropriate comparison format? (`RPT-EV-01`)
10. Are numerical values presented cleanly without redundant repetition between text and tables? (`RPT-EV-02`)
11. Is every factual metric traced to a source finding or tagged `[ASSUMED]`? (`RPT-EV-03`)
12. Did the line edit eliminate nominalizations and reduce lard factor below one-third? (`RPT-ED-01`)
13. Are all terms, units, and dates standardized against the DRAFT style sheet? (`RPT-ED-02`)
14. Does the report pass all seven criteria of the release check? (`RPT-RC-01`)

## 8. Annotated Exemplar Links

Study these mentor exemplars for concrete demonstrations of report craft decisions:

- [MINTO Executive Proposal](../writing_techniques/EXAMPLES/MINTO_EXAMPLE_01-ExecutiveProposal.md)
  - *What makes this work*: Exemplifies consulting decision report design. Opens with an answer-first governing thought and financial payback calculation, structures key-line claims with informative action titles, isolates data points in distinct sections, and concludes with an owner-action-deadline decision block.
- [IMRAD Empirical Results Report](../writing_techniques/EXAMPLES/IMRAD_EXAMPLE_01-EmpiricalResultsReport.md)
  - *What makes this work*: Demonstrates scientific research report architecture. Separates objective results from discussion and limitations, organizes findings by numbered research questions, uses action titles for exhibit findings, and details experimental methodology for replication.

## 9. RULES References

The following rule ID ranges in `REPORT_RULES.md` define the enforceable output standards for all reports:
- `RPT-ST-01` through `RPT-ST-05`: Report structure, header completeness, stand-alone executive summary, action titles, appendix separation, and progressive disclosure.
- `RPT-CT-01` through `RPT-CT-04`: Governing thought, key-line logic, actionable recommendations, and options proposal scoring / bake-off.
- `RPT-EV-01` through `RPT-EV-03`: Exhibit design and comparison types, number placement discipline, and traceable claim attribution.
- `RPT-ED-01` through `RPT-ED-02`: Line clarity with Paramedic Method lard factor, and style sheet consistency across terms and units.
- `RPT-RC-01`: Final release check verification standards.
