---
description: Propose report outline candidates with scoring, recommendation, and optional sample bake-off
default_tier: 1 (fixed)
---

# Propose Report Workflow

Generate scored outline candidates for an analytical or research report, select the strongest, and produce an options proposal with optional sample bake-off.

**Goal**: `[ID]-OPTIONS-NN_[Title].md` with scored report outline candidates and one recommendation

**Why**: Generates structured, comparable report options before drafting, evaluating governing thoughts, key-line claims, and evidence architecture.

## Required Skills

- @skills:write-documents `document_types/REPORT_GUIDES.md` (craft decisions, option scoring, sample bake-off)
- @skills:write-documents `document_types/REPORT_TEMPLATE.md` (section: OPTIONS)
- @skills:write-documents `AI_WRITING_RULES.md` ONLY when `compare techniques` is given (for sample section authoring and bake-off scoring)
- Technique GUIDES (`writing_techniques/[ID]_GUIDES.md`) ONLY when `using <ID>` or `compare techniques` is given; the type TEMPLATE section OPTIONS wraps the technique's Section Inventory; a technique-owned OPTIONS template (`[ID]_OPTIONS_TEMPLATE.md`) exists only where the planning artifact is not a section outline (today: MINTO)
- Never load CHECKS files during execution (`DRSYNART-FR-32`, `GRUC-IG-03`)

## MUST-NOT-FORGET

- User-only selection (`DRSYNART-DD-08`): load technique ONLY when user specifies `using <ID>` or `compare techniques`; never guess or complete partial input
- Unknown technique ID (`DRSYNART-FR-04`): list available IDs from `writing_techniques/README.md` and stop
- CHECKS files are invisible during execution; never load them in this workflow (`DRSYNART-FR-32`, `DRSYNART-DD-39`)
- Invariant 6: writing workflows never modify session tracking files (`NOTES.md`, `PROBLEMS.md`, `PROGRESS.md`, `FAILS.md`)
- `inline` keyword (`DRSYNART-DD-17`): edit target file in place; never create a new file
- Output placement (`DRSYNART-FR-24`): write to active working folder, never to `_agentwork/`

## Command Grammar

```text
/propose-report <input> [using <ID>] [for <audience>] [N options] [compare techniques <ID>, <ID>[, <ID>[, <ID>]]] [inline]
```

## Context-Specific Branches

- **Branch 1 (Without technique)**: Apply `document_types/REPORT_GUIDES.md` defaults (Governing Thought, Key-Line Claims, Action Titles, Executive Summary). Default candidate count: 3 options (range 2-5).
- **Branch 2 (With technique `using <ID>`)**: Technique GRUC overrides macro-structure and section progression per `DRSYNART-FR-35`. Report quality rules remain binding.
- **Branch 3 (Compare techniques `compare techniques <ID>, <ID>[, <ID>[, <ID>]]`)**: Produce one candidate option per specified technique ID (2-4 IDs). Add sample bake-off: write one sample section per option directly into the OPTIONS file, scored against GUIDES criteria and style-pattern signals, never CHECKS (`DRSYNART-DD-39`).

## Steps

1. **Input and Parameter Resolution**:
   - Resolve `<input>`: analysis INFO (C2), research Summary (C1), notes file, or raw text. If omitted, default to newest C2/C1 INFO in working folder.
   - If `using <ID>` or `compare techniques` is passed: verify ID(s) against `writing_techniques/README.md`. On mismatch, list valid IDs and stop.
   - Resolve option count `N`: default 3, overruled by technique GUIDES, user argument `N options`, or count of IDs in `compare techniques`.
2. **Brief**:
   - Write the `## Brief` section (`RPT-CT-05`): Mandate (user request, verbatim), Purpose, Audience, Reader outcome, Governing question, In scope, Out of scope, Constraints, Success criteria. Mark values derived instead of taken from the user with `[ASSUMED]`.
3. **Candidate Generation**:
   - Read input material and extract governing question, core empirical findings, strategic implications, and target audience needs.
   - Generate `N` distinct outline options following the active branch (governing thought, key-line argument, section sequence with action titles, exhibit plan).
   - Write every outline section on its own numbered line with five fields: `Goal` (cites the Reader outcome item), `Content`, `Evidence`, `Reason`, `Handoff`; field labels plain, not bold (`RPT-CT-04`).
   - If `compare techniques`: author one sample section per candidate option directly into the option block (`DRSYNART-DD-39`).
4. **Scoring and Selection**:
   - Score each candidate against the standard criteria from `document_types/REPORT_GUIDES.md`: Goal Alignment (30%), Supportability (30%), Impact (25%), Specificity (15%). Score Goal Alignment and Impact against the Brief fields.
   - In sample bake-off (`compare techniques`): evaluate sample sections against GUIDES quality heuristics and style-pattern signals (never CHECKS); record scores and findings under each option.
   - Select one recommended option and formulate selection rationale; the Goal Alignment and Impact sentences name the Brief field they are measured against.
5. **Output Generation**:
   - If `inline`: update the specified target file in place.
   - Else: write `[ID]-OPTIONS-NN_[Title].md` using `document_types/REPORT_TEMPLATE.md` section OPTIONS, where `[ID]` is the technique ID or `REPORT`. Sequence `NN` is continuous per `[ID]` in the working folder.

## Output

- Deliverable: `[ID]-OPTIONS-NN_[Title].md` in working folder.
- Contains: header block (`Doc ID`, `Document Type: report`, `Technique`, `Source`, `Scoring criteria`), Brief, `N` scored option blocks with five-field outline sections (including sample section and bake-off evaluation when `compare techniques`), and final recommendation block.

## Quality Gate

- [ ] Header block complete and Doc ID matches `[TOPIC]-REPORT-OPTIONS-[NN]`
- [ ] Brief present with all nine fields; Mandate verbatim; derived values marked `[ASSUMED]`
- [ ] Every outline section on its own line with `Goal`, `Content`, `Evidence`, `Reason`, `Handoff`
- [ ] Exactly `N` candidate options scored across weighted dimensions
- [ ] Sample bake-off included when `compare techniques` is invoked, scored with GUIDES criteria and AI-detection rules (never CHECKS)
- [ ] Exactly one option recommended with selection rationale citing Brief fields for Goal Alignment and Impact
- [ ] File placed in working folder, not `_agentwork/`
- [ ] Zero CHECKS files loaded; zero session tracking files modified
