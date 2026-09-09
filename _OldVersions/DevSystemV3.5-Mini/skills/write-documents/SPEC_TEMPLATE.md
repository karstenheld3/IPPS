# SPEC: [Component Name]

Doc ID (TDID): [TOPIC]-SP[NN]
Feature: [FEATURE_SLUG]
Goal: [Single sentence]
Timeline: Created YYYY-MM-DD, Updated N times (YYYY-MM-DD - YYYY-MM-DD)
Target file: `[path/to/file.py]`

Depends on:
- `_SPEC_[X].md [TOPIC-SP01]` for [what it provides]

Does not depend on:
- `_SPEC_[Y].md [TOPIC-SP02]` (explicitly exclude if might seem related)

## MUST-NOT-FORGET

- [Critical rule 1]
- [Critical rule 2]

## 1. Scenario

Problem: [Real-world problem description]

Solution:
- [Approach point 1]

What we don't want:
- [Anti-pattern 1]

## 2. Context

[Project background, related systems, how this component fits]

## 3. Domain Objects

### [ObjectName]

A [ObjectName] represents [description].

Storage: `path/to/storage/`
Definition: `config.json`

Key properties:
- `property_1` - [description]

Schema:
```json
{"field1": "value", "field2": 123}
```

## 4. Functional Requirements

[PREFIX]-FR-01: [Requirement Title]
- [Requirement detail 1]
- [Requirement detail 2]

## 5. Design Decisions

[PREFIX]-DD-01: [Decision description]. Rationale: [Why].

## 6. Implementation Guarantees

[PREFIX]-IG-01: [What the implementation must guarantee]

## 7. Key Mechanisms

[Technical patterns, algorithms, declarative approaches used]

## 8. Action Flow

```
User clicks [Button]
├─> functionA(param)
│   ├─> fetch(`/api/endpoint`)
│   │   └─> On success:
│   │       ├─> updateState()
│   │       └─> renderUI()
```

## 9. Data Structures

```
<start_json>
{"id": 42, "state": "running"}
</start_json>
<end_json>
{"id": 42, "state": "completed", "result": "ok"}
</end_json>
```

## 10. User Actions

*(UI specs only)*

- [Action Name]: [Description of user interaction and expected result]

## 11. UX Design

*(UI specs only)* Show ALL buttons and actions:

```
+---------------------------------------------------------------+
|  Component Name                                               |
|  [Button 1]  [Button 2]                                      |
|  +----+--------+--------+----------------------------------+  |
|  | ID | Name   | Status | Actions                          |  |
|  +----+--------+--------+----------------------------------+  |
|  | 1  | Item A | active | [Edit] [Delete]                  |  |
|  +----+--------+--------+----------------------------------+  |
+---------------------------------------------------------------+
```

## 12. Implementation Details

[Code organization, function signatures, module structure]

## 13. Document History

[YYYY-MM-DD HH:MM]
- Initial specification created