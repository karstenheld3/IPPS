# HANGBENCH: Terminal Hang Test Bench

Rollout gate for every change to `PromptSystemV4.7/skills/terminal-robustness/run-supervised.ps1` or the agent execution pattern (AGENTTERMINAL-SP01 FR-17). Versioned in IPPS, not synced downstream.

## Files

- `hang-cases.ps1` - 27 hang cases (HC-01..HC-27: hang, legitimate long-running, cancel), each traced to an observed incident or card ban
- `hangbench.ps1` - harness: runs every case under every selected solution with terminal-like pipes, counts survivors
- `wrappers.ps1` - in-house wrapper patterns under test
- `runner-tests.ps1` - runner contract tests (TC-01..TC-12 + fallback): log lines, UTF-8, exit codes, stop file, no deadline, kill script, `-Topic`
- `stream-test.ps1`, `live-probe.ps1`, `hook-candidate.ps1` - live output, completion detection, hook classification probes
- `results/` - run results (`full1` all solutions; `runner1`, `runner2` shipped runner with deadline; `runner3` without deadline; `runner5` without deadline, with kill script)

## Run

All commands run as tmp scripts in `_agentwork/` through the runner (`agent-behavior.md` Terminal Hang Prevention).

The shipped runner has no deadline. In hang cases the harness plays the agent and creates the stop file after `-HangCap` seconds (default 5); in the cancel case it runs the kill script after the cancel.

1. Setup once: tmp script calling `hangbench.ps1 -Setup`, expected 200 s. Downloads Process Governor (latest release) and creates `_download_gitignore/venv` with `processkit-py==1.5.0` (Python from PATH). Not versioned
2. Runner contract tests: tmp script calling `runner-tests.ps1`, expected 60 s (default supervisor: the bench venv). Gate: all PASS
3. Bench: tmp script calling `hangbench.ps1 -RunId <id> -Solutions runner,runnerfb`, expected 390 s. Gate: `runner` 27/27; `runnerfb` result recorded with failed case IDs. All solutions: omit `-Solutions` (about 30 min)
4. Report: `hangbench.ps1 -Report -RunId <id>` writes `results/<id>.md`
5. Record the result in `PromptSystemV4.7/skills/terminal-robustness/DevinCascade/TERMINAL_ROBUSTNESS_GUIDES.md` and in "Latest results" below

Live acceptance test in Cascade (cannot run in the bench): `_PROMPTS_99-HangAcceptance.md` in the session folder `_2026-11-11_PromptSequenceHangPrevention`; run one prompt per turn.

## Latest results (2026-11-11, run `runner5`)

- `runner` (processkit): 27/27 (HC-27 passes because the kill script is run after the cancel; without it 7 survivors, run `runner3`)
- `runnerfb` (no processkit): 25/27, failed HC-11, HC-21
- `runner-tests.ps1`: 14/14
