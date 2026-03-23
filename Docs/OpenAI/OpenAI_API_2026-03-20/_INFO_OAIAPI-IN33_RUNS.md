# Runs API

**Doc ID**: OAIAPI-IN33
**Goal**: Document Runs lifecycle, status flow, streaming, and tool output submission
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references
- `_INFO_OAIAPI-IN31_ASSISTANTS.md [OAIAPI-IN31]` for Assistants context

## Summary

Runs API executes assistants on threads. Create run (POST /v1/threads/{thread_id}/runs) to invoke assistant, poll status (GET /v1/threads/{thread_id}/runs/{run_id}) until complete, submit tool outputs (POST /v1/threads/{thread_id}/runs/{run_id}/submit_tool_outputs) for function calls, and retrieve results. Run lifecycle: queued → in_progress → requires_action → in_progress → completed/failed. Supports streaming via SSE for real-time updates. Run configuration: assistant_id, model override, instructions override, tools override, temperature, etc. Status types: queued, in_progress, requires_action, cancelling, cancelled, failed, completed, expired. Failed runs include error details. Tool calls require submission before run continues. Runs can be cancelled mid-execution. Each run tracks token usage, timestamps, and metadata. Use create_and_poll for simplified polling. [VERIFIED] (OAIAPI-SC-OAI-RUNCRT, OAIAPI-SC-OAI-RUNGET, OAIAPI-SC-OAI-GASSIST)

## Key Facts

- **Purpose**: Execute assistants on threads [VERIFIED] (OAIAPI-SC-OAI-RUNCRT)
- **Async**: Runs execute asynchronously [VERIFIED] (OAIAPI-SC-OAI-RUNCRT)
- **Streaming**: Real-time updates via SSE [VERIFIED] (OAIAPI-SC-OAI-RUNSTRM)
- **Tool execution**: Requires tool output submission [VERIFIED] (OAIAPI-SC-OAI-RUNSBMT)
- **Cancellable**: Can cancel in-progress runs [VERIFIED] (OAIAPI-SC-OAI-RUNCAN)

## Use Cases

- **Assistant execution**: Run assistants on conversations
- **Function calling**: Execute custom functions
- **Streaming responses**: Real-time output
- **Long-running tasks**: Background processing
- **Tool orchestration**: Multi-step tool usage

## Quick Reference

```python
# Create run
POST /v1/threads/{thread_id}/runs
{
  "assistant_id": "asst_abc123"
}

# Poll status
GET /v1/threads/{thread_id}/runs/{run_id}

# Submit tool outputs
POST /v1/threads/{thread_id}/runs/{run_id}/submit_tool_outputs
{
  "tool_outputs": [
    {
      "tool_call_id": "call_123",
      "output": "Result"
    }
  ]
}

# Stream
POST /v1/threads/{thread_id}/runs
{
  "assistant_id": "asst_abc123",
  "stream": true
}
```

## Run Object

```json
{
  "id": "run_abc123",
  "object": "thread.run",
  "created_at": 1234567890,
  "thread_id": "thread_xyz789",
  "assistant_id": "asst_def456",
  "status": "completed",
  "started_at": 1234567891,
  "expires_at": null,
  "cancelled_at": null,
  "failed_at": null,
  "completed_at": 1234567900,
  "last_error": null,
  "model": "gpt-5.4",
  "instructions": "You are a helpful assistant.",
  "tools": [{"type": "code_interpreter"}],
  "metadata": {},
  "usage": {
    "prompt_tokens": 100,
    "completion_tokens": 50,
    "total_tokens": 150
  },
  "temperature": 1.0,
  "max_prompt_tokens": 10000,
  "max_completion_tokens": 2000
}
```

## Run Status Lifecycle

```
Created → queued → in_progress → completed
                             ↓
                      requires_action (function call)
                             ↓
                      submit tool outputs
                             ↓
                      in_progress → completed
```

### Status Values

- **queued**: Waiting to start
- **in_progress**: Currently executing
- **requires_action**: Waiting for tool outputs
- **cancelling**: Cancellation in progress
- **cancelled**: Run cancelled
- **failed**: Run failed with error
- **completed**: Successfully completed
- **expired**: Run expired (10 minutes)

## Run Operations

### Create Run

```
POST /v1/threads/{thread_id}/runs
```

**Request:**
```json
{
  "assistant_id": "asst_abc123",
  "model": "gpt-5.4",
  "instructions": "Override instructions",
  "tools": [{"type": "code_interpreter"}],
  "metadata": {"request_id": "req_123"}
}
```

### Create and Poll

Simplified API that polls automatically:

```python
run = client.beta.threads.runs.create_and_poll(
    thread_id=thread_id,
    assistant_id=assistant_id
)
```

### Retrieve Run

```
GET /v1/threads/{thread_id}/runs/{run_id}
```

### List Runs

```
GET /v1/threads/{thread_id}/runs
```

### Modify Run

Update metadata only:
```
POST /v1/threads/{thread_id}/runs/{run_id}
{
  "metadata": {"status": "reviewed"}
}
```

### Cancel Run

```
POST /v1/threads/{thread_id}/runs/{run_id}/cancel
```

### Submit Tool Outputs

```
POST /v1/threads/{thread_id}/runs/{run_id}/submit_tool_outputs
{
  "tool_outputs": [
    {
      "tool_call_id": "call_abc123",
      "output": "Function result"
    }
  ]
}
```

## Streaming

### Server-Sent Events

Stream run execution in real-time:

```python
with client.beta.threads.runs.stream(
    thread_id=thread_id,
    assistant_id=assistant_id
) as stream:
    for event in stream:
        if event.event == "thread.message.delta":
            print(event.data.delta.content[0].text.value)
```

### Stream Events

- **thread.run.created**: Run created
- **thread.run.queued**: Run queued
- **thread.run.in_progress**: Run started
- **thread.run.requires_action**: Needs tool outputs
- **thread.run.completed**: Run finished
- **thread.message.created**: New message
- **thread.message.delta**: Message chunk
- **thread.message.completed**: Message done

## Tool Execution Flow

### 1. Run Created

```python
run = client.beta.threads.runs.create(
    thread_id=thread_id,
    assistant_id=assistant_id
)
```

### 2. Poll Until Action Required

```python
while run.status != "requires_action":
    run = client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run.id
    )
```

### 3. Execute Tools

```python
tool_calls = run.required_action.submit_tool_outputs.tool_calls
outputs = []

for call in tool_calls:
    result = execute_function(call.function.name, call.function.arguments)
    outputs.append({
        "tool_call_id": call.id,
        "output": result
    })
```

### 4. Submit Outputs

```python
run = client.beta.threads.runs.submit_tool_outputs(
    thread_id=thread_id,
    run_id=run.id,
    tool_outputs=outputs
)
```

### 5. Poll to Completion

```python
while run.status != "completed":
    run = client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run.id
    )
```

## SDK Examples (Python)

### Basic Run

```python
from openai import OpenAI
import time

client = OpenAI()

# Create run
run = client.beta.threads.runs.create(
    thread_id="thread_abc123",
    assistant_id="asst_def456"
)

# Poll until complete
while run.status != "completed":
    time.sleep(1)
    run = client.beta.threads.runs.retrieve(
        thread_id="thread_abc123",
        run_id=run.id
    )
    print(f"Status: {run.status}")

print("Run completed")
```

### Create and Poll

```python
from openai import OpenAI

client = OpenAI()

run = client.beta.threads.runs.create_and_poll(
    thread_id="thread_abc123",
    assistant_id="asst_def456"
)

if run.status == "completed":
    messages = client.beta.threads.messages.list(thread_id="thread_abc123")
    print(messages.data[0].content[0].text.value)
```

### With Function Calling

```python
from openai import OpenAI
import json

client = OpenAI()

def execute_function(name, arguments):
    """Execute function based on name"""
    args = json.loads(arguments)
    
    if name == "get_weather":
        return f"Weather in {args['location']}: Sunny, 22°C"
    
    return "Unknown function"

# Create run
run = client.beta.threads.runs.create(
    thread_id="thread_abc123",
    assistant_id="asst_def456"
)

# Wait for action required
while run.status != "requires_action":
    if run.status in ["completed", "failed", "cancelled"]:
        break
    run = client.beta.threads.runs.retrieve(
        thread_id="thread_abc123",
        run_id=run.id
    )

# Execute functions
if run.status == "requires_action":
    tool_outputs = []
    
    for call in run.required_action.submit_tool_outputs.tool_calls:
        result = execute_function(call.function.name, call.function.arguments)
        tool_outputs.append({
            "tool_call_id": call.id,
            "output": result
        })
    
    # Submit outputs
    run = client.beta.threads.runs.submit_tool_outputs(
        thread_id="thread_abc123",
        run_id=run.id,
        tool_outputs=tool_outputs
    )
    
    # Wait for completion
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(
            thread_id="thread_abc123",
            run_id=run.id
        )
```

### Streaming Run

```python
from openai import OpenAI

client = OpenAI()

with client.beta.threads.runs.stream(
    thread_id="thread_abc123",
    assistant_id="asst_def456"
) as stream:
    for event in stream:
        if event.event == "thread.message.delta":
            delta = event.data.delta.content
            if delta:
                print(delta[0].text.value, end="", flush=True)
```

### Cancel Run

```python
from openai import OpenAI

client = OpenAI()

run = client.beta.threads.runs.cancel(
    thread_id="thread_abc123",
    run_id="run_xyz789"
)

print(f"Run status: {run.status}")
```

### List Thread Runs

```python
from openai import OpenAI

client = OpenAI()

runs = client.beta.threads.runs.list(thread_id="thread_abc123")

for run in runs.data:
    print(f"{run.id}: {run.status} - {run.usage.total_tokens} tokens")
```

### Production Run Manager

```python
from openai import OpenAI
import time
import json
from typing import Dict, List, Callable, Optional

class RunManager:
    def __init__(self):
        self.client = OpenAI()
    
    def execute_run(
        self,
        thread_id: str,
        assistant_id: str,
        tool_executor: Optional[Callable] = None,
        timeout: int = 300
    ) -> Dict:
        """Execute run with tool handling"""
        # Create run
        run = self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )
        
        start_time = time.time()
        
        while True:
            # Check timeout
            if time.time() - start_time > timeout:
                self.client.beta.threads.runs.cancel(
                    thread_id=thread_id,
                    run_id=run.id
                )
                return {"error": "Timeout", "run_id": run.id}
            
            # Get current status
            run = self.client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )
            
            # Handle different statuses
            if run.status == "completed":
                return {
                    "status": "completed",
                    "run_id": run.id,
                    "usage": {
                        "total_tokens": run.usage.total_tokens,
                        "prompt_tokens": run.usage.prompt_tokens,
                        "completion_tokens": run.usage.completion_tokens
                    }
                }
            
            elif run.status == "requires_action":
                if not tool_executor:
                    return {"error": "Tool execution required but no executor provided"}
                
                # Execute tools
                tool_outputs = []
                for call in run.required_action.submit_tool_outputs.tool_calls:
                    result = tool_executor(call.function.name, call.function.arguments)
                    tool_outputs.append({
                        "tool_call_id": call.id,
                        "output": result
                    })
                
                # Submit outputs
                run = self.client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread_id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )
            
            elif run.status == "failed":
                return {
                    "error": "Run failed",
                    "details": run.last_error,
                    "run_id": run.id
                }
            
            elif run.status in ["cancelled", "expired"]:
                return {
                    "error": f"Run {run.status}",
                    "run_id": run.id
                }
            
            # Continue polling
            time.sleep(1)
    
    def stream_run(
        self,
        thread_id: str,
        assistant_id: str,
        on_text: Callable[[str], None]
    ):
        """Stream run with text callback"""
        with self.client.beta.threads.runs.stream(
            thread_id=thread_id,
            assistant_id=assistant_id
        ) as stream:
            for event in stream:
                if event.event == "thread.message.delta":
                    if event.data.delta.content:
                        text = event.data.delta.content[0].text.value
                        on_text(text)
    
    def get_run_stats(self, thread_id: str) -> Dict:
        """Get statistics for all runs in thread"""
        runs = self.client.beta.threads.runs.list(thread_id=thread_id)
        
        stats = {
            "total_runs": len(runs.data),
            "completed": 0,
            "failed": 0,
            "cancelled": 0,
            "total_tokens": 0
        }
        
        for run in runs.data:
            stats[run.status] = stats.get(run.status, 0) + 1
            if run.usage:
                stats["total_tokens"] += run.usage.total_tokens
        
        return stats

# Usage
manager = RunManager()

def my_tool_executor(name, arguments):
    args = json.loads(arguments)
    if name == "get_data":
        return json.dumps({"data": "result"})
    return "Unknown function"

# Execute with tools
result = manager.execute_run(
    thread_id="thread_abc123",
    assistant_id="asst_def456",
    tool_executor=my_tool_executor,
    timeout=300
)

if "error" not in result:
    print(f"Run completed: {result['usage']['total_tokens']} tokens")

# Stream run
def on_text(text):
    print(text, end="", flush=True)

manager.stream_run(
    thread_id="thread_abc123",
    assistant_id="asst_def456",
    on_text=on_text
)

# Get stats
stats = manager.get_run_stats("thread_abc123")
print(f"\nThread stats: {stats}")
```

## Error Responses

- **404 Not Found** - Thread or run not found
- **400 Bad Request** - Invalid parameters
- **429 Too Many Requests** - Rate limit exceeded

## Rate Limiting / Throttling

- **Run creation**: Standard rate limits
- **Concurrent runs**: Limited per organization
- **Token usage**: Counts toward TPM limits

## Differences from Other APIs

- **vs Direct API calls**: Runs manage async execution
- **vs Batch API**: Runs for interactive, Batch for bulk
- **vs Streaming completions**: Higher-level abstraction

## Limitations and Known Issues

- **10 minute timeout**: Runs expire after 10 minutes [VERIFIED] (OAIAPI-SC-OAI-RUNCRT)
- **No pause/resume**: Cannot pause in-progress runs [COMMUNITY] (OAIAPI-SC-SO-RUNPAUSE)
- **Tool output size**: Limited tool output size [COMMUNITY] (OAIAPI-SC-SO-TOOLSIZE)

## Gotchas and Quirks

- **Async only**: No synchronous run API [VERIFIED] (OAIAPI-SC-OAI-RUNCRT)
- **Polling required**: Must poll or stream [VERIFIED] (OAIAPI-SC-OAI-RUNCRT)
- **Tool outputs required**: Run blocks until submitted [VERIFIED] (OAIAPI-SC-OAI-RUNSBMT)

## Sources

- OAIAPI-SC-OAI-RUNCRT - POST Create run
- OAIAPI-SC-OAI-RUNGET - GET Retrieve run
- OAIAPI-SC-OAI-RUNSBMT - POST Submit tool outputs
- OAIAPI-SC-OAI-RUNCAN - POST Cancel run
- OAIAPI-SC-OAI-RUNSTRM - Streaming runs
- OAIAPI-SC-OAI-GASSIST - Assistants guide

## Document History

**[2026-03-20 16:41]**
- Fixed: `client.threads` -> `client.beta.threads` per SDK v2.29.0 (all occurrences)

**[2026-03-20 16:17]**
- Initial documentation created
