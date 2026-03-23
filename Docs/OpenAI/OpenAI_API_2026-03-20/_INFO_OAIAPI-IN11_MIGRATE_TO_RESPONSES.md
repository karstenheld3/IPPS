# Migration Guide: Chat Completions to Responses API

**Doc ID**: OAIAPI-IN11
**Goal**: Document migration from Chat Completions API to Responses API with parameter mapping and code examples
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references
- `_INFO_OAIAPI-IN06_RESPONSES_API.md [OAIAPI-IN06]` for Responses API details

## Summary

Responses API is the recommended primary interface, replacing Chat Completions for new applications. Key migration changes: `messages` becomes `input`, `response_format` becomes `text.format`, function calling uses same structure, streaming uses different event names (response.delta vs chat.completion.chunk), and new features include built-in tools (web_search, file_search, code_interpreter), conversation state management, background mode, and compact operation. Most Chat Completions parameters have direct equivalents in Responses API. Breaking changes: structured outputs schema structure different, no `n` parameter (generate multiple responses), tool_choice syntax slightly modified. Migration benefits: access to built-in tools, conversation persistence, background processing, unified API for all capabilities. Both APIs maintained for compatibility but new features only in Responses API. [VERIFIED] (OAIAPI-SC-OAI-GMIGRR)

## Key Facts

- **Recommended**: Responses API is primary interface going forward [VERIFIED] (OAIAPI-SC-OAI-GMIGRR)
- **Parameter mapping**: Most parameters have direct equivalents [VERIFIED] (OAIAPI-SC-OAI-GMIGRR)
- **Breaking changes**: Structured outputs, n parameter, streaming events [VERIFIED] (OAIAPI-SC-OAI-GMIGRR)
- **New features**: Built-in tools, conversations, background mode [VERIFIED] (OAIAPI-SC-OAI-RESOVW)
- **Compatibility**: Chat Completions still supported for existing apps [VERIFIED] (OAIAPI-SC-OAI-CHTCRT)

## Use Cases

- **New applications**: Use Responses API from start
- **Existing apps**: Gradual migration with parameter mapping
- **Tool integration**: Migrate to leverage built-in tools
- **Stateful apps**: Migrate to use conversation persistence

## Quick Reference

### Chat Completions (Old)
```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "Hello"}
    ]
)
```

### Responses API (New)
```python
response = client.responses.create(
    model="gpt-5.4",
    input=[
        {"role": "user", "content": "Hello"}
    ]
)
```

## Parameter Mapping

### Request Parameters

| Chat Completions | Responses API | Notes |
|-----------------|---------------|-------|
| `messages` | `input` | Array of input items |
| `model` | `model` | Same format |
| `temperature` | `temperature` | Same (0-2) |
| `top_p` | `top_p` | Same (0-1) |
| `n` | **REMOVED** | Generate multiple responses not supported |
| `stream` | `stream` | Same boolean |
| `stop` | `stop` | Same array of strings |
| `max_tokens` | `text.max_output_tokens` | Nested in text object |
| `presence_penalty` | `presence_penalty` | Same (-2 to 2) |
| `frequency_penalty` | `frequency_penalty` | Same (-2 to 2) |
| `logit_bias` | **NOT YET** | Not in Responses API |
| `user` | `user` | Same (end-user ID) |
| `response_format` | `text.format` | Different structure |
| `tools` | `tools` | Same structure, plus built-ins |
| `tool_choice` | `tool_choice` | Slightly modified syntax |

### Response Parameters

| Chat Completions | Responses API | Notes |
|-----------------|---------------|-------|
| `choices[0].message` | `output[0]` | Different structure |
| `choices[0].finish_reason` | `status` | Different values |
| `usage` | `usage` | Same structure |
| `id` | `id` | Same format |

## Code Migration Examples

### Basic Request Migration

**Before (Chat Completions):**
```python
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are helpful"},
        {"role": "user", "content": "What is AI?"}
    ],
    temperature=0.7,
    max_tokens=500
)

print(response.choices[0].message.content)
```

**After (Responses API):**
```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-5.4",
    input=[
        {"role": "system", "content": "You are helpful"},
        {"role": "user", "content": "What is AI?"}
    ],
    temperature=0.7,
    text={"max_output_tokens": 500}
)

print(response.output[0].content[0].text)
```

### Function Calling Migration

**Before (Chat Completions):**
```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "What's the weather in Paris?"}],
    tools=[
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get weather",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string"}
                    },
                    "required": ["location"]
                }
            }
        }
    ],
    tool_choice="auto"
)
```

**After (Responses API):**
```python
response = client.responses.create(
    model="gpt-5.4",
    input=[{"role": "user", "content": "What's the weather in Paris?"}],
    tools=[
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get weather",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string"}
                    },
                    "required": ["location"]
                }
            }
        }
    ],
    tool_choice="auto"
)
```

### Structured Outputs Migration

**Before (Chat Completions):**
```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Extract: John is 30"}],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "person",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "integer"}
                },
                "required": ["name", "age"]
            }
        }
    }
)
```

**After (Responses API):**
```python
response = client.responses.create(
    model="gpt-5.4",
    input=[{"role": "user", "content": "Extract: John is 30"}],
    text={
        "format": {
            "type": "json_schema",
            "json_schema": {
                "name": "person",
                "schema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "age": {"type": "integer"}
                    },
                    "required": ["name", "age"]
                },
                "strict": True
            }
        }
    }
)
```

### Streaming Migration

**Before (Chat Completions):**
```python
stream = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Tell a story"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

**After (Responses API - API docs pattern):**
```python
stream = client.responses.create(
    model="gpt-5.4",
    input=[{"role": "user", "content": "Tell a story"}],
    stream=True
)

for event in stream:
    if event.type == "response.delta":
        print(event.delta.output[0].content[0].text, end="", flush=True)
```

**After (Responses API - SDK v2.29.0 verified):**
```python
# Source: openai v2.29.0 - resources/responses/responses.py
# SDK provides responses.stream() convenience method (preferred over stream=True)
with client.responses.stream(
    model="gpt-5.4",
    input=[{"role": "user", "content": "Tell a story"}]
) as stream:
    for event in stream:
        if event.type == "response.text_delta":
            print(event.delta, end="", flush=True)
```

## New Capabilities in Responses API

### Built-in Tools

```python
# Web search (not available in Chat Completions)
response = client.responses.create(
    model="gpt-5.4",
    input=[{"role": "user", "content": "Latest AI news"}],
    tools=[{"type": "web_search"}]
)
```

### Conversation State

```python
# Persistent conversations (not available in Chat Completions)
conversation = client.conversations.create()

response1 = client.responses.create(
    model="gpt-5.4",
    conversation_id=conversation.id,
    input=[{"role": "user", "content": "My name is Alice"}]
)

response2 = client.responses.create(
    model="gpt-5.4",
    conversation_id=conversation.id,
    input=[{"role": "user", "content": "What's my name?"}]
)
```

### Conversation State (SDK v2.29.0 verified)

```python
# Source: openai v2.29.0 - resources/responses/responses.py
# SDK uses conversation={"id": "..."} not conversation_id="..."
conversation = client.conversations.create()

response1 = client.responses.create(
    model="gpt-4.1",
    conversation={"id": conversation.id},
    input=[{"role": "user", "content": "My name is Alice"}]
)

response2 = client.responses.create(
    model="gpt-4.1",
    conversation={"id": conversation.id},
    input=[{"role": "user", "content": "What's my name?"}]
)
```

### Background Mode

```python
# Long-running tasks (not available in Chat Completions)
response = client.responses.create(
    model="o3-deep-research",
    input=[{"role": "user", "content": "Research AI trends"}],
    background={"enabled": True}
)

# Poll for completion
while response.status == "in_progress":
    response = client.responses.retrieve(response.id)
```

## Breaking Changes

### 1. No `n` Parameter

Chat Completions supported generating multiple responses:
```python
# NOT SUPPORTED in Responses API
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[...],
    n=3  # Generate 3 responses
)
```

**Workaround:** Make multiple API calls

### 2. Structured Outputs Schema

Different nesting for json_schema:
- Chat: `response_format.json_schema.schema`
- Responses: `text.format.json_schema.schema`

### 3. Streaming Event Names

Different event types:
- Chat: `chat.completion.chunk`
- Responses: `response.delta`

### 4. Response Access

Different paths to content:
- Chat: `choices[0].message.content`
- Responses: `output[0].content[0].text`

## Migration Strategy

### Gradual Migration

1. **Identify dependencies**: Check Chat Completions-specific code
2. **Update imports**: No changes needed (same OpenAI client)
3. **Map parameters**: Use parameter mapping table
4. **Test thoroughly**: Verify output format changes
5. **Monitor costs**: Different models may have different pricing

### Parallel Running

Run both APIs temporarily:
```python
def generate_response(prompt, use_new_api=False):
    if use_new_api:
        return client.responses.create(
            model="gpt-5.4",
            input=[{"role": "user", "content": prompt}]
        )
    else:
        return client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
```

## Error Responses

Migration-specific errors:
- **400 Bad Request** - Invalid parameter mapping
- **404 Not Found** - Model not available in Responses API

## Differences from Other APIs

- **vs Anthropic Messages**: Anthropic has no Chat Completions equivalent, only Messages (similar to Responses)
- **vs Gemini**: Gemini uses generateContent (similar pattern to Responses)

## Limitations and Known Issues

- **No logit_bias**: Not yet supported in Responses API [VERIFIED] (OAIAPI-SC-OAI-GMIGRR)
- **No n parameter**: Cannot generate multiple responses in one call [VERIFIED] (OAIAPI-SC-OAI-GMIGRR)
- **Model availability**: Some legacy models only in Chat Completions [COMMUNITY] (OAIAPI-SC-SO-MODAVAIL)

## Gotchas and Quirks

- **Input vs messages**: Most common migration error [VERIFIED] (OAIAPI-SC-OAI-GMIGRR)
- **Nested text settings**: max_tokens nested in text object [VERIFIED] (OAIAPI-SC-OAI-RESCRT)
- **Output array access**: Always array even for single response [VERIFIED] (OAIAPI-SC-OAI-RESCRT)

## Sources

- OAIAPI-SC-OAI-GMIGRR - Migration guide from Chat Completions to Responses
- OAIAPI-SC-OAI-RESCRT - POST Create a response
- OAIAPI-SC-OAI-CHTCRT - POST Create chat completion

## Document History

**[2026-03-21 09:22]**
- Added: SDK v2.29.0 verified companion for Conversation State (conversation= param)

**[2026-03-20 16:41]**
- Added: SDK v2.29.0 verified streaming migration example using `responses.stream()`

**[2026-03-20 15:16]**
- Initial documentation created
