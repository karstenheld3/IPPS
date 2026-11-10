---
description: Author finished report across single-turn or planned tiers with revision passes and release check
default_tier: 1 (default)
---

# Write Report Workflow

Produce a publication-ready report from a draft, an options proposal, or raw input, executing single-turn at tier 1 or compiling planned prompt sequences at tier 2-3.

**Goal**: `YYYY-MM-DD_[Title].md` with completed report text and verified release check

**Why**: Delivers an evidence-based report matching institutional quality standards, dynamically scaling execution depth from single-turn authoring to planned multi-pass compilation.

## Required Skills

- @skills:write-documents `document_types/REPORT_GUIDES.md` (craft decisions, tier resolution, revision passes, release check)
- @skills:write-documents `document_types/REPORT_TEMPLATE.md` (section: Output; carries release-check record format)
- @skills:write-documents `AI_WRITING_RULES.md` (anti-AI artifact suppression rules `AW-*` with BAD/GOOD examples, read BEFORE writing)
- Technique files (`writing_techniques/[ID]_GUIDES.md`, `writing_techniques/TEMPLATES/[ID]_TEMPLATE.md`) ONLY when `using <ID>` is given
- Persona file (`writing_personas/[PERSONA].md`) ONLY when `as <PERSONA>` is given (`DRSYNART-DD-17`)
- Never load CHECKS files during execution (`DRSYNART-FR-32`, `GRUC-IG-03`)

## MUST-NOT-FORGET

- First response line (`DRSYNART-8.1`, `DRSYNART-NFR-03`): output `Tier N - [reason]` before any other text
- Tier resolution (`DRSYNART-NFR-03`, `DRSYNART-2.3`): tier 1 default when input has <= 6 top-level sections and target <= 5,000 words; tier 2 when exceeding budget or keyword `tier 2`; escalates to tier 3 when tier 2 plan exceeds 10 prompts
- `plan` or `plan only`: stop tier 2-3 execution after STRUT and PROMPTS files are written
- Style Sheet location: without a DRAFT, the STRUT carries the Style Sheet (`DRSYNART-FR-23`)
- User-only selection (`DRSYNART-DD-08`): load technique or persona ONLY when user specifies `using` or `as`; never guess or complete partial input
- Unknown ID handling (`DRSYNART-FR-04`): list valid IDs from library READMEs and stop
- CHECKS files are invisible during execution; never load them in this workflow
- Invariant 6: writing workflows never modify session tracking files (`NOTES.md`, `PROBLEMS.md`, `PROGRESS.md`, `FAILS.md`)
- `inline` keyword (`DRSYNART-DD-17`): edit target file in place; never create a new file
- Output placement (`DRSYNART-FR-24`): write to active working folder, never to `_agentwork/`
- Release check recording (`DRSYNART-8.5`): record release check in DRAFT when one exists, otherwise in STRUT (tier 2-3) or chat response (tier 1 with `Status: SELF-CHECKED`); recommend `/verify` before publishing

## Command Grammar

```text
/write-report [<input>] [using <ID>] [as <PERSONA>] [for <audience>] [tier N] [plan | plan only] [inline]
```

## Context-Specific Branches

- **Branch 1 (Tier 1 - Single-Turn Authoring)**: When input <= 6 sections and <= 5,000 words (and no `tier 2` or `tier 3` keyword). Author full prose, line pass, copy pass, and release check in one turn.
- **Branch 2 (Tier 2 - Planned Sequence)**: When input exceeds tier 1 budget, or called with `tier 2`. Invoke `/write-strut` then `/write-prompts` (1 PROMPTS file, 3-10 prompts). Compile rule per Section 8.3: pass sequence (sections, line, copy, fact-check, release, VCRIV) with separate `/verify` + `/fix` checkpoint prompts (`DRSYNART-NFR-05`). Stop if `plan` or `plan only`. Execute headless without pause.
- **Branch 3 (Tier 3 - Escalated Program)**: When tier 2 plan exceeds 10 prompts per Section 2.3 escalation rule, or called with `tier 3`. Generate multi-file prompt sequence (2-8 files) with human review checkpoints between files. Stop if `plan` or `plan only`.
- **Branch 4 (Technique / Persona Overrides)**: `using <ID>` applies technique structure per `writing_techniques/[ID]_GUIDES.md`; `as <PERSONA>` applies voice sliders and micro-dose rules per `writing_personas/[PERSONA].md`.

## Steps

1. **Tier Resolution and Parameter Parsing**:
   - Evaluate input size and keywords: emit `Tier N - [reason]` on first response line.
   - Resolve `<input>`: DRAFT (`[ID]-DRAFT-NN_`), OPTIONS (`[ID]-OPTIONS-NN_`) with selected option, or raw input (`DRSYNART-DD-17`). Default to newest DRAFT, else newest OPTIONS.
   - Validate `using <ID>` and `as <PERSONA>` against library READMEs; on mismatch list valid names and stop.
2. **Planning (Tier 2-3 only)**:
   - Run `/write-strut` for `_agentwork/__STRUT_[TOPIC].md`. If no DRAFT exists, compile Style Sheet into STRUT.
   - Run `/write-prompts` compiling Section 8.3 pass sequence and checkpoint prompts.
   - If `plan` or `plan only`: report PROMPTS file path and stop.
3. **Execution and Revision Passes**:
   - At Tier 1: write prose, run line and copy passes against Style Sheet and `AI_WRITING_RULES.md` (`AW-SO-01` through `AW-LX-03` - eliminating staccato fragments, contrast snaps, compressed objection blocks, nominalization chains, and other punchy, flow-breaking robotic patterns while preserving persona pacing), and run release check per `document_types/REPORT_TEMPLATE.md` format.
   - At Tier 2-3: execute generated prompts through pass sequence (sections, line, copy, fact-check, release check, VCRIV) with `AI_WRITING_RULES.md` enforced in the line and release-check passes.
4. **Release Check and Output Compilation**:
   - Record release check in DRAFT if present, else in STRUT (tier 2-3) or chat response (tier 1 with `Status: SELF-CHECKED`; recommend running `/verify` before publishing).
   - If `inline`: update target file in place.
   - Else: compile `YYYY-MM-DD_[Title].md` using `document_types/REPORT_TEMPLATE.md` section Output.

## Output

- Deliverable: `YYYY-MM-DD_[Title].md` in working folder.
- Scaffolding (tier 2-3 only): `__STRUT_[TOPIC].md` and `_PROMPTS_[NN]-[Topic].md` in `_agentwork/`.
- Contains: FR-24 header block (`Doc ID`, `Document Type: report`, `Technique`, `Persona`, `Audience`, `Source`), executive summary, action-titled body sections, exhibits, recommendations, and appendices.
- Release check record: recorded in DRAFT if present, else in STRUT or delivered in chat response (`Status: SELF-CHECKED` at tier 1) with recommendation to run `/verify` before publishing.

## Quality Gate

- [ ] First response line declares `Tier N - [reason]`
- [ ] Header block complete with all six FR-24 fields and Doc ID matches `[TOPIC]-REPORT-[NN]`
- [ ] Executive summary stands alone and action titles used on all sections and exhibits
- [ ] Tier 2-3 runs execute via Section 8.3 compile rule with separate checkpoint prompts
- [ ] Release check executed and recorded (`Status: SELF-CHECKED` at tier 1 in DRAFT, STRUT, or chat response) with `/verify` recommended
- [ ] Deliverable placed in working folder, not `_agentwork/`
- [ ] Zero CHECKS files loaded; zero session tracking files modified
