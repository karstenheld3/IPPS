---
name: write-ebook
description: Author finished ebook across compiled prompt sequence with chapter memory and release check
disable-model-invocation: true
---

# Write Ebook Workflow

Produce a publication-ready ebook from a draft, an options proposal, or raw input, compiling and executing a multi-prompt tier-3 program with running chapter memory and full release verification.

**Goal**: `YYYY-MM-DD_[Title].md` with completed book manuscript and verified release check

**Why**: Delivers a book-length manuscript with narrative continuity, consistent series style, and chapter-by-chapter pedagogical execution without context-window drift.

## Required Skills

- @skills:write-documents `document_types/EBOOK_GUIDES.md` (craft decisions, chapter execution, stitching sequence, release check)
- @skills:write-documents `document_types/EBOOK_TEMPLATE.md` (section: Output; carries release-check record format)
- @skills:write-documents `AI_WRITING_RULES.md` (anti-AI artifact suppression rules `AW-*` with BAD/GOOD examples, read BEFORE writing and referenced in chapter prompts)
- Technique files (`writing_techniques/[ID]_GUIDES.md`, `writing_techniques/TEMPLATES/[ID]_TEMPLATE.md`) ONLY when `using <ID>` is given
- Persona file (`writing_personas/[PERSONA].md`) ONLY when `as <PERSONA>` is given (`DRSYNART-DD-17`)
- Never load CHECKS files during execution (`DRSYNART-FR-32`, `GRUC-IG-03`)

## MUST-NOT-FORGET

- First response line (`DRSYNART-8.1`): output `Tier 3 - fixed program execution` before any other text
- Tier 3 fixed (`DRSYNART-FR-02`, `DRSYNART-NFR-03`): always generates STRUT and PROMPTS files; executes unless `plan` or `plan only` is passed
- Program caps (`DRSYNART-NFR-01`): max 8 prompt files, 35 prompts total, 12 deliverables; books exceeding caps must be split into parts sharing one master DRAFT
- `plan` or `plan only`: stop execution after STRUT and PROMPTS files are written
- Style Sheet and running memory (`DRSYNART-FR-23`, `DRSYNART-DD-36`): DRAFT holds Style Sheet and Chapter Summaries; if DRAFT is absent, STRUT carries them
- Chapter files convention (`DRSYNART-8.3`): chapter prompts write `_agentwork/ch-NN_[Chapter].md` and append to Chapter Summaries; consumed by stitching
- Checkpoint prompts (`DRSYNART-NFR-05`): separate `/verify` + `/fix` checkpoint prompt after each chapter prompt
- User-only selection (`DRSYNART-DD-08`): load technique or persona ONLY when user specifies `using` or `as`; never guess or complete partial input
- Unknown ID handling (`DRSYNART-FR-04`): list valid IDs from library READMEs and stop
- CHECKS files are invisible during execution; never load them in this workflow
- Invariant 6: writing workflows never modify session tracking files (`NOTES.md`, `PROBLEMS.md`, `PROGRESS.md`, `FAILS.md`)
- `inline` keyword (`DRSYNART-DD-17`): edit target file in place; never create a new file
- Output placement (`DRSYNART-FR-24`): write to active working folder, never to `_agentwork/`
- Release check recording (`DRSYNART-8.5`): record release check in DRAFT when one exists, otherwise in STRUT

## Command Grammar

```text
/write-ebook [<input>] [using <ID>] [as <PERSONA>] [for <audience>] [plan | plan only] [inline]
```

## Context-Specific Branches

- **Branch 1 (Within NFR-01 Caps)**: Manuscript fits within 8 prompt files and 35 prompts total. Plan and execute full book in one program run.
- **Branch 2 (Exceeding NFR-01 Caps - Split into Parts)**: When planned prompts exceed 35 or chapter count exceeds single-call envelope. Refuse unpartitioned start, report NFR-01 cap, and plan as sequential parts (e.g., Part 1, Part 2) sharing the master DRAFT.
- **Branch 3 (Technique / Persona Overrides)**: `using <ID>` applies pedagogical progression per `writing_techniques/[ID]_GUIDES.md`; `as <PERSONA>` applies voice sliders and micro-dose rules per `writing_personas/[PERSONA].md`.

## Steps

1. **Input and Scope Resolution**:
   - Emit `Tier 3 - fixed program execution` on first response line.
   - Resolve `<input>`: DRAFT (`[ID]-DRAFT-NN_`), OPTIONS (`[ID]-OPTIONS-NN_`) with selected option, or raw input (`DRSYNART-DD-17`). Default to newest DRAFT, else newest OPTIONS.
   - Validate `using <ID>` and `as <PERSONA>` against library READMEs; on mismatch list valid names and stop.
   - Scope chapter and prompt counts; verify plan satisfies NFR-01 caps or initiate part split.
2. **Program Planning**:
   - Run `/write-strut` for `_agentwork/__STRUT_[TOPIC].md`. If no DRAFT exists, compile Style Sheet and Chapter Summaries into STRUT.
   - Run `/write-prompts` compiling Section 8.3 pass sequence: chapter prompts (1-2 chapters each reading Style Sheet, Chapter Summaries, and `AI_WRITING_RULES.md`, writing `_agentwork/ch-NN_[Chapter].md` with continuous prose free of staccato, contrast snaps, nominalization chains, and flow-breaking robotic patterns), separate checkpoint prompt after each chapter prompt, copy pass, consistency pass, stitching prompt, fact-check prompt, release check prompt, VCRIV gate.
   - If `plan` or `plan only`: report PROMPTS file paths and stop.
3. **Program Execution**:
   - Execute compiled prompt files sequentially with human review checkpoints between files (`DRSYNART-2.3`).
   - Chapter prompts append 3-5 sentence summaries to DRAFT Chapter Summaries section after each chapter batch.
   - Stitching prompt concatenates front matter, parts, chapters from `_agentwork/`, and back matter into single manuscript.
4. **Release Check and Output Compilation**:
   - Execute release check prompt per `document_types/EBOOK_TEMPLATE.md` format and run final VCRIV gate; recommend `/verify` before publishing.
   - Record release check in DRAFT if present, else in STRUT.
   - If `inline`: update target file in place.
   - Else: compile `YYYY-MM-DD_[Title].md` using `document_types/EBOOK_TEMPLATE.md` section Output.

## Output

- Deliverable: `YYYY-MM-DD_[Title].md` in working folder.
- Scaffolding: `__STRUT_[TOPIC].md`, `_PROMPTS_[NN]-[Topic].md`, and intermediate `_agentwork/ch-NN_*.md` (deleted on `/cleanup`).
- Contains: FR-24 header block (`Doc ID`, `Document Type: ebook`, `Technique`, `Persona`, `Audience`, `Source`), front matter, parts, chapters, exercises, and back matter.
- Release check record: recorded in DRAFT if present, else in STRUT.

## Quality Gate

- [ ] First response line declares `Tier 3 - fixed program execution`
- [ ] Program plan complies with NFR-01 caps (or partitioned into parts sharing master DRAFT)
- [ ] Header block complete with all six FR-24 fields and Doc ID matches `[TOPIC]-EBOOK-[NN]`
- [ ] Section 8.3 pass sequence compiled with separate checkpoint prompt after each chapter prompt
- [ ] Style Sheet and Chapter Summaries maintained as running memory across all chapter prompts
- [ ] Release check executed and recorded (in DRAFT or STRUT)
- [ ] Deliverable placed in working folder, not `_agentwork/`
- [ ] Zero CHECKS files loaded; zero session tracking files modified
