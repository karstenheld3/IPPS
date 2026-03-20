# Script-Level Logging Rules

Rules for script output used by Quality Assurance (QA) to verify correctness.

Goal: All failure information must be in the logs. QA must understand what failed and why from log output alone.

## Related Documents

- `LOGGING-RULES.md` - General rules (LOG-GN-01 to LOG-GN-11)
- `LOGGING-RULES-USER-FACING.md` - User-facing rules (LOG-UF-01 to LOG-UF-06)
- `LOGGING-RULES-APP-LEVEL.md` - App-level rules (LOG-AP-01 to LOG-AP-05)

## Rules

### LOG-SC-01: No Timestamps

Test output must be deterministic for diff comparison. No timestamps in test logic.

```
Running test_user_creation...
  OK.
Test 'test_user_creation' completed.
```

Exception: Selftest endpoints streaming to users may include timestamps for progress, but test logic must not depend on them.

### LOG-SC-02: Section Structure

All test output MUST use 100-char START/END headers/footers (matches LOG-UF-06).

- Test header/footer (REQUIRED) - 100 chars total, wraps entire test run
- Phase header - `===== Phase N: Name =====` (5 `=` each side) for sub-phases

```
======================================== START: SHAREPOINT SELFTEST ========================================

===== Phase 1: Configuration =====

[ 1 / 25 ] M1: Config validation - site URL...
  OK. site_url='https://contoso.sharepoint.com/sites/SelftestSite'

===== Phase 2: Connection =====

[ 3 / 25 ] M3: Connect to SharePoint site...
  OK. Connected as 'app@contoso.onmicrosoft.com'

========================================= END: SHAREPOINT SELFTEST =========================================
25 tests passed, 0 failed.
```

### LOG-SC-03: Test Case IDs

Use prefix format for traceability: `TC-01:`, `M1:`, etc.

```
[ 1 / 9 ] TC-01: Creating test site 'selftest_a1b2c3d4'...
[ 5 / 11 ] TC-05: Process library items...
[ 7 / 25 ] M7: Full crawl...
```

### LOG-SC-04: Status Markers

Explicit markers for comparison and assertion results.

Comparison: `[equal]`, `[different]`
```
  [equal] Row count  Expected=14  Actual=14
  [different] Column count  Expected=5  Actual=4
```

Assertion: `[ok]`, `[fail]`
```
  [ok] All required fields present
  [fail] Missing 'created_date' column
```

### LOG-SC-05: Status Patterns

Consistent status keyword patterns:

- Success: `OK.` or `OK. 12 members resolved.`
- Failure: `FAIL: Validation failed -> Expected 5, got 4`
- Partial: `PARTIAL FAIL: 2 of 3 items processed, 1 failed.`
- Warning: `WARNING: 2 items skipped due to missing data.`
- Expected failure: `EXPECTED FAIL: (401) Unauthorized`
- Skip: `SKIP: Test requires database connection.`

### LOG-SC-06: Output Details

Enough detail to understand failures without additional investigation.

Item lists with references:
```
  3 items missing from output:
    Line 8: 'user_alpha@example.com'
    Line 15: 'user_beta@example.com'
```

Comparison details:
```
  [different] Column 'date_created' format
    Expected: 'YYYY-MM-DD'
    Actual: 'MM/DD/YYYY'
    Line 1: '03/04/2026' should be '2026-03-04'
```

Row/column counts:
```
  [equal] Row count: 523
  [different] Column count: Expected=8, Actual=7
    Missing column: 'last_modified'
```

### LOG-SC-07: Summary and Result

Always end with summary counts and final result.

Summary formats:
```
OK: X, FAIL: Y
OK: X, SKIP: Y, FAIL: Z
OK: X, EXPECTED FAIL: Y, SKIP: Z, FAIL: W
```

Final result: `RESULT: PASSED` | `RESULT: PASSED WITH WARNINGS` | `RESULT: FAILED`

Complete summary block:
```
===== SELFTEST COMPLETE =====
OK: 10, EXPECTED FAIL: 1, FAIL: 0
Test execution completed.
END: sites_security_scan_selftest() (12.0 secs).
```

Extended summary: Summary line before END footer, RESULT on final line before footer.

## Complete Examples

### Example 1: CRUD Selftest

```
START: sites_selftest()...

[ 1 / 9 ] TC-01: Creating test site 'selftest_a1b2c3d4'...
  OK.
[ 2 / 9 ] TC-02: Getting test site...
  OK.
[ 4 / 9 ] TC-04: Renaming test site 'selftest_a1b2c3d4' -> 'selftest_a1b2c3d4_renamed'...
  OK.
[ 5 / 9 ] TC-05: Deleting test site 'selftest_a1b2c3d4_renamed'...
  OK.
[ 9 / 9 ] TC-09: Cleaning up underscore folder...
  OK.

===== SELFTEST COMPLETE =====
OK: 9, FAIL: 0
END: sites_selftest() (5.0 secs).
```

### Example 2: Multi-Phase with Expected Fail

```
START: crawler_selftest()...

===== Phase 1: Configuration =====
[ 1 / 25 ] M1: Config validation - CRAWLER_SELFTEST_SHAREPOINT_SITE...
  OK. site_url='https://contoso.sharepoint.com/sites/SelftestSite'

===== Phase 4: Crawl Operations =====
[ 7 / 25 ] M7: Full crawl...
  OK. 5 files crawled in 4.2 secs.
[ 8 / 25 ] M8: Incremental crawl (no changes)...
  OK. 0 changes detected.

===== Phase 5: Error Handling =====
[ 11 / 25 ] M11: Access non-existent file (expected fail)...
  EXPECTED FAIL: (404) File not found
[ 12 / 25 ] M12: Handle rate limiting...
  OK. Retry succeeded after 2 attempts.

===== SELFTEST COMPLETE =====
OK: 24, EXPECTED FAIL: 1, FAIL: 0
Test execution completed.
END: crawler_selftest() (2 mins 3 secs).
```

### Example 3: Data Comparison

```
======================================= START: DATA EXPORT VALIDATION =======================================
Comparing exported CSV against expected output to verify field mapping and data integrity.

  Loading expected file 'expected_output.csv'...
    OK. 523 rows, 8 columns.
  Loading actual file 'actual_output.csv'...
    OK. 523 rows, 8 columns.

  [equal] Row count  expected=523  actual=523
  [equal] Column count  expected=8  actual=8
  [equal] Column names match
  [different] Column 'date_created' format  expected='YYYY-MM-DD'  actual='MM/DD/YYYY'

WARNING: Data matches but format differs.

3 validations run. OK: 2, WARNING: 1. Duration: 0.3s
RESULT: PASSED WITH WARNINGS
======================================== END: DATA EXPORT VALIDATION ========================================
```

### Example 4: Test with Failure

```
START: data_integrity_selftest()...

[ 1 / 5 ] TC-01: Load source data...
  OK. 1000 records loaded.
[ 3 / 5 ] TC-03: Validate schema...
  FAIL: Schema validation failed
    Missing required field: 'customer_id'
    Field 'order_date' has wrong type: expected 'date', got 'string'
    2 validation errors found.
[ 4 / 5 ] TC-04: Compare with expected output...
  SKIP: Skipping due to previous failure.
[ 5 / 5 ] TC-05: Cleanup test data...
  OK.

===== SELFTEST COMPLETE =====
OK: 3, SKIP: 1, FAIL: 1

Failure details:
  TC-03: Schema validation failed
    - Missing required field: 'customer_id'
    - Field 'order_date' has wrong type: expected 'date', got 'string'

END: data_integrity_selftest() (2.3 secs).
RESULT: FAILED
```

### Example 5: Permission Comparison

```
====================================== START: PERMISSION AUDIT COMPARISON ======================================

Loading baseline 'permissions_baseline.json'...
  156 permission entries.
Loading current 'permissions_current.json'...
  159 permission entries.

[different] Entry count  baseline=156  current=159

3 entries added in 'permissions_current.json':
  Line 157: user='new_user@company.com' site='ProjectA' level='Contribute'
  Line 158: user='contractor@external.com' site='ProjectB' level='Read'
  Line 159: group='External Partners' site='ProjectC' level='Read'

0 entries removed from 'permissions_baseline.json'.

2 entries modified (baseline -> current):
  Line 45: user='admin@company.com' level='Contribute' -> 'Full Control'
  Line 89: group='Site Members' members added 'new_member@company.com'

Comparison complete: 3 added, 0 removed, 2 modified.
RESULT: DIFFERENCES FOUND
======================================= END: PERMISSION AUDIT COMPARISON =======================================
```