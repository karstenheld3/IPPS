---
description: Execute a multi-approach tier-3 research program with session STRUT, approach prompt sequences, and cross-approach synthesis
default_tier: 3 (fixed)
---

# Research Program Workflow

Execute a long-running, multi-approach research program across 1-4 distinct investigative approaches, synthesizing individual findings into a unified session-level program Summary with approach comparisons.

**Goal**: Multi-approach C1 Knowledge Library with session `_INFO_[TOPIC]-IN01_Summary.md` containing an Approach Comparison section

**Why**: Solves complex, high-stakes undertakings requiring parallel or competing investigative angles while maintaining prompt load boundaries and preventing context-window degradation.

## Required Skills

- @skills:research-methods `RESEARCH_GUIDES.md` (program structure, tier resolution, caps check, load units)
- @skills:research-methods `SKILL.md` (phase model, source tiers, discovery platforms)
- Strategy files (`RESEARCH_STRATEGY_MEPI.md`, `RESEARCH_STRATEGY_MCPI.md`)
- Domain area profile from `research_areas/` and entity profiles from `research_profiles/`
- Never load CHECKS files during execution (`DRSYNART-FR-32`, `GRUC-IG-03`)

## MUST-NOT-FORGET

- First response line (`DRSYNART-8.1`): output `Tier 3 - fixed program execution` before any other text
- Tier 3 fixed (`DRSYNART-FR-02`): always generates session STRUT, approach STRUTs, and PROMPTS files; executes unless `plan` or `plan only`
- Program caps (`DRSYNART-NFR-01`): max 4 approaches (`T##_` folders), max 8 prompt files, 35 prompts total including checkpoints, 12 deliverables, 3 VCRIV gates
- Preflight refusal (`DRSYNART-IG-06`): if mandate exceeds NFR-01 caps, refuse unpartitioned start and require partition into sequential programs
- `plan` or `plan only`: stop execution after STRUT and PROMPTS files are written
- Approach folder naming: `T0N_[SUBTOPIC]_[Approach]_YYYY-MM-DD/` with nested Doc IDs (`promptsystem-ids.md`)
- Checkpoint prompts (`DRSYNART-NFR-05`): separate `/verify` + `/fix` checkpoint prompt after each implementation prompt
- Human review points (`DRSYNART-2.3`): user reviews between prompt files; execution within each file proceeds headlessly
- Immutable prompt files (`DRSYNART-IG-05`): executed prompt files are never edited; extend by adding new prompt files or approach folders
- Cascade law domain ban: `gesetze-im-internet.de` Playwright only
- Google discovery rule: Google = URL discovery only, click through to primary source websites
- Output placement (`DRSYNART-10.5`): session summary at root; approach summaries, sources, topic files in `T##_` folders
- Invariant 6: research workflows modify session tracking files (`NOTES.md`, `PROBLEMS.md`, `PROGRESS.md`, `FAILS.md`) only through `/session-save`

## Command Grammar

```text
/research-program <goal> [approaches: <A>, <B>[, <C>[, <D>]]] [plan | plan only]
```

## Context-Specific Branches

- **Branch 1 (Within NFR-01 Caps, Default)**: 1-4 approaches, <=8 prompt files, <=35 prompts total. Plan and execute full program.
- **Branch 2 (Exceeding NFR-01 Caps - Partition Required)**: If planned approaches > 4 or prompts > 35, refuse start, report NFR-01 limits, and require partition into sequential programs.

## Phases

### Phase 1: Preflight and Program Planning
1. Emit `Tier 3 - fixed program execution` on first response line.
2. Define 1-4 distinct investigative approaches and record pre-research assumptions (A1..An).
3. Estimate effort (HWH) from `MODEL_INVENTORY.md` workload factors. Check NFR-01 caps; refuse and partition if exceeded.
4. Run `/write-strut` to author session-level `_agentwork/__STRUT_[TOPIC].md`.
5. If called with `plan` or `plan only`: report STRUT path and stop.

### Phase 2: Approach STRUTs and Prompt Generation
1. For each approach (1-4): initialize folder `T0N_[SUBTOPIC]_[Approach]_YYYY-MM-DD/`.
2. Run `/write-strut` to create approach-level `_agentwork/__STRUT_[SUBTOPIC].md` in the approach folder.
3. Run `/write-prompts` to compile 1-2 PROMPTS files per approach (`_agentwork/_PROMPTS_01..02` in the approach folder) with separate `/verify` + `/fix` checkpoints.
4. If called with `plan` or `plan only`: report PROMPTS file paths and stop.

### Phase 3: Program Execution
1. Execute compiled prompt files sequentially with human review checkpoints between files (`DRSYNART-2.3`).
2. Run research topic by topic per active strategy (MEPI/MCPI) and domain profile; transcribe PDFs into `_sources/`.
3. Enforce separate `/verify` + `/fix` checkpoint prompts after each implementation step; enforce at most 3 full VCRIV gates.

### Phase 4: Per-Approach Synthesis
1. Finalize `_INFO_[TOPIC]-[SUBTOPIC]-01_Summary.md` and `_INFO_[TOPIC]-[SUBTOPIC]-02_Sources.md` in each `T##_` folder.
2. Verify all topic files and sources are registered and cross-referenced.

### Phase 5: Program Synthesis and Final Gate
1. Synthesize session-level `_INFO_[TOPIC]-IN01_Summary.md` containing an "Approach Comparison" section evaluating all approaches.
2. Execute final VCRIV quality gate across the complete program deliverable.
3. Sync tracking via `/session-save`.

## Output

Follows SPEC Section 10.5 tier 3 layout:
```text
_YYYY-MM-DD_[Session]/
├── _agentwork/__STRUT_[TOPIC].md
├── T01_[SUBTOPIC]_[Approach]_YYYY-MM-DD/
│   ├── _agentwork/__STRUT_, _PROMPTS_01..02
│   ├── _INFO_[TOPIC]-[SUBTOPIC]-01_Summary.md, -02_Sources.md
│   └── topic files, _sources/
├── T02_.../ (up to 4 approaches)
└── _INFO_[TOPIC]-IN01_Summary.md (Approach Comparison)
```

## Agent-Created Folders

- `_agentwork/` - role: agentwork; parent: working folder (session root and each `T##_` approach folder); creator: Phase 1 and Phase 2; content: `__STRUT_*`, `_PROMPTS_*`
- `_sources/` - role: sources; parent: working folder (each `T##_` approach folder); creator: Phase 3 transcription; content: transcribed sources
- Other research source folders: registered in @skills:research-methods SKILL.md

## Quality Gate

- [ ] First response line declares `Tier 3 - fixed program execution`
- [ ] Program plan complies with NFR-01 caps (<=4 approaches, <=8 prompt files, <=35 prompts total, <=3 full VCRIV gates)
- [ ] Session STRUT documents approaches and pre-research assumptions (A1..An)
- [ ] Every approach folder (`T##_`) has its own STRUT, prompt files, and C1 Knowledge Library
- [ ] Executed prompt files remained immutable (zero post-execution prompt edits)
- [ ] Session-level `_INFO_[TOPIC]-IN01_Summary.md` contains an Approach Comparison section
- [ ] Zero craft or method knowledge in workflow body; zero CHECKS files loaded; session tracking files modified only through `/session-save`
