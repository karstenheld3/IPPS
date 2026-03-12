# INFO: OpenAI API - Background Mode and WebSocket Mode

**Doc ID**: OAIAPI-IN66
**Goal**: Document new execution modes: Background mode for async tasks, WebSocket mode for persistent connections
**Version scope**: API v1, Documentation date 2026-03-12

**Depends on:**
- `__OAIAPI_SOURCES.md [OAIAPI-IN01]` for source references

## Summary

The OpenAI API now supports additional execution modes beyond synchronous REST and SSE streaming. Background mode enables long-running async tasks that can be polled or receive webhook notifications. WebSocket mode provides persistent bidirectional connections for real-time interactions. These modes complement the existing Realtime API for voice and expand options for building responsive, scalable applications.

## Key Facts

- **Background mode**: Async execution for long-running tasks [VERIFIED]
- **WebSocket mode**: Persistent bidirectional connections [VERIFIED]
- **Conversation state**: Server-managed state across requests [VERIFIED]

## Background Mode

Execute long-running tasks asynchronously without blocking.

**Use cases**:
- Long agentic workflows
- Multi-step research tasks
- Batch-like individual requests
- Tasks exceeding typical timeout limits

**Documentation**: https://developers.openai.com/api/docs/guides/background

### Key Features

- Submit task and receive job ID
- Poll for status/results
- Webhook notifications on completion
- No connection timeout constraints

## WebSocket Mode

Persistent bidirectional connection for real-time interactions.

**Use cases**:
- Real-time chat applications
- Live coding assistants
- Interactive agents
- Low-latency streaming

**Documentation**: https://developers.openai.com/api/docs/guides/websocket-mode

### Key Features

- Persistent connection
- Bidirectional messaging
- Lower latency than HTTP
- Maintains conversation context

## Conversation State

Server-managed conversation state for multi-turn interactions.

**Use cases**:
- Stateful assistants
- Context preservation
- Memory management
- Session continuity

**Documentation**: https://developers.openai.com/api/docs/guides/conversation-state

### Key Features

- Server stores conversation history
- Reference previous responses by ID
- Automatic context management
- Compaction for long sessions

## Run and Scale Section Overview

From the API sidebar navigation:

- Conversation state
- Background mode
- Streaming (SSE)
- WebSocket mode
- Webhooks
- File inputs

## Gotchas and Quirks

- Background mode has different billing/timeout characteristics
- WebSocket requires connection management (reconnect logic)
- Conversation state has storage limits
- Consider compaction for very long sessions

## Related Endpoints

- `_INFO_OAIAPI_RESPONSES.md` - Responses API (base for these modes)
- `_INFO_OAIAPI_REALTIME.md` - Realtime API (voice-focused WebSocket)
- `_INFO_OAIAPI_WEBHOOKS.md` - Webhook delivery

## Sources

- `OAIAPI-IN01-SC-DEV-GPT54` - https://developers.openai.com/api/docs/guides/latest-model (sidebar navigation) [2026-03-12]

## Document History

**[2026-03-12 21:18]**
- Initial documentation created from new Run and Scale section in API docs
