# Session: Z.AI Integration

**Topic ID**: ZAIINT
**Goal**: Integrate all Z.AI (GLM) models into model-registry.json, model-pricing.json, model-parameter-mapping.json, call-llm.py, call-llm-batch.py, test-call-llm.py, llm-evaluation-selftest.py, and update-model-registry.md

## Key Paths

- **Canonical JSONs**: `E:\Dev\IPPS\DevSystemV4.3\skills\llm-evaluation\`
- **API docs source**: `E:\Dev\KarstensWorkspace\knowledge\Zhipu\ZAI_API_2026-09-05\`
- **API keys**: `E:\Dev\.tools\.api-keys.txt` (key: `ZAI_API_KEY`)
- **Z.AI base URL**: `https://api.z.ai/api/paas/v4/`

## Z.AI API Key Facts

- OpenAI-compatible: use OpenAI SDK with base_url swap
- Z.AI-specific params via `extra_body`: `thinking`, `reasoning_effort`, `do_sample`, `tool_stream`
- `reasoning_content` in response is Z.AI-specific (thinking output)
- Context caching is implicit (50% discount on cached tokens)
- Forced thinking: GLM-5.3, GLM-5.3-Flash, GLM-4.7, GLM-4.5V (cannot disable)
- Auto-thinking: GLM-5.2, GLM-5.1, GLM-5, GLM-4.6, GLM-4.5
- reasoning_effort: GLM-5.3/5.3-Flash (max/high/low only), GLM-5.2 (7 levels with mappings)
- GLM-5.1 and below: no reasoning_effort support

## Model List (text + vision, chat completions only)

| Model ID | Context | Thinking | reasoning_effort | Input/1M | Cached/1M | Output/1M |
|---|---|---|---|---|---|---|
| glm-5.3 | 1M | forced | max/high/low | $1.40 | $0.26 | $4.40 |
| glm-5.3-flash | 1M | forced | max/high/low | $0.15 | $0.03 | $0.50 |
| glm-5.2 | 1M | auto | 7 levels | $1.40 | $0.26 | $4.40 |
| glm-5.1 | 1M | auto | none | $1.40 | $0.26 | $4.40 |
| glm-5 | 1M | auto | none | $1.00 | $0.20 | $3.20 |
| glm-4.7 | 128K | forced | none | $0.60 | $0.11 | $2.20 |
| glm-4.7-flashx | 128K | auto | none | $0.07 | $0.01 | $0.40 |
| glm-4.7-flash | 128K | auto | none | Free | Free | Free |
| glm-4.6 | 128K | auto | none | $0.60 | $0.11 | $2.20 |
| glm-4.6v | 128K | auto | none | $0.60 | $0.11 | $1.80 |
| glm-4.5v | 128K | forced | none | $0.60 | $0.11 | $1.80 |
| glm-4.5-x | 128K | auto | none | $2.20 | $0.45 | $8.90 |
| glm-4.5-flash | 200K | auto | none | Free | Free | Free |
| glm-4.5-airx | 128K | auto | none | $1.10 | $0.22 | $4.50 |
| glm-4.5 | 128K | auto | none | $0.60 | $0.11 | $2.20 |
| glm-4-air | 128K | auto | none | $0.20 | $0.03 | $1.10 |
| glm-4-32b-0414-128k | 128K | none | none | $0.10 | null | $0.10 |

## Method Mapping

- `zai_reasoning`: GLM-5.3, GLM-5.3-Flash, GLM-5.2 (thinking + reasoning_effort via extra_body)
- `zai_thinking`: GLM-5.1, GLM-5, GLM-4.7, GLM-4.6, GLM-4.5, GLM-4-air, GLM-4.6V, GLM-4.5V (thinking only via extra_body)
- `temperature`: GLM-4-32B (legacy, no thinking)

## Current Phase

**Phase**: EXPLORE
**Workflow**: /session-new + /write-strut
**Assessment**: Data gathered, ready to plan

## IMPORTANT: Cascade Agent Instructions

- DevSystem source is `DevSystemV4.3/`, sync target is `.devin/`
- API keys at `E:\Dev\.tools\.api-keys.txt`
- Z.AI is OpenAI-compatible: use OpenAI SDK with base_url swap
- Z.AI-specific params must go through `extra_body` in OpenAI SDK
- GLM-5.3-Flash has 50% promo pricing until Sep 9, 2026 - use list prices in pricing JSON
- Prefix ordering in model_id_startswith: most specific first (glm-5.3-flash before glm-5.3 before glm-5)
