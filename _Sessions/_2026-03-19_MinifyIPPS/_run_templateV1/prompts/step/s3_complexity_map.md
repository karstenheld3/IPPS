# Step 3: File Complexity Map (FR-03)

You are analyzing a DevSystem. All files are provided in the context above. You also have the call tree analysis from Step 2.

## Task

Create a comprehensive complexity map document (`_02_FILE_COMPLEXITY_MAP.md`) with these sections:

### 1. Concept Inventory
Exhaustive list of concepts the agent must remember across all files. Group by category (rules, patterns, conventions, workflows, skills).

### 2. Per-File Complexity Analysis
For each file, provide:
- **Path**: Relative file path
- **Lines**: Total line count
- **Tokens**: Approximate token count
- **Concepts**: Number of new concepts introduced
- **Rules**: Number of rules defined
- **Steps**: Number of procedural steps defined
- **Branching**: Count of conditional behaviors (if/when/unless clauses)
- **Load frequency**: From call tree (how many other files trigger loading this file)

### 3. Complexity Rankings
Sort files by composite complexity score (weighted: tokens * 0.4 + concepts * 0.2 + rules * 0.2 + branching * 0.1 + load_frequency * 0.1). Show top 20 most complex files.

## Output Format

Write the complete `_02_FILE_COMPLEXITY_MAP.md` document. Use exact file paths. All counts must be verifiable against the source files.

## Quality Criteria

- Every file from the bundle must have an entry
- Token counts must be approximate but reasonable
- Concept counts must be traceable to specific items in the file
- Rankings must be mathematically correct
