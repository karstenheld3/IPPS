<PromptSystem MarkdownTablesAllowed=true />
# Writing Personas Library

**Goal**: Catalog of 20 standalone writing personas that control HOW a text sounds (voice, register, micro-dosed character), with a selector for media type and audience psychology

## Table of Contents

1. [Purpose and Architecture](#1-purpose-and-architecture)
2. [User-Only Selection Rule (DRSYNART-DD-08)](#2-user-only-selection-rule-drsynart-dd-08)
3. [How to Load a Persona](#3-how-to-load-a-persona)
4. [20-Persona Comparison Table](#4-20-persona-comparison-table)
5. [When to Use Which Persona](#5-when-to-use-which-persona)
6. [Reference Catalog: 6 Sliders and 14 Micro-Dosed Traits](#6-reference-catalog-6-sliders-and-14-micro-dosed-traits)

## 1. Purpose and Architecture

A persona defines sentence-level voice only. Document structure (argument order, narrative arc, section skeleton) belongs to `WRITING_TECHNIQUES/` and is combined orthogonally (`DRSYNART-DD-09`): `as <persona>` = how it sounds, `using <technique>` = how it is organized.

Every persona file is a complete Writer Profile with 4 layers:

1. **Universal Zero-Bullshit Gate** (applies at every slider setting): Treat the reader's time as more valuable than your own (Bernoff Iron Imperative). Every sentence delivers a fact, clarifies a mechanism, or guides a decision. Zinsser Bracket Test: delete every word, aside, or metaphor that does no useful work. Plain connectives (*but, so, still, yet*), concrete verbs, natural burstiness (5-9 word sentences alternating with 18-28 word sentences), facts never altered by style
2. **3-Line Persona Header**: `Role` (who speaks), `Audience` (who reads, what they know), `Anti-Tone` (what to strictly avoid)
3. **6 Continuous Sliders (0-10)**: Formality, Warmth, Humor & Color, Narrative Drive, Density, Technicality. Each scale is read in 5 behavioral bands (`0-1`, `2-3`, `4-6`, `7-8`, `9-10`) because Large Language Models (LLMs) cannot distinguish single integer steps without a rubric. Every slider value is always sent to the LLM with its band rule in parentheses. Sliders govern 95% of sentences
4. **1-3 Micro-Dosed Voice Traits (`TR-01..14`)**: Binary `ON/OFF` rhetorical moves. Budget `<= 5%` of sentences: max 1 trait firing per 300-400 words (2-4 trait moments per 1,200-word article), never 2 traits in one paragraph, max 2-10 added words inside an existing sentence. Reason: LLMs over-apply persona traits 5x-10x compared to human authors (generative exaggeration)

```
┌──────────────────────────────────────────────────────────────────┐
│ WRITER PROFILE = GATE + HEADER + 6 SLIDERS + 1-3 TRAITS          │
├──────────────────────────────────────────────────────────────────┤
│ 1. Zero-Bullshit Gate   (every sentence, every persona)          │
│ 2. Persona Header       Role / Audience / Anti-Tone              │
│ 3. 6 Sliders 0-10       95% of sentences, 5 bands, band rule     │
│ 4. 1-3 Traits [ON]      <= 5% of sentences, never 2 per paragraph│
└──────────────────────────────────────────────────────────────────┘
```

Source framework: `docs/_INFO_HOW_TO_CONTROL_WRITING_STYLE_WITH_PARAMETERS_AND_TRAITS.md [DOCWRITEFW-IN01]` (17 personas). Gap analysis and 3 new personas: `_INFO_WRTSTYLTCH-03_WritingPersonasCatalogAndGaps.md [DRSYNART-WRTSTYLTCH-IN03]`.

## 2. User-Only Selection Rule (DRSYNART-DD-08)

- **Rule**: Only the user chooses a persona. The agent applies a persona file only when the user passes `as <persona>`
- **Default without `as <persona>`**: The agent writes with its own reasoning and style, following the standard instructions, templates, and standard GRUC files of the invoked workflow. No file from this library is applied: no Persona Header, no sliders, no traits, no Zero-Bullshit Gate from a persona file
- **Partial input**: When the user passes only `using <technique>`, the agent applies only the technique. It never adds a persona, also not from the persona lists in `WRITING_TECHNIQUES/*_GUIDES.md` or Section 5
- **Same rule for techniques**: Without `using <technique>`, no file from `WRITING_TECHNIQUES/` is applied
- **Proactive selection**: Allowed ONLY when the user explicitly asks for help with writing style or personas (e.g., "which persona fits a board memo?", "make this sound less corporate"). In that case the agent recommends from this library using Section 5 and states which persona it chose and why
- **Forbidden**: Picking, adding, or switching a persona without user input, for example because the topic "looks like" a board memo or because a technique lists fitting personas; mixing sliders or traits from two personas without being asked
- **Why**: The user may want the text in their own voice. An imposed persona is an unrequested bias that is hard to detect later

## 3. How to Load a Persona

- **One file is enough**: Each `WRITING_PERSONAS/[PERSONA-ID].md` is 100% self-contained. A workflow loads only that file and pastes Section 3 (Copy/Paste Writer Profile Prompt Block) at the top of the writing prompt
- **Grammar**: `/write-article about <topic> using <input> as <PERSONA-ID> using <TECHNIQUE>`
- **Rewrite protocol**: Pass 1 applies sliders and at most 2-4 trait firings. Pass 2 audits facts (every number, name, date identical to source), prunes any trait that exceeds 10 extra words or shares a paragraph with another trait
- **Trait markers**: Markers such as `(TR-08)` in persona samples are annotations for the reader of this library. Never output them in production text
- **Diagnostic tuning**: Text wastes time → raise Density to 5-6 and cut introductions that delay the point. Traits feel gimmicky → cap total firings at 2-3. Robotic staccato → lower Density, raise Warmth. Flat and generic → keep sliders, turn on 2 traits at 1 firing per 350 words

## 4. 20-Persona Comparison Table

Legend: F = Formality, W = Warmth, H = Humor & Color, N = Narrative Drive, D = Density, T = Technicality (all 0-10).

Abbreviations: C-suite = top executives (Chief Executive Officer, Chief Financial Officer), PE = Private Equity, capex = capital expenditure, CTO = Chief Technology Officer, ADR = Architecture Decision Record, SOP = Standard Operating Procedure, B2B = Business-to-Business, UI = User Interface, UX = User Experience.

| Persona File                   | Cluster                     | Target Reader & Media                                                  | F | W | H | N | D | T | Active Traits        |
|--------------------------------|-----------------------------|------------------------------------------------------------------------|---|---|---|---|---|---|----------------------|
| `CXO-ADVISOR.md`               | Business & Engineering      | Board, C-suite, PE partners; board memos, capex requests               | 7 | 3 | 1 | 2 | 8 | 5 | TR-08, TR-10, TR-11  |
| `STRATEGIC-THINKER.md`         | Business & Engineering      | Founders, investment committees; theses, position papers               | 5 | 3 | 2 | 4 | 6 | 5 | TR-02, TR-09, TR-11  |
| `SECTOR-COLUMNIST.md`          | Business & Engineering      | Senior practitioners, subscribers; flagship essays, market reports     | 4 | 4 | 4 | 6 | 5 | 5 | TR-01, TR-04, TR-06  |
| `PRINCIPAL-ARCHITECT.md`       | Business & Engineering      | CTOs, tech leads; ADRs, specs, technical diligence                     | 4 | 5 | 2 | 4 | 5 | 5 | TR-03, TR-08, TR-10  |
| `TECHNICAL-WRITER.md`          | Business & Engineering      | Practitioners, cross-functional teams; HOW-TOs, SOPs, playbooks        | 4 | 5 | 1 | 3 | 6 | 3 | TR-07, TR-08, TR-12  |
| `INTELLECTUAL.md`              | Research                    | Educated general readers; science synthesis, trade-book essays         | 4 | 5 | 3 | 7 | 4 | 3 | TR-01, TR-05, TR-09  |
| `JURIST.md`                    | Research                    | Counsel, regulators; legal/tax opinions, statutory analysis            | 8 | 2 | 1 | 2 | 6 | 6 | TR-04, TR-07, TR-10  |
| `ANALYST.md`                   | Research                    | Economists, quant peers; empirical reports, benchmarks                 | 7 | 2 | 1 | 2 | 7 | 6 | TR-07, TR-08, TR-11  |
| `HISTORIAN.md`                 | Research                    | Scholars, case readers; archival case studies, retrospectives          | 6 | 4 | 2 | 8 | 4 | 5 | TR-01, TR-03, TR-06  |
| `BOOK-AUTHOR.md`               | Ebooks, Marketing & Blogs   | Book and ebook readers; multi-chapter playbooks                        | 4 | 6 | 3 | 6 | 4 | 3 | TR-01, TR-09, TR-10  |
| `COACH-MENTOR.md`              | Ebooks, Marketing & Blogs   | Leaders, career/habit builders; leadership and coaching guides         | 3 | 7 | 2 | 5 | 4 | 2 | TR-02, TR-07, TR-12  |
| `PRODUCT-POSITIONER.md`        | Ebooks, Marketing & Blogs   | Skeptical B2B buyers; anti-hype landing pages, launch posts            | 4 | 4 | 2 | 4 | 6 | 4 | TR-08, TR-09, TR-11  |
| `CASE-STORYTELLER.md`          | Ebooks, Marketing & Blogs   | Prospects, internal champions; case studies, before/after proofs       | 4 | 5 | 2 | 7 | 5 | 4 | TR-07, TR-08, TR-11  |
| `PRACTITIONER-BLOGGER.md`      | Ebooks, Marketing & Blogs   | Engineers, builders; tear-downs, build-in-public posts                 | 3 | 4 | 3 | 5 | 5 | 5 | TR-02, TR-03, TR-08  |
| `FOUNDER-ESSAYIST.md`          | Ebooks, Marketing & Blogs   | Founders, operators, generalists; plain-spoken essays                  | 2 | 5 | 3 | 5 | 5 | 2 | TR-02, TR-09, TR-10  |
| `KARSTEN-HELD.md`              | Author-Derived              | Practitioners, team leads; terminology, naming, communication essays   | 3 | 4 | 3 | 5 | 5 | 3 | TR-09, TR-10, TR-14  |
| `JOEL-SPOLSKY.md`              | Author-Derived              | Developers, managers; story-driven software/management essays          | 2 | 6 | 5 | 7 | 4 | 3 | TR-01, TR-03, TR-14  |
| `UX-MANUAL-WRITER.md`          | Gap-Fill (Docs, News, Copy) | First-time end-users; user manuals, help centers, UI microcopy         | 3 | 6 | 0 | 1 | 5 | 1 | TR-07, TR-08, TR-12  |
| `INVESTIGATIVE-JOURNALIST.md`  | Gap-Fill (Docs, News, Copy) | General public, watchdogs; investigative features, data journalism     | 5 | 3 | 1 | 7 | 5 | 4 | TR-01, TR-03, TR-08  |
| `CONVERSION-COPYWRITER.md`     | Gap-Fill (Docs, News, Copy) | Cold prospects; landing pages, direct-response and lifecycle emails    | 2 | 7 | 2 | 4 | 5 | 3 | TR-08, TR-09, TR-11  |

Clusters: `Business & Engineering` (decision, strategy, and engineering reports), `Research` (academic, legal, empirical, historical), `Ebooks, Marketing & Blogs` (books, coaching, anti-hype marketing, blogging), `Author-Derived` (calibrated from a real public text corpus), `Gap-Fill (Docs, News, Copy)` (user documentation, investigative journalism, direct-response copy; added by `DRSYNART-WRTSTYLTCH-IN03`). Each persona file uses the same cluster name in its `Category` field.

## 5. When to Use Which Persona

Use this section ONLY when the user asks for style or persona help (`DRSYNART-DD-08`).

### 5.1 By Media / Output Type

- **Technical Documentation** (Application Programming Interface (API) guides, SOPs, ADRs, specs, release notes for practitioners)
  - `TECHNICAL-WRITER`: Reader executes a professional procedure for the first time
  - `PRINCIPAL-ARCHITECT`: Reader decides a design trade-off (ADR, build-vs-buy, diligence)
  - Typical techniques: `DIATAXIS`, `IMINTO` (release notes), `STA`
- **User Manuals & UX Help** (onboarding guides, help-center articles, error messages, tooltips)
  - `UX-MANUAL-WRITER`: Non-technical first-time end-user who wants to finish one action now
  - `TECHNICAL-WRITER`: Only when the reader is an admin or practitioner who needs domain vocabulary
  - Typical techniques: `DIATAXIS`
- **Marketing & Landing Pages** (website pages, product pages, emails, ads, launch posts)
  - `CONVERSION-COPYWRITER`: Cold or problem-aware prospects; direct response with one call to action
  - `PRODUCT-POSITIONER`: Skeptical B2B evaluators comparing against spreadsheets or in-house builds
  - `CASE-STORYTELLER`: Proof pages and customer stories with measured before/after numbers
  - Typical techniques: `PAS`, `KABOB` (case studies)
- **Business & Board Reports** (decision briefs, strategy papers, budget requests)
  - `CXO-ADVISOR`: Reader must approve, reject, or re-scope a quantified decision
  - `STRATEGIC-THINKER`: Reader places a long-term bet and needs consensus stress-tested
  - `ANALYST`: Reader audits evidence before deciding (benchmarks, cohort analyses)
  - Typical techniques: `MINTO`, `IMINTO` (executive briefs)
- **Flagship Articles & Columns** (industry essays, newsletters, whitepapers, feature articles)
  - `SECTOR-COLUMNIST`: Senior insiders reading voluntarily for synthesis and a memorable model
  - `INTELLECTUAL`: Broad educated audience; science or ideas made vivid
  - `INVESTIGATIVE-JOURNALIST`: Verified-fact narrative, accountability, data journalism
  - `JOEL-SPOLSKY` / `KARSTEN-HELD`: Opinionated software, naming, or team essays from first-hand experience
  - Typical techniques: `MINTO`, `KABOB`, `ABTSTORY`
- **Empirical / Legal / Historical Research** (papers, opinions, retrospectives)
  - `ANALYST`: Quantitative studies, error margins, identification strategy
  - `JURIST`: Statutory text, precedent, burden of proof
  - `HISTORIAN`: Chronological reconstruction from primary records
  - `INTELLECTUAL`: Public-facing synthesis of research for non-specialists
  - Typical techniques: `IMRAD`, `MINTO` (legal memos)
- **Nonfiction Ebooks & Coaching** (books, paid ebooks, course companions, leadership guides)
  - `BOOK-AUTHOR`: Craft or framework mastery across chapters
  - `COACH-MENTOR`: Reader is blocked by fear, habit, or an awkward conversation, not by missing knowledge
  - Typical techniques: `STA`, `ABTSTORY`
- **Engineering & Founder Blogs** (tear-downs, build-in-public, opinion essays)
  - `PRACTITIONER-BLOGGER`: Real benchmarks, dead ends, and the actual bug
  - `FOUNDER-ESSAYIST`: Counter-intuitive lessons in plain everyday words
  - `JOEL-SPOLSKY`: Story-first, comedic, bottom-up explanation of engineering or management truths
  - `KARSTEN-HELD`: Structured practitioner essays on terminology, naming, and communication
  - Typical techniques: `ABTSTORY`, `STA`, `IMINTO`

### 5.2 By Audience Psychology

- **"Approve, reject, or re-scope?"** (decides between meetings) → `CXO-ADVISOR`
- **"Where is the consensus wrong?"** (places long-term bets) → `STRATEGIC-THINKER`
- **"Can I trust this evidence?"** (audits method and sources) → `ANALYST`, `JURIST`, `HISTORIAN`, `INVESTIGATIVE-JOURNALIST`
- **"What breaks at 2 a.m.?"** (weighs design trade-offs) → `PRINCIPAL-ARCHITECT`, `PRACTITIONER-BLOGGER`
- **"How do I do this right now?"**
  - Capable practitioner → `TECHNICAL-WRITER`
  - Frustrated first-time end-user → `UX-MANUAL-WRITER`
- **"Teach me something worth my reading time"** (voluntary reader) → `SECTOR-COLUMNIST`, `INTELLECTUAL`, `FOUNDER-ESSAYIST`, `JOEL-SPOLSKY`, `KARSTEN-HELD`
- **"Help me master this over several hours"** → `BOOK-AUTHOR`
- **"I know what to do but I keep avoiding it"** → `COACH-MENTOR`
- **"What is in it for me?"** (cold, skeptical prospect deciding in seconds) → `CONVERSION-COPYWRITER`
- **"Show me it works for a company like mine"** → `CASE-STORYTELLER`, `PRODUCT-POSITIONER`

### 5.3 Commonly Confused Pairs

- **`TECHNICAL-WRITER` vs. `UX-MANUAL-WRITER`**: Practitioner learning domain vocabulary (Technicality 3) vs. end-user who should never see jargon (Technicality 1, Humor 0, Narrative 1)
- **`PRODUCT-POSITIONER` vs. `CONVERSION-COPYWRITER`**: Anti-hype B2B evaluation (Formality 4, Warmth 4) vs. direct-response urgency for cold prospects (Formality 2, Warmth 7)
- **`SECTOR-COLUMNIST` vs. `INTELLECTUAL`**: Industry insiders and competitive advantages (Technicality 5) vs. broad audience and fundamental science (Technicality 3, Narrative 7)
- **`SECTOR-COLUMNIST` vs. `HISTORIAN`**: One-sentence historical parallel inside a modern essay (Narrative 6) vs. chronology as the main structure of the whole text (Narrative 8)
- **`INVESTIGATIVE-JOURNALIST` vs. `SECTOR-COLUMNIST`**: Reported, sourced fact chain with named gaps vs. authored opinion and synthesis
- **`FOUNDER-ESSAYIST` vs. `JOEL-SPOLSKY`**: Calm philosophical plainness (Humor 3) vs. warm, theatrical, story-first comedy (Humor 5, Narrative 7)

## 6. Reference Catalog: 6 Sliders and 14 Micro-Dosed Traits

### 6.1 The 6 Continuous Sliders (0-10, 5 Behavioral Bands)

- **Formality** (social distance, pronouns, syntactic register)
  - 0-1 Intimate chat: first name, conversational particles, contractions, reaction fragments
  - 2-3 Direct peer: reader addressed as "you", active verbs, natural contractions, zero bureaucratic nouns
  - 4-6 Professional accessible: clean standard prose, inclusive "we" or polite "you", no slang, no stiff noun chains
  - 7-8 Executive formal: measured vocabulary, structured transitions, formal address, zero colloquialisms
  - 9-10 Academic/statutory: impersonal constructions, domain-standard passive voice, institutional register
- **Warmth** (stance toward the reader's situation; stance, not emotional fluff)
  - 0-1 Clinical: object-level facts only, reader's obstacles never mentioned
  - 2-3 Matter-of-fact courteous: task-focused, acknowledges practical constraints without emotional framing
  - 4-6 Supportive peer: acknowledges real friction at transitions, puts failure rates in perspective, reduces stress
  - 7-8 Coaching: warm and reassuring, validates setbacks, celebrates progress
  - 9-10 Pastoral: emotional resonance and personal support are the primary goal
- **Humor & Color** (wit, irony, metaphor; most sensitive slider, needs hard caps)
  - 0 Strictly literal: zero metaphors, zero irony
  - 1-2 Dry understatement: max 1 dry observation per 300-500 word section, 0 extended metaphors, 0 exclamation jokes
  - 3-4 Light wit: 1-2 everyday analogies or wry asides per section, each explaining a mechanism
  - 5-6 Conversational wit: noticeable wordplay and humorous framing in every paragraph, balanced with information
  - 7-10 Satire: punchlines dominate (not used by any persona in this library)
- **Narrative Drive** (ratio of story to exposition)
  - 0-1 Pure inventory: zero scenes, zero hooks; start with scope or summary
  - 2-3 Expository with case proof: direct argument; named cases cited in 1-2 compact sentences
  - 4-5 Scene-anchored guide: 3-sentence situation hook, real cases in 3-4 sentences, then rule and action; no decorative filler
  - 6-7 Case-led feature: each major section built around a protagonist or case, rules woven in
  - 8-10 Documentary story: chronological arc, exposition subordinated to plot
- **Density** (information per sentence, breathing room)
  - 0-2 Spacious/didactic: one idea per sentence, frequent recaps, gentle transitions
  - 3-4 Relaxed editorial flow: smooth transitions, room for brief context, unhurried pacing
  - 5-6 Crisp and focused: zero parenthetical tangents (except a micro-dosed TR-03), every sentence advances the point, complete grammar
  - 7-8 Executive brief: tightly packed clauses, high fact-per-sentence ratio, minimal transitions, complete grammar
  - 9-10 Telegraphic log mode: articles and pronouns dropped; forbidden in reader-facing text
- **Technicality** (jargon allowance and inline explanation)
  - 0-1 Zero jargon: everyday words only, technical concepts replaced by plain descriptions
  - 2-3 Guided practitioner: authentic domain terms, each non-obvious term explained in 3-6 plain words on first use
  - 4-6 Informed practitioner: standard domain vocabulary unexplained; only niche terms briefly glossed
  - 7-8 Domain expert: full terminology and acronyms at speed
  - 9-10 Specialist peer: dense formal notation assumed known

**Precedence rules when sliders conflict:**
1. Technicality 2-3 overrides Density 5-7 on first-use definitions: never cut the 3-6 word gloss of a new term
2. Density 5-7 caps Narrative 4-6 length: keep cases and hooks, compress each to 2-3 sentences without atmospheric filler
3. Formality 7-8 reshapes Warmth 4-6: express warmth by anticipating risks and removing friction, never by slang or exclamation marks

### 6.2 The 14 Micro-Dosed Traits (TR-01..14)

- **Cluster A: Cognitive Threading**
  - `TR-01` Sub-Thought Callback (max 1/article): Plant a 4-8 word comparison inside a sentence, echo the same image in 3-5 words two or more paragraphs later
  - `TR-02` Mid-Sentence Self-Correction (max 1/article): Pivot with "-- or rather," from the polite excuse to the real cause in under 10 words
  - `TR-03` Dry Parenthetical Aside (max 1 per 600 words): One 4-9 word parenthetical stating an unspoken practical reality
- **Cluster B: Erudition That Teaches**
  - `TR-04` Classic Bonmot with Inline Gloss (max 1/article): One maxim or foreign phrase glossed in 2-4 words in parentheses
  - `TR-05` Etymological Root Gloss (max 1/article): A key word's literal root in 3-6 words to sharpen a distinction
  - `TR-06` One-Sentence Historical Parallel (max 1/article): A verified precedent in max 20 words that mirrors the mechanism
- **Cluster C: Candid Stance & Reader Alignment**
  - `TR-07` Pre-Emptive Reader Objection (max 1 per 500 words): Name the reader's rational doubt in the opening clause, answer with a concrete number
  - `TR-08` The Catch (max 1 per major recommendation): One sentence starting "The catch:" stating where the recommendation fails or costs extra
  - `TR-09` Myth-First Contrast (max 1/article): "Standard instinct says X; in practice, Y" in one sentence
- **Cluster D: Precision & Action Signatures**
  - `TR-10` The Colon Law (max 1 per 400 words): Hinge one takeaway on a colon: [concrete fact] : [short rule]
  - `TR-11` Inline Sanity Math (max 1-2/article): Replace vague cost or time adjectives with inline arithmetic (X min x Y runs = Z hours/week)
  - `TR-12` One-Line Verification Step (max 1/article, at section close): One sentence starting "Quick check:" that takes under 15 minutes
- **Cluster E: Corpus-Derived Signatures**
  - `TR-13` Mimetic Chain (max 1/article): Chain the real nested parts of a tangled structure in one long sentence, then a verdict of 6 words or fewer; replaces a sentence instead of adding words
  - `TR-14` Coined Handle (max 1 coinage/article): Name a recurring concept with a 1-3 word everyday phrase, define it in the same sentence, reuse the exact phrase at least twice

**Excluded on purpose** (LLM cliche or fabrication risk): Socratic pivot questions, zoom-lens invented micro-details, rule-of-three lists. Merged into the baseline: conversational onsets, tactile verbs, long-to-short snaps.

## Document History

**[2026-10-29 16:15]**
- Changed: Section 2 renamed to "User-Only Selection Rule"; default without persona = standard workflow instructions, templates, GRUC files; partial input never auto-completed (DRSYNART-DD-08 revision)

**[2026-10-29 16:20]**
- Fixed: Acronyms expanded (LLM, API, abbreviation legend above the table), diagram abbreviation removed, Section 5.3 short slider labels replaced with full names, figurative phrases replaced (MW-WC-10)

**[2026-10-29 15:50]**
- Initial: README with architecture, DRSYNART-DD-08 unbiased default, 20-persona table, media-type and audience selectors, slider and trait reference
