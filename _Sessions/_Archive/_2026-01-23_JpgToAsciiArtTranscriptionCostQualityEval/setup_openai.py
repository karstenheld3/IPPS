"""Setup script for OpenAI models - copies transcriptions for GPT-5, GPT-4.1, GPT-4o."""

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
    ("GPT-5", "GPT_5"),
    ("GPT-4_1", "GPT_4_1"),
    ("GPT-4o", "GPT_4o"),
]

RUNS = ["run01", "run02", "run03"]

def copy_transcriptions():
    """Copy selected transcriptions to eval folder."""
    trans_dir = EVAL_DIR / "transcriptions"
    
    for src_name, dst_name in MODELS:
        model_src = OUTPUTS_DIR / src_name
        model_dst = trans_dir / dst_name
        model_dst.mkdir(parents=True, exist_ok=True)
        
        count = 0
        for image in SELECTED_IMAGES:
            for run in RUNS:
                src_file = model_src / f"{image}_{run}.md"
                if src_file.exists():
                    dst_file = model_dst / f"{image}_{run}.md"
                    shutil.copy2(src_file, dst_file)
                    count += 1
                else:
                    print(f"MISSING: {src_name}/{image}_{run}.md")
        
        print(f"{dst_name}: Copied {count} files")

if __name__ == "__main__":
    print("=== Copying OpenAI model transcriptions ===")
    copy_transcriptions()
    print("=== Done ===")
