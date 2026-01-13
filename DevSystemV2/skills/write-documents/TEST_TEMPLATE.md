# TEST: [Component Name]

**Goal**: [Single sentence describing test purpose]
**Target file**: `[path/to/test_file.py]`

**Depends on:**
- `SPEC_[X].md` for requirements
- `IMPL_[X].md` for implementation details

## Table of Contents

1. [Test Strategy](#1-test-strategy)
2. [Test Cases](#2-test-cases)
3. [Verification Checklist](#3-verification-checklist)

## 1. Test Strategy

**Approach**: [unit | integration | snapshot-based]

**MUST TEST:**
- [Critical function 1]
- [Critical function 2]

**DROP:**
- [Not worth testing] - Reason: [external dependency / UI-only]

## 2. Test Cases

### Category: [Name]

- **[PREFIX]-TC-01**: [Description] -> ok=true, [expected result]
- **[PREFIX]-TC-02**: [Error case] -> ok=false, [error message]

### Category: [Name]

- **[PREFIX]-TC-03**: [Description] -> ok=true, [expected result]

## 3. Verification Checklist

- [ ] All test cases pass
- [ ] Coverage meets requirements
- [ ] Edge cases covered
