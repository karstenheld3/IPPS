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

- **INFO** (IN), **SPEC** (SP), **IMPL** (IP), **TEST** (TP), **TASKS** (TK), **FIX**, **REVIEW** (RV)

### Tracking Documents

- **NOTES**, **PROGRESS**, **PROBLEMS**, **FAILS**

## Project Topics

Register all TOPIC IDs here before use. Format: `TOPIC` - Description

- **GLOB** - Global/workspace-wide concerns
- **AGEN** - Agentic English specs and docs
- **EDIRD** - Phase model specs and docs
- **STRUT** - Structured Thinking specs and docs
- **TRACTFUL** - Document framework specs and docs
- **TDID** - Document ID system specs and docs

## Document History

**[2026-01-20 15:40]**
- Renamed from CONCEPTS.md to ID-REGISTRY.md
- Restructured: DevSystem Constants + Project Topics

**[2026-01-17 14:44]**
- Simplified to inventory format
