# Step 2: File Call Tree Analysis (FR-02)

You are analyzing a DevSystem consisting of rules, workflows, and skills files. All files are provided in the context above.

## Task

Create a comprehensive file call tree document (`_01_FILE_CALL_TREE.md`) with these sections:

### 1. Startup Sequence
List all files loaded at agent startup, in order. Rules are loaded first, then other required files.

### 2. Workflow Call Trees
For each workflow file, document:
- Which files it loads directly
- Which files those files load (recursive)
- Show the full call tree with indentation

### 3. Skill Call Trees
For each skill (SKILL.md files), document:
- Files loaded on skill invocation
- Additional files loaded via progressive disclosure
- Recursive dependencies

### 4. File Reference List (Reverse Index)
For each file in the system, list all other files that trigger its loading. Format:
```
[file_path]: loaded_by_count references
  - triggered by: [list of files that load this file]
```

## Output Format

Write the complete `_01_FILE_CALL_TREE.md` document. Use exact file paths as they appear in the bundle headers. Include reference counts for each file.

## Quality Criteria

- Every file in the bundle must appear in the reverse index
- Reference counts must be accurate
- Recursive call chains must be fully expanded
- Startup sequence must be complete
