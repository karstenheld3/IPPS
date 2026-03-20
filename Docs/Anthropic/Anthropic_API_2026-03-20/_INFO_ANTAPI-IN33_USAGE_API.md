# Admin API: Usage Reports

**Doc ID**: ANTAPI-IN33
**Goal**: Document usage reporting endpoints for messages and Claude Code
**API version**: anthropic-version 2023-06-01

**Depends on:**
- `_INFO_ANTAPI-IN30_ADMIN_ORGS.md [ANTAPI-IN30]` for organization context

## Summary

The Usage Report endpoints provide detailed token consumption and cost data. Two report types exist: Messages usage (API token consumption by model, workspace, API key, context window, inference geo, service tier) and Claude Code usage (developer productivity metrics including commits, code changes, sessions, PRs). Reports support time-based bucketing, grouping dimensions, and cursor pagination.

## Key Facts

- **Messages Report**: `GET /v1/usage/messages`
- **Claude Code Report**: `GET /v1/usage/claude_code`
- **Grouping**: model, workspace_id, api_key_id, context_window, inference_geo, service_tier, speed
- **Time Buckets**: start_time, end_time in RFC 3339 format
- **Pagination**: Cursor-based with `has_more` and `next_page` fields
- **Status**: GA

## Messages Usage Report

### GET /v1/usage/messages

```python
import anthropic

client = anthropic.Anthropic()

# Get usage grouped by model
usage = client.admin.usage_report.retrieve_messages(
    start_time="2026-03-01T00:00:00Z",
    end_time="2026-03-20T00:00:00Z",
    group_by=["model"],
)

for bucket in usage.data:
    print(f"Period: {bucket.start_time} - {bucket.end_time}")
    for item in bucket.items:
        print(f"  Model: {item.model}")
        print(f"  Input tokens: {item.input_tokens}")
        print(f"  Output tokens: {item.output_tokens}")
        print(f"  Cache read: {item.cache_read_input_tokens}")
        print(f"  Cache write: {item.cache_creation_input_tokens}")
```

### Usage Item Fields

- **input_tokens** (`integer`) - Uncached input tokens
- **output_tokens** (`integer`) - Output tokens generated
- **cache_read_input_tokens** (`integer`) - Tokens read from cache
- **cache_creation_input_tokens** (`integer`) - Tokens written to cache
- **cache_creation_input_tokens_5m** (`integer`) - 5-minute cache writes
- **cache_creation_input_tokens_1h** (`integer`) - 1-hour cache writes
- **model** (`string | null`) - Model used (if grouping by model)
- **workspace_id** (`string | null`) - Workspace (if grouping by workspace)
- **api_key_id** (`string | null`) - API key (if grouping by api_key)
- **context_window** (`string | null`) - Context window tier
- **inference_geo** (`string | null`) - Inference geography
- **service_tier** (`string | null`) - Service tier
- **speed** (`string | null`) - Speed tier (requires fast-mode beta header)
- **server_tool_usage** (`object`) - Server tool metrics:
  - **web_search_requests** (`integer`) - Web searches performed

## Claude Code Usage Report

### GET /v1/usage/claude_code

```python
usage = client.admin.usage_report.retrieve_claude_code(
    start_time="2026-03-01T00:00:00Z",
    end_time="2026-03-20T00:00:00Z",
)

for record in usage.data:
    print(f"Date: {record.date}")
    print(f"Actor: {record.actor.email}")
    print(f"Sessions: {record.core_metrics.sessions}")
    print(f"Commits: {record.core_metrics.git_commits}")
    print(f"Lines added: {record.core_metrics.code_changes.lines_added}")
```

### Claude Code Usage Fields

- **date** (`string`) - UTC date (YYYY-MM-DD)
- **actor** - User or API key identity
  - **email** / **api_key_name** (`string`)
- **core_metrics** - Productivity metrics:
  - **sessions** (`integer`) - Distinct sessions
  - **git_commits** (`integer`) - Commits created
  - **pull_requests** (`integer`) - PRs created
  - **code_changes** - Code modification stats:
    - **lines_added** (`integer`)
    - **lines_removed** (`integer`)
- **model_usage** (`array`) - Per-model token breakdown:
  - **model** (`string`) - Model name
  - **tokens** - input, output, cache_read, cache_creation counts
  - **estimated_cost** - amount (minor units), currency
- **customer_type** (`string`) - "api" or "subscription"
- **terminal_type** (`string`) - Environment type
- **tool_actions** (`array`) - Acceptance/rejection rates by tool

## Gotchas and Quirks

- `group_by` parameters are passed as array query parameters (`group_by[]=model&group_by[]=workspace_id`)
- `speed` grouping requires the `fast-mode-2026-02-01` beta header
- `api_key_id` is null for Console usage (not via API key)
- `workspace_id` is null for default workspace usage
- Cost data in Claude Code report uses minor currency units (cents for USD)
- Pagination uses `has_more` boolean and `next_page` cursor token

## Related Endpoints

- `_INFO_ANTAPI-IN30_ADMIN_ORGS.md [ANTAPI-IN30]` - Organization context
- `_INFO_ANTAPI-IN32_ADMIN_WORKSPACES.md [ANTAPI-IN32]` - Workspace management
- `_INFO_ANTAPI-IN12_PRICING.md [ANTAPI-IN12]` - Token pricing rates

## Sources

- ANTAPI-SC-ANTH-ADMIN - https://platform.claude.com/docs/en/api/admin - Admin API reference (usage report section)

## Document History

**[2026-03-20 04:22]**
- Initial documentation created from Admin API reference
