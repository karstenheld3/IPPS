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

- **Inconsistent naming / Terminological synonymy** - Multiple official names for the same concept create a "distinction without a difference". Users assume different words = different things, constructing phantom entities in their mental model. The more authoritative the source, the stronger this false assumption. Violates the terminological ideal of univocity (one term = one concept)
  - "garage" / "service" / "workshop" for same concept
  - "car tickets" (UI) vs "service events" (internal) vs "service tickets" (nested)
  - Software with 4 different names across organization
  - Azure Entra ID identity system - 2 objects, 1 GUID, 1 product, 14+ official names:
    - **Application Object** (the definition of an app): found under "App registrations" (portal blade name), called "Application" (Graph API entity). Microsoft's own docs call it "a template or blueprint to create service principal objects" - but the portal blade is named after the action of registering, not the object itself
    - **Service Principal** (the per-tenant instance): called "Enterprise Application" (portal blade name), "Enterprise App" (shorthand). The blade name "Enterprise applications" sounds like a category of apps (enterprise-grade vs regular) - it's not, it's just where Service Principals are listed. Every registered app gets one, not just "enterprise" ones
    - **The GUID**: "Application ID", "App ID", "Client ID", "Application (client) ID" (portal hedges with parentheses)
    - **The product**: "Azure AD", "Azure Active Directory", "Microsoft Entra ID", "AAD"
    - The two portal blades ("App registrations" and "Enterprise applications") are so similar that people conflate them into "Enterprise App Registrations" - a blade that does not exist

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

- **Inverted semantics** - Name suggests opposite direction of the value
  - `target_compression_percent: 40` - name says "compression" (how much to remove) but value means "output size" (how much to keep). User reads 40% compression, actual meaning is 40% remaining = 60% compression
  - Fix: rename to `target_reduction_percent: 60` - "reduce by 60%" can only mean one thing

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
- **Fewer TERMS, not fewer CHARACTERS**: "Minimal" targets term proliferation (multiple names for one concept). It does NOT mean "use fewest characters." Compressing "Supported" to "S" does not reduce terminology - it introduces a new opaque symbol that must be decoded. Minimal is satisfied when one concept has one name; the name's length is irrelevant

**Explicit**
- No reliance on implicit knowledge ("Humans are born with zero implicit knowledge")
- Self-describing terms that teach structure
- Words that evoke correct association fields: "button" beats "actiontrigger" or "on-off-provider" because everyone knows what a button is
- Choose words from daily life, not obscure technical jargon
- Build on shared experiences and common knowledge
- **Premature compression trap**: Authors define a term then immediately abbreviate it, treating the definition as license to compress. But "Explicit" means decodable at EVERY point of use, not just at the point of definition. Short labels are acceptable when a legend is visible without scrolling (the legend makes them explicit). Without a legend, use the full word. The principle is decodability at point of use, not full words everywhere. Same economics as terminology debt (section 1.2): cheap to prevent, expensive to decode later

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

**Signal vs Noise.** Every design choice in terminology, formatting, naming, and structure is either signal or noise. A signal is a purposeful choice that carries information the reader needs - a consistent name, a deliberate format, a meaningful distinction. Noise is an arbitrary choice that carries no information, yet the reader interprets it as if it does - an inconsistent spelling, a random format change, a redundant label. Because readers treat all variation as intentional, noise actively misleads. The three MECT properties work together to maximize signal and minimize noise: Minimal removes redundant terms (noise), Explicit ensures every term teaches its meaning (signal), and Consistent guarantees that identical patterns always mean the same thing (turning potential noise into reliable signal). See `_INFO_APAPALAN_PRINCIPLE.md [APAPALAN-IN01]` section 2.2 for how APAPALAN enforces this through concrete rules.

**General design principles.** The following principles from Don Norman's "The Design of Everyday Things" and cognitive science apply to all design - products, interfaces, documents, terminology, and communication. MECT builds on these because good communication design follows the same laws as good product design.

- **Proximity** - Information that is needed together must be placed close together. A function name and its parameters belong in the same view. An error message and its recovery action belong in the same line. When related information is scattered, the reader must hold fragments in working memory and reassemble them - a process that fails under cognitive load.
- **Sequence** - If people expect things to happen in a particular order, communication must reflect that order. Chronological events appear chronologically. Triggered actions are documented in processing order. A build-then-test workflow is described build-first, test-second. Violating expected sequence forces the reader to mentally reorder, introducing confusion and errors.
- **Topology** - Things have their place and must not change it. Once a sequence or arrangement of items is established, it must remain stable. Recipients build reliable mental maps that allow them to locate and compare items across sources quickly. Moving items between positions destroys these maps and forces relearning.
- **Signifiers** - Visual or structural cues that communicate affordances to the reader. A raised button signifies "clickable." An underlined blue text signifies "link." A bold heading signifies "section boundary." A code block signifies "literal content." When signifiers are used inconsistently (bold sometimes means emphasis, sometimes means label), the reader cannot predict what interaction or interpretation is expected.
- **Mapping** - The arrangement of information in the reader's mental model must map to the arrangement in the document or interface. If a process flows left-to-right in the reader's mind, the diagram must flow left-to-right. If a configuration has three layers (network, application, database), the documentation must present them in the same spatial relationship. A 1:1 mapping between mental model and presentation eliminates the translation step that causes errors.
- **Cognitive Load Limit** - People can hold roughly 5 to 7 separate items in working memory at once (Miller's Law). Beyond that, mental exhaustion and cognitive strain set in. An email with more than 5 action points, a function with more than 7 parameters, a list with more than 8 items without grouping - all exceed the reader's capacity. When this limit is reached, group items into meaningful clusters, split documents into focused sections, or reduce the number of concurrent concepts the reader must track.

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
Glossaries, Dicts,  ensure exhaustiveness,              Table & Column Names,
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

**Mnemonics vs Abbreviations - step 4 requires DESIGNED compression:**

A mnemonic is designed compression that encodes the concept. The short form evokes the full form through phonetic similarity, structural mapping, or domain convention:
- `CMDTY` → Commodity (phonetic: "commodity" is audible in "CMDTY")
- `OMON` → Option Monitor (structural: first letters of each word)
- `APAPALAN` → As Precise As Possible, As Little As Necessary (structural)
- `grep` → Global Regular Expression Print (structural, became a verb)

An abbreviation is arbitrary compression that removes information. The short form does NOT evoke the full form. The reader must memorize or look up every occurrence:
- `[S]` → Supported? Stable? Strong? Skipped? (opaque)
- `P=1` → Precision? Probability? Priority? (opaque)
- `SC` → Source? Scanner? Security? (opaque)

**Test (Reconstruction Test)**: Can someone unfamiliar with this document reconstruct the full term from the short form alone? If yes: mnemonic. If no: abbreviation.

Step 4 produces mnemonics, not abbreviations. If the short form fails the reconstruction test, it is not a mnemonic - it is an abbreviation disguised as one. Go back to step 1 and design a better short form, or use the full term.

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
- **Unix commands** - `grep` = "global regular expression print". Name describes function: searches globally using regex and prints matches. Easy to remember because acronym encodes behavior.
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

### 5.6 Bad: Azure Entra ID - Phantom Entities from Concurrent Synonyms

Microsoft's Entra ID identity system has two objects for application identity:
- **Application Object** - the global definition of an app (one per app, lives in the home tenant)
- **Service Principal** - the per-tenant instance (one per tenant where the app is used)

Registering an app via the portal automatically creates both an Application Object and a Service Principal. They share the same Application ID (GUID) but have different Object IDs. Via the Graph API, the Service Principal must be created separately. Microsoft's own documentation describes the Application Object as "a template or blueprint to create one or more service principal objects."

**The actual architecture:**

```
┌────────────────────────────────────────────────────────────────────────────┐
│  Entra ID - Application Identity Architecture                              │
│                                                                            │
│  ┌─────────────────────────────┐  creates (auto   ┌──────────────────────┐ │
│  │  Application Object         │ ─ via portal, ─> │  Service Principal   │ │
│  │  (the definition)           │  manual via API) │  (the instance)      │ │
│  │                             │                  │                      │ │
│  │  Lives in: home tenant      │                  │  Lives in: each      │ │
│  │  Scope: global, one per app │                  │  tenant that uses    │ │
│  │                             │                  │  the app             │ │
│  │  Has: Object ID (unique)    │                  │  Has: Object ID      │ │
│  │       Application ID ───────│─── same GUID ────│────── Application ID │ │
│  └─────────────────────────────┘                  └──────────────────────┘ │
│                                                                            │
│  1 Application Object  ──>  N Service Principals (one per tenant)          │
└────────────────────────────────────────────────────────────────────────────┘
"Application ID" = "Client ID" = "App ID" - three names for the same GUID.

Example: "Contoso Reporting Tool" registered in Tenant A, used by Tenant A and Tenant B:

┌──────────────────────────────────────────────────────────────────────────┐
│  Tenant A (home tenant - contoso.com)                                    │
│                                                                          │
│  ┌────────────────────────────────┐  ┌─────────────────────────────────┐ │
│  │  Application Object            │  │  Service Principal              │ │
│  │  "Contoso Reporting Tool"      │  │  "Contoso Reporting Tool"       │ │
│  │                                │  │                                 │ │
│  │  Application ID: 1111...1111   │  │  Application ID: 1111...1111    │ │
│  │  Object ID:      2222...2222   │  │  Object ID:      3333...3333    │ │
│  └────────────────────────────────┘  └─────────────────────────────────┘ │
│  Found under: "App registrations"    Found under: "Enterprise            │
│                                      applications"                       │
├──────────────────────────────────────────────────────────────────────────┤
│  Tenant B (partner tenant - fabrikam.com)                                │
│                                                                          │
│  No Application Object here          ┌─────────────────────────────────┐ │
│  (definition lives in Tenant A)      │  Service Principal              │ │
│                                      │  "Contoso Reporting Tool"       │ │
│                                      │                                 │ │
│                                      │  Application ID: 1111...1111    │ │
│                                      │  Object ID:      4444...4444    │ │
│                                      └─────────────────────────────────┘ │
│  "App registrations": empty          Found under: "Enterprise            │
│  (nothing to see)                    applications"                       │
└──────────────────────────────────────────────────────────────────────────┘

Same Application ID (1111...1111) appears 3 times across 3 objects in 2 tenants.
Each object has a different Object ID. The portal shows no link between them.
"Application ID" = "Client ID" = "App ID" - three names for the same GUID (1111...1111).
```

**The naming problem - same two objects, different name per surface:**

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Surface          │  Application Object       │  Service Principal      │
├───────────────────┼───────────────────────────┼─────────────────────────┤
│  Portal blade     │  "App registrations"      │  "Enterprise            │
│                   │                           │   applications"         │
│  Portal counter   │  "Applications: 19"  (ambiguous - which ones?)      │
│  API (Graph)      │  Application entity       │  ServicePrincipal       │
│                   │                           │   entity                │
│  CLI (az ad)      │  az ad app                │  az ad sp               │
│  Docs (various)   │  "application object"     │  "Enterprise App"       │
│  Informal         │  "Application"            │  "SP"                   │
│  MS docs concept  │  "template / blueprint"   │  "instance"             │
├───────────────────┼───────────────────────────┼─────────────────────────┤
│  The GUID         │  "Application ID" / "App ID" / "Client ID" /        │
│  (shared)         │  "Application (client) ID"                          │
├───────────────────┼─────────────────────────────────────────────────────┤
│  The product      │  "Azure AD" / "Azure Active Directory" /            │
│  (renamed 3x)     │  "Microsoft Entra ID" / "AAD"                       │
└───────────────────┴─────────────────────────────────────────────────────┘
```

**What the portal shows:** The Azure portal's Entra ID section has a left sidebar with a "Manage" group. In that group, two menu items sit near each other at the same hierarchy level:

```
v Manage
    Users
    Groups
    External Identities
    Roles and administrators
    Administrative units
    Delegated admin partners
  > Enterprise applications    <--
    Devices
  > App registrations          <--
    Identity Governance
    ...
```

"Enterprise applications" opens a list of Service Principals. "App registrations" opens a list of Application Objects. Nothing in the portal indicates that these two blades show two sides of the same coin. They appear as independent categories of different things.

**Why the blade names mislead:**
- "Enterprise applications" sounds like a category of apps - enterprise-grade vs regular. It's not. Every registered app gets a Service Principal here, including a simple PowerShell script. The word "Enterprise" is decoration.
- "App registrations" is named after an action (the act of registering) but shows objects (Application Objects). The blade should logically be called "Applications" or "Application definitions."
- The two names are similar enough that people mentally merge them into "Enterprise App Registrations" - a blade that does not exist.
- The overview page shows a counter "Applications: 19" which could refer to either blade or both. A third ambiguous term.
- No cross-reference exists. Nothing in "App registrations" says "the corresponding Service Principal is under Enterprise applications." Nothing in "Enterprise applications" says "the definition is under App registrations."

**Beyond the portal:** The API, CLI, docs, and shorthand each add more synonyms. The Application Object is called "Application" in the Graph API and "application object" in documentation. The Service Principal is also called "Enterprise App" in shorthand. The single identifier GUID is called "Application ID", "App ID", "Client ID", and "Application (client) ID" (the portal hedges with parentheses). The product itself was renamed from "Azure AD" to "Azure Active Directory" to "Microsoft Entra ID."

A developer encountering this system for the first time sees 14+ distinct terms across portal, API, CLI, and docs. No single page lists the synonyms. The reasonable assumption - different official names from an authoritative source mean different things - leads to a mental model with phantom entities that don't exist.

**The problem:** Each surface (portal, API, CLI, docs) introduced its own names independently. The portal blade names were chosen for approachability ("Enterprise Application" instead of "Service Principal"), but approachability that creates false distinctions is worse than technical accuracy. A Microsoft Q&A answer confirmed: "Enterprise application is the friendly name for service principal." The word "friendly" reveals the intent, but friendly names that mislead are not friendly.

**The cost:** Days of wasted onboarding time per developer. Damaged trust in the documentation and architecture. Once a developer discovers that the naming was inconsistent, they start second-guessing correct information too. Trust damage compounds beyond the initial time loss.

**Mitigation:** When encountering 3+ unfamiliar terms in a new system, search "X vs Y" before assuming distinct concepts. Build a synonym map early. In Azure specifically, look at the underlying API object types (Microsoft Graph `Application` entity and `ServicePrincipal` entity) rather than portal blade names. Treat naming inconsistency as a documentation defect, not a personal knowledge gap.

### 5.7 Bad: Azure AI Foundry - Phantom Entities from Serial Renaming

Microsoft renamed its AI development platform twice in two years, producing three successive names. The prebuilt AI services collection was also renamed twice, producing three names. The underlying Azure resource for the services collection (`Microsoft.CognitiveServices/accounts`, `kind: "AIServices"`) remained unchanged throughout - only the marketing name on top of it changed.

**Chain of events:**
- **Pre-Jul 2023:** Prebuilt AI capabilities sold as "Azure Cognitive Services"
- **Jul 2023:** Renamed to "Azure AI Services". Same product, same resource type
- **Nov 2023:** New AI development portal launched as "Azure AI Studio" (Public Preview). Deploys `Microsoft.MachineLearningServices/workspaces` with Hub + Project structure
- **Nov 2024:** "Azure AI Studio" renamed to "Azure AI Foundry". Same portal, same URL, same resources
- **May 2025:** New resource type introduced under the same "Azure AI Foundry" name, now deploying `Microsoft.CognitiveServices/accounts` instead. Old Hub-based resources still work. Two different resource types coexist under one product name. "Azure AI Services" absorbed into "Azure AI Foundry"
- **Nov 2025:** "Azure AI Foundry" renamed to "Microsoft Foundry". "Azure AI Services" renamed to "Foundry Tools" / "Foundry Prebuilt Tools". Portal splits into "Foundry" and "Foundry (classic)" with version switcher

**Result:** The platform had 3 names in 2 years. The prebuilt services had 3 names in 2 years. Each rename left behind tutorials, blog posts, and Stack Overflow answers using the old name. Search engines index all of them without distinguishing current from obsolete. A developer searching today finds content using "Azure AI Studio" (2024), "Azure AI Foundry" (early 2025), and "Microsoft Foundry" (late 2025) - with no indication that these are the same product.

**The problem:** Unlike the Entra ID case (concurrent synonyms), this is serial renaming: the same product gets a new marketing name at each annual conference (Ignite, Build), while previous documentation persists indefinitely. The effect is identical - phantom complexity - but the mechanism is different. The developer cannot distinguish "old name for current product" from "name of a different product" from "name of a discontinued product."

**The cost:** Every rename invalidates existing knowledge. Tutorials become misleading. Internal wikis go stale. Developers waste time confirming that the thing they're reading about still exists under a different name.

**Mitigation:** Look for the underlying resource type (ARM resource provider + `kind` value) rather than the marketing name. Check the publication date of any tutorial - in the Azure AI space, anything older than 12 months likely uses a defunct name.

### 5.8 Bad: Request Examples

**Ambiguous request:**
> "I noticed that for 'Samsung Battery Charger' the availability date '10/11/2017' had a typo."

Problems: Missing identifier, non-ISO date, no explicit state change, no call to action

**Clear request:**
> "Please change the availability date for article number 87568752 'Samsung Battery Charger' from 2017-10-11 to 2017-11-10."

### 5.9 Hall of Fail - Semantic Precision

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

### 5.10 Academic Language vs Plain Language

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

**[2026-04-12 14:50]**
- Added: "Fewer TERMS, not fewer CHARACTERS" to Minimal property (2.2)
- Added: "Premature compression trap" to Explicit property (2.2)
- Added: "Mnemonics vs Abbreviations" distinction to Naming Structure Method (3.2) with Reconstruction Test

**[2026-03-19 22:13]**
- Added: Unix `grep` example - acronym that encodes behavior (5.4)

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
