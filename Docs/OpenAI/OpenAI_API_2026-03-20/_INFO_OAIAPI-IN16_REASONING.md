# Reasoning Models

**Doc ID**: OAIAPI-IN16
**Goal**: Document reasoning models (GPT-5, o4-mini, o3-pro), reasoning effort parameter, and thinking budgets
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references
- `_INFO_OAIAPI-IN03_MODELS.md [OAIAPI-IN03]` for model details

## Summary

Reasoning models (GPT-5, o4-mini, o3-pro) perform extended reasoning before generating responses, showing their work through internal thinking process. Control reasoning depth via reasoning.effort parameter with values: none (skip reasoning), low (minimal reasoning), medium (balanced), high (thorough), xhigh (maximum reasoning). Higher effort increases latency and cost but improves accuracy on complex tasks. Reasoning summaries can be included in response output by setting reasoning.include_summaries to true. Models generate thinking tokens not visible to user by default. Thinking budget determines maximum reasoning tokens - models stop reasoning when budget exhausted. Best for math, logic, coding, analysis, problem-solving. Not beneficial for simple tasks like creative writing or basic questions. GPT-5 supports reasoning, o-series specialized for reasoning tasks. [VERIFIED] (OAIAPI-SC-OAI-GREASN)

## Key Facts

- **Models**: GPT-5, o4-mini, o3-pro support reasoning [VERIFIED] (OAIAPI-SC-OAI-GREASN)
- **Effort levels**: none, low, medium, high, xhigh [VERIFIED] (OAIAPI-SC-OAI-GREASN)
- **Thinking tokens**: Internal reasoning not visible by default [VERIFIED] (OAIAPI-SC-OAI-GREASN)
- **Summaries**: Optional reasoning summaries in output [VERIFIED] (OAIAPI-SC-OAI-GREASN)
- **Cost**: Higher effort = more tokens = higher cost [VERIFIED] (OAIAPI-SC-OAI-GREASN)

## Use Cases

- **Complex problem-solving**: Multi-step reasoning tasks
- **Mathematical proofs**: Formal logic and mathematics
- **Code debugging**: Tracing through complex logic
- **Strategic planning**: Analyzing options and trade-offs
- **Research analysis**: Synthesizing information from multiple sources

## Quick Reference

```python
reasoning={
    "effort": "high",  # none, low, medium, high, xhigh
    "include_summaries": True  # Include reasoning in output
}
```

## Reasoning Effort Levels

### none
- **Reasoning**: Disabled, standard text generation
- **Latency**: Fastest
- **Cost**: Lowest
- **Use case**: Simple tasks not requiring reasoning

### low
- **Reasoning**: Minimal, quick analysis
- **Latency**: Fast
- **Cost**: Low
- **Use case**: Straightforward problems with clear solutions

### medium (default)
- **Reasoning**: Balanced reasoning depth
- **Latency**: Moderate
- **Cost**: Moderate
- **Use case**: General problem-solving

### high
- **Reasoning**: Thorough analysis
- **Latency**: Slower
- **Cost**: Higher
- **Use case**: Complex multi-step problems

### xhigh
- **Reasoning**: Maximum reasoning depth
- **Latency**: Slowest
- **Cost**: Highest
- **Use case**: Extremely difficult tasks requiring deep analysis

## Reasoning Configuration

### Basic Configuration

```python
{
    "reasoning": {
        "effort": "medium"
    }
}
```

### With Summaries

```python
{
    "reasoning": {
        "effort": "high",
        "include_summaries": True
    }
}
```

**include_summaries:** When true, response includes reasoning summaries showing model's thinking process.

## Thinking Budget

Models have thinking token budget:
- Budget determines max reasoning tokens
- Models stop reasoning when budget exhausted
- Budget scales with effort level
- Higher effort = larger budget

Budget not directly controllable - managed by effort level.

## SDK Examples (Python)

### Basic Reasoning

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="o4-mini",
    input=[
        {
            "role": "user",
            "content": "Solve: If a train travels 120 km in 2 hours, then speeds up and travels 180 km in the next 2 hours, what was its average speed for the entire journey?"
        }
    ],
    reasoning={
        "effort": "medium"
    }
)

print(response.output[0].content[0].text)
```

### High Effort for Complex Problem

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="o3-pro",
    input=[
        {
            "role": "user",
            "content": "Prove that the square root of 2 is irrational using proof by contradiction. Show all steps clearly."
        }
    ],
    reasoning={
        "effort": "high",
        "include_summaries": True
    }
)

print(response.output[0].content[0].text)
# Includes reasoning summary showing proof steps
```

### Reasoning for Code Analysis

```python
from openai import OpenAI

client = OpenAI()

code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""

response = client.responses.create(
    model="gpt-5.4-mini",
    input=[
        {
            "role": "user",
            "content": f"Analyze this code for bugs and performance issues. Explain your reasoning:\n\n{code}"
        }
    ],
    reasoning={
        "effort": "high",
        "include_summaries": True
    }
)

print(response.output[0].content[0].text)
```

### Comparing Effort Levels

```python
from openai import OpenAI
import time

client = OpenAI()

problem = "Design an efficient algorithm to find the longest palindromic substring in a given string."

for effort in ["low", "medium", "high"]:
    start = time.time()
    
    response = client.responses.create(
        model="o4-mini",
        input=[
            {"role": "user", "content": problem}
        ],
        reasoning={"effort": effort}
    )
    
    elapsed = time.time() - start
    
    print(f"\n=== Effort: {effort} ===")
    print(f"Time: {elapsed:.2f}s")
    print(f"Tokens: {response.usage.total_tokens}")
    print(f"Response length: {len(response.output[0].content[0].text)} chars")
```

### Strategic Decision Making

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="o3-pro",
    input=[
        {
            "role": "user",
            "content": """
            Our startup has $2M in funding. We need to decide between:
            A) Expanding to 3 new markets with limited features
            B) Perfecting product in current market before expansion
            C) Building B2B enterprise features for current market
            
            Consider: runway, competition, team size (12 people), current traction (1000 users, 20% MoM growth).
            Analyze all options thoroughly with pros/cons and recommend one.
            """
        }
    ],
    reasoning={
        "effort": "xhigh",
        "include_summaries": True
    }
)

print(response.output[0].content[0].text)
```

### Reasoning with Conversation State

```python
from openai import OpenAI

client = OpenAI()

# Create conversation
conversation = client.conversations.create()

# Multi-turn reasoning
response1 = client.responses.create(
    model="o4-mini",
    conversation_id=conversation.id,
    input=[
        {
            "role": "user",
            "content": "I'm building a distributed cache. What are the key design considerations?"
        }
    ],
    reasoning={"effort": "high"}
)

print("=== Initial Analysis ===")
print(response1.output[0].content[0].text)

# Follow-up with reasoning
response2 = client.responses.create(
    model="o4-mini",
    conversation_id=conversation.id,
    input=[
        {
            "role": "user",
            "content": "Now compare consistent hashing vs. rendezvous hashing for this use case"
        }
    ],
    reasoning={
        "effort": "high",
        "include_summaries": True
    }
)

print("\n=== Comparison with Reasoning ===")
print(response2.output[0].content[0].text)
```

### Reasoning with Conversation State (SDK v2.29.0 verified)

```python
# Source: openai v2.29.0 - resources/responses/responses.py
# SDK uses conversation={"id": "..."} not conversation_id="..."
from openai import OpenAI

client = OpenAI()

conversation = client.conversations.create()

response1 = client.responses.create(
    model="o4-mini",
    conversation={"id": conversation.id},
    input=[
        {
            "role": "user",
            "content": "I'm building a distributed cache. What are the key design considerations?"
        }
    ],
    reasoning={"effort": "high"}
)

print("=== Initial Analysis ===")
print(response1.output[0].content[0].text)

response2 = client.responses.create(
    model="o4-mini",
    conversation={"id": conversation.id},
    input=[
        {
            "role": "user",
            "content": "Now compare consistent hashing vs. rendezvous hashing for this use case"
        }
    ],
    reasoning={
        "effort": "high",
        "include_summaries": True
    }
)

print("\n=== Comparison with Reasoning ===")
print(response2.output[0].content[0].text)
```

## Error Responses

- **400 Bad Request** - Invalid reasoning configuration
- **Model not supported** - Non-reasoning model with reasoning parameters

## Rate Limiting / Throttling

- **Thinking tokens count**: Internal reasoning tokens count toward TPM limits
- **Higher costs**: Reasoning models typically more expensive
- **Effort impacts limits**: Higher effort consumes more quota

## Differences from Other APIs

- **vs Anthropic extended thinking**: Anthropic has thinking blocks, similar concept
- **vs Gemini thinking mode**: Gemini has no direct equivalent
- **vs o-series (OpenAI legacy)**: Newer o-series have controllable effort

## Limitations and Known Issues

- **Thinking not always visible**: Internal reasoning hidden unless summaries enabled [VERIFIED] (OAIAPI-SC-OAI-GREASN)
- **Effort not guaranteed**: Model may use less reasoning if problem is simple [COMMUNITY] (OAIAPI-SC-SO-REASEFF)
- **Latency variability**: High effort can vary significantly in time [COMMUNITY] (OAIAPI-SC-SO-REASLAT)

## Gotchas and Quirks

- **Simple tasks don't benefit**: Reasoning overhead not worth it for basic questions [VERIFIED] (OAIAPI-SC-OAI-GREASN)
- **Cost multiplier**: Thinking tokens can double or triple costs [COMMUNITY] (OAIAPI-SC-SO-REASCOST)
- **No thinking token visibility**: Can't see raw thinking without summaries [VERIFIED] (OAIAPI-SC-OAI-GREASN)

## Sources

- OAIAPI-SC-OAI-GREASN - Reasoning guide
- OAIAPI-SC-OAI-GMODLS - Models overview

## Document History

**[2026-03-21 09:23]**
- Added: SDK v2.29.0 verified companion for Reasoning with Conversation State (conversation= param)

**[2026-03-20 15:35]**
- Initial documentation created
