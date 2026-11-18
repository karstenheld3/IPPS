# Model Registry Update Run Report: 2026-11-18 PRICES

**Run mode:** PRICES  
**Working folder:** `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-11-18_PRICES`  
**Registry version before:** 1.13.2 (2026-11-17)  
**Registry version after:** 1.13.3 (2026-11-18)  
**Top rung before:** D13 (2026-11-17)  
**Top rung after:** D13 (2026-11-18)

## 1. Added models

Three new OpenAI text/chat models were added:

- `gpt-6.2-astra` — UC-1 Apex, context window 1,050,000, max output 128,000, D12, `available`, enabled.
- `gpt-6.2-sol` — UC-2 Flagship, context window 1,050,000, max output 128,000, D11, `available`, enabled.
- `gpt-6.2-astra-law` — UC-1 Apex, context window 1,050,000, max output 128,000, D12, `no_access` (Trusted Access only), disabled.

## 2. Price changes

New Standard-tier prices:

| Model | Input USD / 1M | Cached USD / 1M | Output USD / 1M | Context k |
|---|---|---|---|---|
| `gpt-6.2-astra` | 8.00 | 0.40 | 40.00 | 1050 |
| `gpt-6.2-sol` | 2.00 | 0.10 | 10.00 | 1050 |
| `gpt-6.2-astra-law` | 8.00 | 0.40 | 40.00 | 1050 |

No existing model prices were changed in this PRICES run.

## 3. Unchanged count

124 models already in the registry had no field changes other than Epoch ECI score/interval refresh (79 matched, 42 unmatched).

## 4. Registry additions and corrected sourced values

- `context_window` corrected/added for the 3 new models: 1,050,000 tokens (from OpenAI compare / pricing pages).
- `max_output` added: 128,000 tokens for the 3 new models.
- `release_date` set to 2026-11-18 (assumed) for all 3 new models.
- `uc_class` set from vendor tier wording: Apex for Astra/Astra-Law, Flagship for Sol.
- `eci_score` and `eci_ci` refreshed for all 121 registry models evaluated by Epoch.

## 5. Prefix gaps

Gate 5 reported 2 non-text SKU warnings:

- `computer-use-preview`
- `gpt-image-1.5`

These are non-chat models and do not require `model_id_startswith` rows.

## 6. Parameter mapping

No new methods added. Existing methods verified: `adaptive_thinking`, `effort`, `reasoning_effort`, `temperature`, `thinking`.

## 7. Test results

| Model | Calls | Result | Registry status |
|---|---|---|---|
| `gpt-6.2-astra` | 2 (low, high) | PASS | `available`, enabled |
| `gpt-6.2-sol` | 2 (low, high) | PASS | `available`, enabled |
| `gpt-6.2-astra-law` | 1 (low) | FAIL / no access | `no_access`, disabled |

## 8. Long context

All 3 new models have a single context tier of 1,050,000 tokens; no `long_context` block was added.

## 9. Pending resolution

- `gpt-6.2-astra-law` remains `no_access` pending Trusted Access.
- 51 pre-existing INCONSISTENT E3 edges were reported by the depth ladder (kept unchanged per existing rungs); none are new contradictions introduced by this run.
- No squeezes or cycles.

## 10. Sources archived in run folder

- `2026-11-18_Anthropic-Pricing-DOM.json`
- `2026-11-18_Anthropic-ModelIDs-DOM.json`
- `2026-11-18_OpenAI-Standard-DOM.json`
- `2026-11-18_OpenAI-Batch-DOM.json`
- `2026-11-18_OpenAI-Compare-DOM.json`
- `2026-11-18_Google-Pricing-DOM.json`
- `2026-11-18_Google-Models-DOM.json`
- `2026-11-18_ZAI-Pricing-DOM.json`
- `2026-11-18_ZAI-Models-DOM.json`
- `2026-11-18_xAI-Pricing-DOM.json`
- `2026-11-18_xAI-Models-DOM.json`
- `2026-11-18_DeepSeek-Pricing-DOM.json`
- `2026-11-18_DeepSeek-Models-DOM.json`
- `2026-11-18_Moonshot-Pricing-DOM.json`
- `2026-11-18_Moonshot-Models-DOM.json`
- `2026-11-18_Devin-Models-DOM.json`
- `2026-11-18_eci-leaderboard.csv`

## 11. MODEL_INVENTORY.md changes

- Regenerated from registry `1.13.3` and pricing JSON.
- 124 Section 3.1 rows, 4 Section 3.2 rows.
- Added rows for `gpt-6.2-astra` (D12), `gpt-6.2-sol` (D11), and `gpt-6.2-astra-law` (D12*).
- Top rung header updated to `D13 (2026-11-18)`.
- `Value` cells recomputed for all rows.

## 12. Depth ladder

- Inserted rungs:
  - `gpt-6.2-sol` D11 — E1m > `gpt-6-sol`
  - `gpt-6.2-astra` D12 — E1m > `gpt-6-astra`
  - `gpt-6.2-astra-law` D12 — E4m > `gpt-6-astra-law`
- `deeper_than` items added to the 3 new models.
- No E6 estimates applied in this run.
- No `items` or `scope_guard` changes.
- Top rung remained D13.

## 13. Phase 9 distribution and Gate 9 sync verification

- Targets synced:
  - `e:\dev\IPPS\PromptSystemV4.7\skills\llm-tools\` (source)
  - `e:\dev\IPPS\.devin\skills\llm-tools\` (3 JSONs, `test-call-llm.py`, `MODEL_INVENTORY.md`)
  - `e:\Dev\Lana-V1\.agent-data\config` (3 JSONs only)
- SHA-256 matches: **7 / 7**
- **Gate 9: PASS**

---

**Gates:** Gate 8 (tests) completed, Gate 9.4 PASS, Gate 9 PASS.
