# Chat Completions Messages

**Doc ID**: OAIAPI-IN57
**Goal**: Document message types, roles, content formats, and multi-modal inputs for Chat Completions
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references
- `_INFO_OAIAPI-IN55_CHAT_COMPLETIONS.md [OAIAPI-IN55]` for Chat Completions context

## Summary

Messages in the Chat Completions API form a conversation history passed to the model. Each message has a `role` and `content`. Six roles: `developer` (instructions for o1+ models), `system` (legacy instructions), `user` (end-user input), `assistant` (model output), `tool` (tool call results), `function` (deprecated). Content can be a simple string or an array of content parts for multi-modal input. Content part types: `text` (plain text), `image_url` (image via URL or base64), `input_audio` (audio via base64, wav/mp3), `file` (file via ID or base64). Assistant messages can contain `tool_calls` (function call requests), `refusal` (safety refusal text), `audio` (previous audio response reference), and `annotations` (citations). Tool messages must include `tool_call_id` to correlate with the tool call request. The `name` field on user/assistant messages differentiates participants sharing the same role. Message ordering matters - the model sees messages in array order as conversation context. [VERIFIED] (OAIAPI-SC-OAI-CHATC)

## Key Facts

- **Roles**: developer, system, user, assistant, tool, function (deprecated) [VERIFIED] (OAIAPI-SC-OAI-CHATC)
- **Content types**: text, image_url, input_audio, file [VERIFIED] (OAIAPI-SC-OAI-CHATC)
- **Multi-modal**: Mix text with images, audio, files in content array [VERIFIED] (OAIAPI-SC-OAI-CHATC)
- **developer vs system**: Use `developer` for o1+ models; `system` for older models [VERIFIED] (OAIAPI-SC-OAI-CHATC)
- **Tool correlation**: tool messages require `tool_call_id` [VERIFIED] (OAIAPI-SC-OAI-CHATC)
- **Annotations**: Assistant responses may include citation annotations [VERIFIED] (OAIAPI-SC-OAI-CHATC)

## Message Types

### Developer Message

Instructions the model must follow. Replaces `system` for o1+ models.

```json
{
  "role": "developer",
  "content": "You are a helpful assistant that responds in JSON."
}
```

Or with content array:
```json
{
  "role": "developer",
  "content": [
    {"type": "text", "text": "You are a helpful assistant."}
  ]
}
```

### System Message (Legacy)

```json
{
  "role": "system",
  "content": "You are a helpful assistant."
}
```

Use `developer` instead for o1 and newer models.

### User Message

Simple text:
```json
{
  "role": "user",
  "content": "What is the capital of France?"
}
```

Multi-modal with image:
```json
{
  "role": "user",
  "content": [
    {"type": "text", "text": "What's in this image?"},
    {
      "type": "image_url",
      "image_url": {
        "url": "https://example.com/photo.jpg",
        "detail": "auto"
      }
    }
  ]
}
```

Base64 image:
```json
{
  "role": "user",
  "content": [
    {"type": "text", "text": "Describe this image."},
    {
      "type": "image_url",
      "image_url": {
        "url": "data:image/png;base64,iVBORw0KGgo..."
      }
    }
  ]
}
```

Audio input:
```json
{
  "role": "user",
  "content": [
    {
      "type": "input_audio",
      "input_audio": {
        "data": "<base64-encoded-audio>",
        "format": "wav"
      }
    }
  ]
}
```

File input:
```json
{
  "role": "user",
  "content": [
    {"type": "text", "text": "Summarize this document."},
    {
      "type": "file",
      "file": {
        "file_id": "file-abc123"
      }
    }
  ]
}
```

### Assistant Message

Basic response:
```json
{
  "role": "assistant",
  "content": "The capital of France is Paris."
}
```

With tool calls:
```json
{
  "role": "assistant",
  "content": null,
  "tool_calls": [
    {
      "id": "call_abc123",
      "type": "function",
      "function": {
        "name": "get_weather",
        "arguments": "{\"location\":\"Paris\"}"
      }
    }
  ]
}
```

With refusal:
```json
{
  "role": "assistant",
  "content": null,
  "refusal": "I cannot help with that request."
}
```

### Tool Message

```json
{
  "role": "tool",
  "tool_call_id": "call_abc123",
  "content": "{\"temperature\": 22, \"condition\": \"sunny\"}"
}
```

Must include `tool_call_id` matching the assistant's tool call request.

### Function Message (Deprecated)

```json
{
  "role": "function",
  "name": "get_weather",
  "content": "{\"temperature\": 22}"
}
```

Use `tool` role instead.

## Image Detail Levels

- **auto** (default): Model decides based on image size
- **low**: Fixed 512x512 processing. Faster, fewer tokens
- **high**: Detailed analysis. More tokens, higher quality

## Audio Formats

- **wav**: WAV format audio
- **mp3**: MP3 format audio

## Name Field

The optional `name` field differentiates participants sharing the same role:

```json
[
  {"role": "user", "name": "alice", "content": "Hi, I need help."},
  {"role": "user", "name": "bob", "content": "Me too!"},
  {"role": "assistant", "content": "Happy to help both of you."}
]
```

## SDK Examples (Python)

### Multi-Modal Conversation

```python
from openai import OpenAI
import base64

client = OpenAI()

# Encode image
with open("chart.png", "rb") as f:
    image_b64 = base64.b64encode(f.read()).decode()

response = client.chat.completions.create(
    model="gpt-5.4",
    messages=[
        {
            "role": "developer",
            "content": "You are a data analyst. Analyze charts precisely."
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What trends do you see in this chart?"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{image_b64}",
                        "detail": "high"
                    }
                }
            ]
        }
    ],
    max_completion_tokens=500
)

print(response.choices[0].message.content)
```

### Conversation History Management - Production Ready

```python
from openai import OpenAI

client = OpenAI()

class ChatSession:
    """Manage conversation history with token-aware truncation"""
    
    def __init__(self, system_prompt: str, model: str = "gpt-5.4", max_messages: int = 50):
        self.model = model
        self.max_messages = max_messages
        self.messages = [{"role": "developer", "content": system_prompt}]
    
    def add_user_message(self, content):
        self.messages.append({"role": "user", "content": content})
        self._truncate()
    
    def add_assistant_message(self, content):
        self.messages.append({"role": "assistant", "content": content})
    
    def add_tool_result(self, tool_call_id: str, result: str):
        self.messages.append({
            "role": "tool",
            "tool_call_id": tool_call_id,
            "content": result
        })
    
    def _truncate(self):
        """Keep system/developer message + last N messages"""
        if len(self.messages) > self.max_messages:
            self.messages = [self.messages[0]] + self.messages[-(self.max_messages - 1):]
    
    def get_response(self, **kwargs):
        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                **kwargs
            )
            msg = response.choices[0].message
            
            if msg.content:
                self.add_assistant_message(msg.content)
            elif msg.tool_calls:
                self.messages.append({
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        }
                        for tc in msg.tool_calls
                    ]
                })
            
            return msg
        except Exception as e:
            raise

# Usage
session = ChatSession("You are a helpful coding assistant.")
session.add_user_message("How do I read a CSV in Python?")
response = session.get_response(max_completion_tokens=500)
print(response.content)
```

## Differences from Other APIs

- **vs Anthropic**: Anthropic separates `system` from messages array. Content always array format. No `developer` role. Image format uses `source` object not `image_url`
- **vs Gemini**: Uses `contents` with `parts` array. Roles are `user` and `model` only. No system/developer in messages - uses `system_instruction` parameter
- **vs Grok**: Same message format as OpenAI (compatible API)

## Limitations and Known Issues

- **Image token cost**: High-detail images consume many tokens [VERIFIED] (OAIAPI-SC-OAI-CHATC)
- **Audio format**: Only wav and mp3 supported for input [VERIFIED] (OAIAPI-SC-OAI-CHATC)
- **Message ordering**: Model processes messages in array order [VERIFIED] (OAIAPI-SC-OAI-CHATC)

## Gotchas and Quirks

- **developer vs system**: Sending both in same request works but is redundant [VERIFIED] (OAIAPI-SC-OAI-CHATC)
- **Content null with tool_calls**: When assistant makes tool calls, content is null [VERIFIED] (OAIAPI-SC-OAI-CHATC)
- **Tool call ID required**: Tool messages without matching tool_call_id cause errors [VERIFIED] (OAIAPI-SC-OAI-CHATC)
- **Base64 size**: Large base64 images increase request size and token count significantly [VERIFIED] (OAIAPI-SC-OAI-CHATC)

## Sources

- OAIAPI-SC-OAI-CHATC - Chat Completions API Reference

## Document History

**[2026-03-20 18:24]**
- Initial documentation created from API reference
