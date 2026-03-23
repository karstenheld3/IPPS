# Batch API

**Doc ID**: OAIAPI-IN27
**Goal**: Document Batch API for async bulk processing with 50% cost reduction and rate limit bypass
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references

## Summary

Batch API (POST /v1/batches) processes large volumes of API requests asynchronously with 50% cost reduction and no rate limits. Upload JSONL file containing requests, create batch job, and retrieve results file when complete. Supports endpoints: /v1/chat/completions, /v1/embeddings, /v1/completions (legacy). Maximum 50,000 requests per batch. Completion window: 24 hours. Batch statuses: validating, in_progress, finalizing, completed, failed, expired, cancelled. Results include successes and failures with request IDs for matching. Ideal for bulk embeddings, data processing, offline evaluations, and cost-sensitive workloads. Trade-off: 24-hour latency for 50% savings. No streaming support. Results file contains one response per line matching input order. [VERIFIED] (OAIAPI-SC-OAI-BATCRT, OAIAPI-SC-OAI-GBATCH)

## Key Facts

- **Cost**: 50% discount vs real-time API [VERIFIED] (OAIAPI-SC-OAI-GBATCH)
- **Rate limits**: No RPM/TPM limits [VERIFIED] (OAIAPI-SC-OAI-GBATCH)
- **Completion**: Within 24 hours [VERIFIED] (OAIAPI-SC-OAI-BATCRT)
- **Max requests**: 50,000 per batch [VERIFIED] (OAIAPI-SC-OAI-GBATCH)
- **Supported endpoints**: chat/completions, embeddings, completions [VERIFIED] (OAIAPI-SC-OAI-GBATCH)

## Use Cases

- **Bulk embeddings**: Process thousands of documents
- **Data processing**: Transform large datasets
- **Evaluations**: Run eval suites offline
- **Content generation**: Generate batch content
- **Cost optimization**: 50% savings for non-urgent work

## Quick Reference

```python
# Upload batch file
POST /v1/files
file: batch_requests.jsonl
purpose: batch

# Create batch
POST /v1/batches
{
  "input_file_id": "file_abc123",
  "endpoint": "/v1/chat/completions",
  "completion_window": "24h"
}

# Check status
GET /v1/batches/{batch_id}

# Download results
GET /v1/files/{output_file_id}/content
```

## Request Format

### JSONL Structure

Each line contains:
```json
{
  "custom_id": "request-1",
  "method": "POST",
  "url": "/v1/chat/completions",
  "body": {
    "model": "gpt-5.4-mini",
    "messages": [
      {"role": "user", "content": "Hello"}
    ]
  }
}
```

### Required Fields

- **custom_id**: Unique identifier for request (max 64 chars)
- **method**: HTTP method (always "POST")
- **url**: API endpoint
- **body**: Request parameters (same as real-time API)

### Supported Endpoints

- `/v1/chat/completions`
- `/v1/embeddings`
- `/v1/completions` (legacy)

## Creating Batch

### Request Parameters

**Required:**
- **input_file_id**: File ID from Files API
- **endpoint**: Target endpoint
- **completion_window**: "24h" (only option currently)

### Batch Object

```json
{
  "id": "batch_abc123",
  "object": "batch",
  "endpoint": "/v1/chat/completions",
  "input_file_id": "file_xyz",
  "completion_window": "24h",
  "status": "in_progress",
  "created_at": 1234567890,
  "request_counts": {
    "total": 1000,
    "completed": 500,
    "failed": 10
  }
}
```

## Batch Status

### Status Values

- **validating**: Checking input file
- **in_progress**: Processing requests
- **finalizing**: Completing batch
- **completed**: All requests processed
- **failed**: Batch failed
- **expired**: Exceeded 24-hour window
- **cancelled**: User cancelled

### Monitoring Progress

```
GET /v1/batches/{batch_id}
```

Check `request_counts` for progress:
- **total**: Total requests
- **completed**: Successfully processed
- **failed**: Failed requests

## Results Format

### Success Response

```json
{
  "id": "batch_req_abc",
  "custom_id": "request-1",
  "response": {
    "status_code": 200,
    "request_id": "req_xyz",
    "body": {
      "id": "chatcmpl_123",
      "object": "chat.completion",
      "created": 1234567890,
      "model": "gpt-5.4-mini",
      "choices": [...]
    }
  },
  "error": null
}
```

### Error Response

```json
{
  "id": "batch_req_def",
  "custom_id": "request-2",
  "response": {
    "status_code": 400,
    "request_id": "req_abc"
  },
  "error": {
    "message": "Invalid request",
    "type": "invalid_request_error",
    "code": "invalid_value"
  }
}
```

## SDK Examples (Python)

### Prepare Batch File

```python
import json

requests = []
for i in range(1000):
    requests.append({
        "custom_id": f"request-{i}",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "gpt-5.4-mini",
            "messages": [
                {"role": "user", "content": f"Summarize article {i}"}
            ],
            "max_tokens": 100
        }
    })

# Save to JSONL
with open("batch_requests.jsonl", "w") as f:
    for req in requests:
        f.write(json.dumps(req) + "\n")
```

### Upload and Create Batch

```python
from openai import OpenAI

client = OpenAI()

# Upload file
with open("batch_requests.jsonl", "rb") as f:
    batch_file = client.files.create(
        file=f,
        purpose="batch"
    )

# Create batch
batch = client.batches.create(
    input_file_id=batch_file.id,
    endpoint="/v1/chat/completions",
    completion_window="24h"
)

print(f"Batch ID: {batch.id}")
print(f"Status: {batch.status}")
```

### Monitor Batch Progress

```python
from openai import OpenAI
import time

client = OpenAI()

batch_id = "batch_abc123"

while True:
    batch = client.batches.retrieve(batch_id)
    
    print(f"Status: {batch.status}")
    print(f"Progress: {batch.request_counts.completed}/{batch.request_counts.total}")
    
    if batch.status in ["completed", "failed", "expired", "cancelled"]:
        break
    
    time.sleep(60)  # Check every minute

if batch.status == "completed":
    print(f"Output file: {batch.output_file_id}")
```

### Download and Parse Results

```python
from openai import OpenAI
import json

client = OpenAI()

batch = client.batches.retrieve("batch_abc123")

if batch.status == "completed":
    # Download results
    result_file = client.files.content(batch.output_file_id)
    results = result_file.text.split('\n')
    
    # Parse results
    for line in results:
        if line.strip():
            result = json.loads(line)
            custom_id = result["custom_id"]
            
            if result["error"]:
                print(f"{custom_id}: ERROR - {result['error']['message']}")
            else:
                response = result["response"]["body"]
                content = response["choices"][0]["message"]["content"]
                print(f"{custom_id}: {content[:50]}...")
```

### Bulk Embeddings

```python
from openai import OpenAI
import json

client = OpenAI()

# Prepare embedding requests
texts = ["Text 1", "Text 2", ...] * 1000  # 10,000 texts

requests = []
for i, text in enumerate(texts):
    requests.append({
        "custom_id": f"embed-{i}",
        "method": "POST",
        "url": "/v1/embeddings",
        "body": {
            "model": "text-embedding-3-small",
            "input": text
        }
    })

# Save and upload
with open("embeddings_batch.jsonl", "w") as f:
    for req in requests:
        f.write(json.dumps(req) + "\n")

with open("embeddings_batch.jsonl", "rb") as f:
    batch_file = client.files.create(file=f, purpose="batch")

# Create batch
batch = client.batches.create(
    input_file_id=batch_file.id,
    endpoint="/v1/embeddings",
    completion_window="24h"
)

print(f"Processing {len(texts)} embeddings at 50% cost")
print(f"Batch ID: {batch.id}")
```

### Cancel Batch

```python
from openai import OpenAI

client = OpenAI()

batch = client.batches.cancel("batch_abc123")
print(f"Batch cancelled: {batch.status}")
```

### Production Batch Pipeline

```python
from openai import OpenAI
import json
import time
from typing import List, Dict, Callable

class BatchProcessor:
    def __init__(self):
        self.client = OpenAI()
    
    def create_batch_file(
        self,
        requests: List[Dict],
        filename: str = "batch.jsonl"
    ) -> str:
        """Create batch request file"""
        with open(filename, "w") as f:
            for req in requests:
                f.write(json.dumps(req) + "\n")
        return filename
    
    def upload_and_create(
        self,
        file_path: str,
        endpoint: str
    ) -> str:
        """Upload file and create batch"""
        with open(file_path, "rb") as f:
            batch_file = self.client.files.create(
                file=f,
                purpose="batch"
            )
        
        batch = self.client.batches.create(
            input_file_id=batch_file.id,
            endpoint=endpoint,
            completion_window="24h"
        )
        
        return batch.id
    
    def wait_for_completion(
        self,
        batch_id: str,
        check_interval: int = 300,  # 5 minutes
        callback: Callable = None
    ) -> Dict:
        """Wait for batch to complete"""
        while True:
            batch = self.client.batches.retrieve(batch_id)
            
            if callback:
                callback(batch)
            
            if batch.status in ["completed", "failed", "expired", "cancelled"]:
                return {
                    "status": batch.status,
                    "output_file_id": batch.output_file_id,
                    "error_file_id": batch.error_file_id,
                    "counts": batch.request_counts
                }
            
            time.sleep(check_interval)
    
    def download_results(
        self,
        output_file_id: str,
        output_path: str = "results.jsonl"
    ) -> List[Dict]:
        """Download and parse results"""
        content = self.client.files.content(output_file_id)
        
        results = []
        for line in content.text.split('\n'):
            if line.strip():
                results.append(json.loads(line))
        
        # Save to file
        with open(output_path, "w") as f:
            f.write(content.text)
        
        return results
    
    def process_batch(
        self,
        requests: List[Dict],
        endpoint: str,
        wait: bool = True
    ) -> Dict:
        """Complete batch processing pipeline"""
        # Create file
        file_path = self.create_batch_file(requests)
        
        # Upload and create batch
        batch_id = self.upload_and_create(file_path, endpoint)
        print(f"Batch created: {batch_id}")
        
        if not wait:
            return {"batch_id": batch_id}
        
        # Wait for completion
        def progress_callback(batch):
            counts = batch.request_counts
            print(f"Progress: {counts.completed}/{counts.total} "
                  f"(Failed: {counts.failed})")
        
        result = self.wait_for_completion(batch_id, callback=progress_callback)
        
        if result["status"] == "completed":
            results = self.download_results(result["output_file_id"])
            return {
                "batch_id": batch_id,
                "status": "completed",
                "results": results,
                "total": len(results),
                "failed": result["counts"].get("failed", 0)
            }
        else:
            return {
                "batch_id": batch_id,
                "status": result["status"],
                "error": "Batch did not complete successfully"
            }

# Usage
processor = BatchProcessor()

requests = [
    {
        "custom_id": f"req-{i}",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "gpt-5.4-mini",
            "messages": [{"role": "user", "content": f"Task {i}"}]
        }
    }
    for i in range(5000)
]

result = processor.process_batch(
    requests=requests,
    endpoint="/v1/chat/completions",
    wait=True
)

print(f"\nCompleted: {result['total']} requests")
print(f"Failed: {result['failed']}")
```

## Error Responses

- **400 Bad Request** - Invalid batch file or parameters
- **404 Not Found** - Batch or file not found
- **429 Too Many Requests** - Too many active batches

## Rate Limiting / Throttling

- **No request limits**: Batch API bypasses RPM/TPM
- **Batch limits**: Limited concurrent batches
- **File size**: Max file size for batch input

## Differences from Other APIs

- **vs Real-time API**: 50% cheaper, 24h latency vs instant
- **vs Async libraries**: Built-in infrastructure vs custom
- **vs Cloud batch**: OpenAI managed vs self-hosted

## Limitations and Known Issues

- **24-hour window**: Must complete within 24h [VERIFIED] (OAIAPI-SC-OAI-BATCRT)
- **No streaming**: Cannot stream batch responses [VERIFIED] (OAIAPI-SC-OAI-GBATCH)
- **50K limit**: Max 50,000 requests per batch [VERIFIED] (OAIAPI-SC-OAI-GBATCH)

## Gotchas and Quirks

- **custom_id must be unique**: Duplicates cause errors [VERIFIED] (OAIAPI-SC-OAI-GBATCH)
- **Results unordered**: Match by custom_id, not line number [COMMUNITY] (OAIAPI-SC-SO-BATORD)
- **Partial failures**: Some requests can fail while batch completes [VERIFIED] (OAIAPI-SC-OAI-GBATCH)

## Sources

- OAIAPI-SC-OAI-BATCRT - POST Create batch
- OAIAPI-SC-OAI-BATGET - GET Retrieve batch
- OAIAPI-SC-OAI-GBATCH - Batch API guide

## Document History

**[2026-03-20 16:03]**
- Initial documentation created
