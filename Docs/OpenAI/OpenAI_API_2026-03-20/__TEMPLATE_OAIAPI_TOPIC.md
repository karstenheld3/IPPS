# [TOPIC_TITLE]

**Doc ID**: OAIAPI-IN[XX]
**Goal**: [Single sentence describing what this topic documents]
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references
- [List any other topic dependencies]

## Summary

[5-15 sentences covering all key facts about this topic. Include: purpose, main endpoints/features, key parameters, important limitations. Scale with complexity. This should be copy/paste ready.]

## Key Facts

- **[Fact 1]** [VERIFIED] (OAIAPI-SC-[SOURCE])
- **[Fact 2]** [VERIFIED] (OAIAPI-SC-[SOURCE])
- **[Fact N]** [VERIFIED/ASSUMED/COMMUNITY] (OAIAPI-SC-[SOURCE])

## Use Cases

- **[Use case 1]**: [Description]
- **[Use case 2]**: [Description]

## Quick Reference

[One-screen lookup table/list for this topic. Include endpoint URLs, key parameters, common patterns.]

```
[METHOD] /v1/[endpoint]
Headers: Authorization: Bearer $OPENAI_API_KEY
Content-Type: application/json
```

## [Main Section 1: e.g., Request Schema]

### [Subsection]

[Detailed content following TOC structure]

## [Main Section 2: e.g., Response Schema]

### [Subsection]

[Detailed content]

## [Main Section N]

[Additional sections as needed per topic]

## SDK Examples (Python)

### [Example 1 Title]

```python
from openai import OpenAI

client = OpenAI()

# [Description of what this example does]
response = client.[method](
    # [parameters]
)
print(response)
```

### [Example 2 Title - Production-Ready]

```python
from openai import OpenAI
import time

client = OpenAI()

# [Production-ready example with error handling, retries, etc.]
try:
    response = client.[method](
        # [parameters]
    )
except Exception as e:
    # [Error handling]
    print(f"Error: {e}")
```

## Error Responses

- **400 Bad Request** - [Common cause and resolution]
- **401 Unauthorized** - [Common cause and resolution]
- **403 Forbidden** - [Common cause and resolution]
- **429 Too Many Requests** - [Rate limit exceeded, retry with backoff]
- **500 Internal Server Error** - [Retry with exponential backoff]

## Rate Limiting / Throttling

- **Applicable rate limits**: [RPM/TPM for this endpoint]
- **Headers**: x-ratelimit-limit-requests, x-ratelimit-remaining-requests, x-ratelimit-reset-requests
- **Retry strategy**: [Exponential backoff recommendation]

## Differences from Other APIs

- **vs Anthropic**: [Key differences for this topic]
- **vs Gemini**: [Key differences for this topic]
- **vs Grok**: [Key differences for this topic]

## Limitations and Known Issues

- [Limitation 1] [VERIFIED/COMMUNITY] (OAIAPI-SC-[SOURCE])
- [Limitation 2] [VERIFIED/COMMUNITY] (OAIAPI-SC-[SOURCE])

## Gotchas and Quirks

- [Gotcha 1 - undocumented behavior or edge case] [COMMUNITY] (OAIAPI-SC-[SOURCE])

## Sources

- OAIAPI-SC-[SOURCE1] - [Brief description]
- OAIAPI-SC-[SOURCE2] - [Brief description]

## Document History

**[YYYY-MM-DD HH:MM]**
- Initial documentation created

<!-- Template Instructions (delete when using):
1. Replace all [PLACEHOLDERS] with actual values
2. [XX] = sequential Doc ID number matching TOC (01, 02, 03...)
3. Summary must be 5-15 sentences, copy/paste ready
4. All claims must have verification labels: [VERIFIED], [ASSUMED], [TESTED], [PROVEN], [COMMUNITY]
5. All sources must use IDs from __OAIAPI_SOURCES.md
6. SDK examples must be syntactically correct Python
7. Include at least one production-ready example with error handling
8. Error Responses section: document all applicable HTTP status codes
9. Rate Limiting section: populate or note "not applicable"
10. Differences section: compare with Anthropic, Gemini, Grok for this specific topic
11. Limitations: include community-sourced issues with citations
12. No Markdown tables - use lists per core conventions
13. No emojis
14. Delete this comment block when creating actual topic file
-->
