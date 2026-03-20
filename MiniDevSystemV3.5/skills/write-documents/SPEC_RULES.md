# SPEC Document Rules

**Writing quality:** Apply `APAPALAN_RULES.md` - key rules: AP-PR-07 (be specific), AP-PR-08 (examples for every rule), AP-NM-01 (one name per concept), AP-PR-09 (consistent patterns).

## Rule Index

**Requirements (RQ)**
- **SPEC-RQ-01**: Numbered IDs for functional requirements (XXXX-FR-01)
- **SPEC-RQ-02**: Numbered IDs for design decisions (XXXX-DD-01)
- **SPEC-RQ-03**: Numbered IDs for implementation guarantees (XXXX-IG-01)

**Diagrams (DG)**
- **SPEC-DG-01**: ASCII box diagrams with component boundaries
- **SPEC-DG-02**: Show ALL buttons and actions in UI diagrams
- **SPEC-DG-03**: Layer diagrams for multi-tier systems

**Content (CT)**
- **SPEC-CT-01**: Summarize styling - avoid CSS detail
- **SPEC-CT-02**: Code outline only - avoid implementation detail
- **SPEC-CT-03**: Single line statements when possible
- **SPEC-CT-04**: Document event flows with box-drawing characters
- **SPEC-CT-05**: Provide data structure examples (JSON, CSV)
- **SPEC-CT-06**: Compact object definitions - lists, no empty lines between properties
- **SPEC-CT-07**: Compact gate checklists - simple lists, not ASCII box diagrams

**Format (FT)**
- **SPEC-FT-01**: Timestamped changelog, reverse chronological
- **SPEC-FT-02**: No Markdown tables in changelogs
- **SPEC-FT-03**: Proper header block and section order

## Requirements Format

```
**UI-FR-01: Toast Notifications**
- Support info, success, error, warning message types
- Auto-dismiss configurable per toast (default 5000ms)

**DD-UI-03:** Declarative button configuration. Buttons use `data-*` attributes for endpoint URL, method, format - no custom JS per action.
```

Use standard ID types only (`FR`, `DD`, `IG`, `EC`). BAD: `CORNER-01`, `EDGE-02`. GOOD: `CRWL-EC-01`, `CRWL-EC-02`.

## UI Diagrams

Show ALL buttons/actions with component boundaries. BAD omits actions (e.g., missing [Cancel], [Resume], [Start Job]). GOOD shows every interactive element:

```
Main HTML:
+-------------------------------------------------------------------------------+
|  Streaming Jobs (2)                                                           |
|  [Start Job]  [Refresh]                                 [Toasts appear here]  |
|  +----+---------+----------+---------+-------------------------------------+  |
|  | ID | Router  | Endpoint | State   | Actions                             |  |
|  +----+---------+----------+---------+-------------------------------------+  |
|  | 42 | crawler | update   | running | [Monitor] [Pause / Resume] [Cancel] |  |
|  | 41 | crawler | update   | done    | [Monitor]                           |  |
|  +----+---------+----------+---------+-------------------------------------+  |
|  +-------------------------------------------------------------------------+  |
|  | [Resize Handle - Draggable]                                             |  |
|  | Console Output                                                  [Clear] |  |
|  +-------------------------------------------------------------------------+  |
+-------------------------------------------------------------------------------+
```

## Layer Architecture Diagrams

```
┌───────────────────────────────────────────────────────────────────────────┐
│  High-Level (Router)                                                      │
│  ├─> function_a()         # Called by router endpoints                    │
├───────────────────────────────────────────────────────────────────────────┤
│  Mid-Level (Components)                                                   │
│  ├─> function_b()         # Generates HTML fragments                      │
├───────────────────────────────────────────────────────────────────────────┤
│  Low-Level (Helpers)                                                      │
│  └─> json_result()        # Response formatting                           │
└───────────────────────────────────────────────────────────────────────────┘
```

## Summarize Styling

BAD: Full CSS properties. GOOD: `/* Individual toast notification with light theme */`

## Code Outline Only

BAD: Full function body with logic. GOOD: `function renderJobRow(job) { ... }` with comment describing purpose.

## Single Line Statements

BAD: Multi-line button. GOOD: `<button class="btn-small" onclick="controlJob(42, 'pause')"> Pause </button>`

## Compact Object Definitions

Use lists, no empty lines between properties:
```
### [EXPLORE]
- **Purpose**: Understand the situation before acting
- **BUILD**: What feature? What constraints?
- **Entry**: Start of workflow
- **Verbs**: [RESEARCH], [ANALYZE], [ASSESS], [SCOPE]
```

## Compact Gate Checklists

```
### Gate: X → Y
- [ ] Item 1
- [ ] Item 2

**Pass**: proceed to [Y] | **Fail**: remain in [X]
```

## Event Flow Documentation

```
User clicks [Pause] or [Resume]
├─> controlJob(jobId, 'pause' | 'resume')
│   └─> fetch(`/testrouter3/control?id=${id}&action=${action}`)
│       └─> On success (data.success):
│           └─> Optimistically updateJob(jobId, { state: 'paused' | 'running' })
│               └─> renderAllJobs()
```

## Data Structure Examples

```
<start_json>
{"id": 42, "router": "testrouter3", "endpoint": "streaming01", "state": "running", "total": 3, "started": "2025-11-27T11:30:00"}
</start_json>
<end_json>
{"id": 42, "state": "completed", "result": "ok", "finished": "2025-11-27T11:30:15"}
</end_json>
```

## Document History Format

```
## Document History

**[2024-12-17 14:30]**
- Added: "Scenario" section with Problem/Solution/What we don't want
- Changed: Placeholder standardized to `{itemId}` (camelCase)
- Fixed: Modal OK button signature

**[2024-12-17 10:00]**
- Initial specification created
```

## Section Order and Header

Start with title, Goal, Dependencies. No `---` between sections. No orphan fields before first section.

```
# V0 Crawler Toolkit - Standalone SharePoint Crawler

**Goal**: Document the architecture and workflow of the standalone SharePoint-GPT-Crawler-Toolkit.

**Does not depend on:**
- Any V2 specifications (this is the predecessor toolkit)

## Overview
...
```