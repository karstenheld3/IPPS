---
intended_model: [MODEL]
context_window_size: [CONTEXT_WINDOW_SIZE]
effort: [EFFORT]
prompt_system: IPPS
---

<!-- PROMPTS TEMPLATE
Filename: _PROMPTS_ModelInventoryUpdate_TEMPLATE.md
Instance naming: _PROMPTS_01-MdlInv-[RUN_MODE].md
Location: [SESSION_FOLDER]\_PROMPTS_ModelInventoryUpdate_TEMPLATE.md (template); [RUN_FOLDER]\_agentwork\_PROMPTS_01-MdlInv-[RUN_MODE].md (generated instance)
Specification: [SESSION_FOLDER]\T02_MDLINVNTRY_ReliableModelInventory_2026-10-28\_SPEC_MDLRGUP-MDLINVNTRY-01_GenerationLadder.md [MDLRGUP-MDLINVNTRY-SP01]; design in [SESSION_FOLDER]\_INFO_HOW_TO_ORGANIZE_LLMS_BY_CAPABILITY.md [LLMCAPCLS-IN01]
Previous version: _PROMPTS_ModelInventoryUpdate_TEMPLATE_v0.md (year-letter labels, ECI bands, WF; superseded 2026-11-02; removed by /cleanup 2026-11-02, retrievable from git history)

Purpose: Self-contained recurring pipeline to refresh model-registry.json, model-pricing.json, model-parameter-mapping.json, and MODEL_INVENTORY.md from authoritative provider DOM tables, Epoch ECI scores with confidence intervals, vendor capability statements (generation ladder edges), and the observation ledger (Items).
Replaces the former root-level update-model-registry.md workflow and isolates all run artifacts inside a datestamped run folder.

Run modes ([RUN_MODE]):
- FULL: Complete refresh across all providers in [TARGET_PROVIDERS] — DOM extraction incl. the Devin models page tabs (Prompts 2 and 3), full-page screenshot archive and markdown transcription (Prompt 4), capability evidence: Epoch ECI intervals, new-model metadata, generation edge research (Prompt 5), canonical JSON updates with Gates 5-7 (Prompt 6), live API tests + generation layering + MODEL_INVENTORY.md regeneration + Phase 10 report (Prompt 7), distribution incl. external Lana-V1 config (Prompt 8), and Final Checkpoint (Prompt 9).
- PRICES: Fast price and model metadata refresh — executes Prompts 2, 3, 5 (if capability scheme active), 6, 7, 8, 9. Excludes Prompt 4 (screenshots and image transcription).
- NEWMODEL: Targeted onboarding for newly released model(s) specified in [TARGET_MODELS] — executes Prompts 2 and 3 (affected providers only; a DOM part without an affected provider is removed), 5, 6, 7, 8, 9. Excludes Prompt 4 unless [INCLUDE_SCREENSHOTS] = YES.

Run folder structure:
- Each run creates an isolated datestamped folder in the session root: [SESSION_FOLDER]\_[DATE]_[RUN_MODE]\ (e.g., e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-10-28_PRICES\)
- [RUN_FOLDER]\_agentwork\_PROMPTS_01-MdlInv-[RUN_MODE].md - Generated prompt sequence for this run (excludes Prompt 1 Bootstrap)
- [RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Findings.md - Run-scoped findings card and Partition Observations ledger
- [RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Robustness.md - Run-scoped hang-safety and Playwright robustness card
- [RUN_FOLDER]\[DATE]_Anthropic-Pricing-DOM.json, [DATE]_Anthropic-ModelIDs-DOM.json - Anthropic DOM extracts (A1-A4)
- [RUN_FOLDER]\[DATE]_OpenAI-Standard-DOM.json, [DATE]_OpenAI-Batch-DOM.json, [DATE]_OpenAI-Compare-DOM.json - OpenAI DOM extracts (O1-O3)
- [RUN_FOLDER]\[DATE]_Google-Pricing-DOM.json, [DATE]_Google-Models-DOM.json - Google Gemini DOM extracts (G1-G3)
- [RUN_FOLDER]\[DATE]_ZAI-Pricing-DOM.json, [DATE]_ZAI-Models-DOM.json - Z.AI DOM extracts (Z1-Z3)
- [RUN_FOLDER]\[DATE]_xAI-Pricing-DOM.json, [DATE]_xAI-Models-DOM.json - xAI Grok DOM extracts (X1-X3)
- [RUN_FOLDER]\[DATE]_DeepSeek-Pricing-DOM.json, [DATE]_DeepSeek-Models-DOM.json - DeepSeek DOM extracts (D1-D3)
- [RUN_FOLDER]\[DATE]_Moonshot-Pricing-DOM.json, [DATE]_Moonshot-Models-DOM.json - Moonshot (Kimi) DOM extracts (M1-M3)
- [RUN_FOLDER]\[DATE]_Devin-Models-DOM.json - Devin models page extract (DV1): rows of every tab plus `promotions[]`; input of Section 3.2 Devin Model Deviations (DD-22)
- [RUN_FOLDER]\[DATE]_eci-leaderboard.csv, [DATE]_Epoch-ECI-Match.json - Epoch ECI CSV and per-model score + 95% interval match (when [CAPABILITY_SCHEME] = LADDER)
- [RUN_FOLDER]\[DATE]_Generation-Edges.json - New-model metadata (release_date, uc_class), `release_corrections[]`, `devin_only[]` (rung and release_date of Devin-only models), and edge-case outcomes (higher_than candidates, tie lines, E6 notes) from vendor pages (when [CAPABILITY_SCHEME] = LADDER)
- [RUN_FOLDER]\[DATE]_GenerationLadder.log - layer-generation-ladder.py output: inserted rungs, squeezes, rejected edges, contradictions (when [CAPABILITY_SCHEME] = LADDER)
- [RUN_FOLDER]\[DATE]_ChangeSet.json - Phase 5.0 change set (new registry IDs, new and changed pricing IDs)
- [RUN_FOLDER]\[DATE]_screenshots\ and [RUN_FOLDER]\[DATE]_*.md - Screenshot archive and stitched transcriptions (when [INCLUDE_SCREENSHOTS] = YES)
- [RUN_FOLDER]\[DATE]_RunReport.md - Phase 10 summary report
- Reusable session scripts in [SESSION_FOLDER]:
  - [SESSION_FOLDER]\match-epoch-eci.py - Downloads the Epoch ECI CSV and matches every registry model to its score and 95% interval (eci_score, eci_ci_low, eci_ci_high); lists unmatched registry models and DOM models absent from the registry; reads `released[]` of every DOM extract into `released_in_dom` per model, `new_model_releases{}`, and `release_conflicts[]`; `ExplicitNameMap` maps a rolling alias to the Epoch row of its current snapshot (`deepseek-flash` to `DeepSeek V4.1 Flash 1017`), update the entry when the vendor `MODEL VERSION` changes (Prompt 5)
  - [SESSION_FOLDER]\layer-generation-ladder.py - Insert-only generation layering per [MDLRGUP-MDLINVNTRY-SP01] FR-01/FR-02: builds E1/E2/E3/E5 edges plus higher_than manual edges, validates manual edges (source, accessed, statement), writes generation, generation_evidence, generation_estimated for models without generation, reports squeezes and contradictions, aborts on a cycle. `--bootstrap` was a one-time migration to registry 1.12.0 and is never used in a run; reads the optional registry field `point_version` before its ID regex (rolling aliases such as `deepseek-flash` carry no version in the ID) (Prompt 7)
  - [SESSION_FOLDER]\test-layer-generation-ladder.py - Regression test for layer-generation-ladder.py (NFR-01 bootstrap reproduction of the 2026-10-28 snapshot, insert-only, squeeze, rejected edge, cycle); run after any change to the layering script
  - [SESSION_FOLDER]\update-model-inventory.py - Regenerates [INVENTORY_FILE] Section 3.1 (every text model not `retired`) from the registries: columns Model | Generation | ECI Score | Items | Context | Efforts | In USD | Cache USD | Out USD | Value | Released | Notes (`Released` = registry `release_date` as stored, `YYYY-MM-DD` or `YYYY-MM`, DD-24; `Value` = five-symbol star score followed by the number, for example four full stars and one half star for `(4.4)`, symbols per [DESIGN_INFO] Section 5.6, of the log-scale blended cost `0.8 * In + 0.2 * Out` within the rung, `-` for a one-model rung or equal costs, DD-20; no Devin multipliers, DD-21); with `--devin-dom-file` and `--generation-edges-file` it also regenerates Section 3.2 "Devin Model Deviations" (columns Model | Generation | Items | Efforts | In USD | Cache USD | Out USD | Released | Notes; `Released` = registry `release_date` of the matched model or `devin_only[].release_date`, `-` when none; only Devin models without a registry match or with a different In, Cache read, or Out price, list price after promotions, DD-22); without `--devin-dom-file` Section 3.2 stays unchanged; `Top rung` header line, sorted by 1) Generation descending, 2) Model ascending; Notes text beyond derived values comes from the registry `inventory_note` field; the Efforts cell shows `on/off` for DeepSeek and Moonshot models with method `thinking` and Notes show `off-peak price xN` when the pricing entry has `off_peak_factor` (Prompt 7)
  - [SESSION_FOLDER]\verify-and-distribute-registry.ps1 - Executes deterministic verification Gates 1, 2 (skipped for NEWMODEL; with `-Providers` it requires at least one `[DATE]_[Provider]-*-DOM.json` per target provider; `Devin` needs `[DATE]_Devin-Models-DOM.json` with 3 non-empty tabs), 5, 5.2 (context_window vs vendor values in ChangeSet `contextChecks`), 5.3 (pricing `context_window_k` = floor(registry `context_window` / 1000), `null` when the registry value is `null`), 5.4 (every `release_date` is `YYYY-MM-DD` or `YYYY-MM`, no `release_date_assumed`, DOM `released[]` agrees with the registry), 6, 7, 9, 9.4 (incl. ECI Score, `Released` equals the registry `release_date`, `Value` recomputation, and the Section 3.2 deviation check: every row has no Section 3.1 match or a different price), VerifyAll and Phase 9 distribution (Prompts 2, 3, 6, 7, 8, 9). Gate 9.4 compares `generation` against the committed registry (git HEAD): the registry must be committed before each run
  - [SESSION_FOLDER]\format-model-registry.py - Re-serializes model-registry.json to the canonical 1-line-per-entry layout after any scripted write; `--check` verifies layout without writing (Prompts 6, 7). Never write model-registry.json with json.dump(indent=N) or ConvertTo-Json
- Legacy [SESSION_FOLDER]\model-sources\ is read-only historical archive; never write new files into model-sources\.

Field semantics (single definition; every extraction, check, and inventory column uses exactly these meanings; a field without an entry here must not be written):
- `context_window` = TOTAL context window in tokens as printed on the vendor model page (input plus output, e.g. `400,000 context window`). Never derive an input-only value (window minus max output), never copy a value from another model or a previous run without re-reading the vendor page. The inventory column `Context` shows the same number in K
- `max_output` = max output tokens as printed on the vendor model page; must be an integer in every `model_id_startswith[]` row (a `null` crashes `call-llm.py`); when the vendor prints none, write a documented assumption in the row `vision._note`
- `context_window_k` (pricing file) = floor(`context_window` / 1000) of the registry model with the same ID, `null` when the registry value is `null`; never typed from a vendor page (Gate 5.3 compares both files)
- Vendor prints a rounded window (`1M`, `256K`) on one page and an exact count elsewhere: use the exact count and record both pages; DeepSeek prints only `1M`, so `1000000` is the value
- Prices with a time-of-day tier (DeepSeek peak and off-peak): `input_per_1m`, `cached_per_1m`, `output_per_1m` hold the PEAK price, `off_peak_factor` holds the ratio; the extraction file keeps both
- Model ID that is a rolling alias (`deepseek-flash`): registry `snapshot` holds the vendor `MODEL VERSION`; a changed `snapshot` is a reported event (RunReport Section 4) and `generation` never changes; registry `point_version` groups models of one generation for the layering
- Release date (`release_date`, inventory column `Released`, DD-24): `YYYY-MM-DD` when a vendor page, release note, or announcement prints the day; `YYYY-MM` when only the month is printed or known (DeepSeek and Moonshot changelogs print months); never a guessed day, never the Epoch `date`, the run date, or a family-head date as a stand-in; `release_date_assumed` no longer exists
- Release date flow: every DOM extract lists the dates its pages print in a top-level array `released[]` of `{model_id, released, source_url, raw_text}` (`released` = `YYYY-MM-DD`, `YYYY-MM`, or `null` when the page lists the model without a date; `raw_text` = the printed string); Prompt 5 reconciles `released[]` with the registry and researches the rest; Prompt 6 writes `release_date`; Prompt 7 prints `Released` in Sections 3.1 and 3.2; Gate 5.4 compares DOM and registry, Gate 9.4 compares registry and inventory. A day refines a month of the same month; a different month is a correction that needs a page source and is listed in RunReport Section 4
- Any sourced field (`context_window`, `max_output`, prices, effort levels, `release_date`) of EVERY registry model on a page read in this run is compared against that page; the old value is never trusted because it exists. A differing value is corrected in the same run and listed in the RunReport Section 4
- Cross-source conflict (two pages or a page and the registry disagree and the page is not decisive): record in `[SESSION_FOLDER]\PROBLEMS.md`, keep the old value, never guess
- Verification must be machine-checked wherever a gate can compare two values (Gate 5.2 `context_window`, Gate 9.4 inventory vs registry vs pricing); a manual-only check does not count as verified
- Inventory column `Value` (DD-20, [DESIGN_INFO] Section 5.6) = star score of the blended cost `0.8 * In USD + 0.2 * Out USD` on a log scale within the rung (1.0 most expensive, 5.0 cheapest, nearest 0.5 drawn as stars, one decimal); generated, never typed. `Devin cost` and every Devin multiplier no longer exist anywhere (DD-21)
- Devin Model Deviations (DD-22, [DESIGN_INFO] Section 5.7): the Devin models page `DV1` renders its tables with JavaScript, so every tab (`Self-serve`, `Enterprise (ACUs)`, `Legacy enterprise (credits)`) is clicked and read; plain fetch and the `.md` endpoint give empty tables but complete prose (promotions). Section 3.2 lists only Devin models without a registry match, or with a different In, Cache read, or Out price (tolerance 0.5%, cache write ignored); effort words, `Thinking`, `Fast`, and the dagger are stripped when matching; the row shows the list price after promotions with the promotion and its end date in Notes; an announced price change counts from its effective date, earlier it goes to the RunReport Pending resolution; the credits tab is not used

Placeholder registry:
- [MODEL] - Intended execution model ID from MODEL_INVENTORY.md (e.g., glm-5.2, claude-opus-5)
- [CONTEXT_WINDOW_SIZE] - Model context window size in k (e.g., 200k, 1000k)
- [EFFORT] - Reasoning/thinking effort level (low | medium | high | xhigh | max)
- [WORKSPACE_FOLDER] - Workspace root path (e.g., e:\dev\IPPS)
- [PROMPTSYSTEM_FOLDER] - Canonical PromptSystem folder path in workspace (e.g., e:\dev\IPPS\PromptSystemV4.7)
- [AGENT_FOLDER] - Active agent folder path in workspace (e.g., e:\dev\IPPS\.devin)
- [SKILL_FOLDER] - Canonical llm-tools skill folder holding the model JSONs ([PROMPTSYSTEM_FOLDER]\skills\llm-tools)
- [INVENTORY_FILE] - Canonical MODEL_INVENTORY.md file path ([PROMPTSYSTEM_FOLDER]\skills\llm-tools\MODEL_INVENTORY.md)
- [DESIGN_INFO] - Generation ladder design document ([SESSION_FOLDER]\_INFO_HOW_TO_ORGANIZE_LLMS_BY_CAPABILITY.md); Section 2.2 evidence kinds, Section 2.6 edge cases EC-1 to EC-9
- [SESSION_FOLDER] - Permanent session folder ([WORKSPACE_FOLDER]\_Sessions\!ModelRegistryUpdate)
- [RUN_FOLDER] - Datestamped run folder ([SESSION_FOLDER]\_[DATE]_[RUN_MODE])
- [RUN_MODE] - Execution scope mode (FULL | PRICES | NEWMODEL)
- [DATE] - Run date in YYYY-MM-DD format (e.g., 2026-10-28)
- [TARGET_PROVIDERS] - Providers in scope for this run (e.g., Anthropic, OpenAI, Google, Z.AI, xAI, DeepSeek, Moonshot, Devin); `Devin` = Devin models page (`DV1`), the source of Section 3.2; included by default for FULL and PRICES, for NEWMODEL only when named
- [TARGET_MODELS] - Target model IDs for NEWMODEL mode, or ALL for FULL and PRICES modes
- [INCLUDE_SCREENSHOTS] - Include Prompt 4 screenshot capture and transcription (YES | NO)
- [CAPABILITY_SCHEME] - Capability representation mode (LADDER | NONE); LADDER per DD-10 option 3 and [MDLRGUP-MDLINVNTRY-SP01]
- [TOTAL_PROMPTS] - Total prompt count in the generated instance after excluding Bootstrap and removing conditional prompts (08 for FULL, 07 for PRICES and NEWMODEL, fewer when a DOM part has no target provider)
- [VENV_PYTHON] - Shared Python executable path (e.g., e:\dev\.tools\llm-venv\Scripts\python.exe)
- [KEYS_FILE] - API keys file path (e:\dev\.tools\.api-keys.txt)
- [TRANSCRIPTION_SCRIPT] - Image-to-markdown transcription script ([AGENT_FOLDER]\skills\llm-tools\transcription\transcribe-image-to-markdown.py)

Load-based partition table (PRMT-SC-07 assessment for [MODEL] at [EFFORT] effort, [CONTEXT_WINDOW_SIZE] context):
- Prompt 1 (Bootstrap, ~15k tokens, 4 items): Detect [RUN_MODE], [DATE], [PROMPTSYSTEM_FOLDER], create [RUN_FOLDER] and _agentwork cards, generate instance _PROMPTS_01-MdlInv-[RUN_MODE].md via /write-prompts.
- Prompt 2 (Phases 1 + 2 DOM Extraction part A, ~30k tokens, 5 items): Pre-flight Gate 1 + Playwright DOM extraction for Anthropic A1-A4, OpenAI O1-O3, Google Gemini G1-G3 (providers in [TARGET_PROVIDERS] only).
- Prompt 3 (Phase 2 DOM Extraction part B, ~40k tokens, 6 items): Playwright DOM extraction for Z.AI Z1-Z3, xAI X1-X3, DeepSeek D1-D3, Moonshot M1-M3, Devin DV1 with a click on every tab (providers in [TARGET_PROVIDERS] only) + Gate 2 check.
- Prompt 4 (Phases 3 + 4 Screenshots & Transcription, ~40k tokens, 4 items, Conditional on [INCLUDE_SCREENSHOTS] = YES): Full-page scroll capture, copy to [RUN_FOLDER]\[DATE]_screenshots\, run transcribe-image-to-markdown.py, stitch markdowns, verify Gates 3-4.
- Prompt 5 (Capability Evidence, ~35k tokens, 4 items, Conditional on [CAPABILITY_SCHEME] = LADDER): Download Epoch ECI CSV and match scores + intervals ([DATE]_Epoch-ECI-Match.json); read vendor model pages for new models (release_date, uc_class); resolve edge cases EC-1 to EC-9 into [DATE]_Generation-Edges.json.
- Prompt 6 (Phases 5 + 6 + 7 Canonical JSON Updates, ~35k tokens, 5 items): Derive change set (Phase 5.0), update model-registry.json including eci_score, eci_ci, uc_class, release_date, higher_than (Phase 5 + Gate 5), update model-pricing.json (Phase 6 + Gate 6), verify model-parameter-mapping.json (Phase 7 + Gate 7).
- Prompt 7 (Phase 8 + Phase 9.4 + Phase 10, ~35k tokens, 4 items): Run test-call-llm.py for new enabled models (Phase 8 + Gate 8), run layer-generation-ladder.py insert-only, copy items / scope_guard from observed, set rungs of new Devin-only models, regenerate [INVENTORY_FILE] incl. Value column and Section 3.2 Devin Model Deviations (Phase 9.4 + Gate 9.4), write [RUN_FOLDER]\[DATE]_RunReport.md (Phase 10).
- Prompt 8 (Phase 9 Distribution, ~15k tokens, 2 items): Copy canonical JSONs and [INVENTORY_FILE] to [AGENT_FOLDER]\skills\llm-tools\ (9.1), copy JSONs to external target `e:\Dev\Lana-V1\.agent-data\config` (9.3, always; user decision DD-14 2026-11-02: the entire update chain runs inside the prompts file), run Gate 9 hash check.
- Prompt 9 (Final Checkpoint, ~35k tokens, 4 items): Run VerifyAll, independent Playwright spot check of unchecked registry models against vendor pages, /verify across updated JSONs, [INVENTORY_FILE], and [DATE]_RunReport.md; fix any gaps inline (max 2 cycles); update session NOTES.md.

Conditional prompts:
- Prompt 2 (DOM part A) and Prompt 3 (DOM part B) - remove a part when none of its providers is in [TARGET_PROVIDERS] (part A: Anthropic, OpenAI, Google; part B: Z.AI, xAI, DeepSeek, Moonshot, Devin); a part with some of its providers keeps only those provider items.
- Prompt 4 (Phases 3-4 Screenshots and Transcription) - remove when [INCLUDE_SCREENSHOTS] = NO (default for PRICES and NEWMODEL).
- Prompt 5 (Capability Evidence) - remove when [CAPABILITY_SCHEME] = NONE. With NONE, Prompt 6 writes no capability fields and Prompt 7 skips the layering; existing generation values stay untouched.
- After removing any conditional prompt, renumber remaining prompts sequentially in the generated instance file and update [TOTAL_PROMPTS] in every Prompt Marker (e.g., excluding Bootstrap and removing Prompt 4 yields [ 01 / 07 ] through [ 07 / 07 ]).

CRITICAL - Manual execution only:
- Prompts are designed for manual copy-paste, one prompt per turn, with user review at each gate.
- Agent must NEVER self-execute multiple prompts in a single response (PRMT-EX-01, PRMT-EX-02).
- The **STOP.** marker at the end of every prompt is a hard execution boundary.

Generation ladder invariants (every prompt that touches model-registry.json):
- A `generation` value is written once by layer-generation-ladder.py and never edited by hand or by any other step; the only permitted change is `generation_estimated: true` -> measured (MDLRGUP-MDLINVNTRY-IG-01, IG-02).
- A `higher_than` entry needs `model`, `kind` (E1 | E4), `source` (URL or file), `accessed` (YYYY-MM-DD), `statement` (quote). Without all five the layering script and Gate 9.4 reject it (IG-03).
- Silence from the named source is a tie, never a judgment edge (MDLRGUP-MDLINVNTRY-DD-04). Record the tie with the source that was read.
- Vendor pages are read with Playwright; Epoch ECI is the only benchmark source. Never use Artificial Analysis, LMArena, gap-to-frontier, aggregators, or model recollection (QS-12).

Context management:
- Target: 200k+ token context models at Generation G06 or higher (e.g., glm-5.2 high, claude-opus-5 high).
- In PRICES or NEWMODEL mode (Prompts 2, 3, 5, 6, 7, 8, 9), total token consumption is ~175k and fits in a single session.
- In FULL mode (including Prompt 4 screenshot batches), start a fresh session before Prompt 6 if context exceeds 120k tokens; all Phase 2-4 outputs are persisted on disk in [RUN_FOLDER].
- Later prompts must NOT re-read large files already in conversation history from earlier turns in the same session.
- Playwright MCP calls may hang; enforce a 60s timeout per page and use an isolated browser.newContext() if the default tab has concurrent navigation.

Remove template-instruction XML comments (this block, Conditional comments, and the EXAMPLE block at the end) when instantiating _PROMPTS_01-MdlInv-[RUN_MODE].md; keep the opening load-grouping comment and the 1-sentence commentary comment under each ## Prompt N heading (PRMT-FT-04, PRMT-SC-05, PRMT-SC-07).
-->

<!-- Model: [MODEL] (effort: [EFFORT], context: [CONTEXT_WINDOW_SIZE]). Load grouping (PRMT-SC-07): 10 phases of the model inventory update pipeline partitioned into [TOTAL_PROMPTS] prompts (<= 7 items, <= 4 modified files, <= 1 heavy workflow per prompt) so Playwright DOM scraping, screenshot transcription, Epoch matching and vendor edge research, JSON updates, generation layering, API testing, and distribution stay within single-turn budgets. -->

## Prompt 1 - Bootstrap: Detect Context, Create Run Folder, and Generate Instance

<!-- Detects [RUN_MODE] and [DATE], creates [RUN_FOLDER] and _agentwork cards, and instantiates _PROMPTS_01-MdlInv-[RUN_MODE].md. -->

```
01-MdlInv-[RUN_MODE] [ 01 / 09 ] - P3-Bootstrap Detect run parameters, initialize run folder, and generate prompts instance

Session: `[SESSION_FOLDER]`
Working folder: `[SESSION_FOLDER]`

Read `[SESSION_FOLDER]\NOTES.md`, `[SESSION_FOLDER]\_PROMPTS_ModelInventoryUpdate_TEMPLATE.md` (Placeholders, Run modes, Run folder structure, Generation ladder invariants), and `[SESSION_FOLDER]\_agentwork\__CARD_MDLINVNTRY-Robustness.md`. Treat earlier conversation as compacted. Step P3-Bootstrap.
Planning document: `_PROMPTS_ModelInventoryUpdate_TEMPLATE.md`, Prompt 1 Bootstrap.

Initialize a datestamped model inventory update run folder and instantiate a ready-to-run prompts file from `[SESSION_FOLDER]\_PROMPTS_ModelInventoryUpdate_TEMPLATE.md`.

1. Detect workspace and run parameters:
   - Resolve `[WORKSPACE_FOLDER]`, active `[PROMPTSYSTEM_FOLDER]` (e.g., `PromptSystemV4.7`), `[AGENT_FOLDER]` (`.devin`), `[SKILL_FOLDER]`, `[INVENTORY_FILE]`, and `[DESIGN_INFO]`
   - Set `[DATE]` from request metadata (`YYYY-MM-DD`), `[RUN_MODE]` (`FULL` | `PRICES` | `NEWMODEL`, default `PRICES` unless user specified otherwise), `[TARGET_PROVIDERS]` (default `Anthropic, OpenAI, Google, Z.AI, xAI, DeepSeek, Moonshot, Devin` for `FULL` and `PRICES`; for `NEWMODEL` the providers of `[TARGET_MODELS]`, plus `Devin` only when the user names it), `[TARGET_MODELS]` (`ALL` or user-specified model IDs), `[INCLUDE_SCREENSHOTS]` (`YES` if `FULL`, else `NO`), and `[CAPABILITY_SCHEME]` (from `[SESSION_FOLDER]\NOTES.md` Key Decisions `DD-10`, default `LADDER`)
   - Verify `git status --porcelain -- "[SKILL_FOLDER]\model-registry.json"` is empty (Gate 9.4 compares `generation` against the committed registry); if not empty, stop and report: the registry must be committed before the run
2. Create the isolated run folder `[RUN_FOLDER]` (`[SESSION_FOLDER]\_[DATE]_[RUN_MODE]\`) and `[RUN_FOLDER]\_agentwork\`; if `[INCLUDE_SCREENSHOTS] = YES`, also create `[RUN_FOLDER]\[DATE]_screenshots\` subfolders (`Anthropic-Pricing`, `Anthropic-ModelOverview`, `Anthropic-Deprecations`, `OpenAI-Standard`, `OpenAI-Batch`, `OpenAI-Compare`, `Google-Pricing`, `Google-Models`, `ZAI-Pricing`, `ZAI-Models`, `xAI-Pricing`, `xAI-Models`, `DeepSeek-Pricing`, `Moonshot-Pricing`, `Moonshot-Models`)
3. Copy `__CARD_MDLINVNTRY-Robustness.md` to `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Robustness.md` and initialize `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Findings.md` with `# Findings Card: MDLRGUP ([DATE] [RUN_MODE])`, `## Partition Observations`, `## Unresolved`, and `## Resolved`
4. Generate `[RUN_FOLDER]\_agentwork\_PROMPTS_01-MdlInv-[RUN_MODE].md` from `[SESSION_FOLDER]\_PROMPTS_ModelInventoryUpdate_TEMPLATE.md`:
   - Exclude Prompt 1 (already executed in this turn)
   - Remove conditional prompts that do not apply (`Prompt 4` when `[INCLUDE_SCREENSHOTS] = NO`; `Prompt 5` when `[CAPABILITY_SCHEME] = NONE`; `Prompt 2` or `Prompt 3` when none of its providers is in `[TARGET_PROVIDERS]`; in a kept DOM prompt keep only the provider items in `[TARGET_PROVIDERS]`)
   - Replace all `[PLACEHOLDER]` tokens with resolved values, strip template-instruction XML comments while keeping the opening load-grouping comment and 1-sentence prompt commentary comments, and renumber Prompt Markers sequentially up to `[TOTAL_PROMPTS]`

/write-prompts

Constraints:
- All file operations MUST stay within `[SESSION_FOLDER]`
- Do ONLY the numbered items above. Report any item you could not complete as NOT DONE
- Do NOT execute Phase 2 DOM extraction or modify any JSON file in `[SKILL_FOLDER]` during Bootstrap
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state: if `[RUN_FOLDER]` already exists, reuse it and overwrite only `_PROMPTS_01-MdlInv-[RUN_MODE].md`
- Hang safety: no command may wait for stdin, a pager, or an unbounded child. Banned: see `[SESSION_FOLDER]\_agentwork\__CARD_MDLINVNTRY-Robustness.md`. 120s per-command cap. On cap: kill, record in `[SESSION_FOLDER]\PROBLEMS.md`, continue

Findings card: Load and update `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Findings.md`. Append one Partition Observations line for Bootstrap.

Verify: `[RUN_FOLDER]` exists; `__CARD_MDLRGUP-Findings.md` and `__CARD_MDLRGUP-Robustness.md` exist in `[RUN_FOLDER]\_agentwork\`; `[RUN_FOLDER]\_agentwork\_PROMPTS_01-MdlInv-[RUN_MODE].md` exists with zero unresolved `[PLACEHOLDER]` tokens; `model-registry.json` has no uncommitted changes.

**STOP.** Report: resolved placeholders (`[DATE]`, `[RUN_MODE]`, `[TARGET_PROVIDERS]`, `[INCLUDE_SCREENSHOTS]`, `[CAPABILITY_SCHEME]`, `[TOTAL_PROMPTS]`), `[RUN_FOLDER]` path, generated prompts file path, and total prompts in generated sequence. Do NOT execute Prompt 2.
```

---

## Prompt 2 - Phase 1 Pre-Flight and Phase 2 DOM Extraction Part A (Anthropic, OpenAI, Google)

<!-- Expected state: [RUN_FOLDER] and run cards exist; executes Phase 1 pre-flight and Phase 2 DOM extraction for Anthropic, OpenAI, and Google into [RUN_FOLDER]. -->

```
01-MdlInv-[RUN_MODE] [ 02 / 09 ] - Phase 1 + Phase 2A Pre-flight checks and DOM extraction (Anthropic, OpenAI, Google)

Session: `[SESSION_FOLDER]`
Working folder: `[RUN_FOLDER]`

Read `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Robustness.md`, `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Findings.md`, and `[SESSION_FOLDER]\T02_MDLINVNTRY_ReliableModelInventory_2026-10-28\_INFO_MDLRGUP-MDLINVNTRY-04_SourcesPerField.md` (Sections 1-9 provider extraction rules). Treat earlier conversation as compacted. Step Phase 1 + Phase 2.
Planning document: `_PROMPTS_ModelInventoryUpdate_TEMPLATE.md`, Phase 1 and Phase 2 part A (Anthropic A1-A4, OpenAI O1-O3, Google G1-G3).

Execute Phase 1 Pre-Flight Checks and Phase 2 DOM Extraction part A (Anthropic, OpenAI, Google; only providers that are in `[TARGET_PROVIDERS]`, for `[TARGET_MODELS]`), saving all `*-DOM.json` extracts into `[RUN_FOLDER]`. Release dates (Released column, DD-24): for every model a page lists, add `{model_id, released, source_url, raw_text}` to the top-level array `released[]` of that DOM file; `released` = the printed date as `YYYY-MM-DD`, `YYYY-MM` when the page prints no day, or `null` when the model is listed without a date; `raw_text` = the string as printed; a page without dates still gets `released[]` with `null` values. For every page: navigate, resize to `1920x1080`, dismiss cookie/modal overlays, and expand any `"All models" / "View more" / "Show all" / "Expand"` buttons before extracting `<table>` rows.

1. Execute Phase 1 Pre-Flight Check (Gate 1) via `& "[SESSION_FOLDER]\verify-and-distribute-registry.ps1" -Mode Gate1 -RunFolder "[RUN_FOLDER]" -Date "[DATE]" -SkillFolder "[SKILL_FOLDER]" -InventoryFile "[INVENTORY_FILE]" -AllowSameDateReRun`
2. Extract Anthropic DOM data from canonical URLs (`A1` `https://platform.claude.com/docs/en/about-claude/pricing` columns `Base Input Tokens`, `Cache Hits & Refreshes`, `Output Tokens`; `A2`/`A3` `https://platform.claude.com/docs/en/models/overview` API IDs, context window, max output, thinking support; `A4` `https://platform.claude.com/docs/en/about-claude/model-deprecations` retired/deprecated statuses; fallback to `GET https://api.anthropic.com/v1/models` or `"_note_<alias>": "date suffix pending"` if undated) into `[RUN_FOLDER]\[DATE]_Anthropic-Pricing-DOM.json` and `[RUN_FOLDER]\[DATE]_Anthropic-ModelIDs-DOM.json`
3. Extract OpenAI DOM data from `O1` (`https://developers.openai.com/api/docs/pricing?latest-pricing=standard`, Standard tier tables only — distinguish from Batch tables which are ~50% of Standard; capture both short and long context columns), `O2` (`https://developers.openai.com/api/docs/pricing?latest-pricing=batch`), and `O3` (`https://developers.openai.com/api/docs/models/compare`, using `document.body.innerText` search around `'Window'` / `'max output'` since O3 uses div cards rather than `<table>`) into `[RUN_FOLDER]\[DATE]_OpenAI-Standard-DOM.json`, `[RUN_FOLDER]\[DATE]_OpenAI-Batch-DOM.json`, and `[RUN_FOLDER]\[DATE]_OpenAI-Compare-DOM.json`
4. Extract Google Gemini DOM data per `_INFO_MDLRGUP-MDLINVNTRY-04_SourcesPerField.md` Section 9:
   - `G1` (`https://ai.google.dev/gemini-api/docs/pricing`): iterate per-model `<h2>` headings and extract `sectionTables[0]` (Standard tier, parsing current price before any scheduled date increase and separating `<=200k` vs `>200k` rows) into `[RUN_FOLDER]\[DATE]_Google-Pricing-DOM.json`
   - `G2` (`https://ai.google.dev/gemini-api/docs/models` + per-model `/models/<slug>` subpages for `Token limits[*]`) and `G3` (`https://ai.google.dev/gemini-api/docs/thinking` table of `Levels Supported`) into `[RUN_FOLDER]\[DATE]_Google-Models-DOM.json`
5. Close the Playwright browser (`browser_close`)

Constraints:
- All file writes MUST stay within `[RUN_FOLDER]` (and `[SESSION_FOLDER]\PROBLEMS.md` on browser timeout)
- Do ONLY the numbered items above. Report any item you could not complete as NOT DONE
- Do NOT modify any file in `[SKILL_FOLDER]`, `[INVENTORY_FILE]`, or `[SESSION_FOLDER]\model-sources\`; do NOT run Phase 9 distribution
- If Playwright MCP default tab experiences concurrent navigation interference, run extractions inside an isolated `page.context().browser().newContext()` and close it immediately after extraction
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state: overwrite `[RUN_FOLDER]\[DATE]_*-DOM.json` cleanly if already present
- Hang safety: no command may wait for stdin, a pager, or an unbounded child. Banned: see `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Robustness.md`. 60s per-page Playwright cap (max 2 attempts per URL). On second failure: record URL in `[SESSION_FOLDER]\PROBLEMS.md` and continue with remaining providers

Findings card: Load and update `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Findings.md`. Append one Partition Observations line and record any URL redirects or DOM selector changes.

Verify: Gate 1 passes; non-empty `[DATE]_*-DOM.json` files exist in `[RUN_FOLDER]` for every part A provider in `[TARGET_PROVIDERS]`; every such file has a `released[]` array whose `released` values are `YYYY-MM-DD`, `YYYY-MM`, or `null`; Playwright browser is closed.

**STOP.** Report: items DONE / NOT DONE, DOM files created with model counts per provider (and how many have a printed release date), and any new or changed models spotted in raw DOM.
```

---

## Prompt 3 - Phase 2 DOM Extraction Part B (Z.AI, xAI, DeepSeek, Moonshot, Devin) and Gate 2

<!-- Expected state: Part A DOM extracts are in [RUN_FOLDER]; executes Phase 2 DOM extraction for Z.AI, xAI, DeepSeek, Moonshot, and the Devin models page and verifies Gate 2 across all target providers. -->

```
01-MdlInv-[RUN_MODE] [ 03 / 09 ] - Phase 2B DOM extraction (Z.AI, xAI, DeepSeek, Moonshot, Devin) and Gate 2

Session: `[SESSION_FOLDER]`
Working folder: `[RUN_FOLDER]`

Read `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Robustness.md`, `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Findings.md`, `[SESSION_FOLDER]\T02_MDLINVNTRY_ReliableModelInventory_2026-10-28\_INFO_MDLRGUP-MDLINVNTRY-04_SourcesPerField.md` (Sections 1-9 provider extraction rules), `[SESSION_FOLDER]\T03_MDLPRVEXT_DeepSeekKimiIntegration_2026-11-17\_INFO_MDLRGUP-MDLPRVEXT-01_DeepSeekKimiIntegration.md` (Sections 1 and 2.4 DeepSeek and Moonshot pages), and `[DESIGN_INFO]` Section 5.7 (Devin Model Deviations). Treat earlier conversation as compacted. Step Phase 2B.
Planning document: `_PROMPTS_ModelInventoryUpdate_TEMPLATE.md`, Phase 2 part B (Z.AI Z1-Z3, xAI X1-X3, DeepSeek D1-D3, Moonshot M1-M3, Devin DV1).

Execute Phase 2 DOM Extraction part B (Z.AI, xAI, DeepSeek, Moonshot, Devin; only providers that are in `[TARGET_PROVIDERS]`, for `[TARGET_MODELS]`), saving all `*-DOM.json` extracts into `[RUN_FOLDER]`. Release dates (Released column, DD-24): for every model a page lists, add `{model_id, released, source_url, raw_text}` to the top-level array `released[]` of that DOM file; `released` = the printed date as `YYYY-MM-DD`, `YYYY-MM` when the page prints no day (the DeepSeek `D2` updates and Moonshot `M2` changelog print months), or `null` when the model is listed without a date; `raw_text` = the string as printed; a page without dates still gets `released[]` with `null` values. For every page: navigate, resize to `1920x1080`, dismiss cookie/modal overlays, and expand any `"All models" / "View more" / "Show all" / "Expand"` buttons before extracting `<table>` rows.

1. Extract Z.AI DOM data from `Z1` (`https://docs.z.ai/guides/overview/pricing`, use first list price only when dual promo prices appear such as `$0.15 $0.075`; store `"Free"` as `0.00`; implicit caching is 50% of input) and `Z2` (`https://docs.z.ai/guides/overview/overview`, text and vision model tables with context window and thinking/reasoning_effort support) into `[RUN_FOLDER]\[DATE]_ZAI-Pricing-DOM.json` and `[RUN_FOLDER]\[DATE]_ZAI-Models-DOM.json`
2. Extract xAI Grok DOM data from `X1` (`https://docs.x.ai/developers/pricing`, table idx 0 text models including short `<200k` and long `>=200k` context tiers), `X2` (`https://docs.x.ai/developers/models`), and `X3` (`https://docs.x.ai/developers/model-capabilities/text/reasoning`) into `[RUN_FOLDER]\[DATE]_xAI-Pricing-DOM.json` and `[RUN_FOLDER]\[DATE]_xAI-Models-DOM.json`
3. Extract DeepSeek DOM data: `D1` (`https://api-docs.deepseek.com/quick_start/pricing`, flat text of the `Model Details` section or the `.md` endpoint; the table uses `rowspan`, so do not read cell positions: capture API names with the footnote `(1)` alias text, `MODEL VERSION`, context, max output, features, PEAK and OFF-PEAK prices for cache hit, cache miss, and output, and the footnote with the peak hours) into `[RUN_FOLDER]\[DATE]_DeepSeek-Pricing-DOM.json`; `D2` (`https://api-docs.deepseek.com/updates`, newest entries until every registered DeepSeek model has a release date; record the status of legacy names) and `D3` (`https://api-docs.deepseek.com/guides/thinking_mode`, effort values and mapping table) into `[RUN_FOLDER]\[DATE]_DeepSeek-Models-DOM.json`
4. Extract Moonshot (Kimi) DOM data: `M1` (`https://platform.kimi.ai/docs/pricing/chat`, both tables from the DOM, never the `.md` endpoint whose tables are empty, plus the prose line above each table with the series context window and the K2 retirement notice) into `[RUN_FOLDER]\[DATE]_Moonshot-Pricing-DOM.json`; `M2` (`https://platform.kimi.ai/docs/models`, available and deprecated model tables; `https://platform.kimi.ai/docs/platform-changelog.md` release months) and `M3` (`https://platform.kimi.ai/docs/api/models-overview.md`, parameter table: `reasoning_effort`, `thinking`, fixed `temperature`) into `[RUN_FOLDER]\[DATE]_Moonshot-Models-DOM.json`
5. Extract Devin model prices `DV1` (`https://docs.devin.ai/desktop/models`; only when `Devin` is in `[TARGET_PROVIDERS]`): the tables are rendered by JavaScript, so wait for `networkidle`, then for EACH of the 3 tabs (`role=tab`: `Self-serve`, `Enterprise (ACUs)`, `Legacy enterprise (credits)`) click it, wait 2s, and read every row of the visible `table` (header row included, cell text as printed: `$0.50`, `Free`, `—`, `*`, credits numbers); read the prose from `https://docs.devin.ai/desktop/models.md` (its tables are empty, its prose is complete) and record every free period, discount, and dated price change as `promotions[]` entries (`model`, `tab`, `kind` free | discount | change, `list_input`, `list_cache_read`, `list_output`, `until` or `from`, `quote`) together with the page sentence `prices as of [date]`; write `[RUN_FOLDER]\[DATE]_Devin-Models-DOM.json` with keys `tabs` (one row list per tab), `promotions`, `page_price_date`, `released[]` (one entry per model family row, `released` `null` unless the page prints a date); stop and report NOT DONE when a tab has no data rows. If the Playwright MCP browser reports `Browser is already in use`, run the same steps with Python Playwright (`p.chromium.launch(channel="chrome", headless=True)`) from `[VENV_PYTHON]` in the script `[RUN_FOLDER]\_agentwork\.tmp_devin_[HHmmss].py`, started through the supervised runner (tested 2026-11-18: 17, 17, and 14 data rows)
6. Close the Playwright browser (`browser_close`) and run Gate 2 via `& "[SESSION_FOLDER]\verify-and-distribute-registry.ps1" -Mode Gate2 -RunFolder "[RUN_FOLDER]" -Date "[DATE]" -SkillFolder "[SKILL_FOLDER]" -InventoryFile "[INVENTORY_FILE]" -RunMode "[RUN_MODE]" -Providers "[TARGET_PROVIDERS]"` (Gate 2 requires at least one `[DATE]_[Provider]-*-DOM.json` per target provider and reports SKIPPED for `NEWMODEL`: DOM extracts are optional there, DD-01 2026-11-16; for `Devin` it requires `[DATE]_Devin-Models-DOM.json` with 3 non-empty tabs)

Constraints:
- All file writes MUST stay within `[RUN_FOLDER]` (and `[SESSION_FOLDER]\PROBLEMS.md` on browser timeout)
- Do ONLY the numbered items above. Report any item you could not complete as NOT DONE
- Do NOT modify any file in `[SKILL_FOLDER]`, `[INVENTORY_FILE]`, or `[SESSION_FOLDER]\model-sources\`; do NOT run Phase 9 distribution
- If Playwright MCP default tab experiences concurrent navigation interference, run extractions inside an isolated `page.context().browser().newContext()` and close it immediately after extraction
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state: overwrite `[RUN_FOLDER]\[DATE]_*-DOM.json` cleanly if already present
- Hang safety: no command may wait for stdin, a pager, or an unbounded child. Banned: see `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Robustness.md`. 60s per-page Playwright cap (max 2 attempts per URL). On second failure: record URL in `[SESSION_FOLDER]\PROBLEMS.md` and continue with remaining providers

Findings card: Load and update `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Findings.md`. Append one Partition Observations line and record any URL redirects or DOM selector changes.

Verify: Gate 2 passes (`FULL`, `PRICES`: non-empty `[DATE]_*-DOM.json` files exist in `[RUN_FOLDER]` for every provider in `[TARGET_PROVIDERS]`, parts A and B) or reports SKIPPED (`NEWMODEL`); `[DATE]_Devin-Models-DOM.json` holds 3 non-empty tabs when `Devin` is a target; every part B DOM file has a `released[]` array whose `released` values are `YYYY-MM-DD`, `YYYY-MM`, or `null`; Playwright browser is closed.

**STOP.** Report: items DONE / NOT DONE, DOM files created with model counts per provider (Devin: data rows per tab and promotion count; per provider how many models have a printed release date), any new or changed models spotted in raw DOM, and Gate 2 status.
```

---

<!-- Conditional: include Prompt 4 only when [INCLUDE_SCREENSHOTS] = YES (default for [RUN_MODE] = FULL; remove for PRICES and NEWMODEL and renumber remaining prompts). -->

## Prompt 4 - Phases 3 and 4 Screenshot Archive and Markdown Transcription

<!-- Expected state: Phase 2 saved authoritative DOM JSONs in [RUN_FOLDER]; captures full-page screenshots and markdown transcriptions for the historical visual archive. -->

```
01-MdlInv-[RUN_MODE] [ 04 / 09 ] - Phase 3 + Phase 4 Full-page screenshot capture and markdown transcription

Session: `[SESSION_FOLDER]`
Working folder: `[RUN_FOLDER]`

Read `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Robustness.md` and `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Findings.md`. Treat earlier conversation as compacted. Step Phase 3 + Phase 4.
Planning document: `_PROMPTS_ModelInventoryUpdate_TEMPLATE.md`, Phase 3 and Phase 4.

Execute Phase 3 (Screenshot Archive) and Phase 4 (Transcribe Screenshots) into `[RUN_FOLDER]`.

1. Execute Phase 3 full-page scroll capture (`1920x1080` viewport, JPEG quality 90, scrolling `window` or `.docs-scroll-container` on OpenAI `O1`/`O2` by viewport height increments) for `A1`, `A3`, `A4`, `O1`, `O2`, `O3`, `G1`, `G2`, `Z1`, `Z2`, `X1`, `X2`, `D1`, `M1`, `M2`, copying captured `.jpg` files from Playwright's default output directory into `[RUN_FOLDER]\[DATE]_screenshots\<SourceFolder>\`
2. Run Gate 3: verify each screenshot subfolder in `[RUN_FOLDER]\[DATE]_screenshots\` has `>= 1` `.jpg` and spot-check that output price columns are not clipped; close Playwright (`browser_close`)
3. Execute Phase 4.1 using `& "[VENV_PYTHON]" "[TRANSCRIPTION_SCRIPT]" --input-folder <folder> --output-folder <folder> --model gpt-5-mini --initial-candidates 1 --keys-file "[KEYS_FILE]" --force` across each populated `[RUN_FOLDER]\[DATE]_screenshots\<SourceFolder>`
4. Execute Phase 4.2 to stitch sorted per-page `.md` files into `[RUN_FOLDER]\[DATE]_<Source>.md`, remove temporary per-page `.md` and `_batch_summary.json` files, and verify Gate 4 (combined markdowns exist for each captured source)

Constraints:
- All file writes MUST stay within `[RUN_FOLDER]`
- Do ONLY the numbered items above. Report any item you could not complete as NOT DONE
- Do NOT modify canonical JSONs in `[SKILL_FOLDER]` or run Phase 9 distribution
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state: `--force` overwrites partial transcriptions cleanly
- Hang safety: no command may wait for stdin, a pager, or an unbounded child. Banned: see `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Robustness.md`. 60s per-page Playwright cap, 180s per-folder transcription cap. On cap: kill, record in `[SESSION_FOLDER]\PROBLEMS.md`, continue (Gate 4 does not block Phase 5)

Findings card: Load and update `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Findings.md`. Append one Partition Observations line.

Verify: Gate 3 and Gate 4 pass; `[RUN_FOLDER]\[DATE]_screenshots\` subfolders contain `.jpg` files and stitched `[RUN_FOLDER]\[DATE]_*.md` files exist; Playwright browser is closed.

**STOP.** Report: items DONE / NOT DONE, screenshot counts per folder, stitched markdown files created, and Gate 3-4 status.
```

---

<!-- Conditional: include Prompt 5 when [CAPABILITY_SCHEME] = LADDER; omit if [CAPABILITY_SCHEME] = NONE and renumber remaining prompts. -->
<!-- Provider DOM extracts are in [RUN_FOLDER]. Next prompt fetches the Epoch ECI CSV (scores and 95% intervals), reads vendor model pages for new models, and resolves the generation edge cases into [DATE]_Generation-Edges.json. -->

## Prompt 5 - Capability Evidence: Epoch ECI Intervals, New-Model Metadata, and Generation Edge Research

```
01-MdlInv-[RUN_MODE] [ 05 / 09 ] - P3-CapEvidence Refresh Epoch ECI intervals and resolve generation edge cases for new models

Session: `[SESSION_FOLDER]`
Working folder: `[RUN_FOLDER]`

Read `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Robustness.md`, `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Findings.md`, `[SESSION_FOLDER]\T02_MDLINVNTRY_ReliableModelInventory_2026-10-28\_INFO_MDLRGUP-MDLINVNTRY-04_SourcesPerField.md` (Section 6 Capability Evidence), and `[DESIGN_INFO]` Sections 2.2 (evidence kinds E1-E6) and 2.6 (edge cases EC-1 to EC-9). Treat earlier conversation as compacted. Step Capability Evidence.
Planning document: `_PROMPTS_ModelInventoryUpdate_TEMPLATE.md`, Prompt 5 Capability Evidence.

Refresh the Epoch ECI score and 95% interval of every registry model, collect `release_date` and `uc_class` for models that are new in `[RUN_FOLDER]\[DATE]_*-DOM.json`, reconcile the DOM `released[]` values with the registry `release_date`, and resolve every generation edge case for those models from vendor pages, writing the outcomes to `[RUN_FOLDER]\[DATE]_Generation-Edges.json`. No registry file is modified in this prompt.

1. Run `[VENV_PYTHON] "[SESSION_FOLDER]\match-epoch-eci.py" --run-folder "[RUN_FOLDER]" --date "[DATE]" --registry-file "[SKILL_FOLDER]\model-registry.json" --download` to download `https://epoch.ai/data/eci_scores.csv` into `[RUN_FOLDER]\[DATE]_eci-leaderboard.csv` and generate `[RUN_FOLDER]\[DATE]_Epoch-ECI-Match.json` (`model_id`, `epoch_name`, `eci_score`, `eci_ci_low`, `eci_ci_high` per matched model; `unmatched[]` registry models without an Epoch row; `new_models[]` = IDs present in `[RUN_FOLDER]\[DATE]_*-DOM.json` but absent from the registry; `released_in_dom` per model, `new_model_releases{}`, and `release_conflicts[]` from the `released[]` arrays of the DOM extracts)
2. For every ID in `new_models[]` (and every `[TARGET_MODELS]` entry in `NEWMODEL` mode): open the vendor model overview page with Playwright and record into `[RUN_FOLDER]\[DATE]_Generation-Edges.json` under `new_models` the `release_date` (first `new_model_releases{}` of the match file, else the vendor "Released" field, release note, or announcement; `YYYY-MM-DD` when the page prints the day, `YYYY-MM` when it prints only the month; no page prints a date = key absent plus a line in `unresolved[]`, never an Epoch `date`, run date, or family-head date as a stand-in, DD-24), `uc_class` (`UC-1 Apex` | `UC-2 Flagship` | `UC-3 Balanced` | `UC-4 Efficient` from the vendor's tier wording, checked against the price order within the point version), the page URL, and the access date. Also write `release_corrections[]` entries `{model_id, old, new, source, accessed}` (EC-9): 1) every `release_conflicts[]` entry of the match file, resolved by the vendor page (two pages disagree = `[SESSION_FOLDER]\PROBLEMS.md` entry, no correction); 2) in `FULL` mode every registry model with a month-only `release_date` and `released_in_dom` `null`, in other modes only those in `[TARGET_MODELS]`: open its vendor overview, release note, or announcement and record the day when the page prints it (`new` = `YYYY-MM-DD` inside the old month = refinement; another month = correction). DeepSeek and Moonshot pages print release months only in update and changelog pages: `YYYY-MM`. For a rolling alias record the vendor `MODEL VERSION` as `snapshot`
3. Resolve the edge cases of `[DESIGN_INFO]` Section 2.6 for every ID in `new_models[]` and for every existing model whose `eci_ci` appears for the first time in this run:
   - EC-1 (Apex or Flagship of a new point version): read the vendor's model-selection guidance; an escalation statement ("start with X; use Y when X at higher effort still falls short") = `higher_than` candidate `{x, model, kind: "E1", source, accessed, statement}`; a parity statement or silence = `ties[]` line `{x, model, source, accessed, reason}`
   - EC-2 (new member of an existing tier family): read the successor's "what's new" or migration page; "extends" / "succeeds" at same tier and price = inherit the predecessor's recorded edges as candidates with that page as source
   - EC-3 (restricted-access twin): "same underlying model" / "same capabilities" = `ties[]` line with `kind: "E5"`
   - EC-4 (specialized Apex without score): announcement naming the base; more capable and higher price = `E1` candidate over the base; domain variant at equal price = `E5` tie
   - EC-5 (unscored Efficient or vision model): tier wording and price order = `estimates[]` line `{model, sibling, note: "E6"}`
   - Write every outcome, including "source silent → tie", with URL and access date; never leave a new model without an entry
4. Verify `[RUN_FOLDER]\[DATE]_Epoch-ECI-Match.json` and `[RUN_FOLDER]\[DATE]_Generation-Edges.json` are valid JSON; every `new_models[]` ID has `uc_class` and at least one entry in `higher_than_candidates[]`, `ties[]`, or `estimates[]`, and has a `release_date` matching `YYYY-MM-DD` or `YYYY-MM` or a line in `unresolved[]`; every `release_corrections[]` entry has a source and an access date; every `higher_than_candidates[]` entry has all five fields; close Playwright (`browser_close`)

Constraints:
- All file writes MUST stay within `[RUN_FOLDER]`
- Do ONLY the numbered items above. Report any item you could not complete as NOT DONE
- Read ECI from `https://epoch.ai/eci` (CSV download) only; never use Artificial Analysis Intelligence Index, LMArena Elo, gap-to-frontier, aggregators, or model recollection (`QS-12`)
- Vendor pages with Playwright only; quote statements verbatim; silence = tie (MDLRGUP-MDLINVNTRY-DD-04)
- Do NOT modify `[SKILL_FOLDER]` JSONs or `[INVENTORY_FILE]` in this prompt
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state: overwrite `[RUN_FOLDER]\[DATE]_Epoch-ECI-Match.json` and `[RUN_FOLDER]\[DATE]_Generation-Edges.json` cleanly
- Hang safety: no command may wait for stdin, a pager, or an unbounded child. Banned: see `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Robustness.md`. 60s Playwright/download cap (max 2 attempts per URL). On CSV failure: record in `[SESSION_FOLDER]\PROBLEMS.md`, fall back to the most recent `*_Epoch-ECI-Match.json` in `[SESSION_FOLDER]`, and continue. On vendor page failure: record the model as `ties[]` with `reason: "source unreachable"` and the URL in `[SESSION_FOLDER]\PROBLEMS.md`

Findings card: Load and update `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Findings.md`. Append one Partition Observations line; note new models without an Epoch row and every edge case resolved as a tie because the source was silent.

Verify: both JSON files exist and are valid; every `new_models[]` ID has `uc_class`, an edge-case entry, and a `release_date` (`YYYY-MM-DD` or `YYYY-MM`) or an `unresolved[]` line; `release_conflicts[]` of the match file is empty or fully covered by `release_corrections[]`; Playwright browser is closed.

**STOP.** Report: items DONE / NOT DONE, models matched / unmatched in `[DATE]_Epoch-ECI-Match.json`, new models with their `release_date` (day or month only) and `uc_class`, month-only models refined to a day, `higher_than` candidates (x > model, kind, source), ties, E6 estimates, and EC-9 release-date corrections.
```

---

## Prompt 6 - Phases 5, 6, and 7 Canonical JSON Updates and Gates 5-7

<!-- Expected state: DOM extracts ([DATE]_*-DOM.json), Epoch matches ([DATE]_Epoch-ECI-Match.json), and edge outcomes ([DATE]_Generation-Edges.json) are in [RUN_FOLDER]; updates the three canonical JSON files in [SKILL_FOLDER] and verifies Gates 5, 6, and 7. -->

```
01-MdlInv-[RUN_MODE] [ 06 / 09 ] - Phase 5 + Phase 6 + Phase 7 Update canonical JSONs and verify Gates 5-7

Session: `[SESSION_FOLDER]`
Working folder: `[RUN_FOLDER]`

Read `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Robustness.md` and `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Findings.md`. Treat earlier conversation as compacted. Step Phase 5 + Phase 6 + Phase 7.
Planning document: `_PROMPTS_ModelInventoryUpdate_TEMPLATE.md`, Prompt 6 (Phases 5, 6, and 7).

Execute Phases 5, 6, and 7 using the DOM extracts, Epoch matches, and edge outcomes in `[RUN_FOLDER]` to update `[SKILL_FOLDER]\model-registry.json`, `[SKILL_FOLDER]\model-pricing.json`, and `[SKILL_FOLDER]\model-parameter-mapping.json`, and verify Gates 5, 6, and 7. `generation`, `generation_evidence`, and `generation_estimated` are NOT written here (Prompt 7 layering).

1. Phase 5.0 (Derive Change Set): compare `[RUN_FOLDER]\[DATE]_*-DOM.json` against `[SKILL_FOLDER]\model-registry.json` and `[SKILL_FOLDER]\model-pricing.json`; write `newRegistryIds` (in DOM, absent from `models[]`), `newPricingIds` (in DOM, absent from `model-pricing.json`), and `changedPricingIds` (DOM price differs from current `model-pricing.json`) to `[RUN_FOLDER]\[DATE]_ChangeSet.json`
2. Phase 5.1-5.3 (`[SKILL_FOLDER]\model-registry.json`): insert new models at the top of their provider group (`"enabled": false, "status": "untested"`, or `"enabled": true` for testable text models) with `release_date` (`YYYY-MM-DD` or `YYYY-MM`; a new model without a date in `[RUN_FOLDER]\[DATE]_Generation-Edges.json` stops this item as NOT DONE with a `[SESSION_FOLDER]\PROBLEMS.md` entry) and `uc_class` from the same file's `new_models`; set `context_window` per Field semantics, plus `snapshot` and `point_version` for rolling aliases and DeepSeek and Moonshot generations; for a new provider prefix add the `model_id_startswith[]` row with integer `max_output`; re-read `context_window` of EVERY registry model that has a row on a vendor page read in this run (not only new models) and correct differing values; write one `{model_id, vendor_context_window, source, checked}` entry per model into `contextChecks` of `[RUN_FOLDER]\[DATE]_ChangeSet.json` and list models without a vendor value in `contextUnverified`; set `"status": "deprecated", "enabled": false` for newly deprecated models (never remove existing models); refresh `eci_score` and `eci_ci` `[low, high]` for every matched model from `[RUN_FOLDER]\[DATE]_Epoch-ECI-Match.json` (`eci_ci: null` for unmatched); copy every `higher_than_candidates[]` entry onto its `x` model as a `higher_than` item `{model, kind, source, accessed, statement}`; set `release_date` of every registry model from `release_corrections[]` of `[RUN_FOLDER]\[DATE]_Generation-Edges.json` and from a DOM `released[]` value that is more exact than the registry value (day for month of the same month; another month needs the `source` of the correction and a RunReport Section 4 line), and never write or keep `release_date_assumed` (DD-24); update `model_id_startswith[]` prefixes if needed; bump `_version` patch and `_updated` to `[DATE]`; then run `[VENV_PYTHON] "[SESSION_FOLDER]\format-model-registry.py" --registry-file "[SKILL_FOLDER]\model-registry.json"` to restore the 1-line-per-entry layout
3. Phase 6 (`[SKILL_FOLDER]\model-pricing.json`): add `newPricingIds` and update `changedPricingIds` using Standard tier prices across `openai`, `anthropic`, `google`, `zai`, `xai`, `deepseek`, and `moonshot` (`{input_per_1m, cached_per_1m|omit if null, output_per_1m, long_context|omit if no long tier, context_window_k, currency: "USD"}`; never remove legacy entries; for Z.AI use first list price only and `0.00` for free models; for DeepSeek write PEAK prices plus `off_peak_factor`; `context_window_k` = floor(registry `context_window` / 1000)), bump `last_updated` to `[DATE]`, and update `sources` array if URLs changed
4. Phase 7 (`[SKILL_FOLDER]\model-parameter-mapping.json`): verify every `method` in `model_id_startswith[]` maps to an existing key in `effort_mapping`; bump `_version` and `_updated` only if `model-parameter-mapping.json` was modified
5. Run Gates 5, 5.2, 5.3, 5.4, 6, and 7 (Gate 5.4 = every registry `release_date` is `YYYY-MM-DD` or `YYYY-MM`, no `release_date_assumed` key remains, and every DOM `released[]` value equals the registry value or is the month of the registry day; Gate 5.3 = pricing `context_window_k` equals floor(registry `context_window` / 1000); Gate 5.2 = every `contextChecks` entry equals the registry `context_window`; every new model with a `context_window` is in `contextChecks` or `contextUnverified`) via `& "[SESSION_FOLDER]\verify-and-distribute-registry.ps1" -Mode Gate567 -RunFolder "[RUN_FOLDER]" -Date "[DATE]" -SkillFolder "[SKILL_FOLDER]" -InventoryFile "[INVENTORY_FILE]"`

Constraints:
- All file operations MUST stay within `[RUN_FOLDER]` and the three canonical JSON files in `[SKILL_FOLDER]` (`[SKILL_FOLDER]\model-registry.json`, `[SKILL_FOLDER]\model-pricing.json`, `[SKILL_FOLDER]\model-parameter-mapping.json`)
- Do ONLY the numbered items above. Report any item you could not complete as NOT DONE
- Never remove existing or deprecated models from `model-registry.json` or `model-pricing.json`
- Never write, edit, or delete `generation`, `generation_evidence`, or `generation_estimated` on any model (MDLRGUP-MDLINVNTRY-IG-01); never write a `higher_than` item without all five fields (IG-03)
- Do NOT edit `[AGENT_FOLDER]` directly and do NOT execute Phase 9 distribution in this prompt
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state: JSON updates are idempotent and verified by Gates 5-7
- Hang safety: no command may wait for stdin, a pager, or an unbounded child. Banned: see `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Robustness.md`. 120s per-command cap. On cap: kill, record in `[SESSION_FOLDER]\PROBLEMS.md`, continue

Findings card: Load and update `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Findings.md`. Append one Partition Observations line and record any prefix gaps or new effort methods.

Verify: `[RUN_FOLDER]\[DATE]_ChangeSet.json` exists with `contextChecks`; Gates 5, 5.2, 5.3, 5.4, 6, and 7 pass with exit code 0; `format-model-registry.py --check` passes; `_updated` / `last_updated` in modified `[SKILL_FOLDER]` JSONs equal `[DATE]`; `git --no-pager diff --stat -- "[SKILL_FOLDER]\model-registry.json"` shows no line where a `"generation":` value changed.

**STOP.** Report: items DONE / NOT DONE, `newRegistryIds` count, `newPricingIds` count, `changedPricingIds` count, `higher_than` items written, `eci_ci` values refreshed, any prefix gaps, and Gate 5-7 results.
```

---

## Prompt 7 - Phase 8 Live API Tests, Phase 9.4 Generation Layering and Inventory Regeneration, and Phase 10 Report

<!-- Expected state: Canonical JSONs in [SKILL_FOLDER] passed Gates 5-7 and carry eci_ci, uc_class, release_date, higher_than for new models; runs Phase 8 live API tests, Phase 9.4 insert-only generation layering and [INVENTORY_FILE] regeneration, and Phase 10 summary report. -->

```
01-MdlInv-[RUN_MODE] [ 07 / 09 ] - Phase 8 + Phase 9.4 + Phase 10 Test new models, layer generation ladder, regenerate MODEL_INVENTORY.md, and write report

Session: `[SESSION_FOLDER]`
Working folder: `[RUN_FOLDER]`

Read `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Robustness.md`, `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Findings.md`, `[RUN_FOLDER]\[DATE]_ChangeSet.json`, `[RUN_FOLDER]\[DATE]_Generation-Edges.json` (`ties`, `estimates`), `[RUN_FOLDER]\[DATE]_Devin-Models-DOM.json` (when present), and `[INVENTORY_FILE]` Sections 1-2. Treat earlier conversation as compacted. Step Phase 8 + Phase 9.4 + Phase 10.
Planning document: `_PROMPTS_ModelInventoryUpdate_TEMPLATE.md`, Prompt 7 (Phase 8, Phase 9.4, and Phase 10).

Execute Phase 8 (Test New Models), Phase 9.4 (Generation Layering and `MODEL_INVENTORY.md` Regeneration), and Phase 10 (Report), saving the run summary report to `[RUN_FOLDER]\[DATE]_RunReport.md`.

1. Execute Phase 8: for each model in `newRegistryIds` (`[RUN_FOLDER]\[DATE]_ChangeSet.json`) enabled for testing, run `[VENV_PYTHON] "[SKILL_FOLDER]\test-call-llm.py" --keys-file [KEYS_FILE] --model <modelId>` (adding a minimal test entry in `[SKILL_FOLDER]\test-call-llm.py` if absent) (skip the call and keep `"status": "untested"` when the provider key is missing from `[KEYS_FILE]`: `DEEPSEEK_API_KEY`, `MOONSHOT_API_KEY`; report these models as API untested) and apply Gate 8 status updates in `[SKILL_FOLDER]\model-registry.json` (`200 OK` -> `"status": "available", "enabled": true`; `401/403` -> `"status": "no_access", "enabled": false`; `429 Insufficient balance` -> `"status": "no_access"` on paid models, keep free models `"available"`; `400` -> adjust supported `effort` list in `model_id_startswith[]`)
2. Execute Phase 9.4 per `[MDLRGUP-MDLINVNTRY-SP01]` FR-01, FR-07, FR-08 (skip the first two sub-steps when `[CAPABILITY_SCHEME] = NONE`):
   - Run `[VENV_PYTHON] "[SESSION_FOLDER]\layer-generation-ladder.py" --registry-file "[SKILL_FOLDER]\model-registry.json" --match-file "[RUN_FOLDER]\[DATE]_Epoch-ECI-Match.json" --log-file "[RUN_FOLDER]\[DATE]_GenerationLadder.log"` (insert-only, never `--bootstrap`): validates every `higher_than` item, builds E1/E2/E3/E5 and manual edges, writes `generation`, `generation_evidence`, and `generation_estimated` for models without `generation` only, reports squeezes (`squeezed by X`) and E1-E3 contradictions, and aborts without writing on a cycle or a rejected item
   - Review the log: a **rejected** `higher_than` item → fix the missing field from `[DATE]_Generation-Edges.json` and re-run; a **cycle** (run aborted) or a **CONTRADICTION** line (direct conflict; the script keeps the higher-precedence edge E4 > E1 > E3 and drops the other) → EC-8: re-check `uc_class` of both models on the vendor page; wrong class → fix and re-run; right class → record in `[DATE]_RunReport.md` Pending resolution (never change `uc_class` to silence a contradiction); a **squeeze** → EC-7: record `squeezed by X` in Pending resolution, no action in this run
   - Items and scope guard: for every model whose `observed.sequences >= 3`, set `items` to `observed.items` (largest fully completed `items_planned`; lower it when a skip observation says so); set `scope_guard: "strict"` only with a FAILS or ledger reference recorded in `[DATE]_RunReport.md`; never change `generation`
   - Run `[VENV_PYTHON] "[SESSION_FOLDER]\format-model-registry.py" --registry-file "[SKILL_FOLDER]\model-registry.json"` after the Phase 8 and Phase 9.4 registry edits (1-line-per-entry layout)
   - Devin-only rungs (only when `[RUN_FOLDER]\[DATE]_Devin-Models-DOM.json` exists): for every Devin table model without a registry match and without a row in `[INVENTORY_FILE]` Section 3.2, set its rung once from a vendor statement (EC-6) and append `{model, generation, release_date (optional: `YYYY-MM-DD` or `YYYY-MM` from the same vendor announcement; key absent when no page prints a date, shown as `-`), efforts (codes the page prose names but the table lacks, optional), evidence, source, accessed, statement}` to `devin_only[]` in `[RUN_FOLDER]\[DATE]_Generation-Edges.json`; without a statement write `generation` 1 with `evidence` `unplaced`; create the file when it is absent (`[CAPABILITY_SCHEME] = NONE`); every Section 3.2 rung is shown as `G[nn]*`; never change a recorded rung
   - Run `[VENV_PYTHON] "[SESSION_FOLDER]\update-model-inventory.py" --skill-folder "[SKILL_FOLDER]" --inventory-file "[INVENTORY_FILE]" --today "[DATE]" --devin-dom-file "[RUN_FOLDER]\[DATE]_Devin-Models-DOM.json" --generation-edges-file "[RUN_FOLDER]\[DATE]_Generation-Edges.json"` (omit both Devin arguments when no Devin DOM file exists: Section 3.2 then stays unchanged) to regenerate `[INVENTORY_FILE]`: `Top rung: G[nn] ([DATE])` header; Section 3.1 columns `Model | Generation | ECI Score | Items | Context | Efforts | In USD | Cache USD | Out USD | Value | Released | Notes` (`Released` = registry `release_date` as stored, `YYYY-MM-DD` or `YYYY-MM`, DD-24; `Value` per the Field semantics, DD-20; `G[nn]*` for estimated rungs, `ECI Score` = registry `eci_score` with 1 decimal or `-`, `[n]m` for measured Items); Notes from `generation_evidence`, `UC-n`, Epoch score with interval or `no Epoch score`, status, `scope guard strict`, `CSV rows`, adaptive-thinking Medium warning, `squeezed by X`, `unplaced`; Section 3.1 and 3.2 sorted by 1) Generation descending, 2) Model ascending; Section 3.2 "Devin Model Deviations" (columns `Model | Generation | Items | Efforts | In USD | Cache USD | Out USD | Released | Notes`; `Released` = registry `release_date` of the matched model or `devin_only[].release_date`, else `-`) holds only Devin models without a registry match or with a different In, Cache read, or Out price (DD-22), list price after promotions, promotion and end date in Notes; rows that left the Devin page are removed and listed in the RunReport; announced future price changes go to the RunReport Pending resolution
3. Run Gate 9.4 via `& "[SESSION_FOLDER]\verify-and-distribute-registry.ps1" -Mode Gate94 -RunFolder "[RUN_FOLDER]" -Date "[DATE]" -SkillFolder "[SKILL_FOLDER]" -InventoryFile "[INVENTORY_FILE]"` (FR-10: every non-retired text model has `generation`; no `generation` differs from the committed registry at git `HEAD` except `generation_estimated: true` → measured; every `higher_than` item has `model`, `kind`, `source`, `accessed`, `statement`; inventory sorted Generation desc, Model asc; `Top rung` equals the maximum `generation`; source versions/dates and `ECI Score` / `In USD` / `Cache USD` / `Out USD` columns consistent with `[SKILL_FOLDER]` JSONs; `Value` cells equal the recomputation from the registry prices; `Released` cells equal the registry `release_date`; every Section 3.2 row has no Section 3.1 match or a different price)
4. Execute Phase 10 and write the complete run report (1. Added models, 2. Price changes, 3. Unchanged count, 4. Registry additions and corrected sourced values (`context_window`, prices, other fields that differed from the vendor page), 5. Prefix gaps, 6. Parameter mapping, 7. Test results, 8. Long context, 9. Pending resolution (squeezes, contradictions, ties from silent sources), 10. Sources archived in `[RUN_FOLDER]`, 11. `MODEL_INVENTORY.md` changes (Value and Released columns, month-only dates refined to a day or corrected, Section 3.2 rows added, removed, repriced; announced future Devin price changes), 12. Generation ladder: inserted rungs with evidence, `higher_than` items added, E6 estimates, `items` / `scope_guard` changes, Top rung before and after) to `[RUN_FOLDER]\[DATE]_RunReport.md`

Constraints:
- All file operations MUST stay within `[RUN_FOLDER]`, `[SKILL_FOLDER]\model-registry.json`, `[SKILL_FOLDER]\test-call-llm.py`, and `[INVENTORY_FILE]`
- Do ONLY the numbered items above. Report any item you could not complete as NOT DONE
- `generation` is written by `layer-generation-ladder.py` only; never edit `generation`, `generation_evidence`, or `generation_estimated` by hand, never run `--bootstrap`, never edit `[INVENTORY_FILE]` by hand (MDLRGUP-MDLINVNTRY-IG-01, IG-02, IG-04)
- Do NOT execute Phase 9.1-9.3 distribution in this prompt (distribution is isolated in Prompt 8)
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state: layering is insert-only and idempotent for models that already have `generation`; `MODEL_INVENTORY.md` regeneration and `[DATE]_RunReport.md` are idempotent
- Hang safety: no command may wait for stdin, a pager, or an unbounded child. Banned: see `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Robustness.md`. 120s per-model API test cap, 60s layering cap. On timeout: retry once, then record in `[RUN_FOLDER]\[DATE]_RunReport.md` and `[SESSION_FOLDER]\PROBLEMS.md`, continue

Findings card: Load and update `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Findings.md`. Append one Partition Observations line and record any API test failures (e.g., rejected effort values), squeezes, and contradictions.

Verify: Gate 8 and Gate 9.4 pass; `[RUN_FOLDER]\[DATE]_GenerationLadder.log` ends with `OK:` (0 cycles, 0 rejected); `[INVENTORY_FILE]` `Top rung` equals the maximum `generation` in the registry; every `Value` cell in Section 3.1 is a star score or `-`; every `Released` cell in Section 3.1 is `YYYY-MM-DD` or `YYYY-MM` (Section 3.2 Devin-only rows may show `-`); every Section 3.2 row (when a Devin DOM file exists) has no Section 3.1 match or a different price; `[RUN_FOLDER]\[DATE]_RunReport.md` exists with all 12 Phase 10 report sections.

**STOP.** Report: items DONE / NOT DONE, Phase 8 test pass/fail summary, inserted rungs (model, `G[nn]`, evidence), squeezes and contradictions, Gate 9.4 status, and path to `[RUN_FOLDER]\[DATE]_RunReport.md`.
```

---

## Prompt 8 - Phase 9 Distribution and Gate 9 Sync Check

<!-- Expected state: Phase 8 tests, Phase 9.4 layering and MODEL_INVENTORY.md update, and Phase 10 report are complete; distributes updated files to `.devin` and the Lana-V1 runtime config, then verifies Gate 9. -->

```
01-MdlInv-[RUN_MODE] [ 08 / 09 ] - Phase 9 Distribute canonical JSONs and MODEL_INVENTORY.md and verify Gate 9

Session: `[SESSION_FOLDER]`
Working folder: `[RUN_FOLDER]`

Read `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Robustness.md` and `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Findings.md`. Treat earlier conversation as compacted. Step Phase 9.
Planning document: `_PROMPTS_ModelInventoryUpdate_TEMPLATE.md`, Prompt 8 (Phase 9.1-9.3 and Gate 9).

Distribute the updated canonical JSON files (`model-pricing.json`, `model-registry.json`, `model-parameter-mapping.json`) and `[INVENTORY_FILE]` from `[PROMPTSYSTEM_FOLDER]` to all authorized distribution targets and verify file-hash identity via Gate 9.

1. Execute Phases 9.1 (`[AGENT_FOLDER]\skills\llm-tools\`: 3 JSONs, `test-call-llm.py`, `MODEL_INVENTORY.md`), 9.3 (3 JSONs to `e:\Dev\Lana-V1\.agent-data\config`; Phase 9.2 dependent-skill replicas no longer exist since the 2026-10-29 `llm-tools` merge), and Gate 9 via `& "[SESSION_FOLDER]\verify-and-distribute-registry.ps1" -Mode Distribute -RunFolder "[RUN_FOLDER]" -Date "[DATE]" -SkillFolder "[SKILL_FOLDER]" -InventoryFile "[INVENTORY_FILE]" -AgentFolder "[AGENT_FOLDER]" -PromptSystemFolder "[PROMPTSYSTEM_FOLDER]" -IncludeExternal`
2. Append the Phase 9 distribution and Gate 9 sync verification result (targets synced, SHA-256 match count) to `[RUN_FOLDER]\[DATE]_RunReport.md`

Constraints:
- All file operations MUST stay within `[RUN_FOLDER]`, `[AGENT_FOLDER]\skills\llm-tools\`, and `e:\Dev\Lana-V1\.agent-data\config` (3 model JSONs only; never touch other files there, e.g. `agent-config.json`, `.api-keys.txt`)
- External distribution to `e:\Dev\Lana-V1\.agent-data\config` is pre-authorized by the user (DD-14, 2026-11-02); do not ask
- Distribution requires Gate 9.4 passed in Prompt 7; if `[RUN_FOLDER]\[DATE]_GenerationLadder.log` does not end with `OK:`, stop and report
- Do ONLY the numbered items above. Report any item you could not complete as NOT DONE
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state: `Copy-Item -Force` and hash verification are idempotent
- Hang safety: no command may wait for stdin, a pager, or an unbounded child. Banned: see `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Robustness.md`. 60s per-command cap. On cap: kill, record in `[SESSION_FOLDER]\PROBLEMS.md`, continue

Findings card: Load and update `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Findings.md`. Append one Partition Observations line.

Verify: Gate 9 passes with zero SHA-256 hash mismatches across all synced targets; `[AGENT_FOLDER]\skills\llm-tools\MODEL_INVENTORY.md` hash matches `[INVENTORY_FILE]`.

**STOP.** Report: items DONE / NOT DONE, targets synced (with SHA-256 match count), and Gate 9 status.
```

---

## Prompt 9 - Final Verification Checkpoint

<!-- Expected state: All update, test, layering, inventory regeneration, and distribution steps are complete; runs the verification checkpoint across all run deliverables, commits the registry, and updates session tracking. -->

```
01-MdlInv-[RUN_MODE] [ 09 / 09 ] - Final Checkpoint Verify all gates, deliverables, and session tracking

Session: `[SESSION_FOLDER]`
Working folder: `[RUN_FOLDER]`

Read `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Robustness.md`, `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Findings.md`, and `[RUN_FOLDER]\[DATE]_RunReport.md`. Treat earlier conversation as compacted. Step Final Checkpoint.
Planning document: `_PROMPTS_ModelInventoryUpdate_TEMPLATE.md`, Prompt 9 Final Checkpoint.

Verify all outputs of the `[DATE]` `[RUN_MODE]` model inventory update run against Gates 1-9.4 and the generation ladder invariants, fix any gaps inline within 2 cycles, commit the run, and record the completed run in `[SESSION_FOLDER]\NOTES.md`.

/verify

1. Run `& "[SESSION_FOLDER]\verify-and-distribute-registry.ps1" -Mode VerifyAll -RunFolder "[RUN_FOLDER]" -Date "[DATE]" -SkillFolder "[SKILL_FOLDER]" -InventoryFile "[INVENTORY_FILE]" -AgentFolder "[AGENT_FOLDER]" -PromptSystemFolder "[PROMPTSYSTEM_FOLDER]" -RunMode "[RUN_MODE]" -IncludeExternal` to verify Gates 2 (skipped for `NEWMODEL`), 5, 5.2, 5.3, 5.4, 6, 7, 9 (incl. Lana-V1 config), and 9.4, `[DATE]_RunReport.md`, and zero leftover `.tmp_*` scripts in `[RUN_FOLDER]\_agentwork\`
2. Independent spot check (trust no earlier prompt): pick 3 registry models per target provider that were NOT in `contextChecks`, re-read their vendor model pages with Playwright, and compare `context_window`, `max_output`, and input/output prices against `[SKILL_FOLDER]\model-registry.json` and `model-pricing.json`; any difference is corrected, added to `contextChecks`, and counted in the report as a systematic defect (then widen the sample to every model of that provider)
3. Check that `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Findings.md` `## Unresolved` is empty (or copied to `[SESSION_FOLDER]\PROBLEMS.md`) and that every Pending resolution item of `[DATE]_RunReport.md` Section 9 (squeezes, contradictions, silent-source ties) has a `[SESSION_FOLDER]\PROBLEMS.md` entry
4. Fix any verification gaps inline (max 2 gate cycles; on second failure record in `[SESSION_FOLDER]\PROBLEMS.md` and stop); commit `[SKILL_FOLDER]`, `[AGENT_FOLDER]\skills\llm-tools\`, and `[RUN_FOLDER]` with message `chore(llm-tools): model inventory [RUN_MODE] run [DATE]` (the next run's Gate 9.4 compares `generation` against this commit); in repo `e:\Dev\Lana-V1` commit only `.agent-data/config/model-pricing.json`, `.agent-data/config/model-registry.json`, `.agent-data/config/model-parameter-mapping.json` with message `chore(config): model registry update [DATE]` (skip when unchanged); update `[SESSION_FOLDER]\NOTES.md` with a 1-line entry recording `[DATE] [RUN_MODE]` completion, `Top rung`, and `[RUN_FOLDER]` path

Constraints:
- All file operations MUST stay within `[RUN_FOLDER]`, `[SESSION_FOLDER]\NOTES.md`, `[SESSION_FOLDER]\PROBLEMS.md`, `[SKILL_FOLDER]`, `[INVENTORY_FILE]`, `[AGENT_FOLDER]\skills\`, and the 3 model JSONs in `e:\Dev\Lana-V1\.agent-data\config`
- Do ONLY the numbered items above. Report any item you could not complete as NOT DONE
- In `e:\Dev\Lana-V1`, stage only the 3 model JSONs by explicit path; never `git add -A` or commit other changes in that repo
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state: verification and `NOTES.md` status update are idempotent; the commit is skipped when the working tree is clean
- Hang safety: see `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Robustness.md`

Findings card: Load and update `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Findings.md`. Append final Partition Observations line.

Verify: Gates 5, 5.2, 5.3, 5.4, 6, 7, 9, and 9.4 pass; the spot check found zero differences (or every difference is corrected and reported); zero `.tmp_*` files remain in `[RUN_FOLDER]\_agentwork\`; `git status --porcelain -- "[SKILL_FOLDER]"` is empty; `[SESSION_FOLDER]\NOTES.md` lists the `[DATE] [RUN_MODE]` run.

**STOP.** Report: verify findings fixed / open, commit hash, total net time across the run from `__CARD_MDLRGUP-Findings.md`, final run status, and a clickable summary artifact list with separate headings for each output group formatted as: heading, summary of what was done and what the files contain, and bulleted clickable file paths with file purpose/content (`- `relative/path/to/file` - <description>`). Do not wrap the list in code fences, and never use file:/// links or raw HTML.
```

<!-- EXAMPLE: Reference only. Do not copy into new documents. Shows a completed NEWMODEL run instance (Prompt 1 resolved and the Prompt 5 STOP report; Prompts 3 (no part B provider) and 4 (screenshots) omitted because [INCLUDE_SCREENSHOTS] = NO, renumbered to [ 01 / 07 ] - [ 07 / 07 ]). Model IDs and statements are illustrative.

## Example (NEWMODEL Run Instance - Prompt 1 Resolved, Prompt 5 Report)

`````markdown
---
intended_model: claude-opus-5
context_window_size: 1000k
effort: high
prompt_system: IPPS
---

<!-- Model: claude-opus-5 (effort: high, context: 1000k). Load grouping (PRMT-SC-07): 10 phases of the model inventory update pipeline partitioned into 07 prompts (<= 7 items, <= 4 modified files, <= 1 heavy workflow per prompt) so Playwright DOM scraping, Epoch matching and vendor edge research, JSON updates, generation layering, API testing, and distribution stay within single-turn budgets. -->

## Prompt 1 - Bootstrap: Detect Context, Create Run Folder, and Generate Instance

<!-- Detects NEWMODEL and 2026-12-01, creates _2026-12-01_NEWMODEL and _agentwork cards, and instantiates _PROMPTS_01-MdlInv-NEWMODEL.md. -->

```
01-MdlInv-NEWMODEL [ 01 / 07 ] - P3-Bootstrap Detect run parameters, initialize run folder, and generate prompts instance

Session: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate`
Working folder: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate`

Read `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\NOTES.md`, `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_PROMPTS_ModelInventoryUpdate_TEMPLATE.md` (Placeholders, Run modes, Run folder structure, Generation ladder invariants), and `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agentwork\__CARD_MDLINVNTRY-Robustness.md`. Treat earlier conversation as compacted. Step P3-Bootstrap.
Planning document: `_PROMPTS_ModelInventoryUpdate_TEMPLATE.md`, Prompt 1 Bootstrap.

Initialize a datestamped model inventory update run folder and instantiate a ready-to-run prompts file from `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_PROMPTS_ModelInventoryUpdate_TEMPLATE.md`.

1. Detect workspace and run parameters:
   - Resolve `e:\dev\IPPS`, active `e:\dev\IPPS\PromptSystemV4.5`, `e:\dev\IPPS\.devin`, `e:\dev\IPPS\PromptSystemV4.5\skills\llm-tools`, `e:\dev\IPPS\PromptSystemV4.5\skills\llm-tools\MODEL_INVENTORY.md`, and `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_INFO_HOW_TO_ORGANIZE_LLMS_BY_CAPABILITY.md`
   - Set `2026-12-01` from request metadata, `NEWMODEL`, `Anthropic`, `claude-opus-5-6, claude-sonnet-5-6`, `NO` (`INCLUDE_SCREENSHOTS`), `LADDER` (`CAPABILITY_SCHEME` from `NOTES.md` Key Decisions `DD-10`), and `06` (`TOTAL_PROMPTS` in generated instance after excluding Bootstrap and Prompts 3 and 4)
   - Verify `git status --porcelain -- "e:\dev\IPPS\PromptSystemV4.5\skills\llm-tools\model-registry.json"` is empty
2. Create the isolated run folder `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-12-01_NEWMODEL` and `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-12-01_NEWMODEL\_agentwork\`
3. Copy `__CARD_MDLINVNTRY-Robustness.md` to `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-12-01_NEWMODEL\_agentwork\__CARD_MDLRGUP-Robustness.md` and initialize `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-12-01_NEWMODEL\_agentwork\__CARD_MDLRGUP-Findings.md` with `# Findings Card: MDLRGUP (2026-12-01 NEWMODEL)`, `## Partition Observations`, `## Unresolved`, and `## Resolved`
4. Generate `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-12-01_NEWMODEL\_agentwork\_PROMPTS_01-MdlInv-NEWMODEL.md` from `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_PROMPTS_ModelInventoryUpdate_TEMPLATE.md`:
   - Exclude Prompt 1 (already executed in this turn)
   - Remove Prompt 3 (no Z.AI, xAI, DeepSeek, or Moonshot target) and Prompt 4 (`INCLUDE_SCREENSHOTS = NO`), keeping Prompts 2, 5, 6, 7, 8, 9 as `[ 01 / 06 ]` to `[ 06 / 06 ]`
   - Replace all placeholders with resolved values and strip template-instruction XML comments

/write-prompts

Constraints:
- All file operations MUST stay within `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate`
- Do ONLY the numbered items above. Report any item you could not complete as NOT DONE
- Do NOT execute Phase 2 DOM extraction or modify any JSON file in `e:\dev\IPPS\PromptSystemV4.5\skills\llm-tools` during Bootstrap
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state: if `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-12-01_NEWMODEL` already exists, reuse it and overwrite only `_PROMPTS_01-MdlInv-NEWMODEL.md`
- Hang safety: no command may wait for stdin, a pager, or an unbounded child. Banned: see `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agentwork\__CARD_MDLINVNTRY-Robustness.md`. 120s per-command cap. On cap: kill, record in `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\PROBLEMS.md`, continue

Findings card: Load and update `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-12-01_NEWMODEL\_agentwork\__CARD_MDLRGUP-Findings.md`. Append one Partition Observations line for Bootstrap.

Verify: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-12-01_NEWMODEL` exists; `__CARD_MDLRGUP-Findings.md` and `__CARD_MDLRGUP-Robustness.md` exist in `_agentwork\`; `_PROMPTS_01-MdlInv-NEWMODEL.md` exists with zero unresolved placeholders; `model-registry.json` has no uncommitted changes.

**STOP.** Report: resolved placeholders (`2026-12-01`, `NEWMODEL`, `Anthropic`, `NO`, `LADDER`, `06`), run folder path, generated prompts file path, and total prompts (`06`). Do NOT execute Prompt 2.
```

Prompt 5 STOP report (illustrative):

```
DONE 1-4. Matched 93 / 96 registry models; unmatched: claude-opus-5-6, claude-sonnet-5-6, grok-build-0.1 (no Epoch row).
New models: claude-opus-5-6 (release_date 2026-11-20, UC-2 Flagship, $4 / $20), claude-sonnet-5-6 (2026-11-20, UC-3 Balanced, $1.50 / $7.50).
higher_than candidates: none (EC-1: Anthropic model overview "Choosing a model" names Opus 5.6 as the default start and Fable 5.1 for demanding reasoning - escalation statement already recorded for Fable 5.1 > Opus 5.5; no statement ranks Opus 5.6 against Fable 5.1 -> tie).
Ties: claude-opus-5-6 ~ claude-fable-5-1 (source https://platform.claude.com/docs/en/models/overview, accessed 2026-12-01, reason: parity statement only).
E6 estimates: none. EC-9 corrections: none.
Expected Prompt 7 result: claude-opus-5-6 G11 or G12 by E2 >= claude-opus-5-5 and E1 > claude-sonnet-5-6; claude-sonnet-5-6 by E2 >= claude-sonnet-5-5.
```
`````
-->
