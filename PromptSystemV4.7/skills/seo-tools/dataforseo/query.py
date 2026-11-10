#!/usr/bin/env python3
"""
DataForSEO v3 CLI with cost gate. Prints an estimate before every paid request and refuses to run above --max-cost.

Usage:
  python query.py balance
  python query.py keywords "project management" --limit 30
  python query.py search-volume "kanban board" "gantt chart"
  python query.py search-volume --file keywords.txt --max-cost 0.20
  python query.py serp "project management software"
  python query.py competitors example.com --limit 10
  python query.py backlinks example.com
  python query.py serp "example query" --format json

Credentials: DATAFORSEO_LOGIN, DATAFORSEO_PASSWORD in [API_KEYS_FILE] (see SKILL.md section "Credential Keys").
"""

import argparse, base64, json, math, sys, time
from pathlib import Path

import requests

SCRIPT_NAME = "dataforseo"
SETUP_HINT = "dataforseo/SETUP.md"
DEFAULT_KEYS_FILE = Path(__file__).resolve().parents[5] / ".tools" / ".api-keys.txt"
BASE_URL_LIVE = "https://api.dataforseo.com/v3"
BASE_URL_SANDBOX = "https://sandbox.dataforseo.com/v3"

# Prices [LITERAL: 2026-11-03; Keywords Data re-verified 2026-11-10], identical to ENDPOINTS.md and SKILL.md; ads_volume_task is the Live price used by this script (Standard queue: $0.06/task)
PRICES_2026_11_03 = {"labs_task": 0.012, "labs_item": 0.00012, "serp_live": 0.002, "serp_standard": 0.0006, "ads_volume_task": 0.09, "ads_volume_task_standard": 0.06, "backlinks_task": 0.024, "backlinks_row": 0.000036}
MAX_KEYWORDS_PER_VOLUME_TASK = 1000
DEFAULT_MAX_COST_USD = 0.10

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

# Text of one table cell: floats rounded, numbers never truncated
def format_cell(value: object) -> str:
  if value is None: return ""
  if isinstance(value, bool): return str(value)
  if isinstance(value, float):
    if abs(value) >= 1000: return f"{value:,.1f}"
    return f"{value:.4f}".rstrip("0").rstrip(".")
  return str(value)

# Print rows as aligned table; columns = list of (header, key, width); text columns are cut at width, number columns are widened
def print_table(rows: list, columns: list):
  cell_rows = []
  widths = []
  for header, key, width in columns: widths.append(width)
  for row in rows:
    cells = []
    for column_index in range(len(columns)):
      value = row.get(columns[column_index][1], "")
      text = format_cell(value)
      if isinstance(value, (int, float)) and not isinstance(value, bool): widths[column_index] = max(widths[column_index], len(text))
      cells.append(text)
    cell_rows.append(cells)
  header_parts = []
  for column_index in range(len(columns)): header_parts.append(f"{columns[column_index][0]:<{widths[column_index]}}")
  print("  ".join(header_parts))
  print("-" * (sum(widths) + 2 * (len(columns) - 1)))
  for cells in cell_rows:
    parts = []
    for column_index in range(len(columns)): parts.append(f"{cells[column_index][:widths[column_index]]:<{widths[column_index]}}")
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


# ----------------------------------------- START: Cost gate -------------------------------------------------------------------

# Return (estimated USD, formula text) for a paid command
def estimate_cost(args) -> tuple:
  if args.command == "keywords":
    return PRICES_2026_11_03["labs_task"] + args.limit * PRICES_2026_11_03["labs_item"], f"1 task, {plural(args.limit, 'item')}"
  if args.command == "competitors":
    return PRICES_2026_11_03["labs_task"] + args.limit * PRICES_2026_11_03["labs_item"], f"1 task, {plural(args.limit, 'item')}"
  if args.command == "search-volume":
    task_count = math.ceil(len(args.keyword_list) / MAX_KEYWORDS_PER_VOLUME_TASK)
    return task_count * PRICES_2026_11_03["ads_volume_task"], f"{plural(task_count, 'task')}, {plural(len(args.keyword_list), 'keyword')}"
  if args.command == "serp":
    return PRICES_2026_11_03["serp_live"], "1 SERP, live"
  if args.command == "backlinks":
    return PRICES_2026_11_03["backlinks_task"] + PRICES_2026_11_03["backlinks_row"], "1 task, 1 row"
  return 0.0, "free"

def enforce_cost_gate(args) -> float:
  estimate, formula = estimate_cost(args)
  log(f"Estimating cost for '{args.command}' ({formula})...")
  log(f"  Estimate: ${estimate:.4f} (limit ${args.max_cost:.2f}).")
  if estimate > args.max_cost: fail(f"Estimate exceeds limit -> rerun with --max-cost {math.ceil(estimate * 100) / 100:.2f} to allow.", 2)
  return estimate

# ----------------------------------------- END: Cost gate ---------------------------------------------------------------------


# ----------------------------------------- START: DataForSEO requests ---------------------------------------------------------

def build_headers(keys: dict, keys_file: Path) -> dict:
  login = require_key(keys, "DATAFORSEO_LOGIN", keys_file)
  password = require_key(keys, "DATAFORSEO_PASSWORD", keys_file)
  token = base64.b64encode(f"{login}:{password}".encode("utf-8")).decode("ascii")
  return {"Authorization": f"Basic {token}", "Content-Type": "application/json"}

def raise_api_error(code: object, message: str, level: str):
  hint = ""
  if str(code).startswith("401") or str(code).startswith("402"): hint = f" -> check credentials, balance, and account verification (see '{SETUP_HINT}')"
  fail(f"{level} error -> {code} -> {message}{hint}", 1)

# POST one task list; return (tasks, total cost reported by the API)
def api_post(base_url: str, endpoint: str, payload: list, headers: dict) -> tuple:
  log(f"Querying '{endpoint}'...")
  response = http_request("POST", f"{base_url}/{endpoint}", headers=headers, json_body=payload)
  data = parse_json(response)
  if response.status_code != 200 and not isinstance(data, dict): fail(f"HTTP {response.status_code} -> '{endpoint}'", 1)
  if data.get("status_code") != 20000: raise_api_error(data.get("status_code", response.status_code), data.get("status_message", ""), "API")
  tasks = data.get("tasks") or []
  for task in tasks:
    if task.get("status_code") != 20000: raise_api_error(task.get("status_code"), task.get("status_message", ""), "Task")
  return tasks, data.get("cost")

def first_result(tasks: list) -> dict:
  if not tasks: return {}
  results = tasks[0].get("result") or []
  if not results: return {}
  return results[0] or {}

def report_actual_cost(result: dict, estimate: float, reported_cost: object):
  if reported_cost is None:
    result["actual_cost_usd"] = estimate
    log(f"  Actual cost: ${estimate:.4f} (estimated).")
  else:
    result["actual_cost_usd"] = reported_cost
    log(f"  Actual cost: ${float(reported_cost):.4f}.")

# ----------------------------------------- END: DataForSEO requests -----------------------------------------------------------


# ----------------------------------------- START: Commands --------------------------------------------------------------------

def cmd_balance(args, headers: dict, base_url: str) -> dict:
  log("Fetching account balance...")
  response = http_request("GET", f"{base_url}/appendix/user_data", headers=headers)
  data = parse_json(response)
  if data.get("status_code") != 20000: raise_api_error(data.get("status_code", response.status_code), data.get("status_message", ""), "API")
  money = first_result(data.get("tasks") or []).get("money") or {}
  rows = [{"balance_usd": money.get("balance"), "total_spent_usd": money.get("total"), "limit_daily_usd": money.get("limit_daily", "[UNKNOWN]")}]
  notes = [f"Balance: ${float(money.get('balance') or 0):.2f}", f"Total spent: ${float(money.get('total') or 0):.2f}"]
  return {"rows": rows, "notes": notes, "estimated_cost_usd": 0.0, "actual_cost_usd": 0.0}

def cmd_keywords(args, headers: dict, base_url: str) -> dict:
  payload = [{"keyword": args.keyword, "location_code": args.location, "language_code": args.lang, "limit": args.limit, "include_seed_keyword": True}]
  tasks, reported_cost = api_post(base_url, "dataforseo_labs/google/keyword_suggestions/live", payload, headers)
  items = first_result(tasks).get("items") or []
  rows = []
  for item in items:
    keyword_info = item.get("keyword_info") or {}
    keyword_properties = item.get("keyword_properties") or {}
    intent_info = item.get("search_intent_info") or {}
    rows.append({"keyword": item.get("keyword", ""), "volume": keyword_info.get("search_volume") or 0, "difficulty": keyword_properties.get("keyword_difficulty"), "cpc": keyword_info.get("cpc"), "intent": intent_info.get("main_intent", "")})
  rows.sort(key=volume_sort_key, reverse=True)
  log(f"  {plural(len(rows), 'row')} received.")
  return {"rows": rows, "notes": [], "reported_cost": reported_cost}

def volume_sort_key(row: dict) -> int:
  return row.get("volume") or 0

def cmd_search_volume(args, headers: dict, base_url: str) -> dict:
  rows = []
  total_cost = 0.0
  cost_reported = True
  chunk_count = math.ceil(len(args.keyword_list) / MAX_KEYWORDS_PER_VOLUME_TASK)
  for chunk_index in range(chunk_count):
    chunk = args.keyword_list[chunk_index * MAX_KEYWORDS_PER_VOLUME_TASK:(chunk_index + 1) * MAX_KEYWORDS_PER_VOLUME_TASK]
    if chunk_count > 1: log(f"  [ {chunk_index + 1} / {chunk_count} ] {plural(len(chunk), 'keyword')}...")
    payload = [{"keywords": chunk, "location_code": args.location, "language_code": args.lang}]
    tasks, reported_cost = api_post(base_url, "keywords_data/google_ads/search_volume/live", payload, headers)
    if reported_cost is None: cost_reported = False
    else: total_cost += float(reported_cost)
    for task in tasks:
      for item in task.get("result") or []:
        rows.append({"keyword": item.get("keyword", ""), "volume": item.get("search_volume") or 0, "competition": item.get("competition", ""), "cpc": item.get("cpc")})
  rows.sort(key=volume_sort_key, reverse=True)
  log(f"  {plural(len(rows), 'row')} received.")
  return {"rows": rows, "notes": [], "reported_cost": total_cost if cost_reported else None}

def cmd_serp(args, headers: dict, base_url: str) -> dict:
  payload = [{"keyword": args.keyword, "location_code": args.location, "language_code": args.lang, "device": args.device, "load_async_ai_overview": True}]
  tasks, reported_cost = api_post(base_url, "serp/google/organic/live/advanced", payload, headers)
  result = first_result(tasks)
  items = result.get("items") or []
  rows = []
  ai_overview_count = 0
  for item in items:
    if item.get("type") == "ai_overview": ai_overview_count += 1
    if item.get("type") == "organic" and len(rows) < 10:
      rows.append({"position": item.get("rank_group"), "domain": item.get("domain", ""), "title": item.get("title", ""), "url": item.get("url", "")})
  item_types = result.get("item_types") or []
  ai_overview_note = "AI Overview present" if ai_overview_count > 0 else "AI Overview not present"
  notes = [f"{plural(len(rows), 'organic result')}, {ai_overview_note}, {plural(len(item_types), 'SERP feature type')}: {', '.join(item_types)}"]
  log(f"  {notes[0]}.")
  return {"rows": rows, "notes": notes, "reported_cost": reported_cost, "ai_overview_present": ai_overview_count > 0, "serp_feature_types": item_types}

def cmd_competitors(args, headers: dict, base_url: str) -> dict:
  payload = [{"target": args.domain, "location_code": args.location, "language_code": args.lang, "limit": args.limit}]
  tasks, reported_cost = api_post(base_url, "dataforseo_labs/google/competitors_domain/live", payload, headers)
  items = first_result(tasks).get("items") or []
  rows = []
  for item in items:
    organic_metrics = (item.get("full_domain_metrics") or {}).get("organic") or {}
    rows.append({"domain": item.get("domain", ""), "avg_position": item.get("avg_position"), "intersections": item.get("intersections"), "keywords": organic_metrics.get("count"), "traffic_estimate": organic_metrics.get("etv")})
  log(f"  {plural(len(rows), 'row')} received.")
  return {"rows": rows, "notes": [], "reported_cost": reported_cost}

def cmd_backlinks(args, headers: dict, base_url: str) -> dict:
  payload = [{"target": args.domain, "internal_list_limit": 10, "backlinks_status_type": "live"}]
  tasks, reported_cost = api_post(base_url, "backlinks/summary/live", payload, headers)
  result = first_result(tasks)
  row = {"target": args.domain, "backlinks": result.get("backlinks"), "referring_domains": result.get("referring_domains"), "referring_main_domains": result.get("referring_main_domains"), "rank": result.get("rank"), "broken_backlinks": result.get("broken_backlinks")}
  rows = [row] if result else []
  log(f"  {plural(len(rows), 'row')} received.")
  return {"rows": rows, "notes": [], "reported_cost": reported_cost}

COLUMNS = {
  "balance": [("Balance USD", "balance_usd", 12), ("Total spent USD", "total_spent_usd", 16), ("Daily limit", "limit_daily_usd", 12)],
  "keywords": [("Keyword", "keyword", 45), ("Volume", "volume", 8), ("Difficulty", "difficulty", 10), ("CPC", "cpc", 7), ("Intent", "intent", 14)],
  "search-volume": [("Keyword", "keyword", 45), ("Volume", "volume", 8), ("Competition", "competition", 12), ("CPC", "cpc", 7)],
  "serp": [("Pos", "position", 4), ("Domain", "domain", 32), ("Title", "title", 60)],
  "competitors": [("Domain", "domain", 36), ("Avg pos", "avg_position", 8), ("Overlap", "intersections", 8), ("Keywords", "keywords", 9), ("Traffic", "traffic_estimate", 10)],
  "backlinks": [("Target", "target", 30), ("Backlinks", "backlinks", 12), ("Ref domains", "referring_domains", 12), ("Rank", "rank", 6), ("Broken", "broken_backlinks", 8)],
}

COMMANDS = {"balance": cmd_balance, "keywords": cmd_keywords, "search-volume": cmd_search_volume, "serp": cmd_serp, "competitors": cmd_competitors, "backlinks": cmd_backlinks}

# ----------------------------------------- END: Commands ----------------------------------------------------------------------


# ----------------------------------------- START: CLI -------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
  common = create_common_parser()
  paid = argparse.ArgumentParser(add_help=False)
  paid.add_argument("--location", type=int, default=2840, help="Location code (default: 2840 = United States)")
  paid.add_argument("--lang", default="en", help="Language code (default: en)")
  paid.add_argument("--max-cost", type=float, default=DEFAULT_MAX_COST_USD, help=f"Abort when estimate exceeds this USD amount (default: {DEFAULT_MAX_COST_USD:.2f})")
  paid.add_argument("--sandbox", action="store_true", help="Use sandbox endpoint (dummy data)")
  parser = argparse.ArgumentParser(description="DataForSEO v3 CLI with cost gate (prices 2026-11-03)", epilog="Location codes: 2840 United States, 2826 United Kingdom, 2276 Germany, 2250 France")
  subparsers = parser.add_subparsers(dest="command", required=True)
  balance_parser = subparsers.add_parser("balance", parents=[common], help="Account balance ($0)")
  balance_parser.add_argument("--sandbox", action="store_true", help="Use sandbox endpoint")
  keywords_parser = subparsers.add_parser("keywords", parents=[common, paid], help="Labs keyword suggestions ($0.012/task + $0.00012/item)")
  keywords_parser.add_argument("keyword", help="Seed keyword")
  keywords_parser.add_argument("--limit", type=int, default=30, help="Max items (default: 30)")
  volume_parser = subparsers.add_parser("search-volume", parents=[common, paid], help="Google Ads search volume (Live $0.09/task, up to 1,000 keywords per task)")
  volume_parser.add_argument("keywords", nargs="*", help="Keywords")
  volume_parser.add_argument("--file", type=Path, help="UTF-8 text file with one keyword per line")
  serp_parser = subparsers.add_parser("serp", parents=[common, paid], help="Live Google SERP with AI Overview ($0.002/SERP)")
  serp_parser.add_argument("keyword", help="Search query")
  serp_parser.add_argument("--device", choices=["desktop", "mobile"], default="desktop", help="Device (default: desktop)")
  competitors_parser = subparsers.add_parser("competitors", parents=[common, paid], help="Labs competitor domains ($0.012/task + $0.00012/item)")
  competitors_parser.add_argument("domain", help="Target domain")
  competitors_parser.add_argument("--limit", type=int, default=20, help="Max items (default: 20)")
  backlinks_parser = subparsers.add_parser("backlinks", parents=[common, paid], help="Backlink summary ($0.024/task + $0.000036/row)")
  backlinks_parser.add_argument("domain", help="Target domain")
  return parser

def collect_keywords(args) -> list:
  retVal = []
  for keyword in args.keywords: retVal.append(keyword.strip())
  if args.file:
    if not args.file.is_file(): fail(f"Keyword file not found -> '{args.file}'", 2)
    for line in args.file.read_text(encoding="utf-8-sig").splitlines():
      if line.strip(): retVal.append(line.strip())
  if not retVal: fail("No keywords given -> pass keywords or --file.", 2)
  return retVal

def main():
  if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
  if hasattr(sys.stderr, "reconfigure"): sys.stderr.reconfigure(encoding="utf-8")
  args = build_parser().parse_args()
  if args.command == "search-volume": args.keyword_list = collect_keywords(args)
  estimate = 0.0
  if args.command != "balance": estimate = enforce_cost_gate(args)
  base_url = BASE_URL_SANDBOX if getattr(args, "sandbox", False) else BASE_URL_LIVE
  if base_url == BASE_URL_SANDBOX: log("[SANDBOX MODE - results are dummy data]")
  keys = load_api_keys(args.keys_file)
  headers = build_headers(keys, args.keys_file)
  command_result = COMMANDS[args.command](args, headers, base_url)
  params = {}
  for name in ["keyword", "domain", "location", "lang", "limit", "device"]:
    if hasattr(args, name): params[name] = getattr(args, name)
  if args.command == "search-volume": params["keywords"] = len(args.keyword_list)
  result = {"script": SCRIPT_NAME, "command": args.command, "ok": True, "estimated_cost_usd": estimate, "actual_cost_usd": 0.0, "params": params, "rows": command_result.get("rows", []), "notes": command_result.get("notes", [])}
  for extra_key in ["ai_overview_present", "serp_feature_types"]:
    if extra_key in command_result: result[extra_key] = command_result[extra_key]
  if args.command != "balance": report_actual_cost(result, estimate, command_result.get("reported_cost"))
  emit(result, args.format, COLUMNS.get(args.command))
  log("OK.")

if __name__ == "__main__":
  main()

# ----------------------------------------- END: CLI ---------------------------------------------------------------------------
