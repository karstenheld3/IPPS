# Model Registry Update Run Report (2026-11-11 NEWMODEL)

**Doc ID**: MDLRGUP-20261111-REPORT
**Goal**: Summary of the `2026-11-11` `NEWMODEL` run: 5 new text models registered; OCR models deferred
**Run Folder**: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-11-11_NEWMODEL`

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

5 models added to `model-registry.json` and `model-pricing.json`:

- **Anthropic (2)**
  - `claude-fable-5-2`: `$8.00` input, `$0.20` cached, `$40.00` output, 1M context, released 2026-11-09 (`UC-1 Apex`, `D13`, ECI `174.24` [`170.12`-`178.79`])
  - `claude-mythos-5-2`: same prices, verification-required twin of `claude-fable-5-2` (`UC-1 Apex`, `D13`, `E5 = claude-fable-5-2`)
- **Google (1)**
  - `gemini-4-carbon`: `$2.00` input, `$0.10` cached, `$10.00` output through 2026-11-30, then `$4.00` / `$0.20` / `$20.00` from 2026-12-01; 1,048,576 context; max output 65,536 (1,048,576 with long decode); released 2026-10-28 (`UC-1 Apex`, `D11`)
- **OpenAI (2)**
  - `gpt-6-cyber`: `$20.00` input, `$2.00` cached, `$100.00` output (>272K tokens: `$40.00` / `$4.00` / `$150.00`), 1,050,000 context, 128,000 max output, Daybreak Red approval required, released 2026-11-05 (`UC-1 Apex`, `D12`)
  - `gpt-6-astra-law`: `$10.00` input, `$1.00` cached, `$50.00` output (promotional through 2026-12-31 per vendor), no model page (404), context unknown (`null`), released 2026-09-17 (assumed, third-party article), `no_access` (`UC-1 Apex`, `D11`)

Deferred or excluded:

- `glm-ocr` and all other OCR models: deferred by the user (2026-11-11). `glm-ocr` keeps its 2026-02-02 vs registry 2025-10-15 release-date discrepancy and its unverified 8K context
- `chat-latest` (OpenAI, `$5.00` / `$0.50` / `$30.00`): rolling alias without a pinned identity; no depth rung can be assigned

## 2. Price Changes

- **0** existing models had standard-tier price changes (Anthropic, OpenAI GPT-6 tier table, Google, xAI, Z.AI compared against `model-pricing.json`).

## 3. Unchanged

- **All** existing pricing entries unchanged. Z.AI listed new image model `GLM-Image` (`$0.015` per image), not registered (not text).

## 4. Registry Additions

- `model-registry.json` `1.12.1` → `1.12.2` (`_updated: 2026-11-11`); 114 → 119 models (111 text models with depth).
- **`deeper_than` items added (3)**:
  - `claude-fable-5-2 > claude-opus-5-5` (E1, `https://platform.claude.com/docs/en/models/overview`)
  - `gemini-4-carbon > gemini-4-argon` (E1, `https://ai.google.dev/gemini-api/docs/models`)
  - `gpt-6-cyber > gpt-6-astra` (E1, `https://openai.com/index/introducing-gpt-6-cyber`; read through search-result summary, not Playwright)
- **ECI scores and intervals refreshed (71)** from Epoch snapshot 2026-11-11; `gpt-5` keeps `eci_ci: null` (Epoch row has no interval).
- **EC-9 release-date corrections**: none.

## 5. Prefix Gaps

- **0** prefix gaps. `claude-fable-5`, `claude-mythos-5`, `gpt-6`, `gemini-` cover the new IDs. Gate 5 passed (119 models).

## 6. Parameter Mapping

- No change in `model-parameter-mapping.json`. Gate 7 passed.

## 7. Test Results

- `claude-fable-5-2` (`reasoning_effort: low`): 200 OK, 22 tokens in, 4 out → `available`, `enabled: true`. Test entry added to `test-call-llm.py`.
- `gemini-4-carbon`: HTTP 429 free-tier quota (`generate_content_free_tier_input_token_count`), same result as `gemini-4-argon` → `no_access`. Test entry added to `test-call-llm.py`.
- `claude-mythos-5-2`, `gpt-6-astra-law`: not called (vendor-restricted) → `no_access`. `gpt-6-cyber`: not called (Daybreak Red approval) → `untested`.

## 8. Long Context

- `gpt-6-cyber` carries a long-context tier above 272K input tokens (`threshold_k: 272`).

## 9. Pending Resolution

- **Squeezes**: 0.
- **Ties from silent sources**: none new (E5 `claude-mythos-5-2 = claude-fable-5-2` and `gpt-6-astra-law` are stated by vendor pages).
- **Weak E1 evidence**: `gpt-6-cyber > gpt-6-astra` rests on "outperforms GPT-6 Astra on most cyber tasks" (domain-specific claim, vendor announcement). `gpt-6-astra-law` placed D11 by `E1 > gpt-6-sol`, not by its tie to `gpt-6-astra` (D11 as well).
- **Report-only ECI inconsistencies on existing models (21, was 6)**: refreshed Epoch intervals created 15 new report-only overlaps; rungs kept (append-only):
  - `o3-mini` D3 vs `gpt-4.1` D3; `o4-mini` D4 vs `o1` D4
  - `gpt-5-nano` D2 vs `claude-3-5-sonnet`, `gpt-4.1-mini`, `gemini-2.5-flash-lite` (all D2)
  - `gpt-5.1` D6 vs `o3-pro` D6; `claude-opus-4-5` D6 vs `o3-pro` D6
  - `gemini-3.1-pro-preview` D7 vs `gpt-5-pro` D7, `gemini-3-flash-preview` D7
  - `grok-4.20-0309-reasoning` D6 and `grok-4.20-multi-agent-0309` D6 vs `o3-pro` D6
  - `gemini-3.5-flash-lite` D4 vs `o1` D4; `grok-4.5` D7 vs `gpt-5-pro` D7
  - `glm-5.2` D6 vs `o3-pro` D6, `gpt-5.4-mini` D6; `gemini-3.6-flash` D7 vs `gpt-5-pro` D7
  - `gpt-6.1-sol` D10 vs `gpt-5.5-pro` D10, `gpt-5.6-sol` D10; `gpt-6.1-terra` D9 vs `gpt-5.4-pro`, `gpt-5.5`, `gpt-5.6-terra` (all D9)
- **Old claim superseded**: previous run reported 6 inconsistencies (2026-11-02).

## 10. Sources Archived

Saved in `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-11-11_NEWMODEL\`:

- `2026-11-11_NewModelScan.md`
- `2026-11-11_eci-leaderboard.csv`
- `2026-11-11_Epoch-ECI-Match.json`
- `2026-11-11_Depth-Edges.json`
- `2026-11-11_ChangeSet.json`
- `2026-11-11_DepthLadder.log`
- `2026-11-11_RunReport.md`

No `*-DOM.json` extracts were written; provider pages were read ad hoc with Playwright (Anthropic models and pricing, OpenAI pricing and `gpt-6-cyber` page, Google models, model and pricing pages, xAI and Z.AI pricing).

## 11. MODEL_INVENTORY.md Changes

- `Top rung: D13 (2026-11-11)` (was D12).
- Section 3.1: 111 rows; 5 rows added; Section 3.2: 4 hand-maintained rows unchanged. Gate 9.4 PASS.

## 12. Depth Ladder

- **Inserted rungs (5 models)**:
  - `claude-fable-5-2`: **D13** (`E3 > claude-fable-5`; Epoch interval `170.12` above `claude-fable-5` high `167.02`)
  - `claude-mythos-5-2`: **D13** (`E5 = claude-fable-5-2`)
  - `gpt-6-cyber`: **D12** (`E1m > gpt-6-astra`)
  - `gemini-4-carbon`: **D11** (`E1m > gemini-4-argon`)
  - `gpt-6-astra-law`: **D11** (`E1 > gpt-6-sol`)
- **Top rung before**: `D12`. **Top rung after**: `D13` (`claude-fable-5-2`, `claude-mythos-5-2`).
- **E6 estimates**: none. **Items / scope guard changes**: none. **Cycles / rejected edges**: 0 / 0.
- The manual E1 edge `claude-fable-5-2 > claude-opus-5-5` was valid but not decisive; the E3 edge over `claude-fable-5` set the rung.

## 13. Phase 9 Distribution and Gate 9 Sync Check

- **Phase 9.1**: synced `model-pricing.json`, `model-registry.json`, `model-parameter-mapping.json`, `test-call-llm.py`, and `MODEL_INVENTORY.md` to `e:\dev\IPPS\.devin\skills\llm-tools\`.
- **Phase 9.3**: synced the 3 JSONs to `e:\Dev\Lana-V1\.agent-data\config` (DD-14).
- **Gate 9**: **PASS** (`7/7` SHA-256 hashes identical).

## Document History

**[2026-11-11 21:00]**
- Initial report created for the 2026-11-11 NEWMODEL run
