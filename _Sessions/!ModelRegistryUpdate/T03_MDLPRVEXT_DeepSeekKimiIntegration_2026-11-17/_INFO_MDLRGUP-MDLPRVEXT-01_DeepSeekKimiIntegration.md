# INFO: Integrating DeepSeek and Kimi (Moonshot) Models into the Model Inventory Update

**Doc ID**: MDLRGUP-MDLPRVEXT-IN01
**Goal**: Define what must change in `_PROMPTS_ModelInventoryUpdate_TEMPLATE.md` and its scripts so every callable DeepSeek and Kimi model is covered by the recurring update, with at most 10 prompts per file.
**Timeline**: Created 2026-11-17

**Depends on:**
- `_PROMPTS_ModelInventoryUpdate_TEMPLATE.md` (current 8-prompt template, 514 lines)
- `T02_MDLINVNTRY_ReliableModelInventory_2026-10-28\_SPEC_MDLRGUP-MDLINVNTRY-01_GenerationLadder.md [MDLRGUP-MDLINVNTRY-SP01]`

## Summary

- Scope on 2026-11-17: 2 DeepSeek models (`deepseek-flash`, `deepseek-v4-pro`) and 6 Kimi models (`kimi-k3.1-pro`, `kimi-k3.1-pro-highspeed`, `kimi-k3`, `kimi-k2.7-code`, `kimi-k2.7-code-highspeed`, `kimi-k2.6`). All 8 are OpenAI-compatible Chat Completions endpoints [VERIFIED]
- Epoch ECI has a score and 95% interval for 6 of the 8 (both highspeed variants have none; they tie to their base model) [VERIFIED]
- **Prompt budget fits**: template 8 prompts → 9 prompts (Prompt 2 split in two); generated instance 8 (FULL) or 7 (PRICES, NEWMODEL). Limit 10 is met with 1 prompt of headroom [VERIFIED by count]
- **Live API tests are blocked**: `e:\dev\.tools\.api-keys.txt` has no `DEEPSEEK_API_KEY` and no `MOONSHOT_API_KEY`; K3.1 Pro additionally needs a first top-up of 1 USD [VERIFIED]. Until then both providers stay `untested` (inventory shows `API untested`)
- The pipeline cannot onboard the two providers unchanged. Sandbox tests found 9 defects (`DF-01` to `DF-09`, Section 3.1); the 5 that stop or silently corrupt a run: provider detection exits in 4 LLM scripts, `match-epoch-eci.py` finds 0 of 5 new DeepSeek and Kimi IDs, alias names pick the wrong Epoch snapshot (156.70 instead of 159.41), `build_api_params` crashes on `max_output: null`, and `medium` effort is sent to a 3-value API [TESTED]
- Three data-model gaps need a decision: DeepSeek peak and off-peak prices (DD-17), rolling snapshot behind a fixed model ID (DD-18), and how many models "all" means (DD-16) [VERIFIED]
- Distribution to Lana-V1 is safe: Lana picks an adapter only for the provider of a configured role; an unknown registry provider is ignored until a role names it [VERIFIED by code read]
- `.md` page endpoints are not a shortcut: DeepSeek `.md` keeps its price table, Kimi `.md` returns empty `<table>` tags for both price tables; Playwright DOM extraction stays the method [TESTED]

## Table of Contents

1. [Scope: Callable Models on 2026-11-17](#1-scope-callable-models-on-2026-11-17)
2. [Test Results](#2-test-results)
3. [Required Changes by Component](#3-required-changes-by-component)
4. [Proposed Changes to the Prompts Template](#4-proposed-changes-to-the-prompts-template)
5. [Decisions](#5-decisions)
6. [Next Steps](#6-next-steps)
7. [Sources](#7-sources)
8. [Document History](#8-document-history)

## 1. Scope: Callable Models on 2026-11-17

### 1.1 DeepSeek

According to the [DeepSeek Models & Pricing page](https://api-docs.deepseek.com/quick_start/pricing) (`MDLRGUP-MDLPRVEXT-IN01-SC-DSEEK-PRCNG`):

- **`deepseek-flash`** serves snapshot `DeepSeek-V4.1-Flash-1017`. Released 2026-09-10, updated in place on 2026-10-17 (`MDLRGUP-MDLPRVEXT-IN01-SC-DSEEK-CHNGLG`). Vision supported
- **`deepseek-v4-pro`** serves snapshot `DeepSeek-V4-Pro-0813`. GA 2026-08-13; no vision
- Both: context length `1M` (printed that way, no exact token count), max output `384K`, thinking and non-thinking modes, JSON output, tool calls, Responses API, Anthropic API
- Base URLs: `https://api.deepseek.com` (OpenAI format), `https://api.deepseek.com/anthropic`. Env key name for the registry scripts: `DEEPSEEK_API_KEY` [ASSUMED, no key available to confirm]
- Legacy names `deepseek-v4-flash` and `deepseek-v4-flash-vision-exp` are still accepted and routed to `deepseek-flash` (billed at Flash price). `deepseek-chat` and `deepseek-reasoner` were discontinued on 2026-07-24. None of these four is registered: they are aliases, not models
- Prices per 1M tokens, peak hours (01:00-04:00 and 06:00-10:00 UTC, Monday to Friday, excluding Chinese public holidays); off-peak is exactly half:
  - `deepseek-flash`: input cache miss 0.30, cache hit 0.006, output 1.20
  - `deepseek-v4-pro`: input cache miss 1.32, cache hit 0.044, output 3.96
- Peak covers 35 of 168 weekly hours (20.8%) [derived]
- Effort: `reasoning_effort` `low` / `high` / `max` plus `thinking.type` `enabled` / `disabled` in `extra_body`; the server maps `minimal` to `low`, `medium` and `xhigh` to `high`, `ultra` to `max`; default `high` (`MDLRGUP-MDLPRVEXT-IN01-SC-DSEEK-THNKNG`)

### 1.2 Kimi (Moonshot)

According to the [Kimi Model Inference Pricing page](https://platform.kimi.ai/docs/pricing/chat) and the [Kimi Model List](https://platform.kimi.ai/docs/models) (`MDLRGUP-MDLPRVEXT-IN01-SC-KIMI-PRCNG`, `MDLRGUP-MDLPRVEXT-IN01-SC-KIMI-MDLLST`):

- **K3 series**, context stated once in prose above the table: 1,048,576 tokens. Prices per 1M tokens (input / cached input / output; cache write 5m and 1h also listed):
  - `kimi-k3.1-pro`: 2.00 / 0.20 / 10.00 (writes 2.00 and 4.00). "First model of the K3.1 series", post-trained version of K3, 1M context, native vision
  - `kimi-k3.1-pro-highspeed`: 4.00 / 0.20 / 20.00. "Same intelligence, about 2-3x the speed"
  - `kimi-k3`: 3.00 / 0.30 / 15.00. Previous-generation flagship
- **K2 series**, context stated once in prose: 262,144 tokens (the parameter reference prints "256K"). Since 2026-10-31 not available to new users; retirement planned for the end of December 2026:
  - `kimi-k2.7-code`: 0.95 / 0.19 / 4.00; `kimi-k2.7-code-highspeed`: 1.90 / 0.38 / 8.00; `kimi-k2.6`: 0.95 / 0.16 / 4.00
- Already retired (calls return 404, not registered): `kimi-k2.5`, all `moonshot-v1-*`, `kimi-k2-*` (0711, 0905, turbo, thinking), `kimi-latest`, `kimi-thinking-preview`
- Base URL `https://api.moonshot.ai/v1`; env key name `MOONSHOT_API_KEY` (named in the vendor quickstart). K3.1 Pro "unlocked after a successful top-up (minimum $1)"
- K3 series: `reasoning_effort` `low` / `high` / `max`, default `max`, thinking always on; `temperature`, `top_p`, `n`, penalties are fixed and must not be sent; `max_completion_tokens` default 131072, up to 1048576
- K2.7 Code and K2.6: no `reasoning_effort`; `thinking.type` `disabled` turns thinking off on K2.6 (`MDLRGUP-MDLPRVEXT-IN01-SC-KIMI-MDLPRM`)
- Batch API: 60% of standard price (not stored; `_pricing_tier` is `standard`)
- Release dates: the Kimi changelog gives months only (K3 July 2026, K2.7 Code June 2026, K2.6 April 2026; K3.1 Pro not listed); Epoch gives days (see 2.1)

### 1.3 Out of scope (flagged, see DD-16)

Open-weight models without an API on these vendors (for example DeepSeek-OCR-2, DeepSeek-V4-Pro-Preview, Kimi K2 Thinking checkpoints) are not callable through the keys file and are not registered. OCR models stay deferred per `MDLRGUP-PR-0006`.

## 2. Test Results

All tests ran in a sandbox copy (`_agentwork/.tmp_dsk_sandbox`, ignored by git) holding the canonical JSONs plus 8 draft registry entries, 3 draft prefix rows, and 8 draft pricing entries. No canonical file was changed. Test source ids: `MDLRGUP-MDLPRVEXT-IN01-SC-LOCAL-SNDBX`.

### 2.1 Epoch ECI matching (`match-epoch-eci.py`)

- Epoch CSV (256 rows, 2026-11-17) has 24 DeepSeek and Kimi rows (7 Kimi, 17 DeepSeek, including pre-2026 and preview snapshots). Day-level release dates are in the `date` column [VERIFIED]
- **New-model detection fails**: with the 5 IDs in a DOM extract, the unmodified script reports 0 new models; with `deepseek|kimi` added to `MODEL_ID_PATTERN` it reports all 5 [TESTED]
- **Alias-to-snapshot mismatch**: Epoch holds one row per snapshot. Name-based matching picked `DeepSeek V4.1 Flash` (156.70, 2026-09-09) instead of `DeepSeek V4.1 Flash 1017` (159.41, 2026-10-17) for `deepseek-flash`, and `DeepSeek-V4-Pro` (150.17, preview, 2026-04-24) instead of `DeepSeek V4 Pro 0813` (155.94) for `deepseek-v4-pro`. Two `ExplicitNameMap` entries fix it [TESTED]
- Kimi display names equal the Epoch names (`Kimi K3.1 Pro` 161.37 [158.99-164.00], `Kimi K3` 158.58, `Kimi K2.7 Code` 151.15, `Kimi K2.6` 151.56): direct match works. Highspeed variants have no row [TESTED]

### 2.2 Generation layering (`layer-generation-ladder.py`) and inventory

- Draft rungs after insert-only layering (with ECI from 2.1): `kimi-k3.1-pro` G08 (squeezed by `gpt-6.1-terra` G09), `kimi-k3` G08, `kimi-k3.1-pro-highspeed` G08, `deepseek-flash` G08, `deepseek-v4-pro` G07, K2 models G06; 0 cycles; Top rung stays G13 [TESTED]
- `point_version()` has no DeepSeek or Moonshot branch, so each model is its own point version. Rungs were identical with and without a patch in this snapshot; the difference appears only for unscored models (E5, E6). An ID regex cannot work for DeepSeek because `deepseek-flash` carries no version. A registry field `point_version` (`deepseek-4.1` for Flash, `deepseek-4` for Pro, derived from the vendor snapshot name) groups correctly and prevents a false E1 that would place Pro (UC-2) above Flash (UC-3) although ECI says the reverse (155.94 vs 159.41, intervals overlap). Kimi can use a regex (`kimi-k3.1-pro` → `kimi-3.1`) [TESTED patch, ASSUMED benefit]
- `update-model-inventory.py` prints `L M H X` for `kimi-k2.6`: method `thinking` is treated as Anthropic-style budgets for every provider except Z.AI. Kimi K2 and DeepSeek non-thinking are on/off only [TESTED]
- Gate 5 (prefix match), Gate 7 (method keys), Gate 9.4 (inventory vs registry vs pricing, 119 models) pass with the drafts and a regenerated inventory [TESTED]

### 2.3 LLM call scripts (`call-llm.py`)

- `detect_provider("deepseek-flash")` and `("kimi-k3.1-pro")` exit with `ERROR: Cannot detect provider` (xAI and Z.AI IDs work) [TESTED]. Same pattern in `call-llm-batch.py`, `find-workers-limit.py`, `evaluation/analyze-costs.py`; `test-call-llm.py` has no test list per provider
- `build_api_params` with a `kimi-k2` prefix row whose `max_output` is `null` raises `TypeError` (`output_factor * None`). With real numbers it works [TESTED]
- Effort `medium` stays `medium` for prefixes whose list is `low, high, max` (fallback map has no `medium` entry). DeepSeek maps it server-side to `high` (vendor page); for Kimi the vendor does not say. Z.AI's `medium` already returns HTTP 400 for the same list shape (registry note, 2026-09-26) [TESTED, Kimi 400 ASSUMED]
- Default output budget = `output_length` factor × `max_output`: 786,432 tokens for K3.1 Pro (medium) and 288,000 for DeepSeek. Kimi documents `max_completion_tokens`; whether `max_tokens` is accepted is unverified [ASSUMED]
- Request shapes captured against a local mock endpoint with the installed OpenAI SDK 3.49.0: top-level `reasoning_effort` and `max_completion_tokens` (Kimi K3); `reasoning_effort` plus `thinking` in the body through `extra_body` (DeepSeek); `thinking: {"type": "disabled"}` (Kimi K2.6, DeepSeek). Both real endpoints answer an invalid key with HTTP 401 JSON, so base URLs are correct [TESTED]
- Not tested: any authenticated call (no keys), actual HTTP 400 behavior of `medium` on Kimi, access of a new account to K2 models [BLOCKED]

### 2.4 Page extraction

- DeepSeek price table uses `rowspan`: the first price group (cache hit) sits in the row that also holds the `PRICING(2)` label. A reliable recipe reads the flat text of the `Model Details` section or the `.md` endpoint (`https://api-docs.deepseek.com/quick_start/pricing.md`, prices present) [TESTED]
- Kimi pricing page: the two tables read cleanly from the DOM (rows `Name | Input | Output | Cached Input | 5m writes | 1h writes`). The `.md` endpoint returns empty tables; its parameter reference page (`/docs/api/models-overview.md`) keeps a real Markdown table [TESTED]
- The footnote `(1)` on DeepSeek (alias routing) and the retirement notice on Kimi must be captured as text; they are not table cells [VERIFIED]

## 3. Required Changes by Component

Changes 3.1 and 3.2 are one-time implementation work in the session folder and `llm-tools` (not prompts). Section 4 covers the prompts template. Defect IDs `DF-nn` are used in Section 6.

### 3.1 Scripts

- **`DF-01` Provider detection** in `call-llm.py`, `call-llm-batch.py`, `find-workers-limit.py`, `evaluation/analyze-costs.py`: prefixes `deepseek-` → `deepseek`, `kimi-` → `moonshot`. Add `create_deepseek_client` (`https://api.deepseek.com`, `DEEPSEEK_API_KEY`) and `create_moonshot_client` (`https://api.moonshot.ai/v1`, `MOONSHOT_API_KEY`), both through the OpenAI SDK like Z.AI and xAI
- **`DF-02` Call path**: route both providers to Chat Completions (not the xAI default of the Responses API). New `call_openai_compatible` modeled on `call_zai`: DeepSeek sends `reasoning_effort` and `extra_body.thinking`; Kimi K3 sends top-level `reasoning_effort` and `max_completion_tokens` and never `temperature`; Kimi K2 sends `extra_body.thinking` only
- **`DF-03` Null `max_output`** crashes `build_api_params`: every prefix row needs an integer `max_output`; add a guard (`model_config.get('max_output') or 16384`) so a missing value cannot stop a run
- **`DF-04` Effort clamp**: add `medium` → `high` to `fallback_map` when `medium` is not in the registry list (matches the DeepSeek server mapping; avoids the Z.AI-style 400 on Kimi)
- **`DF-05` Output budget**: cap the default `max_tokens` at 131072 for providers `moonshot` and `deepseek` (Kimi K3 default; DeepSeek bills only used tokens). Final value after the first authenticated call
- **`DF-06` `match-epoch-eci.py`**: `MODEL_ID_PATTERN` gains `deepseek|kimi`; `ExplicitNameMap` gains `deepseek-flash` → `DeepSeek V4.1 Flash 1017`, `deepseek-v4-pro` → `DeepSeek V4 Pro 0813` (the map entry is updated whenever the vendor page `MODEL VERSION` changes; see DD-18)
- **`DF-07` `layer-generation-ladder.py`**: read optional registry `point_version` before the regex; add a `moonshot` regex branch. Run `test-layer-generation-ladder.py` after the change (8 cases)
- **`DF-08` `update-model-inventory.py`**: `efforts_for` returns `on/off` for method `thinking` with provider `moonshot` or `deepseek`, instead of `L M H X`; Notes show `off-peak half price` when pricing has `off_peak_factor`
- **`DF-09` `verify-and-distribute-registry.ps1` Gate 2** accepts any 4 DOM files, so a missing DeepSeek or Kimi extract passes (existing gap, now more likely with 7 providers): derive the expected file list from `[TARGET_PROVIDERS]` via a `-Providers` parameter
- `test-call-llm.py`: add `DEEPSEEK_TESTS` (flash at `low` and `max`, thinking off) and `MOONSHOT_TESTS` (K3.1 Pro at `low` and `max`, K2.6 thinking off); skip a provider when its key is missing, as for xAI

### 3.2 Data files

- `model-registry.json`: provider values `deepseek` and `moonshot` (vendor organization names in the Epoch CSV: `DeepSeek`, `Moonshot`). New optional fields `snapshot` (vendor `MODEL VERSION` string) and `point_version`. Three prefix rows (`deepseek-`, `kimi-k3`, `kimi-k2`) before the generic ones; every row with integer `max_input` and `max_output`. K2 models `status: "deprecated"` with `inventory_note: "retires end of 2026-12"`. Kimi release dates from the Epoch `date` column with `release_date_assumed: true` (vendor gives months only)
- `model-pricing.json`: new sections `deepseek` and `moonshot`; `deepseek` prices are peak prices plus `off_peak_factor: 0.5` (DD-17); Kimi cache write prices (5m, 1h) are not stored, as for Anthropic; `sources` gains the two vendor pricing URLs. `context_window_k` = `round(context_window / 1000)`
- `model-parameter-mapping.json`: unchanged (Gate 7 passes with the existing method keys)
- `MODEL_INVENTORY.md`: regenerated by the script; 8 new rows; no manual edit; Top rung unchanged at G13
- Side finding, not caused by this work: `model-pricing.json` `context_window_k` was not updated by the `MDLRGUP-PR-0008` fix (for example `gpt-5` pricing 256 vs registry 400000, `gpt-5.4-mini` 272 vs 400000). No gate compares the two fields. Proposed as new problem entry and as an extra check in Gate 5.2 [VERIFIED by file read]

### 3.3 Environment

- Keys: `DEEPSEEK_API_KEY`, `MOONSHOT_API_KEY` in `[KEYS_FILE]`; first top-up of at least 1 USD on Kimi; `SETUP.md` and `SKILL.md` of `llm-tools` list the two names
- K2 models: a new Kimi account may be refused on K2 (accounts registered before 2026-11-01 only; exact status code unknown); the existing Gate 8 rule sets `no_access` for 401 and 403, so add 404 to it
- `OPENROUTER_API_KEY` exists but is not a substitute: model IDs, limits, and prices differ from the first-party pages that define the registry [ASSUMED]

## 4. Proposed Changes to the Prompts Template

### 4.1 Prompt map (9 prompts in the template, at most 8 in a generated instance)

Reason for the split: Prompt 2 has 7 items today (limit 7 per prompt, `PRMT-SC-07`); DeepSeek and Kimi add 6 extraction items. One prompt with 13 items breaks the limit; two prompts of 5 items each keep it.

```text
Today (8)                          Proposed (9)
┌──────────────────────────┐       ┌──────────────────────────────────────────┐
│ 1 Bootstrap              │       │ 1 Bootstrap                              │
│ 2 Gate 1 + DOM (5 vendors)│ ───>  │ 2 Gate 1 + DOM part A: Anthropic, OpenAI,│
│                          │       │   Google                        (5 items)│
│                          │       │ 3 DOM part B: Z.AI, xAI, DeepSeek,       │
│                          │       │   Moonshot + Gate 2             (5 items)│
│ 3 Screenshots (FULL)     │       │ 4 Screenshots (FULL only)                │
│ 4 Capability evidence    │       │ 5 Capability evidence                    │
│ 5 JSON updates + Gates   │       │ 6 JSON updates + Gates 5-7               │
│ 6 Tests + ladder + report│       │ 7 Tests + ladder + inventory + report    │
│ 7 Distribution           │       │ 8 Distribution                           │
│ 8 Final checkpoint       │       │ 9 Final checkpoint                       │
└──────────────────────────┘       └──────────────────────────────────────────┘
Instance (Bootstrap excluded):  FULL 8, PRICES 7, NEWMODEL 7 (fewer when a DOM part has no target provider)
```

Instantiation rules added: a DOM part whose providers are all outside `[TARGET_PROVIDERS]` is removed; `[TOTAL_PROMPTS]` becomes `08` (FULL), `07` (PRICES, NEWMODEL).

### 4.2 Edits by template location

Line numbers and prompt numbers in this list refer to the current template; from current Prompt 3 on, the new number is the current number plus 1 (Section 4.1). Section 4.3 uses new numbers.

- **L19-21 run modes, L73 `[TOTAL_PROMPTS]`, L78-91 load table and conditional prompts, all Prompt Markers `[ NN / 08 ]`**: renumber to the map above; Prompt 2 and 3 entries describe parts A and B
- **L28-32 run folder structure**: add `[DATE]_DeepSeek-Pricing-DOM.json`, `[DATE]_DeepSeek-Models-DOM.json` (D1-D3) and `[DATE]_Moonshot-Pricing-DOM.json`, `[DATE]_Moonshot-Models-DOM.json` (M1-M3)
- **L40-45 session scripts list**: `match-epoch-eci.py` (alias map, new patterns), `layer-generation-ladder.py` (`point_version` field), `update-model-inventory.py` (on/off effort cell), `verify-and-distribute-registry.ps1` (`-Providers` for Gate 2) are described with the changes of 3.1
- **L48-53 Field semantics**: add three lines
  - `context_window` printed as a rounded value (`1M`, `256K`) while another vendor page prints the exact token count: use the exact count and record both pages; DeepSeek prints only `1M`, so `1000000` is the value and `contextUnverified` stays empty
  - Prices with time-of-day tiers (DeepSeek peak and off-peak): `input_per_1m`, `cached_per_1m`, `output_per_1m` hold the peak price; `off_peak_factor` holds the ratio; the extraction file keeps both
  - A model ID that is a rolling alias (`deepseek-flash`): `snapshot` holds the vendor `MODEL VERSION`; a changed `snapshot` is a reported event (RunReport Section 4), `generation` is never changed
- **L69 and L133 `[TARGET_PROVIDERS]` default**: `Anthropic, OpenAI, Google, Z.AI, xAI, DeepSeek, Moonshot`
- **L135 screenshot subfolders (FULL)**: add `DeepSeek-Pricing`, `Moonshot-Pricing`, `Moonshot-Models`; **L221** capture list adds `D1`, `M1`, `M2`
- **L172, L176, L184 (Prompt 2 reads and Gate 2 call)**: Gate 1 and Anthropic, OpenAI, Google stay in part A; Gate 2 call adds `-Providers "[TARGET_PROVIDERS]"` and sits in part B
- **L259-268 Prompt 4 (capability evidence)**: three additions
  - Epoch row choice for a rolling alias: match the Epoch row whose name carries the registry `snapshot` (`deepseek-flash` with `DeepSeek-V4.1-Flash-1017` → `DeepSeek V4.1 Flash 1017`)
  - Release date: when the vendor gives only a month, use the Epoch `date` and set `release_date_assumed: true`
  - A vendor benchmark comparison with another vendor's model (K3.1 Pro "ahead of GPT-6 Astra on Terminal-Bench 4.0") is not model-selection guidance and creates no E1 edge; a statement that the successor is a post-trained version of the predecessor ("K3.1 Pro is a post-trained version of Kimi K3") is an EC-2 case (E2, no new edge item)
- **L304-308 Prompt 5 (JSON updates)**: item 2 adds `snapshot`, `point_version`, provider values, prefix rows with integer `max_output`; item 3 adds `off_peak_factor` and the two `sources` URLs; Gate 5.2 `contextChecks` covers all 8 new models (every one has a printed window)
- **L344 Prompt 6 (tests; new Prompt 7)**: `DEEPSEEK_API_KEY`, `MOONSHOT_API_KEY` check first; a missing key is reported as `API untested` (not a failure) and listed in RunReport Section 7; K2 models: 401, 403, or 404 → `status: "no_access"`, `enabled: false`
- **L426 Prompt 8 spot check** (now Prompt 9): the rule "3 models per provider NOT in `contextChecks`" selects nothing for DeepSeek (2 models) and Moonshot (6 models) once the JSON update prompt checked them. New rule: per provider take up to 3 models not in `contextChecks`; when fewer exist, fill to 3 (or all) with models whose prices and `max_output` were not re-read on a second source in this run

### 4.3 New extraction items for Prompt 3 (DOM part B), ready to paste

Part B items: 1 Z.AI (unchanged text of today's item 5), 2 xAI (today's item 6), 3 DeepSeek, 4 Moonshot, 5 close Playwright and run Gate 2.

3. Extract DeepSeek data: `D1` (`https://api-docs.deepseek.com/quick_start/pricing`, flat text of the `Model Details` section or the `.md` endpoint; capture API names with footnote `(1)` alias text, `MODEL VERSION`, context, max output, features, PEAK and OFF-PEAK prices for cache hit, cache miss, output, and the footnote with the peak hours) into `[RUN_FOLDER]\[DATE]_DeepSeek-Pricing-DOM.json`; `D2` (`https://api-docs.deepseek.com/updates`, newest entries until every registered DeepSeek model has a release date; record legacy name status) and `D3` (`https://api-docs.deepseek.com/guides/thinking_mode`, effort values and mapping table) into `[RUN_FOLDER]\[DATE]_DeepSeek-Models-DOM.json`
4. Extract Moonshot data: `M1` (`https://platform.kimi.ai/docs/pricing/chat`, both tables from the DOM plus the prose line above each table with the series context window and the K2 retirement notice) into `[RUN_FOLDER]\[DATE]_Moonshot-Pricing-DOM.json`; `M2` (`https://platform.kimi.ai/docs/models`, available and deprecated model tables; `https://platform.kimi.ai/docs/platform-changelog.md` release months) and `M3` (`https://platform.kimi.ai/docs/api/models-overview.md`, parameter table: `reasoning_effort`, `thinking`, fixed `temperature`) into `[RUN_FOLDER]\[DATE]_Moonshot-Models-DOM.json`. Do not use the `.md` endpoint of M1: its tables are empty

## 5. Decisions

Engineering choices made without asking (no user-visible trade-off): provider ids `deepseek` and `moonshot`; Chat Completions for both; cache write prices not stored; `context_window_k` rounding; `snapshot` and `point_version` as optional registry fields.

# DD-16: Which models count as "all DeepSeek and Kimi models"?

**Problem**: The vendors list callable models, retired models, and open-weight checkpoints; the inventory must state a boundary
**Context**: Registry rule today: every non-retired text model is listed, retired models are never added; `MDLRGUP-PR-0006` defers OCR models
**Review**: `_Sessions/!ModelRegistryUpdate/T03_MDLPRVEXT_DeepSeekKimiIntegration_2026-11-17/_INFO_MDLRGUP-MDLPRVEXT-01_DeepSeekKimiIntegration.md` section 1

**Options**
- **1) Callable on 2026-11-17, including K2 until retired** (recommended)
  - What: 8 models (2 DeepSeek, 6 Kimi); K2 models as `deprecated`
  - Why it works: matches what the keys can call and what vendor pricing pages list; same rule as the other providers
  - Implication: K2 rows disappear (status `retired`) after the end-of-2026-12 shutdown
  - Why recommended: smallest set that is fully verifiable from vendor pages
- **2) Option 1 plus retired API models** (`kimi-k2.5`, `kimi-k2-thinking`, `moonshot-v1-*`, `deepseek-v3.2`, `deepseek-r1`)
  - What: about 20 more rows with Epoch scores
  - Why it works: gives rung anchors for older models
  - Implication: rows can never be tested (404), no vendor price page; breaks "sourced field re-read" rule
- **3) Option 1 plus open-weight-only models** (DeepSeek-OCR-2, V4-Pro-Preview)
  - What: rows without an API endpoint
  - Implication: no test, price, or context source; contradicts the registry purpose (callable models)

# DD-17: Which DeepSeek price goes into `input_per_1m`, `cached_per_1m`, `output_per_1m`?

**Problem**: DeepSeek charges by time of day; the schema has one price per token type
**Context**: Peak (20.8% of weekly hours) is twice the off-peak price; Gate 9.4 compares inventory prices to these fields exactly
**Review**: same file, sections 1.1 and 3.2

**Options**
- **1) Peak price plus `off_peak_factor: 0.5`** (recommended)
  - What: `deepseek-flash` 0.30 / 0.006 / 1.20; inventory Notes says `off-peak half price`
  - Why it works: planning cost is an upper bound; no schema change for readers that ignore the new field
  - Implication: cost tools show up to 2x the real cost for off-peak work
  - Why recommended: safe for budgets and keeps Gate 9.4 unchanged
- **2) Off-peak price plus `peak_factor: 2`**
  - What: 0.15 / 0.003 / 0.60
  - Implication: understates cost for 20.8% of hours; budgets can be exceeded
- **3) Weekly blend** (0.18 for `deepseek-flash` input: 20.8% peak, 79.2% off-peak)
  - Implication: matches neither page value; Gate 5.2-style checks cannot compare it to a vendor number

# DD-18: How does the registry treat a model ID that changes its snapshot (`deepseek-flash`)?

**Problem**: `deepseek-flash` moved from `V4.1-Flash` (ECI 156.70) to `V4.1-Flash-1017` (159.41) without an ID change; `generation` is write-once
**Context**: Generation invariants (`MDLRGUP-MDLINVNTRY-IG-01`); callers can only use the alias
**Review**: same file, section 2.1

**Options**
- **1) One entry per API ID with `snapshot` and `epoch_name`; a snapshot change refreshes `eci_*` and is reported, `generation` stays** (recommended)
  - What: registry mirrors what callers can call
  - Why it works: no uncallable rows; the run report lists the change for a human decision
  - Implication: the rung can understate an improved alias until a rung-change rule exists
  - Why recommended: smallest change; matches the append-only rule
- **2) One entry per snapshot** (`deepseek-flash-1017`)
  - Implication: rows cannot be called; tests and prices have no distinct endpoint
- **3) Allow `generation` to move for rolling aliases only**
  - Implication: breaks IG-01 and Gate 9.4 for one provider

# DD-19: How are 7 providers fitted into the 10-prompt limit?

**Problem**: One DOM prompt would hold 13 items
**Context**: `PRMT-SC-07` allows 7 items per prompt; limit requested: 10 prompts per file
**Review**: same file, section 4.1

**Options**
- **1) Split Prompt 2 into DOM part A and part B** (recommended)
  - What: template 9 prompts, instance 8 (FULL) or 7
  - Why it works: 5 items each; 1 prompt of headroom
  - Why recommended: respects the load rule with minimal change
- **2) Keep one Prompt 2 with 13 items**
  - Implication: violates the 7-item rule; failures cost a full re-run of all vendors
- **3) Move DeepSeek and Moonshot to a separate prompts file**
  - Implication: two files per run, two Bootstrap steps, more state to keep consistent

Reply format: `DD-16 1, DD-17 1, DD-18 1, DD-19 1`

## 6. Next Steps

1. Confirm DD-16 to DD-19 (or answer `all 1`)
2. Add `DEEPSEEK_API_KEY`, `MOONSHOT_API_KEY` to `[KEYS_FILE]`; top up Kimi by at least 1 USD (blocker for live tests only)
3. Implement `DF-01` to `DF-09` in session scripts and `llm-tools` (`/implement`); run `test-layer-generation-ladder.py`, `llm-tools-selftest.py`, and the sandbox test again against the real files
4. Edit `_PROMPTS_ModelInventoryUpdate_TEMPLATE.md` per Section 4 (`/write-prompts` rules, prompt count 9)
5. First run mode `NEWMODEL` with `[TARGET_PROVIDERS] = DeepSeek, Moonshot`; commit the registry before the run (Gate 9.4 reads git HEAD)
6. Record new problem `MDLRGUP-PR-0009`: pricing `context_window_k` drift vs registry (Section 3.2 side finding)

## 7. Sources

**Primary Sources:**
- `MDLRGUP-MDLPRVEXT-IN01-SC-DSEEK-PRCNG`: https://api-docs.deepseek.com/quick_start/pricing - models, snapshots, peak and off-peak prices, alias footnote [VERIFIED 2026-11-17]
- `MDLRGUP-MDLPRVEXT-IN01-SC-DSEEK-CHNGLG`: https://api-docs.deepseek.com/updates - release dates, retired names [VERIFIED 2026-11-17]
- `MDLRGUP-MDLPRVEXT-IN01-SC-DSEEK-THNKNG`: https://api-docs.deepseek.com/guides/thinking_mode - effort values, mapping [VERIFIED 2026-11-17]
- `MDLRGUP-MDLPRVEXT-IN01-SC-KIMI-PRCNG`: https://platform.kimi.ai/docs/pricing/chat - K3 and K2 prices, context per series, K2 retirement [VERIFIED 2026-11-17]
- `MDLRGUP-MDLPRVEXT-IN01-SC-KIMI-MDLLST`: https://platform.kimi.ai/docs/models - available and deprecated models [VERIFIED 2026-11-17]
- `MDLRGUP-MDLPRVEXT-IN01-SC-KIMI-MDLPRM`: https://platform.kimi.ai/docs/api/models-overview.md - parameter constraints per series [VERIFIED 2026-11-17]
- `MDLRGUP-MDLPRVEXT-IN01-SC-KIMI-CHNGLG`: https://platform.kimi.ai/docs/platform-changelog.md - release months [VERIFIED 2026-11-17]
- `MDLRGUP-MDLPRVEXT-IN01-SC-KIMI-K31PRO`: https://platform.kimi.ai/docs/guide/kimi-k3-1-pro-quickstart - K3.1 Pro limits, top-up requirement, base URL [VERIFIED 2026-11-17]
- `MDLRGUP-MDLPRVEXT-IN01-SC-EPOCH-ECI`: https://epoch.ai/data/eci_scores.csv - 256 rows, 24 DeepSeek and Kimi [VERIFIED 2026-11-17]
- `MDLRGUP-MDLPRVEXT-IN01-SC-LOCAL-SNDBX`: sandbox scripts in `_agentwork/` of this session (deleted by `/cleanup`) - provider, matcher, layering, inventory, gate, and request-shape tests [TESTED]
- `MDLRGUP-MDLPRVEXT-IN01-SC-LOCAL-LANA`: `e:\Dev\Lana-V1\src\lana\providers\__init__.py`, `config.py` - adapter selection by role provider [VERIFIED]

## 8. Document History

**[2026-11-17 15:10]**
- Initial research document created (DeepSeek and Kimi integration into the model inventory update)




