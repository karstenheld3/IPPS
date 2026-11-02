# Session Problems: Model Registry Update

**Doc ID**: MDLRGUP-PROBLEMS

**Purpose**: Problem tracking for session `!ModelRegistryUpdate`. ID format: `MDLRGUP-PR-[NNNN]`

## Table of Contents

- [Open](#open)
- [Resolved](#resolved)
- [Deferred](#deferred)
- [Problems Changes](#problems-changes)

## Open

- **[2026-11-02 15:00] MDLRGUP-PR-0001**: Silent-source ties from 2026-11-02 PRICES run (`gpt-rosalind-discovery = gpt-rosalind-research`, `gpt-4-turbo-2024-04-09 = gpt-4o`, `gpt-4-0613 = gpt-4.1`). Vendor sources are silent on escalation/dominance; recorded as ties in `2026-11-02_Depth-Edges.json` per EC-1..EC-4 rules until vendor model guidance publishes explicit ranking.
- **[2026-11-02 15:00] MDLRGUP-PR-0002**: Report-only ECI interval inconsistencies on 6 existing models after 2026-11-02 Epoch ECI CSV refresh (`o4-mini` D4 vs `o1` D4, `claude-opus-4-8` D8 vs `grok-4.7` D8, `claude-haiku-5-5` D8 vs `grok-4.7` D8, `gpt-6.1-terra` D9 vs `gpt-5.4-pro` D9, `gpt-6.1-terra` D9 vs `gpt-5.5` D9, `gpt-6.1-terra` D9 vs `gpt-5.6-terra` D9). Kept at established rungs per append-only invariant (NFR-01); monitor next IRT refit.

## Resolved

(none)

## Deferred

(none)

## Problems Changes

**[2026-11-02 15:00]**
- Added: `MDLRGUP-PR-0001` (silent-source ties from 2026-11-02 PRICES run)
- Added: `MDLRGUP-PR-0002` (report-only ECI interval inconsistencies on existing models)
