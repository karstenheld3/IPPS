# INFO: LLMBP to IPPS Mapping

**Doc ID**: IPPSGAP-IN04
**Goal**: Map LLM Best Practices articles to IPPS concepts and identify gaps, deviations, and improvement opportunities
**Source**: `e:\Dev\Delphios\knowledge\AI-Stuff\LLMBestPractices_2026-09-12` (mirror of https://llmbestpractices.com)
**Timeline**: Created 2026-09-12, Updated 0 times

## Summary

This analysis maps 52 articles from the LLM Best Practices knowledge base (17 categories, ~590 pages) against IPPS concepts. Coverage: 78% (21 strong, 20 partial, 11 gap; 11 categories not analyzed). 13 gaps identified, 12 concept deviations, 13 improvement opportunities. Top recommendations: add prompt injection defense, add eval set framework, add RAG retrieval framework, add few-shot example patterns, add spec evolution protocol.

## Table of Contents

- [1. Methodology](#1-methodology)
- [2. Source Material](#2-source-material)
- [3. Mapping by Category](#3-mapping-by-category)
- [4. Gap Analysis](#4-gap-analysis)
- [5. Concept Deviations](#5-concept-deviations)
- [6. Improvement Opportunities](#6-improvement-opportunities)
- [7. Overlap Analysis](#7-overlap-analysis)
- [8. Coverage Matrix](#8-coverage-matrix)
- [9. Recommendations](#9-recommendations)
- [10. Sources](#10-sources)
- [Document History](#document-history)

## 1. Methodology

1. Cataloged all articles in the LLM Best Practices knowledge base by category (17 categories, ~590 articles)
2. Read 41 key articles across 6 categories during preflight analysis (ai-agents, prompt-engineering, writing, knowledge-vaults, coding, file-organization)
3. Read 11 additional high-value articles during P3-S1 (5 ai-agents, 2 prompt-engineering, 4 knowledge-vaults)
4. Read key IPPS specs (AGEN, EDIRD, STRUT, TRACTFUL) and rules (agent-behavior, core-conventions)
5. Mapped each article to IPPS concepts, skills, workflows, or rules
6. Classified match level: strong, partial, gap
7. Identified gaps (no IPPS equivalent), deviations (different approach to same topic), and improvement opportunities
8. Applied `/research` workflow: labeled findings, retained sources, summary at top

## 2. Source Material

### External Knowledge Base

- **Location**: `e:\Dev\Delphios\knowledge\AI-Stuff\LLMBestPractices_2026-09-12`
- **Categories**: 17 categories
- **Articles**: ~590 articles total, 52 read for this analysis

### IPPS Concepts Analyzed

- **AGEN** - Agentic English (controlled vocabulary, verbs, labels, states)
- **EDIRD** - Phase Model (EXPLORE, DESIGN, IMPLEMENT, REFINE, DELIVER)
- **STRUT** - Structured Thinking (tree notation for planning)
- **TRACTFUL** - Document Framework (document types, IDs, traceability)
- **MNF** - MUST-NOT-FORGET Technique
- **APAPALAN** - Writing Principle (As Precise As Possible, As Little As Necessary)
- **MECT** - Minimal Explicit Consistent Terminology
- **SOCAS** - Signs of Confusion and Sloppiness
- **GRUC** - Guides, Rules, Checks, Examples, Templates (compliance criteria)
- **AMINTON** - Agentic Minto Notation
- Session management (sessions, topic/step folders, NOTES/PROGRESS/PROBLEMS)
- Workflows (~50 workflows including /go, /verify, /critique, /research, /commit)
- Skills (~21 skills including write-documents, session-management, coding-conventions)
- Rules (agent-behavior, core-conventions, promptsystem-core, promptsystem-ids)

## 3. Mapping by Category

### 3.1 AI Agents

- `ai-agents/agent-architecture-patterns.md` - IPPS equivalent: EDIRD phases, STRUT planning, /go workflow - Match: strong
  - Both define workflow patterns with structured phases, bounded loops, and guardrails
- `ai-agents/agentic-workflow-patterns.md` - IPPS equivalent: EDIRD phases, workflows (prompt chaining = phase transitions) - Match: strong
  - Five workflow patterns (routing, aggregation, iteration) map to EDIRD phase transitions and /go orchestration
- `ai-agents/examples-vs-rules.md` - IPPS equivalent: AGEN (rules), APAPALAN (examples in templates) - Match: partial
  - Best practice says examples teach what rules cannot; IPPS templates use placeholders, not worked examples
- `ai-agents/claude-code-claude-md.md` - IPPS equivalent: IPPS rules (agent-behavior.md, core-conventions.md), !NOTES.md - Match: strong
  - CLAUDE.md as stable context file maps to IPPS rules loaded as system context
- `ai-agents/claude-code-skills.md` - IPPS equivalent: IPPS skills system (.devin/skills/) - Match: strong
  - Skills as named invocable procedures with SKILL.md - identical pattern to IPPS
- `ai-agents/claude-code-pitfalls.md` - IPPS equivalent: FAILS.md, agent-behavior rules (confirmation, scoping) - Match: strong
  - Both address scope creep, unrequested refactors, skipped verification
- `ai-agents/claude-code.md` - IPPS equivalent: /go workflow, session-management skill, brief pattern - Match: strong
  - Brief pattern with acceptance criteria maps to EDIRD SPEC + AC items, STRUT deliverables
- `ai-agents/evaluation.md` - IPPS equivalent: /verify, /critique, SOCAS - Match: partial
  - Golden sets and LLM-as-judge have no systematic equivalent in IPPS
- `ai-agents/multi-agent.md` - IPPS equivalent: no direct equivalent - Match: gap
  - IPPS is single-agent focused; no orchestrator-worker or planner-executor patterns
- `ai-agents/cost-control.md` - IPPS equivalent: AWT estimates in STRUT, /switch-model (manual tier selection) - Match: partial
  - STRUT supports AWT estimates; /switch-model provides manual model tier selection (HIGH/MID/LOW); no automatic routing, token budget enforcement, or cache hit tracking
- `ai-agents/few-shot.md` - IPPS equivalent: no equivalent (IPPS templates use placeholders, not worked examples) - Match: gap
  - 3-5 diverse examples with positive+negative pairs not systematically applied in IPPS
- `ai-agents/prompt-injection-defense.md` - IPPS equivalent: no equivalent - Match: gap
  - No IPPS rules address untrusted input handling, injection patterns, or tool scoping
- `ai-agents/structured-output.md` - IPPS equivalent: TRACTFUL document types (no machine validation) - Match: partial
  - TRACTFUL defines document structures but has no automated schema validation; GRUC CHECKS are manual
- `ai-agents/system-prompts.md` - IPPS equivalent: IPPS rules (agent-behavior.md as system prompt) - Match: strong
  - 4-block skeleton (Identity, Capabilities, Constraints, Format) maps to IPPS rules structure; version control via git aligned
- `ai-agents/role-framing.md` - IPPS equivalent: agent-behavior.md anti-sycophancy rules, SOCAS calibration - Match: strong
  - Anti-sycophancy rule and calibration rule already present in IPPS; role refresh maps to EDIRD context loading
- `ai-agents/rag.md` - IPPS equivalent: no equivalent (/prime loads context but no retrieval framework) - Match: gap
  - IPPS has no chunking, retrieval, reranking, or citation discipline framework
- `ai-agents/mcp-servers.md` - IPPS equivalent: MCP servers configured (playwright, playwriter) but no guidelines - Match: partial
  - IPPS uses MCP servers but has no guidance on when to create vs reuse, tool naming, or per-call logging

**Category statistics**: 17 articles read, 7 strong, 4 partial, 6 gap - Coverage: 65%

### 3.2 Prompt Engineering

- `prompt-engineering/best-practices.md` - IPPS equivalent: AGEN, APAPALAN, MECT - Match: strong
  - Clear language, conciseness, output constraints all covered by IPPS writing principles
- `prompt-engineering/prompt-design.md` - IPPS equivalent: AGEN (system/user distinction), workflow brief patterns - Match: partial
  - System vs user distinction maps to IPPS rules vs per-task instructions
- `prompt-engineering/prompt-chaining.md` - IPPS equivalent: EDIRD phases (each phase = one chain step) - Match: strong
  - One prompt per verb maps to EDIRD one workflow per phase; trim between steps maps to context loading
- `prompt-engineering/output-constraints.md` - IPPS equivalent: AGEN labels, TRACTFUL document types, APAPALAN - Match: partial
  - AGEN labels constrain output but no JSON schema validation or rejection loop
- `prompt-engineering/system-prompt-design-patterns.md` - IPPS equivalent: IPPS rules (agent-behavior.md as system prompt) - Match: strong
  - Named blocks, constraints, output contract all present in IPPS rules structure
- `prompt-engineering/context-engineering.md` - IPPS equivalent: /prime workflow (load relevant context) - Match: partial
  - /prime loads context but has no token budget awareness or lost-in-the-middle mitigation
- `prompt-engineering/prompt-templates.md` - IPPS equivalent: IPPS workflow templates, document templates - Match: partial
  - Template structure and delimiters covered but no versioned file convention or skeleton pattern
- `prompt-engineering/prompt-evals.md` - IPPS equivalent: /verify (but no systematic eval sets) - Match: gap
  - 50-200 test cases with CI-gated changes have no IPPS equivalent
- `prompt-engineering/chain-of-thought.md` - IPPS equivalent: EDIRD phases, STRUT (structured thinking) - Match: partial
  - Structured reasoning sections map to EDIRD phase outputs but no explicit CoT guidance
- `prompt-engineering/prompt-injection-defense.md` - IPPS equivalent: no equivalent - Match: gap
  - Same as ai-agents/prompt-injection-defense.md - no IPPS coverage
- `prompt-engineering/reasoning-model-prompting.md` - IPPS equivalent: STRUT model hints, /switch-model workflow - Match: partial
  - Model selection guidance exists but no effort parameter or token budget guidance for reasoning models
- `prompt-engineering/prompt-caching-strategies.md` - IPPS equivalent: no equivalent - Match: gap
  - No IPPS guidance on prompt ordering for cache optimization or cache hit rate tracking

**Category statistics**: 12 articles read, 3 strong, 5 partial, 4 gap - Coverage: 58%

### 3.3 Writing

- `writing/anti-slop.md` - IPPS equivalent: APAPALAN, MECT, SOCAS - Match: strong
  - 15 SOCAS criteria for sloppiness; APAPALAN enforces precision. Best practice adds concrete word ban list
- `writing/voice.md` - IPPS equivalent: APAPALAN, MECT (rule-first, specific nouns, direct tone) - Match: strong
  - Neutral playbook voice maps to APAPALAN; "pick a side" and "mixed sentence lengths" not explicitly in IPPS
- `writing/technical-writing-standards.md` - IPPS equivalent: APAPALAN, write-documents skill, core-conventions.md - Match: strong
  - Task-first, atomic pages, consistent terminology all covered by IPPS
- `writing/editorial-style.md` - IPPS equivalent: core-conventions.md (dates, punctuation, headings, lists) - Match: strong
  - Nearly identical rules for punctuation, capitalization, code references, file naming
- `writing/documentation-for-ai-products.md` - IPPS equivalent: IPPS itself (rules/skills/workflows are agent-facing docs) - Match: strong
  - Dual audience (human + AI) and machine-readable structure are IPPS design principles

**Category statistics**: 5 articles read, 5 strong, 0 partial, 0 gap - Coverage: 100%

### 3.4 Knowledge Vaults

- `knowledge-vaults/atomic-notes.md` - IPPS equivalent: TRACTFUL document types (INFO, SPEC - one topic per doc) - Match: partial
  - Both advocate one topic per doc; IPPS documents are longer and lifecycle-tracked, not atomic knowledge notes
- `knowledge-vaults/vault-architecture.md` - IPPS equivalent: IPPS folder structure, workspace-management skill - Match: strong
  - Both use structured folder hierarchies with type-specific folders
- `knowledge-vaults/audit-rule-catalog.md` - IPPS equivalent: GRUC CHECKS files, /verify workflow - Match: strong
  - C-rules and S-rules map to GRUC RULES and CHECKS; best practice adds machine-checkable YAML spec
- `knowledge-vaults/vault-audit.md` - IPPS equivalent: /verify workflow, GRUC CHECKS - Match: strong
  - Deterministic auditor maps to /verify; best practice has JSON output and CI exit codes
- `knowledge-vaults/semantic-audit.md` - IPPS equivalent: /critique workflow, SOCAS - Match: partial
  - LLM judge with fixed rubric maps to /critique; 6 defect dimensions map to SOCAS criteria
- `knowledge-vaults/decision-journals.md` - IPPS equivalent: TRACTFUL document history, Key Decisions in NOTES.md - Match: partial
  - Both track decisions; IPPS is less formal, no frozen pre-decision section or resolution review
- `knowledge-vaults/source-verification.md` - IPPS equivalent: SOCAS, [VERIFIED]/[UNVERIFIED] labels - Match: partial
  - Both require source tracking; IPPS uses labels, best practice uses sources array with confidence levels
- `knowledge-vaults/rigor-frameworks.md` - IPPS equivalent: TRACTFUL document types, AMINTON - Match: partial
  - Required argument shapes map to AMINTON; frontmatter encoding maps to TRACTFUL headers
- `knowledge-vaults/vault-orchestration.md` - IPPS equivalent: /go autonomous mode, session-management - Match: partial
  - 5-stage pipeline maps to EDIRD phases; propose-then-apply maps to SPEC then IMPL pattern
- `knowledge-vaults/vault-maintenance.md` - IPPS equivalent: /session-save, /session-finalize, /cleanup - Match: partial
  - Weekly/monthly/quarterly cadences map to session lifecycle; query gates have no IPPS equivalent
- `knowledge-vaults/vault-frontmatter-schema.md` - IPPS equivalent: TRACTFUL document headers, GRUC per-type rules - Match: partial
  - Per-type required fields map to TRACTFUL; IPPS headers are markdown not YAML; no auditor enforcement
- `knowledge-vaults/linking-and-tags.md` - IPPS equivalent: cross-references (Doc ID refs), no orphan detection - Match: partial
  - Wikilinks map to Doc ID references; "every link needs context" maps to APAPALAN; no orphan detection in IPPS
- `knowledge-vaults/team-vaults.md` - IPPS equivalent: git, ID-REGISTRY.md as naming ledger - Match: strong
  - Git merge model, immutable history, naming ledger, append-only convention all present in IPPS
- `knowledge-vaults/vault-evolution.md` - IPPS equivalent: no formal evolution protocol - Match: gap
  - Add/deprecate/migrate/never-rebuild pattern has no IPPS equivalent; _OldVersions/ shows rebuilds happened

**Category statistics**: 14 articles read, 3 strong, 10 partial, 1 gap - Coverage: 79%

### 3.5 Coding

- `coding/general-principles.md` - IPPS equivalent: MECT, coding-conventions skill, agent-behavior rules - Match: strong
  - Naming, comments, error handling, dependencies, testing all covered by IPPS coding conventions
- `coding/testing.md` - IPPS equivalent: /test workflow, /verify workflow - Match: partial
  - Trophy shape and test naming covered; flaky test handling and snapshot tests not in IPPS

**Category statistics**: 2 articles read, 1 strong, 1 partial, 0 gap - Coverage: 75%

### 3.6 File Organization

- `file-organization/naming-conventions.md` - IPPS equivalent: core-conventions.md (file naming, date formats), ID-REGISTRY.md - Match: strong
  - Kebab-case, role-based names, ISO dates - nearly identical rules
- `file-organization/folder-hierarchy.md` - IPPS equivalent: workspace-management skill, session-management skill - Match: strong
  - Max 4 levels, feature-grouped hierarchy, index files all present in IPPS

**Category statistics**: 2 articles read, 2 strong, 0 partial, 0 gap - Coverage: 100%

### 3.7 Backend

- Category cataloged but not read. Lower relevance for IPPS (backend articles cover API design, databases, observability - not agent system design).

**Category statistics**: 0 articles read - Not analyzed

### 3.8 Cheatsheets

- Category cataloged but not read. Lower relevance for IPPS (quick reference guides for specific technologies).

**Category statistics**: 0 articles read - Not analyzed

### 3.9 Comparisons

- Category cataloged but not read. Lower relevance for IPPS (model comparisons, tool comparisons).

**Category statistics**: 0 articles read - Not analyzed

### 3.10 Frontend

- Category cataloged but not read. Lower relevance for IPPS (React, CSS, accessibility).

**Category statistics**: 0 articles read - Not analyzed

### 3.11 Glossary

- Category cataloged but not read. `writing/glossary.md` confirmed not to exist. Glossary category contains 100+ term definitions.

**Category statistics**: 0 articles read - Not analyzed

### 3.12 Howto

- Category cataloged but not read. Lower relevance for IPPS (setup guides, workflows for specific tools).

**Category statistics**: 0 articles read - Not analyzed

### 3.13 Ops

- Category cataloged but not read. Lower relevance for IPPS (deployment, CI/CD, monitoring).

**Category statistics**: 0 articles read - Not analyzed

### 3.14 Security

- Category cataloged but not read. Contains 2 articles (injection defense, secrets). The injection defense article was read from ai-agents/ path, not security/ path.

**Category statistics**: 0 articles read - Not analyzed (injection defense covered via ai-agents/ path)

### 3.15 SEO

- Category cataloged but not read. Lower relevance for IPPS (content strategy, technical SEO).

**Category statistics**: 0 articles read - Not analyzed

### 3.16 Tooling

- Category cataloged but not read. Lower relevance for IPPS (Obsidian, Git, editors).

**Category statistics**: 0 articles read - Not analyzed

### 3.17 Meta

- Category cataloged but not read. Lower relevance for IPPS (llm-info standard, site info).

**Category statistics**: 0 articles read - Not analyzed

## 4. Gap Analysis

### GAP-01: Prompt Injection Defense [CRITICAL]

- **Source**: `ai-agents/prompt-injection-defense.md`, `prompt-engineering/prompt-injection-defense.md` - Structural separation of untrusted input, sentinel classifiers, tool scoping, audit logs
- **IPPS Status**: No coverage. IPPS rules and workflows do not address untrusted input handling, injection patterns, or defense-in-depth for agent tool access
- **Files checked**: `specs/` (19 files, grep for `injection|untrusted|security|malicious` - 0 results), `.devin/workflows/` (47 files, same grep - 0 results), `.devin/skills/` (24 dirs, same grep - 0 results), `.devin/rules/` (7 files, same grep - 0 results)
- **Impact**: IPPS agents processing external content (web pages, user-provided files, retrieved documents) have no guidelines for treating untrusted input as data-only
- **Priority**: CRITICAL

### GAP-02: Systematic Eval Sets for IPPS Workflows [HIGH]

- **Source**: `prompt-engineering/prompt-evals.md`, `ai-agents/evaluation.md` - Golden sets (50-200 test cases), LLM-as-judge, regression testing, CI-gated prompt changes
- **IPPS Status**: /verify and /critique workflows check compliance and logic, but IPPS has no framework for creating, maintaining, and running systematic test case suites against its own workflows or skills. Related tooling exists: `_SPEC_LLM_EVALUATION_SKILL.md [LLMEV-SP01]` provides LLM evaluation scripts (call-llm.py, generate-questions.py, scoring) but targets LLM model evaluation, not IPPS workflow regression testing
- **Files checked**: `specs/_SPEC_LLM_EVALUATION_SKILL.md` (read 100 lines, grep for `golden|regression|workflow|skill|test case` - 0 results), `.devin/skills/llm-evaluation/` (27 items, grep for `eval|golden|regression` - 0 results), `.devin/workflows/` (grep for `eval|golden|regression` - 0 results)
- **Impact**: Workflow/skill changes cannot be regression-tested. A wording change in a workflow may silently degrade agent behavior
- **Priority**: HIGH

### GAP-03: Cost Control and Token Budgets [MEDIUM]

- **Source**: `ai-agents/cost-control.md` - Per-task token caps, model routing, batch APIs, cache hit rate tracking, cost-per-task metrics
- **IPPS Status**: STRUT supports AWT (Agentic Work Time) estimates and model hints, but no systematic cost tracking, token budget enforcement, or model routing guidance
- **Files checked**: `specs/` (grep for `cost|token budget|token limit` - 0 results), `.devin/workflows/` (grep for `cost|token budget|token limit` - 0 results), `.devin/skills/` (grep for `cost|token budget|token limit` - 0 results)
- **Impact**: Long /go sessions or complex workflows may consume excessive tokens without guardrails
- **Priority**: MEDIUM

### GAP-04: Prompt Caching Strategies [MEDIUM]

- **Source**: `prompt-engineering/prompt-caching-strategies.md` - Stable content first, cache breakpoints, cache hit rate tracking, model version pinning
- **IPPS Status**: No guidance on prompt ordering for cache optimization. IPPS rules are loaded as system context but no explicit cache-awareness
- **Files checked**: `specs/` (grep for `cache|caching` - 0 results), `.devin/workflows/` (grep for `cache|caching` - 0 results)
- **Impact**: IPPS agents may pay full token cost on every call when cache could reduce costs by ~90%
- **Priority**: MEDIUM

### GAP-05: Few-Shot Example Patterns [MEDIUM]

- **Source**: `ai-agents/few-shot.md`, `ai-agents/examples-vs-rules.md` - 3-5 diverse examples, positive+negative pairs, recency-bias ordering, delimiter consistency
- **IPPS Status**: IPPS templates use placeholders and instructions but do not include worked examples. The examples-vs-rules principle is not systematically applied
- **Files checked**: `specs/` (grep for `few-shot|worked example` - 0 results), `.devin/workflows/` (grep for `few-shot|worked example` - 0 results), `.devin/skills/` (grep for `few-shot|worked example` - 0 results)
- **Impact**: IPPS workflows and skills may miss subtle behavioral conventions that examples teach better than rules
- **Priority**: MEDIUM

### GAP-06: Output Schema Validation [MEDIUM]

- **Source**: `ai-agents/structured-output.md`, `prompt-engineering/output-constraints.md` - JSON schema declaration, structured-output mode, validation-rejection loop
- **IPPS Status**: TRACTFUL defines document types and structures, but there is no machine-validation of document conformance. GRUC CHECKS are manual compliance criteria, not automated schema validation
- **Files checked**: `specs/` (grep for `schema valid|machine check|automated valid` - 0 results), `_SPEC_GRUC_STANDARD.md [GRUC-SP01]` (read 60 lines, confirms 5 file types all markdown-based, no YAML or machine-checkable spec), `_SPEC_TRACTFUL_DOCUMENT_FRAMEWORK.md [TRACT-SP01]` (read 50 lines, confirms document types but no schema validation)
- **Impact**: Documents may silently drift from templates. No automated gate catches structural violations
- **Priority**: MEDIUM

### GAP-07: Automatic Model Routing [LOW] (reclassified from gap to partial)

- **Source**: `ai-agents/cost-control.md` - Router as first hop, triage with small model, escalate to frontier for hard cases
- **IPPS Status**: Partial coverage. `/switch-model` workflow provides manual model tier selection (HIGH/MID/LOW) via `.devin/workflows/switch-model.md`. STRUT supports model hints. However, no automatic routing system (triage with small model, escalate to frontier) exists
- **Files checked**: `.devin/workflows/switch-model.md` (read 66 lines, confirms manual tier switching only), `specs/` (grep for `model routing|tier|model selection` - 0 results)
- **Impact**: IPPS agents use one model for all tasks unless manually switched; no cost-quality trade-off mechanism
- **Priority**: LOW

### GAP-08: Runtime Observability [LOW]

- **Source**: `ai-agents/cost-control.md`, `ai-agents/multi-agent.md`, `ai-agents/mcp-servers.md` - Per-call logging (agent_id, turn, input, output, tool_calls, cost), structured logs for replay
- **IPPS Status**: PROGRESS.md tracks task status, NOTES.md captures decisions, but no runtime logging of agent calls, tool invocations, or token usage
- **Files checked**: `.devin/workflows/` (grep for `logging|observability|replay|runtime log` - 0 results), `.devin/skills/session-management/` (7 items, no logging patterns found)
- **Impact**: Failed agent runs cannot be replayed or debugged systematically
- **Priority**: LOW

### GAP-09: Multi-Agent Patterns [LOW]

- **Source**: `ai-agents/multi-agent.md` - Orchestrator-worker, planner-executor, writer-reviewer patterns, typed JSON handoffs, bounded loops
- **IPPS Status**: IPPS is single-agent focused. /go orchestrates phases sequentially within one agent
- **Files checked**: `.devin/workflows/` (grep for `multi-agent|parallel|orchestrator` - 0 results), `specs/` (no multi-agent patterns found)
- **Impact**: IPPS cannot leverage parallelism for independent tasks
- **Priority**: LOW

### GAP-10: Batch Processing [LOW]

- **Source**: `ai-agents/cost-control.md` - Batch APIs at ~50% cost for non-urgent work
- **IPPS Status**: No guidance on batch processing for bulk IPPS operations. Related: `_SPEC_LLM_EVALUATION_SKILL.md` has `call-llm-batch.py` for batch LLM calls, but this targets LLM evaluation, not IPPS workflow batch processing
- **Files checked**: `.devin/workflows/` (grep for `batch|bulk process` - 0 results), `specs/_SPEC_LLM_EVALUATION_SKILL.md` (has batch LLM calling but not IPPS workflow batching)
- **Impact**: Bulk IPPS operations pay full realtime cost
- **Priority**: LOW

### GAP-11: RAG / Retrieval Quality Framework [MEDIUM]

- **Source**: `ai-agents/rag.md` - Chunk on headings (200-800 tokens), hybrid retrieval (vector + BM25 + metadata filters), cross-encoder reranking, golden set evaluation (recall@k), inline citations, stale chunk filtering, embedding/retrieval caching
- **IPPS Status**: /prime workflow loads context files directly but has no retrieval, chunking, reranking, or citation discipline. No evaluation of context retrieval quality
- **Files checked**: `.devin/workflows/prime.md` (read 52 lines, confirms file loading via find_by_name + read_file with no retrieval framework), `.devin/workflows/` (grep for `retrieval|RAG|chunk|embedding` - 0 results)
- **Impact**: IPPS agents load files manually with no quality framework for what context is retrieved or how to verify retrieval completeness
- **Priority**: MEDIUM

### GAP-12: Spec Evolution Protocol [MEDIUM]

- **Source**: `knowledge-vaults/vault-evolution.md` - Add/deprecate/migrate/never-rebuild pattern with four moves: add type, make field required, layer framework, deprecate type
- **IPPS Status**: IPPS has no formal evolution protocol. _OldVersions/ contains V1 through V4 rebuilds, each severing continuity with prior versions. No add/deprecate/migrate discipline
- **Files checked**: `.devin/workflows/` (grep for `evolution|deprecat|migrat|rebuild` - 0 results), `.devin/rules/` (grep for `evolution|deprecat|migrat|rebuild|version trans` - 0 results), `specs/` (no evolution protocol spec found)
- **Impact**: IPPS version transitions lose backward links, reset history, and require full re-learning of the system
- **Priority**: MEDIUM

### GAP-13: Context Engineering / Token Budget Awareness [MEDIUM]

- **Source**: `prompt-engineering/context-engineering.md` - Token budget awareness, lost-in-the-middle mitigation, context compaction for long sessions
- **IPPS Status**: /prime workflow reads all .md files in workspace but has no token budget awareness, no lost-in-the-middle mitigation, no context compaction strategy. Files are loaded by pattern matching without considering context window limits
- **Files checked**: `.devin/workflows/prime.md` (read 52 lines, confirms file loading via find_by_name without budget awareness), `specs/` (grep for `cost|token budget|token limit` - 0 results)
- **Impact**: Long sessions in complex workspaces may exceed context windows or miss critical information buried in the middle of loaded context
- **Priority**: MEDIUM

## 5. Concept Deviations

### DEV-01: Controlled Vocabulary vs. Natural Language Prompts

- **Best Practice**: `prompt-engineering/best-practices.md`, `prompt-engineering/prompt-design.md` - Use straightforward natural language, iterate on prompts, role definition in prose
- **IPPS**: AGEN defines a controlled vocabulary with bracketed verbs (`[RESEARCH]`, `[IMPLEMENT]`), labels (`[CRITICAL]`, `[UNVERIFIED]`), and states (`COMPLEXITY-HIGH`)
- **Assessment**: IPPS is more prescriptive. Best practices advocate for clear natural language; IPPS adds a formal syntax layer. This is an intentional deviation - AGEN makes instructions grep-able and deterministic
- **Verdict**: Intentional improvement. IPPS adds value beyond best practices

### DEV-02: Document Lifecycle vs. Atomic Notes

- **Best Practice**: `knowledge-vaults/atomic-notes.md` - One idea per note, under 500 words, assertion titles, three-state maturity (seedling/budding/evergreen)
- **IPPS**: TRACTFUL defines document types (INFO, SPEC, IMPL, TEST, TASKS) with lifecycle tracking. Documents are lifecycle artifacts, not atomic knowledge notes
- **Assessment**: Different goals. Best practices target knowledge accumulation; IPPS targets development lifecycle traceability
- **Verdict**: Different domains. Both valid for their context

### DEV-03: GRUC vs. Audit Rule Catalog

- **Best Practice**: `knowledge-vaults/audit-rule-catalog.md` - C-rules and S-rules, severity levels, `vault-spec.yaml` for machine-checkable structure, `--fix` mode
- **IPPS**: GRUC separates compliance into 5 file types: GUIDE, RULES, CHECKS, EXAMPLE, TEMPLATE (per `_SPEC_GRUC_STANDARD.md [GRUC-SP01]` line 17). No machine-checkable spec file (no YAML, all markdown-based)
- **Assessment**: Similar concept, different implementation. Best practices use YAML spec for automated checking; IPPS uses markdown for agent-readable checking
- **Verdict**: IPPS could benefit from machine-checkable spec (see IMP-06)

### DEV-04: SOCAS vs. Anti-Slop

- **Best Practice**: `writing/anti-slop.md` - Catalogs specific words/phrases to avoid, paragraph-level slop patterns, concrete rewrites
- **IPPS**: SOCAS defines 17 criteria (SOCAS-01 through SOCAS-17) for confusion and sloppiness signals (per `.devin/skills/write-documents/SOCAS_RULES.md`). APAPALAN enforces precision and conciseness (per `.devin/skills/write-documents/APAPALAN_RULES.md`)
- **Assessment**: Overlapping scope, different approach. Best practices are specific (ban list); IPPS is principled (precision rules)
- **Verdict**: IPPS could benefit from a concrete slop catalog (see IMP-05)

### DEV-05: Phase Gates vs. Prompt Chaining

- **Best Practice**: `prompt-engineering/prompt-chaining.md` - One prompt per verb, trim aggressively between steps, thin router, state in orchestration code
- **IPPS**: EDIRD defines 5 phases with gates. Each phase has verbs, and gate checklists must pass before transition
- **Assessment**: Similar concept. Best practices focus on prompt-level decomposition; IPPS focuses on workflow-level decomposition
- **Verdict**: IPPS is more structured. Both valid

### DEV-06: Session Folders vs. Vault Architecture

- **Best Practice**: `knowledge-vaults/vault-architecture.md` - Numbered top-level folders, `vault-spec.yaml`, frontmatter schema per note type
- **IPPS**: Session folders, tracking files (NOTES.md, PROBLEMS.md, PROGRESS.md), topic/step subfolders, ID-REGISTRY.md
- **Assessment**: Different organizational models. Best practices target knowledge vaults; IPPS targets work sessions
- **Verdict**: Different domains. Both valid for their context

### DEV-07: MNF vs. Pre-Mortem

- **Best Practice**: `knowledge-vaults/decision-journals.md` - Pre-mortem (assume failure, write 3 likely causes), decision journal with frozen fields, resolution review
- **IPPS**: MNF (MUST-NOT-FORGET) - 5-15 critical items collected from FAILS.md, rules, specs. Reviewed before marking task done
- **Assessment**: Different purposes. Best practices target decision quality; IPPS targets task execution completeness
- **Verdict**: Complementary. IPPS could add pre-mortem to DESIGN phase (see IMP-09)

### DEV-08: /verify vs. Deterministic Auditor

- **Best Practice**: `knowledge-vaults/vault-audit.md` - Script-based auditor reads `vault-spec.yaml`, reports violations deterministically, JSON output for CI, exit codes
- **IPPS**: /verify workflow - agent reads GRUC CHECKS and verifies compliance. No script-based auditor
- **Assessment**: Best practices automate structural checking; IPPS delegates to agent judgment
- **Verdict**: IPPS could benefit from deterministic checks for structural rules (see IMP-06)

### DEV-09: APAPALAN vs. Voice Rules

- **Best Practice**: `writing/voice.md` - "Neutral playbook" voice: rule-first, specific nouns, rationale after rule, mixed sentence lengths, pick a side, imperative verbs
- **IPPS**: APAPALAN + MECT - precision over brevity, one name per concept, active voice, plain language
- **Assessment**: Highly overlapping. APAPALAN adds precision-priority. Best practices add "mixed sentence lengths" and "pick a side"
- **Verdict**: Strong alignment. Minor improvement possible (see IMP-05)

### DEV-10: System Prompt Token Budget

- **Best Practice**: `ai-agents/system-prompts.md` - Hard cap 200-800 tokens for system prompts. If prompt grows, factor out examples, schemas, runbooks
- **IPPS**: IPPS rules (agent-behavior.md, core-conventions.md, promptsystem-core.md, promptsystem-ids.md, tools-and-skills.md, workspace-rules.md) total well over 800 tokens, loaded as system context
- **Assessment**: IPPS rules exceed the recommended token budget significantly. However, IPPS rules serve a different purpose (multi-session stable context) vs. a single-agent system prompt
- **Verdict**: Different contexts. IPPS rules are more like a platform configuration than a per-agent prompt. Cache-awareness (GAP-04) is more relevant than token reduction here

### DEV-11: MCP Tool Logging

- **Best Practice**: `ai-agents/mcp-servers.md` - Every tool call gets a log line: tool, args, result_summary, duration_ms, error. Logs feed debugging, eval datasets, audit trails
- **IPPS**: IPPS uses MCP servers (playwright, playwriter) but has no per-call logging requirement or log format
- **Assessment**: Best practices require structured logging for all tool calls; IPPS has no tool call observability
- **Verdict**: IPPS could benefit from tool call logging (see IMP-10)

### DEV-12: /prime Context Loading vs. Context Engineering

- **Best Practice**: `prompt-engineering/context-engineering.md` - Token budget awareness, lost-in-the-middle mitigation, context compaction, cache-aware ordering
- **IPPS**: `/prime` workflow (`.devin/workflows/prime.md`) reads all .md files via find_by_name without token budget, context compaction, or lost-in-the-middle mitigation
- **Assessment**: Both load context for agents, but /prime has no awareness of context window limits or information ordering. Best practices engineer context deliberately; IPPS loads everything matching a pattern
- **Verdict**: IPPS could benefit from context engineering principles (see IMP-07)

## 6. Improvement Opportunities

### IMP-01: Add Prompt Injection Defense to IPPS Rules [HIGH]

- **Source**: `ai-agents/prompt-injection-defense.md`
- **Suggestion**: Add a rule or spec defining structural separation of untrusted input (XML-style delimiters), tool scoping guidelines, sentinel classifier pattern, audit logging for agent tool calls
- **Affected IPPS**: New spec or addition to `agent-behavior.md`
- **Priority**: HIGH

### IMP-02: Add Eval Set Framework to IPPS [HIGH]

- **Source**: `prompt-engineering/prompt-evals.md`, `ai-agents/evaluation.md`
- **Suggestion**: Define golden sets (30-100 test cases per workflow/skill), LLM-as-judge scoring with pinned judge model, regression testing on changes, CI-gated promotion
- **Affected IPPS**: New skill or workflow (`/eval`), addition to GRUC CHECKS
- **Priority**: HIGH

### IMP-03: Add Cost Tracking to IPPS [MEDIUM]

- **Source**: `ai-agents/cost-control.md`
- **Suggestion**: Add per-phase token budget, cost-per-task tracking in PROGRESS.md, model routing guidance, cache hit rate awareness
- **Affected IPPS**: STRUT spec, /go workflow, PROGRESS template
- **Priority**: MEDIUM

### IMP-04: Add Few-Shot Example Patterns to IPPS Templates [MEDIUM]

- **Source**: `ai-agents/few-shot.md`, `ai-agents/examples-vs-rules.md`
- **Suggestion**: Add 3-5 worked examples per workflow template, positive + negative example pairs, example ordering (canonical case last), delimiter consistency
- **Affected IPPS**: write-documents skill, workflow templates, GRUC EXAMPLE files
- **Priority**: MEDIUM

### IMP-05: Add Concrete Slop Catalog to SOCAS [MEDIUM]

- **Source**: `writing/anti-slop.md`, `writing/voice.md`
- **Suggestion**: Enhance SOCAS with specific word/phrase ban list, before-and-after rewrite examples, "mixed sentence lengths" rule, "pick a side" rule
- **Affected IPPS**: SOCAS definition (in rules or specs)
- **Priority**: MEDIUM

### IMP-06: Add Machine-Checkable Spec for Document Validation [MEDIUM]

- **Source**: `knowledge-vaults/vault-audit.md`, `knowledge-vaults/audit-rule-catalog.md`
- **Suggestion**: Create `ipps-spec.yaml` defining document types, required fields, folder placement rules, ID format validation, cross-reference resolution. Run as script before /verify
- **Affected IPPS**: New tool, GRUC CHECKS, /verify workflow
- **Priority**: MEDIUM

### IMP-07: Add Context Engineering to /prime [MEDIUM]

- **Source**: `prompt-engineering/context-engineering.md`
- **Suggestion**: Enhance /prime with token budget awareness, lost-in-the-middle mitigation, context compaction for long sessions, cache-aware ordering
- **Affected IPPS**: /prime workflow, agent-behavior rules
- **Priority**: MEDIUM

### IMP-08: Add Output Schema Validation to TRACTFUL [MEDIUM]

- **Source**: `ai-agents/structured-output.md`, `prompt-engineering/output-constraints.md`
- **Suggestion**: Add machine-readable document schema (YAML or JSON) per document type, validation script, rejection loop
- **Affected IPPS**: TRACTFUL spec, write-documents skill
- **Priority**: MEDIUM

### IMP-09: Add Pre-Mortem to DESIGN Phase [LOW]

- **Source**: `knowledge-vaults/decision-journals.md`
- **Suggestion**: Before implementation, assume failure and write 3 most likely causes. Add checkable causes to key assumptions. Review at DELIVER phase
- **Affected IPPS**: EDIRD spec, DESIGN phase gates
- **Priority**: LOW

### IMP-10: Add Observability Logging Pattern [LOW]

- **Source**: `ai-agents/multi-agent.md`, `ai-agents/cost-control.md`, `ai-agents/mcp-servers.md`
- **Suggestion**: Add per-call log (agent_id, turn, input, output, tool_calls, cost) stored in session folder for replay. Include MCP tool call logging
- **Affected IPPS**: session-management skill, /go workflow
- **Priority**: LOW

### IMP-11: Add RAG Framework to /prime [MEDIUM]

- **Source**: `ai-agents/rag.md`
- **Suggestion**: Add context retrieval quality framework: chunking guidelines (split on headings, 200-800 tokens), metadata attachment (source, date, heading_path), inline citation requirement, stale content filtering, retrieval quality evaluation
- **Affected IPPS**: /prime workflow, agent-behavior rules
- **Priority**: MEDIUM

### IMP-12: Add Spec Evolution Protocol [MEDIUM]

- **Source**: `knowledge-vaults/vault-evolution.md`
- **Suggestion**: Add formal evolution protocol: add new type (declare in spec, add template, create folder, run audit), make field required (migration with worklist), layer framework (additive, not fork), deprecate (archive first, then remove type). Never rebuild
- **Affected IPPS**: New spec or addition to promptsystem-core.md
- **Priority**: MEDIUM

### IMP-13: Add Orphan Detection to /verify [LOW]

- **Source**: `knowledge-vaults/linking-and-tags.md`
- **Suggestion**: Add orphan detection to /verify workflow: scan for documents with no inbound or outbound cross-references. Orphans must be linked or deleted. Cluster detection for groups of unreferenced documents on same topic
- **Affected IPPS**: /verify workflow, GRUC CHECKS
- **Priority**: LOW

## 7. Overlap Analysis

- **Writing standards** - `writing/technical-writing-standards.md`, `writing/editorial-style.md` vs APAPALAN, MECT, core-conventions.md - Overlap: High
  - Both advocate rule-first, consistent terminology, active voice, structured headings
- **File naming** - `file-organization/naming-conventions.md` vs core-conventions.md (YYYY-MM-DD, kebab-case) - Overlap: High
  - Nearly identical rules for file naming conventions
- **Folder structure** - `file-organization/folder-hierarchy.md` vs workspace-management, session-management - Overlap: High
  - Both advocate shallow, feature-grouped hierarchy with max depth
- **Skill structure** - `ai-agents/claude-code-skills.md` vs IPPS skills (.devin/skills/SKILL.md) - Overlap: High
  - Same pattern: named, invocable procedures with SKILL.md as prompt
- **Pitfall avoidance** - `ai-agents/claude-code-pitfalls.md` vs FAILS.md, agent-behavior rules - Overlap: High
  - Both address scope creep, unrequested refactors, skipped verification
- **Phase-verify pattern** - `ai-agents/claude-code.md` (phase-and-verify) vs EDIRD gates, /verify - Overlap: High
  - Both require verification before phase transition
- **Brief pattern** - `ai-agents/claude-code.md` (brief + acceptance criteria) vs EDIRD SPEC + AC items, STRUT deliverables - Overlap: High
  - Both require verifiable acceptance criteria
- **Stable context files** - `ai-agents/claude-code-claude-md.md` (CLAUDE.md) vs IPPS rules (agent-behavior.md, core-conventions.md) - Overlap: High
  - Both separate stable rules from per-task instructions
- **Source verification** - `knowledge-vaults/source-verification.md` vs SOCAS, [VERIFIED]/[UNVERIFIED] labels - Overlap: Medium
  - Both require source tracking, different implementation
- **Decision tracking** - `knowledge-vaults/decision-journals.md` vs NOTES.md Key Decisions, Document History - Overlap: Medium
  - Both track decisions, IPPS is less formal
- **System prompt structure** - `ai-agents/system-prompts.md` vs IPPS rules (agent-behavior.md) - Overlap: High
  - 4-block skeleton (Identity, Capabilities, Constraints, Format) maps to IPPS rules structure
- **Anti-sycophancy** - `ai-agents/role-framing.md` vs agent-behavior.md anti-sycophancy rules - Overlap: High
  - Both contain explicit anti-sycophancy and calibration rules
- **Team coordination** - `knowledge-vaults/team-vaults.md` vs git + ID-REGISTRY.md - Overlap: High
  - Git merge model, naming ledger, append-only convention all present in IPPS

## 8. Coverage Matrix

- **AI Agents** - 17 articles read, 7 strong, 4 partial, 6 gap - Coverage: 65%
- **Prompt Engineering** - 12 articles read, 3 strong, 5 partial, 4 gap - Coverage: 58%
- **Writing** - 5 articles read, 5 strong, 0 partial, 0 gap - Coverage: 100%
- **Knowledge Vaults** - 14 articles read, 3 strong, 10 partial, 1 gap - Coverage: 79%
- **Coding** - 2 articles read, 1 strong, 1 partial, 0 gap - Coverage: 75%
- **File Organization** - 2 articles read, 2 strong, 0 partial, 0 gap - Coverage: 100%
- **Backend** - 0 articles read - Not analyzed
- **Cheatsheets** - 0 articles read - Not analyzed
- **Comparisons** - 0 articles read - Not analyzed
- **Frontend** - 0 articles read - Not analyzed
- **Glossary** - 0 articles read - Not analyzed
- **Howto** - 0 articles read - Not analyzed
- **Ops** - 0 articles read - Not analyzed
- **Security** - 0 articles read - Not analyzed (injection defense covered via ai-agents/ path)
- **SEO** - 0 articles read - Not analyzed
- **Tooling** - 0 articles read - Not analyzed
- **Meta** - 0 articles read - Not analyzed

**Totals**: 52 articles read, 21 strong, 20 partial, 11 gap - Coverage: 78% (of read categories)

## 9. Recommendations

### Immediate (High Priority)

1. **Add prompt injection defense** (IMP-01) - Security-critical for agents reading external content
2. **Add eval set framework** (IMP-02) - Needed for regression-testing workflow/skill changes
3. **Add few-shot examples to templates** (IMP-04) - Examples teach what rules cannot

### Medium Priority

4. **Add cost tracking to /go** (IMP-03) - Guardrails for autonomous operations
5. **Add concrete slop catalog to SOCAS** (IMP-05) - Concrete rewrites complement abstract principles
6. **Add machine-checkable spec** (IMP-06) - Deterministic validation before agent verification
7. **Add context engineering to /prime** (IMP-07) - Token budget awareness
8. **Add output schema validation to TRACTFUL** (IMP-08) - Automated document conformance
9. **Add RAG framework to /prime** (IMP-11) - Retrieval quality and citation discipline
10. **Add spec evolution protocol** (IMP-12) - Add/deprecate/migrate/never-rebuild pattern

### Low Priority

11. **Add pre-mortem to DESIGN** (IMP-09) - Decision quality improvement
12. **Add observability logging** (IMP-10) - Debugging, replay, and tool call tracking
13. **Add orphan detection to /verify** (IMP-13) - Detect unreferenced documents

### What IPPS Does Better

- **AGEN controlled vocabulary** - Grep-able, traceable, deterministic instructions (best practices have no equivalent)
- **EDIRD phase model** - Unified BUILD/SOLVE with gates, complexity levels, and deterministic next-action logic
- **STRUT tree notation** - Expressive planning with concurrent blocks, deliverables, transitions
- **MNF technique** - Operational checklist for task execution (best practices have pre-mortem but not execution checklists)
- **Session management** - Full lifecycle (init, work, save, resume, finalize, archive) with tracking files
- **GRUC 5-file separation** - GUIDE + RULES + CHECKS + EXAMPLE + TEMPLATE per skill (best practices have 2-file: rules + audit catalog)
- **TRACTFUL traceability** - Full lifecycle document IDs, cross-references, sync workflows

## 10. Sources

### AI Agents

- `ai-agents/agent-architecture-patterns.md` - Workflow patterns, structured output, bounded loops
- `ai-agents/agentic-workflow-patterns.md` - Five workflow patterns, guardrails
- `ai-agents/claude-code.md` - Brief pattern, phase-and-verify, acceptance criteria
- `ai-agents/claude-code-claude-md.md` - CLAUDE.md as memory replacement, stable rules
- `ai-agents/claude-code-skills.md` - Skills as named invocable procedures
- `ai-agents/claude-code-pitfalls.md` - Common failure modes and fixes
- `ai-agents/cost-control.md` - Token budgets, model routing, cache hits, batch APIs
- `ai-agents/evaluation.md` - Golden sets, LLM-as-judge, per-slice scoring, regression dashboards
- `ai-agents/few-shot.md` - 3-5 examples, positive+negative pairs, recency bias
- `ai-agents/examples-vs-rules.md` - Rules for hard constraints, examples for subtle conventions
- `ai-agents/multi-agent.md` - Orchestrator-worker, planner-executor, bounded loops, typed handoffs
- `ai-agents/prompt-injection-defense.md` - Structural separation, sentinel classifier, tool scoping
- `ai-agents/structured-output.md` - JSON schema enforcement, typed contracts, downstream code integration
- `ai-agents/system-prompts.md` - 4-block skeleton, token cap, version control, assume leak
- `ai-agents/role-framing.md` - Role/domain/audience, calibration rule, anti-sycophancy, role refresh
- `ai-agents/rag.md` - Chunking, hybrid retrieval, reranking, golden sets, inline citations, caching
- `ai-agents/mcp-servers.md` - Tool grouping, tool naming, resources vs tools, security, per-call logging

### Prompt Engineering

- `prompt-engineering/best-practices.md` - 7 strategies, 5 patterns to memorize
- `prompt-engineering/chain-of-thought.md` - When to use CoT, structured reasoning sections
- `prompt-engineering/context-engineering.md` - Token budget, lost-in-the-middle, compaction
- `prompt-engineering/output-constraints.md` - Examples, escape hatches, schema, validation loop
- `prompt-engineering/prompt-chaining.md` - One prompt per verb, trim between steps, thin router
- `prompt-engineering/prompt-design.md` - System vs user, role definition, non-goals
- `prompt-engineering/prompt-evals.md` - 50-200 cases, CI-gated, score tracking, statistical significance
- `prompt-engineering/prompt-templates.md` - Delimiter conventions, versioned files, skeleton
- `prompt-engineering/system-prompt-design-patterns.md` - Named blocks, constraints, output contract
- `prompt-engineering/prompt-injection-defense.md` - Same as ai-agents/prompt-injection-defense.md
- `prompt-engineering/reasoning-model-prompting.md` - Strip scaffolding, instruction precision, effort parameter, token budget
- `prompt-engineering/prompt-caching-strategies.md` - Stable-first layout, cache controls, hit rate tracking, model version pinning

### Writing

- `writing/anti-slop.md` - Word/phrase ban list, paragraph-level slop, concrete rewrites
- `writing/documentation-for-ai-products.md` - Dual audience, machine-readable structure, dated facts
- `writing/editorial-style.md` - Punctuation, capitalization, code references, file naming
- `writing/technical-writing-standards.md` - Task-first, atomic pages, consistent terminology
- `writing/voice.md` - Neutral playbook voice, rule-first, specific nouns, pick a side

### Knowledge Vaults

- `knowledge-vaults/atomic-notes.md` - One idea per note, conjunction test, 3-state maturity
- `knowledge-vaults/audit-rule-catalog.md` - C-rules, S-rules, severity, --fix mode
- `knowledge-vaults/decision-journals.md` - Frozen fields, pre-mortem, resolution review
- `knowledge-vaults/rigor-frameworks.md` - Required argument shapes, frontmatter encoding
- `knowledge-vaults/semantic-audit.md` - LLM judge with fixed rubric, 6 defect dimensions
- `knowledge-vaults/source-verification.md` - Sources array, confidence levels, staleness
- `knowledge-vaults/vault-architecture.md` - Numbered folders, vault-spec.yaml, frontmatter
- `knowledge-vaults/vault-audit.md` - Deterministic auditor, JSON output, CI exit codes
- `knowledge-vaults/vault-maintenance.md` - Weekly/monthly/quarterly cadences, query gates
- `knowledge-vaults/vault-orchestration.md` - 5-stage pipeline, propose-then-apply, scope freeze
- `knowledge-vaults/vault-frontmatter-schema.md` - Per-type required fields, absent vs empty, rigor framework fields
- `knowledge-vaults/linking-and-tags.md` - Wikilinks for relationships, tags for state, naked link dumps, orphan detection
- `knowledge-vaults/team-vaults.md` - Git merge model, atomicity as concurrency, naming ledger, rename as scope-freeze
- `knowledge-vaults/vault-evolution.md` - Add/deprecate/migrate/never-rebuild, four moves, layer vs fork

### Coding

- `coding/general-principles.md` - Naming, comments, error handling, dependencies, testing
- `coding/testing.md` - Trophy shape, flaky tests, test naming, snapshot tests

### File Organization

- `file-organization/folder-hierarchy.md` - Max 4 levels, feature-grouped, index files
- `file-organization/naming-conventions.md` - Kebab-case, role-based names, ISO dates

## Document History

**[2026-09-12 17:45]**
- Initial mapping created
- 52 articles mapped across 17 categories (6 read, 11 not analyzed)
- 13 gaps, 12 deviations, 13 improvement opportunities identified
- Coverage: 78% of read categories (21 strong, 20 partial, 11 gap)
- P3-S3/S4: All gaps verified against actual IPPS files, GAP-07 reclassified from gap to partial (/switch-model exists), GAP-13 added (context engineering), DEV-03 fixed (5 GRUC types not 4), DEV-04 fixed (17 SOCAS criteria not 15), DEV-12 added (/prime vs. context engineering)
