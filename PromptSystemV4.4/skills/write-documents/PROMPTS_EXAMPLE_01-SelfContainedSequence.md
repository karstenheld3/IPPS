# Prompts Example 01: Self-Contained Sequence

Demonstrates a 3-prompt self-contained sequence for a generic API module setup task.

## Context

This example shows how to write a prompt sequence where each prompt is self-contained: it carries its own context-loading directive, treats earlier conversation as compacted, and names its dependencies by file path. The sequence is anchored by a STRUT planning document and uses context cards for shared state.

The task: create a generic REST API module with user endpoints. Three prompts cover analysis, implementation, and testing. The sequence stays under 6 steps (PRMT-SC-04) and uses `effort: high` in frontmatter, so fewer prompts are needed.

## Document

`````markdown
---
intended_model: claude-sonnet-4-5
context_window_size: 200k
effort: high
prompt_system: IPPS
---

<!-- Planning document: __STRUT_SetupApiModule.md, phases P1-P3
Each prompt implements one phase of the STRUT plan.
Read the STRUT plan and __CARD_00-Rules.md before starting each prompt. -->

## Prompt 1 - Analyze API requirements

<!-- P1 [ANALYZE]: Read requirements and design the API module structure -->

```
Read `__CARD_00-Rules.md` and `__STRUT_SetupApiModule.md` step P1-S1. Treat earlier conversation as compacted. Step P1-S1.
Planning document: `__STRUT_SetupApiModule.md`, step P1-S1.

Analyze the requirements for a generic REST API module with user endpoints (GET /users, POST /users, GET /users/:id, PUT /users/:id, DELETE /users/:id). Write the API design to `_INFO_ApiDesign.md` including: endpoint list, request/response schemas, error codes, and data model.

Constraints:
- Do not write any implementation code in this step
- Do not modify existing project configuration files
- Re-running this prompt must not corrupt state or waste cost: if `_INFO_ApiDesign.md` already exists and contains the endpoint list, skip

Verify: `_INFO_ApiDesign.md` exists with sections for endpoints, schemas, error codes, and data model.
```

---

## Prompt 2 - Implement API module

<!-- P2 [IMPLEMENT]: Create the API module based on the design from P1 -->

```
Read `__CARD_00-Rules.md`, `__STRUT_SetupApiModule.md` step P2-S1, and `_INFO_ApiDesign.md` section 1. Treat earlier conversation as compacted. Step P2-S1.
Planning document: `__STRUT_SetupApiModule.md`, step P2-S1.

Implement the REST API module in `src/modules/users/` based on the design in `_INFO_ApiDesign.md` section 1. Create the route handlers, validation middleware, and error handling. Write the implementation to `src/modules/users/routes.ts` and `src/modules/users/validator.ts`.

Constraints:
- Do not modify files outside `src/modules/users/`
- Do not add new npm dependencies
- Follow the existing project patterns in `src/modules/`
- Re-running this prompt must not corrupt state or waste cost: if `src/modules/users/routes.ts` already exists and passes type checking, skip

Verify: `src/modules/users/routes.ts` and `src/modules/users/validator.ts` exist. Run `npx tsc --noEmit`. No type errors.
```

---

## Prompt 3 - Write and run tests

<!-- P3 [TEST]: Write integration tests for the API module and run them -->

```
Read `__CARD_00-Rules.md`, `__STRUT_SetupApiModule.md` step P3-S1, `_INFO_ApiDesign.md` section 2, and `src/modules/users/routes.ts`. Treat earlier conversation as compacted. Step P3-S1.
Planning document: `__STRUT_SetupApiModule.md`, step P3-S1.

Write integration tests for the user API endpoints in `tests/modules/users.test.ts`. Cover: valid request for each endpoint, invalid input validation, not found cases, and error response format. Run the test suite after writing.

Constraints:
- Do not modify the implementation files in `src/modules/users/`
- Do not modify existing test files
- Use the existing test framework and patterns in `tests/`
- Re-running this prompt must not corrupt state or waste cost: if `tests/modules/users.test.ts` already exists and tests pass, skip

Verify: Run `npx jest tests/modules/users.test.ts`. All tests pass. Test file covers all 5 endpoints with success and error cases.
```
`````

## Key Decisions

- **3 prompts at high effort instead of 6 at low effort**: The effort level in frontmatter is `high`, so each prompt can handle a broader scope. Analysis, implementation, and testing each fit one prompt at this effort level. At low effort, each would need 2 prompts (PRMT-SC-05).
- **STRUT planning document as anchor**: Every prompt references `__STRUT_SetupApiModule.md` by filename and step ID. This enables progress tracking and resume after context reset (PRMT-SC-06).
- **Context card for shared rules**: `__CARD_00-Rules.md` is read at the start of every prompt. This avoids repeating standing rules in each prompt body and keeps prompt density under 8 instructions (PRMT-ST-05).
- **Design document as inter-prompt dependency**: Prompt 2 and 3 reference `_INFO_ApiDesign.md` by filename and section, not "the previous step". This satisfies the no-conversation-dependency rule (PRMT-SC-02).
- **Idempotency constraints in implementation prompts**: Prompts 2 and 3 include "if the output file already exists and passes validation, skip" as idempotency constraints. Prompt 1 is an analysis prompt (no file modifications beyond writing a design doc) but still includes idempotency for the design file (PRMT-SC-03).
- **5-backtick outer fence**: The document uses 5 backticks for the outer fence because the inner prompts use 3-backtick fences. This satisfies PRMT-FT-02 (outer exceeds deepest inner).
