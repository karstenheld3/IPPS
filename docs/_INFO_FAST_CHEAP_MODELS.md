# INFO: Fast and Cheap LLM Model Comparison

**Doc ID**: AMSW-IN01
**Goal**: Compare Grok Code Fast 1 speed/performance to other fast and cheap models

## Summary (Copy/Paste Ready)

**Speed Rankings (tokens/second)** [VERIFIED]
- Gemini 2.5 Flash: ~372 TPS (fastest)
- Grok Code Fast 1: ~236 TPS (very fast)
- GPT-5.2 variants: ~200+ TPS
- Claude Haiku 4.5: ~150-180 TPS (fast, cheap tier)
- DeepSeek V3: ~60-100 TPS (variable by provider)
- Claude Sonnet/Opus: ~80-120 TPS

**Best Fast + Cheap Options** [VERIFIED]
- Gemini 3 Flash: 372 TPS, 78% SWE-Bench (fastest + best coding)
- Grok Code Fast 1: 236 TPS, 70.8% SWE-Bench (Free in Windsurf)
- Claude Haiku 4.5: ~150 TPS, 73.3% SWE-Bench (1x Windsurf cost)
- DeepSeek V3: ~80 TPS, 38.8% SWE-Bench (Free, general purpose)

**Free Models in Windsurf** [TESTED]
- Grok Code Fast 1 (Free in Windsurf, normally $1.50/M output)
- DeepSeek R1/V3 (Free)
- GPT-5-Codex, GPT-5.1-Codex-Mini (Free)
- SWE-1, SWE-1.5 (Free)

**Recommendation**: For Windsurf free tier, Grok Code Fast 1 offers best speed-to-quality ratio for coding tasks.

## Detailed Findings

### Grok Code Fast 1 [VERIFIED]

Source: artificialanalysis.ai, x.ai

- **Speed**: 236 tokens/second (notably fast, 95th percentile)
- **Intelligence Index**: 29 (well above average of 18)
- **Pricing**: $0.20/1M input, $1.50/1M output
- **Context**: 256k tokens
- **SWE-Bench**: 70.8% (strong coding performance)
- **Verbosity**: Very verbose (65M tokens on eval vs 15M average)

Key characteristics:
- Optimized for agentic coding workflows
- "Fast daily driver" positioning
- Currently free in Windsurf (limited time)

### Claude Haiku 4.5 [VERIFIED]

Source: Anthropic, Reddit

- **Speed**: ~150-180 TPS (fast for Claude family)
- **Pricing**: 1x Windsurf cost
- **Context**: 200k tokens
- **SWE-Bench**: 73.3% (strong coding performance)
- **Quality**: Anthropic instruction-following quality

Key characteristics:
- Fastest Claude model
- Good balance of speed and quality
- Best cheap option for tasks requiring Anthropic-level instruction following

### DeepSeek V3 [VERIFIED]

Source: artificialanalysis.ai, Reddit

- **Speed**: Variable by provider (~60-100 TPS)
- **Intelligence Index**: 16 (below average)
- **Pricing**: $0.40/1M input, $0.89/1M output
- **Context**: 128k tokens
- **SWE-Bench**: 38.8% (V3.1 gets 53.8%)
- **Open Weights**: Yes (671B parameters, 37B active)

Key characteristics:
- Open source, can self-host
- Good price/performance for general tasks
- Newer V3.1 version available

### Gemini Flash Models [VERIFIED]

Source: Google, vellum.ai

- **Speed**: 300-372 TPS (fastest available)
- **Pricing**: ~$0.15-0.35 per 1M tokens
- **Context**: 1M+ tokens
- **SWE-Bench**: 78% (Gemini 3 Flash)

Key characteristics:
- Fastest inference speeds
- Good for high-volume, time-sensitive tasks
- Multiple tiers (Low/Medium/High)

### Speed Comparison Chart

```
Model                    | TPS     | Cost Category
-------------------------|---------|---------------
Gemini 2.5 Flash        | ~372    | Cheap
Grok Code Fast 1        | ~236    | Free (Windsurf)
GPT-5.2 variants        | ~200    | Moderate-High
Claude Haiku 4.5        | ~150    | Cheap (1x)
Claude Sonnet 4         | ~100    | Moderate (2x)
DeepSeek V3             | ~80     | Cheap
Claude Opus             | ~60     | Expensive
```

### Windsurf Free Tier Analysis

Models marked "Free" in windsurf-model-registry.json:

| Model | Best For | Speed Estimate |
|-------|----------|----------------|
| Grok Code Fast 1 | Coding, speed | Very Fast (~236 TPS) |
| DeepSeek R1 | Reasoning | Moderate |
| DeepSeek V3 | General | Moderate (~80 TPS) |
| GPT-5-Codex | Coding | Fast |
| GPT-5.1-Codex-Mini | Light coding | Very Fast |
| SWE-1.5 | Software engineering | Moderate |

## Exclusions

**Not considered**:
- Claude models (not free, 2x-20x cost)
- GPT-4o, GPT-5 (not free, 1x-2x cost)
- Reasoning-heavy models (o3, etc.) - different use case

## Sources

- https://artificialanalysis.ai/models/grok-code-fast-1 - Grok Code Fast 1 benchmarks [VERIFIED]
- https://x.ai/news/grok-code-fast-1 - Official xAI announcement [VERIFIED]
- https://artificialanalysis.ai/models/deepseek-v3 - DeepSeek V3 benchmarks [VERIFIED]
- https://artificialanalysis.ai/leaderboards/models - LLM speed leaderboard [VERIFIED]
- https://www.vellum.ai/llm-leaderboard - Speed rankings [VERIFIED]
- https://www.sentisight.ai/which-llm-best-answers-user-queries/ - Gemini speed data [ASSUMED]

## Document History

**[2026-01-26 16:20]**
- Initial research on Grok Code Fast 1 vs fast/cheap models
- Added speed benchmarks from artificialanalysis.ai
- Added Windsurf free tier analysis
