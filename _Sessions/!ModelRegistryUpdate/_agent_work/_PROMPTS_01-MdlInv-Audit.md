---
intended_model: glm-5.2
context_window_size: 1M
effort: high
prompt_system: IPPS
---

<!-- Budget (PROMPTS_GUIDES.md Section 1g): model row glm-5.2, label 26-D, profile guarded (max_items 4, max_files 2, checkpoint_interval 1, scope_guard strict), effort high, WF 0.25 HWH, task 6.75 HWH for the whole STRUT (this file: P1-S1..S3 = 1.75 HWH), estimated cost $13.50 (whole STRUT).
Computed by the Section 1g formula: 27 implementation prompts for the STRUT (capacity-driven), 7 for this file. Chosen: 12 implementation prompts in 3 sub-chain files (4 in this file), checkpoints every 2 prompts.
Deviation stated on purpose: the WF values and profile parameters of MODEL_INVENTORY.md are the subject under review (STRUT "Known Knowns"); a 54-prompt sequence to execute a 1 AWH plan would itself violate Goal 3. Kept from the guarded profile: max_items 4 per prompt, strict scope guard, max_files 2 for deliverables (tracking files, cards, and the STRUT checkbox are exempt). Every prompt reports items DONE / NOT DONE and one partition-observation line in the findings card; STRUT step P1-S8 uses these observations as empirical input.
Sub-chains: 01 Audit (P1-S1..S3), 02 Sources (P1-S4..S9), 03 Template (P2, P3, P4). Workflow load (PRMT-SC-07): checkpoints carry one `/verify` + `/fix` each; the research strategy phases are executed step by step from RESEARCH_STRATEGY_MEPI.md instead of one `/deep-research` call, so no prompt runs more than one heavy workflow.
Planning document: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__STRUT_MDLINVNTRY.md`. Cards: `__CARD_MDLINVNTRY-Findings.md`, `__CARD_MDLINVNTRY-Robustness.md` in the same folder. -->

## Prompt 1 - Create the T02 research folder

```
01-MdlInv-Audit [ 01 / 06 ] - P1-S1 Create T02 folder with NOTES.md and PROGRESS.md

Session: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate`
Working folder: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\T02_MDLINVNTRY_ReliableModelInventory_2026-10-28`

Read `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__STRUT_MDLINVNTRY.md` (MUST-NOT-FORGET, Known Knowns, Plan P1), `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\NOTES.md` (Current Phase, Topic Registry), and `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Findings.md`. Treat earlier conversation as compacted. Step P1-S1 (part 1 of 2).
Planning document: `__STRUT_MDLINVNTRY.md`, step P1-S1.

Objective: the deep-research output folder exists with its two first tracking files, so that later prompts have a working folder, a progress record, and the research instructions in one place. Templates: @skills:session-management `NOTES_TEMPLATE.md`, `PROGRESS_TEMPLATE.md`; folder rules: @skills:research-methods SKILL.md "Output Folder".

1. Create the working folder and its `_agent_work\` subfolder if missing
2. Create `NOTES.md` (Doc ID `MDLRGUP-MDLINVNTRY-NOTES`): MUST-NOT-FORGET copied from the STRUT MUST-NOT-FORGET (all items), Initial Request = the prompt text recorded in the session NOTES.md Significant Prompts Log entry of 2026-10-28 18:45 (copy verbatim), Session Info (Started 2026-10-28, Goal from the STRUT Goal line, Operation Mode IMPL-ISOLATED, Output Location this folder), Agent Instructions (strategy MEPI, scope FOCUSED, domain DEFAULT, dimensions technical and practical; Playwright for every web page; Epoch ECI from epoch.ai only; no Artificial Analysis, LMArena, or gap-to-frontier values), Topic Registry (global `MDLRGUP`, subtopic `MDLINVNTRY`, nested IDs `MDLRGUP-MDLINVNTRY-*`)
3. Create `PROGRESS.md` (Doc ID `MDLRGUP-MDLINVNTRY-PROGRESS`): To Do = STRUT steps P1-S2 to P1-S9 one line each, In Progress empty, Done = `P1-S1 part 1: T02 folder, NOTES.md, PROGRESS.md` with timestamp
4. Mark nothing in the STRUT yet (P1-S1 completes in prompt 2); report

Constraints:
- All file operations MUST stay within the declared working folder unless an absolute path outside it is explicitly named in this prompt
- Do ONLY the numbered items above. Do not refactor, rename, add tests, or touch files not listed. Report any item you could not complete as NOT DONE
- Do not create PROBLEMS.md or a STRUT in this prompt (prompt 2 does)
- Do not edit the session root NOTES.md
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state or waste cost: if a file exists with its required sections, keep it and fill only missing sections
- Hang safety: no command may wait for a key, stdin, a pager, or an unbounded child. Banned list and caps: see `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Robustness.md`. On a cap: kill the process tree, record command and cap in the working folder's PROBLEMS.md (create it only if a cap occurs), continue
- Timestamps in all files come from this prompt's request metadata

Findings card: Load and update `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Findings.md`. File glitches, spec-code mismatches, and unexpected findings. Read at prompt startup for unresolved entries from prior prompts. Append one Partition Observations line for this prompt.

Verify: the working folder contains `_agent_work\`, `NOTES.md` with the sections MUST-NOT-FORGET, Initial Request, Session Info, Agent Instructions, Topic Registry, and `PROGRESS.md` with To Do, In Progress, Done. The Initial Request fence contains the text "Goals:" and "/write-strut for 1 AWH".

**STOP.** Report: items DONE / NOT DONE, files created with absolute paths.
```

---

## Prompt 2 - Research STRUT with prompt decomposition

<!-- Expected state: T02 folder with NOTES.md and PROGRESS.md. This prompt adds PROBLEMS.md and the research STRUT (MEPI Phase 1 Step 1-2). -->

```
01-MdlInv-Audit [ 02 / 06 ] - P1-S1 Create PROBLEMS.md and the research STRUT with decomposition and assumptions

Session: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate`
Working folder: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\T02_MDLINVNTRY_ReliableModelInventory_2026-10-28`

Read `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__STRUT_MDLINVNTRY.md` (Plan P1, Known Knowns), `NOTES.md` in the working folder, `e:\dev\IPPS\.devin\skills\research-methods\SKILL.md` (7 decomposition questions, phase model), `e:\dev\IPPS\.devin\skills\research-methods\RESEARCH_STRATEGY_MEPI.md` (Phase 1 Steps 1-2), `e:\dev\IPPS\.devin\skills\write-documents\STRUT_TEMPLATE.md`, and `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Findings.md`. Treat earlier conversation as compacted. Step P1-S1 (part 2 of 2).
Planning document: `__STRUT_MDLINVNTRY.md`, step P1-S1.

Objective: the research has its own STRUT with the MEPI prompt decomposition, pre-research assumptions, and a phase plan, plus an empty PROBLEMS.md, so that MEPI Phase 1 Steps 1-2 are complete. Model for the STRUT shape: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\T01_MDLBHVPRM_BehavioralParameterBenchmarks_2026-10-19\__STRUT_MDLBHVPRM.md` (read it).

1. Create `PROBLEMS.md` (Doc ID `MDLRGUP-MDLINVNTRY-PROBLEMS`, ID format `MDLRGUP-MDLINVNTRY-PR-[NNNN]`, sections Open, Resolved, Deferred, Problems Changes) from @skills:session-management `PROBLEMS_TEMPLATE.md`
2. Create `_agent_work\__STRUT_MDLRGUP-MDLINVNTRY.md` (Doc ID `MDLRGUP-MDLINVNTRY-RSTRUT`) with the Prompt Decomposition JSON answering the 7 questions: goal (from the session STRUT P1 Objectives), scope FOCUSED, dimensions technical (sources, extraction methods) and practical (planning use, token cost), strategy MEPI with rationale (reversible, time-constrained, action-oriented), domain DEFAULT with rationale, effort estimate 2.5 HWH, discovery platforms (epoch.ai/eci, metr.org/time-horizons, provider documentation pages listed in `e:\dev\IPPS\update-model-registry.md` Sources section, ai.google.dev, Google search for URL discovery)
3. Add "Pre-Research Assumptions" (6-8 items, each `[ASSUMED]`) covering at least: Epoch ECI covers most of the 28 inventory models; METR publishes per-model 50% and 80% horizons; Google publishes an API pricing table comparable to OpenAI's; the 9 provider URLs in `update-model-registry.md` still resolve; the AI News pipeline runs GLM-5.2 at high effort on prompts of about 1-2 HWH without skipped items (contradicts WF 0.25); no public benchmark reports work completed per prompt in human hours
4. Add the Phase Plan (Phase 1 Preflight = prompts 1-3 of sub-chain 01 and the Checkpoint; Phase 2 Planning folded into prompt 8 Summary skeleton; Phase 3 Research = prompts 4-7; Phase 4 Final = prompt 8 and checkpoints 4-5) with Objective, Deliverables, Transition per phase, and a Time Log list with one line per prompt

Constraints:
- All file operations MUST stay within the declared working folder unless an absolute path outside it is explicitly named in this prompt
- Do ONLY the numbered items above. Do not refactor, rename, add tests, or touch files not listed. Report any item you could not complete as NOT DONE
- Do not start source collection or web research in this prompt
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state or waste cost: existing files with the required sections are kept; only missing sections are added
- Hang safety: no command may wait for a key, stdin, a pager, or an unbounded child. Banned list and caps: see `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Robustness.md`. On a cap: kill the process tree, record command and cap in `PROBLEMS.md` of the working folder, continue
- Timestamps in all files come from this prompt's request metadata

Findings card: Load and update `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Findings.md`. File glitches, spec-code mismatches, and unexpected findings. Read at prompt startup for unresolved entries from prior prompts. Append one Partition Observations line for this prompt.

Closing: mark `P1-S1` and deliverable `P1-D1` `[x]` in `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__STRUT_MDLINVNTRY.md`; move `P1-S1` to Done in `PROGRESS.md`.

Verify: `PROBLEMS.md` exists with the four sections. `_agent_work\__STRUT_MDLRGUP-MDLINVNTRY.md` contains a JSON block with keys goal, scope, dimensions, strategy, domain, effort_estimate, discovery_platforms; a "Pre-Research Assumptions" list with 6-8 `[ASSUMED]` items; a Phase Plan with 4 phases; a Time Log. `__STRUT_MDLINVNTRY.md` shows `[x] P1-S1` and `[x] P1-D1`.

**STOP.** Report: items DONE / NOT DONE, assumption count, files created.
```

---

## Verification Checkpoint 1

<!-- Verify prompts 1-2 against the STRUT before source collection starts. -->

```
01-MdlInv-Audit [ 03 / 06 ] - Verification checkpoint after prompts 1-2

Session: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate`
Working folder: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\T02_MDLINVNTRY_ReliableModelInventory_2026-10-28`

Read `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Robustness.md`, `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__STRUT_MDLINVNTRY.md`, and `_agent_work\__STRUT_MDLRGUP-MDLINVNTRY.md` in the working folder. Treat earlier conversation as compacted. Verification checkpoint after prompts 1-2.

/verify

current state against `__STRUT_MDLINVNTRY.md` step P1-S1 and deliverable P1-D1, and the research STRUT `_agent_work\__STRUT_MDLRGUP-MDLINVNTRY.md` in the STRUT Planning context (Objectives linked to Deliverables, AGEN verbs, Transitions reference Deliverables).

/fix

all gaps and remaining work. Max 2 gate cycles; on the second failure record the open items in `PROBLEMS.md` of the working folder and stop.

**STOP.** Report: verify findings fixed / open.
```

---

## Prompt 3 - Prior tier design and source registry

<!-- Expected state: research STRUT with assumptions exists. This prompt reads the user's existing tier design and creates the Sources file (MEPI Phase 1 Steps 3-4, local and known sources; web discovery follows in sub-chain 02). -->

```
01-MdlInv-Audit [ 04 / 06 ] - P1-S2 Read the existing model tier design and create the Sources file

Session: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate`
Working folder: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\T02_MDLINVNTRY_ReliableModelInventory_2026-10-28`

Read `_agent_work\__STRUT_MDLRGUP-MDLINVNTRY.md` (assumptions), `NOTES.md` in the working folder, `e:\dev\IPPS\.devin\skills\research-methods\RESEARCH_STRATEGY_MEPI.md` Phase 1 Steps 3-4, and `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Findings.md`. Treat earlier conversation as compacted. Step P1-S2.
Planning document: `__STRUT_MDLINVNTRY.md`, step P1-S2.

Objective: the research starts from the tier design that already exists instead of inventing one, and every local and known source has an ID in the Sources file.

1. Read `e:\Dev\KarstensWorkspace\_Sessions\_!AINewsResearch\NOTES.md` section "Model and Hardware Tiers" and `e:\Dev\KarstensWorkspace\_Sessions\_!AINewsResearch\_INFO_AINWSRCH-MODELTIER-01_GenerationTiering.md`. Extract into a section "Existing Tier Design" of the research STRUT: the 4 fields of the model tier record with their definitions, the rule "no tier field may depend on which models are newest", the rejected sources with reasons (Artificial Analysis, LMArena, gap to frontier), and the source evaluation that led to Epoch ECI
2. Create `_INFO_MDLRGUP-MDLINVNTRY-02_Sources.md` (Doc ID `MDLRGUP-MDLINVNTRY-IN02`): header with version scope `2026-10-28`, "Preflight accuracy: pending"; sections Local Sources, Provider Documentation, Capability Evidence, Agent Environments. Register with IDs `MDLRGUP-MDLINVNTRY-SC-[SOURCE]-[DOCREF]`: `e:\dev\IPPS\PromptSystemV4.5\skills\write-documents\MODEL_INVENTORY.md`, `TASKS_GUIDES.md`, `PROMPTS_GUIDES.md`, `PROMPTS_RULES.md` (PRMT-SC-05), `e:\dev\IPPS\PromptSystemV4.5\skills\llm-evaluation\model-registry.json`, `model-pricing.json`, `e:\dev\IPPS\PromptSystemV4.5\skills\devin-auto-model-switcher\windsurf-model-registry.json`, `e:\dev\IPPS\update-model-registry.md` (Sources section URLs A1-A4, O1-O3, Z1-Z3 as Provider Documentation entries with status "unchecked"), `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_INFO_HOW_TO_ORGANIZE_LLMS_BY_CAPABILITY.md`, the two AINWSRCH files from item 1, `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\T01_MDLBHVPRM_BehavioralParameterBenchmarks_2026-10-19\_INFO_MDLBHVPRM-06_ModelAwarePartitioning.md` and `-07_PromptFeedbackLoop.md`, and `e:\Dev\KarstensWorkspace\_Sessions\_!AINewsResearch\_PROMPTS_AI-News-Research_TEMPLATE.md` (Context management section as evidence of GLM-5.2 prompt sizes in use)
3. Add the planned web sources to Capability Evidence and Provider Documentation with status "unchecked": `https://epoch.ai/eci`, `https://metr.org/time-horizons/`, `https://ai.google.dev/gemini-api/docs/pricing`, `https://ai.google.dev/gemini-api/docs/models`
4. Verify the assumptions in the research STRUT against the local sources read in items 1-2 (rubric CORRECT / PARTIAL / WRONG per MEPI Step 4); strike through wrong ones with the correction; leave web-dependent assumptions "pending web check"

Constraints:
- All file operations MUST stay within the declared working folder unless an absolute path outside it is explicitly named in this prompt; the paths in items 1-2 are read-only
- Do ONLY the numbered items above. Do not refactor, rename, add tests, or touch files not listed. Report any item you could not complete as NOT DONE
- No web navigation in this prompt
- Do not evaluate or rank the tier designs here; record what exists
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state or waste cost: reuse existing source IDs, add only missing entries
- Hang safety: no command may wait for a key, stdin, a pager, or an unbounded child. Banned list and caps: see `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Robustness.md`. On a cap: kill the process tree, record command and cap in `PROBLEMS.md` of the working folder, continue
- Timestamps in all files come from this prompt's request metadata

Findings card: Load and update `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Findings.md`. File glitches, spec-code mismatches, and unexpected findings. Read at prompt startup for unresolved entries from prior prompts. Append one Partition Observations line for this prompt.

Closing: mark `P1-S2` `[x]` in `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__STRUT_MDLINVNTRY.md`; move `P1-S2` to Done in `PROGRESS.md`.

Verify: Confirm `P1-S1` is `[x]` in `__STRUT_MDLINVNTRY.md`. The research STRUT has a section "Existing Tier Design" naming UC-1 to UC-5, ECI band, generation equivalent, and three rejected sources. `_INFO_MDLRGUP-MDLINVNTRY-02_Sources.md` has at least 18 entries, each with an ID and a path or URL; web entries carry status "unchecked". Every assumption line in the research STRUT carries CORRECT, PARTIAL, WRONG, or "pending web check".

**STOP.** Report: items DONE / NOT DONE, source count, assumptions verified / pending.
```

---

## Prompt 4 - Line-by-line audit of the three files

<!-- Expected state: Sources file and tier design summary exist. This is the heaviest reasoning prompt of the sub-chain: classify every value and rule. -->

```
01-MdlInv-Audit [ 05 / 06 ] - P1-S3 Classify every value and rule in the three files as SOURCED, DERIVED, or ASSUMED

Session: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate`
Working folder: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\T02_MDLINVNTRY_ReliableModelInventory_2026-10-28`

Read `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__STRUT_MDLINVNTRY.md` section "Known Knowns", `_INFO_MDLRGUP-MDLINVNTRY-02_Sources.md`, and `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Findings.md`. Treat earlier conversation as compacted. Step P1-S3.
Planning document: `__STRUT_MDLINVNTRY.md`, step P1-S3.

Objective: a reader sees, per line of `MODEL_INVENTORY.md`, `TASKS_GUIDES.md`, `PROMPTS_GUIDES.md` Sections 1c, 1f, 1g, 3a, 5, and `PROMPTS_RULES.md` PRMT-SC-05, whether a value or rule is SOURCED (a cited provider document, benchmark, or paper states it), DERIVED (computed from SOURCED values by a stated formula), or ASSUMED (no source, judgment, or fitted to reproduce an earlier table), and how much of each file that is.

1. Read the four files at `e:\dev\IPPS\PromptSystemV4.5\skills\write-documents\` (`PROMPTS_RULES.md` lines 1349-1361 only). For `PROMPTS_GUIDES.md` read Sections 1c, 1f, 1g, 3a, 5 only
2. Create `_INFO_MDLRGUP-MDLINVNTRY-03_InventoryAudit.md` (Doc ID `MDLRGUP-MDLINVNTRY-IN03`, first line `<PromptSystem MarkdownTablesAllowed=true />`) with one table per file: columns File | Lines | Item (value, rule, or claim in 10 words or fewer) | Class | Evidence or reason. One row per numeric value, formula, rule (R1-R5, thresholds, parameters, multipliers), and per table column of `MODEL_INVENTORY.md` Section 3. Reason for ASSUMED rows names the missing evidence (for example "no source; LLMCAPCLS-IN01 Section 6: fitted to prior table")
3. Add a section "Counts" with per file: rows SOURCED / DERIVED / ASSUMED, line count, and word count (count with a `.tmp_` script writing to a file in `_agent_work\`, then delete the script); and a section "Goal Violations" listing per file the items that depend on one agent environment (Goal 2: Devin cost, Devin-only rows, Cascade names) and the items that exist only to maintain other rules or duplicate another section (Goal 3: October rule, profile change rule, overlapping partitioning sections 1c, 1f, 1g, 5)
4. Add a Summary (5 bullets) at the top: share of ASSUMED rows per file, the single most load-bearing assumption (the WF formula), what would remain if ASSUMED rows were removed

Constraints:
- All file operations MUST stay within the declared working folder unless an absolute path outside it is explicitly named in this prompt; the files under `e:\dev\IPPS\PromptSystemV4.5\` are read-only
- Do ONLY the numbered items above. Do not refactor, rename, add tests, or touch files not listed. Report any item you could not complete as NOT DONE
- Classify, do not fix: no proposals or alternatives in this file
- HWH size buckets (TASKS_GUIDES.md Section 2) are ASSUMED but marked "keep" in the reason column per the STRUT Known Knowns
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state or waste cost: if the audit file exists with all four file tables and the Counts section, keep it and fill only missing rows
- Hang safety: no command may wait for a key, stdin, a pager, or an unbounded child. Banned list and caps: see `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Robustness.md`. Word count script: 1-minute cap. On a cap: kill the process tree, record command and cap in `PROBLEMS.md` of the working folder, continue
- Timestamps in all files come from this prompt's request metadata

Findings card: Load and update `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Findings.md`. File glitches, spec-code mismatches, and unexpected findings. Read at prompt startup for unresolved entries from prior prompts. Append one Partition Observations line for this prompt.

Closing: mark `P1-S3` and `P1-D2` `[x]` in `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__STRUT_MDLINVNTRY.md`; move `P1-S3` to Done in `PROGRESS.md`.

Verify: Confirm `P1-S2` is `[x]` in `__STRUT_MDLINVNTRY.md`. `_INFO_MDLRGUP-MDLINVNTRY-03_InventoryAudit.md` has four tables (MODEL_INVENTORY.md, TASKS_GUIDES.md, PROMPTS_GUIDES.md, PROMPTS_RULES.md), every row has a Class of SOURCED, DERIVED, or ASSUMED, the Counts section lists all four files with word counts, Goal Violations has entries for Goal 2 and Goal 3. No `.tmp_` script remains in `_agent_work\`.

**STOP.** Report: items DONE / NOT DONE, rows per class per file.
```

---

## Verification Checkpoint 2

<!-- Final checkpoint of sub-chain 01. Sub-chain 02 (`_PROMPTS_02-MdlInv-Sources.md`) continues with web sources. -->

```
01-MdlInv-Audit [ 06 / 06 ] - Verification checkpoint after prompts 3-4

Session: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate`
Working folder: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\T02_MDLINVNTRY_ReliableModelInventory_2026-10-28`

Read `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Robustness.md`, `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__STRUT_MDLINVNTRY.md`, and `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__CARD_MDLINVNTRY-Findings.md`. Treat earlier conversation as compacted. Verification checkpoint after prompts 3-4.

/verify

current state against `__STRUT_MDLINVNTRY.md` steps P1-S1 to P1-S3 and deliverables P1-D1, P1-D2; `_INFO_MDLRGUP-MDLINVNTRY-02_Sources.md` against @skills:research-methods `RESEARCH_RULES.md` Sources Check (SC-*); `_INFO_MDLRGUP-MDLINVNTRY-03_InventoryAudit.md` against INFO document rules (header block, Doc ID, Document History).

/fix

all gaps and remaining work. Max 2 gate cycles; on the second failure record the open items in `PROBLEMS.md` of the working folder and stop. Then commit the session folder: `git add` only files under `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\`, message `docs(model-inventory): T02 preflight and inventory audit`, 2-minute cap.

**STOP.** Report: verify findings fixed / open, commit hash.
```
