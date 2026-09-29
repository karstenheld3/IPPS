# SPEC: Terminal Robustness Skill

**Doc ID**: TERMROBUSTNESS-SP01
**Feature**: TERMINAL_ROBUSTNESS_SKILL
**Goal**: Specify the placement, structure, and linkage of the terminal-robustness skill and robustness cards in IPPS
**Timeline**: Created 2026-09-29, Updated 0 times
**Target file(s)**:
- `PromptSystemV4.5/skills/terminal-robustness/` (authoring) and `.devin/skills/terminal-robustness/` (deployment mirror)
- `PromptSystemV4.5/rules/agent-behavior.md` + `.devin/rules/agent-behavior.md` (minimal rule section)
- `PromptSystemV4.5/workflows/write-prompts.md`, `verify.md` + `.devin/` mirrors (workflow hooks)
- `PromptSystemV4.5/skills/write-documents/PROMPTS_ROBUSTNESS_GUIDES.md` + `.devin/` mirror (trim)
- `ID-REGISTRY.md` (topic TERMROBUSTNESS)

**Depends on:**
- `specs/_SPEC_GRUC_STANDARD.md [GRUC-SP01]` for GRUC file types, consumer mapping, and placement rules
- `specs/_SPEC_IPPS_SKILLS.md [IPPSSKLS-SP01]` for skill anatomy and required files
- `specs/_SPEC_IPPS_WORKFLOWS.md [IPPSWFLW-SP01]` for workflow GRUC consumption rules

**Does not depend on:**
- `specs/_SPEC_IPPS_KNOWLEDGE_BUNDLE_FORMAT.md [IPPSSKBNDL-SP01]` (knowledge bundle placement was a rejected alternative, see TERMROBUSTNESS-DD-01)

## MUST-NOT-FORGET

- Rules carry minimal instructions and link out; no mechanism detail in `agent-behavior.md`
- GRUC-FR-14 compliance: skill files do not cross-link other skills' GRUC files; workflows do the pointing
- No EXAMPLE files in the skill; skeleton at root, re-usable templates in agent subfolders
- ClaudeCode variant ships only generic verified patterns; no claims about Claude Code tool internals (no empirical findings exist for that agent)
- Both copies must stay in sync: `PromptSystemV4.5/` (authoring) and `.devin/` (deployment)
- `check_workflow_refs.ps1` must pass after all changes

## Table of Contents

1. [Scenario](#1-scenario)
2. [Context](#2-context)
3. [Domain Objects](#3-domain-objects)
4. [Functional Requirements](#4-functional-requirements)
5. [Non-Functional Requirements](#5-non-functional-requirements)
6. [Design Decisions](#6-design-decisions)
7. [Implementation Guarantees](#7-implementation-guarantees)
8. [Placement and Link Map](#8-placement-and-link-map)
9. [Key Mechanisms](#9-key-mechanisms)
10. [Action Flow](#10-action-flow)
11. [Technical Constraints](#11-technical-constraints)
12. [Document History](#12-document-history)

## 1. Scenario

**Problem:**
- Agents issue terminal commands that hang sessions indefinitely. The Windsurf terminal tool waits for pipe EOF on all streams, so background processes inheriting std handles hang the terminal; PowerShell `2>&1` creates a merge point that crashes with OutOfMemoryException and a corrupted exit code; verbose stderr throttles at ~2.3KB/s against a 4KB pipe buffer
- The confirmed mechanisms exist only in a session investigation log; no agent-facing knowledge file carries them
- The robustness card concept exists only inside the write-prompts domain (`PROMPTS_ROBUSTNESS_GUIDES.md`, `PROMPTS_EXAMPLE_02`); an agent running commands in regular chat mode has no path to it
- Rules files carry scattered terminal advice without links to deeper knowledge

**Solution:**
- New skill `terminal-robustness` with a full GRUC set, an agent dispatch dimension (ClaudeCode minimum, DevinCascade full findings), and re-usable robustness card templates
- Robustness cards become durable project artifacts: copied from an agent template, extended per project, consumed by both chat-mode agents and prompt sequences, verified against a shared skeleton
- A minimal rule section in `agent-behavior.md` links to the skill; workflow hooks in `write-prompts.md` and `verify.md` integrate the card lifecycle

**What we don't want:**
- Fat rule files duplicating mechanism detail (rules stay minimal, links carry the depth)
- Card knowledge maintained in two skills (drift risk)
- Filled example files inside the skill (skeleton + re-usable templates only)
- Unverified claims about Claude Code tool internals
- Interactive chat sessions left uncovered (prompt-sequence-only protection)

### Architecture Diagram

```
IPPS
├─> rules/agent-behavior.md ............. minimal bans + link (chat-mode entry)
│
├─> skills/terminal-robustness/
│   ├─> SKILL.md ....................... entry + agent dispatch
│   ├─> shared GRUC (GUIDES/RULES/CHECKS)
│   ├─> ROBUSTNESS_CARD_SKELETON.md ..... canonical structure (/verify target)
│   ├─> ClaudeCode/ .................... minimum variant
│   │   ├─> TERMINAL_ROBUSTNESS_GUIDES.md
│   │   └─> ROBUSTNESS_CARD_TEMPLATE.md (re-usable, copy + extend)
│   └─> DevinCascade/ .................. full-findings variant
│       ├─> TERMINAL_ROBUSTNESS_GUIDES.md
│       └─> ROBUSTNESS_CARD_TEMPLATE.md (re-usable, copy + extend)
│
├─> workflows/write-prompts.md .......... hook: card-driven hang-safety planning
├─> workflows/verify.md ................. hook: card instances checked vs skeleton
├─> skills/write-documents/
│   └─> PROMPTS_ROBUSTNESS_GUIDES.md .... trimmed: clause + findings directive
└─> .devin/ ............................. deployment mirror of all above
```

## 2. Context

- The empirical basis is the TERMROBUSTNESS investigation (`_LOG_TERMROBUSTNESS.md`, session `_2026-09-29_TerminalRobustnessSkill`): 24 log entries (I001.001-I001.020 investigation, I001.021-I001.024 process notes), cause-effect matrix in I001.020, confirmed mechanisms with probe evidence
- IPPS is the sync source: content is authored in `PromptSystemV4.5/`, mirrored to `.devin/`, and synced downstream to consumer workspaces. Placement decisions here propagate to all agents
- The GRUC standard (`_SPEC_GRUC_STANDARD.md`) constrains file placement: GUIDE → working agent + `/critique`; RULES + TEMPLATE → `/verify`; CHECKS PD → `/drift-detect`; CHECKS QI → `/improve`. GRUC files live in the skill folder they belong to
- `PROMPTS_ROBUSTNESS_GUIDES.md` already contains the hang-safety clause template and findings-card directive consumed by `write-prompts.md` (PRMT-HS-01). The clause stays there; mechanism depth moves to the new skill

## 3. Domain Objects

### Terminal Robustness Skill

The skill folder `terminal-robustness` under `skills/`. Teaches agents how to prevent hanging terminal commands in both chat mode and prompt sequences.

**Storage:** `PromptSystemV4.5/skills/terminal-robustness/` (authoring), `.devin/skills/terminal-robustness/` (deployment)
**Entry:** `SKILL.md`

**Key properties:**
- Contains one GRUC set (GUIDES, RULES, CHECKS) shared across agents
- Contains one card skeleton and two agent variants
- No EXAMPLE files

### Shared GRUC Files

`TERMINAL_ROBUSTNESS_GUIDES.md`, `TERMINAL_ROBUSTNESS_RULES.md`, `TERMINAL_ROBUSTNESS_CHECKS.md`. Agent-independent content: OS-level mechanisms, card concept, consumption modes, HG/EX/CD rules, PD/QI audits.

### Card Skeleton

`ROBUSTNESS_CARD_SKELETON.md`. Pure structural skeleton: section names and placeholders, no default content. Defines the canonical card structure; the target `/verify` checks card instances against.

### Agent Variant

A subfolder (`ClaudeCode/` or `DevinCascade/`) containing `TERMINAL_ROBUSTNESS_GUIDES.md` (agent-specific guidance) and `ROBUSTNESS_CARD_TEMPLATE.md` (re-usable card with agent-appropriate default content). Same filenames in both variants; folder path disambiguates.

### Robustness Card Instance

`__CARD_[TOPIC]-Robustness.md` in a project or session folder. Created by copying the agent's `ROBUSTNESS_CARD_TEMPLATE.md` and extending it with project-specific banned commands, time caps, and rules. Consumed by chat-mode agents and prompt sequences; verified against the skeleton.

### Minimal Rule Section

A "Terminal Hang Prevention" section in `agent-behavior.md`: hard bans only (no `2>&1` on stderr-heavy commands, no unbounded background children, no stdin/pager waits) plus one link to the skill. Maximum 10 lines.

### Workflow Hook

A reference from a workflow file to the skill: `write-prompts.md` (Required Skills + Step 1 hang-safety planning), `verify.md` (Required Skills + card-instance verification). Workflows point to skills; skill files never point to other skills' GRUC files.

## 4. Functional Requirements

**TERMROBUSTNESS-FR-01: Skill Placement and Mirror**

- Skill authored at `PromptSystemV4.5/skills/terminal-robustness/`
- Mirrored verbatim to `.devin/skills/terminal-robustness/`
- Mirror verified by file-count and content comparison after authoring

**TERMROBUSTNESS-FR-02: Shared GRUC Set**

- `SKILL.md`: goal, overview, GRUC placement map, agent dispatch procedure, references section listing all companion files
- `TERMINAL_ROBUSTNESS_GUIDES.md`: OS-level mechanisms, safe-pattern decisions, card concept, both consumption modes
- `TERMINAL_ROBUSTNESS_RULES.md`: rule index + BAD/GOOD pairs; categories HG (hang guards), EX (execution patterns), CD (card definition)
- `TERMINAL_ROBUSTNESS_CHECKS.md`: PD items (action + evidence + failure indicator + rule references) and QI items (question + improvement tip)

**TERMROBUSTNESS-FR-03: Agent Dispatch**

- `SKILL.md` contains a dispatch step: determine the active agent, then load `ClaudeCode/` or `DevinCascade/` variant files in addition to shared files
- Dispatch keys on the agent folder in use (`.claude/` vs `.devin/`) or explicit context

**TERMROBUSTNESS-FR-04: Card Skeleton**

- `ROBUSTNESS_CARD_SKELETON.md` at skill root contains only section names and placeholders: Banned Commands, Time Caps, Always Rules, On-Cap Behavior, Kill Procedure, Findings Feed
- No agent-specific or project-specific content

**TERMROBUSTNESS-FR-05: Agent Variants**

- `ClaudeCode/TERMINAL_ROBUSTNESS_GUIDES.md`: minimum - generic bans, redirect-to-file pattern, time caps. No claims about Claude Code tool internals
- `DevinCascade/TERMINAL_ROBUSTNESS_GUIDES.md`: full empirical findings - pipe-EOF completion semantics, ~4KB pipe buffer with ~2.3KB/s stderr drain, `2>&1` merge-point OutOfMemoryException and exit-code corruption, grandchild handle inheritance, long-command echo mangling, non-blocking execution + status polling pattern
- Each variant contains `ROBUSTNESS_CARD_TEMPLATE.md`: re-usable card with agent-appropriate defaults, designed to be copied and extended per project

**TERMROBUSTNESS-FR-06: Depth Policy**

- ClaudeCode variant: only generic, verified patterns (stdin/pager bans, redirect-to-file, caps, tree-kill). Every claim must hold for any terminal tool
- DevinCascade variant: full findings, each mechanism traceable to a `_LOG_TERMROBUSTNESS.md` entry ID

**TERMROBUSTNESS-FR-07: Minimal Rule Section**

- `agent-behavior.md` gains "Terminal Hang Prevention" (max 10 lines): three hard bans + link `@skills:terminal-robustness TERMINAL_ROBUSTNESS_GUIDES.md`
- No mechanism explanation in the rule; the link carries it

**TERMROBUSTNESS-FR-08: write-prompts Hook**

- `write-prompts.md` Required Skills lists `@skills:terminal-robustness`
- Step 1 hang-safety planning becomes card-driven: if the project has a robustness card, banned lists and caps come from it; if not, create one by copying the agent's `ROBUSTNESS_CARD_TEMPLATE.md` and extending it
- The hang-safety clause template itself remains in `PROMPTS_ROBUSTNESS_GUIDES.md`

**TERMROBUSTNESS-FR-09: verify Hook**

- `verify.md` Required Skills lists `@skills:terminal-robustness` for robustness-card and terminal-command verification contexts
- Card instances are verified against `ROBUSTNESS_CARD_SKELETON.md` structure and TERMROBUSTNESS-CD rules

**TERMROBUSTNESS-FR-10: drift-detect Hook**

- `/drift-detect` consumes `TERMINAL_ROBUSTNESS_CHECKS.md` PD items to audit terminal command patterns in any session

**TERMROBUSTNESS-FR-11: PROMPTS_ROBUSTNESS_GUIDES Trim**

- Keeps: hang-safety clause template, findings-card directive
- Removes: mechanism depth and banned-list rationale (now maintained in the skill)
- Points to the skill conceptually; the workflow (`write-prompts.md`) provides the file-level link

**TERMROBUSTNESS-FR-12: Card Instance Naming and Lifecycle**

- Instances named `__CARD_[TOPIC]-Robustness.md`, created in project or session root
- Lifecycle: copy agent template → extend with project entries → consume (chat + prompts) → verify against skeleton → audit via CHECKS

**TERMROBUSTNESS-FR-13: Dual Consumption Modes**

- The shared guide documents both modes: chat mode (load guide before risky commands; read project card if present) and prompt-sequence mode (card injected via hang-safety clause, loaded at prompt startup)

**TERMROBUSTNESS-FR-14: Registry Entry**

- `ID-REGISTRY.md` contains topic `TERMROBUSTNESS` with description and datestamp

**TERMROBUSTNESS-FR-15: Reference Integrity**

- All added references resolve; `check_workflow_refs.ps1` passes after implementation

## 5. Non-Functional Requirements

**TERMROBUSTNESS-NFR-01: Context Cost**
- Minimal rule section in `agent-behavior.md` stays under 10 lines
- Verification: line count during implementation and `/verify`

**TERMROBUSTNESS-NFR-02: No Duplication**
- No mechanism text appears in both `write-documents` and `terminal-robustness`
- Verification: text search for mechanism keywords across both skills during `/verify`

**TERMROBUSTNESS-NFR-03: Skeleton-Template Structural Equality**
- Every section in `ROBUSTNESS_CARD_SKELETON.md` maps 1:1 to a section in each agent `ROBUSTNESS_CARD_TEMPLATE.md` (templates = skeleton + default content)
- Verification: section-name comparison during `/verify`

## 6. Design Decisions

**TERMROBUSTNESS-DD-01: Skill over rule file or knowledge bundle.** A dedicated skill was chosen over extending `agent-behavior.md` (rules must stay minimal) and over a knowledge bundle (bundles are reference docs without GRUC structure - no CHECKS for `/drift-detect`, no RULES for `/verify`). Rationale: correct domain (terminal work, not document writing), proper GRUC lifecycle, syncs downstream as a unit.

**TERMROBUSTNESS-DD-02: Naming.** Skill folder `terminal-robustness`; shared files prefixed `TERMINAL_ROBUSTNESS_`; registry topic `TERMROBUSTNESS` (14 chars, registry allows no underscore); root skeleton named `ROBUSTNESS_CARD_SKELETON.md`; agent templates named `ROBUSTNESS_CARD_TEMPLATE.md`. Rationale: full words, no abbreviations; skeleton vs template names distinguish pure structure from re-usable starting point.

**TERMROBUSTNESS-DD-03: Agent dimension as subfolders.** `ClaudeCode/` (minimum) and `DevinCascade/` (full findings) hold agent-specific guides and card templates; identical filenames, path disambiguates. Rationale: content depth differs per agent because empirical findings exist only for DevinCascade; unverified claims must not ship for ClaudeCode.

**TERMROBUSTNESS-DD-04: No EXAMPLE files.** The earlier plan moved `PROMPTS_EXAMPLE_02-RobustnessCard.md` into the skill; rejected. Root holds only the skeleton; agent folders hold re-usable templates that absorb the `[TESTED]` default content (banned-list entries, two-tier execution, tree-kill). Rationale: fewer files; template defaults replace the example's illustration purpose.

**TERMROBUSTNESS-DD-05: Rules minimal + link.** `agent-behavior.md` carries bans and a link only. Rationale: rules are always in context; mechanism depth would inflate every session's token budget.

**TERMROBUSTNESS-DD-06: Card concept ownership moves to terminal-robustness.** The robustness card is a terminal-execution artifact, not a prompt-writing artifact. `PROMPTS_EXAMPLE_02-RobustnessCard.md` retirement (delete + absorb `[TESTED]` content into the DevinCascade template defaults) is recommended; decision pending [ACTOR]. Rationale: one home per concept; the example's card content would otherwise be maintained in two places.

**TERMROBUSTNESS-DD-07: Evidence traceability.** DevinCascade guide cites `_LOG_TERMROBUSTNESS.md` entry IDs for each mechanism. Rationale: claims stay verifiable; future refutations can be traced to the evidence that produced them.

**TERMROBUSTNESS-DD-08: Workflows point, skills do not.** `write-prompts.md` and `verify.md` reference `@skills:terminal-robustness`; no skill-internal file links another skill's GRUC files. Rationale: GRUC-FR-14 self-containment compliance; workflows already reference skills freely.

## 7. Implementation Guarantees

**TERMROBUSTNESS-IG-01:** Every banned command and time cap in agent card templates is traceable to a TERMROBUSTNESS log entry, an existing `[TESTED]` pattern, or a generic stdin/pager/child-process rule

**TERMROBUSTNESS-IG-02:** The ClaudeCode variant contains no DevinCascade-specific mechanism (pipe-EOF semantics, drain rates, merge-point OOM, echo mangling)

**TERMROBUSTNESS-IG-03:** The hang-safety clause template in `PROMPTS_ROBUSTNESS_GUIDES.md` references cards by filename pattern without duplicating card structure

**TERMROBUSTNESS-IG-04:** After implementation, a session can create a valid card by copying an agent template, and `/verify` can check that card against the skeleton without reading any write-documents file

## 8. Placement and Link Map

Authoritative map of where terminal-robustness information lives and how it is linked in IPPS.

### New files

- `PromptSystemV4.5/skills/terminal-robustness/SKILL.md` + `.devin/` mirror - entry point, agent dispatch, references section
- `.../TERMINAL_ROBUSTNESS_GUIDES.md` + mirror - shared mechanisms, card concept, consumption modes
- `.../TERMINAL_ROBUSTNESS_RULES.md` + mirror - HG/EX/CD rules with BAD/GOOD pairs
- `.../TERMINAL_ROBUSTNESS_CHECKS.md` + mirror - PD + QI items
- `.../ROBUSTNESS_CARD_SKELETON.md` + mirror - canonical card structure
- `.../ClaudeCode/TERMINAL_ROBUSTNESS_GUIDES.md` + mirror - minimum variant guide
- `.../ClaudeCode/ROBUSTNESS_CARD_TEMPLATE.md` + mirror - minimum re-usable card
- `.../DevinCascade/TERMINAL_ROBUSTNESS_GUIDES.md` + mirror - full-findings guide (log-cited)
- `.../DevinCascade/ROBUSTNESS_CARD_TEMPLATE.md` + mirror - full re-usable card

### Changed files

- `rules/agent-behavior.md` (both copies) - add "Terminal Hang Prevention" section: 3 bans + link to skill guide
- `workflows/write-prompts.md` (both copies) - Required Skills entry + Step 1 card-driven hang-safety planning
- `workflows/verify.md` (both copies) - Required Skills entry + card-instance verification against skeleton
- `skills/write-documents/PROMPTS_ROBUSTNESS_GUIDES.md` (both copies) - trim mechanism depth to clause + findings directive
- `ID-REGISTRY.md` - topic TERMROBUSTNESS (done 2026-09-29)

### Link graph

```
agent-behavior.md ──────────── link ──> skills/terminal-robustness (GUIDES)
write-prompts.md ── reference ───────> skills/terminal-robustness (GUIDES + agent TEMPLATE)
verify.md ───────── reference ────────> skills/terminal-robustness (RULES + SKELETON)
drift-detect ────── consumes ─────────> skills/terminal-robustness (CHECKS PD)
improve ─────────── consumes ─────────> skills/terminal-robustness (CHECKS QI)
SKILL.md ────────── dispatch ────────> ClaudeCode/ | DevinCascade/ variants
PROMPTS_ROBUSTNESS_GUIDES.md ── concept reference to cards (no file-level cross-skill link)
```

### Content sources

- Mechanisms and evidence: `_LOG_TERMROBUSTNESS.md` I001.001-I001.024 (session `_2026-09-29_TerminalRobustnessSkill`)
- Investigation list and cross-repo context: `_INFO_TERMROBUSTNESS-01_HangingCommandInvestigation.md` (TERMROBUSTNESS-IN01)
- Card default content: `[TESTED]` patterns from the retired `PROMPTS_EXAMPLE_02-RobustnessCard.md`, absorbed into `DevinCascade/ROBUSTNESS_CARD_TEMPLATE.md` (DD-06 executed)
- Clause template (stays): `PROMPTS_ROBUSTNESS_GUIDES.md` Section 2

### Out of scope

- Downstream sync to consumer workspaces (separate `/sync` step)
- `.claude/` deployment folder setup (currently empty; deployment mechanics tracked separately)

## 9. Key Mechanisms

- **Agent dispatch**: `SKILL.md` determines the active agent and points to the variant subfolder; shared files load regardless of agent
- **Card lifecycle**: copy agent template → name `__CARD_[TOPIC]-Robustness.md` → extend with project bans/caps → consume in chat + prompts → verify against skeleton → audit via CHECKS
- **Two-template system**: skeleton (root, pure structure, `/verify` target) vs re-usable template (agent folder, default content, copy source). Templates must stay structurally equal to the skeleton
- **Link discipline**: rules and workflows carry the pointers; skill files never reference other skills' GRUC files

## 10. Action Flow

Chat mode (agent runs commands, no workflow active):
```
Agent about to run risky command
├─> agent-behavior.md Terminal Hang Prevention (always in context)
│   ├─> hard bans enforced
│   └─> link ──> TERMINAL_ROBUSTNESS_GUIDES.md
│       ├─> shared mechanisms + safe patterns
│       └─> SKILL.md dispatch ──> agent variant guide
└─> project card (if present) ──> banned list + caps for this project
```

Prompt sequence (write-prompts flow):
```
/write-prompts Step 1
├─> Required Skills ──> @skills:terminal-robustness
├─> card check: project has __CARD_*-Robustness.md?
│   ├─> yes ──> banned lists + caps from card
│   └─> no ──> copy agent ROBUSTNESS_CARD_TEMPLATE.md ──> extend ──> card created
└─> hang-safety clause (PROMPTS_ROBUSTNESS_GUIDES.md) references card
```

Verification flow:
```
/verify (card instance in scope)
├─> TERMROBUSTNESS-CD rules (structure, completeness)
└─> ROBUSTNESS_CARD_SKELETON.md (section adherence)
```

## 11. Technical Constraints

- GRUC consumer mapping applies (GRUC-SP01): one GRUC type per workflow, `/verify` gets RULES + TEMPLATE, CHECKS invisible during execution
- All content authored in `PromptSystemV4.5/`, mirrored to `.devin/`; no content only in the mirror
- Rule IDs use the TERMROBUSTNESS prefix with HG/EX/CD categories; file names use the `TERMINAL_ROBUSTNESS_` prefix
- `check_workflow_refs.ps1` is the reference-integrity gate
- No file may be created only in `.devin/` without a `PromptSystemV4.5/` source
- Documented exceptions to `SKILL_RULES.md` (SK-FL-01, SK-FL-07): agent variant subfolders (`ClaudeCode/`, `DevinCascade/`) override the flat-layout rule per TERMROBUSTNESS-DD-03 - the agent dimension requires subfolders regardless of file count; `ROBUSTNESS_CARD_TEMPLATE.md` and `ROBUSTNESS_CARD_SKELETON.md` use [ACTOR]-mandated names instead of the `_TEMPLATE` suffix convention - the TEMPLATE marker is present and distinguishes template from operational file, satisfying the rule's intent

## 12. Document History

**[2026-09-29 15:50]**
- Verified (/verify, skill context): 5 findings fixed - F1 private session path in DevinCascade guide replaced with spec-based provenance; F2 log-filename citations genericized in RULES CD-03 and DevinCascade template; F3+F4 SK-FL-01/SK-FL-07 exceptions documented in Technical Constraints; F5 meaningless `compatibility: all` frontmatter removed. All SK-*, IPPSSKLS-FR, GRUC-FR/AC, TERMROBUSTNESS-FR/IG/NFR checks pass

**[2026-09-29 15:35]**
- Implemented: all 9 skill files created in `PromptSystemV4.5/skills/terminal-robustness/`, mirrored to `.devin/` (9 files verified)
- Implemented: `agent-behavior.md` Terminal Hang Prevention section (6 lines + link), `write-prompts.md` + `verify.md` hooks, `PROMPTS_ROBUSTNESS_GUIDES.md` trimmed to prompt-integration layer (659 → 447 lines)
- Removed: `PROMPTS_EXAMPLE_02-RobustnessCard.md` (DD-06 executed: retire + absorb; `[TESTED]` content lives in `DevinCascade/ROBUSTNESS_CARD_TEMPLATE.md`)
- Verified: `check_workflow_refs.ps1` passes; zero stale references (EXAMPLE_02, HANGTERM/HANGCAUS)

**[2026-09-29 14:45]**
- Initial specification created from session design discussion (DD-TERMROBUSTNESS-01/02/03/04 decision series)

