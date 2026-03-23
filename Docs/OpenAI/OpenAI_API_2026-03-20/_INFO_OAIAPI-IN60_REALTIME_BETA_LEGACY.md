# Realtime API Beta (Legacy) [DEPRECATED sunset 2026-05-07]

**Doc ID**: OAIAPI-IN60
**Goal**: Document the [DEPRECATED] Realtime API beta endpoints (sunset 2026-05-07) and migration to GA Realtime API
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references
- `_INFO_OAIAPI-IN39_REALTIME_OVERVIEW.md [OAIAPI-IN39]` for current Realtime API

## Summary

The Realtime API beta was the initial preview release of OpenAI's WebSocket-based real-time audio/text streaming capability. Originally launched with `gpt-4o-realtime-preview` models, it provided bidirectional audio streaming, voice activity detection, and function calling over WebSocket connections. The beta used the `OpenAI-Beta: realtime=v1` header and connected via `wss://api.openai.com/v1/realtime`. The beta evolved through several model snapshots (`gpt-4o-realtime-preview-2024-10-01`, `gpt-4o-realtime-preview-2024-12-17`) before reaching general availability with `gpt-realtime` and `gpt-realtime-1.5` models. Key additions from beta to GA: MCP tool support, DTMF detection, Calls API (SIP telephony), transcription sessions, improved audio codecs, enhanced VAD, and client secrets for browser-safe authentication. The beta API surface (events, session config) remains largely compatible with the GA version. Legacy model snapshots will be deprecated per the model lifecycle policy. [VERIFIED] (OAIAPI-SC-OAI-GRTAPI)

## Key Facts

- **Beta models**: gpt-4o-realtime-preview, dated snapshots [VERIFIED] (OAIAPI-SC-OAI-GRTAPI)
- **GA models**: gpt-realtime, gpt-realtime-1.5 [VERIFIED] (OAIAPI-SC-OAI-RTSREV)
- **Protocol**: Same WebSocket protocol, beta header still accepted [VERIFIED] (OAIAPI-SC-OAI-GRTAPI)
- **GA additions**: MCP, DTMF, Calls API, transcription sessions, client secrets [VERIFIED] (OAIAPI-SC-OAI-RTSREV)

## Evolution: Beta to GA

### Beta (2024)
- Models: `gpt-4o-realtime-preview`
- Events: Core session, audio buffer, conversation, response events
- VAD: Basic server_vad
- Audio: pcm16 only initially
- Auth: API key only

### GA (2025-2026)
- Models: `gpt-realtime`, `gpt-realtime-1.5`, dated variants
- Events: Added MCP events, DTMF, transcription delta/segment events
- VAD: Enhanced with prefix_padding_ms, timeout_triggered
- Audio: pcm16, g711_ulaw, g711_alaw
- Auth: API key + client secrets (ephemeral tokens)
- New features: Calls API, SIP integration, transcription sessions

## Migration

### Model Update

```python
# Before (beta)
url = "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview"

# After (GA)
url = "wss://api.openai.com/v1/realtime?model=gpt-realtime-1.5"
```

### Client Secrets (New in GA)

```python
from openai import OpenAI
client = OpenAI()

# Create ephemeral token for browser clients
session = client.realtime.sessions.create(
    model="gpt-realtime-1.5",
    voice="alloy"
)
# Send session.client_secret.value to frontend
```

### Client Secrets (SDK v2.29.0 verified)

```python
# Source: openai v2.29.0 - resources/realtime/client_secrets.py
# SDK path: client.realtime.client_secrets.create (not realtime.sessions.create)
from openai import OpenAI
client = OpenAI()

response = client.realtime.client_secrets.create(
    session={
        "model": "gpt-realtime-1.5",
        "voice": "alloy"
    }
)
# Send response.client_secret.value to frontend
```

### Session Config Changes

Most session configuration is backwards-compatible. New fields added in GA:
- `input_audio_transcription.model` - Specify transcription model
- MCP server configuration in tools
- Enhanced turn_detection options

## Differences from Other APIs

- **vs Current GA**: Beta is subset of GA. All beta events still work in GA
- **vs Anthropic**: No realtime audio API at any stage
- **vs Gemini Live**: Gemini launched Live API (BidiGenerateContent) with similar timeline

## Limitations and Known Issues

- **Sunset date**: Beta endpoints shut down **2026-05-07** - migrate to GA before this date [VERIFIED] (OAIAPI-SC-OAI-GRTAPI)
- **Preview model deprecation**: gpt-4o-realtime-preview snapshots will be deprecated [VERIFIED] (OAIAPI-SC-OAI-GRTAPI)
- **No new features on beta models**: All development on GA models [VERIFIED] (OAIAPI-SC-OAI-GRTAPI)

## Sources

- OAIAPI-SC-OAI-GRTAPI - Realtime API Guide
- OAIAPI-SC-OAI-RTSREV - Server events reference

## Document History

**[2026-03-21 09:43]**
- Added: SDK v2.29.0 verified companion for Client Secrets (client.realtime.client_secrets.create)

**[2026-03-20 19:58]**
- Added: [DEPRECATED] tag with sunset date (2026-05-07) to title and limitations

**[2026-03-20 18:30]**
- Initial documentation created
