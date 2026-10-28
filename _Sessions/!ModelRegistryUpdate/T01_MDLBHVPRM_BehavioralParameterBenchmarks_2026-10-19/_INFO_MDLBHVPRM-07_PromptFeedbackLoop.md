# INFO: Prompt Sequence Feedback Loop and _agent_work Folder

**Doc ID**: MDLRGUP-MDLBHVPRM-IN07
**Goal**: Define how every `_PROMPTS_` file ends with a drift-detection checkpoint whose per-prompt planned-vs-actual observations flow into model tiers, and define the `_agent_work/` folder that holds all cleanable agent artifacts
**Timeline**: Created 2026-10-19, Updated 2 times (2026-10-19 - 2026-10-19)
**Target file**: `write-prompts.md`, `drift-detect.md`, `drift-correct.md`, `session-finalize.md`, `cleanup.md`, `write-strut.md`, `PROMPTS_GUIDES.md`, `PROMPTS_RULES.md`, `DRIFTS_TEMPLATE.md`, `agent-behavior.md` (File Placement), `model-registry.json`, new `aggregate-partition-observations.py`

**Depends on:**
- `_INFO_MDLBHVPRM-06_ModelAwarePartitioning.md [MDLRGUP-MDLBHVPRM-IN06]` for tiers A/B/C and the partition parameters (max_items, max_files, checkpoint_interval, scope_guard)
- Decision MDLBHVPRM-DD-01 = Option 2 (tiers), PRMTFDBK-DD-01 = Option 2 (structured ledger + script)

## Summary

- **One new folder**: `[SESSION_FOLDER]/_agent_work/` (or `T##_*/_agent_work/`) holds everything an agent creates to do work and that can be deleted without losing output: `_PROMPTS_*`, `__STRUT_*`, `__TASKS_*`, `__CARD_*`, `__DRIFT_*`, `DRIFTS.md`, `.tmp_*`, the observation ledger. Review outputs (`*_CRITIQUE.md`, `*_FACT-CHECK.md`, `_vN` backups, `*_DEFERRED_IMPROVEMENTS.md`) stay beside the document they review. `/cleanup` gets one new category: the folder. [VERIFIED - user decision 2026-10-19]
- **Planned side needs no extra artifact**: the prompts file is the plan. Numbered items, listed files, and frontmatter `tier` are countable by the detector. [VERIFIED - PROMPTS_GUIDES Section 3]
- **Actual side = a mandatory Final Checkpoint prompt** appended by `/write-prompts`: runs `/drift-detect log sequence` (DoD from the prompts file + STRUT, third status `EXTRA` for unrequested work, one JSON line per prompt appended to `_agent_work/partition-observations.jsonl`) then `/drift-correct`. Exempt from chain length like verification checkpoints. [VERIFIED - drift-detect.md, PRMT-SC-04]
- **Weak-auditor fix**: the Final Checkpoint carries `<!-- model: high -->` commentary; the execution engine switches model via `@skills:devin-auto-model-switcher` before running it, so a tier-C model does not grade its own work. [ASSUMED - engine support]
- **Ledger stays in the session**, never in `[PROMPTSYSTEM_FOLDER]` or `[AGENT_FOLDER]`. `/session-finalize` runs `aggregate-partition-observations.py` which merges sums (not means) into `model-registry.json` `observed` and renames the ledger to `*.ingested.jsonl`. `/cleanup` deletes `_agent_work/` but refuses while an un-ingested `.jsonl` exists. [VERIFIED - design, see Section 6]
- **Registry gets 3 properties total**: `tier` (A/B/C, human-set), `tier_note` (provenance, only when deviating from benchmark seed), `observed` (object with sums, derived IF/EG, `tier_suggested`). The script never changes `tier`; `update-model-registry.md` gains a review step. [VERIFIED - design]

## Table of Contents

1. [Problem and Goal](#1-problem-and-goal)
2. [The _agent_work Folder](#2-the-_agent_work-folder)
3. [Data Flow Overview](#3-data-flow-overview)
4. [Planned Side: /write-prompts Changes](#4-planned-side-write-prompts-changes)
5. [Actual Side: /drift-detect Sequence Mode](#5-actual-side-drift-detect-sequence-mode)
6. [Observation Ledger](#6-observation-ledger)
7. [Aggregation into the Registry](#7-aggregation-into-the-registry)
8. [Implementation Map](#8-implementation-map)
9. [Risks and Open Points](#9-risks-and-open-points)

## 1. Problem and Goal

Tiers (IN06) are assigned from benchmarks that measure the wrong thing (IFEval) and from anecdote (GLM-5.2 skips). No mechanism records what a model actually skipped or over-did in a real sequence. Goal: every prompt sequence produces per-prompt observations attributed to `intended_model`, and the observations update `model-registry.json` with evidence so tiers are corrected by data instead of memory.

Second goal from the same decision: stop scattering agent artifacts across the session root. One folder, one cleanup rule.

## 2. The `_agent_work` Folder

```
[SESSION_FOLDER]/
├─ NOTES.md, PROGRESS.md, PROBLEMS.md, FAILS.md   tracking - never in _agent_work
├─ _INFO_*, _SPEC_*, _IMPL_*, _TEST_*            deliverables
├─ _INFO_X_CRITIQUE.md, _INFO_X_FACT-CHECK.md    review output - beside reviewed doc
├─ _INFO_X_v1.md, *_DEFERRED_IMPROVEMENTS.md      improve output - beside improved doc
├─ _agent_work/                                   everything cleanable
│   ├─ _PROMPTS_01-Topic.md                        written by /write-prompts
│   ├─ __STRUT_TOPIC.md, __TASKS_TOPIC.md          planning scaffolding
│   ├─ __CARD_TOPIC-Findings.md, -Robustness.md    prompt cards
│   ├─ __DRIFT_TOPIC.md, DRIFTS.md                 drift control
│   ├─ partition-observations.jsonl                 ledger (Section 6)
│   └─ .tmp_*                                      temp scripts and data
└─ T01_SUB_Topic_YYYY-MM-DD/
    ├─ (same layout)
    └─ _agent_work/
```

Rules:
- **In**: any file an agent creates to organize or execute work whose loss does not lose output: prompts files, STRUT/TASKS scaffolding, cards, drift files, ledgers, `.tmp_*`
- **Out**: tracking documents (session state), deliverables, and review/improve outputs (`*_CRITIQUE.md`, `*_FACT-CHECK.md`, `_vN` backups, `*_DEFERRED_IMPROVEMENTS.md`). These belong to a document, not to agent operation, and `/cleanup review` already manages them per document [VERIFIED - cleanup.md Categories 3, 5]
- **Scope**: one `_agent_work/` per working folder (session root or `T##_*`/`S##_*` subfolder). In PROJECT-MODE: `[WORKSPACE_FOLDER]/_agent_work/`. The Session Anchor's `Working folder:` line (PRMT-SC-08) resolves it: `[Working folder]/_agent_work/`
- **Cleanup**: `/cleanup` Category 7 "Agent work folder" deletes `_agent_work/` recursively in scope, guarded by Section 6 ingestion rule. Categories 1 and 6 keep matching stray files outside the folder during transition
- **Archive**: `/session-archive` runs after `/cleanup`; an archived session has no `_agent_work/` unless the user kept it deliberately

Why a folder instead of more prefixes: `__` and `.tmp_` prefixes already exist and still leak (`DRIFTS.md`, `_PROMPTS_*` have neither). A folder is one glob for `/cleanup`, one `Working folder` derivation for prompts, and visually separates process from product in the IDE. [VERIFIED - cleanup.md Section 6 lists three legacy pattern families]

## 3. Data Flow Overview

```
/write-prompts                    execution engine                     /session-finalize
──────────────                    ────────────────                     ─────────────────
reads tier from registry   ──>   runs prompts 1..N                    runs aggregate script
writes _agent_work/               (intended_model, effort)             reads _agent_work/*.jsonl
  _PROMPTS_NN-Topic.md                 │                               merges sums into
  frontmatter: tier                    v                                 registry.observed
  numbered items per prompt       Final Checkpoint (model: high)        renames ledger
  Final Checkpoint prompt           /drift-detect log sequence            *.ingested.jsonl
                                      DoD from prompts file + STRUT             │
                                      PASS / FAIL / MISSED / EXTRA              v
                                      __DRIFT_, DRIFTS.md                  /update-model-registry
                                      ledger: 1 JSON line per prompt       review tier_suggested
                                    /drift-correct                         set tier, tier_note
```

Planned values are read from the prompts file; actual values are read from the output tree. Nothing is carried in model memory (PRMT-SC-02).

## 4. Planned Side: `/write-prompts` Changes

- **Location** (Step 2): always `[Working folder]/_agent_work/_PROMPTS_[NN]-[Topic].md`. Create the folder if missing. Cards and robustness card go to the same folder. [NN] uniqueness is evaluated across all `_agent_work/` folders of the session
- **Frontmatter** (PRMT-SC-05 extended): add `tier: A|B|C` resolved from `model-registry.json` by `intended_model`; unknown model = `C`. State the derived parameters in the opening commentary: `<!-- tier C: max_items 4, max_files 2, checkpoint every 1, scope_guard strict -->`
- **Countable items**: every implementation prompt lists its work as numbered items (`1.`, `2.`, ...) and names target files explicitly. This is what the detector counts as `items_planned` and `files_planned`. Guides Section 3 already asks for objective + constraints; the numbering is the only addition
- **Final Checkpoint prompt** (new PRMT-SQ-05): mandatory last prompt of every file, heading `## Final Checkpoint`, exempt from chain length (same as PRMT-SQ-04 checkpoints). Template:

```
[NN]-[Topic] [ NN / NN ] - Final checkpoint: drift detection and correction

Session: `[ABSOLUTE_SESSION_FOLDER_PATH]`
Working folder: `[ABSOLUTE_WORKING_FOLDER_PATH]`

Read `_agent_work/_PROMPTS_[NN]-[Topic].md` and `_agent_work/__STRUT_[TOPIC].md`. Treat earlier conversation as compacted. Final checkpoint for prompts 1-[N-1].

/drift-detect log sequence

against `_agent_work/_PROMPTS_[NN]-[Topic].md` for prompts 1-[N-1]. Ledger: `_agent_work/partition-observations.jsonl`.

/drift-correct

all FAIL items.
```

Commentary before the fence: `<!-- model: high - auditor must not be the audited model -->`. The execution engine reads this hint and switches via `@skills:devin-auto-model-switcher`; if it cannot, it runs on `intended_model` and the ledger line records `auditor_model` so reviewers can discount self-audited observations (Section 7 reports `self_audited_prompts` count; no automatic down-weighting). [ASSUMED - engine support, to be confirmed with Lana]

## 5. Actual Side: `/drift-detect` Sequence Mode

New directive `sequence` (`/drift-detect log sequence against [prompts file]`):

- **Context**: "Prompt Sequence" added to `DRIFT_DETECTION.md` Context Detection. Sources: the prompts file (per-prompt numbered items, named files, Verify lines), the STRUT (deliverables), the findings card (resolved/unresolved glitches)
- **DoD extraction**: one DoD item per numbered item per prompt, tagged with `prompt_no`. Files named in a prompt become `files_planned[prompt_no]`
- **Assessment**: PASS / FAIL / MISSED as today, plus **EXTRA** - a change in the output tree (git diff of the working folder since sequence start, or file timestamps) that no DoD item of any prompt requested. EXTRA is the eagerness observation; it is recorded but never "corrected" by `/drift-correct` (reverting unrequested work is a human decision, filed in PROBLEMS.md)
- **Per-prompt roll-up** written to `__DRIFT_[TOPIC].md` and `DRIFTS.md` (DRIFTS_TEMPLATE gets a `### Partition` block with model attribution), and one JSON line per prompt appended to the ledger (Section 6)
- **Location**: `__DRIFT_*` and `DRIFTS.md` go to `_agent_work/`; Mandatory Re-read list unchanged

## 6. Observation Ledger

File: `[Working folder]/_agent_work/partition-observations.jsonl`. One line per executed implementation prompt (checkpoints excluded).

```json
{"date":"2026-10-19","session":"_2026-10-19_ExampleTopic","prompts_file":"_PROMPTS_01-Ex-Impl.md","prompt_no":2,
 "model_id":"glm-5.2","effort":"high","tier_planned":"C","auditor_model":"claude-opus-4-6","engine":"cascade",
 "items_planned":4,"items_done":3,"items_skipped":1,"extra_actions":2,
 "files_planned":2,"files_touched":4,"fixes_applied":1}
```

Lifecycle:
1. Appended by the Final Checkpoint (one file per working folder, may hold several sequences)
2. Ingested by `/session-finalize` step 3b (Section 7). Script renames to `partition-observations.ingested.jsonl` after a successful merge
3. `/cleanup` Category 7 deletes `_agent_work/`. Guard: if the folder contains a `*.jsonl` without `.ingested`, skip the folder, report "un-ingested observations - run /session-finalize first"
4. Never written to `[PROMPTSYSTEM_FOLDER]`, `[AGENT_FOLDER]`, or workspace root. The registry holds the aggregate, the session holds the raw lines until archived

Why sums and not a workspace-level ledger: a central raw file would be a second cross-session store beside the registry and would sit in a synced folder. Merging sums into the registry keeps one home and makes deleting the raw lines safe.

## 7. Aggregation into the Registry

Script `aggregate-partition-observations.py` in `.devin/skills/llm-evaluation/` (code belongs there; data does not). Called by `/session-finalize` step 3b with the session path; scans `**/_agent_work/partition-observations.jsonl`, tolerates and reports malformed lines.

Registry entry after merge (3 behavior properties total):

```json
{"provider":"zai","model_id":"glm-5.2", ..., "tier":"C",
 "tier_note":"observed: skips items in 6+ lists, over-eager (2026-10); OverAct SIR 2.00",
 "observed":{"items_planned":52,"items_done":38,"extra_actions":17,"prompts":13,"sequences":4,
             "self_audited_prompts":3,"last":"2026-10-19","if":0.73,"eg":1.33,"tier_suggested":"C"}}
```

- `if` = items_done / items_planned; `eg` = 1 + extra_actions / items_planned (derived, recomputed on each merge)
- `tier_suggested`: A if `if >= 0.90` and `eg <= 1.20`; C if `if < 0.75` or `eg > 1.50`; else B. Only emitted when `sequences >= 3`; otherwise `null`
- Script never writes `tier`. `update-model-registry.md` gets a step "Review `tier_suggested` vs `tier`; on change set `tier` and append reason to `tier_note`"
- Model resolution: `model_id` from frontmatter `intended_model`; Devin display names resolved by the same loose match the model switcher uses; unresolved names collected under `"model_id":"unresolved:<name>"` for manual mapping
- Tested via `test_all_scripts.py` with a fixture ledger

## 8. Implementation Map

- `agent-behavior.md` File Placement: `[SESSION_FOLDER]/_agent_work/` and `[WORKSPACE_FOLDER]/_agent_work/` (PROJECT-MODE) replace "session folder" as the location for `.tmp_` and `__` artifacts
- `write-prompts.md`: Step 2 location; Step 1 tier lookup and parameter commentary; Step 4a-bis Final Checkpoint insertion; Step 5 checks (PRMT-SQ-05, numbered items)
- `PROMPTS_GUIDES.md`: Section 1c tiers A/B/C with parameters; Section 3a Final Checkpoint; Section 5 density becomes `max_items` by tier
- `PROMPTS_RULES.md`: PRMT-SC-05 adds `tier`; new PRMT-SQ-05 Final Checkpoint; new PRMT-CT-15 numbered countable items; new PRMT-SC-09 strict scope guard for tier C
- `PROMPTS_TEMPLATE.md`, `PROMPTS_EXAMPLE_01`: add Final Checkpoint and `_agent_work/` paths
- `write-strut.md`, `go.md`, `deep-research.md`, `bugfix.md`: scaffolding location `_agent_work/`
- `drift-detect.md`, `DRIFT_DETECTION.md`, `DRIFTS_TEMPLATE.md`, `DRIFT_TEMPLATE.md`: sequence directive, EXTRA status, Partition block, ledger write, `_agent_work/` location
- `drift-correct.md`: locate `__DRIFT_*` in `_agent_work/`; EXTRA items are not TODOs
- `session-finalize.md`: step 3b run aggregation; step 7 confirm all ledgers `.ingested`
- `cleanup.md`: Category 7 Agent work folder with ingestion guard; Protected Locations unchanged
- `model-registry.json`: `tier` for all 75 entries, `tier_note` where deviating, `observed` added by script only; `_comment` documents the three properties
- `llm-evaluation/aggregate-partition-observations.py` + fixture; `update-model-registry.md` review step
- `promptsystem-core.md` folder structure diagrams: add `_agent_work/`

## 9. Risks and Open Points

- **Self-audit bias**: if the engine cannot switch model for the Final Checkpoint, tier-C models under-report their own skips. Mitigation: `auditor_model` in the ledger; aggregation reports `self_audited_prompts`; reviewer discounts. [ASSUMED]
- **EXTRA detection precision**: distinguishing "unrequested change" from "necessary side effect" (import added, test fixture updated) is judgment. Rule: EXTRA = new file or changed file not named in any prompt; changes inside named files count as PASS/FAIL on their item. Coarse but countable. [ASSUMED]
- **Numbered items add tokens for tier-C prompts**: 4 items plus guard is still shorter than today's 6-8 unstructured constraints. Net neutral. [ASSUMED]
- **Transition**: existing sessions have artifacts at root. `/cleanup` keeps Categories 1 and 6 for stray files; no migration of archived sessions.
- **Framework dependence**: observations from Cascade runs and from `call-llm.py` runs are not comparable (SNARE: framework explains 56% of variance). Ledger `engine` field records the execution framework (`cascade`, `lana`, `claude-code`); aggregation should group or flag cross-engine comparisons. [VERIFIED - IN04]
- **Failed checkpoint degrades silently**: if `/drift-detect log sequence` fails (STRUT missing, prompts file unparseable, working folder empty), no ledger line is written. The observation is lost without trace. SPEC should define a fallback: either a minimal error line (`"error": true`) or a PROBLEMS.md entry so the gap is visible. [ASSUMED]
- **Execution model unknown to the model**: Cascade cannot introspect its own LLM identity at runtime (verified 2026-10-19). The `intended_model` from frontmatter is the planned model; if the user or engine switches model mid-sequence, all prompts are attributed to the frontmatter value. An `execution_model` field would require the engine to inject it - not available today. SPEC should state that `intended_model` is plan-of-record, not guaranteed execution identity. [VERIFIED - tested in conversation]
- **Ledger retention after ingestion**: after `.ingested.jsonl` rename and `/cleanup`, raw observation data is gone. If the aggregation script had a bug, recalculation from raw lines is impossible. SPEC should decide: 1) keep ingested ledgers in `_Archive/` alongside the session, or 2) accept loss because the registry aggregate is the source of truth after merge. [ASSUMED]
- **Bootstrap tier for uncovered models**: IN05 coverage matrix does not cover all 75 registry entries. Line 91 handles models missing from the registry (`unknown model = C`), but models present in the registry without benchmark data also need a default tier. Rule proposal: no benchmark data and no observations = tier B (middle ground); SPEC confirms or overrides. [ASSUMED]
- **Concurrent sequence writes**: two prompt files executing in the same working folder append to the same `partition-observations.jsonl`. JSONL append is line-atomic in most file systems and runtimes, but Cascade terminal writes are not guaranteed atomic. Low risk in practice (concurrent prompts in one folder is rare), but SPEC should state the assumption. [ASSUMED]
- **`max_items` overrides existing density heuristic**: PRMT guides use 5-8 instruction density. Tier C `max_items: 4` is below that range. SPEC should state that tier parameters take precedence over the default density guidance, and update PROMPTS_GUIDES.md Section 5 accordingly. [ASSUMED]

## Sources

- `MDLRGUP-MDLBHVPRM-IN07-SC-IPPS-WRTPRMPT`: `.devin/workflows/write-prompts.md` - Steps 1-5, PRMT-SQ-04 checkpoint template [VERIFIED]
- `MDLRGUP-MDLBHVPRM-IN07-SC-IPPS-DRFTDTCT`: `.devin/workflows/drift-detect.md` - log mode, Steps 1-5, DoD statuses [VERIFIED]
- `MDLRGUP-MDLBHVPRM-IN07-SC-IPPS-DRFTCRCT`: `.devin/workflows/drift-correct.md` - FAIL-only correction, `__DRIFT_` location [VERIFIED]
- `MDLRGUP-MDLBHVPRM-IN07-SC-IPPS-DRFTSTMPL`: `.devin/skills/drift-control/DRIFTS_TEMPLATE.md` - entry fields lack model attribution [VERIFIED]
- `MDLRGUP-MDLBHVPRM-IN07-SC-IPPS-CLEANUP`: `.devin/workflows/cleanup.md` - Categories 1-6, Post-Workflow Cleanup Trigger, Protected Locations [VERIFIED]
- `MDLRGUP-MDLBHVPRM-IN07-SC-IPPS-SESSFIN`: `.devin/workflows/session-finalize.md` - Steps 1-7, sync points [VERIFIED]
- `MDLRGUP-MDLBHVPRM-IN07-SC-IPPS-CRITIQUE`: `.devin/workflows/critique.md` - `[filename]_CRITIQUE.md` placed beside reviewed file [VERIFIED]
- `MDLRGUP-MDLBHVPRM-IN07-SC-IPPS-FINDCARD`: `PROMPTS_EXAMPLE_03-FindingsCard.md` - six-field entry, card location [VERIFIED]
- `MDLRGUP-MDLBHVPRM-IN07-SC-IPPS-IN06`: `_INFO_MDLBHVPRM-06_ModelAwarePartitioning.md` - tiers and parameters [VERIFIED]

## Next Steps

1. `/write-spec` for `_agent_work/` folder convention (touches agent-behavior, promptsystem-core, cleanup, write-* workflows) - COMPLEXITY-MEDIUM, independent of 2-3
2. `/write-spec` for `/write-prompts` tier partitioning + Final Checkpoint (IN06 Option 2 + Section 4)
3. `/write-spec` for `/drift-detect` sequence mode, ledger, aggregation script, registry `observed` (Sections 5-7)
4. Seed `tier` for all registry entries from IN05 coverage matrix; `tier_note` for GLM-5.x and other observation-overridden entries
5. Confirm with the execution engine (Lana) whether `<!-- model: high -->` commentary can trigger a model switch

## Document History

**[2026-10-19 17:35]**
- Added: 6 open problems from `/verify` to Section 9 (failed checkpoint, execution model identity, ledger retention, bootstrap tier, concurrency, density override)

**[2026-10-19 17:20]**
- Fixed: Timeline format (INFO-HD-03), TOC links (INFO-TC-01)
- Fixed: Removed phantom `*_REVIEW.md` from Out list, removed "POC scripts" from In list (not cleanable output)
- Fixed: Added `engine` field to ledger schema (was only in Section 9 risk)
- Fixed: Self-audit wording from "down-weight" to "reviewer discounts" (no automatic mechanism)
- Added: PROJECT-MODE `[WORKSPACE_FOLDER]/_agent_work/` to Section 2 Scope

**[2026-10-19 16:55]**
- Initial document: folder convention, data flow, planned/actual sides, ledger, aggregation, implementation map
