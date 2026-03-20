# Curated Research Strategy (MEPI Approach)

Research **[SUBJECT]** using MEPI (Most Executable Point of Information) - curated best options per topic. Follows global Phase 1-4 model in SKILL.md.

## MUST-NOT-FORGET

- Run `/verify` on STRUT plan before proceeding

**Use MEPI instead of MCPI when**: Reversible decisions, time-constrained, action-oriented, low-to-medium stakes (not legal/financial/medical critical)

## Phase 1: Preflight

### Step 1: Create STRUT and Decompose Prompt

- Create `STRUT_[TOPIC].md` via `/write-strut`
- STRUT defines: phases, objectives, steps, deliverables, transitions; enforces 3 VCRIV checkpoints; MUST include quality pipeline steps and time log
- **Domain identification**: Determine domain, read `DOMAIN_*.md` (or DOMAIN_DEFAULT.md), incorporate rules, document in STRUT
- Answer 7 decomposition questions per SKILL.md, store PromptDecomposition in STRUT
- At Q5: Confirm MEPI. Switch to MCPI if high-stakes discovered.
- Run `/verify` on STRUT plan
- **Done when**: STRUT created, 7 questions answered, PromptDecomposition stored, effort estimated

### Step 2: Document Assumptions

- Write "Pre-research assumptions" about [SUBJECT]
- Parse prompt for subject details, scope boundaries, output expectations
- Check conversation history and NOTES.md for prior context
- Document inferred details with [ASSUMED] label
- Proceed with best interpretation - do NOT ask unless genuinely ambiguous

### Step 3: Collect Sources (Curated)

- **Document version scope**: State [SUBJECT] version (e.g., `v2.1.0`) or date `YYYY-MM-DD`
- Create `__[TOPIC]_SOURCES.md`
- Classify discovery platforms from Q7 as FREE/PAID/PARTIAL; use FREE and PARTIAL, note PAID for user follow-up
- Collect **5-10 sources per dimension** (top-tier first); skip exhaustive community collection
- Source tiers from active domain profile. Default: official > vendor > community/analyst
- Assign source IDs: `[TOPIC]-IN01-SC-[SOURCE]-[DOCNAME]`
- Group by category; process all PDF sources through transcription pipeline
- **Done when**: 5-10 quality sources per dimension, all with IDs, PDFs transcribed

### Step 4: Verify and Correct Assumptions

- Verify against primary sources
- If >30% wrong/outdated, re-run with corrected understanding (strikethrough originals). **Max 2 re-runs**, then proceed.
- Document accuracy in `__[TOPIC]_SOURCES.md` header
- **Rubric**: CORRECT = matches exactly. PARTIAL = spirit correct, details differ (counts as wrong). WRONG = contradicted.

### Step 5: Run First VCRIV

Run quality pipeline on Preflight deliverables (SOURCES, STRUT, PromptDecomposition).

## Phase 2: Planning

### Step 1: TOC Creation

- Follow [RESEARCH_CREATE_TOC.md](RESEARCH_CREATE_TOC.md) using [RESEARCH_TOC_TEMPLATE.md](RESEARCH_TOC_TEMPLATE.md)
- Create `__[TOPIC]_TOC.md`; summary 5-10 sentences
- **Done when**: TOC covers major topics, all links resolve

### Step 2: Template Creation

- Create `__TEMPLATE_[TOPIC]_TOPIC.md` with base + domain-specific additions:
  - Header block (Doc ID, Goal, Dependencies, **Version/Date scope**), Summary (5-10 sentences), Key Facts with [VERIFIED] labels, Use Cases, Quick Reference, Main Sections, **Limitations and Known Issues**, **Gotchas and Quirks**, Sources, Document History

### Step 3: TASKS Plan

- Create `TASKS_[TOPIC]_RESEARCH.md` via `/write-tasks-plan`
- Partition TOC topics into discrete tasks with Status, Estimated effort, Sources, Done-when criteria
- Effort estimates typically 2-4 hours total

### Step 4: Run Second VCRIV

Run quality pipeline on Planning deliverables (TOC, template, TASKS).

## Phase 3: Topic-by-Topic Research

Adhere to TASKS plan and STRUT. Run VCRIV per granularity rules.

### Execution

For each topic file from TASKS:
1. Research using official source URLs first
2. Cross-reference with community sources for limitations, quirks
3. Create `_INFO_[TOPIC]-IN[XX]_[SUBTOPIC].md` using template
4. **Focus on curated best options** - recommend, don't just list
5. Include **clear recommendation with rationale** for each topic
6. **Mandatory inline citations**: `[VERIFICATION_LABEL] (SOURCE_ID | URL or filename)`
7. Update TASKS progress and TOC status
- All claims must have verification labels

### VCRIV Granularity

- NARROW: per topic file | FOCUSED/EXPLORATORY: per dimension

## Phase 4: Final Verification and Sync

### Dimension Coverage Check

- Each dimension MUST have: sources, topic file(s), verification labels
- Missing dimensions MUST have documented rationale in STRUT
- 0 sources on any dimension → escalate to [CONSULT]

### Sync and Metadata

- Cross-verify topic files against TOC; sync summaries back into TOC; verify all links
- **Add Research stats to TOC header**: `**Research stats**: Xm net | Y docs | Z sources`

### Run Final VCRIV

## Global Rules

- **Termination**: Max 2 cycles per quality checkpoint. Escalate via [CONSULT] if issues persist.
- **Autonomous**: After Phase 1, NO user interaction until delivery. [CONSULT] is only exception.
- **Rollback**: Fundamental error in earlier phase → document in PROBLEMS.md, consult user.

## Scoring Model (When Ranking Requested)

If user intent includes ranking ("best", "top", "recommend", "which should I"):
1. Define 3-5 scoring dimensions relevant to user's goal
2. Score ALL discovered options 0-3 per dimension, calculate total
3. Use scores to select curated options - top N become recommendations
4. Document selection rationale: **Included** (why high score) and **Excluded** (why didn't make cut)

```
**Scoring Dimensions**: Thematic Fit (0-3), Reach (0-3), Accessibility (0-3)

**Included** (score >= 7):
- Option A (9/9): Perfect thematic fit, high reach, easy to contact

**Excluded** (score < 7):
- Option X (4/9): High reach but no thematic fit - wrong audience
```

## Output Format

MEPI outputs an INFO document with:
1. **Research Question** - What we investigated
2. **Strategy & Domain** - MEPI + domain profile + rationale
3. **Scoring Model** (if ranking) - Dimensions, included/excluded rationale
4. **Key Findings** - Curated recommendations with rationale
5. **Comparison** - Brief pros/cons
6. **Recommendation** - Clear "do this" guidance
7. **Limitations** - What we didn't cover
8. **Sources** - Quality sources with IDs

## Anti-patterns

- Treating MEPI as "skip quality" - VCRIV still runs
- Missing decomposition - Phase 1 is mandatory
- No recommendation - MEPI must recommend, not just list
- Shallow research - curated != minimal effort