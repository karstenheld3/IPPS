# Response Input Items

**Doc ID**: OAIAPI-IN10
**Goal**: Document API for listing input items associated with a response
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references
- `_INFO_OAIAPI-IN06_RESPONSES_API.md [OAIAPI-IN06]` for Responses API context

## Summary

The Response Input Items API (GET /v1/responses/{response_id}/input_items) retrieves the input items that were provided to generate a specific response. Returns paginated list of input messages, system prompts, and other input content used in response generation. Useful for auditing, debugging, and understanding what context was provided to model. Each item includes role, content, and metadata. Supports pagination for long input histories. Items returned in chronological order. Works with both direct responses and conversation-linked responses. [VERIFIED] (OAIAPI-SC-OAI-RESINP)

## Key Facts

- **Endpoint**: GET /v1/responses/{response_id}/input_items [VERIFIED] (OAIAPI-SC-OAI-RESINP)
- **Purpose**: Retrieve input items for audit and debugging [VERIFIED] (OAIAPI-SC-OAI-RESINP)
- **Pagination**: Supports limit and cursor parameters [VERIFIED] (OAIAPI-SC-OAI-RESINP)
- **Order**: Items returned chronologically [VERIFIED] (OAIAPI-SC-OAI-RESINP)
- **Content**: Includes full input content and metadata [VERIFIED] (OAIAPI-SC-OAI-RESINP)

## Use Cases

- **Audit logging**: Track what inputs generated specific responses
- **Debugging**: Verify input sent to model
- **Compliance**: Record interactions for regulatory requirements
- **Analytics**: Analyze input patterns and content

## Quick Reference

```python
GET /v1/responses/{response_id}/input_items?limit=20

# Response:
{
  "object": "list",
  "data": [
    {
      "id": "item_abc",
      "role": "user",
      "content": [{"type": "text", "text": "Hello"}]
    }
  ],
  "has_more": false
}
```

## Request Parameters

### Path Parameters

- **response_id**: Response ID to retrieve input items for

### Query Parameters

- **limit**: Number of items to return (default: 20, max: 100)
- **after**: Cursor for pagination (item ID)
- **before**: Cursor for reverse pagination (item ID)

## Response Schema

```json
{
  "object": "list",
  "data": [
    {
      "id": "item_abc123",
      "object": "conversation.item",
      "type": "message",
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "What is quantum computing?"
        }
      ],
      "created_at": 1234567890
    },
    {
      "id": "item_def456",
      "object": "conversation.item",
      "type": "message",
      "role": "system",
      "content": [
        {
          "type": "text",
          "text": "You are a helpful assistant"
        }
      ],
      "created_at": 1234567880
    }
  ],
  "first_id": "item_abc123",
  "last_id": "item_def456",
  "has_more": false
}
```

### List Object Fields

- **object**: Always "list"
- **data**: Array of input item objects
- **first_id**: ID of first item in page
- **last_id**: ID of last item in page
- **has_more**: Whether more items exist

### Item Object Fields

- **id**: Unique item identifier
- **object**: Object type ("conversation.item")
- **type**: Item type (message, function_call, etc.)
- **role**: Role (user, assistant, system, tool)
- **content**: Array of content objects
- **created_at**: Unix timestamp

## Pagination

### Forward Pagination

```python
# First page
GET /v1/responses/{response_id}/input_items?limit=20

# Next page
GET /v1/responses/{response_id}/input_items?limit=20&after={last_id}
```

### Reverse Pagination

```python
# Last page
GET /v1/responses/{response_id}/input_items?limit=20&before={first_id}
```

## SDK Examples (Python)

### List All Input Items

```python
from openai import OpenAI

client = OpenAI()

# Create response first
response = client.responses.create(
    model="gpt-5.4",
    input=[
        {"role": "system", "content": "You are helpful"},
        {"role": "user", "content": "Hello"}
    ]
)

# List input items
items = client.responses.input_items.list(response.id)

for item in items.data:
    print(f"{item.role}: {item.content[0].text}")
```

### Paginated Retrieval

```python
from openai import OpenAI

client = OpenAI()

response_id = "resp_abc123"

all_items = []
after = None

while True:
    items = client.responses.input_items.list(
        response_id,
        limit=100,
        after=after
    )
    
    all_items.extend(items.data)
    
    if not items.has_more:
        break
    
    after = items.last_id

print(f"Total input items: {len(all_items)}")
```

### Audit Logger

```python
from openai import OpenAI
import json
from datetime import datetime

class ResponseAuditor:
    def __init__(self):
        self.client = OpenAI()
    
    def audit_response(self, response_id: str, output_file: str):
        """Audit response inputs and save to file"""
        items = self.client.responses.input_items.list(response_id)
        
        audit_data = {
            "response_id": response_id,
            "audited_at": datetime.utcnow().isoformat(),
            "input_items": []
        }
        
        for item in items.data:
            audit_data["input_items"].append({
                "id": item.id,
                "role": item.role,
                "type": item.type,
                "content": [c.text if c.type == "text" else c.type 
                           for c in item.content],
                "created_at": item.created_at
            })
        
        with open(output_file, 'w') as f:
            json.dump(audit_data, f, indent=2)
        
        return audit_data

# Usage
auditor = ResponseAuditor()
audit = auditor.audit_response("resp_abc123", "audit_log.json")
print(f"Audited {len(audit['input_items'])} input items")
```

### Input Verification

```python
from openai import OpenAI

def verify_input_sent(response_id: str, expected_content: str) -> bool:
    """Verify specific content was sent in input"""
    client = OpenAI()
    
    items = client.responses.input_items.list(response_id)
    
    for item in items.data:
        for content in item.content:
            if content.type == "text" and expected_content in content.text:
                return True
    
    return False

# Usage
if verify_input_sent("resp_abc123", "quantum computing"):
    print("Input verified")
else:
    print("Input not found")
```

### Conversation History Reconstruction

```python
from openai import OpenAI

def reconstruct_conversation(response_id: str):
    """Reconstruct full conversation from input items"""
    client = OpenAI()
    
    items = client.responses.input_items.list(response_id, limit=100)
    
    conversation = []
    for item in items.data:
        if item.type == "message":
            conversation.append({
                "role": item.role,
                "content": item.content[0].text if item.content else ""
            })
    
    return conversation

# Usage
history = reconstruct_conversation("resp_abc123")
for msg in history:
    print(f"{msg['role']}: {msg['content']}")
```

## Error Responses

- **404 Not Found** - Response ID does not exist
- **400 Bad Request** - Invalid pagination parameters
- **403 Forbidden** - Access denied to response

## Rate Limiting / Throttling

- **List operations**: Count toward project RPM limits
- **Pagination**: Each page request counts as separate API call

## Differences from Other APIs

- **vs Chat Completions**: No equivalent input listing in Chat Completions API
- **vs Anthropic**: Anthropic doesn't provide input retrieval endpoint
- **vs Conversations Items**: This lists inputs for specific response, not full conversation

## Limitations and Known Issues

- **Tool outputs not included**: Only input items, not tool execution results [VERIFIED] (OAIAPI-SC-OAI-RESINP)
- **Max page size**: Limited to 100 items per request [VERIFIED] (OAIAPI-SC-OAI-RESINP)
- **No filtering**: Cannot filter by role or type [COMMUNITY] (OAIAPI-SC-SO-ITEMFILT)

## Gotchas and Quirks

- **Conversation context**: For conversation-linked responses, only shows input array, not full conversation history [VERIFIED] (OAIAPI-SC-OAI-RESINP)
- **Order**: Items in chronological order, oldest first [VERIFIED] (OAIAPI-SC-OAI-RESINP)
- **Cursor-based pagination**: Uses item IDs as cursors, not offset-based [VERIFIED] (OAIAPI-SC-OAI-RESINP)

## Sources

- OAIAPI-SC-OAI-RESINP - GET List input items
- OAIAPI-SC-OAI-RESCRT - POST Create a response

## Document History

**[2026-03-20 15:18]**
- Initial documentation created
