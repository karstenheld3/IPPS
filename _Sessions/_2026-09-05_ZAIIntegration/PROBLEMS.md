# Problems: Z.AI Integration

**Topic ID**: ZAIINT

## Open

- **ZAIINT-PR-0004**: GLM-4.5-Air model ID is `glm-4-air` (not `glm-4.5-air`) - prefix must match actual API ID
- **ZAIINT-PR-0005**: GLM-5.3-Flash has promo pricing (50% off until Sep 9, 2026) - use list prices in JSON, note promo in comments

## Resolved

- **ZAIINT-PR-0001**: Resolved 2026-09-05 - Fallback logic implemented in `build_api_params` for unsupported effort levels
- **ZAIINT-PR-0002**: Resolved 2026-09-05 - Unified params passed via `extra_body` in `call_zai`; no `zai_` prefixed keys
- **ZAIINT-PR-0003**: Resolved 2026-09-05 - Prefix ordering verified correct in model-registry.json
- **ZAIINT-PR-0006**: Resolved 2026-09-05 - call-llm-batch.py has full Z.AI support matching call-llm.py
