# Learnings

**Goal**: Transferable lessons extracted from resolved problems

## Table of Contents

1. [LLMEV-LN-001 API Design - Explicit Over Implicit](#llmev-ln-001)
2. [LLMEV-LN-002 Resist Overengineering](#llmev-ln-002)
3. [LLMEV-LN-003 File Pattern Matching Needs Defensive Filtering](#llmev-ln-003)
4. [LLMEV-LN-004 Workspace File Discipline](#llmev-ln-004)

## Learnings

### LLMEV-LN-001: API Design - Explicit Over Implicit {#llmev-ln-001}

**Problem type**: BUILD / COMPLEXITY-MEDIUM
**Source**: FL-001, FL-003, FL-004

#### Context at Decision Time

- Designing CLI parameters for 6 Python scripts
- Initial naming used generic terms: `--keys`, `--json`, `call.py`
- File type requirements were implicit in documentation

#### Assumptions

- `[UNVERIFIED]` Users will read documentation before using scripts
- `[CONTRADICTS]` Short parameter names are more user-friendly
- `[CONTRADICTS]` File types can be inferred from context

#### What Actually Happened

During spec review (Devil's Advocate), ambiguities were identified:
- `--keys` could mean key names, key file, or key values
- `--json` could mean input format, output format, or metadata
- Script names like `call.py` don't indicate batch vs single

#### Problem Dependency Tree

```
[Implicit naming convention]
├─> [Ambiguous parameter --keys]
│   └─> Users unsure what to pass
├─> [Ambiguous parameter --json]
│   └─> Confusion about input vs output
└─> [Generic script names]
    └─> Hard to remember which script does what
```

#### Root Cause

**Root cause**: Favored brevity over clarity in API design.

**Counterfactual**: If we had used explicit names (`--keys-file`, `--write-json-metadata`, `call-llm.py`), then users would understand parameters without documentation.

**Prevention**: For CLI tools, always use explicit parameter names that describe what they accept (file, path, flag) and what they do. Brevity is not a virtue in APIs.

#### Code Example

```python
# BEFORE (ambiguous)
parser.add_argument('--keys')
parser.add_argument('--json', action='store_true')

# AFTER (explicit)
parser.add_argument('--keys-file', type=Path, help='Path to API keys file (.env format)')
parser.add_argument('--write-json-metadata', action='store_true', help='Write token usage to .meta.json')
```

---

### LLMEV-LN-002: Resist Overengineering {#llmev-ln-002}

**Problem type**: BUILD / COMPLEXITY-MEDIUM
**Source**: FL-002

#### Context at Decision Time

- Designing parameters for LLM evaluation scripts
- Wanted to provide maximum flexibility
- Added parameters "just in case" they might be useful

#### Assumptions

- `[UNVERIFIED]` Users will need fine-grained control over prompts
- `[CONTRADICTS]` More parameters = more useful tool
- `[UNVERIFIED]` Default values won't be sufficient

#### What Actually Happened

Devil's Advocate identified redundant parameters:
- `--system-prompt` / `--user-prompt`: Prompt file already handles this
- `--questions-per-item`: Schema file already defines this
- `--max-tokens`: Rarely needs overriding, can hardcode sensible default

#### Problem Dependency Tree

```
[Anticipating needs without evidence]
├─> [Redundant --system-prompt, --user-prompt]
│   └─> Duplicates prompt file functionality
├─> [Redundant --questions-per-item]
│   └─> Duplicates schema file functionality
└─> [Unnecessary --max-tokens]
    └─> Adds complexity without benefit
```

#### Root Cause

**Root cause**: Added parameters based on imagined future needs rather than actual requirements.

**Counterfactual**: If we had designed for the minimal use case first, then we would have avoided 4 unnecessary parameters and simpler code.

**Prevention**: Start with the minimum viable API. Add parameters only when users request them or when a concrete use case demands them. "You Aren't Gonna Need It" (YAGNI).

---

### LLMEV-LN-003: File Pattern Matching Needs Defensive Filtering {#llmev-ln-003}

**Problem type**: BUILD / COMPLEXITY-MEDIUM
**Source**: FL-007

#### Context at Decision Time

- Implementing `generate-answers.py` to match questions to transcriptions
- Questions have `source_file` field pointing to original input
- Transcriptions are in a folder with various file types

#### Assumptions

- `[CONTRADICTS]` All JSON files in transcription folder contain transcription text
- `[UNVERIFIED]` Filename stem matching is sufficient
- `[CONTRADICTS]` Empty content will be caught downstream

#### What Actually Happened

During API testing, script produced 0 answers:
1. Folder contained `_token_usage__*.json` (metadata, no text)
2. Folder contained `*.meta.json` (metadata, no text)
3. Matching found `sample_document_summary.meta.json` first
4. Loaded empty string as "transcription"
5. All questions failed to find valid transcription

#### Problem Dependency Tree

```
[Weak file filtering]
├─> [Loaded _token_usage__*.json]
│   └─> Empty text field
├─> [Loaded *.meta.json]
│   └─> Empty text field
└─> [No content validation]
    └─> Empty string passed as valid transcription
```

#### Root Cause

**Root cause**: File loading assumed all matching files contain valid content without filtering metadata files or validating content.

**Counterfactual**: If we had filtered `_*` files, `.meta.*` files, and validated non-empty content, then the correct transcription would have been matched.

**Prevention**: When loading files by pattern:
1. Explicitly exclude metadata files (`_*`, `.meta.*`, `.tmp`)
2. Validate content is non-empty before adding to collection
3. Log loaded files for debugging

#### Code Example

```python
# BEFORE (naive loading)
for f in folder.iterdir():
    if f.suffix == '.json':
        data = json.loads(f.read_text())
        transcriptions[f.stem] = data.get("text", "")

# AFTER (defensive filtering)
for f in folder.iterdir():
    if f.name.startswith('_'):
        continue
    if '.meta.' in f.name:
        continue
    if f.suffix == '.json':
        data = json.loads(f.read_text())
        text = data.get("text", "")
        if text:  # Validate non-empty
            transcriptions[f.stem] = text
```

---

### LLMEV-LN-004: Workspace File Discipline {#llmev-ln-004}

**Problem type**: CHORE
**Source**: FL-005, FL-006

#### Context at Decision Time

- Working in session folder `_Sessions\_2026-01-22_LLMEvaluationSkill`
- Multiple similar files exist: PROBLEMS.md, FAILS.md
- Multiple similar folders exist: `.windsurf/`, `DevSystemV3.2/`

#### Assumptions

- `[CONTRADICTS]` Memory of file purposes is reliable
- `[UNVERIFIED]` Quick edits don't need path verification

#### What Actually Happened

Two separate incidents:
1. Wrote failure log entries to PROBLEMS.md instead of FAILS.md
2. Edited `.windsurf/` directly instead of `DevSystemV3.2/` source

#### Problem Dependency Tree

```
[Similar file/folder names]
├─> [PROBLEMS.md vs FAILS.md confusion]
│   └─> Entries in wrong file
└─> [.windsurf/ vs DevSystemV3.2/ confusion]
    └─> Edits in wrong location
```

#### Root Cause

**Root cause**: Relied on memory for file locations instead of verifying against workflow documentation.

**Counterfactual**: If we had checked workflow Step 7 (SESSION-FIRST rule) before writing, then entries would go to correct files.

**Prevention**:
1. Before writing to tracking files, verify path against workflow rules
2. For source/sync pairs (DevSystemV3.2 -> .windsurf), always edit source first
3. When in doubt, `ls` the directory to confirm file names

---

## Summary

| ID | Topic | Key Takeaway |
|----|-------|--------------|
| LN-001 | API Design | Explicit parameter names over brevity |
| LN-002 | Overengineering | YAGNI - start minimal, add on demand |
| LN-003 | File Matching | Filter metadata, validate content |
| LN-004 | File Discipline | Verify paths against workflow rules |

## Document History

**[2026-01-22 22:01]**
- Initial learnings extracted from FL-001 through FL-007
- 4 consolidated learnings from 7 failure entries
