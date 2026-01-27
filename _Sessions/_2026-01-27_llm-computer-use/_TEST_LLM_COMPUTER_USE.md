# TEST: LLM Computer Use v2

**Doc ID**: LLMCU-TP01
**Goal**: Verify llm_computer_use_v2 package functionality
**Timeline**: Created 2026-01-27, Updated 0 times
**Target file**: `poc/llm_computer_use_v2/`

**Depends on:**
- `_SPEC_LLM_COMPUTER_USE.md [LLMCU-SP01]` for requirements

## MUST-NOT-FORGET

- All tests run in dry-run mode by default (safe)
- API tests cost ~$0.01 each
- Tests should not interfere with user's desktop

## Table of Contents

1. [Overview](#1-overview)
2. [Test Strategy](#2-test-strategy)
3. [Test Priority Matrix](#3-test-priority-matrix)
4. [Test Cases](#4-test-cases)
5. [Verification Checklist](#5-verification-checklist)
6. [Document History](#6-document-history)

## 1. Overview

Tests for the minimal v2 package (3 files: __init__.py, core.py, cli.py).

## 2. Test Strategy

**Approach**: CLI-based integration tests

**Phases:**
1. Module import tests (no API)
2. CLI flag tests (no API)
3. API integration tests (costs money)

## 3. Test Priority Matrix

### MUST TEST

- **CLI --version** - Version flag works
- **CLI --help** - Help displays correctly
- **CLI no args** - Shows help, exits 0
- **ScreenCapture** - Screenshot capture works
- **API describe** - Simple describe task completes
- **API click** - Click action in dry-run

### SHOULD TEST

- **Cost estimation** - Cost calculated correctly
- **Duration tracking** - Timing measured
- **Session logging** - --save-log creates file

### DROP

- **Execute mode** - Requires actual mouse control
- **High-risk detection** - Tested via code review
- **Multi-monitor** - Not implemented

## 4. Test Cases

### Category: CLI Flags (3 tests)

- **LLMCU-TC-01**: `--version` -> ok=true, shows "0.4.0"
- **LLMCU-TC-02**: `--help` -> ok=true, shows usage
- **LLMCU-TC-03**: no args -> ok=true, shows help

### Category: Module Import (2 tests)

- **LLMCU-TC-04**: Import ScreenCapture -> ok=true, class available
- **LLMCU-TC-05**: Import AgentSession -> ok=true, class available

### Category: Screenshot (2 tests)

- **LLMCU-TC-06**: capture_for_api() -> ok=true, returns dict with base64
- **LLMCU-TC-07**: get_display_info() -> ok=true, returns monitor info

### Category: API Integration (3 tests)

- **LLMCU-TC-08**: Describe task -> ok=true, status=completed, actions=0
- **LLMCU-TC-09**: Click task -> ok=true, actions>=1, dry_run=true
- **LLMCU-TC-10**: Save log -> ok=true, creates JSON file

## 5. Verification Checklist

- [x] LLMCU-TC-01: --version shows 0.4.0
- [x] LLMCU-TC-02: --help shows usage
- [x] LLMCU-TC-03: no args shows help
- [x] LLMCU-TC-04: ScreenCapture imports
- [x] LLMCU-TC-05: AgentSession imports
- [x] LLMCU-TC-06: capture_for_api works (284920 bytes, 1568x980)
- [x] LLMCU-TC-07: get_display_info works (monitor_count=1)
- [x] LLMCU-TC-08: Describe task completes (status=completed)
- [x] LLMCU-TC-09: Click task dry-run works (actions=1, coord=21,851)
- [x] LLMCU-TC-10: Save log creates file (session_*.json)

**All 10 tests PASSED**

## 6. Document History

**[2026-01-27 20:31]**
- All 10 test cases executed and passed
- Checklist updated with results

**[2026-01-27 20:30]**
- Initial test plan created
- 10 test cases defined
