# ID Registry

Inventory of all IDs, acronyms, and named concepts in the DevSystem.

## Frameworks

- **AGEN** - Agentic English. Controlled vocabulary for agent-human communication
- **EDIRD** - Explore, Design, Implement, Refine, Deliver. 5-phase workflow model
- **STRUT** - Structured Thinking. Method for planning and tracking complex autonomous work
- **TRACT** - Traceability concept/goal. Ensuring development artifacts remain connected from ideation to maintenance
- **TRACTFUL** - TRACT implementation via documents. Traceable Requirements Artifacts and Coded Templates For Unified Lifecycle
- **TDID** - Tractful Document ID system (defined in TRACTFUL spec section 4)

## Core Identifiers

- **TOPIC** - 7-14 uppercase letters identifying a component (e.g., `CRAWLENG`, `AUTHSYST`). Grandfathered topics (pre-2026-06-16) may be 2-6 chars.
- **SUBTOPIC** - 7-14 uppercase letters identifying a subfolder scope within a session. Registered in session NOTES.md only, not here. Used in nested Doc IDs: `[TOPIC]-[SUBTOPIC]-[DOC][NN]`
- **TDID** - Tractful Document ID. Format: `[TOPIC]-[DOC][NN]` or nested: `[TOPIC]-[SUBTOPIC]-[DOC][NN]`
- **FEATURE_SLUG** - Kebab-case feature identifier (e.g., `user-authentication`)

## Document Type IDs

- **IN** - INFO document (research, analysis)
- **SP** - SPEC document (specifications)
- **IP** - IMPL document (implementation plan)
- **TP** - TEST document (test plan)
- **TK** - TASKS document (partitioned work items)
- **RV** - REVIEW document (review findings)
- **LN** - LEARNINGS document (retrospective analysis)

## Spec-Level Item IDs

Used in SPEC documents. Format: `[TOPIC]-[TYPE]-[NN]`

- **FR** - Functional Requirement
- **DD** - Design Decision
- **IG** - Implementation Guarantee
- **NFR** - Non-Functional Requirement
- **AC** - Acceptance Criterion

## Plan-Level Item IDs

Used in IMPL/TEST documents. Format: `[TOPIC]-[DOC][NN]-[TYPE]-[NN]`

- **EC** - Edge Case
- **IS** - Implementation Step
- **TC** - Test Case
- **VC** - Verification Checklist item

## Tracking Item IDs

Used in PROBLEMS.md, FAILS.md, REVIEW.md. Format: `[TOPIC]-[TYPE]-[NNNN]`

- **BG** - Bug (defect in existing code)
- **FT** - Feature (new functionality request)
- **PR** - Problem (issue discovered during session)
- **FX** - Fix (documented fix for a problem)
- **TK** - Task (general work item)
- **RV** - Review finding
- **FL** - Failure log entry
- **LN** - Learning entry

## Source IDs (INFO documents)

Format: `[TOPIC]-[DOC]-SC-[SOURCE_ID]-[SOURCE_REF]`

- **SC** - Source marker

## Agentic concepts and strategies

- **PREN** - "Proper english" - precise natural language avoiding confusion, ambiguities, term conflicts 
- **AGEN** - "Agentic english" - proper english, enriched with semantics like `@mentions`, `/workflow`, `[INSTRUCTION]`, etc.
- **HWT** - Human Work Time. Example: "max 0.5h HWT per task"
- **AWT** - Agentic Work Time. Agent time estimate. Example: "complete in < 5mins AWT"
- **MEPI** - Most Executable Point of Information (used for research and decision making)
- **MCPI** - Most Complete Point of Information (used for research)
- **SOCAS** - Signs Of Confusion And Sloppiness (15 criteria)
- **MNF** - Must Not Forget. Technique for critical item tracking during task execution
- **APAPALAN** - As Precise As Possible, As Little As Necessary. Conciseness principle for workflows and documents
- **VCRIV** - Verify, Critique, Reconcile, Implement, Verify. Quality pipeline for logic and design review. Runs `/verify` → `/critique` → `/reconcile` → `/implement` → `/verify`
- **FACRIV** - Fact-check, Reconcile, Implement, Verify. Quality pipeline for factual claim verification. Runs `/fact-check` → `/reconcile` → `/implement` → `/verify`

## States (no brackets)

### Workflow Types
- **BUILD** - Primary output is working code
- **SOLVE** - Primary output is knowledge/decisions/documents

### Complexity (BUILD)
- **COMPLEXITY-LOW** - Single file, clear scope (patch version)
- **COMPLEXITY-MEDIUM** - Multiple files, some dependencies (minor version)
- **COMPLEXITY-HIGH** - Breaking changes, new patterns (major version)

### Problem Types (SOLVE)
- **RESEARCH** - Explore topic, gather information
- **ANALYSIS** - Deep dive into data or situation
- **EVALUATION** - Compare options, make recommendations
- **WRITING** - Create documents, books, reports
- **DECISION** - Choose between alternatives
- **HOTFIX** - Production down
- **BUGFIX** - Defect investigation
- **CHORE** - Maintenance analysis
- **MIGRATION** - Data or system migration

<!-- START: Core -->
### Core States
- **SESSION-MODE**
- **PROJECT-MODE**

### Core Operation Modes
- **IMPL-CODEBASE**
- **IMPL-ISOLATED**
<!-- END: Core -->

<!-- START: Skill: workspace-management -->
### workspace-management States
- **SINGLE-PROJECT**
- **MONOREPO**
- **WORKSPACE**
- **SINGLE-VERSION**
- **MULTI-VERSION**
- **SYNCED**
- **SELF-CONTAINED**
- **SOFTWARE-DEV**
- **GENERAL**
<!-- END: Skill: workspace-management -->

<!-- See devsystem-core.md for definitions and behavior of each state -->

## Labels

### Severity
- **[CRITICAL]** - Production failure risk
- **[HIGH]** - Likely failure under normal conditions
- **[MEDIUM]** - Edge case failure risk
- **[LOW]** - Minor issue

### Assumption
- **[VERIFIED]** - Confirmed correct
- **[UNVERIFIED]** - Made without evidence
- **[CONTRADICTS]** - Conflicted with reality
- **[OUTDATED]** - May no longer be valid
- **[INCOMPLETE]** - Missing critical considerations

### Status
- **[RESOLVED]** - Issue fixed
- **[WONT-FIX]** - Accepted trade-off
- **[NEEDS-DISCUSSION]** - Requires consultation

## Tracking Documents

- **NOTES** - Key decisions, topic registry, current phase
- **PROGRESS** - To Do, In Progress, Done, phase plan
- **PROBLEMS** - Issues discovered during session
- **FAILS** - Failure log (what went wrong)
- **LEARNINGS** - Retrospective analysis (via `/learn`)

## Project Topics

- **AGNTMAPR** - Agentic MapReduce (Devin's 5-stage pipeline for whole-codebase reasoning: Plan, Shard, Map, Reduce, Verify) - 2026-01-17
- **AGNTPROB** - Agentic Problems (categorized failure patterns in AI-assisted development) - 2026-07-08
- **AIDET** - AI Writing Detection (detection methods, signals, heuristics for identifying AI-generated text) - 2026-06-05
- **AMSW** - Auto Model SWitcher (Windsurf model switching automation) - 2026-01-26
- **AXCEL** - Agent Excel Skill (Excel automation from Cascade agent) - 2026-01-17
- **BNCL** - Binoculars Cross-Perplexity Detection (zero-shot AI text detection via cross-model perplexity ratio) - 2026-06-05
- **DOCWRITEFW** - Document Writing Frameworks (analytical/communication frameworks for IPPS document quality) - 2026-04-12
- **DRPRF** - Deep Research Profile Templates (personal, company, organization, network profile research) - 2026-05-25
- **DVDT** - Devin Desktop (Windsurf IDE renamed to Devin Desktop; INFO_HOW_DEVIN_WORKS reference doc) - 2026-05-27
- **EDIGA** - Energie Digitalisierung A (digitalization in energy sector research) - 2026-01-17
- **ENDIG** - Energie Digitalisierung (digitalization in energy sector research) - 2026-01-17
- **ENDSY** - Energie Digital Synthese (consolidated INFO from EnergieDigitalA + B) - 2026-01-17
- **FCTCHECK** - Factcheck Workflow (factuality verification for agent-generated documents). INFO: `Docs/Concepts/_INFO_HOW_TO_CHECK_FACTUALITY.md` - 2026-08-30
- **FINRESAI** - Finance Research AI (research quality/speed value in finance, AI application critique) - 2026-01-17
- **FINSTRWF** - Follow Instructions Workflow (post-execution instruction-following gap analysis and remediation) - 2026-06-12
- **FLCOR** - Fail Correction (cross-repo fails collection and analysis) - 2026-01-17
- **GCRU** - Global Coding Rules (universal coding conventions) - 2026-01-17
- **GLOB** - Global/project-wide items - 2026-01-22
- **IPPSPRMTFMT** - IPPS Prompt File Format (syntax, semantics, execution model for prompt queue files) - 2026-08-31
- **HMNWRTPTN** - Human Writing Patterns (forensic linguistics research for conversation humanizing rules) - 2026-07-16
- **LLMCG** - LLM Code Generation (RAG-augmented vs fine-tuned vs prompt-engineered approaches comparison) - 2026-01-17
- **LLMEV** - LLM Evaluation Skill (generic evaluation pipeline) - 2026-01-23
- **LLMTR** - LLM Transcription Skill (image-to-markdown, audio-to-markdown) - 2026-01-26
- **LMWS** - LM Studio + Windsurf integration research - 2026-01-29
- **MCPS** - MCP server integrations - 2026-01-22
- **MDPDF** - Markdown to PDF Renderer (Python tool with theme.json and settings.json) - 2026-05-01
- **MECE** - Mutually Exclusive, Collectively Exhaustive (grouping/decomposition quality principle) - 2026-04-12
- **MECT** - Minimal Explicit Consistent Terminology (communication design principle) - 2026-01-17
- **MEPI** - MEPI/MCPI research depth principle - 2026-01-24
- **MINTO** - Minto Pyramid Principle (communication framework research and reference) - 2026-01-17
- **MIPPS** - Minimal IPPS (DevSystem compression pipeline) - 2026-03-20
- **NTICP** - Network Traffic Interception (programmatic HTTPS interception for LLM prompt extraction) - 2026-01-17
- **OCLAW** - OpenClaw exploration (remote agent interaction via WhatsApp/Cascade) - 2026-01-17
- **PLWR** - Playwriter MCP (Chrome extension browser automation) - 2026-03-15
- **RECSLFIM** - Recursive Self-Improvement (AI systems accelerating or automating their own development) - 2026-08-13
- **REPRT** - Report Writing (DevSystem capability for Minto Pyramid-based high-quality reports) - 2026-04-16
- **RLSPROJ** - Release Project Workflow (unified multi-repo tagging and release notes process) - 2026-09-05
- **RUSESCPOL** - Russia escalation policy in Ukraine war (official statements, nuclear doctrine, red lines) - 2026-01-17
- **SDDEV** - Spec-Driven Development (research topic) - 2026-01-17
- **STYLO** - Stylometric Profiling (feature-based AI text detection via writing style analysis) - 2026-06-05
- **SUMQR** - Summary Quality Rules (improving enforcement and quality of summaries) - 2026-04-12
- **TOOLS** - .tools folder relocation and path updates - 2026-02-11
- **TRNGFX** - Transcription graphics/ASCII art optimization - 2026-01-22
- **WMRK** - Watermarking and Provenance (SynthID-Text, C2PA, embedded signal detection for AI-generated text) - 2026-06-05
- **WS2DV** - Windsurf 2.0 and Devin (deep research on Windsurf 2.0 release features and Devin integration) - 2026-01-17
- **WSFT** - Windsurf Features (comprehensive feature research for updating WSRF-IN01) - 2026-01-17
- **WSKMGMT** - Workspace Management Skill (DevSystem V5.0 workspace/project operations skill) - 2026-09-03
- **WSWN** - What? So What? Now What? (reflective framework deep research, Borton/Driscoll/Rolfe) - 2026-04-12
- **WSTKTRAC** - Windsurf Token Logging (token usage tracking via hooks) - 2026-01-17
- **WRTPRMPT** - Write Prompts Workflow (prompt queue file generation for sequential headless execution) - 2026-08-31
- **XLATE** - Translation quality (LLM translation improvement methods, DeepL integration, reflection workflow) - 2026-05-05
- **ZAIINT** - Z.AI Integration (GLM model integration into llm-evaluation skill) - 2026-01-17
