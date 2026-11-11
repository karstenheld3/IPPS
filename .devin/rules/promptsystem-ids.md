---
trigger: always_on
---

# Document ID System

All documents and items must have unique IDs for traceability. Full rules, rationale, and examples for every ID type: @skills:promptsystem `PROMPTSYSTEM_IDS.md`.

## Number Formats (2-digit vs 4-digit)

- **2-digit `[NN]` or `[NUMBER]`** - document-scoped items (bounded, rarely exceed 99): document IDs `CRAWLENG-SP01`, review IDs `CRAWLENG-SP01-RV01`, spec items `CRAWLENG-FR-01`, plan items `CRAWLENG-IP01-EC-01`, review findings `CRAWLENG-SP01-RV01-RF-01`
- **4-digit `[NNNN]`** - tracking IDs (unbounded, accumulate over time): `WEBSYSTM-BG-0001`, `AUTHSYST-PR-0001`, `GLOB-FL-0019`

## Topic Registry

- **Topic**: 7-14 uppercase letters describing a component (`CRAWLENG` = Crawler Engine, `AUTHSYST` = Authentication System). Topics created before 2026-06-16 may have 2-6 chars and remain valid; all NEW topics MUST be 7-14 chars. Monorepo: first 2-3 letters = repo prefix (`CRWCORE`, `IXRCORE`)
- **REQUIREMENT**: the workspace must have an `ID-REGISTRY.md` file as the authoritative source for all TOPICs, acronyms, and states. Topic ids must be unique. Entry format with datestamp: `- **[TOPIC]** - Description - YYYY-MM-DD`
- **Before creating a new TOPIC or acronym**: 1) read `ID-REGISTRY.md` to check for existing TOPICs, 2) if new, add it to the `## Project Topics` section with description and datestamp, 3) use the TOPIC consistently across all related documents, 4) never create duplicate or conflicting TOPICs
- **GLOB** is for tracking IDs only (workspace level): `GLOB-BG-*` bugs in the `_bugfixes` session, `GLOB-FL-*` PromptSystem failures, `GLOB-PR-*` cross-cutting problems, `GLOB-TK-*` workspace-wide tasks. Do NOT use `GLOB` for document IDs: if a document has a name, it has a TOPIC (`EDIRDMDL-IN01`, `AUTHSYST-SP01`)

## Document IDs

Every document MUST have an ID in its header block. **Format:** `[TOPIC]-[DOC][NN]`, e.g. `CRAWLENG-SP01`, `CRAWLNXT-IP01`

Document types: `IN` INFO, `SP` SPEC, `IP` Implementation Plan, `TP` Test Plan, `TK` TASKS, `RV` REVIEW, `LN` LEARNINGS. IMPL and TEST replace the overloaded term "plan": IMPL = how to build it, TEST = how to verify it.

## Deliverable Writing Document IDs (OPTIONS, DRAFT, Output)

For documents produced by `/propose-*`, `/draft-*`, and `/write-*`:
- Options proposal: `[TOPIC]-[ID]-OPTIONS-[NN]`, e.g. `MUSICPROMO-KABOB-OPTIONS-01`
- Working draft: `[TOPIC]-[ID]-DRAFT-[NN]`, e.g. `MUSICPROMO-KABOB-DRAFT-01`
- Final publication output: `[TOPIC]-[TYPE]-[NN]`, e.g. `MUSICPROMO-ARTICLE-01`
- `[ID]` = technique ID (`MINTO`, `ABTSTORY`, `KABOB`, etc.) when `using <ID>` is active, else document type. `[TYPE]` = `ARTICLE`, `REPORT`, `EBOOK`. `[NN]` = two-digit sequence counter, continuous per `[ID]` in the working folder

## Nested Document IDs

Documents inside `T##_` (Topic) or `S##_` (Step) session subfolders use nested IDs. **Format:** `[TOPIC]-[SUBTOPIC]-[DOC][NN]`, e.g. `AIDETECT-STYLMTRY-IN01`

- `TOPIC` = session-level or parent topic (registered in `ID-REGISTRY.md`). `SUBTOPIC` = subfolder-specific topic (7-14 chars), registered in session NOTES.md only
- Nesting applies ONLY inside `T##_` or `S##_` folders; session root documents use flat IDs. Max 1 level of nesting
- Flat ID also when the subfolder topic is itself globally unique and registered in `ID-REGISTRY.md`
- Tracking IDs inside nested folders use the nested format: `AIDETECT-STYLMTRY-PR-0001`

## Review Document IDs

**Format:** `[SOURCE-DOC-ID]-RV[NN]`, e.g. `CRAWLENG-IP01-RV02`, nested `AIDETECT-STYLMTRY-IN01-RV01`

## Spec-Level Item IDs (FR, IG, DD)

Defined in SPECs, referenced across IMPL and TEST plans. **Format:** `[TOPIC]-[TYPE]-[NUMBER]`, e.g. `CRAWLENG-FR-01`, `AUTHSYST-IG-02`

Types: `FR` Functional Requirement, `IG` Implementation Guarantee, `DD` Design Decision, `AC` Acceptance Criteria

## Plan-Level Item IDs (EC, IS, VC, TC, TK)

Local to IMPL, TEST, and TASKS plans. Do NOT use in SPECs. **Format:** `[TOPIC]-[DOC][NN]-[TYPE]-[NUMBER]`, e.g. `CRAWLENG-IP01-EC-01`, `AUTHSYST-TP01-TC-03`

Types: `EC` Edge Case, `IS` Implementation Step, `VC` Verification Checklist item, `TC` Test Case, `TK` Task (work item in TASKS document)

## INFO Document Source IDs

All sources in INFO documents MUST have unique IDs. **Format:** `[TOPIC]-[DOC]-SC-[SOURCE_ID]-[SOURCE_REF]`, e.g. `AGNTSKIL-IN01-SC-ASIO-HOME`

`SC` = source type marker, `SOURCE_ID` = website/source mnemonic (2-6 chars), `SOURCE_REF` = page/section identifier (2-12 chars, omit vowels)

## Session Document IDs

Session tracking documents use the session TOPIC ID, so a session folder can be renamed without modifying its files. **Format:** `[TOPIC]-[TYPE]` with type `NOTES`, `PROBLEMS`, or `PROGRESS`, e.g. `AUTHSYST-NOTES`

## Tracking IDs (BG, FT, PR, FX, FL)

For session and project tracking in PROBLEMS.md, FAILS.md, critique/fact-check review files, and backlog documents. **Format:** `[TOPIC]-[TYPE]-[NNNN]` (4-digit number), e.g. `AUTHSYST-FT-0001`, `GLOB-PR-0003`

Types: `BG` Bug (defect in existing code), `FT` Feature (new functionality request), `PR` Problem (issue discovered during session), `FX` Fix (documented fix for a problem), `FL` Failure log entry (actual failure in FAILS.md)

The `[TOPIC]` links together related SPEC, IMPL, TEST, INFO, FAILS, and REVIEW documents.
