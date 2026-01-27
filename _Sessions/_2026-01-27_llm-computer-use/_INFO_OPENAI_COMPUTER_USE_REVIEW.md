# Devil's Advocate Review: OpenAI Computer Use Research

**Doc ID**: OAICU-IN01-RV01
**Reviewed**: 2026-01-27 19:00
**Reviewer**: Devil's Advocate (Critique Workflow)
**Source**: `_INFO_OPENAI_COMPUTER_USE.md` [OAICU-IN01]

## MUST-NOT-FORGET Checklist

- [x] User goal: Windows desktop automation (not just browser)
- [x] Both Anthropic and OpenAI researched
- [x] Source retention verified
- [x] Labels applied to findings
- [x] Benchmark context: 38.1% OSWorld vs 72.4% human
- [x] Cost reality: Screenshots expensive, multiple iterations

## MUST-RESEARCH Topics

1. **Production computer use failures** - OpenAI CUA reliability issues
2. **Windows-specific challenges** - DPI scaling, coordinate translation
3. **Screenshot quality tradeoffs** - Resolution vs cost vs accuracy
4. **Prompt injection examples** - Malicious screenshot content
5. **Alternative approaches** - Accessibility APIs vs vision-based

## Industry Research Findings

### OpenAI CUA Production Status

**Source**: OpenAI documentation, Reddit discussions

- **Beta status**: "Model may be susceptible to exploits and mistakes"
- **OSWorld 38.1%**: Still far below human 72.4%
- **Browser-optimized**: Non-browser environments "less reliable"
- **Implication**: Production readiness questionable for Windows desktop

### Windows DPI Scaling Issues

**Source**: Microsoft Learn (hidpi, ui-automation)

- **Same issues as Anthropic**: DPI-unaware apps, fractional scaling, multi-monitor
- **Additional concern**: OpenAI docs don't mention DPI at all
- **Implication**: Coordinate translation complexity completely unaddressed

### Prompt Injection Reality

**Source**: OpenAI, OWASP, Lakera

- **Built-in safety checks**: malicious_instructions, irrelevant_domain, sensitive_domain
- **Requires acknowledgment**: User must explicitly confirm to proceed
- **Implication**: Better than Anthropic's opt-out approach, but adds friction

### Accessibility API Alternative

**Source**: Accelirate, Microsoft Learn

- **UI Automation API**: Direct element access, no vision needed
- **Advantages**: Faster, cheaper, more reliable for standard Windows apps
- **Disadvantages**: Requires app support, doesn't work with legacy/custom UIs
- **Implication**: Document doesn't compare vision-based vs API-based approaches

## Critical Issues

### CRIT-001: Browser-First Design Conflicts with User Goal

**Category**: Fundamental Mismatch
**Severity**: Critical
**Impact**: Core use case viability

**Problem**: Document states CUA is "browser-first" and "browser-optimized" but user goal is **Windows desktop automation**.

**Evidence**:
- Line 44: "Browser-first design: Optimized for web-based tasks"
- Line 74: "The model is browser-optimized. Non-browser environments have lower reliability."
- Line 389: "Non-browser environments - Less reliable than browser"
- Line 418: "OpenAI CUA: Optimized for browser; desktop modes less reliable"

**User requirement** (NOTES.md line 10): "windows-desktop-control which does screenshots, sends them to an llm model"

**Contradiction**: User wants Windows desktop, document recommends browser-focused solution.

**Benchmark reality**:
- WebVoyager (browser): 87%
- OSWorld (desktop): 38.1%
- Difference: **48.9 percentage points worse** on desktop

**Risk**: User implements OpenAI CUA for Windows desktop, discovers 38.1% accuracy is unacceptable for production use.

**Recommendation**: Add prominent warning at document start: "⚠️ **CRITICAL**: OpenAI CUA is browser-optimized. For Windows desktop automation, Anthropic Computer Use may be more suitable (see comparison section 11)."

### CRIT-002: "Windows" Environment Parameter Misleading

**Category**: Flawed Assumption
**Severity**: High
**Impact**: Implementation expectations

**Problem**: Lines 67-72 list `"windows"` as supported environment parameter, implying Windows desktop support. But line 74 immediately contradicts this.

**Evidence**:
- Line 71: `"windows"` - Windows desktop
- Line 74: "The model is browser-optimized. Non-browser environments have lower reliability."

**Flawed assumption**: Presence of `"windows"` parameter suggests Windows desktop is a supported, tested use case.

**Reality**: Parameter exists but reliability is "lower" (undefined how much lower).

**Questions**:
1. What does "lower reliability" mean quantitatively? 38.1% vs 87%? Worse?
2. Has OpenAI tested on actual Windows desktop applications?
3. Are there Windows-specific failure modes?

**Risk**: User sets `environment: "windows"`, assumes it's production-ready, discovers it's unreliable.

**Recommendation**: Add explicit warning: "Windows desktop mode exists but is NOT recommended for production. Use browser mode or consider Anthropic for desktop automation."

### CRIT-003: DPI Scaling Completely Unaddressed

**Category**: Missing Critical Information
**Severity**: High
**Impact**: Coordinate accuracy on real Windows systems

**Problem**: Document mentions "Match display_width/height to actual resolution" (line 458) but doesn't address Windows DPI scaling complexity.

**Missing information**:
- How to handle 125%, 150%, 175% DPI scaling
- Multi-monitor with different DPI per screen
- DPI-aware vs DPI-unaware application behavior
- Coordinate translation when Windows intercepts and converts

**Research finding**: Windows DPI scaling is complex (see Anthropic review CRIT-002). OpenAI docs are silent on this.

**Risk**: User implements on Windows with DPI scaling, clicks miss targets by 25-75% offset.

**Recommendation**: Add "Windows DPI Scaling" subsection to Implementation Architecture:
- Query actual DPI using Win32 API
- Test on target DPI settings before deployment
- Consider using accessibility APIs for DPI-aware coordinate translation

### CRIT-004: Cost Calculation Missing Iteration Reality

**Category**: Incomplete Analysis
**Severity**: Medium
**Impact**: Budget planning

**Problem**: Section 6 calculates per-image token cost but doesn't model realistic task costs with iterations.

**Missing calculation**:
- Typical browser task: 5-20 iterations (line 271)
- Typical desktop task: 50+ iterations (line 272)
- Each iteration: 85-1105 tokens (image) + reasoning tokens (output)
- Desktop task cost: 50 * 765 tokens (avg) * $2.50/MTok = **$0.096 input** + output tokens

**Evidence**: Line 271 mentions "5-20+ iterations" but no cost calculation for full task.

**Risk**: User budgets for per-screenshot cost, gets surprised by 10-50x multiplier from iterations.

**Recommendation**: Add "Realistic Task Cost" calculation showing:
- Browser task (10 iterations): $X
- Desktop task (50 iterations): $Y
- Compare with Anthropic costs

### CRIT-005: Safety Check Friction Understated

**Category**: Operational Impact
**Severity**: Medium
**Impact**: Automation workflow design

**Problem**: Section 7 describes safety checks but doesn't explain operational impact.

**Current description** (lines 276-312): Technical implementation of acknowledged_safety_checks.

**Missing**:
- **Frequency**: How often do safety checks trigger? Every 10th action? Every domain change?
- **User experience**: Does automation pause until human confirms? How long can it wait?
- **False positives**: What's the false positive rate? Will legitimate actions get flagged?
- **Automation impact**: Can you run unattended automation, or does it require human monitoring?

**Risk**: User designs fully automated workflow, discovers safety checks require human-in-loop, breaks automation.

**Recommendation**: Add "Safety Check Operational Impact" subsection:
- Frequency of safety check triggers (if known)
- Design patterns for handling checks in automated workflows
- When to use safety checks vs when to opt out (if possible)

## High Priority

### HIGH-001: Operator vs API Confusion

**Category**: Information Architecture
**Severity**: Medium
**Impact**: Implementation path selection

**Problem**: Document mixes Operator (consumer product) and API (developer access) without clear separation.

**Evidence**:
- Line 17: "Operator product: $200/month ChatGPT Pro subscription"
- Line 18: "API access: Standard pay-per-use via Responses API"
- But: Sections 3-12 describe API implementation, not Operator

**Confusion**: User reading for windows-desktop-control skill needs API info, but Operator is mentioned prominently in summary.

**Risk**: User thinks they need $200/month subscription when they actually need API access.

**Recommendation**: Restructure document:
- Section 1: Clearly separate Operator (managed service) vs API (developer)
- Summary: Remove Operator mention or clarify "Operator is consumer product, API is for developers"
- Add note: "This document focuses on API implementation for windows-desktop-control"

### HIGH-002: Responses API Requirement Buried

**Category**: Critical Requirement Visibility
**Severity**: Medium
**Impact**: Implementation planning

**Problem**: Line 78 states "Responses API only (NOT Chat Completions)" but this is a **breaking constraint** for existing OpenAI integrations.

**Implication**: If user has existing Chat Completions code, they must rewrite for Responses API.

**Location**: Buried in "API Requirements" subsection, not in Summary.

**Risk**: User starts implementation with Chat Completions API, discovers incompatibility late.

**Recommendation**: Move to Summary: "API: Responses API only (not Chat Completions) [VERIFIED]"

### HIGH-003: "Drag" Action Undocumented

**Category**: Missing Information
**Severity**: Low
**Impact**: Feature completeness

**Problem**: Line 183 lists `drag` action but provides no parameters or usage details.

**Evidence**:
- Line 183: "drag - Drag from one point to another"
- Line 184: "Parameters: start and end coordinates"
- But: No code example, no format specification

**Questions**:
1. What's the parameter format? `{start: [x1, y1], end: [x2, y2]}`?
2. Is it a single action or multiple (mouse_down, move, mouse_up)?
3. Does it support drag speed/duration?

**Risk**: User attempts to implement drag, guesses parameter format incorrectly.

**Recommendation**: Add drag action example to Section 4 or note "See sample app for drag implementation details."

### HIGH-004: Benchmark Context Missing

**Category**: Incomplete Analysis
**Severity**: Medium
**Impact**: Performance expectations

**Problem**: Section 8 lists benchmarks but doesn't explain what they measure or why scores differ.

**Evidence**:
- Line 320: "OpenAI CUA: 38.1%"
- Line 330: "OpenAI CUA: 87%"
- Line 324: "CUA operates in controlled virtual environments"

**Missing context**:
- What tasks are in OSWorld? (file operations, app usage, system config)
- What tasks are in WebVoyager? (web navigation, form filling, search)
- Why 48.9 point difference? (browser optimization vs desktop complexity)

**Risk**: User sees 87% and assumes CUA is production-ready, doesn't realize it's browser-only.

**Recommendation**: Add benchmark interpretation:
- OSWorld = desktop tasks (CUA weak here)
- WebVoyager = browser tasks (CUA strong here)
- For Windows desktop, expect performance closer to 38.1% than 87%

## Medium Priority

### MED-001: Reasoning Summary Cost Not Calculated

**Category**: Missing Cost Analysis
**Severity**: Low
**Impact**: Budget planning

**Problem**: Line 122 mentions `reasoning: { summary: "concise" }` but doesn't calculate token cost.

**Assumption**: Reasoning summary adds output tokens, but how many?

**Risk**: Minor cost surprise, should be documented.

**Recommendation**: Add note: "Reasoning summary adds ~50-200 output tokens per request (cost varies by summary detail level)."

### MED-002: `truncation: "auto"` Requirement Unexplained

**Category**: Missing Explanation
**Severity**: Low
**Impact**: Understanding

**Problem**: Lines 79, 124, 163 state `truncation: "auto"` is REQUIRED but don't explain why.

**Questions**:
1. What does truncation do?
2. Why is it required for computer use?
3. What happens if you don't set it?

**Risk**: User cargo-cults the parameter without understanding, can't debug if issues arise.

**Recommendation**: Add explanation: "truncation: auto enables automatic context window management for long computer use sessions with many screenshots."

### MED-003: Action Handler Code Incomplete

**Category**: Implementation Gap
**Severity**: Low
**Impact**: Developer experience

**Problem**: Lines 352-364 show Playwright setup but don't show how to handle all action types.

**Evidence**: Code shows browser setup, but action handling is in separate chunks (not shown in document).

**Risk**: Developer has to piece together implementation from multiple sources.

**Recommendation**: Add link to complete implementation: "See OpenAI CUA sample app for complete action handler implementations: [URL]"

### MED-004: Multi-Monitor Handling Unaddressed

**Category**: Missing Information
**Severity**: Low
**Impact**: Complex setups

**Problem**: No guidance on multi-monitor setups.

**Questions**:
1. Send separate screenshots per monitor?
2. Combined screenshot of all monitors?
3. How to specify which monitor for actions?

**Risk**: User with multi-monitor setup doesn't know how to implement.

**Recommendation**: Add "Multi-Monitor Considerations" to Implementation Architecture or note "Multi-monitor support: UNTESTED, recommend single monitor for initial implementation."

## Questions That Need Answers

1. **Windows desktop reliability**: What's the actual accuracy on Windows desktop tasks? Is 38.1% OSWorld representative?

2. **DPI scaling support**: Does CUA understand Windows DPI scaling? Should we send DPI metadata?

3. **Safety check frequency**: How often do safety checks trigger in typical workflows? 1%? 10%? 50%?

4. **Drag action format**: What's the exact parameter format for drag action?

5. **Reasoning summary tokens**: How many tokens does reasoning summary add? Does "concise" vs "detailed" matter?

6. **Truncation behavior**: What exactly does `truncation: "auto"` do? How does it decide what to truncate?

7. **Multi-monitor**: Is multi-monitor supported? If yes, how to implement?

8. **Keyboard layouts**: Does CUA understand non-US keyboard layouts?

9. **Clipboard**: Can CUA use clipboard operations, or only keyboard simulation?

10. **Version stability**: Is `computer-use-preview` model stable, or will it change? Should we pin to snapshot version?

## Recommendations Summary

**Immediate actions**:
1. Add prominent warning: CUA is browser-optimized, not recommended for Windows desktop
2. Clarify Operator vs API distinction in Summary
3. Add Windows DPI scaling warning
4. Calculate realistic per-task costs with iterations

**Before implementation**:
1. Test CUA on actual Windows desktop applications (not just browser)
2. Measure coordinate accuracy with Windows DPI scaling
3. Benchmark safety check trigger frequency
4. Compare with Anthropic for Windows desktop use case

**For next research phase**:
1. Contact OpenAI for Windows desktop guidance
2. Research Windows UI Automation API as alternative
3. Build POC comparing OpenAI (browser) vs Anthropic (desktop)
4. Evaluate hybrid approach: OpenAI for web tasks, Anthropic for desktop

## Comparison with Anthropic Review

**Shared issues**:
- Windows DPI scaling unaddressed (both)
- Cost calculation missing iterations (both)
- Prompt injection mitigation needs detail (both)

**OpenAI-specific issues**:
- Browser-first design conflicts with Windows desktop goal
- Lower desktop reliability (38.1% vs Anthropic 22%, but Anthropic tested on real desktop)
- Safety checks add operational friction (requires human acknowledgment)

**Anthropic-specific issues**:
- Coordinate accuracy "hallucination" mentioned
- Latency data is third-party [ASSUMED]
- More flexible (works with any app) but less reliable

**Recommendation**: For windows-desktop-control skill, **Anthropic appears more suitable** despite lower benchmark score, because:
1. Desktop-first architecture
2. Works with native Windows applications
3. No browser-optimization bias
4. Self-managed environment = full control

OpenAI CUA better for:
1. Browser-based automation
2. Web form filling
3. Tasks where 87% accuracy is acceptable

## Document History

**[2026-01-27 19:00]**
- Initial Devil's Advocate review
- Industry research: production status, Windows DPI, prompt injection, accessibility APIs
- Identified 5 critical, 4 high, 4 medium priority issues
- Generated 10 questions requiring answers
- Compared with Anthropic review findings
