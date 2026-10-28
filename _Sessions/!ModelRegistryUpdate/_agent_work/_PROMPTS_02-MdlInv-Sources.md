---
intended_model: glm-5.2
context_window_size: 1M
effort: high
prompt_system: IPPS
---

<!-- Budget: compressed 2026-10-28 19:45. Original plan had 7 prompts in this file; compressed to 3 by merging web research into one batch, folding P1-S8+S9+P2-S1+S2 into one evaluate+decisions prompt, and dropping the separate critique (self-critique inside evaluation). Prerequisite: sub-chain 01 complete (P1-S1..S3 `[x]`).
Planning document: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__STRUT_MDLINVNTRY.md`. Raw page extracts go to `_SOURCES\` in the working folder. -->

## Prompt 5 - Web research batch: ECI, METR, Google, provider URLs

```
02-MdlInv-Sources [ 01 / 03 ] - P1-S4..S7 Merged web batch: ECI match, METR, Google, provider URL checks, Sources-per-Field file

Session: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate`
Working folder: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\T02_MDLINVNTRY_ReliableModelInventory_2026-10-28`

Read `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__STRUT_MDLINVNTRY.md` (Plan P1, MUST-NOT-FORGET), `_INFO_MDLRGUP-MDLINVNTRY-02_Sources.md`, `_agent_work\__STRUT_MDLRGUP-MDLINVNTRY.md` (Existing Tier Design, assumptions), `e:\dev\IPPS\update-model-registry.md` sections Sources and Phase 2, and `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Findings.md`. Treat earlier conversation as compacted. Steps P1-S4..S7 (merged).
Planning document: `__STRUT_MDLINVNTRY.md`, step P1-S4..S7.

Objective: every inventory field has a named source with cadence, extraction method, and coverage in a new Sources-per-Field file; web assumptions are closed. ECI matching uses the local CSV (already downloaded); Playwright for METR, Google, and spot-checking key provider URLs.

1. ECI match from local CSV: Read `C:\Users\User\Downloads\eci-leaderboard-general.csv` and `e:\dev\IPPS\PromptSystemV4.5\skills\llm-evaluation\model-registry.json`. For each of the 28 registry models, find the best ECI match by model name or family prefix; record model name, ECI value, and confidence interval; count coverage N/28. Save match table as `_SOURCES\2026-10-28_Epoch-ECI-Match.json`
2. METR via Playwright: Navigate `https://metr.org/time-horizons/`. Record per-model 50% and 80% horizon values, units, coverage of the 28 models. Save as `_SOURCES\2026-10-28_METR-TimeHorizons-DOM.json`. If page fails twice: record in `PROBLEMS.md`, mark [UNVERIFIED], continue
3. Google via Playwright: Navigate `https://ai.google.dev/gemini-api/docs/pricing` and `https://ai.google.dev/gemini-api/docs/models`. Record models listed, context window, max output, effort levels, price columns, whether data is in HTML tables. Save as `_SOURCES\2026-10-28_Google-Pricing-DOM.json` and `_SOURCES\2026-10-28_Google-Models-DOM.json`. Note extraction gap vs existing providers in `update-model-registry.md`
4. Provider URL batch: Resolve the nine URLs A1-A4, O1-O3, Z1-Z2 from `update-model-registry.md` via a `.tmp_` PowerShell script (`Invoke-WebRequest -TimeoutSec 20 -MaximumRedirection 5`, write results to `_agent_work\.tmp_url-check-results.txt`). Update each Sources file entry with status "checked", "redirected to [URL]", or "dead". Delete the script after
5. Create `_INFO_MDLRGUP-MDLINVNTRY-04_SourcesPerField.md` (Doc ID `MDLRGUP-MDLINVNTRY-IN04`, first line `<PromptSystem MarkdownTablesAllowed=true />`): one section per inventory field (Context window, Max output, Effort levels, Prices, Release date, Capability evidence, Behavior evidence, Agent environment availability). Each section: Source | URL | Update cadence | Extraction method | Coverage of 28 models | Caveats. Fill from items 1-4 with inline citations `[VERIFIED] (SOURCE_ID | URL)`. Fill Behavior evidence from `T01_MDLBHVPRM...\_INFO_MDLBHVPRM-05_CoverageMatrix.md` (IFEval-Hard, OverAct coverage only). Fill Agent environment availability from `windsurf-model-registry.json` only (note Claude Code, Codex CLI, Cursor as "not inventoried")
6. Close assumptions: every "pending web check" in research STRUT becomes CORRECT, PARTIAL, or WRONG. Write "Preflight accuracy: N/M verified" into Sources file header. Set Epoch and METR entries to "checked" with access date

Constraints:
- All file operations MUST stay within the declared working folder unless an absolute path outside it is explicitly named in this prompt
- Do ONLY the numbered items above. Report any item you could not complete as NOT DONE
- Epoch values from epoch.ai only; no Artificial Analysis, LMArena, or gap-to-frontier values; no Google AI Overview text
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state or waste cost: existing `_SOURCES\` extracts of today are reused
- Hang safety: see `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Robustness.md` (Playwright 2-minute cap per page, URL batch 2-minute cap). `browser_close` at the end. No `.tmp_` scripts remain after
- Timestamps from this prompt's request metadata

Findings card: Load and update `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Findings.md`. Append one Partition Observations line.

Closing: mark `P1-S4..S7` and `P1-D3` `[x]` in `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__STRUT_MDLINVNTRY.md`; move to Done in `PROGRESS.md`; add Time Log line to research STRUT.

Verify: `P1-S3` is `[x]` in `__STRUT_MDLINVNTRY.md`. `_SOURCES\` has ECI match JSON, METR JSON, Google JSONs. `-04_SourcesPerField.md` has eight field sections with coverage counts. Sources file has no "unchecked" entries; assumptions closed. No `.tmp_` scripts remain.

**STOP.** Report: items DONE / NOT DONE, Epoch coverage N/28, METR coverage N/28, URLs checked/redirected/dead, pages failed.
```

---

## Verification Checkpoint 3

```
02-MdlInv-Sources [ 02 / 03 ] - Verification checkpoint after prompt 5

Session: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate`
Working folder: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\T02_MDLINVNTRY_ReliableModelInventory_2026-10-28`

Read `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Robustness.md`, `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__STRUT_MDLINVNTRY.md`, and `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Findings.md`. Treat earlier conversation as compacted.

/verify

current state against `__STRUT_MDLINVNTRY.md` step P1-S4..S7 and deliverable P1-D3; `_INFO_MDLRGUP-MDLINVNTRY-02_Sources.md` against @skills:research-methods `RESEARCH_RULES.md` Sources Check (SC-*); `_INFO_MDLRGUP-MDLINVNTRY-04_SourcesPerField.md` against Topic Files Check (TF-*).

/fix

all gaps. Max 2 gate cycles; on second failure record in `PROBLEMS.md` and stop.

**STOP.** Report: verify findings fixed / open.
```

---

## Prompt 6 - Evaluate options, write summary, present decisions

<!-- Merges P1-S8, P1-S9, P2-S1, P2-S2. Options evaluation with self-critique, lightweight summary, DD-01..05 in chat. -->

```
02-MdlInv-Sources [ 03 / 03 ] - P1-S8+S9 Evaluate work-per-prompt options, write summary, present DD-01..05

Session: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate`
Working folder: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\T02_MDLINVNTRY_ReliableModelInventory_2026-10-28`

Read `_INFO_MDLRGUP-MDLINVNTRY-03_InventoryAudit.md` (Summary, Counts), `_INFO_MDLRGUP-MDLINVNTRY-04_SourcesPerField.md`, `_INFO_MDLRGUP-MDLINVNTRY-02_Sources.md`, `_agent_work\__STRUT_MDLRGUP-MDLINVNTRY.md` (Existing Tier Design), `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__STRUT_MDLINVNTRY.md` (Plan P2 Strategy: DD-01..05), `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Findings.md` (Partition Observations), `e:\dev\IPPS\.devin\rules\agent-behavior.md` section Presenting Decisions, `e:\dev\IPPS\.devin\skills\research-methods\RESEARCH_CREATE_SUMMARY.md`, and `e:\dev\IPPS\.devin\skills\research-methods\RESEARCH_SUMMARY_TEMPLATE.md`. Treat earlier conversation as compacted. Steps P1-S8+S9 (merged, folds P2-S1, P2-S2).
Planning document: `__STRUT_MDLINVNTRY.md`, step P1-S8+S9.

Objective: (a) options for "work per prompt" scored and recommended, (b) summary synthesizes all findings, (c) DD-01..05 presented in chat so the user can answer in one line.

1. Read for evidence: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\T01_MDLBHVPRM_BehavioralParameterBenchmarks_2026-10-19\_INFO_MDLBHVPRM-06_ModelAwarePartitioning.md` Section 4; `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_INFO_HOW_TO_ORGANIZE_LLMS_BY_CAPABILITY.md` Sections 4, 9, 10; `e:\Dev\KarstensWorkspace\_Sessions\_!AINewsResearch\_PROMPTS_AI-News-Research_TEMPLATE.md` lines 55-62 (GLM-5.2 prompt sizes in production)
2. Create `_INFO_MDLRGUP-MDLINVNTRY-05_WorkPerPromptOptions.md` (Doc ID `MDLRGUP-MDLINVNTRY-IN05`, `<PromptSystem MarkdownTablesAllowed=true />`). Scoring dimensions 0-3: Sourced, Coverage, Tokens, General purpose, Calibratable. Options: a) ECI band to HWH table, b) METR 80% horizon + fallback, c) model-agnostic fixed limits without WF, d) keep YY-L formula, e) UC-1..5 to HWH table. Per option: What, Evidence for, Evidence against, Score, Self-critique (one paragraph: what could be wrong about this score). Comparison table, Recommendation, worked example (3 HWH task on glm-5.2 high and claude-opus-5 high), Limitations
3. Create `_INFO_MDLRGUP-MDLINVNTRY-01_Summary.md` (Doc ID `MDLRGUP-MDLINVNTRY-IN01`) from `RESEARCH_SUMMARY_TEMPLATE.md`. Fill: header (Goal, Timeline, Depends on -02..-05, Research stats from time log), Research Question, Strategy & Domain, topic file index, Key Findings (8-12 labeled bullets synthesizing -03, -04, -05), "Decisions for [ACTOR]" with DD-01..05 in Presenting Decisions format (Problem, Context, Options with What / Why it works / Implication, one recommendation per decision, reply format `DD-01 a, DD-02 c, ...`), Recommendation, Limitations
4. Present DD-01 to DD-05 in chat (copy from -01 Summary), closing with reply format. Add to session NOTES.md Key Decisions: `DD-01..05 presented [timestamp]; answers pending`. Mark research STRUT phases and Time Log complete; set all Sources entries to final status

Constraints:
- All file operations MUST stay within the declared working folder unless an absolute path outside it is explicitly named in this prompt; paths in item 1 are read-only
- Do ONLY the numbered items above. Report any item you could not complete as NOT DONE
- No new web research; no option scores 3 on Sourced unless every value has a URL
- Do not decide DD-01..05; recommend only
- Execute without asking for confirmation
- Hang safety: see `__CARD_MDLINVNTRY-Robustness.md`
- Timestamps from this prompt's request metadata

Findings card: Load and update `__CARD_MDLINVNTRY-Findings.md`. Append one Partition Observations line.

Closing: mark `P1-S8+S9`, `P1-D4`, `P1-D5`, P1 Objectives `[x]` in `__STRUT_MDLINVNTRY.md`; move to Done in `PROGRESS.md`; add Time Log line to research STRUT.

Verify: `P1-S4..S7` is `[x]` in `__STRUT_MDLINVNTRY.md`. `-05` has five options with scores, self-critique, comparison, recommendation. `-01` has Key Findings, Decisions, Research stats. Chat output ends with reply format. Sources file has no "unchecked" entry. Research STRUT phases `[x]`.

**STOP.** Report: items DONE / NOT DONE, scores per option, recommended option per DD, finding count.
```
