# Model Registry Update Run Report (2026-11-02 PRICES)

**Doc ID**: MDLRGUP-20261102-REPORT
**Goal**: Summary report for the `2026-11-02` `PRICES` model inventory update run across Anthropic, OpenAI, Google Gemini, Z.AI, and xAI
**Run Folder**: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-11-02_PRICES`

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
- [12. Depth Ladder](#12-depth-ladder)
- [13. Phase 9 Distribution and Gate 9 Sync Check](#13-phase-9-distribution-and-gate-9-sync-check)
- [Document History](#document-history)

## 1. Added Models

14 models added across `model-pricing.json` and `model-registry.json`:

- **OpenAI (8)**:
  - `openai/gpt-6-rosalind`: `$15.00` input, `$1.50` cached, `$75.00` output, `context_window_k: 1050` (`UC-1 Apex`, `D12`, `E1m > gpt-6-astra`)
  - `openai/gpt-rosalind-discovery`: `$5.00` input, `$0.50` cached, `$25.00` output, `context_window_k: 1050` (`UC-1 Apex`, `D11`, `E2 >= gpt-6-astra`)
  - `openai/gpt-rosalind-research`: `$5.00` input, `$0.50` cached, `$25.00` output, `context_window_k: 1050` (`UC-1 Apex`, `D11`, `E2 >= gpt-6-astra`)
  - `openai/gpt-5-search-api`: `$1.25` input, `$0.125` cached, `$10.00` output, `context_window_k: 256` (`UC-2 Flagship`, `D6`, `E1 > gpt-5-mini`)
  - `openai/gpt-4-turbo-2024-04-09`: `$10.00` input, `$30.00` output, `context_window_k: 128` (`UC-2 Flagship`, `D1*`, unplaced legacy snapshot)
  - `openai/gpt-4-0613`: `$30.00` input, `$60.00` output, `context_window_k: 8` (`UC-2 Flagship`, `D1*`, unplaced legacy snapshot)
  - `openai/gpt-3.5-turbo`: `$0.50` input, `$1.50` output, `context_window_k: 16` (`UC-3 Balanced`, `D1*`, unplaced legacy base)
  - `openai/gpt-3.5-turbo-0125`: `$0.50` input, `$1.50` output, `context_window_k: 16` (`UC-3 Balanced`, `D1*`, unplaced legacy snapshot)
- **xAI (1)**:
  - `xai/grok-4.20-multi-agent`: `$1.25` input, `$0.20` cached, `$2.50` output (long context: `$2.50 / $0.40 / $5.00`), `context_window_k: 1000` (`UC-2 Flagship`, `D7`, `E1 > grok-4.20-0309-reasoning`)
- **Z.AI (5)**:
  - `zai/glm-4-32b-0414-128k`: `$0.10` input, `$0.10` output, `context_window_k: 128` (`UC-4 Efficient`, `D1*`, unplaced open weights)
  - `zai/glm-4.5-air`: `$0.20` input, `$0.03` cached, `$1.10` output, `context_window_k: 128` (`UC-4 Efficient`, `D1*`, E6 from `glm-4.5-airx`)
  - `zai/glm-4.6v-flash`: `$0.00` input, `$0.00` output, `context_window_k: 128` (`UC-4 Efficient`, `D1*`, E6 from `glm-4.6`)
  - `zai/glm-4.6v-flashx`: `$0.04` input, `$0.004` cached, `$0.40` output, `context_window_k: 128` (`UC-4 Efficient`, `D1*`, E6 from `glm-4.6`)
  - `zai/glm-ocr`: `$0.03` input, `$0.03` output, `context_window_k: 8` (`UC-4 Efficient`, `D1*`, unplaced OCR)

## 2. Price Changes

- **0** existing models in `model-pricing.json` had price changes on standard tiers.

## 3. Unchanged

- **100** existing models in `model-pricing.json` had no price changes.

## 4. Registry Additions

- **14 models added** to `model-registry.json` (`_version: "1.12.1"`, `_updated: "2026-11-02"`), growing total from 100 to 114.
- **`deeper_than` item added (1)**: On `gpt-6-rosalind` over `gpt-6-astra` (kind: `E1`, source: OpenAI specialized models docs).
- **EC-9 release-date corrections applied (2)**:
  - `claude-sonnet-5-5`: `2026-10-14 → 2026-09-28`
  - `claude-haiku-5-5`: `2026-10-14 → 2026-10-07`
- **ECI scores and intervals refreshed (70)**: 70 models updated with IRT scores and 95% intervals from Epoch ECI CSV snapshot `2026-11-02`.

## 5. Prefix Gaps

- Added prefix `{ "prefix": "gpt-rosalind", "max_output": 16384, "method": "temperature", "effort": [] }`.
- Added prefix `{ "prefix": "glm-ocr", "max_output": 8192, "method": "temperature", "effort": [] }`.
- **0** unexpected prefix gaps remaining. Gate 5 passed cleanly.

## 6. Parameter Mapping

- **No changes needed** in `model-parameter-mapping.json` (`2.4.0`, `2026-09-05`). Gate 7 passed across all 5 active registry methods (`adaptive_thinking`, `effort`, `reasoning_effort`, `temperature`, `thinking`).

## 7. Test Results

- **Phase 8**: All 14 new models initialized with `enabled: false` (status untested/legacy/available). Zero live API calls needed for Gate 8. Gate 8 passed with exit code 0.

## 8. Long Context

- `grok-4.20-multi-agent` carries long-context tier: `$2.50` input, `$0.40` cached, `$5.00` output for `>=200k` tokens (`threshold_k: 200`).

## 9. Pending Resolution

- **Squeezes**: 0 squeezes in this run.
- **Ties from silent sources (3)**:
  - `gpt-rosalind-discovery = gpt-rosalind-research` (E5 tie)
  - `gpt-4-turbo-2024-04-09 = gpt-4o` (E2 tie)
  - `gpt-4-0613 = gpt-4.1` (E2 tie)
- **Report-only ECI Inconsistencies on existing models (6)**: Kept at established rungs per append-only invariant:
  - `o4-mini` D4 vs `o1` D4
  - `claude-opus-4-8` D8 vs `grok-4.7` D8
  - `claude-haiku-5-5` D8 vs `grok-4.7` D8
  - `gpt-6.1-terra` D9 vs `gpt-5.4-pro` D9
  - `gpt-6.1-terra` D9 vs `gpt-5.5` D9
  - `gpt-6.1-terra` D9 vs `gpt-5.6-terra` D9

## 10. Sources Archived

Saved in `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-11-02_PRICES\`:

- `2026-11-02_Anthropic-Pricing-DOM.json`
- `2026-11-02_Anthropic-ModelIDs-DOM.json`
- `2026-11-02_OpenAI-Standard-DOM.json`
- `2026-11-02_OpenAI-Batch-DOM.json`
- `2026-11-02_OpenAI-Compare-DOM.json`
- `2026-11-02_Google-Pricing-DOM.json`
- `2026-11-02_Google-Models-DOM.json`
- `2026-11-02_ZAI-Pricing-DOM.json`
- `2026-11-02_ZAI-Models-DOM.json`
- `2026-11-02_xAI-Pricing-DOM.json`
- `2026-11-02_xAI-Models-DOM.json`
- `2026-11-02_eci-leaderboard.csv`
- `2026-11-02_Epoch-ECI-Match.json`
- `2026-11-02_Depth-Edges.json`
- `2026-11-02_ChangeSet.json`
- `2026-11-02_DepthLadder.log`
- `2026-11-02_RunReport.md`

## 11. MODEL_INVENTORY.md Changes

- **Sources header updated**: `model-registry.json` `1.12.1 (2026-11-02)`, `model-pricing.json` `(2026-11-02)`.
- **Top rung header**: `Top rung: D12 (2026-11-02)`.
- **Section 3.1 rows added**: Total Section 3.1 active text models expanded to 106 rows, sorted by Depth descending, Model ascending.
- **Section 3.2 rows**: Maintained 4 Devin-only rows (`Gemini 3.5 Flash`, `Gemini 3.7 Flash`, `Kimi K3`, `SWE-1.7`).
- **Gate 9.4**: **PASS** (106 Section 3.1 rows verified, Top rung D12, sources and pricing consistent).

## 12. Depth Ladder

- **Inserted rungs (14 models)**:
  - `gpt-6-rosalind`: **D12** (`E1m > gpt-6-astra`)
  - `gpt-rosalind-discovery`: **D11** (`E2 >= gpt-6-astra`)
  - `gpt-rosalind-research`: **D11** (`E2 >= gpt-6-astra`)
  - `grok-4.20-multi-agent`: **D7** (`E1 > grok-4.20-0309-reasoning`)
  - `gpt-5-search-api`: **D6** (`E1 > gpt-5-mini`)
  - `glm-4.5-air`: **D1\*** (`E6 from glm-4.5-airx`)
  - `glm-4.6v-flash`: **D1\*** (`E6 from glm-4.6`)
  - `glm-4.6v-flashx`: **D1\*** (`E6 from glm-4.6`)
  - `glm-4-32b-0414-128k`: **D1\*** (unplaced)
  - `glm-ocr`: **D1\*** (unplaced)
  - `gpt-4-turbo-2024-04-09`: **D1\*** (unplaced)
  - `gpt-4-0613`: **D1\*** (unplaced)
  - `gpt-3.5-turbo`: **D1\*** (unplaced)
  - `gpt-3.5-turbo-0125`: **D1\*** (unplaced)
- **Top rung before**: `D12` (`claude-fable-5-1`, `claude-fable-5`, `claude-mythos-5-1`, `claude-mythos-5`).
- **Top rung after**: `D12` (joined by `gpt-6-rosalind`).
- **`deeper_than` items added**: 1 item (`gpt-6-rosalind > gpt-6-astra`, `E1`).
- **E6 estimates**: 3 estimated from siblings, 6 unplaced (total 9 marked `*`).
- **Items / scope guard changes**: None (`observed.sequences < 3`).
- **Cycles and Rejected Edges**: 0 cycles, 0 rejected items.

## 13. Phase 9 Distribution and Gate 9 Sync Check

- **Phase 9.1 (Agent folder)**: Synced `model-pricing.json`, `model-registry.json`, `model-parameter-mapping.json`, `test-call-llm.py`, and `MODEL_INVENTORY.md` to `e:\dev\IPPS\.devin\skills\llm-tools\`.
- **Phase 9.3 (External config targets)**: Synced `model-pricing.json`, `model-registry.json`, and `model-parameter-mapping.json` to pre-authorized external target `e:\Dev\Lana-V1\.agent-data\config` (DD-14).
- **Gate 9 (SHA-256 Sync Check)**: **PASS** (`7/7` synced files verified identical by SHA-256 hash: 3 JSONs + `MODEL_INVENTORY.md` in `.devin`, plus 3 JSONs in `Lana-V1`).

## Document History

**[2026-11-02 14:55]**
- Added: Section 13 Phase 9 Distribution and Gate 9 Sync Check results (7/7 SHA-256 matches verified identical)

**[2026-11-02 14:45]**
- Initial report created for the 2026-11-02 PRICES model inventory update run across Anthropic, OpenAI, Google Gemini, Z.AI, and xAI
