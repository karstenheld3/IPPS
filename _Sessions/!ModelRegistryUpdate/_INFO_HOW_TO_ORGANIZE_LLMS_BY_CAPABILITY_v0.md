# INFO: How to Organize LLMs by Capability

**Doc ID**: LLMCAPCLS-IN01
**Goal**: Define time-stable model capability labels, a behavior profile per model, and how `MODEL_INVENTORY.md` is produced from them and used to partition TASKS, STRUT, and prompts files by model, effort, and context window
**Timeline**: Created 2026-10-28, Updated 9 times (2026-10-28 - 2026-10-29)
**Target file**: `PromptSystemV4.5/skills/write-documents/MODEL_INVENTORY.md`, `PromptSystemV4.5/skills/llm-evaluation/model-registry.json`, `update-model-registry.md`

**Depends on:**
- `_INFO_MDLBHVPRM-06_ModelAwarePartitioning.md [MDLRGUP-MDLBHVPRM-IN06]` for capacity, instruction following, and eagerness axes and decision MDLBHVPRM-DD-01 (observation overrides benchmarks)
- `_INFO_MDLBHVPRM-07_PromptFeedbackLoop.md [MDLRGUP-MDLBHVPRM-IN07]` for the checkpoint ledger that calibrates WF

## Summary

- **Generation-relative classes go stale**: the former `MODEL_INVENTORY.md` Class A-D was defined as "frontier" / "previous frontier generation", so every release cycle forced a re-grade of the whole table [VERIFIED - LLMCAPCLS-IN01-SC-IPPS-MINV]
- **Applied on 2026-10-29**: `MODEL_INVENTORY.md` lists 92 API models (every text model except `retired`) plus 4 Devin-only models with Label, Comp, Profile, Efforts, WF, prices; `model-registry.json` 1.11.0 carries `release_date`, frozen `eci_band`, script-derived `capability_label`; `update-model-inventory.py` regenerates the tables [VERIFIED - LLMCAPCLS-IN01-SC-IPPS-MINV, LLMCAPCLS-IN01-SC-IPPS-MREG]
- **The letter is the Epoch ECI band relative to a year anchor**: `letter_index = (anchor(YY) - eci_band) / 5`, letters `A`-`Z`, one letter per 5 ECI points. Measured, not judged; vendor tiers no longer decide the letter. 2026 spreads over `A`-`F` (was `B`-`E`) [VERIFIED - band source; anchor ASSUMED]
- **Year anchors rise 15 ECI per year**: top bands 2024 `E140` (o1), 2025 `E155` (gpt-5.2), 2026 `E170` (gpt-6.1-sol, gpt-6-astra, claude-opus-5-5) → `anchor(YY) = 170 + 15 * (YY - 26)` [VERIFIED for 2024-2026 - LLMCAPCLS-IN01-SC-IPPS-MREG; constant for later years ASSUMED]
- **Label is permanent, Comp compares across years**: Label uses the release year; Comp uses the comparison year (`year(today)` from May 1, else the previous year) and shifts three letters at each May 1 wrap. Same band = same Comp, so `gpt-5.2` (`25-A`) and `gpt-5.4` (`26-D`) both show Comp `26-D` [ASSUMED - rule design]
- **WF comes from the band, not the letter**: `WF_high = 2.0 * 2^(-(170 - eci_band) / 10)` halves every two letters (1.5 doublings per year, inside METR's 1-4). WF does not move at the wrap [ASSUMED - anchor and slope]
- **In-house measurement cross-check**: LLM-Research `TBLF-IN02` CSV extraction limits show effort and thinking method dominate (`claude-opus-4-6` 6 rows at Medium, 667 at High) and do not order models within E145-E160; used as Notes marker and Medium warning for adaptive-thinking models, not as letter source [VERIFIED - LLMCAPCLS-IN01-SC-TBLF-IN02]
- **Two independent dimensions per model**: capability label (how much work per prompt, WF) and behavior profile `precise` / `standard` / `guarded` (prompt shape: max_items, max_files, checkpoint_interval, scope_guard). Profile comes from ledger instruction following (IF) and eagerness (EG), then documented observations, then benchmarks; no data = `standard` [VERIFIED - LLMCAPCLS-IN01-SC-IPPS-IN06, LLMCAPCLS-IN01-SC-IPPS-IN07]
- **Prompt count = maximum of three limits**: `ceil(task_HWH / WF)`, `ceil(items / max_items)`, `ceil(files / max_files)`. For a task of 3 Human Work Hours (HWH) Claude Opus 5 is limited by items (3 prompts), GLM-5.2 by capacity (6 prompts) [ASSUMED - Section 9.3]
- **MODEL_INVENTORY.md is generated from the registries**: registry holds `release_date`, `eci_band`, `capability_label`, `behavior_profile`, `observed`; `update-model-inventory.py` adds Comp, Efforts, WF, and price; agents read only the inventory [VERIFIED - script in session `!ModelRegistryUpdate`]
- **HWH, WF, AWH answer three questions**: HWH = how big is the job (human expert hours, model-independent, same unit as [METR](https://metr.org/) (Model Evaluation and Threat Research) and [Anthropic](https://www.anthropic.com/research/estimating-productivity-gains)); WF = how much fits in one prompt; Agent Work Hours (AWH) = how long the agent runs. Estimate HWH in buckets 0.25 / 0.5 / 1 / 2 HWH, split at 4 [VERIFIED - unit definition; buckets ASSUMED]
- **AWH starts at 0.2 × HWH, then gets measured**: default from Anthropic's estimated 80% task-time reduction; replaced by observed minutes per prompt from STRUT Time Logs. Not valid for large familiar codebases, where METR's randomized controlled trial (RCT) measured AI-assisted work as up to 19% slower [VERIFIED - LLMCAPCLS-IN01-SC-ANTH-PROD, LLMCAPCLS-IN01-SC-METR-RCT; default ratio ASSUMED]
- **WF values are plausible against METR**: Claude Opus 4.5 80%-reliability horizon about 1 h (derived from the 50% horizon) vs WF 0.5 HWH for its band `E150`; both within METR's factor-2 error bars, and METR's 1-4 doublings per year make the 1.5-doublings slope conservative [VERIFIED - LLMCAPCLS-IN01-SC-METR-LIMIT, LLMCAPCLS-IN01-SC-METR-BLOG]

## Table of Contents

1. [Problem with Generation-Relative Classes](#1-problem-with-generation-relative-classes)
2. [Year-Letter Label Format](#2-year-letter-label-format)
3. [Year Anchor, Comparison Year, and the May 1 Wrap](#3-year-anchor-comparison-year-and-the-may-1-wrap)
4. [Workload Factor Formula](#4-workload-factor-formula)
5. [Assignment Rules](#5-assignment-rules)
6. [Labels for the Current Inventory](#6-labels-for-the-current-inventory)
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

- `YY` - two-digit release year (general availability via API or product; `release_date` in `model-registry.json`)
- `-` - separator (readability; `26-C` instead of `26C`)
- `L` - letter `A`..`Z` for the model's Epoch ECI band relative to the year anchor (Section 3): `letter_index = (anchor(YY) - eci_band) / 5`. One letter = one 5-point ECI band. No floor; an index below 0 clamps to `A`

The letter is measured, not judged: the ECI band comes from `https://epoch.ai/eci` (score rounded to the nearest 5) and is frozen at first assignment. Vendor tier words (Apex, Flagship, Balanced, Efficient) are not part of the definition; they remain in `uc_class` for the ECI-pending fallback (Section 5).

Two labels per model:

- **Label** - `YY` = release year. Permanent (R1, R2)
- **Comp** - `YY` = comparison year (Section 3.2). Same band = same Comp regardless of release year. Regenerated at every inventory update

```
  Band:        E170  E165  E160  E155  E150  E145  E140  E135  E130  E125  E120
  Label 2024:  -     -     -     -     -     -     A     B     C     D     E
  Label 2025:  -     -     -     A     B     C     D     E     F     G     H
  Label 2026:  A     B     C     D     E     F     G     H     I     J     K
  Comp 26:     A     B     C     D     E     F     G     H     I     J     K
  WF_high:     2.0   1.5   1.0   0.75  0.5   0.38  0.25  0.19  0.13  0.09  0.06
```

Examples (registry 1.11.0):

- `gpt-5.2` - ECI 153.66, `E155`, released 2025-12-11 → Label `25-A`, Comp `26-D`
- `gpt-5.4` - ECI 157.31, `E155`, released 2026-03-05 → Label `26-D`, Comp `26-D` (same band as `gpt-5.2`, same Comp)
- `gpt-5-nano` - ECI 139.21, `E140`, released 2025-08-07 → Label `25-D`, Comp `26-G`
- `gpt-4o` - ECI 128.99, `E130`, released 2024-05-13 → Label `24-C`, Comp `26-I`
- `o1` - ECI 141.72, `E140`, released 2024-12-05 → Label `24-A`, Comp `26-G`

## 3. Year Anchor, Comparison Year, and the May 1 Wrap

### 3.1 Evidence

Major releases per year, from [Next AI Model timeline](https://www.nextaimodel.com/timeline) and [AI Release Index](https://aireleaseindex.com/), key dates confirmed by provider announcements ([OpenAI GPT-5](https://openai.com/index/introducing-gpt-5/), [OpenAI GPT-5.2](https://openai.com/index/introducing-gpt-5-2/), [Google Gemini 3](https://blog.google/products-and-platforms/products/gemini/gemini-3/), [Anthropic models](https://www.anthropic.com/news/models)):

- **2024**: Claude 3 Opus 2024-03-04, GPT-4o 2024-05-13, Claude 3.5 Sonnet 2024-06-20, o1 2024-09-12 (preview) / 2024-12-05, Claude 3.5 Sonnet (new) 2024-10-22 [VERIFIED - LLMCAPCLS-IN01-SC-ARIX-HOME, LLMCAPCLS-IN01-SC-BTLN-TMLN, registry ID `claude-3-5-sonnet-20241022`]
- **2025**: Gemini 2.5 Pro 2025-03-25, o3 2025-04-16, Claude Opus 4 2025-05-22, GPT-5 2025-08-07, Claude Sonnet 4.5 2025-09-29, Claude Haiku 4.5 2025-10-15, GPT-5.1 2025-11-12, Gemini 3 Pro 2025-11-18, Claude Opus 4.5 2025-11-24, GPT-5.2 2025-12-11 [VERIFIED - LLMCAPCLS-IN01-SC-NAIM-TMLN; primary: LLMCAPCLS-IN01-SC-OAI-GPT5, LLMCAPCLS-IN01-SC-ANTH-HAIKU45, LLMCAPCLS-IN01-SC-GOOG-GEM3, LLMCAPCLS-IN01-SC-ANTH-OPUS45, LLMCAPCLS-IN01-SC-OAI-GPT52]
- **2026**: Claude Opus 4.6 2026-02-05, GPT-5.4 2026-03-05, GPT-5.5 2026-04-23, Claude Opus 4.8 2026-05-28, Claude Fable 5 2026-06-09, GPT-5.6 Sol 2026-07-09, Claude Opus 5 2026-07-24, GPT-6 Astra 2026-09-04, GPT-6 Sol 2026-09-22, Claude Opus 5.5 2026-09-22, Gemini 4 Argon 2026-10-13 [VERIFIED - LLMCAPCLS-IN01-SC-NAIM-TMLN; primary for Claude Fable 5 and Claude Opus 5: LLMCAPCLS-IN01-SC-ANTH-FABLE5, LLMCAPCLS-IN01-SC-ANTH-OPUS5]

Top Epoch ECI band per release year (snapshot 2026-10-28, `model-registry.json` 1.11.0) [VERIFIED - LLMCAPCLS-IN01-SC-IPPS-MREG]:

- **2024**: `E140` - o1 141.72
- **2025**: `E155` - gpt-5.2 153.66 (next: gpt-5.2-pro 156.33, also `E155`)
- **2026**: `E170` - claude-opus-5-5 168.83, gpt-6-astra 168.81, gpt-6.1-sol 168.37

The top band rose by exactly 15 ECI points per year for three consecutive years. Release month no longer matters: the strongest 2026 models shipped June to October, the strongest 2024 and 2025 models September to December, and the band-based letter is the same either way.

### 3.2 Rule Design

- **Anchor**: `anchor(YY) = 170 + 15 * (YY - 26)` → 2024 `E140`, 2025 `E155`, 2026 `E170`, 2027 `E185`. The +15 slope is [ASSUMED] for future years (3 data points). Anchors of past years never change; the anchor of a new year is appended when its first model is registered
- **Comparison year**: `year(today)` if today is on or after May 1, else `year(today) - 1`. On 2026-10-29 the comparison year is `26`; it becomes `27` on 2027-05-01
- **Comp** = letter for the model's band against `anchor(comparison year)`. Every Comp shifts by three letters at each wrap (15 ECI = 3 bands); Labels do not move
- **Why May 1**: by May the new year has shipped enough models to make the new anchor meaningful, and the previous year's top band can be recorded here as the measured check of the +15 slope
- **What replaced the October rule**: no letter is reserved for late releases. A model released in January 2027 with `E185` gets `27-A` on day one; if 2027 never reaches `E185`, `27-A` stays empty. Labels of a year never need a promotion review

```
  Label  = letter(anchor(release year)    - band)   permanent, cite in prompts files
  Comp   = letter(anchor(comparison year) - band)   regenerated, use to choose a model
  Wrap   = May 1: comparison year + 1, anchor + 15, every Comp + 3 letters
```

## 4. Workload Factor Formula

WF definition (from `MODEL_INVENTORY.md` Section 1): HWH (Human Work Hours) one prompt can complete in one run at High effort without skipping items or truncating.

Formula at High effort, from the ECI band (not from the letter, so WF does not move at the wrap):

```
WF_high = 2.0 * 2^(-(170 - eci_band) / 10)
E170 2.0 | E165 1.5 | E160 1.0 | E155 0.75 | E150 0.5 | E145 0.38 | E140 0.25 | E135 0.19 | E130 0.13 | E125 0.09 | E120 0.06
```

- Anchor: `E170` = 2.0 HWH (the value the former Class A carried) [ASSUMED]
- Slope: WF halves every 10 ECI points = every two letters = 1.5 doublings per year at the +15 anchor rate. METR measured 1-4 time-horizon doublings per year (Section 10.4), so the slope is at the conservative end [ASSUMED - slope]
- Effort multipliers relative to High: Low 0.25, Medium 0.5, High 1.0, XHigh 1.5, Max 2.0 [ASSUMED]. `MODEL_INVENTORY.md` shows one `WF` column (High) and an `Efforts` column with the supported levels; models with a single mode (`M` or `-`) show `WF_high * 0.5`
- Medium on adaptive-thinking Claude models: `TBLF-IN02` measured `claude-opus-4-6` 6 rows and `claude-opus-4-7` 12 rows at Medium against 667 and 843+ at High on CSV extraction; `TBLF-IN03` E1 traces it to adaptive thinking skipping the reasoning phase. The Notes column warns for every `adaptive_thinking` prefix; for structured-data work plan Low or High [VERIFIED for 4.6/4.7 - LLMCAPCLS-IN01-SC-TBLF-IN02; inheritance by other adaptive models ASSUMED]
- Nothing is re-graded when new models arrive: band, Label, and WF of existing rows stay; only Comp moves at the wrap

## 5. Assignment Rules

- **R1 - Year**: `YY` = year of general availability (`release_date`). Never changes
- **R2 - Band freeze**: the ECI band is read once from the Epoch snapshot at registration and never re-read; `match-epoch-eci.py` reports `band_action: keep` for such models. Newer models or Epoch re-estimates do not move existing labels
- **R3 - ECI pending fallback**: a model without an Epoch score (fewer than 4 benchmarks) takes the band of its nearest same-tier sibling (`glm-5.3-flashx` ← `glm-5.3-flash`, `claude-mythos-5` ← `claude-fable-5`) or, without a sibling, the UC default `anchor(YY) - 5 / 10 / 15 / 20 / 25` for `UC-1..5` (2026 medians of the measured UC tiers). `eci_band_source` marks the fallback; the band is replaced once Epoch publishes a score (`band_action: replace_fallback`). This is the only label change besides R4
- **R4 - Observation downgrade**: a documented observation (FAILS.md entry or findings-card ledger entry naming model and skipped items) lowers the letter by one step within the same year. `capability_note` and the Notes column record the evidence. Labels never move up by observation (MDLBHVPRM-DD-01: observation overrides benchmark only toward stricter). Over-eagerness alone changes the behavior profile, not the letter (`glm-5.2`)
- **Removed**: the former R2 (UC tier → letter), R3 (October cap), and R5 (max-output cap) are obsolete. Max output stays a Notes item (`claude-opus-4-5`: registry 8K is a request limit, provider documents 64K) [VERIFIED - LLMCAPCLS-IN01-SC-ANTH-MODELS]

## 6. Labels for the Current Inventory

Applied in `model-registry.json` 1.11.0 and `MODEL_INVENTORY.md` on 2026-10-29 (`update-model-inventory.py`): 92 API rows (every text model except `status: retired`) plus 4 Devin-only rows, grouped by Comp 26. Release dates from Section 3.1 sources, provider release notes, and model ID date suffixes; 29 rows carry `release_date_assumed` where only the family-head or an unverified announcement date is known (re-checked in the next FULL template run). "Was" = label under the former UC-tier rule (registry 1.10.2).

- **Comp A, E170, WF 2.0** (3): `claude-opus-5-5` (was 26-C), `gpt-6-astra` (was 26-B), `gpt-6.1-sol` (was 26-C)
- **Comp B, E165, WF 1.5** (12): `claude-fable-5`, `claude-fable-5-1` (unchanged 26-B), `claude-opus-5`, `gpt-6-sol`, `gpt-5.6-sol`, `gemini-4-argon` (were 26-C), `claude-sonnet-5-5` (was 26-D), `gpt-5.5-pro`, `gpt-5.5-cyber`, `gpt-5.6-cyber`, `claude-mythos-5`, `claude-mythos-5-1` (new)
- **Comp C, E160, WF 1.0** (5 + 2 Devin): `gpt-5.5`, `claude-opus-4-8` (were 26-C), `gpt-5.6-terra` (was 26-D), `claude-haiku-5-5` (was 26-E), `gpt-5.4-pro` (new); `Kimi K3`, `Gemini 3.7 Flash`
- **Comp D, E155, WF 0.75** (22 + 2 Devin): `gpt-5.4`, `claude-opus-4-6`, `claude-opus-4-7`, `gemini-3.1-pro-preview`, `glm-5.3`, `grok-4.5`, `grok-4.6`, `grok-4.7`, `gpt-5.3-codex` (were 26-C), `claude-sonnet-4-6`, `claude-sonnet-5`, `gemini-3.6-flash`, `gemini-3.8-flash`, `glm-5.3-flash`, `glm-5.3-flashx`, `glm-5.3-flashx-legal`, `gpt-6.1-terra`, `grok-build-0.1` (unchanged 26-D), `gpt-5.6-luna`, `gpt-6-luna` (were 26-E), `gpt-5.2` (25-A, unchanged letter), `gpt-5.2-pro` (new 25-A); `Gemini 3.5 Flash`, `SWE-1.7`
- **Comp E, E150, WF 0.5** (14): `glm-5.2` (was 26-C, profile `guarded` unchanged), `glm-5.1` (was 26-C), `gpt-5.4-mini`, `grok-4.3`, `grok-4.20-*` (were 26-D), `glm-4.7-flash`, `glm-4.7-flashx` (new 26-E), `claude-opus-4-5` (25-A to 25-B), `gpt-5`, `gpt-5.1` (unchanged 25-B), `gemini-3-flash-preview` (25-C to 25-B), `gpt-5-pro` (new 25-B)
- **Comp F, E145, WF 0.38** (17): `glm-5` (was 26-C), `gemini-3.1-flash-lite`, `gemini-3.5-flash-lite` (were 26-E), `gpt-5.4-nano` (new 26-F), `claude-sonnet-4-5`, `gpt-5-mini`, `gemini-2.5-flash` (unchanged 25-C), `o3`, `gemini-2.5-pro` (25-B to 25-C), `o3-pro`, `o4-mini`, `o3-deep-research`, `o4-mini-deep-research`, `glm-4.5`, `glm-4.5-x`, `glm-4.6`, `glm-4.7` (new 25-C)
- **Comp G, E140, WF 0.25** (8): `claude-haiku-4-5` (unchanged 25-D), `gpt-5-nano`, `o3-mini`, `o1-pro`, `glm-4.5-airx`, `glm-4.5v`, `glm-4.6v` (new 25-D), `o1` (new 24-A)
- **Comp H, E135, WF 0.19** (6): `gpt-4.1` (25-B to 25-E), `gemini-2.5-flash-lite` (25-D to 25-E), `gpt-4.1-mini`, `glm-4.5-flash` (new 25-E), `claude-3-5-sonnet`, `o1-mini` (new 24-B)
- **Comp I-K, E130-E120, WF 0.13-0.03** (5): `gpt-4.1-nano` (25-F), `gpt-4o`, `gpt-4o-2024-05-13` (24-C), `gpt-4o-mini` (24-D), `glm-4-air` (24-E)

Largest moves: `gpt-4.1` down three letters (E135 was hidden in `25-B` by its flagship tier), `claude-haiku-5-5` up two (E160 sits with `gpt-5.5`), `glm-5.2` and `glm-5.1` down two (E150 next to `gpt-5`). 2026 now spreads over six letters (A-F) instead of four (B-E).

### 6.1 Cross-Check against Measured CSV Extraction (TBLF-IN02)

LLM-Research measured confirmed reliable row counts for 7-column CSV extraction per model and effort (binary search, n=3, about 28% variance between runs, May 2026) [VERIFIED - LLMCAPCLS-IN01-SC-TBLF-IN02]. The `CSV rows` Notes marker in `MODEL_INVENTORY.md` carries these values.

- **Effort and thinking method dominate**: `gpt-5-mini` L65 / M500 / H675+; `claude-opus-4-6` M6 / H667; `claude-opus-4-7` M12 / H843+; `gpt-5` L356 / M450 / H492. A one-step effort change moves the result more than two ECI bands do
- **Within E145-E160 the test does not order models**: `gpt-5-mini` (E145) M500, `gpt-5.4` (E155) M492, `gpt-5` (E150) H492, `claude-opus-4-8` (E160) H492, `gpt-5.5` (E160) M437, `gpt-5.2` (E155) M215. The test measures attention over structured data, not general capability, so it is not used as the letter source
- **Temperature models fall off**: `gpt-4o` 4, `gpt-4o-mini` 6, `claude-haiku-4-5` 9 (run without thinking). The low tail (Comp I-K, WF 0.13 and below) is real, not an artifact of the formula
- **Use in the inventory**: Notes marker per tested configuration, Medium warning for `adaptive_thinking` prefixes (Section 4), no letter changes (a single-task result with 28% variance is below the R4 evidence bar of skipped items in agentic work)

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

- `claude-opus-5` - `26-B` (E165, WF 1.5), `standard` (no behavior data) → few, broad prompts with checkpoints every 2
- `claude-haiku-4-5` - `25-D` (E140, WF 0.25), `standard` (no behavior data) → many small prompts, checkpoints every 2
- `glm-5.2` - `26-E` (E150, WF 0.5), `guarded` (documented over-eagerness) → 4 items per prompt, checkpoint after every prompt, strict scope guard

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

- `release_date` - provider announcement date; `release_date_assumed: true` when only the family-head date is verified
- `eci_band`, `eci_score` - Epoch band frozen at first assignment (R2); `eci_band_source` marks a fallback band (R3)
- `capability_label` - `YY-L`, script-derived from `release_date` and `eci_band`; `update-model-inventory.py` refuses a mismatch
- `capability_note` - evidence for R4 downgrades; only when present
- `behavior_profile` - `precise` | `standard` | `guarded`, human-set by Section 7.2
- `observed` - script-written ledger aggregate: sums, `if`, `eg`, `sequences`, `self_audited_prompts`, `profile_suggested`

Devin-only models have no registry entry; their label and profile live in `MODEL_INVENTORY.md` Section 3.2 directly.

### 8.2 Inventory Structure

`MODEL_INVENTORY.md` holds data only (GRUC separation: data file, techniques in GUIDES, checks in RULES):
1. Definitions - HWH, WF, label, profile, context
2. Value Derivation - year anchor, Label and Comp derivation, R1-R4, WF formula, profile thresholds, evidence priority, change rule, profile parameters (Section 7.3), effort multipliers, price
3. Model table - one row per model, columns below (3.1 API models, 3.2 Devin-only models), sorted by Comp
4. Maintenance and Calibration - script regeneration, May 1 wrap, R4 and profile calibration

Techniques and checks live in skill resource files:
- `PROMPTS_GUIDES.md` Section 1g - prompt partitioning (Section 9 formulas, checkpoints, scope guard, context fit)
- `TASKS_GUIDES.md` - HWH estimation, TASKS and STRUT step sizing, AWH estimation (Section 10)
- `PROMPTS_RULES.md` PRMT-SC-05 - verification of prompts files against the model data

### 8.3 Model Table Columns

- **Model** - registry `model_id` without date suffix; resolution by longest prefix
- **Label** - `capability_label` (release year + band letter)
- **Comp YY** - band letter against the comparison year's anchor; header carries the comparison year
- **Profile** - `behavior_profile`
- **Context** - `context_window / 1000` with `K` suffix
- **Efforts** - supported levels from `model_id_startswith`: `L M H X MX`; `M` for thinking on/off models, `-` for temperature models
- **WF** - `WF_high` from the band; `WF_high * 0.5` when Efforts is `M` or `-`
- **In USD / Cache USD / Out USD** - standard-tier prices per 1M tokens; Devin-only: `cost_multiplier * 0.50` / `-` / `cost_multiplier * 2.50`
- **Devin cost** - multiplier from `windsurf-model-registry.json`
- **Notes** - `UC`, band and score (or `fallback` source), status, R4 evidence, effort quirks, `CSV rows` marker, adaptive-thinking Medium warning

### 8.4 Regeneration Triggers

- **New model or price change** - `update-model-registry.md` step 9.4: add `release_date` and Epoch band (or fallback) to the registry, run `update-model-inventory.py`
- **Fallback band received an Epoch score** - `match-epoch-eci.py` reports `replace_fallback`; registry band and label updated once
- **May 1** - comparison year advances; append `anchor(YY)` for the new year; regenerate Comp; record the previous year's measured top band in Section 3.1
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

- **`claude-opus-5`** (`26-B`, `standard`, WF 1.5): `max(ceil(3/1.5), ceil(18/6), ceil(7/3))` = `max(2, 3, 3)` = 3 prompts; checkpoint after prompt 2, then Final Checkpoint; cost 3 × 9.00 = $27
- **`glm-5.2`** (`26-E`, `guarded`, WF 0.5): `max(ceil(3/0.5), ceil(18/4), ceil(7/2))` = `max(6, 5, 4)` = 6 prompts; checkpoint after every prompt, strict scope guard; cost 3 × 2.00 = $6

Capacity drives GLM-5.2; instruction items drive Claude Opus 5. Neither dimension alone gives the right count. The MDLINVNTRY run of 2026-10-28 completed about 4.5 HWH on `glm-5.2` High in 8 implementation prompts with no skipped items, consistent with WF 0.5 (the former `26-D` WF 0.25 predicted 18).

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
- Band `E150` for `claude-opus-4-5` gives WF 0.5 HWH at High (label `25-B`, Comp `26-E`). Within a factor of 2 of the derived 1 h, which is the precision METR itself states [ASSUMED - interpretation]

Cross-year rate check: METR measured a 50%-horizon doubling time ([paper](https://arxiv.org/abs/2503.14499), [Time Horizon 1.1](https://metr.org/blog/2026-01-29-time-horizon-1-1/), [blog](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/)) of about 7 months for 2019-2025 and about 89 days since 2024 (Time Horizon 1.1), and calls the trend "around 1-4 doublings per year" [VERIFIED - LLMCAPCLS-IN01-SC-METR-PAPER, LLMCAPCLS-IN01-SC-METR-TH11, LLMCAPCLS-IN01-SC-METR-BLOG]. The Section 4 slope (WF halves every 10 ECI, anchors rise 15 ECI per year = 1.5 doublings per year) is at the conservative end. Conservative is acceptable: underestimated WF produces extra prompts (cost), overestimated WF produces skipped items (failure)

### 10.5 How to Explain It in One Paragraph

"HWH says how big a job is for a skilled human. Every model has a workload factor: how many of those hours fit into one prompt without the model dropping work. Divide HWH by the workload factor and you get the number of prompts. Cost is HWH times the price per workload factor. AWH, the time you wait, starts as one fifth of HWH and is replaced by measured minutes per prompt after a few sessions. All numbers are approximations within a factor of 2."

### 10.6 Exclusions

- **Story points, COCOMO (Constructive Cost Model), function points**: excluded - calibrated for human teams and projects, not single agent prompts; add estimation overhead without better accuracy at factor-2 precision
- **METR 50% horizon as WF directly**: excluded - 50% success means half the prompts fail; WF needs completion without skipping
- **Fixed HWH-to-AWH ratio as permanent rule**: excluded - engine, effort, and review load change the ratio; measured minutes per prompt replace it

## 11. Limitations

- **Anchor slope and WF slope are extrapolations**: +15 ECI per year holds for three measured years; WF halving per 10 ECI is an assumption inside METR's range (Section 10.4). A different measured slope changes anchors of future years and WF values, not existing labels
- **ECI measures general capability, not agentic completion**: Epoch's index aggregates benchmarks; `TBLF-IN02` (Section 6.1) shows effort level and thinking method can outweigh two bands on a structured-data task. The ledger remains the calibration path for WF
- **ECI pending models carry fallback bands**: 22 of 92 rows (`eci_band_source`) use a sibling or UC default band until Epoch publishes a score; `release_date_assumed` marks 29 dates not yet verified against a provider page (label year could shift for `glm-4.7-flash`, `glm-4.7-flashx` if the January 2026 date is wrong)
- **Comp changes at every wrap**: documents that cite Comp instead of Label go stale on May 1; `MODEL_INVENTORY.md` Section 4 requires Label in prompts files
- **Observations depend on the execution framework**: framework explains 56% of over-eagerness variance, base model 21% ([SNARE study](https://arxiv.org/abs/2605.28122)). Ledger lines carry `engine`; profiles derived from `cascade` runs may not hold in `claude-code` or `lana` runs [VERIFIED - LLMCAPCLS-IN01-SC-IPPS-IN06 Section 3, LLMCAPCLS-IN01-SC-SNARE]
- **Self-audit bias**: if the Final Checkpoint runs on the audited model, `guarded` models under-report skips. `self_audited_prompts` in `observed` lets the reviewer discount them [ASSUMED - IN07 Section 9]
- **Profile parameter values are unmeasured**: max_items 8/6/4 and the other Section 7.3 values come from IN06 reasoning, not from runs
- **Registry max output values are request limits**: `model-registry.json` `max_output` (for example 8K for `claude-opus-4-5` and `claude-haiku-4-5`) does not reflect provider-documented limits; the Notes column records provider values where they matter

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
- `LLMCAPCLS-IN01-SC-IPPS-MINV`: `PromptSystemV4.5/skills/write-documents/MODEL_INVENTORY.md` - former Class A-D definitions and WF values (kept in `MODEL_INVENTORY_v0.md`); current version with Label, Comp, Efforts, WF, 92 + 4 rows [VERIFIED]
- `LLMCAPCLS-IN01-SC-IPPS-MREG`: `PromptSystemV4.5/skills/llm-evaluation/model-registry.json` 1.11.0 - `release_date`, `eci_band`, `eci_score` (Epoch snapshot 2026-10-28), `eci_band_source`, `capability_label`, `behavior_profile` per model; top bands per year [VERIFIED]
- `LLMCAPCLS-IN01-SC-TBLF-IN02`: `e:\Dev\LLM-Research\_Sessions\_2026-03-05_TabularDataFormatsForLLMs\01_CSVScaleLimits\_INFO_01_CSVScaleLimits-TestResults.md` [TBLF-IN02] Section 5.1 and `_INFO_02_CSVScaleLimits-Findings.md` [TBLF-IN03] E1 - confirmed CSV extraction rows per model and effort (20 configurations, n=3, about 28% variance, May 2026); adaptive thinking at Medium skips reasoning (accessed 2026-10-29) [VERIFIED]
- `LLMCAPCLS-IN01-SC-IPPS-IN06`: `T01_MDLBHVPRM_BehavioralParameterBenchmarks_2026-10-19/_INFO_MDLBHVPRM-06_ModelAwarePartitioning.md` - behavior axes, partition parameters, IFEval mismatch for GLM-5.2, decision MDLBHVPRM-DD-01 [VERIFIED]
- `LLMCAPCLS-IN01-SC-IPPS-IN07`: `T01_MDLBHVPRM_BehavioralParameterBenchmarks_2026-10-19/_INFO_MDLBHVPRM-07_PromptFeedbackLoop.md` - observation ledger, IF/EG formulas, suggestion thresholds, registry properties, open points [VERIFIED]

## 13. Document History

**[2026-10-29 14:30]**
- Changed: letter definition from UC tier to Epoch ECI band relative to a year anchor (`anchor(YY) = 170 + 15 * (YY - 26)`, letters `A`-`Z`); Sections 2-6 rewritten
- Added: Comp (comparison-year label), May 1 wrap, `release_date` and `eci_band_source` registry fields, Section 6.1 TBLF cross-check, source `LLMCAPCLS-IN01-SC-TBLF-IN02`
- Changed: WF derived from the band (`2.0 * 2^(-(170 - band) / 10)`), one `WF` column plus `Efforts` column in the inventory
- Removed: October cap (former R3), UC-tier letters (former R2), max-output cap (former R5); replaced by R2 band freeze and R3 ECI-pending fallback
- Changed: inventory row set to every text model except `retired` (92 API rows); Summary, Sections 7.4, 8.1-8.4, 9.3, 10.4, 11 aligned

**[2026-10-29 13:37]**
- Changed: `R2` maps UC tiers to letters (`B` Apex, `C` Flagship, `D` Balanced, `E` Efficient) instead of WF-matching heuristic
- Changed: Section 6 labels updated to match `model-registry.json` 1.10.2 (40 label changes, R2 UC-tier separation, R3 pre-October `26-A` ban, added `25-D` tier)
- Fixed: `R3` changed from retroactive October promotion to a strict release-month gate (`YY-A` never assigned to models released before October 1 of `YY`)
- Fixed: `glm-5.2` moved from `26-D` (R4 downgrade) to `26-C` (UC-2 Flagship, over-eagerness changes profile only)
- Fixed: Fable/Opus/Sonnet no longer share `26-A`; each UC tier occupies its own letter

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
