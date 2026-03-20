# Pricing and Model Selection

**Doc ID**: ANTAPI-IN12
**Goal**: Document token pricing, feature-specific pricing multipliers, and model selection guidance
**API version**: anthropic-version 2023-06-01

**Depends on:**
- `_INFO_ANTAPI-IN11_MODELS.md [ANTAPI-IN11]` for model capabilities

## Summary

Anthropic prices API usage by input and output tokens per million (MTok). Pricing varies by model tier (Opus, Sonnet, Haiku) and is modified by feature-specific multipliers: prompt caching (0.1x for cache reads, 1.25x/2x for cache writes), batch processing (0.5x), data residency (1.1x for US-only), fast mode (6x), and long context surcharges. Tool use adds system prompt tokens that vary by model and tool_choice setting. Third-party platforms (Bedrock, Vertex AI, Azure) have their own pricing with optional regional endpoint premiums.

## Key Facts

- **Unit**: Per million tokens (MTok)
- **Billing**: Input tokens + output tokens, per request
- **Batch Discount**: 50% on all tokens
- **Cache Read**: 10% of base input price
- **Cache Write (5m)**: 125% of base input price
- **Cache Write (1h)**: 200% of base input price
- **Fast Mode**: 6x standard rates (Opus 4.6 only)
- **Data Residency (US)**: 1.1x multiplier (Opus 4.6+ models)
- **Multipliers Stack**: Cache + batch + data residency + fast mode all compound

## Feature-Specific Pricing

### Prompt Caching Multipliers (relative to base input price)

- **Cache write (5m TTL)**: 1.25x base input price
- **Cache write (1h TTL)**: 2x base input price
- **Cache read**: 0.1x base input price (10% of standard)

Cache reads pay off after 1 read (5m duration) or 2 reads (1h duration).

### Batch Processing

- **All tokens**: 50% discount (0.5x multiplier on input and output)

### Data Residency

- **US-only inference** (`inference_geo`): 1.1x multiplier on all token categories
- **Global routing** (default): Standard pricing
- Applies to Claude Opus 4.6+ models only; earlier models unaffected

### Fast Mode (Beta)

- **All tokens**: 6x standard rates
- Available for Claude Opus 4.6 only
- Not available with Batch API
- Stacks with caching and data residency multipliers

### Long Context Pricing

Input tokens beyond 200K incur additional pricing (model-specific surcharges apply).

### Tool Use Pricing

Tool use adds hidden system prompt tokens (varies by model and tool_choice):

- Tool definitions (names, descriptions, schemas) count as input tokens
- `tool_use` and `tool_result` content blocks count normally
- Server-side tools (web search) may incur additional per-use charges
- If no tools provided, `tool_choice: none` uses 0 additional system prompt tokens

## Third-Party Platform Pricing

- **AWS Bedrock**: https://aws.amazon.com/bedrock/pricing/
- **Google Vertex AI**: https://cloud.google.com/vertex-ai/generative-ai/pricing
- **Microsoft Foundry**: https://azure.microsoft.com/en-us/pricing/details/ai-foundry/

Starting with Claude Sonnet 4.5 and Haiku 4.5:

- **Global endpoints**: Dynamic routing, standard pricing
- **Regional endpoints**: Guaranteed geography, 10% premium

## Cost Optimization Strategies

### Use Prompt Caching for Repeated Context

```python
import anthropic

client = anthropic.Anthropic()

# Cache a large system prompt (pays off after 1 read with 5m TTL)
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "You are an expert assistant with deep knowledge of...",
            "cache_control": {"type": "ephemeral"},  # 5m TTL, 1.25x write
        }
    ],
    messages=[{"role": "user", "content": "Question 1"}],
)
# Subsequent calls with same system prompt hit cache at 0.1x
```

### Use Batch API for Non-Urgent Work

```python
# 50% discount on all tokens
batch = client.messages.batches.create(
    requests=[
        {
            "custom_id": f"item-{i}",
            "params": {
                "model": "claude-haiku-3-5-20241022",  # Cheapest model
                "max_tokens": 256,
                "messages": [{"role": "user", "content": f"Process item {i}"}],
            },
        }
        for i in range(1000)
    ]
)
```

### Choose the Right Model

```python
# Cost-sensitive: Use Haiku for simple tasks
response = client.messages.create(
    model="claude-haiku-3-5-20241022",
    max_tokens=256,
    messages=[{"role": "user", "content": "Classify this text: ..."}],
)

# Quality-sensitive: Use Sonnet for balanced tasks
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Analyze this document..."}],
)

# Maximum capability: Use Opus for complex reasoning
response = client.messages.create(
    model="claude-opus-4-20250115",
    max_tokens=4096,
    messages=[{"role": "user", "content": "Design an architecture for..."}],
)
```

## Gotchas and Quirks

- Tool use adds hidden system prompt tokens even when tool_choice is "auto" or "any"
- Pricing multipliers stack multiplicatively (e.g., batch + cache read = 0.5 * 0.1 = 0.05x base)
- Fast mode is not compatible with Batch API
- Data residency pricing only affects Opus 4.6+ models
- Third-party platform pricing differs from direct API pricing
- Regional endpoints on Bedrock/Vertex have a 10% premium over global endpoints
- Use 1h cache TTL with batches (5m may expire before batch processes)

## Related Endpoints

- `_INFO_ANTAPI-IN11_MODELS.md [ANTAPI-IN11]` - Model capabilities and context windows
- `_INFO_ANTAPI-IN18_PROMPT_CACHING.md [ANTAPI-IN18]` - Caching implementation
- `_INFO_ANTAPI-IN10_BATCHES.md [ANTAPI-IN10]` - Batch processing
- `_INFO_ANTAPI-IN08_TOKEN_COUNTING.md [ANTAPI-IN08]` - Pre-request cost estimation

## Sources

- ANTAPI-SC-ANTH-PRICING - https://platform.claude.com/docs/en/about-claude/pricing - Full pricing tables, multipliers
- ANTAPI-SC-ANTH-MODCHSE - https://platform.claude.com/docs/en/about-claude/models/choosing-a-model - Model selection
- ANTAPI-SC-ANTH-MODDEP - https://platform.claude.com/docs/en/about-claude/model-deprecations - Deprecation schedule

## Document History

**[2026-03-20 03:00]**
- Initial documentation created from pricing and model selection pages
