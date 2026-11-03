# Ebook Checks

Audits process discipline and quality improvement for ebooks written with `/write-ebook` or planned with `/propose-ebook` and `/draft-ebook`.

Evidence sources: final output document, options proposal (`[ID]-OPTIONS-NN_`), working draft (`[ID]-DRAFT-NN_`), chapter files (`_agentwork/ch-NN_*.md`), planning notes, conversation history.

## Process Discipline (PD)

### EBK-PD-01: Promise and Negative Boundary Drafted Before Outlining

- Action: Agent formulated a testable one-sentence promise and explicit negative reader boundary before drafting chapter outlines
- Evidence: Working draft or planning notes record the one-sentence promise and negative boundary prior to the table of contents
- Failure indicator: Table of contents drafted around generic topics without an explicit reader outcome or audience boundary
- References: EBK-CT-01, EBK-ST-02

### EBK-PD-02: Options Proposal Scored with Bake-Off Integration

- Action: Agent drafted candidate options scored against standard weights and executed sample chapter bake-offs when `compare techniques` was invoked
- Evidence: `[ID]-OPTIONS-NN_` records Goal Alignment (30%), Supportability (30%), Path (25%), Feasibility (15%) with one recommended candidate; every outline chapter carries `Goal`, `Content`, `Evidence`, `Reason`, `Handoff` as plain (not bold) labels; the `Why` line names the Brief field behind Goal Alignment and Path; bake-off samples scored without loading CHECKS
- Failure indicator: Options proposal missing, unscored, outline written as arrow chains, bold field labels below chapter lines, scores that cite no Brief field, or CHECKS files loaded during sample evaluation
- References: EBK-CT-04

### EBK-PD-03: Chapter Sequence Derived from Reader Path

- Action: Agent derived chapter sequence from the reader's operational journey rather than an academic taxonomy
- Evidence: Each chapter in the table of contents marks an observable milestone advancing toward the promise
- Failure indicator: Table of contents organized by the author's internal knowledge map (history, theory, taxonomy)
- References: EBK-CT-02, EBK-ST-03

### EBK-PD-04: Repeating Chapter Pattern and Opening Discipline

- Action: Agent applied the declared pedagogical pattern across all chapters with a concrete problem or advance organizer opening
- Evidence: Every chapter opens with a recognizable failure scenario or advance organizer and follows the chosen pattern consistently
- Failure indicator: Chapters open with table-of-contents previews ("In this chapter...") or structure varies arbitrarily between chapters
- References: EBK-ST-04, EBK-EV-01

### EBK-PD-05: Part Structure and Navigation Maps for Large Manuscripts

- Action: Agent organized manuscripts exceeding 10 chapters into standalone parts with part openers and progress maps
- Evidence: Part openers orient the reader to the phase and provide a visual roadmap of progress through the book
- Failure indicator: Book exceeding 10 chapters runs as an unbroken flat sequence, or parts lack orientation text
- References: EBK-ST-05

### EBK-PD-06: Style Sheet Initialized Before Chapter Prompts

- Action: Agent established the Style Sheet section in the DRAFT file before launching chapter writing prompts
- Evidence: Style sheet records standardized terminology, numbers, units, casing, and cross-reference formats used across prompts
- Failure indicator: Chapter prompts begin without a shared style sheet, resulting in conflicting terms across chapters
- References: EBK-ED-02

### EBK-PD-07: Chapter Summaries Maintained per Written Chapter

- Action: Agent appended a 3-5 sentence summary to the DRAFT file after drafting each chapter
- Evidence: DRAFT Chapter Summaries section contains cumulative entries documenting established facts, introduced terms, and open threads
- Failure indicator: Chapter Summaries section empty or missing entries for completed chapters
- References: EBK-ED-02

### EBK-PD-08: Separate Checkpoint Prompts After Every Chapter Prompt

- Action: Agent executed verification in a separate checkpoint prompt after each chapter authoring prompt
- Evidence: Execution log confirms verification ran as a dedicated prompt invocation rather than inline self-checking
- Failure indicator: Chapter prompts self-verified within the authoring turn without a separate checkpoint prompt
- References: EBK-ED-02, EBK-RC-01

### EBK-PD-09: Tool-Independent Exercises and Inline Indexing

- Action: Agent verified that all exercises use generic tools and formatted internal cross-references with explicit chapter numbers
- Evidence: Exercises require only standard utilities; cross-references cite exact chapter numbers and action titles
- Failure indicator: Exercises depend on author-specific proprietary software, or text uses vague callbacks ("as seen earlier")
- References: EBK-EV-01, EBK-EV-02

### EBK-PD-10: Sourcing and Independent Fact-Checking Execution

- Action: Agent verified every benchmark, throughput metric, and command against sources using an independent verification prompt
- Evidence: Empirical metrics trace to research finding IDs or carry explicit `[ASSUMED]` tags; fact-check recorded before release
- Failure indicator: Unverified metrics presented as facts, or fact-checking omitted
- References: EBK-EV-03

### EBK-PD-11: Book Consistency Pass Before Stitching

- Action: Agent executed a book-level consistency prompt verifying cross-references, terminology, and through-lines before assembly
- Evidence: Consistency audit confirms all chapter cross-references resolve and terms match the DRAFT Style Sheet
- Failure indicator: Chapters stitched directly into the final manuscript without a prior cross-chapter consistency pass
- References: EBK-ED-02, EBK-ED-03

### EBK-PD-12: Capability Recaps and Stitched Assembly Order

- Action: Agent concluded every chapter with a capability recap and stitched the manuscript in proper sequential order
- Evidence: Each chapter ends with "You can now [capability]..."; output follows Front Matter, Parts, Chapters, Back Matter
- Failure indicator: Recaps repeat body text verbatim, or manuscript assembled out of order
- References: EBK-ED-03

### EBK-PD-13: Release Check Documented

- Action: Agent verified the ebook against all seven release check criteria and recorded the release record
- Evidence: Release check block exists in DRAFT or verification log with complete header, AI detection status, and word count
- Failure indicator: Ebook published without an explicit release check verification record
- References: EBK-RC-01, EBK-ST-01

### EBK-PD-14: Brief Recorded Before Options

- Action: Agent wrote the Brief before generating options, carried it into the DRAFT, and kept it out of the output document and chapter files
- Evidence: OPTIONS and DRAFT files contain `## Brief` with all nine fields; Mandate quotes the user request; derived values carry `[ASSUMED]`; DRAFT records `Brief changes`
- Failure indicator: No Brief, Brief written after scoring, Mandate paraphrased, derived values unmarked, or Brief copied into the published ebook
- References: EBK-CT-05, EBK-CT-04

## Quality Improvement (QI)

### EBK-QI-01: Promise Delivery

- Question: Can a beta reader test whether the manuscript delivered its promised outcome with an unambiguous yes or no?
- Improvement tip: Review the final chapter's applied verification against the promise sentence; ensure the final test demonstrates the exact capability promised in the introduction.

### EBK-QI-02: Chapter Removal and Transformation Path

- Question: Does every chapter earn its place, or would the reader still achieve the promise if a chapter were removed?
- Improvement tip: Test each chapter against the path: if removing it does not break the chain of prerequisites, cut the chapter or merge its key principle into an adjacent chapter.

### EBK-QI-03: Skip Test and Non-Linear Usability

- Question: Can a practitioner open a middle chapter directly and execute its steps without reading preceding chapters?
- Improvement tip: Ensure each chapter states its operational prerequisites explicitly and provides inline indexing links to earlier foundational chapters for any missing context.

### EBK-QI-04: Cross-Chapter Concept and Terminology Drift

- Question: Do terms, metrics, or architectural models drift between chapters authored across separate prompt turns?
- Improvement tip: Audit recurring terms against the DRAFT Style Sheet and verify that forward promises noted in Chapter Summaries are fulfilled in subsequent chapters.

### EBK-QI-05: Exercise Practicality and Tool Independence

- Question: Can a reader execute every exercise in their own local environment without encountering hidden dependencies?
- Improvement tip: Replace any proprietary software references with standard open-source tools, vendor-neutral configurations, or generic container commands.
