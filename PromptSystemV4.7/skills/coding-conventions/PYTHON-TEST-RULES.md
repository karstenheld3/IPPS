# Python Test Rules

Enforceable rules for Python test suites using pytest. Apply when writing, reviewing, or debugging Python tests.

**Writing quality:** Apply `APAPALAN_RULES.md`. Key rules: APAPL-PR-07 (be specific), APAPL-PR-09 (consistent patterns), APAPL-BR-01 (single line for single statements), APAPL-BR-04 (compact definitions)

## Rule Index

Runner Configuration (RC)
- PY-TR-RC-01: Quiet-mode flags for agent sessions
- PY-TR-RC-02: Parallel execution with pytest-xdist
- PY-TR-RC-03: pytest.ini marker registration
- PY-TR-RC-04: No piping parallel output through streaming filters

Defect Protocol (DP)
- PY-TR-DP-01: Strict xfail with bug ID
- PY-TR-DP-02: Nightly marker for long-running tests

Test Isolation (TI)
- PY-TR-TI-01: tmp_path for all file I/O
- PY-TR-TI-02: No mutable global state
- PY-TR-TI-03: Environment variable stripping in conftest

Mock Transport (MT)
- PY-TR-MT-01: Mock transport activation via environment variable
- PY-TR-MT-02: FakeClock for time-dependent tests
- PY-TR-MT-03: Fail-fast without mock and without API keys

Naming (NM)
- PY-TR-NM-01: Test file naming by category
- PY-TR-NM-02: Test function naming with TC ID
- PY-TR-NM-03: Helper file organization

Process Safety (PS)
- PY-TR-PS-01: Stray process sweep after every run
- PY-TR-PS-02: Test commands monitored, ended only on a hang

## Rules

### PY-TR-RC-01: Quiet-Mode Flags for Agent Sessions

When running tests inside an agent session, use all four flags to minimize context token usage.

**BAD:**
```
python -m pytest tests/ -v
python -m pytest tests/
pytest tests/ -q
```

**GOOD:**
```
python -m pytest tests/ --no-header -p no:cacheprovider -q
python -m pytest tests/ --no-header -p no:cacheprovider -q -n auto
```

**Flag breakdown:**
- `-q`: one character per test (`.` pass, `x` xfail, `s` skip, `F` fail)
- `--no-header`: suppresses pytest version and plugin banner (3-5 lines)
- `-p no:cacheprovider`: suppresses `.pytest_cache/` directory and cache messages
- `-n auto`: parallel execution (see PY-TR-RC-02)

**Token budget**: 300 tests in quiet mode produce approximately 5 lines. Verbose mode produces 300+ lines. 60x reduction.

### PY-TR-RC-02: Parallel Execution with pytest-xdist

Use `-n auto` to distribute tests across all CPU cores.

**BAD:**
```
python -m pytest tests/ -q --no-header
```
(serial execution on 300+ tests = 10+ min)

**GOOD:**
```
pip install pytest-xdist
python -m pytest tests/ -q --no-header -p no:cacheprovider -n auto
```
(parallel execution = 2-3 min on 8 cores)

**Prerequisite**: tests must use `tmp_path` and have no shared mutable state (see PY-TR-TI-01, PY-TR-TI-02).

### PY-TR-RC-03: pytest.ini Marker Registration

Register custom markers in `pytest.ini` to suppress warnings and document intent.

**BAD:**
```ini
[pytest]
testpaths = tests
```
(custom markers trigger `PytestUnknownMarkWarning`)

**GOOD:**
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
markers =
    nightly: long-running tests excluded from default suite
```

### PY-TR-RC-04: No Piping Parallel Output Through Streaming Filters

Do not pipe pytest-xdist output through PowerShell `Select-Object`, `Where-Object`, or similar streaming commands. These buffer the entire output before processing, which appears to hang.

**BAD:**
```powershell
python -m pytest tests/ -n auto -q | Select-Object -Last 5
python -m pytest tests/ -n auto 2>&1 | Where-Object { $_ -match 'FAIL' }
```

**GOOD:**
```powershell
python -m pytest tests/ -n auto -q --no-header -p no:cacheprovider
python -m pytest tests/ -n auto -q --no-header -p no:cacheprovider 2>&1 > test_output.txt; Get-Content test_output.txt -Tail 5
```

### PY-TR-DP-01: Strict xfail with Bug ID

When a test exposes an implementation defect that cannot be fixed in the current track, mark it with `strict=True` and a trackable bug ID.

**BAD:**
```python
@pytest.mark.xfail
def test_tc_042_crash_recovery():
  ...

@pytest.mark.xfail(reason="broken")
def test_tc_042_crash_recovery():
  ...
```

**GOOD:**
```python
@pytest.mark.xfail(strict=True, reason="PROJ-BG-0142")
def test_tc_042_crash_recovery():
  """TC-42: Recovery after crash during render stage."""
  ...
```

`strict=True` makes the test fail if it unexpectedly passes, forcing marker removal when the bug is fixed. The bug ID links to `PROBLEMS.md`.

### PY-TR-DP-02: Nightly Marker for Long-Running Tests

Tests that run many repetitions, exercise slow paths, or require extended time get the `nightly` marker and are excluded from the default suite.

**BAD:**
```python
def test_tc_155_twenty_repetitions():
  """Runs 20 random seeds - takes 3 minutes."""
  for seed in range(20):
    ...
```
(blocks every test run for 3 minutes)

**GOOD:**
```python
@pytest.mark.nightly
def test_tc_155_twenty_repetitions():
  """Runs 20 random seeds - takes 3 minutes."""
  for seed in range(20):
    ...
```

Default suite: `python -m pytest tests/ -m "not nightly" -q --no-header -p no:cacheprovider -n auto`
Nightly suite: `python -m pytest tests/ -m "nightly" -q --no-header -p no:cacheprovider` (expected runtime about 10 min; runs to its end)

### PY-TR-TI-01: tmp_path for All File I/O

Every test that creates files must use pytest's `tmp_path` fixture. This gives each test its own temporary directory, enabling parallel execution.

**BAD:**
```python
def test_output_format():
  os.makedirs("test_output", exist_ok=True)
  run_pipeline(output_dir="test_output")
  assert os.path.exists("test_output/result.md")
```

**GOOD:**
```python
def test_output_format(tmp_path):
  run_pipeline(output_dir=str(tmp_path))
  assert (tmp_path / "result.md").exists()
```

### PY-TR-TI-02: No Mutable Global State

Tests must not share mutable state across test functions. Each test must be independent.

**BAD:**
```python
results = []

def test_step_1():
  results.append(run_step_1())

def test_step_2():
  assert len(results) == 1
  results.append(run_step_2())
```

**GOOD:**
```python
def test_step_1(tmp_path):
  result = run_step_1(output=tmp_path)
  assert result.success

def test_step_2(tmp_path):
  result = run_step_2(output=tmp_path)
  assert result.success
```

### PY-TR-TI-03: Environment Variable Stripping in conftest

Strip environment variables that could leak real API keys or configuration into mock-based tests. Use a session-scoped autouse fixture.

**BAD:**
```python
# conftest.py - no environment stripping
# Tests accidentally use real API keys from the developer's shell
```

**GOOD:**
```python
# conftest.py
@pytest.fixture(autouse=True, scope="session")
def _strip_env():
  keys = [k for k in os.environ if k.startswith(("OPENAI_", "AZURE_", "ANTHROPIC_"))]
  saved = {k: os.environ.pop(k) for k in keys}
  yield
  os.environ.update(saved)
```

### PY-TR-MT-01: Mock Transport Activation via Environment Variable

Activate the mock transport through an environment variable pointing at a behaviour file. Never hardcode mock activation in production code.

**BAD:**
```python
# In production code
if os.environ.get("TESTING"):
  client = httpx.Client(transport=mock)
```

**GOOD:**
```python
# In conftest.py fixture
@pytest.fixture
def mock_transport(tmp_path):
  behaviour_file = tmp_path / "behaviours.json"
  behaviour_file.write_text(json.dumps(["ok", "ok", "http:429:retry-after=2", "ok"]))
  monkeypatch.setenv("TRANSCRIBE_TEST_TRANSPORT", str(behaviour_file))
  yield
```

### PY-TR-MT-02: FakeClock for Time-Dependent Tests

Time-dependent tests (backoff, timeout, hang detection) must inject a FakeClock that advances without waiting. No `time.sleep()` calls in tests.

**BAD:**
```python
def test_timeout_handling():
  start = time.time()
  result = run_with_timeout(timeout=30)
  assert time.time() - start >= 30
```
(test takes 30 real seconds)

**GOOD:**
```python
def test_timeout_handling(fake_clock):
  result = run_with_timeout(timeout=1, clock=fake_clock)
  assert fake_clock.now >= 1
```
(test completes in milliseconds, FakeClock simulates the timeout)

### PY-TR-MT-03: Fail-Fast Without Mock and Without API Keys

A test run without the mock transport environment variable and without real API keys must exit immediately with a clear error. It must never hang waiting for a connection.

**BAD:**
```python
# No guard - test hangs trying to connect to real API
def test_backend():
  result = call_real_api()
```

**GOOD:**
```python
# In conftest.py or test setup
if not os.environ.get("TRANSCRIBE_TEST_TRANSPORT") and not keys_file.exists():
  pytest.exit("No mock transport and no API keys. Set TRANSCRIBE_TEST_TRANSPORT or provide keys.", returncode=1)
```

### PY-TR-NM-01: Test File Naming by Category

Number test files by test plan category. Use `test_NN_category.py` format. Use a letter suffix for unit vs integration split of the same category.

**BAD:**
```
tests/
├── test_basics.py
├── test_advanced.py
├── test_more_stuff.py
```

**GOOD:**
```
tests/
├── test_00_foundation.py       Category 0: dataclasses, config
├── test_03_backend.py          Category 3: backend faults
├── test_07_batching.py         Category 7: batching (unit)
├── test_07b_batching_cli.py    Category 7: batching (CLI integration)
```

### PY-TR-NM-02: Test Function Naming with TC ID

Embed the Test Case (TC) ID in the function name. Put the full TC description in the docstring.

**BAD:**
```python
def test_crash_recovery():
  ...

def test_42():
  ...
```

**GOOD:**
```python
def test_tc_042_crash_recovery_render():
  """TC-42: Recovery after crash during render stage."""
  ...
```

### PY-TR-NM-03: Helper File Organization

Place shared test helpers in `tests/helpers/` with one file per concern. Track-specific helpers in separate files to enforce disjoint ownership.

**BAD:**
```
tests/
├── helpers.py          (everything in one file)
├── test_03_backend.py
```

**GOOD:**
```
tests/helpers/
├── core.py             Shared: FakeClock, tree_hash, tmp_layout
├── transport.py        Mock transport factory
├── fixtures.py         Fixture copy helpers
├── cli.py              CLI subprocess wrapper
└── t1.py .. t5.py      Track-specific helpers (disjoint ownership)
```

### PY-TR-PS-01: Stray Process Sweep After Every Run

After every test run, verify no Python processes from the test remain running. Orphan processes accumulate across prompt executions and consume system resources.

**BAD:**
```powershell
python -m pytest tests/ -q --no-header -p no:cacheprovider -n auto
# (no cleanup check)
```

**GOOD:**
```powershell
python -m pytest tests/ -q --no-header -p no:cacheprovider -n auto
Get-Process python* -ErrorAction SilentlyContinue
```

If processes remain, kill them before proceeding.

### PY-TR-PS-02: Test Commands Monitored, Ended Only on a Hang

Every test command runs through the supervised runner (`agent-behavior.md` Terminal Hang Prevention). The runner has no time limit: a test run that still shows progress (new output, growing CPU time in the `ALIVE` log lines) runs to its end, however long it takes. Ending a slow run throws away the finished part and forces a second run.

The agent ends a test command only on a hang verdict (Terminal Hang Prevention step 5), through the stop file; the failure goes to the Fails card with the hang evidence and the last 20 output lines. A run that finishes far above its expected runtime is a runtime overrun: the result is used, the cause is recorded, the expected runtime is corrected.

**Starting values for the robustness card `## Expected runtimes`** (replace with measured project values; they start the liveness check, they are not limits):
- Single test file: 60 s
- Full suite: 5 min
- Nightly variant: 10 min
- Git operations: 10 s
