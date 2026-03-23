# Image Generation

**Doc ID**: OAIAPI-IN21
**Goal**: Document image generation and editing with DALL-E and gpt-image models
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references

## Summary

OpenAI image generation via POST /v1/images/generations (create), POST /v1/images/edits (edit), POST /v1/images/variations (variations). Models: gpt-image-1.5 (latest, highest quality), gpt-image-1 (standard), dall-e-3, dall-e-2 (legacy). Generate images from text prompts with size options (1024x1024, 1792x1024, 1024x1792 for DALL-E 3/gpt-image; 256x256, 512x512, 1024x1024 for DALL-E 2). Image editing requires mask for inpainting areas to modify. Variations create similar images from source. Quality parameter (standard/hd) for DALL-E 3+. Style parameter (vivid/natural) controls artistic interpretation. Returns base64 or URLs. Max 10 images per request (DALL-E 2 only, others max 1). Prompt rewriting for safety and quality. Supports PNG format output. [VERIFIED] (OAIAPI-SC-OAI-IMGGEN, OAIAPI-SC-OAI-IMGEDT, OAIAPI-SC-OAI-IMGVAR, OAIAPI-SC-OAI-GIMAGE)

## Key Facts

- **Endpoints**: POST /v1/images/generations, /edits, /variations [VERIFIED] (OAIAPI-SC-OAI-IMGGEN)
- **Models**: gpt-image-1.5, gpt-image-1, dall-e-3, dall-e-2 [VERIFIED] (OAIAPI-SC-OAI-GIMAGE)
- **Sizes**: Up to 1792x1024 (DALL-E 3/gpt-image) [VERIFIED] (OAIAPI-SC-OAI-IMGGEN)
- **Quality**: standard, hd (DALL-E 3+ only) [VERIFIED] (OAIAPI-SC-OAI-IMGGEN)
- **Format**: PNG [VERIFIED] (OAIAPI-SC-OAI-IMGGEN)

## Use Cases

- **Creative design**: Marketing visuals, concept art
- **Content creation**: Blog images, social media
- **Product visualization**: Mock-ups, prototypes
- **Education**: Diagrams, illustrations
- **Art generation**: Digital artwork, style exploration

## Quick Reference

```python
# Generate
POST /v1/images/generations
{
  "model": "gpt-image-1.5",
  "prompt": "A cat in space",
  "size": "1024x1024",
  "quality": "hd"
}

# Edit
POST /v1/images/edits
file: image.png
mask: mask.png
prompt: "Add a hat"

# Variations
POST /v1/images/variations
file: image.png
```

## Models

### gpt-image-1.5 (Latest)
- **Quality**: Highest
- **Sizes**: 1024x1024, 1792x1024, 1024x1792
- **Quality options**: standard, hd
- **Style**: vivid, natural
- **Max images**: 1 per request

### gpt-image-1
- **Quality**: High
- **Sizes**: 1024x1024, 1792x1024, 1024x1792
- **Quality options**: standard, hd
- **Style**: vivid, natural
- **Max images**: 1 per request

### DALL-E 3
- **Quality**: High
- **Sizes**: 1024x1024, 1792x1024, 1024x1792
- **Quality options**: standard, hd
- **Style**: vivid, natural
- **Max images**: 1 per request

### DALL-E 2 (Legacy)
- **Quality**: Standard
- **Sizes**: 256x256, 512x512, 1024x1024
- **Quality options**: N/A
- **Style**: N/A
- **Max images**: 10 per request

## Image Generation

### Request Parameters

**Required:**
- **prompt**: Text description (max 4000 chars for gpt-image/DALL-E 3, 1000 for DALL-E 2)
- **model**: Model ID

**Optional:**
- **n**: Number of images (1-10 for DALL-E 2, 1 for others)
- **size**: Image dimensions
- **quality**: "standard" or "hd" (DALL-E 3+ only)
- **style**: "vivid" or "natural" (DALL-E 3+ only)
- **response_format**: "url" or "b64_json"
- **user**: End-user identifier

### Size Options

**gpt-image/DALL-E 3:**
- 1024x1024 (square)
- 1792x1024 (landscape)
- 1024x1792 (portrait)

**DALL-E 2:**
- 256x256
- 512x512
- 1024x1024

### Quality Settings

**standard**: Faster generation, lower cost
**hd**: Higher detail, slower, higher cost

### Style Settings

**vivid**: More creative, dramatic, artistic
**natural**: More realistic, subdued, photographic

## Image Editing

### Endpoint

```
POST /v1/images/edits
```

### Parameters

**Required:**
- **image**: Source PNG image (max 4MB)
- **prompt**: Edit description
- **model**: Model ID

**Optional:**
- **mask**: PNG mask (transparent = edit area)
- **n**: Number of variations
- **size**: Output size
- **response_format**: "url" or "b64_json"

### Masking

- **Transparent pixels**: Areas to edit
- **Opaque pixels**: Areas to preserve
- **Format**: PNG with alpha channel
- **Size**: Must match source image

## Image Variations

### Endpoint

```
POST /v1/images/variations
```

### Parameters

**Required:**
- **image**: Source PNG image (max 4MB)
- **model**: Model ID

**Optional:**
- **n**: Number of variations (1-10 for DALL-E 2)
- **size**: Output size
- **response_format**: "url" or "b64_json"

## Response Format

### URL Response

```json
{
  "created": 1234567890,
  "data": [
    {
      "url": "https://..."
    }
  ]
}
```

URLs expire after 1 hour.

### Base64 Response

```json
{
  "created": 1234567890,
  "data": [
    {
      "b64_json": "iVBORw0KGgo..."
    }
  ]
}
```

## SDK Examples (Python)

### Basic Image Generation

```python
from openai import OpenAI

client = OpenAI()

response = client.images.generate(
    model="gpt-image-1.5",
    prompt="A serene mountain landscape at sunset with snow-capped peaks",
    size="1024x1024",
    quality="standard",
    n=1
)

image_url = response.data[0].url
print(f"Image URL: {image_url}")
```

### High-Quality Generation

```python
from openai import OpenAI

client = OpenAI()

response = client.images.generate(
    model="gpt-image-1.5",
    prompt="A futuristic cityscape with flying cars and neon lights",
    size="1792x1024",
    quality="hd",
    style="vivid"
)

image_url = response.data[0].url
print(f"High-quality image: {image_url}")
```

### Download Generated Image

```python
from openai import OpenAI
import requests

client = OpenAI()

response = client.images.generate(
    model="gpt-image-1.5",
    prompt="A cute robot playing with a kitten",
    size="1024x1024"
)

image_url = response.data[0].url

# Download image
image_data = requests.get(image_url).content
with open("robot_kitten.png", "wb") as f:
    f.write(image_data)

print("Image saved to robot_kitten.png")
```

### Base64 Response

```python
from openai import OpenAI
import base64

client = OpenAI()

response = client.images.generate(
    model="gpt-image-1.5",
    prompt="An abstract geometric pattern in blue and gold",
    size="1024x1024",
    response_format="b64_json"
)

# Decode base64
image_data = base64.b64decode(response.data[0].b64_json)
with open("pattern.png", "wb") as f:
    f.write(image_data)
```

### Image Editing

```python
from openai import OpenAI

client = OpenAI()

response = client.images.edit(
    model="dall-e-2",
    image=open("original.png", "rb"),
    mask=open("mask.png", "rb"),
    prompt="Add a red hat to the person",
    size="1024x1024"
)

edited_url = response.data[0].url
print(f"Edited image: {edited_url}")
```

### Image Variations

```python
from openai import OpenAI

client = OpenAI()

response = client.images.create_variation(
    model="dall-e-2",
    image=open("source.png", "rb"),
    n=3,
    size="1024x1024"
)

for i, image in enumerate(response.data):
    print(f"Variation {i+1}: {image.url}")
```

### Batch Generation (DALL-E 2)

```python
from openai import OpenAI

client = OpenAI()

response = client.images.generate(
    model="dall-e-2",
    prompt="A minimalist logo for a tech startup",
    n=10,  # Generate 10 variations
    size="512x512"
)

for i, image in enumerate(response.data):
    print(f"Logo variation {i+1}: {image.url}")
```

### Production Image Generator

```python
from openai import OpenAI
import requests
from pathlib import Path

class ImageGenerator:
    def __init__(self, model: str = "gpt-image-1.5"):
        self.client = OpenAI()
        self.model = model
    
    def generate(
        self,
        prompt: str,
        size: str = "1024x1024",
        quality: str = "standard",
        style: str = "vivid",
        save_path: str = None
    ) -> str:
        """Generate image and optionally save"""
        response = self.client.images.generate(
            model=self.model,
            prompt=prompt,
            size=size,
            quality=quality,
            style=style
        )
        
        image_url = response.data[0].url
        
        if save_path:
            image_data = requests.get(image_url).content
            Path(save_path).write_bytes(image_data)
            return save_path
        
        return image_url

# Usage
generator = ImageGenerator(model="gpt-image-1.5")
path = generator.generate(
    prompt="A professional headshot of a business person",
    quality="hd",
    save_path="headshot.png"
)
print(f"Saved to: {path}")
```

## Error Responses

- **400 Bad Request** - Invalid prompt or parameters
- **413 Payload Too Large** - Image exceeds 4MB
- **415 Unsupported Media Type** - Invalid image format

## Rate Limiting / Throttling

- **Image limits**: RPM limits per model/tier
- **Cost per image**: Varies by model, size, quality
- **Concurrent requests**: Limited concurrent generation

## Differences from Other APIs

- **vs Midjourney**: OpenAI simpler API, Midjourney more artistic control
- **vs Stable Diffusion**: OpenAI hosted service, SD open-source
- **vs Adobe Firefly**: Similar capabilities, different licensing

## Limitations and Known Issues

- **Prompt rewriting**: DALL-E 3+ rewrites prompts for safety [VERIFIED] (OAIAPI-SC-OAI-IMGGEN)
- **Text in images**: Poor text rendering quality [COMMUNITY] (OAIAPI-SC-SO-IMGTXT)
- **Faces**: Inconsistent facial features across generations [COMMUNITY] (OAIAPI-SC-SO-FACES)

## Gotchas and Quirks

- **URL expiration**: Generated URLs expire after 1 hour [VERIFIED] (OAIAPI-SC-OAI-IMGGEN)
- **Style only DALL-E 3+**: Style parameter ignored for DALL-E 2 [VERIFIED] (OAIAPI-SC-OAI-IMGGEN)
- **PNG only**: Output always PNG regardless of input [VERIFIED] (OAIAPI-SC-OAI-IMGGEN)

## Sources

- OAIAPI-SC-OAI-IMGGEN - POST Create image
- OAIAPI-SC-OAI-IMGEDT - POST Edit image
- OAIAPI-SC-OAI-IMGVAR - POST Create image variation
- OAIAPI-SC-OAI-GIMAGE - Images guide

## Document History

**[2026-03-20 15:48]**
- Initial documentation created
