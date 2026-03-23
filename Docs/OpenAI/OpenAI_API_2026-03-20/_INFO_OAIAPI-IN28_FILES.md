# Files API

**Doc ID**: OAIAPI-IN28
**Goal**: Document Files API for upload, retrieval, deletion, and purpose management
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references

## Summary

Files API manages file uploads for fine-tuning, batch processing, and vector stores. Upload files via POST /v1/files with purpose parameter (fine-tune, batch, assistants, vision), retrieve file metadata with GET /v1/files/{file_id}, download content with GET /v1/files/{file_id}/content, delete with DELETE /v1/files/{file_id}, and list all files with GET /v1/files. Maximum file size varies by purpose: 512MB for assistants, 100MB for fine-tune. Supported formats depend on purpose - JSONL for fine-tune/batch, various formats for assistants. Files persist until manually deleted. File IDs used across API (fine-tuning jobs, batch inputs, vector stores). Each file has purpose, filename, bytes, created_at metadata. Purpose cannot be changed after upload - must delete and re-upload. Organization-scoped - visible only to organization members. [VERIFIED] (OAIAPI-SC-OAI-FILCRT, OAIAPI-SC-OAI-FILGET, OAIAPI-SC-OAI-GFILES)

## Key Facts

- **Endpoint**: POST /v1/files [VERIFIED] (OAIAPI-SC-OAI-FILCRT)
- **Max size**: 512MB (assistants), 100MB (fine-tune) [VERIFIED] (OAIAPI-SC-OAI-GFILES)
- **Purposes**: fine-tune, batch, assistants, vision [VERIFIED] (OAIAPI-SC-OAI-FILCRT)
- **Persistence**: Files persist until deleted [VERIFIED] (OAIAPI-SC-OAI-GFILES)
- **Scope**: Organization-level [VERIFIED] (OAIAPI-SC-OAI-GFILES)

## Use Cases

- **Fine-tuning**: Upload training data
- **Batch processing**: Upload batch request files
- **Vector stores**: Upload documents for RAG
- **Vision**: Upload images for analysis
- **File storage**: Store files for API use

## Quick Reference

```python
# Upload
POST /v1/files
file: data.jsonl
purpose: fine-tune

# List
GET /v1/files

# Retrieve metadata
GET /v1/files/{file_id}

# Download content
GET /v1/files/{file_id}/content

# Delete
DELETE /v1/files/{file_id}
```

## File Purposes

### fine-tune
- **Format**: JSONL
- **Size limit**: 100MB
- **Use**: Fine-tuning training/validation data
- **Content**: Messages arrays for training

### batch
- **Format**: JSONL
- **Size limit**: 100MB
- **Use**: Batch API requests
- **Content**: API request objects

### assistants
- **Format**: Various (PDF, DOCX, TXT, etc.)
- **Size limit**: 512MB
- **Use**: Assistant file search, code interpreter
- **Content**: Documents, data files

### vision
- **Format**: Images (JPG, PNG, WEBP, GIF)
- **Size limit**: 20MB per image
- **Use**: Image analysis
- **Content**: Images for GPT-4 Vision

## File Object

```json
{
  "id": "file_abc123",
  "object": "file",
  "bytes": 120000,
  "created_at": 1234567890,
  "filename": "training_data.jsonl",
  "purpose": "fine-tune",
  "status": "processed",
  "status_details": null
}
```

### Fields

- **id**: Unique file identifier
- **object**: Always "file"
- **bytes**: File size in bytes
- **created_at**: Unix timestamp
- **filename**: Original filename
- **purpose**: File purpose
- **status**: "uploaded", "processed", "error"
- **status_details**: Error details if status is "error"

## File Operations

### Upload File

```
POST /v1/files
```

**Request (multipart/form-data):**
- **file**: File content (binary)
- **purpose**: File purpose

**Response:** File object

### List Files

```
GET /v1/files
```

**Query parameters:**
- **purpose**: Filter by purpose (optional)
- **limit**: Number of files to return
- **order**: "asc" or "desc"
- **after**: Cursor for pagination

### Retrieve File

```
GET /v1/files/{file_id}
```

Returns file metadata (not content).

### Download Content

```
GET /v1/files/{file_id}/content
```

Returns file content as binary stream.

### Delete File

```
DELETE /v1/files/{file_id}
```

Permanently deletes file.

## Supported Formats by Purpose

### Fine-tune / Batch
- JSONL only

### Assistants
- **Documents**: PDF, DOCX, DOC, HTML, TXT, MD
- **Spreadsheets**: XLSX, XLS, CSV
- **Presentations**: PPTX, PPT
- **Code**: PY, JS, TS, JAVA, C, CPP, etc.
- **Data**: JSON, XML, YAML

### Vision
- **Images**: JPG, JPEG, PNG, WEBP, GIF (non-animated)

## SDK Examples (Python)

### Upload File

```python
from openai import OpenAI

client = OpenAI()

# Upload training data
with open("training_data.jsonl", "rb") as f:
    file = client.files.create(
        file=f,
        purpose="fine-tune"
    )

print(f"File ID: {file.id}")
print(f"Filename: {file.filename}")
print(f"Size: {file.bytes} bytes")
```

### List All Files

```python
from openai import OpenAI

client = OpenAI()

files = client.files.list()

for file in files.data:
    print(f"{file.id}: {file.filename} ({file.purpose})")
```

### Filter by Purpose

```python
from openai import OpenAI

client = OpenAI()

# Get only fine-tune files
fine_tune_files = client.files.list(purpose="fine-tune")

for file in fine_tune_files.data:
    print(f"{file.filename}: {file.bytes} bytes")
```

### Retrieve File Metadata

```python
from openai import OpenAI

client = OpenAI()

file = client.files.retrieve("file_abc123")

print(f"Filename: {file.filename}")
print(f"Purpose: {file.purpose}")
print(f"Status: {file.status}")
print(f"Created: {file.created_at}")
```

### Download File Content

```python
from openai import OpenAI

client = OpenAI()

# Download content
content = client.files.content("file_abc123")

# Save to file
with open("downloaded_file.jsonl", "wb") as f:
    f.write(content.content)

print("File downloaded")
```

### Delete File

```python
from openai import OpenAI

client = OpenAI()

client.files.delete("file_abc123")
print("File deleted")
```

### Upload Multiple Files

```python
from openai import OpenAI

client = OpenAI()

file_paths = [
    "document1.pdf",
    "document2.pdf",
    "document3.pdf"
]

file_ids = []
for path in file_paths:
    with open(path, "rb") as f:
        file = client.files.create(
            file=f,
            purpose="assistants"
        )
        file_ids.append(file.id)
        print(f"Uploaded: {path} -> {file.id}")

print(f"\nTotal uploaded: {len(file_ids)}")
```

### Check Upload Status

```python
from openai import OpenAI
import time

client = OpenAI()

# Upload file
with open("large_file.pdf", "rb") as f:
    file = client.files.create(
        file=f,
        purpose="assistants"
    )

print(f"Uploaded: {file.id}")

# Wait for processing
while file.status == "uploaded":
    time.sleep(1)
    file = client.files.retrieve(file.id)
    print(f"Status: {file.status}")

if file.status == "processed":
    print("File ready to use")
elif file.status == "error":
    print(f"Error: {file.status_details}")
```

### Cleanup Old Files

```python
from openai import OpenAI
from datetime import datetime, timedelta

client = OpenAI()

# Delete files older than 30 days
cutoff_time = (datetime.now() - timedelta(days=30)).timestamp()

files = client.files.list()

deleted_count = 0
for file in files.data:
    if file.created_at < cutoff_time:
        client.files.delete(file.id)
        print(f"Deleted: {file.filename}")
        deleted_count += 1

print(f"\nTotal deleted: {deleted_count}")
```

### Production File Manager

```python
from openai import OpenAI
from typing import List, Optional
import time

class FileManager:
    def __init__(self):
        self.client = OpenAI()
    
    def upload(
        self,
        file_path: str,
        purpose: str,
        wait_for_processing: bool = True
    ) -> dict:
        """Upload file and optionally wait for processing"""
        with open(file_path, "rb") as f:
            file = self.client.files.create(
                file=f,
                purpose=purpose
            )
        
        if wait_for_processing:
            file = self.wait_for_processing(file.id)
        
        return {
            "id": file.id,
            "filename": file.filename,
            "bytes": file.bytes,
            "status": file.status
        }
    
    def wait_for_processing(self, file_id: str, timeout: int = 60):
        """Wait for file to be processed"""
        start = time.time()
        
        while True:
            file = self.client.files.retrieve(file_id)
            
            if file.status in ["processed", "error"]:
                return file
            
            if time.time() - start > timeout:
                raise TimeoutError(f"File processing timeout: {file_id}")
            
            time.sleep(1)
    
    def download(self, file_id: str, output_path: str):
        """Download file content"""
        content = self.client.files.content(file_id)
        
        with open(output_path, "wb") as f:
            f.write(content.content)
        
        return output_path
    
    def list_by_purpose(self, purpose: str) -> List[dict]:
        """List files by purpose"""
        files = self.client.files.list(purpose=purpose)
        
        return [
            {
                "id": f.id,
                "filename": f.filename,
                "bytes": f.bytes,
                "created_at": f.created_at
            }
            for f in files.data
        ]
    
    def delete_old_files(self, days: int = 30) -> int:
        """Delete files older than specified days"""
        from datetime import datetime, timedelta
        
        cutoff = (datetime.now() - timedelta(days=days)).timestamp()
        files = self.client.files.list()
        
        deleted = 0
        for file in files.data:
            if file.created_at < cutoff:
                self.client.files.delete(file.id)
                deleted += 1
        
        return deleted
    
    def get_total_storage(self) -> dict:
        """Get total storage usage by purpose"""
        files = self.client.files.list()
        
        storage = {}
        for file in files.data:
            purpose = file.purpose
            if purpose not in storage:
                storage[purpose] = {"count": 0, "bytes": 0}
            storage[purpose]["count"] += 1
            storage[purpose]["bytes"] += file.bytes
        
        return storage

# Usage
manager = FileManager()

# Upload and wait
result = manager.upload(
    "training_data.jsonl",
    purpose="fine-tune",
    wait_for_processing=True
)
print(f"Uploaded: {result['id']}")

# List files
fine_tune_files = manager.list_by_purpose("fine-tune")
print(f"Fine-tune files: {len(fine_tune_files)}")

# Storage usage
storage = manager.get_total_storage()
for purpose, info in storage.items():
    mb = info["bytes"] / (1024 * 1024)
    print(f"{purpose}: {info['count']} files, {mb:.2f} MB")

# Cleanup
deleted = manager.delete_old_files(days=30)
print(f"Deleted {deleted} old files")
```

## Error Responses

- **400 Bad Request** - Invalid file format or purpose
- **413 Payload Too Large** - File exceeds size limit
- **404 Not Found** - File not found
- **429 Too Many Requests** - Rate limit exceeded

## Rate Limiting / Throttling

- **Upload limits**: Limited concurrent uploads
- **Storage quotas**: Total storage limits per organization
- **File count**: Maximum files per organization

## Differences from Other APIs

- **vs Cloud storage**: API-integrated, not general-purpose storage
- **vs S3**: OpenAI-specific purposes, not generic object storage
- **vs Google Drive**: Temporary vs permanent storage focus

## Limitations and Known Issues

- **No versioning**: Cannot update files, must delete and re-upload [VERIFIED] (OAIAPI-SC-OAI-GFILES)
- **No folders**: Flat file structure, no directories [VERIFIED] (OAIAPI-SC-OAI-GFILES)
- **Purpose immutable**: Cannot change purpose after upload [VERIFIED] (OAIAPI-SC-OAI-FILCRT)

## Gotchas and Quirks

- **Files don't auto-delete**: Must manually clean up [VERIFIED] (OAIAPI-SC-OAI-GFILES)
- **Purpose matters**: Wrong purpose prevents usage [VERIFIED] (OAIAPI-SC-OAI-FILCRT)
- **Processing delay**: Files may take time to process [COMMUNITY] (OAIAPI-SC-SO-FILPROC)

## Sources

- OAIAPI-SC-OAI-FILCRT - POST Upload file
- OAIAPI-SC-OAI-FILGET - GET Retrieve file
- OAIAPI-SC-OAI-FILCNT - GET Download file content
- OAIAPI-SC-OAI-FILDEL - DELETE Delete file
- OAIAPI-SC-OAI-GFILES - Files guide

## Document History

**[2026-03-20 16:05]**
- Initial documentation created
