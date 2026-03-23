# Moderation API

**Doc ID**: OAIAPI-IN24
**Goal**: Document content moderation API with omni-moderation models and category detection
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references

## Summary

OpenAI Moderation API (POST /v1/moderations) classifies text and images for policy-violating content. Model omni-moderation-latest supports multi-modal input (text + images). Returns category flags and confidence scores for: hate, hate/threatening, harassment, harassment/threatening, self-harm, self-harm/intent, self-harm/instructions, sexual, sexual/minors, violence, violence/graphic. Boolean flagged field indicates if content violates policy. Scores 0-1 represent confidence - higher = more likely violating. Use for UGC filtering, content review, compliance. Free to use for OpenAI API customers. Recommended: check all user inputs and model outputs. Multi-language support. Updates without API changes - latest model automatically improves. [VERIFIED] (OAIAPI-SC-OAI-MODCRT, OAIAPI-SC-OAI-GMOD)

## Key Facts

- **Endpoint**: POST /v1/moderations [VERIFIED] (OAIAPI-SC-OAI-MODCRT)
- **Model**: omni-moderation-latest (multi-modal) [VERIFIED] (OAIAPI-SC-OAI-MODCRT)
- **Input**: Text and/or images [VERIFIED] (OAIAPI-SC-OAI-MODCRT)
- **Categories**: 11 policy categories [VERIFIED] (OAIAPI-SC-OAI-MODCRT)
- **Free**: No cost for API customers [VERIFIED] (OAIAPI-SC-OAI-GMOD)

## Use Cases

- **UGC filtering**: Filter user-generated content
- **Content review**: Flag content for human review
- **Compliance**: Enforce platform policies
- **Safety**: Protect users from harmful content
- **Output validation**: Check model-generated content

## Quick Reference

```python
POST /v1/moderations
{
  "model": "omni-moderation-latest",
  "input": [
    {"type": "text", "text": "Sample text"},
    {"type": "image_url", "image_url": {"url": "https://..."}}
  ]
}
```

## Content Categories

### hate
- **Description**: Content promoting hatred based on protected characteristics
- **Examples**: Slurs, derogatory content targeting race, religion, gender, etc.

### hate/threatening
- **Description**: Hateful content including threats or violence
- **Examples**: Calls for violence against groups

### harassment
- **Description**: Bullying, intimidation, mockery
- **Examples**: Personal attacks, doxxing threats

### harassment/threatening
- **Description**: Harassment including threats
- **Examples**: Threats of violence against individuals

### self-harm
- **Description**: Content promoting self-harm
- **Examples**: Encouragement of cutting, suicide

### self-harm/intent
- **Description**: Expresses intent to self-harm
- **Examples**: Suicide notes, self-harm plans

### self-harm/instructions
- **Description**: Instructions on self-harm methods
- **Examples**: How-to guides for self-harm

### sexual
- **Description**: Sexual content
- **Examples**: Explicit sexual descriptions, adult content

### sexual/minors
- **Description**: Sexual content involving minors
- **Examples**: Any sexualization of children

### violence
- **Description**: Content promoting or glorifying violence
- **Examples**: Graphic violence descriptions, torture

### violence/graphic
- **Description**: Extremely graphic violent content
- **Examples**: Gore, graphic injury descriptions

## Request Format

### Text Only

```json
{
  "model": "omni-moderation-latest",
  "input": "Text to moderate"
}
```

### Text + Images

```json
{
  "model": "omni-moderation-latest",
  "input": [
    {
      "type": "text",
      "text": "Text to moderate"
    },
    {
      "type": "image_url",
      "image_url": {
        "url": "https://example.com/image.jpg"
      }
    }
  ]
}
```

### Multiple Inputs

```json
{
  "model": "omni-moderation-latest",
  "input": [
    "First text to check",
    "Second text to check"
  ]
}
```

## Response Format

```json
{
  "id": "modr_abc123",
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
        "hate": 0.001,
        "hate/threatening": 0.0001,
        "harassment": 0.002,
        "harassment/threatening": 0.0001,
        "self-harm": 0.0001,
        "self-harm/intent": 0.0001,
        "self-harm/instructions": 0.0001,
        "sexual": 0.001,
        "sexual/minors": 0.0001,
        "violence": 0.001,
        "violence/graphic": 0.0001
      }
    }
  ]
}
```

### Response Fields

- **flagged**: True if content violates policy
- **categories**: Boolean flags per category
- **category_scores**: Confidence scores (0-1) per category

## SDK Examples (Python)

### Basic Text Moderation

```python
from openai import OpenAI

client = OpenAI()

response = client.moderations.create(
    model="omni-moderation-latest",
    input="This is a sample text to moderate"
)

result = response.results[0]

if result.flagged:
    print("Content flagged for moderation")
    for category, flagged in result.categories.items():
        if flagged:
            score = result.category_scores[category]
            print(f"  {category}: {score:.4f}")
else:
    print("Content passed moderation")
```

### Multi-Modal Moderation

```python
from openai import OpenAI

client = OpenAI()

response = client.moderations.create(
    model="omni-moderation-latest",
    input=[
        {
            "type": "text",
            "text": "Check this content"
        },
        {
            "type": "image_url",
            "image_url": {
                "url": "https://example.com/user-upload.jpg"
            }
        }
    ]
)

result = response.results[0]
print(f"Flagged: {result.flagged}")
```

### Batch Moderation

```python
from openai import OpenAI

client = OpenAI()

texts = [
    "First user comment",
    "Second user comment",
    "Third user comment"
]

response = client.moderations.create(
    model="omni-moderation-latest",
    input=texts
)

for i, result in enumerate(response.results):
    print(f"Text {i+1}: {'FLAGGED' if result.flagged else 'OK'}")
```

### Category-Specific Filtering

```python
from openai import OpenAI

client = OpenAI()

def check_for_violence(text: str) -> bool:
    """Check if text contains violence"""
    response = client.moderations.create(
        model="omni-moderation-latest",
        input=text
    )
    
    result = response.results[0]
    return result.categories.get("violence", False) or \
           result.categories.get("violence/graphic", False)

# Usage
if check_for_violence("Sample text"):
    print("Violence detected")
```

### Score-Based Filtering

```python
from openai import OpenAI

client = OpenAI()

def moderate_with_threshold(text: str, threshold: float = 0.5) -> dict:
    """Moderate with custom threshold"""
    response = client.moderations.create(
        model="omni-moderation-latest",
        input=text
    )
    
    result = response.results[0]
    
    violations = []
    for category, score in result.category_scores.items():
        if score >= threshold:
            violations.append({
                "category": category,
                "score": score,
                "flagged": result.categories[category]
            })
    
    return {
        "flagged": result.flagged,
        "violations": violations
    }

# Usage
result = moderate_with_threshold("Sample text", threshold=0.3)
if result["violations"]:
    print(f"Found {len(result['violations'])} violations")
```

### UGC Filter

```python
from openai import OpenAI
from typing import Optional

class ContentFilter:
    def __init__(self, strict_mode: bool = True):
        self.client = OpenAI()
        self.strict_mode = strict_mode
    
    def filter(self, content: str) -> dict:
        """Filter user-generated content"""
        response = self.client.moderations.create(
            model="omni-moderation-latest",
            input=content
        )
        
        result = response.results[0]
        
        if self.strict_mode:
            # Block if any category flagged
            allowed = not result.flagged
        else:
            # Block only severe categories
            severe_categories = [
                "sexual/minors",
                "hate/threatening",
                "harassment/threatening",
                "self-harm/intent",
                "violence/graphic"
            ]
            allowed = not any(result.categories.get(cat, False) 
                            for cat in severe_categories)
        
        return {
            "allowed": allowed,
            "flagged": result.flagged,
            "categories": result.categories,
            "scores": result.category_scores
        }

# Usage
filter = ContentFilter(strict_mode=True)
result = filter.filter("User comment here")

if result["allowed"]:
    print("Content approved")
else:
    print("Content blocked")
```

### Production Moderation Service

```python
from openai import OpenAI
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class ModerationService:
    def __init__(self):
        self.client = OpenAI()
    
    def moderate_text(self, text: str) -> Dict:
        """Moderate single text"""
        try:
            response = self.client.moderations.create(
                model="omni-moderation-latest",
                input=text
            )
            return self._format_result(response.results[0])
        except Exception as e:
            logger.error(f"Moderation error: {e}")
            # Fail closed - block content on error
            return {"allowed": False, "error": str(e)}
    
    def moderate_batch(self, texts: List[str]) -> List[Dict]:
        """Moderate multiple texts"""
        try:
            response = self.client.moderations.create(
                model="omni-moderation-latest",
                input=texts
            )
            return [self._format_result(r) for r in response.results]
        except Exception as e:
            logger.error(f"Batch moderation error: {e}")
            return [{"allowed": False, "error": str(e)} for _ in texts]
    
    def _format_result(self, result) -> Dict:
        """Format moderation result"""
        return {
            "allowed": not result.flagged,
            "flagged": result.flagged,
            "categories": {k: v for k, v in result.categories.items() if v},
            "top_scores": sorted(
                result.category_scores.items(),
                key=lambda x: x[1],
                reverse=True
            )[:3]
        }

# Usage
service = ModerationService()

# Single text
result = service.moderate_text("User input")
if not result["allowed"]:
    print(f"Blocked: {result['categories']}")

# Batch
batch_results = service.moderate_batch([
    "Comment 1",
    "Comment 2",
    "Comment 3"
])
```

## Error Responses

- **400 Bad Request** - Invalid input format
- **429 Too Many Requests** - Rate limit exceeded (rare, generous limits)

## Rate Limiting / Throttling

- **Free for API customers**: No cost
- **Generous limits**: High rate limits
- **Batch processing**: Multiple inputs per request

## Differences from Other APIs

- **vs Perspective API**: OpenAI multi-modal, Perspective text-only
- **vs Azure Content Safety**: Similar capabilities, different categories
- **vs AWS Rekognition**: AWS image-focused, OpenAI multi-modal

## Limitations and Known Issues

- **Language coverage**: Best for English, supports others [COMMUNITY] (OAIAPI-SC-SO-MODLANG)
- **Context-dependent**: May miss context-specific violations [COMMUNITY] (OAIAPI-SC-SO-MODCTX)
- **False positives**: Some legitimate content flagged [COMMUNITY] (OAIAPI-SC-SO-MODFP)

## Gotchas and Quirks

- **Auto-updates**: Model improves without API changes [VERIFIED] (OAIAPI-SC-OAI-GMOD)
- **Threshold tuning**: May need custom thresholds for use case [COMMUNITY] (OAIAPI-SC-SO-MODTHR)
- **Combined scores**: Text + image scored together in multi-modal [VERIFIED] (OAIAPI-SC-OAI-MODCRT)

## Sources

- OAIAPI-SC-OAI-MODCRT - POST Create moderation
- OAIAPI-SC-OAI-GMOD - Moderation guide

## Document History

**[2026-03-20 15:55]**
- Initial documentation created
