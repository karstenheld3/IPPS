# Vector Stores API

**Doc ID**: OAIAPI-IN30
**Goal**: Document Vector Stores for RAG, file management, chunking, and embedding configuration
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references
- `_INFO_OAIAPI-IN28_FILES.md [OAIAPI-IN28]` for Files API context

## Summary

Vector Stores API manages document collections for RAG (Retrieval Augmented Generation). Create vector store (POST /v1/vector_stores), add files (POST /v1/vector_stores/{vs_id}/files), and use with file_search tool in Responses API. Vector stores automatically chunk documents, generate embeddings, and index for semantic search. Supports file batches for bulk file addition. Configure chunking strategy (auto, static), max chunk size, chunk overlap. Files processed asynchronously - poll status until ready. Each vector store has metadata, file count, usage stats. Use cases: knowledge bases, document Q&A, contextual retrieval. Files can belong to multiple vector stores. Supports file formats: PDF, DOCX, TXT, MD, HTML, etc. Expiration policies available (anchor, last_active_at). Vector stores persist until deleted. [VERIFIED] (OAIAPI-SC-OAI-VSCRT, OAIAPI-SC-OAI-GVECST)

## Key Facts

- **Purpose**: Document collections for RAG [VERIFIED] (OAIAPI-SC-OAI-GVECST)
- **Automatic**: Chunking and embedding handled automatically [VERIFIED] (OAIAPI-SC-OAI-VSCRT)
- **File formats**: PDF, DOCX, TXT, MD, HTML, CSV, etc. [VERIFIED] (OAIAPI-SC-OAI-GVECST)
- **Integration**: Use with file_search tool [VERIFIED] (OAIAPI-SC-OAI-GTOOLS)
- **Async processing**: Files processed in background [VERIFIED] (OAIAPI-SC-OAI-VSFILE)

## Use Cases

- **Knowledge bases**: Searchable document repositories
- **Document Q&A**: Answer questions from documents
- **RAG applications**: Context retrieval for responses
- **Customer support**: Search help docs, FAQs
- **Research**: Query academic papers, reports

## Quick Reference

```python
# Create vector store
POST /v1/vector_stores
{
  "name": "Product Documentation",
  "file_ids": ["file_abc", "file_def"]
}

# Add files
POST /v1/vector_stores/{vs_id}/files
{
  "file_id": "file_xyz"
}

# Use in Responses API
tools=[
  {
    "type": "file_search",
    "file_search": {
      "vector_store_ids": ["vs_abc123"]
    }
  }
]
```

## Vector Store Object

```json
{
  "id": "vs_abc123",
  "object": "vector_store",
  "name": "Product Documentation",
  "status": "completed",
  "usage_bytes": 150000000,
  "file_counts": {
    "total": 10,
    "completed": 10,
    "in_progress": 0,
    "failed": 0,
    "cancelled": 0
  },
  "created_at": 1234567890,
  "metadata": {},
  "chunking_strategy": {
    "type": "auto"
  },
  "expires_after": null
}
```

### Status Values

- **in_progress**: Files being processed
- **completed**: All files ready
- **expired**: Vector store expired

## Vector Store Operations

### Create Vector Store

```
POST /v1/vector_stores
```

**Request:**
```json
{
  "name": "Knowledge Base",
  "file_ids": ["file_1", "file_2"],
  "metadata": {
    "category": "support"
  },
  "chunking_strategy": {
    "type": "static",
    "static": {
      "max_chunk_size_tokens": 800,
      "chunk_overlap_tokens": 400
    }
  },
  "expires_after": {
    "anchor": "last_active_at",
    "days": 7
  }
}
```

### List Vector Stores

```
GET /v1/vector_stores
```

### Retrieve Vector Store

```
GET /v1/vector_stores/{vs_id}
```

### Update Vector Store

```
POST /v1/vector_stores/{vs_id}
```

Update name, metadata, or expiration.

### Delete Vector Store

```
DELETE /v1/vector_stores/{vs_id}
```

Permanently deletes vector store and all indexed data.

## File Management

### Add File

```
POST /v1/vector_stores/{vs_id}/files
```

**Request:**
```json
{
  "file_id": "file_abc123"
}
```

### List Files

```
GET /v1/vector_stores/{vs_id}/files
```

### Remove File

```
DELETE /v1/vector_stores/{vs_id}/files/{file_id}
```

### File Batches

Add multiple files at once:

```
POST /v1/vector_stores/{vs_id}/file_batches
```

**Request:**
```json
{
  "file_ids": ["file_1", "file_2", "file_3"]
}
```

## Chunking Strategies

### Auto (Default)

Automatic chunking with optimal settings:
```json
{
  "chunking_strategy": {
    "type": "auto"
  }
}
```

### Static

Custom chunk size and overlap:
```json
{
  "chunking_strategy": {
    "type": "static",
    "static": {
      "max_chunk_size_tokens": 800,
      "chunk_overlap_tokens": 400
    }
  }
}
```

**Parameters:**
- **max_chunk_size_tokens**: Max tokens per chunk (100-4096)
- **chunk_overlap_tokens**: Overlap between chunks (0-max_chunk_size/2)

## Expiration Policies

### Anchor: last_active_at

Expires after N days of inactivity:
```json
{
  "expires_after": {
    "anchor": "last_active_at",
    "days": 7
  }
}
```

### Anchor: created_at

Expires N days after creation:
```json
{
  "expires_after": {
    "anchor": "created_at",
    "days": 30
  }
}
```

## Using with file_search

### In Responses API

```python
response = client.responses.create(
    model="gpt-5.4",
    input=[
        {"role": "user", "content": "What does the documentation say about API keys?"}
    ],
    tools=[
        {
            "type": "file_search",
            "file_search": {
                "vector_store_ids": ["vs_abc123"],
                "max_num_results": 20
            }
        }
    ]
)
```

Model automatically searches vector store and uses results in response.

## SDK Examples (Python)

### Create Vector Store

```python
from openai import OpenAI

client = OpenAI()

# Upload files first
file_ids = []
for path in ["doc1.pdf", "doc2.pdf", "doc3.pdf"]:
    with open(path, "rb") as f:
        file = client.files.create(file=f, purpose="assistants")
        file_ids.append(file.id)

# Create vector store
vector_store = client.vector_stores.create(
    name="Product Documentation",
    file_ids=file_ids
)

print(f"Vector Store ID: {vector_store.id}")
print(f"Status: {vector_store.status}")
```

### Monitor File Processing

```python
from openai import OpenAI
import time

client = OpenAI()

vs_id = "vs_abc123"

while True:
    vs = client.vector_stores.retrieve(vs_id)
    
    counts = vs.file_counts
    print(f"Completed: {counts.completed}/{counts.total}")
    
    if vs.status == "completed":
        print("All files processed")
        break
    
    time.sleep(5)
```

### Add Files to Existing Store

```python
from openai import OpenAI

client = OpenAI()

# Upload new file
with open("new_doc.pdf", "rb") as f:
    file = client.files.create(file=f, purpose="assistants")

# Add to vector store
client.vector_stores.files.create(
    vector_store_id="vs_abc123",
    file_id=file.id
)

print("File added to vector store")
```

### Batch File Addition

```python
from openai import OpenAI

client = OpenAI()

# Upload files
file_ids = []
for i in range(10):
    with open(f"doc_{i}.pdf", "rb") as f:
        file = client.files.create(file=f, purpose="assistants")
        file_ids.append(file.id)

# Add batch
file_batch = client.vector_stores.file_batches.create(
    vector_store_id="vs_abc123",
    file_ids=file_ids
)

print(f"Batch ID: {file_batch.id}")
print(f"Status: {file_batch.status}")
```

### Custom Chunking

```python
from openai import OpenAI

client = OpenAI()

vector_store = client.vector_stores.create(
    name="Technical Docs",
    file_ids=["file_1", "file_2"],
    chunking_strategy={
        "type": "static",
        "static": {
            "max_chunk_size_tokens": 1000,
            "chunk_overlap_tokens": 200
        }
    }
)

print(f"Created with custom chunking: {vector_store.id}")
```

### With Expiration

```python
from openai import OpenAI

client = OpenAI()

vector_store = client.vector_stores.create(
    name="Temporary KB",
    file_ids=["file_abc"],
    expires_after={
        "anchor": "last_active_at",
        "days": 7
    }
)

print("Vector store expires after 7 days of inactivity")
```

### Use in RAG Application

```python
from openai import OpenAI

client = OpenAI()

def ask_docs(question: str, vs_id: str) -> str:
    """Ask question using vector store"""
    response = client.responses.create(
        model="gpt-5.4",
        input=[
            {"role": "user", "content": question}
        ],
        tools=[
            {
                "type": "file_search",
                "file_search": {
                    "vector_store_ids": [vs_id],
                    "max_num_results": 10
                }
            }
        ]
    )
    
    return response.output[0].content[0].text

# Usage
answer = ask_docs(
    "How do I reset my password?",
    vs_id="vs_abc123"
)
print(answer)
```

### Production Vector Store Manager

```python
from openai import OpenAI
from typing import List, Optional
import time

class VectorStoreManager:
    def __init__(self):
        self.client = OpenAI()
    
    def create_from_files(
        self,
        name: str,
        file_paths: List[str],
        chunking: Optional[dict] = None,
        wait_for_completion: bool = True
    ) -> dict:
        """Create vector store from file paths"""
        # Upload files
        file_ids = []
        for path in file_paths:
            with open(path, "rb") as f:
                file = self.client.files.create(
                    file=f,
                    purpose="assistants"
                )
                file_ids.append(file.id)
                print(f"Uploaded: {path}")
        
        # Create vector store
        params = {"name": name, "file_ids": file_ids}
        if chunking:
            params["chunking_strategy"] = chunking
        
        vs = self.client.vector_stores.create(**params)
        print(f"Created vector store: {vs.id}")
        
        if wait_for_completion:
            vs = self.wait_for_completion(vs.id)
        
        return {
            "id": vs.id,
            "name": vs.name,
            "status": vs.status,
            "file_count": vs.file_counts.total
        }
    
    def wait_for_completion(self, vs_id: str, timeout: int = 600):
        """Wait for all files to be processed"""
        start = time.time()
        
        while True:
            vs = self.client.vector_stores.retrieve(vs_id)
            
            if vs.status == "completed":
                return vs
            
            if time.time() - start > timeout:
                raise TimeoutError(f"Processing timeout: {vs_id}")
            
            counts = vs.file_counts
            print(f"Processing: {counts.completed}/{counts.total}")
            time.sleep(5)
    
    def add_files(self, vs_id: str, file_paths: List[str]):
        """Add files to existing vector store"""
        file_ids = []
        for path in file_paths:
            with open(path, "rb") as f:
                file = self.client.files.create(file=f, purpose="assistants")
                file_ids.append(file.id)
        
        # Add as batch
        file_batch = self.client.vector_stores.file_batches.create(
            vector_store_id=vs_id,
            file_ids=file_ids
        )
        
        return file_batch.id
    
    def query(
        self,
        vs_id: str,
        question: str,
        model: str = "gpt-5.4",
        max_results: int = 10
    ) -> str:
        """Query vector store"""
        response = self.client.responses.create(
            model=model,
            input=[{"role": "user", "content": question}],
            tools=[
                {
                    "type": "file_search",
                    "file_search": {
                        "vector_store_ids": [vs_id],
                        "max_num_results": max_results
                    }
                }
            ]
        )
        
        return response.output[0].content[0].text
    
    def list_all(self) -> List[dict]:
        """List all vector stores"""
        stores = self.client.vector_stores.list()
        
        return [
            {
                "id": vs.id,
                "name": vs.name,
                "status": vs.status,
                "files": vs.file_counts.total,
                "size_mb": vs.usage_bytes / (1024 * 1024)
            }
            for vs in stores.data
        ]

# Usage
manager = VectorStoreManager()

# Create from files
result = manager.create_from_files(
    name="Company Knowledge Base",
    file_paths=["handbook.pdf", "policies.pdf", "faq.pdf"],
    chunking={
        "type": "static",
        "static": {
            "max_chunk_size_tokens": 800,
            "chunk_overlap_tokens": 200
        }
    }
)

print(f"Vector store ready: {result['id']}")

# Query
answer = manager.query(
    vs_id=result["id"],
    question="What is the vacation policy?"
)
print(answer)

# List all stores
stores = manager.list_all()
for store in stores:
    print(f"{store['name']}: {store['files']} files, {store['size_mb']:.1f} MB")
```

## Error Responses

- **404 Not Found** - Vector store or file not found
- **400 Bad Request** - Invalid configuration or file format
- **413 Payload Too Large** - Too many files or total size too large

## Rate Limiting / Throttling

- **Creation limits**: Limited concurrent vector stores
- **File processing**: Background processing, no rate limits
- **Storage quotas**: Total storage limits per organization

## Differences from Other APIs

- **vs Pinecone**: OpenAI managed, Pinecone self-managed
- **vs Weaviate**: Simpler API, fewer configuration options
- **vs Chroma**: OpenAI integrated, Chroma standalone

## Limitations and Known Issues

- **File format support**: Not all formats supported [VERIFIED] (OAIAPI-SC-OAI-GVECST)
- **Processing time**: Large files take time to index [COMMUNITY] (OAIAPI-SC-SO-VSPROC)
- **No custom embeddings**: Must use OpenAI embeddings [VERIFIED] (OAIAPI-SC-OAI-VSCRT)

## Gotchas and Quirks

- **Async processing**: Files not immediately searchable [VERIFIED] (OAIAPI-SC-OAI-VSFILE)
- **Storage costs**: Large vector stores consume storage quota [COMMUNITY] (OAIAPI-SC-SO-VSCOST)
- **Deletion cascades**: Deleting vector store doesn't delete files [VERIFIED] (OAIAPI-SC-OAI-VSDEL)

## Sources

- OAIAPI-SC-OAI-VSCRT - POST Create vector store
- OAIAPI-SC-OAI-VSGET - GET Retrieve vector store
- OAIAPI-SC-OAI-VSFILE - Vector store files management
- OAIAPI-SC-OAI-GVECST - Vector stores guide

## Document History

**[2026-03-20 16:10]**
- Initial documentation created
