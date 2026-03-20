# Admin API: Organizations and Invites

**Doc ID**: ANTAPI-IN30
**Goal**: Document Admin API for organization management and user invitations
**API version**: anthropic-version 2023-06-01

**Depends on:**
- `_INFO_ANTAPI-IN02_AUTHENTICATION.md [ANTAPI-IN02]` for admin API key authentication

## Summary

The Admin API provides organization management endpoints. Organizations are the top-level entity; each contains workspaces, users, and API keys. The Organizations endpoint retrieves the current organization info. The Invites endpoints manage user invitations (create, retrieve, list, delete). Admin API keys with appropriate permissions are required. These endpoints use a separate base URL pattern under `/v1/organizations`.

## Key Facts

- **Organization Endpoint**: `GET /v1/organizations/me`
- **Invites Endpoints**: CRUD at `/v1/invites`
- **Auth**: Admin API key with organization-level permissions
- **Organization Model**: id, name, type="organization"
- **Invite Model**: id, email, role, status, expires_at, created_at, type="invite"
- **Status**: GA

## Organizations

### GET /v1/organizations/me - Get Current Organization

```python
import anthropic

client = anthropic.Anthropic()

org = client.admin.organizations.get()
print(f"Org ID: {org.id}")
print(f"Name: {org.name}")
```

**Response:**

- **id** (`string`) - Organization ID
- **name** (`string`) - Organization name
- **type** (`string`) - Always `"organization"`

## Invites

### POST /v1/invites - Create Invite

```python
invite = client.admin.invites.create(
    email="newuser@example.com",
    role="user",
)
print(f"Invite ID: {invite.id}")
print(f"Expires: {invite.expires_at}")
```

### GET /v1/invites/{invite_id} - Get Invite

```python
invite = client.admin.invites.retrieve("invite-abc123")
print(f"Email: {invite.email}")
print(f"Status: {invite.status}")
```

### GET /v1/invites - List Invites

```python
invites = client.admin.invites.list()
for inv in invites:
    print(f"{inv.email}: {inv.status} (role: {inv.role})")
```

### DELETE /v1/invites/{invite_id} - Delete Invite

```python
client.admin.invites.delete("invite-abc123")
```

## Invite Model

- **id** (`string`) - Invite ID
- **email** (`string`) - Invitee email
- **role** (`string`) - Organization role assigned
- **status** (`string`) - Invite status (pending, accepted, expired)
- **expires_at** (`string`) - RFC 3339 expiration datetime
- **created_at** (`string`) - RFC 3339 creation datetime
- **type** (`string`) - Always `"invite"`

## Gotchas and Quirks

- Admin API requires organization-level admin API keys
- Organization endpoint only returns the current org (no list of all orgs)
- Invites have an expiration date; expired invites must be re-created

## Related Endpoints

- `_INFO_ANTAPI-IN31_ADMIN_USERS.md [ANTAPI-IN31]` - User management
- `_INFO_ANTAPI-IN32_ADMIN_WORKSPACES.md [ANTAPI-IN32]` - Workspace management

## Sources

- ANTAPI-SC-ANTH-ADMIN - https://platform.claude.com/docs/en/api/admin - Admin API reference

## Document History

**[2026-03-20 04:12]**
- Initial documentation created from Admin API reference
