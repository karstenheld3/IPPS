# Devil's Advocate Review - MinimalIPPS Session

**Doc ID**: MIPPS-RV01
**Reviewed**: 2026-03-19 23:45
**Context**: Full session progress including 4 option documents and comparison matrix
**Reviewer**: Devil's Advocate (find flawed assumptions, logic errors, hidden risks)

## MUST-NOT-FORGET

1. **Goal**: Reduce IPPS complexity for cheaper LLMs - NOT just reduce file size
2. **7-step process** defined in NOTES.md - all options must map to these steps
3. **Model specialization**: Mother, Prompting, Transformer, Verification roles
4. **File exclusion thresholds**: < 100 lines AND rarely loaded → skip (user request, not yet in option docs)
5. **Session is IMPL-ISOLATED** - no codebase modifications, planning only
6. **"note but do nothing"** - user wants architecture, not execution yet

## MUST-RESEARCH

1. **LLM prompt compression** - Do compressed prompts actually work with cheap LLMs?
2. **Prompt caching failure modes** - What happens when cache expires mid-pipeline?
3. **Ensemble compression validation** - Any prior art on multi-candidate compression?
4. **Cross-file reference preservation** - How do production systems handle this?
5. **Functional test design for LLM behavior** - Can 25 tests actually catch regressions?

## Critical Issues

### [CRITICAL] `MIPPS-RV01-RF-01` No evidence that compressed prompts work with target LLMs

- **Where**: All 4 option documents
- **Assumption**: "Compressed files will make the agent behave correctly on cheaper LLMs"
- **Flaw**: This is the ENTIRE GOAL, but no option validates it empirically before committing $17-96
- **Evidence gap**: 
  - No proof that GPT-5-mini or Claude Haiku can follow compressed IPPS instructions
  - No baseline: what is current behavior with FULL system on cheap LLM?
  - Maybe cheap LLMs already work fine with full system (no compression needed)
  - Maybe cheap LLMs fail even with compressed system (compression insufficient)
- **Risk**: Spending $50-100 on compression pipeline that produces unusable output
- **Suggested fix**: 
  1. Before any pipeline work, test FULL DevSystem on target cheap LLM
  2. Document which workflows/rules FAIL with full system
  3. This becomes the baseline for measuring compression success

### [CRITICAL] `MIPPS-RV01-RF-02` "75 compressible files" count is wrong

- **Where**: All option documents, cost estimates
- **Assumption**: 8 rules + 36 workflows + 24 skill docs + 7 skill prompts = 75 files
- **Flaw**: File inventory shows `~24 md` and `~7 md` which are APPROXIMATIONS
- **Evidence**: 
  - Original search found 64 md files in `.windsurf/`
  - After excluding pricing-sources, found 68 md files
  - Actual count: 8 + 36 + ? + ? = needs verification
- **Risk**: Cost estimates could be 20-30% off if file count is wrong
- **Suggested fix**: Run exact file count before committing to any option

### [HIGH] `MIPPS-RV01-RF-03` Cache TTL assumption may be wrong

- **Where**: Option B (Mother compresses), Option D (test-driven)
- **Assumption**: "75 calls at ~30s each = ~38 minutes, cache survives"
- **Flaw**: 
  - Anthropic cache TTL is 5 minutes for EACH cache block
  - If ANY call takes > 5 min (complex file, rate limit, retry), cache expires
  - Cache must be RE-WARMED with a new call, which adds cost
- **Evidence**: Anthropic docs say cache blocks expire after 5 min of non-use
- **Risk**: 
  - Option B: If cache expires mid-compression, Mother loses context
  - Costs could double if frequent re-warming needed
- **Suggested fix**: 
  1. Add explicit cache-warming step between batches
  2. Budget for 2x cache misses in cost estimates
  3. Or accept that cache may not survive full pipeline

### [HIGH] `MIPPS-RV01-RF-04` Option D test suite may give false confidence

- **Where**: `_OPTION_D_TEST_DRIVEN.md`, Test Suite Design section
- **Assumption**: "25 test scenarios will catch behavioral regressions"
- **Flaws**:
  1. Tests are designed by Mother model - same model that creates compression strategy
  2. Tests may have blind spots matching compression blind spots
  3. 25 tests cannot cover 75 files × N concepts per file
  4. "False passes" weakness acknowledged but no mitigation
- **Evidence**: 
  - T01-T25 cover ~15 workflows but there are 36 workflows
  - No tests for rarely-used workflows (exactly the ones most likely compressed)
  - Edge case coverage (T21-T25) is generic, not file-specific
- **Risk**: Tests pass, compression deployed, rare workflows break in production
- **Suggested fix**:
  1. Require at least 1 test per workflow (36 tests minimum)
  2. Weight tests toward files marked "Secondary" or "Drop" in compression strategy
  3. Add negative tests: "this concept was dropped, verify agent doesn't use it"

### [HIGH] `MIPPS-RV01-RF-05` File exclusion thresholds not incorporated

- **Where**: All option documents
- **User requirement**: "Files < 100 lines AND rarely loaded → skip compression"
- **Status**: Noted in NOTES.md but NOT added to any option document
- **Risk**: 
  - Options compress ALL 75 files when maybe only 40-50 need it
  - Wasted cost and increased risk for files that don't matter
- **Suggested fix**: Add exclusion criteria to Step 3 (complexity map) in all options

## High Priority Issues

### [HIGH] `MIPPS-RV01-RF-06` No rollback plan if compression fails in production

- **Where**: All options
- **Gap**: Options describe compression but not deployment or rollback
- **Questions**:
  - Where does compressed DevSystem get deployed?
  - How do you switch back to full system if compression breaks things?
  - Is there a feature flag or A/B test capability?
- **Risk**: Compressed system deployed, breaks critical workflows, no quick rollback
- **Suggested fix**: Add "Deployment and Rollback" section to chosen option

### [HIGH] `MIPPS-RV01-RF-07` Thinking token estimates are guesses

- **Where**: Cost estimates in all options
- **Assumption**: "~50-100K thinking tokens per call"
- **Flaw**: 
  - No empirical data on Claude Opus 4.6 thinking token usage for this task type
  - 300K input context is unusual - thinking overhead could be 150K+ per call
  - One user report showed 200K thinking tokens for complex analysis
- **Evidence**: Cost estimates show "~80K out" but thinking could dominate
- **Risk**: Actual costs 2-3x estimates
- **Suggested fix**: 
  1. Run ONE test call with actual bundle to measure thinking tokens
  2. Update estimates with real data before committing

### [MEDIUM] `MIPPS-RV01-RF-08` "Same pattern as transcribe-image-to-markdown.py" is unverified

- **Where**: Option A, Option B, Option D
- **Assumption**: Ensemble compression will work like ensemble transcription
- **Flaw**:
  - Transcription judges image vs text (clear ground truth)
  - Compression judges "is this good enough?" (subjective)
  - Transcription refines by re-reading image
  - Compression refines by... what? Same input, different prompt?
- **Risk**: Ensemble pattern may not transfer, needs adaptation
- **Suggested fix**: Design compression-specific judge criteria before implementation

### [MEDIUM] `MIPPS-RV01-RF-09` Comparison matrix oversimplifies

- **Where**: `_OPTION_ABCD_COMPARISON.md`
- **Flaws**:
  1. "Quality" is a single score but has multiple dimensions (cross-file, functional, structural)
  2. "Parallelization" ignores API rate limits (can't actually run 225 calls in parallel)
  3. "Autonomous" assumes Option D's tests are reliable (see RF-04)
  4. Cost estimates are based on unverified assumptions (see RF-02, RF-07)
- **Risk**: Wrong option chosen based on oversimplified comparison
- **Suggested fix**: Add caveats to comparison, note which assumptions are unverified

## Medium Priority Issues

### [MEDIUM] `MIPPS-RV01-RF-10` No version control strategy for compressed files

- **Where**: All options
- **Gap**: Where do compressed files live? How are they versioned?
- **Questions**:
  - Separate branch? Separate folder?
  - How to track which compression version matches which source version?
  - What happens when source DevSystem is updated?
- **Suggested fix**: Define versioning strategy before implementation

### [MEDIUM] `MIPPS-RV01-RF-11` Python scripts and JSON configs excluded without analysis

- **Where**: All options, "skip_patterns"
- **Assumption**: "Python scripts and JSON configs are non-compressible"
- **Flaw**: 
  - Python scripts contain duplicated utility code (API key loading, retry logic)
  - Could be refactored to reduce total size
  - JSON configs could be minified
- **Risk**: Missing 20-30% of potential size reduction
- **Suggested fix**: At least analyze py/json files for compression potential

### [MEDIUM] `MIPPS-RV01-RF-12` Option C layer boundaries are assumed, not verified

- **Where**: `_OPTION_C_DEPENDENCY_ORDERED.md`, Compression Layers section
- **Assumption**: "Rules → Skills → Prompts → Workflows" is the correct order
- **Flaw**:
  - Some rules reference specific workflows (`/verify`, `/commit`)
  - Some skills reference other skills (`@write-documents` in `/improve`)
  - Actual dependency graph may have cycles or different layers
- **Risk**: Layer order wrong, cascade compression fails
- **Suggested fix**: Mother should COMPUTE layers from actual dependencies, not use assumed structure

## Questions That Need Answers

1. **What is the target cheap LLM?** Options mention GPT-5-mini and Claude Haiku 4.5 but no decision made.
2. **What is acceptable quality degradation?** 80% behavior preservation? 95%? 100%?
3. **Who maintains compressed system?** When source DevSystem changes, who re-runs compression?
4. **Is there a minimum viable subset?** Maybe compress just workflows + core rules, skip skills entirely?
5. **What if compression doesn't help?** Fallback plan if cheap LLMs still fail with compressed system?

## Research Findings (Pending)

Industry research not yet conducted. Before implementation, research:
- Prior art on LLM prompt compression
- Anthropic cache TTL edge cases and workarounds
- Ensemble approaches for text transformation (not transcription)
- How others handle cross-file consistency in generated content

## Summary

**Session progress is solid for PLANNING phase** - 4 well-structured options with cost estimates and tradeoffs.

**Critical gap**: No empirical validation that the GOAL is achievable. All options assume compression will make cheap LLMs work, but this is unproven.

**Recommended next step before implementation**:
1. Test FULL DevSystem on target cheap LLM (GPT-5-mini or Claude Haiku)
2. Document exactly which behaviors FAIL
3. This becomes the baseline for measuring compression success
4. If cheap LLM already works acceptably with full system → compression unnecessary
5. If cheap LLM fails completely even with full system → compression may be insufficient

**If proceeding with compression**: Option D (Test-Driven) is still the best choice, but test suite needs expansion and empirical validation of ensemble pattern.
