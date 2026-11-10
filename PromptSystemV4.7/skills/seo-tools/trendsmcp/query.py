#!/usr/bin/env python3
"""
Trends MCP REST API CLI (prepaid credits, free tier 100 requests per month). Cross-platform trend discovery. REST only, no MCP.

Usage:
  python query.py history "standing desk" --source "Google Search" --last 12
  python query.py growth "standing desk" --source TikTok --window 7D 3M 12M
  python query.py board --type "Google Trends" --limit 10
  python query.py board --type "TikTok Trending Hashtags" --limit 20 --climbers
  python query.py posts "standing desk" --source YouTube --days 30

Billing: 1 request = 1 credit (vendor claim); `board` costs 1 credit per 10 rows ([TESTED 2026-11-10], vendor `cost_note`) and reports `requests_charged`.
Credentials: TRENDSMCP_API_KEY in [API_KEYS_FILE] (see SKILL.md section "Credential Keys").
"""

import argparse, json, math, sys, time
from pathlib import Path

import requests

SCRIPT_NAME = "trendsmcp"
SETUP_HINT = "trendsmcp/SETUP.md"
DEFAULT_KEYS_FILE = Path(__file__).resolve().parents[5] / ".tools" / ".api-keys.txt"
API_URL = "https://api.trendsmcp.ai/api"
CREDIT_PRICE_USD = 0.025
BOARD_ROWS_PER_CREDIT = 10
DEFAULT_MAX_CREDITS = 20
DEFAULT_WINDOWS = ["7D", "3M", "12M"]

# Source and board names [LITERAL: 2026-11-10], vendor data catalog https://www.trendsmcp.ai/data-catalog (updated 2026-11-06)
SERIES_SOURCES = ["Google Search", "Google Images", "Google News", "Google Shopping", "YouTube", "Wikipedia", "TikTok", "Amazon", "Pinterest", "npm", "Python", "Steam", "App Downloads", "App Rankings"]
BOARD_TYPES = [
  "Amazon Best Sellers Top Rated", "Amazon Best Sellers by Category", "App Store Top Free", "App Store Top Paid", "GitHub", "Google News Top News", "Google Play", "Google Trends",
  "Google Trends by Category", "IMDb MOVIEmeter", "Open Library Trending Books", "Pinterest Trending", "Pinterest Trending by Category", "Polymarket Top Markets", "Reddit Hot Posts",
  "Reddit World News", "Top Websites", "Spotify Top Podcasts", "Steam Most Played", "Substack", "Substack by Category", "TikTok Trending Hashtags", "TikTok Trending Hashtags by Category",
  "TikTok Trending Searches", "Wikipedia Trending", "X (Twitter) Trending", "YouTube Trending",
]
CONTEXT_SOURCES = ["News", "YouTube", "TikTok", "Instagram", "X", "Reddit", "Bluesky", "Hacker News", "Polymarket", "GitHub"]

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


# ----------------------------------------- START: Credit gate -----------------------------------------------------------------

def estimate_credits(args) -> tuple:
  if args.command == "board":
    credits_per_board = max(1, math.ceil(args.limit / BOARD_ROWS_PER_CREDIT))
    return len(args.types) * credits_per_board, f"{plural(len(args.types), 'board')} x {plural(credits_per_board, 'credit')} (1 credit per {BOARD_ROWS_PER_CREDIT} rows)"
  return len(args.keywords), f"{plural(len(args.keywords), 'request')} x 1 credit"

def enforce_credit_gate(args) -> int:
  estimate, formula = estimate_credits(args)
  log(f"Estimating credits for '{args.command}' ({formula})...")
  log(f"  Estimate: {plural(estimate, 'credit')} = ${estimate * args.credit_price:.4f} (limit {plural(args.max_credits, 'credit')}).")
  if estimate > args.max_credits: fail(f"Estimate exceeds limit -> rerun with --max-credits {estimate} to allow.", 2)
  return estimate

# ----------------------------------------- END: Credit gate -------------------------------------------------------------------


# ----------------------------------------- START: Trends MCP requests ---------------------------------------------------------

# Case-insensitive match against the vendor catalog; unknown name -> exit 2 listing valid names
def resolve_name(name: str, valid_names: list, kind: str) -> str:
  for valid_name in valid_names:
    if valid_name.lower() == name.lower(): return valid_name
  fail(f"Unknown {kind} '{name}' -> valid: {', '.join(valid_names)} (catalog of 2026-11-06, see '{SETUP_HINT}').", 2)

# REST answers HTTP 200 with {"statusCode": N, "body": "<json string>"}; a missing or wrong key is HTTP 401 or 403
def unwrap_envelope(data: object) -> tuple:
  if isinstance(data, dict) and "statusCode" in data and "body" in data:
    body = data["body"]
    if isinstance(body, str):
      try:
        body = json.loads(body)
      except ValueError:
        body = {"message": body[:200]}
    return int(data["statusCode"]), body
  return 200, data

def call_trends(body: dict, api_key: str) -> object:
  headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
  response = http_request("POST", API_URL, headers=headers, json_body=body)
  if response.status_code in [401, 403]: fail(f"HTTP {response.status_code} -> check TRENDSMCP_API_KEY (see '{SETUP_HINT}').", 1)
  if response.status_code == 402: fail(f"HTTP 402 -> credits exhausted -> top up at the provider account page (see '{SETUP_HINT}').", 1)
  try:
    data = response.json()
  except ValueError:
    fail(f"Non-JSON response -> HTTP {response.status_code} -> {response.text[:200]}", 1)
  status_code, payload = unwrap_envelope(data)
  if status_code == 200 and response.status_code == 200: return payload
  error_code = payload.get("error", "") if isinstance(payload, dict) else ""
  message = payload.get("message", "") if isinstance(payload, dict) else str(payload)
  if error_code == "no_data": return None
  if error_code == "monthly_limit_reached": fail(f"Free tier exhausted (100 requests per month) -> buy credits (see '{SETUP_HINT}').", 1)
  vendor_hint = " -> vendor-side error, retry later or use another source" if int(status_code or 0) >= 500 else ""
  fail(f"Mode '{body.get('mode')}' -> status {status_code or response.status_code} -> {error_code} {str(message)[:200]}{vendor_hint}", 1)

# ----------------------------------------- END: Trends MCP requests -----------------------------------------------------------


# ----------------------------------------- START: Commands --------------------------------------------------------------------

def cmd_history(args, api_key: str) -> dict:
  source = resolve_name(args.source, SERIES_SOURCES, "source")
  rows = []
  notes = []
  for index in range(len(args.keywords)):
    keyword = args.keywords[index]
    log(f"  [ {index + 1} / {len(args.keywords)} ] Time series for '{keyword}' on '{source}'...")
    body = {"mode": "get_time_series", "keyword": keyword, "source": source}
    if args.country: body["country"] = args.country
    if args.resolution: body["resolution"] = args.resolution
    points = call_trends(body, api_key)
    if not isinstance(points, list) or not points:
      notes.append(f"'{keyword}': 0 rows")
      continue
    for point in points: rows.append({"keyword": keyword, "date": str(point.get("date", ""))[:10], "value": point.get("value"), "volume": point.get("volume")})
    values = []
    for point in points:
      if isinstance(point.get("value"), (int, float)): values.append(point["value"])
    if values: notes.append(f"'{keyword}': {plural(len(points), 'point')} {str(points[0].get('date', ''))[:10]} to {str(points[-1].get('date', ''))[:10]}, latest index {values[-1]}, min {min(values)}, max {max(values)}")
  return {"rows": rows, "notes": notes, "credits_used": len(args.keywords)}

def cmd_growth(args, api_key: str) -> dict:
  source = resolve_name(args.source, SERIES_SOURCES, "source")
  rows = []
  notes = []
  for index in range(len(args.keywords)):
    keyword = args.keywords[index]
    log(f"  [ {index + 1} / {len(args.keywords)} ] Growth for '{keyword}' on '{source}' ({', '.join(args.window)})...")
    body = {"mode": "get_growth", "keyword": keyword, "source": source, "percent_growth": args.window}
    if args.country: body["country"] = args.country
    data = call_trends(body, api_key)
    results = (data or {}).get("results") if isinstance(data, dict) else None
    if not results:
      notes.append(f"'{keyword}': 0 rows")
      continue
    for item in results:
      rows.append({"keyword": keyword, "period": item.get("period", ""), "growth_percent": item.get("growth"), "direction": item.get("direction", ""),
        "recent_value": item.get("recent_value"), "baseline_value": item.get("baseline_value"), "volume_growth_percent": item.get("volume_growth")})
  return {"rows": rows, "notes": notes, "credits_used": len(args.keywords)}

def board_row(entry: object) -> dict:
  if isinstance(entry, dict): return {"rank": entry.get("rank"), "keyword": entry.get("keyword", entry.get("name", "")), "previous_rank": entry.get("prev_rank"), "rank_change": entry.get("rank_change"), "category": ""}
  if isinstance(entry, list) and len(entry) >= 2:
    category_parts = []
    if len(entry) > 2:
      if isinstance(entry[2], list):
        for part in entry[2]: category_parts.append(str(part))
      else: category_parts.append(str(entry[2]))
    category = " > ".join(category_parts)
    return {"rank": entry[0], "keyword": entry[1], "previous_rank": None, "rank_change": None, "category": category}
  return {"rank": None, "keyword": str(entry), "previous_rank": None, "rank_change": None, "category": ""}

def cmd_board(args, api_key: str) -> dict:
  rows = []
  notes = []
  credits_used = 0
  for index in range(len(args.types)):
    board_type = resolve_name(args.types[index], BOARD_TYPES, "board")
    log(f"  [ {index + 1} / {len(args.types)} ] Board '{board_type}' (limit {args.limit}{', biggest climbers' if args.climbers else ''})...")
    body = {"mode": "get_top_trends", "type": board_type, "limit": args.limit}
    if args.climbers: body["sort"] = "rank_change"
    if args.country: body["country"] = args.country
    if args.window: body["window"] = args.window
    data = call_trends(body, api_key)
    entries = (data or {}).get("data") if isinstance(data, dict) else None
    charged = (data or {}).get("requests_charged") if isinstance(data, dict) else None
    credits_used += charged if isinstance(charged, int) else 1
    if not entries:
      notes.append(f"'{board_type}': 0 rows")
      continue
    for entry in entries:
      row = board_row(entry)
      row["board"] = board_type
      rows.append(row)
    cost_note = data.get("cost_note", "")
    notes.append(f"'{board_type}': {plural(len(entries), 'row')} as of {data.get('as_of_ts', '[UNKNOWN]')}, requests charged {charged if charged is not None else '[UNKNOWN]'}{', ' + cost_note if cost_note else ''}")
  return {"rows": rows, "notes": notes, "credits_used": credits_used}

def engagement_value(item: dict, names: list) -> object:
  engagement = item.get("engagement") or {}
  for name in names:
    if name in engagement: return engagement[name]
  return None

def cmd_posts(args, api_key: str) -> dict:
  source = resolve_name(args.source, CONTEXT_SOURCES, "source")
  rows = []
  notes = []
  for index in range(len(args.keywords)):
    keyword = args.keywords[index]
    log(f"  [ {index + 1} / {len(args.keywords)} ] Posts about '{keyword}' on '{source}' (last {plural(args.days, 'day')})...")
    body = {"mode": "get_context", "keyword": keyword, "source": source, "days": args.days}
    if args.limit: body["limit"] = args.limit
    data = call_trends(body, api_key)
    sources = (data or {}).get("sources") if isinstance(data, dict) else None
    if not sources:
      notes.append(f"'{keyword}': 0 rows")
      continue
    for source_block in sources:
      if source_block.get("error"): notes.append(f"'{keyword}' on '{source_block.get('source', source)}': {str(source_block['error'])[:120]}")
      for item in source_block.get("items") or []:
        rows.append({"keyword": keyword, "source": source_block.get("source", source), "kind": item.get("kind", ""), "title": item.get("title", ""), "published": (item.get("published") or "")[:10],
          "views": engagement_value(item, ["views", "plays"]), "likes": engagement_value(item, ["likes", "score", "points"]), "comments": engagement_value(item, ["comments", "replies"]), "url": item.get("url", "")})
  return {"rows": rows, "notes": notes, "credits_used": len(args.keywords)}

COLUMNS = {
  "history": [("Keyword", "keyword", 24), ("Date", "date", 10), ("Index", "value", 6), ("Volume", "volume", 10)],
  "growth": [("Keyword", "keyword", 24), ("Period", "period", 7), ("Growth %", "growth_percent", 9), ("Direction", "direction", 9), ("Recent", "recent_value", 8), ("Baseline", "baseline_value", 8), ("Vol. growth %", "volume_growth_percent", 13)],
  "board": [("Board", "board", 24), ("Rank", "rank", 5), ("Keyword", "keyword", 40), ("Prev", "previous_rank", 5), ("Change", "rank_change", 7), ("Category", "category", 30)],
  "posts": [("Keyword", "keyword", 18), ("Source", "source", 9), ("Kind", "kind", 7), ("Title", "title", 50), ("Published", "published", 10), ("Views", "views", 10), ("Likes", "likes", 8), ("Comments", "comments", 8)],
}

# ----------------------------------------- END: Commands ----------------------------------------------------------------------


# ----------------------------------------- START: CLI -------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
  common = create_common_parser()
  common.add_argument("--max-credits", type=int, default=DEFAULT_MAX_CREDITS, help=f"Abort when the estimate is above this many credits (default: {DEFAULT_MAX_CREDITS})")
  common.add_argument("--credit-price", type=float, default=CREDIT_PRICE_USD, help=f"USD per credit for the estimate (default: {CREDIT_PRICE_USD}, lowest-volume pack 2026-11-10)")
  common.add_argument("--country", default="", help="Country filter where the source supports it, e.g. US")
  parser = argparse.ArgumentParser(description="Trends MCP REST CLI (credits; 1 request = 1 credit; free tier 100 requests per month)")
  subparsers = parser.add_subparsers(dest="command", required=True)
  history_parser = subparsers.add_parser("history", parents=[common], help="get_time_series: about 260 weekly points per keyword")
  history_parser.add_argument("keywords", nargs="+")
  history_parser.add_argument("--source", default="Google Search", help="Series source, e.g. 'Google Search', YouTube, TikTok, Wikipedia (default: Google Search)")
  history_parser.add_argument("--resolution", default="", help="Point resolution where the source supports it")
  history_parser.add_argument("--last", type=int, default=26, help="Table rows per keyword, newest last; 0 = all (default: 26; JSON always has all points)")
  growth_parser = subparsers.add_parser("growth", parents=[common], help="get_growth: percent growth per window")
  growth_parser.add_argument("keywords", nargs="+")
  growth_parser.add_argument("--source", default="Google Search")
  growth_parser.add_argument("--window", nargs="+", default=DEFAULT_WINDOWS, help="Windows such as 7D 1W 3M 12M YTD (default: 7D 3M 12M)")
  board_parser = subparsers.add_parser("board", parents=[common], help="get_top_trends: live ranked board without keyword")
  board_parser.add_argument("--type", dest="types", nargs="+", required=True, help="Board name, e.g. 'Google Trends', 'TikTok Trending Hashtags', 'X (Twitter) Trending' (quote names with spaces)")
  board_parser.add_argument("--limit", type=int, default=10)
  board_parser.add_argument("--climbers", action="store_true", help="Sort by rank change (biggest climbers)")
  board_parser.add_argument("--window", default="", help="Rank-change window where the board supports it")
  posts_parser = subparsers.add_parser("posts", parents=[common], help="get_context: posts, videos, stories about a keyword with engagement")
  posts_parser.add_argument("keywords", nargs="+")
  posts_parser.add_argument("--source", default="News", help="Context source: News, YouTube, TikTok, Instagram, X, Reddit, Bluesky, Hacker News, Polymarket, GitHub (default: News)")
  posts_parser.add_argument("--days", type=int, default=7)
  posts_parser.add_argument("--limit", type=int, default=0, help="Items per source (default: vendor default)")
  return parser

def main():
  if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
  if hasattr(sys.stderr, "reconfigure"): sys.stderr.reconfigure(encoding="utf-8")
  args = build_parser().parse_args()
  estimate = enforce_credit_gate(args)
  keys = load_api_keys(args.keys_file)
  api_key = require_key(keys, "TRENDSMCP_API_KEY", args.keys_file)
  if args.command == "history": outcome = cmd_history(args, api_key)
  elif args.command == "growth": outcome = cmd_growth(args, api_key)
  elif args.command == "board": outcome = cmd_board(args, api_key)
  else: outcome = cmd_posts(args, api_key)
  credits_used = outcome["credits_used"]
  actual_usd = round(credits_used * args.credit_price, 6)
  rows = outcome["rows"]
  log(f"  {plural(len(rows), 'row')} received.")
  notes = list(outcome["notes"])
  notes.append(f"Credits used: {plural(credits_used, 'credit')} = ${actual_usd:.4f} at ${args.credit_price} per credit (estimate {plural(estimate, 'credit')}). Index values compare momentum; absolute volume exists only where 'volume' is shown.")
  result = {"script": SCRIPT_NAME, "command": args.command, "ok": True, "estimated_cost_usd": round(estimate * args.credit_price, 6), "actual_cost_usd": actual_usd,
    "params": {"estimated_credits": estimate, "credits_used": credits_used, "max_credits": args.max_credits}, "rows": rows, "notes": notes}
  if args.format == "table" and args.command == "history" and args.last > 0:
    display_rows = []
    for keyword in args.keywords:
      keyword_rows = []
      for row in rows:
        if row["keyword"] == keyword: keyword_rows.append(row)
      display_rows.extend(keyword_rows[-args.last:])
    result["rows"] = display_rows
  emit(result, args.format, COLUMNS.get(args.command))
  log("OK.")

if __name__ == "__main__":
  main()

# ----------------------------------------- END: CLI ---------------------------------------------------------------------------
