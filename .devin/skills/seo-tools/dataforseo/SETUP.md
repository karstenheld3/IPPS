# DataForSEO Setup

Paid pay-per-call SEO data (keyword volume, Labs keyword and competitor data, live SERPs with AI Overview, backlinks). Use only after free sources (see `SKILL.md` When-to-Query-What matrix).

## Pre-Installation Verification

1. Python 3.10+ with `requests`:
   ```powershell
   python -c "import requests, sys; print(sys.version.split()[0], requests.__version__)"
   ```
   Expected: version numbers, no `ModuleNotFoundError`
2. Credentials file `[API_KEYS_FILE]` exists (default `[WORKSPACE_FOLDER]/../.tools/.api-keys.txt`)

## Account and Credentials

1. Create account at https://app.dataforseo.com (new accounts receive $1 trial credit; minimum top-up $50, credits do not expire) [LITERAL: 2026-11-03]
2. Open https://app.dataforseo.com/api-access
3. API login = registration email; API password = generated API password (not the account password)
4. Add to `[API_KEYS_FILE]`:
   ```
   DATAFORSEO_LOGIN=user@example.com
   DATAFORSEO_PASSWORD=0000000000000000
   ```
5. Verify the account (email and profile). Unverified accounts can read the balance, but data endpoints fail

A `DATAFORSEO_BASE64` line from older setups is ignored; the script builds Basic auth from login and password.

## Verify Connection ($0)

```powershell
python query.py balance
```
Expected:
```
Fetching account balance...
Balance USD   Total spent USD   Daily limit
--------------------------------------------
51.0          0                 [UNKNOWN]
Balance: $51.00
...
OK.
```

## First Paid Call (cost gate)

```powershell
python query.py serp "project management software"
```
Expected: `Estimate: $0.0020 (limit $0.10).`, then results and `Actual cost: $0.0020.`
Raise the limit for larger batches: `--max-cost 0.50`.

## Key Facts

- Base URL `https://api.dataforseo.com/v3/`, sandbox `https://sandbox.dataforseo.com/v3/` (`--sandbox`, dummy data)
- Auth: HTTP Basic, no token expiry; valid until the API password is reset
- Prices and endpoint bodies: `ENDPOINTS.md`
- Rate limits per endpoint: `X-RateLimit-Limit` and `X-RateLimit-Remaining` response headers
- Live results are not stored; task_post results are stored 30 days
- IP allow list (optional): dashboard -> API Access -> IP Access; leave empty for any IP

## Troubleshooting

- `ERROR: Keys file not found` -> create `[API_KEYS_FILE]` or pass `--keys-file`
- `ERROR: Key 'DATAFORSEO_LOGIN' not found` -> add the line from step 4
- `API error -> 40100` or `401xx` -> wrong login or API password
- `402xx` -> balance too low or account not verified
- `Estimate exceeds limit` -> intended; rerun with the `--max-cost` value printed

## Removal

1. Delete `DATAFORSEO_LOGIN` and `DATAFORSEO_PASSWORD` lines from `[API_KEYS_FILE]`
2. Reset the API password at https://app.dataforseo.com/api-access (invalidates the old one)
3. No other files to delete
