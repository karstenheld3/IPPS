---
name: draft-article
description: Draft working article structure, section goals, evidence placement, and style sheet
disable-model-invocation: true
---

# Draft Article Workflow

Expand an options proposal or raw research input into a structured working draft with a Brief, section goals, substantive handoffs, evidence placement, and a project style sheet.

**Goal**: `[ID]-DRAFT-NN_[Title].md` ready for final article authoring

**Why**: Establishes section-by-section narrative architecture, resolves evidence citations, and records style sheet conventions before writing full prose. Optional in the tier-1 chain.

## Required Skills

- @skills:write-documents `document_types/ARTICLE_GUIDES.md` (craft decisions, Brief, section goals, handoffs)
- @skills:write-documents `document_types/ARTICLE_TEMPLATE.md` (section: DRAFT)
- @skills:write-documents `AI_WRITING_RULES.md` (anti-AI artifact suppression rules `AW-*`, read BEFORE drafting)
- Technique files (`writing_techniques/[ID]_GUIDES.md`, `writing_techniques/TEMPLATES/[ID]_TEMPLATE.md`) ONLY when `using <ID>` is given
- Persona file (`writing_personas/[PERSONA].md`) ONLY when `as <PERSONA>` is given (`DRSYNART-DD-17`)
- Never load CHECKS files during execution (`DRSYNART-FR-32`, `GRUC-IG-03`)

## MUST-NOT-FORGET

- User-only selection (`DRSYNART-DD-08`): load technique or persona ONLY when user specifies `using` or `as`; never guess or complete partial input
- Unknown ID handling (`DRSYNART-FR-04`): list valid IDs from library READMEs and stop
- CHECKS files are invisible during execution; never load them in this workflow
- Invariant 6: writing workflows never modify session tracking files (`NOTES.md`, `PROBLEMS.md`, `PROGRESS.md`, `FAILS.md`)
- `inline` keyword (`DRSYNART-DD-17`): edit target file in place; never create a new file
- Output placement (`DRSYNART-FR-24`): write to active working folder, never to `_agentwork/`

## Command Grammar

```text
/draft-article [<input>] [using <ID>] [as <PERSONA>] [for <audience>] [inline]
```

## Context-Specific Branches

- **Branch 1 (Without technique)**: Structure draft following `document_types/ARTICLE_GUIDES.md` defaults (Lead, Nut Graf, Body Sections with alternating evidence, Ending).
- **Branch 2 (With technique `using <ID>`)**: Structure draft using the section progression of `writing_techniques/[ID]_GUIDES.md`. Article quality rules remain binding.
- **Branch 3 (With persona `as <PERSONA>`)**: Record persona voice sliders, tone constraints, and micro-dose rules in the Style Sheet section (`DRSYNART-DD-17`).

## Steps

1. **Input and Parameter Resolution**:
   - Resolve `<input>`: selected option from `[ID]-OPTIONS-NN_`, or raw input file/notes (`DRSYNART-DD-17`). If omitted, default to newest OPTIONS file in working folder.
   - If `using <ID>` or `as <PERSONA>` is passed: verify names against `writing_techniques/README.md` and `writing_personas/README.md`. On mismatch, list available names and stop.
2. **Brief and Structural Expansion**:
   - Copy the `## Brief` from the OPTIONS file, or write it when the input is not an OPTIONS file (`ART-CT-05`). Record every change in `Brief changes`.
   - Map chosen thesis/theme and section outline into full heading structure, keeping the OPTIONS sections and field names.
   - Define for each section: `Goal` (cites the Reader outcome item), `Content` (fill-in instructions), `Evidence`, `Reason`, and `Handoff` linking to the next section; field labels plain, not bold (`ART-CT-04`).
3. **Evidence and Style Sheet Compilation**:
   - Compile Evidence Placement block: map every factual claim, metric, and quote to source finding IDs.
   - Initialize Style Sheet: document standardized terms, casing, numerical conventions, and persona voice parameters.
   - Note unresolved author or SME questions in Open Questions block.
4. **Output Generation**:
   - If `inline`: update the specified target file in place.
   - Else: write `[ID]-DRAFT-NN_[Title].md` using `document_types/ARTICLE_TEMPLATE.md` section DRAFT.

## Output

- Deliverable: `[ID]-DRAFT-NN_[Title].md` in working folder.
- Contains: header block (`Doc ID`, `Document Type: article`, `Technique`, `Persona`, `Audience`, `Source`, `Chosen option`),
  Brief, Structure, Evidence Placement, Style Sheet, Open Questions, and Release Check skeleton.

## Quality Gate

- [ ] Header block complete and Doc ID matches `[TOPIC]-ARTICLE-DRAFT-[NN]`
- [ ] Brief present with all nine fields and `Brief changes`
- [ ] Every section carries `Goal`, `Content`, `Evidence`, `Reason`, and `Handoff`
- [ ] Evidence Placement traces all key claims to source IDs or marks `[ASSUMED]`
- [ ] Style Sheet initialized with terms, numbers, and conventions
- [ ] File placed in working folder, not `_agentwork/`
- [ ] Zero CHECKS files loaded; zero session tracking files modified
