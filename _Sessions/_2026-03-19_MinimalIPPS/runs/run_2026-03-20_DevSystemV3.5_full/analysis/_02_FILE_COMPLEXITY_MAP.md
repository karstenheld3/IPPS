# File Complexity Map

**Doc ID**: DVSYS-IN02
**Goal**: Exhaustive complexity analysis of all DevSystem files for cognitive load assessment

## 1. Concept Inventory

### 1.1 Core System Concepts (36 concepts)

- WORKSPACE, PROJECT, SESSION (scope boundaries)
- AGENT_FOLDER, WORKSPACE_FOLDER, PROJECT_FOLDER, SESSION_FOLDER, SRC_FOLDER, DEVSYSTEM_FOLDER, DEFAULT_SESSIONS_FOLDER, SESSION_ARCHIVE_FOLDER (path placeholders)
- ACTOR (decision-making entity)
- SINGLE-PROJECT, MONOREPO (project structure)
- SINGLE-VERSION, MULTI-VERSION (version strategy)
- SESSION-MODE, PROJECT-MODE (work mode)
- IMPL-CODEBASE, IMPL-ISOLATED (operation modes)
- COMPLEXITY-LOW, COMPLEXITY-MEDIUM, COMPLEXITY-HIGH (complexity levels)
- BUILD, SOLVE (workflow types)
- Document types: INFO, SPEC, IMPL, TEST, TASKS, STRUT, REVIEW, LEARNINGS, FIXES, CONVERSATION
- Tracking documents: NOTES, PROGRESS, PROBLEMS, FAILS
- MNF technique (MUST-NOT-FORGET)
- Priority files (! prefix), Ignored files (_ prefix), Hidden files (. prefix), Temporary files (.tmp prefix)
- GLOB prefix (workspace-level tracking)

### 1.2 AGEN Vocabulary (62 concepts)

- Information Gathering verbs (8): RESEARCH, ANALYZE, EXPLORE, INVESTIGATE, GATHER, PRIME, READ, (reserved)
- Thinking/Planning verbs (12): SCOPE, FRAME, PLAN, PARTITION, DECIDE, ASSESS, PRIORITIZE, EVALUATE, SYNTHESIZE, CONCLUDE, DEFINE, RECAP, CONTINUE, GO
- Validation verbs (7): PROVE, PROTOTYPE, VERIFY, TEST, REVIEW, CRITIQUE, RECONCILE
- Documentation verbs (9): WRITE, WRITE-INFO, WRITE-SPEC, WRITE-IMPL-PLAN, WRITE-TEST-PLAN, OUTLINE, SUMMARIZE, DRAFT
- Implementation verbs (7): IMPLEMENT, CONFIGURE, INTEGRATE, REFACTOR, FIX, IMPROVE, OPTIMIZE
- Communication verbs (8): CONSULT, CLARIFY, QUESTION, STATUS, PROPOSE, RECOMMEND, CONFIRMS, PRESENT
- Completion verbs (7): HANDOFF, COMMIT, MERGE, DEPLOY, FINALIZE, CLOSE, ARCHIVE
- Verb modifiers (3): -OK, -FAIL, -SKIP
- Assumption labels (4): UNVERIFIED, CONTRADICTS, OUTDATED, INCOMPLETE
- Status labels (3): RESOLVED, WONT-FIX, NEEDS-DISCUSSION
- Bracket vs no-bracket syntax distinction

### 1.3 EDIRD Phase Model (28 concepts)

- 5 phases: EXPLORE, DESIGN, IMPLEMENT, REFINE, DELIVER
- 5 gate transitions with checklist items
- Gate enforcement, artifact verification, gate output
- Retry limits (infinite for LOW, 5 for MEDIUM/HIGH)
- Visual verification rule
- Entry rule (all workflows start EXPLORE with ASSESS)
- Phase tracking (NOTES.md + PROGRESS.md)
- Stuck detection
- BUILD assessment: COMPLEXITY-LOW/MEDIUM/HIGH
- SOLVE assessment: RESEARCH, ANALYSIS, EVALUATION, WRITING, DECISION, HOTFIX, BUGFIX
- Required documents by complexity (LOW: inline, MEDIUM: SPEC+IMPL, HIGH: all)
- Planning notation: STRUT (high-level) vs TASKS (low-level)
- Phase budgets by complexity
- Diminishing returns detection
- AWT (Agentic Work Time), HHW (Human-Hour Work)
- Next Action Logic

### 1.4 ID System (32 concepts)

- Topic Registry (ID-REGISTRY.md)
- 2-digit vs 4-digit number formats
- Document ID format: [TOPIC]-[DOC][NN]
- Document types: IN, SP, IP, TP, TK, RV, LN
- Review ID format: [SOURCE-DOC-ID]-RV[NN]
- Spec-level items: FR (Functional Requirement), IG (Implementation Guarantee), DD (Design Decision), AC (Acceptance Criteria)
- Plan-level items: EC (Edge Case), IS (Implementation Step), VC (Verification Checklist), TC (Test Case), TK (Task)
- Tracking IDs: BG (Bug), FT (Feature), PR (Problem), FX (Fix), FL (Failure)
- INFO Source ID format: [TOPIC]-[DOC]-SC-[SOURCE_ID]-[SOURCE_REF]
- Session Document ID format: YYYY-MM-DD_[SessionTopicCamelCase]-[TYPE]
- GLOB prefix usage rules

### 1.5 Text and Formatting Conventions (22 concepts)

- ASCII double/single quotes only
- No emojis (unless DevSystem tag opt-in)
- No Markdown tables (unless DevSystem tag opt-in)
- Unicode box-drawing characters (trees: `├─>` `└─>`, boxes: `┌─` `├─` `└─`)
- ASCII for UI diagrams
- Date formats (5 context-specific variants)
- Document structure (TOC placement, no `---` markers, one empty line)
- Header block (Doc ID, Goal, Target file, Depends on, Does not depend on)
- Document History (reverse chronological, action prefixes)
- DevSystem tags: MarkdownTablesAllowed, EmojisAllowed
- Allowed emojis when enabled (6): ✅ ❌ ⚠️ ★ ☆ ⯪
- Skill reference format: @skills:skill-name
- APAPALAN principle (As Precise As Possible, As Little As Necessary)
- Temporary files (.tmp prefix)
- Transcription output rules (no metadata, preserve original)

### 1.6 STRUT Notation (18 concepts)

- Phase ID (P1, P2), Step ID (P1-S1), Deliverable ID (P1-D1)
- Checkbox states: [ ] pending, [x] done, [N] retry count
- 5 node types: Objectives, Strategy, Steps, Deliverables, Transitions
- Objective-Deliverable linking (`← P1-Dx`)
- Transition targets: [PHASE-NAME], [CONSULT], [END]
- Concurrent blocks (virtual step, implicit barrier)
- Step dependencies (`← Px-Sy`)
- Model hints in Strategy sections
- Time Log section
- Execution algorithm (6 steps)
- Verification gates (planning time, phase transitions)
- Resuming interrupted plans
- Embedding in documents

### 1.7 APAPALAN Writing Rules (24 rules)

- Precision: PR-01 through PR-09 (datetime, attributes, contacts, links, IDs, acronyms, specificity, examples, consistency)
- Brevity: BR-01 through BR-06 (single line, grammar sacrifice, DRY, compact objects, show format, pipe-delimited)
- Structure: ST-01 through ST-06 (goal first, actionable subjects, self-contained, anti-DRY delegation, hierarchical ordering, visual grouping)
- Naming: NM-01 through NM-05 (one name, unambiguous compounds, meta-words, opposites, standard terms)

### 1.8 MECT Writing Rules (17 rules)

- Voice: VO-01 through VO-04 (active voice, address "you", simplest verb, obligation words)
- Word Choice: WC-01 through WC-04 (word precision, plain language, no recursive naming, no product-term collision)
- Terminology Design: TD-01 through TD-02 (naming structure method, output-named procedures)
- Headings/Sections: HS-01 through HS-03 (informative headings, three-level depth, declared audience)
- Lists/Tables: LT-01 through LT-03 (two identifiers per row, topology grouping, indexed groups)
- Description Types: DT-01 through DT-03 (four lenses, audience matching, canonical form)

### 1.9 MECT Coding Rules (27 rules)

- Precision: MC-PR-01 through MC-PR-07 (one name, unambiguous compounds, meta-words, specific comments, error messages, log messages, canonical identifiers)
- Brevity: MC-BR-01 through MC-BR-04 (simplest verb, drop filler, output-named functions, boolean predicates)
- Consistency: MC-CO-01 through MC-CO-05 (corresponding pairs, log format, convergent naming, consistent patterns, keep API names)
- Naming Design: MC-ND-01 through MC-ND-07 (naming structure, canonical form, no recursive naming, no product collision, domain types, qualify-not-rename, intuitive opposites)
- Documentation: MC-DC-01 through MC-DC-03 (four descriptions, audience matching, plain language)

### 1.10 Python Rules (24 rules)

- Formatting: PYTHON-FT-01 through FT-05
- Imports: PYTHON-IM-01 through IM-05
- Code Generation: PYTHON-CG-01 through CG-09
- Naming: PYTHON-NM-01 through NM-08
- Comments: PYTHON-CM-01 through CM-05

### 1.11 Logging Rules (30 rules)

- General: LOG-GN-01 through GN-12 (indentation, quoting, numbers first, duration, singular/plural, properties, UNKNOWN, error formatting, log before execute, ellipsis, sentence endings, no acronyms)
- User-Facing: LOG-UF-01 through UF-06 (timestamps, progress indicators, messages/results, feedback timing, context display, activity boundaries)
- App-Level: LOG-AP-01 through AP-05 (extended timestamps, log levels, execution pattern, execution boundaries, error context)
- Script-Level: LOG-SC-01 through SC-07 (no timestamps, section structure, test case IDs, status markers, status patterns, output details, summary/result)
- Logging philosophy concepts (7): APAPALAN, Least Surprise, Full Disclosure, Visible Structure, Announce>Track>Report, Two-Level Errors, Arrow Convention

### 1.12 Workflow Rules (18 rules)

- Header: WF-HD-01 through HD-04
- Structure: WF-ST-01 through ST-06
- References: WF-RF-01 through RF-04
- Content: WF-CT-01 through CT-07
- Branching: WF-BR-01 through BR-04

### 1.13 Spec Rules (12 rules)

- Requirements: SPEC-RQ-01 through RQ-03
- Diagrams: SPEC-DG-01 through DG-03
- Content: SPEC-CT-01 through CT-07
- Format: SPEC-FT-01 through FT-03

### 1.14 Agent Skill Rules (9 concepts)

- SKILL.md required content (7 sections)
- SETUP.md structure (pre-install, install, post-install)
- UNINSTALL.md structure (pre-uninstall, uninstall, post-uninstall)
- MCP config modification pattern
- Token optimization (8 principles)
- JSON intermediate output pattern
- Skill review checklist (11 items)
- Compact vs verbose format criteria

### 1.15 Conversation Rules (18 rules)

- Datetime: CV-DT-01 through DT-03
- Translation: CV-TR-01 through TR-02
- Email: CV-EM-01 through EM-04
- WhatsApp: CV-WA-01 through WA-03
- Structure: CV-ST-01 through ST-04
- Attachments: CV-AT-01 through AT-02
- Todos: CV-TD-01 through TD-02
- Links: CV-LN-01 through LN-02

### 1.16 Deep Research System (26 concepts)

- MEPI (Most Executable Point of Information) strategy
- MCPI (Most Complete Point of Information) strategy
- 4-phase model: Preflight, Planning, Research, Final Verification
- Prompt Decomposition (7 questions, JSON schema)
- Scope levels: NARROW, FOCUSED, EXPLORATORY
- Domain profiles: SOFTWARE, MARKET_INTEL, DOCUMENT_INTEL, LEGAL, DEFAULT
- Source hierarchy (8 tiers)
- Verification labels (5): VERIFIED, ASSUMED, TESTED, PROVEN, COMMUNITY
- VCRIV pipeline (Verify, Critique, Reconcile, Implement, Verify)
- Source tiers per domain profile
- Scoring model for ranking
- Discovery platforms (identify, test, classify: FREE/PAID/PARTIAL)
- TOC creation workflow
- Source ID format
- Effort estimation and validation
- Termination criteria (max 2 cycles)

### 1.17 Session Management (12 concepts)

- Session lifecycle: Init, Work, Save, Resume, Finalize, Archive
- Session folder naming: `_YYYY-MM-DD_[Topic]/`
- Required files: NOTES.md, PROBLEMS.md, PROGRESS.md
- Session-first rule for FAILS location
- Phase tracking in NOTES.md and PROGRESS.md
- _BugFixes permanent session
- Bug List in NOTES.md
- Significant Prompts Log
- Operation Mode tracking
- Initial Request recording (verbatim)
- STOP after session init rule

### 1.18 Git Conventions (10 concepts)

- Conventional Commits format
- 8 commit types (feat, fix, docs, refactor, test, chore, style, perf)
- Safe undo (soft, mixed, hard reset)
- Force push with lease
- .gitignore rules (5 categories)
- Git file recovery workflow
- Reflog recovery
- Batch recovery operations
- Guided recovery workflow
- Commit history navigation

### 1.19 Browser Automation (16 concepts)

- Playwright MCP (Microsoft) - default browser tool
- Playwriter MCP (Chrome extension) - authenticated sessions
- Accessibility tree navigation (ref=eN)
- Cookie popup handling (2 strategies)
- Lazy-load scrolling
- Full page screenshots
- Expand collapsed items
- Link extraction
- Persistent user profiles
- Storage state authentication
- Extension mode
- Visual labels (Playwriter)
- Screen recording (Playwriter)
- Session management (Playwriter)
- State persistence (Playwriter)
- Download handling (temp folder)

### 1.20 PDF and Transcription (14 concepts)

- PDF to JPG conversion (convert-pdf-to-jpg.py)
- PDF text extraction (pdftotext)
- PDF metadata (pdfinfo)
- PDF compression (compress-pdf.py, Ghostscript)
- PDF downsizing (two-pass workflow)
- Image transcription (ensemble + judge + refinement)
- Audio transcription
- Figure Transcription Protocol (ASCII + XML)
- Page boundary markers (header/footer tags)
- Transcription tags: transcription_image, transcription_table, transcription_json, transcription_notes
- Mode A (LLM skill) vs Mode B (built-in prompt)
- DPI selection (120 for transcription, 300 for OCR)
- Long document strategy (50+ pages)

### 1.21 LLM Evaluation (15 concepts)

- call-llm.py (single call)
- call-llm-batch.py (parallel batch)
- find-workers-limit.py (concurrency discovery)
- generate-questions.py / generate-answers.py / evaluate-answers.py pipeline
- compare-transcription-runs.py (hybrid comparison)
- Model registry (model-registry.json)
- Model pricing (model-pricing.json)
- Effort levels (none, minimal, low, medium, high, xhigh)
- Prompt caching (OpenAI automatic, Anthropic explicit)
- Judge prompt calibration
- Worker limits per provider
- Claude model ID format (with date suffix)
- UPDATE_MODEL_PRICING workflow
- UPDATE_MODEL_REGISTRY workflow

**Total unique concepts: ~380+**

## 2. Per-File Complexity Analysis

### 2.1 Rules

| Path | Lines | Tokens | Concepts | Rules | Steps | Branching | Load Freq |
|------|------:|-------:|---------:|------:|------:|----------:|----------:|
| rules/agent-behavior.md | 58 | 412 | 8 | 5 | 4 | 3 | 150 |
| rules/agentic-english.md | 188 | 1816 | 62 | 0 | 0 | 3 | 12 |
| rules/core-conventions.md | 169 | 1709 | 22 | 8 | 0 | 5 | 150 |
| rules/devsystem-core.md | 266 | 2614 | 36 | 6 | 6 | 8 | 150 |
| rules/devsystem-ids.md | 203 | 2077 | 32 | 12 | 0 | 2 | 150 |
| rules/edird-phase-planning.md | 95 | 1179 | 28 | 5 | 0 | 12 | 18 |
| rules/tools-and-skills.md | 18 | 153 | 2 | 0 | 0 | 2 | 150 |
| rules/workspace-rules.md | 4 | 7 | 0 | 0 | 0 | 0 | 150 |

### 2.2 Skills - Coding Conventions

| Path | Lines | Tokens | Concepts | Rules | Steps | Branching | Load Freq |
|------|------:|-------:|---------:|------:|------:|----------:|----------:|
| skills/coding-conventions/AGENT-SKILL-RULES.md | 412 | 3211 | 9 | 9 | 5 | 6 | 3 |
| skills/coding-conventions/JSON-RULES.md | 52 | 518 | 5 | 5 | 0 | 0 | 2 |
| skills/coding-conventions/LOGGING-RULES-APP-LEVEL.md | 319 | 3729 | 7 | 5 | 0 | 3 | 3 |
| skills/coding-conventions/LOGGING-RULES-SCRIPT-LEVEL.md | 511 | 4188 | 7 | 7 | 0 | 4 | 3 |
| skills/coding-conventions/LOGGING-RULES-USER-FACING.md | 372 | 3678 | 7 | 6 | 0 | 3 | 3 |
| skills/coding-conventions/LOGGING-RULES.md | 598 | 4999 | 19 | 12 | 0 | 4 | 5 |
| skills/coding-conventions/MECT_CODING_RULES.md | 688 | 5292 | 27 | 27 | 0 | 2 | 4 |
| skills/coding-conventions/PYTHON-RULES.md | 356 | 2816 | 5 | 24 | 0 | 2 | 3 |
| skills/coding-conventions/SKILL.md | 36 | 346 | 3 | 0 | 0 | 2 | 8 |
| skills/coding-conventions/WORKFLOW-RULES.md | 103 | 824 | 3 | 8 | 0 | 2 | 3 |

### 2.3 Skills - Deep Research

| Path | Lines | Tokens | Concepts | Rules | Steps | Branching | Load Freq |
|------|------:|-------:|---------:|------:|------:|----------:|----------:|
| skills/deep-research/DOMAIN_DEFAULT.md | 95 | 932 | 8 | 3 | 5 | 2 | 2 |
| skills/deep-research/DOMAIN_DOCUMENT_INTEL.md | 53 | 589 | 4 | 4 | 0 | 1 | 1 |
| skills/deep-research/DOMAIN_LEGAL.md | 54 | 676 | 5 | 7 | 0 | 1 | 1 |
| skills/deep-research/DOMAIN_MARKET_INTEL.md | 45 | 566 | 4 | 6 | 0 | 1 | 1 |
| skills/deep-research/DOMAIN_SOFTWARE.md | 44 | 441 | 4 | 6 | 0 | 1 | 1 |
| skills/deep-research/RESEARCH_CREATE_TOC.md | 55 | 637 | 3 | 5 | 10 | 1 | 2 |
| skills/deep-research/RESEARCH_STRATEGY_MCPI.md | 231 | 2649 | 12 | 5 | 14 | 8 | 2 |
| skills/deep-research/RESEARCH_STRATEGY_MEPI.md | 202 | 2109 | 8 | 4 | 12 | 7 | 2 |
| skills/deep-research/RESEARCH_TOC_TEMPLATE.md | 88 | 885 | 3 | 0 | 0 | 0 | 2 |
| skills/deep-research/RESEARCH_TOOLS.md | 334 | 2694 | 14 | 4 | 4 | 12 | 2 |
| skills/deep-research/SKILL.md | 200 | 2177 | 26 | 6 | 7 | 5 | 3 |

### 2.4 Skills - EDIRD Phase Planning

| Path | Lines | Tokens | Concepts | Rules | Steps | Branching | Load Freq |
|------|------:|-------:|---------:|------:|------:|----------:|----------:|
| skills/edird-phase-planning/SKILL.md | 195 | 1759 | 15 | 5 | 5 | 10 | 3 |

### 2.5 Skills - Git

| Path | Lines | Tokens | Concepts | Rules | Steps | Branching | Load Freq |
|------|------:|-------:|---------:|------:|------:|----------:|----------:|
| skills/git/SETUP.md | 113 | 532 | 2 | 0 | 7 | 3 | 1 |
| skills/git/SKILL.md | 313 | 1651 | 10 | 0 | 5 | 4 | 2 |
| skills/git-conventions/SKILL.md | 157 | 960 | 10 | 2 | 0 | 3 | 4 |

### 2.6 Skills - GitHub

| Path | Lines | Tokens | Concepts | Rules | Steps | Branching | Load Freq |
|------|------:|-------:|---------:|------:|------:|----------:|----------:|
| skills/github/SETUP.md | 69 | 506 | 2 | 0 | 4 | 2 | 1 |
| skills/github/SKILL.md | 188 | 1185 | 6 | 0 | 0 | 1 | 1 |

### 2.7 Skills - Google Account

| Path | Lines | Tokens | Concepts | Rules | Steps | Branching | Load Freq |
|------|------:|-------:|---------:|------:|------:|----------:|----------:|
| skills/google-account/SETUP.md | 456 | 3079 | 8 | 0 | 10 | 7 | 1 |
| skills/google-account/SKILL.md | 391 | 3395 | 12 | 5 | 6 | 6 | 1 |
| skills/google-account/UNINSTALL.md | 307 | 2680 | 2 | 0 | 4 | 5 | 1 |

### 2.8 Skills - LLM Computer Use

| Path | Lines | Tokens | Concepts | Rules | Steps | Branching | Load Freq |
|------|------:|-------:|---------:|------:|------:|----------:|----------:|
| skills/llm-computer-use/SKILL.md | 82 | 621 | 5 | 0 | 0 | 2 | 1 |

### 2.9 Skills - LLM Evaluation

| Path | Lines | Tokens | Concepts | Rules | Steps | Branching | Load Freq |
|------|------:|-------:|---------:|------:|------:|----------:|----------:|
| skills/llm-evaluation/LLM_EVALUATION_CLAUDE_MODELS.md | 43 | 652 | 3 | 0 | 3 | 0 | 1 |
| skills/llm-evaluation/LLM_EVALUATION_SCRIPTS.md | 241 | 2575 | 15 | 0 | 0 | 2 | 2 |
| skills/llm-evaluation/LLM_EVALUATION_TESTED_MODELS.md | 60 | 717 | 3 | 0 | 0 | 0 | 1 |
| skills/llm-evaluation/pricing-sources/2026-02-07_Anthropic-ModelPricing.md | 895 | 10175 | 2 | 0 | 0 | 0 | 1 |
| skills/llm-evaluation/pricing-sources/2026-02-07_OpenAI-ModelPricing-Standard.md | 848 | 13662 | 2 | 0 | 0 | 0 | 1 |
| skills/llm-evaluation/pricing-sources/2026-03-10_Anthropic-ModelPricing.md | 34 | 541 | 0 | 0 | 0 | 0 | 1 |
| skills/llm-evaluation/pricing-sources/2026-03-10_OpenAI-ModelPricing-Standard.md | 37 | 559 | 0 | 0 | 0 | 0 | 1 |
| skills/llm-evaluation/pricing-sources/2026-03-10_PricingChanges.md | 85 | 1534 | 1 | 0 | 0 | 0 | 1 |
| skills/llm-evaluation/pricing-sources/2026-03-20_Anthropic-ModelPricing.md | 301 | 3410 | 8 | 0 | 0 | 0 | 1 |
| skills/llm-evaluation/prompts/answer-from-text.md | 15 | 72 | 1 | 3 | 0 | 1 | 1 |
| skills/llm-evaluation/prompts/compare-image-transcription.md | 64 | 450 | 4 | 0 | 0 | 0 | 1 |
| skills/llm-evaluation/prompts/judge-answer.md | 24 | 168 | 1 | 6 | 0 | 0 | 1 |
| skills/llm-evaluation/prompts/summarize-text.md | 17 | 85 | 1 | 4 | 0 | 0 | 1 |
| skills/llm-evaluation/prompts/transcribe-page.md | 16 | 85 | 1 | 4 | 0 | 0 | 1 |
| skills/llm-evaluation/SETUP.md | 214 | 1569 | 2 | 0 | 10 | 4 | 1 |
| skills/llm-evaluation/SKILL.md | 60 | 560 | 8 | 0 | 5 | 2 | 2 |
| skills/llm-evaluation/UNINSTALL.md | 151 | 1433 | 1 | 0 | 2 | 3 | 1 |
| skills/llm-evaluation/UPDATE_MODEL_PRICING.md | 271 | 2784 | 5 | 3 | 4 | 2 | 1 |
| skills/llm-evaluation/UPDATE_MODEL_REGISTRY.md | 324 | 3439 | 5 | 3 | 4 | 3 | 1 |

### 2.10 Skills - LLM Transcription

| Path | Lines | Tokens | Concepts | Rules | Steps | Branching | Load Freq |
|------|------:|-------:|---------:|------:|------:|----------:|----------:|
| skills/llm-transcription/prompts/judge.md | 127 | 1126 | 6 | 3 | 0 | 5 | 1 |
| skills/llm-transcription/prompts/transcription.md | 220 | 1872 | 10 | 8 | 4 | 4 | 1 |
| skills/llm-transcription/SETUP.md | 73 | 372 | 1 | 0 | 3 | 2 | 1 |
| skills/llm-transcription/SKILL.md | 89 | 822 | 5 | 0 | 2 | 2 | 3 |
| skills/llm-transcription/UNINSTALL.md | 170 | 1844 | 1 | 0 | 3 | 4 | 1 |

### 2.11 Skills - Browser Automation

| Path | Lines | Tokens | Concepts | Rules | Steps | Branching | Load Freq |
|------|------:|-------:|---------:|------:|------:|----------:|----------:|
| skills/ms-playwright-mcp/PLAYWRIGHT_ADVANCED_WORKFLOWS.md | 188 | 1732 | 5 | 0 | 5 | 4 | 3 |
| skills/ms-playwright-mcp/PLAYWRIGHT_AUTHENTICATION.md | 46 | 249 | 3 | 0 | 3 | 1 | 1 |
| skills/ms-playwright-mcp/PLAYWRIGHT_FULL_PAGE_SCREENSHOT.md | 89 | 634 | 2 | 0 | 4 | 2 | 2 |
| skills/ms-playwright-mcp/PLAYWRIGHT_TROUBLESHOOTING.md | 51 | 315 | 4 | 0 | 0 | 5 | 2 |
| skills/ms-playwright-mcp/SETUP.md | 404 | 3240 | 5 | 0 | 9 | 8 | 1 |
| skills/ms-playwright-mcp/SKILL.md | 185 | 1916 | 16 | 3 | 3 | 4 | 5 |
| skills/ms-playwright-mcp/UNINSTALL.md | 255 | 2565 | 1 | 0 | 4 | 5 | 1 |
| skills/playwriter-mcp/SETUP.md | 300 | 2135 | 4 | 0 | 8 | 5 | 1 |
| skills/playwriter-mcp/SKILL.md | 265 | 2016 | 12 | 5 | 0 | 4 | 2 |
| skills/playwriter-mcp/UNINSTALL.md | 114 | 773 | 1 | 0 | 5 | 1 | 1 |

### 2.12 Skills - PDF Tools

| Path | Lines | Tokens | Concepts | Rules | Steps | Branching | Load Freq |
|------|------:|-------:|---------:|------:|------:|----------:|----------:|
| skills/pdf-tools/SETUP.md | 212 | 1880 | 6 | 0 | 10 | 5 | 1 |
| skills/pdf-tools/SKILL.md | 295 | 2810 | 14 | 5 | 0 | 4 | 3 |

### 2.13 Skills - Session Management

| Path | Lines | Tokens | Concepts | Rules | Steps | Branching | Load Freq |
|------|------:|-------:|---------:|------:|------:|----------:|----------:|
| skills/session-management/NOTES_TEMPLATE.md | 71 | 608 | 6 | 2 | 0 | 1 | 8 |
| skills/session-management/PROBLEMS_TEMPLATE.md | 68 | 736 | 5 | 1 | 0 | 1 | 8 |
| skills/session-management/PROGRESS_TEMPLATE.md | 51 | 428 | 4 | 0 | 0 | 0 | 8 |
| skills/session-management/SKILL.md | 134 | 1148 | 12 | 3 | 7 | 3 | 8 |

### 2.14 Skills - Travel Info

| Path | Lines | Tokens | Concepts | Rules | Steps | Branching | Load Freq |
|------|------:|-------:|---------:|------:|------:|----------:|----------:|
| skills/travel-info/AT.md | 17 | 179 | 0 | 0 | 0 | 0 | 1 |
| skills/travel-info/BE.md | 16 | 168 | 0 | 0 | 0 | 0 | 1 |
| skills/travel-info/CH.md | 18 | 191 | 0 | 0 | 0 | 0 | 1 |
| skills/travel-info/DE.md | 22 | 237 | 0 | 0 | 0 | 0 | 1 |
| skills/travel-info/ES.md | 18 | 192 | 0 | 0 | 0 | 0 | 1 |
| skills/travel-info/EUROPE.md | 20 | 258 | 0 | 0 | 0 | 0 | 1 |
| skills/travel-info/FLIGHTS.md | 17 | 201 | 0 | 0 | 0 | 0 | 1 |
| skills/travel-info/FR.md | 19 | 189 | 0 | 0 | 0 | 0 | 1 |
| skills/travel-info/IT.md | 20 | 250 | 0 | 0 | 0 | 0 | 1 |
| skills/travel-info/NL.md | 17 | 159 | 0 | 0 | 0 | 0 | 1 |
| skills/travel-info/SKILL.md | 35 | 298 | 1 | 0 | 3 | 2 | 1 |
| skills/travel-info/TRAINS.md | 25 | 255 | 0 | 0 | 0 | 0 | 1 |
| skills/travel-info/TRANSIT.md | 24 | 237 | 0 | 0 | 0 | 0 | 1 |
| skills/travel-info/UK.md | 24 | 247 | 0 | 0 | 0 | 0 | 1 |

### 2.15 Skills - Windows Desktop Control

| Path | Lines | Tokens | Concepts | Rules | Steps | Branching | Load Freq |
|------|------:|-------:|---------:|------:|------:|----------:|----------:|
| skills/windows-desktop-control/SKILL.md | 42 | 319 | 2 | 0 | 0 | 1 | 2 |

### 2.16 Skills - Windsurf Auto Model Switcher

| Path | Lines | Tokens | Concepts | Rules | Steps | Branching | Load Freq |
|------|------:|-------:|---------:|------:|------:|----------:|----------:|
| skills/windsurf-auto-model-switcher/SETUP.md | 83 | 580 | 2 | 0 | 2 | 2 | 1 |
| skills/windsurf-auto-model-switcher/SKILL.md | 70 | 488 | 4 | 0 | 0 | 2 | 2 |
| skills/windsurf-auto-model-switcher/UNINSTALL.md | 63 | 475 | 1 | 0 | 2 | 1 | 1 |
| skills/windsurf-auto-model-switcher/update-model-registry/README.md | 37 | 253 | 1 | 0 | 0 | 2 | 1 |
| skills/windsurf-auto-model-switcher/update-model-registry/UPDATE_WINDSURF_MODEL_REGISTRY.md | 82 | 547 | 2 | 0 | 5 | 3 | 1 |

### 2.17 Skills - Write Documents

| Path | Lines | Tokens | Concepts | Rules | Steps | Branching | Load Freq |
|------|------:|-------:|---------:|------:|------:|----------:|----------:|
| skills/write-documents/APAPALAN_RULES.md | 776 | 6085 | 24 | 24 | 0 | 6 | 12 |
| skills/write-documents/CONVERSATION_RULES.md | 345 | 2254 | 3 | 18 | 0 | 2 | 1 |
| skills/write-documents/CONVERSATION_TEMPLATE.md | 112 | 1088 | 2 | 14 | 0 | 0 | 1 |
| skills/write-documents/FAILS_TEMPLATE.md | 85 | 601 | 5 | 4 | 0 | 2 | 4 |
| skills/write-documents/FIXES_TEMPLATE.md | 85 | 434 | 2 | 0 | 5 | 0 | 2 |
| skills/write-documents/IMPL_TEMPLATE.md | 127 | 953 | 5 | 0 | 0 | 1 | 4 |
| skills/write-documents/INFO_TEMPLATE.md | 57 | 419 | 2 | 0 | 0 | 0 | 4 |
| skills/write-documents/LEARNINGS_TEMPLATE.md | 89 | 724 | 5 | 2 | 0 | 2 | 2 |
| skills/write-documents/MECT_WRITING_RULES.md | 489 | 3851 | 17 | 17 | 0 | 3 | 6 |
| skills/write-documents/REVIEW_TEMPLATE.md | 98 | 589 | 3 | 0 | 0 | 0 | 3 |
| skills/write-documents/SKILL.md | 128 | 1748 | 12 | 2 | 7 | 3 | 18 |
| skills/write-documents/SPEC_RULES.md | 397 | 3050 | 3 | 12 | 0 | 2 | 4 |
| skills/write-documents/SPEC_TEMPLATE.md | 169 | 1077 | 5 | 0 | 0 | 1 | 4 |
| skills/write-documents/STRUT_TEMPLATE.md | 237 | 2499 | 18 | 5 | 0 | 3 | 4 |
| skills/write-documents/TASKS_TEMPLATE.md | 183 | 1178 | 5 | 2 | 0 | 1 | 3 |
| skills/write-documents/TEST_TEMPLATE.md | 134 | 853 | 3 | 0 | 0 | 0 | 3 |
| skills/write-documents/WORKFLOW_RULES.md | 462 | 2432 | 3 | 18 | 0 | 4 | 3 |
| skills/write-documents/WORKFLOW_TEMPLATE.md | 140 | 753 | 3 | 0 | 0 | 2 | 2 |

### 2.18 Skills - YouTube Downloader

| Path | Lines | Tokens | Concepts | Rules | Steps | Branching | Load Freq |
|------|------:|-------:|---------:|------:|------:|----------:|----------:|
| skills/youtube-downloader/SKILL.md | 86 | 807 | 4 | 0 | 0 | 2 | 1 |

### 2.19 Workflows

| Path | Lines | Tokens | Concepts | Rules | Steps | Branching | Load Freq |
|------|------:|-------:|---------:|------:|------:|----------:|----------:|
| workflows/bugfix.md | 278 | 2319 | 8 | 3 | 11 | 12 | 2 |
| workflows/build.md | 41 | 257 | 1 | 4 | 5 | 1 | 3 |
| workflows/commit.md | 31 | 169 | 0 | 0 | 5 | 1 | 5 |
| workflows/continue.md | 128 | 837 | 2 | 1 | 5 | 8 | 6 |
| workflows/critique.md | 336 | 2867 | 6 | 5 | 10 | 8 | 3 |
| workflows/deep-research.md | 16 | 111 | 0 | 0 | 2 | 0 | 1 |
| workflows/fail.md | 166 | 1152 | 2 | 0 | 9 | 7 | 3 |
| workflows/fix.md | 68 | 487 | 1 | 0 | 3 | 6 | 1 |
| workflows/go.md | 95 | 577 | 1 | 4 | 5 | 6 | 4 |
| workflows/implement.md | 116 | 756 |