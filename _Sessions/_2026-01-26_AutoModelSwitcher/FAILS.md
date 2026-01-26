# Session Failures

## AMSW-FL-002: Hardcoded model mapping defeats discovery purpose

**Severity**: [MEDIUM]
**When**: 2026-01-26 10:33
**Where**: `DevSystemV3.2/skills/windsurf-auto-model-switcher/list-models.ps1:28-120`
**What**: Created "discovery" script with 100% hardcoded data - no actual discovery happens

### Evidence
- Script has 90-line `$modelMapping` hashtable with all model names and costs
- Protobuf file only provides model IDs, not display names or costs
- Running script just outputs the hardcoded data with extra steps
- User question: "if we already know everything why run the script?"

### Root Cause
- Misunderstood the goal: thought "extract from pb" meant "map IDs to known names"
- Protobuf binary has no schema - cannot extract display names or costs from it
- Tried to "solve" missing data by hardcoding instead of acknowledging limitation

### Fix
Options:
1. **Delete script, ship static `models.json`** - Honest about what we have
2. **UI scraping with Playwright** - Actually discover data dynamically
3. **ID-only extraction** - Script finds new IDs, manual cost updates

Recommended: Option 1 (static JSON) unless dynamic discovery is truly needed

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
