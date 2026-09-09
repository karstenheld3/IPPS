# Curated Research Strategy (MEPI Approach)

Research **[SUBJECT]** using MEPI (Most Executable Point of Information) - curated best options per topic. Follows global Phase 1-4 model in SKILL.md.

## MUST-NOT-FORGET

- Run `/verify` on STRUT plan before proceeding

**Use MEPI instead of MCPI when:** Reversible decisions, time-constrained, action-oriented, low-to-medium stakes (not legal/financial/medical critical).

## Phase 1: Preflight

### Step 1: Create STRUT and Decompose Prompt

- Create `STRUT_[TOPIC].md` via `/write-strut`
- STRUT defines: phases, objectives, steps, deliverables, transitions, 3 VCRIV checkpoints, quality pipeline steps, time log
- **Domain identification**: Determine domain from context, read `DOMAIN_*.md` profile (fallback: DOMAIN_DEFAULT.md), include in STRUT
- Answer 7 decomposition questions per SKILL.md, store PromptDecomposition in STRUT
- At Q5: Confirm MEPI. Switch to MCPI if high-stakes discovered.
- Run `/verify` on STRUT plan
- **Done when**: STRUT created, 7 questions answered, PromptDecomposition stored, effort estimated

### Step 2: Document Assumptions

- Write "Pre-research assumptions" about [SUBJECT]
- Parse prompt for: subject details, scope boundaries, output expectations
- Check conversation history and NOTES.md for prior context
- Label inferred details with [ASSUMED]. Proceed with best interpretation - do NOT ask unless genuinely ambiguous.

### Step 3: Collect Sources (Curated)

- State [SUBJECT] version (e.g., `v2.1.0`) or date `YYYY-MM-DD`
- Create `__[TOPIC]_SOURCES.md`
- Classify discovery platforms from Q7 as FREE/PAID/PARTIAL; use FREE and PARTIAL, note PAID for follow-up
- Collect **5-10 sources per dimension**, top-tier first. Default tier: official docs > vendor > community/analyst
- Assign source IDs: `[TOPIC]-IN01-SC-[SOURCE]-[DOCNAME]`
- Group by category, process PDFs through transcription pipeline
- **Done when**: 5-10 quality sources per dimension, all with IDs, PDFs transcribed

### Step 4: Verify and Correct Assumptions

- Verify against primary sources. If >30% wrong, re-run with corrected understanding (max 2 re-runs).
- Document accuracy in `__[TOPIC]_SOURCES.md` header (e.g., "Preflight accuracy: 7/10 verified")
- **Rubric**: CORRECT = exact match. PARTIAL = spirit correct, details differ (counts as wrong). WRONG = contradicted.

### Step 5: Run First VCRIV

Run quality pipeline on Preflight deliverables (SOURCES, STRUT, PromptDecomposition).

## Phase 2: Planning

### Step 1: TOC Creation

- Follow [RESEARCH_CREATE_TOC.md](RESEARCH_CREATE_TOC.md), use [RESEARCH_TOC_TEMPLATE.md](RESEARCH_TOC_TEMPLATE.md)
- Create `__[TOPIC]_TOC.md`. Summary 5-10 sentences.
- **Done when**: TOC covers major topics, all links resolve

### Step 2: Template Creation

- Create `__TEMPLATE_[TOPIC]_TOPIC.md` with: Header block (Doc ID, Goal, Dependencies, Version/Date scope), Summary (5-10 sentences), Key Facts [VERIFIED], Use Cases, Quick Reference, Main Sections (per TOC), Limitations/Known Issues, Gotchas/Quirks, Sources, Document History
- **Done when**: Template has all required sections

### Step 3: TASKS Plan

- Create `TASKS_[TOPIC]_RESEARCH.md` via `/write-tasks-plan`
- Each task: Status, Estimated effort, Sources, Done-when criteria. Typically 2-4 hours total.
- **Done when**: All TOC topics have corresponding tasks

### Step 4: Run Second VCRIV

Run quality pipeline on Planning deliverables (TOC, template, TASKS).

## Phase 3: Topic-by-Topic, File-by-File Research

Per TASKS plan and STRUT. For each topic:
1. Research official source URLs first
2. Cross-reference community sources for limitations, quirks
3. Create `_INFO_[TOPIC]-IN[XX]_[SUBTOPIC].md` using template
4. **Focus on curated best options** - recommend, don't just list
5. Include **clear recommendation with rationale**
6. **Mandatory inline citations**: `[VERIFICATION_LABEL] (SOURCE_ID | URL or filename)`
7. Update TASKS progress and TOC status. All claims need verification labels.

**VCRIV granularity**: NARROW: per topic file. FOCUSED/EXPLORATORY: per dimension.
**Done when**: All tasks completed with curated recommendations each.

## Phase 4: Final Verification and Sync

- Each dimension MUST have: sources, topic file(s), verification labels. Missing = documented rationale. Zero sources = [CONSULT].
- Cross-verify topic files against TOC, sync summaries back, verify links
- Add to TOC header: `**Research stats**: Xm net | Y docs | Z sources`
- Run final VCRIV. **Done when**: All requirements met, recommendations actionable.

## Global Rules

- **Termination**: Max 2 cycles per quality checkpoint, then [CONSULT]
- **Autonomous**: After Phase 1, NO user interaction until delivery. [CONSULT] only exception.
- **Rollback**: Fundamental error in earlier phase → PROBLEMS.md + consult user

## Scoring Model (When Ranking Requested)

If user intent includes ranking ("best", "top", "recommend", "which should I"):
1. Define 3-5 scoring dimensions relevant to goal
2. Score ALL options 0-3 per dimension, calculate total
3. Top N become recommendations
4. Document rationale for included (why high) and excluded (why cut)

```
**Scoring Dimensions**: Thematic Fit (0-3), Reach (0-3), Accessibility (0-3)
**Included** (score >= 7):
- Option A (9/9): Perfect thematic fit, high reach, easy to contact
**Excluded** (score < 7):
- Option X (4/9): High reach but no thematic fit - wrong audience
```

## Output Format

MEPI INFO document sections:
1. Research Question
2. Strategy & Domain (MEPI + domain profile + rationale)
3. Scoring Model (if ranking) - dimensions, included/excluded rationale
4. Key Findings - curated recommendations with rationale
5. Comparison - pros/cons
6. Recommendation - clear "do this" guidance
7. Limitations - uncovered areas, caveats
8. Sources - quality sources with IDs

## Anti-patterns

- Treating MEPI as "skip quality" - VCRIV still runs
- Missing decomposition - Phase 1 still mandatory
- No recommendation - MEPI must recommend, not just list
- Shallow research - curated != minimal effort