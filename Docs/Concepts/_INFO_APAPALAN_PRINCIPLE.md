# INFO: APAPALAN - As Precise As Possible, As Little As Necessary

**Doc ID**: APAPALAN-IN01
**Goal**: Document the APAPALAN writing principle - its background, the problems it solves, and how its rules implement MECT for practical use
**Timeline**: Created 2026-03-19

## Summary

- **APAPALAN** = "As Precise As Possible (Priority 1), As Little As Necessary (Priority 2)" [VERIFIED]
- APAPALAN implements MECT (Minimal Explicit Consistent Terminology) through concrete, enforceable rules [VERIFIED]
- MECT designs communication systems; APAPALAN applies MECT using rules for documents, code, logs, communication [VERIFIED]
- Precision always wins over brevity - never sacrifice clarity to save words [VERIFIED]
- Readers interpret ALL deviation as intentional signal. Unintentional variance (LLMs) causes wrong assumptions [VERIFIED]
- 26 rules across four categories: Precision (PR), Brevity (BR), Structure (ST), Naming (NM) [VERIFIED]
- Rules are actionable: each has BAD/GOOD examples an agent or human can pattern-match against [VERIFIED]

## Table of Contents

1. [The APAPALAN Principle](#1-the-apapalan-principle)
2. [Why This Matters](#2-why-this-matters)
3. [Hall of Fail](#3-hall-of-fail)
4. [The Rule System](#4-the-rule-system)
5. [Sources](#5-sources)
6. [Document History](#6-document-history)

## 1. The APAPALAN Principle

### 1.1 Definition

**APAPALAN** = As Precise As Possible, As Little As Necessary

Two priorities, in strict order:

1. **Precision** (Priority 1) - Every statement must be unambiguous. A reader must understand exactly what is meant without guessing. Never sacrifice clarity for brevity.
2. **Brevity** (Priority 2) - After precision is guaranteed, remove every unnecessary word. Sacrifice grammar, filler, and repetition. But never sacrifice a word that carries meaning.

The tension between the two priorities is the core challenge. Cryptic abbreviations sacrifice precision for brevity (`P=1` instead of `Precision=1.00`). Verbose writing sacrifices brevity without adding precision ("The system should be configured in such a way that it automatically processes incoming files on a regular basis" instead of "Auto-process incoming files on schedule").

### 1.2 From MECT to APAPALAN

MECT (Minimal Explicit Consistent Terminology) is the underlying philosophy. See `_INFO_MECT_PHILOSOPHY.md [MECT-IN01]` for the full design philosophy.

- **MECT** = Design philosophy for communication systems (the "why" and "what")
- **APAPALAN** = Implementation principle with enforceable rules (the "how")
- **APAPALAN_RULES.md** = The rule set that codifies APAPALAN

Where MECT says "be consistent," APAPALAN provides rule AP-PR-10 with FAIL examples showing what inconsistency does to readers. Where MECT says "be explicit," APAPALAN provides AP-PR-07 with BAD/GOOD pairs for vague vs concrete writing.

### 1.3 The Priority Order

Precision before brevity is not a suggestion - it's a strict ordering. When the two conflict, precision wins every time.

- "Retry 3 times with exponential backoff (1s, 2s, 4s)" is longer than "handle errors appropriately" but infinitely more useful
- `Precision=1.00, F1-Score=1.00` is longer than `P=1, F1=1` but actually communicable
- `_SPEC_CRAWLER.md [CRWL-SP01]` is longer than "the crawler spec" but findable and unambiguous

Brevity only applies AFTER precision is satisfied. Then you cut aggressively: drop articles, filler words, verbose constructions. "The system should automatically process the incoming files on a regular basis" becomes "Auto-process incoming files on schedule." Same precision, half the words.

## 2. Why This Matters

### 2.1 The Mental Model Chain

MECT establishes that words shape mental models which drive actions (see `_INFO_MECT_PHILOSOPHY.md [MECT-IN01]` section 2.3). For APAPALAN, the practical consequence is:

Every formatting choice, structural pattern, and word in a document shapes the reader's mental model. If any of these are ambiguous or inconsistent, the reader builds a wrong model and takes wrong actions - even while feeling confident they understood. This applies equally to:
- A developer reading a spec and implementing the wrong behavior
- An LLM reading a prompt and generating the wrong output
- A manager reading a status report and making the wrong decision

### 2.2 Style Deviation as Unintentional Signal

Readers interpret ALL formatting changes as intentional. If a document uses `- **Key**: Value` for properties and one property suddenly appears as `- Key = Value`, the reader asks: "Why is this different? Is this property special? Is it from a different source? Is it less important?"

If the deviation was unintentional - the writer just varied their style - the reader's questions lead to wrong assumptions. They might skip the property, treat it as metadata, or assume it's a different category of information.

This problem is amplified with LLMs. LLMs have natural output variance - they don't reproduce the same formatting consistently across long outputs. Every unintentional style change becomes a false signal to the reader. APAPALAN rule AP-PR-10 (Consistent Patterns) exists specifically to counter this.

### 2.3 The Compounding Cost of Inconsistency

MECT established that terminology debt compounds over time (see MECT-IN01 section 1.2). APAPALAN extends this to formatting and structure:

Fixing inconsistent formatting costs minutes. NOT fixing it compounds:
- Reader misinterprets a requirement because the style change seemed intentional
- Developer implements wrong behavior based on the misinterpretation
- Bug discovered weeks later, root cause traced to ambiguous spec
- Fix requires changing code, tests, documentation, and the original spec

The earlier you enforce consistent patterns, the cheaper the total cost.

## 3. Hall of Fail

Each fail shows the inconsistent writing, the misleading question it triggers in the reader, and the wrong assumption the reader makes.

### 3.1 Precision Fails

**FAIL: Vague requirements**
```
The system handles errors appropriately.
Performance should be acceptable.
```
- Reader asks: "What does 'appropriately' mean? What is 'acceptable'?"
- Wrong assumption: Developer implements whatever they think is appropriate. Different developers implement different behaviors. No way to test against the spec because the spec says nothing testable.

**FAIL: Missing identifiers**
```
- Toast notifications should support info, success, error types
- We decided to use localStorage
- There's a race condition in the auth flow
```
- Reader asks: Nothing - reader can't reference these items in other documents, reviews, or conversations.
- Wrong assumption: Items get discussed as "that toast thing" and "the localStorage decision." Two months later, nobody can find or trace these decisions.

**FAIL: Unreferenceable content**
```
See the crawler spec for requirements.
As discussed, please proceed with option 2.
As mentioned above...
```
- Reader asks: "Which crawler spec? Which option 2? Where above?"
- Wrong assumption: Reader searches, finds wrong document or wrong option, proceeds with wrong plan.

**FAIL: Ambiguous date formats**
```
Meeting scheduled for 10/11/2026
```
- Reader asks: "October 11 or November 10?"
- Wrong assumption: Half the team shows up on the wrong date. ISO format `2026-10-11` eliminates ambiguity.

**FAIL: Misleading naming in code**
```python
def nextTo(element):  # What context? Direction? Distance?
obj.visible = False   # Still occupies space, or gone entirely?
planes_with_target = "Bagdad"  # Military strike or travel plans?
```
- Reader asks: "Is `nextTo` about direction, distance, or relationship? Does `visible=False` mean hidden or removed?"
- Wrong assumption: Developer uses `nextTo` for spatial proximity when it meant logical sequence. "target" implies attack when "destination" was meant.

### 3.2 Brevity Fails

**FAIL: Cryptic abbreviations**
```
P=1, F1=1, R=0.95
```
- Reader asks: "What is P? Precision? Probability? Priority? Is F1 the F1-Score or Field 1?"
- Wrong assumption: Reader guesses wrong meaning. Reports wrong metric to stakeholder.

**FAIL: Over-compressed instructions**
```
Fix auth, deploy, notify.
```
- Reader asks: "Fix what in auth? Deploy where? Notify whom?"
- Wrong assumption: Developer fixes the wrong auth issue, deploys to wrong environment, notifies wrong team.

### 3.3 Structure Fails

**FAIL: Missing goal**
```
# Verify Workflow

## Required Skills
...

## Steps
1. Read documents
2. Check rules
```
- Reader asks: "What is this workflow supposed to achieve? How do I know if I've succeeded?"
- Wrong assumption: Reader mechanically follows steps without understanding purpose. Misses issues that fall outside the literal steps but within the spirit of the workflow.

**FAIL: Style variance signals wrong meaning**
```
## Server Config
- **Region**: eu-west-1
- **Type**: m5.xlarge

## Database Config
- Region = us-east-1
- Type = db.r5.large
```
- Reader asks: "Are these different systems? Does `=` mean something different from `:`?"
- Wrong assumption: Reader treats Database Config as environment variables (because `=` looks like env var syntax). Actually, same format - the writer just switched style.

**FAIL: Bold used inconsistently**
```
- **Name**: John Smith
- Email: john@example.com
- **Phone**: +1 555 1234
```
- Reader asks: "Is bold marking required fields? Is Email optional?"
- Wrong assumption: Reader skips Email thinking it's optional. Actually, all fields are required - the writer just forgot to bold Email.

### 3.4 Communication Fails

**FAIL: Implicit style convention**
```
- Name [required]
- Email (optional)
- Phone [required]
```
- Reader asks: Nothing - reader doesn't know `[brackets]` means required.
- Wrong assumption: Reader treats all fields equally. Skips Phone. System fails at validation.

**FAIL: Incomplete delegation**
```
Please update the config for the new server.
```
- Reader asks: "Which config file? Which server? What values? What's the expected outcome?"
- Wrong assumption: Reader updates the wrong config or the wrong values. Hours wasted on rollback.

**FAIL: Mixed instruction granularity**
```
1. Clone the repository
2. Set up the development environment with all necessary dependencies,
   configure the database connection, and run the migration scripts
3. Run tests
```
- Reader asks: "Step 2 is three steps in one. Are they all equally important? What order?"
- Wrong assumption: Reader skips database config, runs migrations against wrong database, tests fail with cryptic errors.

## 4. The Rule System

APAPALAN rules are organized in three categories matching the priority order.

### 4.1 Precision (PR): Making Every Statement Unambiguous

9 rules ensuring every piece of writing can be understood without guessing.

- **AP-PR-01**: Standardized datetime format - `YYYY-MM-DD HH:MM` everywhere
- **AP-PR-02**: Standardized attribute/property format - context-specific but consistent within context
- **AP-PR-03**: Standardized contact information format - structured blocks with all fields
- **AP-PR-04**: Standardized link and reference format - depends on AP-PR-05; three steps: define ID system, apply IDs, use IDs to reference
- **AP-PR-05**: Referenceable IDs on all trackable items - prerequisite for AP-PR-04; you cannot reference what has no ID
- **AP-PR-06**: Write out acronyms on first use - `Full Term (ACRONYM)` format
- **AP-PR-07**: Be specific - no generic or abstract writing; concrete, verifiable statements
- **AP-PR-08**: Every non-obvious rule needs examples - BAD/GOOD pairs for format rules and conventions
- **AP-PR-09**: Consistent patterns - repeat established structures; style deviation = false signal

The referenceability chain (AP-PR-05 -> AP-PR-04) deserves emphasis: you cannot build a useful reference system unless the referenced information has IDs in the first place. Create IDs first, then reference.

### 4.2 Brevity (BR): Removing Without Losing

6 rules for cutting words after precision is secured.

- **AP-BR-01**: Single line for single statements - if it fits on one line, keep it on one line
- **AP-BR-02**: Sacrifice grammar for brevity - drop articles, filler words, verbose constructions (exception: user-facing text preserves full grammar)
- **AP-BR-03**: DRY within same document scope - reference instead of restating (overridden by AP-ST-04 for delegation)
- **AP-BR-04**: Compact object and list definitions - lists, no empty lines between properties
- **AP-BR-05**: Show format over describing format - a format example communicates more precisely than a description
- **AP-BR-06**: Pipe-delimited property lines - `Key: Value | Key: Value` for multi-attribute items

### 4.3 Structure (ST): Organizing for the Reader

6 rules for organizing content so readers find what they need.

- **AP-ST-01**: Goal or intention captured first - reader knows WHY before HOW
- **AP-ST-02**: Subjects direct and actionable - "ACTION: Review contract by 2026-03-20" not "Meeting"
- **AP-ST-03**: Self-contained units - each section, log line, email understandable without external context
- **AP-ST-04**: Anti-DRY for delegation - when requesting action from others, inline ALL needed information (overrides AP-BR-03 because the audience is different)
- **AP-ST-05**: Hierarchical information ordering - general to specific, most important first
- **AP-ST-06**: Visual thought grouping - related content clusters together (no empty lines); distinct thoughts separate by one empty line

The DRY tension (AP-BR-03 vs AP-ST-04) is intentional: within your own document, reference instead of repeating. But when delegating to someone else, inline everything because people don't follow references.

### 4.4 Naming (NM): One Name, One Meaning

5 rules for naming things consistently across documents, code, logs, and communication. Derived from MECT terminology problems.

- **AP-NM-01**: One name per concept - no synonyms (search failures), no polysemy (silent misunderstandings)
- **AP-NM-02**: Unambiguous compound names - word order determines meaning (`KeyOfEmptyCollection` not `EmptyCollectionKey`)
- **AP-NM-03**: Avoid dangerous meta-words - Module, Service, Check, etc. hide ambiguity; qualify them
- **AP-NM-04**: Intuitive word pairs - opposites must be predictable (`Encode/Decode` not `Encode/PlainText`)
- **AP-NM-05**: Use and keep standard terms - established terminology; don't rename (association field principle)

## 5. Sources

**Primary Sources:**
- `APAPALAN-IN01-SC-MECT-IN01`: `_INFO_MECT_PHILOSOPHY.md [MECT-IN01]` - MECT communication design philosophy [VERIFIED]
- `APAPALAN-IN01-SC-APAP-RULES`: `APAPALAN_RULES.md` in DevSystemV3.5/skills/write-documents/ - Full rule set with BAD/GOOD examples [VERIFIED]

**Related Documents:**
- `APAPALAN-IN01-SC-DSYS-IDS`: `devsystem-ids.md` - ID system referenced by AP-PR-04 and AP-PR-05 [VERIFIED]
- `APAPALAN-IN01-SC-LOG-RULES`: `LOGGING-RULES.md` in DevSystemV3.5/skills/coding-conventions/ - Logging rules implementing APAPALAN for output [VERIFIED]

## 6. Document History

**[2026-03-19 21:14]**
- Moved: AP-PR-09 (Pipe-delimited) -> AP-BR-06 (brevity rule, not precision)
- Changed: Renumbered PR-10 -> PR-09. PR count 10 -> 9, BR count 5 -> 6

**[2026-03-19 21:13]**
- Changed: Consolidated AP-PR-07 (Use Standard Industry Terms) into AP-NM-05 (Use and Keep Standard Terms)
- Changed: Renumbered PR-08..PR-11 -> PR-07..PR-10. Rule count 27 -> 26

**[2026-03-19 21:09]**
- Added: Naming (NM) category with 5 rules (AP-NM-01 through AP-NM-05)
- Changed: Rule count 22 -> 27, three -> four categories

**[2026-03-19 21:01]**
- Added: "Misleading naming in code" fail example (nextTo, visible/hidden, target/destination)

**[2026-03-19 20:48]**
- Fixed: Removed mental model chain re-explanation (H1) - reference MECT instead
- Fixed: Removed compounding cost re-explanation (H2) - reference MECT, focus on formatting angle
- Fixed: Replaced MECT-specific fails (vague delegation, academic language) with APAPALAN-specific fails (incomplete delegation, mixed instruction granularity)
- Fixed: Shortened MECT re-explanation in section 1.2 (M1)
- Fixed: Dropped MECT parenthetical from date format fail (M2)
- Fixed: Updated stale filename `_INFO_MECT_PRINCIPLE.md` -> `_INFO_MECT_PHILOSOPHY.md` (L1)

**[2026-03-19 20:44]**
- Initial document created
- Structure: Principle definition, Why it matters, Hall of Fail, Rule system overview
- Fails sourced from MECT-IN01 and APAPALAN_RULES.md
