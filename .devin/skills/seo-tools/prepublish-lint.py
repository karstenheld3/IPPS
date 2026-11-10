#!/usr/bin/env python3
"""
Offline pre-publish metadata linter. Checks platform length limits, prohibited tokens, and keyword set difference
against SEO_RULES.md (limits [LITERAL: 2026-11-03]) and the gate in SEO_CHECKS.md section 2.

Usage:
  python prepublish-lint.py payload.json
  python prepublish-lint.py payload.json --format json

Payload (UTF-8 JSON):
  {"platform": "apple-app-store",
   "fields": {"name": "...", "subtitle": "...", "keywords": "a,b,c", "promotional_text": "..."},
   "context": {"categories": ["Productivity"], "developer": "Example Studio"}}

Platforms and fields:
  web                title, description, jsonld
  kdp                title, subtitle, description, keywords (list of up to 7), series_number   context: author, categories
  apple-books        title, subtitle, description, series_number
  google-play-books  title, subtitle, description, series_number
  kobo               title, subtitle, description, series_number
  apple-app-store    name, subtitle, promotional_text, keywords, iap_name, iap_description  context: categories, developer
  google-play        title, short_description, full_description, developer_name
  podcast            title, description
  gbp                name, description
  linkedin           seo_title, seo_description
  youtube            title, description

Exit code: 0 no FAIL, 1 at least one FAIL, 2 usage error (unknown platform, invalid JSON, missing file).
"""

import argparse, json, re, sys
from pathlib import Path

SCRIPT_NAME = "prepublish-lint"

# (platform, field) -> (max, unit, gate, rule, severity); unit "chars" counts Unicode code points, "bytes" counts UTF-8 bytes
# Values must equal SEO_RULES.md section "Platform Metadata Field Specifications" [LITERAL: 2026-11-03]
LIMITS = {
  ("web", "title"): (60, "chars", "GATE-WEB-03", "SEO-MTD-01", "WARN"),
  ("web", "description"): (160, "chars", "GATE-WEB-03", "SEO-MTD-02", "WARN"),
  ("kdp", "title"): (60, "chars", "GATE-BOOK-01", "SEO-MTX-09", "WARN"),
  ("apple-app-store", "name"): (30, "chars", "GATE-APP-01", "SEO-MAV-06", "FAIL"),
  ("apple-app-store", "subtitle"): (30, "chars", "GATE-APP-01", "SEO-MAV-06", "FAIL"),
  ("apple-app-store", "promotional_text"): (170, "chars", "GATE-APP-01", "SEO-MAV-06", "FAIL"),
  ("apple-app-store", "keywords"): (100, "chars", "GATE-APP-01", "SEO-MAV-06", "FAIL"),
  ("apple-app-store", "iap_name"): (35, "chars", "GATE-APP-01", "SEO-MAV-06", "FAIL"),
  ("apple-app-store", "iap_description"): (55, "chars", "GATE-APP-01", "SEO-MAV-06", "FAIL"),
  ("google-play", "title"): (30, "chars", "GATE-APP-02", "SEO-MAV-07", "FAIL"),
  ("google-play", "short_description"): (80, "chars", "GATE-APP-02", "SEO-MAV-07", "FAIL"),
  ("google-play", "full_description"): (4000, "chars", "GATE-APP-02", "SEO-MAV-07", "FAIL"),
  ("podcast", "title"): (255, "chars", "GATE-POD-01", "SEO-MAV-03", "FAIL"),
  ("podcast", "description"): (4000, "bytes", "GATE-POD-01", "SEO-MAV-03", "FAIL"),
  ("gbp", "description"): (750, "chars", "GATE-GBP-01", "SEO-MTD-11", "FAIL"),
  ("linkedin", "seo_title"): (60, "chars", "GATE-SOC-01", "SEO-MAV-05", "FAIL"),
  ("linkedin", "seo_description"): (160, "chars", "GATE-SOC-01", "SEO-MAV-05", "FAIL"),
  ("youtube", "title"): (100, "chars", "GATE-VID-01", "SEO-MAV-01", "FAIL"),
  ("youtube", "description"): (5000, "chars", "GATE-VID-01", "SEO-MAV-01", "FAIL"),
}

MIN_LIMITS = {
  ("apple-books", "description"): (50, "chars", "GATE-BOOK-03", "SEO-MTX-11", "FAIL"),
  ("linkedin", "seo_description"): (140, "chars", "GATE-SOC-01", "SEO-MAV-05", "WARN"),
}

KDP_TITLE_SUBTITLE_MAX = 199
KDP_KEYWORD_SLOTS = 7
KDP_KEYWORD_SLOT_MAX = 50
KDP_BANNED_TERMS = ["free", "bestselling", "bestseller", "best seller", "kindle", "kdp select", "new", "on sale", "available now", "book", "ebook"]
APPLE_BANNED_KEYWORD_TERMS = ["app", "game"]

# The 5 regexes from SEO_CHECKS.md section 3 (verbatim)
REGEX_LINKS_CONTACT = re.compile(r"https?://|www\.|@\w+|\b\d{3}[-.]?\d{3}[-.]?\d{4}\b")
REGEX_HTML_TAGS = re.compile(r"<[a-zA-Z/][^>]*>")
REGEX_PLAY_PROMO = re.compile(r"#1|best of play|\bfree\b|no ads|% off", re.IGNORECASE)
REGEX_COMMA_SPACES = re.compile(r",\s+|\s+,")
REGEX_RETIRED_SCHEMA = re.compile(r"\"@type\"\s*:\s*\"(FAQPage|HowTo|PracticeProblem|SpecialAnnouncement)\"")

REGEX_SERIES_IN_TITLE = re.compile(r"\b(book|vol\.?|volume|band|tome)\s*\d+\b|\bseries\s+\d+\b", re.IGNORECASE)
REGEX_PRICE_PROMO = re.compile(r"\d+\s*%|[$€£]\s?\d|\d\s?[$€£]|\bsale\b|\bdiscount\b", re.IGNORECASE)
REGEX_EMOJI = re.compile("[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F000-\U0001F2FF]")
REGEX_TIMESTAMP_LINE = re.compile(r"^\s*((\d{1,2}):)?(\d{1,2}):(\d{2})\b")
REGEX_WORD = re.compile(r"\w+", re.UNICODE)

PLATFORM_FIELDS = {
  "web": ["title", "description", "jsonld"],
  "kdp": ["title", "subtitle", "description", "keywords", "series_number"],
  "apple-books": ["title", "subtitle", "description", "series_number"],
  "google-play-books": ["title", "subtitle", "description", "series_number"],
  "kobo": ["title", "subtitle", "description", "series_number"],
  "apple-app-store": ["name", "subtitle", "promotional_text", "keywords", "iap_name", "iap_description"],
  "google-play": ["title", "short_description", "full_description", "developer_name"],
  "podcast": ["title", "description"],
  "gbp": ["name", "description"],
  "linkedin": ["seo_title", "seo_description"],
  "youtube": ["title", "description"],
}

# ----------------------------------------- START: Helpers ---------------------------------------------------------------------

def log(message: str):
  print(message, file=sys.stderr, flush=True)

def fail_usage(message: str):
  log(f"ERROR: {message}")
  sys.exit(2)

def plural(count: int, singular_word: str, plural_word: str = "") -> str:
  if count == 1: return f"{count} {singular_word}"
  return f"{count:,} {plural_word or singular_word + 's'}"

def add_result(results: list, gate: str, check: str, status: str, detail: str, rule: str):
  results.append({"gate": gate, "check": check, "status": status, "detail": detail, "rule": rule})

def measure(value: str, unit: str) -> int:
  if unit == "bytes": return len(value.encode("utf-8"))
  return len(value)

def tokenize(text: str) -> list:
  retVal = []
  for match in REGEX_WORD.finditer(text.lower()): retVal.append(match.group(0))
  return retVal

def singular(token: str) -> str:
  if len(token) > 3 and token.endswith("s") and not token.endswith("ss"): return token[:-1]
  return token

def field_text(fields: dict, name: str) -> str:
  value = fields.get(name)
  if value is None: return None
  if isinstance(value, list):
    parts = []
    for item in value: parts.append(str(item))
    return "\n".join(parts)
  if isinstance(value, (dict, list)): return json.dumps(value, ensure_ascii=False)
  return str(value)

# ----------------------------------------- END: Helpers -----------------------------------------------------------------------


# ----------------------------------------- START: Checks ----------------------------------------------------------------------

def check_lengths(platform: str, fields: dict, results: list):
  for field_name in PLATFORM_FIELDS[platform]:
    text = field_text(fields, field_name)
    if (platform, field_name) in LIMITS:
      limit, unit, gate, rule, severity = LIMITS[(platform, field_name)]
      if text is None: add_result(results, gate, f"{field_name} length", "SKIP", "field absent", rule)
      else:
        size = measure(text, unit)
        add_result(results, gate, f"{field_name} length", "PASS" if size <= limit else severity, f"{size:,} / {limit:,} {unit}", rule)
    if (platform, field_name) in MIN_LIMITS and text is not None:
      minimum, unit, gate, rule, severity = MIN_LIMITS[(platform, field_name)]
      size = measure(text, unit)
      add_result(results, gate, f"{field_name} minimum", "PASS" if size >= minimum else severity, f"{size:,} / min {minimum:,} {unit}", rule)

def check_regex(results: list, gate: str, check_name: str, text: str, pattern: re.Pattern, rule: str):
  if text is None:
    add_result(results, gate, check_name, "SKIP", "field absent", rule)
    return
  match = pattern.search(text)
  if match: add_result(results, gate, check_name, "FAIL", f"found '{match.group(0)}'", rule)
  else: add_result(results, gate, check_name, "PASS", "", rule)

def check_books(platform: str, fields: dict, context: dict, results: list):
  title = field_text(fields, "title") or ""
  subtitle = field_text(fields, "subtitle") or ""
  description = field_text(fields, "description")
  if platform == "kdp" and (title or subtitle):
    combined = len(title) + len(subtitle)
    add_result(results, "GATE-BOOK-01", "title + subtitle length", "PASS" if combined <= KDP_TITLE_SUBTITLE_MAX else "FAIL", f"{combined:,} / < 200 chars", "SEO-MTX-09")
  if title or subtitle:
    check_regex(results, "GATE-BOOK-01", "no series or volume in title/subtitle", f"{title}\n{subtitle}", REGEX_SERIES_IN_TITLE, "SEO-MTX-13")
  series_number = field_text(fields, "series_number")
  if series_number is not None:
    is_digits = series_number.isdigit() and int(series_number) > 0
    add_result(results, "GATE-BOOK-01", "series number digits only", "PASS" if is_digits else "FAIL", f"'{series_number}'", "SEO-MTX-12")
  if platform in ["kdp", "kobo", "google-play-books"]: check_regex(results, "GATE-BOOK-03", "description links and contact data (regex 1)", description, REGEX_LINKS_CONTACT, "SEO-MTD-08")
  if platform == "apple-books": check_regex(results, "GATE-BOOK-03", "description HTML tags (regex 2)", description, REGEX_HTML_TAGS, "SEO-MTX-11")
  if platform == "kdp": check_kdp_keywords(fields, context, title, subtitle, results)

def check_kdp_keywords(fields: dict, context: dict, title: str, subtitle: str, results: list):
  keywords = fields.get("keywords")
  if keywords is None:
    add_result(results, "GATE-BOOK-04", "keyword slots", "SKIP", "field absent", "SEO-MTX-10")
    return
  if isinstance(keywords, str): keywords = [keywords]
  add_result(results, "GATE-BOOK-04", "keyword slot count", "PASS" if len(keywords) <= KDP_KEYWORD_SLOTS else "FAIL", f"{len(keywords)} / {KDP_KEYWORD_SLOTS} slots", "SEO-MTX-10")
  used_text = f"{title} {subtitle} {context.get('author', '')} {' '.join(context.get('categories', []))}"
  used_tokens = set(tokenize(used_text))
  for index in range(len(keywords)):
    slot = str(keywords[index])
    slot_label = f"keyword slot {index + 1}"
    add_result(results, "GATE-BOOK-04", f"{slot_label} length", "PASS" if len(slot) <= KDP_KEYWORD_SLOT_MAX else "FAIL", f"{len(slot)} / {KDP_KEYWORD_SLOT_MAX} chars", "SEO-MTX-10")
    if '"' in slot or "\u201c" in slot or "\u201d" in slot: add_result(results, "GATE-BOOK-04", f"{slot_label} quotes", "FAIL", "quotation marks", "SEO-MTX-10")
    repeated = []
    for token in tokenize(slot):
      if token in used_tokens and token not in repeated: repeated.append(token)
    if repeated: add_result(results, "GATE-BOOK-04", f"{slot_label} set-diff", "FAIL", f"repeated tokens: {', '.join(repeated)}", "SEO-MTD-09")
    banned_found = []
    lowered = " " + " ".join(tokenize(slot)) + " "
    for term in KDP_BANNED_TERMS:
      if f" {term} " in lowered: banned_found.append(term)
    if banned_found: add_result(results, "GATE-BOOK-04", f"{slot_label} banned terms", "FAIL", ", ".join(banned_found), "SEO-MTX-10")

def check_apple_app_store(fields: dict, context: dict, results: list):
  keywords = field_text(fields, "keywords")
  check_regex(results, "GATE-APP-01", "keywords comma spaces (regex 4)", keywords, REGEX_COMMA_SPACES, "SEO-MAV-06")
  if keywords is None: return
  name_subtitle = f"{field_text(fields, 'name') or ''} {field_text(fields, 'subtitle') or ''} {context.get('developer', '')} {' '.join(context.get('categories', []))}"
  used_tokens = set()
  for token in tokenize(name_subtitle): used_tokens.add(singular(token))
  keyword_tokens = tokenize(keywords)
  repeated = []
  for token in keyword_tokens:
    if singular(token) in used_tokens and token not in repeated: repeated.append(token)
  add_result(results, "GATE-APP-01", "keywords set-diff", "FAIL" if repeated else "PASS", f"repeated tokens: {', '.join(repeated)}" if repeated else "", "SEO-MTD-09")
  singular_counts = {}
  for token in keyword_tokens: singular_counts.setdefault(singular(token), set()).add(token)
  plural_duplicates = []
  for root in singular_counts:
    if len(singular_counts[root]) > 1: plural_duplicates.append("/".join(sorted(singular_counts[root])))
  add_result(results, "GATE-APP-01", "keywords plural duplicates", "FAIL" if plural_duplicates else "PASS", ", ".join(plural_duplicates), "SEO-MAV-06")
  banned_found = []
  for token in keyword_tokens:
    if token in APPLE_BANNED_KEYWORD_TERMS and token not in banned_found: banned_found.append(token)
  if "#" in keywords or "@" in keywords: banned_found.append("#/@")
  add_result(results, "GATE-APP-01", "keywords banned terms", "FAIL" if banned_found else "PASS", ", ".join(banned_found), "SEO-MAV-06")

def check_google_play(fields: dict, results: list):
  for field_name in ["title", "short_description", "full_description"]:
    check_regex(results, "GATE-APP-02", f"{field_name} promotional claims (regex 3)", field_text(fields, field_name), REGEX_PLAY_PROMO, "SEO-MAV-07")
  for field_name in ["title", "developer_name"]:
    text = field_text(fields, field_name)
    if text is not None: check_regex(results, "GATE-APP-02", f"{field_name} emoji", text, REGEX_EMOJI, "SEO-MAV-07")
  short_description = (field_text(fields, "short_description") or "").strip().lower()
  full_description = (field_text(fields, "full_description") or "").lower()
  if short_description and full_description:
    repeated = short_description in full_description
    add_result(results, "GATE-APP-02", "short description not in full description", "FAIL" if repeated else "PASS", "", "SEO-MAV-07")

def check_podcast(fields: dict, results: list):
  title = field_text(fields, "title")
  if title is not None: check_regex(results, "GATE-POD-01", "title emoji", title, REGEX_EMOJI, "SEO-MAV-03")
  if title is not None:
    tokens = tokenize(title)
    counts = {}
    for token in tokens: counts[token] = counts.get(token, 0) + 1
    stuffed = []
    for token in counts:
      if counts[token] >= 3 and len(token) > 3: stuffed.append(token)
    add_result(results, "GATE-POD-01", "title keyword repetition", "FAIL" if stuffed else "PASS", f"repeated 3+ times: {', '.join(stuffed)}" if stuffed else "", "SEO-MAV-03")

def check_gbp(fields: dict, results: list):
  description = field_text(fields, "description")
  check_regex(results, "GATE-GBP-01", "description links and contact data (regex 1)", description, REGEX_LINKS_CONTACT, "SEO-MAV-09")
  check_regex(results, "GATE-GBP-01", "description price or promotion", description, REGEX_PRICE_PROMO, "SEO-MAV-09")
  name = field_text(fields, "name")
  if name is not None: check_regex(results, "GATE-GBP-01", "name links and contact data (regex 1)", name, REGEX_LINKS_CONTACT, "SEO-MAV-08")

def check_youtube(fields: dict, results: list):
  description = field_text(fields, "description")
  if description is None: return
  timestamps = []
  for line in description.splitlines():
    match = REGEX_TIMESTAMP_LINE.match(line)
    if match: timestamps.append(int(match.group(2) or 0) * 3600 + int(match.group(3)) * 60 + int(match.group(4)))
  if not timestamps:
    add_result(results, "GATE-VID-01", "chapters", "WARN", "no chapter timestamps", "SEO-MTD-06")
    return
  problems = []
  if timestamps[0] != 0: problems.append("first timestamp is not 00:00")
  if len(timestamps) < 3: problems.append(f"{plural(len(timestamps), 'timestamp')} (< 3)")
  for index in range(1, len(timestamps)):
    if timestamps[index] - timestamps[index - 1] < 10: problems.append(f"segment {index} shorter than 10 s or not ascending")
  add_result(results, "GATE-VID-01", "chapters", "FAIL" if problems else "PASS", "; ".join(problems) if problems else plural(len(timestamps), "chapter"), "SEO-MTD-06")

def lint(payload: dict) -> list:
  retVal = []
  platform = payload.get("platform", "")
  if platform not in PLATFORM_FIELDS: fail_usage(f"Unknown platform '{platform}' -> valid: {', '.join(PLATFORM_FIELDS)}")
  fields = payload.get("fields") or {}
  context = payload.get("context") or {}
  check_lengths(platform, fields, retVal)
  if platform == "web": check_regex(retVal, "GATE-WEB-06", "jsonld retired types (regex 5)", field_text(fields, "jsonld"), REGEX_RETIRED_SCHEMA, "SEO-MTD-04")
  if platform in ["kdp", "apple-books", "google-play-books", "kobo"]: check_books(platform, fields, context, retVal)
  if platform == "apple-app-store": check_apple_app_store(fields, context, retVal)
  if platform == "google-play": check_google_play(fields, retVal)
  if platform == "podcast": check_podcast(fields, retVal)
  if platform == "gbp": check_gbp(fields, retVal)
  if platform == "youtube": check_youtube(fields, retVal)
  return retVal

# ----------------------------------------- END: Checks ------------------------------------------------------------------------


# ----------------------------------------- START: CLI -------------------------------------------------------------------------

def load_payload(path: Path) -> dict:
  if not path.is_file(): fail_usage(f"Payload file not found -> '{path}'")
  try:
    retVal = json.loads(path.read_text(encoding="utf-8-sig"))
  except json.JSONDecodeError as error:
    fail_usage(f"Invalid JSON in '{path}' -> line {error.lineno}, column {error.colno}: {error.msg}")
  if not isinstance(retVal, dict): fail_usage(f"Payload must be a JSON object -> '{path}'")
  return retVal

def main():
  if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
  if hasattr(sys.stderr, "reconfigure"): sys.stderr.reconfigure(encoding="utf-8")
  parser = argparse.ArgumentParser(description="Offline pre-publish metadata linter (SEO_CHECKS.md section 2)", epilog="Platforms: " + ", ".join(PLATFORM_FIELDS), formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument("payload", type=Path, help="UTF-8 JSON payload file")
  parser.add_argument("--format", choices=["table", "json"], default="table")
  args = parser.parse_args()
  payload = load_payload(args.payload)
  log(f"Linting '{args.payload.name}' (platform '{payload.get('platform', '')}')...")
  results = lint(payload)
  counts = {"PASS": 0, "FAIL": 0, "WARN": 0, "SKIP": 0}
  for result in results: counts[result["status"]] += 1
  summary = f"{plural(counts['PASS'], 'check')} passed, {counts['FAIL']} failed, {counts['WARN']} warned, {counts['SKIP']} skipped."
  if args.format == "json":
    print(json.dumps({"script": SCRIPT_NAME, "command": "lint", "ok": counts["FAIL"] == 0, "estimated_cost_usd": 0.0, "actual_cost_usd": 0.0, "params": {"platform": payload.get("platform")}, "rows": results, "notes": [summary]}, ensure_ascii=False, indent=2))
  else:
    for result in results: print(f"  {result['gate']:<13} {result['check']:<46} {result['status']:<5} {result['detail']}")
  log(("FAIL: " if counts["FAIL"] else "OK: ") + summary)
  sys.exit(1 if counts["FAIL"] else 0)

if __name__ == "__main__":
  main()

# ----------------------------------------- END: CLI ---------------------------------------------------------------------------
