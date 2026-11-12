# SPEC: IPPS Research and Writing Tools - Three Layers, Three Tiers

**Doc ID**: DRSYNART-SP01
**Feature**: research-and-writing-tools
**Goal**: Specify the restructured IPPS research-to-deliverable pipeline - three layers (Classic Research, Analysis and Synthesis, Knowledge Packaging), one execution-depth dial (tier 1, 2, 3) shared by all layers, three skills, eighteen entry workflows, and the GRUC content standard every new file must meet - so that the same tools serve a 2-10 minute article, a 10-60 minute report, and a 2-20 hour ebook program with consistent quality
**Timeline**: Created 2026-10-29, Updated 6 times (2026-10-29 - 2026-11-08)
**Target file(s)**:
- `[PROMPTSYSTEM_FOLDER]/skills/research-methods/` (extend: GUIDES, CHECKS, Sources template; rename subfolders to `research_profiles/`, `research_areas/`)
- `[PROMPTSYSTEM_FOLDER]/skills/analysis-methods/` (new skill, 13 new files + 3 `INVESTIGATION_*` files moved from `write-documents`)
- `[PROMPTSYSTEM_FOLDER]/skills/write-documents/` (composite router, `document_types/`, `writing_techniques/`, `writing_personas/`)
- `[PROMPTSYSTEM_FOLDER]/workflows/` (exists: `research-program.md`, `bundle.md`, `pattern-detect.md`, `hypothesize.md`, `validate.md`, `analyze.md`, 9 writing workflows, `deep-research.md`, `research.md`, `investigate.md`; deleted: `propose-minto.md`, `write-minto.md`)
- `[PROMPTSYSTEM_FOLDER]/workflows/verify.md`, `critique.md`, `improve.md` (detection repointed)
- `README.md`, `ID-REGISTRY.md`, `rules/promptsystem-core.md` (registration)

**Depends on:**
- `NOTES.md [DRSYNART-NOTES]` Key Decisions for the verbatim wording of DD-01..DD-09, DD-15..DD-20 (authoritative over any restatement in this SPEC)
- `_INFO_TARGET_ARCHITECTURE.md [DRSYNART-IN02]` for the three-layer model, hand-over contracts C1-C3, and the ten confirmed decisions DD-01..DD-07, DD-18..DD-20
- `2026-10-19_How-IPPS-Is-Currently-Used-To-Perform-Research-Tasks-And-Write-Documents.md [DRSYNART-IN01]` for the 16 invariants (Section 7) and the knowledge location map (Section 6)
- `T01_RSRCHMTHD_ResearchToArticleMethods_2026-10-19/_INFO_RSRCHMTHD-01_Summary.md [DRSYNART-RSRCHMTHD-IN01]` for the S1-S5 method chain, twelve artifacts, likelihood and confidence vocabulary
- `T01_.../_INFO_RSRCHMTHD-03_Terminology.md [DRSYNART-RSRCHMTHD-IN03]` for the 74 binding terms
- `T02_WRTSTYLTCH_WritingStylesAndTechniques_2026-10-29/WRITING_TECHNIQUES/` and `WRITING_PERSONAS/` for the compiled libraries (41 + 21 files) and `_INFO_WRTSTYLTCH-04 [DRSYNART-WRTSTYLTCH-IN04]` for the technique-to-media mapping
- `T04_WRTCRAFT_WritingCraftForGuides_2026-10-29/_INFO_WRTCRAFT-08_GuidesRewriteBlueprint.md [DRSYNART-WRTCRAFT-IN08]` for the required content per GRUC file type and the consistency layer stack; `_INFO_WRTCRAFT-01_Summary.md [DRSYNART-WRTCRAFT-IN01]` for the ten craft decisions per document type; `_INFO_WRTCRAFT-11 [DRSYNART-WRTCRAFT-IN11]` for the script-format decisions DD-21..24
- `specs/_SPEC_GRUC_STANDARD.md [GRUC-SP01]` for GRUC file types and consumer mapping; `specs/_SPEC_IPPS_WORKFLOWS.md [IPPSWFLW-SP01]` for workflow anatomy; `specs/_SPEC_IPPS_SKILLS.md [IPPSSKLS-SP01]` and `write-documents/SKILL_RULES.md` SK-AR-01..07 for composite skills; `specs/_SPEC_IPPS_PROMPT_FILE_FORMAT.md [IPPSPRMTFMT-SP01]` for prompt files; `specs/_SPEC_STRUT_STRUCTURED_THINKING.md` for STRUT
- `specs/_SPEC_IPPS_KNOWLEDGE_BUNDLE_FORMAT.md [IPPSKBNDL-SP01]` for the output format of the optional `/bundle` workflow

**Does not depend on:**
- `specs/_SPEC_INVESTIGATE_WORKFLOW.md [INVESTIGATE-SP01]` - `/investigate` behavior is unchanged; only its skill-file paths move to `analysis-methods` (DD-01)
- Any IMPL or TEST document - they follow this SPEC after `[ACTOR]` confirmation

## MUST-NOT-FORGET

- User decisions (DD-01..DD-09, DD-15..DD-20) are binding; this SPEC never overrides them. Agent-proposed decisions start at DD-30 and need user confirmation
- One concept, one name: "tier" is the execution-depth dial for every layer (tier 1 single-turn, tier 2 planned, tier 3 program). Never introduce "level", "mode", "quick", or "full" as synonyms in files. "inline" is reserved for the DD-17 keyword (edit an existing file in place)
- Tier 3 is capped at the size of the `T04_WRTCRAFT` run: at most 8 prompt files, 35 prompts including checkpoints, 12 INFO deliverables per tier-3 call (NFR-01). This supersedes the earlier NOTES range "1-10 STRUTs, 10-200 prompts"; larger jobs are split into several calls
- Only the user selects `using <WRITING-TECHNIQUE-ID>` and `as <persona>` (DD-08). A workflow without them loads no library file
- Every GUIDES file follows the T04 blueprint (FR-30): purpose and reader outcome, decisions in working order with options and criteria, annotated exemplar links, named failure modes, quality heuristics, self-review questions. No fading exercises (DD-34)
- GRUC consumer boundaries hold (GRUC-SP01): GUIDES before work, RULES for `/verify`, CHECKS PD for `/drift-detect`, CHECKS QI for `/improve`, CHECKS invisible to the working agent. Repetition across the three file types is by design
- All edits go to `[PROMPTSYSTEM_FOLDER]` first, then robocopy to `[AGENT_FOLDER]` (invariant 1). Register rule-ID prefixes in `ID-REGISTRY.md` before any file uses them (invariant 2)
- Writing workflows never modify NOTES, PROBLEMS, PROGRESS, FAILS (invariant 6). Review workflows never modify the target (invariant 7)
- No workflow edit when a technique, persona, document type, or analysis stage is added: filename-pattern discovery only (FR-05)
- OPTIONS and DRAFT files are optional (DD-17): every `draft-*` and `write-*` also works from an OPTIONS file or from raw input

## Table of Contents

1. [Scenario](#1-scenario)
2. [Context](#2-context)
3. [Domain Objects](#3-domain-objects)
4. [Functional Requirements](#4-functional-requirements)
5. [Non-Functional Requirements](#5-non-functional-requirements)
6. [Design Decisions](#6-design-decisions)
7. [Implementation Guarantees](#7-implementation-guarantees)
8. [Key Mechanisms](#8-key-mechanisms)
9. [Action Flow](#9-action-flow)
10. [Data Structures](#10-data-structures)
11. [Logging Requirements](#11-logging-requirements)
12. [Technical Constraints](#12-technical-constraints)
13. [Migration Map](#13-migration-map)
14. [Document History](#14-document-history)

## 1. Scenario

**Problem:** IPPS can collect research (`/research`, `/deep-research`) and write one kind of article (`/propose-minto` → `/write-minto`). It cannot code findings, detect patterns, generate and test competing hypotheses, or write reports and ebooks. The third research tier exists only as hand-assembled practice. Research knowledge is spread over 10+ procedural files without GUIDES or CHECKS. The compiled writing libraries (8 techniques, 20 personas) have no installed home. Existing GUIDES list steps without decisions, options, criteria, failure modes, or annotated examples, so output quality varies between runs. Every new capability so far added a new, differently shaped workflow.

**Solution:**
- Three layers, each one skill folder plus thin entry workflows, connected by hand-over artifacts: Layer 1 `research-methods` produces the knowledge library (C1), Layer 2 `analysis-methods` produces validated knowledge (C2), Layer 3 `write-documents` produces the deliverable (C3)
- One execution-depth dial - tier 1 single-turn (one turn, one file), tier 2 planned (one STRUT, one prompt file), tier 3 program (one STRUT, 2-8 prompt files; `/research-program` adds 1-4 approach STRUTs) - applied with the same meaning in every layer, so the same workflow names serve a 2-10 minute, a 10-60 minute, and a 2-20 hour job
- Knowledge lives in GRUC sets, never in workflow bodies: three document-type sets (ARTICLE, REPORT, EBOOK), nine technique sets, twenty persona files, three analysis-stage sets, one research set. Genres (blog, marketing, scientific, business proposal, research results) are document type x technique, not separate template files (DD-41). Every GUIDES file follows the craft blueprint from T04 so that a reader of the GUIDE, TEMPLATE, and EXAMPLE can produce the document without guessing
- Nine single-entry-point writing workflows (`propose-`, `draft-`, `write-` x `article`, `report`, `ebook`) with one command grammar; `/propose-minto` and `/write-minto` are absorbed as `using MINTO`
- Tier 2 and tier 3 writing compiles the relevant GUIDES, RULES, TEMPLATE, technique, and persona content into self-contained prompt sequences via `/write-prompts`, so long documents are produced pass by pass with verification checkpoints

**What we don't want:**
- A fourth concept for depth ("quick analyze", "full pipeline", "mode", "level") beside the tier dial
- Method files, template subfolders, or helper documents that duplicate what a GUIDES decision already states (IN02 `methods/METHOD_*.md` and the eight Layer 2 artifact templates are folded into the stage GUIDES and TEMPLATE files, DD-30)
- Workflow bodies that carry knowledge; a workflow is an entry point, skill reference, MUST-NOT-FORGET, branches, phases, and a quality gate (IPPSWFLW-SP01)
- Agent-chosen techniques or personas, agent-completed partial selections (DD-08), or genre template files that duplicate a document type x technique combination (DD-41)
- A tier-3 program larger than the T04 run; unbounded prompt counts; prompts that touch more than two content files or more than four numbered items
- New script document types (VIDEO-SCRIPT, PODCAST-SCRIPT) in this release; they are the first extension test (DD-33)
- Fading exercises, practice prompts, or pedagogy aimed at human learners inside GUIDES (DD-34)

### Architecture Diagram

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
│ LAYER 1  CLASSIC RESEARCH                         skill: research-methods                         │
│ collect, transcribe, verify, organize      GRUC: RESEARCH_* + research_areas/, research_profiles/ │
│                                                                                                   │
│   tier 1 /research          tier 2 /deep-research         tier 3 /research-program                │
│   one INFO                  T##_ folder, 1 STRUT,         session STRUT, 1-4 approach             │
│                             1 PROMPTS file (3-10)         STRUTs, <= 8 PROMPTS files              │
│   optional: /bundle (llm-tools, IPPSKBNDL-SP01)   support: /transcribe  /fact-check               │
│ out: C1 KNOWLEDGE LIBRARY = Summary + Sources + topic files + _SOURCES/                           │
└────────────────────────────────────────────┬──────────────────────────────────────────────────────┘
                                             v
┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
│ LAYER 2  ANALYSIS AND SYNTHESIS                   skill: analysis-methods (new)                   │
│ detect, hypothesize, validate on ANY input   GRUC: ANALYSIS_*, PATTERN-DETECTION_*,               │
│                                                    HYPOTHESIS_*, VALIDATION_*, INVESTIGATION_*    │
│   /pattern-detect → /hypothesize → /validate      (stage workflows, tier 1 or 2)                  │
│   /analyze   always STRUT first, always ONE INFO                                                  │
│              tier 2: 1 PROMPTS file | tier 3: 3 PROMPTS files + devil's advocate                  │
│   /investigate   behavior unchanged (INVESTIGATE-SP01), step-by-step alternative                  │
│ out: C2 VALIDATED KNOWLEDGE = pattern map + hypothesis register + validation report               │
└────────────────────────────────────────────┬──────────────────────────────────────────────────────┘
                                             v
┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
│ LAYER 3  KNOWLEDGE PACKAGING                      skill: write-documents (composite)              │
│ type, structure, voice, story, cite, release      document_types/ (ARTICLE REPORT EBOOK)          │
│                                                   writing_techniques/  writing_personas/          │
│   document type:  article            report              ebook                                    │
│   /propose-*   →  [ID]-OPTIONS-NN_[Title].md   outline options, scored, one recommended           │
│   /draft-*     →  [ID]-DRAFT-NN_[Title].md     working draft, style sheet, annotations            │
│   /write-*     →  YYYY-MM-DD_[Title].md        output document (+ release check)                  │
│   tiers: article tier 1 | report tier 1-3 | ebook tier 3 (STRUT + PROMPTS, stitch)                │
│   using <WRITING-TECHNIQUE-ID>  MINTO IMINTO ABTSTORY KABOB STA PAS AIDA DIATAXIS IMRAD           │
│   as <persona>                  20 personas (write-* and draft-article only)                      │
│   inline                        edit an existing file in place, never create one                  │
│   delivery: /render  /translate  /ascii-diagram                                                   │
│ out: C3 DELIVERABLE                                                                               │
└───────────────────────────────────────────────────────────────────────────────────────────────────┘

cross-cutting:  /verify (RULES + TEMPLATE)  /critique (GUIDES)  /drift-detect (CHECKS PD)
                /improve (CHECKS QI)  /fact-check  /write-strut  /write-prompts  /cleanup
tier dial:      tier 1 = one turn, one file   tier 2 = STRUT + 1 PROMPTS file   tier 3 = STRUT + 2-8 PROMPTS files
feedback:       Layer 2 open items (low confidence, disconfirmation exhausted) → research questions → Layer 1
                Layer 3 failed release check → revision pass inside Layer 3, never Layer 2
```

## 2. Context

### 2.1 What the research produced and where this SPEC draws the line

- **T01 RSRCHMTHD** (11 INFO files, 59 sources): the method chain S1 Organize → S2 Detect → S3 Hypothesize → S4 Validate → S5 Write, twelve artifacts, likelihood and confidence vocabulary (ICD-203), ACH as audit trail, GRADE and Toulmin weighting. This SPEC keeps the chain and the vocabulary, runs the S1 coding pass as Decision 1 of pattern detection with `/bundle` as optional pre-step (DD-31), and merges the twelve artifacts into three stage output templates (DD-30)
- **T02 WRTSTYLTCH** (41 technique files, 21 persona files, 10 INFO files): the libraries are complete and verified. This SPEC installs them (FR-20..FR-22), renames per DD-20, and resolves the three open style conflicts (DD-32)
- **T04 WRTCRAFT** (11 INFO files, 59 sources): the GRUC content blueprint, ten craft decisions per document type, four edit levels, the consistency layer stack, and the script-format blueprint. This SPEC makes the blueprint binding for every GUIDES, RULES, CHECKS, TEMPLATE, EXAMPLE file created or rewritten (FR-30..FR-35), defers script formats (DD-33), and drops the fading requirement (DD-34)
- **IN01 + IN02**: current state, 16 invariants, three-layer target, ten confirmed decisions. This SPEC refines IN02 Sections 5-7 where they differ (DD-30, DD-31, DD-35, DD-36) and never contradicts a confirmed decision

### 2.2 The three consumption levels map to tiers

The user runs the pipeline at three sizes. The SPEC gives each size one tier value and one example chain; nothing else differs. The document type in each chain is the typical case, not a restriction: any document type runs at any tier that FR-02 allows (a tier 1 report, a tier 2 report draft).

- **Tier 1 - 2 to 10 minutes - article**: `/research` → `/propose-article` → `/write-article`. Every call is one conversation turn producing one file. No STRUT, no PROMPTS, no sub-folders. Optional `using <ID>` `as <persona>`
- **Tier 2 - 10 to 60 minutes - report**: `/deep-research` → `/analyze` → `/propose-report` → `/draft-report` → `/write-report` → `/render`. `/deep-research` and `/analyze` (tier 2, the user's "reduced pipeline") run from one STRUT and one PROMPTS file each; `/analyze` produces one Analysis INFO; `/write-report` runs single-turn or, when the input exceeds the single-turn budget (NFR-03), from one PROMPTS file. Output in one `T##_` research folder plus the session folder
- **Tier 3 - 2 to 20 hours - ebook**: `/research-program` → `/analyze tier 3` → `/propose-ebook` (optionally `compare techniques` with sample bake-off) → `/draft-ebook` → `/write-ebook` → `/render`. The program runs 1-4 approaches, each its own `T##_` folder; `/analyze` (tier 3, the user's "full analyze pipeline") runs the three stages as separate prompt files writing into one Analysis INFO, with a devil's advocate prompt; `/write-ebook` always runs from STRUT + PROMPTS, chapter by chapter, with line and copy passes, chapter summaries as running memory, a book-level consistency pass against the style sheet, stitching, and release check

### 2.3 Tier definition (binding for all layers)

- **Tier 1 - single-turn**: one workflow call = one conversation turn = one output file. Reads: GRUC of the layer, the input file(s). Writes: output file only. No `_agentwork/` artifacts
- **Tier 2 - planned**: one workflow call = `/write-strut` + `/write-prompts` (one PROMPTS file, 3-10 prompts including checkpoints) + headless or in-conversation execution. No human pause inside the file. Writes: one STRUT, one PROMPTS file in `_agentwork/`, 1-9 deliverable files in one folder. One `/verify` + `/fix` checkpoint after each implementation prompt; one full VCRIV (`/verify`, `/critique`, `/reconcile`, `/implement`, `/verify`) at the end
- **Tier 3 - program**: one STRUT, 2-8 PROMPTS files, 10-35 prompts total including checkpoints. `/research-program` adds 1-4 approach STRUTs under the session STRUT and a Preflight prompt file that scores pre-research assumptions before the first content prompt. Human review happens only between PROMPTS files (the user starts the next file); inside a file the run never pauses. Extension by adding phases and prompt files, never by editing executed ones. Full VCRIV at most three times (gates); checkpoints elsewhere. Uses the `guarded` prompt profile (max 4 numbered items, max 2 content files per prompt)
- **Tier selection**: each workflow has a default tier (FR-02). The user overrides a non-fixed default with the keyword `tier 1`, `tier 2`, or `tier 3` anywhere in the call. `plan` or `plan only` stops a tier 2 or 3 call after STRUT and PROMPTS are written
- **Escalation rule**: a tier 2 plan that needs more than 10 prompts becomes a tier 3 plan; a tier 3 plan above NFR-01 is split into several calls. The first response line names the escalation

## 3. Domain Objects

### Layer

A **Layer** is one of three stages of the pipeline with one owning skill and a fixed hand-over artifact to the next layer.

- `layer_1` Classic Research - owner `research-methods` - hands over C1 Knowledge Library
- `layer_2` Analysis and Synthesis - owner `analysis-methods` - hands over C2 Validated Knowledge
- `layer_3` Knowledge Packaging - owner `write-documents` - hands over C3 Deliverable

### Tier

A **Tier** is the execution depth of one workflow call. Values `1`, `2`, `3` as defined in Section 2.3. Stored nowhere; derived per call from the workflow default and the `tier N` keyword.

### Entry Workflow

An **Entry Workflow** is a file in `[PROMPTSYSTEM_FOLDER]/workflows/` that a user invokes by slash command. It follows IPPSWFLW-SP01 anatomy and is thin: it names the skill files to read, the default tier, the command grammar, the branches, and the quality gate. Eighteen entry workflows exist after this SPEC (Section 10.1).

**Key properties:**
- `name` - slash command, kebab-case, verb or verb-noun
- `layer` - 1, 2, or 3
- `default_tier` - 1, 2, or 3; `fixed` when the tier cannot be overridden
- `required_skills` - skill files read before execution
- `grammar` - accepted keywords (Section 8.2)

### GRUC Set

A **GRUC Set** is the group of files `[PREFIX]_GUIDES.md`, `[PREFIX]_RULES.md`, `[PREFIX]_CHECKS.md`, `[PREFIX]_TEMPLATE.md` (plus `[PREFIX]_EXAMPLE_NN-[Title].md` where required) that carries all knowledge for one document type, technique, or analysis stage (GRUC-SP01). Content requirements per file type: Section 4.4.

### Document Type

A **Document Type** is the default GRUC set for a deliverable when no technique is given (DD-08). Values: `article`, `report`, `ebook`. Each owns: edit levels, audience adaptation, release check, file naming, default option count, document-specific craft decisions (FR-21), and the OPTIONS and DRAFT templates.

**Coverage (DD-20):** landing pages are articles; user manuals are ebooks; reference documentation is reports.

**Storage:** `write-documents/document_types/ARTICLE_*.md`, `REPORT_*.md`, `EBOOK_*.md`, `document_types/EXAMPLES/`
**Rule-ID prefixes:** `ART-`, `RPT-`, `EBK-`

### Writing Technique

A **Writing Technique** is a GRUC set that decides macro-structure (section order, evidence progression, closing type) and overrides the document type for structure only when the user passes `using <ID>`. Nine IDs after DD-20: `MINTO`, `IMINTO`, `ABTSTORY`, `KABOB`, `STA`, `PAS`, `AIDA`, `DIATAXIS`, `IMRAD`. A technique GUIDES may overrule the document-type default option count (DD-17).

**Storage:** `write-documents/writing_techniques/[ID]_GUIDES.md`, `[ID]_RULES.md`, `[ID]_CHECKS.md`, `TEMPLATES/[ID]_TEMPLATE.md`, `TEMPLATES/[ID]_OPTIONS_TEMPLATE.md` (where the technique needs its own options form), `EXAMPLES/[ID]_EXAMPLE_NN-[Title].md`
**Rule-ID prefix:** the technique ID (`MINTO-`, `ABTSTORY-`, ...)

### Persona

A **Persona** is one file defining voice through six sliders, 1-3 micro-dosed traits (from the 14-trait catalog), and a Zero-Bullshit baseline (T02 WRTSTYLTCH-IN03). It applies to `write-*` and `draft-article` only when the user passes `as <persona>`. It never changes structure.

**Storage:** `write-documents/writing_personas/[PERSONA].md` (20 files + `README.md`)

### Analysis Stage

An **Analysis Stage** is one of three GRUC sets in `analysis-methods`, named per DD-04: `PATTERN-DETECTION` (codebook, themes, contradictions, gaps), `HYPOTHESIS` (hypothesis register with test plan), `VALIDATION` (weighted evidence, ACH audit trail, disconfirmation log, ranking). `ANALYSIS_*` holds the orchestration of `/analyze` (tier selection, review points, loop-back) and the single-file output template for `/analyze`. `INVESTIGATION_*` (moved, unchanged) serves `/investigate`.

**Rule-ID prefixes:** `ANA-`, `PTD-`, `HYP-`, `VAL-` (`INVESTIGATION_*` keeps its existing IDs)

### Hand-over Artifact

A **Hand-over Artifact** is the fixed output of a layer that the next layer reads without the producing layer present.

- `C1` Knowledge Library: `_INFO_[TOPIC]-IN01_Summary.md` (Summary, Conclusions, Per-Topic Summaries, Limitations, Open Questions, Recommendations) + `_INFO_[TOPIC]-IN02_Sources.md` + topic files + `_SOURCES/`
- `C2` Validated Knowledge: from `/analyze` always one `_INFO_[TOPIC]-IN[NN]_Analysis.md` with sections Pattern Map, Hypothesis Register, Validation Report (DD-04); from the stage workflows one file each (`_PatternMap.md`, `_HypothesisRegister.md`, `_ValidationReport.md`). Every validated item carries a rank on the ranking scale (Section 8.6), a likelihood phrase and a confidence phrase as prose (DD-06), and a disconfirmation log entry
- `C3` Deliverable: `YYYY-MM-DD_[Title].md` with header block (`**Document Type**`, `**Technique**`, `**Persona**`, `**Doc ID**`), plus the release check record in the DRAFT file when one exists, else in the STRUT (tier 2-3) or the chat response (tier 1)

### Working Files

- `[ID]-OPTIONS-NN_[Title].md` - outline options with scoring and one recommendation, output of `/propose-*`. `[ID]` = technique ID when `using` is given, else document type uppercase (`ARTICLE-OPTIONS-01_...`)
- `[ID]-DRAFT-NN_[Title].md` - working draft with style sheet section, chapter summaries (ebook), user annotations, release check record; output of `/draft-*`; optional input of `/write-*`. For ebooks it persists as the series bible across chapter prompts; without a DRAFT the STRUT carries the Style Sheet and Chapter Summaries sections
- `__STRUT_[TOPIC].md`, `_PROMPTS_[NN]-[Topic].md`, `__CARD_*` - scaffolding in `_agentwork/` at tier 2-3; `/cleanup` deletes them after the goal is reached

## 4. Functional Requirements

### 4.1 Cross-cutting

**DRSYNART-FR-01: Tier dial**
- Every entry workflow in Layers 1-3 declares `default_tier` and whether it is `fixed` in its header section
- `tier 1|2|3` keyword overrides a non-fixed default; `plan` or `plan only` stops after STRUT and PROMPTS at tier 2-3; the escalation rule of Section 2.3 applies
- Tier semantics are exactly Section 2.3; a workflow must not define a fourth depth

**DRSYNART-FR-02: Default tiers**
- Layer 1: `/research` tier 1 fixed; `/deep-research` tier 2 fixed; `/research-program` tier 3 fixed; `/bundle` tier 1 fixed
- Layer 2: `/pattern-detect`, `/hypothesize`, `/validate` tier 1 default, tier 2 when the input is a `T##_` research folder; `/analyze` tier 2 default, tier 3 when the input is a research program (2+ `T##_` folders) or `tier 3` is passed; `/analyze` has no tier 1 because DD-04 requires a STRUT first - single-turn analysis is a single stage workflow call
- Layer 3: `/propose-*` and `/draft-*` tier 1 fixed (escalates to tier 2 when `compare techniques` sample bake-off requests full-length samples exceeding the 500-word tier-1 cap); `/write-article` tier 1 fixed; `/write-report` tier 1 default, tier 2 above NFR-03 or when `tier 2` is passed, tier 3 by the escalation rule; `/write-ebook` tier 3 fixed (DD-17: always STRUT + PROMPTS)

**DRSYNART-FR-03: Hand-over contracts**
- Each layer's last workflow writes the hand-over artifact of Section 3 completely; the next layer's first workflow reads only that artifact plus files it names
- All Layer 2 workflows accept any input (DD-04): C1, a single INFO, a folder, a `/bundle` output, PDFs, websites, chat text; `/validate` also accepts bare statements. When the input is not C1 the coding pass runs first (FR-12) and the output header records input provenance
- `/propose-*` accepts C2, C1, any INFO file, or chat text; it never reads `_SOURCES/` raw files

**DRSYNART-FR-04: Command grammar**
- All Layer 3 workflows and `/analyze` accept the grammar of Section 8.2: `<input>`, `using <ID>`, `as <persona>`, `for <audience>`, `tier N`, `plan` / `plan only`, `N options`, `compare techniques`, `inline` (Layer 3 only)
- `inline` (DD-17): the workflow works in an existing file derived from the input, the conversation, or the session, edits it in place, and never creates a new file; with no existing file it stops and names the missing file
- `using` accepts one technique ID per call; multiple IDs are allowed only with `compare techniques` in `/propose-*`
- Unknown technique or persona name: the workflow lists the available names from the library READMEs and stops; it never guesses or picks

**DRSYNART-FR-05: Discovery by filename pattern**
- Technique sets are discovered by `writing_techniques/[ID]_GUIDES.md`; personas by `writing_personas/[PERSONA].md`; document types by `document_types/[TYPE]_GUIDES.md`; analysis stages by `analysis-methods/[STAGE]_GUIDES.md`; research areas and profiles by `research_areas/[AREA]/` and `research_profiles/` files
- Adding a technique, persona, document type, or stage requires no edit to any workflow or SKILL.md routing line, only the new files and a README line

**DRSYNART-FR-06: Review workflows read the matching GRUC set**
- `/verify` detects the GRUC set from the output header (`**Document Type**`, `**Technique**`) or from the `[ID]-OPTIONS-`, `[ID]-DRAFT-` filename, reads the RULES and TEMPLATE of document type and technique, and reads `writing_personas/[PERSONA].md` for persona compliance when `**Persona**` is set
- `/critique` reads the GUIDES of document type and technique; `/drift-detect` reads CHECKS PD; `/improve` reads CHECKS QI of the same sets
- `verify.md`, `critique.md`, `improve.md` lose the hard-coded `MINTO_*` paths and gain the detection rule above

**DRSYNART-FR-07: Tracking discipline**
- Layer 3 workflows never write NOTES, PROBLEMS, PROGRESS, FAILS (invariant 6); Layer 1 and 2 workflows at tier 2-3 append to the session tracking files only through `/session-save`
- Topic folders (`T##_`, `S##_`) carry no own tracking files; cross-references go to the session files

### 4.2 Layer 1 - Classic Research

**DRSYNART-FR-10: research-methods completes its GRUC set**
- New `RESEARCH_GUIDES.md`: purpose and reader outcome; decisions in working order - tier (1, 2, 3 with criteria), scope (FOCUSED, COMPARATIVE, EXPLORATORY), strategy (MEPI vs MCPI as a decision with the criterion "does the reader need the best-evidenced option or the complete set"), domain profile, discovery platforms, source tiers, load unit per prompt, per-dimension topic file structure, Summary synthesis; annotated links to one existing GOOD Summary and one GOOD Sources file; named failure modes (snippet-only sourcing, unregistered source, topic file without GRUC-implications section, summary that restates instead of synthesizes, program extended by editing executed prompts); quality heuristics; self-review questions
- New `RESEARCH_CHECKS.md`: PD items (preflight assumptions scored before content prompts, Google used for URL discovery only, each source registered in `-02` before first citation, `_SOURCES/` retained, verify+fix checkpoint after each implementation prompt); QI items (does the Summary answer every research question with a topic-file reference, does every dimension meet the 5-source minimum, are contradictions resolved or listed as open)
- New `RESEARCH_SOURCES_TEMPLATE.md` for `_INFO_[TOPIC]-IN02_Sources.md` (source ID, tier, access status, SOCAS flags, citing topic files)
- `RESEARCH_STRATEGY_MEPI.md` and `RESEARCH_STRATEGY_MCPI.md` keep only what differs between the strategies; the shared Phase 1-4 text moves to `RESEARCH_GUIDES.md`
- `SKILL.md` keeps the Intent Lookup and points tier questions to `RESEARCH_GUIDES.md`
- Module subfolders per DD-05: `profiles/` becomes `research_profiles/`; `default/`, `legal/`, `market-intel/`, `software/` move under `research_areas/`; `/research` branch paths and `RESEARCH_*` references follow

**DRSYNART-FR-11: Entry workflows**
- `/research` (tier 1): dead reference `research-and-report-writing-rules.md` replaced by `@skills:research-methods RESEARCH_GUIDES.md`; otherwise unchanged
- `/deep-research` (tier 2): rewritten to the full IPPSWFLW-SP01 anatomy - Required Skills, MUST-NOT-FORGET, GLOBAL-RULES, CONTEXT-SPECIFIC branches by strategy (MEPI default, MCPI when completeness is explicit), phases 1-4 with gate list, Output, Quality Gate; body stays under 120 lines because knowledge lives in the skill
- `/research-program` (tier 3, new): phases Preflight (session STRUT with 1-4 approaches, pre-research assumptions A1..An, caps check against NFR-01) → Approach STRUTs and PROMPTS files via `/write-strut` + `/write-prompts` → headless execution with checkpoints → per-approach Summary → program Summary (`_INFO_[TOPIC]-IN01_Summary.md` at session level, Section "Approach Comparison") → VCRIV gate; approaches are `T##_[SUBTOPIC]_[Name]_YYYY-MM-DD/` folders with nested IDs; extension adds a `T##_` folder or a prompt file, never edits executed files
- `/bundle` (tier 1, optional, DD-01, DD-03): thin workflow over `@skills:llm-tools` (and `/transcribe` for PDFs and images) that reads a research folder or source set and writes one bundle in IPPSKBNDL-SP01 format; no step of Layers 2-3 requires it; the bundle decisions (scope, format, what to transcribe) are a section of `RESEARCH_GUIDES.md`

**DRSYNART-FR-12: Coding pass at the start of Layer 2 (S1)**
- `PATTERN-DETECTION_GUIDES.md` Decision 1 is the coding pass: codebook with code ID, definition, inclusion and exclusion rule, example quote; findings list with finding ID, source ID, verbatim or close paraphrase, code(s), verification label
- The pass runs on any input; when the input is C1 or a bundle, finding IDs reuse the Summary's claim references and source IDs reuse `-02` IDs

### 4.3 Layer 2 - Analysis and Synthesis

**DRSYNART-FR-13: analysis-methods skill (new: 13 files; moved: 3 files)**
- New: `SKILL.md` (Intent Lookup, Do NOT Apply When, contracts, rule-ID prefixes), `ANALYSIS_GUIDES.md`, `ANALYSIS_CHECKS.md` (PD and QI items for `/analyze` and all three stages, one section per stage, DD-42), `ANALYSIS_TEMPLATE.md`, and for each stage `PATTERN-DETECTION`, `HYPOTHESIS`, `VALIDATION`: `_GUIDES.md`, `_RULES.md`, `_TEMPLATE.md`
- Moved unchanged from `write-documents` (DD-01: single source for analysis methods): `INVESTIGATION_GUIDES.md`, `INVESTIGATION_LOG_RULES.md`, `INVESTIGATION_LOG_TEMPLATE.md`; `investigate.md` updates its skill paths only
- No `methods/` and no `templates/` subfolder: a method is an option inside a GUIDES decision; an artifact is a section inside the stage TEMPLATE (DD-30)
- `ANALYSIS_GUIDES.md` owns: tier selection (tier 2 vs tier 3), stage sequence, review points (tier 2: none inside the file, the user reviews the finished INFO; tier 3: the user reviews between the three PROMPTS files), loop-back rule (Section 8.6), devil's advocate prompt at tier 3 (attacks the top three items before ranking), and the transfer of the 74 binding terms (RSRCHMTHD-IN03)

**DRSYNART-FR-14: PATTERN-DETECTION stage**
- Decisions in order: coding pass (FR-12) → theme building (Method A affinity clustering, Method B frequency and co-occurrence, Method C contradiction-first; criterion: input size and whether contradictions are already visible) → contradiction register → key assumptions check → gap list
- `PATTERN-DETECTION_TEMPLATE.md` sections: Input Provenance, Codebook, Findings List, Theme Map (theme, member finding IDs, strength, counter-findings), Contradiction Register (pair, both source IDs, resolution or `OPEN`), Key Assumptions, Gaps
- RULES: every theme names at least two finding IDs from two sources; every contradiction cites both sides; no theme without a counter-finding search recorded

**DRSYNART-FR-15: HYPOTHESIS stage**
- Decisions in order: hypothesis form (causal, correlational, categorical, predictive) → generation method (per theme, per contradiction, per gap) → candidate count (3-7 per research question, RSRCHMTHD-IN01) → competing hypothesis for each (at least one rival or the null) → falsification condition → test plan (what evidence, where, what would refute)
- `HYPOTHESIS_TEMPLATE.md` sections: Hypothesis Register (ID `H-NN`, statement, form, source themes, rival `H-NN`, falsifier, prior likelihood phrase, test plan rows)
- RULES: every hypothesis has a rival and a falsifier; likelihood phrases use only ICD-203 terms; no hypothesis restates a theme without a claim

**DRSYNART-FR-16: VALIDATION stage**
- Input: hypotheses from a register or any list of statements (DD-04)
- Decisions in order: evidence search (local material first; local or web research whenever local material does not settle an item, at every tier; tests executed where the item is testable) → evidence weighting (both, not either: GRADE-style certainty per item and a Toulmin warrant per evidence link, RSRCHMTHD-IN01) → ACH matrix as audit trail and search director, never as the decision rule (Dhami 2019) → disconfirmation log → ranking on the scale of Section 8.6 with likelihood and confidence phrases → implications for Layer 3
- `VALIDATION_TEMPLATE.md` sections: Items, Evidence Weights (GRADE certainty, Toulmin warrants), ACH Matrix (audit trail), Disconfirmation Log (per item: what was searched, where, what was found, exhausted yes/no), Ranking, Research Questions for Layer 1, Writing Implications
- RULES: every rank above `refuted` requires at least one recorded disconfirmation attempt; `refuted` requires the refuting evidence ID; `proven` requires `[PROVEN]` or `[TESTED]` evidence; confidence is stated separately from likelihood; no two items share a rank position (ties are broken by confidence, then by evidence weight, and the tie-break is recorded)

**DRSYNART-FR-17: Entry workflows**
- `/pattern-detect`, `/hypothesize`, `/validate`: stage workflows, each reads its stage GRUC; output one `_INFO_[TOPIC]-IN[NN]_[PatternMap|HypothesisRegister|ValidationReport].md`; each accepts the previous stage's output or any input
- `/analyze` (DD-04): writes a STRUT first, then executes it unless called with `plan` or `plan only`; always produces one `_INFO_[TOPIC]-IN[NN]_Analysis.md` from `ANALYSIS_TEMPLATE.md`. Tier 2 reduced: one PROMPTS file (3-10 prompts: pattern detection, hypotheses, validation, checkpoints, VCRIV). Tier 3 full: three PROMPTS files (one per stage) writing into the same INFO, plus devil's advocate prompt and a full VCRIV gate
- `/investigate`: behavior unchanged; listed in `analysis-methods/SKILL.md` Intent Lookup as the step-by-step alternative with append-only log
- Output location: tier 1 beside the input or in the session root; tier 2-3 in `S##_[SUBTOPIC]_Analysis_YYYY-MM-DD/` under the session with nested IDs

### 4.4 Layer 3 - Knowledge Packaging

**DRSYNART-FR-20: write-documents becomes a composite skill**
- `SKILL.md` is router-only (SK-AR-01): routing table (one line per goal), shared rules, quick commands; function-specific procedures live in the GRUC files
- Three function subfolders share the root infrastructure (SK-AR-07, DD-01, DD-05): `document_types/`, `writing_techniques/`, `writing_personas/`; the existing planning and system GRUC sets (SPEC, IMPL, PROMPTS, INFO, ...) stay at root
- Function documents carry no YAML frontmatter (SK-AR-02); one README per function subfolder is its index
- Root files are not moved by this SPEC except the four MINTO files (FR-22) and the three `INVESTIGATION_*` files (FR-13)

**DRSYNART-FR-21: Document-type GRUC sets (12 files)**
- In `document_types/`, for each of `ARTICLE`, `REPORT`, `EBOOK`: `_GUIDES.md`, `_RULES.md`, `_CHECKS.md`, `_TEMPLATE.md` (12). `[TYPE]_TEMPLATE.md` holds three labeled sections: `OPTIONS` (skeleton of the OPTIONS file), `DRAFT` (skeleton of the DRAFT file), `Output` (skeleton of the output document) (DD-42). Document-type coverage per DD-20 is stated in the `write-documents/SKILL.md` routing table
- Document-type EXAMPLE files are deferred (DD-42); each document-type GUIDES links annotated technique EXAMPLES instead (article: ABTSTORY, KABOB; report: MINTO, IMRAD; ebook: STA, DIATAXIS)
- Each GUIDES carries the ten craft decisions of its type from WRTCRAFT-IN01 Section 2 (article: theme statement, reporting strategy, structure test, lead type, nut graf, section order, ending type, revision passes, quote management, unity check; report: governing thought, key-line claims, action titles, exhibit format, executive summary contents, appendix vs body, recommendation wording, report convention, summary stand-alone test, navigation; ebook: promise, reader, chapter sequence from reader path, chapter pattern, advance organizer, TOC as argument, introduction contract, front and back matter, cross-reference system, beta-read test) plus the type-owned decisions: edit levels that apply, audience adaptation (`for <audience>`), default option count and options scoring, storytelling pass (lead, embedded case, ending - applied without a technique so that untechniqued output still reads as a story), release check (Section 8.5), output naming
- Each RULES carries structural requirements, BAD/GOOD pairs per named failure mode of the GUIDES, completeness, cross-reference integrity, terminology consistency, recap format, release check record format; the `DRAFT` section of `[TYPE]_TEMPLATE.md` contains the Style Sheet section (terminology, numbers, tone decisions, cross-reference format) that the copy pass applies
- The `DRAFT` sections of `REPORT_TEMPLATE.md` and `EBOOK_TEMPLATE.md` contain, per DD-17, the skeleton with all chapters, per-chapter instructions on what to fill in where, and diagram placeholders; `EBOOK_TEMPLATE.md` `DRAFT` adds a Chapter Summaries section (one 3-5 sentence summary per written chapter: what was established, terms introduced, open threads) that every chapter prompt reads and extends - the running memory against long-form drift
- The ebook set additionally owns: chapter file convention, book-level consistency pass against the style sheet, stitching order (front matter, chapters, back matter), and the sample bake-off decision for `compare techniques`

**DRSYNART-FR-22: Technique and persona libraries installed**
- `writing_techniques/`: `README.md` (one line per ID: ID, one-sentence fit, document types it serves; plus the "when to use which" matrix of DD-09 including the genre map of DD-41), 9 x (`[ID]_GUIDES.md`, `[ID]_RULES.md`, `[ID]_CHECKS.md`), `TEMPLATES/[ID]_TEMPLATE.md`, `TEMPLATES/[ID]_OPTIONS_TEMPLATE.md` where present, `EXAMPLES/[ID]_EXAMPLE_NN-[Title].md`
- OPTIONS-form criterion (DRSYNART-DD-44): a technique owns an OPTIONS template only where its planning artifact is not a section outline; today: MINTO (exports its AMINTON Q/A tree; all other techniques export their Section Inventory wrapped by the document-type OPTIONS template)
- IDs and file stems after DD-20: `MINTO`, `IMINTO`, `ABTSTORY`, `KABOB`, `STA`, `PAS`, `AIDA`, `DIATAXIS`, `IMRAD`; rule-ID prefixes equal the ID; `PAS-AIDA-CONVERSION` splits into two full sets `PAS` and `AIDA` (DD-20)
- Root `MINTO_GUIDES.md`, `MINTO_RULES.md`, `MINTO_TEMPLATE.md`, `MINTO-DRAFT_TEMPLATE.md` merge with the T02 `SCQA-PYRAMID_*` set into `writing_techniques/MINTO_*` and `TEMPLATES/MINTO_OPTIONS_TEMPLATE.md` (DD-19); Release 1: root MINTO files are the base, SCQA-PYRAMID contributes CHECKS and EXAMPLE; the FR-30 rewrite closing the four MINTO gaps named in WRTCRAFT-IN08 is Release 2 (DD-42)
- `writing_personas/`: `README.md` (one line per persona: name, one-sentence voice, fits document types) and 20 persona files from T02 with DD-07 ("audience" not "listener") applied; DD-32 edits follow after user confirmation (DD-42)
- Every `-DRAFT` term in library files is renamed to `-OPTIONS` (DD-16)

**DRSYNART-FR-23: Nine writing workflows**
- `propose-article.md`, `draft-article.md`, `write-article.md`, `propose-report.md`, `draft-report.md`, `write-report.md`, `propose-ebook.md`, `draft-ebook.md`, `write-ebook.md`
- Each is a thin entry: Required Skills (`[TYPE]_GUIDES.md`, `[TYPE]_RULES.md`, the matching section of `[TYPE]_TEMPLATE.md`; technique and persona files only when passed), MUST-NOT-FORGET (DD-08, invariant 6, header fields), default tier, grammar, branches `with technique` / `without technique` / `with persona`, phases, Output, Quality Gate; body under 100 lines
- `/propose-*`: reads input, applies Decision 1-3 of the type (theme or governing thought or promise; structure test; options scoring from GUIDES), writes `[ID]-OPTIONS-NN_[Title].md` with `N options` (default from the document-type GUIDES, overruled by the technique GUIDES when `using` is given; DD-17) scored against the GUIDES criteria and one recommendation; `compare techniques` with 2-4 IDs produces one option per ID; at ebook or report scale `compare techniques` adds a sample bake-off: one sample section per option written to the OPTIONS file, scored with the options-scoring criteria and quality heuristics of the document-type GUIDES and the AI-writing detection rules (never with CHECKS, FR-32), result recorded under each option
- `/draft-*`: reads an OPTIONS file and the user's choice, or raw input (DD-17), expands it into `[ID]-DRAFT-NN_[Title].md` with all headings, per-section job and hand-off, evidence placement with citations, Style Sheet section, open questions for the user; report and ebook drafts add per-chapter fill-in instructions and diagram placeholders; `/draft-article` is optional in the chain (tier 1 chain skips it); `as <persona>` is honoured in `draft-article` only
- `/write-*`: reads a DRAFT, an OPTIONS file plus choice, or raw input (DD-17), writes `YYYY-MM-DD_[Title].md` with the header block, applies persona, runs the type's revision passes (developmental via the draft; line and copy in the same turn at tier 1; as separate prompts at tier 2-3), runs the release check and records it, reports the artifact path; tier 2-3 produce STRUT + PROMPTS via `/write-strut` and `/write-prompts` with the compile rule of Section 8.3; without a DRAFT the STRUT carries the Style Sheet (and for ebooks the Chapter Summaries)
- `/write-ebook` (tier 3): one prompt per 1-2 chapters writing `_agentwork/ch-NN_[Chapter].md` and its Chapter Summary; a checkpoint prompt by a different prompt after each chapter prompt; copy pass per 2-4 chapters against the style sheet; book consistency prompt; stitching prompt assembling the output file; `/fact-check` prompt; release check prompt; VCRIV gate. Books that exceed NFR-01 are written as parts (one call per part, shared DRAFT)
- `propose-minto.md` and `write-minto.md` are deleted; `README.md` and the installed `writing_techniques/README.md` state `using MINTO` as the replacement (DD-19)

**DRSYNART-FR-24: Header fields and naming of Layer 3 files**
- Output header block: `**Doc ID**: [TOPIC]-[ARTICLE|REPORT|EBOOK]-[NN]`, `**Document Type**: article|report|ebook`, `**Technique**: [ID]|none`, `**Persona**: [PERSONA]|none`, `**Audience**: [free text]|general`, `**Source**: [DRAFT or OPTIONS path, or input path]`
- OPTIONS and DRAFT files are deliverables in the working folder (session root or the `S##_`/`T##_` folder the user is in; without a session, the working folder is the folder of the input file, else the workspace root), never in `_agentwork/`; `/cleanup ... for publishing` leaves them in place
- One `[NN]` sequence per `[ID]` per working folder for OPTIONS and DRAFT; the output file carries no sequence number in its name

### 4.5 GRUC content standard for every file this SPEC creates or rewrites

**DRSYNART-FR-30: GUIDES content (blueprint WRTCRAFT-IN08 Section 2.1 and 4)**
- Sections in order: Purpose and Reader Outcome (capability statement); Decisions in working order, each with Question, Options, Criterion, source reference; annotated excerpts placed inside the decision where it is hard to see in prose (at least two per document-type GUIDE); Named Failure Modes with strategic guidance and the RULES ID holding the BAD/GOOD pair; Quality Heuristics as observable properties; Self-Review Questions (numbered, each answerable from the output, each citing a RULES ID); Annotated Exemplar Links with "What makes this work"; RULES References by ID range without rule text
- Document-type GUIDES add: Edit Levels that apply (article: line, copy, proof; report: developmental, line, copy, fact-check, proof; ebook: all), Clarity Principles the line pass applies (Paramedic Method, characters-and-actions, classic style), Fact-Checking Standard (line by line, by a prompt that did not write the text, before release), Recap Convention (capability statement, not content summary)
- Forbidden: restated rule text, audit items, CHECKS content, step lists without a criterion, abstract adjectives as criteria, fading exercises (DD-34)
- Acceptance test per GUIDES: a reader with the GUIDE, TEMPLATE, and EXAMPLE and no other file can produce the document; the IMPL proves this once per document type with one complete run

**DRSYNART-FR-31: RULES content (Section 2.2)**
- Structural requirements; one BAD/GOOD pair per named failure mode of the GUIDES showing the same content arranged differently; completeness checks verifiable from the artifact alone; cross-reference integrity; terminology consistency; recap format; release check record format
- Rule IDs `[PREFIX]-[GROUP]-NN` registered in `ID-REGISTRY.md` before first use; groups per set are listed in the set's RULES header

**DRSYNART-FR-32: CHECKS content (Sections 2.3, 2.4)**
- PD items name an action and the evidence that proves it happened (planning artifact drafted before prose, revision passes run, option scoring recorded, style sheet created before the copy pass, fact-check run by a separate prompt, review points recorded)
- QI items are quality questions with an improvement tip, judgment-based, never structural duplicates of RULES
- CHECKS are never loaded by `/propose-*`, `/draft-*`, `/write-*`, `/analyze`, or any prompt file they generate (GRUC-IG-03)

**DRSYNART-FR-33: TEMPLATE content (Section 2.5)**
- Skeleton with placeholders and XML-comment annotations only; planning fields before any section (theme or governing thought or promise), structure fields, ending fields, revision and status fields, style fields; no rules, no guidance, no audit items
- Labeled lines, never Markdown tables, for repeating units (chapters, options, sections) - core-conventions no-tables rule; independent of the pending WRTCRAFT-DD-24

**DRSYNART-FR-34: EXAMPLE content (Section 2.6)**
- Complete GOOD documents, one per technique at minimum (one per document type deferred, DD-42); no BAD examples; the annotation lives in the GUIDES link, not in the EXAMPLE
- Generic data only (Pre-Write Privacy Gate): fictional organisations, placeholder numbers, no real persons

**DRSYNART-FR-35: Consistency layer stack**
- Decisions are owned by exactly one layer (WRTCRAFT-IN08 Section 6.1): house style (`rules/core-conventions.md`, `MECT_WRITING_RULES.md`, `APAPALAN_RULES.md`), document-type set, technique set, persona file, per-document style sheet (DRAFT section), edit passes
- A lower layer adds where a higher layer is silent and never contradicts it; the technique set overrides the document type for structure only; the persona never overrides house style; the style sheet never waives a RULES item
- **Fusion Contract (DRSYNART-DD-44)**: When a document type is combined with a technique (`using <ID>`), the technique implements the document type's slot interface. Type templates declare two mechanical slots per stage (`FRAME` owned by document type; `SECTIONS` filled by technique). Each technique template exports an ordered Section Inventory and an Output body fragment. Fusion is substitution, not judgment: in OPTIONS and DRAFT, each inventory row is wrapped with the five DD-43 outline fields (`Goal`, `Content`, `Evidence`, `Reason`, `Handoff`); in Output, the body fragment is inserted into the frame. Fusion materializes once in the instantiated OPTIONS/DRAFT file; downstream workflows consult only that file, never both templates again.

## 5. Non-Functional Requirements

**DRSYNART-NFR-01: Scalability - tier 3 caps (the T04 run is the maximum)**
- Per tier-3 call (`/research-program`, `/analyze tier 3`, `/write-ebook`, escalated `/write-report`): at most 8 prompt files, 35 prompts counting every prompt including checkpoints, 12 INFO or output deliverables, 3 full VCRIV gates; `/research-program` additionally at most 4 approaches (`T##_` folders)
- Per prompt: at most 4 numbered items, 2 content files changed, 2 topic files loaded (the `guarded` profile)
- Verification: the planning step counts planned prompts and files and refuses to start above the cap; the user splits the job into several calls (research programs by approach, ebooks by part)

**DRSYNART-NFR-02: Performance - wall-clock envelopes**
- Tier 1 chain (research → propose → write) completes in 2-10 minutes of agent time; each call is one turn
- Tier 2 chain completes in 10-60 minutes; each `/deep-research` or `/analyze` call runs 3-10 prompts
- Tier 3 chain completes in 2-20 hours of headless time; the Preflight STRUT states the HWH estimate from `MODEL_INVENTORY.md` workload factors
- Verification: STRUT effort estimate recorded before execution; actual time recorded in the Summary's research stats line

**DRSYNART-NFR-03: Scalability - single-turn writing budget**
- `/write-report` runs at tier 1 when the input has at most 6 top-level sections and a target of at most 5,000 words; above that it runs at tier 2, and at tier 3 when the tier 2 plan exceeds 10 prompts
- `/write-ebook` always runs at tier 3
- Verification: the workflow states the detected tier and the reason in its first response line

**DRSYNART-NFR-04: Usability - thin workflows**
- Entry workflow bodies: Layer 3 under 100 lines, `/deep-research` and `/analyze` under 120 lines, `/research-program` under 150 lines; everything longer belongs in a skill file
- Verification: line count in `/verify` against IPPSWFLW-SP01

**DRSYNART-NFR-05: Reliability - prompt-file execution**
- Every tier 2-3 implementation prompt is followed by a separate `/verify` + `/fix` checkpoint prompt; verification never runs inside the prompt that produced the text (cross-verification reduces cascading errors, self-checking in the same step does not); a prompt that fails three times stops the file and records the failure in session PROBLEMS.md
- Prompt files load at most 2 topic files and reference GRUC files by path, never by pasted copy, except the compiled subset of Section 8.3

**DRSYNART-NFR-06: Compliance - privacy and encoding**
- EXAMPLE files, GUIDES excerpts, and TEMPLATE placeholders contain generic data only; UTF-8 throughout; ASCII quotes in system files

**DRSYNART-NFR-07: Instruction working set budget (DRSYNART-DD-47)**
- Per-call instruction working set <= 15k tokens, measured once per type x technique x persona worst case
- RULES files are excluded from the writing execution load path (`propose-*`, `draft-*`, `write-*`) and reserved for `/verify`

## 6. Design Decisions

Decisions DD-01..DD-09 and DD-15..DD-20 were made by the user before this SPEC (NOTES.md Key Decisions). They are restated in one line each so the SPEC is self-contained; NOTES.md wording is authoritative. DD-21..DD-24 are the WRTCRAFT script-format decisions, still pending. New decisions made by this SPEC start at DD-30 to avoid collision with the parked T03 numbers. DD-30..DD-41 are agent-proposed under the instruction "decide in favour of simplicity"; they are not user-confirmed until the user replies (reply format: `DD-32 ok, DD-33 ok, ...` or an alternative per ID).

**DRSYNART-DD-01 [CONFIRMED] - Skill folders per layer:** `write-documents` becomes a composite skill with Layer 3 assets as function subfolders (not a new skill); `research-methods` is the single source for research methods and workflows (`research`, `deep-research`, `research-program`); `analysis-methods` is the single source for analysis methods and workflows (`investigate`, `analyze`, `pattern-detect`, `hypothesize`, `validate`); `/bundle` uses `llm-tools`, is optional, and Summaries must be useful without it. Applied in FR-11, FR-13, FR-20.

**DRSYNART-DD-02 [CONFIRMED] - Tier 3 form:** new workflow `/research-program`. Applied in FR-11.

**DRSYNART-DD-03 [CONFIRMED] - S1 bundle placement:** standalone, optional `/bundle` workflow in Layer 1 using `llm-tools`. Applied in FR-11, DD-31.

**DRSYNART-DD-04 [CONFIRMED] - Layer 2 entry:** generic workflows on any input material: `/pattern-detect` (structured INFO, GRUC set `PATTERN-DETECTION_*`), `/hypothesize` (hypothesis register), `/validate` (ranks statements or hypotheses from proven to refuted with comparable scores, searches evidence and counter-evidence, runs tests, uses local or web research when material is not enough), `/analyze` (STRUT first, executes unless `plan` / `plan only`, one INFO containing everything), `/investigate` (existing step-by-step alternative). Applied in FR-03, FR-13..FR-17.

**DRSYNART-DD-05 [CONFIRMED] - Module subfolders:** every collection of interchangeable parts gets a subfolder: `writing_personas/`, `writing_techniques/`, `research_profiles/`, `research_areas/`. Applied in FR-10, FR-20; `document_types/` follows the same rule.

**DRSYNART-DD-06 [CONFIRMED] - Likelihood and confidence:** two prose phrases, no new bracket labels, as output of `/analyze` and `/validate`. Applied in Section 8.6.

**DRSYNART-DD-07 [CONFIRMED]:** "audience" replaces "listener".

**DRSYNART-DD-08 (user decision) - User-only selection:** only the user chooses `<persona>` and `<technique>`; without them the agent follows the standard workflow, templates, and GRUC files; partial input is never completed; the agent suggests from the libraries only when the user asks for help with style or technique.

**DRSYNART-DD-09 (user decision) - T02 library structure:** `WRITING_PERSONAS/` one file per persona (6 sliders, 1-3 micro-dosed traits) plus `README.md` with catalog and "when to use which" matrix; `WRITING_TECHNIQUES/` 3 GRUC files per technique plus `README.md`, `TEMPLATES/`, `EXAMPLES/`. Installed as `writing_personas/` and `writing_techniques/` (DD-05, DD-18).

**DRSYNART-DD-15..DD-20 (user decisions; DD-18..DD-20 [CONFIRMED]):** **DD-15** technique IDs: uppercase letters only, max 10 characters; file names and rule-ID prefixes follow the ID. **DD-16** files `[ID]-OPTIONS-NN_`, `[ID]-DRAFT-NN_`, `YYYY-MM-DD_[Title].md`; today's MINTO DRAFT becomes OPTIONS. **DD-17** nine single-entry-point workflows; OPTIONS and DRAFT optional; option count from document-type GUIDES, overruled by technique GUIDES; `inline` keyword in all nine; persona only in `draft-article` and `write-*`; `/write-ebook` writes STRUT and PROMPTS and executes unless `plan` / `plan only`; INFO, SPEC, IMPL, TEST, TASKS untouched. **DD-18** libraries in `write-documents` subfolders. **DD-19** `/propose-minto` and `/write-minto` integrated into the nine workflows. **DD-20** one full file set per technique; `SCQA-PYRAMID` → `MINTO`, `INVERTED-PYRAMID` → `IMINTO`; adds `KABOB`, `STA`, `IMRAD`; `PAS` and `AIDA` as two full sets; landing pages are articles, user manuals are ebooks, reference documentation is reports.

**DRSYNART-WRTCRAFT-DD-21..24 [PENDING USER DECISION]:** document types vs techniques for VIDEO-SCRIPT and PODCAST-SCRIPT, sub-types vs techniques for their variants, labeled lines vs tables in script TEMPLATES (WRTCRAFT-IN11 Section 8.4). This SPEC does not decide them; DD-33 defers the build, and FR-33 already uses labeled lines for all new TEMPLATES independently of DD-24.

**DRSYNART-DD-30: No method files, no template subfolders in `analysis-methods`.** The eight artifact templates and three method files proposed in IN02 Section 6 are folded into three stage TEMPLATE files (artifacts as sections) and three stage GUIDES (methods as options with criteria). Rationale: a method is a GUIDES option by definition (FR-30); separate files would restate the decision and double the read cost per prompt. 16 files instead of about 30.

**DRSYNART-DD-31: `/bundle` is a format converter; coding belongs to Layer 2.** `/bundle` (DD-03) collects, transcribes, and packages sources into one IPPSKBNDL-SP01 bundle; it does not code findings. The S1 coding pass is Decision 1 of `PATTERN-DETECTION_GUIDES.md` (FR-12) and runs on a bundle, on C1, or on raw input. Rationale: Layer 2 must work on any input (DD-04), so it codes its input anyway; coding in `/bundle` too would run the same pass twice.

**DRSYNART-DD-32: The three persona style conflicts (`DRSYNART-WRTSTYLTCH-PR-0004`) are resolved in favour of the stricter rule.** Recap: Zero-Bullshit gate wins; Density low means frequent signposting, never recap paragraphs; the T04 recap convention (capability statement) applies only where the document type requires a recap (ebook chapter end). Rhythm: the numeric 5-9 / 18-28 word alternation is removed; the rule becomes "vary sentence length within every paragraph; no paragraph of uniform length". Humor: the micro-dose budget wins; "in every paragraph" is removed; humor appears at most once per section and never in the BUT, governing thought, or recommendation sentences. Rationale: fewer numeric rules, no contradiction between house style and persona, `/verify` can check the remaining rules from the artifact.

**DRSYNART-DD-33: VIDEO-SCRIPT and PODCAST-SCRIPT are deferred to a follow-up SPEC and serve as the first extension test.** Rationale: scope control; the deliverable of this SPEC is article, report, ebook. The extension must succeed under FR-05 (one GRUC set + 3 thin workflows + README lines, zero edits to existing workflows). If it does not, FR-05 is wrong and must be fixed before scripts are added.

**DRSYNART-DD-34: No fading structure in GUIDES.** The WRTCRAFT blueprint criterion 10 (complete example, partial exercise, independent prompt) is dropped. Rationale: the reader is an LLM executing a task, not a learner practising; worked EXAMPLE plus annotated link is the model-study mechanism that transfers (WRTCRAFT-IN07, WRTCRAFT-IN08 Section 8.9). Closes open question F-24.

**DRSYNART-DD-35: One tier dial for all layers, selected by workflow default plus the `tier N` keyword.** Rationale: the user runs three sizes of job; the only thing that changes between them is planning depth and prompt count. Naming the depth once ("tier") and defining it once (Section 2.3) removes "quick", "full", "reduced", "mode", and "level" from all files; the user's "reduced" and "full" analyze pipelines are `/analyze` tier 2 and tier 3.

**DRSYNART-DD-36: OPTIONS and DRAFT are deliverables, not scaffolding.** When they exist (they stay optional, DD-17), they stay in the working folder, carry user annotations, and the ebook DRAFT persists as series bible, style sheet, and chapter-summary memory. Rationale: the user edits them between steps; `_agentwork/` is deleted by `/cleanup`.

**DRSYNART-DD-37: Output Doc ID form `[TOPIC]-[ARTICLE|REPORT|EBOOK]-[NN]`.** Rationale: keeps the precedent of `[TOPIC]-MINTO-[NN]` without adding document-type codes to `promptsystem-ids.md`; the technique is a header field, so two techniques on one topic share one sequence.

**DRSYNART-DD-38: Polishing, proof-reading, and stitching are phases of `/write-*`, not workflows.** Line and copy passes, fact-check, release check, and (ebook) stitching are decisions and phases in the document-type GUIDES and prompts in the generated PROMPTS file. `/improve` (CHECKS QI) and `/verify` (RULES, incl. proof-level rules) remain the post-release review entry points. Rationale: no new verbs; the edit-level sequence is craft knowledge and belongs in the GUIDES.

**DRSYNART-DD-39: Sample bake-off only under `compare techniques`.** `/propose-report` and `/propose-ebook` write one sample section per candidate technique and score them when the user lists 2-4 techniques. Rationale: the user asked for "trying out different writing approaches and choosing the most optimal" at tier 3; keeping it behind an explicit keyword preserves DD-08 and keeps the default `/propose-*` to one turn.

**DRSYNART-DD-40: Delivery in four increments, each shippable.** A) Layer 3 (document-type sets, libraries, nine workflows, review repointing, MINTO retirement) - usable on existing Summaries at once; B) Layer 1 (RESEARCH_GUIDES, CHECKS, Sources template, `research_areas/` and `research_profiles/` renames, `/deep-research` body, `/research-program`, `/bundle`); C) Layer 2 (`analysis-methods`, `INVESTIGATION_*` move, four new workflows, `investigate.md` paths); D) registration, README, rules, sync. Rationale: A yields the deliverable the user needs first; B and C are independent of each other.


**DRSYNART-DD-41: Genres are document type x technique, not template files.** The initial request's template types map as: blog post → article (optionally `ABTSTORY` or `KABOB`); marketing and landing page → article `using PAS` or `AIDA`; scientific paper and research results → report `using IMRAD`; business proposal → report `using MINTO`; news-style briefing → article `using IMINTO`; tutorial and user manual → ebook `using DIATAXIS` or `STA`; reference documentation → report `using DIATAXIS`. The map lives in `writing_techniques/README.md` ("when to use which", DD-09) and is shown only when the user asks for help (DD-08); each technique ships its own TEMPLATE, so templates stay extensible by adding a technique. Rationale: a genre template would duplicate a document-type set plus a technique set and drift from both.

**DRSYNART-DD-42: Release 1 scope - production-ready core, deferred extras.** Release 1 implements every FR except the items below, and consolidates two file groups. Consolidated: document-type sets use 4 files with a three-section TEMPLATE (FR-21); analysis stage CHECKS live in one `ANALYSIS_CHECKS.md` (FR-13). Deferred to Release 2: `/deep-research` body rewrite and the MEPI/MCPI text deduplication (FR-11, FR-10 bullet 4; the current stub keeps working), `RESEARCH_CHECKS.md` and `RESEARCH_SOURCES_TEMPLATE.md` (FR-10), the FR-30 rewrite of technique GUIDES other than the fixes needed for renamed IDs (T02 GUIDES are verified), the merge of `SCQA-PYRAMID` GUIDES and RULES content into `MINTO` beyond CHECKS and EXAMPLE (root MINTO is the base), document-type EXAMPLE files (FR-21, FR-34), the persona edits of DD-32 (pending user confirmation), acceptance runs for report and ebook (IG-09 runs for article only), the IG-10 dry run, `docs/_INFO_GRUC_GUIDES_RULES_CHECKS.md` inventory update. Rationale: the full SPEC is about 11 AWH; Release 1 delivers all 18 workflows and all three layers at about 2.7 AWH; every deferred item is additive and needs no rework of Release 1 files.

**DRSYNART-DD-50 [CONFIRMED] - `AI_WRITING_RULES.md` for publishing document types only:** `[PROMPTSYSTEM_FOLDER]/skills/write-documents/AI_WRITING_RULES.md` defines enforceable anti-AI writing rules (`AW-SO-*`, `AW-SY-*`, `AW-ST-*`, `AW-VO-*`, `AW-LX-*`) with BAD/GOOD pairs, scoped strictly to publishing document types (`article`, `report`, `ebook` — never SPECs or internal documents). Loaded BEFORE writing by `draft-*`, `write-*`, and `document_types/[TYPE]_GUIDES.md`, and enforced AFTER writing by `/verify` (Authored Documents), `/critique` (Writing Documents), and `/improve` (Authored Documents + `*_CHECKS.md` QI items). Text length and pacing are owned by the writing persona (`writing_personas/*.md`), removing the hardcoded `5-9 / 18-28` sentence alternation.

## 7. Implementation Guarantees

**DRSYNART-IG-01:** No workflow body contains craft knowledge, scoring criteria, option lists, or rule text; every such item is in a GRUC file the workflow names.

**DRSYNART-IG-02:** A workflow with neither `using` nor `as` loads no file from `writing_techniques/` or `writing_personas/`.

**DRSYNART-IG-03:** `/verify`, `/critique`, `/drift-detect`, `/improve` detect the GRUC set from the artifact (header fields or filename) and never from a hard-coded path.

**DRSYNART-IG-04:** Every GUIDES, RULES, CHECKS, TEMPLATE, EXAMPLE file created or rewritten passes FR-30..FR-34; `/verify` with `write-documents` meta rules (GUIDES/RULES/CHECKS/TEMPLATE rules) reports zero violations before sync.

**DRSYNART-IG-05:** Every tier 2-3 run produces its STRUT before its first prompt file and its first prompt file before its first content change; executed prompt files are never edited.

**DRSYNART-IG-06:** A tier 3 call that would exceed NFR-01 does not start; the planning response names the cap and the split.

**DRSYNART-IG-07:** Every rule-ID prefix (`ART-`, `RPT-`, `EBK-`, `ANA-`, `PTD-`, `HYP-`, `VAL-`, nine technique IDs) is registered in `ID-REGISTRY.md` before the first file using it is synced to `[AGENT_FOLDER]`.

**DRSYNART-IG-08:** `/propose-minto` and `/write-minto` are removed in the same release that installs `using MINTO`; `README.md` names the replacement.

**DRSYNART-IG-09:** The acceptance run of FR-30 (one document per type produced from GUIDE, TEMPLATE, EXAMPLE alone) is recorded in the IMPL with artifact paths before Layer 3 is declared done.

**DRSYNART-IG-10:** Adding a tenth technique or a twenty-first persona requires exactly: the new files plus one README line. The IMPL verifies this with a dry run.

**DRSYNART-IG-11:** Every confirmed decision (DD-01..DD-07, DD-15..DD-20) is traceable to at least one FR, mechanism, or migration row; the IMPL lists the mapping and flags any decision without one.

## 8. Key Mechanisms

### 8.1 Tier resolution

```
call arrives
├─> workflow header: default_tier, fixed?
├─> keyword `tier N` present and not fixed → tier = N
├─> else input shape (FR-02): stage workflows: one file or text → 1 | T##_ folder → 2;  /analyze: one set → 2 | 2+ T##_ sets → 3
├─> else size rule (NFR-03) for /write-report
├─> escalation: tier 2 plan > 10 prompts → tier 3; tier 3 plan > NFR-01 → split, refuse to start
└─> first response line: "Tier N - [reason]"
    ├─> tier 1: execute in this turn, write one file
    ├─> tier 2: /write-strut → /write-prompts (1 file) → [plan | plan only? stop] → execute without pause → VCRIV
    └─> tier 3: plan (caps NFR-01; research-program: Preflight, assumptions, approach STRUTs) → /write-prompts (2-8 files)
             → [plan | plan only? stop] → execute file by file, user review between files → gates
```

### 8.2 Command grammar (Layer 3 and `/analyze`)

```
/<verb>-<type> <input> [using <ID>] [as <PERSONA>] [for <audience>] [tier N] [plan | plan only] [N options] [compare techniques <ID>, <ID>[, <ID>[, <ID>]]] [inline]
```

- `<input>`: file path, folder path, Doc ID, or free text; `/draft-*` and `/write-*` default to the newest DRAFT, else the newest OPTIONS in the working folder when omitted, else ask for input; OPTIONS and DRAFT are never required (DD-17)
- `inline`: work in the existing file (from input, conversation, or session) and edit it in place; never create a file (DD-17)
- `using <ID>`: exactly one of the nine IDs; absent means document-type defaults
- `as <PERSONA>`: one persona file stem; honoured by `/write-*` and `/draft-article`; ignored with a notice elsewhere
- `for <audience>`: free text passed to the audience-adaptation decision of the type GUIDES; absent means `general`
- `N options`: 2-5; default from the document-type GUIDES, overruled by the technique GUIDES (DD-17); `/propose-*` only
- `compare techniques`: 2-4 IDs; `/propose-*` only; produces one option per ID and the sample bake-off (DD-39) for report and ebook
- Examples: `/propose-article _INFO_TOPIC-IN01_Summary.md using ABTSTORY` · `/write-report for finance leads tier 2` · `/propose-ebook compare techniques MINTO, STA, DIATAXIS` · `/analyze T02_* tier 3 plan only`

### 8.3 GRUC compilation into prompt files

At tier 2-3 the writing and analysis workflows call `/write-prompts`. Each generated prompt is a single-pass task and carries:

- By reference (path): the GUIDES of document type and technique, the TEMPLATE, the persona file, the DRAFT
- By compiled subset (pasted): the decisions of the GUIDES that this pass executes (for example "Decision 7-8: revision passes, quote management" for a line-edit prompt) and the RULES IDs that `/verify` will check after this pass; never the whole GUIDES, never CHECKS
- The checkpoint prompt that follows: `/verify` against the named RULES IDs, `/fix`
- Passes per document type (ebook shown; report drops stitching and chapter summaries; article runs single-turn): developmental (from DRAFT or input) → chapter prompts (1-2 chapters each, write plus line pass, then append the Chapter Summary) → separate checkpoint prompt → copy pass per 2-4 chapters against the Style Sheet → book consistency pass → stitching → `/fact-check` → release check → VCRIV gate
- Every chapter prompt reads the Style Sheet and all Chapter Summaries written so far (running memory); the outline in the DRAFT may be refined by a chapter prompt only in its Open Questions section, never silently
- Model choice follows `MODEL_INVENTORY.md`: compile and stitching prompts need the 1M-context class; chapter prompts run on the headless default with the `guarded` profile

### 8.4 Discovery by filename pattern (FR-05)

```
using <ID>     → exists writing_techniques/<ID>_GUIDES.md ? load set : list README IDs, stop
as <PERSONA>   → exists writing_personas/<PERSONA>.md ? load : list README names, stop
<verb>-<type>  → load document_types/<TYPE>_GUIDES.md, <TYPE>_RULES.md, <TYPE>_TEMPLATE.md section OPTIONS | DRAFT | Output
/verify target → header **Document Type**, **Technique**, **Persona** → same lookup, RULES + TEMPLATE only
```

### 8.5 Release check

- Defined per document type in `[TYPE]_RULES.md` (record format) and `[TYPE]_GUIDES.md` (last decision): header fields complete, every claim with a source or marked `[ASSUMED]`, cross-references resolve, numbering continuous, no process metadata in the output, style-pattern signals below the threshold set per document type in `[TYPE]_RULES.md` (a technique RULES file lists the structural signals its structure produces by construction, for example the fixed order of MINTO, and those signals are excluded), persona trait budget respected when a persona is set, word count against the target
- Record written to the DRAFT "Release Check" section when a DRAFT exists, else to the STRUT (tier 2-3) or the chat response (tier 1); a failed check loops to a revision pass inside `/write-*`, never back to Layer 2

### 8.6 Ranking scale and loop-back from Layer 2 to Layer 1

- Ranking scale for `/validate` and `/analyze` (DD-04, DD-06): `refuted` (refuting evidence ID recorded) < the seven ICD-203 likelihood terms in their standard order < `proven` (`[PROVEN]` or `[TESTED]` evidence). The rank position (0-8) is the comparable score; the likelihood phrase and a separate confidence phrase (low, moderate, high) are written as prose, never as bracket labels
- Ranking order within one likelihood term: higher confidence first, then higher evidence weight; the tie-break is recorded, so no two items share a position (Dhami 2019: unstructured ACH use produced tied ranks)
- An item with low confidence and `exhausted: yes` in its disconfirmation log is an open item → `VALIDATION_TEMPLATE.md` section "Research Questions for Layer 1" gets one question with the item ID
- The user (or `/go`) decides whether to run `/research` or `/deep-research` on those questions; `/analyze` never calls Layer 1 itself

### 8.7 Extension rule

- New document type: `document_types/[TYPE]_GUIDES/RULES/CHECKS/TEMPLATE.md` + three thin workflows copied from the article trio + README line + `ID-REGISTRY.md` prefix. No other edit
- New technique or persona: files + README line
- New analysis stage: `[STAGE]_GUIDES/RULES/TEMPLATE.md` + a section in `ANALYSIS_CHECKS.md` + one stage workflow + a line in `ANALYSIS_GUIDES.md` stage sequence
- New research approach in a running program: a new `T##_` folder and a new prompt file; the program Summary gains a row

## 9. Action Flow

### 9.1 Tier 1 - article in 2-10 minutes

```
/research "<question>"
└─> _INFO_[TOPIC]-IN01_[Title].md                       (one turn)
/propose-article _INFO_... [using <ID>] [N options]
├─> reads ARTICLE_GUIDES Decision 1-3 (+ <ID>_GUIDES structure decisions)
└─> [ID|ARTICLE]-OPTIONS-01_[Title].md                   scored options, one recommended
user picks option (or annotates)
/write-article [ID|ARTICLE]-OPTIONS-01 [as <PERSONA>] [for <audience>]
├─> expands chosen outline (developmental), writes prose
├─> line pass, copy pass (same turn), release check → chat
└─> YYYY-MM-DD_[Title].md                                header: Document Type, Technique, Persona
/verify (optional)  → detects set from header, RULES + TEMPLATE
```

### 9.2 Tier 2 - report in 10-60 minutes

```
/deep-research "<question>"                             tier 2 fixed
├─> T01_[SUBTOPIC]_[Name]_YYYY-MM-DD/_agentwork/__STRUT_, _PROMPTS_01
├─> execute 3-10 prompts, checkpoint after each
└─> C1: _INFO_-01_Summary, -02_Sources, topic files, _SOURCES/
/analyze T01_[SUBTOPIC]_*                               tier 2 default
├─> S01_[SUBTOPIC]_Analysis_YYYY-MM-DD/_agentwork/__STRUT_, _PROMPTS_01 (pattern detection, hypotheses, validation, checkpoints, VCRIV)
├─> runs without pause; local or web evidence search as needed
└─> C2: _INFO_[TOPIC]-[SUBTOPIC]-IN01_Analysis.md (user reviews the finished INFO)
/propose-report C2 [using <ID>]        → [ID|REPORT]-OPTIONS-01_[Title].md
/draft-report OPTIONS choice           → [ID|REPORT]-DRAFT-01_[Title].md (headings, evidence, Style Sheet, open questions)
user annotates DRAFT
/write-report DRAFT [as <PERSONA>]     tier 1 if <= 6 sections and <= 5,000 words, else tier 2
├─> tier 2: __STRUT_, _PROMPTS_01 (sections → line → copy → fact-check → release → VCRIV)
└─> C3: YYYY-MM-DD_[Title].md + Release Check in DRAFT
/render YYYY-MM-DD_[Title].md          → _EXPORT_gitignore/*.html, *.pdf
```

### 9.3 Tier 3 - ebook in 2-20 hours

```
/research-program "<goal>" [approaches: A, B, C]        tier 3 fixed
├─> Preflight: session __STRUT_[TOPIC] (approaches, A1..An, caps vs NFR-01, HWH estimate) → [plan only? stop]
├─> per approach: T0N_[SUBTOPIC]_[Name]/ with own __STRUT_, 1-2 _PROMPTS_ files
├─> headless execution, checkpoint per prompt, VCRIV gates <= 3
└─> C1: per-approach Summaries + session _INFO_[TOPIC]-IN01_Summary.md (Approach Comparison)
/analyze T01_* T02_* T03_*                              tier 3 by input shape
├─> S01_[SUBTOPIC]_Analysis/: __STRUT_, _PROMPTS_01 pattern detection, _PROMPTS_02 hypotheses, _PROMPTS_03 validation (+ devil's advocate)
├─> user review between files (after Pattern Map, after Hypothesis Register)
└─> C2: one _INFO_..._Analysis.md (Pattern Map, Hypothesis Register, Validation Report, Research Questions for Layer 1)
[optional loop] /deep-research on open research questions → re-run /validate
/propose-ebook C2 compare techniques MINTO, STA, DIATAXIS
├─> one outline option per technique, one sample chapter each, scored (GUIDES scoring criteria + style-pattern signals)
└─> [EBOOK]-OPTIONS-01_[Title].md with bake-off results, one recommended
/draft-ebook OPTIONS choice            → [ID|EBOOK]-DRAFT-01_[Title].md (promise, reader path, chapter pattern, TOC as argument, Style Sheet = series bible)
user annotates DRAFT
/write-ebook DRAFT [as <PERSONA>]      tier 3 fixed; parts when above NFR-01
├─> __STRUT_[TITLE], _PROMPTS_01..0N: chapters (1-2 per prompt, write + line pass + Chapter Summary) → checkpoint → copy pass vs Style Sheet
├─> book consistency pass → stitching (front matter, chapters, back matter) → /fact-check → release check → VCRIV
├─> _agentwork/ch-NN_*.md consumed by stitching
└─> C3: YYYY-MM-DD_[Title].md + Release Check in DRAFT
/render → html, pdf        /cleanup → removes _agentwork/ after goal reached
```

## 10. Data Structures

### 10.1 Entry workflow inventory (18 after this SPEC)

- **Layer 1** (4): `research` tier 1 fixed, exists · `deep-research` tier 2 fixed, exists · `research-program` tier 3 fixed, exists · `bundle` tier 1 fixed, exists, optional
- **Layer 2** (5): `pattern-detect` tier 1 default, exists · `hypothesize` tier 1 default, exists · `validate` tier 1 default, exists · `analyze` tier 2 default, tier 3 by input shape, exists · `investigate` exists, behavior unchanged
- **Layer 3** (9): `propose-article`, `draft-article`, `write-article` tier 1 fixed · `propose-report`, `draft-report` tier 1 fixed, `write-report` tier 1 default · `propose-ebook`, `draft-ebook` tier 1 fixed, `write-ebook` tier 3 fixed; all exist; all nine accept `inline`
- **Retired / Deleted** (2): `propose-minto`, `write-minto` (deleted)
- **Repointed** (3): `verify`, `critique`, `improve` (FR-06)

### 10.2 Skill folder layouts

```
research-methods/
├── SKILL.md                         Intent Lookup (unchanged shape)
├── RESEARCH_GUIDES.md               new: tiers, scope, strategy, platforms, load unit, synthesis, bundle decisions
├── RESEARCH_RULES.md                existing
├── RESEARCH_CHECKS.md               new: PD + QI
├── RESEARCH_STRATEGY_MEPI.md        existing, reduced to deltas
├── RESEARCH_STRATEGY_MCPI.md        existing, reduced to deltas
├── RESEARCH_SUMMARY_RULES.md, RESEARCH_SUMMARY_TEMPLATE.md, RESEARCH_CREATE_SUMMARY.md   existing
├── RESEARCH_SOURCES_TEMPLATE.md     new
├── RESEARCH_TOC_TEMPLATE.md, RESEARCH_CREATE_TOC.md, RESEARCH_TOOLS.md                 existing
├── research_areas/                  default/, legal/, market-intel/, software/ (moved, DD-05)
└── research_profiles/               PERSONAL, ORGA, COMPANY, NETWORK (renamed from profiles/, DD-05)

analysis-methods/                    new: 13 files; moved: 3 files
├── SKILL.md                         Intent Lookup, Do NOT Apply When, contracts C1 → C2, prefixes ANA PTD HYP VAL
├── ANALYSIS_GUIDES.md               /analyze: tier 2 vs 3, stage sequence, review points, loop-back, devil's advocate, 74 terms
├── ANALYSIS_CHECKS.md               PD + QI for /analyze and all three stages (one section each)
├── ANALYSIS_TEMPLATE.md             one-INFO output of /analyze: Pattern Map, Hypothesis Register, Validation Report
├── PATTERN-DETECTION_GUIDES.md, PATTERN-DETECTION_RULES.md, PATTERN-DETECTION_TEMPLATE.md
├── HYPOTHESIS_GUIDES.md, HYPOTHESIS_RULES.md, HYPOTHESIS_TEMPLATE.md
├── VALIDATION_GUIDES.md, VALIDATION_RULES.md, VALIDATION_TEMPLATE.md
└── INVESTIGATION_GUIDES.md, INVESTIGATION_LOG_RULES.md, INVESTIGATION_LOG_TEMPLATE.md   moved from write-documents

write-documents/                     composite
├── SKILL.md                         router-only: routing table, shared rules, quick commands
├── [existing planning and system GRUC files stay at root: SPEC_*, IMPL_*, PROMPTS_*, SKILL_*, WORKFLOW_*, TEMPLATE_*, ...]
├── document_types/
│   ├── ARTICLE_GUIDES.md, ARTICLE_RULES.md, ARTICLE_CHECKS.md, ARTICLE_TEMPLATE.md (sections OPTIONS, DRAFT, Output)
│   └── REPORT_*  (same 4)           EBOOK_*  (same 4)
├── writing_techniques/
│   ├── README.md                    one line per ID + "when to use which" matrix with genre map (DD-09, DD-41)
│   ├── [ID]_GUIDES.md, [ID]_RULES.md, [ID]_CHECKS.md   x 9
│   ├── TEMPLATES/[ID]_TEMPLATE.md, [ID]_OPTIONS_TEMPLATE.md
│   └── EXAMPLES/[ID]_EXAMPLE_NN-[Title].md
└── writing_personas/
    ├── README.md                    one line per persona
    └── [PERSONA].md                 x 20
```

### 10.3 Header blocks

Output document (C3):
```
# [Title]

**Doc ID**: MUSICPROMO-ARTICLE-01
**Document Type**: article
**Technique**: ABTSTORY
**Persona**: none
**Audience**: independent musicians planning a first release
**Source**: ABTSTORY-DRAFT-01_FirstReleaseTiming.md
```

OPTIONS file (`[ID]-OPTIONS-NN_[Title].md`):
```
# OPTIONS: [Title]

**Doc ID**: [TOPIC]-[ID]-OPTIONS-[NN]
**Document Type**: report
**Technique**: MINTO | none
**Source**: _INFO_[TOPIC]-IN01_Analysis.md
**Scoring criteria**: [from [TYPE]_GUIDES options-scoring decision, listed by name]

## Option 1: [Action title]            <- repeated N times, labeled lines, no tables
- **Governing thought / theme / promise**: ...
- **Outline**: ...
- **Score**: [criterion: value] ...
- **Sample** (compare techniques only): ...

## Recommendation
- **Option**: N - **Why**: one sentence per criterion that decided it
```

DRAFT file (`[ID]-DRAFT-NN_[Title].md`): header as OPTIONS with Doc ID `[TOPIC]-[ID]-DRAFT-[NN]` plus `**Chosen option**` (or `**Source**` when drafted from raw input); sections `Structure` (headings with job and hand-off per section; report and ebook: fill-in instructions and diagram placeholders per chapter), `Evidence Placement` (claim → source ID), `Style Sheet` (terminology, numbers, tone, cross-reference format, recap convention), `Chapter Summaries` (ebook; extended by every chapter prompt), `Open Questions`, `Release Check` (filled by `/write-*`).

### 10.4 Layer 2 register rows (labeled lines)

```
## H-03
- **Statement**: Releases announced 6+ weeks ahead reach 2x the first-week streams of releases announced under 2 weeks ahead
- **Form**: correlational   - **Source themes**: T-02, T-05   - **Rival**: H-04 (playlist placement, not lead time, drives the difference)
- **Falsifier**: a sample of 20+ releases where lead time and first-week streams show no monotonic relation
- **Prior likelihood**: likely   - **Confidence**: moderate
- **Test plan**: evidence type: release data with dates; where: label reports in _SOURCES/, web search when local data does not settle it; refutes if: ...
- **Rank** (VALIDATION): position 5 on the 0-8 scale - likely, moderate confidence; tie-break vs H-04: higher evidence weight - exhausted: no - disconfirmation log: DL-07
```

### 10.5 Session folder layout at tier 3

```
_YYYY-MM-DD_[Session]/
├── _agentwork/__STRUT_[TOPIC].md, _PROMPTS_00-Preflight.md          program level
├── T01_[SUBTOPIC]_[Approach]_YYYY-MM-DD/   _agentwork/__STRUT_, _PROMPTS_01..02, _INFO_-01_Summary, -02_Sources, topic files, _SOURCES/
├── T02_.../  T03_.../  T04_.../            at most 4 approaches
├── _INFO_[TOPIC]-IN01_Summary.md           program Summary with Approach Comparison
├── S01_[SUBTOPIC]_Analysis_YYYY-MM-DD/     _agentwork/, one _INFO_..._Analysis.md
├── [ID]-OPTIONS-01_[Title].md, [ID]-DRAFT-01_[Title].md
├── _agentwork/__STRUT_[TITLE].md, _PROMPTS_01..0N-Write*.md, ch-NN_*.md   ebook writing
├── YYYY-MM-DD_[Title].md                   C3
├── _EXPORT_gitignore/                      /render output
└── NOTES.md, PROGRESS.md, PROBLEMS.md      session tracking (only via /session-save)
```

## 11. Logging Requirements

N/A for App-Level and Script-Level: the implementation is Markdown workflows and skill files; no scripts are added. User-Facing output is the chat response and follows three fixed lines:

- First line of every tiered call: `Tier N - [reason]` (NFR-03 verification)
- Progress during tier 2-3 execution: `[ k / n ] prompts done - [current prompt title]`
- Last line: artifact list with paths (and page counts after `/render`)

## 12. Technical Constraints

- `[PROMPTSYSTEM_FOLDER]` is the source of truth; `[AGENT_FOLDER]` receives a robocopy; no direct edits in `.devin/` (workspace NOTES, invariant 1)
- Workflow files follow IPPSWFLW-SP01 anatomy and the `auto_execution_mode` frontmatter of their siblings; skill files follow IPPSSKLS-SP01 and SK-AR-01..07
- Prompt files follow IPPSPRMTFMT-SP01 and `PROMPTS_RULES.md`; STRUTs follow `STRUT_TEMPLATE.md`; the `guarded` profile is defined in `PROMPTS_GUIDES.md`
- `/write-prompts` is the only mechanism that produces prompt files; writing and analysis workflows call it rather than emitting prompts themselves
- The 74 binding terms of RSRCHMTHD-IN03 are the vocabulary of all Layer 2 files; ICD-203 likelihood terms are the only allowed likelihood words
- AI-writing detection rules (`specs/AI_WRITING_DETECTION_RULES.md`) are part of every release check and every bake-off score
- `ID-REGISTRY.md` and `rules/promptsystem-core.md` (skill list, document placement) are updated in increment D before sync
- Cascade: `gesetze-im-internet.de` via Playwright only; Google for URL discovery only; these MUST-NOT-FORGET lines are copied into `RESEARCH_GUIDES.md` and every research workflow
- `INVESTIGATION_*` files move to `analysis-methods` unchanged (DD-01); `investigate.md` and any file referencing them update the path in the same increment; INVESTIGATE-SP01 behavior is untouched
- No Markdown tables in any new file (core-conventions); repeating units use labeled lines

## 13. Migration Map

Source → target, action. Executed in increments A-D (DD-40); each row is verifiable by file existence.

**Increment A - Layer 3**
- `T02_.../WRITING_TECHNIQUES/[OLD-ID]_*.md` → `write-documents/writing_techniques/[ID]_*.md` - copy, rename per DD-20, `-DRAFT` → `-OPTIONS`, GUIDES rewritten to FR-30
- `T02_.../WRITING_TECHNIQUES/TEMPLATES/`, `EXAMPLES/` → `writing_techniques/TEMPLATES/`, `EXAMPLES/` - copy, rename
- `T02_.../WRITING_PERSONAS/*.md` → `write-documents/writing_personas/` - copy, DD-07 and DD-32 applied
- `write-documents/MINTO_GUIDES.md`, `MINTO_RULES.md`, `MINTO_TEMPLATE.md`, `MINTO-DRAFT_TEMPLATE.md` + `T02 SCQA-PYRAMID_*` → `writing_techniques/MINTO_*`, `TEMPLATES/MINTO_TEMPLATE.md`, `TEMPLATES/MINTO_OPTIONS_TEMPLATE.md` - merge, delete root originals
- `T02_.../WRITING_TECHNIQUES/PAS-AIDA-CONVERSION_*` → two full sets `PAS_*` and `AIDA_*` (DD-20)
- new `document_types/ARTICLE_*`, `REPORT_*`, `EBOOK_*` (4 each) - create from WRTCRAFT-IN01 Section 2 decisions and IN08 Sections 2-3
- `write-documents/SKILL.md` - rewrite as router
- new `workflows/propose-article.md` ... `write-ebook.md` (9) - create from one thin pattern
- `workflows/propose-minto.md`, `write-minto.md` - delete; `README.md` notes `using MINTO`
- `workflows/verify.md`, `critique.md`, `improve.md` - replace `MINTO_*` paths with header-based detection

**Increment B - Layer 1**
- new `research-methods/RESEARCH_GUIDES.md`, `RESEARCH_CHECKS.md`, `RESEARCH_SOURCES_TEMPLATE.md` - create
- `RESEARCH_STRATEGY_MEPI.md`, `RESEARCH_STRATEGY_MCPI.md` - move shared Phase 1-4 text to GUIDES, keep deltas
- `research-methods/profiles/` → `research_profiles/`; `default/`, `legal/`, `market-intel/`, `software/` → `research_areas/` - move, update references in `SKILL.md`, `RESEARCH_*`, `research.md`, `deep-research.md` (DD-05)
- `workflows/research.md` - fix dead reference, update profile paths
- `workflows/deep-research.md` - rewrite to full anatomy
- new `workflows/research-program.md`, `workflows/bundle.md` - create

**Increment C - Layer 2**
- new `skills/analysis-methods/` (13 files) - create from RSRCHMTHD-01..03, -05..-08 method content
- `write-documents/INVESTIGATION_GUIDES.md`, `INVESTIGATION_LOG_RULES.md`, `INVESTIGATION_LOG_TEMPLATE.md` → `analysis-methods/` - move; update `investigate.md` and `write-documents/SKILL.md` references
- new `workflows/pattern-detect.md`, `hypothesize.md`, `validate.md`, `analyze.md` - create

**Increment D - Registration and sync**
- `ID-REGISTRY.md` - add prefixes `ART`, `RPT`, `EBK`, `ANA`, `PTD`, `HYP`, `VAL`, nine technique IDs; mark `SCQA-PYRAMID`, `PAS-AIDA-CONVERSION`, `ABT-STORY-SPINE` and other old IDs as renamed
- `rules/promptsystem-core.md` - skill list gains `analysis-methods`; document placement gains OPTIONS/DRAFT rule (DD-36)
- `README.md` - workflow table, retired commands, `using` / `as` grammar
- `docs/_INFO_GRUC_GUIDES_RULES_CHECKS.md` - add document-type and analysis-stage sets to the inventory
- robocopy `[PROMPTSYSTEM_FOLDER]` → `[AGENT_FOLDER]`; `/verify` on every new file; `/session-save`

## 14. Document History

**[2026-11-08 12:55]**
- Added: DRSYNART-DD-50 (`AI_WRITING_RULES.md` in `write-documents/` for publishing document types `article`, `report`, `ebook` only; loaded before writing by `draft-*`/`write-*` and enforced after writing by `/verify`, `/critique`, `/improve`; persona owns text length and pacing)
- Changed: Section 12 updated reference from `specs/AI_WRITING_DETECTION_RULES.md` to `write-documents/AI_WRITING_RULES.md` (`AW-*`)

**[2026-11-02 22:45]**
- Changed: SP01 reverse-update pass (P11 per DRSYNART-DD-49)
- Fixed: agent-work folder spelling updated to `_agentwork/` across all occurrences (DD-49)
- Fixed: Section 10.1 workflow inventory marked "exists", retired MINTO workflows marked deleted
- Fixed: Section 3 Persona definition aligned to "six sliders, 1-3 micro-dosed traits (from the 14-trait catalog)" (VF-09)
- Added: FR-24 defined working folder without a session as the input file's folder, else workspace root (RV-015)
- Changed: Timeline updated count synchronized to Document History entries (VF-10)

**[2026-11-02 22:30]**
- Added: DRSYNART-NFR-07 per-call instruction working set <= 15k tokens budget (DD-47)
- Changed: Section 8.5 reworded AI-writing detection signals to style-pattern signals per DD-47; dropped detector-threshold calibration backlog item

**[2026-11-02 22:00]**
- Changed: FR-22 added OPTIONS-form criterion (technique owns an OPTIONS template only where planning artifact is not a section outline; today: MINTO) per DD-44
- Added: FR-35 Fusion Contract paragraph (slot interface, substitution not judgment, single materialization in OPTIONS/DRAFT) per DD-44

**[2026-10-29 21:50]**
- Added: DD-42 Release 1 scope (consolidations and deferral list) for the implementation STRUT `_agentwork/__STRUT_RWTOOLIMPL.md`
- Changed: FR-21 document-type sets 6 → 4 files (TEMPLATE with OPTIONS, DRAFT, Output sections), document-type EXAMPLES deferred; FR-13 stage CHECKS consolidated into `ANALYSIS_CHECKS.md` (16 → 13 new files); Sections 8.4, 8.7, 10.2, 13 aligned

**[2026-10-29 21:45]**
- Inline `/critique` → `/reconcile` → `/implement` against NOTES.md: 23 findings (3 critical, 7 high, 11 medium, 2 low), all confirmed and applied
- Fixed: DD-01..DD-09, DD-15..DD-20 restated per NOTES.md wording (DD-02, DD-03, DD-06, DD-09 were misrestated); NOTES.md declared authoritative; IG-11 traceability added
- Fixed: confirmed decisions no longer overridden - `/bundle` restored as optional thin workflow (DD-01, DD-03; DD-31 rewritten), `PAS` and `AIDA` as two full sets (DD-20), `research_profiles/` and `research_areas/` (DD-05), `INVESTIGATION_*` moved to `analysis-methods` (DD-01), stage GRUC sets renamed `PATTERN-DETECTION`, `HYPOTHESIS`, `VALIDATION` (DD-04)
- Fixed: `/analyze` always STRUT first and one INFO, tier 2 or 3 only (DD-04); `plan` keyword added
- Fixed: `/validate` accepts statements, uses local or web evidence at every tier, ranks on one scale `refuted` < ICD-203 terms < `proven` with prose likelihood and confidence (DD-04, DD-06); GRADE plus Toulmin, ACH as audit trail only; no tied ranks
- Added: `inline` keyword (DD-17); tier 1 renamed "single-turn" to free the word; option count default from GUIDES; OPTIONS and DRAFT optional for all `draft-*` and `write-*`; draft fill-in instructions and diagram placeholders
- Added: DD-41 genre map (initial-request template types as document type x technique); DD-20 document-type coverage
- Fixed: tier arithmetic - caps count all prompts per tier-3 call, escalation rule tier 2 → 3, `/write-ebook` tier 3 fixed, chapter prompts 1-2 chapters, books split into parts above NFR-01
- Fixed: no human pause inside a PROMPTS file; tier 3 review only between files
- Added: `document_types/` function subfolder; Chapter Summaries as running memory for ebook prompts; separate checkpoint prompts (no self-verification); AI-detection threshold per document type with technique exemptions
- Fixed: bake-off scoring no longer uses CHECKS (GRUC-IG-03); WRTCRAFT-DD-21..24 marked pending; PR ID `DRSYNART-WRTSTYLTCH-PR-0004`; unverified reference-session numbers removed; NOTES tier-3 range explicitly superseded

**[2026-10-29 21:30]**
- Initial specification created from DRSYNART-IN01, IN02, RSRCHMTHD-01/03, WRTSTYLTCH-01/04, WRTCRAFT-01/08/11
- Decisions DD-30..DD-40 added (agent-proposed under the user's "decide in favour of simplicity" instruction; DD-32 and DD-33 need explicit user confirmation before increment A)
- Open for user confirmation: DD-32 (persona style conflicts), DD-33 (scripts deferred), DD-34 (no fading), DD-39 (bake-off keyword), NFR-01 caps
