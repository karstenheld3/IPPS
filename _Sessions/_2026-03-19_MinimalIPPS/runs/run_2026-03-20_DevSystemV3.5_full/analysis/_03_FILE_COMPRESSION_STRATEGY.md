# FILE_COMPRESSION_STRATEGY: DevSystem Compression Plan

**Doc ID**: CMPR-IP01
**Goal**: Categorize all DevSystem files into exclusion, primary, secondary, and drop buckets for token compression
**Exclusion criteria**: < 25 lines AND ≤ 2 references

## Table of Contents

1. [Exclusion List](#1-exclusion-list)
2. [Primary (Keep Mostly As-Is)](#2-primary-keep-mostly-as-is)
3. [Secondary (Compress)](#3-secondary-compress)
4. [Drop (Remove Entirely)](#4-drop-remove-entirely)
5. [Summary Statistics](#5-summary-statistics)

## 1. Exclusion List

Files too small or too rarely loaded to justify compression cost. Each is < 25 lines AND has ≤ 2 references. These remain untouched.

- `rules/workspace-rules.md` (4 lines, 0 references) - Empty trigger shell
- `rules/tools-and-skills.md` (18 lines, 1 reference) - Already minimal disambiguation
- `skills/travel-info/AT.md` (17 lines, 1 ref from SKILL.md)
- `skills/travel-info/BE.md` (16 lines, 1 ref)
- `skills/travel-info/CH.md` (18 lines, 1 ref)
- `skills/travel-info/DE.md` (22 lines, 1 ref)
- `skills/travel-info/ES.md` (18 lines, 1 ref)
- `skills/travel-info/EUROPE.md` (20 lines, 1 ref)
- `skills/travel-info/FLIGHTS.md` (17 lines, 1 ref)
- `skills/travel-info/FR.md` (19 lines, 1 ref)
- `skills/travel-info/IT.md` (20 lines, 1 ref)
- `skills/travel-info/NL.md` (17 lines, 1 ref)
- `skills/travel-info/TRAINS.md` (25 lines, 1 ref)
- `skills/travel-info/TRANSIT.md` (24 lines, 1 ref)
- `skills/travel-info/UK.md` (24 lines, 1 ref)
- `skills/llm-evaluation/prompts/answer-from-text.md` (15 lines, 1 ref)
- `skills/llm-evaluation/prompts/summarize-text.md` (17 lines, 1 ref)
- `skills/llm-evaluation/prompts/transcribe-page.md` (16 lines, 1 ref)
- `skills/llm-evaluation/prompts/judge-answer.md` (24 lines, 1 ref)
- `workflows/deep-research.md` (16 lines, 1 ref - routing wrapper only)
- `workflows/session-save.md` (23 lines, 2 refs)
- `skills/llm-evaluation/LLM_EVALUATION_CLAUDE_MODELS.md` (43 lines, 1 ref) - Already a compact lookup table; however at 43 lines it exceeds threshold. Included here because it's purely reference data with no prose to compress.

**Total excluded**: 22 files, ~435 lines. Already at minimal size.

## 2. Primary (Keep Mostly As-Is)

These files define core agent behavior, critical routing logic, or essential structural contracts. Simplifying them risks breaking agent behavior or losing critical distinctions.

### 2.1 Always-On Rules (loaded every conversation)

- **`rules/agent-behavior.md`** (58 lines)
  Why: Defines fundamental agent attitude, communication rules, confirmation rules, and session behavior. Every instruction is a behavioral constraint. Removing any line changes how the agent operates.

- **`rules/core-conventions.md`** (169 lines)
  Why: Universal formatting contract. Text style, date formats, document structure, header block format, APAPALAN principle summary, skill references. All downstream documents and skills depend on these conventions being unambiguous.

- **`rules/devsystem-core.md`** (266 lines)
  Why: Core definitions (workspace, project, session), folder structure, document types, workflow reference table, STRUT execution algorithm. This is the system's structural backbone. The folder structure diagrams and workflow reference are irreducible.

- **`rules/devsystem-ids.md`** (203 lines)
  Why: Complete ID system (topic registry, document IDs, review IDs, spec-level IDs, plan-level IDs, tracking IDs, source IDs, session IDs). Removing any ID format creates ambiguity downstream. The format definitions and examples are the specification.

- **`rules/edird-phase-planning.md`** (95 lines)
  Why: Phase model core - phases, principles, entry rule, gate summaries, phase tracking, planning notation, workflow types, stuck detection. Already compact. Every section is a behavioral gate that controls agent execution flow.

- **`rules/agentic-english.md`** (188 lines)
  Why: AGEN vocabulary - all verbs, labels, states, and placeholders used across the entire system. This is the shared language. Removing verbs means they can't be referenced in STRUT plans, workflows, or planning.

### 2.2 Critical Workflow Logic

- **`workflows/verify.md`** (284 lines)
  Why: Central verification hub. Context-specific verification rules for INFO, SPEC, IMPL, Code, TEST, Workflows, Skills, Sessions, and STRUT plans. Each context section contains specific check items. Compression would lose verification coverage.

- **`workflows/implement.md`** (116 lines)
  Why: Implementation execution logic with prerequisites, GLOBAL-RULES (trace scope, assess impact, define verification), context branching, operation mode check, impact assessment, execution sequence, gate check. Core implementation contract.

- **`workflows/go.md`** (95 lines)
  Why: Autonomous execution loop. Completion check, pre-flight, execute, loop control with iteration limits and blocker handling. The idempotent behavior section prevents wasted tokens.

- **`workflows/continue.md`** (128 lines)
  Why: Execution sequencing. Builds execution sequence from multiple sources, handles lifecycle workflows with confirmation, loop/stop logic. Critical for autonomous operation.

- **`workflows/bugfix.md`** (278 lines)
  Why: Complete bug-fixing pipeline (SESSION-MODE vs PROJECT-MODE determination, folder creation, reproduction, analysis, impact assessment, verification, documentation). Two distinct paths that must not be confused.

- **`workflows/build.md`** (41 lines)
  Why: BUILD workflow entry point. Already compact. Defines BUILD-specific rules (visual verification for UI, 100-line limit, artifact requirements).

- **`workflows/solve.md`** (42 lines)
  Why: SOLVE workflow entry point. Already compact. Defines SOLVE-specific rules (problem types, research requirements, primary output type).

- **`workflows/recap.md`** (66 lines)
  Why: State assessment. Mandatory re-read lists for SESSION-MODE and PROJECT-MODE. Determines exact position down to individual task. Already compact.

- **`workflows/commit.md`** (31 lines)
  Why: Commit workflow. Already minimal.

### 2.3 Essential Skill Entry Points

- **`skills/write-documents/SKILL.md`** (128 lines)
  Why: Document writing hub. Verb mapping, document type index with when-to-use, dependency chain, file naming, ID system quick reference. This routes to all templates and rules.

- **`skills/session-management/SKILL.md`** (134 lines)
  Why: Session lifecycle definition (Init → Work → Save → Resume → Finalize → Archive), folder location rules, required file definitions, assumed workflow, ID system reference. Core session contract.

- **`skills/edird-phase-planning/SKILL.md`** (195 lines)
  Why: Full phase gate definitions with checkboxes, workflow examples (BUILD HIGH and SOLVE EVALUATION), planning requirements, effort allocation budgets, retry limits, mandatory gate output format. This is the expanded version of the core rule.

- **`skills/coding-conventions/SKILL.md`** (36 lines)
  Why: Coding conventions hub. Routes to all rule files. Already minimal.

- **`skills/deep-research/SKILL.md`** (200 lines)
  Why: Research skill core. Phase model, prompt decomposition (7 questions), source hierarchy, verification labels, quality pipeline (VCRIV), inline citation format, domain profile index, strategy selection criteria. Irreducible specification.

- **`skills/ms-playwright-mcp/SKILL.md`** (185 lines)
  Why: Default browser automation. Intent lookup table, MUST-NOT-FORGET (critical safety: never auto-close browser, downloads to temp), configuration, available tools reference, common workflows, element selection. Primary browser skill.

### 2.4 Essential Templates

- **`skills/session-management/NOTES_TEMPLATE.md`** (71 lines)
  Why: Session notes structure. Initial request verbatim capture, session info, agent instructions, key decisions, bug list, significant prompts log. Template defines the contract for session continuity.

- **`skills/session-management/PROBLEMS_TEMPLATE.md`** (68 lines)
  Why: Problem tracking structure with Open/Resolved/Deferred sections, ID format, history tracking. Defines problem lifecycle.

- **`skills/session-management/PROGRESS_TEMPLATE.md`** (51 lines)
  Why: Progress tracking with To Do/In Progress/Done/Tried But Not Used sections. Already compact.

## 3. Secondary (Compress)

Files that can be reduced while preserving function. Specific compression targets identified per file.

### 3.1 Writing and Coding Rules (Heaviest Targets)

- **`skills/write-documents/APAPALAN_RULES.md`** (776 lines → target ~350)
  Compress: Reduce BAD/GOOD pairs to single-line contrasts. AP-BR-06 pipe-delimited section has 3 full BAD/GOOD examples (60+ lines) - keep 1. AP-ST-04 anti-DRY delegation example (30 lines) - condense to key pattern. AP-PR-02/03 formatting examples - keep format spec, drop verbose examples. Merge AP-NM rules into a table.

- **`skills/write-documents/MECT_WRITING_RULES.md`** (489 lines → target ~200)
  Compress: MW-VO rules have 3-4 BAD/GOOD pairs each - keep 1 per rule. MW-WC-01 confused pairs list (10+ entries) - keep 5 most common. MW-WC-02 plain language section - drop the full paragraph examples, keep transformation list. MW-TD-01 naming structure - keep the 4 steps, drop the extended BAD example. MW-DT-01 four-lens example - keep schema, drop rate limiter paragraph.

- **`skills/coding-conventions/MECT_CODING_RULES.md`** (688 lines → target ~300)
  Compress: MC-PR-01 has 3 code examples - keep 1. MC-CO-04 consistent patterns - 3 full code blocks for same idea - keep 1. MC-ND-01 through MC-ND-07 each have BAD/GOOD pairs - condense to format + 1 example each. Drop the "standard pairs" and "standard opposites" lists (readers know open/close, read/write). MC-BR-03 mechanism naming - keep rule, shorten examples.

- **`skills/coding-conventions/LOGGING-RULES.md`** (598 lines → target ~250)
  Compress: Philosophy section repeats goals that are restated in each specific rule file. Drop Complete Example at end (replicates patterns from individual rules). LOG-GN-06 property format has 4 BAD + 4 GOOD examples - keep 2. LOG-GN-08 error formatting - 3 separate pattern groups with examples - merge to 1. Philosophy-to-Rules Mapping section (50 lines) duplicates information derivable from the rule files themselves.

- **`skills/coding-conventions/LOGGING-RULES-APP-LEVEL.md`** (319 lines → target ~120)
  Compress: 5 complete examples at end (150+ lines) - keep 1 representative example, drop rest. LOG-AP-03 execution pattern - 3 separate example blocks - keep 1. LOG-AP-04 nesting example - keep the simple one, drop the deeply nested variant.

- **`skills/coding-conventions/LOGGING-RULES-SCRIPT-LEVEL.md`** (511 lines → target ~150)
  Compress: 7 complete examples (300+ lines, Examples 1-7) - keep 2 (one passing, one failing). LOG-SC-02 section structure has both bad and good with full output - condense. LOG-SC-06 output details - 3 example patterns - keep 1.

- **`skills/coding-conventions/LOGGING-RULES-USER-FACING.md`** (372 lines → target ~150)
  Compress: 5 complete examples (150+ lines) - keep 2 (scan + upload-with-retry). LOG-UF-02 progress indicators - 4 separate format demos - merge to reference table. LOG-UF-05 context display - 2 full examples - keep 1.

- **`skills/coding-conventions/AGENT-SKILL-RULES.md`** (412 lines → target ~200)
  Compress: Section 3 (SETUP.md Requirements) MCP config modification pattern - 40 lines of PowerShell that could be a reference link. Section 7 (Case Study) is 70 lines of historical narrative - condense to 5-line lessons learned. Section 8 (Token Optimization) repeats principles from WORKFLOW-RULES.md - merge or reference. Section 6 (Documentation Quality) is a 4-item list that could be 2 lines.

- **`skills/coding-conventions/PYTHON-RULES.md`** (356 lines → target ~180)
  Compress: PYTHON-FT-05 function grouping - 25-line BAD/GOOD pair showing comment markers - condense to format definition + 1 example. PYTHON-CM-02/03 docstring rules - 2 full function examples each - keep 1 each. PYTHON-NM-04 corresponding pairs list (15 pairs) - already compact but could be a comma-separated line.

- **`skills/write-documents/SPEC_RULES.md`** (397 lines → target ~180)
  Compress: SPEC-DG-02 UI diagrams - 2 full ASCII art diagrams (BAD 15 lines + GOOD 25 lines) - keep only GOOD. SPEC-CT-02 code outline - full BAD function (20 lines) vs GOOD (2 lines) - drop BAD, the GOOD is self-explanatory. SPEC-CT-04 event flow - already compact. Layer architecture diagram (15 lines) - keep. Summarize styling section - keep GOOD only.

- **`skills/write-documents/WORKFLOW_RULES.md`** (462 lines → target ~180)
  Compress: 17 rule sections each with BAD/GOOD pairs. Many BAD examples are 5-8 lines of "don't do this" that add little after seeing the GOOD. Keep GOOD examples only for simple rules (WF-HD, WF-ST, WF-RF). Keep BAD+GOOD for ambiguous rules (WF-CT-01, WF-BR-01). Drop WF-CT-07 entirely (no Document History in rule files - one-line rule).

- **`skills/write-documents/CONVERSATION_RULES.md`** (345 lines → target ~150)
  Compress: 16 rule sections with BAD/GOOD pairs. Email header format - 3 BAD + 1 GOOD (20 lines) - keep 1 BAD + 1 GOOD. WhatsApp sections - 3 separate rules with examples that could merge. Log entry format - keep GOOD only. URL format - trivially obvious, drop BAD.

- **`skills/coding-conventions/WORKFLOW-RULES.md`** (103 lines → target ~60)
  Compress: "Design principles" list repeats AGENT-SKILL-RULES.md principles 1-8 verbatim. Replace with cross-reference. Quality Checks section (15 lines) overlaps with `/verify` workflow's Workflow context.

- **`skills/coding-conventions/JSON-RULES.md`** (52 lines → target ~35)
  Compress: Effort mapping code example (10 lines) - reduce to 2-line pattern. Field naming BAD/GOOD - keep 1 pair, drop redundant examples.

### 3.2 Verbose Workflows

- **`workflows/critique.md`** (336 lines → target ~180)
  Compress: Research Phase section (40 lines) describes creating MUST-RESEARCH list with full format example - condense. Code review "5 architectural questions" section + "then review implementation details" has 4 categories with 4 questions each (60 lines) - compress to checklist. Context-specific sections for document types repeat patterns - merge common elements. Final Checklist + Output Format (50 lines) - condense.

- **`workflows/reconcile.md`** (205 lines → target ~120)
  Compress: Findings Checklist Format (60 lines of template) - compress to structure outline. Verification Questions section - 3 questions with sub-items (20 lines) - compress to checklist. Code Review Questions and Document Review Questions have 5 items each with explanations - drop explanations, keep questions only.

- **`workflows/transcribe.md`** (569 lines → target ~250)
  Compress: Figure Transcription Protocol (150 lines) - the Step F0/F1/F2/F3 sequence with full example is verbose. Keep the rules, compress the example. Appendix Built-in Prompt (80 lines) - duplicates much of `llm-transcription/prompts/transcription.md`. Long Document Strategy section (20 lines) - already compact. Mode A/B detection and branching adds ~40 lines of PowerShell that could be condensed.

- **`workflows/sync.md`** (165 lines → target ~100)
  Compress: Sync Direction Reference diagram (25 lines) + 6 context-specific sections each with similar structure. Merge common patterns. Verification Label Updates section repeats label definitions from verify.md.

- **`workflows/fail.md`** (166 lines → target ~90)
  Compress: Step 2 (Analyze Context) has 6 sub-steps with 2-3 lines each (30 lines) - compress to checklist. Step 5 (Re-read Failed Workflow) is verbose procedural (25 lines) - compress to "re-read workflow that failed, compare instructions vs execution".

- **`workflows/learn.md`** (163 lines → target ~80)
  Compress: Steps 3-8 each gather a specific dimension but are written as full paragraphs with sub-items. Compress to flat checklist. Step 8 (Problem Dependency Tree) - keep template, drop explanation. Quality Gate overlaps with Step 10.

- **`workflows/improve.md`** (83 lines → target ~50)
  Compress: Three quality check sections (APAPALAN, MECT Writing, MECT Coding) each list 6-8 specific rules with codes - these are just filtered views of the rule files. Replace with "verify against APAPALAN_RULES.md rules AP-PR-07, AP-PR-09, AP-BR-02, AP-NM-01, AP-NM-05, AP-ST-01" etc.

- **`workflows/test.md`** (80 lines → target ~50)
  Compress: 4 context sections (UI, Code, Build, Deploy) each with 5 steps. Some steps are generic ("Document results"). Condense to action items only.

- **`workflows/rename.md`** (52 lines → target ~35)
  Compress: 4-phase structure with grep_search code block and numbered steps - condense phase descriptions.

- **`workflows/prime.md`** (47 lines → target ~30)
  Compress: Step-by-step with PowerShell find_by_name commands that could be condensed.

- **`workflows/fix.md`** (68 lines → target ~40)
  Compress: Step 2 lists 5 problem types with 3 files each to read (30 lines) - compress to routing table.

- **`workflows/project-release.md`** (141 lines → target ~70)
  Compress: Full release notes template (60 lines) embedded in step 3 - compress to structure outline. PowerShell commands in steps 1/4/5/7 are already compact.

- **`workflows/switch-model.md`** (65 lines → target ~35)
  Compress: Three nearly identical PowerShell blocks for HIGH/MID/LOW differing only in query string. Unify to single parameterized block.

- **`workflows/partition.md`** (81 lines → target ~50)
  Compress: 4 strategy descriptions (DEFAULT/DEPENDENCY/SLICE/RISK) - each 4-5 lines - condense to 2 lines each.

- **`workflows/session-finalize.md`** (64 lines → target ~40)
  Compress: 7 steps with similar structure - condense step descriptions.

- **`workflows/session-new.md`** (55 lines → target ~35)
  Compress: Steps are already fairly compact but Step 5 (Document Agent Instructions) has verbose guidance.

- **`workflows/session-load.md`** (49 lines → target ~32)
  Compress: PowerShell one-liner in Step 1 is necessary. Steps 4-5 have prose that can condense.

- **`workflows/session-archive.md`** (35 lines → target ~25)
  Compress: Example section repeats the command from Steps section.

- **`workflows/write-info.md`** (101 lines → target ~50)
  Compress: 8 steps with think-aloud questions in Step 3 (20 lines) - condense. Document Structure example at end (20 lines) - redundant with INFO_TEMPLATE.md.

- **`workflows/write-impl-plan.md`** (57 lines → target ~35)
  Compress: 7 steps - each description is 2-3 lines - can be 1 line each.

- **`workflows/write-spec.md`** (55 lines → target ~35)
  Compress: Similar pattern - condense step descriptions.

- **`workflows/write-test-plan.md`** (61 lines → target ~35)
  Compress: Similar pattern.

- **`workflows/write-tasks-plan.md`** (107 lines → target ~45)
  Compress: Full document structure template (55 lines) at bottom duplicates TASKS_TEMPLATE.md. Remove embedded template, reference template instead.

- **`workflows/write-strut.md`** (37 lines → target ~25)
  Compress: Already compact. Minor trimming.

- **`workflows/research.md`** (36 lines → target ~25)
  Compress: Workflow narrative paragraph (10 lines) can be condensed.

### 3.3 Skill Files (Compress)

- **`skills/deep-research/RESEARCH_STRATEGY_MCPI.md`** (231 lines → target ~130)
  Compress: Phase 1 has 6 steps with verbose "Done when" criteria. Phase 3 execution has 7 sub-steps. Global Rules and Scoring Model sections. Condense step descriptions, keep structure.

- **`skills/deep-research/RESEARCH_STRATEGY_MEPI.md`** (202 lines → target ~110)
  Compress: Mirrors MCPI structure. Anti-patterns section (10 lines) states obvious. Scoring model section (25 lines) could reference MCPI's.

- **`skills/deep-research/RESEARCH_TOOLS.md`** (334 lines → target ~150)
  Compress: Tool Selection Flowchart (20 lines) + 4 Common Workflows (80 lines total) + Anti-Patterns (10 lines) + detailed decision criteria. The 4 workflows are PowerShell command sequences that could be condensed. PDF processing workflow (60 lines) has step-by-step that could be a compact reference.

- **`skills/deep-research/RESEARCH_TOC_TEMPLATE.md`** (88 lines → target ~50)
  Compress: Template instructions in HTML comment (10 lines) are one-time guidance. Topic Details section example is verbose.

- **`skills/deep-research/RESEARCH_CREATE_TOC.md`** (55 lines → target ~35)
  Compress: 10-step workflow with quality gates - condense step descriptions.

- **`skills/deep-research/DOMAIN_DEFAULT.md`** (95 lines → target ~50)
  Compress: Available QA Tools section (30 lines) lists tools already documented in RESEARCH_TOOLS.md. VCRIV Pipeline section restates what's in SKILL.md.

- **`skills/deep-research/DOMAIN_DOCUMENT_INTEL.md`** (53 lines → target ~35)
  Compress: Folder structure example (10 lines) - condense. Quality Criteria section overlaps with SKILL.md VCRIV.

- **`skills/deep-research/DOMAIN_LEGAL.md`** (54 lines → target ~35)
  Compress: Similar to DOCUMENT_INTEL - condense folder structure and quality criteria.

- **`skills/deep-research/DOMAIN_MARKET_INTEL.md`** (45 lines → target ~30)
  Compress: Template additions and quality criteria sections can condense.

- **`skills/deep-research/DOMAIN_SOFTWARE.md`** (44 lines → target ~30)
  Compress: Template additions section - condense.

- **`skills/ms-playwright-mcp/PLAYWRIGHT_ADVANCED_WORKFLOWS.md`** (188 lines → target ~100)
  Compress: 5 sections each with full code blocks. Cookie popup has 2 strategies (Strategy A 5 lines + Strategy B 15 lines of JS) - keep both but trim explanations. Scroll strategies have 4 variants - keep 2.

- **`skills/ms-playwright-mcp/PLAYWRIGHT_FULL_PAGE_SCREENSHOT.md`** (89 lines → target ~45)
  Compress: 4 scroll strategies overlap with ADVANCED_WORKFLOWS.md - reference instead of duplicate. Complete Workflow section (20 lines) also in ADVANCED_WORKFLOWS.

- **`skills/ms-playwright-mcp/PLAYWRIGHT_TROUBLESHOOTING.md`** (51 lines → target ~35)
  Compress: Flaky Test Prevention section (15 lines) is generic advice.

- **`skills/ms-playwright-mcp/PLAYWRIGHT_AUTHENTICATION.md`** (46 lines → target ~30)
  Compress: 3 strategies with code blocks - condense explanations.

- **`skills/ms-playwright-mcp/SETUP.md`** (404 lines → target ~180)
  Compress: PowerShell installation script (150 lines) with verbose state checking, backup handling, PSCustomObject conversion. Keep essential commands, drop defensive coding patterns that are script implementation detail. Installation Summary section (40 lines) is informational output.

- **`skills/ms-playwright-mcp/UNINSTALL.md`** (255 lines → target ~100)
  Compress: PowerShell uninstall script (180 lines) with 4-option interactive menu. Keep command list, compress interactive menu logic. Manual Removal section (40 lines) duplicates script actions.

- **`skills/playwriter-mcp/SKILL.md`** (265 lines → target ~130)
  Compress: Intent Lookup section (20 lines) overlaps with ms-playwright-mcp. CLI Commands section with examples. Common Workflows overlap with Quick Start. Screen Recording section marked [ASSUMED].

- **`skills/playwriter-mcp/SETUP.md`** (300 lines → target ~120)
  Compress: PowerShell MCP config script (100 lines) follows same pattern as ms-playwright-mcp SETUP. Configuration Options section (40 lines) - condense.

- **`skills/playwriter-mcp/UNINSTALL.md`** (114 lines → target ~50)
  Compress: 5-step manual procedure. Verification section duplicates steps.

- **`skills/google-account/SKILL.md`** (391 lines → target ~180)
  Compress: Gmail/Calendar/Tasks/Drive operations (150 lines of command examples) - keep 1 example per category, reference `gog --help` for rest. Configuration section (40 lines) repeats command template. Token Expiry Re-Auth Flow (60 lines) - condense steps. Common Mistakes (30 lines) - keep but condense.

- **`skills/google-account/SETUP.md`** (456 lines → target ~200)
  Compress: Quick OAuth Setup (80 lines) + Pre-Installation Verification (60 lines) + Installation with 3 options (90 lines) + Steps 2-10 (120 lines). Condense multi-option installations to primary option + notes. Pre-installation checklists are valuable but verbose.

- **`skills/google-account/UNINSTALL.md`** (307 lines → target ~120)
  Compress: PowerShell interactive menu script (200 lines) - compress to command list. Manual Removal section (50 lines) duplicates.

- **`skills/pdf-tools/SKILL.md`** (295 lines → target ~150)
  Compress: Optimization Strategies section (80 lines) with 3 strategies + key flags + best practices. Complete CLI reference for 5 tools (100 lines) - keep essential commands, drop alternative flags.

- **`skills/pdf-tools/SETUP.md`** (212 lines → target ~100)
  Compress: 7 installation sections with check-if-installed + download + verify pattern. Condense to command sequences.

- **`skills/git/SKILL.md`** (313 lines → target ~150)
  Compress: Guided Recovery Workflow (40 lines) walks through 5 steps that are just `git show` and `git checkout` commands. Common Patterns section (30 lines) repeats earlier commands. Batch Operations and Comparing Versions sections are compact.

- **`skills/git/SETUP.md`** (113 lines → target ~60)
  Compress: 3 installation methods + verification + troubleshooting. Keep Method 1 (winget), condense others.

- **`skills/git-conventions/SKILL.md`** (157 lines → target ~80)
  Compress: Safe Undo Commit section (50 lines) with 6 code blocks for different scenarios. Condense. .gitignore template (30 lines) - keep but trim comments.

- **`skills/github/SKILL.md`** (188 lines → target ~90)
  Compress: 8 sections (Auth, Repo, Issues, PRs, Releases, Gists, Workflows, Common Patterns) each with command examples. Many commands are `gh <subcommand>` one-liners - merge into compact reference.

- **`skills/github/SETUP.md`** (69 lines → target ~40)
  Compress: Download URL + extract + verify pattern - condense.

- **`skills/llm-evaluation/SKILL.md`** (60 lines → target ~40)
  Compress: "Key Findings" section (15 lines) states session-specific test results. Keep recommendations, drop specifics.

- **`skills/llm-evaluation/SETUP.md`** (214 lines → target ~80)
  Compress: Steps 1-8 follow check-create-install-verify pattern. Verification script (30 lines) is verbose. Troubleshooting section (20 lines) - condense.

- **`skills/llm-evaluation/UNINSTALL.md`** (151 lines → target ~60)
  Compress: Interactive PowerShell script (100 lines) - compress to command list.

- **`skills/llm-evaluation/LLM_EVALUATION_SCRIPTS.md`** (241 lines → target ~130)
  Compress: 8 scripts each with parameters list + examples. Keep parameters, drop some example combinations. Pipeline Example section (20 lines) - keep.

- **`skills/llm-evaluation/LLM_EVALUATION_TESTED_MODELS.md`** (60 lines → target ~35)
  Compress: Model lists with dates - condense to table-style format.

- **`skills/llm-computer-use/SKILL.md`** (82 lines → target ~50)
  Compress: Cost estimate table + options list - condense. Safety section (5 lines) - keep.

- **`skills/llm-transcription/SKILL.md`** (89 lines → target ~50)
  Compress: Model Recommendations table (20 lines) - condense. Usage examples section - keep 1 per script.

- **`skills/llm-transcription/SETUP.md`** (73 lines → target ~40)
  Compress: Standard setup pattern. Condense troubleshooting.

- **`skills/llm-transcription/UNINSTALL.md`** (170 lines → target ~60)
  Compress: Interactive PowerShell (120 lines) - compress to commands.

- **`skills/llm-transcription/prompts/transcription.md`** (220 lines → target ~140)
  Compress: Critical rules section is essential. Table example section (30 lines) - condense. Anti-duplication rule explanation (15 lines) - condense. Keep all tag definitions and format rules.

- **`skills/llm-transcription/prompts/judge.md`** (127 lines → target ~80)
  Compress: Scoring scales have detailed criteria. Keep numeric thresholds, drop verbose justification text. Output format JSON example (20 lines) - keep as reference.

- **`skills/llm-evaluation/prompts/compare-image-transcription.md`** (64 lines → target ~40)
  Compress: 4 evaluation criteria sections with point allocations. Scoring Guide (10 lines) - condense.

- **`skills/windows-desktop-control/SKILL.md`** (42 lines → target ~30)
  Compress: Parameters list and DPI Scaling note - trim.

- **`skills/windsurf-auto-model-switcher/SKILL.md`** (70 lines → target ~40)
  Compress: Model Hints section (10 lines) + Troubleshooting (8 lines) - condense.

- **`skills/windsurf-auto-model-switcher/SETUP.md`** (83 lines → target ~45)
  Compress: PowerShell setup script + manual alternative. Keep one method.

- **`skills/windsurf-auto-model-switcher/UNINSTALL.md`** (63 lines → target ~35)
  Compress: PowerShell script + verify steps.

- **`skills/windsurf-auto-model-switcher/update-model-registry/README.md`** (37 lines → target ~20)
  Compress: Quick Reference table + descriptions - condense.

- **`skills/windsurf-auto-model-switcher/update-model-registry/UPDATE_WINDSURF_MODEL_REGISTRY.md`** (82 lines → target ~45)
  Compress: 3 methods (Docs/UI/Playwright) - condense to primary method + fallback notes.

- **`skills/travel-info/SKILL.md`** (35 lines → target ~25)
  Compress: Examples section (6 lines) - trim to 3.

### 3.4 Templates (Compress)

- **`skills/write-documents/STRUT_TEMPLATE.md`** (237 lines → target ~130)
  Compress: 3 full examples (Simple Hotfix 25 lines, Multi-Phase Feature 35 lines, Research Task 20 lines) - keep 1 (Multi-Phase), drop rest. Concurrent Blocks section (60 lines) with Auth System example - condense to rules + short example.

- **`skills/write-documents/TASKS_TEMPLATE.md`** (183 lines → target ~80)
  Compress: Full Example section (70 lines) duplicates the template structure shown above. Drop full example, keep template + field definitions.

- **`skills/write-documents/CONVERSATION_TEMPLATE.md`** (112 lines → target ~70)
  Compress: MUST-NOT-FORGET section (20 lines) restates CONVERSATION_RULES. Condense to key format reminders.

- **`skills/write-documents/SPEC_TEMPLATE.md`** (169 lines → target ~90)
  Compress: BAD/GOOD example in FR section (10 lines) duplicates SPEC_RULES.md. ASCII diagram example (20 lines) - condense. Remove inline guidance comments.

- **`skills/write-documents/TEST_TEMPLATE.md`** (134 lines → target ~70)
  Compress: Skeleton sections with placeholder descriptions. Condense section descriptions.

- **`skills/write-documents/IMPL_TEMPLATE.md`** (127 lines → target ~70)
  Compress: BAD/GOOD code example (20 lines) duplicates SPEC_RULES. Edge case categories list (5 lines) is guidance - condense.

- **`skills/write-documents