---
description: Run tests based on scope and context
---

# Test Workflow

Run tests based on scope and context.

## Required Skills

- @ms-playwright-mcp for UI testing (SCOPE-UI only)
- @write-documents for documenting problems and failures

## Context Branching

Check scope and proceed accordingly:

### SCOPE-UI

Test UI functionality using Playwright MCP server.

1. Gather UI requirements from SPEC or TEST plan
2. Test using `mcp0_execute` for browser automation
3. Use `accessibilitySnapshot` for element discovery
4. Use `screenshotWithAccessibilityLabels` for visual verification
5. Document results in PROGRESS.md

### SCOPE-CODE

Test code against IMPL and TEST plans.

1. Gather test cases from TEST plan (or IMPL if no TEST)
2. Run using existing test framework or temporary scripts
3. For temporary scripts: prefix with `.tmp_` for cleanup
4. Verify all test cases pass
5. Document problems in PROBLEMS.md and failures in FAILS.md (see @write-documents)

### SCOPE-BUILD

Test if build prerequisites are fulfilled.

1. Gather build requirements from README.md or NOTES.md
2. Verify dependencies installed (package.json, requirements.txt, etc.)
3. Verify environment variables configured
4. Run build command and check success
5. Document missing prerequisites in PROBLEMS.md

### SCOPE-DEPLOY

Test if deployment succeeded.

1. Verify deployment target accessible
2. Check health endpoints respond
3. Test core functionality in deployed environment
4. Verify no errors in deployment logs
5. Document deployment issues in PROBLEMS.md

## Execution

1. Determine which scope applies
2. Execute scope-specific steps above
3. Document results (pass/fail with details)
4. If failures: fix or escalate to user

## Quality Gate

- [ ] All tests executed
- [ ] Results documented
- [ ] Failures addressed or tracked in PROBLEMS.md

## Rules

- Always run tests before committing
- Use existing test infrastructure when available
- Clean up `.tmp_*` test files after completion
- Document flaky tests in PROBLEMS.md with reproduction steps
