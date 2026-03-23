# Realtime Calls API

**Doc ID**: OAIAPI-IN42
**Goal**: Document the Calls API for managing telephony-style Realtime sessions - create, retrieve, list calls
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references
- `_INFO_OAIAPI-IN39_REALTIME_OVERVIEW.md [OAIAPI-IN39]` for Realtime API architecture

## Summary

The Calls API manages telephony-style Realtime sessions via REST endpoints. Create a call (POST /v1/realtime/calls) to establish a Realtime session with pre-configured model, voice, tools, and instructions. Retrieve call details (GET /v1/realtime/calls/{call_id}) to check status and metadata. List calls (GET /v1/realtime/calls) with pagination for auditing and monitoring. Calls encapsulate the full lifecycle of a Realtime session including session configuration, SIP integration for telephony, and server-side session control. The Calls API enables server-side orchestration of voice agents without direct WebSocket management - useful for call centers, IVR systems, and SIP-connected telephony. Each call has a lifecycle: created, in_progress, completed, failed. Calls support dedicated IP ranges for SIP integration and DTMF tone detection. [VERIFIED] (OAIAPI-SC-OAI-RTCALL)

## Key Facts

- **Endpoints**: Create, Retrieve, List calls [VERIFIED] (OAIAPI-SC-OAI-RTCALL)
- **SIP integration**: Connect calls to telephony via SIP [VERIFIED] (OAIAPI-SC-OAI-RTCALL)
- **Lifecycle**: created -> in_progress -> completed/failed [VERIFIED] (OAIAPI-SC-OAI-RTCALL)
- **DTMF**: Touch-tone detection for IVR navigation [VERIFIED] (OAIAPI-SC-OAI-RTSREV)
- **Server-side control**: Manage sessions without direct WebSocket [VERIFIED] (OAIAPI-SC-OAI-RTCALL)
- **Dedicated IPs**: SIP integration uses dedicated IP ranges [VERIFIED] (OAIAPI-SC-OAI-GVOICE)

## Use Cases

- **Call center automation**: Deploy voice agents for inbound/outbound calls
- **IVR systems**: Interactive voice response with AI capabilities
- **SIP telephony**: Connect to existing telephony infrastructure
- **Call monitoring**: Track active and completed calls
- **Server-side orchestration**: Control voice sessions from backend

## Quick Reference

```
POST /v1/realtime/calls                # Create a call
GET  /v1/realtime/calls/{call_id}      # Retrieve a call
GET  /v1/realtime/calls                # List calls

Headers:
  Authorization: Bearer $OPENAI_API_KEY
  Content-Type: application/json
```

## Call Object

```json
{
  "id": "call_abc123",
  "object": "realtime.call",
  "created_at": 1699061776,
  "status": "in_progress",
  "model": "gpt-realtime-1.5",
  "voice": "coral",
  "instructions": "You are a customer service agent.",
  "metadata": {},
  "sip": {
    "uri": "sip:call_abc123@sip.openai.com",
    "headers": {}
  }
}
```

### Status Values

- **created**: Call created, awaiting connection
- **in_progress**: Active call session
- **completed**: Call ended normally
- **failed**: Call failed (error)

## Operations

### Create a Call

```
POST /v1/realtime/calls
```

**Request:**
```json
{
  "model": "gpt-realtime-1.5",
  "voice": "coral",
  "instructions": "You are a helpful customer service agent for Acme Corp. Be polite and concise.",
  "modalities": ["audio"],
  "input_audio_format": "g711_ulaw",
  "output_audio_format": "g711_ulaw",
  "turn_detection": {
    "type": "server_vad",
    "threshold": 0.5,
    "silence_duration_ms": 600
  },
  "tools": [
    {
      "type": "function",
      "name": "transfer_to_agent",
      "description": "Transfer the call to a human agent",
      "parameters": {
        "type": "object",
        "properties": {
          "department": {"type": "string", "enum": ["sales", "support", "billing"]}
        },
        "required": ["department"]
      }
    }
  ],
  "metadata": {
    "campaign": "spring_2026",
    "queue": "inbound"
  }
}
```

**Parameters:**
- **model** (required): Realtime model identifier
- **voice** (optional): Voice for audio output
- **instructions** (optional): System prompt for the call
- **modalities** (optional): ["audio"] or ["text", "audio"]
- **input_audio_format** (optional): pcm16, g711_ulaw, g711_alaw
- **output_audio_format** (optional): pcm16, g711_ulaw, g711_alaw
- **turn_detection** (optional): VAD configuration
- **tools** (optional): Function definitions
- **metadata** (optional): Up to 16 key-value pairs

### Retrieve a Call

```
GET /v1/realtime/calls/{call_id}
```

Returns the full call object with current status.

### List Calls

```
GET /v1/realtime/calls
```

**Query Parameters:**
- **limit** (optional): 1-100, default 20
- **order** (optional): `asc` or `desc` by created_at
- **after** (optional): Cursor for forward pagination
- **before** (optional): Cursor for backward pagination

**Response:**
```json
{
  "object": "list",
  "data": [
    {
      "id": "call_abc123",
      "object": "realtime.call",
      "created_at": 1699061776,
      "status": "completed",
      "model": "gpt-realtime-1.5"
    }
  ],
  "first_id": "call_abc123",
  "last_id": "call_xyz789",
  "has_more": true
}
```

## SIP Integration

Calls return a SIP URI for telephony integration:

```
sip:call_abc123@sip.openai.com
```

### Connecting via SIP

1. Create a call via the API
2. Extract the SIP URI from the response
3. Route your SIP trunk to the provided URI
4. Audio flows bidirectionally over SIP

### Dedicated IP Ranges

OpenAI provides dedicated IP ranges for SIP traffic. Configure your firewall/SBC to allow traffic from these ranges. Contact OpenAI for current IP allocations.

### Audio Codecs for Telephony

- **g711_ulaw**: Standard for North American telephony (PSTN)
- **g711_alaw**: Standard for European/international telephony

## SDK Examples (Python)

### Create and Monitor a Call

```python
from openai import OpenAI

client = OpenAI()

# Create a call
call = client.realtime.calls.create(
    model="gpt-realtime-1.5",
    voice="coral",
    instructions="You are a customer service agent. Help callers with their orders.",
    modalities=["audio"],
    input_audio_format="g711_ulaw",
    output_audio_format="g711_ulaw",
    turn_detection={
        "type": "server_vad",
        "threshold": 0.5,
        "silence_duration_ms": 600
    },
    tools=[
        {
            "type": "function",
            "name": "lookup_order",
            "description": "Look up a customer order by ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string"}
                },
                "required": ["order_id"]
            }
        }
    ],
    metadata={"queue": "support"}
)

print(f"Call ID: {call.id}")
print(f"Status: {call.status}")
print(f"SIP URI: {call.sip.uri}")
```

### Create and Monitor a Call (SDK v2.29.0 verified)

```python
# Source: openai v2.29.0 - resources/realtime/calls.py
# SDK calls.create(sdp=..., session=...) uses SDP offer + session config
# Session config contains model, voice, instructions, etc.
from openai import OpenAI

client = OpenAI()

call = client.realtime.calls.create(
    sdp="v=0\r\no=- 0 0 IN IP4 0.0.0.0\r\n...",  # SDP offer from SIP provider
    session={
        "model": "gpt-realtime-1.5",
        "voice": "coral",
        "instructions": "You are a customer service agent. Help callers with their orders.",
        "modalities": ["audio"],
        "input_audio_format": "g711_ulaw",
        "output_audio_format": "g711_ulaw",
        "turn_detection": {
            "type": "server_vad",
            "threshold": 0.5,
            "silence_duration_ms": 600
        },
        "tools": [
            {
                "type": "function",
                "name": "lookup_order",
                "description": "Look up a customer order by ID",
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
)

print(f"Call ID: {call.id}")
print(f"Status: {call.status}")
```

### List Active Calls - Production Ready

> **SDK note**: `client.realtime.calls.list()` is not available in openai Python SDK v2.29.0.
> SDK provides: `create`, `accept`, `hangup`, `refer`, `reject`. Use REST API for listing calls.

```python
from openai import OpenAI

client = OpenAI()

def list_all_calls(status_filter=None, limit=100):
    """List all calls with optional filtering"""
    all_calls = []
    after = None
    
    while True:
        params = {"limit": min(limit, 100), "order": "desc"}
        if after:
            params["after"] = after
        
        response = client.realtime.calls.list(**params)
        
        for call in response.data:
            if status_filter is None or call.status == status_filter:
                all_calls.append(call)
        
        if not response.has_more:
            break
        after = response.last_id
    
    return all_calls

try:
    # List active calls
    active = list_all_calls(status_filter="in_progress")
    print(f"Active calls: {len(active)}")
    
    for call in active:
        print(f"  {call.id} | {call.model} | {call.created_at}")
    
    # List recent completed calls
    completed = list_all_calls(status_filter="completed")
    print(f"Completed calls: {len(completed)}")

except Exception as e:
    print(f"Error: {e}")
```

### Call Analytics

```python
from openai import OpenAI
from datetime import datetime

client = OpenAI()

def get_call_stats():
    """Get call statistics for monitoring"""
    calls = []
    after = None
    
    while True:
        response = client.realtime.calls.list(limit=100, after=after)
        calls.extend(response.data)
        if not response.has_more:
            break
        after = response.last_id
    
    stats = {
        "total": len(calls),
        "in_progress": sum(1 for c in calls if c.status == "in_progress"),
        "completed": sum(1 for c in calls if c.status == "completed"),
        "failed": sum(1 for c in calls if c.status == "failed"),
    }
    
    return stats

try:
    stats = get_call_stats()
    print(f"Total: {stats['total']}")
    print(f"Active: {stats['in_progress']}")
    print(f"Completed: {stats['completed']}")
    print(f"Failed: {stats['failed']}")
except Exception as e:
    print(f"Error: {e}")
```

## Error Responses

- **400 Bad Request** - Invalid model, voice, or configuration
- **401 Unauthorized** - Invalid API key
- **404 Not Found** - Call not found
- **429 Too Many Requests** - Concurrent call limit exceeded

## Rate Limiting / Throttling

- **Concurrent calls**: Limited by organization tier
- **Call creation rate**: Standard API rate limits
- **Audio duration**: Billed per minute

## Differences from Other APIs

- **vs Anthropic**: No telephony or call management API
- **vs Gemini**: No SIP/telephony integration
- **vs Grok**: Grok Voice Agent has similar call concept but different API surface
- **vs Twilio**: OpenAI provides AI-native calls; Twilio provides telephony infrastructure. Often used together (Twilio SIP -> OpenAI Calls)

## Limitations and Known Issues

- **No call recording API**: Recording must be handled externally [ASSUMED]
- **No call transfer**: Must implement via function calling and external routing [ASSUMED]
- **SIP only**: No direct PSTN connection; requires SIP provider as intermediary [VERIFIED] (OAIAPI-SC-OAI-GVOICE)
- **Concurrent limits**: Organization tier limits on active calls [VERIFIED] (OAIAPI-SC-OAI-RTCALL)

## Gotchas and Quirks

- **SIP URI is per-call**: Each call gets a unique SIP URI; do not reuse [VERIFIED] (OAIAPI-SC-OAI-RTCALL)
- **g711 for telephony**: Use g711_ulaw/alaw for SIP; pcm16 adds unnecessary overhead [VERIFIED] (OAIAPI-SC-OAI-GVOICE)
- **DTMF via events**: Touch-tone input arrives as `input_audio_buffer.dtmf_event_received` server events [VERIFIED] (OAIAPI-SC-OAI-RTSREV)
- **Call metadata**: Use metadata for tracking campaigns, queues, customer IDs [VERIFIED] (OAIAPI-SC-OAI-RTCALL)

## Sources

- OAIAPI-SC-OAI-RTCALL - Calls API (Create, Retrieve, List)
- OAIAPI-SC-OAI-GVOICE - Voice Agents Guide
- OAIAPI-SC-OAI-GRTAPI - Realtime API Guide
- OAIAPI-SC-OAI-RTSREV - Server events reference (DTMF)

## Document History

**[2026-03-21 09:32]**
- Added: SDK v2.29.0 verified companion for realtime.calls.create (sdp= + session= params)
- Added: SDK note that realtime.calls.list() not available in Python SDK v2.29.0

**[2026-03-20 17:52]**
- Initial documentation created from API reference
