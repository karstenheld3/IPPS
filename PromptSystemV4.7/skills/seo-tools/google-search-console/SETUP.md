# Google Search Console Setup

Free first-party Google data: Search Analytics (queries, pages, clicks, impressions, CTR, position), URL Inspection, sitemaps. Access via service account and `query.py`.

## Pre-Installation Verification

1. Python 3.10+ with `requests` and `google-auth`:
   ```powershell
   python -c "import requests, google.oauth2.service_account; print('ok')"
   ```
   Expected: `ok`. If missing: `pip install requests google-auth`
2. You are owner or full user of at least one Search Console property (https://search.google.com/search-console)

## Service Account Setup

1. Open https://console.cloud.google.com, create or select a project
2. APIs & Services -> Library -> "Google Search Console API" -> Enable
3. IAM & Admin -> Service Accounts -> Create service account (no project roles needed)
4. Service account -> Keys -> Add key -> JSON -> download
5. Store the JSON file in the folder of `[API_KEYS_FILE]` and add its file name (relative, no folder):
   ```
   GSC_SERVICE_ACCOUNT_FILE=gsc-service-account.json
   ```
6. Search Console -> Settings -> Users and permissions -> Add user -> service account email (`name@project-id.iam.gserviceaccount.com`)
   - Restricted: enough for `sites`, `analytics`, `inspect`, `sitemaps` list, and all derived analyses
   - Full: required for `sitemaps --submit`
7. Repeat step 6 for every property

## Verify ($0)

```powershell
python query.py sites
```
Expected:
```
Listing Search Console properties...
  1 property found.
Site                                                Permission
...
sc-domain:example.com                               siteRestrictedUser
OK.
```

## Commands

- `sites` - properties visible to the service account
- `analytics SITE` - Search Analytics; `--dimensions query,page,country,device,date,searchAppearance`, `--start`, `--end`, `--filter DIMENSION:OPERATOR:VALUE`, `--search-type web|image|video|news|discover|googleNews`, `--rows`
- `inspect SITE URL...` - index status, user vs Google canonical, last crawl, robots, mobile, rich results
- `sitemaps SITE [--submit SITEMAP_URL]`
- `quick-wins SITE` - queries at average position 4-15 by impressions
- `ctr-gap SITE` - pages with >= 1,000 impressions in 90 days and CTR below 0.60 x median CTR of the site's pages in the same position bucket
- `decay SITE` - pages losing >= 20% and >= 50 clicks (last 3 full months vs same months one year earlier)
- `cannibalization SITE` - queries where >= 2 pages each get >= 10% of impressions

SITE format: domain property `sc-domain:example.com` or URL-prefix property `https://example.com/` (exactly as listed by `sites`).

## Limits [LITERAL: 2026-11-03]

- Search Analytics: max 25,000 rows per request (script paginates), 16 months retention, data lag 2-3 days
- URL Inspection: 2,000 requests per day and 600 per minute per property
- Clicks are the reliable metric for comparisons that include May-September 2025 (impression logging anomaly)

## UI-Only Features (no API)

- Generative AI performance report (AI Overviews and AI Mode impressions and clicks): Search Console -> Performance -> Generative AI
- Search generative AI control setting for the property
- Social and Video Platform Properties (channel performance across Google surfaces, about 24 h data delay)
- Annotations on performance charts: max 120 characters each, max 200 per property; add one for every significant publish or change

## Google Indexing API

The Indexing API accepts only pages with `JobPosting` or `BroadcastEvent` (in `VideoObject`) structured data (200 URLs per day). Never use it for regular pages. For regular pages: accurate sitemap `<lastmod>`, internal links, and URL Inspection "Request indexing" in the UI.

## Troubleshooting

- `HTTP 403 ... API has not been used in project ... or it is disabled` -> step 2
- `HTTP 403 ... User does not have sufficient permission` -> step 6 for that property; Full for `--submit`
- `0 properties` -> service account email not added to any property
- `Service account file not found` -> JSON not in the keys file folder or file name differs
- `Service account file invalid` -> file is an OAuth client secret, not a service account key (`"type": "service_account"` required)

## Removal

1. Search Console -> Settings -> Users and permissions -> remove the service account email from every property
2. Google Cloud -> Service Accounts -> delete the key or the service account
3. Delete the JSON file and the `GSC_SERVICE_ACCOUNT_FILE` line from `[API_KEYS_FILE]`
