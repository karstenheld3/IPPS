#!/usr/bin/env python3
"""
YouTube Data API v3 CLI (free, 10,000 quota units per day). Video demand and competition research.

Usage:
  python query.py search "kanban board tutorial" --max-results 25
  python query.py videos VIDEO_ID [VIDEO_ID ...]

Quota: search.list = 100 units per call, videos.list = 1 unit per call (up to 50 IDs).
Credentials: YOUTUBE_API_KEY in [API_KEYS_FILE] (see SKILL.md section "Credential Keys").
"""

import argparse, json, sys, time
from pathlib import Path

import requests

SCRIPT_NAME = "youtube"
SETUP_HINT = "youtube/SETUP.md"
DEFAULT_KEYS_FILE = Path(__file__).resolve().parents[5] / ".tools" / ".api-keys.txt"
API_BASE = "https://www.googleapis.com/youtube/v3"
SEARCH_UNITS = 100
VIDEOS_UNITS = 1
VIDEOS_BATCH_SIZE = 50

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


# ----------------------------------------- START: YouTube Data API ------------------------------------------------------------

def call_youtube(resource: str, api_key: str, params: dict) -> dict:
  query = {"key": api_key}
  for name in params: query[name] = params[name]
  response = http_request("GET", f"{API_BASE}/{resource}", params=query)
  data = parse_json(response)
  if response.status_code == 200: return data
  error = data.get("error") or {} if isinstance(data, dict) else {}
  reasons = []
  for item in error.get("errors") or []: reasons.append(item.get("reason", ""))
  if "quotaExceeded" in reasons: fail("Daily quota exceeded (10,000 units) -> resets at midnight Pacific Time.", 1)
  hint = f" -> check YOUTUBE_API_KEY and that YouTube Data API v3 is enabled (see '{SETUP_HINT}')" if response.status_code in [400, 403] else ""
  fail(f"{resource} -> HTTP {response.status_code} -> {str(error.get('message', ''))[:200]}{hint}", 1)

def cmd_search(args, api_key: str) -> tuple:
  log(f"Searching YouTube for '{args.query}' (max {args.max_results} results, {SEARCH_UNITS} units)...")
  params = {"part": "snippet", "q": args.query, "type": "video", "order": "relevance", "maxResults": args.max_results}
  if args.region: params["regionCode"] = args.region
  if args.lang: params["relevanceLanguage"] = args.lang
  data = call_youtube("search", api_key, params)
  rows = []
  for item in data.get("items") or []:
    snippet = item.get("snippet") or {}
    rows.append({"video_id": (item.get("id") or {}).get("videoId", ""), "title": snippet.get("title", ""), "channel": snippet.get("channelTitle", ""), "published": (snippet.get("publishedAt") or "")[:10]})
  notes = [f"Total results estimate: {(data.get('pageInfo') or {}).get('totalResults', '[UNKNOWN]')}"]
  log(f"  {plural(len(rows), 'video')} received.")
  return rows, notes, SEARCH_UNITS

def cmd_videos(args, api_key: str) -> tuple:
  rows = []
  units = 0
  batch_count = (len(args.ids) + VIDEOS_BATCH_SIZE - 1) // VIDEOS_BATCH_SIZE
  log(f"Fetching statistics for {plural(len(args.ids), 'video')} ({plural(batch_count, 'call')}, {plural(batch_count * VIDEOS_UNITS, 'unit')})...")
  for batch_index in range(batch_count):
    batch = args.ids[batch_index * VIDEOS_BATCH_SIZE:(batch_index + 1) * VIDEOS_BATCH_SIZE]
    data = call_youtube("videos", api_key, {"part": "snippet,statistics", "id": ",".join(batch)})
    units += VIDEOS_UNITS
    for item in data.get("items") or []:
      snippet = item.get("snippet") or {}
      statistics_data = item.get("statistics") or {}
      rows.append({"video_id": item.get("id", ""), "title": snippet.get("title", ""), "channel": snippet.get("channelTitle", ""), "published": (snippet.get("publishedAt") or "")[:10], "views": int(statistics_data.get("viewCount") or 0), "likes": int(statistics_data.get("likeCount") or 0), "comments": int(statistics_data.get("commentCount") or 0)})
  log(f"  {plural(len(rows), 'video')} received.")
  return rows, [], units

COLUMNS = {
  "search": [("Video ID", "video_id", 12), ("Title", "title", 60), ("Channel", "channel", 25), ("Published", "published", 10)],
  "videos": [("Video ID", "video_id", 12), ("Title", "title", 50), ("Views", "views", 12), ("Likes", "likes", 9), ("Comments", "comments", 9), ("Published", "published", 10)],
}

# ----------------------------------------- END: YouTube Data API --------------------------------------------------------------


# ----------------------------------------- START: CLI -------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
  common = create_common_parser()
  parser = argparse.ArgumentParser(description="YouTube Data API v3 CLI (10,000 units per day)")
  subparsers = parser.add_subparsers(dest="command", required=True)
  search_parser = subparsers.add_parser("search", parents=[common], help="search.list (100 units)")
  search_parser.add_argument("query")
  search_parser.add_argument("--max-results", type=int, default=25, help="1-50 (default: 25)")
  search_parser.add_argument("--region", default="", help="ISO 3166-1 alpha-2, e.g. US")
  search_parser.add_argument("--lang", default="", help="ISO 639-1, e.g. en")
  videos_parser = subparsers.add_parser("videos", parents=[common], help="videos.list statistics (1 unit per 50 IDs)")
  videos_parser.add_argument("ids", nargs="+")
  return parser

def main():
  if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
  if hasattr(sys.stderr, "reconfigure"): sys.stderr.reconfigure(encoding="utf-8")
  args = build_parser().parse_args()
  keys = load_api_keys(args.keys_file)
  api_key = require_key(keys, "YOUTUBE_API_KEY", args.keys_file)
  if args.command == "search": rows, notes, units = cmd_search(args, api_key)
  else: rows, notes, units = cmd_videos(args, api_key)
  notes.append(f"Quota units used: {units} (daily default 10,000).")
  result = {"script": SCRIPT_NAME, "command": args.command, "ok": True, "estimated_cost_usd": 0.0, "actual_cost_usd": 0.0, "params": {"quota_units": units}, "rows": rows, "notes": notes}
  emit(result, args.format, COLUMNS.get(args.command))
  log("OK.")

if __name__ == "__main__":
  main()

# ----------------------------------------- END: CLI ---------------------------------------------------------------------------
