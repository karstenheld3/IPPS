# Handling Stop Reasons

**Doc ID**: ANTAPI-IN09
**Goal**: Document all stop reason values, their meanings, and handling patterns
**API version**: anthropic-version 2023-06-01

**Depends on:**
- `_INFO_ANTAPI-IN06_MESSAGES.md [ANTAPI-IN06]` for Messages API response schema

## Summary

The `stop_reason` field in every successful Messages API response indicates why Claude stopped generating. Unlike errors (failed requests), stop reasons describe successful completion states. There are 6 stop reason values: `end_turn`, `max_tokens`, `stop_sequence`, `tool_use`, `pause_turn`, and `refusal`, plus a newer `model_context_window_exceeded`. Each requires different handling in application code.

## Key Facts

- **Field**: `stop_reason` in response body
- **Always Present**: Non-null in non-streaming; null in streaming `message_start`, non-null after
- **Companion Field**: `stop_sequence` (non-null only when stop_reason is "stop_sequence")
- **Status**: GA

## Stop Reason Values

### end_turn

Claude reached a natural stopping point. The response is complete.

```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=1024,
    messages=[{"role": "user", "content": "What is 2+2?"}],
)

if response.stop_reason == "end_turn":
    print(response.content[0].text)  # Complete response
```

**Gotcha**: If response content is empty with `end_turn`, do not add text blocks immediately after `tool_result` messages. Send tool results directly without additional user text.

### max_tokens

Claude hit the `max_tokens` limit. Response is truncated.

```python
response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=10,
    messages=[{"role": "user", "content": "Explain quantum physics"}],
)

if response.stop_reason == "max_tokens":
    print("Response was truncated at token limit")
    # Consider continuing with another request
```

### stop_sequence

Claude generated one of the custom stop sequences specified in the request.

```python
response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=1024,
    stop_sequences=["END", "STOP"],
    messages=[{"role": "user", "content": "Generate text until you say END"}],
)

if response.stop_reason == "stop_sequence":
    print(f"Stopped at sequence: {response.stop_sequence}")
```

### tool_use

Claude invoked one or more tools and expects execution results. Build an agentic loop to handle this.

```python
import anthropic

client = anthropic.Anthropic()

weather_tool = {
    "name": "get_weather",
    "description": "Get the current weather in a given location",
    "input_schema": {
        "type": "object",
        "properties": {
            "location": {"type": "string", "description": "City and state"},
        },
        "required": ["location"],
    },
}

def execute_tool(name, tool_input):
    return f"Weather in {tool_input.get('location', 'unknown')}: 72F"

response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=1024,
    tools=[weather_tool],
    messages=[{"role": "user", "content": "What's the weather?"}],
)

if response.stop_reason == "tool_use":
    for content in response.content:
        if content.type == "tool_use":
            result = execute_tool(content.name, content.input)
            # Send result back to Claude via tool_result block
```

### pause_turn

Server-side sampling loop reached its iteration limit (default: 10) while executing server tools (web search, web fetch, etc.). The response may contain a `server_tool_use` block without a corresponding `server_tool_result`. Send the response back as-is to let Claude continue.

```python
response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=1024,
    tools=[{"type": "web_search_20250305", "name": "web_search"}],
    messages=[{"role": "user", "content": "Search for latest AI news"}],
)

if response.stop_reason == "pause_turn":
    messages = [
        {"role": "user", "content": "Search for latest AI news"},
        {"role": "assistant", "content": response.content},
    ]
    continuation = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=1024,
        messages=messages,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
    )
```

### refusal

Claude declined to respond due to safety concerns (streaming classifiers intervened).

```python
if response.stop_reason == "refusal":
    print("Claude was unable to process this request")
    # Consider rephrasing or modifying the request
```

If encountering frequent refusals with Claude Sonnet 4.5 or Opus 4.1, try Claude Sonnet 4 (`claude-opus-4-7`) which has different usage restrictions.

### model_context_window_exceeded

Claude hit the model's context window limit before reaching `max_tokens`. The response is valid but was limited by context capacity. Available by default in Sonnet 4.5+ models; for earlier models, use beta header `model-context-window-exceeded-2025-08-26`.

```python
response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=64000,
    messages=[{"role": "user", "content": "Large input using most of context window..."}],
)

if response.stop_reason == "model_context_window_exceeded":
    print("Response reached model's context window limit")
    # Response is still valid, just limited by context capacity
```

## Stop Reasons vs Errors

- **Stop reasons** = successful responses (HTTP 200) where Claude completed normally
- **Errors** = failed requests (HTTP 4xx/5xx) where the API could not process the request

## Best Practices

### Always Check stop_reason

```python
import anthropic

client = anthropic.Anthropic()

def handle_response(response):
    match response.stop_reason:
        case "end_turn":
            return response.content[0].text
        case "max_tokens":
            return response.content[0].text + " [TRUNCATED]"
        case "stop_sequence":
            return response.content[0].text
        case "tool_use":
            return handle_tool_use(response)
        case "pause_turn":
            return continue_turn(response)
        case "refusal":
            return "Request declined by safety filters"
        case "model_context_window_exceeded":
            return response.content[0].text + " [CONTEXT LIMIT]"
        case _:
            return f"Unknown stop reason: {response.stop_reason}"
```

### Implement Retry for pause_turn

Any agent loop using server tools should handle `pause_turn` by appending the assistant response and making another request.

### Handle Truncated Responses

When `max_tokens` is hit, either increase the limit or make a continuation request with the partial response.

## Streaming Considerations

- In streaming mode, `stop_reason` is null in the `message_start` event
- `stop_reason` appears in the `message_delta` event
- `tool_use` stop reason during streaming means accumulate `input_json_delta` events until `content_block_stop`

## Gotchas and Quirks

- `end_turn` with empty content after tool results: do not add text blocks alongside `tool_result`
- `pause_turn` only occurs with server-side tools (web_search, web_fetch, etc.), not client tools
- `refusal` frequency varies by model version; Sonnet 4 has different safety filters than Sonnet 4.5
- `model_context_window_exceeded` is a newer stop reason; handle `_` default case for forward compatibility
- The `stop_sequence` field is only non-null when `stop_reason` is `"stop_sequence"`

## Related Endpoints

- `_INFO_ANTAPI-IN06_MESSAGES.md [ANTAPI-IN06]` - Messages API response schema
- `_INFO_ANTAPI-IN07_STREAMING.md [ANTAPI-IN07]` - Streaming event handling
- `_INFO_ANTAPI-IN21_TOOL_USE.md [ANTAPI-IN21]` - Tool use patterns

## Sources

- ANTAPI-SC-ANTH-STOPREASON - https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons - All stop reasons, examples, patterns

## SDK Verification

7 of 8 Python examples verified against `anthropic` SDK 0.104.0. One finding.

**SDK source files checked**:
- `types/stop_reason.py`: `StopReason = Literal['end_turn', 'max_tokens', 'stop_sequence', 'tool_use', 'pause_turn', 'refusal']`
- `types/message.py` (line 16): `Message.stop_reason: Optional[StopReason]`, `Message.stop_sequence: Optional[str]`
- `types/web_search_tool_20250305_param.py`: `WebSearchTool20250305Param(type="web_search_20250305", name="web_search", ...)`
- `types/tool_use_block.py`: `.type`, `.name`, `.input`, `.id` attributes confirmed
- `resources/messages/messages.py`: `stop_sequences` param confirmed as `SequenceNotStr[str]`

**Finding: `model_context_window_exceeded` not in SDK StopReason type**

The SDK 0.104.0 `StopReason` is `Literal['end_turn', 'max_tokens', 'stop_sequence', 'tool_use', 'pause_turn', 'refusal']`. The value `model_context_window_exceeded` is documented in API docs but not yet in the SDK type definition. The match/case example correctly handles this via `case _` default branch, but type checkers will flag direct comparisons.

**SDK-Verified Example** (anthropic 0.104.0, `types/stop_reason.py`):

```python
# model_context_window_exceeded is NOT in SDK StopReason type (0.104.0)
# It may arrive from the API but won't type-check against StopReason.
# Always include a default/else branch for forward compatibility.
if response.stop_reason == "model_context_window_exceeded":
    # Works at runtime but type checkers may warn
    print("Context window limit reached")
```

## Document History

**[2026-05-22]**
- Updated from Anthropic_API_2026-03-20
- Changed: Model references updated to claude-opus-4-7

**[2026-03-20 06:20]**
- Added: SDK verification section (anthropic 0.104.0)
- Added: SDK-verified note that `model_context_window_exceeded` is not in SDK StopReason type

**[2026-03-20 02:42]**
- Initial documentation created with all 7 stop reason values and Python examples
