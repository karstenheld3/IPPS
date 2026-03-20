# Admin API: Workspaces and Members

**Doc ID**: ANTAPI-IN32
**Goal**: Document Admin API for workspace management and workspace membership
**API version**: anthropic-version 2023-06-01

**Depends on:**
- `_INFO_ANTAPI-IN30_ADMIN_ORGS.md [ANTAPI-IN30]` for organization context

## Summary

Workspaces are organizational units within an Anthropic organization. Each workspace has its own API keys, rate limits, and spend limits. The Admin Workspaces endpoints manage workspace lifecycle (create, retrieve, list, update, archive). Workspace Members endpoints manage user membership within workspaces (add, retrieve, list, update role, remove). API keys and batches are scoped to workspaces.

## Key Facts

- **Workspaces Base**: `/v1/workspaces`
- **Members Base**: `/v1/workspaces/{workspace_id}/members`
- **Workspace Operations**: create, retrieve, list, update, archive
- **Member Operations**: create, retrieve, list, update, delete
- **Workspace Member Model**: user_id, workspace_id, role, type="workspace_member"
- **Status**: GA

## Workspaces

### POST /v1/workspaces - Create Workspace

```python
import anthropic

client = anthropic.Anthropic()

workspace = client.admin.workspaces.create(
    name="Production",
)
print(f"Workspace ID: {workspace.id}")
```

### GET /v1/workspaces/{workspace_id} - Get Workspace

```python
workspace = client.admin.workspaces.retrieve("wrkspc-abc123")
print(f"Name: {workspace.name}")
```

### GET /v1/workspaces - List Workspaces

```python
workspaces = client.admin.workspaces.list()
for ws in workspaces:
    print(f"{ws.id}: {ws.name}")
```

### POST /v1/workspaces/{workspace_id} - Update Workspace

```python
workspace = client.admin.workspaces.update(
    "wrkspc-abc123",
    name="Production v2",
)
```

### POST /v1/workspaces/{workspace_id}/archive - Archive Workspace

```python
workspace = client.admin.workspaces.archive("wrkspc-abc123")
```

## Workspace Members

### POST /v1/workspaces/{workspace_id}/members - Add Member

```python
member = client.admin.workspaces.members.create(
    workspace_id="wrkspc-abc123",
    user_id="user-def456",
    role="developer",
)
```

### GET /v1/workspaces/{workspace_id}/members/{user_id} - Get Member

```python
member = client.admin.workspaces.members.retrieve(
    workspace_id="wrkspc-abc123",
    user_id="user-def456",
)
print(f"Role: {member.workspace_role}")
```

### GET /v1/workspaces/{workspace_id}/members - List Members

```python
members = client.admin.workspaces.members.list(workspace_id="wrkspc-abc123")
for m in members:
    print(f"{m.user_id}: {m.workspace_role}")
```

### POST /v1/workspaces/{workspace_id}/members/{user_id} - Update Member

```python
member = client.admin.workspaces.members.update(
    workspace_id="wrkspc-abc123",
    user_id="user-def456",
    role="admin",
)
```

### DELETE /v1/workspaces/{workspace_id}/members/{user_id} - Remove Member

```python
client.admin.workspaces.members.delete(
    workspace_id="wrkspc-abc123",
    user_id="user-def456",
)
```

## Workspace Member Model

- **user_id** (`string`) - User ID
- **workspace_id** (`string`) - Workspace ID
- **workspace_role** (`string`) - Role within workspace
- **type** (`string`) - Always `"workspace_member"`

## Gotchas and Quirks

- Archiving a workspace is soft-delete; archived workspaces cannot be used but may be viewable
- API keys are created per-workspace via the Console, not the Admin API
- Rate limits and spend limits are configured per-workspace
- Batches are scoped to the workspace of the API key used

## Related Endpoints

- `_INFO_ANTAPI-IN30_ADMIN_ORGS.md [ANTAPI-IN30]` - Organizations and invites
- `_INFO_ANTAPI-IN31_ADMIN_USERS.md [ANTAPI-IN31]` - Users and API keys
- `_INFO_ANTAPI-IN33_USAGE_API.md [ANTAPI-IN33]` - Usage reports per workspace

## Sources

- ANTAPI-SC-ANTH-ADMIN - https://platform.claude.com/docs/en/api/admin - Admin API reference

## Document History

**[2026-03-20 04:18]**
- Initial documentation created from Admin API reference
