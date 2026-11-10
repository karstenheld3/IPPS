# DIATAXIS Checks

Audits process discipline and quality improvement for documentation written `using DIATAXIS`.

Evidence sources: final pages, user-need list or planning notes, product interface or version notes, conversation history.

## Process Discipline (PD)

### DIATAXIS-PD-01: User Needs Mapped to Modes

- Action: Agent listed user needs and assigned each to exactly one mode before writing
- Evidence: Each page declares one mode; no page serves two needs
- Failure indicator: Mixed pages, or pages without a recognizable mode
- References: DIATAXIS-ST-01

### DIATAXIS-PD-02: Mode Boundaries Kept

- Action: Agent removed instructions from reference and explanation pages and moved background out of how-to guides
- Evidence: Reference and explanation pages contain no numbered steps; how-to guides contain no conceptual digressions; cross-links exist
- Failure indicator: Steps in explanation pages, opinions in reference pages, theory in how-to guides
- References: DIATAXIS-ST-04, DIATAXIS-CT-03, DIATAXIS-CT-04

### DIATAXIS-PD-03: Procedures Structured

- Action: Agent wrote tutorials and how-to guides as numbered single-action steps with prerequisites and expected results
- Evidence: Numbered steps, prerequisites block, expected-result sentence; how-to titles start with "How to"
- Failure indicator: Prose procedures, missing prerequisites, or no expected result
- References: DIATAXIS-ST-02, DIATAXIS-ST-03, DIATAXIS-CT-02, DIATAXIS-EV-02

### DIATAXIS-PD-04: Tutorial Safety Verified

- Action: Agent designed the tutorial exercise so it cannot damage real data and always succeeds
- Evidence: Tutorial uses practice objects and states the visible result after key steps
- Failure indicator: Tutorial operates on real customer data or depends on optional settings
- References: DIATAXIS-CT-01

### DIATAXIS-PD-05: Labels and Version Checked

- Action: Agent verified interface labels against the product and stated the version
- Evidence: Labels match the interface exactly; "Applies to" line present
- Failure indicator: Paraphrased labels ("the sharing button") or no version
- References: DIATAXIS-EV-01, DIATAXIS-EV-03

## Quality Improvement (QI)

### DIATAXIS-QI-01: Coverage Balance

- Question: Does the set cover all four modes for the feature, or is one mode missing?
- Improvement tip: List the top three support questions; if one is a "why" question without an explanation page, write that page next.

### DIATAXIS-QI-02: First-Step Speed

- Question: How many sentences does a user read before the first action in a how-to guide?
- Improvement tip: Reduce the introduction to one sentence and move prerequisites into a short list.

### DIATAXIS-QI-03: Failure Anticipation

- Question: At which step do users most often fail?
- Improvement tip: Add one sentence after that step stating what the user sees if it failed and what to do.

### DIATAXIS-QI-04: Findability

- Question: Can a user find the right page from its title alone?
- Improvement tip: Use the user's goal words in how-to titles and the exact setting names in reference titles.
