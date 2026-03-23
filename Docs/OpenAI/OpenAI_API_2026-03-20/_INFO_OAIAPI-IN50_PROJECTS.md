# Projects API

**Doc ID**: OAIAPI-IN50
**Goal**: Document project management - create, retrieve, update, list, archive projects and sub-resources
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references
- `_INFO_OAIAPI-IN47_ADMIN_OVERVIEW.md [OAIAPI-IN47]` for admin context

## Summary

Projects API manages isolated environments within an organization. Each project has its own API keys, service accounts, rate limits, and usage tracking. Create projects (POST /v1/organization/projects), retrieve (GET), update name/description (POST), list (GET with pagination), and archive (POST archive). Projects contain sub-resources: users (add/remove org members to project with roles), groups (assign groups to project), service accounts (programmatic access), API keys (project-scoped keys), and rate limits (per-model limits). Project-scoped API keys can only access resources within their project. Archiving a project revokes all its API keys and service accounts. Projects provide cost isolation - usage is tracked and billed per project. The `OpenAI-Project` header routes API calls to a specific project. [VERIFIED] (OAIAPI-SC-OAI-ADMPRJ)

## Key Facts

- **Isolation**: Each project has own keys, accounts, limits, usage [VERIFIED] (OAIAPI-SC-OAI-ADMPRJ)
- **Scoped keys**: Project API keys only access that project's resources [VERIFIED] (OAIAPI-SC-OAI-ADMPRJ)
- **Archive**: Revokes all keys and service accounts [VERIFIED] (OAIAPI-SC-OAI-ADMPRJ)
- **Header routing**: `OpenAI-Project: proj_xxx` header for API calls [VERIFIED] (OAIAPI-SC-OAI-ADMPRJ)
- **Cost tracking**: Usage tracked per project [VERIFIED] (OAIAPI-SC-OAI-ADMPRJ)

## Quick Reference

```
Projects:
  POST   /v1/organization/projects                           # Create
  GET    /v1/organization/projects                           # List
  GET    /v1/organization/projects/{project_id}              # Retrieve
  POST   /v1/organization/projects/{project_id}              # Update
  POST   /v1/organization/projects/{project_id}/archive      # Archive

Sub-resources:
  /v1/organization/projects/{id}/users                       # Project users
  /v1/organization/projects/{id}/groups                      # Project groups
  /v1/organization/projects/{id}/service_accounts            # Service accounts
  /v1/organization/projects/{id}/api_keys                    # API keys
  /v1/organization/projects/{id}/rate_limits                 # Rate limits
```

## Project Object

```json
{
  "object": "organization.project",
  "id": "proj_abc123",
  "name": "Production App",
  "status": "active",
  "created_at": 1711471533,
  "archived_at": null
}
```

### Status Values

- **active**: Project is operational
- **archived**: Project is archived, all keys revoked

## SDK Examples (Python)

> **SDK note**: `client.organization.*` methods are not available in openai Python SDK v2.29.0.
> The Administration API uses REST-only endpoints with admin API keys (`sk-admin-...`).
> Use `httpx` or `requests` for direct REST calls to `https://api.openai.com/v1/organization/*`.

### Project Lifecycle Management

```python
from openai import OpenAI

client = OpenAI(api_key="sk-admin-...")

# Create project
project = client.organization.projects.create(
    name="Production API",
    description="Production environment for customer-facing API"
)
print(f"Project: {project.id}")

# Add user to project
client.organization.projects.users.create(
    project_id=project.id,
    user_id="user-abc123",
    role="member"
)

# Create service account
svc = client.organization.projects.service_accounts.create(
    project_id=project.id,
    name="CI/CD Pipeline"
)
print(f"Service Account: {svc.id}")
print(f"API Key: {svc.api_key.value}")

# Set rate limits
client.organization.projects.rate_limits.update(
    project_id=project.id,
    model="gpt-5.4",
    max_requests_per_minute=100,
    max_tokens_per_minute=50000
)

# List all projects
projects = client.organization.projects.list(limit=100)
for p in projects.data:
    print(f"  {p.name} ({p.id}) - {p.status}")
```

## Error Responses

- **400 Bad Request** - Invalid project parameters
- **401 Unauthorized** - Invalid admin API key
- **403 Forbidden** - Insufficient permissions
- **404 Not Found** - Project not found

## Differences from Other APIs

- **vs Anthropic**: Anthropic has workspaces (similar concept) but limited API management
- **vs Gemini**: Google Cloud projects with IAM (different abstraction level)
- **vs Grok**: No project isolation API

## Sources

- OAIAPI-SC-OAI-ADMPRJ - Projects Administration API

## Document History

**[2026-03-21 09:48]**
- Added: SDK v2.29.0 note - client.organization.* not in Python SDK (REST-only admin API)

**[2026-03-20 18:10]**
- Initial documentation created
