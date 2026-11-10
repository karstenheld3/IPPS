# Plausible Analytics Setup

Privacy-first web analytics (no cookies). Use for conversion and traffic-source questions: which pages and sources produce goals.

## Plan Requirements [LITERAL: 2026-11-03]

- Self-hosted Community Edition: $0, Stats API included
- Cloud Starter (€9/mo) and Growth (€14/mo): no Stats API
- Cloud Business (€19/mo): Stats API included, 600 requests per hour

## Pre-Installation Verification

1. Python 3.10+ with `requests`: `python -c "import requests; print(requests.__version__)"` -> version number
2. Plausible site with tracking script installed and data visible in the dashboard

## API Key

1. Plausible dashboard -> account settings -> API Keys -> New API key -> type "Stats API"
2. Add to `[API_KEYS_FILE]`:
   ```
   PLAUSIBLE_API_KEY=placeholder-token
   PLAUSIBLE_BASE_URL=https://plausible.io
   ```
   Self-hosted: set `PLAUSIBLE_BASE_URL` to your instance URL. The key is scoped to the team that owns the site.

## Verify ($0)

```powershell
python query.py summary example.com --range 7d
```
Expected:
```
Querying 'https://plausible.io/api/v2/query' (site 'example.com', range '7d')...
  1 row received.
visitors  pageviews  bounce_rate  visit_duration
...
OK.
```

## Commands

- `summary SITE` - visitors, pageviews, bounce rate, visit duration
- `top-pages SITE` - pages by visitors (`event:page`)
- `sources SITE` - traffic sources (`visit:source`)
- `goals SITE` - goal conversions (`event:goal`)
- `raw SITE --query-file FILE` - custom Stats API v2 body (`metrics`, `date_range`, `dimensions`, `filters`, `order_by`, `pagination`); `site_id` is set from SITE

Options: `--range day|7d|30d|month|6mo|12mo|all` (default `30d`), `--limit` (default 20).

Example `query.json` for goal conversions by source:
```json
{"metrics": ["visitors", "events"], "date_range": "30d", "dimensions": ["visit:source"], "filters": [["is", "event:goal", ["Signup"]]]}
```

## Troubleshooting

- HTTP 401 -> key invalid or revoked
- HTTP 402 or 403 -> Cloud plan without Stats API (Starter, Growth) or key from another team
- HTTP 400 -> invalid metric, dimension, or filter in `raw` body
- HTTP 429 -> more than 600 requests per hour (script retries 3 times)

## Removal

1. Delete `PLAUSIBLE_API_KEY` and `PLAUSIBLE_BASE_URL` lines from `[API_KEYS_FILE]`
2. Plausible -> API Keys -> revoke the key
3. No other files to delete
