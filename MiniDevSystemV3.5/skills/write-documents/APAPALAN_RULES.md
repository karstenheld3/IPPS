# APAPALAN Writing Rules

**APAPALAN** = As Precise As Possible (Priority 1), As Little As Necessary (Priority 2)

## Rule Index

Precision (PR) - Priority 1
- AP-PR-01: Standardized datetime format
- AP-PR-02: Standardized attribute/property format
- AP-PR-03: Standardized contact information format
- AP-PR-04: Standardized link and reference format
- AP-PR-05: Referenceable IDs on all trackable items
- AP-PR-06: Write out acronyms on first use
- AP-PR-07: Be specific - no generic or abstract writing
- AP-PR-08: Every non-obvious rule or format needs examples
- AP-PR-09: Consistent patterns (repeat established structures)

Brevity (BR) - Priority 2
- AP-BR-01: Single line for single statements
- AP-BR-02: Sacrifice grammar for brevity
- AP-BR-03: DRY within same document scope
- AP-BR-04: Compact object and list definitions
- AP-BR-05: Show format over describing format
- AP-BR-06: Pipe-delimited property lines for multi-attribute items

Structure (ST)
- AP-ST-01: Goal or intention captured first
- AP-ST-02: Subjects direct and actionable
- AP-ST-03: Self-contained units
- AP-ST-04: Anti-DRY for delegation (inline 100% for action requests)
- AP-ST-05: Hierarchical information ordering (general to specific)
- AP-ST-06: Visual thought grouping (cluster related, separate distinct)

Naming (NM)
- AP-NM-01: One name per concept (no polysemy, no synonyms)
- AP-NM-02: Unambiguous compound names (word order determines meaning)
- AP-NM-03: Avoid dangerous meta-words (Module, Service, Check, etc.)
- AP-NM-04: Word pairs must form intuitive opposites
- AP-NM-05: Use and keep standard terms (association field principle)

## Core Principle

**Priority 1: Precision** - Never sacrifice clarity for brevity. Every statement must be unambiguous.

**Priority 2: Brevity** - After precision is guaranteed, remove every unnecessary word. Never sacrifice a word that carries meaning.

- BAD: `P=1`, `F1=1` - GOOD: `Precision=1.00`, `F1-Score=1.00`

## Precision Rules (PR)

### AP-PR-01: Standardized Datetime Format

Use `YYYY-MM-DD HH:MM` everywhere. Context-specific variations:

- **In documents**: `YYYY-MM-DD HH:MM` - Example: `2026-03-19 14:30`
- **In logging**: `YYYY-MM-DD HH:MM:SS` - Example: `2026-03-19 14:30:23`
- **In filenames**: `YYYY-MM-DD` prefix - Example: `2026-03-19_ServerMigration.md`
- **In session folders**: `YYYY-MM-DD` prefix - Example: `_2026-03-19_FixAuthBug/`
- **In Document History**: `[YYYY-MM-DD HH:MM]` - Example: `**[2026-03-19 14:30]**`

Never use locale-dependent formats (`03/19/2026`, `19.03.2026`, `March 19, 2026`).

### AP-PR-02: Standardized Attribute/Property Format

Consistency within each context is mandatory.

**Logs**: `key='value'` with additional properties in parentheses
```
Processing library 'Documents' (id='045229b3', size=342)...
```

**Documents**: `- **Key**: Value`

**Code**: Follow language conventions (Python: snake_case, JS: camelCase)

### AP-PR-03: Standardized Contact Information Format

```
**John Smith** (john@acme.com)
- Role: Project Manager at Acme Corp
- Phone: +1 555 1234
- Timezone: EST
```

### AP-PR-05: Referenceable IDs on All Trackable Items

**Prerequisite for AP-PR-04.** Create IDs FIRST, then reference.

**What needs IDs:** Requirements (FR), decisions (DD), guarantees (IG), criteria (AC), problems (PR), bugs (BG), fixes (FX), failures (FL), tasks (TK), steps (IS), test cases (TC), sections (numbered headings), plan nodes (P1, P1-S1, P1-D1).

**ID formats by scope:**
- **Document-scoped** (2-digit): `CRWL-FR-01`, `AUTH-DD-03`
- **Tracking** (4-digit): `AUTH-PR-0001`, `GLOB-BG-0002`
- **Plan-scoped** (ephemeral): `P1-S1`, `P2-D1`
- **Headings** (implicit): `## 3. Implementation` -> "section 3"

**GOOD:**
```
- **UI-FR-01**: Toast notifications support info, success, error, warning types
- **AUTH-DD-01**: Use localStorage for token storage
- **AUTH-PR-0001**: Race condition on simultaneous token refresh
```

### AP-PR-04: Standardized Link and Reference Format

**Depends on AP-PR-05.** Three steps: Define ID system, Apply IDs, Use IDs to reference.

**Reference formats:**
- Document: `_SPEC_CRAWLER.md [CRWL-SP01]` (filename AND Doc ID)
- Section: `section 3.2` or `CRWL-FR-01`
- URL: `[Example Site](https://example.com)` (clickable Markdown)
- Cross-doc: `See CRWL-FR-01 in _SPEC_CRAWLER.md [CRWL-SP01]`

### AP-PR-06: Write Out Acronyms on First Use

Format: `Full Term (ACRONYM)`. After first use, acronym alone acceptable within same document.

GOOD: `Use On Behalf Of (OBO) for SharePoint Online (SPO) authentication via Managed Identity (MI).`

### AP-PR-07: Be Specific

No generic or abstract writing. Every statement must contain concrete, verifiable information.

- BAD: `The system handles errors appropriately.`
- GOOD: `Retry 3 times with exponential backoff (1s, 2s, 4s), then fail with ERROR status.`

### AP-PR-08: Every Non-Obvious Rule Needs Examples

Show BAD/GOOD pairs for every format rule, naming convention, and structural pattern.

- BAD: `Use descriptive names with proper prefixes.`
- GOOD: `_INFO_[TOPIC].md` - Research documents. Example: `_INFO_AUTHENTICATION.md`

### AP-PR-09: Consistent Patterns

Repeat established structures. Do not invent new forms for similar content. Before writing, identify established patterns and match exactly.

**Detects:** Same concept with multiple names, same structure expressed differently, overlapping forms.

- **List markers**: `- * +` mixed -> `- - -` one form
- **Properties**: `Key:` `**Key** -` `Key =` -> `**Key**:` throughout
- **Functions**: `get_` `fetch_` `load_` (same purpose) -> `get_` everywhere

## Brevity Rules (BR)

### AP-BR-01: Single Line for Single Statements

If a statement fits on one line, keep it on one line.

```
**Pause Button** (requests job pause):
<button class="btn-small" onclick="controlJob(42, 'pause')"> Pause </button>
```

### AP-BR-02: Sacrifice Grammar for Brevity

Drop articles, filler words, verbose constructions when meaning is preserved.

- BAD: `The system should automatically process the incoming files on a regular basis.`
- GOOD: `Auto-process incoming files on schedule.`

**Exception**: User-facing text, error messages, external communication preserve full grammar.

### AP-BR-03: DRY Within Same Document Scope

Never repeat same information within one document. Reference instead. (For action requests to others, AP-ST-04 overrides this.)

### AP-BR-04: Compact Object and List Definitions

Use lists. No empty lines between properties. No Markdown tables (unless opted-in).

```
### EXPLORE
- **Purpose**: Understand the situation before acting
- **BUILD**: What feature? What constraints?
- **Entry**: Start of workflow
```

### AP-BR-05: Show Format Over Describing Format

A format example communicates more precisely and briefly than a description.

```
## Todo Format
`- **YYYY-MM-DD HH:MM** - Item description - Deadline: YYYY-MM-DD, Status: TODO:ACTION`

Example:
- **2026-03-15 09:15** - Reply to John with proposal - Deadline: 2026-03-20, Status: TODO:REPLY
```

### AP-BR-06: Pipe-Delimited Property Lines for Multi-Attribute Items

Format: `Key: value | Key: value | ...` - always `Key: Value` pairs separated by ` | `. Bold ID starts first line. Group related properties per line.

**When to use:** 4+ properties, catalog items, metadata headers.
**When NOT to use:** Long values, nested data, fewer than 4 properties.

```
**SRV-042** Region: eu-west-1 | Type: m5.xlarge | CPU: 4 vCPU | RAM: 16 GB | Storage: 200 GB SSD
- Status: running | Uptime: 45 days
```

```
**PRD-007** Name: Widget Pro | Version: 2.1 | Price: $49.99 | Stock: yes
- Dimensions: 12x8x4 cm | Weight: 250g | Color: black, silver | Material: aluminum
- Link: https://example.com/products/widget-pro
- Status: DISCONTINUED (replaced by PRD-012)
```

**Conventions:**
- Always `Key: Value` format - no bare values without labels
- Bold ID on header line
- `?` for unknown values in documents (`[UNKNOWN]` is for logs)
- Group by concern: identity/metrics, physical attributes, terms/status

## Structure Rules (ST)

### AP-ST-01: Goal or Intention Captured First

Every document, section, communication starts with purpose. Reader knows WHY before HOW.

```
# Verify Workflow

Goal: Validated work with all issues identified and labeled
Why: Prevents shipping bugs, spec violations, and rule breaks
```

### AP-ST-02: Subjects Direct and Actionable

Headings and labels state the action or outcome, not the topic.

- BAD: `Subject: Meeting`
- GOOD: `Subject: ACTION: Review contract by 2026-03-20`

### AP-ST-03: Self-Contained Units

Each log line, document section, email must be understandable without reading other materials. Ask: "Can the reader act on this without seeking additional information?"

- BAD: `As discussed, please proceed with option 2.`
- GOOD: `Please proceed with Option 2: JWT tokens stored in httpOnly cookies with 15-minute expiry and silent refresh.`

**In logs**: `[ 1 / 2 ] Calling gpt-5-mini to extract 5 records from 20 rows...`

### AP-ST-04: Anti-DRY for Delegation (overrides AP-BR-03)

When requesting action from others, inline ALL needed information. Do NOT reference threads or external docs as the only source. People do not read referenced sources. BR-03 avoids self-repetition for a reader who has the full document; ST-04 ensures a recipient can act without seeking additional sources.

**GOOD:**
```
Please implement these 3 changes to the auth module by 2026-03-25:

1. Replace localStorage token storage with httpOnly cookies
   - Set SameSite=Strict, Secure=true
   - Implementation: src/auth/tokenStore.js

2. Add silent token refresh 5 minutes before expiry
   - Use /api/auth/refresh endpoint
   - Retry 3 times with 2s backoff

3. Add mutex lock for concurrent refresh requests

Full spec: _SPEC_AUTH.md [AUTH-SP01] section 3.2
```

### AP-ST-05: Hierarchical Information Ordering

Order from general to specific. Most important first, details follow.

- BAD: `The button uses a 4px border radius with #0078d4 color and sends a POST request to /api/jobs/start which creates a new crawl job. It's the main action button.`
- GOOD: `[Start Job] - Creates new crawl job via POST /api/jobs/start. Dashboard main action. Style: #0078d4, 4px border-radius.`

### AP-ST-06: Visual Thought Grouping

Related content clusters together (no empty lines); distinct thoughts separate by one empty line.

```
- **Started**: 2026-03-17
- **Goal**: Fix authentication
- **Status**: In Progress

## Next Section
```

No empty lines within one activity; indentation shows nesting; activities separate naturally. Applies to specs, emails, code, logs.

## Naming Rules (NM)

### AP-NM-01: One Name Per Concept

One concept = one name, used everywhere. No synonyms, no polysemy.

- BAD: `"garage" / "service" / "workshop"` (3 names for same concept)
- GOOD: `"workshop"` everywhere
- BAD (polysemy): `"Meter"` = connection point AND physical device AND customer relationship
- GOOD: `"MeterPoint"` (connection), `"MeterDevice"` (physical), `"MeterContract"` (customer)

### AP-NM-02: Unambiguous Compound Names

Word order determines meaning. If multiple readings possible, restructure.

- BAD: `EmptyCollectionKey` -> GOOD: `KeyOfEmptyCollection`
- BAD: `InvalidUserInput` -> GOOD: `InputFromInvalidUser`

### AP-NM-03: Avoid Dangerous Meta-Words

**Dangerous words:** Module, Service, Generation, Check, Payload, Workload, Cargo, Network, Monitor, View, Console, Facade, Provider, Asset

When you must use them, qualify until the name answers "what does it contain/do/provide?"

- BAD: `ProductModule` -> GOOD: `ProductCatalog`
- BAD: `UserService` -> GOOD: `UserAuthProvider`
- BAD: `Check` -> GOOD: `ValidateUserExists` (returns yes/no) or `RunDataCleanup` (performs action)

### AP-NM-04: Intuitive Word Pairs

Opposites must form intuitive pairs. Users predict the counterpart from the first name.

- BAD: `EncodeUrl() / PlainText()` -> GOOD: `EncodeUrl() / DecodeUrl()`

### AP-NM-05: Use and Keep Standard Terms

Use established terminology. If a name worked for years, don't rename it even if it became a misnomer. People predict behavior by the evoked association field, not the literal name.

- Keep `login()` even when credentials no longer required - "Login" already means "authenticate"
- Keep `save()` even when it writes to cloud - "Save" already means "persist my work"
- Build new API if behavior actually changes: `login()` stays, add `sso_connect()` for new flow

**Intentional deviation:** State it explicitly. Example: `"Activity" (not "task") - we use "task" for TASKS documents, so "activity" avoids term collision.`