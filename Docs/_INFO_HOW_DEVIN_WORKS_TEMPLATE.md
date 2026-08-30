<!-- INFO_HOW_DEVIN_WORKS TEMPLATE
Naming: INFO_HOW_DEVIN_WORKS.md (single instance, updated in place)
Lifecycle: Recreated from scratch when product changes accumulate beyond incremental updates.
           Use _DEVIN_RECENT_CHANGES.md [DVDT-IN02] as input for delta since last version.
           Archive old version as INFO_HOW_DEVIN_WORKS_[LAST_UPDATE_DATE].md before recreating.
Remove this comment block after creating the document.
-->

# INFO: How Devin Desktop Works

**Doc ID**: DVDT-IN01
<!-- Topic IDs: 7-14 uppercase chars. Inside T##/S## folders use nested: [TOPIC]-[SUBTOPIC]-IN[NN] -->
**Goal**: Comprehensive reference for Devin Desktop (formerly Windsurf) - agent harnesses, AI models, customization, developer tools, enterprise controls, and architecture internals
**Version scope**: Devin Desktop [VERSION]+ / Devin Local [CLI_VERSION]+
**Timeline**: Created YYYY-MM-DD, Updated N times

## MUST-NOT-FORGET

<!-- Remove this section after writing the document -->
- Factual claims from external sources need a source ID: `DVDT-IN01-SC-[SOURCE_ID]-[SOURCE_REF]`
- Online sources, apps, tools: include inline markdown link at first mention in each content section (INFO-SC-05)
- Summary items need verification labels: [VERIFIED], [ASSUMED], [TESTED], [PROVEN]
- Cascade MUST be included as a maintained agent - it is still being shipped
- Model entries follow repeatable pattern: name, release date, pricing, context/output, knowledge cutoff, benchmarks, availability
- Permission modes are a rapidly evolving area - document all modes with matrix
- Distinguish Devin Local features from Cascade features explicitly (what each supports and does not support)
- Check _DEVIN_RECENT_CHANGES.md [DVDT-IN02] for latest delta since last version

## Summary

<!-- Instruction: Group findings by category matching the major document sections.
     Each item ends with [VERIFIED], [ASSUMED], or other label.
     Keep to 3-5 items per category, max 7 categories. -->

**[Category 1]:**
- [Key finding] [LABEL]

**[Category 2]:**
- [Key finding] [LABEL]

## Table of Contents

1. [Overview](#1-overview)
2. [Product History](#2-product-history)
3. [Agent Architecture](#3-agent-architecture)
4. [Agent Command Center and Spaces](#4-agent-command-center-and-spaces)
5. [AI Models and Routing](#5-ai-models-and-routing)
6. [Permissions and Security](#6-permissions-and-security)
7. [Code Editing and Completion](#7-code-editing-and-completion)
8. [Code Review](#8-code-review)
9. [Extensibility: Rules and AGENTS.md](#9-extensibility-rules-and-agentsmd)
10. [Extensibility: Skills and Workflows](#10-extensibility-skills-and-workflows)
11. [Extensibility: Plugins, MCP, and Hooks](#11-extensibility-plugins-mcp-and-hooks)
12. [Cascade (Legacy Agent)](#12-cascade-legacy-agent)
13. [Devin CLI Reference](#13-devin-cli-reference)
14. [Pricing and Plans](#14-pricing-and-plans)
15. [Enterprise Features](#15-enterprise-features)
16. [Settings and Configuration](#16-settings-and-configuration)
17. [Architecture Internals](#17-architecture-internals)
18. [Sources](#18-sources)
19. [Document History](#19-document-history)

## 1. Overview

<!-- Instruction: Product identity, platform support, remote development, key concepts glossary.
     Include: Devin Next pre-release channel, VS Code OSS base version, supported platforms. -->

[Product description - what Devin Desktop is, how it positions itself]

**Platform support:**
- **Windows** [version]+
- **macOS** [version]+
- **Linux** [distribution and glibc requirements]

**Remote development:**
- **SSH** - [implementation details, host requirements]
- **Dev Containers** - [platform support, Docker requirement]
- **WSL** - [support status]

**Key concepts:**
- **Agent Command Center (ACC)** - [description]
- **Agent Client Protocol (ACP)** - [description]
- **Devin Local** - [description]
- **Devin Cloud** - [description]
- **Devin CLI** - [description]
- **Cascade** - [description]
- **Spaces** - [description]

<!-- Conditional: insert "Devin Next" subsection when pre-release channel has distinct features worth documenting -->

## 2. Product History

<!-- Conditional: shrink or merge into Overview when rebrand is >12 months old and no longer causes user confusion.
     Instruction: Cover rebrand event, backward compatibility, brand unification.
     Keep factual and brief - this section should shrink over time. -->

[Rebrand timeline, what changed, what stayed compatible]

**Backward compatibility:**
- [What carries over: settings, extensions, keybindings, etc.]
- [Path fallbacks: .devin/ vs .windsurf/]
- [CLI aliases that still work]

## 3. Agent Architecture

<!-- Instruction: Cover ALL agent harnesses and how they relate. Each agent gets a subsection.
     For each agent: what it is, how it runs, what it supports/does not support.
     ACP gets its own subsection as the protocol connecting agents to the IDE. -->

### 3.1 Devin Local

<!-- Instruction: Primary local agent. Cover: permissions model, agent profiles, supported features,
     explicitly unsupported features, configuration location. -->

[Description, how it replaces Cascade]

**Supports:** [feature list]
**Does NOT support:** [feature list - explicit gaps vs Cascade]

### 3.2 Devin Cloud

<!-- Instruction: Cloud agent. Cover: VM environment, tiers, session model, PR review integration. -->

[Description, how cloud sessions work]

### 3.3 Devin CLI

<!-- Instruction: Terminal agent. Cover: relationship to Devin Local harness, cross-platform support.
     Detailed commands go in Section 13. Keep this to architecture-level description. -->

[Description, same harness as Devin Local]

### 3.4 Agent Client Protocol (ACP)

<!-- Instruction: Open protocol. Cover: what it is, supported agents, browser preview, slash commands.
     List all known ACP-compatible agents. -->

[Protocol description, supported agents list]

### 3.5 Cascade

<!-- Instruction: Brief architectural description here. Detailed feature coverage in Section 12.
     Cover: what Cascade is, its relationship to Devin Local, maintenance status. -->

[Legacy agent, maintained status, migration path to Devin Local]

## 4. Agent Command Center and Spaces

<!-- Instruction: Cover ACC UI (Kanban view, multi-window, session management) and Spaces (task grouping).
     Include: devin.agentWindow.location setting, session controls (rename, fork, share). -->

### 4.1 Agent Command Center

[ACC description, multi-window support, session management]

### 4.2 Spaces

[Spaces description, shared context across sessions]

## 5. AI Models and Routing

<!-- Instruction: Cover ALL available models with repeatable entry pattern.
     Each model entry: name (linked), release date, pricing, context/output, knowledge cutoff, key benchmarks, availability.
     Also cover: adaptive router, Arena Mode, BYOK, model picker behavior, FrontierCode ranking.
     Group by provider: Cognition (SWE), Anthropic (Claude), OpenAI (GPT), Google (Gemini), Moonshot (Kimi). -->

### 5.1 Cognition Models

<!-- Instruction: SWE model family. Include Lightning variants. Note: no direct API access. -->

**[Model Name](URL)** (released YYYY-MM-DD):
- [Pricing per MTok input/output]
- [Context window, max output]
- [Knowledge cutoff]
- [Key benchmarks with scores]
- [Availability: which Devin surfaces]

### 5.2 Anthropic Models

<!-- Instruction: Claude model family. Include suspended/restored status for any affected models.
     Note pricing changes (introductory vs permanent). Cover adaptive thinking, effort levels. -->

[Model entries following same pattern as 5.1]

### 5.3 OpenAI Models

<!-- Instruction: GPT model family. Include tiered pricing, price cut history, Fast mode.
     Note long-context surcharges. Cover reasoning effort levels. -->

[Model entries following same pattern as 5.1]

### 5.4 Other Models

<!-- Instruction: Gemini, Kimi, and any other third-party models available in Devin. -->

[Model entries following same pattern as 5.1]

### 5.5 FrontierCode Ranking

<!-- Instruction: Current benchmark ranking across all models. Use code block for alignment. -->

```
[score]  [Model Name]
[score]  [Model Name]
```

### 5.6 Model Routing and Selection

<!-- Instruction: Adaptive router, Arena Mode, BYOK, model picker behavior per plan tier. -->

[Router description, Arena Mode, BYOK configuration]

## 6. Permissions and Security

<!-- Instruction: Consolidated permissions and security section. Cover:
     - 5 permission modes (Normal, Accept Edits, Smart, Bypass, Autonomous) with matrix
     - Agent/permission mode independence
     - Smart mode fast-model judging mechanics and never-auto-approved list
     - Permission rule composition (deny-wins across levels)
     - Symlink write protection
     - Restricted Mode (untrusted workspaces)
     - Sudo handling
     - Sandbox enforcement (Autonomous mode)
     - Windows TLS / cert store behavior -->

### 6.1 Permission Modes

[Permission mode descriptions and matrix]

### 6.2 Smart Permission Mode

[Fast model judging, never-auto-approved actions, rollout status]

### 6.3 Permission Rule Composition

[Deny-wins, level precedence: enterprise > mode > user > project > subagent]

### 6.4 Security Hardening

[Symlink protection, restricted mode, sudo handling, TLS/cert store]

### 6.5 Sandbox

<!-- Conditional: insert when Autonomous mode sandbox has distinct documentation beyond permission modes -->

[Sandbox enforcement details for Autonomous mode]

## 7. Code Editing and Completion

<!-- Instruction: Cover Tab completion, Supercomplete, context awareness tools.
     Include: Fast Context, DeepWiki, Knowledge Base, Remote Indexing. -->

### 7.1 Tab Completion

[Autocomplete and Supercomplete description]

### 7.2 Fast Context

[SWE-grep models, retrieval speed]

### 7.3 DeepWiki

[Auto-indexing, architecture wikis]

### 7.4 Knowledge Base

<!-- Conditional: insert when Teams/Enterprise features are documented -->

[Shared Google Docs as team knowledge]

### 7.5 Remote Indexing

[Index remote repos without local clone]

## 8. Code Review

<!-- Instruction: Cover Devin Review (deep PR review) and Quick Review (fast local review).
     Include: Security Swarm, Autofix, smart diff organization. -->

### 8.1 Devin Review

[Deep PR review, smart diff, bug detection, Autofix]

### 8.2 Quick Review

[Fast local review, SWE-check model]

### 8.3 Security Swarm

[Security-focused review capabilities]

## 9. Extensibility: Rules and AGENTS.md

<!-- Instruction: Cover rules system and AGENTS.md.
     Include: trigger modes (always_on, model_decision, glob, manual), path fallbacks (.devin/ vs .windsurf/),
     scoping, nested discovery, .devinrules. Distinguish what works in Cascade vs Devin Local. -->

### 9.1 Rules

[Rules format, trigger modes, path discovery, scoping]

### 9.2 AGENTS.md

[AGENTS.md / agents.md support, behavior]

## 10. Extensibility: Skills and Workflows

<!-- Instruction: Cover skills (work in both Cascade and Devin Local) and workflows (Cascade only).
     Include: progressive disclosure, detection ceiling (~32 skills), triggers: ["user"],
     SKILL.md format, $ARGUMENTS interpolation, context compaction survival.
     Cover devin migrate workflows command. -->

### 10.1 Skills

[Skills format, progressive disclosure, detection ceiling, invocation control]

### 10.2 Workflows

<!-- Instruction: Cascade-only feature. Note migration path via devin migrate workflows. -->

[Workflow format, invocation, Cascade-only status, migration]

## 11. Extensibility: Plugins, MCP, and Hooks

<!-- Instruction: Cover the plugin system, MCP integration, and lifecycle hooks.
     Include: plugin directory structure, manifest precedence, MCP servers/prompts,
     hook types (SessionStart, SessionEnd, Stop), subagent contribution.
     Note closed beta status for plugins if still applicable. -->

### 11.1 Plugins

[Plugin format, directory structure, manifest precedence, install/trust flow]

### 11.2 MCP Integration

[MCP server configuration, mcp_config.json, MCP prompts as slash commands, auth]

### 11.3 Lifecycle Hooks

[Hook types, trigger points, plugin-contributed hooks]

## 12. Cascade (Legacy Agent)

<!-- Instruction: Features UNIQUE to Cascade that Devin Local does not have.
     Include: modes (Code, Plan, Ask), Memories, Code Lenses, App Deploys, Hooks (Cascade-specific).
     Note: maintained through at least [date]. Do NOT duplicate features covered elsewhere (rules, skills). -->

### 12.1 Modes

[Code, Plan, Ask modes. Megaplan.]

### 12.2 Memories

[Auto-generated, workspace-scoped memories]

### 12.3 Cascade-Only Features

<!-- Instruction: Features present in Cascade but absent from Devin Local.
     Examples: Code Lenses, App Deploys, Conversation Sharing (check current status). -->

[Feature list with current status]

## 13. Devin CLI Reference

<!-- Instruction: CLI commands and slash commands reference.
     Include: top-level commands (devin rm, devin desktop, devin doctor, devin plugins),
     slash commands (/recap, /rename, /btw, /fast, /usage, /mode, /share, /loop, /mcp, /context),
     config.json structure, keybindings, notify config, background shells. -->

### 13.1 Top-Level Commands

[devin <command> reference]

### 13.2 Slash Commands

[Slash command reference with descriptions]

### 13.3 Configuration

<!-- Instruction: Cover CLI-specific config only (keymap, notify, permission-mode defaults, subagents_enabled).
     General config paths and OS-specific locations go in Section 16. Avoid duplicating config.json/mcp_config.json structure here -
     reference Section 16 for file format, cover CLI-specific keys only. -->

[CLI-specific configuration keys and options]

## 14. Pricing and Plans

<!-- Instruction: Cover plan tiers, quota system, pricing.
     Include: Free, Pro, Max, Teams, Enterprise with prices and quotas.
     Note ACU (Agent Compute Units) for enterprise. -->

[Plan comparison, quota system, ACU]

## 15. Enterprise Features

<!-- Instruction: Cover enterprise-specific features.
     Include: RBAC, SSO/SCIM, FedRAMP, Analytics API, GPO/MDM policies,
     sandbox enforcement, network enforcement, team settings. -->

[Enterprise feature list]

## 16. Settings and Configuration

<!-- Instruction: Cover paths, config files, migration, proxy settings.
     Include: .devin/ vs .windsurf/ fallback paths, app data locations per OS,
     executable names and aliases, devin.* settings namespace. -->

### 16.1 File Paths and Fallbacks

[Path discovery order, OS-specific locations]

### 16.2 Settings

[devin.* settings, notable configuration options]

### 16.3 Proxy and Network

[Proxy configuration, TLS cert handling]

## 17. Architecture Internals

<!-- Instruction: Cover internal architecture details relevant to power users.
     Include: VS Code OSS base, extension host, agent communication,
     telemetry, update mechanism. Keep brief - this is a reference, not source analysis. -->

[Architecture description]

## 18. Sources

<!-- Instruction: Use source ID format DVDT-IN01-SC-[SOURCE_ID]-[SOURCE_REF].
     Group by Primary Sources and Secondary Sources.
     Each entry: source ID, URL, description, [VERIFIED] label. -->

**Primary Sources:**
- `DVDT-IN01-SC-[SOURCE_ID]-[SOURCE_REF]`: [URL] - [Description] [VERIFIED]

**Secondary Sources:**
- `DVDT-IN01-SC-[SOURCE_ID]-[SOURCE_REF]`: [URL] - [Description] [VERIFIED]

## 19. Document History

**[YYYY-MM-DD HH:MM]**
- Initial document created from template (Option B: Capability-Layer organization)

<!-- EXAMPLE: Reference only. Do not copy into new documents. Shows model entry pattern from Section 5. -->

## Full Example (Model Entry Pattern)

```markdown
### 5.2 Anthropic Models

**[Claude Opus 5](https://www.anthropic.com/research/claude-opus-5)** (released 2026-07-24):
- $5/$25 per MTok (same price as Opus 4.8); Fast mode at $10/$50 (2.5x speed)
- 1M token context, 128K max output (300K on Batch API with beta header)
- Knowledge cutoff: May 2026; adaptive thinking (default effort `high`)
- Available: Claude API, Amazon Bedrock, Google Cloud, Microsoft Foundry
- Benchmarks: Frontier-Bench v0.1 SOTA (2x Opus 4.8), CursorBench 3.2 within 0.5% of Fable 5
- Default on Claude Max, strongest on Claude Pro

**[Claude Sonnet 5](https://www.anthropic.com/news/claude-sonnet-5)** (released 2026-06-30):
- $2/$10 per MTok (introductory pricing made permanent 2026-08-10)
- 1M token context, 128K max output
- Knowledge cutoff: January 2026
- Outperforms Opus 4.8 on FrontierCode benchmark
- Default for Free and Pro plans
```
