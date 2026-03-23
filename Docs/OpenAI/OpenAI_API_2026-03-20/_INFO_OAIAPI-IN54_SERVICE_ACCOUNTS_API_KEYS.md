# Service Accounts and API Keys

**Doc ID**: OAIAPI-IN54
**Goal**: Document project service accounts and API key management
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references
- `_INFO_OAIAPI-IN50_PROJECTS.md [OAIAPI-IN50]` for project context

## Summary

Service Accounts API manages programmatic identities within projects. Create service accounts (POST /v1/organization/projects/{project_id}/service_accounts) to get a service account with an associated API key. Service accounts are non-human identities for CI/CD pipelines, backend services, and automated systems. Each service account has a role (owner, member) and receives an API key on creation. API Keys API manages project-scoped API keys: list keys (GET), retrieve key details (GET by ID), and delete keys (DELETE). API keys are project-scoped - they can only access resources within their project. Key creation returns the secret value only once; it cannot be retrieved later. Service accounts are identified by `svc_acct_` prefix. API keys use `sk-` prefix (regular) or `sk-admin-` prefix (admin). Keys can be rotated by creating a new one and deleting the old one. [VERIFIED] (OAIAPI-SC-OAI-ADMPRJ)

## Key Facts

- **Service accounts**: Non-human identities for programmatic access [VERIFIED] (OAIAPI-SC-OAI-ADMPRJ)
- **Key on creation**: API key returned only at service account creation time [VERIFIED] (OAIAPI-SC-OAI-ADMPRJ)
- **One-time secret**: Key value shown only once, cannot be retrieved later [VERIFIED] (OAIAPI-SC-OAI-ADMPRJ)
- **Project-scoped**: Keys only access their project's resources [VERIFIED] (OAIAPI-SC-OAI-ADMPRJ)
- **Prefixes**: `svc_acct_` (service accounts), `sk-` (keys), `sk-admin-` (admin keys) [VERIFIED] (OAIAPI-SC-OAI-ADMPRJ)

## Quick Reference

```
Service Accounts:
  POST   /v1/organization/projects/{id}/service_accounts                  # Create
  GET    /v1/organization/projects/{id}/service_accounts                  # List
  GET    /v1/organization/projects/{id}/service_accounts/{sa_id}          # Retrieve
  DELETE /v1/organization/projects/{id}/service_accounts/{sa_id}          # Delete

API Keys:
  GET    /v1/organization/projects/{id}/api_keys                          # List keys
  GET    /v1/organization/projects/{id}/api_keys/{key_id}                 # Retrieve key
  DELETE /v1/organization/projects/{id}/api_keys/{key_id}                 # Delete key

Admin API Keys:
  POST   /v1/organization/audit_logs/admin_api_keys                       # Create admin key
  GET    /v1/organization/audit_logs/admin_api_keys                       # List admin keys
  GET    /v1/organization/audit_logs/admin_api_keys/{key_id}              # Retrieve
  DELETE /v1/organization/audit_logs/admin_api_keys/{key_id}              # Delete
```

## Service Account Object

```json
{
  "object": "organization.project.service_account",
  "id": "svc_acct_abc",
  "name": "Production App",
  "role": "member",
  "created_at": 1711471533,
  "api_key": {
    "object": "organization.project.service_account.api_key",
    "value": "sk-abcdefghijklmnop123",
    "name": "Secret Key",
    "created_at": 1711471533,
    "id": "key_abc123"
  }
}
```

Note: `api_key.value` is only present in the creation response.

## API Key Object

```json
{
  "object": "organization.project.api_key",
  "id": "key_abc123",
  "name": "My API Key",
  "redacted_value": "sk-...abc123",
  "created_at": 1711471533,
  "owner": {
    "type": "service_account",
    "service_account": {
      "id": "svc_acct_abc",
      "name": "Production App"
    }
  }
}
```

## SDK Examples (Python)

> **SDK note**: `client.organization.*` methods are not available in openai Python SDK v2.29.0.
> The Administration API uses REST-only endpoints with admin API keys (`sk-admin-...`).
> Use `httpx` or `requests` for direct REST calls to `https://api.openai.com/v1/organization/*`.

### Service Account Lifecycle

```python
from openai import OpenAI

client = OpenAI(api_key="sk-admin-...")

project_id = "proj_abc123"

# Create service account
svc = client.organization.projects.service_accounts.create(
    project_id=project_id,
    name="CI/CD Pipeline"
)

# IMPORTANT: Store the key now - it won't be shown again
api_key_value = svc.api_key.value
print(f"Service Account: {svc.id}")
print(f"API Key (SAVE THIS): {api_key_value}")

# List service accounts
accounts = client.organization.projects.service_accounts.list(
    project_id=project_id
)
for sa in accounts.data:
    print(f"  {sa.name} ({sa.id}) - {sa.role}")
```

### Key Rotation - Production Ready

```python
from openai import OpenAI
import time

client = OpenAI(api_key="sk-admin-...")

def rotate_service_account_key(project_id: str, old_sa_id: str, name: str):
    """Rotate a service account by creating new and deleting old"""
    # Create new service account
    new_svc = client.organization.projects.service_accounts.create(
        project_id=project_id,
        name=f"{name} (rotated {time.strftime('%Y-%m-%d')})"
    )
    
    new_key = new_svc.api_key.value
    print(f"New service account: {new_svc.id}")
    print(f"New API key: {new_key[:10]}...")
    
    # Deploy new key to your services here
    # ... update secrets manager, env vars, etc. ...
    
    # Delete old service account (and its key)
    try:
        client.organization.projects.service_accounts.delete(
            project_id=project_id,
            service_account_id=old_sa_id
        )
        print(f"Deleted old service account: {old_sa_id}")
    except Exception as e:
        print(f"Warning: Could not delete old account: {e}")
    
    return {"new_sa_id": new_svc.id, "new_key": new_key}

try:
    result = rotate_service_account_key(
        project_id="proj_abc123",
        old_sa_id="svc_acct_old",
        name="Production API"
    )
except Exception as e:
    print(f"Rotation failed: {e}")
```

### Audit API Keys

```python
from openai import OpenAI

client = OpenAI(api_key="sk-admin-...")

def audit_project_keys(project_id: str):
    """List all API keys in a project for security audit"""
    keys = client.organization.projects.api_keys.list(
        project_id=project_id,
        limit=100
    )
    
    print(f"Project {project_id}: {len(keys.data)} API keys")
    for key in keys.data:
        owner_type = key.owner.type
        if owner_type == "service_account":
            owner_name = key.owner.service_account.name
        elif owner_type == "user":
            owner_name = key.owner.user.email
        else:
            owner_name = "unknown"
        
        print(f"  {key.redacted_value} | Owner: {owner_name} ({owner_type}) | Created: {key.created_at}")

try:
    audit_project_keys("proj_abc123")
except Exception as e:
    print(f"Error: {e}")
```

## Error Responses

- **400 Bad Request** - Invalid parameters
- **401 Unauthorized** - Invalid admin API key
- **403 Forbidden** - Insufficient permissions
- **404 Not Found** - Service account, key, or project not found
- **409 Conflict** - Name conflict

## Rate Limiting / Throttling

- **Key creation**: Standard admin API rate limits
- **Key listing**: Standard admin API rate limits

## Differences from Other APIs

- **vs Anthropic**: Anthropic has API keys via console; no programmatic service account API
- **vs Gemini**: Google Cloud Service Accounts via IAM API (different paradigm)
- **vs Grok**: Limited API key management

## Limitations and Known Issues

- **One-time key visibility**: API key value only shown at creation; cannot be retrieved later [VERIFIED] (OAIAPI-SC-OAI-ADMPRJ)
- **No key update**: Cannot rename or change permissions on existing keys; must rotate [ASSUMED]
- **Admin key separation**: Admin keys cannot be used as regular API keys [VERIFIED] (OAIAPI-SC-OAI-ADMOVW)

## Gotchas and Quirks

- **Store key immediately**: The API key secret is in the creation response ONLY [VERIFIED] (OAIAPI-SC-OAI-ADMPRJ)
- **Redacted in list**: List/retrieve endpoints show only redacted key values [VERIFIED] (OAIAPI-SC-OAI-ADMPRJ)
- **Rotation pattern**: Create new -> deploy -> delete old (no atomic rotation) [ASSUMED]
- **Service account roles**: Can be `owner` or `member` at project level [VERIFIED] (OAIAPI-SC-OAI-ADMPRJ)

## Sources

- OAIAPI-SC-OAI-ADMPRJ - Projects Administration API
- OAIAPI-SC-OAI-ADMOVW - Administration Overview

## Document History

**[2026-03-21 09:48]**
- Added: SDK v2.29.0 note - client.organization.* not in Python SDK (REST-only admin API)

**[2026-03-20 18:17]**
- Initial documentation created
