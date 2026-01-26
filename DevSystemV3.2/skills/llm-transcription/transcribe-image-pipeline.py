#!/usr/bin/env python3
"""
transcribe-image-pipeline.py - Ensemble transcription with judge and refinement.

Pipeline:
1. Generate 3 transcriptions concurrently (same prompt)
2. Judge all 3 concurrently, select highest score
3. If score < threshold, feed best back with fixing requests
4. Re-score refinement, take as final if higher

Usage:
  python transcribe-image-pipeline.py --input image.png --output result.md
  python transcribe-image-pipeline.py --input-dir ./images --output-dir ./transcripts
"""

import os
import sys
import json
import base64
import asyncio
import argparse
from pathlib import Path
from datetime import datetime, timezone
from dataclasses import dataclass
from typing import Optional

IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
DEFAULT_MODEL = 'gpt-4o'
DEFAULT_JUDGE_MODEL = 'gpt-4o-mini'
DEFAULT_ENSEMBLE_SIZE = 3
DEFAULT_MIN_SCORE = 3.5
DEFAULT_MAX_REFINEMENTS = 1


@dataclass
class TranscriptionResult:
    content: str
    input_tokens: int
    output_tokens: int
    model: str
    elapsed_seconds: float


@dataclass
class JudgeResult:
    text_accuracy: float
    page_structure: float
    graphics_quality: float
    weighted_score: float
    justification: dict
    input_tokens: int
    output_tokens: int


@dataclass
class PipelineResult:
    final_content: str
    final_score: float
    candidates_count: int
    refinement_applied: bool
    total_input_tokens: int
    total_output_tokens: int
    elapsed_seconds: float


def get_script_dir() -> Path:
    return Path(__file__).parent


def load_api_keys() -> dict:
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


def load_prompt(prompt_path: Path) -> str:
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
    return prompt_path.read_text(encoding='utf-8')


def encode_image_base64(image_path: Path) -> tuple[str, str]:
    suffix = image_path.suffix.lower()
    media_types = {
        '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
        '.png': 'image/png', '.gif': 'image/gif', '.webp': 'image/webp'
    }
    media_type = media_types.get(suffix, 'image/png')
    with open(image_path, 'rb') as f:
        data = base64.b64encode(f.read()).decode('utf-8')
    return data, media_type


async def call_openai_vision(model: str, image_data: str, media_type: str,
                              prompt: str, api_key: str, max_tokens: int = 8192) -> dict:
    import httpx
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    payload = {
        'model': model,
        'max_tokens': max_tokens,
        'messages': [{
            'role': 'user',
            'content': [
                {'type': 'text', 'text': prompt},
                {'type': 'image_url', 'image_url': {'url': f'data:{media_type};base64,{image_data}'}}
            ]
        }]
    }
    
    async with httpx.AsyncClient(timeout=180.0) as client:
        response = await client.post(
            'https://api.openai.com/v1/chat/completions',
            headers=headers, json=payload
        )
        response.raise_for_status()
        result = response.json()
    
    return {
        'content': result['choices'][0]['message']['content'],
        'input_tokens': result['usage']['prompt_tokens'],
        'output_tokens': result['usage']['completion_tokens'],
        'model': result.get('model', model)
    }


async def call_openai_text(model: str, prompt: str, api_key: str,
                           max_tokens: int = 4096, response_format: str = None) -> dict:
    import httpx
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    payload = {
        'model': model,
        'max_tokens': max_tokens,
        'messages': [{'role': 'user', 'content': prompt}]
    }
    if response_format == 'json':
        payload['response_format'] = {'type': 'json_object'}
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            'https://api.openai.com/v1/chat/completions',
            headers=headers, json=payload
        )
        response.raise_for_status()
        result = response.json()
    
    return {
        'content': result['choices'][0]['message']['content'],
        'input_tokens': result['usage']['prompt_tokens'],
        'output_tokens': result['usage']['completion_tokens'],
        'model': result.get('model', model)
    }


async def generate_transcription(image_data: str, media_type: str, prompt: str,
                                  model: str, api_key: str) -> TranscriptionResult:
    start = datetime.now(timezone.utc)
    result = await call_openai_vision(model, image_data, media_type, prompt, api_key)
    elapsed = (datetime.now(timezone.utc) - start).total_seconds()
    
    return TranscriptionResult(
        content=result['content'],
        input_tokens=result['input_tokens'],
        output_tokens=result['output_tokens'],
        model=result['model'],
        elapsed_seconds=elapsed
    )


async def judge_transcription(image_data: str, media_type: str, transcription: str,
                               judge_prompt: str, model: str, api_key: str) -> JudgeResult:
    full_prompt = f"""{judge_prompt}

---

## Image
[Provided as attachment]

## Transcription to Judge

{transcription}
"""
    
    result = await call_openai_vision(model, image_data, media_type, full_prompt, api_key, max_tokens=2048)
    
    # Parse JSON response
    content = result['content']
    try:
        # Find JSON in response
        start_idx = content.find('{')
        end_idx = content.rfind('}') + 1
        if start_idx >= 0 and end_idx > start_idx:
            json_str = content[start_idx:end_idx]
            data = json.loads(json_str)
        else:
            raise ValueError("No JSON found in response")
        
        return JudgeResult(
            text_accuracy=data.get('text_accuracy', {}).get('score', 0),
            page_structure=data.get('page_structure', {}).get('score', 0),
            graphics_quality=data.get('graphics_quality', {}).get('score', 0),
            weighted_score=data.get('weighted_score', 0),
            justification=data,
            input_tokens=result['input_tokens'],
            output_tokens=result['output_tokens']
        )
    except (json.JSONDecodeError, KeyError) as e:
        # Fallback: assign middle score if parsing fails
        return JudgeResult(
            text_accuracy=3, page_structure=3, graphics_quality=3,
            weighted_score=3.0,
            justification={'error': str(e), 'raw': content[:500]},
            input_tokens=result['input_tokens'],
            output_tokens=result['output_tokens']
        )


async def refine_transcription(image_data: str, media_type: str, transcription: str,
                                judge_result: JudgeResult, transcribe_prompt: str,
                                model: str, api_key: str) -> TranscriptionResult:
    issues = []
    if judge_result.text_accuracy < 4:
        issues.append("text accuracy errors")
    if judge_result.page_structure < 4:
        issues.append("structure/hierarchy issues")
    if judge_result.graphics_quality < 4:
        issues.append("missing or incomplete graphics")
    
    refinement_prompt = f"""{transcribe_prompt}

---

## REFINEMENT REQUEST

A previous transcription attempt had these issues: {', '.join(issues)}

Previous transcription (fix the issues):
```
{transcription[:4000]}
```

Judge feedback:
{json.dumps(judge_result.justification, indent=2)[:2000]}

Please produce an improved transcription fixing these specific issues.
"""
    
    start = datetime.now(timezone.utc)
    result = await call_openai_vision(model, image_data, media_type, refinement_prompt, api_key)
    elapsed = (datetime.now(timezone.utc) - start).total_seconds()
    
    return TranscriptionResult(
        content=result['content'],
        input_tokens=result['input_tokens'],
        output_tokens=result['output_tokens'],
        model=result['model'],
        elapsed_seconds=elapsed
    )


async def run_pipeline(image_path: Path, transcribe_prompt: str, judge_prompt: str,
                       model: str, judge_model: str, api_key: str,
                       ensemble_size: int = 3, min_score: float = 3.5,
                       max_refinements: int = 1, verbose: bool = False) -> PipelineResult:
    start = datetime.now(timezone.utc)
    total_input_tokens = 0
    total_output_tokens = 0
    
    # Encode image
    image_data, media_type = encode_image_base64(image_path)
    
    # Step 1: Generate N transcriptions concurrently
    if verbose:
        print(f"  [1/3] Generating {ensemble_size} transcriptions...")
    
    transcription_tasks = [
        generate_transcription(image_data, media_type, transcribe_prompt, model, api_key)
        for _ in range(ensemble_size)
    ]
    transcriptions = await asyncio.gather(*transcription_tasks)
    
    for t in transcriptions:
        total_input_tokens += t.input_tokens
        total_output_tokens += t.output_tokens
    
    # Step 2: Judge all transcriptions concurrently
    if verbose:
        print(f"  [2/3] Judging {len(transcriptions)} transcriptions...")
    
    judge_tasks = [
        judge_transcription(image_data, media_type, t.content, judge_prompt, judge_model, api_key)
        for t in transcriptions
    ]
    judge_results = await asyncio.gather(*judge_tasks)
    
    for j in judge_results:
        total_input_tokens += j.input_tokens
        total_output_tokens += j.output_tokens
    
    # Select best
    best_idx = max(range(len(judge_results)), key=lambda i: judge_results[i].weighted_score)
    best_transcription = transcriptions[best_idx]
    best_judge = judge_results[best_idx]
    
    if verbose:
        scores = [f"{j.weighted_score:.2f}" for j in judge_results]
        print(f"       Scores: [{', '.join(scores)}] -> selected #{best_idx + 1} ({best_judge.weighted_score:.2f})")
    
    # Step 3: Refinement if needed
    refinement_applied = False
    if best_judge.weighted_score < min_score and max_refinements > 0:
        if verbose:
            print(f"  [3/3] Score {best_judge.weighted_score:.2f} < {min_score}, refining...")
        
        refined = await refine_transcription(
            image_data, media_type, best_transcription.content,
            best_judge, transcribe_prompt, model, api_key
        )
        total_input_tokens += refined.input_tokens
        total_output_tokens += refined.output_tokens
        
        # Re-judge refinement
        refined_judge = await judge_transcription(
            image_data, media_type, refined.content, judge_prompt, judge_model, api_key
        )
        total_input_tokens += refined_judge.input_tokens
        total_output_tokens += refined_judge.output_tokens
        
        if verbose:
            print(f"       Refined score: {refined_judge.weighted_score:.2f}")
        
        # Take refined if better
        if refined_judge.weighted_score > best_judge.weighted_score:
            best_transcription = refined
            best_judge = refined_judge
            refinement_applied = True
    elif verbose:
        print(f"  [3/3] Score {best_judge.weighted_score:.2f} >= {min_score}, skipping refinement")
    
    elapsed = (datetime.now(timezone.utc) - start).total_seconds()
    
    return PipelineResult(
        final_content=best_transcription.content,
        final_score=best_judge.weighted_score,
        candidates_count=ensemble_size,
        refinement_applied=refinement_applied,
        total_input_tokens=total_input_tokens,
        total_output_tokens=total_output_tokens,
        elapsed_seconds=elapsed
    )


async def process_single(input_path: Path, output_path: Path,
                         transcribe_prompt: str, judge_prompt: str,
                         model: str, judge_model: str, api_key: str,
                         ensemble_size: int, min_score: float,
                         max_refinements: int, verbose: bool) -> dict:
    if verbose:
        print(f"Processing: {input_path}")
    
    result = await run_pipeline(
        input_path, transcribe_prompt, judge_prompt,
        model, judge_model, api_key,
        ensemble_size, min_score, max_refinements, verbose
    )
    
    # Write output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(result.final_content)
    
    if verbose:
        refined_str = " (refined)" if result.refinement_applied else ""
        print(f"  -> {output_path} (score: {result.final_score:.2f}{refined_str}, "
              f"{result.total_input_tokens}+{result.total_output_tokens} tokens, {result.elapsed_seconds:.1f}s)")
    
    return {
        'input': str(input_path),
        'output': str(output_path),
        'score': result.final_score,
        'candidates': result.candidates_count,
        'refinement_applied': result.refinement_applied,
        'input_tokens': result.total_input_tokens,
        'output_tokens': result.total_output_tokens,
        'elapsed_seconds': result.elapsed_seconds
    }


async def process_batch(input_dir: Path, output_dir: Path,
                        transcribe_prompt: str, judge_prompt: str,
                        model: str, judge_model: str, api_key: str,
                        ensemble_size: int, min_score: float,
                        max_refinements: int, verbose: bool) -> list:
    results = []
    
    image_files = [f for f in input_dir.iterdir()
                   if f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS]
    
    if not image_files:
        print(f"No image files found in {input_dir}")
        return results
    
    print(f"Found {len(image_files)} images to process")
    
    for image_file in sorted(image_files):
        output_file = output_dir / (image_file.stem + '.md')
        try:
            result = await process_single(
                image_file, output_file, transcribe_prompt, judge_prompt,
                model, judge_model, api_key, ensemble_size, min_score,
                max_refinements, verbose
            )
            results.append(result)
        except Exception as e:
            print(f"[ERROR] Failed to process {image_file}: {e}", file=sys.stderr)
            results.append({'input': str(image_file), 'error': str(e)})
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description='Ensemble transcription with judge and refinement pipeline.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Pipeline:
  1. Generate N transcriptions concurrently
  2. Judge all N concurrently, select highest score
  3. If score < threshold, refine best and re-judge

Examples:
  python transcribe-image-pipeline.py --input doc.png --output doc.md
  python transcribe-image-pipeline.py --input-dir ./images --output-dir ./out --verbose
        """
    )
    
    # Input/Output
    parser.add_argument('--input', '-i', type=Path, help='Input image file')
    parser.add_argument('--output', '-o', type=Path, help='Output markdown file')
    parser.add_argument('--input-dir', type=Path, help='Input directory for batch')
    parser.add_argument('--output-dir', type=Path, help='Output directory for batch')
    
    # Prompts
    parser.add_argument('--transcribe-prompt', type=Path, help='Transcription prompt file')
    parser.add_argument('--judge-prompt', type=Path, help='Judge prompt file')
    
    # Models
    parser.add_argument('--model', '-m', default=DEFAULT_MODEL,
                        help=f'Transcription model (default: {DEFAULT_MODEL})')
    parser.add_argument('--judge-model', default=DEFAULT_JUDGE_MODEL,
                        help=f'Judge model (default: {DEFAULT_JUDGE_MODEL})')
    
    # Pipeline settings
    parser.add_argument('--ensemble-size', '-n', type=int, default=DEFAULT_ENSEMBLE_SIZE,
                        help=f'Number of transcriptions to generate (default: {DEFAULT_ENSEMBLE_SIZE})')
    parser.add_argument('--min-score', type=float, default=DEFAULT_MIN_SCORE,
                        help=f'Minimum score before refinement (default: {DEFAULT_MIN_SCORE})')
    parser.add_argument('--max-refinements', type=int, default=DEFAULT_MAX_REFINEMENTS,
                        help=f'Max refinement iterations (default: {DEFAULT_MAX_REFINEMENTS})')
    
    # Output
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--json', action='store_true', help='Output results as JSON')
    
    args = parser.parse_args()
    
    # Validate
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
    api_key = api_keys.get('OPENAI_API_KEY')
    if not api_key:
        print("[ERROR] OPENAI_API_KEY not found", file=sys.stderr)
        sys.exit(1)
    
    # Load prompts
    script_dir = get_script_dir()
    prompts_dir = script_dir / 'prompts'
    
    if args.transcribe_prompt:
        transcribe_prompt = load_prompt(args.transcribe_prompt)
    elif (prompts_dir / 'transcription.md').exists():
        transcribe_prompt = load_prompt(prompts_dir / 'transcription.md')
    else:
        print("[ERROR] No transcription prompt. Use --transcribe-prompt or create prompts/transcription.md", file=sys.stderr)
        sys.exit(1)
    
    if args.judge_prompt:
        judge_prompt = load_prompt(args.judge_prompt)
    elif (prompts_dir / 'judge.md').exists():
        judge_prompt = load_prompt(prompts_dir / 'judge.md')
    else:
        print("[ERROR] No judge prompt. Use --judge-prompt or create prompts/judge.md", file=sys.stderr)
        sys.exit(1)
    
    # Run
    try:
        if single_mode:
            result = asyncio.run(process_single(
                args.input, args.output, transcribe_prompt, judge_prompt,
                args.model, args.judge_model, api_key,
                args.ensemble_size, args.min_score, args.max_refinements, args.verbose
            ))
            results = [result]
        else:
            results = asyncio.run(process_batch(
                args.input_dir, args.output_dir, transcribe_prompt, judge_prompt,
                args.model, args.judge_model, api_key,
                args.ensemble_size, args.min_score, args.max_refinements, args.verbose
            ))
        
        # Summary
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            total_tokens = sum(r.get('input_tokens', 0) + r.get('output_tokens', 0) for r in results)
            avg_score = sum(r.get('score', 0) for r in results if 'score' in r) / max(1, len([r for r in results if 'score' in r]))
            refined = sum(1 for r in results if r.get('refinement_applied'))
            errors = sum(1 for r in results if 'error' in r)
            
            print(f"\nSummary: {len(results)} files, {errors} errors")
            print(f"Average score: {avg_score:.2f}, {refined} refined")
            print(f"Total tokens: {total_tokens}")
    
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
