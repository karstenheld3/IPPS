# Session Failures

## AMSW-FL-012: Misunderstood STRUT execution - modified document instead of executing plan

**Severity**: [HIGH]
**When**: 2026-01-26 14:36
**Where**: `_STRUT_TTV_DEMO.md` execution
**What**: User asked to execute STRUT plan. I modified the document and only completed P1 research instead of executing all 3 phases as written.

### Evidence
- User said "execute" - meant run the 3-phase workflow as-is
- I added research findings section, marked steps complete, modified structure
- Only executed P1, documented findings
- Did not execute P2 [DOCUMENT] or P3 [REVIEW] phases
- User feedback: "You modified the strut and only did the research part"

### Root Cause
- Misunderstood "execute STRUT" as "execute and document findings"
- Assumed I should improve/enhance the document during execution
- Did not read the STRUT structure carefully - it was a complete 3-phase plan meant to demonstrate model switching
- Treated it as a research task instead of a workflow demonstration

### Correct Approach
- Execute STRUT phases in order WITHOUT modifying the document structure
- Each phase runs its specified steps
- Mark deliverables complete as you go
- Do not add new sections or enhance content during execution
- The STRUT itself is the specification - follow it, don't improve it

### Fix
- Restore original STRUT document (or create new one)
- Execute all 3 phases in sequence
- Only mark checkboxes, don't restructure or add content

## AMSW-FL-011: Wrong assumption about screen resolution detection on Windows

**Severity**: [HIGH]
**When**: 2026-01-26 13:11
**Where**: `simple-screenshot.ps1`, inline PowerShell screenshot commands
**What**: Used `[System.Windows.Forms.Screen]::PrimaryScreen.Bounds` which returns logical pixels, not physical pixels on systems with DPI scaling

### Evidence
- Screen reported: 2048x1280 (logical)
- Actual physical: 2560x1600 (125% DPI scaling)
- Screenshots were cropped - missing bottom 320 pixels (20% of height)
- User pointed out bottom of screen was "MISSING" in captured images

### Root Cause
- Assumed .NET `Screen.Bounds` returns actual screen resolution
- Did not account for Windows DPI scaling (common: 125%, 150%, 200%)
- `CopyFromScreen` uses physical coordinates but was given logical dimensions

### Correct Approach
```powershell
# Get PHYSICAL resolution via Win32 API
Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public class ScreenMetrics {
    [DllImport("user32.dll")]
    public static extern IntPtr GetDC(IntPtr hwnd);
    [DllImport("user32.dll")]
    public static extern int ReleaseDC(IntPtr hwnd, IntPtr hdc);
    [DllImport("gdi32.dll")]
    public static extern int GetDeviceCaps(IntPtr hdc, int nIndex);
    public const int DESKTOPHORZRES = 118;  // Physical width
    public const int DESKTOPVERTRES = 117;  // Physical height
}
"@
$hdc = [ScreenMetrics]::GetDC([IntPtr]::Zero)
$physWidth = [ScreenMetrics]::GetDeviceCaps($hdc, 118)
$physHeight = [ScreenMetrics]::GetDeviceCaps($hdc, 117)
[ScreenMetrics]::ReleaseDC([IntPtr]::Zero, $hdc)
```

### Fix Applied
- Updated `simple-screenshot.ps1` to use Win32 `GetDeviceCaps` with `DESKTOPHORZRES`/`DESKTOPVERTRES`
- Now correctly captures 2560x1600 instead of 2048x1280

## AMSW-FL-010: Escape key does NOT close Windsurf model selector popup

**Severity**: [CRITICAL]
**When**: 2026-01-26 12:58
**Where**: Windsurf IDE model selector popup
**What**: Escape key does not close the model selector popup - confirmed by user testing manually

### Evidence
- Programmatic Escape (2x, 3x) does not close popup
- User confirmed: manual Escape press also does NOT close popup
- This is a Windsurf UI behavior, not a script issue

### Root Cause
- Windsurf model selector popup ignores Escape key
- Assumed Escape would work like standard VS Code quick pick

### Fix
- Need alternative close method:
  - Click outside popup area?
  - Different keyboard shortcut?
  - Tab to move focus?
  - Ctrl+Shift+F9 toggle (already tried - opens new popup instead)

## AMSW-FL-009: Created duplicate test scripts instead of using working one

**Severity**: [HIGH]
**When**: 2026-01-26 12:53
**Where**: `DevSystemV3.2/skills/windsurf-auto-model-switcher/sonnet 4.5.ps1`
**What**: Created separate test scripts with experimental code (mouse_event) instead of testing the actual `select-windsurf-model-in-ide.ps1` script that was proven to work

### Evidence
- Created `sonnet 4.5.ps1` with mouse click code that doesn't work
- Created `test-escape-fix.ps1`, `test-model-switch-with-click.ps1`, `test-tab-close.ps1`
- Original `select-windsurf-model-in-ide.ps1` was working, just needed 2x Escape fix
- Wasted time debugging scripts that shouldn't exist

### Root Cause
- Instead of fixing the original script, created copies to "test" changes
- Lost track of which script was being used
- Made changes to wrong files

### Fix
1. Delete all garbage test scripts
2. Use ONLY `select-windsurf-model-in-ide.ps1` for testing
3. Restore `auto-model-switch.ps1` from `.DISABLED`

## AMSW-FL-008: Assumed editing hooks.json would disable hook without Cascade restart

**Severity**: [HIGH]
**When**: 2026-01-26 12:49
**Where**: `.windsurf/hooks.json`
**What**: Edited hooks.json to disable hook, but Cascade doesn't reload config at runtime - hook kept running

### Evidence
- Renamed `post_cascade_response` to `post_cascade_response_DISABLED`
- Also added `exit 0` to auto-model-switch.ps1
- Popup kept appearing after every Cascade response
- Wasted 10+ minutes trying file-based disabling approaches

### Root Cause
- Assumed config files are hot-reloaded
- Cascade loads hooks.json at startup, not dynamically
- Didn't think about runtime vs startup configuration

### Fix
1. To disable hook during testing: **rename/delete the target script file** (not the config)
2. Or: restart Cascade to reload hooks.json
3. The `exit 0` in auto-model-switch.ps1 SHOULD work - verify script path is correct

## AMSW-FL-007: Documented hooks as "never triggered" when they work fine

**Severity**: [MEDIUM]
**When**: 2026-01-26 ~10:00
**Where**: `NOTES.md:66`, `PROBLEMS.md:58`, `PROGRESS.md:48`
**What**: Stated `post_cascade_response` hook "never triggered" when hook-log.txt shows 55+ successful triggers today

### Evidence
- `hook-log.txt`: 55 entries from 09:39:03 to 12:15:14
- NOTES.md line 66: "Hooks - [FAILED] `post_cascade_response` hook never triggered"
- PROGRESS.md line 48: "post_cascade_response hook - [TESTED] Never triggered"

### Root Cause
- Tested hook early in session, may have had configuration issue
- Did not re-verify when hook started working
- Documented initial failure without rechecking

### Impact
- Dismissed hook-based auto model switching as infeasible
- Wrote spec (CAMS-SP01) stating "Blocker for Phase 3: Cascade hooks don't trigger reliably"
- Hook-based approach IS viable but was ruled out based on incorrect info

### Fix
1. Update NOTES.md, PROBLEMS.md, PROGRESS.md to reflect hooks ARE working
2. Revisit CAMS-SP01 spec - hook-based Phase 3 may be feasible
3. Always re-verify "failed" findings before documenting as permanent blockers

## AMSW-FL-006: Generic file names instead of specific descriptive names

**Severity**: [LOW]
**When**: 2026-01-26 11:50
**Where**: `DevSystemV3.2/skills/windsurf-auto-model-switcher/`
**What**: Used generic names like `WORKFLOW.md`, `select-model.ps1` instead of specific names

### Evidence
- `WORKFLOW.md` - doesn't say what workflow
- `select-model.ps1` - doesn't say which product/context

### Root Cause
- Defaulted to short generic names
- Didn't consider that files may be referenced from other contexts

### Fix
- Rename to specific names:
  - `WORKFLOW.md` -> `UPDATE_WINDSURF_MODEL_REGISTRY.md`
  - `select-model.ps1` -> `select-windsurf-model-in-ide.ps1`

## AMSW-FL-005: Temporary screenshots committed to git

**Severity**: [MEDIUM]
**When**: 2026-01-26 11:18
**Where**: `DevSystemV3.2/skills/windsurf-auto-model-switcher/{shots,shots2,final,debug}/`
**What**: Committed ~40 temporary screenshot images to git instead of deleting after analysis

### Evidence
- 43 files changed in commit 26eb660
- Images are session-specific, not reusable
- Bloats repository unnecessarily

### Root Cause
- No cleanup step in workflow
- Forgot to add temp folders to .gitignore
- Did not delete images after extracting model data

### Fix
1. Delete all temp image folders from git
2. Add to .gitignore: `shots/`, `shots2/`, `final/`, `debug/`
3. Update script to auto-delete screenshots after successful extraction

## AMSW-FL-004: Hardcoded crop coordinates fail on resolution/window changes

**Severity**: [MEDIUM]
**When**: 2026-01-26 11:16
**Where**: `DevSystemV3.2/skills/windsurf-auto-model-switcher/windsurf-model-registry.json:6-7`
**What**: Stored fixed crop coordinates that only work for one specific screen/window position

### Evidence
- User explicitly stated: "coordinates are different each time"
- Window can move, resolution can change

### Root Cause
- Stored coordinates as static metadata instead of detecting dynamically
- Secondary issue: DPI scaling caused coordinate mismatch (see FL-011)

### Fix
- Use fullscreen capture approach
- Remove hardcoded `_crop_area` from JSON

## AMSW-FL-003: Truncated screenshots missing bottom of screen

**Severity**: [HIGH]
**When**: 2026-01-26 11:05
**Where**: Screenshot capture scripts
**What**: Screenshots were truncated, missing bottom portion of screen including model selector

### Evidence
- Screenshots captured at 2048x1280 but screen is 2560x1600
- Bottom ~320 pixels consistently missing
- User pointed out "MISSING" area at bottom of screenshots

### Root Cause
**CORRECTED**: This was NOT an LLM image scaling issue.
**ACTUAL CAUSE**: Windows DPI scaling (125%) causes `.NET Screen.Bounds` to return logical pixels (2048x1280) instead of physical pixels (2560x1600).

See FL-011 for the correct diagnosis and fix.

### Original Misdiagnosis (Wrong)
- Initially blamed LLM image scaling and grid coordinate detection
- Wasted time on cropping approaches when the real issue was DPI

### Fix
Use Win32 `GetDeviceCaps(DESKTOPHORZRES/DESKTOPVERTRES)` for physical resolution.

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
