# Conversations API

**Doc ID**: OAIAPI-IN08
**Goal**: Document Conversations API for persistent multi-turn state management
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references
- `_INFO_OAIAPI-IN06_RESPONSES_API.md [OAIAPI-IN06]` for Responses API integration

## Summary

The Conversations API provides persistent multi-turn conversation state management for Responses API. Create conversations with POST /v1/conversations, link responses via conversation_id parameter, and maintain context across multiple API calls without resending full message history. Conversations store all input items and responses, supporting CRUD operations (create, retrieve, update, delete). Items can be added, retrieved, updated, and deleted individually. Conversations enable stateful interactions, reduce token usage by avoiding history repetition, and support conversation metadata for organization. Conversations persist until explicitly deleted or after retention period. Compatible with all Responses API features including tools, structured outputs, and streaming. Replaces deprecated Assistants API threads for conversation management. [VERIFIED] (OAIAPI-SC-OAI-CNVCRT, OAIAPI-SC-OAI-CNVGET)

## Key Facts

- **Endpoints**: POST/GET/PATCH/DELETE /v1/conversations [VERIFIED] (OAIAPI-SC-OAI-CNVCRT)
- **Purpose**: Persistent conversation state across multiple responses [VERIFIED] (OAIAPI-SC-OAI-CNVCRT)
- **Items API**: Manage individual messages in conversation [VERIFIED] (OAIAPI-SC-OAI-CNVITM)
- **Integration**: Link to responses via conversation_id parameter [VERIFIED] (OAIAPI-SC-OAI-RESCRT)
- **Replaces**: Deprecated Assistants API threads [VERIFIED] (OAIAPI-SC-OAI-LGASST)

## Use Cases

- **Multi-turn chat**: Maintain context across conversation turns
- **Token optimization**: Avoid resending full message history
- **Conversation management**: Organize and persist user conversations
- **Context preservation**: Store long-term conversation state

## Quick Reference

```python
# Create conversation
POST /v1/conversations
{"metadata": {"user_id": "123"}}

# Link response to conversation
POST /v1/responses
{
  "conversation_id": "conv_abc123",
  "model": "gpt-5.4",
  "input": [{"role": "user", "content": "Hello"}]
}

# Retrieve conversation
GET /v1/conversations/conv_abc123

# Delete conversation
DELETE /v1/conversations/conv_abc123
```

## Conversation Object

### Schema

```json
{
  "id": "conv_abc123",
  "object": "conversation",
  "created_at": 1234567890,
  "metadata": {
    "user_id": "user_123",
    "session_id": "session_456"
  }
}
```

### Fields

- **id**: Unique conversation identifier
- **object**: Always "conversation"
- **created_at**: Unix timestamp
- **metadata**: Custom key-value pairs (optional)

## Conversation Operations

### Create Conversation

```
POST /v1/conversations
```

**Request:**
```json
{
  "metadata": {
    "user_id": "user_123",
    "context": "customer_support"
  }
}
```

**Response:**
```json
{
  "id": "conv_abc123",
  "object": "conversation",
  "created_at": 1234567890,
  "metadata": {
    "user_id": "user_123",
    "context": "customer_support"
  }
}
```

### Retrieve Conversation

```
GET /v1/conversations/{conversation_id}
```

Returns conversation object with metadata.

### Update Conversation

```
PATCH /v1/conversations/{conversation_id}
```

**Request:**
```json
{
  "metadata": {
    "status": "resolved"
  }
}
```

Updates conversation metadata.

### Delete Conversation

```
DELETE /v1/conversations/{conversation_id}
```

Permanently deletes conversation and all items.

## Conversation Items

### Item Types

- **Messages**: User and assistant messages
- **Tool calls**: Function calls and results
- **System prompts**: System instructions

### List Items

```
GET /v1/conversations/{conversation_id}/items
```

Returns all items in conversation.

### Create Item

```
POST /v1/conversations/{conversation_id}/items
```

Add message to conversation:
```json
{
  "role": "user",
  "content": [
    {"type": "text", "text": "Hello"}
  ]
}
```

### Update Item

```
PATCH /v1/conversations/{conversation_id}/items/{item_id}
```

Modify existing item.

### Delete Item

```
DELETE /v1/conversations/{conversation_id}/items/{item_id}
```

Remove item from conversation.

## Integration with Responses API

### Linking Responses

```python
# Create conversation
conversation = client.conversations.create()

# First response
response1 = client.responses.create(
    model="gpt-5.4",
    conversation_id=conversation.id,
    input=[
        {"role": "user", "content": "What is AI?"}
    ]
)

# Second response (with context)
response2 = client.responses.create(
    model="gpt-5.4",
    conversation_id=conversation.id,
    input=[
        {"role": "user", "content": "Give me an example"}
    ]
)
```

### Context Preservation

Conversation automatically maintains:
- All previous input items
- All response outputs
- Tool call history
- Metadata across turns

## SDK Examples (Python)

### Basic Conversation Flow

```python
from openai import OpenAI

client = OpenAI()

# Create conversation
conversation = client.conversations.create(
    metadata={"user_id": "user_123"}
)

print(f"Conversation ID: {conversation.id}")

# Turn 1
response1 = client.responses.create(
    model="gpt-5.4",
    conversation_id=conversation.id,
    input=[
        {"role": "user", "content": "My name is Alice"}
    ]
)
print(response1.output[0].content[0].text)

# Turn 2 (model remembers name)
response2 = client.responses.create(
    model="gpt-5.4",
    conversation_id=conversation.id,
    input=[
        {"role": "user", "content": "What's my name?"}
    ]
)
print(response2.output[0].content[0].text)  # "Your name is Alice"
```

### Conversation with Metadata

```python
from openai import OpenAI

client = OpenAI()

# Create with metadata
conversation = client.conversations.create(
    metadata={
        "user_id": "user_456",
        "session_type": "support",
        "started_at": "2026-03-20T15:00:00Z"
    }
)

# Update metadata
client.conversations.update(
    conversation.id,
    metadata={
        "status": "in_progress",
        "agent_id": "agent_789"
    }
)

# Retrieve with metadata
conv = client.conversations.retrieve(conversation.id)
print(conv.metadata)
```

### Managing Conversation Items

```python
from openai import OpenAI

client = OpenAI()

conversation = client.conversations.create()

# Add system message
client.conversations.items.create(
    conversation.id,
    role="system",
    content=[
        {"type": "text", "text": "You are a helpful assistant"}
    ]
)

# List all items
items = client.conversations.items.list(conversation.id)
for item in items.data:
    print(f"{item.role}: {item.content[0].text}")

# Delete specific item
client.conversations.items.delete(conversation.id, items.data[0].id)
```

### Managing Conversation Items (SDK v2.29.0 verified)

```python
# Source: openai v2.29.0 - resources/conversations/items.py
# items.create(conversation_id, items=[...], include=[...])
# Note: uses 'items' list param, not role/content directly
from openai import OpenAI

client = OpenAI()

conversation = client.conversations.create()

# Add system message via items list
client.conversations.items.create(
    conversation.id,
    items=[
        {
            "type": "message",
            "role": "system",
            "content": [{"type": "input_text", "text": "You are a helpful assistant"}]
        }
    ]
)

# List all items
items = client.conversations.items.list(conversation.id)
for item in items.data:
    print(f"{item.role}: {item.content[0].text}")

# Delete specific item
client.conversations.items.delete(conversation.id, items.data[0].id)
```

### Production Pattern

```python
from openai import OpenAI
from typing import Optional

class ConversationManager:
    def __init__(self):
        self.client = OpenAI()
    
    def create_user_conversation(self, user_id: str) -> str:
        """Create conversation for user"""
        conv = self.client.conversations.create(
            metadata={"user_id": user_id}
        )
        return conv.id
    
    def send_message(
        self,
        conversation_id: str,
        message: str,
        model: str = "gpt-5.4"
    ) -> str:
        """Send message and get response"""
        response = self.client.responses.create(
            model=model,
            conversation_id=conversation_id,
            input=[
                {"role": "user", "content": message}
            ]
        )
        return response.output[0].content[0].text
    
    def cleanup_conversation(self, conversation_id: str):
        """Delete conversation"""
        self.client.conversations.delete(conversation_id)

# Usage
manager = ConversationManager()
conv_id = manager.create_user_conversation("user_123")

reply1 = manager.send_message(conv_id, "Hello")
reply2 = manager.send_message(conv_id, "Tell me more")

manager.cleanup_conversation(conv_id)
```

### Production Pattern (SDK v2.29.0 verified)

```python
# Source: openai v2.29.0 - resources/responses/responses.py
# responses.create uses conversation={"id": "..."} not conversation_id="..."
from openai import OpenAI
from typing import Optional

class ConversationManager:
    def __init__(self):
        self.client = OpenAI()
    
    def create_user_conversation(self, user_id: str) -> str:
        conv = self.client.conversations.create(
            metadata={"user_id": user_id}
        )
        return conv.id
    
    def send_message(
        self,
        conversation_id: str,
        message: str,
        model: str = "gpt-4.1"
    ) -> str:
        response = self.client.responses.create(
            model=model,
            conversation={"id": conversation_id},
            input=[
                {"role": "user", "content": message}
            ]
        )
        return response.output[0].content[0].text
    
    def cleanup_conversation(self, conversation_id: str):
        self.client.conversations.delete(conversation_id)

# Usage
manager = ConversationManager()
conv_id = manager.create_user_conversation("user_123")

reply1 = manager.send_message(conv_id, "Hello")
reply2 = manager.send_message(conv_id, "Tell me more")

manager.cleanup_conversation(conv_id)
```

## Error Responses

- **404 Not Found** - Conversation or item does not exist
- **400 Bad Request** - Invalid conversation ID or item data
- **403 Forbidden** - Access denied to conversation

## Rate Limiting / Throttling

- **Conversation operations**: Count toward project RPM limits
- **Item operations**: Each CRUD operation counts as request

## Differences from Other APIs

- **vs Assistants Threads**: Conversations are simpler, no run concept, direct response integration
- **vs Anthropic**: Anthropic has no built-in conversation persistence (stateless)
- **vs Gemini**: Gemini cachedContents similar but different API structure

## Limitations and Known Issues

- **Retention period**: Conversations deleted after inactivity period [VERIFIED] (OAIAPI-SC-OAI-CNVCRT)
- **Item limit**: Maximum items per conversation [COMMUNITY] (OAIAPI-SC-SO-CONVLIM)
- **Metadata size**: Limited metadata storage per conversation [COMMUNITY] (OAIAPI-SC-SO-METALIM)

## Gotchas and Quirks

- **Automatic item addition**: Responses automatically add items to conversation [VERIFIED] (OAIAPI-SC-OAI-CNVCRT)
- **Metadata merge**: Update merges with existing metadata, not replace [VERIFIED] (OAIAPI-SC-OAI-CNVUPD)
- **Delete is permanent**: No recovery after conversation deletion [VERIFIED] (OAIAPI-SC-OAI-CNVDEL)

## Sources

- OAIAPI-SC-OAI-CNVCRT - POST Create a conversation
- OAIAPI-SC-OAI-CNVGET - GET Retrieve a conversation
- OAIAPI-SC-OAI-CNVUPD - POST Update a conversation
- OAIAPI-SC-OAI-CNVDEL - DELETE Delete a conversation
- OAIAPI-SC-OAI-CNVITM - Conversation Items CRUD

## Document History

**[2026-03-21 09:20]**
- Added: SDK v2.29.0 verified companion for conversations.items.create (items= param)
- Added: SDK v2.29.0 verified companion for Production Pattern (conversation= param)

**[2026-03-20 15:12]**
- Initial documentation created
