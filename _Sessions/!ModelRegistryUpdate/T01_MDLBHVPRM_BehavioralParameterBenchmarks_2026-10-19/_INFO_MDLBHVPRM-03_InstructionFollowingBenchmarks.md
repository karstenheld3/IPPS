# INFO: Instruction Following Benchmarks

**Doc ID**: MDLRGUP-MDLBHVPRM-IN03
**Goal**: Identify benchmarks with per-model scores to populate `instruction_following` (0.2-1.0) in model registry
**Strategy**: MEPI | **Domain**: DEFAULT

## Summary

IFEval is the standard instruction-following benchmark with the broadest model coverage. It directly produces a 0-1 score (prompt-level strict accuracy) that maps naturally to our `instruction_following` parameter. However, IFEval is **saturating** - frontier models cluster at 85-95%, reducing discrimination. IFBench and IFEval-Hard provide harder variants with more spread. WildBench provides complementary multi-task instruction following data.

**Recommendation**: Use IFEval prompt-level strict accuracy as primary source. It covers the most models and directly maps to our 0.2-1.0 scale. Augment with IFBench for frontier models where IFEval saturates.

## Benchmark Comparison

### IFEval (Primary - RECOMMENDED)

- **What it measures**: 25 types of verifiable instructions ("write at least 400 words", "respond in JSON", "include keyword X three times"). Programmatic scoring, no LLM judge.
- **Scale**: 0-1 (prompt-level strict accuracy). Directly maps to our `instruction_following` parameter.
- **Model coverage**: 70+ models on llm-stats.com, 139+ on benchgap.net, 854 results on SOTA2
- **Status**: Saturating. Most frontier models exceed 90%. High contamination risk.
- **Strengths**: Reproducible, cheap, judge-free, broad coverage, standard metric
- **Weaknesses**: Tests only format compliance (not semantic instruction following), saturating at top, high contamination

**Key scores for our registry models** (from multiple sources):
- GPT-5: 93.5% (IFEval-Hard source) / 90.0% (serenitiesai)
- GPT-5-mini: 93.9% (Qwen model card cross-reference)
- GPT-4.1: 87.4% (Qwen cross-ref) / 87.2% (IFEval-Hard) / 85.4% (WildBench)
- GPT-4.1-mini: 84.1% (llm-stats)
- GPT-4o: 83.9% (Qwen cross-ref) / 82.8% (WildBench) / 81.3% (IFEval-Hard)
- GPT-4o-mini: 79.1% (WildBench)
- Claude Sonnet 4.5: 88.0% (serenitiesai) / 85.4% (WildBench)
- Claude Haiku 4.5: 83.9% (WildBench)
- Claude 3.7 Sonnet: 93.2% (llm-stats) / 81.4% (WildBench)
- Claude 3.5 Sonnet: 79.2% (WildBench)
- o3: 86.1% (WildBench)
- o3-mini: 93.9% (llm-stats)
- GLM-4.5-Air: 78.9% (WildBench) [COMMUNITY] closest proxy for GLM family

Note: Scores vary across sources due to different IFEval variants (strict/loose, prompt/instruction level). IFEval-Hard and WildBench scores are consistently lower. Above scores are best available per model.

### IFBench (Secondary - for frontier discrimination)

- **What it measures**: 58 new verifiable constraints testing generalization beyond IFEval's 25. Counting, formatting, sentence/word/character manipulation, copying.
- **Scale**: 0-1 accuracy. Leading models (GPT-4.1, Claude 4 Sonnet) score **below 50%**.
- **Model coverage**: Limited. ~72 results on SOTA2, 6 models on Artificial Analysis.
- **Status**: Active, not saturating
- **Strengths**: High discriminative power, reveals overfitting to IFEval constraints
- **Weaknesses**: Limited model coverage, newer benchmark with fewer standardized results

**Key scores**: Most frontier models 25-50%. Top: Grok 4.3 Medium 83.3%, MiniMax-M3 82.9%, Qwen3.5-27B 77.8%.

### IFEval-Hard (Supplementary)

- **What it measures**: 148-item subset of IFEval where GPT-4o fails at least once in 20 runs
- **Scale**: 0-1, same metric as IFEval but much harder
- **Model coverage**: 7 models tested

**Key scores**:
- GPT-5: 82.4%
- GPT-5.2: 77.0%
- GPT-4.1: 58.1%
- GPT-4o: 39.9%
- DeepSeek V3.2: 73.0%

### WildBench HELM (Supplementary - broader task coverage)

- **What it measures**: Real user tasks from chatbot conversations, graded by rubric-guided judge. Covers coding, creative writing, instruction following.
- **Scale**: 0-100 WB Score
- **Model coverage**: 68 models. Excellent coverage of our registry models.
- **Strengths**: Real-world tasks, good model coverage, Stanford CRFM maintained
- **Weaknesses**: LLM-judged (inherits judge preferences), measures broader helpfulness not just IF

**Key scores** (full list in sources): GPT-5.1 86.3, GPT-5 85.7, GPT-5-mini 85.5, Claude Sonnet 4.5 85.4, GPT-4.1 85.4, Claude Haiku 4.5 83.9, GPT-4.1-mini 83.8, GPT-4o 82.8, GPT-4o-mini 79.1, GPT-5-nano 80.6, GPT-4.1-nano 81.1, GLM-4.5-Air 78.9.

## Mapping to `instruction_following` (0.2-1.0)

IFEval prompt-level strict accuracy maps directly:
- IFEval score of 0.95 -> `instruction_following` = 0.95
- IFEval score of 0.80 -> `instruction_following` = 0.80

**Floor**: No model scores below ~0.20 on IFEval. The 0.2 floor in our scale matches the empirical floor of early/small models.

**Ceiling**: Many frontier models cluster at 0.85-0.95. For discrimination at the top, use IFBench score (normalized to 0-1) as a tiebreaker.

**Proposed formula**: `instruction_following = IFEval_strict * 0.8 + IFBench_normalized * 0.2` (when IFBench data available). Otherwise: `instruction_following = IFEval_strict`.

## Limitations

- IFEval tests format compliance only (word count, JSON format, keyword inclusion), not semantic understanding of complex multi-step instructions. Our IPPS use case involves complex multi-constraint prompts. IFBench and WildIFEval better represent this.
- Score variance across sources (up to 10pp) due to different IFEval variants being reported without stating which one
- Z.AI (GLM) model coverage is sparse across all benchmarks. GLM-4.5-Air on WildBench is the only close proxy.
- No benchmark directly measures "following complex agentic workflow instructions" which is our actual use case

## Document History

**[2026-10-19 16:30]**
- Initial research completed
