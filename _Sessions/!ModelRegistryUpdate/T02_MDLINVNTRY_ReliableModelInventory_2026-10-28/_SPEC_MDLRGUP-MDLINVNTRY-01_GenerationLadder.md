# SPEC: Generation Ladder for MODEL_INVENTORY.md

**Doc ID**: MDLRGUP-MDLINVNTRY-SP01
**Feature**: generation-ladder-inventory
**Goal**: Specify the append-only generation ladder, the Items axis, the registry 1.12.0 fields, the inventory layout, the update-run gates, and the consumer changes that replace year-letter labels, ECI bands, WF, and behavior profiles
**Timeline**: Created 2026-11-02, Updated 3 times (2026-11-02 - 2026-11-18)
**Target file(s)**:
- `PromptSystemV4.5/skills/llm-tools/model-registry.json`
- `PromptSystemV4.5/skills/llm-tools/MODEL_INVENTORY.md`
- `_Sessions/!ModelRegistryUpdate/update-model-inventory.py`, `match-epoch-eci.py`, new `layer-generation-ladder.py`, `verify-and-distribute-registry.ps1` (reusable session scripts)
- `_Sessions/!ModelRegistryUpdate/_PROMPTS_ModelInventoryUpdate_TEMPLATE.md`
- `PromptSystemV4.5/skills/write-documents/PROMPTS_GUIDES.md`, `TASKS_GUIDES.md`, `PROMPTS_RULES.md`, `PROMPTS_TEMPLATE.md`; `PromptSystemV4.5/workflows/write-prompts.md`; `PromptSystemV4.5/skills/edird-phase-planning/SKILL.md`

**Depends on:**
- `_INFO_HOW_TO_ORGANIZE_LLMS_BY_CAPABILITY.md [LLMCAPCLS-IN01]` for the ladder design, the computed 12-rung ladder, the edge-case catalogue EC-1 to EC-9, and the prompt-shape mapping
- `_INFO_MDLBHVPRM-06_ModelAwarePartitioning.md [MDLRGUP-MDLBHVPRM-IN06]` for the partition parameters and MDLBHVPRM-DD-01 (observation overrides benchmarks)
- `_INFO_MDLBHVPRM-07_PromptFeedbackLoop.md [MDLRGUP-MDLBHVPRM-IN07]` for the observation ledger that calibrates Items

**Does not depend on:**
- `_INFO_HOW_TO_ORGANIZE_LLMS_BY_CAPABILITY_v1.md` (year-letter scheme; superseded)
- `windsurf-model-registry.json` content (Devin cost multipliers are read, never changed)

## MUST-NOT-FORGET

- A `generation` value, once written, never changes; the only permitted transition is `generation_estimated: true` → measured (MDLRGUP-MDLINVNTRY-IG-01)
- No edge without a citable source: silence from the named source = tie, never judgment (MDLRGUP-MDLINVNTRY-FR-04)
- `MODEL_INVENTORY.md` is generated; agents read it and compute nothing (GRUC separation, MDLRGUP-MDLINVNTRY-IG-04)
- `[PROMPTSYSTEM_FOLDER]` is the source of truth; `.devin/` is a mirror
- `update-model-registry.md` distributes JSONs to external config folders; never run it without explicit [ACTOR] confirmation
- Goal 3 of the topic: `MODEL_INVENTORY.md` under 60 lines of rules and definitions; fewer numbers, not relabeled numbers
- Nothing in the inventory or the planning method may depend on Devin, Cascade, or IPPS workflow names (Goal 2)

## Table of Contents

1. [Scenario](#1-scenario)
2. [Context](#2-context)
3. [Domain Objects](#3-domain-objects)
4. [Functional Requirements](#4-functional-requirements)
5. [Non-Functional Requirements](#5-non-functional-requirements)
6. [Design Decisions](#6-design-decisions)
7. [Implementation Guarantees](#7-implementation-guarantees)
8. [Key Mechanisms](#8-key-mechanisms)
9. [Action Flow](#9-action-flow)
10. [Data Structures](#10-data-structures)
11. [Logging Requirements](#11-logging-requirements)
12. [Technical Constraints](#12-technical-constraints)
13. [Document History](#13-document-history)

## 1. Scenario

**Problem:** `MODEL_INVENTORY.md` ranks models by a year-letter label derived from Epoch ECI bands. The bands are narrower than the benchmark's confidence intervals, so the labels contradict vendor lineups (`claude-opus-5-5` above `claude-fable-5`, `claude-haiku-5-5` above `claude-opus-4-6`), shift every year (anchor, May 1 wrap, Comp column), and feed a per-model HWH factor (WF) that the ledger disproved. Prompt authors cannot trust the row they read, and every yearly regrade invalidates earlier prompts files.

**Solution:**
- One ordinal rung `G01`, `G02`, ... per model, assigned once from evidence a reader can check (vendor tier, successor order, non-overlapping Epoch intervals, in-house observation), never regraded
- Every undecidable case has a named research source and a recorded outcome; no outcome rests on judgment
- A second, measured axis Items (instructions completed per prompt without skips) from the observation ledger
- Prompt shape read from the absolute rung (explicitness level, Items default) and from Notes (scope guard, adaptive Medium warning)
- Registry carries the evidence; a script layers the ladder; the inventory is a generated view; a gate forbids rung changes between runs

**What we don't want:**
- Scores, bands, letters, year anchors, comparison years, or any value that moves when a newer model appears
- A model-specific HWH divisor (WF) or behavior profile names
- Rungs set by the prompt-writing agent, or by an agent reading a benchmark table at run time
- Edges from aggregators, leaderboards other than Epoch ECI, or LLM recollection
- A second tiering scheme beside Universal Class (UC-1..4) and the ladder

### Architecture

```
┌─ Evidence ───────────────────────────────────────────────────────────────────────────────┐
│  model-registry.json            Epoch ECI CSV            Vendor pages        Ledger      │
│  uc_class, release_date,        score, CI low/high       guidance, "same     items_done  │
│  higher_than (manual edges)     (matched per run)        model", successor   per prompt  │
└──────────┬───────────────────────────┬──────────────────────────┬──────────────┬─────────┘
           v                           v                          v              v
┌─ Scripts ────────────────────────────────────────────────────────────────────────────────┐
│  match-epoch-eci.py  ──>  layer-generation-ladder.py  ──>  update-model-inventory.py     │
│  eci_score, eci_ci        generation,                      rows sorted by Generation     │
│                           generation_evidence,                                           │
│                           generation_estimated (insert-only) │                           │
│  /session-finalize: ledger ──> observed.items ──> items, scope_guard                      │
└──────────────────────────────────────────────┬───────────────────────────────────────────┘
                                               v
┌─ Generated view ─────────────────────────────────────────────────────────────────────────┐
│  MODEL_INVENTORY.md                                                                      │
│  Model | Generation | Items | Context | Efforts | prices | Devin | Notes                 │
└──────────────────────────────────────────────┬───────────────────────────────────────────┘
                                               v
┌─ Consumers (read only) ──────────────────────────────────────────────────────────────────┐
│  /write-tasks-plan   /write-strut   /write-prompts   /verify (PRMT-SC-05)                │
│  effort shift ──> effective rung ──> explicitness level ──> expanded items / Items ──> N  │
└──────────────────────────────────────────────────────────────────────────────────────────┘
                                               ^
  Gate 9.4 (verify-and-distribute-registry.ps1): no rung changed, every edge sourced ──────┘
```

## 2. Context

Topic `MDLINVNTRY` (session `!ModelRegistryUpdate`) set three goals: a workable planning method for TASKS and prompts files, general-purpose use in any agentic environment, and a lean inventory with sourced numbers. `IN01` to `IN05` audited the inventory (45% of classified items `ASSUMED`), collected sources, and compared work-per-prompt options. `LLMCAPCLS-IN01` version 1 introduced year-letter labels (DD-01 b-variant, 2026-10-29); version 2 (2026-11-02, DD-10 option 3) replaced them with the generation ladder after the letters contradicted four vendor lineups. DD-11 (Fable above Opus 5.5) was closed from Anthropic's model-selection guidance; DD-12 approved this specification.

The registry update run is executed from `_PROMPTS_ModelInventoryUpdate_TEMPLATE.md` (Prompts 1-6, one run folder per run). Registry 1.11.0 is the current state; this specification defines 1.12.0.

## 3. Domain Objects

### Generation Rung

A **Generation Rung** `G[nn]` is the integer position of a model on the ladder. `G01` is the lowest registered model; higher means provably deeper reasoning (more may stay implicit in a prompt).

- `generation` - integer, written once by the layering script
- `generation_evidence` - the edge that set the rung: `"E3 > gpt-5.4-pro"`, `"E1 > claude-sonnet-5-5"`, `"E1m > claude-opus-5-5"`, `"E6 from glm-4.7"`, `"bottom"`
- `generation_estimated` - `true` for E6 rungs (shown as `G02*`); absent otherwise
- Equal rung = equal prompt shape, not equal quality

### Evidence Edge

An **Evidence Edge** `x > y` states that x provably dominates y. Kinds:

- `E1` vendor lineup tier: same provider, same point version, lower `uc_class` number (strict)
- `E2` successor not below predecessor: same provider, tier, series; later release (weak, `>=`)
- `E3` benchmark separation: `ci_low(x) > ci_high(y)` on Epoch ECI 95% intervals (strict)
- `E4` in-house observation: head-to-head result naming both models on the same task (strict, overrides E3)
- `E5` sibling tie: unscored model = scored same-provider, same-point-version, same-tier sibling
- `E6` tier-offset estimate: `D(sibling) - (tier(x) - tier(sibling))`, floor 1, marked estimated
- `E1m`, `E4m` manual edges recorded in the registry with a source (Section 3 Manual Edge)

### Manual Edge

A **Manual Edge** is a `higher_than` entry on a registry model: the dominated model, the kind (`E1` or `E4`), the source URL or file, the access date, and the quoted statement. Written by hand after the research step of the matching edge case (FR-04); read by the layering script; rejected when it closes a cycle.

### Items

**Items** is the number of numbered instruction items one implementation prompt may hold for a model so that all complete without skips.

- Measured: largest `items_planned` with `items_done == items_planned` over `>= 3` ledger sequences; stored as `items` (shown `8m`)
- Default: from the effective rung, `G10+` 8, `G07-G09` 6, `G04-G06` 5, `G01-G03` 4
- Shape parameters keyed to Items: `max_files` 6 / 3 / 2 and checkpoint interval 3 / 2 / 1 for Items 8 / 6 / `<= 5`
- `scope_guard: "strict"` when a FAILS or ledger entry documents unrequested actions; does not lower Items

### Inventory Row

An **Inventory Row** is one line of `MODEL_INVENTORY.md` Section 3: `Model | Generation | Items | Context | Efforts | In USD | Cache USD | Out USD | Devin cost | Notes`. Notes carries `generation_evidence`, `UC-n`, Epoch score with interval or `no Epoch score`, status, `scope guard strict`, `CSV rows`, adaptive Medium warning, `squeezed by X`, `unplaced`.

### Edge Case

An **Edge Case** `EC-[n]` is a situation the automatic edges cannot decide, paired with exactly one source type and one rule (FR-04). Nine are defined; new ones are added to `LLMCAPCLS-IN01` Section 2.6 before use.

## 4. Functional Requirements

**MDLRGUP-MDLINVNTRY-FR-01: Generation assignment**
- Every text model in the registry except `status: retired` has a `generation`
- Bootstrap (once): rungs of all models solved together to a fixed point: `D(x) = max(1, max strict-dominated D + 1, max weak-dominated D, D of E5 sibling)`; the layering aborts and names both edges when the iteration does not converge (cycle)
- Insertion (every later run): a model without `generation` receives `floor` as above; if `floor` exceeds `min(D of strict dominators) - 1` or `min(D of weak dominators)`, it receives that cap and Notes `squeezed by [dominator]`; existing rungs never move
- E6 applies when a model has no score, no E5 sibling, and no predecessor but a scored sibling of another tier; otherwise `G01` with Notes `unplaced`

**MDLRGUP-MDLINVNTRY-FR-02: Automatic edges**
- E1 from `uc_class` within one provider and point version; point version per provider: Anthropic `claude-[tier]-[version]` → version; OpenAI `gpt-N[.N]` or `oN`; Google `gemini-N[.N]`; Z.AI `glm-N[.N]`; xAI `grok-N[.N]`
- E2 from the immediate predecessor in the same provider, tier, and series; specialized models (`codex`, `cyber`, `deep-research`, `legal`, `non-reasoning`, `multi-agent`, `build`, vision `v`) form their own series and have no E2 edges
- E3 from `eci_ci` of both models; a model without an interval has no E3 edges in either direction
- E5 from a scored sibling with the same provider, point version, and tier

**MDLRGUP-MDLINVNTRY-FR-03: Manual edges**
- `higher_than` entries carry `model`, `kind` (`E1` or `E4`), `source` (URL or file), `accessed` (date), `statement` (quote)
- The layering script adds them as strict edges, rejects an entry that closes a cycle, and reports the conflicting automatic edge
- Current entries (from DD-11): `claude-fable-5-1 > claude-opus-5-5` (E1, Anthropic Fable 5.1 overview, 2026-11-02); `claude-fable-5 > claude-opus-5-5` (E1 inherited per EC-2, Fable 5.1 what's new, 2026-11-02)

**MDLRGUP-MDLINVNTRY-FR-04: Edge-case resolution**
- Each case below is resolved by reading the named source and recording the outcome before the layering script runs; when the source is silent the outcome is a tie
- EC-1 tier order across point versions: vendor model-selection guidance in platform documentation; escalation statement = E1 edge, parity statement or silence = tie
- EC-2 superseded member of a tier family: successor's "extends" or "succeeds" statement at same tier and price; the successor's edge is inherited unless E3 contradicts
- EC-3 restricted-access twin: "same underlying model" or "same capabilities" statement = E5 tie
- EC-4 specialized Apex model without score: vendor announcement naming base and positioning; more capable and higher price = E1 over base, domain variant at equal price = E5 tie
- EC-5 unscored Efficient or vision model: vendor tier wording and price order = E6 estimate
- EC-6 model outside the registry (Devin-only): vendor comparison statement, routing notice, or base-model lineage = `*` rung one below the reference or equal to the routed target
- EC-7 squeeze on insertion: in-house head-to-head test (same prompt, `n >= 3`) or ledger sequences on the same TASKS = E4 edge; until then Notes `squeezed by X`
- EC-8 E1 against E3 contradiction: re-read `uc_class` on the vendor page; wrong class → fix and re-layer; right class → E1 wins, E3 edge dropped with Notes line
- EC-9 wrong registry input: vendor model overview "Released" field is the source; corrections recorded in PROBLEMS and applied in the same run

**MDLRGUP-MDLINVNTRY-FR-05: Registry 1.12.0 fields**
- Added per model: `eci_ci` `[low, high]`, `generation`, `generation_evidence`, `generation_estimated` (when true), `higher_than` (list, when present), `items` (integer or absent), `scope_guard` (`"strict"` when present)
- Removed per model: `capability_label`, `eci_band`, `eci_band_source`, `gen_equivalent`, `behavior_profile`, `capability_note`
- `observed` gains `items`; `profile_suggested` is removed
- Registry `_comment` and `version` describe 1.12.0

**MDLRGUP-MDLINVNTRY-FR-06: Epoch match output**
- The match file carries `eci_score`, `eci_ci_low`, `eci_ci_high` per matched model; no band, no band action, no generation equivalent, no class inference
- New models without `uc_class` or `release_date` are listed for manual completion from the vendor model overview

**MDLRGUP-MDLINVNTRY-FR-07: Items and scope guard**
- `/session-finalize` aggregates the ledger into `observed.items` (largest fully completed `items_planned`, with `sequences`); the update run copies it to `items` when `sequences >= 3`
- A skip observation (`items_done < items_planned`) with `sequences >= 3` lowers `items` to the largest fully completed value
- `scope_guard: "strict"` is set by hand with the FAILS or ledger reference in Notes

**MDLRGUP-MDLINVNTRY-FR-08: Inventory layout**
- Sections: 1 Definitions (Generation, Items, HWH, Context), 2 Value Derivation (E1-E6, insertion, effort shift, Items defaults and shape parameters, scope guard, prices), 3 Models (`Top rung: G[nn] (date)`, 3.1 API, 3.2 Devin-only), 4 Maintenance
- Columns: `Model | Generation | ECI Score | Items | Context | Efforts | In USD | Cache USD | Out USD | Value | Released | Notes` (`Value` replaced `Devin cost` per `LLMCAPCLS-IN01` DD-20; `ECI Score` added 2026-11-17; `Released` per FR-14); Generation `G[nn]` or `G[nn]*`; Items default unmarked, measured `[n]m`
- Sort: Generation descending, then Model ascending
- Removed: Label, Comp, Profile, WF columns; anchor, letter, WF formula, profile thresholds, change rule, May 1 wrap

**MDLRGUP-MDLINVNTRY-FR-09: Prompt-shape mapping (consumer rules)**
- Effective rung = `generation` shifted by effort: `H` / `X` no shift; `M` no shift except adaptive-thinking models one rung lower; `L` one rung lower; `-` (no reasoning) two rungs lower
- Explicitness level by effective rung: `G01-G03` keystroke-level (4 items per outcome unit), `G04-G06` step-level (2.5), `G07-G09` outcome plus named files (1), `G10+` goal-level (0.5)
- `prompt_count = max(ceil(expanded_items / Items), ceil(files / max_files), ceil(task_HWH / 1))`; input per prompt `<= 50%` of Context
- `/verify` PRMT-SC-05 recomputes these bounds from the inventory row and fails on items above Items, files above `max_files`, missing checkpoint, missing scope guard text, explicitness below the rung's level

**MDLRGUP-MDLINVNTRY-FR-10: Gate 9.4**
- Every non-retired text model has `generation`
- No `generation` differs from the previous committed registry except where `generation_estimated` was true and is now absent
- Every `higher_than` entry has `source`, `accessed`, `statement`
- Inventory rows sorted per FR-08; `Top rung` equals the maximum `generation`
- Every `Released` cell equals the registry `release_date`; a Devin-only row shows `devin_only[].release_date` or `-` (FR-14)
- Gate failure blocks distribution

**MDLRGUP-MDLINVNTRY-FR-11: Template changes**
- `[CAPABILITY_SCHEME]` values `LADDER | NONE`
- Prompt 4 "Capability Evidence": Epoch score and interval per model (match file); `release_date` and `uc_class` for new models from the vendor model overview; edge-case research (FR-04) with outcomes written to `[DATE]_Generation-Edges.json` (`higher_than` candidates, tie lines, E6 notes); band-freeze sentence removed
- Prompt 5: `eci_score`, `eci_ci`, `uc_class`, `release_date`, `higher_than` written to the registry from the two Prompt 4 files
- Prompt 6 item 2: 1) `layer-generation-ladder.py` insert-only, 2) squeeze and contradiction review, 3) `items`, `scope_guard` from `observed`, 4) `format-model-registry.py`, 5) `update-model-inventory.py`; May 1 wrap bullet removed
- Prompt 6 item 3: Gate 9.4 per FR-10
- Released column (FR-14): Prompts 2 and 3 write `released[]` into every DOM extract; Prompt 5 reconciles it and writes `release_corrections[]`; Prompt 6 writes `release_date` and runs Gate 5.4; Prompt 7 prints `Released`

**MDLRGUP-MDLINVNTRY-FR-12: Consumer documents**
- `PROMPTS_GUIDES.md` 1c, 1f, 1g, 5: WF paragraph removed; budget = Items and 1 HWH cap; 1g rewritten to FR-09
- `TASKS_GUIDES.md` 1, 3, 5, 6: default row `G07-G09`, Items 6; `Est <= 1 HWH`, `expanded_items <= Items`, `files <= max_files`
- `PROMPTS_RULES.md` PRMT-SC-05: commentary states Generation, effective rung, explicitness level, Items, prompt count, cost; strict guard check keyed to Notes
- `write-prompts.md` Step 1, `edird-phase-planning` SKILL.md step sizing (`step HWH <= 1` replaces the 30-minute AWH rule), `PROMPTS_TEMPLATE.md` and `PROMPTS_EXAMPLE_01` commentary rows
- Session `NOTES.md` and `IN01` Section 5: DD-01 superseded by DD-10 option 3; DD-02 and DD-03 absorbed

**MDLRGUP-MDLINVNTRY-FR-13: Devin-only rows**
- Section 3.2 rows carry `*` rungs set per EC-6 with the source in Notes: Kimi K3 `G09*`, Gemini 3.7 Flash `G08*`, Gemini 3.5 Flash `G07*`, SWE-1.7 `G06*`
- Rows are re-evaluated only when the referenced model changes rung or the vendor statement changes

**MDLRGUP-MDLINVNTRY-FR-14: Released column**
- Sections 3.1 and 3.2 carry a `Released` column immediately before `Notes`
- `release_date` is `YYYY-MM-DD` when a vendor page, release note, or announcement prints the day, else `YYYY-MM`; the Epoch date, the run date, and the date of the family head never stand in for a day; `release_date_assumed` does not exist
- Every DOM extract carries `released[]` entries `{model_id, released, source_url, raw_text}` with `released` = `YYYY-MM-DD`, `YYYY-MM`, or `null`
- The Epoch match file reports `released_in_dom`, `new_model_releases`, and `release_conflicts`; a conflict is resolved by a `release_corrections[]` entry with a page source in `[DATE]_Generation-Edges.json`; a day refines a month of the same month, a different month needs the source
- A new model without any printed date is listed in `unresolved[]` and blocks its registry insertion
- A month-only date creates an E2 predecessor edge only toward models of a later month
- A Devin-only row takes `devin_only[].release_date` or `-`

## 5. Non-Functional Requirements

**MDLRGUP-MDLINVNTRY-NFR-01: Reproducibility**
- Re-layering the 2026-10-28 snapshot with the two FR-03 edges in bootstrap mode reproduces `LLMCAPCLS-IN01` Section 3 exactly (12 rungs, 92 models); verified by an automated test beside the script

**MDLRGUP-MDLINVNTRY-NFR-02: Token economy**
- `MODEL_INVENTORY.md` Sections 1, 2, 4 together under 60 lines; Section 2 under 20 lines

**MDLRGUP-MDLINVNTRY-NFR-03: Portability**
- No rung, Items value, or consumer rule references an agent engine or IDE; engine-specific data stays in `windsurf-model-registry.json` and Section 3.2

**MDLRGUP-MDLINVNTRY-NFR-04: Encoding and style**
- UTF-8 for every file; scripts follow @skills:coding-conventions (2-space indentation, `retVal`, single-line calls)

## 6. Design Decisions

**MDLRGUP-MDLINVNTRY-DD-01:** Generation is an ordinal rung from dominance edges, not a score or band. Rationale: Epoch intervals are 4-9 points wide at the top; any band narrower than that reads noise as rank (LLMCAPCLS-IN01 Section 1).

**MDLRGUP-MDLINVNTRY-DD-02:** Rungs are append-only; new models insert, old rungs never move. Rationale: prompts files cite Generation; a regrade would invalidate every earlier file (the year-letter scheme's Comp column did exactly that).

**MDLRGUP-MDLINVNTRY-DD-03:** E1 is derived automatically only within a point version; cross-version edges come from the vendor's model-selection guidance (EC-1). Rationale: Anthropic's `5` → `5.5` is a five-month refresh, OpenAI's `gpt-5` → `gpt-5.6` an 18-month generation; an automatic rule fits one vendor and breaks the other.

**MDLRGUP-MDLINVNTRY-DD-04:** Silence from the named source is a tie. Rationale: a tie costs nothing (equal prompt shape); a judgment edge is unverifiable and propagates through E2 and E5.

**MDLRGUP-MDLINVNTRY-DD-05:** Fable 5 inherits Fable 5.1's edge over Opus 5.5 (EC-2). Rationale: the vendor states Fable 5.1 "extends" Fable 5 at the same tier and price; intervals overlap, so no evidence places Fable 5 below Opus 5.5; [ACTOR] confirmed both edges 2026-11-02.

**MDLRGUP-MDLINVNTRY-DD-06:** Bootstrap solves all rungs together once; later runs insert only. Rationale: release-order insertion produced 22 cascading conflicts in the first run because early models were placed before their evidence existed.

**MDLRGUP-MDLINVNTRY-DD-07:** E6 estimates are the only rungs that may change. Rationale: an estimate is marked as such; replacing it with evidence is a correction, not a regrade.

**MDLRGUP-MDLINVNTRY-DD-08:** Items is measured from the ledger and overrides the default in both directions; it never changes Generation. Rationale: completion capacity and reasoning depth are independent (GLM-5.2 at High skipped items before the scope guard; the guard fixed completion, not depth).

**MDLRGUP-MDLINVNTRY-DD-09:** Explicitness levels and Items defaults keep the former profile constants (4 / 5 / 6 / 8; keystroke / step / outcome / goal). Rationale: no measurement exists yet; the ledger is the calibration path; new constants would be new assumptions.

**MDLRGUP-MDLINVNTRY-DD-10:** WF is removed; HWH caps a prompt at 1 and sizes cost. Rationale: METR's horizons carry factor-2 error bars, the TBLF test showed effort outweighs capability bands, and the ledger measures items, not hours.

**MDLRGUP-MDLINVNTRY-DD-11:** Edge-case research is a prompt step in the update run, not script logic. Rationale: the sources are prose pages; a script can detect that a case exists (unscored model, cross-version Apex) but cannot read the statement.

**MDLRGUP-MDLINVNTRY-DD-12:** `Generation` replaces `Depth` as column name, label prefix (`G[nn]`, two digits: `G01`-`G13`, `*` for estimates), JSON key (`generation`, `generation_evidence`, `generation_estimated`; manual edges `higher_than`), and file name (`layer-generation-ladder.py`, `test-layer-generation-ladder.py`, `[DATE]_Generation-Edges.json`, `[DATE]_GenerationLadder.log`, this specification); history files (earlier run folders, run reports, ladder logs and edges files of earlier runs, tracking files) keep the old names. Rationale: user decisions GEN-01 option 2 and GEN-02 option 1 (2026-11-18); the rename changes names only, every rung value stays (registry 1.14.0: 124 rungs, same values as 1.13.3).

**MDLRGUP-MDLINVNTRY-DD-13:** The registry stores the precision a source supports (`YYYY-MM-DD` or `YYYY-MM`) instead of a full date plus an assumed flag. Rationale: user request 2026-11-18; a stored day that no source printed reads as fact in every consumer. The 46 dates that carried `release_date_assumed` became months (registry 1.15.0); no rung changed (regression test 8 of 8, insert-only dry run 0 inserted, 0 squeezed, 0 cycles).

## 7. Implementation Guarantees

**MDLRGUP-MDLINVNTRY-IG-01:** Gate 9.4 fails when any `generation` differs from the previous committed registry, except `generation_estimated` → measured.

**MDLRGUP-MDLINVNTRY-IG-02:** The layering script never writes a `generation` for a model that already has one; in bootstrap mode it refuses to run when any `generation` exists.

**MDLRGUP-MDLINVNTRY-IG-03:** Every `higher_than` entry without `source`, `accessed`, and `statement` is rejected by the layering script and by Gate 9.4.

**MDLRGUP-MDLINVNTRY-IG-04:** `MODEL_INVENTORY.md` contains no value that is not derivable from the registries by `update-model-inventory.py`; hand edits are overwritten on the next run.

**MDLRGUP-MDLINVNTRY-IG-05:** A cycle among strict edges aborts the layering with both edges named; no partial registry is written.

**MDLRGUP-MDLINVNTRY-IG-06:** Consumer documents name Generation, Items, and Notes only; Label, Comp, Profile, WF, and ECI band do not appear in any file under `[PROMPTSYSTEM_FOLDER]` after implementation.

**MDLRGUP-MDLINVNTRY-IG-07:** Gate 5.4 fails when a registry `release_date` is neither `YYYY-MM-DD` nor `YYYY-MM`, when `release_date_assumed` exists, or when a DOM `released[]` value differs from the registry value (a registry day inside the DOM month is no difference); Gate 9.4 fails when a `Released` cell differs from the registry.

## 8. Key Mechanisms

- **Fixed-point layering** (bootstrap): start every model at `G01`; repeat "raise each model to its floor from the current rungs" until no rung changes; more iterations than models = cycle. Order-independent, so the result does not depend on release order
- **Capped insertion** (later runs): floor from dominated models, cap from dominators; floor above cap = squeeze, recorded, never resolved by moving a frozen rung
- **Evidence precedence**: E4 > E1 > E3 when they conflict (MDLBHVPRM-DD-01 for E4; EC-8 for E1 over E3); E2 and E5 never conflict with strict edges because they only raise to a tie
- **Research-then-layer**: the update run resolves edge cases (FR-04) in prose, writes `higher_than` and Notes, then runs the script; the script validates (sources present, no cycle) but never decides
- **Two-axis prompt shape**: Generation → how explicit each instruction must be (items per outcome unit); Items → how many instructions one prompt may hold; the product divided by Items gives the prompt count, capped by files and 1 HWH
- **Measured override**: `observed.items` from the ledger replaces the Items default when `sequences >= 3`; a later skip lowers it; Generation untouched

## 9. Action Flow

```
Registry update run (Prompt 6, Phase 9.4)
├─> Prompt 4 wrote eci_score, eci_ci_low, eci_ci_high for new models (match file)
├─> Author sets release_date, uc_class for new models from the vendor model overview
├─> Author resolves edge cases (FR-04)
│   ├─> EC-1/EC-2/EC-3/EC-4: read vendor page ──> higher_than entry or Notes tie line
│   ├─> EC-5/EC-6: tier wording and price ──> E6 estimate noted
│   └─> EC-9: vendor "Released" field ──> registry correction + PROBLEMS entry
├─> layer-generation-ladder.py (insert-only)
│   ├─> validates higher_than (source, accessed, statement) ──> reject + name entry
│   ├─> builds E1, E2, E3, E5 edges + manual edges
│   ├─> verifies existing generation values are consistent ──> report only
│   ├─> inserts new models (floor, cap, squeeze) ──> generation, generation_evidence, generation_estimated
│   └─> cycle ──> abort, name both edges, write nothing
├─> Author reviews squeezes and contradictions ──> EC-7 / EC-8 follow-up or accept
├─> Author copies observed.items ──> items (sequences >= 3); sets scope_guard with reference
├─> format-model-registry.py
├─> update-model-inventory.py ──> MODEL_INVENTORY.md (Top rung, sorted rows, Notes)
└─> verify-and-distribute-registry.ps1 Gate 9.4 ──> pass: distribute | fail: stop, report
```

## 10. Data Structures

**Registry model entry (1.12.0):**
```json
{"provider": "anthropic", "model_id": "claude-fable-5-1", "name": "Claude Fable 5.1", "context_window": 1000000, "enabled": false, "status": "untested",
 "uc_class": "UC-1 Apex", "release_date": "2026-09-01", "eci_score": 166.49, "eci_ci": [163.47, 171.35],
 "generation": 12, "generation_evidence": "E1m > claude-opus-5-5",
 "higher_than": [{"model": "claude-opus-5-5", "kind": "E1", "source": "https://platform.claude.com/docs/en/models/fable-5-1/overview", "accessed": "2026-11-02",
                  "statement": "For most workloads, start with Claude Opus 5.5. Use Claude Fable 5.1 for demanding reasoning and long-horizon agentic work, or when your evals on Claude Opus 5.5 at higher effort still don't meet your requirements."}]}
```

**Estimated rung:**
```json
{"model_id": "glm-4.7-flash", "uc_class": "UC-4 Efficient", "eci_score": null, "eci_ci": null, "generation": 2, "generation_evidence": "E6 from glm-4.7", "generation_estimated": true}
```

**Measured Items with scope guard:**
```json
{"model_id": "glm-5.2", "generation": 6, "generation_evidence": "E3 > gemini-2.5-pro", "items": 8, "scope_guard": "strict",
 "observed": {"items": 8, "sequences": 3, "if": 1.0, "eg": 2.0}}
```

**Match file entry:**
```json
{"model_id": "claude-sonnet-5-5", "epoch_name": "Claude Sonnet 5.5", "eci_score": 166.18, "eci_ci_low": 163.06, "eci_ci_high": 171.34}
```

**Inventory row (Section 3.1):**
```
| claude-fable-5-1 | G12  | 8  | 1M   | L M H X | 10.00 | 0.25 | 50.00 | .. | E1m > claude-opus-5-5; UC-1; 166.5 [163.5-171.4]; adaptive: Medium may skip reasoning |
| glm-5.2          | G06  | 8m | 200K | H       | ..    | ..   | ..    | -  | E3 > gemini-2.5-pro; UC-2; 151.9 [150.0-154.1]; scope guard strict (FAILS ref)         |
| glm-4.7-flash    | G02* | 4  | 200K | H       | ..    | ..   | ..    | -  | E6 from glm-4.7; UC-4; no Epoch score                                                  |
(`..` = value from model-pricing.json / windsurf-model-registry.json)
```

## 11. Logging Requirements

**Applicable logging types:**
- [x] Script-Level (SC) - `LOGGING-RULES-SCRIPT-LEVEL.md` (layering script, inventory script, Gate 9.4)
- [ ] User-Facing (UF) - not applicable: no end-user console
- [ ] App-Level (AP) - not applicable: no service

**Script-Level logging:**
- **Audience**: the author running Prompt 6, and the reviewer reading the run folder afterwards
- **Goal**: from the log alone, know how many models were layered, which were inserted at which rung with which edge, which were squeezed, which manual edges were rejected and why, and whether a cycle stopped the run
- **Key operations**: edge construction, validation of `higher_than`, insertion per new model, cycle detection, gate checks

**Expected output for an insert-only run:**
```
Layering generation ladder from model-registry.json 1.12.0 and 2026-11-28_Epoch-ECI-Match.json...
  94 models, 92 with generation, 2 to insert.
  Manual edges: 2 valid, 0 rejected.
  Edges: E1 61, E2 48, E3 2104, E5 6, manual 2.
  [ 1 / 2 ] claude-opus-5-6: G12 (E1 > claude-sonnet-5-6 G11)
  [ 2 / 2 ] gemini-4-neon: G09, squeezed by E3 < gemini-4-argon (G10); floor was G10 (E3 > gpt-5.4-pro)
  Existing rungs consistent: 92 / 92.
  OK: 2 inserted, 1 squeezed, 0 cycles.
```

**Expected output for a rejected edge:**
```
  Manual edges: 1 valid, 1 rejected.
    REJECTED claude-fable-5 > claude-opus-5-5: missing 'accessed'
```

## 12. Technical Constraints

- The Epoch CSV at `https://epoch.ai/data/eci_scores.csv` is the only benchmark source; its interval columns feed `eci_ci`; a model absent from the CSV has `eci_ci: null`
- `uc_class`, `release_date`, `higher_than`, `items`, `scope_guard` are hand-maintained registry inputs; `generation`, `generation_evidence`, `generation_estimated`, `eci_score`, `eci_ci` are script outputs
- The layering script reads the registry and the run's match file only; it has no network access
- The inventory script reads the four registries (`model-registry.json`, `model-pricing.json`, `model-parameter-mapping.json`, `windsurf-model-registry.json`) and writes `MODEL_INVENTORY.md` only
- Gate 9.4 compares against the previous committed registry (git `HEAD`), so the registry must be committed before each run
- `.tmp_dominance_ladder.py` in `_Sessions/!ModelRegistryUpdate/_agentwork/` is the reference implementation of the layering (bootstrap mode, E1/E2/E3/E5, manual edges); E6, insert-only mode, and validation are not yet implemented there
- Skill files are general-purpose: no session paths, no real identifiers in illustrative content

## 13. Document History

**[2026-11-18 17:40]**
- Added: MDLRGUP-MDLINVNTRY-FR-14 (Released column), DD-13 (registry stores the precision a source supports), IG-07 (Gate 5.4, Gate 9.4 Released check)
- Changed: FR-08 column list (now `ECI Score`, `Value`, `Released`; `Devin cost` removed); FR-10 and FR-11 name the Released checks and prompts; the Section 10 sample inventory row is not updated

**[2026-11-18 15:18]**
- Added: MDLRGUP-MDLINVNTRY-DD-12 (rung renamed Depth -> Generation)
- Changed: file renamed from `_SPEC_MDLRGUP-MDLINVNTRY-01_DepthLadder.md`; labels `G[nn]`, column, registry keys, script and file names in every section, including earlier history entries; item IDs unchanged; Architecture diagram re-aligned

**[2026-11-02 14:10]**
- Fixed: script locations are the session folder, not the skill folder
- Changed: FR-11 moves edge-case research into Prompt 4 (vendor pages are read there) and adds `[DATE]_Generation-Edges.json` as its output; Prompt 6 runs the layering only

**[2026-11-02 13:45]**
- Initial specification created from `LLMCAPCLS-IN01` Sections 2, 4, 5 after DD-11 (both Fable edges recorded) and DD-12 (approved) on 2026-11-02
