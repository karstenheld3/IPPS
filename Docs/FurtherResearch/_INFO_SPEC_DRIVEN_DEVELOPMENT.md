# INFO: Spec-Driven Development (SDD)

**Doc ID**: SDDEV-IN01
**Goal**: Research and document the Spec-Driven Development methodology, tools, benefits, and limitations
**Timeline**: Created 2026-01-23, Updated 1 time

## Summary

- Spec-Driven Development (SDD) is a methodology where a formal, machine-readable specification serves as the authoritative source of truth [VERIFIED]
- Three implementation levels: spec-first, spec-anchored, spec-as-source [VERIFIED]
- Four-phase lifecycle: Specify, Plan, Task, Implement [VERIFIED]
- Primary use case: AI-assisted development with coding agents [VERIFIED]
- Key tools: Kiro (AWS), Spec Kit (GitHub), Tessl Framework [VERIFIED]
- Main benefit: Prevents "vibe coding" inconsistencies by providing structured intent [VERIFIED]
- Main limitation: Workflow overhead may exceed value for small changes [VERIFIED]
- SDD is still semantically diffuse - term used inconsistently across industry [VERIFIED]

## Table of Contents

1. [Definition](#1-definition)
2. [History](#2-history)
3. [Core Concepts](#3-core-concepts)
4. [Implementation Levels](#4-implementation-levels)
5. [Tools](#5-tools)
6. [Benefits](#6-benefits)
7. [Limitations and Criticisms](#7-limitations-and-criticisms)
8. [Comparison with Other Methodologies](#8-comparison-with-other-methodologies)
9. [Sources](#9-sources)
10. [Document History](#10-document-history)

## 1. Definition

**Spec-Driven Development (SDD)** is a software engineering methodology where:
- A formal, machine-readable specification serves as the authoritative source of truth
- Implementation, testing, and documentation are derived from the specification
- System intent is explicitly defined in structured format (OpenAPI, Markdown) before implementation

**Key distinction from traditional development:** Documentation is proactive (written first), not retrospective.

**In AI context:** SDD transforms specifications into executable blueprints for coding agents, preventing inconsistencies associated with ad-hoc "vibe coding."

**Definition per GitHub:** "In this new world, maintaining software means evolving specifications. The lingua franca of development moves to a higher level, and code is the last-mile approach."

**Definition per Tessl:** "A development approach where specs - not code - are the primary artifact. Specs describe intent in structured, testable language, and agents generate code to match them."

## 2. History

- **1960s**: Roots trace to NASA workflows and early formal methods prioritizing logic verification before coding
- **2004**: Related concepts (Test-Driven Development (TDD), Design by Contract (DbC)) formalized; term "SDD" emerged later with AI coding tools
- **2020s**: Renaissance driven by Large Language Model (LLM)-powered agentic workflows

**Parallel to Model-Driven Development (MDD):**
- Model-Driven Development (MDD) used models (Unified Modeling Language (UML), Domain-Specific Languages (DSLs)) as specs with custom code generators
- MDD never took off for business applications (awkward abstraction, overhead)
- LLMs remove some MDD constraints (no predefined spec language, no elaborate generators)
- Trade-off: LLMs introduce non-determinism

## 3. Core Concepts

### 3.1 Four-Phase Lifecycle

1. **Specify**: Define functional requirements (what, why, user journeys, success criteria)
2. **Plan**: Translate intent into technical architecture (stack, constraints, compliance)
3. **Task**: Decompose plan into atomic, reviewable units
4. **Implement**: Automated code generation with human validation

### 3.2 Spec vs Context

- **Spec**: Behavior-oriented artifact relevant to specific functionality
- **Context/Memory Bank**: General codebase context (rules files, product descriptions) relevant across all sessions

### 3.3 Human Role

- **Steering**: Provide high-level direction
- **Verification**: At each phase, reflect and refine. Verify correctness before moving forward.

## 4. Implementation Levels

Three distinct levels of SDD adoption:

1. **Spec-First**
   - Spec written first, used for current task
   - Most common approach
   - Spec may be discarded after task completion

2. **Spec-Anchored**
   - Spec kept after task completion
   - Used for evolution and maintenance
   - Spec becomes living artifact for feature lifetime

3. **Spec-As-Source**
   - Spec is the only artifact humans edit
   - Code marked with comments like `// GENERATED FROM SPEC - DO NOT EDIT`
   - Human never touches code directly
   - Only Tessl Framework explicitly pursues this level

## 5. Tools

### 5.1 Kiro (AWS)

- VS Code-based distribution
- Workflow: Requirements -> Design -> Tasks
- Each step = one markdown document
- Lightest of the three tools
- Memory bank called "steering" (product.md, structure.md, tech.md)
- Primarily spec-first (no explicit spec-anchored approach)

### 5.2 Spec Kit (GitHub)

- CLI tool, works with multiple agents (Copilot, Claude Code, Gemini CLI)
- Workflow: Constitution -> Specify -> Plan -> Tasks (iterative)
- Constitution = powerful rules file (immutable principles)
- Heavy use of checklists for tracking
- Creates branch per spec
- Commands: `/specify`, `/plan`, `/tasks`
- Creates many markdown files - verbose review overhead
- Currently spec-first despite aspirations to spec-anchored

### 5.3 Tessl Framework

- CLI + MCP server
- Still in private beta
- Only tool explicitly pursuing spec-as-source
- 1:1 mapping between spec and code files
- Can reverse-engineer specs from existing code (`tessl document --code`)
- Build command: `tessl build`
- Tags: `@generate`, `@test` for generation control

## 6. Benefits

1. **Clarity for AI agents**: Specification provides structured guidance, reducing guesswork
2. **Stakeholder alignment**: Clear documentation of goals and requirements
3. **Version-controlled intent**: Changes tracked, not lost in prompts
4. **Separation of concerns**: Stable "what" from flexible "how"
5. **Faster iteration**: Update spec, regenerate plan, rebuild

**Three ideal scenarios (per GitHub):**
- **Greenfield**: New projects benefit from upfront clarity
- **Feature work in existing systems**: Forces clarity on interactions with existing code
- **Legacy modernization**: Capture business logic in modern spec, rebuild without technical debt

**Benefits per Kiro:**
- Agreement between developers and stakeholders
- Guide for AI agents (North Star)
- Tames chaos of prompt-driven coding
- Specification = version-controlled super-prompt

## 7. Limitations and Criticisms

### 7.1 Workflow Overhead and Natural Language Ambiguity

- One-size-fits-all workflow problematic
- Small bugs: sledgehammer to crack a nut
- Medium features: too much markdown, too many files
- Reviewing markdown often more tedious than reviewing code
- Natural language specs are inherently ambiguous; to remove ambiguity, specs must become so detailed they approach code complexity

### 7.2 False Sense of Control

- Larger context windows do not guarantee AI follows all instructions
- Agents ignore instructions or duplicate existing code
- Agents may over-eagerly follow certain rules

### 7.3 Functional vs Technical Separation

- Confusion about when to stay functional vs add technical details
- Industry has poor track record separating requirements from implementation

### 7.4 Target User Ambiguity

- Unclear if developers should do requirements analysis
- Product skills may be needed for larger features

### 7.5 Semantic Diffusion

- Term "spec" used as synonym for "detailed prompt"
- Definition still in flux across industry

### 7.6 MDD Parallels (Concern)

- Risk of combining MDD downsides (inflexibility) with LLM downsides (non-determinism)
- Worth studying past code-from-spec attempts

## 8. Comparison with Other Methodologies

- **TDD (Test-Driven Development)**: Focuses on correctness at implementation level. SDD uses spec to generate initial tests.
- **BDD (Behavior-Driven Development)**: Focuses on user-facing scenarios. SDD provides structural/architectural invariants BDD scenarios must satisfy.
- **MDD (Model-Driven Development)**: Model as primary artifact. SDD similar but uses natural language and LLMs instead of DSLs/generators.

**Related concepts:**
- Model-Driven Engineering
- Behavior-Driven Development
- Formal Methods
- Design by Contract

## 9. Sources

**Primary Sources:**

- `SDDEV-IN01-SC-WIKI-SDD`: https://en.wikipedia.org/wiki/Spec-driven_development - Wikipedia article with definition, history, core concepts [VERIFIED]
- `SDDEV-IN01-SC-FOWL-SDD3T`: https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html - Birgitta Bockeler's analysis of Kiro, Spec Kit, Tessl (Oct 2025 article) [VERIFIED]
- `SDDEV-IN01-SC-GHUB-SPKIT`: https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/ - GitHub's Spec Kit announcement and methodology [VERIFIED]
- `SDDEV-IN01-SC-KIRO-FUTR`: https://kiro.dev/blog/kiro-and-the-future-of-software-development/ - AWS Kiro's vision for SDD [VERIFIED]

**Critical Perspectives:**
- `SDDEV-IN01-SC-ARCT-SCALE`: http://arcturus-labs.com/blog/2025/10/17/why-spec-driven-development-breaks-at-scale-and-how-to-fix-it/ - Arcturus Labs on SDD limitations at scale [VERIFIED]

**Discovered but not consulted:**
- `SDDEV-IN01-SC-MSFT-SPKIT`: https://developer.microsoft.com/blog/spec-driven-development-spec-kit - Microsoft Developer Blog on Spec Kit [DISCOVERED]
- `SDDEV-IN01-SC-GHUB-SPDRV`: https://github.com/github/spec-kit/blob/main/spec-driven.md - Spec Kit methodology documentation [DISCOVERED]

## 10. Document History

**[2026-01-23 15:10]**
- Added: Natural language ambiguity limitation (Section 7.1)
- Changed: Softened 2004 historical claim to reflect term emergence
- Added: Critical source (Arcturus Labs)

**[2026-01-23 15:02]**
- Initial research document created
- Sources: Wikipedia, Martin Fowler, GitHub Blog, Kiro Blog
