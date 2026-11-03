# Report Rules

Output standards for reports written with `/write-report` or planned with `/propose-report` and `/draft-report`.

**Writing quality:** Apply `APAPALAN_RULES.md` and `MECT_WRITING_RULES.md`. Key rules: AP-PR-07 (be specific), AP-PR-05 (referenceable IDs), MW-VO-01 (active voice), MW-WC-02 (plain language).

## Rule Index

Structure (ST)
- RPT-ST-01 [TYPE-OWNED]: Header block completeness and format
- RPT-ST-02 [STRUCTURE-DEFAULT]: Stand-alone executive summary structure
- RPT-ST-03 [STRUCTURE-DEFAULT]: Action titles for all sections and exhibits
- RPT-ST-04 [TYPE-OWNED]: Appendix vs body separation
- RPT-ST-05 [STRUCTURE-DEFAULT]: Storytelling pass for untechniqued reports

Content (CT)
- RPT-CT-01 [TYPE-OWNED]: Single governing thought answering reader question
- RPT-CT-02 [TYPE-OWNED]: Key-line claims logic and ordering
- RPT-CT-03 [TYPE-OWNED]: Actionable recommendation wording
- RPT-CT-04 [TYPE-OWNED]: Options proposal format and sample bake-off scoring criteria
- RPT-CT-05 [TYPE-OWNED]: Brief recorded in OPTIONS and DRAFT

Evidence & Exhibits (EV)
- RPT-EV-01 [TYPE-OWNED]: Exhibit design and comparison type
- RPT-EV-02 [TYPE-OWNED]: Number placement discipline
- RPT-EV-03 [TYPE-OWNED]: Traceable claim attribution and independent fact-checking verification

Editorial & Release Check (ED / RC)
- RPT-ED-01 [TYPE-OWNED]: Line clarity, active verbs, and Paramedic Method lard factor
- RPT-ED-02 [TYPE-OWNED]: Style sheet consistency across terminology, units, and numbering
- RPT-RC-01 [TYPE-OWNED]: Final release check verification standards

## RPT-ST-01 [TYPE-OWNED]: Header Block Completeness and Format

Output files must begin with a complete six-field header block matching `DRSYNART-FR-24`. Deliverable file names follow `DRSYNART-DD-16`: `[ID]-OPTIONS-NN_[Title].md`, `[ID]-DRAFT-NN_[Title].md`, and `YYYY-MM-DD_[Title].md`.

**BAD:**
```markdown
# Support Platform Consolidation Report

**Author**: Operations Team
**Date**: November 2026
```

**GOOD:**
```markdown
# Support Platform Consolidation Report

**Doc ID**: SUPCON-REPORT-01
**Document Type**: report
**Technique**: MINTO
**Persona**: CXO-ADVISOR
**Audience**: executive leadership
**Source**: SUPCON-DRAFT-01_SupportPlatformConsolidation.md
```

**Verification method**: `/verify` inspects lines 1-15 for the six exact bold keys (`Doc ID`, `Document Type: report`, `Technique`, `Persona`, `Audience`, `Source`) and verifies the Doc ID pattern `[TOPIC]-REPORT-[NN]`.

## RPT-ST-02 [STRUCTURE-DEFAULT]: Stand-Alone Executive Summary Structure

The executive summary must stand completely alone. A reader who reviews nothing else must receive the governing thought, key-line findings, primary empirical evidence, and the recommendation with owner and date. Table-of-contents summaries are prohibited.

**BAD:**
```markdown
## Executive Summary

Section 1 reviews customer ticket volumes. Section 2 discusses regional tooling costs. Section 3 outlines migration steps. Section 4 provides concluding thoughts.
```

**GOOD:**
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

**Verification method**: `/verify` checks that the Executive Summary section contains the governing thought, numbered key findings, and an explicit Recommended Action block with owner and deadline.

## RPT-ST-03 [STRUCTURE-DEFAULT]: Action Titles for All Sections and Exhibits

Every section heading and exhibit title must be an active declarative sentence stating the conclusion, not a generic topic label. Readers skimming headings and exhibits alone must understand the complete storyline.

**BAD:**
```markdown
## Regional Analysis

### Exhibit 2: Regional Performance
[Data table follows...]
```

**GOOD:**
```markdown
## Northern Region Pilot Proved That Shared Queueing Cuts First-Response Times by 53%

### Exhibit 2: Queue Consolidation Reduced Median Response Latency from 9.0 to 4.2 Hours
[Data table follows...]
```

**Verification method**: `/verify` checks that all level-2 and level-3 headings and exhibit titles contain a subject and an active verb rather than a static noun phrase.

## RPT-ST-04 [TYPE-OWNED]: Appendix vs. Body Separation

The report body must contain only executive findings, synthesized storyline, and high-level exhibits. Detailed survey instruments, comprehensive tabular datasets, and calculation scripts must reside in the appendix under progressive disclosure.

**BAD:**
```markdown
## Survey Findings

Below are the 42 survey questions and all 1,200 individual employee responses transcribed verbatim:
[15 pages of raw survey tables follow in the main body...]
```

**GOOD:**
```markdown
## Dispatcher Satisfaction Dropped 40% Under Fragmented Regional Tools

A survey of 120 dispatch staff revealed that 78% attribute shift handover delays to dual-entry logging across regional systems (see Exhibit 4). Detailed survey methodology, complete question sets, and statistical distribution tables are documented in Appendix A.
```

**Verification method**: `/verify` checks that comprehensive raw tables (>20 rows) and methodological tools are located under an `# Appendix` heading.

## RPT-ST-05 [STRUCTURE-DEFAULT]: Storytelling Pass for Untechniqued Reports

When a report is authored without a technique (`Technique: none`), it must follow progressive disclosure: executive summary stating the governing answer, section headings carrying the narrative progression via action titles, and body sections synthesizing findings before presenting supporting tables.

**BAD:**
```markdown
# Annual Operational Report

- Table 1: Expenses
- Table 2: Staffing
- Table 3: Revenue
```

**GOOD:**
```markdown
# Operational Consolidation Unlocks 320k EUR in Annual Redundancy Savings

[Executive summary establishing baseline, complication, and financial recommendation...]

## Duplicate Software Licenses Account for 60% of Administrative Cost Growth

[Synthesized narrative developing root causes, followed by summary exhibit...]

## Unified Procurement Recovers Capital Within Three Fiscal Quarters

[Analysis demonstrating ROI timeline and execution milestones...]
```

**Verification method**: `/verify` checks that untechniqued reports feature an executive summary and narrative synthesis paragraphs preceding data tables.

## RPT-CT-01 [TYPE-OWNED]: Single Governing Thought Answering Reader Question

The entire report must support a single governing thought that directly answers the central question brought by the reader.

**BAD:**
```markdown
# European Market Overview

The European market contains many countries with different languages, currencies, and tax laws.
```

**GOOD:**
```markdown
# Enter the European Logistics Market Through Acquisition by Q3 2027 to Secure Regional Distribution Hubs

Organic expansion would require 36 months to secure warehouse permits; acquiring an established mid-sized operator captures existing gate capacity immediately with positive cash flow in year two.
```

**Verification method**: `/verify` verifies that the title and opening executive summary paragraph state a concrete answer to the decision mandate.

## RPT-CT-02 [TYPE-OWNED]: Key-Line Claims Logic and Ordering

Supporting claims under the governing thought must follow a transparent logical ordering (comparative, chronological, structural, or deductive) and maintain mutually exclusive, collectively exhaustive (MECE) boundaries.

**BAD:**
```markdown
Key claims:
1. Costs are high.
2. Software licenses cost 190k EUR.
3. Things are complicated.
4. Support is slow.
```

**GOOD:**
```markdown
Key claims:
1. Tool fragmentation costs 190k EUR annually in redundant contracts (Cost impact).
2. Cross-region transfers double median customer resolution times to 9 hours (Service quality impact).
3. Migration risk is contained within a four-week operational freeze (Implementation feasibility).
```

**Verification method**: `/verify` inspects key-line claims for distinct, non-overlapping analytical categories.

## RPT-CT-03 [TYPE-OWNED]: Actionable Recommendation Wording

Every recommendation must specify an accountable owner (role or department), an action verb, a concrete deadline, and linked body findings.

**BAD:**
```markdown
Recommendations:
- Look into ticketing tools.
- Modernize workflows when time permits.
```

**GOOD:**
```markdown
### Recommendation 1: Authorize Platform Consolidation
- **Owner**: Head of Customer Operations
- **Action**: Authorize vendor contract and execute unified platform cutover
- **Deadline**: Contract signature by 2026-11-30; complete cutover by 2027-06-30
- **Linked Findings**: Finding F-02 (Duplicate licenses) and Finding F-05 (Transfer latency)
```

**Verification method**: `/verify` checks that all recommendation entries contain the four mandatory fields: Owner, Action, Deadline, and Linked Findings.

## RPT-CT-04 [TYPE-OWNED]: Options Proposal Format and Sample Bake-Off Scoring Criteria

An options proposal (`[ID]-OPTIONS-NN_[Title].md`) written by `/propose-report` must contain a Brief (RPT-CT-05), present candidate options scored against the four standard criteria (Goal Alignment 30%, Supportability 30%, Impact 25%, Specificity 15%), and conclude with one recommended option. Under `compare techniques`, each option carries a scored sample section.

Outline format: every section on its own numbered line (`[Section role]: [Section topic]`), with five fields below it:
- `Goal`: what the section achieves for the reader; cites the Brief `Reader outcome` item it serves
- `Content`: the claim, data, or decision the section presents
- `Evidence`: source finding IDs or key facts; `[ASSUMED]` where no source supports the section
- `Reason`: why the section sits at this position and takes this form
- `Handoff`: the question, consequence, or contrast that leads into the next section; for the last section, the final takeaway or pointer

Field labels are plain text (`- Goal: ...`), never bold. Bold is reserved for the numbered section line. The same applies to every field under the `###` headings of the DRAFT `## Structure` section, including `Diagram placeholder`.

Scoring: Goal Alignment is scored against the Brief `Purpose`, `Governing question`, and `Reader outcome`; Impact against the Brief `Audience` and `Reader outcome`. The Recommendation `Why` names the Brief field behind each of these two scores.

**BAD:**
```markdown
## Option 1: Answer-First Decision Proposal
- **Governing thought**: Consolidate regional ticketing tools onto one platform within 10 months to cut response times by 50%
- **Outline**: Executive Summary -> Cost Redundancy -> Pilot Quality Gains -> Migration Governance -> Recommendations
- **Score**: goal_alignment=5, supportability=5, impact=5, specificity=5 (composite: 5.00)

## Recommendation
- **Option**: 1
- **Why**: Option 1 achieves the highest composite score (5.00).
```

**GOOD:**
```markdown
## Option 1: Answer-First Decision Proposal
- **Governing thought**: Consolidate regional ticketing tools onto one platform within 10 months to cut response times by 50%
- **Outline**:
  1. **Executive Summary**: Consolidate within 10 months; approve 280k EUR budget
     - Goal: Board can approve the budget from this page alone [Reader outcome: do]
     - Content: Governing thought, three key findings, recommendation with owner and date
     - Evidence: SUPCON-IN01 F-01, F-04, F-09
     - Reason: Board members read the first page only; the decision must sit there
     - Handoff: Why consolidate now? -> duplicate license cost
  2. **Key Line 1: Duplicate licenses generate 62% of tooling overhead**
     - Goal: Reader sees the cost of the status quo [Reader outcome: know]
     - Content: License inventory per region, overlap analysis
     - Evidence: SUPCON-IN01 F-04
     - Reason: Cost is the board's first objection; answer it first
     - Handoff: Cost alone does not justify migration risk -> pilot quality data
  3. **Key Line 2: The single-platform pilot halved response times**
     - Goal: Reader believes consolidation improves service [Reader outcome: believe]
     - Content: Pilot region before and after response times
     - Evidence: SUPCON-IN01 F-09
     - Reason: Quality proof turns a cost cut into an improvement
     - Handoff: Can the other regions migrate without service gaps?
  4. **Key Line 3: Staged migration keeps service gaps under one day per region**
     - Goal: Reader trusts the migration plan [Reader outcome: believe]
     - Content: Region sequence, freeze windows, rollback protocol
     - Evidence: SUPCON-IN01 F-12; rollback duration [ASSUMED]
     - Reason: Risk boundaries close the last objection before the ask
     - Handoff: What the board must approve and who owns it
  5. **Recommendations**: Approve budget; appoint migration owner
     - Goal: Board knows exactly what to approve [Reader outcome: do]
     - Content: Owner, action, deadline, linked findings per recommendation
     - Evidence: SUPCON-IN01 F-01, F-04, F-09, F-12
     - Reason: Recommendations follow the proof they rest on
     - Handoff: Calculation details in Appendix
- **Score**: goal_alignment=5, supportability=4, impact=5, specificity=5 (composite: 4.70)

## Recommendation
- **Option**: 1
- **Why**: Goal alignment: answers the Brief Governing question "Should we consolidate regional ticketing tools this fiscal year?" with a dated yes; supportability: every key line traces to findings, one value is marked [ASSUMED]; impact: delivers the Brief Reader outcome "do: approve the 280k EUR budget" for the declared board audience; specificity: names budget, timeline, and response-time target.
```

**Verification method**: `/verify` checks that the options file contains a Brief, repeated option blocks with the four named criteria, outline sections each carrying the five fields `Goal`, `Content`, `Evidence`, `Reason`, `Handoff` with plain (not bold) labels, and a recommendation whose Goal Alignment and Impact sentences name a Brief field.

## RPT-CT-05 [TYPE-OWNED]: Brief Recorded in OPTIONS and DRAFT

Every OPTIONS and DRAFT file must contain a `## Brief` section after the header block, so that a reader or agent can judge options and drafts against the report's goal. Fields: `Mandate` (user request, verbatim), `Purpose`, `Audience` (who, prior knowledge, need), `Reader outcome` (know, believe, do), `Governing question`, `In scope`, `Out of scope`, `Constraints` (length, channel, tone), `Success criteria`. Values the agent derived instead of taking from the user carry `[ASSUMED]`. `/draft-report` copies the Brief from the OPTIONS file (or writes it when no OPTIONS file exists) and records every change in `Brief changes`. `/write-report` never copies the Brief into the output document.

**BAD:**
```markdown
**Source**: _INFO_SUPCON-IN01_Analysis.md
**Scoring criteria**: Goal Alignment (30%), Supportability (30%), Impact (25%), Specificity (15%)

## Option 1: Answer-First Decision Proposal
```

**GOOD:**
```markdown
## Brief
- **Mandate**: "Prepare a board report on consolidating our regional support tools"
- **Purpose**: Obtain board approval for the consolidation budget in the next quarterly meeting [ASSUMED]
- **Audience**: Executive board; knows: support cost totals, not tool overlap; needs: a yes or no with cost and risk
- **Reader outcome**: know: duplicate licenses drive overhead; believe: staged migration is low-risk; do: approve the 280k EUR budget
- **Governing question**: Should we consolidate regional ticketing tools this fiscal year?
- **In scope**: License cost, pilot results, migration plan
- **Out of scope**: Vendor contract negotiation, staffing changes
- **Constraints**: length: 8-12 pages; channel: quarterly board pack; tone: executive, plain
- **Success criteria**: Board approves or rejects the budget in one meeting without follow-up questions
```

**Verification method**: `/verify` checks that OPTIONS and DRAFT files contain a `## Brief` section with all nine fields, that DRAFT files contain `Brief changes`, and that the output document contains no Brief section.

## RPT-EV-01 [TYPE-OWNED]: Exhibit Design and Comparison Type

Every exhibit must carry an action title stating the message, a metric label, and a source line. Chart types must match Zelazny comparison standards. Pie charts for exact numerical values are prohibited.

**BAD:**
```markdown
### Exhibit 1: Cost Breakdown
[3D Pie Chart showing six percentage slices...]
```

**GOOD:**
```markdown
### Exhibit 1: Duplicate Software Licenses Generate 62% of Tooling Overhead

- Metric: Annual software expenditures by regional cost center (FY2025 audited accounts)
- Data format: Structured comparison table
- Source: Enterprise Finance Cost-Center Report, 2025-12
```

**Verification method**: `/verify` verifies that exhibits feature an action title, source line, and appropriate comparison format.

## RPT-EV-02 [TYPE-OWNED]: Number Placement Discipline

Exact numbers belong in structured data tables. Prose sentences must be reserved for stating comparisons, trends, and operational impacts. Duplicating every digit from a table in the adjacent narrative is prohibited.

**BAD:**
```markdown
As shown in Table 1, region A had 4,120 tickets, region B had 3,840 tickets, region C had 2,910 tickets, and region D had 1,420 tickets, totaling 12,290 tickets.
```

**GOOD:**
```markdown
Regional ticket distribution was heavily concentrated: regions A and B generated 65% of all inbound cases, while region D accounted for less than 12% (see Table 1).
```

**Verification method**: `/verify` checks that narrative paragraphs do not list more than two exact numerical values that already appear in an adjacent table.

## RPT-EV-03 [TYPE-OWNED]: Traceable Claim Attribution and Independent Fact-Checking Verification

Every empirical metric, financial calculation, and percentage must be attributed to a registered finding ID or marked `[ASSUMED]`. Fact-checking must be documented before release.

**BAD:**
```markdown
It is widely understood that support tickets cost hundreds of euros to resolve and customers hate waiting.
```

**GOOD:**
```markdown
Manual transfer overhead cost 72k EUR across 13,000 rerouted cases in fiscal year 2025 (Operations Audit Finding F-04).
```

**Verification method**: `/verify` verifies that every factual claim traces to a finding ID or carries an `[ASSUMED]` tag.

## RPT-ED-01 [TYPE-OWNED]: Line Clarity, Active Verbs, and Paramedic Method Lard Factor

Report sentences must lead with institutional actors as subjects and operational decisions as active verbs. Passive nominalizations must be eliminated. The lard factor must remain below one-third.

**BAD:**
```markdown
A determination was made by the executive committee that an evaluation of the system should be initiated. (17 words)
```

**GOOD:**
```markdown
The executive committee decided to evaluate the system. (8 words; lard factor = 52.9%)
```

**Verification method**: `/verify` checks for passive voice constructions (`was made by`) and calculates sentence lard factor.

## RPT-ED-02 [TYPE-OWNED]: Style Sheet Consistency Across Terminology, Units, and Numbering

Terminology, acronym definitions, currency symbols, numerical formats, and exhibit numbers must be consistent with the DRAFT style sheet throughout the report.

**BAD:**
```markdown
In section 2: "280,000 EUR..."
In section 4: "EUR 280k..."
In section 6: "280 thousand Euros..."
```

**GOOD:**
```markdown
Consistently throughout report: "280k EUR" (per DRAFT Style Sheet: Numbers and Units).
```

**Verification method**: `/verify` cross-checks recurring terms and currency formats against the Style Sheet section of the DRAFT file.

## RPT-RC-01 [TYPE-OWNED]: Final Release Check Verification Standards

Before a report is released, it must pass the release check (`DRSYNART-SPEC-8.5`) recorded in the DRAFT file or verification audit:
1. Header fields complete and valid (`Doc ID: [TOPIC]-REPORT-[NN]`, `Document Type: report`, `Technique`, `Persona`, `Audience`, `Source`).
2. Sourcing: every empirical metric cited or marked `[ASSUMED]`.
3. Numbering and cross-references: continuous exhibit numbering; all text references resolve.
4. Presentation hygiene: zero agent prompts, scratchpads, or workflow metadata.
5. Style-pattern signals below threshold: at most 1 signal detected across Sourcing, Style, Structure, and Voice (`AI_WRITING_DETECTION_RULES.md`). Structural signals produced by a technique by construction (such as fixed triad progression in MINTO) are excluded.
6. Persona trait budget respected (when a persona is specified).
7. Word count within target envelope.

**BAD (Incomplete / Failing Record):**
```markdown
## Release Check
- Report verified
- Status: done
```

**GOOD (Valid Release Check Record):**
```markdown
## Release Check

- **Header block**: Complete (Doc ID: SUPCON-REPORT-01, Document Type: report, Technique: MINTO, Persona: CXO-ADVISOR, Audience: executive leadership, Source: SUPCON-DRAFT-01_SupportPlatformConsolidation.md)
- **Claim attribution**: 22 empirical claims verified against audit ledger; 2 future cost projections labeled [ASSUMED]
- **Structural integrity**: Exhibit 1 through Exhibit 6 continuously numbered; all in-text cross-references resolve
- **Metadata hygiene**: Zero agent prompts, scratchpad notes, or workflow tags in body
- **Style-pattern signals**: 0 signals detected (AD-SO: 0, AD-SY: 0, AD-ST: 0, AD-VO: 0); technique structural order excluded
- **Persona compliance**: CXO-ADVISOR register verified; zero informal slang; micro-dose budget respected
- **Word count**: 4,250 words (target: 3,500 - 5,000 words)
- **Status**: PASSED
```

**Verification method**: `/verify` inspects the Release Check record in the DRAFT file or audit output, verifying all seven fields and confirming the `PASSED` status.
