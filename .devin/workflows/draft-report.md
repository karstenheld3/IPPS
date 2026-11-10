---
description: Draft working report structure, chapter goals, evidence placement, and style sheet
default_tier: 1 (fixed)
---

# Draft Report Workflow

Expand an options proposal or raw research input into a structured working report draft with a Brief, chapter goals, per-chapter fill-in instructions, diagram placeholders, evidence placement, and a project style sheet.

**Goal**: `[ID]-DRAFT-NN_[Title].md` ready for final report authoring

**Why**: Establishes report pyramid architecture, key-line argument flow, and evidence placement before drafting full prose.

## Required Skills

- @skills:write-documents `document_types/REPORT_GUIDES.md` (craft decisions, key-line logic, action titles)
- @skills:write-documents `document_types/REPORT_TEMPLATE.md` (section: DRAFT)
- @skills:write-documents `AI_WRITING_RULES.md` (anti-AI artifact suppression rules `AW-*`, read BEFORE drafting)
- Technique files (`writing_techniques/[ID]_GUIDES.md`, `writing_techniques/TEMPLATES/[ID]_TEMPLATE.md`) ONLY when `using <ID>` is given
- Never load CHECKS files during execution (`DRSYNART-FR-32`, `GRUC-IG-03`)

## MUST-NOT-FORGET

- User-only selection (`DRSYNART-DD-08`): load technique ONLY when user specifies `using <ID>`; never guess or complete partial input
- Unknown ID handling (`DRSYNART-FR-04`): list valid IDs from library READMEs and stop
- No persona (`DRSYNART-DD-17`): `as <PERSONA>` is not honored in report drafting; ignore with notice if passed
- CHECKS files are invisible during execution; never load them in this workflow
- Invariant 6: writing workflows never modify session tracking files (`NOTES.md`, `PROBLEMS.md`, `PROGRESS.md`, `FAILS.md`)
- `inline` keyword (`DRSYNART-DD-17`): edit target file in place; never create a new file
- Output placement (`DRSYNART-FR-24`): write to active working folder, never to `_agentwork/`

## Command Grammar

```text
/draft-report [<input>] [using <ID>] [for <audience>] [inline]
```

## Context-Specific Branches

- **Branch 1 (Without technique)**: Structure report following `document_types/REPORT_GUIDES.md` defaults (Executive Summary, Key-Line Chapters with Action Titles, Exhibits, Appendix Separation).
- **Branch 2 (With technique `using <ID>`)**: Structure report using the section progression of `writing_techniques/[ID]_GUIDES.md`. Report quality rules remain binding.

## Steps

1. **Input and Parameter Resolution**:
   - Resolve `<input>`: selected option from `[ID]-OPTIONS-NN_`, or raw input file/notes (`DRSYNART-DD-17`). If omitted, default to newest OPTIONS file in working folder.
   - If `using <ID>` is passed: verify ID against `writing_techniques/README.md`. On mismatch, list available IDs and stop.
2. **Brief and Structural Expansion**:
   - Copy the `## Brief` from the OPTIONS file, or write it when the input is not an OPTIONS file (`RPT-CT-05`). Record every change in `Brief changes`.
   - Map governing thought and key-line arguments into full report chapter skeleton with action titles, keeping the OPTIONS sections and field names.
   - Define for each chapter/section: `Goal` (cites the Reader outcome item), `Content` (fill-in instructions), `Evidence`, `Reason`, diagram/exhibit placeholders (`DRSYNART-DD-17`), and `Handoff`; field labels plain, not bold (`RPT-CT-04`).
3. **Evidence and Style Sheet Compilation**:
   - Compile Evidence Placement block: map factual claims, metrics, and data points to source finding IDs.
   - Initialize Style Sheet: document standardized terms, units, numerical conventions, and exhibit numbering.
   - Note unresolved client or SME questions in Open Questions block.
4. **Output Generation**:
   - If `inline`: update the specified target file in place.
   - Else: write `[ID]-DRAFT-NN_[Title].md` using `document_types/REPORT_TEMPLATE.md` section DRAFT.

## Output

- Deliverable: `[ID]-DRAFT-NN_[Title].md` in working folder.
- Contains: header block (`Doc ID`, `Document Type: report`, `Technique`, `Audience`, `Source`, `Chosen option`),
  Brief, Structure (all chapters with `Goal`, `Content`, `Evidence`, `Reason`, diagram placeholders, `Handoff`), Evidence Placement, Style Sheet, Open Questions, and Release Check skeleton.

## Quality Gate

- [ ] Header block complete and Doc ID matches `[TOPIC]-REPORT-DRAFT-[NN]`
- [ ] Brief present with all nine fields and `Brief changes`
- [ ] Skeleton contains all chapters with action titles, `Goal`, `Content`, `Evidence`, `Reason`, `Handoff`, and diagram placeholders
- [ ] Evidence Placement traces all key claims to source IDs or marks `[ASSUMED]`
- [ ] Style Sheet initialized with terms, units, numbering, and conventions
- [ ] File placed in working folder, not `_agentwork/`
- [ ] Zero CHECKS files loaded; zero session tracking files modified
