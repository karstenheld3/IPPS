# Ebook Rules

Output standards for practitioner ebooks, handbooks, and long-form guides written with `/write-ebook` or planned with `/propose-ebook` and `/draft-ebook`.

**Writing quality:** Apply `APAPALAN_RULES.md`, `MECT_WRITING_RULES.md`, and `AI_WRITING_RULES.md`. Key rules: APAPL-PR-07 (be specific), APAPL-PR-05 (referenceable IDs), MECT-VO-01 (active voice), MECT-WC-02 (plain language), AW-SY-01 (no antithetical snaps), AW-ST-01 (integrated counter-arguments).

## Rule Index

Structure (ST)
- EBK-ST-01 [TYPE-OWNED]: Header block completeness and format
- EBK-ST-02 [STRUCTURE-DEFAULT]: Introduction contract and book promise
- EBK-ST-03 [STRUCTURE-DEFAULT]: Table of contents as an argument with action titles
- EBK-ST-04 [STRUCTURE-DEFAULT]: Chapter repeating pattern and opening discipline
- EBK-ST-05 [STRUCTURE-DEFAULT]: Part structure, part openers, and book-level progress navigation

Content (CT)
- EBK-CT-01 [TYPE-OWNED]: One-sentence promise and negative reader boundary
- EBK-CT-02 [TYPE-OWNED]: Reader's path chapter sequencing
- EBK-CT-03 [TYPE-OWNED]: Audience adaptation and practitioner register
- EBK-CT-04 [TYPE-OWNED]: Options proposal format and sample bake-off scoring criteria
- EBK-CT-05 [TYPE-OWNED]: Brief recorded in OPTIONS and DRAFT

Evidence & Pedagogy (EV)
- EBK-EV-01 [TYPE-OWNED]: Self-contained exercises and tool independence
- EBK-EV-02 [TYPE-OWNED]: Cross-reference discipline and inline indexing
- EBK-EV-03 [TYPE-OWNED]: Traceable claim attribution and factual verification

Editorial & Release Check (ED / RC)
- EBK-ED-01 [TYPE-OWNED]: Line clarity, active verbs, and Paramedic Method lard factor
- EBK-ED-02 [TYPE-OWNED]: Style Sheet series bible and running Chapter Summaries memory
- EBK-ED-03 [TYPE-OWNED]: Chapter recap convention, stitching order, and book assembly
- EBK-RC-01 [TYPE-OWNED]: Final release check verification standards

## EBK-ST-01 [TYPE-OWNED]: Header Block Completeness and Format

Output files must begin with a complete six-field header block matching `DRSYNART-FR-24`. Deliverable file names follow `DRSYNART-DD-16`: `[ID]-OPTIONS-NN_[Title].md`, `[ID]-DRAFT-NN_[Title].md`, and `YYYY-MM-DD_[Title].md`.

**BAD:**
```markdown
# Queue Reliability Engineering Manual

**Author**: Site Reliability Engineering Guild
**Version**: Draft 1.4
```

**GOOD:**
```markdown
# Queue Reliability Engineering Manual

**Doc ID**: QUEUEREL-EBOOK-01
**Document Type**: ebook
**Technique**: STA
**Persona**: BOOK-AUTHOR
**Audience**: production infrastructure engineers
**Source**: QUEUEREL-DRAFT-01_QueueReliabilityManual.md
```

**Verification method**: `/verify` inspects lines 1-15 for the six exact bold keys (`Doc ID`, `Document Type: ebook`, `Technique`, `Persona`, `Audience`, `Source`) and verifies the Doc ID pattern `[TOPIC]-EBOOK-[NN]`.

## EBK-ST-02 [STRUCTURE-DEFAULT]: Introduction Contract and Book Promise

The introduction must function as a mutual executive contract: defining the one-sentence promise, specifying who the book is for and who it is not for, detailing prerequisites, and laying out the transformation journey. Summarizing every chapter in a plot-like overview is prohibited. In tactical practitioner handbooks where rapid engagement is prioritized, front matter may be forgone entirely to begin immediately with Chapter 1.

**BAD:**
```markdown
## Introduction

Welcome to this handbook. In Chapter 1, we cover queue basics. In Chapter 2, we discuss message offsets. In Chapter 3, we look at consumer lag. In Chapter 4, we examine partitioning. In Chapter 5, we present monitoring scripts. In Chapter 6, we provide conclusions.
```

**GOOD:**
```markdown
## Introduction: The Production Contract

This handbook is for infrastructure engineers who operate Linux production clusters but have never tuned distributed commit logs. It is not for consensus engine developers, and it is not for readers without container networking experience.

By the end of this handbook, you will configure and operate a message queue cluster handling 100k events per second with zero data loss across network partitions. You will need a workstation capable of running two container nodes and standard network diagnostic utilities.
```

**Verification method**: `/verify` inspects the introduction to ensure it states the promise and audience boundaries without providing a chapter-by-chapter summary list.

## EBK-ST-03 [STRUCTURE-DEFAULT]: Table of Contents as an Argument with Action Titles

Every chapter entry in the table of contents must be an imperative action title asserting an operational step. Scanning the table of contents alone must demonstrate the complete transformation argument from initial failure to final resilience. Topical noun lists are prohibited.

**BAD:**
```markdown
# Contents

1. Introduction
2. Topologies
3. Replicas
4. Partitions
5. Metrics
```

**GOOD:**
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
```

**Verification method**: `/verify` checks that every chapter entry in the table of contents starts with an active verb and conveys an operational task rather than a passive noun phrase.

## EBK-ST-04 [STRUCTURE-DEFAULT]: Chapter Repeating Pattern and Opening Discipline

Every chapter must follow the declared repeating pedagogical pattern (Show-Tell-Apply, textbook, Minto, or Diataxis). The opening section must present either a concrete recognized problem with quantified details or an Ausubel advance organizer. Opening with a topical summary of upcoming sections is prohibited.

**BAD:**
```markdown
# Chapter 4: Synchronous Replicas

In this chapter, we will explain synchronous replicas, quorum counts, and persistence flags. First we discuss quorum, then we discuss flags, and then we discuss failures.
```

**GOOD:**
```markdown
# Chapter 4: Configure Synchronous Replicas to Eliminate Phantom Writes

## The replica that acknowledged unwritten records

Composite incident from payment clearing clusters: at 14:22, broker node 2 crashed while processing a batch of 840 transaction records. Because replication was configured as asynchronous with `ack=1`, the producer received confirmation before replica storage persisted the batch, resulting in 840 lost records during failover.

## An acknowledgment requires multi-node commit confirmation

A write is not committed when one memory buffer stores it; a write is committed when a quorum of independent replicas confirms persistence to disk.
```

**Verification method**: `/verify` verifies that the chapter opening presents a concrete failure scenario or advance organizer and follows the declared pattern without topical previews.

## EBK-ST-05 [STRUCTURE-DEFAULT]: Part Structure, Part Openers, and Book-Level Progress Navigation

When an ebook contains more than 10 chapters or spans distinct operational stages, it must be organized into standalone parts. Each part must begin with an orientation opener describing the phase and a visual "you are here" progress map showing completed, active, and upcoming phases.

**BAD:**
```markdown
# Part II

[Chapter 6 begins immediately without part orientation or roadmap...]
```

**GOOD:**
```markdown
# Part II: Enforce Ingestion Invariants

You have measured your baseline network latency and mapped partition boundary cut points in Part I. Part II implements cluster-level invariants that keep brokers stable under load.

Progress map:
- [x] Part I: Measure the Failure Horizon (Chapters 1-2)
- [>] Part II: Enforce Ingestion Invariants (Chapters 3-5) [Active]
- [ ] Part III: Automate Production Recovery (Chapters 6-8)
```

**Verification method**: `/verify` checks that manuscripts exceeding 10 chapters contain part division openers equipped with phase orientations and progress roadmaps.

## EBK-CT-01 [TYPE-OWNED]: One-Sentence Promise and Negative Reader Boundary

The ebook must define a single testable sentence stating what the reader will be able to do after reading, paired with an explicit negative audience boundary stating who the book is not for. Every chapter must advance the reader toward delivering that promise, and the final chapter must confirm its fulfillment.

**BAD:**
```markdown
This book covers distributed queuing and reliability practices for all technical readers.
```

**GOOD:**
```markdown
- **Book promise**: After reading this handbook, you will design and operate a message queue cluster handling 100k events per second with zero message loss during regional network partitions.
- **Negative reader boundary**: Not for consensus engine developers building custom Raft protocols from scratch; not for engineers without basic Linux networking and container experience.
```

**Verification method**: `/verify` checks that the promise is formulated as a single testable outcome sentence and that negative boundaries are explicitly defined.

## EBK-CT-02 [TYPE-OWNED]: Reader's Path Chapter Sequencing

The chapter sequence must trace the reader's operational journey from their current problem state to the promised capability. Structuring chapters according to the author's internal knowledge taxonomy or textbook theory is prohibited.

**BAD:**
```markdown
Chapter sequence:
1. History of message brokers (1980 to present)
2. Academic taxonomy of consensus models
3. Binary wire protocol specification
4. Production failover configuration
```

**GOOD:**
```markdown
Chapter sequence:
1. Measure partition baseline latency before configuring replication
2. Identify network boundary cut points in multi-zone clusters
3. Enforce client backpressure under network stalls
4. Configure synchronous replicas to eliminate phantom writes
5. Automate regional broker cutover without split-brain risk
```

**Verification method**: `/verify` verifies that each chapter represents an observable step on the reader's transformation path toward the promise.

## EBK-CT-03 [TYPE-OWNED]: Audience Adaptation and Practitioner Register

The technical density, command-line examples, diagnostic scenarios, and exercise depth must match the audience parameter (`for <audience>`). An advanced practitioner guide must not waste space explaining basic Linux commands; an architectural overview must focus on topology trade-offs and operational budgets.

**BAD:**
```markdown
<!-- Written for senior site reliability engineers: -->
To list the files in your directory, type `ls -la` in your terminal window and press Enter.
```

**GOOD:**
```markdown
<!-- Written for senior site reliability engineers: -->
Inspect the broker socket buffer watermark using `ss -t -i 'sport = :9092'` to confirm client TCP receive windows are not stalling.
```

**Verification method**: `/verify` inspects technical vocabulary, command examples, and conceptual explanations against the declared audience in the header block.

## EBK-CT-04 [TYPE-OWNED]: Options Proposal Format and Sample Bake-Off Scoring Criteria

When generated by `/propose-ebook`, options proposals must contain a Brief (EBK-CT-05) and present candidate outlines scored against Goal Alignment (30%), Supportability (30%), Reader Transformation Path (25%), and Scope Feasibility (15%). When `compare techniques` is passed, each candidate must provide a complete sample chapter scored against quality heuristics and style-pattern thresholds without loading CHECKS files.

Outline format: parts as group headings; every chapter on its own numbered line (`Ch N: [Action Title]`), with five fields below it:
- `Goal`: the milestone the chapter delivers on the reader's path; cites the Brief `Reader outcome` item it serves
- `Content`: the problem scenario, principle, steps, and quick check the chapter presents
- `Evidence`: source finding IDs or key facts; `[ASSUMED]` where no source supports the chapter
- `Reason`: why the chapter sits at this position and takes this form
- `Handoff`: the question, consequence, or capability gap that leads into the next chapter; for the last chapter, the capability the reader leaves with

Field labels are plain text (`- Goal: ...`), never bold. Bold is reserved for the part group line and the numbered chapter line. The same applies to every field under the `### Part` and `#### Chapter` headings of the DRAFT `## Structure` section, including `Phase objective`, `Part opener orientation`, and `Diagram placeholder`.

Scoring: Goal Alignment is scored against the Brief `Purpose`, `Governing question`, and `Reader outcome`; Reader Transformation Path against the step from the Brief `Audience` baseline (knows) to the Brief `Reader outcome` (do). The Recommendation `Why` names the Brief field behind each of these two scores.

**BAD:**
```markdown
## Option 1: Chaos-First Failover Path
- **Promise**: Deploy resilient multi-zone queue clusters with verified zero message loss under partition
- **Outline**: [Part I: Baseline] -> [Part II: Invariants] -> [Part III: Recovery]
- **Score**: goal_alignment=5, supportability=4, reader_transformation_path=5, scope_feasibility=4 (composite: 4.55)
```

**GOOD:**
```markdown
## Option 1: Chaos-First Failover Path
- **Promise**: Deploy resilient multi-zone queue clusters with verified zero message loss under partition
- **Reader boundary**: Platform engineers running queue clusters in production; not for first-time queue users
- **Outline**:
  - **Part I: Measure the Baseline Before Changing Anything**
    1. **Ch 1: Reproduce Message Loss Under a Zone Partition**
       - Goal: Reader can reproduce loss on demand [Reader outcome: do]
       - Content: Partition scenario, loss measurement, benchmark steps, quick check
       - Evidence: QUEUEOPS-IN01 F-02, F-05
       - Reason: Readers trust later fixes only after seeing the failure themselves
       - Handoff: Loss appears at zone boundaries -> map the cut points
    2. **Ch 2: Map Zone Boundaries and Network Cut Points**
       - Goal: Reader knows where partitions break delivery [Reader outcome: know]
       - Content: Topology mapping, cut-point inventory, isolation test
       - Evidence: QUEUEOPS-IN01 F-07
       - Reason: Invariants in Part II need a known failure surface
       - Handoff: Known cut points -> which guarantees must hold across them?
  - **Part II: Enforce Delivery Invariants**
    3. **Ch 3: Apply Backpressure Before Memory Runs Out**
       - Goal: Reader configures backpressure under stalls [Reader outcome: do]
       - Content: Queue depth thresholds, client retry policy, stall drill
       - Evidence: QUEUEOPS-IN01 F-11; retry ceiling [ASSUMED]
       - Reason: Backpressure prevents the overload that hides replication faults
       - Handoff: Stable load -> eliminate unacknowledged writes
    <!-- Ch 4-6 (Part II and Part III) follow with the same five fields -->
- **Score**: goal_alignment=5, supportability=4, reader_transformation_path=5, scope_feasibility=4 (composite: 4.55)

## Recommendation
- **Option**: 1
- **Why**: Goal alignment: answers the Brief Governing question "How do we stop losing messages during zone partitions?" chapter by chapter; supportability: every chapter traces to findings, one value is marked [ASSUMED]; reader transformation path: moves the Brief Audience baseline "knows: single-zone operation" to the Brief Reader outcome "do: certify zero loss under chaos tests"; scope feasibility: six chapters fit the Brief length constraint.
```

**Verification method**: `/verify` checks that `[ID]-OPTIONS-NN_` files contain a Brief, candidate options with composite score breakdowns, outline chapters each carrying the five fields `Goal`, `Content`, `Evidence`, `Reason`, `Handoff` with plain (not bold) labels, a recommendation whose Goal Alignment and Reader Transformation Path sentences name a Brief field, and sample chapter evaluations under `compare techniques`.

## EBK-CT-05 [TYPE-OWNED]: Brief Recorded in OPTIONS and DRAFT

Every OPTIONS and DRAFT file must contain a `## Brief` section after the header block, so that a reader or agent can judge options and drafts against the ebook's goal. Fields: `Mandate` (user request, verbatim), `Purpose`, `Audience` (who, prior knowledge, need), `Reader outcome` (know, believe, do), `Governing question`, `In scope`, `Out of scope`, `Constraints` (length, channel, tone), `Success criteria`. Values the agent derived instead of taking from the user carry `[ASSUMED]`. `/draft-ebook` copies the Brief from the OPTIONS file (or writes it when no OPTIONS file exists) and records every change in `Brief changes`. `/write-ebook` never copies the Brief into the output document or chapter files.

**BAD:**
```markdown
**Source**: _INFO_QUEUEOPS-IN01_Analysis.md
**Scoring criteria**: Goal Alignment (30%), Supportability (30%), Reader Transformation Path (25%), Scope Feasibility (15%)

## Option 1: Chaos-First Failover Path
```

**GOOD:**
```markdown
## Brief
- **Mandate**: "Write a practitioner ebook on running queue clusters across zones without message loss"
- **Purpose**: Give platform teams one reference for multi-zone queue operation [ASSUMED]
- **Audience**: Platform engineers; knows: single-zone operation; needs: a tested path to multi-zone durability
- **Reader outcome**: know: where partitions break delivery; believe: invariants beat tuning; do: certify zero loss under chaos tests
- **Governing question**: How do we stop losing messages during zone partitions?
- **In scope**: Partitions, backpressure, replication, failover, chaos testing
- **Out of scope**: Vendor comparison, cost optimization
- **Constraints**: length: 6-8 chapters; channel: internal engineering handbook; tone: practitioner, direct
- **Success criteria**: Reader completes the Chapter 6 chaos drill with zero lost messages
```

**Verification method**: `/verify` checks that OPTIONS and DRAFT files contain a `## Brief` section with all nine fields, that DRAFT files contain `Brief changes`, and that the output document contains no Brief section.

## EBK-EV-01 [TYPE-OWNED]: Self-Contained Exercises and Tool Independence

All application steps, diagnostic worksheets, and quick checks must be doable using standard open-source utilities or generic environments without author-specific proprietary tools or private infrastructure.

**BAD:**
```markdown
1. Open the proprietary CloudMonitor enterprise portal.
2. Select AuthorCustomPlugin from the internal extensions tab.
3. Run the author's internal script `verify_all.sh`.
```

**GOOD:**
```markdown
1. Run `tcpdump -i eth0 -nn 'port 9092 and (tcp[tcpflags] & tcp-syn != 0)'` on the secondary broker node.
2. Trigger the regional network filter using `iptables -A INPUT -p tcp --dport 9092 -j DROP`.
3. Check producer client logs to verify exponential backoff with jitter triggers within 200 ms.
```

**Verification method**: `/verify` scans application steps and quick checks to ensure all referenced tools and commands are vendor-neutral and self-contained.

## EBK-EV-02 [TYPE-OWNED]: Cross-Reference Discipline and Inline Indexing

Internal cross-references across chapters must cite explicit chapter numbers and action titles ("inline indexing"). Vague callbacks such as "as discussed earlier" or "see next chapter" without explicit identifiers are prohibited.

**BAD:**
```markdown
As we saw in the previous chapter, buffer overflows occur easily. Later in the book we will fix this.
```

**GOOD:**
```markdown
As demonstrated in Chapter 3: Enforce Client Backpressure Under Network Stalls, buffer overflows exhaust heap memory within seconds. The replication protocol implemented in Chapter 4: Configure Synchronous Replicas to Eliminate Phantom Writes prevents this data loss.
```

**Verification method**: `/verify` verifies that all internal cross-references specify exact chapter numbers and titles.

## EBK-EV-03 [TYPE-OWNED]: Traceable Claim Attribution and Factual Verification

Every empirical metric, network latency benchmark, throughput figure, and architectural limit must be cross-referenced to an authoritative research finding ID or tagged `[ASSUMED]`. Independent fact-checking must be recorded prior to manuscript release.

**BAD:**
```markdown
Modern cloud networks frequently drop packets and everybody knows clusters fail daily.
```

**GOOD:**
```markdown
Under simulated cross-region network degradation, inter-broker round-trip latency climbed from 1.8 ms to 240 ms, inducing split-brain leader elections within 4.5 seconds (Chaos Benchmark Run CB-08).
```

**Verification method**: `/verify` checks that all empirical claims, metrics, and latency numbers trace to finding IDs or carry explicit `[ASSUMED]` tags.

## EBK-ED-01 [TYPE-OWNED]: Line Clarity, Active Verbs, and Paramedic Method Lard Factor

Prose must feature technical actors (brokers, clients, operators) as grammatical subjects and operational events as active verbs. Passive nominalizations must be removed. The Paramedic Method lard factor must remain under one-third.

**BAD:**
```markdown
The execution of the configuration adjustment on the broker by the administrator is necessary for the avoidance of socket termination. (20 words)
```

**GOOD:**
```markdown
The administrator must adjust broker configuration to prevent socket termination. (10 words; lard factor = 50.0% reduction)
```

**Verification method**: `/verify` checks for passive voice constructions and calculates sentence lard factor across chapter samples.

## EBK-ED-02 [TYPE-OWNED]: Style Sheet Series Bible and Running Chapter Summaries Memory

Manuscript drafting must maintain consistency via the Style Sheet and Chapter Summaries sections of the DRAFT file. Recurring terminology, units, capitalization, and cross-reference formats must follow the Style Sheet. Every completed chapter must possess a 3-5 sentence entry in Chapter Summaries documenting established facts, introduced terms, and open threads.

**BAD:**
```markdown
<!-- Chapter 2 uses: "ack=1", "commit-log", "slave node" -->
<!-- Chapter 6 uses: "acknowledgment level 1", "WAL file", "replica broker" -->
<!-- DRAFT Chapter Summaries is empty -->
```

**GOOD:**
```markdown
<!-- DRAFT Style Sheet enforces: "ack=1", "commit log", "replica node" consistently -->
<!-- DRAFT Chapter Summaries: -->
### Chapter 3 Summary
- Established: Proactive backpressure triggers HTTP 429 when queue depth reaches 75% capacity.
- Introduced terms: queue watermark, exponential backoff with jitter, in-flight request ceiling.
- Open threads: Secondary broker synchronization under partition is resolved in Chapter 4.
```

**Verification method**: `/verify` cross-checks technical terms against the DRAFT Style Sheet and verifies that Chapter Summaries contains an entry for every drafted chapter.

## EBK-ED-03 [TYPE-OWNED]: Chapter Recap Convention, Stitching Order, and Book Assembly

Every chapter must conclude with a standardized capability recap: "You can now [state capability]. In the next chapter, you will [state next transformation step]." Recaps must state actionable capability, not summarize chapter content. The final manuscript must be assembled in proper stitching order: Front Matter, Parts, Chapters, and Back Matter.

**BAD:**
```markdown
## Summary

In this chapter we discussed queue depths, memory exhaustion, client buffers, and retry policies.
```

**GOOD:**
```markdown
## Chapter Recap

You can now configure client backpressure thresholds that keep broker memory stable during downstream outages. In the next chapter, you will configure synchronous replicas to ensure uncommitted messages are never acknowledged.
```

**Verification method**: `/verify` checks that every chapter ends with a capability recap and that the stitched output reflects the sequential assembly of front matter, parts, chapters, and back matter.

## EBK-RC-01 [TYPE-OWNED]: Final Release Check Verification Standards

Before an ebook is released, it must pass the release check (`DRSYNART-SPEC-8.5`) recorded in the DRAFT file or verification audit:
1. Header fields complete and valid (`Doc ID: [TOPIC]-EBOOK-[NN]`, `Document Type: ebook`, `Technique`, `Persona`, `Audience`, `Source`).
2. Sourcing: every empirical metric, latency figure, and command cited or marked `[ASSUMED]`.
3. Numbering and cross-references: continuous chapter and exhibit numbering; all internal cross-references resolve.
4. Presentation hygiene: zero agent prompts, scratchpads, or workflow metadata in final text.
5. Style-pattern signals below threshold: at most 1 signal detected across Sourcing, Style, Structure, Voice, and Lexical (`AI_WRITING_RULES.md`). Structural signals produced by a technique by construction (such as Show-Tell-Apply repeating blocks) are excluded.
6. Persona trait budget and length/pacing profile respected (when a persona is specified).
7. Word count and chapter counts within target envelope.

**BAD (Incomplete / Failing Record):**
```markdown
## Release Check
- Book verified
- Status: finished
```

**GOOD (Valid Release Check Record):**
```markdown
## Release Check

- **Header block**: Complete (Doc ID: QUEUEREL-EBOOK-01, Document Type: ebook, Technique: STA, Persona: BOOK-AUTHOR, Audience: production infrastructure engineers, Source: QUEUEREL-DRAFT-01_QueueReliabilityManual.md)
- **Claim attribution**: 48 empirical metrics verified against benchmark ledger; 4 forward-looking capacity models tagged [ASSUMED]
- **Structural integrity**: Chapters 1 through 8 continuously numbered across Parts I-III; all in-text cross-references resolve
- **Metadata hygiene**: Zero agent prompts, scratchpad notes, or workflow tags in body
- **Style-pattern signals**: 0 signals detected (AW-SO: 0, AW-SY: 0, AW-ST: 0, AW-VO: 0, AW-LX: 0); STA pedagogical repeating structure excluded
- **Persona compliance**: BOOK-AUTHOR register verified; zero informal slang; micro-dose trait budget and length profile respected
- **Word count**: 22,400 words across 8 chapters (target: 20,000 - 25,000 words)
- **Status**: PASSED
```

**Verification method**: `/verify` inspects the Release Check record in the DRAFT file or audit block and verifies all seven criteria.
