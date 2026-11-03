# Article Guide

Read BEFORE writing an article, feature story, analytical essay, or thought-leadership piece with `/propose-article`, `/draft-article`, or `/write-article`.

## 1. Purpose and Reader Outcome

After reading this GUIDE, you can write an article from theme statement to publication release. You can determine the governing theme, select an opening lead and nut graf, order analytical or narrative sections, sustain reader engagement across evidence types, apply clarity and copy editing passes, execute the release check, and integrate writing techniques and personas without structural drift.

## 2. Article Craft Decisions in Working Order

Every article follows ten core craft decisions, executed in the sequence below.

### Decision 1: Theme Statement (Governing Thesis)

- **Question**: What is the piece about in one sentence that crystallizes its tension or consequence?
- **Options**: A static topic label ("Enterprise cloud migration"); an argumentative theme ("Cloud migration reduces infrastructure overhead only when teams decouple legacy monolithic databases first"); an open inquiry ("Why do cloud migrations fail to achieve projected savings?").
- **Criterion**: Choose a theme that asserts a concrete tension, cause, or consequence. Never use a static topic label. The sentence must differentiate this article from any generic treatment of the subject and govern what every section includes or cuts.
- **Source**: William Blundell, *The Art and Craft of Feature Writing*; William Zinsser, *On Writing Well*.
- **Rule Reference**: `ART-CT-01`.

### Decision 2: Opening Lead Type

- **Question**: What does the reader encounter in the first two sentences to create immediate momentum?
- **Options**:
  - Anecdote lead: a concrete person facing a specific choice or breakdown.
  - Statistic lead: a surprising, verified data point or cost calculation.
  - Descriptive lead: a specific scene or operational setting in motion.
  - Contrast lead: a stark mismatch between expectation and reality.
  - Question lead: a direct question sharing the reader's central puzzle.
- **Criterion**: The lead must create an unresolved tension that the nut graf will name and resolve. The reader must meet an actor, a number, or a physical setting within the first two sentences.
- **Source**: Roy Peter Clark, *Writing Tools*; Nieman Storyboard *Annotation Tuesday*.
- **Rule Reference**: `ART-ST-02`.

#### Annotated Excerpt 1: Lead and Nut Graf Pairing

```markdown
At 03:14 on a Tuesday morning, the regional distribution warehouse in Riverton went dark when an automated routing script locked its inventory database. For four hours, sixteen freight trailers sat idling at the gates while dispatchers reverted to clipboards and dry-erase markers.

The Riverton outage was not an isolated glitch: across mid-sized logistics carriers, automated warehouse scripts triggered over 1,200 dispatch halts in 2026, costing operators an estimated 42 million EUR. As freight networks consolidate software layers, the operational bottleneck has shifted from physical road capacity to brittle database locks.
```

*What makes this work*: Paragraph 1 opens with a concrete actor and operational breakdown (Anecdote lead). Paragraph 2 widens the lens with industry-wide data (Nut graf), names the broader trend with a number, and establishes the governing theme before section 1 begins.

### Decision 3: Nut Graf Placement and Promise

- **Question**: Where does the reader learn what the piece is about and why it matters?
- **Options**: Paragraph 2 immediately following the lead; delayed to paragraph 4 or 5 after establishing narrative scene; embedded directly in paragraph 1 for short briefings.
- **Criterion**: The nut graf must appear by paragraph 5 at latest. It must widen the specific lead to the general theme, cite at least one quantified fact, and establish an explicit promise that the body delivers. If the body drifts from the nut graf, revise the nut graf or cut the body sections.
- **Source**: Roy Peter Clark, *Writing Tools*; William Blundell, *The Art and Craft of Feature Writing*.
- **Rule Reference**: `ART-ST-02`.

### Decision 4: Section Ordering Logic

- **Question**: What structural logic connects the body sections?
- **Options**:
  - Argumentative: progressive claims building to a central conclusion.
  - Contrast: juxtaposing two approaches, systems, or case outcomes.
  - Chronological: tracing events or process stages through time.
  - Geographical / Systematic: moving across departments, layers, or regions.
  - Narrative arc: following turning points in an unfolding scenario.
- **Criterion**: Match section logic to the evidence base. If evaluating competing systems, use contrast. If demonstrating a root cause, use argumentative progression. Each section must carry a distinct job and end with an implicit question that the next section answers.
- **Source**: John McPhee, *Structure* (The New Yorker); Jack Hart, *Storycraft*.
- **Rule Reference**: `ART-ST-03`.

### Decision 5: Section Handoffs and Transitions

- **Question**: What connects the end of one section to the beginning of the next?
- **Options**:
  - Question handoff: ending a section with the question raised by its evidence.
  - Thematic echo: picking up a key word or image from the previous section with new context.
  - Contrast bridge: pivoting from one outcome to an opposing result.
  - Cliffhanger / Gold coin: introducing an unresolved data point or paradox that compels reading forward.
- **Criterion**: Never use empty connective adverbs ("Additionally", "Furthermore", "Moreover"). Every handoff must advance content by introducing a new piece of evidence or resolving an open tension.
- **Source**: Roy Peter Clark, *Writing Tools*.
- **Rule Reference**: `ART-ST-03`.

#### Annotated Excerpt 2: Section Transition and Kicker Resolution

```markdown
Manual workarounds kept Riverton's trucks moving until dawn, but they created a second, quieter failure: three hundred pallets were loaded without barcode scans, leaving inventory records corrupted for three weeks.

Resolving that data debt required more than emergency patches. When Riverton's dispatchers finally turned off the legacy script in November, their chief metric was not software uptime but gate velocity: trailers cleared the yard in eight minutes, and the dry-erase markers stayed in the drawer.
```

*What makes this work*: The first paragraph concludes a section with a consequence handoff ("created a second, quieter failure") that propels the reader into the next section. The second paragraph functions as a kicker ending, resolving the initial warehouse breakdown and returning directly to the dry-erase markers introduced in the opening lead.

### Decision 6: Middle Sustainment (Momentum)

- **Question**: How does the body sustain reader energy across long-form analysis?
- **Options**: Alternating evidence types (statistics, expert testimony, document excerpts, case illustrations); re-anchoring to the opening subject mid-piece; embedding counterpoints and boundary conditions; varying sentence rhythm.
- **Criterion**: Alternate evidence types across consecutive paragraphs. Never present three consecutive paragraphs of abstract data or three consecutive quotes. Embed at least one counterpoint or serious objection to test the thesis.
- **Source**: William Blundell, *The Art and Craft of Feature Writing*; John McPhee, *Draft No. 4*.
- **Rule Reference**: `ART-EV-01`.

### Decision 7: Ending Type

- **Question**: How does the article conclude?
- **Options**:
  - Kicker: returning to the opening person, setting, or image with deepened meaning.
  - Consequence: stating the concrete future result of the thesis.
  - Crystallizing quotation: concluding with a source's exact words that summarize the theme.
  - Echoing image: closing with an operational detail that embodies the resolution.
  - Decision threshold: stopping at the precise moment a decision-maker must act.
- **Criterion**: The ending must resolve the tension raised in the lead. Never introduce a new argument or topic in the conclusion. Never write a generic summary that merely repeats the nut graf.
- **Source**: William Blundell, *The Art and Craft of Feature Writing*.
- **Rule Reference**: `ART-ST-04`.

### Decision 8: Revision Sequence

- **Question**: Which revision passes are applied, and in what order?
- **Options**: Single-pass polish; exploratory zero draft followed by line edit; structured three-pass revision (developmental, line, copy/proof).
- **Criterion**: Execute revision in distinct passes:
  1. Developmental pass: verifies theme unity, lead-nut graf pairing, section sequence, and evidence sufficiency.
  2. Line pass: eliminates sentence lard, nominalizations, and weak passive verbs.
  3. Copy and proof pass: checks numbers, citations, style sheet consistency, and formatting.
- **Source**: William Zinsser, *On Writing Well*; John McPhee, *Draft No. 4*.
- **Rule Reference**: `ART-ED-01`.

### Decision 9: Quote and Source Management

- **Question**: Who is quoted directly, and how are sources attributed?
- **Options**: Extended verbatim blocks; short voice quotes integrated into analysis; full paraphrase with source tags; dialogue exchanges.
- **Criterion**: Quotes must add voice, perspective, or accountability, not basic factual data. If a source states a neutral fact, paraphrase it. Attribute every claim to a named actor or role with verifiable context. Be merciless in eliminating platitudes.
- **Source**: William Blundell, *The Art and Craft of Feature Writing*.
- **Rule Reference**: `ART-EV-02`.

### Decision 10: Four-Dimension Unity

- **Question**: What stylistic constraints keep the article unified from first sentence to last?
- **Options**: Declare one setting for each dimension:
  - Mood: investigative, explanatory, reflective, urgent.
  - Pronoun: third person (objective analysis), first person plural (practitioner team), second person (direct tutorial).
  - Tense: past (completed events, historical cases) or present (ongoing system realities).
  - Point of view: close operational, mid-level analytical, distant macroeconomic.
- **Criterion**: Fix all four dimensions before writing. Never shift tense or pronoun without a deliberate, temporary rhetorical purpose.
- **Source**: William Zinsser, *On Writing Well*.
- **Rule Reference**: `ART-CT-02`.

## 3. Type-Owned Decisions and Workflow Integrations

Articles carry specific defaults that govern workflows and tier resolution.

### Execution Tier (Default: Tier 1)

Articles run at tier 1 by default (`DRSYNART-FR-02`, NFR-02). A tier-1 call executes in a single turn (2-10 minutes) and writes the complete article directly. Tier 2 (producing STRUT and PROMPTS) applies only when the user explicitly passes `tier 2` or requests an in-depth planned multi-step sequence.

### Audience Adaptation (`for <audience>`)

The optional parameter `for <audience>` adapts technical depth, vocabulary, and introductory framing:
- `for general`: default register; defines specialized terms on first use; leads with everyday impacts.
- `for practitioners / technical teams`: assumes domain tools and standards; leads with architectural trade-offs; minimizes introductory background.
- `for executive / leadership`: leads with financial and operational impacts; focuses on governance, cost, and decision criteria.
- **Rule Reference**: `ART-CT-03`.

### Option Proposals and Scoring (`/propose-article`)

When invoked via `/propose-article`, the workflow writes an options deliverable named `[ID]-OPTIONS-NN_[Title].md`:
- Brief first: before generating options, write the `## Brief` section (Mandate, Purpose, Audience, Reader outcome, Governing question, In scope, Out of scope, Constraints, Success criteria). Quote the user's request verbatim as Mandate; mark every value you derive instead of taking from the user with `[ASSUMED]`. Without a Brief, nobody can check Goal Alignment or Impact.
- Default option count: exactly 3 candidate options (range 2-5 when specified).
- Outline: every section on its own numbered line with five fields: `Goal` (cites the Reader outcome item it serves), `Content`, `Evidence` (finding IDs or `[ASSUMED]`), `Reason`, `Handoff`. A section whose Goal serves no Reader outcome item is a cut candidate; a missing or empty Handoff signals a break in the argument.
- Scoring criteria:
  - Goal Alignment (30%): how directly the option answers the Brief `Governing question` and serves the Brief `Purpose` and `Reader outcome`.
  - Supportability (30%): whether source findings provide sufficient verifiable evidence; read the `Evidence` field of every section.
  - Impact (25%): significance of the thesis to the Brief `Audience` and its stated need.
  - Specificity (15%): falsifiability and precision of the governing claim.
- Output: exactly one recommended option with composite score; the `Why` line names the Brief field behind the Goal Alignment and Impact scores.
- `/draft-article` copies the Brief and keeps the chosen outline's sections and field names, adding detail (fill-in instructions in `Content`, claim-level Evidence Placement). `/write-article` never copies the Brief into the output.
- **Rule Reference**: `ART-CT-04`, `ART-CT-05`.

### Default Storytelling Pass for Untechniqued Output

When the user calls `/write-article` without `using <ID>`, no technique library file is loaded (`DRSYNART-DD-08`). The article applies the default storytelling pass:
1. Lead: concrete actor or metric tension.
2. Nut graf: scope widening with at least one number.
3. Body: analytical sections ordered by argumentative or contrast logic.
4. Ending: kicker returning to the opening detail.
This ensures untechniqued articles read as engaging human features rather than raw data dumps.
- **Rule Reference**: `ART-ST-05`.

### Technique Override Rule (`using <ID>`)

When the user passes `using <ID>` (e.g., `using ABTSTORY` or `using KABOB`):
- The technique implements the document type's Slot Contract (`DRSYNART-DD-44`) with five fusion assignments:
  1. **Header block = type**: `FRAME` slot (`Doc ID`, `Document Type: article`, `Technique`, `Persona`, `Audience`, `Source`) is owned by the article type.
  2. **OPTIONS/DRAFT scaffolding = type**: `FRAME` slot (Brief, scoring criteria, Style Sheet, Open Questions, Release Check) is owned by the article type.
  3. **Body section inventory and order = technique**: `SECTIONS` slot is filled by the technique's exported Section Inventory (ordered list of section roles and titles).
  4. **Outline wrapping**: In OPTIONS and DRAFT, each technique inventory row is wrapped with the five DD-43 outline fields (`Goal`, `Content`, `Evidence`, `Reason`, `Handoff`).
  5. **Technique exemptions**: Any stage exemptions (such as MINTO's AMINTON Q/A tree in OPTIONS) live in the technique's own GUIDES, not in type files or session notes.
- Without `using <ID>`, the article type's default Section Inventory (Lead/Nut Graf, Body claims, Ending/Kicker) applies.
- Article-level quality standards (`ART-ED-01`, `ART-EV-01..03`, `ART-RC-01`) remain in full effect.
- Technique rules never waive house style or privacy rules.

## 4. Editorial Quality and Consistency Standards

### Edit Levels Applied to Articles

Articles undergo three cumulative editing passes:
1. Line edit: clarity, flow, voice modulation, and lard reduction.
2. Copyedit: punctuation, terminology consistency, dates, numbers, and style sheet compliance.
3. Proofread: production defects, broken markdown links, and formatting glitches.
Developmental editing is achieved during the options and draft phases.

### Clarity Principles (Line Edit)

Every article sentence must satisfy three clarity principles:
1. **Lanham's Paramedic Method**: Circle prepositions and weak state-of-being verbs (`is`, `was`, `has`). Locate the real action, name the real actor as the grammatical subject, and express the action in an active verb. Keep the lard factor (words cut divided by original words) below one-third.
2. **Williams's Characters and Actions**: Ensure characters are subjects and actions are verbs. Place familiar context at the beginning of sentences and push new, complex information to the stress position at the end.
3. **Pinker's Classic Style**: Write as a seeing observer positioning the reader to see an objective reality. Eliminate bureaucratic nominalizations that bury active verbs inside Latinate nouns (e.g., replace "the implementation of the system was undertaken" with "the team implemented the system").
- **Rule Reference**: `ART-ED-01`.

### Fact-Checking Standard

Fact-checking is an independent verification function (Borel, *The Chicago Guide to Fact-Checking*):
- Line-by-line verification: every name, title, organization, date, count, calculation, and quotation must be traced to a registered source finding.
- Independent verification: in multi-step workflows, fact-checking is executed by a separate prompt or pass that did not author the text.
- Labeling: unverified assumptions must be tagged `[ASSUMED]`.
- **Rule Reference**: `ART-EV-03`.

### Recap Convention

Articles do not carry redundant summary paragraphs. If a recap is required at the end of a major section:
- It must state an actionable capability or forward-looking takeaway ("You can now calculate dispatch queue times using...").
- It must never merely re-list points already discussed.

### Release Check Standards

Before publication, every article must pass the release check (`DRSYNART-SPEC-8.5`):
1. Header fields complete: `Doc ID`, `Document Type: article`, `Technique`, `Persona`, `Audience`, `Source`.
2. Sourcing: every factual claim cited or marked `[ASSUMED]`.
3. Structural integrity: continuous section numbering, all markdown links resolve.
4. Clean presentation: zero workflow or agent processing metadata in body.
5. AI writing threshold: detection signals below threshold (no synthetic throat-clearing, balanced sentence lengths, no repetitive transition words).
6. Word count: within target range.
- **Rule Reference**: `ART-RC-01`.

### Output Naming Conventions

All article artifacts follow `DRSYNART-FR-24`:
- Options file: `[ID]-OPTIONS-NN_[Title].md`
- Draft file: `[ID]-DRAFT-NN_[Title].md`
- Final article: `YYYY-MM-DD_[Title].md`
- Deliverables reside in the active working folder, never in `_agentwork/`.

## 5. Named Failure Modes and Strategic Mitigations

1. **Lead without a Nut Graf**: The article opens with a vivid story or scene but never explains what broader trend it represents or why the reader should care.
   - *Strategic mitigation*: Check paragraph 3 to 5. Insert an explicit nut graf that widens from the single subject to the industry or systemic scale with at least one concrete number. See `ART-ST-02`.
2. **Nut Graf that Repeats the Lead**: The nut graf merely rephrases the opening anecdote rather than widening the scope.
   - *Strategic mitigation*: The lead is specific; the nut graf is general. Ensure the nut graf provides baseline context and promises what the body will prove. See `ART-ST-02`.
3. **Section without a Job**: A body section provides descriptive background or historical summary without advancing the core thesis.
   - *Strategic mitigation*: Assign each section an explicit claim or job. If cutting the section does not break the argument, delete or merge it. See `ART-ST-03`.
4. **Transition by "Additionally"**: Consecutive sections are joined by mechanical adverbs ("Additionally", "Furthermore", "In addition") indicating an unstructured list.
   - *Strategic mitigation*: Replace additive transitions with content handoffs: an unanswered question, a counterpoint, or a consequence bridge. See `ART-ST-03`.
5. **Ending Introduces New Topics**: The conclusion raises a completely new policy question, speculative risk, or unrelated observation.
   - *Strategic mitigation*: Strip new claims from the final paragraphs. Return to the opening actor or image (kicker) to resolve the original tension. See `ART-ST-04`.
6. **Summary Ending that Repeats the Nut Graf**: The conclusion acts as a dry executive abstract, repeating points already established.
   - *Strategic mitigation*: Delete summary bullets. Land on a kicker, a crystallizing quotation, or a clear decision threshold. See `ART-ST-04`.
7. **Over-Quoting and Banal Quotes**: The article relies on lengthy quotes that convey generic facts rather than authentic voice.
   - *Strategic mitigation*: Paraphrase factual statements into crisp prose. Reserve direct quotes for authoritative judgment, emotional resonance, or colorful expression. See `ART-EV-02`.
8. **Theme Drift into Topic Survey**: The article forgets its governing thesis and becomes an encyclopedia entry listing various features of the topic.
   - *Strategic mitigation*: Test every section against the one-sentence theme statement from Decision 1. Cut sections that describe without arguing. See `ART-CT-01`.
9. **Violated Unity (Perspective Jumps)**: The text shifts erratically between third-person reportage, second-person advice ("you should"), and first-person reflections.
   - *Strategic mitigation*: Fix mood, pronoun, tense, and distance in Decision 10 and maintain them across all sections. See `ART-CT-02`.
10. **Lardaceous and Passive Prose**: Sentences are congested with nominalizations ("the achievement of optimization"), passive verbs, and prepositional pile-ups.
    - *Strategic mitigation*: Run the Paramedic Method pass. Identify the real actor and action verb; trim lard factor below one-third. See `ART-ED-01`.

## 6. Quality Heuristics (Observable Properties)

Test these observable properties on the finished draft:
- **Five-Paragraph Test**: Is the broader theme and why it matters explicitly stated with a number by paragraph 5? (Yes / No)
- **First-Two-Sentences Test**: Does the reader meet a person, a number, or a physical setting within the first two sentences? (Yes / No)
- **Handoff Test**: Does every section transition use a substantive bridge rather than "Additionally", "Furthermore", or "Moreover"? (Yes / No)
- **Kicker Resonance Test**: Does the final paragraph echo or resolve the specific person, image, or tension introduced in the lead? (Yes / No)
- **Evidence Alternation Test**: Are there any instances of three consecutive paragraphs relying on the same evidence type? (Yes / No)
- **Lard Factor Test**: Does any sentence exceed a lard factor of one-third without technical justification? (Yes / No)

## 7. Self-Review Questions

Review the article against these numbered questions before release:
1. Does the header block contain all six required fields with valid values? (`ART-ST-01`)
2. Does the nut graf appear by paragraph 5 and widen the specific lead with quantified data? (`ART-ST-02`)
3. Does each section heading make an informative claim or advance narrative progression? (`ART-ST-03`)
4. Does the ending resolve the opening tension without introducing new arguments? (`ART-ST-04`)
5. Does the entire article support the single governing theme statement without topic drift? (`ART-CT-01`)
6. Does the prose maintain consistent mood, pronoun, tense, and distance throughout? (`ART-CT-02`)
7. Does the body alternate between at least two distinct evidence types? (`ART-EV-01`)
8. Are all direct quotes reserved for authentic voice and attributed to named actors or roles? (`ART-EV-02`)
9. Is every factual claim sourced or marked with an `[ASSUMED]` tag? (`ART-EV-03`)
10. Have passive constructions and nominalizations been converted to active verbs with lard factor under one-third? (`ART-ED-01`)
11. Are terminology, dates, numbers, and conventions consistent with the style sheet? (`ART-ED-02`)
12. Did the manuscript pass all seven criteria of the release check? (`ART-RC-01`)

## 8. Annotated Exemplar Links

Study these complete mentor exemplars for concrete demonstrations of article craft decisions:

- [ABTSTORY Science and Strategy Arc](../writing_techniques/EXAMPLES/ABTSTORY_EXAMPLE_01-ScienceAndStrategyArc.md)
  - *What makes this work*: Demonstrates a crisp narrative tension arc. The lead establishes an accepted baseline, introduces a quantified conflict (BUT), and pivots to an operational consequence (THEREFORE). Body sections alternate data and case evidence, and the kicker ending circles back to reframe the opening premise.
- [KABOB Industry Feature Article](../writing_techniques/EXAMPLES/KABOB_EXAMPLE_01-IndustryFeatureArticle.md)
  - *What makes this work*: Exemplifies the Wall Street Journal feature structure. Opens with an operational plant manager anecdote (Anecdote lead), widens in paragraph 4 to regional manufacturing metrics (Nut graf), sustains the middle with claim-driven headings and contrasting evidence, and closes with a kicker that returns directly to the opening pump failure.

## 9. RULES References

The following rule ID ranges in `ARTICLE_RULES.md` define the enforceable output standards for all articles:
- `ART-ST-01` through `ART-ST-05`: Article structure, header completeness, lead-nut graf pairing, section handoffs, ending resolution, and storytelling arc.
- `ART-CT-01` through `ART-CT-04`: Theme unity, four-dimension consistency, audience adaptation, and options proposal scoring.
- `ART-EV-01` through `ART-EV-03`: Evidence alternation, quote discipline, and factual claim attribution.
- `ART-ED-01` through `ART-ED-02`: Line clarity, Paramedic Method lard factor, and style sheet consistency.
- `ART-RC-01`: Final release check verification standards.
