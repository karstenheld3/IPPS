---
description: Run tests based on scope and context
auto_execution_mode: 1
---

# Test Workflow

## Required Skills

- @ms-playwright-mcp for UI testing
- @write-documents for documenting problems/failures
- @coding-conventions for code verification

## MUST-NOT-FORGET

- Re-read TEST plan (or IMPL if no TEST) before testing
- Check SPEC for edge cases needing coverage
- Make internal checklist; update after each test, note failures immediately
- Never skip documenting failures

## GLOBAL-RULES

- Always run tests before committing
- Use existing test infrastructure when available
- Clean up `.tmp_*` test files after completion
- Document flaky tests in PROBLEMS.md with reproduction steps

## Workflow

1. Determine context (UI, Code, Build, Deploy)
2. Read relevant context section below
3. Execute steps
4. Document results (pass/fail with details)
5. If failures: fix or ask user

# CONTEXT-SPECIFIC

## UI Testing

1. Gather UI requirements from SPEC or TEST plan
2. Test via Playwright MCP (`mcp0_execute`)
3. Use `accessibilitySnapshot` for element discovery
4. Use `screenshotWithAccessibilityLabels` for visual verification
5. Document results in PROGRESS.md

## Code Testing

1. Gather test cases from TEST plan (or IMPL)
2. Run tests via existing framework or `.tmp_` scripts
3. Verify all test cases pass
4. Document problems in PROBLEMS.md, failures in FAILS.md

## Build Testing

1. Gather build requirements from README.md or NOTES.md
2. Verify dependencies installed
3. Verify environment variables configured
4. Test build command succeeds
5. Document missing prerequisites in PROBLEMS.md

## Deploy Testing

1. Verify deployment target accessible
2. Test health endpoints respond
3. Test core functionality in deployed environment
4. Verify no errors in deployment logs
5. Document issues in PROBLEMS.md