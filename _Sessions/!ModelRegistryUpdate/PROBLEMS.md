# Session Problems: Model Registry Update

**Doc ID**: MDLRGUP-PROBLEMS

**Purpose**: Problem tracking for session `!ModelRegistryUpdate`. ID format: `MDLRGUP-PR-[NNNN]`

## Table of Contents

- [Open](#open)
- [Resolved](#resolved)
- [Deferred](#deferred)
- [Problems Changes](#problems-changes)

## Open

- **[2026-11-16 14:30] MDLRGUP-PR-0007**: `context_window` of Anthropic, Google, Z.AI, and xAI registry models not re-verified against vendor pages after the OpenAI defect (PR-0008). `contextUnverified` in `_2026-11-11_NEWMODEL\2026-11-11_ChangeSet.json` lists `claude-fable-5-2`, `claude-mythos-5-2`, `gemini-4-carbon`. Trigger: next run (template Prompt 5 item 2 and Prompt 8 item 2 now require it), or earlier on request.

- **[2026-11-17 16:10] MDLRGUP-PR-0010**: `test-layer-depth-ladder.py` TC-01 (38 rung differences), TC-02 (extra `gpt-5.3-codex`), TC-03 (Top rung expected D12, actual D13) fail with identical output at git HEAD and in the working tree, so they are not caused by the DeepSeek and Kimi run. Class: TEST. Cause: the test compares against the frozen 2026-10-28 snapshot (`DEFAULT_REGISTRY` still points to `PromptSystemV4.5`), but the registry gained rungs since (`1.12.x`). Trigger: next change to `layer-depth-ladder.py`; fix by freezing the snapshot inside the test or rebasing expectations on registry `1.12.0` depth values.
- **[2026-11-17 16:10] MDLRGUP-PR-0011**: 8 DeepSeek and Kimi models are `status: untested` (no `DEEPSEEK_API_KEY`, `MOONSHOT_API_KEY` in the keys file). Body construction, parameter clamping, and detection are covered by mock checks only; no live call confirmed `reasoning_effort` values, `max_completion_tokens` for Moonshot, or the K2 `thinking` toggle. Trigger: keys added, then run `test-call-llm.py --model <id>` per model and apply Gate 8 status updates.

- **[2026-11-17 15:20] MDLRGUP-PR-0009** (resolved 2026-11-17 16:10 below): `model-pricing.json` `context_window_k` drifts from registry `context_window` (13 of 119 entries differ under the floor rule, audit 2026-11-17): OpenAI `gpt-5*` 256 or 128 vs 400000 (9 models), `gpt-5.4-mini` and `gpt-5.4-nano` 272 vs 400000, `gpt-4.1*` 1024 vs 1047576 (1047 expected, 3 models), `gpt-image-1.5` 128 vs registry `null`; Google 1048 (floor) sits next to 1024 for `gpt-4.1*` (mixed conversion). Class: DATA. Root cause: 1) PR-0008 corrected only `context_window` in the registry; the duplicate field in pricing has no consumer in `llm-tools` scripts, session scripts, or gates, so nothing flagged it; 2) no rule defined the K conversion (observed: floor in 8, 16, 1048; division by 1024 in `gpt-4.1*`); 3) template Prompt 5 item 3 lists the field without a source. Fix: rule `context_window_k = floor(context_window / 1000)`, `null` when the registry window is `null`; Gate 5.3 in `verify-and-distribute-registry.ps1`; data synchronized; template Prompt 5 item 3 states the rule. Lana-V1 consumers not checked (outside workspace).

## Resolved

- **[2026-11-18 14:48] MDLRGUP-PR-0012** resolved: `MODEL_INVENTORY.md` Context column used `round(context_window / 1000)` while `model-pricing.json` `context_window_k` used `floor(context_window / 1000)`, creating a 1K discrepancy for 17 models. Fix: changed `update-model-inventory.py` to `math.floor(context / 1000)`, updated the Context definition in `MODEL_INVENTORY.md`, clarified Section 3.2 Efforts scope, and regenerated the inventory. Verification script passes with zero context/effort mismatches.

- **[2026-11-17 16:10] MDLRGUP-PR-0009** resolved: rule `context_window_k = floor(context_window / 1000)` (`null` when registry value is `null`) written into template Field semantics and Prompt 6; Gate 5.3 added and PASS (127 pricing entries); 13 drifting entries synchronized earlier in the session.
- **[2026-11-16 14:30] MDLRGUP-PR-0008** resolved: 11 OpenAI `context_window` values were wrong (`gpt-5` family 256000 or 128000 instead of 400000, `gpt-5.4-mini` and `gpt-5.4-nano` 272000 = window minus max output, `gpt-5.4` and `gpt-5.4-pro` 1047576 instead of 1050000). Root cause: 1) `Context` was defined as "max input tokens" in `_INFO_MDLRGUP-MDLINVNTRY-03` (L25 marked SOURCED without checking vendor wording) while vendor pages print the total window, so the semantics were ambiguous and mixed; 2) template Prompt 5 only said "backfill `context_window`", so existing values were never re-read; 3) no gate compared `context_window` to any vendor value (Gate 9.4 compares inventory to registry only). Fixes: Field semantics block in `_PROMPTS_ModelInventoryUpdate_TEMPLATE.md`, `contextChecks` in ChangeSet, Gate 5.2 in `verify-and-distribute-registry.ps1`, independent spot check in Prompt 8, registry `1.12.3`.
- **[2026-11-16 13:58] MDLRGUP-PR-0003** resolved: `gpt-6-cyber > gpt-6-astra` re-read with Playwright on `https://openai.com/index/introducing-gpt-6-cyber`; statement "outperforms GPT-6 Astra on most cyber tasks" confirmed. Third-party release date of `gpt-6-astra-law` stays `release_date_assumed: true`.
- **[2026-11-16 13:58] MDLRGUP-PR-0005** resolved (`DD-01 = 1`): Gate 2 in `verify-and-distribute-registry.ps1` is skipped when `ChangeSet.json` has `_run_mode: NEWMODEL`.

## Deferred

- **[2026-11-02 15:00] MDLRGUP-PR-0001**: Silent-source ties from 2026-11-02 PRICES run (`gpt-rosalind-discovery = gpt-rosalind-research`, `gpt-4-turbo-2024-04-09 = gpt-4o`, `gpt-4-0613 = gpt-4.1`). Vendor sources are silent on escalation/dominance; recorded as ties in `2026-11-02_Depth-Edges.json` per EC-1..EC-4 rules until vendor model guidance publishes explicit ranking. **Trigger to reopen**: vendor publishes explicit ranking.
- **[2026-11-02 15:00] MDLRGUP-PR-0002**: Report-only ECI interval inconsistencies on 6 existing models after 2026-11-02 Epoch ECI CSV refresh (`o4-mini` D4 vs `o1` D4, `claude-opus-4-8` D8 vs `grok-4.7` D8, `claude-haiku-5-5` D8 vs `grok-4.7` D8, `gpt-6.1-terra` D9 vs `gpt-5.4-pro` D9, `gpt-6.1-terra` D9 vs `gpt-5.5` D9, `gpt-6.1-terra` D9 vs `gpt-5.6-terra` D9). Kept at established rungs per append-only invariant (NFR-01); monitor next IRT refit. **[2026-11-11 21:00] Update**: refreshed Epoch intervals raised the count to 21 report-only inconsistencies (list in `_2026-11-11_NEWMODEL\2026-11-11_RunReport.md` section 9). **Trigger to reopen**: next Epoch IRT refit.
- **[2026-11-11 21:00] MDLRGUP-PR-0004**: `gemini-4-argon` and `gemini-4-carbon` return HTTP 429 (free-tier quota) with the current `GEMINI_API_KEY`; both stay `no_access` until the key is on a paid tier. Carbon prices rise to `$4/$20` on 2026-12-01 (`model-pricing.json` still holds `$2/$10`): refresh in the first run after 2026-12-01 (`DD-03 = 1`, reminder in `NOTES.md`). **Trigger to reopen**: 2026-12-01.
- **[2026-11-11 21:00] MDLRGUP-PR-0006**: OCR models deferred by the user (2026-11-11, `DD-15`): `glm-ocr` correction (release date 2026-02-02, endpoint `/api/paas/v4/layout_parsing`, file-based limits instead of the unverified 8K context), Mistral OCR 4.1 / OCR 3, open-weights OCR models (list in `_2026-11-11_NEWMODEL\2026-11-11_NewModelScan.md` section 3). `chat-latest` (OpenAI rolling alias) not registered.

## Problems Changes

**[2026-11-18 14:48]**
- Resolved: `MDLRGUP-PR-0012` (Context rounding inconsistency between MODEL_INVENTORY.md and model-pricing.json)

**[2026-11-18 14:05]**
- Added: `MDLRGUP-PR-0012` (Context rounding inconsistency between MODEL_INVENTORY.md and model-pricing.json)

**[2026-11-17 16:10]**
- Resolved: `MDLRGUP-PR-0009`. Added: `MDLRGUP-PR-0010` (stale layer regression snapshot), `MDLRGUP-PR-0011` (new models untested)

**[2026-11-17 15:20]**
- Added: `MDLRGUP-PR-0009` (pricing `context_window_k` drift)

**[2026-11-16 14:30]**
- Resolved: `MDLRGUP-PR-0008` (context_window defect). Added: `MDLRGUP-PR-0007`

**[2026-11-16 13:58]**
- Resolved: `MDLRGUP-PR-0003`, `MDLRGUP-PR-0005`
- Deferred with triggers: `MDLRGUP-PR-0001`, `MDLRGUP-PR-0002`, `MDLRGUP-PR-0004`

**[2026-11-11 21:00]**
- Added: `MDLRGUP-PR-0003`, `MDLRGUP-PR-0004`, `MDLRGUP-PR-0005`, deferred `MDLRGUP-PR-0006`; updated `MDLRGUP-PR-0002`

**[2026-11-02 15:00]**
- Added: `MDLRGUP-PR-0001` (silent-source ties from 2026-11-02 PRICES run)
- Added: `MDLRGUP-PR-0002` (report-only ECI interval inconsistencies on existing models)
