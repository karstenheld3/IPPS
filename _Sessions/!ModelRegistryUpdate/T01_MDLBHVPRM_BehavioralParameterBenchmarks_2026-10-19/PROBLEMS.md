# Session Problems: Behavioral Parameter Benchmarks

**Doc ID**: MDLRGUP-MDLBHVPRM-PROBLEMS

Track problems using ID format: `MDLRGUP-MDLBHVPRM-PR-[NNNN]`

## Open

**MDLRGUP-MDLBHVPRM-PR-0001: No established benchmark directly measures "eagerness"**
- **History**: Added 2026-10-19 16:05
- **Description**: "Eagerness" (task scope completion 0.5-2.0) is a novel concept. No standard benchmark measures whether a model under-delivers or over-delivers relative to instructions. Need to find proxy benchmarks or composite scoring approaches.
- **Impact**: May need to derive eagerness from multiple indirect measures rather than a single benchmark
- **Next Steps**: Research over-generation, verbosity, task scope adherence, and "scope creep" in model outputs

**MDLRGUP-MDLBHVPRM-PR-0002: Mapping benchmark scores to custom scales**
- **History**: Added 2026-10-19 16:05
- **Description**: Most benchmarks use 0-100% or ELO ratings. Need methodology to map to our eagerness (0.5-2.0) and instruction_following (0.2-1.0) scales.
- **Impact**: Without clear mapping, benchmark data cannot populate model registry fields
- **Next Steps**: Define mapping functions as part of research output

## Resolved

(none)

## Deferred

(none)

## Problems Changes

**[2026-10-19 16:05]**
- Added: MDLRGUP-MDLBHVPRM-PR-0001 (no direct eagerness benchmark)
- Added: MDLRGUP-MDLBHVPRM-PR-0002 (score mapping methodology)
