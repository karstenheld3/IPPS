# Graders API

**Doc ID**: OAIAPI-IN31
**Goal**: Document the Graders API - run, validate grader definitions for evaluations and fine-tuning
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references
- `_INFO_OAIAPI-IN30_REINFORCEMENT_FINE_TUNING.md [OAIAPI-IN30]` for RFT context

## Summary

The Graders API **[ALPHA]** provides endpoints to run and validate grader definitions used in evaluations and reinforcement fine-tuning. Graders are automated evaluation functions that score model outputs against defined criteria. Two endpoints: POST /v1/graders/run (execute a grader against input data) and POST /v1/graders/validate (check grader definition for errors without executing). Grader types: score graders (numeric 0-1 output), label graders (categorical pass/fail), and custom graders (user-defined logic). Graders can use LLM-as-judge patterns (another model evaluates the output), string matching, regex patterns, or custom code. Used in two contexts: (1) evaluations - measure model performance on test sets, and (2) reinforcement fine-tuning - provide reward signals during training. Grader definitions include the evaluation criteria, scoring rubric, and pass/fail thresholds. Alpha status means the API surface may change without notice. [VERIFIED] (OAIAPI-SC-OAI-FTGRAD)

## Key Facts

- **Status**: ALPHA - API may change [VERIFIED] (OAIAPI-SC-OAI-FTGRAD)
- **Endpoints**: Run (execute) and Validate (check definition) [VERIFIED] (OAIAPI-SC-OAI-FTGRAD)
- **Types**: Score (numeric), Label (categorical), Custom [VERIFIED] (OAIAPI-SC-OAI-FTGRAD)
- **Contexts**: Evaluations and reinforcement fine-tuning [VERIFIED] (OAIAPI-SC-OAI-FTGRAD)
- **LLM-as-judge**: Use another model to evaluate outputs [VERIFIED] (OAIAPI-SC-OAI-FTGRAD)

## Quick Reference

```
POST /v1/graders/run       # Execute grader on input
POST /v1/graders/validate  # Validate grader definition

Headers:
  Authorization: Bearer $OPENAI_API_KEY
  Content-Type: application/json
```

## Grader Types

### Score Grader

Returns a numeric score between 0 and 1:

```json
{
  "type": "score",
  "name": "accuracy_check",
  "model": "gpt-5.4",
  "input": "Rate the factual accuracy of the response from 0 (completely wrong) to 1 (completely correct). Consider: {{criteria}}",
  "pass_threshold": 0.7
}
```

### Label Grader

Returns a categorical label:

```json
{
  "type": "label",
  "name": "safety_check",
  "model": "gpt-5.4",
  "input": "Is this response safe and appropriate? Reply with 'pass' or 'fail'.",
  "labels": ["pass", "fail"],
  "pass_label": "pass"
}
```

### String Match Grader

Simple pattern matching without LLM:

```json
{
  "type": "string_match",
  "name": "exact_answer",
  "expected": "42",
  "case_sensitive": false
}
```

## SDK Examples (Python)

### Run a Grader

```python
from openai import OpenAI

client = OpenAI()

# Define and run a score grader
result = client.graders.run(
    grader={
        "type": "score",
        "name": "helpfulness",
        "model": "gpt-5.4",
        "input": "Rate the helpfulness of this assistant response from 0 to 1. Consider: clarity, completeness, actionability."
    },
    model_input="How do I reset my password?",
    model_output="Click 'Forgot Password' on the login page, enter your email, and follow the reset link sent to your inbox. The link expires in 24 hours."
)

print(f"Score: {result.score}")
print(f"Passed: {result.passed}")
```

### Run a Grader (SDK v2.29.0 verified)

```python
# Source: openai v2.29.0 - resources/fine_tuning/alpha/graders.py
# SDK path: client.fine_tuning.alpha.graders.run (not client.graders.run)
# Params: grader=..., model_sample=... (not model_input/model_output)
from openai import OpenAI

client = OpenAI()

result = client.fine_tuning.alpha.graders.run(
    grader={
        "type": "score",
        "name": "helpfulness",
        "model": "gpt-4.1",
        "input": "Rate the helpfulness of this assistant response from 0 to 1."
    },
    model_sample="Click 'Forgot Password' on the login page, enter your email, and follow the reset link."
)

print(f"Score: {result.score}")
print(f"Passed: {result.passed}")
```

### Validate Grader Definition

```python
from openai import OpenAI

client = OpenAI()

# Validate before using in fine-tuning
validation = client.graders.validate(
    grader={
        "type": "score",
        "name": "code_quality",
        "model": "gpt-5.4",
        "input": "Evaluate Python code quality: readability, correctness, efficiency. Score 0-1.",
        "pass_threshold": 0.8
    }
)

if validation.valid:
    print("Grader definition is valid")
else:
    print(f"Errors: {validation.errors}")
```

### Validate Grader Definition (SDK v2.29.0 verified)

```python
# Source: openai v2.29.0 - resources/fine_tuning/alpha/graders.py
# SDK path: client.fine_tuning.alpha.graders.validate
from openai import OpenAI

client = OpenAI()

validation = client.fine_tuning.alpha.graders.validate(
    grader={
        "type": "score",
        "name": "code_quality",
        "model": "gpt-4.1",
        "input": "Evaluate Python code quality. Score 0-1.",
        "pass_threshold": 0.8
    }
)

if validation.valid:
    print("Grader definition is valid")
else:
    print(f"Errors: {validation.errors}")
```

### Batch Evaluation with Grader

```python
from openai import OpenAI

client = OpenAI()

grader_def = {
    "type": "score",
    "name": "response_quality",
    "model": "gpt-5.4",
    "input": "Rate overall response quality (accuracy, helpfulness, tone) from 0 to 1.",
    "pass_threshold": 0.7
}

test_cases = [
    {"input": "What is Python?", "output": "Python is a programming language."},
    {"input": "Explain REST APIs", "output": "REST is an architectural style for web services using HTTP methods."},
    {"input": "What is 2+2?", "output": "The answer is 4."}
]

scores = []
for tc in test_cases:
    result = client.graders.run(
        grader=grader_def,
        model_input=tc["input"],
        model_output=tc["output"]
    )
    scores.append(result.score)
    print(f"  [{tc['input'][:30]}] Score: {result.score:.2f} Pass: {result.passed}")

avg_score = sum(scores) / len(scores)
pass_rate = sum(1 for s in scores if s >= 0.7) / len(scores)
print(f"Average score: {avg_score:.2f}, Pass rate: {pass_rate:.0%}")
```

## Error Responses

- **400 Bad Request** - Invalid grader definition
- **401 Unauthorized** - Invalid API key
- **422 Unprocessable Entity** - Grader validation failed

## Differences from Other APIs

- **vs Anthropic**: No grader/evaluation API
- **vs Gemini**: Google has evaluation tools in Vertex AI but different API surface
- **vs OpenAI Evals**: Graders are lower-level primitives used within the Evals framework

## Limitations and Known Issues

- **Alpha status**: API surface may change without notice [VERIFIED] (OAIAPI-SC-OAI-FTGRAD)
- **LLM grader cost**: Each grader run using an LLM model consumes tokens [VERIFIED] (OAIAPI-SC-OAI-FTGRAD)
- **Determinism**: LLM-based graders may produce slightly different scores on same input [ASSUMED]

## Sources

- OAIAPI-SC-OAI-FTGRAD - Graders API Reference

## Document History

**[2026-03-21 09:40]**
- Added: SDK v2.29.0 verified companions (client.fine_tuning.alpha.graders.*, model_sample param)

**[2026-03-20 19:08]**
- Initial documentation created
