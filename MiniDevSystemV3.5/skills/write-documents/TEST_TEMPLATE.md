# TEST: [Component Name]

**Doc ID (TDID)**: [TOPIC]-TP[NN]
**Feature**: [FEATURE_SLUG]
**Goal**: [Single sentence]
**Timeline**: Created YYYY-MM-DD, Updated N times (YYYY-MM-DD - YYYY-MM-DD)
**Target file**: `[path/to/test_file.py]`

**Depends on:**
- `_SPEC_[X].md` [[DOC_ID]] for requirements
- `_IMPL_[X].md` [[DOC_ID]] for implementation details

## MUST-NOT-FORGET

- [Critical rule 1]
- [Critical rule 2]

## 1. Overview

[Brief description]

## 2. Scenario

**Problem:** [What issue or behavior we're testing]
**Solution:** [How tests verify correct behavior]
**What we don't want:**
- [Test anti-pattern 1]

## 3. Test Strategy

**Approach**: [unit | integration | snapshot-based]

## 4. Test Priority Matrix

### MUST TEST (Critical Business Logic)

- **`function_name()`** - module_name
  - Testability: [EASY/Medium/Hard], Effort: [Low/Medium/High]
  - [What to test]

### SHOULD TEST (Important Workflows)

- **`function_name()`** - module_name
  - Testability: Medium, Effort: Medium
  - [Description]

### DROP (Not Worth Testing)

- **`function_name()`** - Reason: [External dependency / UI-only / trivial]

## 5. Test Data

**Required Fixtures:**
- [Fixture 1]: [Description]

**Setup:**
```python
# Setup code
```

**Teardown:**
```python
# Cleanup code
```

## 6. Test Cases

### Category 1: [Name] (N tests)

- **[PREFIX]-TC-01**: [Description] -> ok=true, [expected result]
- **[PREFIX]-TC-02**: [Error case] -> ok=false, [error message]

## 7. Test Phases

1. **Phase 1: Setup** - [Description]
2. **Phase 2: Core Tests** - [Description]
3. **Phase 3: Edge Cases** - [Description]
4. **Phase 4: Cleanup** - [Description]

## 8. Helper Functions

```python
def assert_state_matches(actual, expected): ...
def create_test_fixture(): ...
```

## 9. Cleanup

- [Artifact to remove]

## 10. Verification Checklist

- [ ] All MUST TEST functions covered
- [ ] All test cases pass
- [ ] Coverage meets requirements
- [ ] Edge cases covered
- [ ] Cleanup executed

## 11. Document History

**[YYYY-MM-DD HH:MM]**
- Initial test plan created