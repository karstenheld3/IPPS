# INFO: How to Organize LLMs by Capability

**Doc ID**: LLMCAPCLS-IN01
**Goal**: Define an append-only depth ladder per model, the working-set size per model, and how `MODEL_INVENTORY.md` is produced from them and used to partition TASKS, STRUT, and prompts files by model, effort, and context window
**Timeline**: Created 2026-10-28, Updated 11 times (2026-10-28 - 2026-11-02)
**Target file**: `PromptSystemV4.5/skills/llm-tools/MODEL_INVENTORY.md`, `PromptSystemV4.5/skills/llm-tools/model-registry.json`, `_Sessions/!ModelRegistryUpdate/_PROMPTS_ModelInventoryUpdate_TEMPLATE.md`

**Depends on:**
- `_INFO_MDLBHVPRM-06_ModelAwarePartitioning.md [MDLRGUP-MDLBHVPRM-IN06]` for the capacity, instruction following, and eagerness axes and decision MDLBHVPRM-DD-01 (observation overrides benchmarks)
- `_INFO_MDLBHVPRM-07_PromptFeedbackLoop.md [MDLRGUP-MDLBHVPRM-IN07]` for the checkpoint ledger that calibrates Items

**Supersedes:** `_INFO_HOW_TO_ORGANIZE_LLMS_BY_CAPABILITY_v1.md` (year-letter labels, ECI bands, WF, behavior profiles). Section 1 states why.

## Summary

- **Depth is an ordinal rung `D1`, `D2`, ... assigned once and never regraded**: a model gets the lowest rung consistent with the models it provably dominates; new models insert above, between, or level with existing ones; the ladder grows upward without a year anchor, comparison year, or May 1 wrap [ASSUMED - rule design, DD-10 option 3]
- **"Provably dominates" has four evidence kinds and two fallbacks**: `E1` vendor lineup tier within the same point version (Opus 5.5 > Sonnet 5.5 > Haiku 5.5), `E2` same-lineage successor is not below its predecessor (weak, allows ties), `E3` [Epoch Capabilities Index (ECI)](https://epoch.ai/eci) 95% confidence intervals do not overlap, `E4` documented in-house observation (TBLF, ledger, FAILS); fallbacks `E5` sibling tie and `E6` tier-offset estimate for models without a score. No edge = tie allowed. Benchmark noise cannot create an edge because overlapping intervals produce none [VERIFIED - mechanism tested on 92 models, LLMCAPCLS-IN01-SC-IPPS-LADDER]
- **The current inventory layers into 12 rungs with zero contradictions**: `D12` `claude-fable-5`, `claude-fable-5-1`, `claude-mythos-5`, `claude-mythos-5-1`; `D11` `gpt-6-astra`, `claude-opus-5-5`, `gpt-5.6-cyber`; `D10` `gpt-6.1-sol`, `gpt-6-sol`, `gpt-5.6-sol`, `gemini-4-argon`, `claude-sonnet-5-5`; `D6` `gpt-5`, `claude-opus-4-5`, `glm-5.2`; `D1` `gpt-4o`, `gpt-4o-mini`. 2024-2025 models span `D1`-`D8`, placed 2026 models `D4`-`D12` [TESTED - LLMCAPCLS-IN01-SC-IPPS-LADDER, registry 1.11.0 and Epoch snapshot 2026-10-28]
- **Every case the automatic edges cannot decide has a research mechanism with a named source type** (Section 2.6, EC-1 to EC-9): cross-version tier order from the vendor's model-selection guidance, superseded family members by inheritance, restricted twins by "same model" statements, specialized and unscored models by announcement and price order, squeezes and contradictions by in-house head-to-head tests. Silence = tie, never judgment [ASSUMED - rule design]
- **DD-11 closed: Fable 5 and Fable 5.1 are recorded above Opus 5.5**: Anthropic's [Fable 5.1 overview](https://platform.claude.com/docs/en/models/fable-5-1/overview) says "start with Claude Opus 5.5. Use Claude Fable 5.1 for demanding reasoning ... or when your evals on Claude Opus 5.5 at higher effort still don't meet your requirements"; the Opus 5.5 announcement claims parity "on most work" only. Fable 5 inherits the edge ("Fable 5.1 extends Fable 5", intervals overlap). Re-run: top `D12`, no cycle, no other rung moves [VERIFIED - LLMCAPCLS-IN01-SC-ANTH-FABLE51-OVW, LLMCAPCLS-IN01-SC-ANTH-OPUS55; TESTED - LLMCAPCLS-IN01-SC-IPPS-LADDER]
- **Prompt shape maps from the absolute rung, not from distance to the top**: explicitness level (`D1`-`D3` keystroke-level, `D4`-`D6` step-level, `D7`-`D9` outcome plus named files, `D10`+ goal-level) and Items default (4 / 5 / 6 / 8) are fixed per rung so a model's prompt recipe never changes when newer models arrive; `D10`+ covers every future top rung [ASSUMED - values are the former profile constants]
- **Items is the second axis and the only measured one**: largest `items_planned` completed with zero skips in `>= 3` ledger sequences overrides the default; `glm-5.2` completed 4-12 items per prompt at 100% with strict scope guard over 7 prompts in 2 sequences → provisional Items 8 against a `D6` default of 5. Over-eagerness sets `scope_guard: strict` in Notes and does not lower Items [VERIFIED - LLMCAPCLS-IN01-SC-IPPS-IN07, LLMCAPCLS-IN01-SC-IPPS-IN05 Section 9]
- **Effort shifts the effective rung**: Medium on adaptive-thinking models and Low on any model read one rung lower; no-reasoning models (`-` efforts) two rungs lower [VERIFIED - LLMCAPCLS-IN01-SC-TBLF-IN02: `claude-opus-4-6` M6 vs H667 rows, `gpt-5-mini` L65 vs M500, `gpt-4o` 4; rung sizes ASSUMED]
- **WF, Label, Comp, Profile, and the ECI band leave the inventory**: Human Work Hours (HWH) stay for cost and Agent Work Hours (AWH) only; prompt count = `max(ceil(expanded_items / Items), ceil(files / max_files), ceil(HWH / 1))` [ASSUMED - IN05 option c cap of 1 HWH per prompt]
- **Registry 1.12.0 carries `depth`, `depth_evidence`, `eci_ci`, `items`, `scope_guard`** and drops `capability_label`, `eci_band`, `eci_band_source`, `gen_equivalent`, `behavior_profile`; Gate 9.4 verifies that no existing `depth` changed between runs [ASSUMED - design, Section 5]

## Table of Contents

1. [Why the Year-Letter Scheme Failed](#1-why-the-year-letter-scheme-failed)
2. [Depth Ladder](#2-depth-ladder)
3. [Ladder for the Current Inventory](#3-ladder-for-the-current-inventory)
4. [From Depth to Prompt Shape](#4-from-depth-to-prompt-shape)
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

## 2. Depth Ladder

### 2.1 Definition

`D` is an integer rung. `D1` is the shallowest model in the inventory. Higher `D` = provably deeper reasoning. Rules:

- **Append-only**: a rung is assigned when a model is registered and never changes. New models insert above, between, or level with existing models
- **Unbounded**: there is no top constant; the top rung today is `D12` and rises when a model provably dominates a `D12` model
- **No year**: release date is an input to the evidence, not part of the ID. `gpt-5.2` (2025-12) and `gemini-3-flash-preview` (2025-12) are both `D7`; `gpt-5` (2025-08) is `D6`
- **Ties are expected**: two models without an edge between them may share a rung. Equal rung means equal prompt shape, not equal quality

### 2.2 Evidence Kinds

An edge `x > y` ("x dominates y") exists only with one of these:

- **E1 - vendor lineup tier** (strict): same provider, same point version, higher lineup class (`uc_class`, Universal Class: UC-1 Apex > UC-2 Flagship > UC-3 Balanced > UC-4 Efficient). `claude-opus-5-5 > claude-sonnet-5-5 > claude-haiku-5-5`; `gpt-5.6-sol > gpt-5.6-terra > gpt-5.6-luna`; `gpt-5.4-pro > gpt-5.4`. Across point versions (`claude-fable-5` vs `claude-opus-5-5`) E1 is not derived automatically because vendors use point versions differently: Anthropic's `5` → `5.5` is a refresh within five months, OpenAI's `gpt-5` → `gpt-5.6` spans 18 months and a full generation of progress (`gpt-5-pro` 150.6 vs `gpt-5.6-sol` 162.8 would contradict E3). A cross-version E1 edge is recorded from the vendor's model-selection guidance (Section 2.6 EC-1)
- **E2 - successor not below predecessor** (weak): same provider, same lineup class, same series, later release: `D(successor) >= D(predecessor)`. Allows a tie, forbids a regression. `gpt-6-sol >= gpt-5.6-sol`, `claude-opus-4-7 >= claude-opus-4-6`. Specialized models (`codex`, `cyber`, `deep-research`, `legal`, `non-reasoning`, `multi-agent`, `build`, vision `v`) have no E2 edges
- **E3 - benchmark separation** (strict): [Epoch ECI](https://epoch.ai/eci) 95% confidence intervals do not overlap: `ci_low(x) > ci_high(y)`. `claude-sonnet-5-5` [163.1-171.3] > `gpt-5.4-pro` [157.1-162.7]. `claude-opus-5-5` [165.3-174.0] vs `claude-fable-5` [160.5-168.2]: overlap, no edge
- **E4 - in-house observation** (strict): `TBLF-IN02` CSV limits, ledger sequences, FAILS entries naming both models under the same task. Overrides E3 when they conflict (MDLBHVPRM-DD-01). None recorded yet; Section 2.6 EC-7 names the test design
- **E5 - sibling tie**: a model without an Epoch score takes the rung of a same-provider, same-point-version, same-tier sibling that has one: `claude-mythos-5-1 = claude-fable-5-1`, `glm-5.3-flashx = glm-5.3-flash`

Sources per kind: E1 from `uc_class` and `release_date` in `model-registry.json`; E3 from the Epoch CSV score and 95% interval as matched into `[DATE]_Epoch-ECI-Match.json` (`eci_score`, `eci_ci_low`, `eci_ci_high`; Section 10 LLMCAPCLS-IN01-SC-EPOCH-CSV); E2 from the registry lineage; E4 and manual E1 from a `deeper_than` list in the registry with a source reference.

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
  gpt-4o          D1   bottom (nothing dominated)
  o1-mini         D2   E3 > gpt-4o            [132.4-137.2] clears [124.6-131.2]
  gpt-4.1-mini    D2   E3 > gpt-4o-mini
  gpt-4.1         D3   E1 > gpt-4.1-mini      ([133.6-138.3] overlaps o1-mini; the tier edge lifts it)
  o1              D4   E3 > gpt-4.1           [139.7-142.9] clears 138.3
  gpt-5-mini      D5   E3 > o1                [143.3-147.1] clears 142.9
  gpt-5           D6   E1 > gpt-5-mini        (score 150.0 but no interval in the snapshot, so no E3
                                               edges; the tier edge over its own mini carries the
                                               benchmark evidence upward)
  gpt-5-pro       D7   E1 > gpt-5
  gpt-5.4-pro     D9   E1 > gpt-5.4 (D8, E3 > gemini-3-flash-preview D7)
  claude-sonnet-5-5 D10 E3 > gpt-5.4-pro
  claude-opus-5-5 D11  E1 > claude-sonnet-5-5
  claude-fable-5-1 D12 E1 > claude-opus-5-5 (manual, vendor guidance, Section 2.6 EC-1)
  claude-fable-5  D12  E1 > claude-opus-5-5 (inherited, EC-2); automatic edges alone gave D10
```

The `gpt-5` line shows why tier edges matter: the snapshot carries a score but no interval for `gpt-5`, so on benchmarks alone it would sit at the bottom; its own `mini` has an interval that clears `o1`, and E1 propagates that upward.

### 2.6 Edge Cases and Resolution Mechanisms

Every case the automatic edges cannot decide has one research step with a named source type. The result is recorded in the registry (`deeper_than` entry with URL and access date, or a Notes line) before the layering script runs. No case is resolved by judgment without a citable statement; when the named source is silent, the outcome is a tie.

- **EC-1 Tier order across point versions** (`claude-fable-5-1` vs `claude-opus-5-5`)
  - Source: the vendor's current model-selection guidance in its platform documentation (Anthropic model overview "Choosing a model", OpenAI models page, Google model table)
  - Rule: an escalation statement ("start with X; use Y when X at higher effort still falls short", "Y for the most demanding reasoning") = E1 edge `Y > X`. A parity statement alone ("performs at the level of") or silence = tie
  - Resolved 2026-11-02: the [Fable 5.1 overview](https://platform.claude.com/docs/en/models/fable-5-1/overview) states "For most workloads, start with Claude Opus 5.5. Use Claude Fable 5.1 for demanding reasoning and long-horizon agentic work, or when your evals on Claude Opus 5.5 at higher effort still don't meet your requirements"; the [Opus 5.5 announcement](https://www.anthropic.com/news/claude-opus-5-5) states "performs at the level of Claude Fable 5.1 on most work" and "the gap between Opus 5.5 and Claude Fable 5.1 is narrower than these scores suggest". Depth measures the demanding-reasoning end, so the escalation statement decides: `claude-fable-5-1 > claude-opus-5-5` (E1) [VERIFIED - LLMCAPCLS-IN01-SC-ANTH-FABLE51-OVW, LLMCAPCLS-IN01-SC-ANTH-OPUS55]
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
  - Status: the ladder applies E1 from `uc_class` and price order; the announcement statements are not yet cited in `deeper_than` [ASSUMED until each page is read during the registry 1.12.0 run]
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
  - Rule: if the class is wrong, fix it and re-layer; if it is right, E1 wins (the lineup is the vendor's stated depth order; benchmark mix is the noise described in Section 1) and the E3 edge is dropped with a Notes line. Not occurred in 92 models
- **EC-9 Wrong registry input** (release date, class)
  - Source: the vendor model overview "Released" field, never an aggregator
  - Found 2026-11-02: `claude-fable-5-1` released 2026-09-01 (registry 2026-09-25); `claude-opus-5-5` announced 2026-09-22 (registry 2026-10-14) [VERIFIED - LLMCAPCLS-IN01-SC-ANTH-FABLE51-OVW, LLMCAPCLS-IN01-SC-ANTH-OPUS55]. Neither changes a rung; both go to PROBLEMS for the 1.12.0 run

Effect of EC-1 to EC-3 on the ladder, re-run with `.tmp_manual_edges.json` (`.tmp_ladder_dd11.json`): top `D12`, no cycle, 0 contradictions; `claude-fable-5`, `claude-fable-5-1`, `claude-mythos-5`, `claude-mythos-5-1` at `D12`; `claude-opus-5-5` stays `D11`; no other rung changes [TESTED - LLMCAPCLS-IN01-SC-IPPS-LADDER]. DD-11 is closed with this result.

### 2.7 Models without Evidence

A model with no Epoch score, no scored same-tier sibling, and no predecessor sits at `D1` by the formula, which reads as "shallowest" when it means "unplaced". Rule E6 fills the gap with a marked estimate:

- **E6 - tier offset estimate** (`*`): same provider, same point version, scored sibling of a different tier: `D(new) = D(sibling) - (tier(new) - tier(sibling))`, floor `D1`. The rung carries `*` in the inventory and `depth_estimated: true` in the registry; it is replaced by the evidence-based rung when Epoch publishes a score or a ledger observation arrives (the only case in which a rung changes)
- No sibling at all: `D1*` with Notes `unplaced`. Today: `glm-4-air`, `grok-build-0.1`

## 3. Ladder for the Current Inventory

Computed by `.tmp_dominance_ladder.py` from `model-registry.json` 1.11.0 (`uc_class`, `release_date`) and the Epoch snapshot of 2026-10-28 (`eci_score`, `eci_ci_low`, `eci_ci_high`) [TESTED - LLMCAPCLS-IN01-SC-IPPS-LADDER]. 92 API rows (every text model except `retired`), 12 rungs with the Section 2.6 manual edges (`.tmp_manual_edges.json`), no cycle, no E1-E3 contradiction. E6 estimates (`*`) were derived by hand from the computed rungs and are not yet in the script output. In parentheses: the evidence that set the rung.

- **D12** (4): `claude-fable-5-1` (E1 manual > `claude-opus-5-5`, EC-1), `claude-fable-5` (E1 inherited > `claude-opus-5-5`, EC-2), `claude-mythos-5` (E5 = `claude-fable-5`), `claude-mythos-5-1` (E2 >= `claude-mythos-5`)
- **D11** (3): `gpt-6-astra` (E1 > `gpt-6-sol`), `claude-opus-5-5` (E1 > `claude-sonnet-5-5`), `gpt-5.6-cyber` (E1 > `gpt-5.6-sol`; no Epoch score)
- **D10** (7): `claude-sonnet-5-5` (E3 > `gpt-5.4-pro`), `gpt-6.1-sol` (E3 > `gpt-5.4-pro`), `gpt-6-sol` (E2 >= `gpt-5.6-sol`), `gpt-5.6-sol` (E1 > `gpt-5.6-terra`), `gpt-5.5-pro`, `gpt-5.5-cyber` (E1 > `gpt-5.5`), `gemini-4-argon` (E3 > `gpt-5.4-pro`)
- **D9** (5): `claude-opus-5` (E3 > `gpt-5.2-pro`), `gpt-5.5` (E3 > `grok-4.7`), `gpt-5.4-pro` (E1 > `gpt-5.4`), `gpt-5.6-terra` (E1 > `gpt-5.6-luna`), `gpt-6.1-terra` (E2 >= `gpt-5.6-terra`; no Epoch score)
- **D8** (13): `claude-opus-4-8` (E3 > `gpt-5.2`), `claude-opus-4-7`, `claude-opus-4-6`, `claude-sonnet-5`, `gpt-5.4`, `gpt-5.6-luna`, `gpt-6-luna`, `grok-4.6`, `glm-5.3`, `gemini-3.8-flash` (E3 > `gemini-3-flash-preview`), `claude-haiku-5-5` (E3 > `gpt-5.2`), `gpt-5.2-pro` (E1 > `gpt-5.2`), `grok-4.7` (E2 >= `grok-4.6`)
- **D7** (11): `gpt-5.2`, `gpt-5.3-codex`, `gemini-3-flash-preview`, `gemini-3.1-pro-preview`, `gemini-3.6-flash`, `claude-sonnet-4-6`, `grok-4.5`, `glm-5.3-flash` (E3 > `o3-pro`), `glm-5.3-flashx`, `glm-5.3-flashx-legal` (E5), `gpt-5-pro` (E1 > `gpt-5`)
- **D6** (11): `gpt-5` (E1 > `gpt-5-mini`), `gpt-5.1`, `claude-opus-4-5`, `glm-5.1`, `glm-5.2`, `gpt-5.4-mini`, `grok-4.3`, `grok-4.20-0309-reasoning`, `grok-4.20-multi-agent-0309` (E3 > `gemini-2.5-pro`), `o3-pro`, `o3-deep-research` (E1 > `o3`)
- **D5** (8 + 1 estimated): `gemini-2.5-pro`, `o3`, `gpt-5-mini`, `claude-sonnet-4-5`, `glm-5`, `gpt-5.4-nano` (E3 > `o1`), `o1-pro` (E1 > `o1`), `o4-mini-deep-research` (E1 > `o4-mini`), `grok-4.20-0309-non-reasoning` (`D5*`, E6 from `grok-4.20-0309-reasoning` D6)
- **D4** (7): `o1` (E3 > `gpt-4.1`), `o4-mini` (E3 > `o3-mini`), `gemini-2.5-flash`, `claude-haiku-4-5`, `glm-4.7` (E3 > `gpt-4.1`), `gemini-3.1-flash-lite`, `gemini-3.5-flash-lite` (E3 > `o3-mini`)
- **D3** (5): `gpt-4.1` (E1 > `gpt-4.1-mini`), `o3-mini` (E3 > `gpt-4.1-mini`), `glm-4.5`, `glm-4.5-x` (E1 > `glm-4.5-airx`), `glm-4.6` (E2 >= `glm-4.5-x`)
- **D2** (7 + 3 estimated): `o1-mini` (E3 > `gpt-4o`), `claude-3-5-sonnet`, `gpt-4.1-mini`, `gemini-2.5-flash-lite` (E3 > `gpt-4o-mini`), `gpt-5-nano` (E3 > `gpt-4o`), `glm-4.5-airx`, `glm-4.5v` (E1 > `glm-4.5-flash`), `glm-4.7-flash`, `glm-4.7-flashx` (`D2*`, E6 from `glm-4.7` D4), `glm-4.6v` (`D2*`, E6 from `glm-4.6` D3)
- **D1** (4 + 3 estimated): `gpt-4o`, `gpt-4o-2024-05-13`, `gpt-4o-mini`, `gpt-4.1-nano` (Epoch 129.5, interval overlaps `gpt-4o-mini`), `glm-4.5-flash` (`D1*`, E6 from `glm-4.5` D3, floor), `glm-4-air`, `grok-build-0.1` (`D1*`, unplaced)

Observations:

- **Vendor tiers hold everywhere**: Fable > Opus > Sonnet > Haiku across the Claude 5 generation; Astra > Sol > Luna; Pro > base; every provider's Efficient model sits below its Flagship of the same point version. The letter scheme violated four of these
- **Cross-vendor ties reflect the evidence**: `D10` holds OpenAI and Google Flagship models and Anthropic's Balanced model whose intervals overlap; `D11` holds `gpt-6-astra` and `claude-opus-5-5` (168.8 each); no public evidence separates them
- **Specialized Apex models inherit the top of their point version**: `gpt-5.6-cyber` and `gpt-5.5-cyber` have no Epoch score and get their rung from E1 over the Flagship sibling. The rung states vendor positioning, not measured depth; Notes says so
- **`gpt-4.1-nano` is measured, not unplaced**: Epoch 129.5 with an interval overlapping `gpt-4o-mini` keeps it at `D1`; the 2025 release date does not lift it
- **Compared with the sketch proposed in the DD-10 discussion** (`gpt-4o-mini` 2, `gpt-4o` 3, `o1-mini` = `claude-3-5-sonnet` 4, `gpt-4.1` 4, `gpt-4.1-mini` 3, `gpt-4.1-nano` 2, `gpt-5` 5, `gpt-5-mini` 4, `gpt-5-nano` 3): the computed ladder is one rung lower at the bottom (`gpt-4o-mini` and `gpt-4o` tie at `D1` because their intervals overlap) and otherwise reproduces the order, with `gpt-5` one rung above `gpt-5-mini` above `gpt-5-nano`

### 3.1 Devin-Only Models

No registry entry, no Epoch row. Rungs set by hand in `MODEL_INVENTORY.md` Section 3.2 from the vendor's own positioning and the Devin cost multiplier [ASSUMED]:

- `Kimi K3` - `D9*`: [Moonshot](https://www.kimi.ai/blog/kimi-k3) states it "still trails" `claude-fable-5` (D12) and `gpt-5.6-sol` (D10); one below the lower reference [VERIFIED - LLMCAPCLS-IN01-SC-KIMI-K3]; cost 6x
- `Gemini 3.7 Flash` - `D8*`: the [Gemini API changelog](https://ai.google.dev/gemini-api/docs/changelog) routes it to `gemini-3.8-flash` (D8) since 2026-10-08 [VERIFIED - LLMCAPCLS-IN01-SC-GOOG-APICHG]
- `Gemini 3.5 Flash` - `D7*`: routed to `gemini-3.6-flash` (D7) [VERIFIED - LLMCAPCLS-IN01-SC-GOOG-APICHG]
- `SWE-1.7` - `D6*`: [Cognition](https://www.linkedin.com/posts/jefflinwang_weve-released-swe-17-our-best-model-yet-activity-7480867805618438146-J56D) states it is trained from Kimi K2.7, a 2025-2026 Flagship-class base; cost 1x [VERIFIED - LLMCAPCLS-IN01-SC-COG-SWE17; rung ASSUMED]

## 4. From Depth to Prompt Shape

Depth answers "how much may stay implicit"; Items answers "how many explicit instructions survive one run". Both are read from the inventory row; the prompt-writing agent computes nothing else.

```
  Inventory row ──> Depth ──> effort shift ──> effective rung ──> explicitness level ──> items per unit
                └─> Items ─────────────────────────────────────────────────────────────> prompt count
                └─> Notes: scope guard, CSV rows, adaptive Medium warning ───────────────> prompt text
```

### 4.1 Explicitness Level per Rung

Fixed per absolute rung. A model's recipe does not change when deeper models arrive, because the model did not change. Boundaries [ASSUMED], calibrated by ledger Items (Section 4.3):

- **D10 and above - goal-level**: state outcome, constraints, acceptance check. The model finds files and infers steps. Several reasoning units per prompt
- **D7-D9 - outcome-level**: outcome per unit plus named files plus acceptance check. The model infers steps inside the named files. This is the granularity TASKS items are written at (TASKS_GUIDES Section 3), so one unit = one item
- **D4-D6 - step-level**: each edit named (file, location, change) and expected output stated. One reasoning unit per prompt; no cross-file inference expected. One unit expands to 2-3 items
- **D1-D3 - keystroke-level**: exact old and new text or exact command, exact verification command, nothing implicit, no rationale text. One unit expands to 4-6 items

Expansion factors are writing heuristics: an outcome-level item "add retry with backoff to the three fetch calls in `client.py`" becomes three step-level items (one per call, each with the expected signature) or six keystroke-level items (old text, new text per call).

### 4.2 Effort Shift

The rung describes High effort (`H`). Other efforts read the model as a shallower rung before applying Section 4.1 [sizes ASSUMED; direction VERIFIED - LLMCAPCLS-IN01-SC-TBLF-IN02]:

- `X`, `MX`: no shift (no evidence that XHigh or Max completes more items than High; cost rises)
- `M`: no shift, except `adaptive_thinking` prefixes (Claude 4.6 and later): one rung lower. `TBLF-IN02`: `claude-opus-4-6` 6 rows at Medium against 667 at High; `TBLF-IN03` E1 traces it to adaptive thinking skipping the reasoning phase
- `L`: one rung lower. `gpt-5-mini` 65 rows at Low against 500 at Medium
- `-` (no reasoning): two rungs lower. `gpt-4o` 4 rows, `gpt-4o-mini` 6, `claude-haiku-4-5` without thinking 9

Example: `claude-opus-5` (D9) at Medium reads as D8 (still outcome-level); `claude-haiku-5-5` (D8) at Medium reads as D7; `gpt-4.1` (D3, `-`) reads as D1.

### 4.3 Items and Shape Parameters

**Items** = numbered instruction items per implementation prompt that complete with zero skips.

- **Measured** (preferred): largest `items_planned` with `items_done == items_planned` over `>= 3` sequences in `partition-observations.jsonl`, aggregated by `/session-finalize` into `observed.items` (IN07 Sections 6-7) [VERIFIED - LLMCAPCLS-IN01-SC-IPPS-IN07]. `glm-5.2`: 7 prompts in 2 sequences, 4-12 items, 100% done with strict scope guard → provisional Items 8 until a third sequence is logged [VERIFIED - LLMCAPCLS-IN01-SC-IPPS-IN05 Section 9]
- **Default** until measured, from the effective rung: `D10+` 8, `D7-D9` 6, `D4-D6` 5, `D1-D3` 4 [ASSUMED - the former profile constants]
- **Shape parameters** keyed to Items, not to a profile name: Items 8 → max_files 6, checkpoint every 3 prompts; Items 6 → max_files 3, checkpoint every 2; Items 5 or less → max_files 2, checkpoint after every prompt [ASSUMED - IN06 Section 4]
- **Scope guard**: Notes `scope guard strict` when a FAILS or ledger entry documents unrequested actions (`glm-5.2`, OverAct SIR 2.00, IN06 Section 3 [VERIFIED - LLMCAPCLS-IN01-SC-IPPS-IN06]). Adds "Do ONLY the numbered items below. Do not refactor, rename, add tests, or touch files not listed. Report any item you could not complete as NOT DONE" to every prompt. Does not lower Items: the `glm-5.2` ledger shows 100% completion with the guard in place

Measured Items override the default in both directions; a skip observation (`items_done < items_planned`) with `sequences >= 3` lowers Items to the largest fully completed `items_planned`. Items never changes the rung: completion capacity and depth are separate axes (IN06 Section 2: GLM-5.2 at High still skipped items before the guard, so effort and depth did not fix it).

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

- **`claude-opus-5`** (D9 outcome-level, Items 6 default, max_files 3): expanded 18; `max(ceil(18/6), ceil(7/3), 3)` = 3 prompts; checkpoint after prompt 2, then Final Checkpoint; about $9 per 1M-token prompt → $27
- **`gpt-5.6-luna`** (D8 outcome-level, Items 6 default): same shape, 3 prompts; $0.40 per prompt → $1.20. Same prompt count as Opus 5 is the expected result of equal explicitness level; what differs is the risk that D8 fails an inference D9 would make, visible only in the ledger
- **`glm-5.2`** (D6 step-level, Items 8 provisional measured, max_files 6, scope guard strict): expanded 18 × 2.5 = 45; `max(ceil(45/8), ceil(7/6), 3)` = 6 prompts; checkpoint every 3; $2.00 per prompt → $12
- **`claude-haiku-4-5`** (D4 step-level, Items 5 default, max_files 2): expanded 45; `max(9, 4, 3)` = 9 prompts, checkpoint after every prompt; $1.80 per prompt → $16

The former formula gave `glm-5.2` 6 prompts from WF 0.5 (capacity) and Opus 5 3 prompts from items; the new formula reaches the same counts from explicitness and measured Items, without a model-specific HWH factor.

## 5. Producing MODEL_INVENTORY.md

Proposed changes; nothing below is applied yet. `MODEL_INVENTORY.md` stays a generated, data-only view of the registries (GRUC separation); agents never compute rungs or Items themselves.

```
  model-registry.json ─────────┐  uc_class, release_date, eci_score, eci_ci,
  model-pricing.json ──────────┤  deeper_than, depth, depth_evidence, items,
  model-parameter-mapping.json ┤  scope_guard, observed, effort levels, context
  windsurf-model-registry.json ┘  Devin cost, Devin-only models
              │
              v  layer-depth-ladder.py (insert-only)  ──>  update-model-inventory.py
  MODEL_INVENTORY.md ──> /write-tasks-plan, /write-strut, /write-prompts, /verify
              ^
              │  /session-finalize: ledger → registry.observed → items, scope_guard review
  _agent_work/partition-observations.jsonl  <── Final Checkpoint of every prompts file
```

### 5.1 Registry Properties (1.12.0)

Per `model-registry.json` model entry:

- Keep: `uc_class` (E1 input), `release_date`, `release_date_assumed`, `eci_score`, `observed`, `status`, `enabled`, `context_window`
- Add: `eci_ci` `[low, high]` from the Epoch CSV (E3 input); `depth` integer, written once by the layering script; `depth_evidence` string (`"E3 > gpt-5.4-pro"`, `"E1 > claude-sonnet-5-5"`, `"E6 from glm-4.7"`); `depth_estimated: true` for E6 rungs; `deeper_than` list of `{model, kind, source, accessed, statement}` for manual E1 and E4 edges (Section 2.6); `items` integer or `null` (measured, from `observed`); `scope_guard: "strict"` where documented
- Remove: `capability_label`, `eci_band`, `eci_band_source`, `gen_equivalent`, `behavior_profile`, `capability_note` (evidence moves to `depth_evidence` and `deeper_than`)
- `observed` gains `items` (largest fully completed `items_planned`) next to the existing `if`, `eg`, `sequences`, `self_audited_prompts`; `profile_suggested` is dropped

### 5.2 Inventory Structure and Columns

Sections of `MODEL_INVENTORY.md`:
1. Definitions - Depth, Items, HWH, context; one line each
2. Value Derivation - evidence kinds E1-E6 (one line each), insertion rule, effort shift, Items default and shape parameters, scope guard, prices. About 15 lines against the current 40 (anchor, letters, Comp, WF formula, profile thresholds, change rule gone)
3. Model table, header line `Top rung: D12 (2026-11-02)`, 3.1 API models, 3.2 Devin-only models
4. Maintenance - script regeneration, insert-only guarantee, Items and scope guard review, manual edge review

Columns: `Model | Depth | Items | Context | Efforts | In USD | Cache USD | Out USD | Devin cost | Notes`

- **Depth** - `D11`, `D2*` (estimated). Never changes except `*` → measured
- **Items** - measured values carry `m` (`8m`); defaults per Section 4.3 carry no marker
- **Notes** - `depth_evidence`; `UC-n`; Epoch score with interval (`168.8 [165.3-174.0]`) or `no Epoch score`; status `legacy` / `deprecated` / `no_access`; `scope guard strict`; `CSV rows` marker; adaptive-thinking Medium warning; `unplaced`
- Removed: `Label`, `Comp YY`, `Profile`, `WF`

Sort: Depth descending, then Model ascending. Prompts files cite `Depth` and `Items`; both are stable.

### 5.3 Scripts

- **`layer-depth-ladder.py`** (new, from `_agent_work/.tmp_dominance_ladder.py`): reads registry and the run's Epoch match file; builds E1, E2, E3, E5 edges plus manual `deeper_than`; for models with `depth` present it verifies the stored rung is still consistent (reports, never rewrites); for models without `depth` it applies the online insertion rule (Section 2.4) and writes `depth`, `depth_evidence`, `depth_estimated`; applies E6 for unscored models; aborts on a cycle and names the two edges. `--bootstrap` performs the one-time Section 2.3 layering and is refused when any `depth` exists
- **`match-epoch-eci.py`**: keeps download and name matching; outputs `eci_score`, `eci_ci_low`, `eci_ci_high`; drops `eci_band`, `band_action`, `gen_equivalent`, and the UC inference (`uc_class` is human-set in the registry; the script lists new models whose `uc_class` is missing)
- **`update-model-inventory.py`**: removes `anchor`, `letter_index`, `label_from`, WF formula, profile and Comp columns; reads `depth`, `items`, `scope_guard`; renders the header `Top rung`; keeps `CSV rows` and adaptive Medium markers, price columns, Devin-only Section 3.2
- **`verify-and-distribute-registry.ps1` Gate 9.4**: every text model not `retired` has `depth`; no `depth` differs from the previous committed registry except `depth_estimated` → measured; every `deeper_than` entry has a source; inventory sort order; `Top rung` equals max `depth`

### 5.4 Template Changes (`_PROMPTS_ModelInventoryUpdate_TEMPLATE.md`)

- Header: `[CAPABILITY_SCHEME]` values `LADDER | NONE` (was `UC_ECI | YY_L | NONE`); script list entries for `match-epoch-eci.py` and `update-model-inventory.py` reworded; new `layer-depth-ladder.py` entry; Prompt 4 and Prompt 6 descriptions in the load-based partition table
- Prompt 4: title "Capability Evidence: Epoch ECI scores and intervals"; item 2 appends `eci_score`, `eci_ci_low`, `eci_ci_high` for new models; item 3 verifies intervals present or `fallback_note`; the band-freeze sentence (R2) is removed
- Prompt 5 item 2: capability fields incorporated from the match file are `eci_score`, `eci_ci`; `uc_class` and `release_date` are set by hand for new models with the provider page as source
- Prompt 6 item 2 (Phase 9.4) becomes: 1) `release_date` and `uc_class` for new models, 2) run `layer-depth-ladder.py` (insert-only), 3) review reported squeezes and manual-edge candidates, 4) `items` and `scope_guard` from `observed` review, 5) `format-model-registry.py`, 6) `update-model-inventory.py`. The May 1 wrap bullet is removed. Columns and sort order updated
- Prompt 6 item 3: Gate 9.4 description per Section 5.3
- Example block comments: `UC_ECI` → `LADDER`

### 5.5 Consumers

Documents that read the inventory and currently name Label, Comp, Profile, or WF:

- `PROMPTS_GUIDES.md` Section 1c (WF paragraph), 1f step 3 (budget = Items and 1 HWH cap), 1g (rewritten as Section 4 of this document), Section 5 (`max_items` → Items)
- `TASKS_GUIDES.md` Section 1 (default row: `D7-D9`, Items 6), Section 3 (`Est <= WF` → `Est <= 1 HWH`, expanded items `<= Items`, files `<= max_files`), Sections 5-6
- `PROMPTS_RULES.md` PRMT-SC-05: commentary states Depth, effective rung after effort shift, explicitness level, Items, prompt count, cost; strict guard check keyed to Notes
- `write-prompts.md` Step 1, `edird-phase-planning` SKILL.md step sizing, `PROMPTS_TEMPLATE.md` and `PROMPTS_EXAMPLE_01` commentary rows
- `NOTES.md` of this session: DD-01 (`UC_ECI`) superseded by DD-10 option 3; DD-02 (fixed caps) and DD-03 (drop profiles) absorbed; T02 `IN01` Section 5 decisions updated

## 6. Using the Inventory in Partitioned Documents

Lookup inputs: `intended_model`, `effort`, context window. Output: one row with Depth, Items, Efforts, Context, prices, Notes. Then Section 4: effort shift → explicitness level → expanded items → prompt count and shape.

- **TASKS** - items are written at outcome-level (Section 4.1 `D7-D9` granularity) and carry `Est: [N] HWH`. A task executed by one prompt must satisfy `Est <= 1 HWH` and, after expansion for the target model, `expanded_items <= Items` and `files <= max_files`; larger tasks are split. The TASKS document itself is model-independent; expansion happens in `/write-prompts`
- **STRUT** - a step executed by one prompt satisfies `step HWH <= 1` and the same item and file limits. Replaces the ">30 min AWH = decompose" rule in `edird-phase-planning` with a model-aware check
- **Prompts files** - frontmatter `intended_model`, `effort`, `context_window_size` from the row; opening commentary states Depth, effective rung, explicitness level, Items, prompt count, cost estimate; every implementation prompt holds `<= Items` numbered items at the stated explicitness level and `<= max_files` files; checkpoints per `checkpoint_interval`; `scope guard strict` text when Notes says so; critical items first and last; input per prompt `<= 50%` of Context
- **Verify** (PRMT-SC-05) - recomputes the bounds from the row and the prompts file and fails on: items above Items, files above max_files, missing checkpoint, missing scope guard, explicitness level below the rung's requirement (for example outcome-level items in a `D5` prompts file)

## 7. HWH and AWH

Unchanged from v1 Section 10 except that WF is gone. Two units remain:

```
  HWH  "How big is the job?"     task size, model-independent   → TASKS Est, 1 HWH per prompt cap, cost
  AWH  "How long will I wait?"   agent wall-clock, model-dependent → STRUT phase budgets, scheduling
```

- **HWH (Human Work Hours)** - hours a skilled human expert needs without AI, including reading, editing, verifying. Same unit [METR](https://metr.org/time-horizons/) and [Anthropic](https://www.anthropic.com/research/estimating-productivity-gains) use to size tasks [VERIFIED - LLMCAPCLS-IN01-SC-METR-TH, LLMCAPCLS-IN01-SC-ANTH-PROD]. Estimate in buckets 0.25 / 0.5 / 1 / 2 HWH; split at 4 (agent success falls steeply above about 4 human hours, METR: under 10%) [VERIFIED - LLMCAPCLS-IN01-SC-METR-BLOG; buckets ASSUMED]
- **AWH (Agent Work Hours)** - wall-clock time the agent runs. Default before data `AWH ≈ 0.2 × HWH` (Anthropic's estimated 80% task-time reduction; self-estimated and human-in-the-loop, so [ASSUMED] for unattended runs). With data: `prompt_count × observed minutes per prompt` from STRUT Time Logs. Not applicable in large familiar codebases, where [METR's randomized controlled trial (RCT)](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) measured experienced developers 19% slower with early-2025 tools [VERIFIED - LLMCAPCLS-IN01-SC-METR-RCT, LLMCAPCLS-IN01-SC-METR-UPLIFT]
- **Why no model factor on HWH**: WF claimed "HWH one prompt completes without skipping" per model. METR's own 80%-reliability horizons carry factor-2 error bars [VERIFIED - LLMCAPCLS-IN01-SC-METR-LIMIT], the `TBLF-IN02` test showed effort and thinking method outweigh two capability bands, and the ledger measures items, not hours. Items (measured) plus the 1 HWH cap replace WF; the cap is the one place where HWH still bounds a prompt

One-paragraph explanation: "HWH says how big a job is for a skilled human; no prompt should carry more than one. Depth says how much the model may be left to infer, so a shallower model gets the same job spelled out in more items. Items says how many of those items one prompt may hold before the model drops some. Divide expanded items by Items and you have the prompt count. AWH, the time you wait, starts at one fifth of HWH and is replaced by measured minutes per prompt."

## 8. Limitations

- **Cross-vendor equality is coarse**: `D10` holds seven models from three vendors whose intervals overlap, `D11` an OpenAI and an Anthropic model with equal scores. Equal rung means equal prompt shape, not equal quality; vendor choice stays with the author
- **E1 relies on `uc_class` being right**: the lineup class is set by hand for new models (`sol` / `terra` / `luna`, `grok-build`). A wrong class propagates through E1. The layering script cannot detect it; the price order within a point version is the review check
- **Cross-version edges depend on the vendor's guidance page staying current**: EC-1 reads Anthropic's model-selection guidance at one date; when the vendor rewrites it (next Opus release), the recorded edge keeps its date and source and is not revisited. The edge is append-only like every rung
- **EC-2 inheritance is a rule, not a vendor statement**: Fable 5 is above Opus 5.5 because Fable 5.1 is and the two share tier, generation, and price; the vendor never compared Fable 5 with Opus 5.5 directly
- **Specialized Apex models inherit the top**: `gpt-5.6-cyber` at `D11` and `gpt-5.5-cyber` at `D10` rest on E1 from `uc_class` alone; `o3-deep-research` and `o1-pro` likewise. EC-4 requires the announcement statements to be cited before registry 1.12.0 is written
- **Epoch coverage gaps**: 24 of 100 registry models have no Epoch row and `gpt-5` has a score without an interval; 5 rungs are E6 estimates (`*`), 2 are unplaced. GLM Efficient and vision models are placed by tier offset only
- **Bootstrap vs insertion order**: the Section 2.3 layering is order-independent; later insertions are not. A model squeezed between two frozen rungs ties with the lower one. Expected mid-ladder, rare at the top
- **Explicitness boundaries and Items defaults are unmeasured**: `D10+` / `D7-D9` / `D4-D6` / `D1-D3` and 8 / 6 / 5 / 4 come from the former profile constants; only `glm-5.2` has a measured Items. The ledger is the only calibration path
- **Effort shift sizes are assumed**: direction is measured on three configurations (`TBLF-IN02`); the one-rung and two-rung sizes are not
- **Observations depend on the execution framework**: framework explains 56% of over-eagerness variance, base model 21% ([SNARE](https://arxiv.org/abs/2605.28122)) [VERIFIED - LLMCAPCLS-IN01-SC-SNARE]. Ledger lines carry `engine`; Items measured under `cascade` may not hold under `claude-code`
- **The E6 `*` → measured transition is the one rung change**: it breaks the append-only guarantee for estimated rungs only; Gate 9.4 allows exactly this change
- **The ladder is a session artifact until applied**: `.tmp_dominance_ladder.py` and `.tmp_manual_edges.json` live in `_agent_work/`; no canonical file carries `depth` yet
- **Two registry release dates are wrong** (EC-9): `claude-fable-5-1` 2026-09-01 per vendor (registry 2026-09-25), `claude-opus-5-5` announced 2026-09-22 (registry 2026-10-14). E2 ordering is unaffected in both cases

## 9. Next Steps

1. **DD-11 closed 2026-11-02**: both `claude-fable-5-1` and `claude-fable-5` recorded above `claude-opus-5-5` (Section 2.6 EC-1, EC-2); `.tmp_manual_edges.json` holds the two `deeper_than` entries with sources
2. **DD-12 approved 2026-11-02**: `_SPEC_MDLRGUP-MDLINVNTRY-01_DepthLadder.md` in `T02_MDLINVNTRY_ReliableModelInventory_2026-10-28` carries Sections 2, 4, 5 as requirements; `/write-impl-plan` follows
3. Promote `.tmp_dominance_ladder.py` to `layer-depth-ladder.py` with E6, `deeper_than` from the registry, insert-only mode, and `--bootstrap`; add a test that re-layers the 2026-10-28 snapshot with the two manual edges and reproduces Section 3
4. Cite the EC-4 announcement statements for `gpt-5.6-cyber`, `gpt-5.5-cyber`, `o3-deep-research`, `o1-pro`, `o4-mini-deep-research` before registry 1.12.0 is written
5. Record in the session PROBLEMS.md during `/session-save`: `MDLRGUP-MDLINVNTRY-PR-0004` (ECI letter misordering, Section 1) and `MDLRGUP-MDLINVNTRY-PR-0005` (release dates of `claude-fable-5-1` and `claude-opus-5-5`, EC-9)
6. Mark DD-01, DD-02, DD-03 in session NOTES.md and T02 `IN01` Section 5 as superseded or absorbed during `/session-save`

## 10. Sources

**Primary Sources (providers, research organizations, local files):**
- `LLMCAPCLS-IN01-SC-EPOCH-CSV`: https://epoch.ai/data/eci_scores.csv - Epoch Capabilities Index scores with 95% confidence intervals per model; snapshot 2026-10-28 in `_2026-10-28_PRICES/2026-10-28_eci-leaderboard.csv`, matched to registry IDs in `2026-10-28_Epoch-ECI-Match.json` (76 of 100 models scored) [VERIFIED]
- `LLMCAPCLS-IN01-SC-IPPS-LADDER`: `_agent_work/.tmp_dominance_ladder.py`, `.tmp_ladder.json`, `.tmp_ladder.txt`, `.tmp_manual_edges.json`, `.tmp_ladder_dd11.json` - E1/E2/E3/E5 edge construction plus manual `deeper_than` edges and fixed-point layering over 92 text models; result 11 rungs without and 12 rungs with the two Fable edges, no cycle, no contradiction; first run with release-order insertion produced 22 conflicts (2026-11-02) [TESTED]
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

**[2026-11-02 13:20]**
- Added: Section 2.6 edge-case catalogue EC-1 to EC-9, each with source type, rule, and status; sources `LLMCAPCLS-IN01-SC-ANTH-FABLE51-OVW`, `-FABLE51-NEW`, `-OPUS55`, `-FABLE5`
- Changed: DD-11 closed - `claude-fable-5-1` and `claude-fable-5` recorded above `claude-opus-5-5` from Anthropic's model-selection guidance; ladder re-run to 12 rungs (`D12` Fable 5, Fable 5.1, Mythos 5, Mythos 5.1); Summary, Sections 2.5, 3, 3.1, 8 updated
- Changed: DD-12 approved - Next Steps point to `_SPEC_MDLRGUP-MDLINVNTRY-01_DepthLadder.md`
- Added: EC-9 release-date findings for `claude-fable-5-1` and `claude-opus-5-5`

**[2026-11-02 12:50]**
- Changed: capability representation from year-letter labels on ECI bands to an append-only dominance ladder (`D1`, `D2`, ...) with evidence kinds E1-E6 (DD-10 option 3); Sections 1-6 rewritten; v1 kept as `_INFO_HOW_TO_ORGANIZE_LLMS_BY_CAPABILITY_v1.md`
- Added: computed ladder for 92 models (11 rungs, Section 3), Devin-only rungs, explicitness level per rung, effort shift, Items axis with measured override, partition formula without WF, registry 1.12.0 fields, script and template change list, DD-11 and DD-12
- Removed: Comp, May 1 wrap, year anchor, WF formula, behavior profiles, profile thresholds and change rule, METR WF sanity check
- Added: sources `LLMCAPCLS-IN01-SC-EPOCH-CSV`, `LLMCAPCLS-IN01-SC-IPPS-LADDER`, `LLMCAPCLS-IN01-SC-IPPS-IN05`

**[2026-10-29 14:30]**
- Changed: letter definition from UC tier to Epoch ECI band relative to a year anchor; Comp, May 1 wrap, WF from band, `release_date` and `eci_band_source` fields, TBLF cross-check (v1)

**[2026-10-29 13:37]**
- Changed: R2 mapped UC tiers to letters; R3 release-month gate; 40 label changes (v1)

**[2026-10-28 18:05 - 20:10]**
- Initial research document and eight revisions: year-letter labels, October promotion rule, WF formula, behavior profiles, inventory production, HWH and AWH, GRUC separation (v1 Section 13 lists each)
