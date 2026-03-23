# API Changelog

**Doc ID**: OAIAPI-IN62
**Goal**: Document key API changelog milestones and deprecation timeline
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references

## Summary

The OpenAI API Changelog tracks all significant changes: new endpoints, model releases, deprecations, feature additions, and breaking changes. The changelog is the authoritative source for API evolution. Key recent milestones: Responses API launch (March 2025), Assistants API deprecation announcement (August 2025, sunset August 2026), Realtime API GA, Agents SDK releases (Python and TypeScript), ChatKit beta launch, Codex platform evolution, model releases (GPT-4.1 family, o3/o4 reasoning models, gpt-realtime-1.5), Containers API, MCP integration, Computer Use tool, Deep Research API, and numerous fine-tuning and batch API improvements. The changelog is published at developers.openai.com/api/docs/changelog with entries ordered reverse-chronologically. Deprecation notices include sunset dates and migration guides. Model lifecycle follows dated snapshot pattern with grace periods before removal. [VERIFIED] (OAIAPI-SC-OAI-CHLOG)

## Key Facts

- **URL**: developers.openai.com/api/docs/changelog [VERIFIED] (OAIAPI-SC-OAI-CHLOG)
- **Format**: Reverse-chronological entries [VERIFIED] (OAIAPI-SC-OAI-CHLOG)
- **Deprecations**: Include sunset dates and migration guides [VERIFIED] (OAIAPI-SC-OAI-CHLOG)
- **Model lifecycle**: Dated snapshots with grace periods [VERIFIED] (OAIAPI-SC-OAI-CHLOG)

## Key Milestones (2025-2026)

### API Evolution
- **Responses API** launch (March 2025) - simpler alternative to Chat Completions
- **Assistants API** deprecated (August 2025) - sunset 2026-08-26
- **Legacy Completions** - only gpt-3.5-turbo-instruct remains

### Models
- **GPT-4.1 family**: gpt-4.1, gpt-4.1-mini, gpt-4.1-nano
- **Reasoning models**: o3, o3-pro, o4-mini with deep research variants
- **Realtime models**: gpt-realtime, gpt-realtime-1.5

### Features
- **Containers API**: Sandboxed execution for Code Interpreter and Shell
- **ChatKit**: Embeddable chat UI (beta)
- **MCP integration**: Model Context Protocol tool support
- **Computer Use**: CUA tool for UI automation
- **Deep Research**: Multi-step automated research
- **Agents SDK**: Python and TypeScript releases
- **Prompt caching**: Automatic with up to 90% input cost reduction
- **Flex processing**: 50% discount for latency-insensitive workloads

### Deprecations
- **Assistants API**: Sunset 2026-08-26
- **Legacy Completions**: Limited to gpt-3.5-turbo-instruct
- **gpt-4o-realtime-preview**: Superseded by gpt-realtime GA models
- **function_call parameter**: Replaced by tool_calls

## Deprecation Policy

- **Dated model snapshots**: Specific date suffixed models (e.g., gpt-4o-2024-08-06)
- **Grace period**: Minimum notice before removal
- **Migration guides**: Provided for major API changes
- **Deprecation page**: developers.openai.com/api/docs/deprecations

## Sources

- OAIAPI-SC-OAI-CHLOG - API Changelog

## Document History

**[2026-03-20 18:50]**
- Initial documentation created
