# Session Problems: Model Registry Update

**Doc ID**: MDLRGUP-PROBLEMS

**Purpose**: Problem tracking for session `!ModelRegistryUpdate`. ID format: `MDLRGUP-PR-[NNNN]`

## Table of Contents

- [Open](#open)
- [Resolved](#resolved)
- [Deferred](#deferred)
- [Problems Changes](#problems-changes)

## Open

- **[2026-11-02 15:00] MDLRGUP-PR-0001**: Silent-source ties from 2026-11-02 PRICES run (`gpt-rosalind-discovery = gpt-rosalind-research`, `gpt-4-turbo-2024-04-09 = gpt-4o`, `gpt-4-0613 = gpt-4.1`). Vendor sources are silent on escalation/dominance; recorded as ties in `2026-11-02_Depth-Edges.json` per EC-1..EC-4 rules until vendor model guidance publishes explicit ranking.
- **[2026-11-02 15:00] MDLRGUP-PR-0002**: Report-only ECI interval inconsistencies on 6 existing models after 2026-11-02 Epoch ECI CSV refresh (`o4-mini` D4 vs `o1` D4, `claude-opus-4-8` D8 vs `grok-4.7` D8, `claude-haiku-5-5` D8 vs `grok-4.7` D8, `gpt-6.1-terra` D9 vs `gpt-5.4-pro` D9, `gpt-6.1-terra` D9 vs `gpt-5.5` D9, `gpt-6.1-terra` D9 vs `gpt-5.6-terra` D9). Kept at established rungs per append-only invariant (NFR-01); monitor next IRT refit. **[2026-11-11 21:00] Update**: refreshed Epoch intervals raised the count to 21 report-only inconsistencies (list in `_2026-11-11_NEWMODEL\2026-11-11_RunReport.md` section 9).
- **[2026-11-11 21:00] MDLRGUP-PR-0003**: `gpt-6-cyber > gpt-6-astra` (E1m) rests on a domain-specific vendor claim ("outperforms GPT-6 Astra on most cyber tasks") read through a search-result summary, not Playwright. Re-read `https://openai.com/index/introducing-gpt-6-cyber` with Playwright in the next run; `gpt-6-astra-law` release date `2026-09-17` is from a third-party article (`release_date_assumed: true`) and its API model page returns 404.
- **[2026-11-11 21:00] MDLRGUP-PR-0004**: `gemini-4-argon` and `gemini-4-carbon` return HTTP 429 (free-tier quota) with the current `GEMINI_API_KEY`; both stay `no_access` until the key is on a paid tier. Carbon prices rise to `$4/$20` on 2026-12-01 (`model-pricing.json` still holds `$2/$10`): refresh in the first run after 2026-12-01.
- **[2026-11-11 21:00] MDLRGUP-PR-0005**: The 2026-11-11 NEWMODEL run wrote no `*-DOM.json` extracts, so `verify-and-distribute-registry.ps1 -Mode VerifyAll` fails Gate 2 (expects >= 4 DOM files). Gates 5, 6, 7, 9.4, 9 passed individually. Decide whether NEWMODEL runs need a Gate 2 exemption or minimal DOM files.

## Resolved

(none)

## Deferred

- **[2026-11-11 21:00] MDLRGUP-PR-0006**: OCR models deferred by the user (2026-11-11, `DD-15`): `glm-ocr` correction (release date 2026-02-02, endpoint `/api/paas/v4/layout_parsing`, file-based limits instead of the unverified 8K context), Mistral OCR 4.1 / OCR 3, open-weights OCR models (list in `_2026-11-11_NEWMODEL\2026-11-11_NewModelScan.md` section 3). `chat-latest` (OpenAI rolling alias) not registered.

## Problems Changes

**[2026-11-11 21:00]**
- Added: `MDLRGUP-PR-0003`, `MDLRGUP-PR-0004`, `MDLRGUP-PR-0005`, deferred `MDLRGUP-PR-0006`; updated `MDLRGUP-PR-0002`

**[2026-11-02 15:00]**
- Added: `MDLRGUP-PR-0001` (silent-source ties from 2026-11-02 PRICES run)
- Added: `MDLRGUP-PR-0002` (report-only ECI interval inconsistencies on existing models)
