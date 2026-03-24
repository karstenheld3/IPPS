# Troubleshooting

## npx not found

Use full path: `"command": "[NPX_FULL_PATH]"`

## Profile lock errors

```powershell
Remove-Item "[USER_PROFILE_PATH]\.ms-playwright-mcp-profile\SingletonLock" -Force -ErrorAction SilentlyContinue
```

## Extension mode not connecting

Known issue (GitHub #921): `--extension` may launch new Chrome. Ensure Chrome running with `--remote-debugging-port=9222` before starting MCP.

## Element not found

1. `browser_snapshot()` to refresh refs
2. Wait for full page load
3. Check if element is in iframe (`browser_evaluate` to access)

## Automation detection

1. `--user-data-dir` with existing browser profile
2. Headed mode instead of headless
3. `--extension` mode with real browser

## Flaky Test Prevention

- Always `browser_snapshot()` before interacting
- Use stable selectors (data-testid, roles, labels)
- Wait for specific elements, not arbitrary timeouts
- Isolate tests with fresh browser contexts