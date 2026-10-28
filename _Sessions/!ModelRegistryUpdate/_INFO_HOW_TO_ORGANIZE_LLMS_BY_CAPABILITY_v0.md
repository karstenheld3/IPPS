# INFO: How to Organize LLMs by Capability

**Doc ID**: LLMCAPCLS-IN01
**Goal**: Define a model capability classification whose labels stay valid when new models are released, and which yields an absolute workload factor (WF) per model for `MODEL_INVENTORY.md`
**Timeline**: Created 2026-10-28

**Depends on:**
- `_INFO_MDLBHVPRM-06_ModelAwarePartitioning.md [MDLRGUP-MDLBHVPRM-IN06]` for capacity, instruction following, and eagerness axes and decision MDLBHVPRM-DD-01 (observation overrides benchmarks)
- `_INFO_MDLBHVPRM-07_PromptFeedbackLoop.md [MDLRGUP-MDLBHVPRM-IN07]` for the checkpoint ledger that calibrates WF

## Summary

- **Generation-relative classes go stale**: `MODEL_INVENTORY.md` Class A-D is defined as "frontier" / "previous frontier generation", so every release cycle forces a re-grade of the whole table [VERIFIED - MODEL_INVENTORY.md Section 2]
- **Year-letter labels `YY-L` are permanent**: `YY` = release year, `L` = capability rank within that year (A = top, H = small local models). A label never changes because a newer model appears [ASSUMED]
- **One letter equals one year of progress**: `26-B ≈ 25-A`. This makes WF absolute: `WF_high = 2.0 * 0.5^letter_index * 2^(YY - 26)` [ASSUMED - calibrate with ledger]
- **YY-A is assignable only from October of YY**: until end of September the highest label of year YY is `YY-B`. On the October review the year's top models are promoted to `YY-A`, regardless of release month [ASSUMED - rule design]
- **Release timing supports the October cut only partly**: 2024 and 2025 flagships clustered in September to December (o1, Gemini 3 Pro, GPT-5.1, Claude Opus 4.5, GPT-5.2). 2026 flagships shipped June to September (Claude Fable 5, Claude Opus 5, GPT-6 Astra). Promotion instead of release date covers both patterns [VERIFIED - LLMCAPCLS-IN01-SC-NAIM-TMLN, LLMCAPCLS-IN01-SC-ARIX-HOME]
- **Mapping the current inventory keeps 36 of 37 WF values**: only `gpt-5.2` changes (0.5 → 1.0 at High) [ASSUMED - Section 6]
- **Registry is behind**: GPT-6 Sol (2026-09-22), Claude Opus 5.5 (2026-09-22), Gemini 4 Argon (2026-10-13) are released but missing from `model-registry.json` 1.9.0 [VERIFIED - LLMCAPCLS-IN01-SC-NAIM-TMLN]

## Table of Contents

1. [Problem with Generation-Relative Classes](#1-problem-with-generation-relative-classes)
2. [Year-Letter Label Format](#2-year-letter-label-format)
3. [Release Timing and the October Rule](#3-release-timing-and-the-october-rule)
4. [Workload Factor Formula](#4-workload-factor-formula)
5. [Assignment Rules](#5-assignment-rules)
6. [Proposed Labels for the Current Inventory](#6-proposed-labels-for-the-current-inventory)
7. [Weak Points and Open Questions](#7-weak-points-and-open-questions)
8. [Next Steps](#8-next-steps)
9. [Sources](#9-sources)
10. [Document History](#10-document-history)

## 1. Problem with Generation-Relative Classes

`MODEL_INVENTORY.md` Section 2 defines capacity classes by position relative to the newest models:

- Class A = "frontier models"
- Class B = "strong models, previous frontier generation"
- Class C = "mid models"
- Class D = "small or fast models"

When a new frontier generation ships (roughly every 6 months in 2025-2026, see Section 3), every existing model moves down one class. The WF of the model itself did not change, but its label did. Consequences:

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

- **A** - top models of the year (flagship, assignable only from October, see Section 3)
- **B** - flagship-class models; highest label before October
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

Flagship releases per year, from [Next AI Model timeline](https://www.nextaimodel.com/timeline) and [AI Release Index](https://aireleaseindex.com/):

- **2024**: Claude 3 Opus 2024-03-04, GPT-4o 2024-05-13, Claude 3.5 Sonnet 2024-06-20, o1 2024-09-12 (preview) / 2024-12-05, Claude 3.5 Sonnet (new) 2024-10-22 [VERIFIED - LLMCAPCLS-IN01-SC-ARIX-HOME, registry ID `claude-3-5-sonnet-20241022`]
- **2025**: Gemini 2.5 Pro 2025-03-25, o3 2025-04-16, Claude Opus 4 2025-05-22, GPT-5 2025-08-07, Claude Sonnet 4.5 2025-09-29, GPT-5.1 2025-11-12, Gemini 3 Pro 2025-11-18, Claude Opus 4.5 2025-11-24, GPT-5.2 2025-12-11 [VERIFIED - LLMCAPCLS-IN01-SC-NAIM-TMLN]
- **2026**: Claude Opus 4.6 2026-02-05, GPT-5.4 2026-03-05, GPT-5.5 2026-04-23, Claude Opus 4.8 2026-05-28, Claude Fable 5 2026-06-09, GPT-5.6 Sol 2026-07-09, Claude Opus 5 2026-07-24, GPT-6 Astra 2026-09-04, GPT-6 Sol 2026-09-22, Claude Opus 5.5 2026-09-22, Gemini 4 Argon 2026-10-13 [VERIFIED - LLMCAPCLS-IN01-SC-NAIM-TMLN]

Findings:

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

## 5. Assignment Rules

- **R1 - Year**: `YY` = year of general availability. Never changes
- **R2 - Letter**: `L` = capability rank within year YY, judged against the year's lineup and the cross-year link (`YY-B ≈ (YY-1)-A`)
- **R3 - October cap**: before October 1 of YY the highest assignable letter is B. October review promotes the year's top models to A. Labels freeze after December 31 of YY
- **R4 - Observation downgrade**: a documented observation (FAILS.md entry or findings-card ledger entry naming model and skipped items or out-of-scope actions) lowers the letter by one step within the same year. Notes column records the evidence. Labels never move up by observation (MDLBHVPRM-DD-01: observation overrides benchmark only toward stricter)
- **R5 - Hard limit cap**: max output below 32K tokens caps the letter at B of its year [ASSUMED - threshold from current Class C definition "max output 8K-32K"]

## 6. Proposed Labels for the Current Inventory

Release dates from Section 3.1 sources; models without a verified date marked [ASSUMED]. "Old" = current `MODEL_INVENTORY.md` class and WF at High. For models with one effort level only, WF_high is the High equivalent of the listed Medium value (Medium × 2).

**26-A (WF_high 2.0)** - October 2026 review promotes the year's top models:
- `claude-fable-5` (2026-06-09) - old A 2.0
- `claude-opus-5` (2026-07-24) - old A 2.0
- `gpt-6-astra` (2026-09-04) - old A 2.0
- `gpt-5.6-sol` (2026-07-09) - old A 2.0
- `gpt-5.5` (2026-04-23) - old A 2.0

**26-B (WF_high 1.0)**:
- `claude-opus-4-8` (2026-05-28), `claude-opus-4-7` (2026-04-16), `claude-opus-4-6` (2026-02-05) - old B 1.0
- `claude-sonnet-5` (2026-06-30), `gpt-5.6-terra` (2026-07-09), `gpt-5.4` (2026-03-05) - old B 1.0
- `GPT-5.3-Codex` (2026-02 [ASSUMED]), `Gemini 3.1 Pro` (2026-02-19) - Devin-only, old B 1.0

**26-C (WF_high 0.5)**:
- `claude-sonnet-4-6` (2026-02-17) - old C 0.5
- `glm-5.3` (2026 [ASSUMED]) - old C 0.5; R5 caps at B anyway (max output 16K)
- `Kimi K3` (2026 [ASSUMED]) - Devin-only, old C 0.5

**26-D (WF_high 0.25)**:
- `glm-5.2` (2026 [ASSUMED]) - base 26-C, R4 downgrade to 26-D (observed skipping and over-eagerness) - old D 0.25
- `glm-5.3-flash`, `glm-5.1`, `glm-5` (2026 [ASSUMED]) - old D 0.25. If `glm-5` is a 2025 release, label `25-C` gives the same WF
- `gpt-5.4-mini` (2026-03-17), `gpt-5.6-luna` (2026-07-09) - old D 0.25
- `Gemini 3.5 Flash` (2026-05-19), `Gemini 3.6 Flash` (2026-07-31), `Gemini 3.7 Flash` (2026 [ASSUMED]), `SWE-1.7` (2026 [ASSUMED]) - Devin-only, old D 0.25

**25-A (WF_high 1.0)**:
- `gpt-5.2` (2025-12-11) - old C 0.5. **Only changed value**: December 2025 top model, max output 32K (R5 not triggered)

**25-B (WF_high 0.5)**:
- `claude-opus-4-5` (2025-11-24) - top-class 2025 model, R5 cap (max output 8K) - old C 0.5
- `gpt-5.1` (2025-11-12), `gpt-5` (2025-08-07) - old C 0.5
- `claude-sonnet-4-5` (2025-09-29) - before October and R5 cap (max output 16K) - old C 0.5
- `o3` (2025-04-16), `gpt-4.1` (2025-04-14, no effort: Medium 0.25) - old C 0.5
- `Gemini 2.5 Pro` (2025-03-25, no effort: Medium 0.25) - Devin-only, old C 0.5

**25-C (WF_high 0.25)**:
- `claude-haiku-4-5` (2025-10-01), `gpt-5-mini` (2025-08-07) - old D 0.25
- `Gemini 3 Flash` (2025-12-17) - Devin-only, old D 0.25

Result: 36 of 37 rows keep their WF. The year-letter scheme reproduces the current table without the generation-relative definitions.

## 7. Weak Points and Open Questions

- **Cross-year rate is assumed**: "one letter per year" (WF doubling per year) is not measured. If the ledger shows `26-B` models completing less than `25-A` models, change the factor `2^(YY - 26)` to a measured value. Labels stay; only the formula changes
- **Letter assignment is judgment**: R2 ranks models within a year without a fixed metric. Mitigation: document the reason per row in the Notes column; benchmarks (IN06 Section 3) as tie-breaker
- **Promotion is a second touch**: R3 requires one review per year in October. Bind it to `update-model-registry.md` step 9.4 when run in October to December
- **Release date lookup for Devin-only and Z.AI models**: Kimi K3, SWE-1.7, Gemini 3.7 Flash, GLM-5.x lack verified dates in the sources used. For WF the year matters only at letter boundaries (`26-D` = `25-C`)
- **Behavior axes remain coarse**: one letter step per observation (R4) does not separate low instruction following from high eagerness. IN06/IN07 partition parameters (max_items, scope_guard) remain the per-prompt control
- **Missing registry entries**: GPT-6 Sol, Claude Opus 5.5, Gemini 4 Argon are released but not in `model-registry.json` 1.9.0. They are candidates for `26-A` on the October 2026 review

## 8. Next Steps

1. Replace `MODEL_INVENTORY.md` Section 2 capacity classes (including the TIER-A/B/C references) with Sections 2, 4, 5 of this document; replace the Class column with the labels from Section 6; recompute `gpt-5.2` WF columns
2. Add a `capability_label` property (`YY-L`) to `model-registry.json` entries so `MODEL_INVENTORY.md` reads it instead of storing it twice
3. Extend `update-model-registry.md` step 9.4: assign labels to new models (R1-R5); from October to December run the YY-A promotion review
4. Run `update-model-registry.md` to add GPT-6 Sol, Claude Opus 5.5, Gemini 4 Argon, then run the October 2026 promotion review

## 9. Sources

**Primary Sources:**
- `LLMCAPCLS-IN01-SC-NAIM-TMLN`: https://www.nextaimodel.com/timeline - release dates per model line: OpenAI GPT, Gemini Pro, Claude Opus 2021-2026, including GPT-6 Sol 2026-09-22, Claude Opus 5.5 2026-09-22, Gemini 4 Argon 2026-10-13 (accessed 2026-10-28) [VERIFIED]
- `LLMCAPCLS-IN01-SC-ARIX-HOME`: https://aireleaseindex.com/ - release index 2017-2026, including o1 2024-09-12, Claude Fable 5 2026-06-09, GPT-5.6 Sol/Terra/Luna 2026-07-09, Gemini 3 Flash 2025-12-17 (accessed 2026-10-28) [VERIFIED]
- `LLMCAPCLS-IN01-SC-BTLN-TMLN`: https://botlineage.com/timeline - o1 GA 2024-12-05, Claude Opus 4 2025-05-22 (accessed 2026-10-28) [VERIFIED]
- `LLMCAPCLS-IN01-SC-IPPS-MINV`: `PromptSystemV4.5/skills/write-documents/MODEL_INVENTORY.md` - current Class A-D definitions and WF values [VERIFIED]
- `LLMCAPCLS-IN01-SC-IPPS-MREG`: `PromptSystemV4.5/skills/llm-evaluation/model-registry.json` 1.9.0 - dated Anthropic model IDs, max output per prefix [VERIFIED]
- `LLMCAPCLS-IN01-SC-IPPS-IN06`: `T01_MDLBHVPRM_BehavioralParameterBenchmarks_2026-10-19/_INFO_MDLBHVPRM-06_ModelAwarePartitioning.md` - behavior axes, decision MDLBHVPRM-DD-01 [VERIFIED]

## 10. Document History

**[2026-10-28 18:05]**
- Initial research document created: year-letter labels `YY-L`, October promotion rule, WF formula, mapping of 37 inventory rows
