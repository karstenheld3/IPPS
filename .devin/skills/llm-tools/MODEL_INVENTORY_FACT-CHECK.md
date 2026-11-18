# MODEL_INVENTORY_FACT-CHECK.md

**Doc ID**: MDLRGUP-RV01
**Goal**: Verify context window size values and effort levels in MODEL_INVENTORY.md against canonical registries and vendor pages
**Timeline**: Created 2026-11-18
**Reviewed**: 2026-11-18 14:05
**Context**: Fact-check of MODEL_INVENTORY.md Section 3.1 and Section 3.2 values
**Input**: `PromptSystemV4.7/skills/llm-tools/MODEL_INVENTORY.md`

## Table of Contents

1. [Fact-Check Summary](#fact-check-summary)
2. [Source Verdicts](#source-verdicts)
3. [Fact Verdicts](#fact-verdicts)
4. [Conclusion Verdicts](#conclusion-verdicts)
5. [Unfalsifiable Claims](#unfalsifiable-claims)
6. [Recommendations](#recommendations)
7. [Document History](#document-history)

## Fact-Check Summary

- **Sources**: 9 total (9 confirmed, 0 not-found, 0 changed, 0 inaccessible)
- **Facts**: 8 total (7 confirmed, 0 refuted, 0 unverifiable, 0 unsourced, 1 weakened)
- **Conclusions**: 5 total (3 confirmed, 0 refuted, 0 unverifiable, 0 unsupported, 2 weakened)
- **Unfalsifiable**: 0 flagged
- **Recommendation**: PROCEED WITH CAUTION

## Source Verdicts

### Confirmed Sources

- **S01** `confirmed` - `https://docs.devin.ai/desktop/models`
  - Visual archive: `_download_gitignore/S01_devin_models_page.jpeg`
  - Text extract: `_sources/S01_devin_models_page.md`
  - Table extract: `_sources/S01_devin_models_tables.json`
  - Content matches document claims for Section 3.2 Devin prices and effort variants.
- **S02** `confirmed` - `https://developers.openai.com/api/docs/models/compare`
  - Visual archive: `_download_gitignore/S02_openai_compare_models.jpeg`
  - Confirms GPT-6.2 Astra, GPT-6.2 Sol, and GPT-6 Luna context window is 1,050,000 tokens.
- **S03** `confirmed` - `https://developers.openai.com/api/docs/models/gpt-4.1`
  - Visual archive: `_download_gitignore/S03_openai_gpt41.jpeg`
  - Text extract: `_sources/S03_openai_gpt41_page.md`
  - Confirms GPT-4.1 context window is 1,047,576 tokens.
- **S04** `confirmed` - `https://ai.google.dev/gemini-api/docs/models` (redirects to `https://aistudio.google.com/docs/models`)
  - Visual archive: `_download_gitignore/S04_google_gemini_models.jpeg`
  - Text extract: `_sources/S04_google_gemini_models.md`
  - Confirms Gemini family context window is 1M tokens.
- **S05** `confirmed` - `https://platform.claude.com/docs/en/models/overview`
  - Visual archive: `_download_gitignore/S05_claude_models_overview.jpeg`
  - Text extract: `_sources/S05_claude_models_overview.md`
  - Table extract: `_sources/S05_claude_models_tables.json`
  - Confirms Claude Fable/Opus/Sonnet/Haiku 5.x context window is 1M tokens; Claude Opus/Sonnet/Haiku 4.5 context window is 200K tokens.
- **S06** `confirmed` - `PromptSystemV4.7/skills/llm-tools/model-registry.json`
  - Canonical registry of model properties including `context_window` and `model_id_startswith` effort lists.
- **S07** `confirmed` - `PromptSystemV4.7/skills/llm-tools/model-pricing.json`
  - Canonical pricing including `context_window_k`.
- **S08** `confirmed` - `PromptSystemV4.7/skills/llm-tools/model-parameter-mapping.json`
  - Effort level definitions and mapping.
- **S09** `confirmed` - `_Sessions/!ModelRegistryUpdate/update-model-inventory.py`
  - Generation logic for Section 3.1 Context and Efforts columns.

## Fact Verdicts

### Critical (Refuted)

None.

### High (Weakened / Unsupported)

- **F05** `weakened` - "MODEL_INVENTORY.md Context column values are consistent with `model-pricing.json` `context_window_k`"
  - **Type**: quantitative
  - **Cites**: S06, S07, S09
  - **Reason**: 17 models differ by 1K because the inventory rounds `context_window / 1000` while pricing floors it. Inventory shows 1049K where pricing holds 1048 (Google Gemini and Moonshot Kimi families, 14 rows); inventory shows 1048K where pricing holds 1047 (GPT-4.1 family, 3 rows). See verification script output `_Sessions/!ModelRegistryUpdate/_agentwork/verify_inventory_context_effort.json`.

### Medium (Unverifiable)

None.

### Low (Unsourced)

None.

### Confirmed

- **F01** `confirmed` - "MODEL_INVENTORY.md Section 3.1 Context column is generated from `model-registry.json` `context_window` via `round(context_window / 1000)`"
  - **Type**: sourced-attribution
  - **Cites**: S06, S09
  - **Evidence**: `update-model-inventory.py` lines 286-287 set `context_cell = f"{round(context / 1000)}K" if context else "-"`.
- **F02** `confirmed` - "Section 3.1 Context values match registry-derived expected values for all 124 rows"
  - **Type**: quantitative
  - **Cites**: S06, S09, verification script `_Sessions/!ModelRegistryUpdate/_agentwork/verify_inventory_context_effort.py`
  - **Evidence**: The script parsed 124 Section 3.1 rows and found zero mismatches against the generation logic.
- **F03** `confirmed` - "Section 3.1 Efforts values match registry `model_id_startswith` effort lists for all 124 rows"
  - **Type**: quantitative
  - **Cites**: S06, S08, S09, verification script
  - **Evidence**: The script found zero effort mismatches. Mapping drops `none` and `minimal`, keeps `low`, `medium`, `high`, `xhigh`, `max` as L/M/H/X/MX; `thinking` method models use `M`, `L M H X`, or `on/off` depending on provider.
- **F04** `confirmed` - "`model-pricing.json` `context_window_k` is computed with `floor(context_window / 1000)`"
  - **Type**: sourced-attribution
  - **Cites**: S07, `_Sessions/!ModelRegistryUpdate/PROBLEMS.md` (PR-0009 resolution)
  - **Evidence**: PR-0009 established the rule `context_window_k = floor(context_window / 1000)` and synchronized 13 drifting entries.
- **F06** `confirmed` - "Section 3.2 Devin prices match the Devin Self-serve tab (or list price where the table shows Free or —)"
  - **Type**: quantitative
  - **Cites**: S01
  - **Evidence**: Adaptive matches $0.50/$0.10/$2.00; SWE-2 Flash Medium is Free and the note gives list $0.10/$0.01/$0.50; SWE-2 High shows — and the note gives list $3.00/$0.30/$15.00.
- **F07** `confirmed` - "Section 3.2 lists SWE-2 Efforts = H and SWE-2 Flash Efforts = M"
  - **Type**: factual
  - **Cites**: S01
  - **Evidence**: Self-serve table rows are "SWE-2 High" and "SWE-2 Flash Medium".
- **F08** `confirmed` - "Devin page text states SWE-2 and SWE-2 Flash each come in Medium, High, and Max reasoning-effort variants"
  - **Type**: sourced-attribution
  - **Cites**: S01
  - **Evidence**: Page text: "SWE-2 and SWE-2 Flash each come in Medium, High, and Max reasoning-effort variants."

## Conclusion Verdicts

- **C01** `confirmed` - "MODEL_INVENTORY.md Section 3.1 Context values are internally consistent with `model-registry.json`"
  - **Supports**: F01 (confirmed), F02 (confirmed)
  - **Reasoning**: Sound
- **C02** `weakened` - "MODEL_INVENTORY.md Context values are consistent across all canonical sources"
  - **Supports**: F05 (weakened)
  - **Reasoning**: Pricing file uses floor while inventory uses round, producing a 1K difference for 17 models.
- **C03** `confirmed` - "MODEL_INVENTORY.md Section 3.1 Efforts values are correct"
  - **Supports**: F03 (confirmed)
  - **Reasoning**: Sound
- **C04** `confirmed` - "MODEL_INVENTORY.md Section 3.2 prices match the Devin Self-serve page"
  - **Supports**: F06 (confirmed)
  - **Reasoning**: Sound
- **C05** `weakened` - "MODEL_INVENTORY.md Section 3.2 reports all effort variants offered in Devin"
  - **Supports**: F07 (confirmed), F08 (confirmed)
  - **Reasoning**: Self-serve table lists only one variant per model, but the page text says Medium, High, and Max are offered.

## Unfalsifiable Claims

None.

## Recommendations

### Must Do

- [ ] Reconcile the Context rounding rule between `MODEL_INVENTORY.md` and `model-pricing.json`. Options: change the inventory to use `floor` (consistent with pricing), change pricing to use `round`, or document the different rounding rules and their consumers.

### Should Do

- [ ] Clarify whether Section 3.2 "Efforts" reports only effort variants visible in the Devin Self-serve table or all variants Devin offers. If the intended scope is all offered variants, update the generation script to read from the page text or model selector; if the intended scope is only Self-serve rows, document this in the Section 3.2 description.

### Could Do

- [ ] Add a one-line note in `MODEL_INVENTORY.md` or in `update-model-inventory.py` explaining that the Context column uses `round(context_window / 1000)`.

## Document History

**[2026-11-18 14:05]**
- Initial fact-check review created
