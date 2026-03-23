# Deep Research API

**Doc ID**: OAIAPI-IN67
**Goal**: Document the Deep Research API for automated multi-step research with citation-rich reports
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references

## Summary

The Deep Research API automates complex research workflows that require reasoning, planning, and synthesis across real-world information. It takes a high-level query and returns a structured, citation-rich report by leveraging an agentic model capable of decomposing tasks, searching the web, reading sources, and synthesizing findings. Uses dedicated deep research models (e.g., `o4-mini-deep-research-2025-06-26`) that plan multi-step research strategies, execute web searches, analyze sources, and produce comprehensive reports with inline citations and source metadata. Available via the Responses API with `web_search` tool. Can also be used with the Agents SDK by creating a research agent with `WebSearchTool()`. Reports include figures, statistics, data-backed reasoning, and URL citations. The API handles the full research pipeline: query decomposition -> search planning -> source retrieval -> analysis -> synthesis -> citation formatting. Designed for use cases requiring thorough, reliable research output: market analysis, academic literature review, competitive intelligence, policy research, and technical due diligence. [VERIFIED] (OAIAPI-SC-OAI-GDPRS)

## Key Facts

- **Models**: o4-mini-deep-research-2025-06-26 and variants [VERIFIED] (OAIAPI-SC-OAI-GDPRS)
- **API**: Via Responses API with web_search tool [VERIFIED] (OAIAPI-SC-OAI-GDPRS)
- **Output**: Structured reports with inline citations and source metadata [VERIFIED] (OAIAPI-SC-OAI-GDPRS)
- **Agents SDK**: Compatible with Agent/Runner pattern [VERIFIED] (OAIAPI-SC-OAI-GDPRS)
- **Pipeline**: Query -> decompose -> search -> read -> synthesize -> cite [VERIFIED] (OAIAPI-SC-OAI-GDPRS)
- **Async**: Research tasks may take minutes; use polling or streaming [VERIFIED] (OAIAPI-SC-OAI-GDPRS)

## Use Cases

- **Market analysis**: Research industry trends with data-backed findings
- **Academic review**: Literature survey with cited sources
- **Competitive intelligence**: Compare products, services, strategies
- **Policy research**: Analyze regulations, guidelines, impacts
- **Technical due diligence**: Evaluate technologies, architectures, trade-offs
- **Healthcare research**: Drug efficacy, treatment outcomes with clinical citations

## Quick Reference

```python
# Via Responses API
response = client.responses.create(
    model="o4-mini-deep-research-2025-06-26",
    tools=[{"type": "web_search"}],
    input="Research the economic impact of semaglutide on global healthcare systems"
)

# Via Agents SDK
agent = Agent(
    name="Research Agent",
    model="o4-mini-deep-research-2025-06-26",
    tools=[WebSearchTool()],
    instructions="Perform deep empirical research..."
)
```

## SDK Examples (Python)

### Basic Deep Research

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="o4-mini-deep-research-2025-06-26",
    tools=[{"type": "web_search"}],
    input="""Research the current state of quantum computing hardware.
    Include specific figures, trends, and statistics.
    Prioritize reliable sources: peer-reviewed research, company reports.
    Include inline citations and return all source metadata."""
)

print(response.output_text)

# Extract citations
for item in response.output:
    if hasattr(item, 'annotations'):
        for ann in item.annotations:
            if ann.type == "url_citation":
                print(f"  [{ann.title}]({ann.url})")
```

### Deep Research with Agents SDK

```python
from agents import Agent, Runner, WebSearchTool

research_agent = Agent(
    name="Research Agent",
    model="o4-mini-deep-research-2025-06-26",
    tools=[WebSearchTool()],
    instructions="""You perform deep empirical research based on the user query.
    Include specific figures, trends, statistics, and measurable outcomes.
    Prioritize reliable, up-to-date sources.
    Include inline citations and return all source metadata.
    Be analytical, avoid generalities."""
)

result = Runner.run_sync(
    research_agent,
    "Compare the AI agent frameworks: LangChain, CrewAI, OpenAI Agents SDK. "
    "Include adoption metrics, feature comparison, and production readiness."
)

print(result.final_output)
```

### Production Research Pipeline

```python
from openai import OpenAI
import json

client = OpenAI()

def deep_research(query: str, instructions: str = None) -> dict:
    """Execute deep research and extract structured results"""
    default_instructions = """Include specific figures, trends, and statistics.
    Prioritize reliable sources. Include inline citations.
    Be analytical and data-driven."""
    
    full_input = f"{instructions or default_instructions}\n\nResearch query: {query}"
    
    response = client.responses.create(
        model="o4-mini-deep-research-2025-06-26",
        tools=[{"type": "web_search"}],
        input=full_input
    )
    
    # Extract report and citations
    report = response.output_text
    citations = []
    
    for item in response.output:
        if hasattr(item, 'annotations'):
            for ann in item.annotations:
                if ann.type == "url_citation":
                    citations.append({
                        "title": ann.title,
                        "url": ann.url
                    })
    
    return {
        "report": report,
        "citations": citations,
        "citation_count": len(citations),
        "usage": {
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens
        }
    }

try:
    result = deep_research(
        "What are the latest advances in solid-state batteries for EVs?",
        "Focus on commercial readiness, energy density improvements, and manufacturer timelines."
    )
    
    print(f"Report length: {len(result['report'])} chars")
    print(f"Citations: {result['citation_count']}")
    print(f"Tokens: {result['usage']}")
    
    for cite in result['citations'][:5]:
        print(f"  - {cite['title']}: {cite['url']}")

except Exception as e:
    print(f"Error: {e}")
```

## Research Quality Guidelines

For best results, include in your prompt:
- **Specificity**: Name exact topics, metrics, time periods
- **Source preferences**: "peer-reviewed", "official reports", "regulatory filings"
- **Output format**: Request "inline citations", "source metadata", "data tables"
- **Analytical depth**: "avoid generalities", "data-backed reasoning"
- **Scope boundaries**: Define what to include and exclude

## Error Responses

- **400 Bad Request** - Invalid model or missing web_search tool
- **429 Too Many Requests** - Rate limit exceeded
- **500 Internal Server Error** - Research pipeline failure

## Rate Limiting / Throttling

- **Longer execution**: Deep research tasks take significantly longer than standard completions
- **Higher token usage**: Reports consume more output tokens
- **Concurrent limits**: Limited concurrent deep research tasks per organization

## Differences from Other APIs

- **vs Anthropic**: No equivalent automated deep research API
- **vs Gemini Deep Research**: Google has Deep Research in Gemini Advanced (consumer); API access differs
- **vs Perplexity**: Perplexity provides search-augmented answers but not multi-step research planning
- **vs standard web_search**: Deep research does multi-step planning and synthesis; web_search is single-query retrieval

## Limitations and Known Issues

- **Execution time**: Research tasks may take minutes, not seconds [VERIFIED] (OAIAPI-SC-OAI-GDPRS)
- **Background mode recommended**: Use `store: true` and poll or webhooks for long tasks [VERIFIED] (OAIAPI-SC-OAI-GBKGND)
- **Data retention**: Background mode retains response data for ~10 minutes only [VERIFIED] (OAIAPI-SC-OAI-GBKGND)
- **Source freshness**: Depends on web search index recency [ASSUMED]
- **Hallucination risk**: Citations should be verified for accuracy [ASSUMED]
- **Cost**: Higher token consumption than standard completions [VERIFIED] (OAIAPI-SC-OAI-GDPRS)

## Sources

- OAIAPI-SC-OAI-GDPRS - Deep Research Guide

## Document History

**[2026-03-20 19:57]**
- Added: Background mode and data retention limitations

**[2026-03-20 18:40]**
- Initial documentation created
