# Failure Log

**Goal**: Document failures, mistakes, and lessons learned to prevent repetition

## Table of Contents

1. [Active Issues](#active-issues)
2. [Resolved Issues](#resolved-issues)
3. [Document History](#document-history)

## Active Issues

### 2026-01-22 - Agent Workflow Error

#### [LOW] `LLMEV-FL-005` Writing FL entries to wrong file

- **When**: 2026-01-22 21:03
- **Where**: `/fail` workflow execution
- **What**: Agent wrote FL (failure log) entries to PROBLEMS.md instead of FAILS.md
- **Why it went wrong**: Confused PROBLEMS.md (for tracking session problems) with FAILS.md (for lessons learned)
- **Evidence**: PROBLEMS.md contains FL-001 through FL-004 entries
- **Suggested fix**: Always check /fail workflow Step 7 - SESSION-FIRST rule specifies `[SESSION_FOLDER]/FAILS.md`

## Resolved Issues

### 2026-01-22 - Agent Workflow Error

#### [RESOLVED] `LLMEV-FL-006` Editing .windsurf directly instead of DevSystemV3.2

- **Original severity**: [LOW]
- **Resolved**: 2026-01-22 21:11
- **Solution**: Reverted .windsurf changes, updated DevSystemV3.2 first, then synced
- **Link**: Commit pending

### 2026-01-22 - Spec Refinement

#### [RESOLVED] `LLMEV-FL-004` Implicit Dependencies and File Types

- **Original severity**: [MEDIUM]
- **Resolved**: 2026-01-22 21:02
- **Solution**: Made file types explicit in all parameter descriptions
- **Link**: Commit `07b6318`

#### [RESOLVED] `LLMEV-FL-003` Parameter Names Not Explicit Enough

- **Original severity**: [LOW]
- **Resolved**: 2026-01-22 20:58
- **Solution**: `--keys` -> `--keys-file`, `--json` -> `--write-json-metadata`
- **Link**: Commit `07b6318`

#### [RESOLVED] `LLMEV-FL-002` Overengineering - Redundant Parameters

- **Original severity**: [MEDIUM]
- **Resolved**: 2026-01-22 20:57
- **Solution**: Removed `--system-prompt`, `--user-prompt`, `--questions-per-item`, `--max-tokens`
- **Link**: Commit `07b6318`

#### [RESOLVED] `LLMEV-FL-001` Ambiguous Script and Parameter Naming

- **Original severity**: [MEDIUM]
- **Resolved**: 2026-01-22 20:54
- **Solution**: Applied consistent naming convention - call-llm.py, call-llm-batch.py, generate-answers.py
- **Link**: Commit `07b6318`

## Document History

**[2026-01-22 21:03]**
- Added: LLMEV-FL-005 for wrong file usage
- Moved: FL-001 to FL-004 from PROBLEMS.md (resolved)

