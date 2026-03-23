# Administration Overview

**Doc ID**: OAIAPI-IN47
**Goal**: Document the Administration API hierarchy - organizations, projects, RBAC model, and admin API keys
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references

## Summary

The Administration API provides programmatic management of OpenAI organizations. The hierarchy is Organization -> Projects -> Resources (API keys, service accounts, rate limits). Access requires Admin API Keys created via the create admin API key endpoint - these keys cannot be used for non-admin endpoints. Organization-level resources include users, invites, groups, custom roles, certificates, and audit logs. Project-level resources include users, groups, service accounts, API keys, and rate limits. The RBAC (Role-Based Access Control) model supports built-in roles (owner, admin, member) and custom roles with granular permissions. All admin endpoints use the `/v1/organization/` base path. Audit logs track all organizational actions for security and compliance. Usage and cost tracking available at org and project level. [VERIFIED] (OAIAPI-SC-OAI-ADMOVW)

## Key Facts

- **Hierarchy**: Organization -> Projects -> Resources [VERIFIED] (OAIAPI-SC-OAI-ADMOVW)
- **Admin API Keys**: Required for all admin endpoints; cannot be used for regular API calls [VERIFIED] (OAIAPI-SC-OAI-ADMOVW)
- **Base path**: `/v1/organization/` for all admin endpoints [VERIFIED] (OAIAPI-SC-OAI-ADMOVW)
- **RBAC**: Built-in roles (owner, admin, member) + custom roles [VERIFIED] (OAIAPI-SC-OAI-ADMOVW)
- **Audit logs**: Complete action history for compliance [VERIFIED] (OAIAPI-SC-OAI-ADMOVW)

## Use Cases

- **Organization setup**: Programmatic org configuration and user management
- **Access control**: Assign roles and permissions to users and groups
- **Security**: Audit logging, certificate management, key rotation
- **Cost management**: Track usage and costs per project
- **Automation**: CI/CD integration for API key and service account management

## Quick Reference

```
Admin API Key Creation:
  POST /v1/organization/audit_logs/admin_api_keys   # Create admin API key

Organization Level:
  /v1/organization/users          # Users management
  /v1/organization/invites        # Invite management
  /v1/organization/groups         # Groups management
  /v1/organization/roles          # Custom roles
  /v1/organization/certificates   # mTLS certificates
  /v1/organization/audit_logs     # Audit logs
  /v1/organization/usage          # Usage tracking
  /v1/organization/costs          # Cost reporting

Project Level:
  /v1/organization/projects                          # Project CRUD
  /v1/organization/projects/{id}/users               # Project users
  /v1/organization/projects/{id}/groups              # Project groups
  /v1/organization/projects/{id}/service_accounts    # Service accounts
  /v1/organization/projects/{id}/api_keys            # API keys
  /v1/organization/projects/{id}/rate_limits         # Rate limits

Headers:
  Authorization: Bearer $ADMIN_API_KEY
  Content-Type: application/json
```

## Organization Hierarchy

```
Organization (org-xxx)
├─> Users (members with roles)
├─> Groups (collections of users)
├─> Custom Roles (permission sets)
├─> Certificates (mTLS)
├─> Audit Logs (action history)
├─> Usage / Costs (billing)
└─> Projects (proj-xxx)
    ├─> Project Users (with project roles)
    ├─> Project Groups
    ├─> Service Accounts (svc_acct-xxx)
    ├─> API Keys (sk-xxx)
    └─> Rate Limits (per-model limits)
```

## Built-in Roles

- **Owner**: Full organization access including billing and admin management
- **Admin**: Manage users, projects, and settings (no billing)
- **Member**: Access assigned projects, use API within project scope

## Admin API Keys

Admin API keys are separate from regular API keys:
- Created via POST /v1/organization/audit_logs/admin_api_keys
- Can only call admin endpoints (not Responses, Chat, etc.)
- Should be treated as highly sensitive credentials
- Use for automation, CI/CD, and programmatic org management

## SDK Examples (Python)

> **SDK note**: `client.organization.*` methods are not available in openai Python SDK v2.29.0.
> The Administration API uses REST-only endpoints with admin API keys (`sk-admin-...`).
> Use `httpx` or `requests` for direct REST calls to `https://api.openai.com/v1/organization/*`.

### Create Admin API Key

```python
from openai import OpenAI

# Use existing admin key to create new one
client = OpenAI(api_key="sk-admin-...")

admin_key = client.organization.admin_api_keys.create(
    name="CI/CD Admin Key"
)

print(f"Admin Key: {admin_key.value}")
print(f"Key ID: {admin_key.id}")
```

### Organization Overview - Production Ready

```python
from openai import OpenAI

client = OpenAI(api_key="sk-admin-...")

def get_org_overview():
    """Get complete organization overview"""
    # List users
    users = client.organization.users.list(limit=100)
    
    # List projects
    projects = client.organization.projects.list(limit=100)
    
    # List groups
    groups = client.organization.groups.list(limit=100)
    
    overview = {
        "users": len(users.data),
        "projects": len(projects.data),
        "groups": len(groups.data),
    }
    
    print(f"Users: {overview['users']}")
    print(f"Projects: {overview['projects']}")
    print(f"Groups: {overview['groups']}")
    
    for proj in projects.data:
        print(f"  Project: {proj.name} ({proj.id}) - {proj.status}")
    
    return overview

try:
    get_org_overview()
except Exception as e:
    print(f"Error: {e}")
```

## Error Responses

- **401 Unauthorized** - Invalid or non-admin API key
- **403 Forbidden** - Insufficient admin permissions
- **404 Not Found** - Resource not found
- **429 Too Many Requests** - Rate limit exceeded

## Differences from Other APIs

- **vs Anthropic**: Anthropic has organization management via console only, no programmatic admin API
- **vs Gemini**: Google Cloud IAM handles access control; no API-level admin endpoints
- **vs Grok**: Limited organization management API

## Limitations and Known Issues

- **Admin key separation**: Admin keys cannot call regular API endpoints [VERIFIED] (OAIAPI-SC-OAI-ADMOVW)
- **No cross-org management**: Each admin key scoped to one organization [ASSUMED]

## Sources

- OAIAPI-SC-OAI-ADMOVW - Administration Overview

## Document History

**[2026-03-21 09:48]**
- Added: SDK v2.29.0 note - client.organization.* not in Python SDK (REST-only admin API)

**[2026-03-20 18:05]**
- Initial documentation created
