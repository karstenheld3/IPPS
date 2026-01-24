#!/usr/bin/env python3
"""
compare-transcription-runs.py - Compare transcription output files.

Supports three comparison methods:
- levenshtein: Character-level distance (default)
- semantic: LLM-as-a-judge for all content
- hybrid: Levenshtein for text, LLM-as-a-judge for <transcription_image> sections

Usage:
  python compare-transcription-runs.py --input-folder runs/ --output-file report.json
  python compare-transcription-runs.py --input-folder runs/ --output-file report.json \
      --method hybrid --judge-model gpt-4o --keys-file .tools/.api-keys.txt
"""

import sys, json, argparse, re
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

EFFORT_LEVELS = ['none', 'minimal', 'low', 'medium', 'high', 'xhigh']

DEFAULT_JUDGE_PROMPT = """Compare these two transcriptions of the same figure. Score semantic equivalence 0-100.

**Transcription A:**
{transcription_a}

**Transcription B:**
{transcription_b}

Consider:
- Do they describe the same visual elements?
- Are labels and annotations equivalent?
- Is the spatial layout described similarly?

Output JSON only: {"score": 0-100, "differences": ["list of semantic differences"]}
"""


def levenshtein_distance(s1: str, s2: str) -> int:
    """Calculate minimum edits to transform s1 into s2."""
    if len(s1) < len(s2):
        s1, s2 = s2, s1
    if not s2:
        return len(s1)
    
    prev_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        curr_row = [i + 1]
        for j, c2 in enumerate(s2):
            cost = 0 if c1 == c2 else 1
            curr_row.append(min(
                curr_row[j] + 1,
                prev_row[j + 1] + 1,
                prev_row[j] + cost
            ))
        prev_row = curr_row
    return prev_row[-1]


def normalized_distance(a: str, b: str) -> float:
    """Return 0.0 (identical) to 1.0 (completely different)."""
    if not a and not b:
        return 0.0
    max_len = max(len(a), len(b))
    return levenshtein_distance(a, b) / max_len


def similarity(a: str, b: str) -> float:
    """Return 1.0 (identical) to 0.0 (completely different)."""
    return 1.0 - normalized_distance(a, b)


def count_diff_lines(a: str, b: str) -> int:
    """Count lines that differ between two texts."""
    lines_a = a.splitlines()
    lines_b = b.splitlines()
    max_lines = max(len(lines_a), len(lines_b))
    diff_count = abs(len(lines_a) - len(lines_b))
    
    for i in range(min(len(lines_a), len(lines_b))):
        if lines_a[i] != lines_b[i]:
            diff_count += 1
    
    return diff_count


def extract_source_name(filename: str) -> str:
    """Extract source file name from output filename for grouping."""
    match = re.match(r'^(.+?)_processed_', filename)
    if match:
        return match.group(1)
    match = re.match(r'^(.+?)_run\d+', filename)
    if match:
        return match.group(1)
    return filename


def compare_files(file_paths: list[Path]) -> dict:
    """Compare multiple files and return metrics."""
    contents = {}
    for fp in file_paths:
        try:
            contents[fp.name] = fp.read_text(encoding='utf-8')
        except Exception as e:
            print(f"[WARN] Could not read {fp}: {e}", file=sys.stderr)
    
    if len(contents) < 2:
        return {"error": "Need at least 2 files to compare"}
    
    names = list(contents.keys())
    texts = list(contents.values())
    
    exact_match = all(t == texts[0] for t in texts[1:])
    
    pairwise = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            dist = normalized_distance(texts[i], texts[j])
            diff_lines = count_diff_lines(texts[i], texts[j])
            pairwise.append({
                "a": names[i],
                "b": names[j],
                "distance": round(dist, 4),
                "similarity": round(1 - dist, 4),
                "diff_lines": diff_lines
            })
    
    avg_similarity = sum(p["similarity"] for p in pairwise) / len(pairwise) if pairwise else 1.0
    max_distance = max(p["distance"] for p in pairwise) if pairwise else 0.0
    
    return {
        "files": names,
        "exact_match": exact_match,
        "pairwise": pairwise,
        "avg_similarity": round(avg_similarity, 4),
        "max_distance": round(max_distance, 4)
    }


def group_by_source(files: list[Path]) -> dict[str, list[Path]]:
    """Group files by their source name."""
    groups = {}
    for fp in files:
        source = extract_source_name(fp.name)
        if source not in groups:
            groups[source] = []
        groups[source].append(fp)
    return groups


def extract_sections(content: str) -> dict:
    """Split content into text and image sections."""
    pattern = r'<transcription_image>(.*?)</transcription_image>'
    images = re.findall(pattern, content, re.DOTALL)
    text = re.sub(pattern, '', content, flags=re.DOTALL)
    return {"text": text.strip(), "images": images}


def load_api_keys(keys_file: Path) -> dict:
    """Load API keys from file."""
    keys = {}
    if not keys_file.exists():
        return keys
    with open(keys_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, value = line.split('=', 1)
                keys[key.strip()] = value.strip()
    return keys


def call_judge_llm(prompt: str, model: str, keys: dict, script_dir: Path) -> dict:
    """Call LLM to judge similarity. Returns score and usage."""
    provider = 'anthropic' if model.startswith('claude') else 'openai'
    
    try:
        if provider == 'openai':
            from openai import OpenAI
            client = OpenAI(api_key=keys.get('OPENAI_API_KEY'))
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.0
            )
            text = response.choices[0].message.content
            usage = {"input_tokens": response.usage.prompt_tokens, "output_tokens": response.usage.completion_tokens}
        else:
            from anthropic import Anthropic
            client = Anthropic(api_key=keys.get('ANTHROPIC_API_KEY'))
            response = client.messages.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.0
            )
            text = response.content[0].text if hasattr(response.content[0], 'text') else ""
            usage = {"input_tokens": response.usage.input_tokens, "output_tokens": response.usage.output_tokens}
        
        # Parse JSON from response
        json_match = re.search(r'\{[^{}]*\}', text)
        if json_match:
            result = json.loads(json_match.group())
            result["usage"] = usage
            return result
        return {"score": 50, "differences": ["Could not parse response"], "usage": usage}
    except Exception as e:
        print(f"[WARN] LLM judge error: {e}", file=sys.stderr)
        return {"score": 0, "differences": [str(e)], "usage": {"input_tokens": 0, "output_tokens": 0}}


def compare_images_with_llm(images_a: list, images_b: list, model: str, keys: dict, 
                            judge_prompt: str, script_dir: Path) -> dict:
    """Compare image sections using LLM judge."""
    if not images_a or not images_b:
        return {"avg_similarity": 1.0, "figures": [], "usage": {"input_tokens": 0, "output_tokens": 0, "calls": 0}}
    
    figures = []
    total_input = 0
    total_output = 0
    calls = 0
    
    for i, (img_a, img_b) in enumerate(zip(images_a, images_b)):
        prompt = judge_prompt.format(transcription_a=img_a, transcription_b=img_b)
        result = call_judge_llm(prompt, model, keys, script_dir)
        
        figures.append({
            "figure": f"Figure {i+1}",
            "score": result.get("score", 0) / 100.0,
            "differences": result.get("differences", [])
        })
        total_input += result.get("usage", {}).get("input_tokens", 0)
        total_output += result.get("usage", {}).get("output_tokens", 0)
        calls += 1
    
    avg_score = sum(f["score"] for f in figures) / len(figures) if figures else 1.0
    
    return {
        "avg_similarity": round(avg_score, 4),
        "figures": figures,
        "usage": {"input_tokens": total_input, "output_tokens": total_output, "calls": calls}
    }


def parse_args():
    parser = argparse.ArgumentParser(
        description='Compare transcription output files with Levenshtein or LLM-as-a-judge.',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--input-folder', type=Path, help='Folder with output files')
    parser.add_argument('--files', type=Path, nargs='+', help='Explicit list of files')
    parser.add_argument('--output-file', type=Path, required=True, help='JSON output file')
    parser.add_argument('--group-by-input', action='store_true', help='Group by source input')
    parser.add_argument('--baseline', type=Path, help='Baseline file for comparison')
    parser.add_argument('--method', choices=['levenshtein', 'semantic', 'hybrid'], default='levenshtein',
                        help='Comparison method (default: levenshtein)')
    parser.add_argument('--judge-model', type=str, help='Model for semantic/hybrid comparison')
    parser.add_argument('--judge-prompt', type=Path, help='Custom judge prompt file')
    parser.add_argument('--keys-file', type=Path, default=Path('.env'), help='API keys file')
    parser.add_argument('--temperature', choices=EFFORT_LEVELS, default='medium', help='Judge temperature')
    parser.add_argument('--reasoning-effort', choices=EFFORT_LEVELS, default='medium', help='Judge reasoning effort')
    parser.add_argument('--output-length', choices=EFFORT_LEVELS, default='none', help='Judge output length')
    return parser.parse_args()


def main():
    args = parse_args()
    script_dir = Path(__file__).parent
    
    if args.input_folder and args.files:
        print("[ERROR] Use --input-folder OR --files, not both", file=sys.stderr)
        sys.exit(1)
    
    if not args.input_folder and not args.files:
        print("[ERROR] Must specify --input-folder or --files", file=sys.stderr)
        sys.exit(1)
    
    if args.method in ['semantic', 'hybrid'] and not args.judge_model:
        print("[ERROR] --judge-model required for semantic/hybrid comparison", file=sys.stderr)
        sys.exit(1)
    
    # Load judge prompt if custom
    judge_prompt = DEFAULT_JUDGE_PROMPT
    if args.judge_prompt and args.judge_prompt.exists():
        judge_prompt = args.judge_prompt.read_text(encoding='utf-8')
    
    # Load API keys for LLM judge
    keys = {}
    if args.method in ['semantic', 'hybrid']:
        keys = load_api_keys(args.keys_file)
        if not keys:
            print(f"[WARN] No API keys loaded from {args.keys_file}", file=sys.stderr)
    
    if args.input_folder:
        if not args.input_folder.exists():
            print(f"[ERROR] Folder not found: {args.input_folder}", file=sys.stderr)
            sys.exit(1)
        files = [f for f in args.input_folder.iterdir() 
                 if f.is_file() and f.suffix.lower() in {'.md', '.txt'}
                 and not f.name.startswith('_')]
    else:
        files = [f for f in args.files if f.exists()]
        missing = [f for f in args.files if not f.exists()]
        if missing:
            print(f"[WARN] Files not found: {missing}", file=sys.stderr)
    
    if len(files) < 2:
        print(f"[ERROR] Need at least 2 files, found {len(files)}", file=sys.stderr)
        sys.exit(1)
    
    files.sort()
    
    # Build input_files list
    input_files = [{"path": str(f), "size_bytes": f.stat().st_size} for f in files]
    
    # Track total judge usage
    total_judge_usage = {"model": args.judge_model, "total_input_tokens": 0, "total_output_tokens": 0, "calls": 0}
    
    if args.group_by_input:
        groups = group_by_source(files)
        comparisons = []
        for source, group_files in groups.items():
            if len(group_files) >= 2:
                result = compare_files(group_files)
                result["group"] = source
                
                # Hybrid comparison: split text and images
                if args.method == 'hybrid':
                    contents = [f.read_text(encoding='utf-8') for f in group_files]
                    sections = [extract_sections(c) for c in contents]
                    
                    # Check if any images found
                    has_images = any(s["images"] for s in sections)
                    if not has_images:
                        print(f"[WARN] No <transcription_image> tags in group {source}, using levenshtein", file=sys.stderr)
                    else:
                        # Compare text with levenshtein
                        text_similarities = []
                        for i in range(len(sections)):
                            for j in range(i + 1, len(sections)):
                                text_similarities.append(similarity(sections[i]["text"], sections[j]["text"]))
                        result["text"] = {
                            "method": "levenshtein",
                            "avg_similarity": round(sum(text_similarities) / len(text_similarities), 4) if text_similarities else 1.0
                        }
                        
                        # Compare images with LLM judge
                        if len(sections) >= 2 and sections[0]["images"] and sections[1]["images"]:
                            img_result = compare_images_with_llm(
                                sections[0]["images"], sections[1]["images"],
                                args.judge_model, keys, judge_prompt, script_dir
                            )
                            result["images"] = {
                                "method": "llm-judge",
                                "model": args.judge_model,
                                "avg_similarity": img_result["avg_similarity"],
                                "figures": img_result["figures"],
                                "usage": img_result["usage"]
                            }
                            total_judge_usage["total_input_tokens"] += img_result["usage"]["input_tokens"]
                            total_judge_usage["total_output_tokens"] += img_result["usage"]["output_tokens"]
                            total_judge_usage["calls"] += img_result["usage"]["calls"]
                
                comparisons.append(result)
        
        total_files = sum(len(c.get("files", [])) for c in comparisons)
        exact_matches = sum(1 for c in comparisons if c.get("exact_match", False))
        avg_similarities = [c["avg_similarity"] for c in comparisons if "avg_similarity" in c]
        max_distances = [c["max_distance"] for c in comparisons if "max_distance" in c]
        
        report = {
            "summary": {
                "method": args.method,
                "total_groups": len(comparisons),
                "total_files": total_files,
                "exact_matches": exact_matches,
                "avg_similarity": round(sum(avg_similarities) / len(avg_similarities), 4) if avg_similarities else 1.0,
                "max_distance": round(max(max_distances), 4) if max_distances else 0.0
            },
            "input_files": input_files,
            "comparisons": comparisons,
            "generated": datetime.now(timezone.utc).isoformat()
        }
        if args.method in ['semantic', 'hybrid'] and total_judge_usage["calls"] > 0:
            report["summary"]["judge_usage"] = total_judge_usage
    else:
        result = compare_files(files)
        report = {
            "summary": {
                "method": args.method,
                "total_files": len(result.get("files", [])),
                "exact_match": result.get("exact_match", False),
                "avg_similarity": result.get("avg_similarity", 1.0),
                "max_distance": result.get("max_distance", 0.0)
            },
            "input_files": input_files,
            "comparison": result,
            "generated": datetime.now(timezone.utc).isoformat()
        }
    
    args.output_file.parent.mkdir(parents=True, exist_ok=True)
    args.output_file.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(f"Report written to: {args.output_file}", file=sys.stderr)
    
    if "summary" in report:
        s = report["summary"]
        print(f"Summary: {s.get('total_files', 0)} files, avg similarity: {s.get('avg_similarity', 0):.2%}", file=sys.stderr)


if __name__ == '__main__':
    main()
