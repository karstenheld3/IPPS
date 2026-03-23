# Responses Streaming

**Doc ID**: OAIAPI-IN07
**Goal**: Document SSE streaming for Responses API with event types and stream handling
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references
- `_INFO_OAIAPI-IN06_RESPONSES_API.md [OAIAPI-IN06]` for Responses API overview

## Summary

Responses API supports Server-Sent Events (SSE) streaming by setting `stream: true` in request. Streaming returns incremental updates via events: response.delta (partial content chunks), response.done (completion marker), response.failed (error indicator), and tool-specific events for function calls and tool use. Each event includes event type and JSON data payload. Streaming enables real-time UI updates, progressive content display, and early response cancellation. Events arrive as `data:` lines with event type in `event:` field. Client must handle partial state accumulation - delta events contain incremental changes, not full content. Streaming reduces perceived latency and improves user experience for long responses. Compatible with all Responses API features including tools, structured outputs, and reasoning. [VERIFIED] (OAIAPI-SC-OAI-RESSTR)

## Key Facts

- **Protocol**: Server-Sent Events (SSE) [VERIFIED] (OAIAPI-SC-OAI-RESSTR)
- **Enable**: Set `stream: true` in request [VERIFIED] (OAIAPI-SC-OAI-RESCRT)
- **Event types**: response.delta, response.done, response.failed, tool events [VERIFIED] (OAIAPI-SC-OAI-RESSTR)
- **Format**: `event: type\ndata: {json}\n\n` [VERIFIED] (OAIAPI-SC-OAI-RESSTR)
- **Accumulation**: Client accumulates deltas for full response [VERIFIED] (OAIAPI-SC-OAI-RESSTR)

## Use Cases

- **Real-time chat**: Display response as it generates
- **Progress indication**: Show typing indicators during generation
- **Early cancellation**: Cancel long responses before completion
- **Streaming UI**: Update interface progressively

## Quick Reference

```python
# Enable streaming
response = client.responses.create(
    model="gpt-5.4",
    input=[{"role": "user", "content": "Tell a story"}],
    stream=True
)

# Process events
for event in response:
    if event.type == "response.delta":
        print(event.delta.content[0].text, end="", flush=True)
    elif event.type == "response.done":
        print("\n[Complete]")
```

## Event Types

### response.delta

Incremental content update:
```json
{
  "event": "response.delta",
  "data": {
    "id": "resp_abc123",
    "delta": {
      "output": [
        {
          "index": 0,
          "content": [
            {
              "type": "text",
              "text": "Hello"
            }
          ]
        }
      ]
    }
  }
}
```

**Fields:**
- **index**: Output item index
- **content**: Array of content deltas
- **text**: Incremental text chunk

### response.done

Stream completion marker:
```json
{
  "event": "response.done",
  "data": {
    "id": "resp_abc123",
    "status": "completed",
    "usage": {
      "input_tokens": 10,
      "output_tokens": 50,
      "total_tokens": 60
    }
  }
}
```

**Indicates:** Response fully generated, no more deltas

### response.failed

Error during streaming:
```json
{
  "event": "response.failed",
  "data": {
    "id": "resp_abc123",
    "status": "failed",
    "error": {
      "type": "api_error",
      "message": "Internal server error"
    }
  }
}
```

### tool_calls.delta

Tool call incremental update:
```json
{
  "event": "tool_calls.delta",
  "data": {
    "index": 0,
    "id": "call_abc",
    "type": "function",
    "function": {
      "name": "get_weather",
      "arguments": "{\"location\":"
    }
  }
}
```

### tool_calls.done

Tool call completion:
```json
{
  "event": "tool_calls.done",
  "data": {
    "index": 0,
    "id": "call_abc",
    "type": "function",
    "function": {
      "name": "get_weather",
      "arguments": "{\"location\":\"Paris\"}"
    }
  }
}
```

## Event Processing

### State Accumulation

Client must accumulate deltas:
1. Initialize empty response state
2. Process each delta event, merging into state
3. Display accumulated content progressively
4. Finalize on response.done

### Event Order

Events arrive in sequence:
1. Multiple response.delta events
2. Optional tool_calls.delta/done events
3. Final response.done or response.failed event

## SDK Examples (Python)

### Basic Streaming (API docs pattern)

```python
from openai import OpenAI

client = OpenAI()

stream = client.responses.create(
    model="gpt-5.4",
    input=[
        {"role": "user", "content": "Write a short poem"}
    ],
    stream=True
)

for event in stream:
    if event.type == "response.delta":
        chunk = event.delta.output[0].content[0].text
        print(chunk, end="", flush=True)
    elif event.type == "response.done":
        print("\n")
```

### Basic Streaming (SDK v2.29.0 verified)

```python
# Source: openai v2.29.0 - resources/responses/responses.py
# SDK provides responses.stream() as convenience method (returns ResponseStreamManager)
# responses.create(stream=True) also works but stream() is preferred
from openai import OpenAI

client = OpenAI()

# Preferred: use responses.stream() context manager
with client.responses.stream(
    model="gpt-5.4",
    input=[
        {"role": "user", "content": "Write a short poem"}
    ]
) as stream:
    for event in stream:
        if event.type == "response.text_delta":
            print(event.delta, end="", flush=True)

# Alternative: get final text after streaming
with client.responses.stream(
    model="gpt-5.4",
    input=[{"role": "user", "content": "Write a short poem"}]
) as stream:
    response = stream.get_final_response()
    print(response.output[0].content[0].text)
```

### Streaming with Error Handling

```python
from openai import OpenAI

client = OpenAI()

try:
    stream = client.responses.create(
        model="gpt-5.4",
        input=[{"role": "user", "content": "Explain AI"}],
        stream=True
    )
    
    full_text = ""
    for event in stream:
        if event.type == "response.delta":
            chunk = event.delta.output[0].content[0].text
            full_text += chunk
            print(chunk, end="", flush=True)
        
        elif event.type == "response.done":
            print(f"\n\nTokens used: {event.usage.total_tokens}")
        
        elif event.type == "response.failed":
            print(f"\nError: {event.error.message}")
            break

except Exception as e:
    print(f"Stream error: {e}")
```

### Streaming with Tools

```python
from openai import OpenAI
import json

client = OpenAI()

stream = client.responses.create(
    model="gpt-5.4",
    input=[
        {"role": "user", "content": "What's the weather in Paris?"}
    ],
    tools=[
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get weather for location",
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
    stream=True
)

tool_calls = {}
for event in stream:
    if event.type == "tool_calls.delta":
        idx = event.index
        if idx not in tool_calls:
            tool_calls[idx] = {"function": {"arguments": ""}}
        
        tool_calls[idx]["id"] = event.id
        tool_calls[idx]["type"] = event.type
        tool_calls[idx]["function"]["name"] = event.function.name
        tool_calls[idx]["function"]["arguments"] += event.function.arguments
    
    elif event.type == "tool_calls.done":
        print(f"Tool call: {event.function.name}")
        print(f"Arguments: {event.function.arguments}")
    
    elif event.type == "response.delta":
        if event.delta.output[0].content:
            print(event.delta.output[0].content[0].text, end="", flush=True)
    
    elif event.type == "response.done":
        print(f"\n\nCompleted: {event.status}")
```

### Production Streaming Handler

```python
from openai import OpenAI
from typing import Iterator
import logging

logger = logging.getLogger(__name__)

def stream_response(prompt: str) -> Iterator[str]:
    client = OpenAI()
    
    try:
        stream = client.responses.create(
            model="gpt-5.4",
            input=[{"role": "user", "content": prompt}],
            stream=True
        )
        
        for event in stream:
            if event.type == "response.delta":
                chunk = event.delta.output[0].content[0].text
                yield chunk
            
            elif event.type == "response.done":
                logger.info(f"Stream completed: {event.usage.total_tokens} tokens")
                return
            
            elif event.type == "response.failed":
                logger.error(f"Stream failed: {event.error.message}")
                raise Exception(f"Stream error: {event.error.message}")
    
    except Exception as e:
        logger.error(f"Streaming error: {e}")
        raise

# Usage
for chunk in stream_response("Explain quantum computing"):
    print(chunk, end="", flush=True)
print()
```

## Error Responses

- **Stream interruption**: Network issues cause incomplete streams
- **Server errors**: response.failed event with error details
- **Timeout**: Long pauses may indicate issues

## Rate Limiting / Throttling

- **Streaming counts toward limits**: Each stream uses RPM/TPM quota
- **Token counting**: All generated tokens count, even if stream cancelled early

## Differences from Other APIs

- **vs Chat Completions streaming**: Similar SSE format, different event names (response.delta vs chat.completion.chunk)
- **vs Anthropic streaming**: Anthropic uses message_delta, OpenAI uses response.delta
- **vs Gemini streaming**: Gemini uses different event structure

## Limitations and Known Issues

- **No pause/resume**: Cannot pause stream and resume later [VERIFIED] (OAIAPI-SC-OAI-RESSTR)
- **Buffering delays**: Some proxies/CDNs may buffer events [COMMUNITY] (OAIAPI-SC-SO-SSEBUF)
- **Connection timeout**: Long streams may timeout on slow connections [COMMUNITY] (OAIAPI-SC-SO-TIMEOUT)

## Gotchas and Quirks

- **Delta accumulation required**: Deltas are incremental, not complete [VERIFIED] (OAIAPI-SC-OAI-RESSTR)
- **Event field optional**: Not all events have delta field [VERIFIED] (OAIAPI-SC-OAI-RESSTR)
- **Flush required**: Must flush stdout for real-time display [COMMUNITY] (OAIAPI-SC-SO-FLUSH)

## Sources

- OAIAPI-SC-OAI-RESSTR - Streaming events reference
- OAIAPI-SC-OAI-RESCRT - POST Create a response

## Document History

**[2026-03-20 16:41]**
- Added: SDK v2.29.0 verified streaming example using `responses.stream()` context manager
- Added: Note that `create(stream=True)` also works but `responses.stream()` is preferred SDK pattern

**[2026-03-20 15:10]**
- Initial documentation created
