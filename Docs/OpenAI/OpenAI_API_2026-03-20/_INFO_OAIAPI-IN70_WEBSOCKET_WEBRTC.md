# WebSocket and WebRTC Connections

**Doc ID**: OAIAPI-IN70
**Goal**: Document WebSocket and WebRTC connection patterns for Realtime API - protocols, authentication, lifecycle
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references
- `_INFO_OAIAPI-IN39_REALTIME_OVERVIEW.md [OAIAPI-IN39]` for Realtime API context

## Summary

The Realtime API supports three connection interfaces: WebSocket (server-side), WebRTC (client-side/browser), and SIP (telephony). WebSocket connections use `wss://api.openai.com/v1/realtime` with API key authentication via headers. WebRTC enables browser-based connections using ephemeral client secrets (no API key exposure in browser). SIP connects telephony systems via the Calls API. WebSocket is ideal for server-side applications where the backend manages audio routing. WebRTC is ideal for browser-based voice interfaces with direct peer-to-peer audio. Both support the same event protocol (JSON messages) but differ in authentication and audio transport. WebSocket sends audio as base64-encoded chunks in JSON events. WebRTC handles audio via media tracks (no manual encoding needed). Connection lifecycle: connect -> session.created event -> session.update (configure) -> exchange events -> close. Heartbeat/keepalive managed automatically. Connection timeout after inactivity (configurable). EU data residency supported for specific model snapshots. [VERIFIED] (OAIAPI-SC-OAI-GRTAPI)

## Key Facts

- **WebSocket URL**: `wss://api.openai.com/v1/realtime?model={model}` [VERIFIED] (OAIAPI-SC-OAI-GRTAPI)
- **WebRTC**: Browser-based with ephemeral client secrets [VERIFIED] (OAIAPI-SC-OAI-GRTAPI)
- **SIP**: Telephony via Calls API [VERIFIED] (OAIAPI-SC-OAI-GRTAPI)
- **Auth (WebSocket)**: API key in Authorization header [VERIFIED] (OAIAPI-SC-OAI-GRTAPI)
- **Auth (WebRTC)**: Client secret from realtime.sessions.create [VERIFIED] (OAIAPI-SC-OAI-GRTAPI)
- **Protocol**: JSON events over WebSocket frames [VERIFIED] (OAIAPI-SC-OAI-GRTAPI)
- **Audio (WS)**: Base64-encoded in JSON events [VERIFIED] (OAIAPI-SC-OAI-GRTAPI)
- **Audio (WebRTC)**: Media tracks (automatic encoding) [VERIFIED] (OAIAPI-SC-OAI-GRTAPI)

## Use Cases

- **Server-side voice apps**: WebSocket from backend server
- **Browser voice UI**: WebRTC for direct browser-to-OpenAI audio
- **Call centers**: SIP for telephony integration
- **Hybrid**: Server manages logic via WebSocket, browser handles audio via WebRTC

## Connection Interfaces Comparison

- **WebSocket**
  - Best for: Server-side applications, backend audio processing
  - Auth: API key in header
  - Audio: Base64 in JSON events (manual encode/decode)
  - Latency: Depends on server location
  - Security: API key on server (safe)

- **WebRTC**
  - Best for: Browser applications, client-side voice UI
  - Auth: Ephemeral client secret (no API key in browser)
  - Audio: Media tracks (browser handles encoding)
  - Latency: Direct peer connection (lowest latency)
  - Security: Client secret is short-lived

- **SIP**
  - Best for: Telephony, call centers, IVR
  - Auth: Via Calls API (REST)
  - Audio: g711 codec over SIP
  - Latency: Telephony standard
  - Security: Dedicated IP ranges

## WebSocket Connection

### Connect

```python
import websockets
import json

url = "wss://api.openai.com/v1/realtime?model=gpt-realtime-1.5"
headers = {
    "Authorization": f"Bearer {api_key}",
    "OpenAI-Beta": "realtime=v1"
}

async with websockets.connect(url, extra_headers=headers) as ws:
    # First event: session.created
    event = json.loads(await ws.recv())
    assert event["type"] == "session.created"
    session_id = event["session"]["id"]
```

### Configure Session

```python
await ws.send(json.dumps({
    "type": "session.update",
    "session": {
        "voice": "coral",
        "instructions": "You are a helpful assistant.",
        "input_audio_format": "pcm16",
        "output_audio_format": "pcm16",
        "turn_detection": {
            "type": "server_vad",
            "threshold": 0.5,
            "silence_duration_ms": 500
        }
    }
}))
```

### Send Audio

```python
import base64

# Send audio chunk (pcm16 bytes)
audio_b64 = base64.b64encode(audio_bytes).decode()
await ws.send(json.dumps({
    "type": "input_audio_buffer.append",
    "audio": audio_b64
}))
```

### Receive Events

```python
async for message in ws:
    event = json.loads(message)
    
    if event["type"] == "response.audio.delta":
        audio = base64.b64decode(event["delta"])
        play_audio(audio)
    elif event["type"] == "response.audio.done":
        print("Audio response complete")
    elif event["type"] == "error":
        print(f"Error: {event['error']}")
```

## WebRTC Connection

### Create Client Secret (Server-Side)

```python
from openai import OpenAI

client = OpenAI()

session = client.realtime.sessions.create(
    model="gpt-realtime-1.5",
    voice="coral",
    instructions="You are a helpful assistant."
)

# Send to browser
client_secret = session.client_secret.value
```

### Create Client Secret (SDK v2.29.0 verified)

```python
# Source: openai v2.29.0 - resources/realtime/client_secrets.py
# SDK path: client.realtime.client_secrets.create (not realtime.sessions.create)
from openai import OpenAI

client = OpenAI()

response = client.realtime.client_secrets.create(
    session={
        "model": "gpt-realtime-1.5",
        "voice": "coral",
        "instructions": "You are a helpful assistant."
    }
)

client_secret = response.client_secret.value
```

### Browser-Side Connection (JavaScript)

```javascript
// Get client secret from your server
const response = await fetch('/api/realtime/session', { method: 'POST' });
const { client_secret } = await response.json();

// Create peer connection
const pc = new RTCPeerConnection();

// Add audio track from microphone
const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
stream.getTracks().forEach(track => pc.addTrack(track, stream));

// Handle incoming audio
pc.ontrack = (event) => {
  const audio = new Audio();
  audio.srcObject = event.streams[0];
  audio.play();
};

// Create offer and connect
const offer = await pc.createOffer();
await pc.setLocalDescription(offer);

const sdpResponse = await fetch('https://api.openai.com/v1/realtime/sessions/' + sessionId + '/sdp', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${client_secret}`,
    'Content-Type': 'application/sdp'
  },
  body: offer.sdp
});

const answer = await sdpResponse.text();
await pc.setRemoteDescription({ type: 'answer', sdp: answer });
```

## SDK Examples (Python)

### Full WebSocket Voice Loop - Production Ready

```python
import asyncio
import websockets
import json
import base64
import os

async def realtime_voice_session(
    instructions: str,
    voice: str = "coral",
    model: str = "gpt-realtime-1.5",
    audio_callback=None,
    tools: list = None
):
    """Production WebSocket voice session"""
    url = f"wss://api.openai.com/v1/realtime?model={model}"
    headers = {
        "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
        "OpenAI-Beta": "realtime=v1"
    }
    
    async with websockets.connect(url, extra_headers=headers) as ws:
        # Wait for session.created
        event = json.loads(await ws.recv())
        if event["type"] != "session.created":
            raise RuntimeError(f"Expected session.created, got {event['type']}")
        
        print(f"Session: {event['session']['id']}")
        
        # Configure
        session_config = {
            "voice": voice,
            "instructions": instructions,
            "input_audio_format": "pcm16",
            "output_audio_format": "pcm16",
            "turn_detection": {
                "type": "server_vad",
                "threshold": 0.5,
                "silence_duration_ms": 500
            }
        }
        if tools:
            session_config["tools"] = tools
        
        await ws.send(json.dumps({
            "type": "session.update",
            "session": session_config
        }))
        
        # Event loop
        try:
            async for message in ws:
                event = json.loads(message)
                event_type = event.get("type", "")
                
                if event_type == "response.audio.delta":
                    if audio_callback:
                        audio = base64.b64decode(event["delta"])
                        await audio_callback(audio)
                
                elif event_type == "response.text.delta":
                    print(event.get("delta", ""), end="", flush=True)
                
                elif event_type == "response.done":
                    print("\n[Response complete]")
                
                elif event_type == "error":
                    print(f"Error: {event['error']['message']}")
                
                elif event_type == "session.updated":
                    print("[Session configured]")
                
                elif event_type == "rate_limits.updated":
                    limits = event.get("rate_limits", [])
                    for limit in limits:
                        if limit.get("remaining", 0) < 10:
                            print(f"Warning: {limit['name']} remaining: {limit['remaining']}")
        
        except websockets.exceptions.ConnectionClosed as e:
            print(f"Connection closed: {e.code} {e.reason}")

# Usage
asyncio.run(realtime_voice_session(
    instructions="You are a concise voice assistant.",
    voice="coral"
))
```

## Error Responses

- **WebSocket 401**: Invalid API key or expired client secret
- **WebSocket 429**: Rate limit exceeded
- **WebSocket 1008**: Policy violation (connection closed)
- **WebRTC ICE failure**: Network connectivity issue

## Differences from Other APIs

- **vs Anthropic**: No WebSocket/WebRTC API
- **vs Gemini Live**: Uses BidiGenerateContent RPC (gRPC-based, not WebSocket)
- **vs Grok**: Different WebSocket protocol for voice

## Limitations and Known Issues

- **WebSocket single connection**: One active session per WebSocket connection [VERIFIED] (OAIAPI-SC-OAI-GRTAPI)
- **WebRTC browser support**: Requires modern browser with WebRTC support [VERIFIED] (OAIAPI-SC-OAI-GRTAPI)
- **EU residency**: Only specific model snapshots support EU data residency [VERIFIED] (OAIAPI-SC-OAI-GRTAPI)

## Gotchas and Quirks

- **Model in URL**: Model specified as query parameter in WebSocket URL, not in session config [VERIFIED] (OAIAPI-SC-OAI-GRTAPI)
- **Beta header**: Include `OpenAI-Beta: realtime=v1` for WebSocket connections [VERIFIED] (OAIAPI-SC-OAI-GRTAPI)
- **Client secret expiry**: Ephemeral tokens have short TTL; create fresh for each session [VERIFIED] (OAIAPI-SC-OAI-GRTAPI)
- **Audio format consistency**: Input and output formats must match session config [VERIFIED] (OAIAPI-SC-OAI-GRTAPI)

## Sources

- OAIAPI-SC-OAI-GRTAPI - Realtime API Guide

## Document History

**[2026-03-21 09:44]**
- Added: SDK v2.29.0 verified companion for Create Client Secret (client.realtime.client_secrets.create)

**[2026-03-20 18:46]**
- Initial documentation created
