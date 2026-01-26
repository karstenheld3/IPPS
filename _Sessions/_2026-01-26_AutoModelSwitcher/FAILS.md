# Session Failures

## AMSW-FL-004: Hardcoded crop coordinates fail on resolution/window changes

**Severity**: [CRITICAL]
**When**: 2026-01-26 11:16
**Where**: `DevSystemV3.2/skills/windsurf-auto-model-switcher/windsurf-model-registry.json:6-7`
**What**: Stored fixed crop coordinates (X=1570, Y=1070) that only work for one specific screen/window position

### Evidence
- User explicitly stated: "coordinates are different each time"
- Window can move, resolution can change
- Hardcoded values defeat the purpose of dynamic discovery

### Root Cause
- Did not listen to user's original requirement
- User said: "do first screenshot fullscreen then find position" - this means EVERY TIME
- I stored coordinates as static metadata instead of detecting dynamically

### Fix
1. Phase 1 ALWAYS takes fullscreen screenshot
2. Cascade analyzes and returns popup {x, y, width, height} as JSON
3. Script receives coordinates as parameters for Phase 2
4. NO hardcoded coordinates - always dynamic detection
5. Remove `_crop_area` from JSON - it's session-specific, not reusable

## AMSW-FL-003: Fullscreen screenshots waste tokens, truncated popup misses models

**Severity**: [HIGH]
**When**: 2026-01-26 11:05
**Where**: `DevSystemV3.2/skills/windsurf-auto-model-switcher/discover/capture-all-sections.ps1`
**What**: All screenshots are fullscreen, popup area is small, lower models truncated

### Evidence
- Screenshots ~400KB each, 10 screenshots = 4MB wasted
- Model selector popup is small area in corner, most of image is irrelevant
- Popup bottom is cut off, missing models from list
- User explicitly instructed: "first screenshot fullscreen to find position, then crop subsequent"

### Root Cause
- Did not implement user's two-phase approach
- Assumed full screen capture would work
- No detection of popup position/size
- No cropping to relevant area

### Fix
1. First screenshot: fullscreen to detect popup position
2. Cascade analyzes screenshot, returns {x, y, width, height} of popup
3. Subsequent screenshots: crop to popup area only
4. Smaller files, less tokens, complete model list

### Root Cause Analysis (Step 4)
**Problem**: Estimated coordinates based on scaled-down image display, not actual screen resolution.
- Screen: 2048x1280 actual
- Image displayed: ~1024x640 scaled
- My estimates: X=770, Y=555 (for scaled image)
- Actual needed: X=1570, Y=1070 (for real screen)

**Solution applied**:
1. Query screen resolution first: `[System.Windows.Forms.Screen]::PrimaryScreen.Bounds`
2. Zoom out with large crop area to locate popup
3. Progressively refine coordinates
4. Store working coordinates in JSON metadata for reuse

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
