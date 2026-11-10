<!-- ARTICLE TEMPLATE. Skeletons for article planning, drafting, and final output.
Contains three labeled sections: OPTIONS, DRAFT, Output.
Remove all XML comments after creating instantiated documents. -->

## Section: OPTIONS

<!-- Instantiated as [ID]-OPTIONS-NN_[Title].md by /propose-article. Labeled lines, no tables. -->

<!-- SLOT: FRAME (type-owned: header block, Brief, scoring criteria) -->

# OPTIONS: [Title]

**Doc ID**: [TOPIC]-[ID]-OPTIONS-[NN]
<!-- [ID] = technique ID or ARTICLE; sequence NN is continuous per [ID] in the working folder -->
**Document Type**: article
**Technique**: [ID]|none
**Source**: [path to research Summary, analysis INFO, or raw source notes]
**Scoring criteria**: Goal Alignment (30%), Supportability (30%), Impact (25%), Specificity (15%)

<!-- Brief: written before the options. Records the goal every option is scored against (ART-CT-05).
Mark every value the agent derived instead of taking from the user with [ASSUMED]. -->

## Brief
- **Mandate**: "[User request, verbatim]"
- **Purpose**: [Why this article exists and what it must change]
- **Audience**: [Who reads it]; knows: [prior knowledge]; needs: [what the reader needs from the piece]
- **Reader outcome**: know: [insight]; believe: [conviction]; do: [action]
- **Governing question**: [The one question the article answers]
- **In scope**: [Topics covered]
- **Out of scope**: [Topics excluded]
- **Constraints**: length: [word range]; channel: [publication or medium]; tone: [register]
- **Success criteria**: [Observable signal that the article achieved its purpose]

<!-- SLOT: SECTIONS (technique-fillable: candidate outline wrapped with Goal, Content, Evidence, Reason, Handoff; without using <ID> the default Section Inventory below applies) -->

<!-- Repeated option block: repeat 3 times (range 2-5).
Outline: one numbered section per line, five fields below each section (ART-CT-04). Sections match the DRAFT sections. -->

## Option 1: [Action Title]
- **Theme**: [One-sentence governing thesis naming tension, cause, or consequence]
- **Outline**:
  1. **Lead and Nut Graf ([Lead type])**: [Opening subject and widening claim]
     - Goal: [What the section achieves for the reader; cite the Reader outcome item]
     - Content: [Scene, actor, metric, or claim the section presents]
     - Evidence: [Source finding IDs or key facts]|[ASSUMED]
     - Reason: [Why this section sits here and takes this form]
     - Handoff: [Question, consequence, or contrast that leads into section 2]
  2. **Body: [Section claim]**
     - Goal: [...]
     - Content: [...]
     - Evidence: [...]
     - Reason: [...]
     - Handoff: [...]
  3. **Body: [Section claim]**
     - Goal: [...]
     - Content: [...]
     - Evidence: [...]
     - Reason: [...]
     - Handoff: [...]
  4. **Ending ([Ending type])**: [Resolution]
     - Goal: [...]
     - Content: [...]
     - Evidence: [...]
     - Reason: [...]
     - Handoff: [Final takeaway the reader leaves with]
- **Score**: goal_alignment=[1-5], supportability=[1-5], impact=[1-5], specificity=[1-5] (composite: [N.NN])
- **Sample** (compare techniques only): [Sample opening paragraph demonstrating technique arc]

## Option 2: [Action Title]
- **Theme**: [One-sentence governing thesis]
- **Outline**:
  <!-- Same structure as Option 1: every section numbered, each with Goal, Content, Evidence, Reason, Handoff -->
  1. **[Section role]: [Section topic]**
     - Goal: [...]
     - Content: [...]
     - Evidence: [...]
     - Reason: [...]
     - Handoff: [...]
- **Score**: goal_alignment=[1-5], supportability=[1-5], impact=[1-5], specificity=[1-5] (composite: [N.NN])
- **Sample** (compare techniques only): [Sample opening paragraph demonstrating technique arc]

## Option 3: [Action Title]
- **Theme**: [One-sentence governing thesis]
- **Outline**:
  <!-- Same structure as Option 1: every section numbered, each with Goal, Content, Evidence, Reason, Handoff -->
  1. **[Section role]: [Section topic]**
     - Goal: [...]
     - Content: [...]
     - Evidence: [...]
     - Reason: [...]
     - Handoff: [...]
- **Score**: goal_alignment=[1-5], supportability=[1-5], impact=[1-5], specificity=[1-5] (composite: [N.NN])
- **Sample** (compare techniques only): [Sample opening paragraph demonstrating technique arc]

<!-- END SLOT: SECTIONS -->

<!-- SLOT: FRAME (type-owned: recommendation and scoring rationale) -->

## Recommendation
- **Option**: [N]
- **Why**: [One sentence per criterion explaining why this candidate was selected over alternatives; the Goal Alignment and Impact sentences name the Brief field they are measured against]

---

## Section: DRAFT

<!-- Instantiated as [ID]-DRAFT-NN_[Title].md by /draft-article. Labeled lines, no tables. -->

<!-- SLOT: FRAME (type-owned: header block, Brief) -->

# DRAFT: [Title]

**Doc ID**: [TOPIC]-[ID]-DRAFT-[NN]
<!-- [ID] = technique ID or ARTICLE; sequence NN is continuous per [ID] in the working folder -->
**Document Type**: article
**Technique**: [ID]|none
**Persona**: [PERSONA]|none
**Audience**: [short form]|general
<!-- copied from Brief Audience; Brief is authoritative while a Brief exists; Output header (no Brief) is standalone -->
**Source**: [path to OPTIONS file or raw input]
**Chosen option**: [Option N: Action Title]

<!-- Brief: copied from the OPTIONS file (or written here when no OPTIONS file exists). Log every change in Brief changes.
Never copied into the output document (ART-CT-05). -->

## Brief
- **Mandate**: "[User request, verbatim]"
- **Purpose**: [Why this article exists and what it must change]
- **Audience**: [Who reads it]; knows: [prior knowledge]; needs: [what the reader needs from the piece]
- **Reader outcome**: know: [insight]; believe: [conviction]; do: [action]
- **Governing question**: [The one question the article answers]
- **In scope**: [Topics covered]
- **Out of scope**: [Topics excluded]
- **Constraints**: length: [word range]; channel: [publication or medium]; tone: [register]
- **Success criteria**: [Observable signal that the article achieved its purpose]
- **Brief changes**: none|[field]: [old value] -> [new value] ([reason])

<!-- SLOT: SECTIONS (technique-fillable: section scaffolding matching chosen option; without using <ID> the default Section Inventory below applies) -->

<!-- Structure: same sections and field names as the chosen OPTIONS outline. DRAFT adds detail; Content holds fill-in instructions. -->

## Structure

### Section 1: [Lead and Nut Graf]
- Goal: [Opening tension and thesis promise; cite the Reader outcome item]
- Content: [Fill-in instructions: actor or setting introduction, scope widening with metric, thesis promise]
- Evidence: [Source finding IDs]|[ASSUMED]
- Reason: [Why this lead type and nut graf placement serve the Brief]
- Handoff: [Content bridge to Section 2]

### Section 2: [First Body Claim]
- Goal: [First analytical step or narrative turning point; cite the Reader outcome item]
- Content: [Fill-in instructions]
- Evidence: [Source finding IDs]|[ASSUMED]
- Reason: [Why this step comes first]
- Handoff: [Question, consequence, or contrast bridge to Section 3]

### Section 3: [Second Body Claim]
- Goal: [Second analytical step, counterpoint, or mechanism explanation; cite the Reader outcome item]
- Content: [Fill-in instructions]
- Evidence: [Source finding IDs]|[ASSUMED]
- Reason: [Why this step follows Section 2]
- Handoff: [Content bridge to resolution]

### Section 4: [Ending / Kicker]
- Goal: [Resolution returning to opening subject or forward operational consequence; cite the Reader outcome item]
- Content: [Fill-in instructions]
- Evidence: [Source finding IDs]|[ASSUMED]
- Reason: [Why this ending type resolves the lead tension]
- Handoff: [Final takeaway or decision threshold]

<!-- END SLOT: SECTIONS -->

<!-- SLOT: FRAME (type-owned: Evidence Placement, Style Sheet, Open Questions, Release Check) -->

## Evidence Placement
- **Section 1**: [Claim 1 -> Source ID], [Claim 2 -> Source ID]
- **Section 2**: [Claim 3 -> Source ID], [Claim 4 -> Source ID]
- **Section 3**: [Claim 5 -> Source ID], [Claim 6 -> Source ID]
- **Section 4**: [Claim 7 -> Source ID]

## Style Sheet
- **Terminology**: [Standardized term 1; standardized term 2]
- **Numbers and Dates**: [Numerical notation, YYYY-MM-DD date format, currency rules]
- **Tone and Unity**: [Declared mood, pronoun, tense, narrative distance]
- **Cross-Reference Format**: [Section reference convention, citation tag format]

## Open Questions
- [ ] [Open question 1 for author or fact-checker]
- [ ] [Open question 2]

## Release Check
- **Header block**: [Complete / Pending]
- **Claim attribution**: [All claims verified / [ASSUMED] tags applied]
- **Structural integrity**: [Continuous headings, internal links resolve]
- **Metadata hygiene**: [Zero agent prompts or workflow tags in body]
- **Style-pattern signals**: [N signals detected; technique structural order excluded]
- **Persona compliance**: [Slider budget and traits respected]
- **Word count**: [Word count against target]
- **Status**: [SELF-CHECKED / FAILED]

---

## Section: Output

<!-- Instantiated as YYYY-MM-DD_[Title].md by /write-article. Final publication deliverable. -->
<!-- Release-check record format (recorded in DRAFT or reported in chat response at Tier 1 with Status: SELF-CHECKED):
- **Header block**: [Complete / Pending]
- **Claim attribution**: [All claims verified / [ASSUMED] tags applied]
- **Structural integrity**: [Continuous headings, internal links resolve]
- **Metadata hygiene**: [Zero agent prompts or workflow tags in body]
- **Style-pattern signals**: [N signals detected; technique structural order excluded]
- **Persona compliance**: [Slider budget and traits respected / N/A]
- **Word count**: [Word count against target]
- **Status**: [SELF-CHECKED / FAILED]
-->

<!-- SLOT: FRAME (type-owned: header block) -->

# [Article Title]

**Doc ID**: [TOPIC]-ARTICLE-[NN]
**Document Type**: article
**Technique**: [ID]|none
**Persona**: [PERSONA]|none
**Audience**: [free text]|general
**Source**: [path to DRAFT or OPTIONS file, or input path]

<!-- SLOT: SECTIONS (technique-fillable: output body prose skeleton; without using <ID> the default Section Inventory below applies) -->

<!-- Opening lead: 1-2 sentences introducing an unresolved scene, metric, or tension. Meet actor/number/setting immediately. -->

[Opening lead paragraph.]

<!-- Nut graf: appears by paragraph 5 at latest. Widens lead to systemic scale with at least one number and thesis promise. -->

[Nut graf paragraph.]

## [Section 1 Claim Heading]

<!-- First body section: opens with claim or narrative step. Substantive content handoff at end. -->

[Section 1 body paragraphs alternating evidence types...]

## [Section 2 Claim Heading]

<!-- Second body section: advances thesis, embeds counterpoint or mechanism details. -->

[Section 2 body paragraphs...]

## [Section 3 Claim Heading]

<!-- Third body section: deepens evidence, operational implications, or systematic comparison. -->

[Section 3 body paragraphs...]

## [Conclusion / Kicker Heading]

<!-- Ending: kicker returning to opening actor/setting/image, consequence statement, or decision threshold. No new arguments. -->

[Kicker resolution paragraph.]

<!-- END SLOT: SECTIONS -->
