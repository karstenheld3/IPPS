# Streaming Messages

**Doc ID**: ANTAPI-IN07
**Goal**: Document SSE streaming interface, event types, delta handling, and error recovery
**API version**: anthropic-version 2023-06-01

**Depends on:**
- `_INFO_ANTAPI-IN06_MESSAGES.md [ANTAPI-IN06]` for Messages API request/response schema

## Summary

The Messages API supports real-time streaming via Server-Sent Events (SSE) by setting `stream: true`. The stream follows a structured event flow: `message_start` -> content blocks (each with `content_block_start`, deltas, `content_block_stop`) -> `message_delta` -> `message_stop`. Delta types include `text_delta`, `input_json_delta` (for tool use), `thinking_delta` (for extended thinking), and `signature_delta`. The Python SDK provides `client.messages.stream()` as a context manager with `text_stream` iterator and `get_final_message()` for convenience.

## Key Facts

- **Parameter**: `stream: true` on POST /v1/messages
- **Protocol**: Server-Sent Events (SSE)
- **SDK Method**: `client.messages.stream()` (context manager)
- **Final Message**: `stream.get_final_message()` (Python), `.finalMessage()` (TypeScript)
- **Text Iterator**: `stream.text_stream`
- **Delta Types**: text_delta, input_json_delta, thinking_delta, signature_delta, citations_delta
- **Status**: GA

## Event Flow

1. `message_start` - Contains Message object with empty content
2. For each content block:
   - `content_block_start` - Block type and index
   - `content_block_delta` (one or more) - Incremental content
   - `content_block_stop` - Block complete
3. `message_delta` - Top-level changes (stop_reason, usage). Usage counts are cumulative
4. `message_stop` - Stream complete

Additional events:
- `ping` - Keep-alive events dispersed throughout
- `error` - Error during streaming (e.g., `overloaded_error`)

## Delta Types

### Text Delta

```
event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "text_delta", "text": "ello frien"}}
```

### Input JSON Delta (Tool Use)

Deltas are partial JSON strings. Accumulate them and parse on `content_block_stop`. Current models emit one complete key-value at a time, so there may be delays between events.

```
event: content_block_delta
data: {"type": "content_block_delta", "index": 1, "delta": {"type": "input_json_delta", "partial_json": "{\"location\": \"San Fra"}}
```

### Thinking Delta (Extended Thinking)

```
event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "thinking_delta", "thinking": "I need to find the GCD..."}}
```

A `signature_delta` is sent just before `content_block_stop` for thinking blocks to verify integrity.

```
event: content_block_delta
data: {"type": "content_block_delta", "index": 0, "delta": {"type": "signature_delta", "signature": "EqQBCgIYAhIM..."}}
```

When `display: "omitted"` is set on thinking config, no `thinking_delta` events are sent; only `signature_delta` before close.

## Python Examples

### Basic Streaming

```python
import anthropic

client = anthropic.Anthropic()

with client.messages.stream(
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}],
    model="claude-sonnet-4-20250514",
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

### Get Final Message (No Event Handling)

```python
import anthropic

client = anthropic.Anthropic()

with client.messages.stream(
    max_tokens=128000,
    messages=[{"role": "user", "content": "Write a detailed analysis..."}],
    model="claude-sonnet-4-20250514",
) as stream:
    message = stream.get_final_message()

# message is identical to what .create() returns
print(message.content[0].text)
print(f"Tokens used: {message.usage.output_tokens}")
```

### Async Streaming

```python
import anthropic
import asyncio

async def main():
    client = anthropic.AsyncAnthropic()

    async with client.messages.stream(
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello"}],
        model="claude-sonnet-4-20250514",
    ) as stream:
        async for text in stream.text_stream:
            print(text, end="", flush=True)

asyncio.run(main())
```

### Raw HTTP Streaming

```python
import anthropic
import json

client = anthropic.Anthropic()

# Using raw create with stream=True
with client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}],
    stream=True,
) as response:
    for event in response:
        if event.type == "content_block_delta":
            if event.delta.type == "text_delta":
                print(event.delta.text, end="", flush=True)
        elif event.type == "message_delta":
            print(f"\nStop reason: {event.delta.stop_reason}")
```

## Error Recovery

### Streaming Errors

Errors during streaming arrive as `error` events after the initial 200 response. Standard HTTP error handling does not apply once streaming has started.

```
event: error
data: {"type": "error", "error": {"type": "overloaded_error", "message": "Overloaded"}}
```

### Best Practices

- Always handle unknown event types gracefully (new types may be added per versioning policy)
- Use SDK streaming helpers rather than raw SSE parsing when possible
- For long-running requests, streaming avoids HTTP timeout issues
- SDKs set TCP keep-alive and validate against 10-minute timeouts for non-streaming requests
- Token counts in `message_delta` usage are cumulative, not incremental

## Gotchas and Quirks

- `stream: true` in the request body enables streaming; the SDK `.stream()` method handles this automatically
- Tool use input arrives as partial JSON strings (`input_json_delta`); do not parse until `content_block_stop`
- There may be delays between `content_block_delta` events during tool use while the model generates key-value pairs
- Errors during streaming come as SSE events, not HTTP status codes
- `ping` events are interspersed for keep-alive; ignore them in processing logic
- `get_final_message()` accumulates all stream events internally and returns a complete Message object

## Related Endpoints

- `_INFO_ANTAPI-IN06_MESSAGES.md [ANTAPI-IN06]` - Messages API reference
- `_INFO_ANTAPI-IN09_STOP_REASONS.md [ANTAPI-IN09]` - Stop reason handling
- `_INFO_ANTAPI-IN13_EXTENDED_THINKING.md [ANTAPI-IN13]` - Thinking delta details
- `_INFO_ANTAPI-IN27_TOOL_STREAMING.md [ANTAPI-IN27]` - Fine-grained tool streaming

## Sources

- ANTAPI-SC-ANTH-STREAM - https://platform.claude.com/docs/en/build-with-claude/streaming - Full streaming guide, events, deltas, recovery

## Document History

**[2026-03-20 02:35]**
- Initial documentation created from streaming guide
