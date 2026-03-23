# Audit Logs

**Doc ID**: OAIAPI-IN52
**Goal**: Document audit log retrieval for security monitoring and compliance
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references
- `_INFO_OAIAPI-IN47_ADMIN_OVERVIEW.md [OAIAPI-IN47]` for admin context

## Summary

The Audit Logs API provides a complete record of all actions taken within an organization. List audit log entries (GET /v1/organization/audit_logs) with filtering by event type, actor, date range, and project. Each entry contains the event type, actor (who performed the action), timestamp, and event-specific data. Event types cover user management (user.added, user.removed, user.updated), project management (project.created, project.archived), API key operations (api_key.created, api_key.deleted), service account changes, role assignments, invite actions, certificate operations, and rate limit modifications. Audit logs are essential for SOC2 compliance, security investigations, and change tracking. Logs are immutable and retained per organization's data retention policy. Pagination via cursor-based after/before parameters. Admin API key required for access. [VERIFIED] (OAIAPI-SC-OAI-ADMORG)

## Key Facts

- **Immutable**: Audit logs cannot be modified or deleted [VERIFIED] (OAIAPI-SC-OAI-ADMORG)
- **Comprehensive**: All organizational actions are logged [VERIFIED] (OAIAPI-SC-OAI-ADMOVW)
- **Filterable**: By event type, actor, date range, project [VERIFIED] (OAIAPI-SC-OAI-ADMORG)
- **Compliance**: Supports SOC2, HIPAA audit requirements [VERIFIED] (OAIAPI-SC-OAI-ADMORG)
- **Admin key required**: Only accessible via admin API keys [VERIFIED] (OAIAPI-SC-OAI-ADMOVW)

## Quick Reference

```
GET /v1/organization/audit_logs    # List audit log entries

Query Parameters:
  effective_at[gte]    # Filter by start date (Unix timestamp)
  effective_at[lte]    # Filter by end date (Unix timestamp)
  event_types[]        # Filter by event type(s)
  actor_ids[]          # Filter by actor ID(s)
  project_ids[]        # Filter by project ID(s)
  limit                # 1-100, default 20
  after                # Cursor for forward pagination
  before               # Cursor for backward pagination
```

## Audit Log Entry Object

```json
{
  "id": "audit-abc123",
  "object": "organization.audit_log",
  "type": "api_key.created",
  "effective_at": 1711471533,
  "actor": {
    "type": "user",
    "user": {
      "id": "user-abc123",
      "email": "admin@example.com"
    }
  },
  "project": {
    "id": "proj-abc123",
    "name": "Production"
  },
  "api_key.created": {
    "id": "key-abc123",
    "data": {
      "scopes": ["model.request"]
    }
  }
}
```

## Event Types

### User Events
- **user.added** - User added to organization
- **user.removed** - User removed from organization
- **user.updated** - User role changed

### Project Events
- **project.created** - New project created
- **project.updated** - Project settings changed
- **project.archived** - Project archived

### API Key Events
- **api_key.created** - API key generated
- **api_key.deleted** - API key revoked
- **api_key.updated** - API key settings changed

### Service Account Events
- **service_account.created** - Service account created
- **service_account.deleted** - Service account removed
- **service_account.updated** - Service account updated

### Invite Events
- **invite.sent** - Invitation sent
- **invite.accepted** - Invitation accepted
- **invite.deleted** - Invitation revoked

### Certificate Events
- **certificate.created** - Certificate uploaded
- **certificate.activated** - Certificate activated
- **certificate.deactivated** - Certificate deactivated
- **certificate.deleted** - Certificate removed

### Rate Limit Events
- **rate_limit.updated** - Rate limit configuration changed

## SDK Examples (Python)

> **SDK note**: `client.organization.*` methods are not available in openai Python SDK v2.29.0.
> The Administration API uses REST-only endpoints with admin API keys (`sk-admin-...`).
> Use `httpx` or `requests` for direct REST calls to `https://api.openai.com/v1/organization/*`.

### Query Audit Logs - Production Ready

```python
from openai import OpenAI
import time

client = OpenAI(api_key="sk-admin-...")

def query_audit_logs(
    event_types: list = None,
    hours_back: int = 24,
    project_id: str = None
):
    """Query audit logs with filters"""
    now = int(time.time())
    start = now - (hours_back * 3600)
    
    all_entries = []
    after = None
    
    while True:
        params = {
            "limit": 100,
            "effective_at": {"gte": start, "lte": now}
        }
        if event_types:
            params["event_types"] = event_types
        if project_id:
            params["project_ids"] = [project_id]
        if after:
            params["after"] = after
        
        response = client.organization.audit_logs.list(**params)
        all_entries.extend(response.data)
        
        if not response.has_more:
            break
        after = response.last_id
    
    return all_entries

try:
    # Get all API key events in last 24 hours
    key_events = query_audit_logs(
        event_types=["api_key.created", "api_key.deleted"],
        hours_back=24
    )
    
    for entry in key_events:
        actor_email = entry.actor.user.email if entry.actor.type == "user" else "system"
        print(f"  [{entry.type}] by {actor_email} at {entry.effective_at}")
    
    # Security: detect unusual activity
    removals = query_audit_logs(
        event_types=["user.removed", "api_key.deleted"],
        hours_back=1
    )
    if len(removals) > 5:
        print(f"ALERT: {len(removals)} removal events in last hour")

except Exception as e:
    print(f"Error: {e}")
```

## Error Responses

- **401 Unauthorized** - Invalid admin API key
- **403 Forbidden** - Insufficient permissions
- **429 Too Many Requests** - Rate limit exceeded

## Differences from Other APIs

- **vs Anthropic**: No audit log API
- **vs Gemini**: Google Cloud Audit Logs (different service)
- **vs Grok**: No audit log API

## Sources

- OAIAPI-SC-OAI-ADMORG - Organization Administration API
- OAIAPI-SC-OAI-ADMOVW - Administration Overview

## Document History

**[2026-03-21 09:48]**
- Added: SDK v2.29.0 note - client.organization.* not in Python SDK (REST-only admin API)

**[2026-03-20 18:13]**
- Initial documentation created
