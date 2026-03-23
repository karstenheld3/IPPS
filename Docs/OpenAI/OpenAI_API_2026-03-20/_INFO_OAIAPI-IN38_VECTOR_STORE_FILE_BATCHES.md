# Vector Store File Batches

**Doc ID**: OAIAPI-IN38
**Goal**: Document bulk file operations for vector stores - create batches, track progress, list batch files, cancel batches
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references
- `_INFO_OAIAPI-IN37_VECTOR_STORE_FILES.md [OAIAPI-IN37]` for individual file operations
- `_INFO_OAIAPI-IN30_VECTOR_STORES.md [OAIAPI-IN30]` for vector store context

## Summary

Vector Store File Batches API enables bulk addition of files to a vector store in a single request. Create a batch (POST /v1/vector_stores/{vs_id}/file_batches) with up to 2000 files. Two input modes: `file_ids` (simple list with shared attributes/chunking) or `files` (per-file attributes and chunking overrides). Batches process asynchronously with status tracking: `in_progress`, `completed`, `cancelled`, `failed`. File counts track progress: `in_progress`, `completed`, `failed`, `cancelled`, `total`. Retrieve batch status (GET), list files in a batch (GET with pagination), or cancel an in-progress batch (POST cancel). Each file in the batch follows the same chunking and attribute rules as individual file additions. Batch operations are more efficient than adding files individually when onboarding large document sets. [VERIFIED] (OAIAPI-SC-OAI-VSFBT)

## Key Facts

- **Max batch size**: 2000 files per batch [VERIFIED] (OAIAPI-SC-OAI-VSFBT)
- **Two input modes**: `file_ids` (shared config) or `files` (per-file config), mutually exclusive [VERIFIED] (OAIAPI-SC-OAI-VSFBT)
- **Async processing**: Batch processes in background, poll for status [VERIFIED] (OAIAPI-SC-OAI-VSFBT)
- **Per-file overrides**: `files` mode allows different chunking_strategy and attributes per file [VERIFIED] (OAIAPI-SC-OAI-VSFBT)
- **Cancellable**: In-progress batches can be cancelled [VERIFIED] (OAIAPI-SC-OAI-VSFBT)
- **Beta header required**: `OpenAI-Beta: assistants=v2` [VERIFIED] (OAIAPI-SC-OAI-VSFBT)

## Use Cases

- **Bulk document onboarding**: Add hundreds of files to a knowledge base at once
- **Migration**: Move document sets from external systems to OpenAI vector stores
- **Mixed chunking**: Different document types need different chunk sizes in the same batch
- **Metadata tagging**: Assign category/department attributes to files during batch creation
- **Progress monitoring**: Track processing status across large file sets

## Quick Reference

```
POST /v1/vector_stores/{vector_store_id}/file_batches                        # Create batch
GET  /v1/vector_stores/{vector_store_id}/file_batches/{batch_id}             # Retrieve batch
GET  /v1/vector_stores/{vector_store_id}/file_batches/{batch_id}/files       # List batch files
POST /v1/vector_stores/{vector_store_id}/file_batches/{batch_id}/cancel      # Cancel batch

Headers:
  Authorization: Bearer $OPENAI_API_KEY
  Content-Type: application/json
  OpenAI-Beta: assistants=v2
```

## File Batch Object

```json
{
  "id": "vsfb_abc123",
  "object": "vector_store.file_batch",
  "created_at": 1699061776,
  "vector_store_id": "vs_abc123",
  "status": "in_progress",
  "file_counts": {
    "in_progress": 3,
    "completed": 7,
    "failed": 0,
    "cancelled": 0,
    "total": 10
  }
}
```

### Status Values

- **in_progress**: Files being processed
- **completed**: All files finished (some may have failed individually)
- **cancelled**: Batch was cancelled
- **failed**: Batch-level failure

## Operations

### Create File Batch

```
POST /v1/vector_stores/{vector_store_id}/file_batches
```

**Mode 1: Shared Configuration (file_ids)**

All files share the same chunking strategy and attributes:

```json
{
  "file_ids": ["file-abc123", "file-def456", "file-ghi789"],
  "attributes": {
    "department": "engineering"
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

**Mode 2: Per-File Configuration (files)**

Each file can have its own attributes and chunking:

```json
{
  "files": [
    {
      "file_id": "file-abc123",
      "attributes": {"category": "finance"}
    },
    {
      "file_id": "file-def456",
      "chunking_strategy": {
        "type": "static",
        "static": {
          "max_chunk_size_tokens": 1200,
          "chunk_overlap_tokens": 200
        }
      }
    },
    {
      "file_id": "file-ghi789",
      "attributes": {"category": "legal"},
      "chunking_strategy": {
        "type": "auto"
      }
    }
  ]
}
```

**Parameters:**
- **file_ids** (option A): List of file IDs with shared config. Max 2000
- **files** (option B): List of objects with file_id + optional per-file attributes/chunking_strategy. Max 2000
- **attributes** (optional, with file_ids): Shared attributes for all files
- **chunking_strategy** (optional, with file_ids): Shared chunking for all files

`file_ids` and `files` are mutually exclusive. When using `files` mode, global `attributes` and `chunking_strategy` are ignored.

### Retrieve File Batch

```
GET /v1/vector_stores/{vector_store_id}/file_batches/{batch_id}
```

Returns the file batch object with current status and file counts.

### List Files in Batch

```
GET /v1/vector_stores/{vector_store_id}/file_batches/{batch_id}/files
```

**Query Parameters:**
- **limit** (optional): 1-100, default 20
- **order** (optional): `asc` or `desc` by created_at
- **after** (optional): Cursor for forward pagination
- **before** (optional): Cursor for backward pagination
- **filter** (optional): Filter by status

Returns paginated list of vector store file objects belonging to this batch.

### Cancel File Batch

```
POST /v1/vector_stores/{vector_store_id}/file_batches/{batch_id}/cancel
```

Cancels an in-progress batch. Files already completed remain indexed. Files still in_progress are cancelled.

## SDK Examples (Python)

### Simple Batch with Shared Config

```python
from openai import OpenAI

client = OpenAI()

# Upload files
file_ids = []
for path in ["report_q1.pdf", "report_q2.pdf", "report_q3.pdf", "report_q4.pdf"]:
    with open(path, "rb") as f:
        file = client.files.create(file=f, purpose="assistants")
        file_ids.append(file.id)

# Create batch
batch = client.vector_stores.file_batches.create(
    vector_store_id="vs_abc123",
    file_ids=file_ids,
    attributes={"type": "quarterly_report"},
    chunking_strategy={
        "type": "static",
        "static": {
            "max_chunk_size_tokens": 1000,
            "chunk_overlap_tokens": 250
        }
    }
)

print(f"Batch ID: {batch.id}")
print(f"Status: {batch.status}")
print(f"Files: {batch.file_counts.total}")
```

### Per-File Config Batch

```python
from openai import OpenAI

client = OpenAI()

batch = client.vector_stores.file_batches.create(
    vector_store_id="vs_abc123",
    files=[
        {
            "file_id": "file-finance001",
            "attributes": {"category": "finance", "confidential": "true"}
        },
        {
            "file_id": "file-legal002",
            "attributes": {"category": "legal"},
            "chunking_strategy": {
                "type": "static",
                "static": {
                    "max_chunk_size_tokens": 2000,
                    "chunk_overlap_tokens": 500
                }
            }
        },
        {
            "file_id": "file-hr003",
            "attributes": {"category": "hr"}
        }
    ]
)

print(f"Batch: {batch.id}, Status: {batch.status}")
```

### Monitor Batch Progress - Production Ready

```python
from openai import OpenAI
import time

client = OpenAI()

def wait_for_batch(vs_id: str, batch_id: str, timeout: int = 600) -> dict:
    """Wait for file batch to complete with progress reporting"""
    start = time.time()
    
    while True:
        batch = client.vector_stores.file_batches.retrieve(
            vector_store_id=vs_id,
            batch_id=batch_id
        )
        
        counts = batch.file_counts
        elapsed = time.time() - start
        
        print(
            f"[{elapsed:.0f}s] Status: {batch.status} | "
            f"Completed: {counts.completed}/{counts.total} | "
            f"Failed: {counts.failed} | In progress: {counts.in_progress}"
        )
        
        if batch.status in ("completed", "failed", "cancelled"):
            return {
                "status": batch.status,
                "completed": counts.completed,
                "failed": counts.failed,
                "cancelled": counts.cancelled,
                "total": counts.total,
                "elapsed_seconds": elapsed
            }
        
        if elapsed > timeout:
            # Cancel on timeout
            client.vector_stores.file_batches.cancel(
                vector_store_id=vs_id,
                batch_id=batch_id
            )
            raise TimeoutError(f"Batch {batch_id} timed out after {timeout}s")
        
        time.sleep(5)

try:
    result = wait_for_batch("vs_abc123", "vsfb_xyz789", timeout=300)
    
    if result["failed"] > 0:
        # List failed files for debugging
        failed_files = client.vector_stores.file_batches.list_files(
            vector_store_id="vs_abc123",
            batch_id="vsfb_xyz789",
            filter="failed"
        )
        for f in failed_files.data:
            print(f"FAILED: {f.id} - {f.last_error.code}: {f.last_error.message}")
    else:
        print(f"All {result['completed']} files processed in {result['elapsed_seconds']:.0f}s")

except TimeoutError as e:
    print(f"Timeout: {e}")
except Exception as e:
    print(f"Error: {e}")
```

### Cancel In-Progress Batch

```python
from openai import OpenAI

client = OpenAI()

try:
    batch = client.vector_stores.file_batches.cancel(
        vector_store_id="vs_abc123",
        batch_id="vsfb_xyz789"
    )
    print(f"Cancelled. Completed: {batch.file_counts.completed}, Cancelled: {batch.file_counts.cancelled}")
except Exception as e:
    print(f"Cancel error: {e}")
```

## Error Responses

- **400 Bad Request** - Invalid parameters, both file_ids and files provided, batch exceeds 2000 files
- **404 Not Found** - Vector store or batch not found
- **429 Too Many Requests** - Rate limit exceeded

## Rate Limiting / Throttling

- **Batch creation**: Standard API rate limits
- **File processing**: Background async, no separate rate limit per file
- **Max batch size**: 2000 files per batch request [VERIFIED] (OAIAPI-SC-OAI-VSFBT)

## Differences from Other APIs

- **vs Anthropic**: No vector store or batch file indexing capability
- **vs Gemini**: Gemini File Search Stores support batch operations but different API
- **vs Grok**: Grok Collections API supports adding documents but no explicit batch endpoint
- **vs external (Pinecone, Weaviate)**: External DBs require manual batch upsert of pre-computed vectors; OpenAI handles chunking + embedding automatically

## Limitations and Known Issues

- **Max 2000 files per batch**: Split larger sets into multiple batches [VERIFIED] (OAIAPI-SC-OAI-VSFBT)
- **No partial retry**: Cannot retry only failed files within a batch; must re-add them individually [ASSUMED]
- **Mutual exclusivity**: Cannot mix file_ids and files modes in same request [VERIFIED] (OAIAPI-SC-OAI-VSFBT)

## Gotchas and Quirks

- **Cancel preserves completed**: Cancelling a batch does not remove files already processed [VERIFIED] (OAIAPI-SC-OAI-VSFBT)
- **file_counts.total may lag**: Total count may not reflect all files immediately after creation [ASSUMED]
- **Per-file mode ignores globals**: When using `files` array, top-level `attributes` and `chunking_strategy` are ignored [VERIFIED] (OAIAPI-SC-OAI-VSFBT)
- **Beta header**: Requires `OpenAI-Beta: assistants=v2` for REST calls [VERIFIED] (OAIAPI-SC-OAI-VSFBT)

## Sources

- OAIAPI-SC-OAI-VSFBT - Vector Store File Batches API (create, retrieve, list files, cancel)
- OAIAPI-SC-OAI-VSFIL - Vector Store Files API (individual file operations)
- OAIAPI-SC-OAI-VSAPI - Vector Stores API (parent resource)

## Document History

**[2026-03-20 17:42]**
- Initial documentation created from API reference research
