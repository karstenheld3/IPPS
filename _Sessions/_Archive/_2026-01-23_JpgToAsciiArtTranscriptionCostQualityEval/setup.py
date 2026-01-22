"""Setup script for cost/quality evaluation - copies transcriptions and extracts questions."""

import json
import shutil
from pathlib import Path

BASE = Path(r"E:\Dev\IPPS\_PrivateSessions\_2026-01-22_OptimizeAsciiArtTranscription")
EVAL_DIR = BASE / "_CostQualityEval"
OUTPUTS_DIR = BASE / "_ModelComparisonTest" / "outputs"

SELECTED_IMAGES = [
    "Edison-Financial-Report-2023-FY2023-Results_page004",
    "SSE-Annual-Report-2024-Group-Risk-Report_page002",
    "Werner_2016_Stem_Cell_Networks_page014",
    "Microsoft-365-Copilot-Adotion-Playbook_page003",
    "Rent_Prices_Around_the_World_SITE-2",
]

MODELS = [
    "Claude_Opus_4",
    "Claude_Haiku_3_5",
    "Claude_Sonnet_4",
    "GPT-5-mini",
]

RUNS = ["run01", "run02", "run03"]

def copy_transcriptions():
    """Copy selected transcriptions to eval folder."""
    trans_dir = EVAL_DIR / "transcriptions"
    count = 0
    
    for model in MODELS:
        model_src = OUTPUTS_DIR / model
        model_dst = trans_dir / model
        model_dst.mkdir(parents=True, exist_ok=True)
        
        for image in SELECTED_IMAGES:
            for run in RUNS:
                src_file = model_src / f"{image}_{run}.md"
                if src_file.exists():
                    dst_file = model_dst / f"{image}_{run}.md"
                    shutil.copy2(src_file, dst_file)
                    count += 1
                else:
                    print(f"MISSING: {src_file.name}")
    
    print(f"Copied {count} transcription files")

def extract_questions():
    """Extract questions for selected images only."""
    questions_file = BASE / "_ModelComparisonTest" / "evaluation-questions-v2.json"
    
    with open(questions_file, "r", encoding="utf-8") as f:
        all_questions = json.load(f)
    
    subset = {
        "generated": all_questions["generated"],
        "model": all_questions["model"],
        "images": {}
    }
    
    for image in SELECTED_IMAGES:
        if image in all_questions["images"]:
            subset["images"][image] = all_questions["images"][image]
        else:
            print(f"WARNING: No questions for {image}")
    
    output_file = EVAL_DIR / "questions.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(subset, f, indent=2)
    
    total_q = sum(len(img["questions"]) for img in subset["images"].values())
    print(f"Extracted {total_q} questions for {len(subset['images'])} images")

if __name__ == "__main__":
    print("=== Setting up cost/quality evaluation ===")
    copy_transcriptions()
    extract_questions()
    print("=== Setup complete ===")
