# MECT Writing Rules

Writing principles derived from MECT (Minimal Explicit Consistent Terminology). Complement to `APAPALAN_RULES.md`.

**Abstraction levels:**
- **MECT** (this file) = General principles that guide judgment. Answers: "What makes good writing?" Examples illustrate the principle, not enforce a specific format.
- **APAPALAN** = Concrete enforceable rules with measurable criteria. Answers: "How do I check compliance?" BAD/GOOD examples define the exact pattern to follow.

**Topic split:**
- **MECT_WRITING_RULES** covers: voice, word choice, terminology design, heading design, list construction, description types
- **APAPALAN_RULES** covers: precision formatting, brevity patterns, document structure, naming conventions

No overlap. Both apply simultaneously. When writing documents, read both.

**Core concept - Signal vs Noise:**
Every design choice in a document is either **Signal** (purposeful, carries information the reader needs) or **Noise** (arbitrary, carries no information but the reader interprets as if it does). MECT strengthens signals and eliminates noise. APAPALAN enforces specific patterns to achieve this.

## Rule Index

Voice (VO)
- MW-VO-01: Active voice - actor before action
- MW-VO-02: Address reader as "you"
- MW-VO-03: Simplest verb - no hidden verbs
- MW-VO-04: Obligation words - must/must not/may/should (never "shall")

Word Choice (WC)
- MW-WC-01: Word-level precision - distinguish similar terms
- MW-WC-02: Plain language over academic - daily words, question format
- MW-WC-03: No recursive/implicit naming - no self-referential definitions
- MW-WC-04: No product-as-term collision - avoid domain-common words as names

Terminology Design (TD)
- MW-TD-01: Naming structure method (explicit -> specifiers -> states -> mnemonics)
- MW-TD-02: Procedure/process names describe output, not mechanism

Headings and Sections (HS)
- MW-HS-01: Informative headings - state content, not topic
- MW-HS-02: Limit heading depth to three levels
- MW-HS-03: Write for declared audience

Lists and Tables (LT)
- MW-LT-01: Two identifiers per row (index AND key)
- MW-LT-02: Group by topology - related items cluster
- MW-LT-03: Index groups as they gain importance
- MW-LT-04: Every formatting signal must carry information

Description Types (DT)
- MW-DT-01: Four description lenses (intentional, functional, technical, contextual)
- MW-DT-02: Match description type to audience need
- MW-DT-03: Canonical form for matchable/sortable data

## Table of Contents

- [Voice Rules (VO)](#voice-rules-vo)
- [Word Choice Rules (WC)](#word-choice-rules-wc)
- [Terminology Design Rules (TD)](#terminology-design-rules-td)
- [Heading and Section Rules (HS)](#heading-and-section-rules-hs)
- [List and Table Rules (LT)](#list-and-table-rules-lt)
- [Description Type Rules (DT)](#description-type-rules-dt)

## Voice Rules (VO)

### MW-VO-01: Active Voice

Actor before action. Reader knows WHO does WHAT immediately.

**BAD:**
```
The configuration was updated by the administrator.
Bonds will be withheld.
The lake was polluted by the company.
```

**GOOD:**
```
The administrator updated the configuration.
We will withhold your bond.
The company polluted the lake.
```

Passive voice hides the actor. "Bonds will be withheld" - by whom? "We will withhold your bond" - clear responsibility.

### MW-VO-02: Address Reader as "You"

Direct address reduces ambiguity about who must act.

**BAD:**
```
The applicant must provide his or her address.
Users should ensure their configuration is correct.
One must verify the output before proceeding.
```

**GOOD:**
```
You must provide your address.
Ensure your configuration is correct.
Verify the output before proceeding.
```

### MW-VO-03: Simplest Verb

Replace verbose verb phrases with single verbs. Hidden verbs bury the action inside nouns.

**BAD:**
```
carry out a review          → review
undertake the calculation   → calculate
make a determination        → determine
provide a description of    → describe
conduct an investigation    → investigate
perform an analysis of      → analyze
```

**GOOD:**
```
Review the implementation before merging.
Calculate the retry delay using exponential backoff.
Determine which endpoints require authentication.
```

### MW-VO-04: Obligation Words

Use precise modal verbs. Never use "shall" - it creates ambiguity between obligation and future tense.

- must - obligation (no choice)
- must not - prohibition
- should - recommendation (choice exists)
- may - permission/discretion
- can - capability/ability

**BAD:**
```
The system shall validate input.
Users shall not share credentials.
The API shall return JSON.
```

**GOOD:**
```
The system must validate input.
Users must not share credentials.
The API must return JSON.
```

## Word Choice Rules (WC)

### MW-WC-01: Word-Level Precision

Words that sound similar but differ in meaning. Using the wrong one corrupts the mental model.

**Commonly confused pairs:**
- 'Accuracy' (closeness to true value) != 'Precision' (consistency of repeated measurements)
- 'Simple' (uncomplicated) != 'Simplistic' (oversimplified, missing important detail)
- 'Development' (increase in capacity/capability) != 'Growth' (increase in size/quantity)
- 'Affect' (verb: influence) != 'Effect' (noun: result)
- 'Receiver' (device/person receiving) != 'Recipient' (intended addressee)

**Word order creates opposite meanings:**
- 'Travel Time' (duration of journey) != 'Time Travel' (moving through time)
- 'Having judgement' (wisdom) != 'Being judgemental' (critical)
- 'Account Issue' (problem with account) != 'Issue Account' (create an account)

**Action:** When two terms seem interchangeable, look up the distinction. If the distinction matters in context, use the precise term. If it doesn't matter, pick one and use it consistently (AP-NM-01).

### MW-WC-02: Plain Language Over Academic

Use daily words. Convert academic/bureaucratic language to plain language.

**BAD:**
```
The determinants of the infant mortality rate in the United States.
Individuals and organizations wishing to apply must file applications
with the appropriate offices in a timely manner.
```

**GOOD:**
```
How many babies died in the United States of America between 1991
and 2004 and what were the main causes?
To apply for a grant, send your application to [Office Name] by [Date].
```

**Systematic test:** For each important word, ask: "Would my reader use this word in conversation?" If not, replace it.

- "Determinant" → "cause"
- "Infant" → "baby"
- "Mortality" → "death"
- "Timely manner" → specific date

### MW-WC-03: No Recursive/Implicit Naming

A name must not contain itself at a different level. Definitions must not be self-referential.

**BAD:**
```
Column "Name" contains sub-columns "Name" and "Surname"
→ A person's name cannot be composed of itself and a surname (recursive logic)

"Info Measurement Module" stores license plates
→ Nothing to do with measurements (implicit, misleading container)
```

**GOOD:**
```
Column "FullName" contains sub-columns "GivenName" and "Surname"
→ No recursion: FullName != GivenName

"VehicleRegistry" stores license plates
→ Clear what the container holds
```

### MW-WC-04: No Product-as-Term Collision

Avoid naming concepts, projects, or document sections with words that are common terms in their own domain.

**BAD:**
```
The "Service" component manages all services.
The "Module" system organizes modules into groups.
The "Task" feature tracks tasks across projects.
```
(Product name collides with domain vocabulary - "3 services in Service", "modules in Module")

**GOOD:**
```
The "ServiceHub" component manages all services.
The "Blueprint" system organizes modules into groups.
The "WorkTracker" feature tracks tasks across projects.
```

**Test:** Can you write a sentence using the name AND the domain term without confusion? If not, rename.

## Terminology Design Rules (TD)

### MW-TD-01: Naming Structure Method

Build terminology by progressive qualification. Start explicit, add specifiers, add states, then define short forms.

**Steps:**
1. **Start with most explicit name**: "Project Start Date", "Project End Date"
2. **Add specifiers BEFORE the name**: "Planned Project Start Date", "Actual Project Start Date"
3. **Add states AFTER the name**: "Planned Project Start Date Accepted"
4. **Define short/long mnemonics**: external `ACTUAL_PROJECT_START_DATE` (`APSD`), internal `start_date` (`sd`)
5. **Document naming and spelling rules** per domain

**BAD:**
```
- start date
- the date
- project date
- date1
```
(Four vague names for potentially different concepts)

**GOOD:**
```
- Project Start Date (PSD)
- Planned Project Start Date (PPSD)
- Actual Project Start Date (APSD)
- Project Start Date Status
```

**When to apply:** Whenever a domain grows beyond 5-10 named concepts. The naming structure becomes the "DNA for your field of action" - stable, predictable, extendable.

### MW-TD-02: Procedure/Process Names Describe Output

Name procedures, workflows, and process sections by what they produce - not by what mechanism they use.

**BAD:**
```
## Analyze Traffic
## Check Order State
## Run Data Through Pipeline
```
(Describes mechanism or action, not outcome)

**GOOD:**
```
## Generate Traffic Metrics
## Notify Pending Order Customers
## Produce Cleaned Dataset
```
(Describes what the reader gets after the procedure runs)

**When to use input or mechanism instead:**
- **Name by input** when output varies: "Process Uploaded File" (output depends on file type)
- **Name by mechanism** when the process itself is the distinguishing factor: "Manual Review" vs "Automated Review"

Default: name by output.

## Heading and Section Rules (HS)

### MW-HS-01: Informative Headings

Headings state what the section contains or answers, not the generic topic.

**BAD:**
```
## Applications
## Background
## Data
## Results
```

**GOOD:**
```
## How Do I Apply for a Grant?
## Why We Changed the Authentication Flow
## Server Response Times by Region (Q1 2026)
## 3 Libraries Failed Due to Permission Errors
```

**Test:** Can a reader decide whether to read the section from the heading alone? If the heading is "Background", the answer is no. If the heading is "Why JWT Replaced Session Cookies", the answer is yes.

### MW-HS-02: Limit Heading Depth to Three Levels

Three levels maximum: `#`, `##`, `###`. If you need `####`, restructure the document or split the section.

**BAD:**
```
## 1. Authentication
### 1.1 Token Management
#### 1.1.1 JWT Configuration
##### 1.1.1.1 Expiry Settings
```

**GOOD:**
```
## 1. Authentication
### 1.1 Token Management
### 1.2 JWT Configuration and Expiry
```

Deep nesting signals that the section is too broad. Split into separate documents or flatten the hierarchy.

### MW-HS-03: Write for Declared Audience

State who reads the document. Write for that audience. Don't mix audiences in one section.

**BAD:**
```
# API Reference
This endpoint handles user authentication using OAuth 2.0 flows.
Click the "Login" button to sign in to your account.
```
(Mixing developer audience with end-user audience)

**GOOD:**
```
# API Reference (for developers)
POST /api/auth/token - Exchange authorization code for access token.
```
```
# User Guide
Click "Login" to sign in to your account.
```

## List and Table Rules (LT)

### MW-LT-01: Two Identifiers Per Row

Every list item needs both a position index (for ordering) and a semantic key (for referencing).

**BAD:**
```
- eu-west-1
- us-east-1
- ap-southeast-1
```

**GOOD:**
```
1. **EU-WEST** - eu-west-1 (Frankfurt)
2. **US-EAST** - us-east-1 (Virginia)
3. **AP-SE** - ap-southeast-1 (Singapore)
```

Index (1, 2, 3) enables "the third region." Key (EU-WEST) enables "the EU-WEST region." Both enable unambiguous reference from other documents.

### MW-LT-02: Group by Topology

Related items cluster together. Group reflects real relationships, not alphabetical order.

**BAD** (alphabetical - hides relationships):
```
- ap-southeast-1
- eu-central-1
- eu-west-1
- us-east-1
- us-west-2
```

**GOOD** (grouped by geography):
```
Europe:
1. **EU-WEST** - eu-west-1 (Frankfurt)
2. **EU-CENTRAL** - eu-central-1 (Ireland)

Americas:
3. **US-EAST** - us-east-1 (Virginia)
4. **US-WEST** - us-west-2 (Oregon)

Asia-Pacific:
5. **AP-SE** - ap-southeast-1 (Singapore)
```

### MW-LT-03: Index Groups as They Gain Importance

When groups grow beyond simple clusters, give them IDs and keys too. Groups become referenceable units.

**Before** (simple list, no group IDs):
```
Europe: eu-west-1, eu-central-1
Americas: us-east-1, us-west-2
```

**After** (groups became important enough to reference):
```
**RG-EU** Europe
1. **EU-WEST** - eu-west-1 (Frankfurt)
2. **EU-CENTRAL** - eu-central-1 (Ireland)

**RG-AM** Americas
3. **US-EAST** - us-east-1 (Virginia)
4. **US-WEST** - us-west-2 (Oregon)
```

Now "region group RG-EU" is a valid reference target.

### MW-LT-04: Every Formatting Signal Must Carry Information

Applies the Signal vs Noise principle to formatting. Formatting (bold, italic, indentation, separators) is a communication channel. Each signal must add meaning the reader cannot get from structure alone. When structure already provides distinction (indent, dash, colon, heading), adding formatting on top is noise - it consumes visual weight without increasing information.

**Test:** Remove the formatting. Can the reader still distinguish the elements? If yes, the formatting is noise. See AP-BR-07 for concrete enforcement patterns.

## Description Type Rules (DT)

### MW-DT-01: Four Description Lenses

Any object can be described from four perspectives. Choose based on what the reader needs.

- **Intentional** - WHY it was introduced (the intent, the problem it solves)
- **Functional** - WHAT it does (black-box view, inputs/outputs)
- **Technical** - HOW it works (engine-room view, implementation)
- **Contextual** - WHERE it fits (dependencies, relationships, constraints)

**Example - describing a rate limiter:**

Intentional: "Prevents API abuse by limiting request frequency per client."

Functional: "Accepts requests, counts per client IP within sliding window, returns 429 when limit exceeded."

Technical: "Redis sorted set per IP. Score = timestamp. ZRANGEBYSCORE to count window. ZADD + EXPIRE on each request. 100 requests/minute default."

Contextual: "Sits between API gateway and application handlers. Depends on Redis. Bypassed for health check endpoints. Configured per route in `rate_limits.yaml`."

### MW-DT-02: Match Description Type to Audience

- Stakeholders need intentional (why) + functional (what)
- Developers need functional (what) + technical (how)
- Operations need technical (how) + contextual (where)
- New team members need all four, in order: intentional → functional → technical → contextual

**BAD** (technical description for stakeholders):
```
The rate limiter uses Redis sorted sets with ZRANGEBYSCORE
to count requests within a sliding window of 60 seconds.
```

**GOOD** (intentional + functional for stakeholders):
```
The rate limiter prevents API abuse by blocking clients that
send more than 100 requests per minute. Blocked clients receive
a "too many requests" error until their window resets.
```

### MW-DT-03: Canonical Form for Matchable/Sortable Data

When documenting data that readers (or tools) need to compare, sort, filter, or match - use a single predictable form. Convert vague property descriptions to structured, parseable formats.

**BAD:**
```
The option expires in February 2008 with a strike of 4400 on the Dow Jones EStoxx 50.
ESSTOXX 50 Call at 4400 (Feb 2008)
```
(Two descriptions of the same thing - unmatchable by human or machine)

**GOOD:**
```
Canonical form: CALL-DJESTOXX50@4400EX2008-02

All variants must be convertible to this form:
- "Call on Dow Jones EStoxx 50, strike 4400, expires Feb 2008" -> CALL-DJESTOXX50@4400EX2008-02
- "ESTOXX 50 Call at 4400 (Feb 2008)" -> CALL-DJESTOXX50@4400EX2008-02
```

**When to apply:**
- IDs referenced across documents (use Doc ID system: `CRWL-SP01`)
- Dates in tables or lists (use `YYYY-MM-DD` per AP-PR-01)
- Status values (define enum: `TODO`, `IN_PROGRESS`, `DONE` - not free text)
- Any data that appears in more than one place and must be matchable

**Principle:** "If you can express information in a canonical form, you unlock automated matching across systems - even when sources use completely different wording."
