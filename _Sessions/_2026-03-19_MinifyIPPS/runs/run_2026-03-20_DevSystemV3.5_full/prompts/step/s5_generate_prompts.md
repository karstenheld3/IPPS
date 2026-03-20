# Step 5: Generate Compression Prompts (FR-05)

You are generating compression prompts for different file types in a DevSystem. The full system is provided in context above, along with the compression strategy.

## Task

For each file type in the file_type_map, generate two prompts:

### 1. Transform Prompt
Instructions for compressing a file of that type. The prompt must:
- Reference the compression strategy (Primary/Secondary/Drop classifications)
- Specify what to keep, what to compress, and what to remove
- Include formatting rules specific to the file type
- Preserve all functional content (rules, steps, conditions)
- Sacrifice examples, verbose explanations, and redundant formatting

### 2. Evaluation Prompt
Instructions for judging compression quality. The prompt must:
- Define scoring criteria (1-5 scale)
- Score 5: All functional content preserved, significant size reduction
- Score 4: Minor omissions that don't affect behavior
- Score 3: Some functional content lost but core preserved
- Score 2: Significant functional content lost
- Score 1: Critical content missing, would break agent behavior
- Specify minimum acceptable score: 3.5

## File Types to Generate For

{file_types_list}

Also generate a `compress_other` fallback prompt pair for files not matching any specific type.

## Output Format

Return a JSON object:
```json
{
  "compress_rules": {"transform": "...", "eval": "..."},
  "compress_workflows": {"transform": "...", "eval": "..."},
  ...
  "compress_other": {"transform": "...", "eval": "..."}
}
```
