# INFO: OpenAI API Documentation Changes (2026-01-31 vs 2026-03-20)

**Doc ID**: OAIAPI-CHANGES
**Goal**: Compare OpenAI API documentation between 2026-01-31 (62 topics, 45 files) and 2026-03-20 (74 planned, 36 written) to identify additions, changes, deprecations, and required actions
**Timeline**: Created 2026-03-20, Updated 1 time (2026-03-20 - 2026-03-20)

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` in both `OpenAI_API_2026-01-31/` and `OpenAI_API_2026-03-20/` for topic structure

## Summary

- API grew from 62 topics (45 files) to 74 planned topics (36 written, 38 pending) [VERIFIED]
- 5 new API endpoints, 6 new dedicated topics, 9+ new model families [VERIFIED]
- Responses API expanded from basic create to full CRUD with 3 new endpoints [VERIFIED]
- Assistants API deprecated with sunset 2026-08-26; replaced by Responses + Conversations [VERIFIED]
- Realtime Beta deprecated with sunset 2026-05-07; replaced by GA Realtime API [VERIFIED]
- Video generation SDK method renamed `videos.generate` -> `videos.create` with parameter changes [VERIFIED]
- SDK v2.29.0 verification identified 107 issues across 8 files, 94 fixed [VERIFIED]

## Table of Contents

1. [New Features and Additions](#1-new-features-and-additions)
2. [Changes in Existing API Features](#2-changes-in-existing-api-features)
3. [Deprecations and Phase-Out](#3-deprecations-and-phase-out)
4. [Recommended Actions](#4-recommended-actions)
5. [Sources](#5-sources)
6. [Document History](#6-document-history)

## 1. New Features and Additions

### 1.1 New API Endpoints

- **Token Counting** (2026-03-20 IN09) - `POST /v1/responses/input_tokens/count` for pre-request cost estimation. Not in 2026-01-31 docs
- **Response Input Items** (2026-03-20 IN10) - `GET` list input items for a response with pagination. Not in 2026-01-31 docs
- **Skills API** (2026-03-20 IN17) - Reusable tool packages with CRUD, versioning, content retrieval. Works with `tool_search` built-in tool. Not in 2026-01-31 docs
- **Compact endpoint** (2026-03-20 IN06) - `POST /v1/responses/{id}/compact` to compress conversation context. Not in 2026-01-31 docs
- **Cancel endpoint** (2026-03-20 IN06) - `POST /v1/responses/{id}/cancel` to cancel in-progress responses. Not in 2026-01-31 docs

### 1.2 New Dedicated Topics (Previously Embedded or Absent)

- **Tools Overview** (2026-03-20 IN12) - Dedicated topic for tool types, `tool_choice`, parallel tool calls. Was scattered across Responses and Chat in 2026-01-31
- **Function Calling** (2026-03-20 IN13) - Dedicated topic with JSON schema, strict mode, parallel calls. Was embedded in Chat Completions (2026-01-31 IN09)
- **Web Search** (2026-03-20 IN14) - Built-in `web_search` tool, search context size, user location, deep research models (`o3-deep-research`, `o4-mini-deep-research`)
- **Structured Outputs** (2026-03-20 IN15) - Dedicated topic for JSON schema response formatting, `text.format` (Responses) vs `response_format` (Chat), strict mode
- **Reasoning** (2026-03-20 IN16) - Reasoning models (GPT-5, o4-mini, o3-pro), reasoning effort, thinking budget, reasoning summaries
- **Migration Guide** (2026-03-20 IN11) - Chat Completions -> Responses API parameter mapping, streaming changes, structured output differences

### 1.3 New Models (2026-03-20 vs 2026-01-31)

- **GPT-5.4** - New flagship model (2026-01-31 had GPT-5 as flagship)
- **GPT-5 mini, GPT-5 nano** - Smaller model tiers
- **GPT-5.2-Codex, gpt-5.1-codex-max, gpt-5-codex** - Dedicated coding agent models
- **o3-pro** - High-end reasoning model
- **o3-deep-research, o4-mini-deep-research** - Deep research models
- **gpt-image-1.5, gpt-image-1, gpt-image-1-mini** - New image generation models (replacing/augmenting DALL-E)
- **sora-2-pro** - Higher quality video generation tier
- **computer-use-preview** - Computer Use Agent (CUA) model
- **gpt-4o-mini-transcribe** - New transcription model alongside Whisper

### 1.4 Planned but Not Yet Written (IN37-IN74 in 2026-03-20 TOC)

- Codex/Code Generation (IN63), Agents Framework (IN64), Computer Use (IN65), MCP/Connectors (IN66)
- Deep Research (IN67), File Inputs/Vision (IN68), Voice Agents (IN69), WebSocket Mode (IN70)
- Prompt Caching (IN71), Background/Flex Processing (IN72), Safety/Data Privacy (IN73), Optimization Guides (IN74)
- Reinforcement Fine-Tuning (IN30), Graders (IN31), Prompt Engineering (IN24)
- Full Chat Completions suite (IN55-57), Legacy APIs (IN58-60), Administration (IN47-54)

## 2. Changes in Existing API Features

### 2.1 Responses API (2026-01-31 IN05 -> 2026-03-20 IN06)

- Expanded from basic `create` to full CRUD (Create, Read, Update, Delete): create, retrieve, delete, cancel, compact, count tokens
- Tools expanded from `code_interpreter`, `file_search`, `function` to also include `web_search`, `tool_search`, `computer_use`
- Added background mode for long-running tasks
- Added `previous_response_id` for conversation chaining

### 2.2 Video Generation (2026-01-31 IN18 -> 2026-03-20 IN22)

- Method renamed: `videos.generate` -> `videos.create` in SDK (Software Development Kit) v2.29.0
- Parameters changed: `duration` -> `seconds`, `aspect_ratio`/`resolution` -> `size`
- New operations: `characters`, `edit`, `extend`, `remix`, `download_content`
- New model tier: `sora-2-pro` (higher quality, longer generation)

### 2.3 Audio (2026-01-31 IN17 -> 2026-03-20 IN18+IN19+IN20)

- Split from single topic into 3: Transcription, Text-to-Speech (TTS), Realtime Audio
- TTS expanded with custom voices and consent management (eligible accounts only)
- New transcription model: `gpt-4o-mini-transcribe`

### 2.4 Images (2026-01-31 IN19+IN20 -> 2026-03-20 IN21)

- Consolidated from 2 files to 1 (generation + streaming merged)
- New models: `gpt-image-1.5`, `gpt-image-1`, `gpt-image-1-mini` alongside DALL-E

### 2.5 Evals (2026-01-31 IN24 -> 2026-03-20 IN25)

- Expanded with prompt optimizer
- Added external models in evals
- SDK path corrected: `evals.datasets.create` does not exist; use `evals.create(data_source_config=..., testing_criteria=[...])`

### 2.6 Fine-Tuning (2026-01-31 IN25 -> 2026-03-20 IN26)

- Added pause/resume capabilities
- Added DPO (Direct Preference Optimization) and reinforcement fine-tuning
- Graders integration for training metrics

### 2.7 Vector Stores (2026-01-31 IN30-32 -> 2026-03-20 IN30)

- Consolidated from 3 files to 1 (stores, files, batches combined)
- Added search endpoint directly on vector stores

### 2.8 Realtime API (2026-01-31 IN33-37 -> 2026-03-20 IN20)

- Consolidated from 5 dedicated files to 1 overview file (IN20 Realtime Audio)
- Full detail files planned as IN39-42 but not yet written
- Added Calls API (create, retrieve, list) for lifecycle management
- Legacy Realtime Beta marked deprecated (sunset 2026-05-07)

### 2.9 Conversations (2026-01-31 IN06 -> 2026-03-20 IN08)

- Expanded from basic multi-turn context to full CRUD API
- Items sub-resource with CRUD + list
- Now explicitly positioned as replacement for deprecated Assistants threads

### 2.10 Core Documentation Restructured

- 2026-01-31 `Debugging` (IN03) + `Error Handling` (IN60) -> 2026-03-20 `Errors` (IN04)
- 2026-01-31 `Compatibility` (IN04) -> merged into 2026-03-20 `Introduction` (IN01)
- 2026-01-31 `Rate Limits` guide (IN59) -> promoted to 2026-03-20 core topic (IN05)
- 2026-01-31 `Models` (IN23) -> promoted from "AI Core" to 2026-03-20 core (IN03)

## 3. Deprecations and Phase-Out

### 3.1 Assistants API - Sunset 2026-08-26

- 2026-01-31: Active API with 6 dedicated files (IN11-16: Assistants, Threads, Messages, Runs, Run Steps, Streaming)
- 2026-03-20: Moved to legacy (IN58 planned), 4 files still written (IN31-34) but marked deprecated
- Migration path: Responses API + Conversations API
- SDK: All calls require `client.beta.` prefix (not promoted to stable)

### 3.2 Realtime Beta - Sunset 2026-05-07

- 2026-01-31: Documented as `IN58_REALTIME_BETA`
- 2026-03-20: Planned as `IN60_LEGACY_REALTIME_BETA`
- Migration: GA (General Availability) Realtime API with session/event differences

### 3.3 codex-mini-latest Model - Removed 2026-02-12

- Legacy shell tool only worked with this model
- Replaced by GPT-5.2-Codex family

### 3.4 Legacy Completions API

- 2026-01-31: `IN57_COMPLETIONS` - `POST /v1/completions` (deprecated)
- 2026-03-20: Planned as `IN59_LEGACY_COMPLETIONS`
- Migration: Chat Completions or Responses API

### 3.5 Merged Topics

- **Messages** (2026-01-31 IN13) merged into Threads (2026-03-20 IN32) - messages are now a sub-topic
- **Assistants Streaming** (2026-01-31 IN16) merged into Runs (2026-03-20 IN33) - streaming is now part of run execution

## 4. Recommended Actions

### 4.1 Breaking Changes Requiring Immediate Attention

- **Assistants API users**: Plan migration to Responses + Conversations before 2026-08-26 sunset. Use `client.beta.assistants/threads` prefix in SDK v2.29.0 until migration
- **Realtime Beta users**: Migrate to GA Realtime API before 2026-05-07 sunset
- **Video generation code**: Update `videos.generate` -> `videos.create`, fix param names (`duration`->`seconds`, `aspect_ratio`->`size`)
- **Evals code**: `evals.datasets.create` does not exist in SDK; use `evals.create()` with `data_source_config` parameter

### 4.2 Migrations Worth Considering

- **Chat Completions -> Responses API**: More features (tools, background mode, stored responses, cancel/compact), migration guide in 2026-03-20 IN11
- **Streaming**: SDK prefers `responses.stream()` context manager over `create(stream=True)`. Both work, but `stream()` is the recommended pattern
- **Audio code**: If using single audio topic, split into separate transcription and TTS workflows for clarity

### 4.3 Improvement Options

- **Token counting**: Use new `input_tokens/count` endpoint for cost estimation before expensive requests
- **Prompt caching**: Automatic in API, monitor `cached_tokens` in usage for cost savings (planned IN71)
- **Background mode**: Use for long-running deep research and complex tasks instead of synchronous requests
- **Skills API**: Consider packaging reusable tools as skills for `tool_search` discovery
- **Flex processing**: Lower cost alternative to batch for non-urgent workloads (planned IN72)

### 4.4 Documentation Gaps (2026-03-20 Planned but Not Written)

- 38 files planned in TOC (IN37-IN74) but not yet written
- Missing: Administration (8 files), Chat Completions detail (3 files), Legacy APIs (3 files), Agents/Automation (4 files), Specialized (4 files), Cross-cutting guides (6 files), Realtime detail (3 files), Vector Store sub-resources (2 files), Containers (2 files), ChatKit, SDKs
- Priority: Administration, Chat Completions, and Agents/Automation are highest-value gaps

## 5. Sources

- `__OAIAPI_TOC.md [OAIAPI-TOC]` in `OpenAI_API_2026-01-31/` - 2026-01-31 topic structure (62 topics)
- `__OAIAPI_TOC.md [OAIAPI-TOC]` in `OpenAI_API_2026-03-20/` - 2026-03-20 topic structure (74 topics)
- SDK verification via openai Python SDK v2.29.0 at `e:\Dev\.tools\llm-venv\`
- `STRUT_CODE_VERIFY.md` in `_PrivateSessions/_2026-03-20_OpenAIAPIDocumentation/` - verification plan and results

## 6. Document History

**[2026-03-20 17:08]**
- Initial comparison document created from TOC-level analysis of both documentation sets
- Moved from inline section in `HOW_TO_CREATE_API_DOCS.md` to proper INFO document
