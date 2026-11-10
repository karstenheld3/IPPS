---
name: propose-article
description: Propose article outline candidates with scoring and recommendation
disable-model-invocation: true
---

# Propose Article Workflow

Generate scored outline candidates for an article, blog post, or landing page, select the strongest, and produce an options proposal.

**Goal**: `[ID]-OPTIONS-NN_[Title].md` with scored candidate outlines and one recommendation

**Why**: Generates structured, comparable options before drafting prose, ensuring the strongest hook, angle, and evidence structure are selected.

## Required Skills

- @skills:write-documents `document_types/ARTICLE_GUIDES.md` (craft decisions, option scoring)
- @skills:write-documents `document_types/ARTICLE_TEMPLATE.md` (section: OPTIONS)
- Technique GUIDES (`writing_techniques/[ID]_GUIDES.md`) ONLY when `using <ID>` is given; the type TEMPLATE section OPTIONS wraps the technique's Section Inventory; a technique-owned OPTIONS template (`[ID]_OPTIONS_TEMPLATE.md`) exists only where the planning artifact is not a section outline (today: MINTO)
- Never load CHECKS files during execution (`DRSYNART-FR-32`, `GRUC-IG-03`)

## MUST-NOT-FORGET

- User-only selection (`DRSYNART-DD-08`): load technique ONLY when user specifies `using <ID>`; never guess or complete partial input
- Unknown technique ID (`DRSYNART-FR-04`): list available IDs from `writing_techniques/README.md` and stop
- CHECKS files are invisible during execution; never load them in this workflow
- Invariant 6: writing workflows never modify session tracking files (`NOTES.md`, `PROBLEMS.md`, `PROGRESS.md`, `FAILS.md`)
- `inline` keyword (`DRSYNART-DD-17`): edit target file in place; never create a new file
- Output placement (`DRSYNART-FR-24`): write to active working folder, never to `_agentwork/`

## Command Grammar

```text
/propose-article <input> [using <ID>] [for <audience>] [N options] [compare techniques <ID>, <ID>[, <ID>[, <ID>]]] [inline]
```

## Context-Specific Branches

- **Branch 1 (Without technique)**: Apply `document_types/ARTICLE_GUIDES.md` defaults (Theme, Angle, Lead Type, Nut Graf). Default candidate count: 3 options (range 2-5).
- **Branch 2 (With technique `using <ID>`)**: Technique GRUC overrides macro-structure, section progression, and default option count per `DRSYNART-FR-35`. Article quality rules remain binding.
- **Branch 3 (Compare techniques `compare techniques <ID>, <ID>[, <ID>[, <ID>]]`)**: Produce one candidate option per specified technique ID (2-4 IDs).

## Steps

1. **Input and Parameter Resolution**:
   - Resolve `<input>`: research Summary, analysis INFO, notes file, or raw text. If omitted, default to newest C2/C1 INFO in working folder.
   - If `using <ID>` or `compare techniques` is passed: verify ID(s) against `writing_techniques/README.md`. On mismatch, list valid IDs and stop.
   - Resolve option count `N`: default 3, overruled by technique GUIDES or user argument `N options`.
2. **Brief**:
   - Write the `## Brief` section (`ART-CT-05`): Mandate (user request, verbatim), Purpose, Audience, Reader outcome, Governing question, In scope, Out of scope, Constraints, Success criteria. Mark values derived instead of taken from the user with `[ASSUMED]`.
3. **Candidate Generation**:
   - Read input material and extract core tension, primary empirical facts, and audience takeaways.
   - Generate `N` distinct outline options following the active branch (theme statement, lead type, section sequence, ending).
   - Write every outline section on its own numbered line with five fields: `Goal` (cites the Reader outcome item), `Content`, `Evidence`, `Reason`, `Handoff`; field labels plain, not bold (`ART-CT-04`).
4. **Scoring and Selection**:
   - Score each candidate against the four standard criteria from `document_types/ARTICLE_GUIDES.md`: Goal Alignment (30%), Supportability (30%), Impact (25%), Specificity (15%). Score Goal Alignment and Impact against the Brief fields.
   - Select one recommended option and formulate a one-sentence rationale per criterion; the Goal Alignment and Impact sentences name the Brief field they are measured against.
5. **Output Generation**:
   - If `inline`: update the specified target file in place.
   - Else: write `[ID]-OPTIONS-NN_[Title].md` using `document_types/ARTICLE_TEMPLATE.md` section OPTIONS, where `[ID]` is the technique ID or `ARTICLE`. Sequence `NN` is continuous per `[ID]` in the working folder.

## Output

- Deliverable: `[ID]-OPTIONS-NN_[Title].md` in working folder.
- Contains: header block (`Doc ID`, `Document Type: article`, `Technique`, `Source`, `Scoring criteria`), Brief, `N` scored option blocks with five-field outline sections, and final recommendation block.

## Quality Gate

- [ ] Header block complete and Doc ID matches `[TOPIC]-ARTICLE-OPTIONS-[NN]`
- [ ] Brief present with all nine fields; Mandate verbatim; derived values marked `[ASSUMED]`
- [ ] Every outline section on its own line with `Goal`, `Content`, `Evidence`, `Reason`, `Handoff`
- [ ] Exactly `N` candidate options scored across all four weighted dimensions
- [ ] Exactly one option recommended with selection rationale citing Brief fields for Goal Alignment and Impact
- [ ] File placed in working folder, not `_agentwork/`
- [ ] Zero CHECKS files loaded; zero session tracking files modified
