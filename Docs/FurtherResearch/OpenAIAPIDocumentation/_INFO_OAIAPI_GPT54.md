# INFO: OpenAI API - GPT-5.4 Model Guide

**Doc ID**: OAIAPI-IN63
**Goal**: Document GPT-5.4 model capabilities, parameters, and usage patterns
**Version scope**: API v1, Documentation date 2026-03-12

**Depends on:**
- `__OAIAPI_SOURCES.md [OAIAPI-IN01]` for source references

## Summary

GPT-5.4 is OpenAI's latest flagship model, specifically designed for coding and agentic tasks. It is a reasoning model that breaks problems down step-by-step, producing an internal chain of thought. GPT-5.4 supports five reasoning effort levels (none, low, medium, high, xhigh), with xhigh being new to this model. It powers Codex and Codex CLI and has a knowledge cutoff of August 2025. The model works best with the Responses API and supports all standard tools including function calling, structured outputs, and streaming.

## Key Facts

- **Model ID**: `gpt-5.4` [VERIFIED]
- **Knowledge cutoff**: August 2025 [VERIFIED]
- **Reasoning efforts**: none (default), low, medium, high, xhigh [VERIFIED]
- **Best for**: Coding, agentic tasks, long-horizon workflows [VERIFIED]
- **API**: Responses API recommended, Chat Completions supported [VERIFIED]

## Reasoning Effort Levels

- `none` - Default. Fast, cost-sensitive tasks. No internal reasoning.
- `low` - Latency-sensitive tasks with complex instructions.
- `medium` - Tasks requiring stronger reasoning, balanced cost/latency.
- `high` - Research-heavy, multi-document synthesis.
- `xhigh` - Long, agentic, reasoning-heavy tasks. Maximum intelligence.

## Comparison with Other Models

- **vs GPT-5.3-Codex**: GPT-5.3-Codex is coding-only; GPT-5.4 handles both coding and general tasks
- **vs GPT-5.2**: GPT-5.4 adds xhigh reasoning effort
- **vs GPT-4.1/4o**: Migration recommended with `reasoning_effort: none` start

## Quick Reference

### Basic Request (Responses API)

```bash
curl --request POST \
  --url https://api.openai.com/v1/responses \
  --header "Authorization: Bearer $OPENAI_API_KEY" \
  --header "Content-type: application/json" \
  --data '{
    "model": "gpt-5.4",
    "input": "Your prompt here"
  }'
```

### With Reasoning Effort

```bash
curl --request POST \
  --url https://api.openai.com/v1/responses \
  --header "Authorization: Bearer $OPENAI_API_KEY" \
  --header "Content-type: application/json" \
  --data '{
    "model": "gpt-5.4",
    "input": "Complex reasoning task",
    "reasoning": {
      "effort": "high"
    }
  }'
```

### With Custom Tool

```bash
curl --request POST \
  --url https://api.openai.com/v1/responses \
  --header "Authorization: Bearer $OPENAI_API_KEY" \
  --header "Content-type: application/json" \
  --data '{
    "model": "gpt-5.4",
    "input": "Use the code_exec tool to calculate...",
    "tools": [{
      "type": "custom",
      "name": "code_exec",
      "description": "Executes arbitrary python code"
    }]
  }'
```

## Reasoning Model Best Practices

- Pass `previous_response_id` in multi-turn conversations to avoid re-reasoning
- Include reasoning items when using tools (extra round trips)
- Start with lower reasoning effort, increase only if evals show benefit
- Use prompt optimizer in dashboard for GPT-5.4 specific tuning

## ChatGPT Integration

In ChatGPT, three models use GPT-5.4:
- **GPT-5 Instant** - Fast responses
- **GPT-5 Thinking** - With reasoning
- **GPT-5 Pro** - Maximum capability

A routing layer selects the best model based on the question.

## Migration Guide

| From | Start With | Notes |
|------|------------|-------|
| gpt-5.2 | Match current reasoning | Preserve latency/quality first |
| gpt-5.3-codex | Match current reasoning | Keep same for coding |
| gpt-4.1/gpt-4o | none | Increase only if evals regress |
| Research assistants | medium/high | Add research multi-pass |
| Long-horizon agents | medium/high | Add tool persistence |

## Gotchas and Quirks

- Default reasoning effort is `none` (unlike earlier models)
- xhigh has significant latency/cost tradeoff
- Reasoning items should be passed back in multi-turn for best results
- Works in both Responses API and Chat Completions

## Related Endpoints

- `_INFO_OAIAPI_PROMPT_GUIDANCE.md` - Detailed prompting patterns
- `_INFO_OAIAPI_RESPONSES.md` - Responses API usage
- `_INFO_OAIAPI_MODELS.md` - Models API

## Sources

- `OAIAPI-IN01-SC-DEV-GPT54` - https://developers.openai.com/api/docs/guides/latest-model [2026-03-12]

## Document History

**[2026-03-12 21:18]**
- Initial documentation created from new GPT-5.4 guide
