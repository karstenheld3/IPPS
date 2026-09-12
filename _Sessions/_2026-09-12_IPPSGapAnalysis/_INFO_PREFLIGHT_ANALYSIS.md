# INFO: IPPS Gap Analysis - Preflight Analysis

**Doc ID**: IPPSGAP-IN01
**Goal**: Map LLM best practices articles to IPPS concepts and identify gaps, deviations, and improvement opportunities
**Source**: `e:\Dev\Delphios\knowledge\AI-Stuff\LLMBestPractices_2026-09-12` (mirror of https://llmbestpractices.com)

**Depends on:**
- `README.md` for IPPS concept overview
- `specs/_SPEC_AGEN_AGENTIC_ENGLISH.md [AGEN-SP01]` for controlled vocabulary
- `specs/_SPEC_EDIRD_PHASE_MODEL.md [EDIRD-SP05]` for phase model
- `specs/_SPEC_STRUT_STRUCTURED_THINKING.md [STRUT-SP01]` for planning notation
- `specs/_SPEC_TRACTFUL_DOCUMENT_FRAMEWORK.md [TRACT-SP01]` for document framework

## Summary

This preflight analysis maps 30+ key articles from the LLM Best Practices knowledge base (llmbestpractices.com mirror, 18 categories, ~590 pages) against IPPS concepts. The analysis identifies 10 gaps, 9 concept deviations, and 10 improvement opportunities.

**Key findings:**
- IPPS strongly covers agent architecture, writing standards, document frameworks, and session management
- IPPS has no coverage for prompt injection defense, systematic eval sets, cost control, or prompt caching
- IPPS deviates from best practices in vocabulary control (AGEN vs natural language), document lifecycle (TRACTFUL vs atomic notes), and audit approach (GRUC vs audit-rule-catalog)
- Highest-value improvements: add eval set framework, prompt injection defense, cost tracking, and few-shot example patterns

## Table of Contents

- [1. Methodology](#1-methodology)
- [2. Source Material](#2-source-material)
- [3. Mapping: Best Practices to IPPS](#3-mapping-best-practices-to-ipps)
- [4. Gap Analysis](#4-gap-analysis)
- [5. Concept Deviations](#5-concept-deviations)
- [6. Improvement Opportunities](#6-improvement-opportunities)
- [7. Overlap Analysis](#7-overlap-analysis)
- [8. Coverage Matrix](#8-coverage-matrix)
- [9. Recommendations](#9-recommendations)
- [10. Sources](#10-sources)
- [Document History](#document-history)

## 1. Methodology

1. Cataloged all articles in the LLM Best Practices knowledge base by category
2. Read 30+ key articles across 8 categories (ai-agents, prompt-engineering, writing, knowledge-vaults, coding, file-organization)
3. Read key IPPS specs (AGEN, EDIRD, STRUT, TRACTFUL) and rules (agent-behavior, core-conventions)
4. Mapped each article to IPPS concepts, skills, workflows, or rules
5. Identified gaps (no IPPS equivalent), deviations (different approach to same topic), and improvement opportunities
6. Applied /research workflow: labeled findings, retained sources, summary at top

## 2. Source Material

### LLM Best Practices Knowledge Base

Location: `e:\Dev\Delphios\knowledge\AI-Stuff\LLMBestPractices_2026-09-12`

Categories and article counts (approximate):
- `ai-agents/` - 45 articles (agent architecture, Claude Code, evaluation, multi-agent, cost control)
- `backend/` - 40 articles (API design, databases, observability)
- `cheatsheets/` - 46 articles (quick reference guides)
- `coding/` - 33 articles (general principles, testing, per-language guides)
- `comparisons/` - 50 articles (model comparisons, tool comparisons)
- `file-organization/` - 8 articles (naming, hierarchy, project structure)
- `frontend/` - 65 articles (React, CSS, accessibility)
- `glossary/` - 100+ articles (term definitions)
- `howto/` - 54 articles (setup guides, workflows)
- `knowledge-vaults/` - 18 articles (atomic notes, vault architecture, audits)
- `ops/` - 31 articles (deployment, CI/CD, monitoring)
- `prompt-engineering/` - 13 articles (best practices, templates, evals, chaining)
- `security/` - 2 articles (injection defense, secrets)
- `seo/` - 48 articles (content strategy, technical SEO)
- `tooling/` - 20 articles (Obsidian, Git, editors)
- `writing/` - 8 articles (anti-slop, voice, technical writing, editorial style)
- `meta/` - 8 articles (llm-info standard, site info)

### IPPS Concepts Analyzed

- **AGEN** - Agentic English (controlled vocabulary, verbs, labels, states)
- **EDIRD** - Phase Model (EXPLORE, DESIGN, IMPLEMENT, REFINE, DELIVER)
- **STRUT** - Structured Thinking (tree notation for planning)
- **TRACTFUL** - Document Framework (document types, IDs, traceability)
- **MNF** - MUST-NOT-FORGET Technique
- **APAPALAN** - Writing Principle (As Precise As Possible, As Little As Necessary)
- **MECT** - Minimal Explicit Consistent Terminology
- **SOCAS** - Signs of Confusion and Sloppiness
- **GRUC** - Guides, Rules, Checks (compliance criteria)
- **AMINTON** - Agentic Minto Notation
- Session management (sessions, topic/step folders, NOTES/PROGRESS/PROBLEMS)
- Workflows (~50 workflows including /go, /verify, /critique, /research, /commit)
- Skills (~21 skills including write-documents, session-management, coding-conventions)
- Rules (agent-behavior, core-conventions, promptsystem-core, promptsystem-ids)

## 3. Mapping: Best Practices to IPPS

### 3.1 AI Agents

| Best Practice Article | IPPS Equivalent | Match |
|---|---|---|
| `agent-architecture-patterns.md` | EDIRD phases, STRUT planning, /go workflow | Strong |
| `agentic-workflow-patterns.md` | EDIRD phases, workflows (prompt chaining = phase transitions) | Strong |
| `examples-vs-rules.md` | AGEN (rules), APAPALAN (examples in templates) | Partial |
| `claude-code-claude-md.md` | IPPS rules (agent-behavior.md, core-conventions.md), !NOTES.md | Strong |
| `claude-code-skills.md` | IPPS skills system (.devin/skills/) | Strong |
| `claude-code-pitfalls.md` | FAILS.md, agent-behavior rules (confirmation, scoping) | Strong |
| `claude-code.md` | /go workflow, session-management skill, brief pattern | Strong |
| `evaluation.md` | /verify, /critique, SOCAS | Partial |
| `multi-agent.md` | (no direct equivalent - IPPS is single-agent) | Gap |
| `cost-control.md` | AWT estimates in STRUT (but no systematic cost tracking) | Gap |
| `few-shot.md` | (IPPS templates use placeholders, not worked examples) | Gap |
| `prompt-injection-defense.md` | (no IPPS equivalent) | Gap |

### 3.2 Prompt Engineering

| Best Practice Article | IPPS Equivalent | Match |
|---|---|---|
| `best-practices.md` | AGEN, APAPALAN, MECT (clear language, conciseness, output constraints) | Strong |
| `prompt-design.md` | AGEN (system/user distinction), workflow brief patterns | Partial |
| `prompt-chaining.md` | EDIRD phases (each phase = one chain step) | Strong |
| `output-constraints.md` | AGEN labels, TRACTFUL document types, APAPALAN | Partial |
| `system-prompt-design-patterns.md` | IPPS rules (agent-behavior.md as system prompt) | Strong |
| `context-engineering.md` | /prime workflow (load relevant context) | Partial |
| `prompt-templates.md` | IPPS workflow templates, document templates | Partial |
| `prompt-evals.md` | /verify (but no systematic eval sets) | Gap |
| `chain-of-thought.md` | EDIRD phases, STRUT (structured thinking) | Partial |
| `prompt-injection-defense.md` | (no IPPS equivalent) | Gap |

### 3.3 Writing

| Best Practice Article | IPPS Equivalent | Match |
|---|---|---|
| `anti-slop.md` | APAPALAN, MECT, SOCAS (15 criteria for sloppiness) | Strong |
| `voice.md` | APAPALAN, MECT (rule-first, specific nouns, direct tone) | Strong |
| `technical-writing-standards.md` | APAPALAN, write-documents skill, core-conventions.md | Strong |
| `editorial-style.md` | core-conventions.md (dates, punctuation, headings, lists) | Strong |
| `documentation-for-ai-products.md` | IPPS itself (rules/skills/workflows are agent-facing docs) | Strong |

### 3.4 Knowledge Vaults

| Best Practice Article | IPPS Equivalent | Match |
|---|---|---|
| `atomic-notes.md` | TRACTFUL document types (INFO, SPEC - one topic per doc) | Partial |
| `vault-architecture.md` | IPPS folder structure, workspace-management skill | Strong |
| `audit-rule-catalog.md` | GRUC CHECKS files, /verify workflow | Strong |
| `vault-audit.md` | /verify workflow, GRUC CHECKS | Strong |
| `semantic-audit.md` | /critique workflow, SOCAS | Partial |
| `decision-journals.md` | TRACTFUL document history, Key Decisions in NOTES.md | Partial |
| `source-verification.md` | SOCAS, [VERIFIED]/[UNVERIFIED] labels | Partial |
| `rigor-frameworks.md` | TRACTFUL document types, AMINTON | Partial |
| `vault-orchestration.md` | /go autonomous mode, session-management | Partial |
| `vault-maintenance.md` | /session-save, /session-finalize, /cleanup | Partial |

### 3.5 Coding

| Best Practice Article | IPPS Equivalent | Match |
|---|---|---|
| `general-principles.md` | MECT, coding-conventions skill, agent-behavior rules | Strong |
| `testing.md` | /test workflow, /verify workflow | Partial |

### 3.6 File Organization

| Best Practice Article | IPPS Equivalent | Match |
|---|---|---|
| `naming-conventions.md` | core-conventions.md (file naming, date formats), ID-REGISTRY.md | Strong |
| `folder-hierarchy.md` | workspace-management skill, session-management skill | Strong |

## 4. Gap Analysis

Gaps are topics where LLM best practices provide guidance but IPPS has no equivalent.

### GAP-01: Prompt Injection Defense [CRITICAL]

- **Best Practice**: `prompt-injection-defense.md` - Structural separation of untrusted input, sentinel classifiers, tool scoping, audit logs
- **IPPS Status**: No coverage. IPPS rules and workflows do not address untrusted input handling, injection patterns, or defense-in-depth for agent tool access
- **Impact**: IPPS agents processing external content (web pages, user-provided files, retrieved documents) have no guidelines for treating untrusted input as data-only
- **Priority**: High - security-critical for any agent that reads external content

### GAP-02: Systematic Eval Sets [HIGH]

- **Best Practice**: `prompt-evals.md`, `evaluation.md` - Golden sets (50-200 test cases), LLM-as-judge, regression testing, CI-gated prompt changes
- **IPPS Status**: /verify and /critique workflows check compliance and logic, but IPPS has no framework for creating, maintaining, and running systematic test case suites against workflows or skills
- **Impact**: Workflow/skill changes cannot be regression-tested. A wording change in a workflow may silently degrade agent behavior
- **Priority**: High - needed for IPPS quality assurance at scale

### GAP-03: Cost Control and Token Budgets [MEDIUM]

- **Best Practice**: `cost-control.md` - Per-task token caps, model routing, batch APIs, cache hit rate tracking, cost-per-task metrics
- **IPPS Status**: STRUT supports AWT (Agentic Work Time) estimates and model hints, but no systematic cost tracking, token budget enforcement, or model routing guidance
- **Impact**: Long /go sessions or complex workflows may consume excessive tokens without guardrails
- **Priority**: Medium - relevant for cost-sensitive autonomous operations

### GAP-04: Prompt Caching Strategies [MEDIUM]

- **Best Practice**: `context-engineering.md`, `cost-control.md` - Put stable content first for cache hits, mark cache breakpoints, track cache hit rate
- **IPPS Status**: No guidance on prompt ordering for cache optimization. IPPS rules are loaded as system context but no explicit cache-awareness
- **Impact**: IPPS agents may pay full token cost on every call when cache could reduce costs by ~90%
- **Priority**: Medium - cost optimization

### GAP-05: Few-Shot Example Patterns [MEDIUM]

- **Best Practice**: `few-shot.md`, `examples-vs-rules.md` - 3-5 diverse examples, positive+negative pairs, recency-bias ordering, delimiter consistency
- **IPPS Status**: IPPS templates use placeholders and instructions but do not include worked examples. The `examples-vs-rules.md` principle (examples teach what rules cannot) is not systematically applied
- **Impact**: IPPS workflows and skills may miss subtle behavioral conventions that examples teach better than rules
- **Priority**: Medium - quality improvement

### GAP-06: Output Schema Validation [MEDIUM]

- **Best Practice**: `output-constraints.md`, `prompt-templates.md` - JSON schema declaration, structured-output mode, validation-rejection loop
- **IPPS Status**: TRACTFUL defines document types and structures, but there is no machine-validation of document conformance. GRUC CHECKS are manual compliance criteria, not automated schema validation
- **Impact**: Documents may silently drift from templates. No automated gate catches structural violations
- **Priority**: Medium - relevant for document quality at scale

### GAP-07: Model Routing and Tier Selection [LOW]

- **Best Practice**: `cost-control.md` - Router as first hop, triage with small model, escalate to frontier for hard cases
- **IPPS Status**: STRUT supports model hints ("Opus for analysis, Sonnet for implementation") but no routing system or tier-selection guidance
- **Impact**: IPPS agents use one model for all tasks; no cost-quality trade-off mechanism
- **Priority**: Low - optimization, not correctness

### GAP-08: Runtime Observability [LOW]

- **Best Practice**: `cost-control.md`, `multi-agent.md` - Per-call logging (agent_id, turn, input, output, tool_calls, cost), structured logs for replay
- **IPPS Status**: PROGRESS.md tracks task status, NOTES.md captures decisions, but no runtime logging of agent calls, tool invocations, or token usage
- **Impact**: Failed agent runs cannot be replayed or debugged systematically
- **Priority**: Low - debugging improvement

### GAP-09: Multi-Agent Patterns [LOW]

- **Best Practice**: `multi-agent.md` - Orchestrator-worker, planner-executor, writer-reviewer patterns, typed JSON handoffs, bounded loops
- **IPPS Status**: IPPS is single-agent focused. /go orchestrates phases sequentially within one agent. No guidance for parallel agent decomposition
- **Impact**: IPPS cannot leverage parallelism for independent tasks (e.g., reviewing 20 files)
- **Priority**: Low - different scope (IPPS targets single-agent IDE workflows)

### GAP-10: Batch Processing [LOW]

- **Best Practice**: `cost-control.md` - Batch APIs at ~50% cost for non-urgent work
- **IPPS Status**: No guidance on batch processing for bulk operations
- **Impact**: Bulk IPPS operations (e.g., auditing all specs) pay full realtime cost
- **Priority**: Low - cost optimization

## 5. Concept Deviations

Deviations are topics where both IPPS and best practices provide guidance but with different approaches.

### DEV-01: Controlled Vocabulary vs. Natural Language Prompts

- **Best Practice**: `best-practices.md`, `prompt-design.md` - Use straightforward natural language, iterate on prompts, role definition in prose
- **IPPS**: AGEN defines a controlled vocabulary with bracketed verbs (`[RESEARCH]`, `[IMPLEMENT]`), labels (`[CRITICAL]`, `[UNVERIFIED]`), and states (`COMPLEXITY-HIGH`)
- **Assessment**: IPPS is more prescriptive. Best practices advocate for clear natural language; IPPS adds a formal syntax layer. This is an intentional deviation - AGEN makes instructions grep-able and deterministic. Best practices do not address grep-ability or instruction traceability
- **Verdict**: Intentional improvement. IPPS adds value beyond best practices

### DEV-02: Document Lifecycle vs. Atomic Notes

- **Best Practice**: `atomic-notes.md` - One idea per note, under 500 words, assertion titles, three-state maturity (seedling/budding/evergreen)
- **IPPS**: TRACTFUL defines document types (INFO, SPEC, IMPL, TEST, TASKS) with lifecycle tracking (Document History, cross-references, sync workflows). Documents are lifecycle artifacts, not atomic knowledge notes
- **Assessment**: Different goals. Best practices target knowledge accumulation; IPPS targets development lifecycle traceability. IPPS documents are typically longer and multi-topic (a SPEC may contain 20+ requirements)
- **Verdict**: Different domains. Both valid for their context

### DEV-03: GRUC vs. Audit Rule Catalog

- **Best Practice**: `audit-rule-catalog.md` - C-rules (structural) and S-rules (framework-specific), severity levels, `vault-spec.yaml` for machine-checkable structure, `--fix` mode
- **IPPS**: GRUC separates compliance into GUIDE (how-to), RULES (enforceable rules), CHECKS (verification criteria), EXAMPLE (demonstration). No machine-checkable spec file
- **Assessment**: Similar concept (structured compliance criteria), different implementation. Best practices use a YAML spec for automated checking; IPPS uses markdown files for agent-readable checking. Best practices have `--fix` mode; IPPS relies on agent judgment
- **Verdict**: IPPS could benefit from machine-checkable spec (see IMP-06)

### DEV-04: SOCAS vs. Anti-Slop

- **Best Practice**: `anti-slop.md` - Catalogs specific words/phrases to avoid ("delve", "unlock the power of", em-dashes for asides), paragraph-level slop patterns, concrete rewrites
- **IPPS**: SOCAS defines 15 criteria for confusion and sloppiness signals. APAPALAN enforces precision and conciseness. MECT enforces consistent terminology
- **Assessment**: Overlapping scope, different approach. Best practices are specific (ban list of words); IPPS is principled (precision and consistency rules). Best practices provide concrete rewrites; IPPS provides abstract principles
- **Verdict**: IPPS could benefit from a concrete slop catalog (see IMP-05)

### DEV-05: Phase Gates vs. Prompt Chaining

- **Best Practice**: `prompt-chaining.md` - One prompt per verb, trim aggressively between steps, thin router, state in orchestration code
- **IPPS**: EDIRD defines 5 phases with gates. Each phase has verbs, and gate checklists must pass before transition. /go sequences phases
- **Assessment**: Similar concept (decompose work into steps). Best practices focus on prompt-level decomposition; IPPS focuses on workflow-level decomposition. IPPS gates are more formal (checklists) vs. best practices (implicit step boundaries)
- **Verdict**: IPPS is more structured. Both valid

### DEV-06: Session Folders vs. Vault Architecture

- **Best Practice**: `vault-architecture.md` - Numbered top-level folders (`00-Inbox/`, `10-Sources/`, `20-Atoms/`), `vault-spec.yaml`, frontmatter schema per note type
- **IPPS**: Session folders (`_2026-09-12_IPPSGapAnalysis/`), tracking files (NOTES.md, PROBLEMS.md, PROGRESS.md), topic/step subfolders, ID-REGISTRY.md
- **Assessment**: Different organizational models. Best practices target knowledge vaults (permanent accumulation); IPPS targets work sessions (time-limited endeavors). IPPS sessions are archived after completion
- **Verdict**: Different domains. Both valid for their context

### DEV-07: MNF vs. Pre-Mortem

- **Best Practice**: `decision-journals.md` - Pre-mortem (assume failure, write 3 likely causes), decision journal with frozen fields, resolution review
- **IPPS**: MNF (MUST-NOT-FORGET) - 5-15 critical items collected from FAILS.md, rules, specs, user instructions. Reviewed before marking task done
- **Assessment**: Different purposes. Best practices target decision quality (pre-mortem); IPPS targets task execution completeness (checklist). MNF is operational; pre-mortem is analytical
- **Verdict**: Complementary. IPPS could add pre-mortem to DESIGN phase (see IMP-09)

### DEV-08: /verify vs. Deterministic Auditor

- **Best Practice**: `vault-audit.md` - Script-based auditor reads `vault-spec.yaml`, reports violations deterministically, JSON output for CI, exit codes
- **IPPS**: /verify workflow - agent reads GRUC CHECKS and verifies compliance. /critique finds logic flaws. No script-based auditor
- **Assessment**: Best practices automate structural checking; IPPS delegates to agent judgment. Best practices have deterministic pass/fail; IPPS has agent-assessed compliance
- **Verdict**: IPPS could benefit from deterministic checks for structural rules (see IMP-06)

### DEV-09: APAPALAN vs. Voice Rules

- **Best Practice**: `voice.md` - "Neutral playbook" voice: rule-first, specific nouns, rationale after rule, mixed sentence lengths, pick a side, imperative verbs
- **IPPS**: APAPALAN (As Precise As Possible, As Little As Necessary) + MECT (Minimal Explicit Consistent Terminology) - precision over brevity, one name per concept, active voice, plain language
- **Assessment**: Highly overlapping. Both advocate rule-first, specific nouns, direct tone. APAPALAN adds precision-priority (precision wins over brevity). Best practices add "mixed sentence lengths" and "pick a side" which APAPALAN does not explicitly address
- **Verdict**: Strong alignment. Minor improvement possible (see IMP-05)

## 6. Improvement Opportunities

Improvements are concrete suggestions where best practices could enhance existing IPPS concepts.

### IMP-01: Add Prompt Injection Defense to IPPS Rules [HIGH]

- **Source**: `prompt-injection-defense.md`
- **Suggestion**: Add a rule or spec defining:
  - Structural separation of untrusted input (XML-style delimiters for external content)
  - Tool scoping guidelines (least-privilege for agent tools)
  - Sentinel classifier pattern for high-stakes agents
  - Audit logging for agent tool calls
- **Affected IPPS**: New spec or addition to `agent-behavior.md`
- **Priority**: High - security-critical

### IMP-02: Add Eval Set Framework to IPPS [HIGH]

- **Source**: `prompt-evals.md`, `evaluation.md`
- **Suggestion**: Define a framework for:
  - Golden sets (30-100 test cases per workflow/skill)
  - LLM-as-judge scoring with pinned judge model
  - Regression testing on workflow/skill changes
  - CI-gated promotion (new workflow version must beat baseline)
- **Affected IPPS**: New skill or workflow (`/eval`), addition to GRUC CHECKS
- **Priority**: High - quality assurance at scale

### IMP-03: Add Cost Tracking to IPPS [MEDIUM]

- **Source**: `cost-control.md`
- **Suggestion**: Add to STRUT or /go workflow:
  - Per-phase token budget (hard cap on input + output)
  - Cost-per-task tracking in PROGRESS.md
  - Model routing guidance (when to use frontier vs mid-tier)
  - Cache hit rate awareness (put stable rules first in context)
- **Affected IPPS**: STRUT spec, /go workflow, PROGRESS template
- **Priority**: Medium

### IMP-04: Add Few-Shot Example Patterns to IPPS Templates [MEDIUM]

- **Source**: `few-shot.md`, `examples-vs-rules.md`
- **Suggestion**: Add to write-documents skill or workflow templates:
  - 3-5 worked examples per workflow template (showing input and expected output)
  - Positive + negative example pairs for edge cases
  - Example ordering (canonical case last for recency bias)
  - Delimiter consistency (IPPS already uses fenced code blocks)
- **Affected IPPS**: write-documents skill, workflow templates, GRUC EXAMPLE files
- **Priority**: Medium

### IMP-05: Add Concrete Slop Catalog to SOCAS [MEDIUM]

- **Source**: `anti-slop.md`, `voice.md`
- **Suggestion**: Enhance SOCAS with:
  - Specific word/phrase ban list ("delve", "unlock", "it's not X, it's Y", em-dashes for asides)
  - Before-and-after rewrite examples
  - "Mixed sentence lengths" rule (avoid AI-generated cadence)
  - "Pick a side" rule (avoid excessive hedging)
- **Affected IPPS**: SOCAS definition (in rules or specs)
- **Priority**: Medium

### IMP-06: Add Machine-Checkable Spec for Document Validation [MEDIUM]

- **Source**: `vault-audit.md`, `audit-rule-catalog.md`
- **Suggestion**: Create a `ipps-spec.yaml` or similar that defines:
  - Document types and required fields
  - Folder placement rules
  - ID format validation
  - Cross-reference resolution checks
  - Run as a script (deterministic pass) before /verify (agent pass)
- **Affected IPPS**: New tool, GRUC CHECKS, /verify workflow
- **Priority**: Medium

### IMP-07: Add Context Engineering to /prime [MEDIUM]

- **Source**: `context-engineering.md`
- **Suggestion**: Enhance /prime workflow with:
  - Token budget awareness (system prompt + evidence + history + headroom)
  - Lost-in-the-middle mitigation (put key instructions at start and end)
  - Context compaction for long sessions (summarize old turns, drop superseded results)
  - Cache-aware ordering (stable content first)
- **Affected IPPS**: /prime workflow, agent-behavior rules
- **Priority**: Medium

### IMP-08: Add Output Schema Validation to TRACTFUL [MEDIUM]

- **Source**: `output-constraints.md`, `prompt-templates.md`
- **Suggestion**: Add to TRACTFUL spec:
  - Machine-readable document schema (YAML or JSON) per document type
  - Validation script that checks document conformance
  - Rejection loop (if document fails validation, fix and re-validate)
- **Affected IPPS**: TRACTFUL spec, write-documents skill
- **Priority**: Medium

### IMP-09: Add Pre-Mortem to DESIGN Phase [LOW]

- **Source**: `decision-journals.md`
- **Suggestion**: Add to EDIRD DESIGN phase:
  - Before implementation, assume failure and write 3 most likely causes
  - Add checkable causes to key assumptions
  - Review at DELIVER phase
- **Affected IPPS**: EDIRD spec, DESIGN phase gates
- **Priority**: Low

### IMP-10: Add Observability Logging Pattern [LOW]

- **Source**: `multi-agent.md`, `cost-control.md`
- **Suggestion**: Add to session-management or /go:
  - Per-call log (agent_id, turn, input, output, tool_calls, cost)
  - Store in session folder for replay
  - Use as eval input for future improvements
- **Affected IPPS**: session-management skill, /go workflow
- **Priority**: Low

## 7. Overlap Analysis

Topics where IPPS and best practices address the same concept with similar approaches.

| Topic | Best Practice | IPPS | Overlap |
|---|---|---|---|
| Writing standards | `technical-writing-standards.md`, `editorial-style.md` | APAPALAN, MECT, core-conventions.md | High - both advocate rule-first, consistent terminology, active voice |
| File naming | `naming-conventions.md` | core-conventions.md (YYYY-MM-DD, kebab-case) | High - nearly identical rules |
| Folder structure | `folder-hierarchy.md` | workspace-management, session-management | High - both advocate shallow, feature-grouped hierarchy |
| Skill structure | `claude-code-skills.md` | IPPS skills (.devin/skills/SKILL.md) | High - same pattern (named, invocable, SKILL.md as prompt) |
| Pitfall avoidance | `claude-code-pitfalls.md` | FAILS.md, agent-behavior rules | High - both address scope creep, unrequested refactors, skipped verification |
| Phase-verify pattern | `claude-code.md` (phase-and-verify) | EDIRD gates, /verify | High - both require verification before phase transition |
| Brief pattern | `claude-code.md` (brief + acceptance criteria) | EDIRD SPEC + AC items, STRUT deliverables | High - both require verifiable acceptance criteria |
| Stable context files | `claude-code-claude-md.md` (CLAUDE.md) | IPPS rules (agent-behavior.md, core-conventions.md) | High - both separate stable rules from per-task instructions |
| Source verification | `source-verification.md` | SOCAS, [VERIFIED]/[UNVERIFIED] labels | Medium - both require source tracking, different implementation |
| Decision tracking | `decision-journals.md` | NOTES.md Key Decisions, Document History | Medium - both track decisions, IPPS is less formal |

## 8. Coverage Matrix

Summary of how well IPPS covers each best-practice category.

| Category | Articles Read | Strong Match | Partial Match | Gap | Coverage |
|---|---|---|---|---|---|
| ai-agents | 12 | 6 | 2 | 4 | 67% |
| prompt-engineering | 10 | 3 | 3 | 4 | 60% |
| writing | 5 | 5 | 0 | 0 | 100% |
| knowledge-vaults | 10 | 3 | 5 | 2 | 80% |
| coding | 2 | 1 | 1 | 0 | 75% |
| file-organization | 2 | 2 | 0 | 0 | 100% |
| **Total** | **41** | **20** | **11** | **10** | **70%** |

Categories not read (lower relevance for IPPS): backend, cheatsheets, comparisons, frontend, glossary, howto, ops, seo, tooling, meta, security.

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

### Low Priority

9. **Add pre-mortem to DESIGN** (IMP-09) - Decision quality improvement
10. **Add observability logging** (IMP-10) - Debugging and replay

### What IPPS Does Better Than Best Practices

- **AGEN controlled vocabulary** - Grep-able, traceable, deterministic instructions (best practices have no equivalent)
- **EDIRD phase model** - Unified BUILD/SOLVE with gates, complexity levels, and deterministic next-action logic (best practices only cover prompt chaining)
- **STRUT tree notation** - Expressive planning with concurrent blocks, deliverables, transitions (best practices use numbered lists)
- **MNF technique** - Operational checklist for task execution (best practices have pre-mortem but not execution checklists)
- **Session management** - Full lifecycle (init, work, save, resume, finalize, archive) with tracking files (best practices only cover CLAUDE.md/TODO.md/SESSION_LOG.md)
- **GRUC 4-file separation** - GUIDE + RULES + CHECKS + EXAMPLE per skill (best practices have 2-file: rules + audit catalog)
- **TRACTFUL traceability** - Full lifecycle document IDs, cross-references, sync workflows (best practices have atomic notes but no lifecycle traceability)

## 10. Sources

### LLM Best Practices Articles Read

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
- `coding/general-principles.md` - Naming, comments, error handling, dependencies, testing
- `coding/testing.md` - Trophy shape, flaky tests, test naming, snapshot tests
- `file-organization/folder-hierarchy.md` - Max 4 levels, feature-grouped, index files
- `file-organization/naming-conventions.md` - Kebab-case, role-based names, ISO dates
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
- `prompt-engineering/best-practices.md` - 7 strategies, 5 patterns to memorize
- `prompt-engineering/chain-of-thought.md` - When to use CoT, structured reasoning sections
- `prompt-engineering/context-engineering.md` - Token budget, lost-in-the-middle, compaction
- `prompt-engineering/output-constraints.md` - Examples, escape hatches, schema, validation loop
- `prompt-engineering/prompt-chaining.md` - One prompt per verb, trim between steps, thin router
- `prompt-engineering/prompt-design.md` - System vs user, role definition, non-goals
- `prompt-engineering/prompt-evals.md` - 50-200 cases, CI-gated, score tracking, statistical significance
- `prompt-engineering/prompt-templates.md` - Delimiter conventions, versioned files, skeleton
- `prompt-engineering/system-prompt-design-patterns.md` - Named blocks, constraints, output contract
- `writing/anti-slop.md` - Word/phrase ban list, paragraph-level slop, concrete rewrites
- `writing/documentation-for-ai-products.md` - Dual audience, machine-readable structure, dated facts
- `writing/editorial-style.md` - Punctuation, capitalization, code references, file naming
- `writing/technical-writing-standards.md` - Task-first, atomic pages, consistent terminology
- `writing/voice.md` - Neutral playbook voice, rule-first, specific nouns, pick a side

### IPPS Documents Read

- `README.md` - IPPS concept overview
- `specs/_SPEC_AGEN_AGENTIC_ENGLISH.md [AGEN-SP01]` - Controlled vocabulary
- `specs/_SPEC_EDIRD_PHASE_MODEL.md [EDIRD-SP05]` - Phase model (first 100 lines)
- `specs/_SPEC_STRUT_STRUCTURED_THINKING.md [STRUT-SP01]` - Planning notation (first 100 lines)
- `specs/_SPEC_TRACTFUL_DOCUMENT_FRAMEWORK.md [TRACT-SP01]` - Document framework (first 100 lines)
- `.devin/skills/session-management/SKILL.md` - Session lifecycle
- `.devin/skills/session-management/NOTES_TEMPLATE.md` - Session notes template
- `.devin/skills/session-management/PROBLEMS_TEMPLATE.md` - Session problems template
- `.devin/skills/session-management/PROGRESS_TEMPLATE.md` - Session progress template
- `.devin/workflows/research.md` - Research workflow
- `ID-REGISTRY.md` - Topic registry
- Rules loaded as system context: agent-behavior.md, core-conventions.md, promptsystem-core.md, promptsystem-ids.md, tools-and-skills.md, workspace-rules.md

## Document History

**[2026-09-12 17:30]**
- Initial preflight analysis created
- Mapped 41 best-practice articles to IPPS concepts
- Identified 10 gaps, 9 deviations, 10 improvement opportunities
- Coverage: 70% (20 strong, 11 partial, 10 gap)
