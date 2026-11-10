#!/usr/bin/env python3
"""
IndexNow URL submission (free). One submission reaches Bing, Yandex, Naver, Seznam, and Yep. Google does not take part.

Usage:
  python submit.py submit https://example.com/new-page --host example.com
  python submit.py submit --file urls.txt --host example.com --dry-run
  python submit.py verify-key --host example.com

Credentials: INDEXNOW_API_KEY in [API_KEYS_FILE] (optional, --key overrides; see SKILL.md section "Credential Keys").
"""

import argparse, json, re, sys, time
from pathlib import Path
from urllib.parse import urlparse

import requests

SCRIPT_NAME = "indexnow"
SETUP_HINT = "indexnow/SETUP.md"
DEFAULT_KEYS_FILE = Path(__file__).resolve().parents[5] / ".tools" / ".api-keys.txt"
ENDPOINT = "https://api.indexnow.org/indexnow"
ENGINES = ["Bing", "Yandex", "Naver", "Seznam", "Yep"]
MAX_URLS_PER_POST = 10000
KEY_PATTERN = re.compile(r"^[a-zA-Z0-9-]{8,128}$")
STATUS_MEANINGS = {200: "OK, URLs submitted", 202: "Accepted, key pending verification", 400: "Bad request, invalid format", 403: "Key not valid or key file not found", 422: "URLs do not belong to host or key does not match", 429: "Too many requests"}

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

def emit(result: dict, output_format: str):
  if output_format == "json":
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return
  for row in result.get("rows", []):
    parts = []
    for key in row: parts.append(f"{key}={row[key]}")
    print("  ".join(parts))
  for note in result.get("notes", []): print(note)

def create_common_parser() -> argparse.ArgumentParser:
  common = argparse.ArgumentParser(add_help=False)
  common.add_argument("--keys-file", type=Path, default=DEFAULT_KEYS_FILE, help="Credentials file (default: [WORKSPACE_FOLDER]/../.tools/.api-keys.txt)")
  common.add_argument("--format", choices=["table", "json"], default="table", help="Output format (default: table)")
  return common

# ----------------------------------------- END: Common script contract --------------------------------------------------------


# ----------------------------------------- START: IndexNow --------------------------------------------------------------------

# Key from --key, else INDEXNOW_API_KEY from keys file
def resolve_key(args) -> str:
  retVal = args.key
  if not retVal:
    keys = load_api_keys(args.keys_file)
    retVal = require_key(keys, "INDEXNOW_API_KEY", args.keys_file)
  if not KEY_PATTERN.match(retVal): fail("Invalid key -> 8-128 characters, only a-z, A-Z, 0-9, '-' allowed.", 2)
  return retVal

def collect_urls(args) -> list:
  retVal = []
  for url in args.urls: retVal.append(url.strip())
  if args.file:
    if not args.file.is_file(): fail(f"URL file not found -> '{args.file}'", 2)
    for line in args.file.read_text(encoding="utf-8-sig").splitlines():
      if line.strip(): retVal.append(line.strip())
  if not retVal: fail("No URLs given -> pass URLs or --file.", 2)
  return retVal

def validate_hosts(urls: list, host: str):
  mismatched = []
  for url in urls:
    if (urlparse(url).hostname or "").lower() != host.lower(): mismatched.append(url)
  if mismatched:
    for url in mismatched[:10]: log(f"  Host mismatch: '{url}'")
    fail(f"{plural(len(mismatched), 'URL')} not on host '{host}'.", 2)

def describe_status(status_code: int) -> str:
  return STATUS_MEANINGS.get(status_code, "Unexpected status")

def cmd_submit(args) -> dict:
  urls = collect_urls(args)
  validate_hosts(urls, args.host)
  key = resolve_key(args)
  key_location = args.key_location or f"https://{args.host}/{key}.txt"
  rows = []
  exit_code = 0
  if len(urls) == 1:
    log(f"Submitting 1 URL to IndexNow (GET)...")
    if args.dry_run:
      print(f"DRY RUN: GET {ENDPOINT}?url={urls[0]}&key=<key>")
      return {"rows": [{"chunk": 1, "urls": 1, "status": "dry-run"}], "exit_code": 0}
    response = http_request("GET", ENDPOINT, params={"url": urls[0], "key": key, "keyLocation": key_location})
    rows.append({"chunk": 1, "urls": 1, "status": response.status_code, "meaning": describe_status(response.status_code)})
    if response.status_code not in [200, 202]: exit_code = 1
    return {"rows": rows, "exit_code": exit_code}
  chunk_count = (len(urls) + MAX_URLS_PER_POST - 1) // MAX_URLS_PER_POST
  log(f"Submitting {plural(len(urls), 'URL')} to IndexNow in {plural(chunk_count, 'POST request')}...")
  for chunk_index in range(chunk_count):
    chunk = urls[chunk_index * MAX_URLS_PER_POST:(chunk_index + 1) * MAX_URLS_PER_POST]
    body = {"host": args.host, "key": key, "keyLocation": key_location, "urlList": chunk}
    if args.dry_run:
      print(f"DRY RUN: [ {chunk_index + 1} / {chunk_count} ] POST {ENDPOINT} host='{args.host}' keyLocation='{key_location}' urlList={plural(len(chunk), 'URL')}")
      rows.append({"chunk": chunk_index + 1, "urls": len(chunk), "status": "dry-run"})
      continue
    response = http_request("POST", ENDPOINT, headers={"Content-Type": "application/json; charset=utf-8"}, json_body=body)
    log(f"  [ {chunk_index + 1} / {chunk_count} ] HTTP {response.status_code} - {describe_status(response.status_code)}")
    rows.append({"chunk": chunk_index + 1, "urls": len(chunk), "status": response.status_code, "meaning": describe_status(response.status_code)})
    if response.status_code not in [200, 202]: exit_code = 1
  return {"rows": rows, "exit_code": exit_code}

def cmd_verify_key(args) -> dict:
  key = resolve_key(args)
  key_location = args.key_location or f"https://{args.host}/{key}.txt"
  log(f"Fetching key file '{key_location}'...")
  try:
    response = requests.get(key_location, timeout=30)
  except requests.RequestException as error:
    fail(f"Key file not reachable -> '{key_location}' -> {type(error).__name__}", 1)
  if response.status_code != 200:
    log(f"  FAIL: HTTP {response.status_code} -> key file not found.")
    return {"rows": [{"key_location": key_location, "result": "FAIL", "reason": f"HTTP {response.status_code}"}], "exit_code": 1}
  if response.text.strip() != key:
    log("  FAIL: Key file content does not match the key.")
    return {"rows": [{"key_location": key_location, "result": "FAIL", "reason": "content mismatch"}], "exit_code": 1}
  log("  PASS: Key file matches.")
  return {"rows": [{"key_location": key_location, "result": "PASS"}], "exit_code": 0}

# ----------------------------------------- END: IndexNow ----------------------------------------------------------------------


# ----------------------------------------- START: CLI -------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
  common = create_common_parser()
  parser = argparse.ArgumentParser(description="IndexNow submission (Bing, Yandex, Naver, Seznam, Yep; not Google)")
  subparsers = parser.add_subparsers(dest="command", required=True)
  submit_parser = subparsers.add_parser("submit", parents=[common], help="Submit URLs (1 URL = GET, 2+ URLs = POST, max 10,000 per POST)")
  submit_parser.add_argument("urls", nargs="*", help="Absolute URLs on --host")
  submit_parser.add_argument("--file", type=Path, help="UTF-8 text file with one URL per line")
  submit_parser.add_argument("--host", required=True, help="Host name, e.g. example.com")
  submit_parser.add_argument("--key", default="", help="IndexNow key (default: INDEXNOW_API_KEY from keys file)")
  submit_parser.add_argument("--key-location", default="", help="Key file URL (default: https://{host}/{key}.txt)")
  submit_parser.add_argument("--dry-run", action="store_true", help="Print requests without sending")
  verify_parser = subparsers.add_parser("verify-key", parents=[common], help="Check that the key file is reachable and matches")
  verify_parser.add_argument("--host", required=True, help="Host name, e.g. example.com")
  verify_parser.add_argument("--key", default="", help="IndexNow key (default: INDEXNOW_API_KEY from keys file)")
  verify_parser.add_argument("--key-location", default="", help="Key file URL (default: https://{host}/{key}.txt)")
  return parser

def main():
  if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
  if hasattr(sys.stderr, "reconfigure"): sys.stderr.reconfigure(encoding="utf-8")
  args = build_parser().parse_args()
  command_result = cmd_submit(args) if args.command == "submit" else cmd_verify_key(args)
  notes = []
  if args.command == "submit": notes.append(f"Receiving engines: {', '.join(ENGINES)}. Google is not covered (use sitemap <lastmod>).")
  result = {"script": SCRIPT_NAME, "command": args.command, "ok": command_result["exit_code"] == 0, "estimated_cost_usd": 0.0, "actual_cost_usd": 0.0, "params": {"host": args.host}, "rows": command_result["rows"], "notes": notes}
  emit(result, args.format)
  if command_result["exit_code"] == 0: log("OK.")
  else: log("FAIL.")
  sys.exit(command_result["exit_code"])

if __name__ == "__main__":
  main()

# ----------------------------------------- END: CLI ---------------------------------------------------------------------------
