# ID Registry

**Goal**: Prevent term and ID collisions across workspace.

## DevSystem Constants

### Frameworks

- **AGEN** - Agentic English (controlled vocabulary)
- **EDIRD** - Explore, Design, Implement, Refine, Deliver (phase model)
- **STRUT** - Structured Thinking (planning method)
- **TRACTFUL** - Traceable Requirements Artifacts and Coded Templates For Unified Lifecycle (document framework)

### Identifier Types

- **FEATURE_SLUG** - Kebab-case feature identifier (e.g., `user-authentication`)
- **TOPIC** - 2-6 uppercase letters for component (e.g., `AUTH`, `CRWL`)
- **TDID** - Tractful Document ID. Format: `[TOPIC]-[DOC][NN]`

### Measurement

- **HWT** - Human Work Time
- **AWT** - Agentic Work Time

### Strategies

- **MEPI** - Most Executable Point of Information
- **MCPI** - Most Complete Point of Information
- **SOCAS** - Signs Of Confusion And Sloppiness

### Document Types

- **INFO** (IN) - Research and analysis documents
- **SPEC** (SP) - Technical specifications
- **IMPL** (IP) - Implementation plans
- **TEST** (TP) - Test plans
- **TASKS** (TK) - Task plans (partitioned work items)
- **REVIEW** (RV) - Review documents (suffix: `-RV[NN]`)
- **FIXES** - Code changes log for release documentation

### Tracking Documents

- **NOTES** - Key decisions, topic registry, current phase
- **PROGRESS** - To Do, In Progress, Done tracking
- **PROBLEMS** - Issues discovered during session
- **FAILS** - Failure log (lessons learned)

### Spec-Level Item IDs

Used in SPEC documents, referenced across IMPL and TEST.

- **FR** - Functional Requirement (`[TOPIC]-FR-[NN]`)
- **DD** - Design Decision (`[TOPIC]-DD-[NN]`)
- **IG** - Implementation Guarantee (`[TOPIC]-IG-[NN]`)
- **AC** - Acceptance Criterion (`[TOPIC]-AC-[NN]`)

### Plan-Level Item IDs

Used in IMPL and TEST documents. Include doc reference.

- **EC** - Edge Case (`[TOPIC]-IP[NN]-EC-[NN]`)
- **IS** - Implementation Step (`[TOPIC]-IP[NN]-IS-[NN]`)
- **TC** - Test Case (`[TOPIC]-TP[NN]-TC-[NN]`)
- **VC** - Verification Checklist (`[TOPIC]-IP[NN]-VC-[NN]`)

### Tracking Item IDs

Used in PROBLEMS.md, FAILS.md, REVIEW.md, backlog docs.

- **BG** - Bug (`[TOPIC]-BG-[NNN]`)
- **FT** - Feature request (`[TOPIC]-FT-[NNN]`)
- **PR** - Problem (`[TOPIC]-PR-[NNN]`)
- **FX** - Fix (`[TOPIC]-FX-[NNN]`)
- **TK** - Task (`[TOPIC]-TK-[NNN]`)
- **RV** - Review finding (`[TOPIC]-RV-[NNN]`)
- **FL** - Failure log entry (`[TOPIC]-FL-[NNN]`)
- **RF** - Refactoring (`[TOPIC]-RF-[NNN]`)

### Source IDs (INFO documents)

- **SC** - Source marker (`[TOPIC]-[DOC]-SC-[SOURCE_ID]-[SOURCE_REF]`)

### Verification Labels

Progress markers for findings and assumptions.

- **[ASSUMED]** - Unverified assumption
- **[VERIFIED]** - Verified by re-reading source
- **[TESTED]** - Tested in POC
- **[PROVEN]** - Proven in actual implementation

### Failure Categories

Severity markers for FAILS.md entries.

- **[CRITICAL]** - Production failure risk
- **[HIGH]** - Likely failure under normal conditions
- **[MEDIUM]** - Edge case failure risk
- **[LOW]** - Minor issue
- **[RESOLVED]** - Issue fixed

## Project Topics

Register all TOPIC IDs here before use. Format: `TOPIC` - Description

- **GLOB** - Global/workspace-wide concerns
- **AGEN** - Agentic English specs and docs
- **EDIRD** - Phase model specs and docs
- **STRUT** - Structured Thinking specs and docs
- **TRACTFUL** - Document framework specs and docs
- **TDID** - Document ID system specs and docs

## Document History

**[2026-01-20 16:05]**
- Added exhaustive Item ID Types from all templates
- Added Spec-Level, Plan-Level, Tracking, Source IDs
- Added Verification Labels and Failure Categories

**[2026-01-20 15:40]**
- Renamed from CONCEPTS.md to ID-REGISTRY.md
- Restructured: DevSystem Constants + Project Topics

**[2026-01-17 14:44]**
- Simplified to inventory format
