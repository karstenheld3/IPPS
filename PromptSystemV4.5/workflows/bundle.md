---
description: Package research sources and transcriptions into a standalone IPPSKBNDL-SP01 knowledge bundle
default_tier: 1 (fixed)
---

# Bundle Workflow

Package research folders, source documents, and transcriptions into a portable, structured knowledge bundle conforming to the IPPS Knowledge Bundle Format (`IPPSKBNDL-SP01`).

**Goal**: `_BUNDLE_[TOPIC].md` or bundle directory conforming to `_SPEC_IPPS_KNOWLEDGE_BUNDLE_FORMAT.md`

**Why**: Packages disparate research documents into a standardized, self-contained format for offline LLM consumption and cross-repository synchronization without performing qualitative coding.

## Required Skills

- @skills:research-methods `RESEARCH_GUIDES.md` (Decision 7: bundle decisions)
- @skills:llm-tools (model call scripts and batch processing)
- Workflow `/transcribe` (PDF and web page transcription)
- Never load CHECKS files during execution (`DRSYNART-FR-32`, `GRUC-IG-03`)

## MUST-NOT-FORGET

- First response line (`DRSYNART-8.1`): output `Tier 1 - fixed format conversion` before any other text
- Tier 1 fixed (`DRSYNART-FR-02`): executes in a single conversation turn producing one bundle output
- Format converter only (`DRSYNART-DD-31`): collects and packages sources; NEVER codes findings (coding belongs to Layer 2 `/pattern-detect`)
- Optional workflow (`DRSYNART-DD-03`): downstream Layers 2-3 operate on C1 Knowledge Libraries directly without requiring `/bundle`
- IPPSKBNDL-SP01 format: format files (`_inventory.md`, `_summary.md`, `_topics.md`, `_metadata.json`) and payload documents
- Locators syntax: enforce standard `path#fragment` locators without custom tags
- Cascade law domain ban: `gesetze-im-internet.de` Playwright only
- Invariant 6: research workflows modify session tracking files (`NOTES.md`, `PROBLEMS.md`, `PROGRESS.md`, `FAILS.md`) only through `/session-save`

## Command Grammar

```text
/bundle [<input>]
```

## Context-Specific Branches

- **Branch 1 (Research Folder Input)**: `<input>` is a research folder (`T##_` or C1 folder). Bundle existing topic files, summaries, and `_SOURCES/` transcriptions.
- **Branch 2 (Source Set Input)**: `<input>` is a list or folder of raw URLs, PDFs, or documents. Transcribe untranscribed assets via `/transcribe` before bundling.

## Steps

1. **Scope and Asset Audit**:
   - Resolve `<input>`: research folder path or source document set.
   - Emit `Tier 1 - fixed format conversion` on first response line.
   - Inspect assets: if untranscribed PDFs or images are present, invoke `/transcribe` pipeline to convert to Markdown with 100% content preservation.
2. **Bundle Packaging**:
   - Assemble bundle components per `_SPEC_IPPS_KNOWLEDGE_BUNDLE_FORMAT.md`:
     - Compile `_inventory.md`: document and child folder lookup list.
     - Compile `_summary.md`: origin, representation, scope, and use prose.
     - Compile `_topics.md`: categorized topic entries with `path#fragment` locators.
     - Generate `_metadata.json`: title, format_version 1.0, created date.
   - Package into standalone bundle file `_BUNDLE_[TOPIC].md` or bundle directory.
3. **Verification**:
   - Confirm zero qualitative coding or thematic synthesis was performed (`DRSYNART-DD-31`).
   - Verify all locators resolve to payload documents.

## Output

- Deliverable: `_BUNDLE_[TOPIC].md` (or bundle directory) in working folder.
- Contains: IPPSKBNDL-SP01 structure with inventory, summary, topics, metadata, and transcribed source files.

## Quality Gate

- [ ] First response line declares `Tier 1 - fixed format conversion`
- [ ] Deliverable conforms to IPPSKBNDL-SP01 format with inventory, summary, topics, and metadata
- [ ] Zero qualitative coding performed (findings remain raw/transcribed for Layer 2)
- [ ] All PDF and image assets transcribed to Markdown with 100% content preservation
- [ ] Zero craft or method knowledge in workflow body; zero CHECKS files loaded; session files modified only through `/session-save`
