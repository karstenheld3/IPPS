# Image Streaming

**Doc ID**: OAIAPI-IN22
**Goal**: Document SSE streaming for image generation and editing - partial image events, progressive rendering
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references

## Summary

Image streaming delivers image generation results incrementally via Server-Sent Events (SSE). When `stream: true` is set on image generation or editing requests, the API sends partial image data as the image is being generated, enabling progressive rendering in the UI. Streaming reduces perceived latency for image generation which can take several seconds. Partial image events contain base64-encoded image fragments at increasing quality/resolution. The stream culminates in a final event with the complete image. Compatible with gpt-image-1 and gpt-image-1.5 models. The Responses API also supports image streaming when using the `image_generation` tool with streaming enabled. Streaming image events follow a similar pattern to text streaming: incremental deltas building toward a complete result. [VERIFIED] (OAIAPI-SC-OAI-IMGSTR)

## Key Facts

- **Enable**: `stream: true` on image generation/editing requests [VERIFIED] (OAIAPI-SC-OAI-IMGSTR)
- **Protocol**: Server-Sent Events (SSE) [VERIFIED] (OAIAPI-SC-OAI-IMGSTR)
- **Progressive**: Partial images at increasing quality [VERIFIED] (OAIAPI-SC-OAI-IMGSTR)
- **Models**: gpt-image-1, gpt-image-1.5 [VERIFIED] (OAIAPI-SC-OAI-IMGSTR)
- **Responses API**: Streaming with image_generation tool [VERIFIED] (OAIAPI-SC-OAI-IMGSTR)

## Use Cases

- **Progressive rendering**: Show low-quality preview while generating
- **Perceived latency**: User sees progress instead of waiting
- **Interactive editors**: Update canvas as image generates
- **Thumbnails first**: Show preview, then full resolution

## SDK Examples (Python)

### Stream Image Generation

```python
from openai import OpenAI

client = OpenAI()

stream = client.images.generate(
    model="gpt-image-1",
    prompt="A serene mountain landscape at sunset with a lake reflection",
    size="1024x1024",
    stream=True
)

for event in stream:
    if event.type == "image.partial":
        # Progressive image data (base64)
        partial_b64 = event.data
        # Render partial image in UI
        print(f"Partial: {len(partial_b64)} bytes")
    elif event.type == "image.done":
        # Final complete image
        final_b64 = event.data
        print(f"Complete: {len(final_b64)} bytes")
```

### Stream via Responses API

```python
from openai import OpenAI

client = OpenAI()

stream = client.responses.create(
    model="gpt-5.4",
    tools=[{"type": "image_generation"}],
    input="Generate an image of a futuristic city skyline",
    stream=True
)

for event in stream:
    if event.type == "response.image_generation.partial":
        print(f"Generating... {event.partial_image_index}")
    elif event.type == "response.image_generation.done":
        # Save final image
        import base64
        img_bytes = base64.b64decode(event.result)
        with open("city.png", "wb") as f:
            f.write(img_bytes)
        print("Image saved")
```

## Error Responses

- **400 Bad Request** - Invalid prompt or parameters
- **429 Too Many Requests** - Rate limit exceeded
- **SSE error event** - Generation failed mid-stream

## Differences from Other APIs

- **vs Anthropic**: No image generation or streaming
- **vs Gemini Imagen**: Gemini supports image generation but streaming details differ
- **vs DALL-E 3 (non-streaming)**: Streaming adds progressive rendering; non-streaming waits for complete image

## Limitations and Known Issues

- **Partial quality**: Early partial images are low resolution/quality [VERIFIED] (OAIAPI-SC-OAI-IMGSTR)
- **Stream interruption**: If connection drops, partial data is lost [ASSUMED]

## Sources

- OAIAPI-SC-OAI-IMGSTR - Image Streaming Reference

## Document History

**[2026-03-20 19:00]**
- Initial documentation created
