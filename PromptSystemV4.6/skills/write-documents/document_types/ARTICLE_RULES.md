# Article Rules

Output standards for articles written with `/write-article` or planned with `/propose-article` and `/draft-article`.

**Writing quality:** Apply `APAPALAN_RULES.md` and `MECT_WRITING_RULES.md`. Key rules: AP-PR-07 (be specific), AP-PR-05 (referenceable IDs), MW-VO-01 (active voice), MW-WC-02 (plain language).

## Rule Index

Structure (ST)
- ART-ST-01 [TYPE-OWNED]: Header block completeness and format
- ART-ST-02 [STRUCTURE-DEFAULT]: Lead and nut graf pairing and placement
- ART-ST-03 [TYPE-OWNED]: Section goals and substantive handoffs
- ART-ST-04 [TYPE-OWNED]: Ending resolution without new arguments or repetitive summary
- ART-ST-05 [STRUCTURE-DEFAULT]: Storytelling pass for untechniqued articles

Content (CT)
- ART-CT-01 [TYPE-OWNED]: Unified theme statement governing entire text
- ART-CT-02 [TYPE-OWNED]: Four-dimension unity (mood, pronoun, tense, point of view)
- ART-CT-03 [TYPE-OWNED]: Audience adaptation and register
- ART-CT-04 [TYPE-OWNED]: Options proposal format and scoring criteria
- ART-CT-05 [TYPE-OWNED]: Brief recorded in OPTIONS and DRAFT

Evidence (EV)
- ART-EV-01 [TYPE-OWNED]: Evidence alternation across body sections
- ART-EV-02 [TYPE-OWNED]: Quote discipline, voice relevance, and attribution
- ART-EV-03 [TYPE-OWNED]: Traceable claim attribution and source verification

Editorial & Release Check (ED / RC)
- ART-ED-01 [TYPE-OWNED]: Line clarity, active verbs, and Paramedic Method lard factor
- ART-ED-02 [TYPE-OWNED]: Style sheet consistency across terminology and conventions
- ART-RC-01 [TYPE-OWNED]: Final release check verification standards

## ART-ST-01 [TYPE-OWNED]: Header Block Completeness and Format

Output files must begin with a complete six-field header block matching `DRSYNART-FR-24`. Deliverable file names follow `DRSYNART-DD-16`: `[ID]-OPTIONS-NN_[Title].md`, `[ID]-DRAFT-NN_[Title].md`, and `YYYY-MM-DD_[Title].md`.

**BAD:**
```markdown
# Enterprise Cloud Migration

**Author**: Cascade
**Date**: 2026-10-29
**Tags**: cloud, devops
```

**GOOD:**
```markdown
# Enterprise Cloud Migration

**Doc ID**: CLDMIG-ARTICLE-01
**Document Type**: article
**Technique**: ABTSTORY
**Persona**: CXO-ADVISOR
**Audience**: enterprise engineering directors
**Source**: CLDMIG-DRAFT-01_EnterpriseCloudMigration.md
```

**Verification method**: `/verify` inspects lines 1-15 for the six exact bold keys (`Doc ID`, `Document Type: article`, `Technique`, `Persona`, `Audience`, `Source`) and verifies the Doc ID pattern `[TOPIC]-ARTICLE-[NN]`.

## ART-ST-02 [STRUCTURE-DEFAULT]: Lead and Nut Graf Pairing and Placement

The article must open with an unresolved scene, metric, or tension in the first two sentences. The nut graf must appear by paragraph 5 at latest, widen the specific lead to systemic scale with at least one number, and state what the body promises to prove.

**BAD:**
```markdown
In today's fast-paced digital economy, software reliability is more critical than ever. Organizations across the globe are seeking ways to optimize their infrastructure and improve deployment efficiency.
```

**GOOD:**
```markdown
At 03:14 on a Tuesday morning, the regional distribution warehouse in Riverton went dark when an automated routing script locked its inventory database. For four hours, sixteen freight trailers sat idling at the gates while dispatchers reverted to clipboards and dry-erase markers.

The Riverton outage was not an isolated glitch: across mid-sized logistics carriers, automated warehouse scripts triggered over 1,200 dispatch halts in 2026, costing operators an estimated 42 million EUR. As freight networks consolidate software layers, the operational bottleneck has shifted from physical road capacity to brittle database locks.
```

**Verification method**: `/verify` checks that paragraphs 1-2 establish a concrete actor or operational tension and that a widening sentence with quantified baseline data appears within the first five paragraphs.

## ART-ST-03 [TYPE-OWNED]: Section Goals and Substantive Handoffs

Every body section must open with an idea-stating claim or narrative advance and conclude with a content bridge (unanswered question, consequence, or contrast). Transitions using empty connective adverbs ("Additionally", "Furthermore", "In addition") are prohibited. In OPTIONS and DRAFT files, the section's purpose is recorded in the `Goal` field and the content bridge in the `Handoff` field (ART-CT-04).

**BAD:**
```markdown
## Additional Considerations

Furthermore, cloud storage costs increased significantly last quarter. In addition, network latency was higher than expected across European regions.
```

**GOOD:**
```markdown
## Storage Costs Exploded Once Query Volume Crossed Peak Thresholds

Manual workarounds kept Riverton's trucks moving until dawn, but they created a second, quieter failure: three hundred pallets were loaded without barcode scans, leaving inventory records corrupted for three weeks.
```

**Verification method**: `/verify` checks that section headings state claims and greps for prohibited transition words (`Additionally`, `Furthermore`, `Moreover`, `In addition`) at section openings.

## ART-ST-04 [TYPE-OWNED]: Ending Resolution Without New Arguments or Repetitive Summary

The conclusion must resolve the tension raised in the lead by returning to the opening subject or detail (kicker), stating a concrete consequence, or landing on a decision threshold. It must not introduce new arguments and must not consist of bullet summaries repeating earlier sections.

**BAD:**
```markdown
## Conclusion

In summary, this article covered:
- Database locking risks
- Inventory corruption costs
- Network latency impacts

Additionally, organizations should consider adopting quantum encryption algorithms next year to prevent external cyber threats.
```

**GOOD:**
```markdown
Resolving that data debt required more than emergency patches. When Riverton's dispatchers finally turned off the legacy script in November, their chief metric was not software uptime but gate velocity: trailers cleared the yard in eight minutes, and the dry-erase markers stayed in the drawer.
```

**Verification method**: `/verify` checks the final two paragraphs for absence of bulleted summary lists and verifies that all mentioned entities were introduced earlier in the text.

## ART-ST-05 [STRUCTURE-DEFAULT]: Storytelling Pass for Untechniqued Articles

When an article is written without a technique (`Technique: none`), it must follow the default three-part narrative arc: concrete opening tension, progressive analytical body, and reflective kicker ending.

**BAD:**
```markdown
# Database Performance Analysis

- Key metric 1: Query latency is 45ms
- Key metric 2: Lock wait time is 120ms
- Recommendation: Add connection pooling
```

**GOOD:**
```markdown
# Database Locks Are Strangling Fleet Velocity

A four-millisecond query delay sounds negligible until it hits sixty simultaneous checkout queues. In Riverton, that tiny delay backed up twelve thousand transactions into a single deadlock.

## Deadlocks Compound Across Synchronous Microservices

[Analytical narrative developing root causes and metrics...]

## Velocity Returns When Queues Decouple

When engineers separated checkout writes from reporting queries, deadlock frequency dropped to zero. Fleet velocity returned not through larger database instances, but through decoupled communication paths.
```

**Verification method**: `/verify` confirms that untechniqued articles contain prose paragraphs with a three-part narrative structure rather than naked list items.

## ART-CT-01 [TYPE-OWNED]: Unified Theme Statement Governing Entire Text

Every section, paragraph, and exhibit must support one central theme statement naming a concrete tension, cause, or consequence. Topical surveys and encyclopedic drift are prohibited.

**BAD:**
```markdown
## Everything You Need to Know About Warehousing

Warehouses were invented in ancient times. Modern warehouses have tall racks, forklifts, LED lighting, heating systems, and loading docks.
```

**GOOD:**
```markdown
## Software Brittle Locks, Not Physical Fleet Capacity, Limit Warehouse Gate Speed

Modern freight hubs rarely fail from pallet shortages; they fail when monolithic software scripts lock shared database tables during shift handovers.
```

**Verification method**: `/verify` checks that all section headings and topic sentences advance the core governing claim stated in the nut graf.

## ART-CT-02 [TYPE-OWNED]: Four-Dimension Stylistic Unity

The article must maintain consistent settings across mood, pronoun, tense, and narrative distance. Arbitrary shifts (such as jumping from objective third person to conversational second person) are prohibited.

**BAD:**
```markdown
Engineers analyzed the logs and discovered severe packet drops in the primary cluster. Suddenly, you realize your entire architecture is broken and we wonder why management approved this vendor.
```

**GOOD:**
```markdown
Engineers analyzed the cluster logs and traced the packet drops to misconfigured MTU settings on the gateway routers. The team resolved the bottleneck by standardizing frame sizes across all network interfaces.
```

**Verification method**: `/verify` scans the text for pronoun switches (`I`/`you`/`we`/`they`) and tense shifts between paragraphs.

## ART-CT-03 [TYPE-OWNED]: Audience Adaptation and Register

The technical depth, introductory context, and vocabulary must match the declared `Audience:` field (`general`, `practitioner`, `executive`).

**BAD (for Audience: executive leadership):**
```markdown
To optimize B-tree index traversal in the InnoDB storage engine, configure the `innodb_buffer_pool_instances` parameter to match hardware NUMA nodes and inspect memory allocation via `jemalloc`.
```

**GOOD (for Audience: executive leadership):**
```markdown
Database configuration misalignments consume 28% of server capacity without improving throughput. Aligning database memory allocations with server architecture recovers that capacity without purchasing additional hardware.
```

**Verification method**: `/verify` cross-checks technical definitions and executive framing against the declared audience header field.

## ART-CT-04 [TYPE-OWNED]: Options Proposal Format and Scoring Criteria

An options proposal (`[ID]-OPTIONS-NN_[Title].md`) written by `/propose-article` must contain a Brief (ART-CT-05), present candidate options scored against the four standard criteria (Goal Alignment 30%, Supportability 30%, Impact 25%, Specificity 15%), and conclude with one recommended option.

Outline format: every section on its own numbered line (`[Section role]: [Section topic]`), with five fields below it:
- `Goal`: what the section achieves for the reader; cites the Brief `Reader outcome` item it serves
- `Content`: the scene, actor, metric, or claim the section presents
- `Evidence`: source finding IDs or key facts; `[ASSUMED]` where no source supports the section
- `Reason`: why the section sits at this position and takes this form
- `Handoff`: the question, consequence, or contrast that leads into the next section; for the last section, the final takeaway

Field labels are plain text (`- Goal: ...`), never bold. Bold is reserved for the numbered section line. The same applies to every field under the `### Section` headings of the DRAFT `## Structure` section.

Scoring: Goal Alignment is scored against the Brief `Purpose`, `Governing question`, and `Reader outcome`; Impact against the Brief `Audience` and `Reader outcome`. The Recommendation `Why` names the Brief field behind each of these two scores.

**BAD:**
```markdown
## Option 1: Software Locks Constrain Fleet Gate Speed
- **Theme**: Monolithic inventory locking scripts cause 1,200 dispatch halts annually across mid-sized logistics carriers
- **Outline**: Lead (Riverton outage) -> Nut graf (42M EUR impact) -> Body (Lock contention) -> Resolution (Decoupled queues)
- **Score**: goal_alignment=5, supportability=5, impact=4, specificity=5 (composite: 4.75)

## Recommendation
- **Option**: 1
- **Why**: Option 1 achieves the highest composite score (4.75).
```

**GOOD:**
```markdown
## Option 1: Software Locks Constrain Fleet Gate Speed
- **Theme**: Monolithic inventory locking scripts cause 1,200 dispatch halts annually across mid-sized logistics carriers
- **Outline**:
  1. **Lead and Nut Graf (Anecdote)**: Riverton outage widened to 42M EUR industry cost
     - Goal: Reader recognizes database locks as a fleet-level cost [Reader outcome: know]
     - Content: Four-hour gate stop at Riverton; 1,200 halts and 42M EUR across carriers
     - Evidence: WRTHUB-IN01 F-03, F-07
     - Reason: Operations directors react to a concrete stoppage before an abstract mechanism
     - Handoff: Why does one script stop sixteen trailers? -> lock contention
  2. **Body: Lock contention turns one script into a site-wide halt**
     - Goal: Reader understands the mechanism [Reader outcome: know]
     - Content: Single inventory table, exclusive locks, dispatch queue waits
     - Evidence: WRTHUB-IN01 F-11
     - Reason: The mechanism must precede the fix, or the fix reads as arbitrary
     - Handoff: Manual workarounds created a second failure: corrupted inventory
  3. **Body: Decoupled queues remove the single lock**
     - Goal: Reader believes decoupling is the lowest-risk fix [Reader outcome: believe]
     - Content: Queue-based dispatch pilot, before and after gate times
     - Evidence: WRTHUB-IN01 F-14; pilot gate time [ASSUMED]
     - Reason: Proof follows mechanism; one counterpoint (migration cost) tests the thesis
     - Handoff: What changed at Riverton once the script was off?
  4. **Ending (Kicker)**: Dry-erase markers stay in the drawer
     - Goal: Reader leaves with the decision threshold [Reader outcome: do]
     - Content: Eight-minute gate clearance; return to the opening scene
     - Evidence: WRTHUB-IN01 F-15
     - Reason: Kicker resolves the lead tension without a new argument
     - Handoff: Audit which scripts hold exclusive locks on shared inventory tables
- **Score**: goal_alignment=5, supportability=4, impact=4, specificity=5 (composite: 4.45)

## Recommendation
- **Option**: 1
- **Why**: Goal alignment: answers the Brief Governing question "Why do dispatch halts keep recurring after every patch?" directly; supportability: three of four sections trace to findings, one value is marked [ASSUMED]; impact: delivers the Brief Reader outcome "do: audit lock-holding scripts" for the declared operations audience; specificity: names a measurable mechanism and fix.
```

**Verification method**: `/verify` checks that the options file contains a Brief, repeated option blocks with the four named criteria, outline sections each carrying the five fields `Goal`, `Content`, `Evidence`, `Reason`, `Handoff` with plain (not bold) labels, and a recommendation whose Goal Alignment and Impact sentences name a Brief field.

## ART-CT-05 [TYPE-OWNED]: Brief Recorded in OPTIONS and DRAFT

Every OPTIONS and DRAFT file must contain a `## Brief` section after the header block, so that a reader or agent can judge options and drafts against the article's goal. Fields: `Mandate` (user request, verbatim), `Purpose`, `Audience` (who, prior knowledge, need), `Reader outcome` (know, believe, do), `Governing question`, `In scope`, `Out of scope`, `Constraints` (length, channel, tone), `Success criteria`. Values the agent derived instead of taking from the user carry `[ASSUMED]`. `/draft-article` copies the Brief from the OPTIONS file (or writes it when no OPTIONS file exists) and records every change in `Brief changes`. `/write-article` never copies the Brief into the output document.

**BAD:**
```markdown
**Source**: _INFO_WRTHUB-IN01_Analysis.md
**Scoring criteria**: Goal Alignment (30%), Supportability (30%), Impact (25%), Specificity (15%)

## Option 1: Software Locks Constrain Fleet Gate Speed
```

**GOOD:**
```markdown
## Brief
- **Mandate**: "Write an article for our operations blog on why dispatch halts keep recurring"
- **Purpose**: Convince operations leads to fund a lock audit before the next peak season [ASSUMED]
- **Audience**: Warehouse operations directors; knows: dispatch processes, not database internals; needs: a cause they can act on
- **Reader outcome**: know: exclusive locks cause site-wide halts; believe: decoupled queues are the lowest-risk fix; do: audit lock-holding scripts
- **Governing question**: Why do dispatch halts keep recurring after every patch?
- **In scope**: Inventory database locks, dispatch queues, pilot results
- **Out of scope**: Vendor selection, hardware upgrades
- **Constraints**: length: 1,200-1,500 words; channel: company operations blog; tone: practitioner, plain
- **Success criteria**: Reader can name the lock mechanism and the first audit step
```

**Verification method**: `/verify` checks that OPTIONS and DRAFT files contain a `## Brief` section with all nine fields, that DRAFT files contain `Brief changes`, and that the output document contains no Brief section.

## ART-EV-01 [TYPE-OWNED]: Evidence Alternation Across Body Sections

The article body must alternate between at least two distinct evidence types (empirical statistics, source quotations, document excerpts, case illustrations). Three consecutive paragraphs relying on the same evidence type are prohibited.

**BAD:**
```markdown
According to report A, latency was 42ms. Report B found latency was 45ms. Report C measured latency at 48ms. Report D recorded latency at 51ms.
```

**GOOD:**
```markdown
According to the October performance audit, database query latency rose from 42ms to 120ms during morning dispatch peaks.

"When locks stacked up, dispatchers simply watched their screens freeze," said Marcus Vance, who oversaw Riverton's morning shift. "No error appeared; the queue simply stopped clearing."

Internal ticket records confirm the pattern: dispatch halts accounted for 84% of all Level-1 support escalations during the fourth quarter.
```

**Verification method**: `/verify` inspects body paragraphs to confirm alternation between quantitative data, qualitative attribution, and documentary evidence.

## ART-EV-02 [TYPE-OWNED]: Quote Discipline, Voice Relevance, and Attribution

Direct quotations must be reserved for authentic voice, judgment, or accountability. Quotes stating basic neutral facts must be paraphrased. All quotations must be attributed to named actors or roles.

**BAD:**
```markdown
"Databases store tables that contain rows and columns," explained an anonymous software developer. "When a query runs, data is fetched."
```

**GOOD:**
```markdown
"We knew the script was fragile, but nobody wanted to rewrite dispatch logic during peak shipping season," said the lead infrastructure engineer for Riverton Freight.
```

**Verification method**: `/verify` checks that direct quotes convey opinion, perspective, or emotional weight rather than dry factual definitions, and verifies attribution.

## ART-EV-03 [TYPE-OWNED]: Traceable Claim Attribution and Source Verification

Every concrete factual assertion, metric, date, or operational figure must be attributed to a registered source finding or explicitly marked `[ASSUMED]`.

**BAD:**
```markdown
Most companies lose millions of dollars every single day because their software is terribly slow and employees hate using it.
```

**GOOD:**
```markdown
Across mid-sized logistics carriers, automated warehouse scripts triggered over 1,200 dispatch halts in 2026, costing operators an estimated 42 million EUR (Logistics Automation Benchmark Report, 2026-Q3).
```

**Verification method**: `/verify` verifies that specific numbers and assertions carry explicit source references or an `[ASSUMED]` label.

## ART-ED-01 [TYPE-OWNED]: Line Clarity, Active Verbs, and Paramedic Method Lard Factor

Sentences must lead with actors as grammatical subjects and express actions in simple active verbs. Nominalizations and passive wind-ups must be cut. The lard factor must remain below one-third.

**BAD:**
```markdown
The implementation of the optimization of the database queries was conducted by the engineering department in order to facilitate the reduction of latency. (23 words)
```

**GOOD:**
```markdown
The engineering team optimized database queries to cut latency. (9 words; lard factor = 60.9%)
```

**Verification method**: `/verify` checks for passive voice constructions (`was conducted by`) and nominalizations (`implementation of the optimization of`).

## ART-ED-02 [TYPE-OWNED]: Style Sheet Consistency Across Terminology and Conventions

Key terms, acronyms, product names, numbers, and dates must be consistent with the document's style sheet throughout the text.

**BAD:**
```markdown
In paragraph 2: "the Riverton distribution center..."
In paragraph 6: "the Riverton warehouse facility..."
In paragraph 9: "Riverton depot #4..."
```

**GOOD:**
```markdown
Consistently throughout text: "the Riverton distribution center" (per DRAFT Style Sheet: Terminology).
```

**Verification method**: `/verify` cross-checks recurring names and numerical formats against the Style Sheet section of the DRAFT file.

## ART-RC-01 [TYPE-OWNED]: Final Release Check Verification Standards

Before an article is released, it must pass the release check (`DRSYNART-SPEC-8.5`) recorded in the DRAFT file or verification audit:
1. Header fields complete and valid (`Doc ID`, `Document Type: article`, `Technique`, `Persona`, `Audience`, `Source`).
2. Every claim backed by a source or marked `[ASSUMED]`.
3. Structural integrity verified (continuous numbering, resolving markdown links).
4. Presentation clean (zero workflow or agent processing metadata).
5. Style-pattern signals below threshold: at most 1 signal detected across Sourcing, Style, Structure, and Voice (`AI_WRITING_DETECTION_RULES.md`). Structural signals produced by a technique by construction (such as fixed triad progression in MINTO) are excluded.
6. Persona trait budget respected (when a persona is set).
7. Word count within target envelope.

**BAD (Incomplete / Failing Record):**
```markdown
## Release Check
- Header: checked
- Fact check: looks ok
- AI test: not run
- Status: done
```

**GOOD (Valid Release Check Record):**
```markdown
## Release Check

- **Header block**: Complete (Doc ID: WRTHUB-ARTICLE-01, Document Type: article, Technique: ABTSTORY, Persona: CXO-ADVISOR, Audience: logistics directors, Source: WRTHUB-DRAFT-01_WarehouseSoftwareBottlenecks.md)
- **Claim attribution**: 14 claims verified against registered findings; 1 forward-looking forecast labeled [ASSUMED]
- **Structural integrity**: Continuous headings, all internal links resolve
- **Metadata hygiene**: Zero agent prompts, scratchpad notes, or workflow tags in body
- **Style-pattern signals**: 0 signals detected (AD-SO: 0, AD-SY: 0, AD-ST: 0, AD-VO: 0); technique structural order excluded
- **Persona compliance**: CXO-ADVISOR formality 8, warmth 3, zero slang, micro-dose budget respected
- **Word count**: 1,840 words (target: 1,500 - 2,000 words)
- **Status**: PASSED
```

**Verification method**: `/verify` inspects the Release Check record in the DRAFT file or audit output, verifying all seven fields and confirming the `PASSED` status.
