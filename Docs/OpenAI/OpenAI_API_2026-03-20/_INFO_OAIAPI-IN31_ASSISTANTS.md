# Assistants API

**Doc ID**: OAIAPI-IN31
**Goal**: Document Assistants API for stateful AI agents with tools, files, and persistent threads
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references

## Summary

Assistants API provides stateful AI agents with built-in tool access (code_interpreter, file_search, function calling), file management, and persistent conversation threads. Create assistant (POST /v1/assistants) with instructions, tools, and model. Create thread (POST /v1/threads) for conversation. Add messages (POST /v1/threads/{thread_id}/messages) and run assistant (POST /v1/threads/{thread_id}/runs) to generate responses. Assistants maintain context across runs, access files, execute code, search documents. Run lifecycle: queued → in_progress → requires_action (for functions) → completed/failed. Supports streaming via SSE. Each assistant has instructions (system prompt), tools array, file_ids, metadata. Threads persist conversation history. Use for chatbots, task automation, data analysis, customer support agents. Assistants API higher-level than Responses API - manages threads, retries, tool orchestration automatically. [VERIFIED] (OAIAPI-SC-OAI-ASTCRT, OAIAPI-SC-OAI-GASSIST)

## Key Facts

- **Purpose**: Stateful AI agents with tools [VERIFIED] (OAIAPI-SC-OAI-GASSIST)
- **Components**: Assistants, Threads, Messages, Runs [VERIFIED] (OAIAPI-SC-OAI-GASSIST)
- **Built-in tools**: code_interpreter, file_search, function calling [VERIFIED] (OAIAPI-SC-OAI-ASTCRT)
- **Persistent**: Threads store conversation history [VERIFIED] (OAIAPI-SC-OAI-THRCRT)
- **Async**: Runs execute asynchronously [VERIFIED] (OAIAPI-SC-OAI-RUNCRT)

## Use Cases

- **Customer support**: Persistent support agents
- **Task automation**: Multi-step workflows
- **Data analysis**: Code interpreter for analysis
- **Knowledge bases**: File search for Q&A
- **Personal assistants**: Stateful user interactions

## Quick Reference

```python
# Create assistant
POST /v1/assistants
{
  "model": "gpt-5.4",
  "name": "Math Tutor",
  "instructions": "You are a helpful math tutor.",
  "tools": [{"type": "code_interpreter"}]
}

# Create thread
POST /v1/threads

# Add message
POST /v1/threads/{thread_id}/messages
{
  "role": "user",
  "content": "Solve x^2 + 5x + 6 = 0"
}

# Run assistant
POST /v1/threads/{thread_id}/runs
{
  "assistant_id": "asst_abc123"
}
```

## Assistant Object

```json
{
  "id": "asst_abc123",
  "object": "assistant",
  "created_at": 1234567890,
  "name": "Math Tutor",
  "description": "Helps with math problems",
  "model": "gpt-5.4",
  "instructions": "You are a helpful math tutor.",
  "tools": [
    {"type": "code_interpreter"}
  ],
  "file_ids": [],
  "metadata": {}
}
```

## Thread Object

```json
{
  "id": "thread_xyz789",
  "object": "thread",
  "created_at": 1234567890,
  "metadata": {}
}
```

## Run Object

```json
{
  "id": "run_def456",
  "object": "thread.run",
  "thread_id": "thread_xyz789",
  "assistant_id": "asst_abc123",
  "status": "completed",
  "started_at": 1234567890,
  "completed_at": 1234567900,
  "model": "gpt-5.4",
  "instructions": "You are a helpful math tutor.",
  "tools": [{"type": "code_interpreter"}],
  "usage": {
    "prompt_tokens": 100,
    "completion_tokens": 50,
    "total_tokens": 150
  }
}
```

## Assistant Lifecycle

### 1. Create Assistant

Define capabilities, tools, instructions:

```python
assistant = client.beta.assistants.create(
    name="Support Agent",
    model="gpt-5.4",
    instructions="You are a customer support agent.",
    tools=[
        {"type": "file_search"},
        {"type": "function", "function": {...}}
    ]
)
```

### 2. Create Thread

Start conversation:

```python
thread = client.beta.threads.create()
```

### 3. Add Messages

User messages to thread:

```python
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="How do I reset my password?"
)
```

### 4. Run Assistant

Execute assistant on thread:

```python
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id
)
```

### 5. Poll Run Status

Wait for completion:

```python
while run.status != "completed":
    run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )
```

### 6. Retrieve Messages

Get assistant responses:

```python
messages = client.beta.threads.messages.list(thread_id=thread.id)
```

## Run Status Flow

```
queued → in_progress → completed
                    ↓
                requires_action (function calling)
                    ↓
                submit tool outputs
                    ↓
                in_progress → completed
```

**Status values:**
- **queued**: Waiting to start
- **in_progress**: Processing
- **requires_action**: Needs function output
- **completed**: Finished successfully
- **failed**: Run failed
- **cancelled**: User cancelled
- **expired**: Run expired

## Tools

### code_interpreter

Execute Python code:
- Analyze data
- Generate plots
- Perform calculations
- Process files

### file_search

Search attached files:
- Vector store integration
- Semantic search
- Document Q&A

### function calling

Custom functions:
- External API calls
- Database queries
- Actions

## SDK Examples (Python)

### Basic Assistant

```python
from openai import OpenAI

client = OpenAI()

# Create assistant
assistant = client.beta.assistants.create(
    name="Math Tutor",
    instructions="You help students with math problems. Be clear and encouraging.",
    model="gpt-5.4",
    tools=[{"type": "code_interpreter"}]
)

# Create thread
thread = client.beta.threads.create()

# Add user message
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Solve the equation: 2x + 5 = 15"
)

# Run assistant
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id
)

# Wait for completion
import time
while run.status != "completed":
    time.sleep(1)
    run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )

# Get response
messages = client.beta.threads.messages.list(thread_id=thread.id)
print(messages.data[0].content[0].text.value)
```

### With File Search

```python
from openai import OpenAI

client = OpenAI()

# Upload files
with open("product_docs.pdf", "rb") as f:
    file = client.files.create(file=f, purpose="assistants")

# Create vector store
vector_store = client.vector_stores.create(
    name="Product Docs",
    file_ids=[file.id]
)

# Create assistant with file search
assistant = client.beta.assistants.create(
    name="Product Expert",
    model="gpt-5.4",
    tools=[
        {
            "type": "file_search",
            "file_search": {
                "vector_store_ids": [vector_store.id]
            }
        }
    ]
)

# Use assistant
thread = client.beta.threads.create()
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="What are the main features?"
)

run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant.id
)

if run.status == "completed":
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    print(messages.data[0].content[0].text.value)
```

### Function Calling

```python
from openai import OpenAI
import json

client = OpenAI()

# Define function
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather for location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"}
                },
                "required": ["location"]
            }
        }
    }
]

# Create assistant
assistant = client.beta.assistants.create(
    model="gpt-5.4",
    tools=tools
)

# Create thread and message
thread = client.beta.threads.create()
client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="What's the weather in Paris?"
)

# Run
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id
)

# Poll for function call
import time
while run.status != "requires_action":
    time.sleep(1)
    run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

# Execute function
tool_call = run.required_action.submit_tool_outputs.tool_calls[0]
function_args = json.loads(tool_call.function.arguments)
weather_result = "Sunny, 22°C"  # Simulate API call

# Submit output
run = client.beta.threads.runs.submit_tool_outputs(
    thread_id=thread.id,
    run_id=run.id,
    tool_outputs=[
        {
            "tool_call_id": tool_call.id,
            "output": weather_result
        }
    ]
)

# Wait for completion
while run.status != "completed":
    time.sleep(1)
    run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

messages = client.beta.threads.messages.list(thread_id=thread.id)
print(messages.data[0].content[0].text.value)
```

### Streaming

```python
from openai import OpenAI

client = OpenAI()

assistant = client.beta.assistants.create(
    model="gpt-5.4",
    instructions="You are a helpful assistant."
)

thread = client.beta.threads.create()
client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Tell me a story"
)

# Stream run
with client.beta.threads.runs.stream(
    thread_id=thread.id,
    assistant_id=assistant.id
) as stream:
    for event in stream:
        if event.event == "thread.message.delta":
            print(event.data.delta.content[0].text.value, end="", flush=True)
```

### Production Assistant Manager

```python
from openai import OpenAI
import time
from typing import List, Dict, Optional

class AssistantManager:
    def __init__(self):
        self.client = OpenAI()
    
    def create_assistant(
        self,
        name: str,
        instructions: str,
        model: str = "gpt-5.4",
        tools: List[dict] = None
    ) -> str:
        """Create assistant"""
        assistant = self.client.beta.assistants.create(
            name=name,
            instructions=instructions,
            model=model,
            tools=tools or []
        )
        return assistant.id
    
    def chat(
        self,
        assistant_id: str,
        message: str,
        thread_id: Optional[str] = None
    ) -> Dict:
        """Send message and get response"""
        # Create or use existing thread
        if not thread_id:
            thread = self.client.beta.threads.create()
            thread_id = thread.id
        
        # Add message
        self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message
        )
        
        # Run assistant
        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=thread_id,
            assistant_id=assistant_id
        )
        
        if run.status == "completed":
            messages = self.client.beta.threads.messages.list(thread_id=thread_id)
            response = messages.data[0].content[0].text.value
            
            return {
                "response": response,
                "thread_id": thread_id,
                "run_id": run.id
            }
        else:
            return {
                "error": f"Run status: {run.status}",
                "thread_id": thread_id
            }
    
    def multi_turn_chat(
        self,
        assistant_id: str,
        messages: List[str]
    ) -> List[str]:
        """Multi-turn conversation"""
        thread = self.client.beta.threads.create()
        responses = []
        
        for msg in messages:
            result = self.chat(assistant_id, msg, thread.id)
            if "response" in result:
                responses.append(result["response"])
        
        return responses
    
    def list_assistants(self) -> List[Dict]:
        """List all assistants"""
        assistants = self.client.beta.assistants.list()
        
        return [
            {
                "id": a.id,
                "name": a.name,
                "model": a.model,
                "tools": [t.type for t in a.tools]
            }
            for a in assistants.data
        ]

# Usage
manager = AssistantManager()

# Create assistant
assistant_id = manager.create_assistant(
    name="Customer Support",
    instructions="You are a helpful customer support agent.",
    tools=[{"type": "file_search"}]
)

# Single message
result = manager.chat(
    assistant_id=assistant_id,
    message="How do I reset my password?"
)
print(result["response"])

# Multi-turn conversation
conversation = [
    "Hello!",
    "I need help with my account",
    "I forgot my password"
]
responses = manager.multi_turn_chat(assistant_id, conversation)
for i, resp in enumerate(responses):
    print(f"Turn {i+1}: {resp}")
```

## Error Responses

- **404 Not Found** - Assistant, thread, or run not found
- **400 Bad Request** - Invalid parameters
- **429 Too Many Requests** - Rate limit exceeded

## Rate Limiting / Throttling

- **Assistant operations**: Standard rate limits
- **Run execution**: Background processing
- **Message limits**: Max messages per thread

## Differences from Other APIs

- **vs Responses API**: Assistants stateful, Responses stateless
- **vs Chat Completions**: Assistants manage threads automatically
- **vs LangChain Agents**: Built-in vs custom implementation

## Limitations and Known Issues

- **Thread size limits**: Max messages/tokens per thread [COMMUNITY] (OAIAPI-SC-SO-THRLIM)
- **Run timeout**: Long runs may timeout [COMMUNITY] (OAIAPI-SC-SO-RUNTO)
- **Cost tracking**: Complex cost attribution [COMMUNITY] (OAIAPI-SC-SO-ASTCOST)

## Gotchas and Quirks

- **Async runs**: Must poll, no blocking API [VERIFIED] (OAIAPI-SC-OAI-RUNCRT)
- **Message ordering**: Newest first in list [VERIFIED] (OAIAPI-SC-OAI-MSGLST)
- **Thread persistence**: Threads never auto-delete [VERIFIED] (OAIAPI-SC-OAI-THRCRT)

## Sources

- OAIAPI-SC-OAI-ASTCRT - POST Create assistant
- OAIAPI-SC-OAI-THRCRT - POST Create thread
- OAIAPI-SC-OAI-MSGCRT - POST Create message
- OAIAPI-SC-OAI-RUNCRT - POST Create run
- OAIAPI-SC-OAI-GASSIST - Assistants guide

## Document History

**[2026-03-20 16:41]**
- Fixed: `client.assistants` -> `client.beta.assistants` per SDK v2.29.0 (all occurrences)
- Fixed: `client.threads` -> `client.beta.threads` per SDK v2.29.0 (all occurrences)

**[2026-03-20 16:12]**
- Initial documentation created
