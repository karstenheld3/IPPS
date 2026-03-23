# Skills API

**Doc ID**: OAIAPI-IN17
**Goal**: Document Skills API for reusable tool packages, versioning, and tool_search integration
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references
- `_INFO_OAIAPI-IN12_TOOLS_OVERVIEW.md [OAIAPI-IN12]` for tools context

## Summary

The Skills API provides reusable tool packages with versioning support. Create skills containing multiple function definitions, manage versions independently, and enable dynamic discovery via tool_search. Skills support CRUD operations: create (POST /v1/skills), retrieve (GET /v1/skills/{skill_id}), list (GET /v1/skills), delete (DELETE /v1/skills/{skill_id}). Each skill has name, description, functions array, and version. Versions are immutable once published - create new version for updates. Content retrieval via GET /v1/skills/{skill_id}/versions/{version}/content returns skill definition. tool_search built-in tool enables models to discover and use skills dynamically without explicit skill IDs. Skills enable: reusable tool libraries, version management, team sharing, marketplace distribution. Relatively new API with limited documentation. [VERIFIED] (OAIAPI-SC-OAI-SKLAPI)

## Key Facts

- **Purpose**: Reusable tool packages with versioning [VERIFIED] (OAIAPI-SC-OAI-SKLAPI)
- **Operations**: Create, retrieve, list, delete skills [VERIFIED] (OAIAPI-SC-OAI-SKLAPI)
- **Versioning**: Immutable versions, create new for updates [VERIFIED] (OAIAPI-SC-OAI-SKLAPI)
- **Discovery**: tool_search enables dynamic skill discovery [VERIFIED] (OAIAPI-SC-OAI-SKLAPI)
- **Content**: Skills contain multiple function definitions [VERIFIED] (OAIAPI-SC-OAI-SKLAPI)

## Use Cases

- **Tool libraries**: Package related functions together
- **Team collaboration**: Share skills across projects
- **Version control**: Manage tool versions independently
- **Dynamic discovery**: Let models find relevant skills
- **Marketplace**: Distribute reusable skills

## Quick Reference

```python
# Create skill
POST /v1/skills
{
  "name": "weather_tools",
  "description": "Weather-related tools",
  "functions": [...]
}

# Use skill with tool_search
tools=[{"type": "tool_search"}]
```

## Skill Object

### Schema

```json
{
  "id": "skill_abc123",
  "object": "skill",
  "name": "weather_tools",
  "description": "Tools for weather information",
  "version": "1.0.0",
  "created_at": 1234567890,
  "functions": [
    {
      "name": "get_weather",
      "description": "Get current weather",
      "parameters": {...}
    }
  ]
}
```

### Fields

- **id**: Unique skill identifier
- **object**: Always "skill"
- **name**: Skill name (unique per account)
- **description**: What the skill does
- **version**: Semantic version (e.g., "1.0.0")
- **created_at**: Unix timestamp
- **functions**: Array of function definitions

## Skill Operations

### Create Skill

```
POST /v1/skills
```

**Request:**
```json
{
  "name": "database_tools",
  "description": "Database query and update tools",
  "version": "1.0.0",
  "functions": [
    {
      "name": "query_users",
      "description": "Query user database",
      "parameters": {
        "type": "object",
        "properties": {
          "filter": {"type": "string"}
        }
      }
    }
  ]
}
```

### Retrieve Skill

```
GET /v1/skills/{skill_id}
```

Returns skill metadata and function definitions.

### List Skills

```
GET /v1/skills
```

Returns all skills in account.

### Delete Skill

```
DELETE /v1/skills/{skill_id}
```

Permanently deletes skill and all versions.

### Get Skill Content

```
GET /v1/skills/{skill_id}/versions/{version}/content
```

Returns specific version's function definitions.

## Versioning

### Version Format

Semantic versioning: `MAJOR.MINOR.PATCH`
- **MAJOR**: Breaking changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes

### Creating New Version

```python
# Create new version
client.skills.create(
    name="weather_tools",  # Same name
    version="1.1.0",  # New version
    description="Updated weather tools",
    functions=[...]  # Updated functions
)
```

### Version Immutability

Once created, versions cannot be modified. Create new version for changes.

## tool_search Integration

### Enabling Dynamic Discovery

```python
tools=[
    {"type": "tool_search"}
]
```

Model discovers and uses relevant skills automatically.

### Discovery Process

1. **Model analyzes request**: Determines needed capabilities
2. **Searches skills**: Finds relevant skills by name/description
3. **Loads functions**: Retrieves skill function definitions
4. **Executes**: Calls appropriate functions
5. **Returns results**: Uses skill outputs in response

## SDK Examples (Python)

### Create Skill

```python
from openai import OpenAI

client = OpenAI()

skill = client.skills.create(
    name="calculation_tools",
    description="Mathematical calculation tools",
    version="1.0.0",
    functions=[
        {
            "name": "calculate",
            "description": "Perform mathematical calculation",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string"}
                },
                "required": ["expression"]
            }
        },
        {
            "name": "convert_units",
            "description": "Convert between units",
            "parameters": {
                "type": "object",
                "properties": {
                    "value": {"type": "number"},
                    "from_unit": {"type": "string"},
                    "to_unit": {"type": "string"}
                },
                "required": ["value", "from_unit", "to_unit"]
            }
        }
    ]
)

print(f"Created skill: {skill.id}")
```

### Create Skill (SDK v2.29.0 verified)

```python
# Source: openai v2.29.0 - resources/skills/skills.py
# SDK skills.create(files=...) accepts file upload only, not name/functions directly
# Skill definition is uploaded as a file; metadata passed via extra_body
from openai import OpenAI
import json, tempfile, os

client = OpenAI()

# SDK accepts file upload - create skill definition as file
skill_def = {
    "name": "calculation_tools",
    "description": "Mathematical calculation tools",
    "version": "1.0.0",
    "functions": [
        {
            "name": "calculate",
            "description": "Perform mathematical calculation",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string"}
                },
                "required": ["expression"]
            }
        }
    ]
}

# Write definition to temp file and upload
with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
    json.dump(skill_def, f)
    tmp_path = f.name

try:
    skill = client.skills.create(files=open(tmp_path, "rb"))
    print(f"Created skill: {skill.id}")
finally:
    os.unlink(tmp_path)
```

### List Skills

```python
from openai import OpenAI

client = OpenAI()

skills = client.skills.list()

for skill in skills.data:
    print(f"{skill.name} v{skill.version}: {skill.description}")
    print(f"  Functions: {', '.join(f['name'] for f in skill.functions)}")
```

### Retrieve Skill

```python
from openai import OpenAI

client = OpenAI()

skill = client.skills.retrieve("skill_abc123")

print(f"Name: {skill.name}")
print(f"Version: {skill.version}")
print(f"Functions: {len(skill.functions)}")
```

### Using Skills with tool_search

```python
from openai import OpenAI

client = OpenAI()

# Create skill first
client.skills.create(
    name="weather_api",
    description="Real-time weather information tools",
    version="1.0.0",
    functions=[
        {
            "name": "get_current_weather",
            "description": "Get current weather for location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"}
                },
                "required": ["location"]
            }
        }
    ]
)

# Use with tool_search
response = client.responses.create(
    model="gpt-5.4",
    input=[
        {
            "role": "user",
            "content": "What's the weather in Seattle? Use available weather tools."
        }
    ],
    tools=[
        {"type": "tool_search"}  # Model discovers weather_api skill
    ]
)

print(response.output[0].content[0].text)
```

### Version Management

```python
from openai import OpenAI

client = OpenAI()

# Create v1.0.0
skill_v1 = client.skills.create(
    name="data_tools",
    version="1.0.0",
    description="Data processing tools",
    functions=[
        {
            "name": "process_data",
            "description": "Process data",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {"type": "array", "items": {"type": "string"}}
                }
            }
        }
    ]
)

# Create v1.1.0 with new function
skill_v1_1 = client.skills.create(
    name="data_tools",  # Same name
    version="1.1.0",  # New version
    description="Data processing tools with validation",
    functions=[
        {
            "name": "process_data",
            "description": "Process data",
            "parameters": {...}
        },
        {
            "name": "validate_data",  # New function
            "description": "Validate data format",
            "parameters": {...}
        }
    ]
)

print(f"v1.0.0: {skill_v1.id}")
print(f"v1.1.0: {skill_v1_1.id}")
```

### Delete Skill

```python
from openai import OpenAI

client = OpenAI()

client.skills.delete("skill_abc123")
print("Skill deleted")
```

## Error Responses

- **404 Not Found** - Skill or version does not exist
- **400 Bad Request** - Invalid skill definition
- **409 Conflict** - Skill name/version already exists

## Rate Limiting / Throttling

- **Skill operations**: Count toward project RPM limits
- **tool_search usage**: Skill discovery counts as tool usage

## Differences from Other APIs

- **vs Anthropic**: No equivalent skills system in Anthropic
- **vs Gemini**: No equivalent in Gemini
- **vs OpenAI Plugins (legacy)**: Skills are API-level, not ChatGPT plugins

## Limitations and Known Issues

- **Limited documentation**: Relatively new API, docs sparse [VERIFIED] (OAIAPI-SC-OAI-SKLAPI)
- **tool_search reliability**: Discovery not always accurate [COMMUNITY] (OAIAPI-SC-SO-TOOLSRCH)
- **No skill marketplace**: No public skill sharing yet [COMMUNITY] (OAIAPI-SC-SO-SKLMKT)

## Gotchas and Quirks

- **Name must be unique**: Cannot have multiple skills with same name in account [VERIFIED] (OAIAPI-SC-OAI-SKLAPI)
- **Versions immutable**: Cannot edit existing versions [VERIFIED] (OAIAPI-SC-OAI-SKLAPI)
- **tool_search overhead**: Discovery adds latency vs direct function calling [COMMUNITY] (OAIAPI-SC-SO-DISCOV)

## Sources

- OAIAPI-SC-OAI-SKLAPI - Skills API reference
- OAIAPI-SC-OAI-GTOOLS - Tools overview (tool_search)

## Document History

**[2026-03-21 09:30]**
- Added: SDK v2.29.0 verified companion for skills.create (files= param, not name/functions)

**[2026-03-20 15:37]**
- Initial documentation created
