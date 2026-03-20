# Admin API: Users and API Keys

**Doc ID**: ANTAPI-IN31
**Goal**: Document Admin API for user management and API key administration
**API version**: anthropic-version 2023-06-01

**Depends on:**
- `_INFO_ANTAPI-IN30_ADMIN_ORGS.md [ANTAPI-IN30]` for organization context

## Summary

The Admin Users endpoints manage organization members (retrieve, list, update role, remove). The Admin API Keys endpoints manage API keys (retrieve, list, update). Users have organization roles and can be members of multiple workspaces. API keys are scoped to workspaces and have configurable names and statuses.

## Key Facts

- **Users Base**: `/v1/users`
- **API Keys Base**: `/v1/api_keys`
- **User Operations**: retrieve, list, update, delete (remove)
- **API Key Operations**: retrieve, list, update
- **User Model**: id, email, name, role, created_at, type="user"
- **Status**: GA

## Users

### GET /v1/users/{user_id} - Get User

```python
import anthropic

client = anthropic.Anthropic()

user = client.admin.users.retrieve("user-abc123")
print(f"Name: {user.name}")
print(f"Email: {user.email}")
print(f"Role: {user.role}")
print(f"Joined: {user.created_at}")
```

### GET /v1/users - List Users

```python
users = client.admin.users.list()
for user in users:
    print(f"{user.name} ({user.email}): {user.role}")
```

### POST /v1/users/{user_id} - Update User

```python
user = client.admin.users.update(
    "user-abc123",
    role="developer",
)
```

### DELETE /v1/users/{user_id} - Remove User

```python
client.admin.users.delete("user-abc123")
```

## User Model

- **id** (`string`) - User ID
- **email** (`string`) - User email
- **name** (`string`) - User display name
- **role** (`string`) - Organization role
- **created_at** (`string`) - RFC 3339 join datetime
- **type** (`string`) - Always `"user"`

## API Keys

### GET /v1/api_keys/{api_key_id} - Get API Key

```python
key = client.admin.api_keys.retrieve("apikey-abc123")
print(f"Name: {key.name}")
print(f"Status: {key.status}")
```

### GET /v1/api_keys - List API Keys

```python
keys = client.admin.api_keys.list()
for key in keys:
    print(f"{key.name}: {key.status}")
```

### POST /v1/api_keys/{api_key_id} - Update API Key

```python
key = client.admin.api_keys.update(
    "apikey-abc123",
    name="Production Key",
    status="active",
)
```

## Gotchas and Quirks

- API keys cannot be created via Admin API; use the Console
- Removing a user is irreversible; they must be re-invited
- User roles affect permissions across all workspaces in the organization
- API keys are scoped to specific workspaces

## Related Endpoints

- `_INFO_ANTAPI-IN30_ADMIN_ORGS.md [ANTAPI-IN30]` - Organizations and invites
- `_INFO_ANTAPI-IN32_ADMIN_WORKSPACES.md [ANTAPI-IN32]` - Workspace management

## Sources

- ANTAPI-SC-ANTH-ADMIN - https://platform.claude.com/docs/en/api/admin - Admin API reference

## Document History

**[2026-03-20 04:15]**
- Initial documentation created from Admin API reference
