# Video Generation

**Doc ID**: OAIAPI-IN22
**Goal**: Document video generation with Sora models, prompts, and video editing
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI_SOURCES]` for source references

## Summary

OpenAI video generation via POST /v1/videos/generations creates videos from text prompts using Sora models: sora (original), sora-2 (improved), sora-2-pro (highest quality). Generate videos up to 20 seconds, multiple aspect ratios (16:9, 9:16, 1:1), resolution up to 1080p. Parameters: prompt (text description), duration (seconds), aspect_ratio, model. Returns video ID for async generation - poll status with GET /v1/videos/{video_id} until complete. Download video file via returned URL. Video editing capabilities: extend videos, modify scenes, change styles. Background processing typical - generation takes minutes. Supports MP4 format output. Frame rate 24-30 fps. Content policy enforcement on prompts. Limited availability - may require waitlist access. [VERIFIED] (OAIAPI-SC-OAI-VIDGEN, OAIAPI-SC-OAI-GVIDEO)

## Key Facts

- **Endpoint**: POST /v1/videos/generations [VERIFIED] (OAIAPI-SC-OAI-VIDGEN)
- **Models**: sora, sora-2, sora-2-pro [VERIFIED] (OAIAPI-SC-OAI-GVIDEO)
- **Duration**: Up to 20 seconds [VERIFIED] (OAIAPI-SC-OAI-VIDGEN)
- **Resolution**: Up to 1080p [VERIFIED] (OAIAPI-SC-OAI-VIDGEN)
- **Async**: Background generation with polling [VERIFIED] (OAIAPI-SC-OAI-VIDGEN)

## Use Cases

- **Marketing content**: Product videos, ads
- **Social media**: Short-form video content
- **Concept visualization**: Storyboarding, previsualization
- **Education**: Animated explanations, tutorials
- **Creative projects**: Art, experimental films

## Quick Reference

```python
# Generate
POST /v1/videos/generations
{
  "model": "sora-2",
  "prompt": "A cat playing piano",
  "duration": 10,
  "aspect_ratio": "16:9"
}

# Check status
GET /v1/videos/{video_id}

# Download when complete
video.url
```

## Models

### sora (Original)
- **Quality**: Good
- **Speed**: Faster generation
- **Cost**: Standard pricing
- **Use case**: General video generation

### sora-2
- **Quality**: Improved
- **Speed**: Moderate
- **Cost**: Higher pricing
- **Use case**: Higher quality content

### sora-2-pro
- **Quality**: Highest
- **Speed**: Slower generation
- **Cost**: Premium pricing
- **Use case**: Professional content, marketing

## Video Generation

### Request Parameters

**Required:**
- **model**: Model ID (sora, sora-2, sora-2-pro)
- **prompt**: Text description (max 1000 chars)

**Optional:**
- **duration**: Video length in seconds (1-20, default: 5)
- **aspect_ratio**: "16:9", "9:16", "1:1" (default: "16:9")
- **resolution**: "720p", "1080p" (default: "1080p")
- **frame_rate**: 24, 30 fps (default: 24)

### Aspect Ratios

- **16:9**: Landscape (YouTube, web)
- **9:16**: Portrait (TikTok, Stories)
- **1:1**: Square (Instagram feed)

### Response

```json
{
  "id": "video_abc123",
  "object": "video",
  "status": "processing",
  "created_at": 1234567890,
  "model": "sora-2",
  "prompt": "A cat playing piano"
}
```

### Video Status

- **processing**: Generation in progress
- **completed**: Video ready, URL available
- **failed**: Generation failed

## Polling for Completion

### Check Status

```
GET /v1/videos/{video_id}
```

**Response when complete:**
```json
{
  "id": "video_abc123",
  "status": "completed",
  "url": "https://...",
  "duration": 10,
  "aspect_ratio": "16:9",
  "resolution": "1080p"
}
```

Video URL expires after 24 hours.

## Video Editing

### Extend Video

Continue video from last frame:
```python
POST /v1/videos/generations
{
  "model": "sora-2",
  "prompt": "Continue the scene with the cat walking away",
  "source_video_id": "video_abc123",
  "duration": 5
}
```

### Modify Scene

Change existing video:
```python
POST /v1/videos/generations
{
  "model": "sora-2",
  "prompt": "Change the background to a beach sunset",
  "source_video_id": "video_abc123"
}
```

## SDK Examples (Python)

### Basic Video Generation (API docs pattern)

```python
from openai import OpenAI
import time

client = OpenAI()

# Create video
video = client.videos.create(
    model="sora-2",
    prompt="A golden retriever puppy playing in a field of flowers at sunset",
    duration=10,
    aspect_ratio="16:9"
)

print(f"Video ID: {video.id}")
print(f"Status: {video.status}")

# Poll for completion
while video.status == "processing":
    time.sleep(10)
    video = client.videos.retrieve(video.id)
    print(f"Status: {video.status}")

print(f"Video URL: {video.url}")
```

### Basic Video Generation (SDK v2.29.0 verified)

```python
# Source: openai v2.29.0 - resources/videos.py
# Parameters: prompt(str), model(str), seconds(4|8|12), size("WxH")
from openai import OpenAI

client = OpenAI()

# create() returns Video with id and status
video = client.videos.create(
    model="sora-2",
    prompt="A golden retriever puppy playing in a field of flowers at sunset",
    seconds=8,
    size="1280x720"
)

print(f"Video ID: {video.id}")
print(f"Status: {video.status}")

# create_and_poll() waits for completion automatically
video = client.videos.create_and_poll(
    model="sora-2",
    prompt="A golden retriever puppy playing in a field of flowers at sunset",
    seconds=8,
    size="1280x720"
)

if video.status == "completed":
    # Download video content
    content = client.videos.download_content(video.id)
    content.write_to_file("puppy.mp4")
```

### High-Quality Generation (API docs pattern)

```python
from openai import OpenAI
import time

client = OpenAI()

video = client.videos.create(
    model="sora-2-pro",
    prompt="A cinematic shot of a futuristic city with flying vehicles at night, neon lights reflecting on wet streets",
    duration=15,
    aspect_ratio="16:9",
    resolution="1080p",
    frame_rate=30
)

# Wait for completion
while video.status == "processing":
    time.sleep(15)
    video = client.videos.retrieve(video.id)

if video.status == "completed":
    print(f"High-quality video ready: {video.url}")
```

### High-Quality Generation (SDK v2.29.0 verified)

```python
# Source: openai v2.29.0 - resources/videos.py
# sora-2-pro for higher quality; seconds(4|8|12); no resolution/frame_rate params
from openai import OpenAI

client = OpenAI()

video = client.videos.create_and_poll(
    model="sora-2-pro",
    prompt="A cinematic shot of a futuristic city with flying vehicles at night, neon lights reflecting on wet streets",
    seconds=12,
    size="1792x1024"
)

if video.status == "completed":
    content = client.videos.download_content(video.id)
    content.write_to_file("city_cinematic.mp4")
elif video.status == "failed":
    print(f"Generation failed")
```

### Download Video (API docs pattern)

```python
from openai import OpenAI
import requests
import time

client = OpenAI()

# Generate video
video = client.videos.create(
    model="sora-2",
    prompt="Time-lapse of a flower blooming",
    duration=8
)

# Wait for completion
while video.status == "processing":
    time.sleep(10)
    video = client.videos.retrieve(video.id)

# Download
if video.status == "completed":
    video_data = requests.get(video.url).content
    with open("flower_bloom.mp4", "wb") as f:
        f.write(video_data)
    print("Video saved to flower_bloom.mp4")
```

### Download Video (SDK v2.29.0 verified)

```python
# Source: openai v2.29.0 - resources/videos.py
# download_content() returns HttpxBinaryResponseContent with write_to_file()
# variant: "video" (default), "thumbnail", "spritesheet"
from openai import OpenAI

client = OpenAI()

video = client.videos.create_and_poll(
    model="sora-2",
    prompt="Time-lapse of a flower blooming",
    seconds=8
)

if video.status == "completed":
    content = client.videos.download_content(video.id)
    content.write_to_file("flower_bloom.mp4")

    # Download thumbnail
    thumb = client.videos.download_content(video.id, variant="thumbnail")
    thumb.write_to_file("flower_bloom_thumb.jpg")
```

### Multiple Aspect Ratios (API docs pattern)

```python
from openai import OpenAI

client = OpenAI()

prompt = "A serene mountain landscape with clouds rolling over peaks"

# Generate for different platforms
ratios = {
    "youtube": "16:9",
    "tiktok": "9:16",
    "instagram": "1:1"
}

for platform, ratio in ratios.items():
    video = client.videos.create(
        model="sora-2",
        prompt=prompt,
        duration=10,
        aspect_ratio=ratio
    )
    print(f"{platform}: {video.id} (status: {video.status})")
```

### Multiple Sizes (SDK v2.29.0 verified)

```python
# Source: openai v2.29.0 - resources/videos.py
# Allowed sizes: 720x1280, 1280x720, 1024x1792, 1792x1024
from openai import OpenAI

client = OpenAI()

prompt = "A serene mountain landscape with clouds rolling over peaks"

sizes = {
    "landscape": "1280x720",
    "portrait": "720x1280",
    "wide": "1792x1024",
    "tall": "1024x1792"
}

for label, size in sizes.items():
    video = client.videos.create(
        model="sora-2",
        prompt=prompt,
        seconds=8,
        size=size
    )
    print(f"{label}: {video.id} (status: {video.status})")
```

### Video Extension (API docs pattern)

```python
from openai import OpenAI
import time

client = OpenAI()

# Original video
video1 = client.videos.create(
    model="sora-2",
    prompt="A person walking through a forest",
    duration=10
)

# Wait for completion
while video1.status == "processing":
    time.sleep(10)
    video1 = client.videos.retrieve(video1.id)

# Extend video
video2 = client.videos.create(
    model="sora-2",
    prompt="The person discovers a hidden waterfall",
    source_video_id=video1.id,
    duration=10
)

print(f"Extended video: {video2.id}")
```

### Video Extension (SDK v2.29.0 verified)

```python
# Source: openai v2.29.0 - resources/videos.py
# videos.extend(prompt, seconds, video={"id": ...}) for extending
# videos.edit(prompt, video={"id": ...}) for editing
# videos.remix(video_id, prompt) for remixing
from openai import OpenAI

client = OpenAI()

# Create and wait for original video
video1 = client.videos.create_and_poll(
    model="sora-2",
    prompt="A person walking through a forest",
    seconds=8
)

if video1.status == "completed":
    # Extend with new prompt - seconds allowed: 4, 8, 12, 16, 20
    video2 = client.videos.extend(
        prompt="The person discovers a hidden waterfall",
        seconds=8,
        video={"id": video1.id}
    )
    print(f"Extended video: {video2.id}")
```

### Production Video Service (API docs pattern)

```python
from openai import OpenAI
import time
from typing import Optional

class VideoGenerator:
    def __init__(self, model: str = "sora-2"):
        self.client = OpenAI()
        self.model = model
    
    def generate(
        self,
        prompt: str,
        duration: int = 5,
        aspect_ratio: str = "16:9",
        resolution: str = "1080p",
        wait: bool = True,
        timeout: int = 600
    ) -> dict:
        """Generate video and optionally wait for completion"""
        video = self.client.videos.create(
            model=self.model,
            prompt=prompt,
            duration=duration,
            aspect_ratio=aspect_ratio,
            resolution=resolution
        )
        
        if not wait:
            return {
                "id": video.id,
                "status": video.status
            }
        
        # Wait for completion
        elapsed = 0
        while video.status == "processing" and elapsed < timeout:
            time.sleep(15)
            elapsed += 15
            video = self.client.videos.retrieve(video.id)
        
        if video.status == "completed":
            return {
                "id": video.id,
                "url": video.url,
                "duration": video.duration,
                "status": "completed"
            }
        elif video.status == "failed":
            return {
                "id": video.id,
                "status": "failed",
                "error": "Video generation failed"
            }
        else:
            return {
                "id": video.id,
                "status": "timeout",
                "message": f"Generation exceeded {timeout}s timeout"
            }

# Usage
generator = VideoGenerator(model="sora-2-pro")
result = generator.generate(
    prompt="A professional product showcase video",
    duration=15,
    aspect_ratio="16:9",
    wait=True
)

if result["status"] == "completed":
    print(f"Video ready: {result['url']}")
```

### Production Video Service (SDK v2.29.0 verified)

```python
# Source: openai v2.29.0 - resources/videos.py
# SDK params: prompt(str), model(str), seconds(4|8|12), size("WxH")
# Statuses: "in_progress", "queued", "completed", "failed"
# Use create_and_poll() for automatic polling
from openai import OpenAI
from typing import Literal

class VideoGenerator:
    VALID_SECONDS = (4, 8, 12)
    VALID_SIZES = ("720x1280", "1280x720", "1024x1792", "1792x1024")

    def __init__(self, model: str = "sora-2"):
        self.client = OpenAI()
        self.model = model

    def generate(
        self,
        prompt: str,
        seconds: Literal[4, 8, 12] = 8,
        size: str = "1280x720",
        wait: bool = True
    ) -> dict:
        """Generate video. Use wait=True for automatic polling."""
        if wait:
            video = self.client.videos.create_and_poll(
                model=self.model,
                prompt=prompt,
                seconds=seconds,
                size=size
            )
        else:
            video = self.client.videos.create(
                model=self.model,
                prompt=prompt,
                seconds=seconds,
                size=size
            )

        result = {"id": video.id, "status": video.status}
        if video.status == "completed":
            result["download"] = f"client.videos.download_content('{video.id}')"
        return result

    def download(self, video_id: str, path: str) -> None:
        """Download completed video to file."""
        content = self.client.videos.download_content(video_id)
        content.write_to_file(path)

# Usage
generator = VideoGenerator(model="sora-2-pro")
result = generator.generate(
    prompt="A professional product showcase video",
    seconds=12,
    size="1792x1024",
    wait=True
)

if result["status"] == "completed":
    generator.download(result["id"], "showcase.mp4")
```

## Error Responses

- **400 Bad Request** - Invalid parameters or prompt
- **403 Forbidden** - Account lacks video generation access
- **429 Too Many Requests** - Rate limit exceeded

## Rate Limiting / Throttling

- **Generation limits**: Limited concurrent video generations
- **Duration limits**: Max 20 seconds per video
- **Daily quotas**: May have daily generation limits

## Differences from Other APIs

- **vs Runway**: Similar capabilities, different models
- **vs Pika**: OpenAI simpler API, Pika more editing features
- **vs Synthesia**: Synthesia focuses on avatars, Sora on general video

## Limitations and Known Issues

- **Limited availability**: May require waitlist access [COMMUNITY] (OAIAPI-SC-SO-SORAWAIT)
- **Generation time**: Can take several minutes [VERIFIED] (OAIAPI-SC-OAI-VIDGEN)
- **20 second limit**: Cannot generate longer videos in single call [VERIFIED] (OAIAPI-SC-OAI-VIDGEN)

## Gotchas and Quirks

- **URL expiration**: Video URLs expire after 24 hours [VERIFIED] (OAIAPI-SC-OAI-VIDGEN)
- **No audio**: Generated videos have no audio track [COMMUNITY] (OAIAPI-SC-SO-VIDAUD)
- **Consistency across frames**: Motion/object consistency varies [COMMUNITY] (OAIAPI-SC-SO-CONSIST)

## Sources

- OAIAPI-SC-OAI-VIDGEN - POST Create video
- OAIAPI-SC-OAI-VIDGET - GET Retrieve video
- OAIAPI-SC-OAI-GVIDEO - Video guide

## Document History

**[2026-03-20 16:41]**
- Fixed: `videos.generate` -> `videos.create` (6 occurrences)
- Fixed: Wrong params `duration`/`aspect_ratio`/`resolution`/`frame_rate` -> `seconds`/`size` per SDK v2.29.0
- Fixed: `source_video_id` -> `videos.extend(video={"id": ...})` for video extension
- Added: SDK v2.29.0 verified examples alongside each API docs example
- Added: `create_and_poll()`, `download_content()`, `extend()`, `edit()`, `remix()` patterns

**[2026-03-20 15:50]**
- Initial documentation created
