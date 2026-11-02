# Model Registry Update Run Report (2026-10-28 PRICES)

**Doc ID**: MDLRGUP-20261028-REPORT
**Goal**: Summary report for the `2026-10-28` `PRICES` model inventory update run across Anthropic, OpenAI, Google Gemini, and Z.AI
**Run Folder**: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES`

## Table of Contents

- [1. Added Models](#1-added-models)
- [2. Price Changes](#2-price-changes)
- [3. Unchanged](#3-unchanged)
- [4. Registry Additions](#4-registry-additions)
- [5. Prefix Gaps](#5-prefix-gaps)
- [6. Parameter Mapping](#6-parameter-mapping)
- [7. Test Results](#7-test-results)
- [8. Long Context](#8-long-context)
- [9. Pending Resolution](#9-pending-resolution)
- [10. Sources Archived](#10-sources-archived)
- [11. MODEL_INVENTORY.md Changes](#11-model_inventorymd-changes)
- [12. Phase 9 Distribution and Gate 9 Sync Check](#12-phase-9-distribution-and-gate-9-sync-check)
- [Document History](#document-history)

## 1. Added Models

23 models added across `model-pricing.json` and `model-registry.json`:

- **OpenAI (6)**:
  - `openai/gpt-6.1-sol`: `$2.00` input, `$0.10` cached, `$10.00` output (long context: `$4.00 / $0.20 / $20.00`), `context_window_k: 1050` (`E170`, `168.37`)
  - `openai/gpt-6.1-terra`: `$1.00` input, `$0.05` cached, `$5.00` output (long context: `$2.00 / $0.10 / $10.00`), `context_window_k: 1050` (`UC-3 Balanced`)
  - `openai/gpt-6-sol`: `$2.00` input, `$0.20` cached, `$10.00` output (long context: `$4.00 / $0.40 / $20.00`), `context_window_k: 1050` (`E165`, `163.73`)
  - `openai/gpt-6-luna`: `$0.10` input, `$0.01` cached, `$0.50` output (long context: `$0.20 / $0.02 / $1.00`), `context_window_k: 1050` (`E155`, `156.75`)
  - `openai/gpt-5.5-cyber`: `$12.50` input, `$1.25` cached, `$75.00` output, `context_window_k: null` (`UC-1 Apex`)
  - `openai/gpt-5.3-codex`: `$1.75` input, `$0.175` cached, `$14.00` output (long context: `$3.50 / $0.35 / $28.00`), `context_window_k: null` (`E155`, `157.09`)
- **Anthropic (5)**:
  - `anthropic/claude-fable-5-1`: `$10.00` input, `$0.25` cached, `$50.00` output, `context_window_k: 1000` (`E165`, `166.49`)
  - `anthropic/claude-mythos-5-1`: `$10.00` input, `$0.25` cached, `$50.00` output, `context_window_k: 1000` (`UC-1 Apex`, limited availability)
  - `anthropic/claude-opus-5-5`: `$4.00` input, `$0.20` cached, `$20.00` output, `context_window_k: 1000` (`E170`, `168.83`)
  - `anthropic/claude-sonnet-5-5`: `$2.00` input, `$0.10` cached, `$10.00` output, `context_window_k: 1000` (`E165`, `166.18`)
  - `anthropic/claude-haiku-5-5`: `$0.10` input, `$0.01` cached, `$0.50` output (`<=100k`; long context `>100k`: `$0.50 / $0.05 / $2.50`), `context_window_k: 1000` (`E160`, `159.32`)
- **Google Gemini (10)**:
  - `google/gemini-4-argon`: `$2.00` input, `$0.10` cached, `$10.00` output (through `2026-11-30`; `$4.00 / $0.20 / $20.00` starting `2026-12-01`), `context_window_k: 1048` (`E165`, `166.45`)
  - `google/gemini-3.8-flash`: `$0.75` input, `$0.075` cached, `$3.75` output (through `2026-12-31`; `$1.50 / $0.15 / $7.50` starting `2027-01-01`), `context_window_k: 1048` (`E155`, `157.44`)
  - `google/gemini-3.6-flash`: `$0.75` input, `$0.075` cached, `$3.75` output, `context_window_k: 1048` (`E155`, `154.53`)
  - `google/gemini-3.5-flash-lite`: `$0.30` input, `$0.03` cached, `$2.50` output, `context_window_k: 1048` (`E145`, `144.91`)
  - `google/gemini-3.1-flash-lite`: `$0.25` input, `$0.025` cached, `$1.50` output, `context_window_k: 1048` (`E145`, `144.26`)
  - `google/gemini-3.1-pro-preview`: `$2.00` input, `$0.20` cached, `$12.00` output (`<=200k`; long context `>200k`: `$4.00 / $0.40 / $18.00`), `context_window_k: 1048` (`E155`, `155.34`)
  - `google/gemini-3-flash-preview`: `$0.50` input, `$0.05` cached, `$3.00` output, `context_window_k: 1048` (`E150`, `151.88`)
  - `google/gemini-2.5-pro`: `$1.25` input, `$0.125` cached, `$10.00` output (`<=200k`; long context `>200k`: `$2.50 / $0.25 / $15.00`), `context_window_k: 1048` (`E145`, `145.13`)
  - `google/gemini-2.5-flash`: `$0.30` input, `$0.03` cached, `$2.50` output, `context_window_k: 1048` (`E145`, `142.90`)
  - `google/gemini-2.5-flash-lite`: `$0.10` input, `$0.01` cached, `$0.40` output, `context_window_k: 1048` (`E135`, `133.82`)
- **Z.AI (2)**:
  - `zai/glm-5.3-flashx`: `$0.37` input, `$0.075` cached, `$1.25` output, `context_window_k: 1000` (`UC-3 Balanced`)
  - `zai/glm-5.3-flashx-legal`: `$0.37` input, `$0.075` cached, `$1.25` output, `context_window_k: 1000` (`UC-3 Balanced`)

## 2. Price Changes

12 existing models had standard or long-context price updates:

- **`claude-sonnet-5`**: Standard input `$3.00 → $2.00`, cached `$0.30 → $0.20`, output `$15.00 → $10.00`
- **`gpt-6-astra`**: `long_context.output_per_1m` `$75.00 → $100.00`
- **`gpt-5.6-sol`**: `long_context.output_per_1m` `$30.00 → $40.00`
- **`gpt-5.6-terra`**: `long_context.output_per_1m` `$18.00 → $24.00`
- **`gpt-5.6-luna`**: `long_context.output_per_1m` `$1.80 → $2.40`
- **`gpt-5.5`**: `long_context` `$10.00 / $1.00 / $45.00 → $12.50 / $1.25 / $75.00`
- **`gpt-5.4`**: `long_context.output_per_1m` `$22.50 → $30.00`
- **`gpt-5.4-mini`**: Added `long_context` `$1.50 / $0.15 / $9.00`
- **`gpt-5.2`**: Added `long_context` `$3.50 / $0.35 / $28.00`
- **`gpt-5.1`**: Added `long_context` `$2.50 / $0.25 / $20.00`
- **`gpt-5`**: Added `long_context` `$2.50 / $0.25 / $20.00`
- **`gpt-5-mini`**: Added `long_context` `$0.45 / $0.045 / $3.60`

## 3. Unchanged

- **57** existing models in `model-pricing.json` had no price changes.

## 4. Registry Additions

- **23 models added** to `model-registry.json` (`_version: "1.10.1"`, `_updated: "2026-10-28"`):
  - 22 models added with `"enabled": false, "status": "untested"`
  - 1 model (`claude-mythos-5-1`) added with `"enabled": false, "status": "no_access"` (limited availability)
- **Status update (1)**: `claude-sonnet-4-5-20250929` updated from `"enabled": true, "status": "available"` to `"enabled": false, "status": "deprecated"` (deprecated `2026-09-30` on `A4`, retires `2026-11-30`).
- **Context window backfills (7)**: `gpt-5.2`, `gpt-5.1`, `gpt-5`, `gpt-5-mini`, `gpt-5.2-pro`, `gpt-5-pro` (`null → 256000`), and `gpt-5-nano` (`null → 128000`).
- **Capability enrichment**: All 92 models in `model-registry.json` enriched with `uc_class`, `eci_band`, `eci_score`, and `gen_equivalent` from `2026-10-28_Epoch-ECI-Match.json`.

## 5. Prefix Gaps

- **`claude-haiku-5`**: Added `claude-haiku-5` prefix (`adaptive_thinking`, `max_input: 1000000`, `max_output: 128000`, `effort: ["low", "medium", "high", "xhigh", "max"]`) so `claude-haiku-5-5` does not fall through to the legacy `claude-` temperature fallback (`200k / 4096`).
- **`gemini-*` (Google Gemini)**: Added 5 prefix entries (`gemini-3.6-flash`, `gemini-3.5-flash-lite`, `gemini-3.1-flash-lite`, `gemini-3-flash` with `minimal..high`, and `gemini-` with `low..high`, `max_input: 1048576`, `max_output: 65536`).
- **`gpt-5.3-codex`**: Matches `gpt-5` prefix (`minimal..high`); flagged for review if `xhigh` is enabled later.

## 6. Parameter Mapping

- **No changes needed** in `model-parameter-mapping.json` (`2.4.0`, `2026-09-05`). Gate 7 passed across all 5 methods (`adaptive_thinking`, `effort`, `reasoning_effort`, `temperature`, `thinking`).

## 7. Test Results

- **Phase 8 (`$newEnabledModels`)**: `0` newly added models had `enabled: true` after Phase 5.1 (per Phase 5.1 Rule 1, new models start as `enabled: false, status: "untested"`).
- **`test-call-llm.py` updates**: Added minimal test entries for `gpt-6.1-sol`, `gpt-6.1-terra`, `gpt-6-sol`, `gpt-6-luna`, `claude-fable-5-1`, `claude-opus-5-5`, `claude-sonnet-5-5`, `claude-haiku-5-5`, and `glm-5.3-flashx` so any model enabled in the future can be tested immediately via `--model <id>`. Gate 8 passed with exit code 0.

## 8. Long Context

- **Added `long_context` tier (12 models)**:
  - OpenAI (`threshold_k: null`, `>272k` on pricing page): `gpt-6.1-sol`, `gpt-6.1-terra`, `gpt-6-sol`, `gpt-6-luna`, `gpt-5.3-codex`, `gpt-5.4-mini`, `gpt-5.2`, `gpt-5.1`, `gpt-5`, `gpt-5-mini`
  - Anthropic (`threshold_k: 100`): `claude-haiku-5-5` (`$0.50 / $0.05 / $2.50` over 100k tokens)
  - Google Gemini (`threshold_k: 200`): `gemini-3.1-pro-preview` (`$4.00 / $0.40 / $18.00`), `gemini-2.5-pro` (`$2.50 / $0.25 / $15.00`)
- **Updated `long_context` tier (6 models)**: `gpt-6-astra`, `gpt-5.6-sol`, `gpt-5.6-terra`, `gpt-5.6-luna`, `gpt-5.5`, `gpt-5.4`

## 9. Pending Resolution

- **OpenAI `threshold_k`**: Set to `null` in `model-pricing.json` per Phase 6 Rule 6 (OpenAI pricing page heading notes `<=272k` / `>272k` context).
- **Scheduled Google price increases**: `gemini-4-argon` (`$2/$10` through `2026-11-30` → `$4/$20` starting `2026-12-01`) and `gemini-3.8-flash` / `gemini-3.6-flash` (`$0.75/$3.75` through `2026-12-31` → `$1.50/$7.50` starting `2027-01-01`).
- **Models awaiting `>= 4` Epoch benchmarks (`eci_band: null`)**: `gpt-6.1-terra`, `gpt-5.5-cyber`, `claude-mythos-5-1`, `glm-5.3-flashx`, `glm-5.3-flashx-legal`.

## 10. Sources Archived

Saved in `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\`:

- `2026-10-28_Anthropic-Pricing-DOM.json`
- `2026-10-28_Anthropic-ModelIDs-DOM.json`
- `2026-10-28_OpenAI-Standard-DOM.json`
- `2026-10-28_OpenAI-Batch-DOM.json`
- `2026-10-28_OpenAI-Compare-DOM.json`
- `2026-10-28_Google-Pricing-DOM.json`
- `2026-10-28_Google-Models-DOM.json`
- `2026-10-28_ZAI-Pricing-DOM.json`
- `2026-10-28_ZAI-Models-DOM.json`
- `2026-10-28_eci-leaderboard.csv`
- `2026-10-28_Epoch-ECI-Match.json`
- `2026-10-28_ChangeSet.json`
- `2026-10-28_RunReport.md`

## 11. MODEL_INVENTORY.md Changes

- **Sources header updated**: `model-registry.json` `1.10.1 (2026-10-28)`, `model-pricing.json` `(2026-10-28)`.
- **Section 3.1 rows added (21)**: `claude-opus-5-5`, `gpt-6.1-sol`, `claude-fable-5-1`, `gemini-4-argon`, `claude-sonnet-5-5`, `gpt-6-sol`, `claude-haiku-5-5`, `gemini-3.8-flash`, `gpt-5.3-codex`, `gemini-3.1-pro-preview`, `gpt-6.1-terra`, `gpt-6-luna`, `gemini-3.6-flash`, `glm-5.3-flashx`, `glm-5.3-flashx-legal`, `gemini-3.5-flash-lite`, `gemini-3.1-flash-lite`, `gemini-3-flash-preview`, `gemini-2.5-pro`, `gemini-2.5-flash`, `gemini-2.5-flash-lite` (growing Section 3.1 from 28 to 50 rows, all annotated with `UC-1..4` and `ECI band`).
- **Section 3.1 price recomputed (1)**: `claude-sonnet-5` `USD per WF 1` updated from `5.40` to `3.60`.
- **Section 3.2 Devin-only rows graduated to Section 3.1 (5)**: `GPT-5.3-Codex`, `Gemini 3.1 Pro`, `Gemini 3.6 Flash`, `Gemini 2.5 Pro`, and `Gemini 3 Flash` moved from Section 3.2 to Section 3.1 now that their API registry entries exist (leaving 4 Devin-only rows in Section 3.2: `Kimi K3`, `Gemini 3.5 Flash`, `Gemini 3.7 Flash`, `SWE-1.7`).
- **Gate 9.4**: **PASS** (`50/50` Section 3.1 rows verified against `model-registry.json`).

## 12. Phase 9 Distribution and Gate 9 Sync Check

- **Phase 9.1 (Agent folder)**: Synced `model-pricing.json`, `model-registry.json`, `model-parameter-mapping.json`, and `test-call-llm.py` to `e:\dev\IPPS\.devin\skills\llm-evaluation\`, and `MODEL_INVENTORY.md` to `e:\dev\IPPS\.devin\skills\write-documents\MODEL_INVENTORY.md`.
- **Phase 9.2 (Dependent skills)**: Synced `model-pricing.json`, `model-registry.json`, and `model-parameter-mapping.json` to `e:\dev\IPPS\PromptSystemV4.5\skills\llm-transcription\` and `e:\dev\IPPS\.devin\skills\llm-transcription\`.
- **Phase 9.3 (External config targets)**: Phase 9.3 skipped (external distribution not confirmed).
- **Gate 9 (SHA-256 Sync Check)**: **PASS** (`10/10` synced files verified identical by SHA-256 hash: 9 JSON copies across 3 target folders + `MODEL_INVENTORY.md` mirror in `.devin`).

## Document History

**[2026-10-28 23:45]**
- Added: Section 12 Phase 9 Distribution and Gate 9 Sync Check (`Phase 9.3 skipped`, `10/10` SHA-256 matches verified)

**[2026-10-28 23:42]**
- Added: Initial run report for `2026-10-28 PRICES` across Anthropic, OpenAI, Google Gemini, and Z.AI
