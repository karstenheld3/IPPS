# INFO: How to Organize LLMs by Capability

**Doc ID**: LLMCAPCLS-IN01
**Goal**: Define an append-only generation ladder per model, the working-set size per model, and how `MODEL_INVENTORY.md` is produced from them and used to partition TASKS, STRUT, and prompts files by model, effort, and context window
**Timeline**: Created 2026-10-28, Updated 14 times (2026-10-28 - 2026-11-18)
**Target file**: `PromptSystemV4.5/skills/llm-tools/MODEL_INVENTORY.md`, `PromptSystemV4.5/skills/llm-tools/model-registry.json`, `_Sessions/!ModelRegistryUpdate/_PROMPTS_ModelInventoryUpdate_TEMPLATE.md`

**Depends on:**
- `_INFO_MDLBHVPRM-06_ModelAwarePartitioning.md [MDLRGUP-MDLBHVPRM-IN06]` for the capacity, instruction following, and eagerness axes and decision MDLBHVPRM-DD-01 (observation overrides benchmarks)
- `_INFO_MDLBHVPRM-07_PromptFeedbackLoop.md [MDLRGUP-MDLBHVPRM-IN07]` for the checkpoint ledger that calibrates Items

**Supersedes:** `_INFO_HOW_TO_ORGANIZE_LLMS_BY_CAPABILITY_v1.md` (year-letter labels, ECI bands, WF, behavior profiles). Section 1 states why.

## Summary

- **Generation is an ordinal rung `G01`, `G02`, ... assigned once and never regraded**: a model gets the lowest rung consistent with the models it provably dominates; new models insert above, between, or level with existing ones; the ladder grows upward without a year anchor, comparison year, or May 1 wrap [ASSUMED - rule design, DD-10 option 3]
- **"Provably dominates" has four evidence kinds and two fallbacks**: `E1` vendor lineup tier within the same point version (Opus 5.5 > Sonnet 5.5 > Haiku 5.5), `E2` same-lineage successor is not below its predecessor (weak, allows ties), `E3` [Epoch Capabilities Index (ECI)](https://epoch.ai/eci) 95% confidence intervals do not overlap, `E4` documented in-house observation (TBLF, ledger, FAILS); fallbacks `E5` sibling tie and `E6` tier-offset estimate for models without a score. No edge = tie allowed. Benchmark noise cannot create an edge because overlapping intervals produce none [VERIFIED - mechanism tested on 92 models, LLMCAPCLS-IN01-SC-IPPS-LADDER]
- **The current inventory layers into 12 rungs with zero contradictions**: `G12` `claude-fable-5`, `claude-fable-5-1`, `claude-mythos-5`, `claude-mythos-5-1`; `G11` `gpt-6-astra`, `claude-opus-5-5`, `gpt-5.6-cyber`; `G10` `gpt-6.1-sol`, `gpt-6-sol`, `gpt-5.6-sol`, `gemini-4-argon`, `claude-sonnet-5-5`; `G06` `gpt-5`, `claude-opus-4-5`, `glm-5.2`; `G01` `gpt-4o`, `gpt-4o-mini`. 2024-2025 models span `G01`-`G08`, placed 2026 models `G04`-`G12` [TESTED - LLMCAPCLS-IN01-SC-IPPS-LADDER, registry 1.11.0 and Epoch snapshot 2026-10-28]
- **Every case the automatic edges cannot decide has a research mechanism with a named source type** (Section 2.6, EC-1 to EC-9): cross-version tier order from the vendor's model-selection guidance, superseded family members by inheritance, restricted twins by "same model" statements, specialized and unscored models by announcement and price order, squeezes and contradictions by in-house head-to-head tests. Silence = tie, never judgment [ASSUMED - rule design]
- **DD-11 closed: Fable 5 and Fable 5.1 are recorded above Opus 5.5**: Anthropic's [Fable 5.1 overview](https://platform.claude.com/docs/en/models/fable-5-1/overview) says "start with Claude Opus 5.5. Use Claude Fable 5.1 for demanding reasoning ... or when your evals on Claude Opus 5.5 at higher effort still don't meet your requirements"; the Opus 5.5 announcement claims parity "on most work" only. Fable 5 inherits the edge ("Fable 5.1 extends Fable 5", intervals overlap). Re-run: top `G12`, no cycle, no other rung moves [VERIFIED - LLMCAPCLS-IN01-SC-ANTH-FABLE51-OVW, LLMCAPCLS-IN01-SC-ANTH-OPUS55; TESTED - LLMCAPCLS-IN01-SC-IPPS-LADDER]
- **Prompt shape maps from the absolute rung, not from distance to the top**: explicitness level (`G01`-`G03` keystroke-level, `G04`-`G06` step-level, `G07`-`G09` outcome plus named files, `G10`+ goal-level) and Items default (4 / 5 / 6 / 8) are fixed per rung so a model's prompt recipe never changes when newer models arrive; `G10`+ covers every future top rung [ASSUMED - values are the former profile constants]
- **Items is the second axis and the only measured one**: largest `items_planned` completed with zero skips in `>= 3` ledger sequences overrides the default; `glm-5.2` completed 4-12 items per prompt at 100% with strict scope guard over 7 prompts in 2 sequences → provisional Items 8 against a `G06` default of 5. Over-eagerness sets `scope_guard: strict` in Notes and does not lower Items [VERIFIED - LLMCAPCLS-IN01-SC-IPPS-IN07, LLMCAPCLS-IN01-SC-IPPS-IN05 Section 9]
- **Effort shifts the effective rung**: Medium on adaptive-thinking models and Low on any model read one rung lower; no-reasoning models (`-` efforts) two rungs lower [VERIFIED - LLMCAPCLS-IN01-SC-TBLF-IN02: `claude-opus-4-6` M6 vs H667 rows, `gpt-5-mini` L65 vs M500, `gpt-4o` 4; rung sizes ASSUMED]
- **WF, Label, Comp, Profile, and the ECI band leave the inventory**: Human Work Hours (HWH) stay for cost and Agent Work Hours (AWH) only; prompt count = `max(ceil(expanded_items / Items), ceil(files / max_files), ceil(HWH / 1))` [ASSUMED - IN05 option c cap of 1 HWH per prompt]
- **Registry 1.12.0 carries `generation`, `generation_evidence`, `eci_ci`, `items`, `scope_guard`** (key names since 1.14.0, DD-23) and drops `capability_label`, `eci_band`, `eci_band_source`, `gen_equivalent`, `behavior_profile`; Gate 9.4 verifies that no existing `generation` changed between runs [ASSUMED - design, Section 5]
- **A `Value` column replaces `Devin cost` (DD-20, user decision VAL-01 option 1)**: score 1.0 (most expensive in the rung) to 5.0 (cheapest in the rung) on the log scale of the blended cost `0.8 * In USD + 0.2 * Out USD`, shown as stars plus number (`★★★★⯪ (4.4)`); computed over all Section 3.1 rows of the same rung (Section 5.6) [ASSUMED - rule design]
- **Devin cost multipliers are removed from the calculation and the JSON output (DD-21, user decision VAL-02)**: Devin no longer publishes them; `windsurf-model-registry.json` is no longer an inventory source; Devin prices come from the Devin models page instead (DD-22) [ASSUMED - consequence of the decision, Section 5.6]
- **Section 3.2 becomes "Devin Model Deviations" (DD-22, user decision DEV-01 option 1)**: it lists only Devin models that are absent from Section 3.1 or priced differently there; extracted from `https://docs.devin.ai/desktop/models` with a click on every tab in Prompt 3 and generated in Prompt 7, with no new prompt and no new canonical JSON (Section 5.7) [ASSUMED - rule design]
- **The rung is named Generation (DD-23, user decisions GEN-01 option 2, GEN-02 option 1, 2026-11-18)**: `Generation` replaces `Depth` as column name, label prefix (`G01`-`G13`, two digits, `*` for estimates), registry keys (`generation`, `generation_evidence`, `generation_estimated`, manual edges `higher_than`; registry 1.14.0), and script and file names (`layer-generation-ladder.py`, `[DATE]_Generation-Edges.json`, `[DATE]_GenerationLadder.log`); every rung value stays; history files keep the old names. Requirement: `_SPEC_MDLRGUP-MDLINVNTRY-01_GenerationLadder.md [MDLRGUP-MDLINVNTRY-SP01]` DD-12 [VERIFIED - registry key counts before and after, 2026-11-18]
- **A `Released` column before `Notes` holds the release date as `YYYY-MM-DD`, or `YYYY-MM` when the day is not known (DD-24, user request 2026-11-18)**: the day appears only when a vendor page, release note, or announcement prints it, never an Epoch date, run date, or family-head date as a stand-in; `release_date_assumed` is retired and the 46 registry dates that carried it became `YYYY-MM` (registry 1.15.0: 86 models with a day, 46 with a month); each DOM extract lists the dates its pages print in `released[]`, Prompt 5 reconciles them with the registry and researches the rest, Prompt 6 writes `release_date`, Prompt 7 prints the column in Sections 3.1 and 3.2; Gate 5.4 compares DOM and registry, Gate 9.4 registry and inventory (Section 5.8) [TESTED - gates PASS, 8 of 8 regression tests with month-only dates, DOM test with two injected conflicts; the 46 months themselves are ASSUMED until the next run re-reads the vendor pages]

## Table of Contents

1. [Why the Year-Letter Scheme Failed](#1-why-the-year-letter-scheme-failed)
2. [Generation Ladder](#2-generation-ladder)
3. [Ladder for the Current Inventory](#3-ladder-for-the-current-inventory)
4. [From Generation to Prompt Shape](#4-from-generation-to-prompt-shape)
5. [Producing MODEL_INVENTORY.md](#5-producing-model_inventorymd)
6. [Using the Inventory in Partitioned Documents](#6-using-the-inventory-in-partitioned-documents)
7. [HWH and AWH](#7-hwh-and-awh)
8. [Limitations](#8-limitations)
9. [Next Steps](#9-next-steps)
10. [Sources](#10-sources)
11. [Document History](#11-document-history)

## 1. Why the Year-Letter Scheme Failed

Version 1 of this document (2026-10-29) derived everything from one number: the [Epoch](https://epoch.ai/eci) ECI band. Letter `A`-`Z` = band relative to a year anchor, Comp = the same band against the comparison year, WF = `2.0 * 2^(-(170 - band) / 10)`, and a separate behavior profile. Applied to 92 models it produced orderings that contradict the vendors' own lineups [VERIFIED - LLMCAPCLS-IN01-SC-IPPS-MINV]:

- `claude-opus-5-5` (`26-A`) above `claude-fable-5` (`26-B`): a 4.9-point ECI difference with confidence intervals 160.5-168.2 and 165.3-174.0 decided a letter
- `claude-sonnet-5-5` level with `claude-fable-5` (both `26-B`); `claude-haiku-5-5` (`26-C`) above `claude-opus-4-6` (`26-D`)
- `gpt-5.6-luna` (Efficient tier) level with `gpt-5.4` and `claude-opus-4-6` (`26-D`)

Three causes:

- **ECI resolution is below the band width**: Epoch 95% confidence intervals are 4-9 points wide at the top of the index; a 5-point band reads noise as rank
- **Benchmark inflation rewards late release dates**: a September 2026 model scores higher than a June 2026 model of the same tier because the benchmark mix shifted, not because it reasons deeper. The year anchor and May 1 wrap were built to compensate and added two moving parts
- **WF carried false precision**: `2.0`, `1.5`, `0.75` HWH per prompt derived from a slope assumption; the ledger showed `glm-5.2` completing about 4.5 HWH in 8 prompts with 4-12 items each at 100%, where WF 0.5 predicted 9 prompts and the earlier WF 0.25 predicted 18

Requirement for the replacement: the number must be ordinal, assigned once, explainable by evidence a reader can check, and must never let a noisy score outrank a vendor tier.

## 2. Generation Ladder

### 2.1 Definition

`G` is an integer rung. `G01` is the lowest model in the inventory. Higher `G` = provably deeper reasoning. Rules:

- **Append-only**: a rung is assigned when a model is registered and never changes. New models insert above, between, or level with existing models
- **Unbounded**: there is no top constant; the top rung today is `G12` and rises when a model provably dominates a `G12` model
- **No year**: release date is an input to the evidence, not part of the ID. `gpt-5.2` (2025-12) and `gemini-3-flash-preview` (2025-12) are both `G07`; `gpt-5` (2025-08) is `G06`
- **Ties are expected**: two models without an edge between them may share a rung. Equal rung means equal prompt shape, not equal quality

### 2.2 Evidence Kinds

An edge `x > y` ("x dominates y") exists only with one of these:

- **E1 - vendor lineup tier** (strict): same provider, same point version, higher lineup class (`uc_class`, Universal Class: UC-1 Apex > UC-2 Flagship > UC-3 Balanced > UC-4 Efficient). `claude-opus-5-5 > claude-sonnet-5-5 > claude-haiku-5-5`; `gpt-5.6-sol > gpt-5.6-terra > gpt-5.6-luna`; `gpt-5.4-pro > gpt-5.4`. Across point versions (`claude-fable-5` vs `claude-opus-5-5`) E1 is not derived automatically because vendors use point versions differently: Anthropic's `5` → `5.5` is a refresh within five months, OpenAI's `gpt-5` → `gpt-5.6` spans 18 months and a full generation of progress (`gpt-5-pro` 150.6 vs `gpt-5.6-sol` 162.8 would contradict E3). A cross-version E1 edge is recorded from the vendor's model-selection guidance (Section 2.6 EC-1)
- **E2 - successor not below predecessor** (weak): same provider, same lineup class, same series, later release: `D(successor) >= D(predecessor)`. Allows a tie, forbids a regression. `gpt-6-sol >= gpt-5.6-sol`, `claude-opus-4-7 >= claude-opus-4-6`. Specialized models (`codex`, `cyber`, `deep-research`, `legal`, `non-reasoning`, `multi-agent`, `build`, vision `v`) have no E2 edges
- **E3 - benchmark separation** (strict): [Epoch ECI](https://epoch.ai/eci) 95% confidence intervals do not overlap: `ci_low(x) > ci_high(y)`. `claude-sonnet-5-5` [163.1-171.3] > `gpt-5.4-pro` [157.1-162.7]. `claude-opus-5-5` [165.3-174.0] vs `claude-fable-5` [160.5-168.2]: overlap, no edge
- **E4 - in-house observation** (strict): `TBLF-IN02` CSV limits, ledger sequences, FAILS entries naming both models under the same task. Overrides E3 when they conflict (MDLBHVPRM-DD-01). None recorded yet; Section 2.6 EC-7 names the test design
- **E5 - sibling tie**: a model without an Epoch score takes the rung of a same-provider, same-point-version, same-tier sibling that has one: `claude-mythos-5-1 = claude-fable-5-1`, `glm-5.3-flashx = glm-5.3-flash`

Sources per kind: E1 from `uc_class` in `model-registry.json`; E2 orders models by `release_date` (`YYYY-MM-DD` or `YYYY-MM`; a month-only date precedes only dates in a later month, DD-24); E3 from the Epoch CSV score and 95% interval as matched into `[DATE]_Epoch-ECI-Match.json` (`eci_score`, `eci_ci_low`, `eci_ci_high`; Section 10 LLMCAPCLS-IN01-SC-EPOCH-CSV); E4 and manual E1 from a `higher_than` list in the registry with a source reference.

### 2.3 Bootstrap Layering (once, 2026-11)

For the initial 92 models the rungs are solved together, not inserted one by one (insertion in release order produced 22 cascading conflicts because early models were placed before their evidence existed, LLMCAPCLS-IN01-SC-IPPS-LADDER first run):

```
D(x) = max( 1,
            max over strict-dominated y of D(y) + 1,     E1, E3, E4
            max over weak-dominated y of D(y),           E2
            D(sibling) for E5 ties )
iterated to a fixed point; a cycle (E1 against E3) aborts and is reported
```

Result: longest strict chain below each model. Fixed point reached in under 92 iterations, no cycle, no E1-E3 contradiction among 92 models [TESTED].

### 2.4 Online Insertion (every later model)

```
floor = same formula as 2.3 over existing rungs
cap   = min over strict dominators z of D(z) - 1, and min over weak dominators of D(z)
D(new) = floor                      if floor <= cap or no dominator
D(new) = cap, Notes "squeezed"      if floor > cap   (no free integer between neighbours)
```

Existing rungs never move. A squeezed model ties with the rung of the models it dominates; the Notes column records the dominator it should have been below. Squeezes occur mid-ladder (a new Efficient model between two frozen rungs), not at the top, where new models either dominate the current top or tie with it.

### 2.5 Worked Derivations

```
  gpt-4o          G01  bottom (nothing dominated)
  o1-mini         G02  E3 > gpt-4o            [132.4-137.2] clears [124.6-131.2]
  gpt-4.1-mini    G02  E3 > gpt-4o-mini
  gpt-4.1         G03  E1 > gpt-4.1-mini      ([133.6-138.3] overlaps o1-mini; the tier edge lifts it)
  o1              G04  E3 > gpt-4.1           [139.7-142.9] clears 138.3
  gpt-5-mini      G05  E3 > o1                [143.3-147.1] clears 142.9
  gpt-5           G06  E1 > gpt-5-mini        (score 150.0 but no interval in the snapshot, so no E3
                                               edges; the tier edge over its own mini carries the
                                               benchmark evidence upward)
  gpt-5-pro       G07  E1 > gpt-5
  gpt-5.4-pro     G09  E1 > gpt-5.4 (G08, E3 > gemini-3-flash-preview G07)
  claude-sonnet-5-5 G10 E3 > gpt-5.4-pro
  claude-opus-5-5 G11  E1 > claude-sonnet-5-5
  claude-fable-5-1 G12 E1 > claude-opus-5-5 (manual, vendor guidance, Section 2.6 EC-1)
  claude-fable-5  G12  E1 > claude-opus-5-5 (inherited, EC-2); automatic edges alone gave G10
```

The `gpt-5` line shows why tier edges matter: the snapshot carries a score but no interval for `gpt-5`, so on benchmarks alone it would sit at the bottom; its own `mini` has an interval that clears `o1`, and E1 propagates that upward.

### 2.6 Edge Cases and Resolution Mechanisms

Every case the automatic edges cannot decide has one research step with a named source type. The result is recorded in the registry (`higher_than` entry with URL and access date, or a Notes line) before the layering script runs. No case is resolved by judgment without a citable statement; when the named source is silent, the outcome is a tie.

- **EC-1 Tier order across point versions** (`claude-fable-5-1` vs `claude-opus-5-5`)
  - Source: the vendor's current model-selection guidance in its platform documentation (Anthropic model overview "Choosing a model", OpenAI models page, Google model table)
  - Rule: an escalation statement ("start with X; use Y when X at higher effort still falls short", "Y for the most demanding reasoning") = E1 edge `Y > X`. A parity statement alone ("performs at the level of") or silence = tie
  - Resolved 2026-11-02: the [Fable 5.1 overview](https://platform.claude.com/docs/en/models/fable-5-1/overview) states "For most workloads, start with Claude Opus 5.5. Use Claude Fable 5.1 for demanding reasoning and long-horizon agentic work, or when your evals on Claude Opus 5.5 at higher effort still don't meet your requirements"; the [Opus 5.5 announcement](https://www.anthropic.com/news/claude-opus-5-5) states "performs at the level of Claude Fable 5.1 on most work" and "the gap between Opus 5.5 and Claude Fable 5.1 is narrower than these scores suggest". Generation measures the demanding-reasoning end, so the escalation statement decides: `claude-fable-5-1 > claude-opus-5-5` (E1) [VERIFIED - LLMCAPCLS-IN01-SC-ANTH-FABLE51-OVW, LLMCAPCLS-IN01-SC-ANTH-OPUS55]
- **EC-2 Superseded member of a tier family** (`claude-fable-5` when the guidance names only Fable 5.1)
  - Source: the successor's "what's new" or migration page stating that it "extends" or "succeeds" the predecessor at the same tier and price
  - Rule: an edge recorded for the latest family member is inherited by earlier members of the same generation unless E3 contradicts it (predecessor interval entirely below the target's)
  - Resolved 2026-11-02: "Claude Fable 5.1 extends Claude Fable 5 at the same input and output prices" ([what's new](https://platform.claude.com/docs/en/models/fable-5-1/whats-new-fable-5-1.md)); `claude-fable-5` [160.5-168.2] vs `claude-opus-5-5` [165.3-174.0] overlap → `claude-fable-5 > claude-opus-5-5` (E1, inherited) [VERIFIED - LLMCAPCLS-IN01-SC-ANTH-FABLE51-NEW]
- **EC-3 Restricted-access twin** (`claude-mythos-5`, `claude-mythos-5-1`)
  - Source: vendor statement "same underlying model" or "same capabilities"
  - Rule: E5 tie with the general-access twin
  - Resolved: Mythos 5 "is the same underlying model as Fable 5, but with the safeguards lifted in some areas" ([Fable 5 announcement](https://www.anthropic.com/news/claude-fable-5-mythos-5)); Mythos 5.1 "Same capabilities as Claude Fable 5.1" (what's new) [VERIFIED - LLMCAPCLS-IN01-SC-ANTH-FABLE5, LLMCAPCLS-IN01-SC-ANTH-FABLE51-NEW]
- **EC-4 Specialized Apex model without a score** (`gpt-5.6-cyber`, `gpt-5.5-cyber`, `o3-deep-research`, `o1-pro`, `o4-mini-deep-research`)
  - Source: the vendor announcement of the specialized model naming its base and its positioning ("a version of X for Y", "our most capable X")
  - Rule: E1 over the base when the vendor presents it as more capable and prices it higher; E5 tie with the base when it is presented as a domain variant at equal price
  - Status: the ladder applies E1 from `uc_class` and price order; the announcement statements are not yet cited in `higher_than` [ASSUMED until each page is read during the registry 1.12.0 run]
- **EC-5 Unscored Efficient or vision model** (`glm-4.7-flash`, `glm-4.6v`, `grok-4.20-0309-non-reasoning`)
  - Source: vendor model page tier wording (`flash`, `lite`, `air`, `non-reasoning`) and price order within the point version
  - Rule: E6 tier offset from the scored sibling, marked `*`; replaced by E3 when Epoch publishes an interval
- **EC-6 Model outside the registry** (Devin-only rows, Section 3.1)
  - Source: vendor comparison statement ("still trails X"), routing notice (Gemini API changelog), or base-model lineage statement
  - Rule: `*` rung one below the named reference, or equal to the routed target
- **EC-7 Squeeze on insertion**
  - Source: in-house head-to-head test naming both models on the same task (`TBLF-IN02` design: same prompt, `n >= 3`, confirmed limit), or ledger sequences on the same TASKS document
  - Rule: E4 edge from the result; until then Notes `squeezed by X`. Not occurred
- **EC-8 E1 against E3 contradiction**
  - Source: re-read `uc_class` on the vendor model page
  - Rule: if the class is wrong, fix it and re-layer; if it is right, E1 wins (the lineup is the vendor's stated rung order; benchmark mix is the noise described in Section 1) and the E3 edge is dropped with a Notes line. Not occurred in 92 models
- **EC-9 Wrong registry input** (release date, class)
  - Source: the vendor model overview "Released" field, never an aggregator
  - Found 2026-11-02: `claude-fable-5-1` released 2026-09-01 (registry 2026-09-25); `claude-opus-5-5` announced 2026-09-22 (registry 2026-10-14) [VERIFIED - LLMCAPCLS-IN01-SC-ANTH-FABLE51-OVW, LLMCAPCLS-IN01-SC-ANTH-OPUS55]. Neither changes a rung; both go to PROBLEMS for the 1.12.0 run

Effect of EC-1 to EC-3 on the ladder, re-run with `.tmp_manual_edges.json` (`.tmp_ladder_dd11.json`): top `G12`, no cycle, 0 contradictions; `claude-fable-5`, `claude-fable-5-1`, `claude-mythos-5`, `claude-mythos-5-1` at `G12`; `claude-opus-5-5` stays `G11`; no other rung changes [TESTED - LLMCAPCLS-IN01-SC-IPPS-LADDER]. DD-11 is closed with this result.

### 2.7 Models without Evidence

A model with no Epoch score, no scored same-tier sibling, and no predecessor sits at `G01` by the formula, which reads as "lowest" when it means "unplaced". Rule E6 fills the gap with a marked estimate:

- **E6 - tier offset estimate** (`*`): same provider, same point version, scored sibling of a different tier: `G(new) = G(sibling) - (tier(new) - tier(sibling))`, floor `G01`. The rung carries `*` in the inventory and `generation_estimated: true` in the registry; it is replaced by the evidence-based rung when Epoch publishes a score or a ledger observation arrives (the only case in which a rung changes)
- No sibling at all: `G01*` with Notes `unplaced`. Today: `glm-4-air`, `grok-build-0.1`

## 3. Ladder for the Current Inventory

Computed by `.tmp_dominance_ladder.py` from `model-registry.json` 1.11.0 (`uc_class`, `release_date`) and the Epoch snapshot of 2026-10-28 (`eci_score`, `eci_ci_low`, `eci_ci_high`) [TESTED - LLMCAPCLS-IN01-SC-IPPS-LADDER]. 92 API rows (every text model except `retired`), 12 rungs with the Section 2.6 manual edges (`.tmp_manual_edges.json`), no cycle, no E1-E3 contradiction. E6 estimates (`*`) were derived by hand from the computed rungs and are not yet in the script output. In parentheses: the evidence that set the rung.

- **G12** (4): `claude-fable-5-1` (E1 manual > `claude-opus-5-5`, EC-1), `claude-fable-5` (E1 inherited > `claude-opus-5-5`, EC-2), `claude-mythos-5` (E5 = `claude-fable-5`), `claude-mythos-5-1` (E2 >= `claude-mythos-5`)
- **G11** (3): `gpt-6-astra` (E1 > `gpt-6-sol`), `claude-opus-5-5` (E1 > `claude-sonnet-5-5`), `gpt-5.6-cyber` (E1 > `gpt-5.6-sol`; no Epoch score)
- **G10** (7): `claude-sonnet-5-5` (E3 > `gpt-5.4-pro`), `gpt-6.1-sol` (E3 > `gpt-5.4-pro`), `gpt-6-sol` (E2 >= `gpt-5.6-sol`), `gpt-5.6-sol` (E1 > `gpt-5.6-terra`), `gpt-5.5-pro`, `gpt-5.5-cyber` (E1 > `gpt-5.5`), `gemini-4-argon` (E3 > `gpt-5.4-pro`)
- **G09** (5): `claude-opus-5` (E3 > `gpt-5.2-pro`), `gpt-5.5` (E3 > `grok-4.7`), `gpt-5.4-pro` (E1 > `gpt-5.4`), `gpt-5.6-terra` (E1 > `gpt-5.6-luna`), `gpt-6.1-terra` (E2 >= `gpt-5.6-terra`; no Epoch score)
- **G08** (13): `claude-opus-4-8` (E3 > `gpt-5.2`), `claude-opus-4-7`, `claude-opus-4-6`, `claude-sonnet-5`, `gpt-5.4`, `gpt-5.6-luna`, `gpt-6-luna`, `grok-4.6`, `glm-5.3`, `gemini-3.8-flash` (E3 > `gemini-3-flash-preview`), `claude-haiku-5-5` (E3 > `gpt-5.2`), `gpt-5.2-pro` (E1 > `gpt-5.2`), `grok-4.7` (E2 >= `grok-4.6`)
- **G07** (11): `gpt-5.2`, `gpt-5.3-codex`, `gemini-3-flash-preview`, `gemini-3.1-pro-preview`, `gemini-3.6-flash`, `claude-sonnet-4-6`, `grok-4.5`, `glm-5.3-flash` (E3 > `o3-pro`), `glm-5.3-flashx`, `glm-5.3-flashx-legal` (E5), `gpt-5-pro` (E1 > `gpt-5`)
- **G06** (11): `gpt-5` (E1 > `gpt-5-mini`), `gpt-5.1`, `claude-opus-4-5`, `glm-5.1`, `glm-5.2`, `gpt-5.4-mini`, `grok-4.3`, `grok-4.20-0309-reasoning`, `grok-4.20-multi-agent-0309` (E3 > `gemini-2.5-pro`), `o3-pro`, `o3-deep-research` (E1 > `o3`)
- **G05** (8 + 1 estimated): `gemini-2.5-pro`, `o3`, `gpt-5-mini`, `claude-sonnet-4-5`, `glm-5`, `gpt-5.4-nano` (E3 > `o1`), `o1-pro` (E1 > `o1`), `o4-mini-deep-research` (E1 > `o4-mini`), `grok-4.20-0309-non-reasoning` (`G05*`, E6 from `grok-4.20-0309-reasoning` G06)
- **G04** (7): `o1` (E3 > `gpt-4.1`), `o4-mini` (E3 > `o3-mini`), `gemini-2.5-flash`, `claude-haiku-4-5`, `glm-4.7` (E3 > `gpt-4.1`), `gemini-3.1-flash-lite`, `gemini-3.5-flash-lite` (E3 > `o3-mini`)
- **G03** (5): `gpt-4.1` (E1 > `gpt-4.1-mini`), `o3-mini` (E3 > `gpt-4.1-mini`), `glm-4.5`, `glm-4.5-x` (E1 > `glm-4.5-airx`), `glm-4.6` (E2 >= `glm-4.5-x`)
- **G02** (7 + 3 estimated): `o1-mini` (E3 > `gpt-4o`), `claude-3-5-sonnet`, `gpt-4.1-mini`, `gemini-2.5-flash-lite` (E3 > `gpt-4o-mini`), `gpt-5-nano` (E3 > `gpt-4o`), `glm-4.5-airx`, `glm-4.5v` (E1 > `glm-4.5-flash`), `glm-4.7-flash`, `glm-4.7-flashx` (`G02*`, E6 from `glm-4.7` G04), `glm-4.6v` (`G02*`, E6 from `glm-4.6` G03)
- **G01** (4 + 3 estimated): `gpt-4o`, `gpt-4o-2024-05-13`, `gpt-4o-mini`, `gpt-4.1-nano` (Epoch 129.5, interval overlaps `gpt-4o-mini`), `glm-4.5-flash` (`G01*`, E6 from `glm-4.5` G03, floor), `glm-4-air`, `grok-build-0.1` (`G01*`, unplaced)

Observations:

- **Vendor tiers hold everywhere**: Fable > Opus > Sonnet > Haiku across the Claude 5 generation; Astra > Sol > Luna; Pro > base; every provider's Efficient model sits below its Flagship of the same point version. The letter scheme violated four of these
- **Cross-vendor ties reflect the evidence**: `G10` holds OpenAI and Google Flagship models and Anthropic's Balanced model whose intervals overlap; `G11` holds `gpt-6-astra` and `claude-opus-5-5` (168.8 each); no public evidence separates them
- **Specialized Apex models inherit the top of their point version**: `gpt-5.6-cyber` and `gpt-5.5-cyber` have no Epoch score and get their rung from E1 over the Flagship sibling. The rung states vendor positioning, not measured depth; Notes says so
- **`gpt-4.1-nano` is measured, not unplaced**: Epoch 129.5 with an interval overlapping `gpt-4o-mini` keeps it at `G01`; the 2025 release date does not lift it
- **Compared with the sketch proposed in the DD-10 discussion** (`gpt-4o-mini` 2, `gpt-4o` 3, `o1-mini` = `claude-3-5-sonnet` 4, `gpt-4.1` 4, `gpt-4.1-mini` 3, `gpt-4.1-nano` 2, `gpt-5` 5, `gpt-5-mini` 4, `gpt-5-nano` 3): the computed ladder is one rung lower at the bottom (`gpt-4o-mini` and `gpt-4o` tie at `G01` because their intervals overlap) and otherwise reproduces the order, with `gpt-5` one rung above `gpt-5-mini` above `gpt-5-nano`

### 3.1 Devin-Only Models

No registry entry, no Epoch row. Rungs set by hand in `MODEL_INVENTORY.md` Section 3.2 from the vendor's own positioning [ASSUMED]; Devin no longer publishes cost multipliers (DD-21); from DD-22 on, Section 3.2 is generated from the Devin models page (Section 5.7) and these four hand-set rows are replaced by it. Rungs below are the last hand-set state (2026-11-17):

- `Kimi K3` - `G09*`: [Moonshot](https://www.kimi.ai/blog/kimi-k3) states it "still trails" `claude-fable-5` (G12) and `gpt-5.6-sol` (G10); one below the lower reference [VERIFIED - LLMCAPCLS-IN01-SC-KIMI-K3]
- `Gemini 3.7 Flash` - `G08*`: the [Gemini API changelog](https://ai.google.dev/gemini-api/docs/changelog) routes it to `gemini-3.8-flash` (G08) since 2026-10-08 [VERIFIED - LLMCAPCLS-IN01-SC-GOOG-APICHG]
- `Gemini 3.5 Flash` - `G07*`: routed to `gemini-3.6-flash` (G07) [VERIFIED - LLMCAPCLS-IN01-SC-GOOG-APICHG]
- `SWE-1.7` - `G06*`: [Cognition](https://www.linkedin.com/posts/jefflinwang_weve-released-swe-17-our-best-model-yet-activity-7480867805618438146-J56D) states it is trained from Kimi K2.7, a 2025-2026 Flagship-class base [VERIFIED - LLMCAPCLS-IN01-SC-COG-SWE17; rung ASSUMED]

Devin models page snapshot 2026-11-18 (Section 5.7): `Gemini 3.7 Flash` and `Gemini 3.5 Flash` are no longer listed, `Kimi K3` is now a registry model (`kimi-k3`), `SWE-1.7` appears only in prose without a price. The new Devin-only models are `Adaptive`, `SWE-2 Flash`, and `SWE-2`; no listed model has a deviating price.

## 4. From Generation to Prompt Shape

Generation answers "how much may stay implicit"; Items answers "how many explicit instructions survive one run". Both are read from the inventory row; the prompt-writing agent computes nothing else.

```
  Inventory row ──> Generation ──> effort shift ──> effective rung ──> explicitness level ──> items per unit
                └─> Items ──────────────────────────────────────────────────────────────────> prompt count
                └─> Notes: scope guard, CSV rows, adaptive Medium warning ────────────────────> prompt text
```

### 4.1 Explicitness Level per Rung

Fixed per absolute rung. A model's recipe does not change when higher-rung models arrive, because the model did not change. Boundaries [ASSUMED], calibrated by ledger Items (Section 4.3):

- **G10 and above - goal-level**: state outcome, constraints, acceptance check. The model finds files and infers steps. Several reasoning units per prompt
- **G07-G09 - outcome-level**: outcome per unit plus named files plus acceptance check. The model infers steps inside the named files. This is the granularity TASKS items are written at (TASKS_GUIDES Section 3), so one unit = one item
- **G04-G06 - step-level**: each edit named (file, location, change) and expected output stated. One reasoning unit per prompt; no cross-file inference expected. One unit expands to 2-3 items
- **G01-G03 - keystroke-level**: exact old and new text or exact command, exact verification command, nothing implicit, no rationale text. One unit expands to 4-6 items

Expansion factors are writing heuristics: an outcome-level item "add retry with backoff to the three fetch calls in `client.py`" becomes three step-level items (one per call, each with the expected signature) or six keystroke-level items (old text, new text per call).

### 4.2 Effort Shift

The rung describes High effort (`H`). Other efforts read the model as a lower rung before applying Section 4.1 [sizes ASSUMED; direction VERIFIED - LLMCAPCLS-IN01-SC-TBLF-IN02]:

- `X`, `MX`: no shift (no evidence that XHigh or Max completes more items than High; cost rises)
- `M`: no shift, except `adaptive_thinking` prefixes (Claude 4.6 and later): one rung lower. `TBLF-IN02`: `claude-opus-4-6` 6 rows at Medium against 667 at High; `TBLF-IN03` E1 traces it to adaptive thinking skipping the reasoning phase
- `L`: one rung lower. `gpt-5-mini` 65 rows at Low against 500 at Medium
- `-` (no reasoning): two rungs lower. `gpt-4o` 4 rows, `gpt-4o-mini` 6, `claude-haiku-4-5` without thinking 9

Example: `claude-opus-5` (G09) at Medium reads as G08 (still outcome-level); `claude-haiku-5-5` (G08) at Medium reads as G07; `gpt-4.1` (G03, `-`) reads as D1.

### 4.3 Items and Shape Parameters

**Items** = numbered instruction items per implementation prompt that complete with zero skips.

- **Measured** (preferred): largest `items_planned` with `items_done == items_planned` over `>= 3` sequences in `partition-observations.jsonl`, aggregated by `/session-finalize` into `observed.items` (IN07 Sections 6-7) [VERIFIED - LLMCAPCLS-IN01-SC-IPPS-IN07]. `glm-5.2`: 7 prompts in 2 sequences, 4-12 items, 100% done with strict scope guard → provisional Items 8 until a third sequence is logged [VERIFIED - LLMCAPCLS-IN01-SC-IPPS-IN05 Section 9]
- **Default** until measured, from the effective rung: `G10+` 8, `G07-G09` 6, `G04-G06` 5, `G01-G03` 4 [ASSUMED - the former profile constants]
- **Shape parameters** keyed to Items, not to a profile name: Items 8 → max_files 6, checkpoint every 3 prompts; Items 6 → max_files 3, checkpoint every 2; Items 5 or less → max_files 2, checkpoint after every prompt [ASSUMED - IN06 Section 4]
- **Scope guard**: Notes `scope guard strict` when a FAILS or ledger entry documents unrequested actions (`glm-5.2`, OverAct SIR 2.00, IN06 Section 3 [VERIFIED - LLMCAPCLS-IN01-SC-IPPS-IN06]). Adds "Do ONLY the numbered items below. Do not refactor, rename, add tests, or touch files not listed. Report any item you could not complete as NOT DONE" to every prompt. Does not lower Items: the `glm-5.2` ledger shows 100% completion with the guard in place

Measured Items override the default in both directions; a skip observation (`items_done < items_planned`) with `sequences >= 3` lowers Items to the largest fully completed `items_planned`. Items never changes the rung: completion capacity and generation are separate axes (IN06 Section 2: GLM-5.2 at High still skipped items before the guard, so effort and generation did not fix it).

### 4.4 Partition Formula

```
expanded_items = sum over units of items_per_unit(effective rung)      Section 4.1
prompt_count   = max( ceil(expanded_items / Items),
                      ceil(total_files / max_files),
                      ceil(task_HWH / 1) )                              1 HWH per prompt cap [ASSUMED - IN05 option c]
checkpoints    = floor((prompt_count - 1) / checkpoint_interval) + Final Checkpoint
context fit    = input read per prompt <= 50% of Context                [VERIFIED for <= 2025 models - LLMCAPCLS-IN01-SC-RULER; ASSUMED for 1M windows]
cost           = (0.8 * In USD + 0.2 * Out USD) * tokens_per_prompt / 1M * prompt_count
```

HWH stays as the task-size unit (Section 7) and caps prompt size; it no longer divides by a model factor. If `prompt_count` exceeds the chain length limit (PRMT-SC-04), split into sub-chains.

### 4.5 Worked Example

Task: 3 HWH, 18 outcome-level units, 7 files, High effort.

- **`claude-opus-5`** (G09 outcome-level, Items 6 default, max_files 3): expanded 18; `max(ceil(18/6), ceil(7/3), 3)` = 3 prompts; checkpoint after prompt 2, then Final Checkpoint; about $9 per 1M-token prompt → $27
- **`gpt-5.6-luna`** (G08 outcome-level, Items 6 default): same shape, 3 prompts; $0.40 per prompt → $1.20. Same prompt count as Opus 5 is the expected result of equal explicitness level; what differs is the risk that G08 fails an inference G09 would make, visible only in the ledger
- **`glm-5.2`** (G06 step-level, Items 8 provisional measured, max_files 6, scope guard strict): expanded 18 × 2.5 = 45; `max(ceil(45/8), ceil(7/6), 3)` = 6 prompts; checkpoint every 3; $2.00 per prompt → $12
- **`claude-haiku-4-5`** (G04 step-level, Items 5 default, max_files 2): expanded 45; `max(9, 4, 3)` = 9 prompts, checkpoint after every prompt; $1.80 per prompt → $16

The former formula gave `glm-5.2` 6 prompts from WF 0.5 (capacity) and Opus 5 3 prompts from items; the new formula reaches the same counts from explicitness and measured Items, without a model-specific HWH factor.

## 5. Producing MODEL_INVENTORY.md

Proposed changes; nothing below is applied yet. `MODEL_INVENTORY.md` stays a generated, data-only view of the registries (GRUC separation); agents never compute rungs or Items themselves.

```
  model-registry.json ─────────┐  uc_class, release_date, eci_score, eci_ci,
  model-pricing.json ──────────┤  higher_than, generation, generation_evidence, items,
  model-parameter-mapping.json ┤  scope_guard, observed, effort levels, context
  [DATE]_Devin-Models-DOM.json ┘  Devin Model Deviations (DD-22, run folder)
              │
              v  layer-generation-ladder.py (insert-only)  ──>  update-model-inventory.py
  MODEL_INVENTORY.md ──> /write-tasks-plan, /write-strut, /write-prompts, /verify
              ^
              │  /session-finalize: ledger → registry.observed → items, scope_guard review
  _agentwork/partition-observations.jsonl  <── Final Checkpoint of every prompts file
```

### 5.1 Registry Properties (1.12.0)

Per `model-registry.json` model entry:

- Keep: `uc_class` (E1 input), `release_date` (`YYYY-MM-DD` or `YYYY-MM`, DD-24), `eci_score`, `observed`, `status`, `enabled`, `context_window`
- Add: `eci_ci` `[low, high]` from the Epoch CSV (E3 input); `generation` integer, written once by the layering script; `generation_evidence` string (`"E3 > gpt-5.4-pro"`, `"E1 > claude-sonnet-5-5"`, `"E6 from glm-4.7"`); `generation_estimated: true` for E6 rungs; `higher_than` list of `{model, kind, source, accessed, statement}` for manual E1 and E4 edges (Section 2.6); `items` integer or `null` (measured, from `observed`); `scope_guard: "strict"` where documented
- Remove: `capability_label`, `eci_band`, `eci_band_source`, `gen_equivalent`, `behavior_profile`, `capability_note` (evidence moves to `generation_evidence` and `higher_than`); since 1.15.0 also `release_date_assumed` (DD-24)
- `observed` gains `items` (largest fully completed `items_planned`) next to the existing `if`, `eg`, `sequences`, `self_audited_prompts`; `profile_suggested` is dropped

### 5.2 Inventory Structure and Columns

Sections of `MODEL_INVENTORY.md`:
1. Definitions - Generation, Items, HWH, context; one line each
2. Value Derivation - evidence kinds E1-E6 (one line each), insertion rule, effort shift, Items default and shape parameters, scope guard, prices. About 15 lines against the current 40 (anchor, letters, Comp, WF formula, profile thresholds, change rule gone)
3. Model table, header line `Top rung: G12 (2026-11-02)`, 3.1 API models, 3.2 Devin Model Deviations (DD-22)
4. Maintenance - script regeneration, insert-only guarantee, Items and scope guard review, manual edge review

Columns: `Model | Generation | ECI Score | Items | Context | Efforts | In USD | Cache USD | Out USD | Value | Released | Notes` (`Value` replaces `Devin cost`, DD-20; `ECI Score` was added in the 2026-11-17 inventory; `Released` was added on 2026-11-18, DD-24)

- **Generation** - `G11`, `G02*` (estimated). Never changes except `*` → measured
- **Items** - measured values carry `m` (`8m`); defaults per Section 4.3 carry no marker
- **Value** - price score within the rung, `★★★★⯪ (4.4)`; `-` when the rung has one model, all models cost the same, or the row has no price (Section 5.6)
- **Released** - `YYYY-MM-DD` or `YYYY-MM` (day unknown), the registry `release_date` as stored; `-` only for a Devin-only row without a source date (Section 5.8)
- **Notes** - `generation_evidence`; `UC-n`; Epoch score with interval (`168.8 [165.3-174.0]`) or `no Epoch score`; status `legacy` / `deprecated` / `no_access`; `scope guard strict`; `CSV rows` marker; adaptive-thinking Medium warning; `unplaced`
- Removed: `Label`, `Comp YY`, `Profile`, `WF`

Sort: Generation descending, then Model ascending. Prompts files cite `Generation` and `Items`; both are stable.

### 5.3 Scripts

- **`layer-generation-ladder.py`** (new, from `_agentwork/.tmp_dominance_ladder.py`): reads registry and the run's Epoch match file; builds E1, E2, E3, E5 edges plus manual `higher_than`; for models with `generation` present it verifies the stored rung is still consistent (reports, never rewrites); for models without `generation` it applies the online insertion rule (Section 2.4) and writes `generation`, `generation_evidence`, `generation_estimated`; applies E6 for unscored models; aborts on a cycle and names the two edges. `--bootstrap` performs the one-time Section 2.3 layering and is refused when any `generation` exists. A month-only `release_date` is a predecessor only of dates in a later month (Section 5.8)
- **`match-epoch-eci.py`**: keeps download and name matching; outputs `eci_score`, `eci_ci_low`, `eci_ci_high`; drops `eci_band`, `band_action`, `gen_equivalent`, and the UC inference (`uc_class` is human-set in the registry; the script lists new models whose `uc_class` is missing); reads `released[]` of the run's DOM extracts into `released_in_dom`, `new_model_releases{}`, and `release_conflicts[]` (Section 5.8)
- **`update-model-inventory.py`**: removes `anchor`, `letter_index`, `label_from`, WF formula, profile and Comp columns; reads `generation`, `items`, `scope_guard`; renders the header `Top rung`; keeps `CSV rows` and adaptive Medium markers and price columns; computes `Value` (Section 5.6) for Section 3.1 rows; generates Section 3.2 from the run's Devin DOM file (Section 5.7) and keeps the existing Section 3.2 rows when no Devin DOM file is given; no longer reads Devin multipliers; prints `release_date` as `Released` in both tables and stops on a value that is neither `YYYY-MM-DD` nor `YYYY-MM`
- **`verify-and-distribute-registry.ps1` Gate 9.4**: every text model not `retired` has `generation`; no `generation` differs from the previous committed registry except `generation_estimated` → measured; every `higher_than` entry has a source; inventory sort order; `Top rung` equals max `generation`; header matches the new column list; every `Value` cell equals the recomputation from the registry prices (Section 5.6); every `Released` cell equals the registry `release_date`; every Section 3.2 row is absent from Section 3.1 or priced differently there (Section 5.7); Gate 5.4 (in the Gate 5-7 run) requires every `release_date` to be `YYYY-MM-DD` or `YYYY-MM`, forbids `release_date_assumed`, and compares the DOM `released[]` values with the registry; Gate 2 requires `[DATE]_Devin-Models-DOM.json` for `FULL` and `PRICES` runs

### 5.4 Template Changes (`_PROMPTS_ModelInventoryUpdate_TEMPLATE.md`)

- Header: `[CAPABILITY_SCHEME]` values `LADDER | NONE` (was `UC_ECI | YY_L | NONE`); script list entries for `match-epoch-eci.py` and `update-model-inventory.py` reworded; new `layer-generation-ladder.py` entry; Prompt 4 and Prompt 6 descriptions in the load-based partition table
- Prompt 4: title "Capability Evidence: Epoch ECI scores and intervals"; item 2 appends `eci_score`, `eci_ci_low`, `eci_ci_high` for new models; item 3 verifies intervals present or `fallback_note`; the band-freeze sentence (R2) is removed
- Prompt 5 item 2: capability fields incorporated from the match file are `eci_score`, `eci_ci`; `uc_class` and `release_date` are set by hand for new models with the provider page as source
- Prompt 6 item 2 (Phase 9.4) becomes: 1) `release_date` and `uc_class` for new models, 2) run `layer-generation-ladder.py` (insert-only), 3) review reported squeezes and manual-edge candidates, 4) `items` and `scope_guard` from `observed` review, 5) `format-model-registry.py`, 6) `update-model-inventory.py`. The May 1 wrap bullet is removed. Columns and sort order updated
- Prompt 6 item 3: Gate 9.4 description per Section 5.3
- Example block comments: `UC_ECI` → `LADDER`
- Script list entry and Prompt 6 item 2 (inventory regeneration): column list `... | Out USD | Value | Notes`, `Value` rule from Section 5.6, no Devin multiplier
- Devin integration (DD-22, option 1): Prompt 3 gains the Devin extraction step (`DV1`) and `Devin` joins part B and `[TARGET_PROVIDERS]`; Prompt 7 gains the deviation inputs and the Section 3.2 generation; Prompt count stays 9; Section 5.7
- Released column (DD-24): field semantics define `release_date` and the `released[]` flow; Prompts 2 and 3 write `released[]` into every DOM file and verify it; Prompt 5 reconciles it and writes `release_corrections[]`; Prompt 6 writes `release_date` and runs Gate 5.4; Prompt 7 adds the column to both tables and `devin_only[].release_date`; script list, Gate lists, and Prompt 9 Verify name Gate 5.4; Section 5.8

### 5.5 Consumers

Documents that read the inventory and currently name Label, Comp, Profile, or WF:

- `PROMPTS_GUIDES.md` Section 1c (WF paragraph), 1f step 3 (budget = Items and 1 HWH cap), 1g (rewritten as Section 4 of this document), Section 5 (`max_items` → Items)
- `TASKS_GUIDES.md` Section 1 (default row: `G07-G09`, Items 6), Section 3 (`Est <= WF` → `Est <= 1 HWH`, expanded items `<= Items`, files `<= max_files`), Sections 5-6
- `PROMPTS_RULES.md` PRMT-SC-05: commentary states Generation, effective rung after effort shift, explicitness level, Items, prompt count, cost; strict guard check keyed to Notes
- `write-prompts.md` Step 1, `edird-phase-planning` SKILL.md step sizing, `PROMPTS_TEMPLATE.md` and `PROMPTS_EXAMPLE_01` commentary rows
- `NOTES.md` of this session: DD-01 (`UC_ECI`) superseded by DD-10 option 3; DD-02 (fixed caps) and DD-03 (drop profiles) absorbed; T02 `IN01` Section 5 decisions updated

### 5.6 Value Score (DD-20, DD-21)

Goal: one cell that tells a prompt-writing agent how cheap a model is compared with the models that have the same prompt shape. Replaces `Devin cost`. Computed by `update-model-inventory.py`, never by hand.

- **Cost**: `cost = 0.8 * In USD + 0.2 * Out USD` (the blend of `MODEL_INVENTORY.md` Section 2); cache price and long-context tiers are ignored; free models use the floor `0.01`
- **Peer group**: all Section 3.1 rows with the same rung number; `G08*` and `G08` are one group
- **Score**: `Value = 1 + 4 * (ln(max_cost) - ln(cost)) / (ln(max_cost) - ln(min_cost))`; the most expensive peer scores 1.0, the cheapest 5.0. Log scale because prices inside one rung differ by up to 280x (`G08`: `0.18` to `50.40`), where a linear scale would give almost every model 5.0
- **Display**: nearest 0.5 (round half up) drawn as five symbols, `★` full, `⯪` half, `☆` empty, followed by the one-decimal score: `★★★★⯪ (4.4)`. The user's example `★★★⯪☆ (4.4)` shows 3.5 stars for 4.4; the rule follows the number [ASSUMED - example read as format illustration]
- **No score**: `-` when the rung has one model, when `max_cost = min_cost`, or when the row has no price; Section 3.2 has no `Value` column
- **Insertion effect**: a new model that sets a new minimum or maximum cost in its rung changes the other `Value` cells of that rung; `Value` is a generated column and is the one allowed exception to the append-only rule that applies to `generation`
- **Not a quality score**: Value compares price only. Generation sets the prompt shape, Value says which model of equal shape costs least; ECI differences inside a rung are not part of it
- **Example** (`G08`, 2026-11-17 inventory, min `0.18` `claude-haiku-5-5` and `gpt-6-luna`, max `50.40` `gpt-5.2-pro`): `gpt-5.6-luna` cost `0.40` → `1 + 4 * ln(126) / ln(280)` = 4.4 → `★★★★⯪ (4.4)`; `gpt-5.4` cost `5.00` → 2.6 → `★★⯪☆☆ (2.6)`; `gpt-5.2-pro` → `★☆☆☆☆ (1.0)` [TESTED - hand calculation on the table values]
- **Devin multipliers (DD-21)**: removed from the formula and from every generated output; the Section 3.2 price rule `In USD = cost * 0.50`, `Out USD = cost * 2.50` is deleted from `MODEL_INVENTORY.md` Section 2; `Devin cost` values of the 13 Section 3.1 rows disappear with the column
- **Files affected when applied**: `update-model-inventory.py` (header, `Value` function, Section 3.2 branch), `verify-and-distribute-registry.ps1` Gate 9.4 (header regex, `Value` recomputation), `_PROMPTS_ModelInventoryUpdate_TEMPLATE.md` (script list and Prompt 6 column lists), `MODEL_INVENTORY.md` Sections 1, 2, 3, mirrors in `.devin/skills/llm-tools/` and `.claude/skills/llm-tools/`

### 5.7 Devin Model Deviations (DD-22)

Goal: Section 3.2 lists only what differs between Devin and the global Section 3.1: models that are absent from it, or priced differently. Replaces "Devin-Only Models". Decision DEV-01 option 1: fold into the existing prompts, no new prompt, no new canonical JSON, no distribution change.

- **Source**: `https://docs.devin.ai/desktop/models` (`DV1`). The tables are rendered by JavaScript; a plain fetch and the `.md` endpoint return empty table bodies. Three tabs: `Self-serve`, `Enterprise (ACUs)`, `Legacy enterprise (credits)`. Playwright clicks every tab and reads the visible table (tested 2026-11-18 with Python Playwright and the installed Chrome: 17, 17, and 14 data rows; the Playwright MCP browser was locked by another instance) [TESTED - hand run, LLMCAPCLS-IN01-SC-DEVIN-MODELS]
- **Extract file**: `[DATE]_Devin-Models-DOM.json` in the run folder with the rows per tab plus `promotions[]`: the page prose about discounts, free periods, and dated price changes (model, tab, list prices, `until` or `from` date), read from the `.md` endpoint because the prose is static there
- **Matching**: the Devin display name maps to a registry model by family through an explicit name map in `update-model-inventory.py`; effort words (`Low`, `Medium`, `High`, `XHigh`, `Max`), `Thinking`, `Fast`, and the dagger are stripped because prices do not change with effort. No registry match = Devin-only
- **Deviation test**: Devin-only, or `In USD`, `Cache USD` (cache read), or `Out USD` differs from the Section 3.1 row by more than 0.5%. Cache write is ignored (the inventory has no such column). A matching model is not listed
- **Promotions**: the deviation test and the row prices use the Self-serve table price; where the table shows `Free` or `—` (a free period) the row shows the list price from `promotions[]`. Notes carry each active promotion with its end date and list price. An announced future price change counts as a deviation only from its effective date; the script prints it as a `PROMOTION:` line for the RunReport Pending resolution (2026-11-18: `GPT-5.6 Sol` $5 / $30 from 2026-11-21 against $4 / $20 in Section 3.1 [VERIFIED - LLMCAPCLS-IN01-SC-DEVIN-MODELS prose])
- **Plans**: baseline = Self-serve tab. A difference on the Enterprise tab that is not a promotion goes to Notes. The credits tab is not used (DD-21)
- **Columns**: `Model | Generation | Items | Efforts | In USD | Cache USD | Out USD | Released | Notes` (`Released` from the matched registry model, else `devin_only[].release_date`, else `-`; Section 5.8). Generation for a Devin-only model is set once by the layering rule EC-6 (vendor statement) and recorded in `[DATE]_Generation-Edges.json` `devin_only[]`, never changed afterwards; `Items` default from the rung; `Efforts` = union of the effort words in the tables
- **Snapshot 2026-11-18** (page text: prices as of 2026-11-09): of 15 model families on the token tabs, 12 equal their Section 3.1 price (`Kimi K3` on the credits tab maps to `kimi-k3`); 3 are Devin-only and priced: `Adaptive` ($0.50 / $0.10 / $2.00 Self-serve), `SWE-2 Flash` (list $0.10 / $0.01 / $0.50; free on Self-serve until 2026-12-04), `SWE-2` (list $3.00 / $0.30 / $15.00; free on Self-serve until 2026-11-30, Enterprise $0.50 / $0.05 / $2.50 until 2026-12-31); prose-only without price: `SWE-1.7`, `SWE-1.6`, `SWE-1-mini`, `swe-grep`, `swe-check`, Fusion [VERIFIED - LLMCAPCLS-IN01-SC-DEVIN-MODELS]
- **Rows that left on the first generation** (2026-11-18, not on the page): `Gemini 3.7 Flash`, `Gemini 3.5 Flash`, `Kimi K3` (now `kimi-k3` in Section 3.1), `SWE-1.7`; the generated Section 3.2 holds `SWE-2` (`G06*`), `SWE-2 Flash` (`G05*`), and `Adaptive` (`G01*`, unplaced); both SWE rungs are [ASSUMED] from the vendor wording, recorded in `Generation-Edges.json` `devin_only[]` with `efforts` taken from the page prose
- **Fallback**: a run without a Devin DOM file (`NEWMODEL` without `Devin` in `[TARGET_PROVIDERS]`) keeps the existing Section 3.2 rows unchanged

### 5.8 Released Column (DD-24)

Goal: every inventory row states when the model was released, with only the precision a source supports. Requested 2026-11-18.

- **Format**: `YYYY-MM-DD` when a vendor page, release note, or announcement prints the day; `YYYY-MM` when only the month is printed or known. Registry `release_date` holds the same string and the table prints it unchanged; any other value stops `update-model-inventory.py` and Gate 5.4
- **Not a source for the day**: the Epoch `date`, the run date, and the date of the family head. The former `release_date_assumed: true` marked exactly these cases; the flag is retired, the 46 flagged dates were cut to their month on 2026-11-18, and 7 explicit `false` flags were removed without a value change (registry 1.15.0) [ASSUMED - the month of each cut date comes from the family head or Epoch and is re-read in the next run]
- **Storage in the DOM JSONs**: every `[DATE]_*-DOM.json` has a top-level array `released[]` of `{model_id, released, source_url, raw_text}`; `released` = `YYYY-MM-DD`, `YYYY-MM`, or `null` (the page lists the model without a date); `raw_text` = the printed string. Prompts 2 and 3 write it while the pages are open; pricing pages usually print no date
- **Research**: Prompt 5 runs `match-epoch-eci.py`, which reads the arrays into `released_in_dom` per registry model, `new_model_releases{}`, and `release_conflicts[]`. A new model takes its date from there, else from the vendor overview, release note, or announcement; no page prints one = `unresolved[]` line, and Prompt 6 stops for that model. A registry model with a month-only date gets its vendor page opened for the day (`FULL`: all such models; other modes: `[TARGET_MODELS]`); results go to `release_corrections[]` in `[DATE]_Generation-Edges.json`
- **Rules**: a day refines a month of the same month; a different month is a correction that needs a page source and a RunReport Section 4 line; two pages that disagree go to `PROBLEMS.md` and the old value stays
- **Insert**: Prompt 6 writes `release_date` into the registry; Prompt 7 runs `update-model-inventory.py`, which prints it as `Released` in Section 3.1 and for matched rows of Section 3.2; a Devin-only row takes `devin_only[].release_date` or `-`
- **Gates**: 5.4 (format of all registry values, no `release_date_assumed`, each DOM `released[]` value equals the registry value or is the month of the registry day) and 9.4 (header, every Section 3.1 `Released` cell equals the registry, Section 3.2 cells equal the registry or are `-` for Devin-only rows) [TESTED - DOM test with two injected conflicts: Gate 5.4 FAIL naming both models, then PASS after the fix]
- **Ordering effect**: the layering script orders by the earliest possible day and calls a model a predecessor only when its latest possible day is before the successor's earliest possible day, so a month-only date never creates an E2 edge inside its own month. The 46 month-only dates leave every rung unchanged: regression test 8 of 8, insert-only dry run 0 inserted, 0 squeezed, 0 cycles [TESTED]
- **State 2026-11-18**: registry 1.15.0 has 86 dates with a day and 46 with a month; `MODEL_INVENTORY.md` carries `Released` in 124 Section 3.1 rows; the three Section 3.2 rows (`SWE-2`, `SWE-2 Flash`, `Adaptive`) show `-` because no source date is recorded

## 6. Using the Inventory in Partitioned Documents

Lookup inputs: `intended_model`, `effort`, context window. Output: one row with Generation, Items, Efforts, Context, prices, Notes. Then Section 4: effort shift → explicitness level → expanded items → prompt count and shape.

- **TASKS** - items are written at outcome-level (Section 4.1 `G07-G09` granularity) and carry `Est: [N] HWH`. A task executed by one prompt must satisfy `Est <= 1 HWH` and, after expansion for the target model, `expanded_items <= Items` and `files <= max_files`; larger tasks are split. The TASKS document itself is model-independent; expansion happens in `/write-prompts`
- **STRUT** - a step executed by one prompt satisfies `step HWH <= 1` and the same item and file limits. Replaces the ">30 min AWH = decompose" rule in `edird-phase-planning` with a model-aware check
- **Prompts files** - frontmatter `intended_model`, `effort`, `context_window_size` from the row; opening commentary states Generation, effective rung, explicitness level, Items, prompt count, cost estimate; every implementation prompt holds `<= Items` numbered items at the stated explicitness level and `<= max_files` files; checkpoints per `checkpoint_interval`; `scope guard strict` text when Notes says so; critical items first and last; input per prompt `<= 50%` of Context
- **Verify** (PRMT-SC-05) - recomputes the bounds from the row and the prompts file and fails on: items above Items, files above max_files, missing checkpoint, missing scope guard, explicitness level below the rung's requirement (for example outcome-level items in a `G05` prompts file)

## 7. HWH and AWH

Unchanged from v1 Section 10 except that WF is gone. Two units remain:

```
  HWH  "How big is the job?"     task size, model-independent   → TASKS Est, 1 HWH per prompt cap, cost
  AWH  "How long will I wait?"   agent wall-clock, model-dependent → STRUT phase budgets, scheduling
```

- **HWH (Human Work Hours)** - hours a skilled human expert needs without AI, including reading, editing, verifying. Same unit [METR](https://metr.org/time-horizons/) and [Anthropic](https://www.anthropic.com/research/estimating-productivity-gains) use to size tasks [VERIFIED - LLMCAPCLS-IN01-SC-METR-TH, LLMCAPCLS-IN01-SC-ANTH-PROD]. Estimate in buckets 0.25 / 0.5 / 1 / 2 HWH; split at 4 (agent success falls steeply above about 4 human hours, METR: under 10%) [VERIFIED - LLMCAPCLS-IN01-SC-METR-BLOG; buckets ASSUMED]
- **AWH (Agent Work Hours)** - wall-clock time the agent runs. Default before data `AWH ≈ 0.2 × HWH` (Anthropic's estimated 80% task-time reduction; self-estimated and human-in-the-loop, so [ASSUMED] for unattended runs). With data: `prompt_count × observed minutes per prompt` from STRUT Time Logs. Not applicable in large familiar codebases, where [METR's randomized controlled trial (RCT)](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) measured experienced developers 19% slower with early-2025 tools [VERIFIED - LLMCAPCLS-IN01-SC-METR-RCT, LLMCAPCLS-IN01-SC-METR-UPLIFT]
- **Why no model factor on HWH**: WF claimed "HWH one prompt completes without skipping" per model. METR's own 80%-reliability horizons carry factor-2 error bars [VERIFIED - LLMCAPCLS-IN01-SC-METR-LIMIT], the `TBLF-IN02` test showed effort and thinking method outweigh two capability bands, and the ledger measures items, not hours. Items (measured) plus the 1 HWH cap replace WF; the cap is the one place where HWH still bounds a prompt

One-paragraph explanation: "HWH says how big a job is for a skilled human; no prompt should carry more than one. Generation says how much the model may be left to infer, so a lower-rung model gets the same job spelled out in more items. Items says how many of those items one prompt may hold before the model drops some. Divide expanded items by Items and you have the prompt count. AWH, the time you wait, starts at one fifth of HWH and is replaced by measured minutes per prompt."

## 8. Limitations

- **Cross-vendor equality is coarse**: `G10` holds seven models from three vendors whose intervals overlap, `G11` an OpenAI and an Anthropic model with equal scores. Equal rung means equal prompt shape, not equal quality; vendor choice stays with the author
- **E1 relies on `uc_class` being right**: the lineup class is set by hand for new models (`sol` / `terra` / `luna`, `grok-build`). A wrong class propagates through E1. The layering script cannot detect it; the price order within a point version is the review check
- **Cross-version edges depend on the vendor's guidance page staying current**: EC-1 reads Anthropic's model-selection guidance at one date; when the vendor rewrites it (next Opus release), the recorded edge keeps its date and source and is not revisited. The edge is append-only like every rung
- **EC-2 inheritance is a rule, not a vendor statement**: Fable 5 is above Opus 5.5 because Fable 5.1 is and the two share tier, generation, and price; the vendor never compared Fable 5 with Opus 5.5 directly
- **Specialized Apex models inherit the top**: `gpt-5.6-cyber` at `G11` and `gpt-5.5-cyber` at `G10` rest on E1 from `uc_class` alone; `o3-deep-research` and `o1-pro` likewise. EC-4 requires the announcement statements to be cited before registry 1.12.0 is written
- **Epoch coverage gaps**: 24 of 100 registry models have no Epoch row and `gpt-5` has a score without an interval; 5 rungs are E6 estimates (`*`), 2 are unplaced. GLM Efficient and vision models are placed by tier offset only
- **Bootstrap vs insertion order**: the Section 2.3 layering is order-independent; later insertions are not. A model squeezed between two frozen rungs ties with the lower one. Expected mid-ladder, rare at the top
- **Explicitness boundaries and Items defaults are unmeasured**: `G10+` / `G07-G09` / `G04-G06` / `G01-G03` and 8 / 6 / 5 / 4 come from the former profile constants; only `glm-5.2` has a measured Items. The ledger is the only calibration path
- **Effort shift sizes are assumed**: direction is measured on three configurations (`TBLF-IN02`); the one-rung and two-rung sizes are not
- **Observations depend on the execution framework**: framework explains 56% of over-eagerness variance, base model 21% ([SNARE](https://arxiv.org/abs/2605.28122)) [VERIFIED - LLMCAPCLS-IN01-SC-SNARE]. Ledger lines carry `engine`; Items measured under `cascade` may not hold under `claude-code`
- **The E6 `*` → measured transition is the one rung change**: it breaks the append-only guarantee for estimated rungs only; Gate 9.4 allows exactly this change
- **The ladder is a session artifact until applied**: `.tmp_dominance_ladder.py` and `.tmp_manual_edges.json` live in `_agentwork/`; no canonical file carries `generation` yet
- **Two registry release dates are wrong** (EC-9): `claude-fable-5-1` 2026-09-01 per vendor (registry 2026-09-25), `claude-opus-5-5` announced 2026-09-22 (registry 2026-10-14). E2 ordering is unaffected in both cases
- **46 release dates are month-only** (DD-24): their day was never confirmed by a vendor page, so the inventory shows only the month; the first run with `released[]` refines them where a page prints the day (Section 5.8)

## 9. Next Steps

1. **DD-11 closed 2026-11-02**: both `claude-fable-5-1` and `claude-fable-5` recorded above `claude-opus-5-5` (Section 2.6 EC-1, EC-2); `.tmp_manual_edges.json` holds the two `higher_than` entries with sources
2. **DD-12 approved 2026-11-02**: `_SPEC_MDLRGUP-MDLINVNTRY-01_GenerationLadder.md` in `T02_MDLINVNTRY_ReliableModelInventory_2026-10-28` carries Sections 2, 4, 5 as requirements; `/write-impl-plan` follows
3. Promote `.tmp_dominance_ladder.py` to `layer-generation-ladder.py` with E6, `higher_than` from the registry, insert-only mode, and `--bootstrap`; add a test that re-layers the 2026-10-28 snapshot with the two manual edges and reproduces Section 3
4. Cite the EC-4 announcement statements for `gpt-5.6-cyber`, `gpt-5.5-cyber`, `o3-deep-research`, `o1-pro`, `o4-mini-deep-research` before registry 1.12.0 is written
5. Record in the session PROBLEMS.md during `/session-save`: `MDLRGUP-MDLINVNTRY-PR-0004` (ECI letter misordering, Section 1) and `MDLRGUP-MDLINVNTRY-PR-0005` (release dates of `claude-fable-5-1` and `claude-opus-5-5`, EC-9)
6. Mark DD-01, DD-02, DD-03 in session NOTES.md and T02 `IN01` Section 5 as superseded or absorbed during `/session-save`
7. **DD-20 and DD-21 decided 2026-11-18** (user: `VAL-01 1`, `VAL-02`: remove the multiplier from calculation and JSON output): implement Section 5.6 in the scripts, Gate 9.4, template, and `MODEL_INVENTORY.md`, then mirror to `.devin` and `.claude`
8. **DD-22 decided 2026-11-18** (user: `DEV-01 1`): implement Section 5.7 (Devin extraction in Prompt 3, deviation generation in Prompt 7, Gate 2 and Gate 9.4 checks, name map, `update-model-inventory.py`); open point: confirm that the four rows listed in Section 5.7 (`Gemini 3.7 Flash`, `Gemini 3.5 Flash`, `Kimi K3`, `SWE-1.7`) leave Section 3.2
9. **DD-24 applied 2026-11-18** (`Released` column, Section 5.8): the first run on the new template is the first with `released[]` in the DOM extracts; it refines the 46 month-only dates where a vendor page prints the day, fills `devin_only[].release_date` for `SWE-2`, `SWE-2 Flash`, and `Adaptive` where a source exists, and reports Gate 5.4 for the first time against real DOM data; Lana-V1 and `.claude` copies stay on the earlier registry until the next run with `-IncludeExternal` and the next `.claude` rebuild

## 10. Sources

**Primary Sources (providers, research organizations, local files):**
- `LLMCAPCLS-IN01-SC-EPOCH-CSV`: https://epoch.ai/data/eci_scores.csv - Epoch Capabilities Index scores with 95% confidence intervals per model; snapshot 2026-10-28 in `_2026-10-28_PRICES/2026-10-28_eci-leaderboard.csv`, matched to registry IDs in `2026-10-28_Epoch-ECI-Match.json` (76 of 100 models scored) [VERIFIED]
- `LLMCAPCLS-IN01-SC-IPPS-LADDER`: `_agentwork/.tmp_dominance_ladder.py`, `.tmp_ladder.json`, `.tmp_ladder.txt`, `.tmp_manual_edges.json`, `.tmp_ladder_dd11.json` - E1/E2/E3/E5 edge construction plus manual `higher_than` edges and fixed-point layering over 92 text models; result 11 rungs without and 12 rungs with the two Fable edges, no cycle, no contradiction; first run with release-order insertion produced 22 conflicts (2026-11-02) [TESTED]
- `LLMCAPCLS-IN01-SC-IPPS-MREG`: `PromptSystemV4.5/skills/llm-tools/model-registry.json` 1.11.0 - `uc_class`, `release_date`, `eci_score`, `status` per model (E1, E2 inputs) [VERIFIED]
- `LLMCAPCLS-IN01-SC-IPPS-MINV`: `PromptSystemV4.5/skills/llm-tools/MODEL_INVENTORY.md` (2026-10-29) - letter scheme output used in Section 1; prices and Devin cost multipliers [VERIFIED]
- `LLMCAPCLS-IN01-SC-TBLF-IN02`: `e:\Dev\LLM-Research\_Sessions\_2026-03-05_TabularDataFormatsForLLMs\01_CSVScaleLimits\_INFO_01_CSVScaleLimits-TestResults.md` [TBLF-IN02] Section 5.1 and `_INFO_02_CSVScaleLimits-Findings.md` [TBLF-IN03] E1 - confirmed CSV extraction rows per model and effort (20 configurations, n=3, about 28% variance, May 2026); adaptive thinking at Medium skips reasoning [VERIFIED]
- `LLMCAPCLS-IN01-SC-IPPS-IN06`: `T01_MDLBHVPRM_BehavioralParameterBenchmarks_2026-10-19/_INFO_MDLBHVPRM-06_ModelAwarePartitioning.md` - capacity, instruction following, eagerness axes; partition parameters; GLM-5.2 over-eagerness; MDLBHVPRM-DD-01 [VERIFIED]
- `LLMCAPCLS-IN01-SC-IPPS-IN07`: `T01_MDLBHVPRM_BehavioralParameterBenchmarks_2026-10-19/_INFO_MDLBHVPRM-07_PromptFeedbackLoop.md` - observation ledger, `items_planned` / `items_done`, aggregation by `/session-finalize` [VERIFIED]
- `LLMCAPCLS-IN01-SC-IPPS-IN05`: `T02_MDLINVNTRY_ReliableModelInventory_2026-10-28/_INFO_MDLRGUP-MDLINVNTRY-05_WorkPerPromptOptions.md` - no external benchmark measures single-prompt HWH without item drop-out; option c fixed operational caps; Section 9: `glm-5.2` High completed 4-12 items per prompt at 100% over 7 prompts (`__CARD_MDLINVNTRY-Findings.md`) [VERIFIED]
- `LLMCAPCLS-IN01-SC-ANTH-FABLE51-OVW`: https://platform.claude.com/docs/en/models/fable-5-1/overview - Fable 5.1 released 2026-09-01; "For most workloads, start with Claude Opus 5.5. Use Claude Fable 5.1 for demanding reasoning and long-horizon agentic work, or when your evals on Claude Opus 5.5 at higher effort still don't meet your requirements"; $10 / $50 per 1M tokens (accessed 2026-11-02) [VERIFIED]
- `LLMCAPCLS-IN01-SC-ANTH-FABLE51-NEW`: https://platform.claude.com/docs/en/models/fable-5-1/whats-new-fable-5-1.md - "Claude Fable 5.1 extends Claude Fable 5 at the same input and output prices"; Mythos 5.1 "Same capabilities as Claude Fable 5.1" (accessed 2026-11-02) [VERIFIED]
- `LLMCAPCLS-IN01-SC-ANTH-OPUS55`: https://www.anthropic.com/news/claude-opus-5-5 - announced 2026-09-22; "performs at the level of Claude Fable 5.1 on most work"; "the gap between Opus 5.5 and Claude Fable 5.1 is narrower than these scores suggest"; "comparable to Claude Mythos 5.1 in biology and cybersecurity"; $4 / $20 per 1M tokens (accessed 2026-11-02) [VERIFIED]
- `LLMCAPCLS-IN01-SC-ANTH-FABLE5`: https://www.anthropic.com/news/claude-fable-5-mythos-5 - Fable 5 launched 2026-06-09 as "our 5th model generation"; Mythos 5 "is the same underlying model as Fable 5, but with the safeguards lifted in some areas"; $10 / $50 per 1M tokens (accessed 2026-11-02) [VERIFIED]
- `LLMCAPCLS-IN01-SC-KIMI-K3`: https://www.kimi.ai/blog/kimi-k3 - Kimi K3 "still trails" Claude Fable 5 and GPT-5.6 Sol (accessed 2026-10-28) [VERIFIED]
- `LLMCAPCLS-IN01-SC-COG-SWE17`: https://www.linkedin.com/posts/jefflinwang_weve-released-swe-17-our-best-model-yet-activity-7480867805618438146-J56D - SWE-1.7 trained from Kimi K2.7, live in Devin, released 2026-07-08 (accessed 2026-10-28) [VERIFIED]
- `LLMCAPCLS-IN01-SC-DEVIN-MODELS`: https://docs.devin.ai/desktop/models - Devin Desktop model price tables (Self-serve, Enterprise (ACUs), Legacy enterprise (credits)) rendered by JavaScript; promotion and dated price-change prose; prices as of 2026-11-09 (accessed 2026-11-18) [VERIFIED]
- `LLMCAPCLS-IN01-SC-GOOG-APICHG`: https://ai.google.dev/gemini-api/docs/changelog - 2026-10-08: `gemini-3.7-flash` routed to `gemini-3.8-flash`, `gemini-3.5-flash` to `gemini-3.6-flash` (accessed 2026-10-28) [VERIFIED]
- `LLMCAPCLS-IN01-SC-RULER`: https://arxiv.org/abs/2404.06654 - effective context length at half or less of the claimed window for most tested models (accessed 2026-10-28) [VERIFIED]
- `LLMCAPCLS-IN01-SC-METR-TH`: https://metr.org/time-horizons/ - time horizon defined on human-expert task duration (accessed 2026-10-28) [VERIFIED]
- `LLMCAPCLS-IN01-SC-METR-BLOG`: https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/ - near 100% success under 4 human minutes, under 10% above about 4 hours (accessed 2026-10-28) [VERIFIED]
- `LLMCAPCLS-IN01-SC-METR-LIMIT`: https://metr.org/notes/2026-01-22-time-horizon-limitations/ - error bars about factor 2 (accessed 2026-10-28) [VERIFIED]
- `LLMCAPCLS-IN01-SC-METR-RCT`: https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/ - experienced developers 19% slower with early-2025 AI tools (accessed 2026-10-28) [VERIFIED]
- `LLMCAPCLS-IN01-SC-METR-UPLIFT`: https://metr.org/blog/2026-02-24-uplift-update/ - early-2026 estimates -18% and -4% with wide intervals, selection bias (accessed 2026-10-28) [VERIFIED]
- `LLMCAPCLS-IN01-SC-ANTH-PROD`: https://www.anthropic.com/research/estimating-productivity-gains - tasks about 1.4 h without AI, about 80% time reduction, estimates imperfect but usable (accessed 2026-10-28) [VERIFIED]
- `LLMCAPCLS-IN01-SC-SNARE`: https://arxiv.org/abs/2605.28122 - agent framework explains 56% of over-eagerness variance, base model 21% (accessed 2026-10-19 via IN06) [VERIFIED]

Sources of v1 that this version no longer cites (release-date aggregators, provider announcement pages for individual release dates, benchgap IFEval, Anthropic model overview) remain in `_INFO_HOW_TO_ORGANIZE_LLMS_BY_CAPABILITY_v1.md` Section 12; `release_date` values in the registry carry them.

## 11. Document History

**[2026-11-18 17:40]**
- Added: Section 5.8 Released Column (DD-24): date format, DOM `released[]` storage, research, rules, gates, ordering effect, state; Summary bullet DD-24; Section 5.2 `Released` bullet; Section 5.4 template bullet; Limitations bullet for 46 month-only dates; Next Steps item 9
- Changed: Section 2.2 sources per kind (E2 orders by `release_date`, month-only rule); Section 5.1 (`release_date` format, `release_date_assumed` removed in 1.15.0); Section 5.2 column list; Section 5.3 script entries (layering, match, inventory, Gate 5.4 and 9.4); Section 5.7 Section 3.2 column list

**[2026-11-18 15:18]**
- Added: Summary bullet DD-23 (rung renamed Depth -> Generation)
- Changed: labels `D[n]` -> `G[nn]`, column `Depth` -> `Generation`, registry keys, script and file names, and the formula `G(new) = G(sibling) - ...` in every section, including earlier history entries; Section 2 and Section 4 headings and anchors renamed

**[2026-11-18 08:30]**
- Added: Section 5.7 Devin Model Deviations (DD-22, DEV-01 option 1): extraction with tab clicks, matching, deviation test, promotion handling, columns, 2026-11-18 snapshot; source `LLMCAPCLS-IN01-SC-DEVIN-MODELS`; Next Steps item 8
- Changed: Section 3.2 renamed "Devin Model Deviations" and generated from the Devin page (Summary, Section 3.1 Devin-only note, 5.2, 5.3, 5.4, 5.6); corrected the DD-21 consequence that Section 3.2 rows carry no prices; Section 5 diagram input is the Devin DOM file; Next Steps item 7 open point closed

**[2026-11-18 08:00]**
- Added: Section 5.6 Value Score (DD-20): log-scale price score 1.0-5.0 within the rung with star display; Summary bullets for DD-20 and DD-21; Next Steps item 7
- Changed: `Devin cost` column replaced by `Value` in Section 5.2 columns, Section 5.3 scripts, Gate 9.4, and Section 5.4 template changes; Section 5 diagram and Section 3.1 Devin-only rows no longer use Devin cost multipliers (DD-21)

**[2026-11-02 13:20]**
- Added: Section 2.6 edge-case catalogue EC-1 to EC-9, each with source type, rule, and status; sources `LLMCAPCLS-IN01-SC-ANTH-FABLE51-OVW`, `-FABLE51-NEW`, `-OPUS55`, `-FABLE5`
- Changed: DD-11 closed - `claude-fable-5-1` and `claude-fable-5` recorded above `claude-opus-5-5` from Anthropic's model-selection guidance; ladder re-run to 12 rungs (`G12` Fable 5, Fable 5.1, Mythos 5, Mythos 5.1); Summary, Sections 2.5, 3, 3.1, 8 updated
- Changed: DD-12 approved - Next Steps point to `_SPEC_MDLRGUP-MDLINVNTRY-01_GenerationLadder.md`
- Added: EC-9 release-date findings for `claude-fable-5-1` and `claude-opus-5-5`

**[2026-11-02 12:50]**
- Changed: capability representation from year-letter labels on ECI bands to an append-only dominance ladder (`G01`, `G02`, ...) with evidence kinds E1-E6 (DD-10 option 3); Sections 1-6 rewritten; v1 kept as `_INFO_HOW_TO_ORGANIZE_LLMS_BY_CAPABILITY_v1.md`
- Added: computed ladder for 92 models (11 rungs, Section 3), Devin-only rungs, explicitness level per rung, effort shift, Items axis with measured override, partition formula without WF, registry 1.12.0 fields, script and template change list, DD-11 and DD-12
- Removed: Comp, May 1 wrap, year anchor, WF formula, behavior profiles, profile thresholds and change rule, METR WF sanity check
- Added: sources `LLMCAPCLS-IN01-SC-EPOCH-CSV`, `LLMCAPCLS-IN01-SC-IPPS-LADDER`, `LLMCAPCLS-IN01-SC-IPPS-IN05`

**[2026-10-29 14:30]**
- Changed: letter definition from UC tier to Epoch ECI band relative to a year anchor; Comp, May 1 wrap, WF from band, `release_date` and `eci_band_source` fields, TBLF cross-check (v1)

**[2026-10-29 13:37]**
- Changed: R2 mapped UC tiers to letters; R3 release-month gate; 40 label changes (v1)

**[2026-10-28 18:05 - 20:10]**
- Initial research document and eight revisions: year-letter labels, October promotion rule, WF formula, behavior profiles, inventory production, HWH and AWH, GRUC separation (v1 Section 13 lists each)
