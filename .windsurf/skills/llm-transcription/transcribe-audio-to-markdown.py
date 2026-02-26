#!/usr/bin/env python3
"""
transcribe-audio-to-markdown.py - Convert audio files to markdown transcripts using Whisper API.

Usage:
  python transcribe-audio-to-markdown.py --input recording.mp3 --output transcript.md
  python transcribe-audio-to-markdown.py --input meeting.wav --format --output meeting.md
  python transcribe-audio-to-markdown.py --input-dir ./audio --output-dir ./transcripts
"""

import os
import sys
import json
import argparse
import subprocess
import tempfile
import shutil
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

AUDIO_EXTENSIONS = {'.mp3', '.wav', '.m4a', '.ogg', '.flac', '.webm', '.mp4', '.mpeg', '.mpga'}
DEFAULT_MODEL = 'whisper-1'
DEFAULT_FORMAT_MODEL = 'gpt-4o-mini'
DEFAULT_WORKERS = 4
MAX_FILE_SIZE_MB = 24
DEFAULT_CHUNK_DURATION_MIN = 10

FORMATTING_PROMPT = """You are a transcript editor. Format the provided raw transcript into clean, readable markdown.

INSTRUCTIONS:
1. Add paragraph breaks at natural pauses and topic changes
2. Use headings (##) for major topic shifts or sections
3. Use bullet points for lists mentioned verbally
4. Clean up filler words (um, uh, like) unless they convey meaning
5. Fix obvious transcription errors when context makes intent clear
6. Add speaker labels if multiple speakers are evident: **Speaker 1:**, **Speaker 2:**
7. Preserve all meaningful content - do not summarize or omit information
8. Use **bold** for emphasized words/phrases
9. Use > blockquotes for direct quotes or citations mentioned

OUTPUT FORMAT:
- Return ONLY the formatted markdown
- No explanations or metadata
- Start directly with the transcript content"""


def load_api_keys() -> dict:
    """Load API keys from ~/.llm-keys or environment."""
    keys = {}
    
    if os.environ.get('OPENAI_API_KEY'):
        keys['OPENAI_API_KEY'] = os.environ['OPENAI_API_KEY']
    if os.environ.get('ANTHROPIC_API_KEY'):
        keys['ANTHROPIC_API_KEY'] = os.environ['ANTHROPIC_API_KEY']
    
    keys_file = Path.home() / '.llm-keys'
    if keys_file.exists():
        with open(keys_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    key, value = line.split('=', 1)
                    keys[key.strip()] = value.strip()
    
    return keys


def log(worker_id: int, file_idx: int, total_files: int, message: str):
    """Print formatted log message."""
    print(f"[ worker {worker_id + 1} ] [ {file_idx} / {total_files} ] {message}", file=sys.stderr)


def get_file_size_mb(path: Path) -> float:
    """Get file size in megabytes."""
    return path.stat().st_size / (1024 * 1024)


def get_audio_duration(audio_path: Path) -> float:
    """Get audio duration in seconds using ffprobe."""
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'quiet', '-show_entries', 'format=duration',
             '-of', 'default=noprint_wrappers=1:nokey=1', str(audio_path)],
            capture_output=True, text=True, check=True
        )
        return float(result.stdout.strip())
    except (subprocess.CalledProcessError, ValueError, FileNotFoundError):
        return 0.0


def split_audio_file(audio_path: Path, chunk_duration_min: float, temp_dir: Path) -> list[Path]:
    """Split audio file into chunks using ffmpeg. Returns list of chunk paths."""
    chunk_duration_sec = chunk_duration_min * 60
    duration = get_audio_duration(audio_path)
    
    if duration <= 0:
        return [audio_path]
    
    if duration <= chunk_duration_sec:
        return [audio_path]
    
    chunks = []
    chunk_idx = 0
    start_time = 0
    
    while start_time < duration:
        chunk_path = temp_dir / f"{audio_path.stem}_chunk{chunk_idx:03d}.mp3"
        
        cmd = [
            'ffmpeg', '-y', '-v', 'quiet',
            '-i', str(audio_path),
            '-ss', str(start_time),
            '-t', str(chunk_duration_sec),
            '-acodec', 'libmp3lame', '-b:a', '128k',
            str(chunk_path)
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            if chunk_path.exists() and chunk_path.stat().st_size > 0:
                chunks.append(chunk_path)
        except subprocess.CalledProcessError as e:
            print(f"[WARN] Failed to create chunk {chunk_idx}: {e}", file=sys.stderr)
        
        start_time += chunk_duration_sec
        chunk_idx += 1
    
    return chunks if chunks else [audio_path]


def transcribe_audio(audio_path: Path, api_key: str, model: str = DEFAULT_MODEL,
                     language: str = None, response_format: str = 'text',
                     timeout: float = 600.0) -> dict:
    """Transcribe audio using OpenAI Whisper API."""
    import httpx
    
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    suffix = audio_path.suffix.lower()
    if suffix not in AUDIO_EXTENSIONS:
        raise ValueError(f"Unsupported audio format: {suffix}. Supported: {AUDIO_EXTENSIONS}")
    
    file_size_mb = get_file_size_mb(audio_path)
    if file_size_mb > 25:
        raise ValueError(f"File too large: {file_size_mb:.1f}MB (max 25MB). Use chunking.")
    
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    
    with httpx.Client(timeout=timeout) as client:
        with open(audio_path, 'rb') as f:
            files = {
                'file': (audio_path.name, f, 'audio/mpeg'),
                'model': (None, model),
                'response_format': (None, response_format),
            }
            if language:
                files['language'] = (None, language)
            
            response = client.post(
                'https://api.openai.com/v1/audio/transcriptions',
                headers=headers,
                files=files
            )
        response.raise_for_status()
        
        if response_format == 'json' or response_format == 'verbose_json':
            result = response.json()
            text = result.get('text', '')
            duration = result.get('duration', 0)
        else:
            text = response.text
            duration = 0
    
    return {
        'text': text,
        'duration': duration,
        'model': model
    }


def transcribe_with_chunking(audio_path: Path, api_key: str, model: str = DEFAULT_MODEL,
                              language: str = None, chunk_duration_min: float = DEFAULT_CHUNK_DURATION_MIN,
                              verbose: bool = False) -> dict:
    """Transcribe audio, automatically chunking if file is too large."""
    file_size_mb = get_file_size_mb(audio_path)
    
    if file_size_mb <= MAX_FILE_SIZE_MB:
        return transcribe_audio(audio_path, api_key, model, language, 'verbose_json')
    
    if verbose:
        print(f"  File {file_size_mb:.1f}MB > {MAX_FILE_SIZE_MB}MB, chunking...", file=sys.stderr)
    
    temp_dir = Path(tempfile.mkdtemp(prefix='audio_chunks_'))
    try:
        chunks = split_audio_file(audio_path, chunk_duration_min, temp_dir)
        
        if verbose:
            print(f"  Split into {len(chunks)} chunks", file=sys.stderr)
        
        all_text = []
        total_duration = 0
        
        for i, chunk in enumerate(chunks):
            if verbose:
                print(f"  Transcribing chunk {i+1}/{len(chunks)}...", file=sys.stderr)
            
            result = transcribe_audio(chunk, api_key, model, language, 'verbose_json')
            all_text.append(result['text'])
            total_duration += result.get('duration', 0)
        
        return {
            'text': ' '.join(all_text),
            'duration': total_duration,
            'model': model,
            'chunks': len(chunks)
        }
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def format_transcript(text: str, api_key: str, model: str = DEFAULT_FORMAT_MODEL,
                      prompt: str = None) -> dict:
    """Format raw transcript using LLM."""
    import httpx
    
    if prompt is None:
        prompt = FORMATTING_PROMPT
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'model': model,
        'max_tokens': 8192,
        'messages': [
            {'role': 'system', 'content': prompt},
            {'role': 'user', 'content': f"Format this transcript:\n\n{text}"}
        ]
    }
    
    with httpx.Client(timeout=120.0) as client:
        response = client.post(
            'https://api.openai.com/v1/chat/completions',
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        result = response.json()
    
    return {
        'content': result['choices'][0]['message']['content'],
        'input_tokens': result['usage']['prompt_tokens'],
        'output_tokens': result['usage']['completion_tokens'],
        'model': result.get('model', model)
    }


def process_single(worker_id: int, file_idx: int, total_files: int,
                   input_path: Path, output_path: Path, api_keys: dict,
                   model: str = DEFAULT_MODEL, language: str = None,
                   do_format: bool = False, format_model: str = DEFAULT_FORMAT_MODEL,
                   format_prompt: str = None, chunk_duration_min: float = DEFAULT_CHUNK_DURATION_MIN,
                   results_lock: Lock = None, force: bool = False) -> dict:
    """Process a single audio file."""
    import time
    start_time = time.time()
    
    if output_path.exists() and not force:
        log(worker_id, file_idx, total_files, f"Skipping: {input_path.name} (exists)")
        return {'input': str(input_path), 'output': str(output_path), 'skipped': True}
    
    api_key = api_keys.get('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found")
    
    log(worker_id, file_idx, total_files, f"Processing: {input_path.name}")
    
    file_size_mb = get_file_size_mb(input_path)
    if file_size_mb > MAX_FILE_SIZE_MB:
        log(worker_id, file_idx, total_files, f"Chunking: {file_size_mb:.1f}MB file")
    
    transcript = transcribe_with_chunking(
        input_path, api_key, model, language, chunk_duration_min, verbose=True
    )
    
    text = transcript['text']
    format_tokens = {'input': 0, 'output': 0}
    
    if do_format and text.strip():
        log(worker_id, file_idx, total_files, f"Formatting with {format_model}...")
        format_result = format_transcript(text, api_key, format_model, format_prompt)
        text = format_result['content']
        format_tokens = {
            'input': format_result['input_tokens'],
            'output': format_result['output_tokens']
        }
    
    if results_lock:
        with results_lock:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(text, encoding='utf-8')
    else:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(text, encoding='utf-8')
    
    elapsed = time.time() - start_time
    
    duration_info = f", {transcript['duration']:.1f}s audio" if transcript.get('duration') else ""
    chunks_info = f", {transcript.get('chunks', 1)} chunks" if transcript.get('chunks', 1) > 1 else ""
    log(worker_id, file_idx, total_files, 
        f"Done: {output_path.name} ({elapsed:.1f}s{duration_info}{chunks_info})")
    
    return {
        'input': str(input_path),
        'output': str(output_path),
        'whisper_model': transcript['model'],
        'format_model': format_model if do_format else None,
        'audio_duration': transcript.get('duration', 0),
        'chunks': transcript.get('chunks', 1),
        'format_input_tokens': format_tokens['input'],
        'format_output_tokens': format_tokens['output'],
        'elapsed_seconds': elapsed
    }


def process_batch(input_dir: Path, output_dir: Path, api_keys: dict,
                  model: str = DEFAULT_MODEL, language: str = None,
                  do_format: bool = False, format_model: str = DEFAULT_FORMAT_MODEL,
                  format_prompt: str = None, workers: int = DEFAULT_WORKERS,
                  chunk_duration_min: float = DEFAULT_CHUNK_DURATION_MIN,
                  force: bool = False) -> list:
    """Process all audio files in a directory with parallel workers."""
    results = []
    results_lock = Lock()
    
    audio_files = sorted([f for f in input_dir.iterdir()
                          if f.is_file() and f.suffix.lower() in AUDIO_EXTENSIONS])
    
    if not audio_files:
        print(f"No audio files found in {input_dir}", file=sys.stderr)
        return results
    
    print(f"Found {len(audio_files)} audio files, processing with {workers} workers", file=sys.stderr)
    
    def process_wrapper(idx_and_file):
        idx, audio_file = idx_and_file
        output_file = output_dir / (audio_file.stem + '.md')
        try:
            return process_single(
                idx % workers, idx + 1, len(audio_files),
                audio_file, output_file, api_keys, model, language,
                do_format, format_model, format_prompt, chunk_duration_min,
                results_lock, force
            )
        except Exception as e:
            log(idx % workers, idx + 1, len(audio_files), f"FAILED: {audio_file.name} - {e}")
            return {'input': str(audio_file), 'error': str(e)}
    
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(process_wrapper, (i, f)): f for i, f in enumerate(audio_files)}
        for future in as_completed(futures):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                results.append({'input': str(futures[future]), 'error': str(e)})
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description='Convert audio files to markdown transcripts using Whisper API.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python transcribe-audio-to-markdown.py --input recording.mp3 --output transcript.md
  python transcribe-audio-to-markdown.py --input meeting.wav --format --output meeting.md
  python transcribe-audio-to-markdown.py --input-dir ./audio --output-dir ./transcripts --workers 8
        """
    )
    
    # Input/Output
    parser.add_argument('--input', '-i', type=Path, help='Input audio file')
    parser.add_argument('--output', '-o', type=Path, help='Output markdown file')
    parser.add_argument('--input-dir', type=Path, help='Input directory for batch processing')
    parser.add_argument('--output-dir', type=Path, help='Output directory for batch processing')
    
    # Whisper options
    parser.add_argument('--model', '-m', default=DEFAULT_MODEL,
                        help=f'Whisper model (default: {DEFAULT_MODEL})')
    parser.add_argument('--language', '-l',
                        help='Language code (e.g., en, de, fr). Auto-detect if not specified.')
    
    # Processing options
    parser.add_argument('--workers', '-w', type=int, default=DEFAULT_WORKERS,
                        help=f'Parallel workers for batch mode (default: {DEFAULT_WORKERS})')
    parser.add_argument('--chunk-duration', type=float, default=DEFAULT_CHUNK_DURATION_MIN,
                        help=f'Chunk duration in minutes for large files (default: {DEFAULT_CHUNK_DURATION_MIN})')
    parser.add_argument('--force', action='store_true',
                        help='Force reprocess existing files')
    
    # Formatting options
    parser.add_argument('--format', '-f', action='store_true',
                        help='Format transcript with LLM for better readability')
    parser.add_argument('--format-model', default=DEFAULT_FORMAT_MODEL,
                        help=f'Model for formatting (default: {DEFAULT_FORMAT_MODEL})')
    parser.add_argument('--format-prompt-file', type=Path,
                        help='Custom formatting prompt file')
    
    # Output options
    parser.add_argument('--json', action='store_true',
                        help='Output results as JSON')
    
    args = parser.parse_args()
    
    # Validate arguments
    single_mode = args.input is not None
    batch_mode = args.input_dir is not None
    
    if not single_mode and not batch_mode:
        parser.error("Either --input or --input-dir is required")
    
    if single_mode and batch_mode:
        parser.error("Cannot use both --input and --input-dir")
    
    if single_mode and not args.output:
        args.output = args.input.with_suffix('.md')
    
    if batch_mode and not args.output_dir:
        args.output_dir = args.input_dir / 'transcripts'
    
    # Load API keys
    api_keys = load_api_keys()
    if not api_keys.get('OPENAI_API_KEY'):
        print("[ERROR] OPENAI_API_KEY not found. Set it or create ~/.llm-keys", file=sys.stderr)
        sys.exit(1)
    
    # Load custom format prompt if provided
    format_prompt = None
    if args.format_prompt_file:
        if not args.format_prompt_file.exists():
            print(f"[ERROR] Format prompt file not found: {args.format_prompt_file}", file=sys.stderr)
            sys.exit(1)
        format_prompt = args.format_prompt_file.read_text(encoding='utf-8')
    
    # Process
    try:
        if single_mode:
            result = process_single(
                0, 1, 1,
                args.input, args.output, api_keys, args.model, args.language,
                args.format, args.format_model, format_prompt, args.chunk_duration,
                None, args.force
            )
            results = [result]
        else:
            results = process_batch(
                args.input_dir, args.output_dir, api_keys, args.model, args.language,
                args.format, args.format_model, format_prompt, args.workers,
                args.chunk_duration, args.force
            )
        
        # Output summary
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            successful = [r for r in results if 'whisper_model' in r]
            failed = [r for r in results if 'error' in r]
            skipped = [r for r in results if r.get('skipped')]
            
            total_duration = sum(r.get('audio_duration', 0) for r in successful)
            total_chunks = sum(r.get('chunks', 1) for r in successful)
            total_format_tokens = sum(r.get('format_input_tokens', 0) + r.get('format_output_tokens', 0) for r in successful)
            total_elapsed = sum(r.get('elapsed_seconds', 0) for r in successful)
            
            print(f"\n{'='*60}", file=sys.stderr)
            print(f"Summary: {len(successful)} successful, {len(failed)} failed, {len(skipped)} skipped", file=sys.stderr)
            if total_duration:
                print(f"Audio duration: {total_duration:.1f} seconds", file=sys.stderr)
            if total_chunks > len(successful):
                print(f"Total chunks processed: {total_chunks}", file=sys.stderr)
            if args.format and total_format_tokens:
                print(f"Formatting tokens: {total_format_tokens}", file=sys.stderr)
            print(f"Total time: {total_elapsed:.1f}s", file=sys.stderr)
    
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
