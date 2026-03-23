# Completions API (Legacy)

**Doc ID**: OAIAPI-IN59
**Goal**: Document the legacy Completions API - single-prompt text completion (deprecated)
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references

## Summary

The legacy Completions API (POST /v1/completions) generates text completions for a single prompt string. Unlike Chat Completions which uses a messages array with roles, the Completions API takes a flat `prompt` string and returns a completion. Supported only by `gpt-3.5-turbo-instruct` and older models - not supported by GPT-4+ or reasoning models. The API is **deprecated** in favor of Chat Completions and the Responses API. Returns a `text_completion` object with choices array (each with `text`, `finish_reason`, `logprobs`). Supports streaming, temperature, top_p, max_tokens, stop sequences, n (multiple completions), logprobs, echo, suffix, best_of, frequency_penalty, presence_penalty, and logit_bias. The `suffix` parameter enables fill-in-the-middle completion. The `echo` parameter returns the prompt concatenated with the completion. [VERIFIED] (OAIAPI-SC-OAI-CMPLT)

## Key Facts

- **Status**: DEPRECATED - use Chat Completions or Responses API instead [VERIFIED] (OAIAPI-SC-OAI-CMPLT)
- **Endpoint**: POST /v1/completions [VERIFIED] (OAIAPI-SC-OAI-CMPLT)
- **Models**: gpt-3.5-turbo-instruct only (GPT-4+ not supported) [VERIFIED] (OAIAPI-SC-OAI-CMPLT)
- **Input**: Single `prompt` string (not messages array) [VERIFIED] (OAIAPI-SC-OAI-CMPLT)
- **Unique features**: `suffix` (fill-in-middle), `echo`, `best_of` [VERIFIED] (OAIAPI-SC-OAI-CMPLT)

## Quick Reference

```
POST /v1/completions

{
  "model": "gpt-3.5-turbo-instruct",
  "prompt": "Write a tagline for an ice cream shop: ",
  "max_tokens": 50,
  "temperature": 0.7
}
```

## Response Object

```json
{
  "id": "cmpl-abc123",
  "object": "text_completion",
  "created": 1699061776,
  "model": "gpt-3.5-turbo-instruct",
  "choices": [
    {
      "text": "Every scoop tells a story!",
      "index": 0,
      "logprobs": null,
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 7,
    "total_tokens": 17
  }
}
```

## SDK Examples (Python)

### Basic Usage

```python
from openai import OpenAI

client = OpenAI()

response = client.completions.create(
    model="gpt-3.5-turbo-instruct",
    prompt="Translate to French: Hello, how are you?",
    max_tokens=50
)

print(response.choices[0].text)
```

## Migration

Replace with Chat Completions:

```python
# Before (Completions)
response = client.completions.create(
    model="gpt-3.5-turbo-instruct",
    prompt="Summarize: The cat sat on the mat."
)

# After (Chat Completions)
response = client.chat.completions.create(
    model="gpt-5.4",
    messages=[{"role": "user", "content": "Summarize: The cat sat on the mat."}]
)
```

## Differences from Other APIs

- **vs Chat Completions**: Completions uses flat prompt; Chat uses messages array with roles
- **vs Anthropic**: Anthropic never had a flat-prompt completions endpoint
- **vs Gemini**: Gemini generateContent always uses structured content format

## Sources

- OAIAPI-SC-OAI-CMPLT - Legacy Completions API Reference

## Document History

**[2026-03-20 18:28]**
- Initial documentation created
