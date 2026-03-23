# Chat Completions API

**Doc ID**: OAIAPI-IN55
**Goal**: Document the Chat Completions API - create completions, parameters, response format, and usage
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references

**Does not depend on:**
- `_INFO_OAIAPI-IN04_RESPONSES_API.md [OAIAPI-IN04]` (Responses API is separate, newer endpoint)

## Summary

The Chat Completions API (POST /v1/chat/completions) is the widely-adopted endpoint for text generation. It accepts a list of messages (conversation history) and returns a model-generated completion. Message roles: `developer` (instructions, replaces `system` for o1+ models), `system` (legacy instructions), `user` (end-user input), `assistant` (model responses), `tool` (tool call results), `function` (deprecated). Content types: text, images (vision), audio (input/output), files. Supports function/tool calling, structured outputs (JSON schema), streaming (SSE), logprobs, seed for reproducibility, and response format control. Returns a chat.completion object with choices array, usage stats (prompt_tokens, completion_tokens with detailed breakdowns for cached, audio, reasoning tokens), and service_tier. Finish reasons: `stop`, `length`, `tool_calls`, `content_filter`, `function_call` (deprecated). OpenAI recommends the Responses API for new projects but Chat Completions remains fully supported. [VERIFIED] (OAIAPI-SC-OAI-CHATC)

## Key Facts

- **Endpoint**: POST /v1/chat/completions [VERIFIED] (OAIAPI-SC-OAI-CHATC)
- **Message roles**: developer, system, user, assistant, tool, function [VERIFIED] (OAIAPI-SC-OAI-CHATC)
- **Content modalities**: Text, images, audio, files [VERIFIED] (OAIAPI-SC-OAI-CHATC)
- **Structured outputs**: JSON schema via `response_format` [VERIFIED] (OAIAPI-SC-OAI-CHATC)
- **Tool calling**: Function tools with JSON arguments [VERIFIED] (OAIAPI-SC-OAI-CHATC)
- **Streaming**: SSE via `stream: true` [VERIFIED] (OAIAPI-SC-OAI-CHATC)
- **Token details**: Cached, audio, reasoning, prediction token breakdowns [VERIFIED] (OAIAPI-SC-OAI-CHATC)
- **Recommendation**: Use Responses API for new projects [VERIFIED] (OAIAPI-SC-OAI-CHATC)

## Use Cases

- **Chatbots**: Multi-turn conversational AI
- **Text generation**: Content creation, summarization, translation
- **Function calling**: Integration with external tools and APIs
- **Structured extraction**: Parse data into JSON schemas
- **Vision**: Analyze images with text prompts
- **Audio**: Speech-in, speech-out conversations

## Quick Reference

```
POST /v1/chat/completions

Headers:
  Authorization: Bearer $OPENAI_API_KEY
  Content-Type: application/json

Required parameters:
  model     # Model ID (gpt-5.4, o3, etc.)
  messages  # Array of message objects
```

## Request Parameters

### Required

- **model** (string): Model ID (e.g., "gpt-5.4", "o3", "gpt-4.1")
- **messages** (array): Conversation messages

### Common Optional

- **temperature** (float): 0-2, default 1. Lower = more focused
- **top_p** (float): 0-1, default 1. Nucleus sampling
- **max_tokens** (integer): Maximum completion tokens (deprecated, use max_completion_tokens)
- **max_completion_tokens** (integer): Maximum tokens in completion
- **n** (integer): Number of completions to generate (default 1)
- **stream** (boolean): Enable SSE streaming
- **stop** (string/array): Stop sequences
- **seed** (integer): Deterministic sampling seed
- **store** (boolean): Store completion for later retrieval (default true for new accounts)

### Tools and Functions

- **tools** (array): Tool definitions (function type)
- **tool_choice** (string/object): "auto", "none", "required", or specific function
- **parallel_tool_calls** (boolean): Allow multiple simultaneous tool calls (default true)

### Output Format

- **response_format** (object): Control output format
  - `{"type": "text"}` - Default text output
  - `{"type": "json_object"}` - JSON mode
  - `{"type": "json_schema", "json_schema": {...}}` - Structured outputs with schema

### Audio

- **modalities** (array): ["text"] or ["text", "audio"]
- **audio** (object): Audio output config (voice, format) when modalities includes "audio"

### Advanced

- **frequency_penalty** (float): -2.0 to 2.0
- **presence_penalty** (float): -2.0 to 2.0
- **logprobs** (boolean): Return log probabilities
- **top_logprobs** (integer): 0-20, number of top logprobs per token
- **logit_bias** (object): Modify token probabilities
- **service_tier** (string): "auto" or "default" (flex processing)
- **user** (string): End-user ID for abuse monitoring
- **prediction** (object): Predicted output for faster completions

## Response Object

```json
{
  "id": "chatcmpl-B9MBs8CjcvOU2jLn4n570S5qMJKcT",
  "object": "chat.completion",
  "created": 1741569952,
  "model": "gpt-5.4",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Hello! How can I assist you today?",
        "refusal": null,
        "annotations": []
      },
      "logprobs": null,
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 19,
    "completion_tokens": 10,
    "total_tokens": 29,
    "prompt_tokens_details": {
      "cached_tokens": 0,
      "audio_tokens": 0
    },
    "completion_tokens_details": {
      "reasoning_tokens": 0,
      "audio_tokens": 0,
      "accepted_prediction_tokens": 0,
      "rejected_prediction_tokens": 0
    }
  },
  "service_tier": "default"
}
```

### Finish Reasons

- **stop**: Natural completion or stop sequence hit
- **length**: max_tokens / max_completion_tokens reached
- **tool_calls**: Model wants to call tool(s)
- **content_filter**: Content filtered by safety system
- **function_call**: Deprecated, use tool_calls

## SDK Examples (Python)

### Basic Completion

```python
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-5.4",
    messages=[
        {"role": "developer", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"}
    ]
)

print(response.choices[0].message.content)
print(f"Tokens: {response.usage.total_tokens}")
```

### Tool Calling

```python
from openai import OpenAI
import json

client = OpenAI()

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "City name"},
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
                },
                "required": ["location"]
            }
        }
    }
]

response = client.chat.completions.create(
    model="gpt-5.4",
    messages=[{"role": "user", "content": "What's the weather in Tokyo?"}],
    tools=tools,
    tool_choice="auto"
)

message = response.choices[0].message

if message.tool_calls:
    for call in message.tool_calls:
        args = json.loads(call.function.arguments)
        print(f"Call {call.function.name}: {args}")
        
        # Execute function, then continue conversation
        result = {"temperature": 22, "condition": "cloudy"}
        
        followup = client.chat.completions.create(
            model="gpt-5.4",
            messages=[
                {"role": "user", "content": "What's the weather in Tokyo?"},
                message,
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": json.dumps(result)
                }
            ],
            tools=tools
        )
        print(followup.choices[0].message.content)
```

### Structured Outputs

```python
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-5.4",
    messages=[
        {"role": "user", "content": "Extract: John Smith, age 30, works at Acme Corp"}
    ],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "person",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "integer"},
                    "company": {"type": "string"}
                },
                "required": ["name", "age", "company"],
                "additionalProperties": False
            }
        }
    }
)

import json
person = json.loads(response.choices[0].message.content)
print(person)  # {"name": "John Smith", "age": 30, "company": "Acme Corp"}
```

### Production Multi-Turn Chat

```python
from openai import OpenAI

client = OpenAI()

def chat_loop(system_prompt: str, model: str = "gpt-5.4"):
    """Interactive multi-turn chat with error handling"""
    messages = [{"role": "developer", "content": system_prompt}]
    
    while True:
        user_input = input("You: ").strip()
        if not user_input or user_input.lower() in ("quit", "exit"):
            break
        
        messages.append({"role": "user", "content": user_input})
        
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                max_completion_tokens=1000
            )
            
            choice = response.choices[0]
            assistant_msg = choice.message.content
            
            if choice.finish_reason == "content_filter":
                print("Assistant: [Content filtered]")
                continue
            
            if choice.message.refusal:
                print(f"Assistant: [Refused: {choice.message.refusal}]")
                continue
            
            messages.append({"role": "assistant", "content": assistant_msg})
            print(f"Assistant: {assistant_msg}")
            
            cached = response.usage.prompt_tokens_details.cached_tokens
            print(f"  [{response.usage.total_tokens} tokens, {cached} cached]")
        
        except Exception as e:
            print(f"Error: {e}")

chat_loop("You are a concise, helpful assistant.")
```

## Error Responses

- **400 Bad Request** - Invalid parameters, malformed messages
- **401 Unauthorized** - Invalid API key
- **404 Not Found** - Model not found
- **422 Unprocessable Entity** - Invalid schema for structured outputs
- **429 Too Many Requests** - Rate limit exceeded
- **500 Internal Server Error** - Server error

## Rate Limiting / Throttling

- **Per-model limits**: RPM (requests per minute) and TPM (tokens per minute)
- **Organization tier**: Higher tiers get higher limits
- **Headers**: `x-ratelimit-limit-*`, `x-ratelimit-remaining-*`, `x-ratelimit-reset-*`

## Differences from Other APIs

- **vs Responses API**: Chat Completions uses messages array; Responses uses simpler input string/array. Responses supports built-in tools (file_search, code_interpreter). Chat Completions is more widely adopted in existing codebases
- **vs Anthropic Messages**: Very similar API shape. Anthropic uses `system` param (not in messages), `max_tokens` is required, content is always an array
- **vs Gemini generateContent**: Different structure - uses `contents` array with `parts`. No explicit tool_calls in response; uses `functionCall` in parts
- **vs Grok**: Uses OpenAI-compatible Chat Completions format (same API shape, different base_url)

## Limitations and Known Issues

- **Context window**: Model-dependent (128K for GPT-4.1, 200K for o3) [VERIFIED] (OAIAPI-SC-OAI-CHATC)
- **developer vs system**: o1+ models use `developer` role; older models use `system` [VERIFIED] (OAIAPI-SC-OAI-CHATC)
- **Reasoning models**: Some parameters unsupported (temperature, top_p, etc.) [VERIFIED] (OAIAPI-SC-OAI-CHATC)
- **Deprecated**: `function_call` replaced by `tool_calls` [VERIFIED] (OAIAPI-SC-OAI-CHATC)

## Gotchas and Quirks

- **max_tokens vs max_completion_tokens**: Use max_completion_tokens; max_tokens is deprecated [VERIFIED] (OAIAPI-SC-OAI-CHATC)
- **Tool call JSON**: Model may generate invalid JSON in tool call arguments; always validate [VERIFIED] (OAIAPI-SC-OAI-CHATC)
- **Cached tokens**: prompt_tokens_details.cached_tokens shows automatic prompt caching savings [VERIFIED] (OAIAPI-SC-OAI-CHATC)
- **Store default**: New accounts default to store=true; existing accounts may differ [VERIFIED] (OAIAPI-SC-OAI-CHATC)
- **Annotations**: Response may include annotations (citations) in message [VERIFIED] (OAIAPI-SC-OAI-CHATC)

## Sources

- OAIAPI-SC-OAI-CHATC - Chat Completions API Reference

## Document History

**[2026-03-20 18:20]**
- Initial documentation created from API reference
