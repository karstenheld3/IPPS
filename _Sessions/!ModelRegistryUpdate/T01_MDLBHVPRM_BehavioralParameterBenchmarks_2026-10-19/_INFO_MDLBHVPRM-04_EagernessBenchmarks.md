# INFO: Eagerness Benchmarks

**Doc ID**: MDLRGUP-MDLBHVPRM-IN04
**Goal**: Identify benchmarks with per-model scores to populate `eagerness` (0.5-2.0) in model registry
**Strategy**: MEPI | **Domain**: DEFAULT

## Summary

"Eagerness" - the tendency to do more or less than asked - is a **hot research area in 2025-2026** under multiple names: overeager behavior, scope expansion, over-authorization, verbosity, and over-generation. Several benchmarks directly measure this concept:

1. **OverAct SIR** (Scope Inflation Ratio) is the closest direct mapping to our eagerness parameter: SIR=1.0 means exact scope, SIR=2.0+ means 2x over-authorization
2. **OverEager-Bench** measures overeager action rates in coding agents
3. **YapBench** measures verbosity (doing more with words than asked)
4. **DNR Bench** measures over-reasoning (thinking more than needed)

**Recommendation**: Use OverAct SIR as the primary metric for tool-calling models. Complement with OverEager rate (inverted) for coding agent context and YapBench YapIndex (normalized) for text generation context. Our eagerness scale (0.5-2.0) maps well to SIR with adjustment.

## Benchmark Comparison

### OverAct (Primary - RECOMMENDED for eagerness)

- **What it measures**: Scope Inflation Ratio (SIR) = actual tools called / minimal tools required. SIR=1.0 = exact scope, SIR=3.0 = 3x over-authorization.
- **Scale**: 1.0+ (ratio). Maps almost directly to our eagerness 0.5-2.0 scale (see mapping below).
- **Model coverage**: 7 models (Qwen3.6 family, DeepSeek v3/v4-Pro, GLM-5.2, Kimi-K2.7-Code)
- **Complementary metric**: Task Completion Rate (TCR) measures under-delivery

**Key SIR scores** [VERIFIED] (MDLBHVPRM-SC-LTKB-OVRACT):
- DeepSeek-v3: **1.18** (most restrained)
- Qwen3.6-Flash: **1.50**
- Kimi-K2.7-Code: **1.60**
- Qwen3.6-Plus: **1.65**
- Qwen3.7-Max: **1.74**
- GLM-5.2: **2.00**
- DeepSeek-v4-Pro: **2.39** (most over-eager)

**Strengths**: Deterministic judge-free scoring, ratio metric directly interpretable, 130K runs
**Weaknesses**: Only 7 models tested (no OpenAI, no Anthropic), tool-calling specific

### OverEager-Bench / SNARE OverEager (Secondary - coding agents)

- **What it measures**: Fraction of benign coding scenarios where the agent performs out-of-scope actions (deletes files, rewrites config user never mentioned)
- **Scale**: 0-100% overeager rate. Higher = more eager.
- **Model coverage**: 6 base models x 4 agent frameworks

**Key per-model means** [VERIFIED] (MDLBHVPRM-SC-ARXI-SNARE, across all frameworks):
- GPT-5.3-Codex: **9.80%** mean (most restrained)
- Sonnet-4.6: **21.15%** mean
- MiniMax-M2: **19.25%** mean
- Gemini-2.5-Pro: **21.55%** mean
- GLM-5: **25.80%** mean (most overeager)

**Per Claude Code framework** [VERIFIED] (MDLBHVPRM-SC-THAG-OVREG):
- MiniMax-M2.7: **11.8%**
- GLM-4.6: **12.8%**
- Claude Sonnet 4.6: **27.7%**

**Critical insight**: Framework dominates effect size (56%) over base model (21%). Same model (Sonnet-4.6) spans 1.1-27.7% across frameworks. This means eagerness is partially a system-level property, not just a model property. For our registry, we should use framework-controlled measurements or multi-framework averages.

### YapBench (Supplementary - verbosity dimension)

- **What it measures**: Excess response length beyond minimal sufficient answer. YapIndex = uniform-weighted average of category medians.
- **Scale**: YapIndex (lower = less verbose). Median excess characters.
- **Model coverage**: 76 models. Excellent coverage.

**Key YapIndex scores** [VERIFIED] (MDLBHVPRM-SC-ARXI-YAPBNCH, lower = better):
- gpt-3.5-turbo: **22.7** (least verbose)
- kimi-k2-0905: **44.7**
- gpt-4: **51.2**
- glm-4.7: **66.3**
- grok-4-fast: **70.2**
- gpt-4.1-mini: **75.7**
- o3: **84.3**
- gpt-5.1-codex: **85.3**
- gpt-5.2: **86.8**
- gpt-5.2 (reasoning): **89.8**

**Category-level insights** (Cat A = clarification, Cat B = factual, Cat C = code):
- GPT-5 is best on factual (Cat B excess: 8.5 chars) but not included in top-10 overall
- glm-4.7 is excellent on code (Cat C excess: 2 chars) but very verbose on clarification (138.5)

**Strengths**: Largest model coverage, simple interpretable metric, live leaderboard
**Weaknesses**: Measures text verbosity only (not action scope), newer models may not be listed

### DNR Bench (Supplementary - over-reasoning)

- **What it measures**: Whether reasoning models avoid unnecessary generation on trick prompts
- **Scale**: Accuracy 0-1 and token inefficiency ratio
- **Model coverage**: 8 models (GPT-4o, o3-mini, Claude 3.7, DeepSeek-R1 family)

**Key finding**: Reasoning models generate up to 70x more tokens than GPT-4o while achieving lower accuracy. GPT-4o (non-reasoning baseline) outperforms all reasoning models without instructions.

**Relevance to eagerness**: DNR Bench specifically tests the "thinking too much" dimension of eagerness. Useful for reasoning models (o-series, Claude thinking mode, DeepSeek-R1).

### ScopeBench (Supplementary - security/compliance context)

- **What it measures**: Scope adherence under goal pressure in security tasks. Dead-end construction proves violations.
- **Scale**: Raw capability %, scope adherence %
- **Model coverage**: 8 models

**Key finding**: Opus-4-8 achieves 10pp higher raw capability than Sonnet-4.6 while exhibiting 35.6pp higher scope adherence. Higher capability does not always mean more eagerness.

## Mapping to `eagerness` (0.5-2.0)

Our scale semantics:
- **0.5** = very lazy, completes only 50% of task
- **1.0** = exact scope, does exactly what asked
- **1.5** = somewhat over-eager, does 150% of instructions
- **2.0** = very over-eager, does 200% of instructions

### Proposed composite approach

Since no single benchmark covers all our models AND all dimensions of eagerness:

**Step 1 - OverAct SIR (where available)**:
- `eagerness = SIR` (direct mapping, SIR=1.0 already means exact scope)
- Cap at 2.0 for our scale (SIR=2.39 -> eagerness=2.0)
- Floor at 0.5 (no model tested below SIR=1.0; use TCR to detect under-delivery)

**Step 2 - OverEager rate (where available, no SIR)**:
- `eagerness = 1.0 + (overeager_rate_pct / 100)` (use mean across frameworks)
- 0% overeager -> 1.0 (exact scope), 50% overeager -> 1.5, 100% -> 2.0
- Below 1.0 needs separate "task completion" benchmark (not yet available)

**Step 3 - YapBench (where no scope benchmarks exist)**:
- Normalize YapIndex to 0-1 range using empirical min/max (22.7-400+)
- `eagerness = 1.0 + normalized_yapindex * 0.5` (maps to 1.0-1.5 range)
- Conservative: only captures verbosity, not action scope

**Step 4 - Expert estimate (models with no benchmark data)**:
- Based on model family behavior patterns and provider documentation
- Mark as `[ASSUMED]` in registry

### Coverage gap: Under-delivery (eagerness < 1.0)

No benchmark directly measures task under-completion (laziness). OverAct's TCR detects missing required tools (under-delivery), but TCR data alone doesn't distinguish "lazy" from "confused". The 0.5-1.0 range of our scale currently has no reliable benchmark source.

**Workaround**: Small models and highly safety-tuned models are empirically known to under-deliver. Set `eagerness < 1.0` only via manual testing or user reports.

## Available Per-Model Data for Our Registry

| Registry Model | OverAct SIR | OverEager Rate | YapBench | Proposed eagerness |
|---|---|---|---|---|
| GPT-5.x family | - | - | gpt-5.2: 86.8 | ~1.3 [ASSUMED] |
| GPT-4.1 | - | - | gpt-4.1-mini: 75.7 | ~1.2 [ASSUMED] |
| GPT-4o | - | - | gpt-4o: ~100+ | ~1.3 [ASSUMED] |
| Claude Sonnet 4.5/4.6 | - | 21.15% (mean) | - | 1.21 |
| Claude Haiku 4.5 | - | - | - | ~1.1 [ASSUMED] |
| o3/o3-mini | - | - | o3: 84.3 | ~1.3 [ASSUMED] |
| GLM-5.x | GLM-5.2: 2.00 | GLM-5: 25.80% | glm-4.7: 66.3 | 1.8 (composite) |
| DeepSeek-v3 proxy | 1.18 | - | - | 1.18 |

**Coverage assessment**: Poor for our specific models. OverAct tested none of our OpenAI/Anthropic models. OverEager tested Sonnet-4.6 and GPT-5.3-Codex (not in our registry). YapBench has the best coverage but measures only verbosity.

## Limitations

- Eagerness benchmarks are agent-framework-dependent (same model behaves differently in Claude Code vs OpenHands vs Codex CLI)
- No benchmark measures under-delivery ("laziness") on our 0.5-1.0 subscale
- OverAct and OverEager tested different model sets with minimal overlap to our registry
- Tool-calling eagerness (OverAct) and text verbosity (YapBench) are different dimensions - unclear how they correlate
- All eagerness benchmarks are from 2025-2026 and cover models from that period; older models in our registry have no data

## Document History

**[2026-10-19 16:40]**
- Initial research completed
