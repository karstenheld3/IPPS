# Threads API

**Doc ID**: OAIAPI-IN32
**Goal**: Document Threads for persistent conversation state, messages, and run history
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references
- `_INFO_OAIAPI-IN31_ASSISTANTS.md [OAIAPI-IN31]` for Assistants context

## Summary

Threads API manages persistent conversation contexts for Assistants. Create thread (POST /v1/threads) to start conversation, add messages (POST /v1/threads/{thread_id}/messages), execute runs, and retrieve history. Threads store complete conversation state including user messages, assistant responses, tool outputs, and metadata. Support operations: create empty or with initial messages, retrieve metadata, modify metadata, delete thread. Messages ordered chronologically within thread. Each message has role (user/assistant), content array (text/images/file references), and attachments. Threads never auto-delete - persist until explicitly deleted. Use for multi-turn conversations, customer support sessions, ongoing tasks. Thread context passed to assistant during runs. Maximum context window applies - old messages may be truncated. Annotations reference files/citations in responses. [VERIFIED] (OAIAPI-SC-OAI-THRCRT, OAIAPI-SC-OAI-MSGCRT, OAIAPI-SC-OAI-GASSIST)

## Key Facts

- **Purpose**: Persistent conversation state [VERIFIED] (OAIAPI-SC-OAI-THRCRT)
- **Persistence**: Never auto-delete [VERIFIED] (OAIAPI-SC-OAI-THRCRT)
- **Messages**: User and assistant messages with attachments [VERIFIED] (OAIAPI-SC-OAI-MSGCRT)
- **Context window**: Subject to model limits [VERIFIED] (OAIAPI-SC-OAI-GASSIST)
- **Operations**: Create, retrieve, modify, delete [VERIFIED] (OAIAPI-SC-OAI-THRCRT)

## Use Cases

- **Multi-turn chat**: Persistent conversations
- **Customer support**: Track support sessions
- **Task workflows**: Ongoing task execution
- **User sessions**: Per-user conversation history
- **Context retention**: Maintain conversation state

## Quick Reference

```python
# Create empty thread
POST /v1/threads

# Create with messages
POST /v1/threads
{
  "messages": [
    {"role": "user", "content": "Hello"}
  ]
}

# Add message
POST /v1/threads/{thread_id}/messages
{
  "role": "user",
  "content": "Follow-up question"
}

# List messages
GET /v1/threads/{thread_id}/messages
```

## Thread Object

```json
{
  "id": "thread_abc123",
  "object": "thread",
  "created_at": 1234567890,
  "metadata": {
    "user_id": "user_123",
    "session": "support_001"
  }
}
```

## Message Object

```json
{
  "id": "msg_xyz789",
  "object": "thread.message",
  "created_at": 1234567890,
  "thread_id": "thread_abc123",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": {
        "value": "Hello! How can I help?",
        "annotations": []
      }
    }
  ],
  "assistant_id": "asst_def456",
  "run_id": "run_ghi789",
  "attachments": [],
  "metadata": {}
}
```

## Thread Operations

### Create Thread

Empty thread:
```
POST /v1/threads
```

With initial messages:
```
POST /v1/threads
{
  "messages": [
    {
      "role": "user",
      "content": "I need help with my order",
      "metadata": {"priority": "high"}
    }
  ],
  "metadata": {
    "user_id": "user_123",
    "channel": "email"
  }
}
```

### Retrieve Thread

```
GET /v1/threads/{thread_id}
```

### Modify Thread

Update metadata only:
```
POST /v1/threads/{thread_id}
{
  "metadata": {
    "status": "resolved"
  }
}
```

### Delete Thread

```
DELETE /v1/threads/{thread_id}
```

Permanently deletes thread and all messages.

## Message Operations

### Create Message

```
POST /v1/threads/{thread_id}/messages
{
  "role": "user",
  "content": "What's my order status?",
  "attachments": [
    {
      "file_id": "file_abc123",
      "tools": [{"type": "file_search"}]
    }
  ]
}
```

### List Messages

```
GET /v1/threads/{thread_id}/messages
```

**Query parameters:**
- **limit**: Number of messages (default 20, max 100)
- **order**: "asc" or "desc" (default "desc" - newest first)
- **after**: Cursor for pagination
- **before**: Cursor for pagination

### Retrieve Message

```
GET /v1/threads/{thread_id}/messages/{message_id}
```

### Modify Message

Update metadata only:
```
POST /v1/threads/{thread_id}/messages/{message_id}
{
  "metadata": {"reviewed": "true"}
}
```

## Message Content Types

### Text

```json
{
  "type": "text",
  "text": {
    "value": "Response text",
    "annotations": [
      {
        "type": "file_citation",
        "text": "[1]",
        "file_citation": {
          "file_id": "file_abc",
          "quote": "Relevant quote"
        },
        "start_index": 10,
        "end_index": 13
      }
    ]
  }
}
```

### Image File

```json
{
  "type": "image_file",
  "image_file": {
    "file_id": "file_xyz789"
  }
}
```

### Image URL

```json
{
  "type": "image_url",
  "image_url": {
    "url": "https://example.com/image.jpg"
  }
}
```

## Annotations

### File Citation

References file chunks:
```json
{
  "type": "file_citation",
  "text": "[1]",
  "file_citation": {
    "file_id": "file_abc123",
    "quote": "Quote from file"
  },
  "start_index": 50,
  "end_index": 53
}
```

### File Path

References generated files:
```json
{
  "type": "file_path",
  "text": "sandbox:/file.csv",
  "file_path": {
    "file_id": "file_generated"
  },
  "start_index": 100,
  "end_index": 120
}
```

## SDK Examples (Python)

### Create and Use Thread

```python
from openai import OpenAI

client = OpenAI()

# Create thread
thread = client.beta.threads.create()
print(f"Thread ID: {thread.id}")

# Add message
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Hello, I need help"
)

# Run assistant
run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id="asst_abc123"
)

# Get messages
messages = client.beta.threads.messages.list(thread_id=thread.id)
for msg in messages.data:
    print(f"{msg.role}: {msg.content[0].text.value}")
```

### Create Thread with Initial Messages

```python
from openai import OpenAI

client = OpenAI()

thread = client.beta.threads.create(
    messages=[
        {
            "role": "user",
            "content": "I'm looking for product recommendations",
            "metadata": {"category": "electronics"}
        },
        {
            "role": "user",
            "content": "Budget is $500"
        }
    ],
    metadata={
        "user_id": "user_12345",
        "session_start": "2026-03-20T14:30:00Z"
    }
)

print(f"Created thread with {len(thread.messages)} initial messages")
```

### Multi-turn Conversation

```python
from openai import OpenAI

client = OpenAI()

thread = client.beta.threads.create()
assistant_id = "asst_abc123"

conversation = [
    "What's the weather like today?",
    "Should I bring an umbrella?",
    "What about a jacket?"
]

for user_msg in conversation:
    # Add user message
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_msg
    )
    
    # Run assistant
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant_id
    )
    
    # Get latest response
    messages = client.beta.threads.messages.list(
        thread_id=thread.id,
        limit=1
    )
    
    assistant_msg = messages.data[0].content[0].text.value
    print(f"User: {user_msg}")
    print(f"Assistant: {assistant_msg}\n")
```

### Message Pagination

```python
from openai import OpenAI

client = OpenAI()

thread_id = "thread_abc123"

# Get all messages (paginated)
all_messages = []
after = None

while True:
    messages = client.beta.threads.messages.list(
        thread_id=thread_id,
        limit=100,
        order="asc",
        after=after
    )
    
    all_messages.extend(messages.data)
    
    if not messages.has_more:
        break
    
    after = messages.data[-1].id

print(f"Total messages: {len(all_messages)}")
```

### With File Attachments

```python
from openai import OpenAI

client = OpenAI()

# Upload file
with open("data.csv", "rb") as f:
    file = client.files.create(file=f, purpose="assistants")

# Create thread with file
thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Analyze this data",
    attachments=[
        {
            "file_id": file.id,
            "tools": [{"type": "code_interpreter"}]
        }
    ]
)

print("Message created with file attachment")
```

### Extract Citations

```python
from openai import OpenAI

client = OpenAI()

thread_id = "thread_abc123"
message_id = "msg_xyz789"

message = client.beta.threads.messages.retrieve(
    thread_id=thread_id,
    message_id=message_id
)

# Extract citations
for content in message.content:
    if content.type == "text":
        print(f"Text: {content.text.value}")
        
        for annotation in content.text.annotations:
            if annotation.type == "file_citation":
                print(f"  Citation: {annotation.file_citation.quote}")
                print(f"  File: {annotation.file_citation.file_id}")
```

### Thread Metadata Management

```python
from openai import OpenAI

client = OpenAI()

# Create thread with metadata
thread = client.beta.threads.create(
    metadata={
        "user_id": "user_123",
        "session_type": "support",
        "priority": "high"
    }
)

# Update metadata
updated_thread = client.beta.threads.update(
    thread_id=thread.id,
    metadata={
        "user_id": "user_123",
        "session_type": "support",
        "priority": "high",
        "status": "resolved",
        "resolved_at": "2026-03-20T16:00:00Z"
    }
)

print(f"Thread metadata: {updated_thread.metadata}")
```

### Production Thread Manager

```python
from openai import OpenAI
from typing import List, Dict, Optional
from datetime import datetime

class ThreadManager:
    def __init__(self):
        self.client = OpenAI()
    
    def create_session(
        self,
        user_id: str,
        initial_message: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> str:
        """Create new conversation session"""
        meta = metadata or {}
        meta.update({
            "user_id": user_id,
            "created_at": datetime.now().isoformat()
        })
        
        messages = []
        if initial_message:
            messages.append({
                "role": "user",
                "content": initial_message
            })
        
        thread = self.client.beta.threads.create(
            messages=messages,
            metadata=meta
        )
        
        return thread.id
    
    def send_message(
        self,
        thread_id: str,
        assistant_id: str,
        content: str,
        attachments: Optional[List] = None
    ) -> Dict:
        """Send message and get response"""
        # Create message
        message = self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=content,
            attachments=attachments or []
        )
        
        # Run assistant
        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=thread_id,
            assistant_id=assistant_id
        )
        
        if run.status == "completed":
            # Get latest response
            messages = self.client.beta.threads.messages.list(
                thread_id=thread_id,
                limit=1
            )
            
            response = messages.data[0].content[0].text.value
            
            return {
                "response": response,
                "run_id": run.id,
                "message_id": messages.data[0].id
            }
        else:
            return {
                "error": f"Run failed: {run.status}",
                "run_id": run.id
            }
    
    def get_conversation_history(
        self,
        thread_id: str,
        limit: Optional[int] = None
    ) -> List[Dict]:
        """Get conversation history"""
        messages = self.client.beta.threads.messages.list(
            thread_id=thread_id,
            limit=limit or 100,
            order="asc"
        )
        
        history = []
        for msg in messages.data:
            history.append({
                "role": msg.role,
                "content": msg.content[0].text.value,
                "created_at": msg.created_at
            })
        
        return history
    
    def close_session(
        self,
        thread_id: str,
        resolution: Optional[str] = None
    ):
        """Close conversation session"""
        metadata = {
            "status": "closed",
            "closed_at": datetime.now().isoformat()
        }
        
        if resolution:
            metadata["resolution"] = resolution
        
        self.client.beta.threads.update(
            thread_id=thread_id,
            metadata=metadata
        )
    
    def delete_old_threads(self, user_id: str, days: int = 30):
        """Delete threads older than N days (requires custom tracking)"""
        # Note: OpenAI API doesn't provide thread listing by user
        # You'd need to track thread IDs in your database
        pass

# Usage
manager = ThreadManager()

# Create session
thread_id = manager.create_session(
    user_id="user_123",
    initial_message="I need help with billing",
    metadata={"channel": "web", "priority": "normal"}
)

# Multi-turn conversation
questions = [
    "What's my current balance?",
    "When is my next payment due?",
    "Can I change my payment method?"
]

for question in questions:
    result = manager.send_message(
        thread_id=thread_id,
        assistant_id="asst_billing",
        content=question
    )
    
    print(f"Q: {question}")
    print(f"A: {result['response']}\n")

# Get full history
history = manager.get_conversation_history(thread_id)
print(f"Total messages: {len(history)}")

# Close session
manager.close_session(thread_id, resolution="Billing question resolved")
```

## Error Responses

- **404 Not Found** - Thread or message not found
- **400 Bad Request** - Invalid parameters
- **429 Too Many Requests** - Rate limit exceeded

## Rate Limiting / Throttling

- **Thread operations**: Standard rate limits
- **Message creation**: RPM limits apply
- **Message listing**: Pagination recommended for large threads

## Differences from Other APIs

- **vs Conversations (Responses)**: Threads for Assistants, Conversations for Responses
- **vs Chat history**: Built-in vs manual tracking
- **vs Redis sessions**: Managed by OpenAI vs self-hosted

## Limitations and Known Issues

- **No thread listing**: Cannot list all threads [VERIFIED] (OAIAPI-SC-OAI-THRCRT)
- **Context window limits**: Old messages truncated [VERIFIED] (OAIAPI-SC-OAI-GASSIST)
- **No search**: Cannot search threads by content [COMMUNITY] (OAIAPI-SC-SO-THRSRCH)

## Gotchas and Quirks

- **Newest first**: Messages listed newest first by default [VERIFIED] (OAIAPI-SC-OAI-MSGLST)
- **No auto-cleanup**: Must manually delete old threads [VERIFIED] (OAIAPI-SC-OAI-THRCRT)
- **Metadata only updates**: Cannot edit message content [VERIFIED] (OAIAPI-SC-OAI-MSGMOD)

## Sources

- OAIAPI-SC-OAI-THRCRT - POST Create thread
- OAIAPI-SC-OAI-THRGET - GET Retrieve thread
- OAIAPI-SC-OAI-MSGCRT - POST Create message
- OAIAPI-SC-OAI-MSGLST - GET List messages
- OAIAPI-SC-OAI-GASSIST - Assistants guide

## Document History

**[2026-03-20 16:41]**
- Fixed: `client.threads` -> `client.beta.threads` per SDK v2.29.0 (all occurrences)

**[2026-03-20 16:15]**
- Initial documentation created
