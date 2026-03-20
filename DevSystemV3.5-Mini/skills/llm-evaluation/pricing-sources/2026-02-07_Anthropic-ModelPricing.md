<transcription_page_header> Claude API Docs | Pricing </transcription_page_header>

# Pricing

All prices are in USD. For the most current pricing information, please visit claude.com/pricing.

## Model pricing

<transcription_table>
Model pricing

| Model | Base Input Tokens | 5m Cache Writes | 1h Cache Writes | Cache Hits & Refreshes | Output Tokens |
|-------|-------------------:|----------------:|----------------:|-----------------------:|--------------:|
| Claude Opus 4.6 | $5 / MTok | $6.25 / MTok | $10 / MTok | $0.50 / MTok | $25 / MTok |
| Claude Opus 4.5 | $5 / MTok | $6.25 / MTok | $10 / MTok | $0.50 / MTok | $25 / MTok |
| Claude Opus 4.1 | $15 / MTok | $18.75 / MTok | $30 / MTok | $1.50 / MTok | $75 / MTok |
| Claude Opus 4 | $15 / MTok | $18.75 / MTok | $30 / MTok | $1.50 / MTok | $75 / MTok |
| Claude Sonnet 4.5 | $3 / MTok | $3.75 / MTok | $6 / MTok | $0.30 / MTok | $15 / MTok |
| Claude Sonnet 4 | $3 / MTok | $3.75 / MTok | $6 / MTok | $0.30 / MTok | $15 / MTok |
| Claude Sonnet 3.7 (deprecated) | $3 / MTok | $3.75 / MTok | $6 / MTok | $0.30 / MTok | $15 / MTok |
| Claude Haiku 4.5 | $1 / MTok | $1.25 / MTok | $2 / MTok | $0.10 / MTok | $5 / MTok |
| Claude Haiku 3.5 | $0.80 / MTok | $1 / MTok | $1.6 / MTok | $0.08 / MTok | $4 / MTok |

<transcription_json>
{"table_type":"data_table","title":"Model pricing","columns":["Model","Base Input Tokens","5m Cache Writes","1h Cache Writes","Cache Hits & Refreshes","Output Tokens"],"data":[{"Model":"Claude Opus 4.6","Base Input Tokens":"$5 / MTok","5m Cache Writes":"$6.25 / MTok","1h Cache Writes":"$10 / MTok","Cache Hits & Refreshes":"$0.50 / MTok","Output Tokens":"$25 / MTok"},{"Model":"Claude Opus 4.5","Base Input Tokens":"$5 / MTok","5m Cache Writes":"$6.25 / MTok","1h Cache Writes":"$10 / MTok","Cache Hits & Refreshes":"$0.50 / MTok","Output Tokens":"$25 / MTok"},{"Model":"Claude Opus 4.1","Base Input Tokens":"$15 / MTok","5m Cache Writes":"$18.75 / MTok","1h Cache Writes":"$30 / MTok","Cache Hits & Refreshes":"$1.50 / MTok","Output Tokens":"$75 / MTok"},{"Model":"Claude Opus 4","Base Input Tokens":"$15 / MTok","5m Cache Writes":"$18.75 / MTok","1h Cache Writes":"$30 / MTok","Cache Hits & Refreshes":"$1.50 / MTok","Output Tokens":"$75 / MTok"},{"Model":"Claude Sonnet 4.5","Base Input Tokens":"$3 / MTok","5m Cache Writes":"$3.75 / MTok","1h Cache Writes":"$6 / MTok","Cache Hits & Refreshes":"$0.30 / MTok","Output Tokens":"$15 / MTok"},{"Model":"Claude Sonnet 4","Base Input Tokens":"$3 / MTok","5m Cache Writes":"$3.75 / MTok","1h Cache Writes":"$6 / MTok","Cache Hits & Refreshes":"$0.30 / MTok","Output Tokens":"$15 / MTok"},{"Model":"Claude Sonnet 3.7 (deprecated)","Base Input Tokens":"$3 / MTok","5m Cache Writes":"$3.75 / MTok","1h Cache Writes":"$6 / MTok","Cache Hits & Refreshes":"$0.30 / MTok","Output Tokens":"$15 / MTok"},{"Model":"Claude Haiku 4.5","Base Input Tokens":"$1 / MTok","5m Cache Writes":"$1.25 / MTok","1h Cache Writes":"$2 / MTok","Cache Hits & Refreshes":"$0.10 / MTok","Output Tokens":"$5 / MTok"},{"Model":"Claude Haiku 3.5","Base Input Tokens":"$0.80 / MTok","5m Cache Writes":"$1 / MTok","1h Cache Writes":"$1.6 / MTok","Cache Hits & Refreshes":"$0.08 / MTok","Output Tokens":"$4 / MTok"}],"unit":"USD per MTok"}
</transcription_json>
</transcription_table>

<transcription_page_footer> Page 1 | Anthropic </transcription_page_footer>

## Prompt caching pricing multipliers

<transcription_json>
{"box_type":"info_box","title":"MTok = Million tokens","content":"The \"Base Input Tokens\" column shows standard input pricing, \"Cache Writes\" and \"Cache Hits\" are specific to prompt caching, and \"Output Tokens\" shows output pricing. Prompt caching offers both 5-minute (default) and 1-hour cache durations to optimize costs for different use cases.","bullets":[{"text":"5-minute cache write tokens are 1.25 times the base input tokens price","multiplier":1.25},{"text":"1-hour cache write tokens are 2 times the base input tokens price","multiplier":2.0},{"text":"Cache read tokens are 0.1 times the base input tokens price","multiplier":0.1}]}
</transcription_json>

## Third-party platform pricing

Claude models are available on AWS Bedrock, Google Vertex AI, and Microsoft Foundry.

## Regional endpoint pricing

<transcription_json>
{"box_type":"info_box","title":"Regional endpoint pricing for Claude 4.5 models and beyond","content":"Starting with Claude Sonnet 4.5 and Haiku 4.5, AWS Bedrock and Google Vertex AI offer two endpoint types: Global endpoints and Regional endpoints. Regional endpoints include a 10% premium over global endpoints. The Claude API (1P) is global by default and unaffected by this change.","bullets":[{"label":"Global endpoints","description":"Dynamic routing across regions for maximum availability"},{"label":"Regional endpoints","description":"Data routing guaranteed within specific geographic regions"},{"label":"Regional premium","description":"Regional endpoints include a 10% premium over global endpoints","value":"10%"}],"scope":"This pricing structure applies to Claude Sonnet 4.5, Haiku 4.5, and all future models. Earlier models (Claude Sonnet 4, Opus 4, and prior releases) retain their existing pricing."}
</transcription_json>

<transcription_page_header> Feature-specific pricing | Pricing </transcription_page_header>

# Feature-specific pricing

## Data residency pricing

For Claude Opus 4.6 and newer models, specifying US-only inference via the `inference_geo` parameter incurs a 1.1x multiplier on all token pricing categories. Global routing (the default) uses standard pricing. Applies to Claude API (1P) only. Earlier models retain existing pricing regardless of `inference_geo` settings.

## Batch processing

The Batch API allows asynchronous processing with a 50% discount on both input and output tokens.

<transcription_table>
Table: Batch processing

| Model | Batch input | Batch output |
|-------|-------------:|-------------:|
| Claude Opus 4.6 | $2.50 / MTok | $12.50 / MTok |
| Claude Opus 4.5 | $2.50 / MTok | $12.50 / MTok |
| Claude Opus 4.1 | $7.50 / MTok | $37.50 / MTok |
| Claude Opus 4 | $7.50 / MTok | $37.50 / MTok |
| Claude Sonnet 4.5 | $1.50 / MTok | $7.50 / MTok |
| Claude Sonnet 4 | $1.50 / MTok | $7.50 / MTok |
| Claude Sonnet 3.7 (deprecated) | $1.50 / MTok | $7.50 / MTok |
| Claude Haiku 4.5 | $0.50 / MTok | $2.50 / MTok |
| Claude Haiku 3.5 | $0.40 / MTok | $2 / MTok |
| Claude Opus 3 (deprecated) | $7.50 / MTok | $37.50 / MTok |
| Claude Haiku 3 | $0.125 / MTok | $0.625 / MTok |

<transcription_json>
{"table_type": "data_table", "title": "Batch processing", "columns": ["Model", "Batch input", "Batch output"], "data": [{"Model":"Claude Opus 4.6","Batch input":2.50,"Batch output":12.50,"unit":"$/MTok"},{"Model":"Claude Opus 4.5","Batch input":2.50,"Batch output":12.50,"unit":"$/MTok"},{"Model":"Claude Opus 4.1","Batch input":7.50,"Batch output":37.50,"unit":"$/MTok"},{"Model":"Claude Opus 4","Batch input":7.50,"Batch output":37.50,"unit":"$/MTok"},{"Model":"Claude Sonnet 4.5","Batch input":1.50,"Batch output":7.50,"unit":"$/MTok"},{"Model":"Claude Sonnet 4","Batch input":1.50,"Batch output":7.50,"unit":"$/MTok"},{"Model":"Claude Sonnet 3.7 (deprecated)","Batch input":1.50,"Batch output":7.50,"unit":"$/MTok","deprecated":true},{"Model":"Claude Haiku 4.5","Batch input":0.50,"Batch output":2.50,"unit":"$/MTok"},{"Model":"Claude Haiku 3.5","Batch input":0.40,"Batch output":2.00,"unit":"$/MTok"},{"Model":"Claude Opus 3 (deprecated)","Batch input":7.50,"Batch output":37.50,"unit":"$/MTok","deprecated":true},{"Model":"Claude Haiku 3","Batch input":0.125,"Batch output":0.625,"unit":"$/MTok"}], "unit":"$/MTok"}
</transcription_json>
</transcription_table>

<transcription_page_header>Long context pricing | Pricing</transcription_page_header>

# Long context pricing

When using Claude Opus 4.6, Sonnet 4.5, or Sonnet 4 with the 1M token context window enabled, requests exceeding 200K input tokens are charged at premium rates.

The 1M token context window is currently in beta for organizations in usage tier 4 and organizations with custom rate limits. Only available for Claude Opus 4.6, Sonnet 4.5, and Sonnet 4.

<transcription_table>
Table 1: Long context pricing by model

| Model | ≤ 200K input tokens | > 200K input tokens |
|-------|---------------------|----------------------|
| Claude Opus 4.6 | Input: $5 / MTok<br>Output: $25 / MTok | Input: $10 / MTok<br>Output: $37.50 / MTok |
| Claude Sonnet 4.5 / 4 | Input: $3 / MTok<br>Output: $15 / MTok | Input: $6 / MTok<br>Output: $22.50 / MTok |

<transcription_json>
{"table_type":"data_table","title":"Long context pricing by model","columns":["Model","≤ 200K input tokens"," > 200K input tokens"],"data":[{"Model":"Claude Opus 4.6","≤ 200K input tokens":"Input: $5 / MTok; Output: $25 / MTok"," > 200K input tokens":"Input: $10 / MTok; Output: $37.50 / MTok"},{"Model":"Claude Sonnet 4.5 / 4","≤ 200K input tokens":"Input: $3 / MTok; Output: $15 / MTok"," > 200K input tokens":"Input: $6 / MTok; Output: $22.50 / MTok"}],"unit":"price per million tokens (MTok)"}
</transcription_json>
</transcription_table>

Long context pricing stacks with other pricing modifiers:

- The Batch API 50% discount applies to long context pricing
- Prompt caching multipliers apply on top of long context pricing
- The data residency 1.1x multiplier applies on top of long context pricing

Even with the beta flag enabled, requests with fewer than 200K input tokens are charged at standard rates. If your request exceeds 200K input tokens, all tokens incur premium pricing. The 200K threshold is based solely on input tokens (including cache reads/writes). Output token count does not affect pricing tier selection, though output tokens are charged at the higher rate when the input threshold is exceeded.

Calculate total input tokens by summing: `input_tokens` + `cache_creation_input_tokens` + `cache_read_input_tokens`. If total exceeds 200,000, the entire request was billed at 1M context rates.

## Tool use pricing

Tool use requests are priced based on:

1. Total input tokens sent to the model (including `tools` parameter)
2. Output tokens generated
3. For server-side tools, additional usage-based pricing

The additional tokens from tool use come from the `tools` parameter, `tool_use` content blocks, and `tool_result` content blocks. A special system prompt is automatically included when using tools.

<transcription_table>
Table: Model token counts

| Model | Mode | Tokens |
|-------|------|--------|
| Claude Opus 4.6 | auto , none | 346 tokens |
| Claude Opus 4.6 | any , tool | 313 tokens |
| Claude Opus 4.5 | auto , none | 346 tokens |
| Claude Opus 4.5 | any , tool | 313 tokens |
| Claude Opus 4.1 | auto , none | 346 tokens |
| Claude Opus 4.1 | any , tool | 313 tokens |
| Claude Opus 4 | auto , none | 346 tokens |
| Claude Opus 4 | any , tool | 313 tokens |
| Claude Sonnet 4.5 | auto , none | 346 tokens |
| Claude Sonnet 4.5 | any , tool | 313 tokens |
| Claude Sonnet 4 | auto , none | 346 tokens |
| Claude Sonnet 4 | any , tool | 313 tokens |
| Claude Sonnet 3.7 (deprecated) | auto , none | 346 tokens |
| Claude Sonnet 3.7 (deprecated) | any , tool | 313 tokens |
| Claude Haiku 4.5 | auto , none | 346 tokens |
| Claude Haiku 4.5 | any , tool | 313 tokens |
| Claude Haiku 3.5 | auto , none | 264 tokens |
| Claude Haiku 3.5 | any , tool | 340 tokens |
| Claude Opus 3 (deprecated) | auto , none | 530 tokens |
| Claude Opus 3 (deprecated) | any , tool | 281 tokens |
| Claude Sonnet 3 | auto , none | 159 tokens |
| Claude Sonnet 3 | any , tool | 235 tokens |
| Claude Haiku 3 | auto , none | 264 tokens |
| Claude Haiku 3 | any , tool | 340 tokens |

<transcription_json>
{"table_type":"data_table","title":"Model token counts","columns":["Model","Mode","Tokens"],"data":[{"Model":"Claude Opus 4.6","Mode":"auto , none","Tokens":346},{"Model":"Claude Opus 4.6","Mode":"any , tool","Tokens":313},{"Model":"Claude Opus 4.5","Mode":"auto , none","Tokens":346},{"Model":"Claude Opus 4.5","Mode":"any , tool","Tokens":313},{"Model":"Claude Opus 4.1","Mode":"auto , none","Tokens":346},{"Model":"Claude Opus 4.1","Mode":"any , tool","Tokens":313},{"Model":"Claude Opus 4","Mode":"auto , none","Tokens":346},{"Model":"Claude Opus 4","Mode":"any , tool","Tokens":313},{"Model":"Claude Sonnet 4.5","Mode":"auto , none","Tokens":346},{"Model":"Claude Sonnet 4.5","Mode":"any , tool","Tokens":313},{"Model":"Claude Sonnet 4","Mode":"auto , none","Tokens":346},{"Model":"Claude Sonnet 4","Mode":"any , tool","Tokens":313},{"Model":"Claude Sonnet 3.7 (deprecated)","Mode":"auto , none","Tokens":346},{"Model":"Claude Sonnet 3.7 (deprecated)","Mode":"any , tool","Tokens":313},{"Model":"Claude Haiku 4.5","Mode":"auto , none","Tokens":346},{"Model":"Claude Haiku 4.5","Mode":"any , tool","Tokens":313},{"Model":"Claude Haiku 3.5","Mode":"auto , none","Tokens":264},{"Model":"Claude Haiku 3.5","Mode":"any , tool","Tokens":340},{"Model":"Claude Opus 3 (deprecated)","Mode":"auto , none","Tokens":530},{"Model":"Claude Opus 3 (deprecated)","Mode":"any , tool","Tokens":281},{"Model":"Claude Sonnet 3","Mode":"auto , none","Tokens":159},{"Model":"Claude Sonnet 3","Mode":"any , tool","Tokens":235},{"Model":"Claude Haiku 3","Mode":"auto , none","Tokens":264},{"Model":"Claude Haiku 3","Mode":"any , tool","Tokens":340}],"unit":"tokens"}
</transcription_json>
</transcription_table>

These token counts are added to your normal input and output tokens to calculate total cost.

## Specific tool pricing

### Bash tool

Adds 245 input tokens to API calls. Additional tokens consumed by command outputs, error messages, large file contents.

### Code execution tool

Tracked separately from token usage. Execution time minimum 5 minutes. Files included in request are billed even if tool not used. Each organization receives 1,550 free hours per month. Additional usage: $0.05 per hour, per container.

### Text editor tool

Standard input/output token pricing plus additional input tokens:

<transcription_table>
Table 1: Text editor tool — additional input tokens

| Tool | Additional input tokens |
|------|-------------------------|
| text_editor_20250429 (Claude 4.x) | 700 tokens |
| text_editor_20250124 (Claude Sonnet 3.7 (deprecated)) | 700 tokens |

<transcription_json>
{"table_type":"data_table","title":"Text editor tool - additional input tokens","columns":["Tool","Additional input tokens"],"data":[{"Tool":"text_editor_20250429 (Claude 4.x)","Additional input tokens":"700 tokens"},{"Tool":"text_editor_20250124 (Claude Sonnet 3.7 (deprecated))","Additional input tokens":"700 tokens"}],"unit":"tokens"}
</transcription_json>
</transcription_table>

## Web search tool

Web search: $10 per 1,000 searches, plus standard token costs for search-generated content. Results counted as input tokens. Each search counts as one use regardless of results returned. Errors are not billed.

Usage example:
```json
{"usage":{"input_tokens":105,"output_tokens":6039,"cache_read_input_tokens":7123,"cache_creation_input_tokens":7345,"server_tool_use":{"web_search_requests":1}}}
```

## Web fetch tool

No additional charges beyond standard token costs. Use `max_content_tokens` parameter to limit fetched content size.

Usage example:
```json
{"usage":{"input_tokens":25039,"output_tokens":931,"cache_read_input_tokens":0,"cache_creation_input_tokens":0,"server_tool_use":{"web_fetch_requests":1}}}
```

Example token usage for typical content:
- Average web page (10KB): ~2,500 tokens
- Large documentation page (100KB): ~25,000 tokens
- Research paper PDF (500KB): ~125,000 tokens

## Computer use tool

Standard tool use pricing. System prompt overhead: 466-499 tokens.

<transcription_table>
Computer use tool token usage

| Model | Input tokens per tool definition |
|-------|----------------------------------|
| Claude 4.x models | 735 tokens |
| Claude Sonnet 3.7 (deprecated) | 735 tokens |

<transcription_json>
{"table_type":"data_table","title":"Computer use tool token usage","columns":["Model","Input tokens per tool definition"],"data":[{"Model":"Claude 4.x models","Input tokens per tool definition":735},{"Model":"Claude Sonnet 3.7 (deprecated)","Input tokens per tool definition":735}],"unit":"tokens"}
</transcription_json>
</transcription_table>

Additional token consumption: screenshot images (Vision pricing) and tool execution results.

Note: Bash or text editor tools alongside computer use have their own token costs.

## Agent use case pricing examples

### Customer support agent example

> Processing 10,000 support tickets: ~3,700 tokens per conversation, using Claude Opus 4.6 at $5/MTok input, $25/MTok output

### General agent workflow pricing

1. Initial request processing - 500-1,000 tokens input, ~$0.003 per request
2. Memory and context retrieval - 2,000-5,000 tokens, ~$0.015 per operation
3. Action planning and execution - 1,000-2,000 planning + 500-1,000 feedback, ~$0.045 per action

## Cost optimization strategies

1. Use appropriate models: Haiku for simple tasks, Sonnet for complex reasoning
2. Implement prompt caching: Reduce costs for repeated context
3. Batch operations: Use Batch API for non-time-sensitive tasks
4. Monitor usage patterns: Track token consumption for optimization

# Additional pricing considerations

## Rate limits

- Tier 1: Entry-level usage with basic limits
- Tier 2: Increased limits for growing applications
- Tier 3: Higher limits for established applications
- Tier 4: Maximum standard limits
- Enterprise: Custom limits available

## Volume discounts

Negotiated case-by-case. Enterprise customers contact sales. Academic and research discounts may be available.

## Enterprise pricing

Custom rate limits, volume discounts, dedicated support, custom terms. Contact sales@anthropic.com.

## Billing and payment

- Monthly billing based on actual usage, processed in USD
- Credit card and invoicing options available
- Usage tracking available in the Claude Console

## Frequently asked questions

How is token usage calculated? ~1 token is approximately 4 characters or 0.75 words in English.

Are there free tiers or trials? New users receive free credits. Contact sales for extended enterprise trials.

How do discounts stack? Batch API and prompt caching discounts can be combined.

What payment methods are accepted? Major credit cards for standard accounts. Enterprise customers can arrange invoicing.

For additional questions: support@anthropic.com.