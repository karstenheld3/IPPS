#!/usr/bin/env python3
"""
match-epoch-eci.py - Download Epoch ECI CSV and match inventory models to ECI bands, Universal Classes, and Generation Equivalents.

Band freeze (MODEL_INVENTORY.md R2): a band read from Epoch is never replaced. band_action per match: "set" (no band yet), "replace_fallback" (registry band came from eci_band_source), "keep" (Epoch band exists; new score reported only).

Usage:
  python match-epoch-eci.py --run-folder <path> --date <YYYY-MM-DD> --registry-file <path> [--download]
"""

import argparse
import csv
import json
import sys
import urllib.request
from pathlib import Path

ECI_CSV_URL = "https://epoch.ai/data/eci_scores.csv"

REFERENCE_UC12_MODELS = [
  "Claude Opus 5.5", "GPT-6 Astra", "GPT-6.1 Sol", "Claude Fable 5.1", "Gemini 4 Argon",
  "Claude Opus 5", "GPT-6 Sol", "Claude Fable 5", "GPT-5.6 Sol", "GPT-5.5",
  "Claude Opus 4.8", "GPT-5.4", "Claude Opus 4.7", "Claude Opus 4.6", "Gemini 3.1 Pro",
  "GPT-5.2", "Gemini 3 Pro", "Claude Opus 4.5", "GPT-5", "GPT-5.1",
  "o3", "Gemini 2.5 Pro (Jun 2025)", "Claude Opus 4.1", "Claude Opus 4", "o1",
  "GPT-4.1", "Claude 3.5 Sonnet (October 2024)", "Claude 3.5 Sonnet", "GPT-4o (May 2024)", "Claude 3 Opus"
]

ExplicitNameMap = {
  "gpt-5-mini": "GPT-5 mini",
  "gpt-5-nano": "GPT-5 nano",
  "gpt-4.1-mini": "GPT-4.1 mini",
  "gpt-4.1-nano": "GPT-4.1 nano",
  "gpt-4o": "GPT-4o (May 2024)",
  "gpt-4o-2024-05-13": "GPT-4o (May 2024)",
  "gpt-4o-mini": "GPT-4o mini",
  "o1": "o1",
  "o1-mini": "o1-mini",
  "o3": "o3",
  "o3-pro": "o3-pro",
  "o3-mini": "o3-mini",
  "o4-mini": "o4-mini",
  "claude-opus-4-5-20251101": "Claude Opus 4.5",
  "claude-opus-4-1-20250805": "Claude Opus 4.1",
  "claude-sonnet-4-5-20250929": "Claude Sonnet 4.5",
  "claude-haiku-4-5-20251001": "Claude Haiku 4.5",
  "claude-opus-4-20250514": "Claude Opus 4",
  "claude-sonnet-4-20250514": "Claude Sonnet 4",
  "claude-3-7-sonnet-20250219": "Claude 3.7 Sonnet",
  "claude-3-5-sonnet-20241022": "Claude 3.5 Sonnet (October 2024)",
  "claude-3-5-haiku-20241022": "Claude 3.5 Haiku",
  "claude-3-haiku-20240307": "Claude 3 Haiku",
  "gemini-3.1-pro-preview": "Gemini 3.1 Pro",
  "gemini-3-flash-preview": "Gemini 3 Flash",
  "gemini-2.5-pro": "Gemini 2.5 Pro (Jun 2025)",
  "gemini-2.5-flash": "Gemini 2.5 Flash (Sep 2025)",
  "gemini-2.5-flash-lite": "Gemini 2.5 Flash-Lite (Jun 2025)",
  "glm-5.3-flash": "GLM-5.3-Flash"
}

def infer_uc_class(model_id: str, existing_uc: str = None) -> str:
  if existing_uc:
    return existing_uc
  mid = model_id.lower()
  if any(k in mid for k in ("astra", "fable", "mythos", "-pro", "cyber", "deep-research")) and not mid.startswith("gemini-"):
    return "UC-1 Apex"
  if any(k in mid for k in ("opus", "-sol", "argon", "gemini-3.1-pro", "gemini-2.5-pro", "codex", "glm-5.3", "glm-5.2", "glm-5.1", "glm-4.7", "glm-4.6", "glm-4.5-x")) and "flash" not in mid:
    return "UC-2 Flagship"
  if mid in ("gpt-5.5", "gpt-5.4", "gpt-5.2", "gpt-5.1", "gpt-5", "gpt-4.1", "gpt-4o", "gpt-4o-2024-05-13", "o1", "o3", "glm-5", "glm-4.5"):
    return "UC-2 Flagship"
  if any(k in mid for k in ("sonnet", "terra", "-mini", "flash-lite", "haiku", "luna", "-nano", "air")):
    if any(k in mid for k in ("haiku", "luna", "-nano", "flash-lite", "glm-4.7-flash", "glm-4.5-flash", "glm-4-air")):
      return "UC-4 Efficient"
    return "UC-3 Balanced"
  if "flash" in mid or "4.6v" in mid or "4.5v" in mid:
    return "UC-3 Balanced"
  return "UC-3 Balanced"

def round_band(score: float) -> str:
  retVal = f"E{int(round(score / 5.0) * 5)}"
  return retVal

def download_csv(csv_path: Path, url: str = ECI_CSV_URL) -> bool:
  req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
  with urllib.request.urlopen(req, timeout=45) as resp:
    data = resp.read()
  csv_path.write_bytes(data)
  retVal = csv_path.exists() and csv_path.stat().st_size > 1000
  return retVal

def match_models(csv_path: Path, reg_path: Path, out_path: Path, snapshot_date: str) -> dict:
  with csv_path.open("r", encoding="utf-8") as f:
    csv_rows = list(csv.DictReader(f))

  by_name = {}
  by_lower = {}
  for r in csv_rows:
    m = r["Model"].strip()
    by_name[m] = r
    by_lower[m.lower()] = r
    by_lower[m.lower().replace("-", " ")] = r

  ref_ladder = []
  for rn in REFERENCE_UC12_MODELS:
    if rn in by_name and by_name[rn].get("eci"):
      score = float(by_name[rn]["eci"])
      clean_label = rn.replace(" (Jun 2025)", "").replace(" (October 2024)", "").replace(" (May 2024)", "")
      ref_ladder.append((score, clean_label))
  ref_ladder.sort(key=lambda x: x[0], reverse=True)

  def get_gen_equiv(score: float) -> str:
    for ref_score, ref_label in ref_ladder:
      if ref_score <= score + 1e-9:
        return f"≈ {ref_label}"
    return "≈ Claude 3 Opus"

  reg = json.loads(reg_path.read_text(encoding="utf-8"))
  matches = []
  matched_count = 0
  unmatched_ids = []

  for m in reg["models"]:
    mid = m["model_id"]
    provider = m["provider"]
    display_name = m.get("name", mid)
    uc_class = infer_uc_class(mid, m.get("uc_class"))

    # Resolve CSV row
    csv_row = None
    if mid in ExplicitNameMap and ExplicitNameMap[mid] in by_name:
      csv_row = by_name[ExplicitNameMap[mid]]
    elif display_name in by_name:
      csv_row = by_name[display_name]
    elif display_name.lower() in by_lower:
      csv_row = by_lower[display_name.lower()]
    elif mid.lower() in by_lower:
      csv_row = by_lower[mid.lower()]

    if csv_row and csv_row.get("eci"):
      score = float(csv_row["eci"])
      ci_low = float(csv_row["eci_ci_low"]) if csv_row.get("eci_ci_low") else None
      ci_high = float(csv_row["eci_ci_high"]) if csv_row.get("eci_ci_high") else None
      band = round_band(score)
      gen_eq = get_gen_equiv(score)
      matched_count += 1
      existing_band = m.get("eci_band")
      if not existing_band:
        band_action = "set"
      elif m.get("eci_band_source"):
        band_action = "replace_fallback"
      else:
        band_action = "keep"
      matches.append({
        "provider": provider,
        "model_id": mid,
        "name": display_name,
        "uc_class": uc_class,
        "eci_model": csv_row["Model"].strip(),
        "eci_score": score,
        "eci_ci_low": ci_low,
        "eci_ci_high": ci_high,
        "eci_band": band if band_action != "keep" else existing_band,
        "eci_band_new_score": band,
        "band_action": band_action,
        "gen_equivalent": gen_eq,
        "release_date_in_eci": csv_row.get("date") or None,
        "snapshot_date": snapshot_date
      })
    else:
      unmatched_ids.append(mid)
      matches.append({
        "provider": provider,
        "model_id": mid,
        "name": display_name,
        "uc_class": uc_class,
        "eci_model": None,
        "eci_score": None,
        "eci_ci_low": None,
        "eci_ci_high": None,
        "eci_band": None,
        "gen_equivalent": None,
        "fallback_note": f"No Epoch ECI row (<4 benchmarks or specialized/older SKU); use {uc_class} fallback",
        "snapshot_date": snapshot_date
      })

  retVal = {
    "_source": str(csv_path),
    "_url": "https://epoch.ai/eci",
    "_direct_csv_url": ECI_CSV_URL,
    "_snapshot_date": snapshot_date,
    "_total_csv_models": len(csv_rows),
    "_total_models_evaluated": len(matches),
    "_matched_with_eci_score": matched_count,
    "_unmatched_fallback_to_uc": len(unmatched_ids),
    "_unmatched_model_ids": unmatched_ids,
    "matches": matches
  }
  out_path.write_text(json.dumps(retVal, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
  return retVal

def main():
  parser = argparse.ArgumentParser(description="Download Epoch ECI CSV and match registry models")
  parser.add_argument("--run-folder", type=Path, required=True, help="Run folder path")
  parser.add_argument("--date", type=str, required=True, help="Run date YYYY-MM-DD")
  parser.add_argument("--registry-file", type=Path, required=True, help="Path to model-registry.json")
  parser.add_argument("--download", action="store_true", help="Download fresh CSV from epoch.ai")
  args = parser.parse_args()

  csv_path = args.run_folder / f"{args.date}_eci-leaderboard.csv"
  out_path = args.run_folder / f"{args.date}_Epoch-ECI-Match.json"

  if args.download or not csv_path.exists():
    try:
      download_csv(csv_path)
    except Exception as exc:
      if not csv_path.exists():
        print(f"ERROR: Failed to download ECI CSV and no local file exists: {exc}", file=sys.stderr)
        sys.exit(1)
      print(f"WARN: Download failed ({exc}); using existing {csv_path}", file=sys.stderr)

  res = match_models(csv_path, args.registry_file, out_path, args.date)
  print(f"OK: Matched {res['_matched_with_eci_score']}/{res['_total_models_evaluated']} models ({res['_unmatched_fallback_to_uc']} UC fallbacks) -> {out_path}")

if __name__ == "__main__":
  main()
