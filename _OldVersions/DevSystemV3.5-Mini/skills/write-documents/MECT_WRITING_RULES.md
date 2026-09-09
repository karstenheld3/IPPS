# MECT Writing Rules

Complement to `APAPALAN_RULES.md`. MECT covers voice, word choice, heading design, list construction, description types. APAPALAN covers precision formatting, brevity, structure, naming. No overlap. Both apply simultaneously.

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

Description Types (DT)
- MW-DT-01: Four description lenses (intentional, functional, technical, contextual)
- MW-DT-02: Match description type to audience need
- MW-DT-03: Canonical form for matchable/sortable data

## Voice Rules (VO)

### MW-VO-01: Active Voice

Actor before action. Passive voice hides responsibility.

GOOD:
```
The administrator updated the configuration.
We will withhold your bond.
```

### MW-VO-02: Address Reader as "You"

GOOD:
```
You must provide your address.
Ensure your configuration is correct.
```

### MW-VO-03: Simplest Verb

Replace verbose verb phrases: "carry out a review" → "review", "make a determination" → "determine", "perform an analysis of" → "analyze".

### MW-VO-04: Obligation Words

Never use "shall" - ambiguous between obligation and future tense.

- must - obligation (no choice)
- must not - prohibition
- should - recommendation (choice exists)
- may - permission/discretion
- can - capability/ability

## Word Choice Rules (WC)

### MW-WC-01: Word-Level Precision

Commonly confused pairs:
- Accuracy (closeness to true value) != Precision (consistency of repeated measurements)
- Simple (uncomplicated) != Simplistic (oversimplified)
- Affect (verb: influence) != Effect (noun: result)

Word order creates opposite meanings: "Travel Time" != "Time Travel", "Account Issue" != "Issue Account"

When two terms seem interchangeable, look up the distinction. If it matters, use the precise term. If not, pick one consistently (AP-NM-01).

### MW-WC-02: Plain Language Over Academic

Test: "Would my reader use this word in conversation?" If not, replace it.

- BAD: "The determinants of the infant mortality rate"
- GOOD: "How many babies died and what were the main causes?"
- "Determinant" → "cause", "Timely manner" → specific date

### MW-WC-03: No Recursive/Implicit Naming

A name must not contain itself at a different level.

- BAD: Column "Name" contains sub-columns "Name" and "Surname"
- GOOD: Column "FullName" contains "GivenName" and "Surname"
- BAD: "Info Measurement Module" stores license plates
- GOOD: "VehicleRegistry" stores license plates

### MW-WC-04: No Product-as-Term Collision

Avoid naming concepts with words common in their domain.

- BAD: "The 'Service' component manages all services."
- GOOD: "The 'ServiceHub' component manages all services."

Test: Can you write a sentence using the name AND the domain term without confusion?

## Terminology Design Rules (TD)

### MW-TD-01: Naming Structure Method

Build by progressive qualification:
1. Most explicit name: "Project Start Date"
2. Add specifiers BEFORE: "Planned Project Start Date", "Actual Project Start Date"
3. Add states AFTER: "Planned Project Start Date Accepted"
4. Define mnemonics: `ACTUAL_PROJECT_START_DATE` (`APSD`), internal `start_date` (`sd`)
5. Document naming rules per domain

Apply when domain grows beyond 5-10 named concepts.

### MW-TD-02: Procedure/Process Names Describe Output

- BAD: "Analyze Traffic", "Check Order State"
- GOOD: "Generate Traffic Metrics", "Notify Pending Order Customers"

Exceptions: name by input when output varies ("Process Uploaded File"), name by mechanism when it distinguishes ("Manual Review" vs "Automated Review"). Default: name by output.

## Heading and Section Rules (HS)

### MW-HS-01: Informative Headings

State what the section contains, not the generic topic.

- BAD: "Background", "Results"
- GOOD: "Why We Changed the Authentication Flow", "3 Libraries Failed Due to Permission Errors"

Test: Can a reader decide whether to read the section from the heading alone?

### MW-HS-02: Limit Heading Depth to Three Levels

Max `#`, `##`, `###`. If you need `####`, restructure or split. Deep nesting signals the section is too broad.

### MW-HS-03: Write for Declared Audience

State who reads the document. Don't mix audiences in one section.

- BAD: API Reference mixing developer endpoints with "Click Login button" user instructions
- GOOD: Separate "API Reference (for developers)" and "User Guide"

## List and Table Rules (LT)

### MW-LT-01: Two Identifiers Per Row

Every item needs position index (ordering) AND semantic key (referencing).

```
1. EU-WEST - eu-west-1 (Frankfurt)
2. US-EAST - us-east-1 (Virginia)
```

Index enables "the third region." Key enables "the EU-WEST region."

### MW-LT-02: Group by Topology

Group reflects real relationships, not alphabetical order.

```
Europe:
1. EU-WEST - eu-west-1 (Frankfurt)
2. EU-CENTRAL - eu-central-1 (Ireland)

Americas:
3. US-EAST - us-east-1 (Virginia)
4. US-WEST - us-west-2 (Oregon)
```

### MW-LT-03: Index Groups as They Gain Importance

When groups grow beyond simple clusters, give them IDs too.

```
RG-EU Europe
1. EU-WEST - eu-west-1 (Frankfurt)
2. EU-CENTRAL - eu-central-1 (Ireland)
```

Now "region group RG-EU" is a valid reference target.

## Description Type Rules (DT)

### MW-DT-01: Four Description Lenses

- Intentional - WHY (the problem it solves)
- Functional - WHAT (black-box: inputs/outputs)
- Technical - HOW (implementation details)
- Contextual - WHERE (dependencies, relationships, constraints)

Example - rate limiter:
- Intentional: "Prevents API abuse by limiting request frequency per client."
- Functional: "Counts per client IP in sliding window, returns 429 when exceeded."
- Technical: "Redis sorted set per IP. ZRANGEBYSCORE to count. 100 req/min default."
- Contextual: "Between API gateway and handlers. Depends on Redis. Configured in `rate_limits.yaml`."

### MW-DT-02: Match Description Type to Audience

- Stakeholders: intentional + functional
- Developers: functional + technical
- Operations: technical + contextual
- New team members: all four, in order: intentional → functional → technical → contextual

### MW-DT-03: Canonical Form for Matchable/Sortable Data

Use single predictable form for data that must be compared, sorted, or matched.

```
Canonical: CALL-DJESTOXX50@4400EX2008-02

All variants convertible:
- "Call on Dow Jones EStoxx 50, strike 4400, expires Feb 2008" -> CALL-DJESTOXX50@4400EX2008-02
```

When to apply:
- IDs across documents (Doc ID system: `CRWL-SP01`)
- Dates (use `YYYY-MM-DD` per AP-PR-01)
- Status values (define enum: `TODO`, `IN_PROGRESS`, `DONE` - not free text)
- Any data appearing in multiple places that must be matchable