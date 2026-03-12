# INFO: OpenAI API - Prompt Guidance for GPT-5.4

**Doc ID**: OAIAPI-IN64
**Goal**: Document GPT-5.4 prompting patterns, reasoning effort selection, and migration strategies
**Version scope**: API v1, Documentation date 2026-03-12

**Depends on:**
- `__OAIAPI_SOURCES.md [OAIAPI-IN01]` for source references
- `_INFO_OAIAPI_GPT54.md [OAIAPI-IN63]` for model overview

## Summary

GPT-5.4 prompting requires careful selection of reasoning effort levels and explicit prompt contracts. The model performs best when prompts clearly specify output formats, verification steps, and completion criteria. Key patterns include completeness contracts, verification loops, tool persistence rules, and research mode blocks. Most teams should default to none, low, or medium reasoning effort, reserving high/xhigh for genuinely complex tasks.

## Key Facts

- **Reasoning effort selection**: Match to task complexity, not by default [VERIFIED]
- **Prompt contracts**: Explicit output formats improve reliability [VERIFIED]
- **Migration approach**: One change at a time, pin reasoning effort, run evals [VERIFIED]
- **Research mode**: Multi-pass with citation gating for research tasks [VERIFIED]

## Reasoning Effort Selection Guide

### Recommended Defaults

- `none` - Fast, cost-sensitive, latency-sensitive tasks where model does not need to think
- `low` - Latency-sensitive with complex instructions, small accuracy gain needed
- `medium` or `high` - Tasks requiring stronger reasoning, can absorb latency/cost
- `xhigh` - Avoid as default; only for long, agentic, reasoning-heavy tasks

### Starting Points by Task Type

**Execution-heavy workloads** (start with `none`):
- Workflow steps
- Field extraction
- Support triage
- Short structured transforms

**Research-heavy workloads** (start with `medium` or higher):
- Long-context synthesis
- Multi-document review
- Conflict resolution
- Strategy writing

## Prompt Contract Patterns

### Completeness Contract

```xml
<completeness_contract>
- Define what "done" means explicitly
- List all required output sections
- Specify validation criteria
</completeness_contract>
```

### Verification Loop

```xml
<verification_loop>
- After generating output, verify against requirements
- Check for missing elements
- Validate format compliance
</verification_loop>
```

### Tool Persistence Rules

```xml
<tool_persistence_rules>
- Continue using tools until task is complete
- Do not stop at first partial result
- Retry failed tool calls with adjusted parameters
</tool_persistence_rules>
```

### Initiative Nudge (before raising reasoning effort)

```xml
<dig_deeper_nudge>
- Don't stop at the first plausible answer.
- Look for second-order issues, edge cases, and missing constraints.
- If the task is safety or accuracy critical, perform at least one verification step.
</dig_deeper_nudge>
```

## Research Mode Pattern

For research agents, add these before increasing reasoning effort:

```xml
<research_mode>
- Perform multi-pass research
- Gather evidence from multiple sources
- Synthesize findings before concluding
</research_mode>

<citation_rules>
- Cite sources for all factual claims
- Use consistent citation format
- Verify citations before including
</citation_rules>

<empty_result_recovery>
- If search returns empty, try alternative queries
- Broaden search terms if too specific
- Report gaps explicitly
</empty_result_recovery>
```

## Migration Strategy

### One Change at a Time

1. Switch model first (keep everything else same)
2. Pin `reasoning_effort` to match current behavior
3. Run evals
4. Iterate on prompts
5. Adjust reasoning effort last

### Migration Starting Points

| Current Setup | Suggested GPT-5.4 Start | Notes |
|---------------|-------------------------|-------|
| gpt-5.2 | Match reasoning effort | Preserve profile first |
| gpt-5.3-codex | Match reasoning effort | Keep same for coding |
| gpt-4.1 or gpt-4o | `none` | Keep snappy, increase if regress |
| Research assistants | `medium` or `high` | Add research multi-pass |
| Long-horizon agents | `medium` or `high` | Add tool persistence |

## Web Search and Deep Research

For research agent migration:

1. Add `<research_mode>` block
2. Add `<citation_rules>` block
3. Add `<empty_result_recovery>` block
4. Increase `reasoning_effort` one notch only after prompt fixes

GPT-5.4 excels at:
- Multi-step evidence gathering
- Long-context synthesis
- Explicit prompt contracts

## Gotchas and Quirks

- Stronger prompts often recover performance without raising reasoning effort
- Output contracts and verification loops are high-leverage changes
- Tool persistence rules prevent premature stopping
- Citation gating improves research accuracy

## Related Endpoints

- `_INFO_OAIAPI_GPT54.md` - GPT-5.4 model overview
- `_INFO_OAIAPI_RESPONSES.md` - Responses API usage

## Sources

- `OAIAPI-IN01-SC-DEV-PROMPT` - https://developers.openai.com/api/docs/guides/prompt-guidance [2026-03-12]

## Document History

**[2026-03-12 21:18]**
- Initial documentation created from new Prompt Guidance page
