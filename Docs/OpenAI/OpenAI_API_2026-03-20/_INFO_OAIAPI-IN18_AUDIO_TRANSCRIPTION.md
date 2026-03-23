# Audio Transcription

**Doc ID**: OAIAPI-IN18
**Goal**: Document audio transcription and translation APIs with Whisper and gpt-4o-mini-transcribe models
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references

## Summary

OpenAI provides audio transcription via POST /v1/audio/transcriptions (speech-to-text) and POST /v1/audio/translations (speech-to-English). Two models available: Whisper (whisper-1, multilingual, high accuracy) and gpt-4o-mini-transcribe (faster, lower cost alternative). Transcriptions support multiple audio formats (mp3, mp4, mpeg, mpga, m4a, wav, webm), optional timestamps, prompt for context, language specification, and response formats (json, text, srt, verbose_json, vtt). Translations convert non-English audio to English text. Maximum file size 25MB. API processes audio server-side, returns text transcription. Temperature parameter controls randomness. Timestamps available in verbose_json and vtt formats. [VERIFIED] (OAIAPI-SC-OAI-AUDTRN, OAIAPI-SC-OAI-AUDTRL)

## Key Facts

- **Endpoints**: POST /v1/audio/transcriptions, POST /v1/audio/translations [VERIFIED] (OAIAPI-SC-OAI-AUDTRN)
- **Models**: whisper-1, gpt-4o-mini-transcribe [VERIFIED] (OAIAPI-SC-OAI-GAUDIO)
- **Formats**: mp3, mp4, mpeg, mpga, m4a, wav, webm [VERIFIED] (OAIAPI-SC-OAI-AUDTRN)
- **Max file size**: 25MB [VERIFIED] (OAIAPI-SC-OAI-AUDTRN)
- **Languages**: 50+ languages (Whisper), English only (translations) [VERIFIED] (OAIAPI-SC-OAI-AUDTRN)

## Use Cases

- **Meeting transcription**: Convert recorded meetings to text
- **Podcast transcription**: Generate show notes and transcripts
- **Video subtitles**: Create subtitles from video audio
- **Voice notes**: Convert voice memos to text
- **Multilingual content**: Translate foreign audio to English

## Quick Reference

```python
# Transcription
POST /v1/audio/transcriptions
file: audio.mp3
model: whisper-1

# Translation
POST /v1/audio/translations
file: audio.mp3
model: whisper-1
```

## Transcription API

### Endpoint

```
POST /v1/audio/transcriptions
```

### Parameters

**Required:**
- **file**: Audio file (multipart/form-data)
- **model**: Model ID (whisper-1 or gpt-4o-mini-transcribe)

**Optional:**
- **language**: ISO-639-1 code (e.g., "en", "fr", "de")
- **prompt**: Context for better accuracy
- **response_format**: Output format (json, text, srt, verbose_json, vtt)
- **temperature**: Sampling temperature (0-1)
- **timestamp_granularities**: ["word"] or ["segment"] for timestamps

### Response Formats

**json** (default):
```json
{
  "text": "Hello, how are you?"
}
```

**text**:
```
Hello, how are you?
```

**srt** (SubRip subtitles):
```
1
00:00:00,000 --> 00:00:02,000
Hello, how are you?
```

**verbose_json**:
```json
{
  "task": "transcribe",
  "language": "english",
  "duration": 2.5,
  "text": "Hello, how are you?",
  "segments": [
    {
      "id": 0,
      "seek": 0,
      "start": 0.0,
      "end": 2.0,
      "text": "Hello, how are you?",
      "tokens": [50364, 2425, 11, 577, 366, 291, 30, 50464],
      "temperature": 0.0,
      "avg_logprob": -0.3,
      "compression_ratio": 1.2,
      "no_speech_prob": 0.01
    }
  ]
}
```

**vtt** (WebVTT subtitles):
```
WEBVTT

00:00:00.000 --> 00:00:02.000
Hello, how are you?
```

## Translation API

### Endpoint

```
POST /v1/audio/translations
```

Translates audio to English regardless of input language.

### Parameters

Same as transcription except:
- **No language parameter** (always translates to English)
- **Input**: Any supported language
- **Output**: English text only

## Supported Audio Formats

- **mp3**: MPEG audio
- **mp4**: MPEG-4 audio
- **mpeg**: MPEG audio
- **mpga**: MPEG audio
- **m4a**: Apple audio
- **wav**: Waveform audio
- **webm**: WebM audio

## Supported Languages

**Whisper supports 50+ languages:**
English, Spanish, French, German, Italian, Portuguese, Dutch, Russian, Arabic, Chinese, Japanese, Korean, Hindi, Turkish, Vietnamese, Polish, Ukrainian, Czech, Romanian, Greek, Swedish, Danish, Norwegian, Finnish, Thai, Indonesian, Malay, Filipino, Hebrew, Persian, Bengali, Tamil, Telugu, Urdu, Swahili, and more.

## SDK Examples (Python)

### Basic Transcription

```python
from openai import OpenAI

client = OpenAI()

with open("audio.mp3", "rb") as audio_file:
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )

print(transcription.text)
```

### Transcription with Language

```python
from openai import OpenAI

client = OpenAI()

with open("french_audio.mp3", "rb") as audio_file:
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        language="fr"  # French
    )

print(transcription.text)
```

### Transcription with Timestamps

```python
from openai import OpenAI

client = OpenAI()

with open("meeting.mp3", "rb") as audio_file:
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="verbose_json",
        timestamp_granularities=["segment"]
    )

for segment in transcription.segments:
    print(f"[{segment.start:.2f}s - {segment.end:.2f}s] {segment.text}")
```

### Transcription with Context Prompt

```python
from openai import OpenAI

client = OpenAI()

with open("technical_talk.mp3", "rb") as audio_file:
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        prompt="This is a discussion about machine learning, neural networks, and transformers."
    )

print(transcription.text)
```

### Generate Subtitles (SRT)

```python
from openai import OpenAI

client = OpenAI()

with open("video_audio.mp3", "rb") as audio_file:
    subtitles = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="srt"
    )

with open("subtitles.srt", "w") as f:
    f.write(subtitles)
```

### Translation to English

```python
from openai import OpenAI

client = OpenAI()

with open("spanish_audio.mp3", "rb") as audio_file:
    translation = client.audio.translations.create(
        model="whisper-1",
        file=audio_file
    )

print(translation.text)  # English translation
```

### Using gpt-4o-mini-transcribe

```python
from openai import OpenAI

client = OpenAI()

with open("audio.mp3", "rb") as audio_file:
    transcription = client.audio.transcriptions.create(
        model="gpt-4o-mini-transcribe",  # Faster, cheaper
        file=audio_file
    )

print(transcription.text)
```

### Production Transcription Pipeline

```python
from openai import OpenAI
import os

class TranscriptionService:
    def __init__(self):
        self.client = OpenAI()
    
    def transcribe_file(
        self,
        file_path: str,
        language: str = None,
        with_timestamps: bool = False
    ) -> dict:
        """Transcribe audio file with options"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio file not found: {file_path}")
        
        file_size = os.path.getsize(file_path)
        if file_size > 25 * 1024 * 1024:  # 25MB
            raise ValueError("File exceeds 25MB limit")
        
        with open(file_path, "rb") as audio_file:
            params = {
                "model": "whisper-1",
                "file": audio_file
            }
            
            if language:
                params["language"] = language
            
            if with_timestamps:
                params["response_format"] = "verbose_json"
                params["timestamp_granularities"] = ["segment"]
            
            transcription = self.client.audio.transcriptions.create(**params)
        
        return transcription

# Usage
service = TranscriptionService()
result = service.transcribe_file(
    "podcast.mp3",
    language="en",
    with_timestamps=True
)

for segment in result.segments:
    print(f"{segment.start:.1f}s: {segment.text}")
```

## Error Responses

- **400 Bad Request** - Invalid audio format or parameters
- **413 Payload Too Large** - File exceeds 25MB
- **415 Unsupported Media Type** - Unsupported audio format

## Rate Limiting / Throttling

- **File uploads**: Count toward project limits
- **Processing time**: Longer audio = more time
- **Concurrent requests**: Limited concurrent transcriptions

## Differences from Other APIs

- **vs Google Speech-to-Text**: OpenAI simpler API, Google more features
- **vs Assembly AI**: Similar capabilities, different pricing
- **vs AWS Transcribe**: OpenAI easier setup, AWS more customization

## Limitations and Known Issues

- **25MB file limit**: Large files must be split [VERIFIED] (OAIAPI-SC-OAI-AUDTRN)
- **No speaker diarization**: Cannot identify different speakers [COMMUNITY] (OAIAPI-SC-SO-SPKR)
- **Accuracy varies**: Depends on audio quality and accents [COMMUNITY] (OAIAPI-SC-SO-ACCACC)

## Gotchas and Quirks

- **Language helps accuracy**: Specifying language improves results [VERIFIED] (OAIAPI-SC-OAI-AUDTRN)
- **Prompt for context**: Technical terms benefit from context prompts [COMMUNITY] (OAIAPI-SC-SO-PROMPT)
- **File format matters**: WAV provides best quality, MP3 most compatible [COMMUNITY] (OAIAPI-SC-SO-AUDFMT)

## Sources

- OAIAPI-SC-OAI-AUDTRN - POST Create a transcription
- OAIAPI-SC-OAI-AUDTRL - POST Create a translation
- OAIAPI-SC-OAI-GAUDIO - Audio guide

## Document History

**[2026-03-20 15:40]**
- Initial documentation created
