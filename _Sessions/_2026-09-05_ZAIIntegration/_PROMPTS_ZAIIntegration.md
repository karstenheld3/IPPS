---
intended_model: glm-5.2
context_window_size: 200k
reasoning_settings: high
prompt_system: IPPS
api_docs_path: e:\Dev\KarstensWorkspace\knowledge\Zhipu\ZAI_API_2026-09-05
---

<!-- SOURCE: Full Z.AI API documentation at e:\Dev\KarstensWorkspace\knowledge\Zhipu\ZAI_API_2026-09-05 - read these docs to verify any model details, pricing, parameters, or API behavior before making changes. -->

## Prompt 1 - Update model-registry.json

```
Add 16 Z.AI (GLM) generation 4 and 5 models to the "models" array and 6 prefix entries to the "model_id_startswith" array in E:\Dev\IPPS\DevSystemV4.3\skills\llm-evaluation\model-registry.json. Do NOT add glm-4-32b-0414-128k or any pre-gen-4 models.

Add these 16 entries to the "models" array (after the last anthropic entry):

{"provider": "zai", "model_id": "glm-5.3", "name": "GLM-5.3", "context_window": 1000000, "enabled": true, "status": "available"},
{"provider": "zai", "model_id": "glm-5.3-flash", "name": "GLM-5.3 Flash", "context_window": 1000000, "enabled": true, "status": "available"},
{"provider": "zai", "model_id": "glm-5.2", "name": "GLM-5.2", "context_window": 1000000, "enabled": true, "status": "available"},
{"provider": "zai", "model_id": "glm-5.1", "name": "GLM-5.1", "context_window": 1000000, "enabled": true, "status": "available"},
{"provider": "zai", "model_id": "glm-5", "name": "GLM-5", "context_window": 1000000, "enabled": true, "status": "available"},
{"provider": "zai", "model_id": "glm-4.7", "name": "GLM-4.7", "context_window": 128000, "enabled": true, "status": "available"},
{"provider": "zai", "model_id": "glm-4.7-flashx", "name": "GLM-4.7 FlashX", "context_window": 128000, "enabled": true, "status": "available"},
{"provider": "zai", "model_id": "glm-4.7-flash", "name": "GLM-4.7 Flash", "context_window": 128000, "enabled": true, "status": "available"},
{"provider": "zai", "model_id": "glm-4.6", "name": "GLM-4.6", "context_window": 128000, "enabled": true, "status": "available"},
{"provider": "zai", "model_id": "glm-4.6v", "name": "GLM-4.6V", "context_window": 128000, "enabled": true, "status": "available"},
{"provider": "zai", "model_id": "glm-4.5v", "name": "GLM-4.5V", "context_window": 128000, "enabled": true, "status": "available"},
{"provider": "zai", "model_id": "glm-4.5-x", "name": "GLM-4.5-X", "context_window": 128000, "enabled": true, "status": "available"},
{"provider": "zai", "model_id": "glm-4.5-flash", "name": "GLM-4.5 Flash", "context_window": 200000, "enabled": true, "status": "available"},
{"provider": "zai", "model_id": "glm-4.5-airx", "name": "GLM-4.5 AirX", "context_window": 128000, "enabled": true, "status": "available"},
{"provider": "zai", "model_id": "glm-4.5", "name": "GLM-4.5", "context_window": 128000, "enabled": true, "status": "available"},
{"provider": "zai", "model_id": "glm-4-air", "name": "GLM-4 Air", "context_window": 128000, "enabled": true, "status": "available"}

Add these 6 entries to the "model_id_startswith" array (after the last claude- entry). Order is critical - most specific prefix first:

{ "prefix": "glm-5.3-flash", "provider": "zai", "method": "zai_reasoning", "max_input": 1000000, "max_output": 16384, "effort": ["low", "high", "max"], "default": "high", "seed": false },
{ "prefix": "glm-5.3", "provider": "zai", "method": "zai_reasoning", "max_input": 1000000, "max_output": 16384, "effort": ["low", "high", "max"], "default": "high", "seed": false },
{ "prefix": "glm-5.2", "provider": "zai", "method": "zai_reasoning", "max_input": 1000000, "max_output": 16384, "effort": ["none", "minimal", "low", "medium", "high", "xhigh", "max"], "default": "high", "seed": false },
{ "prefix": "glm-5", "provider": "zai", "method": "zai_thinking", "max_input": 1000000, "max_output": 16384, "seed": false },
{ "prefix": "glm-4.5-flash", "provider": "zai", "method": "zai_thinking", "max_input": 200000, "max_output": 8192, "seed": false },
{ "prefix": "glm-4", "provider": "zai", "method": "zai_thinking", "max_input": 128000, "max_output": 8192, "seed": false }

Also bump _version to "1.9.0" and update _updated to "2026-09-05".

Constraints:
- Do NOT modify any existing openai or anthropic entries
- Do NOT add glm-4-32b-0414-128k or any pre-gen-4 models
- Preserve existing JSON structure and formatting style
- The glm-4.5-flash prefix MUST come before glm-4 (200K vs 128K context)
- The glm-5.3-flash prefix MUST come before glm-5.3 (more specific first)

Verify: JSON is valid. "models" array has 16 new zai entries. "model_id_startswith" array has 6 new glm- entries. No existing entries modified.
```

---

## Prompt 2 - Update model-pricing.json and model-parameter-mapping.json

<!-- Previous step added 16 Z.AI models and 6 prefixes to model-registry.json. -->

````
Add Z.AI pricing data to E:\Dev\IPPS\DevSystemV4.3\skills\llm-evaluation\model-pricing.json and Z.AI parameter mappings to E:\Dev\IPPS\DevSystemV4.3\skills\llm-evaluation\model-parameter-mapping.json.

In model-pricing.json, add a "zai" key inside the "pricing" object (after the "anthropic" block) with these 16 model entries:

"zai": {
  "glm-5.3": {"input_per_1m": 1.40, "cached_per_1m": 0.26, "output_per_1m": 4.40, "context_window_k": 1000, "currency": "USD"},
  "glm-5.3-flash": {"input_per_1m": 0.15, "cached_per_1m": 0.03, "output_per_1m": 0.50, "context_window_k": 1000, "currency": "USD"},
  "glm-5.2": {"input_per_1m": 1.40, "cached_per_1m": 0.26, "output_per_1m": 4.40, "context_window_k": 1000, "currency": "USD"},
  "glm-5.1": {"input_per_1m": 1.40, "cached_per_1m": 0.26, "output_per_1m": 4.40, "context_window_k": 1000, "currency": "USD"},
  "glm-5": {"input_per_1m": 1.00, "cached_per_1m": 0.20, "output_per_1m": 3.20, "context_window_k": 1000, "currency": "USD"},
  "glm-4.7": {"input_per_1m": 0.60, "cached_per_1m": 0.11, "output_per_1m": 2.20, "context_window_k": 128, "currency": "USD"},
  "glm-4.7-flashx": {"input_per_1m": 0.07, "cached_per_1m": 0.01, "output_per_1m": 0.40, "context_window_k": 128, "currency": "USD"},
  "glm-4.7-flash": {"input_per_1m": 0.00, "cached_per_1m": 0.00, "output_per_1m": 0.00, "context_window_k": 128, "currency": "USD"},
  "glm-4.6": {"input_per_1m": 0.60, "cached_per_1m": 0.11, "output_per_1m": 2.20, "context_window_k": 128, "currency": "USD"},
  "glm-4.6v": {"input_per_1m": 0.60, "cached_per_1m": 0.11, "output_per_1m": 1.80, "context_window_k": 128, "currency": "USD"},
  "glm-4.5v": {"input_per_1m": 0.60, "cached_per_1m": 0.11, "output_per_1m": 1.80, "context_window_k": 128, "currency": "USD"},
  "glm-4.5-x": {"input_per_1m": 2.20, "cached_per_1m": 0.45, "output_per_1m": 8.90, "context_window_k": 128, "currency": "USD"},
  "glm-4.5-flash": {"input_per_1m": 0.00, "cached_per_1m": 0.00, "output_per_1m": 0.00, "context_window_k": 200, "currency": "USD"},
  "glm-4.5-airx": {"input_per_1m": 1.10, "cached_per_1m": 0.22, "output_per_1m": 4.50, "context_window_k": 128, "currency": "USD"},
  "glm-4.5": {"input_per_1m": 0.60, "cached_per_1m": 0.11, "output_per_1m": 2.20, "context_window_k": 128, "currency": "USD"},
  "glm-4-air": {"input_per_1m": 0.20, "cached_per_1m": 0.03, "output_per_1m": 1.10, "context_window_k": 128, "currency": "USD"}
}

Also add "https://docs.z.ai/guides/overview/pricing" to the "sources" array.

In model-parameter-mapping.json, add two new fields to each entry in the "effort_mapping" object. Add these fields to each effort level (preserve all existing fields):

"none":    add "zai_reasoning_effort": "none",    "zai_thinking_enabled": 0
"minimal": add "zai_reasoning_effort": "minimal", "zai_thinking_enabled": 0
"low":     add "zai_reasoning_effort": "low",     "zai_thinking_enabled": 0
"medium":  add "zai_reasoning_effort": "medium",  "zai_thinking_enabled": 1
"high":    add "zai_reasoning_effort": "high",    "zai_thinking_enabled": 1
"xhigh":   add "zai_reasoning_effort": "xhigh",   "zai_thinking_enabled": 1
"max":     add "zai_reasoning_effort": "max",     "zai_thinking_enabled": 1

Also bump _version to "2.4.0" and update _updated to "2026-09-05".

Constraints:
- Do NOT modify any existing fields in effort_mapping entries - only add the two new fields
- Free models (glm-4.7-flash, glm-4.5-flash) use 0.00 pricing
- GLM-5.3-Flash list prices (not promo prices) are used - promo ends Sep 9 2026
- Preserve existing JSON structure and formatting

Verify: model-pricing.json has "zai" key with 16 entries. model-parameter-mapping.json has zai_reasoning_effort and zai_thinking_enabled in all 7 effort levels. Both files are valid JSON.
````

---

## Prompt 3 - Update call-llm.py for Z.AI provider support

<!-- Previous steps updated all 3 JSON config files with Z.AI data. -->

````
Add Z.AI (GLM) provider support to E:\Dev\IPPS\DevSystemV4.3\skills\llm-evaluation\call-llm.py. Z.AI is OpenAI-compatible: use the OpenAI SDK with base_url swap and pass Z.AI-specific params via extra_body.

Changes needed:

1. In detect_provider() (around line 127), add glm- prefix detection before the error return:
```python
if model_lower.startswith('glm-'):
    return 'zai'
```

2. Add create_zai_client() function after create_anthropic_client():
```python
def create_zai_client(keys: dict):
    """Create Z.AI client using OpenAI SDK with base_url swap."""
    api_key = keys.get('ZAI_API_KEY')
    if not api_key:
        print("ERROR: ZAI_API_KEY not found in keys file", file=sys.stderr)
        sys.exit(1)
    return OpenAI(api_key=api_key, base_url='https://api.z.ai/api/paas/v4/')
```

3. In build_api_params() (around line 51), add two new method branches after the 'thinking' branch (before the output_factor calculation):
```python
elif method == 'zai_reasoning':
    effort_value = effort_map[reasoning_effort]['zai_reasoning_effort']
    supported = model_config.get('effort', [])
    if effort_value not in supported and supported:
        zai_fallback = {'none': 'low', 'minimal': 'low', 'medium': 'high', 'xhigh': 'max'}
        if effort_value in zai_fallback and zai_fallback[effort_value] in supported:
            print(f"[WARN] '{effort_value}' not supported by {model}, falling back to '{zai_fallback[effort_value]}'", file=sys.stderr)
            effort_value = zai_fallback[effort_value]
    params['zai_reasoning_effort'] = effort_value
    params['zai_thinking'] = {'type': 'enabled'}
elif method == 'zai_thinking':
    thinking_enabled = effort_map[reasoning_effort].get('zai_thinking_enabled', 1)
    params['zai_thinking'] = {'type': 'enabled' if thinking_enabled else 'disabled'}
```

4. Add call_zai() function after call_anthropic():
```python
def call_zai(client, model, prompt, api_params, method,
             image_data=None, image_media_type=None):
    """Call Z.AI API via OpenAI SDK with base_url swap. Uses Chat Completions API only."""
    if image_data:
        content = [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:{image_media_type};base64,{image_data}"}}
        ]
    else:
        content = prompt
    messages = [{"role": "user", "content": content}]
    call_params = {'model': model, 'messages': messages, 'max_tokens': api_params.get('max_tokens', 4096)}
    extra_body = {}
    if 'zai_thinking' in api_params:
        extra_body['thinking'] = api_params['zai_thinking']
    if 'zai_reasoning_effort' in api_params:
        extra_body['reasoning_effort'] = api_params['zai_reasoning_effort']
    if extra_body:
        call_params['extra_body'] = extra_body
    response = client.chat.completions.create(**call_params)
    result = {
        "text": response.choices[0].message.content,
        "usage": {
            "input_tokens": response.usage.prompt_tokens,
            "output_tokens": response.usage.completion_tokens
        },
        "model": response.model
    }
    if hasattr(response.usage, 'prompt_tokens_details') and response.usage.prompt_tokens_details:
        cached = getattr(response.usage.prompt_tokens_details, 'cached_tokens', 0)
        if cached:
            result["usage"]["cached_tokens"] = cached
    return result
```

5. In main() (around line 453), add Z.AI provider routing. After the anthropic else block, add an elif for zai:
```python
if provider == 'openai':
    client = create_openai_client(keys)
    call_fn = lambda: call_openai(client, args.model, prompt, api_params, method, image_data, image_media_type)
    if use_caching:
        print("[INFO] OpenAI prompt caching is automatic (no API changes needed)", file=sys.stderr)
elif provider == 'zai':
    client = create_zai_client(keys)
    call_fn = lambda: call_zai(client, args.model, prompt, api_params, method, image_data, image_media_type)
    if use_caching:
        print("[INFO] Z.AI context caching is automatic (no API changes needed)", file=sys.stderr)
else:
    client = create_anthropic_client(keys)
    call_fn = lambda: call_anthropic(client, args.model, prompt, api_params, method, image_data, image_media_type, use_caching)
    if use_caching:
        print("[INFO] Anthropic prompt caching enabled via cache_control", file=sys.stderr)
```

Constraints:
- Do NOT modify any existing OpenAI or Anthropic functions
- Z.AI uses Chat Completions API only (no Responses API)
- Z.AI-specific params (thinking, reasoning_effort) MUST go through extra_body
- Preserve existing code style (2-space indentation, single quotes, no type hints on function params beyond what exists)
- The zai_fallback map handles GLM-5.3 which only supports [low, high, max]

Verify: python -c "import ast; ast.parse(open(r'E:\Dev\IPPS\DevSystemV4.3\skills\llm-evaluation\call-llm.py').read())" succeeds. detect_provider('glm-5.2') returns 'zai'. build_api_params with a zai_reasoning model produces zai_reasoning_effort and zai_thinking keys.
````

---

## Prompt 4 - Update call-llm-batch.py for Z.AI provider support

<!-- Previous step added Z.AI support to call-llm.py. -->

````
Apply the same Z.AI provider support changes to E:\Dev\IPPS\DevSystemV4.3\skills\llm-evaluation\call-llm-batch.py that were just added to call-llm.py. The batch script has similar functions that need the same Z.AI additions.

The changes mirror call-llm.py:

1. In detect_provider(), add: if model_lower.startswith('glm-'): return 'zai'

2. Add create_zai_client() function (same as in call-llm.py):
```python
def create_zai_client(keys: dict):
    """Create Z.AI client using OpenAI SDK with base_url swap."""
    api_key = keys.get('ZAI_API_KEY')
    if not api_key:
        print("ERROR: ZAI_API_KEY not found in keys file", file=sys.stderr)
        sys.exit(1)
    return OpenAI(api_key=api_key, base_url='https://api.z.ai/api/paas/v4/')
```

3. In build_api_params(), add the same zai_reasoning and zai_thinking method branches as in call-llm.py.

4. Add call_zai() function (same as in call-llm.py). The batch script may have a slightly different function signature - match the existing call_openai/call_anthropic signatures in the batch script.

5. In the main batch processing function, add Z.AI client creation and call routing. Look for where the script creates OpenAI/Anthropic clients and routes calls based on provider. Add the zai branch there.

6. If the batch script has prompt caching support, Z.AI context caching is automatic (like OpenAI) - no explicit cache_control needed.

Constraints:
- Do NOT modify any existing OpenAI or Anthropic functions in the batch script
- Match the existing code style of call-llm-batch.py (it may differ slightly from call-llm.py)
- Z.AI uses Chat Completions API only
- Z.AI-specific params MUST go through extra_body
- The batch script may have additional parameters (like batch metadata, thread pool) - do NOT break those

Verify: python -c "import ast; ast.parse(open(r'E:\Dev\IPPS\DevSystemV4.3\skills\llm-evaluation\call-llm-batch.py').read())" succeeds. The script has create_zai_client, call_zai functions, and glm- detection in detect_provider.
````

---

## Prompt 5 - Update test-call-llm.py and llm-evaluation-selftest.py

<!-- Previous steps added Z.AI support to both call scripts. -->

````
Add Z.AI test coverage to E:\Dev\IPPS\DevSystemV4.3\skills\llm-evaluation\test-call-llm.py and E:\Dev\IPPS\DevSystemV4.3\skills\llm-evaluation\llm-evaluation-selftest.py.

In test-call-llm.py:

1. Add a ZAI_TESTS list with minimal test entries for key Z.AI models. Follow the existing TESTS list pattern. Include at least these models:
- glm-5.2 with reasoning_effort high (zai_reasoning method)
- glm-5.3-flash with reasoning_effort low (zai_reasoning method, limited effort levels)
- glm-4.5-flash with temperature medium (zai_thinking method, free model)
- glm-4.6v with temperature medium (zai_thinking method, vision model)

Example entry pattern (match existing test entries):
```python
{"model": "glm-5.2", "reasoning_effort": "high", "output_length": "medium", "expect_success": True, "provider": "zai"},
{"model": "glm-5.3-flash", "reasoning_effort": "low", "output_length": "medium", "expect_success": True, "provider": "zai"},
{"model": "glm-4.5-flash", "temperature": "medium", "output_length": "medium", "expect_success": True, "provider": "zai"},
{"model": "glm-4.6v", "temperature": "medium", "output_length": "medium", "expect_success": True, "provider": "zai"},
```

2. Add "zai" to the --provider argument choices (alongside "openai" and "anthropic").

3. If the test script filters by provider, ensure zai tests are included when --provider zai or --provider all is used.

In llm-evaluation-selftest.py:

1. Add ZAI_API_KEY to the test fixture keys dictionary (used for testing config loading).

2. Add validation that model-registry.json contains zai provider entries. Check that:
- At least 16 models with provider "zai" exist in the models array
- At least 5 entries with provider "zai" exist in model_id_startswith
- glm-5.3-flash prefix comes before glm-5.3 (ordering check)

3. Add validation that model-pricing.json contains a "zai" key in the pricing object with at least 16 entries.

4. Add validation that model-parameter-mapping.json has zai_reasoning_effort and zai_thinking_enabled fields in each effort_mapping entry.

Constraints:
- Do NOT modify existing test entries for OpenAI or Anthropic
- Do NOT break existing test script functionality
- Match existing code style in both files
- ZAI_TESTS should be minimal - 4 entries covering both methods (zai_reasoning and zai_thinking)

Verify: python -c "import ast; ast.parse(open(r'E:\Dev\IPPS\DevSystemV4.3\skills\llm-evaluation\test-call-llm.py').read())" succeeds. python -c "import ast; ast.parse(open(r'E:\Dev\IPPS\DevSystemV4.3\skills\llm-evaluation\llm-evaluation-selftest.py').read())" succeeds. test-call-llm.py --help shows zai in provider choices.
````

---

## Prompt 6 - Update update-model-registry.md workflow documentation

<!-- Previous steps updated all code files. -->

````
Add Z.AI provider documentation to E:\Dev\IPPS\DevSystemV4.3\skills\llm-evaluation\update-model-registry.md. This workflow document describes how to update model registries and pricing from official provider websites.

Add the following Z.AI-specific content:

1. Add Z.AI source URLs to the sources section:
- Model documentation: https://docs.z.ai/guides/overview/models
- Pricing: https://docs.z.ai/guides/overview/pricing
- API reference: https://docs.z.ai/api-reference

2. Add Z.AI pricing dimensions to the pricing extraction section:
- Input per 1M tokens
- Cached input per 1M tokens (approximately 50% of input price)
- Output per 1M tokens
- Context window in K tokens
- Free models (glm-4.7-flash, glm-4.5-flash) have 0.00 pricing
- GLM-5.3-Flash has promotional pricing (50% off until Sep 9 2026) - use list prices in JSON

3. Add Z.AI-specific extraction notes:
- Z.AI is OpenAI-compatible: uses OpenAI SDK with base_url swap
- Z.AI-specific params (thinking, reasoning_effort) go through extra_body
- reasoning_effort support varies by model:
  - GLM-5.3, GLM-5.3-Flash: only [low, high, max]
  - GLM-5.2: all 7 levels [none, minimal, low, medium, high, xhigh, max]
  - GLM-5.1 and below: not supported
- Thinking modes: forced (GLM-5.3, GLM-5.3-Flash, GLM-4.7, GLM-4.5V), auto (GLM-5.2, GLM-5.1, GLM-5, GLM-4.6, GLM-4.5)
- Method mapping: zai_reasoning (thinking + reasoning_effort), zai_thinking (thinking only)
- Prefix ordering: most specific first (glm-5.3-flash before glm-5.3 before glm-5 before glm-4)
- GLM-4.5-Air model ID is glm-4-air (not glm-4.5-air)

4. Add Z.AI to the provider list in the gating/verification section.

Constraints:
- Do NOT modify existing OpenAI or Anthropic sections
- Match existing document structure and formatting
- Preserve existing markdown heading hierarchy

Verify: Document contains "Z.AI" and "glm-" references. No existing provider sections modified. Document is valid markdown.
````

---

## Prompt 7 - Run verification and test

<!-- All 8 files have been updated. -->

```
Run verification on all Z.AI integration changes.

1. Run the selftest (no API calls needed for config validation):
python E:\Dev\IPPS\DevSystemV4.3\skills\llm-evaluation\llm-evaluation-selftest.py --skip-api-calls

2. If selftest passes, run a minimal API test with a free Z.AI model:
python E:\Dev\IPPS\DevSystemV4.3\skills\llm-evaluation\test-call-llm.py --provider zai --keys-file E:\Dev\.tools\.api-keys.txt --model glm-4.5-flash

3. If the free model test passes, run a reasoning model test:
python E:\Dev\IPPS\DevSystemV4.3\skills\llm-evaluation\test-call-llm.py --provider zai --keys-file E:\Dev\.tools\.api-keys.txt --model glm-5.2 --reasoning-effort high

Constraints:
- If selftest fails, fix the issue before proceeding to API tests
- If API key is missing or invalid, skip API tests and report selftest results only
- If an API test fails, check: prefix matching in model-registry.json, param passing in call-llm.py, client creation with base_url

/verify against __STRUT_ZAIINT.md
```
