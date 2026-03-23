# Safety Best Practices

**Doc ID**: OAIAPI-IN73
**Goal**: Document safety best practices for OpenAI API applications - moderation, content filtering, abuse prevention
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references

## Summary

Safety best practices ensure OpenAI API applications handle content responsibly and prevent misuse. Key strategies: use the Moderation API to screen inputs and outputs, implement input validation and sanitization, limit output tokens to reduce misuse surface, narrow input/output ranges using validated fields (dropdowns, enums), use structured outputs to constrain response format, implement user identification (`user` parameter) for abuse tracking, handle safety refusals (`message.refusal` field) gracefully, monitor `finish_reason: "content_filter"` responses, apply rate limiting per user, implement human review for high-stakes outputs, use guardrails in the Agents SDK for automated safety checks. The Moderation API (POST /v1/moderations) classifies text across categories: hate, harassment, self-harm, sexual, violence, and their subcategories. Each category returns a boolean `flagged` and a confidence score. Multi-modal moderation supports both text and image inputs. Content filtering is built into all models and triggers automatically for harmful content. [VERIFIED] (OAIAPI-SC-OAI-GSAFE)

## Key Facts

- **Moderation API**: POST /v1/moderations - content classification [VERIFIED] (OAIAPI-SC-OAI-GSAFE)
- **Categories**: hate, harassment, self-harm, sexual, violence + subcategories [VERIFIED] (OAIAPI-SC-OAI-GSAFE)
- **Multi-modal**: Text and image moderation supported [VERIFIED] (OAIAPI-SC-OAI-GSAFE)
- **Content filter**: Built into all models, triggers automatically [VERIFIED] (OAIAPI-SC-OAI-GSAFE)
- **Refusal field**: `message.refusal` contains safety refusal text [VERIFIED] (OAIAPI-SC-OAI-CHATC)
- **User tracking**: `user` parameter for abuse monitoring [VERIFIED] (OAIAPI-SC-OAI-GSAFE)

## Safety Layers

```
User Input
  |
  v
1. Input Validation (length, format, sanitization)
  |
  v
2. Moderation API (content screening)
  |
  v
3. Model Generation (built-in content filter)
  |
  v
4. Output Check (refusal detection, moderation)
  |
  v
5. Application Logic (business rules, human review)
  |
  v
Safe Output
```

## Moderation API

### Request

```json
POST /v1/moderations
{
  "model": "omni-moderation-latest",
  "input": "Text to classify"
}
```

### Response

```json
{
  "id": "modr-abc123",
  "model": "omni-moderation-latest",
  "results": [
    {
      "flagged": false,
      "categories": {
        "hate": false,
        "hate/threatening": false,
        "harassment": false,
        "harassment/threatening": false,
        "self-harm": false,
        "self-harm/intent": false,
        "self-harm/instructions": false,
        "sexual": false,
        "sexual/minors": false,
        "violence": false,
        "violence/graphic": false
      },
      "category_scores": {
        "hate": 0.0001,
        "harassment": 0.0002,
        "violence": 0.0001
      }
    }
  ]
}
```

## SDK Examples (Python)

### Comprehensive Safety Pipeline

```python
from openai import OpenAI

client = OpenAI()

def moderate_content(text: str, threshold: float = 0.5) -> dict:
    """Check content against moderation categories"""
    result = client.moderations.create(
        model="omni-moderation-latest",
        input=text
    )
    
    mod = result.results[0]
    flagged_categories = []
    
    for category, score in mod.category_scores.items():
        if score > threshold:
            flagged_categories.append({"category": category, "score": score})
    
    return {
        "flagged": mod.flagged,
        "categories": flagged_categories
    }

def safe_chat(user_input: str, system_prompt: str, model: str = "gpt-5.4") -> dict:
    """Complete chat with safety checks on input and output"""
    # 1. Input validation
    if len(user_input) > 10000:
        return {"error": "Input too long", "safe": False}
    
    # 2. Input moderation
    input_mod = moderate_content(user_input)
    if input_mod["flagged"]:
        return {
            "error": "Input flagged",
            "categories": input_mod["categories"],
            "safe": False
        }
    
    # 3. Generate response
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "developer", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            max_completion_tokens=1000,
            user="user_unique_id"  # For abuse tracking
        )
    except Exception as e:
        return {"error": str(e), "safe": False}
    
    choice = response.choices[0]
    
    # 4. Check for content filter
    if choice.finish_reason == "content_filter":
        return {"error": "Content filtered by model", "safe": False}
    
    # 5. Check for refusal
    if choice.message.refusal:
        return {
            "output": choice.message.refusal,
            "refused": True,
            "safe": True
        }
    
    output = choice.message.content
    
    # 6. Output moderation
    output_mod = moderate_content(output)
    if output_mod["flagged"]:
        return {
            "error": "Output flagged",
            "categories": output_mod["categories"],
            "safe": False
        }
    
    return {"output": output, "safe": True}

# Usage
result = safe_chat(
    "How do I improve my Python code quality?",
    "You are a helpful programming assistant."
)

if result["safe"]:
    print(result.get("output", "Refused: " + result.get("error", "")))
else:
    print(f"Blocked: {result['error']}")
```

### Image Moderation

```python
from openai import OpenAI

client = OpenAI()

def moderate_image(image_url: str) -> dict:
    """Moderate an image for unsafe content"""
    result = client.moderations.create(
        model="omni-moderation-latest",
        input=[
            {"type": "image_url", "image_url": {"url": image_url}}
        ]
    )
    
    mod = result.results[0]
    return {
        "flagged": mod.flagged,
        "categories": {k: v for k, v in mod.categories.items() if v}
    }

result = moderate_image("https://example.com/image.jpg")
print(f"Flagged: {result['flagged']}")
```

## Safety Recommendations

- **Limit output tokens**: Reduce misuse surface with `max_completion_tokens`
- **Validate inputs**: Use dropdown fields, enums, and length limits where possible
- **Structured outputs**: Constrain response format to prevent free-form harmful content
- **User identification**: Always pass `user` parameter for abuse tracking
- **Rate limit per user**: Prevent individual users from excessive usage
- **Human review**: Implement for high-stakes outputs (medical, legal, financial)
- **Logging**: Retain inputs/outputs for abuse investigation (respect privacy)
- **Guardrails**: Use Agents SDK guardrails for automated input/output checks

## Error Responses

- **Moderation API**: Standard API errors (400, 401, 429)
- **Content filter**: `finish_reason: "content_filter"` in response
- **Refusal**: `message.refusal` field populated (not an error, a safety response)

## Differences from Other APIs

- **vs Anthropic**: Anthropic has constitutional AI approach; no separate moderation API endpoint
- **vs Gemini**: Google has Safety Settings with configurable thresholds per category
- **vs Grok**: Limited content moderation capabilities

## Sources

- OAIAPI-SC-OAI-GSAFE - Safety Best Practices Guide
- OAIAPI-SC-OAI-MODAPI - Moderations API Reference

## Document History

**[2026-03-20 18:56]**
- Initial documentation created
