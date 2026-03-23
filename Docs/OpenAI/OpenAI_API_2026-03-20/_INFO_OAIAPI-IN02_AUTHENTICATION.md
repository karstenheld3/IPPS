# Authentication

**Doc ID**: OAIAPI-IN02
**Goal**: Document OpenAI API authentication methods, API key management, and multi-organization routing
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references
- `_INFO_OAIAPI-IN01_INTRODUCTION.md [OAIAPI-IN01]` for API overview

## Summary

OpenAI API authentication uses Bearer token authentication with API keys provided via `Authorization: Bearer $OPENAI_API_KEY` header. API keys are managed through the API Dashboard and can be scoped at organization or project level. Three key types exist: user API keys (legacy, organization-wide access), project API keys (recommended, scoped to specific project), and service account API keys (for production, no user association). For multi-organization access or legacy user keys, clients must specify routing via `OpenAI-Organization` and `OpenAI-Project` headers. Organization IDs are found on organization settings page, project IDs on project settings page. All API requests require authentication - missing or invalid keys return 401 Unauthorized. API keys should be stored securely (environment variables, secret management systems) and never hardcoded. [VERIFIED] (OAIAPI-SC-OAI-OVERVIEW, OAIAPI-SC-OAI-ADMOVW)

## Key Facts

- **Authentication method**: Bearer token via `Authorization` header [VERIFIED] (OAIAPI-SC-OAI-OVERVIEW)
- **Key types**: User API keys (legacy), Project API keys (recommended), Service account keys (production) [VERIFIED] (OAIAPI-SC-OAI-ADMOVW)
- **Multi-org routing**: `OpenAI-Organization` and `OpenAI-Project` headers [VERIFIED] (OAIAPI-SC-OAI-OVERVIEW)
- **Key management**: API Dashboard at platform.openai.com [VERIFIED] (OAIAPI-SC-OAI-ADMOVW)
- **Security**: Keys grant full access to account - store securely [VERIFIED] (OAIAPI-SC-OAI-ADMOVW)

## Use Cases

- **Application authentication**: Authenticating API requests from applications
- **Multi-project isolation**: Separating usage and billing across projects
- **Service accounts**: Production deployments without user association
- **Development vs production**: Using different keys for different environments

## Quick Reference

```
Authorization: Bearer $OPENAI_API_KEY

# Optional multi-org routing:
OpenAI-Organization: org-123456
OpenAI-Project: proj-abc123
```

## API Key Types

### User API Keys (Legacy)

- **Scope**: Organization-wide access
- **Use case**: Personal development, legacy applications
- **Limitation**: Access to all projects in organization
- **Status**: Legacy - project API keys recommended for new applications

### Project API Keys (Recommended)

- **Scope**: Single project only
- **Use case**: New applications, project-scoped access control
- **Benefit**: Usage tracked per project, better isolation
- **Location**: API keys page in project settings

### Service Account API Keys

- **Scope**: Project-level, no user association
- **Use case**: Production deployments, CI/CD pipelines
- **Benefit**: Not tied to individual user account
- **Management**: Created through Administration API

## Authentication Headers

### Required: Authorization Header

```
Authorization: Bearer OPENAI_API_KEY
```

All API requests must include this header. The API key can be:
- User API key (legacy)
- Project API key (recommended)
- Service account API key (production)

### Optional: Multi-Organization Routing

For users with access to multiple organizations or using legacy user API keys:

```
OpenAI-Organization: org-123456
OpenAI-Project: proj-abc123
```

**When to use:**
- Multiple organization membership
- Legacy user API keys (instead of project keys)
- Explicit organization/project specification

**Finding IDs:**
- Organization ID: Organization settings page
- Project ID: General settings page (select specific project)

**Effect:**
- Usage counts toward specified organization and project
- Billing applied to that organization
- Rate limits are project-scoped

## API Key Management

### Creating API Keys

1. Navigate to API Dashboard (platform.openai.com)
2. Select organization and project
3. Go to API keys page
4. Click "Create new secret key"
5. Name the key (for identification)
6. Copy key immediately (shown only once)

### Key Security Best Practices

- **Never hardcode keys**: Use environment variables or secret management
- **Rotate keys regularly**: Especially for production environments
- **Delete unused keys**: Remove keys from old projects/environments
- **Use project keys**: Prefer project API keys over user API keys
- **Service accounts for prod**: Use service account keys in production

### Key Storage

**Recommended storage methods:**
- Environment variables (`OPENAI_API_KEY`)
- Secret management systems (AWS Secrets Manager, Azure Key Vault, HashiCorp Vault)
- CI/CD secret stores (GitHub Secrets, GitLab CI/CD variables)

**Never:**
- Commit to version control
- Include in client-side code
- Share via unsecured channels

## SDK Examples (Python)

### Basic Authentication

```python
from openai import OpenAI

# API key loaded from OPENAI_API_KEY environment variable
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### Explicit API Key

```python
from openai import OpenAI

# Explicitly provide API key (not recommended for production)
client = OpenAI(api_key="sk-proj-...")

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### Multi-Organization Routing

```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-...",  # User API key or project key
    organization="org-123456",
    project="proj-abc123"
)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### Production Setup with Environment Variables

```python
import os
from openai import OpenAI

# Load from environment variables
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set")

client = OpenAI(api_key=api_key)

try:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Hello!"}]
    )
except Exception as e:
    print(f"Authentication error: {e}")
```

## Error Responses

- **401 Unauthorized** - Missing or invalid API key
- **403 Forbidden** - API key lacks required permissions for endpoint
- **429 Too Many Requests** - Rate limit exceeded (check project rate limits)

## Rate Limiting / Throttling

- **Rate limits are project-scoped**: Each project has separate RPM/TPM limits
- **Headers indicate limits**: See `x-ratelimit-*` headers in responses
- **Retry strategy**: Implement exponential backoff on 429 responses

## Differences from Other APIs

- **vs Anthropic**: Uses `x-api-key` header instead of `Authorization: Bearer`
- **vs Gemini**: Uses `x-goog-api-key` query parameter or header
- **vs Grok**: OpenAI-compatible - uses same Bearer authentication

## Limitations and Known Issues

- **User API keys organization-wide**: Cannot scope user API keys to single project [VERIFIED] (OAIAPI-SC-OAI-ADMOVW)
- **Key shown once**: API keys displayed only at creation - must copy immediately [VERIFIED] (OAIAPI-SC-OAI-ADMOVW)
- **No key rotation API**: Must manually create and delete keys for rotation [COMMUNITY] (OAIAPI-SC-SO-KEYROT)

## Gotchas and Quirks

- **Environment variable name**: Python SDK defaults to `OPENAI_API_KEY` (not `OPENAI_KEY`) [VERIFIED] (OAIAPI-SC-GH-SDKPY)
- **Organization header optional**: Only required for multi-org access or legacy user keys [VERIFIED] (OAIAPI-SC-OAI-OVERVIEW)
- **Service account keys admin only**: Require admin API access to create [VERIFIED] (OAIAPI-SC-OAI-ADMOVW)

## Sources

- OAIAPI-SC-OAI-OVERVIEW - API Overview (Authentication section)
- OAIAPI-SC-OAI-ADMOVW - Administration Overview
- OAIAPI-SC-GH-SDKPY - Python SDK documentation

## Document History

**[2026-03-20 14:52]**
- Initial documentation created
