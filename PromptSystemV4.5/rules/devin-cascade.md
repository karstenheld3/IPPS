---
trigger: always_on
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

Command execution follows `agent-behavior.md` Terminal Hang Prevention and Batch Operations. Cascade specifics:

- Non-whitelisted commands: `run_command` runs only the `pwsh -NoProfile -NonInteractive -File _agentwork/.tmp_[purpose].ps1 > ... 2> ...` line; read results with `read_file`
- Use `run_command` with `Blocking: false` for parallel or slow tasks, poll with `command_status`
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
