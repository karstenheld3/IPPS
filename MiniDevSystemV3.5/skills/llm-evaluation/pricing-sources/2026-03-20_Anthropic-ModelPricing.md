<DevSystem MarkdownTablesAllowed=true />

# Anthropic Pricing Data - 2026-03-20

## Sources

- **Primary**: https://platform.claude.com/docs/en/about-claude/pricing
- **Screenshots**: Captured 2026-03-20 from Claude API Docs (3 screenshots covering model pricing, tools, agent examples)

## Model Pricing (per 1M tokens)

| Model                       | Context | Input   | Cache Write | Cache Read | Output  |
|-----------------------------|---------|---------|-------------|------------|---------|
| Claude Opus 4.6             | 200K    | $15.00  | $18.75      | $1.50      | $75.00  |
| Claude Opus 4.5             | 200K    | $15.00  | $18.75      | $1.50      | $75.00  |
| Claude Opus 4.1             | 200K    | $15.00  | $18.75      | $1.50      | $75.00  |
| Claude Opus 4               | 200K    | $15.00  | $18.75      | $1.50      | $75.00  |
| Claude Sonnet 4.6           | 200K    | $3.00   | $3.75       | $0.30      | $15.00  |
| Claude Sonnet 4.5           | 200K    | $3.00   | $3.75       | $0.30      | $15.00  |
| Claude Sonnet 4             | 200K    | $3.00   | $3.75       | $0.30      | $15.00  |
| Claude Sonnet 3.7 (dep.)    | 200K    | $3.00   | $3.75       | $0.30      | $15.00  |
| Claude Haiku 4.5            | 200K    | $1.00   | $1.25       | $0.10      | $5.00   |
| Claude Haiku 3.5            | 200K    | $0.80   | $1.00       | $0.08      | $4.00   |
| Claude 3 Opus (dep.)        | 200K    | $15.00  | $18.75      | $1.50      | $75.00  |
| Claude 3 Haiku              | 200K    | $0.25   | $0.30       | $0.03      | $1.25   |

MTok = Million tokens. All prices USD.

## Prompt Caching

Cache multipliers: 5-min write = 1.25x base input, 1-hour write = 2x base input, cache hit = 0.1x base input. Pays off after 1 read (5-min) or 2 reads (1-hour). Multipliers stack with Batch API, long context, and data residency.

Two modes: **Automatic** (`cache_control` at top level, recommended) or **Explicit breakpoints** (per content block).

## Batch Processing (50% discount)

| Model             | Batch Input | Batch Output |
|-------------------|-------------|--------------|
| Claude Opus 4.6   | $7.50/MTok  | $37.50/MTok  |
| Claude Opus 4.5   | $7.50/MTok  | $37.50/MTok  |
| Claude Opus 4     | $7.50/MTok  | $37.50/MTok  |
| Claude Sonnet 4.5 | $1.50/MTok  | $7.50/MTok   |
| Claude Haiku 4.5  | $0.50/MTok  | $2.50/MTok   |
| Claude Haiku 3    | $0.125/MTok | $0.625/MTok  |

## Long Context Pricing

Context >200K triggers 2x standard rates. Threshold based solely on input tokens (including cache reads).

| Model             | Context   | >200K Input  | >200K Output  |
|-------------------|-----------|--------------|---------------|
| Claude Opus 4.5   | up to 1M  | $30.00/MTok  | $150.00/MTok  |
| Claude Sonnet 4.5 | up to 1M  | $6.00/MTok   | $30.00/MTok   |

Batch 50% discount and caching multipliers apply on top of long context pricing.

## Tool Use Pricing

Priced on: total input tokens (including `tools` param) + output tokens + server-side tool usage fees.

| Model                    | Tool Choice | System Prompt Tokens |
|--------------------------|-------------|----------------------|
| Claude Opus 4.6          | auto, none  | 3K tokens            |
| Claude Opus 4.5          | auto, none  | 3K tokens            |
| Claude Opus 4.1          | auto, text  | 3K tokens            |
| Claude Opus 4            | auto, text  | 3K tokens            |
| Claude Sonnet 4.6        | auto, none  | 3K tokens            |
| Claude Sonnet 4.5        | auto, none  | 3K tokens            |
| Claude Sonnet 4          | auto, none  | 3K tokens            |
| Claude Sonnet 3.7 (dep.) | auto, none  | 3K tokens            |
| Claude Haiku 4.5         | auto, none  | 24K tokens           |
| Claude Haiku 3.5         | auto, none  | 3K tokens            |

## Bash Tool

Adds 245 input tokens. Additional tokens from command outputs, errors, file contents.

## Code Execution Tool

**Free** when used with `web_search_20250305` or `web_fetch_preview`. Otherwise billed by execution time (5-min minimum). 1,500 free hours/month/org, then $0.05/hour/container. Files written = time billed even if tool unused.

## Text Editor Tool

| Tool                 | Additional Input Tokens |
|----------------------|-------------------------|
| text_editor_20250429 | 722 tokens              |
| text_editor_20250124 | 700 tokens              |

## Web Search Tool

**$10 per 1,000 searches** + standard token costs. Search results count as input tokens. Not billed on error.

## Web Fetch Tool

**No additional charges** beyond standard token costs. Use `max_content_tokens` to limit size.

Typical content: web page ~10K tokens, large docs 70-100K, research PDF ~125K tokens.

## Computer Use Tool

System prompt overhead: 466-499 tokens. Tool definition: 735 tokens (Claude 4.x and Sonnet 3.7). Screenshots use Vision pricing.

## Agent Pricing Examples

- **Customer support**: ~3,700 tokens/conversation, ~$7,000 for 10,000 tickets (Opus 4.5)
- **General agent workflow**: ~$0.02/request + ~$0.05/retrieval + ~$0.04/action

## Cost Optimization

1. Use appropriate models (Haiku for simple, Sonnet for complex)
2. Implement prompt caching for repeated context
3. Batch API for non-time-sensitive tasks
4. Monitor token consumption

## Rate Limits

Tier 1 (entry) through Tier 4 (max standard), plus Enterprise (custom). Volume discounts negotiated case-by-case.

## Billing

Monthly usage-based, USD, credit card or invoicing. Usage tracking in Claude Console.

## FAQ

- ~1 token = 4 chars / 0.75 words English
- Free credits for new users; contact sales for extended trials
- Batch + caching discounts combine
- Credit cards for standard; invoicing for enterprise