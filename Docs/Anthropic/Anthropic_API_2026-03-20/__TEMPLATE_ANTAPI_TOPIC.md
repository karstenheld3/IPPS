# [TOPIC_TITLE]

**Doc ID**: ANTAPI-IN[NN]
**Goal**: [Single sentence describing what this topic documents]
**API version**: anthropic-version 2023-06-01

**Depends on:**
- `_INFO_ANTAPI-IN01_INTRODUCTION.md [ANTAPI-IN01]` for base URL, auth headers

## Summary

[2-4 sentence overview of this topic. What it does, when to use it, key characteristics.]

## Key Facts

- **Base URL**: `https://api.anthropic.com`
- **Endpoint**: `[METHOD] /v1/[path]`
- **Auth**: `x-api-key` header
- **Status**: [GA | Beta | Legacy/Deprecated]
- **Python SDK**: `client.[resource].[method]()`

## Use Cases

- [Use case 1]
- [Use case 2]
- [Use case 3]

## Quick Reference

```python
import anthropic

client = anthropic.Anthropic()

# [Brief description of what this example does]
response = client.[resource].[method](
    # [key parameters]
)
```

## Endpoints

### [METHOD] /v1/[path] - [Description]

#### Request

**Required Parameters:**

- **[param_name]** (`type`) - Description
- **[param_name]** (`type`) - Description

**Optional Parameters:**

- **[param_name]** (`type`, default: `value`) - Description

**Full Request Body (JSON):**

```json
{
  "[param]": "[value]",
  "[param]": "[value]"
}
```

**Python Example:**

```python
import anthropic

client = anthropic.Anthropic()

response = client.[resource].[method](
    [param]="[value]",
    [param]="[value]",
)
print(response)
```

#### Response

**Response Body (JSON):**

```json
{
  "[field]": "[value]",
  "[field]": "[value]"
}
```

**Response Fields:**

- **[field]** (`type`) - Description
- **[field]** (`type`) - Description

[Repeat ### block for each endpoint in this topic]

## Error Codes

- **400** `invalid_request_error` - [Description]
- **401** `authentication_error` - [Description]
- **[code]** `[type]` - [Description]

## Gotchas and Quirks

- [Non-obvious behavior 1]
- [Non-obvious behavior 2]

## Limitations

- [Limitation 1]
- [Limitation 2]

## Related Endpoints

- `_INFO_ANTAPI-IN[NN]_[NAME].md [ANTAPI-IN[NN]]` - [Relationship]

## Sources

- [ANTAPI-SC-ID] - [URL] - [What was used from this source]

## Document History

**[YYYY-MM-DD HH:MM]**
- Initial documentation created from [sources]
