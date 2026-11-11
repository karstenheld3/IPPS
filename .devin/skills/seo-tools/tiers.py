#!/usr/bin/env python3
"""
Source tiers for the seo-tools skill. `probe` reports which data tiers are usable right now; `run` executes the Tier 1 and Tier 2 sequence of matrix rows 2, 3, 4.

Tiers:
  1 FREE          $0 marginal cost: first-party APIs, free quotas, offline checks, manual UI sources
  2 PREPAID       prepaid balance or credits, spent through a cost gate
  3 SUBSCRIPTION  flat-fee tools (Ahrefs, Semrush); no script, probe only

Usage:
  python tiers.py probe
  python tiers.py probe --balances --format json
  python tiers.py run keywords "ergonomic office chair"
  python tiers.py run serp "mortgage payoff calculator" --format json
  python tiers.py run competitors example.com --brand Example --ads 2 --max-usd 0.15

`run` executes the Tier 1 and Tier 2 sequence of one matrix row, checks every result before the next step uses it, filters generic domains,
stops paid steps at --max-usd, and prints a step ledger plus one agreement label per claim (CONFIRMED, CONFLICT, SINGLE-SOURCE).

The probe only checks which keys exist in the keys file and never prints values. `--balances` additionally calls the two $0 balance commands
(`scrapecreators/query.py credit-balance`, `dataforseo/query.py balance`) when their keys exist.
Credentials: names in SKILL.md section "Credential Keys"; Tier 3 keys: AHREFS_API_KEY, SEMRUSH_API_KEY.
"""

import argparse, json, subprocess, sys
from pathlib import Path
from urllib.parse import urlparse

SKILL_FOLDER = Path(__file__).resolve().parent
DEFAULT_KEYS_FILE = Path(__file__).resolve().parents[4] / ".tools" / ".api-keys.txt"

TIER_NAMES = {1: "FREE", 2: "PREPAID", 3: "SUBSCRIPTION"}

# Price assumptions for the run budget [LITERAL: 2026-11-10]: ScrapeCreators $1.88 per 1,000 credits; DataForSEO Live prices as in dataforseo/query.py
# SERP estimate uses the highest observed live cost ($0.004 on 2026-11-11, list price $0.002)
SCRAPECREATORS_CREDIT_USD = 0.00188
COMPETITOR_LIMIT = 40
DATAFORSEO_ESTIMATE_USD = {"search-volume": 0.09, "serp": 0.004, "competitors": 0.012 + COMPETITOR_LIMIT * 0.00012}
DEFAULT_MAX_USD = 0.15
MIN_SUGGESTION_ROWS = 5
USEFUL_VOLUME = 100
MIN_BRAND_LETTERS = 4

# Registrable domains that rank for almost everything; never product competitors
GENERIC_DOMAINS = ["youtube.com", "linkedin.com", "reddit.com", "indeed.com", "facebook.com", "medium.com", "quora.com", "wikipedia.org", "pinterest.com", "instagram.com",
  "tiktok.com", "twitter.com", "x.com", "scribd.com", "forbes.com", "nytimes.com", "bbc.com", "newyorker.com", "goodreads.com", "merriam-webster.com", "ted.com", "study.com",
  "coursera.org", "geeksforgeeks.org", "investopedia.com", "researchgate.net", "sciencedirect.com", "chron.com", "amazon.com", "apple.com", "google.com", "microsoft.com",
  "github.com", "adobe.com", "canva.com", "g2.com", "capterra.com", "trustpilot.com", "yelp.com", "irs.gov", "ftc.gov"]

# Words that mark a suggestion as written for another region than the US run
OTHER_REGION_MARKERS = ["uk", "australia", "canada", "india", "ireland", "nz", "£", "€"]

MANUAL_SOURCES = {"keywords": ["Google autocomplete UI", "Google Trends UI"], "serp": ["browser check of the top 10"], "competitors": ["Bing AI Performance grounding queries (UI)"]}

# (tier, provider, required keys, any-of keys, script or None, balance command or None, note)
PROVIDERS = [
  (1, "agent-readiness", [], [], "agent-readiness/check.py", None, "no key"),
  (1, "prepublish-lint", [], [], "prepublish-lint.py", None, "no key, offline"),
  (1, "google-search-console", ["GSC_SERVICE_ACCOUNT_FILE"], [], "google-search-console/query.py", None, "owned sites only"),
  (1, "bing-webmaster", ["BING_WEBMASTER_API_KEY"], [], "bing-webmaster/query.py", None, "owned sites only"),
  (1, "youtube", ["YOUTUBE_API_KEY"], [], "youtube/query.py", None, "10,000 units per day"),
  (1, "plausible", ["PLAUSIBLE_API_KEY"], [], "plausible/query.py", None, "owned sites only; Cloud needs Business plan"),
  (1, "indexnow", [], ["INDEXNOW_API_KEY"], "indexnow/submit.py", None, "key can be passed with --key"),
  (1, "manual-sources", [], [], None, None, "Google Trends, Pinterest Trends, autocomplete, browser top-10, GSC and Bing UI reports"),
  (2, "trendsmcp", ["TRENDSMCP_API_KEY"], [], "trendsmcp/query.py", None, "credits, 100 free requests per month; no balance command"),
  (2, "scrapecreators", ["SCRAPECREATORS_API_KEY"], [], "scrapecreators/query.py", ["credit-balance"], "credits, cost gate default 20 credits"),
  (2, "dataforseo", ["DATAFORSEO_LOGIN", "DATAFORSEO_PASSWORD"], [], "dataforseo/query.py", ["balance"], "USD balance, cost gate default $0.10"),
  (3, "ahrefs", ["AHREFS_API_KEY"], [], None, None, "no script; vendor REST API, manual calls after unit estimate"),
  (3, "semrush", ["SEMRUSH_API_KEY"], [], None, None, "no script; vendor REST API, manual calls after unit estimate"),
]

# ----------------------------------------- START: Common script contract ------------------------------------------------------

def log(message: str):
  print(message, file=sys.stderr, flush=True)

def plural(count: int, noun: str) -> str:
  return f"{count} {noun}" if count == 1 else f"{count} {noun}s"

# Parse KEY=VALUE lines; '#' comments, blank lines, BOM, CRLF, and spaces around '=' are tolerated; a missing file gives no keys
def load_api_keys(keys_file: Path) -> dict:
  retVal = {}
  if not keys_file.is_file(): return retVal
  for raw_line in keys_file.read_text(encoding="utf-8-sig").splitlines():
    line = raw_line.strip()
    if not line or line.startswith("#") or "=" not in line: continue
    key, value = line.split("=", 1)
    retVal[key.strip()] = value.strip()
  return retVal

# ----------------------------------------- END: Common script contract --------------------------------------------------------


# ----------------------------------------- START: Probe -----------------------------------------------------------------------

def provider_status(keys: dict, keys_file: Path, required: list, any_of: list, script: str) -> str:
  retVal = "READY"
  for name in required:
    if not keys.get(name): retVal = "MISSING KEY"
  if any_of and not any(keys.get(name) for name in any_of): retVal = "READY (key via --key)"
  if retVal == "READY" and "GSC_SERVICE_ACCOUNT_FILE" in required and not (keys_file.parent / keys["GSC_SERVICE_ACCOUNT_FILE"]).is_file(): retVal = "MISSING FILE"
  if retVal == "READY" and script is None and required: retVal = "KEY PRESENT (manual vendor calls)"
  return retVal

# Balance value from the first 'label: value' note of a free balance command; '[...]' markers on failure
def read_balance(script: str, command: list, keys_file: Path) -> str:
  data = call_provider(script, command, keys_file)
  if not data.get("ok"): return f"[ERROR] {str(data.get('error', ''))[:60]}"
  for note in data.get("notes", []):
    if ":" in str(note): return str(note).split(":", 1)[1].strip()
  return "[UNKNOWN]"

def run_probe(args) -> dict:
  keys = load_api_keys(args.keys_file)
  notes = []
  if not args.keys_file.is_file(): notes.append(f"Keys file not found -> '{args.keys_file}' -> keyed providers are reported as missing.")
  rows = []
  for tier, provider, required, any_of, script, balance_command, note in PROVIDERS:
    status = provider_status(keys, args.keys_file, required, any_of, script)
    balance = ""
    if args.balances and balance_command and status == "READY": balance = read_balance(script, balance_command, args.keys_file)
    rows.append({"tier": tier, "tier_name": TIER_NAMES[tier], "provider": provider, "status": status, "balance": balance, "note": note})
  summary = {}
  for tier in [1, 2, 3]:
    ready = []
    for row in rows:
      if row["tier"] == tier and (row["status"].startswith("READY") or row["status"].startswith("KEY PRESENT")): ready.append(row["provider"])
    summary[str(tier)] = ready
    label = f"Tier {tier} {TIER_NAMES[tier]}"
    if ready: notes.append(f"{label}: AVAILABLE -> {', '.join(ready)}")
    else: notes.append(f"{label}: UNAVAILABLE -> skip this tier, record 'Tier {tier} unavailable' in the source ledger")
  return {"rows": rows, "summary": summary, "notes": notes}

# ----------------------------------------- END: Probe -------------------------------------------------------------------------


# ----------------------------------------- START: Run flows -------------------------------------------------------------------

# One provider call in JSON format; returns the parsed output with 'ok' and 'error'
def call_provider(script: str, arguments: list, keys_file: Path) -> dict:
  command = [sys.executable, str(SKILL_FOLDER / script)] + arguments + ["--keys-file", str(keys_file), "--format", "json"]
  try:
    completed = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", timeout=180)
  except subprocess.TimeoutExpired:
    return {"ok": False, "error": f"timeout after 180 s -> '{script} {arguments[0]}'", "rows": []}
  except UnicodeDecodeError as error:
    return {"ok": False, "error": f"output of '{script} {arguments[0]}' is not valid UTF-8 at byte {error.start}", "rows": []}
  try:
    retVal = json.loads(completed.stdout)
  except ValueError:
    return {"ok": False, "error": f"exit {completed.returncode}: {completed.stderr.strip()[-200:]}", "rows": []}
  retVal["ok"] = completed.returncode == 0
  if not retVal["ok"]: retVal["error"] = f"exit {completed.returncode}: {completed.stderr.strip()[-200:]}"
  return retVal

def cost_of(data: dict) -> float:
  if data.get("script") == "dataforseo": return float(data.get("actual_cost_usd") or data.get("estimated_cost_usd") or 0)
  credits = (data.get("params") or {}).get("credits_charged")
  if isinstance(credits, (int, float)): return credits * SCRAPECREATORS_CREDIT_USD
  return 0.0

# Run one ledger step; paid steps that would exceed the budget are skipped
def step(state: dict, tier: int, provider: str, script: str, arguments: list, estimate_usd: float) -> dict:
  entry = {"tier": tier, "provider": provider, "call": " ".join(arguments)[:120], "rows": 0, "cost_usd": 0.0, "status": "OK", "check": ""}
  state["steps"].append(entry)
  if state["spent_usd"] + estimate_usd > state["max_usd"]:
    entry["status"] = "SKIPPED"
    entry["check"] = f"budget: ${state['spent_usd']:.4f} spent + ${estimate_usd:.4f} estimate > ${state['max_usd']:.2f}"
    log(f"[ {len(state['steps'])} ] {provider} {entry['call'][:70]} -> SKIPPED ({entry['check']})")
    return {"rows": []}
  log(f"[ {len(state['steps'])} ] {provider} {entry['call'][:70]}...")
  data = call_provider(script, arguments, state["keys_file"])
  if not data.get("ok"):
    entry["status"] = "ERROR"
    entry["check"] = str(data.get("error", ""))[:200]
    log(f"  ERROR: {entry['check']}")
    return {"rows": []}
  cost = cost_of(data)
  entry["rows"] = len(data.get("rows") or [])
  entry["cost_usd"] = round(cost, 4)
  state["spent_usd"] += cost
  return data

def warn(state: dict, message: str):
  state["steps"][-1]["status"] = "WARN"
  state["steps"][-1]["check"] = message
  log(f"  WARN: {message}")

def add_manual_sources(state: dict, flow: str):
  for source in MANUAL_SOURCES[flow]: state["steps"].append({"tier": 1, "provider": "manual", "call": source, "rows": 0, "cost_usd": 0.0, "status": "NOT RUN (manual)", "check": ""})

def claim(state: dict, name: str, label: str, evidence: str):
  state["claims"].append({"claim": name, "label": label, "evidence": evidence})

def host_of(url: str) -> str:
  retVal = urlparse(url or "").netloc.lower()
  if retVal.startswith("www."): retVal = retVal[4:]
  return retVal

# Registrable domain heuristic: last 2 labels, last 3 for country second-level domains (example.co.uk, calhfa.ca.gov)
def registrable(host: str) -> str:
  labels = (host or "").lower().split(".")
  if len(labels) > 2 and len(labels[-1]) == 2 and labels[-2] in ["co", "com", "org", "gov", "ac", "net", "edu"]: return ".".join(labels[-3:])
  if len(labels) > 2 and labels[-1] == "gov" and len(labels[-2]) == 2: return ".".join(labels[-3:])
  return ".".join(labels[-2:])

def letters(text: str) -> str:
  retVal = ""
  for character in (text or "").lower():
    if character.isalnum(): retVal += character
  return retVal

def head_term(term: str) -> str:
  words = term.split()
  if len(words) >= 3: return " ".join(words[:-1])
  return term

def other_region(term: str, region: str) -> bool:
  if region.upper() != "US": return False
  words = term.lower().replace("£", " £ ").replace("€", " € ").split()
  for marker in OTHER_REGION_MARKERS:
    if marker in words: return True
  return False

def flow_keywords(state: dict, seed: str, region: str):
  add_manual_sources(state, "keywords")
  youtube = step(state, 1, "youtube", "youtube/query.py", ["search", seed, "--max-results", "10"], 0.0)
  sources = {seed.lower(): ["seed"]}
  suggestion_calls = [("tiktok-suggestions", ["tiktok-suggestions", seed, "--region", region]), ("youtube-typeahead", ["youtube-typeahead", seed])]
  for name, arguments in suggestion_calls:
    data = step(state, 2, "scrapecreators", "scrapecreators/query.py", arguments, SCRAPECREATORS_CREDIT_USD)
    batches = [(name, data["rows"])]
    if state["steps"][-1]["status"] == "OK" and len(data["rows"]) < MIN_SUGGESTION_ROWS and head_term(seed) != seed:
      warn(state, f"{plural(len(data['rows']), 'suggestion row')} -> retry with head term '{head_term(seed)}' (head-term proxy)")
      retry = step(state, 2, "scrapecreators", "scrapecreators/query.py", [name, head_term(seed)] + arguments[2:], SCRAPECREATORS_CREDIT_USD)
      batches.append((f"{name} head term", retry["rows"]))
    for source_name, batch_rows in batches:
      for row in batch_rows:
        term = " ".join(str(row.get("title") or "").lower().split())
        if not term: continue
        if term not in sources: sources[term] = []
        if source_name not in sources[term]: sources[term].append(source_name)
  candidates = list(sources.keys())
  volume = step(state, 2, "dataforseo", "dataforseo/query.py", ["search-volume"] + candidates[:1000], DATAFORSEO_ESTIMATE_USD["search-volume"])
  rows = []
  dropped = []
  for row in volume["rows"]:
    term = row.get("keyword", "")
    term_sources = sources.get(term, ["dataforseo"])
    flags = []
    if other_region(term, region): flags.append("other region")
    head_only = True
    for source_name in term_sources:
      if not source_name.endswith("head term"): head_only = False
    if head_only: flags.append("head-term proxy")
    entry = {"keyword": term, "volume": row.get("volume") or 0, "cpc": row.get("cpc"), "competition": row.get("competition"), "sources": ", ".join(term_sources), "flag": ", ".join(flags)}
    if entry["volume"] > 0: rows.append(entry)
    else: dropped.append(term)
  if volume["rows"] and not rows: warn(state, "every candidate has zero volume -> check region and spelling of the seed")
  rows.sort(key=volume_sort_key, reverse=True)
  useful = 0
  proxies = 0
  for row in rows:
    if row["volume"] >= USEFUL_VOLUME and "head-term proxy" not in row["flag"]: useful += 1
    if "head-term proxy" in row["flag"]: proxies += 1
  providers = []
  if youtube["rows"]: providers.append("youtube")
  if len(candidates) > 1: providers.append("scrapecreators")
  if rows: providers.append("dataforseo")
  claim(state, "existence", label_for(providers), f"providers with data: {', '.join(providers) or 'none'}")
  if rows: claim(state, "size", "SINGLE-SOURCE (by design)", f"only DataForSEO measures Google volume; {useful} of {len(candidates)} candidates >= {USEFUL_VOLUME} searches per month (head-term proxies excluded: {proxies}), {len(dropped)} with zero volume")
  else: claim(state, "size", "NO DATA", "volume step skipped or failed")
  state["rows"] = rows
  state["columns"] = [("Keyword", "keyword", 45), ("Volume", "volume", 8), ("CPC", "cpc", 6), ("Competition", "competition", 11), ("Sources", "sources", 36), ("Flag", "flag", 16)]
  state["result"] = {"candidates": len(candidates), "dropped_zero_volume": dropped}

def volume_sort_key(row: dict) -> int:
  return row["volume"]

# Recurring hosts first, then alphabetical
def serp_sort_key(row: dict) -> tuple:
  return (row["recurring"] != "yes", row["host"])

def providers_with_rows(named_results: list) -> list:
  retVal = []
  for name, rows in named_results:
    if rows: retVal.append(name)
  return retVal

# Names ordered by count, highest first; ties keep insertion order
def by_count_descending(counts: dict) -> list:
  retVal = list(counts.keys())
  retVal.sort(key=counts.get, reverse=True)
  return retVal

def label_for(providers: list) -> str:
  if len(providers) >= 2: return "CONFIRMED"
  if len(providers) == 1: return "SINGLE-SOURCE"
  return "NO DATA"

def flow_serp(state: dict, keyword: str, region: str):
  add_manual_sources(state, "serp")
  google = step(state, 2, "scrapecreators", "scrapecreators/query.py", ["google-search", keyword, "--region", region], SCRAPECREATORS_CREDIT_USD)
  serp = step(state, 2, "dataforseo", "dataforseo/query.py", ["serp", keyword], DATAFORSEO_ESTIMATE_USD["serp"])
  dataforseo_domains = []
  for row in serp["rows"]: dataforseo_domains.append(registrable(row.get("domain", "")))
  if dataforseo_domains and dataforseo_domains.count("google.com") == len(dataforseo_domains): warn(state, "every DataForSEO result has domain google.com -> redirect links not resolved; host comparison skipped")
  redirects_unresolved = state["steps"][-1]["status"] == "WARN"
  hosts = {}
  for provider, provider_rows in [("scrapecreators", google["rows"]), ("dataforseo", serp["rows"])]:
    if provider == "dataforseo" and redirects_unresolved: continue
    for index, row in enumerate(provider_rows):
      name = registrable(host_of(row.get("url", ""))) if provider == "scrapecreators" else registrable(row.get("domain", ""))
      if not name: continue
      if name not in hosts: hosts[name] = {"host": name, "scrapecreators": "", "dataforseo": "", "title": row.get("title", "")}
      if not hosts[name][provider]: hosts[name][provider] = str(index + 1)
  rows = list(hosts.values())
  recurring = []
  for row in rows:
    row["recurring"] = "yes" if row["scrapecreators"] and row["dataforseo"] else ""
    if row["recurring"]: recurring.append(row["host"])
  rows.sort(key=serp_sort_key)
  if not google["rows"] or not serp["rows"]: claim(state, "supply", label_for(providers_with_rows([("scrapecreators", google["rows"]), ("dataforseo", serp["rows"])])), "one provider returned no results")
  elif len(recurring) >= 2: claim(state, "supply", "CONFIRMED", f"{len(recurring)} hosts recur in both providers: {', '.join(recurring)}")
  else: claim(state, "supply", "CONFLICT", f"{plural(len(recurring), 'recurring host')} (CONFIRMED needs 2); a SERP is a sample -> compare result types in the titles, not ranks")
  if serp["rows"]: claim(state, "ai_overview", "SINGLE-SOURCE (by design)", f"DataForSEO: AI Overview {'present' if serp.get('ai_overview_present') else 'not present'}; features: {', '.join(serp.get('serp_feature_types') or [])}")
  state["rows"] = rows
  state["columns"] = [("Host", "host", 32), ("SC pos", "scrapecreators", 6), ("DFS pos", "dataforseo", 7), ("Recurring", "recurring", 9), ("Title", "title", 60)]
  state["result"] = {"recurring_hosts": recurring, "ai_overview_present": serp.get("ai_overview_present"), "serp_feature_types": serp.get("serp_feature_types")}

# Brand letters inside a host name mark brand-owned or brand-listicle hosts (calendly-alternatives.org); brands shorter than MIN_BRAND_LETTERS match only exactly
def contains_brand(text: str, brand: str) -> bool:
  brand_letters = letters(brand)
  if len(brand_letters) < MIN_BRAND_LETTERS: return brand_letters != "" and letters(text) == brand_letters
  return brand_letters in letters(text)

def is_excluded_host(name: str, own_domain: str, brand: str) -> bool:
  if name == own_domain or name in GENERIC_DOMAINS: return True
  return contains_brand(name.split(".")[0], brand)

def flow_competitors(state: dict, domain: str, region: str, brand: str, ads_count: int):
  own_domain = registrable(host_of("https://" + domain.split("://")[-1]))
  brand = brand or own_domain.split(".")[0]
  add_manual_sources(state, "competitors")
  step(state, 1, "youtube", "youtube/query.py", ["search", f"{brand} alternatives", "--max-results", "10"], 0.0)
  serp_counts = {}
  for query in [f"{brand} alternatives", f"{brand} competitors", f"{brand} vs"]:
    data = step(state, 2, "scrapecreators", "scrapecreators/query.py", ["google-search", query, "--region", region], SCRAPECREATORS_CREDIT_USD)
    seen = []
    for row in data["rows"]:
      name = registrable(host_of(row.get("url", "")))
      if name and name not in seen and not is_excluded_host(name, own_domain, brand): seen.append(name)
    for name in seen: serp_counts[name] = serp_counts.get(name, 0) + 1
  serp_set = []
  for name in by_count_descending(serp_counts):
    if serp_counts[name] >= 2: serp_set.append(name)
  if not serp_set and serp_counts:
    warn(state, "no host recurs in 2 of 3 SERPs -> using hosts from single SERPs")
    serp_set = by_count_descending(serp_counts)[:10]
  competitors = step(state, 2, "dataforseo", "dataforseo/query.py", ["competitors", own_domain, "--limit", str(COMPETITOR_LIMIT)], DATAFORSEO_ESTIMATE_USD["competitors"])
  dataforseo_set = []
  generic_count = 0
  for row in competitors["rows"]:
    name = registrable(row.get("domain", ""))
    if name in GENERIC_DOMAINS: generic_count += 1
    if name and not is_excluded_host(name, own_domain, brand) and name not in dataforseo_set: dataforseo_set.append(name)
  verified = []
  for name in serp_set:
    if name in dataforseo_set: verified.append(name)
  if competitors["rows"] and not verified: warn(state, f"no DataForSEO domain appears in the SERP set ({plural(generic_count, 'generic row')} dropped) -> keyword overlap, not product similarity")
  if verified: claim(state, "competitors", "CONFIRMED", f"in SERP set and DataForSEO: {', '.join(verified)}")
  elif serp_set and competitors["rows"]: claim(state, "competitors", "CONFLICT", "SERP set and DataForSEO do not intersect -> continuing with the SERP set")
  else: claim(state, "competitors", label_for(providers_with_rows([("scrapecreators", serp_set), ("dataforseo", dataforseo_set)])), "one provider returned no competitor")
  targets = verified[:]
  for name in serp_set:
    if name not in targets: targets.append(name)
  ads_summary = {}
  for name in targets[:ads_count]:
    data = step(state, 2, "scrapecreators", "scrapecreators/query.py", ["google-ads", name, "--region", region], SCRAPECREATORS_CREDIT_USD)
    advertisers = {}
    for row in data["rows"]: advertisers[row.get("title") or "[UNKNOWN]"] = advertisers.get(row.get("title") or "[UNKNOWN]", 0) + 1
    own = 0
    for advertiser, count in advertisers.items():
      if contains_brand(advertiser, name.split(".")[0]): own += count
    top = by_count_descending(advertisers)[:1]
    ads_summary[name] = {"ads": len(data["rows"]), "own_brand_ads": own, "advertisers": len(advertisers), "top_advertiser": f"{top[0]} ({advertisers[top[0]]})" if top else ""}
  if ads_summary: claim(state, "ads", "SINGLE-SOURCE (by design)", "Google Ads Transparency via ScrapeCreators; ads linking to the domain include customers and affiliates, see own_brand_ads")
  listed = serp_set[:]
  for name in dataforseo_set[:10]:
    if name not in listed: listed.append(name)
  rows = []
  for name in listed:
    ads = ads_summary.get(name, {})
    rows.append({"domain": name, "serp_count": serp_counts.get(name, 0), "in_dataforseo": "yes" if name in dataforseo_set else "", "verified": "yes" if name in verified else "",
      "ads": ads.get("ads", ""), "own_brand_ads": ads.get("own_brand_ads", ""), "top_advertiser": ads.get("top_advertiser", "")})
  state["rows"] = rows
  state["columns"] = [("Domain", "domain", 30), ("SERPs", "serp_count", 5), ("In DFS", "in_dataforseo", 6), ("Verified", "verified", 8), ("Ads", "ads", 4), ("Own ads", "own_brand_ads", 7),
    ("Top advertiser", "top_advertiser", 40)]
  state["result"] = {"serp_set": serp_set, "verified": verified, "ads_targets": targets[:ads_count], "dataforseo_generic_rows": generic_count}

def run_flow(args) -> dict:
  state = {"keys_file": args.keys_file, "max_usd": args.max_usd, "spent_usd": 0.0, "steps": [], "claims": [], "rows": [], "columns": [], "result": {}}
  if args.flow == "keywords": flow_keywords(state, args.target, args.region)
  if args.flow == "serp": flow_serp(state, args.target, args.region)
  if args.flow == "competitors": flow_competitors(state, args.target, args.region, args.brand, args.ads)
  notes = [f"Spent: ${state['spent_usd']:.4f} of ${state['max_usd']:.2f} budget"]
  return {"flow": args.flow, "target": args.target, "region": args.region, "spent_usd": round(state["spent_usd"], 4), "steps": state["steps"], "claims": state["claims"],
    "rows": state["rows"], "columns": state["columns"], "result": state["result"], "notes": notes}

# ----------------------------------------- END: Run flows ---------------------------------------------------------------------


# ----------------------------------------- START: CLI -------------------------------------------------------------------------

def print_table(rows: list, columns: list = None):
  columns = columns or [("Tier", "tier_name", 12), ("Provider", "provider", 22), ("Status", "status", 34), ("Balance", "balance", 14), ("Note", "note", 60)]
  print("  ".join(f"{header:<{width}}" for header, key, width in columns))
  print("  ".join("-" * width for header, key, width in columns))
  for row in rows:
    cells = []
    for header, key, width in columns:
      value = row.get(key)
      cells.append(f"{('' if value is None else str(value))[:width]:<{width}}")
    print("  ".join(cells))

def build_parser() -> argparse.ArgumentParser:
  parser = argparse.ArgumentParser(description="Source tier probe and Tier 1 + Tier 2 run flows for the seo-tools skill.", formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__)
  subparsers = parser.add_subparsers(dest="command", required=True)
  probe = subparsers.add_parser("probe", help="Report which tiers and providers are usable")
  probe.add_argument("--keys-file", type=Path, default=DEFAULT_KEYS_FILE, help="Credentials file (default: [WORKSPACE_FOLDER]/../.tools/.api-keys.txt)")
  probe.add_argument("--format", choices=["table", "json"], default="table", help="Output format (default: table)")
  probe.add_argument("--balances", action="store_true", help="Also call the $0 balance commands of ScrapeCreators and DataForSEO")
  run = subparsers.add_parser("run", help="Run the Tier 1 and Tier 2 sequence of one matrix row with checks and a claim ledger")
  run.add_argument("flow", choices=["keywords", "serp", "competitors"], help="keywords: matrix row 2; serp: row 3; competitors: row 4")
  run.add_argument("target", help="Seed keyword (keywords, serp) or domain (competitors)")
  run.add_argument("--region", default="US", help="Region code for ScrapeCreators calls (default: US; DataForSEO uses its default location 2840 = US)")
  run.add_argument("--brand", default="", help="Brand name for competitor queries (default: first label of the domain)")
  run.add_argument("--ads", type=int, default=2, help="Competitor domains checked with google-ads (default: 2, 1 credit each)")
  run.add_argument("--max-usd", type=float, default=DEFAULT_MAX_USD, help=f"Budget for all paid steps; a step above it is skipped (default: {DEFAULT_MAX_USD:.2f})")
  run.add_argument("--keys-file", type=Path, default=DEFAULT_KEYS_FILE, help="Credentials file (default: [WORKSPACE_FOLDER]/../.tools/.api-keys.txt)")
  run.add_argument("--format", choices=["table", "json"], default="table", help="Output format (default: table)")
  return parser

def main():
  if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
  if hasattr(sys.stderr, "reconfigure"): sys.stderr.reconfigure(encoding="utf-8")
  args = build_parser().parse_args()
  if args.command == "run":
    result = run_flow(args)
    if args.format == "json":
      result.pop("columns", None)
      print(json.dumps(result, ensure_ascii=False, indent=2))
      return
    print_table(result["steps"], [("Tier", "tier", 4), ("Provider", "provider", 15), ("Call", "call", 50), ("Rows", "rows", 4), ("Cost USD", "cost_usd", 8), ("Status", "status", 16), ("Check", "check", 70)])
    print()
    print_table(result["rows"], result["columns"])
    print()
    print_table(result["claims"], [("Claim", "claim", 12), ("Label", "label", 26), ("Evidence", "evidence", 110)])
    for note in result["notes"]: print(note)
    return
  result = run_probe(args)
  if args.format == "json":
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return
  print_table(result["rows"])
  for note in result["notes"]: print(note)

# ----------------------------------------- END: CLI ---------------------------------------------------------------------------

if __name__ == "__main__":
  main()
