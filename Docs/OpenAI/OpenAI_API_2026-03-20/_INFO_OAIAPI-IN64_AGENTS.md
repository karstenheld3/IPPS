# Building Agents

**Doc ID**: OAIAPI-IN64
**Goal**: Document agent architecture patterns - Agents SDK, tool use loops, handoffs, guardrails, and tracing
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references
- `_INFO_OAIAPI-IN46_SDKS.md [OAIAPI-IN46]` for Agents SDK overview

## Summary

OpenAI provides patterns and tools for building AI agents - systems that use LLMs to take actions autonomously. The Agents SDK (`openai-agents` for Python, `@openai/agents` for TypeScript) provides high-level abstractions: Agent (configured LLM with instructions, tools, handoff targets), Runner (executes agent loops), Handoff (transfer control between agents), Guardrails (input/output validation), and Tracing (built-in observability). Agent architecture follows the tool-use loop pattern: model receives input -> decides to call tools or respond -> tool results fed back -> model continues until done. The Responses API supports this natively with built-in tools (file_search, code_interpreter, web_search) and function tools. Multi-agent systems use handoffs to route conversations between specialized agents (e.g., triage -> sales, support). Agent Builder (visual canvas) enables no-code agent workflow design. Key principles: keep agents focused (single responsibility), use guardrails for safety, implement human-in-the-loop for high-stakes actions, trace all agent actions for debugging. [VERIFIED] (OAIAPI-SC-OAI-GAGNT, OAIAPI-SC-GH-AGNTPY)

## Key Facts

- **Agents SDK**: Python (`openai-agents`) and TypeScript (`@openai/agents`) [VERIFIED] (OAIAPI-SC-GH-AGNTPY)
- **Core abstractions**: Agent, Runner, Handoff, Guardrails, Tracing [VERIFIED] (OAIAPI-SC-GH-AGNTPY)
- **Tool-use loop**: Model calls tools iteratively until task complete [VERIFIED] (OAIAPI-SC-OAI-GAGNT)
- **Handoffs**: Transfer between specialized agents [VERIFIED] (OAIAPI-SC-GH-AGNTPY)
- **Agent Builder**: Visual no-code agent workflow design [VERIFIED] (OAIAPI-SC-OAI-GAGNT)
- **Built-in tools**: file_search, code_interpreter, web_search, computer_use [VERIFIED] (OAIAPI-SC-OAI-GAGNT)

## Use Cases

- **Customer service**: Triage agent routes to sales/support/billing specialists
- **Research**: Agent searches web, reads documents, synthesizes findings
- **Data analysis**: Agent writes and executes code to analyze datasets
- **Workflow automation**: Multi-step business process automation
- **Personal assistants**: Agents that manage calendar, email, tasks

## Agent Architecture Patterns

### Single Agent with Tools

```
User Input -> Agent -> [Tool Call] -> Tool Result -> Agent -> Response
                  ^                                    |
                  |____________________________________|
                         (loop until done)
```

### Multi-Agent with Handoffs

```
User Input -> Triage Agent
                |
        +---------+---------+
        |         |         |
     Sales    Support    Billing
     Agent     Agent      Agent
        |         |         |
        +----+----+---------+
             |
          Response
```

### Agent with Guardrails

```
User Input -> Input Guardrail -> Agent -> Output Guardrail -> Response
                                   |
                              [Tool Calls]
```

## SDK Examples (Python)

### Single Agent with Function Tool

```python
from agents import Agent, Runner, function_tool

@function_tool
def search_knowledge_base(query: str) -> str:
    """Search the internal knowledge base for relevant information"""
    # Implementation
    return f"Found 3 results for: {query}"

@function_tool
def create_ticket(title: str, description: str, priority: str = "medium") -> str:
    """Create a support ticket"""
    return f"Ticket created: {title} (priority: {priority})"

agent = Agent(
    name="Support Agent",
    instructions="""You are a customer support agent. 
    Search the knowledge base before answering questions.
    Create tickets for issues that need escalation.""",
    model="gpt-5.4",
    tools=[search_knowledge_base, create_ticket]
)

result = Runner.run_sync(agent, "My order hasn't arrived. Order #12345")
print(result.final_output)
```

### Multi-Agent System with Handoffs

```python
from agents import Agent, Runner

sales_agent = Agent(
    name="Sales Agent",
    instructions="Help customers with product information and purchases.",
    model="gpt-5.4",
    tools=[]  # Sales-specific tools
)

support_agent = Agent(
    name="Support Agent", 
    instructions="Help customers with technical issues and troubleshooting.",
    model="gpt-5.4",
    tools=[]  # Support-specific tools
)

billing_agent = Agent(
    name="Billing Agent",
    instructions="Help customers with billing, refunds, and account questions.",
    model="gpt-5.4",
    tools=[]  # Billing-specific tools
)

triage_agent = Agent(
    name="Triage Agent",
    instructions="""You are a triage agent. Determine the customer's need and 
    hand off to the appropriate specialist:
    - Sales: product questions, purchases, pricing
    - Support: technical issues, bugs, troubleshooting
    - Billing: invoices, refunds, payment issues""",
    model="gpt-5.4",
    handoffs=[sales_agent, support_agent, billing_agent]
)

result = Runner.run_sync(triage_agent, "I need a refund for my last purchase")
print(f"Handled by: {result.last_agent.name}")
print(result.final_output)
```

### Agent with Guardrails

```python
from agents import Agent, Runner, InputGuardrail, OutputGuardrail, GuardrailFunctionOutput

async def check_pii(ctx, agent, input_text):
    """Block requests containing personal information"""
    pii_patterns = ["ssn", "social security", "credit card"]
    for pattern in pii_patterns:
        if pattern in input_text.lower():
            return GuardrailFunctionOutput(
                output_info={"reason": "PII detected"},
                tripwire_triggered=True
            )
    return GuardrailFunctionOutput(
        output_info={"reason": "clean"},
        tripwire_triggered=False
    )

agent = Agent(
    name="Safe Agent",
    instructions="You are a helpful assistant.",
    model="gpt-5.4",
    input_guardrails=[
        InputGuardrail(guardrail_function=check_pii)
    ]
)

try:
    result = Runner.run_sync(agent, "What is my social security number?")
except Exception as e:
    print(f"Blocked: {e}")
```

### Async Agent with Tracing - Production Ready

```python
from agents import Agent, Runner, function_tool, trace
import asyncio

@function_tool
async def fetch_data(url: str) -> str:
    """Fetch data from a URL"""
    import aiohttp
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.text()

agent = Agent(
    name="Research Agent",
    instructions="Research topics by fetching relevant web pages.",
    model="gpt-5.4",
    tools=[fetch_data]
)

async def main():
    with trace("research-task"):
        result = await Runner.run(
            agent,
            "Find the latest Python release version from python.org"
        )
        print(result.final_output)
        
        # Access trace data
        for step in result.raw_responses:
            print(f"Step: {step}")

asyncio.run(main())
```

## Using Responses API Directly

Agents can be built without the SDK using the Responses API tool loop:

```python
from openai import OpenAI
import json

client = OpenAI()

def run_agent(instructions: str, user_input: str, tools: list, functions: dict):
    """Simple agent loop using Responses API"""
    response = client.responses.create(
        model="gpt-5.4",
        instructions=instructions,
        input=user_input,
        tools=tools
    )
    
    while response.output:
        # Check for tool calls
        tool_calls = [o for o in response.output if o.type == "function_call"]
        if not tool_calls:
            break
        
        # Execute tools and continue
        tool_results = []
        for call in tool_calls:
            fn = functions.get(call.name)
            if fn:
                args = json.loads(call.arguments)
                result = fn(**args)
                tool_results.append({
                    "type": "function_call_output",
                    "call_id": call.call_id,
                    "output": json.dumps(result)
                })
        
        response = client.responses.create(
            model="gpt-5.4",
            instructions=instructions,
            previous_response_id=response.id,
            input=tool_results,
            tools=tools
        )
    
    return response.output_text
```

## Error Responses

- **Agent loop limit**: Runner has configurable max iterations to prevent infinite loops
- **Guardrail tripwire**: Raises exception when guardrail is triggered
- **Tool execution errors**: Caught and fed back to model as error messages

## Differences from Other APIs

- **vs Anthropic**: Anthropic has tool use but no Agents SDK or handoff abstraction
- **vs Gemini**: Google has ADK (Agent Development Kit) with similar patterns
- **vs LangChain/LlamaIndex**: Third-party frameworks; OpenAI Agents SDK is first-party with deeper integration
- **vs CrewAI**: CrewAI focuses on multi-agent collaboration; OpenAI SDK focuses on handoffs

## Limitations and Known Issues

- **Agents SDK maturity**: Relatively new, API may evolve [VERIFIED] (OAIAPI-SC-GH-AGNTPY)
- **Loop limits**: Must configure max iterations to prevent runaway agents [VERIFIED] (OAIAPI-SC-GH-AGNTPY)
- **Tracing storage**: Built-in tracing stores to OpenAI; custom backends need configuration [ASSUMED]

## Sources

- OAIAPI-SC-OAI-GAGNT - Building Agents Guide
- OAIAPI-SC-GH-AGNTPY - Agents SDK Python (GitHub)

## Document History

**[2026-03-20 18:34]**
- Initial documentation created
