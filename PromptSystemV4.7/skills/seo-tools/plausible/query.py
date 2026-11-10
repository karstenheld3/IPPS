#!/usr/bin/env python3
"""
Plausible Analytics Stats API v2 CLI. Free on self-hosted Community Edition; Cloud requires the Business plan.

Usage:
  python query.py summary example.com
  python query.py top-pages example.com --range 30d --limit 20
  python query.py sources example.com
  python query.py goals example.com
  python query.py raw example.com --query-file query.json

Credentials: PLAUSIBLE_API_KEY (required), PLAUSIBLE_BASE_URL (optional, default https://plausible.io) in [API_KEYS_FILE].
"""

import argparse, json, sys, time
from pathlib import Path

import requests

SCRIPT_NAME = "plausible"
SETUP_HINT = "plausible/SETUP.md"
DEFAULT_KEYS_FILE = Path(__file__).resolve().parents[5] / ".tools" / ".api-keys.txt"
DEFAULT_BASE_URL = "https://plausible.io"

PRESETS = {
  "summary": {"metrics": ["visitors", "pageviews", "bounce_rate", "visit_duration"], "dimensions": []},
  "top-pages": {"metrics": ["visitors", "pageviews"], "dimensions": ["event:page"], "order_by": [["visitors", "desc"]]},
  "sources": {"metrics": ["visitors"], "dimensions": ["visit:source"], "order_by": [["visitors", "desc"]]},
  "goals": {"metrics": ["visitors", "events"], "dimensions": ["event:goal"], "order_by": [["visitors", "desc"]]},
}

# ----------------------------------------- START: Common script contract ------------------------------------------------------

def log(message: str):
  print(message, file=sys.stderr, flush=True)

def fail(message: str, exit_code: int):
  log(f"ERROR: {message}")
  sys.exit(exit_code)

# Parse KEY=VALUE lines; '#' comments, blank lines, BOM, CRLF, and spaces around '=' are tolerated
def load_api_keys(keys_file: Path) -> dict:
  retVal = {}
  if not keys_file.is_file(): fail(f"Keys file not found -> '{keys_file}' -> pass --keys-file or create it (see '{SETUP_HINT}').", 2)
  text = keys_file.read_text(encoding="utf-8-sig")
  for raw_line in text.splitlines():
    line = raw_line.strip()
    if not line or line.startswith("#") or "=" not in line: continue
    key, value = line.split("=", 1)
    retVal[key.strip()] = value.strip()
  return retVal

def require_key(keys: dict, key_name: str, keys_file: Path) -> str:
  value = keys.get(key_name, "")
  if not value: fail(f"Key '{key_name}' not found in '{keys_file}' -> see '{SETUP_HINT}'.", 2)
  return value

# URL without query string, so API keys passed as parameters never reach the log
def safe_url(url: str) -> str:
  return url.split("?", 1)[0]

# HTTP request with timeout and retry on 429 and 5xx (1s, 2s, 4s; honors Retry-After)
def http_request(method: str, url: str, headers: dict = None, params: dict = None, json_body: object = None, timeout: int = 30) -> requests.Response:
  delays = [1, 2, 4]
  attempt = 0
  while True:
    try:
      response = requests.request(method, url, headers=headers, params=params, json=json_body, timeout=timeout)
    except requests.RequestException as error:
      if attempt >= len(delays): fail(f"Request failed -> '{safe_url(url)}' -> {type(error).__name__}", 1)
      log(f"  Connection error, retrying in {delays[attempt]}s ({attempt + 1} / {len(delays)})...")
      time.sleep(delays[attempt])
      attempt += 1
      continue
    if (response.status_code == 429 or response.status_code >= 500) and attempt < len(delays):
      wait_seconds = delays[attempt]
      retry_after = response.headers.get("Retry-After", "")
      if retry_after.isdigit(): wait_seconds = min(int(retry_after), 60)
      log(f"  HTTP {response.status_code}, retrying in {wait_seconds}s ({attempt + 1} / {len(delays)})...")
      time.sleep(wait_seconds)
      attempt += 1
      continue
    return response

def parse_json(response: requests.Response) -> object:
  try:
    return response.json()
  except ValueError:
    fail(f"Non-JSON response -> HTTP {response.status_code} -> {response.text[:200]}", 1)

def plural(count: int, singular_word: str, plural_word: str = "") -> str:
  if count == 1: return f"{count} {singular_word}"
  return f"{count:,} {plural_word or singular_word + 's'}"

# Print rows as aligned table; columns = list of (header, key, width)
def print_table(rows: list, columns: list):
  header_parts = []
  total_width = 2 * (len(columns) - 1)
  for header, key, width in columns:
    header_parts.append(f"{header:<{width}}")
    total_width += width
  print("  ".join(header_parts))
  print("-" * total_width)
  for row in rows:
    parts = []
    for header, key, width in columns:
      value = row.get(key, "")
      if value is None: value = ""
      if isinstance(value, float): value = f"{value:.4f}".rstrip("0").rstrip(".")
      parts.append(f"{str(value)[:width]:<{width}}")
    print("  ".join(parts))

def emit(result: dict, output_format: str, columns: list = None):
  if output_format == "json":
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return
  if columns and result.get("rows"): print_table(result["rows"], columns)
  for note in result.get("notes", []): print(note)

def create_common_parser() -> argparse.ArgumentParser:
  common = argparse.ArgumentParser(add_help=False)
  common.add_argument("--keys-file", type=Path, default=DEFAULT_KEYS_FILE, help="Credentials file (default: [WORKSPACE_FOLDER]/../.tools/.api-keys.txt)")
  common.add_argument("--format", choices=["table", "json"], default="table", help="Output format (default: table)")
  return common

# ----------------------------------------- END: Common script contract --------------------------------------------------------


# ----------------------------------------- START: Plausible Stats API ---------------------------------------------------------

def run_query(keys: dict, keys_file: Path, body: dict) -> dict:
  api_key = require_key(keys, "PLAUSIBLE_API_KEY", keys_file)
  base_url = (keys.get("PLAUSIBLE_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
  log(f"Querying '{base_url}/api/v2/query' (site '{body.get('site_id')}', range '{body.get('date_range')}')...")
  response = http_request("POST", f"{base_url}/api/v2/query", headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}, json_body=body)
  data = parse_json(response)
  if response.status_code in [401, 402, 403]: fail(f"HTTP {response.status_code} -> {str(data.get('error', ''))[:200] if isinstance(data, dict) else ''} -> Stats API needs a valid key on self-hosted Community Edition or the Cloud Business plan (see '{SETUP_HINT}').", 1)
  if response.status_code != 200: fail(f"HTTP {response.status_code} -> {str(data.get('error', '') if isinstance(data, dict) else data)[:200]}", 1)
  return data

# Convert v2 results [{"dimensions": [...], "metrics": [...]}] to flat rows
def flatten_results(data: dict, dimensions: list, metrics: list) -> list:
  retVal = []
  for item in data.get("results") or []:
    row = {}
    dimension_values = item.get("dimensions") or []
    metric_values = item.get("metrics") or []
    for index in range(len(dimensions)): row[dimensions[index]] = dimension_values[index] if index < len(dimension_values) else ""
    for index in range(len(metrics)): row[metrics[index]] = metric_values[index] if index < len(metric_values) else None
    retVal.append(row)
  return retVal

def build_columns(dimensions: list, metrics: list) -> list:
  retVal = []
  for dimension in dimensions: retVal.append((dimension, dimension, 50))
  for metric in metrics: retVal.append((metric, metric, 14))
  return retVal

# ----------------------------------------- END: Plausible Stats API -----------------------------------------------------------


# ----------------------------------------- START: CLI -------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
  common = create_common_parser()
  parser = argparse.ArgumentParser(description="Plausible Stats API v2 CLI")
  subparsers = parser.add_subparsers(dest="command", required=True)
  for preset_name in PRESETS:
    preset_parser = subparsers.add_parser(preset_name, parents=[common], help=f"Preset query '{preset_name}'")
    preset_parser.add_argument("site", help="Site ID as configured in Plausible, e.g. example.com")
    preset_parser.add_argument("--range", default="30d", help="date_range: day, 7d, 30d, month, 6mo, 12mo, all (default: 30d)")
    preset_parser.add_argument("--limit", type=int, default=20)
  raw_parser = subparsers.add_parser("raw", parents=[common], help="Send a custom v2 query body from a JSON file")
  raw_parser.add_argument("site")
  raw_parser.add_argument("--query-file", type=Path, required=True)
  return parser

def main():
  if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
  if hasattr(sys.stderr, "reconfigure"): sys.stderr.reconfigure(encoding="utf-8")
  args = build_parser().parse_args()
  if args.command == "raw":
    if not args.query_file.is_file(): fail(f"Query file not found -> '{args.query_file}'", 2)
    try:
      body = json.loads(args.query_file.read_text(encoding="utf-8-sig"))
    except ValueError as error:
      fail(f"Invalid JSON in '{args.query_file}' -> {error}", 2)
    body["site_id"] = args.site
  else:
    preset = PRESETS[args.command]
    body = {"site_id": args.site, "metrics": preset["metrics"], "date_range": args.range}
    if preset["dimensions"]:
      body["dimensions"] = preset["dimensions"]
      body["order_by"] = preset["order_by"]
      body["pagination"] = {"limit": args.limit, "offset": 0}
  keys = load_api_keys(args.keys_file)
  data = run_query(keys, args.keys_file, body)
  dimensions = body.get("dimensions") or []
  metrics = body.get("metrics") or []
  rows = flatten_results(data, dimensions, metrics)
  log(f"  {plural(len(rows), 'row')} received.")
  result = {"script": SCRIPT_NAME, "command": args.command, "ok": True, "estimated_cost_usd": 0.0, "actual_cost_usd": 0.0, "params": {"site": args.site, "date_range": body.get("date_range")}, "rows": rows, "notes": []}
  emit(result, args.format, build_columns(dimensions, metrics))
  log("OK.")

if __name__ == "__main__":
  main()

# ----------------------------------------- END: CLI ---------------------------------------------------------------------------
