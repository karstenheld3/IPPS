# INFO: MECT - Minimal Explicit Consistent Terminology

**Doc ID**: MECT-IN01
**Goal**: Extract communication design philosophy from Karsten Held's MECT article for application in agent-human systems
**Timeline**: Created 2026-03-19

## Summary

- **MECT** = "Use minimal explicit consistent terminology within a defined field of interaction" 
- Applied in communication as APAPALAN principle: "As precise as possible. As little as necessary." 
- One name per concept, self-describing terms, consistent usage everywhere 
- "Language is the operating system of the human mind" - terminology is infrastructure, not decoration 
- Words → concepts → association fields → mental models → predictions → actions (the causal chain) 
- Poor terminology causes: feedback loops, incompatible mental models, tower-of-babel effects 
- Good terminology enables: independent action, fast processing, computer-parseable data 
- Key economics: changing words on paper is orders of magnitude cheaper than changing processes 
- Applied examples: Bloomberg terminal, FUTOP-ID (Universal Future and Option Identifyer), German energy sector, musical notation 

## Table of Contents

1. [Common Problems and Impact](#1-common-problems-and-impact)
2. [Philosophy and Goals](#2-philosophy-and-goals)
3. [Tools and Methods](#3-tools-and-methods)
4. [Practical Rules](#4-practical-rules)
5. [Examples](#5-examples)
6. [Sources](#6-sources)
7. [Document History](#7-document-history)

## 1. Common Problems and Impact

### 1.1 Symptoms of Poor Terminology

- **Name collision (polysemy)** - Same word for related but different things. More dangerous than homonymy (accidental similarity) because people THINK they agree when they don't. "These subtle polysemes could be smoothed over in conversation but not in the precise world of computers." (Martin Fowler)
  - "Ball bearing" = individual ball AND entire assembly
  - "Cardinality" = data modeling relationship vs mathematical set size
  - "Meter" in utilities = connection point vs physical device vs customer relationship

- **Inconsistent naming** - Same thing with multiple names
  - "garage" / "service" / "workshop" for same concept
  - "car tickets" (UI) vs "service events" (internal) vs "service tickets" (nested)
  - Software with 4 different names across organization

- **Ambiguous meta-words** - Generic terms hiding specifics
  - "Welcome screen", "Data Center", "Customer Screen" - unpredictable content
  - "service", "module", "event", "ticket" - overloaded meanings

- **Recursive/implicit naming** - Self-referential definitions that introduce logical paradoxes
  - Column "Name" containing sub-columns "Name" and "Surname" - a person's name cannot be composed of itself and a surname (recursive logic)
  - License plate stored in "Info Measurement Module" (nothing to do with measurements)

- **Verbose procedure naming** - Multiple synonyms for same operation
  - "Refresh", "clean up", "migration", "copy valid data" all referring to same procedure
  - Good: "DataCleanup" or "DropInvalidData" - one name, used everywhere including logfile names

- **Compound name ambiguity** - Word order creates multiple readings
  - "EmptyCollectionKey" - Is the collection empty, or is the key empty?
  - Better: "KeyOfEmptyCollection" - unambiguous word order

- **Product-as-term collision** - Product names that collide with their own domain
  - Microsoft Teams: "3 Teams in Teams", "my teams in Teams" - the product name IS a common domain word

- **Dangerous meta-words** - Words that seem specific but hide ambiguity
  - "Module": What contains what? `Product` vs `ProductModule`, `LessonModule` vs `Lesson`
  - "Service": Named after consumer, provider, or product?
  - "Generation": Generating something (code) or generation of something (3GS mobile)?
  - "Check": Result can be yes/no ("check if exists") or always yes ("perform check")
  - Other dangerous words: Payload, Workload, Cargo, Network, Monitor, View, Console, Facade, Provider, Asset

- **Misleading word pairs** - Parameters that don't form intuitive opposites
  - PowerShell `Compare-Object` uses `-ReferenceObject` and `-DifferenceObject` instead of intuitive `Current/Target` or `Before/After`
  - Users must memorize arbitrary names instead of predicting from pattern

- **Incorrect word pairs** - Functions that break expected naming conventions
  - Power Platform has `EncodeUrl()` and `PlainText()` - overgeneralized. Users search for `DecodeUrl()` and `UnescapeHTML()` and fail to find them
  - Should be: `EncodeUrl/DecodeUrl`, `EscapeHtml/UnescapeHtml`

- **Confusing function names across platforms** - Same operation, different names
  - Power Platform's `Concat()` joins table rows - everywhere else this is called `join()`
  - JavaScript: `join()` joins array elements, `concat()` concatenates strings
  - Users transfer wrong mental model from one platform to another

### 1.2 Organizational Impact

- **Incompatible mental models coexist undetected** - Different teams build different understandings that eventually collide
- **Tower of Babel effect** - Teams speak different languages about same domain
- **Data modeling problems** - New products model data differently, can't integrate
- **Productivity decrease** - Arguments, meetings, feedback loops dominate daily work
- **Over-engineering** - Confusing terminology leads to unnecessary abstractions
- **Compounding cost** - Changing words on paper is orders of magnitude cheaper than changing processes or systems. The cost of NOT investing in terminology compounds over time
- **Bad terminology repels adoption** - Teams refuse to adopt confusing terminology from other teams, creating more fragmentation instead of less

### 1.3 Why Good Terminology is Hard

1. **Forces written commitments** - Exposes assumptions, gaps, ambiguities. Negotiating conventions bears the risk of not succeeding or agreeing on bad compromises. That's why people avoid it at project start. But stable naming conventions become "the DNA for your field of action."
2. **Changes poorly managed** - Habits harder to change than thoughts; managers change terminology to death. "A slow and minimalistic approach is healthier than dictating and recalling changes in a hurry."
3. **Impact underestimated** - "Just words" mentality; mental models grow incompatible until collision

## 2. Philosophy and Goals

### 2.1 Core Principle

**MECT** = Minimal Explicit Consistent Terminology

Use minimal explicit consistent terminology within a defined field of interaction. The field can be: business, document, factory, product, process, team, meeting.

### 2.2 The Three Properties

**Minimal**
- One name for one thing
- Use widely accepted existing names
- Stable over time and across contexts
- Efficiency in understanding > technical correctness
- "If it's horsepower, then it's horsepower"

**Explicit**
- No reliance on implicit knowledge ("Humans are born with zero implicit knowledge")
- Self-describing terms that teach structure
- Words that evoke correct association fields: "button" beats "actiontrigger" or "on-off-provider" because everyone knows what a button is
- Choose words from daily life, not obscure technical jargon
- Build on shared experiences and common knowledge

**Consistent**
- Same terminology everywhere within field
- Always used the same way
- Repetition helps recognition and learning
- Makes things predictable
- Provide translations when interfacing with other terminologies

### 2.3 Deeper Insights

**"Language is the operating system of the human mind."** It determines what you can accept and how you are able to exist. Creating a common language is a continuous, time-consuming effort. Team leaders often fail to recognize how important it is.

**Language as wisdom compression protocol.** Good terminology absorbs experience into single words. Japanese craftsmanship demonstrates this: "Sashimono", "Hozo", "Hukiurushi-shiage" each compress entire philosophies and techniques into one term. These words can then be reused in new contexts to precisely describe how a desired philosophy should be applied. Like programming frameworks, entire bodies of knowledge become reusable because the language is designed to serve multiple purposes.

**Words → mental models → predictions → actions.** "Words represent concepts and their association fields define the mental models we build to predict the outcome of our actions." Once people incorporate mental models they are very unlikely to change them. Incompatible models coexist undetected until they collide.

**"Gardener of communication."** The role of someone applying MECT: shape language and let it grow into a stable and efficient communication platform. If everything feels like being in the right place and having the right name, people will adopt your terminology and your ideas will spread. Growth becomes easier and the field of interaction attracts productive people and sharp minds.

### 2.4 Goals and Outcomes

- **Predictable, safe, efficient communication**
- **Avoid misunderstandings**
- **Minimize dependencies, ambiguities, feedback loops**
- **Enable independent action** - Clear communication removes need for coordination
- **Compatible mental models** - Words lead to efficient shared understanding
- **Reduced process complexity** - Less time managing friction and noise
- **Computer-processable** - Predictable forms enable matching, sorting, counting
- **Reality-aligned** - Terminology reflects how things actually work, not abstract ideals
- **Interoperable** - Good terminology interfaces with other systems and teams
- **Extendable** - Stable naming conventions serve as "the DNA for your field of action"

### 2.5 What MECT is NOT

- NOT minimum communication - More words are fine if they reduce questions
- NOT about saying less - About keeping term fragmentation low and being "compatible with yourself"
- "Like LEGO for communication - every piece has distinctive purpose and fits with all others"
- Distilled: "As precise as possible. As little as necessary." (German: "So prazise wie moglich. So wenig wie notig.")

## 3. Tools and Methods

### 3.1 MECT Tool Categories

```
                    Manuals/Specifications              Systems/Implementations
                    ───────────────────────────────────────────────────────────
Names [Identify]    avoid collisions, remove noise,     Objects & Properties
Codes, Acronyms,    distinguish states, ensure          Identifiers, Names, Syntax
Symbols, IDs,       referenceability, enable            Representation Primitives
Mnemonics, Icons    composability
                    ───────────────────────────────────────────────────────────
Lists [Group]       remove redundancies & duplicates,   Master Data & Views
Glossaries, Dicts,    ensure exhaustiveness,              Table & Column Names,
Tables, References, ensure consistency,                 Column Types
Enumerations        synonyms & translations
                    ───────────────────────────────────────────────────────────
Models [Relate]     topology & proximity,               Data Representation
Hierarchies,        containment & traversability,       & UI Controls
Structures,         navigation efficiency               Data Models, Relations
Diagrams
                    ───────────────────────────────────────────────────────────
Procedures [Execute] communication,                     Actions & Business Logic
How-Tos, Plans,     transactions & reversibility,       Operational Data, View
Processes,          detect & validate states            Models, Update Mechanisms
Workflows
                    ───────────────────────────────────────────────────────────
        Audits, Assessments, Revisions    |    Tests, Code Reviews, Releases
```

### 3.2 Naming Structure Method

1. **Start with most explicit name** - "Project Start Date", "Project End Date"
2. **Add variations/specifiers BEFORE the name** - "Planned Project Start Date", "Actual Project Start Date"
3. **Add states/conditions AFTER the name** - "Project Start Date Status", "Planned Project Start Date Accepted"
4. **Define short/long mnemonics** - external: `ACTUAL_PROJECT_START_DATE`, `APSD`; internal: `START_DATE`, `SD`
5. **Document naming and spelling rules** per domain coding style

### 3.3 Description Types

Four types of descriptions for any object:
- **Intentional** - Why it was introduced (the intent)
- **Functional** - How intent is achieved (black-box view)
- **Technical** - How function is implemented (engine-room view)
- **Contextual** - Dependencies and relations

### 3.4 Procedure Naming

Name procedures by describing:
- **Output** (preferred default): "Generate Traffic Metrics" > "Analyze Traffic"; "Notify Pending Order Customers" > "Check Order State"
- **Input**: When output is variable
- **Mechanism**: When process is the distinguishing factor

### 3.5 Convergent Terminology Systems

Maximum productivity emerges when a terminology serves multiple functions simultaneously through ONE system:

1. **Navigation** - Find any view, object, page instantly by name
2. **Query** - Same syntax serves as search and filter language
3. **Education** - Using the terminology teaches domain structure
4. **Communication protocol** - Same terms reusable in documents, emails, phone calls

When these four functions converge in a single terminology, productivity multiplies because sender and receiver share the same compressed language. (See section 5.1 for the Bloomberg terminal as proof.)

### 3.6 Canonical Form Principle

"That's the essence of language: How you express things with minimum effort so that others understand you instantly and can process information very fast without errors and misunderstandings."

Converting vague property collections into predictable, unambiguous forms enables compare, sort, match, join, count by computers. No brainpower required. If you can express information in a canonical form, you unlock automated matching across systems - even when sources use completely different wording. (See section 5.2 for the FUTOP-ID as proof.)

## 4. Practical Rules

### 4.1 Writing Rules

- **Use "you" to address reader** - "You must provide your address" not "The applicant must provide his or her address"
- **Use active voice** - "The company polluted the lake" not "The lake was polluted by the company"
- **Use simplest verb** - "tell you how to meet" not "describe types of information that would satisfy"
- **Avoid "shall"** - Use "must" for obligation, "must not" for prohibition, "may" for discretionary, "should" for recommendation

### 4.2 Document Rules

- Provide heading numbers for referenceability
- Use informative headings: "How do I apply?" not "Applications"
- Write for your audience - don't guess or assume
- Put most important information first
- Limit heading levels to three or fewer

### 4.3 List Rules

- Provide two identifiers per row: index AND key
- Group related items together (topology)
- As groups get important, introduce indexes and keys for groups

### 4.4 Anti-Patterns to Avoid

- **Wordiness** - "When the process of freeing a vehicle that has been stuck results in ruts or holes, the operator will fill the rut or hole created by such activity before removing the vehicle from the immediate area." Better: "If you make a hole while freeing a stuck vehicle, you must fill the hole before you drive away."
- **Confusing plural constructions** - "Individuals and organizations wishing to apply must file applications with the appropriate offices in a timely manner." Better: split into separate instructions per audience with specific deadlines.
- **Generic topic headings** - "Applications" tells nothing. "How do I apply for a grant under this part?" tells everything.
- **Long dense paragraphs** - Write short sections, address one person
- **Passive voice hiding the actor** - "Bonds will be withheld" hides who withholds. "We will withhold your bond" is clear.
- **Hidden verbs** - "carry out a review" = "review"; "undertake the calculation" = "calculate"

### 4.5 Precision at Word Level

Words that sound similar but differ in meaning. Using the wrong one corrupts the mental model:

- Accuracy != Precision
- Simple != Simplistic
- Development (increase in capacity) != Growth (increase in size)
- Independence != Interdependence
- Affect != Effect
- Cunning != Clever
- Receiver != Recipient
- Travel Time != Time Travel (word order creates opposite meanings)
- Having judgement != Being judgemental
- Account (Issue) != Account (Bank)

## 5. Examples

### 5.1 Good: Bloomberg Terminal

**Why it works:**
- Single short command per view/object/page/function
- Commands reflect descriptive names: "OMON" = Option Monitor, "FXR" = Foreign Exchange Rates, "MCS" = Multi Currency Settlement
- Terminology reusable in documents, emails, phone calls
- Aligned with how professionals actually talk
- Learning commands = learning domain structure ("by listing all futures for a given index I learned what an underlying was")
- Convergent system serving all four functions simultaneously (see section 3.5): navigation, query, education, communication protocol
- Special keyboard with domain keys ("Corp", "Index", "Cmdty") makes the language physically tangible

**Impact:** "You can quickly exchange incredible amounts of information on the phone with a system like that."

**Deeper pattern:** The Bloomberg system made the abstract financial world navigable by giving every concept a unique, short, descriptive mnemonic. Daily use of these commands built the mental model automatically. The system did not just name things - it taught the structure and relation of objects. By listing all futures for a given index, you learned what an underlying was. The sequence of text commands made that clear.

### 5.2 Good: FUTOP-ID (Custom Extension)

**Problem:** No unified naming for futures and options across 12 banks

**Solution:** Predictable ID format using Bloomberg conventions. Two completely different textual representations converge to the same canonical form:
- Bank A sends: "Call on Dow Jones EStoxx 50 with a strike of 4400 that expires in february 2008"
- Bank B sends: "ESTOXX 50 Call at 4400 (Feb 2008)"
- Both become: `CALL-DJESTOXX50@4400EX2008-02`

**Impact:** Parse inventory data from 12 banks daily, match against internal systems automatically. The canonical form bridges different human phrasings into one machine-processable ID.

### 5.3 Good: German Energy Sector Unification (2018)

**Problem:** Multiple overlapping terms: Lieferstelle, Entnahmestellen, Einspeisestelle, Ausspeisestelle, Messstelle, Zählpunkt - used synonymously and contradictorily

**Solution:** Two unified terms:
- **Marktlokation (MaLo-ID)** - billing/accounting point (financial construct)
- **Messlokation** - physical measurement location

**Impact:** Simplified and standardized market communication across entire energy industry

### 5.4 Good: Universal Notations

- **Music** - Note system (F#-3, Ab-1): precise, universal, minimal
- **Electronics** - Resistor names, part naming schemes: standardized across industry
- **Japanese craftsmanship** - "Sashimono" (joining wood without nails), "Hozo" (hidden notch-and-groove technique), "Hukiurushi-shiage" (10+ coats of wiped lacquer). Each word compresses an entire technique into a reusable term that can be applied and taught in new contexts. This is language as a "wisdom compression and transport protocol."

### 5.5 Bad: Automotive Software

**Root cause:** Software conceptually developed in Germany, programmed in Hungary, **without any shared technical document that defined a common terminology**. Programmers could name things as they liked. MECT requires an artifact (a shared terminology document), not just good intentions.

**Problems:**
- Software had 4 different names
- "garage" = "service" = "workshop" (inconsistent)
- "car tickets" (UI) vs "service events" (internal)
- License plate stored in "Info Measurement Module"
- Ambiguous meta-words: "service", "module", "event", "ticket"

**Impact:** Tower of Babel - teams couldn't integrate, productivity dropped. New teams understandably refused to adopt the confusing terminology, creating even more fragmentation.

### 5.6 Bad: Request Examples

**Ambiguous request:**
> "I noticed that for 'Samsung Battery Charger' the availability date '10/11/2017' had a typo."

Problems: Missing identifier, non-ISO date, no explicit state change, no call to action

**Clear request:**
> "Please change the availability date for article number 87568752 'Samsung Battery Charger' from 2017-10-11 to 2017-11-10."

### 5.7 Hall of Fail - Semantic Precision

- Emails do not have "titles", they have **subjects**
- People do not "have emails", they **receive emails** and have **email addresses**
- Flights do not have "targets", they have **destinations**
- A license plate does not identify a car, it identifies a **license to drive** (car may change)

**Character-level precision:**
- Bad: "Can you please remove all asterisks and hyphens?"
- Good: "Can you please remove the following characters: asterisk ('*' U+002A), hyphen-minus ('-' U+002D), minus sign ('-' U+2212)?" (Unicode notation disambiguates visually identical characters)

**Named references create reusability:**
- Bad: "Comma-separated list of all emails for mailing that will be sent out on a monthly basis to those customers who have ordered more than $1m over the last 2 years."
- Good: "Email addresses for Monthly Very Important Customers Mailing (MVIC) in comma-separated format. VIC = customer who has generated more than USD 1 million turnover within the last 2 years."

### 5.8 Academic Language vs Plain Language

**Bad:** "The Determinants of the infant mortality rate in the United States."

Systematic decomposition - every word fails the explicitness test:
- "Determinant" → means "causes" (why not say causes?)
- "Infant" → means "babies" (why not say babies?)
- "Mortality" → means "death" (why not say death?)
- "Rate" → means "how much" (vague without context)
- "United States" → of America or Mexico?

**Good:** "How many babies died in the United States of America between 1991 and 2004 and what were the main causes?"

Every word is from daily life. No interpretation needed. The question format makes the purpose explicit.

## 6. Sources

**Primary Source:**
- `MECT-IN01-SC-KHELD-MECT2017`: Karsten Held, "Minimal Explicit Consistent Terminology", September 2017

**Referenced Resources:**
- `MECT-IN01-SC-PLANG-GOV`: plainlanguage.gov - Federal Plain Language Guidelines
- `MECT-IN01-SC-FOWLR-BCTX`: Martin Fowler on Bounded Context and polysemes

## 7. Document History

**[2026-03-19 19:55]**
- Added: APAPALAN distillation "As precise as possible. As little as necessary." (Summary, 2.5)
- Added: Causal chain "words -> mental models -> predictions -> actions" (Summary, 2.3)
- Added: Polysemy vs homonymy distinction with Fowler quote (1.1)
- Added: "button" vs "actiontrigger" concrete example to Explicit property (2.2)
- Added: Two-input FUTOP-ID convergence showing canonical form power (5.2)
- Added: Root cause "no shared terminology document" to automotive example (5.5)
- Added: "Essence of language" quote to canonical form principle (3.6)
- Added: "be compatible with yourself", APAPALAN distillation (2.5)
- Added: Bad terminology repels adoption feedback loop (1.2)
- Added: "DNA for your field of action", conservative change management quotes (1.3)
- Added: Second procedure naming example "Notify Pending Order Customers" (3.4)
- Added: Unicode character disambiguation and MVIC mailing examples (5.7)
- Added: "Travel Time != Time Travel", "Having judgement != Being judgemental" (4.5)
- Added: Recursive naming logic explanation (1.1)
- Added: Reality-aligned, Interoperable, Extendable properties (2.4)
- Added: Good MECT attracts talent (2.3)

**[2026-03-19 19:50]**
- Fixed: Concept overlap between sections 3.5 and 5.1 (generalized method, moved Bloomberg specifics to example)
- Fixed: Moved "Canonical form principle" from Goals (2.4) to new Methods section (3.6)
- Fixed: Removed duplicate "hidden verbs" from 4.1 (kept in 4.4)
- Added: "Humans are born with zero implicit knowledge" argument to Explicit property (2.2)
- Fixed: Typos "Glossars" and "reversability"

**[2026-03-19 19:45]**
- Added: "Language as operating system" and "wisdom compression protocol" insights (section 2.3)
- Added: "Gardener of communication" role description (section 2.3)
- Added: Canonical form principle, convergent terminology systems (sections 2.4, 3.5)
- Added: Verbose procedure naming, compound name ambiguity, product-as-term collision (section 1.1)
- Added: Compounding cost of terminology debt (section 1.2)
- Added: Academic vs plain language example with systematic word decomposition (section 5.8)
- Added: Word-level precision pairs (section 4.5)
- Added: Concrete before/after text in anti-patterns (section 4.4)
- Added: Deeper Bloomberg analysis with convergence pattern (section 5.1)
- Added: Japanese craftsmanship term definitions (section 5.4)
- Added: Verification labels to Summary items
- Fixed: Section numbering (2.3 Deeper Insights, 2.4 Goals, 2.5 What MECT is NOT)

**[2026-03-19 19:40]**
- Initial extraction from source article
- Structured into: Problems, Philosophy, Tools, Rules, Examples
