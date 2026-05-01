# INFO: SOCAS - Signs of Confusion and Sloppiness

**Doc ID**: SOCAS-IN01
**Goal**: Define criteria for detecting confusion and sloppiness in documents, code, specifications, and organizational outputs
**Timeline**: Created 2026-03-06

## Summary

SOCAS is a quality evaluation heuristic with 15 criteria for detecting degradation in:
- Agent outputs (research, code, specifications)
- Human documents (specs, plans, communications)
- Organizational outputs (websites, policies, processes)
- Researched sources (libraries, frameworks, APIs, tools)

Use during `/verify`, `/critique`, `/improve`, and `/research` workflows.

## Table of Contents

1. [Purpose](#1-purpose)
2. [The 15 SOCAS Criteria](#2-the-15-socas-criteria)
3. [Application Contexts](#3-application-contexts)
4. [Sources](#4-sources)
5. [Next Steps](#5-next-steps)
6. [Document History](#6-document-history)

## 1. Purpose

SOCAS detects early warning signs that indicate:
- Lack of clear thinking or planning
- Rushed or careless execution
- Missing quality control processes
- Organizational dysfunction

When multiple SOCAS criteria are present, the output likely needs rework or the source is unreliable.

## 2. The 15 SOCAS Criteria

### SOCAS-01: Inconsistencies

Any type of inconsistency signals confusion:
- Same concept named multiple ways
- Same word used for different things
- Contradicting statements within same document
- Format/style inconsistencies without reason

### SOCAS-02: Ambiguous Naming and Wording

Lack of clear naming scheme:
- Undefined or hand-wavy concepts
- Key nouns without clear definition or boundaries
- Names that could mean multiple things
- Missing glossary for domain terms

### SOCAS-03: Overlapping Concerns

Redundancy with deviation indicates poor design:
- Two components doing the same job differently
- Concept overlap without clear boundaries
- Responsibilities split inconsistently
- Duplicate mechanisms with slight variations
- Items in same grouping at wildly different levels of detail ("Revenue trends" next to "Johnson account")

### SOCAS-04: Undisclosed Contact Information

Organizational red flag:
- Generic email addresses only (info@, contact@)
- No named contacts for specific concerns
- Hidden or hard-to-find contact details
- No escalation path documented

### SOCAS-05: Ineffective Communication

Forces unnecessary communication loops:
- Information scattered across multiple documents
- Critical details buried in noise
- Missing context requiring follow-up questions
- No clear owner or decision maker identified

### SOCAS-06: Incomplete Specifications

Mixing suggestions with requirements:
- No clear distinction between MUST, SHOULD, MAY
- Underspecified behavior for edge cases
- Implicit assumptions left unstated
- Conclusions not supported by evidence

### SOCAS-07: Confusing Elements

Funny but confusing additions:
- Jokes or humor that obscures meaning
- Creative naming that sacrifices clarity
- Excessive metaphors or analogies
- Easter eggs in serious documentation

### SOCAS-08: Information vs Noise Imbalance

Poor signal-to-noise ratio:
- Relevant details buried in irrelevant additions
- Verbose explanations of obvious things
- Missing explanations of complex things
- Filler content without substance

### SOCAS-09: Lack of Structure

Unstructured writing:
- No clear headings or sections
- Missing enumerations for lists
- No identifiers for referenceable content
- Wall-of-text formatting
- No table of contents for long documents

### SOCAS-10: Gaps in Reasoning

Logical inconsistencies:
- Conclusions not supported by evidence
- Missing steps in explanations
- Assumptions presented as facts
- No explicit tradeoffs or alternatives discussed
- Selection not justified ("Three problems..." - why these three and no others?)

### SOCAS-11: Unnecessary Complexity

Abstractions that don't earn their cost:
- Over-engineered solutions for simple problems
- Jargon where plain language works
- Deep nesting without clear benefit
- Indirection without purpose

### SOCAS-12: Presentation Sloppiness

Surface-level quality issues:
- Typos and grammatical errors
- Stale or broken references
- Inconsistent formatting
- Outdated information mixed with current
- Outdated, abandoned, or unsupported code (deprecated with no successor, unresolved issues, no maintainer response)

### SOCAS-13: Empty Structure

Structure present but hollow - author organized without synthesizing:
- Headings label categories instead of stating ideas ("Background", "Analysis", "Results")
- Main point buried at end or absent entirely
- Section summaries describe what the section covers, not what was found
- No stated purpose - reader cannot tell why the document exists

### SOCAS-14: Arbitrary Sequencing

Items dumped without analyzing relationships:
- Items in lists appear in no discernible order
- No logical, chronological, structural, or importance-based sequence
- Reader cannot determine why item 2 follows item 1

### SOCAS-15: Net-Negative Adoption

Solution introduces more problems than it solves - detectable through community research:
- GitHub issues dominated by workarounds for the tool's own limitations
- Community forums show recurring migration-away discussions
- Known problems acknowledged by maintainers but unresolved across major versions
- Adopters report increased complexity, debugging time, or breaking changes disproportionate to value gained

## 3. Application Contexts

### Agent Output Review

Use during `/verify`, `/critique`, and `/improve`:
- Check generated specs against SOCAS criteria
- Flag research documents with high SOCAS score
- Require rework when 3+ criteria violated

### Document Review

Apply when reviewing human-authored documents:
- Technical specifications
- API documentation
- Process descriptions
- Requirements documents

### Source Evaluation

Use during `/research` to rank sources:
- High SOCAS = unreliable source
- Prefer sources with low SOCAS indicators
- Document SOCAS findings in source notes

### Organizational Assessment

Evaluate organizations by their outputs:
- Website clarity and structure
- Documentation quality
- Communication effectiveness
- Process transparency

### UX Design Review

Apply when evaluating user interfaces:
- Breaking established patterns without substantial gain
- Broken proximity of related UX elements
- No tab order and keyboard support for users without mouse
- No copy functionality for relevant textual information
- Unclear visual hierarchy
- Unestablished commands for standard operations (instead of OK, Cancel, Save, Load)
- Application deletes or loses data without user confirmation
- Users can accidentally close dialogs with entered data by clicking outside

