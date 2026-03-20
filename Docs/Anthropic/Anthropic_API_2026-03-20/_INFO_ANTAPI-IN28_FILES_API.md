# Files API (Beta)

**Doc ID**: ANTAPI-IN28
**Goal**: Document beta Files API - upload, list, retrieve, download, delete operations
**API version**: anthropic-version 2023-06-01

**Depends on:**
- `_INFO_ANTAPI-IN01_INTRODUCTION.md [ANTAPI-IN01]` for base URL, auth headers
- `_INFO_ANTAPI-IN03_VERSIONING.md [ANTAPI-IN03]` for beta header usage

## Summary

The Files API (beta) enables uploading, managing, and referencing files across API calls. Files can be uploaded once and referenced by `file_id` in Messages API requests (e.g., document blocks for PDFs, images). This avoids re-encoding and re-sending large files with every request. The API provides CRUD operations: upload, list, retrieve metadata, download, and delete. Access requires the `files-api-2025-04-14` beta header.

## Key Facts

- **Base Endpoint**: `/v1/files`
- **Beta Header**: `files-api-2025-04-14`
- **SDK Namespace**: `client.beta.files`
- **Operations**: upload, list, retrieve_metadata, download, delete
- **File Reference**: Use `file_id` in document/image source blocks
- **Max File Size**: 500 MB per file
- **Total Storage**: 500 GB per organization
- **Rate Limit**: ~100 requests per minute (beta)
- **Status**: Beta

## Endpoints

### POST /v1/files - Upload File

```python
import anthropic

client = anthropic.Anthropic()

# Upload a file
uploaded = client.beta.files.upload(
    file=open("document.pdf", "rb"),
    purpose="messages",
)
print(f"File ID: {uploaded.id}")
print(f"Filename: {uploaded.filename}")
print(f"Size: {uploaded.size_bytes}")
```

### GET /v1/files - List Files

```python
files = client.beta.files.list()
for f in files:
    print(f"{f.id}: {f.filename} ({f.size_bytes} bytes)")
```

### GET /v1/files/{file_id} - Retrieve Metadata

```python
metadata = client.beta.files.retrieve_metadata("file-abc123")
print(f"Filename: {metadata.filename}")
print(f"Purpose: {metadata.purpose}")
print(f"Created: {metadata.created_at}")
```

### GET /v1/files/{file_id}/content - Download File

```python
content = client.beta.files.download("file-abc123")
with open("downloaded.pdf", "wb") as f:
    f.write(content.content)
```

### DELETE /v1/files/{file_id} - Delete File

```python
result = client.beta.files.delete("file-abc123")
print(f"Deleted: {result.id}")
```

## Using Files in Messages

Reference uploaded files by `file_id` in document or image source blocks:

```python
# Upload once
uploaded = client.beta.files.upload(
    file=open("report.pdf", "rb"),
    purpose="messages",
)

# Reference in multiple requests
message = client.beta.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    betas=["files-api-2025-04-14"],
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {
                        "type": "file",
                        "file_id": uploaded.id,
                    },
                    "citations": {"enabled": True},
                },
                {"type": "text", "text": "Summarize this document."},
            ],
        }
    ],
)
```

## FileMetadata Response

- **id** (`string`) - File identifier (format: `file_...`)
- **type** (`string`) - Always `"file"`
- **filename** (`string`) - Original filename
- **mime_type** (`string`) - Detected MIME type
- **size_bytes** (`integer`) - File size in bytes
- **created_at** (`string`) - ISO 8601 creation timestamp
- **downloadable** (`boolean`) - Whether the file can be downloaded

## Supported File Types

- **application/pdf** - Used as `document` content block
- **text/plain** - Used as `document` content block
- **image/jpeg** - Used as `image` content block
- **image/png** - Used as `image` content block
- **image/gif** - Used as `image` content block
- **image/webp** - Used as `image` content block
- **Datasets and others** - Used as `container_upload` for code execution tool

## Storage Limits

- **Maximum file size**: 500 MB per file
- **Total storage**: 500 GB per organization
- **Rate limits**: ~100 requests per minute during beta (contact Anthropic for higher limits)

## File Lifecycle

- Files are scoped to the workspace of the API key that created them
- Other API keys in the same workspace can access the files
- Files persist until explicitly deleted
- Deleted files cannot be recovered
- Files become inaccessible via API shortly after deletion, but may persist in active Messages API calls
- Deleted files are removed per Anthropic's data retention policy

## Gotchas and Quirks

- Requires `files-api-2025-04-14` beta header
- Use `client.beta.files` namespace in SDK
- **500 MB** max per file, **500 GB** total per organization
- **~100 RPM** rate limit during beta
- Files scoped to workspace, not individual API key (all keys in same workspace share access)
- `.csv`, `.xlsx`, `.docx` files should be converted to plain text before use in document blocks
- File references reduce request size vs base64 encoding for repeated use
- `downloadable` field in response indicates whether the file content can be retrieved
- Deleted files may still be accessible in already-active Messages API calls

## Related Endpoints

- `_INFO_ANTAPI-IN06_MESSAGES.md [ANTAPI-IN06]` - Messages API (file_id in source blocks)
- `_INFO_ANTAPI-IN15_CITATIONS.md [ANTAPI-IN15]` - Citations with file-referenced documents
- `_INFO_ANTAPI-IN17_PDF_SUPPORT.md [ANTAPI-IN17]` - PDF input via file reference

## Sources

- ANTAPI-SC-ANTH-FILES - https://platform.claude.com/docs/en/build-with-claude/files - Files guide
- ANTAPI-SC-GH-SDKAPI - https://github.com/anthropics/anthropic-sdk-python/blob/main/api.md - FileMetadata, DeletedFile types

## Document History

**[2026-03-20 04:45]**
- Added: Storage limits (500 MB/file, 500 GB/org)
- Added: Rate limits (~100 RPM beta)
- Added: Supported file types with content block mapping
- Added: File lifecycle details (workspace scoping, deletion behavior)
- Added: FileMetadata fields (type, mime_type, downloadable)

**[2026-03-20 04:05]**
- Initial documentation created from Files guide and SDK API types
