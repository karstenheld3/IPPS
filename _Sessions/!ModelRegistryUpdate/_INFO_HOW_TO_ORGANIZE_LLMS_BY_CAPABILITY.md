# INFO: How to Organize LLMs by Capability

**Doc ID**: LLMCAPCLS-IN01
**Goal**: Define time-stable model capability labels, a behavior profile per model, and how `MODEL_INVENTORY.md` is produced from them and used to partition TASKS, STRUT, and prompts files by model, effort, and context window
**Timeline**: Created 2026-10-28, Updated 7 times (2026-10-28 - 2026-10-28)
**Target file**: `PromptSystemV4.5/skills/write-documents/MODEL_INVENTORY.md`, `PromptSystemV4.5/skills/llm-evaluation/model-registry.json`, `update-model-registry.md`

**Depends on:**
- `_INFO_MDLBHVPRM-06_ModelAwarePartitioning.md [MDLRGUP-MDLBHVPRM-IN06]` for capacity, instruction following, and eagerness axes and decision MDLBHVPRM-DD-01 (observation overrides benchmarks)
- `_INFO_MDLBHVPRM-07_PromptFeedbackLoop.md [MDLRGUP-MDLBHVPRM-IN07]` for the checkpoint ledger that calibrates WF

## Summary

- **Generation-relative classes go stale**: the former `MODEL_INVENTORY.md` Class A-D was defined as "frontier" / "previous frontier generation", so every release cycle forced a re-grade of the whole table [VERIFIED - LLMCAPCLS-IN01-SC-IPPS-MINV]
- **Applied on 2026-10-28**: `MODEL_INVENTORY.md` now uses labels, profiles, and the three-limit prompt count; `model-registry.json` 1.10.0 carries `capability_label`, `capability_note`, `behavior_profile` for 28 models; `update-model-registry.md` step 9.4 maintains them [VERIFIED - LLMCAPCLS-IN01-SC-IPPS-MINV, LLMCAPCLS-IN01-SC-IPPS-MREG]
- **Year-letter labels `YY-L` are permanent**: `YY` = release year, `L` = capability bucket within that year (A = top, H = small local models). A label never changes because a newer model appears [ASSUMED]
- **One letter equals one year of progress**: `26-B ≈ 25-A`. This makes the workload factor (WF, Human Work Hours one prompt completes) absolute: `WF_high = 2.0 * 0.5^letter_index * 2^(YY - 26)` [ASSUMED - calibrate with ledger]
- **YY-A is assignable only from October of YY**: until end of September the highest label of year YY is `YY-B`. On the October review the year's top models are promoted to `YY-A`, regardless of release month. Labels of year YY are provisional until December 31; promotion is the only upward change and errs conservative (WF underestimated before October) [ASSUMED - rule design]
- **Release timing supports the October cut only partly**: 2024 and 2025 flagships ([OpenAI GPT-5.2](https://openai.com/index/introducing-gpt-5-2/), [Google Gemini 3](https://blog.google/products-and-platforms/products/gemini/gemini-3/), [Anthropic models](https://www.anthropic.com/news/models)) clustered in September to December (o1, Gemini 3 Pro, GPT-5.1, Claude Opus 4.5, GPT-5.2). 2026 flagships shipped June to September (Claude Fable 5, Claude Opus 5, GPT-6 Astra). Promotion instead of release date covers both patterns [VERIFIED - LLMCAPCLS-IN01-SC-OAI-GPT52, LLMCAPCLS-IN01-SC-GOOG-GEM3, LLMCAPCLS-IN01-SC-ANTH-OPUS45, LLMCAPCLS-IN01-SC-ANTH-FABLE5, LLMCAPCLS-IN01-SC-ANTH-OPUS5, LLMCAPCLS-IN01-SC-NAIM-TMLN]
- **Labels can encode the current inventory**: 35 of 37 rows keep their WF; `gpt-5.2` and `claude-opus-4-5` change (0.5 → 1.0 at High). Labels were chosen to reproduce current values, so this shows compatibility, not independent validation [ASSUMED - Section 6]
- **Two independent dimensions per model**: capability label (how much work per prompt, WF) and behavior profile `precise` / `standard` / `guarded` (prompt shape: max_items, max_files, checkpoint_interval, scope_guard). Profile comes from ledger instruction following (IF) and eagerness (EG), then documented observations, then benchmarks; no data = `standard` [VERIFIED - LLMCAPCLS-IN01-SC-IPPS-IN06, LLMCAPCLS-IN01-SC-IPPS-IN07]
- **Prompt count = maximum of three limits**: `ceil(task_HWH / WF)`, `ceil(items / max_items)`, `ceil(files / max_files)`. For a task of 3 Human Work Hours (HWH) Claude Opus 5 is limited by items (3 prompts), GLM-5.2 by capacity (12 prompts) [ASSUMED - Section 9.3]
- **MODEL_INVENTORY.md is generated from the registries**: registry holds `capability_label`, `behavior_profile`, `observed`; inventory adds WF per effort and price; agents read only the inventory [ASSUMED - design, Section 8]
- **HWH, WF, AWH answer three questions**: HWH = how big is the job (human expert hours, model-independent, same unit as [METR](https://metr.org/) (Model Evaluation and Threat Research) and [Anthropic](https://www.anthropic.com/research/estimating-productivity-gains)); WF = how much fits in one prompt; Agent Work Hours (AWH) = how long the agent runs. Estimate HWH in buckets 0.25 / 0.5 / 1 / 2 HWH, split at 4 [VERIFIED - unit definition; buckets ASSUMED]
- **AWH starts at 0.2 × HWH, then gets measured**: default from Anthropic's estimated 80% task-time reduction; replaced by observed minutes per prompt from STRUT Time Logs. Not valid for large familiar codebases, where METR's randomized controlled trial (RCT) measured AI-assisted work as up to 19% slower [VERIFIED - LLMCAPCLS-IN01-SC-ANTH-PROD, LLMCAPCLS-IN01-SC-METR-RCT; default ratio ASSUMED]
- **WF values are plausible against METR**: Claude Opus 4.5 80%-reliability horizon about 1 h (derived from the 50% horizon) vs WF 1.0 HWH for its proposed label `25-A`; METR's 1-4 doublings per year make the one-doubling-per-year label rate conservative [VERIFIED - LLMCAPCLS-IN01-SC-METR-LIMIT, LLMCAPCLS-IN01-SC-METR-BLOG]
- **Registry is behind**: GPT-6 Sol (2026-09-22), Claude Opus 5.5 (2026-09-22), Gemini 4 Argon (2026-10-13) are released but missing from `model-registry.json` 1.9.0 [VERIFIED - LLMCAPCLS-IN01-SC-NAIM-TMLN]

## Table of Contents

1. [Problem with Generation-Relative Classes](#1-problem-with-generation-relative-classes)
2. [Year-Letter Label Format](#2-year-letter-label-format)
3. [Release Timing and the October Rule](#3-release-timing-and-the-october-rule)
4. [Workload Factor Formula](#4-workload-factor-formula)
5. [Assignment Rules](#5-assignment-rules)
6. [Proposed Labels for the Current Inventory](#6-proposed-labels-for-the-current-inventory)
7. [Behavior Profile: Assessing How a Prompt Must Be Shaped](#7-behavior-profile-assessing-how-a-prompt-must-be-shaped)
8. [Producing MODEL_INVENTORY.md](#8-producing-model_inventorymd)
9. [Using the Inventory in Partitioned Documents](#9-using-the-inventory-in-partitioned-documents)
10. [Explaining and Converting HWH and AWH Estimates](#10-explaining-and-converting-hwh-and-awh-estimates)
11. [Limitations](#11-limitations)
12. [Sources](#12-sources)
13. [Document History](#13-document-history)

## 1. Problem with Generation-Relative Classes

`MODEL_INVENTORY.md` Section 2 defines capacity classes by position relative to the newest models:

- Class A = "frontier models"
- Class B = "strong models, previous frontier generation"
- Class C = "mid models"
- Class D = "small or fast models"

When a new frontier model ships (11 major releases in 2026 up to October, see Section 3.1), every existing model moves down one class. The WF of the model itself did not change, but its label did. Consequences:

- Every model release requires a manual re-grade of all rows
- Prompt files written earlier reference a class whose meaning has shifted
- WF is coupled to the label, so WF values silently change meaning

Requirement for a replacement: the label of a model must be assigned once and stay true; WF must be derivable from the label alone.

## 2. Year-Letter Label Format

Format: `YY-L`

- `YY` - two-digit release year (general availability via API or product)
- `-` - separator (readability; `26-C` instead of `26C`)
- `L` - capability letter within that year, A (highest) to H (lowest)

Letter meaning within one year:

- **A** - top models of the year (assignable only from October, see Section 3)
- **B** - flagship models; highest label before October
- **C** - mid models (balanced price and capability)
- **D** - small models (mini variants, fast models)
- **E** - very small models (nano variants)
- **F, G, H** - very small optimized models that can run locally

```
         Letter:  A      B      C      D      E      F      G      H
                  │      │      │      │      │      │      │      │
  25-L  WF_high:  1.0    0.5    0.25   0.13   0.06   0.03   0.02   0.01
  26-L  WF_high:  2.0    1.0    0.5    0.25   0.13   0.06   0.03   0.02
  27-L  WF_high:  4.0    2.0    1.0    0.5    0.25   0.13   0.06   0.03
  Cross-year link: 26-B (1.0) = 25-A (1.0), 27-B (2.0) = 26-A (2.0). One letter step = one year
```

Examples from the 2025 OpenAI lineup:

- `25-A` - GPT-5.2 (top 2025 OpenAI model, December release)
- `25-B` - GPT-5 (August flagship)
- `25-C` - GPT-5 Mini
- `25-D` - GPT-5 Nano
- `25-E` - less capable models of 2025

## 3. Release Timing and the October Rule

### 3.1 Evidence

Major releases per year, from [Next AI Model timeline](https://www.nextaimodel.com/timeline) and [AI Release Index](https://aireleaseindex.com/), key dates confirmed by provider announcements ([OpenAI GPT-5](https://openai.com/index/introducing-gpt-5/), [OpenAI GPT-5.2](https://openai.com/index/introducing-gpt-5-2/), [Google Gemini 3](https://blog.google/products-and-platforms/products/gemini/gemini-3/), [Anthropic models](https://www.anthropic.com/news/models)):

- **2024**: Claude 3 Opus 2024-03-04, GPT-4o 2024-05-13, Claude 3.5 Sonnet 2024-06-20, o1 2024-09-12 (preview) / 2024-12-05, Claude 3.5 Sonnet (new) 2024-10-22 [VERIFIED - LLMCAPCLS-IN01-SC-ARIX-HOME, LLMCAPCLS-IN01-SC-BTLN-TMLN, registry ID `claude-3-5-sonnet-20241022`]
- **2025**: Gemini 2.5 Pro 2025-03-25, o3 2025-04-16, Claude Opus 4 2025-05-22, GPT-5 2025-08-07, Claude Sonnet 4.5 2025-09-29, Claude Haiku 4.5 2025-10-15, GPT-5.1 2025-11-12, Gemini 3 Pro 2025-11-18, Claude Opus 4.5 2025-11-24, GPT-5.2 2025-12-11 [VERIFIED - LLMCAPCLS-IN01-SC-NAIM-TMLN; primary: LLMCAPCLS-IN01-SC-OAI-GPT5, LLMCAPCLS-IN01-SC-ANTH-HAIKU45, LLMCAPCLS-IN01-SC-GOOG-GEM3, LLMCAPCLS-IN01-SC-ANTH-OPUS45, LLMCAPCLS-IN01-SC-OAI-GPT52]
- **2026**: Claude Opus 4.6 2026-02-05, GPT-5.4 2026-03-05, GPT-5.5 2026-04-23, Claude Opus 4.8 2026-05-28, Claude Fable 5 2026-06-09, GPT-5.6 Sol 2026-07-09, Claude Opus 5 2026-07-24, GPT-6 Astra 2026-09-04, GPT-6 Sol 2026-09-22, Claude Opus 5.5 2026-09-22, Gemini 4 Argon 2026-10-13 [VERIFIED - LLMCAPCLS-IN01-SC-NAIM-TMLN; primary for Claude Fable 5 and Claude Opus 5: LLMCAPCLS-IN01-SC-ANTH-FABLE5, LLMCAPCLS-IN01-SC-ANTH-OPUS5]

Findings (dates verified; "strongest" is a judgment) [ASSUMED]:

- In 2024 and 2025 the strongest model of the year shipped between September and December (o1, GPT-5.2, Claude Opus 4.5, Gemini 3 Pro)
- In 2026 the strongest models shipped between June and September (Claude Fable 5, Claude Opus 5, GPT-6 Astra). Only Gemini 4 Argon is an October release
- Conclusion: "yearly top releases come after September" held for 2024-2025, not for 2026. The October rule must not depend on release month

### 3.2 Rule Design

The October rule is about **when A is assigned**, not when the model was released:

- Before October 1 of year YY: the highest label any YY model can receive is `YY-B`. Reason: the year's top is not yet known, and assigning A early leaves no label for a stronger later release
- October review of year YY: the top models of YY are promoted from `YY-B` to `YY-A`. Release month does not matter (Claude Fable 5, released June 2026, becomes `26-A` on review)
- Models released October to December of YY: may receive `YY-A` directly
- After December 31 of YY: all `YY-*` labels are frozen. Only observation downgrades (Section 5, R4) change them

```
  Jan ─────────────────────── Sep │ Oct ─────────── Dec │ next year
  max label: YY-B                 │ review: promote     │ YY labels frozen
  (A reserved)                    │ top to YY-A         │ (R4 downgrades only)
```

## 4. Workload Factor Formula

WF definition (from `MODEL_INVENTORY.md` Section 1): HWH (Human Work Hours) one prompt can complete in one run at a given effort level without skipping items or truncating.

Formula at High effort:

```
WF_high = 2.0 * 0.5^letter_index * 2^(YY - 26)
letter_index: A=0, B=1, C=2, D=3, E=4, F=5, G=6, H=7
```

- Anchor: `26-A` = 2.0 HWH (same value as current Class A)
- Within a year: each letter step halves WF (same ratio as current Class A → B → C → D)
- Across years: each year doubles WF at the same letter, so `26-B` (1.0) = `25-A` (1.0) [ASSUMED - capability doubling per year is not measured; checkpoint ledger in IN07 calibrates it]
- Effort multipliers stay unchanged: Low 0.25, Medium 0.5, High 1.0, XHigh 1.5, Max 2.0 (relative to High)
- Labels are absolute: when 2027 models arrive, `26-A` keeps WF 2.0. Nothing is re-graded
- Exception within the year: a model labeled `YY-B` before October and promoted to `YY-A` doubles its WF. Prompt files written before the promotion used the lower WF and stay valid (more prompts than needed, no skipped work)

## 5. Assignment Rules

- **R1 - Year**: `YY` = year of general availability. Never changes
- **R2 - Letter**: `L` = capability bucket: choose the letter whose `WF_high` (Section 4) best matches the model's estimated capability, checked against the cross-year link (`YY-B ≈ (YY-1)-A`) and, where available, METR time horizons (Section 10.4). The rank descriptions in Section 2 (top, flagship, mid, mini) are heuristics, not the definition: a year with a large gap between top and flagship may leave a letter empty
- **R3 - October cap**: before October 1 of YY the highest assignable letter is B. October review promotes the year's top models to A. Labels freeze after December 31 of YY
- **R4 - Observation downgrade**: a documented observation (FAILS.md entry or findings-card ledger entry naming model and skipped items or out-of-scope actions) lowers the letter by one step within the same year. Notes column records the evidence. Labels never move up by observation (MDLBHVPRM-DD-01: observation overrides benchmark only toward stricter)
- **R5 - Hard limit cap**: provider-documented max output below 32K tokens caps the letter at B of its year [ASSUMED - threshold from current Class C definition "max output 8K-32K"]. Use the provider's models page, not `model-registry.json` `max_output`: registry values are configured request limits (for example 8K for `claude-haiku-4-5` while the [Anthropic models overview](https://docs.anthropic.com/en/docs/about-claude/models/whats-new-claude-4-5) documents 64K) [VERIFIED - LLMCAPCLS-IN01-SC-IPPS-MREG, LLMCAPCLS-IN01-SC-ANTH-MODELS]

## 6. Proposed Labels for the Current Inventory

Release dates from Section 3.1 sources and provider release notes (all verified). Labels applied in `MODEL_INVENTORY.md` and `model-registry.json` 1.10.0 on 2026-10-28. "Old" = former `MODEL_INVENTORY.md` class and WF at High. For models with one effort level only, WF_high is the High equivalent of the listed Medium value (Medium × 2).

**26-A (WF_high 2.0)** - October 2026 review promotes the year's top models:
- `claude-fable-5` (2026-06-09) - old A 2.0
- `claude-opus-5` (2026-07-24) - old A 2.0
- `gpt-6-astra` (2026-09-04) - old A 2.0
- `gpt-5.6-sol` (2026-07-09) - old A 2.0
- `gpt-5.5` (2026-04-23) - old A 2.0

**26-B (WF_high 1.0)**:
- `claude-opus-4-8` (2026-05-28), `claude-opus-4-7` (2026-04-16), `claude-opus-4-6` (2026-02-05) - old B 1.0
- `claude-sonnet-5` (2026-06-30), `gpt-5.6-terra` (2026-07-09), `gpt-5.4` (2026-03-05) - old B 1.0
- `GPT-5.3-Codex` (2026-02-05), `Gemini 3.1 Pro` (2026-02-19) - Devin-only, old B 1.0 [VERIFIED - LLMCAPCLS-IN01-SC-OAI-GPT53C]

**26-C (WF_high 0.5)**:
- `claude-sonnet-4-6` (2026-02-17) - old C 0.5
- `glm-5.3` (2026-08-18) - old C 0.5; registry lists 16K max output, provider value unverified (R5 would cap at B, no effect at C)
- `Kimi K3` (2026-07-16) - Devin-only, old C 0.5; Moonshot states it trails only Claude Fable 5 and GPT-5.6 Sol. Vendor self-assessment, not used for a higher letter [VERIFIED - LLMCAPCLS-IN01-SC-KIMI-K3]

**26-D (WF_high 0.25)**:
- `glm-5.2` (2026-06-16) - base 26-C, R4 downgrade to 26-D (observed skipping and over-eagerness) - old D 0.25
- `glm-5.3-flash` (2026-08-26), `glm-5.1` (2026-04-07), `glm-5` (2026-02-11) - old D 0.25 [VERIFIED - LLMCAPCLS-IN01-SC-ZAI-RELN]
- `gpt-5.4-mini` (2026-03-17), `gpt-5.6-luna` (2026-07-09) - old D 0.25
- `Gemini 3.5 Flash` (2026-05-19), `Gemini 3.6 Flash` (2026-07-31), `Gemini 3.7 Flash` (2026-08-13), `SWE-1.7` (2026-07-08) - Devin-only, old D 0.25. The Gemini API routes 3.5 Flash to 3.6 Flash and 3.7 Flash to 3.8 Flash since 2026-10-08 [VERIFIED - LLMCAPCLS-IN01-SC-GOOG-GEM37, LLMCAPCLS-IN01-SC-GOOG-APICHG, LLMCAPCLS-IN01-SC-COG-SWE17]

**25-A (WF_high 1.0)**:
- `gpt-5.2` (2025-12-11) - old C 0.5. **Changed value**: December 2025 top model; registry request limit 32K, so R5 is not triggered with either registry or provider value
- `claude-opus-4-5` (2025-11-24) - old C 0.5. **Changed value**: top 2025 model; the old "max output 8K" is a registry request limit, [Anthropic evaluated it](https://www.anthropic.com/news/claude-opus-4-5) with a 64K thinking budget (R5 not triggered) [VERIFIED - LLMCAPCLS-IN01-SC-ANTH-OPUS45]

**25-B (WF_high 0.5)**:
- `gpt-5.1` (2025-11-12), `gpt-5` (2025-08-07) - old C 0.5
- `claude-sonnet-4-5` (2025-09-29) - flagship, not top of year - old C 0.5
- `o3` (2025-04-16), `gpt-4.1` (2025-04-14, no effort: Medium 0.25) - old C 0.5
- `Gemini 2.5 Pro` (2025-03-25, no effort: Medium 0.25) - Devin-only, old C 0.5

**25-C (WF_high 0.25)**:
- `claude-haiku-4-5` (2025-10-15), `gpt-5-mini` (2025-08-07) - old D 0.25
- `Gemini 3 Flash` (2025-12-17) - Devin-only, old D 0.25

Result: 35 of 37 rows keep their WF. The labels were chosen to reproduce the current table, so this shows the scheme can encode it; it does not validate the WF values themselves.

## 7. Behavior Profile: Assessing How a Prompt Must Be Shaped

The capability label answers **how much work** one prompt carries (WF). It does not answer **how the prompt must be shaped**: how many instruction items the model completes, how often to verify, how strictly to restrict scope. IN06 showed these are separate axes: GLM-5.2 at High effort still skips items and adds unrequested work, so raising effort or capacity does not fix it [VERIFIED - LLMCAPCLS-IN01-SC-IPPS-IN06 Section 2].

```
  Axis                    Measured by                         Controls
  ──────────────────────  ──────────────────────────────────  ─────────────────────────────────────
  Capacity                capability label + effort           WF → prompt count
                          + context window + max output       context fit per prompt
  Instruction following   IF = items_done / items_planned     max_items, checkpoint_interval
  Eagerness               EG = 1 + extra_actions /            scope_guard, max_files
                               items_planned
```

### 7.1 Profile Thresholds

Three behavior profiles. Names are words, not letters, so they never collide with `YY-L` letters (replaces IN06 TIER-A/B/C):

- **precise** - IF >= 0.90 and EG <= 1.20
- **standard** - neither precise nor guarded
- **guarded** - IF < 0.75 or EG > 1.50

Thresholds from IN07 Section 7 `tier_suggested` rule [VERIFIED - LLMCAPCLS-IN01-SC-IPPS-IN07]. Profile is independent of effort level: one profile per model.

### 7.2 Evidence Priority

Assign the profile from the highest available evidence level:

1. **Ledger observations** - `observed.if` and `observed.eg` in `model-registry.json`, aggregated by `/session-finalize` from `partition-observations.jsonl` (IN07 Sections 6-7). Used only when `sequences >= 3`; the script writes `profile_suggested`, a human sets `behavior_profile`
2. **Documented observation** - FAILS.md entry or findings-card entry naming the model and the skipped items or out-of-scope actions. Overrides benchmarks toward stricter only (MDLBHVPRM-DD-01). GLM-5.2 is `guarded` by this level
3. **Benchmark seed** - IFEval-Hard (instruction following), OverAct SIR and OverEager rate (eagerness). Plain IFEval is not used ([benchgap IFEval estimates](https://benchgap.net/b/ifeval/current)): it rates GLM-5.2 at 93.2% (estimated), within 0.3 points of GPT-5.4 (93.5%), contradicting observed skipping [VERIFIED - LLMCAPCLS-IN01-SC-IPPS-IN06 Section 3, LLMCAPCLS-IN01-SC-BGAP-IFEVAL]
4. **No data** - `standard` [ASSUMED - IN07 Section 9 bootstrap proposal]

Change rule (prevents oscillation): IF is measured under the item load the current profile allows, so a `guarded` model scoring IF 0.95 on 4-item prompts proves nothing about 8-item prompts. Profiles therefore move one step at a time. Upgrade only after 3 sequences at the current profile meet the next profile's threshold, then wait for 3 new sequences before the next upgrade. Downgrade immediately on a documented observation [ASSUMED - rule design]

### 7.3 Partition Parameters per Profile

From IN06 Section 4 and Option 2 [VERIFIED - LLMCAPCLS-IN01-SC-IPPS-IN06]; values themselves [ASSUMED] until calibrated by the ledger:

- **precise** - max_items 8, max_files 6, checkpoint_interval 3, scope_guard normal, heavy_workflows_per_prompt 2
- **standard** - max_items 6, max_files 3, checkpoint_interval 2, scope_guard normal plus explicit file list, heavy_workflows_per_prompt 1
- **guarded** - max_items 4, max_files 2, checkpoint_interval 1, scope_guard strict, heavy_workflows_per_prompt 1

Parameter meaning:
- `max_items` - numbered instruction items per implementation prompt before items get dropped
- `max_files` - files one implementation prompt may change
- `checkpoint_interval` - implementation prompts between `/verify` + `/fix` checkpoints (PRMT-SQ-04)
- `scope_guard strict` - adds "Do ONLY the numbered items below. Do not refactor, rename, add tests, or touch files not listed. Report any item you could not complete as NOT DONE"
- `heavy_workflows_per_prompt` - heavy workflow invocations per prompt (PROMPTS_GUIDES Section 1f)

`max_items` takes precedence over the 5-8 instruction density heuristic in PROMPTS_GUIDES Section 5 [ASSUMED - IN07 Section 9].

### 7.4 Label and Profile Combined

Label and profile are set independently. Examples:

- `claude-opus-5` - `26-A`, `standard` (no behavior data) → few, broad prompts with checkpoints every 2
- `claude-haiku-4-5` - `25-C`, `standard` (no behavior data) → many small prompts, checkpoints every 2
- `glm-5.2` - `26-D` (R4 downgrade), `guarded` (documented observation) → many small prompts, 4 items each, checkpoint after every prompt, strict scope guard

R4 (Section 5) and the profile use the same evidence but answer different questions: skipped items lower the letter (less work completes per prompt) and move the profile toward `guarded` (prompt shape). Over-eagerness alone changes only the profile.

## 8. Producing MODEL_INVENTORY.md

`MODEL_INVENTORY.md` is a generated, human-readable view of the registries. Agents writing TASKS, STRUT, or prompts files read only this file; they never compute labels or profiles themselves.

```
  model-registry.json ─────────┐  context_window, max_output, effort levels,
  model-pricing.json ──────────┤  prices, capability_label, behavior_profile,
  model-parameter-mapping.json ┤  observed (ledger aggregate)
  windsurf-model-registry.json ┘  Devin cost, Devin-only models
              │
              v  update-model-registry.md step 9.4
  MODEL_INVENTORY.md ──> /write-tasks-plan, /write-strut, /write-prompts, /verify
              ^
              │  /session-finalize: ledger → registry.observed → profile_suggested
  _agent_work/partition-observations.jsonl  <── Final Checkpoint of every prompts file
```

### 8.1 Registry Properties

Per `model-registry.json` model entry (replaces IN07 `tier`, `tier_note`, `tier_suggested`):

- `capability_label` - `YY-L`, human-set by R1-R5
- `capability_note` - evidence for R4 downgrades or R5 caps; only when present
- `behavior_profile` - `precise` | `standard` | `guarded`, human-set by Section 7.2
- `observed` - script-written ledger aggregate: sums, `if`, `eg`, `sequences`, `self_audited_prompts`, `profile_suggested`

Devin-only models have no registry entry; their label and profile live in `MODEL_INVENTORY.md` Section 3.2 directly.

### 8.2 Inventory Structure

`MODEL_INVENTORY.md` holds data only (GRUC separation: data file, techniques in GUIDES, checks in RULES):
1. Definitions - HWH, WF, label, profile, context
2. Value Derivation - WF formula, R1-R5, profile thresholds, evidence priority, change rule, profile parameters (Section 7.3), effort multipliers, price
3. Model table - one row per model, columns below (3.1 API models, 3.2 Devin-only models)
4. Maintenance and Calibration - registry consistency, R4 and profile calibration, October review

Techniques and checks live in skill resource files:
- `PROMPTS_GUIDES.md` Section 1g - prompt partitioning (Section 9 formulas, checkpoints, scope guard, context fit)
- `TASKS_GUIDES.md` - HWH estimation, TASKS and STRUT step sizing, AWH estimation (Section 10)
- `PROMPTS_RULES.md` PRMT-SC-05 - verification of prompts files against the model data

### 8.3 Model Table Columns

- **Model** - registry `model_id` without date suffix; resolution by longest prefix
- **Label** - `capability_label`
- **Profile** - `behavior_profile`
- **Context** - `context_window / 1000` with `K` suffix
- **Low / Medium / High / XHigh / Max** - `WF_high * effort multiplier` for supported levels, `-` for unsupported. Thinking-budget models: Max = XHigh. Models without effort: Medium column only, value `WF_high * 0.5`
- **USD per WF 1** - API: `0.8 * input_per_1m + 0.2 * output_per_1m`; Devin-only: `cost_multiplier * 2.50 * 0.36`
- **Devin cost** - multiplier from `windsurf-model-registry.json`
- **Notes** - R4/R5 evidence, unsupported effort quirks, missing data

### 8.4 Regeneration Triggers

- **New model or price change** - `update-model-registry.md` step 9.4: add rows, recompute USD per WF 1
- **October to December** - promotion review: top models of the year from `YY-B` to `YY-A`
- **`profile_suggested` differs from `behavior_profile`** - human review during `update-model-registry.md`; on change update profile and Notes
- **Ledger IF < 0.75 with `sequences >= 3`** - R4 review of the label

## 9. Using the Inventory in Partitioned Documents

Lookup inputs: `intended_model`, `effort`, context window. Output: one row with label, profile, WF at the chosen effort, context, price.

### 9.1 Per Document Type

- **TASKS** - each task carries `Est: [N] HWH`. A task executed by one prompt must satisfy `Est <= WF(model, effort)`; larger tasks are split
- **STRUT** - step sizing by HWH instead of AWH minutes: a step executed by one prompt must satisfy `step HWH <= WF(model, effort)`. The current `edird-phase-planning` rule (">30min AWH" = decompose) is model-agnostic and does not use WF
- **Prompts files** - prompt count and shape from Section 9.2; frontmatter `intended_model`, `effort`, `context_window_size` from the row; opening commentary states label, profile, WF, task HWH, prompt count, cost

### 9.2 Partition Formulas

```
prompt_count = max( ceil(task_HWH / WF),
                    ceil(total_items / max_items),
                    ceil(total_files / max_files) )
checkpoints  = floor((prompt_count - 1) / checkpoint_interval) + Final Checkpoint
cost         = task_HWH * USD per WF 1
context fit  = input read per prompt <= 50% of Context  [ASSUMED - leaves room for output and thinking]
```

Evidence for the 50% context rule: the [RULER benchmark](https://github.com/nvidia/RULER) measured an effective context length (performance above a fixed threshold) of half or less of the claimed window for most tested models, for example GPT-4 128K claimed vs 64K effective [VERIFIED - LLMCAPCLS-IN01-SC-RULER]. RULER covers models up to 2025; current 1M-context models are not measured, so the 50% value stays [ASSUMED] for them.

If `prompt_count` exceeds the chain length limit (PRMT-SC-04), split into sub-chains.

### 9.3 Worked Example

Task: 3 HWH, 18 numbered items, 7 files, High effort.

- **`claude-opus-5`** (`26-A`, `standard`, WF 2.0): `max(ceil(3/2.0), ceil(18/6), ceil(7/3))` = `max(2, 3, 3)` = 3 prompts; checkpoint after prompt 2, then Final Checkpoint; cost 3 × 9.00 = $27
- **`glm-5.2`** (`26-D`, `guarded`, WF 0.25): `max(ceil(3/0.25), ceil(18/4), ceil(7/2))` = `max(12, 5, 4)` = 12 prompts; checkpoint after every prompt, strict scope guard, split into sub-chains; cost 3 × 2.00 = $6

Capacity drives GLM-5.2; instruction items drive Claude Opus 5. Neither dimension alone gives the right count.

## 10. Explaining and Converting HWH and AWH Estimates

Goal: a rough, explainable estimate (factor 2 accuracy), not a measurement. Even [METR](https://metr.org/time-horizons/)'s lab-measured time horizons carry error bars of about a factor of 2 in each direction [VERIFIED - LLMCAPCLS-IN01-SC-METR-LIMIT], so planning documents cannot expect better.

### 10.1 One Question per Unit

```
  HWH  "How big is the job?"          task size, model-independent      → TASKS Est, prompt count, cost
  WF   "How much fits in one prompt?" model + effort property            → prompts = ceil(HWH / WF)
  AWH  "How long will I wait?"        agent wall-clock, model-dependent  → STRUT phase budgets, scheduling
```

- **HWH (Human Work Hours)** - hours a skilled human expert needs without AI, including reading, editing, and verifying. Same unit METR and [Anthropic](https://www.anthropic.com/research/estimating-productivity-gains) use to size tasks: METR times human experts per task [VERIFIED - LLMCAPCLS-IN01-SC-METR-TH]; Anthropic estimates "hours a human professional would need to complete the task without AI assistance" [VERIFIED - LLMCAPCLS-IN01-SC-ANTH-PROD]
- **AWH (Agent Work Hours)** - wall-clock time the agent runs, excluding user wait. Depends on model, effort, and engine
- **WF** - links both: the HWH one prompt completes without skipping (Section 4)

### 10.2 Estimating HWH

Use size buckets instead of free numbers. Estimators distinguish "small vs large" reliably, not "1.5 vs 2 hours" [ASSUMED]:

- **0.25 HWH** - one file, one clear edit, known location
- **0.5 HWH** - one file with analysis, or 2-3 small edits
- **1 HWH** - one feature slice across 2-3 files including verification
- **2 HWH** - multi-file change with design decisions
- **4 HWH** - split before estimating further (larger tasks have lower agent success, see 10.4)

Who estimates: the planning agent may estimate HWH itself. Anthropic used Claude to estimate human task time for 100,000 conversations and reports the estimates as usable but imperfect and not validated across all tasks [VERIFIED - LLMCAPCLS-IN01-SC-ANTH-PROD]. Estimates by human developers are also unreliable: in [METR's randomized controlled trial](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) developers forecast a 24% AI speedup and observed a 19% slowdown [VERIFIED - LLMCAPCLS-IN01-SC-METR-RCT].

### 10.3 Converting HWH to AWH

Do not convert with a fixed ratio for planning; measure instead:

- **Default before data**: `AWH ≈ 0.2 * HWH` for well-specified, self-contained tasks. Basis: Anthropic's estimate that Claude reduces task time by about 80% (tasks of about 1.4 HWH on average) [VERIFIED - LLMCAPCLS-IN01-SC-ANTH-PROD]. Caveats: Claude estimated both times itself, and the "with AI" time is human-in-the-loop chat time, not unattended agent time. Applying it to autonomous agent runs is [ASSUMED]
- **With data**: `AWH = prompt_count * observed minutes per prompt` for the model and effort, from STRUT Time Log net working time (`edird-phase-planning`) [ASSUMED - method]
- **Not applicable**: tasks in large, familiar, messy codebases with heavy review. METR measured +19% (slower) for experienced developers with early-2025 AI tools, and -4% to -18% (faster) in early 2026 ([METR uplift update](https://metr.org/blog/2026-02-24-uplift-update/)) with wide confidence intervals; METR calls the 2026 data a weak signal due to selection effects [VERIFIED - LLMCAPCLS-IN01-SC-METR-RCT, LLMCAPCLS-IN01-SC-METR-UPLIFT]. Here AWH is dominated by review and correction, not by agent run time

Example: task 3 HWH, `claude-opus-5` High → 3 prompts (Section 9.3). Default AWH ≈ 0.6 h (36 min). After 3 sessions show 15 min per prompt: AWH ≈ 45 min.

### 10.4 Sanity Check: WF against METR Time Horizons

METR's time horizon is the HWH of tasks a model completes with a given success probability [VERIFIED - LLMCAPCLS-IN01-SC-METR-TH]. WF requires "without skipping", which corresponds to a high-reliability horizon:

- 80% horizons are about 5x shorter than 50% horizons [VERIFIED - LLMCAPCLS-IN01-SC-METR-PAPER]
- Claude Opus 4.5: 50% horizon about 4 h 49 min (95% confidence interval 1 h 49 min to 20 h 25 min, [METR limitations note](https://metr.org/notes/2026-01-22-time-horizon-limitations/)) [VERIFIED - LLMCAPCLS-IN01-SC-METR-LIMIT] → 80% horizon about 1 h (derived with the 5x rule, not measured)
- Proposed label `25-A` for `claude-opus-4-5` gives WF 1.0 HWH at High (current inventory: 0.5). Both lie within a factor of 2 of the derived 1 h, which is the precision METR itself states [ASSUMED - interpretation]

Cross-year rate check: METR measured a 50%-horizon doubling time ([paper](https://arxiv.org/abs/2503.14499), [Time Horizon 1.1](https://metr.org/blog/2026-01-29-time-horizon-1-1/), [blog](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/)) of about 7 months for 2019-2025 and about 89 days since 2024 (Time Horizon 1.1), and calls the trend "around 1-4 doublings per year" [VERIFIED - LLMCAPCLS-IN01-SC-METR-PAPER, LLMCAPCLS-IN01-SC-METR-TH11, LLMCAPCLS-IN01-SC-METR-BLOG]. The Section 4 rate of one doubling per year is at the conservative end. Conservative is acceptable: underestimated WF produces extra prompts (cost), overestimated WF produces skipped items (failure)

### 10.5 How to Explain It in One Paragraph

"HWH says how big a job is for a skilled human. Every model has a workload factor: how many of those hours fit into one prompt without the model dropping work. Divide HWH by the workload factor and you get the number of prompts. Cost is HWH times the price per workload factor. AWH, the time you wait, starts as one fifth of HWH and is replaced by measured minutes per prompt after a few sessions. All numbers are approximations within a factor of 2."

### 10.6 Exclusions

- **Story points, COCOMO (Constructive Cost Model), function points**: excluded - calibrated for human teams and projects, not single agent prompts; add estimation overhead without better accuracy at factor-2 precision
- **METR 50% horizon as WF directly**: excluded - 50% success means half the prompts fail; WF needs completion without skipping
- **Fixed HWH-to-AWH ratio as permanent rule**: excluded - engine, effort, and review load change the ratio; measured minutes per prompt replace it

## 11. Limitations

- **Cross-year rate is conservative, not measured for WF**: "one letter per year" (WF doubling per year) is below METR's 1-4 time-horizon doublings per year (Section 10.4). A different measured factor changes WF values, not labels
- **Letter assignment is judgment**: R2 places models in capability buckets without a measured metric until ledger data exists. Mitigation: document the reason per row in the Notes column; benchmarks (IN06 Section 3) as tie-breaker
- **Promotion requires a second review**: R3 requires one manual review per year between October and December
- **Observations depend on the execution framework**: framework explains 56% of over-eagerness variance, base model 21% ([SNARE study](https://arxiv.org/abs/2605.28122)). Ledger lines carry `engine`; profiles derived from `cascade` runs may not hold in `claude-code` or `lana` runs [VERIFIED - LLMCAPCLS-IN01-SC-IPPS-IN06 Section 3, LLMCAPCLS-IN01-SC-SNARE]
- **Self-audit bias**: if the Final Checkpoint runs on the audited model, `guarded` models under-report skips. `self_audited_prompts` in `observed` lets the reviewer discount them [ASSUMED - IN07 Section 9]
- **Profile parameter values are unmeasured**: max_items 8/6/4 and the other Section 7.3 values come from IN06 reasoning, not from runs
- **Missing registry entries**: GPT-6 Sol, Claude Opus 5.5, Gemini 4 Argon are released but not in `model-registry.json` 1.10.0 and have no label. Adding them requires a full `update-model-registry.md` run (pricing extraction and distribution to external configuration targets)
- **Registry max output values are request limits**: `model-registry.json` `max_output` (for example 8K for `claude-opus-4-5` and `claude-haiku-4-5`) does not reflect provider-documented limits; R5 reads provider values at label assignment and records the decision in `capability_note` (Section 5)

## 12. Sources

**Secondary Sources (release-date aggregators):**
- `LLMCAPCLS-IN01-SC-NAIM-TMLN`: https://www.nextaimodel.com/timeline - release dates per model line: OpenAI GPT, Gemini Pro, Claude Opus 2021-2026, including GPT-6 Sol 2026-09-22, Claude Opus 5.5 2026-09-22, Gemini 4 Argon 2026-10-13 (accessed 2026-10-28) [VERIFIED]
- `LLMCAPCLS-IN01-SC-ARIX-HOME`: https://aireleaseindex.com/ - release index 2017-2026, including o1 2024-09-12, Claude Fable 5 2026-06-09, GPT-5.6 Sol/Terra/Luna 2026-07-09, Gemini 3 Flash 2025-12-17 (accessed 2026-10-28) [VERIFIED]
- `LLMCAPCLS-IN01-SC-BTLN-TMLN`: https://botlineage.com/timeline - o1 GA 2024-12-05, Claude Opus 4 2025-05-22 (accessed 2026-10-28) [VERIFIED]

**Primary Sources (providers, research organizations, local files):**
- `LLMCAPCLS-IN01-SC-OAI-GPT5`: https://openai.com/index/introducing-gpt-5/ - GPT-5 announced 2025-08-07, GPT-5 mini as fallback model (accessed 2026-10-28) [VERIFIED]
- `LLMCAPCLS-IN01-SC-OAI-GPT52`: https://openai.com/index/introducing-gpt-5-2/ - GPT-5.2 announced 2025-12-11, available in API same day (accessed 2026-10-28) [VERIFIED]
- `LLMCAPCLS-IN01-SC-GOOG-GEM3`: https://blog.google/products-and-platforms/products/gemini/gemini-3/ - Gemini 3 Pro announced 2025-11-18 (accessed 2026-10-28) [VERIFIED]
- `LLMCAPCLS-IN01-SC-ANTH-HAIKU45`: https://www.anthropic.com/news/claude-haiku-4-5 - Claude Haiku 4.5 published 2025-10-15 (accessed 2026-10-28) [VERIFIED]
- `LLMCAPCLS-IN01-SC-ANTH-FABLE5`: https://www.anthropic.com/news/claude-fable-5-mythos-5 - Claude Fable 5 published 2026-06-09 (accessed 2026-10-28) [VERIFIED]
- `LLMCAPCLS-IN01-SC-ANTH-OPUS5`: https://www.anthropic.com/news/claude-opus-5 - Claude Opus 5 published 2026-07-24 (accessed 2026-10-28) [VERIFIED]
- `LLMCAPCLS-IN01-SC-ZAI-RELN`: https://docs.z.ai/release-notes/new-released - Z.AI release notes: GLM-5.3-Flash 2026-08-26, GLM-5.3 2026-08-18, GLM-5.2 2026-06-16; GLM-5.1 and GLM-5 listed earlier; Zhipu research page dates GLM-5.1 2026-04-07 and GLM-5 2026-02-11 (accessed 2026-10-28) [VERIFIED]
- `LLMCAPCLS-IN01-SC-KIMI-K3`: https://www.kimi.ai/blog/kimi-k3 - Kimi K3 introduced, 1M context, "still trails" Claude Fable 5 and GPT-5.6 Sol; launch 2026-07-16 per Bloomberg and AP coverage (accessed 2026-10-28) [VERIFIED]
- `LLMCAPCLS-IN01-SC-COG-SWE17`: https://www.linkedin.com/posts/jefflinwang_weve-released-swe-17-our-best-model-yet-activity-7480867805618438146-J56D - Cognition announcement of SWE-1.7 (reshared by Cognition executive), trained from Kimi K2.7, live in Devin; released 2026-07-08 (accessed 2026-10-28) [VERIFIED]
- `LLMCAPCLS-IN01-SC-GOOG-GEM37`: https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-3-7-flash/ - Gemini 3.7 Flash introduced 2026-08-13 (accessed 2026-10-28) [VERIFIED]
- `LLMCAPCLS-IN01-SC-GOOG-APICHG`: https://ai.google.dev/gemini-api/docs/changelog - 2026-10-08: `gemini-3.7-flash` routed to `gemini-3.8-flash`, `gemini-3.5-flash` routed to `gemini-3.6-flash` (accessed 2026-10-28) [VERIFIED]
- `LLMCAPCLS-IN01-SC-OAI-GPT53C`: https://openai.com/index/introducing-gpt-5-3-codex/ - GPT-5.3-Codex introduced 2026-02-05 (accessed 2026-10-28) [VERIFIED]
- `LLMCAPCLS-IN01-SC-RULER`: https://arxiv.org/abs/2404.06654 - RULER: effective context length below claimed length for most tested models, for example GPT-4 128K claimed vs 64K effective; results table also in https://github.com/nvidia/RULER (accessed 2026-10-28) [VERIFIED]
- `LLMCAPCLS-IN01-SC-METR-BLOG`: https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/ - near 100% success on tasks under 4 human minutes, under 10% above about 4 hours; trend "around 1-4 doublings per year" (accessed 2026-10-28) [VERIFIED]
- `LLMCAPCLS-IN01-SC-SNARE`: https://arxiv.org/abs/2605.28122 - SNARE: agent framework explains 56% of over-eagerness variance, base model 21% (accessed 2026-10-19 via IN06) [VERIFIED]
- `LLMCAPCLS-IN01-SC-BGAP-IFEVAL`: https://benchgap.net/b/ifeval/current - IFEval estimates: GLM-5.2 93.2%, GPT-5.4 93.5% (accessed 2026-10-19 via IN06) [VERIFIED]
- `LLMCAPCLS-IN01-SC-METR-TH`: https://metr.org/time-horizons/ - time horizon = human-expert task duration at which the model succeeds with 50% / 80% probability; human durations from timed expert runs (accessed 2026-10-28) [VERIFIED]
- `LLMCAPCLS-IN01-SC-METR-PAPER`: https://arxiv.org/abs/2503.14499 - 50% horizon doubling about every 7 months 2019-2025; 80% horizons about 5x shorter; near 100% success under 4 human minutes, under 10% above 4 hours (accessed 2026-10-28) [VERIFIED]
- `LLMCAPCLS-IN01-SC-METR-TH11`: https://metr.org/blog/2026-01-29-time-horizon-1-1/ - doubling time 88.6 days for models since 2024 (accessed 2026-10-28) [VERIFIED]
- `LLMCAPCLS-IN01-SC-METR-LIMIT`: https://metr.org/notes/2026-01-22-time-horizon-limitations/ - error bars about factor 2; Claude Opus 4.5 50% horizon 4 h 49 min (CI 1 h 49 min to 20 h 25 min); AIs are usually much faster than humans when they solve tasks (accessed 2026-10-28) [VERIFIED]
- `LLMCAPCLS-IN01-SC-METR-RCT`: https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/ - experienced developers 19% slower with early-2025 AI tools; forecast 24% faster (accessed 2026-10-28) [VERIFIED]
- `LLMCAPCLS-IN01-SC-METR-UPLIFT`: https://metr.org/blog/2026-02-24-uplift-update/ - early-2026 estimates -18% and -4% task time with wide confidence intervals, selection bias (accessed 2026-10-28) [VERIFIED]
- `LLMCAPCLS-IN01-SC-ANTH-PROD`: https://www.anthropic.com/research/estimating-productivity-gains - 100,000 Claude.ai conversations; tasks about 1.4 h without AI; Claude estimates about 80% time reduction; Claude time estimates imperfect but usable (accessed 2026-10-28) [VERIFIED]
- `LLMCAPCLS-IN01-SC-ANTH-MODELS`: https://docs.anthropic.com/en/docs/about-claude/models/whats-new-claude-4-5 - models overview: Claude Haiku 4.5 max output 64K, Claude Fable 5 / Opus 5 / Sonnet 5 max output 128K (accessed 2026-10-28) [VERIFIED]
- `LLMCAPCLS-IN01-SC-ANTH-OPUS45`: https://www.anthropic.com/news/claude-opus-4-5 - Claude Opus 4.5 published 2025-11-24; evaluations run with 64K thinking budget, 200K context (accessed 2026-10-28) [VERIFIED]
- `LLMCAPCLS-IN01-SC-IPPS-MINV`: `PromptSystemV4.5/skills/write-documents/MODEL_INVENTORY.md` - former Class A-D definitions and WF values (kept in `MODEL_INVENTORY_v0.md`); current version with labels, profiles, partition formulas [VERIFIED]
- `LLMCAPCLS-IN01-SC-IPPS-MREG`: `PromptSystemV4.5/skills/llm-evaluation/model-registry.json` 1.10.0 - dated Anthropic model IDs, max output request limit per prefix, `capability_label` and `behavior_profile` per model [VERIFIED]
- `LLMCAPCLS-IN01-SC-IPPS-IN06`: `T01_MDLBHVPRM_BehavioralParameterBenchmarks_2026-10-19/_INFO_MDLBHVPRM-06_ModelAwarePartitioning.md` - behavior axes, partition parameters, IFEval mismatch for GLM-5.2, decision MDLBHVPRM-DD-01 [VERIFIED]
- `LLMCAPCLS-IN01-SC-IPPS-IN07`: `T01_MDLBHVPRM_BehavioralParameterBenchmarks_2026-10-19/_INFO_MDLBHVPRM-07_PromptFeedbackLoop.md` - observation ledger, IF/EG formulas, suggestion thresholds, registry properties, open points [VERIFIED]

## 13. Document History

**[2026-10-28 20:10]**
- Changed: Section 8.2 - `MODEL_INVENTORY.md` holds data only; prompt partitioning moved to `PROMPTS_GUIDES.md` Section 1g, HWH/AWH estimation and task sizing to new `TASKS_GUIDES.md`, verification checks to `PROMPTS_RULES.md` PRMT-SC-05 (GRUC separation)

**[2026-10-28 19:50]**
- Changed: Section 6 labels applied in `MODEL_INVENTORY.md` and `model-registry.json` 1.10.0; all release dates verified (GLM-5.x, Kimi K3, SWE-1.7, Gemini 3.7 Flash, GPT-5.3-Codex); Gemini API routing of 3.5 and 3.7 Flash noted
- Added: RULER evidence for the 50% context rule (Section 9.2)
- Removed: release-date limitation (resolved)
- Changed: missing-registry-entries limitation states the required `update-model-registry.md` run; max-output limitation states how R5 handles it
- Added: 7 sources (Z.AI release notes, Kimi K3, Cognition SWE-1.7, Gemini 3.7 Flash, Gemini API changelog, GPT-5.3-Codex, RULER)

**[2026-10-28 19:20]**
- Fixed: acronyms written out at first use (WF, IF, EG, HWH, AWH, METR, RCT, COCOMO, confidence interval)
- Added: inline source links at first mention in Summary and Sections 5, 6, 7, 10, 11 (INFO-SC-05)
- Changed: figurative wording made explicit ("fence scope", "second touch", "ceremony"); "flagship releases" to "major releases" where the list includes non-flagship models

**[2026-10-28 19:10]**
- Fixed: `claude-haiku-4-5` release date 2025-10-01 (model ID date) to 2025-10-15 (announcement)
- Fixed: IFEval comparison "equal to GPT-5.4" to "within 0.3 points (93.5%)"
- Fixed: "1-4 doublings per year" attributed to METR blog, not paper; `gpt-5.2` max output marked as registry request limit
- Added: 9 primary sources (OpenAI GPT-5, GPT-5.2; Google Gemini 3; Anthropic Haiku 4.5, Fable 5, Opus 5; METR blog; SNARE; benchgap IFEval)
- Added: METR 2026 data qualified as weak signal; "strongest model" findings marked as judgment
- Removed: Next Steps section and action wording in Limitations (formerly Weak Points and Open Questions), D-02 reference, "replaces" wording for STRUT rule, "open point" wording
- Changed: Sources split into primary and secondary; timing Summary cites provider announcements; local inventory and registry source IDs cited

**[2026-10-28 18:55]**
- Fixed: R5 used registry request limits as model max output; now provider-documented values. `claude-opus-4-5` moves to `25-A` (WF 1.0), `claude-sonnet-4-5` stays `25-B` without R5
- Changed: R2 defines the letter as capability bucket; rank descriptions are heuristics
- Changed: October promotion stated as the only upward change, conservative before promotion (Sections 4, Summary)
- Changed: "36 of 37" claim reworded to 35 of 37 and marked as compatibility, not validation
- Added: profile change rule (one step, 3 sequences) against oscillation from load-dependent IF (Section 7.2)
- Added: caveats on Anthropic AWH basis (self-estimated, human-in-the-loop) and derived METR 80% horizon
- Added: Next Steps 6-7, 2 Anthropic sources

**[2026-10-28 18:40]**
- Added: Section 10 explaining and converting HWH and AWH (unit questions, HWH buckets, AWH default and measurement, METR sanity check, one-paragraph explanation, exclusions)
- Added: 7 sources (METR time horizons, paper, TH 1.1, limitations, RCT, uplift update; Anthropic productivity estimates)
- Changed: Summary, TOC, cross-year weak point; Sections 11-14 renumbered

**[2026-10-28 18:25]**
- Added: Section 7 behavior profile (axes, thresholds, evidence priority, partition parameters, label-profile combination) from IN06/IN07
- Added: Section 8 producing `MODEL_INVENTORY.md` (data flow, registry properties, structure, columns, regeneration triggers)
- Added: Section 9 usage in TASKS, STRUT, prompts files with partition formulas and worked example
- Changed: IN06 TIER-A/B/C replaced by profile names to avoid collision with `YY-L` letters; IN07 `tier` properties replaced by `capability_label` and `behavior_profile`
- Fixed: unsupported "every 6 months" claim, missing source label on 2024 dates, "flagship" used for both A and B
- Changed: Weak points, Next Steps, Summary, Sources, TOC, Target file aligned with new sections

**[2026-10-28 18:05]**
- Initial research document created: year-letter labels `YY-L`, October promotion rule, WF formula, mapping of 37 inventory rows
