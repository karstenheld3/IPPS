---
intended_model: [MODEL]
context_window_size: [CONTEXT_WINDOW_SIZE]
effort: [EFFORT]
prompt_system: IPPS
---

<!-- PROMPTS TEMPLATE
Filename: _PROMPTS_ModelInventoryUpdate_TEMPLATE.md
Instance naming: _PROMPTS_[DATE]_ModelInventoryUpdate.md
Location: [SESSION_FOLDER]\_PROMPTS_ModelInventoryUpdate_TEMPLATE.md (template); [RUN_FOLDER]\_PROMPTS_[DATE]_ModelInventoryUpdate.md (generated instance)

Purpose: Recurring pipeline to refresh model-registry.json, model-pricing.json, model-parameter-mapping.json, and MODEL_INVENTORY.md from authoritative provider DOM tables and Epoch ECI capability data.
Invokes phases of [WORKSPACE_FOLDER]\update-model-registry.md by number while isolating all run artifacts inside a datestamped run folder.

Run modes ([RUN_MODE]):
- FULL: Complete refresh across all providers in [TARGET_PROVIDERS] — DOM extraction (Prompt 2), full-page screenshot archive and markdown transcription (Prompt 3), Epoch ECI + Universal Class capability update (Prompt 4), canonical JSON updates with Gates 5-7 (Prompt 5), live API tests + MODEL_INVENTORY.md regeneration + Phase 10 report (Prompt 6), confirmation-gated distribution (Prompt 7), and Final Checkpoint (Prompt 8).
- PRICES: Fast price and model metadata refresh — executes Prompts 2, 4 (if capability scheme active), 5, 6, 7, 8. Excludes Prompt 3 (screenshots and image transcription).
- NEWMODEL: Targeted onboarding for newly released model(s) specified in [TARGET_MODELS] — executes Prompts 2 (affected providers only), 4, 5, 6, 7, 8. Excludes Prompt 3 unless [INCLUDE_SCREENSHOTS] = YES.

Run folder structure:
- Each run creates an isolated datestamped folder in the session root: [SESSION_FOLDER]\_[DATE]_[RUN_MODE]\ (e.g., e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\)
- [RUN_FOLDER]\_PROMPTS_[DATE]_ModelInventoryUpdate.md - Generated prompt sequence for this run (excludes Prompt 1 Bootstrap)
- [RUN_FOLDER]\_agent_work\__CARD_MDLRGUP-Findings.md - Run-scoped findings card and Partition Observations ledger
- [RUN_FOLDER]\_agent_work\__CARD_MDLRGUP-Robustness.md - Run-scoped hang-safety and Playwright robustness card
- [RUN_FOLDER]\[DATE]_Anthropic-Pricing-DOM.json, [DATE]_Anthropic-ModelIDs-DOM.json - Anthropic DOM extracts (A1-A4)
- [RUN_FOLDER]\[DATE]_OpenAI-Standard-DOM.json, [DATE]_OpenAI-Batch-DOM.json, [DATE]_OpenAI-Compare-DOM.json - OpenAI DOM extracts (O1-O3)
- [RUN_FOLDER]\[DATE]_Google-Pricing-DOM.json, [DATE]_Google-Models-DOM.json - Google Gemini DOM extracts (G1-G3)
- [RUN_FOLDER]\[DATE]_ZAI-Pricing-DOM.json, [DATE]_ZAI-Models-DOM.json - Z.AI DOM extracts (Z1-Z3)
- [RUN_FOLDER]\[DATE]_Epoch-ECI-Match.json - Epoch ECI CSV match extract (when [CAPABILITY_SCHEME] = UC_ECI)
- [RUN_FOLDER]\[DATE]_screenshots\ and [RUN_FOLDER]\[DATE]_*.md - Screenshot archive and stitched transcriptions (when [INCLUDE_SCREENSHOTS] = YES)
- [RUN_FOLDER]\[DATE]_RunReport.md - Phase 10 summary report
- Legacy [SESSION_FOLDER]\model-sources\ is read-only historical archive; never write new files into model-sources\.

Placeholder registry:
- [MODEL] - Intended execution model ID from MODEL_INVENTORY.md (e.g., glm-5.2, claude-opus-5)
- [CONTEXT_WINDOW_SIZE] - Model context window size in k (e.g., 200k, 1000k)
- [EFFORT] - Reasoning/thinking effort level (low | medium | high | xhigh | max)
- [WORKSPACE_FOLDER] - Workspace root path (e.g., e:\dev\IPPS)
- [PROMPTSYSTEM_FOLDER] - Canonical PromptSystem folder path in workspace (e.g., e:\dev\IPPS\PromptSystemV4.5)
- [AGENT_FOLDER] - Active agent folder path in workspace (e.g., e:\dev\IPPS\.devin)
- [SKILL_FOLDER] - Canonical llm-evaluation skill folder ([PROMPTSYSTEM_FOLDER]\skills\llm-evaluation)
- [INVENTORY_FILE] - Canonical MODEL_INVENTORY.md file path ([PROMPTSYSTEM_FOLDER]\skills\write-documents\MODEL_INVENTORY.md)
- [SESSION_FOLDER] - Permanent session folder ([WORKSPACE_FOLDER]\_Sessions\!ModelRegistryUpdate)
- [RUN_FOLDER] - Datestamped run folder ([SESSION_FOLDER]\_[DATE]_[RUN_MODE])
- [RUN_MODE] - Execution scope mode (FULL | PRICES | NEWMODEL)
- [DATE] - Run date in YYYY-MM-DD format (e.g., 2026-10-28)
- [TARGET_PROVIDERS] - Providers in scope for this run (e.g., Anthropic, OpenAI, Google, Z.AI)
- [TARGET_MODELS] - Target model IDs for NEWMODEL mode, or ALL for FULL and PRICES modes
- [INCLUDE_SCREENSHOTS] - Include Prompt 3 screenshot capture and transcription (YES | NO)
- [CAPABILITY_SCHEME] - Capability representation mode from DD-01 (UC_ECI | YY_L | NONE)
- [TOTAL_PROMPTS] - Total prompt count in the generated instance after conditional prompt removal (e.g., 08 for FULL, 07 for PRICES)
- [VENV_PYTHON] - Shared Python executable path (e.g., e:\dev\.tools\llm-venv\Scripts\python.exe)
- [KEYS_FILE] - API keys file path (e:\dev\.tools\.api-keys.txt)
- [TRANSCRIPTION_SCRIPT] - Image-to-markdown transcription script ([AGENT_FOLDER]\skills\llm-transcription\transcribe-image-to-markdown.py)

Load-based partition table (PRMT-SC-07 assessment for [MODEL] at [EFFORT] effort, [CONTEXT_WINDOW_SIZE] context):
- Prompt 1 (Bootstrap, ~15k tokens, 4 items): Detect [RUN_MODE], [DATE], [PROMPTSYSTEM_FOLDER], create [RUN_FOLDER] and _agent_work cards, generate instance _PROMPTS_[DATE]_ModelInventoryUpdate.md via /write-prompts.
- Prompt 2 (Phases 1 + 2 DOM Extraction, ~45k tokens, 6 items): Pre-flight Gate 1 + Playwright DOM extraction across [TARGET_PROVIDERS] (Anthropic A1-A4, OpenAI O1-O3, Google Gemini G1-G3, Z.AI Z1-Z3) + Gate 2 check.
- Prompt 3 (Phases 3 + 4 Screenshots & Transcription, ~40k tokens, 4 items, Conditional on [INCLUDE_SCREENSHOTS] = YES): Full-page scroll capture, copy to [RUN_FOLDER]\[DATE]_screenshots\, run transcribe-image-to-markdown.py, stitch markdowns, verify Gates 3-4.
- Prompt 4 (Capability Evidence, ~25k tokens, 4 items, Conditional on [CAPABILITY_SCHEME] = UC_ECI): Download Epoch ECI CSV (eci-leaderboard-general.csv / eci_scores.csv), match inventory models to 5-point ECI bands + UC-1..5 + generation equivalent, save [DATE]_Epoch-ECI-Match.json.
- Prompt 5 (Phases 5 + 6 + 7 Canonical JSON Updates, ~35k tokens, 5 items): Derive change set (Phase 5.0), update model-registry.json (Phase 5 + Gate 5), update model-pricing.json (Phase 6 + Gate 6), verify model-parameter-mapping.json (Phase 7 + Gate 7).
- Prompt 6 (Phase 8 + Phase 9.4 + Phase 10, ~30k tokens, 4 items): Run test-call-llm.py for new enabled models (Phase 8 + Gate 8), regenerate [INVENTORY_FILE] (Phase 9.4 + Gate 9.4), write [RUN_FOLDER]\[DATE]_RunReport.md (Phase 10).
- Prompt 7 (Phase 9 Distribution, ~15k tokens, 4 items, Confirmation-Gated): Copy 3 canonical JSONs to [AGENT_FOLDER] and dependent skills (9.1-9.2), copy to external Lana targets (9.3) ONLY if user confirmed, mirror [INVENTORY_FILE] to [AGENT_FOLDER], run Gate 9 hash check.
- Prompt 8 (Final Checkpoint, ~20k tokens, 3 items): Run /verify across updated JSONs, [INVENTORY_FILE], and [DATE]_RunReport.md; fix any gaps inline (max 2 cycles); update session NOTES.md.

Conditional prompts:
- Prompt 3 (Phases 3-4 Screenshots and Transcription) - remove when [INCLUDE_SCREENSHOTS] = NO (default for PRICES and NEWMODEL).
- Prompt 4 (Capability Evidence: Epoch ECI + UC) - remove when [CAPABILITY_SCHEME] != UC_ECI.
- After removing any conditional prompt, renumber remaining prompts sequentially in the generated instance file and update [TOTAL_PROMPTS] in every Prompt Marker (e.g., removing Prompt 3 yields [ 01 / 07 ] through [ 07 / 07 ]).

CRITICAL - Manual execution only:
- Prompts are designed for manual copy-paste, one prompt per turn, with user review at each gate.
- Agent must NEVER self-execute multiple prompts in a single response (PRMT-EX-01, PRMT-EX-02).
- The **STOP.** marker at the end of every prompt is a hard execution boundary.

Context management:
- Target: 200k+ token context models (e.g., glm-5.2 high, claude-opus-5 high).
- In PRICES or NEWMODEL mode (Prompts 2, 4, 5, 6, 7, 8), total token consumption is ~145k and fits in a single session.
- In FULL mode (including Prompt 3 screenshot batches), start a fresh session before Prompt 5 if context exceeds 120k tokens; all Phase 2-4 outputs are persisted on disk in [RUN_FOLDER].
- Later prompts must NOT re-read large files already in conversation history from earlier turns in the same session.
- Playwright MCP calls may hang; enforce a 60s timeout per page and use an isolated browser.newContext() if the default tab has concurrent navigation.

Remove template-instruction XML comments (this block, Conditional comments, and the EXAMPLE block at the end) when instantiating _PROMPTS_[DATE]_ModelInventoryUpdate.md; keep the opening load-grouping comment and the 1-sentence commentary comment under each ## Prompt N heading (PRMT-FT-04, PRMT-SC-05, PRMT-SC-07).
-->

<!-- Model: [MODEL] (effort: [EFFORT], context: [CONTEXT_WINDOW_SIZE]). Load grouping (PRMT-SC-07): 10 phases of update-model-registry.md partitioned into [TOTAL_PROMPTS] prompts (<= 6 items, <= 4 modified files, <= 1 heavy workflow per prompt) so Playwright DOM scraping, screenshot transcription, Epoch capability matching, JSON updates, API testing, and confirmation-gated distribution stay within single-turn budgets. -->

## Prompt 1 - Bootstrap: Detect Context, Create Run Folder, and Generate Instance

<!-- Detects [RUN_MODE] and [DATE], creates [RUN_FOLDER] and _agent_work cards, and instantiates _PROMPTS_[DATE]_ModelInventoryUpdate.md. -->

```
01-MdlInv-[RUN_MODE] [ 01 / 08 ] - P3-Bootstrap Detect run parameters, initialize run folder, and generate prompts instance

Session: `[SESSION_FOLDER]`
Working folder: `[SESSION_FOLDER]`

Read `[SESSION_FOLDER]\NOTES.md`, `[WORKSPACE_FOLDER]\update-model-registry.md` (Placeholders, Sources, Phase 1), and `[SESSION_FOLDER]\_agent_work\__CARD_MDLINVNTRY-Robustness.md`. Treat earlier conversation as compacted. Step P3-Bootstrap.
Planning document: `update-model-registry.md`, Phase 1 setup.

Initialize a datestamped model inventory update run folder and instantiate a ready-to-run prompts file from `[SESSION_FOLDER]\_PROMPTS_ModelInventoryUpdate_TEMPLATE.md`.

1. Detect workspace and run parameters:
   - Resolve `[WORKSPACE_FOLDER]`, active `[PROMPTSYSTEM_FOLDER]` (e.g., `PromptSystemV4.5`), `[AGENT_FOLDER]` (`.devin`), `[SKILL_FOLDER]`, and `[INVENTORY_FILE]`
   - Set `[DATE]` from request metadata (`YYYY-MM-DD`), `[RUN_MODE]` (`FULL` | `PRICES` | `NEWMODEL`, default `PRICES` unless user specified otherwise), `[TARGET_PROVIDERS]` (default `Anthropic, OpenAI, Google, Z.AI`), `[TARGET_MODELS]` (`ALL` or user-specified model IDs), `[INCLUDE_SCREENSHOTS]` (`YES` if `FULL`, else `NO`), and `[CAPABILITY_SCHEME]` (from `[SESSION_FOLDER]\NOTES.md` Key Decisions `DD-01`, default `UC_ECI`)
2. Create the isolated run folder `[RUN_FOLDER]` (`[SESSION_FOLDER]\_[DATE]_[RUN_MODE]\`) and `[RUN_FOLDER]\_agent_work\`; if `[INCLUDE_SCREENSHOTS] = YES`, also create `[RUN_FOLDER]\[DATE]_screenshots\` subfolders per `update-model-registry.md` Phase 1 step 4
3. Copy `__CARD_MDLINVNTRY-Robustness.md` to `[RUN_FOLDER]\_agent_work\__CARD_MDLRGUP-Robustness.md` and initialize `[RUN_FOLDER]\_agent_work\__CARD_MDLRGUP-Findings.md` with `# Findings Card: MDLRGUP ([DATE] [RUN_MODE])`, `## Partition Observations`, `## Unresolved`, and `## Resolved`
4. Generate `[RUN_FOLDER]\_PROMPTS_[DATE]_ModelInventoryUpdate.md` from `[SESSION_FOLDER]\_PROMPTS_ModelInventoryUpdate_TEMPLATE.md`:
   - Exclude Prompt 1 (already executed in this turn)
   - Remove conditional prompts that do not apply (`Prompt 3` when `[INCLUDE_SCREENSHOTS] = NO`; `Prompt 4` when `[CAPABILITY_SCHEME] != UC_ECI`)
   - Replace all `[PLACEHOLDER]` tokens with resolved values, strip template-instruction XML comments while keeping the opening load-grouping comment and 1-sentence prompt commentary comments, and renumber Prompt Markers sequentially up to `[TOTAL_PROMPTS]`

/write-prompts

Constraints:
- All file operations MUST stay within `[SESSION_FOLDER]`
- Do ONLY the numbered items above. Report any item you could not complete as NOT DONE
- Do NOT execute Phase 2 DOM extraction or modify any JSON file in `[SKILL_FOLDER]` during Bootstrap
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state: if `[RUN_FOLDER]` already exists, reuse it and overwrite only `_PROMPTS_[DATE]_ModelInventoryUpdate.md`
- Hang safety: no command may wait for stdin, a pager, or an unbounded child. Banned: see `[SESSION_FOLDER]\_agent_work\__CARD_MDLINVNTRY-Robustness.md`. 120s per-command cap. On cap: kill, record in `[SESSION_FOLDER]\PROBLEMS.md`, continue

Findings card: Load and update `[RUN_FOLDER]\_agent_work\__CARD_MDLRGUP-Findings.md`. Append one Partition Observations line for Bootstrap.

Verify: `[RUN_FOLDER]` exists; `__CARD_MDLRGUP-Findings.md` and `__CARD_MDLRGUP-Robustness.md` exist in `[RUN_FOLDER]\_agent_work\`; `[RUN_FOLDER]\_PROMPTS_[DATE]_ModelInventoryUpdate.md` exists with zero unresolved `[PLACEHOLDER]` tokens.

**STOP.** Report: resolved placeholders (`[DATE]`, `[RUN_MODE]`, `[TARGET_PROVIDERS]`, `[INCLUDE_SCREENSHOTS]`, `[CAPABILITY_SCHEME]`, `[TOTAL_PROMPTS]`), `[RUN_FOLDER]` path, generated prompts file path, and total prompts in generated sequence. Do NOT execute Prompt 2.
```

---

## Prompt 2 - Phase 1 Pre-Flight and Phase 2 DOM Extraction

<!-- Expected state: [RUN_FOLDER] and run cards exist; executes Phase 1 pre-flight and Phase 2 DOM extraction across [TARGET_PROVIDERS] into [RUN_FOLDER]. -->

```
01-MdlInv-[RUN_MODE] [ 02 / 08 ] - Phase 1 + Phase 2 Pre-flight checks and provider DOM extraction

Session: `[SESSION_FOLDER]`
Working folder: `[RUN_FOLDER]`

Read `[RUN_FOLDER]\_agent_work\__CARD_MDLRGUP-Robustness.md`, `[RUN_FOLDER]\_agent_work\__CARD_MDLRGUP-Findings.md`, `[WORKSPACE_FOLDER]\update-model-registry.md` (Sources, Pricing Dimensions, Common Procedures, Phase 1, Phase 2), and `[SESSION_FOLDER]\T02_MDLINVNTRY_ReliableModelInventory_2026-10-28\_INFO_MDLRGUP-MDLINVNTRY-04_SourcesPerField.md` (Section 9 Google Gemini extraction rules). Treat earlier conversation as compacted. Step Phase 1 + Phase 2.
Planning document: `update-model-registry.md`, Phase 1 and Phase 2 (2.1-2.6 + Google G1-G3).

Execute `update-model-registry.md` Phase 1 Pre-Flight Checks and Phase 2 DOM Extraction across `[TARGET_PROVIDERS]` (for `[TARGET_MODELS]`), saving all `*-DOM.json` extracts into `[RUN_FOLDER]` (mapping `update-model-registry.md` `MODEL_SOURCES` to `[RUN_FOLDER]`).

1. Execute `update-model-registry.md` Phase 1 (Steps 1-2, Gate 1) against `[SKILL_FOLDER]\model-pricing.json`, `model-registry.json`, and `model-parameter-mapping.json`
2. Extract Anthropic DOM data (`update-model-registry.md` Phase 2.1 and 2.2) from canonical URLs (`A1` `https://platform.claude.com/docs/en/about-claude/pricing`, `A2`/`A3` `https://platform.claude.com/docs/en/models/overview`, `A4` `https://platform.claude.com/docs/en/about-claude/model-deprecations`) into `[RUN_FOLDER]\[DATE]_Anthropic-Pricing-DOM.json` and `[RUN_FOLDER]\[DATE]_Anthropic-ModelIDs-DOM.json`
3. Extract OpenAI DOM data (`update-model-registry.md` Phase 2.3, 2.4, and O3 `innerText` window/output card extraction) from `O1` (`https://developers.openai.com/api/docs/pricing?latest-pricing=standard`), `O2` (`https://developers.openai.com/api/docs/pricing?latest-pricing=batch`), and `O3` (`https://developers.openai.com/api/docs/models/compare`) into `[RUN_FOLDER]\[DATE]_OpenAI-Standard-DOM.json`, `[RUN_FOLDER]\[DATE]_OpenAI-Batch-DOM.json`, and `[RUN_FOLDER]\[DATE]_OpenAI-Compare-DOM.json`
4. Extract Google Gemini DOM data per `_INFO_MDLRGUP-MDLINVNTRY-04_SourcesPerField.md` Section 9:
   - `G1` (`https://ai.google.dev/gemini-api/docs/pricing`): iterate per-model `<h2>` headings and extract `sectionTables[0]` (Standard tier, parsing current price before any scheduled date increase and separating `<=200k` vs `>200k` rows) into `[RUN_FOLDER]\[DATE]_Google-Pricing-DOM.json`
   - `G2` (`https://ai.google.dev/gemini-api/docs/models` + per-model `/models/<slug>` subpages for `Token limits[*]`) and `G3` (`https://ai.google.dev/gemini-api/docs/thinking` table of `Levels Supported`) into `[RUN_FOLDER]\[DATE]_Google-Models-DOM.json`
5. Extract Z.AI DOM data (`update-model-registry.md` Phase 2.5 and 2.6) from `Z1` (`https://docs.z.ai/guides/overview/pricing`, first list price only) and `Z2` (`https://docs.z.ai/guides/overview/overview`) into `[RUN_FOLDER]\[DATE]_ZAI-Pricing-DOM.json` and `[RUN_FOLDER]\[DATE]_ZAI-Models-DOM.json`
6. Run `update-model-registry.md` Gate 2 across all saved `[RUN_FOLDER]\[DATE]_*-DOM.json` files and close the Playwright browser (`browser_close`)

Constraints:
- All file writes MUST stay within `[RUN_FOLDER]` (and `[SESSION_FOLDER]\PROBLEMS.md` on browser timeout)
- Do ONLY the numbered items above. Report any item you could not complete as NOT DONE
- Do NOT modify any file in `[SKILL_FOLDER]`, `[INVENTORY_FILE]`, or `[SESSION_FOLDER]\model-sources\`; do NOT run Phase 9 distribution
- If Playwright MCP default tab experiences concurrent navigation interference, run extractions inside an isolated `page.context().browser().newContext()` and close it immediately after extraction
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state: overwrite `[RUN_FOLDER]\[DATE]_*-DOM.json` cleanly if already present
- Hang safety: no command may wait for stdin, a pager, or an unbounded child. Banned: see `[RUN_FOLDER]\_agent_work\__CARD_MDLRGUP-Robustness.md`. 60s per-page Playwright cap (max 2 attempts per URL). On second failure: record URL in `[SESSION_FOLDER]\PROBLEMS.md` and continue with remaining providers

Findings card: Load and update `[RUN_FOLDER]\_agent_work\__CARD_MDLRGUP-Findings.md`. Append one Partition Observations line and record any URL redirects or DOM selector changes.

Verify: Gate 1 and Gate 2 pass; non-empty `[DATE]_*-DOM.json` files exist in `[RUN_FOLDER]` for every provider in `[TARGET_PROVIDERS]`; Playwright browser is closed.

**STOP.** Report: items DONE / NOT DONE, DOM files created with model counts per provider, any new or changed models spotted in raw DOM, and Gate 2 status.
```

---

<!-- Conditional: include Prompt 3 only when [INCLUDE_SCREENSHOTS] = YES (default for [RUN_MODE] = FULL; remove for PRICES and NEWMODEL and renumber remaining prompts). -->

## Prompt 3 - Phases 3 and 4 Screenshot Archive and Markdown Transcription

<!-- Expected state: Phase 2 saved authoritative DOM JSONs in [RUN_FOLDER]; captures full-page screenshots and markdown transcriptions for the historical visual archive. -->

```
01-MdlInv-[RUN_MODE] [ 03 / 08 ] - Phase 3 + Phase 4 Full-page screenshot capture and markdown transcription

Session: `[SESSION_FOLDER]`
Working folder: `[RUN_FOLDER]`

Read `[RUN_FOLDER]\_agent_work\__CARD_MDLRGUP-Robustness.md`, `[RUN_FOLDER]\_agent_work\__CARD_MDLRGUP-Findings.md`, and `[WORKSPACE_FOLDER]\update-model-registry.md` (Phase 3, Phase 4). Treat earlier conversation as compacted. Step Phase 3 + Phase 4.
Planning document: `update-model-registry.md`, Phase 3 and Phase 4.

Execute `update-model-registry.md` Phase 3 (Screenshot Archive) and Phase 4 (Transcribe Screenshots) with `MODEL_SOURCES` mapped to `[RUN_FOLDER]`.

1. Execute `update-model-registry.md` Phase 3 (Body-Scroll Capture for `A1`, `A3`, `A4`, `O3`, `Z1`, `Z2`, and Google `G1`, `G2`; Inner-Scroll Capture for `O1`, `O2`), copying captured `.jpg` files into `[RUN_FOLDER]\[DATE]_screenshots\<SourceFolder>\` per the Screenshot Path Limitation workaround
2. Run `update-model-registry.md` Gate 3: verify each screenshot subfolder in `[RUN_FOLDER]\[DATE]_screenshots\` has `>= 1` `.jpg` and spot-check that output price columns are not clipped; close Playwright (`browser_close`)
3. Execute `update-model-registry.md` Phase 4.1 using `[VENV_PYTHON]` and `[TRANSCRIPTION_SCRIPT]` with `--keys-file [KEYS_FILE]` across each populated `[RUN_FOLDER]\[DATE]_screenshots\<SourceFolder>`
4. Execute `update-model-registry.md` Phase 4.2 to stitch per-page `.md` files into `[RUN_FOLDER]\[DATE]_<Source>.md`, remove temporary per-page `.md` and `_batch_summary.json` files, and verify Gate 4

Constraints:
- All file writes MUST stay within `[RUN_FOLDER]`
- Do ONLY the numbered items above. Report any item you could not complete as NOT DONE
- Do NOT modify canonical JSONs in `[SKILL_FOLDER]` or run Phase 9 distribution
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state: `--force` overwrites partial transcriptions cleanly
- Hang safety: no command may wait for stdin, a pager, or an unbounded child. Banned: see `[RUN_FOLDER]\_agent_work\__CARD_MDLRGUP-Robustness.md`. 60s per-page Playwright cap, 180s per-folder transcription cap. On cap: kill, record in `[SESSION_FOLDER]\PROBLEMS.md`, continue (Gate 4 does not block Phase 5)

Findings card: Load and update `[RUN_FOLDER]\_agent_work\__CARD_MDLRGUP-Findings.md`. Append one Partition Observations line.

Verify: Gate 3 and Gate 4 pass; `[RUN_FOLDER]\[DATE]_screenshots\` subfolders contain `.jpg` files and stitched `[RUN_FOLDER]\[DATE]_*.md` files exist; Playwright browser is closed.

**STOP.** Report: items DONE / NOT DONE, screenshot counts per folder, stitched markdown files created, and Gate 3-4 status.
```

---

<!-- Conditional: DD-01 - include Prompt 4 when [CAPABILITY_SCHEME] = UC_ECI; omit if [CAPABILITY_SCHEME] = NONE and renumber remaining prompts. -->
<!-- Provider DOM extracts are in [RUN_FOLDER]. Next prompt fetches the Epoch ECI CSV and matches all inventory models to their sourced capability band and Universal Class. -->

## Prompt 4 - Capability Evidence: Epoch ECI CSV and Universal Class Matching

```
01-MdlInv-[RUN_MODE] [ 04 / 08 ] - P3-CapEvidence Refresh Epoch ECI scores and Universal Class mappings

Session: `[SESSION_FOLDER]`
Working folder: `[RUN_FOLDER]`

Read `[RUN_FOLDER]\_agent_work\__CARD_MDLRGUP-Robustness.md`, `[RUN_FOLDER]\_agent_work\__CARD_MDLRGUP-Findings.md`, `[SESSION_FOLDER]\T02_MDLINVNTRY_ReliableModelInventory_2026-10-28\_INFO_MDLRGUP-MDLINVNTRY-04_SourcesPerField.md` (Section 6 Capability Evidence), and `[SESSION_FOLDER]\T02_MDLINVNTRY_ReliableModelInventory_2026-10-28\_agent_work\__STRUT_MDLRGUP-MDLINVNTRY.md` (Existing Tier Design). Treat earlier conversation as compacted. Step Capability Evidence.
Planning document: `update-model-registry.md`, Phase 5 and Phase 9.4 capability input.

Download the current Epoch Capabilities Index (ECI) CSV from `https://epoch.ai/eci` and match every inventory model (including any new models found in `[RUN_FOLDER]\[DATE]_*-DOM.json`) to its 5-point ECI band, Universal Class (`UC-1..5`), and generation equivalent.

1. Download `https://epoch.ai/data/eci_scores.csv` (or trigger the leaderboard CSV download `eci-leaderboard-general.csv` on `https://epoch.ai/eci?view=graph&tab=leaderboard` via Playwright and close browser) into `[RUN_FOLDER]\[DATE]_eci-leaderboard.csv`
2. Match all models in `[SKILL_FOLDER]\model-registry.json` (plus any new models in `[RUN_FOLDER]\[DATE]_*-DOM.json`) against the CSV by exact name, case/hyphen variant, or fixed anchor (`GPT-5 = 150.00`), rounding each ECI score to its nearest 5-point band (`E<band> = round(score / 5) * 5`)
3. Assign Universal Class (`UC-1 Apex`, `UC-2 Flagship`, `UC-3 Balanced`, `UC-4 Efficient`, `UC-5 Edge`) from provider documentation / price order and compute `Generation equivalent` (`≈ [highest reference UC-1/UC-2 model with ECI <= model ECI]`)
4. Save the complete mapping (`model_id`, `uc_class`, `eci_score`, `eci_ci_low`, `eci_ci_high`, `eci_band`, `gen_equivalent`, `snapshot_date`) to `[RUN_FOLDER]\[DATE]_Epoch-ECI-Match.json`

Constraints:
- All file writes MUST stay within `[RUN_FOLDER]`
- Do ONLY the numbered items above. Report any item you could not complete as NOT DONE
- Read ECI from `https://epoch.ai/eci` only; never use Artificial Analysis Intelligence Index, LMArena Elo, or gap-to-frontier (`QS-12`)
- Do NOT modify `[SKILL_FOLDER]` JSONs or `[INVENTORY_FILE]` in this prompt
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state: overwrite `[RUN_FOLDER]\[DATE]_Epoch-ECI-Match.json` cleanly
- Hang safety: no command may wait for stdin, a pager, or an unbounded child. Banned: see `[RUN_FOLDER]\_agent_work\__CARD_MDLRGUP-Robustness.md`. 60s Playwright/download cap. On cap after 2 attempts: record in `[SESSION_FOLDER]\PROBLEMS.md`, fall back to the most recent `*_Epoch-ECI-Match.json` in `[SESSION_FOLDER]`, and continue

Findings card: Load and update `[RUN_FOLDER]\_agent_work\__CARD_MDLRGUP-Findings.md`. Append one Partition Observations line and note any newly released models that have `< 4` benchmarks (no ECI row yet).

Verify: `[RUN_FOLDER]\[DATE]_Epoch-ECI-Match.json` exists and is valid JSON; every matched model has `uc_class` and `eci_band` populated (or `eci_band: null` with `uc_class` fallback documented for brand-new models); Playwright browser is closed.

**STOP.** Report: items DONE / NOT DONE, total models matched in `[DATE]_Epoch-ECI-Match.json`, any ECI band shifts since prior run, and any new models lacking 4 Epoch benchmarks.
```

---

## Prompt 5 - Phases 5, 6, and 7 Canonical JSON Updates and Gates 5-7

<!-- Expected state: DOM extracts ([DATE]_*-DOM.json) and capability matches ([DATE]_Epoch-ECI-Match.json) are in [RUN_FOLDER]; updates the three canonical JSON files in [SKILL_FOLDER] and verifies Gates 5, 6, and 7. -->

```
01-MdlInv-[RUN_MODE] [ 05 / 08 ] - Phase 5 + Phase 6 + Phase 7 Update canonical JSONs and verify Gates 5-7

Session: `[SESSION_FOLDER]`
Working folder: `[RUN_FOLDER]`

Read `[RUN_FOLDER]\_agent_work\__CARD_MDLRGUP-Robustness.md`, `[RUN_FOLDER]\_agent_work\__CARD_MDLRGUP-Findings.md`, and `[WORKSPACE_FOLDER]\update-model-registry.md` (Phase 5, Phase 6, Phase 7). Treat earlier conversation as compacted. Step Phase 5 + Phase 6 + Phase 7.
Planning document: `update-model-registry.md`, Phase 5, Phase 6, and Phase 7.

Execute `update-model-registry.md` Phases 5, 6, and 7 using the DOM extracts and capability data in `[RUN_FOLDER]` to update `[SKILL_FOLDER]\model-registry.json`, `[SKILL_FOLDER]\model-pricing.json`, and `[SKILL_FOLDER]\model-parameter-mapping.json`, and verify Gates 5, 6, and 7.

1. Execute `update-model-registry.md` Phase 5.0 (Derive Change Set) by comparing `[RUN_FOLDER]\[DATE]_*-DOM.json` against `[SKILL_FOLDER]\model-registry.json` and `[SKILL_FOLDER]\model-pricing.json`; write `newRegistryIds`, `newPricingIds`, and `changedPricingIds` to `[RUN_FOLDER]\[DATE]_ChangeSet.json`
2. Execute `update-model-registry.md` Phase 5.1, 5.2, and 5.3 on `[SKILL_FOLDER]\model-registry.json` (incorporating capability fields from `[RUN_FOLDER]\[DATE]_Epoch-ECI-Match.json` per `[CAPABILITY_SCHEME]` and bumping `_updated` to `[DATE]`)
3. Run `update-model-registry.md` Gate 5 (Persistence + Consistency check on `[SKILL_FOLDER]\model-registry.json`)
4. Execute `update-model-registry.md` Phase 6 (Rules 1-9) on `[SKILL_FOLDER]\model-pricing.json` (Standard tier prices for Anthropic, OpenAI, Google Gemini, and Z.AI; bump `last_updated` to `[DATE]`) and run Gate 6 (Persistence Check)
5. Execute `update-model-registry.md` Phase 7 (7.1-7.2) on `[SKILL_FOLDER]\model-parameter-mapping.json` and run Gate 7

Constraints:
- All file operations MUST stay within `[RUN_FOLDER]` and the three canonical JSON files in `[SKILL_FOLDER]` (`[SKILL_FOLDER]\model-registry.json`, `[SKILL_FOLDER]\model-pricing.json`, `[SKILL_FOLDER]\model-parameter-mapping.json`)
- Do ONLY the numbered items above. Report any item you could not complete as NOT DONE
- Never remove existing or deprecated models from `model-registry.json` or `model-pricing.json`
- Do NOT edit `[AGENT_FOLDER]` directly and do NOT execute Phase 9 distribution in this prompt
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state: JSON updates are idempotent and verified by Gates 5-7
- Hang safety: no command may wait for stdin, a pager, or an unbounded child. Banned: see `[RUN_FOLDER]\_agent_work\__CARD_MDLRGUP-Robustness.md`. 120s per-command cap. On cap: kill, record in `[SESSION_FOLDER]\PROBLEMS.md`, continue

Findings card: Load and update `[RUN_FOLDER]\_agent_work\__CARD_MDLRGUP-Findings.md`. Append one Partition Observations line and record any prefix gaps or new effort methods.

Verify: `[RUN_FOLDER]\[DATE]_ChangeSet.json` exists; Gates 5, 6, and 7 pass with exit code 0; `_updated` / `last_updated` in modified `[SKILL_FOLDER]` JSONs equal `[DATE]`.

**STOP.** Report: items DONE / NOT DONE, `newRegistryIds` count, `newPricingIds` count, `changedPricingIds` count, any prefix gaps, and Gate 5-7 results.
```

---

## Prompt 6 - Phase 8 Live API Tests, Phase 9.4 Inventory Regeneration, and Phase 10 Report

<!-- Expected state: Canonical JSONs in [SKILL_FOLDER] passed Gates 5-7; runs Phase 8 live API tests on new models, Phase 9.4 regeneration of [INVENTORY_FILE], and Phase 10 summary report. -->

```
01-MdlInv-[RUN_MODE] [ 06 / 08 ] - Phase 8 + Phase 9.4 + Phase 10 Test new models, regenerate MODEL_INVENTORY.md, and write report

Session: `[SESSION_FOLDER]`
Working folder: `[RUN_FOLDER]`

Read `[RUN_FOLDER]\_agent_work\__CARD_MDLRGUP-Robustness.md`, `[RUN_FOLDER]\_agent_work\__CARD_MDLRGUP-Findings.md`, `[RUN_FOLDER]\[DATE]_ChangeSet.json`, `[WORKSPACE_FOLDER]\update-model-registry.md` (Phase 8, Phase 9.4, Phase 10), and `[INVENTORY_FILE]`. Treat earlier conversation as compacted. Step Phase 8 + Phase 9.4 + Phase 10.
Planning document: `update-model-registry.md`, Phase 8, Phase 9.4, and Phase 10.

Execute `update-model-registry.md` Phase 8 (Test New Models), Phase 9.4 (Update `MODEL_INVENTORY.md`), and Phase 10 (Report), saving the run summary report to `[RUN_FOLDER]\[DATE]_RunReport.md`.

1. Execute `update-model-registry.md` Phase 8: for each model in `newRegistryIds` (`[RUN_FOLDER]\[DATE]_ChangeSet.json`) enabled for testing, run `[VENV_PYTHON] "[SKILL_FOLDER]\test-call-llm.py" --keys-file [KEYS_FILE] --model <modelId>` (adding a minimal test entry in `[SKILL_FOLDER]\test-call-llm.py` if absent) and apply Gate 8 status updates (`available`, `no_access`, or effort level adjustments) in `[SKILL_FOLDER]\model-registry.json`
2. Execute `update-model-registry.md` Phase 9.4 to update `[INVENTORY_FILE]` from `[SKILL_FOLDER]\model-registry.json`, `model-pricing.json`, `model-parameter-mapping.json`, and `[RUN_FOLDER]\[DATE]_Epoch-ECI-Match.json` (respecting `[CAPABILITY_SCHEME]`)
3. Run `update-model-registry.md` Gate 9.4 to verify that every enabled model in `[SKILL_FOLDER]\model-registry.json` resolves to a row in `[INVENTORY_FILE]` and all source versions/dates match
4. Execute `update-model-registry.md` Phase 10 and write the complete run report (Added models, Price changes, Unchanged count, Registry additions, Prefix gaps, Parameter mapping, Test results, Long context, Pending resolution, Sources archived in `[RUN_FOLDER]`, `MODEL_INVENTORY.md` changes) to `[RUN_FOLDER]\[DATE]_RunReport.md`

Constraints:
- All file operations MUST stay within `[RUN_FOLDER]`, `[SKILL_FOLDER]\model-registry.json`, `[SKILL_FOLDER]\test-call-llm.py`, and `[INVENTORY_FILE]`
- Do ONLY the numbered items above. Report any item you could not complete as NOT DONE
- Do NOT execute Phase 9.1-9.3 distribution in this prompt (distribution is isolated in Prompt 7)
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state: `MODEL_INVENTORY.md` regeneration and `[DATE]_RunReport.md` are idempotent
- Hang safety: no command may wait for stdin, a pager, or an unbounded child. Banned: see `[RUN_FOLDER]\_agent_work\__CARD_MDLRGUP-Robustness.md`. 120s per-model API test cap. On timeout: retry once, then record in `[RUN_FOLDER]\[DATE]_RunReport.md` and `[SESSION_FOLDER]\PROBLEMS.md`, continue

Findings card: Load and update `[RUN_FOLDER]\_agent_work\__CARD_MDLRGUP-Findings.md`. Append one Partition Observations line and record any API test failures (e.g., rejected effort values).

Verify: Gate 8 and Gate 9.4 pass; `[INVENTORY_FILE]` source versions/dates match `[SKILL_FOLDER]` JSONs; `[RUN_FOLDER]\[DATE]_RunReport.md` exists with all 11 Phase 10 report sections.

**STOP.** Report: items DONE / NOT DONE, Phase 8 test pass/fail summary, Gate 9.4 status, and path to `[RUN_FOLDER]\[DATE]_RunReport.md`. Ask user to confirm whether Prompt 7 should include external config distribution (`e:\Dev\Lana-V1\config`, `e:\Dev\Lana-V2\config`).
```

---

## Prompt 7 - Phase 9 Distribution and Gate 9 Sync Check (Confirmation-Gated)

<!-- Expected state: Phase 8 tests, Phase 9.4 MODEL_INVENTORY.md update, and Phase 10 report are complete; distributes updated files to in-workspace targets and (only if confirmed) external Lana targets, then verifies Gate 9. -->

```
01-MdlInv-[RUN_MODE] [ 07 / 08 ] - Phase 9 Distribute canonical JSONs and MODEL_INVENTORY.md and verify Gate 9

Session: `[SESSION_FOLDER]`
Working folder: `[RUN_FOLDER]`

Read `[RUN_FOLDER]\_agent_work\__CARD_MDLRGUP-Robustness.md`, `[RUN_FOLDER]\_agent_work\__CARD_MDLRGUP-Findings.md`, and `[WORKSPACE_FOLDER]\update-model-registry.md` (Distribution Targets, Phase 9.1-9.3, Gate 9). Treat earlier conversation as compacted. Step Phase 9.
Planning document: `update-model-registry.md`, Phase 9 (9.1-9.3 and Gate 9).

Distribute the updated canonical JSON files (`model-pricing.json`, `model-registry.json`, `model-parameter-mapping.json`) and `[INVENTORY_FILE]` from `[PROMPTSYSTEM_FOLDER]` to all authorized distribution targets and verify file-hash identity via Gate 9.

1. Execute `update-model-registry.md` Phase 9.1: copy `model-pricing.json`, `model-registry.json`, and `model-parameter-mapping.json` from `[SKILL_FOLDER]` to `[AGENT_FOLDER]\skills\llm-evaluation\`, and copy `[INVENTORY_FILE]` to `[AGENT_FOLDER]\skills\write-documents\MODEL_INVENTORY.md`
2. Execute `update-model-registry.md` Phase 9.2: copy existing JSON files to dependent skills (`[AGENT_FOLDER]\skills\llm-transcription\`, `[PROMPTSYSTEM_FOLDER]\skills\llm-transcription\`)
3. Execute `update-model-registry.md` Phase 9.3 (`e:\Dev\Lana-V1\config`, `e:\Dev\Lana-V2\config`) ONLY if the user explicitly confirmed external target distribution in this session; if not confirmed, skip Phase 9.3 and record `"Phase 9.3 skipped (external distribution not confirmed)"` in `[RUN_FOLDER]\[DATE]_RunReport.md`
4. Run `update-model-registry.md` Gate 9 (`Get-FileHash` comparison across all synced targets) and append the sync verification result to `[RUN_FOLDER]\[DATE]_RunReport.md`

Constraints:
- All file operations MUST stay within `[RUN_FOLDER]`, `[AGENT_FOLDER]\skills\llm-evaluation\`, `[AGENT_FOLDER]\skills\write-documents\`, `[AGENT_FOLDER]\skills\llm-transcription\`, `[PROMPTSYSTEM_FOLDER]\skills\llm-transcription\`, and (only when explicitly confirmed by user) `e:\Dev\Lana-V1\config` and `e:\Dev\Lana-V2\config`
- CONFIRMATION GATE: Never copy files to `e:\Dev\Lana-V1\config` or `e:\Dev\Lana-V2\config` without explicit user confirmation
- Do ONLY the numbered items above. Report any item you could not complete as NOT DONE
- Re-running this prompt must not corrupt state: `Copy-Item -Force` and hash verification are idempotent
- Hang safety: no command may wait for stdin, a pager, or an unbounded child. Banned: see `[RUN_FOLDER]\_agent_work\__CARD_MDLRGUP-Robustness.md`. 60s per-command cap. On cap: kill, record in `[SESSION_FOLDER]\PROBLEMS.md`, continue

Findings card: Load and update `[RUN_FOLDER]\_agent_work\__CARD_MDLRGUP-Findings.md`. Append one Partition Observations line.

Verify: Gate 9 passes with zero SHA-256 hash mismatches across all synced targets; `[AGENT_FOLDER]\skills\write-documents\MODEL_INVENTORY.md` hash matches `[INVENTORY_FILE]`.

**STOP.** Report: items DONE / NOT DONE, targets synced (with SHA-256 match count), whether Phase 9.3 external targets were synced or skipped, and Gate 9 status.
```

---

## Prompt 8 - Final Verification Checkpoint

<!-- Expected state: All update, test, inventory regeneration, and distribution steps are complete; runs the verification checkpoint across all run deliverables and updates session tracking. -->

```
01-MdlInv-[RUN_MODE] [ 08 / 08 ] - Final Checkpoint Verify all gates, deliverables, and session tracking

Session: `[SESSION_FOLDER]`
Working folder: `[RUN_FOLDER]`

Read `[RUN_FOLDER]\_agent_work\__CARD_MDLRGUP-Robustness.md`, `[RUN_FOLDER]\_agent_work\__CARD_MDLRGUP-Findings.md`, `[RUN_FOLDER]\[DATE]_RunReport.md`, and `[WORKSPACE_FOLDER]\update-model-registry.md` (Gates 1-9.4). Treat earlier conversation as compacted. Step Final Checkpoint.
Planning document: `update-model-registry.md`, Gates 1-9.4 and Phase 10.

Verify all outputs of the `[DATE]` `[RUN_MODE]` model inventory update run against `update-model-registry.md` Gates 1-9.4 and `MODEL_INVENTORY.md` consistency rules, fix any gaps inline within 2 cycles, and record the completed run in `[SESSION_FOLDER]\NOTES.md`.

/verify

1. Verify `update-model-registry.md` Gates 5, 6, 7, 8, 9, and 9.4 (`[SKILL_FOLDER]` JSONs, `[INVENTORY_FILE]`, and `[AGENT_FOLDER]` mirror hashes)
2. Verify `[RUN_FOLDER]` completeness (`[DATE]_*-DOM.json`, `[DATE]_ChangeSet.json`, `[DATE]_RunReport.md`, and zero leftover `.tmp_*` scripts in `[RUN_FOLDER]\_agent_work\`) and check that `[RUN_FOLDER]\_agent_work\__CARD_MDLRGUP-Findings.md` `## Unresolved` is empty (or copied to `[SESSION_FOLDER]\PROBLEMS.md`)
3. Fix any verification gaps inline (max 2 gate cycles; on second failure record in `[SESSION_FOLDER]\PROBLEMS.md` and stop), and update `[SESSION_FOLDER]\NOTES.md` with a 1-line entry recording `[DATE] [RUN_MODE]` completion and `[RUN_FOLDER]` path

Constraints:
- All file operations MUST stay within `[RUN_FOLDER]`, `[SESSION_FOLDER]\NOTES.md`, `[SESSION_FOLDER]\PROBLEMS.md`, `[SKILL_FOLDER]`, `[INVENTORY_FILE]`, and `[AGENT_FOLDER]\skills\`
- Do ONLY the numbered items above. Report any item you could not complete as NOT DONE
- Do NOT run unconfirmed external distribution to `e:\Dev\Lana-V1\config` or `e:\Dev\Lana-V2\config`
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state: verification and `NOTES.md` status update are idempotent
- Hang safety: see `[RUN_FOLDER]\_agent_work\__CARD_MDLRGUP-Robustness.md`

Findings card: Load and update `[RUN_FOLDER]\_agent_work\__CARD_MDLRGUP-Findings.md`. Append final Partition Observations line.

Verify: Gates 5, 6, 7, 9, and 9.4 pass; zero `.tmp_*` files remain in `[RUN_FOLDER]\_agent_work\`; `[SESSION_FOLDER]\NOTES.md` lists the `[DATE] [RUN_MODE]` run.

**STOP.** Report: verify findings fixed / open, total net time across the run from `__CARD_MDLRGUP-Findings.md`, and final run status.
```

<!-- EXAMPLE: Reference only. Do not copy into new documents. Shows a completed PRICES run instance (Prompts 1 and 2 resolved; Prompt 3 omitted because [INCLUDE_SCREENSHOTS] = NO, renumbered to [ 01 / 07 ] - [ 07 / 07 ]).

## Full Example (PRICES Run Instance - Prompts 1 and 2 Resolved)

`````markdown
---
intended_model: glm-5.2
context_window_size: 200k
effort: high
prompt_system: IPPS
---

<!-- Model: glm-5.2 (effort: high, context: 200k). Load grouping (PRMT-SC-07): 10 phases of update-model-registry.md partitioned into 07 prompts (<= 6 items, <= 4 modified files, <= 1 heavy workflow per prompt) so Playwright DOM scraping, Epoch capability matching, JSON updates, API testing, and confirmation-gated distribution stay within single-turn budgets. -->

## Prompt 1 - Bootstrap: Detect Context, Create Run Folder, and Generate Instance

<!-- Detects PRICES and 2026-10-28, creates _2026-10-28_PRICES and _agent_work cards, and instantiates _PROMPTS_2026-10-28_ModelInventoryUpdate.md. -->

```
01-MdlInv-PRICES [ 01 / 07 ] - P3-Bootstrap Detect run parameters, initialize run folder, and generate prompts instance

Session: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate`
Working folder: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate`

Read `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\NOTES.md`, `e:\dev\IPPS\update-model-registry.md` (Placeholders, Sources, Phase 1), and `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Robustness.md`. Treat earlier conversation as compacted. Step P3-Bootstrap.
Planning document: `update-model-registry.md`, Phase 1 setup.

Initialize a datestamped model inventory update run folder and instantiate a ready-to-run prompts file from `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_PROMPTS_ModelInventoryUpdate_TEMPLATE.md`.

1. Detect workspace and run parameters:
   - Resolve `e:\dev\IPPS`, active `e:\dev\IPPS\PromptSystemV4.5`, `e:\dev\IPPS\.devin`, `e:\dev\IPPS\PromptSystemV4.5\skills\llm-evaluation`, and `e:\dev\IPPS\PromptSystemV4.5\skills\write-documents\MODEL_INVENTORY.md`
   - Set `2026-10-28` from request metadata (`YYYY-MM-DD`), `PRICES` (`FULL` | `PRICES` | `NEWMODEL`), `Anthropic, OpenAI, Google, Z.AI`, `ALL`, `NO` (`INCLUDE_SCREENSHOTS`), `UC_ECI` (`CAPABILITY_SCHEME` from `NOTES.md` Key Decisions `DD-01`), and `06` (`TOTAL_PROMPTS` in generated instance after excluding Bootstrap and Prompt 3)
2. Create the isolated run folder `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES` and `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\_agent_work\`
3. Copy `__CARD_MDLINVNTRY-Robustness.md` to `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\_agent_work\__CARD_MDLRGUP-Robustness.md` and initialize `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\_agent_work\__CARD_MDLRGUP-Findings.md` with `# Findings Card: MDLRGUP (2026-10-28 PRICES)`, `## Partition Observations`, `## Unresolved`, and `## Resolved`
4. Generate `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\_PROMPTS_2026-10-28_ModelInventoryUpdate.md` from `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_PROMPTS_ModelInventoryUpdate_TEMPLATE.md`:
   - Exclude Prompt 1 (already executed in this turn)
   - Remove Prompt 3 (`INCLUDE_SCREENSHOTS = NO`), keeping Prompts 2, 4, 5, 6, 7, 8 as `[ 01 / 06 ]` to `[ 06 / 06 ]`
   - Replace all placeholders with resolved values and strip template-instruction XML comments

/write-prompts

Constraints:
- All file operations MUST stay within `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate`
- Do ONLY the numbered items above. Report any item you could not complete as NOT DONE
- Do NOT execute Phase 2 DOM extraction or modify any JSON file in `e:\dev\IPPS\PromptSystemV4.5\skills\llm-evaluation` during Bootstrap
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state: if `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES` already exists, reuse it and overwrite only `_PROMPTS_2026-10-28_ModelInventoryUpdate.md`
- Hang safety: no command may wait for stdin, a pager, or an unbounded child. Banned: see `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Robustness.md`. 120s per-command cap. On cap: kill, record in `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\PROBLEMS.md`, continue

Findings card: Load and update `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\_agent_work\__CARD_MDLRGUP-Findings.md`. Append one Partition Observations line for Bootstrap.

Verify: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES` exists; `__CARD_MDLRGUP-Findings.md` and `__CARD_MDLRGUP-Robustness.md` exist in `_agent_work\`; `_PROMPTS_2026-10-28_ModelInventoryUpdate.md` exists with zero unresolved placeholders.

**STOP.** Report: resolved placeholders (`2026-10-28`, `PRICES`, `Anthropic, OpenAI, Google, Z.AI`, `NO`, `UC_ECI`, `06`), run folder path, generated prompts file path, and total prompts (`06`). Do NOT execute Prompt 2.
```

---

## Prompt 2 - Phase 1 Pre-Flight and Phase 2 DOM Extraction

<!-- Expected state: _2026-10-28_PRICES and run cards exist; executes Phase 1 pre-flight and Phase 2 DOM extraction across Anthropic, OpenAI, Google, Z.AI into _2026-10-28_PRICES. -->

```
01-MdlInv-PRICES [ 02 / 07 ] - Phase 1 + Phase 2 Pre-flight checks and provider DOM extraction

Session: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate`
Working folder: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES`

Read `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\_agent_work\__CARD_MDLRGUP-Robustness.md`, `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\_agent_work\__CARD_MDLRGUP-Findings.md`, `e:\dev\IPPS\update-model-registry.md` (Sources, Pricing Dimensions, Common Procedures, Phase 1, Phase 2), and `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\T02_MDLINVNTRY_ReliableModelInventory_2026-10-28\_INFO_MDLRGUP-MDLINVNTRY-04_SourcesPerField.md` (Section 9 Google Gemini extraction rules). Treat earlier conversation as compacted. Step Phase 1 + Phase 2.
Planning document: `update-model-registry.md`, Phase 1 and Phase 2 (2.1-2.6 + Google G1-G3).

Execute `update-model-registry.md` Phase 1 Pre-Flight Checks and Phase 2 DOM Extraction across `Anthropic, OpenAI, Google, Z.AI` (for `ALL` models), saving all `*-DOM.json` extracts into `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES`.

1. Execute `update-model-registry.md` Phase 1 (Steps 1-2, Gate 1) against `e:\dev\IPPS\PromptSystemV4.5\skills\llm-evaluation\model-pricing.json`, `model-registry.json`, and `model-parameter-mapping.json`
2. Extract Anthropic DOM data (`update-model-registry.md` Phase 2.1 and 2.2) into `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\2026-10-28_Anthropic-Pricing-DOM.json` and `2026-10-28_Anthropic-ModelIDs-DOM.json`
3. Extract OpenAI DOM data (`update-model-registry.md` Phase 2.3, 2.4, and O3 `innerText` extraction) into `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\2026-10-28_OpenAI-Standard-DOM.json`, `2026-10-28_OpenAI-Batch-DOM.json`, and `2026-10-28_OpenAI-Compare-DOM.json`
4. Extract Google Gemini DOM data (`G1` `/pricing` H2 `sectionTables[0]`, `G2` `/models` + `/models/<slug>`, `G3` `/thinking`) into `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\2026-10-28_Google-Pricing-DOM.json` and `2026-10-28_Google-Models-DOM.json`
5. Extract Z.AI DOM data (`update-model-registry.md` Phase 2.5 and 2.6) into `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\2026-10-28_ZAI-Pricing-DOM.json` and `2026-10-28_ZAI-Models-DOM.json`
6. Run `update-model-registry.md` Gate 2 across all saved `2026-10-28_*-DOM.json` files and close the Playwright browser (`browser_close`)

Constraints:
- All file writes MUST stay within `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES` (and `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\PROBLEMS.md` on browser timeout)
- Do ONLY the numbered items above. Report any item you could not complete as NOT DONE
- Do NOT modify any file in `e:\dev\IPPS\PromptSystemV4.5\skills\llm-evaluation`, `e:\dev\IPPS\PromptSystemV4.5\skills\write-documents\MODEL_INVENTORY.md`, or `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\model-sources\`; do NOT run Phase 9 distribution
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state: overwrite `2026-10-28_*-DOM.json` cleanly if already present
- Hang safety: no command may wait for stdin, a pager, or an unbounded child. Banned: see `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\_agent_work\__CARD_MDLRGUP-Robustness.md`. 60s per-page Playwright cap (max 2 attempts per URL). On second failure: record URL in `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\PROBLEMS.md` and continue

Findings card: Load and update `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\_agent_work\__CARD_MDLRGUP-Findings.md`. Append one Partition Observations line.

Verify: Gate 1 and Gate 2 pass; non-empty `2026-10-28_*-DOM.json` files exist in `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES` for Anthropic, OpenAI, Google, and Z.AI; Playwright browser is closed.

**STOP.** Report: items DONE / NOT DONE, DOM files created with model counts per provider, any new or changed models spotted in raw DOM, and Gate 2 status.
```
`````
-->

