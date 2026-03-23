# Official SDKs

**Doc ID**: OAIAPI-IN46
**Goal**: Document official OpenAI SDKs - Python, TypeScript, .NET, Java, Go, and Agents SDK
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references

## Summary

OpenAI provides official SDKs for Python, TypeScript/Node.js, .NET, Java, and Go. The Python SDK (`openai` package) is the primary SDK with full API coverage including Responses, Chat Completions, Realtime, Files, Vector Stores, Containers, Fine-tuning, and all administrative endpoints. The TypeScript SDK (`openai` npm package) provides equivalent coverage for Node.js and browser environments. The Agents SDK (`openai-agents` for Python, `@openai/agents` for TypeScript) adds higher-level abstractions for building multi-agent systems with tool use, handoffs, guardrails, and tracing. All SDKs handle authentication, retries with exponential backoff, streaming, pagination, and error handling automatically. SDKs are open-source on GitHub. Configuration via environment variable `OPENAI_API_KEY` or constructor parameter. SDKs support organization and project routing via headers. [VERIFIED] (OAIAPI-SC-GH-SDKPY, OAIAPI-SC-GH-AGNTPY)

## Key Facts

- **Python SDK**: `pip install openai` - primary SDK, full API coverage [VERIFIED] (OAIAPI-SC-GH-SDKPY)
- **TypeScript SDK**: `npm install openai` - full API coverage [VERIFIED] (OAIAPI-SC-GH-SDKPY)
- **Agents SDK (Python)**: `pip install openai-agents` - multi-agent framework [VERIFIED] (OAIAPI-SC-GH-AGNTPY)
- **Agents SDK (TypeScript)**: `npm install @openai/agents` [VERIFIED] (OAIAPI-SC-GH-AGNTPY)
- **.NET SDK**: `dotnet add package OpenAI` [VERIFIED] (OAIAPI-SC-GH-SDKREL)
- **Java SDK**: Maven/Gradle package [VERIFIED] (OAIAPI-SC-GH-SDKREL)
- **Go SDK**: `go get github.com/openai/openai-go` [VERIFIED] (OAIAPI-SC-GH-SDKREL)
- **Auto-retry**: All SDKs retry on 429/5xx with exponential backoff [VERIFIED] (OAIAPI-SC-GH-SDKPY)

## Use Cases

- **Application development**: Build AI-powered apps with type-safe API access
- **Multi-agent systems**: Use Agents SDK for orchestrated tool-using agents
- **Streaming applications**: Handle SSE streaming with SDK helpers
- **Production services**: Leverage built-in retry, timeout, and error handling
- **Prototyping**: Quick API exploration with SDK convenience methods

## Quick Reference

```bash
# Python
pip install openai
pip install openai-agents  # Agents SDK

# TypeScript/Node.js
npm install openai
npm install @openai/agents  # Agents SDK

# .NET
dotnet add package OpenAI

# Go
go get github.com/openai/openai-go
```

## Python SDK

### Installation and Configuration

```python
from openai import OpenAI

# Auto-reads OPENAI_API_KEY env var
client = OpenAI()

# Explicit configuration
client = OpenAI(
    api_key="sk-...",
    organization="org-...",
    project="proj-...",
    timeout=60.0,
    max_retries=3
)
```

### Key Features

- **Typed responses**: All API responses are Pydantic models
- **Streaming**: Iterator-based streaming with `.stream()` methods
- **Async support**: `AsyncOpenAI` client for asyncio
- **Auto-pagination**: Iterate over paginated results automatically
- **File uploads**: `client.files.create(file=open(...), purpose=...)`
- **Error handling**: Typed exceptions (`APIError`, `RateLimitError`, etc.)

### Async Client

```python
from openai import AsyncOpenAI
import asyncio

async def main():
    client = AsyncOpenAI()
    
    response = await client.responses.create(
        model="gpt-5.4",
        input="Hello"
    )
    print(response.output_text)

asyncio.run(main())
```

### Streaming

```python
from openai import OpenAI

client = OpenAI()

stream = client.responses.create(
    model="gpt-5.4",
    input="Write a haiku",
    stream=True
)

for event in stream:
    if hasattr(event, 'delta'):
        print(event.delta, end="", flush=True)
```

### Error Handling

```python
from openai import OpenAI, APIError, RateLimitError, APITimeoutError

client = OpenAI()

try:
    response = client.responses.create(
        model="gpt-5.4",
        input="Hello"
    )
except RateLimitError as e:
    print(f"Rate limited. Retry after: {e.response.headers.get('retry-after')}")
except APITimeoutError:
    print("Request timed out")
except APIError as e:
    print(f"API error {e.status_code}: {e.message}")
```

### Auto-Pagination

```python
from openai import OpenAI

client = OpenAI()

# Automatically iterates through all pages
for model in client.models.list():
    print(model.id)
```

## Agents SDK (Python)

### Installation

```bash
pip install openai-agents
```

### Core Concepts

- **Agent**: Configured LLM with instructions, tools, and handoff targets
- **Runner**: Executes agent loops (tool calls, handoffs, guardrails)
- **Handoff**: Transfer control between agents
- **Guardrails**: Input/output validation
- **Tracing**: Built-in observability

### Basic Agent

```python
from agents import Agent, Runner

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
    model="gpt-5.4"
)

result = Runner.run_sync(agent, "What is the capital of France?")
print(result.final_output)
```

### Agent with Tools

```python
from agents import Agent, Runner, function_tool

@function_tool
def get_weather(location: str) -> str:
    """Get current weather for a location"""
    return f"72F and sunny in {location}"

agent = Agent(
    name="Weather Bot",
    instructions="Help users with weather queries.",
    model="gpt-5.4",
    tools=[get_weather]
)

result = Runner.run_sync(agent, "What's the weather in San Francisco?")
print(result.final_output)
```

### Multi-Agent Handoff

```python
from agents import Agent, Runner

sales_agent = Agent(
    name="Sales",
    instructions="Help with product questions and sales.",
    model="gpt-5.4"
)

support_agent = Agent(
    name="Support",
    instructions="Help with technical issues.",
    model="gpt-5.4"
)

triage_agent = Agent(
    name="Triage",
    instructions="Route users to the right agent.",
    model="gpt-5.4",
    handoffs=[sales_agent, support_agent]
)

result = Runner.run_sync(triage_agent, "My product is broken")
print(f"Handled by: {result.last_agent.name}")
print(result.final_output)
```

## TypeScript SDK

### Installation and Usage

```typescript
import OpenAI from 'openai';

const client = new OpenAI();

const response = await client.responses.create({
  model: 'gpt-5.4',
  input: 'Hello',
});

console.log(response.output_text);
```

### Streaming

```typescript
import OpenAI from 'openai';

const client = new OpenAI();

const stream = await client.responses.create({
  model: 'gpt-5.4',
  input: 'Write a poem',
  stream: true,
});

for await (const event of stream) {
  process.stdout.write(event.delta ?? '');
}
```

## SDK Configuration Options

All SDKs support:

- **api_key**: API key (or OPENAI_API_KEY env var)
- **organization**: Organization ID (or OPENAI_ORG_ID env var)
- **project**: Project ID (or OPENAI_PROJECT_ID env var)
- **base_url**: Custom base URL (default: https://api.openai.com/v1)
- **timeout**: Request timeout in seconds
- **max_retries**: Number of retries on failure (default: 2)
- **default_headers**: Additional headers for all requests

## Error Types (Python SDK)

- **APIError**: Base class for all API errors
- **AuthenticationError**: Invalid API key (401)
- **PermissionDeniedError**: Insufficient permissions (403)
- **NotFoundError**: Resource not found (404)
- **UnprocessableEntityError**: Invalid parameters (422)
- **RateLimitError**: Rate limit exceeded (429)
- **InternalServerError**: Server error (500+)
- **APIConnectionError**: Network connectivity issues
- **APITimeoutError**: Request timeout

## Differences from Other APIs

- **vs Anthropic SDK**: `anthropic` Python package. Similar design but different method names (`messages.create` vs `responses.create`). No Agents SDK equivalent
- **vs Gemini SDK**: `google-generativeai` Python package. Different API surface (`generate_content`). Has Vertex AI SDK for enterprise
- **vs Grok SDK**: Uses OpenAI-compatible SDK (`openai` package with custom base_url)
- **Unique**: OpenAI has the most comprehensive SDK ecosystem (6 languages + Agents SDK)

## Limitations and Known Issues

- **Breaking changes**: SDK updates may include breaking changes; pin versions in production [VERIFIED] (OAIAPI-SC-GH-SDKPY)
- **Agents SDK maturity**: Relatively new, API surface may change [VERIFIED] (OAIAPI-SC-GH-AGNTPY)
- **Browser support**: TypeScript SDK works in Node.js; browser usage requires proxying API calls [VERIFIED] (OAIAPI-SC-GH-SDKPY)

## Gotchas and Quirks

- **Env var precedence**: Constructor params override env vars [VERIFIED] (OAIAPI-SC-GH-SDKPY)
- **Retry behavior**: Auto-retries on 429/5xx only; 4xx errors (except 429) are not retried [VERIFIED] (OAIAPI-SC-GH-SDKPY)
- **Streaming types**: Stream events have different types depending on the endpoint used [VERIFIED] (OAIAPI-SC-GH-SDKPY)
- **Agents SDK import**: Import from `agents` not `openai_agents` [VERIFIED] (OAIAPI-SC-GH-AGNTPY)

## Sources

- OAIAPI-SC-GH-SDKPY - OpenAI Python SDK (GitHub)
- OAIAPI-SC-GH-AGNTPY - OpenAI Agents SDK Python (GitHub)
- OAIAPI-SC-GH-SDKREL - SDK release notes

## Document History

**[2026-03-20 18:01]**
- Initial documentation created from GitHub repos and SDK documentation
