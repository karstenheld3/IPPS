<!-- EBOOK TEMPLATE. Skeletons for ebook planning, drafting, and final output.
Contains three labeled sections: OPTIONS, DRAFT, Output.
Remove all XML comments after creating instantiated documents. -->

## Section: OPTIONS

<!-- Instantiated as [ID]-OPTIONS-NN_[Title].md by /propose-ebook. Labeled lines, no tables. -->

<!-- SLOT: FRAME (type-owned: header block, Brief, scoring criteria) -->

# OPTIONS: [Title]

**Doc ID**: [TOPIC]-[ID]-OPTIONS-[NN]
<!-- [ID] = technique ID or EBOOK; sequence NN is continuous per [ID] in the working folder -->
**Document Type**: ebook
**Technique**: [ID]|none
**Source**: [path to research Summary, analysis INFO, or raw source notes]
**Scoring criteria**: Goal Alignment (30%), Supportability (30%), Reader Transformation Path (25%), Scope Feasibility (15%)

<!-- Brief: written before the options. Records the goal every option is scored against (EBK-CT-05).
Mark every value the agent derived instead of taking from the user with [ASSUMED]. -->

## Brief
- **Mandate**: "[User request, verbatim]"
- **Purpose**: [Why this ebook exists and what it must change]
- **Audience**: [Who reads it]; knows: [prior knowledge and skill baseline]; needs: [capability the reader lacks]
- **Reader outcome**: know: [insight]; believe: [conviction]; do: [capability after the last chapter]
- **Governing question**: [The one question the book answers]
- **In scope**: [Topics covered]
- **Out of scope**: [Topics excluded]
- **Constraints**: length: [chapter count or word range]; channel: [publication or distribution]; tone: [register]
- **Success criteria**: [Observable signal that the ebook achieved its purpose]

<!-- SLOT: SECTIONS (technique-fillable: candidate outline wrapped with Goal, Content, Evidence, Reason, Handoff; without using <ID> the default Section Inventory below applies) -->

<!-- Repeated option block: repeat 3 times (range 2-5).
Outline: parts as group headings; one numbered chapter per line with five fields below each chapter (EBK-CT-04). Chapters match the DRAFT chapters. -->

## Option 1: [Action Title]
- **Promise**: [One-sentence testable reader outcome answering what the reader will be able to do]
- **Reader boundary**: [Target audience persona and explicit negative boundary naming who the book is not for]
- **Outline**:
  - **Part I: [Action Title]**
    1. **Ch 1: [Action Title]**
       - Goal: [Milestone the chapter delivers on the reader's path; cite the Reader outcome item]
       - Content: [Problem scenario, principle, steps, and quick check the chapter presents]
       - Evidence: [Source finding IDs or key facts]|[ASSUMED]
       - Reason: [Why this chapter sits here and takes this form]
       - Handoff: [Question, consequence, or capability gap that leads into Ch 2]
    2. **Ch 2: [Action Title]**
       - Goal: [...]
       - Content: [...]
       - Evidence: [...]
       - Reason: [...]
       - Handoff: [...]
  - **Part II: [Action Title]**
    3. **Ch 3: [Action Title]**
       - Goal: [...]
       - Content: [...]
       - Evidence: [...]
       - Reason: [...]
       - Handoff: [...]
    4. **Ch 4: [Action Title]**
       - Goal: [...]
       - Content: [...]
       - Evidence: [...]
       - Reason: [...]
       - Handoff: [Capability the reader leaves with]
- **Score**: goal_alignment=[1-5], supportability=[1-5], reader_transformation_path=[1-5], scope_feasibility=[1-5] (composite: [N.NN])
- **Sample** (compare techniques only): [Complete sample chapter demonstrating opening hook, principle, steps, and quick check]
  - Sample score: Heuristics passed=[N/10], AI detection signals=[N], bake-off rank=[N]

## Option 2: [Action Title]
- **Promise**: [One-sentence testable reader outcome]
- **Reader boundary**: [Target persona and negative boundary]
- **Outline**:
  <!-- Same structure as Option 1: parts as group headings, every chapter numbered, each with Goal, Content, Evidence, Reason, Handoff -->
  - **Part I: [Action Title]**
    1. **Ch 1: [Action Title]**
       - Goal: [...]
       - Content: [...]
       - Evidence: [...]
       - Reason: [...]
       - Handoff: [...]
- **Score**: goal_alignment=[1-5], supportability=[1-5], reader_transformation_path=[1-5], scope_feasibility=[1-5] (composite: [N.NN])
- **Sample** (compare techniques only): [Complete sample chapter]
  - Sample score: Heuristics passed=[N/10], AI detection signals=[N], bake-off rank=[N]

## Option 3: [Action Title]
- **Promise**: [One-sentence testable reader outcome]
- **Reader boundary**: [Target persona and negative boundary]
- **Outline**:
  <!-- Same structure as Option 1: parts as group headings, every chapter numbered, each with Goal, Content, Evidence, Reason, Handoff -->
  - **Part I: [Action Title]**
    1. **Ch 1: [Action Title]**
       - Goal: [...]
       - Content: [...]
       - Evidence: [...]
       - Reason: [...]
       - Handoff: [...]
- **Score**: goal_alignment=[1-5], supportability=[1-5], reader_transformation_path=[1-5], scope_feasibility=[1-5] (composite: [N.NN])
- **Sample** (compare techniques only): [Complete sample chapter]
  - Sample score: Heuristics passed=[N/10], AI detection signals=[N], bake-off rank=[N]

<!-- END SLOT: SECTIONS -->

<!-- SLOT: FRAME (type-owned: recommendation and scoring rationale) -->

## Recommendation
- **Option**: [N]
- **Why**: [One sentence per criterion explaining why this outline and transformation path was selected over alternatives; the Goal Alignment and Reader Transformation Path sentences name the Brief field they are measured against]

---

## Section: DRAFT

<!-- Instantiated as [ID]-DRAFT-NN_[Title].md by /draft-ebook. Persistent series bible across all chapter prompts. Labeled lines, no tables. -->

<!-- SLOT: FRAME (type-owned: header block, Brief, Promise and Reader Boundaries) -->

# DRAFT: [Title]

**Doc ID**: [TOPIC]-[ID]-DRAFT-[NN]
<!-- [ID] = technique ID or EBOOK; sequence NN is continuous per [ID] in the working folder -->
**Document Type**: ebook
**Technique**: [ID]|none
**Persona**: [PERSONA]|none
**Audience**: [short form]|general
<!-- copied from Brief Audience; Brief is authoritative while a Brief exists; Output header (no Brief) is standalone -->
**Source**: [path to OPTIONS file or raw input]
**Chosen option**: [Option N: Action Title]

<!-- Brief: copied from the OPTIONS file (or written here when no OPTIONS file exists). Log every change in Brief changes.
Never copied into the output document (EBK-CT-05). -->

## Brief
- **Mandate**: "[User request, verbatim]"
- **Purpose**: [Why this ebook exists and what it must change]
- **Audience**: [Who reads it]; knows: [prior knowledge and skill baseline]; needs: [capability the reader lacks]
- **Reader outcome**: know: [insight]; believe: [conviction]; do: [capability after the last chapter]
- **Governing question**: [The one question the book answers]
- **In scope**: [Topics covered]
- **Out of scope**: [Topics excluded]
- **Constraints**: length: [chapter count or word range]; channel: [publication or distribution]; tone: [register]
- **Success criteria**: [Observable signal that the ebook achieved its purpose]
- **Brief changes**: none|[field]: [old value] -> [new value] ([reason])

## Promise and Reader Boundaries
- **One-sentence promise**: [Single testable sentence stating what the reader will be able to do after reading]
- **Target reader**: [Target practitioner persona and skill prerequisites]
- **Who this book is not for**: [Explicit negative audience boundary naming who should not read this book]
- **Reader transformation path**: [Summary tracing reader evolution from initial baseline failure to master capability]
- **Chapter pattern**: [Show-Tell-Apply | textbook | Minto | Diataxis]

<!-- SLOT: SECTIONS (technique-fillable: chapter scaffolding matching chosen option; without using <ID> the default Section Inventory below applies) -->

<!-- Structure: same chapters and field names as the chosen OPTIONS outline. DRAFT adds detail; Content holds fill-in instructions. -->

## Structure

### Part I: [First Part Action Title]
- Phase objective: [Operational capability delivered in Part I]
- Part opener orientation: [Orientation narrative and progress map linking baseline to invariants]

#### Chapter 1: [First Chapter Action Title]
- Goal: [First operational milestone on the reader's transformation path; cite the Reader outcome item]
- Content: [Fill-in instructions: detail initial failure conditions, baseline measurement protocols, and benchmark steps]
- Evidence: [Source finding IDs]|[ASSUMED]
- Reason: [Why the path starts with this milestone]
- Diagram placeholder: [Exhibit 1: Action title stating baseline latency or failure topology; diagram/chart format]
- Handoff: [Content bridge linking Chapter 1 findings to Chapter 2 boundary cut points]

#### Chapter 2: [Second Chapter Action Title]
- Goal: [Second operational milestone advancing toward cluster invariants; cite the Reader outcome item]
- Content: [Fill-in instructions: detail boundary mapping, network cut points, and multi-zone partition isolation]
- Evidence: [Source finding IDs]|[ASSUMED]
- Reason: [Why this milestone follows Chapter 1]
- Diagram placeholder: [Exhibit 2: Action title illustrating zone partition boundaries; architectural schematic]
- Handoff: [Content bridge transitioning baseline measurements to ingestion invariants in Part II]

### Part II: [Second Part Action Title]
- Phase objective: [Operational capability delivered in Part II]
- Part opener orientation: [Orientation narrative and progress map linking invariants to cluster stability]

#### Chapter 3: [Third Chapter Action Title]
- Goal: [Third operational milestone enforcing backpressure under stalls; cite the Reader outcome item]
- Content: [Fill-in instructions: detail queue depth thresholds, HTTP 429 backpressure signalling, and client retry policies]
- Evidence: [Source finding IDs]|[ASSUMED]
- Reason: [Why this milestone opens Part II]
- Diagram placeholder: [Exhibit 3: Action title showing memory consumption under backpressure; line graph]
- Handoff: [Content bridge linking client backpressure to synchronous replication in Chapter 4]

#### Chapter 4: [Fourth Chapter Action Title]
- Goal: [Fourth operational milestone eliminating uncommitted phantom acknowledgments; cite the Reader outcome item]
- Content: [Fill-in instructions: detail commit log quorum configuration, synchronous replication flags, and flush timings]
- Evidence: [Source finding IDs]|[ASSUMED]
- Reason: [Why this milestone follows Chapter 3]
- Diagram placeholder: [Exhibit 4: Action title illustrating replication acknowledgment flow; sequence diagram]
- Handoff: [Content bridge linking persistence invariants to automated recovery in Part III]

### Part III: [Third Part Action Title]
- Phase objective: [Operational capability delivered in Part III]
- Part opener orientation: [Orientation narrative and progress map linking recovery protocols to production certification]

#### Chapter 5: [Fifth Chapter Action Title]
- Goal: [Fifth operational milestone automating cutover without split-brain risk; cite the Reader outcome item]
- Content: [Fill-in instructions: detail leader re-election triggers, split-brain fencing tokens, and automated failover scripts]
- Evidence: [Source finding IDs]|[ASSUMED]
- Reason: [Why recovery comes after persistence invariants]
- Diagram placeholder: [Exhibit 5: Action title demonstrating split-brain fencing mechanism; state diagram]
- Handoff: [Content bridge transitioning automated recovery into chaos testing in Chapter 6]

#### Chapter 6: [Sixth Chapter Action Title]
- Goal: [Final operational milestone certifying zero-loss guarantees under active chaos injection; cite the Reader outcome item]
- Content: [Fill-in instructions: detail synthetic chaos cutover drills, packet drop injection, and data audit reconciliation]
- Evidence: [Source finding IDs]|[ASSUMED]
- Reason: [Why certification closes the transformation path]
- Diagram placeholder: [Exhibit 6: Action title showing message loss reconciliation ledger; data summary]
- Handoff: [Concludes transformation path; bridges to appendices and operational checklists]

<!-- END SLOT: SECTIONS -->

<!-- SLOT: FRAME (type-owned: Evidence Placement, Style Sheet, Chapter Summaries, Open Questions, Release Check) -->

## Evidence Placement
- **Chapter 1**: [Metric 1 -> Benchmark Finding ID], [Metric 2 -> Architecture Source ID]
- **Chapter 2**: [Metric 3 -> Network Ledger ID], [Metric 4 -> Zone Audit ID]
- **Chapter 3**: [Metric 5 -> Memory Benchmark ID], [Metric 6 -> Protocol Spec ID]
- **Chapter 4**: [Metric 7 -> Quorum Ledger ID], [Metric 8 -> Incident Finding ID]
- **Chapter 5**: [Metric 9 -> Failover Test ID], [Metric 10 -> Telemetry Finding ID]
- **Chapter 6**: [Metric 11 -> Chaos Drill Report ID], [Metric 12 -> Reconciliation Audit ID]

## Style Sheet (Series Bible)
- **Terminology**: [Standardized term 1; standardized term 2; banned synonyms]
- **Numbers and Units**: [Currency notation, YYYY-MM-DD dates, latency units e.g. ms, throughput e.g. 100k events/sec]
- **Tone and Conventions**: [Declared mood, pronoun 'you', active voice, technical register per audience]
- **Cross-Reference Format**: [Inline indexing convention: "see Chapter N: [Action Title]"]
- **Recap Convention**: [Formula: "You can now [state capability]. In the next chapter, you will [state next step]."]

## Chapter Summaries (Running Memory)
<!-- Every chapter prompt reads all existing entries and appends a 3-5 sentence entry for each drafted chapter. -->
### Chapter 1 Summary
- **Established**: [Capabilities, baseline metrics, and empirical facts proven in this chapter]
- **Introduced terms**: [New concepts, configuration parameters, and vocabulary defined here]
- **Open threads**: [Promises, unresolved scenarios, or forward links bridged to upcoming chapters]

### Chapter 2 Summary
- **Established**: [Capabilities and facts established]
- **Introduced terms**: [New terms introduced]
- **Open threads**: [Forward promises made]

## Open Questions
- [ ] [Open question 1 for author, technical architect, or fact-checker]
- [ ] [Open question 2]

## Release Check
- **Header block**: [Complete / Pending]
- **Claim attribution**: [All claims verified / [ASSUMED] tags applied]
- **Structural integrity**: [Continuous chapter numbering, all internal links resolve]
- **Metadata hygiene**: [Zero agent prompts or workflow tags in body]
- **Style-pattern signals**: [N signals detected; technique repeating structure excluded]
- **Persona compliance**: [Slider budget and traits respected]
- **Word count**: [Word count against target envelope]
- **Status**: [SELF-CHECKED / FAILED]

---

## Section: Output

<!-- Instantiated as YYYY-MM-DD_[Title].md by /write-ebook. Final publication deliverable. -->
<!-- Release-check record format (recorded in DRAFT or reported in chat response at Tier 1 with Status: SELF-CHECKED):
- **Header block**: [Complete / Pending]
- **Claim attribution**: [All claims verified / [ASSUMED] tags applied]
- **Structural integrity**: [Continuous chapter numbering, all internal links resolve]
- **Metadata hygiene**: [Zero agent prompts or workflow tags in body]
- **Style-pattern signals**: [N signals detected; technique repeating structure excluded]
- **Persona compliance**: [Slider budget and traits respected / N/A]
- **Word count**: [Word count against target envelope]
- **Status**: [SELF-CHECKED / FAILED]
-->

<!-- SLOT: FRAME (type-owned: header block) -->

# [Ebook Title]

**Doc ID**: [TOPIC]-EBOOK-[NN]
**Document Type**: ebook
**Technique**: [ID]|none
**Persona**: [PERSONA]|none
**Audience**: [free text]|general
**Source**: [path to DRAFT or OPTIONS file, or input path]

<!-- SLOT: SECTIONS (technique-fillable: output body prose skeleton; without using <ID> the default Section Inventory below applies) -->

## Introduction: The Production Contract

<!-- Mutual contract defining promise, reader boundaries, and prerequisites; or forgone if starting with Chapter 1. -->

[One-sentence promise stating what the reader will be able to do after reading this handbook.]

[Negative reader boundary naming who this book is for and who should not read it.]

[Prerequisites, required tool environment, and overview of the transformation path.]

## Contents

<!-- Table of contents as an argument: action titles asserting operational steps. -->

### Part I: [First Part Action Title]
1. [Chapter 1 Action Title]
2. [Chapter 2 Action Title]

### Part II: [Second Part Action Title]
3. [Chapter 3 Action Title]
4. [Chapter 4 Action Title]

### Part III: [Third Part Action Title]
5. [Chapter 5 Action Title]
6. [Chapter 6 Action Title]

# Part I: [First Part Action Title]

<!-- Part opener orientation narrative and progress map. -->

[Orientation narrative explaining the operational phase and how it builds on initial prerequisites.]

Progress map:
- [>] Part I: [First Part Action Title] (Chapters 1-2) [Active]
- [ ] Part II: [Second Part Action Title] (Chapters 3-4)
- [ ] Part III: [Third Part Action Title] (Chapters 5-6)

# Chapter 1: [First Chapter Action Title]

<!-- First chapter following repeating pedagogical pattern (Show-Tell-Apply illustrated). -->

## [The Recognized Production Failure Case or Advance Organizer]

[Four to six sentences detailing a concrete recognized failure with specific metrics (SHOW).]

## [The Governing Operational Principle]

[One-sentence principle explaining why the failure occurs and what rule prevents it (TELL).]

[Supporting mechanism paragraphs explaining the invariant.]

## [How to Implement the Invariant]

1. [Numbered action step 1 with exact commands or configurations.]
2. [Numbered action step 2 with expected immediate output.]
3. [Numbered action step 3 detailing verification.]
4. [Numbered action step 4 detailing telemetry or monitoring.]

Quick check: [Immediate 15-minute observable verification action.]

## Chapter Recap

You can now [state newly gained practitioner capability]. In the next chapter, you will [state next transformation step linking forward to Chapter 2].

# Chapter 2: [Second Chapter Action Title]

<!-- Second chapter repeating the pedagogical structure. -->

## [Opening Problem or Advance Organizer]

[Concrete case or advance organizer (SHOW)...]

## [Governing Operational Principle]

[Governing principle (TELL)...]

## [How to Implement the Invariant]

1. [Numbered action step 1...]
2. [Numbered action step 2...]
3. [Numbered action step 3...]

Quick check: [Immediate verification test...]

## Chapter Recap

You can now [state capability]. In the next chapter, you will [state next step linking forward to Part II].

# Appendix A: [Operational Reference and Tool Checklists]

<!-- Supplementary reference materials, full configuration files, and checklists. -->

### A.1 Cluster Configuration Checklist
[Verification checklist items...]

### A.2 Benchmark Commands Reference
[Command-line reference listings...]

# Glossary

<!-- Alphabetical index of terms introduced across chapters. -->

- **[Term 1]**: [Definition matching DRAFT Style Sheet usage.]
- **[Term 2]**: [Definition matching DRAFT Style Sheet usage.]

<!-- END SLOT: SECTIONS -->
