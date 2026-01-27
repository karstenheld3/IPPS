# Session Problems

**Doc ID**: 2026-01-27_llm-computer-use-PROBLEMS

## Open

(None)

## Resolved

**LLMCU-PR-001: Windows Defender blocks PowerShell image compression**
- **History**: Added 2026-01-27 19:35 | Resolved 2026-01-27 19:40
- **Description**: Windows Defender blocks .NET System.Drawing image compression in PowerShell
- **Solution**: Use Python + mss + Pillow instead of PowerShell
- **Verification**: POC benchmark: 143ms avg (meets <150ms target)

**ANTCU-PR-001: What Claude models support computer use?**
- **History**: Added 2026-01-27 18:36 | Resolved 2026-01-27 19:00
- **Solution**: Opus 4.5, Sonnet 4.5, Haiku 4.5, Sonnet 4, Opus 4, Opus 4.1, Sonnet 3.7
- **Verification**: Documented in _INFO_ANTHROPIC_COMPUTER_USE.md Section 2

**ANTCU-PR-002: What are the API specifications for computer use?**
- **History**: Added 2026-01-27 18:36 | Resolved 2026-01-27 19:00
- **Solution**: Beta endpoint with computer_20250124/20251124 tools, beta header required
- **Verification**: Documented in _INFO_ANTHROPIC_COMPUTER_USE.md Section 3

**ANTCU-PR-003: What are the pricing and rate limits?**
- **History**: Added 2026-01-27 18:36 | Resolved 2026-01-27 19:00
- **Solution**: $3/MTok input, $15/MTok output (Sonnet 4.5); ~$4.80/1K screenshots; tiered rate limits
- **Verification**: Documented in _INFO_ANTHROPIC_COMPUTER_USE.md Sections 6-7

**ANTCU-PR-004: What screenshot specifications are optimal?**
- **History**: Added 2026-01-27 18:36 | Resolved 2026-01-27 19:00
- **Solution**: Max 1568px long edge, ~1.15MP, formula: tokens=(w*h)/750, JPEG/PNG/GIF/WebP
- **Verification**: Documented in _INFO_ANTHROPIC_COMPUTER_USE.md Section 5

**ANTCU-PR-005: What are expected response times?**
- **History**: Added 2026-01-27 18:36 | Resolved 2026-01-27 19:00
- **Solution**: ~2s TTFT, ~0.030s per token (Sonnet 4.5); too slow for real-time use
- **Verification**: Documented in _INFO_ANTHROPIC_COMPUTER_USE.md Section 8

**ANTCU-PR-006: What are best practices for computer use implementations?**
- **History**: Added 2026-01-27 18:36 | Resolved 2026-01-27 19:00
- **Solution**: Sandbox environment, iteration limits, coordinate scaling, verification prompts, thinking mode
- **Verification**: Documented in _INFO_ANTHROPIC_COMPUTER_USE.md Sections 9-11

## Deferred

(None yet)

## Problems Changes

**[2026-01-27 18:36]**
- Added: ANTCU-PR-001 through ANTCU-PR-006 from initial request
