# SPEC: Workspace Setup Schema and Workflow Redesign

**Doc ID**: WSKMGMT-SP02
**Feature**: workspace-setup-schema
**Goal**: Specify a flat field schema for workspace setup configuration that unifies questionnaire, report template, and workflow use cases (verify, sync, analysis) with conditional logic and typed fields
**Timeline**: Created 2026-09-08, Updated 0 times

**Target file(s)**:
- `DevSystemV4.3/skills/workspace-management/WORKSPACE_SETUP_QUESTIONNAIRE.md` (renamed from WORKSPACE_CREATION_QUESTIONNAIRE.md)
- `DevSystemV4.3/skills/workspace-management/WORKSPACE_SETUP_REPORT_TEMPLATE.md` (new)
- `DevSystemV4.3/skills/workspace-management/SKILL.md` (add Procedures 6 and 7, update References)
- `DevSystemV4.3/workflows/workspace-setup.md` (rewrite with 5 use cases)
- `DevSystemV4.3/workflows/compare-workspace-setup.md` (new workflow for compare use case)
- `DevSystemV4.3/workflows/workspace-create.md` (deprecated, deleted in sync targets)
- `specs/_SPEC_WORKSPACE-MANAGEMENT_SKILL.md [WSKMGMT-SP01]` (amend FR-42, add FR-65 to FR-72)
- `[WORKSPACE_FOLDER]\devsystem-sync.json` (add workspace-create.md to deprecated array)
- `README.md` (update workflow reference)

**Depends on:**
- `_SPEC_WORKSPACE-MANAGEMENT_SKILL.md [WSKMGMT-SP01]` for workspace management skill architecture, existing FRs, and design decisions
- `DevSystemV4.3/skills/workspace-management/WORKSPACE_CREATION_QUESTIONNAIRE.md` for existing questionnaire sections and fields

**Does not depend on:**
- Any UI framework or runtime (schema is markdown-based, consumed by LLM agent)

## MUST-NOT-FORGET

- Schema fields use flat registry with ID references — no nesting, no tree traversal
- Condition syntax supports only `==` and `AND` — no OR, no negation, keeps evaluation trivial for LLM
- Field ordering is significant — conditions always reference earlier field IDs (top-to-bottom evaluation)
- Report template and questionnaire share the same field IDs — harmonization is structural, not by convention
- List fields use set comparison (missing/extra), not ordered comparison — lists are unordered patterns
- `DEVIATION` status is a valid user choice, not a gap — do not auto-fix deviations
- `N/A` status means field condition not met — omit from gap count, do not report as missing
- Privacy gate: all schema examples use generic placeholders ([myapp], [appname], [version])
- Workflow stays thin — dispatches to skill procedures, does not embed logic
- Rename is global — all references in SPEC, SKILL.md, workflow, README.md, and sync targets updated
- `workspace-create.md` in `.devin/workflows/` is deprecated and must be deleted during next sync
- Existing `/verify workspace` context (FR-27) and `/workspace-setup verify` share the same verification logic — `/workspace-setup verify` is an alternative entry point, not a separate implementation

## Table of Contents

1. [Scenario](#1-scenario)
2. [Context](#2-context)
3. [Domain Objects](#3-domain-objects)
4. [Functional Requirements](#4-functional-requirements)
5. [Non-Functional Requirements](#5-non-functional-requirements)
6. [Design Decisions](#6-design-decisions)
7. [Implementation Guarantees](#7-implementation-guarantees)
8. [Key Mechanisms](#8-key-mechanisms)
9. [Action Flow](#9-action-flow)
10. [Data Structures](#10-data-structures)
11. [User Actions](#11-user-actions)
12. [UX Design](#12-ux-design)
13. [Logging Requirements](#13-logging-requirements)
14. [Technical Constraints](#14-technical-constraints)
15. [Document History](#15-document-history)

## 1. Scenario

**Problem:** The workspace setup workflow (`workspace-setup.md`) currently supports only creation (interactive questionnaire). Users need to verify existing workspaces against defaults, sync setup configuration between repos, and analyze current setup state. The questionnaire (`WORKSPACE_CREATION_QUESTIONNAIRE.md`) and any reporting format are not harmonized — there is no shared schema ensuring the same fields, types, and conditions appear in both. Conditional logic (IF → THEN) and typed fields (single values vs lists) are not formally specified, making consistent comparison impossible.

**Solution:**
- Define a flat field schema with metadata (type, condition, default) as a section in the questionnaire
- Create `WORKSPACE_SETUP_REPORT_TEMPLATE.md` referencing the same field IDs for standardized reporting
- Redesign `workspace-setup.md` with 4 use cases: verify, sync from source, sync to target, default analysis
- Add Procedure 6 (Setup Analysis) to SKILL.md — reuses existing Procedures 2 and 4 for sync and verify
- Rename `WORKSPACE_CREATION_QUESTIONNAIRE.md` → `WORKSPACE_SETUP_QUESTIONNAIRE.md`
- Deprecate `workspace-create.md` in sync targets

**What we don't want:**
- Nested schema structures requiring tree traversal — flat registry with ID references only
- Complex condition syntax (OR, negation, nested predicates) — simple `==` and `AND` only
- Report template that duplicates field definitions instead of referencing the schema
- Thick workflow with embedded logic — workflow dispatches to skill procedures
- Separate verification logic for `/workspace-setup verify` and `/verify workspace` — same logic, different entry points
- Schema that cannot express conditional fields (fields only applicable when prior fields have specific values)
- Schema that cannot distinguish single values from list/array values

## 2. Context

The existing workspace management skill (WSKMGMT-SP01) defines a comprehensive set of FRs for workspace compare, update, rollback, and integrity operations. The `WORKSPACE_CREATION_QUESTIONNAIRE.md` provides 7 sections of interactive questions for workspace creation, each with defaults and impact descriptions. However:

- The questionnaire has no formal schema — fields are embedded in prose code blocks
- No report template exists for standardized workspace analysis output
- The workflow only supports creation, not verification or setup sync
- Conditional logic (e.g., "if WORKSPACE mode, ask Section 2") is expressed in HTML comments, not a machine-readable format
- Field types (single value vs list) are implicit, not declared

This SPEC defines the schema format, report template, and workflow redesign to address these gaps. It amends WSKMGMT-SP01 rather than replacing it — all existing FRs remain valid unless explicitly amended.

### Relationship to WSKMGMT-SP01

```
WSKMGMT-SP01 (existing)
├── FR-01 to FR-60: Core skill, sync, verify, commit, creation
├── FR-42: workspace-setup.md workflow (creation only)
│
└── WSKMGMT-SP02 (this SPEC)
    ├── Amends FR-42: 4 use cases (verify, sync from, sync to, analysis)
    ├── FR-65: Setup schema in questionnaire
    ├── FR-66: Report template
    ├── FR-67: Procedure 6 (Setup Analysis)
    ├── FR-68: Verify use case
    ├── FR-69: Sync from source use case
    ├── FR-70: Sync to target use case
    ├── FR-71: Default analysis use case
    └── FR-72: File renames and deprecation
```

## 3. Domain Objects

### SetupField

A **SetupField** is a single configurable setting in the workspace setup schema.

**Storage:** `## Setup Schema` section in `WORKSPACE_SETUP_QUESTIONNAIRE.md`
**Key properties:**
- `id` - unique field identifier (format: `[section]-[letter]`, e.g., `1a-workspace_type`)
- `type` - field type: `single`, `list`, or `enum`
- `condition` - applicability expression (references prior field IDs with `==` and `AND`)
- `default` - default value (single value, enum option, or JSON array for list type)
- `report_label` - display label in report template
- `options` - for enum type: list of valid values

### SetupSchema

A **SetupSchema** is the ordered collection of all SetupField entries.

**Storage:** `## Setup Schema` section in `WORKSPACE_SETUP_QUESTIONNAIRE.md`
**Key properties:**
- `fields` - ordered list of SetupField entries (ordered by section number)
- `version` - schema version for backward compatibility tracking

### SetupReport

A **SetupReport** is the output of workspace analysis, generated from the schema.

**Storage:** Generated to chat (not persisted as file)
**Key properties:**
- `summary` - counts: total fields, OK, gaps, stale, deviations, N/A
- `sections` - per-section results with field-level status
- `list_details` - expanded details for list fields (missing/extra items)

### FieldStatus

A **FieldStatus** is the evaluation result for a single field in a report.

**Key properties:**
- `OK` - current matches default or is a valid customization
- `GAP` - required field missing or incomplete (list missing required items)
- `STALE` - value present but outdated (e.g., DevSystem version mismatch)
- `DEVIATION` - value differs from default but is a valid user choice (not a gap)
- `N/A` - field condition not met (e.g., binary_path when binary_build=no)

## 4. Functional Requirements

### Schema Definition

**WSKMGMT-FR-65: Setup schema in questionnaire**
- Add `## Setup Schema` section to `WORKSPACE_SETUP_QUESTIONNAIRE.md` (renamed from WORKSPACE_CREATION_QUESTIONNAIRE.md)
- Schema contains all fields from questionnaire sections 1-6, expressed as flat SetupField entries
- Each field has: id, type (single/list/enum), condition, default, report_label, options (enum only)
- Fields are ordered by section number — conditions always reference earlier field IDs
- Condition syntax: `==` for equality, `AND` for conjunction, `(always)` for unconditional fields
- No OR, no negation, no nested predicates — evaluation is trivial for LLM
- Schema is the single source of truth — report template references field IDs, not duplicate definitions
- Privacy gate compliant: all default values use generic placeholders

**WSKMGMT-FR-66: WORKSPACE_SETUP_REPORT_TEMPLATE.md**
- New file in `DevSystemV4.3/skills/workspace-management/`
- Report structure mirrors questionnaire sections 1-6 using same field IDs
- Per-section table: Field ID | Current | Default | Status | Proposed Fix
- Summary section: workspace type, mode, sync relationship, counts (OK/GAP/STALE/DEVIATION/N/A)
- List field details section: expanded missing/extra items for list-type fields
- Status values: OK, GAP, STALE, DEVIATION, N/A (see FieldStatus domain object)
- Template is a guide for report generation, not a fill-in form — agent generates report in chat following the structure
- Harmonized with questionnaire: same field IDs, same sections, same condition logic

### Skill Procedure

**WSKMGMT-FR-67: Procedure 6 (Setup Analysis) in SKILL.md**
- New Core Procedure added to SKILL.md Intent Lookup and Core Procedures
- Intent: "Analyze workspace setup and generate report" → Procedure 6
- Steps:
  1. Load `WORKSPACE_SETUP_QUESTIONNAIRE.md` schema section
  2. Detect current workspace type and mode (reuse detection from Procedure 4)
  3. For each field in schema (top-to-bottom):
     a. Evaluate condition — if not met, mark N/A and skip
     b. Read current value from workspace (NOTES.md, devsystem-sync.json, folder structure)
     c. Compare against default
     d. Assign status: OK, GAP, STALE, DEVIATION, or N/A
  4. Generate report following `WORKSPACE_SETUP_REPORT_TEMPLATE.md` structure
  5. Output report to chat
- Does not execute changes — analysis only
- List field comparison: set difference (missing = in default not in current, extra = in current not in default)
- Enum field comparison: validate current is a valid option, compare against default
- Single field comparison: string equality with default

### Workflow Use Cases

**WSKMGMT-FR-68: `/workspace-setup verify` use case**
- Compares current workspace against schema defaults and templates
- Main question: "Is everything correctly set up?"
- Detects: stale configuration, missing components and constants, deviations from templates and recommendations
- Calls @skills:workspace-management Procedure 4 (Integrity Check, existing) with setup-specific scoping
- Procedure 4 enhanced: reads schema fields in addition to WORKSPACE-RULES.md
- Proposes changes in chat — does not execute by default
- Previews proposed changes with field-level detail
- Executes if user responds with @rules:core-conventions.md [CONFIRMATION_KEYWORDS]
- Non-confirmation: aborts, no changes made
- Amends FR-27 (`/verify workspace`): Procedure 4 enhanced with schema-awareness — reads schema fields from WORKSPACE_SETUP_QUESTIONNAIRE.md in addition to WORKSPACE-RULES.md. `/verify workspace` and `/workspace-setup verify` are alternative entry points to the same enhanced logic and produce identical results

**WSKMGMT-FR-69: `/workspace-setup sync from [source]` use case**
- Analyzes workspace setup in source repo, compares with current workspace
- Syncs setup changes FROM source TO current
- Setup content = NOTES.md workspace constants, devsystem-sync.json, folder structure
- Calls @skills:workspace-management Procedure 2 (Update, existing) with setup-specific scoping
- Procedure 2 scoped to setup files only (not DevSystem content, not knowledge bundles)
- Proposes changes in chat — does not execute by default
- Previews: fields to add, fields to modify, fields to remove (with reason)
- Executes if user responds with @rules:core-conventions.md [CONFIRMATION_KEYWORDS]
- Merge strategy: source values win for fields that exist in both, current-only fields are preserved
- List fields: union of source and current items (additive merge, no removal)

**WSKMGMT-FR-70: `/workspace-setup sync to [target]` use case**
- Analyzes workspace setup in target repo, compares with current workspace
- Syncs setup changes FROM current TO target
- Same logic as FR-69 with reversed direction (current is source, target is destination)
- Calls @skills:workspace-management Procedure 2 with swapped source/target
- Same preview/confirm/execute flow as FR-69, same @rules:core-conventions.md [CONFIRMATION_KEYWORDS]
- Same merge strategy: current values win for fields that exist in both, target-only fields preserved

**WSKMGMT-FR-71: `/workspace-setup [instructions]` use case (default)**
- If instructions provided: execute instructions and settings
- If no instructions or settings: analyze and detect current workspace setup
- Default analysis calls Procedure 6 (Setup Analysis, FR-67)
- Compares with defaults and questionnaire schema
- Writes full analysis report into chat following `WORKSPACE_SETUP_REPORT_TEMPLATE.md`
- Does not propose changes or execute — pure analysis output
- If user wants changes after reading report: runs `/workspace-setup verify` or `/workspace-setup sync`

### File Renames and Deprecation

**WSKMGMT-FR-72: Rename and deprecate files**
- Rename `WORKSPACE_CREATION_QUESTIONNAIRE.md` → `WORKSPACE_SETUP_QUESTIONNAIRE.md` in:
  - `DevSystemV4.3/skills/workspace-management/` (source)
  - `.devin/skills/workspace-management/` (sync target, updated via sync)
  - All references in SKILL.md, SPEC, workflow, README.md
- Deprecate `workspace-create.md`:
  - Already renamed to `workspace-setup.md` in `DevSystemV4.3/workflows/`
  - Old `workspace-create.md` in `.devin/workflows/` is stale sync copy
  - Add `workspace-create.md` to `deprecated` array in `devsystem-sync.json` so sync deletes it
  - Update SPEC WSKMGMT-SP01 FR-42 to reflect new workflow scope (amend existing FR)
- Update `README.md` workflow reference (already says `workspace-setup` — verify link target)
- Update all internal references from `WORKSPACE_CREATION_QUESTIONNAIRE` to `WORKSPACE_SETUP_QUESTIONNAIRE` across:
  - `DevSystemV4.3/workflows/workspace-setup.md`
  - `DevSystemV4.3/skills/workspace-management/SKILL.md`
  - `specs/_SPEC_WORKSPACE-MANAGEMENT_SKILL.md`
  - `.devin/` copies (via sync)

### Compare Use Case

**WSKMGMT-FR-73: compare-workspace-setup.md workflow**
- New workflow file in `DevSystemV4.3/workflows/compare-workspace-setup.md`
- Follows WORKFLOW_TEMPLATE.md structure (WF-HD-01 through WF-BR-04)
- Thin workflow — dispatches to Procedure 7 in SKILL.md, no embedded comparison logic
- Frontmatter: description, auto_execution_mode
- Goal: compare workspace settings between two workspaces using schema
- MUST-NOT-FORGET: load schema from questionnaire, agent reads prose NOTES.md (not script), thin workflow, @rules:core-conventions.md [CONFIRMATION_KEYWORDS]
- Required Skills: @skills:workspace-management
- Prerequisites: target workspace path provided in [instructions]
- Steps: load schema, read workspace A (current), read workspace B (target from path), dispatch to Procedure 7 for comparison, generate diff report
- Diff status values: MATCH, DIFF, ONLY_A, ONLY_B, N/A (distinct from verify statuses)
- Output: diff report in chat with per-field comparison and summary counts
- No Context Match fallback: if no target path provided, ask user
- Verification: all applicable schema fields covered, both workspaces read correctly

**WSKMGMT-FR-74: Procedure 7 Compare Workspace Setup in SKILL.md**
- New Procedure 7 in workspace-management SKILL.md
- Steps: load schema from WORKSPACE_SETUP_QUESTIONNAIRE.md, read workspace A (NOTES.md + devsystem-sync.json + folder structure), read workspace B from provided path, compare field-by-field using schema, generate diff report
- Agent is the comparison engine — reads prose NOTES.md directly, evaluates conditions, assigns semantic status
- No script or regex parsing — LLM extraction from prose markdown
- Diff status values: MATCH (identical), DIFF (both have value, different), ONLY_A (only in workspace A), ONLY_B (only in workspace B), N/A (condition not met for this workspace type)
- For list fields: compare as sets (common, only-A, only-B)
- Report follows WORKSPACE_SETUP_REPORT_TEMPLATE.md structure adapted for two-workspace comparison
- Does not modify either workspace — analysis only
- If user requests applying differences after report: dispatch to Procedure 2 (Update) with appropriate direction

**WSKMGMT-FR-75: `/workspace-setup compare [instructions]` use case**
- Called by `/workspace-setup compare [path]` or `/workspace-setup compare [instructions]`
- [path] = filesystem path to target workspace
- [instructions] = natural language instructions (e.g., "compare with the repo at ../OtherProject")
- Dispatches to Procedure 7 via compare-workspace-setup.md workflow
- Generates diff report showing per-field comparison between current and target workspace
- Report shows: field ID, workspace A value, workspace B value, status (MATCH/DIFF/ONLY_A/ONLY_B/N/A)
- Summary: counts per status, total fields compared, fields skipped (N/A)
- Does not modify either workspace without @rules:core-conventions.md [CONFIRMATION_KEYWORDS]
- If target workspace missing NOTES.md or devsystem-sync.json: report GAP status for affected fields, continue comparison
- After report: user can request `/workspace-setup sync from [path]` or `/workspace-setup sync to [path]` to apply differences

## 5. Non-Functional Requirements

**WSKMGMT-NFR-09: Schema evaluation performance**
- Schema evaluation (all fields, top-to-bottom) must complete within 5 seconds for the full field set (~30 fields)
- Verification method: timed evaluation of schema against a fully configured workspace

**WSKMGMT-NFR-10: Schema readability**
- Schema must be readable by LLM agent without parsing tools — plain markdown with structured entries
- Each field entry fits in 5-8 lines (id, type, condition, default, report_label, options)
- Verification method: manual review by agent — no parser needed

**WSKMGMT-NFR-11: Report consistency**
- Report generated from schema must use the same field IDs, sections, and condition logic as the questionnaire
- No field appears in report that is not in schema — no field in schema is omitted from report
- Verification method: cross-check field IDs between schema section and report template

**WSKMGMT-NFR-12: Backward compatibility with existing questionnaire**
- Existing questionnaire sections 1-6 remain unchanged in content — schema section is additive
- Questionnaire flow (present questions section by section) works identically before and after schema addition
- Verification method: run workspace creation flow with and without schema section

## 6. Design Decisions

**WSKMGMT-DD-22:** Flat field registry with ID references, not nested tree. Rationale: Nested structures require tree traversal, which is error-prone for LLM agents. Flat registry with condition references to prior field IDs enables simple top-to-bottom evaluation. Fields are ordered by section number, guaranteeing conditions always reference already-evaluated fields.

**WSKMGMT-DD-23:** Condition syntax limited to `==` and `AND`. Rationale: OR and negation introduce ambiguity in evaluation order and make condition chains harder to trace. The questionnaire's conditional sections (e.g., "if WORKSPACE mode, ask Section 2") are all expressible with `==` and `AND`. Keeping the syntax minimal ensures LLM can evaluate conditions reliably without a parser.

**WSKMGMT-DD-24:** Three field types only: `single`, `list`, `enum`. Rationale: These cover all questionnaire field types. `single` for strings/paths/names. `list` for arrays (never_overwrite patterns, knowledge bundles). `enum` for finite option sets (workspace type, mode, version source). No `object` or `nested` type — complexity is unnecessary for workspace configuration.

**WSKMGMT-DD-25:** List fields use set comparison (missing/extra), not ordered comparison. Rationale: Lists in workspace configuration (never_overwrite patterns, knowledge bundles) are unordered sets. Comparing as sets (items in default not in current = missing, items in current not in default = extra) is the correct semantic. Order does not matter.

**WSKMGMT-DD-26:** `DEVIATION` is a valid user choice, not a gap. Rationale: Users legitimately choose non-default values (e.g., WORKSPACE mode instead of SINGLE-PROJECT). Reporting these as gaps would prompt unnecessary fixes. DEVIATION status informs the user without suggesting action. Only GAP and STALE trigger proposed fixes.

**WSKMGMT-DD-27:** Report template references schema field IDs, not duplicate definitions. Rationale: Duplicating field definitions in both questionnaire and report template creates drift risk. The template defines report structure (sections, columns, status values) and references field IDs from the schema. The agent reads the schema for field details and the template for report format.

**WSKMGMT-DD-28:** `/workspace-setup verify` reuses Procedure 4 (Integrity Check), not a new procedure. Rationale: Procedure 4 already verifies workspace constants, files, and structure against rules and templates. Adding schema-awareness to Procedure 4 (reading schema fields in addition to WORKSPACE-RULES.md) extends it without duplication. `/workspace-setup verify` and `/verify workspace` are alternative entry points to the same logic.

**WSKMGMT-DD-29:** `/workspace-setup sync from/to` reuses Procedure 2 (Update), scoped to setup files. Rationale: Procedure 2 already handles sync preview/confirm/execute flow. Scoping it to setup files (NOTES.md, devsystem-sync.json, folder structure) instead of DevSystem content or knowledge bundles reuses the existing flow. The merge strategy (source wins for shared fields, preserve target-only fields) is a new parameter to Procedure 2, not a new procedure.

**WSKMGMT-DD-30:** Schema section added to questionnaire, not as separate file. Rationale: The questionnaire is the natural home for field definitions — it already contains the questions, defaults, and impact descriptions. A separate schema file would duplicate the field list and create drift. Adding a `## Setup Schema` section makes the questionnaire dual-purpose: interactive guide during creation, structured schema during analysis/verify/sync.

**WSKMGMT-DD-31:** Agent is the comparison engine for workspace diff, not a script. Rationale: NOTES.md is prose markdown designed for human and LLM consumption. Parsing `[DEV_REPO_FOLDER] -> usually called [Product]-Dev` with regex is fragile — every format variation breaks the parser. LLMs excel at extracting structured data from prose. The agent evaluates conditions (`1a == SOFTWARE-DEV AND 2c == SYNCED`), assigns semantic status (MATCH/DIFF/ONLY_A/ONLY_B/N/A), and handles format variations naturally. A script would need custom regex per field, a condition evaluator, and would break on format changes. The schema IS the comparison specification — adding a field automatically makes it comparable.

**WSKMGMT-DD-32:** Compare workflow is thin — dispatches to Procedure 7, no embedded logic. Rationale: Workflow-Skill Separation rule (DD-11). The workflow handles input parsing (extracting target path from instructions) and output formatting (diff report in chat). The comparison logic (reading two workspaces, evaluating schema fields, assigning status) lives in Procedure 7 in SKILL.md. This mirrors how workspace-setup.md dispatches to Procedures 2, 4, and 6.

## 7. Implementation Guarantees

**WSKMGMT-IG-12:** Existing questionnaire sections 1-6 remain unchanged — schema section is additive and does not modify question content.

**WSKMGMT-IG-13:** Existing `/verify workspace` context (FR-27) produces identical results before and after schema addition — schema enhances Procedure 4, does not replace it.

**WSKMGMT-IG-14:** Existing workspace creation flow works identically — schema section is read by analysis/verify/sync, not by the creation questionnaire flow.

**WSKMGMT-IG-15:** All field IDs in schema are unique — no collision between sections.

**WSKMGMT-IG-16:** Renamed `WORKSPACE_SETUP_QUESTIONNAIRE.md` is recognized by all workflows and skills that previously referenced `WORKSPACE_CREATION_QUESTIONNAIRE.md`.

**WSKMGMT-IG-17:** Deprecated `workspace-create.md` is deleted from `.devin/workflows/` during next sync after `devsystem-sync.json` deprecated array is updated.

**WSKMGMT-IG-18:** Compare use case must not modify either workspace without @rules:core-conventions.md [CONFIRMATION_KEYWORDS] — comparison is read-only by default.

**WSKMGMT-IG-19:** Compare use case must handle missing NOTES.md or devsystem-sync.json in target workspace gracefully — report GAP status for affected fields, continue comparison for remaining fields.

## 8. Key Mechanisms

### Schema Evaluation

```
Evaluate schema field:
├─> Read field from schema (top-to-bottom order)
├─> Evaluate condition:
│   ├─> (always) → field applies
│   ├─> [prior_field] == [value] → check prior field result
│   └─> [prior1] == [val1] AND [prior2] == [val2] → check both
├─> Condition met?
│   ├─ Yes → read current value from workspace
│   │   ├─> Compare against default
│   │   ├─> Assign status (OK/GAP/STALE/DEVIATION)
│   │   └─> For list: compute missing/extra sets
│   └─ No → mark N/A, skip to next field
└─> Append result to report
```

### List Field Comparison

```
Compare list field:
├─> expected = default value (array)
├─> current = value from workspace (array)
├─> missing = expected items not in current
│   └─> If missing non-empty → status = GAP (missing required items)
├─> extra = current items not in expected
│   └─> Extra items are valid customizations → do not affect status
├─> If missing empty and current non-empty → status = OK
└─> If current empty and expected non-empty → status = GAP
```

### Workflow Dispatch

```
/workspace-setup [argument]
├─> argument = "verify"
│   └─> Call Procedure 4 (Integrity Check) with schema-aware mode
│       ├─> Read schema fields from questionnaire
│       ├─> Evaluate all fields against current workspace
│       ├─> Propose fixes for GAP and STALE
│       └─> Confirm/execute on user keyword
├─> argument = "sync from [source]"
│   └─> Call Procedure 2 (Update) scoped to setup files
│       ├─> Read source workspace setup (NOTES.md, devsystem-sync.json)
│       ├─> Compare with current using schema
│       ├─> Preview: fields to add/modify/remove
│       └─> Confirm/execute on user keyword
├─> argument = "sync to [target]"
│   └─> Call Procedure 2 (Update) reversed, scoped to setup files
│       ├─> Read current workspace setup
│       ├─> Compare with target using schema
│       ├─> Preview: fields to add/modify/remove
│       └─> Confirm/execute on user keyword
├─> argument = "compare [path]"
│   └─> Call Procedure 7 (Compare Workspace Setup)
│       ├─> Load schema from WORKSPACE_SETUP_QUESTIONNAIRE.md
│       ├─> Read workspace A (current): NOTES.md, devsystem-sync.json, folder structure
│       ├─> Read workspace B (target from path): NOTES.md, devsystem-sync.json, folder structure
│       ├─> For each schema field: evaluate condition, extract A value, extract B value, compare
│       ├─> Assign status: MATCH, DIFF, ONLY_A, ONLY_B, N/A
│       └─> Output diff report to chat
├─> argument = [instructions]
│   └─> Execute instructions and settings
└─> argument = (none)
    └─> Call Procedure 6 (Setup Analysis)
        ├─> Read schema, detect workspace, evaluate all fields
        └─> Output full report to chat
```

## 9. Action Flow

### Verify Use Case

```
/workspace-setup verify
├─> Load WORKSPACE_SETUP_QUESTIONNAIRE.md schema section
├─> Detect workspace type and mode
├─> For each schema field (top-to-bottom):
│   ├─> Evaluate condition
│   ├─> Condition met?
│   │   ├─ Yes → read current value, compare with default
│   │   │   ├─> OK → no action
│   │   │   ├─> GAP → propose fix (add missing constant, create missing file)
│   │   │   ├─> STALE → propose update (refresh outdated value)
│   │   │   └─> DEVIATION → report, no fix proposed
│   │   └─ No → mark N/A, skip
├─> Present proposed changes in chat
├─> User responds?
│   ├─> @rules:core-conventions.md [CONFIRMATION_KEYWORDS]
│   │   └─> Execute proposed changes
│   │       ├─> Add missing constants to NOTES.md
│   │       ├─> Create missing files from templates
│   │       └─> Update stale values
│   └─> No confirmation
│       └─> Abort, no changes made
└─> Report results
```

### Sync From Source Use Case

```
/workspace-setup sync from [source-path]
├─> Load schema from WORKSPACE_SETUP_QUESTIONNAIRE.md
├─> Read source workspace setup:
│   ├─> Source NOTES.md (workspace constants)
│   ├─> Source devsystem-sync.json (sync config)
│   └─> Source folder structure
├─> Read current workspace setup:
│   ├─> Current NOTES.md
│   ├─> Current devsystem-sync.json
│   └─> Current folder structure
├─> For each schema field:
│   ├─> Compare source value with current value
│   ├─> Field in source but not current → propose add
│   ├─> Field in both with different values → propose modify (source wins)
│   └─> Field in current but not source → preserve (no action)
├─> Present proposed changes in chat
├─> User responds?
│   ├─> Confirmation keyword → execute changes
│   └─> No confirmation → abort
└─> Report results
```

### Compare Use Case

```
/workspace-setup compare [target-path]
├─> Load schema from WORKSPACE_SETUP_QUESTIONNAIRE.md
├─> Read workspace A (current):
│   ├─> Current NOTES.md (workspace constants)
│   ├─> Current devsystem-sync.json (sync config)
│   └─> Current folder structure
├─> Read workspace B (target from path):
│   ├─> Target NOTES.md
│   ├─> Target devsystem-sync.json
│   └─> Target folder structure
├─> For each schema field (top-to-bottom):
│   ├─> Evaluate condition for workspace A
│   ├─> Evaluate condition for workspace B
│   ├─> Both conditions met?
│   │   ├─ Yes → extract A value, extract B value, compare
│   │   │   ├─> MATCH → identical values
│   │   │   ├─> DIFF → both have values, different
│   │   │   ├─> ONLY_A → only in workspace A
│   │   │   └─> ONLY_B → only in workspace B
│   │   └─ No → N/A for this workspace type
│   └─> For list fields: compare as sets (common, only-A, only-B)
├─> Generate diff report:
│   ├─> Per-field: field ID, workspace A value, workspace B value, status
│   └─> Summary: counts per status, total compared, N/A count
├─> Output report to chat
└─> No changes executed — pure comparison
```

### Default Analysis Use Case

```
/workspace-setup (no arguments)
├─> Load schema from WORKSPACE_SETUP_QUESTIONNAIRE.md
├─> Detect workspace type and mode
├─> For each schema field (top-to-bottom):
│   ├─> Evaluate condition
│   ├─> Condition met?
│   │   ├─ Yes → read current value, compare with default
│   │   │   └─> Assign status (OK/GAP/STALE/DEVIATION)
│   │   └─ No → mark N/A
├─> Generate report following WORKSPACE_SETUP_REPORT_TEMPLATE.md
├─> Output report to chat
└─> No changes executed — pure analysis
```

## 10. Data Structures

### SetupField Entry Format

```
### Field: [section][letter]-[slug]
- Type: single | list | enum [opt1, opt2, ...]
- Condition: (always) | [prior_field_id] == [value] | [id1] == [val1] AND [id2] == [val2]
- Default: [value] | ["item1", "item2", ...]
- Report label: [Human-readable label]
```

### Complete Schema Field List

```
Section 1: Workspace Type and Mode
├── 1a-workspace_type
│   - Type: enum [SOFTWARE-DEV, GENERAL]
│   - Condition: (always)
│   - Default: SOFTWARE-DEV
│   - Report label: Workspace Type
├── 1b-workspace_mode
│   - Type: enum [SINGLE-PROJECT, MONOREPO, WORKSPACE]
│   - Condition: 1a-workspace_type == SOFTWARE-DEV
│   - Default: SINGLE-PROJECT
│   - Report label: Workspace Mode

Section 2: Product Repo
├── 2a-product_repo_name
│   - Type: single
│   - Condition: 1b-workspace_mode == WORKSPACE
│   - Default: [myapp]
│   - Report label: Product Repo Name
├── 2b-product_repo_description
│   - Type: single
│   - Condition: 1b-workspace_mode == WORKSPACE
│   - Default: [A CLI tool for ...]
│   - Report label: Product Repo Description
├── 2c-binary_build
│   - Type: enum [yes, no]
│   - Condition: 1b-workspace_mode == WORKSPACE
│   - Default: no
│   - Report label: Binary Build
├── 2d-binary_path
│   - Type: single
│   - Condition: 2c-binary_build == yes
│   - Default: dist/[appname]-{version}-win-x64.exe
│   - Report label: Binary Path Pattern

Section 3: Dev Repo / Workspace Root
├── 3a-project_name
│   - Type: single
│   - Condition: (always)
│   - Default: [myapp]
│   - Report label: Project Name
├── 3b-project_goal
│   - Type: single
│   - Condition: (always)
│   - Default: [Describe what this project does]
│   - Report label: Project Goal
├── 3c-agent_folder
│   - Type: single
│   - Condition: (always)
│   - Default: .devin
│   - Report label: Agent Folder Name
├── 3d-sessions_folder
│   - Type: single
│   - Condition: (always)
│   - Default: _sessions
│   - Report label: Sessions Folder Name
├── 3e-sops_file
│   - Type: single
│   - Condition: (always)
│   - Default: SOPS.md
│   - Report label: SOPS File Name

Section 4: Version Strategy
├── 4a-version_source
│   - Type: enum [devsystem_folder, pyproject_toml, package_json, none]
│   - Condition: 1a-workspace_type == SOFTWARE-DEV
│   - Default: devsystem_folder
│   - Report label: Version Source
├── 4b-tag_format
│   - Type: enum [date, semver]
│   - Condition: 1a-workspace_type == SOFTWARE-DEV
│   - Default: date
│   - Report label: Tag Format
├── 4c-post_release_bump
│   - Type: enum [devsystem_rename, patch_bump, minor_bump, none]
│   - Condition: 1a-workspace_type == SOFTWARE-DEV
│   - Default: devsystem_rename
│   - Report label: Post-Release Bump Strategy

Section 5: Sync Sources
├── 5a-sync_relationship
│   - Type: enum [SYNCED, SELF-CONTAINED]
│   - Condition: 1b-workspace_mode == WORKSPACE
│   - Default: SYNCED
│   - Report label: Sync Relationship
├── 5b-devsystem_source
│   - Type: single
│   - Condition: 1b-workspace_mode == WORKSPACE AND 5a-sync_relationship == SYNCED
│   - Default: [WORKSPACE_FOLDER]\..\[devsystem-source-name]\DevSystemV*
│   - Report label: DevSystem Source Path
├── 5c-company_folder
│   - Type: single
│   - Condition: 1b-workspace_mode == WORKSPACE AND 5a-sync_relationship == SYNCED
│   - Default: [WORKSPACE_FOLDER]\..\Company
│   - Report label: Company Folder Path
├── 5d-knowledge_folder
│   - Type: single
│   - Condition: 1b-workspace_mode == WORKSPACE
│   - Default: [WORKSPACE_FOLDER]\knowledge
│   - Report label: Knowledge Folder
├── 5e-specs_folder
│   - Type: single
│   - Condition: 1b-workspace_mode == WORKSPACE
│   - Default: [WORKSPACE_FOLDER]\specs
│   - Report label: Specs Folder
├── 5f-knowledge_bundles
│   - Type: list
│   - Condition: 1b-workspace_mode == WORKSPACE AND 5a-sync_relationship == SYNCED
│   - Default: []
│   - Report label: Knowledge Bundles
├── 5g-specs_bundles
│   - Type: list
│   - Condition: 1b-workspace_mode == WORKSPACE AND 5a-sync_relationship == SYNCED
│   - Default: []
│   - Report label: Specs Bundles
├── 5h-never_overwrite
│   - Type: list
│   - Condition: 1b-workspace_mode == WORKSPACE AND 5a-sync_relationship == SYNCED
│   - Default: ["NOTES.md", "!NOTES.md", "PROBLEMS.md", "!PROGRESS.md", "FAILS.md", "ID-REGISTRY.md", "SOPS.md", "_SOPS.md", "devsystem-sync.json"]
│   - Report label: Never Overwrite Patterns

Section 6: Release Configuration
├── 6a-github_releases
│   - Type: enum [yes, no]
│   - Condition: 1a-workspace_type == SOFTWARE-DEV
│   - Default: yes
│   - Report label: GitHub Releases
├── 6b-release_notes_dir
│   - Type: single
│   - Condition: 1a-workspace_type == SOFTWARE-DEV AND 6a-github_releases == yes
│   - Default: [PRODUCT_DOCS_FOLDER]\ReleaseNotes
│   - Report label: Release Notes Directory
├── 6c-run_tests
│   - Type: enum [yes, no]
│   - Condition: 1a-workspace_type == SOFTWARE-DEV
│   - Default: yes
│   - Report label: Run Tests Before Release
├── 6d-test_command
│   - Type: single
│   - Condition: 1a-workspace_type == SOFTWARE-DEV AND 6c-run_tests == yes
│   - Default: [from Build/Test Rules in NOTES.md]
│   - Report label: Test Command
├── 6e-version_consistency_gate
│   - Type: enum [yes, no]
│   - Condition: 1a-workspace_type == SOFTWARE-DEV AND 2c-binary_build == yes
│   - Default: yes
│   - Report label: Version Consistency Gate
```

### Report Template Structure

```
# Workspace Setup Report

## Summary
- Workspace Type: [value]
- Workspace Mode: [value]
- Sync Relationship: [SYNCED|SELF-CONTAINED]
- Total Fields Checked: N
- OK: N | Gaps: N | Stale: N | Deviations: N | N/A: N

## Section 1: Workspace Type and Mode
- 1a-workspace_type: Current=[value] Default=[value] Status=[OK|GAP|STALE|DEVIATION|N/A] Fix=[description or —]
- 1b-workspace_mode: Current=[value] Default=[value] Status=[OK|GAP|STALE|DEVIATION|N/A] Fix=[description or —]

## Section 2: Product Repo
- 2a-product_repo_name: Current=[value] Default=[value] Status=[...] Fix=[...]
- 2c-binary_build: Current=[value] Default=[value] Status=[...] Fix=[...]
- 2d-binary_path: Status=N/A (2c-binary_build=no)

## Section 5: Sync Sources
- 5h-never_overwrite: Status=GAP (missing 7 patterns)
  - Expected: ["NOTES.md", "!NOTES.md", "PROBLEMS.md", "!PROGRESS.md", "FAILS.md", "ID-REGISTRY.md", "SOPS.md", "_SOPS.md", "devsystem-sync.json"]
  - Current: ["NOTES.md", "FAILS.md"]
  - Missing: ["!NOTES.md", "PROBLEMS.md", "!PROGRESS.md", "ID-REGISTRY.md", "SOPS.md", "_SOPS.md", "devsystem-sync.json"]
  - Extra: (none)
  - Proposed Fix: Add 7 missing patterns to devsystem-sync.json

## Proposed Changes (verify use case only)
1. [field-id]: [action description]
2. [field-id]: [action description]

Execute with: yes | do | confirm | execute
```

## 11. User Actions

- **`/workspace-setup verify`**: Run verification against defaults and templates. Agent proposes fixes in chat. User confirms with keywords (yes, do, confirm, execute) to apply, or responds otherwise to abort
- **`/workspace-setup sync from [source-path]`**: Sync setup configuration from source repo to current. Agent previews changes. User confirms to execute
- **`/workspace-setup sync to [target-path]`**: Sync setup configuration from current to target repo. Agent previews changes. User confirms to execute
- **`/workspace-setup [instructions]`**: Execute provided instructions and settings
- **`/workspace-setup`** (no args): Agent analyzes current workspace, generates full report in chat. No changes executed

## 12. UX Design

N/A: This is a CLI/workflow specification, not a UI component. Output is text in chat.

## 13. Logging Requirements

**User-Facing (UF):**
- Audience: Developer running workspace setup commands
- Goal: Understand current workspace state, what changes are proposed, and what was executed
- Key operations: verify analysis, sync preview, sync execution, default analysis report

**Expected output for verify use case:**
```
Workspace Setup Verification
├─> Workspace Type: SOFTWARE-DEV
├─> Workspace Mode: WORKSPACE
├─> Sync Relationship: SYNCED
├─> Fields Checked: 28
│   ├─> OK: 22
│   ├─> Gaps: 3
│   ├─> Stale: 1
│   ├─> Deviations: 2
│   └─> N/A: 0
├─>
├─> Proposed Changes:
│   ├─> 5h-never_overwrite: Add 7 missing patterns to devsystem-sync.json
│   ├─> 4a-version_source: Update from 'none' to 'devsystem_folder' (stale)
│   └─> 3e-sops_file: Create SOPS.md (missing required file)
├─>
└─> Execute with: yes | do | confirm | execute
```

**Expected output for default analysis:**
```
Workspace Setup Report
├─> Workspace Type: SOFTWARE-DEV
├─> Workspace Mode: WORKSPACE
├─> Sync Relationship: SYNCED
├─> Total Fields: 28 | OK: 22 | Gaps: 3 | Stale: 1 | Deviations: 2 | N/A: 0
├─>
├─> Section 1: Workspace Type and Mode
│   ├─> 1a-workspace_type: SOFTWARE-DEV | OK
│   └─> 1b-workspace_mode: WORKSPACE | DEVIATION (default: SINGLE-PROJECT)
├─>
├─> Section 5: Sync Sources
│   ├─> 5h-never_overwrite: GAP (missing 7 patterns)
│   │   ├─> Missing: !NOTES.md, PROBLEMS.md, !PROGRESS.md, ID-REGISTRY.md, SOPS.md, _SOPS.md, devsystem-sync.json
│   │   └─> Extra: (none)
│   └─> 5f-knowledge_bundles: OK (custom: Windsurf, AI-Standards)
└─> No changes executed — run /workspace-setup verify to propose fixes
```

## 14. Technical Constraints

- Schema is markdown-based — no JSON, YAML, or XML parsing required. Agent reads structured markdown entries
- Schema section is additive to existing questionnaire — no modification to sections 1-6 content
- Procedure 4 enhancement (schema-aware mode) must not break existing `/verify workspace` callers
- Procedure 2 scoping (setup files only) must not break existing `/sync workspace` callers
- Report is generated to chat, not persisted as file — no file I/O needed
- Merge strategy for sync uses case: source wins for shared fields, target-only fields preserved, list fields use additive merge (union)
- Confirmation keywords match @rules:core-conventions.md [CONFIRMATION_KEYWORDS]

## 15. Document History

**[2026-09-08 20:50]**
- Added: FR-73 (compare-workspace-setup.md workflow), FR-74 (Procedure 7), FR-75 (compare use case)
- Added: DD-31 (agent as comparison engine), DD-32 (thin compare workflow)
- Added: IG-18 (no modification without confirmation), IG-19 (graceful missing file handling)
- Added: Compare Use Case to Action Flow and Workflow Dispatch diagram
- Updated: Target files list with compare-workspace-setup.md, SKILL.md Procedures 6 and 7

**[2026-09-08 20:35]**
- Changed: All confirmation keywords replaced with `@rules:core-conventions.md [CONFIRMATION_KEYWORDS]` reference
- Added: `[CONFIRMATION_KEYWORDS]` definition to core-conventions.md (yes, confirm, confirmed, do, execute, apply)

**[2026-09-08 20:30]**
- Fixed: GAP-01 — FR-68 now explicitly says "Amends FR-27" instead of "Relationship to FR-27"
- Fixed: GAP-03 — Added devsystem-sync.json to Target files list
- Fixed: GAP-04 — All confirmation keywords aligned with FR-29: yes, go, confirmed, execute, apply

**[2026-09-08 20:15]**
- Initial specification created
