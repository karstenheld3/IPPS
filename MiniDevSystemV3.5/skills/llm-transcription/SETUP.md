# LLM Transcription Skill Setup

## Prerequisites

- Python 3.10+
- OpenAI API key (GPT vision models, Whisper)
- Anthropic API key (optional, Claude models)

## Installation

### 1. Python Dependencies

```bash
pip install openai anthropic httpx
```

### 2. API Keys

Location: `[WORKSPACE_FOLDER]\..\.tools\.api-keys.txt`

Format:
```
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

Pass `--keys-file` to scripts:
```powershell
python transcribe-image-to-markdown.py --keys-file ..\.tools\.api-keys.txt --input-file image.png
```

### 3. Verify

```bash
python transcribe-image-to-markdown.py --help
python transcribe-audio-to-markdown.py --help
```

## Audio: ffmpeg Required

```powershell
# Windows
winget install ffmpeg
# macOS: brew install ffmpeg
# Linux: sudo apt install ffmpeg
```

## Troubleshooting

- **"API key not found"**: Ensure keys file exists at standard location, pass correct `--keys-file` path
- **"Unsupported file format"**: Check SKILL.md for supported formats; ensure ffmpeg installed for audio
- **"Rate limit exceeded"**: Wait and retry; use batch mode with lower concurrency