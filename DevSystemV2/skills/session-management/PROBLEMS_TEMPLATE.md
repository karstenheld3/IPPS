# Session Problems

Track problems discovered during this session using ID format: `[TOPIC]-PR-[NNN]`

## Open

**AUTH-PR-001: Race condition on simultaneous token refresh**
- **Description**: Multiple API requests trigger token refresh at the same time, causing duplicate refresh calls
- **Impact**: Server rate-limits refresh endpoint, causing 429 errors and failed requests
- **Next Steps**: Implement mutex/lock pattern to ensure only one refresh happens at a time

**API-PR-002: Clock skew causes premature token expiration**
- **Description**: Client-side expiration check uses local time, which may be out of sync with server
- **Impact**: Valid tokens rejected as expired, or expired tokens used causing 401 errors
- **Next Steps**: Use server time from response headers or implement server-side expiration check

## Resolved

**AUTH-PR-003: Refresh token stored in localStorage** - RESOLVED
- **Solution**: Migrated to secure httpOnly cookie storage with SameSite=Strict
- **Verification**: Tested XSS attack vectors, confirmed token not accessible from JavaScript

## Deferred

**API-PR-004: No retry logic for network failures** - DEFERRED
- **Reason**: Requires broader error handling refactor, not critical for current session goal
- **Next**: Implement exponential backoff retry in separate session after auth fixes are stable
