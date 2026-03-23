# Prompt Caching

**Doc ID**: OAIAPI-IN71
**Goal**: Document automatic prompt caching - how it works, cost savings, optimization strategies
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references

## Summary

Prompt caching automatically reduces cost and latency for repeated prompt prefixes. OpenAI routes API requests to servers that recently processed the same prompt prefix, enabling cache hits without any code changes. Caching reduces latency by up to 80% and input token costs by up to 90% (model-dependent). Works automatically on all API requests. Cache matches require an exact prefix match - the longest matching prefix from previous requests is cached. Minimum cacheable prefix length is 1,024 tokens. Cache entries are evicted after a period of inactivity (typically 5-10 minutes). Cached token counts are reported in `usage.prompt_tokens_details.cached_tokens`. Caching works across Chat Completions, Responses API, Assistants API, Fine-tuning API, and Batch API. Discount varies by model: typically 50% for most models, up to 90% for some. Tool definitions, system/developer messages, and static context at the start of the messages array benefit most from caching. [VERIFIED] (OAIAPI-SC-OAI-GCACH)

## Key Facts

- **Automatic**: No code changes required [VERIFIED] (OAIAPI-SC-OAI-GCACH)
- **Latency reduction**: Up to 80% [VERIFIED] (OAIAPI-SC-OAI-GCACH)
- **Cost reduction**: Up to 90% on cached input tokens [VERIFIED] (OAIAPI-SC-OAI-GCACH)
- **Minimum prefix**: 1,024 tokens [VERIFIED] (OAIAPI-SC-OAI-GCACH)
- **Match type**: Exact prefix match [VERIFIED] (OAIAPI-SC-OAI-GCACH)
- **Eviction**: After ~5-10 minutes of inactivity [VERIFIED] (OAIAPI-SC-OAI-GCACH)
- **Reporting**: `usage.prompt_tokens_details.cached_tokens` [VERIFIED] (OAIAPI-SC-OAI-GCACH)

## How It Works

1. Request arrives with prompt (messages + tools + system context)
2. OpenAI checks if any server recently processed the same prefix
3. If match found: cached tokens are reused (cheaper, faster)
4. If no match: full processing (tokens cached for future requests)
5. Cached token count reported in response usage

## Optimization Strategies

- **Static content first**: Place system/developer messages, tool definitions, and static context at the start of messages array
- **Dynamic content last**: User messages and variable content at the end
- **Consistent ordering**: Keep tool definitions and instructions in the same order across requests
- **Batch similar requests**: Process related requests close together in time to maintain cache warmth
- **Minimize prefix changes**: Any change in the prefix invalidates the cache from that point forward

### Optimal Message Ordering

```
1. developer/system message (static instructions)     <- cached
2. Tool definitions (static)                           <- cached
3. Long context/documents (static per session)         <- cached
4. Conversation history (growing)                      <- partially cached
5. Current user message (dynamic)                      <- not cached
```

## SDK Examples (Python)

### Monitor Cache Efficiency

```python
from openai import OpenAI

client = OpenAI()

def chat_with_cache_monitoring(messages: list, model: str = "gpt-5.4"):
    """Make a request and report caching efficiency"""
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    
    usage = response.usage
    cached = usage.prompt_tokens_details.cached_tokens
    total_input = usage.prompt_tokens
    cache_rate = (cached / total_input * 100) if total_input > 0 else 0
    
    print(f"Input tokens: {total_input}")
    print(f"Cached tokens: {cached} ({cache_rate:.1f}%)")
    print(f"Output tokens: {usage.completion_tokens}")
    
    return response

# First request - establishes cache
messages = [
    {"role": "developer", "content": "You are a helpful assistant specialized in Python programming. " * 50},  # Long static prompt
    {"role": "user", "content": "What is a decorator?"}
]
r1 = chat_with_cache_monitoring(messages)

# Second request - same prefix, different question
messages[-1] = {"role": "user", "content": "What is a generator?"}
r2 = chat_with_cache_monitoring(messages)  # Should show cached tokens
```

### Maximize Caching in Multi-Turn Chat

```python
from openai import OpenAI

client = OpenAI()

SYSTEM_PROMPT = """You are a senior Python developer and code reviewer.
Always provide code examples. Explain your reasoning step by step.
Follow PEP 8 conventions. Consider edge cases and error handling."""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "run_code",
            "description": "Execute Python code in sandbox",
            "parameters": {
                "type": "object",
                "properties": {"code": {"type": "string"}},
                "required": ["code"]
            }
        }
    }
]

class CacheOptimizedChat:
    """Chat session optimized for prompt caching"""
    
    def __init__(self, system_prompt: str, tools: list = None, model: str = "gpt-5.4"):
        self.model = model
        self.tools = tools or []
        # Static prefix: system + tools (always cached after first request)
        self.messages = [{"role": "developer", "content": system_prompt}]
        self.total_cached = 0
        self.total_input = 0
    
    def send(self, user_message: str) -> str:
        self.messages.append({"role": "user", "content": user_message})
        
        response = client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            tools=self.tools if self.tools else None,
            max_completion_tokens=1000
        )
        
        # Track caching
        cached = response.usage.prompt_tokens_details.cached_tokens
        self.total_cached += cached
        self.total_input += response.usage.prompt_tokens
        
        content = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": content})
        
        return content
    
    def cache_stats(self):
        rate = (self.total_cached / self.total_input * 100) if self.total_input > 0 else 0
        return {
            "total_input_tokens": self.total_input,
            "total_cached_tokens": self.total_cached,
            "cache_hit_rate": f"{rate:.1f}%"
        }

# Usage
chat = CacheOptimizedChat(SYSTEM_PROMPT, TOOLS)
chat.send("How do I implement a binary search tree?")
chat.send("Add a delete method to it.")
chat.send("Now add unit tests.")
print(chat.cache_stats())
```

## Error Responses

No caching-specific errors. Caching is transparent and automatic.

## Differences from Other APIs

- **vs Anthropic**: Anthropic has explicit prompt caching with `cache_control` markers. OpenAI caching is automatic
- **vs Gemini**: Gemini has Context Caching (explicit, TTL-based). Different pricing model
- **vs Grok**: No documented prompt caching

## Limitations and Known Issues

- **Minimum 1,024 tokens**: Short prompts below threshold are never cached [VERIFIED] (OAIAPI-SC-OAI-GCACH)
- **Exact prefix match**: Any change in prefix invalidates cache [VERIFIED] (OAIAPI-SC-OAI-GCACH)
- **Eviction**: Cache entries expire after inactivity [VERIFIED] (OAIAPI-SC-OAI-GCACH)
- **No explicit control**: Cannot force cache or set TTL (unlike Anthropic/Gemini) [VERIFIED] (OAIAPI-SC-OAI-GCACH)

## Sources

- OAIAPI-SC-OAI-GCACH - Prompt Caching Guide

## Document History

**[2026-03-20 18:52]**
- Initial documentation created
