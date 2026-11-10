<!-- REPORT TEMPLATE. Skeletons for report planning, drafting, and final output.
Contains three labeled sections: OPTIONS, DRAFT, Output.
Remove all XML comments after creating instantiated documents. -->

## Section: OPTIONS

<!-- Instantiated as [ID]-OPTIONS-NN_[Title].md by /propose-report. Labeled lines, no tables. -->

<!-- SLOT: FRAME (type-owned: header block, Brief, scoring criteria) -->

# OPTIONS: [Title]

**Doc ID**: [TOPIC]-[ID]-OPTIONS-[NN]
<!-- [ID] = technique ID or REPORT; sequence NN is continuous per [ID] in the working folder -->
**Document Type**: report
**Technique**: [ID]|none
**Source**: [path to research Summary, analysis INFO, or raw source notes]
**Scoring criteria**: Goal Alignment (30%), Supportability (30%), Impact (25%), Specificity (15%)

<!-- Brief: written before the options. Records the goal every option is scored against (RPT-CT-05).
Mark every value the agent derived instead of taking from the user with [ASSUMED]. -->

## Brief
- **Mandate**: "[User request, verbatim]"
- **Purpose**: [Why this report exists and which decision it supports]
- **Audience**: [Who reads it]; knows: [prior knowledge]; needs: [what the reader needs from the report]
- **Reader outcome**: know: [insight]; believe: [conviction]; do: [decision or action]
- **Governing question**: [The one question the governing thought answers]
- **In scope**: [Topics covered]
- **Out of scope**: [Topics excluded]
- **Constraints**: length: [page or word range]; channel: [board pack, client deliverable, publication]; tone: [register]
- **Success criteria**: [Observable signal that the report achieved its purpose]

<!-- SLOT: SECTIONS (technique-fillable: candidate outline wrapped with Goal, Content, Evidence, Reason, Handoff; without using <ID> the default Section Inventory below applies) -->

<!-- Repeated option block: repeat 3 times (range 2-5).
Outline: one numbered section per line, five fields below each section (RPT-CT-04). Sections match the DRAFT sections. -->

## Option 1: [Action Title]
- **Governing thought**: [One-sentence governing answer resolving the client or research mandate]
- **Outline**:
  1. **Executive Summary**: [Governing answer and decision]
     - Goal: [What the section achieves for the reader; cite the Reader outcome item]
     - Content: [Governing thought, top findings, recommendation]
     - Evidence: [Source finding IDs or key facts]|[ASSUMED]
     - Reason: [Why this section sits here and takes this form]
     - Handoff: [Question, consequence, or contrast that leads into section 2]
  2. **Key Line 1: [Action title]**
     - Goal: [...]
     - Content: [...]
     - Evidence: [...]
     - Reason: [...]
     - Handoff: [...]
  3. **Key Line 2: [Action title]**
     - Goal: [...]
     - Content: [...]
     - Evidence: [...]
     - Reason: [...]
     - Handoff: [...]
  4. **Key Line 3: [Action title]**
     - Goal: [...]
     - Content: [...]
     - Evidence: [...]
     - Reason: [...]
     - Handoff: [...]
  5. **Recommendations**: [Accountable actions]
     - Goal: [...]
     - Content: [...]
     - Evidence: [...]
     - Reason: [...]
     - Handoff: [...]
  6. **Appendix**: [Supporting material]
     - Goal: [...]
     - Content: [...]
     - Evidence: [...]
     - Reason: [...]
     - Handoff: [Final takeaway or pointer for specialists]
- **Score**: goal_alignment=[1-5], supportability=[1-5], impact=[1-5], specificity=[1-5] (composite: [N.NN])
- **Sample** (compare techniques only): [Sample section demonstrating opening executive summary and key line]
  - Sample score: Heuristics passed=[N/6], AI detection signals=[N], bake-off rank=[N]

## Option 2: [Action Title]
- **Governing thought**: [One-sentence governing answer]
- **Outline**:
  <!-- Same structure as Option 1: every section numbered, each with Goal, Content, Evidence, Reason, Handoff -->
  1. **[Section role]: [Section topic]**
     - Goal: [...]
     - Content: [...]
     - Evidence: [...]
     - Reason: [...]
     - Handoff: [...]
- **Score**: goal_alignment=[1-5], supportability=[1-5], impact=[1-5], specificity=[1-5] (composite: [N.NN])
- **Sample** (compare techniques only): [Sample section]
  - Sample score: Heuristics passed=[N/6], AI detection signals=[N], bake-off rank=[N]

## Option 3: [Action Title]
- **Governing thought**: [One-sentence governing answer]
- **Outline**:
  <!-- Same structure as Option 1: every section numbered, each with Goal, Content, Evidence, Reason, Handoff -->
  1. **[Section role]: [Section topic]**
     - Goal: [...]
     - Content: [...]
     - Evidence: [...]
     - Reason: [...]
     - Handoff: [...]
- **Score**: goal_alignment=[1-5], supportability=[1-5], impact=[1-5], specificity=[1-5] (composite: [N.NN])
- **Sample** (compare techniques only): [Sample section]
  - Sample score: Heuristics passed=[N/6], AI detection signals=[N], bake-off rank=[N]

<!-- END SLOT: SECTIONS -->

<!-- SLOT: FRAME (type-owned: recommendation and scoring rationale) -->

## Recommendation
- **Option**: [N]
- **Why**: [One sentence per criterion explaining why this candidate was selected over alternatives; the Goal Alignment and Impact sentences name the Brief field they are measured against]

---

## Section: DRAFT

<!-- Instantiated as [ID]-DRAFT-NN_[Title].md by /draft-report. Labeled lines, no tables. -->

<!-- SLOT: FRAME (type-owned: header block, Brief) -->

# DRAFT: [Title]

**Doc ID**: [TOPIC]-[ID]-DRAFT-[NN]
<!-- [ID] = technique ID or REPORT; sequence NN is continuous per [ID] in the working folder -->
**Document Type**: report
**Technique**: [ID]|none
**Persona**: [PERSONA]|none
**Audience**: [short form]|general
<!-- copied from Brief Audience; Brief is authoritative while a Brief exists; Output header (no Brief) is standalone -->
**Source**: [path to OPTIONS file or raw input]
**Chosen option**: [Option N: Action Title]

<!-- Brief: copied from the OPTIONS file (or written here when no OPTIONS file exists). Log every change in Brief changes.
Never copied into the output document (RPT-CT-05). -->

## Brief
- **Mandate**: "[User request, verbatim]"
- **Purpose**: [Why this report exists and which decision it supports]
- **Audience**: [Who reads it]; knows: [prior knowledge]; needs: [what the reader needs from the report]
- **Reader outcome**: know: [insight]; believe: [conviction]; do: [decision or action]
- **Governing question**: [The one question the governing thought answers]
- **In scope**: [Topics covered]
- **Out of scope**: [Topics excluded]
- **Constraints**: length: [page or word range]; channel: [board pack, client deliverable, publication]; tone: [register]
- **Success criteria**: [Observable signal that the report achieved its purpose]
- **Brief changes**: none|[field]: [old value] -> [new value] ([reason])

<!-- SLOT: SECTIONS (technique-fillable: section scaffolding matching chosen option; without using <ID> the default Section Inventory below applies) -->

<!-- Structure: same sections and field names as the chosen OPTIONS outline. DRAFT adds detail; Content holds fill-in instructions. -->

## Structure

### Executive Summary: [Stand-Alone Executive Summary]
- Goal: [Deliver governing thought, top 3-5 findings, and full recommendation with owner and date; cite the Reader outcome item]
- Content: [Fill-in instructions: draft after body chapters are stable; condense core evidence without table-of-contents lists]
- Evidence: [Source finding IDs]|[ASSUMED]
- Reason: [Why the answer comes first for this audience]
- Handoff: [Provides executive closure; links to Chapter 1 for detailed operational proof]

### Chapter 1: [First Key-Line Action Title]
- Goal: [Prove first supporting claim beneath governing thought; cite the Reader outcome item]
- Content: [Fill-in instructions: insert baseline operational data, cost impact calculations, and root-cause analysis]
- Evidence: [Source finding IDs]|[ASSUMED]
- Reason: [Why this key line comes first]
- Diagram placeholder: [Exhibit 1: Action title stating primary cost or operational comparison; chart/table format]
- Handoff: [Content bridge linking cost impact to operational quality in Chapter 2]

### Chapter 2: [Second Key-Line Action Title]
- Goal: [Prove second supporting claim beneath governing thought; cite the Reader outcome item]
- Content: [Fill-in instructions: document pilot results, performance metrics, and service-level data]
- Evidence: [Source finding IDs]|[ASSUMED]
- Reason: [Why this key line follows Chapter 1]
- Diagram placeholder: [Exhibit 2: Action title stating quality latency reduction; time series or bar chart format]
- Handoff: [Content bridge linking quality gains to implementation feasibility in Chapter 3]

### Chapter 3: [Third Key-Line Action Title]
- Goal: [Prove third supporting claim and address operational risk boundaries; cite the Reader outcome item]
- Content: [Fill-in instructions: analyze migration risks, operational change freeze windows, and contingency protocols]
- Evidence: [Source finding IDs]|[ASSUMED]
- Reason: [Why risk boundaries close the proof]
- Diagram placeholder: [Exhibit 3: Action title stating milestone schedule or risk matrix; table format]
- Handoff: [Content bridge transitioning proof into actionable recommendations]

### Chapter 4: [Actionable Recommendations]
- Goal: [Present accountable recommendations with owner, action, deadline, and linked findings; cite the Reader outcome item]
- Content: [Fill-in instructions: formulate recommendations as active mandates; verify every item traces to Chapter 1-3 findings]
- Evidence: [Finding IDs per recommendation]
- Reason: [Why recommendations follow the proof chapters]
- Handoff: [Directs technical specialists to Appendix for calculation scripts and raw data]

### Appendix: [Methodology and Supplementary Datasets]
- Goal: [Host detailed survey instruments, raw data tables, calculation scripts, and questionnaires]
- Content: [Fill-in instructions: compile technical appendices under progressive disclosure; keep out of main body]
- Evidence: [Dataset and source IDs]
- Reason: [Why this material stays out of the main body]
- Handoff: [Final pointer for specialists]

<!-- END SLOT: SECTIONS -->

<!-- SLOT: FRAME (type-owned: Evidence Placement, Style Sheet, Open Questions, Release Check) -->

## Evidence Placement
- **Chapter 1**: [Claim 1 -> Source ID], [Claim 2 -> Source ID]
- **Chapter 2**: [Claim 3 -> Source ID], [Claim 4 -> Source ID]
- **Chapter 3**: [Claim 5 -> Source ID], [Claim 6 -> Source ID]
- **Chapter 4**: [Recommendation 1 -> Findings F-02, F-05]
- **Appendix**: [Dataset 1 -> Audit Ledger], [Survey Data -> Source ID]

## Style Sheet
- **Terminology**: [Standardized term 1; standardized term 2]
- **Numbers and Units**: [Currency notation e.g. 280k EUR, YYYY-MM-DD date format, percentage decimals]
- **Tone and Unity**: [Declared mood, pronoun, tense, narrative distance]
- **Cross-Reference Format**: [Exhibit citation format e.g. "see Exhibit 2", finding cross-reference convention]

## Open Questions
- [ ] [Open question 1 for client, author, or fact-checker]
- [ ] [Open question 2]

## Release Check
- **Header block**: [Complete / Pending]
- **Claim attribution**: [All claims verified / [ASSUMED] tags applied]
- **Structural integrity**: [Continuous exhibit numbering, all internal links resolve]
- **Metadata hygiene**: [Zero agent prompts or workflow tags in body]
- **Style-pattern signals**: [N signals detected; technique structural order excluded]
- **Persona compliance**: [Slider budget and traits respected]
- **Word count**: [Word count against target]
- **Status**: [SELF-CHECKED / FAILED]

---

## Section: Output

<!-- Instantiated as YYYY-MM-DD_[Title].md by /write-report. Final publication deliverable. -->
<!-- Release-check record format (recorded in DRAFT or reported in chat response at Tier 1 with Status: SELF-CHECKED):
- **Header block**: [Complete / Pending]
- **Claim attribution**: [All claims verified / [ASSUMED] tags applied]
- **Structural integrity**: [Continuous exhibit numbering, all internal links resolve]
- **Metadata hygiene**: [Zero agent prompts or workflow tags in body]
- **Style-pattern signals**: [N signals detected; technique structural order excluded]
- **Persona compliance**: [Slider budget and traits respected / N/A]
- **Word count**: [Word count against target]
- **Status**: [SELF-CHECKED / FAILED]
-->

<!-- SLOT: FRAME (type-owned: header block) -->

# [Report Title]

**Doc ID**: [TOPIC]-REPORT-[NN]
**Document Type**: report
**Technique**: [ID]|none
**Persona**: [PERSONA]|none
**Audience**: [free text]|general
**Source**: [path to DRAFT or OPTIONS file, or input path]

<!-- SLOT: SECTIONS (technique-fillable: output body prose skeleton; without using <ID> the default Section Inventory below applies) -->

## Executive Summary

<!-- Condensed stand-alone report: governing thought, key findings, and actionable recommendation block. -->

[Governing thought paragraph answering central decision mandate.]

Key findings:
1. [First key-line finding with quantified metric.]
2. [Second key-line finding with quantified metric.]
3. [Third key-line finding with feasibility or risk metric.]

### Recommended Action
- **Owner**: [Role or department]
- **Action**: [Active operational mandate]
- **Target Date**: [Enforceable completion date YYYY-MM-DD]
- **Linked Findings**: [Finding IDs]

## [Chapter 1 Action Title]

<!-- First body chapter: opens with claim, synthesizes findings, introduces Exhibit 1. -->

[Chapter 1 synthesized narrative paragraphs...]

### Exhibit 1: [Action Title Stating Conclusion]
- Metric: [Metric description]
- Data format: [Table or chart description]
- Source: [Source attribution line]

[Prose explaining operational takeaways without duplicating exact digits...]

## [Chapter 2 Action Title]

<!-- Second body chapter: proves second claim, introduces Exhibit 2. -->

[Chapter 2 narrative paragraphs...]

### Exhibit 2: [Action Title Stating Conclusion]
- Metric: [Metric description]
- Data format: [Table or chart description]
- Source: [Source attribution line]

[Prose explaining takeaways...]

## [Chapter 3 Action Title]

<!-- Third body chapter: proves third claim, addresses counterpoint/risk, introduces Exhibit 3. -->

[Chapter 3 narrative paragraphs...]

### Exhibit 3: [Action Title Stating Conclusion]
- Metric: [Metric description]
- Data format: [Table or chart description]
- Source: [Source attribution line]

[Prose explaining takeaways...]

## [Chapter 4: Actionable Recommendations]

<!-- Actionable recommendations with owner, action, deadline, and linked findings. -->

### Recommendation 1: [Action Title]
- **Owner**: [Accountable role or department]
- **Action**: [Concrete operational action]
- **Deadline**: [Target completion date YYYY-MM-DD]
- **Linked Findings**: [Finding IDs from Chapter 1-3]

## Appendix A: [Methodology and Supplementary Datasets]

<!-- Progressive disclosure: detailed survey instruments, raw data tables, and calculation notes. -->

### A.1 Methodology and Data Sources
[Detailed methodology description...]

### A.2 Supplementary Datasets
[Extended tabular data...]

<!-- END SLOT: SECTIONS -->
