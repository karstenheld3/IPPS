# Prompt Engineering

**Doc ID**: OAIAPI-IN24
**Goal**: Document prompt engineering best practices, reusable prompts, and prompt guidance features
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references

## Summary

Prompt engineering covers techniques for crafting effective instructions and inputs for OpenAI models. Key techniques: clear and specific instructions (developer/system messages), few-shot examples (provide input-output pairs), chain-of-thought reasoning (instruct model to think step-by-step), structured output specification (JSON schemas, formats), role-playing (assign persona), and constraint definition (what to do AND what not to do). OpenAI provides Reusable Prompts - dashboard-managed prompt templates with variables that can be referenced by ID in API calls, enabling version control and A/B testing of prompts. Prompt Guidance helps craft better prompts by suggesting improvements. For reasoning models (o3, o4-mini), use developer messages instead of system messages, avoid chain-of-thought instructions (model reasons internally), and set reasoning_effort for cost/quality tradeoff. For vision tasks, provide clear image analysis instructions. For tool use, describe tools precisely with parameter descriptions and examples. [VERIFIED] (OAIAPI-SC-OAI-GPRMPT, OAIAPI-SC-OAI-GPRMGD)

## Key Facts

- **Developer messages**: Replace system messages for o1+ models [VERIFIED] (OAIAPI-SC-OAI-GPRMPT)
- **Few-shot**: Include example input-output pairs in messages [VERIFIED] (OAIAPI-SC-OAI-GPRMPT)
- **Chain-of-thought**: "Think step by step" for complex reasoning [VERIFIED] (OAIAPI-SC-OAI-GPRMPT)
- **Reusable prompts**: Dashboard-managed templates with variables [VERIFIED] (OAIAPI-SC-OAI-GPRMGD)
- **Reasoning models**: Don't instruct to think step-by-step (they do it automatically) [VERIFIED] (OAIAPI-SC-OAI-GPRMPT)
- **Prompt guidance**: AI-assisted prompt improvement [VERIFIED] (OAIAPI-SC-OAI-GPRMGD)

## Core Techniques

### 1. Clear Instructions

```python
# BAD: vague
messages = [{"role": "user", "content": "Help with my code"}]

# GOOD: specific
messages = [
    {"role": "developer", "content": "You are a Python code reviewer. Identify bugs, suggest fixes, and follow PEP 8."},
    {"role": "user", "content": "Review this function for bugs:\ndef calc(x, y):\n  return x/y"}
]
```

### 2. Few-Shot Examples

```python
messages = [
    {"role": "developer", "content": "Classify customer feedback as positive, negative, or neutral."},
    {"role": "user", "content": "Great product, fast shipping!"},
    {"role": "assistant", "content": "positive"},
    {"role": "user", "content": "Item arrived broken."},
    {"role": "assistant", "content": "negative"},
    {"role": "user", "content": "The package came on time."},
    # Model classifies this based on examples
]
```

### 3. Chain-of-Thought (Non-Reasoning Models)

```python
messages = [
    {"role": "developer", "content": "Solve math problems step by step. Show your work."},
    {"role": "user", "content": "If a train travels 120km in 2 hours, and then 180km in 3 hours, what is the average speed for the entire trip?"}
]
```

### 4. Structured Output Specification

```python
messages = [
    {"role": "developer", "content": """Extract product info as JSON:
{"name": string, "price": number, "category": string, "in_stock": boolean}"""},
    {"role": "user", "content": "The MacBook Pro 16-inch starts at $2499 and is currently available in the laptop category."}
]
```

### 5. Constraint Definition

```python
messages = [
    {"role": "developer", "content": """You are a customer service bot for Acme Corp.
Rules:
- Only answer questions about Acme products
- Never discuss competitors
- If unsure, say "Let me connect you with a specialist"
- Keep responses under 3 sentences
- Never make up product features"""},
    {"role": "user", "content": "How does your product compare to CompetitorX?"}
]
```

## Reusable Prompts

Dashboard-managed prompt templates with variable substitution:

```python
from openai import OpenAI

client = OpenAI()

# Reference a reusable prompt by ID
response = client.chat.completions.create(
    model="gpt-5.4",
    messages=[
        {"role": "user", "content": "Analyze this feedback: Great service!"}
    ],
    prompt_id="prompt_abc123",  # Managed in dashboard
    prompt_variables={
        "language": "English",
        "format": "JSON"
    }
)
```

### Reusable Prompts (SDK v2.29.0 verified)

```python
# Source: openai v2.29.0 - resources/responses/responses.py
# prompt_id is NOT a param in chat.completions.create
# Reusable prompts use the Responses API with 'prompt' param
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-4.1",
    prompt={"id": "prompt_abc123"},  # Dashboard-managed prompt
    input=[
        {"role": "user", "content": "Analyze this feedback: Great service!"}
    ]
)

print(response.output[0].content[0].text)
```

## Reasoning Model Tips

For o3, o4-mini, and other reasoning models:

```python
# DON'T: instruct to think step-by-step (they already do)
messages = [
    {"role": "developer", "content": "Think step by step and solve this problem."}  # Unnecessary
]

# DO: set reasoning_effort for cost/quality tradeoff
response = client.chat.completions.create(
    model="o3",
    messages=[
        {"role": "developer", "content": "Solve this complex math problem."},
        {"role": "user", "content": "Prove that there are infinitely many primes."}
    ],
    reasoning_effort="high"  # "low", "medium", "high"
)
```

## SDK Examples (Python)

### Prompt Template Pattern

```python
from openai import OpenAI

client = OpenAI()

def create_analysis_prompt(text: str, analysis_type: str, output_format: str = "JSON"):
    """Reusable prompt template for text analysis"""
    return [
        {
            "role": "developer",
            "content": f"""Perform {analysis_type} analysis on the provided text.
Output format: {output_format}
Be specific and cite evidence from the text.
If information is insufficient, state what's missing."""
        },
        {
            "role": "user",
            "content": text
        }
    ]

# Sentiment analysis
response = client.chat.completions.create(
    model="gpt-5.4",
    messages=create_analysis_prompt(
        "The new update broke everything. Support was unhelpful.",
        "sentiment",
        "JSON with fields: sentiment, confidence, key_phrases"
    ),
    response_format={"type": "json_object"}
)

print(response.choices[0].message.content)
```

## Error Responses

No prompt-engineering-specific errors. Standard API errors apply.

## Differences from Other APIs

- **vs Anthropic**: Similar techniques. Anthropic uses `system` parameter (not in messages). Has explicit XML tag patterns
- **vs Gemini**: Similar techniques. Uses `system_instruction` parameter
- **Reusable prompts**: Unique to OpenAI (dashboard-managed templates with variables)

## Limitations and Known Issues

- **Prompt length**: Longer prompts consume more tokens and cost more [VERIFIED] (OAIAPI-SC-OAI-GPRMPT)
- **Reusable prompts**: Not available in Chat Completions (Responses API only) [ASSUMED]
- **Reasoning models**: Chain-of-thought instructions waste tokens on reasoning models [VERIFIED] (OAIAPI-SC-OAI-GPRMPT)

## Sources

- OAIAPI-SC-OAI-GPRMPT - Prompt Engineering Guide
- OAIAPI-SC-OAI-GPRMGD - Prompt Guidance / Reusable Prompts

## Document History

**[2026-03-21 09:35]**
- Added: SDK v2.29.0 verified companion for Reusable Prompts (prompt= in responses.create, not prompt_id in chat.completions)

**[2026-03-20 19:02]**
- Initial documentation created
