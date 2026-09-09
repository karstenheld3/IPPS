---
description: Find flawed assumptions, logic errors, and hidden risks (not rule violations)
auto_execution_mode: 1
---

# Devil's Advocate

Profile: Senior engineer hunting flawed assumptions, design and logic errors. Not formatting or conventions.

Golden Rule: NEVER touch originals. Create/update `_REVIEW` suffix files only.

Scope: Assumptions and logic/design flaws only. `/verify` handles rule violations. Zero overlap.

## Required Skills

- @write-documents for document review (REVIEW_TEMPLATE.md, FAILS_TEMPLATE.md)

## Output Files

- `[filename]_REVIEW.md` - Problems in specific document/code (risks, edge cases, hypothetical failures, questions). Created fresh each review.
- `_PROBLEMS_REVIEW.md` - Problems from conversation/logs review (no specific file). General issues spanning multiple files.
- `FAILS.md` - Actual failures: wrong assumptions, suboptimal designs, spec problems found after coding, untested behavior that broke. Lessons-learned memory read during `/prime`. Never delete, only append.

## Workflow

1. Determine context (Code, Document, Conversation, Logs)
2. Read `FAILS.md` first (if exists)
3. Read GLOBAL-RULES
4. Read relevant Context-Specific section
5. Create internal MUST-NOT-FORGET list - constraints, user requirements, critical rules
6. Create MUST-RESEARCH list - 5 topics for industry research
7. Execute research - industry patterns, alternatives, known pitfalls
8. Create Devil's Advocate task list (informed by research)
9. Work through task list:
   - Update `_PROBLEMS_REVIEW.md` with potential issues
   - Update `FAILS.md` with actual failures discovered
   - Check MUST-NOT-FORGET list after each major finding
   - Include research findings in analysis
10. Run Final Checklist
11. Verify against MUST-NOT-FORGET list

## GLOBAL-RULES

Mindset: Assume every assumption is wrong. Prove the logic is sound.

DO focus on:
- Flawed assumptions about data, environment, behavior
- Logic errors and incorrect reasoning
- Hidden complexity and edge cases
- What happens when things fail unexpectedly
- Contradictions between stated intent and actual behavior

DO NOT focus on (use `/verify`):
- Rule violations, formatting, style, naming conventions, missing doc sections

Working Rules:
- Never edit originals - `_REVIEW` suffix copies only
- Research before assuming - web searches to verify claims, find failure examples
- Question assumptions - what are we taking for granted?
- Be specific - cite line numbers, exact scenarios
- Prioritize by impact - critical logic flaws first

Categories/Labels: See FAILS_TEMPLATE.md and REVIEW_TEMPLATE.md in @write-documents.

## Research Phase

After MUST-NOT-FORGET list, identify 5 topics:

1. Core pattern/approach - industry pattern used? Better alternatives?
2. Known failure modes - what breaks in production?
3. Security considerations - attack vectors?
4. Scalability patterns - how do others handle growth?
5. Testing strategies - what approaches work?

For each topic: web search for patterns/post-mortems, find alternatives, note sources. Add "Industry Research Findings" section to `_REVIEW.md`.

## Context-Specific Sections

### No Document (Conversation Review)

1. Re-read everything: conversation, code changes, logs, console output
2. Hunt for flawed assumptions:
   - Data shape or availability assumptions
   - Execution order or timing assumptions
   - External system behavior assumptions
   - Happy-path-only logic failing on edge cases
   - Contradictions between said and done
   - Decisions based on incomplete information
3. Create/Update `_PROBLEMS_REVIEW.md` with: Critical Issues, High/Medium Priority, Questions That Need Answers
4. Update `FAILS.md` with any failures found

### Document Review

INFO:
- Sources still accessible? Try accessing them
- Findings actually supported by sources, or extrapolated?
- Contradictory information? Search for it
- What changed since written? Version numbers and dates still accurate?

SPEC:
- What happens when [X] fails? (every external dependency)
- Invalid input? Empty input? Huge input?
- Concurrent access scenarios?
- Implicit unstated assumptions?
- What would a malicious user try?
- Success criteria measurable and testable?

IMPL:
- Plan match spec exactly? Mental diff
- Steps that could fail silently?
- Cleanup needed if step N fails after N-1 succeeds?
- Rollback scenarios defined?
- What if interrupted mid-way?

TEST:
- What's NOT being tested?
- Edge cases from SPEC all covered?
- Integration points assumed to work?
- Tests that can fail for wrong reasons (flaky)?
- Test dependencies isolated?

### Code Review

Meta-principle: Where is complexity hiding, and who pays long-term?

Create `[filename]_REVIEW.md`.

Architectural questions first:

1. Explicit invariants - where enforced? Unenforced → latent bugs, silent corruption
2. Single source of truth - how is divergence detected/prevented? Multiple authorities drift
3. Failure strategy - fail fast or degrade gracefully? Does choice preserve guarantees?
4. Unnecessary dimensions - extra code paths, modes, abstractions to eliminate? Each multiplies complexity
5. Testability - core logic testable without mocks, global state, time? Reflects separation of concerns

Implementation details:

Error Handling: Every try/catch - what specific errors? Every async call - timeout/reject/unexpected shape? Every file op - missing/permissions/disk full? Every network call - DNS/reset/partial response?

State Management: Global state corruption? Called twice rapidly? Stale data? Memory leaks (listeners, timers, closures)?

Dependencies: Version assumptions? Breaking changes in newer versions? Unavailable at runtime? Circular?

Security: Input validation (SQLi, XSS, path traversal)? Auth bypass? All paths authorized? Secrets externalized?

Performance: Worst-case complexity? Data grows 100x? N+1 queries? Unbounded loops/recursion?

### Logs/Console Output Review

1. Categorize each error/warning: expected+handled, expected+unhandled, unexpected
2. Trace to root cause - don't stop at symptoms
3. Check patterns: repeated=systemic, timing=race condition, cascading=missing error boundaries
4. Update `_PROBLEMS_REVIEW.md` and `FAILS.md` with root causes

## Devil's Advocate Questions (EVERY review)

1. Worst thing that could happen?
2. Environment assumptions?
3. What happens when [external system] is down?
4. 0 items? 1 item? 1 million items?
5. Runs twice? Concurrently?
6. Sensitive data leaking in logs/errors?
7. Deployed at 3 AM during database migration?
8. What would a new team member misunderstand?

## Final Checklist

- [ ] `FAILS.md` updated with actual failures (categorized by severity)
- [ ] `[filename]_REVIEW.md` created for specific document/code review
- [ ] `_PROBLEMS_REVIEW.md` created only for conversation/logs review (no specific file)
- [ ] No original files modified
- [ ] Each finding has: What, Where, Why it went wrong, Suggested fix
- [ ] Critical issues highlighted at top
- [ ] Questions needing answers listed
- [ ] MUST-RESEARCH list created - 5 topics researched
- [ ] Industry Research Findings section added to review file
- [ ] Research done for uncertain claims
- [ ] MUST-NOT-FORGET list verified - all constraints checked

## Output Format

```
## Devil's Advocate Summary

Reviewed: [What was reviewed]
Time spent: [Duration]

Research Topics Investigated:
1. [Topic 1] - [Key finding]
2. [Topic 2] - [Key finding]
3. [Topic 3] - [Key finding]
4. [Topic 4] - [Key finding]
5. [Topic 5] - [Key finding]

Findings:
- CRITICAL: [count]
- HIGH: [count]
- MEDIUM: [count]
- LOW: [count]

Top 3 Risks:
1. [Most critical issue - one line]
2. [Second most critical - one line]
3. [Third most critical - one line]

Industry Alternatives Identified:
- [Alternative approach worth considering]

Files Created/Updated:
- `FAILS.md` - [X] new entries
- `[filename]_REVIEW.md` - Detailed findings + Industry Research

Recommendation: [PROCEED / PROCEED WITH CAUTION / STOP AND FIX]
```