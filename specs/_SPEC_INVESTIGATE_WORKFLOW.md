# SPEC: Investigate Workflow

**Doc ID**: INVESTIGATE-SP01
**Goal**: Define a structured investigation workflow that produces a STRUT plan and an append-only investigation log for multi-phase problem analysis

**Target file**: `[DEVSYSTEM_FOLDER]/workflows/investigate.md`, `[DEVSYSTEM_FOLDER]/skills/write-documents/INVESTIGATION_LOG_TEMPLATE.md`, `[DEVSYSTEM_FOLDER]/skills/write-documents/INVESTIGATION_GUIDES.md`, `[DEVSYSTEM_FOLDER]/skills/write-documents/INVESTIGATION_LOG_RULES.md`

**Depends on:**
- `_SPEC_STRUT_STRUCTURED_THINKING.md [STRUT-SP01]` for STRUT plan format
- `_SPEC_AGEN_AGENTIC_ENGLISH.md [AGEN-SP01]` for AGEN verb vocabulary

**Does not depend on:**
- `_SPEC_EDIRD_PHASE_MODEL.md [EDIRD-SP01]` (investigate has its own phase model)

## Summary

The investigate workflow provides a structured approach for deep problem analysis. It produces two artifacts: a STRUT plan defining investigation phases with mandatory log checkpoints, and an append-only investigation log tracking findings, hypotheses, tests, and state transitions. The workflow is designed for multi-session investigations where context handover between agents is required.

## Functional Requirements

- **FR-01**: Workflow MUST produce a STRUT plan before investigation begins
- **FR-02**: STRUT plan MUST define phases where Phase 1 is the first to execute
- **FR-03**: STRUT plan MUST include mandatory checkpoints for writing to and appending from the investigation log
- **FR-04**: Workflow MUST create an investigation log file before starting Phase 1
- **FR-05**: Investigation log MUST be append-only (never edit past entries except status updates)
- **FR-06**: After completing each phase, workflow MUST update the log with final state and handover notes
- **FR-07**: After completing each phase, workflow MUST update the STRUT plan with progress state
- **FR-08**: Workflow MUST formulate goal, collect premises, analyze problem nature, and list known knowns and known unknowns before writing the STRUT
- **FR-09**: Investigation log MUST support grep-able entry IDs for searchability across sessions
- **FR-10**: Investigation log MUST track hypotheses with OPEN/CONFIRMED/REFUTED status

## Design Decisions

- **DD-01**: Log file naming: `_LOG_[TOPIC].md` in session folder. Consistent with session document naming.
- **DD-02**: Log entry ID format: `I[NNN].[NNN]-type(topic_mnemonic)`. Thread number + entry number allows multiple investigation threads within one log.
- **DD-03**: Entry types: state, action, finding, hypothesis, test, result, reasoning, note. Covers full investigation lifecycle.
- **DD-04**: Bold reserved for status/outcome values only (STARTING, IN_PROGRESS, BLOCKED, STOPPED, DONE, OPEN, CONFIRMED, REFUTED, PASS, FAIL, INCONCLUSIVE). Visual scanning aid.
- **DD-05**: Pipe notation `key=value | key=value` for compact one-line entries. Reduces log verbosity.
- **DD-06**: Paths defined once in first STATE entry as lookup table. Next agent resolves `[NAME]` placeholders. Avoids repeating long paths.
- **DD-07**: STRUT phases represent investigation approaches, not fixed EDIRD phases. Phase 1 is the highest-priority approach.
- **DD-08**: Log file is session-scoped (lives in session folder). Not a project-level document.
- **DD-09**: Investigation log is verifiable via `/verify` with dedicated INVESTIGATION_LOG_RULES.

## Implementation Guarantees

- **IG-01**: Workflow references @write-documents for INVESTIGATION_LOG_TEMPLATE, INVESTIGATION_GUIDES, and INVESTIGATION_LOG_RULES
- **IG-02**: Workflow references @write-documents STRUT_TEMPLATE for STRUT format
- **IG-03**: Verify.md includes Investigation Logs section referencing INVESTIGATION_LOG_RULES

## Acceptance Criteria

- **AC-01**: Running `/investigate` produces a STRUT plan with at least one phase containing log checkpoints
- **AC-02**: Running `/investigate` creates a `_LOG_[TOPIC].md` file with Goal, Started, Sources, Premises, and Index sections
- **AC-03**: After Phase 1 completion, log contains at least one STATE entry with handover notes
- **AC-04**: After Phase 1 completion, STRUT plan has progress checkboxes updated
- **AC-05**: `/verify` on an investigation log checks INVESTIGATION_LOG_RULES compliance

## Document History

**[2026-09-09 19:45]**
- Initial specification created
