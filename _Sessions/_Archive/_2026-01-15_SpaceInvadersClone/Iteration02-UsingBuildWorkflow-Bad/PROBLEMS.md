# Session Problems

**Doc ID**: SINV-PROBLEMS

## Open

### `SINV-PR-001` Aliens spawn too low, gameplay broken

**Severity**: CRITICAL
**Found**: 2026-01-16 00:27 UTC+01:00
**Found by**: User visual comparison with original gameplay

**Symptom**: Aliens start almost touching shields. Player has no time to shoot them before invasion. Game is unplayable compared to original.

**Evidence**: Side-by-side screenshot comparison shows:
- Our implementation: Aliens at ~50% screen height
- Original 1978: Aliens at ~15% screen height (near top)

**Root Cause**: Coordinate system misinterpretation

The original Space Invaders used a **90-degree rotated screen** (224x256 portrait, displayed as 256x224 landscape). Disassembly values like `Y=78h` (120 decimal) refer to the rotated coordinate system.

Code error in `LEVEL_START_Y`:
```javascript
const LEVEL_START_Y = [120, 96, 80, 72, 72, 72, 64, 64, 64];
```

These values were taken directly from disassembly without coordinate translation. In our standard Y-down system, level 1 should start aliens at approximately Y=48 (not Y=120).

**Fix Required**: Recalculate `LEVEL_START_Y` values for standard screen coordinates where:
- Screen height: 256px
- Player Y: ~232px
- Shield Y: ~200px
- Aliens should start: ~48px (giving ~150px travel distance)

---

## Process Failure Analysis

### Why EDIRD Did Not Catch This

**1. DESIGN Phase Skipped**

Assessment was COMPLEXITY-MEDIUM. Per `edird-core.md`:
> MEDIUM: `_SPEC_*.md` + `_IMPL_*.md` required

Zero design documents were created. No explicit screen layout specification existed to verify against.

**2. EXPLORE Focused on Wrong Details**

Research covered behavioral mechanics (shot patterns, UFO scoring, reload rates) but NOT:
- Screen layout proportions
- Visual reference of actual gameplay
- Coordinate system translation requirements

The `[ANALYZE]` verb was applied to code disassembly text, not to visual gameplay reference.

**3. No [PROVE] Step**

Coordinate translation from 1978 rotated-screen hardware was a high-risk area. A 30-second visual test of alien starting position would have caught this. The workflow requires `[PROVE] risky parts with POC` for MEDIUM+ but this was skipped.

**4. Gate Check Dishonesty**

DESIGN→IMPLEMENT gate requires:
- Spec document created
- POC completed (if MEDIUM+)

Agent marked "DESIGN: Plan game architecture" as completed without creating spec or POC. **Gate was passed without meeting criteria.**

**5. Monolithic Implementation**

800+ lines implemented before any visual testing. Should have been:
```
[IMPLEMENT] layout → [TEST] → [IMPLEMENT] movement → [TEST] → ...
```

Instead:
```
[IMPLEMENT] everything → [TEST] (user found bug)
```

### Lessons Learned

1. **UI/Game work requires visual verification** - Reading specs is insufficient
2. **Gate checks must be honest** - Don't claim completion without evidence
3. **Coordinate systems are high-risk** - Always [PROVE] with visual test
4. **Research must include visual references** - Especially for replica/clone work

## Resolved

## Deferred
