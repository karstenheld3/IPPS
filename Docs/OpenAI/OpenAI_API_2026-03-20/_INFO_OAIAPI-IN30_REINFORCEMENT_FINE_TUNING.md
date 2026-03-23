# Reinforcement Fine-Tuning

**Doc ID**: OAIAPI-IN30
**Goal**: Document reinforcement fine-tuning (RFT), DPO, grader-based training, and training metrics
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references

## Summary

Reinforcement Fine-Tuning (RFT) extends standard supervised fine-tuning with preference-based optimization. Direct Preference Optimization (DPO) trains models to prefer certain outputs over others using paired examples (chosen vs rejected responses). RFT uses graders to automatically evaluate model outputs during training, enabling reward-based optimization without manual preference labeling. Graders score model outputs against criteria (correctness, style, safety) and feed rewards back into the training loop. Supported models include gpt-4.1, gpt-4.1-mini, and gpt-4.1-nano for DPO fine-tuning. Training data format for DPO: JSONL with `messages` (conversation), `chosen` (preferred response), and `rejected` (dispreferred response). Training metrics include reward accuracy, loss curves, and grader scores per checkpoint. RFT enables domain-specific optimization: train models to follow specific coding styles, adhere to safety guidelines, or match expert preferences. Checkpoints are saved during training for evaluation and rollback. [VERIFIED] (OAIAPI-SC-OAI-GRFT, OAIAPI-SC-OAI-FTGRAD)

## Key Facts

- **DPO**: Direct Preference Optimization with chosen/rejected pairs [VERIFIED] (OAIAPI-SC-OAI-GRFT)
- **Graders**: Automated output evaluation for reward signals [VERIFIED] (OAIAPI-SC-OAI-FTGRAD)
- **Models**: gpt-4.1, gpt-4.1-mini, gpt-4.1-nano support DPO [VERIFIED] (OAIAPI-SC-OAI-GRFT)
- **Data format**: JSONL with messages, chosen, rejected [VERIFIED] (OAIAPI-SC-OAI-GRFT)
- **Metrics**: Reward accuracy, loss, grader scores [VERIFIED] (OAIAPI-SC-OAI-GRFT)
- **Checkpoints**: Saved during training for evaluation [VERIFIED] (OAIAPI-SC-OAI-FTCKPT)

## Use Cases

- **Preference alignment**: Align model outputs with expert preferences
- **Style enforcement**: Train model to follow specific writing or coding styles
- **Safety fine-tuning**: Reinforce safe behavior, penalize unsafe outputs
- **Domain expertise**: Optimize for domain-specific correctness (legal, medical, financial)
- **Quality improvement**: Improve output quality based on human feedback

## DPO Training Data Format

```jsonl
{"messages": [{"role": "user", "content": "Write a Python function to sort a list"}], "chosen": {"role": "assistant", "content": "def sort_list(items):\n    return sorted(items)"}, "rejected": {"role": "assistant", "content": "items.sort()\nreturn items"}}
```

### Fields

- **messages**: Conversation context (system + user messages)
- **chosen**: Preferred assistant response
- **rejected**: Dispreferred assistant response

## Grader-Based Training

Graders automatically evaluate model outputs:

```json
{
  "type": "score",
  "name": "code_quality",
  "model": "gpt-5.4",
  "input": "Rate the code quality from 0 to 1 based on: readability, correctness, efficiency",
  "pass_threshold": 0.7
}
```

### Grader Types

- **Score grader**: Returns a numeric score (0-1)
- **Label grader**: Returns a categorical label (pass/fail)
- **Custom grader**: User-defined evaluation logic

## SDK Examples (Python)

### Create DPO Fine-Tuning Job

```python
from openai import OpenAI

client = OpenAI()

# Upload DPO training file
with open("dpo_training.jsonl", "rb") as f:
    training_file = client.files.create(file=f, purpose="fine-tune")

# Create DPO fine-tuning job
job = client.fine_tuning.jobs.create(
    model="gpt-4.1",
    training_file=training_file.id,
    method={
        "type": "dpo",
        "dpo": {
            "hyperparameters": {
                "n_epochs": 3,
                "beta": 0.1  # DPO temperature parameter
            }
        }
    },
    suffix="my-dpo-model"
)

print(f"Job ID: {job.id}")
print(f"Status: {job.status}")
```

### RFT with Graders

```python
from openai import OpenAI

client = OpenAI()

# Upload training file
with open("rft_training.jsonl", "rb") as f:
    training_file = client.files.create(file=f, purpose="fine-tune")

# Create RFT job with grader
job = client.fine_tuning.jobs.create(
    model="gpt-4.1-mini",
    training_file=training_file.id,
    method={
        "type": "reinforcement",
        "reinforcement": {
            "grader": {
                "type": "score",
                "name": "quality_check",
                "model": "gpt-5.4",
                "input": "Evaluate this response for accuracy and helpfulness. Score 0-1.",
                "pass_threshold": 0.7
            },
            "hyperparameters": {
                "n_epochs": 2,
                "reasoning_effort": "medium"
            }
        }
    }
)

print(f"Job: {job.id}, Status: {job.status}")
```

### Monitor Training Metrics

```python
from openai import OpenAI

client = OpenAI()

def monitor_rft_job(job_id: str):
    """Monitor RFT job training metrics"""
    # Get job details
    job = client.fine_tuning.jobs.retrieve(job_id)
    print(f"Status: {job.status}")
    
    # List events
    events = client.fine_tuning.jobs.list_events(job_id, limit=20)
    for event in events.data:
        print(f"  [{event.created_at}] {event.message}")
        if event.data:
            metrics = event.data
            if "reward_accuracy" in metrics:
                print(f"    Reward accuracy: {metrics['reward_accuracy']:.3f}")
            if "loss" in metrics:
                print(f"    Loss: {metrics['loss']:.4f}")
    
    # List checkpoints
    checkpoints = client.fine_tuning.jobs.checkpoints.list(job_id)
    for cp in checkpoints.data:
        print(f"  Checkpoint: {cp.id} (step {cp.step_number})")
        if cp.metrics:
            print(f"    Metrics: {cp.metrics}")

monitor_rft_job("ftjob-abc123")
```

## Error Responses

- **400 Bad Request** - Invalid training data format or DPO configuration
- **404 Not Found** - Training file not found
- **429 Too Many Requests** - Concurrent fine-tuning limit

## Differences from Other APIs

- **vs Anthropic**: Anthropic uses RLHF internally but no public RFT/DPO API
- **vs Gemini**: Google has fine-tuning via Vertex AI but no public DPO API
- **vs Grok**: No public fine-tuning API

## Limitations and Known Issues

- **DPO data quality**: Chosen/rejected pairs must be clearly differentiated [VERIFIED] (OAIAPI-SC-OAI-GRFT)
- **Grader cost**: Grader evaluations consume tokens during training [VERIFIED] (OAIAPI-SC-OAI-FTGRAD)
- **Model support**: Not all models support DPO/RFT [VERIFIED] (OAIAPI-SC-OAI-GRFT)

## Sources

- OAIAPI-SC-OAI-GRFT - Reinforcement Fine-Tuning Guide
- OAIAPI-SC-OAI-FTGRAD - Fine-Tuning Graders API
- OAIAPI-SC-OAI-FTCKPT - Fine-Tuning Checkpoints

## Document History

**[2026-03-20 19:06]**
- Initial documentation created
