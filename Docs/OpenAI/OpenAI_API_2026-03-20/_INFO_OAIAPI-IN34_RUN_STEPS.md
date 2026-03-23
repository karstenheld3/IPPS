# Run Steps API

**Doc ID**: OAIAPI-IN34
**Goal**: Document Run Steps for detailed execution traces, tool usage, and debugging
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references
- `_INFO_OAIAPI-IN33_RUNS.md [OAIAPI-IN33]` for Runs context

## Summary

Run Steps API provides detailed execution trace for assistant runs. Retrieve steps (GET /v1/threads/{thread_id}/runs/{run_id}/steps) to inspect individual operations within run: message creation, tool calls (code_interpreter, file_search, function). Each step has type, status, and detailed information about operation. Step types: message_creation (assistant message), tool_calls (tools executed). Tool call details include input, output, and execution status. Use for debugging, monitoring, auditing tool usage. Steps created automatically during run execution. Step statuses: in_progress, completed, failed, cancelled, expired. Code interpreter steps include input code, outputs, generated files. File search steps show queries and retrieved chunks. Function steps include function name, arguments, output. Steps ordered chronologically. Essential for understanding complex multi-tool runs. [VERIFIED] (OAIAPI-SC-OAI-STPLST, OAIAPI-SC-OAI-STPGET, OAIAPI-SC-OAI-GASSIST)

## Key Facts

- **Purpose**: Detailed run execution trace [VERIFIED] (OAIAPI-SC-OAI-STPLST)
- **Types**: message_creation, tool_calls [VERIFIED] (OAIAPI-SC-OAI-STPGET)
- **Automatic**: Created during run execution [VERIFIED] (OAIAPI-SC-OAI-GASSIST)
- **Debugging**: Inspect tool inputs/outputs [VERIFIED] (OAIAPI-SC-OAI-STPLST)
- **Chronological**: Steps ordered by execution [VERIFIED] (OAIAPI-SC-OAI-STPLST)

## Use Cases

- **Debugging**: Understand run failures
- **Monitoring**: Track tool usage
- **Auditing**: Log tool executions
- **Cost analysis**: Attribute token usage to steps
- **Optimization**: Identify slow operations

## Quick Reference

```python
# List steps
GET /v1/threads/{thread_id}/runs/{run_id}/steps

# Retrieve step
GET /v1/threads/{thread_id}/runs/{run_id}/steps/{step_id}
```

## Run Step Object

```json
{
  "id": "step_abc123",
  "object": "thread.run.step",
  "created_at": 1234567890,
  "run_id": "run_xyz789",
  "thread_id": "thread_def456",
  "type": "tool_calls",
  "status": "completed",
  "step_details": {
    "type": "tool_calls",
    "tool_calls": [
      {
        "id": "call_abc",
        "type": "code_interpreter",
        "code_interpreter": {
          "input": "print(2 + 2)",
          "outputs": [
            {
              "type": "logs",
              "logs": "4\n"
            }
          ]
        }
      }
    ]
  },
  "usage": {
    "prompt_tokens": 50,
    "completion_tokens": 25,
    "total_tokens": 75
  }
}
```

## Step Types

### message_creation

Assistant created message:
```json
{
  "type": "message_creation",
  "message_creation": {
    "message_id": "msg_abc123"
  }
}
```

### tool_calls

Tools executed:
```json
{
  "type": "tool_calls",
  "tool_calls": [
    {
      "id": "call_1",
      "type": "code_interpreter",
      "code_interpreter": {...}
    },
    {
      "id": "call_2",
      "type": "file_search",
      "file_search": {...}
    },
    {
      "id": "call_3",
      "type": "function",
      "function": {...}
    }
  ]
}
```

## Tool Call Details

### code_interpreter

```json
{
  "type": "code_interpreter",
  "code_interpreter": {
    "input": "import pandas as pd\ndf = pd.read_csv('data.csv')\nprint(df.head())",
    "outputs": [
      {
        "type": "logs",
        "logs": "   col1  col2\n0     1     2\n..."
      },
      {
        "type": "image",
        "image": {
          "file_id": "file_generated_123"
        }
      }
    ]
  }
}
```

**Output types:**
- **logs**: Text output
- **image**: Generated image

### file_search

```json
{
  "type": "file_search",
  "file_search": {
    "ranking_options": {
      "score_threshold": 0.5
    },
    "results": [
      {
        "file_id": "file_abc",
        "file_name": "document.pdf",
        "score": 0.85,
        "content": [
          {
            "type": "text",
            "text": "Relevant chunk..."
          }
        ]
      }
    ]
  }
}
```

### function

```json
{
  "type": "function",
  "function": {
    "name": "get_weather",
    "arguments": "{\"location\":\"Paris\"}",
    "output": "{\"temperature\":22,\"conditions\":\"sunny\"}"
  }
}
```

## Step Status

- **in_progress**: Step executing
- **completed**: Step finished
- **failed**: Step failed
- **cancelled**: Run cancelled
- **expired**: Run expired

## Step Operations

### List Steps

```
GET /v1/threads/{thread_id}/runs/{run_id}/steps
```

**Query parameters:**
- **limit**: Number of steps (default 20, max 100)
- **order**: "asc" or "desc" (default "desc")
- **after**: Cursor for pagination
- **before**: Cursor for pagination

### Retrieve Step

```
GET /v1/threads/{thread_id}/runs/{run_id}/steps/{step_id}
```

## SDK Examples (Python)

### List All Steps

```python
from openai import OpenAI

client = OpenAI()

steps = client.beta.threads.runs.steps.list(
    thread_id="thread_abc123",
    run_id="run_xyz789"
)

for step in steps.data:
    print(f"Step {step.id}: {step.type} - {step.status}")
```

### Inspect Tool Calls

```python
from openai import OpenAI

client = OpenAI()

steps = client.beta.threads.runs.steps.list(
    thread_id="thread_abc123",
    run_id="run_xyz789"
)

for step in steps.data:
    if step.type == "tool_calls":
        for tool_call in step.step_details.tool_calls:
            print(f"\nTool: {tool_call.type}")
            
            if tool_call.type == "code_interpreter":
                print(f"Input: {tool_call.code_interpreter.input}")
                print(f"Outputs: {len(tool_call.code_interpreter.outputs)}")
            
            elif tool_call.type == "file_search":
                results = tool_call.file_search.results
                print(f"Results: {len(results)} chunks")
            
            elif tool_call.type == "function":
                print(f"Function: {tool_call.function.name}")
                print(f"Arguments: {tool_call.function.arguments}")
                print(f"Output: {tool_call.function.output}")
```

### Debug Code Interpreter

```python
from openai import OpenAI

client = OpenAI()

steps = client.beta.threads.runs.steps.list(
    thread_id="thread_abc123",
    run_id="run_xyz789"
)

for step in steps.data:
    if step.type == "tool_calls":
        for tool_call in step.step_details.tool_calls:
            if tool_call.type == "code_interpreter":
                code = tool_call.code_interpreter
                
                print("=== Code Executed ===")
                print(code.input)
                
                print("\n=== Outputs ===")
                for output in code.outputs:
                    if output.type == "logs":
                        print(output.logs)
                    elif output.type == "image":
                        print(f"Generated image: {output.image.file_id}")
```

### Track File Search

```python
from openai import OpenAI

client = OpenAI()

steps = client.beta.threads.runs.steps.list(
    thread_id="thread_abc123",
    run_id="run_xyz789"
)

for step in steps.data:
    if step.type == "tool_calls":
        for tool_call in step.step_details.tool_calls:
            if tool_call.type == "file_search":
                results = tool_call.file_search.results
                
                print(f"\n=== File Search: {len(results)} results ===")
                for result in results:
                    print(f"File: {result.file_name}")
                    print(f"Score: {result.score:.2f}")
                    print(f"Content: {result.content[0].text[:100]}...")
```

### Monitor Function Calls

```python
from openai import OpenAI

client = OpenAI()

def monitor_run_functions(thread_id: str, run_id: str):
    """Monitor all function calls in run"""
    steps = client.beta.threads.runs.steps.list(
        thread_id=thread_id,
        run_id=run_id
    )
    
    function_calls = []
    
    for step in steps.data:
        if step.type == "tool_calls":
            for tool_call in step.step_details.tool_calls:
                if tool_call.type == "function":
                    function_calls.append({
                        "step_id": step.id,
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments,
                        "output": tool_call.function.output,
                        "status": step.status
                    })
    
    return function_calls

# Usage
calls = monitor_run_functions("thread_abc123", "run_xyz789")
for call in calls:
    print(f"{call['name']}: {call['status']}")
```

### Calculate Token Usage by Step

```python
from openai import OpenAI

client = OpenAI()

steps = client.beta.threads.runs.steps.list(
    thread_id="thread_abc123",
    run_id="run_xyz789"
)

total_tokens = 0
step_breakdown = []

for step in steps.data:
    if step.usage:
        tokens = step.usage.total_tokens
        total_tokens += tokens
        step_breakdown.append({
            "step_id": step.id,
            "type": step.type,
            "tokens": tokens
        })

print(f"Total tokens: {total_tokens}")
for breakdown in step_breakdown:
    print(f"{breakdown['type']}: {breakdown['tokens']} tokens")
```

### Production Step Analyzer

```python
from openai import OpenAI
from typing import Dict, List

class RunStepAnalyzer:
    def __init__(self):
        self.client = OpenAI()
    
    def get_all_steps(self, thread_id: str, run_id: str) -> List:
        """Get all steps with pagination"""
        all_steps = []
        after = None
        
        while True:
            steps = self.client.beta.threads.runs.steps.list(
                thread_id=thread_id,
                run_id=run_id,
                limit=100,
                order="asc",
                after=after
            )
            
            all_steps.extend(steps.data)
            
            if not steps.has_more:
                break
            
            after = steps.data[-1].id
        
        return all_steps
    
    def analyze_run(self, thread_id: str, run_id: str) -> Dict:
        """Comprehensive run analysis"""
        steps = self.get_all_steps(thread_id, run_id)
        
        analysis = {
            "total_steps": len(steps),
            "message_creations": 0,
            "tool_executions": 0,
            "code_interpreter_calls": 0,
            "file_search_calls": 0,
            "function_calls": 0,
            "total_tokens": 0,
            "failed_steps": [],
            "execution_timeline": []
        }
        
        for step in steps:
            # Count step types
            if step.type == "message_creation":
                analysis["message_creations"] += 1
            elif step.type == "tool_calls":
                analysis["tool_executions"] += 1
                
                for tool_call in step.step_details.tool_calls:
                    if tool_call.type == "code_interpreter":
                        analysis["code_interpreter_calls"] += 1
                    elif tool_call.type == "file_search":
                        analysis["file_search_calls"] += 1
                    elif tool_call.type == "function":
                        analysis["function_calls"] += 1
            
            # Track failures
            if step.status == "failed":
                analysis["failed_steps"].append({
                    "step_id": step.id,
                    "type": step.type
                })
            
            # Token usage
            if step.usage:
                analysis["total_tokens"] += step.usage.total_tokens
            
            # Timeline
            analysis["execution_timeline"].append({
                "step_id": step.id,
                "type": step.type,
                "status": step.status,
                "created_at": step.created_at
            })
        
        return analysis
    
    def extract_code_executions(self, thread_id: str, run_id: str) -> List[Dict]:
        """Extract all code interpreter executions"""
        steps = self.get_all_steps(thread_id, run_id)
        
        executions = []
        
        for step in steps:
            if step.type == "tool_calls":
                for tool_call in step.step_details.tool_calls:
                    if tool_call.type == "code_interpreter":
                        code = tool_call.code_interpreter
                        
                        outputs = []
                        for output in code.outputs:
                            if output.type == "logs":
                                outputs.append({"type": "logs", "content": output.logs})
                            elif output.type == "image":
                                outputs.append({"type": "image", "file_id": output.image.file_id})
                        
                        executions.append({
                            "step_id": step.id,
                            "input": code.input,
                            "outputs": outputs,
                            "status": step.status
                        })
        
        return executions
    
    def extract_file_search_results(self, thread_id: str, run_id: str) -> List[Dict]:
        """Extract all file search results"""
        steps = self.get_all_steps(thread_id, run_id)
        
        searches = []
        
        for step in steps:
            if step.type == "tool_calls":
                for tool_call in step.step_details.tool_calls:
                    if tool_call.type == "file_search":
                        search = tool_call.file_search
                        
                        results = []
                        for result in search.results:
                            results.append({
                                "file_id": result.file_id,
                                "file_name": result.file_name,
                                "score": result.score,
                                "content_preview": result.content[0].text[:200]
                            })
                        
                        searches.append({
                            "step_id": step.id,
                            "results_count": len(results),
                            "results": results
                        })
        
        return searches

# Usage
analyzer = RunStepAnalyzer()

# Comprehensive analysis
analysis = analyzer.analyze_run("thread_abc123", "run_xyz789")
print(f"Total steps: {analysis['total_steps']}")
print(f"Tool executions: {analysis['tool_executions']}")
print(f"Total tokens: {analysis['total_tokens']}")

if analysis['failed_steps']:
    print(f"\nFailed steps: {len(analysis['failed_steps'])}")

# Code executions
code_runs = analyzer.extract_code_executions("thread_abc123", "run_xyz789")
print(f"\nCode interpreter runs: {len(code_runs)}")
for i, run in enumerate(code_runs):
    print(f"\n=== Execution {i+1} ===")
    print(f"Input: {run['input'][:100]}...")
    print(f"Outputs: {len(run['outputs'])}")

# File searches
searches = analyzer.extract_file_search_results("thread_abc123", "run_xyz789")
print(f"\nFile searches: {len(searches)}")
for search in searches:
    print(f"Found {search['results_count']} chunks")
```

## Error Responses

- **404 Not Found** - Thread, run, or step not found
- **400 Bad Request** - Invalid parameters
- **429 Too Many Requests** - Rate limit exceeded

## Rate Limiting / Throttling

- **Step listing**: Standard rate limits
- **Pagination recommended**: For runs with many steps

## Differences from Other APIs

- **vs Run status**: Steps provide granular detail
- **vs Logs**: Structured vs unstructured data
- **vs Traces**: Built-in vs custom tracing

## Limitations and Known Issues

- **No step creation**: Steps auto-created, cannot create manually [VERIFIED] (OAIAPI-SC-OAI-GASSIST)
- **Limited history**: Very old steps may be unavailable [COMMUNITY] (OAIAPI-SC-SO-STPHIST)
- **Large outputs truncated**: Code outputs may be truncated [COMMUNITY] (OAIAPI-SC-SO-STPTRUNC)

## Gotchas and Quirks

- **Newest first**: Steps listed newest first by default [VERIFIED] (OAIAPI-SC-OAI-STPLST)
- **Async creation**: Steps appear during run execution [VERIFIED] (OAIAPI-SC-OAI-GASSIST)
- **Tool call order**: May differ from expected order [COMMUNITY] (OAIAPI-SC-SO-STPORD)

## Sources

- OAIAPI-SC-OAI-STPLST - GET List run steps
- OAIAPI-SC-OAI-STPGET - GET Retrieve run step
- OAIAPI-SC-OAI-GASSIST - Assistants guide

## Document History

**[2026-03-20 16:41]**
- Fixed: `client.threads` -> `client.beta.threads` per SDK v2.29.0 (all occurrences)

**[2026-03-20 16:20]**
- Initial documentation created
