# Prompt Caching

**Doc ID**: ANTAPI-IN18
**Goal**: Document prompt caching mechanisms, automatic vs explicit, TTL options, and pricing
**API version**: anthropic-version 2023-06-01

**Depends on:**
- `_INFO_ANTAPI-IN06_MESSAGES.md [ANTAPI-IN06]` for Messages API request schema

## Summary

Prompt caching reduces costs and latency by reusing previously processed prompt prefixes across API calls. Two approaches exist: automatic caching (top-level `cache_control` that auto-applies to the last cacheable block) and explicit cache breakpoints (`cache_control` on individual content blocks). Cache reads cost 10% of standard input price. Two TTL options: 5 minutes (default, 1.25x write cost) and 1 hour (2x write cost). The cache covers the full prefix including tools, system, and messages up to the designated breakpoint.

## Key Facts

- **Automatic**: Top-level `cache_control: {"type": "ephemeral"}` on request body
- **Explicit**: `cache_control: {"type": "ephemeral"}` on individual content blocks
- **TTL Options**: `"5m"` (default, 1.25x write), `"1h"` (2x write)
- **Cache Read**: 0.1x base input price (10%)
- **Cache Scope**: Full prefix (tools -> system -> messages up to breakpoint)
- **Refresh**: Cache refreshed at no cost each time cached content is used
- **Min Tokens**: Minimum cacheable prefix size varies by model
- **Status**: GA

## Automatic Caching

Simplest approach. Add `cache_control` at top level; system auto-applies to last cacheable block:

```python
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    cache_control={"type": "ephemeral"},  # Auto-applies to last cacheable block
    system="You are a helpful assistant with deep knowledge of quantum physics.",
    messages=[
        {"role": "user", "content": "What is quantum entanglement?"},
    ],
)
print(f"Cache write: {message.usage.cache_creation_input_tokens}")
print(f"Cache read: {message.usage.cache_read_input_tokens}")
```

### Multi-turn with Automatic Caching

As conversations grow, automatic caching extends the cache to include new messages:

```python
messages = [
    {"role": "user", "content": "What is quantum entanglement?"},
    {"role": "assistant", "content": "Quantum entanglement is..."},
    {"role": "user", "content": "How is it used in quantum computing?"},
]

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    cache_control={"type": "ephemeral"},
    system="You are a helpful assistant.",
    messages=messages,
)
# Previous turns are read from cache; new turn triggers cache write extension
```

## Explicit Cache Breakpoints

For fine-grained control, place `cache_control` on specific content blocks:

```python
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "You are an expert assistant with extensive knowledge of...",
            "cache_control": {"type": "ephemeral", "ttl": "1h"},
        }
    ],
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "<large_document>...</large_document>",
                    "cache_control": {"type": "ephemeral"},  # 5m default
                },
                {"type": "text", "text": "Summarize this document."},
            ],
        }
    ],
)
```

## TTL Options

### 5-Minute Cache (Default)

- Write cost: 1.25x base input price
- Pays off after 1 cache read
- Best for: interactive sessions, rapid iteration

### 1-Hour Cache

- Write cost: 2x base input price
- Pays off after 2 cache reads
- Best for: batch processing, long-running workflows

```python
# 1-hour TTL for batch workloads
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "Large shared context for batch processing...",
            "cache_control": {"type": "ephemeral", "ttl": "1h"},
        }
    ],
    messages=[{"role": "user", "content": "Process item 1"}],
)
```

## Cache Behavior

### What Can Be Cached

- System prompts
- Tool definitions
- User messages (text, images, documents)
- Assistant messages in conversation history

### What Cannot Be Cached

- The final user message (always processed fresh)
- Content after the last cache breakpoint

### What Invalidates the Cache

- Any change to content before the cache breakpoint
- Different model
- Different API key/organization

### Tracking Cache Performance

```python
usage = message.usage
print(f"Input tokens: {usage.input_tokens}")
print(f"Cache write: {usage.cache_creation_input_tokens}")
print(f"Cache read: {usage.cache_read_input_tokens}")
# cache_read > 0 means cache hit
```

## Supported Models

All current Claude models support prompt caching (both automatic and explicit): Opus 4.6, Opus 4.5, Opus 4.1, Opus 4, Sonnet 4.6, Sonnet 4.5, Sonnet 4, Haiku 4.5, Haiku 3.5, Haiku 3.

## Gotchas and Quirks

- Cache scope is the full prefix: tools + system + messages in that order
- Automatic caching applies to the last cacheable block only
- Explicit breakpoints can be combined with automatic caching
- Pricing multipliers stack with batch discount, long context, and data residency
- Use 1h TTL with Message Batches API (5m may expire before batch processes)
- Thinking blocks from previous turns can be cached but have specific ordering rules
- Cache is refreshed on each hit at no additional cost
- Minimum cacheable prefix size varies by model

## Related Endpoints

- `_INFO_ANTAPI-IN06_MESSAGES.md [ANTAPI-IN06]` - Messages API (cache_control parameter)
- `_INFO_ANTAPI-IN10_BATCHES.md [ANTAPI-IN10]` - Batches with caching (use 1h TTL)
- `_INFO_ANTAPI-IN12_PRICING.md [ANTAPI-IN12]` - Caching pricing multipliers

## Sources

- ANTAPI-SC-ANTH-CACHE - https://platform.claude.com/docs/en/build-with-claude/prompt-caching - Full caching guide

## Document History

**[2026-03-20 03:28]**
- Initial documentation created from prompt caching guide
