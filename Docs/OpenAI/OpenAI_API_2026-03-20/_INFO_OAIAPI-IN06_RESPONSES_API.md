# Responses API

**Doc ID**: OAIAPI-IN06
**Goal**: Document Responses API - OpenAI's advanced interface for generating model responses with stateful interactions
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references

## Summary

The Responses API (POST /v1/responses) is OpenAI's most advanced interface for text generation, supporting text and image inputs with text outputs. It enables stateful interactions using previous response outputs as input, extends model capabilities with built-in tools (file_search, web_search, code_interpreter, tool_search, computer use), and provides function calling for external system integration. Key features: conversation state management, background mode for long-running tasks, streaming via SSE, reasoning effort control, structured outputs with JSON schema, and response lifecycle operations (retrieve, delete, cancel, compact). The API replaces Chat Completions as the primary interface, offering unified access to tools, conversation persistence, and advanced capabilities. Supports GPT-5.x, o-series reasoning models, and multimodal inputs. Rate limited by project tier. [VERIFIED] (OAIAPI-SC-OAI-RESOVW, OAIAPI-SC-OAI-RESCRT)

## Key Facts

- **Endpoint**: POST /v1/responses [VERIFIED] (OAIAPI-SC-OAI-RESCRT)
- **Status**: Primary interface (replaces Chat Completions) [VERIFIED] (OAIAPI-SC-OAI-RESOVW)
- **Built-in tools**: file_search, web_search, code_interpreter, tool_search, computer use [VERIFIED] (OAIAPI-SC-OAI-RESOVW)
- **Stateful**: Supports conversation persistence via Conversations API [VERIFIED] (OAIAPI-SC-OAI-RESOVW)
- **Background mode**: Long-running tasks with deferred completion [VERIFIED] (OAIAPI-SC-OAI-RESCRT)
- **Streaming**: SSE streaming with response.delta and response.done events [VERIFIED] (OAIAPI-SC-OAI-RESSTR)

## Use Cases

- **Conversational AI**: Multi-turn conversations with state persistence
- **RAG applications**: File search with vector stores
- **Web-enabled chat**: Real-time web search integration
- **Code execution**: Running Python code via code_interpreter
- **Research tasks**: Deep research with o3-deep-research model
- **External integrations**: Function calling to APIs and databases

## Quick Reference

```python
POST /v1/responses

{
  "model": "gpt-5.4",
  "input": [
    {"role": "user", "content": "Hello"}
  ],
  "tools": [
    {"type": "web_search"},
    {"type": "function", "function": {...}}
  ],
  "stream": false
}
```

## Request Schema

### Required Parameters

- **model**: Model ID (gpt-5.4, gpt-5.4-mini, o4-mini, etc.)
- **input**: Array of input items (messages)

### Optional Parameters

- **conversation_id**: Link to existing conversation for state persistence
- **tools**: Array of tool definitions (built-in or functions)
- **tool_choice**: Control tool usage (auto, required, none, specific tool)
- **text**: Text generation settings
  - **format**: Response format (json_schema, json_object, text)
  - **max_output_tokens**: Maximum tokens to generate
- **reasoning**: Reasoning settings
  - **effort**: Reasoning effort level (low, medium, high, xhigh)
  - **include_summaries**: Include reasoning summaries in response
- **background**: Background mode settings
  - **enabled**: Run task in background
- **metadata**: Custom metadata (key-value pairs)
- **stream**: Enable streaming (boolean)
- **temperature**: Sampling temperature (0-2)
- **top_p**: Nucleus sampling parameter
- **frequency_penalty**: Frequency penalty (-2 to 2)
- **presence_penalty**: Presence penalty (-2 to 2)
- **stop**: Stop sequences (array of strings)
- **user**: End-user identifier for abuse monitoring

## Response Schema

### Response Object

```json
{
  "id": "resp_abc123",
  "object": "response",
  "created": 1234567890,
  "model": "gpt-5.4",
  "status": "completed",
  "output": [
    {
      "id": "item_xyz",
      "type": "message",
      "role": "assistant",
      "content": [
        {
          "type": "text",
          "text": "Hello! How can I help you?"
        }
      ]
    }
  ],
  "usage": {
    "input_tokens": 10,
    "output_tokens": 25,
    "total_tokens": 35
  }
}
```

### Status Values

- **in_progress**: Response generation ongoing
- **completed**: Response fully generated
- **failed**: Generation failed
- **cancelled**: Response cancelled by user

## Built-in Tools

### file_search

Search uploaded files in vector stores:
```json
{
  "type": "file_search",
  "file_search": {
    "vector_store_ids": ["vs_abc123"],
    "max_num_results": 20
  }
}
```

### web_search

Real-time web search:
```json
{
  "type": "web_search",
  "web_search": {
    "max_results": 10
  }
}
```

### code_interpreter

Execute Python code in sandbox:
```json
{
  "type": "code_interpreter"
}
```

### tool_search

Discover and use skills:
```json
{
  "type": "tool_search"
}
```

### computer use

Interact with computer interfaces:
```json
{
  "type": "computer_use"
}
```

## Function Calling

Define custom functions:
```json
{
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "Get current weather",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {"type": "string"}
          },
          "required": ["location"]
        }
      }
    }
  ]
}
```

## Conversation State

Link responses to conversations:
```json
{
  "conversation_id": "conv_abc123",
  "input": [...]
}
```

Conversation maintains history and context across multiple response calls.

## Background Mode

For long-running tasks:
```json
{
  "background": {
    "enabled": true
  }
}
```

Response returns immediately with `in_progress` status. Poll or use webhooks for completion.

## Structured Outputs

Force JSON schema response:
```json
{
  "text": {
    "format": {
      "type": "json_schema",
      "json_schema": {
        "name": "response",
        "schema": {
          "type": "object",
          "properties": {
            "answer": {"type": "string"}
          },
          "required": ["answer"]
        },
        "strict": true
      }
    }
  }
}
```

## Response Operations

### Create Response

```
POST /v1/responses
```

### Retrieve Response

```
GET /v1/responses/{response_id}
```

### Delete Response

```
DELETE /v1/responses/{response_id}
```

### Cancel Response

```
POST /v1/responses/{response_id}/cancel
```

Cancel in-progress or background response.

### Compact Response

```
POST /v1/responses/{response_id}/compact
```

Compact conversation context to reduce token usage.

## SDK Examples (Python)

### Basic Response

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-5.4",
    input=[
        {"role": "user", "content": "What is the capital of France?"}
    ]
)

print(response.output[0].content[0].text)
```

### With Tools

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-5.4",
    input=[
        {"role": "user", "content": "Search the web for latest AI news"}
    ],
    tools=[
        {"type": "web_search"}
    ]
)

print(response.output[0].content[0].text)
```

### With Conversation

```python
from openai import OpenAI

client = OpenAI()

# Create conversation
conversation = client.conversations.create()

# First response
response1 = client.responses.create(
    model="gpt-5.4",
    conversation_id=conversation.id,
    input=[
        {"role": "user", "content": "Remember my name is Alice"}
    ]
)

# Second response (with memory)
response2 = client.responses.create(
    model="gpt-5.4",
    conversation_id=conversation.id,
    input=[
        {"role": "user", "content": "What's my name?"}
    ]
)

print(response2.output[0].content[0].text)  # "Your name is Alice"
```

### Background Mode

```python
from openai import OpenAI
import time

client = OpenAI()

# Start background task
response = client.responses.create(
    model="o3-deep-research",
    input=[
        {"role": "user", "content": "Research quantum computing trends"}
    ],
    background={"enabled": True}
)

print(f"Response ID: {response.id}, Status: {response.status}")

# Poll for completion
while response.status == "in_progress":
    time.sleep(5)
    response = client.responses.retrieve(response.id)
    print(f"Status: {response.status}")

print(response.output[0].content[0].text)
```

### Structured Output

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-5.4",
    input=[
        {"role": "user", "content": "Extract name and age: John is 30 years old"}
    ],
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

import json
result = json.loads(response.output[0].content[0].text)
print(result)  # {"name": "John", "age": 30}
```

## Error Responses

- **400 Bad Request** - Invalid parameters, malformed input
- **401 Unauthorized** - Invalid API key
- **404 Not Found** - Response ID not found
- **429 Too Many Requests** - Rate limit exceeded
- **500 Internal Server Error** - Server error, retry

## Rate Limiting / Throttling

- **Project-scoped limits**: RPM/TPM per project
- **Model-specific**: Different limits per model
- **Tool usage counted**: Tool calls count toward token limits

## Differences from Other APIs

- **vs Chat Completions**: Responses API is newer, supports more features (built-in tools, conversation state, background mode)
- **vs Anthropic Messages**: Similar concept, but OpenAI has more built-in tools
- **vs Gemini generateContent**: Responses API has conversation persistence, Gemini uses stateless requests

## Limitations and Known Issues

- **Background mode timeout**: 24-hour maximum for background tasks [VERIFIED] (OAIAPI-SC-OAI-GBKGND)
- **Tool limits**: Max number of tools per request varies by model [COMMUNITY] (OAIAPI-SC-SO-TOOLLIM)
- **Conversation storage**: Limited retention period for conversation data [VERIFIED] (OAIAPI-SC-OAI-CNVCRT)

## Gotchas and Quirks

- **Input vs messages**: Uses `input` parameter, not `messages` (Chat Completions uses `messages`) [VERIFIED] (OAIAPI-SC-OAI-RESCRT)
- **Tool choice required**: If tools provided without tool_choice, model may not use them [COMMUNITY] (OAIAPI-SC-SO-TOOLCH)
- **Status polling interval**: Recommended 1-5 second intervals for background tasks [VERIFIED] (OAIAPI-SC-OAI-GBKGND)

## Sources

- OAIAPI-SC-OAI-RESOVW - Responses API Overview
- OAIAPI-SC-OAI-RESCRT - POST Create a response
- OAIAPI-SC-OAI-RESGET - GET Retrieve a response
- OAIAPI-SC-OAI-RESDEL - DELETE Delete a response
- OAIAPI-SC-OAI-RESCAN - POST Cancel a response
- OAIAPI-SC-OAI-RESCMP - POST Compact a response

## Document History

**[2026-03-20 15:05]**
- Initial documentation created from Responses API reference
