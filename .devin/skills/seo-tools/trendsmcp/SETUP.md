# Trends MCP Setup (REST API)

Cross-platform trend discovery behind one key: time series, growth, live ranked boards, and "what people post" for 54 sources (Google, YouTube, TikTok, Reddit, X, Pinterest, Wikipedia, GitHub, app stores, and more). The skill calls the REST API only; it does not use the MCP server of the same vendor.

## Pricing and limits [LITERAL: 2026-11-10]

- Free tier: 100 requests per month, no credit card
- Credits: never expire; 1 credit = 1 successful request; failed calls are free (vendor claim)
- Packs: 600 credits $15 (2.5 cents per credit), 2,500 credits $49 (1.96 cents), 12,000 credits $199 (1.66 cents)
- Optional subscription plans exist; the skill does not need them
- `board` costs 1 credit per 10 rows (`limit=5` = 1 credit; `limit` 1-200, vendor default 100 = 10 credits) `[TESTED 2026-11-10]`; responses carry `requests_charged` and `cost_note`, the script estimates `ceil(limit / 10)` per board and prints the charged value
- Source: https://www.trendsmcp.ai/pricing (checked 2026-11-10)

## Pre-Installation Verification

1. Python 3.10+ with `requests`: `python -c "import requests; print(requests.__version__)"` -> version number
2. An email address for the account sign-in code

## API Key

1. Open https://www.trendsmcp.ai/account and sign in with the emailed code
2. Copy the API key from the dashboard
3. Add to `[API_KEYS_FILE]`:
   ```
   TRENDSMCP_API_KEY=placeholder-key
   ```

## Verify (1 credit, free tier) `[TESTED 2026-11-10]`

```powershell
python query.py growth "standing desk" --source "Google Search" --window 3M
```
Expected:
```
Estimating credits for 'growth' (1 request x 1 credit)...
  Estimate: 1 credit = $0.0250 (limit 20 credits).
  [ 1 / 1 ] Growth for 'standing desk' on 'Google Search' (3M)...
  1 row received.
Keyword       Period   Growth %   Direction  Recent  Baseline  Vol. growth %
...
Credits used: 1 credit = $0.0250 at $0.025 per credit (estimate 1 credit). Index values compare momentum; absolute volume exists only where 'volume' is shown.
OK.
```

## Commands

- `history KEYWORD... --source S` - weekly time series (about 260 points); `--last N` table rows per keyword (default 26); JSON has all points
- `growth KEYWORD... --source S --window 7D 3M 12M` - percent growth per window (`D`, `W`, `M`, `Y` up to 5 years, plus `MTD`, `QTD`, `YTD`)
- `board --type NAME [NAME...] --limit N [--climbers]` - live ranked board; `--climbers` sorts by rank change
- `posts KEYWORD... --source S --days N` - posts, videos, stories with engagement
- Every command: `--max-credits N` (default 20), `--credit-price USD` (default 0.025), `--country CODE`, `--format json`

Typical discovery run: one `board` call for the platform of interest, then `growth` for the 3-5 most promising candidates, then depth calls with `scrapecreators/query.py` on the top 1-2.

## Source and board names (catalog updated 2026-11-06, checked 2026-11-10)

Source names are case-insensitive in the script and checked before any request.
- `history` and `growth` sources (14): Google Search, Google Images, Google News, Google Shopping, YouTube, Wikipedia, TikTok, Amazon, Pinterest, npm, Python, Steam, App Downloads, App Rankings
- `board` types (27): Amazon Best Sellers Top Rated, Amazon Best Sellers by Category, App Store Top Free, App Store Top Paid, GitHub, Google News Top News, Google Play, Google Trends, Google Trends by Category, IMDb MOVIEmeter, Open Library Trending Books, Pinterest Trending, Pinterest Trending by Category, Polymarket Top Markets, Reddit Hot Posts, Reddit World News, Top Websites, Spotify Top Podcasts, Steam Most Played, Substack, Substack by Category, TikTok Trending Hashtags, TikTok Trending Hashtags by Category, TikTok Trending Searches, Wikipedia Trending, X (Twitter) Trending, YouTube Trending
- `posts` sources (10): News, YouTube, TikTok, Instagram, X, Reddit, Bluesky, Hacker News, Polymarket, GitHub
- Reviews (App Store, Google Play, Amazon) exist in the API; the script does not wrap them
- Current list: https://www.trendsmcp.ai/data-catalog

## Reading the numbers

- `value` is a normalized 0-100 index per source: it compares momentum within one keyword and source, not absolute demand
- `volume` appears only where the source provides it (for example Google Search); size demand with `dataforseo/query.py search-volume` when `volume` is missing
- The methodology of the index per source is not documented by the vendor `[ASSUMED]`

## Troubleshooting

- `HTTP 401` or `403` -> `TRENDSMCP_API_KEY` missing or wrong
- `Free tier exhausted` -> `monthly_limit_reached`; buy credits in the account dashboard
- `HTTP 402` -> credits exhausted; top up
- `Unknown source` -> use a name from the lists above; the script prints the valid names
- `posts --source Reddit` returned a vendor-side status 502 on 2026-11-10 (other sources worked: News, YouTube); use `scrapecreators/query.py reddit-search` instead
- `0 rows` -> the vendor answered `no_data` for that keyword and source (the call is not charged)

## Removal

1. Delete the `TRENDSMCP_API_KEY` line from `[API_KEYS_FILE]`
2. Revoke or rotate the API key in https://www.trendsmcp.ai/account
3. No other files to delete
