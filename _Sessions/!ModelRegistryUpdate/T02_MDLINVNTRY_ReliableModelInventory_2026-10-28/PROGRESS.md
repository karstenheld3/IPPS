# Session Progress: Reliable Model Inventory

**Doc ID**: MDLRGUP-MDLINVNTRY-PROGRESS

## Table of Contents

- [To Do](#to-do)
- [In Progress](#in-progress)
- [Done](#done)

## To Do

- [ ] P2-D1 remainder: `DD-02..05` answers (WF method, behavior profile, Devin data, provider scope)
- [ ] P5-S2/S3 after `DD-02`/`DD-03`: `TASKS_GUIDES.md` and `PROMPTS_GUIDES.md` consolidation (1c, 1f, 1g, 3a, 5)
- [ ] P5-S4 after `DD-03`: `PRMT-SC-05` profile checks, `write-prompts.md` Step 1, `edird-phase-planning` SKILL.md sizing
- [ ] Next FULL template run: verify the 29 `release_date_assumed` dates on provider pages; replace fallback bands that received an Epoch score

## In Progress

(none)

## Done

- [x] **[2026-10-29 14:30]** P2 (partial) + P5-S1/S5/S6 (partial): `DD-01` b-variant, `DD-06 1`, `DD-07 1`, `DD-08 A-Z` applied: `model-registry.json` 1.11.0 (`release_date` x100, fallback `eci_band` x22, derived `capability_label` x92, 71 label changes), `update-model-inventory.py` rewritten (Label/Comp/WF from band, Efforts column, all text rows, `CSV rows` + adaptive Medium markers), `MODEL_INVENTORY.md` Sections 1-4 rewritten and regenerated (92 + 4 rows, Comp 26), `match-epoch-eci.py` band freeze, Gate 9.4 derivation check (PASS 92 rows), `LLMCAPCLS-IN01` Sections 2-6 + 6.1 TBLF cross-check, `PROMPTS_GUIDES.md` 1g, `TASKS_GUIDES.md`, `PRMT-SC-05`, prompts template Prompt 4/6, `PROMPTS_TEMPLATE.md` and `PROMPTS_EXAMPLE_01` rows
- [x] **[2026-10-29 13:37]** `/fix` `MDLRGUP-MDLINVNTRY-PR-0002`: corrected `R3` (no `26-A` for models released before October) and `R2` (strict `UC-1..4` tier separation: `26-B` Apex `Fable`/`Astra` > `26-C` Flagship `Opus`/`Sol`/`glm-5.2` > `26-D` Balanced `Sonnet`/`Terra`/`Flash` > `26-E` Efficient `Haiku`/`Luna`/`Flash-Lite`) in `T02`, `_PROMPTS_ModelInventoryUpdate_TEMPLATE.md`, `_INFO_HOW_TO_ORGANIZE_LLMS_BY_CAPABILITY.md`, `update-model-inventory.py`, `model-registry.json`, and `MODEL_INVENTORY.md`
- [x] **[2026-10-28 20:22]** P4-S1..S3 [VERIFY+STATUS+COMMIT]: verified STRUT and T02 research set (`IN01`-`IN05`) against `RESEARCH_RULES.md` (fixed 4 `TF-*` items in `IN03`), updated `NOTES.md`, `__STRUT_MDLINVNTRY.md` (including `Computed vs actual` Time Log analysis), `PROGRESS.md`, and `PROBLEMS.md`, and committed + pushed session files (P4-D1, P4-D2 checked)
- [x] **[2026-10-28 20:22]** P3-S1..S5 [READ+WRITE+VERIFY]: created `_PROMPTS_ModelInventoryUpdate_TEMPLATE.md` (8 prompts, 20 registered placeholders, FULL/PRICES/NEWMODEL modes, PRICES full example in XML comment, verified against TMPL-* and PRMT-*, P3-D1 checked)
- [x] **[2026-10-28 20:22]** P1-S8+S9 [EVALUATE+WRITE]: evaluated 5 work-per-prompt options (`a`-`e`) in `_INFO_MDLRGUP-MDLINVNTRY-05_WorkPerPromptOptions.md` (P1-D4 checked), finalized `_INFO_MDLRGUP-MDLINVNTRY-01_Summary.md` (P1-D5 checked), and presented `DD-01..05` in chat
- [x] **[2026-10-28 20:21]** P1-S4..S7 [RESEARCH]: ECI match (28/28), METR horizons (6/28 exact, 7/28 with family prefix), Google Pricing and Models DOM extraction, provider URLs A1-A4/O1-O3/Z1-Z2 batch check (5 checked, 4 redirected, 0 dead), `_INFO_MDLRGUP-MDLINVNTRY-04_SourcesPerField.md` written (P1-D3 checked), preflight assumptions closed (7/7 verified)
- [x] **[2026-10-28 19:12]** P1-S1 part 1: T02 folder, `_agent_work\`, NOTES.md, PROGRESS.md
- [x] **[2026-10-28 19:19]** P1-S1 part 2: PROBLEMS.md, research STRUT with decomposition and assumptions
- [x] **[2026-10-28 19:19]** P1-S1 complete, P1-D1 checked
- [x] **[2026-10-28 19:12]** P1-S2: read AINWSRCH tier design, created Sources file (28 entries), verified assumptions (1 CORRECT, 2 PARTIAL, 4 pending web check)
- [x] **[2026-10-28 19:12]** P1-S3: inventory audit, 82 rows classified (S18 D27 A37), P1-D2 checked

## Progress Changes

**[2026-10-29 14:30]**
- Added: P2 partial + P5-S1/S5/S6 partial to Done (band-based labels, Comp column, full row set, TBLF markers)
- Added: To Do items for `DD-02..05`, P5-S2..S4, and the next FULL run date verification

**[2026-10-29 13:37]**
- Added: `/fix` `MDLRGUP-MDLINVNTRY-PR-0002` to Done (`R3` pre-October release ban and `R2` `UC-1..4` tier separation applied across T02, prompts template, registry, and inventory)

**[2026-10-28 20:22]**
- Added: P4-S1..S3 to Done (STRUT + T02 research set verified, session state recorded in `NOTES.md` and `__STRUT_MDLINVNTRY.md`, committed and pushed, P4-D1 and P4-D2 checked)
- Added: P3-S1..S5 to Done (`_PROMPTS_ModelInventoryUpdate_TEMPLATE.md` created and verified against TMPL-* and PRMT-*, P3-D1 checked)
- Added: P1-S8+S9 to Done (`_INFO_MDLRGUP-MDLINVNTRY-05_WorkPerPromptOptions.md`, `_INFO_MDLRGUP-MDLINVNTRY-01_Summary.md`, P1-D4 and P1-D5 checked, `DD-01..05` presented)
- Moved: P1-S8, P1-S9 from To Do

**[2026-10-28 20:21]**
- Added: P1-S4..S7 to Done (`_SOURCES/` JSON extracts, `_INFO_MDLRGUP-MDLINVNTRY-04_SourcesPerField.md`, P1-D3 checked, assumptions closed)
- Moved: P1-S4, P1-S5, P1-S6, P1-S7 from To Do

**[2026-10-28 19:12]**
- Added: P1-S3 to Done (audit file created, 82 rows, P1-D2 checked)
- Moved: P1-S3 from To Do

**[2026-10-28 19:12]**
- Added: P1-S2 to Done (tier design extracted, Sources file created, assumptions verified)
- Moved: P1-S2 from To Do

**[2026-10-28 19:19]**
- Added: P1-S1 part 2 to Done (PROBLEMS.md, research STRUT)
- Added: P1-S1 complete, P1-D1 checked

**[2026-10-28 19:12]**
- Added: P1-S2 through P1-S9 to To Do
- Added: P1-S1 part 1 to Done (folder creation, NOTES.md, PROGRESS.md)
