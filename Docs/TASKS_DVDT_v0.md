# TASKS: DVDT-IN01 Recreation

**Doc ID**: DVDT-TK01
**Goal**: Recreate INFO_HOW_DEVIN_WORKS.md from template, filling all 19 sections with current product state
**Source**: `_INFO_HOW_DEVIN_WORKS_TEMPLATE.md`, internal research files (see Internal Sources below)

## MUST-NOT-FORGET

- **PRIVACY GATE**: The output document (INFO_HOW_DEVIN_WORKS.md) MUST NOT reference any internal source files. No file paths, session folder names, or internal document IDs from sources may appear. The Sources section (S18) must contain ONLY official web URLs (docs.devin.ai, anthropic.com, openai.com, cognition.com, etc.)
- **SELF-CONTAINED**: Every claim must trace to an official web source or be marked [VERIFIED] from product observation
- **CASCADE INCLUDED**: Cascade is still shipped. Section 12 is dedicated to it. Do not minimize or deprecate
- **DEVIN LOCAL UPDATES**: Conversation sharing NOW supported (corrects old doc). Permission modes expanded to 5
- **FABLE 5 CORRECTED**: Suspension lifted 2026-06-30, access restored 2026-07-01 (old doc said suspended)
- **SWE-1.7 REPLACES SWE-1.6**: Update all model references
- **NO MARKDOWN TABLES**: Use lists with bold labels per core-conventions.md

## Internal Sources (for task execution only - NEVER leak into output)

- **SRC-OLD**: Previous version of DVDT-IN01 (1650 lines, covers through 2026-08-04)
- **SRC-DELTA**: DVDT-IN02 recent changes document (485 lines, covers 2026-08-04 to 2026-08-27)
- **SRC-RESEARCH**: Session research folder with Cascade system prompt analysis, tool definitions, protocol internals, multi-model architecture

## Task Overview

- Total tasks: 22
- Phases: 8 (Setup, Foundation, Intelligence, Extensibility, Agent-Specific, Business, Technical, Finalization)
- Parallelizable: 10 tasks (within phases)

## Section Mapping (Old → New)

```
OLD                              NEW                              ACTION
S1  Overview                  →  S1  Overview                     Update key concepts
S2  What Changed              →  S2  Product History              Condense (112→~40 lines)
S3  Agent Harnesses (211 ln)  →  S3  Agent Architecture           Split into 5 subsections
S4  ACP                       →  S3.4 (merged into Agent Arch)    Merge
S5  ACC and Spaces            →  S4  ACC and Spaces               Add multi-window, session controls
S6  AI Models (72 ln)         →  S5  AI Models and Routing        MAJOR expansion (7 new models)
S7  Windsurf Tab              →  S7.1 Tab Completion              Merge into Code Editing
S8  Context Awareness         →  S7.2-7.5                         Merge into Code Editing
S9  Code Review               →  S8  Code Review                  Add Security Swarm
S10 Security                  →  S6  Permissions and Security     NEW consolidated section
S11 Customization (220 ln)    →  S9, S10, S11                     Split into 3 sections
S12 Cascade Hooks             →  S11.3 + S12                      Redistribute
S13 MCP Integration           →  S11.2                            Merge into Extensibility
S14 Developer Tools           →  Distributed to S13, S16          Redistribute
S15 Pricing                   →  S14 Pricing                      Update
S16 Enterprise                →  S15 Enterprise                   Update
S17 Settings (124 ln)         →  S16 Settings                     Update paths
S18 Architecture              →  S17 Architecture                 Enrich from SRC-RESEARCH
S19 Sources                   →  S18 Sources                      Official web URLs only
S20 Document History          →  S19 Document History             Fresh start
```

## Tasks

### Phase 0: Setup

- [ ] **DVDT-TK-001** - Copy template and establish document
  - Copy `_INFO_HOW_DEVIN_WORKS_TEMPLATE.md` to `INFO_HOW_DEVIN_WORKS.md`
  - Strip top comment block, fill header fields (Version scope: 3.8.20+ / CLI 2026.5.26+)
  - Remove MUST-NOT-FORGET section (it's a writing guide, not output content)
  - Done when: File exists with correct header, empty sections ready for content
  - Depends: none
  - Est: 0.25 HHW

### Phase 1: Foundation (sequential)

- [ ] **DVDT-TK-002** - Fill Section 1: Overview
  - From: SRC-OLD S1 (lines 106-137)
  - Content: Product identity, platform support, remote dev, key concepts glossary
  - Update: Add Cascade to key concepts, update Windsurf Tab naming, add VS Code 1.126 base
  - Done when: Platform support, remote dev, and all key concepts defined with [VERIFIED] labels
  - Depends: TK-001
  - Est: 1 HHW

- [ ] **DVDT-TK-003** - Fill Section 2: Product History
  - From: SRC-OLD S2 (lines 138-249, 112 lines → condense to ~40)
  - Content: Rebrand event, backward compat, path fallbacks, CLI aliases
  - Cut: Remove detailed UI change descriptions, keep only facts affecting current users
  - Done when: Rebrand timeline, compat list, and path fallbacks documented. Under 50 lines
  - Depends: TK-002
  - Est: 0.5 HHW

- [ ] **DVDT-TK-004** - Fill Section 3: Agent Architecture
  - From: SRC-OLD S3 (lines 250-460) + S4 (lines 461-513) + SRC-DELTA sections
  - Subsections:
    - 3.1 Devin Local: permissions model (Deny/Ask/Allow), supported/unsupported features, MCP config paths. UPDATE: conversation sharing now supported, editable command approvals, session permission grants
    - 3.2 Devin Cloud: VM environment, tiers (Standard/Fusion/Ultra), PR review
    - 3.3 Devin CLI: architecture-level only (commands go in S13), cross-platform, same harness as Local
    - 3.4 ACP: protocol description, supported agents list (Codex, Claude Agent, OpenCode, Junie, Gemini CLI), browser preview
    - 3.5 Cascade: brief arch description, maintenance status, cross-ref to S12 for detailed features
  - Done when: All 5 subsections filled, Devin Local supports/unsupports lists accurate per SRC-DELTA corrections
  - Depends: TK-002
  - Est: 2 HHW

- [ ] **DVDT-TK-005** - Fill Section 4: Agent Command Center and Spaces
  - From: SRC-OLD S5 (lines 514-575) + SRC-DELTA 3.8.20 ACC changes
  - Content: Kanban view, multi-window (devin.agentWindow.location), session management (rename, fork, share), Ctrl/Cmd+G mode switching
  - Update: Add space-following behavior, side-by-side agent windows from 3.8.20
  - Done when: ACC and Spaces fully described including latest 3.8.20 features
  - Depends: TK-002
  - Parallel: [P] with TK-004 after TK-002
  - Est: 1 HHW

### Phase 2: Intelligence (parallel after Phase 1)

- [ ] **DVDT-TK-006** - Fill Section 5: AI Models and Routing
  - From: SRC-OLD S6 (lines 576-647) + SRC-DELTA Section 1 (all 7 new models with full detail)
  - Subsections:
    - 5.1 Cognition: SWE-1.7 (benchmarks, Cerebras serving, Kimi K2.7 base, Lightning variant), SWE-1.5
    - 5.2 Anthropic: Opus 5 (benchmarks, adaptive thinking, Fast mode), Sonnet 5 (permanent pricing), Fable 5 (CORRECTED: restored July 1), Opus 4.8/4.7
    - 5.3 OpenAI: GPT-5.6 Sol/Terra/Luna (price history, benchmarks, Luna WARNING, METR caveat), GPT-5.5, GPT-5.4
    - 5.4 Other: Gemini 3.7 Flash, Kimi K3 (open weights, Delta Attention)
    - 5.5 FrontierCode ranking (code block from SRC-DELTA)
    - 5.6 Routing: adaptive router, Arena Mode, BYOK
  - Done when: All models have name, release date, pricing, context/output, cutoff, benchmarks, availability
  - Depends: TK-001
  - Parallel: [P]
  - Est: 2 HHW

- [ ] **DVDT-TK-007** - Fill Section 7: Code Editing and Completion
  - From: SRC-OLD S7 (lines 648-678) + S8 (lines 679-729)
  - Subsections: Tab Completion, Fast Context, DeepWiki, Knowledge Base, Remote Indexing
  - Update: Rename "Windsurf Tab" to current product name if changed
  - Done when: All 5 subsections filled with feature descriptions
  - Depends: TK-001
  - Parallel: [P]
  - Est: 1 HHW

- [ ] **DVDT-TK-008** - Fill Section 8: Code Review
  - From: SRC-OLD S9 (lines 730-768) + S10 Security Swarm portion (lines 769-829)
  - Subsections: Devin Review, Quick Review, Security Swarm
  - Done when: Review types described, Security Swarm separated from permissions
  - Depends: TK-001
  - Parallel: [P]
  - Est: 1 HHW

### Phase 3: Permissions (after Phase 1)

- [ ] **DVDT-TK-009** - Fill Section 6: Permissions and Security
  - From: SRC-OLD S10 (lines 769-829) + S3 permissions model + SRC-DELTA Section 3 (smart mode, 5 modes, agent/permission independence)
  - Subsections:
    - 6.1 Permission Modes: all 5 modes (Normal, Accept Edits, Smart, Bypass, Autonomous) with descriptions
    - 6.2 Smart Permission Mode: fast-model judging, never-auto-approved list, rollout status
    - 6.3 Permission Rule Composition: deny-wins, level precedence
    - 6.4 Security Hardening: symlink protection (3.6.27), restricted mode, sudo handling, TLS/cert store (3.7.16)
    - 6.5 Sandbox: Autonomous mode enforcement
  - NEW CONTENT: Agent/permission mode independence, Smart mode permission matrix, never-auto-approved action list
  - Done when: All 5 subsections filled, permission matrix documented, Smart mode mechanics clear
  - Depends: TK-004 (needs Devin Local permissions context)
  - Est: 1.5 HHW

### Phase 4: Extensibility (parallel)

- [ ] **DVDT-TK-010** - Fill Section 9: Extensibility - Rules and AGENTS.md
  - From: SRC-OLD S11 Rules subsection (lines 843-868) + AGENTS.md subsection
  - Content: 4 trigger modes, path discovery order, scoping, .devinrules, glob patterns
  - Clarify: What works in Cascade vs Devin Local
  - Done when: Rules format, trigger modes, path fallbacks, AGENTS.md behavior documented
  - Depends: TK-001
  - Parallel: [P]
  - Est: 1 HHW

- [ ] **DVDT-TK-011** - Fill Section 10: Extensibility - Skills and Workflows
  - From: SRC-OLD S11 Skills + Workflows subsections
  - Content: SKILL.md format, progressive disclosure, detection ceiling (~32), triggers: ["user"], $ARGUMENTS, context compaction survival
  - Content: Workflow format, Cascade-only status, devin migrate workflows
  - Done when: Skills and Workflows fully documented with format examples
  - Depends: TK-001
  - Parallel: [P]
  - Est: 1 HHW

- [ ] **DVDT-TK-012** - Fill Section 11: Extensibility - Plugins, MCP, and Hooks
  - From: SRC-OLD S11 Plugins + S13 (MCP, lines 1085-1153) + S12 (Hooks, lines 1050-1084) + SRC-DELTA (expanded plugins)
  - Subsections:
    - 11.1 Plugins: directory structure, manifest precedence, install/trust flow, closed beta status
    - 11.2 MCP: config locations, mcp_config.json, MCP prompts as slash commands, auth flow
    - 11.3 Hooks: SessionStart, SessionEnd, Stop, plugin-contributed hooks
  - Update from SRC-DELTA: plugins now contribute rules, hooks, MCP servers, subagents
  - Done when: Plugin manifest, MCP config, and hook lifecycle documented
  - Depends: TK-001
  - Parallel: [P]
  - Est: 1.5 HHW

### Phase 5: Agent-Specific (parallel)

- [ ] **DVDT-TK-013** - Fill Section 12: Cascade (Legacy Agent)
  - From: SRC-OLD S3 Cascade subsection + S11 Memories + S12 Hooks + SRC-RESEARCH
  - Subsections:
    - 12.1 Modes: Code, Plan, Ask. Megaplan
    - 12.2 Memories: auto-generated, workspace-scoped, global_rules.md
    - 12.3 Cascade-Only Features: Code Lenses, App Deploys
  - Do NOT duplicate: Rules, Skills (covered in S9, S10). Only features UNIQUE to Cascade
  - Enrich from SRC-RESEARCH: system prompt structure, multi-model architecture, behavioral control mechanisms
  - Done when: Cascade modes, memories, and unique features documented. Cross-refs to S9-S11 for shared features
  - Depends: TK-010, TK-011 (to know what's already covered)
  - Est: 1 HHW

- [ ] **DVDT-TK-014** - Fill Section 13: Devin CLI Reference
  - From: SRC-OLD S3 CLI subsection + S14 (Developer Tools, lines 1154-1199) + SRC-DELTA Section 3
  - Subsections:
    - 13.1 Top-Level Commands: devin rm (--force), devin desktop, devin doctor, devin plugins (install/uninstall/trust/list)
    - 13.2 Slash Commands: /recap, /rename, /btw (parallel side-chat), /fast, /usage, /mode, /share, /loop, /mcp, /context, /plan, /ask, /normal, /smart, /yolo
    - 13.3 Configuration: CLI-specific config keys only (keymap, notify, permission-mode defaults), reference S16 for general config
  - Done when: All commands and slash commands listed with descriptions
  - Depends: TK-001
  - Parallel: [P]
  - Est: 1 HHW

### Phase 6: Business (parallel)

- [ ] **DVDT-TK-015** - Fill Section 14: Pricing and Plans
  - From: SRC-OLD S15 (lines 1200-1247)
  - Content: Free, Pro ($15/mo), Max ($60/mo), Teams ($40/user/mo), Enterprise
  - Include: Quota system, daily/weekly budgets, ACU for enterprise
  - Research: Verify current pricing at https://devin.ai/pricing (may have changed)
  - Done when: All plans listed with prices, quotas, and ACU explanation
  - Depends: TK-001
  - Parallel: [P]
  - Est: 0.5 HHW

- [ ] **DVDT-TK-016** - Fill Section 15: Enterprise Features
  - From: SRC-OLD S16 (lines 1248-1297)
  - Content: RBAC, SSO/SCIM, FedRAMP, Analytics API, GPO/MDM, sandbox enforcement, network enforcement, team settings
  - Done when: Enterprise features listed with descriptions
  - Depends: TK-001
  - Parallel: [P]
  - Est: 0.5 HHW

### Phase 7: Technical (parallel)

- [ ] **DVDT-TK-017** - Fill Section 16: Settings and Configuration
  - From: SRC-OLD S17 (lines 1298-1421)
  - Subsections:
    - 16.1 File Paths and Fallbacks: .devin/ vs .windsurf/, app data per OS, extension paths
    - 16.2 Settings: devin.* namespace, notable config options
    - 16.3 Proxy and Network: proxy config, TLS cert handling (Windows fix from 3.7.16)
  - Include: config.json and mcp_config.json file structure (full format here, S13.3 references this)
  - Done when: All paths, settings, and config formats documented
  - Depends: TK-001
  - Parallel: [P]
  - Est: 1.5 HHW

- [ ] **DVDT-TK-018** - Fill Section 17: Architecture Internals
  - From: SRC-OLD S18 (lines 1422-1475) + SRC-RESEARCH (protocol, multi-model arch, gRPC methods, context growth)
  - Content: VS Code OSS base (1.126), extension host, agent communication, telemetry, update mechanism
  - Enrich: gRPC protocol (7 methods), GetChatMessage structure, multi-model pipeline, feature flags, context growth patterns
  - Privacy: Describe architecture patterns without referencing source extraction methodology
  - Done when: Architecture described at reference level, enriched with protocol details
  - Depends: TK-001
  - Parallel: [P]
  - Est: 1.5 HHW

### Phase 8: Finalization (sequential, after all content)

- [ ] **DVDT-TK-019** - Write Summary section
  - Synthesize key findings from ALL content sections into grouped summary
  - Categories: Agent harnesses, AI models, Extensibility, Permissions, Code editing/review, Pricing, Enterprise, Configuration
  - Each item ends with verification label
  - Max 7 categories, 3-5 items each
  - Done when: Summary covers all major sections, all items labeled
  - Depends: TK-002 through TK-018
  - Est: 1 HHW

- [ ] **DVDT-TK-020** - Build Sources section (S18)
  - Collect all official web URLs used across all sections
  - Format: `DVDT-IN01-SC-[SOURCE_ID]-[SOURCE_REF]`: URL - Description [VERIFIED]
  - Group: Primary Sources, Secondary Sources
  - CRITICAL: No internal file paths. Only official web resources
  - Verify: Each URL resolves to a real page
  - Done when: All sources listed, no internal references, all URLs verified
  - Depends: TK-002 through TK-018
  - Est: 1 HHW

- [ ] **DVDT-TK-021** - Write Document History (S19)
  - Fresh start: "Initial document created from template (Option B: Capability-Layer organization)"
  - Note: Recreated from scratch, previous version archived as INFO_HOW_DEVIN_WORKS_2028-08-04.md
  - Done when: Document History section complete
  - Depends: TK-020
  - Est: 0.25 HHW

- [ ] **DVDT-TK-022** - Final Verification
  - Run `/verify` on completed document
  - Check: APAPALAN, MECT, INFO_RULES compliance
  - Check: No internal source file paths leaked
  - Check: All models have complete entry pattern (name, date, pricing, context, cutoff, benchmarks)
  - Check: Cascade properly represented (not minimized)
  - Check: Fable 5 status corrected (restored, not suspended)
  - Check: Devin Local supports list updated (conversation sharing = yes)
  - Check: TOC anchor links match headings
  - Check: All [VERIFIED]/[ASSUMED] labels present on summary items
  - Done when: All checks pass, document ready for use
  - Depends: TK-021
  - Est: 1 HHW

## Dependency Graph

```
TK-001 (Setup)
├─> TK-002 (S1 Overview)
│   ├─> TK-003 (S2 Product History)
│   ├─> TK-004 (S3 Agent Architecture)
│   │   └─> TK-009 (S6 Permissions)
│   └─> TK-005 (S4 ACC and Spaces) [P]
├─> TK-006 (S5 AI Models) [P]
├─> TK-007 (S7 Code Editing) [P]
├─> TK-008 (S8 Code Review) [P]
├─> TK-010 (S9 Rules) [P]
├─> TK-011 (S10 Skills/Workflows) [P]
├─> TK-012 (S11 Plugins/MCP/Hooks) [P]
│   TK-010 + TK-011
│   └─> TK-013 (S12 Cascade)
├─> TK-014 (S13 CLI Reference) [P]
├─> TK-015 (S14 Pricing) [P]
├─> TK-016 (S15 Enterprise) [P]
├─> TK-017 (S16 Settings) [P]
└─> TK-018 (S17 Architecture) [P]
    ALL(TK-002..TK-018)
    ├─> TK-019 (Summary)
    ├─> TK-020 (Sources)
    │   └─> TK-021 (Document History)
    │       └─> TK-022 (Final Verification)
```

## Document History

**[2026-08-27 20:11]**
- Initial tasks plan created for DVDT-IN01 recreation from Option B template
