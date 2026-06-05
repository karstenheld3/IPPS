# Session Failures

## TRVL-FL-001: Skill files created in wrong location

**Severity:** [HIGH]
**When:** 2026-03-04 15:50
**Where:** `.windsurf/skills/travel-info/` (wrong)

**What happened:**
Created 14 skill files directly in `.windsurf/skills/travel-info/` instead of `[DEVSYSTEM_FOLDER]/skills/travel-info/` (DevSystemV3.3/skills/travel-info/).

**Evidence:**
- Files exist in `E:\Dev\IPPS\.windsurf\skills\travel-info\`
- Should be in `E:\Dev\IPPS\DevSystemV3.3\skills\travel-info\`

**Root cause:**
- SPEC had `Target file: .windsurf/skills/travel-info/SKILL.md`
- Agent followed spec literally without checking `!NOTES.md` workspace rules
- `!NOTES.md` clearly states: "NEVER create or edit directly in `.windsurf/`"

**What should have happened:**
1. Read `!NOTES.md` before implementation
2. Note that `[DEVSYSTEM_FOLDER]` is the source, `.windsurf/` is sync target
3. Create files in `DevSystemV3.3/skills/travel-info/`
4. Sync to `.windsurf/` after

**Fix:**
1. Move files from `.windsurf/skills/travel-info/` to `DevSystemV3.3/skills/travel-info/`
2. Update SPEC target path
3. Run sync to populate `.windsurf/`

**Prevention:**
- Always read `!NOTES.md` before `/implement`
- Check for `[DEVSYSTEM_FOLDER]` references
- Never create skills/workflows/rules directly in `.windsurf/`

**Status:** Resolved - Files moved to DevSystemV3.3/skills/travel-info/
