---
trigger: always_on
---

# Devin Agent Rules

Agent-specific rules for the Devin agent (not Cascade). IPPS has no tested findings for the Devin agent yet. Excluded from sync to non-Devin agent repos.

**Scope gate**: Apply this file only if you are the Devin agent (your system prompt names you Devin, not Cascade). If you are Cascade, ignore this file and follow `devin-cascade.md`.

## No Agent-Specific Findings Yet

- Cascade findings (`devin-cascade.md`) do NOT transfer to the Devin agent: different harness, different tools, untested limits
- Generic rules apply unchanged: `agent-behavior.md` Terminal Hang Prevention, Large File Writes, Attitude (no clarification questions)
- Terminal robustness variant: @skills:terminal-robustness `ClaudeCode/` (minimum variant: generic patterns, no tool-internals claims) until a Devin variant exists

## Tool-Call Payload Limit

Agent-tool robustness (what runs via agent tools). Single source for the Devin agent; prompt sequences copy this section verbatim into the robustness card `## Agent tool limits` (PRMT-HS-11).

- No tested limit. Use the generic limit in `agent-behavior.md` Large File Writes
- After a failed or stalled tool call: never resend the same payload. Read the target to find what reached disk, halve the chunk size, continue
- Record every stalled or dropped tool call with its approximate payload size in the session PROBLEMS.md, so a tested limit can be added here
- JSON content in write tools: untested. If a write fails with an argument-type error (string expected, object received), never retry the same payload; write the file from a `_agentwork/.tmp_[name].ps1` script (JSON text verbatim in a single-quoted here-string) and record the case in PROBLEMS.md

## Agent Folder Mapping

**[AGENT_FOLDER]** location for the Devin agent:
- `.devin/`

## Workspace Definition

- **[WORKSPACE]**: The workspace root folder the Devin agent operates in

## Not Applicable

- `/switch-model` and `@devin-auto-model-switcher` drive the Cascade model selector; do not use them as the Devin agent
