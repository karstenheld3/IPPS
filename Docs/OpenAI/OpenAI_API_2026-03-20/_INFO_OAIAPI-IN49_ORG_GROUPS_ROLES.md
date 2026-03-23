# Organization Groups and Custom Roles

**Doc ID**: OAIAPI-IN49
**Goal**: Document organization groups for bulk access control and custom roles for granular permissions
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references
- `_INFO_OAIAPI-IN47_ADMIN_OVERVIEW.md [OAIAPI-IN47]` for admin context

## Summary

Organization Groups API manages collections of users for bulk access control. Create groups (POST /v1/organization/groups), add/remove members, and assign groups to projects. Groups simplify permission management - instead of assigning users individually to each project, add them to a group and assign the group. Custom Roles API enables granular permission definitions beyond built-in roles (owner, admin, member). Create roles (POST /v1/organization/roles) with specific permission sets, then assign to users or groups. Roles define what actions users can perform: manage projects, view audit logs, create API keys, access billing, etc. List roles (GET), retrieve (GET by ID), update (POST), delete (DELETE). Group membership changes take effect immediately. [VERIFIED] (OAIAPI-SC-OAI-ADMORG)

## Key Facts

- **Groups**: Collections of users for bulk access management [VERIFIED] (OAIAPI-SC-OAI-ADMORG)
- **Custom roles**: Granular permission sets beyond owner/admin/member [VERIFIED] (OAIAPI-SC-OAI-ADMORG)
- **Project assignment**: Groups can be assigned to projects with specific roles [VERIFIED] (OAIAPI-SC-OAI-ADMORG)
- **Immediate effect**: Membership and role changes take effect immediately [VERIFIED] (OAIAPI-SC-OAI-ADMORG)

## Quick Reference

```
Groups:
  POST   /v1/organization/groups                          # Create group
  GET    /v1/organization/groups                          # List groups
  GET    /v1/organization/groups/{group_id}               # Retrieve group
  POST   /v1/organization/groups/{group_id}               # Update group
  DELETE /v1/organization/groups/{group_id}               # Delete group

Roles:
  POST   /v1/organization/roles                           # Create custom role
  GET    /v1/organization/roles                           # List roles
  GET    /v1/organization/roles/{role_id}                 # Retrieve role
  POST   /v1/organization/roles/{role_id}                 # Update role
  DELETE /v1/organization/roles/{role_id}                 # Delete role
```

## Group Object

```json
{
  "object": "organization.group",
  "id": "group-abc123",
  "name": "Engineering Team",
  "description": "Backend and frontend engineers",
  "created_at": 1711471533,
  "metadata": {}
}
```

## Role Object

```json
{
  "object": "organization.role",
  "id": "role-abc123",
  "name": "Developer",
  "description": "Can create API keys and use API endpoints",
  "permissions": [
    "api_keys.create",
    "api_keys.read",
    "projects.read",
    "usage.read"
  ],
  "created_at": 1711471533,
  "is_builtin": false
}
```

## SDK Examples (Python)

> **SDK note**: `client.organization.*` methods are not available in openai Python SDK v2.29.0.
> The Administration API uses REST-only endpoints with admin API keys (`sk-admin-...`).
> Use `httpx` or `requests` for direct REST calls to `https://api.openai.com/v1/organization/*`.

### Group and Role Management

```python
from openai import OpenAI

client = OpenAI(api_key="sk-admin-...")

# Create a custom role
role = client.organization.roles.create(
    name="Developer",
    description="API access with usage visibility",
    permissions=["api_keys.create", "api_keys.read", "projects.read", "usage.read"]
)
print(f"Role: {role.id}")

# Create a group
group = client.organization.groups.create(
    name="Backend Team",
    description="Backend engineering team"
)
print(f"Group: {group.id}")

# List all roles
roles = client.organization.roles.list()
for r in roles.data:
    builtin = " (built-in)" if r.is_builtin else ""
    print(f"  {r.name}{builtin}: {len(r.permissions)} permissions")
```

## Differences from Other APIs

- **vs Anthropic**: No groups or custom roles API
- **vs Gemini**: Google Cloud IAM provides similar RBAC but via Google Cloud APIs
- **vs Grok**: No custom roles API

## Sources

- OAIAPI-SC-OAI-ADMORG - Organization Administration API

## Document History

**[2026-03-21 09:48]**
- Added: SDK v2.29.0 note - client.organization.* not in Python SDK (REST-only admin API)

**[2026-03-20 18:09]**
- Initial documentation created
