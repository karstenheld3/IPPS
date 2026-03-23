# Function Calling

**Doc ID**: OAIAPI-IN13
**Goal**: Document function calling with JSON schema, strict mode, tool_choice, and parallel calls
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references
- `_INFO_OAIAPI-IN12_TOOLS_OVERVIEW.md [OAIAPI-IN12]` for tools context

## Summary

Function calling enables models to invoke developer-defined functions by generating structured JSON arguments matching function schema. Define functions with name, description, and JSON Schema parameters. Model determines when to call functions based on context, generates arguments as JSON string, and returns tool_call object with function name and arguments. Developer executes function in application code, submits results back to API, and model uses results to generate final response. Strict mode enforces schema compliance with constrained sampling - when enabled, model output guaranteed to match schema exactly. Parallel function calls allow multiple invocations in single response. Functions support all JSON Schema types, nested objects, arrays, enums, and descriptions for parameters. [VERIFIED] (OAIAPI-SC-OAI-GFNCAL, OAIAPI-SC-OAI-GSTRCT)

## Key Facts

- **Schema format**: JSON Schema for parameter definition [VERIFIED] (OAIAPI-SC-OAI-GFNCAL)
- **Strict mode**: Guarantees schema-compliant output [VERIFIED] (OAIAPI-SC-OAI-GSTRCT)
- **Parallel calls**: Multiple functions invoked simultaneously [VERIFIED] (OAIAPI-SC-OAI-GFNCAL)
- **tool_choice**: Control when functions called [VERIFIED] (OAIAPI-SC-OAI-GTOOLS)
- **Execution**: Developer executes, model doesn't run functions [VERIFIED] (OAIAPI-SC-OAI-GFNCAL)

## Use Cases

- **API integration**: Call external APIs (weather, databases, CRM)
- **Data retrieval**: Query internal systems and databases
- **Actions**: Trigger operations (send email, create ticket, update record)
- **Calculations**: Delegate computations to specialized functions
- **Validation**: Ensure structured data extraction

## Quick Reference

```python
tools=[
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"]
                    }
                },
                "required": ["location"]
            },
            "strict": True
        }
    }
]
```

## Function Definition Schema

### Required Fields

- **name**: Function identifier (letters, numbers, underscores)
- **description**: What the function does (helps model decide when to call)
- **parameters**: JSON Schema defining function arguments

### Optional Fields

- **strict**: Enable strict mode (boolean, default: false)

### Parameters Schema

Standard JSON Schema with supported types:
- **string**: Text values
- **number**: Numeric values
- **integer**: Whole numbers
- **boolean**: true/false
- **object**: Nested structures
- **array**: Lists
- **enum**: Constrained choices
- **null**: Null values

## Strict Mode

### Enabling Strict Mode

```python
{
    "type": "function",
    "function": {
        "name": "extract_data",
        "parameters": {...},
        "strict": True  # Enable strict mode
    }
}
```

### Benefits

- **Guaranteed compliance**: Output matches schema exactly
- **No validation needed**: Trust model output structure
- **Reliable parsing**: JSON.parse never fails
- **Type safety**: All types enforced

### Restrictions

Strict mode requires:
- All objects have `additionalProperties: false`
- All required fields specified
- No `anyOf`, `allOf`, `oneOf` (use single schema)
- Enums for constrained choices

## Function Calling Flow

### 1. Define Function

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_user",
            "description": "Retrieve user by ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"}
                },
                "required": ["user_id"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
]
```

### 2. Model Calls Function

```json
{
  "tool_calls": [
    {
      "id": "call_abc123",
      "type": "function",
      "function": {
        "name": "get_user",
        "arguments": "{\"user_id\":\"12345\"}"
      }
    }
  ]
}
```

### 3. Execute Function

```python
import json

arguments = json.loads(tool_call.function.arguments)
result = get_user(arguments["user_id"])
```

### 4. Return Result

```python
{
    "role": "tool",
    "tool_call_id": "call_abc123",
    "content": json.dumps(result)
}
```

### 5. Model Uses Result

Model incorporates function result into final response.

## Parallel Function Calls

Model can call multiple functions simultaneously:

```json
{
  "tool_calls": [
    {
      "id": "call_1",
      "function": {"name": "get_weather", "arguments": "{\"location\":\"Paris\"}"}
    },
    {
      "id": "call_2",
      "function": {"name": "get_weather", "arguments": "{\"location\":\"London\"}"}
    },
    {
      "id": "call_3",
      "function": {"name": "get_weather", "arguments": "{\"location\":\"Tokyo\"}"}
    }
  ]
}
```

Execute all and return all results.

## SDK Examples (Python)

### Basic Function Calling

```python
from openai import OpenAI
import json

client = OpenAI()

def get_current_weather(location: str, unit: str = "celsius"):
    """Simulate weather API"""
    return {
        "location": location,
        "temperature": 22,
        "unit": unit,
        "conditions": "Sunny"
    }

# Define function
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city name, e.g. San Francisco"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"]
                    }
                },
                "required": ["location"]
            }
        }
    }
]

# Initial request
response = client.responses.create(
    model="gpt-5.4",
    input=[
        {"role": "user", "content": "What's the weather like in Boston?"}
    ],
    tools=tools
)

# Check for tool calls
if hasattr(response.output[0], 'tool_calls'):
    tool_call = response.output[0].tool_calls[0]
    
    # Parse arguments
    arguments = json.loads(tool_call.function.arguments)
    
    # Execute function
    result = get_current_weather(**arguments)
    
    # Return result to model
    final_response = client.responses.create(
        model="gpt-5.4",
        input=[
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            }
        ]
    )
    
    print(final_response.output[0].content[0].text)
```

### Strict Mode Function

```python
from openai import OpenAI
import json

client = OpenAI()

tools = [
    {
        "type": "function",
        "function": {
            "name": "extract_person",
            "description": "Extract person information",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "integer"},
                    "email": {"type": "string"}
                },
                "required": ["name", "age"],
                "additionalProperties": False
            },
            "strict": True  # Guaranteed schema compliance
        }
    }
]

response = client.responses.create(
    model="gpt-5.4",
    input=[
        {"role": "user", "content": "Extract: John Smith is 30 years old, email: john@example.com"}
    ],
    tools=tools,
    tool_choice="required"
)

tool_call = response.output[0].tool_calls[0]
data = json.loads(tool_call.function.arguments)

# Guaranteed to have name and age, email optional
print(f"Name: {data['name']}, Age: {data['age']}")
```

### Multiple Functions

```python
from openai import OpenAI
import json

client = OpenAI()

def get_weather(location):
    return f"Sunny in {location}"

def get_time(timezone):
    return f"Current time in {timezone}: 14:30"

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather for location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"}
                },
                "required": ["location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "Get current time for timezone",
            "parameters": {
                "type": "object",
                "properties": {
                    "timezone": {"type": "string"}
                },
                "required": ["timezone"]
            }
        }
    }
]

response = client.responses.create(
    model="gpt-5.4",
    input=[
        {"role": "user", "content": "What's the weather and time in Tokyo?"}
    ],
    tools=tools
)

# Handle multiple parallel calls
if hasattr(response.output[0], 'tool_calls'):
    results = []
    for call in response.output[0].tool_calls:
        args = json.loads(call.function.arguments)
        
        if call.function.name == "get_weather":
            result = get_weather(args["location"])
        elif call.function.name == "get_time":
            result = get_time(args["timezone"])
        
        results.append({
            "role": "tool",
            "tool_call_id": call.id,
            "content": result
        })
    
    final = client.responses.create(
        model="gpt-5.4",
        input=results
    )
    
    print(final.output[0].content[0].text)
```

### Production Function Handler

```python
from openai import OpenAI
import json
from typing import Callable, Dict

class FunctionHandler:
    def __init__(self):
        self.client = OpenAI()
        self.functions: Dict[str, Callable] = {}
    
    def register(self, name: str, func: Callable):
        """Register function implementation"""
        self.functions[name] = func
    
    def call_with_functions(self, prompt: str, tools: list):
        """Execute prompt with function calling"""
        response = self.client.responses.create(
            model="gpt-5.4",
            input=[{"role": "user", "content": prompt}],
            tools=tools
        )
        
        # Handle tool calls
        if hasattr(response.output[0], 'tool_calls'):
            tool_results = []
            
            for call in response.output[0].tool_calls:
                func = self.functions.get(call.function.name)
                if not func:
                    raise ValueError(f"Unknown function: {call.function.name}")
                
                args = json.loads(call.function.arguments)
                result = func(**args)
                
                tool_results.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": json.dumps(result) if not isinstance(result, str) else result
                })
            
            # Get final response
            final = self.client.responses.create(
                model="gpt-5.4",
                input=tool_results
            )
            
            return final.output[0].content[0].text
        
        return response.output[0].content[0].text

# Usage
handler = FunctionHandler()

handler.register("get_weather", lambda location: f"Sunny in {location}")
handler.register("get_time", lambda timezone: f"14:30 in {timezone}")

tools = [...]  # Define tools
result = handler.call_with_functions("What's the weather in Paris?", tools)
print(result)
```

## Error Responses

- **400 Bad Request** - Invalid function schema or arguments
- **Parsing errors** - Malformed JSON in function arguments (strict mode prevents this)

## Rate Limiting / Throttling

- **Function calls count**: Token usage includes function definitions and arguments
- **Tool usage limits**: Some models have max tools per request

## Differences from Other APIs

- **vs Anthropic Tools**: Similar structure, Anthropic uses `tools` array too
- **vs Gemini Function Calling**: Gemini uses `function_declarations`, similar concept
- **vs Legacy Functions**: Old `functions` array replaced by `tools` with `type: function`

## Limitations and Known Issues

- **No function execution**: Model only generates arguments, doesn't run functions [VERIFIED] (OAIAPI-SC-OAI-GFNCAL)
- **Strict mode limitations**: No complex schema features (anyOf, allOf, oneOf) [VERIFIED] (OAIAPI-SC-OAI-GSTRCT)
- **Description quality matters**: Poor descriptions reduce accuracy [COMMUNITY] (OAIAPI-SC-SO-FUNCDESC)

## Gotchas and Quirks

- **Arguments as string**: function.arguments is JSON string, not object [VERIFIED] (OAIAPI-SC-OAI-GFNCAL)
- **Tool result must be string**: content field expects string, stringify objects [VERIFIED] (OAIAPI-SC-OAI-GFNCAL)
- **Parallel calls optional**: Model decides, not controllable [VERIFIED] (OAIAPI-SC-OAI-GFNCAL)

## Sources

- OAIAPI-SC-OAI-GFNCAL - Function calling guide
- OAIAPI-SC-OAI-GSTRCT - Structured outputs guide
- OAIAPI-SC-OAI-GTOOLS - Tools overview

## Document History

**[2026-03-20 15:28]**
- Initial documentation created
