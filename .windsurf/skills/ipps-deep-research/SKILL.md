---
name: ipps-deep-research
description: Apply when conducting deep research on technologies, APIs, frameworks, or other software development topics requiring systematic investigation
---

# Deep Research Guide

This skill provides systematic research patterns for in-depth investigation of software development topics.

## Verb Mapping

This skill implements:
- [DEEP-RESEARCH-TECH] - Technology/API/framework research (use TECH_RESEARCH_PATTERN.md)

## When to Use Deep Research

Deep research differs from quick lookups:

**Quick Lookup (not this skill)**
- "What's the syntax for X?"
- "How do I install Y?"
- Single-source answers

**Deep Research (this skill)**
- "Should we use X or Y for our project?"
- "How does X work internally?"
- "What are the production considerations for X?"
- Multi-source synthesis required

## MUST-NOT-FORGET

- Always start with source quality assessment
- Primary sources > secondary sources > community opinions
- Document all sources with URLs and access dates
- Flag information age (APIs change rapidly)
- Distinguish facts from opinions from assumptions
- Create INFO document for findings

## Research Principles

### Source Hierarchy

1. **Official documentation** - Authoritative, version-specific
2. **Official blog/changelog** - Announcements, rationale
3. **GitHub repo** - Source code, issues, PRs, discussions
4. **Conference talks by maintainers** - Design decisions, roadmap
5. **Reputable tech blogs** - Analysis, comparisons
6. **Stack Overflow** - Specific problems (verify currency)
7. **Community forums/Discord** - Anecdotes, edge cases

### Information Currency

- Note version numbers for all API/library info
- Check last updated date on documentation
- Cross-reference with changelog for breaking changes
- Mark stale info with `[STALE: YYYY]` tag

### Verification Levels

- `[VERIFIED]` - Tested or confirmed from primary source
- `[CLAIMED]` - Stated in documentation but not tested
- `[REPORTED]` - Community reports, may vary
- `[ASSUMED]` - Inferred, needs verification

## Integration with MEPI/MCPI

This skill extends the MEPI/MCPI principle from `research-and-report-writing-rules.md`:

- **MEPI** (default): Curated findings with 2-3 key options
- **MCPI**: Exhaustive findings when stakes are high

Deep research typically produces MEPI output unless explicitly requested otherwise.

## Output Format

Deep research outputs an INFO document following `write-documents` skill templates. Key sections:

1. **Research Question** - What we're investigating
2. **Key Findings** - MEPI-style summary (2-3 main points)
3. **Detailed Analysis** - Full investigation results
4. **Sources** - All references with quality indicators
5. **Recommendations** - Actionable conclusions

## Research Patterns

Available patterns (each has its own template):

- `TECH_RESEARCH_PATTERN.md` - Technology/API/framework evaluation

## Usage

1. Identify research type (technology, decision, problem-solving)
2. Read this SKILL.md for core principles
3. Read the appropriate pattern template
4. Follow the pattern's phases systematically
5. Output findings as INFO document
