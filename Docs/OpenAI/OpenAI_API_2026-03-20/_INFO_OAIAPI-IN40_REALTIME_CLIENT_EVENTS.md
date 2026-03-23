# Realtime Client Events

**Doc ID**: OAIAPI-IN40
**Goal**: Document all client-to-server event types for the Realtime WebSocket API
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references
- `_INFO_OAIAPI-IN39_REALTIME_OVERVIEW.md [OAIAPI-IN39]` for Realtime API architecture

## Summary

Client events are JSON messages sent from the client to the OpenAI Realtime WebSocket server. There are 10 client event types organized into 4 categories: session management (`session.update`), audio input (`input_audio_buffer.append`, `input_audio_buffer.commit`, `input_audio_buffer.clear`), conversation management (`conversation.item.create`, `conversation.item.retrieve`, `conversation.item.truncate`, `conversation.item.delete`), and response control (`response.create`, `response.cancel`, `output_audio_buffer.clear`). All events are JSON objects with a required `type` field and optional `event_id` for client-side tracking. The `session.update` event configures model, voice, modalities, tools, turn detection, and audio formats. Audio is streamed via `input_audio_buffer.append` with base64-encoded audio data. Responses are triggered either automatically by server VAD or manually via `response.create`. The `response.create` event supports inline instructions, conversation override, and output configuration. [VERIFIED] (OAIAPI-SC-OAI-RTCLEV)

## Key Facts

- **Total event types**: 10 client events [VERIFIED] (OAIAPI-SC-OAI-RTCLEV)
- **Format**: JSON with required `type` field [VERIFIED] (OAIAPI-SC-OAI-RTCLEV)
- **event_id**: Optional client-assigned ID for correlation [VERIFIED] (OAIAPI-SC-OAI-RTCLEV)
- **Audio encoding**: Base64-encoded audio in `input_audio_buffer.append` [VERIFIED] (OAIAPI-SC-OAI-RTCLEV)
- **Response trigger**: Automatic (server VAD) or manual (`response.create`) [VERIFIED] (OAIAPI-SC-OAI-RTCLEV)

## Use Cases

- **Voice streaming**: Send microphone audio chunks to server
- **Session configuration**: Set model, voice, tools, and turn detection
- **Conversation management**: Add/remove/truncate conversation items
- **Response control**: Trigger or cancel model responses
- **Interruption handling**: Clear output audio buffer when user interrupts

## Quick Reference

```
Session:
  session.update                  # Configure session parameters

Audio Input:
  input_audio_buffer.append       # Send audio chunk (base64)
  input_audio_buffer.commit       # Commit buffer as user turn
  input_audio_buffer.clear        # Discard buffered audio

Conversation:
  conversation.item.create        # Add item to conversation
  conversation.item.retrieve      # Get item details
  conversation.item.truncate      # Truncate audio content
  conversation.item.delete        # Remove item from conversation

Response:
  response.create                 # Trigger model response
  response.cancel                 # Cancel in-progress response

Output:
  output_audio_buffer.clear       # Clear pending output audio
```

## Event Reference

### session.update

Configure session parameters. Can be sent at any time during the session.

```json
{
  "type": "session.update",
  "session": {
    "model": "gpt-realtime-1.5",
    "voice": "alloy",
    "modalities": ["text", "audio"],
    "instructions": "You are a helpful assistant.",
    "input_audio_format": "pcm16",
    "output_audio_format": "pcm16",
    "input_audio_transcription": {
      "model": "gpt-4o-mini-transcribe"
    },
    "turn_detection": {
      "type": "server_vad",
      "threshold": 0.5,
      "prefix_padding_ms": 300,
      "silence_duration_ms": 500
    },
    "tools": [],
    "tool_choice": "auto",
    "temperature": 0.8,
    "max_response_output_tokens": "inf"
  }
}
```

**Session parameters:**
- **model**: Realtime model (gpt-realtime, gpt-realtime-1.5, dated variants)
- **voice**: Output voice (alloy, ash, ballad, coral, echo, sage, shimmer, verse)
- **modalities**: Array of "text" and/or "audio"
- **instructions**: System prompt for the session
- **input_audio_format**: pcm16, g711_ulaw, g711_alaw
- **output_audio_format**: pcm16, g711_ulaw, g711_alaw
- **input_audio_transcription**: Enable input transcription with specified model
- **turn_detection**: Server VAD config or null for client-managed turns
- **tools**: Function definitions for function calling
- **tool_choice**: "auto", "none", "required", or specific function
- **temperature**: 0.6-1.2 (default 0.8)
- **max_response_output_tokens**: Token limit or "inf"

### input_audio_buffer.append

Send audio data to the server input buffer. Audio is base64-encoded.

```json
{
  "type": "input_audio_buffer.append",
  "audio": "<base64-encoded-audio-chunk>"
}
```

Send frequently (every 20-100ms) for smooth streaming. Server accumulates audio until VAD triggers or client commits.

### input_audio_buffer.commit

Commit the current audio buffer as a completed user audio turn. Used when turn_detection is disabled (client-managed turns).

```json
{
  "type": "input_audio_buffer.commit"
}
```

Server responds with `input_audio_buffer.committed`. With server VAD, this is handled automatically.

### input_audio_buffer.clear

Discard all audio in the input buffer without committing.

```json
{
  "type": "input_audio_buffer.clear"
}
```

Server responds with `input_audio_buffer.cleared`.

### conversation.item.create

Add an item to the conversation. Use for injecting text messages, function call results, or pre-populating conversation history.

```json
{
  "type": "conversation.item.create",
  "item": {
    "type": "message",
    "role": "user",
    "content": [
      {
        "type": "input_text",
        "text": "What is the weather today?"
      }
    ]
  }
}
```

**Item types:**
- **message**: User or assistant message with content array
- **function_call**: Function call from assistant
- **function_call_output**: Result of a function call

**Content types (in content array):**
- **input_text**: User text input
- **input_audio**: User audio input (base64)
- **text**: Assistant text output
- **audio**: Assistant audio output

### conversation.item.retrieve

Retrieve details of a specific conversation item.

```json
{
  "type": "conversation.item.retrieve",
  "item_id": "item_abc123"
}
```

### conversation.item.truncate

Truncate audio content of an assistant message item. Useful for removing audio that was interrupted.

```json
{
  "type": "conversation.item.truncate",
  "item_id": "item_abc123",
  "content_index": 0,
  "audio_end_ms": 1500
}
```

**Parameters:**
- **item_id**: ID of the assistant message item
- **content_index**: Index of the content part to truncate
- **audio_end_ms**: Truncate audio at this millisecond offset

### conversation.item.delete

Remove an item from the conversation history.

```json
{
  "type": "conversation.item.delete",
  "item_id": "item_abc123"
}
```

### response.create

Trigger the model to generate a response. With server VAD this happens automatically, but can also be triggered manually.

```json
{
  "type": "response.create",
  "response": {
    "modalities": ["text", "audio"],
    "instructions": "Respond briefly.",
    "temperature": 0.7,
    "max_output_tokens": 500
  }
}
```

**Optional response config:**
- **modalities**: Override session modalities for this response
- **instructions**: Additional instructions for this response only
- **temperature**: Override session temperature
- **max_output_tokens**: Token limit for this response
- **conversation**: "auto" (default) or "none" (stateless, no history)
- **input**: Override conversation input items for this response

### response.cancel

Cancel an in-progress response. Any output generated so far is kept.

```json
{
  "type": "response.cancel"
}
```

### output_audio_buffer.clear

Clear any pending output audio that has not yet been played. Essential for handling user interruptions.

```json
{
  "type": "output_audio_buffer.clear"
}
```

## SDK Examples (Python)

### Configure Session with Tools

```python
import asyncio
import websockets
import json
import os

async def configure_session():
    url = "wss://api.openai.com/v1/realtime?model=gpt-realtime-1.5"
    headers = {
        "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
        "OpenAI-Beta": "realtime=v1"
    }
    
    async with websockets.connect(url, additional_headers=headers) as ws:
        # Wait for session.created
        event = json.loads(await ws.recv())
        assert event["type"] == "session.created"
        
        # Configure session
        await ws.send(json.dumps({
            "type": "session.update",
            "session": {
                "modalities": ["text", "audio"],
                "voice": "coral",
                "instructions": "You are a concise assistant.",
                "input_audio_format": "pcm16",
                "output_audio_format": "pcm16",
                "turn_detection": {
                    "type": "server_vad",
                    "threshold": 0.5,
                    "silence_duration_ms": 500
                },
                "tools": [
                    {
                        "type": "function",
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
                ]
            }
        }))
        
        # Wait for confirmation
        event = json.loads(await ws.recv())
        assert event["type"] == "session.updated"
        print("Session configured")

asyncio.run(configure_session())
```

### Handle Interruptions

```python
async def handle_interruption(ws):
    """Clear output audio and truncate when user interrupts"""
    # Clear any pending output audio
    await ws.send(json.dumps({
        "type": "output_audio_buffer.clear"
    }))
    
    # Cancel current response
    await ws.send(json.dumps({
        "type": "response.cancel"
    }))
    
    print("Interruption handled")
```

## Error Responses

- **Invalid event type**: Server sends `error` event with details
- **Missing required fields**: Server sends `error` event
- **Invalid audio format**: Server sends `error` event
- **Session not configured**: Some events require session.update first

## Differences from Other APIs

- **vs Anthropic**: No realtime/WebSocket API available
- **vs Gemini Live**: Similar event-driven model but different event names and structure. Gemini uses `BidiGenerateContent` with different message format
- **vs Grok Voice Agent**: Similar WebSocket event model, different event taxonomy

## Limitations and Known Issues

- **Audio chunk size**: Very large audio chunks may cause latency [ASSUMED]
- **Event ordering**: Events should be sent in logical order; out-of-order events may cause errors [VERIFIED] (OAIAPI-SC-OAI-RTCLEV)
- **Conversation size**: Large conversation histories increase latency and cost [ASSUMED]

## Gotchas and Quirks

- **Commit vs VAD**: With server VAD, do not send `input_audio_buffer.commit` - VAD handles turn detection automatically [VERIFIED] (OAIAPI-SC-OAI-RTCLEV)
- **Clear on interrupt**: Must send `output_audio_buffer.clear` when handling interruptions to prevent stale audio [VERIFIED] (OAIAPI-SC-OAI-GRTAPI)
- **Function call output**: After receiving function call, must create `function_call_output` item and trigger new response [VERIFIED] (OAIAPI-SC-OAI-RTCLEV)

## Sources

- OAIAPI-SC-OAI-RTCLEV - Realtime client events reference
- OAIAPI-SC-OAI-GRTAPI - Realtime API Guide

## Document History

**[2026-03-20 17:48]**
- Initial documentation created from API reference
