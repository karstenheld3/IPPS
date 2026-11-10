# DataForSEO Endpoints Reference

Base URL: `https://api.dataforseo.com/v3/` (sandbox: `https://sandbox.dataforseo.com/v3/`)
Auth: HTTP Basic with `DATAFORSEO_LOGIN:DATAFORSEO_PASSWORD` (see `SKILL.md` section "Credential Keys")
Prices: [LITERAL: 2026-11-03], source https://dataforseo.com/pricing (checked 2026-11-03). Re-verify before paid batches when older than 6 months.

## Request Patterns

- live: submit and receive result in one call; higher price; used by `query.py`
- task_post: queue task, fetch later with `task_get/{id}`; lower price (SERP Standard $0.0006); results stored 30 days
- One request may carry several tasks; `query.py` sends one task per request and splits search volume lists into tasks of 1,000 keywords

## Price Table [LITERAL: 2026-11-03]

- SERP Google Organic: Standard (task_post) $0.0006/SERP, Live $0.002/SERP
- Keywords Data Google Ads or Bing Ads search volume: Standard queue $0.06/task, Live $0.09/task, up to 1,000 keywords per task; Live is limited to 12 requests per minute per account (re-verified 2026-11-10 at https://dataforseo.com/pricing/keywords-data/google-ads; `query.py` uses Live)
- DataForSEO Labs (keyword suggestions, keyword ideas, competitors, ranked keywords): $0.012/task + $0.00012/item
- Clickstream data: $0.012/task + $0.00012/item
- Google Trends: $0.0027/task
- DataForSEO Trends: $0.0012/task
- Backlinks: $0.024/task + $0.000036/row
- On-Page: from $0.00015/page
- Domain Analytics: from $0.012/task
- AI Optimization LLM Responses: $0.0002/task + LLM provider cost
- AI Optimization LLM Scraper: $0.0012/page
- AI Optimization AI Keyword Search Volume: $0.01/task + $0.0001/row
- AI Optimization LLM Mentions: $0.10/task + $0.001/row
- Appendix (balance, locations, languages): $0

## Commands Implemented in query.py

- `balance` -> `GET /v3/appendix/user_data` -> $0
- `keywords SEED` -> `POST /v3/dataforseo_labs/google/keyword_suggestions/live` -> $0.012 + limit x $0.00012
- `search-volume KW...` -> `POST /v3/keywords_data/google_ads/search_volume/live` -> $0.09 per 1,000 keywords (Live; Standard queue $0.06)
- `serp KEYWORD` -> `POST /v3/serp/google/organic/live/advanced` with `load_async_ai_overview: true` -> $0.002
- `competitors DOMAIN` -> `POST /v3/dataforseo_labs/google/competitors_domain/live` -> $0.012 + limit x $0.00012
- `backlinks DOMAIN` -> `POST /v3/backlinks/summary/live` -> $0.024 + $0.000036 per row

## SERP API

Live advanced with AI Overview:
```json
[{"keyword": "project management software", "location_code": 2840, "language_code": "en", "device": "desktop", "load_async_ai_overview": true}]
```
Returns organic results, featured snippets, People Also Ask, `ai_overview` items, and `item_types` (SERP feature list). Without `load_async_ai_overview: true`, AI Overviews that load asynchronously are missing.

Task post (bulk, cheaper):
```json
[{"keyword": "task tracker", "location_code": 2840, "language_code": "en", "tag": "batch-01"}]
```
Fetch: `GET /v3/serp/google/organic/task_get/advanced/{task_id}`

## Keywords Data API

Search volume (up to 1,000 keywords per task):
```json
[{"keywords": ["kanban board", "gantt chart", "task tracker"], "location_code": 2840, "language_code": "en"}]
```
Returns per keyword: `search_volume`, `monthly_searches`, `competition`, `cpc`.

Related endpoints (not wrapped by `query.py`): `keywords_data/google_ads/keywords_for_site/live`, `keywords_data/google_ads/keywords_for_keywords/live`.

## DataForSEO Labs API

Keyword suggestions:
```json
[{"keyword": "project management", "location_code": 2840, "language_code": "en", "limit": 30, "include_seed_keyword": true}]
```
Returns `keyword`, `keyword_info.search_volume`, `keyword_info.cpc`, `keyword_properties.keyword_difficulty`, `search_intent_info.main_intent`.

Competitors domain:
```json
[{"target": "example.com", "location_code": 2840, "language_code": "en", "limit": 20}]
```
Returns `domain`, `avg_position`, `intersections`, `full_domain_metrics.organic.count`, `full_domain_metrics.organic.etv`.

Related endpoints (not wrapped): `keyword_ideas/live`, `serp_competitors/live`, `domain_rank_overview/live`, `relevant_pages/live`, `ranked_keywords/live`.

## Backlinks API

Summary:
```json
[{"target": "example.com", "internal_list_limit": 10, "backlinks_status_type": "live"}]
```
Returns `backlinks`, `referring_domains`, `referring_main_domains`, `rank`, `broken_backlinks`.

Link gap (not wrapped): `POST /v3/backlinks/domain_intersection/live` with `{"targets": {"1": "example.com", "2": "example.org"}, "exclude_targets": ["example.net"]}` returns domains linking to the targets but not to the excluded domain.

## AI Optimization API

Not wrapped by `query.py`; call manually only after a cost estimate.
- LLM Mentions: `POST /v3/ai_optimization/llm_mentions/...` ($0.10/task + $0.001/row)
- AI Keyword Search Volume: `POST /v3/ai_optimization/ai_keyword_data/...` ($0.01/task + $0.0001/row)

## Appendix (free)

- `GET /v3/appendix/user_data` - balance and spend
- `GET /v3/appendix/locations` - location codes (2840 United States, 2826 United Kingdom, 2276 Germany, 2250 France, 2756 Switzerland, 2040 Austria)
- `GET /v3/appendix/languages` - language codes (`en`, `de`, `fr`, `es`, `pt`)

## Response Status

- Top level and each task carry `status_code`; `20000` = OK
- `cost` at top level = total USD charged for the request
- Codes starting with `401` or `402`: credentials, balance, or account verification problem

## Typical Research Session Cost

- 3 Labs suggestion calls with 100 items each: 3 x ($0.012 + 100 x $0.00012) = $0.072
- 2 search volume tasks (up to 2,000 keywords): 2 x $0.09 = $0.18
- 10 live SERPs: 10 x $0.002 = $0.02
- 1 backlinks summary: $0.024 + $0.000036 = ~$0.024
- Total: ~$0.30
