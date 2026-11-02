#!/usr/bin/env python3
"""
match-epoch-eci.py - Download the Epoch ECI CSV and match every registry model to its score and 95% interval (MDLRGUP-MDLINVNTRY-SP01 FR-06).

Output [DATE]_Epoch-ECI-Match.json:
  matches[]           one entry per registry text model: model_id, epoch_name, eci_score, eci_ci_low, eci_ci_high (null without an Epoch row)
  unmatched[]         registry model IDs without an Epoch row (eci_ci null in the registry)
  new_models[]        model IDs found in [DATE]_*-DOM.json of the run folder but absent from the registry (candidates for Prompts 4 and 5)
  missing_metadata[]  registry models without uc_class or release_date (complete from the vendor model overview)
No band, no generation equivalent, no class inference: uc_class and release_date are hand-maintained registry inputs.

Usage:
  python match-epoch-eci.py --run-folder <path> --date <YYYY-MM-DD> --registry-file <path> [--download]
"""

import argparse, csv, json, re, sys, urllib.request
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
  sys.stdout.reconfigure(encoding="utf-8", errors="replace")
  sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ECI_CSV_URL = "https://epoch.ai/data/eci_scores.csv"
NON_TEXT = {"computer-use-preview", "gpt-image-1.5"}
MODEL_ID_PATTERN = re.compile(r"^(claude|gpt|o\d|gemini|glm|grok)[-a-z0-9.]*$")
SKIPPED_DOM_PATHS = ("shut_down", "retired", "specialized_endpoints")

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
  "glm-5.3-flash": "GLM-5.3-Flash",
  "grok-4.3": "Grok 4.3 Beta",
  "grok-4.20-0309-reasoning": "Grok 4.20",
  "grok-4.20-multi-agent-0309": "Grok 4.20"
}

def base_id(model_id):
  return re.sub(r"-\d{8}$", "", model_id)

def to_float(value):
  return float(value) if value not in (None, "") else None

def download_csv(csv_path: Path, url: str = ECI_CSV_URL) -> bool:
  req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
  with urllib.request.urlopen(req, timeout=45) as resp:
    data = resp.read()
  csv_path.write_bytes(data)
  retVal = csv_path.exists() and csv_path.stat().st_size > 1000
  return retVal

# Collect model-ID-like strings from every DOM extract of the run; display names such as "GLM-5.3 Flash" are normalized to "glm-5.3-flash"
def collect_dom_model_ids(run_folder: Path, date: str) -> list:
  found = {}
  pending = []
  for dom_file in sorted(run_folder.glob(f"{date}_*-DOM.json")):
    pending.append((json.loads(dom_file.read_text(encoding="utf-8")), ""))
  while pending:
    node, path = pending.pop()
    if isinstance(node, dict):
      for key, value in node.items():
        pending.append((value, path + "." + str(key).lower()))
    elif isinstance(node, list):
      for value in node:
        pending.append((value, path))
    elif isinstance(node, str):
      skipped = False
      for marker in SKIPPED_DOM_PATHS:
        if marker in path: skipped = True
      candidate = node.strip()
      if candidate.upper().startswith("GLM-") or candidate.startswith("Grok "): candidate = candidate.lower().replace(" ", "-")
      if not skipped and MODEL_ID_PATTERN.match(candidate): found[candidate] = True
  return sorted(found.keys())

def match_models(csv_path: Path, reg_path: Path, out_path: Path, run_folder: Path, snapshot_date: str) -> dict:
  with csv_path.open("r", encoding="utf-8", newline="") as handle:
    csv_rows = list(csv.DictReader(handle))
  by_name, by_lower = {}, {}
  for row in csv_rows:
    name = row["Model"].strip()
    by_name[name] = row
    by_lower[name.lower()] = row
    by_lower[name.lower().replace("-", " ")] = row
  reg = json.loads(reg_path.read_text(encoding="utf-8"))
  matches, unmatched_ids, missing_metadata = [], [], []
  registry_ids = {}
  for model in reg["models"]:
    registry_ids[model["model_id"]] = True
    registry_ids[base_id(model["model_id"])] = True
    mid = model["model_id"]
    if mid in NON_TEXT or model.get("status") == "retired": continue
    display_name = model.get("name", mid)
    csv_row = None
    if mid in ExplicitNameMap and ExplicitNameMap[mid] in by_name: csv_row = by_name[ExplicitNameMap[mid]]
    elif display_name in by_name: csv_row = by_name[display_name]
    elif display_name.lower() in by_lower: csv_row = by_lower[display_name.lower()]
    elif mid.lower() in by_lower: csv_row = by_lower[mid.lower()]
    entry = {"provider": model["provider"], "model_id": mid, "name": display_name, "epoch_name": None, "eci_score": None, "eci_ci_low": None, "eci_ci_high": None}
    if csv_row and csv_row.get("eci"):
      entry.update({"epoch_name": csv_row["Model"].strip(), "eci_score": to_float(csv_row["eci"]), "eci_ci_low": to_float(csv_row.get("eci_ci_low")), "eci_ci_high": to_float(csv_row.get("eci_ci_high"))})
      entry["release_date_in_eci"] = csv_row.get("date") or None
    else:
      unmatched_ids.append(mid)
    matches.append(entry)
    missing = []
    for field in ("uc_class", "release_date"):
      if not model.get(field): missing.append(field)
    if missing: missing_metadata.append({"model_id": mid, "missing": missing})
  new_models = []
  for candidate in collect_dom_model_ids(run_folder, snapshot_date):
    if candidate not in registry_ids and base_id(candidate) not in registry_ids: new_models.append(candidate)
  retVal = {
    "_source": str(csv_path), "_url": "https://epoch.ai/eci", "_direct_csv_url": ECI_CSV_URL, "_snapshot_date": snapshot_date,
    "_total_csv_models": len(csv_rows), "_total_models_evaluated": len(matches), "_matched_with_eci_score": len(matches) - len(unmatched_ids),
    "unmatched": unmatched_ids, "new_models": new_models, "missing_metadata": missing_metadata, "matches": matches
  }
  out_path.write_text(json.dumps(retVal, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
  return retVal

def main():
  parser = argparse.ArgumentParser(description="Download Epoch ECI CSV and match registry models to score and 95% interval")
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
      print(f"WARNING: Download failed ({exc}); using existing {csv_path}", file=sys.stderr)
  result = match_models(csv_path, args.registry_file, out_path, args.run_folder, args.date)
  with_interval = 0
  for entry in result["matches"]:
    if entry["eci_ci_low"] is not None: with_interval += 1
  print(f"Matched {result['_matched_with_eci_score']} / {result['_total_models_evaluated']} registry models ({with_interval} with interval, {len(result['unmatched'])} unmatched).")
  print(f"New model candidates in DOM: {len(result['new_models'])}" + (f" ({', '.join(result['new_models'])})" if result["new_models"] else ""))
  print(f"Registry models missing uc_class or release_date: {len(result['missing_metadata'])}")
  print(f"OK: {out_path}")

if __name__ == "__main__":
  main()
