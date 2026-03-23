# Streaming API Responses

**Doc ID**: OAIAPI-IN56
**Goal**: Document SSE streaming for Chat Completions and Responses API - event format, delta handling, usage reporting
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references
- `_INFO_OAIAPI-IN55_CHAT_COMPLETIONS.md [OAIAPI-IN55]` for Chat Completions context

## Summary

Streaming delivers model output incrementally via Server-Sent Events (SSE). Enable with `stream: true` in the request. Chat Completions streams `chat.completion.chunk` objects with delta content. Responses API streams typed events (`response.created`, `response.output_text.delta`, `response.completed`, etc.) designed for richer streaming. Each SSE message is prefixed with `data: ` followed by JSON. The stream ends with `data: [DONE]` for Chat Completions. Stream options: `stream_options.include_usage: true` adds a final chunk with token usage stats. Delta objects contain incremental content (text fragments, tool call argument fragments). Tool calls stream argument JSON incrementally - accumulate deltas and parse when complete. Streaming reduces time-to-first-token (TTFT) and enables progressive UI updates. Both sync and async streaming supported in SDKs. OpenAI recommends the Responses API for streaming due to its purpose-built event design. [VERIFIED] (OAIAPI-SC-OAI-GSTRM)

## Key Facts

- **Protocol**: Server-Sent Events (SSE) over HTTP [VERIFIED] (OAIAPI-SC-OAI-GSTRM)
- **Enable**: `stream: true` in request body [VERIFIED] (OAIAPI-SC-OAI-GSTRM)
- **Chat Completions chunks**: `chat.completion.chunk` objects with deltas [VERIFIED] (OAIAPI-SC-OAI-GSTRM)
- **Responses events**: Typed events (response.output_text.delta, etc.) [VERIFIED] (OAIAPI-SC-OAI-GSTRM)
- **Usage in stream**: `stream_options: {"include_usage": true}` [VERIFIED] (OAIAPI-SC-OAI-GSTRM)
- **End marker**: `data: [DONE]` for Chat Completions [VERIFIED] (OAIAPI-SC-OAI-GSTRM)
- **Recommendation**: Use Responses API for streaming [VERIFIED] (OAIAPI-SC-OAI-GSTRM)

## Use Cases

- **Chat UIs**: Progressive text display as model generates
- **Low latency**: Reduce perceived latency with early token delivery
- **Long outputs**: Stream large outputs without waiting for completion
- **Tool call monitoring**: Watch tool call arguments build incrementally
- **Real-time processing**: Process output tokens as they arrive

## Quick Reference

```
# Chat Completions streaming
POST /v1/chat/completions
{"model": "gpt-5.4", "messages": [...], "stream": true}

# Responses API streaming
POST /v1/responses
{"model": "gpt-5.4", "input": "...", "stream": true}

SSE format:
  data: {"id":"chatcmpl-xxx","choices":[{"delta":{"content":"Hello"}}]}
  data: {"id":"chatcmpl-xxx","choices":[{"delta":{"content":" world"}}]}
  data: [DONE]
```

## Chat Completions Stream Chunks

### Content Delta

```json
{
  "id": "chatcmpl-abc123",
  "object": "chat.completion.chunk",
  "created": 1741569952,
  "model": "gpt-5.4",
  "choices": [
    {
      "index": 0,
      "delta": {
        "content": "Hello"
      },
      "finish_reason": null
    }
  ]
}
```

### Role Delta (First Chunk)

```json
{
  "choices": [
    {
      "index": 0,
      "delta": {
        "role": "assistant",
        "content": ""
      },
      "finish_reason": null
    }
  ]
}
```

### Tool Call Delta

```json
{
  "choices": [
    {
      "index": 0,
      "delta": {
        "tool_calls": [
          {
            "index": 0,
            "id": "call_abc123",
            "type": "function",
            "function": {
              "name": "get_weather",
              "arguments": "{\"loc"
            }
          }
        ]
      },
      "finish_reason": null
    }
  ]
}
```

### Final Chunk (with Usage)

```json
{
  "choices": [
    {
      "index": 0,
      "delta": {},
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 19,
    "completion_tokens": 10,
    "total_tokens": 29
  }
}
```

## Responses API Stream Events

```
response.created              # Response object created
response.in_progress          # Processing started
response.output_text.delta    # Text fragment
response.output_text.done     # Text output complete
response.content_part.added   # New content part
response.content_part.done    # Content part complete
response.output_item.added    # New output item
response.output_item.done     # Output item complete
response.function_call_arguments.delta  # Function args fragment
response.function_call_arguments.done   # Function args complete
response.completed            # Response fully complete
response.failed               # Response generation failed
response.incomplete           # Response truncated
```

## SDK Examples (Python)

### Basic Streaming (Chat Completions)

```python
from openai import OpenAI

client = OpenAI()

stream = client.chat.completions.create(
    model="gpt-5.4",
    messages=[
        {"role": "developer", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write a short poem about coding."}
    ],
    stream=True,
    stream_options={"include_usage": True}
)

collected_content = []
for chunk in stream:
    if chunk.choices and chunk.choices[0].delta.content:
        text = chunk.choices[0].delta.content
        collected_content.append(text)
        print(text, end="", flush=True)
    
    if hasattr(chunk, 'usage') and chunk.usage:
        print(f"\n[Tokens: {chunk.usage.total_tokens}]")

full_response = "".join(collected_content)
```

### Async Streaming

```python
from openai import AsyncOpenAI
import asyncio

async def stream_response():
    client = AsyncOpenAI()
    
    stream = await client.chat.completions.create(
        model="gpt-5.4",
        messages=[{"role": "user", "content": "Explain quantum computing briefly."}],
        stream=True
    )
    
    async for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
    
    print()

asyncio.run(stream_response())
```

### Streaming with Tool Calls - Production Ready

```python
from openai import OpenAI
import json

client = OpenAI()

def stream_with_tools(messages: list, tools: list, model: str = "gpt-5.4"):
    """Stream a completion and handle tool calls"""
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        stream=True,
        stream_options={"include_usage": True}
    )
    
    content_parts = []
    tool_calls = {}  # index -> {id, name, arguments}
    finish_reason = None
    usage = None
    
    for chunk in stream:
        if not chunk.choices:
            if chunk.usage:
                usage = chunk.usage
            continue
        
        delta = chunk.choices[0].delta
        finish_reason = chunk.choices[0].finish_reason or finish_reason
        
        # Accumulate content
        if delta.content:
            content_parts.append(delta.content)
            print(delta.content, end="", flush=True)
        
        # Accumulate tool call arguments
        if delta.tool_calls:
            for tc in delta.tool_calls:
                idx = tc.index
                if idx not in tool_calls:
                    tool_calls[idx] = {
                        "id": tc.id or tool_calls.get(idx, {}).get("id"),
                        "name": "",
                        "arguments": ""
                    }
                if tc.id:
                    tool_calls[idx]["id"] = tc.id
                if tc.function:
                    if tc.function.name:
                        tool_calls[idx]["name"] = tc.function.name
                    if tc.function.arguments:
                        tool_calls[idx]["arguments"] += tc.function.arguments
    
    if content_parts:
        print()
    
    result = {
        "content": "".join(content_parts),
        "tool_calls": list(tool_calls.values()),
        "finish_reason": finish_reason,
        "usage": usage
    }
    
    # Parse tool call arguments
    for tc in result["tool_calls"]:
        try:
            tc["parsed_args"] = json.loads(tc["arguments"])
        except json.JSONDecodeError:
            tc["parsed_args"] = None
    
    return result

# Example usage
tools = [{
    "type": "function",
    "function": {
        "name": "search",
        "description": "Search for information",
        "parameters": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"]
        }
    }
}]

try:
    result = stream_with_tools(
        messages=[{"role": "user", "content": "Search for Python tutorials"}],
        tools=tools
    )
    
    if result["tool_calls"]:
        for tc in result["tool_calls"]:
            print(f"Tool: {tc['name']}({tc['parsed_args']})")
    
    if result["usage"]:
        print(f"Tokens: {result['usage'].total_tokens}")

except Exception as e:
    print(f"Error: {e}")
```

### Responses API Streaming

```python
from openai import OpenAI

client = OpenAI()

stream = client.responses.create(
    model="gpt-5.4",
    input="Write a haiku about streaming data.",
    stream=True
)

for event in stream:
    if event.type == "response.output_text.delta":
        print(event.delta, end="", flush=True)
    elif event.type == "response.completed":
        print(f"\n[Done. Tokens: {event.response.usage.total_tokens}]")
```

## Error Responses

- **SSE error events**: Errors during streaming arrive as SSE data chunks
- **Connection drops**: Client must handle reconnection
- **Partial responses**: If stream is interrupted, collected content is all that's available

## Differences from Other APIs

- **vs Anthropic Streaming**: Anthropic uses similar SSE with `content_block_delta` events. Input token count available in `message_start` event
- **vs Gemini Streaming**: Gemini uses `stream=True` with `GenerateContentResponse` chunks. Different event structure
- **vs Grok**: Uses OpenAI-compatible streaming format (same SSE protocol)
- **Chat Completions vs Responses streaming**: Responses API has richer typed events; Chat Completions uses generic delta chunks

## Limitations and Known Issues

- **No retry mid-stream**: If connection drops, must restart entire request [VERIFIED] (OAIAPI-SC-OAI-GSTRM)
- **Usage only at end**: Token counts only in final chunk (with stream_options) [VERIFIED] (OAIAPI-SC-OAI-GSTRM)
- **Tool call fragmentation**: Tool arguments arrive as JSON fragments, not complete objects [VERIFIED] (OAIAPI-SC-OAI-GSTRM)

## Gotchas and Quirks

- **include_usage opt-in**: Must set `stream_options.include_usage: true` to get token counts [VERIFIED] (OAIAPI-SC-OAI-GSTRM)
- **Empty deltas**: Some chunks have empty delta objects (e.g., role-only first chunk) [VERIFIED] (OAIAPI-SC-OAI-GSTRM)
- **finish_reason location**: finish_reason appears in the last chunk with choices [VERIFIED] (OAIAPI-SC-OAI-GSTRM)
- **Tool call index**: Tool calls in stream use `index` field to correlate fragments [VERIFIED] (OAIAPI-SC-OAI-GSTRM)

## Sources

- OAIAPI-SC-OAI-GSTRM - Streaming Responses Guide
- OAIAPI-SC-OAI-CHATC - Chat Completions API Reference

## Document History

**[2026-03-20 18:22]**
- Initial documentation created from guide and API reference
