# Option D: Test-Driven Compression

**Doc ID**: MIPPS-OPT-D
**Goal**: Reduce ~1MB DevSystem to be usable by cheaper LLMs. Define quality bar as functional tests FIRST, then compress to meet it.
**Status**: Draft - pending user review
**Priority**: Quality over cost (best quality/cost ratio)

## Core Idea: Define Success Criteria Before Compressing, Then Validate

Define what "works with a cheap LLM" means before compressing. Create functional test suite: 15-25 scenarios the compressed system must handle correctly. Then compress (any method) and validate against tests. Failed tests pinpoint exactly which compressions went too far.

## Source and Scope

**Source directory**: `.windsurf/` (active DevSystem)

**File inventory** (verified 2026-03-19):
- Rules: 8 md
- Workflows: 36 md
- Skill docs (SKILL.md + supporting): 24 md
- Skill prompts: 7 md
- Python scripts: 20 py (skip)
- JSON configs: 9 json (skip)
- **Compressible: 75 files** | Non-compressible: 29 files (copy as-is)

**Exclusion criteria** (skip compression):
- Files < 100 lines AND rarely loaded → copy as-is
- Applies to: infrequently-invoked workflows, supporting skill docs (SETUP.md, UNINSTALL.md)
- Reduces compression scope by ~20-30%

## Why Higher Quality Than Options A-C

Options A-C measure structural quality: "did the compressed file keep the right sections?" Option D measures functional quality: "does the compressed system make the agent behave correctly?"

Structural quality is a proxy metric. An agent may produce correct behavior with aggressively compressed instructions, or fail with conservatively compressed ones. Only testing reveals which.

## Step-to-Output Mapping

Aligned with NOTES.md Steps 1-7, with added Steps 0 and 8:

- **Step -1**: Baseline test → test FULL DevSystem on target LLM, document failures (prerequisite)
- **Step 0**: Design test suite → `_00_FUNCTIONAL_TEST_SUITE.md` + `tests/test_suite.json` (Mother, implicitly bundles first)
- **Step 1**: Bundle verified → `context/all_files_bundle.md` (already created in Step 0)
- **Step 2**: Analyze call tree → `_01_FILE_CALL_TREE.md` (Mother)
- **Step 3**: Analyze complexity → `_02_FILE_COMPLEXITY_MAP.md` (Mother)
- **Step 4**: Compression strategy → `_03_FILE_COMPRESSION_STRATEGY.md` (Mother)
- **Step 5**: Generate prompts → `prompts/transform/` + `prompts/eval/` (Prompting model)
- **Step 6**: Compress files → `output/` (Transformer + Judge, any method)
- **Step 7**: Structural verify → `_04_FILE_COMPRESSION_REPORT.md` (Verification)
- **Step 8**: Functional test → `_05_FUNCTIONAL_TEST_RESULTS.md` (Target LLM + Judge)
- **Iterate**: Failed tests → identify responsible files → re-compress conservatively

## Test Suite Design (Step 0)

Mother model (with full system context) designs 15-25 test scenarios covering:

### Coverage Categories

```
Workflow Tests (10 scenarios):
  T01: /commit with 3 staged files → conventional commit format, correct type prefix
  T02: /session-new FixAuthBug → folder creation, NOTES.md structure, correct naming
  T03: /build a REST endpoint → EXPLORE phase questions, DESIGN before IMPLEMENT gate
  T04: /verify a SPEC document → structured findings with IDs, severity levels
  T05: /prime in empty session → correct files loaded in order
  T06: /go autonomous loop → recap + continue cycle, progress updates
  T07: /critique a document → Devil's Advocate findings, not rule violations
  T08: /improve a document → APAPALAN + MECT violations found
  T09: /write-spec for auth → SPEC template followed, FR/DD/IG items with IDs
  T10: /fail record a mistake → FAILS.md entry with FL ID, lesson, prevention

Rule Compliance Tests (5 scenarios):
  T11: Write Python code → coding conventions applied (snake_case, docstrings)
  T12: Create a document → header block, Doc ID, no emojis, correct quote style
  T13: Reference another document → filename AND Doc ID format
  T14: Log a multi-step operation → Announce/Track/Report pattern
  T15: Name a new concept → AP-NM-01 check, no synonyms

Skill Tests (5 scenarios):
  T16: Invoke deep-research → MEPI/MCPI strategy selection
  T17: Invoke write-documents → correct template loaded for document type
  T18: Invoke git-conventions → conventional commit message format
  T19: Invoke coding-conventions → correct rules loaded for language
  T20: Invoke session-management → correct session folder structure

Edge Cases (5 scenarios):
  T21: Conflicting instructions → correct priority resolution (rules > workflows)
  T22: Unknown workflow invoked → graceful handling
  T23: Multi-file edit → coding conventions + commit conventions together
  T24: Session with existing PROBLEMS.md → read before acting
  T25: MUST-NOT-FORGET technique → MNF list created and checked
```

### Test Scenario Format

```json
{
  "id": "T01",
  "name": "Conventional commit with 3 files",
  "category": "workflow",
  "input_prompt": "/commit - I've modified auth.py, test_auth.py, and config.yaml",
  "system_context": "3 staged files: auth.py (fix token refresh), test_auth.py (add test), config.yaml (update timeout)",
  "expected_behavior": [
    "Uses conventional commit format: type(scope): description",
    "Identifies correct commit type (fix or feat)",
    "Does not combine unrelated changes without asking",
    "Follows git-conventions skill rules"
  ],
  "pass_criteria": "All 4 expected behaviors present",
  "fail_criteria": "Any expected behavior missing or wrong format",
  "affected_files": ["workflows/commit.md", "skills/git-conventions/SKILL.md", "rules/core-conventions.md"]
}
```

## Folder Structure

```
[SESSION_FOLDER]/
├─> mipps_pipeline.py                    (orchestrator)
├─> pipeline_config.json                 (model roles, test config, thresholds)
├─> pipeline_state.json                  (auto-generated)
├─> prompts/
│   ├─> step/
│   │   ├─> s0_design_tests.md           (test suite generation prompt)
│   │   ├─> s2_call_tree.md
│   │   ├─> s3_complexity_map.md
│   │   ├─> s4_compression_strategy.md
│   │   ├─> s5_generate_prompts.md
│   │   ├─> s7_verify_file.md
│   │   └─> s8_functional_test.md        (test execution + judge prompt)
│   ├─> transform/                       (generated by Step 5)
│   │   └─> ...
│   └─> eval/                            (1:1 with transform/)
│       └─> ...
├─> tests/
│   ├─> test_suite.json                  (all 25 test scenarios)
│   ├─> baseline_results.json            (optional: full system baseline)
│   └─> compressed_results.json          (test results on compressed system)
├─> context/
│   └─> all_files_bundle.md
├─> output/
│   ├─> rules/
│   ├─> workflows/
│   └─> skills/
├─> _00_FUNCTIONAL_TEST_SUITE.md         (Step 0)
├─> _01_FILE_CALL_TREE.md               (Step 2)
├─> _02_FILE_COMPLEXITY_MAP.md           (Step 3)
├─> _03_FILE_COMPRESSION_STRATEGY.md     (Step 4)
├─> _04_FILE_COMPRESSION_REPORT.md       (Step 7)
└─> _05_FUNCTIONAL_TEST_RESULTS.md       (Step 8)
```

## Pipeline Commands

```
mipps_pipeline.py design-tests                            → Step 0: Mother designs test suite
mipps_pipeline.py bundle    --source-dir .windsurf/       → Step 1: generate bundle
mipps_pipeline.py baseline  --model gpt-5-mini            → Optional: run tests with full system
mipps_pipeline.py analyze   --steps 2-4                   → Steps 2-4: Mother, cached context
mipps_pipeline.py check     --step 2|3|4                  → Verify Mother output
mipps_pipeline.py generate  --step 5                      → Step 5: Prompting model → prompts
mipps_pipeline.py transform --step 6 --candidates 3       → Step 6: Transformer + Judge
mipps_pipeline.py verify    --step 7                      → Step 7: Structural verification
mipps_pipeline.py test      --model gpt-5-mini            → Step 8: Functional test on target LLM
mipps_pipeline.py diagnose                                → Compare test results, identify failing files
mipps_pipeline.py iterate   --conservative                → Re-compress failing files (keep more content, fewer drops)
mipps_pipeline.py status                                  → Pipeline state + test pass rate
```

## Model Roles

1. **Mother** - Claude Opus 4.6 Thinking (1M context)
   - Step 0: Design test suite (loads all files, creates bundle as side effect)
   - Steps 2-4: Analysis with cached context
   - Iteration: Review test failures, identify which compressions caused them
   - **Cache note**: Steps 0-4 = 5 calls at ~30s each = ~2.5 minutes. Cache TTL (5 min) is safe.

2. **Sonnet** - Claude Sonnet 4.5 Thinking (200K context)
   - Step 5: Generate transform/ + eval/ prompts

3. **Transformer** - GPT-5-mini (cheap, tests catch failures)
   - Step 6: Compress files using transform/ prompts
   - Ensemble: 3 candidates per file

4. **Target LLM** - The actual cheap LLM intended to use the compressed DevSystem
   - Step 8: Run functional tests with compressed system as instructions
   - **Critical**: This must be the model you actually deploy with (GPT-5-mini, Claude Haiku 4.5, etc.)
   - Tests validate that THIS model understands the compressed instructions

5. **Verification** - GPT-5-mini
   - Step 6: Judge candidates
   - Step 7: Structural comparison
   - Step 8: Judge test responses against expected behavior

## Functional Test Execution (Step 8 Detail)

```
For each test scenario (25 tests):

  1. Build system prompt from compressed files
     Load compressed rules + relevant compressed workflows + relevant compressed skills
     (based on test scenario's affected_files list)

  2. Send test prompt to Target LLM
     System: [compressed DevSystem subset]
     User: [test input_prompt]

  3. Capture Target LLM response

  4. Judge response (Verification model)
     Input: test scenario + expected_behavior + actual response
     Output: {
       "pass": true/false,
       "score": 1-5,
       "matched_behaviors": ["behavior 1", "behavior 3"],
       "missing_behaviors": ["behavior 2"],
       "unexpected_behaviors": [],
       "diagnosis": "The commit format was correct but scope was missing,
                     likely because workflows/commit.md lost the scope rules"
     }
```

## Diagnosis and Iteration

When tests fail:

```
mipps_pipeline.py diagnose

Output:
  PASS: 18/25 tests
  FAIL: 7/25 tests

  Failed tests by root cause:
    workflows/commit.md (too aggressively compressed):
      T01: Missing scope in commit format
      T18: Missing conventional commit type list

    rules/devsystem-core.md (dropped MNF section):
      T25: MUST-NOT-FORGET technique not applied

    skills/coding-conventions/PYTHON-RULES.md (simplified too much):
      T11: Missing docstring requirement
      T14: Logging pattern incomplete

  Recommendation:
    Re-compress 3 files with --conservative flag (less aggressive compression)
    Then re-run: mipps_pipeline.py test --model gpt-5-mini
```

## Step 7 Report Format

Per NOTES.md, 5 lines per file, plus functional test results:

```
### rules/core-conventions.md
1. **Structural changes**: Merged 3 sections, flattened heading depth from 4 to 3
2. **Removed features**: Transcription Output rules, Temporary Files section
3. **Simplified content**: Date format examples reduced from 8 to 3
4. **Sacrificed details**: BAD/GOOD example pairs cut from 12 to 5
5. **Possible impact**: Agent may not apply datetime format in filenames correctly

## Functional Test Results
- **Pass rate**: 18/25 (72%)
- **Failing files**: 3 files need re-compression (see diagnose output)
- **Iteration needed**: Yes - re-compress commit.md, devsystem-core.md, PYTHON-RULES.md
```

## Cost Estimates

**Steps 0-4: Mother analysis**
- Step 0 (test design): 300K cached in × $0.50/1M + ~60K out × $25/1M = $0.15 + $1.50 = ~$1.65
- Steps 2-4: ~$7.80
- **Analysis total: ~$9.45**

**Step 5: Sonnet generates prompts**: ~$3.00

**Step 6: Transformer + Judge (GPT-5-mini)**
- Same as Option A: ~$3.15

**Step 7: Structural verification**: ~$0.38

**Step 8: Functional tests**
- Target LLM (GPT-5-mini): 25 tests × (~100K system prompt + ~2K test = ~102K in × $0.125/1M + ~5K out × $1/1M) = 25 × $0.018 = ~$0.45
- Judge (GPT-5-mini): 25 × (~10K in × $0.125/1M + ~2K out × $1/1M) = 25 × $0.003 = ~$0.08
- **Step 8: ~$0.53**

**Iteration**: Re-compress 3-5 files × $0.01 + re-test 25 × $0.02 = ~$0.55

**First iteration: ~$17.50** (±50% - thinking tokens estimated)
**Subsequent iterations: ~$4.25** (re-compress failures + re-test only)

## Cost Optimization Levers

- **Skip baseline**: Only compare against criteria, not against full-system behavior → saves ~$0.50
- **Reduce test suite**: 15 tests instead of 25 → saves ~$0.20 per test run
- **Batch API**: 50% discount on Step 6 → saves ~$1.55
- **Upgrade Transformer for failing files only**: Use Sonnet 4.5 for re-compression of test failures

## Strengths

- **Measures the actual goal** - agent behavior, not file structure
- **Same cost as Option A** (~$16.50) with functional validation included
- **Self-correcting** - failed tests pinpoint exactly which files to fix
- **Test suite is reusable** - validates future DevSystem changes
- **Cheap Transformers work** - quality issues caught by tests, not prevented by expensive models
- **Fast iteration** - re-compress only failing files, re-test in seconds

## Weaknesses

- **Test design is hard** - 25 scenarios may miss edge cases
- **Target LLM dependency** - tests must run on the actual cheap LLM
- **False passes** - a test may pass for wrong reasons (cheap LLM happens to guess correctly)
- **Slow feedback** - must complete Steps 1-7 before getting first functional signal
- **No cross-file reference checking** (unlike Option C)

## Open Questions

1. **Which target LLM?** Tests must run on intended deployment model. GPT-5-mini? Claude Haiku 4.5? Run both to ensure portability.
2. **Baseline value**: ~$0.50 to establish full-system baseline. Recommended for first run - measures exact degradation. Skip for iterations.
3. **Hybrid with Option C**: Dependency-ordered compression (C) + functional tests (D). ~$100 but maximum quality. Recommended if first iteration fails >30% of tests.
4. **Test maintenance**: Mother can regenerate test suite when DevSystem changes. Add `mipps_pipeline.py update-tests` command.

## Recommended Combination: Option A + D (Best Value)

Use Option A's cheap pipeline for compression, add Option D's test suite for validation:

```
Steps 0-4: Mother designs tests + analyzes system       (~$9.45)
Step 5: Sonnet generates prompts                         (~$3.00)
Step 6: GPT-5-mini compresses (cheap, fast)              (~$3.15)
Step 7: Structural verification                          (~$0.38)
Step 8: Functional test on target LLM                    (~$0.53)
Iterate: Re-compress failures with Sonnet 4.5            (~$1.00)
                                                  Total: ~$17.50
```

**Escalation path** if first iteration fails >30% of tests:
1. Re-compress failing files with Sonnet 4.5 (+$2-5)
2. If still failing: use Option B (Mother compresses failing files) (+$5-10)
3. If cross-file references broken: use Option C for affected layer (+$20-40)
