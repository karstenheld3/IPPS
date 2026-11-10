# Bing Webmaster Tools Setup

Free first-party Bing data: query and page stats, daily traffic, inbound links, URL submission quota. Bing results also feed Microsoft Copilot and other AI assistants that ground on Bing.

## Pre-Installation Verification

1. Python 3.10+ with `requests`: `python -c "import requests; print(requests.__version__)"` -> version number
2. Account at https://www.bing.com/webmasters with at least one verified site (import from Google Search Console is the fastest path)

## API Key

1. Bing Webmaster Tools -> Settings (gear icon) -> API access -> API key -> Generate
2. Add to `[API_KEYS_FILE]`:
   ```
   BING_WEBMASTER_API_KEY=00000000000000000000000000000000
   ```
3. One key covers all sites in the account

## Verify ($0)

```powershell
python query.py sites
```
Expected:
```
Listing Bing Webmaster sites...
  1 site found.
Site                                                Verified
...
https://example.com/                                True
OK.
```
`0 sites found.` means the key works but the account has no site yet.

## Commands

- `sites` - sites in the account
- `query-stats SITE` - queries aggregated over the available period (clicks, impressions, impression-weighted average position)
- `page-stats SITE` - pages aggregated the same way
- `traffic SITE` - daily clicks and impressions
- `links SITE` - pages with inbound link counts
- `quota SITE` - remaining daily and monthly URL submission quota
- `submit SITE URL...` - submit URLs (checks quota first; for bulk use `indexnow/submit.py`)

SITE = site URL exactly as listed by `sites`.

## Key Facts [LITERAL: 2026-11-03]

- Endpoint `https://ssl.bing.com/webmaster/api.svc/json/{Method}?apikey=...`; responses wrapped in `{"d": ...}`
- SOAP and POX endpoints were retired on 2026-08-31; only JSON is used
- API key travels as query parameter; the script never prints request URLs with parameters

## AI Performance Report (UI only, no API)

Bing Webmaster Tools -> AI Performance shows how often site pages are cited in Copilot and Bing AI answers:
- Grounding Queries: queries for which a page was used as grounding source
- Citation Share: share of citations for the site within a topic
- Topics, Intents, Compare (period comparison)

Export: open the report -> select period -> Download (CSV). Store exports in the project, not in the skill folder.

## Troubleshooting

- `ERROR: Key 'BING_WEBMASTER_API_KEY' not found` -> step 2 of API Key
- HTTP 400 or 401 on any method -> key invalid or regenerated; generate a new key
- HTTP 400 for a site -> SITE differs from the registered URL (trailing slash, `www.`, `http` vs `https`)
- `exceed remaining daily quota` -> submit fewer URLs or use IndexNow

## Removal

1. Delete the `BING_WEBMASTER_API_KEY` line from `[API_KEYS_FILE]`
2. Bing Webmaster Tools -> Settings -> API access -> revoke or regenerate the key
3. No other files to delete
