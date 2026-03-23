# Web Search Tool

**Doc ID**: OAIAPI-IN14
**Goal**: Document web search tool configuration, deep research models, and real-time web access
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references
- `_INFO_OAIAPI-IN12_TOOLS_OVERVIEW.md [OAIAPI-IN12]` for tools context

## Summary

The web_search tool enables real-time web access for current information, news, and facts beyond model training data. Configure with max_results parameter to control number of search results. Models perform web searches, extract relevant information, synthesize results, and cite sources in responses. Deep research models (o3-deep-research, o4-mini-deep-research) use web_search with background mode for comprehensive multi-hour research tasks, following iterative search patterns. Web search queries generated automatically by model based on context. Results include URLs, snippets, and metadata. Search context used to augment model knowledge for grounded responses. Supports all text generation models. No additional API key required - web search included with OpenAI API access. [VERIFIED] (OAIAPI-SC-OAI-GWBSRC, OAIAPI-SC-OAI-GDEEP)

## Key Facts

- **Type**: Built-in tool (type: "web_search") [VERIFIED] (OAIAPI-SC-OAI-GWBSRC)
- **Purpose**: Real-time web information access [VERIFIED] (OAIAPI-SC-OAI-GWBSRC)
- **Configuration**: max_results parameter (default: 5-10) [VERIFIED] (OAIAPI-SC-OAI-GWBSRC)
- **Deep research**: o3-deep-research, o4-mini-deep-research models [VERIFIED] (OAIAPI-SC-OAI-GDEEP)
- **Citations**: Model includes source URLs in responses [VERIFIED] (OAIAPI-SC-OAI-GWBSRC)

## Use Cases

- **Current events**: Latest news, breaking stories
- **Real-time data**: Stock prices, weather, sports scores
- **Fact checking**: Verify claims against web sources
- **Research**: Comprehensive information gathering
- **Knowledge updates**: Information beyond training cutoff

## Quick Reference

```python
tools=[
    {
        "type": "web_search",
        "web_search": {
            "max_results": 10
        }
    }
]

# Deep research
model="o3-deep-research"
background={"enabled": True}
```

## Configuration

### Basic Configuration

```python
{
    "type": "web_search"
}
```

Uses default settings (5-10 results).

### Advanced Configuration

```python
{
    "type": "web_search",
    "web_search": {
        "max_results": 20
    }
}
```

**Parameters:**
- **max_results**: Maximum search results to retrieve (1-50, default: 5-10)

## Web Search Behavior

### Automatic Query Generation

Model generates search queries based on:
- User question context
- Information gaps
- Need for current data
- Fact verification requirements

### Search Process

1. **Model identifies need**: Determines web search required
2. **Query generation**: Formulates search query
3. **Search execution**: OpenAI performs web search
4. **Result retrieval**: Gets top N results
5. **Context integration**: Incorporates results into response
6. **Citation**: Includes source URLs

### Result Format

Search results include:
- **URL**: Source web page
- **Title**: Page title
- **Snippet**: Relevant excerpt
- **Metadata**: Publication date, domain

## Deep Research Models

### o3-deep-research

**Purpose:** Comprehensive multi-hour research tasks
**Context window:** Large (supports extensive research)
**Background mode:** Required for full capability
**Search pattern:** Iterative queries, cross-referencing
**Output:** Detailed research report with citations

### o4-mini-deep-research

**Purpose:** Faster research for everyday tasks
**Context window:** Smaller than o3-deep-research
**Background mode:** Recommended
**Search pattern:** Focused queries
**Output:** Concise research summary

### Research Workflow

```python
# Start deep research
response = client.responses.create(
    model="o3-deep-research",
    input=[
        {"role": "user", "content": "Research quantum computing trends 2025-2026"}
    ],
    tools=[{"type": "web_search"}],
    background={"enabled": True}
)

# Poll for completion (can take hours)
while response.status == "in_progress":
    time.sleep(60)  # Check every minute
    response = client.responses.retrieve(response.id)
```

## SDK Examples (Python)

### Basic Web Search

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-5.4",
    input=[
        {"role": "user", "content": "What are the latest developments in AI safety?"}
    ],
    tools=[
        {"type": "web_search"}
    ]
)

print(response.output[0].content[0].text)
# Includes citations like: "According to [Source](URL), ..."
```

### Web Search with Max Results

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-5.4",
    input=[
        {"role": "user", "content": "Compare electric vehicle market leaders"}
    ],
    tools=[
        {
            "type": "web_search",
            "web_search": {
                "max_results": 20  # More comprehensive search
            }
        }
    ]
)

print(response.output[0].content[0].text)
```

### Deep Research Task

```python
from openai import OpenAI
import time

client = OpenAI()

# Initiate deep research
response = client.responses.create(
    model="o3-deep-research",
    input=[
        {
            "role": "user",
            "content": "Conduct comprehensive research on renewable energy adoption trends, policy changes, and market forecasts for 2026-2030"
        }
    ],
    tools=[
        {
            "type": "web_search",
            "web_search": {
                "max_results": 30
            }
        }
    ],
    background={"enabled": True}
)

print(f"Research task started: {response.id}")
print("Status: in_progress (this may take 1-4 hours)")

# Poll for completion
while response.status == "in_progress":
    time.sleep(120)  # Check every 2 minutes
    response = client.responses.retrieve(response.id)
    print(f"Status: {response.status}")

print("\n=== Research Report ===")
print(response.output[0].content[0].text)
```

### Fact Checking with Web Search

```python
from openai import OpenAI

client = OpenAI()

def fact_check(claim: str) -> str:
    """Verify claim using web search"""
    response = client.responses.create(
        model="gpt-5.4",
        input=[
            {
                "role": "user",
                "content": f"Fact check this claim using web sources: {claim}"
            }
        ],
        tools=[{"type": "web_search"}]
    )
    
    return response.output[0].content[0].text

# Usage
claim = "The James Webb Space Telescope launched in December 2021"
result = fact_check(claim)
print(result)
# Output includes: "Verified: According to [NASA](URL), JWST launched on December 25, 2021..."
```

### Current Events Summary

```python
from openai import OpenAI

client = OpenAI()

def get_news_summary(topic: str, max_results: int = 15):
    """Get current news summary on topic"""
    response = client.responses.create(
        model="gpt-5.4",
        input=[
            {
                "role": "user",
                "content": f"Summarize the latest news and developments about {topic}"
            }
        ],
        tools=[
            {
                "type": "web_search",
                "web_search": {
                    "max_results": max_results
                }
            }
        ]
    )
    
    return response.output[0].content[0].text

# Usage
summary = get_news_summary("artificial intelligence regulation")
print(summary)
```

### Web Search + Function Calling

```python
from openai import OpenAI
import json

client = OpenAI()

response = client.responses.create(
    model="gpt-5.4",
    input=[
        {
            "role": "user",
            "content": "Search for recent AI news and save the top 3 headlines to database"
        }
    ],
    tools=[
        {"type": "web_search"},
        {
            "type": "function",
            "function": {
                "name": "save_headlines",
                "description": "Save headlines to database",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "headlines": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    },
                    "required": ["headlines"]
                }
            }
        }
    ]
)

# Model may first search web, then call function with results
```

## Error Responses

- **400 Bad Request** - Invalid web_search configuration
- **429 Too Many Requests** - Web search quota exceeded
- **503 Service Unavailable** - Web search service temporarily unavailable

## Rate Limiting / Throttling

- **Search quota**: Limited web searches per project/tier
- **Token counting**: Search results count toward TPM limits
- **Background tasks**: Deep research has separate quotas

## Differences from Other APIs

- **vs Anthropic**: Anthropic has no built-in web search (requires integration)
- **vs Gemini**: Gemini has Google Search grounding, similar concept
- **vs Perplexity**: Perplexity specializes in search-grounded responses, OpenAI is general-purpose

## Limitations and Known Issues

- **Search result quality**: Depends on web search provider [COMMUNITY] (OAIAPI-SC-SO-WEBSRCH)
- **Deep research time**: Can take 1-4 hours [VERIFIED] (OAIAPI-SC-OAI-GDEEP)
- **No search history**: Cannot access past searches [COMMUNITY] (OAIAPI-SC-SO-SRCHHIST)

## Gotchas and Quirks

- **Automatic queries**: Model decides search queries, not controllable [VERIFIED] (OAIAPI-SC-OAI-GWBSRC)
- **Citation format varies**: No standardized citation format [COMMUNITY] (OAIAPI-SC-SO-CITE)
- **Recency not guaranteed**: Search results may not be real-time [COMMUNITY] (OAIAPI-SC-SO-RECENCY)

## Sources

- OAIAPI-SC-OAI-GWBSRC - Web search guide
- OAIAPI-SC-OAI-GDEEP - Deep research guide
- OAIAPI-SC-OAI-GTOOLS - Tools overview

## Document History

**[2026-03-20 15:30]**
- Initial documentation created
