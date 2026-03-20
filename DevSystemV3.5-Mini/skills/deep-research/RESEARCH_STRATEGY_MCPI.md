# Exhaustive Research Strategy (MCPI Approach)

Research [SUBJECT] exhaustively using MCPI (Most Complete Point of Information). Follows global Phase 1-4 model in SKILL.md.

## MUST-NOT-FORGET

- Run `/verify` on STRUT plan before proceeding

## Phase 1: Preflight

### Step 1: Create STRUT and Decompose Prompt

- Create `STRUT_[TOPIC].md` via `/write-strut`
- STRUT defines: phases, objectives, steps, deliverables, transitions
- STRUT enforces 3 VCRIV checkpoints as deliverables
- STRUT MUST include time log: `Started`, `Ended`, `Active intervals`, `Net research time`
- Domain identification: Determine domain → read `DOMAIN_*.md` → incorporate rules. No match → use DOMAIN_DEFAULT.md
- STRUT MUST include active domain profile and rules
- Answer 7 decomposition questions per SKILL.md, store PromptDecomposition in STRUT
- Run `/verify` on STRUT plan
- Done when: STRUT created, 7 questions answered, PromptDecomposition stored, effort estimated

### Step 2: Document Assumptions

- Write "Pre-research assumptions" about [SUBJECT]
- Parse prompt for: subject details, scope boundaries, output expectations
- Check conversation history and NOTES.md for prior context
- Document inferred details with [ASSUMED] label
- Proceed with best interpretation - do NOT ask unless genuinely ambiguous

### Step 3: Test Discovery Platforms

- Query each platform from Q7 with test search
- Classify access: FREE, PAID, PARTIAL
- Keep FREE/PARTIAL; document PAID in `__SOURCES.md` for user follow-up
- Done when: All platforms tested, access levels documented, selected platforms identified

### Step 4: Collect Sources

- Document version scope explicitly (e.g., `v2.1.0`, `API v3`, or date `YYYY-MM-DD`)
- Create `__[TOPIC]_SOURCES.md` (double underscore = master document)
- Query selected discovery platforms from Step 3 first
- Collect ALL official documentation URLs
- Collect community sources: high-vote SO, GitHub issues, expert blogs, Reddit, changelogs
- Community source rule: Supplement official docs only. Use for limitations, quirks, gotchas. Filter to match [SUBJECT] version.
- Use domain-specific source tiers. Default: official > vendor > community/analyst
- Assign source IDs: `[SUBJECT]-SC-[SOURCE]-[DOCNAME]` per SKILL.md format
- Group by category; include "Related" section for alternatives
- Process all PDF sources through transcription pipeline
- Done when: (a) Official docs TOC fully enumerated, (b) 15-30 sources (min 15), (c) All have IDs, (d) PDFs transcribed

### Step 5: Verify and Correct Assumptions

- Verify against primary sources
- If >30% wrong/outdated, re-run with corrected understanding (strikethrough originals). Max 2 re-runs.
- Document accuracy in `__[TOPIC]_SOURCES.md` header
- Rubric: CORRECT = exact match. PARTIAL = spirit correct, details differ (counts wrong). WRONG = contradicted.

### Step 6: Run First VCRIV

Run quality pipeline on Preflight deliverables (SOURCES, STRUT, PromptDecomposition).

## Phase 2: Planning

### Step 1: TOC Creation

- Follow [RESEARCH_CREATE_TOC.md](RESEARCH_CREATE_TOC.md) using [RESEARCH_TOC_TEMPLATE.md](RESEARCH_TOC_TEMPLATE.md)
- Create `__[TOPIC]_TOC.md`
- Done when: TOC covers all major topics, summary 5-15 sentences, all links resolve

### Step 2: Template Creation

- Create `__TEMPLATE_[TOPIC]_TOPIC.md`
- Structure (base + domain additions): Header block (Doc ID, Goal, Dependencies, Version/Date scope), Summary (5-15 sentences), Key Facts [VERIFIED], Use Cases, Quick Reference, Main Sections, Limitations and Known Issues, Gotchas and Quirks, Sources (same IDs as `__[TOPIC]_SOURCES.md`), Document History
- Include "Template Instructions" section (delete when using)

### Step 3: TASKS Plan

- Create `TASKS_[TOPIC]_RESEARCH.md` via `/write-tasks-plan`
- Partition TOC topics into discrete tasks
- Each task: Status, Estimated effort, Sources, Items to document, Done-when criteria
- Task timing: `- [ ] TK-01: [Description] [HH:MM-HH:MM] Xm` (mark parallel with `(parallel)`)

### Step 4: Run Second VCRIV

Run quality pipeline on Planning deliverables (TOC, template, TASKS).

## Phase 3: Topic-by-Topic, File-by-File Research

### Execution

For each topic file from TASKS:
1. Research using official source URLs first
2. Cross-reference with community sources for limitations, bugs, quirks
3. Process sources per domain profile document handling rules
4. Create `_INFO_[TOPIC]-IN[XX]_[SUBTOPIC].md` using template (XX = sequential, files sort alphabetically)
5. Include "Limitations and Known Issues" with community source citations
6. Mandatory inline citations: Critical conclusions MUST include `[VERIFICATION_LABEL] (SOURCE_ID | URL or filename)`. Referenced files MUST exist in `_SOURCES/`.
7. Update TASKS progress and TOC status
- All claims must have verification labels: [VERIFIED], [ASSUMED], [TESTED], [PROVEN], [COMMUNITY]

### VCRIV per Granularity Rules

- NARROW: VCRIV per topic file
- FOCUSED/EXPLORATORY: VCRIV per dimension
- Done when: All tasks completed and checked off

## Phase 4: Final Verification and Sync

### Dimension Coverage Check

- Each dimension MUST have: 3+ sources, 1+ topic file, verification labels
- Missing dimensions MUST have documented rationale in STRUT
- If any dimension has 0 sources, escalate to [CONSULT]

### Completeness Verification

- Re-read official documentation structure, compare against TOC
- For gaps: assess priority (High/Medium/Low), create INFO files for High/Medium
- Document coverage percentage in TOC header

### Sync and Metadata

- Cross-verify topic files against TOC; sync summaries back into TOC Summary
- Verify all links work; ensure community-sourced limitations included
- Add Research stats to TOC header: `Research stats: 35m net | 62 docs | 79 sources`

### Ex-Post Review Questions

1. Output meets research goal with maximum quality, clarity, correctness?
2. Contains self-critical perspective?
3. Substantial effort on primary sources?
4. Substantial effort on secondary sources?
5. PDFs downloaded and read (not just web research)?
6. All initial research questions answered?
7. Findings properly linked in TOC?

### Run Final VCRIV

- Done when: All requirements met, links work, summaries synced, metadata added

## Global Rules

- Termination: Max 2 cycles per quality checkpoint. Persist → escalate to [ACTOR] via [CONSULT].
- Autonomous: After Phase 1, NO user interaction until delivery. [CONSULT] only exception.
- Rollback: Fundamental error in earlier phase → document in PROBLEMS.md, consult user before rollback.

## Scoring Model (When Ranking Requested)

If user intent includes ranking ("best", "top", "recommend", "which should I"):
1. Define 3-5 scoring dimensions relevant to user's goal
2. Score each option 0-3 per dimension, calculate total
3. Present ranked, most useful on top
4. Include scoring rationale per option

## Output Format

MCPI outputs INFO document with:
1. Research Question
2. Strategy & Domain - MCPI + domain profile + rationale
3. Scoring Model (if ranking requested)
4. Key Findings - Exhaustive, ranked by score if applicable
5. Detailed Analysis - Per-topic breakdowns
6. Limitations - What wasn't covered, caveats
7. Sources - All with IDs and verification labels

See SKILL.md for file naming, verification labels, source hierarchy, and quality rules.