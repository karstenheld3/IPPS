#!/usr/bin/env python3
"""
Source tier probe for the seo-tools skill. Reports which data tiers are usable right now, so an answer can start with Tier 1, enrich and verify with Tier 2, and probe Tier 3.

Tiers:
  1 FREE          $0 marginal cost: first-party APIs, free quotas, offline checks, manual UI sources
  2 PREPAID       prepaid balance or credits, spent through a cost gate
  3 SUBSCRIPTION  flat-fee tools (Ahrefs, Semrush); no script, probe only

Usage:
  python tiers.py probe
  python tiers.py probe --balances --format json

The probe only checks which keys exist in the keys file and never prints values. `--balances` additionally calls the two $0 balance commands
(`scrapecreators/query.py credit-balance`, `dataforseo/query.py balance`) when their keys exist.
Credentials: names in SKILL.md section "Credential Keys"; Tier 3 keys: AHREFS_API_KEY, SEMRUSH_API_KEY.
"""

import argparse, json, subprocess, sys
from pathlib import Path

SKILL_FOLDER = Path(__file__).resolve().parent
DEFAULT_KEYS_FILE = Path(__file__).resolve().parents[4] / ".tools" / ".api-keys.txt"

TIER_NAMES = {1: "FREE", 2: "PREPAID", 3: "SUBSCRIPTION"}

# (tier, provider, required keys, any-of keys, script or None, balance command or None, note)
PROVIDERS = [
  (1, "agent-readiness", [], [], "agent-readiness/check.py", None, "no key"),
  (1, "prepublish-lint", [], [], "prepublish-lint.py", None, "no key, offline"),
  (1, "google-search-console", ["GSC_SERVICE_ACCOUNT_FILE"], [], "google-search-console/query.py", None, "owned sites only"),
  (1, "bing-webmaster", ["BING_WEBMASTER_API_KEY"], [], "bing-webmaster/query.py", None, "owned sites only"),
  (1, "youtube", ["YOUTUBE_API_KEY"], [], "youtube/query.py", None, "10,000 units per day"),
  (1, "plausible", ["PLAUSIBLE_API_KEY"], [], "plausible/query.py", None, "owned sites only; Cloud needs Business plan"),
  (1, "indexnow", [], ["INDEXNOW_API_KEY"], "indexnow/submit.py", None, "key can be passed with --key"),
  (1, "manual-sources", [], [], None, None, "Google Trends, Pinterest Trends, autocomplete, browser top-10, GSC and Bing UI reports"),
  (2, "trendsmcp", ["TRENDSMCP_API_KEY"], [], "trendsmcp/query.py", None, "credits, 100 free requests per month; no balance command"),
  (2, "scrapecreators", ["SCRAPECREATORS_API_KEY"], [], "scrapecreators/query.py", ["credit-balance"], "credits, cost gate default 20 credits"),
  (2, "dataforseo", ["DATAFORSEO_LOGIN", "DATAFORSEO_PASSWORD"], [], "dataforseo/query.py", ["balance"], "USD balance, cost gate default $0.10"),
  (3, "ahrefs", ["AHREFS_API_KEY"], [], None, None, "no script; vendor REST API, manual calls after unit estimate"),
  (3, "semrush", ["SEMRUSH_API_KEY"], [], None, None, "no script; vendor REST API, manual calls after unit estimate"),
]

# ----------------------------------------- START: Common script contract ------------------------------------------------------

def log(message: str):
  print(message, file=sys.stderr, flush=True)

# Parse KEY=VALUE lines; '#' comments, blank lines, BOM, CRLF, and spaces around '=' are tolerated; a missing file gives no keys
def load_api_keys(keys_file: Path) -> dict:
  retVal = {}
  if not keys_file.is_file(): return retVal
  for raw_line in keys_file.read_text(encoding="utf-8-sig").splitlines():
    line = raw_line.strip()
    if not line or line.startswith("#") or "=" not in line: continue
    key, value = line.split("=", 1)
    retVal[key.strip()] = value.strip()
  return retVal

# ----------------------------------------- END: Common script contract --------------------------------------------------------


# ----------------------------------------- START: Probe -----------------------------------------------------------------------

def provider_status(keys: dict, keys_file: Path, required: list, any_of: list, script: str) -> str:
  retVal = "READY"
  for name in required:
    if not keys.get(name): retVal = "MISSING KEY"
  if any_of and not any(keys.get(name) for name in any_of): retVal = "READY (key via --key)"
  if retVal == "READY" and "GSC_SERVICE_ACCOUNT_FILE" in required and not (keys_file.parent / keys["GSC_SERVICE_ACCOUNT_FILE"]).is_file(): retVal = "MISSING FILE"
  if retVal == "READY" and script is None and required: retVal = "KEY PRESENT (manual vendor calls)"
  return retVal

# Last non-empty stdout line of a free balance command
def read_balance(script: str, command: list, keys_file: Path) -> str:
  arguments = [sys.executable, str(SKILL_FOLDER / script)] + command + ["--keys-file", str(keys_file), "--format", "json"]
  try:
    completed = subprocess.run(arguments, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
  except subprocess.TimeoutExpired:
    return "[TIMEOUT]"
  if completed.returncode != 0: return f"[ERROR exit {completed.returncode}]"
  try:
    data = json.loads(completed.stdout)
  except ValueError:
    return "[UNPARSEABLE]"
  for note in data.get("notes", []):
    if ":" in str(note): return str(note).split(":", 1)[1].strip()
  return "[UNKNOWN]"

def run_probe(args) -> dict:
  keys = load_api_keys(args.keys_file)
  notes = []
  if not args.keys_file.is_file(): notes.append(f"Keys file not found -> '{args.keys_file}' -> keyed providers are reported as missing.")
  rows = []
  for tier, provider, required, any_of, script, balance_command, note in PROVIDERS:
    status = provider_status(keys, args.keys_file, required, any_of, script)
    balance = ""
    if args.balances and balance_command and status == "READY": balance = read_balance(script, balance_command, args.keys_file)
    rows.append({"tier": tier, "tier_name": TIER_NAMES[tier], "provider": provider, "status": status, "balance": balance, "note": note})
  summary = {}
  for tier in [1, 2, 3]:
    ready = []
    for row in rows:
      if row["tier"] == tier and (row["status"].startswith("READY") or row["status"].startswith("KEY PRESENT")): ready.append(row["provider"])
    summary[str(tier)] = ready
    label = f"Tier {tier} {TIER_NAMES[tier]}"
    if ready: notes.append(f"{label}: AVAILABLE -> {', '.join(ready)}")
    else: notes.append(f"{label}: UNAVAILABLE -> skip this tier, record 'Tier {tier} unavailable' in the source ledger")
  return {"rows": rows, "summary": summary, "notes": notes}

# ----------------------------------------- END: Probe -------------------------------------------------------------------------


# ----------------------------------------- START: CLI -------------------------------------------------------------------------

def print_table(rows: list):
  columns = [("Tier", "tier_name", 12), ("Provider", "provider", 22), ("Status", "status", 34), ("Balance", "balance", 14), ("Note", "note", 60)]
  print("  ".join(f"{header:<{width}}" for header, key, width in columns))
  print("  ".join("-" * width for header, key, width in columns))
  for row in rows: print("  ".join(f"{str(row[key])[:width]:<{width}}" for header, key, width in columns))

def build_parser() -> argparse.ArgumentParser:
  parser = argparse.ArgumentParser(description="Source tier probe for the seo-tools skill.", formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__)
  subparsers = parser.add_subparsers(dest="command", required=True)
  probe = subparsers.add_parser("probe", help="Report which tiers and providers are usable")
  probe.add_argument("--keys-file", type=Path, default=DEFAULT_KEYS_FILE, help="Credentials file (default: [WORKSPACE_FOLDER]/../.tools/.api-keys.txt)")
  probe.add_argument("--format", choices=["table", "json"], default="table", help="Output format (default: table)")
  probe.add_argument("--balances", action="store_true", help="Also call the $0 balance commands of ScrapeCreators and DataForSEO")
  return parser

def main():
  args = build_parser().parse_args()
  result = run_probe(args)
  if args.format == "json":
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return
  print_table(result["rows"])
  for note in result["notes"]: print(note)

# ----------------------------------------- END: CLI ---------------------------------------------------------------------------

if __name__ == "__main__":
  main()
