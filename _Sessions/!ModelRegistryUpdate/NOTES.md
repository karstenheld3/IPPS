# NOTES: Model Registry Update

**Doc ID**: MDLRGUP-NOTES

Permanent session for updating LLM model registry, pricing, and parameter mapping JSONs.

## Purpose

Fetch current model data from Anthropic and OpenAI provider websites, update canonical JSON files in `[DEVSYSTEM_FOLDER]/skills/llm-evaluation/`, and distribute to all target locations.

## Key Paths

- **Workflow Template**: `_PROMPTS_ModelInventoryUpdate_TEMPLATE.md` (replaces former `[WORKSPACE_FOLDER]/update-model-registry.md`)
- **Reusable Session Scripts**:
  - `match-epoch-eci.py` — Downloads Epoch ECI CSV and matches registry models to 5-point ECI bands, `UC-1..5`, and `Generation equivalent`
  - `update-model-inventory.py` — Regenerates `MODEL_INVENTORY.md` Sections 3.1 and 3.2: Label from `release_date` + `eci_band`, `Comp YY` (`--today`, wraps May 1), Efforts, WF from the band, prices; sorted by `1) Comp`, `2) Label year desc`, `3) Model`
  - `verify-and-distribute-registry.ps1` — Deterministic runner for Gates 1, 2, 5, 6, 7, 9, 9.4, `VerifyAll`, and Phase 9 distribution
- **Canonical JSONs**: `[DEVSYSTEM_FOLDER]/skills/llm-evaluation/`
  - `model-registry.json`
  - `model-pricing.json`
  - `model-parameter-mapping.json`
- **Artifacts**: This session folder (screenshots, DOM extracts, transcriptions)
- **Distribution targets**: `.devin/skills/llm-evaluation/`

## Current Phase

**[2026-10-29 14:30]** `DD-01` (b-variant), `DD-06..08` decided and applied: `model-registry.json` 1.11.0, `MODEL_INVENTORY.md` with ECI-band labels, `Comp 26` column, 92 + 4 rows, Gate 9.4 PASS. **P5 remainder gated on `DD-02..05`** (WF method, profile, Devin data, provider scope).
**[2026-10-28 20:22]** P1-P4 done (`60 / 60 min` net 1 AWH budget complete).
- **Plan**: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__STRUT_MDLINVNTRY.md [MDLRGUP-MDLINVNTRY-STRUT]` (`P1`, `P3`, `P4` `[x]`; `P2` waiting for `[ACTOR]` reply on `DD-01..05`; `P5` gated)
- **Research Summary & Decisions (`DD-01..05`)**: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\T02_MDLINVNTRY_ReliableModelInventory_2026-10-28\_INFO_MDLRGUP-MDLINVNTRY-01_Summary.md [MDLRGUP-MDLINVNTRY-IN01]` (Section 5)
- **Recurring Update Prompts Template (`P3-D1`)**: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_PROMPTS_ModelInventoryUpdate_TEMPLATE.md`
- **Completed Update Runs**:
  - **[2026-10-28 PRICES]**: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES` (23 models added across OpenAI, Anthropic, Google Gemini, Z.AI; 12 price/long-context updates; 90 models matched against Epoch ECI CSV; `model-registry.json` `1.10.1`, `model-pricing.json`, and `MODEL_INVENTORY.md` updated and mirrored to `.devin`; Gates 1-9.4 PASS)
- **Open items before/during P5**:
  1. `[ACTOR]` replies with `DD-02..05` decisions (format: `DD-02 c, DD-03 a, DD-04 a, DD-05 a`) → record in `## Key Decisions` below and check `P2-D1` in `__STRUT_MDLINVNTRY.md`
  2. Execute STRUT `P5` remainder (`P5-S2..S4`, `S7..S9`): apply `DD-02..05` to `PromptSystemV4.5/skills/write-documents/MODEL_INVENTORY.md`, `TASKS_GUIDES.md`, `PROMPTS_GUIDES.md`, `PROMPTS_RULES.md` (`PRMT-SC-05`), `write-prompts.md`, `edird-phase-planning/SKILL.md`, `llm-evaluation/model-registry.json`, `update-model-registry.md` (Phase 9.4 + Google source group `G1`-`G3` + redirected URLs `A1`/`A2`/`A3`/`O3`/`Z3`), and `LLMCAPCLS-IN01`, then mirror `PromptSystemV4.5` → `.devin` and commit

## Key Decisions

- **[2026-10-29 14:17] DD-01 = b-variant, DD-06 = 1, DD-07 = 1, DD-08 = A-Z** (user): `YY-L` kept; letter = Epoch ECI band against `anchor(YY) = 170 + 15 * (YY - 26)` (5 ECI per letter, A-Z); `Comp YY` column = same band against the comparison year (`year(today)` from May 1, else previous year); every text model not `retired` listed; one `WF` column (`2.0 * 2^(-(170 - band) / 10)`) plus `Efforts`. Former R2/R3/R5 removed. Details: `T02/NOTES.md` Key Decisions, `LLMCAPCLS-IN01` Sections 2-6
- `DD-02..05` still open (`DD-01..05 presented 2026-10-28 20:22`):
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

[2026-10-29 14:01] User reloaded the session with three `MODEL_INVENTORY.md` problems and asked for a proposal (no edits yet); T02 to be updated afterwards
````text
/session-load E:\dev\IPPS\_Sessions\!ModelRegistryUpdate

MODEL_INVENTORY.md L1-L153

Problems:

1. Not granular enough spread (for 2026 only B-E)
2. I'm missing older models like gpt-5-nano which are still operational
3. We need next to "Label" a column "Comp" (Comparison) which maps everything to the current year. Year wrapping in the "Comp" column should happen on 2026-05-01. The "Comp" column would only hold 26-* labels as of now.

Think hard what must be changed and propose edits

I also want this to be updated:
E:\dev\IPPS\_Sessions\!ModelRegistryUpdate\T02_MDLINVNTRY_ReliableModelInventory_2026-10-28
````

[2026-10-29 14:08] User added an in-house measured reference for model capability
````text
Here I have tested model capabilities. you can take this as a comparable reference:
e:\Dev\LLM-Research
````
Reference content: `e:\Dev\LLM-Research\_Sessions\_2026-03-05_TabularDataFormatsForLLMs\01_CSVScaleLimits\_INFO_01_CSVScaleLimits-TestResults.md [TBLF-IN02]` Section 5.1 (20 configurations, confirmed CSV extraction row limits per model and effort, May 2026) and `_INFO_02_CSVScaleLimits-Findings.md [TBLF-IN03]`

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
