# INFO: OpenAI and Anthropic API Caching

**Doc ID**: LLMEV-IN02
**Goal**: Document prompt caching and predicted outputs for OpenAI and Anthropic APIs to enable `--use-llm-caching` flag in llm-evaluation scripts
**Timeline**: Created 2026-01-26

## Summary

**OpenAI Prompt Caching:**
- Automatic, no code changes needed [VERIFIED]
- 50% discount on cached input tokens [VERIFIED]
- Minimum 1024 tokens, 128-token increments [VERIFIED]
- 5-10 minute TTL, cleared after 1 hour of inactivity [VERIFIED]
- Response: `usage.prompt_tokens_details.cached_tokens` [VERIFIED]

**OpenAI Predicted Outputs:**
- Reduces latency when output is partially known [VERIFIED]
- Add `prediction: {type: "content", content: "..."}` parameter [VERIFIED]
- Rejected tokens charged at output token rates [VERIFIED]
- NOT compatible with tools/function calling [VERIFIED]

**Anthropic Prompt Caching:**
- Explicit: requires `cache_control: {type: "ephemeral"}` on content blocks [VERIFIED]
- 90% discount on cached reads (0.1x base price), 25% premium on writes (1.25x) [VERIFIED]
- Minimum 1024-4096 tokens depending on model [VERIFIED]
- 5-minute default TTL, optional 1-hour (2x write cost) [VERIFIED]
- Response: `cache_creation_input_tokens`, `cache_read_input_tokens` [VERIFIED]

**Implementation Recommendation:**
- `--use-prompt-caching`: Enable Anthropic cache_control on system/context blocks
- OpenAI prompt caching is automatic - just ensure prompts are >1024 tokens
- Predicted outputs not applicable to llm-evaluation (not for varied responses)

## Table of Contents

1. [OpenAI Prompt Caching](#1-openai-prompt-caching)
2. [OpenAI Predicted Outputs](#2-openai-predicted-outputs)
3. [Anthropic Prompt Caching](#3-anthropic-prompt-caching)
4. [Implementation Strategy](#4-implementation-strategy)
5. [Sources](#5-sources)
6. [Next Steps](#6-next-steps)
7. [Document History](#7-document-history)

## 1. OpenAI Prompt Caching

### 1.1 How It Works

OpenAI prompt caching is **automatic** - no API changes required. The system:
1. Caches the longest prefix of prompts >1024 tokens
2. Checks if cached prefix exists from recent queries
3. Applies 50% discount on cached tokens

**Key characteristics:**
- **Automatic**: Applied without code changes
- **Minimum**: 1024 tokens to enable caching
- **Increment**: 128-token chunks
- **TTL**: 5-10 minutes inactive, max 1 hour
- **Isolation**: Caches not shared between organizations

### 1.2 Pricing

| Model | Uncached Input | Cached Input | Discount |
|-------|----------------|--------------|----------|
| GPT-4o | $2.50/M | $1.25/M | 50% |
| GPT-4o mini | $0.15/M | $0.075/M | 50% |
| o1 | $15.00/M | $7.50/M | 50% |
| o1 mini | $3.00/M | $1.50/M | 50% |

### 1.3 Response Structure

```python
usage = {
    "prompt_tokens": 2006,
    "completion_tokens": 300,
    "prompt_tokens_details": {
        "cached_tokens": 1920,  # Tokens read from cache
        "audio_tokens": 0
    }
}
```

### 1.4 Implementation Notes

No changes needed to enable. To maximize cache hits:
- Keep static content (system prompts, context) at prompt beginning
- Ensure prompts exceed 1024 tokens for caching eligibility
- Reuse identical prefixes across calls

## 2. OpenAI Predicted Outputs

### 2.1 How It Works

Predicted Outputs reduce latency when the output is largely known ahead of time (e.g., code refactoring with minor changes).

**Request parameter:**
```python
completion = client.chat.completions.create(
    model="gpt-4.1",
    messages=[...],
    prediction={
        "type": "content",
        "content": "expected output text"
    }
)
```

### 2.2 Response Structure

```python
usage = {
    "completion_tokens_details": {
        "accepted_prediction_tokens": 60,  # Tokens from prediction used
        "rejected_prediction_tokens": 0    # Tokens not used (still charged)
    }
}
```

### 2.3 Limitations

- **Models**: GPT-4o, GPT-4o-mini, GPT-4.1, GPT-4.1-mini, GPT-4.1-nano only
- **No tools**: Function calling not supported
- **No max_completion_tokens**: Parameter not supported
- **Rejected tokens charged**: Unused predictions still billed at output rates

### 2.4 Applicability to llm-evaluation

**NOT RECOMMENDED** for llm-evaluation scripts because:
- Evaluation outputs are not predictable
- Transcription outputs vary significantly
- Judge scores are unpredictable
- Would add complexity without benefit

## 3. Anthropic Prompt Caching

### 3.1 How It Works

Anthropic caching is **explicit** - requires `cache_control` parameter on content blocks.

**Request structure:**
```python
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    system=[
        {"type": "text", "text": "You are an assistant..."},
        {
            "type": "text",
            "text": "<large context here>",
            "cache_control": {"type": "ephemeral"}  # Enable caching
        }
    ],
    messages=[{"role": "user", "content": "Question here"}]
)
```

### 3.2 Cache Hierarchy

Cache prefixes follow order: `tools` -> `system` -> `messages`

Changes at each level invalidate that level and all subsequent levels.

### 3.3 Minimum Token Requirements

| Model | Minimum Cacheable Tokens |
|-------|-------------------------|
| Claude Opus 4.5 | 4096 |
| Claude Opus 4.1, Opus 4, Sonnet 4.5, Sonnet 4 | 1024 |
| Claude Haiku 4.5 | 4096 |
| Claude Haiku 3.5, Haiku 3 | 2048 |

### 3.4 Pricing

| Duration | Write Cost | Read Cost |
|----------|------------|-----------|
| 5-minute (default) | 1.25x base input | 0.1x base input |
| 1-hour (optional) | 2.0x base input | 0.1x base input |

**Example:** Claude Sonnet 4 at $3/M input tokens:
- Cache write (5m): $3.75/M
- Cache read: $0.30/M (90% savings!)

### 3.5 TTL Options

```python
# Default 5-minute cache
"cache_control": {"type": "ephemeral"}

# Explicit 5-minute
"cache_control": {"type": "ephemeral", "ttl": "5m"}

# Extended 1-hour cache
"cache_control": {"type": "ephemeral", "ttl": "1h"}
```

### 3.6 Response Structure

```python
usage = {
    "input_tokens": 50,                    # Tokens after last cache breakpoint
    "cache_creation_input_tokens": 10000,  # New tokens written to cache
    "cache_read_input_tokens": 0,          # Tokens read from cache
    "output_tokens": 500
}

# Total input = cache_read + cache_creation + input_tokens
```

### 3.7 Best Practices

1. Place static content at prompt beginning
2. Mark end of reusable content with `cache_control`
3. Use up to 4 cache breakpoints per request
4. For multi-turn: set breakpoint at conversation end

### 3.8 Thinking Blocks

Extended thinking blocks have special caching behavior:
- Cannot be explicitly marked with `cache_control`
- Automatically cached alongside other content in tool use flows
- Count as input tokens when read from cache

## 4. Implementation Strategy

### 4.1 Proposed Flag

```
--use-prompt-caching    Enable prompt caching (Anthropic explicit, OpenAI automatic)
```

### 4.2 OpenAI Changes

**Minimal changes required:**
- Track `cached_tokens` in metadata output
- No API call changes needed (automatic)

```python
# In metadata output
if hasattr(response.usage, 'prompt_tokens_details'):
    metadata["cached_tokens"] = response.usage.prompt_tokens_details.cached_tokens
```

### 4.3 Anthropic Changes

**Moderate changes required:**
- Restructure system prompt to use content blocks array
- Add `cache_control` to static content blocks

```python
def call_anthropic_with_caching(client, model, prompt, api_params, 
                                 use_caching=False, cache_ttl="5m"):
    """Call Anthropic API with optional prompt caching."""
    
    if use_caching:
        # Split prompt into cacheable system + variable user message
        system_content = [
            {
                "type": "text",
                "text": prompt,
                "cache_control": {"type": "ephemeral", "ttl": cache_ttl}
            }
        ]
        call_params["system"] = system_content
        messages = [{"role": "user", "content": "Process the above."}]
    else:
        messages = [{"role": "user", "content": prompt}]
    
    # ... rest of call
```

### 4.4 Batch Processing Benefit

For `call-llm-batch.py`, caching is most beneficial when:
- Same prompt template applied to multiple files
- System prompt is large and static
- Many sequential calls within 5-minute window

**Example workflow:**
```
File 1: Cache MISS (write 10K tokens @ 1.25x)
File 2: Cache HIT (read 10K tokens @ 0.1x) - 90% savings
File 3: Cache HIT (read 10K tokens @ 0.1x) - 90% savings
...
```

### 4.5 Cost Tracking

Update `analyze-costs.py` to calculate:
- Cache write cost (Anthropic only)
- Cache read savings
- Net cost with caching vs without

## 5. Sources

**Primary Sources:**
- `LLMEV-IN02-SC-OAIP-PRMCCH`: https://openai.com/index/api-prompt-caching/ - OpenAI prompt caching announcement, 50% discount, automatic [VERIFIED]
- `LLMEV-IN02-SC-OAIP-PRDOUT`: https://platform.openai.com/docs/guides/predicted-outputs - Predicted outputs for latency reduction [VERIFIED]
- `LLMEV-IN02-SC-ANTH-PRMCCH`: https://platform.claude.com/docs/en/build-with-claude/prompt-caching - Anthropic cache_control, pricing, TTL options [VERIFIED]
- `LLMEV-IN02-SC-ANTH-ANNC`: https://www.anthropic.com/news/prompt-caching - Anthropic caching announcement [VERIFIED]

## 6. Next Steps

1. Add `--use-prompt-caching` flag to `call-llm.py` and `call-llm-batch.py`
2. Restructure Anthropic calls to use system content blocks with `cache_control`
3. Track cache metrics in metadata output (both providers)
4. Update `analyze-costs.py` to calculate cache savings
5. Test with large prompts (>1024 tokens) to verify cache hits

## 7. Document History

**[2026-01-26 22:30]**
- Initial research document created
- Documented OpenAI automatic prompt caching
- Documented OpenAI predicted outputs (not applicable to llm-evaluation)
- Documented Anthropic explicit prompt caching with cache_control
- Proposed implementation strategy with --use-prompt-caching flag
