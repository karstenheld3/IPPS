# Claude Model ID Reference

Format: `{model-family}-{version}-{YYYYMMDD}`. Date suffix is the release date, NOT a predictable pattern.

## Common Mistakes

- Using wrong dates (e.g., `20250514` for Opus 4.5 when correct is `20251101`)
- Aliases without dates (e.g., `claude-opus-4-5`) may not work via direct API
- Date patterns from other models do NOT apply universally

## Verified Model IDs (2026-01-25)

Claude 4.5: `claude-opus-4-5-20251101`, `claude-sonnet-4-5-20250929`, `claude-haiku-4-5-20251001`
Claude 4: `claude-opus-4-20250514`, `claude-sonnet-4-20250514`
Claude 3.x: `claude-3-7-sonnet-20250219`, `claude-3-5-haiku-20241022`

## Wrong IDs That Return 404

- Opus 4.5: `claude-opus-4-5-20250929`, `claude-opus-4-5-20251022` → correct: `claude-opus-4-5-20251101`
- Haiku 4.5: `claude-haiku-4-5-20250514`, `claude-haiku-4-5-20251022` → correct: `claude-haiku-4-5-20251001`

## How to Find Correct Model IDs

1. Check third-party docs (OpenRouter, TypingMind, AI/ML API)
2. Search `"claude-{model}-{version}"` with release announcements

## Sources

- https://docs.aimlapi.com/api-references/text-models-llm/anthropic/claude-4.5-opus
- https://www.typingmind.com/guide/anthropic/claude-haiku-4-5-20251001
- https://milvus.io/ai-quick-reference/how-do-i-call-claude-opus-45-via-the-claude-api