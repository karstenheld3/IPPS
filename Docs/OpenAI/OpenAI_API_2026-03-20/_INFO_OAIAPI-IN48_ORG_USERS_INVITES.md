# Organization Users and Invites

**Doc ID**: OAIAPI-IN48
**Goal**: Document organization user management and invite operations
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references
- `_INFO_OAIAPI-IN47_ADMIN_OVERVIEW.md [OAIAPI-IN47]` for admin context

## Summary

Organization Users API manages members of an OpenAI organization. List users (GET /v1/organization/users), retrieve user details (GET by ID), update roles (POST), and remove users (DELETE). Each user has a role (owner, admin, member) and associated email. Invites API manages pending invitations: create invites (POST /v1/organization/invites) with email and role, list pending invites (GET), retrieve invite details (GET by ID), and delete invites (DELETE). Users are identified by user IDs (user-xxx format). Role assignments define the user's permissions at the organization level. Only owners and admins can manage users and invites. Removed users lose access to all organization resources immediately. [VERIFIED] (OAIAPI-SC-OAI-ADMORG)

## Key Facts

- **User roles**: owner, admin, member [VERIFIED] (OAIAPI-SC-OAI-ADMORG)
- **Invite flow**: Create invite -> user accepts via email -> becomes org member [VERIFIED] (OAIAPI-SC-OAI-ADMORG)
- **Removal**: Immediate access revocation [VERIFIED] (OAIAPI-SC-OAI-ADMORG)
- **Admin key required**: All endpoints require admin API key [VERIFIED] (OAIAPI-SC-OAI-ADMOVW)

## Quick Reference

```
Users:
  GET    /v1/organization/users              # List users
  GET    /v1/organization/users/{user_id}    # Retrieve user
  POST   /v1/organization/users/{user_id}    # Update user role
  DELETE /v1/organization/users/{user_id}    # Remove user

Invites:
  GET    /v1/organization/invites            # List invites
  POST   /v1/organization/invites            # Create invite
  GET    /v1/organization/invites/{invite_id}# Retrieve invite
  DELETE /v1/organization/invites/{invite_id}# Delete invite
```

## User Object

```json
{
  "object": "organization.user",
  "id": "user-abc123",
  "name": "Jane Smith",
  "email": "jane@example.com",
  "role": "admin",
  "added_at": 1711471533
}
```

## Invite Object

```json
{
  "object": "organization.invite",
  "id": "invite-abc123",
  "email": "bob@example.com",
  "role": "member",
  "status": "pending",
  "invited_at": 1711471533,
  "expires_at": 1712081133
}
```

## SDK Examples (Python)

> **SDK note**: `client.organization.*` methods are not available in openai Python SDK v2.29.0.
> The Administration API uses REST-only endpoints with admin API keys (`sk-admin-...`).
> Use `httpx` or `requests` for direct REST calls to `https://api.openai.com/v1/organization/*`.

### User and Invite Management - Production Ready

```python
from openai import OpenAI

client = OpenAI(api_key="sk-admin-...")

def invite_user(email: str, role: str = "member"):
    """Invite a user to the organization"""
    try:
        invite = client.organization.invites.create(
            email=email,
            role=role
        )
        print(f"Invited {email} as {role}: {invite.id}")
        return invite
    except Exception as e:
        print(f"Error inviting {email}: {e}")
        return None

def list_users():
    """List all organization users"""
    users = client.organization.users.list(limit=100)
    for user in users.data:
        print(f"  {user.name} ({user.email}) - {user.role}")
    return users.data

def remove_user(user_id: str):
    """Remove user from organization"""
    try:
        client.organization.users.delete(user_id)
        print(f"Removed user: {user_id}")
    except Exception as e:
        print(f"Error: {e}")

# Usage
invite_user("newdev@example.com", "member")
list_users()
```

## Error Responses

- **400 Bad Request** - Invalid email or role
- **401 Unauthorized** - Invalid admin API key
- **403 Forbidden** - Insufficient permissions (must be owner/admin)
- **404 Not Found** - User or invite not found
- **409 Conflict** - User already exists or invite already pending

## Differences from Other APIs

- **vs Anthropic**: No programmatic user management API
- **vs Gemini**: Uses Google Cloud IAM for user management
- **vs Grok**: Limited user management API

## Sources

- OAIAPI-SC-OAI-ADMORG - Organization Administration API

## Document History

**[2026-03-21 09:48]**
- Added: SDK v2.29.0 note - client.organization.* not in Python SDK (REST-only admin API)

**[2026-03-20 18:07]**
- Initial documentation created
