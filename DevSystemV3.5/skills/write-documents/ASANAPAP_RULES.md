<DevSystem MarkdownTablesAllowed=true EmojisAllowed=true />

# ASANAPAP Writing Rules

Rules for applying the ASANAPAP principle across all document types, code, logging, and communication.

**ASANAPAP** = As Short As Necessary (Priority 2), As Precise As Possible (Priority 1)

## Rule Index

Precision (PR) - Priority 1
- AP-PR-01: Standardized datetime format
- AP-PR-02: Standardized attribute/property format
- AP-PR-03: Standardized contact information format
- AP-PR-04: Standardized link and reference format
- AP-PR-05: Referenceable IDs on all trackable items
- AP-PR-06: Write out acronyms on first use
- AP-PR-07: Use standard industry terms; clarify deviations
- AP-PR-08: Be specific - no generic or abstract writing
- AP-PR-09: Every non-obvious rule or format needs examples
- AP-PR-10: Pipe-delimited property lines for multi-attribute items

Brevity (BR) - Priority 2
- AP-BR-01: Single line for single statements
- AP-BR-02: Sacrifice grammar for brevity
- AP-BR-03: DRY within same document scope
- AP-BR-04: Compact object and list definitions
- AP-BR-05: Show format over describing format

Structure (ST)
- AP-ST-01: Goal or intention captured first
- AP-ST-02: Subjects direct and actionable
- AP-ST-03: Self-contained units
- AP-ST-04: Anti-DRY for delegation (inline 100% for action requests)
- AP-ST-05: Hierarchical information ordering (general to specific)

## Table of Contents

- [Core Principle](#core-principle)
- [Precision Rules (PR)](#precision-rules-pr)
- [Brevity Rules (BR)](#brevity-rules-br)
- [Structure Rules (ST)](#structure-rules-st)
- [Coverage Matrix](#coverage-matrix)
- [Gap Analysis](#gap-analysis)

## Core Principle

**Priority 1: Precision** - Never sacrifice clarity for brevity. Every statement must be unambiguous. A reader must understand exactly what is meant without guessing.

**Priority 2: Brevity** - After precision is guaranteed, remove every unnecessary word. Sacrifice grammar, filler, and repetition. But never sacrifice a word that carries meaning.

**Anti-pattern**: Cryptic abbreviations sacrifice precision for brevity.
- BAD: `P=1`, `F1=1` - unclear type, unclear meaning
- GOOD: `Precision=1.00`, `F1-Score=1.00` - full name, 2 decimals indicate float

**Anti-pattern**: Verbose writing sacrifices brevity without adding precision.
- BAD: "The system should be configured in such a way that it automatically processes incoming files on a regular basis."
- GOOD: "Auto-process incoming files on schedule."

## Precision Rules (PR)

### AP-PR-01: Standardized Datetime Format

Use `YYYY-MM-DD HH:MM` everywhere. Exception: logging timestamps use `YYYY-MM-DD HH:MM:SS`.

**BAD:**
```
March 17, 2026 2:30 PM
17.03.2026 14:30
3/17/26
last Tuesday
```

**GOOD:**
```
2026-03-17 14:30
[2026-03-17 14:30:23]  (logging only)
```

### AP-PR-02: Standardized Attribute/Property Format

Context determines format. Consistency within each context is mandatory.

**Logs**: `key='value'` with additional properties in parentheses
```
Processing library 'Documents' (id='045229b3', size=342)...
```

**Documents**: `**Key**: Value` or `- **Key**: Value`
```
- **Started**: 2026-03-17
- **Goal**: Fix authentication
```

**Code**: Follow language conventions (Python: snake_case, JS: camelCase)

**BAD** (mixing formats):
```
Processing file report.csv
Site URL: https://example.com
Library: Documents (id: 045229b3)
```

**GOOD** (consistent):
```
Processing file='report.csv'...
  Site: url='https://example.com'
  Library: title='Documents' (id='045229b3')
```

### AP-PR-03: Standardized Contact Information Format

Structured contact blocks with all relevant fields.

**BAD:**
```
John from Acme Corp, email john@acme.com, call him at +1 555 1234
```

**GOOD:**
```
**John Smith** (john@acme.com)
- Role: Project Manager at Acme Corp
- Phone: +1 555 1234
- Timezone: EST
```

### AP-PR-04: Standardized Link and Reference Format

All URLs as clickable Markdown links. All document references by filename AND Doc ID.

**BAD:**
```
Check https://example.com for details.
See the crawler spec for requirements.
```

**GOOD:**
```
Check [Example Site](https://example.com) for details.
See `_SPEC_CRAWLER.md [CRWL-SP01]` for requirements.
```

### AP-PR-05: Referenceable IDs on All Trackable Items

Every requirement, decision, problem, bug, task, and finding must have a unique ID.

**BAD:**
```
- Toast notifications should support info, success, error types
- We decided to use localStorage
- There's a race condition in the auth flow
```

**GOOD:**
```
- **UI-FR-01**: Toast notifications support info, success, error, warning types
- **AUTH-DD-01**: Use localStorage for token storage
- **AUTH-PR-0001**: Race condition on simultaneous token refresh
```

### AP-PR-06: Write Out Acronyms on First Use

Format: `Full Term (ACRONYM)`. After first use, acronym alone is acceptable within same document.

**BAD:**
```
Use OBO for SPO authentication via MI.
Check the MNF list before completing.
```

**GOOD:**
```
Use On Behalf Of (OBO) for SharePoint Online (SPO) authentication via Managed Identity (MI).
Check the MUST-NOT-FORGET (MNF) list before completing.
```

### AP-PR-07: Use Standard Industry Terms

Use established terminology. When deviating intentionally, state the deviation and reason.

**BAD:**
```
The data holder sends info to the checker which puts it in the box.
```

**GOOD:**
```
The API client sends the payload to the validator which persists it to the message queue.
```

**Intentional deviation:**
```
"Activity" (not "task") - we use "task" for TASKS documents, so "activity" avoids term collision.
```

### AP-PR-08: Be Specific

No generic or abstract writing. Every statement must contain concrete, verifiable information.

**BAD:**
```
The system handles errors appropriately.
Performance should be acceptable.
The feature works as expected.
```

**GOOD:**
```
Retry 3 times with exponential backoff (1s, 2s, 4s), then fail with ERROR status.
Response time < 200ms for 95th percentile under 100 concurrent users.
Toast auto-dismisses after 5000ms, supports info/success/error/warning types.
```

### AP-PR-09: Every Non-Obvious Rule Needs Examples

Rules without examples are ambiguous. Show BAD/GOOD pairs for every format rule, naming convention, and structural pattern.

**BAD:**
```
## File Naming
Use descriptive names with proper prefixes.
```

**GOOD:**
```
## File Naming
- `_INFO_[TOPIC].md` - Research documents. Example: `_INFO_AUTHENTICATION.md`
- `_SPEC_[COMPONENT].md` - Specifications. Example: `_SPEC_CRAWLER.md`
```

### AP-PR-10: Pipe-Delimited Property Lines for Multi-Attribute Items

For items with many properties, use ` | ` (pipe with spaces) to separate values on a single line. Group related properties per line.

**Format:** `Key: value | Key: value | ...` - always use `Key: Value` pairs separated by ` | `. Bold ID starts the first line. Group related properties per line.

**When to use:** 4+ properties, catalog items, metadata headers, anything where vertical lists waste space.
**When NOT to use:** Long values, nested data, fewer than 4 properties.

**BAD** (12 lines for one item):
```
### SRV-042
- **Region**: eu-west-1
- **Type**: m5.xlarge
- **CPU**: 4 vCPU
- **RAM**: 16 GB
- **Storage**: 200 GB SSD
- **Status**: running
- **Uptime**: 45 days
```

**BAD** (pipe-delimited but bare values - reader must guess what each field means):
```
**SRV-042** eu-west-1 | m5.xlarge | 4 vCPU | 16 GB | 200 GB SSD
running | 45 days
```

**GOOD** (same data, every value labeled):
```
**SRV-042** Region: eu-west-1 | Type: m5.xlarge | CPU: 4 vCPU | RAM: 16 GB | Storage: 200 GB SSD
Status: running | Uptime: 45 days
```

**BAD** (missing fields, partial metadata):
```
From: john@example.com
To: me@example.com
Subject: Re: Q2 Timeline
```

**GOOD** (all fields present, `-` for empty):
```
From: john@example.com | To: me@example.com | CC: team@example.com | BCC: -
Subject: Re: Q2 Timeline | Reply-To: - | Thread: Q2 Planning | Message-ID: abc123
Date: 2026-03-17 14:30 | Attachments: Q2_Timeline.pdf (1.2MB)
```

**BAD** (mixed formats, inconsistent labels):
```
PRD-007 - Widget Pro v2.1, costs $49.99, in stock
12x8x4 cm, 250g, available in black and silver, made of aluminum
```

**GOOD** (consistent Key: Value, grouped by concern):
```
**PRD-007** Name: Widget Pro | Version: 2.1 | Price: $49.99 | Stock: yes
  Dimensions: 12x8x4 cm | Weight: 250g | Color: black, silver | Material: aluminum
  Link: https://example.com/products/widget-pro
  Status: DISCONTINUED (replaced by PRD-012)
```

**Conventions:**
- Always `Key: Value` format - no bare values without labels
- Bold ID on header line
- `?` for unknown values in documents (`[UNKNOWN]` is for logs)
- Group by concern: identity/metrics, physical attributes, terms/status

## Brevity Rules (BR)

### AP-BR-01: Single Line for Single Statements

If a statement, decision, or object fits on one line, keep it on one line.

**BAD:**
```
**Pause Button**
(requests job pause):
<button class="btn-small"
  onclick="controlJob(42, 'pause')">
  Pause
</button>
```

**GOOD:**
```
**Pause Button** (requests job pause):
<button class="btn-small" onclick="controlJob(42, 'pause')"> Pause </button>
```

### AP-BR-02: Sacrifice Grammar for Brevity

Drop articles (a, the, an), filler words (basically, actually, just), and verbose constructions when meaning is preserved.

**BAD:**
```
The system should automatically process the incoming files on a regular basis.
Before starting, you should read the relevant documents based on the current mode.
```

**GOOD:**
```
Auto-process incoming files on schedule.
SESSION-MODE: Read NOTES.md, PROBLEMS.md, PROGRESS.md, FAILS.md
```

**Exception**: User-facing text, error messages, and external communication preserve full grammar for professionalism.

### AP-BR-03: DRY Within Same Document Scope

Never repeat the same information within one document. Reference instead of restating.

**BAD:**
```
## Section A
Use `YYYY-MM-DD HH:MM` format for all timestamps.

## Section B
Remember to use `YYYY-MM-DD HH:MM` format for timestamps here too.
```

**GOOD:**
```
## Section A
Use `YYYY-MM-DD HH:MM` format for all timestamps.

## Section B
Timestamps follow AP-PR-01.
```

### AP-BR-04: Compact Object and List Definitions

Use lists. No empty lines between properties. No Markdown tables (unless opted-in).

**BAD:**
```
### EXPLORE

**Purpose**: Understand the situation before acting

**BUILD focus**: What feature? What constraints?

**Entry**: Start of workflow
```

**GOOD:**
```
### EXPLORE

- **Purpose**: Understand the situation before acting
- **BUILD**: What feature? What constraints?
- **Entry**: Start of workflow
```

### AP-BR-05: Show Format Over Describing Format

A format example communicates more precisely and more briefly than a description.

**BAD:**
```
## Todo Format
Todos should start with a bold timestamp in YYYY-MM-DD HH:MM format,
followed by a dash, then the item description, then optionally a deadline
in the same format preceded by "Deadline:", then a status field.
```

**GOOD:**
```
## Todo Format
`- **YYYY-MM-DD HH:MM** - Item description - Deadline: YYYY-MM-DD, Status: TODO:ACTION`

Example:
- **2026-03-15 09:15** - Reply to John with proposal - Deadline: 2026-03-20, Status: TODO:REPLY
```

## Structure Rules (ST)

### AP-ST-01: Goal or Intention Captured First

Every document, section, and communication starts with purpose. Reader knows WHY before HOW.

**BAD:**
```
# Verify Workflow

## Required Skills
...

## Steps
1. Read documents
2. Check rules
```

**GOOD:**
```
# Verify Workflow

**Goal**: Validated work with all issues identified and labeled
**Why**: Prevents shipping bugs, spec violations, and rule breaks

## Required Skills
...
```

### AP-ST-02: Subjects Direct and Actionable

Email subjects, headings, and labels state the action or outcome, not the topic.

**BAD:**
```
Subject: Meeting
Subject: Update
Subject: Question about the project
### Authentication Section
```

**GOOD:**
```
Subject: ACTION: Review contract by 2026-03-20
Subject: FYI: Q2 timeline moved to April 15
Subject: DECISION NEEDED: Choose auth provider by Friday
### AUTH-DD-01: Use JWT with httpOnly Cookie Storage
```

### AP-ST-03: Self-Contained Units

Each log line, document section, email, or message must be understandable without reading other materials. Ask: "Can the reader act on this without seeking additional information?"

**BAD:**
```
As discussed, please proceed with option 2.
See previous email for details.
```

**GOOD:**
```
Please proceed with Option 2: JWT tokens stored in httpOnly cookies
with 15-minute expiry and silent refresh. Implementation guide
attached (auth_impl_v2.pdf).
```

**In logs** (Full Disclosure principle):
```
BAD:  [ 1 / 2 ] LLM extraction run 1...
GOOD: [ 1 / 2 ] Calling gpt-5-mini to extract 5 records from 20 rows...
```

### AP-ST-04: Anti-DRY for Delegation

When requesting action from others, inline ALL needed information. Do NOT reference threads or external docs as the only source. People do not read referenced sources.

**BAD:**
```
Hi John,

As per our discussion and the attached spec (see section 3.2),
please implement the changes we agreed on.

Thanks
```

**GOOD:**
```
Hi John,

Please implement these 3 changes to the auth module by 2026-03-25:

1. Replace localStorage token storage with httpOnly cookies
   - Set SameSite=Strict, Secure=true
   - Implementation: src/auth/tokenStore.js

2. Add silent token refresh 5 minutes before expiry
   - Use /api/auth/refresh endpoint
   - Retry 3 times with 2s backoff

3. Add mutex lock for concurrent refresh requests
   - Only one refresh request at a time
   - Queue subsequent requests until first completes

Full spec: _SPEC_AUTH.md [AUTH-SP01] section 3.2
Previous discussion: [Email 2026-03-15](#2026-03-15-1430---auth-design-review)
```

### AP-ST-05: Hierarchical Information Ordering

Order information from general to specific. Most important first, details follow.

**BAD:**
```
The button uses a 4px border radius with #0078d4 color and sends a POST
request to /api/jobs/start which creates a new crawl job for the site.
It's the main action button on the dashboard.
```

**GOOD:**
```
[Start Job] - Creates new crawl job via POST /api/jobs/start.
Dashboard main action. Style: #0078d4, 4px border-radius.
```

## Coverage Matrix

How ASANAPAP rules map to existing rule documents. ✅ = codified, ⚠️ = partial, ❌ = gap.

| Rule       | core-conv | SPEC_RULES | WF_RULES | CV_RULES | LOG_RULES | LOG_UF | PYTHON | SKILL.md |
|------------|-----------|------------|----------|----------|-----------|--------|--------|----------|
| AP-PR-01   | ✅ Yes     | ✅ Yes      | ❌ No     | ✅ Yes    | ✅ Yes     | ✅ Yes  | ⚠️ tz   | ❌ No     |
| AP-PR-02   | ❌ No      | ✅ Yes      | ❌ No     | ❌ No     | ✅ Yes     | ❌ No   | ❌ No   | ❌ No     |
| AP-PR-03   | ❌ No      | ❌ No       | ❌ No     | ✅ Yes    | ❌ No      | ❌ No   | ❌ No   | ❌ No     |
| AP-PR-04   | ✅ Yes     | ❌ No       | ✅ Yes    | ✅ Yes    | ❌ No      | ❌ No   | ❌ No   | ✅ Yes    |
| AP-PR-05   | ✅ Yes     | ✅ Yes      | ❌ No     | ⚠️ Partial | ❌ No    | ❌ No   | ❌ No   | ✅ Yes    |
| AP-PR-06   | ❌ No      | ❌ No       | ✅ Yes    | ❌ No     | ✅ Yes     | ❌ No   | ❌ No   | ❌ No     |
| AP-PR-07   | ❌ No      | ❌ No       | ❌ No     | ❌ No     | ❌ No      | ❌ No   | ❌ No   | ❌ No     |
| AP-PR-08   | ❌ No      | ✅ Yes      | ✅ Yes    | ❌ No     | ✅ Yes     | ✅ Yes  | ❌ No   | ❌ No     |
| AP-PR-09   | ❌ No      | ✅ Yes      | ✅ Yes    | ✅ Yes    | ✅ Yes     | ✅ Yes  | ✅ Yes  | ❌ No     |
| AP-PR-10   | ❌ No      | ❌ No       | ❌ No     | ✅ Yes    | ❌ No      | ❌ No   | ❌ No   | ❌ No     |
| AP-BR-01   | ✅ Yes     | ✅ Yes      | ❌ No     | ❌ No     | ❌ No      | ❌ No   | ✅ Yes  | ❌ No     |
| AP-BR-02   | ❌ No      | ❌ No       | ❌ No     | ❌ No     | ❌ No      | ❌ No   | ❌ No   | ✅ Yes    |
| AP-BR-03   | ❌ No      | ❌ No       | ✅ Yes    | ❌ No     | ❌ No      | ❌ No   | ✅ Yes  | ✅ Yes    |
| AP-BR-04   | ⚠️ Partial | ✅ Yes      | ❌ No     | ❌ No     | ❌ No      | ❌ No   | ❌ No   | ❌ No     |
| AP-BR-05   | ❌ No      | ❌ No       | ✅ Yes    | ❌ No     | ❌ No      | ❌ No   | ❌ No   | ❌ No     |
| AP-ST-01   | ✅ Yes     | ✅ Yes      | ✅ Yes    | ❌ No     | ❌ No      | ✅ Yes  | ❌ No   | ❌ No     |
| AP-ST-02   | ❌ No      | ❌ No       | ❌ No     | ⚠️ Partial | ❌ No    | ❌ No   | ❌ No   | ❌ No     |
| AP-ST-03   | ❌ No      | ❌ No       | ❌ No     | ❌ No     | ✅ Yes     | ✅ Yes  | ❌ No   | ❌ No     |
| AP-ST-04   | ❌ No      | ❌ No       | ❌ No     | ❌ No     | ❌ No      | ❌ No   | ❌ No   | ❌ No     |
| AP-ST-05   | ❌ No      | ❌ No       | ❌ No     | ❌ No     | ❌ No      | ❌ No   | ❌ No   | ❌ No     |

**Legend**: core-conv = `core-conventions.md`, WF = `WORKFLOW_RULES.md`, CV = `CONVERSATION_RULES.md`, LOG = `LOGGING-RULES.md`, LOG_UF = `LOGGING-RULES-USER-FACING.md`, PYTHON = `PYTHON-RULES.md`

## Gap Analysis

### Fully Covered (codified in 3+ documents)

- **AP-PR-01** (datetime) - Well covered across core-conventions, SPEC, CONVERSATION, LOGGING
- **AP-PR-09** (examples) - All _RULES.md files use BAD/GOOD pattern consistently
- **AP-PR-04** (links/refs) - Covered in core-conventions, WORKFLOW_RULES, CONVERSATION_RULES
- **AP-BR-01** (single line) - core-conventions, SPEC_RULES, PYTHON-RULES

### Partially Covered (1-2 documents)

- **AP-PR-02** (attribute format) - Only LOG-GN-06 and SPEC-CT-06. Missing from core-conventions as cross-cutting rule
- **AP-PR-05** (IDs) - Strong in devsystem-ids.md and SPEC_RULES, but not enforced in CONVERSATION or WORKFLOW docs
- **AP-PR-06** (acronyms) - Only LOG-GN-12 and WF-CT-02. Should be in core-conventions
- **AP-PR-08** (be specific) - Logging has Full Disclosure, SPEC has examples, but missing as explicit cross-cutting rule
- **AP-BR-03** (DRY) - WORKFLOW anti-pattern and SKILL.md mention it, not in core-conventions
- **AP-ST-01** (goal first) - Templates enforce it, but no explicit rule
- **AP-ST-03** (self-contained) - Strong in logging philosophy, missing from document rules

### Not Covered (gaps requiring new rules)

- **AP-PR-10** (pipe-delimited properties) - Only CONVERSATION_RULES email header format. Not codified as general pattern
- **AP-PR-03** (contact format) - Only in CONVERSATION_TEMPLATE as structure, not as a rule
- **AP-PR-07** (industry terms) - Not codified anywhere. Should be in core-conventions
- **AP-BR-02** (grammar sacrifice) - Only SKILL.md agent behavior. Needs elevation to writing rule
- **AP-BR-04** (compact definitions) - SPEC-CT-06 covers it for specs, needs cross-cutting rule
- **AP-BR-05** (format over description) - WF-CT-06 partially, needs explicit rule
- **AP-ST-02** (actionable subjects) - CV-TD-01 has todo actions, but email/heading subjects not covered
- **AP-ST-04** (anti-DRY delegation) - Completely new. Not codified anywhere
- **AP-ST-05** (hierarchical ordering) - Not codified anywhere

### Recommended Actions

1. **Add to `core-conventions.md`**: AP-PR-06 (acronyms), AP-PR-07 (industry terms), AP-BR-02 (grammar sacrifice), AP-ST-01 (goal first)
2. **Add to `SKILL.md` or ASANAPAP_RULES.md**: AP-ST-04 (anti-DRY), AP-ST-02 (actionable subjects), AP-ST-05 (hierarchical ordering)
3. **Cross-reference**: Add ASANAPAP reference to existing rule documents that partially implement these rules
4. **Elevate ASANAPAP_RULES.md**: Consider making this a core rule (always-on) since it applies across ALL writing contexts
