<!-- PROMPTS TEMPLATE
Filename: _PROMPTS_[NN]-[Topic].md
Location: session folder (default), workspace root, or user-specified path
Topic: [DomainShort]-[Purpose] where DomainShort is 2-8 CamelCase chars from STRUT/approach name, Purpose is short CamelCase description (PRMT-NM-04). Total under 30 chars. [NN]-[Topic] must be unique across session.

Read PROMPTS_GUIDES.md BEFORE writing. Verify against all PRMT-* rules in PROMPTS_RULES.md.
Remove ALL XML comments after creating the document. First non-empty line must be frontmatter (optional), Commentary, or opening fence.
Heading recommendation (PRMT-FT-07): use `## Prompt N - [title]` before each prompt for readability.
If headings are used, ALL prompts MUST have headings (consistency enforced).
Prompt Marker (PRMT-FT-10): all prompt sequences MUST include a file identifier prefix `[NN]-[Topic] [ NN / NN ]` as first line inside each prompt's fence, where `[NN]-[Topic]` is derived from the filename `_PROMPTS_[NN]-[Topic].md`. When using a planning document (PRMT-SC-06), marker includes plan summary: `[NN]-[Topic] [ NN / NN ] - [plan step ID] [brief summary]`.

Execution model (PRMT-EX-01/02): Each prompt is a separate turn for an execution engine. NEVER self-execute prompt files by running all prompts in one response. The writing agent creates the file; the execution engine runs it. -->

<!-- Optional Execution Frontmatter (PRMT-FT-08): YAML block at file start.
Provides execution hints to the execution engine. The engine MAY honor or override.
Omit entirely if no execution hints needed. Remove this block if not used.
Supported keys: intended_model, context_window_size, effort, prompt_system -->
---
intended_model: [model identifier, e.g., claude-sonnet-5]
context_window_size: [e.g., 200k, 128k, 1M]
effort: [low | medium | high | extra-high]
prompt_system: [e.g., IPPS]
---

<!-- Budget (PROMPTS_GUIDES.md Section 1g): model row [row], label [YY-L], profile [precise | standard | guarded], effort [level], WF (workload factor) [N] HWH (Human Work Hours), task [N] HWH, [N] implementation prompts, estimated cost $[N] -->

<!-- Simple prompt: 3-backtick fence when no inner code blocks.
Heading before the fence is optional but recommended (PRMT-FT-07). -->
## Prompt 1 - [short title]

```
[NN]-[Topic] [ 01 / NN ] - [short title]

Session: `[ABSOLUTE_SESSION_FOLDER_PATH]`
Working folder: `[ABSOLUTE_WORKING_FOLDER_PATH]`

Read [context-loading directive: files or cards to read]. Treat earlier conversation as compacted. Step [step identifier].
Planning document: [TASKS or STRUT filename], step [ID].

[Objective: what the finished state looks like (1-3 sentences)]

Constraints:
- All file operations MUST stay within the declared working folder unless an absolute path outside it is explicitly named in this prompt
- [What NOT to do]
- [Boundaries to respect]
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state or waste cost
- Hang safety: no command may wait for stdin, a pager, or an unbounded child. Banned: see `__CARD_[TOPIC]-Robustness.md`. [Time cap] cap. On cap: kill, record in PROBLEMS.md, continue.

Findings card: Load and update `__CARD_[TOPIC]-Findings.md`. File glitches, spec-code mismatches, and unexpected findings. Read at prompt startup for unresolved entries from prior prompts.

Verify: [Machine-checkable done criteria]
```

---

<!-- Commentary: purpose of next prompt and expected state from previous step.
For human readers only - never sent to model. Wrap in HTML comments per PRMT-FT-04.
Remove if no commentary needed. -->

<!-- Prompt with inner code blocks: 4-backtick fence. Outer must exceed deepest inner fence. -->
## Prompt 2 - [short title]

<!-- [Expected state from previous step and purpose of this prompt. Max 1 sentence in final files.] -->

````
[NN]-[Topic] [ 02 / NN ] - [short title]

Session: `[ABSOLUTE_SESSION_FOLDER_PATH]`
Working folder: `[ABSOLUTE_WORKING_FOLDER_PATH]`

Read [context-loading directive: files or cards to read]. Treat earlier conversation as compacted. Step [step identifier].
Planning document: [TASKS or STRUT filename], step [ID].

[Objective referencing output from previous prompt explicitly]

Example output format:
```[language]
[Representative example showing expected structure]
```

Constraints:
- All file operations MUST stay within the declared working folder unless an absolute path outside it is explicitly named in this prompt
- [What NOT to do]
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state or waste cost
- Hang safety: no command may wait for stdin, a pager, or an unbounded child. Banned: see `__CARD_[TOPIC]-Robustness.md`. [Time cap] cap. On cap: kill, record in PROBLEMS.md, continue.

Findings card: Load and update `__CARD_[TOPIC]-Findings.md`. File glitches, spec-code mismatches, and unexpected findings. Read at prompt startup for unresolved entries from prior prompts.

Verify: [Observable success criteria]
````

<!-- EXAMPLE: Reference only. Do not copy into new documents. Shows a completed 2-prompt file with optional frontmatter and headings (PRMT-FT-07/08). -->

## Full Example (2-prompt sequence, markers required (PRMT-FT-10))

`````markdown
---
intended_model: claude-sonnet-5
context_window_size: 1M
effort: high
prompt_system: IPPS
---

<!-- Budget (PROMPTS_GUIDES.md Section 1g): model row claude-sonnet-5, label 26-D, profile standard, effort high, WF 0.75 HWH, task 1.0 HWH, 2 implementation prompts, estimated cost $3.60 -->

## Prompt 1 - Security analysis

```
01-SecFix-Analysis [ 01 / 02 ] - Security analysis

Session: `E:\Dev\ProjectX\_2026-10-18_SecurityRemediation`
Working folder: `E:\Dev\ProjectX\_2026-10-18_SecurityRemediation`

Read `src/auth/` directory and `__CARD_00-Rules.md`. Treat earlier conversation as compacted. Step P1-S1.
Planning document: `__STRUT_SecurityFix.md`, step P1-S1.

Analyze the authentication module in src/auth/ for security vulnerabilities.
Focus on: token validation, session management, and password hashing.

Constraints:
- All file operations MUST stay within the declared working folder unless an absolute path outside it is explicitly named in this prompt
- Do not modify any code in this step
- Limit analysis to src/auth/ directory only
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state or waste cost
- Hang safety: no command may wait for stdin, a pager, or an unbounded child. Banned: see `__CARD_[TOPIC]-Robustness.md`. [Time cap] cap. On cap: kill, record in PROBLEMS.md, continue.

Findings card: Load and update `__CARD_[TOPIC]-Findings.md`. File glitches, spec-code mismatches, and unexpected findings. Read at prompt startup for unresolved entries from prior prompts.

Verify: Output a numbered list of findings with severity (HIGH/MEDIUM/LOW) and file location.
```

---

## Prompt 2 - Fix highest-severity finding

<!-- Previous step produced a numbered findings list. Fix the highest-severity item. -->

````
01-SecFix-Analysis [ 02 / 02 ] - Fix highest-severity finding

Session: `E:\Dev\ProjectX\_2026-10-18_SecurityRemediation`
Working folder: `E:\Dev\ProjectX\_2026-10-18_SecurityRemediation`

Read `src/auth/` and the findings list from `_INFO_SecurityAnalysis.md`. Treat earlier conversation as compacted. Step P1-S2.
Planning document: `__STRUT_SecurityFix.md`, step P1-S2.

Fix the highest-severity vulnerability identified in `_INFO_SecurityAnalysis.md`.

Example fix pattern:
```typescript
try {
  const token = jwt.verify(input, secret, { algorithms: ['HS256'] })
} catch (err) {
  return res.status(401).json({ error: 'Invalid token' })
}
```

Constraints:
- All file operations MUST stay within the declared working folder unless an absolute path outside it is explicitly named in this prompt
- Fix only the single highest-severity issue
- Do not change the public API of any exported function
- Do not add new dependencies
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state or waste cost
- Hang safety: no command may wait for stdin, a pager, or an unbounded child. Banned: see `__CARD_[TOPIC]-Robustness.md`. [Time cap] cap. On cap: kill, record in PROBLEMS.md, continue.

Findings card: Load and update `__CARD_[TOPIC]-Findings.md`. File glitches, spec-code mismatches, and unexpected findings. Read at prompt startup for unresolved entries from prior prompts.

Verify: Run `pnpm test:auth`. All tests pass. The specific vulnerability from step 1 is no longer present.
````
`````
