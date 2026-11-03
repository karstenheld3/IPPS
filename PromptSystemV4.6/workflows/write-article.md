---
description: Author finished article with line pass, copy pass, and release check
default_tier: 1 (fixed)
---

# Write Article Workflow

Author a publication-ready article in one turn from a draft, an options proposal, or raw input, applying line editing, copy editing, and release verification.

**Goal**: `YYYY-MM-DD_[Title].md` with completed article text and verified release check

**Why**: Delivers a publication-ready article with consistent voice, rigorous claim sourcing, and verified quality standards in a single turn.

## Required Skills

- @skills:write-documents `document_types/ARTICLE_GUIDES.md` (craft decisions, revision passes, release check)
- @skills:write-documents `document_types/ARTICLE_TEMPLATE.md` (section: Output; carries release-check record format)
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
- Release check recording (`DRSYNART-FR-23`, `DRSYNART-8.5`): record release check in DRAFT when one exists, otherwise in the chat response (`Status: SELF-CHECKED`); recommend `/verify` before publishing

## Command Grammar

```text
/write-article [<input>] [using <ID>] [as <PERSONA>] [for <audience>] [inline]
```

## Context-Specific Branches

- **Branch 1 (Without technique)**: Apply `document_types/ARTICLE_GUIDES.md` defaults (Lead, Nut Graf, Body with alternating evidence, Ending) and storytelling pass.
- **Branch 2 (With technique `using <ID>`)**: Structure article following `writing_techniques/[ID]_GUIDES.md`. Article quality rules remain binding.
- **Branch 3 (With persona `as <PERSONA>`)**: Apply persona voice sliders and micro-dose traits per `writing_personas/[PERSONA].md` during drafting and line editing.

## Steps

1. **Input and Parameter Resolution**:
   - Resolve `<input>`: DRAFT file (`[ID]-DRAFT-NN_`), OPTIONS file (`[ID]-OPTIONS-NN_`) with selected option, or raw input (`DRSYNART-DD-17`). If omitted, default to newest DRAFT, else newest OPTIONS in working folder.
   - If `using <ID>` or `as <PERSONA>` is passed: verify against library READMEs. On mismatch, list valid names and stop.
2. **Prose Authoring (Write Pass)**:
   - Expand structure into full article prose: headline, lead, nut graf, section bodies with claim attribution, and resolution ending.
   - Trace all factual claims, metrics, and quotes to source IDs or mark `[ASSUMED]`.
3. **Revision Passes (Line and Copy Editing)**:
   - Run line editing pass: apply clarity principles (Paramedic Method, active verbs, sentence rhythm) per `document_types/ARTICLE_GUIDES.md`.
   - Run copy editing pass: apply style sheet conventions (terms, capitalization, numbers) from DRAFT or establish inline consistency.
4. **Release Check and Output Compilation**:
   - Execute release check using format from `document_types/ARTICLE_TEMPLATE.md`: verify header completeness, claim attribution, style-pattern signals, and style sheet adherence.
   - Record release check in DRAFT if it exists, else report it in the chat response with `Status: SELF-CHECKED` and recommend running `/verify` before publishing.
   - If `inline`: update the specified target file in place.
   - Else: write `YYYY-MM-DD_[Title].md` using `document_types/ARTICLE_TEMPLATE.md` section Output.

## Output

- Deliverable: `YYYY-MM-DD_[Title].md` in working folder.
- Contains: FR-24 header block (`Doc ID`, `Document Type: article`, `Technique`, `Persona`, `Audience`, `Source`), followed by full article prose.
- Release check record: recorded in DRAFT if present, else delivered in chat response (`Status: SELF-CHECKED`) with recommendation to run `/verify` before publishing.

## Quality Gate

- [ ] Header block complete with all six FR-24 fields and Doc ID matches `[TOPIC]-ARTICLE-[NN]`
- [ ] Full prose authored across all planned sections with zero placeholders
- [ ] Line and copy editing passes completed against style sheet
- [ ] Release check executed and recorded (`Status: SELF-CHECKED` in DRAFT or chat response) with `/verify` recommended
- [ ] File placed in working folder, not `_agentwork/`
- [ ] Zero CHECKS files loaded; zero session tracking files modified
