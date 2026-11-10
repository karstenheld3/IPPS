# YouTube Data API Setup

Free video demand and competition data: which videos rank for a query, their views, likes, comments, and age.

## Quota [LITERAL: 2026-11-03]

- `search` (search.list): max 100 calls per day. Google documents this either as 100 units per call out of the 10,000-unit project quota or as a separate "Search Queries" bucket of 100 calls per day; both allow 100 searches per day
- `videos` (videos.list): 1 unit per call for up to 50 video IDs, from the default 10,000 units per day
- Quotas reset at midnight Pacific Time

## Pre-Installation Verification

1. Python 3.10+ with `requests`: `python -c "import requests; print(requests.__version__)"` -> version number
2. Google account with access to https://console.cloud.google.com

## API Key

1. Google Cloud Console -> create or select a project (the Search Console project can be reused)
2. APIs & Services -> Library -> "YouTube Data API v3" -> Enable
3. APIs & Services -> Credentials -> Create credentials -> API key
4. Edit the key -> API restrictions -> Restrict key -> select only "YouTube Data API v3" -> Save
5. Add to `[API_KEYS_FILE]`:
   ```
   YOUTUBE_API_KEY=placeholder-key
   ```

## Verify (1 unit)

```powershell
python query.py videos dQw4w9WgXcQ
```
Expected:
```
Fetching statistics for 1 video (1 call, 1 unit)...
  1 video received.
Video ID      Title ...  Views ...
...
Quota used: 0 search calls (max 100 per day), 1 unit (default 10,000 per day).
OK.
```

## Commands

- `search QUERY` - top videos by relevance; `--max-results 1-50`, `--region US`, `--lang en`
- `videos ID...` - snippet and statistics for known video IDs

Typical demand check: `search` once (1 of 100 daily searches), then `videos` for the returned IDs (1 unit) to compare views and age.

## Troubleshooting

- HTTP 403 `accessNotConfigured` -> step 2 not done in the key's project
- HTTP 400 `keyInvalid` -> wrong key or key restricted to another API
- `Daily quota exceeded` -> wait for the reset or use another project
- HTTP 403 with referrer or IP restriction -> remove application restrictions for CLI use

## Removal

1. Delete the `YOUTUBE_API_KEY` line from `[API_KEYS_FILE]`
2. Google Cloud Console -> Credentials -> delete the API key
3. No other files to delete
