# Session Problems

**Doc ID**: 2026-03-19_MinimalIPPS-PROBLEMS

## Open

**MIPPS-PR-0001: IPPS system too large for less expensive LLMs**
- **History**: Added 2026-03-19 22:58
- **Description**: Current DevSystem is ~1MB text, too complex for cheaper/smaller LLMs
- **Impact**: Cannot use cost-effective models for IPPS-based workflows
- **Next Steps**: Execute 7-step compression plan

**MIPPS-PR-0002: Unknown file loading dependencies**
- **History**: Added 2026-03-19 22:58
- **Description**: Need to map which files load which other files (call tree)
- **Impact**: Cannot optimize without understanding load patterns
- **Next Steps**: Create _01_FILE_CALL_TREE.md

**MIPPS-PR-0003: Unknown file complexity distribution**
- **History**: Added 2026-03-19 22:58
- **Description**: Need to measure tokens, concepts, rules, branching per file
- **Impact**: Cannot prioritize compression targets
- **Next Steps**: Create _02_FILE_COMPLEXITY_MAP.md

**MIPPS-PR-0004: No compression strategy defined**
- **History**: Added 2026-03-19 22:58
- **Description**: Need to classify content as Primary/Secondary/Drop
- **Impact**: Cannot systematically compress without strategy
- **Next Steps**: Create _03_FILE_COMPRESSION_STRATEGY.md

**MIPPS-PR-0005: No compression prompts exist**
- **History**: Added 2026-03-19 22:58
- **Description**: Need up to 10 prompts for different file types with eval criteria
- **Impact**: Cannot automate compression
- **Next Steps**: Create prompts after strategy is defined

**MIPPS-PR-0006: No automated compression pipeline**
- **History**: Added 2026-03-19 22:58
- **Description**: Need script similar to llm-transcription for batch processing
- **Impact**: Manual compression would be too slow
- **Next Steps**: Create script after prompts are defined

**MIPPS-PR-0007: No verification process for compressed files**
- **History**: Added 2026-03-19 22:58
- **Description**: Need to verify each compressed file against original
- **Impact**: Cannot ensure quality without verification
- **Next Steps**: Create _04_FILE_COMPRESSION_REPORT.md after compression

## Resolved

(none yet)

## Deferred

(none yet)

## Problems Changes

**[2026-03-19 22:58]**
- Added: MIPPS-PR-0001 through MIPPS-PR-0007 (derived from 7-step plan)
