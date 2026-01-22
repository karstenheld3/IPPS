"""Analyze evaluation results: quality, variability, cost-effectiveness."""

import json
from pathlib import Path
from collections import defaultdict
import statistics

EVAL_DIR = Path(r"E:\Dev\IPPS\_PrivateSessions\_2026-01-22_OptimizeAsciiArtTranscription\_CostQualityEval")
SCORES_DIR = EVAL_DIR / "scores"

COSTS = {
    "Claude_Opus_4": 0.111,
    "Claude_Haiku_3_5": 0.004,
    "Claude_Sonnet_4": 0.024,
    "GPT-5-mini": 0.017,
    "GPT_5": 0.100,
    "GPT_4_1": 0.045,
    "GPT_4o": 0.038,
    "GPT_5_2": 0.047,
}

def load_scores(model_folder: Path) -> list:
    scores_file = model_folder / "scores_gpt-5.json"
    if not scores_file.exists():
        return []
    with open(scores_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("scores", [])

def analyze_by_run(scores: list) -> dict:
    """Group scores by run number and calculate per-run stats."""
    by_run = defaultdict(list)
    for item in scores:
        source = item.get("source_file", "")
        for run in ["run01", "run02", "run03"]:
            if run in source:
                by_run[run].append(item["score"])
                break
    
    run_stats = {}
    for run, run_scores in sorted(by_run.items()):
        run_stats[run] = {
            "count": len(run_scores),
            "avg": statistics.mean(run_scores) if run_scores else 0,
            "stdev": statistics.stdev(run_scores) if len(run_scores) > 1 else 0
        }
    return run_stats

def analyze_by_image(scores: list) -> dict:
    """Group scores by image and calculate variability."""
    by_image = defaultdict(list)
    for item in scores:
        source = item.get("source_file", "")
        image_id = source.rsplit("_run", 1)[0] if "_run" in source else source
        by_image[image_id].append(item["score"])
    
    image_stats = {}
    for image, img_scores in by_image.items():
        image_stats[image] = {
            "scores": img_scores,
            "avg": statistics.mean(img_scores) if img_scores else 0,
            "stdev": statistics.stdev(img_scores) if len(img_scores) > 1 else 0,
            "min": min(img_scores) if img_scores else 0,
            "max": max(img_scores) if img_scores else 0,
        }
    return image_stats

def best_of_3(scores: list) -> float:
    """Simulate selecting best transcription out of 3 runs."""
    by_image = defaultdict(list)
    for item in scores:
        source = item.get("source_file", "")
        image_id = source.rsplit("_run", 1)[0] if "_run" in source else source
        by_image[image_id].append(item["score"])
    
    best_scores = []
    for image, img_scores in by_image.items():
        if img_scores:
            best_scores.append(max(img_scores))
    
    return statistics.mean(best_scores) if best_scores else 0

def main():
    print("=" * 60)
    print("TRANSCRIPTION MODEL COST/QUALITY ANALYSIS")
    print("=" * 60)
    
    results = {}
    
    for model in ["Claude_Opus_4", "Claude_Haiku_3_5", "Claude_Sonnet_4", "GPT-5-mini", "GPT_5", "GPT_4_1", "GPT_4o", "GPT_5_2"]:
        model_dir = SCORES_DIR / model
        scores = load_scores(model_dir)
        
        if not scores:
            print(f"\n{model}: No scores found")
            continue
        
        all_scores = [s["score"] for s in scores]
        avg = statistics.mean(all_scores)
        passed = sum(1 for s in all_scores if s >= 4)
        pass_rate = passed / len(all_scores) * 100
        
        image_stats = analyze_by_image(scores)
        
        cost = COSTS[model]
        quality_per_dollar = avg / cost
        
        by_category = defaultdict(list)
        for s in scores:
            by_category[s.get("category", "unknown")].append(s["score"])
        
        results[model] = {
            "avg_score": avg,
            "pass_rate": pass_rate,
            "cost": cost,
            "quality_per_dollar": quality_per_dollar,
            "by_category": {k: statistics.mean(v) for k, v in by_category.items()},
        }
        
        print(f"\n{'='*60}")
        print(f"{model}")
        print(f"{'='*60}")
        print(f"  Average Score: {avg:.2f}/5")
        print(f"  Pass Rate: {pass_rate:.1f}%")
        print(f"  Cost per Image: ${cost:.3f}")
        print(f"  Quality per $1: {quality_per_dollar:.1f} points")
        
        print(f"\n  By Category:")
        for cat, cat_scores in sorted(by_category.items()):
            cat_avg = statistics.mean(cat_scores)
            print(f"    {cat}: {cat_avg:.2f}/5")
        
        print(f"\n  Per-Image Scores:")
        for image, stats in image_stats.items():
            short_name = image[:40] + "..." if len(image) > 40 else image
            print(f"    {short_name}: {stats['avg']:.2f}/5")
    
    print(f"\n{'='*60}")
    print("SUMMARY RANKING")
    print(f"{'='*60}")
    
    ranked = sorted(results.items(), key=lambda x: x[1]["avg_score"], reverse=True)
    print("\nBy Quality:")
    for i, (model, data) in enumerate(ranked, 1):
        print(f"  {i}. {model}: {data['avg_score']:.2f}/5 (${data['cost']:.3f}/img)")
    
    ranked_value = sorted(results.items(), key=lambda x: x[1]["quality_per_dollar"], reverse=True)
    print("\nBy Value (Quality per $):")
    for i, (model, data) in enumerate(ranked_value, 1):
        print(f"  {i}. {model}: {data['quality_per_dollar']:.1f} pts/$ (avg={data['avg_score']:.2f})")
    
    output_file = EVAL_DIR / "analysis_results.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to: {output_file}")

if __name__ == "__main__":
    main()
