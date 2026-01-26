# INFO: OpenAI and Anthropic Model Costs

**Doc ID**: LLMEV-IN02
**Goal**: Document current API pricing for OpenAI and Anthropic models (January 2026)

## Copy-Paste Ready Pricing

### OpenAI (USD per 1M tokens)

**GPT-5 Family:**
- **gpt-5.2**: $1.75 input, $14.00 output
- **gpt-5.1 / gpt-5**: $1.25 input, $10.00 output
- **gpt-5-mini**: $0.25 input, $2.00 output
- **gpt-5-nano**: $0.05 input, $0.40 output
- **gpt-5.2-pro**: $21.00 input, $168.00 output
- **gpt-5-pro**: $15.00 input, $120.00 output

**GPT-4 Family:**
- **gpt-4.1**: $2.00 input, $8.00 output
- **gpt-4.1-mini**: $0.40 input, $1.60 output
- **gpt-4.1-nano**: $0.10 input, $0.40 output
- **gpt-4o**: $2.50 input, $10.00 output
- **gpt-4o-mini**: $0.15 input, $0.60 output

**o-Series (Reasoning):**
- **o4-mini**: $1.10 input, $4.40 output
- **o3-mini**: $1.10 input, $4.40 output
- **o3-deep-research**: $10.00 input, $40.00 output
- **o1**: $15.00 input, $60.00 output
- **o1-mini**: $1.10 input, $4.40 output
- **o1-pro**: $150.00 input, $600.00 output

### Anthropic (USD per 1M tokens)

- **claude-opus-4.1 / opus-4**: $15.00 input, $75.00 output
- **claude-sonnet-4 / sonnet-3.7 / sonnet-3.5**: $3.00 input, $15.00 output
- **claude-haiku-3.5**: $0.80 input, $4.00 output
- **claude-haiku-3**: $0.25 input, $1.25 output

### Caching Discounts (Anthropic)

- Cache writes (5-min): 1.25x base input price
- Cache writes (1-hour): 2x base input price
- Cache reads: 0.1x base input price

## Research Findings

### OpenAI Pricing Structure

GPT-5 family released August 2025:
- **GPT-5.2**: Latest flagship, $1.75/1M input, $14.00/1M output
- **GPT-5.1 / GPT-5**: $1.25/1M input, $10.00/1M output, 400K context
- **GPT-5 Mini**: $0.25/1M input, $2.00/1M output
- **GPT-5 Nano**: $0.05/1M input, $0.40/1M output
- **GPT-5.2-pro / GPT-5-pro**: Extended thinking, $15-21/1M input, $120-168/1M output

GPT-4 series:
- **GPT-4.1**: $2.00/1M input, $8.00/1M output
- **GPT-4.1-mini**: $0.40/1M input, $1.60/1M output
- **GPT-4.1-nano**: $0.10/1M input, $0.40/1M output
- **GPT-4o**: $2.50/1M input, $10.00/1M output
- **GPT-4o-mini**: $0.15/1M input, $0.60/1M output

o-Series (Reasoning models):
- **o4-mini / o3-mini / o1-mini**: $1.10/1M input, $4.40/1M output
- **o3-deep-research**: $10.00/1M input, $40.00/1M output
- **o1**: $15.00/1M input, $60.00/1M output
- **o1-pro**: $150.00/1M input, $600.00/1M output

Newer models (gpt-5, o1, o3) use `max_completion_tokens` parameter instead of `max_tokens`.

### Anthropic Pricing Structure

Claude Opus 4 series:
- **Claude Opus 4.1 / Opus 4**: $15.00/1M input, $75.00/1M output (most powerful)
- Context: 200K standard, up to 1M beta

Claude Sonnet series:
- **Claude Sonnet 4 / 3.7 / 3.5**: $3.00/1M input, $15.00/1M output (mid-tier)

Claude Haiku series:
- **Claude Haiku 3.5**: $0.80/1M input, $4.00/1M output (latest small)
- **Claude Haiku 3**: $0.25/1M input, $1.25/1M output (earlier)

Long context (>200K tokens): 2x input cost beyond threshold.

### Cost Calculation Example

For claude-opus-4-1 transcription test (83,020 input + 47,648 output tokens):
- Input cost: 83,020 / 1,000,000 * $15.00 = $1.25
- Output cost: 47,648 / 1,000,000 * $75.00 = $3.57
- **Total: $4.82**

## Sources

- **pricepertoken.com** - GPT-5 pricing: $1.25 input, $10.00 output
  - URL: https://pricepertoken.com/pricing-page/model/openai-gpt-5
  - Finding: GPT-5 released Aug 2025, 400K context

- **intuitionlabs.ai** - LLM API Pricing Comparison 2025
  - URL: https://intuitionlabs.ai/articles/llm-api-pricing-comparison-2025
  - Findings:
    - GPT-5: $1.25/$10.00, GPT-5 Mini: $0.25/$2.00, GPT-5 Nano: $0.05/$0.40
    - Claude Opus 4.1: $15/$75, Sonnet 4: $3/$15, Haiku 3.5: $0.80/$4
    - Anthropic offers 50% batch discount, caching discounts

- **platform.claude.com** - Official Anthropic pricing
  - URL: https://platform.claude.com/docs/en/about-claude/pricing
  - Finding: Cache reads 0.1x base, cache writes 1.25-2x base

## Document History

**[2026-01-22 23:25]**
- Initial research for LLM Evaluation skill cost analysis
