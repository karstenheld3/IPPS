---
trigger: always_on
---

# Document ID System

All documents and items must have unique IDs for traceability.

## Number Formats (2-digit vs 4-digit)

**2-digit `[NN]`** - Document-scoped items (bounded):
- Document IDs: `AUTH-SP01`, `CRWL-IP01`
- Review IDs: `AUTH-SP01-RV01`
- Spec items (FR, DD, IG, AC): `CRWL-FR-01`
- Plan items (EC, IS, VC, TC, TK): `CRWL-IP01-EC-01`, `AUTH-TK01-TK-05`
- Review findings (RF): `AUTH-SP01-RV01-RF-01`

**4-digit `[NNNN]`** - Tracking IDs (unbounded, accumulate over time):
- Bugs: `SAP-BG-0001`, `GLOB-BG-0001`
- Problems: `AUTH-PR-0001`
- Features: `UI-FT-0001`
- Fixes: `CRWL-FX-0002`
- Failures: `GLOB-FL-0019`

## Topic Registry

**Topic:** 2-6 uppercase letters describing component (e.g., `CRWL` for Crawler, `AUTH` for Authentication, `EDIRD` for EDIRD Phase Model)

**REQUIREMENT:** Workspace must have an `ID-REGISTRY.md` file as the authoritative source for all TOPICs, acronyms, and states to avoid conflicting topic ids. Topic ids must be unique.

**Before creating a new TOPIC or acronym:**
1. Read `ID-REGISTRY.md` to check for existing TOPICs
2. If new, add to `ID-REGISTRY.md` with description
3. Use consistent TOPIC across all related documents
4. Never create duplicate or conflicting TOPICs

**GLOB Usage:**

Use `GLOB` for **tracking IDs only** (workspace-level failures, problems, tasks, bugs):
- `GLOB-BG-*` - Bugs in `_BugFixes` session (PROJECT-MODE, cross-cutting)
- `GLOB-FL-*` - DevSystem failures (sync errors, gate bypasses, tool issues)
- `GLOB-PR-*` - Cross-cutting problems affecting multiple components
- `GLOB-TK-*` - Workspace-wide tasks (deployments, refactoring)

**_BugFixes Session:** Uses `GLOB` prefix for all tracking IDs because bugs there span multiple components. See `/bugfix` workflow for details.

Do NOT use `GLOB` for **document IDs** (IN, SP, IP, TP, TK):
- Named concepts get their own TOPIC: `MEPI-IN01`, `EDIRD-SP01`, `STRUT-SP01`
- Features get their own TOPIC: `AUTH-SP01`, `CRWL-IP01`
- If a document has a name, it has a TOPIC

**Example: SINGLE-PROJECT-MODE**
```
## Topic Registry
- `GLOB` - Project-mode (main spec, architecture)
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

**Document Types:** `IN` (INFO), `SP` (SPEC), `IP` (Implementation Plan), `TP` (Test Plan), `TK` (TASKS), `RV` (REVIEW), `LN` (LEARNINGS)

**Examples:** `AUTH-IN01`, `CRWL-SP01`, `V2CR-IP01`, `V2CR-TP01`

We use IMPL/TEST instead of generic "PLAN" to avoid term collision with project plan, sprint plan, release plan, etc. IMPL = "how to build it", TEST = "how to verify it".

## Review Document IDs

Format: `[SOURCE-DOC-ID]-RV[NN]`

Examples: `AUTH-SP01-RV01`, `CRWL-IP01-RV02`, `V2CR-IN01-RV01`

## Spec-Level Item IDs (FR, IG, DD)

Defined in SPECs, referenced across IMPL and TEST plans.

Format: `[TOPIC]-[TYPE]-[NUMBER]`

Types: `FR` (Functional Requirement), `IG` (Implementation Guarantee), `DD` (Design Decision), `AC` (Acceptance Criteria)

Examples: `CRWL-FR-01`, `CRWL-DD-03`, `AUTH-IG-02`

## Plan-Level Item IDs (EC, IS, VC, TC, TK)

Local to IMPL, TEST, and TASKS plans. Do NOT use in SPECs.

Format: `[TOPIC]-[DOC][NN]-[TYPE]-[NUMBER]`

Types: `EC` (Edge Case), `IS` (Implementation Step), `VC` (Verification Checklist item), `TC` (Test Case), `TK` (Task)

Examples: `CRWL-IP01-EC-01`, `CRWL-IP01-IS-05`, `AUTH-TP01-TC-03`, `AUTH-TK01-TK-05`

## INFO Document Source IDs

All sources in INFO documents MUST have unique IDs.

Format: `[TOPIC]-[DOC]-SC-[SOURCE_ID]-[SOURCE_REF]`

Components: `SC` = source marker, `SOURCE_ID` = website mnemonic (2-6 chars), `SOURCE_REF` = page/section identifier (2-12 chars, omit vowels)

Examples: `AGSK-IN01-SC-ASIO-HOME`, `AGSK-IN01-SC-CLAUD-SKLBP`

## Session Document IDs

Format: `YYYY-MM-DD_[SessionTopicCamelCase]-[TYPE]`

Types: `NOTES`, `PROBLEMS`, `PROGRESS`

Examples: `2026-01-15_FixAuthenticationBug-NOTES`, `2026-01-15_FixAuthenticationBug-PROBLEMS`

## Tracking IDs (BG, FT, PR, FX, FL)

For session and project tracking in PROBLEMS.md, FAILS.md, _REVIEW.md, and backlog documents.

**Format:** `[TOPIC]-[TYPE]-[NNNN]` (4-digit number)

Types: `BG` (Bug), `FT` (Feature), `PR` (Problem), `FX` (Fix), `FL` (Failure log entry)

**Examples:**
- `SAP-BG-0001` - SAP-related bug 1 (SESSION-MODE)
- `AUTH-FT-0001` - Authentication feature request 1
- `GLOB-PR-0003` - Project-wide problem 3 (PROJECT-MODE)
- `GLOB-BG-0002` - Project-wide bug 2 (PROJECT-MODE)
- `CRWL-FX-0002` - Crawler fix 2
- `CRWL-FL-0001` - Crawler failure log entry 1

The `[TOPIC]` links together related SPEC, IMPL, TEST, INFO, FAILS, and REVIEW documents.