# INFO: IPPS AGEN Workflow Syntax - Concept A Verb Sentences

**Doc ID**: AGENSYNTAX-IN03
**Goal**: Work out Concept A (verb sentences) into one learnable AGEN invocation language for all IPPS workflows: word classes, grammar, term snapping, skill binding without replication, signatures that survive workflow-to-skill migration, command conflicts with Claude Code, Devin, and Codex, and a preview of all 63 workflows
**Timeline**: Created 2026-11-03

**Depends on:**
- `_INFO_HOW_IPPS_WORKFLOWS_CURRENTLY_WORK.md [AGENSYNTAX-IN01]` for the current-state inventory (63 workflows, replication patterns, keyword polysemy)
- `_INFO_IPPS_UNIFIED_WORKFLOW_PROPOSALS.md [AGENSYNTAX-IN02]` for Concept A and the shared baseline (Sections 2.1-2.9: slots, resolution order, echo line, unknown-value protocol, procedure placement, side-effect classes, compiled orchestration)
- `_SPEC_AGEN_AGENTIC_ENGLISH.md [AGEN-SP01]` and `agentic-english.md` for the verb vocabulary
- `_SPEC_GRUC_STANDARD.md [GRUC-SP01]` for the GRUC consumer mapping
- `_SPEC_IPPS_WORKFLOWS.md [IPPSWFLW-SP01]` and `_SPEC_IPPS_SKILLS.md [IPPSSKLS-SP01]` for workflow and skill structure
- `_INFO_HOW_TO_IMPLEMENT_WORKFLOWS_AS_SKILLS.md [SKLWRKFL-IN01]` for workflow-to-skill migration
- `_SPEC_IPPS_RESEARCH_AND_WRITING_TOOLS.md [DRSYNART-SP01]` Section 8 for the grammar precursor and filename discovery

## Summary

- AGEN (Agentic English) becomes an invocation language with three word classes: verbs are workflows, keywords are relationships, constants name existing concepts (document types, techniques, personas, strategies, analysis stages, pipelines such as VCRIV). One sentence form `/<verb> <OBJECT> [<input>] [<keyword> <value>]...` covers every workflow [ASSUMED]
- Constants "snap": ordinary words in a prompt that match a registered constant ID or alias are replaced by the canonical term, the agent loads the term's skill files, and the echo line shows the canonical sentence. Users learn the IPPS vocabulary from echo lines and prompt files, which always use canonical forms [ASSUMED]
- Skill binding: a workflow signature declares the constant TYPE and the registry file that owns its values (e.g. `using` → `writing_techniques/README.md`), never the values. Knowledge resolves by filename `[CONSTANT]_[GRUCTYPE].md`, the mechanism DRSYNART already uses for techniques and personas [VERIFIED for DRSYNART precedent, ASSUMED for generalization]
- Keyword list closed at 8: `from`, `against`, `to`, `for`, `in`, `using`, `as`, `tier`. `tier` replaces the `depth` keyword proposed in AGENSYNTAX-IN02, because DRSYNART-SP01 binds "tier" as the only name for execution depth [VERIFIED]
- Platform conflicts (official command references read 2026-11-03): 4 of 63 existing IPPS workflow names equal a built-in name: `/verify` (Claude Code bundled skill), `/deep-research` (Claude Code bundled workflow), `/rename` (built-in in Claude Code, Devin, Codex), `/implement` (Devin system skill). 5 more are near conflicts: `/go`, `/research`, `/research-program`, `/remove`, `/switch-model` [VERIFIED]
- AGENSYNTAX-IN02 Concept A proposed 3 verbs that equal built-in names: `/new`, `/archive`, `/update`. This INFO replaces them with conflict-free verbs `/start`, `/close`, `/record` and drops `/release` and `/configure` (near conflicts) [VERIFIED for conflicts, ASSUMED for replacements]
- Per user decision (2026-11-03), existing IPPS workflow names stay unchanged and carry a conflict state; only new verbs must be conflict-free. All 10 new verbs of this concept have no conflict [VERIFIED against the reserved lists in Section 10]
- Conflicts cluster in chat-session control (`/new`, `/rename`, `/archive`, `/resume`, `/recap`, `/status`) and code review (`/review`, `/verify`, `/diff`). IPPS verbs name document-intelligence and workflow-automation operations; the host agents' verbs name coding and session-control operations. Rule: IPPS never takes a verb that acts on the host agent's chat session [VERIFIED for clustering, ASSUMED for rule]
- Preview: 63 workflows → 30 verbs (20 existing names kept, 10 new verbs; 43 workflows absorbed). Target-state conflicts: 3 exact (`/verify`, `/implement`, `/rename`), 4 near, 23 none [ASSUMED]
- Migration: verb = workflow file stem = skill folder = slash command. The `## Signature` section in the body is the portable declaration; `argument-hint` (Claude Code, Devin) is generated at deploy time because the Agent Skills standard rejects unknown frontmatter keys and Codex has no argument hint [VERIFIED]
- Outdated claim found: `_INFO_HOW_TO_USE_IPPS_WITH_CLAUDE_CODE.md` states all IPPS skill names except `verify` are unreserved (verified 2026-09-23). The official Claude Code command reference now lists `/rename` and `/deep-research` [VERIFIED]

## Table of Contents

1. [Goal: AGEN as an Invocation Language](#1-goal-agen-as-an-invocation-language)
2. [Constraints and User Decisions](#2-constraints-and-user-decisions)
3. [Word Classes](#3-word-classes)
4. [Grammar](#4-grammar)
5. [Term Snapping](#5-term-snapping)
6. [Skill Binding Without Replication](#6-skill-binding-without-replication)
7. [Signature Block](#7-signature-block)
8. [Workflow-to-Skill Migration](#8-workflow-to-skill-migration)
9. [Prompt Files](#9-prompt-files)
10. [Platform Command Conflicts](#10-platform-command-conflicts)
11. [Verb Catalog and Preview of All 63 Workflows](#11-verb-catalog-and-preview-of-all-63-workflows)
12. [Open Decisions](#12-open-decisions)
13. [Next Steps](#13-next-steps)
14. [Sources](#14-sources)
15. [Document History](#15-document-history)

## 1. Goal: AGEN as an Invocation Language

### 1.1 The Language in One Sentence

AGEN today is planning vocabulary: verbs, placeholders, labels, and states used in STRUT plans and planning documents (`agentic-english.md` Scope) [VERIFIED]. The goal is a universally applicable agentic language in which:

- **Verbs are workflows** - `/write`, `/critique`, `/research` each name exactly one workflow (or one user-only skill after migration)
- **Keywords describe relationships** - `from` (input), `against` (authority), `for` (purpose), `to` (target), `in` (location), `using` (method), `as` (voice), `tier` (execution depth)
- **Constants name existing concepts** - `SPEC`, `ARTICLE`, `MINTO`, `MCPI`, `VCRIV` are IDs that point to knowledge already defined in skills and registries

Examples of constants:
- `VCRIV` - pipeline constant: verify → critique → reconcile → implement → verify. One word stands for 5 workflow calls with fixed order and a decision gate after reconcile
- `MINTO` - technique constant: pyramid writing technique = `MINTO_GUIDES.md` (decisions), `MINTO_RULES.md` (verification), `MINTO_CHECKS.md` (post-execution checks), `TEMPLATES/MINTO_TEMPLATE.md` and `TEMPLATES/MINTO_OPTIONS_TEMPLATE.md` (structure), `EXAMPLES/MINTO_EXAMPLE_01-ExecutiveProposal.md` (exemplar). It combines with a document type constant: `ARTICLE` + `MINTO` = article rules plus pyramid structure [VERIFIED file set]
- `MCPI` - research strategy constant defined in `research-methods`
- `SPEC` - object constant: document type with its own GRUC set in `write-documents`

### 1.2 Problem Solved

- **Replication** - today every new document type adds 3 workflows plus sections in up to 4 review workflows (AGENSYNTAX-IN01). In the target state a new type adds GRUC files and 1 registry line, 0 workflows [ASSUMED]
- **No learnable pattern** - today 4 invocation formats (`## Command Grammar`, `## Trigger`, `## Usage`, `## Command Dispatch`) and 35 workflows without any (AGENSYNTAX-IN01). Target: one sentence form and one `## Signature` per workflow [ASSUMED]
- **Intent derivation** - when the words of a prompt snap to registered terms, the agent maps the prompt to the right workflow and skill files by lookup instead of interpretation [ASSUMED]
- **Prompt-file readability** - a workflow call in a prompt file reads as one English sentence split at the verb (Section 9) [ASSUMED]

### 1.3 How a Prompt Becomes a Call

```
User prompt (ordinary English)
│  "write a strut plan based on _SPEC_TOPIC.md for migrating auth to tokens"
│
├─> Snap: words matched against the AGEN lexicon (Section 5)
│   ├─> verb      "write"         → /write       workflow
│   ├─> object    "strut plan"    → STRUT        constant, owner write-documents
│   ├─> keyword   "based on"      → from         relationship INPUT
│   └─> keyword   "for"           → for          relationship GOAL
│
├─> Echo: canonical sentence shown as first response line
│   Resolved: /write STRUT | from _SPEC_TOPIC.md | for "migrating auth to tokens" | tier 1
│
└─> Execute: /write loads the skill files named by the constants
    └─> STRUT_GUIDES.md (if present), STRUT_TEMPLATE.md
```

### 1.4 Learning Over Time

- Day 1: user writes plain English; the agent snaps words and echoes the canonical sentence
- Week 1: user copies canonical sentences from echo lines and prompt files
- Later: user composes calls directly (`/propose ARTICLE from _INFO_TOPIC-IN01_Summary.md using ABTSTORY 3 options`) and knows that `using` always introduces a method, `as` always a voice, `against` always an authority

The language stays learnable because the 3 word classes never change meaning: a keyword means the same thing after every verb, and a constant means the same thing in every document [ASSUMED].

## 2. Constraints and User Decisions

**Fixed points from AGENSYNTAX-IN02 Section 1** (unchanged): F1 AGEN not in workflow step bodies, F2 orchestration only in prompt sequences and planning documents, F3 never ask questions, F4 GRUC consumer mapping, F5 user-only selection of technique and persona, F6 phase-model independence, F7 platforms (Cascade/Devin workflows, Claude Code skills; extended here by Codex).

**Additional fixed points:**
- **F8 - One name for execution depth**: "tier is the execution-depth dial for every layer ... Never introduce 'level', 'mode', 'quick', or 'full' as synonyms" (`DRSYNART-SP01` MUST-NOT-FORGET). Consequence: keyword `tier`, not `depth` [VERIFIED]
- **F9 - Prompt-file call format**: executed workflow on a standalone line without backticks, arguments on the following line (`PRMT-CT-08`); mentions in backticks (`PRMT-CT-10`) [VERIFIED]
- **F10 - Skill migration**: every verb workflow must deploy as one user-only skill on Claude Code, Devin, and Codex without content changes (user request 2026-11-03)

**User decisions (2026-11-03):**
- **U1** - Concept A (verb sentences) is the working direction
- **U2** - No new verb may conflict with a command, alias, bundled skill, or bundled workflow of Claude Code, Devin, or Codex
- **U3** - Existing IPPS workflow names stay unchanged for now; conflicts are marked, resolution follows later
- **U4** - IPPS focuses on document intelligence and workflow automation, not on coding. The verb set is designed for documents, knowledge, and work sessions; coding verbs (`/commit`, `/deploy`, `/test`, `/project-release`) stay as they are

## 3. Word Classes

```
Invocation sentence
├── VERB       /write             one workflow; side-effect class; GRUC role
├── OBJECT     STRUT              constant of type OBJECT; selects the GRUC set
├── INPUT      _SPEC_TOPIC.md     value (positional shorthand for "from")
├── CLAUSES    for "<goal>"       keyword + value; keyword = relationship
│              using MINTO        keyword + constant
└── FLAGS      3 options          closed phrase list declared by the verb
```

### 3.1 Verbs

- One verb = one workflow file = one user-only skill after migration (Section 8)
- Lowercase English imperative, one word, no object suffix (`/write`, not `/write-spec`)
- Each verb has exactly one side-effect class (AGENSYNTAX-IN02 Section 2.8): Create, Report-only, Edit, Destructive or outward-facing
- Each verb has one GRUC role: which GRUC file type it reads (Section 6.4)
- Each verb maps to one AGEN verb (`/write` ↔ `[WRITE]`, `/critique` ↔ `[CRITIQUE]`). New verbs without an AGEN entry extend AGEN (Section 11.10)
- New verb names must have conflict state `CONFLICT-NONE` (Section 10.3, rule CR-1)

### 3.2 Keywords

8 relationship words, closed list, one meaning each (Section 4.2). A keyword never changes meaning between verbs.

### 3.3 Constants

A constant is an ID that names a concept already defined somewhere in the PromptSystem. Each constant type has exactly one owning registry, and the registry lives in a skill or rule file, never in a workflow.

- **OBJECT** - position: directly after the verb - owner: one object registry (to be built, AGENSYNTAX-IN02 Next Step 2) that points each object to its owning skill: document types → `@skills:write-documents` SKILL.md routing table, `DIAGRAM` → `@skills:write-documents` `ASCII_ART_*`, `SESSION` → `@skills:session-management`, `DRIFT` → `@skills:drift-control` - examples: `INFO`, `SPEC`, `IMPL`, `TEST`, `TASKS`, `STRUT`, `PROMPTS`, `TEMPLATE`, `ARTICLE`, `REPORT`, `EBOOK`, `CONVERSATION`, `DIAGRAM`, `SESSION`, `BUG`, `DRIFT`, `FAILURE`, `LEARNING` [ASSUMED]
- **TECHNIQUE** - keyword `using` - owner: `@skills:write-documents` `writing_techniques/README.md` - 9 IDs: `ABTSTORY`, `AIDA`, `DIATAXIS`, `IMINTO`, `IMRAD`, `KABOB`, `MINTO`, `PAS`, `STA` - user-only (F5) [VERIFIED]
- **PERSONA** - keyword `as` - owner: `@skills:write-documents` `writing_personas/README.md` - 20 personas - user-only (F5) [VERIFIED]
- **STRATEGY** - keyword `using` - owner: `@skills:research-methods` SKILL.md - `MEPI`, `MCPI`
- **PROFILE** and **AREA** - keyword `using` - owner: `@skills:research-methods` `research_profiles/`, `research_areas/` - profiles `PERSONAL`, `ORGA`, `COMPANY`, `NETWORK`; areas `default`, `legal`, `market-intel`, `software`
- **STAGE** - keyword `using` - owner: `@skills:analysis-methods` SKILL.md - `PATTERN-DETECTION`, `HYPOTHESIS`, `VALIDATION`, `INVESTIGATION` (the file stems of the stage GRUC sets)
- **PIPELINE** - keyword `using`, valid only with `/go` and `/write PROMPTS` - owner: `promptsystem-core.md` Quality Pipelines and `ID-REGISTRY.md` - `VCRIV`, `FACRIV`
- **AUTHORITY** - keyword `against` - owner: verb signature (closed values) - `rules` (default of `/verify`), `facts` (external evidence), or a file
- **SCOPE** - keyword `in` - owner: workspace and session `NOTES.md` folder constants - `session`, `workspace`, `[SESSIONS_FOLDER]`, `[SESSION_FOLDER]`, or a folder path
- **FORMAT** and **LANGUAGE** - keyword `to` - owner: `/convert` and `/translate` signatures - `markdown`, `html`, `pdf`, `bundle`; language codes `DE`, `PT`, ...

**Registry disjointness**: one keyword may accept several constant types (`using` accepts TECHNIQUE, STRATEGY, PROFILE, AREA, STAGE, PIPELINE). The ID sets behind one keyword must be disjoint; an ID found in two registries is an unknown value (AGENSYNTAX-IN02 Section 4.2). Today the sets are disjoint [VERIFIED by comparing the lists above].

**Not invocation constants**: AGEN states (`COMPLEXITY-HIGH`, `SESSION-MODE`) and labels (`[VERIFIED]`, `[CRITICAL]`) stay document vocabulary. They are checked or applied inside work, never passed as arguments.

### 3.4 Values

- Paths, globs (`T01_*`), Doc IDs (`TOPIC-SP01`), quoted free text (`"migrate auth to tokens"`)
- Context values: `chat` (current conversation), `last run` (output of the previous call in this conversation)
- Selectors inside an input: `option 2 in ARTICLE-OPTIONS-01_Title.md`

## 4. Grammar

### 4.1 Sentence Form

```
/<verb> [<OBJECT>] [<input>] [<keyword> <value>]... [<flag>]...

<keyword> := from | against | to | for | in | using | as | tier
<flag>    := inline | plan | plan only | <N> options
           | compare <ID>, <ID>[, <ID>[, <ID>]] | approaches <A>, <B>[, ...]
```

- **G1 Order** - verb, then object, then positional input, then clauses and flags in any order. Canonical order (echo lines, prompt files, STRUT): `from`, `against`, `for`, `to`, `in`, `using`, `as`, `tier`, flags
- **G2 Positional input** - the first value after the object that is not introduced by a keyword is the `from` value
- **G3 Quoting** - free text containing spaces or a keyword word is written in double quotes
- **G4 One clause per keyword** - several constants of different types share one `using` clause, comma-separated: `using MCPI, COMPANY`. Two constants of the same type in one clause are invalid, except in the `compare` flag
- **G5 Fillers** - `with` before a flag (`with 3 options`), articles, and politeness words are removed during normalization. Canonical form omits them
- **G6 Casing** - constants are uppercase IDs in canonical form; registered lowercase aliases are accepted in chat (`article` → `ARTICLE`)
- **G7 Flags are verb-owned** - each verb signature lists the flags it accepts; a flag not in the signature is an unknown value

### 4.2 Keywords

- **`from`** - INPUT source - file, folder, glob, Doc ID, quoted text, `chat`, `last run` - `/write SPEC from _INFO_TOPIC.md`
- **`against`** - INPUT authority to compare with - `rules`, `facts`, file - `/critique _INFO_TOPIC.md against facts`
- **`for`** - GOAL purpose, goal sentence, audience, or recipient - free text - `/draft CONVERSATION for Jane Smith`
- **`to`** - GOAL target - output path, FORMAT, LANGUAGE, new name - `/convert report.pdf to markdown`
- **`in`** - SCOPE location where to read or write - SCOPE constant or folder - `/remove reviews in T01_TOPIC_Folder`
- **`using`** - OPTIONS method - TECHNIQUE, STRATEGY, PROFILE, AREA, STAGE, PIPELINE - `/propose ARTICLE using ABTSTORY`
- **`as`** - OPTIONS voice - PERSONA only - `/write ARTICLE as <PERSONA>`
- **`tier`** - OPTIONS execution depth - `1`, `2`, `3` (DRSYNART-SP01 Section 8.1) - `/research "<question>" tier 2`

### 4.3 Flags

- **`inline`** - edit the input file in place, never create a file (DRSYNART-DD-17)
- **`plan`** / **`plan only`** - tier 2-3 planning behavior as defined in DRSYNART-SP01 Section 8.1
- **`<N> options`** - number of candidates for `/propose` (2-5)
- **`compare <ID>, <ID>`** - one candidate per technique for `/propose` (2-4 IDs)
- **`approaches <A>, <B>`** - named research approaches for `/research tier 3`

### 4.4 Keyword Synonyms

Synonyms normalize prose to canonical keywords. They are input normalizers only: echo lines, prompt files, and STRUT plans always contain the canonical keyword (precedent: PowerShell approved verbs, which forbid synonyms of approved verbs for discoverability, AGENSYNTAX-IN02 Section 4.7).

- `based on`, `out of` → `from`
- `compared with`, `checked against` → `against`
- `aimed at`, `addressed to`, `on behalf of` → `for`
- `into`, `as file` → `to`
- `inside`, `within` → `in`
- `with technique`, `in the style of` → `using` (only when a registered constant follows)
- `in the voice of`, `written as` → `as` (only when a registered persona follows)
- `only plan`, `just plan` → `plan only`

Not registered: `depth`, `level`, `mode` as synonyms of `tier` (F8 forbids them as synonyms in files). The echo line always states `tier N`, so a user who writes "level 2" sees the canonical word.

Polysemy removed (AGENSYNTAX-IN01 Section 5.3): `as article` (output form in `/cleanup`) becomes `for publishing`; `for a prompts file` (object type) becomes the object token `PROMPTS`; `as` carries PERSONA only.

## 5. Term Snapping

"Snapping" means: a word or phrase in a prompt that matches a registered term is replaced by the canonical term, and the agent attaches the term's definition (its skill files) to the request. Registered terms pull nearby words into a known shape, the way a magnet pulls iron filings into field lines.

### 5.1 Lexicon

The lexicon is the union of:
- **Verbs** - the verb list in `agentic-english.md` (extended by Section 11.10)
- **Keywords and keyword synonyms** - one new section in `agentic-english.md` (Section 4.2, 4.4)
- **Constant types** - one new section in `agentic-english.md` that lists each type with a pointer to its owning registry (Section 3.3). No constant values are copied into the rule file
- **Constant values and aliases** - the owning registries (`writing_techniques/README.md`, `writing_personas/README.md`, `research-methods` SKILL.md, `analysis-methods` SKILL.md, object registry). Each entry may list aliases next to its ID, e.g. `MINTO` - aliases "Minto Pyramid", "pyramid principle"

Effect: adding a technique adds its ID and aliases to the lexicon without editing any rule or workflow (DRSYNART-IG-10 extension rule) [ASSUMED].

### 5.2 Snap Order

First match wins, from strongest to weakest:

1. **S1 Slash verb** - `/write` at line start (chat) or a standalone call line (prompt file)
2. **S2 Keyword** - canonical keyword or registered keyword synonym (Section 4.4)
3. **S3 Constant ID** - exact ID, case-insensitive (`minto` → `MINTO`)
4. **S4 Constant alias** - alias registered in the owning registry ("pyramid principle" → `MINTO`)
5. **S5 Free text** - no snap; the value is passed as written

### 5.3 Snap Guards

- **SG-1 User-only constants** - TECHNIQUE and PERSONA snap only from an ID (S3) or registered alias (S4), never from a description. "Make it persuasive" stays free text and loads no technique (F5, DRSYNART-DD-08)
- **SG-2 No snap inside values** - quoted text, paths, and code are never scanned
- **SG-3 Ambiguity** - a phrase that matches terms of two registries is an unknown value: list the candidates, stop (AGENSYNTAX-IN02 Section 2.4)
- **SG-4 Prose verbs inform, slash verbs execute** - "please verify this" maps the intent to `[VERIFY]` for interpretation and suggestions; only the slash form (chat) or a standalone call line (prompt file) executes a workflow
- **SG-5 Alias cap** - aliases are registered only for wording observed in real prompts, at most 3 per constant. This keeps aliases from growing into a second vocabulary (AGENSYNTAX-IN02 Section 4.7) [ASSUMED]

### 5.4 Echo Line

The first response line states the resolved call, marks the source of every value (explicit, session, context, default; AGENSYNTAX-IN02 Section 2.2), lists every snap, and names the loaded knowledge:

```
Resolved: /write ARTICLE | from option 2 in ARTICLE-OPTIONS-01_Title.md (explicit) | for "finance leads" (explicit)
| using MINTO (snapped: "pyramid principle") | as <PERSONA> (explicit) | tier 1 (default)
| knowledge: ARTICLE_GUIDES.md, ARTICLE_TEMPLATE.md, MINTO_GUIDES.md, <PERSONA>.md
```

- The user corrects any value with one follow-up line; F3 (never ask) stays safe for reversible verbs
- Destructive and outward-facing verbs keep preview-then-confirm and never take their target from context or default (AGENSYNTAX-IN02 Section 2.3)
- `knowledge: generic` states that a GRUC file for this verb-object pair is missing and the verb runs its generic procedure (AGENSYNTAX-IN02 Section 2.5)

### 5.5 Learning Loop

```
prose prompt ──> snap ──> echo (canonical) ──> user reads canonical form
     ^                                                  │
     └──────── next prompt uses canonical words <───────┘
```

- Prompt files, STRUT plans, and echo lines contain only canonical terms, never synonyms or aliases. Every file a user reads teaches the canonical vocabulary
- The STRUT notation reuses the same sentence: `[WRITE](STRUT from _SPEC_TOPIC.md for "migrate auth to tokens")` is the planning form of `/write STRUT from _SPEC_TOPIC.md for "migrate auth to tokens"`. One sentence, three places: chat, prompt file, STRUT plan [ASSUMED]

## 6. Skill Binding Without Replication

### 6.1 Principle

- Workflows name constant TYPES and the registry that owns them
- Skills own constant VALUES, their definitions, procedures, rules, templates, and examples
- A workflow body or signature never enumerates skill-owned values (no list of technique IDs, persona names, document types, strategies, or stages in a workflow). Exception: the frontmatter `description` may name 2-4 example objects for slash-menu discoverability, ending with "..." (Section 8.4)
- Verb-owned closed values may be enumerated in the signature: `tier 1|2|3`, AUTHORITY `rules|facts`, FORMAT `markdown|html|pdf|bundle`

Consequence: adding a technique, persona, document type, research profile, or analysis stage changes zero workflows. This generalizes `DRSYNART-FR-05` ("No workflow edit when a technique, persona, document type, or analysis stage is added: filename-pattern discovery only") to all constant types [VERIFIED for DRSYNART, ASSUMED for generalization].

### 6.2 Resolution Chain

```
/write ARTICLE from option 2 in ARTICLE-OPTIONS-01_Title.md using MINTO as <PERSONA>
│
├─> /write ─────────────── workflows/write.md: signature, verb-generic steps, quality gate
├─> ARTICLE ────────────── object registry → @skills:write-documents SKILL.md routing table
│                          └─> document_types/ARTICLE_GUIDES.md, ARTICLE_TEMPLATE.md (section Output)
├─> using MINTO ────────── TECHNIQUE registry → writing_techniques/README.md
│                          └─> writing_techniques/MINTO_GUIDES.md, TEMPLATES/MINTO_TEMPLATE.md
├─> as <PERSONA> ───────── PERSONA registry → writing_personas/README.md
│                          └─> writing_personas/<PERSONA>.md
└─> never loaded ───────── *_CHECKS.md (GRUC-IG-03); *_RULES.md only by /verify
```

Each step is a filename lookup, not a branch in the workflow:
- OBJECT → `[skill]/[OBJECT]_[GRUCTYPE].md` or the path the router table names
- TECHNIQUE → `writing_techniques/[ID]_GUIDES.md` exists ? load : list README IDs, stop (DRSYNART-SP01 Section 8.4)
- PERSONA → `writing_personas/[PERSONA].md` exists ? load : list README names, stop
- STAGE → `analysis-methods/[STAGE]_GUIDES.md`
- STRATEGY, PROFILE, AREA → path named in `research-methods` SKILL.md Intent Lookup

### 6.3 Signature Slots Point to Registries

A slot line in the signature names the type, the registry pointer, and the selection rule. The workflow never knows that `MINTO` exists:

```
- using: TECHNIQUE - registry: @skills:write-documents writing_techniques/README.md - user-only, no default - unknown: list registry, stop
- as: PERSONA - registry: @skills:write-documents writing_personas/README.md - user-only, no default - unknown: list registry, stop
```

### 6.4 GRUC Role per Verb

Each verb reads exactly the GRUC types of its role (GRUC-SP01 consumer mapping, AGENSYNTAX-IN02 Concept D lens idea):

- **Producing verbs** (`/write`, `/propose`, `/draft`, `/start`, `/record`, `/research`, `/analyze`, `/convert`, `/translate`) - GUIDES + TEMPLATE of the object and of every named constant; EXAMPLE files through GUIDES links
- **`/verify`** - RULES + TEMPLATE of the object and of every constant named in the target's header (`**Document Type**`, `**Technique**`, `**Persona**`; DRSYNART-SP01 Section 8.4)
- **`/critique`** - GUIDES (logic, goal alignment); `against facts` adds external evidence
- **`/audit`** - CHECKS section PD (process discipline)
- **`/improve`** - CHECKS section QI (quality improvement)
- **`/reconcile`** - review files (`*_CRITIQUE.md`, `*_FACT-CHECK.md`) plus GUIDES for feasibility
- **Changing verbs** (`/fix`, `/implement`, `/rename`) - the plan or findings given as input plus GUIDES of the changed object
- **No working verb reads CHECKS** (GRUC-IG-03)

### 6.5 Procedure Placement

Absorbed workflows carry object-specific procedures. They move into the object's GUIDES file as decisions in working order (GRUC-SP01 GUIDES content; AGENSYNTAX-IN02 Section 2.7). The verb workflow keeps verb-generic steps only.

- `/write-spec` alternatives and design decisions → `SPEC_GUIDES.md` (to create)
- `/write-article` Brief → `ARTICLE_GUIDES.md` (exists; DRSYNART)
- `/bugfix` bug folder, reproduction, regression test → `BUG_GUIDES.md` (to create; owner to decide). The commit step leaves the verb and becomes a separate call in the compiled sequence (F2, side-effect class)
- `/fact-check` claim extraction and source rating → `FACT-CHECK_GUIDES.md` (to create; owner `research-methods` [ASSUMED])
- `/learn` retrospective steps → `LEARNING_GUIDES.md` (to create)
- `/conversation-draft` "write as the user" rules → `CONVERSATION_GUIDES.md` (to create)
- `/transcribe`, `/render`, `/bundle` → existing skills `llm-transcription`, `pdf-tools`, `renderings`, `research-methods` (bundle decisions)

Prerequisite: 11 objects lack GUIDES files (AGENSYNTAX-IN01 Section 7.3). Until a GUIDES file exists, the verb runs its generic procedure and echoes `knowledge: generic`.

### 6.6 Example Verb Workflow Skeleton

```markdown
---
description: Create a registered document (INFO, SPEC, STRUT, ARTICLE, ...) from input material
---

# Write Workflow

**Goal**: One new document of the requested OBJECT, built from its TEMPLATE and GUIDES

## Signature

/write <OBJECT> [from <input>] [for <goal>] [to <target>] [in <scope>] [using <TECHNIQUE>] [as <PERSONA>] [tier 1|2|3] [plan only] [inline]

- OBJECT: object registry - required - unknown: list registry, stop
- ... (one line per slot, Section 7)

## Required Skills

- @skills:write-documents SKILL.md (routing table: OBJECT → GUIDES, TEMPLATE)
- Technique and persona files only when `using` or `as` is given

## MUST-NOT-FORGET

- Never load CHECKS files; never modify NOTES, PROBLEMS, PROGRESS, FAILS
- `using` and `as` are user-only; never guess or complete them

## Steps

1. Resolve slots (resolution order), print the echo line
2. Load OBJECT GUIDES and TEMPLATE; load technique and persona files if named
3. Follow the GUIDES decisions in order; tier 2-3: write STRUT and prompt file, then stop or execute per tier rules
4. Write the output to the target path from the TEMPLATE naming rule

## Quality Gate

- [ ] Echo line printed with sources of all values
- [ ] Output follows OBJECT TEMPLATE; zero CHECKS files loaded
```

The description names example objects for the slash menu but does not enumerate the registry; angle brackets are avoided in descriptions (Section 8.4). Steps use plain English, no AGEN brackets (F1).

## 7. Signature Block

The signature is the annotated function declaration of a workflow. It replaces the 4 current formats `## Command Grammar`, `## Trigger`, `## Usage`, `## Command Dispatch` (AGENSYNTAX-IN01).

### 7.1 Format

```markdown
## Signature

/write <OBJECT> [from <input>] [for <goal>] [to <target>] [in <scope>] [using <TECHNIQUE>] [as <PERSONA>] [tier 1|2|3] [plan only] [inline]

- OBJECT: object registry - required - unknown: list registry, stop
- from: file | folder | glob | Doc ID | text | chat | last run - default: newest predecessor object in working folder (object registry)
- for: goal sentence or audience - default: session goal (NOTES.md)
- to: output path - default: naming rule in [OBJECT]_TEMPLATE.md
- in: working folder - default: current working folder
- using: TECHNIQUE - registry: @skills:write-documents writing_techniques/README.md - user-only, no default - unknown: list registry, stop
- as: PERSONA - registry: @skills:write-documents writing_personas/README.md - user-only, no default - unknown: list registry, stop
- tier: 1 | 2 | 3 - default: object default (object registry); tier 2-3 writes STRUT and prompt file (F2)
- plan only: write STRUT and prompt file, do not execute
- inline: edit the input file in place, never create a file (DRSYNART-DD-17)
```

### 7.2 Signature Rules

- **SIG-1** - First line after the heading is the grammar line: verb, required slots in `<...>`, optional slots in `[...]`. It is machine-extractable (deploy scripts read it, Section 8.2)
- **SIG-2** - One line per slot: name, type or registry pointer, required or default, unknown-value behavior
- **SIG-3** - Skill-owned values appear as registry pointers, never as enumerations (Section 6.1). Verb-owned closed values may be enumerated
- **SIG-4** - Defaults name a resolution rule, not a literal value ("newest predecessor object", "session goal")
- **SIG-5** - User-only slots state "user-only, no default"
- **SIG-6** - Destructive verbs state "preview-then-confirm" in the grammar-line slot that selects the target
- **SIG-7** - The signature lives in the body, not in frontmatter, so it survives every platform transformation (Section 8.2)

## 8. Workflow-to-Skill Migration

### 8.1 Names

- Verb = workflow file stem = skill folder name = skill `name` = slash command. One lowercase word
- Claude Code derives the command name from the skill folder or `name`; Devin uses the directory name as skill identifier; Codex uses `name` [VERIFIED]
- A verb name must pass the conflict audit before it becomes a workflow (Section 10.3)

### 8.2 Frontmatter per Platform

Source workflows in `[PROMPTSYSTEM_FOLDER]/workflows/` carry only `description` (and existing IPPS fields such as `default_tier`). Platform keys are generated at deploy time from the signature grammar line:

- **Cascade / Devin workflows** (`[AGENT_FOLDER]/workflows/<verb>.md`) - `description`; signature in body; invoked `/<verb>`
- **Claude Code skill** (`.claude/skills/<verb>/SKILL.md`) - `name`, `description`, `disable-model-invocation: true`, `argument-hint` from the grammar line; invoked `/<verb>` [VERIFIED]
- **Devin CLI / Local skill** (`.devin/skills/<verb>/SKILL.md`) - `name`, `description`, `argument-hint`, `triggers: ["user"]`; invoked `/<verb>` [VERIFIED]
- **Codex skill** (`.agents/skills/<verb>/SKILL.md`) - `name`, `description` (both required); `agents/openai.yaml` with `policy.allow_implicit_invocation: false`; invoked `$<verb>` or `/skills` picker; no argument-hint field, so the body signature is the only declaration [VERIFIED 2026-07 per `_INFO_HOW_CODEX_WORKS.md`]
- **Agent Skills standard / Skills API packaging** - allowed keys are `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`; `argument-hint` produces "Unexpected key(s) in SKILL.md frontmatter" [VERIFIED]. This is why SIG-7 keeps the signature in the body and `argument-hint` is a deploy-time addition

### 8.3 Arguments

- Claude Code: `$ARGUMENTS`, `$ARGUMENTS[N]`, `$N`, named `$name`; without a placeholder the arguments are appended as `ARGUMENTS: <value>` [VERIFIED]
- Devin: `$ARGUMENTS`, `$1`-`$9`; without a placeholder the arguments are appended to the skill content [VERIFIED]
- Codex: the rest of the prompt after `$<verb>` is ordinary context [ASSUMED]
- Consequence: verb bodies use no positional placeholders. The whole sentence after the verb is parsed against the signature, so behavior is identical on all platforms [ASSUMED]

### 8.4 Description and Argument Hint

- `description` - one sentence: verb action + 2-4 example objects + "...". No angle brackets: Claude Code shows `<` and `>` in descriptions as `&lt;` and `&gt;` [VERIFIED]
- `argument-hint` - grammar line without the verb, square brackets only (Claude Code examples use `[issue-number]`, `[filename] [format]`): `[OBJECT] [from input] [for goal] [to target] [using TECHNIQUE] [as PERSONA] [tier 1-3]` [ASSUMED rendering]

### 8.5 Context Cost

- Claude Code: user-only skills (`disable-model-invocation: true`) cost zero context and are exempt from the model-selection ceiling of 32-36 skills (`SKLWRKFL-IN01`, `_INFO_HOW_CLAUDE_CODE_WORKS.md` Section 8) [VERIFIED]
- Codex: name, description, and path of every skill are injected at startup within a budget of 2% of the context window or 8,000 characters [VERIFIED 2026-07]. 30 verb skills instead of 63 workflow skills halve this cost [ASSUMED]

### 8.6 Existing Migration Paths

- Claude Code: `_PROMPTS_UpdateClaude.md` deploys workflows as user-only skills and renames `verify` to `ipps-verify` (bundled-skill collision) [VERIFIED]
- Devin: `devin migrate workflows` converts legacy workflows to native skills; `.devin/workflows/` is excluded from the `.claude/commands/` import [VERIFIED per `_INFO_HOW_DEVIN_WORKS.md`]
- Codex: no IPPS deployment exists yet

## 9. Prompt Files

Prompt files call workflows on standalone lines without backticks, with arguments on the following line (PRMT-CT-08). With verb sentences, the call line plus argument line reads as one English sentence split after the verb.

### 9.1 Single Call

```
/write
STRUT from _SPEC_TOPIC.md for "migrate auth to tokens"
```

### 9.2 Pipeline Expanded

A pipeline constant names a sequence; in a prompt file it is expanded into standalone calls, because each executed workflow needs its own line (PRMT-CT-08). The constant stays visible in the objective line as a reference:

```
Objective: VCRIV pass on _SPEC_TOPIC.md

/verify
_SPEC_TOPIC.md against rules

/critique
_SPEC_TOPIC.md

/reconcile
_SPEC_TOPIC_CRITIQUE.md

Gate: stop for the user selection of accepted findings.

/implement
accepted findings from _SPEC_TOPIC_CRITIQUE.md

/verify
_SPEC_TOPIC.md against rules
```

### 9.3 Writing Sequence

```
/propose
ARTICLE from _INFO_TOPIC-IN01_Summary.md for "finance leads" using ABTSTORY 3 options

Gate: stop for the user choice of one option.

/draft
ARTICLE from option 2 in ABTSTORY-OPTIONS-01_Title.md

/write
ARTICLE from ABTSTORY-DRAFT-01_Title.md as <PERSONA>
```

### 9.4 Rules

- Canonical forms only (Section 5.5); no synonyms, no aliases, no fillers
- Mentions without execution stay in backticks (PRMT-CT-10): "the `/critique` output feeds `/reconcile`"
- Codex: skills are invoked with `$<verb>`, not `/<verb>`. A prompt file executed on Codex needs the runner or the model to map `/<verb>` to `$<verb>` [ASSUMED; needs a test]

## 10. Platform Command Conflicts

### 10.1 Method

- Reserved names collected from the official command references of Claude Code, Devin CLI, and Codex (CLI and IDE extension), read 2026-11-03, plus the Devin skills product guide (system skills) and the IPPS platform INFOs in `docs/` (Sources)
- Checked: all 63 existing IPPS workflow names, all 30 target verbs of this concept, the verbs proposed in AGENSYNTAX-IN02 (Concepts A, D, E), and the AGEN verb list
- Not checked: Cascade built-in commands (no command reference in the read sources; Cascade lists workflows in its slash menu, `_INFO_HOW_WINDSURF_WORKS.md`)

### 10.2 Conflict States

- **CONFLICT-HARD** - the name equals a built-in command, a command alias, a bundled skill, a bundled workflow, or a system skill on at least one target platform
- **CONFLICT-NEAR** - no equal name, but 1) typing the full IPPS name also matches a built-in in the slash menu (the IPPS name is the start of a built-in name or of a hyphen-separated word in it; Claude Code matches "from the start of the name or from a word within it, ignoring the :, _, and - separators" [VERIFIED]), or 2) a built-in performs the same kind of operation under a related name
- **CONFLICT-NONE** - neither

### 10.3 Conflict Rules

- **CR-1** - A new verb must be `CONFLICT-NONE` on all target platforms (U2)
- **CR-2** - Existing IPPS workflow names keep their names for now and carry their conflict state in every list of this concept (U3). Resolution is a later decision (Section 13)
- **CR-3** - IPPS verbs name document-intelligence and workflow-automation operations. IPPS never takes a verb that acts on the host agent's chat session, model, mode, or code review (`new`, `clear`, `resume`, `continue`, `rename`, `archive`, `fork`, `recap`, `status`, `plan`, `review`, `compact`, `export`) (U4)
- **CR-4** - AGEN verbs whose names are reserved slash commands stay planning-only bracket verbs and never become workflows (Section 10.7)
- **CR-5** - The audit is repeated when a platform command reference changes and before each IPPS release; the reserved lists below are dated

### 10.4 Reserved Names per Platform (read 2026-11-03)

**Claude Code - built-in commands and listed aliases** [VERIFIED, `AGENSYNTAX-IN03-SC-CLAUD-CMDS`]:
`add-dir`, `advisor`, `agents`, `allowed-tools`, `android`, `app`, `artifacts`, `auto-mode-setup`, `autocompact`, `autofix-pr`, `background`, `bashes`, `bg`, `branch`, `btw`, `bug`, `cd`, `checkpoint`, `checkup`, `chrome`, `clear`, `color`, `compact`, `config`, `context`, `continue`, `copy`, `cost`, `design-login`, `desktop`, `diff`, `effort`, `exit`, `export`, `extra-usage`, `fast`, `feedback`, `focus`, `fork`, `goal`, `heapdump`, `help`, `hooks`, `ide`, `import`, `init`, `insights`, `install-github-app`, `install-slack-app`, `ios`, `keybindings`, `list-agents`, `login`, `logout`, `mcp`, `memory`, `mobile`, `model`, `new`, `output-style`, `passes`, `peers`, `permissions`, `plan`, `plugin`, `plugin-authoring`, `powerup`, `pr-comments`, `privacy-settings`, `proactive`, `quit`, `radio`, `rate-limit-options`, `rc`, `recap`, `release-notes`, `reload-plugins`, `reload-skills`, `remote-control`, `remote-env`, `rename`, `reset`, `restart`, `resume`, `review`, `rewind`, `routines`, `sandbox`, `schedule`, `scroll-speed`, `security-review`, `settings`, `setup-bedrock`, `setup-vertex`, `share`, `skill-doctor`, `skills`, `stats`, `status`, `statusline`, `stickers`, `stop`, `subtask`, `tasks`, `team-onboarding`, `teleport`, `terminal-setup`, `theme`, `tp`, `tui`, `ultraplan`, `ultrareview`, `undo`, `update`, `upgrade`, `usage`, `usage-credits`, `vim`, `voice`, `web-setup`, `workflows`

**Claude Code - bundled skills and workflows** [VERIFIED]:
`artifact-capabilities`, `artifact-diagramming`, `batch`, `claude-api`, `claude-in-chrome`, `code-review` (alias `review`), `dataviz`, `debug`, `deep-research` (bundled workflow), `design`, `design-sync`, `doctor`, `fewer-permission-prompts`, `loop`, `run`, `run-skill-generator`, `simplify`, `slides`, `update-config`, `verify`, `workflow-authoring`

**Devin CLI and Devin Local (ACP slash commands)** [VERIFIED, `AGENSYNTAX-IN03-SC-DEVIN-CMDS`]:
`accept-edits`, `add-dir`, `archive`, `ask`, `autonomous`, `bug`, `btw`, `bypass`, `clear`, `cloud`, `code`, `compact`, `confetti`, `config`, `context`, `continue`, `copy`, `dangerous`, `exit`, `export`, `fast`, `feedback`, `fork`, `fusion`, `handoff`, `help`, `hooks`, `list-sessions`, `login`, `login-status`, `logout`, `loop`, `ls`, `mcp`, `mode`, `model`, `mouse`, `new`, `normal`, `open`, `org`, `pickup`, `plan`, `platform`, `quit`, `recap`, `remove-dir`, `rename`, `rename-session`, `repo`, `resume`, `revert`, `rm-session`, `session-stats`, `share`, `shortcuts`, `smart`, `ssh`, `stats`, `status`, `steps`, `theme`, `title`, `undo-add-dir`, `update`, `upgrade`, `usage`, `workspace`, `workspaces`, `yolo`. `loop` and `share` from `_INFO_DEVIN_RECENT_CHANGES.md` and `_INFO_HOW_DEVIN_WORKS.md`

**Devin system skills** (System Skills plugin, "installed for everyone"; the source lists them as examples, so the list may be incomplete) [VERIFIED, `AGENSYNTAX-IN03-SC-DEVIN-SKLPG`]:
`implement`, `plan`, `review`, `triage`

**Codex CLI** [VERIFIED, `AGENSYNTAX-IN03-SC-OPNAI-CXCMD`]:
`agents`, `app`, `apps`, `approve`, `archive`, `btw`, `cd`, `clear`, `compact`, `config`, `copy`, `cwd`, `daemon`, `daybreak`, `debug-config`, `delete`, `diff`, `exit`, `experimental`, `export`, `fast`, `feedback`, `fork`, `goal`, `hooks`, `ide`, `import`, `init`, `keymap`, `logout`, `mcp`, `memories`, `mention`, `model`, `new`, `permissions`, `pet`, `pets`, `plan`, `plugins`, `presets`, `ps`, `pwd`, `quit`, `raw`, `recap`, `rename`, `resume`, `review`, `setup-default-sandbox`, `side`, `skills`, `status`, `statusline`, `stop`, `subagents`, `theme`, `title`, `tui`, `usage`, `vim`, `voice`, `warnings`, `worktree`

**Codex IDE extension** [VERIFIED]:
`approve`, `cloud`, `cloud-environment`, `compact`, `fast`, `feedback`, `fork`, `goal`, `ide-context`, `init`, `local`, `mcp`, `memories`, `model`, `plan`, `project`, `reasoning`, `review`, `side`, `status`, `worktree`

### 10.5 Existing IPPS Workflow Names (63 checked)

**CONFLICT-HARD (4)** - names stay unchanged for now (CR-2):
- `/verify` - Claude Code bundled skill `verify`; it records recipes to `.claude/skills/verify/SKILL.md` and overwrites any project skill there. Current mitigation: deployed as `/ipps-verify` in Claude Code [VERIFIED]
- `/deep-research` - Claude Code bundled workflow `deep-research` (fans research out across subagents, runs in the background) [VERIFIED]
- `/rename` - built-in on all three platforms: Claude Code, Devin (`/rename [new title]`, aliases `title`, `rename-session`), Codex. All three rename the chat session; IPPS `/rename` refactors terms across files [VERIFIED]
- `/implement` - Devin system skill `implement` [VERIFIED]

**CONFLICT-NEAR (5)**:
- `/go` - start of Claude Code and Codex `/goal`; overlapping meaning (`/goal` sets a task goal or completion condition, IPPS `/go` loops until the goal is reached)
- `/research` - hyphen-separated word of Claude Code `/deep-research`; overlapping meaning
- `/research-program` - overlapping meaning with Claude Code `/deep-research` (multi-agent research run)
- `/remove` - start of Devin `/remove-dir`
- `/switch-model` - same operation as `/model` on all three platforms; already excluded from the Claude Code deployment

**CONFLICT-NONE (54)**: `/analyze`, `/ascii-diagram`, `/bugfix`, `/bundle`, `/cleanup`, `/commit`, `/compare-workspace-setup`, `/conversation-draft`, `/conversation-start`, `/conversation-update`, `/critique`, `/deploy`, `/draft-article`, `/draft-ebook`, `/draft-report`, `/drift-correct`, `/drift-detect`, `/fact-check`, `/fail`, `/fix`, `/hypothesize`, `/improve`, `/investigate`, `/learn`, `/pattern-detect`, `/prime`, `/project-release`, `/propose-article`, `/propose-ebook`, `/propose-report`, `/reconcile`, `/render`, `/session-archive`, `/session-finalize`, `/session-load`, `/session-new`, `/session-save`, `/sync`, `/test`, `/transcribe`, `/translate`, `/validate`, `/workspace-setup`, `/write-article`, `/write-ebook`, `/write-impl-plan`, `/write-info`, `/write-prompts`, `/write-report`, `/write-spec`, `/write-strut`, `/write-tasks-plan`, `/write-template`, `/write-test-plan`

### 10.6 Verbs Proposed in AGENSYNTAX-IN02

- `/new` (Concept A, session-new) - CONFLICT-HARD: Claude Code alias of `/clear`, Devin alias of `/clear`, Codex built-in → replaced by `/start`
- `/archive` (Concept A, session-archive) - CONFLICT-HARD: Codex built-in, Devin cloud-session command → replaced by `/close`
- `/update` (Concept A, conversation-update) - CONFLICT-HARD: Devin `/update` (CLI self-update), listed in the Claude Code reference → replaced by `/record`
- `/release` (Concept A, project-release) - CONFLICT-NEAR: start of Claude Code `/release-notes` → not adopted; `/project-release` stays (U4)
- `/configure` (Concept A, switch-model and workspace-setup) - CONFLICT-NEAR: same operation as `/config` on all three platforms → not adopted; `/workspace-setup` and `/switch-model` stay
- `/load` (Concept A, session-load and prime) - CONFLICT-NONE → not adopted; the existing `/prime` absorbs session-load (fewer new verbs, AGEN `[PRIME]` exists)
- `/review` (Concept D) - CONFLICT-HARD on all three platforms (Claude Code alias, Codex built-in, Devin system skill)
- `/run` (Concept D) - CONFLICT-HARD: Claude Code bundled skill
- `/create`, `/change`, `/explore`, `/track` (Concept D), `/make` (Concept E) - CONFLICT-NONE

### 10.7 AGEN Verbs Reserved as Slash Names

These AGEN verbs stay planning-only bracket verbs (CR-4):
- CONFLICT-HARD: `[PLAN]` (all three), `[REVIEW]` (all three), `[RECAP]` (all three), `[STATUS]` (all three), `[CONTINUE]` (Claude Code alias, Devin), `[ARCHIVE]` (Codex, Devin), `[HANDOFF]` (Devin)
- CONFLICT-HARD, used by existing workflows (CR-2): `[VERIFY]`, `[IMPLEMENT]`
- CONFLICT-NEAR: `[GO]` (`/goal`), `[CONFIGURE]` (`/config`)

### 10.8 Collision Behavior

- **Claude Code** - "A same-named project skill replaces a bundled command but never its aliases" [VERIFIED 2026-09-21 per `_INFO_HOW_CLAUDE_CODE_WORKS.md` Section 7.2]. Exception: bundled `/verify` overwrites `.claude/skills/verify/SKILL.md`, hence `ipps-verify`. Precedence between a project skill and a non-skill built-in command (`/rename`) is not documented in the read sources [ASSUMED: built-in wins; needs a test]. Plugins namespace their skills as `/plugin-name:skill-name` [VERIFIED]
- **Devin** - precedence between a skill and a built-in slash command of the same name is not documented in the read sources [ASSUMED: built-in wins; needs a test]. System skills are called with `@skills:<name>` [VERIFIED]
- **Codex** - skills are invoked with `$<name>`; slash names belong to built-ins, so a skill never shadows a built-in. The conflict is user confusion only: `$review` (IPPS) next to `/review` (Codex) [VERIFIED invocation per `_INFO_HOW_CODEX_WORKS.md`]

### 10.9 Outdated Platform Claims in `docs/`

- `_INFO_HOW_TO_USE_IPPS_WITH_CLAUDE_CODE.md` Section 4: "All other 70 IPPS skill names are unreserved ... [VERIFIED 2026-09-23]". No longer true: the official reference (read 2026-11-03) lists `/rename` (built-in) and `/deep-research` (bundled workflow) [VERIFIED]
- `_INFO_HOW_CLAUDE_CODE_WORKS.md` Sections 7.1 and 7.2 lack `/rename`, `/recap`, `/goal`, `/run`, `/deep-research`, and others present in the official reference [VERIFIED]

### 10.10 Observation: Different Verb Spaces

- The host agents are coding agents. Their reserved verbs act on 1) the chat session (`new`, `clear`, `resume`, `continue`, `rename`, `archive`, `fork`, `recap`, `export`, `compact`), 2) agent settings (`model`, `mode`, `plan`, `config`, `effort`, `fast`), 3) code (`review`, `diff`, `simplify`, `debug`, `verify`, `run`) [VERIFIED by the lists in 10.4]
- The IPPS document-intelligence verbs (`/write`, `/propose`, `/draft`, `/analyze`, `/critique`, `/reconcile`, `/convert`, `/translate`, `/record`, `/audit`) collide with none of them [VERIFIED]
- All 4 HARD conflicts of existing names are in the host agents' verb space: session control (`/rename`), code verification (`/verify`), code changes (`/implement`), and a bundled research workflow (`/deep-research`)
- **"Session" is polysemous**: IPPS session = work-session folder with NOTES, PROGRESS, PROBLEMS; host session = chat transcript. IPPS keeps the object `SESSION` but only with IPPS-only verbs (`/start`, `/prime`, `/save`, `/finalize`, `/close`), never with host verbs (`/new`, `/resume`, `/rename`, `/archive`) [ASSUMED]

## 11. Verb Catalog and Preview of All 63 Workflows

Target-state preview. Nothing is renamed or removed until the decisions in Section 12 and the SPEC. Existing names are kept (CR-2); new verbs are `CONFLICT-NONE` (CR-1).

- 30 verbs: 20 existing names kept, 10 new verbs (`/write`, `/propose`, `/draft`, `/convert`, `/start`, `/audit`, `/record`, `/save`, `/finalize`, `/close`)
- 43 workflows absorbed; 20 kept + 43 absorbed = 63
- Conflict states of the 30 verbs: CONFLICT-HARD 3 (`/verify`, `/implement`, `/rename`), CONFLICT-NEAR 4 (`/research`, `/go`, `/remove`, `/switch-model`), CONFLICT-NONE 23

Block format per verb: AGEN verb - side-effect class - conflict state (new or existing name); signature; knowledge; preview lines `today → concept`.

### 11.1 Create

**`/write`** - `[WRITE]` - Create - CONFLICT-NONE (new)
- Signature: `/write <OBJECT> [from <input>] [for <goal>] [to <target>] [in <scope>] [using <TECHNIQUE>] [as <PERSONA>] [tier 1|2|3] [plan only] [inline]`
- Knowledge: OBJECT GUIDES + TEMPLATE via `@skills:write-documents` routing table; technique and persona files when named
- `/write-info` → `/write INFO from <input> for "<question>"`
- `/write-spec` → `/write SPEC from _INFO_TOPIC.md`
- `/write-impl-plan` → `/write IMPL from _SPEC_TOPIC.md`
- `/write-test-plan` → `/write TEST from _SPEC_TOPIC.md`
- `/write-tasks-plan` → `/write TASKS from _IMPL_TOPIC.md, _TEST_TOPIC.md`
- `/write-strut` → `/write STRUT from _SPEC_TOPIC.md for "migrate auth to tokens"`
- `/write-prompts` → `/write PROMPTS from _IMPL_TOPIC.md`
- `/write-template` → `/write TEMPLATE for "<document kind>"`
- `/write-article` → `/write ARTICLE from ARTICLE-DRAFT-01_Title.md as <PERSONA>`
- `/write-report` → `/write REPORT from REPORT-DRAFT-01_Title.md tier 2`
- `/write-ebook` → `/write EBOOK from EBOOK-DRAFT-01_Title.md` (tier 3 is the EBOOK default in the object registry)
- `/ascii-diagram` (create mode) → `/write DIAGRAM for "<what it shows>" to _SPEC_TOPIC.md`

**`/propose`** - `[PROPOSE]` - Create - CONFLICT-NONE (new)
- Signature: `/propose <OBJECT> [from <input>] [for <audience>] [in <scope>] [using <TECHNIQUE>] [<N> options] [compare <ID>, <ID>[, <ID>[, <ID>]]] [inline]`
- Knowledge: `document_types/[OBJECT]_GUIDES.md` (option scoring), `[OBJECT]_TEMPLATE.md` section OPTIONS; technique GUIDES when named
- `/propose-article` → `/propose ARTICLE from _INFO_TOPIC-IN01_Summary.md using ABTSTORY 3 options`
- `/propose-report` → `/propose REPORT from _INFO_TOPIC-IN02_Analysis.md`
- `/propose-ebook` → `/propose EBOOK from _INFO_TOPIC-IN02_Analysis.md compare MINTO, STA, DIATAXIS`

**`/draft`** - `[DRAFT]` - Create - CONFLICT-NONE (new)
- Signature: `/draft <OBJECT> [from <input>] [for <audience or recipient>] [in <scope>] [using <TECHNIQUE>] [as <PERSONA>] [inline]`
- Knowledge: `[OBJECT]_GUIDES.md`, `[OBJECT]_TEMPLATE.md` section DRAFT; `CONVERSATION_GUIDES.md` for messages written as the user (to create)
- `/draft-article` → `/draft ARTICLE from option 2 in ARTICLE-OPTIONS-01_Title.md`
- `/draft-report` → `/draft REPORT from option 1 in REPORT-OPTIONS-01_Title.md`
- `/draft-ebook` → `/draft EBOOK from option 3 in EBOOK-OPTIONS-01_Title.md`
- `/conversation-draft` → `/draft CONVERSATION for Jane Smith from <latest message>`

**`/research`** - `[RESEARCH]` - Create - CONFLICT-NEAR (existing name; Claude Code `/deep-research`)
- Signature: `/research <question> [for <purpose>] [in <scope>] [using <STRATEGY>, <PROFILE>, <AREA>] [tier 1|2|3] [plan only] [approaches <A>, <B>[, ...]]`
- Knowledge: `@skills:research-methods` (RESEARCH_GUIDES, strategy files, `research_profiles/`, `research_areas/`)
- `/research "<question>"` → `/research "<question>"` (tier 1 default)
- `/deep-research "<question>"` (CONFLICT-HARD) → `/research "<question>" tier 2 using MCPI`
- `/research-program "<goal>"` (CONFLICT-NEAR) → `/research "<goal>" tier 3 approaches "<A>", "<B>", "<C>"`

**`/analyze`** - `[ANALYZE]` - Create - CONFLICT-NONE (existing name)
- Signature: `/analyze <input> [for <question>] [in <scope>] [using <STAGE>] [tier 1|2|3] [plan only]`
- Knowledge: `@skills:analysis-methods` (`ANALYSIS_GUIDES.md`, `[STAGE]_GUIDES.md`, `[STAGE]_TEMPLATE.md`). Without `using`: full stage sequence (today's `/analyze`)
- `/analyze T01_* T02_* tier 3` → `/analyze T01_TOPIC_* T02_TOPIC_* tier 3` (writes STRUT and prompt files, stops; F2)
- `/pattern-detect` → `/analyze T01_TOPIC_* using PATTERN-DETECTION`
- `/hypothesize` → `/analyze _INFO_TOPIC-IN02_PatternMap.md using HYPOTHESIS`
- `/validate` → `/analyze _INFO_TOPIC-IN03_HypothesisRegister.md using VALIDATION`
- `/investigate` → `/analyze "<issue>" using INVESTIGATION`

**`/convert`** - `[CONVERT]` (new AGEN verb) - Create - CONFLICT-NONE (new)
- Signature: `/convert <input> to <FORMAT or path> [for <purpose>] [in <scope>] [inline]` - FORMAT: `markdown`, `html`, `pdf`, `bundle` (verb-owned); `for publishing` strips PromptSystem artifacts
- Knowledge: `@skills:llm-transcription`, `@skills:pdf-tools` (to markdown), `@skills:renderings` (to html, pdf), `@skills:research-methods` and `IPPSKBNDL-SP01` (to bundle)
- `/transcribe` → `/convert report.pdf to markdown`
- `/render` → `/convert _INFO_TOPIC.md to pdf`
- `/bundle` → `/convert T01_TOPIC_Folder to bundle`
- `/cleanup <file> prompt system` (file mode of `/cleanup`) → `/convert _INFO_TOPIC.md for publishing to TOPIC_Article.md` (in place: add `inline`)

**`/translate`** - `[TRANSLATE]` (new AGEN verb) - Create - CONFLICT-NONE (existing name)
- Signature: `/translate <input> to <LANGUAGE>[, <LANGUAGE>] [in <scope>]`
- `/translate` → `/translate _INFO_TOPIC.md to DE, PT`

**`/start`** - `[START]` (new AGEN verb) - Create - CONFLICT-NONE (new)
- Signature: `/start <OBJECT> [from <input>] [for <goal or counterparty>] [in <location>]` - OBJECT: `SESSION`, `CONVERSATION`
- Knowledge: `@skills:session-management` (SESSION); conversation template (to move into `CONVERSATION_TEMPLATE.md`)
- `/session-new` → `/start SESSION for "<goal>" in [SESSIONS_FOLDER]`
- `/conversation-start` → `/start CONVERSATION for Jane Smith from chat`

### 11.2 Report-only

**`/critique`** - `[CRITIQUE]` - Report-only - CONFLICT-NONE (existing name)
- Signature: `/critique <target> [against facts|<file>] [for <goal>] [in <scope>]`
- Knowledge: target GUIDES (logic, goal alignment); `against facts`: external evidence, procedure in `FACT-CHECK_GUIDES.md` (to create)
- `/critique` → `/critique _SPEC_TOPIC.md` (writes `_SPEC_TOPIC_CRITIQUE.md`)
- `/fact-check` → `/critique _INFO_TOPIC.md against facts` (writes `_INFO_TOPIC_FACT-CHECK.md`, today's output name)

**`/reconcile`** - `[RECONCILE]` - Report-only - CONFLICT-NONE (existing name)
- Signature: `/reconcile <review file>[, <review file>] [for <goal>]`
- `/reconcile` → `/reconcile _SPEC_TOPIC_CRITIQUE.md, _SPEC_TOPIC_FACT-CHECK.md`

**`/audit`** - `[AUDIT]` (new AGEN verb) - Report-only - CONFLICT-NONE (new)
- Signature: `/audit <executed work> [against <plan or prompt file>]`
- Knowledge: `@skills:drift-control`, CHECKS section PD of the object (GRUC-SP01)
- `/drift-detect` → `/audit last run against _PROMPTS_01-Topic.md` (writes `__DRIFT_*`)

**`/prime`** - `[PRIME]` - Report-only (loads context, writes no file) - CONFLICT-NONE (existing name)
- Signature: `/prime [<OBJECT>] [<name>] [in <location>]` - OBJECT: workspace (default), `SESSION`
- `/prime` → `/prime`
- `/session-load` → `/prime SESSION _2026-01-15_TopicName`

**`/test`** - `[TEST]` - Report-only - CONFLICT-NONE (existing name, coding verb, unchanged)
- `/test` → `/test [<scope>]`

### 11.3 Edit

**`/verify`** - `[VERIFY]` - Edit (fixes rule violations in place) - CONFLICT-HARD (existing name; Claude Code bundled skill; deployed as `/ipps-verify`)
- Signature: `/verify <target> [against rules|<file>] [in <scope>]`
- Knowledge: RULES + TEMPLATE of the object and of every constant in the target header (DRSYNART-SP01 Section 8.4)
- `/verify` → `/verify _SPEC_TOPIC.md` (authority `rules` by default), `/verify _IMPL_TOPIC.md against _SPEC_TOPIC.md`

**`/improve`** - `[IMPROVE]` - Edit - CONFLICT-NONE (existing name)
- Signature: `/improve <target> [for <goal>]`
- Knowledge: CHECKS section QI of the object
- `/improve` → `/improve _SPEC_TOPIC.md`

**`/fix`** - `[FIX]` - Edit - CONFLICT-NONE (existing name)
- Signature: `/fix [<OBJECT>] <problem or target> [from <evidence>] [in <scope>]` - OBJECT: `BUG`, `DRIFT`, `DIAGRAM`; none = generic problem
- Knowledge: `BUG_GUIDES.md` (to create), `@skills:drift-control`, `ASCII_ART_GUIDES.md`
- `/fix` → `/fix "<problem>"`
- `/bugfix` → `/fix BUG "<symptom>"` (commit leaves the verb, Section 6.5)
- `/drift-correct` → `/fix DRIFT from __DRIFT_Topic.md`
- `/ascii-diagram` (fix mode) → `/fix DIAGRAM in _SPEC_TOPIC.md`

**`/implement`** - `[IMPLEMENT]` - Edit - CONFLICT-HARD (existing name; Devin system skill)
- Signature: `/implement <plan or findings> [from <file>] [in <scope>]`
- `/implement` → `/implement _IMPL_TOPIC.md`, `/implement accepted findings from _SPEC_TOPIC_CRITIQUE.md`

**`/rename`** - `[REFACTOR]` - Edit - CONFLICT-HARD (existing name; built-in on all three platforms)
- Signature: `/rename <term> to <new term> [in <scope>]`
- `/rename` → `/rename "OldTerm" to "NewTerm" in workspace`

**`/record`** - `[RECORD]` (new AGEN verb) - Edit (append-only) - CONFLICT-NONE (new)
- Signature: `/record <OBJECT> [from <input>] [for <counterparty>] [in <log>]` - OBJECT: `FAILURE` (FAILS.md), `LEARNING` (LEARNINGS.md), `CONVERSATION` (CONVERSATION file)
- Knowledge: `LEARNING_GUIDES.md` (to create; retrospective steps of `/learn`), conversation templates
- `/fail` → `/record FAILURE from chat`
- `/learn` → `/record LEARNING from TOPIC-PR-0001`
- `/conversation-update` → `/record CONVERSATION for Jane Smith from <pasted emails>`

**`/save`** - `[SAVE]` (new AGEN verb) - Edit (session tracking files) - CONFLICT-NONE (new)
- `/session-save` → `/save SESSION`

**`/finalize`** - `[FINALIZE]` - Edit (session tracking files, sync to project) - CONFLICT-NONE (new)
- `/session-finalize` → `/finalize SESSION`

### 11.4 Destructive or Outward-Facing

All verbs in this class keep preview-then-confirm and never take their target from context or default (AGENSYNTAX-IN02 Section 2.3). Exception kept from today: `/cleanup` categories delete after preview without confirmation; this behavior moves unchanged into `/remove`.

**`/remove`** - `[REMOVE]` (new AGEN verb) - Destructive - CONFLICT-NEAR (existing name; Devin `/remove-dir`)
- Signature: `/remove <what> [in <scope>]` - what: files, `temp files`, `reviews`, `markers`, session content, conversation content (verb-owned list)
- `/remove` → `/remove "<files>" in T01_TOPIC_Folder`
- `/cleanup` → `/remove temp files in <scope>`
- `/cleanup review [path]` → `/remove reviews in T01_TOPIC_Folder`
- `/cleanup <file>` (general file mode) → `/remove markers in _INFO_TOPIC.md`

**`/close`** - `[CLOSE]` - Destructive (moves the session folder) - CONFLICT-NONE (new)
- `/session-archive` → `/close SESSION`

**`/sync`** - `[SYNC]` (new AGEN verb) - Outward-facing - CONFLICT-NONE (existing name)
- Signature: `/sync <what> [from <source>] [to <target>]`
- `/sync` → `/sync _SPEC_TOPIC.md to _IMPL_TOPIC.md, _TEST_TOPIC.md`, `/sync knowledge from source`, `/sync workspace settings to <repo>`

**`/commit`**, **`/deploy`**, **`/project-release`** - `[COMMIT]`, `[DEPLOY]`, none - Outward-facing - CONFLICT-NONE (existing names, coding verbs, unchanged; U4)

### 11.5 Orchestrator

**`/go`** - `[GO]` - inherits the classes and gates of the verbs it runs - CONFLICT-NEAR (existing name; `/goal` in Claude Code and Codex)
- Signature: `/go [<goal or plan>] [using <PIPELINE>] [in <scope>]`
- Writes STRUT or TASKS, executes the calls, stops at decision gates (F2: STRUT is a planning document)
- `/go` → `/go "<goal>"`, `/go _SPEC_TOPIC.md using VCRIV`, `/go __STRUT_TOPIC.md`

### 11.6 Environment (unchanged; U4)

**`/workspace-setup`** - `[CONFIGURE]` - Edit - CONFLICT-NONE (existing name)
- Family workflow kept as object-first exception, because its 5 use cases are environment administration, not document work
- `/compare-workspace-setup` → `/workspace-setup compare against <other workspace>`

**`/switch-model`** - `[CONFIGURE]` - Edit - CONFLICT-NEAR (existing name; `/model` on all three platforms)
- Cascade only; excluded from the Claude Code deployment today

### 11.7 Count Check

- Create (8 verbs): `/write` 12, `/propose` 3, `/draft` 4, `/research` 3, `/analyze` 5, `/convert` 3, `/translate` 1, `/start` 2 = 33 workflows
- Report-only (5 verbs): `/critique` 2, `/reconcile` 1, `/audit` 1, `/prime` 2, `/test` 1 = 7
- Edit (8 verbs): `/verify` 1, `/improve` 1, `/fix` 3, `/implement` 1, `/rename` 1, `/record` 3, `/save` 1, `/finalize` 1 = 12
- Destructive or outward-facing (6 verbs): `/remove` 2, `/close` 1, `/sync` 1, `/commit` 1, `/deploy` 1, `/project-release` 1 = 7
- Orchestrator (1 verb): `/go` 1 = 1
- Environment (2 verbs): `/workspace-setup` 2, `/switch-model` 1 = 3
- Total: 30 verbs, 33 + 7 + 12 + 7 + 1 + 3 = 63 workflows. Mode splits (counted once): `/ascii-diagram` under `/write` (create) and `/fix` (fix); `/cleanup` under `/remove` (delete, markers) and `/convert` (publishing)

### 11.8 Reference Tasks (AGENSYNTAX-IN02 Section 3)

- **T1** `/draft CONVERSATION for Jane Smith`
- **T2** `/write STRUT from _SPEC_TOPIC.md for "migrate auth to tokens"`
- **T3** `/propose ARTICLE from _INFO_TOPIC-IN01_Summary.md using ABTSTORY 3 options`
- **T4** `/critique _SPEC_TOPIC.md against facts`
- **T5** `/research "<question>" tier 2`
- **T6** `/start SESSION for "<goal>" in [SESSIONS_FOLDER]`
- **T7** `/remove reviews in T01_TOPIC_Folder`
- **T8** `/analyze T01_TOPIC_* T02_TOPIC_* tier 3` → writes `__STRUT_` and `_PROMPTS_01..03` calling `/analyze ... using PATTERN-DETECTION`, `/analyze ... using HYPOTHESIS`, `/analyze ... using VALIDATION`, `/verify`, `/critique`, then stops; `/go` executes the sequence as a separate invocation (AGENSYNTAX-IN02 Section 2.9)

### 11.9 Behavior Changes a User Would Notice

- `/fact-check` becomes `/critique ... against facts`; output file name unchanged
- `/cleanup` splits by side-effect class: deletion and markers → `/remove`; publishing → `/convert ... for publishing` (default writes a new file; today in place, which now needs `inline`)
- `/bugfix` no longer commits; the commit is a separate call
- Research depth is chosen with `tier` instead of 3 commands
- `/prime SESSION` replaces `/session-load`; `/close SESSION` replaces `/session-archive`
- HARD-conflict names stay: `/verify` (still `/ipps-verify` on Claude Code), `/implement`, `/rename`

### 11.10 AGEN Extension

- **AGEN verbs that become workflow verbs** (unchanged definitions): `[WRITE]`, `[PROPOSE]`, `[DRAFT]`, `[RESEARCH]`, `[ANALYZE]`, `[CRITIQUE]`, `[RECONCILE]`, `[VERIFY]`, `[IMPROVE]`, `[FIX]`, `[IMPLEMENT]`, `[REFACTOR]` (as `/rename`), `[PRIME]`, `[TEST]`, `[GO]`, `[COMMIT]`, `[DEPLOY]`, `[FINALIZE]`, `[CLOSE]`, `[CONFIGURE]`
- **New AGEN verbs** (one per new workflow verb without an AGEN entry): `[CONVERT]`, `[TRANSLATE]`, `[START]`, `[AUDIT]`, `[RECORD]`, `[SAVE]`, `[REMOVE]`, `[SYNC]`
- **Changed definition**: `[CLOSE]` today "Mark as done and sync data to container"; for `SESSION` it also moves the folder to the archive, absorbing the slash use of `[ARCHIVE]` (which stays a planning-only verb, CR-4)
- **Compound verbs retire**: `[WRITE-INFO]`, `[WRITE-SPEC]`, `[WRITE-IMPL-PLAN]`, `[WRITE-TEST-PLAN]` become `[WRITE](INFO ...)`, `[WRITE](SPEC ...)`, `[WRITE](IMPL ...)`, `[WRITE](TEST ...)`; `[PARTITION]` becomes `[WRITE](TASKS ...)`; `[INVESTIGATE]` becomes `[ANALYZE](... using INVESTIGATION)`
- **Planning-only AGEN verbs** (no workflow): `[EXPLORE]`, `[GATHER]`, `[READ]`, `[SCOPE]`, `[FRAME]`, `[PLAN]`, `[DECIDE]`, `[ASSESS]`, `[PRIORITIZE]`, `[EVALUATE]`, `[SYNTHESIZE]`, `[CONCLUDE]`, `[DEFINE]`, `[RECAP]`, `[CONTINUE]`, `[PROVE]`, `[PROTOTYPE]`, `[REVIEW]`, `[OUTLINE]`, `[SUMMARIZE]`, `[INTEGRATE]`, `[OPTIMIZE]`, `[CONSULT]`, `[CLARIFY]`, `[QUESTION]`, `[STATUS]`, `[RECOMMEND]`, `[CONFIRMS]`, `[PRESENT]`, `[HANDOFF]`, `[MERGE]`, `[ARCHIVE]`
- AGEN Scope stays valid (F1): bracket verbs remain excluded from workflow step bodies; the slash forms appear in invocation lines, signatures, prompt files, and planning documents (AGENSYNTAX-DD-01)

## 12. Open Decisions

AGENSYNTAX-DD-02 (concept) is set to Concept A as working direction (U1). Deferred, not presented here: resolution of the 4 HARD conflicts of existing names (U3), AGENSYNTAX-DD-05 (`/make` as user command), AGENSYNTAX-DD-06 (scope-boundary mentions in workflows).

### AGENSYNTAX-DD-03: How many verbs does the target state have?

**Problem**: The verb count decides how many slash commands a user learns and how many workflows remain to maintain.
**Context**: Each verb must keep one side-effect class (AGENSYNTAX-IN02 Section 2.8); new verbs must be `CONFLICT-NONE` (CR-1); existing names stay (CR-2). Under these rules only 2 further merges remain possible; the other merges of the AGENSYNTAX-IN02 aggressive variant either rename existing workflows or mix side-effect classes.

**Options**
- **1) 30 verbs (Section 11)** (recommended)
  - What: verb set as in Section 11
  - Why it works: every verb has one side-effect class and one GRUC role; every absorbed procedure has a target GUIDES file
  - Implication: 63 → 30 workflows; `/translate`, `/finalize`, `/close` stay separate commands
  - Why recommended: largest reduction that keeps every verb's behavior predictable from its name
- **2) 28 verbs**
  - What: `/translate` merges into `/convert ... to <LANGUAGE>`; `/finalize` merges into `/close SESSION` (finalize, then archive, in one confirmed call)
  - Why it works: translation is a conversion to another language; finalize always precedes archive
  - Implication: `/close` becomes a two-step destructive verb with a longer preview; a user who wants to finalize without archiving needs a flag (`plan only` does not fit), so a new flag is required

### AGENSYNTAX-DD-04: Where does a workflow declare its signature?

**Problem**: Users and agents need one place to read how a workflow is called; deploy scripts need a machine-readable source.
**Context**: The Agent Skills standard rejects unknown frontmatter keys such as `argument-hint`; Codex has no argument-hint field; Claude Code and Devin support `argument-hint` (Section 8.2).

**Options**
- **1) Markdown `## Signature` in the body; deploy scripts generate `argument-hint` from the grammar line** (recommended)
  - What: SIG-1 to SIG-7 (Section 7.2); `_PROMPTS_UpdateClaude.md` and later deploy prompts read the first signature line
  - Why it works: the body is copied unchanged to every platform; the grammar line is extractable by line position
  - Implication: one deploy step per platform must generate `argument-hint`
  - Why recommended: the only option that is valid on Cascade, Claude Code, Devin, Codex, and the Agent Skills standard at once
- **2) Frontmatter YAML signature (AGENSYNTAX-IN02 Concept B)**
  - What: typed `signature:` block in frontmatter
  - Why it works: lintable by a script
  - Implication: custom frontmatter keys must be stripped for Skills API packaging; users read YAML instead of a sentence
- **3) Both, frontmatter generated from the body**
  - What: body is the source; a script writes a YAML copy for linting
  - Why it works: keeps readability and lintability
  - Implication: two representations to keep in sync; one more generated artifact

### AGENSYNTAX-DD-07: Which verbs form the session lifecycle?

**Problem**: The AGENSYNTAX-IN02 session verbs `/new` and `/archive` are reserved by Claude Code, Devin, and Codex (Section 10.6).
**Context**: CR-1 forbids conflicting new verbs; CR-3 forbids verbs that act on the host chat session. "Session" means a work-session folder in IPPS and a chat transcript in the host agents (Section 10.10).

**Options**
- **1) `/start`, `/prime`, `/save`, `/finalize`, `/close`** (recommended)
  - What: `/start SESSION`, `/prime SESSION <name>`, `/save SESSION`, `/finalize SESSION`, `/close SESSION`
  - Why it works: all 5 are `CONFLICT-NONE`; `/prime` is an existing workflow and AGEN verb, so only 4 new verbs; `/start` also serves `CONVERSATION`
  - Implication: `[CLOSE]` definition extended to "move to archive" (Section 11.10)
  - Why recommended: conflict-free, reuses an existing verb, reads as plain English
- **2) Keep `/session-new`, `/session-load`, `/session-save`, `/session-finalize`, `/session-archive`**
  - What: object-first family names stay, like the Environment group
  - Why it works: no new names, `CONFLICT-NONE` today
  - Implication: 5 workflows stay outside the verb pattern; the single-pattern goal (AGENSYNTAX-PR-0002) has an exception
- **3) `/start`, `/load`, `/save`, `/finalize`, `/close`**
  - What: as option 1, but a new verb `/load` instead of `/prime SESSION`
  - Why it works: `/load` is `CONFLICT-NONE` and plainer English than "prime"
  - Implication: one more verb; `/load` and `/prime` overlap in meaning (both load context)

Reply format: `DD-03 1, DD-04 1, DD-07 1`

## 13. Next Steps

1. User decides AGENSYNTAX-DD-03, DD-04, DD-07
2. Later (U3): resolve the 4 HARD conflicts of existing names (`/verify`, `/deep-research`, `/rename`, `/implement`). Options to evaluate then: rename the verb, deploy-time prefix `ipps-<verb>` (precedent `ipps-verify`), plugin namespace `/ipps:<verb>` (Claude Code plugins namespace skills as `/plugin-name:skill-name` [VERIFIED]; Devin and Codex namespaces not verified)
3. Test collision behavior: project skill named `rename` in Claude Code and Devin CLI; slash-menu highlight for `/go` vs `/goal` and `/research` vs `/deep-research`; `/<verb>` call lines in prompt files executed on Codex
4. Update `_INFO_HOW_TO_USE_IPPS_WITH_CLAUDE_CODE.md` Section 4 and `_INFO_HOW_CLAUDE_CODE_WORKS.md` Sections 7.1-7.2 with the reserved names of 2026-11-03 (Section 10.9)
5. Build the object registry and the AGEN lexicon sections (keywords, constant types with registry pointers); add aliases to the owning registries (Section 5.1)
6. Write `AGENSYNTAX-SP01` with grammar (G1-G7), signature rules (SIG-1 to SIG-7), snap rules (S1-S5, SG-1 to SG-5), and conflict rules (CR-1 to CR-5)
7. After SPEC confirmation, GRUC additions: `WORKFLOW_RULES.md` (signature section, verb-name conflict check with dated reserved lists), `WORKFLOW_GUIDES.md` (choosing a verb, pointing slots to registries), `WORKFLOW_CHECKS.md` (PD: echo line printed; QI: signature completeness), `WORKFLOW_TEMPLATE.md` (`## Signature`), `agentic-english.md` and `AGEN-SP01` (keywords, constant types, new verbs), `IPPSWFLW-SP01`

## 14. Sources

**Primary Sources** (local, read 2026-11-03):
- `AGENSYNTAX-IN03-SC-IPPS-CURST`: `_INFO_HOW_IPPS_WORKFLOWS_CURRENTLY_WORK.md [AGENSYNTAX-IN01]` - 63 workflows, invocation formats, GUIDES and CHECKS gaps, polysemy [VERIFIED]
- `AGENSYNTAX-IN03-SC-IPPS-PRPSL`: `_INFO_IPPS_UNIFIED_WORKFLOW_PROPOSALS.md [AGENSYNTAX-IN02]` - Concept A, shared baseline, reference tasks, open decisions [VERIFIED]
- `AGENSYNTAX-IN03-SC-IPPS-AGNRL`: `[PROMPTSYSTEM_FOLDER]/rules/agentic-english.md` - AGEN scope and verb list [VERIFIED]
- `AGENSYNTAX-IN03-SC-IPPS-GRCSP`: `specs/_SPEC_GRUC_STANDARD.md [GRUC-SP01]` - consumer mapping, CHECKS invisible during execution [VERIFIED]
- `AGENSYNTAX-IN03-SC-IPPS-WFLSP`: `specs/_SPEC_IPPS_WORKFLOWS.md [IPPSWFLW-SP01]` and `specs/_SPEC_IPPS_SKILLS.md [IPPSSKLS-SP01]` - workflow and skill structure [VERIFIED]
- `AGENSYNTAX-IN03-SC-IPPS-DRSY`: `_SPEC_IPPS_RESEARCH_AND_WRITING_TOOLS.md [DRSYNART-SP01]` - MUST-NOT-FORGET (tier), Sections 8.1-8.4, 8.7, FR-05, DD-08, DD-17, IG-10 [VERIFIED]
- `AGENSYNTAX-IN03-SC-IPPS-PRMRL`: `[PROMPTSYSTEM_FOLDER]/skills/write-documents/PROMPTS_RULES.md` - PRMT-CT-08, PRMT-CT-10, PRMT-CT-11 [VERIFIED]
- `AGENSYNTAX-IN03-SC-IPPS-WDSKL`: `[PROMPTSYSTEM_FOLDER]/skills/write-documents/` - SKILL.md routing, `writing_techniques/` (9 GUIDES files, MINTO file set), `writing_personas/README.md` [VERIFIED]
- `AGENSYNTAX-IN03-SC-IPPS-WFDIR`: `[PROMPTSYSTEM_FOLDER]/workflows/` - 63 workflow descriptions, `default_tier` values, `/cleanup` and `/sync` triggers, `/propose-article` grammar [VERIFIED]
- `AGENSYNTAX-IN03-SC-IPPS-SKLWF`: `docs/_INFO_HOW_TO_IMPLEMENT_WORKFLOWS_AS_SKILLS.md [SKLWRKFL-IN01]` - user-only skills, 32-36 ceiling [VERIFIED]
- `AGENSYNTAX-IN03-SC-IPPS-CCWRK`: `docs/_INFO_HOW_CLAUDE_CODE_WORKS.md` Sections 7.1-7.3 - built-ins, bundled skills, same-name replacement rule, `/verify` recipe overwrite [VERIFIED]
- `AGENSYNTAX-IN03-SC-IPPS-CCUSE`: `docs/_INFO_HOW_TO_USE_IPPS_WITH_CLAUDE_CODE.md` Section 4 - reserved-name claim of 2026-09-23 [VERIFIED]
- `AGENSYNTAX-IN03-SC-IPPS-CCDPL`: `_PROMPTS_UpdateClaude.md` - `ipps-verify` rename, `switch-model` exclusion [VERIFIED]
- `AGENSYNTAX-IN03-SC-IPPS-DVWRK`: `docs/_INFO_HOW_DEVIN_WORKS.md` Sections 10, 13 - slash commands, skill paths, `devin migrate workflows` [VERIFIED]
- `AGENSYNTAX-IN03-SC-IPPS-DVCHG`: `docs/_INFO_DEVIN_RECENT_CHANGES.md` Section 3.4 - new slash commands, ACP slash commands [VERIFIED]
- `AGENSYNTAX-IN03-SC-IPPS-CXWRK`: `docs/_INFO_HOW_CODEX_WORKS.md` - built-in slash commands, `$skill-name` invocation, `.agents/skills/`, context budget [VERIFIED 2026-07]

**External Sources** (read 2026-11-03):
- `AGENSYNTAX-IN03-SC-CLAUD-CMDS`: https://code.claude.com/docs/en/commands - built-in commands, bundled skills and workflows, slash-menu matching rule [VERIFIED]
- `AGENSYNTAX-IN03-SC-CLAUD-SKLS`: https://code.claude.com/docs/en/skills - bundled skills, frontmatter fields, `argument-hint`, `$ARGUMENTS`, Agent Skills key restriction, plugin namespace, angle brackets in descriptions [VERIFIED]
- `AGENSYNTAX-IN03-SC-DEVIN-CMDS`: https://docs.devin.ai/cli/reference/commands - Devin CLI slash commands [VERIFIED]
- `AGENSYNTAX-IN03-SC-DEVIN-SKLCR`: https://docs.devin.ai/cli/extensibility/skills/creating-skills - frontmatter fields `argument-hint`, `triggers` [VERIFIED]
- `AGENSYNTAX-IN03-SC-DEVIN-SKLPG`: https://docs.devin.ai/product-guides/skills - System Skills plugin (`implement`, `plan`, `triage`, `review`), `@skills:` invocation, argument substitution [VERIFIED]
- `AGENSYNTAX-IN03-SC-OPNAI-CXCMD`: https://learn.chatgpt.com/docs/developer-commands?surface=cli - Codex CLI and IDE extension slash commands [VERIFIED]

## 15. Document History

**[2026-11-03 17:00]**
- Initial INFO created: Concept A worked out (word classes, grammar with 8 keywords, term snapping, skill binding, signature block, skill migration, prompt files), platform conflict audit for Claude Code, Devin, Codex, verb catalog with preview of all 63 workflows, open decisions DD-03, DD-04, DD-07

