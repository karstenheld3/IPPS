<PromptSystem MarkdownTablesAllowed=true />

# INFO: Benchmark Coverage Matrix

**Doc ID**: MDLRGUP-MDLBHVPRM-IN05
**Goal**: Check which models from both registries have benchmark data available

## Sources Tested

**Instruction Following (IF)**:
- **IFEval (llm-stats)**: 70 measured models
- **IFEval (benchgap)**: 139+ models (measured + estimated)
- **IFEval (LM Market Cap)**: 29 models
- **IFEval (Inference Index)**: additional models
- **WildBench HELM**: 68 models

**Eagerness (EG)**:
- **OverAct SIR**: 7 models
- **OverEager-Bench/SNARE**: 5-6 base models
- **YapBench**: 76 models

## LLM Evaluation Registry Coverage

Legend: Y = direct match, E = estimated (benchgap), P = proxy (similar model), - = no data

| Model                  | Status     | IF-IFEval | IF-IFEval Score     | IF-WildBench | EG-OverAct | EG-OverEager | EG-YapBench |
|------------------------|------------|-----------|---------------------|--------------|------------|--------------|-------------|
| gpt-6-astra            | untested   | -         |                     | -            | -          | -            | -           |
| gpt-5.6-sol            | available  | -         |                     | -            | -          | -            | -           |
| gpt-5.6-terra          | available  | -         |                     | -            | -          | -            | -           |
| gpt-5.6-luna           | available  | -         |                     | -            | -          | -            | -           |
| gpt-5.6-cyber          | untested   | -         |                     | -            | -          | -            | -           |
| gpt-5.5                | available  | E         | 93.3% est           | -            | -          | -            | -           |
| gpt-5.5-pro            | available  | -         |                     | -            | -          | -            | -           |
| gpt-5.4                | available  | E/Y       | 93.2-93.5%          | -            | -          | -            | -           |
| gpt-5.4-pro            | untested   | -         |                     | -            | -          | -            | -           |
| gpt-5.4-mini           | untested   | E         | 93.2% est           | -            | -          | -            | -           |
| gpt-5.4-nano           | untested   | E         | 93.3% est           | -            | -          | -            | -           |
| gpt-5.2                | available  | E/Y       | 93.0-93.3%          | -            | -          | -            | Y 86.8      |
| gpt-5.1                | available  | Y         | 92.5%               | Y 86.3%      | -          | -            | P 85.3      |
| gpt-5                  | available  | Y         | 90.0-93.5%          | Y 85.7%      | -          | -            | -           |
| gpt-5-mini             | available  | Y         | 93.9% (xref)        | Y 85.5%      | -          | -            | -           |
| gpt-5-nano             | available  | -         |                     | Y 80.6%      | -          | -            | -           |
| gpt-5.2-pro            | untested   | -         |                     | -            | -          | -            | -           |
| gpt-5-pro              | untested   | -         |                     | -            | -          | -            | -           |
| gpt-4.1                | available  | Y         | 87.2-87.4%          | Y 85.4%      | -          | -            | -           |
| gpt-4.1-mini           | available  | Y         | 84.1%               | Y 83.8%      | -          | -            | Y 75.7      |
| gpt-4.1-nano           | available  | -         |                     | Y 81.1%      | -          | -            | -           |
| gpt-4o                 | available  | Y         | 81.3-83.9%          | Y 82.8%      | -          | -            | -           |
| gpt-4o-mini            | available  | -         |                     | Y 79.1%      | -          | -            | -           |
| gpt-4o-2024-05-13      | legacy     | -         |                     | -            | -          | -            | -           |
| o1                     | untested   | Y         | listed              | -            | -          | -            | -           |
| o1-pro                 | untested   | -         |                     | -            | -          | -            | -           |
| o1-mini                | no_access  | -         |                     | -            | -          | -            | -           |
| o3                     | untested   | Y         | listed              | Y 86.1%      | -          | -            | Y 84.3      |
| o3-pro                 | untested   | -         |                     | -            | -          | -            | -           |
| o3-mini                | untested   | Y         | 93.9%               | -            | -          | -            | -           |
| o3-deep-research       | untested   | -         |                     | -            | -          | -            | -           |
| o4-mini                | untested   | Y         | listed              | Y 85.4%      | -          | -            | -           |
| o4-mini-deep-research  | untested   | -         |                     | -            | -          | -            | -           |
| computer-use-preview   | untested   | -         |                     | -            | -          | -            | -           |
| gpt-image-1.5          | untested   | -         |                     | -            | -          | -            | -           |
| claude-fable-5         | untested   | -         |                     | -            | -          | -            | -           |
| claude-mythos-5        | no_access  | -         |                     | -            | -          | -            | -           |
| claude-opus-5          | untested   | -         |                     | -            | -          | -            | -           |
| claude-sonnet-5        | untested   | -         |                     | -            | -          | -            | -           |
| claude-opus-4-8        | untested   | -         |                     | -            | -          | -            | -           |
| claude-opus-4-7        | untested   | Y         | 92.1% (infidx)      | -            | -          | -            | -           |
| claude-opus-4-6        | untested   | Y         | 92.8%               | -            | -          | -            | -           |
| claude-sonnet-4-6      | untested   | Y         | 90.5% (infidx)      | -            | -          | Y 21.15%     | -           |
| claude-opus-4-5        | available  | Y         | listed              | Y 85.2%      | -          | -            | -           |
| claude-opus-4-1        | retired    | -         |                     | -            | -          | -            | -           |
| claude-sonnet-4-5      | available  | Y         | 88.0%               | Y 85.4%      | -          | -            | -           |
| claude-haiku-4-5       | available  | Y         | listed              | Y 83.9%      | -          | -            | -           |
| claude-opus-4          | retired    | -         |                     | Y 83.3%      | -          | -            | -           |
| claude-sonnet-4        | retired    | -         |                     | Y 82.5%      | -          | -            | -           |
| claude-3-7-sonnet      | retired    | Y         | 93.2%               | Y 81.4%      | -          | -            | -           |
| claude-3-5-sonnet      | deprecated | -         |                     | Y 79.2%      | -          | -            | -           |
| claude-3-5-haiku       | retired    | -         |                     | -            | -          | -            | -           |
| claude-3-haiku         | retired    | -         |                     | -            | -          | -            | -           |
| glm-5.3                | available  | -         |                     | -            | -          | -            | -           |
| glm-5.3-flash          | available  | -         |                     | -            | -          | -            | -           |
| glm-5.2                | available  | E         | 93.2% est           | -            | Y 2.00     | -            | -           |
| glm-5.1                | available  | E         | 93.3% est           | -            | -          | -            | -           |
| glm-5                  | available  | -         |                     | -            | -          | Y 25.80%     | -           |
| glm-4.7                | available  | -         |                     | -            | -          | -            | Y 66.3      |
| glm-4.7-flashx         | available  | -         |                     | -            | -          | -            | -           |
| glm-4.7-flash          | available  | -         |                     | -            | -          | -            | -           |
| glm-4.6                | available  | -         |                     | -            | -          | Y 12.8%      | -           |
| glm-4.6v               | available  | -         |                     | -            | -          | -            | -           |
| glm-4.5v               | available  | -         |                     | -            | -          | -            | -           |
| glm-4.5-x              | available  | -         |                     | -            | -          | -            | -           |
| glm-4.5-flash          | available  | -         |                     | -            | -          | -            | -           |
| glm-4.5-airx           | available  | -         |                     | -            | -          | -            | -           |
| glm-4.5                | available  | -         |                     | Y 78.9%      | -          | -            | -           |
| glm-4-air              | available  | -         |                     | -            | -          | -            | -           |

## Devin Registry Coverage (Base Models Only)

Devin registry has ~200 entries but these collapse to ~40 unique base models after removing thinking/effort/fast/1M variants.

| Base Model             | IF-IFEval | IF-WildBench | EG-OverAct | EG-OverEager | EG-YapBench |
|------------------------|-----------|--------------|------------|--------------|-------------|
| Claude Fable 5/5.1     | -         | -            | -          | -            | -           |
| Claude Haiku 3.5       | -         | -            | -          | -            | -           |
| Claude Haiku 4.5       | Y         | Y 83.9%      | -          | -            | -           |
| Claude Opus 3.5        | -         | -            | -          | -            | -           |
| Claude Opus 4.5        | Y         | Y 85.2%      | -          | -            | -           |
| Claude Opus 4.6        | Y 92.8%   | -            | -          | -            | -           |
| Claude Opus 4.7        | Y 92.1%   | -            | -          | -            | -           |
| Claude Opus 4.8        | -         | -            | -          | -            | -           |
| Claude Opus 5          | -         | -            | -          | -            | -           |
| Claude Opus 5.5        | -         | -            | -          | -            | -           |
| Claude Sonnet 3.5      | -         | Y 79.2%      | -          | -            | -           |
| Claude Sonnet 4.5      | Y 88%     | Y 85.4%      | -          | -            | -           |
| Claude Sonnet 4.6      | Y 90.5%   | -            | -          | Y 21.15%     | -           |
| Claude Sonnet 5        | -         | -            | -          | -            | -           |
| Gemini 2.5 Pro         | -         | Y 85.7%      | -          | Y 21.55%     | -           |
| Gemini 3 Flash         | -         | -            | -          | -            | -           |
| Gemini 3.1 Pro         | E 93.3%   | -            | -          | -            | -           |
| Gemini 3.5 Flash       | E 93.3%   | -            | -          | -            | -           |
| Gemini 3.6-3.8 Flash   | -         | -            | -          | -            | -           |
| Gemini 4 Alpha         | -         | -            | -          | -            | -           |
| DeepSeek R2            | -         | -            | P 1.18     | -            | -           |
| GLM-5.2                | E 93.2%   | -            | Y 2.00     | -            | -           |
| Google M2              | -         | -            | -          | -            | -           |
| Grok 4/4.1             | -         | -            | -          | -            | Y 70.2      |
| GPT-4.1                | Y 87.4%   | Y 85.4%      | -          | -            | -           |
| GPT-4o                 | Y 83.9%   | Y 82.8%      | -          | -            | -           |
| GPT-5                  | Y 90-93%  | Y 85.7%      | -          | -            | -           |
| GPT-5.1                | Y 92.5%   | Y 86.3%      | -          | -            | P 85.3      |
| GPT-5.2                | Y 93.0%   | -            | -          | -            | Y 86.8      |
| GPT-5.3-Codex          | E 93.3%   | -            | -          | Y 9.80%      | Y 85.3      |
| GPT-5.4                | Y 93.5%   | -            | -          | -            | -           |
| GPT-5.5                | E 93.3%   | -            | -          | -            | -           |
| GPT-5.6 Sol/Terra/Luna | -         | -            | -          | -            | -           |
| GPT-5.8                | -         | -            | -          | -            | -           |
| GPT-OSS 120B           | -         | -            | -          | -            | -           |
| Kimi K2.6/K2.7/K3      | E 93.3%   | Y 86.2%      | P 1.60     | -            | Y 44.7      |
| MN Codex 2             | -         | -            | -          | -            | -           |
| NovaChem 3 Ultra       | -         | -            | -          | -            | -           |
| o3                     | Y         | Y 86.1%      | -          | -            | Y 84.3      |
| SWE-1.x/2              | -         | -            | -          | -            | -           |

## Coverage Summary

### LLM Evaluation Registry (75 models)

| Benchmark          | Models with data | Coverage |
|--------------------|-----------------|----------|
| IFEval (any)       | 27              | 36%      |
| IFEval (measured)  | 17              | 23%      |
| WildBench          | 19              | 25%      |
| IF (any source)    | 32              | 43%      |
| OverAct SIR        | 1               | 1%       |
| OverEager rate     | 3               | 4%       |
| YapBench           | 3               | 4%       |
| EG (any source)    | 6               | 8%       |

### Devin Registry (~40 base models)

| Benchmark          | Models with data | Coverage |
|--------------------|-----------------|----------|
| IFEval (any)       | 18              | 45%      |
| WildBench          | 12              | 30%      |
| IF (any source)    | 21              | 53%      |
| OverAct SIR        | 2               | 5%       |
| OverEager rate     | 3               | 8%       |
| YapBench           | 6               | 15%      |
| EG (any source)    | 8               | 20%      |

## Key Gaps

### Models with ZERO benchmark data across all sources

**LLM Evaluation Registry**:
- GPT-6 Astra, GPT-5.6 Sol/Terra/Luna/Cyber (too new)
- GPT-5.5 Pro, GPT-5.4 Pro, GPT-5.2 Pro, GPT-5 Pro (Pro variants)
- Claude Fable 5, Claude Mythos 5 (too new / no access)
- Claude Opus 5, Claude Sonnet 5, Claude Opus 4.8 (too new)
- Computer Use Preview, GPT Image 1.5 (non-text models)
- o1-pro, o3-pro, o3-deep-research, o4-mini-deep-research (specialty variants)
- GLM-4.7 FlashX/Flash, GLM-4.6V, GLM-4.5V/X/Flash/AirX, GLM-4 Air (Z.AI minor variants)

**Devin Registry**:
- Claude Fable 5/5.1, Claude Opus 5/5.5, Claude Sonnet 5 (too new)
- Claude Opus 4.8, Claude Opus 3.5 (niche)
- Gemini 3.6-3.8 Flash, Gemini 4 Alpha (too new)
- GPT-5.6 Sol/Terra/Luna, GPT-5.8 (too new)
- Google M2, MN Codex 2, NovaChem 3 Ultra (proprietary/unknown)
- SWE-1.x/2, Adaptive, Arena variants (Devin-internal, no benchmark equivalent)
- GPT-OSS 120B (open-source variant)

### Structural coverage problem

**instruction_following**: Reasonable coverage (43-53%). IFEval measured + estimated from benchgap covers most OpenAI and some Anthropic/GLM models. Main gap: newest models (5.6+, Fable, Opus 5) and Z.AI variants.

**eagerness**: Very poor coverage (8-20%). Only 6-8 models have any eagerness data. No OpenAI model has OverAct SIR data. Only Sonnet-4.6 and GPT-5.3-Codex have OverEager data. YapBench adds a few more but measures verbosity not scope.

## Verdict

**instruction_following**: Feasible for first assessment. Can populate ~50% of models from existing leaderboards. Remaining ~50% needs either proxy estimation from model family or own benchmarking.

**eagerness**: NOT feasible from existing benchmarks alone. Custom probe testing required for most models. Can use existing data to calibrate the probe and validate results.

## Document History

**[2026-10-19 16:55]**
- Initial coverage matrix compiled from 8 benchmark sources
