---
intended_model: claude-sonnet-4-5
context_window_size: 200k
effort: high
prompt_system: IPPS
---

<!-- Model: claude-sonnet-4-5 (effort: high, context: 200k). Load grouping (PRMT-SC-07): 10 phases of update-model-registry.md partitioned into 06 prompts (<= 6 items, <= 4 modified files, <= 1 heavy workflow per prompt) so Playwright DOM scraping, Epoch capability matching, JSON updates, API testing, and confirmation-gated distribution stay within single-turn budgets. -->

## Prompt 1 - Phase 1 Pre-Flight and Phase 2 DOM Extraction

<!-- Expected state: _2026-10-28_PRICES and run cards exist; executes Phase 1 pre-flight and Phase 2 DOM extraction across Anthropic, OpenAI, Google, Z.AI into _2026-10-28_PRICES. -->

```
01-MdlInv-PRICES [ 01 / 06 ] - Phase 1 + Phase 2 Pre-flight checks and provider DOM extraction

Session: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate`
Working folder: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES`

Read `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\_agent_work\__CARD_MDLRGUP-Robustness.md`, `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\_agent_work\__CARD_MDLRGUP-Findings.md`, `e:\dev\IPPS\update-model-registry.md` (Sources, Pricing Dimensions, Common Procedures, Phase 1, Phase 2), and `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\T02_MDLINVNTRY_ReliableModelInventory_2026-10-28\_INFO_MDLRGUP-MDLINVNTRY-04_SourcesPerField.md` (Section 9 Google Gemini extraction rules). Treat earlier conversation as compacted. Step Phase 1 + Phase 2.
Planning document: `update-model-registry.md`, Phase 1 and Phase 2 (2.1-2.6 + Google G1-G3).

Execute `update-model-registry.md` Phase 1 Pre-Flight Checks and Phase 2 DOM Extraction across `Anthropic, OpenAI, Google, Z.AI` (for `ALL` models), saving all `*-DOM.json` extracts into `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES`.

1. Execute `update-model-registry.md` Phase 1 (Steps 1-2, Gate 1) against `e:\dev\IPPS\PromptSystemV4.5\skills\llm-evaluation\model-pricing.json`, `model-registry.json`, and `model-parameter-mapping.json`
2. Extract Anthropic DOM data (`update-model-registry.md` Phase 2.1 and 2.2) from canonical URLs (`A1` `https://platform.claude.com/docs/en/about-claude/pricing`, `A2`/`A3` `https://platform.claude.com/docs/en/models/overview`, `A4` `https://platform.claude.com/docs/en/about-claude/model-deprecations`) into `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\2026-10-28_Anthropic-Pricing-DOM.json` and `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\2026-10-28_Anthropic-ModelIDs-DOM.json`
3. Extract OpenAI DOM data (`update-model-registry.md` Phase 2.3, 2.4, and O3 `innerText` window/output card extraction) from `O1` (`https://developers.openai.com/api/docs/pricing?latest-pricing=standard`), `O2` (`https://developers.openai.com/api/docs/pricing?latest-pricing=batch`), and `O3` (`https://developers.openai.com/api/docs/models/compare`) into `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\2026-10-28_OpenAI-Standard-DOM.json`, `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\2026-10-28_OpenAI-Batch-DOM.json`, and `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\2026-10-28_OpenAI-Compare-DOM.json`
4. Extract Google Gemini DOM data per `_INFO_MDLRGUP-MDLINVNTRY-04_SourcesPerField.md` Section 9:
   - `G1` (`https://ai.google.dev/gemini-api/docs/pricing`): iterate per-model `<h2>` headings and extract `sectionTables[0]` (Standard tier, parsing current price before any scheduled date increase and separating `<=200k` vs `>200k` rows) into `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\2026-10-28_Google-Pricing-DOM.json`
   - `G2` (`https://ai.google.dev/gemini-api/docs/models` + per-model `/models/<slug>` subpages for `Token limits[*]`) and `G3` (`https://ai.google.dev/gemini-api/docs/thinking` table of `Levels Supported`) into `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\2026-10-28_Google-Models-DOM.json`
5. Extract Z.AI DOM data (`update-model-registry.md` Phase 2.5 and 2.6) from `Z1` (`https://docs.z.ai/guides/overview/pricing`, first list price only) and `Z2` (`https://docs.z.ai/guides/overview/overview`) into `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\2026-10-28_ZAI-Pricing-DOM.json` and `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\2026-10-28_ZAI-Models-DOM.json`
6. Run `update-model-registry.md` Gate 2 across all saved `2026-10-28_*-DOM.json` files and close the Playwright browser (`browser_close`)

Constraints:
- All file writes MUST stay within `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES` (and `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\PROBLEMS.md` on browser timeout)
- Do ONLY the numbered items above. Report any item you could not complete as NOT DONE
- Do NOT modify any file in `e:\dev\IPPS\PromptSystemV4.5\skills\llm-evaluation`, `e:\dev\IPPS\PromptSystemV4.5\skills\write-documents\MODEL_INVENTORY.md`, or `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\model-sources\`; do NOT run Phase 9 distribution
- If Playwright MCP default tab experiences concurrent navigation interference, run extractions inside an isolated `page.context().browser().newContext()` and close it immediately after extraction
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state: overwrite `2026-10-28_*-DOM.json` cleanly if already present
- Hang safety: no command may wait for stdin, a pager, or an unbounded child. Banned: see `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\_agent_work\__CARD_MDLRGUP-Robustness.md`. 60s per-page Playwright cap (max 2 attempts per URL). On second failure: record URL in `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\PROBLEMS.md` and continue with remaining providers

Findings card: Load and update `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\_agent_work\__CARD_MDLRGUP-Findings.md`. Append one Partition Observations line and record any URL redirects or DOM selector changes.

Verify: Gate 1 and Gate 2 pass; non-empty `2026-10-28_*-DOM.json` files exist in `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES` for Anthropic, OpenAI, Google, and Z.AI; Playwright browser is closed.

**STOP.** Report: items DONE / NOT DONE, DOM files created with model counts per provider, any new or changed models spotted in raw DOM, and Gate 2 status.
```

---

## Prompt 2 - Capability Evidence: Epoch ECI CSV and Universal Class Matching

<!-- Provider DOM extracts are in _2026-10-28_PRICES. Next prompt fetches the Epoch ECI CSV and matches all inventory models to their sourced capability band and Universal Class. -->

```
01-MdlInv-PRICES [ 02 / 06 ] - P3-CapEvidence Refresh Epoch ECI scores and Universal Class mappings

Session: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate`
Working folder: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES`

Read `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\_agent_work\__CARD_MDLRGUP-Robustness.md`, `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\_agent_work\__CARD_MDLRGUP-Findings.md`, `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\T02_MDLINVNTRY_ReliableModelInventory_2026-10-28\_INFO_MDLRGUP-MDLINVNTRY-04_SourcesPerField.md` (Section 6 Capability Evidence), and `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__STRUT_MDLRGUP-MDLINVNTRY.md` (Existing Tier Design). Treat earlier conversation as compacted. Step Capability Evidence.
Planning document: `update-model-registry.md`, Phase 5 and Phase 9.4 capability input.

Download the current Epoch Capabilities Index (ECI) CSV from `https://epoch.ai/eci` and match every inventory model (including any new models found in `2026-10-28_*-DOM.json`) to its 5-point ECI band, Universal Class (`UC-1..5`), and generation equivalent.

1. Download `https://epoch.ai/data/eci_scores.csv` (or trigger the leaderboard CSV download `eci-leaderboard-general.csv` on `https://epoch.ai/eci?view=graph&tab=leaderboard` via Playwright and close browser) into `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\2026-10-28_eci-leaderboard.csv`
2. Match all models in `e:\dev\IPPS\PromptSystemV4.5\skills\llm-evaluation\model-registry.json` (plus any new models in `2026-10-28_*-DOM.json`) against the CSV by exact name, case/hyphen variant, or fixed anchor (`GPT-5 = 150.00`), rounding each ECI score to its nearest 5-point band (`E<band> = round(score / 5) * 5`)
3. Assign Universal Class (`UC-1 Apex`, `UC-2 Flagship`, `UC-3 Balanced`, `UC-4 Efficient`, `UC-5 Edge`) from provider documentation / price order and compute `Generation equivalent` (`≈ [highest reference UC-1/UC-2 model with ECI <= model ECI]`)
4. Save the complete mapping (`model_id`, `uc_class`, `eci_score`, `eci_ci_low`, `eci_ci_high`, `eci_band`, `gen_equivalent`, `snapshot_date`) to `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\2026-10-28_Epoch-ECI-Match.json`

Constraints:
- All file writes MUST stay within `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES`
- Do ONLY the numbered items above. Report any item you could not complete as NOT DONE
- Read ECI from `https://epoch.ai/eci` only; never use Artificial Analysis Intelligence Index, LMArena Elo, or gap-to-frontier (`QS-12`)
- Do NOT modify `e:\dev\IPPS\PromptSystemV4.5\skills\llm-evaluation` JSONs or `e:\dev\IPPS\PromptSystemV4.5\skills\write-documents\MODEL_INVENTORY.md` in this prompt
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state: overwrite `2026-10-28_Epoch-ECI-Match.json` cleanly
- Hang safety: no command may wait for stdin, a pager, or an unbounded child. Banned: see `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\_agent_work\__CARD_MDLRGUP-Robustness.md`. 60s Playwright/download cap. On cap after 2 attempts: record in `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\PROBLEMS.md`, fall back to the most recent `*_Epoch-ECI-Match.json` in `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate`, and continue

Findings card: Load and update `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\_agent_work\__CARD_MDLRGUP-Findings.md`. Append one Partition Observations line and note any newly released models that have `< 4` benchmarks (no ECI row yet).

Verify: `2026-10-28_Epoch-ECI-Match.json` exists and is valid JSON; every matched model has `uc_class` and `eci_band` populated (or `eci_band: null` with `uc_class` fallback documented for brand-new models); Playwright browser is closed.

**STOP.** Report: items DONE / NOT DONE, total models matched in `2026-10-28_Epoch-ECI-Match.json`, any ECI band shifts since prior run, and any new models lacking 4 Epoch benchmarks.
```

---

## Prompt 3 - Phases 5, 6, and 7 Canonical JSON Updates and Gates 5-7

<!-- Expected state: DOM extracts (2026-10-28_*-DOM.json) and capability matches (2026-10-28_Epoch-ECI-Match.json) are in _2026-10-28_PRICES; updates the three canonical JSON files in SKILL_FOLDER and verifies Gates 5, 6, and 7. -->

```
01-MdlInv-PRICES [ 03 / 06 ] - Phase 5 + Phase 6 + Phase 7 Update canonical JSONs and verify Gates 5-7

Session: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate`
Working folder: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES`

Read `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\_agent_work\__CARD_MDLRGUP-Robustness.md`, `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\_agent_work\__CARD_MDLRGUP-Findings.md`, and `e:\dev\IPPS\update-model-registry.md` (Phase 5, Phase 6, Phase 7). Treat earlier conversation as compacted. Step Phase 5 + Phase 6 + Phase 7.
Planning document: `update-model-registry.md`, Phase 5, Phase 6, and Phase 7.

Execute `update-model-registry.md` Phases 5, 6, and 7 using the DOM extracts and capability data in `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES` to update `e:\dev\IPPS\PromptSystemV4.5\skills\llm-evaluation\model-registry.json`, `e:\dev\IPPS\PromptSystemV4.5\skills\llm-evaluation\model-pricing.json`, and `e:\dev\IPPS\PromptSystemV4.5\skills\llm-evaluation\model-parameter-mapping.json`, and verify Gates 5, 6, and 7.

1. Execute `update-model-registry.md` Phase 5.0 (Derive Change Set) by comparing `2026-10-28_*-DOM.json` against `e:\dev\IPPS\PromptSystemV4.5\skills\llm-evaluation\model-registry.json` and `e:\dev\IPPS\PromptSystemV4.5\skills\llm-evaluation\model-pricing.json`; write `newRegistryIds`, `newPricingIds`, and `changedPricingIds` to `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\2026-10-28_ChangeSet.json`
2. Execute `update-model-registry.md` Phase 5.1, 5.2, and 5.3 on `e:\dev\IPPS\PromptSystemV4.5\skills\llm-evaluation\model-registry.json` (incorporating capability fields from `2026-10-28_Epoch-ECI-Match.json` per `UC_ECI` and bumping `_updated` to `2026-10-28`)
3. Run `update-model-registry.md` Gate 5 (Persistence + Consistency check on `e:\dev\IPPS\PromptSystemV4.5\skills\llm-evaluation\model-registry.json`)
4. Execute `update-model-registry.md` Phase 6 (Rules 1-9) on `e:\dev\IPPS\PromptSystemV4.5\skills\llm-evaluation\model-pricing.json` (Standard tier prices for Anthropic, OpenAI, Google Gemini, and Z.AI; bump `last_updated` to `2026-10-28`) and run Gate 6 (Persistence Check)
5. Execute `update-model-registry.md` Phase 7 (7.1-7.2) on `e:\dev\IPPS\PromptSystemV4.5\skills\llm-evaluation\model-parameter-mapping.json` and run Gate 7

Constraints:
- All file operations MUST stay within `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES` and the three canonical JSON files in `e:\dev\IPPS\PromptSystemV4.5\skills\llm-evaluation` (`model-registry.json`, `model-pricing.json`, `model-parameter-mapping.json`)
- Do ONLY the numbered items above. Report any item you could not complete as NOT DONE
- Never remove existing or deprecated models from `model-registry.json` or `model-pricing.json`
- Do NOT edit `e:\dev\IPPS\.devin` directly and do NOT execute Phase 9 distribution in this prompt
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state: JSON updates are idempotent and verified by Gates 5-7
- Hang safety: no command may wait for stdin, a pager, or an unbounded child. Banned: see `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\_agent_work\__CARD_MDLRGUP-Robustness.md`. 120s per-command cap. On cap: kill, record in `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\PROBLEMS.md`, continue

Findings card: Load and update `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\_agent_work\__CARD_MDLRGUP-Findings.md`. Append one Partition Observations line and record any prefix gaps or new effort methods.

Verify: `2026-10-28_ChangeSet.json` exists; Gates 5, 6, and 7 pass with exit code 0; `_updated` / `last_updated` in modified JSONs equal `2026-10-28`.

**STOP.** Report: items DONE / NOT DONE, `newRegistryIds` count, `newPricingIds` count, `changedPricingIds` count, any prefix gaps, and Gate 5-7 results.
```

---

## Prompt 4 - Phase 8 Live API Tests, Phase 9.4 Inventory Regeneration, and Phase 10 Report

<!-- Expected state: Canonical JSONs in SKILL_FOLDER passed Gates 5-7; runs Phase 8 live API tests on new models, Phase 9.4 regeneration of MODEL_INVENTORY.md, and Phase 10 summary report. -->

```
01-MdlInv-PRICES [ 04 / 06 ] - Phase 8 + Phase 9.4 + Phase 10 Test new models, regenerate MODEL_INVENTORY.md, and write report

Session: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate`
Working folder: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES`

Read `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\_agent_work\__CARD_MDLRGUP-Robustness.md`, `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\_agent_work\__CARD_MDLRGUP-Findings.md`, `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\2026-10-28_ChangeSet.json`, `e:\dev\IPPS\update-model-registry.md` (Phase 8, Phase 9.4, Phase 10), and `e:\dev\IPPS\PromptSystemV4.5\skills\write-documents\MODEL_INVENTORY.md`. Treat earlier conversation as compacted. Step Phase 8 + Phase 9.4 + Phase 10.
Planning document: `update-model-registry.md`, Phase 8, Phase 9.4, and Phase 10.

Execute `update-model-registry.md` Phase 8 (Test New Models), Phase 9.4 (Update `MODEL_INVENTORY.md`), and Phase 10 (Report), saving the run summary report to `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\2026-10-28_RunReport.md`.

1. Execute `update-model-registry.md` Phase 8: for each model in `newRegistryIds` (`2026-10-28_ChangeSet.json`) enabled for testing, run `e:\dev\.tools\llm-venv\Scripts\python.exe "e:\dev\IPPS\PromptSystemV4.5\skills\llm-evaluation\test-call-llm.py" --keys-file e:\dev\.tools\.api-keys.txt --model <modelId>` (adding a minimal test entry in `test-call-llm.py` if absent) and apply Gate 8 status updates (`available`, `no_access`, or effort level adjustments) in `e:\dev\IPPS\PromptSystemV4.5\skills\llm-evaluation\model-registry.json`
2. Execute `update-model-registry.md` Phase 9.4 to update `e:\dev\IPPS\PromptSystemV4.5\skills\write-documents\MODEL_INVENTORY.md` from `e:\dev\IPPS\PromptSystemV4.5\skills\llm-evaluation\model-registry.json`, `model-pricing.json`, `model-parameter-mapping.json`, and `2026-10-28_Epoch-ECI-Match.json` (enforcing R2 strict `UC-1..4` vendor-tier separation so Fable != Opus != Sonnet != Haiku, R3 pre-October release gate so no model released before October 1 receives `YY-A`, and R4 over-eagerness affecting `behavior_profile` only so `glm-5.2` stays `26-C` `guarded`; run `update-model-inventory.py --recompute-wf`)
3. Run `update-model-registry.md` Gate 9.4 to verify that every enabled model in `e:\dev\IPPS\PromptSystemV4.5\skills\llm-evaluation\model-registry.json` resolves to a row in `e:\dev\IPPS\PromptSystemV4.5\skills\write-documents\MODEL_INVENTORY.md` and all source versions/dates match
4. Execute `update-model-registry.md` Phase 10 and write the complete run report (Added models, Price changes, Unchanged count, Registry additions, Prefix gaps, Parameter mapping, Test results, Long context, Pending resolution, Sources archived in `_2026-10-28_PRICES`, `MODEL_INVENTORY.md` changes) to `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\2026-10-28_RunReport.md`

Constraints:
- All file operations MUST stay within `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES`, `e:\dev\IPPS\PromptSystemV4.5\skills\llm-evaluation\model-registry.json`, `e:\dev\IPPS\PromptSystemV4.5\skills\llm-evaluation\test-call-llm.py`, and `e:\dev\IPPS\PromptSystemV4.5\skills\write-documents\MODEL_INVENTORY.md`
- Do ONLY the numbered items above. Report any item you could not complete as NOT DONE
- Do NOT execute Phase 9.1-9.3 distribution in this prompt (distribution is isolated in Prompt 5)
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state: `MODEL_INVENTORY.md` regeneration and `2026-10-28_RunReport.md` are idempotent
- Hang safety: no command may wait for stdin, a pager, or an unbounded child. Banned: see `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\_agent_work\__CARD_MDLRGUP-Robustness.md`. 120s per-model API test cap. On timeout: retry once, then record in `2026-10-28_RunReport.md` and `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\PROBLEMS.md`, continue

Findings card: Load and update `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\_agent_work\__CARD_MDLRGUP-Findings.md`. Append one Partition Observations line and record any API test failures (e.g., rejected effort values).

Verify: Gate 8 and Gate 9.4 pass; `e:\dev\IPPS\PromptSystemV4.5\skills\write-documents\MODEL_INVENTORY.md` source versions/dates match JSONs; `2026-10-28_RunReport.md` exists with all 11 Phase 10 report sections.

**STOP.** Report: items DONE / NOT DONE, Phase 8 test pass/fail summary, Gate 9.4 status, and path to `2026-10-28_RunReport.md`. Ask user to confirm whether Prompt 5 should include external config distribution (`e:\Dev\Lana-V1\config`, `e:\Dev\Lana-V2\config`).
```

---

## Prompt 5 - Phase 9 Distribution and Gate 9 Sync Check (Confirmation-Gated)

<!-- Expected state: Phase 8 tests, Phase 9.4 MODEL_INVENTORY.md update, and Phase 10 report are complete; distributes updated files to in-workspace targets and (only if confirmed) external Lana targets, then verifies Gate 9. -->

```
01-MdlInv-PRICES [ 05 / 06 ] - Phase 9 Distribute canonical JSONs and MODEL_INVENTORY.md and verify Gate 9

Session: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate`
Working folder: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES`

Read `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\_agent_work\__CARD_MDLRGUP-Robustness.md`, `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\_agent_work\__CARD_MDLRGUP-Findings.md`, and `e:\dev\IPPS\update-model-registry.md` (Distribution Targets, Phase 9.1-9.3, Gate 9). Treat earlier conversation as compacted. Step Phase 9.
Planning document: `update-model-registry.md`, Phase 9 (9.1-9.3 and Gate 9).

Distribute the updated canonical JSON files (`model-pricing.json`, `model-registry.json`, `model-parameter-mapping.json`) and `e:\dev\IPPS\PromptSystemV4.5\skills\write-documents\MODEL_INVENTORY.md` from `e:\dev\IPPS\PromptSystemV4.5` to all authorized distribution targets and verify file-hash identity via Gate 9.

1. Execute `update-model-registry.md` Phase 9.1: copy `model-pricing.json`, `model-registry.json`, and `model-parameter-mapping.json` from `e:\dev\IPPS\PromptSystemV4.5\skills\llm-evaluation\` to `e:\dev\IPPS\.devin\skills\llm-evaluation\`, and copy `e:\dev\IPPS\PromptSystemV4.5\skills\write-documents\MODEL_INVENTORY.md` to `e:\dev\IPPS\.devin\skills\write-documents\MODEL_INVENTORY.md`
2. Execute `update-model-registry.md` Phase 9.2: copy existing JSON files to dependent skills (`e:\dev\IPPS\.devin\skills\llm-transcription\`, `e:\dev\IPPS\PromptSystemV4.5\skills\llm-transcription\`)
3. Execute `update-model-registry.md` Phase 9.3 (`e:\Dev\Lana-V1\config`, `e:\Dev\Lana-V2\config`) ONLY if the user explicitly confirmed external target distribution in this session; if not confirmed, skip Phase 9.3 and record `"Phase 9.3 skipped (external distribution not confirmed)"` in `2026-10-28_RunReport.md`
4. Run `update-model-registry.md` Gate 9 (`Get-FileHash` comparison across all synced targets) and append the sync verification result to `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\2026-10-28_RunReport.md`

Constraints:
- All file operations MUST stay within `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES`, `e:\dev\IPPS\.devin\skills\llm-evaluation\`, `e:\dev\IPPS\.devin\skills\write-documents\`, `e:\dev\IPPS\.devin\skills\llm-transcription\`, `e:\dev\IPPS\PromptSystemV4.5\skills\llm-transcription\`, and (only when explicitly confirmed by user) `e:\Dev\Lana-V1\config` and `e:\Dev\Lana-V2\config`
- CONFIRMATION GATE: Never copy files to `e:\Dev\Lana-V1\config` or `e:\Dev\Lana-V2\config` without explicit user confirmation
- Do ONLY the numbered items above. Report any item you could not complete as NOT DONE
- Re-running this prompt must not corrupt state: `Copy-Item -Force` and hash verification are idempotent
- Hang safety: no command may wait for stdin, a pager, or an unbounded child. Banned: see `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\_agent_work\__CARD_MDLRGUP-Robustness.md`. 60s per-command cap. On cap: kill, record in `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\PROBLEMS.md`, continue

Findings card: Load and update `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\_agent_work\__CARD_MDLRGUP-Findings.md`. Append one Partition Observations line.

Verify: Gate 9 passes with zero SHA-256 hash mismatches across all synced targets; `e:\dev\IPPS\.devin\skills\write-documents\MODEL_INVENTORY.md` hash matches `e:\dev\IPPS\PromptSystemV4.5\skills\write-documents\MODEL_INVENTORY.md`.

**STOP.** Report: items DONE / NOT DONE, targets synced (with SHA-256 match count), whether Phase 9.3 external targets were synced or skipped, and Gate 9 status.
```

---

## Prompt 6 - Final Verification Checkpoint

<!-- Expected state: All update, test, inventory regeneration, and distribution steps are complete; runs the verification checkpoint across all run deliverables and updates session tracking. -->

```
01-MdlInv-PRICES [ 06 / 06 ] - Final Checkpoint Verify all gates, deliverables, and session tracking

Session: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate`
Working folder: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES`

Read `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\_agent_work\__CARD_MDLRGUP-Robustness.md`, `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\_agent_work\__CARD_MDLRGUP-Findings.md`, `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\2026-10-28_RunReport.md`, and `e:\dev\IPPS\update-model-registry.md` (Gates 1-9.4). Treat earlier conversation as compacted. Step Final Checkpoint.
Planning document: `update-model-registry.md`, Gates 1-9.4 and Phase 10.

Verify all outputs of the `2026-10-28` `PRICES` model inventory update run against `update-model-registry.md` Gates 1-9.4 and `MODEL_INVENTORY.md` consistency rules, fix any gaps inline within 2 cycles, and record the completed run in `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\NOTES.md`.

/verify

1. Verify `update-model-registry.md` Gates 5, 6, 7, 8, 9, and 9.4 (`e:\dev\IPPS\PromptSystemV4.5\skills\llm-evaluation` JSONs, `e:\dev\IPPS\PromptSystemV4.5\skills\write-documents\MODEL_INVENTORY.md`, and `e:\dev\IPPS\.devin` mirror hashes)
2. Verify `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES` completeness (`2026-10-28_*-DOM.json`, `2026-10-28_ChangeSet.json`, `2026-10-28_RunReport.md`, and zero leftover `.tmp_*` scripts in `_agent_work\`) and check that `__CARD_MDLRGUP-Findings.md` `## Unresolved` is empty (or copied to `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\PROBLEMS.md`)
3. Fix any verification gaps inline (max 2 gate cycles; on second failure record in `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\PROBLEMS.md` and stop), and update `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\NOTES.md` with a 1-line entry recording `2026-10-28 PRICES` completion and `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES` path

Constraints:
- All file operations MUST stay within `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES`, `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\NOTES.md`, `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\PROBLEMS.md`, `e:\dev\IPPS\PromptSystemV4.5\skills\llm-evaluation`, `e:\dev\IPPS\PromptSystemV4.5\skills\write-documents\MODEL_INVENTORY.md`, and `e:\dev\IPPS\.devin\skills\`
- Do ONLY the numbered items above. Report any item you could not complete as NOT DONE
- Do NOT run unconfirmed external distribution to `e:\Dev\Lana-V1\config` or `e:\Dev\Lana-V2\config`
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state: verification and `NOTES.md` status update are idempotent
- Hang safety: see `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\_agent_work\__CARD_MDLRGUP-Robustness.md`

Findings card: Load and update `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\_agent_work\__CARD_MDLRGUP-Findings.md`. Append final Partition Observations line.

Verify: Gates 5, 6, 7, 9, and 9.4 pass; zero `.tmp_*` files remain in `_agent_work\`; `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\NOTES.md` lists the `2026-10-28 PRICES` run.

**STOP.** Report: verify findings fixed / open, total net time across the run from `__CARD_MDLRGUP-Findings.md`, and final run status.
```
