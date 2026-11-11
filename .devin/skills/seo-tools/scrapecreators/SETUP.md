# ScrapeCreators Setup (REST API)

Post-level public social data behind one key and one prepaid credit balance: TikTok, YouTube, Reddit, Pinterest, Instagram, and more. Use it for depth on the 1-2 candidates that `trendsmcp/query.py` or free sources surfaced, not for broad discovery.

X is shallow at this vendor (independent review ranks it last for X; user tweets return about 100 popular posts) and the vendor has no X trends and no Google Trends endpoint. X trends are a deferred source (see "Deferred Data Sources" in `SKILL.md`).

## Pricing and limits [LITERAL: 2026-11-10, checked 2026-11-11]

- Free: 100 credits without credit card, plus up to 1,200 bonus credits to claim (pricing page); the CLI docs state 10,000 free calls for GitHub signup (contradiction not resolved, `[UNVERIFIED]`)
- Packs: $47 = 25,000 credits ($1.88 per 1,000), $497 = 500,000 credits ($0.99 per 1,000); credits never expire; no subscription
- Most endpoints cost 1 credit; some cost 10 or more (find-creator-emails: 1 credit without result, 10 with an email; Google company ads with `get_ad_details=true`: 25; Instagram comments with replies: 15; TikTok audience: 26; `download_media=true`: 10); cache hits cost 0 credits; failed lookups cost 0 credits
- No API rate limit; the vendor recommends staying below 500 concurrent requests; the script sends requests one after another
- Every data response reports `credits_charged` and `credits_remaining`; the script prints both. The account endpoint `credit-balance` returns `creditCount` instead `[TESTED 2026-11-11]`
- Source: https://scrapecreators.com/, https://docs.scrapecreators.com/introduction, and the OpenAPI spec https://docs.scrapecreators.com/openapi.json (checked 2026-11-11); the OpenAPI spec lists every endpoint with its parameters

## Pre-Installation Verification

1. Python 3.10+ with `requests`: `python -c "import requests; print(requests.__version__)"` -> version number
2. An account at https://app.scrapecreators.com

## API Key

1. Sign up at https://app.scrapecreators.com and copy the API key (100 free credits)
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
- `google-search QUERY...` - `GET /v1/google/search`; `--region`, `--date-posted`, `--page` (1-11); 10 organic results per page (title, URL, description); no search volume, SERP features, or AI Overview
- `tiktok-suggestions QUERY...` - `GET /v1/tiktok/search/suggestions`; `--region`; autocomplete phrases (demand signal on TikTok)
- `youtube-typeahead QUERY...` - `GET /v1/youtube/search/typeahead`; autocomplete phrases (demand signal on YouTube)
- `google-ads DOMAIN...` - `GET /v1/google/company/ads`; `--region`, `--platform`, `--ad-format`, `--start-date`, `--end-date`, `--cursor`; 40 ads per page from the Google Ads Transparency Center; `--param get_ad_details=true` costs 25 credits per request and raises the estimate
- `youtube-transcript URL...` - `GET /v1/youtube/video/transcript`; `--language`; native captions only; table shows a text excerpt, `--format json` has the full text; a video without transcript is not charged
- `tiktok-popular-videos` - `GET /v1/tiktok/videos/popular`; `--period`, `--country`, `--page`, `--order-by`; path not in the vendor OpenAPI spec; unavailable on 2026-11-10 and 2026-11-11 (HTTP 400, `service_unavailable`, vendor message: TikTok Creative Center is down; not charged)
- `tiktok-popular-songs` - `GET /v1/tiktok/songs/popular`; `--period`, `--country`, `--page`; same status as `tiktok-popular-videos`
- `tiktok-trending-feed` - `GET /v1/tiktok/get-trending-feed`; `--region` (default US)
- `tiktok-search QUERY...` - `GET /v1/tiktok/search/keyword`; `--date-posted`, `--sort-by`, `--region`, `--cursor`
- `youtube-trending-shorts` - `GET /v1/youtube/shorts/trending`; about 48 shorts per call
- `youtube-search QUERY...` - `GET /v1/youtube/search`; `--upload-date`, `--sort-by`, `--type`, `--region`
- `reddit-search QUERY...` - `GET /v1/reddit/search`; `--filter`, `--sort`, `--timeframe`
- `reddit-subreddit NAME...` - `GET /v1/reddit/subreddit`; `--sort`, `--timeframe`
- `pinterest-topic URL...` - `GET /v1/pinterest/topic`; 1 credit per request; URL is the Pinterest ideas URL
- `instagram-search-reels QUERY...` - `GET /v2/instagram/reels/search`; `--page` (pages 1-11); results are best-effort Google-indexed reels
- `credit-balance` - `GET /v1/account/credit-balance`; free (the older path `/v1/credit-balance` returns the same data)
- Every paid command: `--max-credits N` (default 20), `--credit-price USD` (default 0.00188), `--rows N` table rows per request (default 10), `--cache-max-age 1d|3d|7d|14d|30d`, `--full` (no `trim`), `--param KEY=VALUE` for vendor parameters without an option, `--format json`

Credits per request [LITERAL: 2026-11-11, vendor claim]: 1 for every command above except `credit-balance` (0) and `google-ads` with `get_ad_details=true` (25). The same table is the `ENDPOINTS` constant in `query.py`.

Cost gate: the estimate is `requests x credits per request`. A batch stops when the credits charged reach `--max-credits`, so one expensive endpoint cannot run away.

## Parameter status (checked 2026-11-10)

- `[TESTED 2026-11-10]` live: `credit-balance`, `reddit-search`, `youtube-trending-shorts`, `tiktok-trending-feed`, `instagram-search-reels` (parameter `query`), `pinterest-topic` (parameter `url`, ideas URL with topic id); each charged 1 credit, a failed call was not charged
- `[TESTED 2026-11-11]` live: `google-search`, `tiktok-suggestions`, `youtube-typeahead`, `google-ads` (domain), `youtube-transcript`; each charged 1 credit; the vendor popular endpoints stayed unavailable and uncharged
- Vendor `llms.txt` is stale: it lists TikTok popular endpoints and Reddit ad endpoints; the Reddit ad endpoints are permanently deprecated (HTTP 400, not charged). Use the OpenAPI spec as the contract
- Confirmed from the vendor endpoint specification: `tiktok-search`, `youtube-search`, `reddit-subreddit`; `pinterest-topic` costs 1 credit per request
- `[ASSUMED]` until a live call confirms them: `tiktok-popular-videos` and `tiktok-popular-songs` parameter names (`period`, `countryCode`, `page`, `orderBy`; the endpoints were down), the 1-credit price of each endpoint not listed as tested; use `--param` to correct a name without editing the script
- Response parsing is tolerant: known list keys first, otherwise the first list of objects; rows carry title, author, views, likes, comments, shares, published date, and URL where the vendor sends them
- Observed behavior `[TESTED 2026-11-11]`:
  - `tiktok-suggestions` with `--region US` still returned UK variants ("... uk", "under £100"); `youtube-typeahead` has no region parameter; the `score` field is relevance, not likes
  - `youtube-typeahead` returned 4 rows for "standing desk calculator" and 14 for "standing desk"
  - `google-ads DOMAIN` lists every ad whose destination is the domain, including customers and agencies: own-brand ads were 39 of 40 for asana.com, 35 of 40 for teamwork.com, 7 of 40 for acuityscheduling.com, 14 of 28 for youcanbook.me; group rows by advertiser

## Troubleshooting

- `HTTP 401` -> `SCRAPECREATORS_API_KEY` missing or wrong
- `HTTP 402` -> credits exhausted; buy credits in the dashboard
- `HTTP 400` -> a required parameter is missing or invalid, or the vendor endpoint is unavailable (`service_unavailable`, body `errorStatus` 503); compare with the endpoint page on https://docs.scrapecreators.com
- `0 rows (not found)` -> the vendor confirmed the resource does not exist; confirmed not-found may be billed as an answered request
- Duplicate TikTok results -> TikTok-side behavior documented by the vendor
- Missing TikTok posts -> not proof of deletion; see https://docs.scrapecreators.com/tiktok-post-availability.md

## Removal

1. Delete the `SCRAPECREATORS_API_KEY` line from `[API_KEYS_FILE]`
2. Revoke or rotate the API key in https://app.scrapecreators.com
3. No other files to delete
