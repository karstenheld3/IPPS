<PromptSystem MarkdownTablesAllowed=true />

# INFO: Candidate Methods for Deriving Work-per-Prompt

**Doc ID**: MDLRGUP-MDLINVNTRY-IN05
**Goal**: Score and compare five candidate methods for sizing agentic prompts (`work per prompt`) against sourced evidence, coverage, token overhead, general-purpose portability, and empirical calibratability
**Timeline**: Created 2026-10-28, Updated 0 times
**Version scope**: 2026-10-28

**Depends on:**
- `_INFO_MDLRGUP-MDLINVNTRY-02_Sources.md [MDLRGUP-MDLINVNTRY-IN02]` for source IDs and URL verification
- `_INFO_MDLRGUP-MDLINVNTRY-03_InventoryAudit.md [MDLRGUP-MDLINVNTRY-IN03]` for assumption density and token counts across audited files
- `_INFO_MDLRGUP-MDLINVNTRY-04_SourcesPerField.md [MDLRGUP-MDLINVNTRY-IN04]` for per-field source coverage (`Epoch ECI 28/28`, `METR 6/28 exact`)

## Summary

- **No public benchmark measures Human Work Hours (HWH) completed per single prompt without item drop-out**: [Epoch Capabilities Index (ECI)](https://epoch.ai/eci) measures cross-benchmark capability via Item Response Theory (IRT) across 270 models (`28/28` inventory coverage), whereas [Model Evaluation and Threat Research (METR) Time Horizons](https://metr.org/time-horizons/) measures multi-step autonomous task completion duration (`6/28` exact coverage, `7/28` with family prefix) and stopped updating on `2026-09-08` `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-EPOCH-ECI | https://epoch.ai/eci)` `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-METR-TMHOR | https://metr.org/time-horizons/)`.
- **Because converting any capability index or task bucket into HWH-per-prompt requires at least one unmeasured anchor or threshold, no candidate option scores `3/3` on `Sourced`**: Under the strict rule that `3/3` requires every numeric parameter to have a primary URL, the ceiling on `Sourced` is `2/3` `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-LOCAL-LLMCAP | e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_INFO_HOW_TO_ORGANIZE_LLMS_BY_CAPABILITY.md)`.
- **Empirical production evidence contradicts the `YY-L` formula's `8x` capacity gap (`WF 2.0` vs `WF 0.25`)**: In both the `AINWSRCH` production pipeline (`~90k` token prompts completing 58-69 sources without skipped items) and the current `MDLINVNTRY` prompt sequence (`7/7` prompts completed `100%` of planned items, `4-12` items and `2-9` files per prompt in `3-9` minutes), `glm-5.2` at high effort executes `0.5-1.0 HWH` prompts reliably when given a strict scope guard `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-KWRK-TMPLTE | e:\Dev\KarstensWorkspace\_Sessions\_!AINewsResearch\_PROMPTS_AI-News-Research_TEMPLATE.md)` `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-IPPS-FAILS | e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Findings.md)`.
- **Five options were evaluated on a 0-15 scale (`Sourced`, `Coverage`, `Tokens`, `General purpose`, `Calibratable`)**: **Option c (Model-agnostic fixed limits without Workload Factor (WF))** scores highest at **13/15**, followed by **Option a (ECI band to HWH table)** at **12/15**, **Option e (Universal Class (UC) UC-1..5 to HWH table)** at **10/15**, **Option b (METR 80% horizon + fallback)** at **7/15**, and **Option d (Keep `YY-L` formula)** at **6/15** `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-IPPS-MDLINV | e:\dev\IPPS\PromptSystemV4.5\skills\write-documents\MODEL_INVENTORY.md)`.
- **Recommendation depends on whether `DD-02` prioritizes maximum leanness (Goal 3) or model-differentiated sizing (Goal 1)**: Option c (`13/15`) is recommended if eliminating unmeasured WF numbers and cutting ~80 lines of rules is prioritized; Option a (`12/15`) is the recommended runner-up if model-aware HWH scaling is retained using `28/28` sourced ECI bands `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-EPOCH-ECI | https://epoch.ai/eci)`.

## Table of Contents

- [Summary](#summary)
1. [Scoring Methodology and Empirical Baseline](#1-scoring-methodology-and-empirical-baseline)
2. [Option a: ECI Band to HWH Table](#2-option-a-eci-band-to-hwh-table)
3. [Option b: METR 80% Horizon + Fallback](#3-option-b-metr-80-horizon--fallback)
4. [Option c: Model-Agnostic Fixed Limits without WF](#4-option-c-model-agnostic-fixed-limits-without-wf)
5. [Option d: Keep YY-L Formula](#5-option-d-keep-yy-l-formula)
6. [Option e: UC-1..5 to HWH Table](#6-option-e-uc-15-to-hwh-table)
7. [Comparison Table and Recommendation](#7-comparison-table-and-recommendation)
8. [Worked Example: 3 HWH Task on glm-5.2 High and claude-opus-5 High](#8-worked-example-3-hwh-task-on-glm-52-high-and-claude-opus-5-high)
9. [Limitations and Known Issues](#9-limitations-and-known-issues)
- [Sources](#sources)
- [Document History](#document-history)

## 1. Scoring Methodology and Empirical Baseline

Each option is scored `0` to `3` across five criteria (maximum `15` points):
- **Sourced (0-3)**: `0` = invented formula/labels; `1` = mostly assumed with sparse benchmark anchors; `2` = primary inputs sourced from URLs or provider docs, with at most one explicit planning heuristic (`[ASSUMED]`); `3` = every numeric value has an authoritative external URL (no option achieves `3` because no external benchmark measures single-prompt HWH capacity).
- **Coverage (0-3)**: Share of the 28 API models in `MODEL_INVENTORY.md` Section 3.1 covered without manual judgment (`0` = `<25%`, `1` = `25-59%`, `2` = `60-89%`, `3` = `90-100%`).
- **Tokens (0-3)**: Token and line economy in `MODEL_INVENTORY.md`, `TASKS_GUIDES.md`, `PROMPTS_GUIDES.md`, and `PROMPTS_RULES.md` (`0` = `>100` lines of rules/tables, `1` = `60-100` lines, `2` = `25-59` lines, `3` = `<25` lines).
- **General purpose (0-3)**: Usability in any agentic environment (Devin/Cascade, Claude Code, OpenAI Codex CLI, Cursor, custom CLI) without environment-specific registries or yearly manual calendar rules (`0` = tied to one IDE, `1` = requires manual yearly re-grading, `2` = portable with minor lookup conventions, `3` = works identically everywhere).
- **Calibratable (0-3)**: Ability to calibrate from `Partition Observations` (`items_planned`, `items_done`, `files_touched`, `minutes`) without circular parameters (`0` = uncalibratable/frozen, `1` = requires multi-parameter refit, `2` = 4-6 discrete bands/classes, `3` = 1-3 global operational limits).

- **Key Facts (Empirical Baseline)**:
  - **Audit baseline (`MDLRGUP-MDLINVNTRY-IN03`)**: Across `MODEL_INVENTORY.md` (127 lines, 2151 words), `TASKS_GUIDES.md` (60 lines, 633 words), `PROMPTS_GUIDES.md` Sections 1c/1f/1g/3a/5 (115 lines, 1685 words), and `PROMPTS_RULES.md` `PRMT-SC-05` (13 lines, 248 words), `37/82` classified items (45%) are `ASSUMED` and `20/27` `DERIVED` items depend on `ASSUMED` inputs `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-IPPS-MDLINV | e:\dev\IPPS\PromptSystemV4.5\skills\write-documents\MODEL_INVENTORY.md)`.
  - **Production evidence (`AINWSRCH` template)**: `glm-5.2` at high effort runs prompts of `~90k` tokens (Prompt 2: 58-69 sources verified) and `~165k` tokens across 4 prompts (Session A) without skipping items `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-KWRK-TMPLTE | e:\Dev\KarstensWorkspace\_Sessions\_!AINewsResearch\_PROMPTS_AI-News-Research_TEMPLATE.md)`.
  - **In-session Partition Observations (`__CARD_MDLINVNTRY-Findings.md`)**: Across 7 executed prompts on `glm-5.2` high (`01-MdlInv-Audit[01..05]` and `02-MdlInv-Sources[01..02]`), `items_planned` ranged from `4` to `12`, `items_done` matched `100%` (`not_done: none` on all 7 prompts), `files_touched` ranged from `2` to `9`, and net working time ranged from `3` to `9` minutes per prompt `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-IPPS-FAILS | e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Findings.md)`.

## 2. Option a: ECI Band to HWH Table

- **What**: Replace `YY-L` and the WF formula with a 4-tier lookup table mapping 5-point [Epoch ECI](https://epoch.ai/eci) bands directly to `WF_high` (HWH per prompt at High effort): `E165-E170` (`>=162.5`) → `2.0 HWH`, `E155-E160` (`152.5-162.4`) → `1.0 HWH`, `E145-E150` (`142.5-152.4`) → `0.5 HWH`, `<=E140` (`<142.5`) → `0.25 HWH` (`[ASSUMED]` anchor `E155-E160 = 1.0 HWH`, `[SOURCED]` ECI scores and Epoch's finding that ~5-10 ECI points correspond to capability doubling). Effort multipliers are simplified to Low `0.5x`, Medium `0.75x`, High/XHigh/Max `1.0x` (or High only).
- **Evidence for**:
  - Covers `28/28` (100%) of `MODEL_INVENTORY.md` Section 3.1 models from a single machine-readable CSV (`eci-leaderboard-general.csv`) `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-EPOCH-ECI | https://epoch.ai/eci)`.
  - Aligns with the existing `AINWSRCH` 4-field model tier record (`Vendor generation`, `UC-1..5`, `ECI band`, `Generation equivalent`), eliminating duplicate tiering schemes (MECT) `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-KWRK-MODTIR | e:\Dev\KarstensWorkspace\_Sessions\_!AINewsResearch\_INFO_AINWSRCH-MODELTIER-01_GenerationTiering.md)`.
  - Places `glm-5.3` (`155.99`, `E155`) and `glm-5.3-flash` (`153.08`, `E155`) at `1.0 HWH` and `glm-5.2` (`151.94`, `E150`) at `0.5 HWH` (`6` prompts for a `3 HWH` task instead of `12`), matching observed session throughput `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-EPOCH-ECI | https://epoch.ai/eci)`.
- **Evidence against**:
  - The mapping from an ECI band (`E155-E160`) to `1.0 HWH` per prompt is still `[ASSUMED]`; ECI aggregates 60 static benchmarks rather than measuring multi-file instruction drop-out `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-KWRK-MODTIR | e:\Dev\KarstensWorkspace\_Sessions\_!AINewsResearch\_INFO_AINWSRCH-MODELTIER-01_GenerationTiering.md)`.
  - Newly released models require `>=4` evaluated benchmarks before appearing in Epoch's CSV (`claude-mythos-5` is absent from ECI CSV despite appearing in METR), requiring a temporary UC-based fallback on release day `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-EPOCH-ECI | https://epoch.ai/eci)`.
- **Score**: **12 / 15** — `Sourced: 2/3`, `Coverage: 3/3`, `Tokens: 2/3`, `General purpose: 3/3`, `Calibratable: 2/3`.
- **Self-critique**: Scoring Option a at `12/15` could overstate `Sourced` (`2/3`) and `Coverage` (`3/3`) if Epoch ECI lags by 1-3 weeks after a major model launch or if static benchmark capability diverges from agentic instruction compliance. Specifically, `glm-5.2` (`ECI 151.94`) and `claude-opus-4-5` (`ECI 150.11`) sit in the same `E150` band (`1.8` points apart), yet `glm-5.2` exhibits higher scope inflation (`OverAct SIR 2.00`) without a strict scope guard `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-LOCAL-COVMTX | e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\T01_MDLBHVPRM_BehavioralParameterBenchmarks_2026-10-19\_INFO_MDLBHVPRM-05_CoverageMatrix.md)`.

## 3. Option b: METR 80% Horizon + Fallback

- **What**: Set each model's `WF_high` directly equal to its [METR](https://metr.org/time-horizons/) `p80_horizon_length` converted from minutes to hours (`claude-opus-4-6 = 1.16 HWH`, `gpt-5.2 = 1.10 HWH`, `gpt-5.4 = 0.90 HWH`, `claude-opus-4-5 = 0.82 HWH`, `gpt-5.1 = 0.84 HWH`, `gpt-5 = 0.64 HWH`, `o3 = 0.50 HWH`), with a fallback formula or ECI/UC table for the remaining `21/28` models not in METR.
- **Evidence for**:
  - METR `p80_horizon_length` is the only external benchmark whose unit is literally **human expert completion hours** at an 80% success rate, matching the conceptual unit of HWH `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-METR-TMHOR | https://metr.org/time-horizons/)`.
  - For the 7 covered models, METR's `p80` values (`0.50` to `1.16` hours) fall squarely in the `0.5-1.5 HWH` range used in practical prompt partitioning `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-METR-TMHOR | https://metr.org/time-horizons/)`.
- **Evidence against**:
  - Covers only `6/28` (21%) exact or `7/28` (25%) with family prefix (`0/5` Z.AI models and `0` mid/late-2026 flagships: `gpt-6-astra`, `gpt-5.6-*`, `gpt-5.5`, `claude-fable-5`, `claude-opus-5`, `claude-sonnet-5`, `claude-opus-4-8/4-7`), so **75-79% of the inventory runs on the fallback** `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-METR-TMHOR | https://metr.org/time-horizons/)`.
  - The METR Time Horizons page displays the banner `"This page is no longer actively updated. LAST UPDATED September 8, 2026"`, making it a frozen source for recurring updates `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-METR-TMHOR | https://metr.org/time-horizons/)`.
  - Maintaining both a METR lookup and a fallback scheme for 75% of models increases rule complexity rather than reducing it (violates Goal 3) `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-IPPS-MDLINV | e:\dev\IPPS\PromptSystemV4.5\skills\write-documents\MODEL_INVENTORY.md)`.
- **Score**: **7 / 15** — `Sourced: 2/3`, `Coverage: 1/3`, `Tokens: 1/3`, `General purpose: 2/3`, `Calibratable: 1/3`.
- **Self-critique**: Scoring Option b at `7/15` treats METR's `2026-09-08` freeze as permanent; if METR releases a v1.2/v2.0 suite covering late-2026 models, `Coverage` would rise from `1/3` to `2/3`. Even before the freeze, however, METR never evaluated Z.AI (`glm-*`) or mini/flash tiers (`haiku`, `mini`, `luna`), and its 2x confidence intervals (`claude-opus-4-6` `p80` `0.53-2.18 hr`) mean raw `p80` decimals (`1.16` vs `0.90`) create false precision `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-METR-TMHOR | https://metr.org/time-horizons/)`.

## 4. Option c: Model-Agnostic Fixed Limits without WF

- **What**: Drop `WF`, `WF_high`, per-effort WF columns (`Low/Medium/High/XHigh/Max`), `USD per WF 1`, and the `prompt_count = ceil(task_HWH / WF)` formula from `MODEL_INVENTORY.md`, `TASKS_GUIDES.md`, `PROMPTS_GUIDES.md`, and `PROMPTS_RULES.md`. Size every prompt by model-agnostic operational caps in `PROMPTS_GUIDES.md`: `<= 1.0 HWH`, `<= 6` instruction items, `<= 3` files modified, `<= 1` heavy workflow, input read `<= 50%` of the model's sourced `context_window`, and checkpoint every `2-3` prompts (or every `1-2` prompts plus strict scope guard when a model has a documented observation in `MODEL_INVENTORY.md` `Notes`, such as `glm-5.2`) (`[ASSUMED]` operational caps, `[SOURCED]` context window, max output, effort support, and per-1M-token prices).
- **Evidence for**:
  - Eliminates all **26 `ASSUMED` items in `MODEL_INVENTORY.md`** (`MDLRGUP-MDLINVNTRY-IN03`), cutting `MODEL_INVENTORY.md` from 127 lines to `<55` lines (Goal 3) and keeping only `100%` sourced facts (`Model`, `UC`, `ECI band`, `Context`, `Max output`, `Effort levels`, `Input/Cached/Output USD per 1M`, `Notes`) `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-IPPS-MDLINV | e:\dev\IPPS\PromptSystemV4.5\skills\write-documents\MODEL_INVENTORY.md)`.
  - Matches how `edird-phase-planning` (`SKILL.md` `>30 min AWH = decompose`), `AINWSRCH` (`_PROMPTS_AI-News-Research_TEMPLATE.md`), and the compressed `_PROMPTS_02-MdlInv-Sources.md` (`3` prompts of `4-6` items each) actually partition work in practice `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-KWRK-TMPLTE | e:\Dev\KarstensWorkspace\_Sessions\_!AINewsResearch\_PROMPTS_AI-News-Research_TEMPLATE.md)` `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-IPPS-FAILS | e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Findings.md)`.
  - In `LLMCAPCLS-IN01` Section 9.3's own worked example for `claude-opus-5` (`3 HWH`, `18` items, `7` files), `ceil(total_items / max_items) = ceil(18/6) = 3` and `ceil(total_files / max_files) = ceil(7/3) = 3` already dominate `ceil(3 / 2.0) = 2`; WF only changed the prompt count on `glm-5.2` by inflating it to `12` prompts (`ceil(3 / 0.25)`), which the user compressed from `13` prompts down to `5` in this session without any skipped items `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-LOCAL-LLMCAP | e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_INFO_HOW_TO_ORGANIZE_LLMS_BY_CAPABILITY.md)` `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-IPPS-FAILS | e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Findings.md)`.
  - Works on day zero for every new or unbenchmarked model (`28/28` API models plus any new release) in any agent environment (Goal 2) `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-IPPS-MREG | e:\dev\IPPS\PromptSystemV4.5\skills\llm-evaluation\model-registry.json)`.
- **Evidence against**:
  - Does not automatically scale prompt count when switching from a frontier flagship (`claude-opus-5`, `E165`) to a small model (`claude-haiku-4-5`, `E140`, or `gpt-4.1`, `E135`); the author must rely on `Notes` or `UC`/`ECI` inspection when targeting a `UC-4` model `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-EPOCH-ECI | https://epoch.ai/eci)`.
  - Still uses three `[ASSUMED]` global heuristics (`<= 1.0 HWH`, `<= 6` items, `<= 3` files), though these are stated once in `PROMPTS_GUIDES.md` rather than multiplied into 140 per-model-per-effort table cells `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-IPPS-PRMGD | e:\dev\IPPS\PromptSystemV4.5\skills\write-documents\PROMPTS_GUIDES.md)`.
- **Score**: **13 / 15** — `Sourced: 2/3`, `Coverage: 3/3`, `Tokens: 3/3`, `General purpose: 3/3`, `Calibratable: 2/3`.
- **Self-critique**: Option c scores `13/15` because it treats model-specific HWH scaling as unnecessary overhead on top of item/file/context caps. That assumption holds when prompts are executed by `UC-1..3` models at High effort (`E150-E170`, including `glm-5.2` high and `claude-opus-5` high), where `6` items and `3` files per prompt are the binding constraint. It could fail if `/write-prompts` is regularly used to generate long autonomous chains for `UC-4`/`E135-E140` models (`gpt-4.1`, `claude-haiku-4-5`) at Low/Medium effort, where `6` items per prompt may exceed instruction-following reliability without a tier adjustment `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-LOCAL-PARTTN | e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\T01_MDLBHVPRM_BehavioralParameterBenchmarks_2026-10-19\_INFO_MDLBHVPRM-06_ModelAwarePartitioning.md)`.

## 5. Option d: Keep YY-L Formula

- **What**: Retain the current `MODEL_INVENTORY.md` Section 2 system: capability labels `YY-L` (`25-A`..`26-D`), formula `WF_high = 2.0 * 0.5^letter_index * 2^(YY - 26)`, rules `R1`-`R5` (including `R3` October cap/promotion review), effort multipliers (`0.25x` to `2.0x`), and behavior profiles (`precise`/`standard`/`guarded`) `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-IPPS-MDLINV | e:\dev\IPPS\PromptSystemV4.5\skills\write-documents\MODEL_INVENTORY.md)`.
- **Evidence for**:
  - Already implemented across `MODEL_INVENTORY.md`, `TASKS_GUIDES.md`, `PROMPTS_GUIDES.md` Section 1g, `PROMPTS_RULES.md` `PRMT-SC-05`, and `model-registry.json` (`28/28` models labeled) on `2026-10-28` (`__TASKS_LLMCAPCLS.md`) `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-IPPS-MDLINV | e:\dev\IPPS\PromptSystemV4.5\skills\write-documents\MODEL_INVENTORY.md)`.
  - Encodes cross-year progress (`26-B = 25-A = 1.0 HWH`) and effort scaling in a single algebraic expression `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-LOCAL-LLMCAP | e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_INFO_HOW_TO_ORGANIZE_LLMS_BY_CAPABILITY.md)`.
- **Evidence against**:
  - **Circular and unmeasured (`Sourced: 0/3`)**: `LLMCAPCLS-IN01` Section 6 explicitly admits that `YY-L` labels were chosen to reproduce the previous unmeasured table (`35/37` rows identical); `26/44` classified items in `MODEL_INVENTORY.md` (59%) are `ASSUMED` `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-LOCAL-LLMCAP | e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_INFO_HOW_TO_ORGANIZE_LLMS_BY_CAPABILITY.md)`.
  - **Empirically falsified on `glm-5.2`**: Assigns `glm-5.2` `26-D` (`WF_high = 0.25 HWH`), forcing `12` prompts for a `3 HWH` task, whereas `glm-5.2` high completes `4-12` items and `~0.5-1.0 HWH` per prompt with `0` skipped items when given a strict scope guard `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-IPPS-FAILS | e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Findings.md)`.
  - **Violates Goal 3 (lean) and MECT**: Requires manual yearly October re-grading (`R3`), duplicates the `AINWSRCH` tier design (`UC + ECI band`), and maintains 27/28 identical `standard` profile rows because `IFEval-Hard` coverage is `0/28` and `OverAct` coverage is `1/28` `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-LOCAL-COVMTX | e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\T01_MDLBHVPRM_BehavioralParameterBenchmarks_2026-10-19\_INFO_MDLBHVPRM-05_CoverageMatrix.md)`.
- **Score**: **6 / 15** — `Sourced: 0/3`, `Coverage: 3/3`, `Tokens: 0/3`, `General purpose: 2/3`, `Calibratable: 1/3`.
- **Self-critique**: Scoring Option d at `6/15` heavily penalizes its circular derivation (`Sourced: 0/3`) and rule bloat (`Tokens: 0/3`). One could argue that because `YY-L` is already written into the files, keeping it has zero migration cost in `P5`, and that `R4` (observation downgrade) could eventually calibrate labels if `partition-observations.jsonl` were built. However, keeping 26 `ASSUMED` rules and a 12-prompt penalty on `glm-5.2` directly violates the user's primary prompt (`"MODEL_INVENTORY.md is full of unreliable information and assumptions"`, Goal 3) `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-IPPS-MDLINV | e:\dev\IPPS\PromptSystemV4.5\skills\write-documents\MODEL_INVENTORY.md)`.

## 6. Option e: UC-1..5 to HWH Table

- **What**: Map each model's **Universal Class (`UC-1..5`)** from the `AINWSRCH` tier record (`UC-1 Apex`, `UC-2 Flagship`, `UC-3 Balanced`, `UC-4 Efficient`, `UC-5 Edge`, derived from vendor lineup role and price order) to a fixed `WF_high` table: `UC-1 / UC-2 → 1.5 HWH` (or `UC-1 → 2.0`, `UC-2 → 1.0`), `UC-3 → 0.75 HWH` (or `0.5`), `UC-4 → 0.25 HWH` (`[SOURCED]` vendor lineup class from provider docs/pricing, `[ASSUMED]` HWH per class).
- **Evidence for**:
  - `UC-1..5` is `100%` determinable on release day (`28/28` coverage) directly from provider documentation and pricing tables (`model-pricing.json`), with zero dependency on external benchmark lag `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-KWRK-MODTIR | e:\Dev\KarstensWorkspace\_Sessions\_!AINewsResearch\_INFO_AINWSRCH-MODELTIER-01_GenerationTiering.md)`.
  - Reuses field 2 of the `AINWSRCH` tier record (`UC-1..5`), never changes after release, and requires no October calendar rule `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-KWRK-ANTIER | e:\Dev\KarstensWorkspace\_Sessions\_!AINewsResearch\NOTES.md)`.
- **Evidence against**:
  - **Conflates vendor lineup role with absolute capability across generations and vendors**: `AINWSRCH-MODELTIER-IN01` explicitly designed `UC-1..5` to show *vendor lineup role*, not cross-year or cross-vendor capability `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-KWRK-MODTIR | e:\Dev\KarstensWorkspace\_Sessions\_!AINewsResearch\_INFO_AINWSRCH-MODELTIER-01_GenerationTiering.md)`.
  - Under `UC → HWH`, a 2025 `UC-2` model (`gpt-4.1`, `ECI 136.65`, `E135`) receives the same HWH as a late-2026 `UC-2` model (`claude-opus-5`, `ECI 163.94`, `E165`), while a 2026 `UC-3` model (`claude-sonnet-5`, `ECI 156.88`, `E155`) is rated below `gpt-4.1` despite outscoring it by `20.2` ECI points `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-EPOCH-ECI | https://epoch.ai/eci)`.
- **Score**: **10 / 15** — `Sourced: 1/3`, `Coverage: 3/3`, `Tokens: 2/3`, `General purpose: 3/3`, `Calibratable: 1/3`.
- **Self-critique**: Option e's score (`10/15`) penalizes `Sourced` (`1/3`) and `Calibratable` (`1/3`) because `UC` ignores generational capability gains (`gpt-4.1` vs `claude-opus-5`). If the inventory pruned all pre-2026 legacy models (`gpt-4.1`, `o3`, `claude-*-4-5`, `gpt-5/5.1/5.2`), within-year `UC-1..4` would correlate more closely with ECI (`E165` vs `E155` vs `E150`). Even within 2026, however, `glm-5.3` (`UC-2`, `ECI 155.99`) and `claude-opus-5` (`UC-2`, `ECI 163.94`) differ by `8` ECI points (`~2.5x` METR horizon equivalent), which `UC` alone cannot distinguish `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-EPOCH-ECI | https://epoch.ai/eci)`.

## 7. Comparison Table and Recommendation

| Option                                     | Sourced (0-3) | Coverage (0-3) | Tokens (0-3) | General purpose (0-3) | Calibratable (0-3) | Total (0-15) |
|--------------------------------------------|---------------|----------------|--------------|-----------------------|--------------------|--------------|
| c) Model-agnostic fixed limits (no WF)     | 2             | 3              | 3            | 3                     | 2                  | 13           |
| a) ECI band to HWH table                   | 2             | 3              | 2            | 3                     | 2                  | 12           |
| e) UC-1..5 to HWH table                    | 1             | 3              | 2            | 3                     | 1                  | 10           |
| b) METR 80% horizon + fallback             | 2             | 1              | 1            | 2                     | 1                  | 7            |
| d) Keep YY-L formula                       | 0             | 3              | 0            | 2                     | 1                  | 6            |

- **Primary Recommendation (`Option c`, 13/15 — Lean / Zero-WF)**: Adopt **Option c** for `DD-02` if Goal 3 (lean files, `<60` lines in `MODEL_INVENTORY.md`, zero invented WF numbers) is primary. Keep `UC` + `ECI band` in `MODEL_INVENTORY.md` as descriptive capability evidence (`DD-01 Option a`), drop `WF` and per-effort WF columns, and partition prompts in `PROMPTS_GUIDES.md` using a single set of operational limits (`<= 1.0 HWH`, `<= 6` items, `<= 3` files, `<= 50%` context window, plus strict scope guard and 1-2 prompt checkpoint interval when `Notes` records over-eagerness/skipping) `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-IPPS-MDLINV | e:\dev\IPPS\PromptSystemV4.5\skills\write-documents\MODEL_INVENTORY.md)`.
- **Close Runner-Up (`Option a`, 12/15 — Sourced ECI-Band WF)**: Adopt **Option a** for `DD-02` if [ACTOR] wants `prompt_count` to scale automatically with model capability (`ceil(task_HWH / WF)`). Map the 4 ECI band groups (`E165+ → 2.0`, `E155-E160 → 1.0`, `E145-E150 → 0.5`, `<=E140 → 0.25 HWH`, with `UC` fallback for brand-new models not yet in Epoch CSV) in a 5-line lookup table in `PROMPTS_GUIDES.md` instead of `MODEL_INVENTORY.md` `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-EPOCH-ECI | https://epoch.ai/eci)`.

## 8. Worked Example: 3 HWH Task on glm-5.2 High and claude-opus-5 High

**Benchmark task (from `LLMCAPCLS-IN01` Section 9.3)**: `3 HWH` total work, `18` numbered instruction items, `7` files touched, run at **High** effort `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-LOCAL-LLMCAP | e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_INFO_HOW_TO_ORGANIZE_LLMS_BY_CAPABILITY.md)`:
- **`claude-opus-5` High**: `UC-2 Flagship`, `ECI 163.94` (`E165`), `Context 1000K`, `Max output 128K`, no adverse `Notes`.
- **`glm-5.2` High**: `UC-2 Flagship`, `ECI 151.94` (`E150`), `Context 200K`, `Max output 16K`, `Notes`: documented over-eagerness (`OverAct SIR 2.00`) and item skipping without strict scope guard.

| Option                                     | claude-opus-5 High calculation                              | claude-opus-5 prompts | glm-5.2 High calculation                                    | glm-5.2 prompts | Notes on glm-5.2 result                                             |
|--------------------------------------------|-------------------------------------------------------------|-----------------------|-------------------------------------------------------------|-----------------|---------------------------------------------------------------------|
| c) Model-agnostic fixed limits (no WF)     | max(ceil(3/1.0), ceil(18/6), ceil(7/3)) = max(3,3,3)        | 3 (+1 ckpt)           | max(ceil(3/1.0), ceil(18/6), ceil(7/3)) = max(3,3,3)        | 3 (+2 ckpts)    | Strict scope guard + ckpt every 1-2 prompts from Notes; matches P1  |
| a) ECI band to HWH table                   | WF=2.0 (E165); max(ceil(3/2.0), ceil(18/6), ceil(7/3))      | 3 (+1 ckpt)           | WF=0.5 (E150); max(ceil(3/0.5), ceil(18/6), ceil(7/3))      | 6 (+3 ckpts)    | Halves YY-L's 12 prompts to 6; reflects E150 (151.94) band          |
| e) UC-1..5 to HWH table                    | WF=1.0 (UC-2); max(ceil(3/1.0), ceil(18/6), ceil(7/3))      | 3 (+1 ckpt)           | WF=1.0 (UC-2); max(ceil(3/1.0), ceil(18/6), ceil(7/3))      | 3 (+2 ckpts)    | Treats glm-5.2 and opus-5 identically because both are vendor UC-2  |
| b) METR 80% horizon + fallback             | Not in METR → fallback (e.g. 1.0-2.0) → max(2..3, 3, 3)     | 3 (+1 ckpt)           | Not in METR → fallback (e.g. 0.5) → max(6, 3, 3)            | 6 (+3 ckpts)    | Neither model is in METR YAML (6/28 exact); 100% driven by fallback |
| d) Keep YY-L formula                       | WF=2.0 (26-A); max(ceil(3/2.0), ceil(18/6), ceil(7/3))      | 3 (+1 ckpt)           | WF=0.25 (26-D, R4); max(ceil(3/0.25), ceil(18/4), ceil(7/2))| 12 (+12 ckpts)  | 24 total prompts incl. checkpoints; contradicts session observations|

- **Key Takeaway from Worked Example**: For `claude-opus-5` High, **all five options produce `3` implementation prompts** because item density (`18 / 6 = 3`) and file breadth (`7 / 3 = 3`) are the binding constraints. The options diverge only on `glm-5.2` High: Option d (`YY-L`) forces `12` implementation prompts (`24` with checkpoints), Option a (`ECI band`) produces `6` prompts, and Option c (`Model-agnostic limits + Notes scope guard`) produces `3` implementation prompts (`5` with checkpoints)—matching the `5`-prompt compressed sequence that `glm-5.2` high executed with `0` skipped items in this session `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-IPPS-FAILS | e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Findings.md)`.

## 9. Limitations and Known Issues

- **In-session Partition Observations cover only `glm-5.2` high (`N=7` prompts)**: While `AINWSRCH` and `MDLINVNTRY` confirm that `glm-5.2` high completes `4-12` items per prompt under a strict scope guard, comparable ledger rows for `UC-4` (`claude-haiku-4-5`, `gpt-5-mini`, `gpt-5.6-luna`) are not yet recorded `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-IPPS-FAILS | e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Findings.md)`.
- **Human HWH estimation variance is ~2x**: Both [METR's developer RCT](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) and [Anthropic's productivity study](https://www.anthropic.com/research/estimating-productivity-gains) show that human and LLM task-hour estimates vary by a factor of ~2, bounding the precision of any HWH-based formula `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-LOCAL-LLMCAP | e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_INFO_HOW_TO_ORGANIZE_LLMS_BY_CAPABILITY.md)`.
- **Framework variance exceeds model variance on over-eagerness**: The [SNARE benchmark study](https://arxiv.org/abs/2605.28122) found that the agent framework accounts for `56%` of over-eagerness variance vs `21%` for the base model, meaning prompt scope guards in `PROMPTS_GUIDES.md` have higher leverage than per-model numeric multipliers `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-LOCAL-PARTTN | e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\T01_MDLBHVPRM_BehavioralParameterBenchmarks_2026-10-19\_INFO_MDLBHVPRM-06_ModelAwarePartitioning.md)`.

## Sources

- **MDLRGUP-MDLINVNTRY-SC-IPPS-MDLINV**: `e:\dev\IPPS\PromptSystemV4.5\skills\write-documents\MODEL_INVENTORY.md` - Current `YY-L` formula, R1-R5 rules, profile parameters, and 28-model table (Accessed: 2026-10-28) `[VERIFIED]`
- **MDLRGUP-MDLINVNTRY-SC-IPPS-TSKGD**: `e:\dev\IPPS\PromptSystemV4.5\skills\write-documents\TASKS_GUIDES.md` - HWH buckets and task sizing rules (Accessed: 2026-10-28) `[VERIFIED]`
- **MDLRGUP-MDLINVNTRY-SC-IPPS-PRMGD**: `e:\dev\IPPS\PromptSystemV4.5\skills\write-documents\PROMPTS_GUIDES.md` - Sections 1c, 1f, 1g, 3a, 5 partitioning formulas and item/file heuristics (Accessed: 2026-10-28) `[VERIFIED]`
- **MDLRGUP-MDLINVNTRY-SC-IPPS-PRMRL**: `e:\dev\IPPS\PromptSystemV4.5\skills\write-documents\PROMPTS_RULES.md` - `PRMT-SC-05` verification checks (Accessed: 2026-10-28) `[VERIFIED]`
- **MDLRGUP-MDLINVNTRY-SC-IPPS-MREG**: `e:\dev\IPPS\PromptSystemV4.5\skills\llm-evaluation\model-registry.json` - 28 capability-labeled models, context windows, and prefix rules (Accessed: 2026-10-28) `[VERIFIED]`
- **MDLRGUP-MDLINVNTRY-SC-IPPS-FAILS**: `e:\dev\IPPS\FAILS.md` and `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Findings.md` - 7 Partition Observations on `glm-5.2` high (`100%` item completion, `3-9` min/prompt) (Accessed: 2026-10-28) `[VERIFIED]`
- **MDLRGUP-MDLINVNTRY-SC-LOCAL-LLMCAP**: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_INFO_HOW_TO_ORGANIZE_LLMS_BY_CAPABILITY.md` - Sections 4, 6, 9, 10 (`YY-L` circular derivation, worked example, HWH/AWH conversion) (Accessed: 2026-10-28) `[VERIFIED]`
- **MDLRGUP-MDLINVNTRY-SC-KWRK-ANTIER**: `e:\Dev\KarstensWorkspace\_Sessions\_!AINewsResearch\NOTES.md` - 4-field model tier record (`Vendor generation`, `UC-1..5`, `ECI band`, `Generation equivalent`) (Accessed: 2026-10-28) `[VERIFIED]`
- **MDLRGUP-MDLINVNTRY-SC-KWRK-MODTIR**: `e:\Dev\KarstensWorkspace\_Sessions\_!AINewsResearch\_INFO_AINWSRCH-MODELTIER-01_GenerationTiering.md` - Rationale for UC-1..5 and Epoch ECI 5-point bands (Accessed: 2026-10-28) `[VERIFIED]`
- **MDLRGUP-MDLINVNTRY-SC-LOCAL-COVMTX**: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\T01_MDLBHVPRM_BehavioralParameterBenchmarks_2026-10-19\_INFO_MDLBHVPRM-05_CoverageMatrix.md` - `0/28` IFEval-Hard and `1/28` OverAct SIR coverage (Accessed: 2026-10-28) `[VERIFIED]`
- **MDLRGUP-MDLINVNTRY-SC-LOCAL-PARTTN**: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\T01_MDLBHVPRM_BehavioralParameterBenchmarks_2026-10-19\_INFO_MDLBHVPRM-06_ModelAwarePartitioning.md` - Section 4 partition parameters (`max_items`, `max_files`, `checkpoint_interval`, `scope_guard`) and SNARE variance (Accessed: 2026-10-28) `[VERIFIED]`
- **MDLRGUP-MDLINVNTRY-SC-KWRK-TMPLTE**: `e:\Dev\KarstensWorkspace\_Sessions\_!AINewsResearch\_PROMPTS_AI-News-Research_TEMPLATE.md` - Lines 55-62 production prompt sizes on `glm-5.2` high (`~90k` tokens in P02, `~165k` in Session A) (Accessed: 2026-10-28) `[VERIFIED]`
- **MDLRGUP-MDLINVNTRY-SC-EPOCH-ECI**: Epoch Capabilities Index https://epoch.ai/eci - `28/28` coverage in `eci-leaderboard-general.csv` (`_SOURCES/2026-10-28_Epoch-ECI-Match.json`) (Accessed: 2026-10-28) `[VERIFIED]`
- **MDLRGUP-MDLINVNTRY-SC-METR-TMHOR**: METR Time Horizons https://metr.org/time-horizons/ - `6/28` exact (`7/28` prefix) coverage in `benchmark_results_1_1.yaml`, frozen `2026-09-08` (`_SOURCES/2026-10-28_METR-TimeHorizons-DOM.json`) (Accessed: 2026-10-28) `[VERIFIED]`

## Document History

**[2026-10-28 20:22]**
- Initial evaluation of five work-per-prompt options (`a`-`e`) with 0-3 scoring across five dimensions, self-critiques, comparison table, worked example on `glm-5.2` high and `claude-opus-5` high, and recommendation

