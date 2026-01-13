# Document ID System

All documents and items must have unique IDs for traceability.

## Topic Registry

**Topic:** 2-5 uppercase letters describing component (e.g., `CRWL` for Crawler, `AUTH` for Authentication)

**REQUIREMENT:** Workspace/project-level NOTES.md MUST maintain a complete list of registered TOPIC IDs.

Before using a new TOPIC ID:
1. Check workspace/project NOTES.md for existing TOPIC IDs
2. If new, add to NOTES.md Topic Registry section
3. Use consistent TOPIC across all related documents

**Example: SINGLE-PROJECT**
```
## Topic Registry
- `GLOB` - Project-wide (main spec, architecture)
- `V1CR` - Version 1 Crawler
- `V2CR` - Version 2 Crawler
- `CUIF` - Common UI Functions
- `CSPF` - Common SharePoint Functions
```

**Example: MONOREPO** (first 2 letters = repo prefix)
```
## Topic Registry
- `CRCORE` - CR: Crawler Core (shared libraries)
- `CRAPI` - CR: Crawler API (REST endpoints)
- `CRUI` - CR: Crawler UI (frontend)
- `IXCORE` - IX: Indexer Core (indexing engine)
- `IXSCHED` - IX: Indexer Scheduler (job scheduling)
```

## Document IDs

Every document MUST have an ID in its header block.

**Format:** `[TOPIC]-[DOC][NN]`

**Document Types:**
- `IN` - INFO document
- `SP` - SPEC document
- `IP` - Implementation Plan
- `TP` - Test Plan

**Examples:**
- `AUTH-IN01` - Authentication Info doc 1
- `CRWL-SP01` - Crawler Spec 1
- `V2CR-IP01` - V2 Crawler Implementation Plan 1
- `V2CR-TP01` - V2 Crawler Test Plan 1

## Spec-Level Item IDs (FR, IG, DD)

Defined in SPECs, referenced across IMPL and TEST plans.

**Format:** `[TOPIC]-[TYPE]-[NUMBER]`

**Types:**
- `FR` - Functional Requirement
- `IG` - Implementation Guarantee
- `DD` - Design Decision

**Examples:**
- `CRWL-FR-01` - Crawler Functional Requirement 1
- `CRWL-DD-03` - Crawler Design Decision 3
- `AUTH-IG-02` - Authentication Implementation Guarantee 2

## Plan-Level Item IDs (EC, IS, VC, TC)

Local to IMPL and TEST plans. Do NOT use in SPECs.

**Format:** `[TOPIC]-[DOC][NN]-[TYPE]-[NUMBER]`

**Types:**
- `EC` - Edge Case
- `IS` - Implementation Step
- `VC` - Verification Checklist item
- `TC` - Test Case

**Examples:**
- `CRWL-IP01-EC-01` - Crawler Plan 01, Edge Case 1
- `CRWL-IP01-IS-05` - Crawler Plan 01, Implementation Step 5
- `AUTH-TP01-TC-03` - Authentication Test Plan 01, Test Case 3

## INFO Document Source IDs

All sources in INFO documents MUST have unique IDs.

**Format:** `[TOPIC]-[DOC]-SC-[SOURCE_ID]-[SOURCE_REF]`

**Components:**
- `SC` - Source type marker
- `SOURCE_ID` - Website/source mnemonic (2-6 chars)
- `SOURCE_REF` - Page/section identifier (2-12 chars, omit vowels)

**Examples:**
- `AGSK-IN01-SC-ASIO-HOME` - agentskills.io/home
- `AGSK-IN01-SC-CLAUD-SKLBP` - platform.claude.com/.../best-practices

## Tracking IDs (PR, FX)

For session and project tracking in PROBLEMS.md and FIXES documents.

**Format:** `[TOPIC]-[TYPE]-[NUMBER]`

**Types:**
- `PR` - Problem (tracked in PROBLEMS.md)
- `FX` - Fix (tracked in IMPL_*_FIXES.md)

**Examples:**
- `SAP-PR-01` - SAP-related problem 1
- `SCHD-FX-01` - Damage module fix 1
- `PRXL-PR-03` - Project-wide problem 3
