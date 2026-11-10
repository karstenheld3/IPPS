# SPEC: SEO Tools Skill (SEO-First Upgrade)

**Doc ID**: SEOFIRST-SP01
**Feature**: SEOTOOLS_SKILL
**Goal**: Specify the upgrade of the `seo-tools` skill from raw data retrieval to an SEO-first working skill with lifecycle guides, normative rules, executable checks, and MCP-free Python provider scripts
**Timeline**: Created 2026-11-10, Updated 5 times (2026-11-10 - 2026-11-10)
**Target file(s)**:
- `[PROMPTSYSTEM_FOLDER]/skills/seo-tools/` (all files, see SEOFIRST-FR-01)

**Depends on:**
- `_INFO_SEOGUIDE-12_SkillBlueprint.md [SEOFIRST-SEOGUIDE-IN12]` (session research, not versioned) for artifact areas, lifecycle mapping, media checklists, provider change list
- `_INFO_SEOGUIDE-03..11 [SEOFIRST-SEOGUIDE-IN03..IN11]` (session research, not versioned) for rule content, metadata limits, prices, endpoints
- `@skills:coding-conventions` for Python style, UTF-8 IO, logging rules

**Does not depend on:**
- `_SPEC_AGENT_CREATED_FOLDERS.md [AGNTFOLDERS-SP01]` (the skill creates no utility folders)
- Any MCP server specification (MCP is out of scope, see SEOFIRST-DD-04)

## MUST-NOT-FORGET

- No MCP servers, no `npx`, no `uvx`, no PowerShell scripts in the skill. Every provider is a Python script (SEOFIRST-DD-04)
- General-purpose skill: no drive-letter paths, no real customer domains, brands, or keywords. Examples use `example.com` (privacy gate Dimension 1)
- Credentials only via `[API_KEYS_FILE]`; secrets never printed
- Credential key names follow SEOFIRST-DD-09 and are registered in `SKILL.md` section "Credential Keys"; no script reads an unregistered name
- Paid calls (DataForSEO) only after a printed cost estimate that stays under `--max-cost`
- Google Indexing API only for `JobPosting` or `BroadcastEvent` pages; never for regular URLs
- Every rule carries an evidence label and a source URL with access date; folklore goes to the Do-Not-Do list without rule ID
- Prices and platform limits are `[LITERAL: 2026-11-03]` values; copy character-for-character from research

## Table of Contents

1. [Scenario](#1-scenario)
2. [Context](#2-context)
3. [Domain Objects](#3-domain-objects)
4. [Functional Requirements](#4-functional-requirements)
5. [Non-Functional Requirements](#5-non-functional-requirements)
6. [Design Decisions](#6-design-decisions)
7. [Implementation Guarantees](#7-implementation-guarantees)
8. [Key Mechanisms](#8-key-mechanisms)
9. [Action Flow](#9-action-flow)
10. [Data Structures](#10-data-structures)
11. [Logging Requirements](#11-logging-requirements)
12. [Technical Constraints](#12-technical-constraints)
13. [Document History](#13-document-history)

## 1. Scenario

**Problem:** The current `seo-tools` skill only fetches data. It has no decision rules for ideation, creation, publishing, audit, campaigns, or metadata. A claim audit (2026-11-03) of 28 claims found 9 wrong and 4 outdated claims, among them: Google Indexing API used for regular URLs, two non-existent MCP packages, DataForSEO prices off by 12x-100x, missing `load_async_ai_overview`, hardcoded drive paths, fictional Google Search Console (GSC) tool names, outdated Plausible pricing, incomplete IndexNow engine list.

**Solution:**
- Four root knowledge files: router (`SKILL.md`), procedures (`SEO_GUIDES.md`), normative rules and platform limits (`SEO_RULES.md`), gates, audit, scoring, and alerts (`SEO_CHECKS.md`)
- One Python script per provider, all sharing one CLI contract (credentials, output format, cost gate, logging)
- Free-first escalation: first-party free sources before any paid call
- Offline pre-publish linter that enforces platform length limits and prohibited tokens

**What we don't want:**
- MCP server configurations or tool lists that depend on third-party packages
- PowerShell and Python duplicates of the same script
- Advice without evidence label; vendor folklore presented as rule
- Paid API calls without cost estimate
- Many small per-platform knowledge files
- Hardcoded machine paths or real customer data in skill files

### Architecture (BEFORE)

```
seo-tools/
├─> SKILL.md                      (data-call intent lookup, wrong prices, MCP tool names)
├─> dataforseo/   SETUP.md, ENDPOINTS.md, query.py, query.ps1   (paid, outdated prices)
├─> google-search-console/   SETUP.md                           (2 broken MCP options)
├─> indexnow/   SETUP.md, submit.ps1
└─> plausible/   SETUP.md                                       (no script)
```

### Architecture (AFTER)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ Knowledge layer (Markdown, loaded on demand)                                 │
│  SKILL.md ─────> lifecycle router + When-to-Query-What matrix + script index │
│  SEO_GUIDES.md ─> procedures per lifecycle stage, campaigns, metadata steps  │
│  SEO_RULES.md ──> SEO-* rules + platform metadata field limits               │
│  SEO_CHECKS.md ─> pre-publish gate, audit, MOS scoring, decay, alerts        │
├──────────────────────────────────────────────────────────────────────────────┤
│ Execution layer (Python 3.10+, shared CLI contract, [API_KEYS_FILE])         │
│  prepublish-lint.py ──────────> offline gate checks              ($0)        │
│  agent-readiness/check.py ────> HTTP probes of a public site     ($0)        │
│  google-search-console/query.py > GSC Search Analytics, Inspection ($0)      │
│  bing-webmaster/query.py ─────> Bing Webmaster JSON API          ($0)        │
│  indexnow/submit.py ──────────> IndexNow push                    ($0)        │
│  youtube/query.py ────────────> YouTube Data API v3              ($0, quota) │
│  plausible/query.py ──────────> Plausible Stats API v2   ($0 CE / paid plan) │
│  dataforseo/query.py ─────────> DataForSEO v3 (cost gate)        (paid)      │
│  trendsmcp/query.py ──────────> cross-platform trend index (REST) (credits)  │
│  scrapecreators/query.py ─────> social post-level data (REST)    (credits)   │
└──────────────────────────────────────────────────────────────────────────────┘
```

## 2. Context

- `seo-tools` lives in `[PROMPTSYSTEM_FOLDER]/skills/seo-tools/` and is mirrored to `[AGENT_FOLDER]` by robocopy. Downstream repos receive it through `sync.ps1`
- Consumers: writing workflows (`/write-article`, `/write-report`, `/write-ebook`, `/propose-*`), `/deploy` as pre-publish gate, and standalone use (audit, campaign planning, research questions)
- The agent has terminal, Python venv at `[SKILL_TOOLS_FOLDER]/llm-venv/`, Playwright MCP (agent tool, not part of the skill), and web search
- Content source: deep research `SEOFIRST-SEOGUIDE-IN01..IN12` (87 sources, 72 metadata field specs, accessed 2026-11-03). The research has 101 rules: 97 domain rules (carried into the skill) and 4 blueprint rules `BLP-01..04` about the skill itself (implemented by this SPEC, not copied). The research lives in a private session folder; the skill must be self-contained and must not reference research document IDs or paths
- Acronyms added 2026-11-10: Model Context Protocol (MCP), Representational State Transfer application programming interface (REST API); "Trends MCP" is a vendor name, the skill calls only its REST API
- User decisions 2026-11-10: 4-file root layout; no MCP, Python scripts only; repair existing scripts and add Bing Webmaster script and pre-publish linter; SPEC in `[DEV_SPECS_FOLDER]`, IMPL in session; zero-cost tests plus one capped DataForSEO live test (`< $1`); standardized credential key names registered in `SKILL.md`; relative file paths in `[API_KEYS_FILE]`
- Decision IDs: `SEOFIRST-DD-01..09` are user decisions recorded in the session; this SPEC reuses those IDs where it states the same decision and numbers its own engineering decisions from `SEOFIRST-DD-10` to `SEOFIRST-DD-20`; `SEOFIRST-DD-21` is a later user decision (trend and social providers) recorded in the session under the same ID
- Acronyms: Search Engine Results Page (SERP), click-through rate (CTR), Generative Engine Optimization (GEO), Kindle Direct Publishing (KDP), Google Business Profile (GBP), Plausible Community Edition (CE, self-hosted), year over year (YoY)

## 3. Domain Objects

### Lifecycle Stage

A **Lifecycle Stage** is a phase of SEO work the router dispatches to.
- `IDEATE` - demand-first opportunity finding, shaping, naming
- `CREATE` - media-specific structure, agent readiness, entity anchoring
- `PUBLISH` - metadata generation, pre-publish gate, indexing push
- `IMPROVE` - audit, decay triage, opportunity scoring, campaigns, competitor gaps
- `RESEARCH` - answering a data question with the cheapest sufficient source
- `MONITOR` - scheduled alert checks

### Rule

A **Rule** is one normative, testable requirement in `SEO_RULES.md`.
- `id` - `SEO-[DOMAIN]-[NN]`; domains: `FND` foundations, `DMD` demand, `MTX` text and book media, `MAV` audio and video, social, apps, local business, localization, `AGT` agent discoverability, `AUD` audit, `CMP` campaigns, `MTD` metadata, `TLS` tools and data
- `statement` - single imperative sentence block with concrete limits
- `evidence` - `[VERIFIED]`, `[ASSUMED]`, or `[COMMUNITY]`
- `sources` - one or more URLs with access date `YYYY-MM-DD`

### Metadata Field Spec

A **Metadata Field Spec** is one platform field limit in `SEO_RULES.md`.
- `platform_group` - one of 10: Web head, Open Graph and agent frontmatter, Schema.org, images and PDFs, video, podcasts, books, apps, local business, social
- `field`, `indexed` (yes/no/partial), `limit` (`[LITERAL: 2026-11-03]`), `truncation`, `prohibited`, `source`

### Gate Check

A **Gate Check** is a PASS/FAIL item of the pre-publish gate in `SEO_CHECKS.md`.
- `id` - `GATE-WEB-01..09`, `GATE-BOOK-01..04`, `GATE-APP-01..02`, `GATE-VID-01`, `GATE-POD-01`, `GATE-GBP-01`, `GATE-SOC-01`, `GATE-COMPL-01` (20 items)
- `rules` - referenced `SEO-*` rule IDs
- `automated` - `lint` (checked by `prepublish-lint.py`), `probe` (checked by `agent-readiness/check.py`), or `manual`

### Provider Script

A **Provider Script** is a Python CLI wrapping one data source.
- `path` - `[provider]/query.py`, `indexnow/submit.py`, `agent-readiness/check.py`, or root `prepublish-lint.py`
- `commands` - CLI subcommands
- `cost_class` - `free`, `quota` (free with daily quota), `credits` (prepaid credits, free tier available), `paid`
- `credential_keys` - key names read from `[API_KEYS_FILE]`

### Credential Entry

A **Credential Entry** is one `KEY=VALUE` line in `[API_KEYS_FILE]`. Name format `[PROVIDER]_[QUALIFIER_][SUFFIX]` (SEOFIRST-DD-09). Complete registry:
- `DATAFORSEO_LOGIN` - required for `dataforseo/query.py`; API login (registration email)
- `DATAFORSEO_PASSWORD` - required for `dataforseo/query.py`; API password (not the account password)
- `GSC_SERVICE_ACCOUNT_FILE` - required for `google-search-console/query.py`; file name of the service account JSON stored in the folder of `[API_KEYS_FILE]`; relative paths resolve against that folder; documentation and examples use relative paths only (absolute paths are accepted but not documented)
- `BING_WEBMASTER_API_KEY` - required for `bing-webmaster/query.py`
- `INDEXNOW_API_KEY` - optional for `indexnow/submit.py`; `--key` overrides
- `PLAUSIBLE_API_KEY` - required for `plausible/query.py`
- `PLAUSIBLE_BASE_URL` - optional for `plausible/query.py`; default `https://plausible.io`
- `YOUTUBE_API_KEY` - required for `youtube/query.py`
- `TRENDSMCP_API_KEY` - required for `trendsmcp/query.py` (REST API key; the vendor name contains "MCP", the skill uses REST only)
- `SCRAPECREATORS_API_KEY` - required for `scrapecreators/query.py`; sent as `x-api-key` header
- Not part of the standard: `DATAFORSEO_BASE64` (legacy line, ignored; scripts build Basic auth from login and password)

### Opportunity Score (MOS)

An **Opportunity Score** ranks audit fixes and content opportunities.
- Inputs `D` demand, `I` intent value, `F` feasibility, `B` business fit, `C` confidence, each 1-5 with rubric in `SEO_CHECKS.md`
- `MOS = 100 * ((D^0.20 * I^0.25 * F^0.25 * B^0.20 * C^0.10) / 5) * G_gate`, `G_gate = 0` if `B = 1` or `I = 1`, else 1
- `MOS_ROI = (MOS * Confidence_Factor) / Effort_Hours`
- Evidence `[ASSUMED]` (no composite formula has longitudinal causal proof); weights are constants in one block

## 4. Functional Requirements

### Knowledge files

**SEOFIRST-FR-01: File layout**
- Root: `SKILL.md`, `SEO_GUIDES.md`, `SEO_RULES.md`, `SEO_CHECKS.md`, `prepublish-lint.py`
- `dataforseo/`: `SETUP.md`, `ENDPOINTS.md`, `query.py`
- `google-search-console/`: `SETUP.md`, `query.py`
- `bing-webmaster/`: `SETUP.md`, `query.py`
- `indexnow/`: `SETUP.md`, `submit.py`
- `plausible/`: `SETUP.md`, `query.py`
- `youtube/`: `SETUP.md`, `query.py`
- `trendsmcp/`: `SETUP.md`, `query.py` (SEOFIRST-DD-21)
- `scrapecreators/`: `SETUP.md`, `query.py` (SEOFIRST-DD-21)
- `agent-readiness/`: `check.py` (no credentials, usage documented in `SKILL.md`)
- No other files. Removed: `dataforseo/query.ps1`, `indexnow/submit.ps1`
- No `UNINSTALL.md` files (SEOFIRST-DD-20)
- Skill resource files (`SEO_GUIDES.md`, `SEO_RULES.md`, `SEO_CHECKS.md`, `ENDPOINTS.md`) contain no bold markup and no Document History section; `SKILL.md` is the only entry point

**SEOFIRST-FR-02: `SKILL.md` router**
- Frontmatter: `name: seo-tools`; `description` names SEO-first scope (ideation, creation, metadata, pre-publish gate, audit, campaigns, monitoring, agent discoverability, data queries); `compatibility: Python 3.10+ (requests; google-auth for GSC)`
- MUST-NOT-FORGET: free-first, cost gate, Indexing API restriction, `[API_KEYS_FILE]`, pre-publish gate before publishing, evidence labels
- When to use / When not to use (not for: paid ads management, general web analytics questions without SEO intent, legal review of claims)
- Architecture: knowledge files and scripts with their relations (diagram)
- Lifecycle router: each stage `IDEATE`, `CREATE`, `PUBLISH`, `IMPROVE`, `RESEARCH`, `MONITOR` with trigger condition and pointer to the `SEO_GUIDES.md` section
- When-to-Query-What matrix: 10 question types (demand trajectory, keyword sizing, SERP overlap, competitor gap, technical and agent readiness, owned ranking and decay, backlinks, AI citation, conversion, indexing push), each with 1st free source and 2nd paid fallback, mapped to a script command or a manual UI step
- Trend discovery order in the matrix row for demand trajectory: 1) free sources, 2) one `trendsmcp` call (`growth` or `board`) to find candidates, 3) `scrapecreators` depth calls only for the top candidates (SEOFIRST-DD-21)
- Intent lookup: user intent → exact script command line
- Provider registry: per script commands, cost class, `SETUP.md` pointer; credentials referenced by pointing to section "Credential Keys" (key names are not repeated)
- Limitations: UI-only data (GSC Generative AI report, Bing AI Performance), deferred sources (SEOFIRST-FR-16), no rank tracking history beyond GSC 16 months
- Sources: official documentation URLs per provider with access date
- Section "Credential Keys": the single registry of all credential key names (SEOFIRST Credential Entry) with naming rule, provider, required or optional, value format, and `SETUP.md` pointer; `SETUP.md` files and scripts use exactly these names
- Size target: `<= 300` lines

**SEOFIRST-FR-03: `SEO_GUIDES.md` procedures**
- One section per lifecycle stage with numbered steps, inputs, outputs, rule references, and the script commands each step uses; no checklists (checklists go to `SEO_CHECKS.md`)
- `IDEATE`: 3-pillar demand triangulation, SERP-overlap clustering (`>= 3` shared top-10 URLs → one page; `< 3` → separate pages), AI Overview displacement pivot, 5-step pre-build validation, 4 naming gates
- `CREATE`: 12 media playbooks (web, articles, PDFs, developer docs, images, books, video, podcasts, social, apps, local business, offline) with minimal requirement checklists, 4 competitive GEO gatekeepers, agent readiness by site type A-D, entity and brand memory, localization
- `PUBLISH`: 5-step metadata generation pipeline (front-loading, set-difference keyword packing, 5 description variants, schema and thumbnail parity, accessibility and AI provenance), post-publish push (IndexNow, sitemap `<lastmod>`, GSC annotation, propagation windows)
- `IMPROVE`: pre-audit hygiene, 7-layer audit, 4-signature decay classification, 6 triage actions, MOS ranking, 6-step competitor gap method, 9 campaign templates with velocity bands, 20% holdout, `>= 8` repetitions per prompt for AI visibility sampling (research range 7-8; upper bound used)
- `RESEARCH`: escalation protocol and pre-batch cost estimate procedure
- `MONITOR`: daily and 4-6-week monitoring runs mapped to alerts in `SEO_CHECKS.md`
- Do-Not-Do list: practices with zero or negative evidence (FAQ blocks and `FAQPage` for AI citation, author boxes, body-only stylistic GEO rewrites, `/llms.txt` for Google Search, fake `dateModified`, query fan-out doorway pages, Apple Podcasts review campaigns for ranking), each with source URL

**SEOFIRST-FR-04: `SEO_RULES.md` normative rules**
- All 97 domain rules of the research (`FND` 12, `DMD` 10, `MTX` 14, `MAV` 12, `AGT` 12, `AUD` 7, `CMP` 8, `MTD` 12, `TLS` 10), renumbered `SEO-[DOMAIN]-[NN]` with the same domain and number
- `TLS` rules rewritten for script access paths (no MCP), keeping endpoints, quotas, and prices
- Rule Index at top: one line per rule ID with title, grouped by domain
- Each rule: ID, title, statement, evidence label, source URLs with access date
- BAD/GOOD example pair for every rule whose statement constrains a concrete field, markup, or file (domains `MTD`, `MTX`, `MAV`, `AGT`, `FND` where applicable); examples use `example.com` and generic products
- Platform metadata field section: the 72 research fields in 10 platform groups, written as 54 entries (related fields share one entry, one line per entry), limits tagged `[LITERAL: 2026-11-03]`
- Rules contain no procedure steps (those go to `SEO_GUIDES.md`) and no checklists (those go to `SEO_CHECKS.md`)

**SEOFIRST-FR-05: `SEO_CHECKS.md` gates, audit, scoring, alerts**
- Constants block at top: MOS weights, decay thresholds (`>= 20%` 3-month YoY click loss and `>= 50` lost clicks), RE-TITLE thresholds, monitoring alert thresholds, cost gate default; each constant with evidence label
- Every check item in this file states action, evidence, and failure indicator
- 20-item pre-publish gate (SEOFIRST Gate Check), each item with rule references and `automated` marker
- 5 prohibited-token regexes (SEOFIRST-FR-17)
- 12-media minimal requirements checklist
- 7-layer audit checklist
- MOS and MOS_ROI with 1-5 rubrics per input and free-data fallback for every input
- 4-signature decay triage table with action, effort hours, and preconditions; PRUNE preconditions
- 6 monitoring alerts with cadence, threshold, data source, and triggered action

### Script contract

**SEOFIRST-FR-06: Common CLI contract (all scripts)**
- Python 3.10+, subcommands, `--help` works without credentials and without network
- `--keys-file PATH` overrides the default credentials path (SEOFIRST-FR-07)
- `--format table|json` (default `table`); JSON goes to stdout as one object (SEOFIRST Data Structures)
- Progress and errors to stderr; results to stdout
- Exit codes: `0` success, `1` request or API error, `2` usage or precondition error (missing key, cost gate exceeded, invalid input)
- HTTP timeout 30s; retry on HTTP 429 and 5xx up to 3 times with exponential backoff (1s, 2s, 4s); honor `Retry-After`
- UTF-8 for all file and network text
- Self-contained: no imports from sibling folders; third-party imports limited to `requests` and `google-auth` (GSC only)

**SEOFIRST-FR-07: Credential resolution**
- Default path: `[WORKSPACE_FOLDER]/../.tools/.api-keys.txt`, computed from the script location (skill folder depth is identical under `[PROMPTSYSTEM_FOLDER]` and `[AGENT_FOLDER]`)
- Format: `KEY=VALUE` lines, `#` comments, BOM tolerated
- Scripts read only names registered in `SKILL.md` section "Credential Keys"
- Missing file or key → exit 2 with message naming the key, the file path, and the `SETUP.md` to read
- Secret values never printed, logged, or written to JSON output

**SEOFIRST-FR-08: Cost gate (paid scripts)**
- Price table in the script, dated `2026-11-03`, identical to `dataforseo/ENDPOINTS.md`
- Before every paid request: print estimated cost in USD with formula inputs (tasks, items)
- `--max-cost USD` (default `0.10`); estimate above limit → exit 2 without request
- After the request: print actual cost when the API returns it (`cost` field), else the estimate
- `balance` command is free and runs without gate

### Provider scripts

**SEOFIRST-FR-09: `dataforseo/query.py`** (paid)
- `balance` - `GET /v3/appendix/user_data` ($0)
- `keywords SEED` - Labs `keyword_suggestions/live` ($0.012/task + $0.00012/item)
- `search-volume KW [KW...] | --file PATH` - Keywords Data `google_ads/search_volume/live`, up to 1,000 keywords per task (Live $0.09/task, Standard queue $0.06/task; Live limited to 12 requests per minute; re-verified 2026-11-10); splits larger lists into tasks
- `serp KEYWORD` - SERP `google/organic/live/advanced` with `load_async_ai_overview` true ($0.002/SERP); prints top 10 organic, AI Overview presence, SERP feature types
- `competitors DOMAIN` - Labs `competitors_domain/live` ($0.012/task + $0.00012/item)
- `backlinks DOMAIN` - Backlinks `summary/live` ($0.024/task + $0.000036/row)
- Options: `--location` (default 2840), `--lang` (default `en`), `--limit`, `--sandbox`, `--max-cost`

**SEOFIRST-FR-10: `google-search-console/query.py`** (free)
- Auth: service account JSON from `GSC_SERVICE_ACCOUNT_FILE`; read scope `webmasters.readonly`, write scope `webmasters` only for `sitemaps submit`
- `sites` - list properties
- `analytics SITE` - Search Analytics query: `--start`, `--end` (default last 28 days ending 3 days ago), `--dimensions` (query, page, country, device, date, searchAppearance), `--filter DIM:OP:VALUE`, `--search-type` (web, image, video, news, discover, googleNews), `--rows` (paginates up to 25,000 per request)
- `inspect SITE URL [URL...]` - URL Inspection (quota 2,000/day/property); prints coverage state, canonical (user vs Google), last crawl, mobile usability, rich results
- `sitemaps SITE` and `sitemaps SITE --submit SITEMAP_URL` (submit needs "Full" permission for the service account on the property; "Restricted" returns HTTP 403 with a hint)
- Derived analyses (thresholds as options, defaults from `SEO_CHECKS.md` constants):
  - `quick-wins SITE` - queries at average position 4-15 sorted by impressions
  - `ctr-gap SITE` - pages at position 1.0-10.9 with `>= 1,000` impressions in 90 days and CTR `< 0.60 *` expected CTR (RE-TITLE candidates)
  - `decay SITE` - pages with `>= 20%` and `>= 50` lost clicks, last 3 months vs same 3 months a year earlier; output includes clicks, impressions, position deltas for the 4-signature classification
  - `cannibalization SITE` - queries where `>= 2` pages each receive `>= 10%` of the query's impressions

**SEOFIRST-FR-11: `bing-webmaster/query.py`** (free)
- Auth: `BING_WEBMASTER_API_KEY` as `apikey` query parameter on the JSON endpoint `https://ssl.bing.com/webmaster/api.svc/json/`
- `sites`, `query-stats SITE`, `page-stats SITE`, `traffic SITE`, `links SITE`, `quota SITE`, `submit SITE URL [URL...]` (checks quota first)
- `SETUP.md` documents the UI-only AI Performance report (Grounding Queries, Citation Share, Topics, Intents, Compare) and how to export it

**SEOFIRST-FR-12: `indexnow/submit.py`** (free; replaces `submit.ps1`)
- `submit URL [URL...] | --file PATH` with `--host`, `--key` (or `INDEXNOW_API_KEY`), `--key-location`
- 1 URL → GET; 2+ URLs → POST JSON, chunks of `<= 10,000`
- All URLs must belong to `--host`; mismatch → exit 2
- `verify-key --host --key` fetches the key file and compares content
- `--dry-run` prints request without sending
- Status mapping: 200 OK, 202 accepted (key pending), 400 bad request, 403 key not found, 422 URL/host mismatch, 429 too many requests
- Output states the receiving engines: Bing, Yandex, Naver, Seznam, Yep; Google not covered

**SEOFIRST-FR-13: `plausible/query.py`** (free self-hosted, paid Cloud Business plan)
- Auth: `PLAUSIBLE_API_KEY`, base `PLAUSIBLE_BASE_URL`; endpoint `POST /api/v2/query`
- Presets: `summary SITE`, `top-pages SITE`, `sources SITE`, `goals SITE`; `--range` (default `30d`), `--limit`
- `raw SITE --query-file PATH` sends a custom query body
- HTTP 401/402/403 → message that Stats API needs self-hosted CE or Cloud Business plan

**SEOFIRST-FR-14: `youtube/query.py`** (free with quota)
- Auth: `YOUTUBE_API_KEY`
- `search QUERY` - `search.list` (`order=relevance`, `--max-results` default 25, `--region`, `--lang`), counted as one of at most 100 search calls per day (Google documents this as 100 units of the 10,000-unit quota or as a separate bucket of 100 calls; both allow 100 searches per day)
- `videos ID [ID...]` - `videos.list` statistics and snippet, 1 unit per call (batches of 50)
- Prints search calls and units consumed per run (daily default 10,000 units)

**SEOFIRST-FR-15: `agent-readiness/check.py`** (free, no credentials)
- `check URL --site-type A|B|C|D` (default A)
- Site types are cumulative: B = A + B checks, C = A + C checks, D = A + B + D checks (API platforms have documentation; ecommerce checks do not apply to them)
- Type A checks: `robots.txt` reachable and parseable, `Sitemap:` line, per-class AI bot directives (search/grounding vs training vs user agents), `Content-Signal` presence, `Accept: text/markdown` response with `Content-Type: text/markdown` and `Vary: Accept`
- Type B adds: `{url}/index.md`, root `/llms.txt` and content type
- Type C adds: `Product` JSON-LD on given URL; WebMCP is listed as INFO "manual check" (not detectable by HTTP probe)
- Type D adds: `/.well-known/api-catalog` (`application/linkset+json`), `/.well-known/mcp/server-card.json`, `/.well-known/agent-skills/index.json`, `/.well-known/oauth-protected-resource`
- Each check: PASS, FAIL, WARN, or INFO with `SEO-AGT-*` rule ID; `<= 20` HTTP requests per run; User-Agent identifies the checker
- Exit 0 when no FAIL, else 1

**SEOFIRST-FR-16: Deferred data sources (documented, not scripted)**
- Google Ads `KeywordPlanIdeaService` (requires Ads account and developer token) and Google Trends API alpha (requires allowlist access): listed in the matrix as "manual or not available" with DataForSEO `search-volume` and Google Trends web UI as fallbacks
- Ahrefs and Semrush: listed as subscription alternatives without integration
- X trends and X search: official X API pay-per-use (Trends `$0.010` per request, post read `$0.005`) or `twitterapi.io`; listed in the matrix as optional alternatives without script (SEOFIRST-DD-21)
- AIsa (single-balance aggregator): listed as alternative to the two credit providers pending live test; no script

### Trend and social providers (added by SEOFIRST-DD-21; IDs continue after FR-19)

**SEOFIRST-FR-20: `trendsmcp/query.py`** (credits; free tier 100 requests/month) - SEOFIRST-DD-21
- Auth: `TRENDSMCP_API_KEY` as `Authorization: Bearer` header; REST only, no MCP
- One endpoint: `POST https://api.trendsmcp.ai/api` with JSON body whose `mode` selects the operation `[VERIFIED: vendor API reference, 2026-11-10]`
- Commands and modes: `history KEYWORD --source S` → `get_time_series` (about 260 weekly points, fields `date`, `value`, `volume` where the source has it); `growth KEYWORD --source S --window W [W...]` → `get_growth` (`percent_growth` windows such as `7D`, `3M`, `12M`, `YTD`; result per window with `growth`, `direction`, `volume_growth`); `board --type T [--limit N] [--climbers]` → `get_top_trends` (ranked board; `--climbers` sets `sort` to `rank_change`); `posts KEYWORD --source S [--days N]` → `get_context` (posts, videos, news with engagement)
- `get_reviews` is not wrapped
- Source and board names (for example `Google Search`, `Google Trends`, `News`, `YouTube`, `TikTok`, `Reddit`, `X`) are taken from the vendor data catalog `https://www.trendsmcp.ai/data-catalog` at implementation time and stored in `SETUP.md`; 54 sources in total (vendor claim)
- Billing: 1 request = 1 credit (vendor claim); `get_top_trends` costs 1 credit per 10 rows (`limit=5` charged 1 credit `[TESTED 2026-11-10, TREND-T1]`), the estimate is `ceil(limit / 10)` per board and the charged value is read from `requests_charged`; cost gate per SEOFIRST-FR-22
- Source and board names are validated against the stored catalog (updated 2026-11-06) before any request; unknown name → exit 2 listing valid names
- Known vendor issue `[TESTED 2026-11-10]`: `posts --source Reddit` returned a vendor-side status 502; `scrapecreators` `reddit-search` is the fallback
- Output shows the 0-100 `value` index and `volume` when the source returns it; the index compares momentum, absolute volume exists only where `volume` is present

**SEOFIRST-FR-21: `scrapecreators/query.py`** (credits; 100 free credits) - SEOFIRST-DD-21
- Auth: `SCRAPECREATORS_API_KEY` as `x-api-key` header; base `https://api.scrapecreators.com`
- Commands (one per documented vendor endpoint): `tiktok-popular-videos`, `tiktok-popular-songs`, `tiktok-trending-feed`, `tiktok-search KEYWORD`, `youtube-trending-shorts`, `youtube-search QUERY`, `reddit-search QUERY`, `reddit-subreddit NAME`, `pinterest-topic URL`, `instagram-search-reels QUERY`, `credit-balance` (free)
- Vendor endpoints used: `/v1/tiktok/videos/popular`, `/v1/tiktok/songs/popular`, `/v1/tiktok/get-trending-feed`, `/v1/tiktok/search/keyword`, `/v1/youtube/shorts/trending`, `/v1/youtube/search`, `/v1/reddit/search`, `/v1/reddit/subreddit`, `/v1/pinterest/topic`, `/v2/instagram/reels/search`, `/v1/credit-balance`; parameters verified by test `TREND-T2`
- Most endpoints cost 1 credit; some cost 10 or more; cache hits cost 0; per-endpoint credit table (`ENDPOINTS` constant) is stored in the script and in `SETUP.md` with access date; every response carries `credits_charged` and `credits_remaining`
- `[TESTED 2026-11-10, TREND-T2]`: `credit-balance`, `reddit-search`, `youtube-trending-shorts`, `tiktok-trending-feed`, `instagram-search-reels` (1 credit each; failed calls not charged); `tiktok-popular-videos` and `tiktok-popular-songs` returned vendor HTTP 400 (TikTok Creative Center down); parameter names of those two and of `pinterest-topic` stay `[ASSUMED]`
- X is not covered at depth by this vendor; X trends are deferred (SEOFIRST-FR-16)

**SEOFIRST-FR-22: Cost gate for credit providers**
- Applies to `trendsmcp/query.py` and `scrapecreators/query.py`
- Before every request or batch: print estimated credits and estimated USD (`credits * price_per_credit`, price per credit configurable, default from lowest-volume pack: Trends MCP `0.025`, ScrapeCreators `0.00188`, `[LITERAL: 2026-11-10]`)
- `--max-credits N` (default `20`); estimate above limit → exit 2 without request; a running batch stops when the credits actually charged reach `--max-credits`, so an endpoint that costs more than its table value cannot run away
- After the request: print remaining balance when the API returns it (ScrapeCreators `credit-balance`), else the estimate

### Linter and removals

**SEOFIRST-FR-17: `prepublish-lint.py`** (offline)
- Input: JSON file with `platform` and fields (SEOFIRST Data Structures); platforms `web`, `kdp`, `apple-books`, `google-play-books`, `kobo`, `apple-app-store`, `google-play`, `podcast`, `gbp`, `linkedin`, `youtube`
- Length checks for every field spec of the listed platforms that has a character or byte limit in `SEO_RULES.md` (characters; bytes for podcast `<description>`); field specs without a numeric limit stay manual gate items
- Set-difference checks: KDP keyword slots and Apple keywords contain no word from title, subtitle, author, categories
- 5 regexes: 1) URL, email, handle, phone in KDP/Kobo/GBP descriptions; 2) HTML tags in Apple Books description; 3) `#1`, `best of play`, `free`, `no ads`, `% off` in Google Play title and descriptions (case-insensitive); 4) spaces around commas in Apple keywords; 5) retired schema types in JSON-LD
- Additional token checks: quotes in KDP keywords, Google Play short description repeated in full description
- Output: one line per check with `GATE-*` ID, PASS/FAIL, measured value, limit; exit 1 on any FAIL
- Limit table in the script cites the `SEO-*` rule ID per limit

**SEOFIRST-FR-18: Removals**
- Delete `dataforseo/query.ps1`, `indexnow/submit.ps1`
- Remove all MCP configurations, package names, and MCP tool names from every file
- Remove Google Indexing API guidance for regular URLs; keep one restriction statement
- Remove `pytrends` and Bing SOAP/POX references
- Remove hardcoded paths (`E:\`, `C:\`, user folders)

**SEOFIRST-FR-19: Provider `SETUP.md` content**
- Account creation steps, credential key names and the line format for `[API_KEYS_FILE]`, a free verification command with expected output, pricing and limits tagged `[LITERAL: 2026-11-03]`, troubleshooting for common errors
- Section "Removal": delete the provider lines from `[API_KEYS_FILE]`, revoke or delete the key in the provider console, delete referenced credential files (SEOFIRST-DD-20)
- `google-search-console/SETUP.md` additionally documents UI-only features: Generative AI performance report, Search generative AI control, Social and Video Platform Properties, Annotations (`<= 120` chars, max 200 per property)
- `plausible/SETUP.md`: self-hosted CE $0 with Stats API; Cloud Starter €9/mo and Growth €14/mo without Stats API; Business €19/mo with Stats API (600 requests/hour)
- `indexnow/SETUP.md`: engines Bing, Yandex, Naver, Seznam, Yep; key file hosting options

## 5. Non-Functional Requirements

**SEOFIRST-NFR-01: Cost - zero by default**
- Every command except DataForSEO data commands, `trendsmcp` commands, and `scrapecreators` commands costs $0; credit provider commands use free tiers first
- Verification: SKILL.md provider registry lists cost class per command; DataForSEO commands refuse to run above `--max-cost`; credit provider commands refuse to run above `--max-credits`

**SEOFIRST-NFR-02: Security - secrets**
- No secret value appears in stdout, stderr, or JSON output
- Verification: run each script with a keys file containing marker values and grep output for the markers

**SEOFIRST-NFR-03: Portability**
- Scripts run on Windows and Linux; paths built with `pathlib`; no drive letters
- Verification: grep skill folder for `[A-Z]:\\` returns 0 hits

**SEOFIRST-NFR-04: Privacy - general-purpose content**
- Examples use `example.com`, `example.org`, generic brands; no customer data
- Verification: manual review of all examples during `/verify`

**SEOFIRST-NFR-05: Freshness - dated literals**
- Every price, quota, and platform limit carries `[LITERAL: 2026-11-03]` or an access date
- `SKILL.md` MUST-NOT-FORGET instructs re-verification of prices before paid batches when the date is older than 6 months

**SEOFIRST-NFR-06: Reliability - network**
- Timeout and retry per SEOFIRST-FR-06; non-JSON responses reported with HTTP status and first 200 characters

## 6. Design Decisions

**SEOFIRST-DD-03:** 4-file consolidated root (`SKILL.md`, `SEO_GUIDES.md`, `SEO_RULES.md`, `SEO_CHECKS.md`) plus provider folders. Rationale: user decision 2026-11-10; separates procedure, norm, and check so a rule changes in one place.

**SEOFIRST-DD-04:** No MCP; every provider is a Python script inside the skill; PowerShell scripts removed. Rationale: user decision 2026-11-10; removes dependency on third-party MCP packages (two of the previously documented packages did not exist) and on Node; one language for all scripts.

**SEOFIRST-DD-06:** Default credentials path derived from script location (`[WORKSPACE_FOLDER]/../.tools/.api-keys.txt`), override with `--keys-file`. Rationale: matches the `tools-and-skills.md` default; works from `[PROMPTSYSTEM_FOLDER]` and `[AGENT_FOLDER]` because both have the same depth; no machine path in skill files.

**SEOFIRST-DD-09:** Credential key names are standardized as `[PROVIDER]_[QUALIFIER_][SUFFIX]` and registered in one place, `SKILL.md` section "Credential Keys". Provider prefixes (one per provider folder): `DATAFORSEO`, `GSC`, `BING_WEBMASTER`, `INDEXNOW`, `PLAUSIBLE`, `YOUTUBE`, `TRENDSMCP`, `SCRAPECREATORS`. Qualifier (optional, names what the credential belongs to): currently only `SERVICE_ACCOUNT`. Suffixes (closed set): `API_KEY`, `LOGIN`, `PASSWORD`, `BASE_URL`, `FILE` (`FILE` values are file names relative to the `[API_KEYS_FILE]` folder). Names already present in the user's keys file keep their spelling; `INDEXNOW_KEY` becomes `INDEXNOW_API_KEY`; `DATAFORSEO_BASE64` is dropped because it duplicates login and password. Rationale: user decision 2026-11-10; one registry prevents name drift between scripts, `SETUP.md` files, and the keys file.

**SEOFIRST-DD-10:** Self-contained scripts without a shared helper module. Rationale: provider folders stay independently copyable; avoids `sys.path` manipulation; cost is about 40 duplicated lines (key loading, HTTP retry, output) per script.

**SEOFIRST-DD-11:** Skill rule IDs `SEO-[DOMAIN]-[NN]` keep the research domain and number. Rationale: the skill is general-purpose and must not reference private research IDs; identical numbering keeps traceability for maintainers.

**SEOFIRST-DD-12:** GSC derived analyses (`quick-wins`, `ctr-gap`, `decay`, `cannibalization`) are computed in the script from Search Analytics rows. Rationale: replaces the MCP "extended tools" without dependency; thresholds stay identical to `SEO_CHECKS.md`.

**SEOFIRST-DD-13:** `ctr-gap` uses the site's own CTR baseline: expected CTR for a position bucket = median CTR of the site's pages in that bucket over the same 90 days (buckets 1.0-1.9, 2.0-2.9, 3.0-3.9, 4.0-5.9, 6.0-10.9). Rationale: no published position-CTR curve is evidence-grade for every site; a self-baseline needs no external data.

**SEOFIRST-DD-14:** Agent readiness is checked by a local HTTP probe script instead of the `isitagentready.com` MCP. Rationale: SEOFIRST-DD-04; checks are plain HTTP requests against documented paths and headers.

**SEOFIRST-DD-15:** Google Ads `KeywordPlanIdeaService` and Google Trends API alpha are deferred (SEOFIRST-FR-16). Rationale: both need gated access (Ads developer token, alpha allowlist); DataForSEO `search-volume` and the Trends web UI cover the questions until access exists.

**SEOFIRST-DD-16:** Cost gate default `--max-cost 0.10` USD per command. Rationale: covers a single SERP ($0.002), a 100-item Labs call (~$0.024), one search-volume task ($0.09 Live), one backlinks summary (~$0.024); larger batches require an explicit decision.

**SEOFIRST-DD-17:** Folklore lives in a Do-Not-Do list in `SEO_GUIDES.md` without rule IDs. Rationale: rule IDs signal norms; negative-evidence practices must stay visible as warnings without looking like requirements.

**SEOFIRST-DD-18:** `prepublish-lint.py` holds its own limit table with `SEO-*` rule references; `SEO_RULES.md` is the source of truth. Rationale: the linter runs offline without parsing Markdown; a test compares both tables.

**SEOFIRST-DD-19:** Default DataForSEO location `2840` (United States), language `en`. Rationale: neutral default for a general-purpose skill (previous default `2276` was project-specific).

**SEOFIRST-DD-20:** No `UNINSTALL.md` files; each provider `SETUP.md` has a "Removal" section instead. Rationale: `AGENT-SKILL-RULES.md` requires `UNINSTALL.md` when `SETUP.md` installs software or changes agent configuration; these `SETUP.md` files only create provider accounts and add lines to `[API_KEYS_FILE]`, so removal is 3 steps and 6 extra files would contradict the few-files rule.

**SEOFIRST-DD-21:** Trend and social discovery uses two credit providers behind Python scripts: `trendsmcp` for cross-platform trend index and live boards, `scrapecreators` for post-level social data; DataForSEO stays the Google provider. No MCP (SEOFIRST-DD-04). Rationale: user decision 2026-11-10 (option 1 of the provider comparison); no single provider covers Google, X, YouTube, TikTok, and Reddit at depth, DataForSEO retired its Social Media API on 2026-09-16, both vendors sell credits that never expire without a required subscription; trend-index calls cost about 10x raw social calls, so trend discovery runs first and depth calls only on top candidates. Free-first order is unchanged (free sources, then trend index, then depth).

## 7. Implementation Guarantees

**SEOFIRST-IG-01:** No file in `seo-tools/` contains a drive-letter path, `npx`, `uvx`, `mcpServers`, `.ps1`, `submit_url`, or `pytrends`.

**SEOFIRST-IG-02:** No paid request is sent without a printed estimate `<= --max-cost` (DataForSEO) or `<= --max-credits` (credit providers).

**SEOFIRST-IG-03:** Every script prints help with exit 0 when run with `--help`, without keys file and without network.

**SEOFIRST-IG-04:** Every `SEO-*` rule in `SEO_RULES.md` has an evidence label and at least one source URL with access date; exception: `SEO-TLS-10` is `[ASSUMED]` with "Sources: none" (internal convention without external source).

**SEOFIRST-IG-05:** Every rule ID referenced in `SKILL.md`, `SEO_GUIDES.md`, `SEO_CHECKS.md`, and `prepublish-lint.py` exists in `SEO_RULES.md`.

**SEOFIRST-IG-06:** No secret value from `[API_KEYS_FILE]` appears in any script output; the IndexNow key is masked to its first 4 characters.

**SEOFIRST-IG-07:** Google Indexing API appears only together with the `JobPosting` / `BroadcastEvent` restriction.

**SEOFIRST-IG-08:** DataForSEO prices in `query.py`, `ENDPOINTS.md`, `SKILL.md`, and `SEO_RULES.md` are identical.

**SEOFIRST-IG-09:** The set of credential key names read by the scripts equals the set registered in `SKILL.md` section "Credential Keys", and every name in `SETUP.md` files is in that set.

## 8. Key Mechanisms

**Free-first escalation:** For each question type, the router names a $0 source first; the paid fallback is used only when the free source cannot answer (unowned competitor data, keyword difficulty, third-party backlinks, bulk SERPs above 10 queries, third-party LLM panels).

**Cost estimate:** `estimate = Σ tasks * task_price + Σ items * item_price`; items = `--limit` for Labs, expected rows for Backlinks; search-volume tasks = `ceil(keywords / 1,000)`; board rows = `ceil(limit / 10)` credits.

**Credential loading:** Parse keys file once; return dict; lookup with explicit error naming the key; DataForSEO Basic auth built from `DATAFORSEO_LOGIN` and `DATAFORSEO_PASSWORD`.

**GSC date windows:** Data lag 3 days; `decay` compares the last full 3 months with the same months one year earlier (within GSC 16-month retention); clicks are the anchor metric for comparisons involving May-September 2025 (impression logging anomaly).

**Set-difference packing check:** `used = tokens(title ∪ subtitle ∪ author ∪ categories)`; any keyword-slot token in `used` → FAIL with the offending tokens; tokens lowercased, punctuation stripped; Apple plurals compared by trailing `s` removal.

**Decay signature classification (agent-applied from `decay` output):** Signature 1 ranking decay (clicks down, impressions down, position worse `>= 2.0`) → REFRESH; Signature 2 zero-click capture (clicks down, impressions flat or up, position flat or better, AI Overview present) → RE-FORMAT or stop; Signature 3 intent drift (SERP format changed) → RE-FORMAT; Signature 4 demand decay (clicks and impressions down, position flat, Trends down) → CONSOLIDATE or PRUNE.

**Agent readiness probes:** Sequential HTTP GETs with `Accept` header variants; checks status code, `Content-Type`, `Vary`, and minimal body structure (robots directives, YAML frontmatter start, JSON parse for well-known files).

## 9. Action Flow

```
Agent receives SEO-relevant task
├─> Read SKILL.md
│   ├─> Lifecycle router → stage IDEATE | CREATE | PUBLISH | IMPROVE | RESEARCH | MONITOR
│   │   └─> Read SEO_GUIDES.md section of that stage
│   │       ├─> Apply SEO_RULES.md rules referenced by each step
│   │       └─> Needs data? → When-to-Query-What matrix
│   │           ├─> Free source → run script (gsc, bing, youtube, agent-readiness, plausible)
│   │           ├─> Trend discovery → trendsmcp/query.py (credit gate) → scrapecreators/query.py for top candidates
│   │           └─> Paid needed → dataforseo/query.py balance
│   │               └─> dataforseo/query.py CMD --max-cost N
│   │                   ├─> Estimate <= N → request → print actual cost
│   │                   └─> Estimate > N → exit 2, agent reports estimate to user
│   └─> Stage PUBLISH
│       ├─> prepublish-lint.py metadata.json → FAIL? fix fields, re-run
│       ├─> agent-readiness/check.py URL → FAIL? fix, re-run
│       ├─> Manual GATE-* items from SEO_CHECKS.md
│       └─> All PASS → indexnow/submit.py + sitemap <lastmod> + GSC annotation
```

## 10. Data Structures

**`[API_KEYS_FILE]` lines (placeholder values):**
```
DATAFORSEO_LOGIN=user@example.com
DATAFORSEO_PASSWORD=0000000000000000
GSC_SERVICE_ACCOUNT_FILE=gsc-service-account.json
BING_WEBMASTER_API_KEY=00000000000000000000000000000000
INDEXNOW_API_KEY=0123456789abcdef0123456789abcdef
PLAUSIBLE_API_KEY=placeholder-token
PLAUSIBLE_BASE_URL=https://plausible.io
YOUTUBE_API_KEY=placeholder-key
TRENDSMCP_API_KEY=placeholder-key
SCRAPECREATORS_API_KEY=placeholder-key
```

**Script JSON output envelope (`--format json`):**
```json
{"script": "dataforseo", "command": "serp", "ok": true, "estimated_cost_usd": 0.002, "actual_cost_usd": 0.002, "params": {"keyword": "example query", "location": 2840, "lang": "en"}, "rows": [{"position": 1, "domain": "example.org", "title": "Example title"}], "notes": ["AI Overview present"]}
```

**`prepublish-lint.py` input:**
```json
{"platform": "apple-app-store", "fields": {"name": "Example: Task Planner", "subtitle": "Plan Projects Offline", "keywords": "todo,checklist,kanban,schedule", "promotional_text": "Plan weekly work in minutes."}, "context": {"categories": ["Productivity"], "developer": "Example Studio"}}
```

**`prepublish-lint.py` output (table format):**
```
Linting 'metadata.json' (platform 'apple-app-store')...
  GATE-APP-01  name                  PASS  22 / 30 chars
  GATE-APP-01  subtitle              PASS  21 / 30 chars
  GATE-APP-01  keywords length       PASS  30 / 100 chars
  GATE-APP-01  keywords comma space  PASS
  GATE-APP-01  keywords set-diff     FAIL  repeated tokens: planner
  GATE-APP-01  promotional_text      PASS  28 / 170 chars
FAIL: 5 checks passed, 1 failed.
```

## 11. Logging Requirements

**Applicable logging types:**
- [x] User-Facing (UF) - `LOGGING-RULES-USER-FACING.md`
- [ ] App-Level (AP) - not a service
- [ ] Script-Level (SC) - test harness lives in the session folder, not in the skill

**User-Facing logging:**
- **Audience**: The agent reading CLI output; the user reviewing the chat transcript
- **Goal**: Know which request ran, what it cost, how many rows came back, and why a run stopped
- **Key operations**: credential loading, cost estimate, HTTP request, pagination, result summary, gate result

**Expected output for a paid DataForSEO call:**
```
Estimating cost for 'keywords' (1 task, 30 items)...
  Estimate: $0.0156 (limit $0.10).
Querying 'dataforseo_labs/google/keyword_suggestions/live'...
  30 rows received.
  Actual cost: $0.0156.
OK.
```

**Expected output when the cost gate blocks:**
```
Estimating cost for 'search-volume' (2 tasks, 1,500 keywords)...
  Estimate: $0.18 (limit $0.10).
ERROR: Estimate exceeds limit -> rerun with --max-cost 0.18 to allow.
```

**Expected output for a credit provider call:**
```
Estimating credits for 'growth' (1 request, 2 windows)...
  Estimate: 1 credit, about $0.0166 (limit 20 credits).
Querying 'POST https://api.trendsmcp.ai/api' (mode 'get_growth')...
  2 windows received.
  Charged: 1 credit.
OK.
```

**Expected output when the credit gate blocks:**
```
Estimating credits for 'tiktok-search' (30 requests)...
  Estimate: 30 credits, about $0.056 (limit 20 credits).
ERROR: Estimate exceeds limit -> rerun with --max-credits 30 to allow.
```

**Expected output for a missing key:**
```
ERROR: Key 'BING_WEBMASTER_API_KEY' not found in '[API_KEYS_FILE]' -> see 'bing-webmaster/SETUP.md'.
```

## 12. Technical Constraints

- Shared venv `[SKILL_TOOLS_FOLDER]/llm-venv/` provides `requests` and `google-auth` (verified 2026-11-10); no new packages required
- GSC: Search Analytics `<= 25,000` rows per request, 16-month retention, 2-3 day lag; URL Inspection 2,000/day and 600/minute per property; service account must be added as user to the property
- Bing Webmaster: SOAP and POX endpoints retired 2026-08-31; JSON endpoint only; AI Performance has no API
- IndexNow: `<= 10,000` URLs per POST; key 8-128 characters `[a-zA-Z0-9-]`; key file reachable over HTTPS
- YouTube Data API: 10,000 units/day default; max 100 `search.list` calls per day (documentation shows 100 units per call or a separate 100-call bucket); `videos.list` 1 unit
- Trends MCP (REST): free 100 requests/month; credit packs 600 / 2,500 / 12,000 at 2.5 / 1.96 / 1.66 cents per credit, credits never expire, failed calls free `[LITERAL: 2026-11-10]`
- ScrapeCreators: 100 free credits; packs 25,000 credits `$47` and 500,000 credits `$497`, credits never expire, cache hit 0 credits `[LITERAL: 2026-11-10]`
- DataForSEO: account verification required for data endpoints; balance endpoint works unverified; `$50` minimum top-up; Keywords Data Live `$0.09`/task, Standard `$0.06`/task, up to 1,000 keywords per task, Live 12 requests per minute `[LITERAL: 2026-11-10]`
- Plausible Stats API: 600 requests/hour; API key scoped to owning team
- Google Indexing API: only `JobPosting` and `BroadcastEvent` in `VideoObject`; 200 URLs/day
- Sync: `[PROMPTSYSTEM_FOLDER]` → `[AGENT_FOLDER]` by robocopy; `.claude/` regeneration via `_PROMPTS_UpdateClaude.md` is a separate step outside this spec

## 13. Document History

**[2026-11-10 21:30]**
- Fixed: reverse sync from implementation and live tests - Keywords Data Live $0.09/task and 1,000 keywords per task (PR-0010), YouTube quota wording, 54 field entries for 72 fields, `SEO-TLS-10` exception, cumulative site types, IndexNow key masking (PR-0013)
- Changed: FR-20 board billing 1 credit per 10 rows and source name validation, FR-21 tested endpoints and vendor outages, FR-22 running-batch stop

**[2026-11-10 20:25]**
- Fixed: `/verify` - FR order (FR-16 before FR-20), FR-20 rewritten to the verified Trends MCP REST contract (single endpoint, `mode` values, `requests_charged`), DD-09 prefix list, Context decision IDs and acronyms, matrix trend order, action flow, credit gate log examples

**[2026-11-10 20:15]**
- Added: SEOFIRST-DD-21 (user decision: Trends MCP + ScrapeCreators + DataForSEO, Python scripts, no MCP), SEOFIRST-FR-20..22, credential keys `TRENDSMCP_API_KEY` and `SCRAPECREATORS_API_KEY`, folders `trendsmcp/` and `scrapecreators/`, `credits` cost class
- Changed: SEOFIRST-FR-16 (X trends and AIsa deferred), NFR-01, IG-02, technical constraints

**[2026-11-10 19:45]**
- Changed: `/verify` - SPEC design decisions renumbered to match session decision IDs (DD-03, DD-04, DD-06, DD-09 = user decisions; engineering decisions DD-10..DD-20); DD-14 naming standard is now DD-09
- Changed: Lifecycle stage labels `[A]..[M]` replaced by decodable names `IDEATE`..`MONITOR`
- Changed: DD-09 name format `[PROVIDER]_[QUALIFIER_][SUFFIX]` covers `GSC_SERVICE_ACCOUNT_FILE`
- Added: SKILL.md required sections (When to use, Architecture, Limitations, Sources), skill resource file format rules (Rule Index, BAD/GOOD, no bold, check items with evidence), DD-20 Removal sections instead of `UNINSTALL.md`
- Fixed: claim audit count (9 wrong + 4 outdated of 28), 97 vs 101 rule count explained, ctr-gap baseline defined on pages, competitors price, WebMCP check, sitemap submit permission, linter scope, acronyms

**[2026-11-10 19:35]**
- Added: SEOFIRST-DD-14 credential key naming standard, SEOFIRST-IG-09, "Credential Keys" registry in `SKILL.md` (FR-02, FR-07)
- Changed: `INDEXNOW_KEY` renamed to `INDEXNOW_API_KEY`; `DATAFORSEO_BASE64` removed from the standard
- Changed: `GSC_SERVICE_ACCOUNT_FILE` documented as file name relative to the `[API_KEYS_FILE]` folder

**[2026-11-10 19:20]**
- Initial specification created from research `SEOFIRST-SEOGUIDE-IN12` and user decisions DD-03..DD-08 of 2026-11-10
