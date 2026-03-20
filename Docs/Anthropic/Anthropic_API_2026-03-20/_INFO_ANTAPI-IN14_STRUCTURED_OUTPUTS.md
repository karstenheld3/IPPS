# Structured Outputs

**Doc ID**: ANTAPI-IN14
**Goal**: Document JSON mode, strict tool schemas, and output_config.format parameter
**API version**: anthropic-version 2023-06-01

**Depends on:**
- `_INFO_ANTAPI-IN06_MESSAGES.md [ANTAPI-IN06]` for Messages API request schema

## Summary

Structured outputs guarantee schema-compliant JSON responses through constrained decoding. Two mechanisms exist: JSON outputs (`output_config.format` with `type: "json_schema"`) for controlling response format, and strict tool use (`strict: true` on tool schemas) for validated tool inputs. Both eliminate JSON parsing errors, missing fields, and type mismatches. The Python SDK integrates with Pydantic models via `client.messages.parse()` for automatic schema generation and response validation.

## Key Facts

- **JSON Output**: `output_config.format` with `type: "json_schema"`
- **Strict Tools**: `strict: true` on tool input_schema
- **SDK Helper**: `client.messages.parse()` (Python/Pydantic)
- **Guarantee**: Always valid JSON matching schema (constrained decoding)
- **Response Location**: `response.content[0].text` (JSON string)
- **Status**: GA

## JSON Outputs

### Basic Usage

```python
import anthropic
import json

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    output_config={
        "format": {
            "type": "json_schema",
            "json_schema": {
                "name": "lead_info",
                "schema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "email": {"type": "string"},
                        "plan_interest": {"type": "string", "enum": ["Starter", "Pro", "Enterprise"]},
                        "demo_requested": {"type": "boolean"},
                    },
                    "required": ["name", "email", "plan_interest", "demo_requested"],
                },
            },
        }
    },
    messages=[
        {"role": "user", "content": "Extract lead info: John Smith, john@example.com, interested in Enterprise, wants a demo"}
    ],
)

data = json.loads(message.content[0].text)
print(data["name"])  # "John Smith"
```

### With Pydantic (SDK Helper)

```python
import anthropic
from pydantic import BaseModel

client = anthropic.Anthropic()

class LeadInfo(BaseModel):
    name: str
    email: str
    plan_interest: str
    demo_requested: bool

result = client.messages.parse(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    output_format=LeadInfo,
    messages=[
        {"role": "user", "content": "Extract: John Smith, john@example.com, Enterprise plan, wants demo"}
    ],
)

lead = result.parsed  # LeadInfo instance
print(lead.name)  # "John Smith"
print(lead.demo_requested)  # True
```

## Strict Tool Use

### Basic Usage

```python
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=[
        {
            "name": "create_order",
            "description": "Create a new order",
            "input_schema": {
                "type": "object",
                "properties": {
                    "product_id": {"type": "string"},
                    "quantity": {"type": "integer"},
                    "priority": {"type": "string", "enum": ["low", "medium", "high"]},
                },
                "required": ["product_id", "quantity", "priority"],
            },
            "strict": True,  # Guarantees schema validation
        }
    ],
    messages=[{"role": "user", "content": "Order 5 units of SKU-123, high priority"}],
)
```

## JSON Schema Limitations

- `minimum`, `maximum`, `minLength`, `maxLength` constraints not directly enforced (SDK adds to descriptions)
- `additionalProperties: false` is automatically added to all objects
- Limited `format` support for strings
- `pattern` (regex) support varies by feature
- Complex nested schemas may hit compilation limits

## SDK Schema Transformation

Python and TypeScript SDKs automatically:

1. Remove unsupported constraints (minimum, maximum, etc.)
2. Update descriptions with constraint info
3. Add `additionalProperties: false` to all objects
4. Filter string formats to supported list
5. Validate responses against original schema (with all constraints)

## Grammar Compilation and Caching

- First request with a new schema incurs a one-time compilation cost
- Subsequent requests reuse the compiled grammar (cached)
- Schema compilation adds latency on first use

## Gotchas and Quirks

- `output_config.format` replaces the older `output_format` parameter (SDK still accepts both)
- JSON output is returned in `response.content[0].text` as a string; parse with `json.loads()`
- Schema constraints like `minimum`/`maximum` are not enforced by constrained decoding; SDK validates post-generation
- First request with a new schema is slower due to grammar compilation
- Both JSON outputs and strict tools can be used together in the same request
- Not all JSON Schema features are supported; test complex schemas before production use

## Related Endpoints

- `_INFO_ANTAPI-IN06_MESSAGES.md [ANTAPI-IN06]` - Messages API (output_config parameter)
- `_INFO_ANTAPI-IN21_TOOL_USE.md [ANTAPI-IN21]` - Tool use with strict schemas

## Sources

- ANTAPI-SC-ANTH-STRUCT - https://platform.claude.com/docs/en/build-with-claude/structured-outputs - Full structured outputs guide

## Document History

**[2026-03-20 03:15]**
- Initial documentation created from structured outputs guide
