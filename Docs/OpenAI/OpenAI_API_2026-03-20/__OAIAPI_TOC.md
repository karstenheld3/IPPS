# OpenAI API Documentation - Table of Contents

**Doc ID**: OAIAPI-TOC
**Goal**: Master index for all OpenAI API documentation files
**Version scope**: API v1, Documentation date 2026-03-20
**Research stats**: [pending - added in final phase]

**Depends on:**
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references

## Summary

The OpenAI API is a RESTful API (v1) at `https://api.openai.com` providing programmatic access to OpenAI's language models (GPT-5.4, GPT-5, o4-mini, o3-pro), image generation (gpt-image-1.5, gpt-image-1, DALL-E), video generation (Sora, sora-2), audio (Whisper, TTS, gpt-4o-mini-transcribe), embedding, and moderation models. Authentication uses `Authorization: Bearer` with API keys, plus optional `OpenAI-Organization` and `OpenAI-Project` headers for multi-org/project routing. Two primary text generation interfaces exist: the Responses API (`POST /v1/responses`) as the recommended primary interface supporting conversations, built-in tools (web_search, file_search, code_interpreter, tool_search), and background mode; and the Chat Completions API (`POST /v1/chat/completions`) as the stable legacy interface. The Conversations API provides persistent multi-turn state management, replacing the deprecated Assistants API (sunset August 26, 2026). Built-in tools include web search, file search with vector stores, code interpreter with containers, tool search for skill discovery, deep research agents (o3-deep-research, o4-mini-deep-research), and remote MCP server integration. The Skills API enables reusable tool packages with versioning. Platform APIs cover audio (transcription, translation, TTS, custom voices with consent management), video generation and editing (characters, extend, remix), image generation and editing with streaming, embeddings, evals with graders, fine-tuning (supervised, DPO, reinforcement with pause/resume), batch processing at 50% cost, files and multipart uploads, models, and moderations. Vector Stores provide built-in RAG with file chunking, embedding, search, and batch operations. ChatKit (beta) offers embeddable chat UI with sessions, threads, and customizable widgets. Containers provide sandboxed code execution environments. The Realtime API enables WebSocket-based voice/text streaming with calls and transcription sessions. Webhooks deliver event notifications with signature verification. Administration APIs manage organizations, projects, users, groups, roles, certificates (mTLS), service accounts, API keys, rate limits, audit logs, usage tracking, and cost reporting. Rate limits are tier-based (RPM/TPM) per model, per organization/project, with x-ratelimit-* response headers. The API version is `2020-10-01` with backwards-compatible evolution. Official SDKs exist for Python, TypeScript/Node, .NET, Java, Go, and more.

## Topic Files

### Core Documentation (5 files)

- [`_INFO_OAIAPI-IN01_INTRODUCTION.md`](./_INFO_OAIAPI-IN01_INTRODUCTION.md) OAIAPI-IN01
  - API overview, base URL, versioning, backwards compatibility, X-Client-Request-Id
  - Sources: OAIAPI-SC-OAI-OVERVIEW, OAIAPI-SC-OAI-GOVRVW

- [`_INFO_OAIAPI-IN02_AUTHENTICATION.md`](./_INFO_OAIAPI-IN02_AUTHENTICATION.md) OAIAPI-IN02
  - API keys, Bearer auth, OpenAI-Organization, OpenAI-Project headers, key management
  - Sources: OAIAPI-SC-OAI-OVERVIEW, OAIAPI-SC-OAI-ADMOVW

- [`_INFO_OAIAPI-IN03_MODELS.md`](./_INFO_OAIAPI-IN03_MODELS.md) OAIAPI-IN03
  - Model families (GPT-5.x, o-series, image, audio, embedding, moderation), capabilities, pricing, aliases, context windows, deprecations
  - Sources: OAIAPI-SC-OAI-MODAPI, OAIAPI-SC-OAI-GMODLS, OAIAPI-SC-OAI-GPRICE, OAIAPI-SC-OAI-GLATEST, OAIAPI-SC-OAI-GDEPR

- [`_INFO_OAIAPI-IN04_ERRORS.md`](./_INFO_OAIAPI-IN04_ERRORS.md) OAIAPI-IN04
  - HTTP status codes, error response format, error types, debugging, x-request-id
  - Sources: OAIAPI-SC-OAI-OVERVIEW, OAIAPI-SC-OAI-GERROR

- [`_INFO_OAIAPI-IN05_RATE_LIMITS.md`](./_INFO_OAIAPI-IN05_RATE_LIMITS.md) OAIAPI-IN05
  - Rate limit tiers, RPM/TPM, x-ratelimit-* headers, usage tiers, project-level rate limits
  - Sources: OAIAPI-SC-OAI-GRLMT, OAIAPI-SC-OAI-ADMPRJ

### Responses API (6 files)

- [`_INFO_OAIAPI-IN06_RESPONSES_API.md`](./_INFO_OAIAPI-IN06_RESPONSES_API.md) OAIAPI-IN06
  - POST /v1/responses - create, retrieve, delete, cancel, compact; full request/response schema, parameters, tools configuration, reasoning, background mode
  - Sources: OAIAPI-SC-OAI-RESOVW, OAIAPI-SC-OAI-RESCRT, OAIAPI-SC-OAI-RESGET, OAIAPI-SC-OAI-RESDEL, OAIAPI-SC-OAI-RESCAN, OAIAPI-SC-OAI-RESCMP

- [`_INFO_OAIAPI-IN07_RESPONSES_STREAMING.md`](./_INFO_OAIAPI-IN07_RESPONSES_STREAMING.md) OAIAPI-IN07
  - SSE streaming events for Responses API, event types, partial responses, stream manager
  - Sources: OAIAPI-SC-OAI-RESSTR

- [`_INFO_OAIAPI-IN08_CONVERSATIONS.md`](./_INFO_OAIAPI-IN08_CONVERSATIONS.md) OAIAPI-IN08
  - Conversations API - create, retrieve, update, delete conversations; items CRUD; persistent multi-turn state
  - Sources: OAIAPI-SC-OAI-CNVCRT, OAIAPI-SC-OAI-CNVGET, OAIAPI-SC-OAI-CNVUPD, OAIAPI-SC-OAI-CNVDEL, OAIAPI-SC-OAI-CNVITM

- [`_INFO_OAIAPI-IN09_TOKEN_COUNTING.md`](./_INFO_OAIAPI-IN09_TOKEN_COUNTING.md) OAIAPI-IN09
  - POST /v1/responses/input_tokens/count - pre-request token estimation, cost calculation
  - Sources: OAIAPI-SC-OAI-RESTOK

- [`_INFO_OAIAPI-IN10_RESPONSE_INPUT_ITEMS.md`](./_INFO_OAIAPI-IN10_RESPONSE_INPUT_ITEMS.md) OAIAPI-IN10
  - GET list input items for a response, pagination
  - Sources: OAIAPI-SC-OAI-RESINP

- [`_INFO_OAIAPI-IN11_MIGRATE_TO_RESPONSES.md`](./_INFO_OAIAPI-IN11_MIGRATE_TO_RESPONSES.md) OAIAPI-IN11
  - Migration guide from Chat Completions to Responses API, parameter mapping, structured outputs changes
  - Sources: OAIAPI-SC-OAI-GMIGRR

### Tools and Function Calling (6 files)

- [`_INFO_OAIAPI-IN12_TOOLS_OVERVIEW.md`](./_INFO_OAIAPI-IN12_TOOLS_OVERVIEW.md) OAIAPI-IN12
  - Tool types overview: built-in tools vs function calling, tool_choice, parallel tool calls
  - Sources: OAIAPI-SC-OAI-GTOOLS, OAIAPI-SC-OAI-GFNCAL

- [`_INFO_OAIAPI-IN13_FUNCTION_CALLING.md`](./_INFO_OAIAPI-IN13_FUNCTION_CALLING.md) OAIAPI-IN13
  - Function definitions, JSON schema, strict mode, tool_choice, parallel function calls
  - Sources: OAIAPI-SC-OAI-GFNCAL, OAIAPI-SC-OAI-GSTRCT

- [`_INFO_OAIAPI-IN14_WEB_SEARCH.md`](./_INFO_OAIAPI-IN14_WEB_SEARCH.md) OAIAPI-IN14
  - Web search tool configuration, search context size, user location, deep research (o3-deep-research, o4-mini-deep-research)
  - Sources: OAIAPI-SC-OAI-GWBSRC, OAIAPI-SC-OAI-GDEEP

- [`_INFO_OAIAPI-IN15_STRUCTURED_OUTPUTS.md`](./_INFO_OAIAPI-IN15_STRUCTURED_OUTPUTS.md) OAIAPI-IN15
  - JSON schema response formatting, text.format (Responses) vs response_format (Chat), strict mode
  - Sources: OAIAPI-SC-OAI-GSTRCT

- [`_INFO_OAIAPI-IN16_REASONING.md`](./_INFO_OAIAPI-IN16_REASONING.md) OAIAPI-IN16
  - Reasoning models (GPT-5, o4-mini, o3-pro), reasoning effort, reasoning summaries, thinking budget
  - Sources: OAIAPI-SC-OAI-GREASN

- [`_INFO_OAIAPI-IN17_SKILLS.md`](./_INFO_OAIAPI-IN17_SKILLS.md) OAIAPI-IN17
  - Skills API - CRUD, versions, content retrieval; tool search; reusable tool packages
  - **Note**: Relatively new API, limited documentation
  - Sources: OAIAPI-SC-OAI-SKLAPI

### Audio (3 files)

- [`_INFO_OAIAPI-IN18_AUDIO_TRANSCRIPTION.md`](./_INFO_OAIAPI-IN18_AUDIO_TRANSCRIPTION.md) OAIAPI-IN18
  - POST /v1/audio/transcriptions, POST /v1/audio/translations; Whisper, gpt-4o-mini-transcribe; supported formats
  - Sources: OAIAPI-SC-OAI-AUDTRN, OAIAPI-SC-OAI-AUDTRL, OAIAPI-SC-OAI-GAUDIO

- [`_INFO_OAIAPI-IN19_TEXT_TO_SPEECH.md`](./_INFO_OAIAPI-IN19_TEXT_TO_SPEECH.md) OAIAPI-IN19
  - POST /v1/audio/speech; TTS models, voices, formats, speed; custom voices with consent management
  - **Limitation**: Custom voices limited to eligible accounts only
  - Sources: OAIAPI-SC-OAI-AUDSPK, OAIAPI-SC-OAI-AUDVOI, OAIAPI-SC-OAI-AUDVCS, OAIAPI-SC-OAI-GAUDIO

- [`_INFO_OAIAPI-IN20_REALTIME_AUDIO.md`](./_INFO_OAIAPI-IN20_REALTIME_AUDIO.md) OAIAPI-IN20
  - Realtime audio streaming, voice agents, realtime transcription overview
  - Sources: OAIAPI-SC-OAI-GAUDIO, OAIAPI-SC-OAI-GRTAPI

### Media Generation (4 files)

- [`_INFO_OAIAPI-IN21_IMAGE_GENERATION.md`](./_INFO_OAIAPI-IN21_IMAGE_GENERATION.md) OAIAPI-IN21
  - POST /v1/images/generations, /v1/images/edits, /v1/images/variations; gpt-image-1.5, gpt-image-1, DALL-E; sizes, formats, quality
  - Sources: OAIAPI-SC-OAI-IMGGEN, OAIAPI-SC-OAI-IMGEDT, OAIAPI-SC-OAI-IMGVAR, OAIAPI-SC-OAI-GIMAGE

- [`_INFO_OAIAPI-IN22_IMAGE_STREAMING.md`](./_INFO_OAIAPI-IN22_IMAGE_STREAMING.md) OAIAPI-IN22
  - SSE streaming for image generation and editing, partial image events
  - Sources: OAIAPI-SC-OAI-IMGSTR

- [`_INFO_OAIAPI-IN23_VIDEO_GENERATION.md`](./_INFO_OAIAPI-IN23_VIDEO_GENERATION.md) OAIAPI-IN23
  - POST /v1/videos; Sora, sora-2, sora-2-pro; create, retrieve, delete, list, download; characters, edit, extend, remix
  - **Note**: sora-2-pro is higher quality/longer generation time tier
  - Sources: OAIAPI-SC-OAI-VIDCRT, OAIAPI-SC-OAI-VIDCHR, OAIAPI-SC-OAI-VIDGET, OAIAPI-SC-OAI-VIDEDT, OAIAPI-SC-OAI-GVIDEO

- [`_INFO_OAIAPI-IN24_PROMPT_ENGINEERING.md`](./_INFO_OAIAPI-IN24_PROMPT_ENGINEERING.md) OAIAPI-IN24
  - Prompt engineering best practices, system prompts, few-shot, chain-of-thought, reusable prompts (dashboard prompt management with variables), prompt guidance
  - Sources: OAIAPI-SC-OAI-GPRMPT, OAIAPI-SC-OAI-GPRMGD

### AI Core (3 files)

- [`_INFO_OAIAPI-IN25_EMBEDDINGS.md`](./_INFO_OAIAPI-IN25_EMBEDDINGS.md) OAIAPI-IN25
  - POST /v1/embeddings; text-embedding-3-small/large, text-embedding-ada-002; dimensions, encoding formats
  - Sources: OAIAPI-SC-OAI-EMBCRT

- [`_INFO_OAIAPI-IN26_MODERATIONS.md`](./_INFO_OAIAPI-IN26_MODERATIONS.md) OAIAPI-IN26
  - POST /v1/moderations; omni-moderation-latest; category scores, multi-modal input
  - Sources: OAIAPI-SC-OAI-MODRT, OAIAPI-SC-OAI-GMODR

- [`_INFO_OAIAPI-IN27_MODELS_API.md`](./_INFO_OAIAPI-IN27_MODELS_API.md) OAIAPI-IN27
  - GET /v1/models, GET /v1/models/{model}, DELETE /v1/models/{model}; model listing, fine-tuned model deletion
  - Sources: OAIAPI-SC-OAI-MODAPI

### Evaluation and Training (4 files)

- [`_INFO_OAIAPI-IN28_EVALS.md`](./_INFO_OAIAPI-IN28_EVALS.md) OAIAPI-IN28
  - Evals API - CRUD evals, create/retrieve/delete/list/cancel runs, output items; prompt optimizer; external models in evals; evaluation best practices
  - Sources: OAIAPI-SC-OAI-EVLAPI, OAIAPI-SC-OAI-GEVLBP

- [`_INFO_OAIAPI-IN29_FINE_TUNING.md`](./_INFO_OAIAPI-IN29_FINE_TUNING.md) OAIAPI-IN29
  - Fine-tuning jobs - create, retrieve, list, cancel, pause, resume; events; checkpoints; permissions; supported models
  - Sources: OAIAPI-SC-OAI-FTJOBS, OAIAPI-SC-OAI-FTCKPT, OAIAPI-SC-OAI-GFNTN

- [`_INFO_OAIAPI-IN30_REINFORCEMENT_FINE_TUNING.md`](./_INFO_OAIAPI-IN30_REINFORCEMENT_FINE_TUNING.md) OAIAPI-IN30
  - DPO, reinforcement fine-tuning, graders (run, validate), training metrics
  - Sources: OAIAPI-SC-OAI-FTGRAD, OAIAPI-SC-OAI-GRFT

- [`_INFO_OAIAPI-IN31_GRADERS.md`](./_INFO_OAIAPI-IN31_GRADERS.md) OAIAPI-IN31
  - **[ALPHA]** Graders API - run, validate; grader types; eval integration
  - Sources: OAIAPI-SC-OAI-FTGRAD

### Processing (4 files)

- [`_INFO_OAIAPI-IN32_BATCH_API.md`](./_INFO_OAIAPI-IN32_BATCH_API.md) OAIAPI-IN32
  - POST /v1/batches; create, retrieve, list, cancel; 50% cost reduction; JSONL input/output; supported endpoints
  - Sources: OAIAPI-SC-OAI-BTCAPI, OAIAPI-SC-OAI-GBATCH

- [`_INFO_OAIAPI-IN33_FILES.md`](./_INFO_OAIAPI-IN33_FILES.md) OAIAPI-IN33
  - Files API - list, create, retrieve, delete, content; purpose types; supported formats
  - Sources: OAIAPI-SC-OAI-FILAPI

- [`_INFO_OAIAPI-IN34_UPLOADS.md`](./_INFO_OAIAPI-IN34_UPLOADS.md) OAIAPI-IN34
  - Uploads API - create, cancel, complete, create parts; multipart uploads for large files (>100MB)
  - Sources: OAIAPI-SC-OAI-UPLAPI

- [`_INFO_OAIAPI-IN35_WEBHOOKS.md`](./_INFO_OAIAPI-IN35_WEBHOOKS.md) OAIAPI-IN35
  - Webhook events, event types, signature verification, retry behavior
  - Sources: OAIAPI-SC-OAI-WBHEVT

### Vector Stores (3 files)

- [`_INFO_OAIAPI-IN36_VECTOR_STORES.md`](./_INFO_OAIAPI-IN36_VECTOR_STORES.md) OAIAPI-IN36
  - Vector stores - create, retrieve, update, delete, list, search; expiration policies; file search integration
  - Sources: OAIAPI-SC-OAI-VSAPI

- [`_INFO_OAIAPI-IN37_VECTOR_STORE_FILES.md`](./_INFO_OAIAPI-IN37_VECTOR_STORE_FILES.md) OAIAPI-IN37
  - Vector store files - create, retrieve, update, delete, list, content; chunking strategies; status tracking
  - Sources: OAIAPI-SC-OAI-VSFIL

- [`_INFO_OAIAPI-IN38_VECTOR_STORE_FILE_BATCHES.md`](./_INFO_OAIAPI-IN38_VECTOR_STORE_FILE_BATCHES.md) OAIAPI-IN38
  - File batches - create, retrieve, list files, cancel; bulk file operations
  - Sources: OAIAPI-SC-OAI-VSFBT

### Realtime API (4 files)

- [`_INFO_OAIAPI-IN39_REALTIME_OVERVIEW.md`](./_INFO_OAIAPI-IN39_REALTIME_OVERVIEW.md) OAIAPI-IN39
  - Realtime API overview, WebSocket connection, sessions, transcription sessions, calls
  - Sources: OAIAPI-SC-OAI-RTCLNT, OAIAPI-SC-OAI-RTCALL, OAIAPI-SC-OAI-GRTAPI

- [`_INFO_OAIAPI-IN40_REALTIME_CLIENT_EVENTS.md`](./_INFO_OAIAPI-IN40_REALTIME_CLIENT_EVENTS.md) OAIAPI-IN40
  - Client-to-server event types, session configuration, audio input, conversation management
  - Sources: OAIAPI-SC-OAI-RTCLEV

- [`_INFO_OAIAPI-IN41_REALTIME_SERVER_EVENTS.md`](./_INFO_OAIAPI-IN41_REALTIME_SERVER_EVENTS.md) OAIAPI-IN41
  - Server-to-client event types, audio output, function calls, error events
  - Sources: OAIAPI-SC-OAI-RTSREV

- [`_INFO_OAIAPI-IN42_REALTIME_CALLS.md`](./_INFO_OAIAPI-IN42_REALTIME_CALLS.md) OAIAPI-IN42
  - Calls API - create, retrieve, list; call lifecycle management
  - Sources: OAIAPI-SC-OAI-RTCALL

### Infrastructure (4 files)

- [`_INFO_OAIAPI-IN43_CONTAINERS.md`](./_INFO_OAIAPI-IN43_CONTAINERS.md) OAIAPI-IN43
  - Containers API - create, retrieve, delete, list; sandboxed execution environments
  - Sources: OAIAPI-SC-OAI-CNTAPI

- [`_INFO_OAIAPI-IN44_CONTAINER_FILES.md`](./_INFO_OAIAPI-IN44_CONTAINER_FILES.md) OAIAPI-IN44
  - Container files - create, retrieve, delete, list, content; file management in containers
  - Sources: OAIAPI-SC-OAI-CNTFIL

- [`_INFO_OAIAPI-IN45_CHATKIT.md`](./_INFO_OAIAPI-IN45_CHATKIT.md) OAIAPI-IN45
  - **[BETA]** ChatKit - sessions, threads, list items; embeddable chat UI; widgets; developer mode
  - Sources: OAIAPI-SC-OAI-CKSESS, OAIAPI-SC-OAI-CKTHR, OAIAPI-SC-OAI-GCHATK, OAIAPI-SC-OAI-GCKWDG

- [`_INFO_OAIAPI-IN46_SDKS.md`](./_INFO_OAIAPI-IN46_SDKS.md) OAIAPI-IN46
  - Official SDKs (Python, TypeScript, .NET, Java, Go), Agents SDK, installation, configuration
  - Sources: OAIAPI-SC-GH-SDKPY, OAIAPI-SC-GH-AGNTPY, OAIAPI-SC-GH-SDKREL

### Administration (8 files)

- [`_INFO_OAIAPI-IN47_ADMIN_OVERVIEW.md`](./_INFO_OAIAPI-IN47_ADMIN_OVERVIEW.md) OAIAPI-IN47
  - Administration overview, org/project hierarchy, RBAC model
  - Sources: OAIAPI-SC-OAI-ADMOVW

- [`_INFO_OAIAPI-IN48_ORG_USERS_INVITES.md`](./_INFO_OAIAPI-IN48_ORG_USERS_INVITES.md) OAIAPI-IN48
  - Organization users, invites, roles, role assignments; user management
  - Sources: OAIAPI-SC-OAI-ADMORG

- [`_INFO_OAIAPI-IN49_ORG_GROUPS_ROLES.md`](./_INFO_OAIAPI-IN49_ORG_GROUPS_ROLES.md) OAIAPI-IN49
  - Organization groups, custom roles, role CRUD; group-based access control
  - Sources: OAIAPI-SC-OAI-ADMORG

- [`_INFO_OAIAPI-IN50_PROJECTS.md`](./_INFO_OAIAPI-IN50_PROJECTS.md) OAIAPI-IN50
  - Projects - create, retrieve, update, list, archive; project users, groups, service accounts, API keys, rate limits
  - Sources: OAIAPI-SC-OAI-ADMPRJ

- [`_INFO_OAIAPI-IN51_CERTIFICATES.md`](./_INFO_OAIAPI-IN51_CERTIFICATES.md) OAIAPI-IN51
  - mTLS certificates - CRUD, activate, deactivate; org-level and project-level certificates
  - Sources: OAIAPI-SC-OAI-ADMORG

- [`_INFO_OAIAPI-IN52_AUDIT_LOGS.md`](./_INFO_OAIAPI-IN52_AUDIT_LOGS.md) OAIAPI-IN52
  - Audit logs - list, filtering; compliance and security logging
  - Sources: OAIAPI-SC-OAI-ADMORG

- [`_INFO_OAIAPI-IN53_USAGE_COSTS.md`](./_INFO_OAIAPI-IN53_USAGE_COSTS.md) OAIAPI-IN53
  - Usage tracking (completions, embeddings, images, audio, moderations, vector stores), cost reporting
  - Sources: OAIAPI-SC-OAI-ADMORG

- [`_INFO_OAIAPI-IN54_SERVICE_ACCOUNTS_API_KEYS.md`](./_INFO_OAIAPI-IN54_SERVICE_ACCOUNTS_API_KEYS.md) OAIAPI-IN54
  - Project service accounts, project API keys; programmatic access management
  - Sources: OAIAPI-SC-OAI-ADMPRJ

### Chat Completions (3 files)

- [`_INFO_OAIAPI-IN55_CHAT_COMPLETIONS.md`](./_INFO_OAIAPI-IN55_CHAT_COMPLETIONS.md) OAIAPI-IN55
  - POST /v1/chat/completions - create, retrieve, update, delete, list; full request/response schema; messages format
  - Sources: OAIAPI-SC-OAI-CHTCRT, OAIAPI-SC-OAI-CHTLST

- [`_INFO_OAIAPI-IN56_CHAT_STREAMING.md`](./_INFO_OAIAPI-IN56_CHAT_STREAMING.md) OAIAPI-IN56
  - SSE streaming for Chat Completions, chunk format, delta objects
  - Sources: OAIAPI-SC-OAI-CHTSTR

- [`_INFO_OAIAPI-IN57_CHAT_MESSAGES.md`](./_INFO_OAIAPI-IN57_CHAT_MESSAGES.md) OAIAPI-IN57
  - List messages for a chat completion; conversation history retrieval
  - Sources: OAIAPI-SC-OAI-CHTMSG

### Legacy APIs (3 files)

- [`_INFO_OAIAPI-IN58_LEGACY_ASSISTANTS.md`](./_INFO_OAIAPI-IN58_LEGACY_ASSISTANTS.md) OAIAPI-IN58
  - **[DEPRECATED sunset 2026-08-26]** Assistants API - assistants, threads, messages, runs, run steps, streaming; migration path to Responses + Conversations
  - Sources: OAIAPI-SC-OAI-LGASST

- [`_INFO_OAIAPI-IN59_LEGACY_COMPLETIONS.md`](./_INFO_OAIAPI-IN59_LEGACY_COMPLETIONS.md) OAIAPI-IN59
  - Legacy Completions API (POST /v1/completions); freeform prompt interface
  - Sources: OAIAPI-SC-OAI-LGCOMP

- [`_INFO_OAIAPI-IN60_LEGACY_REALTIME_BETA.md`](./_INFO_OAIAPI-IN60_LEGACY_REALTIME_BETA.md) OAIAPI-IN60
  - **[DEPRECATED sunset 2026-05-07]** Realtime Beta (legacy sessions, transcription sessions); migration to GA Realtime
  - Sources: OAIAPI-SC-OAI-LGRTBM

### Agents and Automation (4 files)

- [`_INFO_OAIAPI-IN63_CODE_GENERATION_CODEX.md`](./_INFO_OAIAPI-IN63_CODE_GENERATION_CODEX.md) OAIAPI-IN63
  - Code generation, Codex coding agent, GPT-5.2-Codex/gpt-5.1-codex-max/gpt-5-codex models, shell tool, IDE/CLI/CI-CD integration
  - Sources: OAIAPI-SC-OAI-GCODGN, OAIAPI-SC-OAI-GSHELL

- [`_INFO_OAIAPI-IN64_AGENTS_FRAMEWORK.md`](./_INFO_OAIAPI-IN64_AGENTS_FRAMEWORK.md) OAIAPI-IN64
  - Agents overview, building agents, deploying in products, optimization, Agents SDK (Python/TypeScript), multi-step tool use
  - Sources: OAIAPI-SC-OAI-GAGENT, OAIAPI-SC-GH-AGNTPY

- [`_INFO_OAIAPI-IN65_COMPUTER_USE.md`](./_INFO_OAIAPI-IN65_COMPUTER_USE.md) OAIAPI-IN65
  - **[PREVIEW]** Computer Use Agent (CUA), computer-use-preview model, browser automation, Playwright integration, screenshot-action loop
  - Sources: OAIAPI-SC-OAI-GCMPTU

- [`_INFO_OAIAPI-IN66_MCP_AND_CONNECTORS.md`](./_INFO_OAIAPI-IN66_MCP_AND_CONNECTORS.md) OAIAPI-IN66
  - Remote MCP server integration, connector setup, server_url/server_label config, MCP for ChatGPT apps, authentication
  - Sources: OAIAPI-SC-OAI-GMCP, OAIAPI-SC-OAI-GTOOLS

### Specialized Capabilities (4 files)

- [`_INFO_OAIAPI-IN67_DEEP_RESEARCH.md`](./_INFO_OAIAPI-IN67_DEEP_RESEARCH.md) OAIAPI-IN67
  - Deep research models (o3-deep-research, o4-mini-deep-research), background mode for long tasks, webhook integration, MCP for deep research
  - Sources: OAIAPI-SC-OAI-GDEEP

- [`_INFO_OAIAPI-IN68_FILE_INPUTS_VISION.md`](./_INFO_OAIAPI-IN68_FILE_INPUTS_VISION.md) OAIAPI-IN68
  - File inputs (PDF, images, documents), vision capabilities, multimodal input processing, supported file formats
  - Sources: OAIAPI-SC-OAI-GFILIN

- [`_INFO_OAIAPI-IN69_VOICE_AGENTS.md`](./_INFO_OAIAPI-IN69_VOICE_AGENTS.md) OAIAPI-IN69
  - Voice agent patterns, Realtime API usage for voice, SIP integration, dedicated IP ranges, voice agent architecture
  - Sources: OAIAPI-SC-OAI-GVOICE, OAIAPI-SC-OAI-GRTAPI

- [`_INFO_OAIAPI-IN70_WEBSOCKET_MODE.md`](./_INFO_OAIAPI-IN70_WEBSOCKET_MODE.md) OAIAPI-IN70
  - WebSocket mode for Responses API (alternative to SSE streaming), persistent connections, binary frames
  - Sources: OAIAPI-SC-OAI-GWSMOD

### Cross-Cutting Guides (6 files)

- [`_INFO_OAIAPI-IN61_PRODUCTION_BEST_PRACTICES.md`](./_INFO_OAIAPI-IN61_PRODUCTION_BEST_PRACTICES.md) OAIAPI-IN61
  - Production readiness, retry strategies, backoff, monitoring, organization setup, safety
  - Sources: OAIAPI-SC-OAI-GERROR, OAIAPI-SC-OAI-GRLMT

- [`_INFO_OAIAPI-IN62_CHANGELOG_DEPRECATIONS.md`](./_INFO_OAIAPI-IN62_CHANGELOG_DEPRECATIONS.md) OAIAPI-IN62
  - API changelog, model deprecation schedule, version history, breaking changes
  - Sources: OAIAPI-SC-OAI-GCHLOG, OAIAPI-SC-OAI-GDEPR

- [`_INFO_OAIAPI-IN71_PROMPT_CACHING.md`](./_INFO_OAIAPI-IN71_PROMPT_CACHING.md) OAIAPI-IN71
  - Automatic prompt caching, cached_tokens in usage, cache hit rates, pricing discount, monitoring
  - Sources: OAIAPI-SC-OAI-GPCACH

- [`_INFO_OAIAPI-IN72_BACKGROUND_FLEX_PROCESSING.md`](./_INFO_OAIAPI-IN72_BACKGROUND_FLEX_PROCESSING.md) OAIAPI-IN72
  - Background mode (async long-running requests, ~10 min data retention), flex processing (lower cost, lower priority), comparison with batch API
  - Sources: OAIAPI-SC-OAI-GBKGND, OAIAPI-SC-OAI-GFLEX

- [`_INFO_OAIAPI-IN73_SAFETY_DATA_PRIVACY.md`](./_INFO_OAIAPI-IN73_SAFETY_DATA_PRIVACY.md) OAIAPI-IN73
  - Safety best practices, content policies, data usage policies ("your data"), API data retention, opt-out
  - Sources: OAIAPI-SC-OAI-GSAFTY, OAIAPI-SC-OAI-GYDATA

- [`_INFO_OAIAPI-IN74_OPTIMIZATION_GUIDES.md`](./_INFO_OAIAPI-IN74_OPTIMIZATION_GUIDES.md) OAIAPI-IN74
  - Latency optimization, cost optimization, accuracy optimization, model selection optimization cycle
  - Sources: OAIAPI-SC-OAI-GOPTIM

## Topic Count

- **Total Topics**: 74
- **Core Documentation**: 5
- **Responses API**: 6
- **Tools and Function Calling**: 6
- **Audio**: 3
- **Media Generation**: 4
- **AI Core**: 3
- **Evaluation and Training**: 4
- **Processing**: 4
- **Vector Stores**: 3
- **Realtime API**: 4
- **Infrastructure**: 4
- **Administration**: 8
- **Chat Completions**: 3
- **Legacy APIs**: 3
- **Agents and Automation**: 4
- **Specialized Capabilities**: 4
- **Cross-Cutting Guides**: 6

## Feature Status Matrix

### Beta Features
- **ChatKit** (IN45) - Embeddable chat UI, sessions, threads, widgets. Beta since launch, API may change
- **Skills API** (IN17) - Reusable tool packages. Relatively new, limited third-party documentation

### Alpha Features
- **Graders API** (IN31) - Run and validate graders for evals. Alpha status, schema may change

### Preview Features
- **Computer Use** (IN65) - CUA with computer-use-preview model. Screenshot-action loop for browser automation. Preview model, expect breaking changes

### Deprecated (with sunset dates)
- **Assistants API** (IN58) - Sunset **2026-08-26**. Replace with Responses API + Conversations API. Migration guide available
- **Realtime Beta** (IN60) - Sunset **2026-05-07**. Replace with GA Realtime API. Migration guide for session/event differences
- **codex-mini-latest** - Removed **2026-02-12**. Legacy shell tool only worked with this model

### Key Limitations
- **Custom voices** (IN19) - Limited to eligible accounts only; requires consent recording + sample recording
- **Background mode** (IN72) - Retains response data for ~10 minutes only; must poll or use webhooks
- **Flex processing** (IN72) - Lower cost but lower priority; longer completion times, no SLA
- **Prompt caching** (IN71) - Automatic only (no manual cache control like Anthropic); cache eviction is opaque
- **Video generation** (IN23) - sora-2-pro has longer generation times; video editing features may have rate limit constraints
- **Deep research** (IN67) - Requests can take minutes; must use background mode; ~10 min data retention
- **WebSocket mode** (IN70) - Alternative to SSE; not all SDKs may support it equally

### Not Available (vs competitors)
- **No per-request safety settings** - Unlike Gemini (configurable HarmBlockThreshold per request), OpenAI uses moderation API separately
- **No manual cache control** - Unlike Anthropic (cache_control breakpoints with configurable TTL), OpenAI caching is fully automatic
- **No Google Search grounding** - OpenAI has web_search but no Google-specific grounding with citations metadata
- **No X Search** - Unlike Grok (real-time Twitter/X data), OpenAI web_search uses general web
- **No multi-agent orchestration API** - Unlike Grok (Multi-Agent Research), OpenAI agents are single-model (use Agents SDK for orchestration)
- **No deferred completions** - Unlike Grok (async with polling), OpenAI uses background mode + webhooks
- **No provisioned throughput API** - Unlike Grok (guaranteed capacity), OpenAI uses tier-based rate limits
- **No OpenAI-compatible endpoint** - Unlike Gemini (provides /v1/chat/completions compatibility layer), OpenAI IS the standard

## Topic Details

### Topic: Introduction
**Scope**: API overview, protocol, base URL, versioning, backwards compatibility, request/response debugging
**Contents**:
- Base URL: `https://api.openai.com/v1/`
- REST API version: `2020-10-01`
- Backwards compatibility policy
- X-Client-Request-Id header for client-side request tracking
- HTTP response headers (openai-organization, openai-processing-ms, openai-version, x-request-id)
**Sources**: OAIAPI-SC-OAI-OVERVIEW, OAIAPI-SC-OAI-GOVRVW
**Differences from other APIs**:
- Anthropic uses `anthropic-version` header for versioning; OpenAI uses fixed `2020-10-01` with backwards-compatible evolution
- Gemini uses API key in query param or header; OpenAI uses Bearer token only
- Grok is OpenAI-compatible (same endpoints)

### Topic: Authentication
**Scope**: API key types, authentication headers, multi-org/project routing
**Contents**:
- `Authorization: Bearer` header
- `OpenAI-Organization` header for org routing
- `OpenAI-Project` header for project routing
- Project-scoped API keys
- Legacy user API keys
**Sources**: OAIAPI-SC-OAI-OVERVIEW, OAIAPI-SC-OAI-ADMOVW
**Differences from other APIs**:
- Anthropic uses `x-api-key` header (not Bearer)
- Gemini uses `x-goog-api-key` header
- Grok uses `Authorization: Bearer` (OpenAI-compatible)
- OpenAI has most granular key scoping (org + project level)

### Topic: Models
**Scope**: Model families, capabilities, pricing, context windows, deprecation schedule
**Contents**:
- GPT-5.4 (flagship), GPT-5, GPT-5 mini, GPT-5 nano
- GPT-5.2-Codex, gpt-5.1-codex-max, gpt-5-codex (code generation)
- o4-mini, o3-pro (reasoning models)
- o3-deep-research, o4-mini-deep-research (deep research)
- gpt-image-1.5, gpt-image-1, gpt-image-1-mini (image generation)
- Sora, sora-2, sora-2-pro (video generation)
- Whisper, gpt-4o-mini-transcribe (audio)
- computer-use-preview (CUA)
- text-embedding-3-small/large (embeddings)
- omni-moderation-latest (moderation)
**Sources**: OAIAPI-SC-OAI-MODAPI, OAIAPI-SC-OAI-GMODLS, OAIAPI-SC-OAI-GPRICE
**Differences from other APIs**:
- Largest model ecosystem of all four APIs
- Only API with dedicated video generation models
- Only API with dedicated moderation models
- Only API with dedicated deep research models
- Only API with dedicated coding agent models (Codex family)

### Topic: Responses API
**Scope**: Primary text generation interface with tool support, conversations, and background mode
**Contents**:
- POST /v1/responses - create response with tools, instructions, conversation context
- GET /v1/responses/{id} - retrieve stored response
- DELETE /v1/responses/{id} - delete stored response
- POST /v1/responses/{id}/cancel - cancel in-progress response
- POST /v1/responses/{id}/compact - compact conversation context
- POST /v1/responses/input_tokens/count - pre-request token estimation
- Built-in tools: web_search, file_search, code_interpreter, tool_search, computer_use
- Background mode for long-running tasks
- previous_response_id for conversation chaining
**Sources**: OAIAPI-SC-OAI-RESOVW, OAIAPI-SC-OAI-RESCRT
**Differences from other APIs**:
- Anthropic Messages API: stateless, no stored responses, no background mode
- Gemini generateContent: similar but different parameter names, no response storage
- Grok: OpenAI-compatible /v1/responses endpoint
- Unique: Cancel, Compact, Count input tokens endpoints

### Topic: Conversations API
**Scope**: Persistent multi-turn conversation management, replacing Assistants threads
**Contents**:
- POST /v1/conversations - create
- GET /v1/conversations/{id} - retrieve
- POST /v1/conversations/{id} - update
- DELETE /v1/conversations/{id} - delete
- Items sub-resource: CRUD + list
**Sources**: OAIAPI-SC-OAI-CNVCRT, OAIAPI-SC-OAI-CNVGET
**Differences from other APIs**:
- Anthropic: no server-side conversation state (stateless)
- Gemini: no conversation management API
- Grok: no conversation management API
- Replaces deprecated Assistants API threads

### Topic: Skills API
**Scope**: Reusable tool packages with versioning
**Contents**:
- POST /v1/skills - create
- GET /v1/skills/{id} - retrieve
- POST /v1/skills/{id} - update
- DELETE /v1/skills/{id} - delete
- GET /v1/skills - list
- Versions sub-resource: CRUD + list
- Content retrieval
**Sources**: OAIAPI-SC-OAI-SKLAPI
**Differences from other APIs**:
- Anthropic has a Skills API (beta) with similar concept
- Gemini: no equivalent
- Grok: no equivalent
- OpenAI Skills work with tool_search built-in tool

### Topic: Vector Stores
**Scope**: Built-in RAG with file management, chunking, search
**Contents**:
- CRUD + List + Search
- File sub-resource: CRUD + List + Content
- File Batches: Create, Retrieve, List Files, Cancel
- Expiration policies
- Chunking strategies (auto, static)
- Integration with file_search tool
**Sources**: OAIAPI-SC-OAI-VSAPI, OAIAPI-SC-OAI-VSFIL, OAIAPI-SC-OAI-VSFBT
**Differences from other APIs**:
- Anthropic: no built-in vector stores
- Gemini: File Search Stores (similar concept, less mature)
- Grok: Collections API (simpler equivalent)
- OpenAI: most complete built-in RAG infrastructure

### Topic: Realtime API
**Scope**: WebSocket-based real-time voice/text streaming
**Contents**:
- WebSocket connection to wss://api.openai.com/v1/realtime
- Sessions and transcription sessions
- Calls API (create, retrieve, list)
- Client events and server events
- Voice activity detection
- Audio formats (pcm16, g711_ulaw, g711_alaw)
**Sources**: OAIAPI-SC-OAI-RTCLNT, OAIAPI-SC-OAI-RTCALL, OAIAPI-SC-OAI-GRTAPI
**Differences from other APIs**:
- Gemini: Live API (BidiGenerateContent) via WebSocket - true bidirectional
- Grok: Voice Agent API (similar WebSocket approach)
- Anthropic: no realtime API
- OpenAI: most mature with Calls sub-resource for lifecycle management

### Topic: Administration
**Scope**: Organization, project, user, group, role, certificate, audit, usage management
**Contents**:
- Organization: invites, audit logs, usage, costs, users, groups, roles, certificates
- Projects: CRUD + archive, users, groups, service accounts, API keys, rate limits, certificates, roles
- Custom roles with permissions
- mTLS certificates with activate/deactivate
- Audit log querying
- Usage and cost tracking per resource type
**Sources**: OAIAPI-SC-OAI-ADMOVW, OAIAPI-SC-OAI-ADMORG, OAIAPI-SC-OAI-ADMPRJ
**Differences from other APIs**:
- Most comprehensive admin API of all four providers
- Only API with mTLS certificate management
- Only API with audit logs endpoint
- Only API with custom role CRUD
- Anthropic: simpler org/workspace/user model
- Gemini: via Google Cloud IAM
- Grok: Management API (keys, ACLs, audit)

## Related APIs/Technologies

- **Anthropic API**
  - URL: https://docs.anthropic.com/en/docs/
  - Relation: Direct competitor, Messages API pattern, different auth (x-api-key), unique Extended Thinking

- **Google Gemini API**
  - URL: https://ai.google.dev/api
  - Relation: Direct competitor, generateContent pattern, OpenAI-compatible layer available, unique Google Search grounding

- **Grok API (xAI)**
  - URL: https://docs.x.ai
  - Relation: OpenAI SDK-compatible, uses same /v1/chat/completions and /v1/responses endpoints, unique X Search

- **Azure OpenAI**
  - URL: https://learn.microsoft.com/en-us/azure/ai-services/openai/
  - Relation: Same OpenAI models, different hosting/auth/endpoints, enterprise features, regional deployment

## Document History

**[2026-03-20 02:55]**
- Added: 12 new topics (IN63-IN74) covering code generation/Codex, agents framework, computer use, MCP/connectors, deep research, file inputs/vision, voice agents, WebSocket mode, prompt caching, background/flex processing, safety/data privacy, optimization guides
- Added: Feature Status Matrix with beta/alpha/preview/deprecated annotations and key limitations
- Added: "Not Available" comparison vs Anthropic, Gemini, Grok
- Changed: Topic count from 62 to 74 (18 categories)
- Changed: Existing topics annotated with [BETA], [ALPHA], [PREVIEW], [DEPRECATED] flags
- Changed: Models topic expanded with Codex family, sora-2-pro, computer-use-preview
- Changed: Prompt Engineering expanded with reusable prompts
- Changed: Evals expanded with prompt optimizer, external models
- Fixed: Missing sora-2-pro model in video generation
- Fixed: Missing custom voice eligibility limitation in TTS

**[2026-03-20 03:05]**
- Initial TOC created with 62 topics in 15 categories
- Full API structure mapped via Playwright sidebar extraction
- Topic details include cross-API differences for key sections
