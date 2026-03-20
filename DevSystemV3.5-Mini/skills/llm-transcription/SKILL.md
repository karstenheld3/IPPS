---
name: llm-transcription
description: Universal transcription tools using LLMs with optimized prompts for each purpose.
---

# LLM Transcription Skill

## When to Use

**Apply when:** Converting images/audio to structured markdown, batch transcription, preserving document structure.

**Do NOT apply when:** Evaluating LLM performance (use @llm-evaluation), simple text extraction, real-time transcription.

## Scripts

- `transcribe-image-to-markdown.py` - Ensemble transcription with judge and refinement
- `transcribe-audio-to-markdown.py` - Audio to markdown transcript

```bash
python transcribe-image-to-markdown.py --input-file doc.png --output-file doc.md --verbose
python transcribe-image-to-markdown.py --input-folder ./images --output-folder ./out --initial-candidates 3 --min-score 3.5
python transcribe-audio-to-markdown.py --input recording.mp3 --output transcript.md --model whisper-1
```

## Supported Formats

**Images:** `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`
**Audio:** `.mp3`, `.wav`, `.m4a`, `.ogg`, `.flac`

## Key Features

- Optimized prompts per transcription type
- Structure preservation (headings, lists, tables)
- Batch processing with parallel workers
- Cost tracking with token usage reports
- OpenAI and Anthropic model support

## Model Recommendations

Tested on EU AI Act (144 pages, German legal text):

**gpt-5-mini** (recommended for legal/regulatory): 4.87 avg score, ~99.5% accuracy, $3.89. Verbatim transcription, correct regulation numbers, 0 critical errors in 144 pages.

**gpt-5-nano** (informal notes only): 4.17 avg score, ~92% accuracy, $1.23. Rewrites instead of transcribing, wrong regulation numbers, wrong terminology with legal implications, 50+ [unclear] markers.

**For legal documents**: Use `--model gpt-5-mini --dpi 120` to avoid factual errors with regulatory consequences.

## Configuration

API keys required in `~/.llm-keys` or environment variables:
- `OPENAI_API_KEY` - For GPT models and Whisper
- `ANTHROPIC_API_KEY` - For Claude models