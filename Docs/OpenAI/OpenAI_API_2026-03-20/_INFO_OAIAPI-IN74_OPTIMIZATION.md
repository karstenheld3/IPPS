# API Optimization

**Doc ID**: OAIAPI-IN74
**Goal**: Document strategies for optimizing API cost, latency, and throughput
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references

## Summary

API optimization covers cost reduction, latency improvement, and throughput maximization. Cost strategies: prompt caching (automatic, up to 90% input discount), flex processing (50% discount for latency-insensitive work), Batch API (50% discount, 24h window), model selection (smaller models for simpler tasks), max_completion_tokens (prevent runaway generation), structured outputs (constrain output size). Latency strategies: streaming (reduce time-to-first-token), prompt caching (up to 80% latency reduction), shorter prompts (fewer tokens = faster), parallel requests (concurrent API calls), predicted outputs (faster edits with prediction parameter), model routing (fast models for simple tasks, powerful models for complex ones). Throughput strategies: Batch API (separate rate limit pool), organization tier upgrades, project-level rate limit configuration, async processing with connection pooling. Token optimization: minimize system/developer prompt length, use references instead of repeating context, leverage conversation chaining via previous_response_id, use embeddings for similarity rather than LLM comparison. [VERIFIED] (OAIAPI-SC-OAI-GBPRD, OAIAPI-SC-OAI-GCACH, OAIAPI-SC-OAI-GFLEX)

## Key Facts

- **Prompt caching**: Up to 90% cost, 80% latency reduction (automatic) [VERIFIED] (OAIAPI-SC-OAI-GCACH)
- **Flex processing**: 50% cost reduction [VERIFIED] (OAIAPI-SC-OAI-GFLEX)
- **Batch API**: 50% cost reduction, separate rate pool [VERIFIED] (OAIAPI-SC-OAI-GBATCH)
- **Model routing**: Use appropriate model size per task [VERIFIED] (OAIAPI-SC-OAI-GBPRD)
- **Streaming**: Reduces perceived latency via TTFT [VERIFIED] (OAIAPI-SC-OAI-GSTRM)
- **Predicted outputs**: Faster for edit-style tasks [VERIFIED] (OAIAPI-SC-OAI-CHATC)

## Cost Optimization Matrix

- **Prompt caching** - Automatic, 50-90% input discount. Best for: repeated prompts, static context
- **Flex processing** - 50% discount, higher latency. Best for: background jobs, pipelines
- **Batch API** - 50% discount, 24h window. Best for: bulk offline processing
- **Smaller models** - Cheaper per token. Best for: classification, extraction, simple tasks
- **max_completion_tokens** - Prevent runaway costs. Best for: all requests
- **Structured outputs** - Constrain output format. Best for: data extraction

## Latency Optimization

### Streaming

```python
from openai import OpenAI

client = OpenAI()

# Streaming reduces time-to-first-token
stream = client.chat.completions.create(
    model="gpt-5.4",
    messages=[{"role": "user", "content": "Explain async/await"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

### Predicted Outputs (Edit Tasks)

```python
from openai import OpenAI

client = OpenAI()

# For code editing: provide predicted output for faster completion
existing_code = """def hello():
    print("hello world")
"""

response = client.chat.completions.create(
    model="gpt-5.4",
    messages=[
        {"role": "user", "content": f"Add type hints to this function:\n{existing_code}"}
    ],
    prediction={
        "type": "content",
        "content": existing_code  # Model uses this as starting point
    }
)

print(response.choices[0].message.content)
# Faster because model confirms/modifies prediction rather than generating from scratch
```

### Parallel Requests

```python
from openai import AsyncOpenAI
import asyncio

async def parallel_completions(prompts: list, model: str = "gpt-5.4"):
    """Process multiple prompts concurrently"""
    client = AsyncOpenAI()
    
    sem = asyncio.Semaphore(20)  # Respect rate limits
    
    async def single(prompt):
        async with sem:
            response = await client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_completion_tokens=200
            )
            return response.choices[0].message.content
    
    return await asyncio.gather(*[single(p) for p in prompts])

results = asyncio.run(parallel_completions([
    "Summarize: topic A",
    "Summarize: topic B",
    "Summarize: topic C"
]))
```

## Model Routing Strategy

```python
from openai import OpenAI

client = OpenAI()

def route_model(task_type: str) -> str:
    """Select optimal model based on task complexity"""
    routing = {
        "classification": "gpt-4.1-nano",    # Fast, cheap
        "extraction": "gpt-4.1-mini",         # Balanced
        "summarization": "gpt-4.1-mini",      # Balanced
        "code_generation": "gpt-4.1",          # Capable
        "reasoning": "o3",                      # Reasoning model
        "research": "o4-mini-deep-research-2025-06-26",  # Deep research
    }
    return routing.get(task_type, "gpt-5.4")

def smart_completion(task_type: str, prompt: str, **kwargs):
    model = route_model(task_type)
    return client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        **kwargs
    )

# Simple classification - use nano model
result = smart_completion("classification", "Is this review positive? 'Great product!'")

# Complex reasoning - use o3
result = smart_completion("reasoning", "Prove that sqrt(2) is irrational.")
```

## Token Optimization Tips

- **Concise system prompts**: Every token counts; trim instructions to essentials
- **Reference, don't repeat**: Use previous_response_id instead of re-sending history
- **Structured context**: Use JSON or bullet points instead of prose for context data
- **Token counting**: Use `tiktoken` library to estimate costs before sending
- **Image detail**: Use `detail: "low"` for images when high detail isn't needed
- **Stop sequences**: Set stop sequences to prevent unnecessary generation

### Token Counting

```python
import tiktoken

def count_tokens(text: str, model: str = "gpt-5.4") -> int:
    """Estimate token count for cost planning"""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))

prompt = "Your prompt text here..."
tokens = count_tokens(prompt)
print(f"Estimated tokens: {tokens}")
```

## Throughput Optimization

- **Batch API**: Separate rate limit pool; use for bulk processing
- **Tier upgrades**: Higher organization tiers = higher RPM/TPM
- **Project rate limits**: Configure per-project limits via admin API
- **Connection pooling**: Reuse HTTP connections (SDK does this automatically)
- **Async clients**: Use AsyncOpenAI for concurrent requests
- **Queue management**: Implement request queue with rate limit awareness

## Cost Comparison (Relative)

```
Standard request:     100% cost, lowest latency
Flex processing:       50% cost, variable latency
Batch API:             50% cost, up to 24h latency
Cached tokens:      10-50% cost, lower latency
Cached + Flex:       5-25% cost, variable latency
```

## Differences from Other APIs

- **vs Anthropic**: Similar optimization patterns. Anthropic has explicit cache_control. No flex tier
- **vs Gemini**: Google has context caching (explicit TTL). Batch prediction API available
- **vs Grok**: Limited optimization options

## Sources

- OAIAPI-SC-OAI-GBPRD - Production Best Practices
- OAIAPI-SC-OAI-GCACH - Prompt Caching Guide
- OAIAPI-SC-OAI-GFLEX - Flex Processing Guide
- OAIAPI-SC-OAI-GBATCH - Batch API Guide

## Document History

**[2026-03-20 18:58]**
- Initial documentation created
