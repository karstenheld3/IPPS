<PromptSystem MarkdownTablesAllowed=true />

# Reliable Model Inventory and Lean Agentic Work Planning - Summary

**Doc ID**: MDLRGUP-MDLINVNTRY-IN01
**Goal**: Cross-document synthesis, source-backed model inventory evaluation, and design decisions DD-01..05 for Reliable Model Inventory research
**Timeline**: Created 2026-10-28, Updated 0 times
**Version scope**: 2026-10-28
**Strategy & Domain**: MEPI (curated, actionable; reversible inventory schema decisions within a 30 min P1 research budget) | DEFAULT (spans provider documentation, benchmark databases Epoch and METR, and practical prompt planning)
**Research stats**: 32 sources (16 local files, 10 provider documentation URLs, 5 capability/benchmark web sources, 1 environment registry), 3 topic files (IN03-IN05), 4 DOM/CSV JSON extracts in `_SOURCES/`, 7/7 preflight assumptions verified (3 CORRECT, 4 PARTIAL, 0 WRONG), 48 min net working time across 8 prompts

**Depends on:**
- `_INFO_MDLRGUP-MDLINVNTRY-02_Sources.md [MDLRGUP-MDLINVNTRY-IN02]` for source IDs and verification status
- `_INFO_MDLRGUP-MDLINVNTRY-03_InventoryAudit.md [MDLRGUP-MDLINVNTRY-IN03]` for SOURCED / DERIVED / ASSUMED classification and token counts
- `_INFO_MDLRGUP-MDLINVNTRY-04_SourcesPerField.md [MDLRGUP-MDLINVNTRY-IN04]` for authoritative sources and coverage per inventory field
- `_INFO_MDLRGUP-MDLINVNTRY-05_WorkPerPromptOptions.md [MDLRGUP-MDLINVNTRY-IN05]` for scored work-per-prompt options and worked example

## Goals

- **Goal 1 (Workable agentic planning in TASKS and PROMPTS)** → `[ACHIEVED]` Evaluated five candidate methods (`a`-`e`) in `MDLRGUP-MDLINVNTRY-IN05`; identified **Option c (Model-agnostic fixed limits, 13/15)** and **Option a (ECI band to HWH table, 12/15)** as workable replacements for the circular `YY-L` formula `[VERIFIED]`
- **Goal 2 (General-purpose portability across agent environments)** → `[ACHIEVED]` Identified all 5 Devin-specific items in `MODEL_INVENTORY.md` (`Devin cost` column, 9 Section 3.2 Devin-only rows, Devin price formula, `windsurf-model-registry.json` dependency, display-name rule) for removal or isolation in `DD-04` `[VERIFIED]`
- **Goal 3 (Lean inventory and instructions without unnecessary token consumption)** → `[ACHIEVED]` Audited 315 lines (4,717 words) across 4 files (`MDLRGUP-MDLINVNTRY-IN03`); showed that dropping Section 2 assumptions and consolidating 5 overlapping `PROMPTS_GUIDES.md` sections cuts `MODEL_INVENTORY.md` from 127 lines to `<55` lines `[VERIFIED]`
- **Goal 4 (Reliable sources for recurring inventory updates)** → `[ACHIEVED]` Verified `28/28` model coverage across 5 core fields (`Context window`, `Max output`, `Effort levels`, `Prices`, `Epoch ECI`), checked all 9 `update-model-registry.md` provider URLs (`5` direct, `4` redirected, `0` dead), and extracted Google Gemini's DOM structure (`MDLRGUP-MDLINVNTRY-IN04`) `[VERIFIED]`

## Questions

Q1: Which values and rules in `MODEL_INVENTORY.md`, `TASKS_GUIDES.md`, `PROMPTS_GUIDES.md` (1c, 1f, 1g, 3a, 5), and `PROMPTS_RULES.md` (`PRMT-SC-05`) are SOURCED vs DERIVED vs ASSUMED?
A1: Across 82 classified items (315 lines, 4,717 words), only `18` (22%) are `SOURCED`, `27` (33%) are `DERIVED` (`20/27` derived from assumed inputs), and `37` (45%) are `ASSUMED`—with `MODEL_INVENTORY.md` carrying `59%` `ASSUMED` (`26/44` rows), anchored by the circular `YY-L` Workload Factor (WF) formula (`MDLRGUP-MDLINVNTRY-IN03`) `[VERIFIED]`.

Q2: What authoritative source, update cadence, extraction method, and model coverage exist for each of the eight model inventory fields?
A2: Five fields achieve `28/28` (100%) coverage of Section 3.1 API models from authoritative sources (`Context window`, `Max output`, `Effort levels`, `Prices`, and `Capability evidence` via [Epoch Capabilities Index (ECI)](https://epoch.ai/eci) CSV `eci-leaderboard-general.csv`), whereas `Release date` (`3/28` in registry IDs, `28/28` in Epoch full CSV), [Model Evaluation and Threat Research (METR) Time Horizons](https://metr.org/time-horizons/) (`6/28` exact, `7/28` prefix, frozen `2026-09-08`), `Behavior evidence` (`0/28` IFEval-Hard, `1/28` OverAct Scope Inflation Rate (SIR)), and `Agent environment availability` (`22/28` in Devin, `0` in Claude Code/Codex/Cursor) have partial or environment-specific coverage (`MDLRGUP-MDLINVNTRY-IN04`) `[VERIFIED]`.

Q3: How can Google Gemini API models and pricing be extracted into the canonical JSONs alongside Anthropic, OpenAI, and Z.AI?
A3: [Google Gemini Pricing](https://ai.google.dev/gemini-api/docs/pricing) (88 HTML tables) and [Google Gemini Models](https://ai.google.dev/gemini-api/docs/models) (11 index tables plus per-model subpages and [Thinking docs](https://ai.google.dev/gemini-api/docs/thinking)) use standard HTML `<table>` elements covering all 10 current Gemini text models (`gemini-4-argon` through `gemini-2.5-flash-lite`), but require three Google-specific Document Object Model (DOM) rules: iterating per-model `<h2>` headings (`table[0]` for Standard tier), parsing scheduled dual prices in cells (`$2.00 through Nov 30 / $4.00 starting Dec 1`), and joining `/models/<slug>` token limits with `/thinking` effort tables (`MDLRGUP-MDLINVNTRY-IN04`) `[VERIFIED]`.

Q4: What is the best method to size agentic prompts (`work per prompt`) from sourced data without precision theater?
A4: **Option c (Model-agnostic fixed limits without WF)** scores highest (`13/15`: `<= 1.0` Human Work Hours (HWH), `<= 6` items, `<= 3` files, `<= 50%` context, plus `Notes`-driven strict scope guard and checkpoint interval), followed closely by **Option a (ECI band to HWH table)** (`12/15`: 4 ECI band groups mapped to `2.0 / 1.0 / 0.5 / 0.25 HWH`), whereas keeping the `YY-L` formula scores lowest (`6/15`) and forces `12` prompts on `glm-5.2` high for a `3 HWH` task that `glm-5.2` high completes in `3-5` prompts (`MDLRGUP-MDLINVNTRY-IN05`) `[VERIFIED]`.

## Summary

This research audited the model inventory and prompt-partitioning rules introduced by `LLMCAPCLS-TK01` across four PromptSystem files (`MODEL_INVENTORY.md`, `TASKS_GUIDES.md`, `PROMPTS_GUIDES.md`, `PROMPTS_RULES.md`), tested external capability and provider sources against all 28 API models, and evaluated five replacement methods for prompt sizing (`MDLRGUP-MDLINVNTRY-IN03`, `IN04`, `IN05`) `[VERIFIED]`. The line-by-line audit found that `59%` of `MODEL_INVENTORY.md` (`26/44` items) and `45%` of all 82 classified items across the four scopes are unmeasured assumptions (`ASSUMED`), and `20 of 27` `DERIVED` items propagate those assumptions (`IN03`) `[VERIFIED]`. In particular, the `YY-L` capability labels (`25-A`..`26-D`) and `WF_high` formula were fitted circularly to reproduce the prior table (`LLMCAPCLS-IN01` Section 6), require manual October re-grading (`R3`), duplicate the time-independent 4-field model tier record already established in `AINWSRCH-MODELTIER-IN01` (`Vendor generation`, `Universal Class UC-1..5`, `ECI band`, `Generation equivalent`), and penalize `glm-5.2` high with `WF = 0.25 HWH` (`12` prompts for a `3 HWH` task) despite empirical runs showing `100%` item completion across `7/7` prompts (`4-12` items/prompt) when guarded by a strict scope boundary (`IN03`, `IN05`) `[VERIFIED]`. Source verification confirmed that five inventory fields—`Context window`, `Max output`, `Effort levels`, `Prices`, and `Epoch ECI` (`eci-leaderboard-general.csv`)—have `28/28` (100%) sourced coverage across all current inventory models, whereas `METR Time Horizons` covers only `6/28` exact (`7/28` prefix) and stopped updating on `2026-09-08`, and `Behavior evidence` covers `0/28` for `IFEval-Hard` and `1/28` for `OverAct SIR`, leaving `27/28` models with an identical `standard` profile (`IN04`) `[VERIFIED]`. Evaluating five work-per-prompt methods on a 15-point scale showed that **Option c (Model-agnostic fixed limits without WF, 13/15)** and **Option a (ECI band to HWH table, 12/15)** eliminate the circular `YY-L` formula (`6/15`), cut `MODEL_INVENTORY.md` below 60 lines, and remove environment-specific Devin columns (`IN05`) `[VERIFIED]`.

### Key Findings (Cross-Document Synthesis)

- **KF-01 (`IN03` — High assumption density in `MODEL_INVENTORY.md`)**: Across 82 classified items (315 lines, 4,717 words) in the four audited scopes, `37` (45%) are `ASSUMED`, `27` (33%) are `DERIVED` (`20/27` depending on `ASSUMED` inputs), and `18` (22%) are `SOURCED`; `MODEL_INVENTORY.md` Section 2 alone (37 lines) holds `60%` of all `ASSUMED` items in the file `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-IPPS-MDLINV | e:\dev\IPPS\PromptSystemV4.5\skills\write-documents\MODEL_INVENTORY.md)`
- **KF-02 (`IN03` — Circular `YY-L` derivation and duplicate tiering)**: `LLMCAPCLS-IN01` Section 6 explicitly states that `YY-L` labels (`25-A`..`26-D`) were assigned to reproduce the previous unmeasured WF table (`35/37` rows unchanged), creating a second model tiering scheme alongside the time-independent `AINWSRCH` 4-field tier record (`Vendor generation`, `UC-1..5`, `ECI band`, `Generation equivalent`) `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-LOCAL-LLMCAP | e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_INFO_HOW_TO_ORGANIZE_LLMS_BY_CAPABILITY.md)`
- **KF-03 (`IN04` — 100% Epoch ECI coverage across all 28 inventory models)**: Every one of the 28 API models in `MODEL_INVENTORY.md` Section 3.1 matches a row in [Epoch's ECI leaderboard CSV](https://epoch.ai/eci) (`eci-leaderboard-general.csv`, 270 models) by exact name (`24/28`), case variant (`2/28`: `o3`, `GPT-5 mini`), hyphen variant (`1/28`: `GLM-5.3-Flash`), or scale anchor (`1/28`: `GPT-5 = 150.00`), spanning eight 5-point bands from `E135` (`gpt-4.1` `136.65`) to `E170` (`gpt-6-astra` `168.81`) (`_SOURCES/2026-10-28_Epoch-ECI-Match.json`) `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-EPOCH-ECI | https://epoch.ai/eci)`
- **KF-04 (`IN04` — METR Time Horizons is frozen and covers only 21-25% of inventory)**: [METR Time Horizons](https://metr.org/time-horizons/) (`benchmark_results_1_1.yaml`, 26 models, raw values in minutes) displays the banner `"This page is no longer actively updated. LAST UPDATED September 8, 2026"` and covers only `6/28` exact (`7/28` with `gpt-5.1` prefix) of the 28 inventory models, with `0/5` Z.AI models and `0` mid/late-2026 flagships (`_SOURCES/2026-10-28_METR-TimeHorizons-DOM.json`) `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-METR-TMHOR | https://metr.org/time-horizons/)`
- **KF-05 (`IN04` — Near-zero behavioral benchmark coverage makes `Profile` column redundant)**: In `_INFO_MDLBHVPRM-05_CoverageMatrix.md`, `IFEval-Hard` covers `0/28` inventory models and `OverAct SIR` covers `1/28` (`glm-5.2` = `2.00`), causing `27 of 28` rows in `MODEL_INVENTORY.md` to default to `standard` profile `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-LOCAL-COVMTX | e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\T01_MDLBHVPRM_BehavioralParameterBenchmarks_2026-10-19\_INFO_MDLBHVPRM-05_CoverageMatrix.md)`
- **KF-06 (`IN04` — All 9 provider URLs resolve HTTP 200, with 4 redirects and 1 div-card layout)**: Batch checking `A1`-`A4`, `O1`-`O3`, and `Z1`-`Z2` from `update-model-registry.md` confirmed `0` dead links (`5` direct HTTP 200: `A4`, `O1`, `O2`, `Z1`, `Z2`; `4` HTTP 200 redirects: `A1` → `platform.claude.com/docs/en/about-claude/pricing`, `A2`/`A3` → `platform.claude.com/docs/en/models/overview`, `O3` → `developers.openai.com/api/docs/models/compare`), with `O3` rendering custom `<div>` cards instead of an HTML `<table>` `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-IPPS-UMREG | e:\dev\IPPS\update-model-registry.md)`
- **KF-07 (`IN04` — Google Gemini DOM extraction requires 3 provider-specific rules)**: [Google Gemini Pricing](https://ai.google.dev/gemini-api/docs/pricing) (88 HTML tables) and [Google Gemini Models](https://ai.google.dev/gemini-api/docs/models) (11 index tables) cover 10 current Gemini text models (`gemini-4-argon` `E165`, `gemini-3.8-flash` `E155`, `gemini-3.6-flash` `E155`, `gemini-3.5-flash-lite`, `gemini-3.1-flash-lite`, `gemini-3.1-pro-preview` `E155`, `gemini-3-flash-preview` `E150`, `gemini-2.5-pro` `E145`, `gemini-2.5-flash`, `gemini-2.5-flash-lite`), requiring H2-scoped `table[0]` extraction, scheduled dual-price parsing (`$2.00` through Nov 30 / `$4.00` starting Dec 1 on `gemini-4-argon`), and joining per-model subpages (`1,048,576` input context, `65,536` default output) with `/thinking` effort tables (`_SOURCES/2026-10-28_Google-Pricing-DOM.json`, `_SOURCES/2026-10-28_Google-Models-DOM.json`) `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-GOOG-GMPRC | https://ai.google.dev/gemini-api/docs/pricing)`
- **KF-08 (`IN03`, `IN04` — Five Goal 2 violations tie `MODEL_INVENTORY.md` to Devin/Cascade)**: `MODEL_INVENTORY.md` embeds `Devin cost` in Section 3.1 (`22/28` coverage from `windsurf-model-registry.json`), 9 Devin-only models in Section 3.2, a Devin-only price formula, `windsurf-model-registry.json` as canonical source #4, and a Devin display-name resolution rule, while Claude Code, OpenAI Codex CLI, and Cursor are not inventoried `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-IPPS-WMREG | e:\dev\IPPS\PromptSystemV4.5\skills\devin-auto-model-switcher\windsurf-model-registry.json)`
- **KF-09 (`IN05` — Production and in-session runs refute `glm-5.2` `WF = 0.25 HWH`)**: `glm-5.2` high completes `~90k` token research prompts (58-69 sources) in `AINWSRCH` and completed `7/7` prompts (`100%` of planned items, `4-12` items and `2-9` files per prompt in `3-9` minutes) in this session when paired with a strict scope guard, proving that `glm-5.2`'s failure mode is scope inflation (`OverAct SIR 2.00`), not a `0.25 HWH` capacity ceiling `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-IPPS-FAILS | e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Findings.md)`
- **KF-10 (`IN05` — Work-per-prompt options c and a outperform YY-L by +6 to +7 points)**: On the 15-point rubric (`Sourced`, `Coverage`, `Tokens`, `General purpose`, `Calibratable`), **Option c (Model-agnostic fixed limits without WF)** scores `13/15` and **Option a (ECI band to HWH table)** scores `12/15`, ahead of **Option e (UC-1..5 to HWH table, 10/15)**, **Option b (METR 80% horizon + fallback, 7/15)**, and **Option d (Keep YY-L formula, 6/15)** `[VERIFIED] (MDLRGUP-MDLINVNTRY-SC-IPPS-MDLINV | e:\dev\IPPS\PromptSystemV4.5\skills\write-documents\MODEL_INVENTORY.md)`

## Table of Contents

1. [Topic Files](#1-topic-files)
2. [Topic Count](#2-topic-count)
3. [Per-Topic Summaries](#3-per-topic-summaries)
4. [Conclusions](#4-conclusions)
5. [Decisions for ACTOR (DD-01 to DD-05)](#5-decisions-for-actor-dd-01-to-dd-05)
6. [Recommendations](#6-recommendations)
7. [Limitations](#7-limitations)
8. [Document History](#8-document-history)

## 1. Topic Files

### Audit and Source Verification (2 files)

- [`_INFO_MDLRGUP-MDLINVNTRY-03_InventoryAudit.md`](./_INFO_MDLRGUP-MDLINVNTRY-03_InventoryAudit.md) [MDLRGUP-MDLINVNTRY-IN03]
  - Line-by-line SOURCED / DERIVED / ASSUMED classification across `MODEL_INVENTORY.md`, `TASKS_GUIDES.md`, `PROMPTS_GUIDES.md` (1c, 1f, 1g, 3a, 5), and `PROMPTS_RULES.md` (`PRMT-SC-05`), with word/line counts and Goal 2/3 violations
- [`_INFO_MDLRGUP-MDLINVNTRY-04_SourcesPerField.md`](./_INFO_MDLRGUP-MDLINVNTRY-04_SourcesPerField.md) [MDLRGUP-MDLINVNTRY-IN04]
  - Authoritative source, URL, update cadence, extraction method, coverage of the 28 inventory models, and caveats for all eight inventory fields, plus Google Gemini DOM extraction gap analysis

### Planning Method Evaluation (1 file)

- [`_INFO_MDLRGUP-MDLINVNTRY-05_WorkPerPromptOptions.md`](./_INFO_MDLRGUP-MDLINVNTRY-05_WorkPerPromptOptions.md) [MDLRGUP-MDLINVNTRY-IN05]
  - Evaluation of five candidate methods (`a`-`e`) for deriving work-per-prompt on a 0-15 rubric, with self-critiques, comparison table, recommendation, and worked example on `glm-5.2` high and `claude-opus-5` high

## 2. Topic Count

- **Total Topics**: 3 (plus `IN01` Summary and `IN02` Sources)
- **Audit and Source Verification**: 2 (`IN03`, `IN04`)
- **Planning Method Evaluation**: 1 (`IN05`)

## 3. Per-Topic Summaries

### IN03: Inventory Audit - Value and Rule Classification

`MDLRGUP-MDLINVNTRY-IN03` audited every statement, formula, threshold, and table column across `MODEL_INVENTORY.md` (127 lines, 2,151 words), `TASKS_GUIDES.md` (60 lines, 633 words), `PROMPTS_GUIDES.md` Sections 1c/1f/1g/3a/5 (115 lines, 1,685 words), and `PROMPTS_RULES.md` `PRMT-SC-05` (13 lines, 248 words). Across 82 classified rows totaling 315 lines and 4,717 words, only `18` rows (22%) are `SOURCED`, `27` (33%) are `DERIVED`, and `37` (45%) are `ASSUMED`. `MODEL_INVENTORY.md` has the highest assumption density at `59%` (`26/44` rows), concentrated in Section 2 (L28-64), which defines the `YY-L` capability labels, the `WF_high` formula, rules `R2`/`R3`, profile thresholds, profile parameters, effort multipliers, and the `1 HWH = 1M tokens` cost conversion. Furthermore, `20 of the 27` `DERIVED` rows across the four files compute directly from `ASSUMED` inputs (`WF` or profile parameters), meaning `PRMT-SC-05` enforces verification against unmeasured numbers ("precision theater").

**Key Findings:**
- `MODEL_INVENTORY.md` is `59%` `ASSUMED` (`26/44` rows); removing `ASSUMED` items leaves only Model IDs, Context windows, Max output, Effort flags, provider prices, and documented FAILS observations `[VERIFIED]`
- Five items in `MODEL_INVENTORY.md` violate Goal 2 (environment independence) by embedding Devin cost multipliers, 9 Devin-only models, and `windsurf-model-registry.json` rules `[VERIFIED]`
- Four structures violate Goal 3 (leanness): `R3` October review rule, the 3-sequence profile change rule, partitioning spread across 5 overlapping sections of `PROMPTS_GUIDES.md` (`1c`, `1f`, `1g`, `3a`, `5`), and `PRMT-SC-05` numeric verification against assumed WF values `[VERIFIED]`

### IN04: Reliable Sources per Model Inventory Field

`MDLRGUP-MDLINVNTRY-IN04` mapped each of the eight model inventory fields (`Context window`, `Max output`, `Effort levels`, `Prices`, `Release date`, `Capability evidence`, `Behavior evidence`, `Agent environment availability`) to its primary source, URL, update cadence, extraction method, coverage across the 28 Section 3.1 models, and caveats. Five fields have `28/28` (100%) coverage from authoritative sources: `Context window` (`24/28` in `model-registry.json` + `4/28` fallback in `model-pricing.json`), `Max output` (`28/28` via prefix rules + provider docs), `Effort levels` (`28/28` via prefix rules + Phase 8 API probes), `Prices` (`28/28` in `model-pricing.json`), and `Capability evidence` via Epoch's `eci-leaderboard-general.csv` (`28/28`). Conversely, `METR Time Horizons` covers only `6/28` exact (`7/28` prefix) and stopped updating on `2026-09-08`, and `Behavior evidence` covers `0/28` for `IFEval-Hard` and `1/28` for `OverAct SIR`. Playwright DOM extraction on Google Gemini's `/pricing`, `/models`, and `/thinking` pages confirmed 100% HTML table coverage for all 10 current Google text models and documented the three extraction adaptations required for `update-model-registry.md`.

**Key Findings:**
- Epoch ECI CSV (`eci-leaderboard-general.csv`, 270 rows) covers `28/28` Section 3.1 models (`E135` to `E170`) plus 15 additional frontier/Google/Devin models (`Gemini 4 Argon` `166.45`, `Claude Opus 5.5` `168.83`, `GPT-6.1 Sol` `168.37`) `[VERIFIED]`
- All 9 provider URLs in `update-model-registry.md` (`A1`-`A4`, `O1`-`O3`, `Z1`-`Z2`) return HTTP 200 (`5` direct, `4` redirected to canonical `platform.claude.com` / `developers.openai.com` URLs, `0` dead) `[VERIFIED]`
- Google Gemini API pricing (88 tables, H2-per-model with 4-5 tier tabs and scheduled dual prices) and models (split across `/models`, `/models/<slug>`, and `/thinking`) require a dedicated Google extraction block in `update-model-registry.md` `[VERIFIED]`

### IN05: Candidate Methods for Deriving Work-per-Prompt

`MDLRGUP-MDLINVNTRY-IN05` scored five candidate methods (`a` through `e`) for sizing agentic prompts (`work per prompt`) across five 0-3 criteria (`Sourced`, `Coverage`, `Tokens`, `General purpose`, `Calibratable`; max 15) and tested each on the benchmark `3 HWH` task (`18` items, `7` files) for `claude-opus-5` high and `glm-5.2` high. Because no external benchmark measures single-prompt HWH capacity before item drop-out, no option scores `3/3` on `Sourced`. **Option c (Model-agnostic fixed limits without WF)** scores highest at `13/15` (`2+3+3+3+2`), eliminating all 26 `ASSUMED` items in `MODEL_INVENTORY.md` and sizing prompts by global operational caps (`<= 1.0 HWH`, `<= 6` items, `<= 3` files, `<= 50%` context, plus `Notes`-driven strict scope guard). **Option a (ECI band to HWH table)** finishes a close second at `12/15` (`2+3+2+3+2`), using `28/28` sourced Epoch ECI bands (`E165+ → 2.0`, `E155-E160 → 1.0`, `E145-E150 → 0.5`, `<=E140 → 0.25 HWH`) for model-differentiated sizing, ahead of **Option e (UC-1..5 to HWH, 10/15)**, **Option b (METR 80% horizon + fallback, 7/15)**, and **Option d (Keep YY-L formula, 6/15)**.

**Key Findings:**
- On `claude-opus-5` high (`3 HWH`, `18` items, `7` files), all five options yield `3` implementation prompts because item count (`18/6 = 3`) and file count (`7/3 = 3`) dominate WF `[VERIFIED]`
- On `glm-5.2` high, Option d (`YY-L` `26-D`, `WF 0.25`) forces `12` implementation prompts (`24` with checkpoints), whereas Option a (`ECI E150`, `WF 0.5`) yields `6` prompts and Option c (`Fixed limits + Notes scope guard`) yields `3` implementation prompts (`5` with checkpoints), matching the `5`-prompt compressed chain executed with `0` skipped items in this session `[VERIFIED]`
- Option c (`13/15`) is recommended for maximum leanness (Goal 3); Option a (`12/15`) is the recommended alternative if model-scaled HWH partitioning is desired `[VERIFIED]`

## 4. Conclusions

1. **Replace `YY-L` with the existing `UC + ECI band` tier record (`IN03`, `IN04`)**: `YY-L` is circular (`LLMCAPCLS-IN01` Section 6), requires manual October reviews (`R3`), and violates MECT by duplicating the `AINWSRCH` tier design, whereas `UC-1..5` (from vendor docs/pricing) + `ECI band` (from `https://epoch.ai/eci`, `28/28` coverage) are 100% sourced and time-independent `[VERIFIED]`.
2. **Eliminate `WF` columns from `MODEL_INVENTORY.md` and adopt either Model-Agnostic Fixed Limits (`Option c`, 13/15) or a 4-row ECI-Band Lookup (`Option a`, 12/15) in `PROMPTS_GUIDES.md` (`IN03`, `IN05`)**: Keeping `MODEL_INVENTORY.md` strictly as a sourced reference table (`Model`, `UC`, `ECI band`, `Context`, `Max output`, `Effort levels`, `Standard Prices`, `Notes`) cuts it from 127 lines to `<55` lines and removes all 26 `ASSUMED` items `[VERIFIED]`.
3. **Drop the `Profile` column (`27/28` `standard`) and record behavioral quirks in `Notes` (`IN03`, `IN04`, `IN05`)**: With `0/28` `IFEval-Hard` and `1/28` `OverAct SIR` coverage, the 3-tier profile system (`precise`/`standard`/`guarded`) and unbuilt JSONL ledger add 20+ lines of rules to express a single fact (`glm-5.2` requires a strict scope guard and 1-2 prompt checkpoints), which `Notes` already captures `[VERIFIED]`.
4. **Remove Devin-specific columns and rows from `MODEL_INVENTORY.md` (`IN03`, `IN04`)**: Moving `Devin cost` and the 9 Devin-only models out of `MODEL_INVENTORY.md` (keeping them in `windsurf-model-registry.json`) satisfies Goal 2 (general-purpose inventory) `[VERIFIED]`.
5. **Add Google Gemini API (`10` models) to the canonical registries and `update-model-registry.md` (`IN04`)**: Adding Anthropic, OpenAI, Google Gemini, and Z.AI under one DOM extraction workflow covers all four primary API providers used across workspaces `[VERIFIED]`.

## 5. Decisions for ACTOR (DD-01 to DD-05)

# DD-01: Which capability representation should MODEL_INVENTORY.md and model-registry.json use?

**Problem**: `MODEL_INVENTORY.md` and `model-registry.json` currently use `YY-L` (`25-A`..`26-D`), a circularly fitted judgment scheme (`LLMCAPCLS-IN01` Section 6) that requires a manual October re-grading review (`R3`) and duplicates the 4-field model tier record already established in `AINWSRCH` (`MDLRGUP-MDLINVNTRY-IN03`).
**Context**: MECT requires one scheme per concept across workspaces. Fixed points: Epoch ECI (`https://epoch.ai/eci`) is the sole external capability index (`QS-12` bans Artificial Analysis and LMArena Elo), and `eci-leaderboard-general.csv` covers `28/28` current inventory models (`MDLRGUP-MDLINVNTRY-IN04`).

**Options**
- **a) Reuse UC + ECI band + generation equivalent** (recommended)
  - What: Replace `capability_label` (`YY-L`) with the `AINWSRCH` tier fields: `Universal Class` (`UC-1..5` from vendor docs/price order), `ECI band` (`E135`..`E170` with score and snapshot date from `https://epoch.ai/eci`), and `Generation equivalent` (`≈ [reference model]`).
  - Why it works: `100%` of the 28 inventory models have both a sourced `UC` and a sourced `ECI` score (`28/28`), fields never drift when newer models ship, and no October calendar review is needed (`IN04`).
  - Implication: Replaces `capability_label` in `model-registry.json`, `MODEL_INVENTORY.md`, `TASKS_GUIDES.md`, `PROMPTS_GUIDES.md`, and `update-model-registry.md` 9.4 during Phase P5.
  - Why recommended: Eliminates circular `YY-L` labels and unifies IPPS and `KarstensWorkspace` on a single 100% sourced, time-independent capability record.
- **b) Keep YY-L**
  - What: Keep `25-A`..`26-D` labels and rules `R1`-`R5` in `MODEL_INVENTORY.md` and `model-registry.json`.
  - Why it works: Already written into the files on `2026-10-28` (`__TASKS_LLMCAPCLS.md`); zero P5 migration effort for label names.
  - Implication: Retains 6 `ASSUMED` assignment rules (`R2`, `R3` manual October review), preserves a duplicate tiering scheme alongside `AINWSRCH` (violates MECT), and keeps judgment-assigned letters (`IN03`).
- **c) METR horizon only**
  - What: Use [METR Time Horizons](https://metr.org/time-horizons/) (`p50` / `p80` in human hours) as the sole capability column in `MODEL_INVENTORY.md`.
  - Why it works: Directly expresses autonomous task duration in human expert hours for evaluated models (`claude-opus-4-6`, `gpt-5.4`, `gpt-5.2`, `claude-opus-4-5`, `gpt-5.1`, `gpt-5`, `o3`).
  - Implication: Leaves `21/28` models (`75%`, including all Z.AI models and all mid/late-2026 flagships) blank (`-`), and relies on a page that stopped updating on `2026-09-08` (`IN04`).

# DD-02: How should TASKS_GUIDES.md and PROMPTS_GUIDES.md size work per prompt?

**Problem**: Today's partitioning formulas (`prompt_count = max(ceil(HWH/WF), ...)`, `WF_high = 2.0 * 0.5^letter * 2^(YY-26)`) rest on 26 `ASSUMED` rules (`MDLRGUP-MDLINVNTRY-IN03`) and force `12` implementation prompts (`24` with checkpoints) for a `3 HWH` task on `glm-5.2` high, contradicting empirical runs where `glm-5.2` high completes `3-5` prompts with `0` skipped items (`MDLRGUP-MDLINVNTRY-IN05`).
**Context**: No external benchmark measures single-prompt HWH capacity before item drop-out (`IN04`). Fixed points: HWH task estimation buckets (`0.25`, `0.5`, `1`, `2`, `4 HWH`) in `TASKS_GUIDES.md` stay; context window, max output, effort levels, and prices remain sourced from providers.

**Options**
- **c) Model-agnostic fixed limits without WF** (recommended — scored `13/15` in `IN05`)
  - What: Drop `WF`, per-effort WF columns, and `USD per WF 1` from `MODEL_INVENTORY.md`; size every prompt in `PROMPTS_GUIDES.md` by fixed operational caps (`<= 1.0 HWH`, `<= 6` instruction items, `<= 3` files modified, `<= 1` heavy workflow, input read `<= 50%` of `Context`), applying a strict scope guard and `1-2` prompt checkpoint interval when `MODEL_INVENTORY.md` `Notes` documents over-eagerness or skipping.
  - Why it works: Item density (`<= 6` items) and file breadth (`<= 3` files) already dominate `WF` on frontier models (`3` prompts for `3 HWH / 18 items / 7 files`), while strict scope guards prevent `glm-5.2` scope inflation without splitting work into 12 micro-prompts (`IN05`).
  - Implication: Cuts `MODEL_INVENTORY.md` below 55 lines with zero `ASSUMED` WF columns (Goal 3), consolidates 5 overlapping sections in `PROMPTS_GUIDES.md` (`1c`, `1f`, `1g`, `3a`, `5`) into one section, and simplifies `PRMT-SC-05` to check frontmatter model/effort/context and `<= 6` items / `<= 3` files.
  - Why recommended: Achieves the highest score (`13/15`), eliminates all invented WF numbers and `USD per WF 1` assumptions from `MODEL_INVENTORY.md`, and matches actual production partitioning in `AINWSRCH` and `MDLINVNTRY`.
- **a) ECI-band → HWH table** (close runner-up — scored `12/15` in `IN05`)
  - What: Map 5-point Epoch ECI bands to a 4-row `WF_high` lookup table in `PROMPTS_GUIDES.md`: `E165+ → 2.0 HWH`, `E155-E160 → 1.0 HWH`, `E145-E150 → 0.5 HWH`, `<=E140 → 0.25 HWH` (with `UC` fallback for brand-new models not yet in Epoch's CSV).
  - Why it works: Uses `28/28` sourced ECI scores (`IN04`) to scale prompt count automatically across capability tiers (`3` prompts on `claude-opus-5` `E165`, `6` prompts on `glm-5.2` `E150`, `12` prompts on `claude-haiku-4-5` `E140`).
  - Implication: Keeps `WF` and `ceil(task_HWH / WF)` in `TASKS_GUIDES.md`, `PROMPTS_GUIDES.md`, and `PRMT-SC-05`, retaining one `[ASSUMED]` anchor (`E155-E160 = 1.0 HWH`).
- **e) UC-1..5 → HWH table** (scored `10/15` in `IN05`)
  - What: Map vendor Universal Class (`UC-1..5`) to a fixed HWH table (`UC-1/2 → 1.0-1.5 HWH`, `UC-3 → 0.5 HWH`, `UC-4 → 0.25 HWH`).
  - Why it works: `100%` available on release day from provider docs/pricing without waiting for Epoch benchmark evaluations.
  - Implication: Treats a 2025 `UC-2` (`gpt-4.1`, `E135`) as equal to a 2026 `UC-2` (`claude-opus-5`, `E165`) and rates `claude-sonnet-5` (`UC-3`, `E155`) lower than `gpt-4.1` (`IN05`).
- **b) METR 80% horizon + fallback** (scored `7/15` in `IN05`)
  - What: Use METR `p80_horizon_length` in hours as `WF_high` where available (`7/28` models), and fall back to Option a or e for the remaining `21/28` models.
  - Why it works: Uses measured human-hour horizons for the 7 covered models (`0.50` to `1.16` hr).
  - Implication: `75%` of inventory models (`21/28`, including both `claude-opus-5` and `glm-5.2`) rely on the fallback, and METR stopped updating on `2026-09-08` (`IN04`, `IN05`).
- **d) Keep YY-L formula** (scored `6/15` in `IN05`)
  - What: Keep `WF_high = 2.0 * 0.5^letter * 2^(YY-26)` and per-effort WF columns in `MODEL_INVENTORY.md`.
  - Why it works: No changes needed to existing `PROMPT` / `TASKS` formulas.
  - Implication: Retains 26 `ASSUMED` items in `MODEL_INVENTORY.md`, keeps the circularly fitted table, and forces 12 implementation prompts on `glm-5.2` high for a `3 HWH` task (`IN03`, `IN05`).

# DD-03: How should model behavioral differences (skipping items, scope creep) be recorded and used?

**Problem**: `MODEL_INVENTORY.md` defines three behavior profiles (`precise`, `standard`, `guarded`), numeric IF/EG thresholds, a 3-sequence change rule, and an unimplemented `partition-observations.jsonl` ledger (`LLMCAPCLS-DF01` D-02), yet `27 of 28` models are `standard` because `IFEval-Hard` coverage is `0/28` and `OverAct SIR` coverage is `1/28` (`MDLRGUP-MDLINVNTRY-IN03`, `IN04`).
**Context**: Only `glm-5.2` has documented over-eagerness (`OverAct SIR 2.00`) and skipping observations in `FAILS.md`. Fixed point: documented observations in `FAILS.md` and findings cards remain the authoritative trigger for stricter prompt guards.

**Options**
- **a) Drop profiles and ledger; use Notes column for observations only** (recommended)
  - What: Remove `behavior_profile` (`precise`/`standard`/`guarded`), profile threshold rules, and `observed` ledger fields from `MODEL_INVENTORY.md` and `model-registry.json`. Record documented behavioral quirks (such as `glm-5.2`: `OverAct SIR 2.00; requires strict scope guard and 1-2 prompt checkpoints`) in the `Notes` column of `MODEL_INVENTORY.md`.
  - Why it works: Preserves `100%` of the actionable information (`glm-5.2` gets a strict scope guard and frequent checkpoints) while deleting ~25 lines of unmeasured profile rules and a redundant column where 27/28 cells say `standard` (`IN03`, `IN04`).
  - Implication: Removes `behavior_profile` from `model-registry.json`, `MODEL_INVENTORY.md`, `PROMPTS_GUIDES.md`, and `PRMT-SC-05` in P5; closes deferred item `LLMCAPCLS-DF01` D-02 (`partition-observations.jsonl`).
  - Why recommended: Replaces a 28-row column of 96% identical values and unmeasured thresholds with a direct, zero-assumption `Notes` rule (Goal 3).
- **b) Keep profiles and ledger**
  - What: Retain `behavior_profile` (`precise`/`standard`/`guarded`) in `MODEL_INVENTORY.md` and `model-registry.json`, keep the `max_items 8/6/4` and `max_files 6/3/2` profile table, and keep the planned `partition-observations.jsonl` aggregation.
  - Why it works: Provides a structured enum field if future benchmark or probe data populates all 28 models.
  - Implication: Retains 9 `ASSUMED` rules/thresholds in `MODEL_INVENTORY.md`, keeps 27/28 identical `standard` rows, and leaves `LLMCAPCLS-DF01` D-02 open until a JSONL aggregation script is built (`IN03`).

# DD-04: Where should agent-environment-specific data (Devin cost multipliers, Devin-only models, display names) live?

**Problem**: `MODEL_INVENTORY.md` currently embeds a `Devin cost` column in Section 3.1, 9 Devin-only models in Section 3.2, a Devin price formula (`L63`), and `windsurf-model-registry.json` as canonical source #4—violating Goal 2 (general-purpose files usable with any agent or agentic environment) (`MDLRGUP-MDLINVNTRY-IN03`, `IN04`).
**Context**: `windsurf-model-registry.json` (`skills/devin-auto-model-switcher/`) already stores all 177 Devin/Cascade display names, `cost_multiplier` values, and tier mappings (`22/28` coverage of Section 3.1 models), while Claude Code, OpenAI Codex CLI, and Cursor have no local registry (`IN04`).

**Options**
- **a) Remove Devin cost and Devin-only rows from MODEL_INVENTORY.md; keep environment data in environment registries** (recommended)
  - What: Remove the `Devin cost` column, Section 3.2 (Devin-only models), the Devin cost formula, and the `windsurf-model-registry.json` dependency from `MODEL_INVENTORY.md`. Keep Devin display names, cost multipliers, and Devin-only models exclusively in `skills/devin-auto-model-switcher/windsurf-model-registry.json` (and add a brief environment-alias note in `PROMPTS_GUIDES.md` explaining that `intended_model` uses canonical API model IDs or prefixes).
  - Why it works: Makes `MODEL_INVENTORY.md`, `TASKS_GUIDES.md`, and `PROMPTS_GUIDES.md` 100% environment-agnostic (usable identically in Claude Code, Codex CLI, Cursor, Devin, or custom runners) without losing any Devin data (which remains in `devin-auto-model-switcher`).
  - Implication: Deletes 5 Goal 2 violations and ~20 lines from `MODEL_INVENTORY.md`; `update-model-registry.md` 9.4 no longer joins `windsurf-model-registry.json` when regenerating `MODEL_INVENTORY.md`.
  - Why recommended: Directly satisfies Goal 2 and MECT by separating provider API facts (`MODEL_INVENTORY.md`) from IDE-specific UI/billing metadata (`windsurf-model-registry.json`).
- **b) Keep Devin cost and Devin-only rows in MODEL_INVENTORY.md**
  - What: Retain the `Devin cost` column in Section 3.1 and the 9 Devin-only models in Section 3.2 of `MODEL_INVENTORY.md`.
  - Why it works: Allows a Devin user to see API prices and Devin ACU multipliers in a single table.
  - Implication: Violates Goal 2, leaves `6/28` API models without a Devin cost entry, and keeps 9 Section 3.2 rows that lack sourced context windows and API pricing (`IN03`, `IN04`).

# DD-05: Which providers and models should MODEL_INVENTORY.md and the canonical JSONs cover?

**Problem**: `MODEL_INVENTORY.md` Section 3.1 covers 28 API models from only three providers (Anthropic `10`, OpenAI `13`, Z.AI `5`), omitting all **Google Gemini API** models (`gemini-4-argon`, `gemini-3.8-flash`, `gemini-3.6-flash`, `gemini-3.1-pro-preview`, `gemini-2.5-pro/flash`) as well as late-September 2026 releases (`Claude Opus 5.5`, `GPT-6 Sol`) (`MDLRGUP-MDLINVNTRY-IN04`).
**Context**: In `P1-S6`, Playwright DOM extraction verified that Google publishes complete HTML tables for all 10 current Gemini API text models across `/pricing`, `/models`, and `/thinking`, and Epoch's CSV includes ECI scores for Google Gemini (`Gemini 4 Argon = 166.45`, `Gemini 3.8 Flash = 157.44`, `Gemini 3.6 Flash = 154.53`, `Gemini 3.1 Pro = 155.34`, `Gemini 3 Flash = 151.88`, `Gemini 2.5 Pro = 145.13`) (`IN04`).

**Options**
- **a) Four providers: Anthropic, OpenAI, Google Gemini, Z.AI** (recommended)
  - What: Expand `MODEL_INVENTORY.md`, `model-registry.json`, `model-pricing.json`, `model-parameter-mapping.json`, and `update-model-registry.md` (plus the P3 prompts template) to cover the four primary API providers: **Anthropic, OpenAI, Google Gemini, and Z.AI** (adding the Google source group `G1`-`G3` for `/pricing`, `/models`, `/thinking`).
  - Why it works: All four providers have verified, DOM-extractable HTML documentation (`_SOURCES/2026-10-28_Google-Pricing-DOM.json`, `_SOURCES/2026-10-28_Google-Models-DOM.json`) and `100%` Epoch ECI coverage for flagship/flash tiers (`IN04`).
  - Implication: Adds Google source group `G1`-`G3` to `update-model-registry.md` and the P3 recurring update template; adds current Gemini API models (and missing Sep/Oct 2026 Anthropic/OpenAI releases on next full registry run) while keeping the table compact (`~35` active models).
  - Why recommended: Closes the glaring Google Gemini API gap using DOM extraction rules already verified and saved in `_SOURCES/` during P1, without bloating the inventory with providers not configured in `.tools/.api-keys.txt`.
- **b) Seven+ providers: Anthropic, OpenAI, Google, Z.AI, plus xAI, DeepSeek, Mistral, Moonshot**
  - What: Add xAI (`grok-*`), DeepSeek (`deepseek-*`), Mistral, and Moonshot (`kimi-*`) API documentation scraping to `update-model-registry.md` and `MODEL_INVENTORY.md`.
  - Why it works: Broadens the inventory to every major frontier lab appearing on the Epoch ECI leaderboard.
  - Implication: Doubles the DOM scraping surface area in `update-model-registry.md` (from 4 to 8 providers), requires new unverified provider URLs, and pushes `MODEL_INVENTORY.md` over the 60-line Goal 3 target.
- **c) Keep current 3-provider scope (Anthropic, OpenAI, Z.AI only)**
  - What: Keep `MODEL_INVENTORY.md` and `update-model-registry.md` limited to Anthropic, OpenAI, and Z.AI.
  - Why it works: Zero new provider extraction rules in `update-model-registry.md`.
  - Implication: Leaves Google Gemini API models (`gemini-4-argon`, `gemini-3.8-flash`, `gemini-3.1-pro-preview`) completely absent from the general-purpose inventory despite Google being one of the Big 3 frontier labs (`IN04`).

Reply format: `DD-01 a, DD-02 c, DD-03 a, DD-04 a, DD-05 a`

## 6. Recommendations

### Immediate P3-P5 Execution Path (Pending ACTOR DD Reply)

- **Adopt the recommended decision set (`DD-01 a, DD-02 c, DD-03 a, DD-04 a, DD-05 a`)**:
  - Replace `YY-L` with `UC-1..5` + `ECI band` (`E135`..`E170`) + `Generation equivalent` (`DD-01 a`, `IN03`, `IN04`).
  - Drop `WF` columns and `USD per WF 1` from `MODEL_INVENTORY.md` and use fixed operational caps (`<= 1.0 HWH`, `<= 6` items, `<= 3` files, `<= 50%` context, plus `Notes` scope guard) in `PROMPTS_GUIDES.md` (`DD-02 c`, `IN05`)—or, if model-scaled HWH is preferred, use the 4-row ECI-band lookup (`DD-02 a`, `IN05`).
  - Drop `behavior_profile` (`27/28` `standard`) and record empirically observed quirks in `Notes` (`DD-03 a`, `IN03`, `IN04`).
  - Remove `Devin cost` and Section 3.2 Devin-only rows from `MODEL_INVENTORY.md`, keeping them in `windsurf-model-registry.json` (`DD-04 a`, `IN03`, `IN04`).
  - Include Anthropic, OpenAI, Google Gemini (`G1`-`G3`), and Z.AI in `update-model-registry.md` and the P3 recurring update template (`DD-05 a`, `IN04`).
- **Update redirected URLs in `update-model-registry.md` (`IN04`)**: Update `A1` → `https://platform.claude.com/docs/en/about-claude/pricing`, `A2`/`A3` → `https://platform.claude.com/docs/en/models/overview`, `O3` → `https://developers.openai.com/api/docs/models/compare`, and `Z3` → `https://docs.z.ai/api-reference/introduction`.

## 7. Limitations

- **Single-model in-session empirical ledger (`N=8` prompts on `glm-5.2` high)**: All Partition Observations recorded during `MDLINVNTRY` (`01-Audit` and `02-Sources`) ran on `glm-5.2` high; small `UC-4` models (`claude-haiku-4-5`, `gpt-5-mini`, `gpt-5.6-luna`) were not empirically run on multi-item prompt sequences during this session (`IN05`).
- **METR Time Horizons freeze (`2026-09-08`)**: Because METR ceased active updates on `2026-09-08` (`6/28` exact coverage), cross-checking ECI bands against measured human-hour horizons is limited to pre-September 2026 releases (`IN04`).
- **Epoch ECI minimum-4-benchmark gate**: Brand-new models require at least 4 evaluated benchmarks in Epoch's database before receiving an ECI score (`claude-mythos-5` is absent from `eci-leaderboard-general.csv`), requiring `UC` as a release-day fallback (`IN04`, `IN05`).

## 8. Document History

**[2026-10-28 20:22]**
- Initial Summary created with 3 topic files (`IN03`-`IN05`), 32 sources (`IN02`), 10 cross-document Key Findings (`KF-01`..`KF-10`), and design decisions `DD-01`..`DD-05` in Presenting Decisions format

