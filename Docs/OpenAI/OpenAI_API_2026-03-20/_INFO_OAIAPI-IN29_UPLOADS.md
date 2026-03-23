# Uploads API

**Doc ID**: OAIAPI-IN29
**Goal**: Document multipart upload API for large files with chunking and resumability
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references
- `_INFO_OAIAPI-IN28_FILES.md [OAIAPI-IN28]` for Files API context

## Summary

Uploads API enables multipart upload for large files exceeding simple upload limits. Create upload (POST /v1/uploads), add parts (POST /v1/uploads/{upload_id}/parts), and complete (POST /v1/uploads/{upload_id}/complete) to finalize file. Supports resumable uploads - if connection drops, resume by adding remaining parts. Minimum part size 5MB, maximum 512MB total. Each part uploaded separately with part number, then assembled on completion. Use for large fine-tuning datasets, batch files, assistant documents. Benefits: resume interrupted uploads, parallel part uploads, handle network issues. Upload expires after 1 hour if not completed. On completion, returns file ID usable in Files API. Supports same purposes as Files API. Parts can be uploaded in any order. Cancel with POST /v1/uploads/{upload_id}/cancel. [VERIFIED] (OAIAPI-SC-OAI-UPLCRT, OAIAPI-SC-OAI-GUPLOAD)

## Key Facts

- **Endpoint**: POST /v1/uploads [VERIFIED] (OAIAPI-SC-OAI-UPLCRT)
- **Min part size**: 5MB [VERIFIED] (OAIAPI-SC-OAI-GUPLOAD)
- **Max total size**: 512MB [VERIFIED] (OAIAPI-SC-OAI-GUPLOAD)
- **Resumable**: Can resume interrupted uploads [VERIFIED] (OAIAPI-SC-OAI-GUPLOAD)
- **Expiration**: 1 hour if not completed [VERIFIED] (OAIAPI-SC-OAI-UPLCRT)

## Use Cases

- **Large fine-tuning files**: Upload >100MB training data
- **Unreliable networks**: Resume failed uploads
- **Parallel uploads**: Upload parts concurrently
- **Large batch files**: Handle big batch request files
- **Assistant documents**: Upload large PDFs, datasets

## Quick Reference

```python
# Create upload
POST /v1/uploads
{
  "purpose": "fine-tune",
  "filename": "large_dataset.jsonl",
  "bytes": 150000000,
  "mime_type": "application/jsonl"
}

# Add part
POST /v1/uploads/{upload_id}/parts
data: <binary chunk>

# Complete
POST /v1/uploads/{upload_id}/complete
{
  "part_ids": ["part_1", "part_2", ...]
}
```

## Upload Workflow

### 1. Create Upload

```
POST /v1/uploads
```

**Request:**
```json
{
  "purpose": "fine-tune",
  "filename": "training_data.jsonl",
  "bytes": 150000000,
  "mime_type": "application/jsonl"
}
```

**Response:**
```json
{
  "id": "upload_abc123",
  "object": "upload",
  "bytes": 150000000,
  "created_at": 1234567890,
  "filename": "training_data.jsonl",
  "purpose": "fine-tune",
  "status": "pending",
  "expires_at": 1234571490
}
```

### 2. Upload Parts

```
POST /v1/uploads/{upload_id}/parts
```

**Request (binary):**
- Upload part as binary data
- Minimum 5MB per part (except last part)

**Response:**
```json
{
  "id": "part_xyz789",
  "object": "upload.part",
  "upload_id": "upload_abc123",
  "created_at": 1234567890
}
```

### 3. Complete Upload

```
POST /v1/uploads/{upload_id}/complete
```

**Request:**
```json
{
  "part_ids": ["part_1", "part_2", "part_3"]
}
```

**Response:**
```json
{
  "id": "upload_abc123",
  "object": "upload",
  "status": "completed",
  "file": {
    "id": "file_def456",
    "object": "file",
    "purpose": "fine-tune"
  }
}
```

### 4. Cancel Upload (Optional)

```
POST /v1/uploads/{upload_id}/cancel
```

## Upload Status

- **pending**: Upload created, awaiting parts
- **completed**: Upload finished, file ready
- **cancelled**: User cancelled upload
- **expired**: Upload expired (not completed within 1 hour)

## Part Management

### Part Size Requirements

- **Minimum**: 5MB per part (except final part)
- **Maximum**: No explicit max per part, but total ≤ 512MB
- **Last part**: Can be any size

### Part Upload Order

Parts can be uploaded in any order:
- Upload parts 1, 3, 2 (out of order)
- Must provide correct order in complete request

### Parallel Part Upload

Upload multiple parts concurrently for faster completion.

## SDK Examples (Python)

### Basic Multipart Upload

```python
from openai import OpenAI
import os

client = OpenAI()

file_path = "large_training_data.jsonl"
file_size = os.path.getsize(file_path)
part_size = 10 * 1024 * 1024  # 10MB chunks

# Create upload
upload = client.uploads.create(
    purpose="fine-tune",
    filename=os.path.basename(file_path),
    bytes=file_size,
    mime_type="application/jsonl"
)

print(f"Upload ID: {upload.id}")

# Upload parts
part_ids = []
with open(file_path, "rb") as f:
    part_number = 0
    while True:
        chunk = f.read(part_size)
        if not chunk:
            break
        
        part = client.uploads.parts.create(
            upload_id=upload.id,
            data=chunk
        )
        part_ids.append(part.id)
        part_number += 1
        print(f"Uploaded part {part_number}")

# Complete upload
completed = client.uploads.complete(
    upload_id=upload.id,
    part_ids=part_ids
)

print(f"File ID: {completed.file.id}")
```

### Resumable Upload

```python
from openai import OpenAI
import os
import pickle

client = OpenAI()

def save_progress(upload_id, part_ids, offset):
    """Save upload progress"""
    with open("upload_progress.pkl", "wb") as f:
        pickle.dump({
            "upload_id": upload_id,
            "part_ids": part_ids,
            "offset": offset
        }, f)

def load_progress():
    """Load upload progress"""
    try:
        with open("upload_progress.pkl", "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None

file_path = "large_file.jsonl"
file_size = os.path.getsize(file_path)
part_size = 10 * 1024 * 1024

# Try to resume
progress = load_progress()

if progress:
    upload_id = progress["upload_id"]
    part_ids = progress["part_ids"]
    offset = progress["offset"]
    print(f"Resuming upload from byte {offset}")
else:
    # Create new upload
    upload = client.uploads.create(
        purpose="fine-tune",
        filename=os.path.basename(file_path),
        bytes=file_size,
        mime_type="application/jsonl"
    )
    upload_id = upload.id
    part_ids = []
    offset = 0
    print("Starting new upload")

# Upload remaining parts
with open(file_path, "rb") as f:
    f.seek(offset)
    
    while True:
        chunk = f.read(part_size)
        if not chunk:
            break
        
        try:
            part = client.uploads.parts.create(
                upload_id=upload_id,
                data=chunk
            )
            part_ids.append(part.id)
            offset += len(chunk)
            
            # Save progress
            save_progress(upload_id, part_ids, offset)
            print(f"Uploaded {offset}/{file_size} bytes")
            
        except Exception as e:
            print(f"Upload interrupted: {e}")
            print("Progress saved, run again to resume")
            raise

# Complete upload
completed = client.uploads.complete(
    upload_id=upload_id,
    part_ids=part_ids
)

# Clean up progress file
os.remove("upload_progress.pkl")
print(f"Upload complete: {completed.file.id}")
```

### Parallel Part Upload

```python
from openai import OpenAI
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

client = OpenAI()

def upload_part(upload_id, chunk, part_number):
    """Upload single part"""
    part = client.uploads.parts.create(
        upload_id=upload_id,
        data=chunk
    )
    return part_number, part.id

file_path = "large_file.jsonl"
file_size = os.path.getsize(file_path)
part_size = 10 * 1024 * 1024

# Create upload
upload = client.uploads.create(
    purpose="fine-tune",
    filename=os.path.basename(file_path),
    bytes=file_size,
    mime_type="application/jsonl"
)

# Read all chunks
chunks = []
with open(file_path, "rb") as f:
    while True:
        chunk = f.read(part_size)
        if not chunk:
            break
        chunks.append(chunk)

print(f"Uploading {len(chunks)} parts in parallel...")

# Upload parts in parallel
part_results = {}
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = {
        executor.submit(upload_part, upload.id, chunk, i): i
        for i, chunk in enumerate(chunks)
    }
    
    for future in as_completed(futures):
        part_num, part_id = future.result()
        part_results[part_num] = part_id
        print(f"Part {part_num + 1}/{len(chunks)} uploaded")

# Complete in correct order
part_ids = [part_results[i] for i in sorted(part_results.keys())]

completed = client.uploads.complete(
    upload_id=upload.id,
    part_ids=part_ids
)

print(f"Upload complete: {completed.file.id}")
```

### Production Upload Manager

```python
from openai import OpenAI
import os
from typing import Optional, Callable
import hashlib

class UploadManager:
    def __init__(self, chunk_size_mb: int = 10):
        self.client = OpenAI()
        self.chunk_size = chunk_size_mb * 1024 * 1024
    
    def upload_large_file(
        self,
        file_path: str,
        purpose: str,
        progress_callback: Optional[Callable] = None
    ) -> str:
        """Upload large file with progress tracking"""
        file_size = os.path.getsize(file_path)
        filename = os.path.basename(file_path)
        
        # Determine MIME type
        mime_type = self._get_mime_type(filename)
        
        # Create upload
        upload = self.client.uploads.create(
            purpose=purpose,
            filename=filename,
            bytes=file_size,
            mime_type=mime_type
        )
        
        print(f"Created upload: {upload.id}")
        
        # Upload parts
        part_ids = []
        bytes_uploaded = 0
        
        with open(file_path, "rb") as f:
            part_number = 0
            
            while True:
                chunk = f.read(self.chunk_size)
                if not chunk:
                    break
                
                part = self.client.uploads.parts.create(
                    upload_id=upload.id,
                    data=chunk
                )
                
                part_ids.append(part.id)
                part_number += 1
                bytes_uploaded += len(chunk)
                
                if progress_callback:
                    progress_callback(bytes_uploaded, file_size)
                
                print(f"Part {part_number}: {bytes_uploaded}/{file_size} bytes")
        
        # Complete upload
        completed = self.client.uploads.complete(
            upload_id=upload.id,
            part_ids=part_ids
        )
        
        return completed.file.id
    
    def _get_mime_type(self, filename: str) -> str:
        """Determine MIME type from filename"""
        ext = os.path.splitext(filename)[1].lower()
        mime_types = {
            ".jsonl": "application/jsonl",
            ".json": "application/json",
            ".pdf": "application/pdf",
            ".txt": "text/plain",
            ".csv": "text/csv"
        }
        return mime_types.get(ext, "application/octet-stream")
    
    def verify_upload(self, file_id: str, original_path: str) -> bool:
        """Verify uploaded file matches original"""
        # Download uploaded file
        content = self.client.files.content(file_id)
        
        # Compare checksums
        uploaded_hash = hashlib.md5(content.content).hexdigest()
        
        with open(original_path, "rb") as f:
            original_hash = hashlib.md5(f.read()).hexdigest()
        
        return uploaded_hash == original_hash

# Usage
manager = UploadManager(chunk_size_mb=10)

def progress(uploaded, total):
    pct = (uploaded / total) * 100
    print(f"Progress: {pct:.1f}%")

file_id = manager.upload_large_file(
    "large_training_data.jsonl",
    purpose="fine-tune",
    progress_callback=progress
)

print(f"File uploaded: {file_id}")

# Verify
if manager.verify_upload(file_id, "large_training_data.jsonl"):
    print("✓ Upload verified")
else:
    print("✗ Upload verification failed")
```

### Cancel Upload

```python
from openai import OpenAI

client = OpenAI()

upload = client.uploads.cancel("upload_abc123")
print(f"Upload cancelled: {upload.status}")
```

## Error Responses

- **400 Bad Request** - Invalid upload parameters or part data
- **404 Not Found** - Upload not found
- **410 Gone** - Upload expired
- **413 Payload Too Large** - Total size exceeds limit

## Rate Limiting / Throttling

- **Upload creation**: Standard rate limits
- **Part uploads**: May have concurrent upload limits
- **Bandwidth**: Network bandwidth constraints

## Differences from Other APIs

- **vs Files API**: Uploads for large files, Files for small
- **vs S3 multipart**: Similar concept, OpenAI-specific
- **vs Resumable uploads (Google)**: Similar resumability features

## Limitations and Known Issues

- **1 hour expiration**: Must complete within 1 hour [VERIFIED] (OAIAPI-SC-OAI-UPLCRT)
- **Part size minimum**: 5MB minimum (except last) [VERIFIED] (OAIAPI-SC-OAI-GUPLOAD)
- **No partial download**: Cannot download incomplete uploads [COMMUNITY] (OAIAPI-SC-SO-UPLDOWN)

## Gotchas and Quirks

- **Order matters on complete**: Must provide parts in correct order [VERIFIED] (OAIAPI-SC-OAI-UPLCMP)
- **Cannot modify parts**: Once uploaded, parts immutable [VERIFIED] (OAIAPI-SC-OAI-GUPLOAD)
- **Expiration non-extendable**: Cannot extend 1-hour limit [COMMUNITY] (OAIAPI-SC-SO-UPLEXP)

## Sources

- OAIAPI-SC-OAI-UPLCRT - POST Create upload
- OAIAPI-SC-OAI-UPLPRT - POST Add upload part
- OAIAPI-SC-OAI-UPLCMP - POST Complete upload
- OAIAPI-SC-OAI-UPLCAN - POST Cancel upload
- OAIAPI-SC-OAI-GUPLOAD - Uploads guide

## Document History

**[2026-03-20 16:07]**
- Initial documentation created
