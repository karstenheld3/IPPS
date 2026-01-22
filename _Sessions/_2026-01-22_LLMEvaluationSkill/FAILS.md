# Failure Log

**Goal**: Document failures, mistakes, and lessons learned to prevent repetition

## Table of Contents

1. [Active Issues](#active-issues)
2. [Resolved Issues](#resolved-issues)
3. [Document History](#document-history)

## Active Issues

### `LLMEV-FL-009` Ignored documented settings in NOTES.md

- **Severity**: [MEDIUM]
- **When**: 2026-01-22 23:03
- **Where**: Agent command execution for test runs
- **What**: Agent repeatedly used `--workers 2` instead of `--workers 4` despite NOTES.md clearly specifying "Workers: 4 parallel" in Test Configuration section
- **Evidence**: User had to stop agent multiple times and explicitly point to NOTES.md:L65 showing "Workers: 4 parallel"
- **Why it went wrong**: Agent used hardcoded value from memory instead of reading current NOTES.md settings before executing commands
- **Suggested fix**: Before running test commands, always read NOTES.md Test Configuration section and use those exact values

## Resolved Issues

### 2026-01-22 - Wrong Location

#### [RESOLVED] `LLMEV-FL-008` Created skill in .windsurf instead of DevSystemV3.2

- **Original severity**: [HIGH]
- **When**: 2026-01-22 21:45 during `/implement` workflow
- **Where**: Entire `llm-evaluation` skill folder
- **What**: Created skill directly in `.windsurf/skills/llm-evaluation/` instead of source location `DevSystemV3.2/skills/llm-evaluation/`
- **Why it went wrong**: Did not check workspace structure; assumed .windsurf was the source location
- **Resolved**: 2026-01-22 22:02
- **Solution**: Copied skill folder to `DevSystemV3.2/skills/llm-evaluation/`

### 2026-01-22 - Implementation Bug

#### [RESOLVED] `LLMEV-FL-007` Transcription matching loaded empty .meta.json files

- **Original severity**: [MEDIUM]
- **When**: 2026-01-22 21:53 during API testing
- **Where**: `generate-answers.py` lines 213-231
- **What**: Script matched `sample_document_summary.meta.json` (empty text field) instead of actual transcription JSON, resulting in 0 answers generated
- **Why it went wrong**: No filtering for `_*` files, `.meta.*` files, or empty content when loading transcriptions
- **Resolved**: 2026-01-22 21:57
- **Solution**: Added filters to skip `_*` files, `.meta.*` files, and only include non-empty content
- **Link**: Commit `6f12e2e`

### 2026-01-22 - Agent Workflow Error

#### [RESOLVED] `LLMEV-FL-005` Writing FL entries to wrong file

- **When**: 2026-01-22 21:03
- **Where**: `/fail` workflow execution
- **What**: Agent wrote FL (failure log) entries to PROBLEMS.md instead of FAILS.md
- **Why it went wrong**: Confused PROBLEMS.md (for tracking session problems) with FAILS.md (for lessons learned)
- **Evidence**: PROBLEMS.md contains FL-001 through FL-004 entries
- **Suggested fix**: Always check /fail workflow Step 7 - SESSION-FIRST rule specifies `[SESSION_FOLDER]/FAILS.md`

### 2026-01-22 - Spec Refinement

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

**[2026-01-22 23:05]**
- Added: LLMEV-FL-009 for ignoring documented settings

**[2026-01-22 22:00]**
- Added: LLMEV-FL-007 for transcription matching bug (resolved)
- Moved: FL-005 to resolved

**[2026-01-22 21:03]**
- Added: LLMEV-FL-005 for wrong file usage
- Moved: FL-001 to FL-004 from PROBLEMS.md (resolved)

