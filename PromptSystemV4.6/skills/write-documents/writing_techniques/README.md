# Writing Techniques Library

**Goal**: Catalog of 9 writing techniques that control HOW a document is structured (section order, argument logic, narrative arc, reader progression), each packaged as a GRUC set (Guides, Rules, Checks) plus a template and example.

**Note**: Selection is by keyword `using <ID>`. `using MINTO` replaces the retired workflows propose-minto and write-minto.

## Table of Contents

- [1. Purpose and How Techniques Pair with Personas](#1-purpose-and-how-techniques-pair-with-personas)
- [2. Technique Catalog](#2-technique-catalog)
- [3. User-Only Selection Rule (DRSYNART-DD-08)](#3-user-only-selection-rule-drsynart-dd-08)
- [4. When to Use Which: By Media Type and Genre Map (DRSYNART-DD-41)](#4-when-to-use-which-by-media-type-and-genre-map-drsynart-dd-41)
- [5. When to Use Which: By Reader Goal and Cognitive Mechanism](#5-when-to-use-which-by-reader-goal-and-cognitive-mechanism)
- [6. Common Confusions](#6-common-confusions)
- [7. GRUC Architecture Map](#7-gruc-architecture-map)
- [8. File Inventory and Rule ID Prefixes](#8-file-inventory-and-rule-id-prefixes)

## 1. Purpose and How Techniques Pair with Personas

A technique defines document-level structure. A persona from `WRITING_PERSONAS/` defines sentence-level voice (6 sliders, 1-3 micro-dosed traits). The two are orthogonal (`DRSYNART-DD-09`) and combine in one command:

```
/write-article about <topic> using <input> as <persona> using <technique>
```

- `using <technique>` decides: opening mechanism, section sequence, where the main claim appears, how evidence is ordered, how the text ends
- `as <persona>` decides: formality, warmth, humor, narrative density, jargon level, and the few rhetorical traits allowed
- Example: `using MINTO as CXO-ADVISOR` produces an answer-first board memo in executive register; `using MINTO as FOUNDER-ESSAYIST` produces the same argument structure in plain everyday words
- Both parts are optional and chosen only by the user (`DRSYNART-DD-08`). A command with only `using <technique>` gets no persona; a command with only `as <persona>` gets no technique
- Conflict rule: when a persona slider pulls against a technique rule (for example Narrative 7 against an answer-first opening), the technique rule wins for structure and the persona wins for wording inside each section
- Mechanism-first organization: each technique is defined once and reused across media types, because one medium often needs several techniques (a user manual uses 4 Diataxis modes) and one technique serves several media (MINTO serves memos, articles, and whitepapers)

## 2. Technique Catalog

One line per DD-20 technique ID, linking each set's GUIDES:

- **MINTO**: [MINTO_GUIDES.md](MINTO_GUIDES.md) - Answer-first governing thought and MECE question-and-answer tree; serves reports, flagship articles, and executive proposals.
- **IMINTO**: [IMINTO_GUIDES.md](IMINTO_GUIDES.md) - Decreasing-importance inverted pyramid with 25-40 word lede; serves news-style briefings, release notes, and incident briefs.
- **ABTSTORY**: [ABTSTORY_GUIDES.md](ABTSTORY_GUIDES.md) - Narrative tension arc with And, But, Therefore opening and embedded Story Spine; serves founder essays, science and strategy articles, and chapter openings.
- **KABOB**: [KABOB_GUIDES.md](KABOB_GUIDES.md) - Wall Street Journal feature structure (anecdote lede, nut graf, claim-driven body, kicker); serves flagship articles, long-form essays, and case-driven analyses.
- **STA**: [STA_GUIDES.md](STA_GUIDES.md) - Inductive craft teaching (concrete Show case, Tell principle, numbered Apply steps, quick check); serves nonfiction ebooks, tutorials, and onboarding guides.
- **PAS**: [PAS_GUIDES.md](PAS_GUIDES.md) - Direct-response conversion (Problem recognition, cost Agitation, Solution mechanism, honest limit, single CTA); serves marketing articles, landing pages, cold emails, and ad copy.
- **AIDA**: [AIDA_GUIDES.md](AIDA_GUIDES.md) - Progressive conversion (Attention hook, Interest mechanism, Desire benefits, Action CTA); serves product pages, comparison articles, and warm emails.
- **DIATAXIS**: [DIATAXIS_GUIDES.md](DIATAXIS_GUIDES.md) - Need-based documentation modes (tutorial, how-to, reference, explanation); serves technical manuals, developer documentation, and system reference reports.
- **IMRAD**: [IMRAD_GUIDES.md](IMRAD_GUIDES.md) - Complete empirical research reporting (Abstract, Introduction, Methods, Results, Discussion, Limitations); serves scientific papers, empirical research reports, and benchmark studies.

## 3. User-Only Selection Rule (DRSYNART-DD-08)

- **Rule**: Only the user chooses a technique. The agent applies a technique only when the user passes `using <ID>`
- **Default without `using <ID>`**: The agent structures the text with its own reasoning, following the standard instructions, templates, and standard GRUC files of the invoked workflow. No file from this library is applied: no `*_GUIDES.md`, `*_RULES.md`, `*_CHECKS.md`, `TEMPLATES/`, or `EXAMPLES/` file
- **Partial input**: When the user passes only `as <persona>`, the agent applies only the persona. It never adds a technique
- **Same rule for personas**: Without `as <persona>`, no persona file is applied
- **Proactive selection**: Allowed ONLY when the user explicitly asks for help with writing techniques or document structure (for example "how should I structure this report?"). The agent then recommends from Sections 4-5, names the technique ID, and states why it fits the reader goal
- **Forbidden**: Picking, adding, or switching a technique without user input, for example because the content "looks like" a report or a landing page. When a chosen technique does not fit, the agent tells the user and keeps the chosen technique until the user decides
- **Retirement replacement**: `using MINTO` replaces the retired workflows propose-minto and write-minto (DRSYNART-DD-19). Invoke `/propose-article ... using MINTO` or `/propose-report ... using MINTO`, and `/write-article ... using MINTO` or `/write-report ... using MINTO`

## 4. When to Use Which: By Media Type and Genre Map (DRSYNART-DD-41)

Use only when the user asks for structure help (`DRSYNART-DD-08`):

- **Reports (decision, empirical, reference)**
  - Primary: `using MINTO` (business proposals, decision reports, board memos)
  - Alternatives: `using IMRAD` (scientific papers, empirical results, benchmarks), `using DIATAXIS` (reference documentation, system specifications)
  - Recommended Personas: CXO-ADVISOR, STRATEGIC-THINKER, ANALYST, JURIST, PRINCIPAL-ARCHITECT
- **Flagship Articles & Essays (long-form, thought leadership)**
  - Primary: `using KABOB` (case-driven industry trends, feature stories)
  - Alternatives: `using MINTO` (thesis-driven arguments, executive essays), `using ABTSTORY` (founder essays, narrative arcs)
  - Recommended Personas: SECTOR-COLUMNIST, INTELLECTUAL, INVESTIGATIVE-JOURNALIST, FOUNDER-ESSAYIST
- **Marketing Material & Landing Pages (direct response, conversion)**
  - Primary: `using PAS` (problem-aware prospects, search landing pages, cold emails)
  - Alternatives: `using AIDA` (product-aware prospects, product pages, comparison pages), `using KABOB` (case studies)
  - Recommended Personas: CONVERSION-COPYWRITER, PRODUCT-POSITIONER, CASE-STORYTELLER
- **Technical Documentation & Manuals (user guides, system docs)**
  - Primary: `using DIATAXIS` (tutorials, how-to guides, reference, explanations)
  - Alternatives: `using IMINTO` (incident briefings, release notes), `using STA` (guided training)
  - Recommended Personas: TECHNICAL-WRITER, PRINCIPAL-ARCHITECT, UX-MANUAL-WRITER
- **Nonfiction Ebooks & Books (long-form instructional, book chapters)**
  - Primary: `using STA` (instructional chapters, craft guides)
  - Alternatives: `using ABTSTORY` (narrative chapter openings, case transitions), `using DIATAXIS` (user manuals)
  - Recommended Personas: BOOK-AUTHOR, COACH-MENTOR, PRACTITIONER-BLOGGER
- **News-Style Briefings & Updates (incident, release, company news)**
  - Primary: `using IMINTO` (most important facts in 25-40 word lede)
  - Alternatives: `using ABTSTORY` (context-conflict-action summaries)
  - Recommended Personas: INVESTIGATIVE-JOURNALIST, SECTOR-COLUMNIST
- **Engineering & Founder Blogs (practitioner insights)**
  - Primary: `using ABTSTORY` (technical journey, problem-to-solution narrative)
  - Alternatives: `using STA` (code walkthroughs, technical tutorials), `using IMINTO` (release briefs)
  - Recommended Personas: PRACTITIONER-BLOGGER, FOUNDER-ESSAYIST, JOEL-SPOLSKY, KARSTEN-HELD

## 5. When to Use Which: By Reader Goal and Cognitive Mechanism

Use only when the user asks for structure help (`DRSYNART-DD-08`):

- **Persuade a decision-maker**: `using MINTO` - Answer first; each section answers the question the previous level raises
- **Inform an early-stopping reader**: `using IMINTO` - Most important facts in a 25-40 word lede; every later paragraph matters less
- **Hold narrative tension across complex facts**: `using ABTSTORY` - AND (context) - BUT (conflict) - THEREFORE (consequence) replaces fact lists
- **Humanize a trend or analysis with a case**: `using KABOB` - Concrete person first, nut graf states the trend, kicker returns to the person
- **Teach a reusable craft or skill**: `using STA` - Inductive learning: case, then principle, then numbered application with a check
- **Convert a skeptical prospect**: `using PAS` - Problem recognition, cost of inaction, solution with proof, honest limit, one action
- **Engage a product-aware evaluator**: `using AIDA` - Distinct attention hook, mechanism interest, translated benefit desire, clear action CTA
- **Document a system or manual by user need**: `using DIATAXIS` - One page = one mode: tutorial, how-to guide, reference, or explanation
- **Document complete empirical findings**: `using IMRAD` - Completeness over the declared scope; method and limits let readers judge the data

## 6. Common Confusions

- `MINTO` selects evidence for one governing thought (article logic); `IMRAD` documents the whole finding set (report logic). Using MINTO for a report hides findings that do not support the main claim
- `PAS` agitates the reader's pain; `MINTO` states the complication neutrally. Using PAS for a board memo sounds manipulative; using MINTO for a landing page sounds cold
- `ABTSTORY` is often a component inside `MINTO` or `KABOB` (the opening paragraph or abstract), not the whole document
- `AIDA` starts with product attention; `PAS` starts with customer pain

## 7. GRUC Architecture Map

Each technique has five to six files (GUIDES, RULES, CHECKS, TEMPLATE, optional OPTIONS template, and EXAMPLE). Each workflow reads exactly one file type (`GRUC-SP01`), except `/verify`, which reads RULES and TEMPLATE.

```
Writing lifecycle for "using <TECHNIQUE>"
│
├─> BEFORE and DURING writing (working agent)
│   ├─> [TECHNIQUE]_GUIDES.md           decision steps, persona interaction
│   └─> EXAMPLES/[TECHNIQUE]_EXAMPLE_01-*.md   linked from GUIDES
│
├─> AFTER: structural verification (/verify)
│   ├─> [TECHNIQUE]_RULES.md            ST / CT / EV rules with BAD/GOOD pairs
│   └─> TEMPLATES/[TECHNIQUE]_TEMPLATE.md   section skeleton adherence
│
├─> AFTER: strategic review (/critique)
│   └─> [TECHNIQUE]_GUIDES.md + EXAMPLES   right technique? right approach?
│
├─> AFTER: process audit (/drift-detect)
│   └─> [TECHNIQUE]_CHECKS.md  section "Process Discipline (PD)"
│
└─> AFTER: quality improvement (/improve)
    └─> [TECHNIQUE]_CHECKS.md  section "Quality Improvement (QI)"
```

- The working agent never reads `*_CHECKS.md` while writing (prevents writing to pass the checks instead of serving the reader)
- `TEMPLATES/` files are skeletons only; filled-in demonstrations live in `EXAMPLES/`
- `EXAMPLES/` files show complete GOOD documents with a named persona and list key decisions; BAD/GOOD pairs stay in `*_RULES.md`

## 8. File Inventory and Rule ID Prefixes

- **MINTO**: Rule ID prefix `MINTO` - Template: `TEMPLATES/MINTO_TEMPLATE.md` + `TEMPLATES/MINTO_OPTIONS_TEMPLATE.md` - Example: `EXAMPLES/MINTO_EXAMPLE_01-ExecutiveProposal.md`
- **IMINTO**: Rule ID prefix `IMINTO` - Template: `TEMPLATES/IMINTO_TEMPLATE.md` - Example: `EXAMPLES/IMINTO_EXAMPLE_01-IncidentAndReleaseBrief.md`
- **ABTSTORY**: Rule ID prefix `ABTSTORY` - Template: `TEMPLATES/ABTSTORY_TEMPLATE.md` - Example: `EXAMPLES/ABTSTORY_EXAMPLE_01-ScienceAndStrategyArc.md`
- **KABOB**: Rule ID prefix `KABOB` - Template: `TEMPLATES/KABOB_TEMPLATE.md` - Example: `EXAMPLES/KABOB_EXAMPLE_01-IndustryFeatureArticle.md`
- **STA**: Rule ID prefix `STA` - Template: `TEMPLATES/STA_TEMPLATE.md` - Example: `EXAMPLES/STA_EXAMPLE_01-EbookChapterAndGuide.md`
- **PAS**: Rule ID prefix `PAS` - Template: `TEMPLATES/PAS_TEMPLATE.md` - Example: `EXAMPLES/PAS_EXAMPLE_01-WebsiteLandingPage.md`
- **AIDA**: Rule ID prefix `AIDA` - Template: `TEMPLATES/AIDA_TEMPLATE.md` - Example: deferred to Release 2 (`EXAMPLES/PAS_EXAMPLE_01-WebsiteLandingPage.md` used as interim reference per DD-42)
- **DIATAXIS**: Rule ID prefix `DIATAXIS` - Template: `TEMPLATES/DIATAXIS_TEMPLATE.md` - Example: `EXAMPLES/DIATAXIS_EXAMPLE_01-UserManualAndHowTo.md`
- **IMRAD**: Rule ID prefix `IMRAD` - Template: `TEMPLATES/IMRAD_TEMPLATE.md` - Example: `EXAMPLES/IMRAD_EXAMPLE_01-EmpiricalResultsReport.md`

Rule ID categories in every `*_RULES.md`: `[PREFIX]-ST-NN` structure, `[PREFIX]-CT-NN` content, `[PREFIX]-EV-NN` evidence. Checks use `[PREFIX]-PD-NN` (process discipline) and `[PREFIX]-QI-NN` (quality improvement).

Expansions: MINTO = Situation, Complication, Question, Answer; ABT = And, But, Therefore; PAS = Problem, Agitate, Solve; AIDA = Attention, Interest, Desire, Action; IMRaD = Introduction, Methods, Results, and Discussion; GRUC = Guides, Rules, Checks (plus Examples and Templates).

Sources: `_INFO_WRTSTYLTCH-04_WritingTechniquesAndMediaMapping.md [DRSYNART-WRTSTYLTCH-IN04]` (technique research, taxonomy decision), `specs/_SPEC_GRUC_STANDARD.md [GRUC-SP01]` (file type boundaries).

## Document History

**[2026-10-29 22:25]**
- Changed: Catalog updated to 9 DD-20 technique IDs with links to each GUIDES; tables converted to lists per core-conventions no-tables rule; DD-41 genre map added; `using MINTO` replacement note for propose-minto and write-minto added (P1-S6)

**[2026-10-29 16:15]**
- Changed: Section 2 renamed to "User-Only Selection Rule"; default without technique = standard workflow instructions, templates, GRUC files; partial input never auto-completed; Section 4 gated to user help requests (DRSYNART-DD-08 revision)

**[2026-10-29 16:40]**
- Initial: README with persona pairing, DRSYNART-DD-08 unbiased default, media-type and reader-goal selector matrices, GRUC architecture map, file inventory with rule ID prefixes
