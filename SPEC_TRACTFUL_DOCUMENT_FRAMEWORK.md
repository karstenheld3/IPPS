# SPEC: TRACTFUL Document Framework

**Doc ID (TDID)**: TRACT-SP01
**Goal**: Define document framework ensuring development lifecycle traceability from ideation to maintenance
**Timeline**: Created 2026-01-20

**Depends on:**
- `SPEC_AGEN_AGENTIC_ENGLISH.md [AGEN-SP01]` for controlled vocabulary
- `ID-REGISTRY.md` for TOPIC registration

**Does not depend on:**
- `SPEC_EDIRD_PHASE_MODEL.md [EDIRD-SP04]` (TRACTFUL is phase-model agnostic)

## MUST-NOT-FORGET

- Every document MUST have a TDID (Tractful Document ID)
- Cross-references use format: `filename.md [DOC-ID]`
- Document History section required at end, reverse chronological
- Sync documents when implementation deviates from plan

## Table of Contents

1. [Scenario](#1-scenario)
2. [Context](#2-context)
3. [Domain Objects](#3-domain-objects)
4. [ID System (TDID)](#4-id-system-tdid)
5. [Document Types](#5-document-types)
6. [Document Lifecycle](#6-document-lifecycle)
7. [Traceability Rules](#7-traceability-rules)
8. [Functional Requirements](#8-functional-requirements)
9. [Design Decisions](#9-design-decisions)
10. [Implementation Guarantees](#10-implementation-guarantees)
11. [Acceptance Criteria](#11-acceptance-criteria)
12. [Document History](#12-document-history)

## 1. Scenario

**Problem:** Development artifacts become disconnected over time. Initial requirements drift from implementation. Decisions made during development are lost. When revisiting code months later, the reasoning behind choices is unclear. Bug fixes and refactoring happen without updating upstream documents.

**Solution:**
- Define document types covering entire lifecycle (ideation to maintenance)
- Require unique IDs for all documents and items within documents
- Enforce cross-referencing between related documents
- Mandate sync workflows when implementation deviates from plan
- Provide templates ensuring consistent structure

**What we don't want:**
- Documents that exist but are never read or updated
- Implementation that diverges silently from specification
- Duplicate or conflicting information across documents
- IDs that collide or are reused incorrectly
- Heavy documentation overhead that discourages usage

## 2. Context

TRACTFUL (Traceable Requirements Artifacts and Coded Templates For Unified Lifecycle) provides the document framework for agent-assisted development. It works alongside:

- **AGEN** - Controlled vocabulary for document content
- **TDID** - ID system for document and item references (defined in this spec)
- **EDIRD** (or alternative) - Phase model that sequences document creation

TRACTFUL is phase-model agnostic. Documents can be created in any order, though typical flow follows ideation-to-implementation pattern.

## 3. Domain Objects

### Document

A **Document** is a Markdown file with structured content following a TRACTFUL template.

**Key properties:**
- `TDID` - Unique identifier (required)
- `Type` - One of the defined document types
- `Goal` - Single sentence purpose statement
- `Dependencies` - References to other documents
- `History` - Chronological change log

### Item

An **Item** is a numbered element within a document (requirement, decision, test case).

**Key properties:**
- `Item ID` - Unique within document scope (e.g., FR-01, DD-03)
- `Full ID` - TOPIC-TYPE-NN format (e.g., AUTH-FR-01)
- `Description` - What the item defines or requires
- `References` - Links to related items in other documents

### Traceability Link

A **Traceability Link** connects items across documents.

**Types:**
- `implements` - Code/IMPL item implements SPEC item
- `verifies` - TEST item verifies SPEC/IMPL item
- `derives-from` - Item is derived from another item
- `supersedes` - Item replaces a previous item

## 4. ID System (TDID)

TDID (Tractful Document ID) ensures every document and item is uniquely identifiable and referencable.

### 4.1 TOPIC Registration

A **TOPIC** is a 2-6 uppercase letter code identifying a component or concern.

**Examples:** `AUTH`, `CRWL`, `EDIRD`, `GLOB`

**Rule:** Before using a TOPIC, register it in `ID-REGISTRY.md` in workspace root.

### 4.2 Document IDs

**Format:** `[TOPIC]-[DOC][NN]`

**Components:**
- `TOPIC` - Registered topic code (2-6 chars)
- `DOC` - Document type (IN, SP, IP, TP, TK, RV, LN)
- `NN` - Sequential number (01-99)

**Document Type Codes:**
- `IN` - INFO
- `SP` - SPEC
- `IP` - IMPL (Implementation Plan)
- `TP` - TEST (Test Plan)
- `TK` - TASKS
- `RV` - REVIEW
- `LN` - LEARNINGS

**Examples:** `AUTH-SP01`, `CRWL-IP02`, `GLOB-IN01`

### 4.3 Item IDs

Every major item within a document has a unique ID.

**Spec-Level Items** (in SPEC documents):
- Format: `[TOPIC]-[TYPE]-[NN]`
- Types: FR (Functional Requirement), DD (Design Decision), IG (Implementation Guarantee), AC (Acceptance Criteria)
- Examples: `AUTH-FR-01`, `CRWL-DD-03`, `TRACT-AC-02`

**Plan-Level Items** (in IMPL, TEST, TASKS documents):
- Format: `[TOPIC]-[DOC][NN]-[TYPE]-[NN]`
- Types: IS (Implementation Step), EC (Edge Case), TC (Test Case), VC (Verification Checklist), TK (Task)
- Examples: `AUTH-IP01-IS-05`, `CRWL-TP01-TC-03`, `AUTH-TK01-TK-001`

**Tracking Items** (in PROBLEMS, FAILS, LEARNINGS):
- Format: `[TOPIC]-[TYPE]-[NNN]` (3-digit)
- Types: PR (Problem), FL (Failure Log), LN (Learning), BG (Bug), FT (Feature)
- Examples: `STRUT-PR-005`, `AUTH-FL-001`

### 4.4 Cross-Reference Format

**Document reference:** `filename.md [DOC-ID]`
- Example: `_SPEC_AUTH.md [AUTH-SP01]`

**Item reference:** `[FULL-ITEM-ID]`
- Example: `AUTH-FR-01`, `CRWL-IP01-EC-02`

### 4.5 ID Regex Patterns

```
TOPIC:      ^[A-Z]{2,6}$
Document:   ^[A-Z]{2,6}-(IN|SP|IP|TP|TK|RV|LN)\d{2}$
Spec-Item:  ^[A-Z]{2,6}-(FR|DD|IG|AC)-\d{2}$
Plan-Item:  ^[A-Z]{2,6}-(IN|SP|IP|TP|TK)\d{2}-(IS|EC|TC|VC|TK)-\d{2,3}$
Tracking:   ^[A-Z]{2,6}-(PR|FL|LN|BG|FT)-\d{3}$
```

## 5. Document Types

### Research Documents

- **INFO** - Research findings, options analysis, background context
  - Template: `INFO_TEMPLATE.md`
  - Naming: `_INFO_[TOPIC].md`
  - Contains: Sources, findings, recommendations

### Specification Documents

- **SPEC** - Technical specification defining what to build
  - Template: `SPEC_TEMPLATE.md`
  - Naming: `_SPEC_[COMPONENT].md` or `SPEC_[COMPONENT].md`
  - Contains: FR (Functional Requirements), DD (Design Decisions), IG (Implementation Guarantees), AC (Acceptance Criteria)

### Planning Documents

- **IMPL** - Implementation plan defining how to build
  - Template: `IMPL_TEMPLATE.md`
  - Naming: `_IMPL_[COMPONENT].md`
  - Contains: IS (Implementation Steps), EC (Edge Cases), VC (Verification Checklist)

- **TEST** - Test plan defining how to verify
  - Template: `TEST_TEMPLATE.md`
  - Naming: `_TEST_[COMPONENT].md`
  - Contains: TC (Test Cases), test data, coverage requirements

- **TASKS** - Partitioned work items with estimates
  - Template: `TASKS_TEMPLATE.md`
  - Naming: `TASKS_[TOPIC].md`
  - Contains: TK (Tasks) with dependencies, estimates, verification commands

### Execution Documents

- **FIXES** - Code changes log for release documentation
  - Template: `FIXES_TEMPLATE.md`
  - Naming: `_IMPL_[COMPONENT]_FIXES.md`
  - Contains: Bug fixes, features, refactoring changes

### Learning Documents

- **FAILS** - Failure log capturing mistakes and lessons
  - Template: `FAILS_TEMPLATE.md`
  - Naming: `FAILS.md`
  - Contains: FL (Failure Log entries) with severity, resolution

- **LEARNINGS** - Retrospective analysis of resolved problems
  - Template: `LEARNINGS_TEMPLATE.md`
  - Naming: `LEARNINGS.md`
  - Contains: LN (Learning entries) with root cause analysis

### Review Documents

- **REVIEW** - Potential issues and improvement suggestions
  - Template: `REVIEW_TEMPLATE.md`
  - Naming: `_REVIEW.md` or `[SOURCE]-RV[NN].md`
  - Contains: RV (Review findings) categorized by priority

## 6. Document Lifecycle

```
[WRITE-INFO] research and analysis
├─> INFO documents created
│
[WRITE-SPEC] define requirements
├─> SPEC with FR, DD, IG, AC items
│
[WRITE-IMPL-PLAN] define implementation approach
[WRITE-TEST-PLAN] define verification approach
├─> IMPL and TEST documents
│
[PARTITION] create TASKS from IMPL/TEST
├─> TASKS document with work items
│
[IMPLEMENT] execute tasks
├─> Code changes tracked in FIXES
│
[TEST] verify implementation
├─> TC results recorded
│
[VERIFY] SPECs and IMPL plans against rules
[CRITIQUE] SPECs and IMPL plans for logic flaws
├─> REVIEW document with findings
│
[FAIL] record failures when they occur
[LEARN] analyze resolved problems
├─> FAILS and LEARNINGS documents
│
[SYNC] update documents when implementation changes
```

## 7. Traceability Rules

### TRACT-TR-01: Forward Traceability

Every SPEC item (FR, DD, IG) must trace forward to:
- At least one IMPL step (IS) or explicit skip justification
- At least one TEST case (TC) or explicit untestable justification

### TRACT-TR-02: Backward Traceability

Every IMPL step must trace backward to:
- At least one SPEC item (FR, DD, or IG)
- Or explicit rationale for implementation-driven addition

### TRACT-TR-03: Sync on Deviation

When implementation deviates from SPEC or IMPL:
- Run `/sync` workflow to update upstream documents
- Add DD entry explaining deviation rationale
- Update affected TC if behavior changed

### TRACT-TR-04: Acceptance Verification

SPEC is considered implemented when:
- All AC items pass verification
- All IG items are proven (via test or inspection)
- No open REVIEW findings at CRITICAL or HIGH severity

## 8. Functional Requirements

**TRACT-FR-01: Document Templates**
- Each document type has a corresponding template
- Templates define required sections and item ID formats
- Templates are versioned and tracked in write-documents skill

**TRACT-FR-02: Unique Identification**
- Every document has a TDID in header block
- Every item has a unique ID within its document
- Full item IDs include TOPIC prefix for global uniqueness

**TRACT-FR-03: Cross-Reference Format**
- Format: `filename.md [DOC-ID]`
- Example: `_SPEC_AUTH.md [AUTH-SP01]`
- Item references: `AUTH-FR-01`, `AUTH-SP01-TC-03`

**TRACT-FR-04: Document History**
- Every document ends with Document History section
- Entries in reverse chronological order
- Format: `**[YYYY-MM-DD HH:MM]**` followed by change list

**TRACT-FR-05: Dependency Declaration**
- Documents declare dependencies in header block
- Optional: explicit non-dependencies to prevent confusion

**TRACT-FR-06: Sync Workflow**
- `/sync` workflow propagates changes across related documents
- Direction: Code→IMPL→SPEC or SPEC→IMPL→TEST
- Labels updated: [ASSUMED]→[VERIFIED]→[TESTED]→[PROVEN]

## 9. Design Decisions

**TRACT-DD-01:** Phase-model agnostic. TRACTFUL defines document types and traceability, not the order of creation. Any phase model (EDIRD or alternative) can use TRACTFUL documents.

**TRACT-DD-02:** Templates over conventions. Explicit templates with required sections are easier for agents to follow than implicit conventions.

**TRACT-DD-03:** ID system is integral. TDID (Tractful Document ID) is defined within TRACTFUL spec (section 4) as it is core to traceability.

**TRACT-DD-04:** Lightweight sync over heavyweight process. Documents should be easy to update. Sync is encouraged but not blocking.

**TRACT-DD-05:** Learning documents are optional. FAILS.md and LEARNINGS.md capture lessons but are not required for every project.

## 10. Implementation Guarantees

**TRACT-IG-01:** Every template exists in `write-documents` skill folder with corresponding verb mapping.

**TRACT-IG-02:** ID-REGISTRY.md in workspace root contains all registered TOPICs and prevents ID collisions.

**TRACT-IG-03:** `/verify` workflow checks document structure against template requirements.

**TRACT-IG-04:** Document History section is always at document end (before any appendices).

## 11. Acceptance Criteria

**TRACT-AC-01:** Template coverage (verifies: FR-01)
- Test: List all document types, verify each has template
- Pass: All 9 document types have templates in write-documents skill

**TRACT-AC-02:** Cross-reference works (verifies: FR-03)
- Test: Create two documents with cross-references, verify links
- Pass: References resolve correctly in agent context

**TRACT-AC-03:** Sync workflow exists (verifies: FR-06)
- Test: Run `/sync` after code change
- Pass: Upstream documents updated with change evidence

## 12. Document History

**[2026-01-20 19:12]**
- Changed: Document Types subsections renamed from "X Phase" to "X Documents" (phase-agnostic)
- Changed: Document Lifecycle now shows verbs and document outputs, not phases
- Changed: Review section clarifies we review SPECs and IMPL plans

**[2026-01-20 19:10]**
- Added: Section 4 - ID System (TDID) with TOPIC registration, document IDs, item IDs, cross-references, regex patterns
- Changed: TDID is now part of TRACTFUL spec, not separate

**[2026-01-20 18:57]**
- Initial specification created
