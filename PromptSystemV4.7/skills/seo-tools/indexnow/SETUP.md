# IndexNow Setup

Free push notification of new or changed URLs. One submission reaches Bing, Yandex, Naver, Seznam, and Yep [LITERAL: 2026-11-03]. Google does not take part: for Google, keep sitemap `<lastmod>` accurate and use Search Console URL Inspection. The Google Indexing API is only for pages with `JobPosting` or `BroadcastEvent` (in `VideoObject`) structured data, never for regular URLs.

## Pre-Installation Verification

1. Python 3.10+ with `requests`: `python -c "import requests; print(requests.__version__)"` -> version number
2. You can publish a static text file at the site root over HTTPS (for example a static `public/` folder)

## Key Setup

1. Generate a key (8-128 characters, `a-z`, `A-Z`, `0-9`, `-`):
   ```powershell
   python -c "import secrets; print(secrets.token_hex(16))"
   ```
2. Create a file named `{key}.txt` containing only the key and deploy it to `https://example.com/{key}.txt`
3. Optional: add the key to `[API_KEYS_FILE]` (otherwise pass `--key` each time):
   ```
   INDEXNOW_API_KEY=0123456789abcdef0123456789abcdef
   ```
   One key per site. With several sites, pass `--key` per call.
4. Verify the key file:
   ```powershell
   python submit.py verify-key --host example.com
   ```
   Expected: `PASS: Key file matches.` and `OK.`

## Submit URLs

```powershell
python submit.py submit https://example.com/blog/new-post --host example.com
python submit.py submit https://example.com/a https://example.com/b --host example.com
python submit.py submit --file urls.txt --host example.com --dry-run
```
- 1 URL -> `GET https://api.indexnow.org/indexnow?url=...&key=...`
- 2+ URLs -> `POST https://api.indexnow.org/indexnow` with JSON `{"host", "key", "keyLocation", "urlList"}`, max 10,000 URLs per POST; larger lists are split
- All URLs must be on `--host`; mismatches stop the run (exit 2)

## Response Codes

- 200 - OK, URLs submitted
- 202 - Accepted, key pending verification (retry later)
- 400 - Bad request, invalid format
- 403 - Key not valid or key file not found
- 422 - URLs do not belong to host or key does not match
- 429 - Too many requests (script retries 3 times)

## Key Facts

- Free, no account, no dashboard
- Submit only new, changed, or deleted URLs; repeated submission of unchanged URLs gives no benefit
- Key file name = key value + `.txt`; must be reachable over HTTPS
- `--key-location` allows the key file in a sub-folder; only URLs under that folder are then accepted

## Troubleshooting

- `Invalid key` -> regenerate with step 1
- `verify-key` FAIL HTTP 404 -> key file not deployed or wrong path
- 403 on submit -> key file content differs from the key (trailing whitespace is ignored by the script, not always by engines)
- 422 -> URL host differs from `--host` (for example `www.` vs apex)

## Removal

1. Delete the `INDEXNOW_API_KEY` line from `[API_KEYS_FILE]`
2. Delete `{key}.txt` from the site root
3. No account to close
