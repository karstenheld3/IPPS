# Realtime API Overview

**Doc ID**: OAIAPI-IN39
**Goal**: Document the Realtime API architecture - WebSocket connection, sessions, transcription sessions, calls, and authentication
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references
- `_INFO_OAIAPI-IN20_REALTIME_AUDIO.md [OAIAPI-IN20]` for audio overview

## Summary

The Realtime API provides bidirectional WebSocket-based streaming for voice and text conversations with low latency. Connect via `wss://api.openai.com/v1/realtime` with API key authentication. Sessions are configured with model (gpt-realtime, gpt-realtime-1.5), modalities (text, audio), voice, and turn detection settings. Communication uses event-driven protocol: client sends events (session.update, input_audio_buffer.append, response.create) and server responds with events (session.created, response.output_audio.delta, response.done). Supports Voice Activity Detection (VAD) with server_vad (automatic) or client-managed turn boundaries. Audio formats: pcm16, g711_ulaw, g711_alaw. Features include function calling, MCP tool integration, conversation history management, audio transcription (input and output), and interruption handling. The Calls API (POST /v1/realtime/calls) manages telephony-style sessions. Client secrets (POST /v1/realtime/sessions) provide ephemeral tokens for client-side WebSocket connections without exposing API keys. Transcription sessions enable real-time audio-to-text without conversational AI. [VERIFIED] (OAIAPI-SC-OAI-RTCLNT, OAIAPI-SC-OAI-GRTAPI)

## Key Facts

- **Protocol**: WebSocket at `wss://api.openai.com/v1/realtime` [VERIFIED] (OAIAPI-SC-OAI-GRTAPI)
- **Models**: gpt-realtime, gpt-realtime-1.5, plus dated variants [VERIFIED] (OAIAPI-SC-OAI-RTSREV)
- **Modalities**: text, audio, or both [VERIFIED] (OAIAPI-SC-OAI-RTCLEV)
- **Audio formats**: pcm16, g711_ulaw, g711_alaw [VERIFIED] (OAIAPI-SC-OAI-GRTAPI)
- **VAD**: Server VAD (automatic) or client-managed [VERIFIED] (OAIAPI-SC-OAI-GRTAPI)
- **Client secrets**: Ephemeral tokens via POST /v1/realtime/sessions [VERIFIED] (OAIAPI-SC-OAI-RTCLNT)
- **Calls**: Telephony sessions via POST /v1/realtime/calls [VERIFIED] (OAIAPI-SC-OAI-RTCALL)
- **MCP support**: Remote MCP tools in Realtime sessions [VERIFIED] (OAIAPI-SC-OAI-RTSREV)

## Use Cases

- **Voice assistants**: Real-time conversational AI with natural turn-taking
- **Phone agents**: Automated customer support via telephony (SIP/PSTN)
- **Live transcription**: Real-time speech-to-text for meetings, broadcasts
- **Voice interfaces**: Hands-free application control
- **Interactive demos**: Low-latency voice-powered experiences

## Quick Reference

```
WebSocket: wss://api.openai.com/v1/realtime?model=gpt-realtime-1.5

Authentication (choose one):
  - Query param: ?model=gpt-realtime-1.5 + Authorization: Bearer $OPENAI_API_KEY
  - Client secret: POST /v1/realtime/sessions -> ephemeral token

REST endpoints:
  POST /v1/realtime/sessions          # Create client secret (ephemeral token)
  POST /v1/realtime/calls             # Create a call
  GET  /v1/realtime/calls/{call_id}   # Retrieve a call
  GET  /v1/realtime/calls             # List calls
```

## Architecture

### Connection Flow

1. **Authenticate**: Obtain API key or client secret (ephemeral token)
2. **Connect**: Open WebSocket to `wss://api.openai.com/v1/realtime?model=<model>`
3. **Configure**: Send `session.update` event with voice, modalities, tools, instructions
4. **Stream**: Send audio via `input_audio_buffer.append`, receive audio via `response.output_audio.delta`
5. **Respond**: Server detects speech end (VAD) or client commits buffer, triggers response
6. **Close**: Disconnect WebSocket

### Session Configuration

```json
{
  "type": "session.update",
  "session": {
    "model": "gpt-realtime-1.5",
    "voice": "alloy",
    "modalities": ["text", "audio"],
    "instructions": "You are a helpful customer service agent.",
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
    "tools": [
      {
        "type": "function",
        "name": "lookup_order",
        "description": "Look up order status",
        "parameters": {
          "type": "object",
          "properties": {
            "order_id": {"type": "string"}
          },
          "required": ["order_id"]
        }
      }
    ]
  }
}
```

### Voice Options

- **alloy** - Neutral, balanced
- **ash** - Warm, conversational
- **ballad** - Expressive
- **coral** - Clear, professional
- **echo** - Smooth
- **sage** - Calm, authoritative
- **shimmer** - Bright, energetic
- **verse** - Versatile

### Turn Detection

**Server VAD (recommended)**:
- Automatic speech detection with configurable threshold (0.0-1.0)
- `silence_duration_ms`: How long silence before triggering response (default 500ms)
- `prefix_padding_ms`: Audio before speech start to include (default 300ms)
- Handles interruptions automatically

**Client-managed**:
- Client explicitly commits audio buffer via `input_audio_buffer.commit`
- No automatic speech detection
- More control for custom turn-taking logic

### Audio Formats

- **pcm16**: 16-bit PCM, little-endian, mono. Standard for most applications
- **g711_ulaw**: mu-law compression. Standard in North American telephony
- **g711_alaw**: A-law compression. Standard in European telephony

## Client Secrets (Ephemeral Tokens)

```
POST /v1/realtime/sessions
```

Creates a short-lived token for client-side WebSocket connections without exposing API keys.

**Request:**
```json
{
  "model": "gpt-realtime-1.5",
  "voice": "alloy",
  "modalities": ["text", "audio"]
}
```

**Response:**
```json
{
  "id": "sess_abc123",
  "object": "realtime.session",
  "client_secret": {
    "value": "eph_abc123...",
    "expires_at": 1699062376
  }
}
```

Use the ephemeral token in WebSocket connection:
```
wss://api.openai.com/v1/realtime?model=gpt-realtime-1.5
Authorization: Bearer eph_abc123...
```

## SDK Examples (Python)

### Basic WebSocket Connection

```python
import asyncio
import websockets
import json
import os

async def realtime_session():
    url = "wss://api.openai.com/v1/realtime?model=gpt-realtime-1.5"
    headers = {
        "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
        "OpenAI-Beta": "realtime=v1"
    }
    
    async with websockets.connect(url, additional_headers=headers) as ws:
        # Configure session
        await ws.send(json.dumps({
            "type": "session.update",
            "session": {
                "modalities": ["text"],
                "instructions": "You are a helpful assistant."
            }
        }))
        
        # Wait for session.updated
        event = json.loads(await ws.recv())
        print(f"Event: {event['type']}")
        
        # Send text message
        await ws.send(json.dumps({
            "type": "conversation.item.create",
            "item": {
                "type": "message",
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Hello, how are you?"}
                ]
            }
        }))
        
        # Request response
        await ws.send(json.dumps({"type": "response.create"}))
        
        # Collect response
        while True:
            event = json.loads(await ws.recv())
            if event["type"] == "response.output_text.delta":
                print(event["delta"], end="", flush=True)
            elif event["type"] == "response.done":
                print()
                break

asyncio.run(realtime_session())
```

### Client Secret for Browser Applications

```python
from openai import OpenAI

client = OpenAI()

# Create ephemeral token (server-side)
session = client.realtime.sessions.create(
    model="gpt-realtime-1.5",
    voice="alloy",
    modalities=["text", "audio"]
)

# Send this token to browser client
ephemeral_token = session.client_secret.value
expires_at = session.client_secret.expires_at

print(f"Token: {ephemeral_token[:20]}...")
print(f"Expires: {expires_at}")
```

### Create Ephemeral Token (SDK v2.29.0 verified)

```python
# Source: openai v2.29.0 - resources/realtime/client_secrets.py
# SDK path: client.realtime.client_secrets.create (not client.realtime.sessions.create)
# Session config passed as session={...} dict
from openai import OpenAI

client = OpenAI()

response = client.realtime.client_secrets.create(
    session={
        "model": "gpt-realtime-1.5",
        "voice": "alloy",
        "modalities": ["text", "audio"]
    }
)

ephemeral_token = response.client_secret.value
expires_at = response.client_secret.expires_at

print(f"Token: {ephemeral_token[:20]}...")
print(f"Expires: {expires_at}")
```

### Production Voice Agent

```python
import asyncio
import websockets
import json
import os
import base64

async def voice_agent():
    """Production voice agent with error handling and function calling"""
    url = "wss://api.openai.com/v1/realtime?model=gpt-realtime-1.5"
    headers = {
        "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
        "OpenAI-Beta": "realtime=v1"
    }
    
    try:
        async with websockets.connect(
            url,
            additional_headers=headers,
            ping_interval=20,
            ping_timeout=10
        ) as ws:
            # Configure session with tools
            await ws.send(json.dumps({
                "type": "session.update",
                "session": {
                    "modalities": ["text", "audio"],
                    "voice": "coral",
                    "instructions": "You are a customer service agent for Acme Corp.",
                    "input_audio_format": "pcm16",
                    "output_audio_format": "pcm16",
                    "turn_detection": {
                        "type": "server_vad",
                        "threshold": 0.5,
                        "silence_duration_ms": 600
                    },
                    "tools": [
                        {
                            "type": "function",
                            "name": "check_order_status",
                            "description": "Check the status of a customer order",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "order_id": {
                                        "type": "string",
                                        "description": "The order ID"
                                    }
                                },
                                "required": ["order_id"]
                            }
                        }
                    ]
                }
            }))
            
            async for message in ws:
                event = json.loads(message)
                event_type = event.get("type", "")
                
                if event_type == "session.created":
                    print("Session started")
                
                elif event_type == "error":
                    print(f"Error: {event.get('error', {}).get('message')}")
                
                elif event_type == "response.output_audio.delta":
                    audio_data = base64.b64decode(event["delta"])
                    # Send audio_data to speaker/output
                
                elif event_type == "response.function_call_arguments.done":
                    # Handle function call
                    call_id = event["call_id"]
                    name = event["name"]
                    args = json.loads(event["arguments"])
                    
                    if name == "check_order_status":
                        result = {"status": "shipped", "eta": "2026-03-22"}
                    else:
                        result = {"error": f"Unknown function: {name}"}
                    
                    # Return function result
                    await ws.send(json.dumps({
                        "type": "conversation.item.create",
                        "item": {
                            "type": "function_call_output",
                            "call_id": call_id,
                            "output": json.dumps(result)
                        }
                    }))
                    await ws.send(json.dumps({"type": "response.create"}))
                
                elif event_type == "response.done":
                    print("Response complete")
                
                elif event_type == "rate_limits.updated":
                    limits = event.get("rate_limits", [])
                    for limit in limits:
                        print(f"Rate limit {limit['name']}: {limit['remaining']}/{limit['limit']}")
    
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Connection closed: {e}")
    except Exception as e:
        print(f"Error: {e}")

asyncio.run(voice_agent())
```

## Error Responses

- **401 Unauthorized** - Invalid API key or expired ephemeral token
- **429 Too Many Requests** - Rate limit exceeded (concurrent sessions)
- **500 Internal Server Error** - Server-side error, reconnect with backoff

## Rate Limiting / Throttling

- **Concurrent sessions**: Limited per organization tier
- **Audio duration**: Billed per minute of audio processed
- **Token usage**: Input/output tokens counted for text content
- **rate_limits.updated events**: Server sends real-time rate limit status during session

## Differences from Other APIs

- **vs Anthropic**: Anthropic has no realtime/streaming audio API
- **vs Gemini**: Gemini Live API (BidiGenerateContent) is similar WebSocket-based bidirectional streaming but uses different protocol and event format. Gemini supports video input in Live API
- **vs Grok**: Grok Voice Agent API (wss://api.x.ai/v1/realtime) is similar WebSocket approach
- **vs WebRTC**: OpenAI also supports WebRTC for browser-based audio; WebSocket is for server-side integration

## Limitations and Known Issues

- **Session duration**: Sessions have maximum duration limits [VERIFIED] (OAIAPI-SC-OAI-GRTAPI)
- **Concurrent sessions**: Limited by org tier [VERIFIED] (OAIAPI-SC-OAI-GRTAPI)
- **Audio-only models**: gpt-realtime models are specialized; not all GPT features available [VERIFIED] (OAIAPI-SC-OAI-GRTAPI)
- **Latency**: Network conditions affect real-time performance [ASSUMED]

## Gotchas and Quirks

- **Beta header**: Requires `OpenAI-Beta: realtime=v1` header [VERIFIED] (OAIAPI-SC-OAI-GRTAPI)
- **Ephemeral tokens expire**: Client secrets are short-lived, must refresh [VERIFIED] (OAIAPI-SC-OAI-RTCLNT)
- **VAD sensitivity**: server_vad threshold needs tuning per environment (background noise affects detection) [COMMUNITY]
- **Buffer management**: Must clear output audio buffer on interruption to prevent stale audio playback [VERIFIED] (OAIAPI-SC-OAI-GRTAPI)

## Sources

- OAIAPI-SC-OAI-RTCLNT - Client Secrets (Create session)
- OAIAPI-SC-OAI-RTCALL - Calls API (Create, Retrieve, List)
- OAIAPI-SC-OAI-RTCLEV - Client events reference
- OAIAPI-SC-OAI-RTSREV - Server events reference
- OAIAPI-SC-OAI-GRTAPI - Realtime API Guide

## Document History

**[2026-03-21 09:42]**
- Added: SDK v2.29.0 verified companion for ephemeral token (client.realtime.client_secrets.create)

**[2026-03-20 17:45]**
- Initial documentation created from API reference and guide research
