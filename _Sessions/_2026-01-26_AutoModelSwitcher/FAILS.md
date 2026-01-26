# Session Failures

## AMSW-FL-001: Clipboard anti-pattern in list-models.ps1

**Severity**: [MEDIUM]
**When**: 2026-01-26 10:28
**Where**: `DevSystemV3.2/skills/windsurf-auto-model-switcher/list-models.ps1`
**What**: Used clipboard (Ctrl+C/V) to read model names from UI

### Evidence
- Script cycles endlessly due to unreliable clipboard reading
- No way to verify if clipboard content matches current UI selection
- Clipboard can be overwritten by other processes

### Root Cause
- Assumed clipboard was reliable way to read UI content
- No visual feedback to user about progress
- No proper termination condition (duplicate detection unreliable)

### Fix
1. Remove clipboard usage
2. Add progress indicator for each section
3. Save results incrementally
4. Stop when reaching bottom (detect "No results" or empty section)
5. Allow user to cancel with Ctrl+C
