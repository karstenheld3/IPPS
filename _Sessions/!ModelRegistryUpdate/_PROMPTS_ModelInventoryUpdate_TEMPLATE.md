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
Specification: [SESSION_FOLDER]\T02_MDLINVNTRY_ReliableModelInventory_2026-10-28\_SPEC_MDLRGUP-MDLINVNTRY-01_DepthLadder.md [MDLRGUP-MDLINVNTRY-SP01]; design in [SESSION_FOLDER]\_INFO_HOW_TO_ORGANIZE_LLMS_BY_CAPABILITY.md [LLMCAPCLS-IN01]
Previous version: _PROMPTS_ModelInventoryUpdate_TEMPLATE_v0.md (year-letter labels, ECI bands, WF; superseded 2026-11-02; removed by /cleanup 2026-11-02, retrievable from git history)

Purpose: Self-contained recurring pipeline to refresh model-registry.json, model-pricing.json, model-parameter-mapping.json, and MODEL_INVENTORY.md from authoritative provider DOM tables, Epoch ECI scores with confidence intervals, vendor capability statements (depth ladder edges), and the observation ledger (Items).
Replaces the former root-level update-model-registry.md workflow and isolates all run artifacts inside a datestamped run folder.

Run modes ([RUN_MODE]):
- FULL: Complete refresh across all providers in [TARGET_PROVIDERS] — DOM extraction (Prompt 2), full-page screenshot archive and markdown transcription (Prompt 3), capability evidence: Epoch ECI intervals, new-model metadata, depth edge research (Prompt 4), canonical JSON updates with Gates 5-7 (Prompt 5), live API tests + depth layering + MODEL_INVENTORY.md regeneration + Phase 10 report (Prompt 6), distribution incl. external Lana-V1 config (Prompt 7), and Final Checkpoint (Prompt 8).
- PRICES: Fast price and model metadata refresh — executes Prompts 2, 4 (if capability scheme active), 5, 6, 7, 8. Excludes Prompt 3 (screenshots and image transcription).
- NEWMODEL: Targeted onboarding for newly released model(s) specified in [TARGET_MODELS] — executes Prompts 2 (affected providers only), 4, 5, 6, 7, 8. Excludes Prompt 3 unless [INCLUDE_SCREENSHOTS] = YES.

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
- [RUN_FOLDER]\[DATE]_eci-leaderboard.csv, [DATE]_Epoch-ECI-Match.json - Epoch ECI CSV and per-model score + 95% interval match (when [CAPABILITY_SCHEME] = LADDER)
- [RUN_FOLDER]\[DATE]_Depth-Edges.json - New-model metadata (release_date, uc_class) and edge-case outcomes (deeper_than candidates, tie lines, E6 notes) from vendor pages (when [CAPABILITY_SCHEME] = LADDER)
- [RUN_FOLDER]\[DATE]_DepthLadder.log - layer-depth-ladder.py output: inserted rungs, squeezes, rejected edges, contradictions (when [CAPABILITY_SCHEME] = LADDER)
- [RUN_FOLDER]\[DATE]_ChangeSet.json - Phase 5.0 change set (new registry IDs, new and changed pricing IDs)
- [RUN_FOLDER]\[DATE]_screenshots\ and [RUN_FOLDER]\[DATE]_*.md - Screenshot archive and stitched transcriptions (when [INCLUDE_SCREENSHOTS] = YES)
- [RUN_FOLDER]\[DATE]_RunReport.md - Phase 10 summary report
- Reusable session scripts in [SESSION_FOLDER]:
  - [SESSION_FOLDER]\match-epoch-eci.py - Downloads the Epoch ECI CSV and matches every registry model to its score and 95% interval (eci_score, eci_ci_low, eci_ci_high); lists unmatched registry models and DOM models absent from the registry (Prompt 4)
  - [SESSION_FOLDER]\layer-depth-ladder.py - Insert-only depth layering per [MDLRGUP-MDLINVNTRY-SP01] FR-01/FR-02: builds E1/E2/E3/E5 edges plus deeper_than manual edges, validates manual edges (source, accessed, statement), writes depth, depth_evidence, depth_estimated for models without depth, reports squeezes and contradictions, aborts on a cycle. `--bootstrap` was a one-time migration to registry 1.12.0 and is never used in a run (Prompt 6)
  - [SESSION_FOLDER]\test-layer-depth-ladder.py - Regression test for layer-depth-ladder.py (NFR-01 bootstrap reproduction of the 2026-10-28 snapshot, insert-only, squeeze, rejected edge, cycle); run after any change to the layering script
  - [SESSION_FOLDER]\update-model-inventory.py - Regenerates [INVENTORY_FILE] Section 3.1 (every text model not `retired`) from the registries and recomputes Items and prices of the hand-maintained Section 3.2 rows: columns Model | Depth | Items | Context | Efforts | In USD | Cache USD | Out USD | Devin cost | Notes, `Top rung` header line, sorted by 1) Depth descending, 2) Model ascending; Notes text beyond derived values comes from the registry `inventory_note` field (Prompt 6)
  - [SESSION_FOLDER]\verify-and-distribute-registry.ps1 - Executes deterministic verification Gates 1, 2, 5, 6, 7, 9, 9.4, VerifyAll and Phase 9 distribution (Prompts 2, 5, 6, 7, 8). Gate 9.4 compares `depth` against the committed registry (git HEAD): the registry must be committed before each run
  - [SESSION_FOLDER]\format-model-registry.py - Re-serializes model-registry.json to the canonical 1-line-per-entry layout after any scripted write; `--check` verifies layout without writing (Prompts 5, 6). Never write model-registry.json with json.dump(indent=N) or ConvertTo-Json
- Legacy [SESSION_FOLDER]\model-sources\ is read-only historical archive; never write new files into model-sources\.

Placeholder registry:
- [MODEL] - Intended execution model ID from MODEL_INVENTORY.md (e.g., glm-5.2, claude-opus-5)
- [CONTEXT_WINDOW_SIZE] - Model context window size in k (e.g., 200k, 1000k)
- [EFFORT] - Reasoning/thinking effort level (low | medium | high | xhigh | max)
- [WORKSPACE_FOLDER] - Workspace root path (e.g., e:\dev\IPPS)
- [PROMPTSYSTEM_FOLDER] - Canonical PromptSystem folder path in workspace (e.g., e:\dev\IPPS\PromptSystemV4.5)
- [AGENT_FOLDER] - Active agent folder path in workspace (e.g., e:\dev\IPPS\.devin)
- [SKILL_FOLDER] - Canonical llm-tools skill folder holding the model JSONs ([PROMPTSYSTEM_FOLDER]\skills\llm-tools)
- [INVENTORY_FILE] - Canonical MODEL_INVENTORY.md file path ([PROMPTSYSTEM_FOLDER]\skills\llm-tools\MODEL_INVENTORY.md)
- [DESIGN_INFO] - Depth ladder design document ([SESSION_FOLDER]\_INFO_HOW_TO_ORGANIZE_LLMS_BY_CAPABILITY.md); Section 2.2 evidence kinds, Section 2.6 edge cases EC-1 to EC-9
- [SESSION_FOLDER] - Permanent session folder ([WORKSPACE_FOLDER]\_Sessions\!ModelRegistryUpdate)
- [RUN_FOLDER] - Datestamped run folder ([SESSION_FOLDER]\_[DATE]_[RUN_MODE])
- [RUN_MODE] - Execution scope mode (FULL | PRICES | NEWMODEL)
- [DATE] - Run date in YYYY-MM-DD format (e.g., 2026-10-28)
- [TARGET_PROVIDERS] - Providers in scope for this run (e.g., Anthropic, OpenAI, Google, Z.AI, xAI)
- [TARGET_MODELS] - Target model IDs for NEWMODEL mode, or ALL for FULL and PRICES modes
- [INCLUDE_SCREENSHOTS] - Include Prompt 3 screenshot capture and transcription (YES | NO)
- [CAPABILITY_SCHEME] - Capability representation mode (LADDER | NONE); LADDER per DD-10 option 3 and [MDLRGUP-MDLINVNTRY-SP01]
- [TOTAL_PROMPTS] - Total prompt count in the generated instance after excluding Bootstrap and removing conditional prompts (07 for FULL, 06 for PRICES and NEWMODEL)
- [VENV_PYTHON] - Shared Python executable path (e.g., e:\dev\.tools\llm-venv\Scripts\python.exe)
- [KEYS_FILE] - API keys file path (e:\dev\.tools\.api-keys.txt)
- [TRANSCRIPTION_SCRIPT] - Image-to-markdown transcription script ([AGENT_FOLDER]\skills\llm-tools\transcription\transcribe-image-to-markdown.py)

Load-based partition table (PRMT-SC-07 assessment for [MODEL] at [EFFORT] effort, [CONTEXT_WINDOW_SIZE] context):
- Prompt 1 (Bootstrap, ~15k tokens, 4 items): Detect [RUN_MODE], [DATE], [PROMPTSYSTEM_FOLDER], create [RUN_FOLDER] and _agentwork cards, generate instance _PROMPTS_01-MdlInv-[RUN_MODE].md via /write-prompts.
- Prompt 2 (Phases 1 + 2 DOM Extraction, ~45k tokens, 7 items): Pre-flight Gate 1 + Playwright DOM extraction across [TARGET_PROVIDERS] (Anthropic A1-A4, OpenAI O1-O3, Google Gemini G1-G3, Z.AI Z1-Z3, xAI X1-X3) + Gate 2 check.
- Prompt 3 (Phases 3 + 4 Screenshots & Transcription, ~40k tokens, 4 items, Conditional on [INCLUDE_SCREENSHOTS] = YES): Full-page scroll capture, copy to [RUN_FOLDER]\[DATE]_screenshots\, run transcribe-image-to-markdown.py, stitch markdowns, verify Gates 3-4.
- Prompt 4 (Capability Evidence, ~35k tokens, 4 items, Conditional on [CAPABILITY_SCHEME] = LADDER): Download Epoch ECI CSV and match scores + intervals ([DATE]_Epoch-ECI-Match.json); read vendor model pages for new models (release_date, uc_class); resolve edge cases EC-1 to EC-9 into [DATE]_Depth-Edges.json.
- Prompt 5 (Phases 5 + 6 + 7 Canonical JSON Updates, ~35k tokens, 5 items): Derive change set (Phase 5.0), update model-registry.json including eci_score, eci_ci, uc_class, release_date, deeper_than (Phase 5 + Gate 5), update model-pricing.json (Phase 6 + Gate 6), verify model-parameter-mapping.json (Phase 7 + Gate 7).
- Prompt 6 (Phase 8 + Phase 9.4 + Phase 10, ~30k tokens, 4 items): Run test-call-llm.py for new enabled models (Phase 8 + Gate 8), run layer-depth-ladder.py insert-only, copy items / scope_guard from observed, regenerate [INVENTORY_FILE] (Phase 9.4 + Gate 9.4), write [RUN_FOLDER]\[DATE]_RunReport.md (Phase 10).
- Prompt 7 (Phase 9 Distribution, ~15k tokens, 2 items): Copy canonical JSONs and [INVENTORY_FILE] to [AGENT_FOLDER]\skills\llm-tools\ (9.1), copy JSONs to external target `e:\Dev\Lana-V1\.agent-data\config` (9.3, always; user decision DD-14 2026-11-02: the entire update chain runs inside the prompts file), run Gate 9 hash check.
- Prompt 8 (Final Checkpoint, ~20k tokens, 3 items): Run /verify across updated JSONs, [INVENTORY_FILE], and [DATE]_RunReport.md; fix any gaps inline (max 2 cycles); update session NOTES.md.

Conditional prompts:
- Prompt 3 (Phases 3-4 Screenshots and Transcription) - remove when [INCLUDE_SCREENSHOTS] = NO (default for PRICES and NEWMODEL).
- Prompt 4 (Capability Evidence) - remove when [CAPABILITY_SCHEME] = NONE. With NONE, Prompt 5 writes no capability fields and Prompt 6 skips the layering; existing depth values stay untouched.
- After removing any conditional prompt, renumber remaining prompts sequentially in the generated instance file and update [TOTAL_PROMPTS] in every Prompt Marker (e.g., excluding Bootstrap and removing Prompt 3 yields [ 01 / 06 ] through [ 06 / 06 ]).

CRITICAL - Manual execution only:
- Prompts are designed for manual copy-paste, one prompt per turn, with user review at each gate.
- Agent must NEVER self-execute multiple prompts in a single response (PRMT-EX-01, PRMT-EX-02).
- The **STOP.** marker at the end of every prompt is a hard execution boundary.

Depth ladder invariants (every prompt that touches model-registry.json):
- A `depth` value is written once by layer-depth-ladder.py and never edited by hand or by any other step; the only permitted change is `depth_estimated: true` -> measured (MDLRGUP-MDLINVNTRY-IG-01, IG-02).
- A `deeper_than` entry needs `model`, `kind` (E1 | E4), `source` (URL or file), `accessed` (YYYY-MM-DD), `statement` (quote). Without all five the layering script and Gate 9.4 reject it (IG-03).
- Silence from the named source is a tie, never a judgment edge (MDLRGUP-MDLINVNTRY-DD-04). Record the tie with the source that was read.
- Vendor pages are read with Playwright; Epoch ECI is the only benchmark source. Never use Artificial Analysis, LMArena, gap-to-frontier, aggregators, or model recollection (QS-12).

Context management:
- Target: 200k+ token context models at Depth D6 or higher (e.g., glm-5.2 high, claude-opus-5 high).
- In PRICES or NEWMODEL mode (Prompts 2, 4, 5, 6, 7, 8), total token consumption is ~155k and fits in a single session.
- In FULL mode (including Prompt 3 screenshot batches), start a fresh session before Prompt 5 if context exceeds 120k tokens; all Phase 2-4 outputs are persisted on disk in [RUN_FOLDER].
- Later prompts must NOT re-read large files already in conversation history from earlier turns in the same session.
- Playwright MCP calls may hang; enforce a 60s timeout per page and use an isolated browser.newContext() if the default tab has concurrent navigation.

Remove template-instruction XML comments (this block, Conditional comments, and the EXAMPLE block at the end) when instantiating _PROMPTS_01-MdlInv-[RUN_MODE].md; keep the opening load-grouping comment and the 1-sentence commentary comment under each ## Prompt N heading (PRMT-FT-04, PRMT-SC-05, PRMT-SC-07).
-->

<!-- Model: [MODEL] (effort: [EFFORT], context: [CONTEXT_WINDOW_SIZE]). Load grouping (PRMT-SC-07): 10 phases of the model inventory update pipeline partitioned into [TOTAL_PROMPTS] prompts (<= 7 items, <= 4 modified files, <= 1 heavy workflow per prompt) so Playwright DOM scraping, screenshot transcription, Epoch matching and vendor edge research, JSON updates, depth layering, API testing, and distribution stay within single-turn budgets. -->

## Prompt 1 - Bootstrap: Detect Context, Create Run Folder, and Generate Instance

<!-- Detects [RUN_MODE] and [DATE], creates [RUN_FOLDER] and _agentwork cards, and instantiates _PROMPTS_01-MdlInv-[RUN_MODE].md. -->

```
01-MdlInv-[RUN_MODE] [ 01 / 08 ] - P3-Bootstrap Detect run parameters, initialize run folder, and generate prompts instance

Session: `[SESSION_FOLDER]`
Working folder: `[SESSION_FOLDER]`

Read `[SESSION_FOLDER]\NOTES.md`, `[SESSION_FOLDER]\_PROMPTS_ModelInventoryUpdate_TEMPLATE.md` (Placeholders, Run modes, Run folder structure, Depth ladder invariants), and `[SESSION_FOLDER]\_agentwork\__CARD_MDLINVNTRY-Robustness.md`. Treat earlier conversation as compacted. Step P3-Bootstrap.
Planning document: `_PROMPTS_ModelInventoryUpdate_TEMPLATE.md`, Prompt 1 Bootstrap.

Initialize a datestamped model inventory update run folder and instantiate a ready-to-run prompts file from `[SESSION_FOLDER]\_PROMPTS_ModelInventoryUpdate_TEMPLATE.md`.

1. Detect workspace and run parameters:
   - Resolve `[WORKSPACE_FOLDER]`, active `[PROMPTSYSTEM_FOLDER]` (e.g., `PromptSystemV4.5`), `[AGENT_FOLDER]` (`.devin`), `[SKILL_FOLDER]`, `[INVENTORY_FILE]`, and `[DESIGN_INFO]`
   - Set `[DATE]` from request metadata (`YYYY-MM-DD`), `[RUN_MODE]` (`FULL` | `PRICES` | `NEWMODEL`, default `PRICES` unless user specified otherwise), `[TARGET_PROVIDERS]` (default `Anthropic, OpenAI, Google, Z.AI, xAI`), `[TARGET_MODELS]` (`ALL` or user-specified model IDs), `[INCLUDE_SCREENSHOTS]` (`YES` if `FULL`, else `NO`), and `[CAPABILITY_SCHEME]` (from `[SESSION_FOLDER]\NOTES.md` Key Decisions `DD-10`, default `LADDER`)
   - Verify `git status --porcelain -- "[SKILL_FOLDER]\model-registry.json"` is empty (Gate 9.4 compares `depth` against the committed registry); if not empty, stop and report: the registry must be committed before the run
2. Create the isolated run folder `[RUN_FOLDER]` (`[SESSION_FOLDER]\_[DATE]_[RUN_MODE]\`) and `[RUN_FOLDER]\_agentwork\`; if `[INCLUDE_SCREENSHOTS] = YES`, also create `[RUN_FOLDER]\[DATE]_screenshots\` subfolders (`Anthropic-Pricing`, `Anthropic-ModelOverview`, `Anthropic-Deprecations`, `OpenAI-Standard`, `OpenAI-Batch`, `OpenAI-Compare`, `Google-Pricing`, `Google-Models`, `ZAI-Pricing`, `ZAI-Models`, `xAI-Pricing`, `xAI-Models`)
3. Copy `__CARD_MDLINVNTRY-Robustness.md` to `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Robustness.md` and initialize `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Findings.md` with `# Findings Card: MDLRGUP ([DATE] [RUN_MODE])`, `## Partition Observations`, `## Unresolved`, and `## Resolved`
4. Generate `[RUN_FOLDER]\_agentwork\_PROMPTS_01-MdlInv-[RUN_MODE].md` from `[SESSION_FOLDER]\_PROMPTS_ModelInventoryUpdate_TEMPLATE.md`:
   - Exclude Prompt 1 (already executed in this turn)
   - Remove conditional prompts that do not apply (`Prompt 3` when `[INCLUDE_SCREENSHOTS] = NO`; `Prompt 4` when `[CAPABILITY_SCHEME] = NONE`)
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

## Prompt 2 - Phase 1 Pre-Flight and Phase 2 DOM Extraction

<!-- Expected state: [RUN_FOLDER] and run cards exist; executes Phase 1 pre-flight and Phase 2 DOM extraction across [TARGET_PROVIDERS] into [RUN_FOLDER]. -->

```
01-MdlInv-[RUN_MODE] [ 02 / 08 ] - Phase 1 + Phase 2 Pre-flight checks and provider DOM extraction

Session: `[SESSION_FOLDER]`
Working folder: `[RUN_FOLDER]`

Read `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Robustness.md`, `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Findings.md`, and `[SESSION_FOLDER]\T02_MDLINVNTRY_ReliableModelInventory_2026-10-28\_INFO_MDLRGUP-MDLINVNTRY-04_SourcesPerField.md` (Sections 1-9 provider extraction rules). Treat earlier conversation as compacted. Step Phase 1 + Phase 2.
Planning document: `_PROMPTS_ModelInventoryUpdate_TEMPLATE.md`, Phase 1 and Phase 2 (Anthropic A1-A4, OpenAI O1-O3, Google G1-G3, Z.AI Z1-Z3, xAI X1-X3).

Execute Phase 1 Pre-Flight Checks and Phase 2 DOM Extraction across `[TARGET_PROVIDERS]` (for `[TARGET_MODELS]`), saving all `*-DOM.json` extracts into `[RUN_FOLDER]`. For every page: navigate, resize to `1920x1080`, dismiss cookie/modal overlays, and expand any `"All models" / "View more" / "Show all" / "Expand"` buttons before extracting `<table>` rows.

1. Execute Phase 1 Pre-Flight Check (Gate 1) via `& "[SESSION_FOLDER]\verify-and-distribute-registry.ps1" -Mode Gate1 -RunFolder "[RUN_FOLDER]" -Date "[DATE]" -SkillFolder "[SKILL_FOLDER]" -InventoryFile "[INVENTORY_FILE]" -AllowSameDateReRun`
2. Extract Anthropic DOM data from canonical URLs (`A1` `https://platform.claude.com/docs/en/about-claude/pricing` columns `Base Input Tokens`, `Cache Hits & Refreshes`, `Output Tokens`; `A2`/`A3` `https://platform.claude.com/docs/en/models/overview` API IDs, context window, max output, thinking support; `A4` `https://platform.claude.com/docs/en/about-claude/model-deprecations` retired/deprecated statuses; fallback to `GET https://api.anthropic.com/v1/models` or `"_note_<alias>": "date suffix pending"` if undated) into `[RUN_FOLDER]\[DATE]_Anthropic-Pricing-DOM.json` and `[RUN_FOLDER]\[DATE]_Anthropic-ModelIDs-DOM.json`
3. Extract OpenAI DOM data from `O1` (`https://developers.openai.com/api/docs/pricing?latest-pricing=standard`, Standard tier tables only — distinguish from Batch tables which are ~50% of Standard; capture both short and long context columns), `O2` (`https://developers.openai.com/api/docs/pricing?latest-pricing=batch`), and `O3` (`https://developers.openai.com/api/docs/models/compare`, using `document.body.innerText` search around `'Window'` / `'max output'` since O3 uses div cards rather than `<table>`) into `[RUN_FOLDER]\[DATE]_OpenAI-Standard-DOM.json`, `[RUN_FOLDER]\[DATE]_OpenAI-Batch-DOM.json`, and `[RUN_FOLDER]\[DATE]_OpenAI-Compare-DOM.json`
4. Extract Google Gemini DOM data per `_INFO_MDLRGUP-MDLINVNTRY-04_SourcesPerField.md` Section 9:
   - `G1` (`https://ai.google.dev/gemini-api/docs/pricing`): iterate per-model `<h2>` headings and extract `sectionTables[0]` (Standard tier, parsing current price before any scheduled date increase and separating `<=200k` vs `>200k` rows) into `[RUN_FOLDER]\[DATE]_Google-Pricing-DOM.json`
   - `G2` (`https://ai.google.dev/gemini-api/docs/models` + per-model `/models/<slug>` subpages for `Token limits[*]`) and `G3` (`https://ai.google.dev/gemini-api/docs/thinking` table of `Levels Supported`) into `[RUN_FOLDER]\[DATE]_Google-Models-DOM.json`
5. Extract Z.AI DOM data from `Z1` (`https://docs.z.ai/guides/overview/pricing`, use first list price only when dual promo prices appear such as `$0.15 $0.075`; store `"Free"` as `0.00`; implicit caching is 50% of input) and `Z2` (`https://docs.z.ai/guides/overview/overview`, text and vision model tables with context window and thinking/reasoning_effort support) into `[RUN_FOLDER]\[DATE]_ZAI-Pricing-DOM.json` and `[RUN_FOLDER]\[DATE]_ZAI-Models-DOM.json`
6. Extract xAI Grok DOM data from `X1` (`https://docs.x.ai/developers/pricing`, table idx 0 text models including short `<200k` and long `>=200k` context tiers), `X2` (`https://docs.x.ai/developers/models`), and `X3` (`https://docs.x.ai/developers/model-capabilities/text/reasoning`) into `[RUN_FOLDER]\[DATE]_xAI-Pricing-DOM.json` and `[RUN_FOLDER]\[DATE]_xAI-Models-DOM.json`
7. Close the Playwright browser (`browser_close`) and run Gate 2 via `& "[SESSION_FOLDER]\verify-and-distribute-registry.ps1" -Mode Gate2 -RunFolder "[RUN_FOLDER]" -Date "[DATE]" -SkillFolder "[SKILL_FOLDER]" -InventoryFile "[INVENTORY_FILE]"`

Constraints:
- All file writes MUST stay within `[RUN_FOLDER]` (and `[SESSION_FOLDER]\PROBLEMS.md` on browser timeout)
- Do ONLY the numbered items above. Report any item you could not complete as NOT DONE
- Do NOT modify any file in `[SKILL_FOLDER]`, `[INVENTORY_FILE]`, or `[SESSION_FOLDER]\model-sources\`; do NOT run Phase 9 distribution
- If Playwright MCP default tab experiences concurrent navigation interference, run extractions inside an isolated `page.context().browser().newContext()` and close it immediately after extraction
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state: overwrite `[RUN_FOLDER]\[DATE]_*-DOM.json` cleanly if already present
- Hang safety: no command may wait for stdin, a pager, or an unbounded child. Banned: see `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Robustness.md`. 60s per-page Playwright cap (max 2 attempts per URL). On second failure: record URL in `[SESSION_FOLDER]\PROBLEMS.md` and continue with remaining providers

Findings card: Load and update `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Findings.md`. Append one Partition Observations line and record any URL redirects or DOM selector changes.

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

Read `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Robustness.md` and `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Findings.md`. Treat earlier conversation as compacted. Step Phase 3 + Phase 4.
Planning document: `_PROMPTS_ModelInventoryUpdate_TEMPLATE.md`, Phase 3 and Phase 4.

Execute Phase 3 (Screenshot Archive) and Phase 4 (Transcribe Screenshots) into `[RUN_FOLDER]`.

1. Execute Phase 3 full-page scroll capture (`1920x1080` viewport, JPEG quality 90, scrolling `window` or `.docs-scroll-container` on OpenAI `O1`/`O2` by viewport height increments) for `A1`, `A3`, `A4`, `O1`, `O2`, `O3`, `G1`, `G2`, `Z1`, `Z2`, `X1`, `X2`, copying captured `.jpg` files from Playwright's default output directory into `[RUN_FOLDER]\[DATE]_screenshots\<SourceFolder>\`
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

<!-- Conditional: include Prompt 4 when [CAPABILITY_SCHEME] = LADDER; omit if [CAPABILITY_SCHEME] = NONE and renumber remaining prompts. -->
<!-- Provider DOM extracts are in [RUN_FOLDER]. Next prompt fetches the Epoch ECI CSV (scores and 95% intervals), reads vendor model pages for new models, and resolves the depth edge cases into [DATE]_Depth-Edges.json. -->

## Prompt 4 - Capability Evidence: Epoch ECI Intervals, New-Model Metadata, and Depth Edge Research

```
01-MdlInv-[RUN_MODE] [ 04 / 08 ] - P3-CapEvidence Refresh Epoch ECI intervals and resolve depth edge cases for new models

Session: `[SESSION_FOLDER]`
Working folder: `[RUN_FOLDER]`

Read `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Robustness.md`, `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Findings.md`, `[SESSION_FOLDER]\T02_MDLINVNTRY_ReliableModelInventory_2026-10-28\_INFO_MDLRGUP-MDLINVNTRY-04_SourcesPerField.md` (Section 6 Capability Evidence), and `[DESIGN_INFO]` Sections 2.2 (evidence kinds E1-E6) and 2.6 (edge cases EC-1 to EC-9). Treat earlier conversation as compacted. Step Capability Evidence.
Planning document: `_PROMPTS_ModelInventoryUpdate_TEMPLATE.md`, Prompt 4 Capability Evidence.

Refresh the Epoch ECI score and 95% interval of every registry model, collect `release_date` and `uc_class` for models that are new in `[RUN_FOLDER]\[DATE]_*-DOM.json`, and resolve every depth edge case for those models from vendor pages, writing the outcomes to `[RUN_FOLDER]\[DATE]_Depth-Edges.json`. No registry file is modified in this prompt.

1. Run `[VENV_PYTHON] "[SESSION_FOLDER]\match-epoch-eci.py" --run-folder "[RUN_FOLDER]" --date "[DATE]" --registry-file "[SKILL_FOLDER]\model-registry.json" --download` to download `https://epoch.ai/data/eci_scores.csv` into `[RUN_FOLDER]\[DATE]_eci-leaderboard.csv` and generate `[RUN_FOLDER]\[DATE]_Epoch-ECI-Match.json` (`model_id`, `epoch_name`, `eci_score`, `eci_ci_low`, `eci_ci_high` per matched model; `unmatched[]` registry models without an Epoch row; `new_models[]` = IDs present in `[RUN_FOLDER]\[DATE]_*-DOM.json` but absent from the registry)
2. For every ID in `new_models[]` (and every `[TARGET_MODELS]` entry in `NEWMODEL` mode): open the vendor model overview page with Playwright and record into `[RUN_FOLDER]\[DATE]_Depth-Edges.json` under `new_models` the `release_date` (vendor "Released" field, `YYYY-MM-DD`; set `release_date_assumed: true` only when the page gives a month without a day), `uc_class` (`UC-1 Apex` | `UC-2 Flagship` | `UC-3 Balanced` | `UC-4 Efficient` from the vendor's tier wording, checked against the price order within the point version), the page URL, and the access date. Also record a correction for any existing registry model whose "Released" field differs from its `release_date` (EC-9)
3. Resolve the edge cases of `[DESIGN_INFO]` Section 2.6 for every ID in `new_models[]` and for every existing model whose `eci_ci` appears for the first time in this run:
   - EC-1 (Apex or Flagship of a new point version): read the vendor's model-selection guidance; an escalation statement ("start with X; use Y when X at higher effort still falls short") = `deeper_than` candidate `{x, model, kind: "E1", source, accessed, statement}`; a parity statement or silence = `ties[]` line `{x, model, source, accessed, reason}`
   - EC-2 (new member of an existing tier family): read the successor's "what's new" or migration page; "extends" / "succeeds" at same tier and price = inherit the predecessor's recorded edges as candidates with that page as source
   - EC-3 (restricted-access twin): "same underlying model" / "same capabilities" = `ties[]` line with `kind: "E5"`
   - EC-4 (specialized Apex without score): announcement naming the base; more capable and higher price = `E1` candidate over the base; domain variant at equal price = `E5` tie
   - EC-5 (unscored Efficient or vision model): tier wording and price order = `estimates[]` line `{model, sibling, note: "E6"}`
   - Write every outcome, including "source silent → tie", with URL and access date; never leave a new model without an entry
4. Verify `[RUN_FOLDER]\[DATE]_Epoch-ECI-Match.json` and `[RUN_FOLDER]\[DATE]_Depth-Edges.json` are valid JSON; every `new_models[]` ID has `release_date`, `uc_class`, and at least one entry in `deeper_than_candidates[]`, `ties[]`, or `estimates[]`; every `deeper_than_candidates[]` entry has all five fields; close Playwright (`browser_close`)

Constraints:
- All file writes MUST stay within `[RUN_FOLDER]`
- Do ONLY the numbered items above. Report any item you could not complete as NOT DONE
- Read ECI from `https://epoch.ai/eci` (CSV download) only; never use Artificial Analysis Intelligence Index, LMArena Elo, gap-to-frontier, aggregators, or model recollection (`QS-12`)
- Vendor pages with Playwright only; quote statements verbatim; silence = tie (MDLRGUP-MDLINVNTRY-DD-04)
- Do NOT modify `[SKILL_FOLDER]` JSONs or `[INVENTORY_FILE]` in this prompt
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state: overwrite `[RUN_FOLDER]\[DATE]_Epoch-ECI-Match.json` and `[RUN_FOLDER]\[DATE]_Depth-Edges.json` cleanly
- Hang safety: no command may wait for stdin, a pager, or an unbounded child. Banned: see `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Robustness.md`. 60s Playwright/download cap (max 2 attempts per URL). On CSV failure: record in `[SESSION_FOLDER]\PROBLEMS.md`, fall back to the most recent `*_Epoch-ECI-Match.json` in `[SESSION_FOLDER]`, and continue. On vendor page failure: record the model as `ties[]` with `reason: "source unreachable"` and the URL in `[SESSION_FOLDER]\PROBLEMS.md`

Findings card: Load and update `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Findings.md`. Append one Partition Observations line; note new models without an Epoch row and every edge case resolved as a tie because the source was silent.

Verify: both JSON files exist and are valid; every `new_models[]` ID has `release_date`, `uc_class`, and an edge-case entry; Playwright browser is closed.

**STOP.** Report: items DONE / NOT DONE, models matched / unmatched in `[DATE]_Epoch-ECI-Match.json`, new models with their `release_date` and `uc_class`, `deeper_than` candidates (x > model, kind, source), ties, E6 estimates, and EC-9 release-date corrections.
```

---

## Prompt 5 - Phases 5, 6, and 7 Canonical JSON Updates and Gates 5-7

<!-- Expected state: DOM extracts ([DATE]_*-DOM.json), Epoch matches ([DATE]_Epoch-ECI-Match.json), and edge outcomes ([DATE]_Depth-Edges.json) are in [RUN_FOLDER]; updates the three canonical JSON files in [SKILL_FOLDER] and verifies Gates 5, 6, and 7. -->

```
01-MdlInv-[RUN_MODE] [ 05 / 08 ] - Phase 5 + Phase 6 + Phase 7 Update canonical JSONs and verify Gates 5-7

Session: `[SESSION_FOLDER]`
Working folder: `[RUN_FOLDER]`

Read `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Robustness.md` and `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Findings.md`. Treat earlier conversation as compacted. Step Phase 5 + Phase 6 + Phase 7.
Planning document: `_PROMPTS_ModelInventoryUpdate_TEMPLATE.md`, Prompt 5 (Phases 5, 6, and 7).

Execute Phases 5, 6, and 7 using the DOM extracts, Epoch matches, and edge outcomes in `[RUN_FOLDER]` to update `[SKILL_FOLDER]\model-registry.json`, `[SKILL_FOLDER]\model-pricing.json`, and `[SKILL_FOLDER]\model-parameter-mapping.json`, and verify Gates 5, 6, and 7. `depth`, `depth_evidence`, and `depth_estimated` are NOT written here (Prompt 6 layering).

1. Phase 5.0 (Derive Change Set): compare `[RUN_FOLDER]\[DATE]_*-DOM.json` against `[SKILL_FOLDER]\model-registry.json` and `[SKILL_FOLDER]\model-pricing.json`; write `newRegistryIds` (in DOM, absent from `models[]`), `newPricingIds` (in DOM, absent from `model-pricing.json`), and `changedPricingIds` (DOM price differs from current `model-pricing.json`) to `[RUN_FOLDER]\[DATE]_ChangeSet.json`
2. Phase 5.1-5.3 (`[SKILL_FOLDER]\model-registry.json`): insert new models at the top of their provider group (`"enabled": false, "status": "untested"`, or `"enabled": true` for testable text models) with `release_date`, `release_date_assumed` (when set), and `uc_class` from `[RUN_FOLDER]\[DATE]_Depth-Edges.json` `new_models`; backfill `context_window`; set `"status": "deprecated", "enabled": false` for newly deprecated models (never remove existing models); refresh `eci_score` and `eci_ci` `[low, high]` for every matched model from `[RUN_FOLDER]\[DATE]_Epoch-ECI-Match.json` (`eci_ci: null` for unmatched); copy every `deeper_than_candidates[]` entry onto its `x` model as a `deeper_than` item `{model, kind, source, accessed, statement}`; apply EC-9 `release_date` corrections; update `model_id_startswith[]` prefixes if needed; bump `_version` patch and `_updated` to `[DATE]`; then run `[VENV_PYTHON] "[SESSION_FOLDER]\format-model-registry.py" --registry-file "[SKILL_FOLDER]\model-registry.json"` to restore the 1-line-per-entry layout
3. Phase 6 (`[SKILL_FOLDER]\model-pricing.json`): add `newPricingIds` and update `changedPricingIds` using Standard tier prices across `openai`, `anthropic`, `google`, `zai`, and `xai` (`{input_per_1m, cached_per_1m|omit if null, output_per_1m, long_context|omit if no long tier, context_window_k, currency: "USD"}`; never remove legacy entries; for Z.AI use first list price only and `0.00` for free models), bump `last_updated` to `[DATE]`, and update `sources` array if URLs changed
4. Phase 7 (`[SKILL_FOLDER]\model-parameter-mapping.json`): verify every `method` in `model_id_startswith[]` maps to an existing key in `effort_mapping`; bump `_version` and `_updated` only if `model-parameter-mapping.json` was modified
5. Run Gates 5, 6, and 7 via `& "[SESSION_FOLDER]\verify-and-distribute-registry.ps1" -Mode Gate567 -RunFolder "[RUN_FOLDER]" -Date "[DATE]" -SkillFolder "[SKILL_FOLDER]" -InventoryFile "[INVENTORY_FILE]"`

Constraints:
- All file operations MUST stay within `[RUN_FOLDER]` and the three canonical JSON files in `[SKILL_FOLDER]` (`[SKILL_FOLDER]\model-registry.json`, `[SKILL_FOLDER]\model-pricing.json`, `[SKILL_FOLDER]\model-parameter-mapping.json`)
- Do ONLY the numbered items above. Report any item you could not complete as NOT DONE
- Never remove existing or deprecated models from `model-registry.json` or `model-pricing.json`
- Never write, edit, or delete `depth`, `depth_evidence`, or `depth_estimated` on any model (MDLRGUP-MDLINVNTRY-IG-01); never write a `deeper_than` item without all five fields (IG-03)
- Do NOT edit `[AGENT_FOLDER]` directly and do NOT execute Phase 9 distribution in this prompt
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state: JSON updates are idempotent and verified by Gates 5-7
- Hang safety: no command may wait for stdin, a pager, or an unbounded child. Banned: see `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Robustness.md`. 120s per-command cap. On cap: kill, record in `[SESSION_FOLDER]\PROBLEMS.md`, continue

Findings card: Load and update `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Findings.md`. Append one Partition Observations line and record any prefix gaps or new effort methods.

Verify: `[RUN_FOLDER]\[DATE]_ChangeSet.json` exists; Gates 5, 6, and 7 pass with exit code 0; `format-model-registry.py --check` passes; `_updated` / `last_updated` in modified `[SKILL_FOLDER]` JSONs equal `[DATE]`; `git --no-pager diff --stat -- "[SKILL_FOLDER]\model-registry.json"` shows no line where a `"depth":` value changed.

**STOP.** Report: items DONE / NOT DONE, `newRegistryIds` count, `newPricingIds` count, `changedPricingIds` count, `deeper_than` items written, `eci_ci` values refreshed, any prefix gaps, and Gate 5-7 results.
```

---

## Prompt 6 - Phase 8 Live API Tests, Phase 9.4 Depth Layering and Inventory Regeneration, and Phase 10 Report

<!-- Expected state: Canonical JSONs in [SKILL_FOLDER] passed Gates 5-7 and carry eci_ci, uc_class, release_date, deeper_than for new models; runs Phase 8 live API tests, Phase 9.4 insert-only depth layering and [INVENTORY_FILE] regeneration, and Phase 10 summary report. -->

```
01-MdlInv-[RUN_MODE] [ 06 / 08 ] - Phase 8 + Phase 9.4 + Phase 10 Test new models, layer depth ladder, regenerate MODEL_INVENTORY.md, and write report

Session: `[SESSION_FOLDER]`
Working folder: `[RUN_FOLDER]`

Read `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Robustness.md`, `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Findings.md`, `[RUN_FOLDER]\[DATE]_ChangeSet.json`, `[RUN_FOLDER]\[DATE]_Depth-Edges.json` (`ties`, `estimates`), and `[INVENTORY_FILE]` Sections 1-2. Treat earlier conversation as compacted. Step Phase 8 + Phase 9.4 + Phase 10.
Planning document: `_PROMPTS_ModelInventoryUpdate_TEMPLATE.md`, Prompt 6 (Phase 8, Phase 9.4, and Phase 10).

Execute Phase 8 (Test New Models), Phase 9.4 (Depth Layering and `MODEL_INVENTORY.md` Regeneration), and Phase 10 (Report), saving the run summary report to `[RUN_FOLDER]\[DATE]_RunReport.md`.

1. Execute Phase 8: for each model in `newRegistryIds` (`[RUN_FOLDER]\[DATE]_ChangeSet.json`) enabled for testing, run `[VENV_PYTHON] "[SKILL_FOLDER]\test-call-llm.py" --keys-file [KEYS_FILE] --model <modelId>` (adding a minimal test entry in `[SKILL_FOLDER]\test-call-llm.py` if absent) and apply Gate 8 status updates in `[SKILL_FOLDER]\model-registry.json` (`200 OK` -> `"status": "available", "enabled": true`; `401/403` -> `"status": "no_access", "enabled": false`; `429 Insufficient balance` -> `"status": "no_access"` on paid models, keep free models `"available"`; `400` -> adjust supported `effort` list in `model_id_startswith[]`)
2. Execute Phase 9.4 per `[MDLRGUP-MDLINVNTRY-SP01]` FR-01, FR-07, FR-08 (skip the first two sub-steps when `[CAPABILITY_SCHEME] = NONE`):
   - Run `[VENV_PYTHON] "[SESSION_FOLDER]\layer-depth-ladder.py" --registry-file "[SKILL_FOLDER]\model-registry.json" --match-file "[RUN_FOLDER]\[DATE]_Epoch-ECI-Match.json" --log-file "[RUN_FOLDER]\[DATE]_DepthLadder.log"` (insert-only, never `--bootstrap`): validates every `deeper_than` item, builds E1/E2/E3/E5 and manual edges, writes `depth`, `depth_evidence`, and `depth_estimated` for models without `depth` only, reports squeezes (`squeezed by X`) and E1-E3 contradictions, and aborts without writing on a cycle or a rejected item
   - Review the log: a **rejected** `deeper_than` item → fix the missing field from `[DATE]_Depth-Edges.json` and re-run; a **cycle** (run aborted) or a **CONTRADICTION** line (direct conflict; the script keeps the higher-precedence edge E4 > E1 > E3 and drops the other) → EC-8: re-check `uc_class` of both models on the vendor page; wrong class → fix and re-run; right class → record in `[DATE]_RunReport.md` Pending resolution (never change `uc_class` to silence a contradiction); a **squeeze** → EC-7: record `squeezed by X` in Pending resolution, no action in this run
   - Items and scope guard: for every model whose `observed.sequences >= 3`, set `items` to `observed.items` (largest fully completed `items_planned`; lower it when a skip observation says so); set `scope_guard: "strict"` only with a FAILS or ledger reference recorded in `[DATE]_RunReport.md`; never change `depth`
   - Run `[VENV_PYTHON] "[SESSION_FOLDER]\format-model-registry.py" --registry-file "[SKILL_FOLDER]\model-registry.json"` after the Phase 8 and Phase 9.4 registry edits (1-line-per-entry layout)
   - Run `[VENV_PYTHON] "[SESSION_FOLDER]\update-model-inventory.py" --skill-folder "[SKILL_FOLDER]" --inventory-file "[INVENTORY_FILE]" --today "[DATE]"` to regenerate `[INVENTORY_FILE]`: `Top rung: D[n] ([DATE])` header; columns `Model | Depth | Items | Context | Efforts | In USD | Cache USD | Out USD | Devin cost | Notes` (`D[n]*` for estimated rungs, `[n]m` for measured Items); Notes from `depth_evidence`, `UC-n`, Epoch score with interval or `no Epoch score`, status, `scope guard strict`, `CSV rows`, adaptive-thinking Medium warning, `squeezed by X`, `unplaced`; Section 3.1 and 3.2 sorted by 1) Depth descending, 2) Model ascending; Section 3.2 Devin-only rows stay hand-maintained in `[INVENTORY_FILE]` with their `*` rungs (EC-6)
3. Run Gate 9.4 via `& "[SESSION_FOLDER]\verify-and-distribute-registry.ps1" -Mode Gate94 -RunFolder "[RUN_FOLDER]" -Date "[DATE]" -SkillFolder "[SKILL_FOLDER]" -InventoryFile "[INVENTORY_FILE]"` (FR-10: every non-retired text model has `depth`; no `depth` differs from the committed registry at git `HEAD` except `depth_estimated: true` → measured; every `deeper_than` item has `model`, `kind`, `source`, `accessed`, `statement`; inventory sorted Depth desc, Model asc; `Top rung` equals the maximum `depth`; source versions/dates and `In USD` / `Cache USD` / `Out USD` columns consistent with `[SKILL_FOLDER]` JSONs)
4. Execute Phase 10 and write the complete run report (1. Added models, 2. Price changes, 3. Unchanged count, 4. Registry additions, 5. Prefix gaps, 6. Parameter mapping, 7. Test results, 8. Long context, 9. Pending resolution (squeezes, contradictions, ties from silent sources), 10. Sources archived in `[RUN_FOLDER]`, 11. `MODEL_INVENTORY.md` changes, 12. Depth ladder: inserted rungs with evidence, `deeper_than` items added, E6 estimates, `items` / `scope_guard` changes, Top rung before and after) to `[RUN_FOLDER]\[DATE]_RunReport.md`

Constraints:
- All file operations MUST stay within `[RUN_FOLDER]`, `[SKILL_FOLDER]\model-registry.json`, `[SKILL_FOLDER]\test-call-llm.py`, and `[INVENTORY_FILE]`
- Do ONLY the numbered items above. Report any item you could not complete as NOT DONE
- `depth` is written by `layer-depth-ladder.py` only; never edit `depth`, `depth_evidence`, or `depth_estimated` by hand, never run `--bootstrap`, never edit `[INVENTORY_FILE]` by hand (MDLRGUP-MDLINVNTRY-IG-01, IG-02, IG-04)
- Do NOT execute Phase 9.1-9.3 distribution in this prompt (distribution is isolated in Prompt 7)
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state: layering is insert-only and idempotent for models that already have `depth`; `MODEL_INVENTORY.md` regeneration and `[DATE]_RunReport.md` are idempotent
- Hang safety: no command may wait for stdin, a pager, or an unbounded child. Banned: see `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Robustness.md`. 120s per-model API test cap, 60s layering cap. On timeout: retry once, then record in `[RUN_FOLDER]\[DATE]_RunReport.md` and `[SESSION_FOLDER]\PROBLEMS.md`, continue

Findings card: Load and update `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Findings.md`. Append one Partition Observations line and record any API test failures (e.g., rejected effort values), squeezes, and contradictions.

Verify: Gate 8 and Gate 9.4 pass; `[RUN_FOLDER]\[DATE]_DepthLadder.log` ends with `OK:` (0 cycles, 0 rejected); `[INVENTORY_FILE]` `Top rung` equals the maximum `depth` in the registry; `[RUN_FOLDER]\[DATE]_RunReport.md` exists with all 12 Phase 10 report sections.

**STOP.** Report: items DONE / NOT DONE, Phase 8 test pass/fail summary, inserted rungs (model, `D[n]`, evidence), squeezes and contradictions, Gate 9.4 status, and path to `[RUN_FOLDER]\[DATE]_RunReport.md`.
```

---

## Prompt 7 - Phase 9 Distribution and Gate 9 Sync Check

<!-- Expected state: Phase 8 tests, Phase 9.4 layering and MODEL_INVENTORY.md update, and Phase 10 report are complete; distributes updated files to `.devin` and the Lana-V1 runtime config, then verifies Gate 9. -->

```
01-MdlInv-[RUN_MODE] [ 07 / 08 ] - Phase 9 Distribute canonical JSONs and MODEL_INVENTORY.md and verify Gate 9

Session: `[SESSION_FOLDER]`
Working folder: `[RUN_FOLDER]`

Read `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Robustness.md` and `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Findings.md`. Treat earlier conversation as compacted. Step Phase 9.
Planning document: `_PROMPTS_ModelInventoryUpdate_TEMPLATE.md`, Prompt 7 (Phase 9.1-9.3 and Gate 9).

Distribute the updated canonical JSON files (`model-pricing.json`, `model-registry.json`, `model-parameter-mapping.json`) and `[INVENTORY_FILE]` from `[PROMPTSYSTEM_FOLDER]` to all authorized distribution targets and verify file-hash identity via Gate 9.

1. Execute Phases 9.1 (`[AGENT_FOLDER]\skills\llm-tools\`: 3 JSONs, `test-call-llm.py`, `MODEL_INVENTORY.md`), 9.3 (3 JSONs to `e:\Dev\Lana-V1\.agent-data\config`; Phase 9.2 dependent-skill replicas no longer exist since the 2026-10-29 `llm-tools` merge), and Gate 9 via `& "[SESSION_FOLDER]\verify-and-distribute-registry.ps1" -Mode Distribute -RunFolder "[RUN_FOLDER]" -Date "[DATE]" -SkillFolder "[SKILL_FOLDER]" -InventoryFile "[INVENTORY_FILE]" -AgentFolder "[AGENT_FOLDER]" -PromptSystemFolder "[PROMPTSYSTEM_FOLDER]" -IncludeExternal`
2. Append the Phase 9 distribution and Gate 9 sync verification result (targets synced, SHA-256 match count) to `[RUN_FOLDER]\[DATE]_RunReport.md`

Constraints:
- All file operations MUST stay within `[RUN_FOLDER]`, `[AGENT_FOLDER]\skills\llm-tools\`, and `e:\Dev\Lana-V1\.agent-data\config` (3 model JSONs only; never touch other files there, e.g. `agent-config.json`, `.api-keys.txt`)
- External distribution to `e:\Dev\Lana-V1\.agent-data\config` is pre-authorized by the user (DD-14, 2026-11-02); do not ask
- Distribution requires Gate 9.4 passed in Prompt 6; if `[RUN_FOLDER]\[DATE]_DepthLadder.log` does not end with `OK:`, stop and report
- Do ONLY the numbered items above. Report any item you could not complete as NOT DONE
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state: `Copy-Item -Force` and hash verification are idempotent
- Hang safety: no command may wait for stdin, a pager, or an unbounded child. Banned: see `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Robustness.md`. 60s per-command cap. On cap: kill, record in `[SESSION_FOLDER]\PROBLEMS.md`, continue

Findings card: Load and update `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Findings.md`. Append one Partition Observations line.

Verify: Gate 9 passes with zero SHA-256 hash mismatches across all synced targets; `[AGENT_FOLDER]\skills\llm-tools\MODEL_INVENTORY.md` hash matches `[INVENTORY_FILE]`.

**STOP.** Report: items DONE / NOT DONE, targets synced (with SHA-256 match count), and Gate 9 status.
```

---

## Prompt 8 - Final Verification Checkpoint

<!-- Expected state: All update, test, layering, inventory regeneration, and distribution steps are complete; runs the verification checkpoint across all run deliverables, commits the registry, and updates session tracking. -->

```
01-MdlInv-[RUN_MODE] [ 08 / 08 ] - Final Checkpoint Verify all gates, deliverables, and session tracking

Session: `[SESSION_FOLDER]`
Working folder: `[RUN_FOLDER]`

Read `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Robustness.md`, `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Findings.md`, and `[RUN_FOLDER]\[DATE]_RunReport.md`. Treat earlier conversation as compacted. Step Final Checkpoint.
Planning document: `_PROMPTS_ModelInventoryUpdate_TEMPLATE.md`, Prompt 8 Final Checkpoint.

Verify all outputs of the `[DATE]` `[RUN_MODE]` model inventory update run against Gates 1-9.4 and the depth ladder invariants, fix any gaps inline within 2 cycles, commit the run, and record the completed run in `[SESSION_FOLDER]\NOTES.md`.

/verify

1. Run `& "[SESSION_FOLDER]\verify-and-distribute-registry.ps1" -Mode VerifyAll -RunFolder "[RUN_FOLDER]" -Date "[DATE]" -SkillFolder "[SKILL_FOLDER]" -InventoryFile "[INVENTORY_FILE]" -AgentFolder "[AGENT_FOLDER]" -PromptSystemFolder "[PROMPTSYSTEM_FOLDER]" -IncludeExternal` to verify Gates 2, 5, 6, 7, 9 (incl. Lana-V1 config), and 9.4, `[DATE]_RunReport.md`, and zero leftover `.tmp_*` scripts in `[RUN_FOLDER]\_agentwork\`
2. Check that `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Findings.md` `## Unresolved` is empty (or copied to `[SESSION_FOLDER]\PROBLEMS.md`) and that every Pending resolution item of `[DATE]_RunReport.md` Section 9 (squeezes, contradictions, silent-source ties) has a `[SESSION_FOLDER]\PROBLEMS.md` entry
3. Fix any verification gaps inline (max 2 gate cycles; on second failure record in `[SESSION_FOLDER]\PROBLEMS.md` and stop); commit `[SKILL_FOLDER]`, `[AGENT_FOLDER]\skills\llm-tools\`, and `[RUN_FOLDER]` with message `chore(llm-tools): model inventory [RUN_MODE] run [DATE]` (the next run's Gate 9.4 compares `depth` against this commit); in repo `e:\Dev\Lana-V1` commit only `.agent-data/config/model-pricing.json`, `.agent-data/config/model-registry.json`, `.agent-data/config/model-parameter-mapping.json` with message `chore(config): model registry update [DATE]` (skip when unchanged); update `[SESSION_FOLDER]\NOTES.md` with a 1-line entry recording `[DATE] [RUN_MODE]` completion, `Top rung`, and `[RUN_FOLDER]` path

Constraints:
- All file operations MUST stay within `[RUN_FOLDER]`, `[SESSION_FOLDER]\NOTES.md`, `[SESSION_FOLDER]\PROBLEMS.md`, `[SKILL_FOLDER]`, `[INVENTORY_FILE]`, `[AGENT_FOLDER]\skills\`, and the 3 model JSONs in `e:\Dev\Lana-V1\.agent-data\config`
- Do ONLY the numbered items above. Report any item you could not complete as NOT DONE
- In `e:\Dev\Lana-V1`, stage only the 3 model JSONs by explicit path; never `git add -A` or commit other changes in that repo
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state: verification and `NOTES.md` status update are idempotent; the commit is skipped when the working tree is clean
- Hang safety: see `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Robustness.md`

Findings card: Load and update `[RUN_FOLDER]\_agentwork\__CARD_MDLRGUP-Findings.md`. Append final Partition Observations line.

Verify: Gates 5, 6, 7, 9, and 9.4 pass; zero `.tmp_*` files remain in `[RUN_FOLDER]\_agentwork\`; `git status --porcelain -- "[SKILL_FOLDER]"` is empty; `[SESSION_FOLDER]\NOTES.md` lists the `[DATE] [RUN_MODE]` run.

**STOP.** Report: verify findings fixed / open, commit hash, total net time across the run from `__CARD_MDLRGUP-Findings.md`, final run status, and a clickable summary artifact list with separate headings for each output group formatted as: heading, summary of what was done and what the files contain, and bulleted clickable file paths with file purpose/content (`- `relative/path/to/file` - <description>`). Do not wrap the list in code fences, and never use file:/// links or raw HTML.
```

<!-- EXAMPLE: Reference only. Do not copy into new documents. Shows a completed NEWMODEL run instance (Prompt 1 resolved and the Prompt 4 STOP report; Prompt 3 omitted because [INCLUDE_SCREENSHOTS] = NO, renumbered to [ 01 / 07 ] - [ 07 / 07 ]). Model IDs and statements are illustrative.

## Example (NEWMODEL Run Instance - Prompt 1 Resolved, Prompt 4 Report)

`````markdown
---
intended_model: claude-opus-5
context_window_size: 1000k
effort: high
prompt_system: IPPS
---

<!-- Model: claude-opus-5 (effort: high, context: 1000k). Load grouping (PRMT-SC-07): 10 phases of the model inventory update pipeline partitioned into 07 prompts (<= 7 items, <= 4 modified files, <= 1 heavy workflow per prompt) so Playwright DOM scraping, Epoch matching and vendor edge research, JSON updates, depth layering, API testing, and distribution stay within single-turn budgets. -->

## Prompt 1 - Bootstrap: Detect Context, Create Run Folder, and Generate Instance

<!-- Detects NEWMODEL and 2026-12-01, creates _2026-12-01_NEWMODEL and _agentwork cards, and instantiates _PROMPTS_01-MdlInv-NEWMODEL.md. -->

```
01-MdlInv-NEWMODEL [ 01 / 07 ] - P3-Bootstrap Detect run parameters, initialize run folder, and generate prompts instance

Session: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate`
Working folder: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate`

Read `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\NOTES.md`, `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_PROMPTS_ModelInventoryUpdate_TEMPLATE.md` (Placeholders, Run modes, Run folder structure, Depth ladder invariants), and `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agentwork\__CARD_MDLINVNTRY-Robustness.md`. Treat earlier conversation as compacted. Step P3-Bootstrap.
Planning document: `_PROMPTS_ModelInventoryUpdate_TEMPLATE.md`, Prompt 1 Bootstrap.

Initialize a datestamped model inventory update run folder and instantiate a ready-to-run prompts file from `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_PROMPTS_ModelInventoryUpdate_TEMPLATE.md`.

1. Detect workspace and run parameters:
   - Resolve `e:\dev\IPPS`, active `e:\dev\IPPS\PromptSystemV4.5`, `e:\dev\IPPS\.devin`, `e:\dev\IPPS\PromptSystemV4.5\skills\llm-tools`, `e:\dev\IPPS\PromptSystemV4.5\skills\llm-tools\MODEL_INVENTORY.md`, and `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_INFO_HOW_TO_ORGANIZE_LLMS_BY_CAPABILITY.md`
   - Set `2026-12-01` from request metadata, `NEWMODEL`, `Anthropic`, `claude-opus-5-6, claude-sonnet-5-6`, `NO` (`INCLUDE_SCREENSHOTS`), `LADDER` (`CAPABILITY_SCHEME` from `NOTES.md` Key Decisions `DD-10`), and `06` (`TOTAL_PROMPTS` in generated instance after excluding Bootstrap and Prompt 3)
   - Verify `git status --porcelain -- "e:\dev\IPPS\PromptSystemV4.5\skills\llm-tools\model-registry.json"` is empty
2. Create the isolated run folder `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-12-01_NEWMODEL` and `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-12-01_NEWMODEL\_agentwork\`
3. Copy `__CARD_MDLINVNTRY-Robustness.md` to `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-12-01_NEWMODEL\_agentwork\__CARD_MDLRGUP-Robustness.md` and initialize `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-12-01_NEWMODEL\_agentwork\__CARD_MDLRGUP-Findings.md` with `# Findings Card: MDLRGUP (2026-12-01 NEWMODEL)`, `## Partition Observations`, `## Unresolved`, and `## Resolved`
4. Generate `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_2026-12-01_NEWMODEL\_agentwork\_PROMPTS_01-MdlInv-NEWMODEL.md` from `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_PROMPTS_ModelInventoryUpdate_TEMPLATE.md`:
   - Exclude Prompt 1 (already executed in this turn)
   - Remove Prompt 3 (`INCLUDE_SCREENSHOTS = NO`), keeping Prompts 2, 4, 5, 6, 7, 8 as `[ 01 / 06 ]` to `[ 06 / 06 ]`
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

Prompt 4 STOP report (illustrative):

```
DONE 1-4. Matched 93 / 96 registry models; unmatched: claude-opus-5-6, claude-sonnet-5-6, grok-build-0.1 (no Epoch row).
New models: claude-opus-5-6 (release_date 2026-11-20, UC-2 Flagship, $4 / $20), claude-sonnet-5-6 (2026-11-20, UC-3 Balanced, $1.50 / $7.50).
deeper_than candidates: none (EC-1: Anthropic model overview "Choosing a model" names Opus 5.6 as the default start and Fable 5.1 for demanding reasoning - escalation statement already recorded for Fable 5.1 > Opus 5.5; no statement ranks Opus 5.6 against Fable 5.1 -> tie).
Ties: claude-opus-5-6 ~ claude-fable-5-1 (source https://platform.claude.com/docs/en/models/overview, accessed 2026-12-01, reason: parity statement only).
E6 estimates: none. EC-9 corrections: none.
Expected Prompt 6 result: claude-opus-5-6 D11 or D12 by E2 >= claude-opus-5-5 and E1 > claude-sonnet-5-6; claude-sonnet-5-6 by E2 >= claude-sonnet-5-5.
```
`````
-->
