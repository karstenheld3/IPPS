#!/usr/bin/env python3
"""
Bing Webmaster Tools CLI (free). JSON API: sites, query and page stats, traffic, inbound links, URL submission.

Usage:
  python query.py sites
  python query.py query-stats https://example.com/
  python query.py page-stats https://example.com/
  python query.py traffic https://example.com/
  python query.py links https://example.com/
  python query.py quota https://example.com/
  python query.py submit https://example.com/ https://example.com/new-page

Credentials: BING_WEBMASTER_API_KEY in [API_KEYS_FILE] (see SKILL.md section "Credential Keys").
AI Performance report (Grounding Queries, Citation Share) has no API; see SETUP.md for the UI export.
"""

import argparse, datetime, json, re, sys, time
from pathlib import Path

import requests

SCRIPT_NAME = "bing-webmaster"
SETUP_HINT = "bing-webmaster/SETUP.md"
DEFAULT_KEYS_FILE = Path(__file__).resolve().parents[5] / ".tools" / ".api-keys.txt"
API_BASE = "https://ssl.bing.com/webmaster/api.svc/json"
DATE_PATTERN = re.compile(r"/Date\((-?\d+)")

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


# ----------------------------------------- START: Bing Webmaster API ----------------------------------------------------------

# Call one API method; unwrap {"d": ...}
def call_bing(method_name: str, api_key: str, params: dict = None, json_body: dict = None) -> object:
  query = {"apikey": api_key}
  if params:
    for name in params: query[name] = params[name]
  http_method = "POST" if json_body is not None else "GET"
  response = http_request(http_method, f"{API_BASE}/{method_name}", headers={"Content-Type": "application/json; charset=utf-8"}, params=query, json_body=json_body)
  data = parse_json(response)
  if response.status_code != 200:
    message = ""
    if isinstance(data, dict): message = str(data.get("Message") or data.get("ErrorCode") or "")
    hint = f" -> check BING_WEBMASTER_API_KEY and site verification (see '{SETUP_HINT}')" if response.status_code in [400, 401, 403] else ""
    fail(f"{method_name} -> HTTP {response.status_code} -> {message[:200]}{hint}", 1)
  if isinstance(data, dict) and "d" in data: return data["d"]
  return data

# Convert '/Date(1700000000000-0800)/' to YYYY-MM-DD
def parse_bing_date(value: object) -> str:
  match = DATE_PATTERN.search(str(value or ""))
  if not match: return str(value or "")
  return datetime.datetime.fromtimestamp(int(match.group(1)) / 1000, datetime.timezone.utc).date().isoformat()

def stats_rows(items: list, key_name: str) -> list:
  retVal = []
  for item in items or []:
    retVal.append({key_name: item.get("Query", ""), "date": parse_bing_date(item.get("Date")), "clicks": item.get("Clicks", 0), "impressions": item.get("Impressions", 0), "avg_impression_position": item.get("AvgImpressionPosition"), "avg_click_position": item.get("AvgClickPosition")})
  return retVal

# Aggregate daily rows per query or page
def aggregate_rows(rows: list, key_name: str) -> list:
  retVal = []
  totals = {}
  for row in rows:
    key = row[key_name]
    if key not in totals:
      totals[key] = {key_name: key, "clicks": 0, "impressions": 0, "weighted_position": 0.0}
      retVal.append(totals[key])
    totals[key]["clicks"] += row["clicks"] or 0
    totals[key]["impressions"] += row["impressions"] or 0
    if row["avg_impression_position"] and row["avg_impression_position"] > 0: totals[key]["weighted_position"] += row["avg_impression_position"] * (row["impressions"] or 0)
  for total in retVal:
    total["avg_position"] = round(total["weighted_position"] / total["impressions"], 1) if total["impressions"] else None
    del total["weighted_position"]
  retVal.sort(key=impressions_sort_key, reverse=True)
  return retVal

def impressions_sort_key(row: dict) -> int:
  return row.get("impressions") or 0

# ----------------------------------------- END: Bing Webmaster API ------------------------------------------------------------


# ----------------------------------------- START: Commands --------------------------------------------------------------------

def cmd_sites(args, api_key: str) -> dict:
  log("Listing Bing Webmaster sites...")
  items = call_bing("GetUserSites", api_key) or []
  rows = []
  for item in items: rows.append({"site": item.get("Url", ""), "verified": item.get("IsVerified", "")})
  log(f"  {plural(len(rows), 'site')} found.")
  return {"rows": rows, "notes": []}

def cmd_query_stats(args, api_key: str) -> dict:
  log(f"Fetching query stats for '{args.site}' (last 6 months, aggregated)...")
  rows = aggregate_rows(stats_rows(call_bing("GetQueryStats", api_key, {"siteUrl": args.site}), "query"), "query")
  log(f"  {plural(len(rows), 'query', 'queries')} received.")
  return {"rows": rows[:args.limit], "notes": []}

def cmd_page_stats(args, api_key: str) -> dict:
  log(f"Fetching page stats for '{args.site}' (last 6 months, aggregated)...")
  rows = aggregate_rows(stats_rows(call_bing("GetPageStats", api_key, {"siteUrl": args.site}), "page"), "page")
  log(f"  {plural(len(rows), 'page')} received.")
  return {"rows": rows[:args.limit], "notes": []}

def cmd_traffic(args, api_key: str) -> dict:
  log(f"Fetching rank and traffic stats for '{args.site}'...")
  items = call_bing("GetRankAndTrafficStats", api_key, {"siteUrl": args.site}) or []
  rows = []
  for item in items: rows.append({"date": parse_bing_date(item.get("Date")), "clicks": item.get("Clicks", 0), "impressions": item.get("Impressions", 0)})
  log(f"  {plural(len(rows), 'day')} received.")
  return {"rows": rows, "notes": []}

def cmd_links(args, api_key: str) -> dict:
  log(f"Fetching inbound link counts for '{args.site}'...")
  data = call_bing("GetLinkCounts", api_key, {"siteUrl": args.site, "page": 0}) or {}
  rows = []
  for item in data.get("Links") or []: rows.append({"url": item.get("Url", ""), "links": item.get("Count", 0)})
  log(f"  {plural(len(rows), 'page')} with inbound links.")
  return {"rows": rows[:args.limit], "notes": []}

def fetch_quota(site: str, api_key: str) -> dict:
  data = call_bing("GetUrlSubmissionQuota", api_key, {"siteUrl": site}) or {}
  return {"daily_quota": data.get("DailyQuota", 0), "monthly_quota": data.get("MonthlyQuota", 0)}

def cmd_quota(args, api_key: str) -> dict:
  log(f"Fetching URL submission quota for '{args.site}'...")
  return {"rows": [fetch_quota(args.site, api_key)], "notes": []}

def cmd_submit(args, api_key: str) -> dict:
  log(f"Checking URL submission quota for '{args.site}'...")
  quota = fetch_quota(args.site, api_key)
  if len(args.urls) > quota["daily_quota"]: fail(f"{plural(len(args.urls), 'URL')} exceed remaining daily quota {quota['daily_quota']} -> submit fewer URLs or use indexnow/submit.py.", 2)
  log(f"Submitting {plural(len(args.urls), 'URL')}...")
  call_bing("SubmitUrlBatch", api_key, json_body={"siteUrl": args.site, "urlList": args.urls})
  return {"rows": [{"submitted": len(args.urls), "daily_quota_before": quota["daily_quota"]}], "notes": []}

COLUMNS = {
  "sites": [("Site", "site", 50), ("Verified", "verified", 8)],
  "query-stats": [("Query", "query", 50), ("Clicks", "clicks", 8), ("Impressions", "impressions", 11), ("Avg pos", "avg_position", 7)],
  "page-stats": [("Page", "page", 60), ("Clicks", "clicks", 8), ("Impressions", "impressions", 11), ("Avg pos", "avg_position", 7)],
  "traffic": [("Date", "date", 10), ("Clicks", "clicks", 8), ("Impressions", "impressions", 11)],
  "links": [("URL", "url", 70), ("Links", "links", 8)],
  "quota": [("Daily quota", "daily_quota", 12), ("Monthly quota", "monthly_quota", 14)],
  "submit": [("Submitted", "submitted", 10), ("Daily quota before", "daily_quota_before", 18)],
}

COMMANDS = {"sites": cmd_sites, "query-stats": cmd_query_stats, "page-stats": cmd_page_stats, "traffic": cmd_traffic, "links": cmd_links, "quota": cmd_quota, "submit": cmd_submit}

# ----------------------------------------- END: Commands ----------------------------------------------------------------------


# ----------------------------------------- START: CLI -------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
  common = create_common_parser()
  parser = argparse.ArgumentParser(description="Bing Webmaster Tools CLI (JSON API, free)", epilog="SITE: site URL exactly as registered in Bing Webmaster Tools, e.g. https://example.com/")
  subparsers = parser.add_subparsers(dest="command", required=True)
  subparsers.add_parser("sites", parents=[common], help="List sites in the account")
  for command_name, help_text in [("query-stats", "Search queries (clicks, impressions, position)"), ("page-stats", "Pages (clicks, impressions, position)"), ("links", "Pages with inbound link counts")]:
    command_parser = subparsers.add_parser(command_name, parents=[common], help=help_text)
    command_parser.add_argument("site")
    command_parser.add_argument("--limit", type=int, default=50)
  traffic_parser = subparsers.add_parser("traffic", parents=[common], help="Daily clicks and impressions")
  traffic_parser.add_argument("site")
  quota_parser = subparsers.add_parser("quota", parents=[common], help="URL submission quota")
  quota_parser.add_argument("site")
  submit_parser = subparsers.add_parser("submit", parents=[common], help="Submit URLs (checks daily quota first)")
  submit_parser.add_argument("site")
  submit_parser.add_argument("urls", nargs="+")
  return parser

def main():
  if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
  if hasattr(sys.stderr, "reconfigure"): sys.stderr.reconfigure(encoding="utf-8")
  args = build_parser().parse_args()
  keys = load_api_keys(args.keys_file)
  api_key = require_key(keys, "BING_WEBMASTER_API_KEY", args.keys_file)
  command_result = COMMANDS[args.command](args, api_key)
  params = {}
  for name in ["site", "limit"]:
    if hasattr(args, name): params[name] = getattr(args, name)
  result = {"script": SCRIPT_NAME, "command": args.command, "ok": True, "estimated_cost_usd": 0.0, "actual_cost_usd": 0.0, "params": params, "rows": command_result["rows"], "notes": command_result.get("notes", [])}
  emit(result, args.format, COLUMNS.get(args.command))
  log("OK.")

if __name__ == "__main__":
  main()

# ----------------------------------------- END: CLI ---------------------------------------------------------------------------
