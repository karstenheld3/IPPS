# SPEC: IPPS Knowledge Bundle Format

**Doc ID**: IPPSKBNDL-SP01
**Feature**: knowledge-bundle-format
**Goal**: Define a folder-and-document format that LLM-based agents can search, read, and update with minimal effort - progressive disclosure, structured extraction, composability, two storage variants, and generated files that stay in sync under bulk inserts, removals, and small edits
**Timeline**: Created 2026-09-15, Updated 24 times (2026-09-15 - 2026-09-15)

**Does not depend on:**
- Any implementation code (this is a format specification, not a software spec)
- Any specific chunking, embedding, or indexing scheme of a search technology

## MUST-NOT-FORGET

- This is a general-purpose format spec - ALL examples use generic content, no real project names or paths
- Two concepts only: **Folder** and **Document**. No Part, Section, Chapter, or Page as format concepts
- A Folder is a Knowledge Bundle iff it contains `_inventory.md`. Every such folder MUST also contain `_summary.md` and `_topics.md` - root included. Self-similar: every bundle folder has the same three files. Composability: bundles contain bundles contain bundles; moving a bundle into another bundle touches only the receiving folder's `_inventory.md`, `_summary.md`, `_topics.md`
- `_inventory.md` is a pure lookup: title plus one line per direct child folder and document (`- \`name\` - purpose`). No metadata lines, no format files, no derived files. Cost of any document or folder change: exactly one line
- `_summary.md` is the cover card: title plus prose on origin, what the material represents, scope, and use. No volatile facts (counts, latest dates, names, values) - those live in `_inventory.md`, `_topics.md`, `_metadata.json`. Regenerated only when a child folder is added or removed or `_metadata.json` scope fields change; never on document changes; never from documents
- A Document is any content file in a folder: transcribed book page, scanned letter, wiki article, blog post, factsheet, price series CSV. The format never modifies documents
- `_topics.md` in a folder that holds documents is LLM-extracted. `_topics.md` in a folder that holds only folders is a mechanical merge (code, no model call) of the direct children's `_topics.md`, each locator prefixed with the child folder name
- `_` prefix and `.data.md` suffix = format files expected by agents; everything else is payload
- Asset folders use self-explaining names: `_images/`, `_svg/`, `_fonts/`, `_audio/`. Never meta-words like `_assets/` or `_files/` - agents derive nothing from them
- Documents of native origin keep their relative assets where they reference them
- Progressive disclosure is the core design principle: agent finds `_summary.md` and `_topics.md` via search, navigates with `_inventory.md`, goes deeper on demand
- Single vector store: all `_summary.md` and `_topics.md` files in one index - no separate tier indices
- On-demand retrieval: `.data.md`, documents, assets - NOT in vector store, retrieved after search identifies the target
- `_topics.md` and `.data.md` are plain markdown: headings, list items, fenced code blocks. No custom tag syntax
- One locator syntax everywhere: `path#fragment` - `#heading-slug`, `#L12-L40`, `#L12C5-L40C80`, `#page=47`, `#t=00:12:30`, `#cell=B2:D14`
- No size, length, word-count, or attribute-count constraints on `_inventory.md` or `_summary.md`. Larger context windows and better search will shift what is optimal; the format only fixes the bare minimum
- Ordering prefixes (`NN_`, `YYYY-MM-DD_`) are SHOULD, never MUST. Any sort scheme that yields the intended order is valid
- Two storage variants only: folder on disk, and .zip archive on disk
- Minimal design: no derived aggregates in `_metadata.json`; structural data lives in `_inventory.md` at the folder that owns the children
- Agent-editable: every generated file except `_summary.md` is line-oriented (one child, entry, or locator per line) and scoped to its own folder. Adding or removing N documents touches N inventory lines and N locator sets, zero summary regenerations. Update cost per scenario in Key Mechanisms
- No model work beyond the parent: a folder change touches one line in `P/_inventory.md` and regenerates `P/_summary.md` once from three small files. Siblings are never touched. Merged `_topics.md` files from P up to the root are rebuilt by code, never by a model
- Process independence: the format defines structure and generated files only. How a bundle is produced (tools, models, settings, cost, quality scores, logs) and what material it holds is the user's decision and is not part of the format. No provenance file, no process records, no transcription parameters
- No document history chapter

## One-Page Summary

Self-contained format card. Copy it into any prompt or README; it is all an agent needs to read or maintain a bundle.

````text
IPPS KNOWLEDGE BUNDLE - FORMAT CARD (format_version 1.0)

WHAT: A folder tree that LLM agents search, read, and update with minimal effort. Two concepts:
  Folder    groups documents or folders. A folder containing _inventory.md is a Knowledge Bundle.
            Bundles nest to any depth; every nested bundle is complete on its own.
  Document  any content file (page, letter, article, CSV, transcript, source file). Never modified.

FORMAT FILES (names with `_` prefix or `.data.md` suffix; everything else is payload):
  _inventory.md   REQUIRED in every bundle folder. "# Title", then one line per direct child:
                    - `01_Folder/` - purpose
                    - `Document.md` - purpose
                  Lists child bundles and documents only. No format files, no assets, no prose.
  _summary.md     REQUIRED in every bundle folder. "# Title", then prose in this order:
                  origin, representation, scope (incl. what is not here), use.
                  No counts, latest dates, file names, or values. Written from own _metadata.json,
                  _inventory.md, _topics.md only - never from documents.
  _topics.md      REQUIRED in every bundle folder. "## Category" headings
                  (open set: Concepts, Facts, Decisions, Contacts, Todos, ...), then per entry:
                    - Name: statement
                      - `locator`
                  Nothing to list: the single line "No topics."
                  Folder holds documents: LLM-extracted. Folder holds only folders: mechanical merge
                  of direct children's _topics.md by code - same category headings, entries with the
                  same name merged, every locator prefixed with `child/`. No model call.
  Doc.data.md     OPTIONAL, next to Doc.*; only when structured data was extracted from
                  unstructured content. Per unit: "## Title", "Origin: table|chart|figure|image|inline
                  [ | label]", one "- `locator`" line per source, one fenced ```lang block.
  _data.md        OPTIONAL per folder, same unit grammar, consolidates data across documents.
  _metadata.json  REQUIRED at root, optional in nested bundles. Required: title, format_version.
                  Optional: description, author, publisher, source, source_url, source_type,
                  publishing_date, source_date, created, last_modified, language, license,
                  classification, producer-defined keys. No derived aggregates (counts, child lists).
  _images/ _svg/ _audio/ _video/ _pdf/ _fonts/
                  Asset folders for format-generated binaries; the name states the content type.
                  Native documents keep their own relative assets where they reference them.

LOCATORS: `path#fragment`, path relative to the folder that owns the referencing file.
  #heading-slug   #L12   #L12-L40   #L12C5-L40C80   #page=47   #t=00:12:30,00:14:05
  #cell=B2:D14   #cell=Sheet!B2:D14
  Omit the fragment when the document is the unit. One fragment per locator.
  Prefer headings over line numbers. Avoid ../ paths.

SEARCH: one vector store holds every _summary.md and _topics.md at every depth. Everything else
  is read on demand: _inventory.md, .data.md, _data.md, documents, assets.
  Progressive disclosure: summary -> topics -> inventory -> data -> document -> asset.

CHANGE COSTS (F = folder of the change, P = its parent; no model call anywhere else):
  Document edit, add, remove, rename   lines in F/_inventory.md, F/_topics.md, F/[doc].data.md.
                                       No summary regeneration.
  Folder add, move in, or remove       moved folder untouched; new folder gets its own files;
  under P                              1 line in P/_inventory.md, 1 regeneration of P/_summary.md,
                                       1 merge of P/_topics.md.
  Folder rename under P                1 line in P/_inventory.md, 1 merge of P/_topics.md.
                                       No regeneration.
  _metadata.json scope field change    1 regeneration of that folder's _summary.md.
  Merge = code re-reads direct children's _topics.md and rewrites the merged file; no model call;
  MAY cascade up to the root, MAY be deferred to the end of a batch.
  Bulk operations add up; at most 1 regeneration per parent after the batch. No model call above P.
  No step reads a document.

STORAGE: folder on disk, or .zip with the root folder as its single top-level entry. Same contents.

NOT PART OF THE FORMAT: how a bundle was produced (tools, models, settings, cost, quality, logs),
  transcription parameters, and what material a user bundles. Users decide.
````

## Table of Contents

1. [Scenario](#1-scenario)
2. [Context](#2-context)
3. [Applications](#3-applications)
4. [Domain Objects](#4-domain-objects)
5. [Functional Requirements](#5-functional-requirements)
6. [Non-Functional Requirements](#6-non-functional-requirements)
7. [Design Decisions](#7-design-decisions)
8. [Implementation Guarantees](#8-implementation-guarantees)
9. [Key Mechanisms](#9-key-mechanisms)
10. [Action Flow](#10-action-flow)
11. [Data Structures](#11-data-structures)
12. [Logging Requirements](#12-logging-requirements)
13. [Technical Constraints](#13-technical-constraints)
14. [Document History](#14-document-history)

## 1. Scenario

**Problem:** AI agents processing large bodies of material (books, wikis, document archives, data collections) cannot efficiently find specific knowledge without reading everything. Full-text search returns verbose results. Vector search over raw content dilutes relevance with boilerplate. Agents need structured, progressively-disclosed content where summaries enable fast relevance decisions and extracted knowledge enables precise retrieval. Material also changes: documents are added in bulk, removed, corrected. Generated indexes that must be rebuilt whole after every change rot, because the agent maintaining them gives up.

**Solution:**
- Recursive folder structure: every folder with `_inventory.md` is a self-contained Knowledge Bundle, at any depth
- Two concepts only: Folders group, Documents carry content. Any material maps onto them
- Single vector store with all `_summary.md` and `_topics.md` files; progressive disclosure for on-demand reading (data extracts, documents, assets)
- Standardized `_` file conventions for agent-discoverable content; ordering prefixes recommended, not mandated
- Two storage variants: folder on disk, and .zip archive for portability
- Agent tools (read, search) treat the format as a document type alongside PDF and plain text
- Every generated file is line-oriented and folder-local, so an agent inserting or removing hundreds of documents or folders edits a bounded, predictable set of lines and never rebuilds a global index
- After a small document edit, the files to re-sync are enumerable from the change alone (Change Propagation in Key Mechanisms)

**What we don't want:**
- Format concepts tied to one material type (chapters, pages, slides)
- Size or shape constraints on summaries and inventory that encode today's context window limits
- Meta-named folders (`_assets/`, `_misc/`) that tell an agent nothing
- Global indexes, cross-folder aggregates, or inline lists that force whole-file regeneration after one change
- Any generated content an agent cannot update with a single-line insert or delete
- Process records inside the bundle: production tool, model, settings, cost, quality scores, logs, transcription parameters. The format defines structure; users decide how they produce a bundle and what they put in it

### Architecture Diagram

```
Knowledge Bundle - Two Storage Variants

Variant 1: Folder on disk          Variant 2: .zip archive on disk

  BundleName/                        BundleName.zip
  ├── _inventory.md                (root folder is the single top-level entry in the archive)
  ├── _summary.md
  ├── _topics.md                   (merged from children by code)
  ├── _metadata.json
  ├── 01_FolderName/
  │   ├── _inventory.md
  │   ├── _summary.md
  │   ├── _topics.md               (extracted from documents by LLM)
  │   ├── _images/
  │   ├── Document-01.md
  │   ├── Document-01.data.md
  │   └── ...
  ├── 02_FolderName/
  │   ├── _inventory.md
  │   ├── _summary.md
  │   ├── _topics.md               (merged from children by code)
  │   ├── 01_FolderName/             (nested bundle, any depth)
  │   │   ├── _inventory.md
  │   │   ├── _summary.md
  │   │   ├── _topics.md
  │   │   └── ...
  │   └── 02_FolderName/
  └── ...

Vector Store and Progressive Disclosure

  Vector store (single index):
  ├── All _summary.md files    → folder summaries at every depth
  └── All _topics.md files     → topics as typed lists with locators

  On-demand retrieval (NOT in vector store):
  ├── *.data.md               → structured data (code, tables, CSV, JSON)
  ├── documents               → verbatim content
  └── assets                  → original fidelity (page scans, diagrams, audio)
```

### File Structure with Purpose Annotations

```
BundleName/                                                                Purpose
├── _inventory.md            Title, one line per child folder and document   Lookup (on-demand)
├── _summary.md              Cover text: origin, representation, scope, use  Vector store
├── _topics.md               Merge of child _topics.md, locators prefixed    Vector store (optional)
├── _metadata.json           Source metadata (title, format version, ...)    Search refinement (SQL)
├── _images/                 Bundle-level images (optional)                  Original fidelity (on-demand)
├── 01_FolderName/           Semantic grouping                               Context engineering
│   ├── _inventory.md        Folder title, one line per document             Lookup (on-demand, composable)
│   ├── _summary.md          Cover text for this folder                      Vector store
│   ├── _topics.md           Topics as typed lists with locators             Vector store
│   ├── _images/             Images belonging to documents in this folder    Original fidelity (on-demand)
│   │   ├── Document-01.jpg
│   │   └── ...
│   ├── Document-01.md       Verbatim content                                Full-text (on-demand)
│   ├── Document-01.data.md  Extracted code/tables/JSON                      Context engineering (on-demand)
│   ├── Document-02.md
│   └── ...                  (no .data.md = no structured data)
└── 02_FolderName/
    └── ...
```

## 2. Context

The format uses progressive disclosure: agent reads summaries first, goes deeper on demand. Context steering via file structure, not prompt.

Two concepts:
- **Folder** - groups documents or other folders. A folder with `_inventory.md` is a Knowledge Bundle in its own right. Depth is unlimited and mirrors whatever structure the material has: none (flat archive), one level (blog by year), several (book parts and chapters, wiki namespaces)
- **Document** - any content file. The format never alters documents; it adds `_inventory.md`, `_summary.md`, `_topics.md` per folder and optional `.data.md` per document - generated by LLM where documents are read, by code where children are merged - to make any material full-text, SQL, and vector searchable and discoverable by agents

Core mechanisms:
- `_inventory.md` per folder: lookup table, one line per child folder and document; changes by exactly one line per child event
- `_summary.md` per folder: cover text on origin, representation, scope, and use; no volatile facts, so it survives document changes and is regenerated only on folder-level events
- `_topics.md` per folder: dedicated vector search layer for whatever the consumer needs to find (concepts, keywords, facts, hypotheses, but also contacts, todos, decisions, deadlines) as typed lists, each entry pointing to its documents. LLM-extracted where documents live; mechanically merged from children where only folders live
- `.data.md` per document: optional structured data extraction (code, tables, CSV, JSON) as fenced blocks with a source locator
- `_metadata.json` at root: source-level metadata for SQL indexing; MAY also exist in any nested bundle
- Asset folders (`_images/`, `_svg/`, `_fonts/`, ...) hold format-generated binaries such as page scans; native documents keep their own relative assets

Process independence: the format specifies the files above and nothing about how they come to exist. Which tool, model, or settings produced documents, topics, or summaries, what it cost, how good it is, and what material a user chooses to bundle are the user's concerns and are recorded, if at all, outside the format.

Locators: every reference to a document is `path#fragment` - a heading (`#open-closed`), lines (`#L12-L40`), line and column (`#L12C5-L40C80`), a page (`#page=47`), a time (`#t=00:12:30`), or cells (`#cell=B2:D14`). The fragment forms follow GitHub, ISO 32000 (PDF), and W3C Media Fragments conventions so that agents, editors, and viewers already parse them.

## 3. Applications

The same two concepts cover different material. One pattern per application; all names generic.

### Ebook or textbook

```
BookTitle/
├── 00_FrontMatter/                           title, copyright, table of contents
├── 01_PartName/
│   ├── 01_ChapterName/
│   │   ├── _images/CleanCode-01_Page047.jpg
│   │   ├── CleanCode-01_Page047.md          document = one page
│   │   └── CleanCode-02_Page048.md
│   └── 02_ChapterName/
├── 02_PartName/
└── 99_BackMatter/                            index, bibliography
```

- Documents are transcribed pages; recommended name `[Topic]-[NN]_Page[NNN].md` keeps original page number and reading order
- Page scans in `_images/` with the same base name
- Locator `CleanCode-01_Page047.md` names the page; `#page=2` only inside multi-page documents

### Wiki or blog export

```
SiteName/
├── 2024/
│   ├── 2024-03-15_PostTitle.md              document = one article, unmodified
│   ├── 2024-03-15_PostTitle/diagram.png     relative asset stays where referenced
│   └── 2024-06-02_PostTitle.md
└── 2025/
```

- Folders mirror namespaces, categories, or years
- Documents are the native markdown files, byte-identical, original names
- Locator `2024-03-15_PostTitle.md#heading-slug` points into an article

### Scanned document collection

```
CorrespondenceArchive/
├── 2019/
│   ├── _images/2019-02-11_Letter_Supplier.jpg
│   ├── 2019-02-11_Letter_Supplier.md        document = one scanned letter
│   └── 2019-05-30_Invoice_0412.md
└── 2020/
```

- Each scan is one document with its own transcription; the term "page" does not apply and is not needed
- Multi-page scans: one document per scan, `#page=2` for positions inside it
- `_metadata.json` per year folder MAY record sender, recipient, case numbers for SQL filtering

### Financial data collection

```
FundResearch/
├── FundAlpha/
│   ├── _data.md                              consolidated table across factsheets (optional)
│   ├── Prices_2020-2025.csv                  document = structured data, no .data.md needed
│   ├── AnalystNote_2025-06.md                document = prose, topics extracted
│   ├── Factsheet_2025-Q2.md                  document = transcribed PDF, .data.md holds its tables
│   └── Factsheet_2025-Q2.data.md
└── FundBeta/
```

- A document may itself be structured (`.csv`, `.json`) - then no `.data.md` is created
- `.data.md` exists only where structured data had to be extracted from unstructured content
- Locator `Prices_2020-2025.csv#cell=B2:D14` references cells

### Slide deck, transcript, or recording

```
TalkTitle/
├── _images/Slide-01.jpg
├── _audio/Recording.mp3
├── Slide-01.md                               document = one slide
└── Transcript.md                             document = full transcript
```

- Locator `Transcript.md#t=00:12:30` for time positions inside a transcript
- Asset folder names state the content type: `_images/`, `_audio/`, `_video/`

### Code repository documentation

```
ProjectDocs/
├── guides/
│   ├── setup.md                              document = native markdown, unmodified
│   └── setup/architecture.svg                relative asset stays where referenced
└── reference/
```

- Folders mirror the repository tree
- Locator `guides/setup.md#L120-L140` for line ranges

## 4. Domain Objects

### Knowledge Bundle

A **Knowledge Bundle** is any folder that contains `_inventory.md`. The outermost bundle is the root; every nested bundle is a complete bundle on its own (composability).

- **Storage**: Folder on disk (variant 1) or .zip archive on disk (variant 2)
- **Root naming (recommended)**: `BundleName/` or `BundleName_YYYY-MM-DD/`; date = first non-empty of `publishing_date`, `source_date`, `last_modified`, `created` from `_metadata.json`
- **Required files**: `_inventory.md`, `_summary.md`, `_topics.md` - in every bundle folder, root included
- **Optional files**: `_metadata.json`, `_data.md`, asset folders

### Folder

A **Folder** groups documents or other folders. A folder becomes a Knowledge Bundle by containing `_inventory.md`. Depth is unlimited.

- **Naming (recommended)**: ordering prefix plus self-explaining name - `01_TopicName/`, `2024/`, `2024-03_TopicName/`
- **Ordering**: any prefix scheme that yields the intended lexical sort order; zero-pad numbers so sort order equals intended order
- **Plain subfolder**: a folder without `_inventory.md` is not a bundle; it holds only relative assets of native documents (e.g., `PostTitle/diagram.png`)
- **Key properties**: `name`, `children` (documents, folders, format files)

### Document

A **Document** is any content file inside a folder. The format never modifies documents.

- **Origin examples**: transcribed page, scanned letter, wiki article, blog post, factsheet, price series, transcript
- **Storage**: any filename, any extension, inside a bundle folder; `_` prefix and `.data.md` suffix are reserved for format files; relative assets referenced by a native document are not documents
- **Naming (recommended)**: preserve traceability to the original in the name - page number (`Topic-01_Page047.md`), date (`2019-02-11_Letter_Supplier.md`), or the original filename
- **Key properties**: `path` (relative to the owning folder, used in locators), `content` (verbatim, no agent annotations)

### Asset Folder

An **Asset Folder** holds format-generated binaries belonging to the documents of its parent folder.

- **Storage**: `_[type]/` inside the folder - `_images/`, `_svg/`, `_fonts/`, `_audio/`, `_video/`, `_pdf/`
- **Naming rule**: the folder name states the content type. Meta-words (`_assets/`, `_files/`, `_misc/`) are forbidden
- **Native assets**: documents of native origin keep their own relative assets where they reference them; those are not asset folders
- **Key properties**: asset files SHOULD share the base name of the document they belong to (`Document-01.md` ↔ `_images/Document-01.jpg`)

### Inventory

An **Inventory** is the lookup table of a folder: which child folders and documents exist and what each is for. An agent that has decided a folder is relevant reads it to pick the next file.

- **Storage**: `_inventory.md` in every bundle folder; the file whose presence makes a folder a bundle
- **Content**: `#` title, then one line per direct child folder and per document: `- \`name\` - one-line purpose`. Folder names end with `/`. Purpose MAY carry a range (pages, dates)
- **Not listed**: format files (`_summary.md`, `_topics.md`, `_metadata.json`, `_data.md`), `.data.md` files, asset folders, native relative-asset subfolders - all discoverable by convention from the document name or the format
- **Not contained**: metadata lines (in `_metadata.json`), tables of contents (the list is the table of contents), prose (in `_summary.md`)
- **Boundary**: direct children only - never the inventory of a nested folder
- **Update cost**: exactly one line per child added, removed, renamed, or re-described. Never more

### Summary

A **Summary** is the cover card of a folder, like the cover text of a book or the label on a file folder: where the material comes from, what it represents, what it covers and does not cover, and what it is good for. An agent reads it to decide whether the folder is relevant; a search engine indexes it to find the folder.

- **Storage**: `_summary.md` in every bundle folder
- **Content**: `#` title, then prose. SHOULD answer four questions in order: origin (where from, who made it, when), representation (what kind of material, in what form), scope (period, entities, subjects covered; what is deliberately not here), use (which questions it answers, how to navigate it). Typically one to five paragraphs; no size constraint
- **Stability rule**: no volatile facts - no counts, no latest dates, no document or folder names, no specific values. Those change with every document and live in `_inventory.md`, `_topics.md`, `_metadata.json`. A summary that obeys this rule stays valid while hundreds of documents are added
- **Regeneration inputs**: own `_metadata.json`, own `_inventory.md`, own `_topics.md`. Never documents, never child summaries. Three small files bound the cost
- **Regeneration triggers**: a child folder added or removed; a scope field of `_metadata.json` changed (`source`, `source_type`, `description`, `language`, dates); explicit request. Document changes never trigger regeneration; after a bulk document operation the producer SHOULD read summary and inventory once and confirm the scope statement still holds
- **Key properties**: `title`, `origin`, `representation`, `scope`, `use`

### Topic List

A **Topic List** holds whatever the bundle consumer needs to find in the documents of one folder - extracted knowledge, but equally contacts, todos, decisions, dates, open questions - as typed lists in plain markdown. A topic is any named thing with a statement and the places it occurs.

- **Storage**: `_topics.md` in every bundle folder
- **Two origins**: a folder that holds documents has an LLM-extracted topic list; a folder that holds only folders has a merged topic list, produced by code from the direct children's `_topics.md`: same `##` categories, entries with identical name under the same category merged into one (first statement kept, locators concatenated), every locator prefixed with `child/`. Deterministic, no model call, reproducible at any time
- **Self-similarity**: a bundle moved into another bundle needs no change of its own; the receiving folder re-merges its `_topics.md`, adds one inventory line, regenerates its summary
- **Format**: one `##` heading per category, one list item per entry, one nested list item per locator (see Data Structures)
- **Categories**: open set, defined by the consumer's needs. Knowledge extraction commonly uses Concepts, Principles, Methods, Keywords, Acronyms, Facts, Conclusions, Hypotheses, Problems, Solutions, Ideas. Other material calls for Contacts, Todos, Decisions, Deadlines, Amounts, Open Questions, Risks, Requirements. Any `##` heading is valid
- **Key properties**: `category`, `name`, `statement`, `locators` (one or more, relative to the folder)

### Data Extract

A **Data Extract** is structured data (code, tables, CSV, JSON, XML) extracted from one document or consolidated across a folder, stored as data units in plain markdown.

- **Storage**: `[document base name].data.md` next to the document (per document), or `_data.md` in the folder (consolidated, optional)
- **Created only when** structured data had to be extracted from unstructured content. A document that is already structured (`.csv`, `.json`) gets no `.data.md`
- **Format**: one `##` heading per data unit, one `Origin:` line, one list item per locator, one fenced code block (see Data Structures)
- **Key properties**: `title`, `locators` (one or more, relative to the folder), `origin` (`table`, `chart`, `figure`, `image`, `inline`), `lang` (fence info string)

### Bundle Metadata

**Bundle Metadata** is machine-readable source metadata for SQL indexing and search refinement.

- **Storage**: `_metadata.json` at root; MAY exist in any nested bundle
- **Required keys**: `title`, `format_version`
- **Optional keys**: `description`, `author`, `publisher`, `source`, `source_url`, `source_type`, `publishing_date`, `source_date`, `created`, `last_modified`, `language`, `license`, `classification`, and any further key the producer needs
- **Never contains**: derived aggregates (counts, child arrays) - those come from the file system, nor process records (tool, model, settings, cost, quality) - those are outside the format

## 5. Functional Requirements

**IPPSKBNDL-FR-01: Two storage variants**
- Variant 1: folder structure on disk (`BundleName/`)
- Variant 2: .zip archive on disk (`BundleName.zip`)
- Both variants contain identical internal structure
- .zip archive contains the root folder as its single top-level entry and preserves the hierarchy
- .zip archive includes asset folders; gitignore policy applies to the folder variant only

**IPPSKBNDL-FR-02: Inventory file**
- Every bundle folder contains `_inventory.md`; its presence makes the folder a bundle (composability)
- Content: `#` title, then one line per direct child folder and per document: `- \`name\` - purpose`. Nothing else
- Lists payload children only: child folders (name with trailing `/`) and documents. Format files, `.data.md`, asset folders, and native relative-asset subfolders are not listed - they follow from convention
- No metadata lines (belong in `_metadata.json`), no table of contents (the list is one), no prose (belongs in `_summary.md`)
- Purpose is one line and MAY carry a range (pages, dates) or a document count for a child folder
- Direct children only - no level repeats the inventory of another level
- Not in the vector store: read on demand after `_summary.md` or `_topics.md` identified the folder

**IPPSKBNDL-FR-03: Metadata file**
- Root contains `_metadata.json`; nested bundles MAY contain their own
- MUST contain: `title`, `format_version`
- MAY contain: `description`, `author`, `publisher`, `source`, `source_url`, `source_type`, `publishing_date`, `source_date`, `created`, `last_modified`, `language`, `license`, `classification`, and producer-defined keys
- `source_type` is free text describing the origin (e.g., `pdf-transcription`, `markdown-export`, `scan`, `csv`)
- `classification` values are organization-defined (sensitivity or handling label)
- Folder and document structure is derived from the file system at runtime - NOT stored in metadata
- Used for SQL indexing and search refinement on source attributes, NOT vector search

**IPPSKBNDL-FR-04: Folder structure**
- A folder is a bundle iff it contains `_inventory.md`; every bundle folder also contains `_summary.md`
- Every bundle folder also contains `_topics.md`; every folder that directly contains documents is a bundle
- A folder without `_inventory.md` holds only relative assets of native documents - never documents
- Documents live directly in the folder; `.data.md` files live next to their document
- Format-generated binaries live in asset folders (`_images/`, `_svg/`, `_fonts/`, ...) inside the folder
- Nesting depth is unlimited and mirrors the material's own structure
- Folder names SHOULD be self-explaining and SHOULD carry an ordering prefix when order matters

**IPPSKBNDL-FR-05: Summary**
- Every bundle folder contains `_summary.md`: `#` title, then prose (format in Data Structures)
- Prose SHOULD cover, in order: origin, representation, scope (incl. what is not here), use. Typically one to five paragraphs; no size or language constraint
- Stability: no counts, no latest dates, no document or folder names, no specific values. Volatile facts live in `_inventory.md`, `_topics.md`, `_metadata.json`
- Derived from own `_metadata.json`, `_inventory.md`, `_topics.md` only - never from documents, never from child summaries
- Regenerated only when a child folder is added or removed, a scope field of `_metadata.json` changes, or on explicit request. Document add, remove, rename, edit: no regeneration. After a bulk document operation: one read of summary and inventory to confirm the scope statement, no rewrite unless it fails
- Part of the single vector store; the first paragraph carries the strongest relevance signal and SHOULD state the subject in its first sentence

**IPPSKBNDL-FR-06: Topic list**
- Every bundle folder has `_topics.md`. Folder holds documents: LLM-extracted. Folder holds only folders: mechanical merge of the direct children's `_topics.md` by code (categories unioned, same-name entries merged, locators prefixed with `child/`)
- Plain markdown: `##` heading per category, `- Name: statement` per entry, nested `- \`locator\`` line per source (format in Data Structures)
- Categories: open set - any `##` heading the consumer needs (knowledge: Concepts, Principles, Methods, Keywords, Acronyms, Facts, Conclusions, Hypotheses, Problems, Solutions, Ideas; operational: Contacts, Todos, Decisions, Deadlines, Amounts, Open Questions, Risks, Requirements); only categories with entries appear
- Every entry carries at least one locator (`path#fragment`, relative to the folder)
- Entries are self-contained: retrievable without reading the referenced document
- Folders with nothing to list contain `_topics.md` with the single line `No topics.`
- Topics file is part of the single vector store; producers MAY exclude merged topic lists from the index to avoid duplicate hits, the file on disk is still required

**IPPSKBNDL-FR-07: Documents**
- Any file in a bundle folder that is not `_`-prefixed, not `.data.md`, and not a relative asset referenced by a native document is a document
- Documents are stored verbatim: transcribed content has no agent annotations; native files are byte-identical with original names
- Document names SHOULD preserve traceability to the original (page number, date, or original filename)
- Recommended pattern for paginated material: `[Topic]-[NN]_Page[NNN].md` with `NN` = position in folder, `NNN` = original page number, zero-padded so sort order equals reading order
- Documents are retrieved on demand only after search identifies them

**IPPSKBNDL-FR-08: Data extract files (optional)**
- Created only when structured data had to be extracted from unstructured content
- Per document: `[document base name].data.md` (e.g., `Topic-01_Page047.data.md`, `README.data.md`)
- Per folder (optional): `_data.md` consolidating data across documents; each unit carries its own locators
- Plain markdown: `##` heading (title), `Origin:` line (origin, optional source label), one list item per locator, fenced code block with language info string (format in Data Structures)
- Origin values: `table`, `chart`, `figure`, `image`, `inline`
- CSV is normalized on extraction: `,` column separator, `.` decimal separator, no thousands separator
- No empty `.data.md` files
- Data files are retrieved on demand only after search identifies the document

**IPPSKBNDL-FR-09: Asset folders**
- Format-generated binaries (page scans, rendered diagrams, extracted audio) go to asset folders inside the owning folder
- Asset folder names state the content type: `_images/`, `_svg/`, `_fonts/`, `_audio/`, `_video/`, `_pdf/`. Meta-names (`_assets/`, `_files/`) are forbidden
- Asset files SHOULD share the base name of their document (`Document-01.md` ↔ `_images/Document-01.jpg`)
- Documents of native origin keep their relative assets where they reference them - relative links must keep working; these are payload, not asset folders
- Asset folders contain binaries - gitignore policy is environment-specific, not encoded in the folder name

**IPPSKBNDL-FR-10: Naming conventions**
- `_` prefix = format files and asset folders expected by agents (`_inventory.md`, `_summary.md`, `_topics.md`, `_data.md`, `_metadata.json`, `_images/`, ...)
- Ordering prefixes SHOULD be used where order matters: `NN_` for authored sequences, `YYYY-MM-DD_` or `YYYY-MM_` for chronological material, or any other scheme whose lexical sort equals the intended order
- Numbers in ordering prefixes SHOULD be zero-padded to the width the collection needs
- Names SHOULD be self-explaining; an agent must be able to infer the content from the name alone
- Names MUST be safe for file systems and .zip archives

**IPPSKBNDL-FR-11: Single vector store and progressive disclosure**
- Single vector store contains all `_summary.md` and `_topics.md` files from all folders at all depths - no separate tier indices
- Vector search returns relevant folders and specific topic entries from one query
- On-demand retrieval (NOT in vector store):
  - `.data.md` and `_data.md` - structured data - retrieved after search identifies the document or folder
  - Documents - verbatim content - retrieved when topics and data are insufficient
  - Assets - original fidelity - retrieved when text is insufficient (diagrams, charts, layouts, audio)
- Excluding documents and assets from the vector store prevents result dilution

**IPPSKBNDL-FR-12: Process independence**
- The format defines folder structure, format files, and their grammar - nothing about how they are produced
- No format file records production tool, model, settings, cost, quality scores, logs, or transcription parameters
- Users decide which material they bundle, how they produce documents and generated files, and where they keep process records - outside the bundle or in their own payload documents
- `source_type` in `_metadata.json` names the kind of source (`scan`, `markdown-export`), not the process that handled it

**IPPSKBNDL-FR-13: Nested bundles**
- When the material has hierarchical structure (parts and chapters, namespaces, years, instruments), folders mirror it at any depth
- Every nested folder that is a bundle contains `_inventory.md`, `_summary.md`, `_topics.md` - identical to the root
- A bundle moved into another bundle is not modified; only the receiving folder's three files change
- Flat material (a folder of scans) needs no nesting - documents live in the root folder

**IPPSKBNDL-FR-14: Original fidelity via assets**
- When derived text is insufficient (diagrams, charts, visual layouts, tone of voice), the agent retrieves the asset belonging to the document from the asset folder
- Agent embeds the asset (image, audio) for context when the document text does not answer the question
- If assets are absent (native material, or gitignored in the folder variant), agent falls back to the document
- Assets are on demand only, NOT in vector store

## 6. Non-Functional Requirements

**IPPSKBNDL-NFR-01: Git compatibility**
- Generated files (`.md`, `.json`) are text-based and git-friendly
- Format-generated binaries are isolated in asset folders so an environment can gitignore them

**IPPSKBNDL-NFR-02: Portability**
- .zip variant preserves all directory hierarchy and file contents
- .zip variant is openable by standard archive tools

**IPPSKBNDL-NFR-03: Scalability**
- Format supports bundles of any size and depth
- No fixed widths, counts, or lengths - all numeric conventions grow with the collection

**IPPSKBNDL-NFR-04: Agent editability**
- Adding or removing N documents costs O(N) line edits: N inventory lines in one `_inventory.md`, N locator sets in one `_topics.md`, N optional `.data.md` files. Zero summary regenerations; one summary read after the batch
- Adding, moving in, or removing a folder costs the folder's own format files, one line in `P/_inventory.md`, one regeneration of `P/_summary.md` from three small files, one code merge of `P/_topics.md`. No model work above P
- A document change needs model work only inside its folder. A folder change needs model work only in itself and its parent. Merged `_topics.md` files up to the root are rebuilt by code, deferrable to the end of a batch
- Summary regeneration reads `_metadata.json`, `_inventory.md`, `_topics.md` of one folder - never documents, never child summaries; a small model suffices
- Every generated file except `_summary.md` is updatable by inserting, deleting, or replacing whole lines; `_summary.md` is regenerated whole but rarely, and only from generated inputs; no generated file needs a parser beyond markdown lists and fenced blocks
- The set of files to re-sync after any change is derivable from the change alone (Change Propagation rules), no global scan required

**IPPSKBNDL-NFR-05: Producer neutrality**
- Any tool, model, or manual process can produce a compliant bundle; the format imposes no pipeline, no settings, no quality gates
- A bundle carries nothing that ties it to the process that made it; two producers yield structurally identical bundles from the same material

## 7. Design Decisions

**IPPSKBNDL-DD-01:** `_` prefix for format files and asset folders, `.data.md` suffix for per-document data extracts - separates format layer from payload by name alone

**IPPSKBNDL-DD-02:** Ordering prefixes are SHOULD, not MUST; multiple schemes (`NN_`, ISO dates, none) are valid - the material dictates the order

**IPPSKBNDL-DD-03:** `_summary.md` in every bundle folder at every depth

**IPPSKBNDL-DD-04:** Format-generated binaries separated from documents in asset folders

**IPPSKBNDL-DD-05:** `_topics.md` as dedicated vector search layer for topics - extracted knowledge and any consumer-defined item (contacts, todos, decisions)

**IPPSKBNDL-DD-06:** `.data.md` optional per document - only created when structured data had to be extracted

**IPPSKBNDL-DD-07:** Single vector store with all `_summary.md` and `_topics.md` files - no separate tier indices

**IPPSKBNDL-DD-08:** Two storage variants (folder and .zip) with identical internal structure - no further containers

**IPPSKBNDL-DD-09:** Minimal design - no derived aggregates in `_metadata.json`; structural data lives in `_inventory.md` at the folder that owns the children, never duplicated across levels

**IPPSKBNDL-DD-10:** `_metadata.json` stores source-level metadata only; structure derived at runtime

**IPPSKBNDL-DD-11:** `_inventory.md` in every bundle folder enables composability - bundles contain bundles contain bundles

**IPPSKBNDL-DD-12:** Process independence - the format contains no record of how a bundle was produced (tool, model, settings, cost, quality scores, logs). Users decide how they use the format and what they bundle with it; process records belong outside the bundle or in the user's own payload documents

**IPPSKBNDL-DD-13:** Two format concepts only - Folder and Document. Part, Section, Chapter, Page, Slide, Article are material vocabulary, shown in Applications, never format rules

**IPPSKBNDL-DD-14:** Plain markdown for `_topics.md` and `.data.md` - headings, list items, fenced code blocks. No custom tag syntax: token-efficient, readable, parseable with any markdown tool

**IPPSKBNDL-DD-15:** Original fidelity via assets when derived text is insufficient

**IPPSKBNDL-DD-16:** Documents are payload of any origin; the format never modifies them. Origin is named in `source_type`, not encoded in the structure

**IPPSKBNDL-DD-17:** Asset folder names are self-explaining (`_images/`, `_svg/`, `_fonts/`) - an LLM derives nothing from meta-words like `_assets/` `[ASSUMED]`

**IPPSKBNDL-DD-18:** No size or attribute-count constraints on `_inventory.md` and `_summary.md` - only the bare minimum content is fixed; optimal size depends on model, search technology, and material and will change `[ASSUMED]`

**IPPSKBNDL-DD-19:** One locator syntax for all material: `path#fragment`, reusing established fragment conventions - GitHub `#L12C5-L40C80`, ISO 32000 `#page=47`, W3C Media Fragments `#t=00:12:30,00:14:05`, heading slugs. Extensions (`#cell=`) follow the same key=value pattern

**IPPSKBNDL-DD-20:** Locality and line orientation over compactness - every generated file describes only its own folder's direct children, one item per line. This costs a few tokens per entry and buys O(1) edits per change, clean diffs, and no cross-folder invalidation. The format is designed for the agent that maintains it, not only for the agent that reads it

**IPPSKBNDL-DD-21:** Two files with disjoint jobs - `_inventory.md` is lookup (what exists, one line each, changes with every document), `_summary.md` is cover text (what it is, prose, changes with scope only). Mixing them would make the prose churn with every document or bloat the lookup with paragraphs

**IPPSKBNDL-DD-22:** `_summary.md` is derived from generated files, not from documents - own `_metadata.json`, `_inventory.md`, `_topics.md`. Regeneration cost is independent of document count and size, a cheap model can do it, and it is triggered by folder-level events only

**IPPSKBNDL-DD-23:** Stability by exclusion - `_summary.md` contains no counts, dates, names, or values. Every fact that changes with a document has a line-oriented home elsewhere. This is what lets hundreds of documents be added without touching the summary, and it removes the "did meaning change materially" judgment: if the summary obeys the rule, document changes cannot invalidate it

**IPPSKBNDL-DD-24:** Inventory lists payload only. Format files, `.data.md`, and asset folders follow from convention and would double the line count for zero navigational value

**IPPSKBNDL-DD-25:** `_topics.md` in folder-only bundles is a code merge, not an LLM abstraction. Self-similarity requires every bundle folder to have the same three files, so a bundle can be moved into any other bundle without modification. Making the parent's topic list a deterministic merge of its children keeps that file model-free: it never needs judgment, never drifts, and can be rebuilt at any time from files that already exist. The price is duplication of topic lines up the tree, which is why producers MAY leave merged lists out of the vector store

## 8. Implementation Guarantees

**IPPSKBNDL-IG-01:** Every bundle folder MUST contain `_inventory.md`, `_summary.md`, `_topics.md` - root included, no exceptions
**IPPSKBNDL-IG-02:** `_topics.md` in a folder without documents MUST be reproducible by code from the direct children's `_topics.md` alone - no model call, no document read (single line `No topics.` when nothing to list)
**IPPSKBNDL-IG-03:** Format-generated binaries appear only in asset folders, never next to documents
**IPPSKBNDL-IG-04:** Documents contain verbatim content only - no agent annotations, no metadata, no processing comments
**IPPSKBNDL-IG-05:** `.data.md` and `_data.md` files are created only when structured data was extracted - no empty data files
**IPPSKBNDL-IG-06:** Both storage variants (folder, .zip) contain identical internal structure - no variant-specific files or differences
**IPPSKBNDL-IG-07:** Traceability to the original is never lost - via document name, locator fragment, or `source` in `_metadata.json`
**IPPSKBNDL-IG-08:** Documents of native origin are stored byte-identical with original names; relative asset links keep working
**IPPSKBNDL-IG-09:** Every topic entry and every data unit carries at least one locator; no `_topics.md` or `.data.md` content is unattributed
**IPPSKBNDL-IG-10:** Asset folder names state the content type - no meta-words
**IPPSKBNDL-IG-11:** No generated file references content outside its own subtree; downward references are limited to `_inventory.md` naming its direct child folders and merged `_topics.md` carrying child-prefixed locators; `../` locators SHOULD be avoided; a change in one folder never invalidates a sibling folder's generated files
**IPPSKBNDL-IG-12:** Every generated file except `_summary.md` is line-oriented: one child per inventory line, one entry per list item, one locator per nested line, one data unit per heading. No inline enumerations
**IPPSKBNDL-IG-13:** `_summary.md` MUST be reproducible from the folder's own `_metadata.json`, `_inventory.md`, and `_topics.md`. A producer that needs to read documents to write a summary has put content into the wrong file
**IPPSKBNDL-IG-14:** `_summary.md` contains no counts, no dates other than the scope period, no document or folder names, no specific values. A document change never makes a compliant summary wrong
**IPPSKBNDL-IG-15:** `_inventory.md` lists exactly the direct child folders and documents, one line each, nothing else. Its line count equals the number of payload children
**IPPSKBNDL-IG-16:** No format file contains process records - production tool, model, settings, cost, quality scores, logs, or transcription parameters

## 9. Key Mechanisms

### Progressive Disclosure

Agent retrieves knowledge from the vector store, then goes deeper on demand:

```
Agent receives question
├─> Vector search (single store: all _summary.md + _topics.md)
│   └─> Returns relevant folders (summary hits) and specific entries with locators (topic hits)
├─> Read _inventory.md of a relevant folder (if navigation needed)
│   └─> One line per child folder and document: pick the next file by purpose
├─> Read .data.md or _data.md (if structured data needed)
│   └─> Retrieves code, tables, CSV, JSON for the identified document or folder
├─> Read document (if verbatim content needed)
│   └─> Retrieves exact content at the locator
└─> Read asset (if original fidelity needed)
    └─> Embeds page scan, diagram, or audio for context
```

### Locators

A locator is `path#fragment`. `path` is the document path relative to the folder that owns the referencing file (`_topics.md`, `.data.md`, `_data.md`, `_inventory.md`). `fragment` is optional and names a position inside the document. The fragment grammar reuses conventions that agents, editors, and viewers already parse; no new syntax is invented.

**Fragment forms:**

- **Heading** - `#heading-slug` - GitHub-style slug of the heading text: lowercase, spaces to `-`, punctuation removed. `setup.md#open-closed`
- **Line** - `#L12` - one line; `#L12-L40` - inclusive range. GitHub permalink syntax. `setup.md#L120-L140`
- **Line and column** - `#L12C5` - line 12, column 5; `#L12C5-L40C80` - range with columns; mixed forms `#L12C5-L40` and `#L12-L40C80` allowed. GitHub permalink syntax. Use when a line is long (minified files, single-line JSON, data dumps). `bundle.min.js#L1C4820-L1C4975`
- **Page** - `#page=47` - one page, 1-based. ISO 32000 (PDF) fragment identifier. Ranges as two locators or `#page=47-50`. `Report.md#page=47`
- **Time** - `#t=00:12:30` - start time; `#t=00:12:30,00:14:05` - range (comma-separated, half-open). W3C Media Fragments Normal Play Time: `hh:mm:ss[.fff]`, `mm:ss`, or seconds. `Transcript.md#t=00:12:30,00:14:05`
- **Cell** - `#cell=B12` - one cell; `#cell=B2:D14` - range; `#cell=Prices!B2:D14` - with sheet. Key=value extension in the ISO 32000 and Media Fragments style. `Prices_2020-2025.csv#cell=B2:D14`

**Rules:**

- Lines and columns are 1-based, columns count Unicode code points
- Lines and pages are inclusive ranges, time is half-open `[start, end)`
- One fragment per locator. Several positions in one document = several locators
- Omit the fragment when the document itself is the unit (one page per document, one letter per document)
- Percent-encode `#`, `%`, and whitespace inside `path`
- Producers SHOULD prefer heading over line locators for markdown documents: headings survive edits, line numbers do not
- Locators SHOULD stay inside the owning folder. A `../` locator couples two folders: renaming or removing the target folder forces edits in the referencing folder (see Change Propagation). Prefer repeating the topic in the target folder's own `_topics.md`
- Text alias: `path:line[:column]` (compiler and editor convention, e.g. `setup.md:120:5`) is accepted on input and normalized to `path#L120C5` on output

**In markdown:** locators are written as plain inline code (`` `setup.md#L120-L140` ``) in the generated files for token efficiency. The link form (`[setup.md](setup.md#L120-L140)`) carries the same locator and MAY be used in documents or consumer-authored files where clickability matters.

**Examples by material:**

- Transcribed page, whole document: `CleanCode-01_Page047.md`
- Multi-page scan, page 3: `2019-05-30_Invoice_0412.md#page=3`
- Wiki article, heading: `2024-03-15_PostTitle.md#deployment-checklist`
- Native guide, lines: `guides/setup.md#L120-L140`
- Single-line JSON dump, byte range inside line 1: `exports/config.json#L1C4820-L1C4975`
- Column-precise start, line end: `data/dump.log#L88C12-L88`
- Price series, cell range: `Prices_2020-2025.csv#cell=B2:D14`
- Workbook with sheets, one cell: `Holdings.xlsx#cell=Q2!F7`
- Transcript, start only: `Transcript.md#t=00:41:10`
- Transcript, range: `Transcript.md#t=00:12:30,00:14:05`
- Recording asset, seconds: `_audio/Recording.mp3#t=750,845`
- Path with space, percent-encoded: `Board%20Minutes_2025-03.md#page=2`
- Document in a sibling folder, relative path (allowed, SHOULD be avoided): `../02_ChapterName/CleanCode-14_Page212.md`
- Link form: `[Setup guide](guides/setup.md#prerequisites)`
- Text alias on input: `guides/setup.md:120:5` normalizes to `guides/setup.md#L120C5`

### Change Propagation

What an agent must touch after each kind of change. Nothing else changes. `F` is the folder containing the change, `P` its parent.

Cost units: **line** = insert, delete, or replace one line (no model call needed beyond knowing the line); **regen** = rewrite one `_summary.md` from `_metadata.json`, `_inventory.md`, `_topics.md` of that folder (one small-model call, three small inputs, no documents); **merge** = rewrite one folder-only `_topics.md` from the direct children's `_topics.md` by code (no model call); **read** = read one small file to confirm nothing needs to change.

Merges cascade: a changed `F/_topics.md` invalidates `P/_topics.md`, which invalidates its parent's, up to the root. Because a merge is code, the cascade costs no model call and MAY be deferred to one pass at the end of a batch. Costs below count model work; merges are listed separately.

**Document edited in F (content changed, name unchanged):**
- `F/[doc].data.md` - re-extract if the edit touched structured data; delete if none remains
- `F/_topics.md` - re-check entries whose locators point to the document: heading slugs and line numbers may have moved; add, remove, or re-point locator lines; drop entries left with zero locators
- `F/_inventory.md` - 0 lines, or 1 line if the document's purpose changed
- `F/_summary.md` - 0
- Root or nearest `_metadata.json` - `last_modified`
- Cost: k locator lines, 0-1 inventory line, 0 regen; merges up the chain if `F/_topics.md` changed

**Document added to F:**
- `F/_inventory.md` - 1 line
- `F/_topics.md` - new entries or locator lines under existing entries
- `F/[doc].data.md` - create if structured data was extracted
- `F/_summary.md` - 0
- Cost: 1 inventory line, k topic lines, 0 regen; merges up the chain

**Document removed from F:**
- `F/_inventory.md` - 1 line
- `F/_topics.md` - delete every locator line pointing to it; delete entries left with zero locators
- `F/[doc].data.md` - delete
- `F/_data.md` - delete locator lines pointing to it; delete units left with zero locators
- Format-generated assets of the document in `F/_images/` etc. - delete
- `F/_summary.md` - 0
- Cost: 1 inventory line, k topic lines, 0 regen; merges up the chain

**Document renamed in F:**
- `F/_inventory.md` - 1 line
- `F/_topics.md`, `F/_data.md` - every locator line with the old path (mechanical find and replace)
- `F/[doc].data.md` and assets - rename
- `F/_summary.md` - 0 (names never appear in a summary)
- Cost: 1 inventory line, k locator lines, 0 regen; merges up the chain

**Folder added under P:**
- New folder - create `_inventory.md`, `_summary.md`, `_topics.md`
- `P/_inventory.md` - 1 line
- `P/_summary.md` - 1 regen (scope of P changed)
- `P/_topics.md` - 1 merge
- Above P - 0 model calls: the grandparent's inventory lists P, not P's children, and its summary describes P's scope only in terms P's own inventory line already gives; merges cascade by code
- Cost: new folder's own files, 1 inventory line, 1 regen, merges up the chain

**Existing bundle moved into P (composability):**
- The moved bundle - 0: all its files are relative to itself and complete
- `P/_inventory.md` - 1 line
- `P/_summary.md` - 1 regen
- `P/_topics.md` - 1 merge
- Old parent - as "Folder removed"
- Cost: 1 inventory line, 1 regen, merges up the chain; the moved bundle is never opened beyond its own `_inventory.md` line and `_topics.md`

**Folder removed under P:**
- Delete the folder
- `P/_inventory.md` - 1 line
- `P/_summary.md` - 1 regen
- `P/_topics.md` - 1 merge
- Any `../` locator in a sibling that pointed into the removed folder - delete the locator line (this is why `../` locators SHOULD be avoided)
- Cost: 1 inventory line, 1 regen, merges up the chain

**Folder renamed or reordered under P:**
- Rename the folder
- `P/_inventory.md` - 1 line
- `P/_summary.md` - 0 (names never appear in a summary)
- `P/_topics.md` - 1 merge (locator prefixes carry the folder name)
- Locators inside the folder are relative and unaffected
- `../` locators in siblings - edit (avoidable by not using them)
- Cost: 1 inventory line, 0 regen, merges up the chain

**Child folder re-described (F's purpose changed, e.g. its subject shifted):**
- `P/_inventory.md` - 1 line (F's purpose)
- `P/_summary.md` - 1 regen only if P's scope statement no longer covers F; otherwise 0
- Cost: 1 inventory line, 0-1 regen

**`_metadata.json` scope field changed (source, source_type, description, language, dates):**
- `_summary.md` of that folder - 1 regen
- Cost: 1 regen

**Bulk operations:** costs add. 300 documents added to F = 300 inventory lines, up to 300 `.data.md` files, topic lines, 0 regen, then 1 read of `F/_summary.md` against `F/_inventory.md` to confirm the scope statement still holds (it does unless the batch introduced a new subject, period, or entity class - then 1 regen). 40 folders added under P = 40 new folder sets, 40 inventory lines in P, 1 regen of `P/_summary.md` after the batch, not 40. Merges: one pass from the deepest changed folder to the root after the batch, not per change.

**Worst case per change:** 1 regen, at the parent, from three small files. Never two regens, never a model call above the parent, never a document read. **Typical case** (document-level change): 0 regen. Merges are code and do not count as model work.

**Invariant:** after any change, the files needing model work are inside `F`, plus `P/_inventory.md` and possibly `P/_summary.md` for folder-level changes. Merged `_topics.md` files from P to the root are rebuilt by code. An agent enumerates all of them from the change without scanning the bundle, and no step opens a document.

## 10. Action Flow

### Creating a Knowledge Bundle

```
Material (page images, native files, data files, scans, recordings)
├─> Produce documents
│   ├─> Paginated or scanned material: render each unit to a document, store originals in asset folders
│   └─> Native files: copy byte-identical, keep original names and relative assets
├─> Analyze documents → identify folder structure (mirror the material's own structure)
├─> Propose folder breakdown for user review
├─> Create folders with self-explaining names and ordering prefixes where order matters
├─> Place documents; move format-generated binaries to asset folders
├─> Extract topics → write _topics.md per folder with documents (locator per entry)
├─> Merge topics → write _topics.md per folder without documents from direct children (code, locators prefixed)
├─> Extract structured data → write .data.md per document where applicable; _data.md per folder if consolidation helps
├─> Write _inventory.md per folder (title, one line per child folder and document)
├─> Write _summary.md per folder from own _metadata.json, _inventory.md, _topics.md (origin, representation, scope, use; no volatile facts)
├─> Write _metadata.json at root (and in nested bundles where useful)
└─> Optionally: create .zip archive variant
```

## 11. Data Structures

### _metadata.json Schema

Minimum:

```json
{
  "title": "Source Material Title",
  "format_version": "1.0"
}
```

With optional keys:

```json
{
  "title": "Source Material Title",
  "description": "Brief one-line description of the source",
  "author": "Author Name",
  "publisher": "Publisher Name",
  "source": "path/to/source/or/description",
  "source_url": "https://example.com/source",
  "source_type": "pdf-transcription",
  "publishing_date": "2026-01-15",
  "source_date": "",
  "created": "2026-09-15",
  "last_modified": "2026-09-15",
  "language": "en",
  "license": "CC-BY-4.0",
  "classification": "",
  "format_version": "1.0"
}
```

- `source_type` - free text describing origin
- `source_date` - date the source was retrieved or last observed; used when `publishing_date` is empty
- `classification` - organization-defined, empty when unused
- Producer-defined keys are allowed

Native export (wiki), root:

```json
{
  "title": "Engineering Wiki",
  "description": "Internal engineering wiki, markdown export",
  "source": "wiki-export-2026-09-01.zip",
  "source_url": "https://wiki.example.com/engineering",
  "source_type": "markdown-export",
  "source_date": "2026-09-01",
  "created": "2026-09-02",
  "last_modified": "2026-09-02",
  "language": "en",
  "classification": "internal",
  "format_version": "1.0"
}
```

Nested bundle (scan archive, one year) with producer-defined keys:

```json
{
  "title": "Correspondence 2019",
  "source_type": "scan",
  "source_date": "2019-12-31",
  "language": "de",
  "format_version": "1.0",
  "counterparties": ["Supplier GmbH", "Tax Office"],
  "case_numbers": ["2019-0412", "2019-0587"]
}
```

Data collection, root:

```json
{
  "title": "Fund Research",
  "description": "Factsheets, analyst notes, and price series for tracked funds",
  "source_type": "mixed",
  "publishing_date": "",
  "source_date": "2026-06-30",
  "created": "2026-07-01",
  "last_modified": "2026-09-10",
  "language": "en",
  "format_version": "1.0"
}
```

### _summary.md Format

Plain markdown: `#` title, then prose. Cover text, not an index.

```
# Folder Title

<origin: where the material comes from, who produced it, how it got here>

<representation: what kind of material this is and in what form it is stored>

<scope: period, entities, subjects covered - and what is deliberately not here>

<use: which questions this folder answers and how to navigate it>
```

- Four questions in order, one paragraph each is the common shape; merge or split as the material needs. Typically one to five paragraphs; no size constraint
- First sentence names the subject - it is the strongest signal in the vector store chunk
- **Stability rule** - nothing that changes when a document is added or removed: no counts ("12 factsheets"), no latest dates ("through 2025-Q2"), no document or folder names, no specific values ("TER 0.85%"). Period boundaries that define the scope are allowed ("2019 correspondence"); running end dates are not. Everything excluded has a line-oriented home: names and purposes in `_inventory.md`, facts and values in `_topics.md`, dates and source in `_metadata.json`
- Written from own `_metadata.json`, `_inventory.md`, `_topics.md`. Never from documents, never from child summaries
- Regenerated whole, but only on folder-level events (child folder added or removed, `_metadata.json` scope field changed). A compliant summary survives any number of document changes unchanged
- Test before writing: "If 300 more documents of the same kind arrive tomorrow, is every sentence still true?" If not, move the offending fact to its line-oriented home

Leaf folder (folder of price series):

```
# Prices

Daily closing prices exported from the fund administrator's portal, adjusted for distributions.

One CSV per fund, one row per trading day, columns for date, close, and adjustment factor.

Covers the tracked funds for their full trading history in the collection. Intraday data and benchmark series are not included.

Use for drawdown, recovery, and volatility questions; combine with the factsheets in the sibling folders for holdings and fees.
```

Leaf folder (chapter of a textbook):

```
# 01_ChapterName

Transcribed pages of the first chapter of a software design textbook, taken from the publisher PDF and transcribed page by page.

One markdown document per page with the original page number in the file name; page scans in the image folder for figures and code listings.

Introduces the Single Responsibility Principle through a billing-module refactoring, with cohesion, coupling, and dependency injection as supporting concepts. Does not cover the Open-Closed or Liskov principles - those follow in the next chapters.

Use for definitions, the refactoring walkthrough, and the end-of-chapter checklist; principles and methods are listed with page locators in the topics file.
```

Non-leaf folder (fund research root):

```
# Fund Research

Research collection maintained by the investment team: factsheets downloaded from fund providers, internal analyst notes, and price series from the fund administrator.

One folder per tracked fund. Factsheets are transcribed PDFs with their tables extracted; analyst notes are native markdown; prices are CSV.

Covers funds under active review with their available history. Funds sold or dropped from review are archived elsewhere and not present here.

Use for fee, holdings, liquidity, and drawdown questions on a single fund; cross-fund comparison needs the data files of each fund folder.
```

Non-leaf folder (correspondence archive root):

```
# Correspondence Archive

Scanned incoming and outgoing paper correspondence of a small company - letters, invoices, credit notes, official notices - digitized from the physical files.

One document per scan with a page-by-page transcription; scans kept alongside for signatures, stamps, and layout. Grouped by calendar year.

Covers the years present as folders. Email and digital-native documents are not part of this archive.

Use for questions about what was agreed, invoiced, disputed, or decided with a counterparty; contacts, amounts, deadlines, and decisions are listed per year in the topics files.
```

Note what is absent from every example: no counts, no "latest", no file names, no figures. Adding a 2021 folder to the archive changes the root inventory by one line and triggers one summary regeneration; adding 200 scans to `2020/` changes `2020/_inventory.md` by 200 lines and nothing else.

### _topics.md Format

Plain markdown. One `##` heading per category, one list item per entry, one nested list item per locator. Entry grammar:

```
- Name: statement
  - `locator`
  - `locator`
```

- `Name` - the term as the source uses it; for acronyms the short form
- `statement` - one self-contained sentence or fragment; for acronyms the expansion; for keywords MAY be empty (`- Name`)
- Locators - one per nested line, inline code, relative to the folder (see Key Mechanisms, Locators). At least one per entry. No duplicates within an entry. Order not significant
- One locator per line is deliberate: agents add or remove sources by inserting or deleting whole lines; the entry line is never rewritten when sources change, and diffs show exactly which source moved
- Categories are `##` headings and form an open set. Knowledge extraction: Concepts, Principles, Methods, Keywords, Acronyms, Facts, Conclusions, Hypotheses, Problems, Solutions, Ideas. Operational material: Contacts, Todos, Decisions, Deadlines, Amounts, Open Questions, Risks, Requirements. Use the headings the consumer needs, omit headings without entries
- No other formatting: no bold, no third list level, no blank lines inside an entry

Example:

```
# Topics: Chapter Name

## Principles

- Single Responsibility: a class should have one reason to change
  - `CleanCode-01_Page047.md`
- Open-Closed: open for extension, closed for modification
  - `guides/architecture.md#open-closed`

## Methods

- Dependency Injection: pass dependencies as constructor parameters, never create them internally
  - `CleanCode-02_Page048.md`
  - `guides/architecture.md#L120-L140`

## Keywords

- Cohesion
  - `guides/architecture.md#cohesion`
- Coupling
  - `guides/architecture.md#cohesion`
  - `CleanCode-02_Page048.md`

## Acronyms

- SRP: Single Responsibility Principle
  - `CleanCode-01_Page047.md`
- DI: Dependency Injection
  - `CleanCode-02_Page048.md`

## Facts

- Top holding weight 4.2% as of 2025-06-30
  - `Factsheet_2025-Q2.md#page=2`

## Conclusions

- Thin secondary market makes exits above 2% of daily volume take weeks
  - `AnalystNote_2025-06.md#liquidity`

## Hypotheses

- Staggering exits over ten trading days keeps single-day volume under 15% of turnover
  - `AnalystNote_2025-06.md#liquidity`

## Ideas

- Publish factsheet tables as machine-readable CSV alongside the PDF
  - `Transcript.md#t=00:41:10`
```

Folders with nothing to extract: the file contains the single line `No topics.`

Merged topic list (folder that holds only folders), produced by code from the direct children's `_topics.md`:
- Title: `# Topics: [folder title]`
- Categories: union of the children's `##` headings, in first-seen order
- Entries: one per distinct `Name` within a category; first statement encountered is kept, locators of all same-name entries concatenated in child order
- Locators: each child locator prefixed with the child folder name and `/` - `Page047.md#srp` in `01_Chapter/` becomes `01_Chapter/Page047.md#srp`
- Children whose `_topics.md` reads `No topics.` contribute nothing; if all do, the merged file reads `No topics.`

Example, merged from `01_Principles/` and `02_Practices/`:

```
# Topics: Part One

## Principles

- Single Responsibility: a class should have one reason to change
  - `01_Principles/CleanCode-01_Page047.md`
  - `02_Practices/Refactoring_Page112.md#srp-in-practice`

## Methods

- Dependency Injection: pass dependencies as constructor parameters, never create them internally
  - `01_Principles/CleanCode-02_Page048.md`

## Keywords

- Cohesion
  - `01_Principles/guides/architecture.md#cohesion`
  - `02_Practices/Refactoring_Page115.md`
```

Example, scanned correspondence (one year):

```
# Topics: Correspondence 2019

## Facts

- Invoice 0412 total 4,812.50 EUR, due 2019-06-29
  - `2019-05-30_Invoice_0412.md`
- Credit note 0412-C issued 2019-08-14 for 1,200.00 EUR
  - `2019-08-14_CreditNote_Supplier.md`

## Problems

- Delivered quantity 40 units below order 2019-0412
  - `2019-06-03_Letter_Supplier.md#page=1`

## Solutions

- Partial credit instead of re-delivery, accepted 2019-08-02
  - `2019-08-02_Letter_Supplier.md`
  - `2019-08-14_CreditNote_Supplier.md`

## Keywords

- Retention of title
  - `2019-02-11_Letter_Supplier.md#page=2`

## Acronyms

- AGB: Allgemeine Geschäftsbedingungen (general terms and conditions)
  - `2019-02-11_Letter_Supplier.md#page=2`
```

Example, financial data folder:

```
# Topics: FundAlpha

## Facts

- Total expense ratio 0.85% p.a.
  - `Factsheet_2025-Q1.md#page=1`
  - `Factsheet_2025-Q2.md#page=1`
- Fund size 412 million EUR as of 2025-06-30
  - `Factsheet_2025-Q2.md#page=1`
- Max drawdown 2020-03: -31.4%
  - `Prices_2020-2025.csv#cell=B58:B79`

## Conclusions

- Recovery to pre-drawdown level took 9 months
  - `Prices_2020-2025.csv#cell=B79:B268`
  - `AnalystNote_2025-06.md#recovery`

## Hypotheses

- Distribution yield above 3% attracts inflows in the following quarter
  - `AnalystNote_2025-06.md#flows`

## Methods

- Staggered exit: sell over ten trading days, cap at 15% of average daily turnover
  - `AnalystNote_2025-06.md#liquidity`
```

Example, native code documentation folder:

```
# Topics: guides

## Concepts

- Workspace: a folder holding one or more services with a shared toolchain
  - `setup.md#workspace`
- Service manifest: `service.yaml` declaring ports, env, dependencies
  - `architecture.md#service-manifest`

## Methods

- Bootstrap: run `./bootstrap.sh --env dev` before first build
  - `setup.md#L40-L58`
- Hot reload: `make watch` rebuilds on file change
  - `setup.md#hot-reload`

## Principles

- Every service owns its schema; no cross-service table access
  - `architecture.md#data-ownership`

## Problems

- Port collisions when two services default to 8080
  - `setup.md#troubleshooting`

## Solutions

- Override with `PORT` env var per service
  - `setup.md#troubleshooting`
  - `architecture.md#L212-L220`

## Acronyms

- ADR: Architecture Decision Record
  - `architecture.md#decisions`
```

Example, consumer-defined categories (project correspondence folder used by an assistant agent):

```
# Topics: Project Delta 2026-Q3

## Contacts

- Jane Smith: project lead at Supplier GmbH, decides on delivery schedule
  - `2026-07-02_Kickoff_Minutes.md#attendees`
  - `2026-08-19_Email_Supplier.md`
- Max Mustermann: our procurement contact for contract changes
  - `2026-07-02_Kickoff_Minutes.md#attendees`

## Decisions

- Phase 2 starts only after acceptance of Phase 1 test report
  - `2026-07-02_Kickoff_Minutes.md#decisions`
  - `2026-08-19_Email_Supplier.md#L14-L22`

## Todos

- Send signed change request CR-07 to Supplier GmbH
  - `2026-08-19_Email_Supplier.md#L30`
- Book acceptance test slot in week 38
  - `2026-09-01_Statusreport.md#next-steps`

## Deadlines

- 2026-09-15: Phase 1 test report due
  - `2026-07-02_Kickoff_Minutes.md#milestones`
  - `2026-09-01_Statusreport.md#milestones`

## Amounts

- CR-07 adds 18,400.00 EUR to the contract
  - `2026-08-19_Email_Supplier.md#L18`

## Open Questions

- Who covers freight for the replacement units
  - `2026-08-19_Email_Supplier.md#L26`
```

Example, nothing to list (folder of raw price series):

```
No topics.
```

### .data.md and _data.md Format

Plain markdown. One `##` heading per data unit, one `Origin:` line, one list item per locator, one fenced code block. Unit grammar:

````
## Title

Origin: origin[ | source label]

- `locator`
- `locator`

```lang
...data...
```
````

- `Title` - name of the data unit; the source's own caption when it has one
- `Origin:` line - origin (`table`, `chart`, `figure`, `image`, `inline`), optional label the source assigns (`Table 1`, `Figure 3`, `Listing 2`)
- Locators - one per list line, inline code, relative to the folder. At least one per unit. Same rationale as in `_topics.md`: sources change by inserting or deleting whole lines
- `lang` - fence info string: `csv`, `json`, `xml`, `bash`, `python`, `text`, ... - the only place the data type is stated
- CSV units are normalized: `,` column separator, `.` decimal separator, no thousands separator, first row is the header
- In `_data.md` (folder-level), the locators on each unit name its documents; otherwise identical

Example `Factsheet_2025-Q2.data.md`:

````
# Data: Factsheet_2025-Q2

## Top Holdings

Origin: table | Table 1

- `Factsheet_2025-Q2.md#page=2`

```csv
Holding,Weight
Alpha Corp,4.2
Beta Ltd,3.9
```

## Service Topology

Origin: figure | Figure 2

- `Factsheet_2025-Q2.md#page=5`

```json
{
  "nodes": ["Client", "API", "Database"],
  "edges": [["Client", "API"], ["API", "Database"]]
}
```
````

Example `README.data.md` (native document, code extracted):

````
# Data: README

## Build and Bootstrap

Origin: inline

- `README.md#L40-L58`

```bash
./bootstrap.sh --env dev
./build.sh
```
````

Example `Slide-07.data.md` (chart read into CSV, diagram into XML):

````
# Data: Slide-07

## Monthly Active Users 2025

Origin: chart | Figure 1

- `Slide-07.md`

```csv
Month,Users
2025-01,12400
2025-02,13100
2025-03,15800
```

## Request Lifecycle

Origin: figure | Figure 2

- `Slide-07.md`

```xml
<diagram type="flowchart">
  <node id="client" label="Client"/>
  <node id="api" label="API"/>
  <node id="db" label="Database"/>
  <edge from="client" to="api"/>
  <edge from="api" to="db"/>
</diagram>
```
````

Example `2019-05-30_Invoice_0412.data.md` (scanned invoice, line items):

````
# Data: 2019-05-30_Invoice_0412

## Line Items

Origin: table

- `2019-05-30_Invoice_0412.md#page=1`

```csv
Pos,Description,Qty,Unit,UnitPrice,Total
1,Steel bracket type A,200,pcs,12.50,2500.00
2,Mounting kit,200,pcs,8.75,1750.00
3,Freight,1,flat,562.50,562.50
```

## Payment Terms

Origin: inline

- `2019-05-30_Invoice_0412.md#page=1`

```text
Net 30 days, 2% discount within 10 days
```
````

Example `_data.md` (folder-level consolidation across factsheets):

````
# Data: FundAlpha

## Top Holdings by Quarter

Origin: table

- `Factsheet_2025-Q1.md#page=2`
- `Factsheet_2025-Q2.md#page=2`

```csv
Quarter,Holding,Weight
2025-Q1,Alpha Corp,3.9
2025-Q1,Beta Ltd,3.7
2025-Q2,Alpha Corp,4.2
2025-Q2,Beta Ltd,3.9
```

## Fund Size by Quarter

Origin: inline

- `Factsheet_2025-Q1.md#page=1`
- `Factsheet_2025-Q2.md#page=1`

```csv
Quarter,SizeMillionEUR
2025-Q1,388
2025-Q2,412
```
````

In `_data.md`, a unit that merges several documents lists one locator line per document.

### _inventory.md Format

Plain markdown: `#` title, then one list item per direct child folder and per document. Nothing else.

```
# Folder Title

- `01_FolderName/` - purpose
- `02_FolderName/` - purpose
- `Document-01.md` - purpose
- `Document-02.md` - purpose
```

- Line grammar: `- \`name\` - purpose`. Folder names end with `/`. Purpose is one line and MAY carry a range (pages, dates) or a count for a folder
- Listed: child folders that are bundles, documents
- Not listed: `_summary.md`, `_topics.md`, `_metadata.json`, `_data.md`, `.data.md` files, asset folders (`_images/` ...), native relative-asset subfolders. All of these follow from the format or from a document's name
- Not contained: metadata lines, table of contents, prose, headings below `#`
- Order: SHOULD follow the folder's sort order so the file mirrors a directory listing
- Update cost: one line per child event. Line count equals the number of payload children, which makes a missing or stale line detectable by a directory comparison

Root of a transcribed book:

```
# Source Material Title

- `00_FrontMatter/` - title page, copyright, table of contents, pages i-xii
- `01_PartName/` - first part, pages 001-140
- `02_PartName/` - second part, pages 141-310
- `99_BackMatter/` - index and bibliography, pages 311-330
```

Chapter folder of a transcribed book:

```
# 01_ChapterName

- `Topic-01_Page001.md` - chapter opening, motivation, page 001
- `Topic-02_Page002.md` - billing module before refactoring, page 002
- `Topic-03_Page003.md` - first split of responsibilities, page 003
```

Scanned correspondence for one year:

```
# Correspondence 2019

- `2019-02-11_Letter_Supplier.md` - supplier terms and conditions, 2 pages
- `2019-05-30_Invoice_0412.md` - supplier invoice 0412
- `2019-06-03_Letter_Supplier.md` - complaint about short delivery
- `2019-08-02_Letter_Supplier.md` - settlement proposal
- `2019-08-14_CreditNote_Supplier.md` - credit note 0412-C
```

Wiki export, one year folder with native documents (the relative-asset subfolder `2024-03-15_PostTitle/` is not listed):

```
# Engineering Wiki 2024

- `2024-03-15_PostTitle.md` - deployment checklist for the new cluster
- `2024-06-02_PostTitle.md` - incident review, June outage
- `2024-11-20_PostTitle.md` - migration guide to the v2 API
```

Data collection root:

```
# Fund Research

- `FundAlpha/` - factsheets, analyst note, prices for FundAlpha
- `FundBeta/` - factsheets and prices for FundBeta
```

Fund folder with native and transcribed documents (`_data.md`, `.data.md` files, and `_pdf/` are not listed):

```
# FundAlpha

- `Prices_2020-2025.csv` - daily closing prices, adjusted
- `AnalystNote_2025-06.md` - liquidity and flow analysis
- `Factsheet_2025-Q1.md` - transcribed factsheet Q1 2025
- `Factsheet_2025-Q2.md` - transcribed factsheet Q2 2025
```

Adding a Q3 factsheet to this folder is one inserted line here, one `.data.md` file, topic lines, and nothing in `_summary.md`.

## 12. Logging Requirements

N/A: this is a file format specification with no runtime, console output, or service component. The format carries no process logs (IPPSKBNDL-FR-12); tools that produce or consume bundles define their own logging in their specs and keep it outside the bundle.

## 13. Technical Constraints

- All generated files are text-based (`.md`, `.json`) for git compatibility and text search
- Format-generated binaries are isolated in asset folders; native documents keep their relative assets
- `.gitignore` pattern for asset folders is environment-specific (not mandated by format spec)
- Generated file extensions are lowercase (`.md`, `.json`, `.data.md`, `.zip`); documents keep their original extension
- Names are safe for file systems and .zip archives (no path separators, no reserved characters)
- Numbers in ordering prefixes are zero-padded so lexical sort equals intended order; width grows with the collection
- No format file stores process records; the format imposes no production pipeline, settings, or quality thresholds