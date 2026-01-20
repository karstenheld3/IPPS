# SPEC: TDID Document ID System

**Doc ID (TDID)**: TDID-SP01
**Goal**: Define the Tractful Document ID system ensuring global uniqueness and traceability
**Timeline**: Created 2026-01-20

**Depends on:**
- `SPEC_TRACTFUL_DOCUMENT_FRAMEWORK.md [TRACT-SP01]` for document types

**Does not depend on:**
- `SPEC_EDIRD_PHASE_MODEL.md [EDIRD-SP04]` (TDID is phase-model agnostic)

## MUST-NOT-FORGET

- TOPIC IDs must be registered in ID-REGISTRY.md before use
- Document IDs follow format: `[TOPIC]-[DOC][NN]`
- Item IDs follow format: `[TOPIC]-[TYPE]-[NN]` (spec-level) or `[TOPIC]-[DOC][NN]-[TYPE]-[NN]` (plan-level)
- Cross-references include both filename and TDID: `filename.md [DOC-ID]`

## Table of Contents

1. [Scenario](#1-scenario)
2. [Context](#2-context)
3. [Domain Objects](#3-domain-objects)
4. [ID Formats](#4-id-formats)
5. [Registration Rules](#5-registration-rules)
6. [Functional Requirements](#6-functional-requirements)
7. [Design Decisions](#7-design-decisions)
8. [Implementation Guarantees](#8-implementation-guarantees)
9. [Acceptance Criteria](#9-acceptance-criteria)
10. [Document History](#10-document-history)

## 1. Scenario

**Problem:** Development artifacts lack consistent identification. When referencing requirements, decisions, or test cases across documents, there is no standard format. IDs are invented ad-hoc, leading to collisions and confusion. Finding the source of a reference requires manual search.

**Solution:**
- Define hierarchical ID system: TOPIC → Document → Item
- Require TOPIC registration in central registry
- Enforce consistent ID formats across all document types
- Mandate cross-reference format including filename and ID

**What we don't want:**
- IDs that collide across documents or projects
- Ad-hoc ID formats that vary by author
- References that cannot be resolved
- Registration overhead that discourages usage

## 2. Context

TDID (Tractful Document ID) is the identification subsystem of TRACTFUL. It provides:

- **Global uniqueness** - No two items share the same full ID
- **Traceability** - IDs encode document type and topic
- **Discoverability** - Consistent format enables grep/search
- **Hierarchy** - Document IDs contain topic, item IDs contain document

## 3. Domain Objects

### TOPIC

A **TOPIC** is a 2-6 uppercase letter code identifying a component or concern.

**Examples:**
- `AUTH` - Authentication
- `CRWL` - Crawler
- `EDIRD` - Phase model
- `GLOB` - Global/workspace-wide

**Registration:** ID-REGISTRY.md in workspace root

### Document ID (TDID)

A **Document ID** uniquely identifies a document within the workspace.

**Format:** `[TOPIC]-[DOC][NN]`

**Components:**
- `TOPIC` - Registered topic code (2-6 chars)
- `DOC` - Document type abbreviation (2 chars)
- `NN` - Sequential number (2 digits, 01-99)

**Document Type Abbreviations:**
- `IN` - INFO
- `SP` - SPEC
- `IP` - IMPL (Implementation Plan)
- `TP` - TEST (Test Plan)
- `TK` - TASKS
- `RV` - REVIEW
- `LN` - LEARNINGS

**Examples:**
- `AUTH-SP01` - First AUTH specification
- `CRWL-IP02` - Second CRWL implementation plan
- `GLOB-IN01` - First global info document

### Item ID

An **Item ID** uniquely identifies an item within a document.

**Two levels:**

**Spec-Level** (used in SPEC documents):
- Format: `[TOPIC]-[TYPE]-[NN]`
- Types: FR (Functional Requirement), DD (Design Decision), IG (Implementation Guarantee), AC (Acceptance Criteria)
- Example: `AUTH-FR-01`, `CRWL-DD-03`

**Plan-Level** (used in IMPL, TEST, TASKS documents):
- Format: `[TOPIC]-[DOC][NN]-[TYPE]-[NN]`
- Types: IS (Implementation Step), EC (Edge Case), TC (Test Case), VC (Verification Checklist), TK (Task)
- Example: `AUTH-IP01-IS-05`, `CRWL-TP01-TC-03`

### Cross-Reference

A **Cross-Reference** links to another document or item.

**Document reference format:** `filename.md [DOC-ID]`
- Example: `_SPEC_AUTH.md [AUTH-SP01]`

**Item reference format:** `[FULL-ITEM-ID]`
- Example: `AUTH-FR-01`, `CRWL-IP01-EC-02`

## 4. ID Formats

### Summary Table

```
Level       Format                          Example
─────────────────────────────────────────────────────────────
TOPIC       [A-Z]{2,6}                      AUTH, CRWL, EDIRD
Document    [TOPIC]-[DOC][NN]               AUTH-SP01
Spec-Item   [TOPIC]-[TYPE]-[NN]             AUTH-FR-01
Plan-Item   [TOPIC]-[DOC][NN]-[TYPE]-[NN]   AUTH-IP01-IS-05
Reference   filename.md [DOC-ID]            _SPEC_AUTH.md [AUTH-SP01]
```

### Regex Patterns

```
TOPIC:      ^[A-Z]{2,6}$
Document:   ^[A-Z]{2,6}-(IN|SP|IP|TP|TK|RV|LN)\d{2}$
Spec-Item:  ^[A-Z]{2,6}-(FR|DD|IG|AC)-\d{2}$
Plan-Item:  ^[A-Z]{2,6}-(IN|SP|IP|TP|TK)\d{2}-(IS|EC|TC|VC|TK)-\d{2}$
```

## 5. Registration Rules

### TDID-RR-01: TOPIC Registration

Before using a TOPIC, it must be registered in ID-REGISTRY.md:

```markdown
## Frameworks
- **AUTH** - Authentication and authorization
- **CRWL** - Web crawler component
```

### TDID-RR-02: Uniqueness Check

Before creating a new TOPIC:
1. Search ID-REGISTRY.md for existing TOPIC
2. Search workspace for files using proposed TOPIC
3. If collision found, choose alternative

### TDID-RR-03: Sequential Numbering

Document numbers are sequential within TOPIC+TYPE:
- First AUTH spec: `AUTH-SP01`
- Second AUTH spec: `AUTH-SP02`
- First AUTH impl: `AUTH-IP01` (separate sequence)

### TDID-RR-04: Item Numbering

Item numbers are sequential within document:
- First FR in AUTH-SP01: `AUTH-FR-01`
- Second FR in AUTH-SP01: `AUTH-FR-02`
- First FR in AUTH-SP02: `AUTH-FR-01` (new document, restarts)

## 6. Functional Requirements

**TDID-FR-01: Central Registry**
- ID-REGISTRY.md exists in workspace root
- Contains all registered TOPICs with descriptions
- Searchable by agents and humans

**TDID-FR-02: Document Header**
- Every TRACTFUL document has `Doc ID (TDID)` in header block
- Format: `**Doc ID (TDID)**: [TOPIC]-[DOC][NN]`

**TDID-FR-03: Item Prefixes**
- Items in SPEC use spec-level format
- Items in IMPL/TEST/TASKS use plan-level format
- Bold format: `**[ID]:** description`

**TDID-FR-04: Cross-Reference Format**
- References include filename AND TDID
- Enables both human navigation and agent search
- Example: `See _SPEC_AUTH.md [AUTH-SP01] for requirements`

**TDID-FR-05: Tracking IDs**
- PROBLEMS.md uses: `[TOPIC]-PR-[NNN]`
- FAILS.md uses: `[TOPIC]-FL-[NNN]`
- LEARNINGS.md uses: `[TOPIC]-LN-[NNN]`
- Three-digit numbers for tracking documents

## 7. Design Decisions

**TDID-DD-01:** Two-character document type codes. Rationale: Short enough to not clutter, long enough to be recognizable.

**TDID-DD-02:** Spec-level items omit document number. Rationale: `AUTH-FR-01` is cleaner than `AUTH-SP01-FR-01`. Items are unique within TOPIC scope for specs.

**TDID-DD-03:** Plan-level items include document number. Rationale: Multiple IMPL plans may exist for same TOPIC. `AUTH-IP01-IS-05` vs `AUTH-IP02-IS-05` are distinct.

**TDID-DD-04:** Sequential numbering over UUIDs. Rationale: Human-readable, sortable, predictable. Small number space sufficient for typical documents.

**TDID-DD-05:** Tracking IDs use 3 digits. Rationale: Problems and failures accumulate over project lifetime. 3 digits (001-999) provides adequate range.

## 8. Implementation Guarantees

**TDID-IG-01:** ID-REGISTRY.md always exists in workspace root for TRACTFUL-enabled workspaces.

**TDID-IG-02:** `/verify` workflow checks TDID format compliance in documents.

**TDID-IG-03:** Document templates include Doc ID field with placeholder.

**TDID-IG-04:** Grep patterns in ID-REGISTRY.md enable automated ID discovery.

## 9. Acceptance Criteria

**TDID-AC-01:** Registry exists (verifies: FR-01)
- Test: Check for ID-REGISTRY.md in workspace root
- Pass: File exists with Frameworks section

**TDID-AC-02:** Documents have TDID (verifies: FR-02)
- Test: Grep all SPEC/IMPL/TEST files for `Doc ID (TDID)`
- Pass: All TRACTFUL documents have valid TDID in header

**TDID-AC-03:** Cross-references work (verifies: FR-04)
- Test: Find cross-references, verify target exists
- Pass: All `filename.md [ID]` references resolve

## 10. Document History

**[2026-01-20 19:00]**
- Initial specification created
