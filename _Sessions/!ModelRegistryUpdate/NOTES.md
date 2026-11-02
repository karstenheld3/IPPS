# NOTES: Model Registry Update

**Doc ID**: MDLRGUP-NOTES

Permanent session for updating LLM model registry, pricing, and parameter mapping JSONs.

## Purpose

Fetch current model data from Anthropic and OpenAI provider websites, update canonical JSON files in `[PROMPTSYSTEM_FOLDER]/skills/llm-tools/`, and distribute to all target locations.

## Key Paths

- **Workflow Template**: `_PROMPTS_ModelInventoryUpdate_TEMPLATE.md` (replaces former `[WORKSPACE_FOLDER]/update-model-registry.md`)
- **Reusable Session Scripts**:
  - `match-epoch-eci.py` — Downloads Epoch ECI CSV and matches registry models to score and 95% interval; lists `unmatched`, `new_models` (from run DOM files), `missing_metadata`
  - `update-model-inventory.py` — Regenerates `MODEL_INVENTORY.md` Section 3.1 (Depth, Items, Context, Efforts, prices, Devin cost, Notes; sorted Depth desc, Model asc) and recomputes Section 3.2 Items and prices; `Top rung` line
  - `verify-and-distribute-registry.ps1` — Deterministic runner for Gates 1, 2, 5, 6, 7, 9, 9.4, `VerifyAll`, and Phase 9 distribution
  - `layer-depth-ladder.py` — Append-only depth layering (insert-only per run; `--bootstrap` used once on 2026-11-02); regression test `test-layer-depth-ladder.py` (8 cases, NFR-01)
  - `format-model-registry.py` — Re-serializes `model-registry.json` to the 1-line-per-entry layout (`--check` for verify-only). Run after every scripted registry write; never write the registry with `json.dump(indent=N)` or `ConvertTo-Json`
- **Canonical JSONs**: `[PROMPTSYSTEM_FOLDER]/skills/llm-tools/` (since 2026-10-29; was `skills/llm-evaluation/` with a replica in `skills/llm-transcription/`)
  - `model-registry.json`
  - `model-pricing.json`
  - `model-parameter-mapping.json`
- **Canonical MODEL_INVENTORY.md**: `[PROMPTSYSTEM_FOLDER]/skills/llm-tools/MODEL_INVENTORY.md` (since 2026-10-29; was `skills/write-documents/`)
- **Artifacts**: This session folder (screenshots, DOM extracts, transcriptions)
- **Distribution targets**: `.devin/skills/llm-tools/` (JSONs, `test-call-llm.py`, `MODEL_INVENTORY.md`); no other skill replicas exist

## Current Phase

**[2026-11-02 13:37]** Run prepared (Prompt 1 Bootstrap executed): `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-11-02_PRICES\_PROMPTS_2026-11-02_ModelInventoryUpdate.md` (06 prompts, `glm-5.2` high 1M, PRICES, LADDER, 5 providers, no screenshots); run cards in `_2026-11-02_PRICES\_agent_work\`. Next: execute Prompt 01 in a `glm-5.2` session, one prompt per turn.
**[2026-11-02 13:37]** `DD-13 1` (user) + `/go`: SP01 implemented (details: `T02/PROGRESS.md` Done 2026-11-02). Registry `1.12.0` with depth ladder (top D12, 92 models, 7 estimated), inventory regenerated, Gate 9.4 PASS, FR-12 consumers updated, mirrored to `.devin`. Next: commit, then Prompt 1 Bootstrap for `glm-5.2` (high, 1000k, PRICES).
**[2026-11-02 13:27]** Session reloaded to prepare a template run with `glm-5.2`. State found: `DD-10` option 3 (depth ladder), `DD-11`, `DD-12` decided; `_SPEC_MDLRGUP-MDLINVNTRY-01_DepthLadder.md [MDLRGUP-MDLINVNTRY-SP01]` written (T02, untracked); `_PROMPTS_ModelInventoryUpdate_TEMPLATE.md` rewritten to the ladder pipeline (v0 kept as `_PROMPTS_ModelInventoryUpdate_TEMPLATE_v0.md`). **Implementation not started**: `layer-depth-ladder.py` missing; `update-model-inventory.py`, `verify-and-distribute-registry.ps1` have no ladder code; `model-registry.json` still `1.11.0` (no `depth`, `eci_ci`, `deeper_than`); registry and 20 `llm-tools` files uncommitted (template Prompt 1 stops on uncommitted registry). Run preparation blocked; decision `DD-13` presented in chat.
**[2026-11-02 11:46]** Session reloaded. User rejects the ECI-band letter as capability metric (Opus 5.5 `26-A` above Fable 5 `26-B`; late-2026 models enter `A`). Request: propose 3 improvement options for a two-axis metric (reasoning depth, single-shot workload) that a prompt-writing agent can use to segment work and set prompt explicitness. Proposal presented in chat as `DD-09`; no files changed. Supersedes the open `DD-02..05` framing if accepted.
**[2026-10-29 15:40]** Skill merge (session `_2026-10-29_UnifyLlmToolsSkill`, `LLMTOOLS-IN01`): `llm-evaluation`, `llm-transcription`, `llm-computer-use` became `skills/llm-tools/`. Canonical JSONs and `MODEL_INVENTORY.md` now in `llm-tools/` root; `update-model-inventory.py` (paths, heading `### 3.1 API Models (llm-tools registry)`) and `verify-and-distribute-registry.ps1` (Distribute + Gate 9 targets) updated; `_PROMPTS_ModelInventoryUpdate_TEMPLATE.md` placeholders `[SKILL_FOLDER]`, `[INVENTORY_FILE]`, `[TRANSCRIPTION_SCRIPT]` and Prompt 9 paths updated. Next run must pass `-SkillFolder [PROMPTSYSTEM_FOLDER]\skills\llm-tools -InventoryFile [PROMPTSYSTEM_FOLDER]\skills\llm-tools\MODEL_INVENTORY.md`.
**[2026-10-29 14:50]** Fixed `model-registry.json` layout regression: commit `e6139f1` (14:36, v1.11.0 capability-label pass) rewrote the registry with an indented `json.dump`, expanding 118 lines to 2836 (one key per line). Root cause: a since-deleted `.tmp_` script used `indent=2`. Restored via new `format-model-registry.py` (100 models, 53 prefixes, 164 lines; data round-trip identical), mirrored to `.devin`, hashes equal. Template Prompts 5 and 6 now call the formatter after registry writes.
**[2026-10-29 14:37]** xAI/Grok provider integration completed across pipeline: `model-registry.json` (8 Grok models + 12 prefixes), `model-pricing.json` (xAI pricing section), all 5 Python scripts (`call-llm.py`, `call-llm-batch.py`, `find-workers-limit.py`, `analyze-costs.py`, `test-call-llm.py`), and `_PROMPTS_ModelInventoryUpdate_TEMPLATE.md` (X1-X3 extraction steps, example section). Fixed batch dispatch bug where Google/xAI fell through to Anthropic branch. Z.AI tests 7/7 PASSED; Google 5/8 (gemini-3.8-flash timeouts); xAI untested (no `XAI_API_KEY`).
**[2026-10-29 14:30]** `DD-01` (b-variant), `DD-06..08` decided and applied: `model-registry.json` 1.11.0, `MODEL_INVENTORY.md` with ECI-band labels, `Comp 26` column, 92 + 4 rows, Gate 9.4 PASS. **P5 remainder gated on `DD-02..05`** (WF method, profile, Devin data, provider scope).
**[2026-10-28 20:22]** P1-P4 done (`60 / 60 min` net 1 AWH budget complete).
- **Plan**: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__STRUT_MDLINVNTRY.md [MDLRGUP-MDLINVNTRY-STRUT]` (`P1`, `P3`, `P4` `[x]`; `P2` waiting for `[ACTOR]` reply on `DD-01..05`; `P5` gated)
- **Research Summary & Decisions (`DD-01..05`)**: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\T02_MDLINVNTRY_ReliableModelInventory_2026-10-28\_INFO_MDLRGUP-MDLINVNTRY-01_Summary.md [MDLRGUP-MDLINVNTRY-IN01]` (Section 5)
- **Recurring Update Prompts Template (`P3-D1`)**: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_PROMPTS_ModelInventoryUpdate_TEMPLATE.md`
- **Completed Update Runs**:
  - **[2026-10-28 PRICES]**: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES` (23 models added across OpenAI, Anthropic, Google Gemini, Z.AI; 12 price/long-context updates; 90 models matched against Epoch ECI CSV; `model-registry.json` `1.10.1`, `model-pricing.json`, and `MODEL_INVENTORY.md` updated and mirrored to `.devin`; Gates 1-9.4 PASS)
- **Open items** (2026-11-02): `DD-04` (Devin data in inventory) and `DD-05` (provider scope) undecided, current state unchanged; EC-4 citations for specialized Apex models pending (see `T02/PROGRESS.md` To Do)

## Key Decisions

- **[2026-11-02 13:37] DD-13 = 1** (user): implement the depth ladder (SP01) before the first ladder run; run executes with `glm-5.2` (high, 1000k)
- **[2026-11-02] DD-10 = option 3** (user): capability as append-only ordinal depth ladder `D1`, `D2`, ... with evidence kinds E1-E6, plus measured Items axis; replaces year-letter labels, ECI bands, Comp, WF, behavior profiles. Supersedes `DD-01`; absorbs `DD-02`, `DD-03` (`LLMCAPCLS-IN01` lines 16, 341)
- **[2026-11-02] DD-11 closed**: `claude-fable-5` and `claude-fable-5-1` recorded above `claude-opus-5-5` from Anthropic model-selection guidance; ladder top `D12` (`LLMCAPCLS-IN01` line 385)
- **[2026-11-02] DD-12 approved**: `MDLRGUP-MDLINVNTRY-SP01` carries `LLMCAPCLS-IN01` Sections 2, 4, 5 as requirements; `/write-impl-plan` follows (`LLMCAPCLS-IN01` line 386)
- **[2026-10-29 14:17] DD-01 = b-variant, DD-06 = 1, DD-07 = 1, DD-08 = A-Z** (user): `YY-L` kept; letter = Epoch ECI band against `anchor(YY) = 170 + 15 * (YY - 26)` (5 ECI per letter, A-Z); `Comp YY` column = same band against the comparison year (`year(today)` from May 1, else previous year); every text model not `retired` listed; one `WF` column (`2.0 * 2^(-(170 - band) / 10)`) plus `Efforts`. Former R2/R3/R5 removed. Details: `T02/NOTES.md` Key Decisions, `LLMCAPCLS-IN01` Sections 2-6
- `DD-02`, `DD-03` absorbed by `DD-10`; `DD-04`, `DD-05` still open (`DD-01..05 presented 2026-10-28 20:22`):
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

[2026-11-02 11:46] User reloaded the session, rejected the ECI-band capability metric, and asked for 3 improvement options (propose only)
````text
/session-load E:\dev\IPPS\_Sessions\!ModelRegistryUpdate

In the last session output we have many problems:

MODEL_INVENTORY.md L1-L205

E:\dev\IPPS\_Sessions\!ModelRegistryUpdate

I think the benchmark we use is not accurate.

Example:
Claude Opus 5.5 does not think as deep as claude fable 5. Why is it then ranked above Fable 5?

Weaker models that are released after September now jump into the "A" tier, leaving older but stronger models behind.

What we want is a combined metric for reasoning depth and for single-shot workload completion. So 2 questions:
- How deep can a model understand a task? For example Opus models can understand problems way deeper than Sonnet models,
- How many tasks in a single prompt can a model keep in mind and finish with reliable accuracy?

Think hard, read verything we have and then propose changes.

The goal is to have a reliable tool (model inventory) for a prompt writing agent to assess and partition work into promot series. If a target model cant understand a problem as deep as another target model, the work must be segmented in smaller parts to achieve the same reasoning depth. Also the prompts must be written more explicitly because the target model will maybe not infer all implicitly available information from the prompt. At the same time, overwhelming the target model with too much detail might also be a problem.

So how to navigate this problem space?

Think really hard and propose 3 improvement options.
````

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
