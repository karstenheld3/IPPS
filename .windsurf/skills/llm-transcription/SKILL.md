# LLM Transcription Skill

Universal transcription tools using LLMs with optimized prompts for each purpose.

## When to Use This Skill

**Apply when:**
- Converting images (screenshots, documents, diagrams) to markdown
- Transcribing audio files to markdown text
- Batch processing multiple files for transcription
- Preserving document structure in markdown format

**Do NOT apply when:**
- Evaluating LLM performance (use @llm-evaluation)
- Simple text extraction without formatting needs
- Real-time transcription (these are batch tools)

## Quick Start

1. Run `SETUP.md` once to install dependencies
2. Choose your script:
   - **Image to Markdown**: `transcribe-image-to-markdown.py` - Ensemble + judge + refinement
   - **Audio to Markdown**: `transcribe-audio-to-markdown.py`

## Available Scripts

**Image Transcription:**
- `transcribe-image-to-markdown.py` - Ensemble transcription with judge and refinement

**Audio Transcription:**
- `transcribe-audio-to-markdown.py` - Convert audio to markdown transcript

## Usage Examples

**Image Transcription:**
```bash
python transcribe-image-to-markdown.py --input-file doc.png --output-file doc.md --verbose
python transcribe-image-to-markdown.py --input-folder ./images --output-folder ./out --initial-candidates 3 --min-score 3.5
```

**Audio Transcription:**
```bash
python transcribe-audio-to-markdown.py --input recording.mp3 --output transcript.md
python transcribe-audio-to-markdown.py --input-dir ./audio --output-dir ./transcripts --workers 8
python transcribe-audio-to-markdown.py --input meeting.wav --format --output meeting.md
```

## Supported Formats

**Images:** `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`
**Audio:** `.mp3`, `.wav`, `.m4a`, `.ogg`, `.flac`

## Key Features

- **Optimized prompts** for each transcription type
- **Structure preservation** - headings, lists, tables maintained
- **Batch processing** support for multiple files
- **Parallel workers** - configurable via `--workers` flag
- **Skip existing** - safe to re-run after interruption
- **Cost tracking** with token usage reports
- **Multiple model support** - OpenAI and Anthropic
- **Real-time progress logging** - `[ worker N ]` format visible in terminal

## Audio Transcription Features

- **Auto-chunking** - Files >24MB automatically split into 10-min chunks via ffmpeg
- **Parallel workers** - `--workers N` for batch processing
- **Skip existing** - Skips files with existing `.md` output
- **LLM formatting** - `--format` cleans up transcript with speaker labels, paragraphs
- **Language hint** - `--language de` for better accuracy

**Requirements:** `ffmpeg` and `ffprobe` in PATH for chunking large files.

## Terminal Output

**IMPORTANT**: Never suppress script output with `| Out-Null` or `2>&1 | Out-Null`. The scripts provide real-time progress logging that must remain visible:

```
[ worker 1 ] [ 1 / 22 ] Processing: document_page001.jpg
[ worker 1 ] [ 1 / 22 ] Transcribing (1 candidates)...
[ worker 1 ] [ 1 / 22 ] Judging 1 candidates...
[ worker 1 ] [ 1 / 22 ] Done: document_page001.md (5.00, 6230+4760 tokens, $0.0111, 90.2s)
```

## Parallel Batching (Large Jobs)

For 50+ folders, split into N batches and run N parallel Cascade terminals:

```powershell
# 6 batches x 20 workers = 120 total workers
$folders = Get-ChildItem -Path $baseDir -Filter "*.jpg" -Recurse | 
    Group-Object DirectoryName | ForEach-Object { $_.Name }

# Split into batches (run each as separate non-blocking Cascade command)
$batch1 = $folders[0..12]   # Terminal 1: 13 folders
$batch2 = $folders[13..25]  # Terminal 2: 13 folders
# ... etc

# Each batch command
foreach ($f in $batchN) {
    $out = Join-Path $f "transcripts"
    & $venv $script --input-folder $f --output-folder $out --workers 20
}
```

Script skips existing transcriptions, so safe to re-run after interruption.

## Model Recommendations for Legal Documents

Tested on EU AI Act (144 pages, German legal text, 2024-02-04):

| Model | Avg Score | Accuracy | Cost | Use Case |
|-------|-----------|----------|------|----------|
| **gpt-5-mini** | 4.87 | ~99.5% | $3.89 | Legal, regulatory, contracts |
| **gpt-5-nano** | 4.17 | ~92% | $1.23 | Informal notes, drafts |

**gpt-5-mini** (recommended for legal):
- Verbatim transcription preserving exact wording
- Correct regulation numbers (e.g., "2022/2065")
- Accurate technical terminology
- No [unclear] markers - confident reading
- 0 critical errors in 144 pages

**gpt-5-nano** (not recommended for legal):
- Rewrites/summarizes instead of transcribing verbatim
- Wrong regulation numbers (e.g., "2022/665" instead of "2022/2065")
- Wrong terminology with legal/medical implications (e.g., "Blutanalyse" instead of "Blutdruck")
- 50+ [unclear] markers indicating reading difficulties
- Content duplication and structural issues

**For legal documents**: Use `--model gpt-5-mini --dpi 150` to avoid factual errors that could have regulatory consequences. The 150 DPI setting provides optimal balance between image quality and processing speed for document transcription.

## Configuration

API keys required in `~/.llm-keys` or environment variables:
- `OPENAI_API_KEY` - For GPT models and Whisper
- `ANTHROPIC_API_KEY` - For Claude models
