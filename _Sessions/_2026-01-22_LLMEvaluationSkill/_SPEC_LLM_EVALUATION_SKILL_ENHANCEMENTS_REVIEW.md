# SPEC Review: LLM Evaluation Skill Enhancements

**Doc ID**: LLMEV-SP01-RV01
**Reviewed**: 2026-01-24 19:20
**Source**: `_SPEC_LLM_EVALUATION_SKILL_ENHANCEMENTS.md [LLMEV-SP01]`
**Focus**: API parameter accuracy, provider differences, research verification

## Critical Issues

### `LLMEV-RV-019` Reasoning Models Do NOT Support temperature/top_p

- **Location**: FR-01, entire SPEC
- **What**: SPEC proposes adding `--temperature` and `--top-p` but **reasoning models (o1, o3, o4, gpt-5 series) do NOT support these parameters at all**
- **Evidence**: Azure OpenAI docs: "The following are currently unsupported with reasoning models: temperature, top_p, presence_penalty, frequency_penalty, logprobs, top_logprobs, logit_bias, max_tokens"
- **Risk**: API will return 400 error: "Unsupported parameter: 'temperature' is not supported with this model"
- **Suggested fix**: 
  - Remove `--top-p` from SPEC entirely (user request)
  - Keep `--temperature` for backward compatibility with older models (gpt-4o, gpt-4.1-mini)
  - Add `--reasoning-effort` parameter for reasoning models (none, minimal, low, medium, high, xhigh)

### `LLMEV-RV-020` Missing reasoning_effort Parameter

- **Location**: Not in SPEC
- **What**: Reasoning models use `reasoning_effort` instead of temperature to control output
- **Evidence**: Azure docs: "reasoning_effort can be set to low, medium, or high for all reasoning models. GPT-5 models support minimal and none."
- **Values**:
  - `none` - No reasoning (gpt-5.1 default, fastest)
  - `minimal` - Minimal reasoning (gpt-5 only)
  - `low` - Low reasoning
  - `medium` - Medium reasoning (o-series default)
  - `high` - High reasoning (gpt-5-pro default and only option)
  - `xhigh` - Extreme reasoning (gpt-5.1-codex-max only)
- **Suggested fix**: Add `--reasoning-effort` parameter for reasoning models

### `LLMEV-RV-021` Output Length Parameter Complexity Not Addressed

- **Location**: FR-01
- **What**: SPEC proposes simple `--max-tokens` but reality is more complex:
  - **OpenAI Legacy** (gpt-4o): `max_tokens`
  - **OpenAI Reasoning** (o1, o3, o4): `max_completion_tokens` (Chat Completions API)
  - **OpenAI GPT-5** (Responses API): `max_output_tokens`
  - **Anthropic**: `max_tokens` (REQUIRED, fails without it)
- **Evidence**: OpenAI docs: "Reasoning models will only work with the max_completion_tokens parameter when using the Chat Completions API. Use max_output_tokens with the Responses API."
- **Suggested fix**: Implementation must detect model type and use correct parameter name internally

### `LLMEV-RV-022` Missing verbosity Parameter for GPT-5

- **Location**: Not in SPEC
- **What**: GPT-5 models have a new `verbosity` parameter (low/medium/high) that controls detail level
- **Evidence**: OpenAI docs: "verbosity accepts 'low', 'medium' (default), or 'high'. It influences detail level but not hard limits."
- **Note**: Only GPT-5 models (gpt-5.2, etc.). O-series and legacy models do not support it.
- **Suggested fix**: Consider adding `--verbosity` for GPT-5 models

### `LLMEV-RV-023` Anthropic Has effort Parameter (Beta)

- **Location**: Not in SPEC
- **What**: Anthropic Claude Opus 4.5 has an `effort` parameter similar to OpenAI's reasoning_effort
- **Evidence**: AWS Bedrock docs: "The effort parameter tells Claude how liberally it should spend tokens... can be set to high (default), medium, or low"
- **Note**: Requires beta header `effort-2025-11-24`
- **Suggested fix**: Consider adding `--effort` for Anthropic Opus 4.5

### `LLMEV-RV-011` Temperature Range Wrong for Anthropic

- **Location**: FR-01, line 96
- **What**: SPEC says `--temperature (float, 0.0-2.0)` but Anthropic only supports **0.0-1.0**
- **Evidence**: Anthropic docs quoted in GitHub discussion: "Ranges from 0.0 to 1.0"
- **Risk**: Passing temperature > 1.0 to Anthropic API will cause error or unexpected behavior
- **Suggested fix**: 
  - OpenAI: 0.0-2.0
  - Anthropic: 0.0-1.0
  - Implementation must clamp or warn when temperature > 1.0 for Anthropic

### `LLMEV-RV-012` Anthropic Has NO Seed Parameter

- **Location**: FR-01, DD-02, IG-02, EC-03
- **What**: SPEC correctly notes seed is OpenAI-only, but research confirms: **Anthropic has NO seed parameter at all**
- **Evidence**: Reddit thread: "Anthropic models don't have the transparency of OpenAI models... they do not support seed parameter"
- **Status**: SPEC is correct about this - DD-02 and IG-02 handle it properly

### `LLMEV-RV-013` OpenAI Seed is Beta and NOT Guaranteed

- **Location**: DD-01, Section 2 Context
- **What**: SPEC mentions seed reduces variability. Research confirms OpenAI docs say: "This feature is in Beta. If specified, our system will make a best effort... Determinism is not guaranteed"
- **Evidence**: OpenAI API Reference: "you should refer to the system_fingerprint response parameter to monitor changes in the backend"
- **Risk**: Users may expect reproducibility that isn't possible
- **Suggested fix**: Add `system_fingerprint` to metadata output for tracking backend changes

## High Priority

### `LLMEV-RV-014` Anthropic Has top_k, OpenAI Does Not

- **Location**: Not in SPEC
- **What**: Anthropic supports `top_k` parameter which OpenAI does not have
- **Evidence**: Anthropic docs: "top_k - Recommended for advanced use cases only"
- **Risk**: Missing parameter that advanced users might want
- **Suggested fix**: Consider adding `--top-k` (Anthropic only) or document explicitly as not supported

### `LLMEV-RV-015` Anthropic Says "Use temperature OR top_p, Not Both"

- **Location**: FR-01 (implies both can be used)
- **What**: Anthropic docs explicitly state: "You should either alter temperature or top_p, but not both"
- **Evidence**: Anthropic Messages API documentation
- **Risk**: Setting both may cause undefined behavior on Anthropic
- **Suggested fix**: Add warning if both --temperature and --top-p are set for Anthropic

### `LLMEV-RV-016` response_format Differences Not Documented

- **Location**: FR-02
- **What**: OpenAI supports `json_object` AND `json_schema` (Structured Outputs). SPEC only mentions `json_object`
- **Evidence**: OpenAI docs: "Setting to { \"type\": \"json_schema\", \"json_schema\": {...} } enables Structured Outputs"
- **Risk**: Missing more powerful structured output option
- **Suggested fix**: Consider supporting `--response-format json_schema` with schema file

## Medium Priority

### `LLMEV-RV-017` max_tokens vs max_completion_tokens

- **Location**: FR-01, Key Mechanisms
- **What**: SPEC mentions this in code but doesn't document which models use which parameter
- **Evidence**: OpenAI docs: "max_tokens is now deprecated in favor of max_completion_tokens, and is not compatible with o-series models"
- **Risk**: Wrong parameter for reasoning models (o1, o3, o4)
- **Suggested fix**: Document explicitly: gpt-5/o-series use `max_completion_tokens`, older models use `max_tokens`

### `LLMEV-RV-018` Anthropic "Not Fully Deterministic" Even at temp=0

- **Location**: MUST-NOT-FORGET (correct), but not reflected in all sections
- **What**: Anthropic docs explicitly state: "even with temperature of 0.0, the results will not be fully deterministic"
- **Evidence**: Quoted directly from Anthropic Messages API docs
- **Status**: MUST-NOT-FORGET captures this, good

## Industry Research Findings

### OpenAI API Parameters `[VERIFIED]`

- **seed**: Beta feature, integer, "best effort" determinism only
- **temperature**: 0.0-2.0
- **top_p**: 0.0-1.0, alternative to temperature
- **max_completion_tokens**: For gpt-5, o1, o3, o4 models
- **max_tokens**: Deprecated, for older models
- **response_format**: `text`, `json_object`, `json_schema`
- **system_fingerprint**: Returned in response, changes indicate backend updates

### Anthropic API Parameters `[VERIFIED]`

- **seed**: NOT SUPPORTED
- **temperature**: 0.0-1.0 only (NOT 0-2)
- **top_p**: Supported, but "use temperature OR top_p, not both"
- **top_k**: Supported (OpenAI doesn't have this)
- **max_tokens**: Required parameter (Anthropic fails without it)
- **Even temp=0 is not deterministic**: Explicitly documented

### Model-Specific Support (CORRECTED)

**Legacy Models (gpt-4o, gpt-4.1-mini, etc.)**:
- temperature: 0-2 ✓
- top_p: 0-1 ✓
- seed: Yes (beta) ✓
- max_tokens: Yes ✓

**Reasoning Models (o1, o3, o4, gpt-5 series)**:
- temperature: ❌ NOT SUPPORTED
- top_p: ❌ NOT SUPPORTED
- seed: Unknown
- max_tokens: ❌ Must use max_completion_tokens
- reasoning_effort: ✓ NEW (none/minimal/low/medium/high/xhigh)

**Anthropic Claude**:
- temperature: 0-1 only
- top_p: Yes, but "use temp OR top_p, not both"
- top_k: Yes (unique to Anthropic)
- seed: ❌ NOT SUPPORTED

## Recommendations

### Must Fix

- [ ] **Remove `--top-p` from SPEC** - Deprecated for reasoning models, user doesn't want it
- [ ] **Add `--reasoning-effort`** - Required for reasoning models (none/minimal/low/medium/high/xhigh)
- [ ] Change temperature: only for legacy models (gpt-4o, gpt-4.1-mini), error for reasoning models
- [ ] Change Anthropic temperature range: 0-1 only
- [ ] Add warning when both temperature AND top_p set for Anthropic

### Should Add

- [ ] Capture `system_fingerprint` from OpenAI responses in metadata
- [ ] Document `max_tokens` vs `max_completion_tokens` by model
- [ ] Consider `--top-k` parameter (Anthropic only)

### Consider

- [ ] Support `json_schema` response format with schema file
- [ ] Document model-specific parameter support in SKILL.md

## Document History

**[2026-01-24 19:35]**
- Added: LLMEV-RV-021 - Output length parameter complexity (max_tokens vs max_completion_tokens vs max_output_tokens)
- Added: LLMEV-RV-022 - GPT-5 verbosity parameter
- Added: LLMEV-RV-023 - Anthropic effort parameter (beta)

**[2026-01-24 19:30]**
- Added: LLMEV-RV-019 - Reasoning models do NOT support temperature/top_p
- Added: LLMEV-RV-020 - Missing reasoning_effort parameter
- Updated: Model-specific support table corrected
- Changed: Must Fix priorities based on user feedback

**[2026-01-24 19:20]**
- Initial review created
- Research verified API parameters against official documentation
- Found critical issue: temperature range differs by provider
