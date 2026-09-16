# INFO: How to Optimize Development Tests for Agentic Workflows

**Doc ID**: DEVTESTS-IN01
**Goal**: Document patterns for structuring and running large test suites in agentic development workflows so that hundreds of tests execute fast, produce token-efficient output, and integrate cleanly with prompt sequences
**Timeline**: Created 2026-09-16, Updated 1 time (2026-09-16 - 2026-09-16)

## Summary

- **pytest `-q` mode with `--no-header -p no:cacheprovider` produces one character per test** - hundreds of tests render as a single line of dots, `x`, `s`, and `F` markers, keeping agent context usage near zero [VERIFIED]
- **`pytest-xdist` with `-n auto` cuts wall time proportionally to CPU cores** - 10 min serial suite becomes 2-3 min parallel; no test isolation changes needed when tests use `tmp_path` [VERIFIED]
- **strict xfail records defects without blocking the suite** - `@pytest.mark.xfail(strict=True, reason="BUG-ID")` lets tests document expected failures; the test fails if the bug is silently fixed, forcing marker removal [VERIFIED]
- **Parallel test-writing tracks with disjoint file ownership prevent merge conflicts** - five agent sessions write tests simultaneously because each track owns exclusive file lists, shares only a read-only contract, and defers fixes to a sequential phase [VERIFIED]
- **A robustness card prevents agent hangs during test execution** - banned commands, time caps, on-cap kill procedures, and stray-process sweeps encoded in a single card that every prompt loads [VERIFIED]
- **Mock transport with scripted behaviours eliminates live API costs from the test suite** - fault injection (429, 503, timeout, hang, truncation, garbage) proves resilience without spending money [VERIFIED]
- **Reference-run comparison replaces assertion-heavy test code** - a fault-free run's file-tree hash and call log become the reference; every recovery test asserts tree-hash equality, not individual file contents [VERIFIED]

## Table of Contents

- [Summary](#summary)
- [1. The Token-Efficient Test Runner](#1-the-token-efficient-test-runner)
- [2. Parallel Execution with pytest-xdist](#2-parallel-execution-with-pytest-xdist)
- [3. The xfail-First Defect Protocol](#3-the-xfail-first-defect-protocol)
- [4. Parallel Test-Writing Tracks](#4-parallel-test-writing-tracks)
- [5. Robustness Card for Test Execution](#5-robustness-card-for-test-execution)
- [6. Mock Transport and Fault Injection](#6-mock-transport-and-fault-injection)
- [7. Reference-Run Comparison](#7-reference-run-comparison)
- [8. Test Suite Structure and Naming](#8-test-suite-structure-and-naming)
- [9. Cost Reference Profiles](#9-cost-reference-profiles)
- [10. Integration with Prompt Sequences](#10-integration-with-prompt-sequences)
- [Sources](#sources)
- [Next Steps](#next-steps)
- [Document History](#document-history)

## 1. The Token-Efficient Test Runner

Running hundreds of tests inside an agent session burns context tokens on test output. The standard pytest verbose mode (`-v`) produces one line per test - 300 tests produce 300 lines of output. That output is rarely useful when tests pass; it becomes critical only when they fail.

**The solution**: pytest quiet mode with cache and header suppression.

```
python -m pytest tests/ --no-header -p no:cacheprovider -q -n auto
```

This produces output like:

```
bringing up nodes...
..........................x.x......xx.x..xx.......F...xxx..xx.xxxF...xxx.x.xx.x...... [ 82%]
```

Each character encodes exactly one Test Case (TC) result:
- `.` = passed
- `x` = expected failure (xfail)
- `s` = skipped
- `F` = unexpected failure

**Why each flag matters:**
- `-q` (quiet): one character per test instead of one line; failure details still printed at the end
- `--no-header`: suppresses the pytest version and plugin banner (3-5 lines saved)
- `-p no:cacheprovider`: suppresses the `.pytest_cache/` directory and "no tests ran" cache messages; prevents file system clutter in work folders
- `-n auto`: parallel execution via pytest-xdist (see Section 2)

**Token budget**: a 300-test suite in quiet mode produces approximately 5 lines of output (progress bar, percentage, summary). Verbose mode would produce 300+ lines. For an agent consuming test output as context, this is a 60x reduction.

**Failure output is preserved**: quiet mode still prints full tracebacks for failed tests at the end. The agent sees the compact progress bar during execution and the detailed failure information only when something breaks - exactly the right information at the right time.

## 2. Parallel Execution with pytest-xdist

Serial test execution on a large suite (300+ tests with subprocess spawning, file I/O, and mock HTTP) can take 10+ minutes. The `-n auto` flag uses `pytest-xdist` to distribute tests across all CPU cores.

**Prerequisites:**
- Install: `pip install pytest-xdist` (also available in most Continuous Integration (CI) images)
- Tests must use `tmp_path` (pytest built-in) for all file I/O - each test gets its own temporary directory
- Tests must not share mutable global state across test functions
- Tests must not depend on execution order

**Performance**: a 10-minute serial suite drops to 2-3 minutes with `-n auto` on an 8-core machine. The `bringing up nodes...` line in the output confirms parallel execution is active.

**Caveat**: do not pipe parallel test output through `| Select-Object` or similar PowerShell streaming commands. These buffer the entire output before processing, which appears to hang. Read the output directly or redirect to a file.

## 3. The xfail-First Defect Protocol

In agentic development, test-writing and implementation often happen in separate agent sessions. A test track that discovers an implementation defect cannot fix it (the fix might break other tracks running in parallel). The xfail protocol solves this.

**The pattern:**

```python
@pytest.mark.xfail(strict=True, reason="PROJ-BG-0142")
def test_tc_042_crash_recovery_render():
  """TC-42: Recovery after crash during render stage."""
  # ... test code that currently fails due to implementation defect ...
```

**Why `strict=True` matters**: a strict xfail makes the test fail if it unexpectedly passes. This forces the developer to remove the marker when the bug is fixed. Without `strict=True`, a silently fixed bug would leave a dead marker - the test would pass as "xpass" and nobody would notice the marker is stale.

**The workflow:**

```
[TEST TRACK]                    [FIX PHASE]
Write test                      Read xfail reason (BG-0142)
Test fails on defect             Find root cause in implementation
Mark xfail(strict, BG-0142)     Fix the defect
Record in status file            Remove the xfail marker
Continue to next TC              Run test - now passes as green
```

**In the test output**, xfailed tests appear as `x` characters. The count of `x` markers equals the number of known defects. After the fix phase, the xfail count drops to zero (or to the count of deferred bugs requiring user consultation).

**Bug ID linkage**: the `reason` string contains a trackable bug ID (e.g., `PROJ-BG-0142`). The same ID appears in `PROBLEMS.md`. A grep for the ID finds: the test marker, the PROBLEMS entry, and the fix commit message. Full traceability from test to bug to fix.

## 4. Parallel Test-Writing Tracks

When a test suite has 150+ test cases across 16 categories, a single agent session writing all tests sequentially takes hours. The solution: partition test categories into parallel tracks, each running in its own agent session.

**The structure** (observed in the TRNSKILRW session):

```
Track T1: backend faults + quality loop    (TC-23..TC-40, TC-89..TC-100)
Track T2: crashes + locks                  (TC-41..TC-54, TC-55..TC-63)
Track T3: resume + batching + boundaries   (TC-64..TC-79, TC-80..TC-88, TC-140..TC-147)
Track T4: assembly + CLI + concurrency     (TC-101..TC-114, TC-115..TC-134)
Track T5: cost guard + pairwise            (TC-148..TC-158)
```

**Parallel execution guarantees (PG) that prevent interference:**

- **PG-01 Disjoint file ownership**: each track has an explicit list of files it may create or edit. No file appears in two lists
- **PG-03 Own tests only**: a track runs only its own test files. The full suite runs at barriers
- **PG-07 Test-write and fix separation**: test tracks never edit implementation code. A failing test is xfailed, not fixed
- **PG-05 No commits**: tracks do not commit. The barrier collects all work and commits once
- **PG-08 Shared read-only artefacts**: fixtures and references written before the parallel phase are read-only during it

**The barrier**: after all tracks report `Status: done`, a sequential barrier prompt collects defects into `PROBLEMS.md`, runs the full suite, verifies xfail counts match finding counts, and commits everything atomically.

**Why this works for agents**: each track's prompt is self-contained. It reads the test plan, the robustness card, and the implementation contracts. It writes its test files and a status file. No coordination with other tracks is needed during execution.

## 5. Robustness Card for Test Execution

Agents running test suites can hang on commands that wait for stdin, pagers, or unbounded streams. A robustness card is a dedicated document (`__CARD_01-Robustness.md`) loaded by every prompt that prevents these failures.

**The card contains four sections:**

**Banned commands** - commands known to hang in this stack:
- `| Select-Object` on test output (buffers indefinitely)
- `git log` without `--no-pager` (launches pager)
- `pytest` without a file scope in implementation prompts (full suite only in final verification)
- Any command that waits for stdin (`Read-Host`, `pause`, etc.)

**Time caps** - per command type:
- Single test file: 3 min cap
- Full suite: 15 min cap
- Nightly variant: 30 min cap
- Git operations: 30 s cap

**Always rules** - positive requirements:
- Tests always run with `-q -x --no-header -p no:cacheprovider`
- After every test run: verify no stray python processes remain (`Get-Process python*`)

**On-cap behaviour** - what to do when a cap is exceeded:
1. Kill the process tree (children first)
2. Record command, cap, and last 20 output lines in `PROBLEMS.md`
3. Continue with the next step
4. Same command hits the cap twice: stop the prompt, record as `blocked`

**Why this prevents cost overruns**: without the card, an agent hitting a hanging `pytest` run will wait indefinitely, burning API tokens on an idle context window. The card's time caps and kill procedures give the agent a deterministic recovery path.

## 6. Mock Transport and Fault Injection

Testing a pipeline that makes paid API calls requires a mock transport layer. The TRNSKILRW project uses `httpx.MockTransport` with scripted behaviours.

**The behaviour vocabulary:**

```
ok                    - valid response with correct envelope
http:429:retry-after=2 - rate limit with Retry-After header
http:503              - server error (retryable)
timeout               - no byte within --timeout (simulated via FakeClock)
hang                  - idle timeout fires
reset                 - connection dropped mid-body
garbage               - plain text, no envelope markers
truncate:<n>          - body cut at n characters (finish_reason: length)
drop-page:<id>        - valid envelope but missing a page
dup-page:<id>         - duplicate DOCUMENT block for same page
refuse                - model refuses the request
```

**FakeClock injection**: time-dependent tests (backoff, timeout, hang detection) inject a `FakeClock` that advances without waiting. `--timeout 1` with `FakeClock` means the test completes in milliseconds while proving the timeout logic works correctly. No `time.sleep()` in tests.

**Zero live calls**: every automated test runs against the mock transport. The mock transport is activated via environment variable (`TRANSCRIBE_TEST_TRANSPORT` pointing at a behaviour JSON file). A run without this variable and without API keys must fail fast with exit 1, never hang.

## 7. Reference-Run Comparison

Instead of asserting individual file contents in every test, the TRNSKILRW project uses reference-run comparison.

**The pattern:**

```
┌─────────────────────┐
│ 1. REFERENCE RUN    │  Fault-free run on fixture
│   (once per fixture)│
├─────────────────────┤
│ Record:             │
│  - file-tree hash   │
│  - call log         │
│  - cost profile     │
└────────┬────────────┘
         │ stored in tests/fixtures/reference/
         v
┌─────────────────────┐     ┌─────────────────────┐
│ 2. FAULT RUN        │────>│ 3. RECOVERY RUN     │
│    (inject fault)   │     │    (same cmd, no    │
│                     │     │     fault)          │
├─────────────────────┤     ├─────────────────────┤
│ Observe:            │     │ Assert:             │
│  - exit code        │     │  - tree hash =      │
│  - partial state    │     │    reference        │
│  - failed pages     │     │  - no page done 2x  │
└─────────────────────┘     │  - call count within│
                            │    tolerance        │
                            └─────────────────────┘
```

1. Run the pipeline fault-free on a fixture. Record: file-tree hash of output, mock's call log (purposes, counts, tokens)
2. Store the reference in `tests/fixtures/reference/<fixture>-<verb>-<params-hash>.json`
3. In every recovery test:
   a. Run with fault injected - observe exit code and state
   b. Run again without fault (recovery run)
   c. Assert: output tree hash equals reference; no page transcribed twice; call count within tolerance

**Why this is better than per-file assertions:**
- One reference covers hundreds of output properties simultaneously
- A change to output format updates one reference file, not dozens of assertions
- Recovery tests prove end-to-end correctness: "the output is identical regardless of where the crash happened"
- The reference is committed; a functional change that alters the reference must be deliberate

**Cost profiles as references**: the reference also stores calls by purpose (`draft`, `judge`, `improve`, `calibrate`, `summary`), token counts, and computed cost. A doubled judge loop or a leaked candidate call changes the cost profile and fails TC-148 (5% tolerance) before it reaches production.

## 8. Test Suite Structure and Naming

**File naming by category**: test files are numbered by test plan category, creating a scannable directory:

```
tests/
├── test_00_foundation.py       Category 0: dataclasses, config, helpers
├── test_01_input.py            Category 1: input resolution
├── test_02_survey.py           Category 2: survey and classification
├── test_03_backend.py          Category 3: backend faults
├── test_04_crashes.py          Category 4: crash and recovery
├── test_05_locks.py            Category 5: locks and disk errors
├── test_06_resume.py           Category 6: resume and staleness
├── test_07_batching.py         Category 7: batching (function level)
├── test_07b_batching_cli.py    Category 7: batching (CLI level)
├── test_08_quality.py          Category 8: quality loop (function level)
├── test_08b_quality_cli.py     Category 8: quality loop (CLI level)
├── test_09_assembly.py         Category 9: assembly (function level)
├── test_09b_assembly_cli.py    Category 9: assembly (CLI level)
├── test_10_maintenance.py      Category 10: CLI, status, clean
├── test_10b_cli.py             Category 10: CLI (integration)
├── test_11_concurrency.py      Category 11: concurrency safety
├── test_12_windows_fs.py       Category 12: Windows paths
├── test_13_boundaries.py       Category 13: boundary cases
├── test_15_cost_guard.py       Category 15: cost regression
└── test_16_pairwise.py         Category 16: parameter combinations
```

**The `b` suffix convention**: `test_07_batching.py` tests the batching logic at the function level (unit tests). `test_07b_batching_cli.py` tests the same logic at the Command-Line Interface (CLI) level (integration tests through `run_cli`). Same category, two levels.

**Function naming**: `test_tc_NNN_<slug>` with the TC ID in the docstring. This makes grep for a specific test case trivial:

```python
def test_tc_042_crash_recovery_render():
  """TC-42: Recovery after crash during render stage."""
```

**Helper organization**: helpers live in `tests/helpers/` with one file per track:

```
tests/helpers/
├── core.py           Shared helpers (FakeClock, tree_hash, tmp_layout)
├── transport.py      Mock transport factory
├── fixtures.py       Fixture copy helpers
├── loop.py           Quality loop test builders
├── workfolders.py    Synthetic work folder builders
├── cli.py            run_cli subprocess wrapper
└── t1.py .. t5.py    Track-specific helpers (PG-01 disjoint ownership)
```

## 9. Cost Reference Profiles

When a pipeline makes paid API calls, test suites should guard against accidental cost increases. The TRNSKILRW project stores a cost profile per reference run.

**What the profile contains:**
- Calls by purpose: `draft: 12, judge: 10, improve: 3, calibrate: 1, summary: 1`
- Tokens in and out per purpose
- Computed cost from the test pricing file

**How the guard works:**
- TC-148: exact per-purpose call counts; 5% token and amount tolerance
- TC-150: mutation probe - a judge scripted to score 3.9 (below `--min-score 4.0`) triggers improvement rounds; the guard reports the per-purpose delta
- TC-151: `--candidates 3` adds exactly 2 extra draft calls (3 total minus 1 default)
- TC-152: crash run + recovery run together exceed reference by at most one call per crashed stage

**Why cost profiles belong in the test suite**: a bug that adds an unnecessary judge retry or skips the "already done" check doubles the API cost. The cost guard catches this as a test failure, not as a surprise invoice.

## 10. Integration with Prompt Sequences

Tests integrate with IPPS prompt sequences through consistent patterns.

**Default test command in NOTES.md**: the session records the exact test command so every prompt uses the same invocation:

```
CWD: [SKILL_FOLDER]
Python: [PYTHON]
Command: python -m pytest tests/ --no-header -p no:cacheprovider -q -n auto
```

**Verification blocks in prompts**: every prompt ends with a `Verify:` block naming the exact test command and expected outcome:

```
Verify: [PYTHON] -m pytest tests/test_03_backend.py -q --no-header -p no:cacheprovider
  completes with every test passed or strict-xfailed;
  18 test functions present;
  Get-Process python* filtered to the venv returns nothing.
```

**Nightly marker for long-running tests**: tests that run 20 repetitions or exercise slow paths are marked `@pytest.mark.nightly` and excluded from the default suite (`-m "not nightly"`). The nightly variant runs once in the final verification phase (P7-S3) with a 30-minute cap.

**Stray process sweep**: after every test run, prompts verify no python processes from the test remain:

```powershell
Get-Process python* -ErrorAction SilentlyContinue
```

This prevents orphan processes from accumulating across prompt executions and consuming system resources.

## Sources

- `DEVTESTS-IN01-SC-TRNSKILRW-NOTES`: Session NOTES.md from the TranscriptionSkillRewrite session - test command, pytest-xdist configuration, pipe warning [VERIFIED]
- `DEVTESTS-IN01-SC-TRNSKILRW-TP01`: `_TEST_LLM_TRANSCRIPTION_SKILL_V2.md` - 158 test cases across 16 categories, reference-run comparison pattern, cost profiles, mock transport behaviours [VERIFIED]
- `DEVTESTS-IN01-SC-TRNSKILRW-STRUT`: `__STRUT_TRNSKILRW.md` - parallel execution guarantees PG-01..PG-10, track structure, barrier protocol [VERIFIED]
- `DEVTESTS-IN01-SC-TRNSKILRW-CARD01`: `__CARD_01-Robustness.md` - banned commands, time caps, on-cap kill procedure, stray process sweep [VERIFIED]
- `DEVTESTS-IN01-SC-TRNSKILRW-CARD00`: `__CARD_00-Rules.md` - start/end protocol, source of truth order, conventions section [VERIFIED]
- `DEVTESTS-IN01-SC-TRNSKILRW-P06A`: `_PROMPTS_06a-TestsT1-FaultsLoop.md` - xfail protocol, track file ownership, findings card, verification block [VERIFIED]
- `DEVTESTS-IN01-SC-TRNSKILRW-P06F`: `_PROMPTS_06f-TestsBarrier.md` - barrier gate, defect collection, full suite, xfail-to-BG mapping [VERIFIED]
- `DEVTESTS-IN01-SC-TRNSKILRW-P07`: `_PROMPTS_07-Fix.md` - sequential fix protocol, one BG per fix, marker removal, reference update [VERIFIED]
- `DEVTESTS-IN01-SC-TRNSKILRW-CONFTEST`: `tests/conftest.py` - fixture registry, mock transport factory, crash hook, CLI env stripping [VERIFIED]
- `DEVTESTS-IN01-SC-TRNSKILRW-PYTESTINI`: `pytest.ini` - nightly marker registration, test paths [VERIFIED]
- `DEVTESTS-IN01-SC-PREX02`: `PROMPTS_EXAMPLE_02-RobustnessCard.md` - robustness card pattern, two-tier defense, process-tree kill [VERIFIED]

## Next Steps

1. Extract pytest runner rules into `coding-conventions` as a `TESTING-RULES.md` file covering: quiet-mode flags, xfail protocol, nightly markers, stray process sweeps, and the pipe deadlock warning
2. Add the parallel test-writing track pattern (PG-01..PG-10) to `PROMPTS_GUIDES.md` as a section on test prompt sequences
3. Add mock transport and FakeClock patterns to `PYTHON-RULES.md` or a dedicated `TESTING-RULES.md`
4. Add cost reference profiles as a recommended testing pattern for any skill that makes API calls

## Document History

**[2026-09-16 13:28]**
- Fixed: Timeline missing "Updated 0 times" (INFO-HD-03)
- Fixed: Acronyms TC, CLI, CI expanded on first use (AP-PR-06)
- Fixed: File trees converted to Unicode box-drawing characters (INFO-FT-03)
- Added: Reference-run comparison flow diagram in Section 7 (INFO-FT-05)
- Fixed: Unexplained `consult` jargon replaced with plain language (AP-PR-12)

**[2026-09-16 13:22]**
- Initial research document created from analysis of `_2026-09-16_TranscriptionSkillRewrite` session
