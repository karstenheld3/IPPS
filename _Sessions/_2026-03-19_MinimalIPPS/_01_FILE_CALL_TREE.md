# File Call Tree: DevSystem

**Doc ID**: DSYS-IN01
**Goal**: Map every file loading relationship in the DevSystem for dependency analysis

## Table of Contents

1. [Startup Sequence](#1-startup-sequence)
2. [Workflow Call Trees](#2-workflow-call-trees)
3. [Skill Call Trees](#3-skill-call-trees)
4. [File Reference List (Reverse Index)](#4-file-reference-list-reverse-index)

## 1. Startup Sequence

Files loaded automatically at agent initialization, in order. All files with `trigger: always_on` frontmatter load first, followed by the implicit always-available rule files.

### 1.1 Always-On Rules (loaded first)

```
rules/agent-behavior.md           (trigger: always_on)
rules/core-conventions.md         (trigger: always_on)
rules/devsystem-core.md           (trigger: always_on)
rules/devsystem-ids.md            (trigger: always_on)
rules/tools-and-skills.md         (trigger: always_on)
rules/workspace-rules.md          (trigger: always_on, empty)
```

### 1.2 Implicit Always-Available Rules (no trigger, but referenced by always-on rules)

```
rules/agentic-english.md          (vocabulary referenced by devsystem-core.md)
rules/edird-phase-planning.md     (phase model referenced by devsystem-core.md)
```

### 1.3 Startup Load Order

```
1. rules/agent-behavior.md
2. rules/agentic-english.md
3. rules/core-conventions.md
4. rules/devsystem-core.md
   ├── references: rules/agentic-english.md (AGEN vocabulary)
   ├── references: rules/edird-phase-planning.md (phase model)
   └── references: all workflow commands (by name, not loaded)
5. rules/devsystem-ids.md
6. rules/edird-phase-planning.md
   └── references: skills/edird-phase-planning/SKILL.md (on-demand)
7. rules/tools-and-skills.md
8. rules/workspace-rules.md
```

## 2. Workflow Call Trees

Each workflow shows direct skill invocations (`@skills:`), direct file reads, and workflow cross-references (`/command`). Recursive skill expansion shown on first occurrence only.

### 2.1 workflows/bugfix.md

```
workflows/bugfix.md
├── @write-documents → skills/write-documents/SKILL.md
│   ├── skills/write-documents/APAPALAN_RULES.md
│   ├── skills/write-documents/MECT_WRITING_RULES.md
│   ├── skills/write-documents/INFO_TEMPLATE.md
│   ├── skills/write-documents/STRUT_TEMPLATE.md
│   └── skills/write-documents/FIXES_TEMPLATE.md
├── @coding-conventions → skills/coding-conventions/SKILL.md
│   ├── skills/coding-conventions/MECT_CODING_RULES.md
│   ├── skills/coding-conventions/PYTHON-RULES.md
│   ├── skills/coding-conventions/JSON-RULES.md
│   ├── skills/coding-conventions/WORKFLOW-RULES.md
│   ├── skills/coding-conventions/AGENT-SKILL-RULES.md
│   ├── skills/coding-conventions/LOGGING-RULES.md
│   ├── skills/coding-conventions/LOGGING-RULES-APP-LEVEL.md
│   ├── skills/coding-conventions/LOGGING-RULES-SCRIPT-LEVEL.md
│   └── skills/coding-conventions/LOGGING-RULES-USER-FACING.md
├── @session-management → skills/session-management/SKILL.md
│   ├── skills/session-management/NOTES_TEMPLATE.md
│   ├── skills/session-management/PROBLEMS_TEMPLATE.md
│   └── skills/session-management/PROGRESS_TEMPLATE.md
├── /write-info → workflows/write-info.md
├── /write-strut → workflows/write-strut.md
├── /write-tasks-plan → workflows/write-tasks-plan.md
├── /write-test-plan → workflows/write-test-plan.md
├── /implement → workflows/implement.md
├── /commit → workflows/commit.md
├── /learn → workflows/learn.md
└── /session-new → workflows/session-new.md
```

### 2.2 workflows/build.md

```
workflows/build.md
├── @edird-phase-planning → skills/edird-phase-planning/SKILL.md
│   └── rules/edird-phase-planning.md (full model)
├── @session-management → skills/session-management/SKILL.md
│   └── (templates, see 2.1)
├── @write-documents → skills/write-documents/SKILL.md
│   └── (templates + rules, see 2.1)
├── /session-new → workflows/session-new.md
└── /session-finalize → workflows/session-finalize.md
```

### 2.3 workflows/commit.md

```
workflows/commit.md
└── @git-conventions → skills/git-conventions/SKILL.md
```

### 2.4 workflows/continue.md

```
workflows/continue.md
├── /session-load → workflows/session-load.md
├── /session-archive → workflows/session-archive.md
├── /session-finalize → workflows/session-finalize.md
├── /go → workflows/go.md
└── /recap → workflows/recap.md
```

### 2.5 workflows/critique.md

```
workflows/critique.md
├── @write-documents → skills/write-documents/SKILL.md
│   ├── skills/write-documents/REVIEW_TEMPLATE.md
│   └── skills/write-documents/FAILS_TEMPLATE.md
└── /verify → workflows/verify.md (mentioned)
```

### 2.6 workflows/deep-research.md

```
workflows/deep-research.md
└── @skills:deep-research → skills/deep-research/SKILL.md
    ├── skills/deep-research/RESEARCH_STRATEGY_MCPI.md
    │   ├── skills/deep-research/RESEARCH_CREATE_TOC.md
    │   │   └── skills/deep-research/RESEARCH_TOC_TEMPLATE.md
    │   ├── skills/deep-research/RESEARCH_TOOLS.md
    │   │   ├── @skills:pdf-tools → skills/pdf-tools/SKILL.md
    │   │   ├── @skills:llm-transcription → skills/llm-transcription/SKILL.md
    │   │   └── @skills:ms-playwright-mcp → skills/ms-playwright-mcp/SKILL.md
    │   ├── /write-strut → workflows/write-strut.md
    │   ├── /verify → workflows/verify.md
    │   ├── /critique → workflows/critique.md
    │   ├── /reconcile → workflows/reconcile.md
    │   ├── /implement → workflows/implement.md
    │   └── /write-tasks-plan → workflows/write-tasks-plan.md
    ├── skills/deep-research/RESEARCH_STRATEGY_MEPI.md
    │   ├── skills/deep-research/RESEARCH_CREATE_TOC.md
    │   ├── /write-strut → workflows/write-strut.md
    │   ├── /verify → workflows/verify.md
    │   ├── /critique → workflows/critique.md
    │   ├── /reconcile → workflows/reconcile.md
    │   └── /write-tasks-plan → workflows/write-tasks-plan.md
    ├── skills/deep-research/RESEARCH_TOOLS.md
    ├── skills/deep-research/RESEARCH_TOC_TEMPLATE.md
    ├── skills/deep-research/RESEARCH_CREATE_TOC.md
    ├── skills/deep-research/DOMAIN_DEFAULT.md
    │   ├── @skills:pdf-tools → skills/pdf-tools/SKILL.md
    │   ├── @skills:llm-transcription → skills/llm-transcription/SKILL.md
    │   ├── /verify → workflows/verify.md
    │   ├── /critique → workflows/critique.md
    │   └── /reconcile → workflows/reconcile.md
    ├── skills/deep-research/DOMAIN_SOFTWARE.md
    ├── skills/deep-research/DOMAIN_MARKET_INTEL.md
    ├── skills/deep-research/DOMAIN_DOCUMENT_INTEL.md
    └── skills/deep-research/DOMAIN_LEGAL.md
```

### 2.7 workflows/fail.md

```
workflows/fail.md
├── @write-documents → skills/write-documents/SKILL.md
│   └── skills/write-documents/FAILS_TEMPLATE.md
└── /learn → workflows/learn.md (suggested post-fix)
```

### 2.8 workflows/fix.md

```
workflows/fix.md
├── (always reads) rules/devsystem-core.md
├── (always reads) rules/agent-behavior.md
├── (CODE context)
│   ├── workflows/bugfix.md
│   ├── workflows/implement.md
│   └── skills/coding-conventions/SKILL.md
├── (DOCUMENT context)
│   ├── workflows/improve.md
│   ├── workflows/verify.md
│   └── skills/write-documents/SKILL.md
├── (DESIGN context)
│   ├── workflows/critique.md
│   ├── workflows/reconcile.md
│   └── rules/edird-phase-planning.md
├── (UNDERSTANDING context)
│   ├── workflows/research.md
│   ├── workflows/deep-research.md
│   └── skills/deep-research/SKILL.md
└── (PROCESS context)
    ├── workflows/write-spec.md
    └── workflows/write-impl-plan.md
```

### 2.9 workflows/go.md

```
workflows/go.md
├── (reads) rules/devsystem-core.md
├── /recap → workflows/recap.md
├── /continue → workflows/continue.md
├── /verify → workflows/verify.md
├── /write-info → workflows/write-info.md
├── /critique → workflows/critique.md
├── /reconcile → workflows/reconcile.md
├── /write-tasks-plan → workflows/write-tasks-plan.md
└── /implement → workflows/implement.md
```

### 2.10 workflows/implement.md

```
workflows/implement.md
├── @coding-conventions → skills/coding-conventions/SKILL.md
├── @write-documents → skills/write-documents/SKILL.md
├── /write-spec → workflows/write-spec.md
├── /write-impl-plan → workflows/write-impl-plan.md
├── /write-test-plan → workflows/write-test-plan.md
└── /verify → workflows/verify.md
```

### 2.11 workflows/improve.md

```
workflows/improve.md
├── (reads) skills/write-documents/APAPALAN_RULES.md
├── (reads) skills/write-documents/MECT_WRITING_RULES.md
└── (reads) skills/coding-conventions/MECT_CODING_RULES.md
```

### 2.12 workflows/learn.md

```
workflows/learn.md
├── @write-documents → skills/write-documents/SKILL.md
│   └── skills/write-documents/LEARNINGS_TEMPLATE.md
└── /fail → workflows/fail.md
```

### 2.13 workflows/partition.md

```
workflows/partition.md
└── @write-documents → skills/write-documents/SKILL.md
```

### 2.14 workflows/prime.md

```
workflows/prime.md
├── (dynamic) [AGENT_FOLDER]/rules/*.md (all rule files)
├── (dynamic) [WORKSPACE_FOLDER]/!*.md (priority files)
└── (dynamic) [WORKSPACE_FOLDER]/*.md (standard files, excluding _*)
```

### 2.15 workflows/project-release.md

```
workflows/project-release.md
└── (uses) skills/github/SKILL.md (gh CLI, implicit)
```

### 2.16 workflows/recap.md

```
workflows/recap.md
└── (reads tracking documents: NOTES.md, PROBLEMS.md, PROGRESS.md, FAILS.md,
     LEARNINGS.md, _SPEC_*.md, _IMPL_*.md, _TEST_*.md, _TASKS_*.md)
```

### 2.17 workflows/reconcile.md

```
workflows/reconcile.md
├── @write-documents → skills/write-documents/SKILL.md
│   ├── skills/write-documents/FAILS_TEMPLATE.md
│   └── skills/write-documents/REVIEW_TEMPLATE.md
├── @coding-conventions → skills/coding-conventions/SKILL.md
└── /implement → workflows/implement.md (when in implementation mode)
```

### 2.18 workflows/rename.md

```
workflows/rename.md
└── (no skill or workflow references)
```

### 2.19 workflows/research.md

```
workflows/research.md
├── @write-documents → skills/write-documents/SKILL.md
└── (reads) skills/write-documents/APAPALAN_RULES.md
```

### 2.20 workflows/session-archive.md

```
workflows/session-archive.md
└── @session-management → skills/session-management/SKILL.md
```

### 2.21 workflows/session-finalize.md

```
workflows/session-finalize.md
├── @session-management → skills/session-management/SKILL.md
├── @git-conventions → skills/git-conventions/SKILL.md
└── /session-archive → workflows/session-archive.md (suggested)
```

### 2.22 workflows/session-load.md

```
workflows/session-load.md
├── @session-management → skills/session-management/SKILL.md
└── /prime → workflows/prime.md
```

### 2.23 workflows/session-new.md

```
workflows/session-new.md
└── @session-management → skills/session-management/SKILL.md
```

### 2.24 workflows/session-save.md

```
workflows/session-save.md
├── @session-management → skills/session-management/SKILL.md
├── @git-conventions → skills/git-conventions/SKILL.md
└── (invokes) workflows/commit.md
```

### 2.25 workflows/solve.md

```
workflows/solve.md
├── @edird-phase-planning → skills/edird-phase-planning/SKILL.md
├── @session-management → skills/session-management/SKILL.md
├── @write-documents → skills/write-documents/SKILL.md
├── /session-new → workflows/session-new.md
└── /session-finalize → workflows/session-finalize.md
```

### 2.26 workflows/switch-model.md

```
workflows/switch-model.md
└── @skills:windsurf-auto-model-switcher → skills/windsurf-auto-model-switcher/SKILL.md
    ├── skills/windsurf-auto-model-switcher/SETUP.md
    ├── skills/windsurf-auto-model-switcher/UNINSTALL.md
    └── skills/windsurf-auto-model-switcher/update-model-registry/UPDATE_WINDSURF_MODEL_REGISTRY.md
```

### 2.27 workflows/sync.md

```
workflows/sync.md
├── @write-documents → skills/write-documents/SKILL.md
└── @coding-conventions → skills/coding-conventions/SKILL.md
```

### 2.28 workflows/test.md

```
workflows/test.md
├── @ms-playwright-mcp → skills/ms-playwright-mcp/SKILL.md
│   ├── skills/ms-playwright-mcp/PLAYWRIGHT_ADVANCED_WORKFLOWS.md
│   ├── skills/ms-playwright-mcp/PLAYWRIGHT_AUTHENTICATION.md
│   ├── skills/ms-playwright-mcp/PLAYWRIGHT_FULL_PAGE_SCREENSHOT.md
│   ├── skills/ms-playwright-mcp/PLAYWRIGHT_TROUBLESHOOTING.md
│   └── skills/ms-playwright-mcp/SETUP.md
├── @write-documents → skills/write-documents/SKILL.md
└── @coding-conventions → skills/coding-conventions/SKILL.md
```

### 2.29 workflows/transcribe.md

```
workflows/transcribe.md
├── @pdf-tools → skills/pdf-tools/SKILL.md
│   └── skills/pdf-tools/SETUP.md
├── @ms-playwright-mcp → skills/ms-playwright-mcp/SKILL.md
├── @llm-transcription → skills/llm-transcription/SKILL.md
│   ├── skills/llm-transcription/SETUP.md
│   ├── skills/llm-transcription/prompts/judge.md
│   └── skills/llm-transcription/prompts/transcription.md
└── /verify → workflows/verify.md
```

### 2.30 workflows/verify.md

```
workflows/verify.md
├── @write-documents → skills/write-documents/SKILL.md
├── @coding-conventions → skills/coding-conventions/SKILL.md
├── (INFO context)
│   ├── workflows/research.md
│   ├── skills/write-documents/APAPALAN_RULES.md
│   └── skills/write-documents/MECT_WRITING_RULES.md
├── (SPEC context)
│   ├── skills/write-documents/SPEC_RULES.md
│   ├── skills/write-documents/APAPALAN_RULES.md
│   └── skills/write-documents/MECT_WRITING_RULES.md
├── (IMPL context)
│   ├── skills/write-documents/APAPALAN_RULES.md
│   └── skills/write-documents/MECT_WRITING_RULES.md
├── (Code context)
│   ├── skills/coding-conventions/MECT_CODING_RULES.md
│   ├── skills/coding-conventions/LOGGING-RULES.md
│   ├── skills/coding-conventions/LOGGING-RULES-USER-FACING.md
│   ├── skills/coding-conventions/LOGGING-RULES-APP-LEVEL.md
│   └── skills/coding-conventions/LOGGING-RULES-SCRIPT-LEVEL.md
├── (TEST context)
│   ├── skills/write-documents/APAPALAN_RULES.md
│   └── skills/write-documents/MECT_WRITING_RULES.md
├── (Workflow context)
│   ├── skills/coding-conventions/WORKFLOW-RULES.md
│   ├── skills/write-documents/APAPALAN_RULES.md
│   └── skills/write-documents/MECT_WRITING_RULES.md
├── (Skill context)
│   └── skills/coding-conventions/AGENT-SKILL-RULES.md
└── (STRUT context)
    └── (inline checks, no additional files)
```

### 2.31 workflows/write-impl-plan.md

```
workflows/write-impl-plan.md
├── @write-documents → skills/write-documents/SKILL.md
│   └── skills/write-documents/IMPL_TEMPLATE.md
└── /verify → workflows/verify.md
```

### 2.32 workflows/write-info.md

```
workflows/write-info.md
├── @write-documents → skills/write-documents/SKILL.md
│   └── skills/write-documents/INFO_TEMPLATE.md
└── /verify → workflows/verify.md
```

### 2.33 workflows/write-spec.md

```
workflows/write-spec.md
├── @write-documents → skills/write-documents/SKILL.md
│   ├── skills/write-documents/SPEC_TEMPLATE.md
│   └── skills/write-documents/SPEC_RULES.md
└── /verify → workflows/verify.md
```

### 2.34 workflows/write-strut.md

```
workflows/write-strut.md
├── @write-documents → skills/write-documents/SKILL.md
│   └── skills/write-documents/STRUT_TEMPLATE.md
└── /verify → workflows/verify.md
```

### 2.35 workflows/write-tasks-plan.md

```
workflows/write-tasks-plan.md
├── @write-documents → skills/write-documents/SKILL.md
│   └── skills/write-documents/TASKS_TEMPLATE.md
└── /partition → workflows/partition.md
```

### 2.36 workflows/write-test-plan.md

```
workflows/write-test-plan.md
├── @write-documents → skills/write-documents/SKILL.md
│   └── skills/write-documents/TEST_TEMPLATE.md
└── /verify → workflows/verify.md
```

## 3. Skill Call Trees

### 3.1 skills/write-documents/SKILL.md

```
skills/write-documents/SKILL.md
├── skills/write-documents/APAPALAN_RULES.md (mandatory pre-read)
├── skills/write-documents/MECT_WRITING_RULES.md (mandatory pre-read)
├── skills/write-documents/INFO_TEMPLATE.md ([WRITE-INFO])
├── skills/write-documents/SPEC_TEMPLATE.md ([WRITE-SPEC])
├── skills/write-documents/SPEC_RULES.md ([WRITE-SPEC])
├── skills/write-documents/IMPL_TEMPLATE.md ([WRITE-IMPL-PLAN])
├── skills/write-documents/TEST_TEMPLATE.md ([WRITE-TEST-PLAN])
├── skills/write-documents/FIXES_TEMPLATE.md ([WRITE-FIX])
├── skills/write-documents/FAILS_TEMPLATE.md ([WRITE-FAIL])
├── skills/write-documents/REVIEW_TEMPLATE.md ([WRITE-REVIEW])
├── skills/write-documents/TASKS_TEMPLATE.md ([WRITE-TASKS-PLAN])
├── skills/write-documents/STRUT_TEMPLATE.md ([WRITE-STRUT])
├── skills/write-documents/LEARNINGS_TEMPLATE.md (via /learn)
├── skills/write-documents/WORKFLOW_TEMPLATE.md (workflow authoring)
├── skills/write-documents/WORKFLOW_RULES.md (workflow authoring)
├── skills/write-documents/CONVERSATION_RULES.md (conversation docs)
└── skills/write-documents/CONVERSATION_TEMPLATE.md (conversation docs)
```

### 3.2 skills/coding-conventions/SKILL.md

```
skills/coding-conventions/SKILL.md
├── skills/coding-conventions/MECT_CODING_RULES.md (mandatory pre-read)
├── skills/coding-conventions/PYTHON-RULES.md (Python code)
├── skills/coding-conventions/JSON-RULES.md (JSON files)
├── skills/coding-conventions/WORKFLOW-RULES.md (workflow documents)
├── skills/coding-conventions/AGENT-SKILL-RULES.md (skill development)
├── skills/coding-conventions/LOGGING-RULES.md (logging code, read first)
├── skills/coding-conventions/LOGGING-RULES-APP-LEVEL.md (app logging)
├── skills/coding-conventions/LOGGING-RULES-SCRIPT-LEVEL.md (script logging)
└── skills/coding-conventions/LOGGING-RULES-USER-FACING.md (user logging)
```

### 3.3 skills/deep-research/SKILL.md

```
skills/deep-research/SKILL.md
├── skills/deep-research/RESEARCH_STRATEGY_MCPI.md
│   ├── skills/deep-research/RESEARCH_CREATE_TOC.md
│   │   └── skills/deep-research/RESEARCH_TOC_TEMPLATE.md
│   ├── /write-strut → workflows/write-strut.md
│   ├── /verify → workflows/verify.md
│   ├── /critique → workflows/critique.md
│   ├── /reconcile → workflows/reconcile.md
│   ├── /implement → workflows/implement.md
│   └── /write-tasks-plan → workflows/write-tasks-plan.md
├── skills/deep-research/RESEARCH_STRATEGY_MEPI.md
│   ├── skills/deep-research/RESEARCH_CREATE_TOC.md
│   ├── /write-strut → workflows/write-strut.md
│   ├── /verify → workflows/verify.md
│   ├── /critique → workflows/critique.md
│   ├── /reconcile → workflows/reconcile.md
│   └── /write-tasks-plan → workflows/write-tasks-plan.md
├── skills/deep-research/RESEARCH_TOOLS.md
│   ├── @skills:pdf-tools → skills/pdf-tools/SKILL.md
│   ├── @skills:llm-transcription → skills/llm-transcription/SKILL.md
│   └── @skills:ms-playwright-mcp → skills/ms-playwright-mcp/SKILL.md
├── skills/deep-research/RESEARCH_TOC_TEMPLATE.md
├── skills/deep-research/RESEARCH_CREATE_TOC.md
├── skills/deep-research/DOMAIN_DEFAULT.md
│   ├── @skills:pdf-tools → skills/pdf-tools/SKILL.md
│   └── @skills:llm-transcription → skills/llm-transcription/SKILL.md
├── skills/deep-research/DOMAIN_SOFTWARE.md
├── skills/deep-research/DOMAIN_MARKET_INTEL.md
├── skills/deep-research/DOMAIN_DOCUMENT_INTEL.md
└── skills/deep-research/DOMAIN_LEGAL.md
```

### 3.4 skills/edird-phase-planning/SKILL.md

```
skills/edird-phase-planning/SKILL.md
├── rules/edird-phase-planning.md (full model with gates)
├── /build → workflows/build.md
├── /solve → workflows/solve.md
├── /write-spec → workflows/write-spec.md
├── /write-impl-plan → workflows/write-impl-plan.md
├── /write-test-plan → workflows/write-test-plan.md
└── /write-tasks-plan → workflows/write-tasks-plan.md
```

### 3.5 skills/session-management/SKILL.md

```
skills/session-management/SKILL.md
├── skills/session-management/NOTES_TEMPLATE.md
├── skills/session-management/PROBLEMS_TEMPLATE.md
├── skills/session-management/PROGRESS_TEMPLATE.md
└── rules/devsystem-ids.md (ID system reference)
```

### 3.6 skills/ms-playwright-mcp/SKILL.md

```
skills/ms-playwright-mcp/SKILL.md
├── skills/ms-playwright-mcp/PLAYWRIGHT_ADVANCED_WORKFLOWS.md
├── skills/ms-playwright-mcp/PLAYWRIGHT_AUTHENTICATION.md
├── skills/ms-playwright-mcp/PLAYWRIGHT_FULL_PAGE_SCREENSHOT.md
├── skills/ms-playwright-mcp/PLAYWRIGHT_TROUBLESHOOTING.md
├── skills/ms-playwright-mcp/SETUP.md
└── skills/ms-playwright-mcp/UNINSTALL.md
```

### 3.7 skills/pdf-tools/SKILL.md

```
skills/pdf-tools/SKILL.md
└── skills/pdf-tools/SETUP.md
```

### 3.8 skills/llm-transcription/SKILL.md

```
skills/llm-transcription/SKILL.md
├── skills/llm-transcription/SETUP.md
├── skills/llm-transcription/UNINSTALL.md
├── skills/llm-transcription/prompts/judge.md
└── skills/llm-transcription/prompts/transcription.md
```

### 3.9 skills/llm-evaluation/SKILL.md

```
skills/llm-evaluation/SKILL.md
├── skills/llm-evaluation/SETUP.md
├── skills/llm-evaluation/UNINSTALL.md
├── skills/llm-evaluation/LLM_EVALUATION_SCRIPTS.md
├── skills/llm-evaluation/LLM_EVALUATION_CLAUDE_MODELS.md
├── skills/llm-evaluation/LLM_EVALUATION_TESTED_MODELS.md
├── skills/llm-evaluation/UPDATE_MODEL_PRICING.md
│   ├── @skills:ms-playwright-mcp (PLAYWRIGHT_ADVANCED_WORKFLOWS.md)
│   └── @skills:llm-transcription (transcription script)
├── skills/llm-evaluation/UPDATE_MODEL_REGISTRY.md
│   ├── @skills:ms-playwright-mcp (PLAYWRIGHT_ADVANCED_WORKFLOWS.md)
│   └── @skills:llm-transcription (transcription script)
├── skills/llm-evaluation/pricing-sources/2026-02-07_Anthropic-ModelPricing.md
├── skills/llm-evaluation/pricing-sources/2026-02-07_OpenAI-ModelPricing-Standard.md
├── skills/llm-evaluation/pricing-sources/2026-03-10_Anthropic-ModelPricing.md
├── skills/llm-evaluation/pricing-sources/2026-03-10_OpenAI-ModelPricing-Standard.md
├── skills/llm-evaluation/pricing-sources/2026-03-10_PricingChanges.md
├── skills/llm-evaluation/pricing-sources/2026-03-20_Anthropic-ModelPricing.md
├── skills/llm-evaluation/prompts/answer-from-text.md
├── skills/llm-evaluation/prompts/compare-image-transcription.md
├── skills/llm-evaluation/prompts/judge-answer.md
├── skills/llm-evaluation/prompts/summarize-text.md
└── skills/llm-evaluation/prompts/transcribe-page.md
```

### 3.10 skills/git/SKILL.md

```
skills/git/SKILL.md
└── skills/git/SETUP.md
```

### 3.11 skills/git-conventions/SKILL.md

```
skills/git-conventions/SKILL.md
└── (no sub-file references)
```

### 3.12 skills/github/SKILL.md

```
skills/github/SKILL.md
└── skills/github/SETUP.md
```

### 3.13 skills/google-account/SKILL.md

```
skills/google-account/SKILL.md
├── skills/google-account/SETUP.md
└── skills/google-account/UNINSTALL.md
```

### 3.14 skills/llm-computer-use/SKILL.md

```
skills/llm-computer-use/SKILL.md
└── (no sub-file references)
```

### 3.15 skills/playwriter-mcp/SKILL.md

```
skills/playwriter-mcp/SKILL.md
├── skills/playwriter-mcp/SETUP.md
└── skills/playwriter-mcp/UNINSTALL.md
```

### 3.16 skills/travel-info/SKILL.md

```
skills/travel-info/SKILL.md
├── skills/travel-info/EUROPE.md
├── skills/travel-info/FLIGHTS.md
├── skills/travel-info/TRAINS.md
├── skills/travel-info/TRANSIT.md
├── skills/travel-info/DE.md
├── skills/travel-info/FR.md
├── skills/travel-info/UK.md
├── skills/travel-info/AT.md
├── skills/travel-info/CH.md
├── skills/travel-info/IT.md
├── skills/travel-info/BE.md
├── skills/travel-info/NL.md
└── skills/travel-info/ES.md
```

### 3.17 skills/windows-desktop-control/SKILL.md

```
skills/windows-desktop-control/SKILL.md
└── (no sub-file references)
```

### 3.18 skills/windsurf-auto-model-switcher/SKILL.md

```
skills/windsurf-auto-model-switcher/SKILL.md
├── skills/windsurf-auto-model-switcher/SETUP.md
├── skills/windsurf-auto-model-switcher/UNINSTALL.md
└── skills/windsurf-auto-model-switcher/update-model-registry/UPDATE_WINDSURF_MODEL_REGISTRY.md
    └── skills/windsurf-auto-model-switcher/update-model-registry/README.md
        └── skills/windows-desktop-control/SKILL.md (simple-screenshot.ps1)
```

### 3.19 skills/youtube-downloader/SKILL.md

```
skills/youtube-downloader/SKILL.md
└── (no sub-file references)
```

## 4. File Reference List (Reverse Index)

Format: `[file_path]`: **N** references
- triggered by: [list]

### 4.1 Rules

**`rules/agent-behavior.md`**: **3** references
- triggered by: startup (always_on), workflows/fix.md, workflows/prime.md

**`rules/agentic-english.md`**: **2** references
- triggered by: startup (implicit), rules/devsystem-core.md

**`rules/core-conventions.md`**: **2** references
- triggered by: startup (always_on), workflows/prime.md

**`rules/devsystem-core.md`**: **5** references
- triggered by: startup (always_on), workflows/fix.md, workflows/go.md, workflows/prime.md, skills/session-management/SKILL.md

**`rules/devsystem-ids.md`**: **3** references
- triggered by: startup (always_on), workflows/prime.md, skills/session-management/SKILL.md

**`rules/edird-phase-planning.md`**: **4** references
- triggered by: startup (implicit), rules/devsystem-core.md, workflows/fix.md, skills/edird-phase-planning/SKILL.md

**`rules/tools-and-skills.md`**: **2** references
- triggered by: startup (always_on), workflows/prime.md

**`rules/workspace-rules.md`**: **2** references
- triggered by: startup (always_on), workflows/prime.md

### 4.2 Workflows

**`workflows/bugfix.md`**: **2** references
- triggered by: user (`/bugfix`), workflows/fix.md

**`workflows/build.md`**: **2** references
- triggered by: user (`/build`), skills/edird-phase-planning/SKILL.md

**`workflows/commit.md`**: **3** references
- triggered by: user (`/commit`), workflows/bugfix.md, workflows/session-save.md

**`workflows/continue.md`**: **2** references
- triggered by: user (`/continue`), workflows/go.