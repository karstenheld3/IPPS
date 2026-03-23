# Realtime Audio Overview

**Doc ID**: OAIAPI-IN20
**Goal**: Document realtime audio streaming, voice agents, and realtime transcription overview
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references

## Summary

Realtime Audio capabilities include WebSocket-based voice streaming via Realtime API, voice agent architecture for conversational AI, and realtime transcription sessions. The Realtime API provides bidirectional audio streaming with low latency for voice conversations, supporting interruptions, function calling, and multi-turn dialogs. Voice agents combine speech-to-text, text generation, and text-to-speech in unified conversational flow with natural turn-taking and context awareness. Realtime transcription enables live audio-to-text conversion for meetings, calls, and broadcasts. Key features: VAD (voice activity detection), audio buffering, session management, WebSocket connections, and event-driven communication. Supports gpt-4o-realtime models optimized for conversational latency. Distinct from batch transcription - realtime processes audio as it arrives. [VERIFIED] (OAIAPI-SC-OAI-GAUDIO, OAIAPI-SC-OAI-GRTAPI, OAIAPI-SC-OAI-GVOICE)

## Key Facts

- **Protocol**: WebSocket for bidirectional streaming [VERIFIED] (OAIAPI-SC-OAI-GRTAPI)
- **Models**: gpt-4o-realtime optimized for voice [VERIFIED] (OAIAPI-SC-OAI-GRTAPI)
- **Use cases**: Voice assistants, phone agents, live transcription [VERIFIED] (OAIAPI-SC-OAI-GVOICE)
- **Latency**: Low-latency streaming (~200-500ms) [VERIFIED] (OAIAPI-SC-OAI-GRTAPI)
- **Features**: VAD, interruptions, function calling [VERIFIED] (OAIAPI-SC-OAI-GRTAPI)

## Use Cases

- **Voice assistants**: Conversational AI applications
- **Customer service**: Automated phone support
- **Live transcription**: Meeting transcripts, captions
- **Voice interfaces**: Hands-free applications
- **Interactive voice response**: IVR systems

## Quick Reference

```
WebSocket: wss://api.openai.com/v1/realtime

Session config: {
  "model": "gpt-4o-realtime",
  "voice": "alloy",
  "modalities": ["text", "audio"]
}
```

## Realtime API Components

### WebSocket Connection

**Endpoint**: `wss://api.openai.com/v1/realtime`

**Authentication**: API key in query param or Authorization header

**Session lifecycle**:
1. Connect WebSocket
2. Configure session
3. Stream audio/text
4. Receive responses
5. Close session

### Session Configuration

```json
{
  "type": "session.update",
  "session": {
    "model": "gpt-4o-realtime",
    "voice": "alloy",
    "modalities": ["text", "audio"],
    "instructions": "You are a helpful assistant",
    "input_audio_format": "pcm16",
    "output_audio_format": "pcm16",
    "turn_detection": {
      "type": "server_vad",
      "threshold": 0.5,
      "silence_duration_ms": 500
    }
  }
}
```

### Audio Formats

**Supported formats**:
- **pcm16**: 16-bit PCM (raw audio)
- **g711_ulaw**: G.711 μ-law (telephony)
- **g711_alaw**: G.711 A-law (telephony)

**Sample rates**: 16kHz, 24kHz (model-dependent)

### Voice Activity Detection (VAD)

**Server VAD** (recommended):
- Automatic turn detection
- Configurable threshold
- Silence duration triggers

**Client VAD**:
- Client controls turn boundaries
- More control, more complexity

## Voice Agents

### Architecture

```
User Speech → STT → Text Processing → TTS → Agent Speech
             ↑                              ↓
             └──────── Context Loop ────────┘
```

### Features

- **Natural conversation**: Turn-taking, interruptions
- **Context awareness**: Multi-turn memory
- **Function calling**: Invoke tools during conversation
- **Personality**: Configurable voice and behavior

### Implementation Patterns

**WebSocket-based**:
- Real-time bidirectional streaming
- Low latency
- Suitable for: chatbots, voice assistants

**SIP-based** (telephony):
- Phone integration
- IVR systems
- Suitable for: customer service, call centers

## Realtime Transcription

### Live Transcription Sessions

Real-time audio-to-text as audio streams:
- Lower latency than batch transcription
- Partial results during speech
- Final results after silence
- Suitable for: live captions, meeting notes

### Transcription Workflow

1. **Start session**: Initialize transcription
2. **Stream audio**: Send audio chunks
3. **Receive partials**: Get interim results
4. **Finalize**: Get complete transcription
5. **Close session**: End transcription

## Event Types

### Client → Server

- **session.update**: Configure session
- **input_audio_buffer.append**: Send audio chunk
- **input_audio_buffer.commit**: Mark audio complete
- **conversation.item.create**: Add text message
- **response.create**: Request response

### Server → Client

- **session.created**: Session initialized
- **conversation.item.created**: New item added
- **input_audio_buffer.speech_started**: Speech detected
- **input_audio_buffer.speech_stopped**: Silence detected
- **response.audio.delta**: Audio response chunk
- **response.audio.done**: Audio complete
- **response.text.delta**: Text response chunk
- **response.text.done**: Text complete

## SDK Examples (Python)

### Basic Realtime Connection

```python
import asyncio
import websockets
import json
import os

async def realtime_session():
    api_key = os.getenv("OPENAI_API_KEY")
    url = f"wss://api.openai.com/v1/realtime?api_key={api_key}"
    
    async with websockets.connect(url) as ws:
        # Configure session
        config = {
            "type": "session.update",
            "session": {
                "model": "gpt-4o-realtime",
                "voice": "alloy",
                "modalities": ["text", "audio"]
            }
        }
        await ws.send(json.dumps(config))
        
        # Send text message
        message = {
            "type": "conversation.item.create",
            "item": {
                "type": "message",
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Hello!"}
                ]
            }
        }
        await ws.send(json.dumps(message))
        
        # Request response
        await ws.send(json.dumps({"type": "response.create"}))
        
        # Receive events
        async for message in ws:
            event = json.loads(message)
            print(f"Event: {event['type']}")
            
            if event['type'] == "response.text.done":
                print(f"Response: {event['text']}")
                break

# Run
asyncio.run(realtime_session())
```

### Voice Agent Example

```python
import asyncio
import websockets
import json
import pyaudio
import os

async def voice_agent():
    api_key = os.getenv("OPENAI_API_KEY")
    url = f"wss://api.openai.com/v1/realtime?api_key={api_key}"
    
    # Audio setup
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=24000,
        input=True,
        output=True,
        frames_per_buffer=4096
    )
    
    async with websockets.connect(url) as ws:
        # Configure session
        config = {
            "type": "session.update",
            "session": {
                "model": "gpt-4o-realtime",
                "voice": "nova",
                "modalities": ["audio"],
                "input_audio_format": "pcm16",
                "output_audio_format": "pcm16",
                "turn_detection": {
                    "type": "server_vad",
                    "threshold": 0.5,
                    "silence_duration_ms": 700
                }
            }
        }
        await ws.send(json.dumps(config))
        
        async def send_audio():
            while True:
                audio_chunk = stream.read(4096, exception_on_overflow=False)
                event = {
                    "type": "input_audio_buffer.append",
                    "audio": audio_chunk.hex()
                }
                await ws.send(json.dumps(event))
                await asyncio.sleep(0.01)
        
        async def receive_events():
            async for message in ws:
                event = json.loads(message)
                
                if event['type'] == "response.audio.delta":
                    audio_data = bytes.fromhex(event['delta'])
                    stream.write(audio_data)
                
                elif event['type'] == "response.audio.done":
                    print("Response complete")
        
        # Run both concurrently
        await asyncio.gather(send_audio(), receive_events())
    
    stream.close()
    audio.terminate()

# Run
asyncio.run(voice_agent())
```

### Realtime Transcription

```python
import asyncio
import websockets
import json
import os

async def realtime_transcription(audio_stream):
    api_key = os.getenv("OPENAI_API_KEY")
    url = f"wss://api.openai.com/v1/realtime?api_key={api_key}"
    
    async with websockets.connect(url) as ws:
        # Configure for transcription
        config = {
            "type": "session.update",
            "session": {
                "model": "gpt-4o-realtime",
                "modalities": ["text"],
                "input_audio_format": "pcm16",
                "turn_detection": {
                    "type": "server_vad"
                }
            }
        }
        await ws.send(json.dumps(config))
        
        transcript = []
        
        async def send_audio():
            for chunk in audio_stream:
                event = {
                    "type": "input_audio_buffer.append",
                    "audio": chunk.hex()
                }
                await ws.send(json.dumps(event))
                await asyncio.sleep(0.01)
        
        async def receive_transcription():
            async for message in ws:
                event = json.loads(message)
                
                if event['type'] == "conversation.item.created":
                    if event['item']['role'] == "user":
                        text = event['item']['content'][0]['transcript']
                        transcript.append(text)
                        print(f"[Transcript] {text}")
        
        await asyncio.gather(send_audio(), receive_transcription())
        
        return transcript

# Usage
# transcript = asyncio.run(realtime_transcription(audio_stream))
```

## Error Responses

- **Connection errors**: WebSocket connection failures
- **Authentication errors**: Invalid API key
- **Model errors**: Unsupported model or configuration

## Rate Limiting / Throttling

- **Concurrent sessions**: Limited active WebSocket connections
- **Audio duration**: Usage tracked by audio minutes
- **Token usage**: Text responses count toward limits

## Differences from Other APIs

- **vs Batch transcription**: Realtime processes as audio arrives, batch after upload
- **vs Twilio/Vonage**: OpenAI provides AI models, telephony providers handle calls
- **vs Google Dialogflow**: Similar voice agent capabilities, different implementation

## Limitations and Known Issues

- **WebSocket only**: No REST API alternative [VERIFIED] (OAIAPI-SC-OAI-GRTAPI)
- **Model availability**: Limited realtime-optimized models [VERIFIED] (OAIAPI-SC-OAI-GRTAPI)
- **Network sensitivity**: Requires stable connection [COMMUNITY] (OAIAPI-SC-SO-RTNET)

## Gotchas and Quirks

- **VAD tuning required**: Default VAD may need adjustment [COMMUNITY] (OAIAPI-SC-SO-VAD)
- **Audio format critical**: Format mismatch causes errors [COMMUNITY] (OAIAPI-SC-SO-AUDFMT)
- **Session state**: Must manage conversation state manually [VERIFIED] (OAIAPI-SC-OAI-GRTAPI)

## Sources

- OAIAPI-SC-OAI-GAUDIO - Audio guide
- OAIAPI-SC-OAI-GRTAPI - Realtime API guide
- OAIAPI-SC-OAI-GVOICE - Voice agents guide

## Document History

**[2026-03-20 15:45]**
- Initial documentation created
