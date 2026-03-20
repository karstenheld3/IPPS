# IMPL: [Feature Name]

**Doc ID (TDID)**: [TOPIC]-IP[NN]
**Feature**: [FEATURE_SLUG]
**Goal**: [Single sentence]
**Timeline**: Created YYYY-MM-DD, Updated N times (YYYY-MM-DD - YYYY-MM-DD)

**Target files**:
- `[path/to/file1.py]` (NEW)
- `[path/to/file2.py]` (EXTEND +50 lines)
- `[path/to/file3.py]` (MODIFY)

**Depends on:**
- `_SPEC_[X].md` [[DOC_ID]] for [what it provides]

## MUST-NOT-FORGET

- [Critical rule 1]
- [Critical rule 2]

## 1. File Structure

```
[folder]/
├── [file1.py]    # [Description] (~N lines) [NEW]
├── [file2.py]    # [Description] [EXTEND +50 lines]
└── [subfolder]/
    └── [file3.py]  # [Description] [MODIFY]
```

## 2. Edge Cases

- **[PREFIX]-IP01-EC-01**: [Condition] -> [Behavior]

Categories: input boundaries, state transitions, external failures, data anomalies.

## 3. Implementation Steps

### [PREFIX]-IP01-IS-01: [Action Description]

**Location**: `filename.py` > `function_name()`
**Action**: [Add | Modify | Remove] [description]

```python
# Outline only - no implementation detail
def new_function(...): ...
```

**Note**: [Gotchas]

## 4. Test Cases

### [Category Name] (N tests)

- **[PREFIX]-IP01-TC-01**: [Description] -> ok=true, [expected result]
- **[PREFIX]-IP01-TC-02**: [Error case] -> ok=false, [error message]

## 5. Verification Checklist

### Prerequisites
- [ ] **[PREFIX]-IP01-VC-01**: Related specs read and understood
- [ ] **[PREFIX]-IP01-VC-02**: Backward compatibility test created (if applicable)

### Implementation
- [ ] **[PREFIX]-IP01-VC-03**: IS-01 completed

### Validation
- [ ] **[PREFIX]-IP01-VC-10**: All test cases pass
- [ ] **[PREFIX]-IP01-VC-11**: Manual verification in UI

## 6. Document History

**[YYYY-MM-DD HH:MM]**
- Initial implementation plan created