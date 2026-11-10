# Ebook Guide

Read BEFORE writing a practitioner ebook, handbook, long-form guide, or user manual with `/propose-ebook`, `/draft-ebook`, or `/write-ebook`.

## 1. Purpose and Reader Outcome

After reading this GUIDE, you can plan, structure, and write a practitioner ebook from promised outcome to final stitched manuscript. You can formulate a testable one-sentence promise paired with a negative audience boundary, derive chapter sequences from the reader's transformation path, apply a consistent repeating pedagogical pattern (Show-Tell-Apply, textbook, Minto, or Diataxis), craft advance organizers and concrete problem openings, design an action-title table of contents that reads as an argument, establish forward and backward inline indexing, maintain cross-chapter consistency through a DRAFT style sheet and running chapter summaries, execute multi-prompt tier-3 workflows without drift, and verify publication readiness through formal release checks.

## 2. Ebook Craft Decisions in Working Order

Every ebook follows ten core craft decisions, executed in the sequence below.

### Decision 1: One-Sentence Promise

- **Question**: What will the reader be able to do after reading this book that they cannot do now?
- **Options**:
  - Topic description: "A comprehensive handbook on distributed queue architectures."
  - Title statement: "The Production Queue Reliability Handbook."
  - Table of contents list: "Twelve chapters covering queue topologies, partitioning, failover, and metrics."
  - Testable promise: "After reading this handbook, you will design and operate a message queue cluster handling 100k events per second with zero message loss during regional network partitions."
- **Criterion**: Choose the testable promise. The promise must be one declarative sentence stating an observable reader outcome. It must be testable: a reader or beta tester can answer "did the book deliver this capability?" with a definitive yes or no. Every chapter must directly advance the reader toward delivering this outcome. A topic is not a promise; a title is not a promise; a table of contents is not a promise.
- **Source**: Rob Fitzpatrick, *Write Useful Books*.
- **Rule Reference**: `EBK-CT-01`.

### Decision 2: Who the Book Is Not For (Negative Reader Boundary)

- **Question**: Which readers should explicitly not buy or read this book?
- **Options**:
  - Universal audience: "For software engineers, managers, architects, and technical professionals of all experience levels."
  - Target persona only: "For senior site reliability engineers who manage production message brokers."
  - Persona combined with negative boundary: "For infrastructure engineers who already operate Linux production clusters but have never tuned distributed commit logs; not for queue platform developers building consensus engines from scratch, and not for engineers without basic networking and container experience."
- **Criterion**: Choose the negative boundary alongside the target persona. Naming who the book is not for prevents scope creep, protects the technical register from dilution, and gives beta readers a clear standard to judge relevance. A book written for everyone serves no one.
- **Source**: Rob Fitzpatrick, *Write Useful Books*.
- **Rule Reference**: `EBK-CT-01`, `EBK-CT-03`.

### Decision 3: Deriving Chapter Count and Sequence from the Reader's Path

- **Question**: How many chapters does the book contain, and what principle governs their order?
- **Options**:
  - Author knowledge map: "Chapter 1: History of Queuing, Chapter 2: Theoretical Consensus Models, Chapter 3: Wire Protocols, Chapter 4: Broker Architecture."
  - Competitor table of contents: mirroring the chapter breakdown of existing commercial manuals.
  - Reader transformation path: "Chapter 1: Measure partition baseline latency, Chapter 2: Configure synchronous replicas, Chapter 3: Enforce client backpressure, Chapter 4: Automate regional cutover."
- **Criterion**: Base chapter count and sequence strictly on the reader's path from their initial problem state to the promised capability. Each chapter is an indispensable milestone on that journey, not a category in the author's personal knowledge map. If removing a chapter does not break the reader's ability to reach the promise, that chapter does not earn its place and must be cut.
- **Source**: Reedsy, *How to Write a Book Proposal*; Rob Fitzpatrick, *Write Useful Books*.
- **Rule Reference**: `EBK-CT-02`.

### Decision 4: Repeating Chapter Pattern

- **Question**: What internal pedagogical architecture governs every chapter?
- **Options**:
  - Unstructured narrative: free-form prose with arbitrary topical subheadings.
  - Academic textbook pattern: formal abstract, theoretical exposition, summary, review questions.
  - Minto pyramid: governing answer first, inductive/deductive key line, drill-down evidence.
  - Show-Tell-Apply (STA): open with a concrete recognizable failure or case (SHOW), state the governing principle in one sentence (TELL), provide numbered action steps the reader applies (APPLY), and close with a quick check and forward link.
- **Criterion**: For practitioner books teaching actionable skills, use Show-Tell-Apply. For argument-driven books making a policy or strategic case, use Minto pyramid. For reference manuals and how-to guides, use Diataxis. The chosen pattern must repeat consistently across all chapters so returning readers know where to find principles, steps, and tests. Deviate only when a chapter explicitly states why its content requires a different structure.
- **Source**: Show-Tell-Apply Guide (`STA_GUIDES.md`); Rob Fitzpatrick, *Write Useful Books*.
- **Rule Reference**: `EBK-ST-04`.

#### Annotated Excerpt 1: Chapter Opening and Repeating Pattern Using Show-Tell-Apply

```markdown
# Chapter 3: Enforce Client Backpressure Under Network Stalls

## The broker that ran out of memory in 90 seconds

Composite case from regional logistics hubs: at 08:14 on a Monday, a fiber cut isolated the Frankfurt ingestion broker from its primary downstream database. Ingestion workers continued accepting client HTTP payloads at 18,000 requests per second. With downstream database flushes blocked and in-memory request buffering unconstrained, the broker heap exhausted all 32 GB of memory within 88 seconds, crashing the container and terminating 4,200 active client TCP sockets.

## A broker must reject traffic before memory exhausts

Accepting traffic that downstream storage cannot persist is not resilience; it is deferred data corruption. A resilient broker signals backpressure upstream the instant downstream ingestion latency exceeds processing thresholds.

The mechanism is straightforward: when internal queue depth crosses 70% capacity, worker nodes return HTTP 429 Retry-After responses rather than buffering unbounded payloads in RAM. Client SDKs back off exponentially, preserving broker stability until connectivity restores.

## How to configure proactive backpressure thresholds

1. Measure your average database batch flush duration under normal operating load (baseline: 45 ms).
2. Set `max_in_flight_requests_per_connection` to a static ceiling of 64 on client producer configurations.
3. Define broker queue watermark policies: trigger warning telemetry at 60% capacity; return HTTP 429 at 75% capacity.
4. Configure client SDK exponential backoff with jitter: minimum delay 100 ms, maximum delay 5,000 ms, multiplier 1.5.
5. Deploy a synthetic traffic probe generating 20,000 requests per second while downstream databases are temporarily paused.

Quick check: under a 60-second downstream freeze, the broker memory consumption remains flat and clients report HTTP 429 responses with valid Retry-After headers.

## What would have changed on Monday

If Frankfurt had enforced queue watermarks at 75% capacity, memory usage would have plateaued at 24 GB. The broker would have rejected excess requests cleanly, allowing clients to retry safely once the fiber cut was repaired at 08:35 without a single container crash.
```

*What makes this work*: The chapter opens with an immediate, concrete failure scenario containing specific numbers (SHOW). The governing rule is stated directly in one sentence (TELL). Five numbered, tool-independent steps instruct the reader exactly how to configure thresholds (APPLY). An immediate 15-minute quick check verifies the behavior, and the closing section reconnects to the opening case.

### Decision 5: Chapter Opening Discipline (Advance Organizer vs. Concrete Problem)

- **Question**: What must the first section of every chapter accomplish?
- **Options**:
  - Table-of-contents summary: "In this chapter, we will discuss connection pools, thread starvation, and configuration flags."
  - Theoretical definition: "A connection pool is a cache of database connections maintained so that connections can be reused."
  - Concrete recognized problem (SHOW): an immediate, relatable production failure showing what goes wrong without the principle.
  - Ausubel advance organizer: an introductory passage at a higher level of abstraction, generality, and inclusiveness that links the new material to existing mental models before technical details begin.
- **Criterion**: Choose either a concrete recognized problem (for practitioner engagement) or an advance organizer (for conceptual scaffolding). Never write a summary of upcoming topics; it explains what the chapter covers without giving the reader a reason to care.
- **Source**: David Ausubel, *Advance Organizers in Educational Psychology*; Rob Fitzpatrick, *Write Useful Books*.
- **Rule Reference**: `EBK-ST-04`.

### Decision 6: Forward and Backward Cross-Referencing and Inline Indexing

- **Question**: How do chapters interconnect to serve non-linear readers?
- **Options**:
  - Isolated chapters: zero cross-references; assumes linear cover-to-cover reading.
  - Vague references: implicit callbacks ("as noted previously", "as will be discussed later").
  - Explicit chapter cross-references with inline indexing: "see Chapter 2: Configure Synchronous Replicas" or "see Section 4.2 for buffer allocation".
- **Criterion**: Use explicit cross-references with chapter numbers and action titles ("inline indexing"). Nonfiction ebooks are reference artifacts accessed non-linearly. When a later chapter relies on an earlier concept, name the exact chapter and title. Close every chapter with a through-line link pointing to the immediate next step.
- **Source**: Rob Fitzpatrick, *Write Useful Books* (Nonfiction Design Patterns: Inline Indexing).
- **Rule Reference**: `EBK-EV-02`.

### Decision 7: Placement and Scope of Exercises and Checklists

- **Question**: Where do exercises, worksheets, and verification checks belong, and what tools do they require?
- **Options**:
  - End-of-book appendix: all worksheets collected at the back matter.
  - Inline application steps and quick check: numbered action steps in the chapter body, completed with a 15-minute quick check at chapter close.
  - Proprietary-tool exercise: exercises requiring the author's custom scripts or paid software.
- **Criterion**: Put actionable application steps inline in the chapter body, followed by a quick check at chapter close. Every exercise must be executable using standard industry tools or generic environments without author-specific dependencies.
- **Source**: Show-Tell-Apply Guide (`STA_GUIDES.md`).
- **Rule Reference**: `EBK-EV-01`.

### Decision 8: Part Structure and Navigation Maps

- **Question**: When does an ebook require grouping into parts, and what apparatus accompanies each part?
- **Options**:
  - Flat structure: Chapter 1 through Chapter N in a single unbroken sequence.
  - Part structure without openers: dividing chapters under "Part I", "Part II" without introductory text.
  - Standalone parts with progress maps: grouping chapters into major operational phases, opening each part with a standalone orientation and a visual "you are here" progress map.
- **Criterion**: Use a flat sequence for short ebooks under 10 chapters. When an ebook exceeds 10 chapters or encompasses distinct operational phases (Foundations, Production Implementation, Failure Resilience), use standalone parts. Each part opener must orient the reader independently and display a map of progress through the book.
- **Source**: Rob Fitzpatrick, *Write Useful Books* (Standalone Parts and Map of Progress).
- **Rule Reference**: `EBK-ST-05`.

### Decision 9: Table of Contents as an Argument

- **Question**: How is the table of contents formulated?
- **Options**:
  - Noun-phrase list: "Chapter 1: Introduction, Chapter 2: Architecture, Chapter 3: Failover, Chapter 4: Monitoring."
  - Question-based list: "Chapter 1: Why do partitions occur? Chapter 2: How to configure brokers?"
  - Action-title argument: declarative imperative titles tracing the complete transformation path ("Chapter 1: Measure partition baseline latency, Chapter 2: Isolate message loss with synchronous replicas, Chapter 3: Enforce client backpressure under network stalls").
- **Criterion**: Write the table of contents as an action-title argument. Scanning the table of contents alone must lay out the complete argument and methodology for delivering the promise. A reader reviewing only the table of contents must understand the sequence of actions that achieves the book outcome.
- **Source**: Reedsy, *How to Write a Book Proposal*; Chicago Manual of Style (CMOS), 18th Edition.
- **Rule Reference**: `EBK-ST-03`.

#### Annotated Excerpt 2: Table of Contents That Reads as an Argument

```markdown
# Contents

## Part I: Measure the Failure Horizon
1. Measure partition baseline latency before configuring replication
2. Identify network boundary cut points in multi-zone clusters

## Part II: Enforce Ingestion Invariants
3. Enforce client backpressure under network stalls
4. Configure synchronous replicas to eliminate phantom writes
5. Drain in-flight buffers safely during broker restarts

## Part III: Automate Production Recovery
6. Automate regional broker cutover without split-brain risk
7. Reconcile partitioned sequence logs across multi-master storage
8. Run chaos cutover drills to certify zero-loss guarantees
```

*What makes this work*: Every chapter title uses an active verb expressing an operational step rather than a passive noun phrase like "Replication Configurations". The sequence demonstrates the argument: measure the failure horizon, enforce invariants in the cluster, and automate recovery. Scanning the list reveals the entire engineering path.

### Decision 10: Introduction Contract vs. Forgoing Front Matter

- **Question**: What does the introduction accomplish, and when should front matter be omitted?
- **Options**:
  - Chapter-by-chapter preview: summarizing the contents of every chapter in order.
  - Personal author memoir: personal narrative explaining how the author discovered the topic.
  - Introduction contract: a concise 1-3 page agreement defining the promise, naming who the book is for and not for, outlining the reader's journey, and setting expectations.
  - Forgo front matter: omitting prefatory material entirely and starting directly with Chapter 1's opening hook.
- **Criterion**: For practitioner ebooks, write an introduction contract or forgo front matter. If an introduction is present, it must function as a mutual contract, never a chapter-by-chapter plot summary. For short tactical handbooks where engagement is critical, begin directly with Chapter 1.
- **Source**: Rob Fitzpatrick, *Write Useful Books* (Forgo the Front-Matter); Chicago Manual of Style (CMOS), 18th Edition.
- **Rule Reference**: `EBK-ST-02`.

### Technique Override Rule (`using <ID>`)

When the user passes `using <ID>` (e.g., `using MINTO`, `using STA`, or `using DIATAXIS`):
- The technique implements the document type's Slot Contract (`DRSYNART-DD-44`) with five fusion assignments:
  1. **Header block = type**: `FRAME` slot (`Doc ID`, `Document Type: ebook`, `Technique`, `Persona`, `Audience`, `Source`) is owned by the ebook type.
  2. **Scaffolding and governance = type**: `FRAME` slot (Brief, scoring criteria, Promise and Reader Boundaries, Chapter Summaries, Style Sheet, multi-pass stitching, and Release Check) is owned by the ebook type.
  3. **Section inventory and order = technique**: `SECTIONS` slot is filled by the technique's exported Section Inventory (TOC, part progression, and chapter sequence are determined by the technique).
  4. **Outline wrapping**: In OPTIONS and DRAFT, each technique chapter entry is wrapped with the five DD-43 outline fields (`Goal`, `Content`, `Evidence`, `Reason`, `Handoff`).
  5. **Technique exemptions**: Any stage exemptions (such as MINTO's AMINTON Q/A tree in OPTIONS) live in the technique's own GUIDES, not in type files or session notes.
- Without `using <ID>`, the ebook type's default Section Inventory (prerequisites, part progression, Show-Tell-Apply chapter sequence, appendices, glossary) applies.
- Ebook quality rules (`EBK-ST-01..05`, `EBK-EV-01..02`, `EBK-ED-01..02`, `EBK-RC-01`) remain strictly binding.
- Technique rules never waive house style or privacy rules.

## 3. Type-Owned Decisions and Multi-Prompt Execution

Ebooks are large-scale projects requiring dedicated execution patterns, multi-prompt compilation, and running memory.

### Execution Tier Default and Escalation (Tier 3 Fixed)

- **Tier 3 Fixed**: By construction (`DRSYNART-FR-02`, `DRSYNART-NFR-03`), `/write-ebook` always runs at tier 3. Producing a book-length manuscript requires a STRUT and compiled prompt sequences executing chapter by chapter.
- **Splitting into Parts Above NFR-01**: A single tier-3 call is capped at 8 prompt files, 35 prompts total, and 12 deliverables (`DRSYNART-NFR-01`). Ebooks that exceed these limits must be split into separate parts (e.g., Part 1 call, Part 2 call) that share the same master `[ID]-DRAFT-NN_[Title].md` file.

### Audience Adaptation (`for <audience>`)

The optional parameter `for <audience>` adapts technical register, scenario context, and exercise tools:
- `for engineering leads / architects`: emphasizes cluster topology trade-offs, operational budgets, failure cascades, and governance.
- `for practitioners / devops engineers`: emphasizes exact configuration parameters, command-line steps, failure reproduction, and telemetry hooks.
- `for enterprise operators / compliance officers`: emphasizes auditability, disaster recovery certifications, and data durability guarantees.
- **Rule Reference**: `EBK-CT-03`.

### Option Proposals and Scoring (`/propose-ebook`)

When invoked via `/propose-ebook`, the workflow produces `[ID]-OPTIONS-NN_[Title].md`:
- Brief first: before generating options, write the `## Brief` section (Mandate, Purpose, Audience, Reader outcome, Governing question, In scope, Out of scope, Constraints, Success criteria). Quote the user's request verbatim as Mandate; mark every value you derive instead of taking from the user with `[ASSUMED]`. Without a Brief, nobody can check Goal Alignment or Reader Transformation Path.
- Default candidate count: exactly 3 options.
- Outline: parts as group headings; every chapter on its own numbered line with five fields: `Goal` (cites the Reader outcome item it serves), `Content`, `Evidence` (finding IDs or `[ASSUMED]`), `Reason`, `Handoff`. A chapter whose Goal serves no Reader outcome item is a cut or appendix candidate; a missing Handoff signals a gap in the reader's path.
- Standard scoring weights: Goal Alignment (30%), Supportability (30%), Reader Transformation Path (25%), Scope Feasibility (15%). Goal Alignment is scored against the Brief `Governing question`, `Purpose`, and `Reader outcome`; Reader Transformation Path against the step from the Brief `Audience` baseline to the Brief `Reader outcome`; Scope Feasibility against the Brief `Constraints`. For ebooks, Reader Transformation Path and Scope Feasibility replace Impact and Specificity because long-form pedagogical success depends on whether the cumulative chapter arc actually bridges the capability gap within realistic reader and author constraints, rather than single-article rhetorical force.
- Concludes with one recommended option and selection rationale; the `Why` line names the Brief field behind the Goal Alignment and Reader Transformation Path scores.
- `/draft-ebook` copies the Brief and keeps the chosen outline's chapters and field names, adding detail (fill-in instructions in `Content`, diagram placeholders, claim-level Evidence Placement). `/write-ebook` never copies the Brief into the output or chapter files.
- **Rule Reference**: `EBK-CT-04`, `EBK-CT-05`.

### Sample Chapter Bake-Off (`compare techniques` per DRSYNART-DD-39)

When the user calls `/propose-ebook` with `compare techniques <ID>, <ID>[, <ID>]` (2-4 technique IDs, e.g., `compare techniques STA, DIATAXIS, MINTO`):
- The workflow writes one candidate outline per technique ID.
- It authors one complete sample chapter per candidate directly into the OPTIONS file.
- Sample length cap: at tier 1, sample chapters in the bake-off are capped at 500 words each to protect the single-turn budget; when full-length sample chapters are requested, escalate to tier 2.
- It scores each sample chapter against:
  1. This GUIDE's quality heuristics (advance organizer, repeating pattern, tool independence).
  2. The style-pattern signals (`AI_WRITING_RULES.md`).
  3. CHECKS files are NEVER loaded during bake-off scoring (`DRSYNART-FR-32`).
- Results are recorded under each option's `Sample:` field.

### Chapter File Conventions

Individual chapter files produced during drafting reside in `_agentwork/`:
- Naming format: `_agentwork/ch-NN_[Chapter].md` (e.g., `_agentwork/ch-01_MeasurePartitionBaseline.md`).
- Each chapter prompt authors 1-2 chapters using the `guarded` prompt profile (`DRSYNART-NFR-01`).

### Checkpoint Prompts and Separate Verification

- Every chapter prompt is immediately followed by a separate checkpoint prompt executed by a fresh prompt invocation (`DRSYNART-NFR-05`).
- The checkpoint prompt runs `/verify` against the targeted `EBK-` rules and applies `/fix` if issues arise. Verification never runs inside the authoring prompt.

### Style Sheet as Series Bible in DRAFT

The DRAFT file (`[ID]-DRAFT-NN_[Title].md`) contains a permanent "Style Sheet" section:
- Serves as the series bible across all prompts.
- Records terminology decisions, capitalization standards, numerical conventions, and cross-reference formats.
- Updated whenever a recurring convention is established; never overridden by local chapter preferences.
- **Rule Reference**: `EBK-ED-02`.

### Chapter Summaries as Running Memory

The DRAFT file contains a "Chapter Summaries" section:
- Every chapter prompt reads all existing chapter summaries before drafting.
- After authoring its assigned chapter(s), the prompt appends a concise 3-5 sentence summary for each new chapter:
  1. What capabilities and facts were established.
  2. What terms and concepts were introduced.
  3. What open threads or forward promises were made.
- This running memory prevents chapter drift, duplicate explanations, and contradictions across long prompt sequences.
- **Rule Reference**: `EBK-ED-02`.

### Multi-Pass Stitching, Consistency, and Assembly Sequence (SPEC 8.3)

At tier 3, book execution follows a compiled prompt sequence:
1. Master outline and Style Sheet initialized in `[ID]-DRAFT-NN_[Title].md`.
2. Chapter prompts author 1-2 chapters into `_agentwork/ch-NN_[Chapter].md` and append Chapter Summaries.
3. Checkpoint prompts verify each chapter batch against structural and pedagogical rules.
4. Copyediting pass regularizes terms, numbers, and cross-references against the Style Sheet.
5. Book consistency prompt checks transitions, through-lines, and cross-references across all chapter files.
6. Stitching prompt concatenates the final manuscript in proper order: Front Matter, Parts, Chapters, Back Matter.
7. Independent fact-check prompt verifies claims and numbers against sources.
8. Release check prompt validates final publication criteria.
9. Full VCRIV (Verify, Critique, Reconcile, Implement, Verify) gate verifies final manuscript integrity before publication.

Model selection adheres to `MODEL_INVENTORY.md`: compilation and stitching prompts require the 1M-context class, while chapter authoring prompts run on the headless default model using the guarded prompt profile (at most 4 numbered items, at most 2 content files changed per prompt).


### Output Naming Conventions

All ebook artifacts follow `DRSYNART-FR-24`:
- Options file: `[ID]-OPTIONS-NN_[Title].md`
- Draft file: `[ID]-DRAFT-NN_[Title].md`
- Final book manuscript: `YYYY-MM-DD_[Title].md`
- Deliverables reside in the active working folder, never in `_agentwork/`.

## 4. Editorial Quality and Consistency Standards

### Edit Levels Applied to Ebooks

Ebooks require all four standard editorial passes plus independent fact-checking:
1. Developmental edit: verified through the initial outline, transformation path, and chapter sequence.
2. Line edit: clarity, flow, active verbs, and Paramedic Method lard reduction.
3. Copyedit: regularizing terms, numbers, capitalization, and formatting against the Style Sheet.
4. Fact-check: independent verification of every metric, source citation, and code sample.
5. Proofread: final layout check, link verification, and front/back matter apparatus inspection.

### Clarity Principles (Line Edit)

1. **Lanham's Paramedic Method**: Eliminate nominalizations, circle prepositions, replace passive constructions with active verbs, and reduce the lard factor below one-third.
2. **Williams's Characters and Actions**: Make technical actors (brokers, clients, operators) the grammatical subjects and actions the verbs. Keep familiar concepts at sentence openings and push new technical terms to sentence endings.
3. **Pinker's Classic Style**: Treat the text as a window through which reader and author gaze together at the reality of the system.
4. **Anti-AI Prose Discipline (`AI_WRITING_RULES.md`)**: Sustain continuous, natural prose flow. Avoid staccato fragments, contrast snaps, telegraphic objection blocks, mechanical tricolons, signpost openers, reflex header/list inflation, prestige-register buzzwords, and nominalization chains that produce punchy, flow-breaking robotic writing. Calibrate sentence rhythm, punctuation variety, and paragraph length to the active persona.
- **Rule Reference**: `EBK-ED-01`, `AW-SO-01` through `AW-LX-03`.

### Fact-Checking Standard

Ebooks carry practitioner operational liability and require strict fact-checking (Borel):
- Every metric, benchmark, version number, and command must be cross-referenced to an authoritative source or marked `[ASSUMED]`.
- Fact-checking must be performed by a prompt that did not author the chapter text.
- **Rule Reference**: `EBK-EV-03`.

### Chapter Recap Convention

Every chapter concludes with a concise recap section formatted as a capability statement, not a content summary:
- Form: "You can now [state capability]. In the next chapter, you will [state next transformation step]."
- Never restate topics or bullet points already covered in the chapter body.
- **Rule Reference**: `EBK-ED-03`.

### Release Check Standards

Before publication, every ebook manuscript must satisfy the seven release check criteria (`DRSYNART-SPEC-8.5`):
1. Header fields complete: `Doc ID: [TOPIC]-EBOOK-[NN]`, `Document Type: ebook`, `Technique`, `Persona`, `Audience`, `Source`.
2. Sourcing: every factual metric, benchmark, and empirical claim cited or marked `[ASSUMED]`.
3. Numbering and cross-references: continuous chapter and exhibit numbering; all internal cross-references resolve.
4. Presentation hygiene: zero prompt fragments, scratchpads, or temporary generation artifacts in the final text.
5. AI-writing detection: style-pattern signals below threshold (`<= 1` signal across `AW-SO`, `AW-SY`, `AW-ST`, `AW-VO`, `AW-LX` in `AI_WRITING_RULES.md`; excluding structural signals inherent to the chosen technique).
6. Persona trait budget and length/pacing profile respected (when a persona is specified).
7. Word count and chapter counts within target range.
- **Rule Reference**: `EBK-RC-01`.

## 5. Named Failure Modes and Strategic Mitigations

1. **Promise as a Topic Instead of a Testable Outcome**: The book states what it is about ("A Guide to Microservices") rather than what the reader will be able to do.
   - *Strategic mitigation*: Formulate a single declarative sentence stating an observable capability answerable with yes/no. See `EBK-CT-01`.
2. **Chapter Sequence Mirroring Author's Knowledge Map**: Chapters trace the author's academic taxonomy (history, concepts, variants) instead of the reader's operational journey.
   - *Strategic mitigation*: Derive the table of contents from the sequence of steps a practitioner takes from zero to the promised capability. See `EBK-CT-02`.
3. **Table of Contents of Nouns**: Headings use passive noun phrases ("Configurations", "Architectures") rather than action-oriented claims.
   - *Strategic mitigation*: Rewrite every chapter title as an imperative action title. See `EBK-ST-03`.
4. **Introduction That Summarizes the Whole Book**: The introduction gives away every chapter's contents in detail, eliminating narrative motivation.
   - *Strategic mitigation*: Restructure the introduction as an executive contract (promise, audience boundaries, prerequisites) or forgo front matter entirely. See `EBK-ST-02`.
5. **Chapter Without a Recap**: A chapter ends abruptly after the last application step without reflecting on the acquired skill or bridging forward.
   - *Strategic mitigation*: Add a standardized recap section stating the new capability and introducing the next step. See `EBK-ED-03`.
6. **Recaps That Repeat Verbatim**: The recap restates bullet points from the chapter opening or body text.
   - *Strategic mitigation*: Enforce the capability recap formula: state what the reader can now do, not what the chapter discussed. See `EBK-ED-03`.
7. **Examples Requiring Author's Proprietary Tools**: Practical exercises depend on custom scripts or internal tooling unavailable to general readers.
   - *Strategic mitigation*: Rewrite exercises using standard command-line tools, vendor-neutral configurations, or generic templates. See `EBK-EV-01`.
8. **No Cross-References for Non-Linear Readers**: Chapters assume cover-to-cover reading and fail to link interrelated concepts.
   - *Strategic mitigation*: Apply inline indexing with explicit chapter numbers and titles whenever earlier foundations or later applications are referenced. See `EBK-EV-02`.
9. **Chapter Drift Across Long-Form Prompt Sequences**: Later chapters introduce conflicting conventions, forget earlier promises, or repeat explanations.
   - *Strategic mitigation*: Enforce reading and updating the DRAFT Chapter Summaries running memory at every prompt. See `EBK-ED-02`.
10. **Inconsistent Terminology and Concepts Across Chapters**: Terms, acronyms, and casing change across chapter boundaries.
    - *Strategic mitigation*: Maintain and enforce the Style Sheet series bible in the DRAFT file throughout all writing and copyediting passes. See `EBK-ED-02`.

## 6. Quality Heuristics (Observable Properties)

Test these observable properties on the finished ebook manuscript:
- **Promise Test**: Can a reader state what they will be able to do after reading in one sentence, and can a beta reader answer whether the book delivered it with yes/no? (Yes / No)
- **Path Step Test**: Does every chapter represent an indispensable step on the reader's transformation path toward the promise? (Yes / No)
- **Skip Test**: Can a reader open Chapter 4 directly and execute its steps using explicit inline cross-references without getting stuck? (Yes / No)
- **Argument TOC Test**: Does reading the table of contents alone outline a coherent, actionable transformation argument? (Yes / No)
- **Contract Test**: Does the introduction establish audience boundaries and delivery commitments without providing a boring chapter-by-chapter plot summary? (Yes / No)
- **Tool Independence Test**: Can all exercises and quick checks be performed using generic tools without proprietary author software? (Yes / No)
- **Recap Capability Test**: Does every chapter recap assert a concrete newly gained capability rather than repeating body text? (Yes / No)
- **Inline Indexing Test**: Are all cross-references explicitly formatted with chapter numbers and titles rather than vague callbacks? (Yes / No)
- **Running Memory Test**: Do all chapter prompts reflect the cumulative context documented in the DRAFT Chapter Summaries? (Yes / No)
- **Style Sheet Consistency Test**: Are all technical terms, units, and casing standardized against the DRAFT Style Sheet across every chapter? (Yes / No)

## 7. Self-Review Questions

Review the ebook manuscript against these numbered questions before release:
1. Does the header block contain all six required fields matching FR-24? (`EBK-ST-01`)
2. Does the introduction function as a binding contract rather than a chapter-by-chapter plot summary? (`EBK-ST-02`)
3. Does every chapter heading in the table of contents state an action title that advances the argument? (`EBK-ST-03`)
4. Does every chapter follow the stated repeating pattern with a concrete opening problem or advance organizer? (`EBK-ST-04`)
5. Does a book exceeding 10 chapters organize into standalone parts with part openers and progress maps? (`EBK-ST-05`)
6. Is the book-level promise a single testable sentence paired with an explicit negative audience boundary? (`EBK-CT-01`)
7. Does the chapter sequence trace the reader's transformation path rather than the author's topic map? (`EBK-CT-02`)
8. Does the technical depth and register match the requested audience specification? (`EBK-CT-03`)
9. Did the options proposal provide three scored candidates and evaluate sample chapters during bake-off without loading CHECKS? (`EBK-CT-04`)
10. Can all chapter exercises and quick checks be performed using generic tools without proprietary software? (`EBK-EV-01`)
11. Are cross-references formatted with explicit chapter numbers and titles for non-linear lookup? (`EBK-EV-02`)
12. Is every factual claim, benchmark, and empirical metric cited or marked `[ASSUMED]`? (`EBK-EV-03`)
13. Did the line edit eliminate nominalizations and reduce the Paramedic Method lard factor below one-third? (`EBK-ED-01`)
14. Were terminology, numbers, and formatting decisions maintained across all chapters via the Style Sheet series bible and Chapter Summaries? (`EBK-ED-02`)
15. Does every chapter close with a capability recap linking forward, and did the stitching prompt assemble parts in proper sequence? (`EBK-ED-03`)
16. Does the complete manuscript pass all seven criteria of the release check? (`EBK-RC-01`)

## 8. Annotated Exemplar Links

Study these mentor exemplars for concrete demonstrations of practitioner book craft:

- [STA Ebook Chapter and Guide](../writing_techniques/EXAMPLES/STA_EXAMPLE_01-EbookChapterAndGuide.md)
  - *What makes this work*: Exemplifies practitioner ebook chapter architecture using the Show-Tell-Apply technique. Opens with a concrete four-sentence failure scenario containing specific metrics (SHOW), states the governing rule in one clear sentence (TELL), provides six tool-independent numbered steps (APPLY), includes an immediate quick check, and closes by reconnecting to the opening case.
- [DIATAXIS User Manual and How-To](../writing_techniques/EXAMPLES/DIATAXIS_EXAMPLE_01-UserManualAndHowTo.md)
  - *What makes this work*: Demonstrates structured non-linear documentation craft. Separates step-by-step goal-oriented how-to guides from conceptual explanations and reference specifications, providing distinct navigation cues and explicit prerequisites for technical practitioners.

## 9. RULES References

The following rule ID ranges in `EBOOK_RULES.md` define the enforceable output standards for all ebooks:
- `EBK-ST-01` through `EBK-ST-05`: Ebook structure, header completeness, introduction contract, action-title table of contents, repeating chapter patterns, and part organization.
- `EBK-CT-01` through `EBK-CT-04`: One-sentence promise, reader transformation sequence, audience adaptation, and options proposal scoring / bake-off.
- `EBK-EV-01` through `EBK-EV-03`: Tool-independent exercises, inline indexing cross-references, and factual claim verification.
- `EBK-ED-01` through `EBK-ED-03`: Line clarity with Paramedic Method lard factor, Style Sheet series bible with Chapter Summaries running memory, and recap convention with stitching assembly.
- `EBK-RC-01`: Final release check verification standards.
- `AW-SO-01` through `AW-LX-03` (`../AI_WRITING_RULES.md`): Anti-AI writing artifact suppression and detection across Sourcing, Style, Structure, Voice, and Lexical choice.
