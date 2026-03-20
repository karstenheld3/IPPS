# Step 6: Compress File (FR-06)

You are compressing a DevSystem file according to the compression strategy and type-specific instructions.

## Context

The full DevSystem is available in the cached context above. The compression strategy classifies content as Primary (keep), Secondary (compress), or Drop (remove).

## File to Compress

**Path**: {file_path}
**Type**: {file_type}
**Original content**:
```
{file_content}
```

## Compression Instructions

{transform_prompt}

## Rules

1. Preserve ALL functional content: rules, conditions, steps, triggers, dependencies
2. Remove: verbose examples, redundant explanations, excessive formatting
3. Compress: BAD/GOOD pairs to single correct example, multi-paragraph explanations to key points
4. Keep: exact file references, variable names, command syntax, config keys
5. Output ONLY the compressed file content - no explanations, no metadata
6. The compressed output must be valid markdown that an agent can parse and follow

## Quality Target

The output will be scored 1-5. Target: >= 3.5/5.0.
If your first attempt scores below 3.5, you will be asked to refine once.
