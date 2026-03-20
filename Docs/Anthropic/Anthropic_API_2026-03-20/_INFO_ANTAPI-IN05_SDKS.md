# Client SDKs

**Doc ID**: ANTAPI-IN05
**Goal**: Document official SDK installation, configuration, and usage patterns with focus on Python
**API version**: anthropic-version 2023-06-01

**Depends on:**
- `_INFO_ANTAPI-IN01_INTRODUCTION.md [ANTAPI-IN01]` for base URL and general overview
- `_INFO_ANTAPI-IN02_AUTHENTICATION.md [ANTAPI-IN02]` for API key configuration

## Summary

Anthropic provides official client SDKs in 7 languages: Python, TypeScript, Java, Go, Ruby, C#, and PHP. All SDKs handle authentication headers, request formatting, error handling, retries, streaming, and timeouts automatically. The Python SDK (`anthropic` package) provides sync and async clients with Pydantic models. SDKs support direct API, Amazon Bedrock, Google Vertex AI, and Microsoft Foundry platforms.

## Key Facts

- **Python Package**: `anthropic` (pip install anthropic)
- **Env Variable**: `ANTHROPIC_API_KEY`
- **Sync Client**: `anthropic.Anthropic()`
- **Async Client**: `anthropic.AsyncAnthropic()`
- **Beta Namespace**: `client.beta.messages.create()`
- **GitHub**: https://github.com/anthropics/anthropic-sdk-python

## Available SDKs

- **Python** - Sync and async clients, Pydantic models
- **TypeScript** - Node.js, Deno, Bun, and browser support
- **Java** - Builder pattern, CompletableFuture async
- **Go** - Context-based cancellation, functional options
- **Ruby** - Sorbet types, streaming helpers
- **C#** - .NET Standard 2.0+, IChatClient integration
- **PHP** - Value objects, builder pattern

## Python SDK

### Installation

```python
pip install anthropic
```

### Basic Usage

```python
import anthropic

# Reads ANTHROPIC_API_KEY from environment
client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude"}],
)
print(message.content[0].text)
```

### Async Usage

```python
import anthropic
import asyncio

async def main():
    client = anthropic.AsyncAnthropic()

    message = await client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello, Claude"}],
    )
    print(message.content[0].text)

asyncio.run(main())
```

### Streaming

```python
import anthropic

client = anthropic.Anthropic()

with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Tell me a story"}],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

### Streaming with Final Message

```python
import anthropic

client = anthropic.Anthropic()

# Get complete message without event-handling code
with client.messages.stream(
    max_tokens=128000,
    messages=[{"role": "user", "content": "Write a detailed analysis..."}],
    model="claude-sonnet-4-20250514",
) as stream:
    message = stream.get_final_message()
print(message.content[0].text)
```

### Beta Features

```python
import anthropic

client = anthropic.Anthropic()

# Access beta features via beta namespace
response = client.beta.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}],
    betas=["files-api-2025-04-14"],
)
```

### Error Handling

```python
import anthropic

client = anthropic.Anthropic()

try:
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello"}],
    )
except anthropic.AuthenticationError as e:
    print(f"Auth failed: {e}")
except anthropic.RateLimitError as e:
    print(f"Rate limited: {e}")
except anthropic.APIStatusError as e:
    print(f"API error {e.status_code}: {e.message}")
```

### Request ID Access

```python
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}],
)
print(f"Request ID: {message._request_id}")
```

### Platform Configuration

```python
import anthropic

# Amazon Bedrock
client = anthropic.AnthropicBedrock()

# Google Vertex AI
client = anthropic.AnthropicVertex(
    project_id="your-project",
    region="us-east5",
)
```

## SDK Benefits Over Raw HTTP

- Automatic header management (x-api-key, anthropic-version, content-type)
- Type-safe request and response handling (Pydantic models in Python)
- Built-in retry logic with exponential backoff for transient errors
- Streaming support with high-level helpers
- Request timeout management and TCP keep-alive
- 10-minute timeout validation for non-streaming requests

## GitHub Repositories

- **Python**: https://github.com/anthropics/anthropic-sdk-python
- **TypeScript**: https://github.com/anthropics/anthropic-sdk-typescript
- **Java**: https://github.com/anthropics/anthropic-sdk-java
- **Go**: https://github.com/anthropics/anthropic-sdk-go
- **Ruby**: https://github.com/anthropics/anthropic-sdk-ruby
- **C#**: https://github.com/anthropics/anthropic-sdk-csharp
- **PHP**: https://github.com/anthropics/anthropic-sdk-php

## Gotchas and Quirks

- The Python SDK uses `_request_id` (with underscore prefix) to access the request ID
- `client.messages.stream()` is a context manager; use `with` statement
- Beta features require the `beta` namespace: `client.beta.messages.create()`
- SDKs validate non-streaming requests against a 10-minute timeout
- Bedrock and Vertex AI clients use different authentication mechanisms but same API surface

## Related Endpoints

- `_INFO_ANTAPI-IN01_INTRODUCTION.md [ANTAPI-IN01]` - API overview
- `_INFO_ANTAPI-IN02_AUTHENTICATION.md [ANTAPI-IN02]` - API key configuration
- `_INFO_ANTAPI-IN07_STREAMING.md [ANTAPI-IN07]` - Streaming details

## Sources

- ANTAPI-SC-ANTH-SDKOVW - https://platform.claude.com/docs/en/api/client-sdks - SDK overview, platform support, repos
- ANTAPI-SC-ANTH-SDKPY - https://platform.claude.com/docs/en/api/sdks/python - Python SDK details
- ANTAPI-SC-GH-SDKPY - https://github.com/anthropics/anthropic-sdk-python - SDK source, api.md

## Document History

**[2026-03-20 02:22]**
- Initial documentation created from SDK overview and Python SDK pages
