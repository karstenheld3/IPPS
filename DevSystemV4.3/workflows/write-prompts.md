---
description: Create prompt queue files (_PROMPTS_[Topic].md) for sequential headless execution
---

# Write Prompts Workflow

Create `_PROMPTS_[Topic].md` files containing an ordered list of prompts. Each prompt is a fenced code block. Prompts execute sequentially as turns of ONE session.

**Goal**: Validated `_PROMPTS_[Topic].md` file with focused, verifiable prompts

**Why**: Headless prompts must be complete on first submission - no human correction loop

## Required Skills

- @write-documents `PROMPTS_TEMPLATE.md` for file skeleton (copy and fill)
- @write-documents `PROMPTS_GUIDES.md` for strategic approach (read BEFORE writing)
- @write-documents `PROMPTS_RULES.md` for output verification (PRMT-* rules)

## MUST-NOT-FORGET

- First non-empty line MUST be an opening fence (no header block, no frontmatter)
- Fence length: 3-9 backticks per prompt. Outer fence MUST exceed deepest inner fence
- `---` separator between every pair of consecutive prompts
- Commentary (headings, notes) only between `---` and next fence - never sent to model
- At least one prompt per file
- **NEVER modify tracking documents** (PROGRESS.md, PROBLEMS.md, NOTES.md, FAILS.md). Write-* workflows create NEW files only.
- Pre-Write Privacy Gate (`agent-behavior.md`): General-purpose documents → all content generic. ILLUSTRATIVE content → examples generic.

## Prerequisites

- User has described one or more prompts to execute sequentially
- Determine if prompts contain code blocks (affects fence length)

## Step 1: Read PROMPTS_GUIDES.md

Read `PROMPTS_GUIDES.md` from @write-documents. Classify the task, decide decomposition, plan state flow between prompts.

## Step 2: Determine File Location and Name

- Filename: `_PROMPTS_[Topic].md`
- `[Topic]` = CamelCase description of prompt purpose
- Location: session folder (default), workspace root, or user-specified path
- Examples: `_PROMPTS_SetupProject.md`, `_PROMPTS_MigrateAuth.md`, `_PROMPTS_AnalyzePerformance.md`

## Step 3: Select Fence Length Per Prompt

For each prompt, find the deepest inner fence and set the outer fence one longer.

- Prompt has no code blocks → 3 backticks
- Prompt contains ``` blocks → 4+ backtick outer fence
- Prompt contains ```` blocks (e.g. markdown examples with ``` inside) → 5+ backtick outer fence
- Maximum outer fence: 9 backticks. If deeper nesting needed, restructure the prompt.

## Step 4: Write Prompts File

**Format overview** (3-prompt example):

`````markdown
```
First prompt text. Plain instruction, no code blocks inside.
```

---

## Step 2 - commentary heading (never sent to model)

Optional notes explaining the next prompt's purpose.

````
Second prompt with a code block inside:
```python
print("hello")
```
````

---

```
Third prompt. Simple again.
```
`````

**Format rules:**
1. First non-empty line = opening fence
2. Each prompt = opening fence + prompt text + closing fence
3. Closing fence = line with >= N backticks (where N = opening fence length)
4. `---` on its own line between consecutive prompts
5. Commentary (headings, paragraphs, lists) allowed only between `---` and next opening fence
6. Info string after opening fence (e.g. `` ```text ``) is optional and ignored by executor
7. Prompts execute in file order

## Step 5: Verify

Check output against all PRMT-* rules in `PROMPTS_RULES.md`:

- [ ] Format (FT): PRMT-FT-01 through PRMT-FT-06
- [ ] Structure (ST): PRMT-ST-01 through PRMT-ST-05
- [ ] Sequence (SQ): PRMT-SQ-01 through PRMT-SQ-03
- [ ] Content (CT): PRMT-CT-01 through PRMT-CT-07

## Output

Validated `_PROMPTS_[Topic].md` file in target location.

## Quality Gate

- [ ] All PRMT-* rules pass (Step 5)
- [ ] Privacy gate applied (no real project data in examples)
- [ ] Fence depths verified (outer > deepest inner per prompt)
