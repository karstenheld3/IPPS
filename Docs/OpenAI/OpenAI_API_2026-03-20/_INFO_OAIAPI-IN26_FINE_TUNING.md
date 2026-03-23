# Fine-tuning API

**Doc ID**: OAIAPI-IN26
**Goal**: Document fine-tuning API for custom model training, jobs, hyperparameters, and checkpoints
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references

## Summary

Fine-tuning API (POST /v1/fine_tuning/jobs) trains custom models on user-provided datasets. Upload training data via Files API (JSONL format with prompt-completion pairs), create fine-tuning job specifying base model and hyperparameters, monitor progress via job status, and use fine-tuned model ID in API calls. Supports models: gpt-4o, gpt-4o-mini, gpt-5.4-mini. Minimum 10 training examples required. Hyperparameters: n_epochs, batch_size, learning_rate_multiplier. Job statuses: validating_files, running, succeeded, failed, cancelled. Checkpoints saved during training for recovery. Validation data optional for metrics. Costs: training tokens + base model usage. Use for domain adaptation, style consistency, instruction following, task specialization. Results in model ID like ft:gpt-4o:org:suffix:abc123. [VERIFIED] (OAIAPI-SC-OAI-FTCRT, OAIAPI-SC-OAI-GFTUNE)

## Key Facts

- **Endpoint**: POST /v1/fine_tuning/jobs [VERIFIED] (OAIAPI-SC-OAI-FTCRT)
- **Supported models**: gpt-4o, gpt-4o-mini, gpt-5.4-mini [VERIFIED] (OAIAPI-SC-OAI-GFTUNE)
- **Min examples**: 10 training examples [VERIFIED] (OAIAPI-SC-OAI-GFTUNE)
- **Format**: JSONL with messages array [VERIFIED] (OAIAPI-SC-OAI-GFTUNE)
- **Duration**: Hours to days depending on dataset size [VERIFIED] (OAIAPI-SC-OAI-FTCRT)

## Use Cases

- **Domain adaptation**: Medical, legal, technical domains
- **Style matching**: Brand voice, writing style
- **Task specialization**: Specific workflows, instructions
- **Quality improvement**: Reduce errors on specific tasks
- **Cost optimization**: Use smaller fine-tuned models

## Quick Reference

```python
# Upload training data
POST /v1/files
file: training_data.jsonl
purpose: fine-tune

# Create fine-tuning job
POST /v1/fine_tuning/jobs
{
  "model": "gpt-4o-mini",
  "training_file": "file_abc123",
  "hyperparameters": {
    "n_epochs": 3
  }
}

# Use fine-tuned model
model="ft:gpt-4o-mini:org:suffix:abc123"
```

## Training Data Format

### JSONL Structure

Each line is JSON object with messages array:

```jsonl
{"messages": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "What is AI?"}, {"role": "assistant", "content": "AI is artificial intelligence..."}]}
{"messages": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "Explain ML"}, {"role": "assistant", "content": "ML is machine learning..."}]}
```

### Message Roles

- **system**: System prompt (optional)
- **user**: User message
- **assistant**: Model response
- **function**: Function call results (if using functions)

### Data Requirements

- **Minimum**: 10 examples
- **Recommended**: 50-100 examples for quality
- **Optimal**: 100+ examples for best results
- **Format**: Valid JSONL (one JSON per line)
- **Encoding**: UTF-8

## Creating Fine-tuning Job

### Request Parameters

**Required:**
- **model**: Base model ID (gpt-4o, gpt-4o-mini, gpt-5.4-mini)
- **training_file**: File ID from Files API

**Optional:**
- **validation_file**: Validation data file ID
- **hyperparameters**: Training configuration
  - **n_epochs**: Number of training epochs (1-50, auto by default)
  - **batch_size**: Batch size (auto by default)
  - **learning_rate_multiplier**: Learning rate multiplier (auto by default)
- **suffix**: Custom suffix for model ID (max 40 chars)
- **seed**: Random seed for reproducibility

### Hyperparameters

**n_epochs:**
- Higher = more training, potential overfitting
- Lower = less training, potential underfitting
- Default: Auto-determined

**batch_size:**
- Larger = faster training, more memory
- Smaller = slower training, less memory
- Default: Auto-determined

**learning_rate_multiplier:**
- Higher = faster learning, less stable
- Lower = slower learning, more stable
- Default: Auto-determined

## Job Status

### Status Values

- **validating_files**: Checking uploaded data
- **queued**: Waiting to start
- **running**: Training in progress
- **succeeded**: Completed successfully
- **failed**: Training failed
- **cancelled**: User cancelled job

### Monitoring Progress

```
GET /v1/fine_tuning/jobs/{job_id}
```

**Response includes:**
- Training metrics (loss, accuracy)
- Estimated completion time
- Current epoch
- Checkpoint information

## Checkpoints

Saved periodically during training:
- Resume from checkpoint if job fails
- Evaluate intermediate models
- Early stopping if validation metrics degrade

Access checkpoints:
```
GET /v1/fine_tuning/jobs/{job_id}/checkpoints
```

## Using Fine-tuned Models

### Model ID Format

```
ft:{base_model}:{org_id}:{suffix}:{job_id}
```

Example: `ft:gpt-4o-mini:org-abc:customer-support:ft-123`

### API Usage

Use like any other model:
```python
client.chat.completions.create(
    model="ft:gpt-4o-mini:org-abc:support:ft-123",
    messages=[...]
)
```

## SDK Examples (Python)

### Prepare Training Data

```python
import json

training_data = [
    {
        "messages": [
            {"role": "system", "content": "You are a customer support agent."},
            {"role": "user", "content": "How do I reset my password?"},
            {"role": "assistant", "content": "To reset your password: 1. Click 'Forgot Password' 2. Enter your email 3. Check your inbox for reset link"}
        ]
    },
    {
        "messages": [
            {"role": "system", "content": "You are a customer support agent."},
            {"role": "user", "content": "Where is my order?"},
            {"role": "assistant", "content": "I can help you track your order. Please provide your order number."}
        ]
    }
    # ... more examples
]

# Save to JSONL
with open("training_data.jsonl", "w") as f:
    for item in training_data:
        f.write(json.dumps(item) + "\n")
```

### Upload Training File

```python
from openai import OpenAI

client = OpenAI()

# Upload file
with open("training_data.jsonl", "rb") as f:
    training_file = client.files.create(
        file=f,
        purpose="fine-tune"
    )

print(f"File ID: {training_file.id}")
```

### Create Fine-tuning Job

```python
from openai import OpenAI

client = OpenAI()

job = client.fine_tuning.jobs.create(
    model="gpt-4o-mini",
    training_file="file_abc123",
    hyperparameters={
        "n_epochs": 3
    },
    suffix="customer-support"
)

print(f"Job ID: {job.id}")
print(f"Status: {job.status}")
```

### Monitor Job Progress

```python
from openai import OpenAI
import time

client = OpenAI()

job_id = "ftjob-abc123"

while True:
    job = client.fine_tuning.jobs.retrieve(job_id)
    print(f"Status: {job.status}")
    
    if job.status in ["succeeded", "failed", "cancelled"]:
        break
    
    time.sleep(60)  # Check every minute

if job.status == "succeeded":
    print(f"Fine-tuned model: {job.fine_tuned_model}")
else:
    print(f"Job {job.status}: {job.error}")
```

### Use Fine-tuned Model

```python
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="ft:gpt-4o-mini:org-abc:support:ftjob-123",
    messages=[
        {"role": "system", "content": "You are a customer support agent."},
        {"role": "user", "content": "I need help with billing"}
    ]
)

print(response.choices[0].message.content)
```

### With Validation Data

```python
from openai import OpenAI

client = OpenAI()

# Upload validation file
with open("validation_data.jsonl", "rb") as f:
    val_file = client.files.create(
        file=f,
        purpose="fine-tune"
    )

# Create job with validation
job = client.fine_tuning.jobs.create(
    model="gpt-4o-mini",
    training_file="file_train_abc",
    validation_file=val_file.id,
    hyperparameters={
        "n_epochs": 5
    }
)

print(f"Job created: {job.id}")
```

### List All Jobs

```python
from openai import OpenAI

client = OpenAI()

jobs = client.fine_tuning.jobs.list(limit=10)

for job in jobs.data:
    print(f"{job.id}: {job.status} - {job.fine_tuned_model}")
```

### Cancel Job

```python
from openai import OpenAI

client = OpenAI()

job = client.fine_tuning.jobs.cancel("ftjob-abc123")
print(f"Job cancelled: {job.status}")
```

### Production Fine-tuning Pipeline

```python
from openai import OpenAI
import time
import json
from typing import List, Dict

class FineTuningPipeline:
    def __init__(self):
        self.client = OpenAI()
    
    def prepare_data(self, examples: List[Dict], output_file: str):
        """Prepare training data in JSONL format"""
        with open(output_file, "w") as f:
            for example in examples:
                f.write(json.dumps({"messages": example}) + "\n")
        return output_file
    
    def upload_file(self, file_path: str) -> str:
        """Upload training file"""
        with open(file_path, "rb") as f:
            file = self.client.files.create(
                file=f,
                purpose="fine-tune"
            )
        return file.id
    
    def create_job(
        self,
        model: str,
        training_file_id: str,
        validation_file_id: str = None,
        n_epochs: int = 3,
        suffix: str = None
    ) -> str:
        """Create fine-tuning job"""
        params = {
            "model": model,
            "training_file": training_file_id,
            "hyperparameters": {"n_epochs": n_epochs}
        }
        
        if validation_file_id:
            params["validation_file"] = validation_file_id
        if suffix:
            params["suffix"] = suffix
        
        job = self.client.fine_tuning.jobs.create(**params)
        return job.id
    
    def wait_for_completion(self, job_id: str, check_interval: int = 60):
        """Wait for job to complete"""
        while True:
            job = self.client.fine_tuning.jobs.retrieve(job_id)
            print(f"Status: {job.status}")
            
            if job.status == "succeeded":
                return job.fine_tuned_model
            elif job.status in ["failed", "cancelled"]:
                raise Exception(f"Job {job.status}: {job.error}")
            
            time.sleep(check_interval)
    
    def fine_tune(
        self,
        examples: List[Dict],
        model: str = "gpt-4o-mini",
        validation_split: float = 0.1,
        n_epochs: int = 3,
        suffix: str = None
    ) -> str:
        """Complete fine-tuning pipeline"""
        # Split data
        split_idx = int(len(examples) * (1 - validation_split))
        train_examples = examples[:split_idx]
        val_examples = examples[split_idx:]
        
        # Prepare files
        self.prepare_data(train_examples, "train.jsonl")
        self.prepare_data(val_examples, "val.jsonl")
        
        # Upload files
        train_file_id = self.upload_file("train.jsonl")
        val_file_id = self.upload_file("val.jsonl")
        
        # Create job
        job_id = self.create_job(
            model=model,
            training_file_id=train_file_id,
            validation_file_id=val_file_id,
            n_epochs=n_epochs,
            suffix=suffix
        )
        
        print(f"Fine-tuning job started: {job_id}")
        
        # Wait for completion
        model_id = self.wait_for_completion(job_id)
        print(f"Fine-tuned model ready: {model_id}")
        
        return model_id

# Usage
pipeline = FineTuningPipeline()

examples = [
    [
        {"role": "system", "content": "You are an expert."},
        {"role": "user", "content": "Question 1"},
        {"role": "assistant", "content": "Answer 1"}
    ],
    # ... more examples
]

model_id = pipeline.fine_tune(
    examples=examples,
    model="gpt-4o-mini",
    n_epochs=3,
    suffix="my-model"
)
```

## Error Responses

- **400 Bad Request** - Invalid training data or parameters
- **404 Not Found** - File or job not found
- **429 Too Many Requests** - Rate limit exceeded

## Rate Limiting / Throttling

- **Job creation**: Limited concurrent jobs
- **Training cost**: Charged per training token
- **Model usage**: Standard rate limits apply

## Differences from Other APIs

- **vs Hugging Face**: OpenAI managed infrastructure, HF more control
- **vs Cohere Fine-tuning**: Similar capabilities, different models
- **vs Cloud providers**: OpenAI simpler, clouds more customization

## Limitations and Known Issues

- **Limited models**: Only specific models support fine-tuning [VERIFIED] (OAIAPI-SC-OAI-GFTUNE)
- **Training time**: Can take hours to days [VERIFIED] (OAIAPI-SC-OAI-FTCRT)
- **Cost**: Training can be expensive for large datasets [COMMUNITY] (OAIAPI-SC-SO-FTCOST)

## Gotchas and Quirks

- **Auto hyperparameters**: Default auto often best [VERIFIED] (OAIAPI-SC-OAI-GFTUNE)
- **Overfitting risk**: Too many epochs can overfit [COMMUNITY] (OAIAPI-SC-SO-FTOVER)
- **Data quality matters**: More than quantity [COMMUNITY] (OAIAPI-SC-SO-FTDATA)

## Sources

- OAIAPI-SC-OAI-FTCRT - POST Create fine-tuning job
- OAIAPI-SC-OAI-FTGET - GET Retrieve fine-tuning job
- OAIAPI-SC-OAI-GFTUNE - Fine-tuning guide

## Document History

**[2026-03-20 16:00]**
- Initial documentation created
