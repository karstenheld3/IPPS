# Flex Processing

**Doc ID**: OAIAPI-IN72
**Goal**: Document Flex Processing - discounted latency-insensitive API processing via service_tier parameter
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references

## Summary

Flex Processing provides a 50% discount on token pricing for latency-insensitive workloads. Enabled by setting `service_tier: "flex"` in the request. Flex runs through the standard Responses API and Chat Completions API (not a separate batch endpoint), making it more flexible than the Batch API. Requests are processed when capacity is available, resulting in variable and potentially higher latency. Flex is compatible with prompt caching, providing additional cost savings on top of the 50% base discount. Unlike the Batch API which requires file upload and polling, Flex uses the same synchronous/streaming request flow as standard API calls. Ideal for background processing, data pipelines, bulk analysis, and any workload where response time is not critical. The response includes `service_tier: "flex"` confirming flex pricing was applied. Available for most text generation models. [VERIFIED] (OAIAPI-SC-OAI-GFLEX)

## Key Facts

- **Discount**: 50% on token pricing [VERIFIED] (OAIAPI-SC-OAI-GFLEX)
- **Parameter**: `service_tier: "flex"` [VERIFIED] (OAIAPI-SC-OAI-GFLEX)
- **APIs**: Responses API and Chat Completions API [VERIFIED] (OAIAPI-SC-OAI-GFLEX)
- **Latency**: Variable, higher than default tier [VERIFIED] (OAIAPI-SC-OAI-GFLEX)
- **Caching compatible**: Stacks with prompt caching discount [VERIFIED] (OAIAPI-SC-OAI-GFLEX)
- **Same API flow**: Synchronous/streaming, not batch file upload [VERIFIED] (OAIAPI-SC-OAI-GFLEX)

## Use Cases

- **Data pipelines**: Bulk processing of documents, logs, or records
- **Content generation**: Generating large volumes of content offline
- **Analysis**: Batch analysis of datasets
- **Migration**: Processing historical data through new models
- **Testing**: Running large test suites against model outputs
- **Evaluation**: Bulk evaluation of model performance

## Quick Reference

```python
# Chat Completions
response = client.chat.completions.create(
    model="gpt-5.4",
    messages=[...],
    service_tier="flex"
)

# Responses API
response = client.responses.create(
    model="gpt-5.4",
    input="...",
    service_tier="flex"
)
```

## SDK Examples (Python)

### Basic Flex Processing

```python
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-5.4",
    messages=[
        {"role": "developer", "content": "Summarize the following text concisely."},
        {"role": "user", "content": "Long text to summarize..."}
    ],
    service_tier="flex"
)

print(f"Service tier: {response.service_tier}")  # "flex"
print(response.choices[0].message.content)
```

### Bulk Processing - Production Ready

```python
from openai import OpenAI
import asyncio
from openai import AsyncOpenAI

async def process_batch_flex(items: list, system_prompt: str, model: str = "gpt-5.4"):
    """Process multiple items with flex pricing"""
    client = AsyncOpenAI()
    results = []
    
    sem = asyncio.Semaphore(10)  # Limit concurrency
    
    async def process_one(item):
        async with sem:
            try:
                response = await client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "developer", "content": system_prompt},
                        {"role": "user", "content": item}
                    ],
                    service_tier="flex",
                    max_completion_tokens=500
                )
                return {
                    "input": item[:50],
                    "output": response.choices[0].message.content,
                    "tokens": response.usage.total_tokens,
                    "tier": response.service_tier
                }
            except Exception as e:
                return {"input": item[:50], "error": str(e)}
    
    tasks = [process_one(item) for item in items]
    results = await asyncio.gather(*tasks)
    
    success = sum(1 for r in results if "output" in r)
    total_tokens = sum(r.get("tokens", 0) for r in results)
    
    print(f"Processed: {success}/{len(items)}")
    print(f"Total tokens: {total_tokens}")
    
    return results

# Usage
items = ["Summarize: " + doc for doc in documents]
results = asyncio.run(process_batch_flex(
    items,
    system_prompt="Create a one-paragraph summary."
))
```

## Flex vs Batch API Comparison

- **Flex Processing**
  - Same API call flow (sync/stream)
  - 50% discount
  - Variable latency
  - Compatible with streaming
  - No file upload/polling
  - Stacks with prompt caching

- **Batch API**
  - File upload -> poll -> download results
  - 50% discount
  - Up to 24h completion window
  - No streaming
  - Requires JSONL file management
  - Separate rate limit pool

## Error Responses

- **400 Bad Request** - Invalid service_tier value
- **429 Too Many Requests** - Flex capacity exhausted

## Differences from Other APIs

- **vs Anthropic**: No equivalent flex/discount tier
- **vs Gemini**: No equivalent discount processing tier
- **vs Grok**: No equivalent
- **vs Batch API**: Same discount but different UX - Flex uses standard API calls

## Limitations and Known Issues

- **No SLA guarantee**: Lower priority than default tier, no completion time guarantee [VERIFIED] (OAIAPI-SC-OAI-GFLEX)
- **Unpredictable latency**: Response time varies with capacity [VERIFIED] (OAIAPI-SC-OAI-GFLEX)
- **Not for real-time**: Not suitable for user-facing interactive applications [VERIFIED] (OAIAPI-SC-OAI-GFLEX)
- **Model availability**: Not all models may support flex tier [ASSUMED]

## Sources

- OAIAPI-SC-OAI-GFLEX - Flex Processing Guide

## Document History

**[2026-03-20 19:58]**
- Added: No SLA guarantee limitation

**[2026-03-20 18:54]**
- Initial documentation created
