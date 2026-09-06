<!-- Page 001 -->


<transcription_page_header> Claude API Docs | Pricing </transcription_page_header>

# Pricing
Learn about Anthropic's pricing structure for models and features

This page provides detailed pricing information for Anthropic's models and features. All prices are in USD.

For the most current pricing information, please visit claude.com/pricing.

<!-- Section 1 -->
<!-- Column 1 -->
## Model pricing

The following table shows pricing for all Claude models across different usage tiers:

<transcription_table>
**Model pricing**

| Model | Base input tokens | 5m cache writes | 1h cache writes | Cache hits & refreshes | Output tokens |
|-------|-------------------:|----------------:|----------------:|-----------------------:|--------------:|
| Claude Opus 4.5 | [unclear] | [unclear] | [unclear] | [unclear] | [unclear] |
| Claude Opus 4.1 | [unclear] | [unclear] | [unclear] | [unclear] | [unclear] |
| Claude Opus 4 | [unclear] | [unclear] | [unclear] | [unclear] | [unclear] |
| Claude Sonnet 4.5 | [unclear] | [unclear] | [unclear] | [unclear] | [unclear] |
| Claude Sonnet 4 | [unclear] | [unclear] | [unclear] | [unclear] | [unclear] |
| Claude Sonnet 3.7 (deprecated) | [unclear] | [unclear] | [unclear] | [unclear] | [unclear] |
| Claude Haiku 4.5 | [unclear] | [unclear] | [unclear] | [unclear] | [unclear] |
| Claude Haiku 3.5 | [unclear] | [unclear] | [unclear] | [unclear] | [unclear] |
| Claude Opus 3 (deprecated) | [unclear] | [unclear] | [unclear] | [unclear] | [unclear] |
| Claude Haiku 3 | [unclear] | [unclear] | [unclear] | [unclear] | [unclear] |

<transcription_json>
{"table_type": "data_table", "title": "Model pricing", "columns": ["Model","Base input tokens","5m cache writes","1h cache writes","Cache hits & refreshes","Output tokens"], "data": [{"Model":"Claude Opus 4.5","Base input tokens":"[unclear]","5m cache writes":"[unclear]","1h cache writes":"[unclear]","Cache hits & refreshes":"[unclear]","Output tokens":"[unclear]"},{"Model":"Claude Opus 4.1","Base input tokens":"[unclear]","5m cache writes":"[unclear]","1h cache writes":"[unclear]","Cache hits & refreshes":"[unclear]","Output tokens":"[unclear]"},{"Model":"Claude Opus 4","Base input tokens":"[unclear]","5m cache writes":"[unclear]","1h cache writes":"[unclear]","Cache hits & refreshes":"[unclear]","Output tokens":"[unclear]"},{"Model":"Claude Sonnet 4.5","Base input tokens":"[unclear]","5m cache writes":"[unclear]","1h cache writes":"[unclear]","Cache hits & refreshes":"[unclear]","Output tokens":"[unclear]"},{"Model":"Claude Sonnet 4","Base input tokens":"[unclear]","5m cache writes":"[unclear]","1h cache writes":"[unclear]","Cache hits & refreshes":"[unclear]","Output tokens":"[unclear]"},{"Model":"Claude Sonnet 3.7 (deprecated)","Base input tokens":"[unclear]","5m cache writes":"[unclear]","1h cache writes":"[unclear]","Cache hits & refreshes":"[unclear]","Output tokens":"[unclear]"},{"Model":"Claude Haiku 4.5","Base input tokens":"[unclear]","5m cache writes":"[unclear]","1h cache writes":"[unclear]","Cache hits & refreshes":"[unclear]","Output tokens":"[unclear]"},{"Model":"Claude Haiku 3.5","Base input tokens":"[unclear]","5m cache writes":"[unclear]","1h cache writes":"[unclear]","Cache hits & refreshes":"[unclear]","Output tokens":"[unclear]"},{"Model":"Claude Opus 3 (deprecated)","Base input tokens":"[unclear]","5m cache writes":"[unclear]","1h cache writes":"[unclear]","Cache hits & refreshes":"[unclear]","Output tokens":"[unclear]"},{"Model":"Claude Haiku 3","Base input tokens":"[unclear]","5m cache writes":"[unclear]","1h cache writes":"[unclear]","Cache hits & refreshes":"[unclear]","Output tokens":"[unclear]"}], "unit": "USD per MTok or as shown"}
</transcription_json>

<transcription_notes>
- Table spans leftmost column of the page.
- Many numeric values in the table were not legible at the image scale; unreadable cells are marked "[unclear]".
- The table visually contains a blue info callout below it describing cache pricing multipliers (5-minute cache write, 1-hour cache write, cache read multipliers). The callout also includes clarifications about "Base input tokens" and "Output tokens".
</transcription_notes>
</transcription_table>

<!-- Section 2 -->
## Feature-specific pricing

<!-- Column 1 -->
### Batch processing

The Batch API allows asynchronous processing of large volumes of requests with a 50% discount on both input and output tokens.

<transcription_table>
**Batch processing**

| Model | Batch input | Batch output |
|-------|------------:|-------------:|
| Claude Opus 4.5 | [unclear] | [unclear] |
| Claude Opus 4.1 | [unclear] | [unclear] |
| Claude Opus 4 | [unclear] | [unclear] |
| Claude Sonnet 4.5 | [unclear] | [unclear] |
| Claude Sonnet 4 | [unclear] | [unclear] |
| Claude Sonnet 3.7 (deprecated) | [unclear] | [unclear] |
| Claude Haiku 4.5 | [unclear] | [unclear] |
| Claude Haiku 3.5 | [unclear] | [unclear] |
| Claude Opus 3 (deprecated) | [unclear] | [unclear] |
| Claude Haiku 3 | [unclear] | [unclear] |

<transcription_json>
{"table_type":"data_table","title":"Batch processing","columns":["Model","Batch input","Batch output"], "data":[{"Model":"Claude Opus 4.5","Batch input":"[unclear]","Batch output":"[unclear]"},{"Model":"Claude Opus 4.1","Batch input":"[unclear]","Batch output":"[unclear]"},{"Model":"Claude Opus 4","Batch input":"[unclear]","Batch output":"[unclear]"},{"Model":"Claude Sonnet 4.5","Batch input":"[unclear]","Batch output":"[unclear]"},{"Model":"Claude Sonnet 4","Batch input":"[unclear]","Batch output":"[unclear]"},{"Model":"Claude Sonnet 3.7 (deprecated)","Batch input":"[unclear]","Batch output":"[unclear]"},{"Model":"Claude Haiku 4.5","Batch input":"[unclear]","Batch output":"[unclear]"},{"Model":"Claude Haiku 3.5","Batch input":"[unclear]","Batch output":"[unclear]"},{"Model":"Claude Opus 3 (deprecated)","Batch input":"[unclear]","Batch output":"[unclear]"},{"Model":"Claude Haiku 3","Batch input":"[unclear]","Batch output":"[unclear]"}], "unit":"USD per MTok (batch discounted rates)"}
</transcription_json>

<transcription_notes>
- Section includes a blue callout about long context pricing and a 1M token context window beta for some models. The callout also shows rate examples for "<200K input tokens" vs ">200K input tokens" with input/output rates (these numbers were not legible at the image resolution).
- The page mentions the Batch API 50% discount applies to long context pricing and prompt caching multipliers apply on top of long context pricing.
</transcription_notes>
</transcription_table>

<!-- Section 3 -->
## Tool use pricing

Tool use requests are priced based on:
1. The total number of input tokens sent to the model (including in the tools parameter)
2. The number of output tokens generated
3. For server-side tools, additional usage-based pricing (e.g., web search charges per search performed)

Client-side tools are priced the same as any other Claude API request, while server-side tools may incur additional charges based on their specific usage.

The additional tokens from tool use come from:
- The tools parameter in API requests (tool names, descriptions, and schemas)
- tool_use content blocks in API requests and responses
- tool_result content blocks in API responses

When you use tools, we also automatically include a special system prompt for the model which enables tool use. The number of tool use tokens required for each model are listed below (excluding the additional tokens listed above). Note that the table assumes at least 1 tool is provided. If no tools are provided, then a tool choice of none uses 0 additional system prompt tokens.

<transcription_table>
**Tool use system prompt token counts**

| Model | Tool choice | Tool use system prompt token count |
|-------|-------------|-----------------------------------:|
| Claude Opus 4.5 | auto, none | 346 tokens |
| Claude Opus 4.1 | any, tool | 313 tokens |
| Claude Opus 4 | auto, none | 313 tokens |
| Claude Sonnet 4.5 | auto, none | 346 tokens |
| Claude Sonnet 4 | any, tool | 313 tokens |
| Claude Sonnet 3.7 (deprecated) | auto, none | 313 tokens |
| Claude Haiku 4.5 | auto, none | 346 tokens |
| Claude Haiku 3.5 | any, tool | 264 tokens |
| Claude Opus 3 (deprecated) | auto, none | 530 tokens |
| Claude Sonnet 3 | any, tool | 235 tokens |
| Claude Haiku 3 | auto, none | 240 tokens |

<transcription_json>
{"table_type":"data_table","title":"Tool use system prompt token counts","columns":["Model","Tool choice","Tool use system prompt token count"], "data":[{"Model":"Claude Opus 4.5","Tool choice":"auto, none","Tool use system prompt token count":"346"},{"Model":"Claude Opus 4.1","Tool choice":"any, tool","Tool use system prompt token count":"313"},{"Model":"Claude Opus 4","Tool choice":"auto, none","Tool use system prompt token count":"313"},{"Model":"Claude Sonnet 4.5","Tool choice":"auto, none","Tool use system prompt token count":"346"},{"Model":"Claude Sonnet 4","Tool choice":"any, tool","Tool use system prompt token count":"313"},{"Model":"Claude Sonnet 3.7 (deprecated)","Tool choice":"auto, none","Tool use system prompt token count":"313"},{"Model":"Claude Haiku 4.5","Tool choice":"auto, none","Tool use system prompt token count":"346"},{"Model":"Claude Haiku 3.5","Tool choice":"any, tool","Tool use system prompt token count":"264"},{"Model":"Claude Opus 3 (deprecated)","Tool choice":"auto, none","Tool use system prompt token count":"530"},{"Model":"Claude Sonnet 3","Tool choice":"any, tool","Tool use system prompt token count":"235"},{"Model":"Claude Haiku 3","Tool choice":"auto, none","Tool use system prompt token count":"240"}], "unit":"tokens"}
</transcription_json>

<transcription_notes>
- The token counts above were read visually from the table in the center-right column of the page. Most counts were legible; where the image was ambiguous some counts have been conservatively left as shown in the source image.
- The page notes: "These token counts are added to your normal input and output tokens to calculate the total cost of a request."
</transcription_notes>
</transcription_table>

<!-- Section 4 -->
### Specific tool pricing

#### Code execution tool
Code execution tool usage is tracked separately from token usage. Execution time has a minimum of 5 minutes. If files are included in the request, execution time is billed even if the tool is not used due to files being preloaded onto the container.

Each organization receives 1,550 free hours of usage with the code execution tool per month. Additional usage beyond the first 1,550 hours is billed at $0.05 per hour, per container. [unclear: exact phrasing preserved where legible]

#### Text editor tool
The text editor tool uses the same pricing structure as other tools used with Claude. It follows the standard input and output token pricing based on the Claude model you're using.

In addition to the base tokens, the following additional input tokens are needed for the text editor tool:

<transcription_table>
**Text editor tool additional input tokens**

| Tool | Additional input tokens |
|------|------------------------:|
| text_editor_20250421 (Claude 4.x) | 700 tokens |
| text_editor_20250421 (Claude Sonnet 3.7 (deprecated)) | 700 tokens |

<transcription_json>
{"table_type":"data_table","title":"Text editor tool additional input tokens","columns":["Tool","Additional input tokens"], "data":[{"Tool":"text_editor_20250421 (Claude 4.x)","Additional input tokens":"700"},{"Tool":"text_editor_20250421 (Claude Sonnet 3.7 (deprecated))","Additional input tokens":"700"}], "unit":"tokens"}
</transcription_json>

<transcription_notes>
- The page shows two listed editor tool identifiers both with 700 tokens.
</transcription_notes>
</transcription_table>

#### Web search tool
Web search usage is charged in addition to token usage. The page includes an example JSON "usage" object for a web search request:

<transcription_image>
**Figure: Web search tool usage example**

```ascii
"usage": {
  "input_tokens": 106,
  "output_tokens": 6830,
  "cache_read_input_tokens": 7123,
  "cache_creation_input_tokens": 7345,
  "server_tool_use": {
    "web_search_requests": 1
  }
}
```

<transcription_json>
{"chart_type":"code_snippet","title":"Web search tool usage example","data":{"usage":{"input_tokens":106,"output_tokens":6830,"cache_read_input_tokens":7123,"cache_creation_input_tokens":7345,"server_tool_use":{"web_search_requests":1}}}}
</transcription_json>

<transcription_notes>
- Type: JSON usage example shown in a gray code box on the rightmost column.
- Values appear to be an example of token accounting for a web search request: input_tokens 106, output_tokens 6830, cache_read_input_tokens 7123, cache_creation_input_tokens 7345, web_search_requests 1.
- The page states: "Web search is available on the Claude API for $10 per 1,000 searches, plus standard token costs for search-generated content."
</transcription_notes>
</transcription_image>

#### Web fetch tool
Web fetch tool usage example JSON is shown below on the page:

<transcription_image>
**Figure: Web fetch tool usage example**

```ascii
"usage": {
  "input_tokens": 25039,
  "output_tokens": 931,
  "cache_read_input_tokens": 0,
  "cache_creation_input_tokens": 0,
  "server_tool_use": {
    "web_fetch_requests": 1
  }
}
```

<transcription_json>
{"chart_type":"code_snippet","title":"Web fetch tool usage example","data":{"usage":{"input_tokens":25039,"output_tokens":931,"cache_read_input_tokens":0,"cache_creation_input_tokens":0,"server_tool_use":{"web_fetch_requests":1}}}}
</transcription_json>

<transcription_notes>
- Type: JSON usage example shown in a gray code box lower on the rightmost column.
- Values illustrate a typical web fetch where input_tokens is large (e.g., 25039) and output_tokens smaller (931).
- The page text explains web fetch usage has no additional charges beyond standard token costs for the fetched content.
</transcription_notes>
</transcription_image>

<!-- Section 5 -->
### Web search and web fetch pricing notes
- Web search: $10 per 1,000 searches (plus token costs).
- Web fetch: charged only by token usage (no additional fixed tool cost).
- Example token usages shown for typical content:
  - Average web page (10KB): ~2,500 tokens
  - Large documentation page (100KB): ~25,000 tokens
  - Research paper PDF (500KB): ~125,000 tokens

<!-- Section 6 -->
## Third-party platform pricing

Claude models are available on AWS Bedrock, Google Vertex AI, and Microsoft Foundry. For official pricing, visit:
- AWS Bedrock pricing
- Google Vertex AI pricing
- Microsoft Foundry pricing

<transcription_notes>
- The left column contains a blue info box discussing regional endpoint pricing for Claude 4.5 models and beyond, and notes about global vs regional endpoints and pricing applicability across models.
- The page footer contains small links and a page navigation area (not transcribed).
</transcription_notes>

<transcription_page_footer> Page 1 | Claude API Docs </transcription_page_footer>

---
<!-- Page 002 -->


<transcription_page_header>Claude API Docs | Pricing</transcription_page_header>

# Pricing

<!-- Section 1 -->
<!-- Column 1 -->

## Additional token consumption:
- Screenshot images (see Vision pricing)
- Tool execution results returned to Claude

> If you're also using bash or text editor tools alongside computer use, those tools have their own token costs as documented in their respective pages.

## Agent use case pricing examples
Understanding pricing for agent applications is crucial when building with Claude. These real-world examples can help you estimate costs for different agent patterns.

### Customer support agent example
When building a customer support agent, here's how costs might break down:

Example calculation for processing 10,000 support tickets:
- Average ~3,700 tokens per conversation
- Using Claude Sonnet 4.5 at $3/MToken input, $15/MToken output [unclear]
- Total cost: ~$22.20 per 10,000 tickets

For a detailed walkthrough of this calculation, see our customer support agent guide.

### General agent workflow pricing
For more complex agent architectures with multiple steps:

1. Initial request processing
: Typical input: 500–1,000 tokens
: Processing cost: ~$0.003 per request

2. Memory and context retrieval
: Retrieved context: 2,000–5,000 tokens
: Cost per retrieval: ~$0.015 per operation

3. Action planning and execution
: Planning tokens: 1,000–2,000
: Execution feedback: 500–1,000
: Combined cost: ~$0.045 per action

For a comprehensive guide on agent pricing patterns, see our agent use cases guide.

### Cost optimization strategies
When building agents with Claude:
1. Use appropriate models: Choose Haiku for simple tasks, Sonnet for complex reasoning
2. Implement prompt caching: Reduce costs for repeated content
3. Batch operations: Use the Batch API for non-time-sensitive tasks
4. Monitor usage patterns: Track token consumption to identify optimization opportunities

For high-volume agent applications, consider contacting our enterprise sales team for custom pricing arrangements.

<!-- Column 2 -->

## Additional pricing considerations

### Rate limits
Rate limits vary by usage tier and affect how many requests you can make:
- Tier 1: Entry-level usage with basic limits
- Tier 2: Increased limits for growing applications
- Tier 3: Higher limits for established applications
- Tier 4: Maximum standard limits
- Enterprise: Custom limits available

For detailed rate limit information, see our rate limits documentation.

For higher rate limits or custom pricing arrangements, contact our sales team.

### Volume discounts
Volume discounts may be available for high-volume users. These are negotiated on a case-by-case basis.
- Standard tiers use the pricing shown above
- Enterprise customers can contact sales for custom pricing
- Academic and research discounts may be available

### Enterprise pricing
For enterprise customers with specific needs:
- Custom rate limits
- Volume discounts
- Dedicated support
- Custom terms

Contact our sales team at sales@anthropic.com or through the Claude Console to discuss enterprise pricing options.

### Billing and payment
- Billing is calculated monthly based on actual usage
- Payments are processed in USD
- Credit card and invoicing options available
- Usage tracking available in the Claude Console

## Frequently asked questions

**How is token usage calculated?**  
Tokens are pieces of text that models process. As a rough estimate, 1 token is approximately 4 characters or 0.75 words in English. The exact count varies by language and content type.

**Are there free tiers or trials?**  
New users receive a small amount of free credits to test the API. Contact sales for information about extended trials for enterprise customers.

**How do discounts stack?**  
Batch API and prompt caching discounts can be combined. For example, using both features together provides significant cost savings compared to standard API calls.

**What payment methods are accepted?**  
We accept major credit cards for standard accounts. Enterprise customers can arrange invoicing and other payment methods.

For additional questions about pricing, contact support@anthropic.com.

<transcription_notes>
- Page layout: two-column documentation page from "Claude API Docs" (Pricing).
- Visual elements:
  - Top-left: Claude logo and breadcrumb "Models & pricing > Pricing".
  - Left column contains blue callout boxes:
    - Small blue info box under "Additional token consumption" with rounded border and light-blue background containing note about token costs for bash/text editor tools.
    - Larger blue example box under "Customer support agent example" titled "Example calculation for processing 10,000 support tickets:" with three bulleted lines (average tokens, model & rates line, total cost). Box background: light blue; border: medium blue. Text inside is darker blue/black.
  - Right column is plain text with headings and bullet lists.
- Colors observed:
  - Headings: dark brown/black.
  - Callout boxes: light blue backgrounds, medium blue borders.
  - Page background: off-white.
- Positioning:
  - Left column: "Additional token consumption", agent examples, general workflow, cost optimization.
  - Right column: "Additional pricing considerations", rate limits, volume discounts, enterprise pricing, billing, FAQ.
- Unclear text:
  - The specific model name and per-MToken rates in the example calculation line are partially unclear in the image. Marked inline as [unclear].
- No charts or data tables detected on this page.
</transcription_notes>

<transcription_page_footer>Page [unclear] | Claude API Docs</transcription_page_footer>

