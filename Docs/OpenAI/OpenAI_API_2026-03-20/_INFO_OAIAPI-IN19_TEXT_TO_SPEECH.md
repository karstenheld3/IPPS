# Text-to-Speech (TTS)

**Doc ID**: OAIAPI-IN19
**Goal**: Document TTS API with models, voices, custom voices, and consent management
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references

## Summary

OpenAI TTS API (POST /v1/audio/speech) converts text to spoken audio using neural voices. Two model tiers: tts-1 (faster, lower latency) and tts-1-hd (higher quality, slower). Six preset voices: alloy, echo, fable, onyx, nova, shimmer with distinct characteristics. Custom voices available for eligible accounts via voice consent management workflow - requires recording samples, consent verification, and voice profile creation. Output formats: mp3 (default), opus, aac, flac, wav, pcm. Speed parameter controls playback rate (0.25-4.0). Maximum input 4096 characters per request. Voice profiles support versioning and can be updated. Pricing per character. Real-time capable for streaming applications. [VERIFIED] (OAIAPI-SC-OAI-AUDSPK, OAIAPI-SC-OAI-AUDVOI, OAIAPI-SC-OAI-AUDVCS)

## Key Facts

- **Endpoint**: POST /v1/audio/speech [VERIFIED] (OAIAPI-SC-OAI-AUDSPK)
- **Models**: tts-1 (fast), tts-1-hd (quality) [VERIFIED] (OAIAPI-SC-OAI-AUDSPK)
- **Preset voices**: alloy, echo, fable, onyx, nova, shimmer [VERIFIED] (OAIAPI-SC-OAI-AUDVOI)
- **Custom voices**: Available for eligible accounts [VERIFIED] (OAIAPI-SC-OAI-AUDVCS)
- **Max input**: 4096 characters [VERIFIED] (OAIAPI-SC-OAI-AUDSPK)

## Use Cases

- **Audiobook narration**: Convert books to audio
- **Voice assistants**: Generate spoken responses
- **Accessibility**: Screen readers, navigation
- **Content creation**: Podcast intros, video voiceovers
- **E-learning**: Course narration and explanations

## Quick Reference

```python
POST /v1/audio/speech
{
  "model": "tts-1",
  "input": "Hello, world!",
  "voice": "alloy"
}
```

## Models

### tts-1
- **Latency**: Lower (~real-time capable)
- **Quality**: Good
- **Use case**: Real-time applications, chatbots
- **Cost**: Standard pricing

### tts-1-hd
- **Latency**: Higher
- **Quality**: Higher fidelity
- **Use case**: Audiobooks, high-quality content
- **Cost**: Premium pricing

## Preset Voices

### alloy
- **Characteristics**: Neutral, balanced
- **Use case**: General-purpose applications

### echo
- **Characteristics**: Clear, articulate
- **Use case**: Educational content, instructions

### fable
- **Characteristics**: Warm, storytelling
- **Use case**: Audiobooks, narratives

### onyx
- **Characteristics**: Deep, authoritative
- **Use case**: Announcements, professional content

### nova
- **Characteristics**: Bright, energetic
- **Use case**: Engaging content, marketing

### shimmer
- **Characteristics**: Soft, gentle
- **Use case**: Meditation, calming content

## Custom Voices

### Availability
- **Eligible accounts only** - Contact OpenAI for access
- **Use case**: Brand-specific voices, celebrity voices, personalized assistants

### Voice Consent Workflow

1. **Record samples**: Provide voice recordings (15+ minutes recommended)
2. **Submit consent**: Legal consent form from voice owner
3. **Verification**: OpenAI verifies consent and samples
4. **Profile creation**: Voice profile generated
5. **API access**: Use custom voice ID in API calls

### Voice Profile Management

```python
# Create voice profile
POST /v1/audio/voices

# List voices
GET /v1/audio/voices

# Delete voice
DELETE /v1/audio/voices/{voice_id}
```

## Request Parameters

### Required

- **model**: tts-1 or tts-1-hd
- **input**: Text to convert (max 4096 chars)
- **voice**: Voice ID (preset or custom)

### Optional

- **response_format**: Audio format (mp3, opus, aac, flac, wav, pcm)
- **speed**: Playback speed (0.25-4.0, default: 1.0)

## Response Formats

### mp3 (default)
- **Compression**: Good
- **Quality**: High
- **Compatibility**: Universal
- **Use case**: General audio files

### opus
- **Compression**: Excellent
- **Quality**: Good
- **Streaming**: Optimized
- **Use case**: Real-time streaming

### aac
- **Compression**: Good
- **Quality**: High
- **Compatibility**: Wide
- **Use case**: Mobile applications

### flac
- **Compression**: Lossless
- **Quality**: Highest
- **Size**: Large
- **Use case**: Archival, production

### wav
- **Compression**: None
- **Quality**: Highest
- **Size**: Largest
- **Use case**: Editing, production

### pcm
- **Compression**: None (raw)
- **Quality**: Highest
- **Size**: Largest
- **Use case**: Audio processing

## SDK Examples (Python)

### Basic TTS

```python
from openai import OpenAI

client = OpenAI()

response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input="Hello! This is a test of the text-to-speech system."
)

response.stream_to_file("output.mp3")
```

### High-Quality TTS

```python
from openai import OpenAI

client = OpenAI()

response = client.audio.speech.create(
    model="tts-1-hd",
    voice="fable",
    input="Once upon a time, in a land far away, there lived a brave knight."
)

response.stream_to_file("story.mp3")
```

### With Speed Control

```python
from openai import OpenAI

client = OpenAI()

response = client.audio.speech.create(
    model="tts-1",
    voice="echo",
    input="This audio will play faster than normal.",
    speed=1.5  # 1.5x speed
)

response.stream_to_file("fast_speech.mp3")
```

### Different Output Formats

```python
from openai import OpenAI

client = OpenAI()

# Opus for streaming
response = client.audio.speech.create(
    model="tts-1",
    voice="nova",
    input="Streaming-optimized audio.",
    response_format="opus"
)

response.stream_to_file("stream.opus")

# WAV for editing
response = client.audio.speech.create(
    model="tts-1-hd",
    voice="shimmer",
    input="High-quality uncompressed audio.",
    response_format="wav"
)

response.stream_to_file("edit.wav")
```

### Long Text Chunking

```python
from openai import OpenAI
import os

def text_to_speech_long(text: str, output_file: str, chunk_size: int = 4000):
    """Convert long text to speech by chunking"""
    client = OpenAI()
    
    # Split into chunks
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    
    audio_files = []
    for i, chunk in enumerate(chunks):
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=chunk
        )
        
        chunk_file = f"chunk_{i}.mp3"
        response.stream_to_file(chunk_file)
        audio_files.append(chunk_file)
    
    # Concatenate audio files (requires external tool like ffmpeg)
    # ffmpeg -i "concat:file1.mp3|file2.mp3" -acodec copy output.mp3
    
    return audio_files

# Usage
long_text = "..." * 10000  # Very long text
chunks = text_to_speech_long(long_text, "full_audio.mp3")
```

### Voice Comparison

```python
from openai import OpenAI

client = OpenAI()

text = "Hello, this is a voice comparison test."
voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]

for voice in voices:
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text
    )
    
    response.stream_to_file(f"voice_{voice}.mp3")
    print(f"Generated {voice}.mp3")
```

### Production TTS Service

```python
from openai import OpenAI
from pathlib import Path

class TTSService:
    def __init__(self, model: str = "tts-1", voice: str = "alloy"):
        self.client = OpenAI()
        self.model = model
        self.voice = voice
    
    def generate(
        self,
        text: str,
        output_path: str,
        speed: float = 1.0,
        format: str = "mp3"
    ):
        """Generate TTS audio"""
        if len(text) > 4096:
            raise ValueError("Text exceeds 4096 character limit")
        
        response = self.client.audio.speech.create(
            model=self.model,
            voice=self.voice,
            input=text,
            speed=speed,
            response_format=format
        )
        
        response.stream_to_file(output_path)
        
        file_size = Path(output_path).stat().st_size
        return {
            "path": output_path,
            "size": file_size,
            "format": format,
            "voice": self.voice
        }

# Usage
tts = TTSService(model="tts-1-hd", voice="fable")
result = tts.generate(
    "Welcome to our service!",
    "welcome.mp3",
    speed=1.0,
    format="mp3"
)
print(f"Generated: {result['path']} ({result['size']} bytes)")
```

### Custom Voice (Eligible Accounts)

```python
from openai import OpenAI

client = OpenAI()

# Use custom voice
response = client.audio.speech.create(
    model="tts-1-hd",
    voice="voice_custom_abc123",  # Custom voice ID
    input="This uses a custom voice profile."
)

response.stream_to_file("custom_voice.mp3")
```

## Error Responses

- **400 Bad Request** - Invalid parameters or text too long
- **403 Forbidden** - Custom voice access denied
- **429 Too Many Requests** - Rate limit exceeded

## Rate Limiting / Throttling

- **Character-based pricing**: Charged per character
- **Request limits**: RPM limits apply
- **Concurrent requests**: Limited concurrent TTS generation

## Differences from Other APIs

- **vs Google Text-to-Speech**: OpenAI simpler, Google more voice options
- **vs Amazon Polly**: Similar capabilities, different pricing
- **vs ElevenLabs**: ElevenLabs specializes in voice cloning, OpenAI general-purpose

## Limitations and Known Issues

- **4096 char limit**: Long text must be chunked [VERIFIED] (OAIAPI-SC-OAI-AUDSPK)
- **Custom voices limited**: Only eligible accounts [VERIFIED] (OAIAPI-SC-OAI-AUDVCS)
- **No SSML support**: Cannot control pronunciation, pauses [COMMUNITY] (OAIAPI-SC-SO-SSML)

## Gotchas and Quirks

- **Voice selection matters**: Different voices better for different content [COMMUNITY] (OAIAPI-SC-SO-VOICESEL)
- **Speed affects quality**: Very fast/slow speeds may reduce quality [COMMUNITY] (OAIAPI-SC-SO-SPEED)
- **Format file extension**: Must use correct extension for format [VERIFIED] (OAIAPI-SC-OAI-AUDSPK)

## Sources

- OAIAPI-SC-OAI-AUDSPK - POST Create speech
- OAIAPI-SC-OAI-AUDVOI - Audio voices guide
- OAIAPI-SC-OAI-AUDVCS - Custom voices and consent guide
- OAIAPI-SC-OAI-GAUDIO - Audio guide

## Document History

**[2026-03-20 15:42]**
- Initial documentation created
