# Authentication Strategies

## Strategy 1: Persistent User Profile

Configure `--user-data-dir` to persist cookies and login state:
```json
{"args": ["@playwright/mcp@latest", "--user-data-dir", "[USER_PROFILE_PATH]/.ms-playwright-mcp-profile"]}
```

## Strategy 2: Storage State File

Save state after login: `await context.storageState({ path: 'auth.json' });`

Use with: `"args": ["@playwright/mcp@latest", "--storage-state", "auth.json"]`

## Strategy 3: Browser Extension Mode

Connect to existing browser: `"args": ["@playwright/mcp@latest", "--extension"]`

Start Chrome with debugging: `& "[PROGRAM_FILES]\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222`

Note: Known issue (GitHub #921) - may launch new Chrome instead of connecting.