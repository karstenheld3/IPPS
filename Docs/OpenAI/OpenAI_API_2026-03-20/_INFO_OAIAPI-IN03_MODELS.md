# Models

**Doc ID**: OAIAPI-IN03
**Goal**: Document OpenAI model families, capabilities, pricing, context windows, and deprecations
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references

## Summary

OpenAI provides multiple model families for different use cases: GPT-5.x flagship models (GPT-5.4, GPT-5.4-mini, GPT-5.4-nano) for text generation with up to 1M token context windows, o-series reasoning models (o4-mini, o3-pro) for complex problem-solving, image generation models (gpt-image-1.5, gpt-image-1, DALL-E 2/3), video generation (Sora, sora-2, sora-2-pro), audio models (Whisper, gpt-4o-mini-transcribe for transcription, TTS for speech synthesis), embeddings (text-embedding-3-small/large), and moderation (omni-moderation-latest). GPT-5.4 is the latest flagship with 1M context, $2/1M input tokens, $12/1M output tokens, tools support, and Aug 31 2025 knowledge cutoff. GPT-5.4-mini offers 400K context at $0.75/$4.50 per MTok with reasoning capabilities. Model IDs can be specific snapshots (gpt-4o-2024-08-06) or auto-updating aliases (gpt-4o points to latest). Pricing varies by model tier - flagship models cost more but offer better capabilities. Context windows range from 4K (legacy) to 1M (GPT-5.4). All models accessed via GET /v1/models API. [VERIFIED] (OAIAPI-SC-OAI-GMODLS, OAIAPI-SC-OAI-GPRICE)

## Key Facts

- **Latest flagship**: GPT-5.4 (1M context, $2/$12 per MTok, Aug 2025 cutoff) [VERIFIED] (OAIAPI-SC-OAI-GMODLS)
- **Model families**: GPT-5.x (text), o-series (reasoning), gpt-image (images), Sora (video), Whisper/TTS (audio), embeddings, moderation [VERIFIED] (OAIAPI-SC-OAI-GMODLS)
- **Pricing tiers**: Nano ($0.20-$1.25), Mini ($0.75-$4.50), Standard ($2-$12), Pro (higher) [VERIFIED] (OAIAPI-SC-OAI-GPRICE)
- **Context windows**: 4K-1M tokens depending on model [VERIFIED] (OAIAPI-SC-OAI-GMODLS)
- **Model aliases**: Auto-updating (gpt-4o) vs pinned snapshots (gpt-4o-2024-08-06) [VERIFIED] (OAIAPI-SC-OAI-GMODLS)

## Use Cases

- **Text generation**: GPT-5.4, GPT-5.4-mini for chat, content, code
- **Reasoning tasks**: o4-mini, o3-pro for complex problem-solving
- **Image creation**: gpt-image-1.5 for high-quality images
- **Video generation**: Sora-2 for video content
- **Audio processing**: Whisper for transcription, TTS for speech

## Quick Reference

```
GET /v1/models
GET /v1/models/{model}

Model families:
- GPT-5.x: Text generation (gpt-5.4, gpt-5.4-mini, gpt-5.4-nano)
- o-series: Reasoning (o4-mini, o3-pro, o3-deep-research)
- Image: gpt-image-1.5, gpt-image-1, DALL-E
- Video: Sora, sora-2, sora-2-pro
- Audio: Whisper, gpt-4o-mini-transcribe, TTS
- Embeddings: text-embedding-3-small/large
- Moderation: omni-moderation-latest
```

## Model Families

### GPT-5.x Series (Flagship Text Models)

#### GPT-5.4
- **Context window**: 1M tokens
- **Max output**: 128K tokens
- **Pricing**: $2.00/MTok input, $12.00/MTok output
- **Latency**: Faster
- **Tools**: Functions, Web search, File search, Computer use, MCP
- **Knowledge cutoff**: Aug 31, 2025
- **Use case**: Flagship model for complex tasks requiring large context
- **Model ID**: `gpt-5.4`

#### GPT-5.4 mini
- **Context window**: 400K tokens
- **Max output**: 128K tokens
- **Pricing**: $0.75/MTok input, $4.50/MTok output
- **Latency**: Faster
- **Reasoning**: Supports reasoning effort (none/low/medium/high/xhigh)
- **Tools**: Functions, Web search, File search, Computer use
- **Knowledge cutoff**: Aug 31, 2025
- **Use case**: Strongest mini model for coding, computer use, subagents
- **Model ID**: `gpt-5.4-mini`

#### GPT-5.4 nano
- **Context window**: 400K tokens
- **Max output**: 128K tokens
- **Pricing**: $0.20/MTok input, $1.25/MTok output
- **Latency**: Faster
- **Reasoning**: Supports reasoning effort
- **Tools**: Functions, Web search, File search, MCP
- **Knowledge cutoff**: Aug 31, 2025
- **Use case**: Cheapest GPT-5.4-class model for simple high-volume tasks
- **Model ID**: `gpt-5.4-nano`

### o-Series (Reasoning Models)

#### o4-mini
- **Purpose**: Fast reasoning for everyday tasks
- **Pricing**: Lower than flagship
- **Use case**: General reasoning, coding, math
- **Model ID**: `o4-mini`

#### o3-pro
- **Purpose**: Advanced reasoning for complex problems
- **Pricing**: Premium tier
- **Use case**: Research, complex analysis, hard problem-solving
- **Model ID**: `o3-pro`

#### o3-deep-research
- **Purpose**: Deep research agent with background mode
- **Use case**: Long-running research tasks
- **Model ID**: `o3-deep-research`

### Image Generation Models

#### gpt-image-1.5
- **Purpose**: Primary image generation model
- **Quality**: High-quality images
- **Use case**: Image generation, editing, variations
- **Model ID**: `gpt-image-1.5`

#### gpt-image-1
- **Purpose**: Standard image generation
- **Model ID**: `gpt-image-1`

#### DALL-E 3
- **Status**: Legacy, still supported
- **Model ID**: `dall-e-3`

#### DALL-E 2
- **Status**: Legacy
- **Model ID**: `dall-e-2`

### Video Generation Models

#### sora-2-pro
- **Purpose**: Higher quality, longer generation time
- **Use case**: Professional video content
- **Model ID**: `sora-2-pro`

#### sora-2
- **Purpose**: Standard video generation
- **Model ID**: `sora-2`

#### Sora
- **Purpose**: Original video model
- **Model ID**: `sora`

### Audio Models

#### Whisper
- **Purpose**: Audio transcription and translation
- **Languages**: Multilingual support
- **Model ID**: `whisper-1`

#### gpt-4o-mini-transcribe
- **Purpose**: Fast transcription model
- **Use case**: Lower-cost alternative to Whisper
- **Model ID**: `gpt-4o-mini-transcribe`

#### TTS (Text-to-Speech)
- **Models**: `tts-1`, `tts-1-hd`
- **Voices**: Multiple voice options
- **Custom voices**: Available for eligible accounts

### Embeddings Models

#### text-embedding-3-large
- **Dimensions**: Up to 3072
- **Use case**: High-quality semantic search, clustering
- **Model ID**: `text-embedding-3-large`

#### text-embedding-3-small
- **Dimensions**: Up to 1536
- **Use case**: Cost-effective embeddings
- **Model ID**: `text-embedding-3-small`

#### text-embedding-ada-002
- **Status**: Legacy, still supported
- **Model ID**: `text-embedding-ada-002`

### Moderation Models

#### omni-moderation-latest
- **Purpose**: Multi-modal content moderation
- **Input**: Text and images
- **Model ID**: `omni-moderation-latest`

## Model Aliases vs Snapshots

### Auto-Updating Aliases

Model aliases automatically point to latest version:
- `gpt-4o` → latest GPT-4o snapshot
- `gpt-5.4` → latest GPT-5.4 snapshot
- `o4-mini` → latest o4-mini snapshot

**Behavior**: Model prompting and output may change as snapshots update

### Pinned Snapshots

Specific dated versions for consistent behavior:
- `gpt-4o-2024-08-06`
- `gpt-4o-2024-05-13`
- `gpt-5.4-2025-08-15` (example)

**Recommendation**: Use pinned snapshots for production + implement evals

## Pricing

### Flagship Models (GPT-5.4)
- **Input**: $2.00 per 1M tokens
- **Output**: $12.00 per 1M tokens

### Mini Models (GPT-5.4-mini)
- **Input**: $0.75 per 1M tokens
- **Output**: $4.50 per 1M tokens

### Nano Models (GPT-5.4-nano)
- **Input**: $0.20 per 1M tokens
- **Output**: $1.25 per 1M tokens

### Image Generation
- **gpt-image-1.5**: Higher pricing for quality
- **DALL-E 3**: Standard image pricing
- **DALL-E 2**: Legacy pricing

### Audio
- **Whisper**: Per minute pricing
- **TTS**: Per character pricing

### Embeddings
- **text-embedding-3-large**: Higher cost, better quality
- **text-embedding-3-small**: Lower cost

## Context Windows and Limits

- **GPT-5.4**: 1M input context, 128K max output
- **GPT-5.4-mini/nano**: 400K input context, 128K max output
- **GPT-4o**: 128K context
- **o4-mini**: Large context (specific limit varies)
- **Legacy models**: 4K-16K context

## Knowledge Cutoffs

- **GPT-5.4 series**: August 31, 2025
- **GPT-4o series**: Varies by snapshot
- **o-series**: Current as of model training

## SDK Examples (Python)

### List All Models

```python
from openai import OpenAI

client = OpenAI()

models = client.models.list()
for model in models.data:
    print(f"{model.id}: {model.created}")
```

### Retrieve Model Details

```python
from openai import OpenAI

client = OpenAI()

model = client.models.retrieve("gpt-5.4")
print(f"Model: {model.id}")
print(f"Owner: {model.owned_by}")
```

### Using Specific Model

```python
from openai import OpenAI

client = OpenAI()

# Use auto-updating alias
response = client.chat.completions.create(
    model="gpt-5.4",
    messages=[{"role": "user", "content": "Hello!"}]
)

# Use pinned snapshot for consistency
response = client.chat.completions.create(
    model="gpt-4o-2024-08-06",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### Production Setup with Model Pinning

```python
from openai import OpenAI
import os

client = OpenAI()

# Pin specific snapshot for production
MODEL_ID = "gpt-4o-2024-08-06"

try:
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[{"role": "user", "content": "Hello!"}]
    )
    print(response.choices[0].message.content)
except Exception as e:
    print(f"Error using model {MODEL_ID}: {e}")
```

## Error Responses

- **404 Not Found** - Model does not exist or has been deprecated
- **400 Bad Request** - Invalid model ID format
- **403 Forbidden** - Account lacks access to specified model

## Rate Limiting / Throttling

- **Model-specific limits**: Each model has separate RPM/TPM limits
- **Tier-based**: Usage tier determines limits
- **Project-scoped**: Limits apply per project

## Differences from Other APIs

- **vs Anthropic**: OpenAI has broader model family (image, video, audio); Anthropic focuses on Claude text models
- **vs Gemini**: OpenAI has more specialized models; Gemini has native multimodal models
- **vs Grok**: OpenAI has wider model selection; Grok focuses on text models with X integration

## Limitations and Known Issues

- **Model availability**: Some models restricted by tier or account type [VERIFIED] (OAIAPI-SC-OAI-GMODLS)
- **Snapshot deprecation**: Old snapshots eventually deprecated with advance notice [VERIFIED] (OAIAPI-SC-OAI-GDEPR)
- **Custom voices limited**: TTS custom voices only for eligible accounts [VERIFIED] (OAIAPI-SC-OAI-AUDVOI)

## Gotchas and Quirks

- **Alias behavior changes**: Using `gpt-4o` alias means output may change without warning when new snapshot released [VERIFIED] (OAIAPI-SC-OAI-GMODLS)
- **Context != output**: Max output tokens often much smaller than context window [VERIFIED] (OAIAPI-SC-OAI-GMODLS)
- **Model ID case-sensitive**: Use exact case for model IDs [COMMUNITY] (OAIAPI-SC-SO-MODCASE)

## Sources

- OAIAPI-SC-OAI-MODAPI - Models API reference
- OAIAPI-SC-OAI-GMODLS - Models overview guide
- OAIAPI-SC-OAI-GPRICE - Pricing information
- OAIAPI-SC-OAI-GLATEST - Latest model guide
- OAIAPI-SC-OAI-GDEPR - Deprecations guide

## Document History

**[2026-03-20 14:55]**
- Initial documentation created from developers.openai.com/docs/models
