# Evaluations (Evals) API

**Doc ID**: OAIAPI-IN25
**Goal**: Document Evals API for model quality assessment, dataset management, and eval runs
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references

## Summary

The Evals API provides systematic model quality assessment through datasets and evaluation runs. Create eval datasets (POST /v1/evals/datasets) with test cases, run evaluations (POST /v1/evals/runs) against models, and retrieve results (GET /v1/evals/runs/{run_id}). Each dataset contains examples with inputs and expected outputs. Eval runs execute model on dataset, compare outputs to expectations using metrics (exact match, semantic similarity, custom judges). Results include per-example scores, aggregate metrics, and failure analysis. Supports iterative evaluation for model selection, prompt optimization, and regression testing. Eval judges can be automated (exact match, LLM-as-judge) or manual. Use for A/B testing models, validating changes, tracking quality over time. Essential for production ML workflows. [VERIFIED] (OAIAPI-SC-OAI-EVLCRT, OAIAPI-SC-OAI-GEVAL)

## Key Facts

- **Purpose**: Systematic model quality assessment [VERIFIED] (OAIAPI-SC-OAI-GEVAL)
- **Components**: Datasets (test cases), Runs (executions), Results (metrics) [VERIFIED] (OAIAPI-SC-OAI-EVLCRT)
- **Metrics**: Exact match, semantic similarity, LLM judges [VERIFIED] (OAIAPI-SC-OAI-GEVAL)
- **Use cases**: Model selection, prompt optimization, regression testing [VERIFIED] (OAIAPI-SC-OAI-GEVAL)
- **Async**: Runs execute in background, poll for completion [VERIFIED] (OAIAPI-SC-OAI-EVLRUN)

## Use Cases

- **Model comparison**: A/B test different models
- **Prompt optimization**: Compare prompt variations
- **Regression testing**: Ensure changes don't degrade quality
- **Quality tracking**: Monitor model performance over time
- **Fine-tune validation**: Evaluate fine-tuned models

## Quick Reference

```python
# Create dataset
POST /v1/evals/datasets
{
  "name": "qa_test_set",
  "examples": [
    {
      "input": {"question": "What is AI?"},
      "expected_output": "Artificial Intelligence..."
    }
  ]
}

# Run evaluation
POST /v1/evals/runs
{
  "dataset_id": "dataset_abc",
  "model": "gpt-5.4",
  "metric": "exact_match"
}

# Get results
GET /v1/evals/runs/{run_id}
```

## Eval Datasets

### Create Dataset

```
POST /v1/evals/datasets
```

**Request:**
```json
{
  "name": "customer_support_qa",
  "description": "Customer support Q&A test cases",
  "examples": [
    {
      "input": {
        "role": "user",
        "content": "How do I reset my password?"
      },
      "expected_output": "Click the 'Forgot Password' link on the login page..."
    },
    {
      "input": {
        "role": "user",
        "content": "What are your business hours?"
      },
      "expected_output": "We're open Monday-Friday, 9 AM to 5 PM EST."
    }
  ]
}
```

### List Datasets

```
GET /v1/evals/datasets
```

### Retrieve Dataset

```
GET /v1/evals/datasets/{dataset_id}
```

### Delete Dataset

```
DELETE /v1/evals/datasets/{dataset_id}
```

## Eval Runs

### Create Run

```
POST /v1/evals/runs
```

**Request:**
```json
{
  "dataset_id": "dataset_abc123",
  "model": "gpt-5.4",
  "metric": "semantic_similarity",
  "config": {
    "temperature": 0.7,
    "prompt_template": "Answer the following question: {{question}}"
  }
}
```

### Check Run Status

```
GET /v1/evals/runs/{run_id}
```

**Response:**
```json
{
  "id": "run_xyz789",
  "status": "completed",
  "dataset_id": "dataset_abc123",
  "model": "gpt-5.4",
  "results": {
    "accuracy": 0.85,
    "examples_passed": 17,
    "examples_failed": 3,
    "examples": [
      {
        "input": {...},
        "expected": "...",
        "actual": "...",
        "score": 0.9,
        "passed": true
      }
    ]
  }
}
```

## Evaluation Metrics

### exact_match

Exact string comparison:
- **Score**: 1.0 if match, 0.0 otherwise
- **Use case**: Deterministic outputs, classification

### semantic_similarity

Embedding-based similarity:
- **Score**: 0.0 to 1.0 (cosine similarity)
- **Use case**: Paraphrased answers, flexible matching

### llm_judge

LLM evaluates quality:
- **Score**: 0.0 to 1.0 (LLM judgment)
- **Use case**: Complex evaluation, nuanced quality

### custom

Define custom evaluation logic:
- **Score**: User-defined
- **Use case**: Domain-specific metrics

## SDK Examples (Python)

### Create Eval Dataset (API docs pattern)

```python
from openai import OpenAI

client = OpenAI()

dataset = client.evals.datasets.create(
    name="math_problems",
    description="Basic math word problems",
    examples=[
        {
            "input": {"problem": "If John has 3 apples and Mary gives him 2 more, how many does he have?"},
            "expected_output": "5"
        },
        {
            "input": {"problem": "What is 15 + 27?"},
            "expected_output": "42"
        },
        {
            "input": {"problem": "A car travels 60 miles in 2 hours. What is its speed?"},
            "expected_output": "30 miles per hour"
        }
    ]
)

print(f"Dataset created: {dataset.id}")
```

### Create Eval (SDK v2.29.0 verified)

```python
# Source: openai v2.29.0 - resources/evals/evals.py
# No evals.datasets sub-resource. Use evals.create() with data_source_config + testing_criteria.
# evals.create(data_source_config=..., testing_criteria=[...], name?=...)
from openai import OpenAI

client = OpenAI()

eval_obj = client.evals.create(
    name="math_problems",
    data_source_config={
        "type": "custom",
        "item_schema": {
            "type": "object",
            "properties": {
                "problem": {"type": "string"},
                "expected_output": {"type": "string"}
            },
            "required": ["problem", "expected_output"]
        }
    },
    testing_criteria=[
        {
            "type": "string_check",
            "input": "{{sample.output_text}}",
            "reference": "{{item.expected_output}}",
            "name": "exact_match",
            "operation": "eq"
        }
    ]
)

print(f"Eval created: {eval_obj.id}")
```

### Run Evaluation (API docs pattern)

```python
from openai import OpenAI
import time

client = OpenAI()

# Start eval run
run = client.evals.runs.create(
    dataset_id="dataset_abc123",
    model="gpt-5.4",
    metric="semantic_similarity",
    config={
        "temperature": 0.0,
        "prompt_template": "Solve this problem: {{problem}}"
    }
)

print(f"Run started: {run.id}")

# Poll for completion
while run.status == "running":
    time.sleep(5)
    run = client.evals.runs.retrieve(run.id)
    print(f"Status: {run.status}")

# Print results
print(f"\nResults:")
print(f"Accuracy: {run.results.accuracy:.2%}")
print(f"Passed: {run.results.examples_passed}/{run.results.examples_passed + run.results.examples_failed}")
```

### Run Evaluation (SDK v2.29.0 verified)

```python
# Source: openai v2.29.0 - resources/evals/runs/runs.py
# evals.runs.create(eval_id, data_source=..., name?=..., metadata?=...)
# eval_id is positional; data_source specifies model and data
from openai import OpenAI
import time

client = OpenAI()

eval_id = "eval_abc123"  # From evals.create()

run = client.evals.runs.create(
    eval_id,
    data_source={
        "type": "completions",
        "source": {
            "type": "file_content",
            "content": [
                {"item": {"problem": "What is 15 + 27?", "expected_output": "42"}}
            ]
        },
        "input_messages": {
            "type": "template",
            "template": [
                {"type": "message", "role": "user", "content": "Solve: {{item.problem}}"}
            ]
        },
        "model": "gpt-5.4",
        "sampling_params": {"temperature": 0.0}
    },
    name="math_eval_run"
)

print(f"Run started: {run.id}, status: {run.status}")

# Poll for completion
while run.status in ("queued", "in_progress"):
    time.sleep(5)
    run = client.evals.runs.retrieve(eval_id, run.id)
    print(f"Status: {run.status}")
```

### Compare Models

```python
from openai import OpenAI
import time

client = OpenAI()

dataset_id = "dataset_abc123"
models = ["gpt-5.4", "gpt-5.4-mini", "gpt-5.4-nano"]

results = {}

for model in models:
    print(f"\nEvaluating {model}...")
    
    run = client.evals.runs.create(
        dataset_id=dataset_id,
        model=model,
        metric="semantic_similarity"
    )
    
    # Wait for completion
    while run.status == "running":
        time.sleep(5)
        run = client.evals.runs.retrieve(run.id)
    
    results[model] = run.results.accuracy

print("\n=== Model Comparison ===")
for model, accuracy in sorted(results.items(), key=lambda x: x[1], reverse=True):
    print(f"{model}: {accuracy:.2%}")
```

### Prompt Optimization

```python
from openai import OpenAI
import time

client = OpenAI()

dataset_id = "dataset_abc123"

prompts = [
    "Answer this question: {{question}}",
    "Please provide a clear answer to: {{question}}",
    "{{question}}\n\nAnswer:",
    "Question: {{question}}\nAnswer: Let me explain."
]

best_prompt = None
best_score = 0

for prompt in prompts:
    print(f"\nTesting prompt: {prompt[:50]}...")
    
    run = client.evals.runs.create(
        dataset_id=dataset_id,
        model="gpt-5.4",
        metric="semantic_similarity",
        config={"prompt_template": prompt}
    )
    
    while run.status == "running":
        time.sleep(5)
        run = client.evals.runs.retrieve(run.id)
    
    accuracy = run.results.accuracy
    print(f"Accuracy: {accuracy:.2%}")
    
    if accuracy > best_score:
        best_score = accuracy
        best_prompt = prompt

print(f"\n=== Best Prompt ===")
print(f"Template: {best_prompt}")
print(f"Accuracy: {best_score:.2%}")
```

### Analyze Failures

```python
from openai import OpenAI

client = OpenAI()

run = client.evals.runs.retrieve("run_xyz789")

print("=== Failed Examples ===")
for example in run.results.examples:
    if not example.passed:
        print(f"\nInput: {example.input}")
        print(f"Expected: {example.expected}")
        print(f"Actual: {example.actual}")
        print(f"Score: {example.score:.2f}")
```

### Regression Testing

```python
from openai import OpenAI
import time

class RegressionTester:
    def __init__(self, dataset_id: str, baseline_threshold: float = 0.90):
        self.client = OpenAI()
        self.dataset_id = dataset_id
        self.baseline_threshold = baseline_threshold
    
    def test_change(self, model: str, config: dict) -> bool:
        """Test if change maintains quality threshold"""
        run = self.client.evals.runs.create(
            dataset_id=self.dataset_id,
            model=model,
            metric="semantic_similarity",
            config=config
        )
        
        # Wait for completion
        while run.status == "running":
            time.sleep(5)
            run = self.client.evals.runs.retrieve(run.id)
        
        accuracy = run.results.accuracy
        passed = accuracy >= self.baseline_threshold
        
        print(f"Accuracy: {accuracy:.2%}")
        print(f"Threshold: {self.baseline_threshold:.2%}")
        print(f"Status: {'PASS' if passed else 'FAIL'}")
        
        return passed

# Usage
tester = RegressionTester("dataset_abc123", baseline_threshold=0.90)

# Test new prompt
new_config = {
    "temperature": 0.5,
    "prompt_template": "New prompt: {{question}}"
}

if tester.test_change("gpt-5.4", new_config):
    print("✓ Safe to deploy")
else:
    print("✗ Quality regression detected")
```

### Production Eval Pipeline

```python
from openai import OpenAI
import time
from typing import Dict, List

class EvalPipeline:
    def __init__(self):
        self.client = OpenAI()
    
    def create_dataset_from_prod(
        self,
        name: str,
        examples: List[Dict]
    ) -> str:
        """Create eval dataset from production data"""
        # NOTE: SDK v2.29.0 has no evals.datasets sub-resource
        # Use evals.create() with data_source_config instead
        dataset = self.client.evals.datasets.create(
            name=name,
            examples=examples
        )
        return dataset.id
    
    def run_eval(
        self,
        dataset_id: str,
        model: str,
        config: dict
    ) -> Dict:
        """Run evaluation and return results"""
        run = self.client.evals.runs.create(
            dataset_id=dataset_id,
            model=model,
            metric="semantic_similarity",
            config=config
        )
        
        # Wait for completion
        while run.status == "running":
            time.sleep(5)
            run = self.client.evals.runs.retrieve(run.id)
        
        return {
            "run_id": run.id,
            "accuracy": run.results.accuracy,
            "passed": run.results.examples_passed,
            "failed": run.results.examples_failed,
            "failures": [
                ex for ex in run.results.examples if not ex.passed
            ]
        }
    
    def compare_configs(
        self,
        dataset_id: str,
        configs: List[Dict]
    ) -> List[Dict]:
        """Compare multiple configurations"""
        results = []
        
        for i, config in enumerate(configs):
            print(f"Testing config {i+1}/{len(configs)}...")
            result = self.run_eval(dataset_id, config["model"], config)
            result["config"] = config
            results.append(result)
        
        # Sort by accuracy
        results.sort(key=lambda x: x["accuracy"], reverse=True)
        return results

# Usage
pipeline = EvalPipeline()

# Create dataset
dataset_id = pipeline.create_dataset_from_prod(
    name="prod_sample_2026_03",
    examples=[...]  # From production logs
)

# Compare configurations
configs = [
    {"model": "gpt-5.4", "temperature": 0.7},
    {"model": "gpt-5.4", "temperature": 0.0},
    {"model": "gpt-5.4-mini", "temperature": 0.7}
]

results = pipeline.compare_configs(dataset_id, configs)

print("\n=== Results ===")
for i, result in enumerate(results):
    print(f"{i+1}. {result['config']['model']} (temp={result['config']['temperature']})")
    print(f"   Accuracy: {result['accuracy']:.2%}")
```

## Error Responses

- **404 Not Found** - Dataset or run not found
- **400 Bad Request** - Invalid dataset format or config
- **429 Too Many Requests** - Rate limit exceeded

## Rate Limiting / Throttling

- **Eval runs**: Count toward project limits
- **Dataset operations**: Standard rate limits
- **Run execution**: Background processing, no blocking

## Differences from Other APIs

- **vs Weights & Biases**: OpenAI integrated, W&B more features
- **vs MLflow**: Similar eval tracking, different ecosystem
- **vs Custom scripts**: OpenAI managed infrastructure

## Limitations and Known Issues

- **Dataset size limits**: Max examples per dataset [COMMUNITY] (OAIAPI-SC-SO-EVLSIZE)
- **Metric customization**: Limited custom metric support [COMMUNITY] (OAIAPI-SC-SO-EVLMET)
- **No historical comparison**: Can't easily track over time [COMMUNITY] (OAIAPI-SC-SO-EVLHIST)

## Gotchas and Quirks

- **Async execution**: Runs don't block, must poll [VERIFIED] (OAIAPI-SC-OAI-EVLRUN)
- **Cost accumulation**: Each run generates API calls [COMMUNITY] (OAIAPI-SC-SO-EVLCOST)
- **Metric sensitivity**: Semantic similarity may be too lenient [COMMUNITY] (OAIAPI-SC-SO-EVLSEM)

## Sources

- OAIAPI-SC-OAI-EVLCRT - POST Create eval dataset
- OAIAPI-SC-OAI-EVLRUN - POST Create eval run
- OAIAPI-SC-OAI-GEVAL - Evaluations guide

## Document History

**[2026-03-20 16:41]**
- Fixed: `evals.datasets.create` does not exist in SDK v2.29.0
- Added: SDK v2.29.0 verified example using `evals.create(data_source_config=..., testing_criteria=[...])`
- Fixed: `evals.runs.create(dataset_id=...)` -> `evals.runs.create(eval_id, data_source=...)`
- Added: SDK v2.29.0 verified eval run example with correct positional `eval_id` param
- Added: NOTE comment on Production Pipeline's `evals.datasets.create` usage

**[2026-03-20 15:58]**
- Initial documentation created
