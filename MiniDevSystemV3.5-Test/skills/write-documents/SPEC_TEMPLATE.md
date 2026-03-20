# SPEC: [Component Name]

**Doc ID (TDID)**: [TOPIC]-SP[NN]
**Feature**: [FEATURE_SLUG]
**Goal**: [Single sentence describing what to specify]
**Timeline**: Created YYYY-MM-DD, Updated N times (YYYY-MM-DD - YYYY-MM-DD)
**Target file**: `[path/to/file.py]`

**Depends on:**
- `_SPEC_[X].md [TOPIC-SP01]` for [what it provides]

**Does not depend on:**
- `_SPEC_[Y].md [TOPIC-SP02]` (explicitly exclude if might seem related)

## MUST-NOT-FORGET

- [Critical rule 1]
- [Critical rule 2]

## 1. Scenario

**Problem:** [Real-world problem description]

**Solution:**
- [Approach point 1]
- [Approach point 2]

**What we don't want:**
- [Anti-pattern 1]
- [Anti-pattern 2]

## 2. Context

[Project background, related systems, how this component fits]

## 3. Domain Objects

### [ObjectName]

A **[ObjectName]** represents [description].

**Storage:** `path/to/storage/`
**Definition:** `config.json`

**Key properties:**
- `property_1` - [description]
- `property_2` - [description]

**Schema:**
```json
{
  "field1": "value",
  "field2": 123
}
```

## 4. Functional Requirements

**[PREFIX]-FR-01: [Requirement Title]**
- [Requirement detail 1]
- [Requirement detail 2]

**[PREFIX]-FR-02: [Requirement Title]**
- [Requirement detail]

## 5. Design Decisions

**[PREFIX]-DD-01:** [Decision description]. Rationale: [Why this decision].

**[PREFIX]-DD-02:** [Decision description]. Rationale: [Why this decision].

## 6. Implementation Guarantees

**[PREFIX]-IG-01:** [What the implementation must guarantee]

**[PREFIX]-IG-02:** [What the implementation must guarantee]

## 7. Key Mechanisms

[Technical patterns, algorithms, declarative approaches used]

## 8. Action Flow

Use box-drawing characters (2-space indentation compatible):

```
User clicks [Button]
├─> functionA(param)
│   ├─> fetch(`/api/endpoint`)
│   │   └─> On success:
│   │       ├─> updateState()
│   │       └─> renderUI()
```

## 9. Data Structures

```json
// Request:  {"id": 42, "state": "running"}
// Response: {"id": 42, "state": "completed", "result": "ok"}
```

## 10. UI Sections

*(UI specs only - add User Actions and UX Design sections with ASCII box diagrams)*

## 11. Implementation Details

[Code organization, function signatures, module structure]

## 12. Document History

**[YYYY-MM-DD HH:MM]**
- Initial specification created