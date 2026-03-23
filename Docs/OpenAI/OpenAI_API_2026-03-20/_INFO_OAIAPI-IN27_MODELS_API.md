# Models API

**Doc ID**: OAIAPI-IN27
**Goal**: Document the Models API - list, retrieve, and delete models
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references

## Summary

The Models API provides endpoints to list available models, retrieve model details, and delete fine-tuned models. GET /v1/models returns all models accessible to the organization including base models and fine-tuned variants. GET /v1/models/{model} returns details for a specific model: id, object type, created timestamp, and owned_by. DELETE /v1/models/{model} deletes a fine-tuned model (only fine-tuned models can be deleted; base models cannot). Model IDs follow patterns: base models use descriptive names (gpt-5.4, o3, gpt-4.1-mini), dated snapshots use date suffixes (gpt-4o-2024-08-06), and fine-tuned models use the `ft:` prefix (ft:gpt-4.1:org:name:id). The list endpoint does not support pagination - it returns all models at once. Model availability depends on organization tier and permissions. [VERIFIED] (OAIAPI-SC-OAI-MODAPI)

## Key Facts

- **List**: GET /v1/models - all accessible models [VERIFIED] (OAIAPI-SC-OAI-MODAPI)
- **Retrieve**: GET /v1/models/{model} - model details [VERIFIED] (OAIAPI-SC-OAI-MODAPI)
- **Delete**: DELETE /v1/models/{model} - fine-tuned models only [VERIFIED] (OAIAPI-SC-OAI-MODAPI)
- **No pagination**: List returns all models at once [VERIFIED] (OAIAPI-SC-OAI-MODAPI)
- **Fine-tune prefix**: `ft:` prefix for fine-tuned models [VERIFIED] (OAIAPI-SC-OAI-MODAPI)

## Quick Reference

```
GET    /v1/models              # List all models
GET    /v1/models/{model}      # Retrieve model details
DELETE /v1/models/{model}      # Delete fine-tuned model

Headers:
  Authorization: Bearer $OPENAI_API_KEY
```

## Model Object

```json
{
  "id": "gpt-5.4",
  "object": "model",
  "created": 1686935002,
  "owned_by": "openai"
}
```

## Model ID Patterns

- **Base models**: `gpt-5.4`, `o3`, `gpt-4.1-mini`, `gpt-4.1-nano`
- **Dated snapshots**: `gpt-4o-2024-08-06`, `o3-2025-04-16`
- **Fine-tuned**: `ft:gpt-4.1:my-org:custom-name:abc123`
- **Realtime**: `gpt-realtime-1.5`
- **Image**: `gpt-image-1`, `gpt-image-1.5`
- **Embedding**: `text-embedding-3-small`, `text-embedding-3-large`
- **TTS**: `gpt-4o-mini-tts`
- **Transcription**: `gpt-4o-mini-transcribe`, `whisper-1`
- **Moderation**: `omni-moderation-latest`

## SDK Examples (Python)

### List and Filter Models

```python
from openai import OpenAI

client = OpenAI()

# List all models
models = client.models.list()

# Filter by category
base_models = [m for m in models if not m.id.startswith("ft:")]
fine_tuned = [m for m in models if m.id.startswith("ft:")]
gpt_models = [m for m in models if "gpt" in m.id]

print(f"Total: {len(list(models))}")
print(f"Fine-tuned: {len(fine_tuned)}")

for m in sorted(gpt_models, key=lambda x: x.id):
    print(f"  {m.id} (owned by: {m.owned_by})")
```

### Delete Fine-Tuned Model

```python
from openai import OpenAI

client = OpenAI()

model_id = "ft:gpt-4.1:my-org:custom-name:abc123"

try:
    result = client.models.delete(model_id)
    print(f"Deleted: {result.id}, Status: {result.deleted}")
except Exception as e:
    print(f"Error: {e}")
```

## Error Responses

- **401 Unauthorized** - Invalid API key
- **404 Not Found** - Model not found or not accessible
- **403 Forbidden** - Cannot delete base models

## Differences from Other APIs

- **vs Anthropic**: No models list endpoint; model IDs are documented
- **vs Gemini**: `models.list()` and `models.get()` with more metadata (token limits, capabilities)
- **vs Grok**: Uses OpenAI-compatible models endpoint

## Sources

- OAIAPI-SC-OAI-MODAPI - Models API Reference

## Document History

**[2026-03-20 19:04]**
- Initial documentation created
