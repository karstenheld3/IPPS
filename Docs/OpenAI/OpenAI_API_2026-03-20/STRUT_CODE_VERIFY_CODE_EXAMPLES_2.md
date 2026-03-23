# STRUT: SDK Code Example Verification v2

**Doc ID**: OAIAPI-STRUT-CV2
**Goal**: Verify all 423 Python code examples against openai SDK v2.29.0 source files; keep originals, add corrected SDK examples
**SDK version**: openai v2.29.0
**SDK path**: `E:\Dev\.tools\llm-venv\Lib\site-packages\openai\`

## MUST-NOT-FORGET

- KEEP original code examples from API docs unchanged
- ADD corrected examples as separate code blocks below original
- Note SDK source file path and version in each correction
- Only fix verified discrepancies (WRONG_PARAM and METHOD_NOT_FOUND with known correct path)
- REST-only endpoints (no SDK method): add note, do NOT invent SDK code
- Update Document History in each modified file

## Verification Results Summary

**Script**: `.tmp_verify_sdk.py` (AST-based source parsing)
**Stats**: 79 files, 423 blocks, 526 client calls, 444 OK, 82 issues

## Issue Inventory

### WRONG_PARAM (25 occurrences, 7 patterns)

- **WP-1**: `conversation_id` → `conversation` in `responses.create` (6 locs: IN08:263,319; IN11:284x2; IN16:252x2)
  - SDK file: `resources/responses/responses.py`
- **WP-2**: `duration/aspect_ratio/resolution/frame_rate` → `seconds/size` in `videos.create` (7 locs: IN22:162,224,273,327,381x2,440)
  - SDK file: `resources/videos.py`
- **WP-3**: `name/functions/description/version` → `files` in `skills.create` (5 locs: IN17:151,189,259,303x2)
  - SDK file: `resources/skills/skills.py`
- **WP-4**: `dataset_id/model/metric/config` → `data_source/eval_id` in `evals.runs.create` (5 locs: IN25:255,332,366,430,480)
  - SDK file: `resources/evals/runs/runs.py`
- **WP-5**: direct params → `sdp/session` in `realtime.calls.create` (2 locs: IN42:192; IN69:177)
  - SDK file: `resources/realtime/calls.py`
- **WP-6**: `prompt_id` not real param in `chat.completions.create` (1 loc: IN24:91)
  - SDK file: `resources/chat/completions/completions.py`
- **WP-7**: `role/content` → `items/include` in `conversations.items.create` (1 loc: IN08:263)
  - SDK file: `resources/conversations/items.py`

### METHOD_NOT_FOUND with correct SDK path (10 unique, fixable)

- **MF-1**: `client.chatkit.*` → `client.beta.chatkit.*` (4 locs: IN45:167,185,203x2)
- **MF-2**: `client.graders.run/validate` → `client.fine_tuning.alpha.graders.run/validate` (3 locs: IN31)
- **MF-3**: `client.realtime.sessions.create` → `client.beta.realtime.sessions.create` (3 locs: IN39,IN60,IN70)

### METHOD_NOT_FOUND - REST only, no SDK equivalent (24 unique)

- **MF-REST**: `client.organization.*` (20 locs: IN47-IN54) - Admin API uses REST only
- **MF-REST**: `client.codex.*` (2 locs: IN63) - Codex not in SDK
- **MF-REST**: `client.evals.datasets.create` (2 locs: IN25) - Not in SDK
- **MF-REST**: `client.realtime.calls.list` (2 locs: IN42) - Not in SDK
- **MF-REST**: `client.call_with_backoff` (1 loc) - Invented method

### FALSE POSITIVE (1)

- `client.beta.threads.runs.steps.list` - EXISTS in SDK (mixin pattern, AST missed it)

## Plan

[x] P1 [FIX]: WRONG_PARAM corrections (highest impact, 25 fixes)
├─ Objectives:
│   └─ [x] All WRONG_PARAM examples have corrected SDK companion ← P1-D1
├─ Strategy: Fix by file, largest first. Read SDK source, add corrected block after original
├─ [x] P1-S1 [FIX](IN22 - videos.create: duration→seconds, aspect_ratio→size) 7 locs - ALREADY HAD SDK companions
├─ [x] P1-S2 [FIX](IN08 - responses.create: conversation_id→conversation; items.create params) 3 locs
├─ [x] P1-S3 [FIX](IN11 - responses.create: conversation_id→conversation) 2 locs
├─ [x] P1-S4 [FIX](IN16 - responses.create: conversation_id→conversation) 2 locs
├─ [x] P1-S5 [FIX](IN25 - evals.runs.create params) 5 locs - ALREADY HAD SDK companions
├─ [x] P1-S6 [FIX](IN17 - skills.create params) 5 locs
├─ [x] P1-S7 [FIX](IN42 - realtime.calls.create params) 1 loc
├─ [x] P1-S8 [FIX](IN69 - realtime.calls.create params) 1 loc
├─ [x] P1-S9 [FIX](IN24 - chat.completions.create prompt_id) 1 loc
├─ Deliverables:
│   └─ [x] P1-D1: All 25 WRONG_PARAM occurrences have SDK-correct companion examples
└─> Transitions:
    - P1-D1 checked → P2 [FIX-PATHS]

[x] P2 [FIX-PATHS]: METHOD_NOT_FOUND with known correct path (10 fixes)
├─ Objectives:
│   └─ [x] All fixable METHOD_NOT_FOUND have corrected SDK companion ← P2-D1
├─ Strategy: Add corrected examples using actual SDK paths
├─ [x] P2-S1 [FIX](IN45 - chatkit → beta.chatkit) 4 locs
├─ [x] P2-S2 [FIX](IN31 - graders → fine_tuning.alpha.graders) 3 locs
├─ [x] P2-S3 [FIX](IN39,IN60,IN70 - realtime.sessions → realtime.client_secrets) 3 locs
├─ Deliverables:
│   └─ [x] P2-D1: All 10 fixable METHOD_NOT_FOUND corrected
└─> Transitions:
    - P2-D1 checked → P3 [ANNOTATE]

[x] P3 [ANNOTATE]: REST-only endpoint notes (24 methods)
├─ Objectives:
│   └─ [x] All REST-only examples have SDK availability note ← P3-D1
├─ Strategy: Add brief note under each REST-only example
├─ [x] P3-S1 [ANNOTATE](IN47-IN54 - organization admin endpoints) 20 locs
├─ [x] P3-S2 [ANNOTATE](IN63 - codex) 2 locs
├─ [x] P3-S3 [ANNOTATE](IN25 - evals.datasets.create) 2 locs - ALREADY HAD NOTE from previous pass
├─ [x] P3-S4 [ANNOTATE](IN42 - realtime.calls.list) 2 locs - annotated in P1-S7 fix
├─ Deliverables:
│   └─ [x] P3-D1: All REST-only examples annotated
└─> Transitions:
    - P3-D1 checked → [END]

## Document History

**[2026-03-21 09:50]**
- Completed: All P1 (WRONG_PARAM), P2 (METHOD_NOT_FOUND), P3 (REST-only) phases
- 18 files modified, 82 issues addressed

**[2026-03-21 09:10]**
- Initial STRUT plan created from verification results
