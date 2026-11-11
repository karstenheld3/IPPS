#!/usr/bin/env python3
"""
ScrapeCreators REST API CLI (prepaid credits). Post-level social data for trend depth: TikTok, YouTube, Reddit, Pinterest, Instagram, plus Google results, autocomplete, ads, and transcripts.

Usage:
  python query.py google-search "standing desk" --region US --page 1
  python query.py tiktok-suggestions "standing desk" --region US
  python query.py youtube-typeahead "standing desk"
  python query.py google-ads asana.com --region US
  python query.py youtube-transcript "https://www.youtube.com/watch?v=VIDEO_ID" --cache-max-age 7d
  python query.py tiktok-popular-videos --period 7 --country US   (vendor endpoint unavailable on 2026-11-11)
  python query.py tiktok-search "standing desk" --sort-by most-liked --date-posted this-month
  python query.py youtube-search "standing desk" --sort-by popular --upload-date this_month
  python query.py reddit-search "standing desk" --timeframe month --sort top
  python query.py reddit-subreddit ergonomics --sort top --timeframe week
  python query.py pinterest-topic "https://www.pinterest.com/ideas/standing-desks/123456789/"
  python query.py credit-balance

Billing: most endpoints cost 1 credit, cache hits cost 0 (vendor claim); data responses report `credits_charged` and `credits_remaining`, `credit-balance` reports `creditCount`.
Expensive options (`--param get_ad_details=true` = 25 credits) raise the estimate; see SETUP.md.
X is not covered at depth by this vendor; X trends are listed as a deferred source in SKILL.md.
Credentials: SCRAPECREATORS_API_KEY in [API_KEYS_FILE] (see SKILL.md section "Credential Keys").
"""

import argparse, json, sys, time
from pathlib import Path

import requests

SCRIPT_NAME = "scrapecreators"
SETUP_HINT = "scrapecreators/SETUP.md"
DEFAULT_KEYS_FILE = Path(__file__).resolve().parents[5] / ".tools" / ".api-keys.txt"
API_BASE = "https://api.scrapecreators.com"
CREDIT_PRICE_USD = 0.00188
DEFAULT_MAX_CREDITS = 20
DEFAULT_TABLE_ROWS = 10

# Command table [LITERAL: 2026-11-10]. positional = (argument name, API parameter) or None; options = (flag, API parameter, help); credits = vendor claim per request;
# trim = the endpoint documents `trim=true` for a smaller response; assumed = parameter names not yet confirmed by a live call; expensive_params = `--param` names that raise the price when set to true
ENDPOINTS = {
  "google-search": {"path": "/v1/google/search", "credits": 1, "positional": ("queries", "query"), "trim": False, "assumed": False, "help": "Google organic results (title, URL, description), 10 per page",
    "options": [("--region", "region", "2-letter country code, e.g. US"), ("--date-posted", "date_posted", "last-hour, last-day, last-week, last-month, last-year"), ("--page", "page", "Page 1-11")]},
  "tiktok-suggestions": {"path": "/v1/tiktok/search/suggestions", "credits": 1, "positional": ("queries", "query"), "trim": False, "assumed": False, "help": "TikTok search autocomplete phrases",
    "options": [("--region", "region", "Region code, e.g. US")]},
  "youtube-typeahead": {"path": "/v1/youtube/search/typeahead", "credits": 1, "positional": ("queries", "query"), "trim": False, "assumed": False, "help": "YouTube search autocomplete phrases", "options": []},
  "google-ads": {"path": "/v1/google/company/ads", "credits": 1, "positional": ("domains", "domain"), "trim": False, "assumed": False, "help": "Google Ads Transparency Center ads of an advertiser domain, 40 per page",
    "expensive_params": {"get_ad_details": 25},
    "options": [("--region", "region", "Region, default anywhere"), ("--platform", "platform", "google_maps, google_play, google_search, google_shopping, youtube"), ("--ad-format", "format", "text, image, video"),
      ("--start-date", "start_date", "YYYY-MM-DD"), ("--end-date", "end_date", "YYYY-MM-DD"), ("--cursor", "cursor", "Cursor from a previous response")]},
  "youtube-transcript": {"path": "/v1/youtube/video/transcript", "credits": 1, "positional": ("urls", "url"), "trim": False, "assumed": False, "help": "YouTube video or short transcript (native captions; use --format json for the full text)",
    "options": [("--language", "language", "Language code, e.g. en, es, en-US")]},
  "tiktok-popular-videos": {"path": "/v1/tiktok/videos/popular", "credits": 1, "positional": None, "trim": False, "assumed": True, "help": "Popular TikTok videos by period and country (vendor endpoint unavailable on 2026-11-11)",
    "options": [("--period", "period", "Days, e.g. 7 or 30"), ("--country", "countryCode", "Country code, e.g. US"), ("--page", "page", "Page number"), ("--order-by", "orderBy", "Sort order")]},
  "tiktok-popular-songs": {"path": "/v1/tiktok/songs/popular", "credits": 1, "positional": None, "trim": False, "assumed": True, "help": "Popular TikTok songs (vendor endpoint unavailable on 2026-11-11)",
    "options": [("--period", "period", "Days, e.g. 7 or 30"), ("--country", "countryCode", "Country code, e.g. US"), ("--page", "page", "Page number")]},
  "tiktok-trending-feed": {"path": "/v1/tiktok/get-trending-feed", "credits": 1, "positional": None, "trim": True, "assumed": False, "help": "TikTok trending (For You) feed for a region",
    "options": [("--region", "region", "Proxy region, required by the API (default: US)")]},
  "tiktok-search": {"path": "/v1/tiktok/search/keyword", "credits": 1, "positional": ("queries", "query"), "trim": True, "assumed": False, "help": "TikTok videos matching a keyword",
    "options": [("--date-posted", "date_posted", "yesterday, this-week, this-month, last-3-months, last-6-months, all-time"), ("--sort-by", "sort_by", "relevance, most-liked, date-posted"),
      ("--region", "region", "Proxy region, e.g. US"), ("--cursor", "cursor", "Cursor from a previous response")]},
  "youtube-trending-shorts": {"path": "/v1/youtube/shorts/trending", "credits": 1, "positional": None, "trim": False, "assumed": False, "help": "About 48 trending YouTube Shorts per call", "options": []},
  "youtube-search": {"path": "/v1/youtube/search", "credits": 1, "positional": ("queries", "query"), "trim": False, "assumed": False, "help": "YouTube videos, shorts, channels, playlists for a query",
    "options": [("--upload-date", "uploadDate", "today, this_week, this_month, this_year"), ("--sort-by", "sortBy", "relevance, popular"), ("--type", "type", "videos, shorts, channels, playlists"),
      ("--region", "region", "Proxy region, e.g. US")]},
  "reddit-search": {"path": "/v1/reddit/search", "credits": 1, "positional": ("queries", "query"), "trim": True, "assumed": False, "help": "Reddit posts or comments matching a query",
    "options": [("--filter", "filter", "posts, comments"), ("--sort", "sort", "relevance, new, top, comment_count (posts only)"), ("--timeframe", "timeframe", "all, day, week, month, year (posts only)")]},
  "reddit-subreddit": {"path": "/v1/reddit/subreddit", "credits": 1, "positional": ("names", "subreddit"), "trim": True, "assumed": False, "help": "Recent posts of a subreddit",
    "options": [("--sort", "sort", "best, hot, new, top, rising"), ("--timeframe", "timeframe", "all, day, week, month, year")]},
  "pinterest-topic": {"path": "/v1/pinterest/topic", "credits": 1, "positional": ("urls", "url"), "trim": False, "assumed": True, "help": "Pinterest topic search-interest count and refinement chips from an ideas URL",
    "options": []},
  "instagram-search-reels": {"path": "/v2/instagram/reels/search", "credits": 1, "positional": ("queries", "query"), "trim": False, "assumed": False, "help": "Google-indexed Instagram reels matching a keyword",
    "options": [("--page", "page", "Page 1-11")]},
  "credit-balance": {"path": "/v1/account/credit-balance", "credits": 0, "positional": None, "trim": False, "assumed": False, "help": "Remaining credits (free)", "options": []},
}

NORMALIZED_FIELDS = [
  ("title", ["desc", "title", "name", "text", "advertiserName"]),
  ("author", ["author.unique_id", "author.nickname", "author.name", "author", "channel.title", "channel", "owner.username", "username"]),
  ("views", ["statistics.play_count", "viewCountInt", "views", "play_count", "view_count"]),
  ("likes", ["statistics.digg_count", "score", "ups", "likes", "like_count", "digg_count"]),
  ("comments", ["statistics.comment_count", "num_comments", "comment_count", "comments"]),
  ("shares", ["statistics.share_count", "share_count", "shares"]),
  ("published", ["create_time_utc", "publishedTime", "created_at_iso", "published", "publish_date", "date"]),
  ("url", ["url", "permalink", "adUrl"]),
]

# Fields added for single commands; (output key, source paths)
EXTRA_FIELDS = {
  "google-search": [("description", ["description"])],
  "tiktok-suggestions": [("position", ["position"]), ("language", ["language"]), ("score", ["score"])],
  "youtube-typeahead": [("type", ["type"])],
  "google-ads": [("format", ["format"]), ("first_shown", ["firstShown"]), ("last_shown", ["lastShown"])],
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

def request_values(args, spec: dict) -> list:
  if spec["positional"] is None: return [None]
  return getattr(args, spec["positional"][0])

# Price of one request: base price, raised by `--param KEY=true` for keys listed in the endpoint's expensive_params
def credits_per_request(args, spec: dict) -> int:
  retVal = spec["credits"]
  for pair in args.param:
    if "=" not in pair: continue
    key, value = pair.split("=", 1)
    if value.strip().lower() == "true": retVal = max(retVal, spec.get("expensive_params", {}).get(key.strip(), 0))
  return retVal

def estimate_credits(args, spec: dict) -> tuple:
  request_count = len(request_values(args, spec))
  price = credits_per_request(args, spec)
  return request_count * price, f"{plural(request_count, 'request')} x {price} credit{'s' if price != 1 else ''} (vendor claim, cache hits cost 0)"

def enforce_credit_gate(args, spec: dict) -> int:
  estimate, formula = estimate_credits(args, spec)
  log(f"Estimating credits for '{args.command}' ({formula})...")
  log(f"  Estimate: {plural(estimate, 'credit')} = ${estimate * args.credit_price:.4f} (limit {plural(args.max_credits, 'credit')}).")
  if estimate > args.max_credits: fail(f"Estimate exceeds limit -> rerun with --max-credits {estimate} to allow.", 2)
  return estimate

# ----------------------------------------- END: Credit gate -------------------------------------------------------------------


# ----------------------------------------- START: ScrapeCreators requests -----------------------------------------------------

def call_scrapecreators(path: str, api_key: str, params: dict) -> dict:
  response = http_request("GET", f"{API_BASE}{path}", headers={"x-api-key": api_key}, params=params)
  if response.status_code == 401: fail(f"HTTP 401 -> check SCRAPECREATORS_API_KEY (see '{SETUP_HINT}').", 1)
  if response.status_code == 402: fail(f"HTTP 402 -> credits exhausted or free credits used -> buy credits (see '{SETUP_HINT}').", 1)
  try:
    data = response.json()
  except ValueError:
    fail(f"Non-JSON response -> HTTP {response.status_code} -> {response.text[:200]}", 1)
  if response.status_code == 404: return {"success": True, "not_found": True, "credits_charged": data.get("credits_charged") if isinstance(data, dict) else None}
  if response.status_code >= 400:
    message = ""
    if isinstance(data, dict): message = str(data.get("message") or data.get("error") or "")
    fail(f"{path} -> HTTP {response.status_code} -> {message[:200]}", 1)
  if not isinstance(data, dict): fail(f"{path} -> unexpected response type '{type(data).__name__}'", 1)
  return data

def build_params(args, spec: dict, positional_value: object) -> dict:
  params = {}
  for flag, api_name, help_text in spec["options"]:
    value = getattr(args, "opt_" + flag.lstrip("-").replace("-", "_"), None)
    if value is not None and value != "": params[api_name] = value
  if spec["positional"] is not None: params[spec["positional"][1]] = positional_value
  if spec["trim"] and not args.full: params["trim"] = "true"
  if args.cache_max_age: params["cache_max_age"] = args.cache_max_age
  for pair in args.param:
    if "=" not in pair: fail(f"--param expects KEY=VALUE -> got '{pair}'.", 2)
    key, value = pair.split("=", 1)
    params[key.strip()] = value.strip()
  return params

# ----------------------------------------- END: ScrapeCreators requests -------------------------------------------------------


# ----------------------------------------- START: Row extraction --------------------------------------------------------------

# Scalar at a dotted path inside nested dicts; dicts and lists are not scalars
def get_path(item: dict, path: str) -> object:
  current = item
  for part in path.split("."):
    if not isinstance(current, dict) or part not in current: return None
    current = current[part]
  if isinstance(current, (dict, list)) or current is None or current == "": return None
  return current

def normalize_item(item: dict, extra_fields: list = None) -> dict:
  retVal = {}
  for output_key, paths in NORMALIZED_FIELDS + (extra_fields or []):
    retVal[output_key] = None
    for path in paths:
      value = get_path(item, path)
      if value is not None:
        retVal[output_key] = value
        break
  for text_key in ["title", "description"]:
    if isinstance(retVal.get(text_key), str): retVal[text_key] = " ".join(retVal[text_key].split())
  if isinstance(retVal["published"], str): retVal["published"] = retVal["published"][:10]
  if "score" in retVal: retVal["likes"] = None
  return retVal

# Items of a response: known list keys first, otherwise the first list of dicts
def extract_items(command: str, data: dict) -> list:
  retVal = []
  if command == "tiktok-search":
    for entry in data.get("search_item_list") or []:
      if isinstance(entry, dict) and isinstance(entry.get("aweme_info"), dict): retVal.append(entry["aweme_info"])
    return retVal
  for key in ["aweme_list", "videos", "shorts", "posts", "reels", "items", "songs", "results", "suggestions", "ads", "data"]:
    value = data.get(key)
    if isinstance(value, list):
      for entry in value:
        if isinstance(entry, dict): retVal.append(entry)
  if retVal: return retVal
  for key in data:
    value = data[key]
    if isinstance(value, list) and value and isinstance(value[0], dict):
      for entry in value: retVal.append(entry)
      break
  return retVal

def find_balance(data: dict) -> object:
  for key in ["credits_remaining", "creditCount", "credits", "balance", "remaining"]:
    if isinstance(data.get(key), (int, float)): return data[key]
  return None

COLUMNS = [("Query", "query", 20), ("Title", "title", 50), ("Author", "author", 18), ("Views", "views", 10), ("Likes", "likes", 8), ("Comments", "comments", 8), ("Published", "published", 10), ("URL", "url", 40)]
TOPIC_COLUMNS = [("Topic", "name", 30), ("Search count", "search_count", 12), ("Updated", "updated_at", 20), ("Refinements", "refinement_count", 11), ("URL", "url", 50)]
TRANSCRIPT_COLUMNS = [("URL", "query", 44), ("Language", "language", 10), ("Characters", "characters", 10), ("Segments", "segments", 8), ("Text", "text", 80)]
COMMAND_COLUMNS = {
  "google-search": [("Query", "query", 20), ("Title", "title", 50), ("Description", "description", 50), ("URL", "url", 50)],
  "tiktok-suggestions": [("Query", "query", 20), ("Suggestion", "title", 50), ("Position", "position", 8), ("Score", "score", 8), ("Language", "language", 8)],
  "youtube-typeahead": [("Query", "query", 20), ("Suggestion", "title", 50), ("Type", "type", 10)],
  "google-ads": [("Query", "query", 20), ("Advertiser", "title", 30), ("Format", "format", 8), ("First shown", "first_shown", 10), ("Last shown", "last_shown", 10), ("URL", "url", 70)],
  "youtube-transcript": TRANSCRIPT_COLUMNS,
}

# ----------------------------------------- END: Row extraction ----------------------------------------------------------------


# ----------------------------------------- START: Commands --------------------------------------------------------------------

def run_balance(args, api_key: str) -> dict:
  log("Fetching credit balance...")
  data = call_scrapecreators(ENDPOINTS["credit-balance"]["path"], api_key, {})
  balance = find_balance(data)
  rows = [{"credits_remaining": balance}]
  notes = [f"Credits remaining: {balance if balance is not None else '[UNKNOWN] (response keys: ' + ', '.join(sorted(data.keys())) + ')'}"]
  return {"rows": rows, "notes": notes, "credits_charged": 0, "credits_remaining": balance, "columns": [("Credits remaining", "credits_remaining", 17)], "stopped": False}

def run_requests(args, spec: dict, api_key: str) -> dict:
  values = request_values(args, spec)
  rows = []
  notes = []
  credits_charged = 0
  credits_remaining = None
  stopped = False
  columns = COMMAND_COLUMNS.get(args.command, COLUMNS)
  for index in range(len(values)):
    if index > 0 and credits_charged >= args.max_credits:
      stopped = True
      notes.append(f"Stopped after {plural(index, 'request')}: {plural(credits_charged, 'credit')} charged reached --max-credits {args.max_credits}; {plural(len(values) - index, 'request')} not sent.")
      break
    label = values[index] if values[index] is not None else args.command
    log(f"  [ {index + 1} / {len(values)} ] {args.command} '{label}'...")
    data = call_scrapecreators(spec["path"], api_key, build_params(args, spec, values[index]))
    charged = data.get("credits_charged")
    credits_charged += charged if isinstance(charged, (int, float)) else credits_per_request(args, spec)
    if data.get("credits_remaining") is not None: credits_remaining = data["credits_remaining"]
    if data.get("not_found"):
      notes.append(f"'{label}': 0 rows (not found)")
      continue
    if args.command == "pinterest-topic":
      columns = TOPIC_COLUMNS
      refinements = data.get("refinements") or []
      rows.append({"query": label, "name": data.get("name", ""), "search_count": data.get("search_count"), "updated_at": data.get("updated_at", ""), "refinement_count": len(refinements), "url": data.get("url", label)})
      labels = []
      for chip in refinements[:10]:
        if isinstance(chip, dict): labels.append(str(chip.get("label") or chip.get("name") or ""))
      if labels: notes.append(f"Refinements of '{data.get('name', label)}': {', '.join(labels)}")
      notes.append("search_count is Pinterest's native internal count; its period is unspecified, it is not monthly search volume.")
      continue
    if args.command == "youtube-transcript":
      text = " ".join(str(data.get("transcript_only_text") or "").split())
      if not text:
        notes.append(f"'{label}': 0 rows (no transcript)")
        continue
      rows.append({"query": label, "language": data.get("language", ""), "characters": len(text), "segments": len(data.get("transcript") or []), "text": text})
      continue
    items = extract_items(args.command, data)
    if not items: notes.append(f"'{label}': 0 rows")
    for item in items:
      row = normalize_item(item, EXTRA_FIELDS.get(args.command))
      row["query"] = label
      rows.append(row)
  return {"rows": rows, "notes": notes, "credits_charged": credits_charged, "credits_remaining": credits_remaining, "columns": columns, "stopped": stopped}

# ----------------------------------------- END: Commands ----------------------------------------------------------------------


# ----------------------------------------- START: CLI -------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
  common = create_common_parser()
  common.add_argument("--max-credits", type=int, default=DEFAULT_MAX_CREDITS, help=f"Abort when the estimate is above this many credits; a running batch stops when this many are charged (default: {DEFAULT_MAX_CREDITS})")
  common.add_argument("--credit-price", type=float, default=CREDIT_PRICE_USD, help=f"USD per credit for the estimate (default: {CREDIT_PRICE_USD}, lowest-volume pack 2026-11-10)")
  common.add_argument("--rows", type=int, default=DEFAULT_TABLE_ROWS, help=f"Table rows per request; 0 = all; JSON always has all rows (default: {DEFAULT_TABLE_ROWS})")
  common.add_argument("--cache-max-age", choices=["1d", "3d", "7d", "14d", "30d"], default="", help="Accept a cached response of this age or newer (0 credits)")
  common.add_argument("--full", action="store_true", help="Do not request the trimmed response where the endpoint supports `trim`")
  common.add_argument("--param", action="append", default=[], metavar="KEY=VALUE", help="Extra vendor parameter, repeatable")
  parser = argparse.ArgumentParser(description="ScrapeCreators REST CLI (credits; most endpoints cost 1 credit; 100 free credits)")
  subparsers = parser.add_subparsers(dest="command", required=True)
  for command in ENDPOINTS:
    spec = ENDPOINTS[command]
    sub = subparsers.add_parser(command, parents=[common], help=spec["help"])
    if spec["positional"] is not None: sub.add_argument(spec["positional"][0], nargs="+")
    for flag, api_name, help_text in spec["options"]:
      default = "US" if (command == "tiktok-trending-feed" and flag == "--region") else None
      sub.add_argument(flag, dest="opt_" + flag.lstrip("-").replace("-", "_"), default=default, help=help_text)
  return parser

def main():
  if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
  if hasattr(sys.stderr, "reconfigure"): sys.stderr.reconfigure(encoding="utf-8")
  args = build_parser().parse_args()
  spec = ENDPOINTS[args.command]
  estimate = 0
  if args.command != "credit-balance": estimate = enforce_credit_gate(args, spec)
  keys = load_api_keys(args.keys_file)
  api_key = require_key(keys, "SCRAPECREATORS_API_KEY", args.keys_file)
  if args.command == "credit-balance": outcome = run_balance(args, api_key)
  else: outcome = run_requests(args, spec, api_key)
  rows = outcome["rows"]
  log(f"  {plural(len(rows), 'row')} received.")
  credits_charged = outcome["credits_charged"]
  actual_usd = round(credits_charged * args.credit_price, 6)
  notes = list(outcome["notes"])
  if args.command != "credit-balance":
    remaining_text = f", {plural(int(outcome['credits_remaining']), 'credit')} remaining" if outcome["credits_remaining"] is not None else ""
    notes.append(f"Credits charged: {plural(credits_charged, 'credit')} = ${actual_usd:.4f} at ${args.credit_price} per credit (estimate {plural(estimate, 'credit')}){remaining_text}.")
  result = {"script": SCRIPT_NAME, "command": args.command, "ok": True, "estimated_cost_usd": round(estimate * args.credit_price, 6), "actual_cost_usd": actual_usd,
    "params": {"estimated_credits": estimate, "credits_charged": credits_charged, "credits_remaining": outcome["credits_remaining"], "max_credits": args.max_credits, "stopped_at_max_credits": outcome["stopped"]},
    "rows": rows, "notes": notes}
  if args.format == "table" and args.rows > 0 and args.command not in ["credit-balance", "pinterest-topic"]:
    display_rows = []
    seen_counts = {}
    for row in rows:
      seen_counts[row["query"]] = seen_counts.get(row["query"], 0) + 1
      if seen_counts[row["query"]] <= args.rows: display_rows.append(row)
    result["rows"] = display_rows
  emit(result, args.format, outcome["columns"])
  log("OK.")

if __name__ == "__main__":
  main()

# ----------------------------------------- END: CLI ---------------------------------------------------------------------------
