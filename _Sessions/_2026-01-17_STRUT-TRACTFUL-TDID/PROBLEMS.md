# Session Problems

## Open

### STRUT-PR-001: Workflows depend on EDIRD phase model

**Status**: Open
**Severity**: HIGH
**Description**: Current workflow implementations contain knowledge about EDIRD phases. This prevents swapping EDIRD for alternative phase models.
**Impact**: Cannot experiment with different phase models without rewriting workflows.
**Proposed solution**: Workflows should only contain task knowledge. Phase orchestration should be in a separate layer.

### STRUT-PR-002: Verbs cannot be extended per scope

**Status**: Open
**Severity**: MEDIUM
**Description**: AGEN verbs are globally defined. No mechanism to add workspace/project/session-specific verbs.
**Impact**: Cannot adapt vocabulary to domain-specific needs.
**Proposed solution**: Define verb extension mechanism with scope precedence.

### STRUT-PR-004: AGEN syntax ambiguity

**Status**: Open
**Severity**: MEDIUM
**Description**: Two token types (Instruction Tokens in brackets, Context States in uppercase) but unclear generalization for TOPICs, concepts.
**Impact**: Inconsistent usage, unclear when to use brackets vs uppercase.
**Proposed solution**: Formalize CONSTANT (uppercase, no brackets) vs [INSTRUCTION] (brackets) distinction.

### STRUT-PR-007: No Acceptance Criteria in SPECs

**Status**: Open
**Severity**: MEDIUM
**Description**: SPECs have FR/DD/IG but no explicit AC section defining when spec is implemented.
**Impact**: Unclear completion criteria, ambiguous verification.
**Proposed solution**: Add AC (Acceptance Criteria) section to SPEC template.

## Resolved

### STRUT-PR-005: IMPL plans give agent too much freedom

**Status**: Resolved
**Severity**: HIGH
**Description**: IMPL plans are directly implemented without intermediate partitioning. Agent can choose arbitrary strategies that fail.
**Impact**: Unpredictable implementation quality, difficult to test incrementally.
**Solution applied**: Added [PARTITION] verb and TASKS_*.md to Required Documents in SPEC_EDIRD. DESIGN→IMPLEMENT gate now requires TASKS document. partition.md workflow exists with strategies (DEFAULT, DEPENDENCY, SLICE, RISK). TASKS_TEMPLATE.md provides structure. Replaced [DECOMPOSE] with [PARTITION] throughout spec.

### STRUT-PR-003: No central TOPIC ID registry

**Status**: Resolved
**Severity**: HIGH
**Description**: TOPIC IDs are mentioned in devsystem-ids.md but no enforcement of uniqueness.
**Impact**: Risk of duplicate TOPIC IDs causing traceability issues.
**Solution applied**: Comprehensive ID-REGISTRY.md created with all IDs, acronyms, context states, and labels. Includes Document Type IDs, Spec-Level IDs, Plan-Level IDs, Tracking IDs, and measurement units.

### STRUT-PR-006: FAILS.md captures only technical failures

**Status**: Resolved
**Severity**: MEDIUM
**Description**: Current FAILS.md mechanism focuses on implementation failures. Missing conceptual, planning, and assessment failures.
**Impact**: Repeated strategic mistakes, not just technical ones.
**Solution applied**: Created `/learn` workflow and LEARNINGS.md document type. FAILS.md stays simple (what failed). LEARNINGS.md captures structured retrospective analysis: problem type classification, assumption reconstruction, rationale analysis, dependency tree, root cause identification. Learning entries update linked FAILS.md entries with insights.

## Deferred
