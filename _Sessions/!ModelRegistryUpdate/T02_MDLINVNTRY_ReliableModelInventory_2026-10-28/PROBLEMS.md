# Session Problems: Reliable Model Inventory

**Doc ID**: MDLRGUP-MDLINVNTRY-PROBLEMS

**Purpose**: Problem tracking for T02 deep research. ID format: `MDLRGUP-MDLINVNTRY-PR-[NNNN]`

## Table of Contents

- [Open](#open)
- [Resolved](#resolved)
- [Deferred](#deferred)
- [Problems Changes](#problems-changes)

## Open

(none - 0 open problems across P1-P4)

## Resolved

- **[2026-10-29 14:30] MDLRGUP-MDLINVNTRY-PR-0003**: UC-tier letters gave 2026 only four letters (`26-C` held 22 models spanning ECI 145.8-168.8), 60 of 100 registry models had no label (no `release_date` field, labels hand-assigned), and no cross-year comparison existed (`25-A` `gpt-5.2` E155 would have mapped next to `26-B` E165 models) — resolved by deriving the letter from the frozen Epoch ECI band against a year anchor (`anchor(YY) = 170 + 15 * (YY - 26)`, A-Z), adding `release_date` and fallback `eci_band`/`eci_band_source` to `model-registry.json` 1.11.0, a `Comp YY` column (wraps May 1), one `WF` column from the band, and 92 rows (every text model not `retired`); `update-model-inventory.py`, `match-epoch-eci.py` (band freeze), Gate 9.4, `LLMCAPCLS-IN01`, `PROMPTS_GUIDES.md` 1g, `TASKS_GUIDES.md`, `PRMT-SC-05`, prompts template and examples updated. Gate 9.4 PASS (92 rows).
- **[2026-10-29 13:37] MDLRGUP-MDLINVNTRY-PR-0002**: `MODEL_INVENTORY.md` assigned `26-A` to 11 pre-October 2026 models (`R3` phrased as retroactive October promotion instead of release-month gate), placed `claude-sonnet-5-5` (`UC-3`) and `claude-opus-5`/`5-5` (`UC-2`) in the same category as `claude-fable-5` (`UC-1`), and hid `glm-5.2` (`UC-2 Flagship`) in `26-D` — resolved by fixing `R2` (strict `UC-1..4` letter separation: `26-B` Apex, `26-C` Flagship incl. `Opus` and `glm-5.2`, `26-D` Balanced incl. `Sonnet`, `26-E` Efficient incl. `Haiku`) and `R3` (`YY-A` only for Oct–Dec `UC-1` releases; pre-October models capped at `YY-B`) across `T02`, `_INFO_HOW_TO_ORGANIZE_LLMS_BY_CAPABILITY.md`, `_PROMPTS_ModelInventoryUpdate_TEMPLATE.md`, `update-model-inventory.py`, `model-registry.json`, and `MODEL_INVENTORY.md`.
- **[2026-10-28 20:24] MDLRGUP-MDLINVNTRY-PR-0001**: Playwright shared-tab collision during `02-MdlInv-Sources[01/03]` (`browser_navigate` interrupted by concurrent process navigating the default tab) — resolved in-prompt by running DOM extractions inside an isolated `page.context().browser().newContext()` and closing the context immediately after extraction.

## Deferred

(none)

## Problems Changes

**[2026-10-29 14:30]**
- Added: `MDLRGUP-MDLINVNTRY-PR-0003` under Resolved (band-based letters, Comp column, full row set)

**[2026-10-29 13:37]**
- Added: `MDLRGUP-MDLINVNTRY-PR-0002` under Resolved (`R3` pre-October `26-A` ban, `R2` strict `UC-1..4` tier separation, `glm-5.2` in `26-C`)

**[2026-10-28 20:22]**
- Added: `MDLRGUP-MDLINVNTRY-PR-0001` under Resolved (synced from `_agent_work/__CARD_MDLINVNTRY-Findings.md`); confirmed 0 open problems at P4 close
