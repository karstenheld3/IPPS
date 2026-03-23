# Assistants API (Legacy)

**Doc ID**: OAIAPI-IN58
**Goal**: Document the deprecated Assistants API - threads, runs, steps, and migration path to Responses API
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references

## Summary

The Assistants API is **deprecated** and will shut down on **2026-08-26**. It provided server-side conversation state management via Threads (message collections), Runs (asynchronous processing), and Steps (execution details). Assistants were configurable AI agents with instructions, tools (code_interpreter, file_search, function), and model settings. The Responses API replaces all Assistants functionality with a simpler, synchronous API. Key concepts: Assistants (persistent agent config), Threads (conversation sessions, max 100,000 messages), Messages (user/assistant content within threads), Runs (process a thread with an assistant), Run Steps (individual tool calls and model invocations within a run). Migration path: Threads -> conversation state managed client-side or via `previous_response_id`; Runs -> synchronous `responses.create`; Code Interpreter/File Search -> same tools in Responses API; Assistants -> inline model config in each request. [VERIFIED] (OAIAPI-SC-OAI-ASTAPI, OAIAPI-SC-OAI-ASTMIG)

## Key Facts

- **Status**: DEPRECATED - shuts down 2026-08-26 [VERIFIED] (OAIAPI-SC-OAI-ASTMIG)
- **Replacement**: Responses API with full feature parity [VERIFIED] (OAIAPI-SC-OAI-ASTMIG)
- **Beta header**: Required `OpenAI-Beta: assistants=v2` [VERIFIED] (OAIAPI-SC-OAI-ASTAPI)
- **Server-side state**: Threads stored conversation history on OpenAI servers [VERIFIED] (OAIAPI-SC-OAI-ASTAPI)
- **Async processing**: Runs processed asynchronously, required polling [VERIFIED] (OAIAPI-SC-OAI-ASTAPI)
- **Thread limit**: 100,000 messages per thread [VERIFIED] (OAIAPI-SC-OAI-ASTAPI)

## Quick Reference

```
Assistants:
  POST   /v1/assistants                          # Create
  GET    /v1/assistants                          # List
  GET    /v1/assistants/{id}                     # Retrieve
  POST   /v1/assistants/{id}                     # Update
  DELETE /v1/assistants/{id}                     # Delete

Threads:
  POST   /v1/threads                             # Create
  GET    /v1/threads/{id}                        # Retrieve
  POST   /v1/threads/{id}                        # Update
  DELETE /v1/threads/{id}                        # Delete

Messages:
  POST   /v1/threads/{id}/messages               # Create
  GET    /v1/threads/{id}/messages               # List
  GET    /v1/threads/{id}/messages/{msg_id}      # Retrieve
  POST   /v1/threads/{id}/messages/{msg_id}      # Update
  DELETE /v1/threads/{id}/messages/{msg_id}      # Delete

Runs:
  POST   /v1/threads/{id}/runs                   # Create
  GET    /v1/threads/{id}/runs                   # List
  GET    /v1/threads/{id}/runs/{run_id}          # Retrieve
  POST   /v1/threads/{id}/runs/{run_id}          # Update
  POST   /v1/threads/{id}/runs/{run_id}/cancel   # Cancel
  POST   /v1/threads/{id}/runs/{run_id}/submit_tool_outputs  # Submit tool results

Run Steps:
  GET    /v1/threads/{id}/runs/{run_id}/steps           # List
  GET    /v1/threads/{id}/runs/{run_id}/steps/{step_id} # Retrieve
```

## Migration to Responses API

### Key Mappings

- **Assistant** -> Inline model config in `responses.create` call
- **Thread** -> Client-side history or `previous_response_id` chaining
- **Run** -> Synchronous `responses.create` call
- **Messages** -> `input` parameter (string or array)
- **Run Steps** -> Output items in response
- **code_interpreter tool** -> Same tool in Responses API (with containers)
- **file_search tool** -> Same tool in Responses API (with vector stores)

### Before (Assistants)

```python
from openai import OpenAI
client = OpenAI()

# Create assistant
assistant = client.beta.assistants.create(
    model="gpt-5.4",
    instructions="You are a helpful assistant.",
    tools=[{"type": "file_search"}]
)

# Create thread and message
thread = client.beta.threads.create()
client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="What's in my documents?"
)

# Run and poll
run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant.id
)

# Get messages
messages = client.beta.threads.messages.list(thread_id=thread.id)
```

### After (Responses API)

```python
from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-5.4",
    instructions="You are a helpful assistant.",
    tools=[{
        "type": "file_search",
        "vector_store_ids": ["vs_abc123"]
    }],
    input="What's in my documents?"
)

print(response.output_text)

# Chain conversations
followup = client.responses.create(
    model="gpt-5.4",
    instructions="You are a helpful assistant.",
    previous_response_id=response.id,
    input="Tell me more about the first document."
)
```

## Error Responses

- **400 Bad Request** - Invalid parameters
- **404 Not Found** - Assistant, thread, or run not found
- **409 Conflict** - Run already in progress on thread

## Differences from Other APIs

- **vs Anthropic**: Anthropic has no equivalent server-side state management
- **vs Gemini**: Gemini has no assistants/threads concept
- **vs Responses API**: Assistants is async + server-side state; Responses is sync + client-side state

## Limitations and Known Issues

- **Deprecated**: Will shut down 2026-08-26 [VERIFIED] (OAIAPI-SC-OAI-ASTMIG)
- **Async complexity**: Required polling for run completion [VERIFIED] (OAIAPI-SC-OAI-ASTAPI)
- **No new features**: Feature development moved to Responses API [VERIFIED] (OAIAPI-SC-OAI-ASTMIG)

## Sources

- OAIAPI-SC-OAI-ASTAPI - Assistants API Reference
- OAIAPI-SC-OAI-ASTMIG - Assistants Migration Guide

## Document History

**[2026-03-20 18:26]**
- Initial documentation created
