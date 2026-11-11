---
name: seo-tools
description: SEO-first working skill for ideation, content and media creation, metadata generation, pre-publish gate, audit and decay triage, campaigns, monitoring, agent discoverability, and SEO data queries. Apply when planning, writing, publishing, or improving any web page, article, document, book, app, video, podcast, social post, or local listing for search engines and AI answer engines, or when querying GSC, Bing Webmaster, IndexNow, DataForSEO, YouTube, Plausible, cross-platform trend, or social post data.
compatibility: Python 3.10+ (requests; google-auth for GSC). Windows and Linux. No MCP servers.
---

# SEO Tools

Router for SEO-first work. Procedures: `SEO_GUIDES.md`. Rules and platform limits: `SEO_RULES.md`. Gates, audit, scoring, alerts: `SEO_CHECKS.md`. Data: Python scripts in provider folders.

## MUST-NOT-FORGET

- Tier protocol: every data question starts with Tier 1 (free), then enriches and verifies with Tier 2 (prepaid), then probes Tier 3 (subscription) and enriches and verifies again; use several sources per claim and report agreement (section "Source Tiers", SEO-TLS-01, SEO-TLS-11)
- Paid DataForSEO calls: run `dataforseo/query.py balance` first; every paid command prints an estimate and aborts above `--max-cost` (default $0.10); never raise the limit without a stated reason (SEO-TLS-05)
- Credit providers (`trendsmcp`, `scrapecreators`): every command prints a credit estimate and aborts above `--max-credits` (default 20); use free tiers first; discover with one `trendsmcp` call, go deep with `scrapecreators` only on the top candidates
- Prices and limits are [LITERAL: 2026-11-03] (trend and social providers [LITERAL: 2026-11-10]); re-verify at the source before paid batches when that date is older than 6 months
- Google Indexing API only for `JobPosting` or `BroadcastEvent` pages; regular URLs: IndexNow + sitemap `<lastmod>` + URL Inspection (SEO-TLS-02)
- Run the pre-publish gate (`SEO_CHECKS.md` section 2, `prepublish-lint.py`) before anything goes live
- Credentials only from `[API_KEYS_FILE]` with the names in section "Credential Keys"; never print secret values
- Label recommendations [VERIFIED], [ASSUMED], or [COMMUNITY]; never recommend items of the Do-Not-Do list in `SEO_GUIDES.md`

## When to Use

- Planning what to build or write (demand, clustering, naming)
- Writing or structuring web pages, articles, PDFs, docs, images, books, videos, podcasts, social posts, apps, local listings, print media
- Generating and validating metadata before publishing
- Diagnosing traffic or AI citation drops, ranking fixes, planning campaigns, setting up monitoring
- Making a site readable for AI agents (robots.txt, Markdown, llms.txt, well-known endpoints)
- Answering SEO data questions with GSC, Bing, YouTube, IndexNow, Plausible, DataForSEO
- Finding trends and breakout topics across Google, YouTube, TikTok, Reddit, Pinterest, and more

## When Not to Use

- Paid ads campaign management (bids, budgets, ad copy)
- General web analytics questions without search or discoverability intent
- Legal review of claims, trademarks, or privacy compliance (the skill flags risks, it does not give legal advice)

## Architecture

```
SKILL.md (router, matrix, credentials)
├─> SEO_GUIDES.md  procedures per stage ─┬─> SEO_RULES.md   SEO-* rules + field limits
│                                        └─> SEO_CHECKS.md  gate, audit, MOS, decay, alerts
└─> scripts (Python, [API_KEYS_FILE])
    ├─> tiers.py                        tier probe $0; run flows     paid steps, budget
    ├─> prepublish-lint.py              offline metadata gate        $0
    ├─> agent-readiness/check.py        HTTP probes of a site        $0
    ├─> google-search-console/query.py  Search Analytics, Inspection $0
    ├─> bing-webmaster/query.py         Bing Webmaster JSON API      $0
    ├─> indexnow/submit.py              IndexNow push                $0
    ├─> youtube/query.py                YouTube Data API v3          $0 (quota)
    ├─> plausible/query.py              Plausible Stats API v2       $0 CE / Business plan
    ├─> trendsmcp/query.py              cross-platform trend index   credits (100 free per month)
    ├─> scrapecreators/query.py         social post-level data       credits (100 free)
    └─> dataforseo/query.py             DataForSEO v3, cost gate     paid
```

## Lifecycle Router

Pick the stage, then follow the section in `SEO_GUIDES.md`.
- IDEATE: before building a product, book, course, app, video, podcast, or new page -> demand validation, SERP-overlap clustering, intent and shape, naming gates
- CREATE: while drafting or architecting an asset -> web foundation, media playbooks, agent readiness by site type, entity and brand memory, localization
- PUBLISH: before and after go-live -> metadata pipeline, gate, post-publish push
- IMPROVE: every 4-6 weeks, after an alert, on a drop, for campaigns -> audit cycle, AI visibility gap, competitor gap, 9 campaign templates
- RESEARCH: any step needs data -> matrix below, cost discipline
- MONITOR: scheduled runs -> 6 alerts in `SEO_CHECKS.md` section 8

## Source Tiers

Tiers by cost model: Tier 1 FREE ($0 marginal: first-party APIs, free quotas, offline checks, manual UI sources), Tier 2 PREPAID (credits or balance behind a cost gate: `trendsmcp`, `scrapecreators`, `dataforseo`), Tier 3 SUBSCRIPTION (flat-fee tools: Ahrefs, Semrush; usually not available; no script). Tier of each provider: section "Provider Registry".

Protocol for every data question (SEO-TLS-11):
1. Probe: run `python tiers.py probe` once per task ($0; `--balances` adds the ScrapeCreators and DataForSEO balances); a tier with no usable provider is skipped and recorded as "Tier N unavailable"
2. Tier 1 collect: run every Tier 1 source of the matrix row that a script can run; Tier 1 sources without a script (Google Trends UI, Pinterest Trends, autocomplete UI, GSC and Bing UI reports) go into the ledger as "not run (manual)" and are named to the user, never counted as a source
3. Tier 2 enrich and verify: matrix rows 2, 3, 4 run as one command, `python tiers.py run keywords|serp|competitors TARGET` (default budget `--max-usd 0.15` [ASSUMED]); it runs cheap to expensive, checks each result before the next step uses it, and prints a step ledger and claim labels. Other rows: call the provider scripts in the same order: suggestion and SERP calls find candidates, one batched volume call sizes all of them, per-domain calls run only on discovered competitor domains, never on the domain the user asked about; cost gates stay on (`--max-credits`, `--max-cost`); owned-data rows stay at Tier 1
4. Term level: suggestions are candidates until a volume call confirms them; when a provider returns sparse data (fewer than 5 suggestion rows, null index), retry once with the head term and label the result "head-term proxy"; a head term never stands for the long-tail term
5. Tier 3 probe, enrich, verify: if the probe shows a Tier 3 key, state the estimated vendor units, call the vendor REST API for the same claims, and compare with Tiers 1 and 2; no key: skip, never block the answer
6. Ledger: per claim type (existence, size, trend, supply, competitors) list tier, source, date, cost, and one agreement label; CONFIRMED (2 or more different providers agree on direction and order of magnitude), CONFLICT (providers disagree: report both values and the likely cause, never average), SINGLE-SOURCE (only one provider answered; "by design" when only one provider can measure the claim, e.g. Google volume); evidence for these rules: SEO-TLS-11
7. Stop early only when the user asks for a tier cap ("free only"), a balance is zero (mark that tier unavailable), or a gate aborts; say which

## When-to-Query-What Matrix

Question -> T1 free sources (run all) -> T2 prepaid (enrich and verify) -> T3 subscription (probe, then enrich and verify when a key exists). Protocol: section "Source Tiers".
1. Demand trajectory (growing, seasonal, declining) and trend discovery -> T1: Google Trends UI with anchor term (manual), Pinterest Trends (manual), `youtube/query.py search` -> T2: one cross-platform call `trendsmcp/query.py growth|board|history KEYWORD`, then depth on the top 1-2 candidates `scrapecreators/query.py tiktok-search|youtube-search|reddit-search|pinterest-topic`; Google volume check: DataForSEO Trends via `dataforseo/ENDPOINTS.md` ($0.0012/task, manual call) -> T3: keyword overview and trend of the vendor
2. Keyword sizing and ideas -> T1: autocomplete (manual), `google-search-console/query.py analytics SITE --dimensions query` (owned site), `youtube/query.py search QUERY` -> T2: `tiers.py run keywords SEED` (TikTok and YouTube suggestions -> one `dataforseo search-volume` call over all candidates; flags other-region and head-term-proxy rows; about $0.10); alternative seed expansion: `dataforseo/query.py keywords SEED` -> T3: keyword volume and difficulty of the vendor
3. SERP overlap and features (clustering, AI Overview presence) -> T1: browser check of top-10 (manual, few queries) -> T2: `tiers.py run serp KEYWORD` (`scrapecreators google-search` + `dataforseo serp`; recurring hosts, AI Overview, feature types; CONFIRMED when 2 or more hosts recur; about $0.004); a SERP is a sample: compare by result type and recurring hosts, never by exact rank; > 10 queries: task_post pattern in `dataforseo/ENDPOINTS.md` -> T3: SERP overview of the vendor
4. Competitor gap -> T1: `bing-webmaster/query.py query-stats SITE` (owned site only), Bing AI Performance grounding queries (UI), `youtube/query.py search "X alternatives"` (run by `tiers.py run competitors`) -> T2: `tiers.py run competitors DOMAIN [--brand NAME] [--ads 2]` (3 Google SERPs "X alternatives", "X competitors", "X vs" -> hosts in 2 of 3 form the competitor set; `dataforseo competitors` only confirms it; `google-ads` on the top competitors, grouped by advertiser; about $0.03); ad copy needs `scrapecreators/query.py google-ads DOMAIN --param get_ad_details=true` (25 credits) -> T3: organic competitors of the vendor
5. Technical and agent readiness -> T1: `agent-readiness/check.py URL --site-type A|B|C|D`, `google-search-console/query.py inspect SITE URL` -> T2: none needed -> T3: none needed
6. Owned ranking, CTR gap, decay, cannibalization -> T1: `google-search-console/query.py quick-wins|ctr-gap|decay|cannibalization SITE`, `bing-webmaster/query.py page-stats SITE` -> T2: none needed -> T3: none needed
7. Backlinks -> T1: GSC Links report (UI), `bing-webmaster/query.py links SITE` -> T2: `dataforseo/query.py backlinks DOMAIN` -> T3: backlink index of the vendor
8. AI citation and brand visibility -> T1: GSC Generative AI report (UI), Bing AI Performance (UI), own prompt panel with >= 8 runs per prompt -> T2: DataForSEO AI Optimization endpoints (manual, after estimate) -> T3: AI visibility tracker of the vendor
9. Conversion by page and source -> T1: `plausible/query.py goals SITE`, `sources SITE` -> T2: none needed -> T3: none needed
10. Indexing push -> T1: `indexnow/submit.py submit URL... --host HOST`, sitemap `<lastmod>`, `google-search-console/query.py sitemaps SITE --submit URL` -> T2: none needed -> T3: none needed

## Intent Lookup

- "Is there demand for X?" -> `SEO_GUIDES.md` IDEATE demand validation; matrix rows 1-2
- "What is trending right now?" -> `python trendsmcp/query.py board --type "Google Trends" --limit 10`; climbers: `board --type "TikTok Trending Hashtags" --climbers`
- "Is topic X growing on platform Y?" -> `python trendsmcp/query.py growth "X" --source TikTok --window 7D 3M 12M`
- "What do people post about X?" -> `python scrapecreators/query.py reddit-search "X" --timeframe month --sort top`; `tiktok-search`, `youtube-search`
- "What do people type into TikTok or YouTube search for X?" -> `python scrapecreators/query.py tiktok-suggestions "X"`; `youtube-typeahead "X"` (long phrases can return few rows: retry with the head term)
- "What ranks on Google for X (titles, URLs, descriptions only)?" -> `python scrapecreators/query.py google-search "X" --region US`; SERP features and AI Overview: `dataforseo/query.py serp`
- "What ads does competitor Y run on Google?" -> `python scrapecreators/query.py google-ads Y.com`
- "Who competes with X?" -> `python tiers.py run competitors x.com`
- "Which keywords should a page about X target?" -> `python tiers.py run keywords "X"`
- "Who ranks for X and is there an AI Overview?" -> `python tiers.py run serp "X"`
- "What does this YouTube video say?" -> `python scrapecreators/query.py youtube-transcript "URL" --cache-max-age 30d --format json`
- "Which keywords go on one page?" -> IDEATE SERP-overlap clustering; `dataforseo/query.py serp`
- "Name this product/book/app" -> IDEATE naming gates
- "Write or structure this page/asset" -> CREATE web foundation + media playbook
- "Check metadata before publishing" -> `python prepublish-lint.py payload.json` + `SEO_CHECKS.md` section 2
- "Is the site ready for AI agents?" -> `python agent-readiness/check.py https://example.com/ --site-type A`
- "Why did traffic drop?" -> IMPROVE audit cycle; `python google-search-console/query.py decay sc-domain:example.com`
- "Which pages should get new titles?" -> `python google-search-console/query.py ctr-gap sc-domain:example.com`
- "Which pages compete with each other?" -> `python google-search-console/query.py cannibalization sc-domain:example.com`
- "Quick wins?" -> `python google-search-console/query.py quick-wins sc-domain:example.com`
- "Tell search engines about new URLs" -> `python indexnow/submit.py submit https://example.com/new --host example.com`
- "Who are our search competitors?" -> IMPROVE competitor gap; `python tiers.py run competitors example.com`
- "Plan a launch or campaign" -> IMPROVE campaign templates
- "How much budget is left?" -> `python dataforseo/query.py balance`

## Provider Registry

Credentials: see section "Credential Keys" (names are not repeated here).
- `tiers.py` - Tier probe ($0) and run flows (Tier 1 + Tier 2, budget `--max-usd`) - `probe [--balances]`, `run keywords|serp|competitors TARGET` - no setup
- `prepublish-lint.py` - Tier 1, offline - payload format in `--help` - no setup
- `agent-readiness/check.py` - Tier 1 - `URL --site-type A|B|C|D` (no subcommand; exit 1 when a check fails) (A content site, B docs, C ecommerce, D API platform) - no setup
- `google-search-console/query.py` - Tier 1 - `sites`, `analytics`, `inspect`, `sitemaps`, `quick-wins`, `ctr-gap`, `decay`, `cannibalization` - `google-search-console/SETUP.md`
- `bing-webmaster/query.py` - Tier 1 - `sites`, `query-stats`, `page-stats`, `traffic`, `links`, `quota`, `submit` - `bing-webmaster/SETUP.md`
- `indexnow/submit.py` - Tier 1 - `submit`, `verify-key` - `indexnow/SETUP.md`
- `youtube/query.py` - Tier 1, free with quota (max 100 searches per day, 10,000 units per day) - `search`, `videos` - `youtube/SETUP.md`
- `plausible/query.py` - Tier 1 (owned data), free self-hosted CE or Cloud Business plan - `summary`, `top-pages`, `sources`, `goals`, `raw` - `plausible/SETUP.md`
- `trendsmcp/query.py` - Tier 2, credits, 100 free requests per month, REST only - `history`, `growth`, `board`, `posts` - `trendsmcp/SETUP.md`
- `scrapecreators/query.py` - Tier 2, credits, 100 free credits - `google-search`, `tiktok-suggestions`, `youtube-typeahead`, `google-ads`, `youtube-transcript`, `tiktok-popular-videos` and `tiktok-popular-songs` (vendor-side outage on 2026-11-10 and 2026-11-11), `tiktok-trending-feed`, `tiktok-search`, `youtube-trending-shorts`, `youtube-search`, `reddit-search`, `reddit-subreddit`, `pinterest-topic`, `instagram-search-reels`, `credit-balance` ($0) - `scrapecreators/SETUP.md`
- `dataforseo/query.py` - Tier 2, prepaid balance with cost gate - `balance` ($0), `keywords`, `search-volume`, `serp`, `competitors`, `backlinks` - `dataforseo/SETUP.md`, prices `dataforseo/ENDPOINTS.md`
- Ahrefs, Semrush - Tier 3, subscription, no script; presence probed by `tiers.py probe` through `AHREFS_API_KEY` and `SEMRUSH_API_KEY`; usage: section "Source Tiers" step 5

DataForSEO prices [LITERAL: 2026-11-03]: SERP Standard $0.0006/SERP, SERP Live $0.002/SERP; Labs $0.012/task + $0.00012/item; Keywords Data Standard $0.06/task, Live $0.09/task (up to 1,000 keywords; `query.py` uses Live); Backlinks $0.024/task + $0.000036/row.

Trend and social provider prices [LITERAL: 2026-11-10]: Trends MCP free 100 requests per month, then credits $15 per 600 (2.5 cents), $49 per 2,500 (1.96 cents), $199 per 12,000 (1.66 cents), credits never expire, 1 credit per request and per 10 board rows; ScrapeCreators 100 free credits, then $47 per 25,000 credits ($1.88 per 1,000) or $497 per 500,000 ($0.99 per 1,000), most endpoints 1 credit, credits never expire. Credit scripts use `--max-credits N` (default 20) and `--credit-price USD`.

Common script contract:
- Run with the shared venv: `[SKILL_TOOLS_FOLDER]/llm-venv/Scripts/python.exe <script> ...`
- `--help` works without credentials and network
- `--keys-file PATH` overrides the default `[WORKSPACE_FOLDER]/../.tools/.api-keys.txt` (resolved from the script location)
- `--format table|json`; results on stdout, progress and errors on stderr
- Exit codes: 0 success, 1 API or request error (or gate FAIL), 2 usage or precondition error (missing key, cost gate, invalid input)
- Retries HTTP 429 and 5xx 3 times (1 s, 2 s, 4 s); timeout 30 s

## Credential Keys

Single registry of credential names in `[API_KEYS_FILE]` (`KEY=VALUE` lines, `#` comments allowed). Scripts and `SETUP.md` files use exactly these names.

Name format: `[PROVIDER]_[QUALIFIER_][SUFFIX]`
- Provider prefixes: `DATAFORSEO`, `GSC`, `BING_WEBMASTER`, `INDEXNOW`, `PLAUSIBLE`, `YOUTUBE`, `TRENDSMCP`, `SCRAPECREATORS`, `AHREFS`, `SEMRUSH`
- Qualifier (optional): `SERVICE_ACCOUNT`
- Suffixes: `API_KEY`, `LOGIN`, `PASSWORD`, `BASE_URL`, `FILE` (`FILE` = file name relative to the `[API_KEYS_FILE]` folder; no absolute paths)

Keys:
- `DATAFORSEO_LOGIN` - required by `dataforseo/query.py` - API login (registration email) - `dataforseo/SETUP.md`
- `DATAFORSEO_PASSWORD` - required by `dataforseo/query.py` - API password (not the account password) - `dataforseo/SETUP.md`
- `GSC_SERVICE_ACCOUNT_FILE` - required by `google-search-console/query.py` - service account JSON file name, stored next to `[API_KEYS_FILE]` - `google-search-console/SETUP.md`
- `BING_WEBMASTER_API_KEY` - required by `bing-webmaster/query.py` - API key from Bing Webmaster Tools settings - `bing-webmaster/SETUP.md`
- `INDEXNOW_API_KEY` - optional for `indexnow/submit.py` (`--key` overrides) - 8-128 chars `[a-zA-Z0-9-]`, one per site - `indexnow/SETUP.md`
- `PLAUSIBLE_API_KEY` - required by `plausible/query.py` - Stats API key - `plausible/SETUP.md`
- `PLAUSIBLE_BASE_URL` - optional for `plausible/query.py` - default `https://plausible.io`; self-hosted instance URL - `plausible/SETUP.md`
- `YOUTUBE_API_KEY` - required by `youtube/query.py` - Google Cloud API key restricted to YouTube Data API v3 - `youtube/SETUP.md`
- `TRENDSMCP_API_KEY` - required by `trendsmcp/query.py` - REST API key from the account dashboard (the vendor name contains "MCP"; the skill uses REST only) - `trendsmcp/SETUP.md`
- `SCRAPECREATORS_API_KEY` - required by `scrapecreators/query.py` - API key from the dashboard, sent as `x-api-key` header - `scrapecreators/SETUP.md`
- `AHREFS_API_KEY` - optional, read by `tiers.py probe` only (no script) - Tier 3 availability marker; vendor API token from a plan with API access
- `SEMRUSH_API_KEY` - optional, read by `tiers.py probe` only (no script) - Tier 3 availability marker; vendor API key from a plan with API access

Legacy: a `DATAFORSEO_BASE64` line is ignored (Basic auth is built from login and password).

## Limitations

- UI-only data without API: GSC Generative AI performance report, Search generative AI control, GSC social and video platform properties, GSC Annotations, Bing AI Performance (export CSV manually)
- GSC history limited to 16 months; data lag 2-3 days; URL Inspection 2,000 per day per property
- Agent readiness checks plain HTTP; WebMCP and JavaScript-only behavior need manual checks
- `prepublish-lint.py` checks numeric limits and token rules only; content quality, image opacity, and signage names stay manual gate items
- Scoring (MOS), decay thresholds, and alert thresholds are [ASSUMED] engineering conventions

## Deferred Data Sources (not scripted)

- Google Ads Keyword Planner API (`KeywordPlanIdeaService`): needs an Ads account and developer token; fallback `dataforseo/query.py search-volume` (rules in SEO-DMD-01)
- Google Trends API alpha: needs allowlist access; fallback Trends web UI with anchor term (SEO-DMD-02)
- Ahrefs and Semrush: subscription tools, Tier 3; no script, availability probed only (SEO-TLS-07, SEO-TLS-11)
- X (Twitter) trends and search: `trendsmcp/query.py` reads the `X (Twitter) Trending` board and `posts --source X`; for depth use the official X API pay-per-use (Trends $0.010 per request, post read $0.005) or `twitterapi.io`; `scrapecreators/query.py` is shallow on X [COMMUNITY]
- AIsa (one balance for LLMs and 100+ data APIs): possible single-balance alternative to the two credit providers, depth unverified; no script

## Sources

Checked 2026-11-03 unless a line states another date.
- Google Search Central: https://developers.google.com/search/docs
- Search Console API: https://developers.google.com/webmaster-tools
- Bing Webmaster API: https://learn.microsoft.com/en-us/bingwebmaster/
- IndexNow: https://www.indexnow.org/documentation
- YouTube Data API: https://developers.google.com/youtube/v3/docs/search/list
- Plausible Stats API: https://plausible.io/docs/stats-api
- DataForSEO: https://dataforseo.com/pricing, https://docs.dataforseo.com/v3/
- Trends MCP (checked 2026-11-10): https://www.trendsmcp.ai/docs/api, https://www.trendsmcp.ai/data-catalog, https://www.trendsmcp.ai/pricing
- ScrapeCreators (checked 2026-11-10): https://docs.scrapecreators.com/llms.txt, https://scrapecreators.com/
- Cloudflare agent readiness: https://blog.cloudflare.com/agent-readiness/
- Citation drivers study: https://arxiv.org/abs/2610.15033
- GEO survey: https://arxiv.org/abs/2607.14035
- Competitive GEO arena: https://arxiv.org/abs/2605.25517
