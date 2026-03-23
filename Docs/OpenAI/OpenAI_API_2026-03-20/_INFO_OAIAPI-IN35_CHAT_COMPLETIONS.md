# Chat Completions API (Legacy)

**Doc ID**: OAIAPI-IN35
**Goal**: Document Chat Completions API for backward compatibility with existing integrations
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references
- `_INFO_OAIAPI-IN06_RESPONSES_API.md [OAIAPI-IN06]` for migration context

## Summary

Chat Completions API (POST /v1/chat/completions) is the legacy interface for text generation, maintained for backward compatibility. Recommended: migrate to Responses API for new projects. Supports messages array with roles (system, user, assistant), streaming via SSE, function calling, and structured outputs via response_format. Parameters: model, messages, temperature, max_tokens, top_p, n (generate multiple), stop sequences, presence_penalty, frequency_penalty. Returns choices array with message and finish_reason. Streaming returns chunks with delta. No built-in tools (web_search, file_search, code_interpreter) - Responses API exclusive. Function calling available but Responses API preferred. Still receives model updates and bug fixes. Use for existing integrations not yet migrated. New features added to Responses API only. [VERIFIED] (OAIAPI-SC-OAI-CHTCRT, OAIAPI-SC-OAI-GMIGRR)

## Key Facts

- **Status**: Legacy, maintained for compatibility [VERIFIED] (OAIAPI-SC-OAI-GMIGRR)
- **Endpoint**: POST /v1/chat/completions [VERIFIED] (OAIAPI-SC-OAI-CHTCRT)
- **Recommended**: Migrate to Responses API [VERIFIED] (OAIAPI-SC-OAI-GMIGRR)
- **Limitations**: No built-in tools [VERIFIED] (OAIAPI-SC-OAI-RESOVW)
- **Support**: Bug fixes only, no new features [VERIFIED] (OAIAPI-SC-OAI-GMIGRR)

## Use Cases

- **Legacy integrations**: Existing code not yet migrated
- **Backward compatibility**: Maintain existing applications
- **Transition period**: Gradual migration to Responses API

## Quick Reference

```python
POST /v1/chat/completions
{
  "model": "gpt-4o",
  "messages": [
    {"role": "system", "content": "You are helpful"},
    {"role": "user", "content": "Hello"}
  ]
}
```

## Request Parameters

**Required:**
- **model**: Model ID
- **messages**: Array of message objects

**Optional:**
- **temperature**: 0-2 (default: 1)
- **max_tokens**: Max completion tokens
- **top_p**: 0-1 (default: 1)
- **n**: Number of completions (1-10)
- **stream**: Boolean for streaming
- **stop**: Stop sequences
- **presence_penalty**: -2 to 2
- **frequency_penalty**: -2 to 2
- **logit_bias**: Token biases
- **user**: End-user identifier
- **response_format**: Output format
- **tools**: Function definitions
- **tool_choice**: Tool selection

## Response Format

```json
{
  "id": "chatcmpl_abc123",
  "object": "chat.completion",
  "created": 1234567890,
  "model": "gpt-4o",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Hello! How can I help?"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 5,
    "total_tokens": 15
  }
}
```

## SDK Examples (Python)

### Basic Usage

```python
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is AI?"}
    ]
)

print(response.choices[0].message.content)
```

### Streaming

```python
from openai import OpenAI

client = OpenAI()

stream = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Tell a story"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

### Migration to Responses API

```python
from openai import OpenAI

client = OpenAI()

# OLD: Chat Completions
response_old = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}]
)
content_old = response_old.choices[0].message.content

# NEW: Responses API
response_new = client.responses.create(
    model="gpt-5.4",
    input=[{"role": "user", "content": "Hello"}]
)
content_new = response_new.output[0].content[0].text
```

## Differences from Responses API

- **messages** → **input**: Parameter name
- **choices[0].message** → **output[0]**: Response structure
- **No built-in tools**: web_search, file_search unavailable
- **No conversations**: No persistent state management
- **No background mode**: No long-running tasks
- **Legacy focus**: Maintenance only

## Error Responses

Same as Responses API:
- **400 Bad Request**
- **401 Unauthorized**
- **429 Too Many Requests**
- **500 Internal Server Error**

## Sources

- OAIAPI-SC-OAI-CHTCRT - POST Create chat completion
- OAIAPI-SC-OAI-GMIGRR - Migration guide

## Document History

**[2026-03-20 16:22]**
- Initial documentation created
