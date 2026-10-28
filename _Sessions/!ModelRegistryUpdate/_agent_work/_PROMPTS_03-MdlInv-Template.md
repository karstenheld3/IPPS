---
intended_model: glm-5.2
context_window_size: 1M
effort: high
prompt_system: IPPS
---

<!-- Budget: compressed 2026-10-28 19:45. Original plan had 6 prompts; compressed to 2 by merging template read+write+verify into one prompt and merging verify+status+commit. DD presentation moved to _PROMPTS_02 prompt 6; P2-S1+S2 folded there. Prerequisite: sub-chain 02 complete (P1 `[x]`, DD-01..05 presented).
Working folder is the session root. STRUT P5 is not in this file.
Planning document: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\_agent_work\__STRUT_MDLINVNTRY.md`. -->

## Prompt 7 - Full template: read rules, partition, write, verify

<!-- Merges P3-S1..S5. One prompt reads rules and exemplar, partitions update-model-registry.md, writes all template prompts, and self-verifies. -->

```
03-MdlInv-Template [ 01 / 02 ] - P3-S1..S5 Read rules and exemplar, partition, write all template prompts, verify

Session: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate`
Working folder: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate`

Read `_agent_work\__STRUT_MDLINVNTRY.md` (Plan P3 Strategy, MUST-NOT-FORGET), `T02_MDLINVNTRY_ReliableModelInventory_2026-10-28\_INFO_MDLRGUP-MDLINVNTRY-04_SourcesPerField.md`, `e:\dev\IPPS\.devin\workflows\write-template.md` (Prompts Template branch), and `_agent_work\__CARD_MDLINVNTRY-Findings.md`. Treat earlier conversation as compacted. Steps P3-S1..S5 (merged).
Planning document: `__STRUT_MDLINVNTRY.md`, step P3-S1..S5.

Objective: a complete prompts template that produces a dated prompts file for recurring model inventory updates, with all prompts filled, verified against TMPL-* and PRMT-*, ready for use.

1. Read rules: `e:\dev\IPPS\.devin\skills\write-documents\TEMPLATE_GUIDES.md`, `TEMPLATE_RULES.md`, `PROMPTS_TEMPLATE.md`, and Rule Index at top of `PROMPTS_RULES.md`. Note TMPL-* rules for prompts templates
2. Read exemplar: `e:\Dev\KarstensWorkspace\_Sessions\_!AINewsResearch\_PROMPTS_AI-News-Research_TEMPLATE.md` lines 1-110. Note: top comment structure, placeholder registry, run folder convention, bootstrap prompt, STOP gates, conditional pairs, context management
3. Read `e:\dev\IPPS\update-model-registry.md` (Phases 1-10, Distribution Targets, Archive Convention). Partition by load into: Prompt 1 Bootstrap (detect FULL|PRICES|NEWMODEL, create run folder, robustness card, generate instance) - Prompt 2 Phase 1 pre-flight + Phase 2 DOM extraction all providers including Google from -04 - Prompt 3 Phases 3-4 screenshots/transcription (FULL only, conditional) - Prompt 4 capability evidence Epoch+UC (conditional on DD-01) - Prompt 5 Phases 5-7 JSON updates with Gates - Prompt 6 Phase 8 tests + Phase 9.4 regeneration + Phase 10 report - Prompt 7 Phase 9 distribution (confirmation-gated) - Final Checkpoint
4. Write `_PROMPTS_ModelInventoryUpdate_TEMPLATE.md`: complete top comment block (filename, instance naming, purpose, run modes, run folder structure, placeholder registry, partition table, context management, "CRITICAL - Manual execution only"), frontmatter, ALL 8 prompts fully written (not skeletons), full example in XML comment for a PRICES run. Each prompt: marker, Session Anchor, numbered items calling `update-model-registry.md` phases by number, Constraints (idempotent, hang safety, no Phase 9 in prompts 2-6), Verify, STOP report
5. Self-verify: check the template against TMPL-AN-01, TMPL-ST-04, TMPL-ST-05, PRMT-FT-10, PRMT-SC-01, PRMT-SC-07, PRMT-SC-08 on the post-comment-removal view. Fix any findings inline. Fence length: 3 backticks unless prompt contains code block, then 4

Constraints:
- All file operations MUST stay within the declared working folder unless an absolute path outside it is explicitly named in this prompt; rule files and `update-model-registry.md` are read-only
- Do ONLY the numbered items above. Report any item you could not complete as NOT DONE
- `update-model-registry.md` stays the procedure of record: prompts invoke phases by number, not restate them
- Execute without asking for confirmation
- Re-running this prompt must not corrupt state: existing complete template is kept
- Hang safety: see `_agent_work\__CARD_MDLINVNTRY-Robustness.md`
- Timestamps from this prompt's request metadata

Findings card: Load and update `_agent_work\__CARD_MDLINVNTRY-Findings.md`. Append one Partition Observations line.

Closing: mark `P3-S1..S5` and `P3-D1` `[x]` in `_agent_work\__STRUT_MDLINVNTRY.md`; move to Done in `T02_MDLINVNTRY_ReliableModelInventory_2026-10-28\PROGRESS.md`.

Verify: template has 8 fenced prompts with markers `[ 01 / 08 ]` to `[ 08 / 08 ]`, every prompt has Session Anchor, Constraints, Verify, STOP line; Prompts 3+4 carry Conditional markers; Prompt 7 has confirmation constraint; full example resolves all Prompt 1+2 placeholders; every `[PLACEHOLDER]` in registry.

**STOP.** Report: items DONE / NOT DONE, placeholder count, TMPL/PRMT self-verify findings fixed.
```

---

## Prompt 8 - Close the 1 AWH run

<!-- Merges P4-S1..S3. Verify, record state, commit. P5 starts after DD answers. -->

```
03-MdlInv-Template [ 02 / 02 ] - P4-S1..S3 Verify, record session state, commit

Session: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate`
Working folder: `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate`

Read `_agent_work\__STRUT_MDLINVNTRY.md`, `NOTES.md`, `_agent_work\__CARD_MDLINVNTRY-Findings.md` (Partition Observations, Unresolved), `T02_MDLINVNTRY_ReliableModelInventory_2026-10-28\PROGRESS.md`, and `T02_MDLINVNTRY_ReliableModelInventory_2026-10-28\PROBLEMS.md`. Treat earlier conversation as compacted. Steps P4-S1..S3 (merged).
Planning document: `__STRUT_MDLINVNTRY.md`, step P4-S1..S3.

Objective: the next run can start STRUT P5 from the files alone: NOTES.md states phase, decisions, open items; STRUT shows checked steps and filled Time Log; everything committed.

1. Verify: this STRUT Planning and Transition contexts; T02 research set against `RESEARCH_RULES.md`. Max 2 gate cycles on failures; on second failure record in `PROBLEMS.md` and continue to items 2-4
2. Update `NOTES.md`: Current Phase (P1-P4 done, P5 gated on DD answers, open items, template path, Summary path); Key Decisions (DD answers if replied, else "answers pending")
3. Update STRUT: `P4-S1..S3` `[x]`, Objectives of P2-P4 `[x]` where linked Deliverables checked; Time Log intervals from findings card observations, net total vs 60 min budget, "Computed vs actual" line
4. Update `PROGRESS.md` (all steps Done, Progress Changes) and `PROBLEMS.md` (status of open entries). Commit: `git add` only `e:\dev\IPPS\_Sessions\!ModelRegistryUpdate\` and `e:\dev\IPPS\ID-REGISTRY.md`; message `docs(model-inventory): decisions presented, inventory update template, session state`; `git push`; mark `P4-D1`, `P4-D2` `[x]`

Constraints:
- All file operations MUST stay within the declared working folder unless an absolute path outside it is explicitly named
- Do ONLY the numbered items above. Report any item you could not complete as NOT DONE
- Do not start P5; do not edit files under `PromptSystemV4.5\` or `.devin\`
- Git: `--no-pager`, no `git add -A`, nothing under `_PrivateSessions_gitignore\`
- Execute without asking for confirmation
- If working tree clean and Current Phase dated today: report "already done" and stop
- Hang safety: see `_agent_work\__CARD_MDLINVNTRY-Robustness.md` (git 2-minute cap)
- Timestamps from this prompt's request metadata

Findings card: Load and update `_agent_work\__CARD_MDLINVNTRY-Findings.md`. Append one Partition Observations line.

Verify: `P3-D1` is `[x]` in STRUT. NOTES.md Current Phase dated today names P5 gated. STRUT Time Log has net total and "Computed vs actual" line. `git --no-pager status --short` clean under `_Sessions\!ModelRegistryUpdate\`. `git --no-pager log -1 --oneline` shows commit message.

**STOP.** Report: items DONE / NOT DONE, net minutes vs 60, items NOT DONE across sequence, commit hash, DD answers recorded or pending.
```
