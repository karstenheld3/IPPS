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

**Priority 1: Precision** - Never sacrifice clarity for brevity. Every statement unambiguous.
**Priority 2: Brevity** - After precision guaranteed, remove every unnecessary word.

- BAD: `P=1` (unclear) / GOOD: `Precision=1.00` (full name, type-indicating decimals)
- Verbose writing without added precision equally bad (see AP-BR-02)

## Precision Rules (PR)

### AP-PR-01: Standardized Datetime Format

- **Documents**: `YYYY-MM-DD HH:MM` → `2026-03-19 14:30`
- **Logging**: `YYYY-MM-DD HH:MM:SS` → `2026-03-19 14:30:23`
- **Filenames**: `YYYY-MM-DD` prefix → `2026-03-19_ServerMigration.md`
- **Session folders**: `YYYY-MM-DD` prefix → `_2026-03-19_FixAuthBug/`
- **Document History**: `[YYYY-MM-DD HH:MM]` → `**[2026-03-19 14:30]**`

Never use locale-dependent formats (`03/19/2026`, `19.03.2026`, `March 19, 2026`).

### AP-PR-02: Standardized Attribute/Property Format

Consistency within each context mandatory.

**Logs**: `key='value'` with parenthesized extras
```
Processing library 'Documents' (id='045229b3', size=342)...
```
**Documents**: `**Key**: Value` or `- **Key**: Value`
**Code**: Follow language conventions

BAD (mixed): `Processing file report.csv` / `Site URL: https://...` / `Library: Documents (id: 045229b3)`
GOOD (consistent): `Processing file='report.csv'...` / `Library: title='Documents' (id='045229b3')`

### AP-PR-03: Standardized Contact Information Format

```
**John Smith** (john@acme.com)
- Role: Project Manager at Acme Corp
- Phone: +1 555 1234
- Timezone: EST
```

### AP-PR-05: Referenceable IDs on All Trackable Items

**Prerequisite for AP-PR-04.** Create IDs FIRST, then reference.

**What needs IDs:** Requirements (FR), decisions (DD), guarantees (IG), criteria (AC), problems (PR), bugs (BG), fixes (FX), failures (FL), tasks (TK), steps (IS), test cases (TC), sections (numbered headings), plan nodes (P1, P1-S1)

**ID formats by scope:**
- **Document-scoped** (2-digit): `CRWL-FR-01`, `AUTH-DD-03`
- **Tracking** (4-digit): `AUTH-PR-0001`, `GLOB-BG-0002`
- **Plan-scoped** (ephemeral): `P1-S1`, `P2-D1`
- **Headings** (implicit): `## 3. Implementation` → "section 3"

BAD: `Toast notifications should support info, success, error types`
GOOD: `**UI-FR-01**: Toast notifications support info, success, error, warning types`

### AP-PR-04: Standardized Link and Reference Format

**Depends on AP-PR-05.** Define ID system → apply IDs → use IDs to reference.

**Reference formats:**
- Document: `_SPEC_CRAWLER.md [CRWL-SP01]` (filename AND Doc ID)
- Section: `section 3.2` or `CRWL-FR-01`
- URL: `[Example Site](https://example.com)`
- Cross-doc: `See CRWL-FR-01 in _SPEC_CRAWLER.md [CRWL-SP01]`

BAD: `See the crawler spec for requirements.` / `As mentioned above...`
GOOD: `Per CRWL-FR-01, the crawler must...`

### AP-PR-06: Write Out Acronyms on First Use

Format: `Full Term (ACRONYM)`. After first use, acronym alone acceptable within same document.

BAD: `Use OBO for SPO authentication via MI.`
GOOD: `Use On Behalf Of (OBO) for SharePoint Online (SPO) authentication via Managed Identity (MI).`

### AP-PR-07: Be Specific

Every statement must contain concrete, verifiable information.

BAD: `The system handles errors appropriately.`
GOOD: `Retry 3 times with exponential backoff (1s, 2s, 4s), then fail with ERROR status.`

### AP-PR-08: Every Non-Obvious Rule Needs Examples

Show BAD/GOOD pairs for every format rule, naming convention, structural pattern.

BAD: `Use descriptive names with proper prefixes.`
GOOD: `_INFO_[TOPIC].md` - Research documents. Example: `_INFO_AUTHENTICATION.md`

### AP-PR-09: Consistent Patterns

Repeat established structures. Do not invent new forms for similar content. Inconsistency signals unclear thinking.

Before writing, identify established patterns from existing documents. Match exactly.

- **List markers**: `- * +` mixed → `- - -` one form
- **Headings**: `## 1.` `## Design` `## IV.` → `## 1.` `## 2.` `## 3.`
- **Properties**: `Key:` `**Key** -` `Key =` → `**Key**:` throughout
- **Functions**: `get_` `fetch_` `load_` (same purpose) → `get_` everywhere

## Brevity Rules (BR)

### AP-BR-01: Single Line for Single Statements

If a statement fits on one line, keep it on one line.

BAD: Button label, parenthetical, and HTML tag on 4 separate lines
GOOD: `**Pause Button** (requests job pause): <button class="btn-small" onclick="controlJob(42, 'pause')"> Pause </button>`

### AP-BR-02: Sacrifice Grammar for Brevity

Drop articles, filler words, verbose constructions when meaning preserved.

BAD: `The system should automatically process the incoming files on a regular basis.`
GOOD: `Auto-process incoming files on schedule.`

**Exception**: User-facing text, error messages, external communication preserve full grammar.

### AP-BR-03: DRY Within Same Document Scope

Reference instead of restating. For delegation to others, see AP-ST-04 (overrides this).

BAD: Restating `YYYY-MM-DD HH:MM` format in multiple sections
GOOD: `Timestamps follow AP-PR-01.`

### AP-BR-04: Compact Object and List Definitions

Use lists. No empty lines between properties. No Markdown tables (unless opted-in).

BAD: Each property as its own bold paragraph with blank lines between
GOOD: `- **Purpose**: ...` / `- **BUILD**: ...` / `- **Entry**: ...`

### AP-BR-05: Show Format Over Describing Format

A format example communicates more precisely and briefly than description.

BAD: Prose describing todo format fields and order
GOOD:
```
`- **YYYY-MM-DD HH:MM** - Item description - Deadline: YYYY-MM-DD, Status: TODO:ACTION`
Example: - **2026-03-15 09:15** - Reply to John with proposal - Deadline: 2026-03-20, Status: TODO:REPLY
```

### AP-BR-06: Pipe-Delimited Property Lines for Multi-Attribute Items

Use ` | ` to separate `Key: Value` pairs on single lines. Bold ID starts first line. Group related properties per line.

**When to use:** 4+ properties, catalog items, metadata headers
**When NOT to use:** Long values, nested data, fewer than 4 properties

BAD (bare values): `**SRV-042** eu-west-1 | m5.xlarge | 4 vCPU | 16 GB`
GOOD (labeled):
```
**SRV-042** Region: eu-west-1 | Type: m5.xlarge | CPU: 4 vCPU | RAM: 16 GB | Storage: 200 GB SSD
- Status: running | Uptime: 45 days
```

GOOD (complete metadata):
```
From: john@example.com | To: me@example.com | CC: team@example.com | BCC: -
- Subject: Re: Q2 Timeline | Reply-To: - | Thread: Q2 Planning | Message-ID: abc123
- Date: 2026-03-17 14:30 | Attachments: Q2_Timeline.pdf (1.2MB)
```

GOOD (product catalog):
```
**PRD-007** Name: Widget Pro | Version: 2.1 | Price: $49.99 | Stock: yes
- Dimensions: 12x8x4 cm | Weight: 250g | Color: black, silver | Material: aluminum
- Status: DISCONTINUED (replaced by PRD-012)
```

**Conventions:**
- Always `Key: Value` format - no bare values
- Bold ID on header line
- `?` for unknown in documents, `[UNKNOWN]` in logs
- Group by concern: identity/metrics, physical attributes, terms/status

## Structure Rules (ST)

### AP-ST-01: Goal or Intention Captured First

Every document, section, communication starts with purpose. Reader knows WHY before HOW.

BAD: Jump to steps without stating goal
GOOD: `Goal: Validated work with all issues identified and labeled`

### AP-ST-02: Subjects Direct and Actionable

Headings and subjects state action or outcome, not topic.

BAD: `Subject: Meeting` / `### Authentication Section`
GOOD: `Subject: ACTION: Review contract by 2026-03-20` / `### AUTH-DD-01: Use JWT with httpOnly Cookie Storage`

### AP-ST-03: Self-Contained Units

Each unit understandable without reading other materials. Test: "Can reader act on this alone?"

BAD: `As discussed, please proceed with option 2.`
GOOD: `Please proceed with Option 2: JWT tokens stored in httpOnly cookies with 15-minute expiry and silent refresh.`

**In logs** (Full Disclosure):
BAD: `[ 1 / 2 ] LLM extraction run 1...`
GOOD: `[ 1 / 2 ] Calling gpt-5-mini to extract 5 records from 20 rows...`

### AP-ST-04: Anti-DRY for Delegation (overrides AP-BR-03)

When requesting action from others, inline ALL needed information. People do not read referenced sources. BR-03 avoids self-repetition for same-document reader; ST-04 ensures recipient can act without seeking additional sources.

BAD: `As per our discussion and the attached spec (see section 3.2), please implement the changes we agreed on.`
GOOD: List all 3 changes inline with file paths, parameters, and retry logic, then reference spec for full context.

### AP-ST-05: Hierarchical Information Ordering

General to specific. Most important first, details follow.

BAD: `The button uses a 4px border radius with #0078d4 color and sends a POST request to /api/jobs/start which creates a new crawl job. It's the main action button.`
GOOD: `[Start Job] - Creates new crawl job via POST /api/jobs/start. Dashboard main action. Style: #0078d4, 4px border-radius.`

### AP-ST-06: Visual Thought Grouping

Related content clusters together (no empty lines); distinct thoughts separate by one empty line.

BAD (scattered):
```
- **Started**: 2026-03-17

- **Goal**: Fix authentication

- **Status**: In Progress
```

GOOD (grouped):
```
- **Started**: 2026-03-17
- **Goal**: Fix authentication
- **Status**: In Progress
```

Applies to docs, logs, code, email. In logs: no empty lines within one activity; indentation shows nesting.
```
Processing 3 libraries...
  [ 1 / 3 ] Processing library 'Documents'...
    342 files retrieved.
    OK.
  [ 2 / 3 ] Processing library 'Reports'...
    ERROR: Access denied -> (403) Forbidden
  FAIL: 2 libraries processed, 1 failed.
```

In code: group related statements, separate distinct concerns by one blank line.

## Naming Rules (NM)

### AP-NM-01: One Name Per Concept

One concept = one name everywhere. No synonyms, no polysemy.

Synonyms cause search failures. Polysemy causes silent misunderstandings.

BAD: "garage" / "service" / "workshop" (3 names, same concept)
GOOD: "workshop" everywhere - UI, API, database, documentation

BAD (polysemy): "Meter" = connection point AND device AND contract
GOOD: "MeterPoint" (connection), "MeterDevice" (physical), "MeterContract" (customer)

### AP-NM-02: Unambiguous Compound Names

Word order determines meaning. If multiple readings possible, restructure.

BAD: `EmptyCollectionKey` (collection empty or key empty?)
GOOD: `KeyOfEmptyCollection`

### AP-NM-03: Avoid Dangerous Meta-Words

Dangerous words: Module, Service, Generation, Check, Payload, Workload, Cargo, Network, Monitor, View, Console, Facade, Provider, Asset

When used, qualify until name answers "what does it contain/do/provide?"

BAD: `ProductModule`, `UserService`, `Check`
GOOD: `ProductCatalog`, `UserAuthProvider`, `ValidateUserExists`, `RunDataCleanup`

### AP-NM-04: Intuitive Word Pairs

Opposites must form predictable pairs. Users predict counterpart from first name.

BAD: `EncodeUrl()` / `PlainText()` → users search for `DecodeUrl()`, fail
GOOD: `EncodeUrl()` / `DecodeUrl()`

### AP-NM-05: Use and Keep Standard Terms

Use established terminology. Don't rename working names even if they became misnomers. People predict behavior by the evoked association field, not the literal name.

BAD: Rename `login()` → `authenticate()` because credentials no longer required
GOOD: Keep `login()` (means "authenticate" in users' minds). Add `sso_connect()` for genuinely new flow.

**Intentional deviation:** State it: `"Activity" (not "task") - we use "task" for TASKS documents, so "activity" avoids term collision.`