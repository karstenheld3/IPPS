# ScrapeCreators Setup (REST API)

Post-level public social data behind one key and one prepaid credit balance: TikTok, YouTube, Reddit, Pinterest, Instagram, and more. Use it for depth on the 1-2 candidates that `trendsmcp/query.py` or free sources surfaced, not for broad discovery.

X is shallow at this vendor (independent review ranks it last for X; user tweets return about 100 popular posts) and the vendor has no X trends and no Google Trends endpoint. X trends are a deferred source (see "Deferred Data Sources" in `SKILL.md`).

## Pricing and limits [LITERAL: 2026-11-10]

- Free: 100 credits
- Packs: $47 = 25,000 credits ($1.88 per 1,000), $497 = 500,000 credits ($0.99 per 1,000); credits never expire; no subscription
- Most endpoints cost 1 credit; some cost 10 or more (for example find-creator-emails: 1 credit without result, 10 credits with an email); cache hits cost 0 credits; failed lookups cost 0 credits
- No API rate limit; the vendor recommends staying below 500 concurrent requests; the script sends requests one after another
- Every response reports `credits_charged` and `credits_remaining`; the script prints both
- Source: https://scrapecreators.com/ and https://docs.scrapecreators.com/introduction (checked 2026-11-10)

## Pre-Installation Verification

1. Python 3.10+ with `requests`: `python -c "import requests; print(requests.__version__)"` -> version number
2. An account at https://app.scrapecreators.com

## API Key

1. Sign up at ccc and copy the API key (100 free credits)
2. Add to `[API_KEYS_FILE]`:
   ```
   SCRAPECREATORS_API_KEY=placeholder-key
   ```

## Verify (free)

```powershell
python query.py credit-balance
```
Expected:
```
Fetching credit balance...
  1 row received.
Credits remaining
-----------------
100
Credits remaining: 100
OK.
```
Run `credit-balance` before and after a paid batch; the difference equals `credits_charged`.

## Commands

Each command is one vendor endpoint; query commands accept several values and send one request per value.
- `tiktok-popular-videos` - `GET /v1/tiktok/videos/popular`; `--period`, `--country`, `--page`, `--order-by`; unavailable on 2026-11-10 (HTTP 400, vendor message: TikTok Creative Center is down; not charged)
- `tiktok-popular-songs` - `GET /v1/tiktok/songs/popular`; `--period`, `--country`, `--page`; unavailable on 2026-11-10 (HTTP 400, same cause; not charged)
- `tiktok-trending-feed` - `GET /v1/tiktok/get-trending-feed`; `--region` (default US)
- `tiktok-search QUERY...` - `GET /v1/tiktok/search/keyword`; `--date-posted`, `--sort-by`, `--region`, `--cursor`
- `youtube-trending-shorts` - `GET /v1/youtube/shorts/trending`; about 48 shorts per call
- `youtube-search QUERY...` - `GET /v1/youtube/search`; `--upload-date`, `--sort-by`, `--type`, `--region`
- `reddit-search QUERY...` - `GET /v1/reddit/search`; `--filter`, `--sort`, `--timeframe`
- `reddit-subreddit NAME...` - `GET /v1/reddit/subreddit`; `--sort`, `--timeframe`
- `pinterest-topic URL...` - `GET /v1/pinterest/topic`; 1 credit per request; URL is the Pinterest ideas URL
- `instagram-search-reels QUERY...` - `GET /v2/instagram/reels/search`; `--page` (pages 1-11); results are best-effort Google-indexed reels
- `credit-balance` - `GET /v1/credit-balance`; free
- Every paid command: `--max-credits N` (default 20), `--credit-price USD` (default 0.00188), `--rows N` table rows per request (default 10), `--cache-max-age 1d|3d|7d|14d|30d`, `--full` (no `trim`), `--param KEY=VALUE` for vendor parameters without an option, `--format json`

Credits per request [LITERAL: 2026-11-10, vendor claim]: 1 for every command above except `credit-balance` (0). The same table is the `ENDPOINTS` constant in `query.py`.

Cost gate: the estimate is `requests x credits per request`. A batch stops when the credits charged reach `--max-credits`, so one expensive endpoint cannot run away.

## Parameter status (checked 2026-11-10)

- `[TESTED 2026-11-10]` live: `credit-balance`, `reddit-search`, `youtube-trending-shorts`, `tiktok-trending-feed`, `instagram-search-reels` (parameter `query`), `pinterest-topic` (parameter `url`, ideas URL with topic id); each charged 1 credit, a failed call was not charged
- Confirmed from the vendor endpoint specification: `tiktok-search`, `youtube-search`, `reddit-subreddit`; `pinterest-topic` costs 1 credit per request
- `[ASSUMED]` until a live call confirms them: `tiktok-popular-videos` and `tiktok-popular-songs` parameter names (`period`, `countryCode`, `page`, `orderBy`; the endpoints were down), the 1-credit price of each endpoint not listed as tested; use `--param` to correct a name without editing the script
- Response parsing is tolerant: known list keys first, otherwise the first list of objects; rows carry title, author, views, likes, comments, shares, published date, and URL where the vendor sends them

## Troubleshooting

- `HTTP 401` -> `SCRAPECREATORS_API_KEY` missing or wrong
- `HTTP 402` -> credits exhausted; buy credits in the dashboard
- `HTTP 400` -> a required parameter is missing or invalid; compare with the endpoint page on https://docs.scrapecreators.com
- `0 rows (not found)` -> the vendor confirmed the resource does not exist; confirmed not-found may be billed as an answered request
- Duplicate TikTok results -> TikTok-side behavior documented by the vendor
- Missing TikTok posts -> not proof of deletion; see https://docs.scrapecreators.com/tiktok-post-availability.md

## Removal

1. Delete the `SCRAPECREATORS_API_KEY` line from `[API_KEYS_FILE]`
2. Revoke or rotate the API key in https://app.scrapecreators.com
3. No other files to delete
