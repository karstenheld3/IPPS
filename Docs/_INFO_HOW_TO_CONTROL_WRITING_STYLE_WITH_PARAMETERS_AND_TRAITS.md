# INFO: How to Control Writing Style with Parameters and Traits

**Doc ID**: DOCWRITEFW-IN01
**Goal**: Define a zero-fluff framework for steering and rewriting LLM text using 6 continuous sliders (0 to 10) plus up to 3 micro-dosed ON/OFF authorial voice traits (12 curated from a 20-trait brainstorm, plus 2 derived from a real author corpus), complete with before/after examples, AI anti-patterns, and copy/paste persona presets

**Related documents:**
- [`_INFO_HOW_TO_DETECT_AI_ASSISTED_WRITING.md [AIDET-IN01]`](_INFO_HOW_TO_DETECT_AI_ASSISTED_WRITING.md) - The five AI-writing signal categories (`SO`, `SY`, `ST`, `VO`, `LX`) that uncalibrated style prompts trigger
- [`_INFO_HUMAN_WRITING_PATTERNS.md [HMNWRTPTN-IN01]`](_INFO_HUMAN_WRITING_PATTERNS.md) - Forensic linguistics research on burstiness, discourse markers, and idiolect consistency
- [`_INFO_APAPALAN_PRINCIPLE.md [APAPALAN-IN01]`](_INFO_APAPALAN_PRINCIPLE.md) - Precision and brevity baseline for agent logs and technical specs

## Summary

- **Zero-Bullshit Law (The Iron Imperative)**: Every style setting is subordinate to one rule: **treat the reader's time as more valuable than your own** ([Bernoff 2016](https://bernoff.com/wp-content/uploads/2023/05/Writing-Without-Bullshit-Book-Chapter-1.pdf); [Zinsser 2006](http://richardcolby.net/writ2000/wp-content/uploads/2017/09/On-Writing-Well-30th-Anniversa-Zinsser-William.pdf)). Style never means padding. Any sentence, metaphor, or trait that does not carry a fact, clarify a mechanism, or help the reader decide is deleted [PROVEN] (DOCWRITEFW-IN01-SC-BERN-IRON16; DOCWRITEFW-IN01-SC-ZINSS-CLUT06)
- **Three-Layer Architecture**: A complete **Writer Profile** combines: 1) a **3-line Persona Header** (`Role`, `Audience`, `Anti-Tone`), 2) **6 Continuous Sliders (`0 = None` to `10 = Max`)** that govern the macro-register (**Formality**, **Warmth**, **Humor & Color**, **Narrative Drive**, **Density**, **Technicality**), and 3) **1 to 3 binary `ON/OFF` Authorial Voice Traits (`TR-01..14`)** that inject human character in micro-doses [VERIFIED]
- **Why LLMs Overdo Style ("Generative Exaggeration" & Caricature)**: Empirical LLM persona research ([CoMPosT EMNLP 2023](https://aclanthology.org/2023.emnlp-main.669/); [PANDA EMNLP 2024](https://doi.org/10.18653/v1/2024.emnlp-main.670); [Generative Exaggeration 2025, arXiv:2507.00657](https://arxiv.org/html/2507.00657); [SCONPOS EMNLP 2026](https://aclanthology.org/2026.emnlp-main.2029/)) proves that LLMs systematically **overuse persona traits by 5x-10x compared to humans**, forcing every enabled quirk into every paragraph regardless of context. When an LLM fires a quirk twice in a row, readers immediately detect it as an artificial tic [PROVEN] (DOCWRITEFW-IN01-SC-EMNLP-COMPOST23; DOCWRITEFW-IN01-SC-EMNLP-PANDA24; DOCWRITEFW-IN01-SC-ARXV-EXAGG25; DOCWRITEFW-IN01-SC-EMNLP-SCONPOS26)
- **The Micro-Dose Budget (`<= 5%` of Sentences)**: To prevent caricature and detection, **95% of sentences must be clean, direct, invisible prose** governed only by the 6 sliders. Active `ON` traits are restricted to **at most 1 trait occurrence per 300-400 words** (2-4 total trait moments across a 1,200-word article), and **two traits must never fire in the same paragraph** [VERIFIED]
- **Curated 14-Trait Catalog (12 Brainstormed + 2 Corpus-Derived; 8 Dropped)**: We pruned the initial 20-trait brainstorm down to **12 orthogonal, information-carrying traits (`TR-01..12`)**. Five traits that restated existing sliders or other traits (*Conversational Onsets*, *Tactile Verbs*, *Long-to-Short Snap*, *Cross-Domain Analogy*, *100x Reductio*) were merged, and three traits that tempted AI clichés or fabrication (*Socratic Pivot Question*, *Zoom-Lens Micro-Detail*, *Rule-of-Three*) were dropped (documented in Section 2.7). Two further traits, **`TR-13` Mimetic Chain** and **`TR-14` Coined Handle**, were extracted from a real practitioner essay (Section 2.6, Section 5.16) because no slider or existing trait could reproduce them [VERIFIED]

## Diagrams

```
┌──────────────────────────────────────────────────────────────────────────────────────┐
│              WRITER PROFILE = ZERO-BS BASELINE + 6 SLIDERS + 1-3 TRAITS              │
├──────────────────────────────────────────────────────────────────────────────────────┤
│  1. Universal Zero-Bullshit Gate (Iron Imperative + Zinsser Bracket Test)            │
│     └─> Every sentence must advance a fact, mechanism, or decision. 0 throat-clearing│
├──────────────────────────────────────────────────────────────────────────────────────┤
│  2. Persona Header                                                                   │
│     ├─> Role: Who is speaking (e.g., "Experienced practitioner peer")                │
│     ├─> Audience: Who is reading & prior knowledge                                   │
│     └─> Anti-Tone: What to strictly avoid (e.g., "No hype, no SY-01 staccato")       │
├──────────────────────────────────────────────────────────────────────────────────────┤
│  3. Six Continuous Sliders (Governs 95% of sentences; 5 behavioral bands)            │
│     ├─> Formality     [0 Casual Chat      ───────●────────── 10 Institutional/Legal] │
│     ├─> Warmth        [0 Cold/Detached    ──────────●─────── 10 Deeply Empathetic]   │
│     ├─> Humor & Color [0 Strictly Literal ───●────────────── 10 Satirical/Metaphor]  │
│     ├─> Narrative     [0 Pure Checklist   ────────●───────── 10 Scene-by-Scene Story]│
│     ├─> Density       [0 Spacious/Guided  ──────────●─────── 10 Telegraphic/Log Mode]│
│     └─> Technicality  [0 Layperson/Plain  ───────●────────── 10 Unexplained Jargon]  │
├──────────────────────────────────────────────────────────────────────────────────────┤
│  4. Micro-Dosed Character Traits (Select 1-3 ON from TR-01..14; <= 5% of sentences)  │
│     ├─> [ON]  TR-01 Sub-Thought Callback (Max 1/article: aside -> red thread -> echo)│
│     ├─> [ON]  TR-04 Explained Classic Bonmot (Max 1/article: 2-4 word gloss in-line) │
│     ├─> [ON]  TR-08 Candid Trade-Off ("The catch:" - 1 sentence on where it fails)   │
│     └─> Dosing Rule: Max 1 trait firing per 300-400 words. Never 2 in one paragraph. │
└──────────────────────────────────────────────────────────────────────────────────────┘
```

## Table of Contents

1. [The 6-Parameter Style Sliders (0 to 10) & Zero-Bullshit Baseline](#1-the-6-parameter-style-sliders-0-to-10--zero-bullshit-baseline)
2. [Curated Catalog of 14 Micro-Dosed Authorial Traits (`TR-01` to `TR-14`)](#2-curated-catalog-of-14-micro-dosed-authorial-traits-tr-01-to-tr-14)
3. [Good Patterns vs. AI Anti-Patterns](#3-good-patterns-vs-ai-anti-patterns)
4. [Same Fact Across 5 Personas (6 Sliders + Micro-Dosed Traits)](#4-same-fact-across-5-personas-6-sliders--micro-dosed-traits)
5. [Market-Derived Persona Catalog (17 Personas)](#5-market-derived-persona-catalog-17-personas)
6. [Prompt Template and Re-Writing Controls](#6-prompt-template-and-re-writing-controls)
7. [Scientific and Industry Backing](#7-scientific-and-industry-backing)
8. [Sources](#8-sources)

## 1. The 6-Parameter Style Sliders (0 to 10) & Zero-Bullshit Baseline

A complete Writer Profile consists of a **3-line Persona Header** (`Role`, `Audience`, `Anti-Tone`), **6 sliders from 0 to 10**, and **1 to 3 micro-dosed traits**. Because LLMs cannot distinguish single-integer steps (`4` vs `5`) without a rubric ([arXiv:2610.22187](https://arxiv.org/html/2610.22187)), the 0-to-10 scale is divided into **five 2-point behavioral bands** (`0-1`, `2-3`, `4-6`, `7-8`, `9-10`). When prompting an LLM, always include the **short band rule in parentheses** next to the number.

### 1.1 Universal Zero-Bullshit Baseline (Applies at ALL Slider Settings 0-10)

Style is **how** you deliver value, never a substitute for value. Before any slider or trait takes effect, every paragraph must pass four non-negotiable gates:

1. **The Iron Imperative (Never Waste the Reader's Time)**: Treat the reader's time as more valuable than your own ([Bernoff 2016](https://bernoff.com/wp-content/uploads/2023/05/Writing-Without-Bullshit-Book-Chapter-1.pdf)). Never write throat-clearing introductions (*"In today's fast-paced world..."*, *"Before we dive in, it is worth reflecting on..."*), empty transitions (*"Moving on to the next point..."*), or recap paragraphs that repeat what was just said. Start every section with the point or the concrete problem.
2. **Zinsser's Bracket Test (Information-Bearing Style Only)**: Put mental brackets around every word, aside, or metaphor that is not doing useful work ([Zinsser 2006](http://richardcolby.net/writ2000/wp-content/uploads/2017/09/On-Writing-Well-30th-Anniversa-Zinsser-William.pdf)). An analogy, bonmot, or aside is allowed **only if it compresses a real mechanism, constraint, or trade-off** so the reader understands it faster than literal prose alone. Purely decorative "color" is bullshit -- cut it.
3. **Natural Grammar & Plain Connectives**: Write complete, idiomatic sentences in the target language (`Density: 0-8`). Never invent unnatural collocations (such as blending "unheard voicemails" and "unread messages" into *"unheard messages"*). Prefer plain connectives (*but, so, still, yet*) over stiff conjunctive adverbs (*Furthermore, Consequently, Moreover* - `LX-03`), and prefer concrete action verbs (*strip out, wire up, block*) over Latinate filler (*facilitate, utilize, optimize* - `LX-01`).
4. **Sentence Rhythm (Burstiness) & Fact Integrity (`SO-01`, `SO-03`)**: Alternate short single-clause statements (5-9 words) with longer multi-clause explanations (18-28 words). Never write 3+ choppy fragments or uniform-length sentences in a row (`SY-01`). Style sliders change *how* claims are framed, never *what* the evidence says. When the source contains the literal identifier, label, command, or string (`"OMON"`, `"Info Measurement Module"`), quote it verbatim instead of paraphrasing it; never invent a specimen that is not in the source.

### 1.2 Parameter 1: Formality (`0 = Casual Peer` to `10 = Institutional / Academic`)

Controls social distance, pronoun choice, and syntactic register.

- **0-1 (Intimate / Chat)**: First name, conversational particles (*well, actually, anyway*), contractions, brief reaction fragments allowed.
- **2-3 (Direct Peer - Conversational "You")**: Reader addressed directly as *you*, active verbs, natural contractions, zero bureaucratic nominalizations.
- **4-6 (Professional Accessible)**: Clean standard prose, inclusive *we* or polite *you*, no slang, no stiff noun chains (*"Perform an installation of"* → *"Install"*).
- **7-8 (Executive / Corporate Formal)**: Measured vocabulary, structured transitions, third-person or formal address, zero colloquialisms.
- **9-10 (Academic / Statutory)**: Impersonal constructions, domain-standard passive voice where required (e.g., IMRaD Methods section), strict institutional register.

**Examples (Formality):**
- **`Formality: 2` (Direct Peer)**: *"Upload your config file through the web dashboard and skip the manual server setup."*
- **`Formality: 5` (Professional Accessible)**: *"Submit your configuration file through the web dashboard; manual server provisioning is not required."*
- **`Formality: 9` (Academic / Institutional)**: *"Configuration parameters must be transmitted exclusively via the designated web interface; manual server-side modifications are rejected by the deployment pipeline."*

### 1.3 Parameter 2: Warmth & Empathy (`0 = Detached` to `10 = Deeply Empathetic`)

Controls how strongly the writer acknowledges the reader's situation, frustration, and effort. **Warmth is stance (taking the reader's side and removing friction), not emotional fluff (`VO-03`).**

- **0-1 (Clinical / Detached)**: Pure object-level facts. Reader's obstacles or feelings are never mentioned.
- **2-3 (Matter-of-Fact Courteous)**: Respectful and task-focused; acknowledges practical constraints without emotional framing.
- **4-6 (Supportive Peer - Nonfiction Sweet Spot)**: Acknowledges real friction at transition points, puts high rejection or failure rates into reassuring perspective, and designs steps that reduce stress.
- **7-8 (Coaching / Mentoring)**: Warm, reassuring, explicitly validates setbacks and celebrates progress.
- **9-10 (Intimate / Pastoral)**: Emotional resonance and personal support are the primary goal.

**Examples (Warmth):**
- **`Warmth: 1` (Detached)**: *"Eighty percent of initial patent filings receive an office action rejecting at least one claim. Filings without a response within ninety days are marked abandoned."*
- **`Warmth: 5` (Supportive Peer)**: *"Four out of five initial patent filings get pushed back on the first review. That looks intimidating on paper, but most examiner objections target overly broad wording rather than the core invention -- and you have a full ninety-day window to narrow the claims."*
- **`Warmth: 9` (High-Empathy Coaching)**: *"It is completely normal to feel deflated when your first examiner report comes back full of red ink after months of hard work. Don't let that discourage you: almost every granted patent started with a first-round rejection."*

### 1.4 Parameter 3: Humor & Figurative Color (`0 = Strictly Literal` to `10 = Satirical / Metaphor-Heavy`)

Controls wit, irony, metaphors, and colourful asides. **This is the most sensitive slider for LLMs and requires hard frequency caps.**

- **0 (Strictly Literal)**: Zero metaphors, zero irony, zero rhetorical winks. Every word is denotative.
- **1-2 (Dry Understatement - Nonfiction Sweet Spot)**: **Max 1 brief dry observation or deadpan contrast per major section (300-500 words). Zero extended metaphors, zero exclamation-mark jokes.** Wit comes from stating an uncomfortable truth plainly.
- **3-4 (Light Wit & Occasional Analogy)**: 1-2 everyday analogies or wry asides per section; playful subheadings allowed if informative.
- **5-6 (Entertaining / Conversational Wit)**: Noticeable wordplay, vivid imagery, and humorous framing in every paragraph, balanced with information.
- **7-10 (Roast / Satire / Comedy)**: Figurative exaggeration and punchlines dominate the text.

**Examples (Humor & Figurative Color):**
- **`Humor: 0` (Strictly Literal)**: *"Across 400 paid fast-track vendor listings, 95 received profile clicks, but only 3 resulted in a signed procurement contract."*
- **`Humor: 2` (Dry Understatement)**: *"Paid vendor directories can occasionally land a lead, but they mostly operate like an expensive raffle where a polite automated badge already counts as winning."*
- **`Humor: 8` (Satirical / Over-Seasoned)**: *"Paid vendor directories are basically coin-operated ego-massage machines: you feed in fifty dollars, a bot awards you a shiny 'Top Innovator!' sticker, and your proposal still goes straight into the corporate shredder."*

### 1.5 Parameter 4: Narrative Drive (`0 = Pure Reference` to `10 = Scene-by-Scene Story`)

Controls the ratio of storytelling (scenes, named protagonists, chronological cases) to direct exposition.

- **0-1 (Pure Inventory / Checklist)**: Zero scenes, zero narrative hooks. Starts directly with scope or summary bullets.
- **2-3 (Expository with Case Proof)**: Direct argument structure (SCQA); named cases are cited in 1-2 compact sentences as proof without scenic staging.
- **4-5 (Scene-Anchored Guide - Show-Tell-Apply)**: Opens with a 3-sentence recognizable situation hook, uses 1 compact concrete mini-scene where helpful, and tells real cases in 3-4 sentences before extracting the rule and action steps. **No decorative filler (no weather, beverage temperature, or fictional dialogue).**
- **6-7 (Case-Led Feature Article)**: Each major section is built around a protagonist's journey or case study, with rules woven into the narrative.
- **8-10 (Pure Narrative / Documentary Story)**: Chronological story arc from start to finish; exposition is subordinated to plot and character.

**Examples (Narrative Drive):**
- **`Narrative: 1` (Inventory)**: *"Open municipal design competitions allow small architecture studios to win public contracts (e.g., Jane Smith Studio 2024, NordBuild 2025)."*
- **`Narrative: 4` (Scene-Anchored Guide)**: *"When the city opened an anonymous design competition for its new library wing in 2025, an unknown two-person studio submitted a timber-frame proposal and won. Six months later, their design broke ground ahead of three international firms."*
- **`Narrative: 8` (Feature Story)**: *"At ten minutes to midnight, Jane Smith clicked 'Submit' on the municipal portal, convinced her two-person studio stood no chance against the fifty-architect firms downtown. Yet when the jury unsealed the numbered envelopes the following Thursday, her timber model was sitting in the center of the table..."*

### 1.6 Parameter 5: Density & Pacing (`0 = Spacious & Guided` to `10 = Ultra-Compressed`)

Controls information per sentence, parenthetical side-notes, and structural breathing room.

- **0-2 (Spacious / Didactic)**: One idea per sentence, frequent recaps, gentle transitions, ample whitespace.
- **3-4 (Relaxed Editorial Flow)**: Smooth transitions between paragraphs, room for brief context, unhurried pacing.
- **5-6 (Crisp & Focused - Nonfiction Sweet Spot)**: **Zero parenthetical tangents or side-remarks** (the only exception is a micro-dosed `TR-03` aside, Section 2.2). Every sentence advances the argument, the evidence, or the action step, while maintaining complete, fluid grammar.
- **7-8 (High-Density Executive Brief)**: Tightly packed clauses, high fact-per-sentence ratio, minimal transition sentences, complete grammar preserved.
- **9-10 (Telegraphic / APAPALAN Log Mode)**: Maximum compression; articles and pronouns may be dropped (`AP-BR-02`). **Reserved for internal agent tracking (`NOTES.md`, `PROGRESS.md`); forbidden in reader-facing articles.**

**Examples (Density):**
- **`Density: 2` (Spacious / Didactic)**: *"Before you run the database migration, always create a fresh snapshot first. Why does this matter? Because if a schema change fails halfway through, you will need a clean restore point so you don't lose customer records."*
- **`Density: 5` (Crisp & Focused)**: *"Create a database snapshot before running the migration so you can roll back immediately if a schema change fails."*
- **`Density: 9` (Telegraphic / Agent Log)**: *"Snapshot DB before migration (enables instant rollback on schema failure)."*

### 1.7 Parameter 6: Technicality (`0 = Layperson` to `10 = Specialist Insider`)

Controls domain jargon allowance and inline explanation depth.

- **0-1 (Zero Jargon)**: Everyday words only; technical concepts are replaced by plain descriptions.
- **2-3 (Guided Practitioner - Explain on First Use)**: Uses authentic domain terms so the reader learns the vocabulary, but **explains every non-obvious term in 3-6 plain words on first mention**.
- **4-6 (Informed Practitioner)**: Standard domain vocabulary used without explanation; only niche legal, mathematical, or institutional terms are briefly glossed.
- **7-8 (Domain Expert)**: Full professional terminology, acronyms, and methodological terms used at speed.
- **9-10 (Specialist Peer)**: Dense formal notation and specialist terminology assumed known.

**Examples (Technicality):**
- **`Technicality: 1` (Zero Jargon)**: *"Make sure your server can handle receiving the same payment request twice without charging the customer's card a second time."*
- **`Technicality: 3` (Guided Practitioner)**: *"Make sure your payment endpoint is idempotent (meaning duplicate requests produce the exact same result without charging the customer twice)."*
- **`Technicality: 8` (Domain Expert)**: *"Enforce idempotency on `POST /v1/charges` via client-supplied `Idempotency-Key` headers persisted in Redis with a 24-hour time-to-live (TTL)."*

### 1.8 Parameter Interactions and Precedence Rules (Disentanglement)

Empirical research on LLM style steering ([CASSE 2026, arXiv:2601.10809](https://arxiv.org/html/2601.10809)) proves that style attributes are **entangled in latent space**: prompting an LLM to be "concise" (`Density: 7-8`) automatically causes it to drop explanations and perceived expertise, while prompting for "formal" (`Formality: 7-8`) suppresses warmth. When two sliders pull in opposite directions, enforce these three precedence rules:

1. **`Technicality (2-3)` overrides `Density (5-7)` on first-use definitions**: High density cuts conversational tangents and filler adverbs, **never** the 3-to-6-word inline explanation of a new technical term.
2. **`Density (5-7)` caps `Narrative Drive (4-6)` length**: When both are active, keep concrete cases and hooks, but compress each case to 2-3 crisp sentences with zero atmospheric filler.
3. **`Formality (7-8)` reshapes `Warmth (4-6)`**: In formal prose, express warmth by anticipating reader risks, stating clear remedies, and removing procedural friction -- never by switching to casual slang or chatty exclamation marks.

## 2. Curated Catalog of 14 Micro-Dosed Authorial Traits (`TR-01` to `TR-14`)

While the 6 sliders control the **continuous macro-register** across 95% of sentences, human writers are recognizable by **a small, recurring repertoire of cognitive and rhetorical moves** ([`HMNWRTPTN-IN01`](_INFO_HUMAN_WRITING_PATTERNS.md); [Medical Education Voice Repertoire 2024](https://asmepublications.onlinelibrary.wiley.com/doi/10.1111/medu.15298); [Brevity Craft Essays](https://brevitymag.com/craft-essays/on-the-aside-looking-in/)).

### 2.1 The Micro-Dose & Subtlety Law (Preventing LLM Caricature and Time-Wasting)

Empirical studies on persona-assigned LLMs ([CoMPosT EMNLP 2023](https://aclanthology.org/2023.emnlp-main.669/); [PANDA EMNLP 2024](https://doi.org/10.18653/v1/2024.emnlp-main.670); [Generative Exaggeration 2025](https://arxiv.org/html/2507.00657); [SCONPOS EMNLP 2026](https://aclanthology.org/2026.emnlp-main.2029/)) demonstrate that when an LLM is given a stylistic quirk, it suffers from **generative exaggeration** -- firing the quirk 5x to 10x more often than a real human author and over-explaining the joke or quote until it wastes the reader's time. Enforce four strict rules:

1. **The 95/5 Budget (`<= 5%` of Sentences)**: At least **95% of sentences must be clean, direct, unmannered prose** governed solely by the 6 sliders. Active traits may touch **at most 1 sentence out of every 20 (roughly 1 trait firing per 300-400 words)**.
2. **Subtlety & Word-Addition Ceiling (`<= 10` Extra Words)**: A trait must never hijack the paragraph or introduce unrelated trivia. Inline translations (`TR-04`), etymologies (`TR-05`), or parentheticals (`TR-03`) must be woven **inside the existing sentence in 2 to 10 words** -- never as a separate lecturing sentence (*"In plain English, what this famous quote means is..."*). The only exception is `TR-13` (*Mimetic Chain*), which replaces one sentence rather than adding to it and is capped at 1 per article.
3. **Hard Per-Article Cap & No Stacking**: Across an entire 1,200-word article, fire **only 2 to 4 trait moments in total**, and **never place two traits in the same paragraph**.
4. **Zero-Distraction Gate**: A trait may fire **only** if it sharpens the exact point being made. If the reader has to stop and wonder why climbing ropes or 19th-century telegraphs are being discussed, the trait is overdone -- cut it.

### 2.2 Cluster A: Cognitive Threading (`TR-01` to `TR-03`)

#### `TR-01`: Sub-Thought Callback (Brief Comparison → Red Thread → Later 3-Word Echo)
- **What it does**: Touches a concrete comparison in 4-8 words without leaving the sentence, returns immediately to the red thread, and **echoes that exact image in 3-5 words** several paragraphs later to close the loop.
- **LLM Prompt Instruction**: `"[ON] TR-01 (Max 1/article): Plant one brief 4-8 word comparison inside a sentence, stay on the main point, and echo that same image in 3-5 words two paragraphs later. Never write a separate tangent sentence."`
- **`OFF` (Standard Linear)**:
  > *"Automated integration tests catch schema regressions before deployment, yet teams often skip them under deadline pressure. ... [3 paragraphs later] ... Skipping that final pre-cutover check means deploying blind when traffic is highest."*
- **`ON` (Subtle 6-Word Plant + 4-Word Echo)**:
  > *"Automated integration tests act like a pre-flight check on your reserve chute, yet teams routinely skip them to save twenty minutes before a deadline. ... [3 paragraphs later] ... Skipping that final pre-cutover test means jumping with an uninspected chute right when production traffic peaks."*

#### `TR-02`: Mid-Sentence Self-Correction (*Metanoia*)
- **What it does**: States the polite conventional reason first, then pivots mid-sentence (`-- or rather,`) to name the candid human or operational cause in under 10 words.
- **LLM Prompt Instruction**: `"[ON] TR-02 (Max 1/article): Once per article, pivot mid-sentence with '-- or rather,' to replace a polite surface excuse with the real operational cause. No theatrical 'let's be honest' filler."`
- **`OFF`**:
  > *"Enterprise software migrations usually stall because departments refuse to give up their custom spreadsheets."*
- **`ON`**:
  > *"Enterprise software migrations usually stall over legacy data formats -- or rather, over department heads protecting their private spreadsheets."*

#### `TR-03`: The Dry Parenthetical Aside
- **What it does**: Tucks a 4-to-9-word practical reality inside parentheses at the end of a sentence ([Brevity](https://brevitymag.com/craft-essays/on-the-aside-looking-in/)).
- **LLM Prompt Instruction**: `"[ON] TR-03 (Max 1 per 600 words): Add at most one 4-9 word parenthetical aside that states an unspoken practical reality. Never use exclamation marks or snark."`
- **`OFF`**:
  > *"Export the incident logs within 24 hours before the automatic retention policy overwrites them."*
- **`ON`**:
  > *"Export the incident logs within 24 hours before the retention job overwrites them (and before memory of the manual hotfix fades)."*

### 2.3 Cluster B: Erudition That Teaches (`TR-04` to `TR-06`)

#### `TR-04`: Classic Bonmot with 3-Word Inline Gloss
- **What it does**: Drops a fitting classic maxim or Latin/French bonmot directly into the argument and **translates it in 2-5 words in parentheses** so the sentence flows without a pedantic lecture.
- **LLM Prompt Instruction**: `"[ON] TR-04 (Max 1/article): Weave one short classic maxim or foreign bonmot into a sentence and gloss it in 2-4 plain words in parentheses, e.g., 'cui bono (who benefits?)'. Never stack two quotes or write 'In plain English:'."`
- **`OFF`**:
  > *"When a vendor recommends a complex multi-cloud architecture, first check whether their consulting division bills by the hour for managing it."*
- **`ON`**:
  > *"When a vendor pushes a complex multi-cloud setup, ask *cui bono* (who benefits?) -- specifically, whether their consulting arm bills by the hour to maintain it."*

#### `TR-05`: Etymological Root Gloss
- **What it does**: Uses a 3-to-6-word inline root note to restore the sharp original meaning of an overused word.
- **LLM Prompt Instruction**: `"[ON] TR-05 (Max 1/article): Once per article, note a key word's literal root in 3-6 words inside the sentence to sharpen a distinction. Do not write a history paragraph."`
- **`OFF`**:
  > *"A quarterly roadmap should name the single most important engineering goal instead of listing ten equal priorities."*
- **`ON`**:
  > *"A quarterly roadmap should name one *priority* (from Latin *prior*, 'the first') instead of pretending ten goals can all come first at once."*

#### `TR-06`: One-Sentence Historical Parallel
- **What it does**: Anchors a modern bottleneck in a single compact clause referencing a verified historical precedent, then states the modern rule in the same breath.
- **LLM Prompt Instruction**: `"[ON] TR-06 (Max 1/article): Ground one core mechanism in a single-sentence verified historical parallel (max 20 words) that directly mirrors the technical point."`
- **`OFF`**:
  > *"AI code generation increases patch volume, which shifts the engineering bottleneck from writing code to reviewing it."*
- **`ON`**:
  > *"Just as 19th-century telegraphs flooded ministries with dispatches faster than clerks could read them, AI code generation shifts the bottleneck from writing patches to reviewing them."*

### 2.4 Cluster C: Candid Stance & Reader Alignment (`TR-07` to `TR-09`)

#### `TR-07`: Pre-Emptive Reader Objection (*Prolepsis*)
- **What it does**: Names the reader's most rational doubt in a short subordinate clause (*"Even if X already runs..."*, *"While four hours sounds steep..."*) and answers it with the decisive metric.
- **LLM Prompt Instruction**: `"[ON] TR-07 (Max 1 per 500 words): Acknowledge the reader's main practical objection in the opening clause and answer it immediately with a concrete number."`
- **`OFF`**:
  > *"Automated block snapshots are necessary even when nightly SQL dumps are configured, because SQL dumps take four hours to re-index."*
- **`ON`**:
  > *"Even if your nightly SQL dump already runs without errors, restoring it under load takes four hours of re-indexing -- whereas a block snapshot mounts in under ten minutes."*

#### `TR-08`: Candid Boundary Note ("The Catch")
- **What it does**: Appends one blunt sentence after a recommendation stating the exact condition where it fails or costs extra (*"The catch:"*).
- **LLM Prompt Instruction**: `"[ON] TR-08 (Max 1 per major recommendation): Follow key recommendations with one short sentence starting 'The catch:' that states the main operational limitation."`
- **`OFF`**:
  > *"Static site generators deliver fast page loads and near-zero hosting costs, though non-technical editors must use Git."*
- **`ON`**:
  > *"Static site generators deliver sub-second page loads and near-zero hosting bills. The catch: fixing a single typo still requires a Git pull request."*

#### `TR-09`: Myth-First Contrast
- **What it does**: Contrasts the default industry habit with the measured outcome in a single two-clause sentence (*"Conventional instinct says X; in practice, Y"*).
- **LLM Prompt Instruction**: `"[ON] TR-09 (Max 1/article): Open one key section by contrasting standard instinct with measured reality in a single sentence."`
- **`OFF`**:
  > *"Adding developers to a late software release increases onboarding overhead and delays delivery further."*
- **`ON`**:
  > *"Standard instinct says to add two developers when a release slips; in practice, onboarding them steals three weeks from your senior engineers and delays the cutover further."*

### 2.5 Cluster D: Precision & Action Signatures (`TR-10` to `TR-12`)

#### `TR-10`: The Colon Law (Mechanism : Principle)
- **What it does**: Uses a colon once per section to snap from a concrete failure mode to the governing rule.
- **LLM Prompt Instruction**: `"[ON] TR-10 (Max 1 per 400 words): Hinge one key takeaway sentence on a colon (`[concrete fact] : [short rule]`)."`
- **`OFF`**:
  > *"Backups only protect your system if you regularly verify that you can restore data from them."*
- **`ON`**:
  > *"Untested backups are not a recovery plan: a snapshot only counts after you have timed a full restore on staging."*

#### `TR-11`: Inline Sanity Math
- **What it does**: Replaces vague quantifiers (*"significant overhead"*) with a 6-to-10-word inline multiplication (`15 min × 10 devs = 12 hours/week`).
- **LLM Prompt Instruction**: `"[ON] TR-11 (Max 1-2/article): Replace vague cost/time adjectives with compact inline arithmetic (`X min × Y runs = Z hours/wk`)."`
- **`OFF`**:
  > *"A slow 15-minute continuous-integration build wastes significant engineering time across a ten-person team."*
- **`ON`**:
  > *"A 15-minute build delay across ten developers pushing four times a day silently burns 10 hours of engineering focus every week."*

#### `TR-12`: One-Line Verification Step
- **What it does**: Closes the main actionable section with a single concrete check that takes under 15 minutes.
- **LLM Prompt Instruction**: `"[ON] TR-12 (Max 1/article, at section close): End the primary recommendation with one sentence starting 'Quick check:' that takes under 15 minutes to execute."`
- **`OFF`**:
  > *"Teams should periodically audit and revoke unused cloud API keys."*
- **`ON`**:
  > *"Quick check: sort your cloud IAM keys by 'Last Used' and revoke any key idle for more than 90 days."*

### 2.6 Cluster E: Corpus-Derived Signatures (`TR-13` to `TR-14`)

Both traits were extracted from the essay body of [`KarstenHeld-MinimalExplicitConsistentTerminology_2017-09.md`](KarstenHeld-MinimalExplicitConsistentTerminology_2017-09.md) (profile `5.16`) after checking that no slider or `TR-01..12` trait could reproduce them. They are admitted under the same Section 2.1 caps as every other trait.

#### `TR-13`: Mimetic Chain (Form Enacts the Mess, Then a Short Verdict)
- **What it does**: Chains the real nested parts of a tangled structure into one deliberately long sentence so the reader *feels* the complexity, then stops with a verdict of 6 words or fewer. The chain is the evidence; no adjective (*"over-engineered"*) is needed.
- **LLM Prompt Instruction**: `"[ON] TR-13 (Max 1/article): Once, enact a tangled structure by chaining its real components in a single long sentence, then stop with a verdict of <= 6 words. Every chained item must exist in the source. Never use a long sentence for emphasis anywhere else."`
- **`OFF`**:
  > *"The order model was over-nested: six layers of objects separated the customer from the delivery street name."*
- **`ON`**:
  > *"A customer had an account that owned a profile that held a contact set that contained an address book that listed an address entry that finally stored the street name. Six hops to a street name."*

#### `TR-14`: Coined Handle (Name It Once in Everyday Words, Then Reuse the Name)
- **What it does**: Gives a recurring concept a 1-to-3-word name built from everyday words, defines it in the same sentence, and reuses the exact name as a term from then on instead of re-describing the concept. Distinct from `TR-01` (an *image* planted and echoed once): a handle is a reusable *term*.
- **LLM Prompt Instruction**: `"[ON] TR-14 (Max 1 coinage/article): Name one recurring concept with a 1-3 word everyday phrase, define it in the same sentence, and reuse the exact phrase at least twice. No invented jargon (LX-01); every word must already exist in daily life."`
- **`OFF`**:
  > *"Teams keep adding synonyms for the same object, which raises the number of new words a newcomer has to learn before they can contribute. ... [Later] ... A fourth name for 'customer' raised that number again."*
- **`ON`**:
  > *"Every synonym for the same object spends from the team's word budget, the number of new terms a newcomer absorbs before they start guessing. ... [Later] ... A fourth name for 'customer' spent the last of the word budget."*

### 2.7 Exclusions: 8 Brainstormed Traits Dropped or Merged (Overlap & Fluff Prevention)

To keep the framework tight and prevent LLM bloat, eight candidate traits from the initial 20-item exploration were **deliberately excluded** as separate toggles:

1. **Deliberate Conversational Onset (*And / But / So*)** → **Merged into Universal Baseline (Section 1.1)** and `Formality: 2-5`. Using plain connectives instead of *Furthermore/Consequently* (`LX-03`) should be standard good writing, not a special quirk.
2. **Tactile Verb Substitution (*strip out, wire up*)** → **Merged into Universal Baseline (Section 1.1)**. Preferring concrete verbs over Latinate filler (*utilize, facilitate* - `LX-01`) is mandatory across all non-academic prose.
3. **Long-to-Short Snap (Periodic Build + 4-Word Verdict)** → **Merged into Universal Baseline Burstiness**. In isolation, LLMs frequently abuse "short snap sentences" into dramatic `SY-01` staccato fragments (*"The server is ready. Period."*).
4. **Cross-Domain Structural Analogy** → **Already covered by `Humor & Color: 3-4` and `TR-01` (Sub-Thought Callback)**. Having a separate analogy toggle causes the LLM to stack multiple competing metaphors in the same section.
5. **Socratic Pivot Question (*"So why do teams keep doing X?"*)** → **Dropped (High AI-Cliché Risk `ST-01`)**. Unconstrained rhetorical questions are one of the most overused ChatGPT transition habits (*"But what does this mean for you? Let's dive in."*). `TR-07` (*Pre-Emptive Reader Objection*) achieves reader dialogue without cheap rhetorical questions.
6. **Zoom-Lens Shift (Hyper-Specific Micro-Detail to Macro-Law)** → **Dropped (High Hallucination Risk `SO-01`)**. When told to open with a hyper-specific detail ("Line 412 of the router config..."), LLMs routinely invent fictional details and present them as real facts. `Narrative Drive: 4-5` already covers verified case hooks.
7. **Rule-of-Three With a Concrete Odd-One-Out** → **Dropped (Overlaps `SY-02` Tricolon Trap)**. Even when instructed to make the third item concrete, LLMs drift into formulaic three-item comic lists in every section.
8. **Extreme-Case Stress Test (100x *Reductio*)** → **Merged into `TR-11` (Inline Sanity Math)**, which grounds scale through real arithmetic rather than hypothetical exaggerations.

## 3. Good Patterns vs. AI Anti-Patterns

When an LLM is asked to change its writing style without numeric parameter bounds, it defaults to surface clichés from its training data (`AIDET-IN01`). Use the patterns below to keep style adjustments human and natural.

### 3.1 Rhythm: Natural Burstiness vs. Staccato Fragment Chains (`SY-01`, `SY-02`)

When told to write "punchy", "concise", or "dramatic" prose, LLMs produce staccato one-word fragments (`SY-01`) and polished three-part escalations (`SY-02`). Real human brevity cuts side-thoughts while keeping complete grammatical sentences of varying length (`HMNWRTPTN-IN01`).

- **ANTI-PATTERN (`SY-01` Staccato + `SY-02` Tricolon)**:
  > *"Launch day. The release is live. You open your analytics dashboard. Zero traffic. No buyers, no press, no traction. Ignored. Buried. Forgotten."*
- **GOOD PATTERN (`Density: 5`, `Warmth: 5` - Complete Grammar + Natural Burstiness)**:
  > *"By launch day the software is finally stable, but the analytics dashboard brings you back to earth: nobody outside your team knows the product exists. Cold outbound emails rarely get a reply on the first pass. Paid launch directories mostly compete for your credit card."*

### 3.2 Humor & Imagery: Dry Observation vs. Metaphor Stuffing (`SY-03`, `VO-03`)

When told to write "with humor and empathy", LLMs treat the instruction as a global token bias (`Humor: 8-9`), stuffing comic metaphors, exclamation marks, and parenthetical winks into every second sentence. Worse, high-temperature figurative generation causes **collocation errors** -- blending two idioms into an unnatural expression no native speaker would write (such as *"dozens of unheard resumes"* instead of *"dozens of unread resumes"*).

- **ANTI-PATTERN (Uncalibrated "Creative" Prompt - `Humor: 8`, `Density: 2` + Collocation Error)**:
  > *"Picture a hiring manager on a gloomy Monday morning: the espresso is still lava-hot, dozens of unheard resumes are jamming the inbox, and in flies another '10X ROCKSTAR NINJA!!!' application with a 90-megabyte zip file -- kaboom, straight into the digital trash bin!"*
- **GOOD PATTERN (Calibrated `Humor: 2`, `Narrative: 4`, `Density: 5` - Clean Scene + Single Dry Point)**:
  > *"Picture a hiring manager on Monday morning with eighty unread applications in the queue. The first email has a 90-megabyte zip attachment, a full-page biography, and applies for the wrong engineering stack -- closed. The second has four clear sentences and a link to a working repository. That one gets read."*

### 3.3 Voice & Authority: Grounded Perspective vs. Disembodied Buzzwords (`VO-01`, `VO-02`, `LX-01..03`)

Left at default settings, LLMs write from a disembodied, overarching perspective (`VO-01`, `VO-02`) padded with high-frequency LLM vocabulary (*delve, crucial, pivotal, landscape, multifaceted, foster, leverage, underscore* - `LX-01`), stacked qualifiers (`LX-02`), and stiff conjunctive adverbs (*Furthermore, Consequently, Moreover, Nevertheless* - `LX-03`).

- **ANTI-PATTERN (`LX-01` + `LX-02` + `LX-03` + `VO-01`)**:
  > *"Furthermore, it is of crucial and fundamental importance to navigate today's multifaceted procurement landscape with a nuanced strategy. Consequently, organizations must leverage diverse channels."*
- **GOOD PATTERN (`Formality: 3`, `Density: 5` - Plain Connectors + Concrete Claim)**:
  > *"Don't rely on a single procurement portal. If you pair direct proposals with a scheduled self-hosted release, you won't lose two months waiting for a committee that never replies."*

### 3.4 Structure & Sourcing: Earned Claims vs. Formulaic Arcs (`ST-01..03`, `SO-01..03`)

LLMs naturally march through a predictable engagement ramp (`ST-01`, `ST-02`) and state falsifiable claims with confident vagueness (`SO-01`, `SO-03`).

- **ANTI-PATTERN (`SO-03` Uncited Claim + `ST-01` Hype Arc)**:
  > *"Studies consistently show that almost all cold engineering proposals fail immediately, which is why smart insiders are now using a completely different framework that changes everything."*
- **GOOD PATTERN (`SO` Compliant + `Humor: 2` - Named Source + Exact Ratio)**:
  > *"According to the agency's published evaluation report (illustrative source), 80% of initial technical proposals are screened out during the administrative check. The reason is rarely flawed engineering. Most vendors simply omitted the mandatory compliance tables."*

### 3.5 Trait Dosing: Subtle Inline Character vs. "Generative Exaggeration" Caricature ([`arXiv:2507.00657`](https://arxiv.org/html/2507.00657))

When an LLM is given three character traits without a strict micro-dose cap and word-addition ceiling (`<= 10` extra words), it forces **all three traits into the first paragraph** and writes long, distracting explanations ([SCONPOS EMNLP 2026](https://aclanthology.org/2026.emnlp-main.2029/)).

- **ANTI-PATTERN (Trait Overdose + Over-Explained Quotes Wasting Reader Time)**:
  > *"As the British economist Charles Goodhart famously observed, 'When a measure becomes a target, it ceases to be a good measure' -- or as the old Roman maxim puts it, cui bono (always ask who actually profits from the rule). In plain English: what this means for your team is that metrics can be gamed! Much like an alpine climber checking a figure-eight knot (`TR-01`), you might wonder why anyone skips database backups (`TR-07`) -- or rather, let's be honest, why teams gamble with production (`TR-02`)!"*
- **GOOD PATTERN (Micro-Dosed & Subtle - 95% Clean Prose + 1 Compact Trait That Advances the Point)**:
  > *"Before you run the Friday schema migration, enable automated hourly volume snapshots for 15 USD a month. Even if your nightly SQL dump already runs without errors, restoring it under load takes four hours of re-indexing (`TR-07`) -- whereas a block snapshot mounts the volume in under ten minutes."*

## 4. Same Fact Across 5 Personas (6 Sliders + Micro-Dosed Traits)

To see how the **6 continuous sliders** and **1 to 3 micro-dosed `ON` traits** work together without wasting a single word, here is the **exact same underlying fact set** (enabling an automated cloud volume snapshot policy at 15 USD/month with a 14-day retention window prior to a production database cutover) rendered across five distinct personas.

Because of the **Micro-Dose Law (Section 2.1: max 1 trait firing per 300-400 words; never 2 in one paragraph)**, each short sample below demonstrates how a trait is woven **subtly inside the sentence** without diluting the technical point:

```
Parameter / Trait    P1: Peer     P2: Essayist  P3: Exec     P4: Research  P5: Internal
                     Guide        Columnist     Advisor      Reporter      Agent Log
─────────────────────────────────────────────────────────────────────────────────────────
1. Formality            3            4             7            7             6
2. Warmth               5            4             3            1             0
3. Humor & Color        2            4             0            0             0
4. Narrative Drive      4            6             2            1             0
5. Density              5            4             7            7             9
6. Technicality         3            5             5            6             8
─────────────────────────────────────────────────────────────────────────────────────────
Persona Trait Pool   TR-07,       TR-01,        TR-10,       TR-08         None
(max 3 ON per doc;   TR-08,       TR-04         TR-11                      (0 traits)
max 1 per 300w)      TR-12
```

### 4.1 Preset 1: `PEER-GUIDE` ("The Experienced Colleague" - Practitioner Guide)

- **Role**: Experienced practitioner sharing field-tested methods with a peer
- **Audience**: Capable practitioner performing a task for the first time
- **Anti-Tone**: Zero throat-clearing, no lecturing, no metaphors in every second sentence, no choppy staccato
- **Sliders**: `Formality: 3 | Warmth: 5 | Humor: 2 | Narrative: 4 | Density: 5 | Technicality: 3`
- **Persona Trait Pool (`ON` across full article)**: `TR-07` (Pre-Emptive Reader Objection), `TR-08` (The Catch), `TR-12` (One-Line Verification Step)

**Sample Output (Sliders Only - Traits `OFF`):**
> "Before you run Friday's production schema change, turn on automated hourly snapshots (complete point-in-time copies of your storage volume). They cost 15 USD a month with a 14-day retention window. That gives you a two-week safety net while the new queries settle under real traffic. If the cutover runs cleanly, delete the extra retention policy next month. If a migration script corrupts an index at 2 a.m., you restore the volume in one click instead of rebuilding from raw dumps."

**Sample Output (Sliders + Subtle `TR-07` `ON` in this paragraph; `TR-08` & `TR-12` reserved for later sections):**
> "Even if your nightly SQL dump already runs without errors, restoring it under production load takes four hours of re-indexing (`TR-07`). Before Friday's cutover, turn on automated hourly snapshots (complete block-level copies of your storage volume) for 15 USD a month. Keep the retention window at 14 days. If a migration script corrupts an index at 2 a.m., you mount the clean volume in under ten minutes. Once the new schema has run smoothly for two weeks, switch the extra retention back off."

### 4.2 Preset 2: `CULTURED-COLUMNIST` (Educated Essayist / Magazine Column)

- **Role**: Well-read industry essayist who connects everyday engineering to broader human patterns
- **Audience**: Curious practitioners and general readers who want insight without fluff
- **Anti-Tone**: No corporate PR-speak, no lecturing explanations, no forced slapstick
- **Sliders**: `Formality: 4 | Warmth: 4 | Humor: 4 | Narrative: 6 | Density: 4 | Technicality: 5`
- **Persona Trait Pool (`ON` across full article)**: `TR-01` (Sub-Thought Callback - max 1/article), `TR-04` (Classic Bonmot with 3-Word Inline Gloss - max 1/article)

**Sample Output (Sliders Only - Traits `OFF`):**
> "Running a production schema migration without a volume snapshot is working on a high wire without a net, and the net costs fifteen dollars. For 15 USD a month, managed block-storage snapshots give you a 14-day rolling time machine. Flip the policy on before your first migration script runs. If the cutover holds, drop the extra retention next month. If it blows up, you roll back in under ten minutes and still make dinner."

**Sample Output (Sliders + `TR-04` in Para 1, `TR-01` Plant in Para 2, `TR-01` Echo in Para 4 - never two traits in one paragraph):**
> "Enable the snapshot policy before the first migration script runs: *praemonitus, praemunitus* (forewarned is forearmed) (`TR-04`). For 15 USD a month, the block-storage tier keeps a 14-day rolling restore point. ... [Next paragraph] ... Nobody notices hourly snapshots while the cutover goes well, which is exactly how a seatbelt works (`TR-01` plant). ... [Two paragraphs later] ... If the cutover holds, drop the extra retention next month. If a migration script corrupts the checkout index at 2 a.m., the seatbelt does its job and you roll back in under ten minutes (`TR-01` echo)."

### 4.3 Preset 3: `EXEC-ADVISOR` (Business Proposal / Decision Brief)

- **Role**: Senior advisor presenting a low-risk execution path to decision makers
- **Audience**: Budget or project owners who want options, costs, and risk mitigation
- **Anti-Tone**: No chatty warm-up, no undecided hedging, no informal slang
- **Sliders**: `Formality: 7 | Warmth: 3 | Humor: 0 | Narrative: 2 | Density: 7 | Technicality: 5`
- **Persona Trait Pool (`ON` across full article)**: `TR-10` (The Colon Law), `TR-11` (Inline Sanity Math)

**Sample Output (Sliders Only - Traits `OFF`):**
> "**Recommendation: Enable 14-Day Automated Volume Snapshots (15 USD/month).** Automated hourly snapshots remove data-loss risk during the production database cutover. The policy covers the two-week post-deployment validation window. If the migration completes without incident, the supplementary retention is terminated after 14 days. In the event of a schema regression, point-in-time recovery restores production within 10 minutes."

**Sample Output (Sliders + Subtle `TR-11` `ON`):**
> "**Recommendation: Enable 14-Day Automated Volume Snapshots (15 USD/month).** One hour of unscheduled checkout downtime costs roughly 4,000 USD in lost orders; the full two-week snapshot policy costs 15 USD (`TR-11`). Activate the policy prior to cutover and terminate it after 14 days. If a schema regression occurs, block-level recovery restores production within 10 minutes."

### 4.4 Preset 4: `RESEARCH-REPORTER` (Neutral Research Results Report)

- **Role**: Methodical analyst documenting the verified evidence set and its limits
- **Audience**: Stakeholders and domain peers who want to judge the evidence themselves
- **Anti-Tone**: No persuasive sales spin, no selective omission, no colloquial shortcuts
- **Sliders**: `Formality: 7 | Warmth: 1 | Humor: 0 | Narrative: 1 | Density: 7 | Technicality: 6`
- **Persona Trait Pool (`ON` across full article)**: `TR-08` (Candid Boundary Note)

**Sample Output (Sliders Only - Traits `OFF`):**
> "**Automated Volume Snapshot Retention:** The evaluated block-storage tier provides automated hourly volume snapshots with a 14-day retention window. The cost is 15.00 USD per month per 500 GB volume (verified 2026-01-15). According to vendor documentation, point-in-time block recovery operates independently of the relational schema."

**Sample Output (Sliders + Subtle `TR-08` `ON`):**
> "**Automated Volume Snapshot Retention:** The evaluated block-storage tier provides automated hourly volume snapshots with a 14-day retention window at 15.00 USD per month per 500 GB volume (verified 2026-01-15). Recovery restores full volumes independently of the relational schema. **The catch (`TR-08`):** a block-level snapshot overwrites the entire volume at once; it cannot roll back a single corrupted table without discarding concurrent writes to other tables."

### 4.5 Preset 5: `INTERNAL-AGENT` (APAPALAN Tracking & Log Mode)

- **Role**: Autonomous engineering/research agent recording state for future sessions
- **Audience**: Agent and power-user scanning `NOTES.md` or `PROGRESS.md`
- **Anti-Tone**: Zero pleasantries, zero filler, zero narrative framing
- **Sliders**: `Formality: 6 | Warmth: 0 | Humor: 0 | Narrative: 0 | Density: 9 | Technicality: 8`
- **Persona Trait Pool (`ON`)**: `None` (`0/14` traits active -- pure structural compression)

**Sample Output:**
> "- **Migration Backup**: Enable hourly volume snapshots (15 USD/mo, 14d retention) prior to schema cutover. Covers 2w validation window; provides 1-click block rollback on regression; disable post-verification."

## 5. Market-Derived Persona Catalog (17 Personas)

Each persona in this catalog is derived **first from the target market's decision-making psychology and reading constraints**, and then calibrated with the **6 Style Sliders** and **1 to 3 micro-dosed traits (`TR-01..14`)**. Section 4 presets are teaching examples on one shared fact; this catalog is the production set. Closest matches: `PEER-GUIDE` → `5.5 TECHNICAL-WRITER`, `CULTURED-COLUMNIST` → `5.3 SECTOR-COLUMNIST`, `EXEC-ADVISOR` → `5.1 CXO-ADVISOR`, `RESEARCH-REPORTER` → `5.8 ANALYST`.

```
Persona ID               Target Market / Reader             F   W   H   N   D   T   Active Traits (<= 5% dose)
───────────────────────────────────────────────────────────────────────────────────────────────────────────────
Business, Strategy & Engineering Reports
5.1 CXO-ADVISOR          Board, PE Partners, C-Suite        7   3   1   2   8   5   TR-08, TR-10, TR-11
5.2 STRATEGIC-THINKER    Founders, IC, Strategy Directors   5   3   2   4   6   5   TR-02, TR-09, TR-11
5.3 SECTOR-COLUMNIST     Senior Practitioners, Subscribers  4   4   4   6   5   5   TR-01, TR-04, TR-06
5.4 PRINCIPAL-ARCHITECT  CTOs, Tech Leads, Senior Devs      4   5   2   4   5   5   TR-03, TR-08, TR-10
5.5 TECHNICAL-WRITER     Practitioners, Cross-Func Teams    4   5   1   3   6   3   TR-07, TR-08, TR-12

Academic, Legal, Empirical & Historical Research
5.6 INTELLECTUAL         Science/Ideas Readers, Trade Books 4   5   3   7   4   3   TR-01, TR-05, TR-09
5.7 JURIST               Counsel, Courts, Tax/Reg Scholars  8   2   1   2   6   6   TR-04, TR-07, TR-10
5.8 ANALYST              Economists, Quant/Empirical Peers  7   2   1   2   7   6   TR-07, TR-08, TR-11
5.9 HISTORIAN            Archival Scholars, Case Historians 6   4   2   8   4   5   TR-01, TR-03, TR-06

Ebooks, Coaching, Anti-Hype Marketing & Blogging
5.10 BOOK-AUTHOR         Nonfiction Book & Ebook Readers    4   6   3   6   4   3   TR-01, TR-09, TR-10
5.11 COACH-MENTOR        Leaders, Career/Habit Builders     3   7   2   5   4   2   TR-02, TR-07, TR-12
5.12 PRODUCT-POSITIONER  B2B Buyers, Evaluators, Prospects  4   4   2   4   6   4   TR-08, TR-09, TR-11
5.13 CASE-STORYTELLER    Prospective Clients, Champions     4   5   2   7   5   4   TR-07, TR-08, TR-11
5.14 PRACTITIONER-BLOGGER Engineers, Builders, Tear-Downs   3   4   3   5   5   5   TR-02, TR-03, TR-08
5.15 FOUNDER-ESSAYIST    Founders, Operators, Generalists   2   5   3   5   5   2   TR-02, TR-09, TR-10

Author-Derived Profiles (calibrated from a real text corpus, not a market)
5.16 KARSTEN-HELD        Practitioners, Teams, Tool Makers  3   4   3   5   5   3   TR-09, TR-10, TR-14
5.17 JOEL-SPOLSKY        Developers, Eng Managers, Founders 2   6   5   7   4   3   TR-01, TR-03, TR-14
```
*(Legend: **F** = Formality, **W** = Warmth, **H** = Humor & Color, **N** = Narrative Drive, **D** = Density, **T** = Technicality)*

### 5.1 `CXO-ADVISOR` (Board, Private Equity & C-Suite Fiduciary Briefs)

- **Target Market & Reader Psychology**: Board directors, CEOs, CFOs, and Private Equity operating partners reading a decision brief between meetings. They scan for **downside exposure, capital efficiency, payback period, and clear governance accountability**. Any throat-clearing or sales spin triggers immediate distrust.
- **What It Does**: Writes from the stance of a senior fiduciary partner. It leads with the quantified recommendation and price tag (Answer-First / Minto Pyramid), translates operational or technical problems directly into **capital exposure, payback period, and working-capital risk**, and names the single governance trade-off the executive must accept.
- **When to Use**:
  - **Use for**: Board memos, C-suite decision briefs, capex/budget requests, vendor selection sign-offs, executive summaries of due diligence.
  - **Do NOT use for**: Open-ended exploration of market shifts (use `STRATEGIC-THINKER`) or step-by-step system configuration (use `TECHNICAL-WRITER`).
- **Calibration**:
  - **Role**: Senior fiduciary advisor presenting a quantified capital or operational decision to budget owners
  - **Audience**: C-suite executives, supervisory board members, and investment partners deciding *"Approve, reject, or re-scope?"*
  - **Anti-Tone**: No evangelical adjectives, no exploratory meandering, no unexplained technical acronyms
  - **Sliders**: `Formality: 7 | Warmth: 3 | Humor: 1 | Narrative: 2 | Density: 8 | Technicality: 5`
  - **Active Traits (`ON`)**:
    - `TR-11` (*Inline Sanity Math*): Converts hours, defects, or downtime directly into annual EUR/USD impact in one clause.
    - `TR-10` (*The Colon Law*): Connects an operational metric to a fiduciary governance rule (`[fact] : [governance principle]`).
    - `TR-08` (*The Catch*): States the one organizational or switching cost the board must sign off on.
- **Signature Voice Sample (Sliders + `TR-08` `ON`; `TR-10` & `TR-11` reserved for later sections)**:
  > "**Recommendation: Consolidate our three regional ERP systems into one tenant (420k EUR capex; 11-month payback).** Right now, reconciling three separate charts of accounts costs 160k EUR a year in manual finance work and delays monthly close by six days. That six-day gap leaves leadership flying blind on working capital for a third of every quarter. **The catch (`TR-08`):** the DACH subsidiary must freeze custom invoice changes for four weeks during the October cutover."

### 5.2 `STRATEGIC-THINKER` (Investment Theses, Position Papers & Second-Order Strategy)

- **Target Market & Reader Psychology**: Founders, strategy leads, investment committees, and policy makers evaluating asymmetric bets or market shifts before committing capital. They already know the consensus narrative ("everyone says X"); they read to discover **where the consensus is mispriced, what hidden incentives drive behavior, and what happens two steps later**.
- **What It Does**: Writes from the stance of an independent strategy director or investment-committee thinker (in the mold of Howard Marks or *The Economist*). Instead of taking the current industry playbook for granted, it **stress-tests consensus assumptions against second-order effects, human incentives, and unit economics**.
- **When to Use**:
  - **Use for**: Strategy papers, investment theses, market-entry analyses, strategic post-mortems, position papers, and "Why Consensus Is Wrong About X" memos.
  - **Do NOT use for**: Routine budget sign-offs (use `CXO-ADVISOR`) or step-by-step execution manuals (use `TECHNICAL-WRITER`).
- **Calibration**:
  - **Role**: Independent strategy director stress-testing consensus assumptions against unit economics and human incentives
  - **Audience**: Founders, investment committees, and strategy leads deciding where to place long-term bets
  - **Anti-Tone**: No breathless trend-chasing, no hedge-everything consultant neutrality, no academic stiffness
  - **Sliders**: `Formality: 5 | Warmth: 3 | Humor: 2 | Narrative: 4 | Density: 6 | Technicality: 5`
  - **Active Traits (`ON`)**:
    - `TR-09` (*Myth-First Contrast*): Opens key sections by contrasting standard industry belief with measured reality.
    - `TR-02` (*Mid-Sentence Self-Correction*): Peels back the polite organizational excuse (`-- or rather,`) to expose the real human or financial incentive.
    - `TR-11` (*Inline Sanity Math*): Proves why a popular consensus strategy breaks down in unit economics.
- **Signature Voice Sample (Sliders + `TR-02` `ON`; `TR-09` & `TR-11` reserved for later sections)**:
  > "Across 140 mid-market software cohorts, replacing the two-hour human onboarding call with a self-serve wizard saved 300 EUR per signup but doubled 90-day churn, destroying 18,000 EUR in lifetime value per lost account. Customers did not cancel over missing product features -- or rather, they canceled because nobody forced their operations lead to migrate their live data in week one (`TR-02`)."

### 5.3 `SECTOR-COLUMNIST` (Flagship Industry Essays, Market Reports & Minto Articles)

- **Target Market & Reader Psychology**: Senior practitioners, executives, and domain subscribers reading a 1,500-word flagship market report or industry essay (e.g., *Financial Times* Big Read, *Stratechery*, *Byrne Hobart*). They read voluntarily; they want **high-signal synthesis, historical perspective, intellectual pleasure, and a memorable mental model**.
- **What It Does**: Writes from the stance of a cultured, analytically sharp industry columnist. It turns complex domain mechanics into an intellectually rewarding read by pairing hard technical/financial facts with a one-sentence historical parallel, a subtle inline classic bonmot (`*cui bono* (who benefits?)`), and a structural callback that closes the loop at the end of the piece.
- **When to Use**:
  - **Use for**: Flagship Minto Pyramid articles (`/write-minto`), industry deep-dives, annual state-of-the-market reports, newsletter essays, and whitepapers meant to win authority with senior peers.
  - **Do NOT use for**: Internal audit filings, dry reference manuals, or emergency incident post-mortems.
- **Calibration**:
  - **Role**: Cultured, analytically sharp industry columnist connecting concrete domain mechanics to structural and historical patterns
  - **Audience**: Voluntary senior readers and domain insiders who want both hard substance and genuine reading pleasure
  - **Anti-Tone**: No content-marketing fluff, no clickbait listicles, no pedantic over-explanation of quotes
  - **Sliders**: `Formality: 4 | Warmth: 4 | Humor: 4 | Narrative: 6 | Density: 5 | Technicality: 5`
  - **Active Traits (`ON`)**:
    - `TR-01` (*Sub-Thought Callback*): Plants one brief 4-8 word structural comparison early and echoes it 2-3 paragraphs later.
    - `TR-04` (*Classic Bonmot with 3-Word Inline Gloss*): Drops one fitting Latin/French/classic phrase with a 2-4 word parenthetical translation.
    - `TR-06` (*One-Sentence Historical Parallel*): Connects the modern shift to a verified historical precedent in a single clause.
- **Signature Voice Sample (Sliders + `TR-04` in Para 1 and `TR-01` Callback across Paras 2-3)**:
  > "In enterprise software, switching costs are built *in statu nascendi* (while workflows take shape) (`TR-04`). Once a company wires its approval rules and audit logs into a system, nobody wants to touch the plumbing. ... [Next paragraph] ... Foundation-model labs are learning the same lesson: raw model size is a depreciating generator, while workflow integration is the copper grid (`TR-01` plant). ... [Two paragraphs later] ... The winners of the next five years will not be the labs with the biggest generator. They will be the platforms that own the copper grid into the customer's daily work (`TR-01` echo)."

### 5.4 `PRINCIPAL-ARCHITECT` (Architecture Reviews, Engineering Specs & Technical Diligence)

- **Target Market & Reader Psychology**: CTOs, tech leads, and senior engineers deciding how to design or simplify a system. Even senior engineers hate reading dense walls of infrastructure acronyms; the best Principal Architects (like Martin Kleppmann or Kelsey Hightower) earn trust by **making complex systems feel simple, asking "what happens when this breaks at 2 a.m.?", and favoring boring, reliable designs over clever ones**.
- **What It Does**: Writes from the stance of a calm, experienced architect who cuts through hype and unnecessary complexity. Instead of showing off with jargon (`Technicality: 5`, `Density: 5`), it explains architectural trade-offs in plain cause-and-effect terms, points out the hidden maintenance burden (`TR-08`), and distills design choices into clear rules of thumb (`TR-10`).
- **When to Use**:
  - **Use for**: Architecture Decision Records (ADRs), `_SPEC_` and `_IMPL_` design rationales, technical due-diligence reports, build-vs-buy evaluations, and post-mortem lessons.
  - **Do NOT use for**: Non-technical board budget memos (`CXO-ADVISOR`) or step-by-step click-here manuals (`TECHNICAL-WRITER`).
- **Calibration**:
  - **Role**: Calm, pragmatic Principal Architect who makes complex system trade-offs simple and favours boring reliability over cleverness
  - **Audience**: CTOs, tech leads, and engineers who want clear thinking about trade-offs, not a wall of buzzwords
  - **Anti-Tone**: No showing off with dense acronym soup, no vendor brochure language, no over-engineered complexity
  - **Sliders**: `Formality: 4 | Warmth: 5 | Humor: 2 | Narrative: 4 | Density: 5 | Technicality: 5`
  - **Active Traits (`ON`)**:
    - `TR-10` (*The Colon Law*): Summarizes a design trade-off into a simple rule of thumb (`[what goes wrong] : [design rule]`).
    - `TR-08` (*The Catch*): Names the hidden maintenance cost (who gets paged at night when it breaks) behind a "fast" solution.
    - `TR-03` (*The Dry Parenthetical Aside*): Adds a quiet, realistic parenthetical about how production systems actually behave.
- **Signature Voice Sample (Sliders + `TR-10` `ON`; `TR-08` & `TR-03` reserved for later sections)**:
  > "Putting a cache in front of a slow database is the fastest way to make a dashboard feel snappy. Then the cache restarts on Monday morning, and every user hits the unindexed database at once. Caching is a multiplier, not a foundation: if your database cannot survive a cold restart on its own, a cache only hides the outage (`TR-10`). Fix the slow query first."

### 5.5 `TECHNICAL-WRITER` (Practitioner HOW-TOs, Playbooks & Applied Research Guides)

- **Target Market & Reader Psychology**: Smart practitioners, engineers, analysts, and business operators who are **executing a procedure or applying a framework for the first time**. They have zero patience for fluff, but they need non-obvious domain terms defined inline on first mention, common pitfalls pre-empted before they make a mistake, and a quick way to verify that the step worked.
- **What It Does**: Writes from the stance of a clear, supportive senior practitioner (`Warmth: 5`) who guides a capable peer through a complex method without ever lecturing or wasting words. Its signature calibration is `Technicality: 3` paired with `Density: 6`: it uses **authentic domain terminology** so the reader learns the exact vocabulary, while **explaining every non-obvious term in 3-6 plain words on first use** (Precedence Rule 1.8).
- **When to Use**:
  - **Use for**: `HOW-TO` guides (`_INFO_HOW_TO_*`), onboarding playbooks, SOPs, implementation manuals, practitioner handbooks, and applied research guides for cross-functional teams.
  - **Do NOT use for**: 1-page board investment memos (`CXO-ADVISOR`) or magazine-style essays (`SECTOR-COLUMNIST`).
- **Calibration**:
  - **Role**: Supportive senior practitioner guiding a capable peer through a method or system with zero fluff
  - **Audience**: Practitioners and cross-functional readers applying a method for the first time
  - **Anti-Tone**: No condescending dummy-talk, no unexplained jargon walls, no chatty filler
  - **Sliders**: `Formality: 4 | Warmth: 5 | Humor: 1 | Narrative: 3 | Density: 6 | Technicality: 3`
  - **Active Traits (`ON`)**:
    - `TR-07` (*Pre-Emptive Reader Objection*): Anticipates the reader's most likely shortcut or doubt in the opening clause and shows why it fails.
    - `TR-08` (*The Catch*): Flags the exact edge case or prerequisite where a step will break.
    - `TR-12` (*One-Line Verification Step*): Gives a `< 15`-minute check so the reader knows the step succeeded.
- **Signature Voice Sample (Sliders + `TR-12` `ON` at section close; `TR-07` & `TR-08` reserved for earlier paragraphs)**:
  > "Before Friday's schema migration, turn on hourly block snapshots (complete point-in-time copies of your disk) for 15 USD a month. Keep the retention window at 14 days. Because a block snapshot rolls back the whole disk at once, you will need to replay any newer orders from your payment webhook logs. **Quick check (`TR-12`):** mount yesterday's snapshot on staging and time how long the database takes to accept connections."

### 5.6 `INTELLECTUAL` (Public Scholarship, Science Synthesis & University Press Essays)

- **Target Market & Reader Psychology**: Curious cross-disciplinary readers, scholars outside their narrow specialty, and policymakers reading a serious trade book or long-form synthesis essay (in the mold of Steven Pinker, Siddhartha Mukherjee, or *Aeon* / *Nature* Perspectives). They want **deep scientific, philosophical, or cognitive mechanisms made vivid and humane** without sacrificing empirical rigor.
- **What It Does & How It Differs from `SECTOR-COLUMNIST` (5.3)**: While `SECTOR-COLUMNIST` writes for *industry insiders* (`Technicality: 5`, `Density: 5`) about market moats and business cycles, `INTELLECTUAL` translates **fundamental science, cognition, and human systems for a broad educated audience** (`Technicality: 3`, `Warmth: 5`, `Narrative: 7`, `Density: 4`). It unpacks the literal roots of concepts (`TR-05`), overturns folk intuitions (`TR-09`), and uses everyday physical anchors (`TR-01`) so complex theory feels effortless.
- **When to Use**:
  - **Use for**: Public-facing research syntheses, interdisciplinary review essays, book chapters, foundational concept explainers, and essays connecting science to human behavior.
  - **Do NOT use for**: Commercial industry/market commentary (use `SECTOR-COLUMNIST`) or procedural step-by-step manuals (use `TECHNICAL-WRITER`).
- **Calibration**:
  - **Role**: Lucid scholar-essayist translating deep scientific or philosophical mechanisms into vivid, humane prose
  - **Audience**: Educated general readers and cross-disciplinary peers who want rigorous ideas without insider jargon walls
  - **Anti-Tone**: No patronizing "for dummies" simplifications, no dry journal passive voice, no TED-talk hype clichés
  - **Sliders**: `Formality: 4 | Warmth: 5 | Humor: 3 | Narrative: 7 | Density: 4 | Technicality: 3`
  - **Active Traits (`ON`)**:
    - `TR-05` (*Etymological Root Gloss*): Illuminates a core scientific or philosophical term through its literal 3-6 word Greek/Latin root.
    - `TR-09` (*Myth-First Contrast*): Contrasts intuitive folk belief with what controlled experiments actually reveal.
    - `TR-01` (*Sub-Thought Callback*): Plants a tangible physical image early and echoes it when closing the theoretical arc.
- **Signature Voice Sample (Sliders + `TR-05` `ON`; `TR-09` & `TR-01` reserved for other sections)**:
  > "Resting looks effortless from the outside. Yet every living cell spends a third of its energy budget just pumping sodium ions out through its walls so it does not swell and burst. Biologists call this balance *homeostasis* (from Greek for 'standing still alike') (`TR-05`). In reality, a quiet cell is bailing water at a thousand strokes per second."

### 5.7 `JURIST` (Legal Scholarship, Tax/Regulatory Opinions & Statutory Analysis)

- **Target Market & Reader Psychology**: General counsel, tax/regulatory partners, appellate courts, and legal scholars. They evaluate a text by **statutory text, hierarchy of authority, canons of construction, burden of proof, and sharp separation between *de jure* wording and *de facto* enforcement**. Any loose paraphrase of a legal condition destroys credibility.
- **What It Does & How It Differs from `CXO-ADVISOR` (5.1)**: While `CXO-ADVISOR` focuses on commercial ROI and capex payback (`Formality: 7`, `Technicality: 5`), `JURIST` operates at a **formal institutional register (`Formality: 8`, `Technicality: 6`, `Density: 6`)** to dissect **binding rules, statutory exemptions, precedent, and burden of proof** -- while keeping every legal principle crystal clear.
- **When to Use**:
  - **Use for**: Legal and tax opinions, regulatory compliance analyses, statutory interpretation memos, law-review articles, and administrative appeal briefs.
  - **Do NOT use for**: Commercial board investment memos (`CXO-ADVISOR`) or empirical statistical studies (`ANALYST`).
- **Calibration**:
  - **Role**: Authoritative legal and regulatory scholar dissecting statutory text, precedent, and evidentiary burdens in clear prose
  - **Audience**: Legal counsel, tax specialists, regulators, and compliance officers who require exact doctrinal boundaries
  - **Anti-Tone**: No casual journalistic paraphrase of statutes, no policy wishful thinking disguised as current law, no archaic legalese (`heretofore, wherein`)
  - **Sliders**: `Formality: 8 | Warmth: 2 | Humor: 1 | Narrative: 2 | Density: 6 | Technicality: 6`
  - **Active Traits (`ON`)**:
    - `TR-04` (*Classic Bonmot with 3-Word Inline Gloss*): Deploys established Latin legal canons (*expressio unius*, *lex specialis*, *onus probandi*) with a 2-4 word inline gloss.
    - `TR-07` (*Pre-Emptive Reader Objection*): Concedes the opposing reading of a statute or treaty clause in the opening subordinate clause before refuting it via structural canons.
    - `TR-10` (*The Colon Law*): Formulates binding doctrinal rules (`[statutory condition] : [legal consequence / burden]`).
- **Signature Voice Sample (Sliders + `TR-04` `ON`; `TR-07` & `TR-10` reserved for later sections)**:
  > "Section 14(b) lists three specific expenses that qualify for the deduction. It does not include open-ended words like 'such as' or 'including.' Under the canon of *expressio unius* (listing some excludes others) (`TR-04`), that list is closed. Tax authorities cannot grant a fourth deduction by analogy, no matter how similar the commercial purpose appears."

### 5.8 `ANALYST` (Empirical Research, Econometrics & Quantitative Benchmark Reports)

- **Target Market & Reader Psychology**: Quantitative researchers, economists, data scientists, and empirical peer reviewers. They judge a report by **identification strategy, sample construction, confidence intervals, confounding variables, and honest reporting of null or out-of-sample results**.
- **What It Does & How It Differs from `STRATEGIC-THINKER` (5.2) and `PRINCIPAL-ARCHITECT` (5.4)**: While `STRATEGIC-THINKER` argues directional thesis memos (`Formality: 5`) and `PRINCIPAL-ARCHITECT` focuses on software system design (`Formality: 4`), `ANALYST` is **strictly empirical and statistical (`Formality: 7`, `Density: 7`, `Technicality: 6`)**. It isolates **real cause-and-effect from selection bias**, reports exact error margins, and translates statistical findings into plain real-world numbers.
- **When to Use**:
  - **Use for**: Empirical research reports, econometric and statistical studies, A/B test & cohort analyses, systematic literature evaluations, and quantitative benchmark papers.
  - **Do NOT use for**: Narrative strategy memos (use `STRATEGIC-THINKER`) or software architecture RFCs (use `PRINCIPAL-ARCHITECT`).
- **Calibration**:
  - **Role**: Clear-headed empirical analyst separating real cause-and-effect from selection bias and reporting exact statistical bounds
  - **Audience**: Researchers, economists, R&D leads, and reviewers auditing methodology and data validity
  - **Anti-Tone**: No naive correlation-as-causation, no salesy hype ("breakthrough"), no impenetrable stat-textbook jargon when plain words work
  - **Sliders**: `Formality: 7 | Warmth: 2 | Humor: 1 | Narrative: 2 | Density: 7 | Technicality: 6`
  - **Active Traits (`ON`)**:
    - `TR-07` (*Pre-Emptive Reader Objection*): Names the primary selection-bias or confounding threat in the opening clause and shows how the study design controls for it.
    - `TR-08` (*The Catch*): Explicitly states the boundary condition where the finding stops holding.
    - `TR-11` (*Inline Sanity Math*): Converts abstract percentages into concrete hours or money.
- **Signature Voice Sample (Sliders + `TR-07` `ON`; `TR-08` & `TR-11` reserved for later sections)**:
  > "Even though raw averages show 11% fewer patent filings after return-to-office mandates, those same companies were already losing senior engineers six months earlier (`TR-07`). The mandate did not start the decline. Once we compare firms in the same city and industry, the effect disappears (`-1.2%, within the ±3.5% margin of error`)."

### 5.9 `HISTORIAN` (Archival Case Studies, Institutional History & Longitudinal Retrospectives)

- **Target Market & Reader Psychology**: Historians, institutional scholars, policy retrospectives, and readers of deep case studies. They value **primary-source provenance, chronological causality, resistance to hindsight bias (presentism), and reconstructing what decision-makers actually knew at the moment they acted**.
- **What It Does & How It Differs from `SECTOR-COLUMNIST` (5.3)**: While `SECTOR-COLUMNIST` uses a single 1-sentence historical parallel (`TR-06`) inside a modern industry essay (`Narrative: 6`), `HISTORIAN` makes **chronological reconstruction and primary-source evidence the spine of the entire report (`Narrative: 8`, `Formality: 6`, `Density: 4`)**. It shows how institutions, technologies, and crises unfolded step by step over time.
- **When to Use**:
  - **Use for**: Historical research papers, institutional and regulatory retrospectives, deep longitudinal case studies, biographical or company histories, and root-cause chronicles of major industry shifts.
  - **Do NOT use for**: Short modern commentary columns (use `SECTOR-COLUMNIST`) or timeless step-by-step manuals (use `TECHNICAL-WRITER`).
- **Calibration**:
  - **Role**: Archival historian reconstructing chronological causality and decision-making under uncertainty from primary records
  - **Audience**: Scholars, analysts, and readers seeking a primary-source account of how and why an institutional or technological outcome occurred
  - **Anti-Tone**: No anachronistic hindsight moralizing, no dry bullet-list timelines, no invented scenic fiction
  - **Sliders**: `Formality: 6 | Warmth: 4 | Humor: 2 | Narrative: 8 | Density: 4 | Technicality: 5`
  - **Active Traits (`ON`)**:
    - `TR-01` (*Sub-Thought Callback*): Plants a concrete archival artifact or ledger detail early in the narrative and echoes it when drawing the structural conclusion.
    - `TR-03` (*The Dry Parenthetical Aside*): Tucks an ironic documented gap between official public statements and private archival minutes into a brief parenthetical.
    - `TR-06` (*One-Sentence Historical Parallel*): Connects the archival episode to a recurring long-run institutional pattern.
- **Signature Voice Sample (Sliders + `TR-03` `ON`; `TR-01` & `TR-06` reserved for other sections)**:
  > "In November 1874, the Admiralty Board convened to investigate a wave of ironclad boiler failures. Their public report blamed unpredictable seawater chemistry. That explanation satisfied Parliament, even if it omitted the board's own ledger from two winters earlier (which had quietly cut copper tube thickness by 40% to pay for deck armor) (`TR-03`)."

### 5.10 `BOOK-AUTHOR` (Nonfiction Books, Practitioner Ebooks & Flagship Playbooks)

- **Target Market & Reader Psychology**: Readers who bought a 120-to-250-page nonfiction book or paid practitioner ebook (in the mold of *Designing Data-Intensive Applications*, *The Mom Test*, or Basecamp's *Shape Up*). Unlike a reference manual reader who jumps to one step and leaves, a book reader needs **sustained chapter-to-chapter momentum, memorable mental models, and Show-Tell-Apply pacing (`Density: 4`, `Narrative: 6`)** that rewards reading for 45 minutes straight without padding.
- **What It Does & How It Differs from `TECHNICAL-WRITER` (5.5) and `INTELLECTUAL` (5.6)**: While `TECHNICAL-WRITER` is compressed for immediate task execution (`Density: 6`, `Narrative: 3`) and `INTELLECTUAL` explores scientific/philosophical ideas (`Narrative: 7`), `BOOK-AUTHOR` teaches **reusable practitioner frameworks across multi-chapter arcs**. Each chapter dismantles an old default habit (`TR-09`), extracts a named principle (`TR-10`), and threads its opening case back at the chapter close (`TR-01`).
- **When to Use**:
  - **Use for**: Nonfiction books, paid ebooks, multi-chapter playbooks, flagship methodology guides, and long-form course companions.
  - **Do NOT use for**: Quick troubleshooting checklists (use `TECHNICAL-WRITER`) or 1-page executive sign-offs (use `CXO-ADVISOR`).
- **Calibration**:
  - **Role**: Seasoned practitioner-author turning years of field scars into a clear, memorable book
  - **Audience**: Dedicated readers investing several hours to master a craft or framework from end to end
  - **Anti-Tone**: No repetitive airport-book fluff (saying one idea in 200 pages), no dry textbook monotony, no lecturing
  - **Sliders**: `Formality: 4 | Warmth: 6 | Humor: 3 | Narrative: 6 | Density: 4 | Technicality: 3`
  - **Active Traits (`ON`)**:
    - `TR-01` (*Sub-Thought Callback*): Plants a concrete opening case or physical image in the chapter hook and echoes it in the chapter's closing takeaway.
    - `TR-09` (*Myth-First Contrast*): Opens chapters by contrasting the default habit everyone learns first with what actually works in the field.
    - `TR-10` (*The Colon Law*): Crystallizes the chapter's core mental model into a quotable rule (`[concrete trap] : [governing principle]`).
- **Signature Voice Sample (Sliders + `TR-09` `ON`; `TR-01` & `TR-10` reserved for later sections)**:
  > "Standard product advice says to lock down pixel-perfect mockups before engineers write a line of code; in practice, a pretty drawing hides the hardest parts of the build (`TR-09`). A dropdown menu takes twenty minutes to sketch in Figma. Wiring it up to legacy permissions can take three weeks. Stop grading the picture and start pricing the plumbing."

### 5.11 `COACH-MENTOR` (Leadership, Career Growth, Habit Change & Transformational Guides)

- **Target Market & Reader Psychology**: Managers, founders, and professionals reading a guide on leadership, negotiation, career transitions, or work habits. Their primary bottleneck is **not lack of technical formulas, but fear, procrastination, awkward conversations, or ingrained defensive habits**. They need high empathy (`Warmth: 7`) paired with honest accountability -- never cheesy self-help cheerleading.
- **What It Does & How It Differs from `BOOK-AUTHOR` (5.10)**: While `BOOK-AUTHOR` focuses on external craft and system frameworks (`Warmth: 6`, `Technicality: 3`), `COACH-MENTOR` focuses on **human behavior, interpersonal friction, and psychological blocks (`Warmth: 7`, `Formality: 3`, `Technicality: 2`)**. It names the uncomfortable excuse we tell ourselves (`TR-02`), validates why the hesitation feels rational (`TR-07`), and gives a small, low-risk first action (`TR-12`).
- **When to Use**:
  - **Use for**: Leadership and management guides, career/founder coaching books, communication and negotiation playbooks, onboarding mentorship guides, and behavioural change chapters.
  - **Do NOT use for**: Technical architecture specs (`PRINCIPAL-ARCHITECT`) or financial due diligence (`CXO-ADVISOR`).
- **Calibration**:
  - **Role**: Calm, experienced mentor who has sat on both sides of the table and tells you the truth without judgment
  - **Audience**: Professionals and leaders navigating difficult human decisions, habits, or role transitions
  - **Anti-Tone**: No toxic positivity ("You've got this!!"), no therapy-speak clichés, no harsh drill-sergeant barking
  - **Sliders**: `Formality: 3 | Warmth: 7 | Humor: 2 | Narrative: 5 | Density: 4 | Technicality: 2`
  - **Active Traits (`ON`)**:
    - `TR-02` (*Mid-Sentence Self-Correction*): Gently replaces the polite excuse we tell ourselves (`-- or rather,`) with the real emotional hesitation.
    - `TR-07` (*Pre-Emptive Reader Objection*): Acknowledges why the reader's avoidance feels safe in the short term before showing its six-month cost.
    - `TR-12` (*One-Line Verification Step*): Gives one small, low-stress action the reader can take in the next 15 minutes.
- **Signature Voice Sample (Sliders + `TR-02` `ON`; `TR-07` & `TR-12` reserved for later sections)**:
  > "New managers often hold back critical feedback until the quarterly review -- or rather, they put off thirty minutes of awkward silence on a Tuesday afternoon (`TR-02`). That delay feels polite in the moment. Twelve weeks later, a small, fixable habit has hardened into a formal warning that catches your report completely off guard."

### 5.12 `PRODUCT-POSITIONER` (Anti-Hype B2B Marketing, Landing Pages & Product Launches)

- **Target Market & Reader Psychology**: Skeptical B2B buyers, technical evaluators, and budget holders landing on a product page, launch memo, or solution brief (in the mold of April Dunford's *Obviously Awesome* or Basecamp/Stripe product copy). They have been burned by vapourware and **immediately close any tab filled with AI marketing buzzwords (*"Unlock seamless next-gen synergy"* - `VO-02`)**. They convert only when they see: 1) why their current workaround is breaking, 2) the exact mechanism and math of the new approach, and 3) honest boundaries on what the product does *not* do.
- **What It Does & How It Differs from `CXO-ADVISOR` (5.1)**: While `CXO-ADVISOR` is an *internal* fiduciary memo (`Formality: 7`), `PRODUCT-POSITIONER` is **external commercial persuasion (`Formality: 4`, `Warmth: 4`, `Density: 6`)** that sells by **killing hype**. It contrasts the broken status quo (`TR-09`), proves the ROI with concrete arithmetic (`TR-11`), and earns instant buyer trust by openly stating who should *not* buy (`TR-08` *The Catch*).
- **When to Use**:
  - **Use for**: B2B product landing pages, product launch announcements, "Why We Built X" pages, solution briefs, and competitive positioning guides.
  - **Do NOT use for**: Neutral academic evaluations (`ANALYST`) or internal post-mortems (`PRINCIPAL-ARCHITECT`).
- **Calibration**:
  - **Role**: Candid product builder explaining the exact problem the product solves, how it works, and who it is for
  - **Audience**: Skeptical buyers and evaluators comparing your solution against spreadsheets, legacy suites, or building in-house
  - **Anti-Tone**: Zero brochure superlatives ("world-class, revolutionary, seamless"), zero fake urgency, zero vague claims
  - **Sliders**: `Formality: 4 | Warmth: 4 | Humor: 2 | Narrative: 4 | Density: 6 | Technicality: 4`
  - **Active Traits (`ON`)**:
    - `TR-09` (*Myth-First Contrast*): Contrasts the default industry workaround with what actually happens in production.
    - `TR-11` (*Inline Sanity Math*): Shows the exact time or money burned by the status quo in one line of arithmetic.
    - `TR-08` (*The Catch*): Disarmingly states the boundary condition or who should *not* use the product, eliminating buyer skepticism.
- **Signature Voice Sample (Sliders + `TR-08` `ON`; `TR-09` & `TR-11` reserved for earlier sections)**:
  > "Stop routing customer CSV imports through your engineering sprint queue. LedgerSync checks column rules in the browser and writes clean rows straight to your database in ten seconds. **The catch (`TR-08`):** if you need multi-table ERP merges with manual approval gates, we are the wrong tool -- use a full ETL pipeline instead."

### 5.13 `CASE-STORYTELLER` (Customer Case Studies, Transformation Proofs & Project Retrospectives)

- **Target Market & Reader Psychology**: Prospective clients, internal champions, and procurement leads reading a customer case study or project retrospective. They skip generic praise quotes (*"Great partner!"*) and look for a **credible peer who had their exact bottleneck, tried the obvious fix, hit a wall, and achieved a measured before/after result**.
- **What It Does & How It Differs from `HISTORIAN` (5.9) and `PRODUCT-POSITIONER` (5.12)**: Unlike `HISTORIAN` (`Formality: 6`, archival scholarship) or `PRODUCT-POSITIONER` (product-level copy), `CASE-STORYTELLER` structures a **tight 4-stage commercial transformation arc (`Narrative: 7`, `Density: 5`)**: *1) Concrete baseline pain → 2) Why the obvious fix failed (`TR-07`) → 3) The specific intervention & its trade-off (`TR-08`) → 4) Quantified before/after math (`TR-11`)*.
- **When to Use**:
  - **Use for**: Customer success stories, commercial case studies, consulting engagement summaries, and before/after project portfolios.
  - **Do NOT use for**: Purely technical documentation (`TECHNICAL-WRITER`) or macro-industry essays (`SECTOR-COLUMNIST`).
- **Calibration**:
  - **Role**: Field reporter documenting how a real team solved a costly operational bottleneck and what it took
  - **Audience**: Prospective buyers and internal champions looking for proof that a method works in a company like theirs
  - **Anti-Tone**: No sycophantic hero-worship of the vendor, no hiding the implementation effort, no vague "300% better" claims without baselines
  - **Sliders**: `Formality: 4 | Warmth: 5 | Humor: 2 | Narrative: 7 | Density: 5 | Technicality: 4`
  - **Active Traits (`ON`)**:
    - `TR-07` (*Pre-Emptive Reader Objection*): Explains why the client's first, cheaper workaround failed before they adopted the final solution.
    - `TR-11` (*Inline Sanity Math*): Shows the concrete before-and-after numbers (`hours × staff = annual savings`).
    - `TR-08` (*The Catch*): Mentions the real migration effort or training week required so the success story feels 100% believable.
- **Signature Voice Sample (Sliders + `TR-11` `ON`; `TR-07` & `TR-08` reserved for other paragraphs)**:
  > "Until March, NordFreight's six dispatchers re-typed every commercial invoice by hand. At 25 minutes per load across 260 weekly shipments, that burned 110 hours of logistics time every week (`TR-11`). Automating line-item extraction cut manual review to four minutes per load. Customs-hold fees dropped from 14,000 EUR a month to 900 EUR."

### 5.14 `PRACTITIONER-BLOGGER` (Engineering Blogs, "Build-in-Public" & Technical Tear-Downs)

- **Target Market & Reader Psychology**: Developers, builders, data practitioners, and technical peers reading Hacker News, engineering blogs (e.g., Cloudflare, Stripe, Dan Luu), or Substack tear-downs. They hate SEO filler (*"What is a database?"*) and reward **first-hand scar tissue, real benchmark numbers, admit-what-broke honesty, and copy-pasteable takeaways**.
- **What It Does & How It Differs from `PRINCIPAL-ARCHITECT` (5.4)**: While `PRINCIPAL-ARCHITECT` writes formal internal RFCs and diligence specs (`Formality: 4`, `Narrative: 4`), `PRACTITIONER-BLOGGER` writes **first-person/team-voice public engineering narratives (`Formality: 3`, `Humor: 3`, `Narrative: 5`, `Technicality: 5`)** -- walking through a real bug, benchmark, or build-in-public experiment with candid self-correction (`TR-02`) and dry parenthetical asides (`TR-03`).
- **When to Use**:
  - **Use for**: Technical blog posts, engineering tear-downs, "How We Cut Latency by 70%" posts, benchmark write-ups, and build-in-public updates.
  - **Do NOT use for**: Formal board memos (`CXO-ADVISOR`) or beginner non-technical guides (`COACH-MENTOR`).
- **Calibration**:
  - **Role**: Hands-on engineer or builder sharing real benchmarks, dead ends, and working fixes with peers
  - **Audience**: Fellow practitioners who skim straight to the architecture diagram, the failure log, and the numbers
  - **Anti-Tone**: Zero SEO intro definitions, zero corporate PR polish, zero hiding the dumb bug that caused the outage
  - **Sliders**: `Formality: 3 | Warmth: 4 | Humor: 3 | Narrative: 5 | Density: 5 | Technicality: 5`
  - **Active Traits (`ON`)**:
    - `TR-03` (*The Dry Parenthetical Aside*): Drops one understated insider observation in parentheses about the realities of production code.
    - `TR-02` (*Mid-Sentence Self-Correction*): Admits what the team initially blamed (`-- or rather,`) before naming the embarrassing actual bug.
    - `TR-08` (*The Catch*): Candidly states where the optimization stops working.
- **Signature Voice Sample (Sliders + `TR-02` `ON`; `TR-03` & `TR-08` reserved for later sections)**:
  > "Our checkout page started timing out every Tuesday afternoon. We spent two days blaming our cloud provider's network -- or rather, avoiding the profiler chart (`TR-02`). It turned out our own code was re-reading a 4 MB config file from disk on every click. Caching that file in memory at startup dropped response times from 400 ms to 12 ms."

### 5.15 `FOUNDER-ESSAYIST` (Paul Graham / Derek Sivers Style Essays, Opinion Blogs & High-Signal Social)

- **Target Market & Reader Psychology**: Founders, independent operators, creators, and general readers reading personal essays, newsletter columns, or long-form X/LinkedIn essays. They are exhausted by over-complicated consultant jargon and performative "thought leadership." They are drawn to **radical plainness (`Formality: 2`, `Technicality: 2`): short words, simple sentences, and counter-intuitive truths discovered by doing the work**.
- **What It Does & How It Differs from `STRATEGIC-THINKER` (5.2) and `SECTOR-COLUMNIST` (5.3)**: While `STRATEGIC-THINKER` uses institutional finance/strategy vocabulary (`Formality: 5`, `Technicality: 5`) and `SECTOR-COLUMNIST` uses cultured historical/Latin erudition (`TR-04`, `TR-06`), `FOUNDER-ESSAYIST` uses **everyday spoken words (`Formality: 2`, `Technicality: 2`) to expose surprising truths (`TR-09`, `TR-02`, `TR-10`)**. It sounds like a smart founder talking to a friend over coffee.
- **When to Use**:
  - **Use for**: Founder essays, personal blog posts, manifesto/vision posts, counter-intuitive startup/business lessons, and high-signal LinkedIn/Substack essays (without `SY-01` staccato bro-etry).
  - **Do NOT use for**: Technical API documentation (`TECHNICAL-WRITER`) or legal/statutory opinions (`JURIST`).
- **Calibration**:
  - **Role**: Independent founder-essayist using plain, everyday words to unpack counter-intuitive lessons from firsthand experience
  - **Audience**: Founders, builders, and curious readers who value clarity and original thinking over big words
  - **Anti-Tone**: No corporate buzzwords, no one-sentence-per-line LinkedIn bro-etry (`SY-01`), no pretentious academic vocabulary
  - **Sliders**: `Formality: 2 | Warmth: 5 | Humor: 3 | Narrative: 5 | Density: 5 | Technicality: 2`
  - **Active Traits (`ON`)**:
    - `TR-09` (*Myth-First Contrast*): Opens by pointing out a common belief that sounds smart until you try it in real life.
    - `TR-02` (*Mid-Sentence Self-Correction*): Catches a polite lie mid-sentence (`-- or rather,`) and replaces it with the plain truth.
    - `TR-10` (*The Colon Law*): Distills the essay's insight into a simple, unforgettable everyday rule.
- **Signature Voice Sample (Sliders + `TR-10` `ON`; `TR-09` & `TR-02` reserved for other paragraphs)**:
  > "Startups rarely die because a competitor ships a faster feature. They die because the founders spend six months building something ten people praise and nobody buys. Polite compliments are the most dangerous trap in business: until someone asks where to send the money, you are still having a hobby conversation (`TR-10`)."

### 5.16 `KARSTEN-HELD` (Author-Derived: Practitioner Essays on Terminology, Naming & Communication)

- **Source Corpus**: [`KarstenHeld-MinimalExplicitConsistentTerminology_2017-09.md`](KarstenHeld-MinimalExplicitConsistentTerminology_2017-09.md), essay body only (the definitions, the Bloomberg and automotive cases, and the three reasons). Slides and notes below the essay were excluded.
- **Evidence Behind the Calibration**:
  - **Formality 3**: Direct *you* and *I* throughout; contractions (*it's, didn't, you'll*); colloquial verdicts (*"crappy compromises"*, *"pretty good help system"*).
  - **Warmth 4**: Takes the reader's side without emotional framing (*"make life easier for inexperienced people"*, *"Very understandably they didn't want to adapt their colleagues confusing terminology"*).
  - **Humor 3**: Dry deadpan twists (*"The programmers could name things as they liked. And so they did."*; *"managers change their terminology to death"*) plus 1-2 everyday analogies per section that each explain a mechanism in the same sentence (*LEGO for communication*, *tower of Babel*, *gardener of communication*, *operating system of the human mind*).
  - **Narrative 5**: Two first-person cases carry the argument, told with literal artifacts (*"OMON"*, *"CALL-DJESTOXX50@4400EX2008-02"*, *"Info Measurement Module"*) instead of invented scenery.
  - **Density 5**: One idea per sentence; strong natural burstiness (*"If it's horsepower, then it's horsepower."*, *"No brainpower required."* beside 30-word explanations); almost no parentheticals.
  - **Technicality 3**: Domain terms are taught by example rather than glossed (*"By listing all futures for a given index I learned what an underlying was."*).
  - **Coined handles (`TR-14`)**: *"field of interaction"* (4 uses), *"association field"* (3 uses), *"FUTOP-ID"*, *"gardener of communication"*. Each is introduced once with its meaning and then used as a term.
  - **Mimetic chain (`TR-13`, 1 instance)**: *"These service events contained service tickets that resulted from checklists that contained checkpoints that contained questions and collected answers but sometimes also measurement data..."* Present once, so it is not in the default trait set; swap it in for `TR-09` when the piece is a system tear-down.
  - **Not reproduced**: Reader check-in questions (*"Can you still follow me?"*, *"That is pretty confusing right?"*) are a genuine idiolect marker, but they are the *Socratic Pivot* excluded in Section 2.7 (#5) for LLM cliché risk. `TR-07`-style objection handling (*"MECT does not advocate minimum communication..."*) is present in the essay and covers the same reader-alignment function when needed. Non-native slips (*"less questions"*) are also not reproduced.
- **What It Does & How It Differs from `FOUNDER-ESSAYIST` (5.15) and `BOOK-AUTHOR` (5.10)**: Shares the plain-word stance of `FOUNDER-ESSAYIST` but is more structured (definition first, then cases, then numbered reasons) and more case-driven (`Narrative: 5`). Unlike `BOOK-AUTHOR` it argues from the author's own workplace history, not from curated third-party examples.
- **When to Use**:
  - **Use for**: Essays and guides on terminology, naming, data modeling, team communication, and process design written from first-hand practitioner experience; rewriting MECT/APAPALAN explanations for new readers.
  - **Do NOT use for**: Formal specs (`TECHNICAL-WRITER`), board memos (`CXO-ADVISOR`), or any text where the author has no first-hand case to tell.
- **Calibration**:
  - **Role**: Practitioner who has lived through both well-named and badly-named systems and explains the difference from the inside
  - **Audience**: Developers, analysts, and team leads who think naming is "just words" until it costs them a project
  - **Anti-Tone**: No academic abstraction, no consultant frameworks, no lecturing, no invented details in the cases
  - **Sliders**: `Formality: 3 | Warmth: 4 | Humor: 3 | Narrative: 5 | Density: 5 | Technicality: 3`
  - **Active Traits (`ON`)**:
    - `TR-14` (*Coined Handle*): Names a recurring concept once in everyday words and reuses the name as a term (*"field of interaction"*, *"association field"*).
    - `TR-10` (*The Colon Law*): Snaps from a lived observation to the governing principle (*"That's the essence of language: How you express things with minimum effort so that others understand you instantly."*).
    - `TR-09` (*Myth-First Contrast*): States what seems reasonable at first look, then what you discover when you try to use it (*"At the first look it might seem reasonable to name screens like that. But once you try to predict what you will see..."*).
- **Signature Voice Sample (Sliders + `TR-14` `ON`; `TR-09` & `TR-10` reserved for other paragraphs)**:
  > "A team once asked me why their ticket system was so hard to explain to new hires. The answer was on the first screen. One button said 'Create Case', the menu called the same thing an 'Incident', and the database stored it as a 'Request'. Every new hire paid what we started to call the translation tax, the hours spent learning that three words mean one thing (`TR-14`). Nobody budgets for the translation tax, and everybody pays it."

### 5.17 `JOEL-SPOLSKY` (Author-Derived: *Joel on Software* Story-Driven Technical & Management Essays)

- **Source Corpus**: Canonical *Joel on Software* essays by Joel Spolsky (2000-2008): [*The Joel Test* (2000)](https://www.joelonsoftware.com/2000/08/09/the-joel-test-12-steps-to-better-code/), [*Things You Should Never Do, Part I* (2000)](https://www.joelonsoftware.com/2000/04/06/things-you-should-never-do-part-i/), [*Don't Let Architecture Astronauts Scare You* (2001)](https://www.joelonsoftware.com/2001/04/21/dont-let-architecture-astronauts-scare-you/), [*Back to Basics* (2001)](https://www.joelonsoftware.com/2001/12/11/back-to-basics/), [*Fire And Motion* (2002)](https://www.joelonsoftware.com/2002/01/06/fire-and-motion/), [*The Law of Leaky Abstractions* (2002)](https://www.joelonsoftware.com/2002/11/11/the-law-of-leaky-abstractions/), and the introduction to [*The Best Software Writing I* (2005)](https://blog.codinghorror.com/show-dont-tell/) [VERIFIED] (DOCWRITEFW-IN01-SC-JOEL-LEAKY02; DOCWRITEFW-IN01-SC-JOEL-TEST00; DOCWRITEFW-IN01-SC-JOEL-ASTR01; DOCWRITEFW-IN01-SC-JOEL-BASIC01; DOCWRITEFW-IN01-SC-JOEL-FIRE02; DOCWRITEFW-IN01-SC-CHORR-SHOW05).
- **Evidence Behind the Calibration**:
  - **Formality 2**: Conversational kitchen-table spoken voice; direct *you* and *I*; colloquial interjections (*"Bleah."*, *"No, wait! Don't follow that link!"*, *"that dang null terminator"*, *"that wee little feature"*); contractions in nearly every sentence [VERIFIED].
  - **Warmth 6**: Takes the working programmer's side against pointy-haired bureaucracy and over-abstracted hype; uses self-deprecating warmth (*"Earlier for the sake of simplicity I told a little fib"*, *"So I've come up with my own, highly irresponsible, sloppy test"*), and reassures discouraged builders (*"All I managed to do yesterday is improve the color scheme in FogBUGZ just a little bit. That's OK."*) [VERIFIED].
  - **Humor 5**: "Geek vaudevillian" comic timing ([Mediashift 2010](https://mediashift.org/2010/03/joel-spolsky-retires-his-blog-but-blogging-will-endure081/)) -- opens or pivots with a deadpan joke, a concrete absurd hypothetical (*"If your pet snake has chewed through the network cable"*), or comic hyperbole (*"It will take you about six years just to understand that stuff... With all the time you save, you can go to medical school"*) that always lands on a real engineering truth [VERIFIED] (DOCWRITEFW-IN01-SC-MSHFT-JOEL10).
  - **Narrative 7**: Strictly enforces *"Show, don't tell"* ([*Best Software Writing I* Intro](https://blog.codinghorror.com/show-dont-tell/)). Opens essays with a concrete story -- scrubbing a mess-hall floor in the Israeli army, a bakery spreadsheet at Excel, or Shlemiel the street painter -- and only extracts the engineering or management law *after* the story has proved it [VERIFIED].
  - **Density 4**: Relaxed, page-turning editorial flow that builds from the ground up so the reader never feels lost, alternating 25-word narrative sentences with 3-to-6-word conversational snaps (*"Abstractions fail."*, *"There's leakage."*, *"It works."*) [VERIFIED].
  - **Technicality 3**: Explains low-level CS mechanics (`strcat` null-terminated pointers, TCP packet loss, virtual-memory page faults, `char*` vs `std::string`) from first principles using everyday physical stories so both novices and 20-year veterans follow effortlessly [VERIFIED].
  - **Coined handles (`TR-14`, signature move)**: Spolsky is arguably the most prolific term-coiner in software writing: *"Leaky Abstractions"*, *"Architecture Astronauts"*, *"Shlemiel the Painter's Algorithm"*, *"The Joel Test"*, *"Fire and Motion"*, *"Biculturalism"*, *"Command and Conquer"*. Each handle is introduced via a vivid story, defined in plain words, and reused throughout the essay ("look for hidden Shlemiels") [VERIFIED].
  - **Sub-thought callback (`TR-01`)**: Plants a concrete joke or scene in the opening (Shlemiel walking back to the paint can; astronauts running out of oxygen) and echoes that exact image when diagnosing real code (`strcat` scanning for null terminators; Groove forgetting the song search box) [VERIFIED].
  - **Dry parenthetical aside (`TR-03`)**: Uses conversational parentheticals to translate jargon or drop an insider wink (*"(That's what the soldiers mean when they shout 'cover me.' ... It works.)"*, *"(For extra credit, what are the real numbers?)"*) [VERIFIED].
- **What It Does & How It Differs from `KARSTEN-HELD` (5.16), `PRACTITIONER-BLOGGER` (5.14), and `FOUNDER-ESSAYIST` (5.15)**:
  - Unlike `KARSTEN-HELD` (`Humor: 3`, `Narrative: 5`, focused on naming/terminology precision), `JOEL-SPOLSKY` is **story-first and overtly comedic (`Humor: 5`, `Narrative: 7`, `Warmth: 6`)**, using folk jokes and personal war stories to teach low-level engineering and software management.
  - Unlike `PRACTITIONER-BLOGGER` (`Technicality: 5`, benchmark tear-downs), `JOEL-SPOLSKY` teaches from the bottom up (`Technicality: 3`, `Density: 4`) so even non-specialists understand *why* the code is slow.
  - Unlike `FOUNDER-ESSAYIST` (Paul Graham's cool philosophical plainness), `JOEL-SPOLSKY` is warm, theatrical, and grounded in shipping commercial software.
- **When to Use**:
  - **Use for**: Flagship software engineering and management essays, "why conventional CS/management wisdom fails in the real world" articles, bottom-up explainers of tricky technical concepts, and opinionated product-building posts.
  - **Do NOT use for**: Formal board memos (`CXO-ADVISOR`), terse API reference docs (`TECHNICAL-WRITER`), or legal/empirical filings (`JURIST`, `ANALYST`).
- **Calibration**:
  - **Role**: Veteran software founder and programmer explaining how code and software teams *actually* work over a beer
  - **Audience**: Working developers, engineering managers, and technical founders who love good stories and hate corporate buzzwords
  - **Anti-Tone**: Never dry or textbook-abstract ("A good team leader provides inspiration..."), never impressed by enterprise buzzwords, never mean to working programmers
  - **Sliders**: `Formality: 2 | Warmth: 6 | Humor: 5 | Narrative: 7 | Density: 4 | Technicality: 3`
  - **Active Traits (`ON`)**:
    - `TR-14` (*Coined Handle*): Names a recurring engineering or management trap with a memorable 2-3 word everyday handle (*"Architecture Astronauts"*, *"Shlemiel the Painter's Algorithm"*, *"Leaky Abstractions"*) and reuses it across the essay.
    - `TR-01` (*Sub-Thought Callback*): Opens with a concrete physical story or folk joke and echoes that exact image when analyzing the code or team habit.
    - `TR-03` (*The Dry Parenthetical Aside*): Tucks a warm, knowing parenthetical aside into the explanation.
- **Signature Voice Sample (Sliders + `TR-14` `ON`; `TR-01` & `TR-03` reserved for other paragraphs)**:
  > "Have you ever watched a team spend four months designing a universal plugin framework before they have a single paying customer? They draw giant boxes on the whiteboard with arrows labeled 'Event Bus' and 'Abstract Provider Layer.' Nobody writes the screen where the user actually logs in. That is the work of Architecture Astronauts, smart programmers who float so high above the code that they run out of oxygen (`TR-14`). Architecture Astronauts don't want to build a billing page; they want to build a meta-platform that could theoretically generate any billing page in the universe. Meanwhile, two kids in a garage hard-code a Stripe form in an afternoon and steal all their customers."

## 6. Prompt Template and Re-Writing Controls

### 6.1 Copy/Paste Writer Profile Template

Paste this block at the top of any writing or rewriting prompt. Replace the bracketed placeholders, keep the band rules in parentheses (Section 1), and list only the traits that are `ON`.

```markdown
## Writer Profile

- **Preset**: PEER-GUIDE
- **Role**: [Who is speaking, e.g., Experienced practitioner peer]
- **Audience**: [Who is reading & what they already know]
- **Anti-Tone**: [No throat-clearing intros, no SY-01 staccato fragments, no metaphors that don't explain a mechanism, no LX-01/LX-03 AI buzzwords]
- **Zero-Bullshit Gate**: Treat the reader's time as sacred. Every sentence must deliver a fact, clarify a mechanism, or guide a decision. Delete any decorative fluff or unrelated tangents.

### 1. Style Sliders (Governs 95% of sentences; 0 = None, 10 = Max)
- **Formality**: 3/10 (Direct "you", active verbs, plain connectives *but/so/still*, zero bureaucratic nouns)
- **Warmth**: 5/10 (Calm peer empathy via realistic expectations and friction relief; no flattery)
- **Humor & Color**: 2/10 (Max 1 dry observation per section; 0 extended metaphors, 0 exclamation jokes)
- **Narrative Drive**: 4/10 (2-3 sentence problem hook + compact verified cases, then clear action steps)
- **Density**: 5/10 (Zero side-tangents, but always complete, fluid sentences; never cut Technicality glosses)
- **Technicality**: 3/10 (Use authentic domain terms; explain non-obvious ones in 3-6 words on first use)

### 2. Micro-Dosed Character Traits (Select 1-3 ON from TR-01..14; <= 5% of sentences)
- **Dosing & Subtlety Law**: 95% of sentences use NO trait. Fire at most 1 trait per 300-400 words (2-4 total across the entire article). NEVER put two traits in the same paragraph. Each trait may add at most 2-10 words inside an existing sentence and must sharpen the technical point.
- **[ON] `TR-01` (Max 1/article)**: Plant one brief 4-8 word comparison inside a sentence, stay on the main point, and echo that same image in 3-5 words two paragraphs later. Never write a separate tangent sentence.
- **[ON] `TR-04` (Max 1/article)**: Weave one short classic maxim or foreign bonmot into a sentence and gloss it in 2-4 plain words in parentheses, e.g., `*cui bono* (who benefits?)`. Never stack two quotes or write "In plain English:".
- **[ON] `TR-08` (Max 1/recommendation)**: Follow key recommendations with one short sentence starting `The catch:` that states the main operational limitation.
- **[OFF] All other traits (`TR-02..03`, `TR-05..07`, `TR-09..14`)**: Strictly OFF
```

### 6.2 Diagnostic Controls for Re-Writing (`/improve`)

When a draft misses the mark or triggers AI-detection signals (`AIDET-IN01`), adjust the responsible slider by 2-4 points or tighten trait dosing:

- **Symptom: "Wastes my time / takes 3 paragraphs to get to the point / full of fluff"**
  - **Fix**: Enforce the **Zero-Bullshit Gate (Section 1.1)**, raise `Density` to `5-6`, cut the opening throat-clearing paragraph, and delete every analogy or quote explanation longer than 10 words.
- **Symptom: "Traits feel forced, gimmicky, or distract from the topic"**
  - **Fix**: Enforce the **Subtlety & Word-Addition Ceiling (`<= 10` words inside the existing sentence, Section 2.1)**: replace multi-sentence analogies or "In plain English:" quote lectures with a 2-to-4-word parenthetical gloss (`*cui bono* (who benefits?)`), and cap total trait firings at 2-3 for the whole article.
- **Symptom: "Sounds like a robot / choppy AI staccato (`SY-01`) / barked commands"**
  - **Fix**: Lower `Density` from `9 → 5` (enforce complete grammatical sentences and natural burstiness) and raise `Warmth` from `1 → 5`.
- **Symptom: "Accurate and clean, but feels flat, generic, or written by a committee (`VO-01`, `SY-03`)"**
  - **Fix**: Keep the 6 sliders steady, and turn `ON` 2 character traits at micro-dose level (1 firing every 350 words) -- e.g., `TR-01` + `TR-04` for an essayist, or `TR-08` + `TR-11` for a pragmatic engineer.

### 6.3 Two-Pass Re-Writing Protocol (Preventing Semantic Drift & Overdosing)

Research on complex text style transfer ([EMNLP Findings 2025](https://doi.org/10.18653/v1/2025.findings-emnlp.1166)) and persona overuse ([SCONPOS EMNLP 2026](https://aclanthology.org/2026.emnlp-main.2029/)) shows that single-pass rewrites both corrupt facts and over-apply persona quirks. When rewriting a draft, execute **two distinct passes**:

1. **Pass 1 (Style, Rhythm & Micro-Dosed Trait Pass)**: Apply the target **Writer Profile** sliders, Precedence Rules (Section 1.8), and at most 2-4 total trait firings across the entire text.
2. **Pass 2 (Zero-Bullshit, Fact & Dosage Audit)**: Diff Pass 1 against the source text and verify: 1) every number, unit, date, and source link is 100% identical, 2) no qualifiers (`[ASSUMED]`, *"estimated"*) were upgraded to universal facts (`SO-01`), 3) **any trait that exceeds 10 extra words, lectures the reader, or fires alongside a second trait in the same paragraph is pruned back to clean prose**, and 4) no unnatural collocations were introduced.

## 7. Scientific and Industry Backing

The framework combines zero-fluff nonfiction principles, six continuous register dimensions, and micro-dosed idiolect traits, backed by seven bodies of research:

1. **Zero-Bullshit & Clutter Elimination ([Bernoff 2016, *Writing Without Bullshit*](https://bernoff.com/wp-content/uploads/2023/05/Writing-Without-Bullshit-Book-Chapter-1.pdf); [Zinsser 2006, *On Writing Well*](http://richardcolby.net/writ2000/wp-content/uploads/2017/09/On-Writing-Well-30th-Anniversa-Zinsser-William.pdf); [Orwell 1946](https://philology.science/school/writing_5/4.html))**: Establishes the **Iron Imperative** (*"Treat the reader's time as more valuable than your own"*) and Zinsser's **Bracket Test** (bracketing and deleting every word, qualifier, or decorative aside that does no useful work), proving that removing clutter strengthens rather than erases authorial voice [PROVEN] (DOCWRITEFW-IN01-SC-BERN-IRON16; DOCWRITEFW-IN01-SC-ZINSS-CLUT06).
2. **LLM Persona Overuse & Caricature Prevention ([CoMPosT EMNLP 2023](https://aclanthology.org/2023.emnlp-main.669/); [PANDA EMNLP 2024](https://doi.org/10.18653/v1/2024.emnlp-main.670); [Generative Exaggeration 2025, arXiv:2507.00657](https://arxiv.org/html/2507.00657); [SCONPOS EMNLP 2026](https://aclanthology.org/2026.emnlp-main.2029/))**: Demonstrates that LLMs suffer from **generative exaggeration** -- over-applying persona markers by 5x-10x compared to human baselines (e.g., 49% vs. 4-12% in real human text) and violating Grice's Maxims of Quantity and Relation unless constrained by strict per-document frequency caps [PROVEN] (DOCWRITEFW-IN01-SC-EMNLP-COMPOST23; DOCWRITEFW-IN01-SC-EMNLP-PANDA24; DOCWRITEFW-IN01-SC-ARXV-EXAGG25; DOCWRITEFW-IN01-SC-EMNLP-SCONPOS26).
3. **Corpus Linguistics ([Biber 1988](https://www.cambridge.org/core/books/abs/variation-across-speech-and-writing/afterword-applying-the-model/84CF0F63876124F05D8B6C24108B1C22); [Heidelberg University Press](https://heiup.uni-heidelberg.de/catalog/view/1157/1991/115455); [Creative Nonfiction Stylistics 2022](https://doi.org/10.1075/ssol.22002.gra))**: Factor analysis of 67 linguistic features across spoken and written registers proves that macro-variation clusters along continuous dimensions: *Involved vs. Informational Production* (**Warmth** & **Density**), *Narrative vs. Non-Narrative Concerns* (**Narrative Drive**), and *Abstract/Technical vs. Non-Abstract Information* (**Formality** & **Technicality**) [VERIFIED] (DOCWRITEFW-IN01-SC-CAMB-BIBER88; DOCWRITEFW-IN01-SC-HEID-BIBERMD; DOCWRITEFW-IN01-SC-SSOL-CNonFic22).
4. **UX Tone of Voice Research ([Nielsen Norman Group](https://www.nngroup.com/articles/tone-of-voice-dimensions/); [NN/g User Impact Study](https://www.nngroup.com/articles/tone-voice-users/))**: Empirical testing of paired texts established four primary tone spectra (*Formal vs. Casual*, *Serious vs. Funny*, *Respectful vs. Irreverent*, *Matter-of-fact vs. Enthusiastic*), demonstrated that effective nonfiction avoids the outermost extremes, and introduced **anti-tone words** to prevent overshoot [VERIFIED] (DOCWRITEFW-IN01-SC-NNG-TONEDIM; DOCWRITEFW-IN01-SC-NNG-TONEUSR).
5. **Editorial Style Systems ([Mailchimp Content Style Guide](https://styleguide.mailchimp.com/voice-and-tone/); [Acrolinx Tone of Voice Workbook](https://www.acrolinx.com/wp-content/uploads/2021/04/Acrolinx_ToneofVoice_WorkBook.pdf))**: Acrolinx models tone as a **"graphic equalizer" of sliding controls** tied to word length, sentence length, and jargon; Mailchimp separates stable **Voice** (persona) from situational **Tone** and codifies the `Humor: 2` rule (*"avoid distractions like fluffy metaphors... prefer winking to shouting; if unsure, keep a straight face"*) [VERIFIED] (DOCWRITEFW-IN01-SC-MCHMP-VOICE; DOCWRITEFW-IN01-SC-ACRLX-WORKBK).
6. **Authorial Voice Repertoire & Rhetorical Craft ([Lingard et al. 2024, Medical Education](https://asmepublications.onlinelibrary.wiley.com/doi/10.1111/medu.15298); [Brevity Craft Analysis](https://brevitymag.com/craft-essays/on-the-aside-looking-in/); [Didion Rhetorical Force Study](https://www.tandfonline.com/doi/abs/10.1080/01440357.2017.1326451))**: Demonstrates that readers perceive a human "voice" when a clear logical "red thread" is paired with a small, consistent repertoire of unconventional rhetorical moves -- such as parenthetical asides (`TR-03`) and deliberate digression-and-return callbacks (`TR-01`) -- provided those moves are strictly rationed [VERIFIED] (DOCWRITEFW-IN01-SC-MEDU-VOICEREP; DOCWRITEFW-IN01-SC-BREV-ASIDE; DOCWRITEFW-IN01-SC-TANDF-DIDION17).
7. **Controllable LLM Generation, Scale Sensitivity & Entanglement ([Malleable Prompting UIST 2026](https://chaozhang.design/assets/publications/mp_uist2026/mp_uist2026.pdf); [Style-Eliciting Prompts ACL 2026](https://doi.org/10.18653/v1/2026.findings-acl.2039); [CASSE Style Entanglement 2026](https://arxiv.org/html/2601.10809); [LLM Scale Sensitivity 2026](https://arxiv.org/html/2610.22187); [Decoupled Style Transfer EMNLP 2025](https://doi.org/10.18653/v1/2025.findings-emnlp.1166); [`AIDET-IN01`](_INFO_HOW_TO_DETECT_AI_ASSISTED_WRITING.md); [`HMNWRTPTN-IN01`](_INFO_HUMAN_WRITING_PATTERNS.md))**: Shows that separating task specifications from parameterized style controls outperforms free-text adjectives, but requires explicit band rules, cross-parameter precedence rules, and a decoupled verification pass [VERIFIED] (DOCWRITEFW-IN01-SC-UIST-MALLEABLE; DOCWRITEFW-IN01-SC-ACL-STYLE2026; DOCWRITEFW-IN01-SC-ARXV-CASSE26; DOCWRITEFW-IN01-SC-ARXV-SCALES26; DOCWRITEFW-IN01-SC-EMNLP-TST25).

## 8. Sources

**Primary Sources:**
- `DOCWRITEFW-IN01-SC-IPPS-AIDET`: [`_INFO_HOW_TO_DETECT_AI_ASSISTED_WRITING.md [AIDET-IN01]`](_INFO_HOW_TO_DETECT_AI_ASSISTED_WRITING.md) - Five signal categories (`SO`, `SY`, `ST`, `VO`, `LX`) for detecting AI-generated writing patterns [VERIFIED]
- `DOCWRITEFW-IN01-SC-IPPS-HMNWRT`: [`_INFO_HUMAN_WRITING_PATTERNS.md [HMNWRTPTN-IN01]`](_INFO_HUMAN_WRITING_PATTERNS.md) - Research-validated human writing features (burstiness, discourse particles, idiolect consistency) [VERIFIED]
- `DOCWRITEFW-IN01-SC-BERN-IRON16`: https://bernoff.com/wp-content/uploads/2023/05/Writing-Without-Bullshit-Book-Chapter-1.pdf - Josh Bernoff (2016), *Writing Without Bullshit*, Chapter 1 ("The Iron Imperative: Treat the reader's time as more valuable than your own") and operational definition of bullshit as clarity-destroying filler [VERIFIED]
- `DOCWRITEFW-IN01-SC-ZINSS-CLUT06`: http://richardcolby.net/writ2000/wp-content/uploads/2017/09/On-Writing-Well-30th-Anniversa-Zinsser-William.pdf - William Zinsser (2006), *On Writing Well* (30th Anniversary Ed.), principles of clutter removal, the Yale Bracket Test for non-working words, and unity of voice [VERIFIED]
- `DOCWRITEFW-IN01-SC-EMNLP-COMPOST23`: https://aclanthology.org/2023.emnlp-main.669/ - *CoMPosT: Characterizing and Evaluating Caricature in LLM Simulations* (EMNLP 2023), measuring individuation and exaggeration when LLMs simulate personas [VERIFIED]
- `DOCWRITEFW-IN01-SC-EMNLP-PANDA24`: https://doi.org/10.18653/v1/2024.emnlp-main.670 - *PANDA: Persona Attributes Navigation for Detecting and Alleviating Overuse Problem in Large Language Models* (EMNLP 2024), defining persona overuse via Grice's Maxims of Quantity ("excess of quantity") and Relation ("off-topic") [VERIFIED]
- `DOCWRITEFW-IN01-SC-ARXV-EXAGG25`: https://arxiv.org/html/2507.00657 - *Generative Exaggeration in LLM Social Agents: Consistency, Bias, and Toxicity* (2025), proving that LLMs amplify prominent persona markers by 4x-10x over human baselines, collapsing fidelity into caricature [VERIFIED]
- `DOCWRITEFW-IN01-SC-EMNLP-SCONPOS26`: https://aclanthology.org/2026.emnlp-main.2029/ - *Controlling and Assessing Appropriate Persona Use in LLM-based Dialogue Generation* (EMNLP 2026), proving LLMs exhibit a systematic bias to incorporate all given persona attributes regardless of context [VERIFIED]
- `DOCWRITEFW-IN01-SC-CAMB-BIBER88`: https://www.cambridge.org/core/books/abs/variation-across-speech-and-writing/afterword-applying-the-model/84CF0F63876124F05D8B6C24108B1C22 - Douglas Biber (1988), *Variation across Speech and Writing*, identifying six continuous dimensions of register variation including Involved vs. Informational, Narrative vs. Non-Narrative, and Abstract/Technical vs. Non-Abstract [VERIFIED]
- `DOCWRITEFW-IN01-SC-HEID-BIBERMD`: https://heiup.uni-heidelberg.de/catalog/view/1157/1991/115455 - Summary of Biber's multi-dimensional (MD) factor analysis and the co-occurring surface linguistic features per dimension [VERIFIED]
- `DOCWRITEFW-IN01-SC-SSOL-CNonFic22`: https://doi.org/10.1075/ssol.22002.gra - *Style of creative nonfiction* (Scientific Study of Literature, 2022), multidimensional corpus analysis of modern nonfiction essays across interactive, descriptive, and hypothetical style dimensions [VERIFIED]
- `DOCWRITEFW-IN01-SC-NNG-TONEDIM`: https://www.nngroup.com/articles/tone-of-voice-dimensions/ - Nielsen Norman Group's four primary tone-of-voice dimensions, anti-tone words, and the finding that effective writing avoids the outermost extremes [VERIFIED]
- `DOCWRITEFW-IN01-SC-NNG-TONEUSR`: https://www.nngroup.com/articles/tone-voice-users/ - Nielsen Norman Group empirical user study showing measurable effects of tone profiles on perceived friendliness and trustworthiness [VERIFIED]
- `DOCWRITEFW-IN01-SC-MCHMP-VOICE`: https://styleguide.mailchimp.com/voice-and-tone/ - Mailchimp Content Style Guide separating stable Voice from situational Tone and warning against fluffy metaphors and forced humor [VERIFIED]
- `DOCWRITEFW-IN01-SC-ACRLX-WORKBK`: https://www.acrolinx.com/wp-content/uploads/2021/04/Acrolinx_ToneofVoice_WorkBook.pdf - Acrolinx Tone of Voice Workbook modeling tone as a "graphic equalizer" of sliding controls mapped to concrete linguistic elements [VERIFIED]
- `DOCWRITEFW-IN01-SC-MEDU-VOICEREP`: https://asmepublications.onlinelibrary.wiley.com/doi/10.1111/medu.15298 - Lingard et al. (2024), *The writer's voice repertoire: Exploring how health researchers accomplish a distinctive 'voice' in their writing*, showing how authors pair a logical "red thread" with selected unconventional voice moves [VERIFIED]
- `DOCWRITEFW-IN01-SC-BREV-ASIDE`: https://brevitymag.com/craft-essays/on-the-aside-looking-in/ - *On the Aside Looking In* (Brevity: A Journal of Concise Literary Nonfiction), analyzing parenthetical asides as insider connection and warning against over-indulgence [VERIFIED]
- `DOCWRITEFW-IN01-SC-TANDF-DIDION17`: https://www.tandfonline.com/doi/abs/10.1080/01440357.2017.1326451 - *Joan Didion's memoirs: substance & style* (Prose Studies, 2017), analyzing delayed resolution via parenthetical asides, periodic accumulation, and elliptical snap sentences [VERIFIED]
- `DOCWRITEFW-IN01-SC-UIST-MALLEABLE`: https://chaozhang.design/assets/publications/mp_uist2026/mp_uist2026.pdf - *From Words to Widgets for Controllable LLM Generation* (Malleable Prompting, UIST 2026), separating task specifications from parameterized preference sliders [VERIFIED]
- `DOCWRITEFW-IN01-SC-ACL-STYLE2026`: https://doi.org/10.18653/v1/2026.findings-acl.2039 - *Interpreting Style Representations via Style-Eliciting Prompts* (ACL Findings 2026), showing that LLMs follow stylistic instructions reliably when high-level style dimensions are translated into explicit lexical, syntactic, and rhetorical constraints [VERIFIED]
- `DOCWRITEFW-IN01-SC-ARXV-CASSE26`: https://arxiv.org/html/2601.10809 - *A Concise Agent is Less Expert: Revealing Side Effects of Using Style Features on Conversational Agents* (2026), proving that style features are entangled in LLMs (e.g., conciseness reduces perceived expertise) and require multi-objective precedence constraints [VERIFIED]
- `DOCWRITEFW-IN01-SC-ARXV-SCALES26`: https://arxiv.org/html/2610.22187 - *Change the Number, Change the Answer: Assessing Rating Scale Sensitivity in LLM-Based Text Scoring* (2026), showing ~10% normalized score shifts and 20% category shifts across numeric scales unless anchored to explicit bands [VERIFIED]
- `DOCWRITEFW-IN01-SC-EMNLP-TST25`: https://doi.org/10.18653/v1/2025.findings-emnlp.1166 - *A Decoupled Multi-Agent Framework for Complex Text Style Transfer* (EMNLP Findings 2025), showing that single-step style transfer causes semantic drift on complex styles and requires a separate content-preservation check [VERIFIED]
- `DOCWRITEFW-IN01-SC-GH-TEQUAL`: https://github.com/Ileies/tequalizer/blob/master/README.md - Tequalizer browser extension using five numeric sliders (length, imagery, warmth, formality, simplicity) to rewrite web articles into a target style [VERIFIED]
- `DOCWRITEFW-IN01-SC-GH-CLAUDEBLG`: https://github.com/AgriciDaniel/claude-blog/blob/main/skills/blog-persona/SKILL.md - Claude blog-persona skill combining NN/g tone sliders with vocabulary tier, sentence length variation, and explicit Do/Don't rules [VERIFIED]
- `DOCWRITEFW-IN01-SC-PLOS-STYLJP`: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0335369 - *Stylometry can reveal AI authorship, but humans struggle* (PLOS One 2025), confirming 99.8% stylometric detection across 7 LLMs including reasoning models [VERIFIED]
- `DOCWRITEFW-IN01-SC-ARXV-STYLOREC`: https://arxiv.org/abs/2507.00838 - *Stylometry recognizes human and LLM-generated texts in short samples* (Expert Systems with Applications 2025), demonstrating greater grammatical standardization in LLM outputs [VERIFIED]
- `DOCWRITEFW-IN01-SC-JOEL-TEST00`: https://www.joelonsoftware.com/2000/08/09/the-joel-test-12-steps-to-better-code/ - Joel Spolsky (2000), *The Joel Test: 12 Steps to Better Code*, demonstrating conversational openings, comic hyperbole ("With all the time you save, you can go to medical school"), and pragmatic 12-question heuristics [VERIFIED]
- `DOCWRITEFW-IN01-SC-JOEL-NEVER00`: https://www.joelonsoftware.com/2000/04/06/things-you-should-never-do-part-i/ - Joel Spolsky (2000), *Things You Should Never Do, Part I*, case-led argument against ground-up Netscape rewrites [VERIFIED]
- `DOCWRITEFW-IN01-SC-JOEL-ASTR01`: https://www.joelonsoftware.com/2001/04/21/dont-let-architecture-astronauts-scare-you/ - Joel Spolsky (2001), *Don't Let Architecture Astronauts Scare You*, coining "Architecture Astronauts" (`TR-14`) and grounding the critique in Napster vs. Groove [VERIFIED]
- `DOCWRITEFW-IN01-SC-JOEL-BASIC01`: https://www.joelonsoftware.com/2001/12/11/back-to-basics/ - Joel Spolsky (2001), *Back to Basics*, teaching `strcat` O(n²) complexity via the "Shlemiel the Painter's Algorithm" joke (`TR-01`, `TR-14`) [VERIFIED]
- `DOCWRITEFW-IN01-SC-JOEL-FIRE02`: https://www.joelonsoftware.com/2002/01/06/fire-and-motion/ - Joel Spolsky (2002), *Fire And Motion*, connecting an infantry paratrooper story to daily software shipping momentum [VERIFIED]
- `DOCWRITEFW-IN01-SC-JOEL-LEAKY02`: https://www.joelonsoftware.com/2002/11/11/the-law-of-leaky-abstractions/ - Joel Spolsky (2002), *The Law of Leaky Abstractions*, coining "Leaky Abstractions" (`TR-14`) through TCP, SQL, and NFS examples [VERIFIED]
- `DOCWRITEFW-IN01-SC-CHORR-SHOW05`: https://blog.codinghorror.com/show-dont-tell/ - Jeff Atwood quoting Joel Spolsky's introduction to *The Best Software Writing I* (2005) on the "Show, don't tell" rule and the Israeli army Sergeant Major story [VERIFIED]
- `DOCWRITEFW-IN01-SC-MSHFT-JOEL10`: https://mediashift.org/2010/03/joel-spolsky-retires-his-blog-but-blogging-will-endure081/ - Mediashift (2010) analysis of Joel Spolsky's "geek vaudevillian" comic voice, story-led crash courses, and influence on technical blogging [VERIFIED]

## Document History

**[2026-10-28 23:32]**
- Added: Researched and added `5.17 JOEL-SPOLSKY` under `Author-Derived Profiles` in Section 5 (`F:2 W:6 H:5 N:7 D:4 T:3 | TR-01, TR-03, TR-14`), backed by 8 primary and secondary sources (`DOCWRITEFW-IN01-SC-JOEL-*`, `CHORR-SHOW05`, `MSHFT-JOEL10`); Section 5 count updated to 17

**[2026-10-28 23:25]**
- Added: Section 2.6 `Cluster E: Corpus-Derived Signatures` with `TR-13` (*Mimetic Chain*) and `TR-14` (*Coined Handle*), extracted from the `5.16` source essay; catalog is now 14 traits
- Added: Specimen Quote rule to Section 1.1 Gate 4 (quote literal identifiers verbatim, never invent one)
- Changed: Exclusions renumbered to Section 2.7; all `TR-01..12` ranges, the `0/12` count, Goal, Summary, diagram, TOC, and template `[OFF]` list updated to 14
- Changed: `5.16 KARSTEN-HELD` traits from `TR-07, TR-09, TR-10` to `TR-09, TR-10, TR-14` (by instance count in the corpus); voice sample now demonstrates `TR-14`; `TR-13` documented as a single-instance optional swap

**[2026-10-28 23:15]**
- Added: `5.16 KARSTEN-HELD` as first entry of a new `Author-Derived Profiles` cluster in Section 5, calibrated from the essay body of `KarstenHeld-MinimalExplicitConsistentTerminology_2017-09.md` with quoted evidence per slider and trait; Section 5 count updated to 16

**[2026-10-28 23:05]**
- Fixed: Restored missing Section 6 heading and `6.1` template intro; repaired garbled `Density` line that had swallowed a Document History entry
- Fixed: TOC now lists Sections 1-8 (Section 5 was missing; 6-8 were misnumbered); Section 5 heading widened to `(15 Personas)` with a Section 4 → Section 5 preset mapping
- Fixed: Word-addition ceiling unified to `<= 10` (was `12` in 2.1 and 3.5, `10` elsewhere); snapshot restore time unified to "under ten minutes" across the shared fact set (was 3 vs 10 minutes)
- Fixed: Summary trait-pruning count (5 merged + 3 dropped, not "six + two") and stale `Section 2.5` reference → `2.6`
- Fixed: 4.2 `CULTURED-COLUMNIST` used *falsus in uno* with an invented meaning (replaced by *praemonitus, praemunitus*) and fired `TR-04` + `TR-01` in one paragraph (violates 2.1 rule 3); traits now in separate paragraphs
- Changed: All Section 3, 4, and 5 voice samples rewritten to obey Gate 4 burstiness (no 30+ word sentences; 5-10 word statements alternate with 15-25 word explanations)
- Changed: `TR-12` reduced from 5 personas to 2 (`5.5`, `5.11`); `5.4 PRINCIPAL-ARCHITECT` recalibrated to `T:5 D:5` with `TR-03, TR-08, TR-10`; `5.7`, `5.8`, `5.14` Technicality/Density lowered for readability; Section 5 table trait order sorted ascending
- Changed: 1.6 `Density 5-6` now names the micro-dosed `TR-03` aside as the only parenthetical exception (removes contradiction with 5.4, 5.9, 5.14)

**[2026-10-28 22:45]**
- Added: Six personas for ebooks, coaching, anti-hype marketing, and blogging to Section 5 (`5.10 BOOK-AUTHOR`, `5.11 COACH-MENTOR`, `5.12 PRODUCT-POSITIONER`, `5.13 CASE-STORYTELLER`, `5.14 PRACTITIONER-BLOGGER`, `5.15 FOUNDER-ESSAYIST`) with explicit non-overlap boundaries

**[2026-10-28 22:38]**
- Added: Section 5 (`Market-Derived Persona Catalog for Business & Research Reports`) with `5.1 CXO-ADVISOR`, `5.2 STRATEGIC-THINKER`, `5.3 SECTOR-COLUMNIST`, `5.4 PRINCIPAL-ARCHITECT`, and `5.5 TECHNICAL-WRITER` (structured for expansion as additional personas follow)

**[2026-10-28 22:30]**
- Added: Four academic and research personas to Section 5 (`5.6 INTELLECTUAL`, `5.7 JURIST`, `5.8 ANALYST`, `5.9 HISTORIAN`) with explicit non-overlap boundaries against `5.1..5.5`

**[2026-10-28 20:50]**
- Changed: Reworked all 12 traits (`TR-01..12`) in Section 2 with compact, subtle examples (`*cui bono* (who benefits?)` in 2-4 words rather than multi-sentence explanations) and explicit **LLM Prompt Instructions**
- Fixed: Replaced all 0-based section and diagram numbering (`0.`, `1.0`, `2.0`) with strict 1-based numbering (`1.1..1.8`, `2.1..2.6`) per `/verify`

**[2026-10-28 20:42]**
- Added: Section 1.1 (`Universal Zero-Bullshit Baseline`: Bernoff's Iron Imperative + Zinsser's Bracket Test) and Section 2.1 (`The Micro-Dose & Subtlety Law`: 95/5 sentence budget, max 1 trait per 300-400 words, never 2 traits in one paragraph), backed by `CoMPosT` (2023), `PANDA` (2024), `Generative Exaggeration` (2025), and `SCONPOS` (2026)
- Changed: Pruned the 20 brainstormed traits down to **12 orthogonal, information-carrying traits (`TR-01..12`)** and documented the 8 merged/dropped traits in Section 2.6 (`Exclusions`)
- Added: Section 3.5 (`Trait Dosing: Subtle Inline Character vs. Generative Exaggeration Caricature`) and updated the 5 Persona Presets so each short sample fires only 1 subtle trait

**[2026-10-28 20:35]**
- Added: Initial 20 ON/OFF Authorial Voice Traits, updated 5 Persona Presets, and renamed document to `_INFO_HOW_TO_CONTROL_WRITING_STYLE_WITH_PARAMETERS_AND_TRAITS.md`

**[2026-10-28 20:25]**
- Added: Section 1.8 (`Parameter Interactions and Precedence Rules`) and Section 5.3 (`Two-Pass Re-Writing Protocol`) from `/critique` and `/reconcile` review
- Changed: Generalized all examples to 100% generic English and moved to `E:\dev\IPPS\docs\` with Doc ID `DOCWRITEFW-IN01`


