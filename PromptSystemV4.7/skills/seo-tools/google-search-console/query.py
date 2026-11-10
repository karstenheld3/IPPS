#!/usr/bin/env python3
"""
Google Search Console CLI (free). Search Analytics, URL Inspection, sitemaps, and derived analyses.

Usage:
  python query.py sites
  python query.py analytics sc-domain:example.com --dimensions query,page --rows 1000
  python query.py inspect https://example.com/ https://example.com/blog/post
  python query.py sitemaps https://example.com/ --submit https://example.com/sitemap.xml
  python query.py quick-wins sc-domain:example.com
  python query.py ctr-gap sc-domain:example.com
  python query.py decay sc-domain:example.com
  python query.py cannibalization sc-domain:example.com

Credentials: GSC_SERVICE_ACCOUNT_FILE in [API_KEYS_FILE] (file name relative to the keys file folder; see SKILL.md section "Credential Keys").
"""

import argparse, datetime, json, statistics, sys, time
from pathlib import Path
from urllib.parse import quote

import requests
from google.auth.transport.requests import AuthorizedSession
from google.oauth2 import service_account

SCRIPT_NAME = "google-search-console"
SETUP_HINT = "google-search-console/SETUP.md"
DEFAULT_KEYS_FILE = Path(__file__).resolve().parents[5] / ".tools" / ".api-keys.txt"
API_BASE = "https://www.googleapis.com/webmasters/v3"
INSPECTION_URL = "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect"
SCOPE_READ = "https://www.googleapis.com/auth/webmasters.readonly"
SCOPE_WRITE = "https://www.googleapis.com/auth/webmasters"
MAX_ROWS_PER_REQUEST = 25000
DATA_LAG_DAYS = 3
RETENTION_DAYS = 486

# Defaults identical to SEO_CHECKS.md constants block
QUICK_WIN_MIN_POSITION = 4.0
QUICK_WIN_MAX_POSITION = 15.0
CTR_GAP_DAYS = 90
CTR_GAP_MIN_IMPRESSIONS = 1000
CTR_GAP_RATIO = 0.60
CTR_GAP_MIN_BUCKET_PAGES = 5
CTR_GAP_BUCKETS = [(1.0, 1.9), (2.0, 2.9), (3.0, 3.9), (4.0, 5.9), (6.0, 10.9)]
DECAY_MIN_LOSS_PERCENT = 20.0
DECAY_MIN_LOST_CLICKS = 50
CANNIBALIZATION_MIN_SHARE = 0.10
CANNIBALIZATION_MIN_QUERY_IMPRESSIONS = 100

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

# HTTP request with timeout and retry on 429 and 5xx (1s, 2s, 4s; honors Retry-After); session = authorized session or None
def http_request(method: str, url: str, headers: dict = None, params: dict = None, json_body: object = None, timeout: int = 30, session: object = None) -> requests.Response:
  delays = [1, 2, 4]
  attempt = 0
  client = session if session is not None else requests
  while True:
    try:
      response = client.request(method, url, headers=headers, params=params, json=json_body, timeout=timeout)
    except Exception as error:
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


# ----------------------------------------- START: GSC access ------------------------------------------------------------------

# Resolve service account JSON: relative values resolve against the keys file folder
def resolve_service_account_file(keys: dict, keys_file: Path) -> Path:
  value = require_key(keys, "GSC_SERVICE_ACCOUNT_FILE", keys_file)
  retVal = Path(value)
  if not retVal.is_absolute(): retVal = keys_file.parent / retVal
  if not retVal.is_file(): fail(f"Service account file not found -> '{retVal}' -> see '{SETUP_HINT}'.", 2)
  return retVal

def create_session(keys_file: Path, write_access: bool) -> AuthorizedSession:
  keys = load_api_keys(keys_file)
  account_file = resolve_service_account_file(keys, keys_file)
  scope = SCOPE_WRITE if write_access else SCOPE_READ
  try:
    credentials = service_account.Credentials.from_service_account_file(str(account_file), scopes=[scope])
  except (ValueError, KeyError) as error:
    fail(f"Service account file invalid -> '{account_file.name}' -> {type(error).__name__}", 2)
  return AuthorizedSession(credentials)

def check_response(response: requests.Response, context: str) -> object:
  data = parse_json(response)
  if response.status_code == 200: return data
  message = ""
  if isinstance(data, dict): message = (data.get("error") or {}).get("message", "")
  hint = ""
  if response.status_code == 403: hint = f" -> enable Search Console API and add the service account as user (Full for sitemap submit), see '{SETUP_HINT}'"
  if response.status_code == 401: hint = f" -> service account credentials rejected, see '{SETUP_HINT}'"
  fail(f"{context} -> HTTP {response.status_code} -> {message[:200]}{hint}", 1)

def site_path(site: str) -> str:
  return quote(site, safe="")

# Fetch Search Analytics rows with pagination (25,000 rows per request)
def query_search_analytics(session: AuthorizedSession, site: str, body: dict, max_rows: int) -> list:
  retVal = []
  start_row = 0
  url = f"{API_BASE}/sites/{site_path(site)}/searchAnalytics/query"
  while len(retVal) < max_rows:
    request_rows = min(MAX_ROWS_PER_REQUEST, max_rows - len(retVal))
    page_body = dict(body)
    page_body["rowLimit"] = request_rows
    page_body["startRow"] = start_row
    data = check_response(http_request("POST", url, json_body=page_body, session=session), f"Search Analytics '{site}'")
    rows = data.get("rows") or []
    for row in rows: retVal.append(row)
    if len(rows) < request_rows: break
    start_row += len(rows)
  return retVal

def flatten_rows(rows: list, dimensions: list) -> list:
  retVal = []
  for row in rows:
    flat = {}
    keys = row.get("keys") or []
    for index in range(len(dimensions)):
      flat[dimensions[index]] = keys[index] if index < len(keys) else ""
    flat["clicks"] = row.get("clicks", 0)
    flat["impressions"] = row.get("impressions", 0)
    flat["ctr"] = round(row.get("ctr", 0.0), 4)
    flat["position"] = round(row.get("position", 0.0), 1)
    retVal.append(flat)
  return retVal

def last_available_day() -> datetime.date:
  return datetime.datetime.now(datetime.timezone.utc).date() - datetime.timedelta(days=DATA_LAG_DAYS)

def date_window(days: int) -> tuple:
  end_date = last_available_day()
  start_date = end_date - datetime.timedelta(days=days - 1)
  return start_date, end_date

def base_body(start_date: datetime.date, end_date: datetime.date, dimensions: list, search_type: str) -> dict:
  return {"startDate": start_date.isoformat(), "endDate": end_date.isoformat(), "dimensions": dimensions, "type": search_type}

# ----------------------------------------- END: GSC access --------------------------------------------------------------------


# ----------------------------------------- START: Derived analyses (pure functions, testable offline) -------------------------

def find_bucket(position: float) -> tuple:
  for bucket in CTR_GAP_BUCKETS:
    if bucket[0] <= position <= bucket[1]: return bucket
  return None

# Pages at position 1.0-10.9 with >= min_impressions and CTR < ratio * median page CTR of their position bucket
def compute_ctr_gap(rows: list, min_impressions: int, ratio: float) -> list:
  retVal = []
  bucket_ctrs = {}
  for row in rows:
    bucket = find_bucket(row["position"])
    if bucket is None or row["impressions"] <= 0: continue
    if bucket not in bucket_ctrs: bucket_ctrs[bucket] = []
    bucket_ctrs[bucket].append(row["ctr"])
  for row in rows:
    bucket = find_bucket(row["position"])
    if bucket is None or row["impressions"] < min_impressions: continue
    bucket_label = f"{bucket[0]:.1f}-{bucket[1]:.1f}"
    ctr_values = bucket_ctrs.get(bucket, [])
    if len(ctr_values) < CTR_GAP_MIN_BUCKET_PAGES:
      retVal.append({"page": row["page"], "position": row["position"], "impressions": row["impressions"], "ctr": row["ctr"], "expected_ctr": None, "bucket": bucket_label, "status": "INSUFFICIENT_BASELINE"})
      continue
    expected_ctr = statistics.median(ctr_values)
    if row["ctr"] < ratio * expected_ctr:
      retVal.append({"page": row["page"], "position": row["position"], "impressions": row["impressions"], "ctr": row["ctr"], "expected_ctr": round(expected_ctr, 4), "bucket": bucket_label, "status": "RE-TITLE"})
  retVal.sort(key=impressions_sort_key, reverse=True)
  return retVal

# Pages that lost >= min_lost_clicks and >= min_loss_percent clicks between previous and current window
def compute_decay(current_rows: list, previous_rows: list, min_loss_percent: float, min_lost_clicks: int) -> list:
  retVal = []
  current_by_page = {}
  for row in current_rows: current_by_page[row["page"]] = row
  for previous in previous_rows:
    current = current_by_page.get(previous["page"], {"clicks": 0, "impressions": 0, "position": 0.0})
    lost_clicks = previous["clicks"] - current["clicks"]
    if previous["clicks"] <= 0 or lost_clicks < min_lost_clicks: continue
    loss_percent = 100.0 * lost_clicks / previous["clicks"]
    if loss_percent < min_loss_percent: continue
    position_delta = round(current["position"] - previous["position"], 1) if current["position"] else None
    retVal.append({"page": previous["page"], "clicks_previous": previous["clicks"], "clicks_current": current["clicks"], "loss_percent": round(loss_percent, 1), "impressions_previous": previous["impressions"], "impressions_current": current["impressions"], "position_previous": previous["position"], "position_current": current["position"], "position_delta": position_delta})
  retVal.sort(key=lost_clicks_sort_key, reverse=True)
  return retVal

# Queries where >= 2 pages each receive >= min_share of the query's impressions
def compute_cannibalization(rows: list, min_share: float, min_query_impressions: int = 0) -> list:
  retVal = []
  pages_by_query = {}
  for row in rows:
    if row["query"] not in pages_by_query: pages_by_query[row["query"]] = []
    pages_by_query[row["query"]].append(row)
  for query in pages_by_query:
    query_rows = pages_by_query[query]
    total_impressions = 0
    for row in query_rows: total_impressions += row["impressions"]
    if total_impressions <= 0 or total_impressions < min_query_impressions: continue
    competing_pages = []
    for row in query_rows:
      share = row["impressions"] / total_impressions
      if share >= min_share: competing_pages.append(f"{row['page']} ({share:.0%}, pos {row['position']})")
    if len(competing_pages) >= 2: retVal.append({"query": query, "impressions": total_impressions, "pages": len(competing_pages), "competing_pages": "; ".join(competing_pages)})
  retVal.sort(key=impressions_sort_key, reverse=True)
  return retVal

def impressions_sort_key(row: dict) -> int:
  return row.get("impressions") or 0

def lost_clicks_sort_key(row: dict) -> int:
  return row["clicks_previous"] - row["clicks_current"]

# Last 3 full months with data and the same months one year earlier
def decay_windows() -> tuple:
  last_day = last_available_day()
  current_end = last_day.replace(day=1) - datetime.timedelta(days=1)
  current_start = shift_months(current_end.replace(day=1), -2)
  previous_start = shift_months(current_start, -12)
  previous_end = shift_months(current_end.replace(day=1), -12)
  previous_end = shift_months(previous_end, 1) - datetime.timedelta(days=1)
  return current_start, current_end, previous_start, previous_end

def shift_months(date_value: datetime.date, months: int) -> datetime.date:
  month_index = date_value.year * 12 + (date_value.month - 1) + months
  return datetime.date(month_index // 12, month_index % 12 + 1, 1)

# ----------------------------------------- END: Derived analyses --------------------------------------------------------------


# ----------------------------------------- START: Commands --------------------------------------------------------------------

def cmd_sites(args) -> dict:
  session = create_session(args.keys_file, False)
  log("Listing Search Console properties...")
  data = check_response(http_request("GET", f"{API_BASE}/sites", session=session), "Sites")
  rows = []
  for entry in data.get("siteEntry") or []: rows.append({"site": entry.get("siteUrl", ""), "permission": entry.get("permissionLevel", "")})
  log(f"  {plural(len(rows), 'property', 'properties')} found.")
  return {"rows": rows, "notes": [] if rows else ["0 properties: add the service account email as user in Search Console (see SETUP.md)."]}

def cmd_analytics(args) -> dict:
  session = create_session(args.keys_file, False)
  dimensions = []
  for part in args.dimensions.split(","):
    if part.strip(): dimensions.append(part.strip())
  start_date, end_date = date_window(28)
  if args.start: start_date = datetime.date.fromisoformat(args.start)
  if args.end: end_date = datetime.date.fromisoformat(args.end)
  body = base_body(start_date, end_date, dimensions, args.search_type)
  filters = []
  for filter_text in args.filter:
    parts = filter_text.split(":", 2)
    if len(parts) != 3: fail(f"Invalid filter '{filter_text}' -> expected DIMENSION:OPERATOR:VALUE (operator: equals, contains, notContains, notEquals, includingRegex, excludingRegex)", 2)
    filters.append({"dimension": parts[0], "operator": parts[1], "expression": parts[2]})
  if filters: body["dimensionFilterGroups"] = [{"filters": filters}]
  log(f"Fetching Search Analytics for '{args.site}' ({start_date} to {end_date}, dimensions: {', '.join(dimensions)})...")
  rows = flatten_rows(query_search_analytics(session, args.site, body, args.rows), dimensions)
  log(f"  {plural(len(rows), 'row')} received.")
  return {"rows": rows, "notes": [], "columns": dimension_columns(dimensions)}

def cmd_inspect(args) -> dict:
  session = create_session(args.keys_file, False)
  rows = []
  for index in range(len(args.urls)):
    url = args.urls[index]
    log(f"  [ {index + 1} / {len(args.urls)} ] Inspecting '{url}'...")
    body = {"inspectionUrl": url, "siteUrl": args.site, "languageCode": "en-US"}
    data = check_response(http_request("POST", INSPECTION_URL, json_body=body, session=session), f"URL Inspection '{url}'")
    result = data.get("inspectionResult") or {}
    index_status = result.get("indexStatusResult") or {}
    rows.append({"url": url, "verdict": index_status.get("verdict", ""), "coverage": index_status.get("coverageState", ""), "user_canonical": index_status.get("userCanonical", ""), "google_canonical": index_status.get("googleCanonical", ""), "last_crawl": index_status.get("lastCrawlTime", ""), "robots": index_status.get("robotsTxtState", ""), "mobile": (result.get("mobileUsabilityResult") or {}).get("verdict", ""), "rich_results": (result.get("richResultsResult") or {}).get("verdict", "")})
  return {"rows": rows, "notes": ["URL Inspection quota: 2,000 per day and 600 per minute per property."]}

def cmd_sitemaps(args) -> dict:
  session = create_session(args.keys_file, bool(args.submit))
  if args.submit:
    log(f"Submitting sitemap '{args.submit}' for '{args.site}'...")
    response = http_request("PUT", f"{API_BASE}/sites/{site_path(args.site)}/sitemaps/{quote(args.submit, safe='')}", session=session)
    if response.status_code not in [200, 204]: check_response(response, f"Sitemap submit '{args.submit}'")
    log("  Submitted.")
  log(f"Listing sitemaps for '{args.site}'...")
  data = check_response(http_request("GET", f"{API_BASE}/sites/{site_path(args.site)}/sitemaps", session=session), "Sitemaps")
  rows = []
  for entry in data.get("sitemap") or []:
    submitted_count = 0
    for content in entry.get("contents") or []: submitted_count += int(content.get("submitted") or 0)
    rows.append({"path": entry.get("path", ""), "last_submitted": entry.get("lastSubmitted", ""), "last_downloaded": entry.get("lastDownloaded", ""), "errors": entry.get("errors", 0), "warnings": entry.get("warnings", 0), "urls_submitted": submitted_count})
  log(f"  {plural(len(rows), 'sitemap')} found.")
  return {"rows": rows, "notes": []}

def cmd_quick_wins(args) -> dict:
  session = create_session(args.keys_file, False)
  start_date, end_date = date_window(args.days)
  log(f"Fetching queries for '{args.site}' ({start_date} to {end_date})...")
  rows = flatten_rows(query_search_analytics(session, args.site, base_body(start_date, end_date, ["query"], "web"), 25000), ["query"])
  candidates = []
  for row in rows:
    if QUICK_WIN_MIN_POSITION <= row["position"] <= QUICK_WIN_MAX_POSITION: candidates.append(row)
  candidates.sort(key=impressions_sort_key, reverse=True)
  log(f"  {plural(len(candidates), 'query', 'queries')} at position {QUICK_WIN_MIN_POSITION:.0f}-{QUICK_WIN_MAX_POSITION:.0f}.")
  return {"rows": candidates[:args.limit], "notes": []}

def cmd_ctr_gap(args) -> dict:
  session = create_session(args.keys_file, False)
  start_date, end_date = date_window(CTR_GAP_DAYS)
  log(f"Fetching pages for '{args.site}' ({start_date} to {end_date})...")
  rows = flatten_rows(query_search_analytics(session, args.site, base_body(start_date, end_date, ["page"], "web"), 25000), ["page"])
  log(f"Computing CTR gap (>= {args.min_impressions:,} impressions, CTR < {args.ratio:.2f} x bucket median)...")
  candidates = compute_ctr_gap(rows, args.min_impressions, args.ratio)
  log(f"  {plural(len(candidates), 'page')} match.")
  return {"rows": candidates[:args.limit], "notes": []}

def cmd_decay(args) -> dict:
  session = create_session(args.keys_file, False)
  current_start, current_end, previous_start, previous_end = decay_windows()
  if (last_available_day() - previous_start).days > RETENTION_DAYS: fail(f"Year-ago window starts {previous_start} -> outside GSC 16-month retention.", 2)
  log(f"Fetching Search Analytics for '{args.site}' (dimension: page)...")
  log(f"  [ 1 / 2 ] Current window {current_start} to {current_end}...")
  current_rows = flatten_rows(query_search_analytics(session, args.site, base_body(current_start, current_end, ["page"], "web"), 25000), ["page"])
  log(f"    {plural(len(current_rows), 'row')}.")
  log(f"  [ 2 / 2 ] Year-ago window {previous_start} to {previous_end}...")
  previous_rows = flatten_rows(query_search_analytics(session, args.site, base_body(previous_start, previous_end, ["page"], "web"), 25000), ["page"])
  log(f"    {plural(len(previous_rows), 'row')}.")
  log(f"Computing decay (threshold {args.min_loss_percent:.0f}% and {args.min_lost_clicks} clicks)...")
  candidates = compute_decay(current_rows, previous_rows, args.min_loss_percent, args.min_lost_clicks)
  log(f"  {plural(len(candidates), 'page')} match.")
  notes = ["Classify each page with the 4 decay signatures in SEO_CHECKS.md (position delta, impressions trend, AI Overview, Trends)."]
  return {"rows": candidates[:args.limit], "notes": notes}

def cmd_cannibalization(args) -> dict:
  session = create_session(args.keys_file, False)
  start_date, end_date = date_window(args.days)
  log(f"Fetching query and page rows for '{args.site}' ({start_date} to {end_date})...")
  rows = flatten_rows(query_search_analytics(session, args.site, base_body(start_date, end_date, ["query", "page"], "web"), 100000), ["query", "page"])
  log(f"Computing cannibalization (>= 2 pages with >= {args.min_share:.0%} impression share)...")
  candidates = compute_cannibalization(rows, args.min_share, args.min_query_impressions)
  log(f"  {plural(len(candidates), 'query', 'queries')} match.")
  return {"rows": candidates[:args.limit], "notes": []}

def dimension_columns(dimensions: list) -> list:
  retVal = []
  for dimension in dimensions: retVal.append((dimension, dimension, 60 if dimension in ["page", "query"] else 14))
  retVal.append(("Clicks", "clicks", 8))
  retVal.append(("Impressions", "impressions", 11))
  retVal.append(("CTR", "ctr", 7))
  retVal.append(("Pos", "position", 5))
  return retVal

COLUMNS = {
  "sites": [("Site", "site", 50), ("Permission", "permission", 20)],
  "inspect": [("URL", "url", 50), ("Verdict", "verdict", 8), ("Coverage", "coverage", 30), ("Last crawl", "last_crawl", 20), ("Rich results", "rich_results", 12)],
  "sitemaps": [("Path", "path", 50), ("Last downloaded", "last_downloaded", 25), ("Errors", "errors", 6), ("Warnings", "warnings", 8), ("URLs", "urls_submitted", 8)],
  "quick-wins": [("Query", "query", 50), ("Clicks", "clicks", 8), ("Impressions", "impressions", 11), ("CTR", "ctr", 7), ("Pos", "position", 5)],
  "ctr-gap": [("Page", "page", 55), ("Pos", "position", 5), ("Impressions", "impressions", 11), ("CTR", "ctr", 7), ("Expected", "expected_ctr", 8), ("Status", "status", 22)],
  "decay": [("Page", "page", 50), ("Clicks before", "clicks_previous", 13), ("Clicks now", "clicks_current", 10), ("Loss %", "loss_percent", 7), ("Pos delta", "position_delta", 9)],
  "cannibalization": [("Query", "query", 40), ("Impressions", "impressions", 11), ("Pages", "pages", 5), ("Competing pages", "competing_pages", 80)],
}

COMMANDS = {"sites": cmd_sites, "analytics": cmd_analytics, "inspect": cmd_inspect, "sitemaps": cmd_sitemaps, "quick-wins": cmd_quick_wins, "ctr-gap": cmd_ctr_gap, "decay": cmd_decay, "cannibalization": cmd_cannibalization}

# ----------------------------------------- END: Commands ----------------------------------------------------------------------


# ----------------------------------------- START: CLI -------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
  common = create_common_parser()
  parser = argparse.ArgumentParser(description="Google Search Console CLI (Search Analytics, URL Inspection, sitemaps, derived analyses)", epilog="SITE: URL-prefix property (https://example.com/) or domain property (sc-domain:example.com)")
  subparsers = parser.add_subparsers(dest="command", required=True)
  subparsers.add_parser("sites", parents=[common], help="List properties the service account can access")
  analytics_parser = subparsers.add_parser("analytics", parents=[common], help="Search Analytics query")
  analytics_parser.add_argument("site")
  analytics_parser.add_argument("--start", default="", help="YYYY-MM-DD (default: 28 days ending 3 days ago)")
  analytics_parser.add_argument("--end", default="", help="YYYY-MM-DD")
  analytics_parser.add_argument("--dimensions", default="query", help="Comma list: query, page, country, device, date, searchAppearance")
  analytics_parser.add_argument("--filter", action="append", default=[], help="DIMENSION:OPERATOR:VALUE, repeatable")
  analytics_parser.add_argument("--search-type", default="web", choices=["web", "image", "video", "news", "discover", "googleNews"])
  analytics_parser.add_argument("--rows", type=int, default=1000, help="Max rows (paginates 25,000 per request)")
  inspect_parser = subparsers.add_parser("inspect", parents=[common], help="URL Inspection (2,000 per day per property)")
  inspect_parser.add_argument("site")
  inspect_parser.add_argument("urls", nargs="+")
  sitemaps_parser = subparsers.add_parser("sitemaps", parents=[common], help="List sitemaps, optionally submit one (needs Full permission)")
  sitemaps_parser.add_argument("site")
  sitemaps_parser.add_argument("--submit", default="", help="Sitemap URL to submit")
  quick_parser = subparsers.add_parser("quick-wins", parents=[common], help=f"Queries at position {QUICK_WIN_MIN_POSITION:.0f}-{QUICK_WIN_MAX_POSITION:.0f} sorted by impressions")
  quick_parser.add_argument("site")
  quick_parser.add_argument("--days", type=int, default=28)
  quick_parser.add_argument("--limit", type=int, default=50)
  ctr_parser = subparsers.add_parser("ctr-gap", parents=[common], help="RE-TITLE candidates: CTR below bucket median (90 days)")
  ctr_parser.add_argument("site")
  ctr_parser.add_argument("--min-impressions", type=int, default=CTR_GAP_MIN_IMPRESSIONS)
  ctr_parser.add_argument("--ratio", type=float, default=CTR_GAP_RATIO)
  ctr_parser.add_argument("--limit", type=int, default=50)
  decay_parser = subparsers.add_parser("decay", parents=[common], help="Pages losing clicks: last 3 full months vs same months a year earlier")
  decay_parser.add_argument("site")
  decay_parser.add_argument("--min-loss-percent", type=float, default=DECAY_MIN_LOSS_PERCENT)
  decay_parser.add_argument("--min-lost-clicks", type=int, default=DECAY_MIN_LOST_CLICKS)
  decay_parser.add_argument("--limit", type=int, default=50)
  cannibal_parser = subparsers.add_parser("cannibalization", parents=[common], help="Queries split across 2+ pages")
  cannibal_parser.add_argument("site")
  cannibal_parser.add_argument("--days", type=int, default=28)
  cannibal_parser.add_argument("--min-share", type=float, default=CANNIBALIZATION_MIN_SHARE)
  cannibal_parser.add_argument("--min-query-impressions", type=int, default=CANNIBALIZATION_MIN_QUERY_IMPRESSIONS)
  cannibal_parser.add_argument("--limit", type=int, default=50)
  return parser

def main():
  if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
  if hasattr(sys.stderr, "reconfigure"): sys.stderr.reconfigure(encoding="utf-8")
  args = build_parser().parse_args()
  command_result = COMMANDS[args.command](args)
  params = {}
  for name in ["site", "days", "limit"]:
    if hasattr(args, name): params[name] = getattr(args, name)
  result = {"script": SCRIPT_NAME, "command": args.command, "ok": True, "estimated_cost_usd": 0.0, "actual_cost_usd": 0.0, "params": params, "rows": command_result["rows"], "notes": command_result.get("notes", [])}
  emit(result, args.format, command_result.get("columns") or COLUMNS.get(args.command))
  log("OK.")

if __name__ == "__main__":
  main()

# ----------------------------------------- END: CLI ---------------------------------------------------------------------------
