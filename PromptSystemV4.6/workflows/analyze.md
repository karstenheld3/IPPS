---
description: Execute qualitative coding, pattern detection, hypothesis generation, and evidence validation into a single Analysis INFO deliverable
default_tier: 2 (default)
---

# Analyze Workflow

Synthesize research findings into validated knowledge through qualitative coding, pattern detection, abductive hypothesis generation, and evidence validation, compiling into a single C2 Analysis deliverable.

**Goal**: `_INFO_[TOPIC]-IN[NN]_Analysis.md` in `S##_[SUBTOPIC]_Analysis_YYYY-MM-DD\` conforming to `ANALYSIS_TEMPLATE.md`

**Why**: Transforms raw or research inputs into structured, evidence-weighted, falsifiable knowledge with calibrated likelihood and confidence assessments for downstream writing.

## Required Skills

- @skills:analysis-methods `ANALYSIS_GUIDES.md` (orchestration decisions, tier selection, review points, devil's advocate, loop-back)
- @skills:analysis-methods `ANALYSIS_TEMPLATE.md` (single-INFO C2 deliverable structure)
- @skills:analysis-methods `PATTERN-DETECTION_GUIDES.md`, `PATTERN-DETECTION_RULES.md`
- @skills:analysis-methods `HYPOTHESIS_GUIDES.md`, `HYPOTHESIS_RULES.md`
- @skills:analysis-methods `VALIDATION_GUIDES.md`, `VALIDATION_RULES.md`
- Never load CHECKS files during execution (`DRSYNART-FR-32`, `GRUC-IG-03`)

## MUST-NOT-FORGET

- First response line (`DRSYNART-8.1`): output `Tier N - [reason]` before any other text
- No tier 1 (`DRSYNART-FR-02`): `/analyze` has no tier 1 because DD-04 requires a STRUT first; single-turn analysis runs via stage workflows (`/pattern-detect`, `/hypothesize`, `/validate`)
- Tier resolution (`DRSYNART-FR-02`, `DRSYNART-8.1`): Tier 2 default for single topic sets; Tier 3 for 2+ `T##_` topic folders or keyword `tier 3`; escalates from Tier 2 to Tier 3 when planned prompts exceed 10
- Planning anchor (`DRSYNART-DD-04`, `DRSYNART-IG-05`): `/write-strut` first for `__STRUT_[TOPIC].md`, then `/write-prompts`; executes unless `plan` or `plan only`
- Prompt file partitioning: Tier 2 compiles 1 PROMPTS file (3-10 prompts) running without pause; Tier 3 compiles 3 stage PROMPTS files plus devil's advocate prompt attacking top 3 candidates and full VCRIV gate
- User review checkpoints (`DRSYNART-FR-13`): Tier 3 halts between stage prompt files for user inspection after Pattern Map and after Hypothesis Register
- Checkpoint prompts (`DRSYNART-NFR-05`): separate `/verify` + `/fix` checkpoint prompt after each implementation prompt
- Program caps (`DRSYNART-NFR-01`): Tier 3 max 8 prompt files, 35 prompts total, 12 deliverables, 3 VCRIV gates; refuse unpartitioned start if exceeded
- Output deliverable (`DRSYNART-DD-04`, `DRSYNART-FR-17`): exactly one `_INFO_[TOPIC]-IN[NN]_Analysis.md` in `S##_[SUBTOPIC]_Analysis_YYYY-MM-DD\`
- CHECKS files are invisible during execution; never load them in this workflow
- Invariant 6: analysis workflows modify session tracking files (`NOTES.md`, `PROBLEMS.md`, `PROGRESS.md`, `FAILS.md`) only through `/session-save`

## Command Grammar

```text
/analyze [<input>] [tier N] [plan | plan only]
```

## Context-Specific Branches

- **Branch 1 (Tier 2 - Planned Pipeline, Default)**: Input is a single topic set, single INFO, bundle, or raw material. Run `/write-strut` then `/write-prompts` (1 PROMPTS file, 3-10 prompts covering pattern detection, hypotheses, validation, checkpoints, VCRIV). Stop if `plan` or `plan only`. Execute headlessly without pause.
- **Branch 2 (Tier 3 - Multi-Stage Program)**: Input is 2+ `T##_` folders or called with `tier 3` (or Tier 2 plan > 10 prompts). Verify plan complies with NFR-01 caps. Run `/write-strut` then `/write-prompts` for 3 stage prompt files. Include devil's advocate prompt attacking top 3 candidates and full VCRIV gate. Stop if `plan` or `plan only`. Execute stage by stage with user review checkpoints between files.

## Steps

1. **Tier Resolution and Scope**:
   - Evaluate input and keywords: if 2+ `T##_` folders or `tier 3` -> Tier 3; else Tier 2 default.
   - If called with `tier 1`: reject with explanation pointing to stage workflows (`DRSYNART-FR-02`).
   - Emit `Tier N - [reason]` on first response line.
   - For Tier 3, verify prompt and deliverable counts satisfy NFR-01 caps or initiate partition.
2. **Planning**:
   - Determine target step folder `S##_[SUBTOPIC]_Analysis_YYYY-MM-DD\` under session root.
   - Run `/write-strut` to create `_agentwork/__STRUT_[TOPIC].md`.
   - Run `/write-prompts` to generate PROMPTS file(s) with separate `/verify` + `/fix` checkpoint prompts after each implementation step:
     - Tier 2: 1 PROMPTS file (3-10 prompts). If > 10 prompts, escalate to Tier 3.
     - Tier 3: 3 stage PROMPTS files plus devil's advocate prompt attacking top 3 candidates and full VCRIV gate.
   - If `plan` or `plan only`: report PROMPTS file paths and stop.
3. **Execution**:
   - Tier 2: execute prompt sequence headlessly to completion without human pause.
   - Tier 3: execute `_PROMPTS_01` (pattern detection), halt for user review; execute `_PROMPTS_02` (hypotheses), halt for user review; execute `_PROMPTS_03` (validation, devil's advocate challenge, and VCRIV).
   - Write single C2 deliverable incrementally using `ANALYSIS_TEMPLATE.md`: S2 writes Pattern Map, S3 appends Hypothesis Register, S4 appends Validation Report, Layer 1 Research Questions, and Writing Implications.
4. **Verification and Session Save**:
   - Run VCRIV quality gate against `PATTERN-DETECTION_RULES.md`, `HYPOTHESIS_RULES.md`, and `VALIDATION_RULES.md`.
   - Sync tracking via `/session-save`.

## Output

- Deliverable: one `_INFO_[TOPIC]-IN[NN]_Analysis.md` (or nested `_INFO_[TOPIC]-[SUBTOPIC]-IN01_Analysis.md`) in `S##_[SUBTOPIC]_Analysis_YYYY-MM-DD\`.
- Scaffolding: `__STRUT_[TOPIC].md` and `_PROMPTS_*.md` in `_agentwork/` (removed by `/cleanup`).
- Contains: Pattern Map (codebook, findings, themes, contradictions, assumptions, gaps), Hypothesis Register (statements, forms, rivals, falsifiers, test plans), Validation Report (weighted evidence, ACH audit trail, disconfirmation log, 0-8 ranking with Kent likelihood and confidence), Research Questions for Layer 1, and Writing Implications.

## Quality Gate

- [ ] First response line declares `Tier N - [reason]` (Tier 2 or Tier 3; zero Tier 1)
- [ ] Planning produced `__STRUT_[TOPIC].md` before PROMPTS and PROMPTS before content edits
- [ ] Tier 2 executed 1 PROMPTS file without pause; Tier 3 executed 3 stage files with user review between files
- [ ] Tier 3 included devil's advocate prompt attacking top 3 candidate hypotheses
- [ ] Output is exactly one Analysis INFO deliverable matching `ANALYSIS_TEMPLATE.md` in `S##_[SUBTOPIC]_Analysis_YYYY-MM-DD\`
- [ ] Checkpoint prompts (`/verify` + `/fix`) separate from implementation prompts
- [ ] Zero craft or method knowledge in workflow body; zero CHECKS files loaded; session files modified only through `/session-save`
