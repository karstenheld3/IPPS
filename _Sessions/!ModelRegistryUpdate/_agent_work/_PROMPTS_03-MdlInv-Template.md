---
intended_model: glm-5.2
context_window_size: 1M
effort: high
prompt_system: IPPS
---

<!-- Budget (PROMPTS_GUIDES.md Section 1g): model row glm-5.2, label 26-D, profile guarded, effort high, WF 0.25 HWH, this file P2 + P3 + P4 = 3.0 HWH, computed 12 implementation prompts, chosen 4 (deviation and reasons stated in `_PROMPTS_01-MdlInv-Audit.md` opening commentary). Checkpoints after prompts 9-10 and after prompt 11 (template verification against TMPL-* and PRMT-*). Prerequisite: sub-chain 02 complete (P1 `[x]`, critique files exist).
Working folder is the session root: the template lives there (like the AI News exemplar), the T02 research files are read by absolute path. STRUT P5 (edits to PromptSystem files) is not in this file: it starts only after the user answers DD-01 to DD-05.
Planning document: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__STRUT_MDLINVNTRY.md`. -->

## Prompt 9 - Present the five decisions

```
03-MdlInv-Template [ 01 / 06 ] - P2-S1 P2-S2 Apply the critique and present DD-01 to DD-05

Session: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate`
Working folder: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate`

Read `_agent_work\__STRUT_MDLINVNTRY.md` (Plan P2), `T02_MDLINVNTRY_ReliableModelInventory_2026-10-28\_INFO_MDLRGUP-MDLINVNTRY-01_Summary.md` (section Decisions for [ACTOR]), `T02_MDLINVNTRY_ReliableModelInventory_2026-10-28\_INFO_MDLRGUP-MDLINVNTRY-05_WorkPerPromptOptions.md`, the two critique files beside them (`*_CRITIQUE.md`), `e:\dev\IPPS\.devin\rules\agent-behavior.md` section Presenting Decisions, and `_agent_work\__CARD_MDLINVNTRY-Findings.md`. Treat earlier conversation as compacted. Steps P2-S1, P2-S2.
Planning document: `__STRUT_MDLINVNTRY.md`, steps P2-S1, P2-S2.

Objective: the user receives five decisions that already account for the critique, each with exactly one recommendation and the evidence behind it, and can answer in one line.

1. For every HIGH or MEDIUM critique finding that touches a decision option or its recommendation: adjust the option text, implication, or recommendation in the Summary section "Decisions for [ACTOR]"; record each adjustment in the Summary Document History with the finding ID. Findings that do not change a decision: list them under "Critique findings not applied" with a one-line reason
2. Add to the Summary a section "Engineering Decisions (agent)" for choices without user-visible trade-off: layout of the rewritten inventory (one definitions block, one model table, one maintenance block), column order, and where a display-name alias table per agent environment lives (`windsurf-model-registry.json` for Devin; one file per environment) - one line of rationale each
3. Present DD-01 to DD-05 in chat, copied from the Summary, in the Presenting Decisions format (Problem, Context, Options with What / Why it works / Implication, one recommendation per decision), closing with the reply format `DD-01 a, DD-02 c, DD-03 a, DD-04 a, DD-05 a`
4. Add to `NOTES.md` section Key Decisions the line `DD-01..05 presented [timestamp]; answers pending` (replace it with the answers when they arrive)

Constraints:
- All file operations MUST stay within the declared working folder unless an absolute path outside it is explicitly named in this prompt
- Do ONLY the numbered items above. Do not refactor, rename, add tests, or touch files not listed. Report any item you could not complete as NOT DONE
- Do not decide for the user; do not edit any file under `e:\dev\IPPS\PromptSystemV4.5\` or `e:\dev\IPPS\.devin\`
- No `/reconcile` or `/implement` in this prompt; the critique is applied by judgment in item 1 (light input)
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state or waste cost: adjustments already recorded in the Document History are not applied twice
- Hang safety: no command may wait for a key, stdin, a pager, or an unbounded child. Banned list and caps: see `_agent_work\__CARD_MDLINVNTRY-Robustness.md`. On a cap: kill the process tree, record command and cap in `T02_MDLINVNTRY_ReliableModelInventory_2026-10-28\PROBLEMS.md`, continue
- Timestamps in all files come from this prompt's request metadata

Findings card: Load and update `_agent_work\__CARD_MDLINVNTRY-Findings.md`. File glitches, spec-code mismatches, and unexpected findings. Read at prompt startup for unresolved entries from prior prompts. Append one Partition Observations line for this prompt.

Closing: mark `P2-S1`, `P2-S2` `[x]` in `_agent_work\__STRUT_MDLINVNTRY.md` (P2-S3 and P2-D1 stay open until the user answers); move both to Done in `T02_MDLINVNTRY_ReliableModelInventory_2026-10-28\PROGRESS.md`.

Verify: Confirm `P1-S9` is `[x]` in `__STRUT_MDLINVNTRY.md` and both critique files exist. The Summary section "Decisions for [ACTOR]" has five decisions, each with exactly one option marked "(recommended" and a Why recommended line; "Engineering Decisions (agent)" has three entries; the Document History lists the applied critique findings. The chat output ends with the reply format line. `NOTES.md` Key Decisions has the "answers pending" line.

**STOP.** Report: items DONE / NOT DONE, critique findings applied / not applied, the five recommendations in one line.
```

---

## Prompt 10 - Template skeleton and load partition

<!-- Expected state: decisions presented (answers may still be pending; the template does not depend on them except the capability block, which is written as a conditional). -->

```
03-MdlInv-Template [ 02 / 06 ] - P3-S1 P3-S2 P3-S3 Read the template rules, analyze the exemplar, partition update-model-registry.md, write the skeleton

Session: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate`
Working folder: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate`

Read `_agent_work\__STRUT_MDLINVNTRY.md` (Plan P3 Strategy), `T02_MDLINVNTRY_ReliableModelInventory_2026-10-28\_INFO_MDLRGUP-MDLINVNTRY-04_SourcesPerField.md`, `e:\dev\IPPS\.devin\workflows\write-template.md` (Prompts Template branch), and `_agent_work\__CARD_MDLINVNTRY-Findings.md`. Treat earlier conversation as compacted. Steps P3-S1, P3-S2, P3-S3.
Planning document: `__STRUT_MDLINVNTRY.md`, steps P3-S1 to P3-S3.

Objective: the prompts template exists as a skeleton whose top comment block already fixes the run folder convention, run modes, placeholder registry, and the load-based partition of `update-model-registry.md` into prompts, with Prompt 1 (Bootstrap) complete, so that prompt 11 only fills the remaining prompts.

1. Read the rule files at `e:\dev\IPPS\.devin\skills\write-documents\`: `TEMPLATE_GUIDES.md`, `TEMPLATE_RULES.md`, `PROMPTS_TEMPLATE.md`, and the Rule Index at the top of `PROMPTS_RULES.md` (not the full file). Note the TMPL-* rules that apply to a prompts template (XML comment annotations, one instance of repeatable items, full example, placeholder registry)
2. Read `e:\Dev\KarstensWorkspace\_Sessions\_!AINewsResearch\_PROMPTS_AI-News-Research_TEMPLATE.md` lines 1-110. List in the new template's top comment the elements reused from it: top comment structure, placeholder registry, run folder `[SESSION_FOLDER]\_[DATE]_[RUN_MODE]\`, bootstrap prompt that generates the instance file without itself, STOP gates, conditional prompt pairs with renumbering, context management note
3. Read `e:\dev\IPPS\update-model-registry.md` (Phases 1-10, Distribution Targets, Archive Convention) and assess each phase on input volume, output volume, and reasoning depth. Record a partition table in the top comment: Prompt 1 Bootstrap (detect run mode FULL | PRICES | NEWMODEL, create run folder, create `_agent_work\__CARD_MDLRGUP-Robustness.md` from `e:\dev\IPPS\.devin\skills\terminal-robustness\DevinCascade\ROBUSTNESS_CARD_TEMPLATE.md` if missing, generate the instance file) - Prompt 2 Phase 1 pre-flight and Phase 2 DOM extraction for all providers including a new Google section derived from -04 - Prompt 3 Phases 3-4 screenshots and transcription (FULL only) - Prompt 4 capability evidence (Epoch ECI snapshot, release dates, Universal Class; conditional on DD-01) - Prompt 5 Phases 5-7 JSON updates with Gates 5-7 - Prompt 6 Phase 8 tests, Phase 9.4 inventory regeneration, Phase 10 report - Prompt 7 Phase 9 distribution to agent folder and external targets (separate, confirmation-gated) - Final Checkpoint (standalone `/verify` and `/fix` calls against the generated instance). State per prompt why the grouping fits one run (PRMT-SC-07)
4. Write `_PROMPTS_ModelInventoryUpdate_TEMPLATE.md` in the working folder: top comment block (filename, instance naming `_PROMPTS_[DATE]_ModelInventoryUpdate.md` in `[RUN_FOLDER]`, purpose, run modes, run folder structure with DOM extracts, screenshots, transcriptions, findings card, report inside the run folder and `model-sources\` declared read-only legacy, placeholder registry with every placeholder from the STRUT P3 Strategy plus `[RUN_FOLDER]` contents, usage, the partition table from item 3, context management note for a 200k-context model, "CRITICAL - Manual execution only" block, workflows and rules referenced), frontmatter `intended_model: [MODEL]`, `context_window_size: [CONTEXT]`, `effort: high`, `prompt_system: IPPS`, headings `## Prompt N - [title]` for Prompts 1-7 and `## Final Checkpoint` with a one-line XML comment objective each, and Prompt 1 Bootstrap complete (Prompt Marker, Session Anchor with `[SESSION_FOLDER]` and `[RUN_FOLDER]`, numbered items, constraints, Verify, STOP report)

Constraints:
- All file operations MUST stay within the declared working folder unless an absolute path outside it is explicitly named in this prompt; the paths in items 1-3 are read-only
- Do ONLY the numbered items above. Do not refactor, rename, add tests, or touch files not listed. Report any item you could not complete as NOT DONE
- Prompts 2-7 and the Final Checkpoint stay headings with objective comments only (prompt 11 fills them)
- `update-model-registry.md` stays the procedure of record: the template invokes phases by number, it does not restate their JavaScript or PowerShell
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state or waste cost: an existing template with a complete top comment and Prompt 1 is kept; only missing elements are added
- Hang safety: no command may wait for a key, stdin, a pager, or an unbounded child. Banned list and caps: see `_agent_work\__CARD_MDLINVNTRY-Robustness.md`. On a cap: kill the process tree, record command and cap in `T02_MDLINVNTRY_ReliableModelInventory_2026-10-28\PROBLEMS.md`, continue
- Timestamps come from this prompt's request metadata (templates carry no Document History)

Findings card: Load and update `_agent_work\__CARD_MDLINVNTRY-Findings.md`. File glitches, spec-code mismatches, and unexpected findings. Read at prompt startup for unresolved entries from prior prompts. Append one Partition Observations line for this prompt.

Closing: mark `P3-S1`, `P3-S2`, `P3-S3` `[x]` in `_agent_work\__STRUT_MDLINVNTRY.md`; move them to Done in `T02_MDLINVNTRY_ReliableModelInventory_2026-10-28\PROGRESS.md`.

Verify: Confirm `P2-S2` is `[x]` in `__STRUT_MDLINVNTRY.md`. `_PROMPTS_ModelInventoryUpdate_TEMPLATE.md` exists; its top comment contains a placeholder registry with at least 9 placeholders, a run folder structure, run modes, and a partition table with 8 rows (Prompts 1-7, Final Checkpoint); headings exist for all 8; Prompt 1 is a complete fenced prompt with marker `[ 01 / 08 ]`, Session Anchor, numbered items, Constraints, Verify, and a `**STOP.**` line.

**STOP.** Report: items DONE / NOT DONE, placeholder count, partition rows.
```

---

## Verification Checkpoint 6

<!-- Verify prompts 9-10 before the template is filled. -->

```
03-MdlInv-Template [ 03 / 06 ] - Verification checkpoint after prompts 9-10

Session: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate`
Working folder: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate`

Read `_agent_work\__CARD_MDLINVNTRY-Robustness.md`, `_agent_work\__STRUT_MDLINVNTRY.md`, and `_agent_work\__CARD_MDLINVNTRY-Findings.md`. Treat earlier conversation as compacted. Verification checkpoint after prompts 9-10.

/verify

current state against `__STRUT_MDLINVNTRY.md` steps P2-S1, P2-S2, P3-S1 to P3-S3; the Summary section "Decisions for [ACTOR]" against the Presenting Decisions format in `e:\dev\IPPS\.devin\rules\agent-behavior.md`; the template top comment and Prompt 1 against `TEMPLATE_RULES.md` (TMPL-AN-01, TMPL-ST-04) and PRMT-FT-10, PRMT-SC-01, PRMT-SC-08.

/fix

all gaps and remaining work. Max 2 gate cycles; on the second failure record the open items in `T02_MDLINVNTRY_ReliableModelInventory_2026-10-28\PROBLEMS.md` and stop.

**STOP.** Report: verify findings fixed / open.
```

---

## Prompt 11 - Fill the template prompts

<!-- Expected state: template skeleton with Prompt 1 complete and a verified partition table. -->

```
03-MdlInv-Template [ 04 / 06 ] - P3-S4 Write Prompts 2-7, the Final Checkpoint, and the full example

Session: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate`
Working folder: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate`

Read `_PROMPTS_ModelInventoryUpdate_TEMPLATE.md` (top comment, partition table, Prompt 1), `e:\dev\IPPS\update-model-registry.md` (phase headings, gates, Distribution Targets), `T02_MDLINVNTRY_ReliableModelInventory_2026-10-28\_INFO_MDLRGUP-MDLINVNTRY-04_SourcesPerField.md`, `e:\dev\IPPS\.devin\skills\write-documents\PROMPTS_TEMPLATE.md`, and `_agent_work\__CARD_MDLINVNTRY-Findings.md`. Treat earlier conversation as compacted. Step P3-S4.
Planning document: `__STRUT_MDLINVNTRY.md`, step P3-S4.

Objective: every prompt of the template is a complete fenced prompt that a filled instance can run unattended: self-contained opening, numbered items that call `update-model-registry.md` phases by number, constraints, Verify, STOP report; the capability prompt is marked conditional on DD-01; a full example shows placeholder resolution for one PRICES run.

1. Write Prompt 2 (Phase 1 pre-flight gate, Phase 2 DOM extraction for Anthropic, OpenAI, Z.AI, and Google; Google extraction method from -04; all extracts into `[RUN_FOLDER]`; Gate 2) and Prompt 3 (Phases 3-4 screenshots and transcription into `[RUN_FOLDER]`; `<!-- Conditional: FULL run mode only; remove for PRICES and NEWMODEL and renumber -->`)
2. Write Prompt 4 (`<!-- Conditional: DD-01 -->` capability evidence: Epoch ECI snapshot for every registry model via Playwright on `https://epoch.ai/eci`, release dates from provider announcements, Universal Class from vendor lineup role per the AINWSRCH "Model and Hardware Tiers" definitions; written to `[RUN_FOLDER]\[DATE]_Capability-Evidence.md`) and Prompt 5 (Phases 5-7 with Gates 5-7, change set from Phase 5.0, no removal of legacy entries)
3. Write Prompt 6 (Phase 8 tests for new enabled models, Phase 9.4 regeneration of `MODEL_INVENTORY.md` from the JSONs - rows, prices, capability fields per the DD-01 and DD-02 outcome placeholders `[CAPABILITY_FIELDS]` -, Phase 10 report saved as `[RUN_FOLDER]\[DATE]_Report.md`), Prompt 7 (Phase 9 distribution to `[AGENT_FOLDER]` and external targets; constraints: run only after the user confirms in chat; Gate 9), and the Final Checkpoint (standalone `/verify` and `/fix` calls against the Phase gates)
4. Add the full example at the end in an XML comment: a PRICES run on `[DATE]` = 2026-11-15 with all placeholders resolved for Prompt 1 and Prompt 2 only (TMPL-ST-05, one instance); add `<!-- Conditional -->` markers and the renumbering rule for removed prompts; keep every XML comment (this is the template, not an instance)

Each prompt: Prompt Marker `[NN]-ModelInventoryUpdate [ NN / 08 ] - [title]`, Session Anchor (`Session: [SESSION_FOLDER]`, `Working folder: [RUN_FOLDER]`), context-loading directive, "Treat earlier conversation as compacted", step identifier, numbered items (max 6), Constraints (working-folder constraint first; "Execute without asking for confirmation"; idempotency; hang safety referencing `[SESSION_FOLDER]\_agent_work\__CARD_MDLRGUP-Robustness.md` with Playwright 2-minute and transcription 10-minute caps; "Do not run Phase 9 distribution" in Prompts 2-6), Findings card `[RUN_FOLDER]\__CARD_MDLRGUP-Findings.md`, Verify (phase gate conditions), `**STOP.** Report:` line.

Constraints:
- All file operations MUST stay within the declared working folder unless an absolute path outside it is explicitly named in this prompt; `update-model-registry.md` and the skill files are read-only
- Do ONLY the numbered items above. Do not refactor, rename, add tests, or touch files not listed. Report any item you could not complete as NOT DONE
- Do not change Prompt 1 or the top comment except to correct a placeholder that items 1-4 introduce (then add it to the registry)
- Fence length: 3 backticks unless a prompt contains a code block, then 4 (PRMT-FT-02)
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state or waste cost: prompts already complete are kept; only missing prompts or sections are written
- Hang safety: no command may wait for a key, stdin, a pager, or an unbounded child. Banned list and caps: see `_agent_work\__CARD_MDLINVNTRY-Robustness.md`. On a cap: kill the process tree, record command and cap in `T02_MDLINVNTRY_ReliableModelInventory_2026-10-28\PROBLEMS.md`, continue
- Timestamps come from this prompt's request metadata

Findings card: Load and update `_agent_work\__CARD_MDLINVNTRY-Findings.md`. File glitches, spec-code mismatches, and unexpected findings. Read at prompt startup for unresolved entries from prior prompts. Append one Partition Observations line for this prompt.

Closing: mark `P3-S4` `[x]` in `_agent_work\__STRUT_MDLINVNTRY.md`; move it to Done in `T02_MDLINVNTRY_ReliableModelInventory_2026-10-28\PROGRESS.md`.

Verify: Confirm `P3-S3` is `[x]` in `__STRUT_MDLINVNTRY.md`. The template has 8 fenced prompts with markers `[ 01 / 08 ]` to `[ 08 / 08 ]`, `---` between consecutive prompts, every prompt has a Session Anchor, Constraints with "Execute without asking for confirmation", a Verify line, and a `**STOP.**` line; Prompts 3 and 4 carry Conditional markers; Prompt 7 contains the chat-confirmation constraint; the full example resolves every placeholder used in Prompts 1-2; every `[PLACEHOLDER]` in the file appears in the registry.

**STOP.** Report: items DONE / NOT DONE, prompt count, placeholders added to the registry.
```

---

## Verification Checkpoint 7 - Template

<!-- P3-S5: verify the template against TMPL-* and PRMT-* (post-comment-removal view), fix, no other work. -->

```
03-MdlInv-Template [ 05 / 06 ] - P3-S5 Verification checkpoint after prompt 11: template rules

Session: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate`
Working folder: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate`

Read `_agent_work\__CARD_MDLINVNTRY-Robustness.md`, `_agent_work\__STRUT_MDLINVNTRY.md` (Plan P3), and `_agent_work\__CARD_MDLINVNTRY-Findings.md`. Treat earlier conversation as compacted. Verification checkpoint after prompt 11, STRUT step P3-S5.

/verify

`_PROMPTS_ModelInventoryUpdate_TEMPLATE.md` against `TEMPLATE_RULES.md` (full audit checklist) and `PROMPTS_RULES.md` PRMT-FT, PRMT-ST, PRMT-SQ, PRMT-CT, PRMT-SC, PRMT-HS, PRMT-RB as they apply to the filled instance after XML comment removal (PRMT-FT-01 exception for the leading comment); and `__STRUT_MDLINVNTRY.md` step P3-S4 and deliverable P3-D1.

/fix

all gaps and remaining work. Max 2 gate cycles; on the second failure record the open items in `T02_MDLINVNTRY_ReliableModelInventory_2026-10-28\PROBLEMS.md` and stop. Then mark `P3-S5` and `P3-D1` `[x]` in `_agent_work\__STRUT_MDLINVNTRY.md`.

**STOP.** Report: TMPL and PRMT findings fixed / open.
```

---

## Prompt 12 - Close the 1 AWH run

<!-- P4: session state, time log, commit. P5 starts in a new prompts file after the user answers DD-01 to DD-05. -->

```
03-MdlInv-Template [ 06 / 06 ] - P4-S1 P4-S2 P4-S3 Record session state, time log, and commit

Session: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate`
Working folder: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate`

Read `_agent_work\__STRUT_MDLINVNTRY.md`, `NOTES.md`, `_agent_work\__CARD_MDLINVNTRY-Findings.md` (Partition Observations, Unresolved), `T02_MDLINVNTRY_ReliableModelInventory_2026-10-28\PROGRESS.md`, and `T02_MDLINVNTRY_ReliableModelInventory_2026-10-28\PROBLEMS.md`. Treat earlier conversation as compacted. Steps P4-S1 to P4-S3.
Planning document: `__STRUT_MDLINVNTRY.md`, steps P4-S1 to P4-S3.

Objective: the next run can start STRUT P5 from the files alone: the session NOTES.md states phase, decisions, and what is open; the STRUT shows checked steps and a filled Time Log; everything is committed.

1. Update `NOTES.md`: Current Phase entry with this prompt's timestamp - P1 to P4 done, P5 gated on DD answers, open items from PROBLEMS.md and the findings card Unresolved section, path of the template and of the T02 Summary; Key Decisions - the DD answers if the user has replied in chat or in NOTES.md, else keep "answers pending"
2. Update `_agent_work\__STRUT_MDLINVNTRY.md`: `P4-S1`, `P4-S2` `[x]` (P4-S3 after the commit), Objectives of P2 to P4 `[x]` where all linked Deliverables are checked; Time Log intervals - one line per executed prompt from the findings card Partition Observations minutes, net total against the 60-minute budget, and one line "Computed vs actual: 27 implementation prompts computed by PROMPTS_GUIDES.md 1g, 12 executed, items NOT DONE across all prompts: [N]"
3. Update `T02_MDLINVNTRY_ReliableModelInventory_2026-10-28\PROGRESS.md` (all P1 steps Done, Progress Changes entry) and `PROBLEMS.md` (status of every open entry; move resolved ones)
4. Commit: `git add` only files under `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\` and `e:\dev\IPPS\ID-REGISTRY.md`; message `docs(model-inventory): decisions presented, inventory update template, session state`; `git push`; then mark `P4-S3`, `P4-D1`, `P4-D2` `[x]` in the STRUT and amend nothing

Constraints:
- All file operations MUST stay within the declared working folder unless an absolute path outside it is explicitly named in this prompt
- Do ONLY the numbered items above. Do not refactor, rename, add tests, or touch files not listed. Report any item you could not complete as NOT DONE
- Do not start P5; do not edit any file under `e:\dev\IPPS\PromptSystemV4.5\` or `e:\dev\IPPS\.devin\`
- Git: `--no-pager` on every read command; no `git add -A`; nothing under `_PrivateSessions_gitignore\`
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state or waste cost: if the working tree is clean and the Current Phase entry carries today's date, report "already done" and stop
- Hang safety: no command may wait for a key, stdin, a pager, or an unbounded child. Banned list and caps: see `_agent_work\__CARD_MDLINVNTRY-Robustness.md` (git 2-minute cap). On a cap: kill the process tree, record command and cap in `T02_MDLINVNTRY_ReliableModelInventory_2026-10-28\PROBLEMS.md`, continue
- Timestamps come from this prompt's request metadata

Findings card: Load and update `_agent_work\__CARD_MDLINVNTRY-Findings.md`. File glitches, spec-code mismatches, and unexpected findings. Read at prompt startup for unresolved entries from prior prompts. Append one Partition Observations line for this prompt.

Verify: Confirm `P3-S5` is `[x]` in `__STRUT_MDLINVNTRY.md`. `NOTES.md` Current Phase has an entry dated today naming P5 as gated; the STRUT Time Log has a net total and the "Computed vs actual" line; `git --no-pager status --short` shows no changes under `_Sessions\!ModelRegistryUpdate\`; `git --no-pager log -1 --oneline` shows the commit message above.

**STOP.** Report: items DONE / NOT DONE, net minutes vs 60, items NOT DONE across the sequence, commit hash, DD answers recorded or pending.
```
