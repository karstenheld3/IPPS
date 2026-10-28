---
intended_model: glm-5.2
context_window_size: 1M
effort: high
prompt_system: IPPS
---

<!-- Budget (PROMPTS_GUIDES.md Section 1g): model row glm-5.2, label 26-D, profile guarded, effort high, WF 0.25 HWH, this file P1-S4..S9 = 2.0 HWH, computed 8 implementation prompts, chosen 4 (deviation and reasons stated in `_PROMPTS_01-MdlInv-Audit.md` opening commentary). Checkpoints: after prompts 5-6 (`/verify` + `/fix`), after prompts 7-8 (`/verify` + `/fix` on the research set, commit), then one `/critique` prompt alone (heavy workflow, one per prompt). Prerequisite: sub-chain 01 complete (P1-S1..S3 `[x]`).
Planning document: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__STRUT_MDLINVNTRY.md`. Raw page extracts go to `_SOURCES\` in the working folder; documents count toward max_files, extracts and tracking files do not. -->

## Prompt 5 - Capability evidence: Epoch ECI and METR time horizons

```
02-MdlInv-Sources [ 01 / 07 ] - P1-S4 P1-S5 Read Epoch ECI and METR time horizons; start the Sources-per-Field file

Session: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate`
Working folder: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\T02_MDLINVNTRY_ReliableModelInventory_2026-10-28`

Read `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__STRUT_MDLINVNTRY.md` (Plan P1, MUST-NOT-FORGET), `_INFO_MDLRGUP-MDLINVNTRY-02_Sources.md`, `_agent_work\__STRUT_MDLRGUP-MDLINVNTRY.md` (section Existing Tier Design), and `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Findings.md`. Treat earlier conversation as compacted. Steps P1-S4, P1-S5.
Planning document: `__STRUT_MDLINVNTRY.md`, steps P1-S4, P1-S5.

Objective: the two public capability sources are measured on four questions (table shape, coverage of the 28 models in `MODEL_INVENTORY.md` Section 3.1, snapshot or update date, extraction method), and the Sources-per-Field file exists with its field skeleton and the capability section filled. All pages via Playwright MCP.

1. Google discovery (URL discovery only, 3 queries, 10-minute cap): `"Epoch Capabilities Index" models table`, `"time horizon" models site:metr.org`, `"Gemini API" pricing site:ai.google.dev`. Register new relevant URLs in `_INFO_MDLRGUP-MDLINVNTRY-02_Sources.md` with status "unchecked"
2. Navigate `https://epoch.ai/eci`. Record: columns of the model table, whether values are in HTML tables or a JSON data endpoint (check network requests), snapshot date, and for each of the 28 inventory models whether an ECI value exists (value, else "missing"). Save the extracted table as `_SOURCES\2026-10-28_Epoch-ECI-DOM.json`
3. Navigate `https://metr.org/time-horizons/`. Record: per-model 50% and 80% horizon values with units, confidence intervals if shown, which inventory models are covered, publication or update cadence, extraction method. Save the extracted table as `_SOURCES\2026-10-28_METR-TimeHorizons-DOM.json`
4. Create `_INFO_MDLRGUP-MDLINVNTRY-04_SourcesPerField.md` (Doc ID `MDLRGUP-MDLINVNTRY-IN04`, first line `<PromptSystem MarkdownTablesAllowed=true />`) with one section per inventory field: Context window, Max output, Effort levels, Prices, Release date, Capability evidence, Behavior evidence, Agent environment availability. Each section has the same table: Source | URL | Update cadence | Extraction method | Coverage of 28 models | Caveats. Fill Capability evidence (Epoch, METR) from items 2-3 with inline citations `[VERIFIED] (SOURCE_ID | URL)`; fill Behavior evidence from `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\T01_MDLBHVPRM_BehavioralParameterBenchmarks_2026-10-19\_INFO_MDLBHVPRM-05_CoverageMatrix.md` (IFEval-Hard, OverAct coverage numbers only, no new research). Set the status of Epoch and METR entries in the Sources file to "checked" with access date

Constraints:
- All file operations MUST stay within the declared working folder unless an absolute path outside it is explicitly named in this prompt
- Do ONLY the numbered items above. Do not refactor, rename, add tests, or touch files not listed. Report any item you could not complete as NOT DONE
- Epoch values from epoch.ai only; no Artificial Analysis, LMArena, or gap-to-frontier values; no Google AI Overview or Featured Snippet text
- A page that fails twice (timeout, 403, captcha): record URL and error in `PROBLEMS.md`, mark dependent rows [UNVERIFIED], continue
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state or waste cost: existing `_SOURCES\` extracts of today are reused, existing table rows are kept
- Hang safety: no command may wait for a key, stdin, a pager, or an unbounded child. Banned list and caps: see `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Robustness.md` (Playwright step 2-minute cap, Google batch 10-minute cap). On a cap: kill the process tree, record command and cap in `PROBLEMS.md` of the working folder, continue. `browser_close` at the end
- Timestamps in all files come from this prompt's request metadata

Findings card: Load and update `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Findings.md`. File glitches, spec-code mismatches, and unexpected findings. Read at prompt startup for unresolved entries from prior prompts. Append one Partition Observations line for this prompt.

Closing: mark `P1-S4`, `P1-S5` `[x]` in `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__STRUT_MDLINVNTRY.md`; move both to Done in `PROGRESS.md`; add a Time Log line to `_agent_work\__STRUT_MDLRGUP-MDLINVNTRY.md`.

Verify: Confirm `P1-S3` is `[x]` in `__STRUT_MDLINVNTRY.md`. `_SOURCES\` contains the two DOM JSON files of today. `_INFO_MDLRGUP-MDLINVNTRY-04_SourcesPerField.md` has eight field sections; Capability evidence lists Epoch and METR with coverage counts out of 28; every claim carries a verification label and a source ID. The Sources file shows Epoch and METR as "checked".

**STOP.** Report: items DONE / NOT DONE, Epoch coverage N/28, METR coverage N/28, pages failed.
```

---

## Prompt 6 - Provider documentation: Google, and the nine known URLs

<!-- Expected state: -04 exists with the capability section. This prompt fills the fact fields (context, max output, effort levels, prices, release date) and closes the assumption check. -->

```
02-MdlInv-Sources [ 02 / 07 ] - P1-S6 P1-S7 Check Google Gemini API pages and the nine provider URLs; fill the fact fields

Session: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate`
Working folder: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\T02_MDLINVNTRY_ReliableModelInventory_2026-10-28`

Read `_INFO_MDLRGUP-MDLINVNTRY-02_Sources.md`, `_INFO_MDLRGUP-MDLINVNTRY-04_SourcesPerField.md`, `e:\dev\IPPS\update-model-registry.md` sections Sources and Phase 2, `_agent_work\__STRUT_MDLRGUP-MDLINVNTRY.md` (assumptions), and `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Findings.md`. Treat earlier conversation as compacted. Steps P1-S6, P1-S7.
Planning document: `__STRUT_MDLINVNTRY.md`, steps P1-S6, P1-S7.

Objective: every fact field of the inventory has a named provider source with cadence, extraction method, and coverage, including Google, and the pre-research assumptions are closed with an accuracy score. All pages via Playwright MCP.

1. Navigate `https://ai.google.dev/gemini-api/docs/pricing` and `https://ai.google.dev/gemini-api/docs/models`. Record: models listed, context window, max output, thinking or effort levels, price columns, whether data is in HTML tables (run the Table Extraction snippet from `update-model-registry.md` Common Procedures) or in other markup. Save extracts as `_SOURCES\2026-10-28_Google-Pricing-DOM.json` and `_SOURCES\2026-10-28_Google-Models-DOM.json`
2. Resolve the nine URLs A1-A4, O1-O3, Z1-Z2 from `update-model-registry.md`: HTTP status, final URL after redirects, and for A1, O1, O2, Z1 whether a pricing table is still present. Update each entry in the Sources file with status "checked", "redirected to [URL]", or "dead"
3. Fill the sections Context window, Max output, Effort levels, Prices, Release date of `_INFO_MDLRGUP-MDLINVNTRY-04_SourcesPerField.md`: one row per provider (Anthropic, OpenAI, Z.AI, Google) with URL, cadence, extraction method, coverage, caveats; add a column or note "current extraction in update-model-registry.md: Phase 2.x / none" so the gap for Google is visible
4. Fill Agent environment availability from `e:\dev\IPPS\PromptSystemV4.5\skills\devin-auto-model-switcher\windsurf-model-registry.json` only (Devin display names, exposed effort levels, cost multipliers; no web research for other environments - note Claude Code, Codex CLI, Cursor as "not inventoried, alias table candidate"). Close the assumption check in the research STRUT (every "pending web check" becomes CORRECT, PARTIAL, or WRONG) and write "Preflight accuracy: N/M verified" into the Sources file header

Constraints:
- All file operations MUST stay within the declared working folder unless an absolute path outside it is explicitly named in this prompt; `windsurf-model-registry.json` and `update-model-registry.md` are read-only
- Do ONLY the numbered items above. Do not refactor, rename, add tests, or touch files not listed. Report any item you could not complete as NOT DONE
- Do not run any phase of `update-model-registry.md`; reuse only its JavaScript snippets for table extraction
- A page that fails twice: record URL and error in `PROBLEMS.md`, mark the row [UNVERIFIED], continue
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state or waste cost: reuse today's extracts in `_SOURCES\`, keep existing rows
- Hang safety: no command may wait for a key, stdin, a pager, or an unbounded child. Banned list and caps: see `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Robustness.md` (Playwright step 2-minute cap; URL checks with `Invoke-WebRequest -TimeoutSec 20 -MaximumRedirection 5` are allowed as a `.tmp_` script writing to a file). On a cap: kill the process tree, record command and cap in `PROBLEMS.md` of the working folder, continue. `browser_close` at the end
- Timestamps in all files come from this prompt's request metadata

Findings card: Load and update `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Findings.md`. File glitches, spec-code mismatches, and unexpected findings. Read at prompt startup for unresolved entries from prior prompts. Append one Partition Observations line for this prompt.

Closing: mark `P1-S6`, `P1-S7`, `P1-D3` `[x]` in `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__STRUT_MDLINVNTRY.md`; move both steps to Done in `PROGRESS.md`; add a Time Log line to the research STRUT.

Verify: Confirm `P1-S5` is `[x]` in `__STRUT_MDLINVNTRY.md`. `_SOURCES\` contains the two Google extracts. In `-04_SourcesPerField.md` the five fact-field sections each have four provider rows; the Google rows state the extraction method; the Sources file has no entry left with status "unchecked" and its header states "Preflight accuracy: N/M verified". The research STRUT has no assumption marked "pending web check". No `.tmp_` script remains in `_agent_work\`.

**STOP.** Report: items DONE / NOT DONE, URLs checked / redirected / dead, preflight accuracy.
```

---

## Verification Checkpoint 3

<!-- Verify prompts 5-6 (sources and field tables) before the options evaluation uses them. -->

```
02-MdlInv-Sources [ 03 / 07 ] - Verification checkpoint after prompts 5-6

Session: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate`
Working folder: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\T02_MDLINVNTRY_ReliableModelInventory_2026-10-28`

Read `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Robustness.md`, `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__STRUT_MDLINVNTRY.md`, and `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Findings.md`. Treat earlier conversation as compacted. Verification checkpoint after prompts 5-6.

/verify

current state against `__STRUT_MDLINVNTRY.md` steps P1-S4 to P1-S7 and deliverable P1-D3; `_INFO_MDLRGUP-MDLINVNTRY-02_Sources.md` against @skills:research-methods `RESEARCH_RULES.md` Sources Check (SC-*); `_INFO_MDLRGUP-MDLINVNTRY-04_SourcesPerField.md` against Topic Files Check (TF-*).

/fix

all gaps and remaining work. Max 2 gate cycles; on the second failure record the open items in `PROBLEMS.md` of the working folder and stop.

**STOP.** Report: verify findings fixed / open.
```

---

## Prompt 7 - Options for "work per prompt"

<!-- Expected state: audit (-03) and sources per field (-04) verified. This prompt evaluates how a planning parameter can be derived from sourced data and recommends one option. -->

```
02-MdlInv-Sources [ 04 / 07 ] - P1-S8 Evaluate options a-e for deriving work per prompt from sourced data

Session: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate`
Working folder: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\T02_MDLINVNTRY_ReliableModelInventory_2026-10-28`

Read `_INFO_MDLRGUP-MDLINVNTRY-03_InventoryAudit.md` (Summary, Counts), `_INFO_MDLRGUP-MDLINVNTRY-04_SourcesPerField.md`, `_agent_work\__STRUT_MDLRGUP-MDLINVNTRY.md` (Existing Tier Design), `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Findings.md` (Partition Observations), and `e:\dev\IPPS\.devin\skills\research-methods\RESEARCH_STRATEGY_MEPI.md` section Scoring Model. Treat earlier conversation as compacted. Step P1-S8.
Planning document: `__STRUT_MDLINVNTRY.md`, step P1-S8.

Objective: a decision-ready comparison of five ways to answer "how much work fits in one prompt for model X at effort Y", scored on five criteria, with one recommendation, so that `TASKS_GUIDES.md` and `PROMPTS_GUIDES.md` can keep one small method.

1. Read for evidence: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\T01_MDLBHVPRM_BehavioralParameterBenchmarks_2026-10-19\_INFO_MDLBHVPRM-06_ModelAwarePartitioning.md` Section 4; `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_INFO_HOW_TO_ORGANIZE_LLMS_BY_CAPABILITY.md` Sections 4, 9, 10; `e:\Dev\KarstensWorkspace\_Sessions\_!AINewsResearch\_PROMPTS_AI-News-Research_TEMPLATE.md` lines 55-62 (context management: prompt sizes GLM-5.2 runs in production)
2. Create `_INFO_MDLRGUP-MDLINVNTRY-05_WorkPerPromptOptions.md` (Doc ID `MDLRGUP-MDLINVNTRY-IN05`, first line `<PromptSystem MarkdownTablesAllowed=true />`). Define the scoring dimensions, 0-3 each: Sourced (values traceable to a published source), Coverage (share of the 28 models the method covers today, from -04), Tokens (lines the method needs in the inventory plus guides; fewer is better), General purpose (no dependency on one agent environment or on IPPS workflow names), Calibratable (observations can correct the values). Options: a) ECI band to HWH table (4-5 rows), b) METR 80% horizon where measured plus fallback, c) model-agnostic fixed limits (items per prompt, files per prompt, checkpoint interval) without a model-specific capacity number, d) keep the YY-L formula, e) Universal Class UC-1..5 to HWH table (reuses the existing tier record)
3. Write per option: What, Evidence for, Evidence against, Score - with inline citations `[LABEL] (SOURCE_ID | URL or file)`. Evidence must include: Epoch and METR coverage from -04; the AI News observation (GLM-5.2 high runs 10 prompts of about 1-2 HWH each with STOP gates) against the inventory WF 0.25; the Partition Observations lines collected so far in the findings card; the audit share of ASSUMED rows that each option removes
4. Write Comparison (one table), Recommendation ("do this", with the rationale and the values that stay [ASSUMED] and how observations calibrate them), and Limitations. Include a 3-line worked example of the recommended option for a 3 HWH task on `glm-5.2` high and `claude-opus-5` high

Constraints:
- All file operations MUST stay within the declared working folder unless an absolute path outside it is explicitly named in this prompt; the paths in item 1 are read-only
- Do ONLY the numbered items above. Do not refactor, rename, add tests, or touch files not listed. Report any item you could not complete as NOT DONE
- No new web research; use -04 and the files in item 1
- Scores need a one-line justification each; no option scores 3 on Sourced unless every value in it has a URL
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state or waste cost: keep an existing -05 and fill only missing options or sections
- Hang safety: no command may wait for a key, stdin, a pager, or an unbounded child. Banned list and caps: see `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Robustness.md`. On a cap: kill the process tree, record command and cap in `PROBLEMS.md` of the working folder, continue
- Timestamps in all files come from this prompt's request metadata

Findings card: Load and update `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Findings.md`. File glitches, spec-code mismatches, and unexpected findings. Read at prompt startup for unresolved entries from prior prompts. Append one Partition Observations line for this prompt.

Closing: mark `P1-S8`, `P1-D4` `[x]` in `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__STRUT_MDLINVNTRY.md`; move `P1-S8` to Done in `PROGRESS.md`; add a Time Log line to the research STRUT.

Verify: Confirm `P1-S7` is `[x]` in `__STRUT_MDLINVNTRY.md`. `-05_WorkPerPromptOptions.md` has five options a-e, each with What, Evidence for, Evidence against, Score with five dimension values; a Comparison table; a Recommendation naming exactly one option; a worked example with two models. Every evidence line carries a verification label and a source ID.

**STOP.** Report: items DONE / NOT DONE, scores per option, recommended option.
```

---

## Prompt 8 - Summary with synthesis and decision candidates

<!-- Expected state: -03, -04, -05 exist. This prompt creates the Summary (MEPI Phase 2 Step 1 and Phase 4) and closes the research STRUT. -->

```
02-MdlInv-Sources [ 05 / 07 ] - P1-S9 Write the Summary with cross-document synthesis and the decision candidates

Session: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate`
Working folder: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\T02_MDLINVNTRY_ReliableModelInventory_2026-10-28`

Read `_INFO_MDLRGUP-MDLINVNTRY-03_InventoryAudit.md`, `-04_SourcesPerField.md`, `-05_WorkPerPromptOptions.md`, `-02_Sources.md`, `_agent_work\__STRUT_MDLRGUP-MDLINVNTRY.md`, `e:\dev\IPPS\.devin\skills\research-methods\RESEARCH_CREATE_SUMMARY.md`, `e:\dev\IPPS\.devin\skills\research-methods\RESEARCH_SUMMARY_TEMPLATE.md`, `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__STRUT_MDLINVNTRY.md` (Plan P2 Strategy: DD-01 to DD-05), and `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Findings.md`. Treat earlier conversation as compacted. Step P1-S9.
Planning document: `__STRUT_MDLINVNTRY.md`, step P1-S9.

Objective: a reader of the Summary alone knows what is unreliable in the three files, which source answers which inventory field, which work-per-prompt method is recommended, and which five decisions remain for the user.

1. Copy `RESEARCH_SUMMARY_TEMPLATE.md` literally to `_INFO_MDLRGUP-MDLINVNTRY-01_Summary.md` (Doc ID `MDLRGUP-MDLINVNTRY-IN01`), then fill the header (Goal from the session STRUT, Timeline, Depends on -02 to -05), Research Question, Strategy & Domain (MEPI, DEFAULT, FOCUSED, with rationale), and the topic file index with working links
2. Write Key Findings as cross-document synthesis (8-12 bullets, each with a verification label and a source ID): audit shares per file, the load-bearing WF assumption, source per field with coverage, Google gap in `update-model-registry.md`, the recommended work-per-prompt option, the conflict between the YY-L scheme and the existing tier record, the Goal 2 and Goal 3 violations
3. Write the section "Decisions for [ACTOR]" with DD-01 to DD-05 from the session STRUT P2 Strategy in the Presenting Decisions format of `e:\dev\IPPS\.devin\rules\agent-behavior.md` (Problem, Context, Options with What / Why it works / Implication, exactly one recommendation per decision from -05 and -04 evidence, closing reply format `DD-01 a, DD-02 c, ...`); then Recommendation and Limitations
4. Add `**Research stats**: Xm net | Y docs | Z sources` to the header from the research STRUT Time Log; mark all research STRUT phases and the Time Log complete; set every Sources entry to a final status

Constraints:
- All file operations MUST stay within the declared working folder unless an absolute path outside it is explicitly named in this prompt
- Do ONLY the numbered items above. Do not refactor, rename, add tests, or touch files not listed. Report any item you could not complete as NOT DONE
- No new findings: every Summary claim traces to -03, -04, or -05
- Do not decide DD-01 to DD-05; recommend only
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state or waste cost: keep an existing Summary and fill only missing sections
- Hang safety: no command may wait for a key, stdin, a pager, or an unbounded child. Banned list and caps: see `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Robustness.md`. On a cap: kill the process tree, record command and cap in `PROBLEMS.md` of the working folder, continue
- Timestamps in all files come from this prompt's request metadata

Findings card: Load and update `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Findings.md`. File glitches, spec-code mismatches, and unexpected findings. Read at prompt startup for unresolved entries from prior prompts. Append one Partition Observations line for this prompt.

Closing: mark `P1-S9`, `P1-D5` `[x]` and the three P1 Objectives `[x]` in `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__STRUT_MDLINVNTRY.md`; move `P1-S9` to Done in `PROGRESS.md`.

Verify: Confirm `P1-S8` is `[x]` in `__STRUT_MDLINVNTRY.md`. `-01_Summary.md` has Research Question, Strategy & Domain, Key Findings (8-12 labeled bullets), "Decisions for [ACTOR]" with five decisions each carrying exactly one "(recommended ...)" option, Recommendation, Limitations, Research stats in the header; all topic file links resolve. The Sources file has no "unchecked" entry. The research STRUT shows all phases `[x]`.

**STOP.** Report: items DONE / NOT DONE, finding count, recommended option per DD.
```

---

## Verification Checkpoint 4

<!-- Final verification of the research set, then commit. -->

```
02-MdlInv-Sources [ 06 / 07 ] - Verification checkpoint after prompts 7-8: full research set

Session: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate`
Working folder: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\T02_MDLINVNTRY_ReliableModelInventory_2026-10-28`

Read `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Robustness.md`, `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__STRUT_MDLINVNTRY.md`, and `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Findings.md`. Treat earlier conversation as compacted. Verification checkpoint after prompts 7-8.

/verify

the working folder as a Deep Research Output set against @skills:research-methods `RESEARCH_RULES.md` (RS, SC, SM, TF, ST, QA) and `RESEARCH_SUMMARY_RULES.md`; and `__STRUT_MDLINVNTRY.md` P1 in the STRUT Transition context (all P1 deliverables checked, Objectives supported).

/fix

all gaps and remaining work. Max 2 gate cycles; on the second failure record the open items in `PROBLEMS.md` of the working folder and stop. Then commit: `git add` only files under `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\`, message `docs(model-inventory): T02 research set - audit, sources per field, work-per-prompt options, summary`, 2-minute cap.

**STOP.** Report: rule families passed / fixed / open, commit hash.
```

---

## Verification Checkpoint 5 - Critique

<!-- One heavy workflow alone (guarded profile). Critique output stays beside the documents; prompt 9 in `_PROMPTS_03-MdlInv-Template.md` reads it before presenting the decisions. No `/reconcile` here. -->

```
02-MdlInv-Sources [ 07 / 07 ] - Critique of the Summary and the options file before decisions are presented

Session: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate`
Working folder: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\T02_MDLINVNTRY_ReliableModelInventory_2026-10-28`

Read `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Robustness.md` and `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__STRUT_MDLINVNTRY.md` (Known Knowns, Plan P2). Treat earlier conversation as compacted. Quality gate after prompt 8, before STRUT P2.

/critique

`_INFO_MDLRGUP-MDLINVNTRY-01_Summary.md` and `_INFO_MDLRGUP-MDLINVNTRY-05_WorkPerPromptOptions.md`. Focus: flawed assumptions behind each option score, circular evidence (values justified by the table they replace), hidden dependencies on one agent environment, and whether the recommended option is the least complex one that still answers "how many prompts". Write the critique files beside the documents; do not modify the documents.

**STOP.** Report: findings per severity, the three findings most relevant to DD-01 and DD-02.
```
