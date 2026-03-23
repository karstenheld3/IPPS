# Vector Store Files

**Doc ID**: OAIAPI-IN37
**Goal**: Document vector store file management - create, retrieve, update, delete, list files within a vector store
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references
- `_INFO_OAIAPI-IN30_VECTOR_STORES.md [OAIAPI-IN30]` for vector store context

## Summary

Vector Store Files API manages individual files within a vector store. Add files (POST /v1/vector_stores/{vs_id}/files) to index them for semantic search via the file_search tool. Each file is chunked, embedded, and indexed asynchronously - poll status until `completed`. Retrieve file details including chunking strategy, status, usage bytes, and error information. Files support metadata (up to 16 key-value pairs) and custom attributes for filtering during search. Chunking strategy can be `auto` (default: 800 token chunks, 400 token overlap) or `static` (custom sizes, 100-4096 tokens per chunk, overlap up to half of max chunk size). File status values: `in_progress`, `completed`, `failed`, `cancelled`. Error codes: `server_error`, `unsupported_file`, `invalid_file`. List files with pagination (cursor-based, limit 1-100, default 20), filter by status, sort by created_at. Deleting a file from a vector store removes the indexed data but does not delete the underlying file object. [VERIFIED] (OAIAPI-SC-OAI-VSFIL)

## Key Facts

- **Async processing**: Files indexed in background, poll until `completed` [VERIFIED] (OAIAPI-SC-OAI-VSFIL)
- **Chunking strategies**: `auto` (800/400 defaults) or `static` (custom 100-4096 tokens) [VERIFIED] (OAIAPI-SC-OAI-VSFIL)
- **Metadata**: Up to 16 key-value pairs per file (keys max 64 chars, values max 512 chars) [VERIFIED] (OAIAPI-SC-OAI-VSFIL)
- **Attributes**: Custom key-value pairs for search filtering [VERIFIED] (OAIAPI-SC-OAI-VSFIL)
- **Pagination**: Cursor-based with `after`/`before`, limit 1-100 [VERIFIED] (OAIAPI-SC-OAI-VSFIL)
- **Error types**: `server_error`, `unsupported_file`, `invalid_file` [VERIFIED] (OAIAPI-SC-OAI-VSFIL)

## Use Cases

- **Add documents to knowledge base**: Index new files for RAG retrieval
- **Monitor processing status**: Track file indexing progress
- **Custom chunking per file**: Different chunk sizes for different document types
- **File metadata management**: Tag files with attributes for filtered search
- **Audit file status**: List and filter files by processing status

## Quick Reference

```
POST   /v1/vector_stores/{vector_store_id}/files          # Create (add file)
GET    /v1/vector_stores/{vector_store_id}/files           # List files
GET    /v1/vector_stores/{vector_store_id}/files/{file_id} # Retrieve file
POST   /v1/vector_stores/{vector_store_id}/files/{file_id} # Update file
DELETE /v1/vector_stores/{vector_store_id}/files/{file_id} # Delete file

Headers:
  Authorization: Bearer $OPENAI_API_KEY
  Content-Type: application/json
  OpenAI-Beta: assistants=v2
```

## Vector Store File Object

```json
{
  "id": "file-abc123",
  "object": "vector_store.file",
  "created_at": 1699061776,
  "vector_store_id": "vs_abc123",
  "status": "completed",
  "usage_bytes": 12345,
  "last_error": null,
  "attributes": {
    "category": "support"
  },
  "chunking_strategy": {
    "type": "static",
    "static": {
      "max_chunk_size_tokens": 800,
      "chunk_overlap_tokens": 400
    }
  }
}
```

### Status Values

- **in_progress**: File being chunked and indexed
- **completed**: File ready for search
- **failed**: Processing error (check `last_error`)
- **cancelled**: Processing was cancelled

### Error Codes (last_error.code)

- **server_error**: Internal processing failure, retry
- **unsupported_file**: File format not supported
- **invalid_file**: File corrupted or unreadable

## Operations

### Create (Add File to Vector Store)

```
POST /v1/vector_stores/{vector_store_id}/files
```

**Request:**
```json
{
  "file_id": "file-abc123",
  "attributes": {
    "category": "finance",
    "department": "accounting"
  },
  "chunking_strategy": {
    "type": "static",
    "static": {
      "max_chunk_size_tokens": 1000,
      "chunk_overlap_tokens": 200
    }
  }
}
```

**Parameters:**
- **file_id** (required): ID of uploaded file (from Files API)
- **attributes** (optional): Key-value pairs for search filtering
- **chunking_strategy** (optional): `auto` or `static` with custom settings

### List Files

```
GET /v1/vector_stores/{vector_store_id}/files
```

**Query Parameters:**
- **limit** (optional): 1-100, default 20
- **order** (optional): `asc` or `desc` by created_at
- **after** (optional): Cursor for forward pagination
- **before** (optional): Cursor for backward pagination
- **filter** (optional): Filter by status (`in_progress`, `completed`, `failed`, `cancelled`)

**Response:**
```json
{
  "object": "list",
  "data": [
    {
      "id": "file-abc123",
      "object": "vector_store.file",
      "created_at": 1699061776,
      "vector_store_id": "vs_abc123"
    }
  ],
  "first_id": "file-abc123",
  "last_id": "file-abc456",
  "has_more": false
}
```

### Retrieve File

```
GET /v1/vector_stores/{vector_store_id}/files/{file_id}
```

Returns the full vector store file object with status, chunking strategy, usage, and errors.

### Update File

```
POST /v1/vector_stores/{vector_store_id}/files/{file_id}
```

Update metadata and attributes on an existing vector store file.

### Delete File

```
DELETE /v1/vector_stores/{vector_store_id}/files/{file_id}
```

Removes the file from the vector store and deletes indexed chunks. Does NOT delete the underlying file object from the Files API.

## Chunking Strategies

### Auto (Default)

```json
{
  "chunking_strategy": {
    "type": "auto"
  }
}
```

Uses `max_chunk_size_tokens: 800` and `chunk_overlap_tokens: 400`.

### Static (Custom)

```json
{
  "chunking_strategy": {
    "type": "static",
    "static": {
      "max_chunk_size_tokens": 1200,
      "chunk_overlap_tokens": 300
    }
  }
}
```

**Constraints:**
- `max_chunk_size_tokens`: 100-4096
- `chunk_overlap_tokens`: 0 to max_chunk_size_tokens/2

### Other (Legacy)

Returned when file was indexed before `chunking_strategy` was introduced. Type is `other` - strategy details unknown.

## SDK Examples (Python)

### Add File to Vector Store

```python
from openai import OpenAI

client = OpenAI()

# Upload file first
with open("product_manual.pdf", "rb") as f:
    file = client.files.create(file=f, purpose="assistants")

# Add to vector store with custom attributes
vs_file = client.vector_stores.files.create(
    vector_store_id="vs_abc123",
    file_id=file.id,
    attributes={"category": "product", "version": "2.0"}
)

print(f"File ID: {vs_file.id}")
print(f"Status: {vs_file.status}")
```

### Poll File Until Ready

```python
from openai import OpenAI
import time

client = OpenAI()

vs_id = "vs_abc123"
file_id = "file-xyz789"

while True:
    vs_file = client.vector_stores.files.retrieve(
        vector_store_id=vs_id,
        file_id=file_id
    )
    
    if vs_file.status == "completed":
        print(f"File ready. Usage: {vs_file.usage_bytes} bytes")
        break
    elif vs_file.status == "failed":
        print(f"Error: {vs_file.last_error.code} - {vs_file.last_error.message}")
        break
    
    print(f"Status: {vs_file.status}")
    time.sleep(2)
```

### List and Filter Files - Production Ready

```python
from openai import OpenAI

client = OpenAI()

def list_all_vs_files(vs_id: str, status_filter: str = None):
    """List all files in a vector store with optional status filter"""
    all_files = []
    after = None
    
    while True:
        params = {
            "vector_store_id": vs_id,
            "limit": 100,
            "order": "desc"
        }
        if after:
            params["after"] = after
        if status_filter:
            params["filter"] = status_filter
        
        response = client.vector_stores.files.list(**params)
        all_files.extend(response.data)
        
        if not response.has_more:
            break
        after = response.last_id
    
    return all_files

try:
    # List completed files
    completed = list_all_vs_files("vs_abc123", status_filter="completed")
    print(f"Completed files: {len(completed)}")
    
    # List failed files for debugging
    failed = list_all_vs_files("vs_abc123", status_filter="failed")
    for f in failed:
        print(f"Failed: {f.id} - {f.last_error.message}")

except Exception as e:
    print(f"Error listing files: {e}")
```

### Remove File from Vector Store

```python
from openai import OpenAI

client = OpenAI()

try:
    result = client.vector_stores.files.delete(
        vector_store_id="vs_abc123",
        file_id="file-xyz789"
    )
    print(f"Deleted: {result.deleted}")
except Exception as e:
    print(f"Error: {e}")
```

## Error Responses

- **400 Bad Request** - Invalid file_id, unsupported chunking parameters
- **404 Not Found** - Vector store or file not found
- **409 Conflict** - File already exists in vector store
- **429 Too Many Requests** - Rate limit exceeded

## Rate Limiting / Throttling

- **File additions**: Subject to standard API rate limits
- **Processing**: Async background processing, no separate rate limit
- **Polling**: Standard API rate limits apply to retrieve/list calls

## Differences from Other APIs

- **vs Anthropic**: Anthropic has no vector store or file indexing API
- **vs Gemini**: Gemini has File Search Stores (closest equivalent) but different API surface
- **vs Grok**: Grok has Collections API with `collections_search` tool - similar concept, different implementation
- **vs Pinecone/external**: OpenAI handles chunking and embedding automatically; external vector DBs require manual pipeline

## Limitations and Known Issues

- **Processing time**: Large files (100+ pages) can take minutes to index [VERIFIED] (OAIAPI-SC-OAI-VSFIL)
- **No custom embeddings**: Must use OpenAI's embedding model, cannot bring your own [VERIFIED] (OAIAPI-SC-OAI-VSFIL)
- **Chunk size limits**: max_chunk_size_tokens capped at 4096 [VERIFIED] (OAIAPI-SC-OAI-VSFIL)
- **Format support**: Not all file formats supported; unsupported files return `unsupported_file` error [VERIFIED] (OAIAPI-SC-OAI-VSFIL)

## Gotchas and Quirks

- **Delete scope**: Deleting a VS file removes indexed data but NOT the underlying file object [VERIFIED] (OAIAPI-SC-OAI-VSFIL)
- **Legacy chunking**: Files indexed before chunking_strategy feature show `type: "other"` [VERIFIED] (OAIAPI-SC-OAI-VSFIL)
- **OpenAI-Beta header**: Requires `OpenAI-Beta: assistants=v2` header for REST calls [VERIFIED] (OAIAPI-SC-OAI-VSFIL)
- **Overlap constraint**: chunk_overlap_tokens must not exceed half of max_chunk_size_tokens [VERIFIED] (OAIAPI-SC-OAI-VSFIL)

## Sources

- OAIAPI-SC-OAI-VSFIL - Vector Store Files API (create, retrieve, update, delete, list)
- OAIAPI-SC-OAI-VSAPI - Vector Stores API (parent resource)

## Document History

**[2026-03-20 17:40]**
- Initial documentation created from API reference research
