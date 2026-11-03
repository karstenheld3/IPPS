---
description: Draft working ebook structure, series bible style sheet, and chapter-summary memory
default_tier: 1 (fixed)
---

# Draft Ebook Workflow

Expand an options proposal or raw research input into a structured working ebook draft with a Brief, part and chapter goals, fill-in instructions, diagram placeholders, evidence placement, style sheet series bible, and running chapter-summary memory.

**Goal**: `[ID]-DRAFT-NN_[Title].md` with complete book skeleton, style sheet series bible, and chapter-summary memory

**Why**: Establishes reader transformation path, chapter-by-chapter fill-in instructions, evidence citations, and running memory structure before multi-prompt authoring. Stays in the working folder as the persistent series bible (`DRSYNART-DD-36`).

## Required Skills

- @skills:write-documents `document_types/EBOOK_GUIDES.md` (craft decisions, TOC as argument, chapter patterns)
- @skills:write-documents `document_types/EBOOK_TEMPLATE.md` (section: DRAFT)
- Technique files (`writing_techniques/[ID]_GUIDES.md`, `writing_techniques/TEMPLATES/[ID]_TEMPLATE.md`) ONLY when `using <ID>` is given
- Never load CHECKS files during execution (`DRSYNART-FR-32`, `GRUC-IG-03`)

## MUST-NOT-FORGET

- User-only selection (`DRSYNART-DD-08`): load technique ONLY when user specifies `using <ID>`; never guess or complete partial input
- Unknown ID handling (`DRSYNART-FR-04`): list valid IDs from library READMEs and stop
- No persona (`DRSYNART-DD-17`): `as <PERSONA>` is not honored in ebook drafting; ignore with notice if passed
- CHECKS files are invisible during execution; never load them in this workflow
- Invariant 6: writing workflows never modify session tracking files (`NOTES.md`, `PROBLEMS.md`, `PROGRESS.md`, `FAILS.md`)
- `inline` keyword (`DRSYNART-DD-17`): edit target file in place; never create a new file
- Output placement (`DRSYNART-FR-24`, `DRSYNART-DD-36`): write to active working folder, never to `_agentwork/`; persists across all chapter prompts as series bible and running memory

## Command Grammar

```text
/draft-ebook [<input>] [using <ID>] [for <audience>] [inline]
```

## Context-Specific Branches

- **Branch 1 (Without technique)**: Structure draft following `document_types/EBOOK_GUIDES.md` defaults (Promise, Reader Boundary, Part and Chapter Progression with Action Titles, Repeating Pattern).
- **Branch 2 (With technique `using <ID>`)**: Structure draft using chapter sequence and pedagogical scaffolding of `writing_techniques/[ID]_GUIDES.md`. Ebook quality rules remain binding.

## Steps

1. **Input and Parameter Resolution**:
   - Resolve `<input>`: selected option from `[ID]-OPTIONS-NN_`, or raw input file/notes (`DRSYNART-DD-17`). If omitted, default to newest OPTIONS file in working folder.
   - If `using <ID>` is passed: verify ID against `writing_techniques/README.md`. On mismatch, list available IDs and stop.
2. **Brief and Structural Expansion**:
   - Copy the `## Brief` from the OPTIONS file, or write it when the input is not an OPTIONS file (`EBK-CT-05`). Record every change in `Brief changes`.
   - Map one-sentence promise, target reader boundary, and transformation path into full part and chapter skeleton with action titles, keeping the OPTIONS chapters and field names.
   - Define for each chapter: `Goal` (cites the Reader outcome item), `Content` (fill-in instructions), `Evidence`, `Reason`, diagram/exhibit placeholders, and `Handoff` (`DRSYNART-DD-17`); field labels plain, not bold (`EBK-CT-04`).
3. **Evidence, Style Sheet, and Memory Compilation**:
   - Compile Evidence Placement block: map factual claims, benchmarks, and configuration parameters to source finding IDs.
   - Initialize Style Sheet series bible: document standardized terms, units, code formatting, cross-reference syntax, and recap formulas.
   - Initialize empty Chapter Summaries running memory section (`DRSYNART-DD-36`): prepare entry slots for upcoming chapter prompts.
   - Note unresolved technical or architectural questions in Open Questions block.
4. **Output Generation**:
   - If `inline`: update the specified target file in place.
   - Else: write `[ID]-DRAFT-NN_[Title].md` using `document_types/EBOOK_TEMPLATE.md` section DRAFT.

## Output

- Deliverable: `[ID]-DRAFT-NN_[Title].md` in working folder.
- Contains: header block (`Doc ID`, `Document Type: ebook`, `Technique`, `Audience`, `Source`, `Chosen option`),
  Brief, Promise and Reader Boundaries, Structure (all parts and chapters with `Goal`, `Content`, `Evidence`, `Reason`, diagram placeholders, `Handoff`), Evidence Placement, Style Sheet (series bible), Chapter Summaries (running memory), Open Questions, and Release Check skeleton.

## Quality Gate

- [ ] Header block complete and Doc ID matches `[TOPIC]-EBOOK-DRAFT-[NN]`
- [ ] Brief present with all nine fields and `Brief changes`
- [ ] Skeleton contains all parts and chapters with action titles, `Goal`, `Content`, `Evidence`, `Reason`, `Handoff`, and diagram placeholders
- [ ] Evidence Placement traces all key claims to source IDs or marks `[ASSUMED]`
- [ ] Style Sheet series bible initialized with terms, numbers, cross-references, and recap formulas
- [ ] Empty Chapter Summaries section initialized for running memory
- [ ] File placed in working folder, not `_agentwork/`
- [ ] Zero CHECKS files loaded; zero session tracking files modified
