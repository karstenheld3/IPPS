---
trigger: model_decision
description: When working with "Cascade" agent inside Devin IDE (not "Devin CLI" or "Devin Desktop" agents)
---

# Devin Cascade Rules

Agent-specific rules for the Cascade agent (Windsurf/Devin IDE chat panel agent). All IPPS agent-specific findings for the Devin product family come from Cascade. Excluded from sync to non-Devin agent repos.

**Scope gate**: Apply this file only if you are Cascade (your system prompt names you Cascade). If you are the Devin agent, ignore this file and follow `devin-devin.md`.

## Tool Constraints

- NEVER ask questions. NEVER use the `ask_user_question` tool. Resolve ambiguity through prompt analysis, not clarification requests
- The `ask_user_question` tool is FORBIDDEN. This includes all interactive prompt mechanisms. The only exception: when two interpretations lead to destructive, irreversible, and materially different outcomes
- `gesetze-im-internet.de`: Playwright only. `search_web` / `read_url_content` on this domain crash the conversation. Repeat this ban in prompts that research German law

## Terminal Limits

**Cascade terminal limit (2026-03-09):** Max 4 concurrent terminals. Additional terminals are queued/delayed.

Command rules: `agent-behavior.md` Terminal Hang Prevention (whitelist, supervised runner, monitoring, hang verdict, runtime check). Cascade tool specifics:

- Every `run_command`: `Blocking: false`, `WaitMsBeforeAsync` = (expected seconds + 5) * 1000, max 60000. The tool can miss the end of a finished command and can report a running command as done (both observed 2026-11-11); a blocking call can then wait forever
- No end line (`DONE`, `KILLED`, `ERROR`) in the runner log yet: `command_status` with `WaitDurationSeconds: 60`, then read the log again; repeat for as long as the `ALIVE` lines show progress (step 4). Never decide from `command_status` or terminal output alone, and never end a command because a wait count or a time limit is reached
- Runner gone: no `START` 60 s after the call, or no new `ALIVE` line for 90 s and no end line -> check the runner process (`pid=` in the `START` line, `Get-Process -Id`); gone -> end surviving processes of the command and record a Fails entry (completion miss or runner error). Runner alive -> only a hang verdict (step 5) ends the command
- Terminals are shared between concurrent Cascade conversations: tool output can contain another conversation's text, and a command reading stdin can receive another conversation's input
- Never open external terminals unless explicitly requested
- Terminal robustness variant: @skills:terminal-robustness `DevinCascade/`

## Tool-Call Payload Limit

Agent-tool robustness (what runs via agent tools), not terminal robustness (what runs in the terminal). Single source for Cascade; prompt sequences copy this section verbatim into the robustness card `## Agent tool limits` (PRMT-HS-11).

Cascade drops or stalls tool calls with large arguments: the call never executes, the generated content is lost, and the step appears to hang. Observed thresholds vary by session: failures at 3,000-4,000 tokens per call; in one session `edit` failed at 1,800-2,600 characters per `new_string` and succeeded in ~40 calls at 1,500 characters or less. The generic ~4,000-token limit in `agent-behavior.md` Large File Writes is too high for Cascade.

- Default: max ~6,000 characters (about 80 lines of prose) per tool call, counting ALL arguments: `CodeContent`, `old_string` + `new_string`, every entry of `multi_edit` `edits`, `new_source`
- After the first `invalid json in tool call: unexpected end of JSON input` error: max ~1,500 characters per string argument for the rest of the session
- This limit overrides any higher limit in rules, workflows, skills, or prompts (e.g. "split writes above ~4,000 tokens")
- `multi_edit` does NOT bypass the limit: all its edits travel in one tool call. Use one tool call per chunk
- New file: `write_to_file` with header and first section, then append each further section with `edit` using a short unique anchor as `old_string` (1-3 lines, e.g. `## Document History`) and anchor plus new section as `new_string`
- Rewrite of an existing file or section above the limit: write the new version in chunks to `_agentwork/.tmp_[name].md`, then replace the original with one inline `Move-Item -Force [tmp] [target]`. Never put a large section into `old_string`
- Before a multi-chunk write, announce `Writing [file] in [N] parts...` and report each finished part
- After a failed or stalled call: never resend the same payload. `read_file` the target tail to find the last chunk on disk, halve the chunk size, continue

JSON content: the Cascade tool-call serializer parses a string argument that is valid JSON as an object, and the call fails with `Invalid argument type for 'CodeContent': expected string but got object` (observed twice on one payload, two repos).

- Never pass a complete JSON document as `CodeContent`. New `.json` file: write a `_agentwork/.tmp_[name].ps1` that holds the JSON in a single-quoted here-string (`@'` ... `'@`) and writes it with `[System.IO.File]::WriteAllText([path], $json, [System.Text.UTF8Encoding]::new($false))`; run it per Terminal Limits
- Never use `ConvertTo-Json` to produce the file text: it drops the column alignment required by @skills:coding-conventions `JSON-RULES.md`. Write the formatted text verbatim
- Existing `.json` file: use `edit`. No `old_string` or `new_string` may be a complete JSON value on its own (`{...}`, `[...]`, a bare number or string); include the preceding key or a trailing comma so the argument is a fragment
- After every JSON write or edit: parse check in a tmp script (`Get-Content -Raw [path] | Test-Json`) and report the result. Write path plus parse check tested 2026-11-03: valid JSON, column alignment preserved
- On `expected string but got object`: never retry the same payload; switch to the tmp-script path

## Agent Folder Mapping

**[AGENT_FOLDER]** location for Cascade:
- `.devin/`

## Workspace Definition

- **[WORKSPACE]**: The Windsurf/VSCode workspace root folder

## Cascade-Specific Workflows

- `/switch-model` - Switch Cascade AI model tier (HIGH, MID, LOW)

## Cascade-Specific Skills

- `@devin-auto-model-switcher` - Switch Cascade AI model tier programmatically
