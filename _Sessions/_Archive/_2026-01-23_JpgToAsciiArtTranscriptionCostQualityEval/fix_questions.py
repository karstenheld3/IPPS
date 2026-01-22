"""Fix questions format to match generate-answers.py expectations."""

import json
from pathlib import Path

EVAL_DIR = Path(r"E:\Dev\IPPS\_PrivateSessions\_2026-01-22_OptimizeAsciiArtTranscription\_CostQualityEval")

def fix_questions():
    input_file = EVAL_DIR / "questions.json"
    
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    flat_questions = []
    for image_id, image_data in data["images"].items():
        for q in image_data["questions"]:
            flat_questions.append({
                "source_file": image_id,
                "question": q["question"],
                "category": q["category"],
                "reference_answer": q["reference_answer"],
                "id": q["id"]
            })
    
    output = {
        "generated": data["generated"],
        "model": data["model"],
        "questions": flat_questions
    }
    
    with open(input_file, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"Fixed {len(flat_questions)} questions")

if __name__ == "__main__":
    fix_questions()
