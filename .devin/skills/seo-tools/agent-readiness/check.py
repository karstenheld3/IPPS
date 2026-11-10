#!/usr/bin/env python3
"""
Agent readiness checker (free, no credentials). HTTP probes of one public site against SEO-AGT rules in SEO_RULES.md.

Site types (checks are cumulative as listed):
  A  Content or marketing website: robots.txt, sitemap, AI bot classes, Content-Signal, indexability, Markdown negotiation
  B  Documentation site: A + {url}/index.md fallback + /llms.txt
  C  Ecommerce storefront: A + Product JSON-LD + WebMCP (manual)
  D  API or SaaS platform: A + B + API catalog, MCP server card, agent skills index, OAuth protected resource metadata

Usage:
  python check.py https://example.com/ --site-type A
  python check.py https://docs.example.com/guide/ --site-type B --format json

Exit code: 0 when no check FAILs, 1 when at least one FAILs, 2 on usage error.
"""

import argparse, json, re, sys
from urllib.parse import urljoin, urlparse

import requests

SCRIPT_NAME = "agent-readiness"
USER_AGENT = "seo-tools-agent-readiness/1.0"
MAX_BODY_BYTES = 2 * 1024 * 1024
TIMEOUT_SECONDS = 20
SEARCH_BOTS = ["Googlebot", "Bingbot", "OAI-SearchBot", "PerplexityBot", "Applebot"]
TRAINING_BOTS = ["GPTBot", "Google-Extended", "ClaudeBot", "Applebot-Extended", "CCBot", "Meta-ExternalAgent"]
USER_TRIGGERED_BOTS = ["ChatGPT-User", "Claude-Web", "Perplexity-User", "Google-NotebookLM"]
SITE_TYPE_GROUPS = {"A": ["A"], "B": ["A", "B"], "C": ["A", "C"], "D": ["A", "B", "D"]}
NOINDEX_PATTERN = re.compile(r"<meta[^>]+name=[\"']robots[\"'][^>]*content=[\"'][^\"']*noindex", re.IGNORECASE)
PRODUCT_JSONLD_PATTERN = re.compile(r"\"@type\"\s*:\s*\[?\s*\"Product\"", re.IGNORECASE)

# ----------------------------------------- START: Output helpers --------------------------------------------------------------

def log(message: str):
  print(message, file=sys.stderr, flush=True)

def plural(count: int, singular_word: str, plural_word: str = "") -> str:
  if count == 1: return f"{count} {singular_word}"
  return f"{count:,} {plural_word or singular_word + 's'}"

def add_check(checks: list, name: str, status: str, rule_id: str, detail: str = ""):
  checks.append({"check": name, "status": status, "rule": rule_id, "detail": detail})

# ----------------------------------------- END: Output helpers ----------------------------------------------------------------


# ----------------------------------------- START: HTTP probe ------------------------------------------------------------------

# GET url; return status, final URL, headers, body text (first 2 MB) or error
def probe(url: str, accept: str = "") -> dict:
  headers = {"User-Agent": USER_AGENT}
  if accept: headers["Accept"] = accept
  retVal = {"url": url, "status": 0, "final_url": url, "content_type": "", "vary": "", "headers": {}, "body": "", "error": ""}
  try:
    with requests.get(url, headers=headers, timeout=TIMEOUT_SECONDS, stream=True, allow_redirects=True) as response:
      body_bytes = b""
      for chunk in response.iter_content(chunk_size=65536):
        body_bytes += chunk
        if len(body_bytes) >= MAX_BODY_BYTES: break
      retVal["status"] = response.status_code
      retVal["final_url"] = response.url
      retVal["content_type"] = response.headers.get("Content-Type", "")
      retVal["vary"] = response.headers.get("Vary", "")
      retVal["headers"] = dict(response.headers)
      retVal["body"] = body_bytes[:MAX_BODY_BYTES].decode(response.encoding or "utf-8", errors="replace")
  except requests.RequestException as error:
    retVal["error"] = type(error).__name__
  return retVal

def describe_failure(result: dict) -> str:
  if result["error"]: return f"request failed ({result['error']})"
  return f"HTTP {result['status']}, Content-Type '{result['content_type']}'"

# ----------------------------------------- END: HTTP probe --------------------------------------------------------------------


# ----------------------------------------- START: robots.txt parsing ----------------------------------------------------------

# Return list of groups: {"agents": [...], "rules": [("allow"|"disallow", path)]}
def parse_robots(text: str) -> list:
  retVal = []
  current = None
  previous_was_agent = False
  for raw_line in text.splitlines():
    line = raw_line.split("#", 1)[0].strip()
    if ":" not in line: continue
    field, value = line.split(":", 1)
    field = field.strip().lower()
    value = value.strip()
    if field == "user-agent":
      if current is None or not previous_was_agent:
        current = {"agents": [], "rules": []}
        retVal.append(current)
      current["agents"].append(value.lower())
      previous_was_agent = True
      continue
    previous_was_agent = False
    if current is not None and field in ["allow", "disallow"]: current["rules"].append((field, value))
  return retVal

def find_group(groups: list, bot_name: str) -> dict:
  for group in groups:
    if bot_name.lower() in group["agents"]: return group
  for group in groups:
    if "*" in group["agents"]: return group
  return None

def mentions_bot(groups: list, bot_name: str) -> bool:
  for group in groups:
    if bot_name.lower() in group["agents"]: return True
  return False

# True when the bot's group disallows "/" and has no "Allow: /"
def is_fully_blocked(groups: list, bot_name: str) -> bool:
  group = find_group(groups, bot_name)
  if group is None: return False
  disallow_root = False
  allow_root = False
  for rule_type, path in group["rules"]:
    if rule_type == "disallow" and path == "/": disallow_root = True
    if rule_type == "allow" and path == "/": allow_root = True
  return disallow_root and not allow_root

# ----------------------------------------- END: robots.txt parsing ------------------------------------------------------------


# ----------------------------------------- START: Checks ----------------------------------------------------------------------

def check_robots(base_url: str, checks: list):
  result = probe(urljoin(base_url, "/robots.txt"))
  if result["status"] != 200 or "html" in result["content_type"].lower():
    add_check(checks, "robots.txt reachable", "FAIL", "SEO-AGT-01", describe_failure(result))
    add_check(checks, "Sitemap line in robots.txt", "FAIL", "SEO-AGT-01", "robots.txt missing")
    add_check(checks, "Search and grounding bots allowed", "WARN", "SEO-AGT-02", "robots.txt missing, crawler defaults apply")
    add_check(checks, "Training bots configured explicitly", "WARN", "SEO-AGT-02", "robots.txt missing")
    check_content_signal("", result["headers"], checks)
    return
  add_check(checks, "robots.txt reachable", "PASS", "SEO-AGT-01", "HTTP 200")
  text = result["body"]
  sitemap_lines = []
  for line in text.splitlines():
    if line.strip().lower().startswith("sitemap:"): sitemap_lines.append(line.strip())
  if sitemap_lines: add_check(checks, "Sitemap line in robots.txt", "PASS", "SEO-AGT-01", plural(len(sitemap_lines), "Sitemap line"))
  else: add_check(checks, "Sitemap line in robots.txt", "FAIL", "SEO-AGT-01", "no 'Sitemap:' line")
  groups = parse_robots(text)
  blocked_search_bots = []
  for bot_name in SEARCH_BOTS:
    if is_fully_blocked(groups, bot_name): blocked_search_bots.append(bot_name)
  if blocked_search_bots: add_check(checks, "Search and grounding bots allowed", "FAIL", "SEO-AGT-02", f"blocked: {', '.join(blocked_search_bots)}")
  else: add_check(checks, "Search and grounding bots allowed", "PASS", "SEO-AGT-02", ", ".join(SEARCH_BOTS))
  configured_training_bots = []
  for bot_name in TRAINING_BOTS:
    if mentions_bot(groups, bot_name): configured_training_bots.append(bot_name)
  if configured_training_bots: add_check(checks, "Training bots configured explicitly", "PASS", "SEO-AGT-02", ", ".join(configured_training_bots))
  else: add_check(checks, "Training bots configured explicitly", "WARN", "SEO-AGT-02", "no training bot group (GPTBot, Google-Extended, ClaudeBot, ...)")
  blocked_user_bots = []
  for bot_name in USER_TRIGGERED_BOTS:
    if is_fully_blocked(groups, bot_name): blocked_user_bots.append(bot_name)
  if blocked_user_bots: add_check(checks, "User-triggered fetchers allowed", "WARN", "SEO-AGT-02", f"blocked: {', '.join(blocked_user_bots)}")
  else: add_check(checks, "User-triggered fetchers allowed", "PASS", "SEO-AGT-02", ", ".join(USER_TRIGGERED_BOTS))
  check_content_signal(text, result["headers"], checks)

def check_content_signal(robots_text: str, headers: dict, checks: list):
  signal_values = []
  for line in robots_text.splitlines():
    if line.strip().lower().startswith("content-signal:"): signal_values.append(line.split(":", 1)[1].strip().lower())
  for header_name in headers:
    if header_name.lower() == "content-signal": signal_values.append(str(headers[header_name]).lower())
  if not signal_values:
    add_check(checks, "Content-Signal declared", "WARN", "SEO-AGT-03", "no Content-Signal in robots.txt")
    return
  for value in signal_values:
    if re.search(r"search\s*=\s*no", value):
      add_check(checks, "Content-Signal declared", "FAIL", "SEO-AGT-03", f"search=no blocks search use: '{value}'")
      return
  add_check(checks, "Content-Signal declared", "PASS", "SEO-AGT-03", signal_values[0])

def check_page_indexable(page_url: str, checks: list) -> dict:
  result = probe(page_url)
  if result["status"] != 200:
    add_check(checks, "Page returns HTTP 200", "FAIL", "SEO-FND-01", describe_failure(result))
    return result
  if result["final_url"].rstrip("/") != page_url.rstrip("/"): add_check(checks, "Page redirect", "INFO", "SEO-FND-01", f"final URL '{result['final_url']}'")
  add_check(checks, "Page returns HTTP 200", "PASS", "SEO-FND-01", "HTTP 200")
  robots_header = ""
  for header_name in result["headers"]:
    if header_name.lower() == "x-robots-tag": robots_header = str(result["headers"][header_name]).lower()
  if "noindex" in robots_header or NOINDEX_PATTERN.search(result["body"]): add_check(checks, "Page indexable (no noindex)", "FAIL", "SEO-FND-01", "noindex in meta robots or X-Robots-Tag")
  else: add_check(checks, "Page indexable (no noindex)", "PASS", "SEO-FND-01", "")
  return result

def check_markdown_negotiation(page_url: str, strict: bool, checks: list):
  result = probe(page_url, accept="text/markdown")
  missing_status = "FAIL" if strict else "WARN"
  if result["status"] == 200 and "text/markdown" in result["content_type"].lower():
    add_check(checks, "Accept: text/markdown returns Markdown", "PASS", "SEO-AGT-04", result["content_type"])
    if "accept" in result["vary"].lower(): add_check(checks, "Vary: Accept on Markdown response", "PASS", "SEO-AGT-04", result["vary"])
    else: add_check(checks, "Vary: Accept on Markdown response", "FAIL", "SEO-AGT-04", f"Vary '{result['vary']}'")
    if result["body"].lstrip().startswith("---"): add_check(checks, "Markdown YAML frontmatter", "PASS", "SEO-AGT-04", "")
    else: add_check(checks, "Markdown YAML frontmatter", "WARN", "SEO-AGT-04", "no frontmatter (title, description, image)")
    return
  add_check(checks, "Accept: text/markdown returns Markdown", missing_status, "SEO-AGT-04", describe_failure(result))

def check_index_md(page_url: str, checks: list):
  index_url = page_url.rstrip("/") + "/index.md"
  result = probe(index_url)
  content_type = result["content_type"].lower()
  if result["status"] == 200 and ("markdown" in content_type or "text/plain" in content_type): add_check(checks, "{url}/index.md fallback", "PASS", "SEO-AGT-05", content_type)
  else: add_check(checks, "{url}/index.md fallback", "FAIL", "SEO-AGT-05", describe_failure(result))

def check_llms_txt(base_url: str, checks: list):
  result = probe(urljoin(base_url, "/llms.txt"))
  content_type = result["content_type"].lower()
  if result["status"] == 200 and ("text/plain" in content_type or "markdown" in content_type): add_check(checks, "/llms.txt", "PASS", "SEO-AGT-06", content_type)
  else: add_check(checks, "/llms.txt", "FAIL", "SEO-AGT-06", describe_failure(result))

def check_product_jsonld(page_result: dict, checks: list):
  if PRODUCT_JSONLD_PATTERN.search(page_result.get("body", "")): add_check(checks, "Product JSON-LD on page", "PASS", "SEO-MTD-04", "")
  else: add_check(checks, "Product JSON-LD on page", "FAIL", "SEO-MTD-04", "no \"@type\": \"Product\" in initial HTML")
  add_check(checks, "WebMCP tools for browser agents", "INFO", "SEO-AGT-10", "manual check (not detectable by HTTP probe)")

def check_well_known(base_url: str, checks: list):
  catalog = probe(urljoin(base_url, "/.well-known/api-catalog"))
  if catalog["status"] == 200 and "linkset+json" in catalog["content_type"].lower(): add_check(checks, "/.well-known/api-catalog", "PASS", "SEO-AGT-07", catalog["content_type"])
  else: add_check(checks, "/.well-known/api-catalog", "FAIL", "SEO-AGT-07", describe_failure(catalog))
  for path, rule_id in [("/.well-known/mcp/server-card.json", "SEO-AGT-08"), ("/.well-known/agent-skills/index.json", "SEO-AGT-08"), ("/.well-known/oauth-protected-resource", "SEO-AGT-09")]:
    result = probe(urljoin(base_url, path))
    is_json = False
    if result["status"] == 200:
      try:
        json.loads(result["body"])
        is_json = True
      except ValueError:
        is_json = False
    if is_json: add_check(checks, path, "PASS", rule_id, "valid JSON")
    else: add_check(checks, path, "WARN", rule_id, describe_failure(result) if result["status"] != 200 else "not valid JSON")

# ----------------------------------------- END: Checks ------------------------------------------------------------------------


# ----------------------------------------- START: CLI -------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
  parser = argparse.ArgumentParser(description="Agent readiness checker (HTTP probes, no credentials)", epilog="Site types: A content site, B documentation (A+B), C ecommerce (A+C), D API platform (A+B+D)")
  parser.add_argument("url", help="Page URL, e.g. https://example.com/")
  parser.add_argument("--site-type", choices=["A", "B", "C", "D"], default="A")
  parser.add_argument("--format", choices=["table", "json"], default="table")
  return parser

def main():
  if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
  if hasattr(sys.stderr, "reconfigure"): sys.stderr.reconfigure(encoding="utf-8")
  args = build_parser().parse_args()
  parsed = urlparse(args.url)
  if parsed.scheme not in ["http", "https"] or not parsed.netloc:
    log("ERROR: URL must be absolute, e.g. https://example.com/")
    sys.exit(2)
  base_url = f"{parsed.scheme}://{parsed.netloc}/"
  groups = SITE_TYPE_GROUPS[args.site_type]
  log(f"Checking '{args.url}' (site type {args.site_type})...")
  checks = []
  check_robots(base_url, checks)
  page_result = check_page_indexable(args.url, checks)
  check_markdown_negotiation(args.url, "B" in groups, checks)
  if "B" in groups:
    check_index_md(args.url, checks)
    check_llms_txt(base_url, checks)
  if "C" in groups: check_product_jsonld(page_result, checks)
  if "D" in groups: check_well_known(base_url, checks)
  counts = {"PASS": 0, "WARN": 0, "FAIL": 0, "INFO": 0}
  for check in checks: counts[check["status"]] += 1
  summary = f"{plural(counts['PASS'], 'check')} passed, {counts['WARN']} warned, {counts['FAIL']} failed, {counts['INFO']} info."
  if args.format == "json":
    print(json.dumps({"script": SCRIPT_NAME, "command": "check", "ok": counts["FAIL"] == 0, "estimated_cost_usd": 0.0, "actual_cost_usd": 0.0, "params": {"url": args.url, "site_type": args.site_type}, "rows": checks, "notes": [summary]}, ensure_ascii=False, indent=2))
  else:
    for index in range(len(checks)):
      check = checks[index]
      print(f"  [ {index + 1:>2} / {len(checks)} ] {check['check']:<40} {check['status']:<5} {check['rule']:<11} {check['detail']}")
  log(("FAIL: " if counts["FAIL"] else "OK: ") + summary)
  sys.exit(1 if counts["FAIL"] else 0)

if __name__ == "__main__":
  main()

# ----------------------------------------- END: CLI ---------------------------------------------------------------------------
