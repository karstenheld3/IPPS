# SOCAS Coding Rules

Field rules of Signs of Confusion and Sloppiness (SOCAS) for code and code specifications. Run together with `SOCAS_RULES.md` (general rules, application rules, reporting rules, priority model and rule format; in `write-documents`). Origin: `_INFO_SOCAS_SIGNS_OF_CONFUSION_AND_SLOPPINESS.md [SOCAS-IN01]` (Karsten Held, 2026). Discarded, merged and deferred candidates: `_INFO_SOCAS_DISCARDED_RULE_CANDIDATES.md [SOCAS-IN02]`.

**Content types**: source code, configuration, scripts, diffs and pull requests, repositories, dependencies, technical READMEs, code specifications (software SPEC, IMPL, TEST, API specifications; in IPPS all `_SPEC_*`, `_IMPL_*`, `_TEST_*` and `_TASKS_*` documents, including specifications of workflows and skills, because they specify executable agent behavior). User interfaces: no rule (discarded until researched).

`MECT_CODING_RULES.md` owns naming, comments, error messages, logs and documentation wording in code. SOCAS-CD rules cover other areas. Tool checks (scanner, complexity metric, registry lookup) beat an LLM pass; a SOCAS run calls or recommends them and flags only obvious cases without them [ASSUMED]. Not encoded: "defects cost 100 times more the later they are found" ([no delayed-issue effect in 171 projects](https://doi.org/10.1007/s10664-016-9469-x)).

## Rule Index

Coding (CD)
- SOCAS-CD-01: Invented Dependency
- SOCAS-CD-02: Insecure Construction
- SOCAS-CD-03: Unresolved Debt Markers
- SOCAS-CD-04: Change Too Large to Review
- SOCAS-CD-05: Excess Complexity
- SOCAS-CD-06: Stale or Unhealthy Dependency
- SOCAS-CD-08: Missing Tests, History or Setup
- SOCAS-CD-09: Behavior, Edge Cases or Acceptance Undefined
- SOCAS-CD-10: Unverifiable Requirement Wording

## Table of Contents

- [Rank Order](#rank-order)
- [Code and Repository](#code-and-repository)
- [Code Specifications](#code-specifications)

## Rank Order

Run after the general rules (SOCAS-AP-12). On source code, scripts, configuration and diffs the general rules SOCAS-GN-02, GN-03, GN-15, GN-19, GN-21 and GN-22 return `SKIP`. Code specifications and technical READMEs are text and run all general rules. Within this file:
- P1: SOCAS-CD-02, CD-09, CD-01, CD-10, CD-04, CD-08
- P2: SOCAS-CD-05, CD-06, CD-03

## Code and Repository

### SOCAS-CD-01: Invented Dependency

- A package or import name does not exist in its registry, or exists without history
- **Applies to**: code, dependency manifests and documentation that name packages
- **Test**: Does every package or import exist in its registry with a history?
- **Priority**: P1 | Cost: medium, 1 registry lookup per name | Value: high, evidence B ([19.7% of 2.23 million packages suggested by 16 code models did not exist](https://www.usenix.org/system/files/usenixsecurity25-spracklen.pdf); USENIX Security 2025)
- **Web**: yes, registry lookup by tool; without a tool, unknown or unusual names first within the SOCAS-AP-10 budget
- **Overlap**: none

### SOCAS-CD-02: Insecure Construction

- String-built SQL or shell commands, hard-coded secrets, unsafe deserialization, disabled certificate checks
- **Applies to**: source code, scripts, configuration
- **Test**: Does the code contain a construction known as insecure?
- **Priority**: P1 | Cost: low for obvious cases (scanner for full check) | Value: high, evidence B ([about 40% of 1,689 GitHub Copilot programs vulnerable](https://arxiv.org/html/2108.09293v3))
- **Web**: no
- **Overlap**: none

### SOCAS-CD-03: Unresolved Debt Markers

- TODO, FIXME or hack markers without owner, date or ticket; a marker on the core function. One marker is not a defect
- **Applies to**: source code
- **Test**: Are there debt markers without owner or date, or on the core function?
- **Priority**: P2 | Cost: low, text search | Value: low, [markers are common](https://doi.org/10.1109/icsme.2014.31) (2.4% to 31% of files in 4 systems). Kept because agent-written code leaves unfinished stubs, no other rule covers them and the cost is low
- **Web**: no
- **Overlap**: none (MECT-PR-04 covers comment wording only)

### SOCAS-CD-04: Change Too Large to Review

- Diff over about 400 lines without split, or without stated purpose [ASSUMED threshold for other teams]
- **Applies to**: diffs and pull requests
- **Test**: Is the change too large to review in one pass, or without stated purpose?
- **Priority**: P1 | Cost: low, line count from diff | Value: medium, evidence C ([2,500 reviews: defect density dropped above 200 lines](https://static1.smartbear.co/support/media/resources/cc/book/code-review-cisco-case-study.pdf); vendor-run case study)
- **Web**: no
- **Overlap**: none

### SOCAS-CD-05: Excess Complexity

- Deep nesting, long branching chains, indirection without benefit, over-engineered solution for a simple problem. Use a complexity tool for the metric
- **Applies to**: source code
- **Test**: Is there a simpler construction that does the same?
- **Priority**: P2 | Cost: medium, tool or judgment | Value: medium, evidence B ([Cognitive Complexity correlated 0.654 with comprehension time](https://dl.acm.org/doi/10.1145/3382494.3410636), 14 studies)
- **Web**: no
- **Overlap**: none

### SOCAS-CD-06: Stale or Unhealthy Dependency

- Archived or abandoned repository referenced as active; no maintenance activity; known vulnerabilities; declared end-of-life without successor; many open issues without maintainer response
- **Applies to**: code, READMEs or proposals that name dependencies a decision rests on
- **Test**: Is a decision-relevant dependency active, maintained and free of known vulnerabilities?
- **Priority**: P2 | Cost: medium, 1 lookup per decision-relevant dependency | Value: medium, evidence C ([Open Source Security Foundation (OpenSSF) Scorecard](https://github.com/ossf/scorecard/blob/main/README.md) checks; the tool states a low score is not a definitive risk)
- **Web**: yes
- **Overlap**: none

### SOCAS-CD-08: Missing Tests, History or Setup

- No tests or tests disabled; no version history or a single commit; boilerplate README without setup instructions; dead code
- **Applies to**: repositories and code deliveries (bids, handovers); not code snippets
- **Test**: Are tests, history and setup instructions present?
- **Priority**: P1 | Cost: low, file listing | Value: medium, evidence C ([US government 18F guide for evaluating bids](https://guides.18f.gov/derisking-government-tech/resources/evaluate-bids/))
- **Web**: no
- **Overlap**: none

## Code Specifications

### SOCAS-CD-09: Behavior, Edge Cases or Acceptance Undefined

- Behavior, edge cases (empty input, timeout, concurrent access), error handling or acceptance check not stated; two requirements conflict; unstated assumptions
- **Applies to**: code specifications (content types above)
- **Test**: Can the implementer tell the required behavior, the edge cases, the error handling and how acceptance is checked?
- **Priority**: P1 | Cost: low, text only | Value: high, evidence B ([unstated requirements dropped agent accuracy 22.6% on average](https://aclanthology.org/2026.findings-acl.441/); [NASA](https://www.nasa.gov/reference/appendix-c-how-to-write-a-good-requirement/) and [IBM](https://www.ibm.com/docs/en/erqa?topic=assistant-guidelines-good-requirements) requirement rules)
- **Web**: no
- **Overlap**: none

### SOCAS-CD-10: Unverifiable Requirement Wording

- Escape clauses; one requirement holding several obligations; adjectives without measure; goals without tolerance range; missing units; to be determined (TBD) values without owner and date; requirement without unique ID; requirement without rationale or parent ("why is it here?")
- **Applies to**: code specifications
- **Test**: Is each requirement one verifiable obligation with measure, unit and an owner for open values?
- **Priority**: P1 | Cost: low, text only | Value: medium, evidence B-C ([RFC 8174](https://www.rfc-editor.org/rfc/rfc8174.html), IBM, NASA, [EARS](https://doi.org/10.1109/re.2009.9))
- **Web**: no
- **Overlap**: REF - obligation words fixed by MECT-VO-04; IDs fixed by APAPL-PR-05
