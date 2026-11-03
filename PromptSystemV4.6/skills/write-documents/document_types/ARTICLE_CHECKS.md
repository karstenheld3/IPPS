# Article Checks

Audits process discipline and quality improvement for articles written with `/write-article` or planned with `/propose-article` and `/draft-article`.

Evidence sources: final output document, options proposal (`[ID]-OPTIONS-NN_`), working draft (`[ID]-DRAFT-NN_`), planning notes, conversation history.

## Process Discipline (PD)

### ART-PD-01: Theme Statement Drafted First

- Action: Agent formulated a unified single-sentence theme statement before drafting section prose
- Evidence: Working draft or planning notes contain an explicit theme statement governing all section handoffs
- Failure indicator: Prose begins immediately with topical anecdotes lacking a defined central theme
- References: ART-CT-01, ART-ST-02

### ART-PD-02: Options Proposal Scored and Recommended

- Action: Agent drafted candidate options scored against the four standard criteria and recorded a clear selection rationale
- Evidence: `[ID]-OPTIONS-NN_` file records scores for Goal Alignment (30%), Supportability (30%), Impact (25%), and Specificity (15%) with one recommended candidate; every outline section carries `Goal`, `Content`, `Evidence`, `Reason`, `Handoff` as plain (not bold) labels; the `Why` line names the Brief field behind Goal Alignment and Impact
- Failure indicator: Options file missing, unscored, or lacking selection rationale; outline written as one arrow chain; bold field labels below section lines; scores that cite no Brief field
- References: ART-CT-04

### ART-PD-03: Intentional Lead and Nut Graf Pairing

- Action: Agent selected an explicit lead type (anecdotal, scene-setter, news hook) and positioned the nut graf by paragraph 3 to 5
- Evidence: Nut graf appears within the first five paragraphs and explicitly links the lead hook to the theme statement
- Failure indicator: Lead meanders past paragraph 5 without stating what the story is about, or nut graf stands disconnected
- References: ART-ST-02, ART-CT-01

### ART-PD-04: Section Goals and Transition Pacing

- Action: Agent defined a distinct argumentative or narrative goal for each body section and linked them via substantive handoffs
- Evidence: Each section advances one facet of the theme; OPTIONS and DRAFT sections record it in `Goal` and `Handoff`; section openings bridge from the previous section conclusion
- Failure indicator: Body sections repeat similar points or read like disconnected blog items
- References: ART-ST-03, ART-ST-05

### ART-PD-05: Evidence Alternation and Quote Discipline

- Action: Agent alternated evidence types across sections and verified that all quotes carry distinctive subject-matter voice
- Evidence: Hard empirical metrics alternate with real-world cases; quotes provide authentic perspective rather than dry facts
- Failure indicator: Consecutive sections rely solely on abstract statistics, or quotes are used to convey routine numbers
- References: ART-EV-01, ART-EV-02

### ART-PD-06: Sourcing and Factual Verification

- Action: Agent verified every factual claim against research sources or marked unverified forward projections with `[ASSUMED]`
- Evidence: Specific metrics, percentages, and dates trace to registered finding IDs or source documents
- Failure indicator: Broad assertions made without attribution, or unverified claims stated as definitive facts
- References: ART-EV-03

### ART-PD-07: Editorial Passes and Style Sheet Creation

- Action: Agent executed distinct line editing and copyediting passes and recorded recurring conventions in the style sheet
- Evidence: Sentences show Paramedic Method lard reduction (active verbs, low lard factor); terms and casing are standardized
- Failure indicator: High lard factor (>33%), passive nominalizations, or inconsistent spelling and capitalization
- References: ART-ED-01, ART-ED-02

### ART-PD-08: Ending Resolution Connected to Theme

- Action: Agent concluded with an intentional ending type (kicker, circular return, forward look) without adding new arguments
- Evidence: Final paragraph resolves the opening tension and reinforces the theme statement without introducing unvetted claims
- Failure indicator: Ending introduces an unexpected new argument, trails off, or merely repeats the lead verbatim
- References: ART-ST-04, ART-CT-01

### ART-PD-09: Release Check Documented

- Action: Agent verified the article against all seven release check criteria and recorded the release record
- Evidence: Release check block exists in DRAFT or verification log with complete header, AI detection status, and word count
- Failure indicator: Article published without an explicit release check verification record
- References: ART-RC-01, ART-ST-01

### ART-PD-10: Brief Recorded Before Options

- Action: Agent wrote the Brief before generating options, carried it into the DRAFT, and kept it out of the output document
- Evidence: OPTIONS and DRAFT files contain `## Brief` with all nine fields; Mandate quotes the user request; derived values carry `[ASSUMED]`; DRAFT records `Brief changes`
- Failure indicator: No Brief, Brief written after scoring, Mandate paraphrased, derived values unmarked, or Brief copied into the published article
- References: ART-CT-05, ART-CT-04

## Quality Improvement (QI)

### ART-QI-01: Theme Resonance Across Body

- Question: Does every paragraph actively advance the central theme, or do tangential anecdotes dilute the core argument?
- Improvement tip: Read only the topic sentence of each paragraph against your theme statement; cut or refocus any paragraph that explores a side topic.

### ART-QI-02: Lead Hook Urgency

- Question: Does the opening scenario create immediate, undeniable tension for the target reader within three sentences?
- Improvement tip: Open with the specific moment a breakdown occurred or the exact metric that violated expectations, rather than general background context.

### ART-QI-03: Gold Coin Transition Pacing

- Question: Does the middle of the article maintain momentum, or does it sag after the initial lead and nut graf?
- Improvement tip: Place an unexpected data point, counter-intuitive quote, or striking micro-case at the halfway mark ("gold coin") to reward reader attention.

### ART-QI-04: Authentic Voice and Micro-Dose Register

- Question: Does the article sound like an authoritative practitioner without sounding artificial or over-performing persona traits?
- Improvement tip: Keep persona traits micro-dosed (at most 1-2 distinct expressions per section); ensure technical nouns and active verbs carry the authority.

### ART-QI-05: Kicker Circularity

- Question: Does the ending leave the reader with a lasting insight that reinterprets the opening situation?
- Improvement tip: Return to the specific character, scenario, or data point introduced in paragraph 1, showing how the theme transforms what it means.
