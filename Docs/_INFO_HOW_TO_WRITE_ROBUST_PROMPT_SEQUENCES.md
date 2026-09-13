# INFO: How to Write Robust Prompt Sequences

**Doc ID**: PRMTRBST-IN01
**Goal**: Synthesize evidence on hang-prevention, inter-prompt problem filing, and robustness patterns from CI/CD, agent frameworks, process management, and real prompt sequence sessions

## Summary

- **Multi-layer timeout strategy** [VERIFIED]: CI/CD systems (GitLab CI, GitHub Actions) use project-level, job-level, step-level, and shell-level timeouts. Lowest applicable limit wins. Prompt sequences should mirror this with per-command, per-prompt, and per-sequence caps.
- **No-output timeout** [VERIFIED]: GitLab CI has a separate no-output timeout (`RUNNER_SCRIPT_TIMEOUT`) that fires when a job produces no log output, even if wall-clock budget remains. Prompt sequences should detect silent hangs, not just long runs.
- **3x average duration heuristic** [VERIFIED]: GitHub Actions recommends `timeout-minutes` set to roughly 3x the job's average duration. Prompt caps should follow the same heuristic.
- **SIGTERM → SIGKILL escalation** [VERIFIED]: The `timeout` command sends SIGTERM first, then SIGKILL after a grace period. Process cleanup should follow the same escalation: request stop, wait, force-kill.
- **PowerShell pipe deadlock root cause** [VERIFIED]: `StandardOutput.ReadToEnd()` + `StandardError.ReadToEnd()` called sequentially deadlocks when stderr fills the pipe buffer while stdout is being read. Fix: async-read one stream with `BeginErrorReadLine()`.
- **Orphan process reaper pattern** [VERIFIED]: AutoGPT implements a reaper that finds RUNNING node_executions older than 5 min whose parent is terminal, marks them FAILED. Prompt sequences should specify the same: detect orphans, kill, record.
- **Two-regime idle timeout** [VERIFIED]: AutoGPT uses 30 min idle timeout when no tool pending, 2h cap when a tool is pending. Prompt sequences should differentiate between waiting-for-command and waiting-for-model.
- **Session reset after timeout must be communicated** [VERIFIED]: LangChain ShellToolMiddleware timeout silently resets the shell session without telling the model. The model keeps issuing commands against a reset shell. Prompt sequences must record timeout events in tracking files.
- **`finally` block, not `except`** [VERIFIED]: Process cleanup in `except` blocks is bypassed by exceptions. Use `finally` for guaranteed cleanup. SIGKILL cannot be caught, so `atexit` and `finally` don't run on force-kill.
- **Process group kill** [VERIFIED]: Kill the process group, not just the parent process. `start_new_session=True` (POSIX) or `CREATE_NEW_PROCESS_GROUP` (Windows) ensures the whole tree dies. `taskkill /T /F /PID` on Windows.
- **Inter-prompt problem filing prevents repeated mistakes** [VERIFIED]: A harness rewrite session used a shared glitch-and-findings INFO document that recorded 16 issues across 5 prompts. Later prompts read the document and avoided repeating the same mistakes. Sessions without a glitch document had drift detected only at the end — too late to fix without re-running earlier prompts.
- **Drift detection catches what in-prompt verification misses** [VERIFIED]: Four drift detection files from real prompt sequence sessions all found issues that passed in-prompt verification. The MITRE ATLAS drift caught a 107-page gap that was unnoticed during execution.
- **Current/Target Comparison is often absent** [VERIFIED]: The MITRE ATLAS drift file explicitly noted "Current/Target Comparison: absent" — no check of completed vs planned before starting case study prompts. This is a common robustness gap.
- **Strategy justification is often partial or absent** [VERIFIED]: The LLM Best Practices drift file noted "Strategy Justification: absent" (method deviation not logged). The Scan Jobs drift noted "Strategy Justification: Partial". Prompt sequences should require strategy justification in PROGRESS.md.
- **Planning errors propagate silently** [VERIFIED]: The LLM Best Practices session assumed 647 `<hr>` delimiters = 647 files, but 21 segments lacked Source lines or had duplicates (626 actual). The planning error was not caught until drift detection at the end.
- **ID collisions and numbering errors** [VERIFIED]: A security assessment session had finding IDs SEC-020 to SEC-023 assigned to both HIGH and MEDIUM findings. A glitch-and-findings document would catch this earlier.
- **Timestamps from memory instead of real clock** [VERIFIED]: A security assessment session recorded timestamps that predated the real clock. Prompt sequences should mandate `Get-Date` for timestamps, never memory.
- **Method deviation without logging** [VERIFIED]: The LLM Best Practices session switched from Playwright to Invoke-WebRequest but did not log WHY in PROGRESS.md. Later prompts could not understand the deviation. Prompt sequences should require strategy justification for method changes.
- **Extraction bugs during execution are invisible without a glitch document** [VERIFIED]: The MITRE ATLAS session had 6 extraction bugs (trailing `&`, duplicate rows, description filtering) identified and fixed during execution. Without a glitch document, these fixes are invisible to later prompts.
- **Constraint re-reading varies across sessions** [VERIFIED]: Some sessions re-read constraints (MITRE ATLAS, Portugal Healthcare), others don't (Scan Jobs: "Partial - constraints followed but not explicitly re-read mid-execution"). Prompt sequences should mandate constraint re-reading.

## 1. CI/CD Timeout Patterns

### Multi-Layer Timeout Architecture

CI/CD systems enforce multiple timeout layers simultaneously. The lowest applicable limit always wins [VERIFIED].

**GitLab CI** layers:
- Project pipeline timeout (default 1h)
- Per-job `timeout:` keyword in `.gitlab-ci.yml`
- Runner `maximum_timeout` in `config.toml`
- No-output timeout (`RUNNER_SCRIPT_TIMEOUT`) — fires when job produces no log output

**GitHub Actions** layers:
- Job-level `timeout-minutes` (default 360 min = 6 hours)
- Step-level `timeout-minutes` (independent of job-level)
- Shell-level `timeout` command (seconds, exit code 124)

**Heuristic**: Set timeout to roughly 3x the job's average duration [VERIFIED]. If a test suite normally runs in 8 minutes, set timeout to 25 minutes. This gives headroom for slow runs without letting a hung process run for hours.

**No-output timeout**: A separate timeout that fires when a process produces no log output for too long, even if the wall-clock budget remains [VERIFIED]. This catches silent hangs: a process waiting on stdin, a stalled download, a frozen network mount. Prompt sequences should specify both wall-clock caps and no-output detection.

### Shell-Level Timeout Pattern

```bash
timeout --kill-after=5s 10s command
```

Sends SIGTERM first, waits 5s, then SIGKILL [VERIFIED]. Exit code 124 indicates timeout. This is the pattern prompt sequences should recommend for per-command caps.

Sources:
- https://costops.dev/guides/reduce-ci-timeouts
- https://devopsaitoolkit.com/blog/gitlab-error-job-execution-timeout/
- https://latchkey.dev/learn/gitlab-ci/gitlab-job-execution-timeout
- https://coderlegion.com/12372/timeout-handling-in-bash-preventing-hanging-scripts-in-production

## 2. Agent Framework Hang-Prevention Patterns

### AutoGPT: LLM Request Timeout + Orphan Reaper

AutoGPT PR #13051 [VERIFIED] fixed a production incident where:
- Most LLM provider calls had no timeout (only Anthropic had `timeout=600`)
- A stalled HTTP read parked the executor thread indefinitely
- Orphan `RUNNING` node_executions persisted after parent graph was `FAILED`

**Fix**:
- Module-level constant `LLM_REQUEST_TIMEOUT_SECONDS = 600`
- `asyncio.wait_for(..., timeout=LLM_REQUEST_TIMEOUT_SECONDS)` wrapping provider calls
- Belt-and-suspenders: both `asyncio.wait_for` (outer) and per-SDK `timeout=` (inner)
- `reap_orphan_node_executions()`: finds RUNNING node_execs older than 5 min whose parent is terminal, marks them FAILED

### AutoGPT: E2B Sandbox Timeout + Retry

AutoGPT PR #12774 [VERIFIED] fixed sandbox creation hangs:
- `AsyncSandbox.create()` used `httpx.AsyncClient(timeout=None)` — infinite wait
- When E2B API stalled, executor goroutines hung indefinitely
- RabbitMQ consumer timeout (1h42m) eventually killed the pod

**Fix**:
- Per-attempt timeout: `asyncio.wait_for(AsyncSandbox.create(), timeout=30)`
- 3 retries with exponential backoff (~93s worst case vs infinite)
- Recovery re-enqueue: on unexpected failure, re-enqueue session to RabbitMQ

### AutoGPT: Two-Regime Idle Timeout

AutoGPT PR #12927 [VERIFIED] introduced:
- 30 min idle timeout when no tool pending (raised from 10 min)
- 2h hard cap when a tool is pending (hung-tool protection)
- Differentiates between "waiting for model response" and "waiting for tool execution"

### LangChain: Silent Session Reset on Timeout

LangChain issue #39953 [VERIFIED] documented:
- `ShellToolMiddleware` timeout silently restarts the shell session
- `startup_commands` (ulimit, umask, environment) are NOT re-run on timeout path
- Model is never told the session was reset → keeps issuing commands against a reset shell
- Guards placed in `startup_commands` stop applying silently

**Lesson**: Timeout events must be communicated to the agent and recorded in tracking files. A timeout that silently resets state is worse than no timeout.

Sources:
- https://github.com/Significant-Gravitas/AutoGPT/pull/13051
- https://github.com/Significant-Gravitas/AutoGPT/pull/12774
- https://github.com/Significant-Gravitas/AutoGPT/pull/12927
- https://github.com/langchain-ai/langchain/issues/39953

## 3. PowerShell Pipe Deadlock

### Root Cause

Microsoft's Raymond Chen documented the fundamental problem [VERIFIED]:

When a process redirects both stdin and stdout to pipes, reading stdout and writing stdin sequentially deadlocks. The parent blocks waiting for the child to read all stdin data. The child blocks waiting for the parent to read its stdout data. Both wait forever.

**Buffering masks the problem**: The pipe manager buffers writes, so small data amounts don't deadlock. The deadlock appears only when data exceeds the pipe buffer size — typically with large output or many lines of prompt text.

### The `ReadToEnd()` Deadlock Pattern

```csharp
// DEADLOCK: sequential reads
string output = process.StandardOutput.ReadToEnd();
string errors = process.StandardError.ReadToEnd();
```

This pattern [VERIFIED] is the exact cause of the PowerShell `2>&1` hang documented in a harness rewrite session. Reading one stream to completion before starting the other deadlocks when the unread stream fills its pipe buffer.

### Fix: Async Read One Stream

```csharp
// FIX: async-read one stream
process.BeginErrorReadLine();
string output = process.StandardOutput.ReadToEnd();
process.WaitForExit();
```

`BeginErrorReadLine()` starts an async read on the error stream, preventing the pipe from filling [VERIFIED].

### Relevance to Prompt Sequences

The `2>&1` merge with `Blocking: true` in agent execution tools triggers this exact pattern. The agent's process management reads stdout synchronously while stderr fills the pipe buffer. The fix in prompt sequences: ban `2>&1` with blocking execution, use non-blocking execution with separate stream handling.

Sources:
- https://devblogs.microsoft.com/oldnewthing/20110707-00/?p=10223
- https://stackoverflow.com/questions/6611098/powershell-start-job-wait-job-host-thread-never-exits-when-run-from-asp-net-ii
- https://stackoverflow.com/questions/71198189/powershell-system-diagnostics-processstartinfo-hangs-reason-unknown

## 4. Process Cleanup Best Practices

### Process Group Kill

**POSIX** [VERIFIED]:
```python
proc = subprocess.Popen(args, start_new_session=True)
os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
```

**Windows** [VERIFIED]:
```python
proc = subprocess.Popen(args, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
proc.send_signal(signal.CTRL_BREAK_EVENT)
# or: taskkill /T /F /PID <pid>
```

### Escalation Pattern

1. SIGTERM (graceful stop request)
2. Wait (5s default)
3. SIGKILL (force-kill, cannot be caught)
4. Drain pipes (read remaining buffered output)

### `finally` Block, Not `except`

Process cleanup in `except` blocks is bypassed by exceptions [VERIFIED]. Use `finally` for guaranteed cleanup:

```python
try:
    proc = subprocess.Popen(args, start_new_session=True)
    yield proc
finally:
    if proc.poll() is None:
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
```

### SIGKILL Limitation

SIGKILL cannot be caught [VERIFIED]. `atexit` hooks and `finally` blocks don't run on SIGKILL. Children are reparented to PID 1 and keep running unless they were in the same process group. This is why process group kill is essential.

### Orphan Reaper Pattern

AutoGPT's reaper [VERIFIED]:
- Finds RUNNING node_execs older than 5 min whose parent is terminal
- Marks them FAILED
- Conservative: only acts on old orphans with terminal parents

Claude Code hooks [VERIFIED]:
- PostToolUse hook scans for orphaned child processes after Bash tool execution
- Kills orphans with SIGTERM → wait → SIGKILL
- Scans by ppid, not tool_name — tool-agnostic

Sources:
- https://aitoolsguidebook.com/en/articles/agent-subprocess-orphaned/
- https://dev.to/chenyuan20509/your-subprocesses-outlive-your-program-heres-how-to-kill-them-for-real-4npp
- https://github.com/terrylica/cc-skills/blob/main/plugins/itp-hooks/hooks/posttooluse-subprocess-orphan-cleanup.ts

## 5. Evidence from Real Prompt Sequence Sessions

This section presents findings from analyzing prompt sequence sessions across three workspaces. Each session used `_PROMPTS_*.md` files with sequential prompt execution. Drift detection files (`__DRIFT_*.md`) and problem tracking files (`PROBLEMS.md`) provide ex-post analysis of what went wrong and what was caught.

### 5.1 Sessions Analyzed

| Session | Prompts | Drift File | Glitch Doc | Outcome |
|---------|---------|------------|------------|---------|
| Harness rewrite (2026-09-07) | 5 files, 25+ prompts | No | Yes (16 entries) | Glitches caught in-prompt, later prompts avoided repeats |
| Security assessment (2026-09-12) | Multi-prompt, STRUT-driven | No | No | ID collision, timestamp errors caught late |
| Specs from V1 (2026-09-06) | 4 prompts | No | No | Multiple open problems at session end |
| MITRE ATLAS transcription (2026-09-10) | 35 batched prompts | Yes | No | 107-page gap unnoticed during execution, drift caught it |
| LLM Best Practices download (2026-09-12) | 4 prompts | Yes | No | 4 MISSED items (planning error), method deviation unlogged |
| Portugal Healthcare (2026-09-09) | 3 prompts | Yes | No | 1 FAIL (abbreviations), all meta-criteria present |
| Scan and Rank Jobs (2026-09-10) | 5 prompts | Yes | No | 9 FAIL items (broker coverage), strategy justification partial |

### 5.2 Inter-Prompt Problem Filing: The Harness Rewrite Session

**Session**: Harness rewrite (2026-09-07), 5 prompt files, 25+ prompts
**Glitch document**: `_INFO_IMPLEMENTATION_GLITCHES_AND_FINDINGS.md` — 16 entries across 5 prompts

The harness rewrite session is the only session that used a dedicated glitch-and-findings INFO document. Every prompt included a `Documentation:` directive pointing to the file. The document recorded:

- 1 HIGH-severity hang (pipe deadlock from `2>&1` with `Blocking: true`)
- 2 HIGH-severity sequencing violations (STRUT step skipped, test regression survived 3 prompts)
- 5 MEDIUM-severity spec-code mismatches (type mismatch, property naming, test expectation drift)
- 8 LOW-severity issues (lint allow-list shifts, flaky tests, bypass inventory interpretation)

**How later prompts used the findings**: Later prompts read the glitch document at startup and:
- Avoided the `2>&1` pattern (banned in card 00 Section 12 after the first hang)
- Caught spec-code mismatches earlier by checking the findings document before verification
- Followed the naming convention after reading the mismatch entry
- Backfilled the skipped STRUT step after reading the sequencing violation entry

**What happened in sessions without a glitch document**: The MITRE ATLAS session had 6 extraction bugs (trailing `&`, duplicate rows, description filtering) fixed during execution, but these fixes were invisible to later prompts. The LLM Best Practices session switched from Playwright to Invoke-WebRequest without logging why — later prompts could not understand the deviation.

### 5.3 Drift Detection Catches What In-Prompt Verification Misses

All four drift detection files found issues that passed in-prompt verification [VERIFIED]:

**MITRE ATLAS** (`__DRIFT_MTRATLAS.md`): 35 prompts, 340 pages transcribed. Drift found:
- 107 technique pages initially missed (technique gap unnoticed during execution)
- `/verify` not run after completion (MISSED criterion 27)
- Current/Target Comparison: **absent** — no check of completed vs planned before starting case study prompts
- 6 extraction bugs identified and fixed during execution (trailing `&`, duplicate technique IDs, description filtering)

**LLM Best Practices** (`__DRIFT_LLMBSTPRC.md`): 4 prompts, 647 pages planned. Drift found:
- 4 MISSED items: 626 actual files vs 647 expected (planning error: 21 segments lacked Source lines or had duplicates)
- Spot-check against live .md not possible (site serves HTML at .md URLs, not raw markdown)
- Strategy Justification: **absent** — method deviation (Playwright to Invoke-WebRequest) not logged in PROGRESS.md
- Self-Correction: present (switched from browser_evaluate to Invoke-WebRequest when browser could not save to disk)

**Portugal Healthcare** (`__DRIFT_PTHLTINS.md`): 3 prompts, 62 criteria. Drift found:
- 1 FAIL: abbreviations not expanded on first use in new summary sections (fixed)
- All meta-criteria present (prompt decomposition, current/target comparison, constraint re-reading, self-correction, backtracking, strategy justification, quantitative completeness)
- Best-structured session of all analyzed: constraints followed, labels used consistently, no markdown tables in new content

**Scan and Rank Jobs** (`__DRIFT_SCANJOBS.md`): 5 prompts, 42 criteria. Drift found:
- 9 FAIL items: 8 broker coverage shortfalls (3+ brokers per country not met initially), 1 citation missing
- Constraint Re-reading: **partial** — constraints followed but not explicitly re-read mid-execution
- Strategy Justification: **partial** — some decisions explained, others not
- Self-Correction: present (adapted Freelancermap URL strategy, used Google fallback for LinkedIn)

### 5.4 Common Robustness Gaps Across Sessions

**Current/Target Comparison absent** [VERIFIED]: The MITRE ATLAS session explicitly noted this gap. No check of completed vs planned before starting the next batch of prompts. The technique gap (107 pages) was unnoticed until drift detection. Prompt sequences should include a "what is done vs what remains" check at the start of each prompt.

**Strategy Justification absent or partial** [VERIFIED]: Two of four drift files noted this gap. Method deviations and strategy changes were not logged in PROGRESS.md. Later prompts could not understand why earlier prompts deviated. Prompt sequences should require a one-line strategy justification in PROGRESS.md when the agent deviates from the planned method.

**Planning errors propagate silently** [VERIFIED]: The LLM Best Practices session assumed 647 `<hr>` delimiters = 647 files. The actual count was 626 (21 segments lacked Source lines or had duplicates). This planning error was not caught until drift detection at the end. Prompt sequences should verify planning assumptions early — a quick count check after the first batch would have caught the discrepancy.

**ID collisions and numbering errors** [VERIFIED]: The security assessment session had finding IDs SEC-020 to SEC-023 assigned to both HIGH and MEDIUM findings. This was caught and resolved by renumbering MEDIUM/LOW to SEC-024 to SEC-044, but a glitch-and-findings document would have caught it at the moment of assignment.

**Timestamps from memory instead of real clock** [VERIFIED]: The security assessment session recorded timestamps that predated the real clock (entries at 18:10 and 18:30, but backup mtime was 17:34). Prompt sequences should mandate `Get-Date` for timestamps, never memory or estimation.

**Constraint re-reading varies** [VERIFIED]: The Scan Jobs drift noted "Constraint Re-reading: Partial — constraints followed but not explicitly re-read mid-execution." The MITRE ATLAS and Portugal Healthcare sessions re-read constraints. Prompt sequences should mandate constraint re-reading at the start of each prompt, especially for long sequences.

### 5.5 What Works: Patterns from the Best Sessions

**Portugal Healthcare** (best-structured session):
- 3-prompt sequence with clear decomposition (research, supplement, summary)
- Every prompt had explicit constraints (no new files in step 1, no summary modification in steps 1-2, labels used consistently, no markdown tables in new content)
- All meta-criteria present
- Only 1 FAIL (abbreviations), caught and fixed

**Harness rewrite** (best problem-filing):
- Dedicated glitch-and-findings document with 16 entries
- Every prompt included a `Documentation:` directive
- Later prompts read the findings and avoided repeating mistakes
- Card system (card 00) enforced hang-safety and end-of-prompt protocol

**MITRE ATLAS** (best recovery):
- 107-page gap caught by drift detection
- Backtracking present: returned to fill technique gap, Prompts 7-21 executed
- 6 extraction bugs identified and fixed during execution
- 340/340 pages verified (100% after correction)

### 5.6 The Card System as a Robustness Mechanism

The harness rewrite session used a card system — compact context documents read at the start of each prompt. The card system provides:

- **Fixed operating contract**: Card 00 (Rules) defines hang-safe commands, failure handling, commit conventions, and the end-of-prompt protocol. Every prompt reads card 00 first.
- **Context budget management**: Card 00 Section 2 limits what can be read per prompt (at most 3 SPEC documents, 6 source files). This prevents context overflow.
- **Resume detection**: Card 00 Section 3 checks if a STRUT step is already done before starting work. This prevents re-execution.
- **End-of-prompt protocol**: Card 00 Section 4 enforces verification, STRUT update, PROGRESS.md, PROBLEMS.md, commit. This prevents incomplete work from being marked done.
- **Residual sweep**: Card 00 Section 7 defines term groups that must return zero matches outside Document History. This catches stale references.

The card system integrates with problem filing at two points:
- Section 3 (start-of-prompt): read the glitch-and-findings document for unresolved entries
- Section 4 (end-of-prompt): file glitches before the commit

Sessions without a card system (MITRE ATLAS, LLM Best Practices, Portugal Healthcare, Scan Jobs) relied on the prompt text itself for constraints and verification. These sessions had more drift because the constraints were not re-read at the start of each prompt.

## 6. Recommendations for Robust Prompt Sequences

Based on the evidence above, robust prompt sequences should:

1. **Include a hang-safety clause** in every implementation prompt (prohibition, banned list, cap behavior)
2. **Designate a shared glitch-and-findings INFO document** and include a `Documentation:` directive in every implementation prompt
3. **Read the findings document at prompt startup** for unresolved entries from prior prompts
4. **File glitches before the end-of-prompt commit** — record what, expected, actual, root cause, resolution, prevention
5. **Use a card system** for long sequences (5+ prompts) to enforce constraint re-reading and end-of-prompt protocol
6. **Verify planning assumptions early** — a quick count check after the first batch prevents planning errors from propagating
7. **Log strategy justifications** in PROGRESS.md when deviating from the planned method
8. **Mandate `Get-Date` for timestamps** — never use memory or estimation
9. **Include a Current/Target Comparison** at the start of each prompt — check what is done vs what remains
10. **Run drift detection** after completion to catch issues that passed in-prompt verification

## 7. Exclusions

- **Docker/container orchestration timeouts**: Out of scope for prompt sequences (agent execution, not container management)
- **Database query timeouts**: Out of scope (prompt sequences don't typically run database queries directly)
- **Network request timeouts**: Partially covered (curl `--max-time` mentioned), but HTTP client configuration is out of scope
- **Kernel-level hang detection** (D-state processes): Out of scope for prompt-level prevention
- **Sessions without prompt files**: Sessions that used `/go` or ad-hoc commands without `_PROMPTS_*.md` files are out of scope (no prompt sequence to analyze)

## Sources

### External Sources (Web Research)

1. https://costops.dev/guides/reduce-ci-timeouts — GitHub Actions timeout best practices
2. https://devopsaitoolkit.com/blog/gitlab-error-job-execution-timeout/ — GitLab CI timeout layers
3. https://latchkey.dev/learn/gitlab-ci/gitlab-job-execution-timeout — GitLab CI timeout configuration
4. https://coderlegion.com/12372/timeout-handling-in-bash-preventing-hanging-scripts-in-production — Bash timeout handling
5. https://github.com/Significant-Gravitas/AutoGPT/pull/13051 — AutoGPT LLM timeout + orphan reaper
6. https://github.com/Significant-Gravitas/AutoGPT/pull/12774 — AutoGPT E2B sandbox timeout + retry
7. https://github.com/Significant-Gravitas/AutoGPT/pull/12927 — AutoGPT two-regime idle timeout
8. https://github.com/langchain-ai/langchain/issues/39953 — LangChain silent session reset on timeout
9. https://devblogs.microsoft.com/oldnewthing/20110707-00/?p=10223 — PowerShell pipe deadlock root cause
10. https://stackoverflow.com/questions/6611098/powershell-start-job-wait-job-host-thread-never-exits-when-run-from-asp-net-ii — PowerShell `ReadToEnd()` deadlock fix
11. https://stackoverflow.com/questions/71198189/powershell-system-diagnostics-processstartinfo-hangs-reason-unknown — PowerShell process output deadlock
12. https://aitoolsguidebook.com/en/articles/agent-subprocess-orphaned/ — Agent subprocess orphan cleanup
13. https://dev.to/chenyuan20509/your-subprocesses-outlive-your-program-heres-how-to-kill-them-for-real-4npp — Process termination protocol
14. https://github.com/terrylica/cc-skills/blob/main/plugins/itp-hooks/hooks/posttooluse-subprocess-orphan-cleanup.ts — Claude Code orphan cleanup hook

### Internal Sources (Session Analysis)

15. `e:\Dev\Lana-V2-Dev\_sessions\_2026-09-07_AgentDesignImprovement\_INFO_IMPLEMENTATION_GLITCHES_AND_FINDINGS.md` — 16 glitch entries across 5 prompts [VERIFIED]
16. `e:\Dev\Lana-V2-Dev\_sessions\_2026-09-07_AgentDesignImprovement\__CARD_00-Rules.md` — Card system with hang-safety, end-of-prompt protocol, residual sweep [VERIFIED]
17. `e:\Dev\Lana-V2-Dev\_sessions\_2026-09-07_AgentDesignImprovement\_PROMPTS_HarnessRewrite-05-SealAndShip.md` — 10-prompt sequence with Documentation directive [VERIFIED]
18. `e:\Dev\Lana-V2-Dev\_sessions\_2026-09-12_SecurityAssessment\PROBLEMS.md` — ID collision (SEC-020 to SEC-023), timestamp errors [VERIFIED]
19. `e:\Dev\Lana-V2-Dev\_sessions\_2026-09-12_SecurityAssessment\_PROMPTS_SecurityAssessmentExecution.md` — Multi-prompt STRUT-driven sequence [VERIFIED]
20. `e:\Dev\Lana-V2-Dev\_sessions\_2026-09-06_SpecsFromV1\PROBLEMS.md` — 20 open problems, memory retrieval race, ACP session switch [VERIFIED]
21. `e:\Dev\Lana-V2-Dev\_sessions\_2026-09-06_SpecsFromV1\_PROMPTS_LanaV2DeferredWork.md` — 4-prompt sequence [VERIFIED]
22. `e:\Dev\KarstensWorkspace\_PrivateSessions\_2026-09-10_MITREAtlasTranscription\__DRIFT_MTRATLAS.md` — 35-prompt transcription, 107-page gap, Current/Target Comparison absent [VERIFIED]
23. `e:\Dev\KarstensWorkspace\_PrivateSessions\_2026-09-12_LLMBestPracticesPromptChaining\__DRIFT_LLMBSTPRC.md` — 4-prompt download, planning error (626 vs 647), Strategy Justification absent [VERIFIED]
24. `e:\Dev\KarstensWorkspace\_Sessions\_!EmigrationGermanyToPortugal\Portugal-Healthcare\__DRIFT_PTHLTINS.md` — 3-prompt research, all meta-criteria present, 1 FAIL [VERIFIED]
25. `e:\Dev\KarstensWorkspace\_Sessions\_!KarstenHeldPersonalBrand\T04_OtherRecruitersAndJobSearch\__DRIFT_SCANJOBS.md` — 5-prompt research, 9 FAIL items, Strategy Justification partial [VERIFIED]

## Document History

**[2026-09-12 19:15]**
- Renamed from `_INFO_PRMTHNGS-In01_HangPreventionInAgentExecution.md` to `_INFO_HOW_TO_WRITE_ROBUST_PROMPT_SEQUENCES.md`
- Changed: Doc ID from PRMTHNGS-IN01 to PRMTRBST-IN01
- Changed: Title from "Hang-Prevention in Prompt Sequences and Agent Execution" to "How to Write Robust Prompt Sequences"
- Added: Section 5 "Evidence from Real Prompt Sequence Sessions" with 7 session analyses, 6 common robustness gaps, 3 best-session patterns, and card system analysis
- Added: 11 new summary findings from session evidence (items 11-21 in Summary)
- Added: Section 6 "Recommendations for Robust Prompt Sequences" with 10 evidence-based recommendations
- Added: 11 internal sources (items 15-25) from session analysis
- Kept: All existing external research findings (Sections 1-4) unchanged

**[2026-09-12 18:50]**
- Initial research document created from web search on hang-prevention in CI/CD, agent frameworks, and process management
