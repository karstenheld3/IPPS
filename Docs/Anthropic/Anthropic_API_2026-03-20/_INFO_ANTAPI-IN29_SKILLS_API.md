# Skills API (Beta)

**Doc ID**: ANTAPI-IN29
**Goal**: Document beta Skills API - create, retrieve, list, delete operations
**API version**: anthropic-version 2023-06-01

**Depends on:**
- `_INFO_ANTAPI-IN01_INTRODUCTION.md [ANTAPI-IN01]` for base URL, auth headers
- `_INFO_ANTAPI-IN03_VERSIONING.md [ANTAPI-IN03]` for beta header usage

## Summary

The Skills API (beta) enables creating and managing reusable agent skills. Skills encapsulate specific capabilities (instructions, tools, configurations) that can be attached to Claude for consistent behavior across conversations. The API provides CRUD operations: create, retrieve, list, and delete. Skills are accessed via the `client.beta.skills` namespace.

## Key Facts

- **Base Endpoint**: `/v1/skills`
- **SDK Namespace**: `client.beta.skills`
- **Operations**: create, retrieve, list, delete
- **Pagination**: Cursor-based (`SyncPageCursor`)
- **Status**: Beta

## Endpoints

### POST /v1/skills - Create Skill

```python
import anthropic

client = anthropic.Anthropic()

skill = client.beta.skills.create(
    name="data_analyst",
    description="A skill for analyzing datasets and generating insights",
    # Additional skill configuration parameters
)
print(f"Skill ID: {skill.id}")
```

### GET /v1/skills/{skill_id} - Retrieve Skill

```python
skill = client.beta.skills.retrieve("skill-abc123")
print(f"Name: {skill.name}")
print(f"Description: {skill.description}")
```

### GET /v1/skills - List Skills

```python
skills = client.beta.skills.list()
for skill in skills:
    print(f"{skill.id}: {skill.name}")
```

### DELETE /v1/skills/{skill_id} - Delete Skill

```python
result = client.beta.skills.delete("skill-abc123")
print(f"Deleted: {result.id}")
```

## SDK Types

- **SkillCreateResponse** - Response from skill creation
- **SkillRetrieveResponse** - Response from skill retrieval
- **SkillListResponse** - Response from skill listing (cursor-paginated)
- **SkillDeleteResponse** - Response from skill deletion

## Gotchas and Quirks

- Skills API is in beta; the interface may change
- Use `client.beta.skills` namespace in SDK
- Skills list uses cursor-based pagination (`SyncPageCursor`), different from standard `SyncPage`
- Skill configuration parameters are still evolving; check latest documentation

## Related Endpoints

- `_INFO_ANTAPI-IN21_TOOL_USE.md [ANTAPI-IN21]` - Tool use (skills can define tools)
- `_INFO_ANTAPI-IN28_FILES_API.md [ANTAPI-IN28]` - Files API (another beta feature)

## Sources

- ANTAPI-SC-GH-SDKAPI - https://github.com/anthropics/anthropic-sdk-python/blob/main/api.md - Skill types and methods

## Document History

**[2026-03-20 04:08]**
- Initial documentation created from SDK API types
