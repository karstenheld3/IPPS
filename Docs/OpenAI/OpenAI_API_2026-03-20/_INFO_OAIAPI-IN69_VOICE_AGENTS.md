# Voice Agents Guide

**Doc ID**: OAIAPI-IN69
**Goal**: Document building voice agents with OpenAI - architecture, Agents SDK, telephony, production patterns
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references
- `_INFO_OAIAPI-IN39_REALTIME_OVERVIEW.md [OAIAPI-IN39]` for Realtime API context

## Summary

Voice agents are AI-powered conversational systems that communicate via speech. OpenAI provides multiple paths to build voice agents: the Agents SDK (fastest path for common patterns), the Realtime API (full control over audio streaming), and the Calls API (telephony/SIP integration). The Agents SDK provides `VoiceAgent` abstractions for building voice-first agents with tools, handoffs, and guardrails. The Realtime API provides WebSocket-based bidirectional audio streaming with server-side VAD, multiple voice options, and function calling. The Calls API connects to telephony via SIP URIs for call center automation. Key production considerations: latency optimization (choose appropriate VAD settings, minimize tool execution time), audio format selection (g711 for telephony, pcm16 for web), interruption handling (barge-in), conversation repair (handling misheard speech), DTMF for IVR navigation, and dedicated IP ranges for SIP. Voice models include gpt-realtime and gpt-realtime-1.5 with multiple voice options (alloy, ash, ballad, coral, echo, fable, onyx, nova, sage, shimmer, verse). [VERIFIED] (OAIAPI-SC-OAI-GVOICE)

## Key Facts

- **Three paths**: Agents SDK, Realtime API, Calls API [VERIFIED] (OAIAPI-SC-OAI-GVOICE)
- **Models**: gpt-realtime, gpt-realtime-1.5 [VERIFIED] (OAIAPI-SC-OAI-GVOICE)
- **Voices**: alloy, ash, ballad, coral, echo, fable, onyx, nova, sage, shimmer, verse [VERIFIED] (OAIAPI-SC-OAI-GVOICE)
- **Audio formats**: pcm16, g711_ulaw, g711_alaw [VERIFIED] (OAIAPI-SC-OAI-GVOICE)
- **VAD**: Server-side voice activity detection with configurable thresholds [VERIFIED] (OAIAPI-SC-OAI-GVOICE)
- **Telephony**: SIP integration via Calls API [VERIFIED] (OAIAPI-SC-OAI-GVOICE)
- **DTMF**: Touch-tone detection for IVR menus [VERIFIED] (OAIAPI-SC-OAI-RTSREV)

## Use Cases

- **Call center automation**: AI agents handling inbound/outbound calls
- **IVR systems**: Voice menus with natural language understanding
- **Virtual receptionist**: Answer calls, route, take messages
- **Voice assistants**: In-app voice interaction
- **Accessibility**: Voice interface for visually impaired users
- **Language tutoring**: Conversational language practice

## Architecture Options

### Option 1: Agents SDK (Recommended for Common Patterns)

```
User Audio -> Agents SDK VoiceAgent -> Tools/Handoffs -> Audio Response
```

Fastest path. Handles audio encoding, VAD, turn management automatically.

### Option 2: Realtime API (Full Control)

```
User Audio -> WebSocket -> Realtime API -> Audio Stream
                             |
                        Tool Calls / Function Results
```

Full control over audio streaming, custom VAD, event handling.

### Option 3: Calls API (Telephony)

```
Phone Call -> SIP Trunk -> Calls API -> AI Agent -> Audio Response
                             |
                        Tool Calls / DTMF
```

SIP-connected telephony with REST-based call management.

## SDK Examples (Python)

### Voice Agent with Agents SDK

```python
from agents import Agent, Runner, function_tool
from agents.voice import VoiceAgent

@function_tool
def check_order_status(order_id: str) -> str:
    """Check the status of a customer order"""
    return f"Order {order_id}: Shipped, arriving tomorrow"

@function_tool
def transfer_to_human(department: str) -> str:
    """Transfer the call to a human agent"""
    return f"Transferring to {department}..."

voice_agent = VoiceAgent(
    name="Customer Service",
    instructions="""You are a friendly customer service agent for Acme Corp.
    Help customers check orders, answer questions, and transfer to humans when needed.
    Be concise - voice conversations should be brief and clear.""",
    model="gpt-realtime-1.5",
    voice="coral",
    tools=[check_order_status, transfer_to_human]
)

# Run voice agent (connects to audio stream)
result = Runner.run_sync(voice_agent, audio_stream=audio_input)
```

### Realtime API Voice Agent

```python
import asyncio
import websockets
import json
import base64

async def voice_agent():
    url = "wss://api.openai.com/v1/realtime?model=gpt-realtime-1.5"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "OpenAI-Beta": "realtime=v1"
    }
    
    async with websockets.connect(url, extra_headers=headers) as ws:
        # Configure session
        await ws.send(json.dumps({
            "type": "session.update",
            "session": {
                "voice": "coral",
                "instructions": "You are a helpful voice assistant. Be concise.",
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
                        "description": "Get weather for a location",
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
        
        async for message in ws:
            event = json.loads(message)
            
            if event["type"] == "response.audio.delta":
                # Play audio chunk
                audio_data = base64.b64decode(event["delta"])
                play_audio(audio_data)
            
            elif event["type"] == "response.function_call_arguments.done":
                # Handle tool call
                args = json.loads(event["arguments"])
                result = handle_tool(event["name"], args)
                
                await ws.send(json.dumps({
                    "type": "conversation.item.create",
                    "item": {
                        "type": "function_call_output",
                        "call_id": event["call_id"],
                        "output": json.dumps(result)
                    }
                }))
                
                await ws.send(json.dumps({
                    "type": "response.create"
                }))
            
            elif event["type"] == "error":
                print(f"Error: {event['error']['message']}")

asyncio.run(voice_agent())
```

### Telephony Voice Agent via Calls API

```python
from openai import OpenAI

client = OpenAI()

def create_voice_call(instructions: str, tools: list = None):
    """Create a telephony voice agent call"""
    call = client.realtime.calls.create(
        model="gpt-realtime-1.5",
        voice="coral",
        instructions=instructions,
        modalities=["audio"],
        input_audio_format="g711_ulaw",
        output_audio_format="g711_ulaw",
        turn_detection={
            "type": "server_vad",
            "threshold": 0.5,
            "silence_duration_ms": 600
        },
        tools=tools or []
    )
    
    print(f"Call ID: {call.id}")
    print(f"SIP URI: {call.sip.uri}")
    print("Route your SIP trunk to this URI")
    
    return call

# Create inbound call handler
call = create_voice_call(
    instructions="You are the automated receptionist for Acme Corp. "
    "Greet callers, determine their needs, and transfer appropriately.",
    tools=[
        {
            "type": "function",
            "name": "transfer_call",
            "description": "Transfer to a department",
            "parameters": {
                "type": "object",
                "properties": {
                    "department": {"type": "string", "enum": ["sales", "support", "billing"]}
                },
                "required": ["department"]
            }
        }
    ]
)
```

### Telephony Voice Agent via Calls API (SDK v2.29.0 verified)

```python
# Source: openai v2.29.0 - resources/realtime/calls.py
# SDK calls.create(sdp=..., session=...) wraps config in session dict
from openai import OpenAI

client = OpenAI()

def create_voice_call(sdp_offer: str, instructions: str, tools: list = None):
    """Create a telephony voice agent call via SDK"""
    call = client.realtime.calls.create(
        sdp=sdp_offer,
        session={
            "model": "gpt-realtime-1.5",
            "voice": "coral",
            "instructions": instructions,
            "modalities": ["audio"],
            "input_audio_format": "g711_ulaw",
            "output_audio_format": "g711_ulaw",
            "turn_detection": {
                "type": "server_vad",
                "threshold": 0.5,
                "silence_duration_ms": 600
            },
            "tools": tools or []
        }
    )
    print(f"Call ID: {call.id}")
    return call

call = create_voice_call(
    sdp_offer="v=0\r\no=- 0 0 IN IP4 0.0.0.0\r\n...",
    instructions="You are the automated receptionist for Acme Corp.",
    tools=[
        {
            "type": "function",
            "name": "transfer_call",
            "description": "Transfer to a department",
            "parameters": {
                "type": "object",
                "properties": {
                    "department": {"type": "string", "enum": ["sales", "support", "billing"]}
                },
                "required": ["department"]
            }
        }
    ]
)
```

## Production Best Practices

- **VAD tuning**: Adjust silence_duration_ms (shorter for fast interactions, longer for thoughtful queries)
- **Latency**: Minimize tool execution time; users notice >2s pauses
- **Interruption**: Handle barge-in gracefully (user speaking over agent)
- **Error recovery**: If speech is misheard, prompt for clarification
- **g711 for telephony**: Use g711_ulaw/alaw for SIP; pcm16 adds overhead
- **Conversation repair**: Detect and handle "sorry, I didn't catch that" patterns
- **Monitoring**: Track call duration, tool usage, and error rates

## Error Responses

- **WebSocket errors**: Connection timeout, authentication failure
- **Tool execution timeout**: Function call taking too long
- **Audio format mismatch**: Sending wrong audio format

## Differences from Other APIs

- **vs Anthropic**: No voice/audio API
- **vs Gemini Live**: Google has Gemini Live for real-time audio; different API surface
- **vs Grok Voice**: Grok has voice agent capability; different architecture
- **vs Twilio**: Twilio provides telephony infrastructure; OpenAI provides AI. Often used together

## Limitations and Known Issues

- **Long conversation degradation**: Quality may degrade in very long conversations [VERIFIED] (OAIAPI-SC-OAI-GVOICE)
- **Edge case silence**: Model may struggle with extended silence periods [VERIFIED] (OAIAPI-SC-OAI-GVOICE)
- **Tool-driven flows**: Precision in tool use during voice conversations still improving [VERIFIED] (OAIAPI-SC-OAI-GVOICE)

## Sources

- OAIAPI-SC-OAI-GVOICE - Voice Agents Guide
- OAIAPI-SC-OAI-GRTAPI - Realtime API Guide
- OAIAPI-SC-OAI-RTSREV - Server Events Reference

## Document History

**[2026-03-21 09:33]**
- Added: SDK v2.29.0 verified companion for Telephony Voice Agent (sdp= + session= params)

**[2026-03-20 18:44]**
- Initial documentation created
