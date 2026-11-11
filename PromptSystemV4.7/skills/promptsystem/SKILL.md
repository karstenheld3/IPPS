---
name: promptsystem
description: Apply when doing planning for long-running tasks in sessions on top level (EDIRD phase model, gates, `/go`), when writing STRUT or phase plans with Agentic English verbs, when a rule file links here for details (utility folder standard, ID system), or when editing or compacting rule files
---

# PromptSystem

Full information behind the compact rule files in `[AGENT_FOLDER]/rules/`. A rule file holds the always-loaded short form. This skill holds the complete wording, rationale, and examples, and maps every rule section to its detail home.

## MUST-NOT-FORGET

- Rules win: a rule file states the binding short form; the files here complete it and never contradict it
- One home per concept: detail lives in exactly one file listed under Detail Map; a rule links to it and does not restate it
- Rule files stay below 11,800 bytes each: Cascade loads only about the first 12,000 bytes of an always-on rule file (observed 2026-11-11) and cuts off the rest without a warning
- Removing content from a rule: leave the generic concept and a link to the detail file in the same edit
- Section headings and step numbers of rules are cited by other files (e.g. `agent-behavior.md` Terminal Hang Prevention steps): search for citations before renaming or renumbering

## Intent Lookup

- **Create or name a utility folder, register a module folder, verify folder names** → `PROMPTSYSTEM_AGENT_FOLDERS.md`
- **Plan long-running work, run `/go`, check a phase gate, write the gate output** → `PROMPTSYSTEM_EDIRD.md`
- **Write a STRUT or phase plan with AGEN verbs, look up a verb, label, or state** → `PROMPTSYSTEM_AGENTIC_ENGLISH.md`
- **Assign a Doc ID, topic, nested ID, item ID, source ID, or tracking ID** → `PROMPTSYSTEM_IDS.md`
- **Edit or compact a rule file** → MUST-NOT-FORGET, then Detail Map

## Detail Map

Rule section → detail home:

- `agent-behavior.md` Agent-Created Folders → `PROMPTSYSTEM_AGENT_FOLDERS.md`
- `agent-behavior.md` Terminal Hang Prevention → @skills:terminal-robustness
- `agentic-english.md` → `PROMPTSYSTEM_AGENTIC_ENGLISH.md`
- `promptsystem-ids.md` → `PROMPTSYSTEM_IDS.md`
- `edird-phase-planning.md` → `PROMPTSYSTEM_EDIRD.md`
- `promptsystem-core.md` Folder Structure → @skills:workspace-management `WORKSPACE-GUIDES.md` section Folder Structure Trees
- `promptsystem-core.md` Document Placement → @skills:workspace-management `WORKSPACE-RULES.md` WS-DP-01 through WS-DP-06
- `promptsystem-core.md` STRUT Execution → @skills:write-documents `STRUT_TEMPLATE.md` section Execution Rules
- `core-conventions.md` Authoritative Literals → @skills:write-documents `APAPALAN_RULES.md` APAPL-PR-13
- `core-conventions.md` APAPALAN Writing Principle → @skills:write-documents `APAPALAN_RULES.md`, `MECT_WRITING_RULES.md`
- `tools-and-skills.md` Prompt Templates in NOTES.md → @skills:write-documents `PROMPTS_RULES.md` PRMT-CT-08

## References

- `PROMPTSYSTEM_EDIRD.md` - EDIRD phase model: phases, gates, workflow types, phase plans, effort allocation, stuck detection, gate output
- `PROMPTSYSTEM_AGENTIC_ENGLISH.md` - AGEN vocabulary: placeholders, verbs, labels, states
- `PROMPTSYSTEM_AGENT_FOLDERS.md` - utility folder standard: name anatomy, semantics, core roles, allowed parents, extension, generic consumers, migration
- `PROMPTSYSTEM_IDS.md` - ID system: number formats, topic registry, all ID types with rules and examples
