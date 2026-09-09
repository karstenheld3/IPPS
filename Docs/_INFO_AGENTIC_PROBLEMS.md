# INFO: Agentic Problems and Failure Patterns

**Doc ID**: AGNTPROB-IN01
**Goal**: Categorize and record recurring agentic failure patterns observed during AI-assisted development

## MUST-NOT-FORGET

- **Categories**: Mutually exclusive problem categories. Each captures a distinct causal mechanism that must be addressed individually. Minimal overlap.
- **Failure Modes**: Observable behavior and patterns. May be caused by multiple categories. A failure mode is what you SEE; a category is WHY it happens.
- **Instances**: Concrete examples of failure. Every instance must reference at least 1 category and at least 1 failure mode.
- Do NOT record fix suggestions - only record and categorize the problem
- Every instance MUST link to its FAILS.md entry if one exists

## Summary

- 4 categories, 5 failure modes, 1 instance recorded
- Categories: Attention Dilution, Context Processing Variance, Hallucination, Probabilistic Variance
- Failure Modes: Constraint Decay, Process Discipline Collapse, Budget Misallocation, Self-Correction Shortcutting, Context Bleeding

## Table of Contents

- [1. Categories](#1-categories)
- [2. Failure Modes](#2-failure-modes)
- [3. Instances](#3-instances)

## 1. Categories

### CAT-01: Attention Dilution

A rule or constraint is loaded in the context window but does not activate at the moment of action. The agent "knows" the rule (it is present in system prompt or loaded rules) but generates output that violates it because task-local signals (immediate goal, user-provided artifacts, pattern completion) have stronger attention weight than the preventive constraint.

**Mechanism**: Preventive rules (negative constraints like "never do X") compete with generative signals (positive task completion like "write a good example"). At generation time, the concrete task dominates the abstract constraint. The rule's presence in context is necessary but insufficient for compliance.

**Distinguishing feature**: The rule was verifiably in context. The agent did not lack the information - it failed to apply it at the critical moment.

### CAT-02: Context Processing Variance

Depth of context processing and reasoning varies across models and across runs of the same model. More context capacity enables broader analysis but does not guarantee deeper analysis. The agent may read all sources but extract surface-level information from some while deeply analyzing others.

**Mechanism**: Models allocate reasoning effort unevenly across input material. A 200-page source corpus may receive thorough analysis for the first 50 pages and shallow scanning for the rest. This is not random - it correlates with token position, source complexity, and how well the content matches the model's training distribution.

**Distinguishing feature**: The input was available and accessible. The agent processed it but extracted less value than the material contained.

### CAT-03: Hallucination

The agent fills information gaps with probabilistic completions that are indistinguishable from factual statements. Missing data, ambiguous sources, or insufficient context trigger the model to generate plausible-sounding but fabricated content.

**Mechanism**: LLMs generate text token-by-token based on probability distributions. When source material does not contain the answer, the model generates the most likely continuation rather than acknowledging the gap. The output reads identically to verified facts - no syntactic or stylistic signal distinguishes hallucinated content from grounded content.

**Distinguishing feature**: The information was not in any source. The agent invented it rather than reporting a gap.

### CAT-04: Probabilistic Variance

Same input produces different outputs across runs due to sampling mechanics (temperature, top-p, random seed). Small differences in prompt phrasing, context ordering, or token boundaries can produce materially different results.

**Mechanism**: LLM inference involves stochastic sampling from probability distributions. Even at low temperature, multiple tokens may have near-equal probability, creating branching points where different runs diverge. These divergences compound through the generation, producing structurally different outputs from identical inputs.

**Distinguishing feature**: Nothing changed in the input, rules, or context. The output simply differed between runs.

## 2. Failure Modes

Observable behavior and patterns. Each failure mode may be caused by one or more categories.

### FM-01: Constraint Decay

Agent forgets or ignores constraints after a measureable amount of tokens of task-focused generation. Rules loaded at the start of a conversation or task progressively lose influence as the generation continues.

- **Observable**: Rule compliance drops as output length increases. Early sections follow constraints; later sections violate them.
- **Measured**: ~97% compliance on output structure rules vs ~45% compliance on process discipline rules (DRAFT_VORTRAG.md, line 168)
- **Caused by**: CAT-01 (Attention Dilution), CAT-04 (Probabilistic Variance)

### FM-02: Process Discipline Collapse

Agent maintains output format (headings, structure, naming) but abandons process rules (verification steps, source checking, confirmation gates). Structural compliance masks procedural non-compliance.

- **Observable**: Output looks correct but was produced by skipping required steps. The result may be right by accident but the process was not followed.
- **Measured**: 97% output structure compliance vs 45% process discipline compliance (DRAFT_VORTRAG.md, line 168)
- **Caused by**: CAT-01 (Attention Dilution), CAT-02 (Context Processing Variance)

### FM-03: Budget Misallocation

Agent allocates token/compute budget disproportionately to answer generation over verification, compliance checking, or source analysis. The agent prioritizes producing output over ensuring that output is correct.

- **Observable**: Agent produces long, detailed answers but skips verification steps, source cross-referencing, or rule compliance checks that would have caught errors.
- **Caused by**: CAT-01 (Attention Dilution), CAT-02 (Context Processing Variance)

### FM-04: Self-Correction Shortcutting

When detection and correction happen in the same pass, the agent shortcuts on detection to preserve budget for correction. Combined detect+correct passes produce shallow analysis.

- **Observable**: Agent reports "no issues found" or finds only surface-level problems when detection and correction share a single generation pass. Separating into two passes (read-only detection, then correction) reveals significantly more issues.
- **Caused by**: CAT-01 (Attention Dilution), CAT-02 (Context Processing Variance)

### FM-05: Context Bleeding

Information from user-provided artifacts (screenshots, conversation history, example files) leaks into outputs where it does not belong. The agent treats contextual input as template material.

- **Observable**: Private paths, names, project-specific identifiers, or user-provided examples appear in reusable templates, generic documentation, or outputs intended for different audiences.
- **Caused by**: CAT-01 (Attention Dilution)

## 3. Instances

### INST-001: Private path leaked into reusable template

- **FAILS ref**: `GLOB-FL-034`
- **Date**: 2026-07-08
- **Categories**: CAT-01 (Attention Dilution)
- **Failure modes**: FM-05 (Context Bleeding)
- **What happened**: Agent added CV-LN-04 rule to CONVERSATION_TEMPLATE.md requiring absolute file links. Used a real private Dropbox filesystem path as the example, copied from the user's screenshot. The template is a reusable skill file deployed to all linked repositories.
- **Rule violated**: `agent-behavior.md` L63: "Never leak project-specific or private data into workflows, skills, or rules."

## Sources

- `AGNTPROB-IN01-SC-IPPS-FAILS`: `E:\Dev\IPPS\FAILS.md` - 34 failure entries (GLOB-FL-001 through GLOB-FL-034)
- `AGNTPROB-IN01-SC-IPPS-LEARN`: `E:\Dev\IPPS\LEARNINGS.md` - 2 learning entries (AMSW-LN-001, MCPS-LN-001)
- `AGNTPROB-IN01-SC-KWRK-DRAFT`: `E:\Dev\KarstensWorkspace\_Sessions\_2026-07-02_AgentischesDesignVortrag\DRAFT_VORTRAG.md` - Presentation draft identifying 4 root causes and compliance measurements

## Document History

**[2026-07-08 11:48]**
- Restructured: 3-tier model (Categories, Failure Modes, Instances)
- Added: CAT-02 (Context Processing Variance), CAT-03 (Hallucination), CAT-04 (Probabilistic Variance)
- Added: FM-01 through FM-05
- Updated: MNF, Summary, ToC, INST-001
- Source: DRAFT_VORTRAG.md (4 root causes, 97%/45% compliance measurements)

**[2026-07-08 11:44]**
- Initial document created
- Added: CAT-01 (Attention Dilution)
- Added: INST-001 (GLOB-FL-034, private path in template)
