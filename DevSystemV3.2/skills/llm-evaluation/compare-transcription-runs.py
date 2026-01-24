#!/usr/bin/env python3
"""
compare-outputs.py - Compare LLM output files using Levenshtein distance.

Usage:
  python compare-outputs.py --input-folder outputs/ --output-file comparison.json
  python compare-outputs.py --files output1.md output2.md --output-file comparison.json
"""

import sys, json, argparse, re
from pathlib import Path
from datetime import datetime, timezone


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


def parse_args():
    parser = argparse.ArgumentParser(
        description='Compare LLM output files using Levenshtein distance.',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--input-folder', type=Path, help='Folder with output files')
    parser.add_argument('--files', type=Path, nargs='+', help='Explicit list of files')
    parser.add_argument('--output-file', type=Path, required=True, help='JSON output file')
    parser.add_argument('--group-by-input', action='store_true', help='Group by source input')
    parser.add_argument('--baseline', type=Path, help='Baseline file for comparison')
    return parser.parse_args()


def main():
    args = parse_args()
    
    if args.input_folder and args.files:
        print("[ERROR] Use --input-folder OR --files, not both", file=sys.stderr)
        sys.exit(1)
    
    if not args.input_folder and not args.files:
        print("[ERROR] Must specify --input-folder or --files", file=sys.stderr)
        sys.exit(1)
    
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
    
    if args.group_by_input:
        groups = group_by_source(files)
        comparisons = []
        for source, group_files in groups.items():
            if len(group_files) >= 2:
                result = compare_files(group_files)
                result["group"] = source
                comparisons.append(result)
        
        total_files = sum(len(c.get("files", [])) for c in comparisons)
        exact_matches = sum(1 for c in comparisons if c.get("exact_match", False))
        avg_similarities = [c["avg_similarity"] for c in comparisons if "avg_similarity" in c]
        max_distances = [c["max_distance"] for c in comparisons if "max_distance" in c]
        
        report = {
            "summary": {
                "total_groups": len(comparisons),
                "total_files": total_files,
                "exact_matches": exact_matches,
                "avg_similarity": round(sum(avg_similarities) / len(avg_similarities), 4) if avg_similarities else 1.0,
                "max_distance": round(max(max_distances), 4) if max_distances else 0.0
            },
            "comparisons": comparisons,
            "generated": datetime.now(timezone.utc).isoformat()
        }
    else:
        result = compare_files(files)
        report = {
            "summary": {
                "total_files": len(result.get("files", [])),
                "exact_match": result.get("exact_match", False),
                "avg_similarity": result.get("avg_similarity", 1.0),
                "max_distance": result.get("max_distance", 0.0)
            },
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
