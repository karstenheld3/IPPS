# NOTES: Model Registry Update

**Doc ID**: MDLRGUP-NOTES

Permanent session for updating LLM model registry, pricing, and parameter mapping JSONs.

## Purpose

Fetch current model data from Anthropic and OpenAI provider websites, update canonical JSON files in `[DEVSYSTEM_FOLDER]/skills/llm-evaluation/`, and distribute to all target locations.

## Key Paths

- **Workflow**: `[WORKSPACE_FOLDER]/update-model-registry.md`
- **Canonical JSONs**: `[DEVSYSTEM_FOLDER]/skills/llm-evaluation/`
  - `model-registry.json`
  - `model-pricing.json`
  - `model-parameter-mapping.json`
- **Artifacts**: This session folder (screenshots, DOM extracts, transcriptions)
- **Distribution targets**: `.devin/skills/llm-evaluation/`

## Current Phase

**[2026-10-28 20:22]** P1-P4 done (`60 / 60 min` net 1 AWH budget complete); **P5 gated on DD-01..05 answers**.
- **Plan**: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__STRUT_MDLINVNTRY.md [MDLRGUP-MDLINVNTRY-STRUT]` (`P1`, `P3`, `P4` `[x]`; `P2` waiting for `[ACTOR]` reply on `DD-01..05`; `P5` gated)
- **Research Summary & Decisions (`DD-01..05`)**: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\T02_MDLINVNTRY_ReliableModelInventory_2026-10-28\_INFO_MDLRGUP-MDLINVNTRY-01_Summary.md [MDLRGUP-MDLINVNTRY-IN01]` (Section 5)
- **Recurring Update Prompts Template (`P3-D1`)**: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_PROMPTS_ModelInventoryUpdate_TEMPLATE.md`
- **Open items before/during P5**:
  1. `[ACTOR]` replies with `DD-01..05` decisions (format: `DD-01 a, DD-02 c, DD-03 a, DD-04 a, DD-05 a`) → record in `## Key Decisions` below and check `P2-D1` in `__STRUT_MDLINVNTRY.md`
  2. Execute STRUT `P5` (`P5-S1..S9`, ~45 min outside the 1 AWH budget): apply `DD-01..05` to `PromptSystemV4.5/skills/write-documents/MODEL_INVENTORY.md`, `TASKS_GUIDES.md`, `PROMPTS_GUIDES.md`, `PROMPTS_RULES.md` (`PRMT-SC-05`), `write-prompts.md`, `edird-phase-planning/SKILL.md`, `llm-evaluation/model-registry.json`, `update-model-registry.md` (Phase 9.4 + Google source group `G1`-`G3` + redirected URLs `A1`/`A2`/`A3`/`O3`/`Z3`), and `LLMCAPCLS-IN01`, then mirror `PromptSystemV4.5` → `.devin` and commit

## Key Decisions

- `DD-01..05 presented 2026-10-28 20:22; answers pending`:
  - `DD-01` (Capability representation): recommended `a` (Reuse `UC-1..5` + `ECI band` + `Generation equivalent`) | `b` (Keep `YY-L`) | `c` (METR horizon only)
  - `DD-02` (Work per prompt): recommended `c` (Model-agnostic fixed limits without WF, scored `13/15`) | runner-up `a` (ECI-band → HWH table, scored `12/15`) | `e` (UC → HWH, `10/15`) | `b` (METR 80% + fallback, `7/15`) | `d` (Keep `YY-L` formula, `6/15`)
  - `DD-03` (Behavior profile): recommended `a` (Drop profiles and ledger; use `Notes` column for observations only) | `b` (Keep profiles and ledger)
  - `DD-04` (Environment data): recommended `a` (Remove `Devin cost` and Devin-only rows from `MODEL_INVENTORY.md`; keep in `windsurf-model-registry.json`) | `b` (Keep in `MODEL_INVENTORY.md`)
  - `DD-05` (Inventory scope): recommended `a` (Anthropic, OpenAI, Google Gemini, Z.AI) | `b` (Add xAI, DeepSeek, Mistral, Moonshot) | `c` (Current 3 providers)

## Topic Registry

**Global topics** (registered in ID-REGISTRY.md):
- `MDLRGUP` - Model Registry Update (this session; parent topic for nested IDs)
- `MDLBHVPRM` - Model Behavioral Parameters (eagerness and instruction-following benchmarks)
- `LLMCAPCLS` - LLM Capability Classes (year-letter labels; under review by MDLINVNTRY)

**Subtopics** (session-local):
- `MDLINVNTRY` - Model Inventory Reliability: source-backed inventory, lean TASKS/PROMPTS planning method, recurring inventory update template (nested as MDLRGUP-MDLINVNTRY)

## Topic Folders

- **T01_MDLBHVPRM_BehavioralParameterBenchmarks_2026-10-19** - Research benchmarks for eagerness and instruction_following model parameters
- **T02_MDLINVNTRY_ReliableModelInventory_2026-10-28** - Audit of inventory values (`IN03`), reliable sources per field (`IN04`), work-per-prompt options (`IN05`), and synthesis + `DD-01..05` (`IN01`, `IN02`)

## Related External Design

- KarstensWorkspace `_Sessions\_!AINewsResearch\NOTES.md` "Model and Hardware Tiers" (2026-10-25) and `_INFO_AINWSRCH-MODELTIER-01_GenerationTiering.md`: time-independent model tier record (Vendor generation, Universal Class UC-1..5, Epoch ECI band with snapshot date, generation equivalent). QS-12: no Artificial Analysis scores for tiering. Candidate replacement for the `YY-L` scheme (DD-01)
- KarstensWorkspace `_Sessions\_!AINewsResearch\_PROMPTS_AI-News-Research_TEMPLATE.md`: exemplar for the run-folder prompts template (STRUT P3)

## Migration History

**[2026-08-30]** Restructured from in-skill workflow to workspace-level workflow.
- Moved `update-model-registry.md` from `skills/llm-evaluation/` to workspace root
- Moved `model-sources/` artifacts from `skills/llm-evaluation/model-sources/` to this session
- Deleted `model-sources/` from both DevSystemV4.2 and .devin

## Significant Prompts Log

[2026-10-28 18:45] User reopened the session after the LLMCAPCLS rewrite; set four goals and asked for a 1 AWH STRUT
````text
/session-load E:\dev\IPPS\_Sessions\!ModelRegistryUpdate\

MODEL_INVENTORY.md is full of unreliable information and assumptions
review also
TASKS_GUIDES.md
PROMPTS_GUIDES.md

Goals:
1. We must find a workable solution for agentic work planning in TASKS and PROMPTS files.
2. I want these files to be as general purpose as is needed to be used with any agent or agentic environment.
3. inventory and instructions should not be over-engineered and not consume unnecessary tokens
4. We need reliable sources so that we can use a prompts template that is used to write a prompts file with full instructions to update all model inventories. Like here e:\Dev\KarstensWorkspace\_Sessions\_!AINewsResearch\_PROMPTS_AI-News-Research_TEMPLATE.md  Each run should get its own folder.

Then think hard what is needed to reach the goal. Use deep-research.md and write-template.md and other prompt system workflows

/write-strut for 1 AWH
````
