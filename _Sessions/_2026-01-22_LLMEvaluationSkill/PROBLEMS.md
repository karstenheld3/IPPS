# Session Problems

**Session ID**: 2026-01-22_LLMEvaluationSkill

## Open

(none)

## Resolved

### LLMEV-FL-004: Implicit Dependencies and File Types

**Severity**: [MEDIUM]
**When**: 2026-01-22 21:02
**Resolved**: 2026-01-22 21:02
**Where**: `SPEC_LLM_EVALUATION_SKILL.md` - Script parameters

**Problem:**
File types not explicit in parameter descriptions.

**Resolution:**
Made file types explicit:
- `--input-folder` - Folder with .md files (output of `call-llm-batch.py`)
- `--output-folder` - Folder for .json answer files
- etc.

### LLMEV-FL-003: Parameter Names Not Explicit Enough

**Severity**: [LOW]
**When**: 2026-01-22 20:58
**Resolved**: 2026-01-22 20:58
**Where**: `SPEC_LLM_EVALUATION_SKILL.md` - Script parameters

**Problem:**
`--keys` and `--json` not explicit enough.

**Resolution:**
- `--keys` → `--keys-file`
- `--json` → `--write-json-metadata`

### LLMEV-FL-002: Overengineering - Redundant Parameters

**Severity**: [MEDIUM]
**When**: 2026-01-22 20:56
**Resolved**: 2026-01-22 20:57
**Where**: `SPEC_LLM_EVALUATION_SKILL.md` - Script parameters

**Problem:**
Multiple ways to do the same thing - too many optional parameters.

**Resolution:**
Removed:
- `--system-prompt`, `--user-prompt` → merged to `--prompt-file`
- `--questions-per-item` → use `--schema-file`
- `--max-tokens` → not needed for most cases

### LLMEV-FL-001: Ambiguous Script and Parameter Naming

**Severity**: [MEDIUM]
**When**: 2026-01-22 20:52
**Resolved**: 2026-01-22 20:54
**Where**: `SPEC_LLM_EVALUATION_SKILL.md` - Skill Summary section

**Problem:**
Script and parameter names were inconsistent and ambiguous.

**Resolution:**
Applied consistent naming convention (Option B):
- `call-llm.py`, `call-llm-batch.py` - LLM calls
- `generate-questions.py`, `generate-answers.py` - Generation
- `evaluate-answers.py`, `analyze-costs.py` - Analysis
- All folder params: `--{noun}-folder`
- All file params: `--{noun}-file`

## Deferred

(none)
